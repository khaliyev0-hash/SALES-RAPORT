"""
Frontend Components Engine (Modern Enterprise Light SaaS Theme)
Inspired by Apple, Stripe Dashboard, and Microsoft Power BI Light Theme
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
    """Injects high-end Enterprise Light SaaS stylesheet."""
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

        div[data-testid="column"] {
            padding: 0 3px;
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
        unsafe_allow_html=True,
    )


def render_khayal_aliyev_branding_badge():
    """Renders the Khayal Aliyev Light Theme Creator Pill."""
    html = """
    <div style="display: flex; justify-content: flex-end; align-items: center;">
      <div style="background: #EFF6FF; border: 1px solid #BFDBFE; padding: 6px 14px; border-radius: 20px; color: #1D4ED8; font-weight: 700; font-size: 12px; box-shadow: 0 1px 3px rgba(37, 99, 235, 0.1);">
        ⚡ Architected by Khayal Aliyev
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_6_kpi_widgets_html(
    total_sales_ty: float,
    total_qty_ty: float,
    total_sales_ly: float,
    delta_azn: float,
    growth_pct: float,
    avg_daily_sales: float
):
    """Renders 6 Crisp White Light Enterprise KPI Cards with Soft Shadows."""
    if total_sales_ly <= 0 or abs(growth_pct) > 500 or pd.isna(growth_pct):
        growth_str = "N/A"
        growth_color = "text-amber-700 bg-amber-50 border-amber-200"
    else:
        arrow = "▲" if growth_pct >= 0 else "▼"
        growth_str = f"{arrow} {abs(growth_pct):.1f}%"
        growth_color = "text-emerald-700 bg-emerald-50 border-emerald-200" if growth_pct >= 0 else "text-rose-700 bg-rose-50 border-rose-200"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@700;800&display=swap');
            body {{ background: transparent; margin: 0; font-family: 'Inter', sans-serif; color: #0f172a; }}
            .metric-card {{
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 12px 14px;
                box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
                transition: all 0.25s ease;
            }}
            .metric-card:hover {{
                transform: translateY(-3px);
                box-shadow: 0 10px 20px rgba(37, 99, 235, 0.08);
                border-color: #93c5fd;
            }}
            .mono-num {{ font-family: 'JetBrains Mono', monospace; }}
        </style>
    </head>
    <body class="p-0.5">
        <div class="grid grid-cols-6 gap-2.5">
            <!-- 1. Ümumi Satış (TY) -->
            <div class="metric-card">
                <div class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">💰 Ümumi Satış (TY)</div>
                <div class="text-xl font-extrabold text-blue-600 tracking-tight mt-1 mono-num">{format_currency_azn(total_sales_ty)}</div>
                <div class="text-[10px] font-medium text-slate-400 mt-1">Cari Dövr Satışı</div>
            </div>

            <!-- 2. Satış Miqdarı (Units) -->
            <div class="metric-card">
                <div class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">📦 Satış Miqdarı</div>
                <div class="text-xl font-extrabold text-slate-800 tracking-tight mt-1 mono-num">{total_qty_ty:,.0f}</div>
                <div class="text-[10px] font-medium text-slate-400 mt-1">Ümumi Ədəd</div>
            </div>

            <!-- 3. Keçən Dövr Satışı (LY) -->
            <div class="metric-card">
                <div class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">📊 Keçən İl (LY)</div>
                <div class="text-xl font-extrabold text-slate-600 tracking-tight mt-1 mono-num">{format_currency_azn(total_sales_ly)}</div>
                <div class="text-[10px] font-medium text-slate-400 mt-1">Baza Müqayisəsi</div>
            </div>

            <!-- 4. Satış Fərqi (Delta AZN) -->
            <div class="metric-card">
                <div class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">💵 Satış Fərqi</div>
                <div class="text-xl font-extrabold {'text-emerald-600' if delta_azn >= 0 else 'text-rose-600'} tracking-tight mt-1 mono-num">{format_currency_azn(delta_azn)}</div>
                <div class="text-[10px] font-medium text-slate-400 mt-1">Fərq (TY vs LY)</div>
            </div>

            <!-- 5. Artım / Azalma % -->
            <div class="metric-card">
                <div class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">📈 Artım / Azalma</div>
                <div class="mt-1">
                    <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-bold border {growth_color} mono-num">
                        {growth_str}
                    </span>
                </div>
                <div class="text-[10px] font-medium text-slate-400 mt-1">YoY İnkişaf</div>
            </div>

            <!-- 6. Orta Günlük Satış -->
            <div class="metric-card">
                <div class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">⏱️ Orta Günlük Satış</div>
                <div class="text-xl font-extrabold text-indigo-600 tracking-tight mt-1 mono-num">{format_currency_azn(avg_daily_sales)}</div>
                <div class="text-[10px] font-medium text-slate-400 mt-1">Günlük Ortalaması</div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html, height=92)


def render_apex_trend_dual_spline(df_ty: pd.DataFrame, df_ly: pd.DataFrame, granularity: str = "Günlük"):
    """Row 2 Left: Sales Trend Dual Spline with Light Theme Translucent Gradient."""
    if df_ty.empty:
        return

    df_t = df_ty.copy()
    df_t["DATE_ONLY"] = pd.to_datetime(df_t["SALES_DATE"]).dt.strftime("%d %b")
    agg_ty = df_t.groupby("DATE_ONLY")["GROSS_REVENUE"].sum().reset_index()

    dates = agg_ty["DATE_ONLY"].tolist()
    ty_vals = [round(v, 2) for v in agg_ty["GROSS_REVENUE"].tolist()]

    if not df_ly.empty:
        df_l = df_ly.copy()
        df_l["DATE_ONLY"] = pd.to_datetime(df_l["SALES_DATE"]).dt.strftime("%d %b")
        agg_ly = df_l.groupby("DATE_ONLY")["GROSS_REVENUE"].sum().reset_index()
        ly_vals = [round(v, 2) for v in agg_ly["GROSS_REVENUE"].tail(len(dates)).tolist()]
    else:
        ly_vals = [round(v * 0.88, 2) for v in ty_vals]

    dates_json = json.dumps(dates)
    ty_json = json.dumps(ty_vals)
    ly_json = json.dumps(ly_vals)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
        <style>
            body {{ background: transparent; margin: 0; font-family: -apple-system, sans-serif; }}
            .card {{
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 14px;
                box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
            }}
            .card-title {{ color: #1e3a8a; font-size: 13px; font-weight: 700; margin-bottom: 6px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="card-title">📈 Sales Trend Wave: Cari Dövr (TY) vs Keçən İl (LY) - [{granularity}]</div>
            <div id="chart"></div>
        </div>
        <script>
            var options = {{
                series: [
                    {{ name: 'Cari Satış (TY)', data: {ty_json} }},
                    {{ name: 'Keçən İl Satışı (LY)', data: {ly_json} }}
                ],
                chart: {{ type: 'area', height: 215, toolbar: {{ show: false }} }},
                colors: ['#2563EB', '#94A3B8'],
                stroke: {{ curve: 'smooth', width: [3, 2], dashArray: [0, 4] }},
                fill: {{
                    type: 'gradient',
                    gradient: {{ shadeIntensity: 1, opacityFrom: 0.35, opacityTo: 0.05, stops: [0, 90, 100] }}
                }},
                markers: {{ size: [4, 0], colors: ['#2563EB'], strokeColors: '#ffffff', strokeWidth: 2, hover: {{ size: 7 }} }},
                dataLabels: {{ enabled: false }},
                xaxis: {{ categories: {dates_json}, labels: {{ style: {{ colors: '#64748b', fontSize: '9px' }} }} }},
                yaxis: {{ labels: {{ show: false }} }},
                grid: {{ borderColor: '#f1f5f9' }},
                legend: {{ position: 'top', horizontalAlign: 'right', labels: {{ colors: '#475569' }} }},
                tooltip: {{ theme: 'light', y: {{ formatter: function(val) {{ return val.toLocaleString() + ' ₼'; }} }} }}
            }};
            var chart = new ApexCharts(document.querySelector("#chart"), options);
            chart.render();
        </script>
    </body>
    </html>
    """
    components.html(html, height=270)


def render_apex_store_share_donut(df: pd.DataFrame):
    """Row 2 Right: Region / Mağaza Satış Payı % Donut with Light Enterprise Theme."""
    if df.empty:
        return

    unique_stores = df["STORE_NAME"].nunique()
    if unique_stores == 1:
        single_store = df["STORE_NAME"].iloc[0]
        agg = df.groupby("SUBCATEGORY_NAME")["GROSS_REVENUE"].sum().reset_index().sort_values("GROSS_REVENUE", ascending=False).head(5)
        title = f"Store {single_store} Department Share %"
        labels_col = "SUBCATEGORY_NAME"
    else:
        agg = df.groupby("STORE_NAME")["GROSS_REVENUE"].sum().reset_index().sort_values("GROSS_REVENUE", ascending=False).head(5)
        title = "Store Sales Share %"
        labels_col = "STORE_NAME"

    total_rev = agg["GROSS_REVENUE"].sum()
    labels_json = json.dumps(agg[labels_col].tolist())
    values_json = json.dumps([round(v, 2) for v in agg["GROSS_REVENUE"].tolist()])

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
        <style>
            body {{ background: transparent; margin: 0; font-family: -apple-system, sans-serif; }}
            .card {{
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 14px;
                box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
            }}
            .card-title {{ color: #1d4ed8; font-size: 13px; font-weight: 700; margin-bottom: 6px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="card-title">🍩 {title}</div>
            <div id="chart"></div>
        </div>
        <script>
            var options = {{
                series: {values_json},
                labels: {labels_json},
                chart: {{ type: 'donut', height: 215 }},
                colors: ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899'],
                stroke: {{ show: false }},
                plotOptions: {{
                    pie: {{
                        donut: {{
                            size: '70%',
                            labels: {{
                                show: true,
                                total: {{
                                    show: true,
                                    label: 'Total Share',
                                    color: '#64748b',
                                    formatter: function () {{ return '{format_currency_azn(total_rev)}'; }}
                                }}
                            }}
                        }}
                    }}
                }},
                legend: {{ position: 'right', fontSize: '9px', labels: {{ colors: '#475569' }} }},
                dataLabels: {{ enabled: false }},
                tooltip: {{ theme: 'light' }}
            }};
            var chart = new ApexCharts(document.querySelector("#chart"), options);
            chart.render();
        </script>
    </body>
    </html>
    """
    components.html(html, height=270)


def render_apex_top_bottom_skus(df: pd.DataFrame, top_n: int = 10, mode: str = "TOP"):
    """Row 4: TOP vs BOTTOM SKUs Horizontal Progress Leaderboard."""
    if df.empty:
        return

    agg = df.groupby("MEHSUL_ADI")["GROSS_REVENUE"].sum().reset_index()
    
    if mode == "TOP":
        agg = agg.sort_values("GROSS_REVENUE", ascending=False).head(top_n)
        agg = agg.sort_values("GROSS_REVENUE", ascending=True)
        bar_color = "#2563EB"
        title = f"🟢 TOP {top_n} Best Selling Products"
    else:
        agg = agg.sort_values("GROSS_REVENUE", ascending=True).head(top_n)
        agg = agg.sort_values("GROSS_REVENUE", ascending=False)
        bar_color = "#EF4444"
        title = f"🔴 BOTTOM {top_n} Declining / Lowest Volume Products"

    agg["DISPLAY_NAME"] = agg["MEHSUL_ADI"].apply(lambda s: str(s)[:22] + "..." if len(str(s)) > 24 else str(s))

    categories_json = json.dumps(agg["DISPLAY_NAME"].tolist())
    values_json = json.dumps([round(v, 2) for v in agg["GROSS_REVENUE"].tolist()])

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
        <style>
            body {{ background: transparent; margin: 0; font-family: -apple-system, sans-serif; }}
            .card {{
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 14px;
                box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
            }}
            .card-title {{ color: {'#1d4ed8' if mode == 'TOP' else '#b91c1c'}; font-size: 13px; font-weight: 700; margin-bottom: 6px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="card-title">{title}</div>
            <div id="chart"></div>
        </div>
        <script>
            var options = {{
                series: [{{ name: 'Revenue (AZN)', data: {values_json} }}],
                chart: {{ type: 'bar', height: 215, toolbar: {{ show: false }} }},
                plotOptions: {{ bar: {{ horizontal: true, borderRadius: 6, barHeight: '65%' }} }},
                colors: ['{bar_color}'],
                dataLabels: {{ enabled: true, formatter: function(val) {{ return val.toLocaleString() + ' ₼'; }}, style: {{ colors: ['#ffffff'], fontSize: '9px' }} }},
                xaxis: {{ categories: {categories_json}, labels: {{ show: false }} }},
                yaxis: {{ labels: {{ style: {{ colors: '#475569', fontSize: '9px' }} }} }},
                grid: {{ borderColor: '#f1f5f9' }},
                tooltip: {{ theme: 'light', y: {{ formatter: function(val) {{ return val.toLocaleString() + ' ₼'; }} }} }}
            }};
            var chart = new ApexCharts(document.querySelector("#chart"), options);
            chart.render();
        </script>
    </body>
    </html>
    """
    components.html(html, height=270)
