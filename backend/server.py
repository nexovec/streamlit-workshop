
import os
from threading import Thread, Event
from types import TracebackType
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
import fastapi
import uvicorn
import logging
from pydantic import BaseModel
from datetime import datetime
import time

cwd = os.path.dirname(__file__)
os.chdir(cwd)

# BACKEND

app = FastAPI(title="Launcher", version="0.1.0", description="Launcher for the Streamlit app.")
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

@app.get("/")
async def root():
    logging.info("Redirecting to localhost:5002")
    return RedirectResponse("http://localhost:5002")
    
# udela hustou vec s databazi
@app.post("/create_car_entry")
async def create_car_entry():
    print("delam hustou vec s databazi")
    return {"status":"ok"}

@app.get("/get_manufacturers")
async def get_manufacturers():
    return ["Škoda", "Toyota", "Subaru"]

@app.get("/get_car_models/{manufacturer}")
async def get_car_models(manufacturer = "Škoda"):
    skodovky = ["Octavia", "Fabia", "Favorit"]
    toyoty = ["Yaris"]
    subaru = ["Impreza"]

    models_by_manufacturer = {
    "Škoda":skodovky,
    "Toyota": toyoty,
    "Subaru": subaru
    }
    return models_by_manufacturer.get(manufacturer)

@app.get("/health")
async def health():
    return {"status": "OK"}

@app.get("/stop")
async def stop():
    exit(0)
    # return {"message": "OK"}
