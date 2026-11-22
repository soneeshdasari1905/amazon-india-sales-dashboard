"""Order Analytics Page: Fulfillment pipeline, delivery status, return rates, and cancellations."""

import streamlit as st
import pandas as pd
from styles import render_header, render_kpi_card, render_section_header, render_html
from utils.formatting import format_inr, format_count, format_pct
from utils.charts import (
    plot_order_status_distribution,
    plot_category_returns_and_cancellations,
    plot_fulfillment_order_status,
    STATUS_COLORS,
    AMAZON_ORANGE,
    AMAZON_BLUE
)
import plotly.graph_objects as go


def render_order_analytics(df, total_rows):
    """Render the Order Analytics dashboard page."""
    render_header(
        title="Order Analytics",
        subtitle="Operational fulfillment metrics, delivery lifecycle, return rates, and cancellation diagnostics",
        record_count=len(df),
        total_count=total_rows
    )

    if df.empty:
        st.warning("⚠️ No data available matching the selected filters. Please adjust your filter criteria in the sidebar.")
        return

    # 1. CORE STATUS METRICS & RATES
    total_orders = len(df)
    status_counts = df['Order_Status'].value_counts()

    delivered_count = status_counts.get('Delivered', 0)
    shipped_count = status_counts.get('Shipped', 0)
    returned_count = status_counts.get('Returned', 0)
    cancelled_count = status_counts.get('Cancelled', 0)

    delivered_pct = (delivered_count / total_orders) * 100 if total_orders > 0 else 0
    shipped_pct = (shipped_count / total_orders) * 100 if total_orders > 0 else 0
    return_rate = (returned_count / total_orders) * 100 if total_orders > 0 else 0
    cancellation_rate = (cancelled_count / total_orders) * 100 if total_orders > 0 else 0

    # 2. STATUS KPI CARDS (6 Metrics)
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        render_kpi_card(
            title="Delivered Orders",
            value=format_count(delivered_count),
            subtitle=f"{delivered_pct:.1f}% fulfillment rate",
            icon="✅",
            variant="green",
            pill_text="Success"
        )

    with col2:
        render_kpi_card(
            title="Shipped Orders",
            value=format_count(shipped_count),
            subtitle=f"{shipped_pct:.1f}% in-transit",
            icon="🚚",
            variant="blue",
            pill_text="In Transit"
        )

    with col3:
        render_kpi_card(
            title="Returned Orders",
            value=format_count(returned_count),
            subtitle=f"RTO / Reverse pickups",
            icon="🔄",
            variant="orange",
            pill_text="Returns"
        )

    with col4:
        render_kpi_card(
            title="Cancelled Orders",
            value=format_count(cancelled_count),
            subtitle=f"Pre-dispatch drops",
            icon="❌",
            variant="red",
            pill_text="Drop-off"
        )

    with col5:
        render_kpi_card(
            title="Return Rate",
            value=format_pct(return_rate, decimals=2),
            subtitle="Industry benchmark < 6%",
            icon="📉",
            variant="orange" if return_rate <= 6 else "red",
            pill_text="Normal" if return_rate <= 6 else "Elevated"
        )

    with col6:
        render_kpi_card(
            title="Cancellation Rate",
            value=format_pct(cancellation_rate, decimals=2),
            subtitle="Target threshold < 5%",
            icon="⚠️",
            variant="green" if cancellation_rate <= 5 else "red",
            pill_text="Healthy" if cancellation_rate <= 5 else "Action Req."
        )

    render_html("<div style='height: 14px;'></div>")

    # 3. ORDER STATUS BREAKDOWN & FULFILLMENT MATRIX
    render_section_header("Order Lifecycle & Channel Diagnostics", icon="🔄")

    chart_c1, chart_c2 = st.columns(2)
    with chart_c1:
        st.plotly_chart(plot_order_status_distribution(df), use_container_width=True)
    with chart_c2:
        st.plotly_chart(plot_fulfillment_order_status(df), use_container_width=True)

    # 4. CATEGORY-WISE RETURNS & CANCELLATIONS
    render_html("<div style='height: 14px;'></div>")
    render_section_header("Category-wise Returns & Cancellations", icon="📦")

    cat_rc_c1, cat_rc_c2 = st.columns([3, 2])
    with cat_rc_c1:
        st.plotly_chart(plot_category_returns_and_cancellations(df), use_container_width=True)

    with cat_rc_c2:
        # Table of returns and cancellations with rates
        cat_rc = df.groupby('Category').agg(
            Total=('Order_ID', 'count'),
            Returned=('Order_Status', lambda s: (s == 'Returned').sum()),
            Cancelled=('Order_Status', lambda s: (s == 'Cancelled').sum()),
            Delivered=('Order_Status', lambda s: (s == 'Delivered').sum())
        ).reset_index()

        cat_rc['Return_Rate'] = (cat_rc['Returned'] / cat_rc['Total']) * 100
        cat_rc['Cancel_Rate'] = (cat_rc['Cancelled'] / cat_rc['Total']) * 100
        cat_rc = cat_rc.sort_values('Return_Rate', ascending=False)

        render_html("""
        <div style="font-size: 14px; font-weight: 700; color: #131921; margin-bottom: 10px; border-bottom: 2px solid #EAEDED; padding-bottom: 6px;">
            📊 Return & Cancellation Rate by Category
        </div>
        """)

        display_rc = pd.DataFrame({
            'Category': cat_rc['Category'],
            'Total': cat_rc['Total'].apply(format_count),
            'Returned': cat_rc['Returned'].apply(format_count),
            'Return %': cat_rc['Return_Rate'].apply(lambda x: f"{x:.2f}%"),
            'Cancelled': cat_rc['Cancelled'].apply(format_count),
            'Cancel %': cat_rc['Cancel_Rate'].apply(lambda x: f"{x:.2f}%")
        })

        st.dataframe(display_rc, use_container_width=True, hide_index=True)

    # 5. FULFILLMENT EFFICIENCY BENCHMARK TABLE
    render_html("<div style='height: 14px;'></div>")
    render_section_header("Fulfillment Channel Efficiency Analysis", icon="🚚")

    ful_grp = df.groupby('Fulfillment').agg(
        Total_Orders=('Order_ID', 'count'),
        Delivered=('Order_Status', lambda s: (s == 'Delivered').sum()),
        Returned=('Order_Status', lambda s: (s == 'Returned').sum()),
        Cancelled=('Order_Status', lambda s: (s == 'Cancelled').sum()),
        Total_Sales=('Total_Sales_INR', 'sum'),
        Total_Profit=('Profit_INR', 'sum')
    ).reset_index()

    ful_grp['Delivery_Rate'] = (ful_grp['Delivered'] / ful_grp['Total_Orders']) * 100
    ful_grp['Return_Rate'] = (ful_grp['Returned'] / ful_grp['Total_Orders']) * 100
    ful_grp['Cancel_Rate'] = (ful_grp['Cancelled'] / ful_grp['Total_Orders']) * 100
    ful_grp['Profit_Margin'] = (ful_grp['Total_Profit'] / ful_grp['Total_Sales']) * 100

    ful_display = pd.DataFrame({
        'Fulfillment Channel': ful_grp['Fulfillment'],
        'Total Orders': ful_grp['Total_Orders'].apply(format_count),
        'Delivery Rate': ful_grp['Delivery_Rate'].apply(lambda x: f"{x:.1f}%"),
        'Return Rate': ful_grp['Return_Rate'].apply(lambda x: f"{x:.2f}%"),
        'Cancel Rate': ful_grp['Cancel_Rate'].apply(lambda x: f"{x:.2f}%"),
        'Total Sales': ful_grp['Total_Sales'].apply(lambda x: format_inr(x, compact=True)),
        'Total Profit': ful_grp['Total_Profit'].apply(lambda x: format_inr(x, compact=True)),
        'Margin': ful_grp['Profit_Margin'].apply(lambda x: f"{x:.1f}%")
    })

    st.dataframe(ful_display, use_container_width=True, hide_index=True)
