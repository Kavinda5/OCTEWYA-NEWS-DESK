"""
Geopolitical & War Risk Intelligence Engine
Parses real-time wire feeds and quantifies the Safe-Haven Index for XAUUSD.
"""

import time
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

PEACE_BEARISH_KEYWORDS = [
    "ceasefire", "peace talk", "truce", "de-escalat", "treaty", "diplomat",
    "hostage release", "agreement", "withdraw"
]

def fetch_geopolitical_intel(ttl_seconds: int = 60) -> dict:
    """
    Parses real-time breaking wires and calculates the Safe-Haven Score.
    """
    now = time.time()
    if _GEO_CACHE["data"] and (now - _GEO_CACHE["last_fetch"] < ttl_seconds):
        return _GEO_CACHE["data"]

    headlines = []
    
    # 1. Google News Macro & Conflict Wire
    query = 'Gold XAUUSD OR "Middle East" OR "Russia Ukraine" OR "war" OR "missile" OR "ceasefire" when:2d'
    encoded_q = urllib.parse.quote(query)
    gn_url = f"https://news.google.com/rss/search?q={encoded_q}&hl=en-US&gl=US&ceid=US:en"
    
    # 2. FinancialJuice & ForexLive
    sources = [
        ("Google Macro Wire", gn_url),
        ("ForexLive", "https://www.forexlive.com/feed/news"),
        ("FinancialJuice", "https://www.financialjuice.com/feed.ashx")
    ]

    war_mentions = 0
    peace_mentions = 0

    for source_name, url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:15]:
                title = entry.get("title", "").strip()
                published = entry.get("published", "") or entry.get("updated", "")
                link = entry.get("link", "#")

                if not title:
                    continue

                lower_title = title.lower()
                
                # Check sentiment impact on Gold
                is_war = any(k in lower_title for k in WAR_BULLISH_KEYWORDS)
                is_peace = any(k in lower_title for k in PEACE_BEARISH_KEYWORDS)

                bias = "NEUTRAL"
                if is_war:
                    bias = "BULLISH_GOLD"
                    war_mentions += 1
                elif is_peace:
                    bias = "BEARISH_GOLD"
                    peace_mentions += 1

                headlines.append({
                    "title": title,
                    "source": source_name,
                    "published": published[:22] if published else "Recent",
                    "link": link,
                    "bias": bias,
                    "is_hot": is_war or is_peace
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

    # Sort hot headlines first
    unique_headlines.sort(key=lambda x: (x["is_hot"], x["bias"] == "BULLISH_GOLD"), reverse=True)

    # Calculate Geopolitical Tension Score (0 - 100)
    # Baseline normal background tension is 25
    calculated_score = 25 + (war_mentions * 6) - (peace_mentions * 8)
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

    result = {
        "score": safe_haven_score,
        "risk_level": risk_level,
        "impulse": impulse,
        "war_mentions": war_mentions,
        "peace_mentions": peace_mentions,
        "headlines": unique_headlines[:20],
        "sync_time": time.strftime("%H:%M:%S")
    }

    _GEO_CACHE["last_fetch"] = now
    _GEO_CACHE["data"] = result
    return result
