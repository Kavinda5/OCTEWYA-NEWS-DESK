"""
Forecast Card & Multi-Day Order Flow Renderer
Renders high-visibility dynamic probability radar and two-stage price roadmap for OCTEWYA.
Synced 100% with TradingView & MT5 (XAUUSD Spot / Futures).
"""

def render_forecast_html(forecast_data: dict, lang_choice: str = "si") -> str:
    is_si = (lang_choice == "si")
    
    forecast_title = "🔮 ඉදිරි වෙළඳ සැසි ආයතනික Roadmap (DYNAMIC SESSION & MULTI-DAY FORECAST)" if is_si else "🔮 DYNAMIC SESSION & MULTI-DAY ORDER FLOW FORECAST"
    
    sell_prob = forecast_data.get("sell_prob", 66)
    buy_prob = forecast_data.get("buy_prob", 34)
    primary_dir = forecast_data.get("primary_dir", "SELL")
    
    session_label = forecast_data.get("session_label_si" if is_si else "session_label_en", "NEXT SESSION")
    session_phase_name = forecast_data.get("session_phase_name_si" if is_si else "session_phase_name_en", "Active Session Roadmap")
    curr_session_desc = forecast_data.get("curr_session_desc_si" if is_si else "session_phase_name_en", "Active Push")
    next_session_desc = forecast_data.get("next_session_desc_si" if is_si else "session_phase_name_en", "Reversal Pivot")
    
    bearish_t1 = forecast_data.get("bearish_t1", "$3989.1 - $3993.1")
    bearish_t2 = forecast_data.get("bearish_t2", "$3955.9 - $3962.9")
    bullish_t1 = forecast_data.get("bullish_t1", "$4056.8 - $4063.8")
    bullish_t2 = forecast_data.get("bullish_t2", "$4211.2")
    
    inval_bear = forecast_data.get("invalidation_bearish", "$4025.5")
    inval_bull = forecast_data.get("invalidation_bullish", "$3985.1")
    
    pivot_level = forecast_data.get("pivot_level", "$3989.1 - $3993.1")
    pivot_prob = forecast_data.get("pivot_prob", 70)
    pivot_target = forecast_data.get("pivot_target", "$4030.8 (VPOC) / VWAP")
    pivot_action = forecast_data.get("pivot_action_si" if is_si else "pivot_action_en", "Absorption & Liquidity Sweep")
    pivot_note = forecast_data.get("pivot_note_si" if is_si else "pivot_note_en", "")
    
    reason_text = forecast_data.get("reason_si" if is_si else "reason_en", "")

    # Reversal badge color
    pivot_badge_color = "#38BDF8" if "BULLISH" in forecast_data.get("pivot_type", "") else "#F87171"
    pivot_dir_text = "🟢 BUY REVERSAL PIVOT" if "BULLISH" in forecast_data.get("pivot_type", "") else "🔴 SELL REVERSAL PIVOT"

    return (
        f'<div style="background: rgba(15, 23, 42, 0.95); border: 1.5px solid #334155; border-radius: 12px; padding: 16px 18px; margin-top: 15px; box-shadow: 0 6px 20px rgba(0,0,0,0.45); font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif;">'
        
        # Header Row
        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">'
        f'<div>'
        f'<span style="font-size: 15.5px; font-weight: 800; color: #F59E0B; letter-spacing: 0.5px;">{forecast_title}</span>'
        f'<div style="font-size: 12.5px; color: #94A3B8; margin-top: 2px;">📍 <strong style="color: #E2E8F0;">{session_phase_name}</strong></div>'
        f'</div>'
        f'<div style="display: flex; align-items: center; gap: 8px;">'
        f'<span style="background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid #38BDF8; font-size: 12px; font-weight: 700; padding: 3px 9px; border-radius: 5px;">📈 TradingView / MT5 (XAUUSD) Synced</span>'
        f'<span style="background: #10B98122; color: #10B981; border: 1px solid #10B981; font-size: 12px; font-weight: 800; padding: 3px 9px; border-radius: 5px;">● DYNAMIC LIVE RADAR</span>'
        f'</div>'
        f'</div>'

        # Stage 1: Active Push Probabilities
        f'<div style="margin-bottom: 6px; font-size: 13.5px; font-weight: 800; color: #CBD5E1; text-transform: uppercase; letter-spacing: 0.5px;">'
        f'⚡ STAGE 1: {curr_session_desc}'
        f'</div>'
        f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px;">'
        f'<div style="background: rgba(239, 68, 68, 0.15); border: 1.5px solid #EF4444; border-radius: 9px; padding: 12px; text-align: center;">'
        f'<div style="font-size: 13.5px; font-weight: 800; color: #FCA5A5; text-transform: uppercase;">🔴 {session_label} SELL PROBABILITY</div>'
        f'<div style="font-size: 28px; font-weight: 900; color: #EF4444; line-height: 1.2; margin: 3px 0;">{sell_prob}%</div>'
        f'<div style="font-size: 12.5px; color: #CBD5E1;">(US10Y Yields 4.99% & Sub-VWAP Bear Pressure)</div>'
        f'</div>'
        f'<div style="background: rgba(16, 185, 129, 0.15); border: 1.5px solid #10B981; border-radius: 9px; padding: 12px; text-align: center;">'
        f'<div style="font-size: 13.5px; font-weight: 800; color: #86EFAC; text-transform: uppercase;">🟢 {session_label} BUY PROBABILITY</div>'
        f'<div style="font-size: 28px; font-weight: 900; color: #10B981; line-height: 1.2; margin: 3px 0;">{buy_prob}%</div>'
        f'<div style="font-size: 12.5px; color: #CBD5E1;">(Crude $103 Spike & Geopolitical Safe Haven)</div>'
        f'</div>'
        f'</div>'

        # Active Push Price Targets
        f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px;">'
        f'<div style="background: rgba(0, 0, 0, 0.45); border-left: 4px solid #EF4444; border-radius: 7px; padding: 10px 14px;">'
        f'<div style="font-size: 13.5px; font-weight: 800; color: #EF4444;">🔴 ප්‍රධාන පහළ ඉලක්ක (Bearish Targets):</div>'
        f'<div style="font-size: 14px; color: #F1F5F9; font-weight: 700; margin-top: 5px;">• Target 1: <span style="color:#FCA5A5; font-size:15px;">{bearish_t1}</span> <span style="font-size:12px; color:#94A3B8;">(SSL / News Low)</span></div>'
        f'<div style="font-size: 14px; color: #F1F5F9; font-weight: 700; margin-top: 4px;">• Target 2: <span style="color:#FCA5A5; font-size:15px;">{bearish_t2}</span> <span style="font-size:12px; color:#94A3B8;">(Daily FVG Block)</span></div>'
        f'<div style="font-size: 12.5px; color: #F87171; margin-top: 5px; font-weight: 600;">⚠️ අවලංගු වීම: Reclaim above {inval_bear}</div>'
        f'</div>'
        f'<div style="background: rgba(0, 0, 0, 0.45); border-left: 4px solid #10B981; border-radius: 7px; padding: 10px 14px;">'
        f'<div style="font-size: 13.5px; font-weight: 800; color: #10B981;">🟢 විකල්ප ඉහළ ඉලක්ක (Bullish Targets):</div>'
        f'<div style="font-size: 14px; color: #F1F5F9; font-weight: 700; margin-top: 5px;">• Target 1: <span style="color:#86EFAC; font-size:15px;">{bullish_t1}</span> <span style="font-size:12px; color:#94A3B8;">(VWAP / VAH Block)</span></div>'
        f'<div style="font-size: 14px; color: #F1F5F9; font-weight: 700; margin-top: 4px;">• Target 2: <span style="color:#86EFAC; font-size:15px;">{bullish_t2}</span> <span style="font-size:12px; color:#94A3B8;">(VPOC Magnet)</span></div>'
        f'<div style="font-size: 12.5px; color: #4ADE80; margin-top: 5px; font-weight: 600;">⚠️ අවලංගු වීම: Break below {inval_bull}</div>'
        f'</div>'
        f'</div>'

        # Stage 2: Reversal Pivot Card (What happens next / tomorrow morning)
        f'<div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95)); border: 1.5px solid #38BDF8; border-radius: 9px; padding: 13px 15px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(56, 189, 248, 0.1);">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 6px;">'
        f'<div style="display: flex; align-items: center; gap: 8px;">'
        f'<span style="font-size: 14px; font-weight: 800; color: #38BDF8;">🔄 STAGE 2: {next_session_desc}</span>'
        f'<span style="background: rgba(56, 189, 248, 0.15); color: {pivot_badge_color}; border: 1px solid {pivot_badge_color}; font-size: 11.5px; font-weight: 800; padding: 2px 7px; border-radius: 4px;">{pivot_dir_text}</span>'
        f'</div>'
        f'<div style="font-size: 13px; font-weight: 800; color: #FCD34D;">සම්භාවිතාව (Probability): <span style="color: #38BDF8; font-size: 15px;">{pivot_prob}%</span></div>'
        f'</div>'
        f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px; background: rgba(0, 0, 0, 0.35); padding: 10px; border-radius: 7px; margin-bottom: 8px;">'
        f'<div>'
        f'<div style="font-size: 12px; color: #94A3B8; font-weight: 700; text-transform: uppercase;">🎯 හැරවුම් කලාපය (Reversal Pivot Zone):</div>'
        f'<div style="font-size: 15.5px; font-weight: 800; color: #F59E0B; margin-top: 2px;">{pivot_level}</div>'
        f'</div>'
        f'<div>'
        f'<div style="font-size: 12px; color: #94A3B8; font-weight: 700; text-transform: uppercase;">🚀 ප්‍රතිවිරුද්ධ ඉලක්කය (Reversal Target):</div>'
        f'<div style="font-size: 15.5px; font-weight: 800; color: #A7F3D0; margin-top: 2px;">{pivot_target}</div>'
        f'</div>'
        f'</div>'
        f'<div style="font-size: 13px; color: #E2E8F0; line-height: 1.5; background: rgba(15, 23, 42, 0.6); padding: 8px 10px; border-radius: 6px; border-left: 3px solid #F59E0B;">'
        f'💡 <strong style="color: #FCD34D;">ආයතනික උපදේශය:</strong> {pivot_note}'
        f'</div>'
        f'</div>'

        # Institutional Rationale / Order Flow Confluence
        f'<div style="background: rgba(30, 41, 59, 0.7); border-radius: 7px; padding: 10px 14px;">'
        f'<div style="font-size: 13px; font-weight: 800; color: #F59E0B; margin-bottom: 4px;">📊 ආයතනික හේතු සාධක සහ Order Flow Confluence (5 Pillars):</div>'
        f'<div style="font-size: 13.5px; color: #E2E8F0; line-height: 1.55;">{reason_text}</div>'
        f'</div>'
        
        f'</div>'
    )
