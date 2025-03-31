import streamlit as st
import math
from utils import load_paver_data, calculate_material_cost

# Constants
EDGE_RESTRAINT_COST = 220
INLAY_COST_FULL = 4000
INLAY_COST_SIMPLE = 2850
GRAVEL_COST_PER_LOAD = 250
SAND_COST_PER_BAG = 50
SAND_COST_PREMIUM = 75
EQUIPMENT_HOURLY_RATE = 130
TRAILER_BASE_COST = 250
TRAILER_KM_THRESHOLD = 30
TRAILER_KM_RATE = 4.20
PASSENGER_KM_RATE = 0.80
TAX_RATE = 0.15
MEAL_COST_PER_LABORER = 50  # per night

st.set_page_config(page_title="AKL Walkway Estimator", layout="wide")
st.title("🧱 AKL Hardscape Master Tool – Walkway Estimator")

# Load Data
paver_data = load_paver_data()

# --- Inputs ---
st.header("📐 Project Details")
sqft = st.number_input("Square Feet of Walkway", min_value=0, step=1)
margin = st.slider("Contractor Margin %", 0, 100, 30)

# Product dropdown with unit in display
paver_options = paver_data.apply(
    lambda row: f"{row['Products']} — ({str(row['Unit']).strip().lower()})", axis=1
)
selected_display = st.selectbox("🧱 Choose Product", paver_options)
selected_product = selected_display.split(" — ")[0]

# Labor
st.header("👷 Labor")
num_laborers = st.selectbox("Number of Laborers", list(range(1, 11)))
labor_total = 0
for i in range(num_laborers):
    hours = st.selectbox(f"Hours for Laborer #{i+1}", list(range(1, 13)), key=f"hours_{i}")
    rate = st.selectbox(f"Hourly Rate for Laborer #{i+1}", [35, 40, 45, 50, 55, 60, 65], key=f"rate_{i}")
    labor_total += hours * rate

# Equipment
st.header("🚜 Equipment Usage")
excavator_hours = st.selectbox("Excavator Hours", list(range(0, 13)))
skid_steer_hours = st.selectbox("Skid Steer Hours", list(range(0, 13)))
dump_truck_hours = st.selectbox("Dump Truck Hours", list(range(0, 13)))
equipment_total = (excavator_hours + skid_steer_hours + dump_truck_hours) * EQUIPMENT_HOURLY_RATE
equipment_total_with_tax = round(equipment_total * (1 + TAX_RATE))

# Travel
st.header("🚚 Travel")
excavator_km = st.number_input("Excavator Trailer KM", min_value=0, step=1)
skid_km = st.number_input("Skid Steer Trailer KM", min_value=0, step=1)
truck_km = st.number_input("Dump Truck Trailer KM", min_value=0, step=1)
passenger_km = st.number_input("Passenger Vehicle KM", min_value=0, step=1)
passenger_vehicles = st.selectbox("Number of Passenger Vehicles", list(range(1, 11)))

def trailer_cost(km):
    return TRAILER_BASE_COST if km <= TRAILER_KM_THRESHOLD else TRAILER_BASE_COST + (km - TRAILER_KM_THRESHOLD) * TRAILER_KM_RATE

trailer_total = sum([trailer_cost(km) for km in [excavator_km, skid_km, truck_km]])
passenger_total = passenger_km * passenger_vehicles * PASSENGER_KM_RATE

# Gravel
st.header("🪨 Gravel Base")
gravel_depth_inches = 6
gravel_depth_ft = gravel_depth_inches / 12
gravel_volume_yd3 = (sqft * 1.25 * gravel_depth_ft) / 27
gravel_loads = math.ceil(gravel_volume_yd3 / 3)
gravel_base_cost = gravel_loads * GRAVEL_COST_PER_LOAD

extra_gravel_loads = st.selectbox("Add Extra Gravel Loads", list(range(0, 6)))
extra_gravel_price = st.number_input("Price per Extra Load ($)", value=250)
extra_gravel_km = st.number_input("Extra Gravel Delivery KM", value=30)
extra_gravel_cost = (extra_gravel_loads * extra_gravel_price) + max(0, (extra_gravel_km - 30)) * 4.20

# Edge Restraint
st.header("🧱 Concrete Edge Restraint")
edge_units = math.ceil(sqft / 100)
edge_cost = edge_units * EDGE_RESTRAINT_COST
edge_cost_with_tax = round(edge_cost * (1 + TAX_RATE))

# Inlay Options
st.header("🎨 Inlay Options")
inlay_full = st.checkbox("Add Full Inlay ($4000 + HST)")
inlay_simple = st.checkbox("Add Simple Inlay - No Background or Border ($2850 + HST)")
inlay_cost = 0
if inlay_full:
    inlay_cost += INLAY_COST_FULL * (1 + TAX_RATE)
if inlay_simple:
    inlay_cost += INLAY_COST_SIMPLE * (1 + TAX_RATE)

# Polymeric Sand
st.header("🌾 Polymeric Sand")
sand_type = st.selectbox("Sand Type", ["None", "$50+tax per bag", "$75+tax per bag"])
sand_cost = 0
bags_needed = math.ceil(sqft / 80) if sand_type != "None" else 0
if sand_type == "$50+tax per bag":
    sand_cost = round(bags_needed * 50 * (1 + TAX_RATE))
elif sand_type == "$75+tax per bag":
    sand_cost = round(bags_needed * 75 * (1 + TAX_RATE))

# Overnight Stay
st.header("🏨 Overnight Stay")
room_cost = st.number_input("Room Cost ($)", value=0)
overnight_laborers = st.selectbox("Laborers Staying Overnight", list(range(0, 11)))
overnight_food_total = overnight_laborers * MEAL_COST_PER_LABORER * (1 + TAX_RATE)
overnight_total = round(room_cost + overnight_food_total)

# Material
material = calculate_material_cost(selected_product, sqft, paver_data, margin_override=margin)

# Totals
subtotal = (
    material["material_total"] + edge_cost_with_tax + gravel_base_cost +
    labor_total + equipment_total_with_tax + trailer_total +
    passenger_total + extra_gravel_cost + sand_cost + inlay_cost + overnight_total
)
hst = round(subtotal * TAX_RATE)
grand_total = round(subtotal + hst)

# --- Output ---
st.markdown("## 📋 Estimate Summary")
st.write(f"**Material ({selected_product})**: ${material['material_total']}")
st.write(f"**Edge Restraint:** ${edge_cost_with_tax}")
st.write(f"**Gravel (Base):** ${gravel_base_cost}")
st.write(f"**Extra Gravel Loads:** ${extra_gravel_cost}")
st.write(f"**Labor:** ${labor_total}")
st.write(f"**Equipment:** ${equipment_total_with_tax}")
st.write(f"**Trailer Transport:** ${trailer_total}")
st.write(f"**Passenger Travel:** ${passenger_total}")
if sand_cost:
    st.write(f"**Polymeric Sand ({bags_needed} bags):** ${sand_cost}")
if inlay_cost:
    st.write(f"**Inlay:** ${inlay_cost}")
if overnight_total:
    st.write(f"**Overnight Stay Total:** ${overnight_total}")

st.markdown("---")
st.write(f"**Subtotal:** ${subtotal}")
st.write(f"**HST (15%):** ${hst}")
st.markdown(f"### 💰 Final Total: ${grand_total}")
