import pandas as pd
import math

# Load and clean Excel files
def load_clean_excel(path):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()
    df = df[df["Products"].notna()]
    return df

def load_paver_data():
    return load_clean_excel("Shaw Price 2025 Pavers slabs.xlsx")

# Material cost
def calculate_material_cost(product_name, sqft, df, margin_override=None):
    df.columns = df.columns.str.strip()
    row = df[df["Products"] == product_name].iloc[0]

    price = float(row["Net"])
    margin = float(margin_override) / 100 if margin_override is not None else float(row["Margin"])
    coverage = float(row["Coverage"])

    units = sqft / coverage
    unit_cost = price * (1 + margin)
    material_total = unit_cost * units

    return {
        "price_per_unit": round(unit_cost, 2),
        "units_required": math.ceil(units),
        "material_total": round(material_total, 2)
    }
