import pandas as pd
import math

# Load each Shaw category individually
def load_paver_data():
    df = pd.read_excel("Shaw Price 2025 Pavers slabs.xlsx", skiprows=1)
    df.columns = df.columns.str.strip()  # remove extra spaces in headers
    df = df[df[df.columns[1]].notna()]   # filter out blank rows

    # Safety check for required columns
    if "Unit" not in df.columns or "TOTAL" not in df.columns:
        raise KeyError("Excel sheet is missing required columns: 'Unit' or 'TOTAL'")

    return df[df["Unit"] == "sft"].dropna(subset=["TOTAL"])

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

# Calculate material cost
def calculate_material_cost(product_name, sqft, product_data):
    try:
        product_data.columns = product_data.columns.str.strip()  # clean up headers just in case
        row = product_data[product_data.iloc[:, 1] == product_name].iloc[0]
        price = row["TOTAL"]
        coverage = row["Pallet Qty"]
        unit = row["Unit"]

        if unit == "sft":
            material_cost = price * (sqft / coverage)
        else:
            material_cost = price

        return round(material_cost, 2)
    except Exception as e:
        print(f"Error calculating material cost: {e}")
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
