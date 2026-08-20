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
        /* =======================================================
           2. BULLETPROOF STREAMLIT TAB FIX (v1.4x+ compatible)
           ======================================================= */

        div[data-testid="stTabs"] div[role="tablist"] {
            gap: 6px !important;
            background: rgba(7,10,19,0.35) !important;
            padding: 6px 8px !important;
            border: 1px solid rgba(255,255,255,0.06) !important;
            border-radius: 12px !important;
        }

        div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
        div[data-testid="stTabs"] [data-testid="stTabHighlight"],
        div[data-testid="stTabs"] [data-baseweb="tab-border"] {
            display: none !important;
            opacity: 0 !important;
            height: 0 !important;
        }

        div[data-testid="stTabs"] [role="tab"],
        div[data-testid="stTabs"] button[data-testid="stTab"],
        div[data-testid="stTabs"] [data-testid="stTab"] {
            background: rgba(15, 23, 42, 0.96) !important;
            border: 1px solid rgba(148,163,184,0.28) !important;
            border-radius: 9px !important;
            padding: 10px 14px !important;
            margin: 0 !important;
            min-height: 42px !important;
            opacity: 1 !important;
            transition: all .2s ease !important;
        }

        div[data-testid="stTabs"] [role="tab"],
        div[data-testid="stTabs"] [role="tab"] *,
        div[data-testid="stTabs"] button[data-testid="stTab"],
        div[data-testid="stTabs"] button[data-testid="stTab"] *,
        div[data-testid="stTabs"] [data-testid="stTab"],
        div[data-testid="stTabs"] [data-testid="stTab"] * {
            color: #E5F3FF !important;
            -webkit-text-fill-color: #E5F3FF !important;
            fill: #E5F3FF !important;
            opacity: 1 !important;
            font-weight: 700 !important;
            font-size: 13px !important;
            text-shadow: 0 1px 8px rgba(56,189,248,.22) !important;
        }

        div[data-testid="stTabs"] [role="tab"]:hover,
        div[data-testid="stTabs"] button[data-testid="stTab"]:hover,
        div[data-testid="stTabs"] [data-testid="stTab"]:hover {
            background: rgba(30,41,59,1) !important;
            border-color: rgba(0,242,254,.65) !important;
            box-shadow: 0 0 16px rgba(0,242,254,.18) !important;
        }

        div[data-testid="stTabs"] [role="tab"][aria-selected="true"],
        div[data-testid="stTabs"] button[data-testid="stTab"][aria-selected="true"],
        div[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"] {
            background: linear-gradient(180deg, rgba(0,242,254,.22), rgba(15,23,42,.98)) !important;
            border-color: #22D3EE !important;
            box-shadow: inset 0 0 0 1px rgba(34,211,238,.18), 0 0 18px rgba(34,211,238,.22) !important;
        }

        div[data-testid="stTabs"] [role="tab"][aria-selected="true"],
        div[data-testid="stTabs"] [role="tab"][aria-selected="true"] *,
        div[data-testid="stTabs"] button[data-testid="stTab"][aria-selected="true"],
        div[data-testid="stTabs"] button[data-testid="stTab"][aria-selected="true"] *,
        div[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"],
        div[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"] * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            fill: #FFFFFF !important;
            text-shadow: 0 0 10px rgba(34,211,238,.55) !important;
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
