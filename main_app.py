import streamlit as st
import math
from utils import load_paver_data, calculate_material_cost

# Constants
TAX = 0.15
GRAVEL_COST = 250
GEOTEXTILE_COST_PER_SQFT = 0.5
EQUIP_RATE = 130
TRAILER_BASE_KM = 30
TRAILER_BASE_COST = 250
TRAILER_EXTRA_KM_RATE = 4.20
PASSENGER_KM_RATE = 0.80
EDGE_RESTRAINT_COST = 220  # Per 100 sqft
INLAY_COST = 4000
INLAY_NO_BORDER_COST = 2850
FOOD_PER_NIGHT_PER_LABORER = 50

# UI
st.set_page_config(page_title="AKL Hardscape Master Tool – Walkway Estimator", layout="wide")
st.title("🧱 AKL Hardscape Master Tool – Walkway Estimator")

try:
    df = load_paver_data()

    # Inputs
    sqft = st.number_input("📏 Square Feet", min_value=0, step=1)
    margin = st.slider("📊 Override Margin %", 0, 100, 30)

    products = df["Products"].dropna().tolist()
    selected_product = st.selectbox("🧱 Choose Product", products)

    st.subheader("👷 Labor")
    num_laborers = st.selectbox("Number of Laborers", list(range(1, 11)))
    labor_total = 0
    for i in range(num_laborers):
        hours = st.selectbox(f"Hours for Laborer #{i+1}", list(range(1, 13)), key=f"hrs_{i}")
        rate = st.selectbox(f"Hourly Rate for Laborer #{i+1}", [35, 40, 45, 50, 55, 60, 65], key=f"rate_{i}")
        labor_total += hours * rate

    st.subheader("🚜 Equipment Use")
    excavator_hours = st.selectbox("Excavator Hours", list(range(0, 13)))
    skid_steer_hours = st.selectbox("Skid Steer Hours", list(range(0, 13)))
    dump_truck_hours = st.selectbox("Dump Truck Hours", list(range(0, 13)))
    excavator_km = st.number_input("Excavator Trailer Km", step=1, value=30)
    skid_km = st.number_input("Skid Steer Trailer Km", step=1, value=30)
    truck_km = st.number_input("Dump Truck Trailer Km", step=1, value=30)

    st.subheader("🚗 Travel")
    round_trip_km = st.number_input("Round Trip Distance (km)", step=1, value=30)
    num_vehicles = st.selectbox("Number of Passenger Vehicles", list(range(1, 11)))

    st.subheader("➕ Add-Ons")
    inlay = st.checkbox("Include 4 ft wide inlay ($4000 + HST)")
    inlay_no_border = st.checkbox("Inlay with no border/background ($2850 + HST)")
    sand_type = st.selectbox("Polymeric Sand Type", ["None", "$50+tax per bag", "$75+tax per bag"])

    extra_gravel_loads = st.selectbox("Extra Gravel Loads", list(range(0, 6)))
    gravel_price = st.number_input("Extra Gravel Price per Load ($)", value=250, step=1)
    delivery_km = st.number_input("Delivery Distance (km)", step=1, value=30)

    st.subheader("🏨 Overnight Stay")
    overnight_room_cost = st.number_input("Room Cost ($)", value=0, step=1)
    num_nights = st.selectbox("Nights", list(range(0, 8)))
    overnight_food_total = num_laborers * FOOD_PER_NIGHT_PER_LABORER * num_nights
    overnight_total = overnight_room_cost * num_nights + overnight_food_total

    # MATERIALS
    material = calculate_material_cost(selected_product, sqft, df, margin_override=margin)

    # GRAVEL
    gravel_yards = math.ceil(sqft * 0.5 / 27)
    gravel_base_cost = gravel_yards * GRAVEL_COST
    geotextile_total = round(sqft * GEOTEXTILE_COST_PER_SQFT, 2)

    # EDGE RESTRAINT
    edge_units = math.ceil(sqft / 100)
    edge_total = edge_units * EDGE_RESTRAINT_COST * (1 + TAX)

    # INLAY
    inlay_total = 0
    if inlay:
        inlay_total += INLAY_COST * (1 + TAX)
    if inlay_no_border:
        inlay_total += INLAY_NO_BORDER_COST * (1 + TAX)

    # EQUIPMENT
    equipment_hours = excavator_hours + skid_steer_hours + dump_truck_hours
    equipment_cost = equipment_hours * EQUIP_RATE * (1 + TAX)

    # TRAILER
    def trailer_cost(km):
        return TRAILER_BASE_COST if km <= TRAILER_BASE_KM else TRAILER_BASE_COST + (km - TRAILER_BASE_KM) * TRAILER_EXTRA_KM_RATE

    trailer_total = sum([
        trailer_cost(excavator_km),
        trailer_cost(skid_km),
        trailer_cost(truck_km)
    ])

    # PASSENGER VEHICLE
    passenger_travel_cost = round(round_trip_km * PASSENGER_KM_RATE * num_vehicles, 2)

    # SAND
    sand_price = 0
    sand_coverage = 0
    if sand_type == "$50+tax per bag":
        sand_price = 50
        sand_coverage = 80
    elif sand_type == "$75+tax per bag":
        sand_price = 75
        sand_coverage = 80
    sand_bags = math.ceil(sqft / sand_coverage) if sand_coverage else 0
    sand_total = sand_bags * sand_price * (1 + TAX)

    # EXTRA GRAVEL
    extra_km = max(0, delivery_km - 30)
    delivery_charge = extra_km * 4.20
    gravel_addon_cost = extra_gravel_loads * gravel_price + delivery_charge

    # SUMMARY
    subtotal = sum([
        material["material_total"],
        gravel_base_cost,
        geotextile_total,
        edge_total,
        inlay_total,
        labor_total,
        equipment_cost,
        trailer_total,
        passenger_travel_cost,
        sand_total,
        gravel_addon_cost,
        overnight_total
    ])

    hst = round(subtotal * TAX, 2)
    final = round(subtotal + hst, 2)

    # Output
    st.subheader("📋 Estimate Summary")
    st.write(f"**Product:** {selected_product}")
    st.write(f"**Price per Unit (with margin):** ${material['unit_price']}")
    st.write(f"**Units Required:** {material['units_required']}")
    st.write(f"**Material Total:** ${material['material_total']}")
    st.markdown("---")
    st.write(f"**Gravel Yards:** {gravel_yards} @ ${GRAVEL_COST}/yd = ${gravel_base_cost}")
    st.write(f"**Geotextile Fabric Cost:** ${geotextile_total}")
    st.write(f"**Edge Restraint:** {edge_units} x $220 = ${round(edge_total, 2)}")
    st.write(f"**Labor Total:** ${labor_total}")
    st.write(f"**Equipment Cost:** ${round(equipment_cost, 2)}")
    st.write(f"**Trailer Transport:** ${round(trailer_total, 2)}")
    st.write(f"**Passenger Vehicle Travel:** ${passenger_travel_cost}")
    st.write(f"**Extra Gravel Loads:** ${gravel_addon_cost}")
    st.write(f"**Polymeric Sand:** {sand_bags} bags = ${round(sand_total, 2)}")
    if inlay_total:
        st.write(f"**Inlay Add-On:** ${round(inlay_total, 2)}")
    if overnight_total > 0:
        st.write(f"**Overnight Stay Total:** ${round(overnight_total, 2)}")

    st.markdown("---")
    st.write(f"**Subtotal:** ${round(subtotal, 2)}")
    st.write(f"**HST (15%) :** ${hst}")
    st.markdown(f"### 💰 Final Total: ${final}")

except Exception as e:
    st.error(f"Something went wrong: {e}")
