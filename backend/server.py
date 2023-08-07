
# print("INFO:")
# print(__name__)
# print(__main__)
# import subprocess
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

import models

# FRONTEND

cwd = os.path.dirname(__file__)
os.chdir(cwd)

SECRETS_PATH = os.path.abspath(os.environ.get("SECRETS_PATH", "/run/secrets"))
# cwd = os.getcwd()
# os.environ["STREAMLIT_SERVER_ENABLE_STATIC_SERVING"] = "true"

## DEFAULT VALUES ARE FOR LOCAL TESTING, SUPPLY YOUR OWN ##
# FIXME: the if statement breaks the compose build
# if os.environ.get("DOCKER_COMPOSE") != 1:
#     os.environ["DB_HOST"] = "172.28.194.111" if os.environ.get("DB_HOST") is None else os.environ.get("DB_HOST")
#     os.environ["SECRETS_PATH"] = "../secrets" if os.environ.get("SECRETS_PATH") is None else os.environ.get("SECRETS_PATH")
############################################################

# cmd = ["streamlit", "run", "webui.py", "--browser.gatherUsageStats", "false", "--server.port", "5000"]

# print(f"LAUNCHER WORKING DIRECTORY: {os.getcwd()}")
# def run_frontend():
#     subprocess.run(cmd, cwd=cwd, env=os.environ, check=True)

# frontend_thread = Thread(target=run_frontend)
# frontend_thread.start()

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
