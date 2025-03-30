import pandas as pd
import math

# Load each Shaw category individually and clean data
def load_clean_excel(path):
    df = pd.read_excel(path, skiprows=1)
    df.columns = df.columns.str.strip()
    df = df[df[df.columns[1]].notna()]  # Filter valid product rows
    df["Unit"] = df["Unit"].astype(str).str.upper().str.strip()
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

# Material cost logic using unit type
def calculate_material_cost(product_name, sqft, product_data, override_margin=None):
    try:
        product_data.columns = product_data.columns.str.strip()
        row = product_data[product_data["Product Name"] == product_name].iloc[0]
        unit = row["Unit"]
        price = row["Net"]
        margin = override_margin / 100 if override_margin is not None else row["Margin"]
        final_price = price * (1 + margin)

        # Coverage
        if "Coverage" in row and not pd.isna(row["Coverage"]):
            coverage = row["Coverage"]
        elif unit == "SFT":
            coverage = row["Pallet Qty"]
        elif unit == "EA":
            # Default square footage per pallet if unit is EA (based on assumed product thickness)
            name = row["Product Name"].lower()
            if "50mm" in name:
                coverage = 126
            elif "60mm" in name:
                coverage = 102
            elif "80mm" in name:
                coverage = 88
            else:
                coverage = 100
        elif unit == "TON":
            coverage = 80
        elif unit == "KIT":
            coverage = 1
        else:
            coverage = 100

        material_cost = final_price * (sqft / coverage)
        return round(material_cost, 2)
    except:
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
    if "flagstone" in material_type.lower():
        coverage = 50 if "random" in material_type.lower() else 120
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
