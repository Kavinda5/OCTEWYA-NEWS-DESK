"""
AI Analyst & Strategic Synthesis Engine
Produces comprehensive institutional analysis in Sinhala and English,
supporting both Gemini API (google-genai) and a built-in deterministic quantitative model.
"""

import os
from google import genai
from google.genai import types

def generate_macro_assessment(
    macro_data: dict,
    geo_data: dict,
    precedent_data: dict,
    lang: str = "si"
) -> dict:
    """
    Synthesizes all real-time factors into an actionable M1/M15 intraday game plan.
    """
    gold_price = macro_data.get("gold_price", 2735.0)
    gold_atr = macro_data.get("gold_atr", 14.0)
    us10y = macro_data.get("us10y_yield", 4.22)
    us02y = macro_data.get("us02y_yield", 4.11)
    yield_spread = macro_data.get("yield_spread", 0.11)
    yield_pressure = macro_data.get("yield_pressure", "NEUTRAL")
    buyers_pct = macro_data.get("buyers_pct", 55)
    sellers_pct = macro_data.get("sellers_pct", 45)
    regime = macro_data.get("regime", "COMPRESSION")
    est_duration = macro_data.get("estimated_duration", "1 - 2 Hours")
    safe_score = geo_data.get("score", 30)

    # Calculate overall strategic score (-100 to +100)
    # Yield pressure has high negative correlation with gold
    yield_score = -35 if yield_pressure == "BEARISH_ON_GOLD" else (35 if yield_pressure == "BULLISH_ON_GOLD" else 0)
    
    # Safe haven score is positive for gold
    geo_score = int((safe_score - 30) * 0.8) # positive when war tension > 30

    # Order flow positioning
    buyer_score = int((buyers_pct - 50) * 0.9)

    total_score = yield_score + geo_score + buyer_score

    # Determine master bias
    if total_score >= 35:
        master_bias = "STRONG_BUY"
        bias_label_en = "GOLD (XAUUSD): STRONG BUY 🟢 (Safe-Haven & Yield Support)"
        bias_label_si = "GOLD (රත්රන්): දැඩි BUY නැඹුරුවක් 🟢 (Safe-Haven සහ Yield වාසිදායකයි)"
    elif total_score >= 12:
        master_bias = "BUY"
        bias_label_en = "GOLD (XAUUSD): MODERATE BUY 🟢 (Accumulation Bias)"
        bias_label_si = "GOLD (රත්රන්): සාමාන්‍ය BUY නැඹුරුවක් 🟢 (ගැණුම්කරුවන්ගේ එකතුවීමක්)"
    elif total_score <= -35:
        master_bias = "STRONG_SELL"
        bias_label_en = "GOLD (XAUUSD): STRONG SELL 🔴 (Treasury Yield Headwind)"
        bias_label_si = "GOLD (රත්රන්): දැඩි SELL පීඩනයක් 🔴 (බැඳුම්කර ප්‍රතිලාභ ඉහළ යාම)"
    elif total_score <= -12:
        master_bias = "SELL"
        bias_label_en = "GOLD (XAUUSD): MODERATE SELL 🔴 (Distribution / Fade)"
        bias_label_si = "GOLD (රත්රන්): සාමාන්‍ය SELL නැඹුරුවක් 🔴 (විකුණුම් පීඩනයක්)"
    else:
        master_bias = "NEUTRAL"
        bias_label_en = "GOLD (XAUUSD): NEUTRAL / RANGE 🟡 (Balanced Drivers)"
        bias_label_si = "GOLD (රත්රන්): මධ්‍යස්ථ / RANGE 🟡 (දෝලනය වන තත්ත්වයක්)"

    conviction = min(max(abs(total_score) + 40, 50), 96)

    # Key Invalidation Levels for M1/M15 scalpers
    invalidation_up = round(gold_price + (gold_atr * 1.2), 2)
    invalidation_down = round(gold_price - (gold_atr * 1.2), 2)

    # Try Gemini API if API key exists
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    ai_narrative = ""

    if gemini_key:
        try:
            client = genai.Client(api_key=gemini_key)
            prompt = f"""
You are an institutional macro strategist specializing in XAUUSD (Gold) scalping/intraday trading.
Analyze the following real-time conditions:
- Gold Price: {gold_price:.2f} (ATR: {gold_atr:.2f})
- US 10Y Yield: {us10y:.3f}%, US 02Y Yield: {us02y:.3f}% (Yield Spread: {yield_spread:.3f}%)
- Yield Pressure on Gold: {yield_pressure}
- Order Flow: {buyers_pct}% Buyers vs {sellers_pct}% Sellers
- Geopolitical Safe-Haven Score: {safe_score}/100
- Market Regime: {regime} (Estimated Duration: {est_duration})
- Master Calculated Bias: {master_bias}

Language requested: {"Sinhala (සිංහල)" if lang == "si" else "English"}
Provide a sharp, 3-point trading summary:
1. Primary Driver & Direction (Why yields and safe-haven dictate the direction)
2. Scalp Duration Profile (Will this be a 15-minute spike or sustained multi-hour trend? How long will range consolidation last?)
3. Invalidation Zone & Risk Guideline (Key levels around {invalidation_down} and {invalidation_up}).
Keep it practical, professional, without generic disclaimers.
"""
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            if response and response.text:
                ai_narrative = response.text
        except Exception:
            ai_narrative = ""

    # High-quality deterministic fallback narrative
    if not ai_narrative:
        if lang == "si":
            ai_narrative = f"""
### 📊 ආයතනික සාර්ව ආර්ථික විශ්ලේෂණය (OCTEWYA Strategy):

1. **ප්‍රධාන වෙළඳපොළ ධාවකය (Yields & Safe-Haven):**
   * වත්මන් **US10Y ({us10y:.2f}%)** සහ **US02Y ({us02y:.2f}%)** බැඳුම්කර ප්‍රතිලාභ මට්ටම Gold සඳහා **{yield_pressure}** තත්ත්වයක පවතී.
   * භූ-දේශපාලනික යුද අවදානම් දර්ශකය **{safe_score}/100** මට්ටමක ඇති බැවින්, ආරක්ෂිත තෝතැන්න (Safe-Haven) ඉල්ලුම වෙළඳපොළේ Buy පීඩනයට සහය දක්වයි.
   * වෙළඳපොළේ ගැණුම්කරුවන් **{buyers_pct}%** සහ විකුණුම්කරුවන් **{sellers_pct}%** ලෙස සටහන් වන අතර, සමස්ත නැඹුරුව **{bias_label_si}** වේ.

2. **චලනයේ කාලසීමාව සහ Regime එක (Duration & Consolidation):**
   * වෙළඳපොළ මේ වන විට **{regime}** තත්ත්වයක පවතින අතර, මෙම පරාසය තව **{est_duration}** පමණ පැවතිය හැක.
   * Breakout එකක් සිදුවුවහොත්, එය **M1/M5/M15** timeframe තුළ වේගවත් **±120 සිට ±220 pips** දක්වා වූ චලනයක් වීමට වැඩි ඉඩක් ඇත.

3. **තීරණාත්මක Invalidation සහ Risk මට්ටම්:**
   * ඉහළ Breakout සීමාව: **${invalidation_up}** (මෙහිදී Buy Momentum තවදුරටත් තහවුරු වේ).
   * පහළ Breakout සීමාව: **${invalidation_down}** (මෙම සීමාව කැඩී ගියහොත් Sell පීඩනය වේගවත් වේ).
"""
        else:
            ai_narrative = f"""
### 📊 Institutional Macro Playbook (OCTEWYA Strategy):

1. **Primary Macro Drivers (Yields & Geopolitical Safe-Haven):**
   * Benchmark **US10Y ({us10y:.2f}%)** and **US02Y ({us02y:.2f}%)** are currently producing a **{yield_pressure}** effect on non-yielding bullion.
   * The Geopolitical War Tension Index is registering at **{safe_score}/100**, sustaining background safe-haven bids.
   * Order flow proxy displays **{buyers_pct}% Buyers vs {sellers_pct}% Sellers**, anchoring an overall **{bias_label_en}**.

2. **Market Regime & Horizon Duration:**
   * Gold is currently operating in a **{regime}** state with an estimated timeframe horizon of **{est_duration}**.
   * Any pending volatility breakout carries an anticipated target trajectory of **±120 to ±220 pips**.

3. **Key Invalidation & Scalp Risk Zones:**
   * Bullish Acceleration Ceiling: **${invalidation_up}**
   * Bearish Liquidation Floor: **${invalidation_down}**
"""

    return {
        "master_bias": master_bias,
        "bias_label": bias_label_si if lang == "si" else bias_label_en,
        "conviction": conviction,
        "total_score": total_score,
        "invalidation_up": invalidation_up,
        "invalidation_down": invalidation_down,
        "narrative": ai_narrative
    }
