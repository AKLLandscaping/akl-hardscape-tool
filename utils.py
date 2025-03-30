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

# Material cost
def calculate_material_cost(product_name, sqft, df, margin_override=None):
    df.columns = df.columns.str.strip()
    row = df[df["Products"] == product_name].iloc[0]

    price = float(row["Net"])
    margin = float(margin_override) / 100 if margin_override is not None else float(row["Margin"])
    pallet_qty = float(row["Pallet Qty"])
    coverage = float(row["Coverage"])

    unit = str(row["Unit"]).strip().upper()

    if unit == "SFT":
        units = sqft / coverage
    elif unit == "EA":
        units = math.ceil(sqft / coverage)
    elif unit == "KIT":
        units = 1
    elif unit == "TON":
        units = sqft / 80
    else:
        units = 1

    total = units * price * (1 + margin)
    return round(total, 2)

# Gravel cost
def calculate_gravel_cost(sqft, depth_inches):
    gravel_depth_ft = depth_inches / 12
    volume_yd3 = (sqft * 1.25 * gravel_depth_ft) / 27
    loads = math.ceil(volume_yd3 / 3)
    return round(loads * 250, 2)

# Fabric
def calculate_fabric_cost(sqft):
    return round(sqft * 0.50, 2)

# Polymeric sand
def calculate_polymeric_sand(sqft, material_type="Paver"):
    if "Flagstone" in material_type:
        coverage = 50 if "Random" in material_type else 120
    else:
        coverage = 80
    bags = math.ceil(sqft / coverage)
    return bags, round(bags * 50, 2)

# Labor cost
def calculate_labor_cost(laborers):
    total = 0
    for person in laborers:
        total += int(person['hours']) * float(person['rate'])
    return round(total, 2)

# Equipment cost
def calculate_equipment_cost(equipment_hours):
    total = 0
    for eq, hours in equipment_hours.items():
        total += round(hours * 130, 2)
    return round(total, 2)

# Travel cost
def calculate_travel_cost(trailer_km, passenger_km, num_vehicles):
    trailer_cost = 250 if trailer_km <= 30 else (250 + (trailer_km - 30) * 4.20)
    passenger_cost = passenger_km * num_vehicles * 0.80
    return round(trailer_cost + passenger_cost, 2)

# Total + tax
def calculate_total(*args):
    subtotal = sum(args)
    tax = subtotal * 0.15
    total = subtotal + tax
    return round(subtotal, 2), round(tax, 2), round(total, 2)
