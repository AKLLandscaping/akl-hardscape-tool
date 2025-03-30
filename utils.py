
import streamlit as st
import pandas as pd

def load_shaw_products():
    return pd.read_excel("shaw_products.xlsx")

def labor_input():
    st.subheader("👷 Labor")
    labor_data = []
    num_laborers = st.number_input("Number of Laborers", 1, 10, 1)
    for i in range(num_laborers):
        cols = st.columns([2, 2, 2])
        name = cols[0].text_input(f"Laborer #{i+1} Name", key=f"name_{i}")
        rate = cols[1].selectbox(f"Hourly Rate for {name or f'Worker {i+1}'}", [35, 40, 45, 50, 55, 60, 65], key=f"rate_{i}")
        hours = cols[2].number_input(f"Hours Worked by {name or f'Worker {i+1}'}", min_value=0.0, value=8.0, key=f"hours_{i}")
        labor_data.append({"name": name, "rate": rate, "hours": hours})
    return labor_data

def equipment_input():
    st.subheader("🚜 Equipment Hours")
    excavator = st.number_input("Excavator Hours", 0.0, 24.0, 0.0)
    skid_steer = st.number_input("Skid Steer Hours", 0.0, 24.0, 0.0)
    dump_truck = st.number_input("Dump Truck Hours", 0.0, 24.0, 0.0)
    return {"excavator": excavator, "skid_steer": skid_steer, "dump_truck": dump_truck}

def travel_input():
    st.subheader("🚗 Travel")
    trailer_km = st.number_input("Trailer Transport Distance (km)", 0.0, 500.0, 0.0)
    vehicle_km = st.number_input("Passenger Vehicle Distance (km)", 0.0, 500.0, 0.0)
    return {"trailer_km": trailer_km, "vehicle_km": vehicle_km}

def calculate_walkway_cost(shaw_data):
    st.header("🚶 Walkway Calculator")

    walkway_products = shaw_data[shaw_data['Section'] == "Walkway"]
    product = st.selectbox("Choose Material", walkway_products['Product Name'].unique())
    sqft = st.number_input("Square Footage", min_value=0.0, value=100.0)

    selected = walkway_products[walkway_products["Product Name"] == product].iloc[0]
    unit_price = selected["Contractor Price"]
    unit_type = selected["Unit Type"]
    pallet_qty = selected["Pallet Quantity"]

    material_cost = sqft * unit_price
    st.write(f"Material Cost (@ ${unit_price}/{unit_type}): ${material_cost:,.2f}")

    # Pallets
    per_pallet_coverage = pallet_qty if unit_type == "sft" else 1
    pallets_needed = -(-sqft // per_pallet_coverage)
    pallet_charge = st.checkbox("Include Pallet Charge ($25 each)", value=True)
    lifter_rental = st.checkbox("Include Lifter Rental ($100)", value=False)
    pallet_cost = (pallets_needed * 25 if pallet_charge else 0) + (100 if lifter_rental else 0)

    # Gravel Base
    st.subheader("🪨 Gravel Base")
    include_gravel = st.checkbox("Include Gravel Base", value=True)
    gravel_depth_in = st.number_input("Gravel Depth (inches)", 0.0, 24.0, 6.0)
    gravel_volume_y3 = 0
    gravel_cost = 0
    if include_gravel:
        cubic_ft = sqft * 1.25 * (gravel_depth_in / 12)
        gravel_volume_y3 = cubic_ft / 27
        gravel_loads = -(-gravel_volume_y3 // 3)
        gravel_cost = gravel_loads * 250
        st.write(f"Gravel Volume: {gravel_volume_y3:.2f} yd³ → Loads: {gravel_loads}, Cost: ${gravel_cost:,.2f}")

    # Geotextile
    fabric_cost = 0
    if st.checkbox("Include Geotextile Fabric ($0.50/sq ft)", value=True):
        fabric_cost = sqft * 0.50

    # Polymeric Sand
    st.subheader("🧪 Polymeric Sand")
    bags = -(-sqft // 80)
    sand_cost = bags * 50
    st.write(f"{bags} bags needed @ $50/bag → ${sand_cost:,.2f}")

    # Labor, Equipment, Travel
    labor_data = labor_input()
    labor_cost = sum([l["rate"] * l["hours"] for l in labor_data])
    equipment = equipment_input()
    equipment_cost = equipment["excavator"] * 130 + equipment["skid_steer"] * 110 + equipment["dump_truck"] * 100
    travel = travel_input()
    trailer_cost = (travel["trailer_km"] / 25) * 250
    vehicle_cost = travel["vehicle_km"] * 0.80

    subtotal = sum([material_cost, pallet_cost, gravel_cost, fabric_cost, sand_cost, labor_cost, equipment_cost, trailer_cost, vehicle_cost])
    hst = subtotal * 0.15
    total = subtotal + hst

    st.subheader("💰 Walkway Section Total")
    st.write(f"Subtotal: ${subtotal:,.2f}")
    st.write(f"HST (15%): ${hst:,.2f}")
    st.success(f"Total: ${total:,.2f}")

    return total

def calculate_wall_cost(shaw_data):
    st.header("🧱 Retaining Wall Calculator")

    wall_products = shaw_data[shaw_data['Section'] == "Retaining Wall"]
    product = st.selectbox("Choose Wall Material", wall_products['Product Name'].unique())
    wall_length = st.number_input("Wall Length (ft)", min_value=0.0, value=20.0)
    wall_height = st.number_input("Wall Height (ft)", min_value=0.0, value=3.0)

    selected = wall_products[wall_products["Product Name"] == product].iloc[0]
    unit_price = selected["Contractor Price"]
    unit_type = selected["Unit Type"]
    pallet_qty = selected["Pallet Quantity"]

    face_sqft = wall_length * wall_height
    material_cost = face_sqft * unit_price
    st.write(f"Wall Face Area: {face_sqft:.2f} sq ft @ ${unit_price}/{unit_type} = ${material_cost:,.2f}")

    # Pallets
    per_pallet_coverage = pallet_qty if unit_type == "sft" else 1
    pallets_needed = -(-face_sqft // per_pallet_coverage)
    pallet_charge = st.checkbox("Include Pallet Charge ($25 each)", value=True, key="wall_pallet")
    lifter_rental = st.checkbox("Include Lifter Rental ($100)", value=False, key="wall_lifter")
    pallet_cost = (pallets_needed * 25 if pallet_charge else 0) + (100 if lifter_rental else 0)

    # Gravel Base
    st.subheader("🪨 Gravel Base")
    include_gravel = st.checkbox("Include Gravel Base", value=True, key="wall_gravel")
    gravel_depth_in = st.number_input("Gravel Depth (inches)", 0.0, 24.0, 12.0, key="wall_gravel_depth")
    gravel_volume_y3 = 0
    gravel_cost = 0
    if include_gravel:
        cubic_ft = face_sqft * 1.25 * (gravel_depth_in / 12)
        gravel_volume_y3 = cubic_ft / 27
        gravel_loads = -(-gravel_volume_y3 // 3)
        gravel_cost = gravel_loads * 250
        st.write(f"Gravel Volume: {gravel_volume_y3:.2f} yd³ → Loads: {gravel_loads}, Cost: ${gravel_cost:,.2f}")

    # Geotextile
    fabric_cost = 0
    if st.checkbox("Include Geotextile Fabric ($0.50/sq ft)", value=True, key="wall_fabric"):
        fabric_cost = face_sqft * 0.5

    # Drain Stone
    st.subheader("🪨 Drain Stone Behind Wall")
    drainstone_volume = (wall_height * wall_length * 2) / 27  # 24" deep x full height
    loads_needed = -(-drainstone_volume // 3)
    drainstone_cost = loads_needed * 250
    st.write(f"Drain Stone Volume: {drainstone_volume:.2f} yd³ → Loads: {loads_needed}, Cost: ${drainstone_cost:,.2f}")

    # Engineering if wall > 8ft
    engineer_cost = 0
    if wall_height > 8:
        st.warning("Wall is over 8 ft — Engineer Required")
        engineer_cost = 1500

    # Cap Block + Adhesive
    st.subheader("🧱 Cap Block + Adhesive")
    cap_length = st.number_input("Linear Feet of Cap Blocks", 0.0, 200.0, wall_length, key="cap_length")
    cap_price = 6.00  # placeholder
    adhesive_tubes = -(-cap_length // 20)
    adhesive_cost = adhesive_tubes * 15
    cap_block_cost = cap_length * cap_price
    st.write(f"Cap Block Cost: ${cap_block_cost:,.2f}, Adhesive: {adhesive_tubes} tubes = ${adhesive_cost:,.2f}")

    # Labor, Equipment, Travel
    labor_data = labor_input()
    labor_cost = sum([l["rate"] * l["hours"] for l in labor_data])
    equipment = equipment_input()
    equipment_cost = equipment["excavator"] * 130 + equipment["skid_steer"] * 110 + equipment["dump_truck"] * 100
    travel = travel_input()
    trailer_cost = (travel["trailer_km"] / 25) * 250
    vehicle_cost = travel["vehicle_km"] * 0.80

    subtotal = sum([
        material_cost, pallet_cost, gravel_cost, fabric_cost,
        drainstone_cost, engineer_cost, cap_block_cost,
        adhesive_cost, labor_cost, equipment_cost, trailer_cost, vehicle_cost
    ])
    hst = subtotal * 0.15
    total = subtotal + hst

    st.subheader("💰 Retaining Wall Section Total")
    st.write(f"Subtotal: ${subtotal:,.2f}")
    st.write(f"HST (15%): ${hst:,.2f}")
    st.success(f"Total: ${total:,.2f}")

    return total

def calculate_steps_cost(shaw_data):
    st.header("🪜 Steps Calculator")

    step_products = shaw_data[shaw_data['Section'] == "Steps"]
    product = st.selectbox("Choose Step Material", step_products['Product Name'].unique())
    num_steps = st.number_input("Number of Steps", min_value=0, value=3)

    selected = step_products[step_products["Product Name"] == product].iloc[0]
    unit_price = selected["Contractor Price"]
    unit_type = selected["Unit Type"]
    pallet_qty = selected["Pallet Quantity"]

    material_cost = num_steps * unit_price
    st.write(f"Material Cost: {num_steps} steps @ ${unit_price}/{unit_type} = ${material_cost:,.2f}")

    # Pallets
    pallets_needed = -(-num_steps // pallet_qty)
    pallet_charge = st.checkbox("Include Pallet Charge ($25 each)", value=True, key="step_pallet")
    lifter_rental = st.checkbox("Include Lifter Rental ($100)", value=False, key="step_lifter")
    pallet_cost = (pallets_needed * 25 if pallet_charge else 0) + (100 if lifter_rental else 0)

    # Gravel Base
    gravel_cost = 0
    fabric_cost = 0
    st.subheader("🪨 Base Preparation")
    on_gravel = st.radio("Install On:", ["Gravel Base", "Existing Ground"], key="step_base")
    if on_gravel == "Gravel Base":
        gravel_depth_in = st.number_input("Gravel Depth (inches)", 0.0, 24.0, 12.0, key="step_gravel_depth")
        cubic_ft = num_steps * 4 * 4 * (gravel_depth_in / 12) * 1.25
        gravel_volume_y3 = cubic_ft / 27
        gravel_loads = -(-gravel_volume_y3 // 3)
        gravel_cost = gravel_loads * 250
        st.write(f"Gravel Volume: {gravel_volume_y3:.2f} yd³ → Loads: {gravel_loads}, Cost: ${gravel_cost:,.2f}")

        if st.checkbox("Include Geotextile Fabric ($0.50/sq ft)", value=True, key="step_fabric"):
            fabric_cost = num_steps * 16 * 0.5  # 4'x4' step area

    # Adhesive
    st.subheader("🧱 Adhesive")
    lf_of_steps = num_steps * 4
    adhesive_tubes = -(-lf_of_steps // 20)
    adhesive_cost = adhesive_tubes * 15
    st.write(f"Adhesive: {adhesive_tubes} tubes = ${adhesive_cost:,.2f}")

    # Labor, Equipment, Travel
    labor_data = labor_input()
    labor_cost = sum([l["rate"] * l["hours"] for l in labor_data])
    equipment = equipment_input()
    equipment_cost = equipment["excavator"] * 130 + equipment["skid_steer"] * 110 + equipment["dump_truck"] * 100
    travel = travel_input()
    trailer_cost = (travel["trailer_km"] / 25) * 250
    vehicle_cost = travel["vehicle_km"] * 0.80

    subtotal = sum([
        material_cost, pallet_cost, gravel_cost, fabric_cost,
        adhesive_cost, labor_cost, equipment_cost, trailer_cost, vehicle_cost
    ])
    hst = subtotal * 0.15
    total = subtotal + hst

    st.subheader("💰 Steps Section Total")
    st.write(f"Subtotal: ${subtotal:,.2f}")
    st.write(f"HST (15%): ${hst:,.2f}")
    st.success(f"Total: ${total:,.2f}")

    return total

def calculate_firepit_cost(shaw_data):
    st.header("🔥 Fire Pit Calculator")

    fire_products = shaw_data[shaw_data['Section'] == "Fire Pit"]
    product = st.selectbox("Choose Fire Pit Kit", fire_products['Product Name'].unique())
    num_pits = st.number_input("Number of Fire Pits", min_value=0, value=1)

    selected = fire_products[fire_products["Product Name"] == product].iloc[0]
    unit_price = selected["Contractor Price"]
    unit_type = selected["Unit Type"]
    pallet_qty = selected["Pallet Quantity"]

    material_cost = num_pits * unit_price
    st.write(f"Material Cost: {num_pits} x ${unit_price} = ${material_cost:,.2f}")

    # Pallets
    pallets_needed = -(-num_pits // pallet_qty)
    pallet_charge = st.checkbox("Include Pallet Charge ($25 each)", value=True, key="pit_pallet")
    lifter_rental = st.checkbox("Include Lifter Rental ($100)", value=False, key="pit_lifter")
    pallet_cost = (pallets_needed * 25 if pallet_charge else 0) + (100 if lifter_rental else 0)

    # Gravel Base
    st.subheader("🪨 Gravel Base")
    include_gravel = st.checkbox("Include Gravel Base", value=True, key="pit_gravel")
    gravel_depth_in = st.number_input("Gravel Depth (inches)", 0.0, 24.0, 6.0, key="pit_gravel_depth")
    gravel_volume_y3 = 0
    gravel_cost = 0
    if include_gravel:
        cubic_ft = num_pits * 4 * 4 * (gravel_depth_in / 12) * 1.25
        gravel_volume_y3 = cubic_ft / 27
        gravel_loads = -(-gravel_volume_y3 // 3)
        gravel_cost = gravel_loads * 250
        st.write(f"Gravel Volume: {gravel_volume_y3:.2f} yd³ → Loads: {gravel_loads}, Cost: ${gravel_cost:,.2f}")

        if st.checkbox("Include Geotextile Fabric ($0.50/sq ft)", value=True, key="pit_fabric"):
            fabric_cost = num_pits * 16 * 0.5  # 4'x4' pit area
        else:
            fabric_cost = 0
    else:
        fabric_cost = 0

    # Adhesive
    st.subheader("🧱 Adhesive")
    lf_of_blocks = num_pits * 10
    adhesive_tubes = -(-lf_of_blocks // 20)
    adhesive_cost = adhesive_tubes * 15
    st.write(f"Adhesive: {adhesive_tubes} tubes = ${adhesive_cost:,.2f}")

    # Fill Material
    st.subheader("🔥 Optional Fill")
    fill_type = st.selectbox("Interior Fill Material", ["None", "Lava Rock", "Gravel"], key="pit_fill")
    fill_cost = 0
    if fill_type != "None":
        cubic_yards = st.number_input(f"{fill_type} Volume (yd³)", min_value=0.0, value=0.5)
        fill_cost = cubic_yards * 200
        st.write(f"{fill_type} Cost: ${fill_cost:,.2f}")

    # Labor, Equipment, Travel
    labor_data = labor_input()
    labor_cost = sum([l["rate"] * l["hours"] for l in labor_data])
    equipment = equipment_input()
    equipment_cost = equipment["excavator"] * 130 + equipment["skid_steer"] * 110 + equipment["dump_truck"] * 100
    travel = travel_input()
    trailer_cost = (travel["trailer_km"] / 25) * 250
    vehicle_cost = travel["vehicle_km"] * 0.80

    subtotal = sum([
        material_cost, pallet_cost, gravel_cost, fabric_cost,
        adhesive_cost, fill_cost, labor_cost,
        equipment_cost, trailer_cost, vehicle_cost
    ])
    hst = subtotal * 0.15
    total = subtotal + hst

    st.subheader("💰 Fire Pit Section Total")
    st.write(f"Subtotal: ${subtotal:,.2f}")
    st.write(f"HST (15%): ${hst:,.2f}")
    st.success(f"Total: ${total:,.2f}")

    return total

def calculate_grand_total(walkway_total, wall_total, steps_total, firepit_total):
    st.header("📊 Project Quote Summary")

    subtotal = sum([walkway_total, wall_total, steps_total, firepit_total])
    hst = subtotal * 0.15
    total = subtotal + hst

    st.write(f"Walkway Total: ${walkway_total:,.2f}")
    st.write(f"Retaining Wall Total: ${wall_total:,.2f}")
    st.write(f"Steps Total: ${steps_total:,.2f}")
    st.write(f"Fire Pit Total: ${firepit_total:,.2f}")
    st.subheader("🔢 Final Totals")
    st.write(f"Subtotal: ${subtotal:,.2f}")
    st.write(f"HST (15%): ${hst:,.2f}")
    st.success(f"Grand Total: ${total:,.2f}")

    return {
        "subtotal": subtotal,
        "hst": hst,
        "total": total
    }
