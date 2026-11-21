"""Plotly interactive chart builders with Amazon-inspired styling."""

import plotly.express as px
import plotly.graph_objects as go
from utils.formatting import format_inr, format_count, format_pct

# Amazon Theme Palette
AMAZON_ORANGE = "#FF9900"
AMAZON_ORANGE_DARK = "#E67A00"
AMAZON_ORANGE_LIGHT = "#FFB84D"
AMAZON_DARK_NAVY = "#131921"
AMAZON_SQUID_INK = "#232F3E"
AMAZON_BLUE = "#146EB4"
AMAZON_TEAL = "#007185"
AMAZON_GRAY = "#565959"
AMAZON_LIGHT_GRAY = "#EAEDED"
AMAZON_BG = "#FFFFFF"

# Status Colors
STATUS_COLORS = {
    "Delivered": "#067D62",   # Amazon Green
    "Shipped": "#146EB4",     # Amazon Blue
    "Returned": "#FF9900",    # Amazon Orange
    "Cancelled": "#C40000"    # Amazon Crimson
}

# Category Colors
CATEGORY_COLORS = {
    "Apparel & Fashion": "#FF9900",
    "Electronics & Mobiles": "#146EB4",
    "Beauty & Personal Care": "#D84315",
    "Home & Kitchen": "#007185",
    "Pantry & Groceries": "#067D62"
}

# Fulfillment Colors
FULFILLMENT_COLORS = {
    "Amazon (FBA)": "#FF9900",
    "Seller Flex": "#146EB4",
    "Merchant (FBM)": "#7A329F"
}

# Payment Method Colors
PAYMENT_COLORS = {
    "UPI": "#007185",
    "Credit/Debit Card": "#146EB4",
    "Cash on Delivery (COD)": "#FF9900",
    "Net Banking": "#5E35B1",
    "Amazon Pay Later": "#067D62"
}

# Coordinates for India States (for Geo Map visualization)
STATE_COORDINATES = {
    "Maharashtra": {"lat": 19.7515, "lon": 75.7139},
    "Karnataka": {"lat": 15.3173, "lon": 75.7139},
    "Delhi": {"lat": 28.7041, "lon": 77.1025},
    "Tamil Nadu": {"lat": 11.1271, "lon": 78.6569},
    "Uttar Pradesh": {"lat": 26.8467, "lon": 80.9462},
    "Telangana": {"lat": 18.1124, "lon": 79.0193},
    "West Bengal": {"lat": 22.9868, "lon": 87.8550},
    "Gujarat": {"lat": 22.2587, "lon": 71.1924},
    "Kerala": {"lat": 10.8505, "lon": 76.2711},
    "Rajasthan": {"lat": 27.0238, "lon": 74.2179}
}


def apply_amazon_theme(fig, title=None, height=400, show_legend=True):
    """Apply consistent Amazon-inspired layout, typography, and tooltip styling."""
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(size=16, color=AMAZON_DARK_NAVY, family="Segoe UI, -apple-system, sans-serif"),
            x=0.01,
            y=0.96
        ) if title else None,
        paper_bgcolor=AMAZON_BG,
        plot_bgcolor=AMAZON_BG,
        font=dict(family="Segoe UI, -apple-system, sans-serif", color=AMAZON_DARK_NAVY, size=12),
        height=height,
        margin=dict(l=45, r=30, t=55 if title else 25, b=45),
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
            bgcolor="rgba(255, 255, 255, 0.8)"
        ),
        hoverlabel=dict(
            bgcolor=AMAZON_DARK_NAVY,
            font_size=12,
            font_family="Segoe UI, sans-serif",
            font_color="#FFFFFF",
            bordercolor=AMAZON_ORANGE
        )
    )
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="#F0F2F5",
        zeroline=False,
        linecolor="#D5D9D9",
        tickfont=dict(size=11, color=AMAZON_GRAY)
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="#F0F2F5",
        zeroline=False,
        linecolor="#D5D9D9",
        tickfont=dict(size=11, color=AMAZON_GRAY)
    )
    return fig


def plot_monthly_sales_and_profit(df):
    """Dual-axis line & bar chart showing Monthly Sales & Monthly Profit with margins."""
    monthly = df.groupby('Year_Month').agg(
        Total_Sales=('Total_Sales_INR', 'sum'),
        Total_Profit=('Profit_INR', 'sum'),
        Total_Orders=('Order_ID', 'count')
    ).reset_index()

    monthly['Profit_Margin'] = (monthly['Total_Profit'] / monthly['Total_Sales']) * 100
    monthly['Sales_Formatted'] = monthly['Total_Sales'].apply(lambda x: format_inr(x, compact=True))
    monthly['Profit_Formatted'] = monthly['Total_Profit'].apply(lambda x: format_inr(x, compact=True))

    fig = go.Figure()

    # Sales Bar
    fig.add_trace(go.Bar(
        x=monthly['Year_Month'],
        y=monthly['Total_Sales'],
        name="Total Sales",
        marker_color=AMAZON_ORANGE,
        hovertemplate="<b>%{x}</b><br>Sales: %{customdata[0]}<br>Orders: %{customdata[1]}<extra></extra>",
        customdata=list(zip(monthly['Sales_Formatted'], monthly['Total_Orders'].apply(format_count)))
    ))

    # Profit Line
    fig.add_trace(go.Scatter(
        x=monthly['Year_Month'],
        y=monthly['Total_Profit'],
        name="Total Profit",
        mode="lines+markers",
        line=dict(color=AMAZON_BLUE, width=3),
        marker=dict(size=7, color=AMAZON_BLUE, symbol="circle"),
        hovertemplate="<b>%{x}</b><br>Profit: %{customdata[0]}<br>Margin: %{customdata[1]}<extra></extra>",
        customdata=list(zip(monthly['Profit_Formatted'], monthly['Profit_Margin'].apply(lambda x: f"{x:.1f}%"))),
        yaxis="y2"
    ))

    fig.update_layout(
        yaxis=dict(
            title="Total Sales (INR)",
            showgrid=True,
            gridcolor="#F0F2F5"
        ),
        yaxis2=dict(
            title="Total Profit (INR)",
            overlaying="y",
            side="right",
            showgrid=False
        )
    )

    return apply_amazon_theme(fig, title="Monthly Sales & Profit Trends", height=420)


def plot_category_sales(df):
    """Bar chart of category-wise sales."""
    cat_df = df.groupby('Category').agg(
        Sales=('Total_Sales_INR', 'sum'),
        Orders=('Order_ID', 'count')
    ).reset_index().sort_values('Sales', ascending=True)

    cat_df['Sales_Label'] = cat_df['Sales'].apply(lambda x: format_inr(x, compact=True))
    colors = [CATEGORY_COLORS.get(c, AMAZON_ORANGE) for c in cat_df['Category']]

    fig = go.Figure(go.Bar(
        x=cat_df['Sales'],
        y=cat_df['Category'],
        orientation='h',
        marker=dict(color=colors, line=dict(color="#FFFFFF", width=1)),
        text=cat_df['Sales_Label'],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Total Sales: %{text}<br>Orders: %{customdata:,}<extra></extra>",
        customdata=cat_df['Orders']
    ))

    fig.update_layout(
        xaxis=dict(title="Total Sales (INR)"),
        yaxis=dict(title="")
    )
    return apply_amazon_theme(fig, title="Category-wise Sales", height=350, show_legend=False)


def plot_category_profit(df):
    """Bar chart of category-wise profit with margin annotations."""
    cat_df = df.groupby('Category').agg(
        Profit=('Profit_INR', 'sum'),
        Sales=('Total_Sales_INR', 'sum')
    ).reset_index().sort_values('Profit', ascending=True)

    cat_df['Margin'] = (cat_df['Profit'] / cat_df['Sales']) * 100
    cat_df['Profit_Label'] = cat_df['Profit'].apply(lambda x: format_inr(x, compact=True))
    colors = [CATEGORY_COLORS.get(c, AMAZON_BLUE) for c in cat_df['Category']]

    fig = go.Figure(go.Bar(
        x=cat_df['Profit'],
        y=cat_df['Category'],
        orientation='h',
        marker=dict(color=colors, line=dict(color="#FFFFFF", width=1)),
        text=[f"{p} ({m:.1f}%)" for p, m in zip(cat_df['Profit_Label'], cat_df['Margin'])],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Profit: %{customdata[0]}<br>Margin: %{customdata[1]:.1f}%<extra></extra>",
        customdata=list(zip(cat_df['Profit_Label'], cat_df['Margin']))
    ))

    fig.update_layout(
        xaxis=dict(title="Total Profit (INR)"),
        yaxis=dict(title="")
    )
    return apply_amazon_theme(fig, title="Category-wise Profit & Margins", height=350, show_legend=False)


def plot_category_units(df):
    """Donut chart of units sold by category."""
    cat_units = df.groupby('Category')['Quantity'].sum().reset_index()
    colors = [CATEGORY_COLORS.get(c, AMAZON_ORANGE) for c in cat_units['Category']]

    fig = go.Figure(go.Pie(
        labels=cat_units['Category'],
        values=cat_units['Quantity'],
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
        textinfo='label+percent',
        hovertemplate="<b>%{label}</b><br>Units Sold: %{value:,}<br>Share: %{percent}<extra></extra>"
    ))

    fig.update_layout(
        annotations=[dict(text="<b>Units</b>", x=0.5, y=0.5, font_size=15, showarrow=False)]
    )
    return apply_amazon_theme(fig, title="Category-wise Units Sold", height=360, show_legend=True)


def plot_top_10_products(df):
    """Horizontal bar chart for Top 10 products by Sales."""
    prod_df = df.groupby(['Product', 'Category']).agg(
        Sales=('Total_Sales_INR', 'sum'),
        Profit=('Profit_INR', 'sum'),
        Units=('Quantity', 'sum')
    ).reset_index().sort_values('Sales', ascending=True).tail(10)

    prod_df['Margin'] = (prod_df['Profit'] / prod_df['Sales']) * 100
    prod_df['Sales_Label'] = prod_df['Sales'].apply(lambda x: format_inr(x, compact=True))
    colors = [CATEGORY_COLORS.get(c, AMAZON_ORANGE) for c in prod_df['Category']]

    fig = go.Figure(go.Bar(
        x=prod_df['Sales'],
        y=prod_df['Product'],
        orientation='h',
        marker=dict(color=colors, line=dict(color="#FFFFFF", width=1)),
        text=prod_df['Sales_Label'],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Category: %{customdata[0]}<br>Sales: %{text}<br>Profit: %{customdata[1]}<br>Margin: %{customdata[2]:.1f}%<br>Units Sold: %{customdata[3]:,}<extra></extra>",
        customdata=list(zip(
            prod_df['Category'],
            prod_df['Profit'].apply(lambda x: format_inr(x, compact=True)),
            prod_df['Margin'],
            prod_df['Units']
        ))
    ))

    fig.update_layout(
        xaxis=dict(title="Total Sales (INR)"),
        yaxis=dict(title="")
    )
    return apply_amazon_theme(fig, title="Top 10 Products by Sales", height=420, show_legend=False)


def plot_order_status_distribution(df):
    """Donut chart for order status breakdown."""
    status_df = df['Order_Status'].value_counts().reset_index()
    status_df.columns = ['Status', 'Count']
    colors = [STATUS_COLORS.get(s, AMAZON_GRAY) for s in status_df['Status']]

    fig = go.Figure(go.Pie(
        labels=status_df['Status'],
        values=status_df['Count'],
        hole=0.6,
        marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
        textinfo='label+percent',
        hovertemplate="<b>%{label}</b><br>Orders: %{value:,}<br>Share: %{percent}<extra></extra>"
    ))

    total_orders = status_df['Count'].sum()
    fig.update_layout(
        annotations=[dict(text=f"<b>{format_count(total_orders)}</b><br><span style='font-size:11px;color:#565959'>Orders</span>", x=0.5, y=0.5, font_size=15, showarrow=False)]
    )
    return apply_amazon_theme(fig, title="Order Status Breakdown", height=360, show_legend=True)


def plot_category_returns_and_cancellations(df):
    """Grouped bar chart for returns and cancellations across categories."""
    grouped = df.groupby(['Category', 'Order_Status'])['Order_ID'].count().unstack(fill_value=0).reset_index()

    # Ensure required columns exist
    for col in ['Delivered', 'Shipped', 'Returned', 'Cancelled']:
        if col not in grouped.columns:
            grouped[col] = 0

    grouped['Total'] = grouped['Delivered'] + grouped['Shipped'] + grouped['Returned'] + grouped['Cancelled']
    grouped['Return_Rate'] = (grouped['Returned'] / grouped['Total']) * 100
    grouped['Cancel_Rate'] = (grouped['Cancelled'] / grouped['Total']) * 100

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=grouped['Category'],
        y=grouped['Returned'],
        name="Returned Orders",
        marker_color=STATUS_COLORS["Returned"],
        hovertemplate="<b>%{x}</b><br>Returned: %{y:,}<br>Return Rate: %{customdata:.1f}%<extra></extra>",
        customdata=grouped['Return_Rate']
    ))

    fig.add_trace(go.Bar(
        x=grouped['Category'],
        y=grouped['Cancelled'],
        name="Cancelled Orders",
        marker_color=STATUS_COLORS["Cancelled"],
        hovertemplate="<b>%{x}</b><br>Cancelled: %{y:,}<br>Cancel Rate: %{customdata:.1f}%<extra></extra>",
        customdata=grouped['Cancel_Rate']
    ))

    fig.update_layout(
        barmode='group',
        xaxis=dict(title="Category"),
        yaxis=dict(title="Order Count")
    )
    return apply_amazon_theme(fig, title="Returns & Cancellations by Category", height=380)


def plot_fulfillment_order_status(df):
    """Stacked bar chart showing Order Status breakdown by Fulfillment channel."""
    matrix = df.groupby(['Fulfillment', 'Order_Status'])['Order_ID'].count().unstack(fill_value=0).reset_index()

    fig = go.Figure()
    for status in ['Delivered', 'Shipped', 'Returned', 'Cancelled']:
        if status in matrix.columns:
            fig.add_trace(go.Bar(
                x=matrix['Fulfillment'],
                y=matrix[status],
                name=status,
                marker_color=STATUS_COLORS.get(status, AMAZON_GRAY),
                hovertemplate=f"<b>%{{x}}</b><br>{status}: %{{y:,}}<extra></extra>"
            ))

    fig.update_layout(
        barmode='stack',
        xaxis=dict(title="Fulfillment Method"),
        yaxis=dict(title="Orders")
    )
    return apply_amazon_theme(fig, title="Fulfillment Channel vs Order Status", height=380)


def plot_payment_method_sales_profit(df):
    """Bar chart comparing Sales and Profit by Payment Method."""
    pay_df = df.groupby('Payment_Method').agg(
        Sales=('Total_Sales_INR', 'sum'),
        Profit=('Profit_INR', 'sum'),
        Orders=('Order_ID', 'count')
    ).reset_index().sort_values('Sales', ascending=False)

    pay_df['Margin'] = (pay_df['Profit'] / pay_df['Sales']) * 100
    pay_df['Sales_Fmt'] = pay_df['Sales'].apply(lambda x: format_inr(x, compact=True))
    pay_df['Profit_Fmt'] = pay_df['Profit'].apply(lambda x: format_inr(x, compact=True))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=pay_df['Payment_Method'],
        y=pay_df['Sales'],
        name="Sales",
        marker_color=AMAZON_ORANGE,
        hovertemplate="<b>%{x}</b><br>Sales: %{customdata[0]}<br>Orders: %{customdata[1]:,}<extra></extra>",
        customdata=list(zip(pay_df['Sales_Fmt'], pay_df['Orders']))
    ))

    fig.add_trace(go.Bar(
        x=pay_df['Payment_Method'],
        y=pay_df['Profit'],
        name="Profit",
        marker_color=AMAZON_BLUE,
        hovertemplate="<b>%{x}</b><br>Profit: %{customdata[0]}<br>Margin: %{customdata[1]:.1f}%<extra></extra>",
        customdata=list(zip(pay_df['Profit_Fmt'], pay_df['Margin']))
    ))

    fig.update_layout(
        barmode='group',
        xaxis=dict(title="Payment Method"),
        yaxis=dict(title="Amount (INR)")
    )
    return apply_amazon_theme(fig, title="Sales & Profit by Payment Method", height=380)


def plot_fulfillment_sales_profit(df):
    """Bar chart comparing Sales and Profit by Fulfilment Method."""
    ful_df = df.groupby('Fulfillment').agg(
        Sales=('Total_Sales_INR', 'sum'),
        Profit=('Profit_INR', 'sum'),
        Orders=('Order_ID', 'count')
    ).reset_index().sort_values('Sales', ascending=False)

    ful_df['Margin'] = (ful_df['Profit'] / ful_df['Sales']) * 100
    ful_df['Sales_Fmt'] = ful_df['Sales'].apply(lambda x: format_inr(x, compact=True))
    ful_df['Profit_Fmt'] = ful_df['Profit'].apply(lambda x: format_inr(x, compact=True))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=ful_df['Fulfillment'],
        y=ful_df['Sales'],
        name="Sales",
        marker_color=AMAZON_ORANGE,
        hovertemplate="<b>%{x}</b><br>Sales: %{customdata[0]}<br>Orders: %{customdata[1]:,}<extra></extra>",
        customdata=list(zip(ful_df['Sales_Fmt'], ful_df['Orders']))
    ))

    fig.add_trace(go.Bar(
        x=ful_df['Fulfillment'],
        y=ful_df['Profit'],
        name="Profit",
        marker_color=AMAZON_BLUE,
        hovertemplate="<b>%{x}</b><br>Profit: %{customdata[0]}<br>Margin: %{customdata[1]:.1f}%<extra></extra>",
        customdata=list(zip(ful_df['Profit_Fmt'], ful_df['Margin']))
    ))

    fig.update_layout(
        barmode='group',
        xaxis=dict(title="Fulfilment Method"),
        yaxis=dict(title="Amount (INR)")
    )
    return apply_amazon_theme(fig, title="Sales & Profit by Fulfilment Method", height=380)


def plot_state_sales(df):
    """Horizontal ranked bar chart of Sales by State."""
    state_df = df.groupby('Ship_State').agg(
        Sales=('Total_Sales_INR', 'sum'),
        Orders=('Order_ID', 'count')
    ).reset_index().sort_values('Sales', ascending=True)

    state_df['Sales_Fmt'] = state_df['Sales'].apply(lambda x: format_inr(x, compact=True))

    fig = go.Figure(go.Bar(
        x=state_df['Sales'],
        y=state_df['Ship_State'],
        orientation='h',
        marker=dict(color=AMAZON_ORANGE, line=dict(color="#FFFFFF", width=1)),
        text=state_df['Sales_Fmt'],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Sales: %{text}<br>Orders: %{customdata:,}<extra></extra>",
        customdata=state_df['Orders']
    ))

    fig.update_layout(
        xaxis=dict(title="Total Sales (INR)"),
        yaxis=dict(title="")
    )
    return apply_amazon_theme(fig, title="State-wise Sales", height=420, show_legend=False)


def plot_state_profit(df):
    """Horizontal ranked bar chart of Profit by State with margin annotations."""
    state_df = df.groupby('Ship_State').agg(
        Profit=('Profit_INR', 'sum'),
        Sales=('Total_Sales_INR', 'sum')
    ).reset_index().sort_values('Profit', ascending=True)

    state_df['Margin'] = (state_df['Profit'] / state_df['Sales']) * 100
    state_df['Profit_Fmt'] = state_df['Profit'].apply(lambda x: format_inr(x, compact=True))

    fig = go.Figure(go.Bar(
        x=state_df['Profit'],
        y=state_df['Ship_State'],
        orientation='h',
        marker=dict(color=AMAZON_BLUE, line=dict(color="#FFFFFF", width=1)),
        text=[f"{p} ({m:.1f}%)" for p, m in zip(state_df['Profit_Fmt'], state_df['Margin'])],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Profit: %{customdata[0]}<br>Margin: %{customdata[1]:.1f}%<extra></extra>",
        customdata=list(zip(state_df['Profit_Fmt'], state_df['Margin']))
    ))

    fig.update_layout(
        xaxis=dict(title="Total Profit (INR)"),
        yaxis=dict(title="")
    )
    return apply_amazon_theme(fig, title="State-wise Profit & Margins", height=420, show_legend=False)


def plot_state_orders(df):
    """Bar chart of Orders by State."""
    state_df = df.groupby('Ship_State')['Order_ID'].count().reset_index()
    state_df.columns = ['Ship_State', 'Orders']
    state_df = state_df.sort_values('Orders', ascending=True)

    fig = go.Figure(go.Bar(
        x=state_df['Orders'],
        y=state_df['Ship_State'],
        orientation='h',
        marker=dict(color=AMAZON_TEAL, line=dict(color="#FFFFFF", width=1)),
        text=state_df['Orders'].apply(format_count),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Total Orders: %{text}<extra></extra>"
    ))

    fig.update_layout(
        xaxis=dict(title="Total Orders"),
        yaxis=dict(title="")
    )
    return apply_amazon_theme(fig, title="State-wise Orders", height=420, show_legend=False)


def plot_state_geo_scatter(df):
    """Interactive Scatter Geo bubble map of India showing sales and orders."""
    state_agg = df.groupby('Ship_State').agg(
        Sales=('Total_Sales_INR', 'sum'),
        Profit=('Profit_INR', 'sum'),
        Orders=('Order_ID', 'count')
    ).reset_index()

    # Add lat / lon
    state_agg['lat'] = state_agg['Ship_State'].apply(lambda s: STATE_COORDINATES.get(s, {}).get('lat', None))
    state_agg['lon'] = state_agg['Ship_State'].apply(lambda s: STATE_COORDINATES.get(s, {}).get('lon', None))
    state_agg = state_agg.dropna(subset=['lat', 'lon'])

    state_agg['Sales_Fmt'] = state_agg['Sales'].apply(lambda x: format_inr(x, compact=True))
    state_agg['Profit_Fmt'] = state_agg['Profit'].apply(lambda x: format_inr(x, compact=True))
    state_agg['Margin'] = (state_agg['Profit'] / state_agg['Sales']) * 100

    # Bubble size scaling
    max_sales = state_agg['Sales'].max()
    state_agg['size'] = 18 + (state_agg['Sales'] / max_sales) * 35

    fig = go.Figure()

    fig.add_trace(go.Scattergeo(
        lon=state_agg['lon'],
        lat=state_agg['lat'],
        text=state_agg['Ship_State'],
        mode='markers+text',
        textposition='top center',
        textfont=dict(size=10, color=AMAZON_DARK_NAVY, family="Segoe UI, sans-serif"),
        marker=dict(
            size=state_agg['size'],
            color=state_agg['Sales'],
            colorscale=[[0, "#FFE0B2"], [0.5, "#FF9900"], [1.0, "#E65100"]],
            cmin=state_agg['Sales'].min(),
            cmax=state_agg['Sales'].max(),
            colorbar=dict(
                title=dict(text="Sales (INR)", font=dict(size=11)),
                thickness=12,
                len=0.75,
                y=0.5
            ),
            line=dict(width=1.5, color=AMAZON_DARK_NAVY),
            opacity=0.88
        ),
        hovertemplate="<b>%{text}</b><br>Sales: %{customdata[0]}<br>Profit: %{customdata[1]} (Margin: %{customdata[2]:.1f}%)<br>Orders: %{customdata[3]:,}<extra></extra>",
        customdata=list(zip(
            state_agg['Sales_Fmt'],
            state_agg['Profit_Fmt'],
            state_agg['Margin'],
            state_agg['Orders']
        ))
    ))

    fig.update_layout(
        geo=dict(
            scope='asia',
            center=dict(lat=22.0, lon=80.0),
            projection_scale=3.8,
            showland=True,
            landcolor="#F7F8FA",
            subunitcolor="#D5D9D9",
            countrycolor="#999999",
            countrywidth=1,
            showocean=False,
            showcountries=True
        )
    )

    return apply_amazon_theme(fig, title="India Geographic Sales & Density Map", height=460, show_legend=False)
