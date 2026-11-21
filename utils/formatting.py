"""Formatting utilities for Indian currency, numbers, and percentages."""

def format_inr(val, compact=True, decimals=2):
    """
    Format a numeric value into Indian Rupee representation.
    If compact=True:
        >= 1,00,00,000 -> ₹X.XX Cr
        >= 1,00,000    -> ₹X.XX L
        >= 1,000       -> ₹X.XX K
        < 1,000        -> ₹X.XX
    If compact=False:
        Full Indian comma-separated format (e.g., ₹1,55,78,989.39)
    """
    if val is None:
        return "₹0.00"
    try:
        val = float(val)
    except (ValueError, TypeError):
        return "₹0.00"

    is_negative = val < 0
    abs_val = abs(val)

    if compact:
        if abs_val >= 10_000_000:
            formatted = f"₹{abs_val / 10_000_000:.{decimals}f} Cr"
        elif abs_val >= 100_000:
            formatted = f"₹{abs_val / 100_000:.{decimals}f} L"
        elif abs_val >= 1_000:
            formatted = f"₹{abs_val / 1_000:.{decimals}f} K"
        else:
            formatted = f"₹{abs_val:.{decimals}f}"
    else:
        formatted = f"₹{indian_number_format(abs_val, decimals=decimals)}"

    return f"-{formatted}" if is_negative else formatted


def indian_number_format(val, decimals=2):
    """
    Format a number in Indian Numbering System (e.g., 12,34,56,789.00).
    """
    try:
        val = float(val)
    except (ValueError, TypeError):
        return "0"

    parts = f"{val:.{decimals}f}".split(".")
    integer_part = parts[0]
    decimal_part = parts[1] if len(parts) > 1 and decimals > 0 else ""

    if len(integer_part) <= 3:
        formatted_int = integer_part
    else:
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]
        groups = []
        while len(remaining) > 2:
            groups.append(remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.append(remaining)
        groups.reverse()
        formatted_int = ",".join(groups) + "," + last_three

    if decimal_part:
        return f"{formatted_int}.{decimal_part}"
    return formatted_int


def format_count(val):
    """Format an integer count with Indian grouping or standard comma."""
    try:
        val = int(round(float(val)))
        return f"{val:,}"
    except (ValueError, TypeError):
        return "0"


def format_pct(val, decimals=1, include_sign=False):
    """Format a percentage value."""
    try:
        val = float(val)
        prefix = "+" if include_sign and val > 0 else ""
        return f"{prefix}{val:.{decimals}f}%"
    except (ValueError, TypeError):
        return "0.0%"
