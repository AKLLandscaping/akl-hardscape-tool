import pandas as pd
import math

# Load and clean any Excel sheet
def load_clean_excel(path):
    df = pd.read_excel(path, skiprows=1)
    df.columns = df.columns.str.strip()
    df = df[df.columns[df.columns.str.contains("Products", case=False)][0]].notna()
    df = pd.read_excel(path, skiprows=1)
    df.columns = df.columns.str.strip()
    df = df[df[df.columns[1]].notna()]  # Drop empty rows
    return df

# Specific loaders
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
def calculate_material_cost(product_name, sqft, df, override_margin=None):
    df.columns = df.columns.str.strip()
    row = df[df["Products"] == product_name].iloc[0]
    unit = str(row["Unit"]).strip().upper()
    price = float(row["Contractor"])
    margin = override_margin / 100 if override_margin is not None else float(row["Margin"])
    coverage = float(row["Coverage"])

    if unit == "SFT":
        cost = (price * (1 + margin)) * (sqft / coverage)
    elif unit == "EA":
        pallets = math.ceil(sqft / coverage)
        cost = pallets * (price * coverage) * (1 + margin)
    elif unit == "KIT":
        cost = price * (1 + margin)
    elif unit == "TON":
        # Ton is 80 sqft/pallet
        cost = (price * (1 + margin)) * (sqft / 80)
    else:
        cost = 0

    return round(cost, 2)

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
def calculate_labor_cost(laborers):
    total = 0
    for name, rate, hours in laborers:
        total += float(rate) * float(hours)
    return round(total, 2)

# Equipment (all $130/hr + tax)
def calculate_equipment_cost(equipment_hours):
    total = 0
    for machine, hours in equipment_hours.items():
        total += hours * 130
    return round(total * 1.15, 2)

# Trailer Transport
def calculate_trailer_transport_cost(km):
    base_km = 30
    if km <= base_km:
        return round(250 * 1.15, 2)
    else:
        extra_km = km - base_km
        return round((250 + extra_km * 4.2) * 1.15, 2)

# Passenger Vehicle
def calculate_passenger_vehicle_cost(km, num_vehicles):
    return round(km * num_vehicles * 0.80, 2)

# Totals
def calculate_total(*costs):
    subtotal = sum(costs)
    hst = subtotal * 0.15
    return round(subtotal, 2), round(hst, 2), round(subtotal + hst, 2)
