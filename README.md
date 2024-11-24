# **RepairLink**

**Industry 4.0 project for Supply Chain Management**  
RepairLink is a supply chain management project designed to manage sensors (like the **MPU-6050 accelerometer**), drones (like the **DJI Phantom 4 Pro**), and customer feedback. It uses **FastAPI** for backend APIs, **MongoDB** for database management, and **Streamlit** for the frontend interface. The system integrates multiple roles, including suppliers, OEMs, retailers, and customers, for seamless inventory, assembly, and feedback management.

---

## **How to Install and Run**

### **Step 1: Install Dependencies**
1. Clone this repository to your local machine.
2. Install required Python packages using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt

### **Step 2: Set Up MongoDB**
1. Download and install **MongoDB Compass** from the [official website](https://www.mongodb.com/products/compass).
2. Start MongoDB locally or configure a cloud-based MongoDB instance.
3. Create a new database named `SupplyChainDB` (if it doesn't already exist).
4. Collections for `sensors`, `drones`, and `feedback` will automatically be created and populated as the backend runs.

---

### **Step 3: Run the Backend Server**
1. Navigate to the project directory in your terminal.
2. Start the FastAPI backend server using **Uvicorn**:
   ```bash
   uvicorn api:app --reload

### **Step 4: Run the Frontend Application**
1. Navigate to the project directory in your terminal.
2. Start the **Streamlit frontend** using the following command:
   ```bash
   streamlit run app.py


