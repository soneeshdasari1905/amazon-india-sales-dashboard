"""Product Analytics Page: Category breakdowns, product performance, units sold, and Top 10 rankings."""

import streamlit as st
import pandas as pd
from styles import render_header, render_kpi_card, render_section_header, render_html
from utils.formatting import format_inr, format_count, format_pct
from utils.charts import (
    plot_category_sales,
    plot_category_profit,
    plot_category_units,
    plot_top_10_products,
    AMAZON_ORANGE,
    AMAZON_BLUE
)
import plotly.express as px
import plotly.graph_objects as go


def render_product_analytics(df, total_rows):
    """Render the Product Analytics dashboard page."""
    render_header(
        title="Product Analytics",
        subtitle="Category-level velocity, product profitability rankings, and volume distribution",
        record_count=len(df),
        total_count=total_rows
    )

    if df.empty:
        st.warning("⚠️ No data available matching the selected filters. Please adjust your filter criteria in the sidebar.")
        return

    # 1. SUMMARY METRICS
    cat_summary = df.groupby('Category').agg(
        Sales=('Total_Sales_INR', 'sum'),
        Profit=('Profit_INR', 'sum'),
        Units=('Quantity', 'sum')
    ).reset_index()
    cat_summary['Margin'] = (cat_summary['Profit'] / cat_summary['Sales']) * 100

    top_cat = cat_summary.loc[cat_summary['Sales'].idxmax()]['Category']
    top_cat_sales = cat_summary['Sales'].max()

    prod_summary = df.groupby(['Product', 'Category']).agg(
        Sales=('Total_Sales_INR', 'sum'),
        Profit=('Profit_INR', 'sum'),
        Units=('Quantity', 'sum'),
        Avg_Price=('Unit_Price_INR', 'mean'),
        Avg_Discount=('Discount_Pct', 'mean')
    ).reset_index()
    prod_summary['Margin'] = (prod_summary['Profit'] / prod_summary['Sales']) * 100

    best_product = prod_summary.loc[prod_summary['Sales'].idxmax()]['Product']
    best_product_sales = prod_summary['Sales'].max()
    highest_margin_cat = cat_summary.loc[cat_summary['Margin'].idxmax()]['Category']
    highest_margin_val = cat_summary['Margin'].max()

    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card(
            title="Top Revenue Category",
            value=top_cat,
            subtitle=f"{format_inr(top_cat_sales, compact=True)} total sales",
            icon="🏆",
            variant="orange",
            pill_text="Leader"
        )
    with col2:
        render_kpi_card(
            title="Best-Selling Product",
            value=best_product,
            subtitle=f"{format_inr(best_product_sales, compact=True)} total sales",
            icon="⭐",
            variant="blue",
            pill_text="No. 1 SKU"
        )
    with col3:
        render_kpi_card(
            title="Highest Margin Category",
            value=highest_margin_cat,
            subtitle=f"{highest_margin_val:.1f}% profit margin",
            icon="💎",
            variant="green",
            pill_text="Max Margin"
        )
    with col4:
        render_kpi_card(
            title="Unique Catalog SKUs",
            value=f"{df['Product'].nunique()} Products",
            subtitle=f"Across {df['Category'].nunique()} active categories",
            icon="🏷️",
            variant="teal",
            pill_text="Catalog"
        )

    render_html("<div style='height: 14px;'></div>")

    # 2. CATEGORY BREAKDOWN GRAPHS
    render_section_header("Category Performance Diagnostics", icon="📦")

    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        st.plotly_chart(plot_category_sales(df), use_container_width=True)
    with row1_c2:
        st.plotly_chart(plot_category_profit(df), use_container_width=True)

    row2_c1, row2_c2 = st.columns([1, 1])
    with row2_c1:
        st.plotly_chart(plot_category_units(df), use_container_width=True)
    with row2_c2:
        # Category efficiency table
        render_html("""
        <div style="font-size: 14px; font-weight: 700; color: #131921; margin-bottom: 10px; border-bottom: 2px solid #EAEDED; padding-bottom: 6px;">
            📋 Category Metrics Matrix
        </div>
        """)

        cat_matrix_display = cat_summary.sort_values('Sales', ascending=False).copy()
        cat_matrix_display['Sales_Fmt'] = cat_matrix_display['Sales'].apply(lambda x: format_inr(x, compact=True))
        cat_matrix_display['Profit_Fmt'] = cat_matrix_display['Profit'].apply(lambda x: format_inr(x, compact=True))
        cat_matrix_display['Margin_Fmt'] = cat_matrix_display['Margin'].apply(lambda x: f"{x:.1f}%")
        cat_matrix_display['Units_Fmt'] = cat_matrix_display['Units'].apply(format_count)

        st.dataframe(
            cat_matrix_display[['Category', 'Sales_Fmt', 'Profit_Fmt', 'Margin_Fmt', 'Units_Fmt']].rename(columns={
                'Category': 'Category',
                'Sales_Fmt': 'Sales',
                'Profit_Fmt': 'Profit',
                'Margin_Fmt': 'Margin %',
                'Units_Fmt': 'Units'
            }),
            use_container_width=True,
            hide_index=True
        )

    # 3. TOP 10 PRODUCTS BY SALES
    render_html("<div style='height: 14px;'></div>")
    render_section_header("Top 10 Products by Sales", icon="🔥")
    st.plotly_chart(plot_top_10_products(df), use_container_width=True)

    # 4. CATEGORY DRILL-DOWN & FULL PRODUCT CATALOG TABLE
    render_html("<div style='height: 14px;'></div>")
    render_section_header("Catalog Performance Deep Dive", icon="🔍")

    selected_category = st.selectbox(
        "Filter Deep Dive by Category:",
        options=["All Categories"] + sorted(df['Category'].unique().tolist()),
        index=0
    )

    drill_df = prod_summary if selected_category == "All Categories" else prod_summary[prod_summary['Category'] == selected_category]

    catalog_display = drill_df.sort_values('Sales', ascending=False).copy()
    catalog_display['Sales (INR)'] = catalog_display['Sales'].apply(lambda x: format_inr(x, compact=False, decimals=2))
    catalog_display['Profit (INR)'] = catalog_display['Profit'].apply(lambda x: format_inr(x, compact=False, decimals=2))
    catalog_display['Margin %'] = catalog_display['Margin'].apply(lambda x: f"{x:.1f}%")
    catalog_display['Units Sold'] = catalog_display['Units'].apply(format_count)
    catalog_display['Avg Price'] = catalog_display['Avg_Price'].apply(lambda x: format_inr(x, compact=False, decimals=2))
    catalog_display['Avg Discount'] = catalog_display['Avg_Discount'].apply(lambda x: f"{x*100:.1f}%")

    st.dataframe(
        catalog_display[['Product', 'Category', 'Sales (INR)', 'Profit (INR)', 'Margin %', 'Units Sold', 'Avg Price', 'Avg Discount']],
        use_container_width=True,
        hide_index=True
    )

    # CSV Download Button
    csv = catalog_display.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Product Performance (CSV)",
        data=csv,
        file_name="amazon_india_product_performance.csv",
        mime="text/csv",
        help="Export the current filtered product table into a spreadsheet-friendly CSV format"
    )
