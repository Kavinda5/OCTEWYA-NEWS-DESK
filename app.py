"""
OCTEWYA | XAUUSD Institutional Macro & Yields Intelligence Desk
Real-time Geopolitical, Treasury Yields (US02Y / US10Y) & Dynamic Precedent Engine.
© OCTEWYA all rights reserved.
"""

import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from datetime import datetime, timezone, timedelta

# Local Modules
from modules.i18n import t, LANGUAGES
try:
    from modules.market_data import fetch_live_macro_data, calculate_multi_day_orderflow_forecast
except ImportError:
    from modules.market_data import fetch_live_macro_data
    def calculate_multi_day_orderflow_forecast(m, g=None):
        return {}
from modules.geopolitics_engine import fetch_geopolitical_intel
try:
    from modules.forecast_card import render_forecast_html
except ImportError:
    def render_forecast_html(f, l="si"):
        return ""
from modules.history_engine import HISTORICAL_EVENTS, compare_historical_precedent
try:
    from modules.calendar_engine import fetch_dynamic_calendar, get_upcoming_macro_watch
except ImportError:
    from modules.calendar_engine import fetch_dynamic_calendar
    def get_upcoming_macro_watch(events, macro_data):
        return {
            "status": "UPCOMING",
            "title": "US High-Impact Economic Event",
            "impact": "HIGH",
            "time_str": "Session Watch (SL Time)",
            "countdown_str": "Active",
            "evolving_bias": "BUY_ON_GOLD",
            "impact_label_en": "🟢 GOLD IMPACT: BUY BIAS 🟢",
            "impact_label_si": "🟢 GOLD වෙත බලපෑම: BUY BIAS 🟢",
            "badge_color": "#10B981",
            "reason_en": "Awaiting fresh catalyst.",
            "reason_si": "දත්ත නිකුත් වනතුරු රැඳී සිටින්න.",
            "forecast": "-",
            "previous": "-",
            "is_imminent": False
        }
try:
    from modules.ai_analyst import generate_macro_assessment, generate_pre_news_scenario_matrix
except ImportError:
    from modules.ai_analyst import generate_macro_assessment
    def generate_pre_news_scenario_matrix(macro_watch, current_macro, lang="si"):
        return {
            "matrix_text": "Awaiting module sync.",
            "dump_target_1": 0,
            "pump_target_1": 0,
            "whipsaw_trap_low": 0,
            "whipsaw_pump_target": 0
        }

# Universal Timezone Definition directly in app.py
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

def trigger_audio_alert(sound_type: str):
    """Triggers synthetic Web Audio notification in the browser."""
    if not sound_type or sound_type == "NONE":
        return
    js_code = f"""
    <script>
    (function() {{
        try {{
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (!AudioCtx) return;
            const audioCtx = new AudioCtx();
            if (audioCtx.state === 'suspended') {{ audioCtx.resume(); }}
            const now = audioCtx.currentTime;
            
            if ("{sound_type}" === "BULLISH") {{
                // Institutional Chime (D5 -> A5 ascending)
                const osc1 = audioCtx.createOscillator();
                const gain1 = audioCtx.createGain();
                osc1.type = 'sine';
                osc1.frequency.setValueAtTime(587.33, now);
                gain1.gain.setValueAtTime(0.35, now);
                gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
                osc1.connect(gain1);
                gain1.connect(audioCtx.destination);
                osc1.start(now);
                osc1.stop(now + 0.5);

                const osc2 = audioCtx.createOscillator();
                const gain2 = audioCtx.createGain();
                osc2.type = 'sine';
                osc2.frequency.setValueAtTime(880, now + 0.12);
                gain2.gain.setValueAtTime(0.4, now + 0.12);
                gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.85);
                osc2.connect(gain2);
                gain2.connect(audioCtx.destination);
                osc2.start(now + 0.12);
                osc2.stop(now + 0.85);
            }} else if ("{sound_type}" === "BEARISH") {{
                // Institutional Warning Tone (440Hz -> 311Hz double pulse)
                const osc1 = audioCtx.createOscillator();
                const gain1 = audioCtx.createGain();
                osc1.type = 'triangle';
                osc1.frequency.setValueAtTime(440, now);
                gain1.gain.setValueAtTime(0.4, now);
                gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
                osc1.connect(gain1);
                gain1.connect(audioCtx.destination);
                osc1.start(now);
                osc1.stop(now + 0.22);

                const osc2 = audioCtx.createOscillator();
                const gain2 = audioCtx.createGain();
                osc2.type = 'triangle';
                osc2.frequency.setValueAtTime(311.13, now + 0.25);
                gain2.gain.setValueAtTime(0.45, now + 0.25);
                gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.6);
                osc2.connect(gain2);
                gain2.connect(audioCtx.destination);
                osc2.start(now + 0.25);
                osc2.stop(now + 0.6);
            }}
        }} catch (e) {{
            console.error("Audio error:", e);
        }}
    }})();
    </script>
    """
    components.html(js_code, height=0, width=0)

# 1. Page Configuration
st.set_page_config(
    page_title="OCTEWYA | XAUUSD Macro & Yields Desk",
    page_icon="🟡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom Institutional Dark-Themed CSS
st.markdown("""
<style>
    /* Global Styling */
    .stApp {
        background-color: #0B0E14;
        color: #E6EDF3;
    }
    
    /* Global Typography Enhancement for Supreme Readability */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 15px;
    }
    
    /* Top Header Bar */
    .brand-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 22px;
        background: linear-gradient(90deg, #161B26 0%, #1A2234 100%);
        border: 1px solid #283347;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .brand-title {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 1px;
        color: #F59E0B;
        margin: 0;
    }
    .brand-subtitle {
        font-size: 14.5px;
        color: #94A3B8;
        margin-top: 4px;
        font-weight: 500;
    }
    .brand-badge {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid #F59E0B;
        color: #F59E0B;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12.5px;
        font-weight: 700;
    }

    /* Metric Cards */
    .ticker-card {
        background: #161B26;
        border: 1px solid #232D3F;
        border-radius: 10px;
        padding: 14px 16px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .ticker-label {
        font-size: 13.5px;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .ticker-value {
        font-size: 24px;
        font-weight: 800;
        color: #F8FAFC;
    }
    .ticker-delta-green {
        color: #10B981;
        font-size: 13.5px;
        font-weight: 700;
    }
    .ticker-delta-red {
        color: #EF4444;
        font-size: 13.5px;
        font-weight: 700;
    }

    /* Signal Cards */
    .signal-box {
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 15px;
        border: 1px solid #2E384D;
    }
    .buy-signal {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.05) 100%);
        border: 1px solid #10B981;
    }
    .sell-signal {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.05) 100%);
        border: 1px solid #EF4444;
    }
    .neutral-signal {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.05) 100%);
        border: 1px solid #F59E0B;
    }

    /* News Badge */
    .news-badge {
        font-size: 12.5px;
        padding: 3px 9px;
        border-radius: 5px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-bullish { background: rgba(16, 185, 129, 0.2); color: #10B981; border: 1px solid #10B981; }
    .badge-bearish { background: rgba(239, 68, 68, 0.2); color: #EF4444; border: 1px solid #EF4444; }
    .badge-neutral { background: rgba(148, 163, 184, 0.2); color: #94A3B8; border: 1px solid #64748B; }

    /* Footer Branding */
    .footer-bar {
        text-align: center;
        padding: 16px;
        color: #94A3B8;
        font-size: 13.5px;
        border-top: 1px solid #1E293B;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# 2.1 Authentication Gate
AUTH_USER = os.environ.get("ADMIN_USERNAME", "octewya")
AUTH_PASS = os.environ.get("ADMIN_PASSWORD", "Oct921027")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    _, col2, _ = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-top: 50px; margin-bottom: 25px;">
            <h1 style="color: #F59E0B; font-weight: 800; font-size: 34px; margin: 0; letter-spacing: 1px;">OCTEWYA</h1>
            <div style="color: #94A3B8; font-size: 14px; margin-top: 4px;">Institutional Macro Intelligence Desk</div>
            <div style="font-size: 13.5px; color: #64748B; margin-top: 4px;">© OCTEWYA all rights reserved</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("### 🔒 Portal Login")
            u_input = st.text_input("Username / පරිශීලක නම", placeholder="Enter username")
            p_input = st.text_input("Password / මුරපදය", type="password", placeholder="Enter password")
            submit_btn = st.form_submit_button("Sign In / ඇතුල් වන්න", use_container_width=True)
            
            if submit_btn:
                if u_input.strip() == AUTH_USER and p_input.strip() == AUTH_PASS:
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("❌ Invalid Username or Password / පරිශීලක නම හෝ මුරපදය වැරදියි")
        
        st.markdown("<div style='text-align:center; font-size: 13.5px; color:#64748B; margin-top:20px;'>Protected Institutional Environment &bull; Unauthorized Access Prohibited</div>", unsafe_allow_html=True)
    st.stop()

# 3. Sidebar Configuration (Language, Timezone, Auto-Refresh)
with st.sidebar:
    st.markdown("### 🌐 Settings / සැකසුම්")
    lang_choice = st.selectbox(
        "Interface Language / භාෂාව තෝරන්න",
        options=list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x],
        index=0
    )

    tz_choice = st.selectbox(
        "🕒 Timezone / වේලා කලාපය",
        options=list(TIMEZONES.keys()),
        format_func=lambda x: TIMEZONES[x][0],
        index=0
    )

    auto_refresh_sec = st.selectbox(
        "⚡ Auto Refresh / ස්වයංක්‍රීය යාවත්කාලීන",
        options=[2, 5, 10, 15, 30, 60, 120, 0],
        format_func=lambda s: "Off (Manual)" if s == 0 else ("⚡ Sniper Turbo (2s)" if s == 2 else f"Every {s} seconds"),
        index=4 # Default Every 30 seconds
    )
    
    st.markdown("---")
    
    # Refresh Trigger
    if st.button(t("refresh_data", lang_choice), use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    curr_time_display = get_current_time_str(tz_choice)
    st.markdown(f"**OCTEWYA Intelligence Engine**  \n`Status: Real-Time Stream Active`  \n`Live Time: {curr_time_display}`")

    st.markdown("---")
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if gemini_key:
        st.success("🟢 Gemini Macro AI: Connected & Active")
    else:
        with st.expander("🔑 Gemini AI Key (Optional)", expanded=False):
            api_key_input = st.text_input("API Key", type="password")
            if api_key_input:
                os.environ["GEMINI_API_KEY"] = api_key_input

    # Audio Alerts Control
    st.markdown("---")
    st.markdown("### 🔊 Audio Alerts / ශබ්ද දැනුම්දීම්")
    audio_on = st.toggle("Enable Sound Alerts", value=st.session_state.get("audio_enabled", True), key="audio_enabled_toggle")
    st.session_state["audio_enabled"] = audio_on
    
    col_a1, col_a2 = st.columns(2)
    if col_a1.button("🔔 Test Buy", use_container_width=True):
        st.session_state["play_sound"] = "BULLISH"
    if col_a2.button("⚠️ Test Sell", use_container_width=True):
        st.session_state["play_sound"] = "BEARISH"

    # Logout Button
    st.markdown("---")
    if st.button("🚪 Logout / ඉවත් වන්න", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

    # Elegant subtle branding in sidebar
    st.markdown(f"""
    <div style='margin-top: 30px; font-size: 13.5px; color: #64748B; text-align: center;'>
        <b>OCTEWYA Institutional Suite</b><br>
        {t("brand_copyright", lang_choice)}
    </div>
    """, unsafe_allow_html=True)

# 4. Main Dashboard Engine with Dynamic Auto-Refresh & Timezone
@st.fragment(run_every=f"{auto_refresh_sec}s" if auto_refresh_sec > 0 else None)
def render_main_dashboard(lang_choice: str, tz_choice: str):
    macro_data = fetch_live_macro_data()
    geo_data = fetch_geopolitical_intel()
    calendar_events = fetch_dynamic_calendar(macro_data)
    macro_watch = get_upcoming_macro_watch(calendar_events, macro_data)
    precedent_data = compare_historical_precedent("CPI", macro_data["yield_pressure"], geo_data["risk_level"])
    ai_assessment = generate_macro_assessment(macro_data, geo_data, precedent_data, lang_choice)
    forecast_data = calculate_multi_day_orderflow_forecast(macro_data, geo_data)

    # Audio Alert Processing
    sound_to_trigger = st.session_state.pop("play_sound", None)
    m_state = geo_data.get("market_state", {})
    if st.session_state.get("audio_enabled", True) and m_state.get("state") == "FLASH_IMPACT":
        current_alert_id = m_state.get("alert_id", "")
        if current_alert_id and current_alert_id != st.session_state.get("last_alert_id"):
            st.session_state["last_alert_id"] = current_alert_id
            if m_state.get("impact_dir") == "BEARISH_DUMP":
                sound_to_trigger = "BEARISH"
            elif m_state.get("impact_dir") == "BULLISH_SURGE":
                sound_to_trigger = "BULLISH"

    # Imminent Macro Event Audio Warning (5 minutes before major release)
    if st.session_state.get("audio_enabled", True) and macro_watch.get("is_imminent"):
        event_key = macro_watch.get("title", "") + "_imminent"
        if event_key != st.session_state.get("last_imminent_key"):
            st.session_state["last_imminent_key"] = event_key
            sound_to_trigger = "BEARISH" # Warning chime

    if sound_to_trigger:
        trigger_audio_alert(sound_to_trigger)

    # 5. Top Header Branding Bar
    live_tz_time = get_current_time_str(tz_choice)
    tz_label = TIMEZONES.get(tz_choice, ("UTC",))[0]
    st.markdown(f"""
    <div class="brand-header">
        <div>
            <h1 class="brand-title">OCTEWYA</h1>
            <div class="brand-subtitle">{t("app_title", lang_choice)}</div>
        </div>
        <div style="text-align: right;">
            <span class="brand-badge">XAUUSD INTRADAY</span>
            <div style="font-size: 13.5px; color: #94A3B8; margin-top: 5px;">
                {t("last_updated", lang_choice)}: <span style="color:#10B981; font-weight:700;">{live_tz_time}</span> 
                <span style="font-size: 12.5px; color:#64748B;">({tz_label})</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # News Sniper High-Frequency Banner
    is_sniper_active = macro_watch.get("is_imminent", False) or (macro_watch.get("status") == "POST_RELEASE" and macro_watch.get("mins_ago", 1) <= 3)
    if is_sniper_active:
        sniper_lbl = "⚡ NEWS SNIPER WINDOW ACTIVE: HIGH-VOLATILITY CLUSTER ARMED" if lang_choice == "en" else "⚡ NEWS SNIPER සක්‍රීයයි: ඉහළ චලනයක් සහිත පුවත් කවුළුව"
        sniper_sub = f"Dominant Anchor: {macro_watch.get('dominant_event', 'Key Event')} (Weight: {macro_watch.get('dominant_weight', 5)}/10) • Anti-Fakeout Protection Active"
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #7F1D1D 0%, #B91C1C 100%); border: 1px solid #EF4444; color: #FFFFFF; padding: 10px 16px; border-radius: 8px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 0 15px rgba(239, 68, 68, 0.4);">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 18px;">⚡</span>
                <div>
                    <div style="font-size: 13px; font-weight: 800; letter-spacing: 0.5px;">{sniper_lbl}</div>
                    <div style="font-size: 13.5px; color: #FECACA;">{sniper_sub}</div>
                </div>
            </div>
            <span style="background: rgba(0,0,0,0.4); border: 1px solid #FECACA; padding: 3px 10px; border-radius: 20px; font-size: 13.5px; font-weight: 800; color: #FEE2E2;">REAL-TIME SNIPER</span>
        </div>
        """, unsafe_allow_html=True)

    # 6. Top Ticker Row (Gold, US10Y, US02Y, Spread, DXY, Buyers vs Sellers)
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        g_delta_class = "ticker-delta-green" if macro_data["gold_change"] >= 0 else "ticker-delta-red"
        g_sign = "+" if macro_data["gold_change"] >= 0 else ""
        st.markdown(f"""
        <div class="ticker-card">
            <div class="ticker-label">{t("gold_price", lang_choice)}</div>
            <div class="ticker-value">${macro_data['gold_price']:.2f}</div>
            <div class="{g_delta_class}">{g_sign}{macro_data['gold_change']:.2f} ({g_sign}{macro_data['gold_change_pct']:.2f}%)</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        y10_delta_class = "ticker-delta-green" if macro_data["us10y_change"] >= 0 else "ticker-delta-red"
        y10_sign = "+" if macro_data["us10y_change"] >= 0 else ""
        st.markdown(f"""
        <div class="ticker-card">
            <div class="ticker-label">{t("us10y_yield", lang_choice)}</div>
            <div class="ticker-value">{macro_data['us10y_yield']:.3f}%</div>
            <div class="{y10_delta_class}">{y10_sign}{macro_data['us10y_change']:.3f} pts</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        oil_price = macro_data.get("oil_price", 75.0)
        oil_chg = macro_data.get("oil_change", 0.0)
        oil_pct = macro_data.get("oil_change_pct", 0.0)
        oil_spike = macro_data.get("oil_spike", False)
        oil_delta_class = "ticker-delta-red" if oil_spike else ("ticker-delta-green" if oil_chg >= 0 else "ticker-delta-red")
        oil_sign = "+" if oil_chg >= 0 else ""
        oil_tag = " ⚡ SPIKE" if oil_spike else ""
        oil_label = "CRUDE OIL (USOIL)" if lang_choice == "en" else "බොරතෙල් (USOIL)"
        st.markdown(f"""
        <div class="ticker-card">
            <div class="ticker-label">{oil_label}{oil_tag}</div>
            <div class="ticker-value">${oil_price:.2f}</div>
            <div class="{oil_delta_class}">{oil_sign}${oil_chg:.2f} ({oil_sign}{oil_pct:.2f}%)</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        dxy_delta_class = "ticker-delta-green" if macro_data["dxy_change"] >= 0 else "ticker-delta-red"
        dxy_sign = "+" if macro_data["dxy_change"] >= 0 else ""
        st.markdown(f"""
        <div class="ticker-card">
            <div class="ticker-label">{t("dxy_index", lang_choice)}</div>
            <div class="ticker-value">{macro_data['dxy_price']:.2f}</div>
            <div class="{dxy_delta_class}">{dxy_sign}{macro_data['dxy_change']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="ticker-card">
            <div class="ticker-label">{t("buyers_sellers", lang_choice)}</div>
            <div class="ticker-value" style="color: #10B981;">{macro_data['buyers_pct']}% <span style="font-size:14px; color:#94A3B8;">/</span> <span style="color:#EF4444;">{macro_data['sellers_pct']}%</span></div>
            <div style="font-size: 13.5px; color: #94A3B8;">Buyers vs Sellers</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # 7. Collapsible / Dedicated Dynamic Evolving Calendar Drawer
    with st.expander(f"📑 {t('calendar_drawer_title', lang_choice)} (Click to Expand / බලන්න මෙතන ඔබන්න)", expanded=False):
        st.markdown(f"*{t('calendar_intro', lang_choice)}*")
        
        cal_cols = st.columns([2.5, 1, 1.2, 1.2, 2.5])
        cal_cols[0].markdown(f"**{t('event_name', lang_choice)}**")
        cal_cols[1].markdown(f"**{t('event_impact', lang_choice)}**")
        cal_cols[2].markdown(f"**{t('event_time', lang_choice)}**")
        cal_cols[3].markdown(f"**{t('forecast_vs_prev', lang_choice)}**")
        cal_cols[4].markdown(f"**{t('evolving_bias', lang_choice)}**")
        st.markdown("<hr style='margin:4px 0 10px 0; border-color:#283347;'>", unsafe_allow_html=True)

        for ev in calendar_events:
            ec1, ec2, ec3, ec4, ec5 = st.columns([2.5, 1, 1.2, 1.2, 2.5])
            ec1.write(f"**{ev['title']}**")
            
            # Impact Badge
            if ev['impact'] == "HIGH":
                ec2.markdown("<span style='color:#EF4444; font-weight:700;'>🔴 HIGH</span>", unsafe_allow_html=True)
            else:
                ec2.markdown("<span style='color:#F59E0B; font-weight:700;'>🟡 MED</span>", unsafe_allow_html=True)

            ec3.write(ev['date'])
            ec4.write(f"{ev['forecast']} / {ev['previous']}")

            # Dynamic Evolving Bias Badge
            if ev['evolving_bias'] == "BUY_ON_GOLD":
                bias_badge = "<span class='news-badge badge-bullish'>🟢 BUY BIAS</span>"
            elif ev['evolving_bias'] == "SELL_ON_GOLD":
                bias_badge = "<span class='news-badge badge-bearish'>🔴 SELL BIAS</span>"
            else:
                bias_badge = "<span class='news-badge badge-neutral'>🟡 NEUTRAL</span>"
            
            reason_txt = ev['reason_si'] if lang_choice == "si" else ev['reason_en']
            ec5.markdown(f"{bias_badge} <br><span style='font-size: 13.5px; color:#94A3B8;'>{reason_txt}</span>", unsafe_allow_html=True)
            st.markdown("<hr style='margin:6px 0; border-color:#1E293B;'>", unsafe_allow_html=True)

    st.write("")

    # 7.5. Dedicated Hero Section: Gold Market Real-Time State & Live Flash Wires
    m_state = geo_data.get("market_state")
    if not m_state or not isinstance(m_state, dict):
        m_state = {
            "state": "NORMAL_REGIME",
            "regime_badge": "🟢 NORMAL REGIME",
            "headline": "Baseline Market Structure (Technical Flow & Macro Yield Drift)",
            "source": "OCTEWYA Intelligence",
            "published": "Active",
            "impact_dir": "NEUTRAL",
            "badge_color": "#3B82F6",
            "impact_desc_en": "NORMAL MARKET REGIME: No emergency geopolitical or Fed shockwires active. Gold is following baseline technical structure and Treasury yield correlation.",
            "impact_desc_si": "සාමාන්‍ය වෙළඳපොළ තත්ත්වය: හදිසි භූ-දේශපාලනික හෝ Fed ප්‍රවෘත්ති නොමැත. Gold සාමාන්‍ය Technical පරාසය සහ බැඳුම්කර ප්‍රතිලාභ මත පදනම්ව ගමන් කරයි.",
            "action_en": "Standard intraday M1/M15 range scalping around key support/resistance.",
            "action_si": "ප්‍රධාන Support/Resistance මට්ටම් අතර සාමාන්‍ය Scalping සිදුකරන්න."
        }

    state_color = m_state.get("badge_color", "#3B82F6")
    state_badge = m_state.get("regime_badge", "🟢 NORMAL REGIME")
    headline = m_state.get("headline", "Baseline Market Structure")
    
    state_title = t('gold_state_title', lang_choice)
    if state_title == 'gold_state_title':
        state_title = "රන් වෙළඳපොළ සජීවී තත්ත්වය සහ ක්ෂණික පුවත්" if lang_choice == "si" else "Gold Market Real-Time State & Live Wires"

    impact_desc = m_state.get("impact_desc_si" if lang_choice == "si" else "impact_desc_en")
    if not impact_desc:
        impact_desc = "සාමාන්‍ය වෙළඳපොළ තත්ත්වය: හදිසි භූ-දේශපාලනික හෝ Fed ප්‍රවෘත්ති නොමැත. Gold සාමාන්‍ය Technical පරාසය මත පදනම්ව ගමන් කරයි." if lang_choice == "si" else "NORMAL MARKET REGIME: No emergency shock wires active. Gold is trading within baseline technical structure."

    action_text = m_state.get("action_si" if lang_choice == "si" else "action_en")
    if not action_text:
        action_text = "ප්‍රධාන Support/Resistance මට්ටම් අතර සාමාන්‍ය Scalping සිදුකරන්න." if lang_choice == "si" else "Standard intraday M1/M15 range scalping around key support/resistance."

    source = m_state.get("source", "OCTEWYA Intelligence")
    pub_time = m_state.get("published", "Live")
    audio_status_text = "🔊 Audio Armed" if st.session_state.get("audio_enabled", True) else "🔇 Audio Muted"

    watch_status = macro_watch.get("status", "UPCOMING")
    watch_title = macro_watch.get("title", "High-Impact USD Release")
    watch_time = macro_watch.get("time_str", "")
    watch_countdown = macro_watch.get("countdown_str", "")
    watch_impact_label = macro_watch.get("impact_label_si" if lang_choice == "si" else "impact_label_en", "GOLD IMPACT")
    watch_badge_color = macro_watch.get("badge_color", "#10B981")
    watch_reason = macro_watch.get("reason_si" if lang_choice == "si" else "reason_en", "")

    # Last Completed Event Scorecard & After-Movement Radar
    scorecard = macro_watch.get("last_event_scorecard")
    scorecard_html = ""
    if scorecard:
        acc_label = scorecard.get("accuracy_label_si" if lang_choice == "si" else "accuracy_label_en", "")
        acc_clr = scorecard.get("accuracy_color", "#10B981")
        mov_state = scorecard.get("movement_state_si" if lang_choice == "si" else "movement_state_en", "")
        mov_desc = scorecard.get("movement_desc_si" if lang_choice == "si" else "movement_desc_en", "")
        mov_clr = scorecard.get("movement_color", "#10B981")
        imb_note = scorecard.get("imbalance_note_si" if lang_choice == "si" else "imbalance_note_en", "")
        imb_badge = scorecard.get("imbalance_badge", "")
        sc_title = "🎯 පසුගිය ප්‍රවෘත්ති ප්‍රතිඵලය සහ ගමන්මග" if lang_choice == "si" else "🎯 LAST EVENT OUTCOME & AFTER-MOVEMENT"

        scorecard_html = (
            f'<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid #283347; border-radius: 8px; padding: 12px 14px; margin-top: 12px;">'
            f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">'
            f'<span style="font-size: 13px; font-weight: 800; color: #94A3B8; text-transform: uppercase;">{sc_title}</span>'
            f'<span style="background: {acc_clr}22; color: {acc_clr}; border: 1px solid {acc_clr}; font-size: 14px; font-weight: 800; padding: 2px 8px; border-radius: 4px;">{acc_label}</span>'
            f'</div>'
            f'<div style="font-size: 14px; color: #E2E8F0; font-weight: 700;">📌 {scorecard.get("title")}</div>'
            f'<div style="font-size: 12.5px; color: #64748B; margin-top: 2px;">🕒 {scorecard.get("released_time")}</div>'
            f'<div style="margin-top: 8px; padding: 8px 10px; background: rgba(0,0,0,0.3); border-radius: 6px; border-left: 3px solid {mov_clr};">'
            f'<div style="font-size: 13px; font-weight: 800; color: {mov_clr};">🧭 {mov_state}</div>'
            f'<div style="font-size: 14px; color: #CBD5E1; margin-top: 3px; line-height: 1.4;">{mov_desc}</div>'
            f'</div>'
            f'<div style="margin-top: 8px; padding: 8px 10px; background: rgba(30, 41, 59, 0.5); border-radius: 6px;">'
            f'<div style="font-size: 14px; font-weight: 800; color: #F59E0B;">{imb_badge}</div>'
            f'<div style="font-size: 14px; color: #CBD5E1; line-height: 1.4; margin-top: 3px;">{imb_note}</div>'
            f'</div>'
            f'</div>'
        )

    watch_header = "🚨 ඉදිරි ප්‍රධාන ආර්ථික සිදුවීම" if lang_choice == "si" else "🚨 UPCOMING HIGH-IMPACT MACRO EVENT"
    if watch_status == "POST_RELEASE":
        watch_header = "⚡ නිකුත් වූ දත්ත හා ක්ෂණික ප්‍රතිචාරය" if lang_choice == "si" else "⚡ POST-RELEASE OUTCOME TRACKER"
    elif watch_status == "IMMINENT":
        watch_header = "🔥 නිකුත් වීමට ආසන්නයි (අවධානය!)" if lang_choice == "si" else "🔥 RELEASE IMMINENT (HIGH VOLATILITY!)"

    # Dynamic Multi-Day Institutional Order Flow & Price Target Forecast
    forecast_html = render_forecast_html(forecast_data, lang_choice)

    hero_html = (
        f'<div style="background: #111827; border: 2px solid {state_color}; border-radius: 12px; padding: 18px 22px; margin-bottom: 22px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);">'
        f'<div style="display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap;">'
        f'<div style="flex: 1.25; min-width: 320px; border-right: 1px solid #1E293B; padding-right: 18px;">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-bottom: 10px;">'
        f'<div style="display: flex; align-items: center; gap: 10px;">'
        f'<span style="background: {state_color}; color: #FFFFFF; font-weight: 900; font-size: 14.5px; padding: 5px 14px; border-radius: 6px; letter-spacing: 0.5px;">{state_badge}</span>'
        f'<span style="font-size: 14.5px; color: #94A3B8; font-weight: 600;">{state_title}</span>'
        f'</div>'
        f'<div style="font-size: 12.5px; color: #64748B;">'
        f'<span style="color:#10B981; font-weight:700;">{audio_status_text}</span> &bull; Source: <span style="color:#CBD5E1;">{source}</span> &bull; {pub_time}'
        f'</div>'
        f'</div>'
        f'<div style="font-size: 17.5px; font-weight: 800; color: #FFFFFF; margin: 8px 0; line-height: 1.45;">{headline}</div>'
        f'<div style="background: rgba(0,0,0,0.3); border-left: 4px solid {state_color}; padding: 12px 16px; border-radius: 6px; margin-top: 10px;">'
        f'<div style="font-size: 14px; color: #E2E8F0; font-weight: 600; line-height: 1.5;">{impact_desc}</div>'
        f'<div style="font-size: 14px; color: #F59E0B; font-weight: 700; margin-top: 6px;">🎯 {action_text}</div>'
        f'</div>'
        f'{forecast_html}'
        f'</div>'
        f'<div style="flex: 0.85; min-width: 280px; display: flex; flex-direction: column; justify-content: space-between;">'
        f'<div>'
        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">'
        f'<span style="color: #94A3B8; font-size: 12.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">{watch_header}</span>'
        f'<span style="background: rgba(245,158,11,0.2); color: #F59E0B; font-weight: 800; font-size: 14px; padding: 3px 9px; border-radius: 4px;">⏳ {watch_countdown}</span>'
        f'</div>'
        f'<div style="font-size: 16.5px; font-weight: 800; color: #FFFFFF; line-height: 1.35;">📌 {watch_title}</div>'
        f'<div style="font-size: 13.5px; color: #38BDF8; font-weight: 700; margin-top: 3px;">🕒 {watch_time}</div>'
        f'</div>'
        f'<div style="background: rgba(0,0,0,0.5); border: 2px solid {watch_badge_color}; border-radius: 8px; padding: 12px; margin: 10px 0; text-align: center; box-shadow: 0 0 16px {watch_badge_color}33;">'
        f'<div style="font-size: 19px; font-weight: 900; color: {watch_badge_color}; letter-spacing: 0.5px; text-transform: uppercase;">{watch_impact_label}</div>'
        f'</div>'
        f'<div style="font-size: 12.5px; color: #CBD5E1; line-height: 1.4;"><b>💡 Insight:</b> {watch_reason}</div>'
        f'{scorecard_html}'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    # Pre-News 3-Scenario Matrix (Clean Sell vs Whipsaw Trap vs Clean Buy)
    scenario_matrix = generate_pre_news_scenario_matrix(macro_watch, macro_data, lang_choice)
    matrix_expander_title = "🎯 AI Pre-News 3-Scenario Playbook (පූර්ව අවස්ථා 3 සහ Whipsaw Trap සැලසුම)" if lang_choice == "si" else "🎯 AI Pre-News 3-Scenario Playbook (Divergence & Whipsaw Traps)"
    with st.expander(matrix_expander_title, expanded=(macro_watch.get("is_whipsaw", False) or macro_watch.get("is_imminent", False))):
        st.markdown(scenario_matrix["matrix_text"])
        st.markdown(f"""
        <div style="background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8B5CF6; padding: 10px 14px; border-radius: 4px; font-size: 14px; color: #E2E8F0; margin-top: 8px;">
            <b>🧠 Institutional Trading Rule:</b> {"පළමු news එකට Market එක තත්පර කිහිපයකින් Pip 50-100ක් පහළට Dump වුවත්, ප්‍රමුඛ දත්තය (Dominant Metric) පරස්පර වුවහොත් (Miss), එම Dump එක Sell Trap එකකි! එහිදී Sell වලට නොපැන, පහළ Trap මට්ටමේදී Massive Buy Reversal එකක් බලාපොරොත්තු වන්න." if lang_choice == "si" else "If secondary data beats but the Dominant Anchor misses, the initial 50-100 pip dump is an institutional liquidity trap. Do NOT chase shorts; prepare for violent 300+ pip buy reversal!"}
        </div>
        """, unsafe_allow_html=True)

    # 8. Main Working Deck (2-Column Grid)
    left_col, right_col = st.columns([1.1, 0.9])

    with left_col:
        # A. Master Strategic Bias & Regime
        bias_style = "buy-signal" if "BUY" in ai_assessment["master_bias"] else ("sell-signal" if "SELL" in ai_assessment["master_bias"] else "neutral-signal")
        master_sig_title = t('master_signal_title', lang_choice)
        if master_sig_title == 'master_signal_title':
            master_sig_title = "👑 ප්‍රධාන වෙළඳපොළ නැඹුරුව: GOLD (XAUUSD) INTRADAY" if lang_choice == "si" else "👑 MASTER STRATEGIC BIAS: GOLD (XAUUSD) INTRADAY"

        st.markdown(f"""<div class="signal-box {bias_style}">
<div style="font-size: 13px; font-weight: 800; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px;">{master_sig_title}</div>
<div style="font-size: 25px; font-weight: 900; margin: 8px 0; color: #FFFFFF; line-height: 1.3;">{ai_assessment['bias_label']}</div>
<div style="font-size: 13px; color: #CBD5E1;"><b>{t('confidence_level', lang_choice)}:</b> {ai_assessment['conviction']}% | <b>Order Flow:</b> {macro_data['buyers_pct']}% Buyers vs {macro_data['sellers_pct']}% Sellers</div>
</div>""", unsafe_allow_html=True)

        # B. Regime & Duration Predictor Card
        st.markdown(f"### {t('regime_title', lang_choice)}")
        rc1, rc2 = st.columns(2)
        with rc1:
            st.markdown(f"""<div class="ticker-card" style="text-align: left;">
<div class="ticker-label">{t('regime_title', lang_choice)}</div>
<div style="font-size: 16px; font-weight: 700; color: #F59E0B;">{t('regime_' + macro_data['regime'].lower(), lang_choice)}</div>
<div style="font-size: 14px; color: #94A3B8; margin-top: 4px;"><b>{t('expected_duration', lang_choice)}:</b> {macro_data['estimated_duration']}</div>
</div>""", unsafe_allow_html=True)

        with rc2:
            st.markdown(f"""<div class="ticker-card" style="text-align: left;">
<div class="ticker-label">{t('breakout_risk', lang_choice)}</div>
<div style="font-size: 16px; font-weight: 700; color: #10B981;">{macro_data['breakout_risk_pct']}% Probability</div>
<div style="font-size: 14px; color: #94A3B8; margin-top: 4px;"><b>ATR (M15 Volatility):</b> ±${macro_data['gold_atr']:.2f} pips</div>
</div>""", unsafe_allow_html=True)

        st.write("")

        # C. Real-Time Gold Action & Shock Radar (Replaces static yields gauge)
        shock = ai_assessment.get("shock_warning", {})
        shock_status = shock.get("status", "CLEAR")
        shock_title = shock.get("title", "🛡️ EVENT HORIZON: STABLE")
        shock_action = shock.get("action", "Market drivers are orderly.")
        shock_color = shock.get("color", "#3B82F6")

        radar_title = "⚡ සජීවී වෙළඳපොළ දිශාව සහ පුවත් අවදානම් රේඩාර්" if lang_choice == "si" else "⚡ Real-Time Gold Action & Shock Radar"
        st.markdown(f"### {radar_title}")

        # 1. Event Shock Reversal Warning Box
        if shock_status != "CLEAR":
            shock_box_html = (
                f'<div style="background: rgba(0,0,0,0.4); border: 2px solid {shock_color}; border-radius: 10px; padding: 14px 18px; margin-bottom: 15px;">'
                f'<div style="color: {shock_color}; font-weight: 900; font-size: 15px;">{shock_title}</div>'
                f'<div style="color: #F8FAFC; font-size: 13px; font-weight: 600; margin-top: 5px;">👉 {shock_action}</div>'
                f'</div>'
            )
        else:
            shock_box_html = (
                f'<div style="background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.3); border-radius: 10px; padding: 12px 16px; margin-bottom: 15px;">'
                f'<div style="color: #10B981; font-weight: 800; font-size: 14px;">{shock_title}</div>'
                f'<div style="color: #94A3B8; font-size: 14px; margin-top: 3px;">{shock_action}</div>'
                f'</div>'
            )
        st.markdown(shock_box_html, unsafe_allow_html=True)

        # 2. 3 Tactical Drivers Cards (Order Flow, Yield Momentum, Oil Spike Watch)
        k1, k2, k3 = st.columns(3)
        with k1:
            vwap_val = macro_data.get("vwap", macro_data["gold_price"])
            vwap_dist = macro_data.get("vwap_dist", 0.0)
            vwap_color = "#10B981" if vwap_dist >= 0 else "#EF4444"
            vwap_badge = "Above VWAP (Bullish)" if vwap_dist >= 0 else "Below VWAP (Bearish)"
            of_event = macro_data.get("orderflow_event", "NORMAL_LIQUIDITY").replace("_", " ")

            st.markdown(
                f'<div class="ticker-card" style="text-align: left; padding: 12px 14px;">'
                f'<div class="ticker-label">🌊 INTRADAY VWAP & LIQUIDITY</div>'
                f'<div style="font-size: 15px; font-weight: 800; color: {vwap_color}; margin-top: 4px;">${vwap_val:.2f}</div>'
                f'<div style="font-size: 13.5px; color: #CBD5E1; margin-top: 2px;"><b>Pos:</b> <span style="color:{vwap_color};">{vwap_badge}</span></div>'
                f'<div style="font-size: 13.5px; color: #94A3B8; margin-top: 2px;"><b>Event:</b> {of_event}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        with k2:
            y10_val = macro_data["us10y_yield"]
            y10_chg = macro_data["us10y_change"]
            y_color = "#10B981" if y10_chg < -0.01 else ("#EF4444" if y10_chg > 0.01 else "#F59E0B")
            y_desc = macro_data.get("yield_momentum_desc", "Neutral Yield Drift")

            st.markdown(
                f'<div class="ticker-card" style="text-align: left; padding: 12px 14px;">'
                f'<div class="ticker-label">🏛️ US10Y YIELD MOMENTUM</div>'
                f'<div style="font-size: 15px; font-weight: 800; color: #FFFFFF; margin-top: 4px;">{y10_val:.3f}% <span style="font-size: 14px; color:{y_color};">({y10_chg:+.3f}%)</span></div>'
                f'<div style="font-size: 13.5px; color: {y_color}; font-weight: 700; margin-top: 2px;">{y_desc}</div>'
                f'<div style="font-size: 13.5px; color: #94A3B8; margin-top: 2px;">2Y/10Y Spread: {macro_data["yield_spread"]:+.2f}%</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        with k3:
            y2_val = macro_data.get("us02y_yield", 4.10)
            y2_chg = macro_data.get("us02y_change", 0.0)
            spread_val = macro_data.get("yield_spread", 0.10)
            spread_color = "#10B981" if spread_val > 0 else "#EF4444"
            spread_status = "Normal Curve (Steepening)" if spread_val > 0 else "Inverted Curve (Recession Watch)"
            y2_color = "#10B981" if y2_chg < -0.01 else ("#EF4444" if y2_chg > 0.01 else "#F59E0B")

            st.markdown(
                f'<div class="ticker-card" style="text-align: left; padding: 12px 14px;">'
                f'<div class="ticker-label">⚡ 2Y/10Y SPREAD & FED PROXY</div>'
                f'<div style="font-size: 15px; font-weight: 800; color: {spread_color}; margin-top: 4px;">{spread_val:+.3f}% <span style="font-size: 13.5px; color:#94A3B8;">(10Y - 2Y)</span></div>'
                f'<div style="font-size: 13.5px; color: #CBD5E1; margin-top: 2px;"><b>US 02Y:</b> {y2_val:.3f}% <span style="color:{y2_color}; font-weight:700;">({y2_chg:+.3f} pts)</span></div>'
                f'<div style="font-size: 13.5px; color: #94A3B8; margin-top: 2px;">{spread_status}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        # D. Historical Reaction Precedent & Causality
        st.markdown(f"### {t('history_title', lang_choice)}")
        st.markdown(f"*{t('history_explanation', lang_choice)}*")

        selected_event = st.selectbox(
            "Select Macro Precedent Event / ආර්ථික සිදුවීමක් තෝරන්න",
            options=list(HISTORICAL_EVENTS.keys()),
            format_func=lambda x: HISTORICAL_EVENTS[x]["event_name"]
        )
        
        comp = compare_historical_precedent(selected_event, macro_data["yield_pressure"], geo_data["risk_level"])
        prec = comp["sample_precedent"]

        why_reason = prec["why_it_happened_si"] if lang_choice == "si" else prec["why_it_happened_en"]
        duration_summary = comp["duration_summary_si"] if lang_choice == "si" else comp["duration_summary_en"]

        st.markdown(f"""
        <div style="background: #161B26; border: 1px solid #283347; border-radius: 10px; padding: 14px; margin-top: 10px;">
            <div style="color: #F59E0B; font-weight: 700; font-size: 14px;">
                {comp['event_name']} ({prec['date']})
            </div>
            <div style="margin: 6px 0; font-size: 13px;">
                <b>Historical 15m Move:</b> <span style="color:#10B981; font-weight:700;">{prec['reaction_15m']}</span> | 
                <b>1-Hour Profile:</b> {prec['reaction_1h']}
            </div>
            <div style="background: rgba(0,0,0,0.25); padding: 8px 12px; border-left: 3px solid #F59E0B; border-radius: 4px; font-size: 14px; margin: 8px 0;">
                <b>{t('why_it_happened', lang_choice)}</b><br>{why_reason}
            </div>
            <div style="font-size: 14px; color: #CBD5E1; margin-top: 8px;">
                <b>🎯 Today's Precedent Projection:</b> <span style="color:#F59E0B; font-weight:700;">{comp['predicted_pips']} ({comp['move_type']})</span><br>
                <b>⏱️ Duration Forecast:</b> {duration_summary}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        # A. Geopolitical & War Risk Barometer
        st.markdown(f"### {t('geo_title', lang_choice)}")
        
        geo_badge_color = "#EF4444" if geo_data["score"] >= 65 else ("#F59E0B" if geo_data["score"] >= 40 else "#10B981")
        geo_status_text = t("geo_status_" + ("extreme" if geo_data["score"] >= 65 else ("elevated" if geo_data["score"] >= 40 else "calm")), lang_choice)
        
        st.markdown(f"""
        <div class="ticker-card" style="text-align: left; border-left: 4px solid {geo_badge_color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="ticker-label">{t('geo_safe_haven', lang_choice)}</span>
                <span style="font-size: 18px; font-weight: 800; color: {geo_badge_color};">{geo_data['score']}/100</span>
            </div>
            <div style="font-size: 14px; font-weight: 700; color: #FFFFFF; margin: 6px 0;">
                {geo_status_text}
            </div>
            <div style="font-size: 14px; color: #94A3B8;">
                <b>Active Gold Impulse:</b> {geo_data['impulse']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # B. Live Breaking Conflict & Financial Wires
        st.markdown(f"#### 🛰️ {t('breaking_wires', lang_choice)}")
        news_container = st.container(height=320)
        with news_container:
            for item in geo_data["headlines"][:10]:
                if item["bias"] == "BULLISH_GOLD":
                    badge = "<span class='news-badge badge-bullish'>🟢 BULLISH GOLD (WAR/HEDGE)</span>"
                elif item["bias"] == "BEARISH_GOLD":
                    badge = "<span class='news-badge badge-bearish'>🔴 BEARISH GOLD (DE-ESCALATION)</span>"
                else:
                    badge = "<span class='news-badge badge-neutral'>🟡 NEUTRAL</span>"

                st.markdown(f"""
                <div style="padding: 8px 0; border-bottom: 1px solid #1E293B;">
                    <div style="font-size: 14px; font-weight: 600; color: #E2E8F0;">
                        <a href="{item['link']}" target="_blank" style="text-decoration:none; color:#E2E8F0;">{item['title']}</a>
                    </div>
                    <div style="margin-top: 4px; display: flex; justify-content: space-between; align-items: center;">
                        {badge}
                        <span style="font-size: 12.5px; color: #64748B;">{item['source']} | {item['published']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.write("")

        # C. Non-News Periods Analysis
        st.markdown(f"### {t('non_news_title', lang_choice)}")
        st.markdown(f"""
        <div style="background: #161B26; border: 1px solid #283347; border-radius: 10px; padding: 14px; font-size: 14px; color: #CBD5E1;">
            <p style="margin-bottom: 8px;">{t('non_news_desc', lang_choice)}</p>
            <ul style="padding-left: 18px; margin: 0;">
                <li><b>Real Rate Drift:</b> If Treasury yields drift higher during London/NY overlap, Gold faces steady sell pressure.</li>
                <li><b>Central Bank Floor:</b> Physical bullion accumulation by BRICS & Global Central Banks forms a strong buying floor on intraday dips.</li>
                <li><b>Weekend & Overnight Gap Risk:</b> Traders maintain long Gold positions into market close as geopolitical protection.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # 9. AI Strategic Macro Deep-Dive Playbook
    st.markdown("---")
    st.markdown(f"## {t('ai_analyst_title', lang_choice)}")
    st.markdown(ai_assessment["narrative"])

    # 10. Subtle, Elegant Branding Footer
    st.markdown(f"""
    <div class="footer-bar">
        <b>OCTEWYA Institutional Trading Technologies</b> &bull; {t('brand_copyright', lang_choice)}<br>
        <span style="font-size: 13.5px; color: #475569;">Quantitative Yields & Geopolitical Intelligence for High-Frequency Scalpers</span>
    </div>
    """, unsafe_allow_html=True)

# Run Master Dashboard Fragment
render_main_dashboard(lang_choice, tz_choice)
