# 🛒 Amazon India Sales Analytics Dashboard

A modern, executive-grade sales intelligence and operations analytics dashboard tailored for Amazon India marketplace data. Built with **Streamlit**, **Pandas**, **Plotly**, and **OpenPyXL**, featuring an authentic Amazon-inspired UI theme (Dark Navy, Squid Ink, Amazon Orange, and Amazon Blue).

---

## 🚀 Quick Start

### 1. Requirements & Prerequisites
- Python 3.10+ (Recommended: Python 3.12)
- Dependencies installed from `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Launching the Dashboard

#### Option A: One-Click Batch Script (Windows)
Double-click `run_dashboard.bat` or run:
```cmd
.\run_dashboard.bat
```

#### Option B: Standard Streamlit CLI
Run using the designated Python interpreter:
```bash
streamlit run app.py
```
Or with explicit Python path:
```bash
python -m streamlit run app.py
```

The application will start and automatically open in your default web browser at **`http://localhost:8501`**.

---

## 📊 Dashboard Modules & Feature Breakdown

### 1. 📊 Sales Overview
- **Executive KPI Cards**:
  - **Total Sales**: Formatted in Indian Rupee notation (₹ Cr / ₹ Lakh).
  - **Total Profit**: Net earnings and aggregate profit velocity.
  - **Total Orders**: Total transaction count and percentage of catalog volume.
  - **Units Sold**: Total volume of items dispatched with average units/order.
  - **Average Order Value (AOV)**: Revenue per customer order.
  - **Profit Margin (%)**: Overall net margin health indicator.
- **Monthly Trajectory Chart**: Dual-axis Plotly visualization comparing monthly sales run-rate against profit margins with interactive hover tooltips.
- **Key Performance Highlights**: Peak revenue months, average monthly order run-rate, and date span.
- **Category Share Comparisons**: Comparative bar charts for revenue and profit across product categories.
- **Month-over-Month (MoM) Growth Table**: Detailed tabular breakdown with MoM growth rates, orders, and AOVs.

---

### 2. 📦 Product Analytics
- **Category Performance Diagnostics**:
  - **Category-wise Sales**: Ranked horizontal bars with revenue badges.
  - **Category-wise Profit**: Net profit breakdown with category margins.
  - **Category-wise Units Sold**: Interactive donut visualization of product quantity share.
  - **Category Metrics Matrix**: Tabular scorecard of sales, profits, margins, and units.
- **Top 10 Products by Sales**: Ranked horizontal bar chart featuring top revenue-generating SKUs, margins, and sales volume.
- **Catalog Deep Dive & Drill-Down**: Interactive category selector to explore individual product prices, discounts, and units.
- **Export**: One-click **CSV export** for product performance records.

---

### 3. 🚚 Order Analytics
- **Order Lifecycle KPIs**:
  - **Delivered Orders**: Count and % fulfillment success rate.
  - **Shipped Orders**: In-transit order volume.
  - **Returned Orders**: Customer returns and reverse pickups.
  - **Cancelled Orders**: Pre-dispatch order drops.
  - **Return Rate (%)**: Percentage of returned orders vs total orders.
  - **Cancellation Rate (%)**: Percentage of cancelled orders vs total orders.
- **Visual Diagnostics**:
  - **Order Status Breakdown**: Styled donut chart with Amazon operational status palette.
  - **Fulfillment Channel vs Order Status**: Stacked bar comparison across Amazon (FBA), Seller Flex, and Merchant (FBM).
  - **Category-wise Returns & Cancellations**: Grouped bar chart identifying high-return categories.
  - **Fulfillment Efficiency Benchmark**: Tabular matrix comparing delivery rates, return rates, cancellation rates, and margins per fulfillment channel.

---

### 4. 💳 Payment & Geographic Analytics
- **Payment Method Analytics**:
  - Comparative Sales and Profit by payment mode (UPI, Credit/Debit Card, Cash on Delivery, Net Banking, Amazon Pay Later).
  - Detailed payment performance table showing transactions, AOV, and average units per order.
- **Fulfilment Method Analytics**:
  - Comparative analysis of Sales and Profit across Amazon (FBA), Seller Flex, and Merchant (FBM).
- **State-wise Geographic Analytics**:
  - **India Geographic Bubble Map**: Interactive Plotly map with state coordinates, sales heat intensity, and order density.
  - **State-wise Sales**: Ranked horizontal bar chart.
  - **State-wise Profit**: State profit rankings with net margin labels.
  - **State-wise Orders**: Order volume distribution across destination states.
  - **State Scorecard Table**: Comprehensive metrics table with regional contribution percentages and AOVs.

---

## 🛠️ Global Filters (Sidebar)

Every page dynamically respects the global filters configured in the sidebar:
1. **Order Date Range**: Interactive date picker with start and end dates.
2. **Product Category**: Multi-select filter with options to isolate specific categories.
3. **Fulfillment Channel**: Filter by Amazon (FBA), Seller Flex, or Merchant (FBM).
4. **Order Status**: Filter by Delivered, Shipped, Returned, or Cancelled.
5. **Destination State**: Filter by customer shipping state.
6. **Payment Method**: Filter by customer payment type.
7. **Reset All Filters**: Instant one-click filter reset.

---

## 📁 Project Structure

```
Amazon_India_Sales_Dashboard/
│
├── app.py                     # Main application entrypoint & sidebar router
├── data_loader.py             # Excel data loader, validator, cleaner & cacher
├── styles.py                  # Amazon custom CSS & KPI card HTML builders
├── requirements.txt           # Project dependencies
├── run_dashboard.bat          # One-click Windows launcher
├── README.md                  # Complete documentation
│
├── views/                     # Dashboard view modules
│   ├── __init__.py
│   ├── sales_overview.py      # Page 1: Sales Overview
│   ├── product_analytics.py   # Page 2: Product Analytics
│   ├── order_analytics.py     # Page 3: Order Analytics
│   └── payment_geo.py         # Page 4: Payment & Geographic Analytics
│
├── utils/                     # Helper utilities
│   ├── __init__.py
│   ├── formatting.py          # Indian Rupee (₹ Cr, ₹ L) & percentage formatting
│   └── charts.py              # Plotly chart builders with Amazon color palette
│
├── .streamlit/                # Streamlit configuration
│   └── config.toml            # Amazon theme configuration
│
└── Amazon Sales Data India.xlsx  # Source Excel dataset
```

---

## 📐 KPI Calculation Reference

| Metric | Formula |
| :--- | :--- |
| **Total Sales** | `∑ Total_Sales_INR` |
| **Total Profit** | `∑ Profit_INR` |
| **Total Orders** | `Count(Order_ID)` |
| **Total Units Sold** | `∑ Quantity` |
| **Average Order Value (AOV)** | `Total Sales / Total Orders` |
| **Profit Margin %** | `(Total Profit / Total Sales) * 100` |
| **Delivered Rate %** | `(Delivered Orders / Total Orders) * 100` |
| **Return Rate %** | `(Returned Orders / Total Orders) * 100` |
| **Cancellation Rate %** | `(Cancelled Orders / Total Orders) * 100` |

---

## 🎨 Theme & Palette Reference

- **Dark Navy**: `#131921` (Amazon Core)
- **Squid Ink**: `#232F3E` (Amazon Navigation)
- **Amazon Orange**: `#FF9900` (Call-to-Action & Accents)
- **Amazon Blue**: `#146EB4` (Secondary Highlights & Links)
- **Amazon Teal**: `#007185` (Informational Accents)
- ---

## 🚀 Live Dashboard

The Amazon India Sales Analytics Dashboard is deployed using Streamlit Community Cloud.

### 🌐 [Click Here to Open the Live Dashboard](https://amazon-india-sales-dashboard-o8ywwm7fvgoazveypkaaapp.streamlit.app/)

### Dashboard Features

- 📊 Overall Sales & Profit Performance
- 📦 Category & Product Analytics
- 🚚 Order Status & Revenue Analysis
- 💳 Payment Method Analysis
- 🌍 Geographic Performance Analysis

### Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- OpenPyXL

**Deployment:** Streamlit Community Cloud

**Repository:** [GitHub Source Code](https://github.com/soneeshdasari1905/amazon-india-sales-dashboard)
- **Delivered Green**: `#067D62` (Success)
- **Cancelled Red**: `#C40000` (Error)
