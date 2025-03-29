
import streamlit as st

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="wide")

# Branding and contact header
st.markdown("""
<div style='display: flex; justify-content: space-between; align-items: center; background-color: #1a1a1a; padding: 1rem; border-radius: 16px; margin-bottom: 1rem;'>
    <img src='https://i.imgur.com/OMb9dKn.png' height='60' style='margin-right: 1rem;'>
    <img src='https://i.imgur.com/3DT9Z4H.png' height='50' style='margin-right: 1rem;'>
    <img src='https://i.imgur.com/HgClBqG.png' height='40' style='margin-right: auto;'>
    <div style='text-align: right; color: white;'>
        <div style='font-size: 1.2rem;'><strong>📞 902-802-4563</strong></div>
        <div style='font-size: 0.9rem;'>🌐 <a href="https://www.akllandscaping.com" style="color:#00ff88;">www.AKLLandscaping.com</a></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("🧱 AKL Hardscape Master Tool")

# Section selector
section = st.sidebar.radio("📂 Select Project Section", ["Walkway", "Retaining Wall", "Steps", "Fire Pit"])

# Initialize totals for session
if "totals" not in st.session_state:
    st.session_state["totals"] = {}

# Walkway
if section == "Walkway":
    st.header("🚶 Walkway Calculator")
    sq_ft = st.number_input("Square Feet", min_value=0)
    mat_cost = st.number_input("Material Cost per sq ft", value=10.0)
    labor_rate = st.number_input("Labor Rate per Hour", value=65.0)
    hours = st.number_input("Estimated Labor Hours", value=8.0)
    total = (sq_ft * mat_cost) + (labor_rate * hours)
    hst = total * 0.15
    final = total + hst
    st.success(f"Total: ${final:,.2f} (includes HST ${hst:,.2f})")
    st.session_state["totals"]["Walkway"] = final

# Retaining Wall
elif section == "Retaining Wall":
    st.header("🧱 Retaining Wall Calculator")
    length = st.number_input("Wall Length (ft)", min_value=0)
    height = st.number_input("Wall Height (ft)", min_value=0)
    mat_cost = st.number_input("Material Cost per sq ft", value=12.0)
    labor_rate = st.number_input("Labor Rate per Hour", value=65.0)
    hours = st.number_input("Estimated Labor Hours", value=10.0)
    face_area = length * height
    total = (face_area * mat_cost) + (labor_rate * hours)
    hst = total * 0.15
    final = total + hst
    st.success(f"Total: ${final:,.2f} (includes HST ${hst:,.2f})")
    st.session_state["totals"]["Retaining Wall"] = final

# Steps
elif section == "Steps":
    st.header("🪜 Steps Calculator")
    steps = st.number_input("Number of Steps", min_value=0)
    cost_per = st.number_input("Cost per Step", value=150.0)
    labor_rate = st.number_input("Labor Rate per Hour", value=65.0)
    hours = st.number_input("Estimated Labor Hours", value=4.0)
    total = (steps * cost_per) + (labor_rate * hours)
    hst = total * 0.15
    final = total + hst
    st.success(f"Total: ${final:,.2f} (includes HST ${hst:,.2f})")
    st.session_state["totals"]["Steps"] = final

# Fire Pit
elif section == "Fire Pit":
    st.header("🔥 Fire Pit Calculator")
    fire_type = st.selectbox("Fire Pit Type", ["Precast Kit", "Custom Stone", "Block Circle"])
    base_cost = {"Precast Kit": 800, "Custom Stone": 1200, "Block Circle": 1000}[fire_type]
    labor_rate = st.number_input("Labor Rate per Hour", value=65.0)
    hours = st.number_input("Estimated Labor Hours", value=5.0)
    total = base_cost + (labor_rate * hours)
    hst = total * 0.15
    final = total + hst
    st.success(f"Total: ${final:,.2f} (includes HST ${hst:,.2f})")
    st.session_state["totals"]["Fire Pit"] = final

# Grand total button
if st.sidebar.button("📊 View Grand Total"):
    totals = st.session_state.get("totals", {})
    if totals:
        st.markdown("### 🧾 Project Totals Summary")
        for k, v in totals.items():
            st.write(f"✅ {k}: ${v:,.2f}")
        grand = sum(totals.values())
        st.markdown("---")
        st.success(f"💵 Grand Total: ${grand:,.2f}")
    else:
        st.warning("Add at least one section quote to view the total.")
