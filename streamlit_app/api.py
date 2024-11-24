from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime, date
from typing import Optional

# Initialize FastAPI app
app = FastAPI()

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["SupplyChainDB"]

# Pydantic models for validation
class Sensor(BaseModel):
    sensor_id: str
    batch_number: str
    name: str
    status: str
    manufacturer_date: date
    datasheet: Optional[str] = None
    feedback: Optional[str] = None

class Drone(BaseModel):
    drone_id: str
    sensor_id: str
    assembly_date: date
    status: str
    feedback: Optional[str] = None

class Feedback(BaseModel):
    feedback_id: str
    product_type: str
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
    drone_data = drone.dict()
    drone_data["assembly_date"] = datetime.combine(drone.assembly_date, datetime.min.time())
    db.drones.insert_one(drone_data)
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
    feedback_data = feedback.dict()
    feedback_data["feedback_date"] = datetime.combine(feedback.feedback_date, datetime.min.time())
    db.feedback.insert_one(feedback_data)
    return {"message": "Feedback added successfully"}

@app.get("/api/feedback")
async def get_feedback():
    feedbacks = list(db.feedback.find({}, {"_id": 0}))
    return feedbacks
