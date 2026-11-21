"""Custom Amazon-inspired styling, CSS injection, and UI card components."""

import streamlit as st

AMAZON_DARK_NAVY = "#131921"
AMAZON_SQUID_INK = "#232F3E"
AMAZON_ORANGE = "#FF9900"
AMAZON_ORANGE_HOVER = "#E67A00"
AMAZON_BLUE = "#146EB4"
AMAZON_TEAL = "#007185"
AMAZON_TEXT_DARK = "#0F1111"
AMAZON_TEXT_MUTED = "#565959"
AMAZON_BORDER = "#D5D9D9"
AMAZON_BG_LIGHT = "#F7F8FA"


def inject_custom_css():
    """Inject modern Amazon India inspired styling across all dashboard pages."""
    css = f"""
    <style>
    /* Global Page Styling */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    
    .stApp {{
        background-color: {AMAZON_BG_LIGHT};
        color: {AMAZON_TEXT_DARK};
    }}

    /* Top Padding & Clean Margin */
    .block-container {{
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1400px;
    }}

    /* Amazon Dark Navy Sidebar */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #131921 0%, #1c2633 60%, #232f3e 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }}

    section[data-testid="stSidebar"] * {{
        color: #E6E6E6 !important;
    }}

    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {{
        color: #FFFFFF !important;
        font-weight: 700;
        letter-spacing: 0.3px;
    }}

    /* Sidebar Radio Buttons (Navigation) */
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {{
        background: rgba(255, 255, 255, 0.04);
        padding: 10px 14px;
        border-radius: 8px;
        margin-bottom: 6px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.2s ease;
        cursor: pointer;
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {{
        background: rgba(255, 153, 0, 0.12);
        border-color: {AMAZON_ORANGE};
        transform: translateX(3px);
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] {{
        background: linear-gradient(90deg, rgba(255, 153, 0, 0.25) 0%, rgba(255, 153, 0, 0.08) 100%);
        border-left: 4px solid {AMAZON_ORANGE} !important;
        border-color: {AMAZON_ORANGE};
    }}

    /* Sidebar Selectbox & Inputs */
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] > div {{
        background-color: #232F3E !important;
        border: 1px solid #3E4C59 !important;
        border-radius: 6px;
    }}

    section[data-testid="stSidebar"] .stButton > button {{
        background: linear-gradient(180deg, #FFA41C 0%, #FF8A00 100%) !important;
        color: #111111 !important;
        border: 1px solid #C47100 !important;
        border-radius: 6px;
        font-weight: 600;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        transition: all 0.2s ease;
        width: 100%;
    }}

    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: linear-gradient(180deg, #FA8900 0%, #E67A00 100%) !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        transform: translateY(-1px);
    }}

    /* Main Dashboard Header */
    .dash-header {{
        background: #FFFFFF;
        padding: 18px 24px;
        border-radius: 10px;
        border: 1px solid {AMAZON_BORDER};
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        margin-bottom: 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
    }}

    .dash-title-group h1 {{
        margin: 0;
        font-size: 24px;
        font-weight: 700;
        color: {AMAZON_DARK_NAVY};
        display: flex;
        align-items: center;
        gap: 10px;
    }}

    .dash-title-group p {{
        margin: 3px 0 0 0;
        font-size: 13px;
        color: {AMAZON_TEXT_MUTED};
    }}

    .amazon-badge {{
        background: {AMAZON_DARK_NAVY};
        color: #FFFFFF;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}

    .amazon-badge span {{
        color: {AMAZON_ORANGE};
    }}

    /* Professional KPI Card */
    .kpi-card {{
        background: #FFFFFF;
        border-radius: 10px;
        padding: 18px 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
        height: 100%;
    }}

    .kpi-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
        border-color: {AMAZON_ORANGE};
    }}

    .kpi-top-bar {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
    }}

    .kpi-card-inner {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }}

    .kpi-label {{
        font-size: 13px;
        font-weight: 600;
        color: {AMAZON_TEXT_MUTED};
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }}

    .kpi-value {{
        font-size: 26px;
        font-weight: 700;
        color: {AMAZON_TEXT_DARK};
        line-height: 1.2;
        margin-bottom: 8px;
    }}

    .kpi-icon-box {{
        width: 44px;
        height: 44px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        flex-shrink: 0;
    }}

    .kpi-subtitle {{
        font-size: 12px;
        color: {AMAZON_TEXT_MUTED};
        display: flex;
        align-items: center;
        gap: 6px;
    }}

    .pill-badge {{
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
    }}

    .pill-orange {{
        background: rgba(255, 153, 0, 0.15);
        color: #B85D00;
    }}

    .pill-blue {{
        background: rgba(20, 110, 180, 0.12);
        color: #146EB4;
    }}

    .pill-green {{
        background: rgba(6, 125, 98, 0.12);
        color: #067D62;
    }}

    .pill-red {{
        background: rgba(196, 0, 0, 0.12);
        color: #C40000;
    }}

    /* Section Subheaders */
    .section-header {{
        font-size: 17px;
        font-weight: 700;
        color: {AMAZON_DARK_NAVY};
        margin: 24px 0 14px 0;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 2px solid #EAEDED;
        padding-bottom: 8px;
    }}

    .section-header::before {{
        content: "";
        display: inline-block;
        width: 4px;
        height: 18px;
        background: {AMAZON_ORANGE};
        border-radius: 2px;
    }}

    /* Chart Containers */
    .chart-box {{
        background: #FFFFFF;
        border-radius: 10px;
        padding: 16px 18px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        margin-bottom: 18px;
    }}

    /* Metric / Stat Highlight Callout */
    .insight-callout {{
        background: #F0F9FF;
        border-left: 4px solid {AMAZON_BLUE};
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin: 14px 0;
        font-size: 13px;
        color: #0C4A6E;
    }}

    /* Filter Tag Pills */
    .filter-summary-bar {{
        background: #FFFFFF;
        padding: 10px 16px;
        border-radius: 8px;
        border: 1px solid {AMAZON_BORDER};
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 13px;
    }}

    /* Footer */
    .dash-footer {{
        margin-top: 36px;
        padding-top: 18px;
        border-top: 1px solid #EAEDED;
        text-align: center;
        font-size: 12px;
        color: {AMAZON_TEXT_MUTED};
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_kpi_card(title, value, subtitle=None, icon="📈", variant="orange", pill_text=None):
    """
    Render a high-end, responsive Amazon-styled KPI card.
    Variants: 'orange', 'blue', 'green', 'red', 'teal'
    """
    colors = {
        "orange": {"top": AMAZON_ORANGE, "bg": "rgba(255, 153, 0, 0.1)", "icon_color": "#D97706", "pill": "pill-orange"},
        "blue": {"top": AMAZON_BLUE, "bg": "rgba(20, 110, 180, 0.1)", "icon_color": "#146EB4", "pill": "pill-blue"},
        "green": {"top": "#067D62", "bg": "rgba(6, 125, 98, 0.1)", "icon_color": "#067D62", "pill": "pill-green"},
        "red": {"top": "#C40000", "bg": "rgba(196, 0, 0, 0.1)", "icon_color": "#C40000", "pill": "pill-red"},
        "teal": {"top": AMAZON_TEAL, "bg": "rgba(0, 113, 133, 0.1)", "icon_color": AMAZON_TEAL, "pill": "pill-blue"}
    }
    cfg = colors.get(variant, colors["orange"])

    pill_html = f"<span class='pill-badge {cfg['pill']}'>{pill_text}</span>" if pill_text else ""
    subtitle_html = f"<div class='kpi-subtitle'>{pill_html} <span>{subtitle or ''}</span></div>" if (subtitle or pill_text) else ""

    html = f"""
    <div class="kpi-card">
        <div class="kpi-top-bar" style="background: {cfg['top']};"></div>
        <div class="kpi-card-inner">
            <div>
                <div class="kpi-label">{title}</div>
                <div class="kpi-value">{value}</div>
            </div>
            <div class="kpi-icon-box" style="background: {cfg['bg']}; color: {cfg['icon_color']};">
                {icon}
            </div>
        </div>
        {subtitle_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_header(title, subtitle, record_count=None, total_count=None):
    """Render top dashboard header with Amazon logo styling and filter indicators."""
    filter_info = ""
    if record_count is not None and total_count is not None:
        pct = (record_count / total_count) * 100 if total_count > 0 else 0
        filter_info = f"""
        <div class="amazon-badge">
            <span>●</span> {record_count:,} / {total_count:,} orders ({pct:.0f}%)
        </div>
        """

    html = f"""
    <div class="dash-header">
        <div class="dash-title-group">
            <h1>
                <span style="color: {AMAZON_ORANGE};">amazon</span><span style="font-size: 16px; color: {AMAZON_TEXT_MUTED}; font-weight: 500;">.in</span>
                &nbsp;|&nbsp; {title}
            </h1>
            <p>{subtitle}</p>
        </div>
        {filter_info}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_section_header(title, icon="🔹"):
    """Render a section header with Amazon orange accent."""
    html = f"""
    <div class="section-header">
        <span>{icon}</span> {title}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
