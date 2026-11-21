"""Main application entrypoint for the Amazon India Sales Analytics Dashboard."""

import streamlit as st
import datetime
from data_loader import load_and_clean_data, filter_dataset
from styles import inject_custom_css, AMAZON_ORANGE, AMAZON_DARK_NAVY
from views.sales_overview import render_sales_overview
from views.product_analytics import render_product_analytics
from views.order_analytics import render_order_analytics
from views.payment_geo import render_payment_and_geographic

# 1. STREAMLIT APP CONFIGURATION
st.set_page_config(
    page_title="Amazon India Sales Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INJECT AMAZON CUSTOM CSS
inject_custom_css()


def main():
    # 3. LOAD DATASET
    try:
        raw_df, meta = load_and_clean_data()
    except Exception as e:
        st.error(f"❌ Failed to load dataset: {e}")
        st.info("Please ensure that 'Amazon Sales Data India.xlsx' exists in the project directory.")
        return

    # 4. SIDEBAR NAVIGATION & BRANDING
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 12px 4px 18px 4px; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 18px;">
            <div style="display: flex; align-items: baseline; gap: 6px;">
                <span style="font-size: 28px; font-weight: 800; color: {AMAZON_ORANGE}; letter-spacing: -0.5px;">amazon</span>
                <span style="font-size: 16px; font-weight: 600; color: #FFFFFF;">.in</span>
            </div>
            <div style="font-size: 12px; font-weight: 600; color: #A0AEC0; text-transform: uppercase; letter-spacing: 1px; margin-top: 3px;">
                Sales Analytics Dashboard
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='font-size: 11px; font-weight: 700; color: #A0AEC0; text-transform: uppercase; margin-bottom: 8px;'>Navigation</p>", unsafe_allow_html=True)

        page = st.radio(
            "Select Dashboard View:",
            options=[
                "📊 Sales Overview",
                "📦 Product Analytics",
                "🚚 Order Analytics",
                "💳 Payment & Geographic"
            ],
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 20px 0 16px 0;'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 11px; font-weight: 700; color: #A0AEC0; text-transform: uppercase; margin-bottom: 10px;'>Global Filters</p>", unsafe_allow_html=True)

        # Date Range Filter
        min_date = meta['min_date'].date()
        max_date = meta['max_date'].date()

        date_selection = st.date_input(
            "Order Date Range:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            help="Select start and end dates to filter transactions"
        )

        # Category Filter
        selected_categories = st.multiselect(
            "Product Category:",
            options=meta['categories'],
            default=[],
            placeholder="All Categories"
        )

        # Fulfillment Filter
        selected_fulfillments = st.multiselect(
            "Fulfillment Channel:",
            options=meta['fulfillments'],
            default=[],
            placeholder="All Channels"
        )

        # Order Status Filter
        selected_statuses = st.multiselect(
            "Order Status:",
            options=meta['order_statuses'],
            default=[],
            placeholder="All Statuses"
        )

        # State Filter
        selected_states = st.multiselect(
            "Destination State:",
            options=meta['states'],
            default=[],
            placeholder="All States"
        )

        # Payment Method Filter
        selected_payments = st.multiselect(
            "Payment Method:",
            options=meta['payment_methods'],
            default=[],
            placeholder="All Payment Methods"
        )

        # Reset button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reset All Filters"):
            st.rerun()

        st.markdown(f"""
        <div style="font-size: 11px; color: #718096; margin-top: 24px; padding-top: 14px; border-top: 1px solid rgba(255,255,255,0.1);">
            Dataset: <b>{meta['total_rows']:,} records</b><br>
            Timeline: <b>{min_date.strftime('%b %Y')} – {max_date.strftime('%b %Y')}</b>
        </div>
        """, unsafe_allow_html=True)

    # 5. APPLY FILTERS TO DATASET
    filtered_df = filter_dataset(
        raw_df,
        date_range=date_selection if isinstance(date_selection, (tuple, list)) and len(date_selection) == 2 else None,
        categories=selected_categories,
        fulfillments=selected_fulfillments,
        statuses=selected_statuses,
        states=selected_states,
        payment_methods=selected_payments
    )

    # 6. ROUTE TO SELECTED PAGE
    if page == "📊 Sales Overview":
        render_sales_overview(filtered_df, meta['total_rows'])
    elif page == "📦 Product Analytics":
        render_product_analytics(filtered_df, meta['total_rows'])
    elif page == "🚚 Order Analytics":
        render_order_analytics(filtered_df, meta['total_rows'])
    elif page == "💳 Payment & Geographic":
        render_payment_and_geographic(filtered_df, meta['total_rows'])

    # 7. DASHBOARD FOOTER
    st.markdown("""
    <div class="dash-footer">
        <b>Amazon India Sales Analytics Dashboard</b> &nbsp;•&nbsp; Built with Streamlit, Pandas, Plotly & OpenPyXL &nbsp;•&nbsp; Confidential & Proprietary
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
