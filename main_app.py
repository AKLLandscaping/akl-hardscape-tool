
import streamlit as st
from utils import (
    load_shaw_products,
    calculate_walkway_cost,
    calculate_wall_cost,
    calculate_steps_cost,
    calculate_firepit_cost,
    calculate_grand_total
)

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="wide")
st.title("🧱 AKL Hardscape Master Tool")

# Sidebar Navigation
section = st.sidebar.radio("📂 Select Project Section", [
    "Walkway", "Retaining Wall", "Steps", "Fire Pit", "📄 Quote Preview"
])

# Load product data
shaw_data = load_shaw_products()

# Totals per section (persist across reruns using session state)
if "walkway_total" not in st.session_state: st.session_state.walkway_total = 0
if "wall_total" not in st.session_state: st.session_state.wall_total = 0
if "steps_total" not in st.session_state: st.session_state.steps_total = 0
if "firepit_total" not in st.session_state: st.session_state.firepit_total = 0

# Run selected section
if section == "Walkway":
    st.session_state.walkway_total = calculate_walkway_cost(shaw_data)
elif section == "Retaining Wall":
    st.session_state.wall_total = calculate_wall_cost(shaw_data)
elif section == "Steps":
    st.session_state.steps_total = calculate_steps_cost(shaw_data)
elif section == "Fire Pit":
    st.session_state.firepit_total = calculate_firepit_cost(shaw_data)
elif section == "📄 Quote Preview":
    st.header("🧾 Quote Preview")
    client_name = st.text_input("Client Name")
    job_address = st.text_input("Job Site Address")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")

    st.markdown("---")
    totals = calculate_grand_total(
        st.session_state.walkway_total,
        st.session_state.wall_total,
        st.session_state.steps_total,
        st.session_state.firepit_total
    )

    st.markdown("---")
    st.subheader("✅ Client Info")
    st.write(f"**Name:** {client_name}")
    st.write(f"**Address:** {job_address}")
    st.write(f"**Phone:** {phone}")
    st.write(f"**Email:** {email}")

    st.markdown("---")
    st.success(f"Final Grand Total: ${totals['total']:,.2f}")
