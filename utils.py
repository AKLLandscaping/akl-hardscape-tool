import pandas as pd

# Load and clean Excel file
def load_paver_data():
    df = pd.read_excel("Shaw Price 2025 Pavers slabs.xlsx")
    df.columns = df.columns.str.strip()
    df = df[df["Products"].notna()]
    return df

# Calculate material cost
def calculate_material_cost(product_name, sqft, df, margin_override=None):
    df.columns = df.columns.str.strip()
    row = df[df["Products"] == product_name].iloc[0]

    price = float(row["Net"])
    margin = float(margin_override) / 100 if margin_override is not None else float(row["Margin"])
    pallet_qty = float(row["Pallet Qty"]) if row["Pallet Qty"] != "x" else 1
    coverage = float(row["Coverage"])

    unit_price = price * (1 + margin)
    units = sqft / coverage
    total = units * unit_price

    return {
        "unit_price": round(unit_price, 2),
        "units_required": round(units, 2),
        "material_total": round(total, 2),
        "coverage": coverage,
        "pallet_qty": pallet_qty
    }
