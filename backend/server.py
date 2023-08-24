
import os
from threading import Thread, Event
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import fastapi
import uvicorn
import logging
from pydantic import BaseModel

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

engine = create_engine(connection_string, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

models.Base.metadata.create_all(engine)

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
    
@app.post("/create_car_entry")
# async def create_car_entry(form_contents: models.Create_Car_Entry_Validator):
async def create_car_entry(form_contents: models.Create_Car_Entry_Validator):
    
    return 501 # not implemented

@app.get("/health")
async def health():
    return {"message": "OK"}

@app.get("/stop")
async def stop():
    exit(0)
    # return {"message": "OK"}

# @app.get("/docs")
# async def docs():
#     return get_swagger_ui_html()

@app.get("/car_data")
async def car_data():
    return [{"name": "Mercedes", "id": 1}]

@app.get("/car_detail/{car_id}")
async def car_detail(car_id: int):
    return {"id":"nevim"}