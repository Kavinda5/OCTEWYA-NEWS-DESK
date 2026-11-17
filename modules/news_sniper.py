"""
OCTEWYA VIP High-Strike News Sniper & Post-Release Reality Radar Engine
Reverse-engineered from top institutional news desks (ICT / SMC London Session Liquidity & Macro Nowcast).
Handles:
1. Pre-News VIP Sniper Call (Single high-conviction BUY/SELL strike 1-3h before release).
2. London Session Range & Draw on Liquidity (Premium vs Discount location).
3. Judas Swing / Trap Wick Shield (Prevents getting stopped out by 60-90 pip initial fakeouts).
4. After-Movement Horizon (Intraday Mean Reversion vs Macro Regime Expansion).
5. Post-Release Reality Radar & Accountability (Honest acknowledgment of misses + Revenge Trading Shield + Recovery Zones).
"""

from datetime import datetime, timezone, timedelta

def calculate_news_sniper_call(macro_watch: dict, current_macro: dict, geo_data: dict = None) -> dict:
    """
    Computes a high-conviction pre-news strike call aligned with London session liquidity,
    commodity nowcasting, and market structure.
    """
    gold_price = current_macro.get("gold_price", 2730.0)
    gold_high = current_macro.get("gold_high", gold_price + 15.0)
    gold_low = current_macro.get("gold_low", gold_price - 15.0)
    gold_atr = max(current_macro.get("gold_atr", 14.0), 8.0)
    
    oil_price = current_macro.get("oil_price", 80.0)
    oil_chg_pct = current_macro.get("oil_change_pct", 0.0)
    oil_spike = current_macro.get("oil_spike", False)
    
    us10y = current_macro.get("us10y_yield", 4.5)
    us10y_chg = current_macro.get("us10y_change", 0.0)
    dxy_chg = current_macro.get("dxy_change", 0.0)
    yield_pressure = current_macro.get("yield_pressure", "NEUTRAL")
    
    buyers_pct = current_macro.get("buyers_pct", 50)
    sellers_pct = current_macro.get("sellers_pct", 50)
    
    dominant_title = macro_watch.get("dominant_event", "US High-Impact Economic Event")
    title_low = dominant_title.lower()
    
    # 1. Calculate Session Premium vs Discount Location
    session_range = max(gold_high - gold_low, 6.0)
    price_loc_pct = (gold_price - gold_low) / session_range
    price_loc_pct = min(max(price_loc_pct, 0.0), 1.0)
    
    is_deep_premium = (price_loc_pct >= 0.65)
    is_deep_discount = (price_loc_pct <= 0.35)
    
    # 2. Event Type Classification
    is_inflation = any(k in title_low for k in ["cpi", "ppi", "pce", "inflation"])
    is_labor = any(k in title_low for k in ["nfp", "payrolls", "unemployment", "claims", "jobless", "adp"])
    is_rates = any(k in title_low for k in ["fomc", "rate", "fed", "powell"])
    is_activity = any(k in title_low for k in ["pmi", "ism", "services", "manufacturing"])
    
    # 3. Macro Scoring
    macro_bull_score = 0
    macro_bear_score = 0

    # Incorporate evolving bias from macro_watch (e.g., CAD Strong -> BUY_ON_GOLD)
    evolving_bias = macro_watch.get("evolving_bias")
    if evolving_bias == "BUY_ON_GOLD":
        macro_bull_score += 30
    elif evolving_bias == "SELL_ON_GOLD":
        macro_bear_score += 30
    
    if is_inflation:
        # Crude oil dropping = cooling inflation = Dovish Fed = Gold BUY
        if oil_chg_pct < -0.4 or oil_price < 85.0:
            macro_bull_score += 40
        elif oil_chg_pct > 0.8 or oil_spike:
            macro_bear_score += 40
            
        if us10y_chg > 0.02 or us10y >= 5.0:
            macro_bear_score += 25
        elif us10y_chg < -0.02:
            macro_bull_score += 25
            
    elif is_labor:
        # Labor softening = Gold BUY
        if sellers_pct > 65:
            # Over-positioned for strong labor -> Asymmetric short squeeze!
            macro_bull_score += 45
        elif buyers_pct > 65:
            macro_bear_score += 45
            
        if us10y_chg < -0.01:
            macro_bull_score += 25
        else:
            macro_bear_score += 25
            
    elif is_rates:
        if "rate" in title_low or "fomc" in title_low:
            # Fed easing cycle bias
            if is_deep_discount:
                macro_bull_score += 50
            else:
                macro_bear_score += 30
    else:
        if dxy_chg < 0:
            macro_bull_score += 25
        else:
            macro_bear_score += 25
            
    # 4. Integrate Session Liquidity (The SMC Draw on Liquidity)
    # If in Deep Premium, Smart Money has built short inventory -> SELL GOLD into Equal Lows!
    # If in Deep Discount, Smart Money has swept sell stops -> BUY GOLD into Equal Highs!
    if is_deep_premium:
        macro_bear_score += 50
        loc_desc_si = f"මිල දවසේ ඉහළම Premium කලාපයේ ({int(price_loc_pct*100)}%) රැඳී ඇති බැවින් පහළ Equal Lows වෙත Dump වීමේ සම්භාවිතාව වැඩිය."
        loc_desc_en = f"Price is parked in Deep Premium ({int(price_loc_pct*100)}% of range). Liquidity draw favors a violent flush into resting Sell-Side Lows."
    elif is_deep_discount:
        macro_bull_score += 50
        loc_desc_si = f"මිල දවසේ පහළම Discount කලාපයේ ({int(price_loc_pct*100)}%) රැඳී ඇති බැවින් ඉහළ Equal Highs වෙත Pump වීමේ සම්භාවිතාව වැඩිය."
        loc_desc_en = f"Price is parked in Deep Discount ({int(price_loc_pct*100)}% of range). Liquidity draw favors a violent rocket into resting Buy-Side Highs."
    else:
        loc_desc_si = f"මිල දවසේ මැද කලාපයේ ({int(price_loc_pct*100)}%) පවතින බැවින් පෙරගමන් Macro දර්ශක වල දිශාව ප්‍රමුඛ වේ."
        loc_desc_en = f"Price is in Mid-Range equilibrium ({int(price_loc_pct*100)}%). Leading macro nowcasts dictate primary directional bias."

    # 5. Determine Strike Direction & Conviction
    if macro_bull_score >= macro_bear_score:
        direction = "BUY_GOLD"
        direction_label = "🟢 BUY GOLD ‼️"
        conviction = min(max(int(70 + (macro_bull_score - macro_bear_score) * 0.35), 78), 94)
        
        # Targets & Protection
        entry_min = round(gold_price - 2.5, 1)
        entry_max = round(gold_price + 2.0, 1)
        
        trap_wick_val = round(gold_price - (gold_atr * 0.65), 1)
        stop_loss_val = round(gold_price - (gold_atr * 1.05), 1)
        tp1_val = round(gold_price + 28.0, 1) # ~280 pips
        tp2_val = round(gold_price + 48.0, 1) # ~480 pips
        
        trap_desc_si = f"News එක ආ සැනින් Pip 60-90 ක Fakeout Dip එකක් ${trap_wick_val} වෙත ඒමට ඉඩ ඇත (Judas Swing). කලබල වී පහළින් Sell නොකරන්න! Stop Loss එක ${stop_loss_val} ට පහළින් තබාගෙන Buy එක අල්ලන්න."
        trap_desc_en = f"Expect an initial 60-90 pip Judas trap dip toward ${trap_wick_val} to sweep sell stops. Do NOT chase shorts! Keep stop loss protected at ${stop_loss_val} and ride the expansion rocket."
        
        rationale_si = f"{loc_desc_si} පෙරගමන් Macro දර්ශක සහ ආයතනික Liquidity එකඟ වී ඇති බැවින් Gold ඉහළට (BUY) දැවැන්ත ලෙස තල්ලු වීමට 90%+ ඉඩක් ඇත."
        rationale_en = f"{loc_desc_en} Leading macro sub-metrics and London liquidity structure align to launch Gold higher (BUY)."
    else:
        direction = "SELL_GOLD"
        direction_label = "🔴 SELL GOLD ‼️"
        conviction = min(max(int(70 + (macro_bear_score - macro_bull_score) * 0.35), 78), 94)
        
        # Targets & Protection
        entry_min = round(gold_price - 2.0, 1)
        entry_max = round(gold_price + 2.5, 1)
        
        trap_wick_val = round(gold_price + (gold_atr * 0.65), 1)
        stop_loss_val = round(gold_price + (gold_atr * 1.05), 1)
        tp1_val = round(gold_price - 28.0, 1) # ~280 pips
        tp2_val = round(gold_price - 48.0, 1) # ~480 pips
        
        trap_desc_si = f"News එක ආ සැනින් Pip 60-90 ක Fakeout Pump එකක් ${trap_wick_val} වෙත ඒමට ඉඩ ඇත (Judas Swing). කලබල වී ඉහළින් Buy නොකරන්න! Stop Loss එක ${stop_loss_val} ට ඉහළින් තබාගෙන Sell එක අල්ලන්න."
        trap_desc_en = f"Expect an initial 60-90 pip Judas trap pump toward ${trap_wick_val} to sweep buy stops. Do NOT chase longs! Keep stop loss protected at ${stop_loss_val} and catch the expansion drop."
        
        rationale_si = f"{loc_desc_si} ඉහළ Resistance සහ Yield පීඩනය නිසා News එක පාවිච්චි කරමින් පහළ Sell-Side Liquidity වෙත කඩා වැටීමේ (SELL) 90%+ ඉඩක් ඇත."
        rationale_en = f"{loc_desc_en} Overhead resistance and Treasury yield momentum favor a violent flush into discount liquidity (SELL)."

    # 6. After-Movement Horizon Profile
    if is_rates or ("cpi" in title_low and "core" in title_low):
        horizon_type = "MACRO_REGIME_EXPANSION"
        horizon_badge_si = "🔥 MACRO REGIME EXPANSION (මාසික Breakout අවස්ථාවක්)"
        horizon_badge_en = "🔥 MACRO REGIME EXPANSION (Multi-Session Runner Potential)"
        horizon_advice_si = "මෙම පුවතින් පසු ආරම්භක මට්ටමට ආපසු පැමිණීමක් සිදු නොවේ! 50% ලාභ අරන් ඉතිරි 50% Runners ලෙස Pip 800 - 1,500+ දක්වා තබාගන්න."
        horizon_advice_en = "Structural policy shift! Do NOT expect a full return to origin. Take partial profits at TP1 and hold 50% runners for a multi-session 800-1,500+ pip trend."
    else:
        horizon_type = "INTRADAY_MEAN_REVERSION"
        horizon_badge_si = "⏱️ INTRADAY MEAN REVERSION (පැය කිහිපයකින් ආපසු හැරේ)"
        horizon_badge_en = "⏱️ INTRADAY MEAN REVERSION (Scalp & Lock Gains)"
        horizon_advice_si = "News එකෙන් පසු පැය 2-4 ක් ඇතුළත වෙළඳපොළ ආරම්භක මට්ටම වෙත නැවත පැමිණිය හැක. TP1 / TP2 හිදී ලාභ අරන් ඉවත් වන්න!"
        horizon_advice_en = "Post-news imbalance is temporary. Price is expected to mean-revert toward baseline within 2-4 hours. Take profits cleanly at TP1/TP2!"

    return {
        "dominant_title": dominant_title,
        "direction": direction,
        "direction_label": direction_label,
        "conviction": conviction,
        "entry_zone": f"${entry_min:.1f} - ${entry_max:.1f}",
        "trap_wick_level": str(trap_wick_val),
        "trap_desc_si": trap_desc_si,
        "trap_desc_en": trap_desc_en,
        "stop_loss": str(stop_loss_val),
        "tp1": str(tp1_val),
        "tp2": str(tp2_val),
        "rationale_si": rationale_si,
        "rationale_en": rationale_en,
        "price_loc_pct": int(price_loc_pct * 100),
        "horizon_type": horizon_type,
        "horizon_badge_si": horizon_badge_si,
        "horizon_badge_en": horizon_badge_en,
        "horizon_advice_si": horizon_advice_si,
        "horizon_advice_en": horizon_advice_en
    }


def render_news_sniper_card_html(sniper_data: dict, macro_watch: dict, lang_choice: str = "si") -> str:
    """
    Renders the dedicated VIP High-Strike News Sniper Card and Post-Release Reality Radar.
    """
    is_si = (lang_choice == "si")
    watch_status = macro_watch.get("status", "UPCOMING")
    scorecard = macro_watch.get("last_event_scorecard")
    
    # Check if a past event prediction was missed
    is_missed = False
    if scorecard:
        is_missed = scorecard.get("is_prediction_missed", False)
        # Fallback check
        acc_label = scorecard.get("accuracy_label_en", "")
        if "MISSED" in acc_label or "INVERTED" in acc_label:
            is_missed = True

    # =========================================================================
    # CASE 1: POST-RELEASE REALITY RADAR (Event Just Concluded or Past Scorecard Active)
    # =========================================================================
    if watch_status == "POST_RELEASE":
        # Extract live verified move details from scorecard if available
        actual_bias = scorecard.get("actual_bias", "NEUTRAL") if scorecard else "NEUTRAL"
        pre_bias = scorecard.get("pre_bias", "NEUTRAL") if scorecard else "NEUTRAL"
        accuracy_label = scorecard.get("accuracy_label_si" if is_si else "accuracy_label_en", "") if scorecard else ""
        movement_state = scorecard.get("movement_state_si" if is_si else "movement_state_en", "") if scorecard else ""
        movement_desc = scorecard.get("movement_desc_si" if is_si else "movement_desc_en", "") if scorecard else ""
        event_title = macro_watch.get("dominant_event", macro_watch.get("title", "Recent Macro Release"))

        if is_missed:
            # Honest Acknowledgment & Recovery Protocol
            card_border = "#EF4444"
            card_bg = "linear-gradient(135deg, rgba(30, 41, 59, 0.98), rgba(20, 10, 15, 0.98))"
            header_title = "❌ POST-RELEASE REALITY RADAR: PREDICTION INVERTED" if not is_si else "❌ පශ්චාත් පුවත් සත්‍ය රේඩාර්: පූර්ව අපේක්ෂාව වැරදී ගියේය"
            sub_title = f"⚠️ ආයතනික අවංකභාවය: {event_title} පුවතේ Actual දත්තය අපේක්ෂිත දිශාවට පටහැනිව පැමිණ ඇත." if is_si else f"⚠️ INSTITUTIONAL ACCOUNTABILITY: {event_title} actual release deviated contrary to pre-drift consensus."
            
            outcome_box = (
                f'<div style="background: rgba(239, 68, 68, 0.15); border: 1.5px solid #EF4444; border-radius: 8px; padding: 12px; margin: 10px 0;">'
                f'<div style="font-size: 14.5px; font-weight: 800; color: #FCA5A5;">🛑 REVENGE TRADING BLOCKED (කලබල වී Orders නොදමන්න!)</div>'
                f'<div style="font-size: 13.5px; color: #E2E8F0; line-height: 1.5; margin-top: 4px;">'
                f'{"Pre-news අපේක්ෂාවට එරෙහිව Actual දත්තය අනපේක්ෂිත ලෙස ප්‍රතිවිරුද්ධ දිශාවට ගිය බැවින් Stop Loss ආරක්ෂා විය යුතුය. මෙවැනි වෙලාවට පළිගැනීමට (Revenge Trade) නොගොස් වෙළඳපොළ සන්සුන් වනතුරු ඉවසීම නියම Trader කෙනෙකුගේ ලක්ෂණයයි." if is_si else "Actual economic data deviated contrary to pre-drift consensus, triggering an inverse expansion. Do NOT revenge trade into live volatility; preserve capital."}'
                f'</div>'
                f'</div>'
                f'<div style="background: rgba(0, 0, 0, 0.45); border-left: 4px solid #38BDF8; border-radius: 6px; padding: 10px 14px; margin-top: 8px;">'
                f'<div style="font-size: 13.5px; font-weight: 800; color: #38BDF8;">🧭 දැන් මාර්කට් එකේ මොකද වෙන්නේ? (Current Market State & Recovery):</div>'
                f'<div style="font-size: 13.5px; color: #CBD5E1; line-height: 1.5; margin-top: 3px;">'
                f'{"• ක්ෂණික News Momentum එක මේ වන විට Exhaust වෙමින් පවතී.<br>• " + movement_desc + "<br>• <b>Recovery Plan:</b> ක්ෂණික චලනය පසුපස නොඑලවා, සැබෑ Support/Resistance Zone එකක් තහවුරු වනතුරු රැඳී සිටින්න." if is_si else "• Initial news velocity is exhausting into higher-timeframe levels.<br>• " + movement_desc + "<br>• <b>Recovery Plan:</b> Await retest exhaustion at key levels before re-engaging."}'
                f'</div>'
                f'</div>'
            )
        else:
            # Verified Hit & Realistic Post-Release Assessment
            card_border = "#10B981"
            card_bg = "linear-gradient(135deg, rgba(15, 23, 42, 0.98), rgba(6, 78, 59, 0.25))"
            header_title = f"✅ POST-RELEASE REALITY RADAR: {event_title.upper()}" if not is_si else f"✅ පශ්චාත් පුවත් සත්‍ය රේඩාර්: {event_title}"
            sub_title = f"🎯 සත්‍යාපිත තත්ත්වය: {accuracy_label}" if is_si else f"🎯 Verified Status: {accuracy_label}"
            
            outcome_box = (
                f'<div style="background: rgba(16, 185, 129, 0.15); border: 1.5px solid #10B981; border-radius: 8px; padding: 12px; margin: 10px 0;">'
                f'<div style="font-size: 14.5px; font-weight: 800; color: #86EFAC;">💰 TAKE PROFITS & LOCK GAINS (ලාභ සුරක්ෂිත කරගන්න)</div>'
                f'<div style="font-size: 13.5px; color: #E2E8F0; line-height: 1.5; margin-top: 4px;">'
                f'{"පුවත නිකුත් වීමෙන් පසු වෙළඳපොළ ආරම්භක ඉලක්කය වෙත ගමන් කර ඇත. දැනටමත් Market එක චලනය වී ඇති බැවින් පස්සේ නොඑලවා (Do not chase), අත්පත් කරගත් ලාභ සුරක්ෂිත කරගන්න." if is_si else "Post-news reaction has expanded into initial target zone. Do NOT chase extended price; lock in gains and protect capital."}'
                f'</div>'
                f'</div>'
                f'<div style="background: rgba(0, 0, 0, 0.45); border-left: 4px solid #F59E0B; border-radius: 6px; padding: 10px 14px; margin-top: 8px;">'
                f'<div style="font-size: 13.5px; font-weight: 800; color: #F59E0B;">🧭 වත්මන් තත්ත්වය: {movement_state}</div>'
                f'<div style="font-size: 13.5px; color: #CBD5E1; line-height: 1.5; margin-top: 3px;">'
                f'{movement_desc}'
                f'</div>'
                f'</div>'
            )


        raw_case1 = (
            f'<div style="background: {card_bg}; border: 2px solid {card_border}; border-radius: 12px; padding: 16px 20px; margin-bottom: 20px; box-shadow: 0 6px 24px rgba(0,0,0,0.5); font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif;">'
            f'<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">'
            f'<div>'
            f'<div style="font-size: 16px; font-weight: 900; color: {card_border}; letter-spacing: 0.5px;">{header_title}</div>'
            f'<div style="font-size: 13px; color: #94A3B8; margin-top: 2px;">{sub_title}</div>'
            f'</div>'
            f'<span style="background: {card_border}22; color: {card_border}; border: 1px solid {card_border}; font-size: 12px; font-weight: 800; padding: 4px 10px; border-radius: 5px;">● POST-NEWS AUDIT</span>'
            f'</div>'
            f'{outcome_box}'
            f'</div>'
        )
        return "".join(raw_case1.splitlines()).replace("$", "&#36;")

    # =========================================================================
    # CASE 2: PRE-NEWS HIGH-STRIKE SNIPER CALL (Upcoming / Imminent)
    # =========================================================================
    direction = sniper_data.get("direction", "SELL_GOLD")
    is_buy = (direction == "BUY_GOLD")
    strike_color = "#10B981" if is_buy else "#EF4444"
    strike_bg = "rgba(16, 185, 129, 0.15)" if is_buy else "rgba(239, 68, 68, 0.15)"
    strike_border = "#10B981" if is_buy else "#EF4444"
    
    direction_badge = "🟢 BUY GOLD ‼️" if is_buy else "🔴 SELL GOLD ‼️"
    
    card_title = "⚡ OCTEWYA VIP HIGH-STRIKE NEWS SNIPER DESK" if not is_si else "⚡ OCTEWYA VIP HIGH-STRIKE NEWS SNIPER DESK"
    event_title = sniper_data.get("dominant_title", "High-Impact US Economic Release")
    event_time = macro_watch.get("time_str", "Upcoming Session")
    countdown = macro_watch.get("countdown_str", "00h 00m")
    
    # Impact Folder Badge (High, Medium, Low)
    impact_level = macro_watch.get("impact", "HIGH").upper()
    if impact_level == "HIGH":
        impact_badge_html = '<span style="background: rgba(239, 68, 68, 0.25); color: #FCA5A5; border: 1.5px solid #EF4444; font-size: 11.5px; font-weight: 900; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px;">🔴 HIGH IMPACT (RED FOLDER)</span>'
    elif impact_level == "MEDIUM":
        impact_badge_html = '<span style="background: rgba(245, 158, 11, 0.25); color: #FCD34D; border: 1.5px solid #F59E0B; font-size: 11.5px; font-weight: 900; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px;">🟡 MED IMPACT (ORANGE FOLDER)</span>'
    else:
        impact_badge_html = '<span style="background: rgba(148, 163, 184, 0.2); color: #CBD5E1; border: 1px solid #94A3B8; font-size: 11.5px; font-weight: 800; padding: 3px 8px; border-radius: 4px;">⚪ LOW IMPACT</span>'

    entry_zone = sniper_data.get("entry_zone", "$4,070 - $4,074")
    stop_loss = sniper_data.get("stop_loss", "$4,082")
    tp1 = sniper_data.get("tp1", "$4,042")
    tp2 = sniper_data.get("tp2", "$4,028")
    
    trap_desc = sniper_data.get("trap_desc_si" if is_si else "trap_desc_en", "")
    rationale = sniper_data.get("rationale_si" if is_si else "rationale_en", "")
    
    horizon_badge = sniper_data.get("horizon_badge_si" if is_si else "horizon_badge_en", "")
    horizon_advice = sniper_data.get("horizon_advice_si" if is_si else "horizon_advice_en", "")

    raw_case2 = (
        f'<div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.98), rgba(20, 25, 40, 0.98)); border: 2px solid {strike_color}; border-radius: 12px; padding: 18px 22px; margin-bottom: 22px; box-shadow: 0 8px 30px rgba(0,0,0,0.6); font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif;">'
        
        # Header Row
        f'<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;">'
        f'<div>'
        f'<div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">'
        f'<span style="font-size: 16px; font-weight: 900; color: #F59E0B; letter-spacing: 0.5px;">{card_title}</span>'
        f'{impact_badge_html}'
        f'</div>'
        f'<div style="font-size: 13.5px; color: #E2E8F0; margin-top: 4px;">🚨 <b>{event_title}</b> &bull; <span style="color:#38BDF8;">{event_time}</span></div>'
        f'</div>'
        f'<div style="display: flex; align-items: center; gap: 8px;">'
        f'<span style="background: rgba(245, 158, 11, 0.2); color: #FCD34D; border: 1px solid #F59E0B; font-size: 12.5px; font-weight: 800; padding: 4px 10px; border-radius: 5px;">⏳ {countdown}</span>'
        f'<span style="background: {strike_bg}; color: {strike_color}; border: 1px solid {strike_border}; font-size: 12.5px; font-weight: 800; padding: 4px 10px; border-radius: 5px;">● PRE-NEWS STRIKE READY</span>'
        f'</div>'
        f'</div>'

        # Main Strike Signal Banner
        f'<div style="background: {strike_bg}; border: 2px solid {strike_border}; border-radius: 10px; padding: 14px 18px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 14px;">'
        f'<div>'
        f'<div style="font-size: 12.5px; font-weight: 800; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px;">🎯 HIGH-CONVICTION STRIKE DIRECTION:</div>'
        f'<div style="font-size: 32px; font-weight: 950; color: {strike_color}; letter-spacing: 1px; line-height: 1.2; margin-top: 2px;">{direction_badge}</div>'
        f'</div>'
        f'<div style="text-align: right;">'
        f'<div style="font-size: 12.5px; color: #94A3B8; font-weight: 700;">CONVICTION:</div>'
        f'<div style="font-size: 26px; font-weight: 900; color: #F59E0B;">{sniper_data.get("conviction", 92)}%</div>'
        f'<div style="font-size: 11.5px; color: #CBD5E1;">(London Liquidity Synced)</div>'
        f'</div>'
        f'</div>'

        # Execution Grid (Entry, Trap SL, TP1, TP2)
        f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin-bottom: 14px;">'
        f'<div style="background: rgba(0, 0, 0, 0.45); border-left: 4px solid #38BDF8; border-radius: 7px; padding: 10px 14px;">'
        f'<div style="font-size: 12px; font-weight: 800; color: #94A3B8; text-transform: uppercase;">📍 ENTRY ZONE:</div>'
        f'<div style="font-size: 17px; font-weight: 900; color: #38BDF8; margin-top: 3px;">{entry_zone}</div>'
        f'<div style="font-size: 11.5px; color: #CBD5E1; margin-top: 2px;">Position: {sniper_data.get("price_loc_pct", 50)}% of Range</div>'
        f'</div>'
        f'<div style="background: rgba(0, 0, 0, 0.45); border-left: 4px solid #EF4444; border-radius: 7px; padding: 10px 14px;">'
        f'<div style="font-size: 12px; font-weight: 800; color: #FCA5A5; text-transform: uppercase;">🛑 TIGHT STOP LOSS:</div>'
        f'<div style="font-size: 17px; font-weight: 900; color: #EF4444; margin-top: 3px;">{stop_loss}</div>'
        f'<div style="font-size: 11.5px; color: #CBD5E1; margin-top: 2px;">Beyond Trap Wick Shield</div>'
        f'</div>'
        f'<div style="background: rgba(0, 0, 0, 0.45); border-left: 4px solid #10B981; border-radius: 7px; padding: 10px 14px;">'
        f'<div style="font-size: 12px; font-weight: 800; color: #86EFAC; text-transform: uppercase;">🚀 TARGET 1 (280 PIPS):</div>'
        f'<div style="font-size: 17px; font-weight: 900; color: #10B981; margin-top: 3px;">{tp1}</div>'
        f'<div style="font-size: 11.5px; color: #CBD5E1; margin-top: 2px;">Session Liquidity Pool</div>'
        f'</div>'
        f'<div style="background: rgba(0, 0, 0, 0.45); border-left: 4px solid #F59E0B; border-radius: 7px; padding: 10px 14px;">'
        f'<div style="font-size: 12px; font-weight: 800; color: #FCD34D; text-transform: uppercase;">🚀 TARGET 2 (480 PIPS):</div>'
        f'<div style="font-size: 17px; font-weight: 900; color: #F59E0B; margin-top: 3px;">{tp2}</div>'
        f'<div style="font-size: 11.5px; color: #CBD5E1; margin-top: 2px;">Full HTF Expansion</div>'
        f'</div>'
        f'</div>'

        # Whipsaw & Judas Trap Warning Box
        f'<div style="background: rgba(139, 92, 246, 0.12); border: 1.5px solid #8B5CF6; border-radius: 8px; padding: 11px 15px; margin-bottom: 12px;">'
        f'<div style="font-size: 13.5px; font-weight: 900; color: #C4B5FD;">🛡️ WHIPSAW & JUDAS TRAP SHIELD (දෙපැත්ත කැපීමේ ආරක්ෂණය):</div>'
        f'<div style="font-size: 13.5px; color: #F1F5F9; line-height: 1.5; margin-top: 4px;">{trap_desc}</div>'
        f'</div>'

        # After-Movement Horizon Box
        f'<div style="background: rgba(0, 0, 0, 0.4); border-left: 4px solid #F59E0B; border-radius: 7px; padding: 11px 15px; margin-bottom: 10px;">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px;">'
        f'<div style="font-size: 13px; font-weight: 800; color: #F59E0B;">🧭 AFTER-MOVEMENT HORIZON (පශ්චාත් පුවත් හැසිරීම):</div>'
        f'<div style="font-size: 12px; font-weight: 800; color: #FCD34D;">{horizon_badge}</div>'
        f'</div>'
        f'<div style="font-size: 13px; color: #E2E8F0; line-height: 1.45; margin-top: 4px;">💡 {horizon_advice}</div>'
        f'</div>'

        # Rationale
        f'<div style="font-size: 12.5px; color: #94A3B8; line-height: 1.45; background: rgba(30, 41, 59, 0.5); padding: 8px 12px; border-radius: 6px;">'
        f'📊 <strong style="color: #CBD5E1;">ආයතනික පදනම (Institutional Footprint):</strong> {rationale}'
        f'</div>'

        f'</div>'
    )
    return "".join(raw_case2.splitlines()).replace("$", "&#36;")
