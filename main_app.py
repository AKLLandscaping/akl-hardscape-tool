import streamlit as st
import math
from utils import load_paver_data, calculate_material_cost

# Constants
EDGE_RESTRAINT_COST = 220
INLAY_STANDARD = 4000
INLAY_NO_BORDER = 2850
GRAVEL_COST_PER_LOAD = 250
SAND_COST_OPTIONS = {"$50+tax per bag": 50, "$75+tax per bag": 75}
EQUIPMENT_HOURLY_RATE = 130
TRAILER_BASE_KM = 30
TRAILER_BASE_COST = 250
TRAILER_EXTRA_COST_PER_KM = 4.20
PASSENGER_COST_PER_KM = 0.80
TAX_RATE = 0.15
MEAL_COST_PER_NIGHT = 50

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="wide")

def calculate_edge_restraint_cost(sqft):
    edge_units = math.ceil(sqft / 100)
    return round(edge_units * EDGE_RESTRAINT_COST * (1 + TAX_RATE), 2)

def calculate_gravel_base_cost(sqft):
    gravel_depth_ft = 0.5  # 6"
    volume_yd3 = (sqft * 1.25 * gravel_depth_ft) / 27
    return math.ceil(volume_yd3), math.ceil(volume_yd3 / 3) * GRAVEL_COST_PER_LOAD

def calculate_extra_gravel_cost(loads, price_per_load, km):
    extra_km = max(0, km - TRAILER_BASE_KM)
    delivery_cost = extra_km * TRAILER_EXTRA_COST_PER_KM
    return round(loads * price_per_load + delivery_cost, 2)

def calculate_inlay_cost(standard, no_border):
    cost = 0
    if standard:
        cost += INLAY_STANDARD
    if no_border:
        cost += INLAY_NO_BORDER
    return round(cost * (1 + TAX_RATE), 2)

def calculate_poly_sand_cost(sqft, bag_price):
    if not bag_price:
        return 0, 0
    coverage = 80  # pavers default
    bags = math.ceil(sqft / coverage)
    return bags, round(bags * bag_price * (1 + TAX_RATE), 2)

def calculate_labor_cost(num_laborers):
    total = 0
    for i in range(num_laborers):
        hours = st.selectbox(f"Hours for Laborer #{i+1}", list(range(1, 13)), index=7, key=f"hours_{i}")
        rate = st.selectbox(f"Hourly Rate for Laborer #{i+1}", [35, 40, 45, 50, 55, 60, 65], index=2, key=f"rate_{i}")
        total += hours * rate
    return total

def calculate_equipment_cost(hours):
    return round(hours * EQUIPMENT_HOURLY_RATE * (1 + TAX_RATE), 2)

def calculate_trailer_cost(km):
    if km <= TRAILER_BASE_KM:
        return TRAILER_BASE_COST
    else:
        return TRAILER_BASE_COST + (km - TRAILER_BASE_KM) * TRAILER_EXTRA_COST_PER_KM

def calculate_passenger_vehicle_cost(km, num_vehicles):
    return round(km * 2 * PASSENGER_COST_PER_KM * num_vehicles, 2)

def calculate_overnight_cost(room_cost, nights, laborers):
    meal_total = laborers * nights * MEAL_COST_PER_NIGHT * (1 + TAX_RATE)
    return round(room_cost + meal_total, 2), meal_total

def main():
    st.title("🧱 AKL Hardscape Master Tool - Walkway Estimator")

    data = load_paver_data()

    sqft = st.number_input("📐 Total Square Feet", min_value=0, value=100, step=1)
    margin = st.slider("💰 Margin %", 0, 100, value=30)

    product = st.selectbox("🧱 Select Paver Product", data["Products"].dropna().unique())

    st.markdown("### 🔲 Inlay Options")
    inlay_standard = st.checkbox("4ft Inlay ($4000 + HST)")
    inlay_no_border = st.checkbox("Inlay (no background or border) ($2850 + HST)")

    st.markdown("### 🧱 Polymeric Sand")
    sand_price_selection = st.selectbox("Poly Sand Bag Price", ["", *SAND_COST_OPTIONS.keys()])
    bag_price = SAND_COST_OPTIONS.get(sand_price_selection, 0)

    st.markdown("### 🚧 Base Gravel")
    gravel_yards, gravel_base_cost = calculate_gravel_base_cost(sqft)

    extra_gravel_loads = st.selectbox("Extra Gravel Loads", list(range(0, 6)))
    extra_gravel_price = st.number_input("Price per Extra Load ($)", value=250)
    extra_gravel_km = st.number_input("Extra Gravel Delivery Distance (km)", value=30, step=1)

    st.markdown("### 👷 Labor")
    num_laborers = st.selectbox("Number of Laborers", list(range(1, 11)), index=1)
    labor_total = calculate_labor_cost(num_laborers)

    st.markdown("### 🚜 Equipment")
    excavator_hours = st.selectbox("Excavator Hours", list(range(0, 13)))
    skid_steer_hours = st.selectbox("Skid Steer Hours", list(range(0, 13)))
    dump_truck_hours = st.selectbox("Dump Truck Hours", list(range(0, 13)))

    excavator_km = st.number_input("Excavator Trailer Km", value=30)
    skid_km = st.number_input("Skid Steer Trailer Km", value=30)
    truck_km = st.number_input("Dump Truck Trailer Km", value=30)

    trailer_cost = sum([
        calculate_trailer_cost(excavator_km),
        calculate_trailer_cost(skid_km),
        calculate_trailer_cost(truck_km)
    ]) * (1 + TAX_RATE)

    st.markdown("### 🚗 Passenger Vehicle Travel")
    passenger_km = st.number_input("Passenger Vehicle Distance (km)", value=30)
    num_vehicles = st.selectbox("Number of Passenger Vehicles", list(range(1, 11)))
    passenger_travel_cost = calculate_passenger_vehicle_cost(passenger_km, num_vehicles)

    st.markdown("### 🏨 Overnight Stay")
    room_cost = st.number_input("Room Cost ($)", value=0)
    nights = st.selectbox("Number of Nights", list(range(0, 8)))
    overnight_laborers = st.selectbox("Laborers Staying Overnight", list(range(0, 11)))
    overnight_total, meal_total = calculate_overnight_cost(room_cost, nights, overnight_laborers)

    edge_cost = calculate_edge_restraint_cost(sqft)
    inlay_cost = calculate_inlay_cost(inlay_standard, inlay_no_border)
    sand_bags, sand_total = calculate_poly_sand_cost(sqft, bag_price)
    extra_gravel_total = calculate_extra_gravel_cost(extra_gravel_loads, extra_gravel_price, extra_gravel_km)
    material = calculate_material_cost(product, sqft, data, margin_override=margin)

    equip_total = sum([
        calculate_equipment_cost(excavator_hours),
        calculate_equipment_cost(skid_steer_hours),
        calculate_equipment_cost(dump_truck_hours)
    ])

    st.markdown("---")
    st.subheader("📊 Estimate Summary")

    st.write(f"**Material ({product}):** ${material['material_total']}")
    st.write(f"**Gravel Base (approx {gravel_yards} yds³):** ${gravel_base_cost}")
    st.write(f"**Edge Restraint:** ${edge_cost}")
    st.write(f"**Labor Total:** ${round(labor_total, 2)}")
    st.write(f"**Equipment:** ${equip_total}")
    st.write(f"**Trailer Transport:** ${trailer_cost}")
    st.write(f"**Passenger Travel:** ${passenger_travel_cost}")
    st.write(f"**Extra Gravel:** ${extra_gravel_total}")
    if bag_price:
        st.write(f"**Polymeric Sand ({sand_bags} bags):** ${sand_total}")
    if inlay_cost:
        st.write(f"**Inlay Option(s):** ${inlay_cost}")
    if overnight_total > 0:
        st.write(f"**Room Cost:** ${room_cost}")
        st.write(f"**Meals for {overnight_laborers} laborers × {nights} nights:** ${round(meal_total, 2)}")
        st.write(f"**Overnight Total:** ${overnight_total}")

    subtotal = sum([
        material["material_total"], gravel_base_cost, edge_cost, labor_total,
        equip_total, trailer_cost, passenger_travel_cost, extra_gravel_total,
        sand_total, inlay_cost, overnight_total
    ])
    hst = round(subtotal * TAX_RATE, 2)
    total = round(subtotal + hst, 2)

    st.markdown("---")
    st.write(f"**Subtotal:** ${subtotal}")
    st.write(f"**HST (15%):** ${hst}")
    st.markdown(f"### 💰 Total: ${total}")

if __name__ == "__main__":
    main()
