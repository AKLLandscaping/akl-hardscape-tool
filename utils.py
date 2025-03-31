import pandas as pd
import math

def load_paver_data():
    df = pd.read_excel("Shaw Price 2025 Pavers slabs.xlsx")
    df.columns = df.columns.str.strip()
    df = df[df.columns[df.columns.str.lower().str.strip() == "products"][0]].notna()
    return pd.read_excel("Shaw Price 2025 Pavers slabs.xlsx", skiprows=0)

def calculate_material_cost(product_name, sqft, df, margin_override=None):
    df.columns = df.columns.str.strip()
    row = df[df["Products"] == product_name].iloc[0]

    price = float(row["Net"])
    margin = float(margin_override) / 100 if margin_override is not None else float(row["Margin"])
    pallet_qty = float(row["Pallet Qty"]) if row["Pallet Qty"] != "x" else 1
    coverage = float(row["Coverage"])
    unit = "SFT"

    if unit == "SFT":
        units = math.ceil(sqft / coverage)
    else:
        units = 1

    unit_price = round(price * (1 + margin), 2)
    material_total = round(units * unit_price, 2)

    return {
        "unit_price": unit_price,
        "units_required": units,
        "material_total": material_total
    }
