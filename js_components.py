"""
Pure JavaScript (ApexCharts JS & Apache ECharts & Canvas Animations) Component Engine
High-Tech Cosmic Dark & Neon Glow Architecture
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
        
        # Handle string or float values for ticker
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
            // JavaScript Animated Count-Up Ticker Engine
            document.addEventListener('DOMContentLoaded', () => {{
                const tickers = document.querySelectorAll('.ticker-num');
                tickers.forEach(t => {{
                    const isNum = t.getAttribute('data-is-num') === '1';
                    if (!isNum) return;
                    const target = parseFloat(t.getAttribute('data-target'));
                    if (isNaN(target)) return;
                    
                    let current = 0;
                    const duration = 1200; // ms
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
    """
    Renders a dynamic ApexCharts dual-spline area wave chart with neon cyan (#00f2fe) and magenta (#ec4899) glowing gradient lines.
    Includes dark-glass tooltips, crosshair tracking, and smooth pan/zoom physics.
    """
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
    """
    Renders an Apache ECharts high-density glowing hollow donut with animated entry and center total readout.
    """
    chart_data = []
    total_val = sum(values)
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
                        label: {{
                            show: false,
                            position: 'center'
                        }},
                        emphasis: {{
                            label: {{
                                show: true,
                                fontSize: 13,
                                fontWeight: 'bold',
                                color: '#00f2fe'
                            }}
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
    """
    Renders horizontal ApexCharts neon bars with smooth hover expansion and gradient fills for Top/Bottom SKU rankings.
    """
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
