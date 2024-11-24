import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
from streamlit_option_menu import option_menu

# Initialize session state for shared data
if "data" not in st.session_state:
    st.session_state.data = {
        "sensors": [],      # List of sensors (for Supplier Page)
        "actuators": [],    # List of actuators (for OEM Page)
        "feedback": []      # List of feedback (for Retailer Page)
    }

# Sidebar for navigation
with st.sidebar:
    page = option_menu(
        menu_title="Navigation",
        options=["Supplier Page", "OEM Page", "Retailer Page"],
        
    )

# Utility function to display dynamic tables
def display_dynamic_table(data, key):
    if not data:
        st.info(f"No {key} data available yet.")
    else:
        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(data)
        
        # Use GridOptionsBuilder to customize Ag-Grid
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)  # Enable pagination
        gb.configure_default_column(resizable=True, sortable=True, filterable=True)  # Make columns interactive
        grid_options = gb.build()
        
        # Display the Ag-Grid table
        AgGrid(df, gridOptions=grid_options, fit_columns_on_grid_load=True)

# ---------------------- Supplier Page ----------------------
if page == "Supplier Page":
    st.image("assets/supplier_icon.png", width=100)
    st.title("📦 Supplier Dashboard")
    st.markdown("""
    ### Manage Sensors Inventory
    Use this dashboard to **add new sensors**, update their status, and view the current stock.
    """)
    st.write("---")

    # Form to add or update sensors
    with st.form("add_sensor_form"):
        col1, col2 = st.columns(2)

        with col1:
            sensor_id = st.text_input("Sensor ID", placeholder="Enter sensor ID to add or update")
            batch_number = st.text_input("Batch Number")
            status = st.selectbox("Status", ["In Stock", "Shipped", "Repaired"])

        with col2:
            manufacturer_date = st.date_input("Manufacture Date")
            shipment_date = st.date_input("Shipment Date")

        submit = st.form_submit_button("Add or Update Sensor")

        if submit:
            # Check if the sensor ID already exists
            existing_sensor = next((s for s in st.session_state.data["sensors"] if s["sensor_id"] == sensor_id), None)
            if existing_sensor:
                # Update existing sensor
                existing_sensor.update({
                    "batch_number": batch_number,
                    "status": status,
                    "manufacturer_date": manufacturer_date,
                    "shipment_date": shipment_date,
                })
                st.success(f"Sensor with ID '{sensor_id}' updated successfully!")
            else:
                # Add new sensor
                st.session_state.data["sensors"].append({
                    "sensor_id": sensor_id,
                    "batch_number": batch_number,
                    "status": status,
                    "manufacturer_date": manufacturer_date,
                    "shipment_date": shipment_date
                })
                st.success("Sensor added successfully!")

    # Display dynamic table for sensors
    st.write("### Current Sensors")
    display_dynamic_table(st.session_state.data["sensors"], "sensor")

# ---------------------- OEM Page ----------------------
elif page == "OEM Page":
    st.title("🔧 OEM Dashboard")
    st.markdown("""
    ### Assemble Actuators
    Track and manage the integration of sensors into actuators.
    """)
    st.write("---")

    # Form to assemble or update actuators
    with st.form("assemble_actuator_form"):
        col1, col2 = st.columns(2)

        with col1:
            actuator_id = st.text_input("Actuator ID", placeholder="Enter actuator ID to add or update")
            sensor_id = st.selectbox(
                "Select Sensor", 
                [s["sensor_id"] for s in st.session_state.data["sensors"]]
                if st.session_state.data["sensors"] else ["No sensors available"]
            )

        with col2:
            assembly_date = st.date_input("Assembly Date")
            status = st.selectbox("Status", ["Assembled", "Shipped"])

        submit = st.form_submit_button("Add or Update Actuator")

        if submit:
            # Check if the actuator ID already exists
            existing_actuator = next((a for a in st.session_state.data["actuators"] if a["actuator_id"] == actuator_id), None)
            if existing_actuator:
                # Update existing actuator
                existing_actuator.update({
                    "sensor_id": sensor_id,
                    "assembly_date": assembly_date,
                    "status": status,
                })
                st.success(f"Actuator with ID '{actuator_id}' updated successfully!")
            elif sensor_id == "No sensors available":
                st.error("No sensors available for assembly.")
            else:
                # Add new actuator
                st.session_state.data["actuators"].append({
                    "actuator_id": actuator_id,
                    "sensor_id": sensor_id,
                    "assembly_date": assembly_date,
                    "status": status
                })
                st.success("Actuator added successfully!")

    # Display dynamic table for actuators
    st.write("### Current Actuators")
    display_dynamic_table(st.session_state.data["actuators"], "actuator")

# ---------------------- Retailer Page ----------------------
elif page == "Retailer Page":
    st.title("🛒 Retailer Dashboard")
    st.markdown("""
    ### Manage Customer Feedback
    Submit and view feedback from customers about products.
    """)
    st.write("---")

    # Form to submit or update feedback
    with st.form("submit_feedback_form"):
        col1, col2 = st.columns(2)

        with col1:
            feedback_id = st.text_input("Feedback ID", placeholder="Enter feedback ID to add or update")
            product_id = st.text_input("Product ID")
            customer_id = st.text_input("Customer ID")

        with col2:
            description = st.text_area("Feedback Description")
            feedback_date = st.date_input("Feedback Date")

        submit = st.form_submit_button("Add or Update Feedback")

        if submit:
            # Check if the feedback ID already exists
            existing_feedback = next((f for f in st.session_state.data["feedback"] if f["feedback_id"] == feedback_id), None)
            if existing_feedback:
                # Update existing feedback
                existing_feedback.update({
                    "product_id": product_id,
                    "customer_id": customer_id,
                    "description": description,
                    "feedback_date": feedback_date,
                })
                st.success(f"Feedback with ID '{feedback_id}' updated successfully!")
            else:
                # Add new feedback
                st.session_state.data["feedback"].append({
                    "feedback_id": feedback_id,
                    "product_id": product_id,
                    "customer_id": customer_id,
                    "description": description,
                    "feedback_date": feedback_date
                })
                st.success("Feedback added successfully!")

    # Display dynamic table for feedback
    st.write("### Customer Feedback")
    display_dynamic_table(st.session_state.data["feedback"], "feedback")

