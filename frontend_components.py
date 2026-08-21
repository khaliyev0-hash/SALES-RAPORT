"""
Frontend Components Engine (Tier-1 Luxury SaaS Interface)
Enterprise SaaS UI/UX Overhaul - High Precision CSS Overrides
Global Selectboxes & Inputs, Tab Neon Glow & Red Underline Destruction, DataFrames Dark Lock
"""

import json
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


def format_currency_azn(val: float) -> str:
    """Formats numbers to AZN currency (e.g. 624,771 ₼, 1.25M ₼)."""
    if abs(val) >= 1_000_000:
        return f"{val / 1_000_000:.2f}M ₼"
    elif abs(val) >= 1_000:
        return f"{val / 1_000:.1f}K ₼"
    else:
        return f"{val:,.2f} ₼"


def inject_global_theme_css():
    """Injects high-priority Cyberpunk Dark Glass CSS stylesheet."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&display=swap');

        /* --- 1. Global Reset & Hard Lock --- */
        :root {
            color-scheme: dark !important;

            /* --- Force native st.dataframe (glide-data-grid canvas) to dark theme ---
               This widget renders on a <canvas> and reads its colors from these
               CSS custom properties at mount time, NOT from element CSS below.
               Without this (and/or .streamlit/config.toml theme=dark), the grid
               stays white no matter how the wrapper div is styled. */
            --gdg-bg-cell: #0B1120 !important;
            --gdg-bg-cell-medium: #101726 !important;
            --gdg-bg-header: #0F172A !important;
            --gdg-bg-header-has-focus: #1E293B !important;
            --gdg-bg-header-hovered: #1E293B !important;
            --gdg-text-dark: #F8FAFC !important;
            --gdg-text-medium: #CBD5E1 !important;
            --gdg-text-light: #94A3B8 !important;
            --gdg-text-bubble: #F8FAFC !important;
            --gdg-bg-bubble: #1E293B !important;
            --gdg-bg-bubble-selected: #0284C7 !important;
            --gdg-text-bubble-selected: #FFFFFF !important;
            --gdg-border-color: rgba(0, 242, 254, 0.25) !important;
            --gdg-horizontal-border-color: rgba(0, 242, 254, 0.15) !important;
            --gdg-drilldown-border: rgba(0, 242, 254, 0.4) !important;
            --gdg-link-color: #00F2FE !important;
            --gdg-accent-color: #00F2FE !important;
            --gdg-accent-fg: #070A13 !important;
            --gdg-accent-light: rgba(0, 242, 254, 0.16) !important;
            --gdg-bg-search-result: rgba(0, 242, 254, 0.25) !important;
        }

        html, body, [data-testid="stAppViewContainer"], .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] {
            background-color: #070A13 !important;
            background: radial-gradient(circle at 50% 0%, #0F172A 0%, #070A13 75%) !important;
            color: #F8FAFC !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
        }

        /* --- Dark Frosted Sidebar --- */
        [data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
            background: rgba(15, 23, 42, 0.95) !important;
            border-right: 1px solid rgba(0, 242, 254, 0.2) !important;
            box-shadow: 10px 0 25px rgba(0, 0, 0, 0.5) !important;
        }

        /* =======================================================
           1. STRICT GLOBAL DARK LOCK FOR ALL SELECTBOXES & INPUTS (SIDEBAR & MAIN BODY)
           ======================================================= */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"],
        div[data-baseweb="input"] input,
        div[data-baseweb="base-input"],
        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        .stTextInput input,
        .stDateInput input,
        /* data-testid based selectors: current Streamlit builds have dropped
           some legacy .stDateInput / .stTextInput wrapper classes, so the
           rules above alone can silently stop matching after an upgrade. */
        [data-testid="stDateInput"] input,
        [data-testid="stDateInput"] div[data-baseweb="input"],
        [data-testid="stDateInput"] div[data-baseweb="base-input"],
        [data-testid="stTextInput"] input,
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div,
        [data-testid="stNumberInput"] input {
            background-color: #101726 !important;
            background: #101726 !important;
            border: 1px solid rgba(0, 242, 254, 0.35) !important;
            border-radius: 8px !important;
            color: #F8FAFC !important;
            -webkit-text-fill-color: #F8FAFC !important;
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.1) !important;
        }

        div[data-baseweb="select"] *,
        div[data-baseweb="input"] *,
        [data-testid="stDateInput"] *,
        [data-testid="stTextInput"] *,
        [data-testid="stNumberInput"] * {
            color: #F8FAFC !important;
            -webkit-text-fill-color: #F8FAFC !important;
        }

        /* The date-range display text specifically (the "2026/07/22 - 2026/08/21"
           readout) sits in a nested span/div that inherits from a baseweb
           class not always caught above — force it explicitly. */
        [data-testid="stDateInput"] input::placeholder {
            color: #94A3B8 !important;
            -webkit-text-fill-color: #94A3B8 !important;
        }

        div[data-baseweb="select"] svg {
            fill: #00F2FE !important;
            color: #00F2FE !important;
        }

        div[data-baseweb="tag"] {
            background: linear-gradient(135deg, rgba(0, 242, 254, 0.2), rgba(99, 102, 241, 0.25)) !important;
            border: 1px solid rgba(0, 242, 254, 0.5) !important;
            border-radius: 6px !important;
        }
        div[data-baseweb="tag"] span {
            color: #00F2FE !important;
            font-weight: 600 !important;
        }

        /* Sidebar labels & Headings */
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] label p,
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3,
        [data-testid="stSidebar"] .stMarkdown h4 {
            color: #38BDF8 !important;
            font-weight: 700 !important;
            letter-spacing: 0.4px !important;
            text-shadow: 0 0 8px rgba(56, 189, 248, 0.6) !important;
        }

        /* =======================================================
           2. PERMANENT BRIGHT CYAN GLOW ON ALL TABS (DESTROY RED HIGHLIGHT)
           ======================================================= */
        div[data-testid="stTabs"] > div[role="tablist"],
        div[data-testid="stTabs"] [data-baseweb="tab-list"] {
            background: transparent !important;
            border-bottom: 1px solid rgba(0, 242, 254, 0.25) !important;
            gap: 6px !important;
        }

        div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
        div[data-testid="stTabs"] [data-testid="stTabHighlight"],
        div[data-baseweb="tab-highlight"] {
            display: none !important;
            opacity: 0 !important;
            height: 0px !important;
            background: transparent !important;
        }

        div[data-testid="stTabs"] button,
        div[data-testid="stTabs"] button[role="tab"],
        button[data-baseweb="tab"] {
            background: rgba(15, 23, 42, 0.85) !important;
            border: 1px solid rgba(0, 242, 254, 0.3) !important;
            border-radius: 8px 8px 0 0 !important;
            padding: 8px 16px !important;
            margin-right: 4px !important;
        }

        div[data-testid="stTabs"] button *,
        div[data-testid="stTabs"] button p,
        div[data-testid="stTabs"] button span,
        div[data-testid="stTabs"] button div,
        div[data-testid="stTabs"] button [data-testid="stMarkdownContainer"],
        div[data-testid="stTabs"] button [data-testid="stMarkdownContainer"] p,
        div[data-testid="stTabs"] [role="tab"] *,
        div[data-testid="stTabs"] [data-baseweb="tab"] *,
        button[data-baseweb="tab"] * {
            color: #38BDF8 !important;
            opacity: 1 !important;
            -webkit-text-fill-color: #38BDF8 !important;
            font-weight: 700 !important;
            font-size: 13px !important;
            text-shadow: 0 0 8px rgba(56, 189, 248, 0.8) !important;
        }

        /* Belt-and-braces: some Streamlit builds render the tab label text
           directly as a text node inside the button with no wrapping span,
           so the rules above (which target descendants) can miss it. */
        div[data-testid="stTabs"] button,
        button[data-baseweb="tab"] {
            color: #38BDF8 !important;
            -webkit-text-fill-color: #38BDF8 !important;
        }

        div[data-testid="stTabs"] button[aria-selected="true"],
        button[data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(180deg, rgba(0, 242, 254, 0.3), rgba(15, 23, 42, 0.95)) !important;
            border: 1px solid #00F2FE !important;
            border-bottom: 3px solid #00F2FE !important;
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.5) !important;
        }

        div[data-testid="stTabs"] button[aria-selected="true"],
        div[data-testid="stTabs"] button[aria-selected="true"] * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            text-shadow: 0 0 12px rgba(0, 242, 254, 1) !important;
        }

        /* =======================================================
           3. FIX ALL WHITE DATAFRAME & TABLE CONTAINERS
           ======================================================= */
        [data-testid="stDataFrame"],
        [data-testid="stTable"],
        .stDataFrame,
        div[data-testid="stDataFrame"] > div,
        div[data-testid="stDataFrame"] canvas {
            background-color: #0B1120 !important;
            background: #0B1120 !important;
            border: 1px solid rgba(0, 242, 254, 0.25) !important;
            border-radius: 10px !important;
            color: #F8FAFC !important;
        }

        /* Datepicker calendar container popup */
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] > div,
        div[data-baseweb="calendar"],
        div[data-baseweb="calendar"] * {
            background-color: #0F172A !important;
            color: #F8FAFC !important;
            border-color: rgba(0, 242, 254, 0.25) !important;
        }

        div[data-baseweb="calendar"] header,
        div[data-baseweb="calendar"] select {
            background-color: #1E293B !important;
            color: #00F2FE !important;
        }

        div[data-baseweb="calendar"] [role="gridcell"] {
            background-color: #0F172A !important;
            color: #E2E8F0 !important;
        }

        div[data-baseweb="calendar"] [aria-selected="true"] {
            background: linear-gradient(135deg, #0284C7, #00F2FE) !important;
            color: #070A13 !important;
            font-weight: 800 !important;
            border-radius: 6px !important;
        }

        /* Dropdown popup menus */
        ul[data-baseweb="menu"],
        div[data-baseweb="popover"] ul {
            background-color: #0F172A !important;
            border: 1px solid rgba(0, 242, 254, 0.35) !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8) !important;
        }

        li[data-baseweb="menu-item"],
        div[role="option"] {
            background-color: #0F172A !important;
            color: #E2E8F0 !important;
        }

        li[data-baseweb="menu-item"]:hover,
        div[role="option"]:hover,
        li[data-baseweb="menu-item"][aria-selected="true"] {
            background-color: rgba(0, 242, 254, 0.18) !important;
            color: #00F2FE !important;
        }

        /* File Uploader */
        [data-testid="stFileUploader"], 
        [data-testid="stFileUploader"] section, 
        [data-testid="stFileUploader"] > div,
        [data-testid="stFileUploaderDropzone"] {
            background-color: #101726 !important;
            background: #101726 !important;
            border: 1px dashed rgba(0, 242, 254, 0.4) !important;
            border-radius: 10px !important;
            color: #F8FAFC !important;
        }

        [data-testid="stFileUploaderDropzoneInstructions"] div,
        [data-testid="stFileUploader"] small,
        [data-testid="stFileUploader"] span {
            color: #94A3B8 !important;
        }

        /* Remove default Streamlit top header gap */
        header[data-testid="stHeader"] {
            background: transparent !important;
            height: 0rem !important;
            z-index: -1 !important;
        }

        .block-container {
            padding-top: 0.3rem !important;
            padding-bottom: 0.3rem !important;
            max-width: 98.5% !important;
        }

        div[data-testid="column"] {
            padding: 0 3px;
        }

        /* Glassmorphic Containers & Cards */
        div[data-testid="stVerticalBlock"] > div:has(.metric-card),
        .cyber-card, .metric-card,
        div[data-testid="stMetric"],
        .header-container {
            background: rgba(15, 23, 42, 0.75) !important;
            backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37) !important;
            color: #F8FAFC !important;
            transition: all 0.3s ease !important;
        }

        .cyber-card:hover, .metric-card:hover {
            transform: translateY(-3px) !important;
            border-color: rgba(0, 242, 254, 0.4) !important;
            box-shadow: 0 10px 25px rgba(0, 242, 254, 0.2) !important;
        }

        /* KPI Values & Badges */
        .metric-value, [data-testid="stMetricValue"] {
            color: #00F2FE !important;
            text-shadow: 0 0 12px rgba(0, 242, 254, 0.6) !important;
            font-weight: 800 !important;
        }

        /* Glowing Buttons */
        .stButton > button,
        div[data-testid="stButton"] > button,
        button[kind="secondary"],
        div[data-testid="stFileUploader"] button {
            background: linear-gradient(135deg, #1E293B, #0F172A) !important;
            color: #00F2FE !important;
            border: 1px solid rgba(0, 242, 254, 0.4) !important;
            border-radius: 8px !important;
            box-shadow: 0 0 12px rgba(0, 242, 254, 0.2) !important;
            font-weight: 600 !important;
        }

        .stButton > button:hover,
        div[data-testid="stButton"] > button:hover,
        button[kind="secondary"]:hover {
            background: linear-gradient(135deg, #0284C7, #0369A1) !important;
            color: #FFFFFF !important;
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.5) !important;
        }

        /* Pulse Dot Indicator Animation */
        .live-dot {
            width: 9px;
            height: 9px;
            background: #10B981;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            animation: live-pulse 1.8s infinite cubic-bezier(0.66, 0, 0, 1);
        }

        @keyframes live-pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        /* Khayal Aliyev Pulsating Neon Badge Styling */
        .creator-badge-container {
            display: flex;
            justify-content: flex-end;
            align-items: center;
        }
        .creator-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 5px 12px;
            border-radius: 20px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.18), rgba(236, 72, 153, 0.18));
            border: 1px solid rgba(168, 85, 247, 0.4);
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.35), inset 0 0 10px rgba(99, 102, 241, 0.2);
            animation: neonGlowPulse 2.5s infinite alternate ease-in-out;
        }
        .creator-name {
            font-weight: 800;
            color: #38bdf8;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-shadow: 0 0 8px rgba(56, 189, 248, 0.8), 0 0 16px rgba(168, 85, 247, 0.6);
            animation: textFlicker 3s infinite alternate;
        }
        .badge-text {
            color: #e2e8f0;
            font-size: 11px;
            font-weight: 500;
        }
        @keyframes neonGlowPulse {
            0% {
                box-shadow: 0 0 8px rgba(56, 189, 248, 0.3), inset 0 0 5px rgba(99, 102, 241, 0.1);
                border-color: rgba(56, 189, 248, 0.3);
            }
            100% {
                box-shadow: 0 0 22px rgba(168, 85, 247, 0.6), inset 0 0 14px rgba(236, 72, 153, 0.3);
                border-color: rgba(236, 72, 153, 0.6);
            }
        }
        @keyframes textFlicker {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.85; filter: brightness(1.2); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_khayal_aliyev_branding_badge():
    """Renders the Khayal Aliyev Pulsating Neon Badge."""
    html = """
    <div class="creator-badge-container">
      <div class="creator-badge">
        <span class="badge-icon">⚡</span>
        <span class="badge-text">Architected & Engineered by <span class="creator-name">Khayal Aliyev</span></span>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
