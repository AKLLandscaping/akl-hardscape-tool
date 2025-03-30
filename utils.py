import pandas as pd
import math

# Load and clean Excel files
def load_clean_excel(path):
    df = pd.read_excel(path, skiprows=1)
    df.columns = df.columns.str.strip()  # Strip whitespace from headers
    product_col = next(col for col in df.columns if col.strip().lower() == "products")
    df = df[df[product_col].notna()]
    return df

def load_paver_data():
    return load_clean_excel("Shaw Price 2025 Pavers slabs.xlsx")

def load_wall_data():
    return load_clean_excel("Shaw Price 2025 Walls.xlsx")

def load_steps_data():
    return load_clean_excel("Shaw Price 2025 Steps Stairs.xlsx")

def load_firepit_data():
    return load_clean_excel("Shaw Price 2025 Fire pits.xlsx")

def load_garden_wall_data():
    return load_clean_excel("Shaw Price 2025 Garden Walls.xlsx")

def load_extras_data():
    return load_clean_excel("Shaw Price 2025 Extras.xlsx")

# Material cost calculator
def calculate_material_cost(product_name, sqft, df, margin_override=None):
    df.columns = df.columns.str.strip()
    row = df[df["Products"] == product_name].iloc[0]

    price = float(row["Net"])
    margin = float(margin_override) / 100 if margin_override is not None else float(row["Margin"])
    pallet_qty = float(row["Pallet Qty"])
    coverage = float(row["Coverage"])

    unit = str(row.get("Unit", "SFT")).strip().upper()

    if unit == "SFT":
        units = sqft / coverage
    elif unit == "EA":
        units = sqft
    elif unit == "KIT":
        units = 1
    elif unit == "TON":
        units = sqft / 80  # Default ton coverage
    else:
        raise ValueError(f"Unknown unit type: {unit}")

    total_cost = units * price * (1 + margin)
    return math.ceil(total_cost)
