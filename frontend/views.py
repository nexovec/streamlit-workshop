import streamlit as st
import numpy as np
from PIL import Image
import random
from streamlit.components.v1 import html
import httpx
import os
import logging
# import mysql.connector
import sqlite3
from datetime import datetime
import plotly.express as px
import pandas as pd
import time

import routing

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
ctx = routing.Routing_Context()

CAR_DETAIL_ID = "car_previewed"
class ROUTES:
    HOME = "home"
    CREATE_CAR = "create_car"
    BROWSE_CARS = "browse_cars"
    LOGIN_SCREEN = "login_screen"
    PHOTO_GALLERY = "photo gallery"
    CAR_DETAIL = "car_detail"

# načítám docker secrets
SECRETS_PATH = os.path.abspath(os.environ.get("SECRETS_PATH", "/run/secrets"))
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

# # přípojka k mariadb, pokud ji potřebujete
# try:
#  connection = mysql.connector.connect(
#      host=os.environ.get("DB_HOST", "mariadb"),
#      database=secrets["db_name"],
#      user=secrets["db_user"],
#      password=secrets["db_password"],
#      port=os.environ.get("DB_PORT", 3306),
#  )
# except Exception as e:
#  st.warning("Our database is probably restarting, try later.")
#  st.error(e)
#  st.stop()

# přípojka k SQLite
SQLITE_DB_PATH = "data/vehicles.db"
def initialize_sqlite():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    # Tvorba tabulek
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            manufacturer TEXT,
            model TEXT,
            license_plate VARCHAR,
            VIN VARCHAR,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id INTEGER,
            filename TEXT,
            data BLOB,
            FOREIGN KEY(car_id) REFERENCES vehicles(id)
        )
    ''')
    cursor.close()
    conn.close()
initialize_sqlite()

# pohledy ve streamlitu
@ctx.route(ROUTES.HOME)
def home():
    st.title("Streamlit workshop")
    st.write("Psaní textu")
    st.write("Umí **tučně** i emoji :construction_worker:")
    st.info("Letí nad námi letadlo")
    st.warning("Padá na nás letadlo")
    st.error("Kritické poškození trupu!!")
    st.select_slider("slider 1", ["Málo", "Středně", "Hodně"])
    st.divider()
    with st.spinner("Načítám"):
        time.sleep(3)

    col1, col2, col3, col4 = st.columns(4)
    col1.write("Psaní do sloupečku")
    col2.write("Psaní do druhého sloupečku")
    with col3:
        st.write("Jiný zápis")
    with col4:
        st.write("streamlit válí 🤟")

    # čisté HTML a javascript ve streamlitu
    image_html = open("templates/reffed_image.html").read().format(href="https://www.huggingface.co", image_src="app/static/hug.jpg")
    st.markdown(image_html, unsafe_allow_html=True)
    script_html = open("templates/inline_script.html").read().format(open("static/js/onload.js").read())
    # st.markdown(script_html, unsafe_allow_html=True) # Javascript does not execute with this one
    html(script_html, height=0)
    st.markdown("nevim")
    st.markdown("[Odkaz na dokumentaci](https://docs.streamlit.io/library/api-reference)")

@ctx.route(ROUTES.CREATE_CAR)
def create_car_view():
    st.title("Create car")
    col1, col2 = st.columns(2)
    car_name = col1.text_input("Name", placeholder="Name of the car")
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
    images = [file for file in uploaded_files if is_image(file)] if uploaded_files is not None else []
    with col1:
        with st.spinner("Loading images"):
            default_image_data = np.random.rand(100, 100)
            slot = st.empty()

            image_data = default_image_data
            if len(images) > 0:
                image_data = images[random.randint(0, len(images) - 1)]
            try:
                slot.image(image_data, caption="thumbnail", use_column_width=True)
            except ValueError as e:
                slot.image(default_image_data, caption="couldn't load the image", use_column_width=True)
                # slot.error(e)

    address = f"{os.getenv('BACKEND_URL')}/get_manufacturers"
    manufacturer_options = httpx.get(address).json()
    manufacturer = col2.selectbox("Manufacturer", options=manufacturer_options)
    address = f"{os.getenv('BACKEND_URL')}/get_car_models/{manufacturer}"
    resp = httpx.get(address)
    st.info(resp)
    options = resp.json()
    car_model = col2.selectbox("Model", options=options)
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
                try:
                    cols[column].image(image, caption="photos", use_column_width=True)
                except ValueError as e:
                    st.error(image.name.__repr__() + ":\t" + e.__repr__())
    st.text_area("Car description", placeholder="Description of the car")
    col1, col3 = st.columns([2, 1])
    VIN_no = col1.text_input("VIN code", placeholder="VIN", label_visibility="collapsed")
    create_car_btn = col3.button("Create car")

    # create_car
    if create_car_btn:
        license_plate_stripped = license_plate.strip().replace(" ", "")

        # validace dat
        valid = True
        # aby se to lépe ukazovalo, validace je vypnutá, následující není vyčerpávající seznam toho co se musí ošetřit.
        # if car_name.strip() == "":
        #     valid = False
        #     st.error("No name was supplied")
        # if license_plate_stripped.__len__() > 8 or license_plate_stripped.__len__() < 7:
        #     valid = False
        #     st.error("License plate invalid")
        # if car_name.strip() == "":
        #     valid = False
        #     st.error("No name was supplied")

        if valid:
            # příklad 1 - posílám informace do API
            address = f"{os.getenv('BACKEND_URL')}/create_car"
            body = {
                "manufacturer": manufacturer,
                "model":car_model,
                "name": car_name
            }
            httpx.post(address, params=body)
            st.info("Car was created")

            # příklad 2 - ukládám auto do vlastní databáze
            vehicle_data = (car_name, manufacturer, car_model, license_plate_stripped, VIN_no, datetime.now())
            conn = sqlite3.connect(SQLITE_DB_PATH)
            cursor = conn.cursor()

            # Insert data into the table
            cursor.execute('''
                INSERT INTO vehicles (name, manufacturer, model, license_plate, VIN, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', vehicle_data)
            lastid = cursor.lastrowid
            assert lastid is not None

            query_params = []
            for file in images:
                query_param = (lastid, file.name, file.read())
                query_params.append(query_param)
            # Commit the changes and close the connection
            cursor.executemany('''
                INSERT INTO images (car_id, filename, data) VALUES
                (?, ?, ?)
            ''', query_params)
            conn.commit()
            conn.close()


# zobrazí auta v databázi
@ctx.route(ROUTES.BROWSE_CARS)
def browse_cars_view():
    st.title("Car data browser")
    st.header("Statistics")
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vehicles")
    car_entries = cursor.fetchall()

    cursor.close()
    conn.close()

    df = pd.DataFrame(car_entries)
    df.columns = ["id", "name", "manufacturer", "model", "license_plate", "VIN", "timestamp"]
    st.dataframe(df.head())
    # Group by manufacturer and count car models
    manufacturer_counts = df.groupby("manufacturer")["id"].count().reset_index()

    # Rename the columns for clarity
    manufacturer_counts.columns = ["Manufacturer", "Car Count"]
    graph = px.histogram(manufacturer_counts, x="Manufacturer", y="Car Count")
    st.plotly_chart(graph)

    st.header("Registered car list")
    st.warning(f"number of cars registered: {len(car_entries)}")
    col1, col2 = st.columns([6,1])
    for i, thing in enumerate(car_entries):
        col1.info(f"{thing}")
        if col2.button("Show detail", "detail_" + str(i)):
            st.session_state["car_detail"] = thing[0]
            ctx.redirect(ROUTES.CAR_DETAIL)

@ctx.route(ROUTES.CAR_DETAIL)
def car_detail():
    col1, col2 = st.columns(2)
    car_id = st.session_state.get("car_detail")
    # st.info()
    col1.write("Name:")
    col1.write("Manufacturer:")
    col1.write("Model:")
    col1.write("License plate:")
    col1.write("VIN")
    col1.write("Registeration date:")

    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vehicles WHERE id=?", str(car_id))
    result = cursor.fetchone()
    for item in result[1:]:
        col2.write(item)

    images = cursor.execute("SELECT * FROM images WHERE car_id=?", str(car_id)).fetchall()
    st.info(f"This car has {len(images)} associated images")
    for image in images:
        st.image(image[-1], use_column_width=True)
    cursor.close()
    conn.close()
@ctx.route(ROUTES.LOGIN_SCREEN)
def login_screen():
    st.title("Přihlášování")

@ctx.route(ROUTES.PHOTO_GALLERY)
def photo_gallery():
    st.title("Galerie")
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    code = st.text_area("SQL editor")
    if st.button("Execute"):
        cursor.execute(code)
        conn.commit()

    images = cursor.execute("SELECT * FROM images").fetchall()
    for image in images:
        st.info("associated car id: " + str(image[1]))
        st.image(image[-1], use_column_width=True)

    cursor.close()
    conn.close()
