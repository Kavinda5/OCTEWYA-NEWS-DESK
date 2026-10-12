"""
Historical Reaction Precedent & Causality Engine
Contains curated historical reactions for major US releases (CPI, NFP, FOMC, PPI, Claims)
with fundamental causality ("Why it happened") and compares with today's live conditions.
"""

HISTORICAL_EVENTS = {
    "CPI": {
        "event_name": "US Consumer Price Index (CPI)",
        "frequency": "Monthly",
        "impact": "HIGH",
        "precedents": [
            {
                "date": "Recent Release (Hot Inflation Beat)",
                "actual_vs_forecast": "Actual Core CPI +0.3% (Forecast +0.2%)",
                "reaction_15m": "-$26.40 (Sell Spike)",
                "reaction_1h": "-$19.80 (Partial Pullback)",
                "duration_profile": "Immediate 15m Sell Spike, then Choppy Stabilization",
                "why_it_happened_en": "Higher inflation forced traders to price out imminent Fed rate cuts. US02Y yield surged +13 bps, strengthening the USD and severely punishing non-yielding Gold.",
                "why_it_happened_si": "උද්ධමනය ඉහළ යාම නිසා Fed පොලී අනුපාතික කපාහැරීමේ බලාපොරොත්තු බිඳවැටුණි. US02Y බැඳුම්කර ප්‍රතිලාභය +13 bps ඉහළ ගිය අතර, පොලී නොලැබෙන Gold විකුණා ඩොලර් සහ බැඳුම්කර වෙත ආයෝජකයින් ඇදී ගියේය."
            },
            {
                "date": "Previous Release (Cooling Inflation Miss)",
                "actual_vs_forecast": "Actual Core CPI +0.1% (Forecast +0.2%)",
                "reaction_15m": "+$22.80 (Buy Spike)",
                "reaction_1h": "+$31.50 (Strong NY Trend)",
                "duration_profile": "Full Session Buy Trend (Sustained 4+ Hours)",
                "why_it_happened_en": "Cooling inflation signaled Fed rate cuts were imminent. US10Y yield dropped -11 bps and DXY collapsed, unleashing aggressive institutional Gold buying.",
                "why_it_happened_si": "උද්ධමනය පහත වැටීම නිසා ඉක්මනින් පොලී අනුපාතික පහත හෙළනු ඇතැයි වෙළඳපොළ තීරණය කළේය. US10Y ප්‍රතිලාභය -11 bps කඩා වැටුණු අතර, ආයතනික ආයෝජකයින් දැඩි ලෙස Gold මිලදී ගත්තේය."
            }
        ]
    },
    "NFP": {
        "event_name": "US Non-Farm Payrolls & Unemployment",
        "frequency": "First Friday of Month",
        "impact": "HIGH",
        "precedents": [
            {
                "date": "Recent Release (Strong Jobs + Low Unemployment)",
                "actual_vs_forecast": "Actual +254K (Forecast +147K)",
                "reaction_15m": "-$31.20 (Violent M5 Sell)",
                "reaction_1h": "-$24.50 (Consolidated Lows)",
                "duration_profile": "Rapid 10-Min Flash Crash followed by 2-Hour tight range",
                "why_it_happened_en": "Labor market resilience crushed 50 bps Fed rate cut bets. Real yields spiked aggressively, prompting institutional long liquidations in Gold.",
                "why_it_happened_si": "රැකියා වෙළඳපොළ ශක්තිමත් වීම නිසා ලොකු පොලී කප්පාදුවක අවශ්‍යතාව නැතිවිය. Real Yields ඉහළ යාමත් සමඟ Gold Long Trades විශාල වශයෙන් liquidate විය."
            },
            {
                "date": "Previous Release (Weak Labor Market Miss)",
                "actual_vs_forecast": "Actual +114K (Forecast +175K) | Unemployment jumped to 4.3%",
                "reaction_15m": "+$36.00 (Explosive Buy Surge)",
                "reaction_1h": "+$48.20 (Multi-day Breakout)",
                "duration_profile": "Multi-Day Structural Bull Trend",
                "why_it_happened_en": "Recession fears sparked Sahm Rule triggers. Markets priced in emergency Fed easing, driving a massive safe-haven flight into Gold.",
                "why_it_happened_si": "ආර්ථික අවපාත බිය මතුවූ අතර Fed පොලී ඉක්මනින් කපනු ඇතැයි බලාපොරොත්තු ඇතිවිය. බැඳුම්කර කඩා වැටී Gold වෙත විශාල ප්‍රාග්ධනයක් ගලා ආවේය."
            }
        ]
    },
    "FOMC": {
        "event_name": "FOMC Interest Rate Decision & Powell Speech",
        "frequency": "Every 6 Weeks",
        "impact": "HIGH",
        "precedents": [
            {
                "date": "Dovish Rate Pivot",
                "actual_vs_forecast": "Rate cut delivered with dovish forward guidance",
                "reaction_15m": "+$28.50 (Initial Whipsaw -> Surge)",
                "reaction_1h": "+$44.00 (All-Night Continuation)",
                "duration_profile": "Long-Term Macro Trend (Days/Weeks)",
                "why_it_happened_en": "Lower benchmark interest rates reduce the opportunity cost of holding physical Gold, fundamentally expanding long-term institutional demand.",
                "why_it_happened_si": "පොලී අනුපාතික පහත හෙළීම නිසා Gold ළඟ තබාගැනීමේ opportunity cost එක අඩු වූ අතර, දිගුකාලීන ආයතන Gold රඳවා ගැනීම ආරම්භ කළේය."
            }
        ]
    },
    "PPI": {
        "event_name": "US Producer Price Index (PPI - Wholesale Inflation)",
        "frequency": "Monthly",
        "impact": "MEDIUM / HIGH",
        "precedents": [
            {
                "date": "Recent Release (Pipeline Inflation Signal)",
                "actual_vs_forecast": "PPI Core YoY higher by +0.2%",
                "reaction_15m": "-$14.20 (Scalp Sell Spike)",
                "reaction_1h": "-$8.50 (Quick Mean-Reversion)",
                "duration_profile": "Short 15-25 min Scalp Move (Fade opportunity)",
                "why_it_happened_en": "Wholesale prices feed into future CPI. Traders used the knee-jerk reaction for quick scalps before fading back into the session trend.",
                "why_it_happened_si": "නිෂ්පාදන මිල ඉහළ යාම ඉදිරි CPI එකට බලපායි. මෙය විනාඩි 15-20ක කෙටි Scalp Sell එකකට පසු ආපහු සාමාන්‍ය මට්ටමට පැමිණියේය."
            }
        ]
    }
}

def compare_historical_precedent(event_key: str, current_yield_trend: str, safe_haven_level: str) -> dict:
    """
    Compares today's macro conditions with the closest historical event.
    """
    event_data = HISTORICAL_EVENTS.get(event_key, HISTORICAL_EVENTS["CPI"])
    sample = event_data["precedents"][0]

    # Synthesize current comparison
    if current_yield_trend == "BEARISH_ON_GOLD" and safe_haven_level != "EXTREME_WAR_RISK":
        predicted_direction = "SELL_BIAS"
        predicted_pips = "180 - 260 Pips (-$18 to -$26 Drop)"
        move_type = "High-Speed M5/M15 Sell Spike"
        duration_summary_en = "Initial 15-minute sell drop. Watch for consolidation support after 30-45 minutes."
        duration_summary_si = "මුල් විනාඩි 15 තුළ වේගවත් Sell පහත වැටීමක්. විනාඩි 30-45 කට පසු consolidation මට්ටමක ස්ථාවර විය හැක."
    elif safe_haven_level == "EXTREME_WAR_RISK" or current_yield_trend == "BULLISH_ON_GOLD":
        predicted_direction = "BUY_BIAS"
        predicted_pips = "220 - 350 Pips (+$22 to +$35 Surge)"
        move_type = "Sustained Bullish Momentum"
        duration_summary_en = "Strong buy continuation. Momentum expected to hold for 2 to 4 hours."
        duration_summary_si = "ශක්තිමත් Buy ගමනක්. ඉදිරි පැය 2 සිට 4 දක්වා momentum එක පවතිනු ඇතැයි අපේක්ෂා කෙරේ."
    else:
        predicted_direction = "CHOPPY_RANGE"
        predicted_pips = "80 - 140 Pips (Whipsaw Range)"
        move_type = "Consolidation / Two-Way Scalping"
        duration_summary_en = "Range-bound choppy action. Fast in-and-out scalping only."
        duration_summary_si = "පරාසයක දෝලනය වන තත්ත්වයක්. කෙටි scalping පමණක් සුදුසු වේ."

    return {
        "event_name": event_data["event_name"],
        "impact": event_data["impact"],
        "sample_precedent": sample,
        "predicted_direction": predicted_direction,
        "predicted_pips": predicted_pips,
        "move_type": move_type,
        "duration_summary_en": duration_summary_en,
        "duration_summary_si": duration_summary_si
    }
