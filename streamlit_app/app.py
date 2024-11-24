import streamlit as st
import requests
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
from streamlit_option_menu import option_menu

API_URL = "http://127.0.0.1:8000/api"


# Initialize session state for shared data
if "data" not in st.session_state:
    st.session_state.data = {
        "sensors": [],      # List of sensors (for Supplier Page)
        "drones": [],    # List of drones (for OEM Page)
        "feedback": []      # List of feedback (for Retailer Page)
    }

# Navbar for navigation
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
    st.image("streamlit_app/assets/supplier_icon.png", width=100)
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
            payload = {
                "sensor_id": sensor_id,
                "batch_number": batch_number,
                "status": status,
                "manufacturer_date": str(manufacturer_date),
                "shipment_date": str(shipment_date),
            }

            try:
                # Check if the sensor ID already exists by querying the backend
                response = requests.get(f"{API_URL}/sensors/{sensor_id}")
                if response.status_code == 200:
                    # If the sensor exists, update it using the PUT method
                    update_response = requests.put(f"{API_URL}/sensors/{sensor_id}", json=payload)
                    if update_response.status_code == 200:
                        st.success(f"Sensor with ID '{sensor_id}' updated successfully!")
                    else:
                        st.error(f"Failed to update sensor. Error: {update_response.json().get('detail', 'Unknown error')}")
                elif response.status_code == 404:
                    # If the sensor does not exist, create a new one using the POST method
                    create_response = requests.post(f"{API_URL}/sensors", json=payload)
                    if create_response.status_code == 200:
                        st.success("Sensor added successfully!")
                    else:
                        st.error(f"Failed to add sensor. Error: {create_response.json().get('detail', 'Unknown error')}")
                else:
                    st.error(f"Unexpected response from the server: {response.status_code}")
            except Exception as e:
                st.error(f"Failed to connect to the backend. Error: {e}")

    # Display dynamic table for sensors
    def fetch_sensors_data():
        try:
            response = requests.get('http://127.0.0.1:8000/api/sensors')
            # Check if the request was successful
            if response.status_code == 200:
                return response.json()  # Assuming the response is a list of sensors
            else:
                st.error(f"Failed to fetch sensors data. Status code: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"Error fetching sensors data: {e}")
            return []

    # Fetch the sensors data when the app loads
    sensors_data = fetch_sensors_data()

    # Check if data exists and display it
    if sensors_data:
        st.write("### Current Sensors")
        st.dataframe(sensors_data)  # Display the sensors data as a dynamic table
    else:
        st.write("No sensor data available.")

# ---------------------- OEM Page ----------------------
elif page == "OEM Page":
    st.title("🔧 OEM Dashboard")
    st.markdown("""
    ### Assemble drones
    Track and manage the integration of sensors into drones.
    """)
    st.write("---")

    # Form to assemble or update drones
    with st.form("assemble_drone_form"):
        col1, col2 = st.columns(2)

        with col1:
            drone_id = st.text_input("Drone ID", placeholder="Enter drone ID to add or update")
            sensor_id = st.selectbox(
                "Select Sensor", 
                [s["sensor_id"] for s in st.session_state.data["sensors"]]
                if st.session_state.data["sensors"] else ["No sensors available"]
            )

        with col2:
            assembly_date = st.date_input("Assembly Date")
            status = st.selectbox("Status", ["Assembled", "Shipped"])

        submit = st.form_submit_button("Add or Update Drone")
        if submit:
            # Check if the drone ID already exists
            existing_drone = next((a for a in st.session_state.data["drones"] if a["drone_id"] == drone_id), None)
            if existing_drone:
                # Update existing drone
                existing_drone.update({
                    "sensor_id": sensor_id,
                    "assembly_date": assembly_date,
                    "status": status,
                })
                st.success(f"drone with ID '{drone_id}' updated successfully!")
            elif sensor_id == "No sensors available":
                st.error("No sensors available for assembly.")
            else:
                # Add new drone
                st.session_state.data["drones"].append({
                    "drone_id": drone_id,
                    "sensor_id": sensor_id,
                    "assembly_date": assembly_date,
                    "status": status
                })
                st.success("drone added successfully!")

    # Display dynamic table for drones
    st.write("### Current drones")
    display_dynamic_table(st.session_state.data["drones"], "drone")

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

