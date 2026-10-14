"""
Geopolitical, Macro & Breaking Wire Intelligence Engine
Parses real-time fast financial wires (ForexLive, FXStreet, Google News),
quantifies the Safe-Haven Index, categorizes Fed/Macro shockwires,
and determines the real-time Gold Market State (Flash Impact vs Normal Regime).
"""

import time
import hashlib
import urllib.parse
import feedparser

_GEO_CACHE = {
    "last_fetch": 0,
    "data": None
}

WAR_BULLISH_KEYWORDS = [
    "war", "missile", "strike", "drone", "attack", "escalat", "retaliat",
    "military", "invasi", "troops", "conflict", "bomb", "explosion",
    "sanction", "red sea", "middle east", "iran", "israel", "gaza",
    "lebanon", "russia", "ukraine", "taiwan", "china", "nuclear", "strait of hormuz"
]

FED_DOVISH_KEYWORDS = [
    "rate cut", "dovish", "cut rates", "50 bps", "lower rates", "easing",
    "yields fall", "yields drop", "yields plunge", "dollar weakens", "dollar falls",
    "dxy drops", "dollar slides", "cooling inflation", "weak jobs", "unemployment rises",
    "safe-haven", "safe haven", "gold rallies", "gold surges", "record high", "gold jumps"
]

BEARISH_KEYWORDS = [
    "hawkish", "cautious on cut", "cautious on rate", "delay cut", "fewer cut",
    "slower cut", "higher for longer", "rate hike", "waller", "powell hawkish",
    "fed warns", "patience on cut", "sticky inflation", "hot cpi", "strong jobs",
    "strong payrolls", "yields rise", "yields jump", "yields surge", "yields spike",
    "dollar rallies", "dollar surges", "dxy surges", "dxy jumps", "treasury yields rise",
    "ceasefire", "peace talk", "truce", "de-escalat", "treaty", "diplomat",
    "hostage deal", "hostage release", "agreement", "withdraw",
    "gold falls", "gold drops", "gold tumbles", "gold plunges", "gold selloff", "gold slides"
]

EXCLUDE_KEYWORDS = [
    "medal", "olympic", "championship", "tournament", "football", "soccer",
    "cricket", "basketball", "movie", "film", "actor", "actress", "concert",
    "fashion", "festival"
]

def fetch_geopolitical_intel(ttl_seconds: int = 45) -> dict:
    """
    Parses real-time breaking wires and calculates both the Safe-Haven Score
    and the real-time Gold Market State (Flash Alert vs Normal Regime).
    """
    now = time.time()
    if _GEO_CACHE["data"] and (now - _GEO_CACHE["last_fetch"] < ttl_seconds):
        return _GEO_CACHE["data"]

    headlines = []
    
    q_geo = 'Gold XAUUSD OR "Middle East" OR "Iran" OR "Israel" OR "Lebanon" OR "Russia" OR "war" OR "missile" when:1d'
    q_fed = 'Gold XAUUSD OR "Federal Reserve" OR "Fed" OR "Powell" OR "Waller" OR "Treasury yield" OR "US10Y" when:1d'
    
    sources = [
        ("FXStreet Fast Wire", "https://www.fxstreet.com/rss/news"),
        ("ForexLive", "https://www.forexlive.com/feed/news"),
        ("Google Macro Wire", f"https://news.google.com/rss/search?q={urllib.parse.quote(q_fed)}&hl=en-US&gl=US&ceid=US:en"),
        ("Google Conflict Wire", f"https://news.google.com/rss/search?q={urllib.parse.quote(q_geo)}&hl=en-US&gl=US&ceid=US:en")
    ]

    war_mentions = 0
    dovish_mentions = 0
    bearish_mentions = 0

    for source_name, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:12]:
                title = entry.get("title", "").strip()
                published = entry.get("published", "") or entry.get("updated", "")
                link = entry.get("link", "#")

                if not title:
                    continue

                lower_title = title.lower()
                
                # Exclude sports or entertainment false positives
                if any(ex in lower_title for ex in EXCLUDE_KEYWORDS):
                    continue
                
                # Check impact on Gold
                is_war = any(k in lower_title for k in WAR_BULLISH_KEYWORDS)
                is_dovish = any(k in lower_title for k in FED_DOVISH_KEYWORDS)
                is_bearish = any(k in lower_title for k in BEARISH_KEYWORDS)

                bias = "NEUTRAL"
                impact_type = "GENERAL"
                if is_war:
                    bias = "BULLISH_GOLD"
                    impact_type = "GEOPOLITICAL_RISK"
                    war_mentions += 1
                elif is_dovish:
                    bias = "BULLISH_GOLD"
                    impact_type = "MACRO_DOVISH"
                    dovish_count = 1
                elif is_bearish:
                    bias = "BEARISH_GOLD"
                    impact_type = "MACRO_HAWKISH"
                    bearish_mentions += 1

                pub_parsed = entry.get("published_parsed")
                pub_epoch = time.mktime(pub_parsed) if pub_parsed else 0

                headlines.append({
                    "title": title,
                    "source": source_name,
                    "published": published[:22] if published else "Recent",
                    "pub_epoch": pub_epoch,
                    "link": link,
                    "bias": bias,
                    "impact_type": impact_type,
                    "is_hot": (bias != "NEUTRAL")
                })
        except Exception:
            continue

    # Deduplicate headlines by title
    seen = set()
    unique_headlines = []
    for h in headlines:
        core = h["title"][:50].lower()
        if core not in seen:
            seen.add(core)
            unique_headlines.append(h)

    # Sort hot headlines first, and within hot headlines, sort by ABSOLUTE NEWEST published time!
    unique_headlines.sort(key=lambda x: (x["is_hot"], x.get("pub_epoch", 0)), reverse=True)

    # Calculate Geopolitical Tension Score (0 - 100)
    calculated_score = 25 + (war_mentions * 6) - (bearish_mentions * 4)
    safe_haven_score = max(min(calculated_score, 95), 10)

    if safe_haven_score >= 65:
        risk_level = "EXTREME_WAR_RISK"
        impulse = "STRONG_SAFE_HAVEN_BUY"
    elif safe_haven_score >= 40:
        risk_level = "ELEVATED_TENSION"
        impulse = "MODERATE_SAFE_HAVEN_BUY"
    else:
        risk_level = "CALM"
        impulse = "NEUTRAL_TO_FADE"

    # Evaluate Real-Time Gold Market State
    hot_items = [h for h in unique_headlines if h["is_hot"]]
    
    if hot_items:
        top_hot = hot_items[0]
        alert_id = hashlib.md5(top_hot["title"].encode("utf-8")).hexdigest()[:10]
        
        if top_hot["bias"] == "BEARISH_GOLD":
            market_state = {
                "state": "FLASH_IMPACT",
                "regime_badge": "🔴 FLASH DUMP ALERT",
                "headline": top_hot["title"],
                "source": top_hot["source"],
                "published": top_hot["published"],
                "impact_dir": "BEARISH_DUMP",
                "audio_type": "BEARISH_WARNING",
                "badge_color": "#EF4444",
                "alert_id": alert_id,
                "impact_desc_en": "CRITICAL DUMP ALERT: Hawkish Fed or Yield Surge wire detected. Immediate institutional liquidation pressure on Gold. AVOID LONGS until yields settle.",
                "impact_desc_si": "අවධානය: හදිසි SELL/DUMP පීඩනයක්! Fed ප්‍රකාශ හෝ බැඳුම්කර ප්‍රතිලාභ ඉහළ යාමක් හේතුවෙන් Gold පහත වැටෙමින් පවතී. LONGS (BUY) ගැනීමෙන් වළකින්න!",
                "action_en": "Action: Favor Scalp Short pullbacks or stay in cash.",
                "action_si": "ක්‍රියාමාර්ගය: Short (Sell) අවස්ථා සොයන්න හෝ වෙළඳපොළ ස්ථාවර වනතුරු ඉවසන්න."
            }
        else:
            market_state = {
                "state": "FLASH_IMPACT",
                "regime_badge": "🟢 FLASH PUMP ALERT",
                "headline": top_hot["title"],
                "source": top_hot["source"],
                "published": top_hot["published"],
                "impact_dir": "BULLISH_SURGE",
                "audio_type": "BULLISH_CHIME",
                "badge_color": "#10B981",
                "alert_id": alert_id,
                "impact_desc_en": "BULLISH BREAKOUT ALERT: Geopolitical Safe-Haven or Dovish Yield Collapse detected. Rapid institutional buying into physical Gold.",
                "impact_desc_si": "අවධානය: හදිසි BUY/SURGE අවස්ථාවක්! යුද අවදානම හෝ බැඳුම්කර ප්‍රතිලාභ කඩා වැටීම හේතුවෙන් Gold වේගයෙන් ඉහළ යමින් පවතී.",
                "action_en": "Action: Favor Longs on M1/M5 dips with tight invalidation.",
                "action_si": "ක්‍රියාමාර්ගය: M1/M5 Retracement වලදී Long (Buy) අවස්ථා සොයන්න."
            }
    else:
        market_state = {
            "state": "NORMAL_REGIME",
            "regime_badge": "🟢 NORMAL REGIME",
            "headline": "Baseline Market Structure (Technical Flow & Macro Yield Drift)",
            "source": "OCTEWYA Intelligence",
            "published": "Active",
            "impact_dir": "NEUTRAL",
            "audio_type": "NONE",
            "badge_color": "#3B82F6",
            "alert_id": "NORMAL",
            "impact_desc_en": "NORMAL MARKET REGIME: No emergency geopolitical or Fed shockwires active. Gold is following baseline technical structure and Treasury yield correlation.",
            "impact_desc_si": "සාමාන්‍ය වෙළඳපොළ තත්ත්වය: හදිසි භූ-දේශපාලනික හෝ Fed ප්‍රවෘත්ති නොමැත. Gold සාමාන්‍ය Technical පරාසය සහ බැඳුම්කර ප්‍රතිලාභ මත පදනම්ව ගමන් කරයි.",
            "action_en": "Action: Standard intraday M1/M15 range scalping around key support/resistance.",
            "action_si": "ක්‍රියාමාර්ගය: ප්‍රධාන Support/Resistance මට්ටම් අතර සාමාන්‍ය Scalping සිදුකරන්න."
        }

    result = {
        "score": safe_haven_score,
        "risk_level": risk_level,
        "impulse": impulse,
        "war_mentions": war_mentions,
        "bearish_mentions": bearish_mentions,
        "headlines": unique_headlines[:25],
        "market_state": market_state,
        "sync_time": time.strftime("%H:%M:%S")
    }

    _GEO_CACHE["last_fetch"] = now
    _GEO_CACHE["data"] = result
    return result
