import streamlit as st
from utils import (
    load_paver_data,
    calculate_material_cost,
    calculate_gravel_cost,
    calculate_fabric_cost,
    calculate_polymeric_sand,
    calculate_total,
)

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="wide")

st.title("🧱 AKL Hardscape Master Tool")

section = st.radio("📂 Select Project Section", ["Walkway", "Retaining Wall", "Steps", "Fire Pit", "Quote Preview"])

if section == "Walkway":
    st.header("🚶‍♂️ Walkway Estimator")

    # Basic Input
    sqft = st.number_input("📐 Square Feet", min_value=0, value=0, step=1)

    # Margin Override
    margin_override = st.slider("📊 Override Margin %", 0, 100, 30)

    # Load product data
    data = load_paver_data()
    products = data["Products"].dropna().unique().tolist()
    selected_product = st.selectbox("🧱 Choose Product", products)

    # Material Cost
    material_cost = calculate_material_cost(selected_product, sqft, data, margin_override=margin_override)

    # Lifter removed as requested

    # Gravel
    st.subheader("🪨 Gravel")
    include_gravel = st.checkbox("✅ Include Gravel Base", value=True)
    gravel_depth = st.number_input("Gravel Depth (inches)", min_value=0, value=6, step=1)
    gravel_cost = 0
    if include_gravel:
        gravel_cost, gravel_volume, gravel_loads = calculate_gravel_cost(sqft, gravel_depth)

    include_fabric = st.checkbox("✅ Include Geotextile Fabric ($0.50/sq ft)", value=True)
    fabric_cost = calculate_fabric_cost(sqft) if include_fabric else 0

    # Polymeric Sand
    st.subheader("🧪 Polymeric Sand")
    sand_bags, sand_cost = calculate_polymeric_sand(sqft, selected_product)

    # Labor
    st.subheader("👷 Labor")
    num_laborers = st.number_input("Number of Laborers", min_value=1, value=1, step=1)
    laborer_inputs = []
    for i in range(num_laborers):
        col1, col2 = st.columns(2)
        with col1:
            rate = st.number_input(f"Laborer {i+1} Rate ($/hr)", min_value=0, value=35, step=1)
        with col2:
            hours = st.number_input(f"Laborer {i+1} Hours", min_value=0, value=8, step=1)
        laborer_inputs.append((rate, hours))

    labor_cost = sum(rate * hours for rate, hours in laborer_inputs)

    # Equipment Use
    st.subheader("🚜 Equipment Use")

    # Excavator
    excavator_hours = st.number_input("Excavator Hours", min_value=0, step=1)
    excavator_km = st.number_input("Excavator Trailer Km", min_value=0, step=1)

    # Skid Steer
    skid_steer_hours = st.number_input("Skid Steer Hours", min_value=0, step=1)
    skid_steer_km = st.number_input("Skid Steer Trailer Km", min_value=0, step=1)

    # Dump Truck
    dump_truck_hours = st.number_input("Dump Truck Hours", min_value=0, step=1)
    dump_truck_km = st.number_input("Dump Truck Trailer Km", min_value=0, step=1)

    equipment_hourly_cost = 130
    equipment_cost = round(
        (excavator_hours + skid_steer_hours + dump_truck_hours) * equipment_hourly_cost, 2
    )
    equipment_tax = round(equipment_cost * 0.15, 2)
    total_equipment = equipment_cost + equipment_tax

    # Trailer Transport
    st.subheader("🚚 Trailer Transport")
    trailer_total_km = excavator_km + skid_steer_km + dump_truck_km
    if trailer_total_km <= 30:
        trailer_cost = 250
    else:
        extra_km = trailer_total_km - 30
        trailer_cost = 250 + (extra_km * 4.20)
    trailer_cost = round(trailer_cost, 2)
    trailer_tax = round(trailer_cost * 0.15, 2)
    total_trailer = trailer_cost + trailer_tax

    # Passenger Travel
    st.subheader("🚗 Passenger Travel")
    passenger_km = st.number_input("Round Trip Distance (km)", min_value=0, value=0, step=1)
    num_vehicles = st.number_input("Number of Passenger Vehicles", min_value=0, value=1, step=1)
    passenger_cost = round(passenger_km * 2 * num_vehicles * 0.80, 2)

    # Totals
    st.subheader("📊 Summary")
    subtotal, hst, grand_total = calculate_total(
        material_cost,
        gravel_cost,
        fabric_cost,
        sand_cost,
        labor_cost,
        total_equipment,
        total_trailer,
        passenger_cost,
    )

    st.markdown(f"**Material Cost:** ${material_cost:,.2f}")
    st.markdown(f"**Gravel Base:** ${gravel_cost:,.2f}")
    st.markdown(f"**Geotextile Fabric:** ${fabric_cost:,.2f}")
    st.markdown(f"**Polymeric Sand:** ${sand_cost:,.2f} ({sand_bags} bags)")
    st.markdown(f"**Labor Cost:** ${labor_cost:,.2f}")
    st.markdown(f"**Equipment Cost:** ${total_equipment:,.2f}")
    st.markdown(f"**Trailer Transport:** ${total_trailer:,.2f}")
    st.markdown(f"**Passenger Travel:** ${passenger_cost:,.2f}")

    st.markdown("---")
    st.markdown(f"### 💵 Subtotal: ${subtotal:,.2f}")
    st.markdown(f"### 🧾 HST (15%): ${hst:,.2f}")
    st.markdown(f"### ✅ Total: ${grand_total:,.2f}")
