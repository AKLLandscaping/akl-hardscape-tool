import pandas as pd
import math

# Loaders for each section
def load_paver_data():
    return pd.read_excel("Shaw Price 2025 Pavers.xlsx")

def load_wall_data():
    return pd.read_excel("Shaw Price 2025 Walls.xlsx")

def load_garden_wall_data():
    return pd.read_excel("Shaw Price 2025 Garden Walls.xlsx")

def load_steps_data():
    return pd.read_excel("Shaw Price 2025 Steps.xlsx")

def load_firepit_data():
    return pd.read_excel("Shaw Price 2025 Fire pits.xlsx")

def load_extras_data():
    return pd.read_excel("Shaw Price 2025 Extras.xlsx")

# Main material cost calculator
def calculate_material_cost(product_name, sqft, product_data, margin_percent):
    try:
        row = product_data[product_data["Product Name"] == product_name].iloc[0]
        unit = row["Unit"].strip().upper()
        base_price = float(row["Contractor"])
        pallet_qty = float(row["Pallet Qty"]) if not pd.isna(row["Pallet Qty"]) else 1

        # Apply margin
        price = base_price * (1 + margin_percent / 100)

        # Pricing logic
        if unit == "SFT":
            return round(price * (sqft / pallet_qty), 2)
        elif unit == "EA":
            return round(price * sqft, 2)  # sqft input acts as unit count here
        elif unit == "KIT":
            return round(price, 2)
        else:
            return 0.0
    except Exception:
        return 0.0

# Gravel base
def calculate_gravel_cost(sqft, depth_inches):
    volume = (sqft * 1.25 * (depth_inches / 12)) / 27  # in cubic yards
    loads = math.ceil(volume / 3)
    return round(loads * 250, 2), round(volume, 2), loads

# Geotextile
def calculate_fabric_cost(sqft):
    return round(sqft * 0.50, 2)

# Polymeric sand
def calculate_polymeric_sand(sqft, material_type):
    if "Flagstone" in material_type:
        coverage = 50 if "Random" in material_type else 120
    else:
        coverage = 80
    bags = math.ceil(sqft / coverage)
    return bags, round(bags * 50, 2)

# Labor
def calculate_labor_cost(labor_entries):
    return sum(entry["rate"] * entry["hours"] for entry in labor_entries)

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

# Total cost
def calculate_total(*costs):
    subtotal = sum(costs)
    hst = round(subtotal * 0.15, 2)
    return round(subtotal, 2), hst, round(subtotal + hst, 2)
