import pandas as pd
import math

# Normalize and clean data
def load_clean_excel(path):
    df = pd.read_excel(path, skiprows=0)
    df.columns = df.columns.str.strip()
    df = df[df["Products"].notna()]
    if "Unit" in df.columns:
        df["Unit"] = df["Unit"].astype(str).str.upper().str.strip()
    return df

def load_paver_data():
    return load_clean_excel("Shaw Price 2025 Pavers slabs.xlsx")

# Material cost with margin override
def calculate_material_cost(product_name, sqft, product_data, margin_override=None):
    try:
        row = product_data[product_data["Products"] == product_name].iloc[0]
        unit = row["Unit"]
        price = float(row["Net"])
        margin = float(margin_override) if margin_override is not None else float(row["Margin"])
        coverage = float(row["Coverage"]) if "Coverage" in row and not pd.isna(row["Coverage"]) else 1
        final_price = price * (1 + margin)

        if unit == "SFT":
            return round(final_price * sqft / coverage, 2)
        elif unit == "EA":
            return round(final_price * (sqft / coverage), 2)
        elif unit == "KIT":
            return round(final_price, 2)
        elif unit == "TON":
            return round(final_price * (sqft / coverage), 2)
        else:
            return round(final_price, 2)
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
    if "FLAGSTONE" in material_type.upper():
        coverage = 50 if "RANDOM" in material_type.upper() else 120
    else:
        coverage = 80
    bags = math.ceil(sqft / coverage)
    return bags, bags * 50

# Labor
def calculate_labor_cost(laborers):
    total = 0
    for laborer in laborers:
        total += laborer['rate'] * laborer['hours']
    return round(total, 2)

# Equipment
def calculate_equipment_cost(excavator_hrs, skid_steer_hrs, dump_truck_hrs):
    hourly_cost = (excavator_hrs + skid_steer_hrs + dump_truck_hrs) * 130 * 1.15
    return round(hourly_cost, 2)

# Trailer transport logic
def calculate_trailer_cost(km):
    base_cost = 250 * 1.15
    if km <= 30:
        return round(base_cost, 2)
    else:
        extra_km = km - 30
        return round(base_cost + (extra_km * 4.20), 2)

# Passenger vehicle travel
def calculate_passenger_vehicle_cost(km, vehicles):
    return round(km * 2 * vehicles * 0.80, 2)

# Totals
def calculate_total(*costs):
    subtotal = sum(costs)
    hst = subtotal * 0.15
    return round(subtotal, 2), round(hst, 2), round(subtotal + hst, 2)
