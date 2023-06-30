import streamlit as st
import mysql.connector
import os
import pandas as pd
from streamlit.components.v1 import html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
import logging
import numpy as np

import debugpy

DEBUGGER_PORT = 5678
DEBUGGER_HOST = "0.0.0.0"
SECRETS_PATH = os.path.abspath(os.environ.get("SECRETS_PATH", "/run/secrets"))
if os.environ.get("DEBUGGER") is not None:
    try:
        debugpy.listen((DEBUGGER_HOST, DEBUGGER_PORT))
        debugpy.wait_for_client()
    except RuntimeError as e:
        st.error(e)
        st.warning(f"Check if port {DEBUGGER_PORT} is already in use.")
        st.stop()
        # raise e

streamlit_menu_items = {
    # "Get help": "<url>",
    # 'Report a bug': "<url>",
    # 'About': "<url>",
}


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


st.set_page_config("Check-da-car", layout="wide", initial_sidebar_state="expanded", page_icon="🚗", menu_items=streamlit_menu_items)
st.title("Hello World")
st.sidebar.title("Navigation")
st.sidebar.button("Home", use_container_width=True)
st.sidebar.button("Add new car", use_container_width=True)
st.sidebar.button("Browse cars", use_container_width=True)
st.sidebar.button("See users", use_container_width=True)
st.sidebar.button("Gallery", use_container_width=True)

col1, col2 = st.columns(2)
col1.text_input("Name", placeholder="Name of the car")
col2.text_input("License plate", value="", placeholder="XXX-XXXX")
col1, col2, col3 = st.columns([1,2,2])
with st.spinner("Loading images"):
    image_data = np.random.rand(100, 100)
    col1.image(image_data, caption="Car image", use_column_width=True)
col2.selectbox("Manufacturer", options=["Add entry"])
col2.selectbox("Model", options=["Add entry"])
st.text_area("Car description", placeholder="Description of the car")
col1, col3 = st.columns([2, 1])
col1.text_input("VIN code", placeholder="VIN", label_visibility="collapsed")
col3.button("Create car")

# if create_car_btn:
#     st.write("You can insert a new car here.")

# temporary logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.info(f"Database connection: {connection_string}")

# mock streamlit pure html and javascript
image_html = open("templates/reffed_image.html").read().format(href="https://www.huggingface.co", image_src="app/static/hug.jpg")
st.markdown(image_html, unsafe_allow_html=True)
script_html = open("templates/inline_script.html").read().format(open("static/js/onload.js").read())
# st.markdown(script_html, unsafe_allow_html=True) # Javascript does not execute with this one
html(script_html, height=0)
st.markdown("Hello World")


# # list all database tables with mysql.connector
# cursor = connection.cursor(buffered=True)
# generator = cursor.execute("SHOW DATABASES")
# tables = [] if generator is None else generator.fetchall()
# df = pd.DataFrame(tables)
# st.table(df)
# for tablename in tables:
#     st.write(tablename)

# # close mysql.connector connection
# try:
#     cursor.close()
#     connection.close()
# except Exception as e:
#     st.error(e)
