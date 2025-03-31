import pandas as pd

def load_paver_data():
    df = pd.read_excel("Shaw Price 2025 Pavers slabs.xlsx")
    return df[df["Products"].notna()]

def calculate_material_cost(product_name, sqft, df, margin_override=30):
    row = df[df["Products"] == product_name].iloc[0]
    coverage = row["Coverage"]
    pallet_qty = row["Pallet Qty"]
    base_price = row["Net"]
    
    units_required = (sqft / coverage)
    price_with_margin = base_price * (1 + (margin_override / 100))
    material_total = round(price_with_margin * units_required, 2)

    return {
        "unit_price": round(price_with_margin, 2),
        "units_required": round(units_required, 2),
        "material_total": material_total
    }
