import pandas as pd
import math

# Load Shaw Brick Pavers
def load_paver_data():
    df = pd.read_excel("Shaw Price 2025 Pavers slabs.xlsx", skiprows=1)
    df = df[df["Unit"] == "sft"]                      # Only sft products
    df = df[df["TOTAL"].notna()]                     # Drop rows with no price
    df = df[df["Clay Pavers"].notna()]               # Drop mid-sheet header rows
    return df

def load_wall_data():
    return pd.read_excel("Shaw Price 2025 Walls.xlsx", skiprows=1)

def load_steps_data():
    return pd.read_excel("Shaw Price 2025 Steps Stairs.xlsx", skiprows=1)

def load_firepit_data():
    return pd.read_excel("Shaw Price 2025 Fire pits.xlsx", skiprows=1)

def load_garden_wall_data():
    return pd.read_excel("Shaw Price 2025 Garden Walls.xlsx", skiprows=1)

def load_extras_data():
    return pd.read_excel("Shaw Price 2025 Extras.xlsx", skiprows=1)

# Material calculation
def calculate_material_cost(product_name, sqft, product_data):
    try:
        row = product_data[product_data["Clay Pavers"] == product_name].iloc[0]
        price = row["TOTAL"]
        coverage = row["Pallet Qty"]
        unit = row["Unit"]
        if unit == "sft":
            return round(price * (sqft / coverage), 2)
        else:
            return round(price, 2)
    except:
        return 0.0

# Gravel
def calculate_gravel_cost(sqft, depth_inches):
    depth_ft = depth_inches / 12
    volume_yd3 = (sqft * 1.25 * depth_ft) / 27
    loads = math.ceil(volume_yd3 / 3)
    cost = loads * 250
    return round(cost, 2), round(volume_yd3, 2), loads

# Fabric
def calculate_fabric_cost(sqft):
    return round(sqft * 0.50, 2)

# Polymeric sand
def calculate_polymeric_sand(sqft, material_type):
    if "Flagstone" in material_type:
        coverage = 50 if "Random" in material_type else 120
    else:
        coverage = 80
    bags = math.ceil(sqft / coverage)
    return bags, bags * 50

# Labor
def calculate_labor_cost(num_laborers, hours, rate):
    return round(num_laborers * hours * rate, 2)

# Equipment
def calculate_equipment_cost(excavator, skid_steer, dump_truck):
    total = 0
    if excavator: total += 400
    if skid_steer: total += 350
    if dump_truck: total += 300
    return total

# Travel
def calculate_travel_cost(trailer_km, passenger_km):
    trailer = trailer_km * 2 * 1.25
    passenger = passenger_km * 2 * 0.80
    return round(trailer + passenger, 2)

# Totals
def calculate_total(*args):
    subtotal = sum(args)
    hst = subtotal * 0.15
    return round(subtotal, 2), round(hst, 2), round(subtotal + hst, 2)
