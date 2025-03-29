
import streamlit as st

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="wide")

# Branding banner
st.markdown("""
<div style='display: flex; justify-content: space-between; align-items: center; background-color: #1a1a1a; padding: 1rem; border-radius: 12px;'>
    <img src='https://i.imgur.com/OMb9dKn.png' alt='AKL Landscaping' height='60'>
    <img src='https://i.imgur.com/3DT9Z4H.png' alt='Landscape NS' height='50'>
    <img src='https://i.imgur.com/HgClBqG.png' alt='Almita Piling' height='40'>
    <div style='color: white; text-align: right;'>
        <div style='font-size: 1.1rem;'>📞 <strong>902-802-4563</strong></div>
        <div style='font-size: 0.9rem;'>🌐 <a href="https://www.akllandscaping.com" style="color: #00ff88;">www.AKLLandscaping.com</a></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("🧱 AKL Hardscape Master Tool")

section = st.sidebar.radio("Select Section", ["Walkway", "Retaining Wall", "Steps", "Fire Pit"])

totals = {}

if section == "Walkway":
    st.header("🚶 Walkway Quote")
    sq_ft = st.number_input("Square Feet", min_value=0)
    material_cost = st.number_input("Material Cost per sq ft", value=10.0)
    labor_cost = st.number_input("Labor Rate per Hour", value=65.0)
    hours = st.number_input("Estimated Hours", value=8.0)
    total = (sq_ft * material_cost) + (labor_cost * hours)
    hst = total * 0.15
    st.success(f"Subtotal: ${total:,.2f} | HST: ${hst:,.2f} | Total: ${total + hst:,.2f}")
    totals["Walkway"] = total + hst

elif section == "Retaining Wall":
    st.header("🧱 Retaining Wall Quote")
    length = st.number_input("Wall Length (ft)", min_value=0)
    height = st.number_input("Wall Height (ft)", min_value=0)
    material_cost = st.number_input("Material Cost per sq ft", value=12.0)
    labor_cost = st.number_input("Labor Rate per Hour", value=65.0)
    hours = st.number_input("Estimated Hours", value=10.0)
    face_area = length * height
    total = (face_area * material_cost) + (labor_cost * hours)
    hst = total * 0.15
    st.success(f"Subtotal: ${total:,.2f} | HST: ${hst:,.2f} | Total: ${total + hst:,.2f}")
    totals["Retaining Wall"] = total + hst

elif section == "Steps":
    st.header("🪜 Steps Quote")
    num_steps = st.number_input("Number of Steps", min_value=0)
    cost_per_step = st.number_input("Cost per Step", value=150.0)
    labor_cost = st.number_input("Labor Rate per Hour", value=65.0)
    hours = st.number_input("Estimated Hours", value=4.0)
    total = (num_steps * cost_per_step) + (labor_cost * hours)
    hst = total * 0.15
    st.success(f"Subtotal: ${total:,.2f} | HST: ${hst:,.2f} | Total: ${total + hst:,.2f}")
    totals["Steps"] = total + hst

elif section == "Fire Pit":
    st.header("🔥 Fire Pit Quote")
    type_selected = st.selectbox("Fire Pit Type", ["Precast Kit", "Custom Stone", "Block Circle"])
    base_price = {"Precast Kit": 800, "Custom Stone": 1200, "Block Circle": 1000}[type_selected]
    labor_cost = st.number_input("Labor Rate per Hour", value=65.0)
    hours = st.number_input("Estimated Hours", value=5.0)
    total = base_price + (labor_cost * hours)
    hst = total * 0.15
    st.success(f"Subtotal: ${total:,.2f} | HST: ${hst:,.2f} | Total: ${total + hst:,.2f}")
    totals["Fire Pit"] = total + hst

if st.sidebar.button("📊 View Full Project Total"):
    st.markdown("### 🧾 Grand Total for All Sections")
    grand_total = sum(totals.values())
    for k, v in totals.items():
        st.write(f"{k}: ${v:,.2f}")
    st.markdown("---")
    st.success(f"Grand Total: ${grand_total:,.2f}")
