import pandas as pd
import math

def load_clean_excel(path):
    df = pd.read_excel(path, skiprows=1)
    df.columns = df.columns.str.strip()
    df = df[df.columns[df.columns.str.contains("Products", case=False)][0]].notna()
    df = pd.read_excel(path, skiprows=1)
    df.columns = df.columns.str.strip()
    return df[df["Products"].notna()]

def load_paver_data():
    return load_clean_excel("Shaw Price 2025 Pavers slabs.xlsx")

def load_wall_data():
    return load_clean_excel("Shaw Price 2025 Walls.xlsx")

def load_steps_data():
    return load_clean_excel("Shaw Price 2025 Steps.xlsx")

def load_firepit_data():
    return load_clean_excel("Shaw Price 2025 Fire pits.xlsx")

def load_garden_wall_data():
    return load_clean_excel("Shaw Price 2025 Garden Walls.xlsx")

def load_extras_data():
    return load_clean_excel("Shaw Price 2025 Extras.xlsx")

def calculate_material_cost(product_name, sqft, df, override_margin=None):
    row = df[df["Products"] == product_name].iloc[0]
    price = row["Net"]
    margin = override_margin / 100 if override_margin is not None else row["Margin"]
    total_price = price * (1 + margin)
    coverage = row["Coverage"]
    return round((sqft / coverage) * total_price, 2)

def calculate_gravel_cost(sqft, depth_inches):
    gravel_depth_ft = depth_inches / 12
    volume_yd3 = (sqft * 1.25 * gravel_depth_ft) / 27
    loads = math.ceil(volume_yd3 / 3)
    return round(loads * 250, 2), round(volume_yd3, 2), loads

def calculate_fabric_cost(sqft):
    return round(sqft * 0.5, 2)

def calculate_polymeric_sand(sqft, product_name):
    if "Flagstone" in product_name:
        coverage = 50 if "Random" in product_name else 120
    else:
        coverage = 80
    bags = math.ceil(sqft / coverage)
    return bags, round(bags * 50, 2)

def calculate_labor_cost(laborers):
    return sum(round(l["hours"]) * l["rate"] for l in laborers)

def calculate_equipment_cost(equipment_hours):
    total = 0
    for equip, hours in equipment_hours.items():
        total += round(hours) * 130
    return total

def calculate_travel_cost(trailer_km, passenger_km, passenger_vehicles):
    base = 250 if trailer_km <= 30 else 250 + (trailer_km - 30) * 4.2
    trailer_total = round(base * 1.15, 2)
    passenger_total = round(passenger_km * 2 * 0.80 * passenger_vehicles, 2)
    return trailer_total + passenger_total

def calculate_total(*costs):
    subtotal = sum(costs)
    hst = subtotal * 0.15
    return round(subtotal, 2), round(hst, 2), round(subtotal + hst, 2)
