from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime,date

# Initialize FastAPI app
app = FastAPI()

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["SupplyChainDB"]

# Pydantic models for validation
class Sensor(BaseModel):
    sensor_id: str
    batch_number: str
    status: str
    manufacturer_date: date
    shipment_date: date

class Drone(BaseModel):
    drone_id: str
    sensor_id: str
    assembly_date: date
    status: str

class Feedback(BaseModel):
    feedback_id: str
    product_id: str
    customer_id: str
    description: str
    feedback_date: date

# ------------------ Sensor APIs ------------------
@app.post("/api/sensors")
async def add_sensor(sensor: Sensor):
    if db.sensors.find_one({"sensor_id": sensor.sensor_id}):
        raise HTTPException(status_code=400, detail="Sensor ID already exists.")
    sensor_data = sensor.dict()
    sensor_data["manufacturer_date"] = datetime.combine(sensor.manufacturer_date, datetime.min.time())
    sensor_data["shipment_date"] = datetime.combine(sensor.shipment_date, datetime.min.time())

    db.sensors.insert_one(sensor_data)
    return {"message": "Sensor added successfully"}

@app.get("/api/sensors")
async def get_sensors():
    sensors = list(db.sensors.find({}, {"_id": 0}))
    return sensors

# ------------------ Drone APIs ------------------
@app.post("/api/drones")
async def add_drone(drone: Drone):
    if not db.sensors.find_one({"sensor_id": drone.sensor_id}):
        raise HTTPException(status_code=400, detail="Sensor ID does not exist.")
    if db.drones.find_one({"drone_id": drone.drone_id}):
        raise HTTPException(status_code=400, detail="Drone ID already exists.")
    db.drones.insert_one(drone.dict())
    return {"message": "Drone added successfully"}

@app.get("/api/drones")
async def get_drones():
    drones = list(db.drones.find({}, {"_id": 0}))
    return drones

# ------------------ Feedback APIs ------------------
@app.post("/api/feedback")
async def add_feedback(feedback: Feedback):
    if db.feedback.find_one({"feedback_id": feedback.feedback_id}):
        raise HTTPException(status_code=400, detail="Feedback ID already exists.")
    db.feedback.insert_one(feedback.dict())
    return {"message": "Feedback added successfully"}

@app.get("/api/feedback")
async def get_feedback():
    feedbacks = list(db.feedback.find({}, {"_id": 0}))
    return feedbacks
