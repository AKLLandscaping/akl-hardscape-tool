import pandas as pd
import math

# Normalize and clean data
def load_clean_excel(path):
    df = pd.read_excel(path, skiprows=0)
    df.columns = df.columns.str.strip()

    # Drop rows that don't have a product name
    df = df[df["Products"].notna()]
    
    # Normalize unit formats (e.g., "sft", "SFT", "Sft" all become "SFT")
    if "Unit" in df.columns:
        df["Unit"] = df["Unit"].astype(str).str.upper().str.strip()

    return df

# Load specific categories
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

# Material Cost
def calculate_material_cost(product_name, sqft, product_data, margin_override=None):
    try:
        row = product_data[product_data["Products"] == product_name].iloc[0]
        unit = row["Unit"]
        price = float(row["Net"])
        margin = float(margin_override) if margin_override is not None else float(row["Margin"])
        pallet_qty = float(row["Pallet Qty"]) if row["Pallet Qty"] != "x" else 1
        coverage = float(row["Coverage"]) if "Coverage" in row and not pd.isna(row["Coverage"]) else 1

        final_price = price * (1 + margin)

        if unit == "SFT":
            material_cost = final_price * sqft / coverage
        elif unit == "EA":
            material_cost = final_price * (sqft / coverage)
        elif unit == "KIT":
            material_cost = final_price
        elif unit == "TON":
            material_cost = final_price * (sqft / coverage)
        else:
            material_cost = final_price

        return round(material_cost, 2)
    except Exception as e:
        return 0.0

# Gravel
def calculate_gravel_cost(sqft, depth_inches):
    gravel_depth_ft = depth_inches / 12
    gravel_volume_yd3 = (sqft * 1.25 * gravel_depth_ft) / 27
    loads = math.ceil(gravel_volume_yd3 / 3)
    cost = loads * 250
    return round(cost, 2), round(gravel_volume_yd3, 2), loads

# Fabric
def calculate_fabric_cost(sqft):
    return round(sqft * 0.50, 2)

# Sand
def calculate_polymeric_sand(sqft, material_type):
    if "Flagstone" in material_type:
        coverage = 50 if "Random" in material_type else 120
    else:
        coverage = 80
    bags = math.ceil(sqft / coverage)
    return bags, bags * 50

# Labor
def calculate_labor_cost(num_laborers, hours_per_laborer, rate):
    return round(num_laborers * hours_per_laborer * rate, 2)

# Equipment
def calculate_equipment_cost(excavator, skid_steer, dump_truck):
    total = 0
    if excavator:
        total += 400
    if skid_steer:
        total += 350
    if dump_truck:
        total += 300
    return total

# Travel
def calculate_travel_cost(trailer_km, passenger_km):
    trailer_cost = trailer_km * 2 * 1.25
    passenger_cost = passenger_km * 2 * 0.80
    return round(trailer_cost + passenger_cost, 2)

# Totals
def calculate_total(*costs):
    subtotal = sum(costs)
    hst = subtotal * 0.15
    return round(subtotal, 2), round(hst, 2), round(subtotal + hst, 2)
