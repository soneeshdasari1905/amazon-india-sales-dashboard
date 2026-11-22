"""Sales Overview Page: High-level financial KPIs, monthly trends, and revenue drivers."""

import streamlit as st
import pandas as pd
from styles import render_header, render_kpi_card, render_section_header, render_html
from utils.formatting import format_inr, format_count, format_pct
from utils.charts import plot_monthly_sales_and_profit, plot_category_sales, plot_category_profit


def render_sales_overview(df, total_rows):
    """Render the Sales Overview dashboard page."""
    render_header(
        title="Sales Overview",
        subtitle="Executive financial performance, monthly sales & profit velocity, and margin analytics",
        record_count=len(df),
        total_count=total_rows
    )

    if df.empty:
        st.warning("⚠️ No data available matching the selected filters. Please adjust your filter criteria in the sidebar.")
        return

    # 1. CORE KPI CALCULATIONS
    total_sales = df['Total_Sales_INR'].sum()
    total_profit = df['Profit_INR'].sum()
    total_orders = len(df)
    total_units = int(df['Quantity'].sum())
    aov = total_sales / total_orders if total_orders > 0 else 0
    profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

    # 2. EXECUTIVE KPI CARDS ROW (6 Metrics)
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        render_kpi_card(
            title="Total Sales",
            value=format_inr(total_sales, compact=True),
            subtitle=f"Full: {format_inr(total_sales, compact=False, decimals=0)}",
            icon="💰",
            variant="orange",
            pill_text="Revenue"
        )

    with col2:
        render_kpi_card(
            title="Total Profit",
            value=format_inr(total_profit, compact=True),
            subtitle=f"Margin: {profit_margin:.1f}%",
            icon="📈",
            variant="blue",
            pill_text="Net Gain"
        )

    with col3:
        render_kpi_card(
            title="Total Orders",
            value=format_count(total_orders),
            subtitle=f"{total_orders/total_rows*100:.1f}% of total" if total_rows > 0 else "",
            icon="🛒",
            variant="teal",
            pill_text="Volume"
        )

    with col4:
        render_kpi_card(
            title="Units Sold",
            value=format_count(total_units),
            subtitle=f"{total_units/total_orders:.1f} units/order" if total_orders > 0 else "",
            icon="📦",
            variant="orange",
            pill_text="Quantity"
        )

    with col5:
        render_kpi_card(
            title="Avg Order Value",
            value=format_inr(aov, compact=False, decimals=0),
            subtitle="Per customer transaction",
            icon="🏷️",
            variant="blue",
            pill_text="AOV"
        )

    with col6:
        render_kpi_card(
            title="Profit Margin",
            value=format_pct(profit_margin, decimals=1),
            subtitle=f"Net return on sales",
            icon="🎯",
            variant="green" if profit_margin >= 20 else "orange",
            pill_text="Healthy" if profit_margin >= 20 else "Watch"
        )

    render_html("<div style='height: 14px;'></div>")

    # 3. MONTHLY SALES AND PROFIT TRENDS
    render_section_header("Monthly Sales & Profit Trajectory", icon="📊")

    # Timeframe selection & chart
    trend_col, summary_col = st.columns([3, 1])

    with trend_col:
        fig_trend = plot_monthly_sales_and_profit(df)
        st.plotly_chart(fig_trend, use_container_width=True)

    with summary_col:
        # Calculate monthly aggregations for summary insights
        monthly_grp = df.groupby('Year_Month').agg(
            Sales=('Total_Sales_INR', 'sum'),
            Profit=('Profit_INR', 'sum'),
            Orders=('Order_ID', 'count')
        ).reset_index()

        if not monthly_grp.empty:
            best_month = monthly_grp.loc[monthly_grp['Sales'].idxmax()]
            avg_monthly_sales = monthly_grp['Sales'].mean()
            avg_monthly_orders = monthly_grp['Orders'].mean()

            highlights_html = f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 18px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
                <div style="font-size: 13px; font-weight: 700; color: #131921; margin-bottom: 12px; border-bottom: 1px solid #EAEDED; padding-bottom: 6px;">
                    ⭐ KEY SALES HIGHLIGHTS
                </div>
                <div style="margin-bottom: 14px;">
                    <span style="font-size: 12px; color: #565959;">Peak Month:</span><br>
                    <b style="font-size: 15px; color: #131921;">{best_month['Year_Month']}</b><br>
                    <span style="font-size: 12px; color: #067D62; font-weight: 600;">{format_inr(best_month['Sales'], compact=True)}</span>
                    <span style="font-size: 11px; color: #565959;">({best_month['Orders']:,} orders)</span>
                </div>
                <div style="margin-bottom: 14px;">
                    <span style="font-size: 12px; color: #565959;">Avg Monthly Run-Rate:</span><br>
                    <b style="font-size: 15px; color: #131921;">{format_inr(avg_monthly_sales, compact=True)}</b><br>
                    <span style="font-size: 11px; color: #565959;">~{int(avg_monthly_orders):,} orders / month</span>
                </div>
                <div style="margin-bottom: 10px;">
                    <span style="font-size: 12px; color: #565959;">Recorded Period:</span><br>
                    <b style="font-size: 13px; color: #131921;">{df['Order_Date'].min().strftime('%d %b %Y')} – {df['Order_Date'].max().strftime('%d %b %Y')}</b>
                </div>
            </div>
            """
            render_html(highlights_html)

    # 4. CATEGORY DISTRIBUTION COMPARISON
    render_section_header("Category Revenue & Profit Share", icon="🛍️")

    cat_col1, cat_col2 = st.columns(2)
    with cat_col1:
        st.plotly_chart(plot_category_sales(df), use_container_width=True)
    with cat_col2:
        st.plotly_chart(plot_category_profit(df), use_container_width=True)

    # 5. MONTH-OVER-MONTH PERFORMANCE TABLE
    with st.expander("📅 View Detailed Monthly Performance Breakdown", expanded=False):
        monthly_table = monthly_grp.copy()
        monthly_table['Margin_%'] = (monthly_table['Profit'] / monthly_table['Sales']) * 100
        monthly_table['MoM_Sales_Growth_%'] = monthly_table['Sales'].pct_change() * 100
        monthly_table['AOV'] = monthly_table['Sales'] / monthly_table['Orders']

        # Format display
        display_table = pd.DataFrame({
            "Month": monthly_table['Year_Month'],
            "Total Sales (INR)": monthly_table['Sales'].apply(lambda x: format_inr(x, compact=False, decimals=2)),
            "Total Profit (INR)": monthly_table['Profit'].apply(lambda x: format_inr(x, compact=False, decimals=2)),
            "Profit Margin": monthly_table['Margin_%'].apply(lambda x: f"{x:.1f}%"),
            "MoM Growth": monthly_table['MoM_Sales_Growth_%'].apply(
                lambda x: "—" if pd.isna(x) else f"{'+' if x>0 else ''}{x:.1f}%"
            ),
            "Orders": monthly_table['Orders'].apply(format_count),
            "Avg Order Value": monthly_table['AOV'].apply(lambda x: format_inr(x, compact=False, decimals=0))
        })
        st.dataframe(display_table, use_container_width=True, hide_index=True)
