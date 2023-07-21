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
from PIL import Image
import random
import httpx

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
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.title("Create car")
st.sidebar.title("Navigation")
st.sidebar.button("Home", use_container_width=True)
st.sidebar.button("Add new car", use_container_width=True)
st.sidebar.button("Browse cars", use_container_width=True)
st.sidebar.button("See users", use_container_width=True)
st.sidebar.button("Gallery", use_container_width=True)

col1, col2 = st.columns(2)
name = col1.text_input("Name", placeholder="Name of the car")
license_plate = col2.text_input("License plate", value="", placeholder="XXX-XXXX")
col1, col2, col3 = st.columns([1, 2, 2])
def is_image(file):
    try:
        img = Image.open(file)
        img.verify()
        try:
            img.close()
        except ValueError:
            pass
        return True
    except (IOError, SyntaxError):
        return False
uploaded_files = col2.file_uploader("Upload photos", accept_multiple_files=True)
images = [file for file in uploaded_files if is_image(file)]
with col1:
    with st.spinner("Loading images"):
        image_data = np.random.rand(100, 100)
        if len(images) > 0:
            image_data = images[random.randint(0, len(images) - 1)]
        st.image(image_data, caption="thumbnail", use_column_width=True)
manufacturer = col2.selectbox("Manufacturer", options=["Add entry"])
amodel = col2.selectbox("Model", options=["Add entry"])
# images = [np.random.rand(100, 100)] * 10
if images == None:
    images = []
with col3:
    st.write("Images")
    with st.spinner("Loading images"):
        max_row_length = 5
        # column_count = min(images.__len__(), max_row_length)
        column_count = max_row_length
        row_count = images.__len__() // max_row_length
        cols = st.columns(max(column_count, 1))
        for i, image in enumerate(images):
            # row = i // column_count
            column = i % column_count
            cols[column].image(image, caption="photos", use_column_width=True)
# col4.file_uploader("nevim")
st.text_area("Car description", placeholder="Description of the car")
col1, col3 = st.columns([2, 1])
col1.text_input("VIN code", placeholder="VIN", label_visibility="collapsed")
create_car_btn = col3.button("Create car")

# create_car
if create_car_btn:
    # validates data
    valid = True
    if name.strip() == "":
        valid = False
        st.error("No name was supplied")
    license_plate_stripped = license_plate.strip().replace(" ", "")
    if license_plate_stripped.__len__() > 8 or license_plate_stripped.__len__() < 7:
        valid = False
        st.error("License plate invalid")
    if name.strip() == "":
        valid = False
        st.error("No name was supplied")

    if valid:
        st.info("Car was created")


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
st.markdown("nevim")


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
