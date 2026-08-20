"""
Frontend Components Engine (Tier-1 Luxury SaaS Interface)
Enterprise SaaS UI/UX Overhaul - High Precision CSS Overrides
Sidebar White Boxes Fix & Unreadable Tabs Fix
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
           1. FIX ALL WHITE INPUT BOXES IN SIDEBAR (SELECTBOX, DATE, MULTISELECT)
           ======================================================= */
        /* All selectboxes, date input, and multiselect containers in sidebar */
        [data-testid="stSidebar"] div[data-baseweb="select"] > div,
        [data-testid="stSidebar"] div[data-baseweb="input"],
        [data-testid="stSidebar"] div[data-baseweb="input"] > input,
        [data-testid="stSidebar"] .stSelectbox > div > div,
        [data-testid="stSidebar"] .stMultiSelect > div > div,
        [data-testid="stSidebar"] .stDateInput input,
        [data-testid="stSidebar"] div[data-testid="stDateInput"] > div > div {
            background-color: #101726 !important;
            background: #101726 !important;
            border: 1px solid rgba(0, 242, 254, 0.35) !important;
            border-radius: 8px !important;
            color: #F8FAFC !important;
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.1) !important;
        }

        /* Fix text and placeholder inside selectboxes and inputs */
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] div[data-baseweb="select"] * {
            color: #F8FAFC !important;
            -webkit-text-fill-color: #F8FAFC !important;
        }

        [data-testid="stSidebar"] div[data-baseweb="select"] span {
            color: #94A3B8 !important;
        }

        [data-testid="stSidebar"] div[data-baseweb="select"] svg {
            fill: #00F2FE !important;
            color: #00F2FE !important;
        }

        /* =======================================================
           1b. FIX WHITE FILE UPLOADER BOX IN SIDEBAR
           ======================================================= */
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"],
        [data-testid="stSidebar"] section[data-testid="stFileUploaderDropzone"],
        [data-testid="stSidebar"] div[data-testid="stFileUploader"] section {
            background: #101726 !important;
            border: 1px dashed rgba(0, 242, 254, 0.4) !important;
            border-radius: 10px !important;
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.1) !important;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] *,
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] * {
            color: #E2E8F0 !important;
            -webkit-text-fill-color: #E2E8F0 !important;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] small,
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] span {
            color: #94A3B8 !important;
            -webkit-text-fill-color: #94A3B8 !important;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] svg {
            fill: #00F2FE !important;
            color: #00F2FE !important;
        }

        /* Uploaded file row (name / size / remove icon) */
        [data-testid="stSidebar"] [data-testid="stFileUploaderFile"] {
            background: #0F172A !important;
            border: 1px solid rgba(0, 242, 254, 0.2) !important;
            border-radius: 8px !important;
            color: #F8FAFC !important;
        }
        [data-testid="stSidebar"] [data-testid="stFileUploaderFile"] * {
            color: #F8FAFC !important;
            -webkit-text-fill-color: #F8FAFC !important;
        }

        [data-testid="stSidebar"] div[data-baseweb="tag"] {
            background: linear-gradient(135deg, rgba(0, 242, 254, 0.2), rgba(99, 102, 241, 0.25)) !important;
            border: 1px solid rgba(0, 242, 254, 0.5) !important;
            border-radius: 6px !important;
        }
        [data-testid="stSidebar"] div[data-baseweb="tag"] span {
            color: #00F2FE !important;
            font-weight: 600 !important;
        }

        /* Dropdown Popup Menus & List Items */
        ul[data-baseweb="menu"], div[data-baseweb="popover"], div[role="listbox"] {
            background-color: #0F172A !important;
            border: 1px solid rgba(0, 242, 254, 0.3) !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8) !important;
        }

        li[data-baseweb="menu-item"], div[role="option"] {
            background-color: transparent !important;
            color: #E2E8F0 !important;
        }

        li[data-baseweb="menu-item"]:hover, div[role="option"]:hover {
            background-color: rgba(0, 242, 254, 0.15) !important;
            color: #00F2FE !important;
        }

        /* =======================================================
           1c. FIX WHITE DATE-RANGE CALENDAR POPUP
           (BaseWeb's Calendar is portaled to <body>, so it sits
           OUTSIDE [data-testid="stSidebar"] and needs global rules.)
           ======================================================= */
        div[data-baseweb="calendar"],
        div[data-baseweb="datepicker"] {
            background: #0F172A !important;
            border: 1px solid rgba(0, 242, 254, 0.3) !important;
            border-radius: 10px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8) !important;
        }

        div[data-baseweb="calendar"] div {
            background: transparent !important;
        }

        /* Month/Year header + nav arrows */
        div[data-baseweb="calendar"] div[role="presentation"],
        div[data-baseweb="calendar"] button[aria-label*="previous" i],
        div[data-baseweb="calendar"] button[aria-label*="next" i] {
            color: #38BDF8 !important;
            background: transparent !important;
        }

        /* Weekday header row (S M T W T F S) */
        div[data-baseweb="calendar"] [role="columnheader"] {
            color: #94A3B8 !important;
            font-weight: 700 !important;
        }

        /* Day cells */
        div[data-baseweb="calendar"] div[role="gridcell"] div {
            color: #F8FAFC !important;
            background: transparent !important;
        }

        /* Disabled / outside-range days */
        div[data-baseweb="calendar"] div[aria-disabled="true"] div {
            color: #475569 !important;
        }

        /* Hover state on a selectable day */
        div[data-baseweb="calendar"] div[role="gridcell"]:hover div {
            background: rgba(0, 242, 254, 0.18) !important;
            border-radius: 6px !important;
        }

        /* Selected day / range highlight keeps its accent, just force readable text */
        div[data-baseweb="calendar"] div[aria-selected="true"] div {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* Month / Year select dropdowns inside the calendar header */
        div[data-baseweb="calendar"] div[data-baseweb="select"] > div {
            background: #101726 !important;
            color: #F8FAFC !important;
            border: 1px solid rgba(0, 242, 254, 0.3) !important;
        }

        /* Force all text in sidebar labels to High-Contrast Cyan/White */
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
           2. FIX UNREADABLE TABS & REMOVE DEFAULT RED UNDERLINE
           (Rewritten against the ACTUAL rendered DOM confirmed via
           DevTools: tabs are <div data-testid="stTab" role="tab">,
           NOT <button>. Label text lives in
           div[data-testid="stMarkdownContainer"] > p. Selected state
           uses aria-selected="true" AND data-selected="true".)
           ======================================================= */
        /* Kill the pink/red pill selection indicator */
        div[role="tablist"] .react-aria-SelectionIndicator {
            display: none !important;
            background: transparent !important;
        }

        div[role="tablist"] {
            gap: 4px !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        /* Base style for ALL tab pills */
        div[data-testid="stTab"][role="tab"] {
            background: rgba(15, 23, 42, 0.9) !important;
            border: 1px solid rgba(0, 242, 254, 0.25) !important;
            border-radius: 8px 8px 0 0 !important;
            padding: 8px 16px !important;
            margin-right: 4px !important;
            transition: all 0.25s ease-in-out !important;
        }

        /* ---------------------------------------------------------
           GUARANTEED READABILITY LAYER: force every tab's paragraph
           text to a bright, high-contrast color no matter what.
           --------------------------------------------------------- */
        div[data-testid="stTab"][role="tab"] p,
        div[data-testid="stTab"][role="tab"] [data-testid="stMarkdownContainer"],
        div[data-testid="stTab"][role="tab"] [data-testid="stMarkdownContainer"] * {
            color: #7DD3FC !important;
            -webkit-text-fill-color: #7DD3FC !important;
            opacity: 1 !important;
            font-weight: 700 !important;
            font-size: 13px !important;
            text-shadow: 0 0 8px rgba(125, 211, 252, 0.9) !important;
        }

        /* ---------------------------------------------------------
           COLORFUL LAYER: distinct accent per tab, using the real
           direct-child relationship div[role="tablist"] > div[data-testid="stTab"].
           --------------------------------------------------------- */
        div[role="tablist"] > div[data-testid="stTab"]:nth-child(1) p { color: #38BDF8 !important; -webkit-text-fill-color: #38BDF8 !important; text-shadow: 0 0 8px rgba(56,189,248,0.9) !important; }
        div[role="tablist"] > div[data-testid="stTab"]:nth-child(2) p { color: #22D3EE !important; -webkit-text-fill-color: #22D3EE !important; text-shadow: 0 0 8px rgba(34,211,238,0.9) !important; }
        div[role="tablist"] > div[data-testid="stTab"]:nth-child(3) p { color: #C4B5FD !important; -webkit-text-fill-color: #C4B5FD !important; text-shadow: 0 0 8px rgba(196,181,253,0.9) !important; }
        div[role="tablist"] > div[data-testid="stTab"]:nth-child(4) p { color: #F9A8D4 !important; -webkit-text-fill-color: #F9A8D4 !important; text-shadow: 0 0 8px rgba(249,168,212,0.9) !important; }
        div[role="tablist"] > div[data-testid="stTab"]:nth-child(5) p { color: #FCD34D !important; -webkit-text-fill-color: #FCD34D !important; text-shadow: 0 0 8px rgba(252,211,77,0.9) !important; }
        div[role="tablist"] > div[data-testid="stTab"]:nth-child(6) p { color: #6EE7B7 !important; -webkit-text-fill-color: #6EE7B7 !important; text-shadow: 0 0 8px rgba(110,231,183,0.9) !important; }
        div[role="tablist"] > div[data-testid="stTab"]:nth-child(7) p { color: #FDBA74 !important; -webkit-text-fill-color: #FDBA74 !important; text-shadow: 0 0 8px rgba(253,186,116,0.9) !important; }
        div[role="tablist"] > div[data-testid="stTab"]:nth-child(8) p { color: #FCA5A5 !important; -webkit-text-fill-color: #FCA5A5 !important; text-shadow: 0 0 8px rgba(252,165,165,0.9) !important; }
        div[role="tablist"] > div[data-testid="stTab"]:nth-child(9) p { color: #A5B4FC !important; -webkit-text-fill-color: #A5B4FC !important; text-shadow: 0 0 8px rgba(165,180,252,0.9) !important; }

        /* Active / Selected Tab (Bright White text on Electric Cyan border) */
        div[data-testid="stTab"][role="tab"][aria-selected="true"],
        div[data-testid="stTab"][role="tab"][data-selected="true"] {
            background: linear-gradient(180deg, rgba(0, 242, 254, 0.35), rgba(15, 23, 42, 0.95)) !important;
            border: 1px solid #00F2FE !important;
            border-bottom: 3px solid #00F2FE !important;
            box-shadow: 0 0 18px rgba(0, 242, 254, 0.5) !important;
        }

        div[data-testid="stTab"][role="tab"][aria-selected="true"] p,
        div[data-testid="stTab"][role="tab"][data-selected="true"] p {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            text-shadow: 0 0 12px rgba(0, 242, 254, 1) !important;
        }

        /* Remove Excel-like Table Look */
        div[data-testid="stDataFrame"], div[data-testid="stTable"] {
            border: 1px solid rgba(0, 242, 254, 0.25) !important;
            border-radius: 12px !important;
            background: rgba(15, 23, 42, 0.8) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
            overflow: hidden !important;
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
