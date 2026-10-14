"""
Internationalization (i18n) Module
Provides seamless toggle between English and Sinhala (සිංහල).
"""

LANGUAGES = {
    "en": "English 🇬🇧",
    "si": "සිංහල 🇱🇰"
}

TRANSLATIONS = {
    # App Header & Branding
    "app_title": {
        "en": "OCTEWYA | XAUUSD Institutional Macro & Yields Intelligence Desk",
        "si": "OCTEWYA | රන් වෙළඳපොළ සාර්ව ආර්ථික සහ බැඳුම්කර බුද්ධි පද්ධතිය"
    },
    "app_subtitle": {
        "en": "Real-time Geopolitical, Treasury Yields (US02Y / US10Y) & Dynamic Precedent Engine",
        "si": "සජීවී භූ-දේශපාලනික, ඇමරිකානු බැඳුම්කර ප්‍රතිලාභ (US02Y / US10Y) සහ අතීත දත්ත සැසඳුම් පද්ධතිය"
    },
    "brand_copyright": {
        "en": "© OCTEWYA all rights reserved",
        "si": "© OCTEWYA all rights reserved"
    },
    "select_language": {
        "en": "Language / භාෂාව",
        "si": "භාෂාව / Language"
    },
    "refresh_data": {
        "en": "🔄 Refresh Live Data",
        "si": "🔄 සජීවී දත්ත යාවත්කාලීන කරන්න"
    },
    "last_updated": {
        "en": "Last sync",
        "si": "අවසන් යාවත්කාලීන කිරීම"
    },

    # Top Tickers
    "gold_price": {
        "en": "XAUUSD Spot / Futures",
        "si": "XAUUSD රන් මිල"
    },
    "us10y_yield": {
        "en": "US 10Y Yield (^TNX)",
        "si": "US 10Y බැඳුම්කර ප්‍රතිලාභය"
    },
    "us02y_yield": {
        "en": "US 02Y Yield (Short-Term)",
        "si": "US 02Y කෙටි කාලීන ප්‍රතිලාභය"
    },
    "yield_spread": {
        "en": "Yield Curve (10Y - 2Y)",
        "si": "බැඳුම්කර පරතරය (10Y - 2Y)"
    },
    "dxy_index": {
        "en": "US Dollar Index (DXY)",
        "si": "US ඩොලර් දර්ශකය (DXY)"
    },
    "buyers_sellers": {
        "en": "Buyers vs Sellers",
        "si": "ගැණුම්කරුවන් සහ විකුණුම්කරුවන්"
    },

    # Master Direction & Regimes
    "master_signal_title": {
        "en": "👑 MASTER STRATEGIC BIAS: GOLD (XAUUSD) INTRADAY",
        "si": "👑 ප්‍රධාන වෙළඳපොළ නැඹුරුව: GOLD (XAUUSD) INTRADAY"
    },
    "bias_strong_buy": {
        "en": "🟢 GOLD (XAUUSD): STRONG BUY (High Conviction)",
        "si": "🟢 GOLD (රත්රන්): දැඩි BUY නැඹුරුවක් (Strong Buy)"
    },
    "bias_buy": {
        "en": "🟢 GOLD (XAUUSD): MODERATE BUY (Accumulation)",
        "si": "🟢 GOLD (රත්රන්): සාමාන්‍ය BUY නැඹුරුවක් (Moderate Buy)"
    },
    "bias_neutral": {
        "en": "🟡 GOLD (XAUUSD): NEUTRAL / RANGE (Consolidation)",
        "si": "🟡 GOLD (රත්රන්): මධ්‍යස්ථ / RANGE (දෝලනය වන තත්ත්වයක්)"
    },
    "bias_sell": {
        "en": "🔴 GOLD (XAUUSD): MODERATE SELL (Distribution)",
        "si": "🔴 GOLD (රත්රන්): සාමාන්‍ය SELL නැඹුරුවක් (Moderate Sell)"
    },
    "bias_strong_sell": {
        "en": "🔴 GOLD (XAUUSD): STRONG SELL (Yield Headwind)",
        "si": "🔴 GOLD (රත්රන්): දැඩි SELL පීඩනයක් (Strong Sell)"
    },
    "confidence_level": {
        "en": "Macro Conviction Score",
        "si": "සාර්ව ආර්ථික විශ්වාසනීයත්ව ලකුණු"
    },
    "gold_state_title": {
        "en": "⚡ Gold Market Real-Time State & Live Wires",
        "si": "⚡ රන් වෙළඳපොළ සජීවී තත්ත්වය සහ ක්ෂණික පුවත්"
    },
    "audio_alerts": {
        "en": "🔊 Audio Notification Alerts",
        "si": "🔊 ශබ්ද මඟින් දැනුම්දීම් (Audio Alerts)"
    },

    # Market Regime & Duration
    "regime_title": {
        "en": "⏱️ Move Duration & Volatility Regime",
        "si": "⏱️ චලනයේ කාලසීමාව සහ වෙළඳපොළ තත්ත්වය"
    },
    "regime_compression": {
        "en": "Compression / Sideways Range",
        "si": "තදින් සිරවුණු පරාසයක දෝලනය වීම (Consolidation)"
    },
    "regime_expansion": {
        "en": "High Volatility Expansion (Breakout)",
        "si": "ඉහළ වේගයකින් සිදුවන Breakout චලනයක්"
    },
    "regime_orderly": {
        "en": "Orderly Trend Continuation",
        "si": "ක්‍රමානුකූල Trend ගමනක්"
    },
    "expected_duration": {
        "en": "Estimated Horizon / Duration",
        "si": "අපේක්ෂිත කාලසීමාව"
    },
    "breakout_risk": {
        "en": "Imminent Breakout Alert",
        "si": "ඉදිරි Breakout සම්භාවිතාව"
    },

    # Yields vs Dollar Analysis
    "yield_analysis_title": {
        "en": "📊 The Institutional Yield Driver (Why Yields Dominate DXY)",
        "si": "📊 ආයතනික බැඳුම්කර බලපෑම (DXY වලට වඩා Yields බලපාන්නේ ඇයි)"
    },
    "yield_insight": {
        "en": "Gold pays 0% yield. When US02Y and US10Y rise, money leaves Gold for Treasury yields. When yields collapse or real rates turn negative, Gold explodes higher.",
        "si": "රත්‍රන් සඳහා පොලී නොලැබේ. US02Y සහ US10Y ඉහළ යන විට ආයෝජකයින් Gold විකුණා බැඳුම්කර වෙත යයි. Yields පහත වැටෙන විට Gold ඉහළට පිපිරී යයි."
    },
    "yield_pressure_status": {
        "en": "Yield Pressure on Gold",
        "si": "බැඳුම්කර වලින් Gold වෙත ඇති පීඩනය"
    },

    # Geopolitical & War Risk
    "geo_title": {
        "en": "🛡️ Geopolitical & War Risk Barometer",
        "si": "🛡️ භූ-දේශපාලනික සහ යුද අවදානම් දර්ශකය"
    },
    "geo_safe_haven": {
        "en": "Safe-Haven Impulse",
        "si": "ආරක්ෂිත තෝතැන්න ඉල්ලුම (Safe-Haven)"
    },
    "geo_status_calm": {
        "en": "Low Conflict Tension (Diplomatic Calm)",
        "si": "අඩු යුද අවදානමක් (සන්සුන් තත්ත්වයක්)"
    },
    "geo_status_elevated": {
        "en": "Elevated Tensions (Escalation Watch)",
        "si": "මධ්‍යම මට්ටමේ යුද ආතතියක් (අවධානයෙන් සිටින්න)"
    },
    "geo_status_extreme": {
        "en": "🚨 Extreme War Escalation (Flight to Gold)",
        "si": "🚨 දැඩි යුද ගැටුම් උත්සන්න වීමක් (Gold මිලදී ගැනීමේ රැල්ලක්)"
    },
    "breaking_wires": {
        "en": "Live Flash Headlines & Conflict Wires",
        "si": "සජීවී ක්ෂණික ප්‍රවෘත්ති සහ ගැටුම් තොරතුරු"
    },

    # Historical Precedent
    "history_title": {
        "en": "🏛️ Historical News Reaction Precedent & Causality",
        "si": "🏛️ අතීත News ප්‍රතික්‍රියා සහ සිදුවීමට හේතු වූ කරුණු"
    },
    "history_explanation": {
        "en": "Comparing today's macroeconomic landscape with identical past releases to identify the probable M1/M15 scalp move and the underlying fundamental driver.",
        "si": "පසුගිය වසරවල මෙවැනිම news ආ අවස්ථාවල Gold හැසිරුණු ආකාරය, එසේ වීමට හේතුව සහ අද දවසේ සිදුවිය හැකි චලනය සංසන්දනය කිරීම."
    },
    "why_it_happened": {
        "en": "The Fundamental Driver (Why it happened):",
        "si": "එසේ වීමට මූලික හේතුව (Why it happened):"
    },
    "expected_pip_move": {
        "en": "Historical 15m Pip Range",
        "si": "අතීත විනාඩි 15 තුළ සාමාන්‍ය Pip වෙනස"
    },

    # Dynamic Evolving Calendar
    "calendar_drawer_title": {
        "en": "📅 Dynamic Evolving Economic Calendar",
        "si": "📅 සජීවීව වෙනස්වන ආර්ථික දින දර්ශනය (Dynamic Calendar)"
    },
    "calendar_intro": {
        "en": "Forecasts dynamically evolve in real-time as intermediate Yields, Inflation precursors, and Geopolitical shifts reshape market expectations before release day.",
        "si": "නිකුත් වීමට නියමිත දිනයට පෙර අතරමැදි කාලයේදී Yields, උද්ධමන පෙරනිමිති සහ යුද තත්ත්වයන් වෙනස් වන විට, එක් එක් news එකට ඇති බලාපොරොත්තුව (Bias) සජීවීව Update වේ."
    },
    "event_name": {
        "en": "Event",
        "si": "සිදුවීම"
    },
    "event_time": {
        "en": "Date / Time",
        "si": "දිනය / වේලාව"
    },
    "event_impact": {
        "en": "Impact",
        "si": "බලපෑම"
    },
    "evolving_bias": {
        "en": "Dynamic Market Expectation for Gold",
        "si": "වර්තමාන තත්ත්වය අනුව Gold වලට ඇති බලාපොරොත්තුව"
    },
    "forecast_vs_prev": {
        "en": "Forecast vs Previous",
        "si": "පුරෝකථනය සහ පෙර අගය"
    },

    # Non-News Periods Analysis
    "non_news_title": {
        "en": "🧭 Non-News Market Condition & Structural Sentiment",
        "si": "🧭 News නොමැති වෙලාවල වෙළඳපොළ තත්ත්වය"
    },
    "non_news_desc": {
        "en": "When no major economic data is releasing, Gold is governed by Central Bank physical accumulation, real interest rate drift, and safe-haven background flows.",
        "si": "ප්‍රධාන ආර්ථික දත්ත නිකුත් නොවන සාමාන්‍ය වෙලාවලදී Gold පාලනය වන්නේ ලෝක මහ බැංකු වල රන් මිලදී ගැනීම්, සැබෑ පොලී අනුපාතික සහ පසුබිම් යුද අවදානම මඟිනි."
    },

    # AI Macro Analyst
    "ai_analyst_title": {
        "en": "🧠 OCTEWYA Macro AI Strategic Assessment",
        "si": "🧠 OCTEWYA මැක්‍රෝ AI උපායමාර්ගික විශ්ලේෂණය"
    },
    "generate_ai_analysis": {
        "en": "Generate Deep-Dive AI Assessment",
        "si": "පූර්ණ AI විශ්ලේෂණය ලබාගන්න"
    },
    "scalp_playbook": {
        "en": "M1 - M15 Scalper Playbook",
        "si": "M1 - M15 Scalper උපදෙස් මාලාව"
    },
    "invalidation_levels": {
        "en": "Key Reversal / Invalidation Zones",
        "si": "චලනය වෙනස්විය හැකි තීරණාත්මක සීමාවන්"
    }
}

def t(key: str, lang: str = "en") -> str:
    """Retrieve translated text by key and language code."""
    item = TRANSLATIONS.get(key)
    if not item:
        return key
    return item.get(lang, item.get("en", key))
