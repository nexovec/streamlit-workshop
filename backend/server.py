
import os
from threading import Thread, Event
from types import TracebackType
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from sqlalchemy import create_engine
from sqlalchemy.orm import decl_base, sessionmaker
import fastapi
from sqlalchemy.orm.path_registry import PropRegistry
from sqlalchemy.sql.ddl import sort_tables_and_constraints
import uvicorn
import logging
from pydantic import BaseModel
from datetime import datetime
import time

import sql.models as models

cwd = os.path.dirname(__file__)
os.chdir(cwd)

SECRETS_PATH = os.path.abspath(os.environ.get("SECRETS_PATH", "/run/secrets"))
# database connection

## validating secrets and environment variables
secrets = ["db_name", "db_user", "db_password"]
assert os.environ.get("DB_HOST") is not None, f"Please provide url of mariadb through variable DB_HOST"
for secret in secrets:
    path = os.path.join(SECRETS_PATH, secret)
    condition = os.path.exists(path) and (os.path.isfile(path) or os.path.islink(path))
    err_msg = f"Please provide {secret} through docker secrets"
    assert condition, err_msg
secrets = {secret: open(os.path.join(SECRETS_PATH, secret), "r").read().strip() for secret in secrets}
for secret in secrets:
    assert secret != "", f"Secret {os.path.join(SECRETS_PATH, secret)} must not be empty"

## connecting with mysql.connector
# try:
#     connection = mysql.connector.connect(
#         host=os.environ.get("DB_HOST", "mariadb"),
#         database=secrets["db_name"],
#         user=secrets["db_user"],
#         password=secrets["db_password"],
#         port=os.environ.get("DB_PORT", 3306),
#     )
# except Exception as e:
#     st.warning("Our database is probably restarting, try later.")
#     st.error(e)
#     st.stop()

## connecting with sqlalchemy
# TODO: catch any exceptions
protocol = "mysql+mysqlconnector"
host=os.environ.get("DB_HOST", "mariadb")
database=secrets["db_name"]
user=secrets["db_user"]
password=secrets["db_password"]
port=os.environ.get("DB_PORT", 3306)
hostname = f"{host}:{port}" if port is not None else host

connection_string = f"{protocol}://{user}:{password}@{hostname}/{database}"

engine = None
while engine is None:
    try:
        engine = create_engine(connection_string, echo=True)
    except Exception as e:
        print(f"Exception: {e.with_traceback()}", flush=True)
        time.sleep(1)
Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

models.Base.metadata.create_all(engine)

# Create a sample user

db = Session()
try:
    # FIXME: doensn't reconnect
    default_user = models.User(id=1, timestamp_created=datetime.utcnow(), username="admin", password="password")
    db.add(default_user)
    db.commit()
except Exception as e:
    db.rollback()
    pass

default_user = db.query(models.User).where(models.User.id == 1).first()
assert default_user is not None

# BACKEND

app = FastAPI(title="Launcher", version="0.1.0", description="Launcher for the Streamlit app.")
# logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.info(f"Database connection: {connection_string}")

@app.get("/")
async def root():
    logging.info("Redirecting to localhost:5002")
    return RedirectResponse("http://localhost:5002")
    # return "Hello there"

@app.post("/create_car_manufacturer")
async def create_car_manufacturer(name: str):
    db.rollback()
    obj = models.Car_Manufacturer(name=name, timestamp_created=datetime.utcnow())
    db.add(obj)
    db.commit()
    return 200

@app.post("/create_car_model")
async def create_car_model(manufacturer_name:str, model_name:str):
    db.rollback()
    # TODO: make sure model name is unique for the given manufacturer
    manufacturer_ids = db.query(models.Car_Manufacturer.id).where(models.Car_Manufacturer.name == manufacturer_name).all()
    manufacturer_ids = [manufacturer_id[0] for manufacturer_id in manufacturer_ids]
    if len(manufacturer_ids) == 0:
        return 400
    obj = models.Car_Model(name=model_name, car_manufacturer_id=manufacturer_ids[0], timestamp_created=datetime.utcnow())
    db.add(obj)
    db.commit()

# @app.get("/get_car_models/{manufacturer}")
# async def get_car_models(manufacturer: str):
#     results = db.query(models.Car_Model.name).all()
#     return [result[0] for result in results]
    
@app.get("/get_car_manufacturers")
async def get_car_manufacturers() -> list[str]:
    db.rollback()
    results = db.query(models.Car_Manufacturer.name).all()
    # if len(results) == 0:
        # return []
    # return result
    return [result[0] for result in results]
    # return ["nevim"]
@app.get("/get_car_models/{manufacturer}")
async def get_car_models(manufacturer: str):
    db.rollback()
    manufacturer_id = db.query(models.Car_Manufacturer.id).where(models.Car_Manufacturer.name == manufacturer).first()
    results = db.query(models.Car_Model.name).where(models.Car_Model.car_manufacturer_id == manufacturer_id[0]).all()
    # if not result:
    #     return []
    # return result
    return [result[0] for result in results]

@app.get("/get_usernames_list")
async def get_usernames_list():
    db.rollback()
    result = db.query(models.User.username).all()
    return result
    
@app.post("/create_car_entry")
# async def create_car_entry(form_contents: models.Create_Car_Entry_Validator):
async def create_car_entry(form_contents: models.Create_Car_Entry_Validator):
    db.rollback()
    # db = Session()

    valid_fields = form_contents.dict()
    valid_car_model_fields = {
        key: value for key, value in valid_fields.items() if key in models.Car_Model.__table__.columns
    }
    valid_car_manufacturer_fields = {
        key: value for key, value in valid_fields.items() if key in models.Car_Manufacturer.__table__.columns
    }
    valid_car_entry_fields = {
        key: value for key, value in valid_fields.items() if key in models.Create_Car_Entry.__table__.columns
    }

    # valid_car_entry_fields["owner_id"] = default_user.id
    valid_car_entry_fields["creator_id"] = default_user.id

    print(f"valid car fields: {models.Car_Model.__table__.columns}")
    # print(valid_car_model_fields.get("name"))
    valid_car_model_fields["name"] = "test"
    car_model = models.Car_Model(**valid_car_model_fields)
    car_manufacturer = models.Car_Manufacturer(**valid_car_manufacturer_fields)
    car_entry = models.Create_Car_Entry(**valid_car_entry_fields, manufacturer_id=car_manufacturer.id, model_id=car_model.id)

    db.add(car_model)
    db.add(car_manufacturer)
    db.add(car_entry)

    db.commit()
        
    # return 501 # not implemented
    return {"status":"OK"}

@app.get("/health")
async def health():
    return {"status": "OK"}

@app.get("/stop")
async def stop():
    exit(0)
    # return {"message": "OK"}

# @app.get("/docs")
# async def docs():
#     return get_swagger_ui_html()

@app.get("/car_data")
async def car_data():
    db.rollback()
    cars = db.query(models.Create_Car_Entry.license_plate).all()
    # return cars
    return [car[0] for car in cars]
    # return [{"name": "Mercedes", "id": 1}]

@app.get("/car_detail/{car_id}")
async def car_detail(car_id: int):
    return {"id":"nevim"}