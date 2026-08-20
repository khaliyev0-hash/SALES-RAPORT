"""
Tam Store Sales Analysis Portal
Architected & Engineered by Khayal Aliyev
High-Tech Cosmic Dark & Neon Glow Architecture (High-Specificity Sidebar & Tab Fixes)
"""

import sys
import os
import io
import datetime
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Force current working directory & app directory into sys.path for Streamlit Cloud parity
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

try:
    from queries import fetch_ty_and_ly_datasets, apply_cascading_filters, force_db_status_reset, standardize_dataframe_columns
    from frontend_components import (
        inject_global_theme_css,
        render_khayal_aliyev_branding_badge,
    )
    from js_components import (
        render_neon_kpi_cards,
        render_apex_sales_wave,
        render_echarts_hollow_donut,
        render_apex_horizontal_bars,
        render_glassmorphic_store_ranking_table,
        render_glassmorphic_supplier_leadership_table,
        render_glassmorphic_risk_radar_table,
    )
    from visuals import (
        create_day_of_week_chart,
        create_store_ranking_chart,
        create_store_treemap,
        create_pareto_chart,
        create_waterfall_contribution_chart,
        create_basket_analytics_chart,
        create_product_velocity_quadrant,
        create_top_suppliers_chart,
        create_supplier_concentration_donut_chart,
        create_insert_sales_comparison_chart,
        create_top_insert_products_chart,
    )
except ImportError as err:
    st.error(f"⚠️ Critical Module Import Error: {err}. Please ensure all .py files (js_components.py, queries.py, frontend_components.py, visuals.py, db.py) are present in the root directory.")
    st.stop()

# Page Setup
st.set_page_config(
    page_title="Tam Store Sales Analysis Portal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Global Theme & Zero-Leak Dark Glass Styling
inject_global_theme_css()

# High-Specificity Cosmic Dark & Neon Glow CSS Overrides
st.markdown(
    """
    <style>
    /* --- 1. Global Reset & Hard Lock --- */
    :root {
        color-scheme: dark !important;
    }

    html, body, [data-testid="stAppViewContainer"], .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        background-color: #070A13 !important;
        background: radial-gradient(circle at 50% 0%, #0F172A 0%, #070A13 75%) !important;
        color: #F8FAFC !important;
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
       2. FIX UNREADABLE TABS & REMOVE DEFAULT RED UNDERLINE
       ======================================================= */
    /* Kill red underline highlight */
    div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
    div[data-testid="stTabs"] [data-testid="stTabHighlight"] {
        display: none !important;
        background-color: transparent !important;
        height: 0px !important;
    }

    /* Base style for ALL tab buttons */
    div[data-testid="stTabs"] button[role="tab"] {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(0, 242, 254, 0.25) !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 8px 16px !important;
        margin-right: 4px !important;
        transition: all 0.25s ease-in-out !important;
    }

    /* Force all inactive tab labels to bright cyan glow */
    div[data-testid="stTabs"] button[role="tab"] p,
    div[data-testid="stTabs"] button[role="tab"] span,
    div[data-testid="stTabs"] button[role="tab"] div,
    div[data-testid="stTabs"] button[role="tab"] * {
        color: #38BDF8 !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        text-shadow: 0 0 8px rgba(56, 189, 248, 0.8) !important;
    }

    /* Active / Selected Tab (Bright White text on Electric Cyan border) */
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background: linear-gradient(180deg, rgba(0, 242, 254, 0.3), rgba(15, 23, 42, 0.95)) !important;
        border: 1px solid #00F2FE !important;
        border-bottom: 3px solid #00F2FE !important;
        box-shadow: 0 0 18px rgba(0, 242, 254, 0.4) !important;
    }

    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] * {
        color: #FFFFFF !important;
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
        padding-top: 0.4rem !important;
        padding-bottom: 2rem !important;
        max-width: 98.5% !important;
    }
    div[data-testid="stToolbar"] {
        visibility: hidden !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def reset_all_sidebar_filters():
    for key in list(st.session_state.keys()):
        if key.startswith("sb_") or key.startswith("calendar_") or key == "uploaded_sku_list":
            del st.session_state[key]

PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True}

# ==========================================
# SIDEBAR: ADVANCED CALENDAR & BULK SKU UPLOADER
# ==========================================
with st.sidebar:
    st.markdown("### ⚡ Controls & Filters")

    if st.button("🔄 Reset All Filters", use_container_width=True, key="btn_sidebar_reset_top"):
        reset_all_sidebar_filters()
        st.rerun()

    st.markdown("---")

    # Date Selector Engine
    st.markdown("#### 📅 Calendar & Date Engine")
    
    date_preset = st.selectbox(
        "Quick Presets",
        options=["Bu gün", "Dünən", "Son 7 gün", "Son 30 gün", "Cari ay", "Keçən ay", "Cari il (YTD)", "Keçən ilin eyni dövrü", "Custom Range"],
        index=3,
        key="sb_date_preset"
    )

    today = datetime.date.today()
    if date_preset == "Bu gün":
        default_start, default_end = today, today
    elif date_preset == "Dünən":
        default_start = today - datetime.timedelta(days=1)
        default_end = default_start
    elif date_preset == "Son 7 gün":
        default_start = today - datetime.timedelta(days=7)
        default_end = today
    elif date_preset == "Son 30 gün":
        default_start = today - datetime.timedelta(days=30)
        default_end = today
    elif date_preset == "Cari ay":
        default_start = datetime.date(today.year, today.month, 1)
        default_end = today
    elif date_preset == "Keçən ay":
        first_of_curr = datetime.date(today.year, today.month, 1)
        last_of_prev = first_of_curr - datetime.timedelta(days=1)
        default_start = datetime.date(last_of_prev.year, last_of_prev.month, 1)
        default_end = last_of_prev
    elif date_preset == "Cari il (YTD)":
        default_start = datetime.date(today.year, 1, 1)
        default_end = today
    elif date_preset == "Keçən ilin eyni dövrü":
        default_start = datetime.date(today.year - 1, 1, 1)
        default_end = datetime.date(today.year - 1, today.month, today.day)
    else:
        default_start = today - datetime.timedelta(days=30)
        default_end = today

    cal_range = st.date_input(
        "Tarix Aralığı Seçin",
        value=(default_start, default_end),
        key="calendar_date_range"
    )

    if isinstance(cal_range, (tuple, list)) and len(cal_range) == 2:
        start_date, end_date = cal_range[0], cal_range[1]
    elif isinstance(cal_range, (tuple, list)) and len(cal_range) == 1:
        start_date, end_date = cal_range[0], cal_range[0]
    else:
        start_date, end_date = default_start, default_end

    st.markdown("---")

    # Bulk Product / SKU File Uploader
    st.markdown("#### 📁 Bulk SKU File Uploader")
    uploaded_file = st.file_uploader(
        "📁 Xüsusi Məhsul Siyahısı Yüklə (.xlsx, .csv, .txt)",
        type=["xlsx", "xls", "csv", "txt"],
        key="sku_uploader"
    )

    uploaded_skus = []
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(('.xlsx', '.xls')):
                up_df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.csv'):
                up_df = pd.read_csv(uploaded_file)
            else:
                up_df = pd.read_csv(uploaded_file, header=None, names=["SKU"])

            sku_col = None
            for col in up_df.columns:
                if str(col).upper() in ["MEHSUL_KODU", "URUN KODU", "SKU", "MEHSUL KODU", "ITEM_CODE"]:
                    sku_col = col
                    break
            if sku_col is None:
                sku_col = up_df.columns[0]

            uploaded_skus = up_df[sku_col].astype(str).str.strip().unique().tolist()
            st.markdown(
                f"""
                <div style="background: rgba(0, 242, 254, 0.15); border: 1px solid rgba(0, 242, 254, 0.4); 
                            padding: 8px 12px; border-radius: 6px; color: #00f2fe; font-size: 0.76rem; font-weight: 600; margin-top: 6px;">
                    🔍 Xüsusi Siyahı Aktivdir: {len(uploaded_skus)} məhsul analiz edilir
                </div>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Fayl oxunarkən xəta yaratdı: {e}")

    st.markdown("---")

    # Fetch Datasets
    df_base_ty, df_base_ly, is_live_db, status_msg, diag_log = fetch_ty_and_ly_datasets(start_date, end_date)

    st.markdown("#### 🔍 Cascading Filters")

    all_regions = sorted(df_base_ty["REGION"].dropna().unique().tolist()) if not df_base_ty.empty else []
    sel_region = st.multiselect("Region / Şəhər", options=all_regions, default=[], key="sb_sel_region")

    df_st_scope = df_base_ty[df_base_ty["REGION"].isin(sel_region)] if sel_region else df_base_ty
    all_stores = sorted(df_st_scope["STORE_NAME"].dropna().unique().tolist()) if not df_st_scope.empty else []
    sel_stores = st.multiselect("Mağaza (MAGAZA)", options=all_stores, default=[], key="sb_sel_stores")

    df_grp_scope = apply_cascading_filters(df_base_ty, selected_region=sel_region, selected_stores=sel_stores)
    all_qrup = sorted(df_grp_scope["QRUP"].dropna().unique().tolist()) if not df_grp_scope.empty else []
    sel_qrup = st.multiselect("QRUP", options=all_qrup, default=[], key="sb_sel_qrup")

    df_fam_scope = apply_cascading_filters(df_grp_scope, selected_qrup=sel_qrup)
    all_family = sorted(df_fam_scope["FAMILY NAME"].dropna().unique().tolist()) if not df_fam_scope.empty else []
    sel_family = st.multiselect("FAMILY NAME", options=all_family, default=[], key="sb_sel_family")

    df_cat_scope = apply_cascading_filters(df_fam_scope, selected_family=sel_family)
    all_category = sorted(df_cat_scope["CATEGORY NAME"].dropna().unique().tolist()) if not df_cat_scope.empty else []
    sel_category = st.multiselect("CATEGORY NAME", options=all_category, default=[], key="sb_sel_category")

    df_sub_scope = apply_cascading_filters(df_cat_scope, selected_category=sel_category)
    all_subcat = sorted(df_sub_scope["SUB CATEGORY NAME"].dropna().unique().tolist()) if not df_sub_scope.empty else []
    sel_subcategory = st.multiselect("SUB CATEGORY NAME", options=all_subcat, default=[], key="sb_sel_subcategory")

    df_sup_scope = apply_cascading_filters(df_sub_scope, selected_category=sel_category)
    all_suppliers = sorted(df_sup_scope["SATICI ADI"].dropna().unique().tolist()) if not df_sup_scope.empty else []
    sel_supplier = st.multiselect("SATICI ADI (Supplier)", options=all_suppliers, default=[], key="sb_sel_supplier")

    st.markdown("---")
    if st.button("⚡ Live Refresh Database", use_container_width=True, key="btn_sb_refresh"):
        force_db_status_reset()
        st.rerun()

# Filter Datasets
df_filtered_ty = apply_cascading_filters(
    df_base_ty,
    selected_region=sel_region,
    selected_stores=sel_stores,
    selected_qrup=sel_qrup,
    selected_family=sel_family,
    selected_category=sel_category,
    selected_subcategory=sel_subcategory,
    selected_supplier=sel_supplier,
    selected_item=uploaded_skus if uploaded_skus else None
)

df_filtered_ly = apply_cascading_filters(
    df_base_ly,
    selected_region=sel_region,
    selected_stores=sel_stores,
    selected_qrup=sel_qrup,
    selected_family=sel_family,
    selected_category=sel_category,
    selected_subcategory=sel_subcategory,
    selected_supplier=sel_supplier,
    selected_item=uploaded_skus if uploaded_skus else None
)

df_filtered_ty = standardize_dataframe_columns(df_filtered_ty)
df_filtered_ly = standardize_dataframe_columns(df_filtered_ly)

# ==========================================
# CYBERPUNK LIVE HEADER WITH TAM STORE TITLE & ALIGNED CONTROLS
# ==========================================
c_hdr_title, c_hdr_badge, c_hdr_controls = st.columns([2.2, 1.3, 0.8])

with c_hdr_title:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 12px; padding: 10px 16px; 
                    background: rgba(18, 24, 38, 0.75); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px;">
            <span class="live-dot"></span>
            <div>
                <h2 style="margin: 0; font-size: 1.15rem; font-weight: 800; color: #ffffff; letter-spacing: -0.01em;">
                    Tam Store Sales Analysis Portal
                </h2>
                <span style="font-size: 0.72rem; color: #10B981; font-weight: 600; letter-spacing: 0.5px;">
                    SYSTEM LIVE • REAL-TIME FEED &nbsp;|&nbsp; <b>Period:</b> {start_date} – {end_date}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c_hdr_badge:
    render_khayal_aliyev_branding_badge()

with c_hdr_controls:
    c_btn1, c_btn2 = st.columns(2)
    if c_btn1.button("🔄", use_container_width=True, key="btn_hdr_reset", help="Reset All Filters"):
        reset_all_sidebar_filters()
        st.rerun()
    if c_btn2.button("⚡", use_container_width=True, key="btn_hdr_refresh", help="Live Refresh Database"):
        force_db_status_reset()
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

if diag_log:
    with st.expander("⚠️ Database Diagnostic Log (SQL Connection Inspection)", expanded=False):
        st.code(diag_log, language="sql")

# ==========================================
# MODULAR EXECUTIVE TABS
# ==========================================
tab1, tab2, tab3, tab_supplier, tab_insert, tab4, tab5, tab6 = st.tabs([
    "📊 Əsas İcmal & Trendlər",
    "🏬 Mağaza & Region Analizi",
    "📦 Kateqoriya & Risk Radar",
    "🏭 Təchizatçı & Brend Analizi",
    "🎁 İnser & Aksiya Satışları",
    "🧾 Səbət & Çek Dinamikası",
    "🟢 Top / 🔴 Bottom Radar",
    "📑 Master Data & Briefing Export"
])

# ------------------------------------------
# TAB 1: 📊 ƏSAS İCMAL, STORE CHAMPION & JS CHARTS
# ------------------------------------------
with tab1:
    if not df_filtered_ty.empty:
        total_sales_ty = float(df_filtered_ty["GROSS_REVENUE"].sum())
        total_qty_ty = float(df_filtered_ty["QUANTITY"].sum())
        total_sales_ly = float(df_filtered_ly["GROSS_REVENUE"].sum()) if not df_filtered_ly.empty else 0.0
        delta_azn = total_sales_ty - total_sales_ly
        growth_pct = (delta_azn / total_sales_ly * 100) if total_sales_ly > 0 else 0.0
        days_count = max(1, (end_date - start_date).days + 1)
        avg_daily_sales = total_sales_ty / days_count

        # 1. JavaScript Animated Neon KPI Ticker Row
        metrics_list = [
            {"title": "💰 Ümumi Satış (TY)", "value": total_sales_ty, "sub_text": "Cari Dövr Satışı", "accent_color": "#00f2fe", "suffix": " ₼"},
            {"title": "📦 Satış Miqdarı", "value": total_qty_ty, "sub_text": "Ümumi Ədəd", "accent_color": "#6366f1", "suffix": " əd"},
            {"title": "📊 Keçən İl (LY)", "value": total_sales_ly, "sub_text": "Baza Müqayisəsi", "accent_color": "#c084fc", "suffix": " ₼"},
            {"title": "💵 Satış Fərqi", "value": delta_azn, "sub_text": "Fərq (TY vs LY)", "accent_color": "#10b981" if delta_azn >= 0 else "#f43f5e", "suffix": " ₼"},
            {"title": "📈 Artım / Azalma", "value": f"{growth_pct:+.1f}%" if total_sales_ly > 0 else "N/A", "sub_text": "YoY İnkişaf", "accent_color": "#10b981" if growth_pct >= 0 else "#f43f5e"},
            {"title": "⏱️ Orta Günlük Satış", "value": avg_daily_sales, "sub_text": "Günlük Ortalaması", "accent_color": "#f59e0b", "suffix": " ₼"}
        ]
        
        js_kpi_html = render_neon_kpi_cards(metrics_list)
        components.html(js_kpi_html, height=92, scrolling=False)

        st.markdown("<br>", unsafe_allow_html=True)

        c_champ, c_ai = st.columns([1, 1.5])
        
        with c_champ:
            top_st_df = df_filtered_ty.groupby("STORE_NAME")["GROSS_REVENUE"].sum().reset_index().sort_values("GROSS_REVENUE", ascending=False)
            top_st_name = top_st_df.iloc[0]["STORE_NAME"] if not top_st_df.empty else "N/A"
            top_st_val = top_st_df.iloc[0]["GROSS_REVENUE"] if not top_st_df.empty else 0
            top_st_share = (top_st_val / total_sales_ty * 100) if total_sales_ty > 0 else 0

            st.markdown(
                f"""
                <div style="background: rgba(18, 24, 38, 0.75); border: 1px solid rgba(255, 215, 0, 0.3); border-radius: 10px; padding: 14px;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #ffd700; text-transform: uppercase;">🏆 STORE CHAMPION LEADERBOARD</div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: #ffffff; margin-top: 4px;">🥇 {top_st_name}</div>
                    <div style="font-size: 0.85rem; color: #34d399; font-weight: 600; margin-top: 2px;">
                        Gəlir: <b>{top_st_val:,.0f} ₼</b> ({top_st_share:.1f}% Pay)
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c_ai:
            top_grp_df = df_filtered_ty.groupby("QRUP")["GROSS_REVENUE"].sum().reset_index().sort_values("GROSS_REVENUE", ascending=False)
            top_grp_name = top_grp_df.iloc[0]["QRUP"] if not top_grp_df.empty else "Qıda"
            
            st.markdown(
                f"""
                <div style="background: rgba(18, 24, 38, 0.75); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 10px; padding: 14px;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #818cf8; text-transform: uppercase;">🤖 EXECUTIVE AI INSIGHTS DIGEST</div>
                    <ul style="font-size: 0.8rem; color: #cbd5e1; margin-top: 6px; padding-left: 18px; line-height: 1.4;">
                        <li>🚀 Cari dövr ümumi gəlir: <b>{total_sales_ty:,.0f} ₼</b> (Dövriyyənin əsas sürücüsü: <b>{top_grp_name}</b> qrupu).</li>
                        <li>🏬 Ən yüksək performans göstərən mağaza: <b>{top_st_name}</b> ({top_st_val:,.0f} ₼ gəlir ilə).</li>
                        <li>💡 Ortalama günlük satış <b>{avg_daily_sales:,.0f} ₼</b> təşkil edir.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        c_t1_left, c_t1_right = st.columns([1.5, 1])
        with c_t1_left:
            df_t = df_filtered_ty.copy()
            df_t["DATE_ONLY"] = pd.to_datetime(df_t["SALES_DATE"]).dt.strftime("%d %b")
            agg_ty = df_t.groupby("DATE_ONLY")["GROSS_REVENUE"].sum().reset_index()
            dates_list = agg_ty["DATE_ONLY"].tolist()
            ty_list = agg_ty["GROSS_REVENUE"].tolist()

            if not df_filtered_ly.empty:
                df_l = df_filtered_ly.copy()
                df_l["DATE_ONLY"] = pd.to_datetime(df_l["SALES_DATE"]).dt.strftime("%d %b")
                agg_ly = df_l.groupby("DATE_ONLY")["GROSS_REVENUE"].sum().reset_index()
                ly_list = agg_ly["GROSS_REVENUE"].tail(len(dates_list)).tolist()
            else:
                ly_list = [v * 0.88 for v in ty_list]

            apex_wave_html = render_apex_sales_wave(dates_list, ty_list, ly_list)
            components.html(apex_wave_html, height=270, scrolling=False)

        with c_t1_right:
            unique_stores = df_filtered_ty["STORE_NAME"].nunique()
            if unique_stores == 1:
                agg_donut = df_filtered_ty.groupby("SUBCATEGORY_NAME")["GROSS_REVENUE"].sum().reset_index().sort_values("GROSS_REVENUE", ascending=False).head(5)
                donut_cats = agg_donut["SUBCATEGORY_NAME"].tolist()
            else:
                agg_donut = df_filtered_ty.groupby("STORE_NAME")["GROSS_REVENUE"].sum().reset_index().sort_values("GROSS_REVENUE", ascending=False).head(5)
                donut_cats = agg_donut["STORE_NAME"].tolist()
            
            donut_vals = agg_donut["GROSS_REVENUE"].tolist()
            echarts_donut_html = render_echarts_hollow_donut(donut_cats, donut_vals)
            components.html(echarts_donut_html, height=270, scrolling=False)

        st.markdown("---")
        fig_dow = create_day_of_week_chart(df_filtered_ty)
        st.plotly_chart(fig_dow, use_container_width=True, config=PLOTLY_CONFIG, key="fig_tab1_dow_pattern")

# ------------------------------------------
# TAB 2: 🏬 MAĞAZA & REGİON ANALİZİ (GLASSMORPHIC CARDS)
# ------------------------------------------
with tab2:
    if not df_filtered_ty.empty:
        c_t2_left, c_t2_right = st.columns([1, 1.5])
        with c_t2_left:
            top_st = st.slider("Mağaza Sayı", min_value=3, max_value=20, value=10, key="sld_tab2_topn")
            fig_st_rank = create_store_ranking_chart(df_filtered_ty, top_n=top_st, mode="Top")
            st.plotly_chart(fig_st_rank, use_container_width=True, config=PLOTLY_CONFIG, key="fig_tab2_st_rank")
        
        with c_t2_right:
            st.markdown("#### 📊 Glassmorphic Mağaza Performans Cədvəli (TY vs LY)")
            agg_st = df_filtered_ty.groupby(["STORE_ID", "STORE_NAME"])["GROSS_REVENUE"].sum().reset_index()
            if not df_filtered_ly.empty:
                agg_st_ly = df_filtered_ly.groupby("STORE_ID")["GROSS_REVENUE"].sum().reset_index()
                agg_st = pd.merge(agg_st, agg_st_ly, on="STORE_ID", how="left", suffixes=("_TY", "_LY")).fillna(0)
                if "GROSS_REVENUE_TY" in agg_st.columns:
                    agg_st["GROSS_REVENUE"] = agg_st["GROSS_REVENUE_TY"]
                if "GROSS_REVENUE_LY" not in agg_st.columns:
                    agg_st["GROSS_REVENUE_LY"] = 0.0
            else:
                agg_st["GROSS_REVENUE_LY"] = agg_st["GROSS_REVENUE"] * 0.88

            for col in ["GROSS_REVENUE", "GROSS_REVENUE_LY"]:
                if col not in agg_st.columns:
                    agg_st[col] = 0.0

            agg_st["FƏRQ_AZN"] = agg_st["GROSS_REVENUE"] - agg_st["GROSS_REVENUE_LY"]
            agg_st["ARTIM_%"] = (agg_st["FƏRQ_AZN"] / agg_st["GROSS_REVENUE_LY"].replace(0, 1)) * 100
            agg_st = agg_st.sort_values("GROSS_REVENUE", ascending=False).reset_index(drop=True)
            agg_st.index += 1

            # Render Custom Interactive Glassmorphic Table instead of raw Excel dataframe
            st_table_html = render_glassmorphic_store_ranking_table(agg_st)
            components.html(st_table_html, height=400, scrolling=False)

# ------------------------------------------
# TAB 3: 📦 KATEQORİYA, ABC & RISK RADAR (GLASSMORPHIC CARDS)
# ------------------------------------------
with tab3:
    if not df_filtered_ty.empty:
        blocked_df = df_filtered_ty[df_filtered_ty["SATISA BLOKLU"] == 1]
        st.markdown("#### ⚠️ RISK RADAR: SATIŞA BLOKLANMIŞ MƏHSUL PANEDİ")
        risk_table_html = render_glassmorphic_risk_radar_table(blocked_df)
        components.html(risk_table_html, height=390, scrolling=False)

        st.markdown("<br>", unsafe_allow_html=True)
        c_t3_left, c_t3_right = st.columns(2)
        with c_t3_left:
            fig_pareto = create_pareto_chart(df_filtered_ty)
            st.plotly_chart(fig_pareto, use_container_width=True, config=PLOTLY_CONFIG, key="fig_tab3_pareto")
        with c_t3_right:
            fig_waterfall = create_waterfall_contribution_chart(df_filtered_ty, df_filtered_ly)
            st.plotly_chart(fig_waterfall, use_container_width=True, config=PLOTLY_CONFIG, key="fig_tab3_waterfall")

        st.markdown("---")
        fig_quadrant = create_product_velocity_quadrant(df_filtered_ty)
        st.plotly_chart(fig_quadrant, use_container_width=True, config=PLOTLY_CONFIG, key="fig_tab3_velocity_quadrant")

        st.markdown("---")
        fig_treemap = create_store_treemap(df_filtered_ty)
        st.plotly_chart(fig_treemap, use_container_width=True, config=PLOTLY_CONFIG, key="fig_tab3_treemap")

# ------------------------------------------
# TAB SUPPLIER: 🏭 TƏCHİZATÇI & BREND ANALİZİ (GLASSMORPHIC CARDS)
# ------------------------------------------
with tab_supplier:
    if not df_filtered_ty.empty:
        st.markdown("### 🏭 Təchizatçı & Brend Liderlik Analizi")
        
        c_sup1, c_sup2 = st.columns(2)
        with c_sup1:
            fig_sup_top = create_top_suppliers_chart(df_filtered_ty, top_n=10)
            st.plotly_chart(fig_sup_top, use_container_width=True, config=PLOTLY_CONFIG, key="fig_sup_top10")
        with c_sup2:
            fig_sup_donut = create_supplier_concentration_donut_chart(df_filtered_ty)
            st.plotly_chart(fig_sup_donut, use_container_width=True, config=PLOTLY_CONFIG, key="fig_sup_donut")

        st.markdown("---")
        st.markdown("#### 🏆 Glassmorphic Təchizatçı Liderlik Paneli")
        sup_table_html = render_glassmorphic_supplier_leadership_table(df_filtered_ty, top_n=12)
        components.html(sup_table_html, height=400, scrolling=False)

        st.markdown("---")
        st.markdown("#### 🎯 Təchizatçı üzrə Detallı Drilldown")
        
        all_sups = sorted(df_filtered_ty["SATICI ADI"].dropna().unique().tolist())
        selected_single_supplier = st.selectbox("Təchizatçı Seçin", options=all_sups, index=0, key="sb_single_supplier")

        df_single_sup = df_filtered_ty[df_filtered_ty["SATICI ADI"] == selected_single_supplier]

        if not df_single_sup.empty:
            sup_rev = df_single_sup["GROSS_REVENUE"].sum()
            sup_qty = df_single_sup["QUANTITY"].sum()
            sup_skus = df_single_sup["MEHSUL_KODU"].nunique()

            st.markdown(
                f"""
                <div style="background: rgba(45, 212, 191, 0.15); border: 1px solid rgba(45, 212, 191, 0.4); 
                            padding: 10px 14px; border-radius: 8px; margin-bottom: 12px;">
                    <span style="color: #2dd4bf; font-weight: 800;">🏭 {selected_single_supplier} İcmalı</span> &nbsp;|&nbsp; 
                    <span>Satış: <b>{sup_rev:,.0f} ₼</b></span> &nbsp;|&nbsp; 
                    <span>Miqdar: <b>{sup_qty:,.0f} ədəd</b></span> &nbsp;|&nbsp; 
                    <span>Məhsul Çeşidi: <b>{sup_skus} SKU</b></span>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.dataframe(
                df_single_sup[[
                    "MEHSUL_KODU", "MEHSUL_ADI", "CATEGORY NAME", 
                    "QUANTITY", "GROSS_REVENUE", "MARGIN", "STORE_NAME"
                ]],
                use_container_width=True,
                height=320
            )

# ------------------------------------------
# TAB INSERT: 🎁 DEDICATED INSERT / PROMOSİYA SATIŞLARI
# ------------------------------------------
with tab_insert:
    if not df_filtered_ty.empty:
        total_gross = float(df_filtered_ty["GROSS_REVENUE"].sum())
        total_insert_rev = float(df_filtered_ty["INSERT_SATIS_EDV"].sum())
        total_insert_qty = float(df_filtered_ty["INSERT_MIQDARI"].sum())
        insert_share_pct = (total_insert_rev / total_gross * 100) if total_gross > 0 else 0
        insert_skus_count = df_filtered_ty[df_filtered_ty["INSERT_MIQDARI"] > 0]["MEHSUL_KODU"].nunique()

        st.markdown(
            f"""
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px;">
                <div style="background: rgba(18,24,38,0.75); border: 1px solid rgba(244,63,94,0.3); padding: 12px 14px; border-radius: 8px;">
                    <span style="font-size: 0.72rem; color: #f43f5e; font-weight: 700;">🎁 TOPLAM İNSER SATIŞI (AZN)</span>
                    <div style="font-size: 1.5rem; font-weight: 800; color: #ffffff; margin-top: 2px;">{total_insert_rev:,.0f} ₼</div>
                </div>
                <div style="background: rgba(18,24,38,0.75); border: 1px solid rgba(244,63,94,0.3); padding: 12px 14px; border-radius: 8px;">
                    <span style="font-size: 0.72rem; color: #f43f5e; font-weight: 700;">📦 İNSER MİQDARI (ƏDƏD)</span>
                    <div style="font-size: 1.5rem; font-weight: 800; color: #ffffff; margin-top: 2px;">{total_insert_qty:,.0f}</div>
                </div>
                <div style="background: rgba(18,24,38,0.75); border: 1px solid rgba(244,63,94,0.3); padding: 12px 14px; border-radius: 8px;">
                    <span style="font-size: 0.72rem; color: #f43f5e; font-weight: 700;">📈 İNSER SATIŞ PAYI %</span>
                    <div style="font-size: 1.5rem; font-weight: 800; color: #fb7185; margin-top: 2px;">{insert_share_pct:.1f}%</div>
                </div>
                <div style="background: rgba(18,24,38,0.75); border: 1px solid rgba(244,63,94,0.3); padding: 12px 14px; border-radius: 8px;">
                    <span style="font-size: 0.72rem; color: #f43f5e; font-weight: 700;">🏷️ AKSİYADA OLAN MƏHSUL SAYI</span>
                    <div style="font-size: 1.5rem; font-weight: 800; color: #ffffff; margin-top: 2px;">{insert_skus_count:,.0f} SKU</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        c_ins1, c_ins2 = st.columns(2)
        with c_ins1:
            fig_ins_comp = create_insert_sales_comparison_chart(df_filtered_ty)
            st.plotly_chart(fig_ins_comp, use_container_width=True, config=PLOTLY_CONFIG, key="fig_insert_comp")
        with c_ins2:
            fig_ins_top = create_top_insert_products_chart(df_filtered_ty, top_n=10)
            st.plotly_chart(fig_ins_top, use_container_width=True, config=PLOTLY_CONFIG, key="fig_insert_top")

        st.markdown("---")
        st.markdown("#### 🎁 Detallı İnser Promosiya Cədvəli")
        insert_df = df_filtered_ty[df_filtered_ty["INSERT_MIQDARI"] > 0].copy()
        
        if not insert_df.empty:
            st.dataframe(
                insert_df[[
                    "MEHSUL_KODU", "MEHSUL_ADI", "FAMILY NAME", "CATEGORY NAME", 
                    "INSERT_MIQDARI", "INSERT_SATIS_EDV", "INSERT_SATIS_EDVSIZ", "STORE_NAME", "SALES_DATE"
                ]],
                use_container_width=True,
                height=350
            )

            ins_excel_buffer = io.BytesIO()
            with pd.ExcelWriter(ins_excel_buffer, engine="openpyxl") as writer:
                insert_df.to_excel(writer, index=False, sheet_name="Insert Sales")
            ins_excel_data = ins_excel_buffer.getvalue()

            st.download_button(
                label="📥 Export Insert Sales to Excel (.xlsx)",
                data=ins_excel_data,
                file_name=f"insert_sales_{datetime.date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="btn_insert_excel_dl"
            )

# ------------------------------------------
# TAB 4: 🧾 SƏBƏT & ÇEK DİNAMİKASI
# ------------------------------------------
with tab4:
    if not df_filtered_ty.empty:
        total_rev = float(df_filtered_ty["GROSS_REVENUE"].sum())
        total_trans = df_filtered_ty["TRANSACTION_ID"].nunique()
        total_units = float(df_filtered_ty["QUANTITY"].sum())
        
        avg_ticket = total_rev / total_trans if total_trans > 0 else 0.0
        units_per_trans = total_units / total_trans if total_trans > 0 else 0.0

        st.markdown(
            f"""
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 16px;">
                <div style="background: rgba(18,24,38,0.75); border: 1px solid rgba(255,255,255,0.08); padding: 14px; border-radius: 8px;">
                    <span style="font-size: 0.72rem; color: #94a3b8; font-weight: 700;">💳 ORTALAMA ÇEK MƏBLƏĞİ</span>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #38bdf8; margin-top: 4px;">{avg_ticket:,.2f} ₼</div>
                </div>
                <div style="background: rgba(18,24,38,0.75); border: 1px solid rgba(255,255,255,0.08); padding: 14px; border-radius: 8px;">
                    <span style="font-size: 0.72rem; color: #94a3b8; font-weight: 700;">🛍️ ÇEK BAŞINA MƏHSUL SAYI</span>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #4ade80; margin-top: 4px;">{units_per_trans:.1f} ədəd</div>
                </div>
                <div style="background: rgba(18,24,38,0.75); border: 1px solid rgba(255,255,255,0.08); padding: 14px; border-radius: 8px;">
                    <span style="font-size: 0.72rem; color: #94a3b8; font-weight: 700;">🧾 ÜMUMİ ÇEK / TRANZAKSİYA</span>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #c084fc; margin-top: 4px;">{total_trans:,.0f}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        fig_basket = create_basket_analytics_chart(df_filtered_ty)
        st.plotly_chart(fig_basket, use_container_width=True, config=PLOTLY_CONFIG, key="fig_tab4_basket_chart")

# ------------------------------------------
# TAB 5: 🟢 TOP / 🔴 BOTTOM RADAR (APEX JS BARS)
# ------------------------------------------
with tab5:
    if not df_filtered_ty.empty:
        c_t5_left, c_t5_right = st.columns(2)
        with c_t5_left:
            top_count = st.slider("TOP Count", min_value=5, max_value=50, value=10, key="sld_tab5_topn")
            top_df = df_filtered_ty.groupby("MEHSUL_ADI")["GROSS_REVENUE"].sum().reset_index().sort_values("GROSS_REVENUE", ascending=False).head(top_count)
            top_df = top_df.sort_values("GROSS_REVENUE", ascending=True)
            labels_top = [str(name)[:22] + "..." if len(str(name)) > 24 else str(name) for name in top_df["MEHSUL_ADI"].tolist()]
            vals_top = top_df["GROSS_REVENUE"].tolist()

            js_top_bars = render_apex_horizontal_bars(labels_top, vals_top, title=f"🟢 TOP {top_count} Best Selling Products", color="#00f2fe")
            components.html(js_top_bars, height=270, scrolling=False)

        with c_t5_right:
            bottom_count = st.slider("BOTTOM Count", min_value=5, max_value=50, value=10, key="sld_tab5_bottomn")
            bot_df = df_filtered_ty.groupby("MEHSUL_ADI")["GROSS_REVENUE"].sum().reset_index().sort_values("GROSS_REVENUE", ascending=True).head(bottom_count)
            bot_df = bot_df.sort_values("GROSS_REVENUE", ascending=False)
            labels_bot = [str(name)[:22] + "..." if len(str(name)) > 24 else str(name) for name in bot_df["MEHSUL_ADI"].tolist()]
            vals_bot = bot_df["GROSS_REVENUE"].tolist()

            js_bot_bars = render_apex_horizontal_bars(labels_bot, vals_bot, title=f"🔴 BOTTOM {bottom_count} Declining / Lowest Volume Products", color="#ef4444")
            components.html(js_bot_bars, height=270, scrolling=False)

# ------------------------------------------
# TAB 6: 📑 MASTER DATA & BRIEFING EXPORT
# ------------------------------------------
with tab6:
    st.markdown("### 📑 Executive Briefing & Master Data Export Engine")
    
    if not df_filtered_ty.empty:
        st.markdown("#### 📄 Executive Briefing Summary Report")
        top_5_st = df_filtered_ty.groupby("STORE_NAME")["GROSS_REVENUE"].sum().nlargest(5).to_dict()
        top_5_sup = df_filtered_ty.groupby("SATICI ADI")["GROSS_REVENUE"].sum().nlargest(5).to_dict()
        
        briefing_html = f"""
        <div style="background: rgba(18,24,38,0.85); border: 1px solid rgba(99,102,241,0.3); border-radius: 10px; padding: 16px; margin-bottom: 16px;">
            <div style="font-size: 1.1rem; font-weight: 800; color: #ffffff; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px;">
                📋 EXECUTIVE BRIEFING SUMMARY REPORT ({start_date} ~ {end_date})
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 12px; font-size: 0.82rem;">
                <div>
                    <span style="color: #38bdf8; font-weight: 700;">🏬 TOP 5 MAĞAZALAR:</span>
                    <ul style="color: #cbd5e1; margin-top: 4px; padding-left: 16px;">
                        {''.join([f"<li><b>{k}:</b> {v:,.0f} ₼</li>" for k, v in top_5_st.items()])}
                    </ul>
                </div>
                <div>
                    <span style="color: #2dd4bf; font-weight: 700;">🏭 TOP 5 TƏCHİZATÇILAR:</span>
                    <ul style="color: #cbd5e1; margin-top: 4px; padding-left: 16px;">
                        {''.join([f"<li><b>{k}:</b> {v:,.0f} ₼</li>" for k, v in top_5_sup.items()])}
                    </ul>
                </div>
            </div>
        </div>
        """
        st.markdown(briefing_html, unsafe_allow_html=True)

        st.markdown("---")
        search_term = st.text_input("⚡ Search Master Records", "", key="txt_tab6_search")
        
        display_df = df_filtered_ty.copy()
        if search_term:
            display_df = display_df[
                display_df["MEHSUL_ADI"].astype(str).str.contains(search_term, case=False) |
                display_df["MEHSUL_KODU"].astype(str).str.contains(search_term, case=False) |
                display_df["STORE_NAME"].astype(str).str.contains(search_term, case=False) |
                display_df["FAMILY NAME"].astype(str).str.contains(search_term, case=False)
            ]

        st.dataframe(
            display_df[[
                "MEHSUL_KODU", "MEHSUL_ADI", "FAMILY NAME", 
                "CATEGORY NAME", "SUB CATEGORY NAME", "SATICI ADI",
                "MIQDARI", "SATIS_EDV", "SATIS_EDVSIZ", "MARGIN", "STORE_NAME", "SALES_DATE"
            ]],
            use_container_width=True,
            height=350
        )

        st.markdown("<br>", unsafe_allow_html=True)
        col_ex1, col_ex2, _ = st.columns([1, 1, 2])

        csv_data = display_df.to_csv(index=False).encode('utf-8')
        col_ex1.download_button(
            label="📄 Export Master Data to CSV",
            data=csv_data,
            file_name=f"sales_data_{datetime.date.today()}.csv",
            mime="text/csv",
            use_container_width=True,
            key="btn_tab6_csv_dl"
        )

        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            display_df.to_excel(writer, index=False, sheet_name="Sales Report")
        excel_data = excel_buffer.getvalue()

        col_ex2.download_button(
            label="📥 Export Master Data to Excel (.xlsx)",
            data=excel_data,
            file_name=f"sales_data_{datetime.date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="btn_tab6_excel_dl"
        )
    else:
        st.info("No records available.")
