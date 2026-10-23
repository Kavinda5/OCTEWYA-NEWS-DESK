"""
Market Data & Yields Intelligence Module
Handles live pricing for XAUUSD, US02Y, US10Y, DXY,
and calculates Buyer/Seller dominance, Yield Pressure, and Regime Duration.
"""

import time
import math
import numpy as np
import pandas as pd
import yfinance as yf

from datetime import datetime, timezone, timedelta

TIMEZONES = {
    "SL": ("Sri Lanka (UTC+5:30)", 5, 30),
    "UTC": ("UTC / GMT (Server)", 0, 0),
    "DXB": ("Dubai (UTC+4:00)", 4, 0),
    "LDN": ("London (UTC+1:00)", 1, 0),
    "NY": ("New York (UTC-4:00)", -4, 0)
}

def get_current_time_str(tz_key: str = "SL") -> str:
    """Returns formatted time for selected timezone (default Sri Lanka)."""
    tz_info = TIMEZONES.get(tz_key, TIMEZONES["SL"])
    hours, mins = tz_info[1], tz_info[2]
    dt = datetime.now(timezone.utc) + timedelta(hours=hours, minutes=mins)
    return dt.strftime("%I:%M:%S %p")

def get_current_sl_time_str() -> str:
    return get_current_time_str("SL")

# Fallback cache to prevent API rate limiting
_CACHE = {
    "last_fetch": 0,
    "data": None
}

def fetch_live_macro_data(ttl_seconds: int = 30) -> dict:
    """
    Fetches real-time price, yield, and index data with in-memory caching.
    """
    now = time.time()
    if _CACHE["data"] and (now - _CACHE["last_fetch"] < ttl_seconds):
        return _CACHE["data"]

    result = {
        "gold_price": 2735.50,
        "gold_change": 0.0,
        "gold_change_pct": 0.0,
        "gold_high": 2742.00,
        "gold_low": 2728.00,
        "gold_atr": 14.50,
        "us10y_yield": 4.225,
        "us10y_change": 0.0,
        "us02y_yield": 4.110,
        "us02y_change": 0.0,
        "yield_spread": 0.115, # 10Y - 2Y in % (11.5 bps)
        "dxy_price": 103.85,
        "dxy_change": 0.0,
        "oil_price": 75.00,
        "oil_change": 0.0,
        "oil_change_pct": 0.0,
        "oil_spike": False,
        "vwap": 2735.0,
        "vwap_dist": 0.0,
        "vwap_status": "AT_VWAP",
        "cvd_value": 0,
        "cvd_trend": "NEUTRAL",
        "orderflow_event": "NORMAL_LIQUIDITY",
        "orderflow_bias": "NEUTRAL_FLOW",
        "yield_momentum_desc": "Flat / Neutral Yield Drift",
        "buyers_pct": 58,
        "sellers_pct": 42,
        "yield_pressure": "NEUTRAL",
        "regime": "COMPRESSION",
        "estimated_duration": "1 - 2 Hours",
        "breakout_risk_pct": 65,
        "gold_history": None,
        "sync_time": get_current_sl_time_str()
    }

    try:
        # 1. Fetch Gold Futures (GC=F)
        gold = yf.Ticker("GC=F")
        g_hist = gold.history(period="5d", interval="1h")
        if not g_hist.empty:
            latest_g = g_hist.iloc[-1]
            prev_g = g_hist.iloc[-2] if len(g_hist) > 1 else latest_g
            result["gold_price"] = float(latest_g["Close"])
            result["gold_high"] = float(latest_g["High"])
            result["gold_low"] = float(latest_g["Low"])
            result["gold_change"] = float(latest_g["Close"] - prev_g["Close"])
            result["gold_change_pct"] = float((result["gold_change"] / prev_g["Close"]) * 100)
            
            # Simple ATR estimation
            high_low = g_hist["High"] - g_hist["Low"]
            result["gold_atr"] = float(high_low.tail(14).mean()) if len(g_hist) >= 14 else float(high_low.mean())
            result["gold_history"] = g_hist

        # 2. Fetch US 10-Year Yield (^TNX)
        tnx = yf.Ticker("^TNX")
        tnx_hist = tnx.history(period="5d", interval="1d")
        if not tnx_hist.empty:
            latest_tnx = tnx_hist.iloc[-1]["Close"]
            prev_tnx = tnx_hist.iloc[-2]["Close"] if len(tnx_hist) > 1 else latest_tnx
            result["us10y_yield"] = float(latest_tnx)
            result["us10y_change"] = float(latest_tnx - prev_tnx)

        # 3. Fetch US Short-Term Treasury Proxy (^IRX & ^FVX to derive US02Y)
        irx = yf.Ticker("^IRX")
        irx_hist = irx.history(period="5d", interval="1d")
        fvx = yf.Ticker("^FVX")
        fvx_hist = fvx.history(period="5d", interval="1d")
        
        if not irx_hist.empty and not fvx_hist.empty:
            irx_val = irx_hist.iloc[-1]["Close"]
            fvx_val = fvx_hist.iloc[-1]["Close"]
            derived_2y = (0.55 * irx_val) + (0.45 * fvx_val)
            prev_2y = (0.55 * irx_hist.iloc[-2]["Close"]) + (0.45 * fvx_hist.iloc[-2]["Close"]) if len(irx_hist) > 1 else derived_2y
            result["us02y_yield"] = float(derived_2y)
            result["us02y_change"] = float(derived_2y - prev_2y)
        elif not tnx_hist.empty:
            result["us02y_yield"] = float(result["us10y_yield"] - 0.15)
            result["us02y_change"] = float(result["us10y_change"] * 0.9)

        result["yield_spread"] = float(result["us10y_yield"] - result["us02y_yield"])

        # 4. Fetch DXY (DX-Y.NYB)
        dxy = yf.Ticker("DX-Y.NYB")
        dxy_hist = dxy.history(period="5d", interval="1d")
        if not dxy_hist.empty:
            latest_dxy = dxy_hist.iloc[-1]["Close"]
            prev_dxy = dxy_hist.iloc[-2]["Close"] if len(dxy_hist) > 1 else latest_dxy
            result["dxy_price"] = float(latest_dxy)
            result["dxy_change"] = float(latest_dxy - prev_dxy)

        # 5. Fetch Crude Oil (CL=F) for Energy / War Surge Detection
        try:
            oil = yf.Ticker("CL=F")
            oil_hist = oil.history(period="3d", interval="1d")
            if not oil_hist.empty:
                latest_oil = float(oil_hist.iloc[-1]["Close"])
                prev_oil = float(oil_hist.iloc[-2]["Close"]) if len(oil_hist) > 1 else latest_oil
                result["oil_price"] = latest_oil
                result["oil_change"] = float(latest_oil - prev_oil)
                result["oil_change_pct"] = float((result["oil_change"] / prev_oil) * 100) if prev_oil > 0 else 0.0
                result["oil_spike"] = (result["oil_change_pct"] >= 1.8)
        except Exception:
            pass

        # 6. Quantitative Order Flow & VWAP Analysis (5m Intraday Bars)
        try:
            g_5m = gold.history(period="1d", interval="5m")
            if not g_5m.empty and g_5m["Volume"].sum() > 0:
                tp = (g_5m["High"] + g_5m["Low"] + g_5m["Close"]) / 3.0
                vol = g_5m["Volume"].replace(0, 1)
                vwap_series = (tp * vol).cumsum() / vol.cumsum()
                curr_vwap = float(vwap_series.iloc[-1])
                curr_price = float(g_5m["Close"].iloc[-1])
                result["vwap"] = curr_vwap
                result["vwap_dist"] = curr_price - curr_vwap
                result["vwap_status"] = "ABOVE_VWAP" if result["vwap_dist"] > 0.5 else ("BELOW_VWAP" if result["vwap_dist"] < -0.5 else "AT_VWAP")

                # Cumulative Volume Delta (CVD)
                delta_bar = np.where(g_5m["Close"] >= g_5m["Open"], g_5m["Volume"], -g_5m["Volume"])
                cvd_series = delta_bar.cumsum()
                result["cvd_value"] = int(cvd_series.iloc[-1])
                
                # Check recent 6 bars (last 30 mins) CVD slope
                recent_cvd = cvd_series.iloc[-6:] if len(cvd_series) >= 6 else cvd_series
                if recent_cvd.iloc[-1] > recent_cvd.iloc[0] + 50:
                    result["cvd_trend"] = "BUYER_DOMINANT"
                elif recent_cvd.iloc[-1] < recent_cvd.iloc[0] - 50:
                    result["cvd_trend"] = "SELLER_DOMINANT"
                else:
                    result["cvd_trend"] = "NEUTRAL"

                # Absorption & Exhaustion Detection on last bar
                last_bar = g_5m.iloc[-1]
                bar_range = max(last_bar["High"] - last_bar["Low"], 0.2)
                upper_wick = last_bar["High"] - max(last_bar["Open"], last_bar["Close"])
                lower_wick = min(last_bar["Open"], last_bar["Close"]) - last_bar["Low"]
                avg_vol = g_5m["Volume"].tail(15).mean()
                curr_vol = last_bar["Volume"]

                if (lower_wick / bar_range > 0.45) and (curr_vol > avg_vol * 1.15):
                    result["orderflow_event"] = "BULLISH_ABSORPTION"
                elif (upper_wick / bar_range > 0.45) and (curr_vol > avg_vol * 1.15):
                    result["orderflow_event"] = "BEARISH_ABSORPTION"
                elif (curr_vol < avg_vol * 0.55) and (curr_price > curr_vwap + 5.0):
                    result["orderflow_event"] = "BUYER_EXHAUSTION"
                elif (curr_vol < avg_vol * 0.55) and (curr_price < curr_vwap - 5.0):
                    result["orderflow_event"] = "SELLER_EXHAUSTION"
                else:
                    result["orderflow_event"] = "NORMAL_LIQUIDITY"

                # Combined Order Flow Bias
                if result["vwap_status"] == "ABOVE_VWAP" and result["cvd_trend"] == "BUYER_DOMINANT":
                    result["orderflow_bias"] = "BULLISH_FLOW"
                elif result["vwap_status"] == "BELOW_VWAP" and result["cvd_trend"] == "SELLER_DOMINANT":
                    result["orderflow_bias"] = "BEARISH_FLOW"
                elif result["orderflow_event"] == "BULLISH_ABSORPTION":
                    result["orderflow_bias"] = "BULLISH_FLOW"
                elif result["orderflow_event"] == "BEARISH_ABSORPTION":
                    result["orderflow_bias"] = "BEARISH_FLOW"
                else:
                    result["orderflow_bias"] = "MIXED_FLOW"
        except Exception:
            pass

    except Exception as e:
        # Keep realistic default fallbacks if network has brief glitch
        pass

    # 7. Calculate Quantitative Buyer vs Seller Dominance Ratio
    high_low_range = max(result["gold_high"] - result["gold_low"], 1.0)
    pos_in_range = (result["gold_price"] - result["gold_low"]) / high_low_range
    
    # Base calculation adjusted by order flow and yield pressure
    base_buyers = int(pos_in_range * 60 + 20)
    if result["us10y_change"] > 0.02:
        base_buyers -= 7
    elif result["us10y_change"] < -0.02:
        base_buyers += 7

    if result.get("orderflow_bias") == "BULLISH_FLOW":
        base_buyers += 8
    elif result.get("orderflow_bias") == "BEARISH_FLOW":
        base_buyers -= 8

    result["buyers_pct"] = max(min(base_buyers, 88), 12)
    result["sellers_pct"] = 100 - result["buyers_pct"]

    # 8. Dynamic Yield Momentum on Gold (Intraday Delta)
    if result["us10y_change"] < -0.015:
        result["yield_pressure"] = "BULLISH_ON_GOLD"
        result["yield_momentum_desc"] = "Falling Yields (Bullish Gold Tailwinds)"
    elif result["us10y_change"] > 0.015:
        result["yield_pressure"] = "BEARISH_ON_GOLD"
        result["yield_momentum_desc"] = "Rising Yields (Bearish Sell Pressure)"
    else:
        result["yield_pressure"] = "NEUTRAL"
        result["yield_momentum_desc"] = "Flat / Neutral Yield Drift"

    # 9. Regime & Move Duration
    if result["gold_history"] is not None and len(result["gold_history"]) >= 5:
        recent_bars = result["gold_history"].tail(5)
        bar_range_avg = (recent_bars["High"] - recent_bars["Low"]).mean()
        if bar_range_avg < (result["gold_atr"] * 0.75):
            result["regime"] = "COMPRESSION"
            result["estimated_duration"] = "1 - 3 Hours (Tight Range before Breakout)"
            result["breakout_risk_pct"] = 78
        elif bar_range_avg > (result["gold_atr"] * 1.3):
            result["regime"] = "EXPANSION"
            result["estimated_duration"] = "30 - 60 Mins (High Volatility Scalp Move)"
            result["breakout_risk_pct"] = 92
        else:
            result["regime"] = "ORDERLY_TREND"
            result["estimated_duration"] = "2 - 4 Hours (Session Trend)"
            result["breakout_risk_pct"] = 45

    _CACHE["last_fetch"] = now
    _CACHE["data"] = result
    return result
