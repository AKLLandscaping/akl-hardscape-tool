import pandas as pd
import math

def load_clean_excel(file_path):
    df = pd.read_excel(file_path)
    df.columns = [col.strip() for col in df.columns]
    df = df[df["Products"].notna()]
    return df

def load_paver_data():
    return load_clean_excel("Shaw Price 2025 Pavers slabs.xlsx")

def calculate_material_cost(product_name, sqft, df, margin_override=None):
    product_row = df[df["Products"] == product_name].iloc[0]

    unit_price = product_row["Total"]
    coverage = product_row["Coverage"]
    margin = product_row["Margin"]

    if margin_override is not None:
        unit_price = round(product_row["Net"] * (1 + margin_override / 100), 2)

    units_required = math.ceil(sqft / coverage) if coverage > 0 else 1
    material_total = round(units_required * unit_price, 2)

    return {
        "unit_price": round(unit_price, 2),
        "units_required": units_required,
        "material_total": material_total
    }
