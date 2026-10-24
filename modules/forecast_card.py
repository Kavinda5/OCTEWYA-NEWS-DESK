"""
Forecast Card & Multi-Day Order Flow Renderer
Renders high-visibility dynamic probability radar and price targets for OCTEWYA.
"""

def render_forecast_html(forecast_data: dict, lang_choice: str = "si") -> str:
    forecast_title = "🔮 ඉදිරි දින සඳහා ආයතනික මිල පුරෝකථනය (NEXT SESSION & MULTI-DAY FORECAST)" if lang_choice == "si" else "🔮 NEXT SESSION & MULTI-DAY ORDER FLOW FORECAST"
    sell_prob = forecast_data.get("sell_prob", 66)
    buy_prob = forecast_data.get("buy_prob", 34)
    primary_dir = forecast_data.get("primary_dir", "SELL")
    
    session_label = "NEXT MONDAY" if lang_choice == "si" else "NEXT SESSION"
    
    bearish_t1 = forecast_data.get("bearish_t1", "$3989.1 - $3993.1")
    bearish_t2 = forecast_data.get("bearish_t2", "$3955.9 - $3962.9")
    bullish_t1 = forecast_data.get("bullish_t1", "$4037.6 - $4044.6")
    bullish_t2 = forecast_data.get("bullish_t2", "$4140.9")
    
    reason_text = forecast_data.get("reason_si" if lang_choice == "si" else "reason_en", "")
    inval_bear = forecast_data.get("invalidation_bearish", "$4025.5")
    inval_bull = forecast_data.get("invalidation_bullish", "$3985.1")

    return (
        f'<div style="background: rgba(15, 23, 42, 0.9); border: 1.5px solid #334155; border-radius: 10px; padding: 14px 16px; margin-top: 14px; box-shadow: 0 4px 16px rgba(0,0,0,0.4);">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 8px;">'
        f'<span style="font-size: 14px; font-weight: 800; color: #F59E0B; letter-spacing: 0.5px;">{forecast_title}</span>'
        f'<div style="display: flex; align-items: center; gap: 8px;">'
        f'<span style="background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid #38BDF8; font-size: 11.5px; font-weight: 700; padding: 2px 8px; border-radius: 4px;">📈 TradingView / MT5 (XAUUSD) Synced</span>'
        f'<span style="background: #10B98122; color: #10B981; border: 1px solid #10B981; font-size: 12px; font-weight: 800; padding: 2px 9px; border-radius: 4px;">● DYNAMIC LIVE RADAR</span>'
        f'</div>'
        f'</div>'
        f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 12px;">'
        f'<div style="background: rgba(239, 68, 68, 0.15); border: 1.5px solid #EF4444; border-radius: 8px; padding: 10px; text-align: center;">'
        f'<div style="font-size: 13px; font-weight: 800; color: #FCA5A5; text-transform: uppercase;">🔴 {session_label} SELL PROBABILITY</div>'
        f'<div style="font-size: 26px; font-weight: 900; color: #EF4444; line-height: 1.2; margin: 2px 0;">{sell_prob}%</div>'
        f'<div style="font-size: 12px; color: #CBD5E1;">(Yields 4.99% & Sub-VWAP)</div>'
        f'</div>'
        f'<div style="background: rgba(16, 185, 129, 0.15); border: 1.5px solid #10B981; border-radius: 8px; padding: 10px; text-align: center;">'
        f'<div style="font-size: 13px; font-weight: 800; color: #86EFAC; text-transform: uppercase;">🟢 {session_label} BUY PROBABILITY</div>'
        f'<div style="font-size: 26px; font-weight: 900; color: #10B981; line-height: 1.2; margin: 2px 0;">{buy_prob}%</div>'
        f'<div style="font-size: 12px; color: #CBD5E1;">(Crude $103 Spike & Safe Haven)</div>'
        f'</div>'
        f'</div>'
        f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px;">'
        f'<div style="background: rgba(0, 0, 0, 0.4); border-left: 4px solid #EF4444; border-radius: 6px; padding: 9px 12px;">'
        f'<div style="font-size: 13px; font-weight: 800; color: #EF4444;">🔴 ප්‍රධාන පහළ ඉලක්ක (Bearish Targets):</div>'
        f'<div style="font-size: 13.5px; color: #F1F5F9; font-weight: 700; margin-top: 4px;">• Target 1: <span style="color:#FCA5A5;">{bearish_t1}</span> <span style="font-size:11.5px; color:#94A3B8;">(SSL / News Low)</span></div>'
        f'<div style="font-size: 13.5px; color: #F1F5F9; font-weight: 700; margin-top: 3px;">• Target 2: <span style="color:#FCA5A5;">{bearish_t2}</span> <span style="font-size:11.5px; color:#94A3B8;">(Daily FVG Block)</span></div>'
        f'<div style="font-size: 12px; color: #F87171; margin-top: 4px; font-weight: 600;">⚠️ අවලංගු වීම: Reclaim above {inval_bear}</div>'
        f'</div>'
        f'<div style="background: rgba(0, 0, 0, 0.4); border-left: 4px solid #10B981; border-radius: 6px; padding: 9px 12px;">'
        f'<div style="font-size: 13px; font-weight: 800; color: #10B981;">🟢 විකල්ප ඉහළ ඉලක්ක (Bullish Targets):</div>'
        f'<div style="font-size: 13.5px; color: #F1F5F9; font-weight: 700; margin-top: 4px;">• Target 1: <span style="color:#86EFAC;">{bullish_t1}</span> <span style="font-size:11.5px; color:#94A3B8;">(VWAP / Value Area)</span></div>'
        f'<div style="font-size: 13.5px; color: #F1F5F9; font-weight: 700; margin-top: 3px;">• Target 2: <span style="color:#86EFAC;">{bullish_t2}</span> <span style="font-size:11.5px; color:#94A3B8;">(VPOC Magnet)</span></div>'
        f'<div style="font-size: 12px; color: #4ADE80; margin-top: 4px; font-weight: 600;">⚠️ අවලංගු වීම: Break below {inval_bull}</div>'
        f'</div>'
        f'</div>'
        f'<div style="background: rgba(30, 41, 59, 0.7); border-radius: 6px; padding: 9px 12px; margin-top: 8px;">'
        f'<div style="font-size: 12.5px; font-weight: 800; color: #F59E0B; margin-bottom: 3px;">💡 ආයතනික හේතුව සහ Order Flow විග්‍රහය (Institutional Rationale):</div>'
        f'<div style="font-size: 13px; color: #E2E8F0; line-height: 1.5;">{reason_text}</div>'
        f'</div>'
        f'</div>'
    )
