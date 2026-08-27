# Indian-style abbreviation (Cr / L) for currency and counts, mirroring
# frontend/src/utils/format.js — used for fallback (non-AI) summary text so
# it doesn't show a long run of digits, and to pre-format the figures handed
# to the AI summary prompt so the model has an abbreviated form to work from.


def format_inr(value, fallback="₹0"):
    n = float(value or 0)
    if not n:
        return fallback
    abs_n = abs(n)
    if abs_n >= 10000000:
        return f"₹{n / 10000000:.1f} Cr"
    if abs_n >= 100000:
        return f"₹{n / 100000:.1f} L"
    return f"₹{n:,.0f}"


def format_count(value, fallback="0"):
    n = float(value or 0)
    if not n:
        return fallback
    abs_n = abs(n)
    if abs_n >= 10000000:
        return f"{n / 10000000:.1f} Cr"
    if abs_n >= 100000:
        return f"{n / 100000:.1f} L"
    if abs_n >= 1000:
        return f"{n / 1000:.1f}K"
    return f"{n:,.0f}"
