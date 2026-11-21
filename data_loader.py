"""Data loading, validation, cleaning, and preprocessing module."""

import os
import streamlit as st
import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    'Order_ID',
    'Order_Date',
    'Category',
    'Product',
    'Quantity',
    'Unit_Price_INR',
    'Discount_Pct',
    'Total_Sales_INR',
    'Profit_INR',
    'Payment_Method',
    'Fulfillment',
    'Order_Status',
    'Ship_State'
]

DATASET_FILENAME = "Amazon Sales Data India.xlsx"


def find_dataset_path(filename=DATASET_FILENAME):
    """Locate the Excel dataset file in workspace or common directories."""
    candidates = [
        filename,
        os.path.join(".", filename),
        os.path.join("..", filename),
        os.path.join(os.path.dirname(__file__), filename),
        os.path.join(os.getcwd(), filename)
    ]
    for path in candidates:
        if os.path.exists(path):
            return os.path.abspath(path)
    return None


@st.cache_data(show_spinner="Loading Amazon India Sales Dataset...")
def load_and_clean_data(file_path=None):
    """
    Load, validate, and clean the Amazon Sales Data India dataset.
    Returns:
        tuple: (pd.DataFrame, dict with metadata / validation info)
    """
    if file_path is None:
        file_path = find_dataset_path()

    if file_path is None or not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Could not find dataset file '{DATASET_FILENAME}'. "
            "Please ensure it is placed in the project directory."
        )

    # Read Excel file using openpyxl engine
    df = pd.read_excel(file_path, engine="openpyxl")

    # Column name trimming
    df.columns = [str(c).strip() for c in df.columns]

    # Validate required columns
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")

    # Data Cleaning
    # 1. Strip string columns
    str_cols = ['Order_ID', 'Category', 'Product', 'Payment_Method', 'Fulfillment', 'Order_Status', 'Ship_State']
    for c in str_cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()

    # 2. Date conversion and feature engineering
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    df['Year'] = df['Order_Date'].dt.year
    df['Month'] = df['Order_Date'].dt.month
    df['Month_Name'] = df['Order_Date'].dt.strftime('%b')
    df['Year_Month'] = df['Order_Date'].dt.strftime('%Y-%m')
    df['Quarter'] = 'Q' + df['Order_Date'].dt.quarter.astype(str)
    df['Day_Name'] = df['Order_Date'].dt.strftime('%a')

    # 3. Numeric conversions and null safety
    num_cols = ['Quantity', 'Unit_Price_INR', 'Discount_Pct', 'Total_Sales_INR', 'Profit_INR']
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    # 4. Safe Profit Margin Calculation
    # Profit Margin % = (Profit / Total Sales) * 100
    df['Profit_Margin'] = np.where(
        df['Total_Sales_INR'] > 0,
        (df['Profit_INR'] / df['Total_Sales_INR']) * 100,
        0.0
    )

    # 5. Metadata dictionary
    meta = {
        "file_path": file_path,
        "total_rows": len(df),
        "total_cols": len(df.columns),
        "min_date": df['Order_Date'].min(),
        "max_date": df['Order_Date'].max(),
        "categories": sorted(df['Category'].dropna().unique().tolist()),
        "states": sorted(df['Ship_State'].dropna().unique().tolist()),
        "payment_methods": sorted(df['Payment_Method'].dropna().unique().tolist()),
        "fulfillments": sorted(df['Fulfillment'].dropna().unique().tolist()),
        "order_statuses": sorted(df['Order_Status'].dropna().unique().tolist()),
    }

    return df, meta


def filter_dataset(df, date_range=None, categories=None, fulfillments=None, statuses=None, states=None, payment_methods=None):
    """
    Apply global dashboard filters to dataset safely.
    """
    filtered = df.copy()

    # Date range filter
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        if start_date and end_date:
            filtered = filtered[
                (filtered['Order_Date'].dt.date >= start_date) &
                (filtered['Order_Date'].dt.date <= end_date)
            ]

    # Category filter
    if categories and len(categories) > 0 and "All" not in categories:
        filtered = filtered[filtered['Category'].isin(categories)]

    # Fulfillment filter
    if fulfillments and len(fulfillments) > 0 and "All" not in fulfillments:
        filtered = filtered[filtered['Fulfillment'].isin(fulfillments)]

    # Status filter
    if statuses and len(statuses) > 0 and "All" not in statuses:
        filtered = filtered[filtered['Order_Status'].isin(statuses)]

    # State filter
    if states and len(states) > 0 and "All" not in states:
        filtered = filtered[filtered['Ship_State'].isin(states)]

    # Payment method filter
    if payment_methods and len(payment_methods) > 0 and "All" not in payment_methods:
        filtered = filtered[filtered['Payment_Method'].isin(payment_methods)]

    return filtered
