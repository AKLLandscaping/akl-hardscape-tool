import pandas as pd
import math

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

def calculate_material_cost(product_name, sqft, df, margin_override=None):
    df.columns = df.columns.str.strip()
    row = df[df["Products"] == product_name].iloc[0]

    price = float(row["Net"])
    margin = float(margin_override) / 100 if margin_override is not None else float(row["Margin"])
    coverage = float(row["Coverage"])

    units = sqft / coverage
    total = math.ceil(units) * (price * (1 + margin))
    return round(total, 2), math.ceil(units)

def calculate_gravel_cost(sqft, depth_inches):
    gravel_depth_ft = depth_inches / 12
    gravel_volume_yd3 = (sqft * 1.25 * gravel_depth_ft) / 27
    loads = math.ceil(gravel_volume_yd3 / 3)
    cost = loads * 250
    return round(cost, 2), round(gravel_volume_yd3, 2), loads

def calculate_fabric_cost(sqft):
    return round(sqft * 0.50, 2)

def calculate_polymeric_sand(sqft, material_type):
    if "Flagstone" in material_type:
        coverage = 50 if "Random" in material_type else 120
    else:
        coverage = 80
    bags = math.ceil(sqft / coverage)
    return bags, bags * 50

def calculate_labor_cost(laborers):
    total = 0
    for person in laborers:
        total += int(round(person["hours"])) * float(person["rate"])
    return round(total, 2)

def calculate_equipment_cost(equipment):
    total = 0
    for machine in equipment:
        hours = int(round(machine["hours"]))
        total += hours * 130
    return round(total, 2)

def calculate_travel_cost(trailer_km, passenger_km, num_passenger_vehicles=1):
    trailer_base = 250
    trailer_cost = trailer_base if trailer_km <= 30 else trailer_base + ((trailer_km - 30) * 4.2)
    passenger_cost = passenger_km * 2 * 0.80 * num_passenger_vehicles
    return round(trailer_cost + passenger_cost, 2)

def calculate_total(*costs):
    subtotal = sum(costs)
    hst = subtotal * 0.15
    return round(subtotal, 2), round(hst, 2), round(subtotal + hst, 2)
