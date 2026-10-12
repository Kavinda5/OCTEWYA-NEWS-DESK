"""
Dynamic Evolving Economic Calendar Module
Fetches official ForexFactory economic calendar data and dynamically calculates
the evolving market expectation (Buy vs Sell for Gold) based on live yield & geopolitical conditions.
"""

import time
import requests
from datetime import datetime

_CAL_CACHE = {
    "last_fetch": 0,
    "data": None
}

def fetch_dynamic_calendar(current_macro: dict, ttl_seconds: int = 120) -> list:
    """
    Fetches real-time calendar and calculates dynamic bias for each event.
    """
    now = time.time()
    if _CAL_CACHE["data"] and (now - _CAL_CACHE["last_fetch"] < ttl_seconds):
        return _CAL_CACHE["data"]

    events = []
    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
    headers = {"User-Agent": "OCTEWYA-MacroDesk/1.0"}

    try:
        resp = requests.get(url, headers=headers, timeout=6)
        if resp.status_code == 200:
            raw_data = resp.json()
            # Filter for USD high and medium impact events
            usd_events = [e for e in raw_data if e.get("country") == "USD" and e.get("impact") in ["High", "Medium"]]
            
            for item in usd_events[:15]:
                title = item.get("title", "US Economic Event")
                impact = item.get("impact", "Medium").upper()
                date_str = item.get("date", "")
                forecast = item.get("forecast", "-") or "-"
                previous = item.get("previous", "-") or "-"

                # Parse date nicely
                try:
                    dt = datetime.fromisoformat(date_str)
                    formatted_date = dt.strftime("%a %b %d | %H:%M")
                except Exception:
                    formatted_date = date_str

                # Calculate Dynamic Evolving Bias based on intermediate macro conditions
                yield_pressure = current_macro.get("yield_pressure", "NEUTRAL")
                safe_haven_score = current_macro.get("safe_haven_score", 30)
                us02y_change = current_macro.get("us02y_change", 0.0)

                lower_title = title.lower()
                
                # Dynamic Logic
                if "cpi" in lower_title or "ppi" in lower_title:
                    if us02y_change > 0.02 and safe_haven_score < 60:
                        bias = "SELL_ON_GOLD"
                        badge_color = "red"
                        reason_en = "Current rising 2Y yields suggest sticky inflation expectations. Market currently pricing upside surprise risk (Bearish Gold)."
                        reason_si = "වත්මන් 2Y බැඳුම්කර ප්‍රතිලාභ ඉහළ යාම නිසා උද්ධමනය වැඩිවීමේ අවදානමක් වෙළඳපොළ බලාපොරොත්තු වේ (Gold සඳහා Sell නැඹුරුවක්)."
                    elif safe_haven_score >= 60:
                        bias = "BUY_ON_GOLD"
                        badge_color = "green"
                        reason_en = "Safe-haven war hedge demand currently outweighs yield drag, keeping gold dip-buyers active ahead of release."
                        reason_si = "යුද අවදානම් ආරක්ෂණ ඉල්ලුම ඉහළ මට්ටමක පවතින බැවින්, news එකට පෙර පවා Gold සඳහා Buy ඉල්ලුමක් පවතී."
                    else:
                        bias = "NEUTRAL"
                        badge_color = "yellow"
                        reason_en = "Balanced yield curve. Wait for release deviation."
                        reason_si = "බැඳුම්කර පීඩනය සමතුලිතයි. News එක නිකුත් වන තෙක් ස්ථාවරයි."

                elif "claims" in lower_title or "payroll" in lower_title or "unemployment" in lower_title:
                    if current_macro.get("buyers_pct", 50) > 55 or safe_haven_score > 50:
                        bias = "BUY_ON_GOLD"
                        badge_color = "green"
                        reason_en = "Labor cooling narrative and steady buyer accumulation support upside momentum."
                        reason_si = "රැකියා වෙළඳපොළ ලිහිල් වීමේ ප්‍රවණතාව සහ ගැණුම්කරුවන්ගේ එකතුවීම නිසා Gold Buy නැඹුරුවක් පවතී."
                    else:
                        bias = "SELL_ON_GOLD"
                        badge_color = "red"
                        reason_en = "Firm labor market expectations supporting Dollar."
                        reason_si = "රැකියා දත්ත ශක්තිමත් වනු ඇතැයි බලාපොරොත්තු වන නිසා ඩොලරයට වාසිදායක වේ."

                elif "fomc" in lower_title or "rate" in lower_title or "powell" in lower_title:
                    if yield_pressure == "BEARISH_ON_GOLD":
                        bias = "SELL_ON_GOLD"
                        badge_color = "red"
                        reason_en = "Hawkish Fed rhetoric repricing yields higher."
                        reason_si = "Fed නිලධාරීන්ගේ දැඩි ප්‍රතිපත්ති නිසා බැඳුම්කර ඉහළ ගොස් Gold මත පීඩනයක් ඇත."
                    else:
                        bias = "BUY_ON_GOLD"
                        badge_color = "green"
                        reason_en = "Dovish easing sentiment lifting non-yielding bullion."
                        reason_si = "පොලී කප්පාදු අපේක්ෂාවන් Gold ඉහළට තල්ලු කරයි."

                else:
                    bias = "NEUTRAL"
                    badge_color = "gray"
                    reason_en = "Standard intraday volatility expected."
                    reason_si = "සාමාන්‍ය intraday volatility අපේක්ෂා කෙරේ."

                events.append({
                    "title": title,
                    "impact": impact,
                    "date": formatted_date,
                    "forecast": forecast,
                    "previous": previous,
                    "evolving_bias": bias,
                    "badge_color": badge_color,
                    "reason_en": reason_en,
                    "reason_si": reason_si
                })
    except Exception:
        pass

    # Fallback if network issue
    if not events:
        events = [
            {
                "title": "US Core CPI m/m",
                "impact": "HIGH",
                "date": "Wednesday | 18:00 (SL Time)",
                "forecast": "0.3%",
                "previous": "0.3%",
                "evolving_bias": "SELL_ON_GOLD",
                "badge_color": "red",
                "reason_en": "Elevated 2Y yields suggest sticky service inflation risk.",
                "reason_si": "2Y බැඳුම්කර ප්‍රතිලාභ ඉහළ මට්ටමක ඇති බැවින් උද්ධමනය වැඩිවීමේ අවදානමක් ඇත."
            },
            {
                "title": "US Initial Jobless Claims",
                "impact": "MEDIUM",
                "date": "Thursday | 18:00 (SL Time)",
                "forecast": "221K",
                "previous": "219K",
                "evolving_bias": "BUY_ON_GOLD",
                "badge_color": "green",
                "reason_en": "Softer employment trends favor safe-haven gold bids.",
                "reason_si": "රැකියා ඉල්ලුම්පත් වැඩිවීම Gold සඳහා වාසිදායක වේ."
            }
        ]

    _CAL_CACHE["last_fetch"] = now
    _CAL_CACHE["data"] = events
    return events
