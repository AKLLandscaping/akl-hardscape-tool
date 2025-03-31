import pandas as pd

def load_clean_excel(filename):
    df = pd.read_excel(filename)
    df.columns = [col.strip() for col in df.columns]
    if "Products" not in df.columns:
        raise KeyError("Missing 'Products' column in the Excel file.")
    return df[df["Products"].notna()]

def load_paver_data():
    df = load_clean_excel("Shaw Price 2025 Pavers slabs.xlsx")
    if "Unit" not in df.columns:
        raise KeyError("Missing 'Unit' column in the paver Excel sheet.")
    return df[df["Unit"].isin(["sft", "ea", "kit", "ton"])].dropna(subset=["TOTAL"])

def calculate_material_cost(product, sqft, df, margin_override=30):
    row = df[df["Products"] == product].iloc[0]
    unit_type = row["Unit"]
    coverage = row["Coverage"]
    net_price = row["Net"]
    unit_price = net_price * (1 + margin_override / 100)

    if unit_type == "sft":
        units_required = sqft / coverage
    else:
        units_required = 1  # For kit, ea, ton: 1 unit flat

    material_total = round(units_required * unit_price, 2)

    return {
        "unit_type": unit_type,
        "unit_price": round(unit_price, 2),
        "units_required": round(units_required, 2),
        "material_total": material_total
    }
