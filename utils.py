import pandas as pd
import math

# 🔧 Universal cleaner for Shaw Brick files
def load_clean_excel(path):
    df = pd.read_excel(path, skiprows=1)
    df.columns = df.columns.str.strip().str.title()
    df = df[df.columns[df.columns.str.contains("Products", case=False)][0]].notna()
    df = pd.read_excel(path, skiprows=1)
    df.columns = df.columns.str.strip().str.title()
    df = df[df["Products"].notna()]
    return df

# 📥 Loaders for each category
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

# 💲 Material cost with dynamic margin
def calculate_material_cost(product_name, sqft, product_data, margin):
    try:
        product_row = product_data[product_data["Products"] == product_name].iloc[0]
        unit = str(product_row["Unit"]).strip().upper()
        price = float(product_row["Contractor"])
        coverage = float(product_row.get("Coverage", 1))

        if unit == "SFT":
            cost = sqft * price
        elif unit == "EA":
            pallets = math.ceil(sqft / coverage)
            cost = pallets * price
        elif unit == "KIT":
            cost = price
        elif unit == "TON":
            pallets = math.ceil(sqft / coverage)
            cost = pallets * price
        else:
            cost = sqft * price

        cost_with_margin = cost * (1 + margin)
        return round(cost_with_margin, 2)
    except Exception:
        return 0.0

# 🪨 Gravel base
def calculate_gravel_cost(sqft, depth_inches):
    gravel_depth_ft = depth_inches / 12
    volume = (sqft * 1.25 * gravel_depth_ft) / 27
    loads = math.ceil(volume / 3)
    cost = loads * 250
    return round(cost, 2), round(volume, 2), loads

# 🧵 Fabric
def calculate_fabric_cost(sqft):
    return round(sqft * 0.50, 2)

# 🧱 Polymeric sand
def calculate_polymeric_sand(sqft, product):
    if "Flagstone" in product:
        coverage = 50 if "Random" in product else 120
    else:
        coverage = 80
    bags = math.ceil(sqft / coverage)
    return bags, bags * 50

# 👷 Labor
def calculate_labor_cost(num_laborers, hours_per_laborer, rate):
    return round(num_laborers * hours_per_laborer * rate, 2)

# 🚜 Equipment
def calculate_equipment_cost(excavator, skid_steer, dump_truck):
    total = 0
    if excavator: total += 400
    if skid_steer: total += 350
    if dump_truck: total += 300
    return total

# 🚗 Travel
def calculate_travel_cost(trailer_km, passenger_km):
    trailer_cost = trailer_km * 2 * 1.25
    passenger_cost = passenger_km * 2 * 0.80
    return round(trailer_cost + passenger_cost, 2)

# ➕ Totals
def calculate_total(*costs):
    subtotal = sum(costs)
    hst = subtotal * 0.15
    return round(subtotal, 2), round(hst, 2), round(subtotal + hst, 2)
