import streamlit as st
from utils import *

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="centered")
st.title("🧱 AKL Hardscape Master Tool")

section = st.radio("📂 Select Project Section", ["Walkway", "Retaining Wall", "Steps", "Fire Pit", "Quote Preview"])

if section == "Walkway":
    st.header("🚶 Walkway Estimator")

    sqft = st.number_input("📏 Square Feet", min_value=0, value=0)

    # Margin override
    margin_override = st.slider("📊 Override Margin %", 0, 100, 30)

    # Load and select product
    df = load_paver_data()
    product = st.selectbox("🧱 Choose Product", df["Products"].dropna().unique())
    material_cost, unit_price = calculate_material_cost(product, sqft, df, margin_override)

    # Gravel
    st.markdown("### 🪨 Gravel")
    include_gravel = st.checkbox("✅ Include Gravel Base", value=True)
    gravel_depth = st.number_input("Gravel Depth (inches)", min_value=0, max_value=24, value=6)
    gravel_cost = calculate_gravel_cost(sqft, gravel_depth)[0] if include_gravel else 0

    # Fabric
    include_fabric = st.checkbox("✅ Include Geotextile Fabric ($0.50/sq ft)", value=True)
    fabric_cost = calculate_fabric_cost(sqft) if include_fabric else 0

    # Sand
    st.markdown("### 🧪 Polymeric Sand")
    bags, sand_cost = calculate_polymeric_sand(sqft, product)

    # Labor
    st.markdown("### 👷 Labor")
    num_laborers = st.slider("Number of Laborers", 1, 4, 2)
    hours_per = st.number_input("Hours per Laborer", min_value=1, max_value=16, value=8)
    rate = st.selectbox("Hourly Rate", [35, 40, 45, 50, 55, 60, 65])
    labor_cost = calculate_labor_cost(num_laborers, hours_per, rate)

    # Equipment
    st.markdown("### 🚜 Equipment Use")
    excavator_hours = st.number_input("Excavator Hours", value=0.0)
    excavator_km = st.number_input("Excavator Trailer Km", value=0)

    skid_hours = st.number_input("Skid Steer Hours", value=0.0)
    skid_km = st.number_input("Skid Steer Trailer Km", value=0)

    dump_hours = st.number_input("Dump Truck Hours", value=0.0)
    dump_km = st.number_input("Dump Truck Trailer Km", value=0)

    equipment_cost = calculate_equipment_cost([
        excavator_hours, skid_hours, dump_hours
    ])

    trailer_km_total = excavator_km + skid_km + dump_km
    trailer_cost = calculate_trailer_charge(trailer_km_total)

    # Passenger travel
    st.markdown("### 🚗 Passenger Travel")
    passenger_km = st.number_input("Round Trip Distance (km)", value=35)
    passenger_vehicles = st.number_input("Number of Passenger Vehicles", min_value=0, value=1)
    passenger_cost = calculate_passenger_vehicle_cost(passenger_km, passenger_vehicles)

    # Totals
    st.markdown("### 💵 Totals")
    subtotal, hst, grand_total = calculate_total(
        material_cost, gravel_cost, fabric_cost, sand_cost,
        labor_cost, equipment_cost, trailer_cost, passenger_cost
    )

    st.markdown(f"**Material Cost:** ${material_cost:.2f}")
    st.markdown(f"**Gravel Cost:** ${gravel_cost:.2f}")
    st.markdown(f"**Fabric Cost:** ${fabric_cost:.2f}")
    st.markdown(f"**Sand Cost:** ${sand_cost:.2f}")
    st.markdown(f"**Labor Cost:** ${labor_cost:.2f}")
    st.markdown(f"**Equipment Cost:** ${equipment_cost:.2f}")
    st.markdown(f"**Trailer Cost:** ${trailer_cost:.2f}")
    st.markdown(f"**Passenger Travel:** ${passenger_cost:.2f}")
    st.markdown(f"**Subtotal:** ${subtotal:.2f}")
    st.markdown(f"**HST (15%):** ${hst:.2f}")
    st.markdown(f"**Grand Total:** ${grand_total:.2f}")
