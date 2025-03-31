import pandas as pd
import math

# Load and clean Excel files
def load_clean_excel(path):
    df = pd.read_excel(path, skiprows=1)
    df.columns = df.columns.str.strip()
    df = df[df["Products"].notna()]
    return df

def load_paver_data():
    return load_clean_excel("Shaw Price 2025 Pavers slabs.xlsx")

# Calculate material cost
def calculate_material_cost(product_name, sqft, product_data, margin_override=30):
    product_data.columns = product_data.columns.str.strip()
    match = product_data[product_data["Products"] == product_name]

    if match.empty:
        return {"material_total": 0, "unit_price": 0, "units_required": 0}

    row = match.iloc[0]
    price = float(row["Contractor"])
    unit = str(row["Unit"]).lower().strip()
    margin = margin_override / 100
    unit_price = price * (1 + margin)

    # Default coverage per pallet based on unit type
    if unit == "sft":
        coverage = float(row["Pallet Qty"])
    elif unit == "ea":
        coverage = 1
    elif unit == "kit":
        coverage = 1
    elif unit == "ton":
        coverage = 80  # Default for natural stone
    else:
        coverage = 1

    if unit in ["sft", "ton"]:
        units_required = math.ceil(sqft / coverage)
    else:
        units_required = 1

    material_total = round(units_required * unit_price, 2)

    return {
        "material_total": material_total,
        "unit_price": round(unit_price, 2),
        "units_required": units_required
    }
