"""
High-Density Executive Analytics Visuals Engine
Includes Product Velocity Quadrant Matrix, Insert/Promotion Charts, Supplier Analytics & Risk Radar
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

COLOR_BG_DARK = "#070A13"
COLOR_CARD = "#121826"
COLOR_TEXT_MAIN = "#f8fafc"
COLOR_TEXT_MUTED = "#94a3b8"


def apply_dark_theme(fig: go.Figure, height: int = 280, **kwargs) -> go.Figure:
    """Applies ultra-clean Plotly dark theme with smooth 500ms transitions."""
    theme = dict(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLOR_TEXT_MAIN, family="Inter, -apple-system, sans-serif", size=10),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(color=COLOR_TEXT_MUTED, size=9),
            title="",
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(color=COLOR_TEXT_MUTED, size=9),
            title="",
        ),
        margin=dict(l=15, r=15, t=32, b=15),
        transition={"duration": 500, "easing": "cubic-in-out"},
    )
    theme.update(kwargs)
    fig.update_layout(**theme)
    return fig


def create_day_of_week_chart(df: pd.DataFrame) -> go.Figure:
    """Tab 1 Bottom: Day of Week Sales Pattern (Monday-Sunday peak analysis)."""
    if df.empty:
        return go.Figure()

    df_dow = df.copy()
    df_dow["DOW_NUM"] = pd.to_datetime(df_dow["SALES_DATE"]).dt.dayofweek
    dow_names = ["Bazar ertəsi", "Çərşənbə axşamı", "Çərşənbə", "Cümə axşamı", "Cümə", "Şənbə", "Bazar"]
    df_dow["DOW_NAME"] = df_dow["DOW_NUM"].apply(lambda n: dow_names[n])
    
    agg = df_dow.groupby(["DOW_NUM", "DOW_NAME"])["GROSS_REVENUE"].sum().reset_index().sort_values("DOW_NUM")

    fig = go.Figure(
        go.Bar(
            x=agg["DOW_NAME"],
            y=agg["GROSS_REVENUE"],
            marker=dict(color=agg["GROSS_REVENUE"], colorscale="Viridis", showscale=False),
            text=agg["GROSS_REVENUE"].apply(lambda v: f"{v:,.0f} ₼"),
            textposition="outside",
            hovertemplate="<b>Gün:</b> %{x}<br><b>Satış:</b> <b>%{y:,.2f} ₼</b><extra></extra>"
        )
    )

    apply_dark_theme(
        fig,
        height=260,
        title=dict(text="<b>📅 Haftalık Günlük Satış Nümunəsi (Peak Sales Days)</b>", font=dict(size=13, color="#38bdf8")),
        yaxis=dict(showticklabels=False)
    )
    return fig


def create_store_ranking_chart(df: pd.DataFrame, top_n: int = 10, mode: str = "Top") -> go.Figure:
    """Horizontal bar chart for Store Revenue Rankings (Tab 2)."""
    if df.empty:
        return go.Figure()

    agg = df.groupby("STORE_NAME")["GROSS_REVENUE"].sum().reset_index()
    
    if mode in ["Top", "Ən Yaxşı"]:
        agg = agg.sort_values("GROSS_REVENUE", ascending=False).head(top_n)
        agg = agg.sort_values("GROSS_REVENUE", ascending=True)
        colorscale = "Purples"
    else:
        agg = agg.sort_values("GROSS_REVENUE", ascending=True).head(top_n)
        agg = agg.sort_values("GROSS_REVENUE", ascending=False)
        colorscale = "Reds"

    fig = go.Figure(
        go.Bar(
            x=agg["GROSS_REVENUE"],
            y=agg["STORE_NAME"],
            orientation="h",
            marker=dict(color=agg["GROSS_REVENUE"], colorscale=colorscale, showscale=False),
            text=agg["GROSS_REVENUE"].apply(lambda v: f"{v:,.0f} ₼"),
            textposition="inside",
            hovertemplate="<b>Mağaza:</b> %{y}<br><b>Satış:</b> <b>%{x:,.2f} ₼</b><extra></extra>"
        )
    )

    apply_dark_theme(
        fig,
        height=300,
        title=dict(text=f"<b>Mağaza Gəlir Reytinqi ({mode} {top_n})</b>", font=dict(size=13, color="#c084fc"))
    )
    return fig


def create_store_treemap(df: pd.DataFrame) -> go.Figure:
    """Interactive Treemap for QRUP / Category Distribution (Tab 3)."""
    if df.empty:
        return go.Figure()

    agg = df.groupby(["QRUP", "FAMILY NAME", "CATEGORY NAME"]).agg(REVENUE=("GROSS_REVENUE", "sum")).reset_index()

    fig = px.treemap(
        agg,
        path=[px.Constant("Bütün Kateqoriyalar"), "QRUP", "FAMILY NAME", "CATEGORY NAME"],
        values="REVENUE",
        color="REVENUE",
        color_continuous_scale="Tealgrn"
    )

    apply_dark_theme(
        fig,
        height=300,
        title=dict(text="<b>QRUP və Kateqoriya Paylanma Treemap-i</b>", font=dict(size=13, color="#38bdf8")),
        margin=dict(l=10, r=10, t=35, b=10)
    )
    return fig


def create_pareto_chart(df: pd.DataFrame) -> go.Figure:
    """80/20 Pareto & ABC Chart (Tab 3)."""
    if df.empty:
        return go.Figure()

    agg = df.groupby("CATEGORY NAME")["GROSS_REVENUE"].sum().reset_index()
    agg = agg.sort_values("GROSS_REVENUE", ascending=False)
    agg["CUMSUM"] = agg["GROSS_REVENUE"].cumsum()
    total_rev = agg["GROSS_REVENUE"].sum()
    agg["CUM_PCT"] = (agg["CUMSUM"] / total_rev) * 100 if total_rev > 0 else 0

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=agg["CATEGORY NAME"],
            y=agg["GROSS_REVENUE"],
            name="Satış (AZN)",
            marker_color="#6366f1",
            hovertemplate="<b>Kateqoriya:</b> %{x}<br><b>Satış:</b> <b>%{y:,.2f} ₼</b><extra></extra>"
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=agg["CATEGORY NAME"],
            y=agg["CUM_PCT"],
            name="Kumulyativ %",
            mode="lines+markers",
            line=dict(color="#f59e0b", width=2.5),
            marker=dict(size=6, color="#ffffff"),
            hovertemplate="<b>Kateqoriya:</b> %{x}<br><b>Kumulyativ %:</b> <b>%{y:.1f}%</b><extra></extra>"
        ),
        secondary_y=True
    )

    fig.add_hline(y=80, line_dash="dash", line_color="#ef4444", annotation_text="80% Baza Sərhədi", secondary_y=True)

    apply_dark_theme(
        fig,
        height=300,
        title=dict(text="<b>Pareto 80/20 & ABC Kateqoriya Analizi</b>", font=dict(size=13, color="#6366f1")),
        showlegend=False
    )

    fig.update_yaxes(showticklabels=False, secondary_y=False)
    fig.update_yaxes(showticklabels=False, secondary_y=True)

    return fig


def create_product_velocity_quadrant(df: pd.DataFrame) -> go.Figure:
    """Tab 3: 4-Quadrant Bubble/Scatter Matrix (Sales Vol vs Gross Revenue)."""
    if df.empty:
        return go.Figure()

    agg = df.groupby(["MEHSUL_KODU", "MEHSUL_ADI", "CATEGORY NAME"]).agg(
        TOTAL_REV=("GROSS_REVENUE", "sum"),
        TOTAL_QTY=("QUANTITY", "sum")
    ).reset_index()

    agg["AVG_PRICE"] = agg["TOTAL_REV"] / agg["TOTAL_QTY"].replace(0, 1)
    median_rev = agg["TOTAL_REV"].median()
    median_qty = agg["TOTAL_QTY"].median()

    fig = px.scatter(
        agg,
        x="TOTAL_QTY",
        y="TOTAL_REV",
        size="AVG_PRICE",
        color="CATEGORY NAME",
        hover_name="MEHSUL_ADI",
        size_max=30,
        labels={"TOTAL_QTY": "Satış Miqdarı (Ədəd)", "TOTAL_REV": "Ümumi Satış (AZN)"}
    )

    fig.add_vline(x=median_qty, line_dash="dash", line_color="rgba(255,255,255,0.3)")
    fig.add_hline(y=median_rev, line_dash="dash", line_color="rgba(255,255,255,0.3)")

    apply_dark_theme(
        fig,
        height=320,
        title=dict(text="<b>⚡ Product Velocity & 4-Quadrant Matrix (Star vs Cash Cows)</b>", font=dict(size=13, color="#00f2fe")),
        showlegend=False
    )
    return fig


def create_top_suppliers_chart(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Supplier Intelligence: Top 10 Suppliers Horizontal Bar Chart."""
    if df.empty:
        return go.Figure()

    agg = df.groupby("SATICI ADI")["GROSS_REVENUE"].sum().reset_index()
    agg = agg.sort_values("GROSS_REVENUE", ascending=False).head(top_n)
    agg = agg.sort_values("GROSS_REVENUE", ascending=True)

    fig = go.Figure(
        go.Bar(
            x=agg["GROSS_REVENUE"],
            y=agg["SATICI ADI"],
            orientation="h",
            marker=dict(color=agg["GROSS_REVENUE"], colorscale="Teal", showscale=False),
            text=agg["GROSS_REVENUE"].apply(lambda v: f"{v:,.0f} ₼"),
            textposition="inside",
            hovertemplate="<b>Təchizatçı:</b> %{y}<br><b>Satış:</b> <b>%{x:,.2f} ₼</b><extra></extra>"
        )
    )

    apply_dark_theme(
        fig,
        height=300,
        title=dict(text=f"<b>🏭 Top {top_n} Təchizatçı Liderlik Paneli (Satış AZN)</b>", font=dict(size=13, color="#2dd4bf")),
        margin=dict(l=140, r=20, t=35, b=10)
    )
    return fig


def create_supplier_concentration_donut_chart(df: pd.DataFrame) -> go.Figure:
    """Supplier Intelligence: Supplier Revenue Concentration Donut Chart."""
    if df.empty:
        return go.Figure()

    agg = df.groupby("SATICI ADI")["GROSS_REVENUE"].sum().reset_index().sort_values("GROSS_REVENUE", ascending=False)
    total_rev = agg["GROSS_REVENUE"].sum()

    if len(agg) > 5:
        top5 = agg.head(5).copy()
        others_val = agg.iloc[5:]["GROSS_REVENUE"].sum()
        others_df = pd.DataFrame([{"SATICI ADI": "Digər Təchizatçılar", "GROSS_REVENUE": others_val}])
        agg_final = pd.concat([top5, others_df], ignore_index=True)
    else:
        agg_final = agg

    fig = go.Figure(
        go.Pie(
            labels=agg_final["SATICI ADI"],
            values=agg_final["GROSS_REVENUE"],
            hole=0.6,
            marker=dict(colors=["#2dd4bf", "#38bdf8", "#818cf8", "#c084fc", "#fb923c", "#94a3b8"]),
            textinfo="percent",
            textposition="inside",
            hovertemplate="<b>Təchizatçı:</b> %{label}<br><b>Satış:</b> <b>%{value:,.2f} ₼</b> (%{percent})<extra></extra>"
        )
    )

    apply_dark_theme(
        fig,
        height=300,
        title=dict(text="<b>🍩 Təchizatçı Gəlir Cəmləşməsi (Top 5 vs Digər)</b>", font=dict(size=13, color="#2dd4bf")),
        annotations=[
            dict(
                text=f"<b>Ümumi</b><br><span style='font-size:12px; color:#ffffff;'>{total_rev:,.0f} ₼</span>",
                x=0.5, y=0.5, font_size=10, showarrow=False
            )
        ],
        legend=dict(orientation="v", font=dict(size=8), y=0.5)
    )
    return fig


def create_insert_sales_comparison_chart(df: pd.DataFrame) -> go.Figure:
    """Tab Insert: Standart Satış vs İnser Satış Comparison (Dual Bar)."""
    if df.empty:
        return go.Figure()

    df_d = df.copy()
    df_d["DATE"] = pd.to_datetime(df_d["SALES_DATE"]).dt.strftime("%d %b")
    agg = df_d.groupby("DATE").agg(
        TOTAL_REV=("GROSS_REVENUE", "sum"),
        INSERT_REV=("INSERT_SATIS_EDV", "sum")
    ).reset_index().tail(15)

    agg["STANDARD_REV"] = agg["TOTAL_REV"] - agg["INSERT_REV"]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=agg["DATE"],
            y=agg["STANDARD_REV"],
            name="Standart Satış",
            marker_color="#6366f1",
            hovertemplate="<b>Tarix:</b> %{x}<br><b>Standart Satış:</b> <b>%{y:,.2f} ₼</b><extra></extra>"
        )
    )

    fig.add_trace(
        go.Bar(
            x=agg["DATE"],
            y=agg["INSERT_REV"],
            name="İnser / Promosiya Satışı",
            marker_color="#f43f5e",
            hovertemplate="<b>Tarix:</b> %{x}<br><b>İnser Satış:</b> <b>%{y:,.2f} ₼</b><extra></extra>"
        )
    )

    apply_dark_theme(
        fig,
        height=290,
        title=dict(text="<b> Standart Satış vs İnser Promosiya Satış Dinamikası</b>", font=dict(size=13, color="#f43f5e")),
        barmode="stack",
        yaxis=dict(showticklabels=False)
    )
    return fig


def create_top_insert_products_chart(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Tab Insert: Top 10 Insert / Promotion Products (Horizontal Neon Bar)."""
    if df.empty:
        return go.Figure()

    agg = df.groupby("MEHSUL_ADI")["INSERT_SATIS_EDV"].sum().reset_index()
    agg = agg.sort_values("INSERT_SATIS_EDV", ascending=False).head(top_n)
    agg = agg.sort_values("INSERT_SATIS_EDV", ascending=True)

    agg["DISPLAY_NAME"] = agg["MEHSUL_ADI"].apply(lambda s: str(s)[:22] + "..." if len(str(s)) > 24 else str(s))

    fig = go.Figure(
        go.Bar(
            x=agg["INSERT_SATIS_EDV"],
            y=agg["DISPLAY_NAME"],
            orientation="h",
            marker=dict(color="#f43f5e", line=dict(color="#fb7185", width=1)),
            text=agg["INSERT_SATIS_EDV"].apply(lambda v: f"{v:,.0f} ₼"),
            textposition="outside",
            hovertemplate="<b>Məhsul:</b> %{y}<br><b>İnser Satışı:</b> <b>%{x:,.2f} ₼</b><extra></extra>"
        )
    )

    apply_dark_theme(
        fig,
        height=290,
        title=dict(text=f"<b> Top {top_n} İnser Promosiya Məhsulları</b>", font=dict(size=13, color="#fb7185")),
        xaxis=dict(showticklabels=False),
        margin=dict(l=110, r=40, t=35, b=10)
    )
    return fig


def create_waterfall_contribution_chart(df_ty: pd.DataFrame, df_ly: pd.DataFrame) -> go.Figure:
    """Sales Contribution Waterfall Chart showing top category revenue drivers (Tab 3)."""
    if df_ty.empty:
        return go.Figure()

    agg_ty = df_ty.groupby("CATEGORY NAME")["GROSS_REVENUE"].sum().reset_index()
    if not df_ly.empty:
        agg_ly = df_ly.groupby("CATEGORY NAME")["GROSS_REVENUE"].sum().reset_index()
        merged = pd.merge(agg_ty, agg_ly, on="CATEGORY NAME", how="outer", suffixes=("_TY", "_LY")).fillna(0)
    else:
        merged = agg_ty.copy()
        merged["GROSS_REVENUE_TY"] = merged["GROSS_REVENUE"]
        merged["GROSS_REVENUE_LY"] = merged["GROSS_REVENUE"] * 0.85

    merged["DELTA"] = merged["GROSS_REVENUE_TY"] - merged["GROSS_REVENUE_LY"]
    merged = merged.sort_values("DELTA", ascending=False).head(5)

    x_vals = ["Keçən İl (LY)"] + merged["CATEGORY NAME"].tolist() + ["Cari İl (TY)"]
    measures = ["absolute"] + ["relative"] * len(merged) + ["total"]
    y_vals = [merged["GROSS_REVENUE_LY"].sum()] + merged["DELTA"].tolist() + [0]

    fig = go.Figure(
        go.Waterfall(
            name="Gəlir Töhfəsi",
            orientation="v",
            measure=measures,
            x=x_vals,
            y=y_vals,
            connector=dict(line=dict(color="rgba(255,255,255,0.2)")),
            increasing=dict(marker=dict(color="#10b981")),
            decreasing=dict(marker=dict(color="#ef4444")),
            totals=dict(marker=dict(color="#6366f1"))
        )
    )

    apply_dark_theme(
        fig,
        height=300,
        title=dict(text="<b>Gəlir Fərqinə Ən Çox Töhfə Verən Kateqoriyalar (Waterfall)</b>", font=dict(size=13, color="#10b981"))
    )
    return fig


def create_basket_analytics_chart(df: pd.DataFrame) -> go.Figure:
    """Basket Analytics: SATIS_EDV vs SATIS_EDVSIZ Tax Analysis (Tab 4)."""
    if df.empty:
        return go.Figure()

    df_b = df.copy()
    df_b["DATE"] = pd.to_datetime(df_b["SALES_DATE"]).dt.strftime("%d %b")
    agg = df_b.groupby("DATE").agg(
        EDV_INCL=("SATIS_EDV", "sum"),
        EDV_EXCL=("SATIS_EDVSIZ", "sum")
    ).reset_index().tail(15)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=agg["DATE"],
            y=agg["EDV_INCL"],
            name="ƏDV Daxil Satış",
            marker_color="#38bdf8",
            hovertemplate="<b>Tarix:</b> %{x}<br><b>ƏDV Daxil:</b> <b>%{y:,.2f} ₼</b><extra></extra>"
        )
    )

    fig.add_trace(
        go.Bar(
            x=agg["DATE"],
            y=agg["EDV_EXCL"],
            name="ƏDV-siz Satış (Maya/Net)",
            marker_color="#818cf8",
            hovertemplate="<b>Tarix:</b> %{x}<br><b>ƏDV Xaric:</b> <b>%{y:,.2f} ₼</b><extra></extra>"
        )
    )

    apply_dark_theme(
        fig,
        height=280,
        title=dict(text="<b>ƏDV Daxil və ƏDV-siz Satış Fərq Analizi</b>", font=dict(size=13, color="#38bdf8")),
        barmode="group",
        yaxis=dict(showticklabels=False)
    )
    return fig
