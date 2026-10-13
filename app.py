"""
OCTEWYA | XAUUSD Institutional Macro & Yields Intelligence Desk
Real-time Geopolitical, Treasury Yields (US02Y / US10Y) & Dynamic Precedent Engine.
© OCTEWYA all rights reserved.
"""

import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# Local Modules
from modules.i18n import t, LANGUAGES
from modules.market_data import fetch_live_macro_data, TIMEZONES, get_current_time_str
from modules.geopolitics_engine import fetch_geopolitical_intel
from modules.history_engine import HISTORICAL_EVENTS, compare_historical_precedent
from modules.calendar_engine import fetch_dynamic_calendar
from modules.ai_analyst import generate_macro_assessment

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
    
    /* Top Header Bar */
    .brand-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 20px;
        background: linear-gradient(90deg, #161B26 0%, #1A2234 100%);
        border: 1px solid #283347;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .brand-title {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: 1px;
        color: #F59E0B;
        margin: 0;
    }
    .brand-subtitle {
        font-size: 13px;
        color: #94A3B8;
        margin-top: 4px;
    }
    .brand-badge {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid #F59E0B;
        color: #F59E0B;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
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
        font-size: 12px;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .ticker-value {
        font-size: 22px;
        font-weight: 800;
        color: #F8FAFC;
    }
    .ticker-delta-green {
        color: #10B981;
        font-size: 12px;
        font-weight: 600;
    }
    .ticker-delta-red {
        color: #EF4444;
        font-size: 12px;
        font-weight: 600;
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
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-bullish { background: rgba(16, 185, 129, 0.2); color: #10B981; border: 1px solid #10B981; }
    .badge-bearish { background: rgba(239, 68, 68, 0.2); color: #EF4444; border: 1px solid #EF4444; }
    .badge-neutral { background: rgba(148, 163, 184, 0.2); color: #94A3B8; border: 1px solid #64748B; }

    /* Footer Branding */
    .footer-bar {
        text-align: center;
        padding: 16px;
        color: #64748B;
        font-size: 12px;
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
            <div style="font-size: 11px; color: #64748B; margin-top: 4px;">© OCTEWYA all rights reserved</div>
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
        
        st.markdown("<div style='text-align:center; font-size:11px; color:#64748B; margin-top:20px;'>Protected Institutional Environment &bull; Unauthorized Access Prohibited</div>", unsafe_allow_html=True)
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
        options=[30, 60, 120, 0],
        format_func=lambda s: "Off (Manual)" if s == 0 else f"Every {s} seconds",
        index=0
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

    # Logout Button
    st.markdown("---")
    if st.button("🚪 Logout / ඉවත් වන්න", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

    # Elegant subtle branding in sidebar
    st.markdown(f"""
    <div style='margin-top: 30px; font-size: 11px; color: #64748B; text-align: center;'>
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
    precedent_data = compare_historical_precedent("CPI", macro_data["yield_pressure"], geo_data["risk_level"])
    ai_assessment = generate_macro_assessment(macro_data, geo_data, precedent_data, lang_choice)

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
            <div style="font-size: 11px; color: #94A3B8; margin-top: 5px;">
                {t("last_updated", lang_choice)}: <span style="color:#10B981; font-weight:700;">{live_tz_time}</span> 
                <span style="font-size:10px; color:#64748B;">({tz_label})</span>
            </div>
        </div>
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
        y2_delta_class = "ticker-delta-green" if macro_data["us02y_change"] >= 0 else "ticker-delta-red"
        y2_sign = "+" if macro_data["us02y_change"] >= 0 else ""
        st.markdown(f"""
        <div class="ticker-card">
            <div class="ticker-label">{t("us02y_yield", lang_choice)}</div>
            <div class="ticker-value">{macro_data['us02y_yield']:.3f}%</div>
            <div class="{y2_delta_class}">{y2_sign}{macro_data['us02y_change']:.3f} pts</div>
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
            <div style="font-size: 11px; color: #94A3B8;">Buyers vs Sellers</div>
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
            ec5.markdown(f"{bias_badge} <br><span style='font-size:11px; color:#94A3B8;'>{reason_txt}</span>", unsafe_allow_html=True)
            st.markdown("<hr style='margin:6px 0; border-color:#1E293B;'>", unsafe_allow_html=True)

    st.write("")

    # 8. Main Working Deck (2-Column Grid)
    left_col, right_col = st.columns([1.1, 0.9])

    with left_col:
        # A. Master Strategic Bias & Regime
        bias_style = "buy-signal" if "BUY" in ai_assessment["master_bias"] else ("sell-signal" if "SELL" in ai_assessment["master_bias"] else "neutral-signal")
        
        st.markdown(f"""
        <div class="signal-box {bias_style}">
            <div style="font-size: 13px; font-weight: 700; color: #94A3B8; text-transform: uppercase;">
                {t('master_signal_title', lang_choice)}
            </div>
            <div style="font-size: 26px; font-weight: 900; margin: 8px 0; color: #FFFFFF;">
                {ai_assessment['bias_label']}
            </div>
            <div style="font-size: 13px; color: #CBD5E1;">
                <b>{t('confidence_level', lang_choice)}:</b> {ai_assessment['conviction']}% | 
                <b>Order Flow:</b> {macro_data['buyers_pct']}% Buyers vs {macro_data['sellers_pct']}% Sellers
            </div>
        </div>
        """, unsafe_allow_html=True)

        # B. Regime & Duration Predictor Card
        st.markdown(f"### {t('regime_title', lang_choice)}")
        rc1, rc2 = st.columns(2)
        with rc1:
            st.markdown(f"""
            <div class="ticker-card" style="text-align: left;">
                <div class="ticker-label">{t('regime_title', lang_choice)}</div>
                <div style="font-size: 16px; font-weight: 700; color: #F59E0B;">
                    {t('regime_' + macro_data['regime'].lower(), lang_choice)}
                </div>
                <div style="font-size: 12px; color: #94A3B8; margin-top: 4px;">
                    <b>{t('expected_duration', lang_choice)}:</b> {macro_data['estimated_duration']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with rc2:
            st.markdown(f"""
            <div class="ticker-card" style="text-align: left;">
                <div class="ticker-label">{t('breakout_risk', lang_choice)}</div>
                <div style="font-size: 16px; font-weight: 700; color: #10B981;">
                    {macro_data['breakout_risk_pct']}% Probability
                </div>
                <div style="font-size: 12px; color: #94A3B8; margin-top: 4px;">
                    <b>ATR (M15 Volatility):</b> ±${macro_data['gold_atr']:.2f} pips
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # C. Yields Driver Analysis
        st.markdown(f"### {t('yield_analysis_title', lang_choice)}")
        st.info(f"💡 **Insight:** {t('yield_insight', lang_choice)}")

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=macro_data["us10y_yield"],
            delta={'reference': 4.0, 'position': "top", 'valueformat': ".2f"},
            title={'text': "US10Y Yield vs Gold Pressure Zone", 'font': {'size': 14, 'color': '#CBD5E1'}},
            gauge={
                'axis': {'range': [3.0, 5.5], 'tickcolor': "#94A3B8"},
                'bar': {'color': "#F59E0B"},
                'steps': [
                    {'range': [3.0, 3.8], 'color': "rgba(16, 185, 129, 0.4)"},
                    {'range': [3.8, 4.4], 'color': "rgba(245, 158, 11, 0.4)"},
                    {'range': [4.4, 5.5], 'color': "rgba(239, 68, 68, 0.4)"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 3},
                    'thickness': 0.75,
                    'value': 4.5
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor="#161B26",
            font={'color': "#E6EDF3"},
            height=220,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

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
            <div style="background: rgba(0,0,0,0.25); padding: 8px 12px; border-left: 3px solid #F59E0B; border-radius: 4px; font-size: 12px; margin: 8px 0;">
                <b>{t('why_it_happened', lang_choice)}</b><br>{why_reason}
            </div>
            <div style="font-size: 12px; color: #CBD5E1; margin-top: 8px;">
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
            <div style="font-size: 12px; color: #94A3B8;">
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
                    <div style="font-size: 12px; font-weight: 600; color: #E2E8F0;">
                        <a href="{item['link']}" target="_blank" style="text-decoration:none; color:#E2E8F0;">{item['title']}</a>
                    </div>
                    <div style="margin-top: 4px; display: flex; justify-content: space-between; align-items: center;">
                        {badge}
                        <span style="font-size: 10px; color: #64748B;">{item['source']} | {item['published']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.write("")

        # C. Non-News Periods Analysis
        st.markdown(f"### {t('non_news_title', lang_choice)}")
        st.markdown(f"""
        <div style="background: #161B26; border: 1px solid #283347; border-radius: 10px; padding: 14px; font-size: 12px; color: #CBD5E1;">
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
        <span style="font-size: 11px; color: #475569;">Quantitative Yields & Geopolitical Intelligence for High-Frequency Scalpers</span>
    </div>
    """, unsafe_allow_html=True)

# Run Master Dashboard Fragment
render_main_dashboard(lang_choice, tz_choice)
