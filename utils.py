import pandas as pd
import math

def load_paver_data():
    return load_clean_excel("Shaw Price 2025 Pavers slabs.xlsx")

def load_clean_excel(path):
    df = pd.read_excel(path, skiprows=1)
    df.columns = df.columns.str.strip()
    return df[df[df.columns[0]].notna()]

def calculate_material_cost(product_name, sqft, df, margin_override=30):
    row = df[df["Products"] == product_name].iloc[0]
    unit_coverage = row["Coverage"]
    contractor_price = row["Contractor"]
    margin = margin_override / 100
    unit_price = round(contractor_price * (1 + margin), 2)
    units_required = math.ceil(sqft / unit_coverage)
    material_total = round(unit_price * units_required, 2)
    return {
        "unit_price": unit_price,
        "units_required": units_required,
        "material_total": material_total
    }
