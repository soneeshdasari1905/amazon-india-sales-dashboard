"""Payment and Geographic Analytics Page: Payment preferences, fulfillment share, and state-wise metrics."""

import streamlit as st
import pandas as pd
from styles import render_header, render_kpi_card, render_section_header
from utils.formatting import format_inr, format_count, format_pct
from utils.charts import (
    plot_payment_method_sales_profit,
    plot_fulfillment_sales_profit,
    plot_state_sales,
    plot_state_profit,
    plot_state_orders,
    plot_state_geo_scatter,
    AMAZON_ORANGE,
    AMAZON_BLUE
)
import plotly.graph_objects as go


def render_payment_and_geographic(df, total_rows):
    """Render the Payment & Geographic Analytics dashboard page."""
    render_header(
        title="Payment & Geographic Analytics",
        subtitle="Regional penetration across India, state profit margins, and payment method adoption",
        record_count=len(df),
        total_count=total_rows
    )

    if df.empty:
        st.warning("⚠️ No data available matching the selected filters. Please adjust your filter criteria in the sidebar.")
        return

    # 1. SUMMARY KPIS
    state_agg = df.groupby('Ship_State').agg(
        Sales=('Total_Sales_INR', 'sum'),
        Profit=('Profit_INR', 'sum'),
        Orders=('Order_ID', 'count')
    ).reset_index()

    top_state = state_agg.loc[state_agg['Sales'].idxmax()]
    pay_agg = df.groupby('Payment_Method').agg(
        Sales=('Total_Sales_INR', 'sum'),
        Orders=('Order_ID', 'count')
    ).reset_index()
    top_payment = pay_agg.loc[pay_agg['Sales'].idxmax()]
    ful_agg = df.groupby('Fulfillment')['Total_Sales_INR'].sum().reset_index()
    top_fulfillment = ful_agg.loc[ful_agg['Total_Sales_INR'].idxmax()]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card(
            title="Top Revenue State",
            value=top_state['Ship_State'],
            subtitle=f"{format_inr(top_state['Sales'], compact=True)} ({top_state['Orders']:,} orders)",
            icon="📍",
            variant="orange",
            pill_text="No. 1 State"
        )
    with col2:
        render_kpi_card(
            title="Leading Payment Mode",
            value=top_payment['Payment_Method'],
            subtitle=f"{format_inr(top_payment['Sales'], compact=True)} ({top_payment['Orders']:,} orders)",
            icon="💳",
            variant="teal",
            pill_text="Preferred"
        )
    with col3:
        render_kpi_card(
            title="Dominant Fulfillment",
            value=top_fulfillment['Fulfillment'],
            subtitle=f"{format_inr(top_fulfillment['Total_Sales_INR'], compact=True)} shipped",
            icon="📦",
            variant="blue",
            pill_text="Prime Velocity"
        )
    with col4:
        render_kpi_card(
            title="Active Indian States",
            value=f"{df['Ship_State'].nunique()} States",
            subtitle=f"Full pan-India logistics reach",
            icon="🗺️",
            variant="green",
            pill_text="Coverage"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. STATE-WISE GEOGRAPHIC ANALYTICS
    render_section_header("State-wise Geographic Performance", icon="🗺️")

    map_c1, map_c2 = st.columns([3, 2])
    with map_c1:
        st.plotly_chart(plot_state_geo_scatter(df), use_container_width=True)
    with map_c2:
        st.plotly_chart(plot_state_sales(df), use_container_width=True)

    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        st.plotly_chart(plot_state_profit(df), use_container_width=True)
    with row2_c2:
        st.plotly_chart(plot_state_orders(df), use_container_width=True)

    # 3. STATE PERFORMANCE SCORECARD TABLE
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📊 View Complete State Performance Scorecard", expanded=False):
        state_table = state_agg.sort_values('Sales', ascending=False).copy()
        state_table['Profit_Margin_%'] = (state_table['Profit'] / state_table['Sales']) * 100
        state_table['Avg_Order_Value'] = state_table['Sales'] / state_table['Orders']
        state_table['Sales_Share_%'] = (state_table['Sales'] / df['Total_Sales_INR'].sum()) * 100

        display_state_table = pd.DataFrame({
            "State": state_table['Ship_State'],
            "Total Sales (INR)": state_table['Sales'].apply(lambda x: format_inr(x, compact=False, decimals=2)),
            "Total Profit (INR)": state_table['Profit'].apply(lambda x: format_inr(x, compact=False, decimals=2)),
            "Profit Margin": state_table['Profit_Margin_%'].apply(lambda x: f"{x:.1f}%"),
            "Total Orders": state_table['Orders'].apply(format_count),
            "Avg Order Value": state_table['Avg_Order_Value'].apply(lambda x: format_inr(x, compact=False, decimals=0)),
            "National Share": state_table['Sales_Share_%'].apply(lambda x: f"{x:.1f}%")
        })
        st.dataframe(display_state_table, use_container_width=True, hide_index=True)

    # 4. PAYMENT & FULFILLMENT METHOD ANALYTICS
    st.markdown("<br>", unsafe_allow_html=True)
    render_section_header("Payment & Fulfillment Method Insights", icon="💳")

    pay_col, ful_col = st.columns(2)
    with pay_col:
        st.plotly_chart(plot_payment_method_sales_profit(df), use_container_width=True)
    with ful_col:
        st.plotly_chart(plot_fulfillment_sales_profit(df), use_container_width=True)

    # 5. DETAILED PAYMENT BREAKDOWN TABLE
    st.markdown("<br>", unsafe_allow_html=True)
    pay_table_data = df.groupby('Payment_Method').agg(
        Total_Sales=('Total_Sales_INR', 'sum'),
        Total_Profit=('Profit_INR', 'sum'),
        Orders=('Order_ID', 'count'),
        Avg_Units=('Quantity', 'mean')
    ).reset_index().sort_values('Total_Sales', ascending=False)

    pay_table_data['Profit_Margin'] = (pay_table_data['Total_Profit'] / pay_table_data['Total_Sales']) * 100
    pay_table_data['AOV'] = pay_table_data['Total_Sales'] / pay_table_data['Orders']

    display_pay_table = pd.DataFrame({
        "Payment Method": pay_table_data['Payment_Method'],
        "Total Sales (INR)": pay_table_data['Total_Sales'].apply(lambda x: format_inr(x, compact=False, decimals=2)),
        "Total Profit (INR)": pay_table_data['Total_Profit'].apply(lambda x: format_inr(x, compact=False, decimals=2)),
        "Profit Margin": pay_table_data['Profit_Margin'].apply(lambda x: f"{x:.1f}%"),
        "Orders": pay_table_data['Orders'].apply(format_count),
        "Avg Order Value": pay_table_data['AOV'].apply(lambda x: format_inr(x, compact=False, decimals=0)),
        "Avg Units/Order": pay_table_data['Avg_Units'].apply(lambda x: f"{x:.2f}")
    })

    st.dataframe(display_pay_table, use_container_width=True, hide_index=True)
