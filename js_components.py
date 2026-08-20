"""
Pure JavaScript (ApexCharts JS & Apache ECharts & Custom Glassmorphic Cards) Component Engine
High-Tech Cosmic Dark & Neon Glow Architecture (Excel-Killer SaaS Table Engine)
"""

import json
import pandas as pd


def format_currency_azn(val: float) -> str:
    """Formats numbers to AZN currency (e.g. 624,771 ₼, 1.25M ₼)."""
    if abs(val) >= 1_000_000:
        return f"{val / 1_000_000:.2f}M ₼"
    elif abs(val) >= 1_000:
        return f"{val / 1_000:.1f}K ₼"
    else:
        return f"{val:,.2f} ₼"


def render_neon_kpi_cards(metrics_data: list) -> str:
    """
    Renders 6 glassmorphic glowing KPI cards with JavaScript animated count-up number tickers.
    metrics_data format: list of dicts with keys ['title', 'value', 'sub_text', 'accent_color', 'prefix', 'suffix']
    """
    cards_html = ""
    for idx, m in enumerate(metrics_data):
        title = m.get("title", "")
        raw_value = m.get("value", 0)
        sub_text = m.get("sub_text", "")
        accent = m.get("accent_color", "#00f2fe")
        prefix = m.get("prefix", "")
        suffix = m.get("suffix", "")
        
        is_num = isinstance(raw_value, (int, float)) and not pd.isna(raw_value)
        val_display = f"{raw_value:,.2f}" if is_num else str(raw_value)

        cards_html += f"""
        <div class="kpi-card" style="border-top: 2.5px solid {accent};">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value-row" style="color: {accent}; text-shadow: 0 0 10px {accent}80;">
                <span class="prefix">{prefix}</span>
                <span class="ticker-num" data-target="{raw_value if is_num else 0}" data-is-num="{1 if is_num else 0}">{val_display if not is_num else 0}</span>
                <span class="suffix">{suffix}</span>
            </div>
            <div class="kpi-sub">{sub_text}</div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700;800&family=Inter:wght@600;700&display=swap');
            body {{ background: transparent; margin: 0; padding: 2px; font-family: 'Inter', sans-serif; color: #f8fafc; }}
            
            .kpi-container {{
                display: grid;
                grid-template-columns: repeat(6, 1fr);
                gap: 8px;
            }}
            .kpi-card {{
                background: rgba(15, 23, 42, 0.75);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 10px 12px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
                transition: all 0.3s ease;
            }}
            .kpi-card:hover {{
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(0, 242, 254, 0.25);
            }}
            .kpi-title {{
                font-size: 10px;
                font-weight: 700;
                color: #94a3b8;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            .kpi-value-row {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 18px;
                font-weight: 800;
                margin-top: 4px;
                line-height: 1.2;
            }}
            .kpi-sub {{
                font-size: 9px;
                font-weight: 600;
                color: #64748b;
                margin-top: 4px;
            }}
        </style>
    </head>
    <body>
        <div class="kpi-container">
            {cards_html}
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', () => {{
                const tickers = document.querySelectorAll('.ticker-num');
                tickers.forEach(t => {{
                    const isNum = t.getAttribute('data-is-num') === '1';
                    if (!isNum) return;
                    const target = parseFloat(t.getAttribute('data-target'));
                    if (isNaN(target)) return;
                    
                    let current = 0;
                    const duration = 1200;
                    const steps = 40;
                    const stepVal = target / steps;
                    const intervalTime = duration / steps;
                    
                    const timer = setInterval(() => {{
                        current += stepVal;
                        if (current >= target) {{
                            current = target;
                            clearInterval(timer);
                        }}
                        t.textContent = current.toLocaleString(undefined, {{ minimumFractionDigits: target % 1 === 0 ? 0 : 2, maximumFractionDigits: 2 }});
                    }}, intervalTime);
                }});
            }});
        </script>
    </body>
    </html>
    """


def render_apex_sales_wave(dates: list, current_sales: list, ly_sales: list) -> str:
    """Renders a dynamic ApexCharts dual-spline area wave chart."""
    dates_json = json.dumps(dates)
    curr_json = json.dumps([round(v, 2) for v in current_sales])
    ly_json = json.dumps([round(v, 2) for v in ly_sales])

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
        <style>
            body {{ background: transparent; margin: 0; font-family: 'Inter', sans-serif; }}
            .chart-card {{
                background: rgba(15, 23, 42, 0.75);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 12px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
            }}
            .chart-title {{
                color: #00f2fe;
                font-size: 13px;
                font-weight: 800;
                margin-bottom: 6px;
                text-shadow: 0 0 10px rgba(0, 242, 254, 0.5);
            }}
        </style>
    </head>
    <body>
        <div class="chart-card">
            <div class="chart-title">📈 Sales Trend Wave: Cari Dövr (TY) vs Keçən İl (LY)</div>
            <div id="apex-sales-wave"></div>
        </div>
        <script>
            var options = {{
                series: [
                    {{ name: 'Cari Satış (TY)', data: {curr_json} }},
                    {{ name: 'Keçən İl Satışı (LY)', data: {ly_json} }}
                ],
                chart: {{
                    type: 'area',
                    height: 220,
                    toolbar: {{ show: false }},
                    animations: {{
                        enabled: true,
                        easing: 'easeinout',
                        speed: 800,
                        animateGradually: {{ enabled: true, delay: 150 }}
                    }}
                }},
                colors: ['#00f2fe', '#ec4899'],
                stroke: {{ curve: 'smooth', width: [3, 2], dashArray: [0, 4] }},
                fill: {{
                    type: 'gradient',
                    gradient: {{
                        shadeIntensity: 1,
                        opacityFrom: 0.55,
                        opacityTo: 0.05,
                        stops: [0, 90, 100]
                    }}
                }},
                markers: {{
                    size: [4, 0],
                    colors: ['#00f2fe'],
                    strokeColors: '#ffffff',
                    strokeWidth: 2,
                    hover: {{ size: 7 }}
                }},
                dataLabels: {{ enabled: false }},
                xaxis: {{
                    categories: {dates_json},
                    labels: {{ style: {{ colors: '#94a3b8', fontSize: '9px' }} }}
                }},
                yaxis: {{ labels: {{ show: false }} }},
                grid: {{ show: false }},
                legend: {{
                    position: 'top',
                    horizontalAlign: 'right',
                    labels: {{ colors: '#94a3b8' }}
                }},
                tooltip: {{
                    theme: 'dark',
                    x: {{ show: true }},
                    y: {{ formatter: function(val) {{ return val.toLocaleString() + ' ₼'; }} }}
                }}
            }};
            var chart = new ApexCharts(document.querySelector("#apex-sales-wave"), options);
            chart.render();
        </script>
    </body>
    </html>
    """


def render_echarts_hollow_donut(categories: list, values: list) -> str:
    """Renders an Apache ECharts glowing hollow donut."""
    chart_data = []
    for cat, val in zip(categories, values):
        chart_data.append({"name": cat, "value": round(val, 2)})

    data_json = json.dumps(chart_data)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
        <style>
            body {{ background: transparent; margin: 0; font-family: 'Inter', sans-serif; }}
            .chart-card {{
                background: rgba(15, 23, 42, 0.75);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 12px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
            }}
            .chart-title {{
                color: #a855f7;
                font-size: 13px;
                font-weight: 800;
                margin-bottom: 6px;
                text-shadow: 0 0 10px rgba(168, 85, 247, 0.5);
            }}
        </style>
    </head>
    <body>
        <div class="chart-card">
            <div class="chart-title">🍩 Store / Department Sales Share %</div>
            <div id="echarts-donut" style="width: 100%; height: 220px;"></div>
        </div>
        <script>
            var chartDom = document.getElementById('echarts-donut');
            var myChart = echarts.init(chartDom, 'dark');
            var option = {{
                backgroundColor: 'transparent',
                tooltip: {{
                    trigger: 'item',
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    borderColor: '#00f2fe',
                    textStyle: {{ color: '#f8fafc' }},
                    formatter: '<b>{{b}}</b><br/>Satış: <b>{{c}} ₼</b> ({{d}}%)'
                }},
                legend: {{
                    orient: 'vertical',
                    right: 10,
                    top: 'center',
                    textStyle: {{ color: '#94a3b8', fontSize: 9 }}
                }},
                color: ['#00f2fe', '#a855f7', '#10b981', '#f59e0b', '#f43f5e'],
                series: [
                    {{
                        name: 'Sales Share',
                        type: 'pie',
                        radius: ['50%', '75%'],
                        avoidLabelOverlap: false,
                        itemStyle: {{
                            borderRadius: 6,
                            borderColor: '#070a13',
                            borderWidth: 2
                        }},
                        label: {{ show: false, position: 'center' }},
                        emphasis: {{
                            label: {{ show: true, fontSize: 13, fontWeight: 'bold', color: '#00f2fe' }}
                        }},
                        labelLine: {{ show: false }},
                        data: {data_json}
                    }}
                ]
            }};
            myChart.setOption(option);
            window.addEventListener('resize', myChart.resize);
        </script>
    </body>
    </html>
    """


def render_apex_horizontal_bars(labels: list, values: list, title: str = "TOP SKUs", color: str = "#00f2fe") -> str:
    """Renders horizontal ApexCharts neon bars for Top/Bottom SKU rankings."""
    labels_json = json.dumps(labels)
    values_json = json.dumps([round(v, 2) for v in values])

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
        <style>
            body {{ background: transparent; margin: 0; font-family: 'Inter', sans-serif; }}
            .chart-card {{
                background: rgba(15, 23, 42, 0.75);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 12px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
            }}
            .chart-title {{
                color: {color};
                font-size: 13px;
                font-weight: 800;
                margin-bottom: 6px;
                text-shadow: 0 0 10px {color}80;
            }}
        </style>
    </head>
    <body>
        <div class="chart-card">
            <div class="chart-title">{title}</div>
            <div id="apex-bars"></div>
        </div>
        <script>
            var options = {{
                series: [{{ name: 'Revenue (AZN)', data: {values_json} }}],
                chart: {{
                    type: 'bar',
                    height: 220,
                    toolbar: {{ show: false }}
                }},
                plotOptions: {{
                    bar: {{
                        horizontal: true,
                        borderRadius: 6,
                        barHeight: '65%'
                    }}
                }},
                colors: ['{color}'],
                dataLabels: {{
                    enabled: true,
                    formatter: function(val) {{ return val.toLocaleString() + ' ₼'; }},
                    style: {{ colors: ['#ffffff'], fontSize: '9px' }}
                }},
                xaxis: {{
                    categories: {labels_json},
                    labels: {{ show: false }}
                }},
                yaxis: {{
                    labels: {{ style: {{ colors: '#94a3b8', fontSize: '9px' }} }}
                }},
                grid: {{ show: false }},
                tooltip: {{
                    theme: 'dark',
                    y: {{ formatter: function(val) {{ return val.toLocaleString() + ' ₼'; }} }}
                }}
            }};
            var chart = new ApexCharts(document.querySelector("#apex-bars"), options);
            chart.render();
        </script>
    </body>
    </html>
    """


def render_glassmorphic_store_ranking_table(agg_st_df: pd.DataFrame) -> str:
    """
    Renders an Enterprise Glassmorphic Store Performance Table replacing raw Excel dataframe in Tab 2.
    Features: Rank Medals (🥇, 🥈, 🥉), Glowing Progress Bars, YoY Growth Badges.
    """
    if agg_st_df.empty:
        return "<div style='color:#94a3b8;'>Məlumat tapılmadı.</div>"

    total_rev = agg_st_df["GROSS_REVENUE"].sum()
    rows_html = ""
    for idx, row in agg_st_df.iterrows():
        rank = idx
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
        medal_color = "#ffd700" if rank == 1 else "#e2e8f0" if rank == 2 else "#cd7f32" if rank == 3 else "#38bdf8"
        
        st_id = row.get("STORE_ID", "")
        st_name = row.get("STORE_NAME", "Unknown")
        rev = row.get("GROSS_REVENUE", 0.0)
        rev_ly = row.get("GROSS_REVENUE_LY", 0.0)
        diff = row.get("FƏRQ_AZN", rev - rev_ly)
        pct = row.get("ARTIM_%", (diff / rev_ly * 100) if rev_ly > 0 else 0.0)
        
        share_pct = (rev / total_rev * 100) if total_rev > 0 else 0.0
        
        growth_badge = f"<span class='badge-pos'>▲ +{pct:.1f}%</span>" if pct >= 0 else f"<span class='badge-neg'>▼ {pct:.1f}%</span>"
        
        rows_html += f"""
        <tr class="table-row">
            <td class="col-rank" style="color: {medal_color};">{medal}</td>
            <td class="col-store">
                <div class="st-title">{st_name}</div>
                <div class="st-sub">ID: {st_id}</div>
            </td>
            <td class="col-num val-ty">{rev:,.2f} ₼</td>
            <td class="col-num val-ly">{rev_ly:,.2f} ₼</td>
            <td class="col-num">{growth_badge}</td>
            <td class="col-bar">
                <div class="bar-container">
                    <div class="bar-fill" style="width: {min(100, max(4, share_pct))}%;"></div>
                </div>
                <span class="bar-label">{share_pct:.1f}% Pay</span>
            </td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@600;800&family=Inter:wght@500;600;700;800&display=swap');
            body {{ background: transparent; margin: 0; padding: 0; font-family: 'Inter', sans-serif; color: #f8fafc; }}
            
            .glass-table-card {{
                background: rgba(15, 23, 42, 0.85);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(0, 242, 254, 0.25);
                border-radius: 12px;
                padding: 12px 16px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
                max-height: 380px;
                overflow-y: auto;
            }}
            
            /* Custom Neon Scrollbar */
            .glass-table-card::-webkit-scrollbar {{ width: 6px; }}
            .glass-table-card::-webkit-scrollbar-track {{ background: #070a13; }}
            .glass-table-card::-webkit-scrollbar-thumb {{ background: rgba(0, 242, 254, 0.4); border-radius: 4px; }}
            
            table {{ width: 100%; border-collapse: collapse; }}
            th {{
                text-align: left;
                font-size: 11px;
                font-weight: 700;
                color: #38bdf8;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                padding: 10px 8px;
                border-bottom: 1px solid rgba(0, 242, 254, 0.2);
                position: sticky;
                top: 0;
                background: #0f172a;
                z-index: 10;
            }}
            .table-row {{
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                transition: background 0.2s ease;
            }}
            .table-row:hover {{
                background: rgba(0, 242, 254, 0.08);
            }}
            td {{ padding: 10px 8px; font-size: 12.5px; vertical-align: middle; }}
            
            .col-rank {{ font-size: 15px; font-weight: 800; text-align: center; width: 40px; }}
            .st-title {{ font-weight: 700; color: #f8fafc; }}
            .st-sub {{ font-size: 10px; color: #64748b; font-weight: 500; }}
            
            .col-num {{ font-family: 'JetBrains Mono', monospace; font-weight: 700; }}
            .val-ty {{ color: #00f2fe; text-shadow: 0 0 8px rgba(0, 242, 254, 0.4); }}
            .val-ly {{ color: #94a3b8; }}
            
            .badge-pos {{
                background: rgba(16, 185, 129, 0.2);
                border: 1px solid #10b981;
                color: #34d399;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 10.5px;
                font-weight: 700;
                display: inline-block;
            }}
            .badge-neg {{
                background: rgba(244, 63, 94, 0.2);
                border: 1px solid #f43f5e;
                color: #fb7185;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 10.5px;
                font-weight: 700;
                display: inline-block;
            }}
            
            .col-bar {{ width: 140px; }}
            .bar-container {{
                height: 7px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                overflow: hidden;
                margin-bottom: 2px;
            }}
            .bar-fill {{
                height: 100%;
                background: linear-gradient(90deg, #00f2fe, #6366f1);
                border-radius: 4px;
                box-shadow: 0 0 8px rgba(0, 242, 254, 0.6);
            }}
            .bar-label {{ font-size: 10px; color: #94a3b8; font-weight: 600; }}
        </style>
    </head>
    <body>
        <div class="glass-table-card">
            <table>
                <thead>
                    <tr>
                        <th>Sıra</th>
                        <th>Mağaza Adı</th>
                        <th>Cari Satış (AZN)</th>
                        <th>Keçən İl (LY)</th>
                        <th>Artım YoY</th>
                        <th>Satış Payı %</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """


def render_glassmorphic_supplier_leadership_table(df_filtered_ty: pd.DataFrame, top_n: int = 10) -> str:
    """
    Renders an Enterprise Glassmorphic Supplier Leadership Table replacing raw Excel dataframe in Supplier tab.
    Features: Rank Medals, Supplier Name, SKU Count, Gross Revenue, Sales Share % mini progress bars, Status Badges.
    """
    if df_filtered_ty.empty:
        return "<div style='color:#94a3b8;'>Məlumat tapılmadı.</div>"

    agg_sup = df_filtered_ty.groupby("SATICI ADI").agg(
        GROSS_REVENUE=("GROSS_REVENUE", "sum"),
        QUANTITY=("QUANTITY", "sum"),
        SKU_COUNT=("MEHSUL_KODU", "nunique")
    ).reset_index().sort_values("GROSS_REVENUE", ascending=False).head(top_n)

    total_rev = df_filtered_ty["GROSS_REVENUE"].sum()
    rows_html = ""

    for idx, row in agg_sup.reset_index(drop=True).iterrows():
        rank = idx + 1
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
        medal_color = "#ffd700" if rank == 1 else "#e2e8f0" if rank == 2 else "#cd7f32" if rank == 3 else "#a855f7"
        
        sup_name = row["SATICI ADI"]
        rev = row["GROSS_REVENUE"]
        qty = row["QUANTITY"]
        skus = row["SKU_COUNT"]
        share_pct = (rev / total_rev * 100) if total_rev > 0 else 0.0

        status_badge = "<span class='badge-active'>🟢 Lider Təchizatçı</span>" if rank <= 3 else "<span class='badge-norm'>⚡ Aktiv</span>"

        rows_html += f"""
        <tr class="table-row">
            <td class="col-rank" style="color: {medal_color};">{medal}</td>
            <td class="col-sup">
                <div class="sup-title">{sup_name}</div>
                <div class="sup-sub">Çeşid: {skus} SKU &nbsp;|&nbsp; Miqdar: {qty:,.0f} əd</div>
            </td>
            <td class="col-num val-rev">{rev:,.2f} ₼</td>
            <td class="col-badge">{status_badge}</td>
            <td class="col-bar">
                <div class="bar-container">
                    <div class="bar-fill" style="width: {min(100, max(4, share_pct))}%;"></div>
                </div>
                <span class="bar-label">{share_pct:.1f}% Pay</span>
            </td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@600;800&family=Inter:wght@500;600;700;800&display=swap');
            body {{ background: transparent; margin: 0; padding: 0; font-family: 'Inter', sans-serif; color: #f8fafc; }}
            
            .glass-table-card {{
                background: rgba(15, 23, 42, 0.85);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(168, 85, 247, 0.3);
                border-radius: 12px;
                padding: 12px 16px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
                max-height: 380px;
                overflow-y: auto;
            }}
            
            .glass-table-card::-webkit-scrollbar {{ width: 6px; }}
            .glass-table-card::-webkit-scrollbar-track {{ background: #070a13; }}
            .glass-table-card::-webkit-scrollbar-thumb {{ background: rgba(168, 85, 247, 0.4); border-radius: 4px; }}
            
            table {{ width: 100%; border-collapse: collapse; }}
            th {{
                text-align: left;
                font-size: 11px;
                font-weight: 700;
                color: #c084fc;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                padding: 10px 8px;
                border-bottom: 1px solid rgba(168, 85, 247, 0.25);
                position: sticky;
                top: 0;
                background: #0f172a;
                z-index: 10;
            }}
            .table-row {{
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                transition: background 0.2s ease;
            }}
            .table-row:hover {{
                background: rgba(168, 85, 247, 0.1);
            }}
            td {{ padding: 10px 8px; font-size: 12.5px; vertical-align: middle; }}
            
            .col-rank {{ font-size: 15px; font-weight: 800; text-align: center; width: 40px; }}
            .sup-title {{ font-weight: 700; color: #f8fafc; }}
            .sup-sub {{ font-size: 10px; color: #94a3b8; font-weight: 500; margin-top: 2px; }}
            
            .col-num {{ font-family: 'JetBrains Mono', monospace; font-weight: 700; }}
            .val-rev {{ color: #a855f7; text-shadow: 0 0 8px rgba(168, 85, 247, 0.5); }}
            
            .badge-active {{
                background: rgba(168, 85, 247, 0.2);
                border: 1px solid #a855f7;
                color: #e9d5ff;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 10.5px;
                font-weight: 700;
                display: inline-block;
            }}
            .badge-norm {{
                background: rgba(0, 242, 254, 0.15);
                border: 1px solid rgba(0, 242, 254, 0.4);
                color: #38bdf8;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 10.5px;
                font-weight: 700;
                display: inline-block;
            }}
            
            .col-bar {{ width: 140px; }}
            .bar-container {{
                height: 7px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                overflow: hidden;
                margin-bottom: 2px;
            }}
            .bar-fill {{
                height: 100%;
                background: linear-gradient(90deg, #a855f7, #ec4899);
                border-radius: 4px;
                box-shadow: 0 0 8px rgba(168, 85, 247, 0.6);
            }}
            .bar-label {{ font-size: 10px; color: #94a3b8; font-weight: 600; }}
        </style>
    </head>
    <body>
        <div class="glass-table-card">
            <table>
                <thead>
                    <tr>
                        <th>Sıra</th>
                        <th>Təchizatçı / Brend Adı</th>
                        <th>Ümumi Gəlir (AZN)</th>
                        <th>Status Badji</th>
                        <th>Satış Payı %</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """


def render_glassmorphic_risk_radar_table(blocked_df: pd.DataFrame) -> str:
    """
    Renders an Enterprise Glassmorphic Danger Risk Radar Table in Tab 3 replacing raw Excel dataframe.
    Features: Red Danger Glow Cards, Status Badges (🔴 SATIŞA BLOKLANIB), Item Name/Code, Lost Revenue.
    """
    if blocked_df.empty:
        return """
        <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; padding: 12px; border-radius: 10px; color: #34d399; font-weight: 700;">
            ✅ Qrup üzrə heç bir məhsul satışa bloklanmayıb! Bütün çeşidlər aktivdir.
        </div>
        """

    rows_html = ""
    agg_blocked = blocked_df.groupby(["MEHSUL_KODU", "MEHSUL_ADI", "CATEGORY NAME", "SATICI ADI"]).agg(
        GROSS_REVENUE=("GROSS_REVENUE", "sum"),
        QUANTITY=("QUANTITY", "sum")
    ).reset_index().sort_values("GROSS_REVENUE", ascending=False).head(15)

    for idx, row in agg_blocked.iterrows():
        sku = row["MEHSUL_KODU"]
        name = row["MEHSUL_ADI"]
        cat = row["CATEGORY NAME"]
        sup = row["SATICI ADI"]
        rev = row["GROSS_REVENUE"]
        qty = row["QUANTITY"]

        rows_html += f"""
        <tr class="table-row">
            <td class="col-badge"><span class="badge-danger">🔴 SATIŞA BLOKLU</span></td>
            <td class="col-item">
                <div class="item-title">{name}</div>
                <div class="item-sub">SKU: {sku} &nbsp;|&nbsp; Kateqoriya: {cat}</div>
            </td>
            <td class="col-sup">{sup}</td>
            <td class="col-num val-lost">{rev:,.2f} ₼</td>
            <td class="col-num">{qty:,.0f} əd</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@600;800&family=Inter:wght@500;600;700;800&display=swap');
            body {{ background: transparent; margin: 0; padding: 0; font-family: 'Inter', sans-serif; color: #f8fafc; }}
            
            .glass-table-card {{
                background: rgba(239, 68, 68, 0.1);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(239, 68, 68, 0.4);
                border-radius: 12px;
                padding: 12px 16px;
                box-shadow: 0 8px 32px rgba(239, 68, 68, 0.2);
                max-height: 380px;
                overflow-y: auto;
            }}
            
            .glass-table-card::-webkit-scrollbar {{ width: 6px; }}
            .glass-table-card::-webkit-scrollbar-track {{ background: #070a13; }}
            .glass-table-card::-webkit-scrollbar-thumb {{ background: rgba(239, 68, 68, 0.5); border-radius: 4px; }}
            
            table {{ width: 100%; border-collapse: collapse; }}
            th {{
                text-align: left;
                font-size: 11px;
                font-weight: 700;
                color: #f87171;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                padding: 10px 8px;
                border-bottom: 1px solid rgba(239, 68, 68, 0.3);
                position: sticky;
                top: 0;
                background: #18090e;
                z-index: 10;
            }}
            .table-row {{
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                transition: background 0.2s ease;
            }}
            .table-row:hover {{
                background: rgba(239, 68, 68, 0.15);
            }}
            td {{ padding: 10px 8px; font-size: 12.5px; vertical-align: middle; }}
            
            .item-title {{ font-weight: 700; color: #f8fafc; }}
            .item-sub {{ font-size: 10px; color: #fca5a5; font-weight: 500; margin-top: 2px; }}
            .col-sup {{ color: #cbd5e1; font-size: 11.5px; }}
            
            .col-num {{ font-family: 'JetBrains Mono', monospace; font-weight: 700; }}
            .val-lost {{ color: #ef4444; text-shadow: 0 0 8px rgba(239, 68, 68, 0.6); }}
            
            .badge-danger {{
                background: rgba(239, 68, 68, 0.25);
                border: 1px solid #ef4444;
                color: #fca5a5;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 10.5px;
                font-weight: 800;
                display: inline-block;
            }}
        </style>
    </head>
    <body>
        <div class="glass-table-card">
            <table>
                <thead>
                    <tr>
                        <th>Status</th>
                        <th>Məhsul Kodu & Adı</th>
                        <th>Təchizatçı</th>
                        <th>Potensial İtki (AZN)</th>
                        <th>Miqdar</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
