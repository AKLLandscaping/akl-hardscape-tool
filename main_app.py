import streamlit as st
from utils import (
    calculate_sod_needs,
    calculate_equipment_cost,
    calculate_trailer_cost,
    calculate_passenger_vehicle_cost,
    calculate_total_quote
)

st.set_page_config(page_title="🌱 AKL Sod Estimate Tool", layout="centered")
st.title("🌱 AKL Sod Installation Quote")
st.markdown("---")

# -----------------------------
# 👤 Client Information
# -----------------------------
st.header("👤 Client Information")
client_name = st.text_input("Client Name")
address = st.text_input("Job Site Address")
phone = st.text_input("Phone Number")
email = st.text_input("Email Address")

st.markdown("---")

# -----------------------------
# 📐 Job Details
# -----------------------------
st.header("📐 Job Details")
sqft_needed = st.number_input("Total Square Footage of Sod Needed", min_value=0)
distance_km = st.number_input("One-Way Travel Distance to Site (km)", min_value=0)
laborers = st.slider("Number of Laborers", 1, 10, 2)

st.markdown("---")

# -----------------------------
# 🚜 Equipment Usage
# -----------------------------
st.subheader("🚜 Equipment Usage (Hourly)")
excavator_hrs = st.number_input("Excavator Hours", min_value=0, step=1)
skidsteer_hrs = st.number_input("Skid Steer Hours", min_value=0, step=1)
dumptruck_hrs = st.number_input("Dump Truck Hours", min_value=0, step=1)

st.markdown("---")

# -----------------------------
# 🛻 Trailer Delivery
# -----------------------------
st.subheader("🛻 Trailer Delivery Per Machine")
excavator_trailer_km = st.number_input("Trailer Round Trip Distance for Excavator (km)", min_value=0)
skidsteer_trailer_km = st.number_input("Trailer Round Trip Distance for Skid Steer (km)", min_value=0)
dumptruck_trailer_km = st.number_input("Trailer Round Trip Distance for Dump Truck (km)", min_value=0)

# Passenger vehicle travel
total_passenger_km = st.number_input("Passenger Vehicle Round Trip Distance (km)", min_value=0)
num_passenger_vehicles = st.selectbox("Number of Passenger Vehicles", options=list(range(1, 11)), index=0)

st.markdown("---")

# -----------------------------
# 📊 Estimate Summary
# -----------------------------
st.subheader("📊 Estimate Summary")

pallets, sod_cost = calculate_sod_needs(sqft_needed)
equipment_cost = calculate_equipment_cost(excavator_hrs, skidsteer_hrs, dumptruck_hrs)
trailer_cost = calculate_trailer_cost(excavator_trailer_km, skidsteer_trailer_km, dumptruck_trailer_km)
vehicle_cost = calculate_passenger_vehicle_cost(total_passenger_km, num_passenger_vehicles)
total, hst, grand_total = calculate_total_quote(sod_cost, equipment_cost, trailer_cost, vehicle_cost)

st.markdown(f"**Number of Pallets:** {pallets}")
st.markdown(f"**Sod Material Cost:** ${sod_cost:,.2f}")
st.markdown(f"**Labor Cost (not shown here):** add-on later")
st.markdown(f"**Equipment Cost:** ${equipment_cost:,.2f}")
st.markdown(f"**Trailer Delivery:** ${trailer_cost:,.2f}")
st.markdown(f"**Passenger Vehicle Travel:** ${vehicle_cost:,.2f}")
st.markdown(f"**Subtotal:** ${total:,.2f}")
st.markdown(f"**HST (15%):** ${hst:,.2f}")
st.success(f"**Total Estimate: ${grand_total:,.2f}**")

# Footer branding
st.markdown("---")
st.caption("Built for AKL Landscaping · www.AKLLandscaping.com · 📞 902-802-4563")
