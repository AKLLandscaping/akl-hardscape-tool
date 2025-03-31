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

def calculate_material_cost(product_name, sqft, product_data, margin_override=30):
    try:
        row = product_data[product_data["Products"] == product_name].iloc[0]
        price = float(row["Contractor"])
        unit = str(row["Unit"]).strip().lower()
        coverage = float(row["Pallet Qty"])
        margin = margin_override / 100

        # Determine coverage logic
        if unit in ["sft", "sqft"]:
            units_required = sqft / coverage
            unit_price = price * (1 + margin)
            material_total = unit_price * units_required
        elif unit in ["ea", "each"]:
            units_required = math.ceil(sqft / coverage)
            unit_price = price * (1 + margin)
            material_total = unit_price * units_required
        elif unit in ["kit"]:
            units_required = 1
            unit_price = price * (1 + margin)
            material_total = unit_price
        elif unit in ["ton"]:
            units_required = sqft / 80  # for natural stone: 80 sqft per ton
            unit_price = price * (1 + margin)
            material_total = unit_price * units_required
        else:
            # Fallback
            units_required = 1
            unit_price = price * (1 + margin)
            material_total = unit_price

        return {
            "unit_price": round(unit_price, 2),
            "units_required": math.ceil(units_required),
            "material_total": round(material_total, 2)
        }

    except Exception as e:
        return {
            "unit_price": 0.0,
            "units_required": 0,
            "material_total": 0.0
        }
