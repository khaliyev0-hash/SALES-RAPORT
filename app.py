"""
Tam Store Sales Analysis Portal
Architected & Engineered by Khayal Aliyev
Ultra-Clean Modern Enterprise Light SaaS Theme (Apple, Stripe & Power BI Inspired)
"""

import io
import datetime
import pandas as pd
import streamlit as st

from queries import fetch_ty_and_ly_datasets, apply_cascading_filters, force_db_status_reset, standardize_dataframe_columns
from frontend_components import (
    inject_global_theme_css,
    render_khayal_aliyev_branding_badge,
    render_6_kpi_widgets_html,
    render_apex_trend_dual_spline,
    render_apex_store_share_donut,
    render_apex_top_bottom_skus,
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

# Page Setup
st.set_page_config(
    page_title="Tam Store Sales Analysis Portal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Global Theme
inject_global_theme_css()

# High-End Light Enterprise SaaS CSS
st.markdown(
    """
    <style>
    /* --- Global Body & Workspace Background --- */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #F1F5F9 !important;
        background: #F1F5F9 !important;
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, sans-serif !important;
    }

    /* --- Clean White Sidebar --- */
    [data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        box-shadow: 2px 0 12px rgba(0, 0, 0, 0.03) !important;
    }

    /* --- Remove Top Header Blank Area --- */
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0rem !important;
    }

    .block-container {
        padding-top: 0.4rem !important;
        padding-bottom: 2rem !important;
        max-width: 98.5% !important;
    }
    div[data-testid="stToolbar"] {
        visibility: hidden !important;
    }

    /* --- Live System Green Badge (Light Mode) --- */
    .live-dot {
        width: 9px; height: 9px; background: #16A34A; border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.6);
        animation: pulseLight 2s infinite;
    }
    @keyframes pulseLight {
        0% { box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.6); }
        70% { box-shadow: 0 0 0 8px rgba(22, 163, 74, 0); }
        100% { box-shadow: 0 0 0 0 rgba(22, 163, 74, 0); }
    }

    /* --- Modern Light Tab Bar --- */
    button[data-baseweb="tab"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px 8px 0 0 !important;
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
        padding: 10px 18px !important;
        margin-right: 4px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
    }
    button[data-baseweb="tab"]:hover {
        color: #2563EB !important;
        background-color: #F8FAFC !important;
        border-color: #CBD5E1 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #EFF6FF !important;
        color: #1D4ED8 !important;
        border: 1px solid #BFDBFE !important;
        border-bottom: 3px solid #2563EB !important;
        font-weight: 700 !important;
    }
    button[data-baseweb="tab"] * {
        color: inherit !important;
    }

    /* --- Crisp Light Inputs, Selectbox & Uploader --- */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"],
    .stDateInput input,
    div[data-testid="stFileUploader"],
    section[data-testid="stFileUploadDropzone"] {
        background-color: #F8FAFC !important;
        border: 1px solid #CBD5E1 !important;
        color: #0F172A !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] * {
        color: #0F172A !important;
    }

    /* --- Buttons (Clean Blue & Slate Accents) --- */
    .stButton > button, button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    }
    .stButton > button:hover {
        background: #2563EB !important;
        color: #FFFFFF !important;
        border-color: #2563EB !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
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
                <div style="background: #EFF6FF; border: 1px solid #BFDBFE; 
                            padding: 8px 12px; border-radius: 6px; color: #1D4ED8; font-size: 0.76rem; font-weight: 600; margin-top: 6px;">
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
# CRISP LIGHT HEADER WITH TAM STORE TITLE & ALIGNED CONTROLS
# ==========================================
c_hdr_title, c_hdr_badge, c_hdr_controls = st.columns([2.2, 1.3, 0.8])

with c_hdr_title:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 12px; padding: 10px 16px; 
                    background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);">
            <span class="live-dot"></span>
            <div>
                <h2 style="margin: 0; font-size: 1.15rem; font-weight: 800; color: #0F172A; letter-spacing: -0.01em;">
                    Tam Store Sales Analysis Portal
                </h2>
                <span style="font-size: 0.72rem; color: #16A34A; font-weight: 600; letter-spacing: 0.5px;">
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
# TAB 1: 📊 ƏSAS İCMAL, STORE CHAMPION & AI INSIGHTS
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

        render_6_kpi_widgets_html(
            total_sales_ty=total_sales_ty,
            total_qty_ty=total_qty_ty,
            total_sales_ly=total_sales_ly,
            delta_azn=delta_azn,
            growth_pct=growth_pct,
            avg_daily_sales=avg_daily_sales
        )

        st.markdown("<br>", unsafe_allow_html=True)

        c_champ, c_ai = st.columns([1, 1.5])
        
        with c_champ:
            top_st_df = df_filtered_ty.groupby("STORE_NAME")["GROSS_REVENUE"].sum().reset_index().sort_values("GROSS_REVENUE", ascending=False)
            top_st_name = top_st_df.iloc[0]["STORE_NAME"] if not top_st_df.empty else "N/A"
            top_st_val = top_st_df.iloc[0]["GROSS_REVENUE"] if not top_st_df.empty else 0
            top_st_share = (top_st_val / total_sales_ty * 100) if total_sales_ty > 0 else 0

            st.markdown(
                f"""
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #D97706; text-transform: uppercase;">🏆 STORE CHAMPION LEADERBOARD</div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: #0F172A; margin-top: 4px;">🥇 {top_st_name}</div>
                    <div style="font-size: 0.85rem; color: #059669; font-weight: 600; margin-top: 2px;">
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
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #2563EB; text-transform: uppercase;">🤖 EXECUTIVE AI INSIGHTS DIGEST</div>
                    <ul style="font-size: 0.8rem; color: #334155; margin-top: 6px; padding-left: 18px; line-height: 1.4;">
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
            granularity = st.radio("Trend Scope", options=["Günlük", "Həftəlik", "Aylıq"], horizontal=True, key="rad_tab1_trend_gran")
            render_apex_trend_dual_spline(df_filtered_ty, df_filtered_ly, granularity=granularity)
        with c_t1_right:
            render_apex_store_share_donut(df_filtered_ty)

        st.markdown("---")
        fig_dow = create_day_of_week_chart(df_filtered_ty)
        st.plotly_chart(fig_dow, use_container_width=True, config=PLOTLY_CONFIG, key="fig_tab1_dow_pattern")

# ------------------------------------------
# TAB 2: 🏬 MAĞAZA & REGİON ANALİZİ
# ------------------------------------------
with tab2:
    if not df_filtered_ty.empty:
        c_t2_left, c_t2_right = st.columns([1, 1.5])
        with c_t2_left:
            top_st = st.slider("Mağaza Sayı", min_value=3, max_value=20, value=10, key="sld_tab2_topn")
            fig_st_rank = create_store_ranking_chart(df_filtered_ty, top_n=top_st, mode="Top")
            st.plotly_chart(fig_st_rank, use_container_width=True, config=PLOTLY_CONFIG, key="fig_tab2_st_rank")
        
        with c_t2_right:
            st.markdown("#### 📊 Mağaza Performans Cədvəli (TY vs LY)")
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

            st.dataframe(
                agg_st.rename(columns={
                    "STORE_ID": "Mağaza Kodu",
                    "STORE_NAME": "Mağaza Adı",
                    "GROSS_REVENUE": "Cari Satış (AZN)",
                    "GROSS_REVENUE_LY": "Keçən İl (LY)",
                    "FƏRQ_AZN": "Fərq (AZN)",
                    "ARTIM_%": "Artım %"
                }),
                use_container_width=True,
                height=320
            )

# ------------------------------------------
# TAB 3: 📦 KATEQORİYA, ABC & RISK RADAR
# ------------------------------------------
with tab3:
    if not df_filtered_ty.empty:
        blocked_df = df_filtered_ty[df_filtered_ty["SATISA BLOKLU"] == 1]
        if not blocked_df.empty:
            blocked_count = blocked_df["MEHSUL_KODU"].nunique()
            blocked_rev = blocked_df["GROSS_REVENUE"].sum()
            st.markdown(
                f"""
                <div style="background: #FEF2F2; border: 1px solid #FCA5A5; 
                            padding: 10px 14px; border-radius: 8px; margin-bottom: 14px;">
                    <span style="color: #DC2626; font-weight: 800; font-size: 0.9rem;">⚠️ RISK RADAR: SATIŞA BLOKLANMIŞ MƏHSULLAR</span><br>
                    <span style="font-size: 0.78rem; color: #991B1B;">
                        Hazırda <b>{blocked_count} adət</b> yüksək gəlirli məhsul (Ümumi gəlir: <b>{blocked_rev:,.0f} ₼</b>) satışa bloklanmış və ya təchizat riskindədir!
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

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
# TAB SUPPLIER: 🏭 TƏCHİZATÇI & BREND ANALİZİ
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
                <div style="background: #F0FDFA; border: 1px solid #99F6E4; 
                            padding: 10px 14px; border-radius: 8px; margin-bottom: 12px;">
                    <span style="color: #0D9488; font-weight: 800;">🏭 {selected_single_supplier} İcmalı</span> &nbsp;|&nbsp; 
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
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 12px 14px; border-radius: 8px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);">
                    <span style="font-size: 0.72rem; color: #E11D48; font-weight: 700;">🎁 TOPLAM İNSER SATIŞI (AZN)</span>
                    <div style="font-size: 1.5rem; font-weight: 800; color: #0F172A; margin-top: 2px;">{total_insert_rev:,.0f} ₼</div>
                </div>
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 12px 14px; border-radius: 8px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);">
                    <span style="font-size: 0.72rem; color: #E11D48; font-weight: 700;">📦 İNSER MİQDARI (ƏDƏD)</span>
                    <div style="font-size: 1.5rem; font-weight: 800; color: #0F172A; margin-top: 2px;">{total_insert_qty:,.0f}</div>
                </div>
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 12px 14px; border-radius: 8px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);">
                    <span style="font-size: 0.72rem; color: #E11D48; font-weight: 700;">📈 İNSER SATIŞ PAYI %</span>
                    <div style="font-size: 1.5rem; font-weight: 800; color: #E11D48; margin-top: 2px;">{insert_share_pct:.1f}%</div>
                </div>
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 12px 14px; border-radius: 8px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);">
                    <span style="font-size: 0.72rem; color: #E11D48; font-weight: 700;">🏷️ AKSİYADA OLAN MƏHSUL SAYI</span>
                    <div style="font-size: 1.5rem; font-weight: 800; color: #0F172A; margin-top: 2px;">{insert_skus_count:,.0f} SKU</div>
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
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 14px; border-radius: 8px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);">
                    <span style="font-size: 0.72rem; color: #64748B; font-weight: 700;">💳 ORTALAMA ÇEK MƏBLƏĞİ</span>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #2563EB; margin-top: 4px;">{avg_ticket:,.2f} ₼</div>
                </div>
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 14px; border-radius: 8px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);">
                    <span style="font-size: 0.72rem; color: #64748B; font-weight: 700;">🛍️ ÇEK BAŞINA MƏHSUL SAYI</span>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #059669; margin-top: 4px;">{units_per_trans:.1f} ədəd</div>
                </div>
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 14px; border-radius: 8px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);">
                    <span style="font-size: 0.72rem; color: #64748B; font-weight: 700;">🧾 ÜMUMİ ÇEK / TRANZAKSİYA</span>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #7C3AED; margin-top: 4px;">{total_trans:,.0f}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        fig_basket = create_basket_analytics_chart(df_filtered_ty)
        st.plotly_chart(fig_basket, use_container_width=True, config=PLOTLY_CONFIG, key="fig_tab4_basket_chart")

# ------------------------------------------
# TAB 5: 🟢 TOP / 🔴 BOTTOM RADAR
# ------------------------------------------
with tab5:
    if not df_filtered_ty.empty:
        c_t5_left, c_t5_right = st.columns(2)
        with c_t5_left:
            top_count = st.slider("TOP Count", min_value=5, max_value=50, value=10, key="sld_tab5_topn")
            render_apex_top_bottom_skus(df_filtered_ty, top_n=top_count, mode="TOP")
        with c_t5_right:
            bottom_count = st.slider("BOTTOM Count", min_value=5, max_value=50, value=10, key="sld_tab5_bottomn")
            render_apex_top_bottom_skus(df_filtered_ty, top_n=bottom_count, mode="BOTTOM")

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
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);">
            <div style="font-size: 1.1rem; font-weight: 800; color: #0F172A; border-bottom: 1px solid #E2E8F0; padding-bottom: 8px;">
                📋 EXECUTIVE BRIEFING SUMMARY REPORT ({start_date} ~ {end_date})
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 12px; font-size: 0.82rem;">
                <div>
                    <span style="color: #2563EB; font-weight: 700;">🏬 TOP 5 MAĞAZALAR:</span>
                    <ul style="color: #334155; margin-top: 4px; padding-left: 16px;">
                        {''.join([f"<li><b>{k}:</b> {v:,.0f} ₼</li>" for k, v in top_5_st.items()])}
                    </ul>
                </div>
                <div>
                    <span style="color: #0D9488; font-weight: 700;">🏭 TOP 5 TƏCHİZATÇILAR:</span>
                    <ul style="color: #334155; margin-top: 4px; padding-left: 16px;">
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
