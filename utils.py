import pandas as pd
import math

# Load and clean Excel file
def load_clean_excel(path):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()
    return df[df["Products"].notna()]

# Load Paver Data
def load_paver_data():
    return load_clean_excel("Shaw Price 2025 Pavers slabs.xlsx")

# Material Calculation
def calculate_material_cost(product_name, sqft, df, margin_override=None):
    df.columns = df.columns.str.strip()
    row = df[df["Products"] == product_name].iloc[0]

    price = float(row["Net"])
    margin = float(margin_override) / 100 if margin_override is not None else float(row["Margin"])
    pallet_qty = float(row["Pallet Qty"])
    coverage = float(row["Coverage"])
    unit = "SQFT"

    units_required = math.ceil(sqft / coverage)
    total_price_per_unit = round(price * (1 + margin), 2)
    material_total = round(total_price_per_unit * units_required, 2)

    return {
        "unit_price": total_price_per_unit,
        "units_required": units_required,
        "material_total": material_total
    }
