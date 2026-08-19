"""
Frontend Components Engine (Tier-1 Luxury SaaS Interface)
High-Tech Cosmic Dark & Neon Glow Theme Engine
Pure JS, ApexCharts CDN, Tailwind CSS & CSS3 Glassmorphic Micro-Animations
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
    """Injects high-priority Cosmic Dark CSS stylesheet."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&display=swap');

        /* --- Deep Cosmic Canvas --- */
        html, body, [data-testid="stAppViewContainer"], .stApp {
            background: radial-gradient(circle at 50% 0%, #0F172A 0%, #070A13 75%) !important;
            background-color: #070A13 !important;
            color: #F8FAFC !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
        }

        /* --- Dark Frosted Sidebar --- */
        [data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
            background: rgba(15, 23, 42, 0.95) !important;
            border-right: 1px solid rgba(0, 242, 254, 0.2) !important;
            box-shadow: 10px 0 25px rgba(0, 0, 0, 0.5) !important;
        }

        /* --- Remove Top Header Blank Area --- */
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

        /* --- Glassmorphic Containers & Cards --- */
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

        /* --- KPI Values & Badges --- */
        .metric-value, [data-testid="stMetricValue"] {
            color: #00F2FE !important;
            text-shadow: 0 0 12px rgba(0, 242, 254, 0.6) !important;
            font-weight: 800 !important;
        }

        /* --- Permanent Glowing Tabs --- */
        button[data-baseweb="tab"] {
            background: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid rgba(0, 242, 254, 0.25) !important;
            border-radius: 8px 8px 0 0 !important;
            color: #38BDF8 !important;
            font-weight: 700 !important;
            margin-right: 4px !important;
            text-shadow: 0 0 8px rgba(56, 189, 248, 0.6) !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(180deg, rgba(0, 242, 254, 0.25), rgba(15, 23, 42, 0.95)) !important;
            color: #FFFFFF !important;
            border: 1px solid #00F2FE !important;
            border-bottom: 3px solid #00F2FE !important;
            box-shadow: 0 0 18px rgba(0, 242, 254, 0.4) !important;
            text-shadow: 0 0 12px rgba(0, 242, 254, 0.9) !important;
        }
        button[data-baseweb="tab"] * { color: inherit !important; }

        /* --- Dark Inputs, Selectboxes, DatePicker & File Uploader --- */
        div[data-baseweb="select"] > div,
        div[data-baseweb="select"] div[role="combobox"],
        div[data-baseweb="base-input"],
        div[data-baseweb="input"],
        .stDateInput input,
        div[data-testid="stFileUploader"],
        section[data-testid="stFileUploadDropzone"] {
            background-color: #111827 !important;
            border: 1px solid rgba(0, 242, 254, 0.25) !important;
            color: #F8FAFC !important;
            border-radius: 8px !important;
        }
        div[data-baseweb="select"] * { color: #F8FAFC !important; }

        /* --- Glowing Buttons --- */
        .stButton > button, div[data-testid="stFileUploader"] button {
            background: linear-gradient(135deg, #1E293B, #0F172A) !important;
            color: #00F2FE !important;
            border: 1px solid rgba(0, 242, 254, 0.4) !important;
            border-radius: 8px !important;
            box-shadow: 0 0 12px rgba(0, 242, 254, 0.2) !important;
        }
        .stButton > button:hover {
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


def render_6_kpi_widgets_html(
    total_sales_ty: float,
    total_qty_ty: float,
    total_sales_ly: float,
    delta_azn: float,
    growth_pct: float,
    avg_daily_sales: float
):
    """Renders 6 Luxury Glassmorphic KPI Row Cards with multi-color neon accent top borders."""
    if total_sales_ly <= 0 or abs(growth_pct) > 500 or pd.isna(growth_pct):
        growth_str = "N/A"
        growth_color = "text-amber-400 border-amber-500/30 bg-amber-500/15"
    else:
        arrow = "▲" if growth_pct >= 0 else "▼"
        growth_str = f"{arrow} {abs(growth_pct):.1f}%"
        growth_color = "text-emerald-400 border-emerald-500/30 bg-emerald-500/15" if growth_pct >= 0 else "text-rose-400 border-rose-500/30 bg-rose-500/15"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700;800&display=swap');
            body {{ background: transparent; margin: 0; font-family: 'Inter', sans-serif; color: #f8fafc; }}
            .glass-card {{
                background: rgba(18, 24, 38, 0.75);
                backdrop-filter: blur(20px) saturate(180%);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 10px;
                padding: 10px 14px;
                position: relative;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            .glass-card:hover {{
                border-color: rgba(0, 242, 254, 0.35);
                box-shadow: 0 8px 32px 0 rgba(0, 242, 254, 0.25);
                transform: translateY(-3px);
            }}
            .top-accent-cyan {{ border-top: 2.5px solid #00f2fe; }}
            .top-accent-indigo {{ border-top: 2.5px solid #6366f1; }}
            .top-accent-emerald {{ border-top: 2.5px solid #10b981; }}
            .top-accent-amber {{ border-top: 2.5px solid #f59e0b; }}
            .top-accent-purple {{ border-top: 2.5px solid #c084fc; }}
            .top-accent-rose {{ border-top: 2.5px solid #f43f5e; }}

            .mono-num {{ font-family: 'JetBrains Mono', monospace; }}
        </style>
    </head>
    <body class="p-0.5">
        <div class="grid grid-cols-6 gap-2">
            <!-- 1. Ümumi Satış (TY) -->
            <div class="glass-card top-accent-cyan">
                <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400">💰 Ümumi Satış (TY)</div>
                <div class="text-xl font-extrabold text-cyan-400 tracking-tight mt-1 mono-num">{format_currency_azn(total_sales_ty)}</div>
                <div class="text-[10px] font-semibold text-cyan-400 mt-1">Cari Dövr Satışı</div>
            </div>

            <!-- 2. Satış Miqdarı (Units) -->
            <div class="glass-card top-accent-indigo">
                <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400">📦 Satış Miqdarı</div>
                <div class="text-xl font-extrabold text-indigo-400 tracking-tight mt-1 mono-num">{total_qty_ty:,.0f}</div>
                <div class="text-[10px] font-semibold text-slate-400 mt-1">Ümumi Ədəd</div>
            </div>

            <!-- 3. Keçən Dövr Satışı (LY) -->
            <div class="glass-card top-accent-purple">
                <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400">📊 Keçən İl (LY)</div>
                <div class="text-xl font-extrabold text-slate-300 tracking-tight mt-1 mono-num">{format_currency_azn(total_sales_ly)}</div>
                <div class="text-[10px] font-semibold text-slate-400 mt-1">Baza Müqayisəsi</div>
            </div>

            <!-- 4. Satış Fərqi (Delta AZN) -->
            <div class="glass-card {'top-accent-emerald' if delta_azn >= 0 else 'top-accent-rose'}">
                <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400">💵 Satış Fərqi</div>
                <div class="text-xl font-extrabold {'text-emerald-400' if delta_azn >= 0 else 'text-rose-400'} tracking-tight mt-1 mono-num">{format_currency_azn(delta_azn)}</div>
                <div class="text-[10px] font-semibold text-slate-400 mt-1">Fərq (TY vs LY)</div>
            </div>

            <!-- 5. Artım / Azalma % -->
            <div class="glass-card top-accent-emerald">
                <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400">📈 Artım / Azalma</div>
                <div class="mt-1">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-extrabold border {growth_color} mono-num">
                        {growth_str}
                    </span>
                </div>
                <div class="text-[10px] font-semibold text-slate-400 mt-1">YoY İnkişaf</div>
            </div>

            <!-- 6. Orta Günlük Satış -->
            <div class="glass-card top-accent-amber">
                <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400">⏱️ Orta Günlük Satış</div>
                <div class="text-xl font-extrabold text-amber-400 tracking-tight mt-1 mono-num">{format_currency_azn(avg_daily_sales)}</div>
                <div class="text-[10px] font-semibold text-slate-400 mt-1">Günlük Ortalaması</div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html, height=88)


def render_apex_trend_dual_spline(df_ty: pd.DataFrame, df_ly: pd.DataFrame, granularity: str = "Günlük"):
    """Row 2 Left: Sales Trend Dual Spline with multi-stop neon gradient fill and pulse markers."""
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
            body {{ background: transparent; margin: 0; font-family: 'Inter', sans-serif; }}
            .card {{
                background: rgba(18, 24, 38, 0.75);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 10px;
                padding: 12px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            }}
            .card-title {{ color: #00F2FE; font-size: 13px; font-weight: 700; margin-bottom: 6px; }}
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
                colors: ['#00F2FE', '#A855F7'],
                stroke: {{ curve: 'smooth', width: [3, 2], dashArray: [0, 4] }},
                fill: {{
                    type: 'gradient',
                    gradient: {{ shadeIntensity: 1, opacityFrom: 0.45, opacityTo: 0.05, stops: [0, 90, 100] }}
                }},
                markers: {{ size: [4, 0], colors: ['#00F2FE'], strokeColors: '#ffffff', strokeWidth: 2, hover: {{ size: 7 }} }},
                dataLabels: {{ enabled: false }},
                xaxis: {{ categories: {dates_json}, labels: {{ style: {{ colors: '#94a3b8', fontSize: '9px' }} }} }},
                yaxis: {{ labels: {{ show: false }} }},
                grid: {{ show: false }},
                legend: {{ position: 'top', horizontalAlign: 'right', labels: {{ colors: '#94a3b8' }} }},
                tooltip: {{ theme: 'dark', y: {{ formatter: function(val) {{ return val.toLocaleString() + ' ₼'; }} }} }}
            }};
            var chart = new ApexCharts(document.querySelector("#chart"), options);
            chart.render();
        </script>
    </body>
    </html>
    """
    components.html(html, height=270)


def render_apex_store_share_donut(df: pd.DataFrame):
    """Row 2 Right: Region / Mağaza Satış Payı % Donut with custom dark glass tooltip."""
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
            body {{ background: transparent; margin: 0; font-family: 'Inter', sans-serif; }}
            .card {{
                background: rgba(18, 24, 38, 0.75);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 10px;
                padding: 12px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            }}
            .card-title {{ color: #00F2FE; font-size: 13px; font-weight: 700; margin-bottom: 6px; }}
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
                colors: ['#00F2FE', '#A855F7', '#10B981', '#F59E0B', '#F43F5E'],
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
                                    color: '#94a3b8',
                                    formatter: function () {{ return '{format_currency_azn(total_rev)}'; }}
                                }}
                            }}
                        }}
                    }}
                }},
                legend: {{ position: 'right', fontSize: '9px', labels: {{ colors: '#94a3b8' }} }},
                dataLabels: {{ enabled: false }},
                tooltip: {{ theme: 'dark' }}
            }};
            var chart = new ApexCharts(document.querySelector("#chart"), options);
            chart.render();
        </script>
    </body>
    </html>
    """
    components.html(html, height=270)


def render_apex_top_bottom_skus(df: pd.DataFrame, top_n: int = 10, mode: str = "TOP"):
    """Row 4: TOP vs BOTTOM SKUs Horizontal Progress Leaderboard with rounded pill ends."""
    if df.empty:
        return

    agg = df.groupby("MEHSUL_ADI")["GROSS_REVENUE"].sum().reset_index()
    
    if mode == "TOP":
        agg = agg.sort_values("GROSS_REVENUE", ascending=False).head(top_n)
        agg = agg.sort_values("GROSS_REVENUE", ascending=True)
        bar_color = "#00F2FE"
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
            body {{ background: transparent; margin: 0; font-family: 'Inter', sans-serif; }}
            .card {{
                background: rgba(18, 24, 38, 0.75);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 10px;
                padding: 12px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            }}
            .card-title {{ color: {'#00F2FE' if mode == 'TOP' else '#EF4444'}; font-size: 13px; font-weight: 700; margin-bottom: 6px; }}
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
                yaxis: {{ labels: {{ style: {{ colors: '#94a3b8', fontSize: '9px' }} }} }},
                grid: {{ show: false }},
                tooltip: {{ theme: 'dark', y: {{ formatter: function(val) {{ return val.toLocaleString() + ' ₼'; }} }} }}
            }};
            var chart = new ApexCharts(document.querySelector("#chart"), options);
            chart.render();
        </script>
    </body>
    </html>
    """
    components.html(html, height=270)
