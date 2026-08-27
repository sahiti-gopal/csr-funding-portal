// Indian-style abbreviation (Cr / L) for currency and counts, so a large
// number never renders as an unbroken string of digits that overflows a
// narrow card/tile/table cell. Below 1 lakh, values are shown in full
// (with comma grouping) since they're short enough not to need abbreviating.

export function formatCurrency(value, { fallback = "₹0" } = {}) {
  const n = Number(value);
  if (!n) return fallback;
  const abs = Math.abs(n);
  if (abs >= 10000000) return `₹${(n / 10000000).toFixed(1)} Cr`;
  if (abs >= 100000) return `₹${(n / 100000).toFixed(1)} L`;
  return `₹${n.toLocaleString("en-IN")}`;
}

export function formatCount(value, { fallback = "0" } = {}) {
  const n = Number(value);
  if (!n) return fallback;
  const abs = Math.abs(n);
  if (abs >= 10000000) return `${(n / 10000000).toFixed(1)} Cr`;
  if (abs >= 100000) return `${(n / 100000).toFixed(1)} L`;
  if (abs >= 1000) return `${(n / 1000).toFixed(1)}K`;
  return n.toLocaleString("en-IN");
}
