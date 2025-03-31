import pandas as pd
import math

# Load and clean Excel file
def load_clean_excel(path):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()
    return df

# Load paver data
def load_paver_data():
    return load_clean_excel("Shaw Price 2025 Pavers slabs.xlsx")

# Material calculation
def calculate_material_cost(product_name, sqft, df, margin_override=None):
    df.columns = df.columns.str.strip()
    row = df[df["Products"] == product_name].iloc[0]

    price = float(row["Net"])
    margin = float(margin_override) / 100 if margin_override is not None else float(row["Margin"])
    coverage = float(row["Coverage"])
    units = math.ceil(sqft / coverage)

    total = units * price * (1 + margin)
    return {
        "units": units,
        "unit_price_with_margin": price * (1 + margin),
        "total": total
    }
