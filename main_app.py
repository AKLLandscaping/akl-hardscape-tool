import streamlit as st
import pandas as pd
import math
from utils import load_paver_data, calculate_material_cost

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="wide")

st.title("🧱 AKL Hardscape Master Tool")
st.header("🧍‍♂️ Walkway Estimator")

# Inputs
sqft = st.number_input("📏 Square Feet", min_value=0, value=0, step=10)
margin = st.slider("📊 Override Margin %", 0, 100, 30)

data = load_paver_data()
product = st.selectbox("🎨 Choose Product", data["Products"].unique())

# Labor
st.subheader("👷 Labor")
num_laborers = st.number_input("Number of Laborers", min_value=1, value=2)
labor_hours = st.number_input("Total Labor Hours", min_value=0.0, value=8.0, step=0.5)
labor_rate = st.number_input("Hourly Pay per Laborer ($)", min_value=0.0, value=50.0, step=5.0)

# Equipment
st.subheader("🚜 Equipment Use")
excavator_hours = st.number_input("Excavator Hours", min_value=0.0, value=0.0, step=0.25)
skid_steer_hours = st.number_input("Skid Steer Hours", min_value=0.0, value=0.0, step=0.25)
dump_truck_hours = st.number_input("Dump Truck Hours", min_value=0.0, value=0.0, step=0.25)

excavator_km = st.number_input("Excavator Trailer Km", min_value=0, value=0)
skid_steer_km = st.number_input("Skid Steer Trailer Km", min_value=0, value=0)
dump_truck_km = st.number_input("Dump Truck Trailer Km", min_value=0, value=0)

# Travel
st.subheader("🚗 Travel")
round_trip_km = st.number_input("Round Trip Distance (km)", min_value=0, value=30)
passenger_vehicles = st.number_input("Number of Passenger Vehicles", min_value=1, value=1)

# Estimate Summary
st.subheader("🧮 Estimate Summary")

try:
    mat = calculate_material_cost(product, sqft, data, margin)

    # Gravel base (6 inches = 0.5 feet deep)
    gravel_depth_ft = 0.5
    gravel_width_ft = math.sqrt(sqft)  # assume square layout for rough calc
    gravel_length_ft = sqft / gravel_width_ft
    cubic_ft = gravel_width_ft * gravel_length_ft * gravel_depth_ft
    gravel_yards = math.ceil(cubic_ft / 27)
    gravel_cost = gravel_yards * 250  # 5-ton load = $250

    # Geotextile fabric
    fabric_cost = sqft * 0.50

    # Labor
    labor_cost = num_laborers * labor_hours * labor_rate

    # Equipment
    equipment_cost = (
        excavator_hours + skid_steer_hours + dump_truck_hours
    ) * 130

    # Trailer transport
    trailer_cost = 0
    for km in [excavator_km, skid_steer_km, dump_truck_km]:
        if km > 30:
            trailer_cost += 250 + ((km - 30) * 4.2)
        elif km > 0:
            trailer_cost += 250

    # Travel cost (passenger vehicles)
    travel_cost = passenger_vehicles * round_trip_km * 0.80

    subtotal = (
        mat["material_total"]
        + labor_cost
        + equipment_cost
        + trailer_cost
        + travel_cost
        + gravel_cost
        + fabric_cost
    )

    tax = subtotal * 0.15
    total = subtotal + tax

    st.markdown(f"**Product:** {product}")
    st.markdown(f"**Price per Unit (with margin):** ${mat['unit_price']}")
    st.markdown(f"**Units Required:** {mat['units_required']}")
    st.markdown(f"**Material Total:** ${mat['material_total']}")
    st.markdown("---")
    st.markdown(f"**Gravel Yards:** {gravel_yards} @ $250/yd = ${gravel_cost}")
    st.markdown(f"**Geotextile Fabric Cost:** ${fabric_cost:.2f}")
    st.markdown(f"**Labor Total:** ${labor_cost:.2f}")
    st.markdown(f"**Equipment Cost:** ${equipment_cost:.2f}")
    st.markdown(f"**Trailer Transport:** ${trailer_cost:.2f}")
    st.markdown(f"**Passenger Vehicle Travel:** ${travel_cost:.2f}")
    st.markdown("---")
    st.markdown(f"**Subtotal:** ${subtotal:.2f}")
    st.markdown(f"**HST (15%):** ${tax:.2f}")
    st.markdown(f"### 💰 Final Total: ${total:.2f}")

except Exception as e:
    st.error(f"Error in calculation: {e}")
