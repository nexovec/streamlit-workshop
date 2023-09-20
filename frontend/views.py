import streamlit as st
import numpy as np
from PIL import Image
import random
from streamlit.components.v1 import html
import httpx
import os
import json
import logging
import mysql.connector

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

# přípojka k mariadb
try:
 connection = mysql.connector.connect(
     host=os.environ.get("DB_HOST", "mariadb"),
     database=secrets["db_name"],
     user=secrets["db_user"],
     password=secrets["db_password"],
     port=os.environ.get("DB_PORT", 3306),
 )
except Exception as e:
 st.warning("Our database is probably restarting, try later.")
 st.error(e)
 st.stop()

# pohledy ve streamlitu
@ctx.route(ROUTES.HOME)
def home():
    st.title("Streamlit workshop")

@ctx.route(ROUTES.CREATE_CAR)
def create_car_view():
    st.title("Create car")
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
    images = [file for file in uploaded_files if is_image(file)] if uploaded_files is not None else []
    with col1:
        with st.spinner("Loading images"):
            image_data = np.random.rand(100, 100)
            if len(images) > 0:
                image_data = images[random.randint(0, len(images) - 1)]
            st.image(image_data, caption="thumbnail", use_column_width=True)


    manufacturer_options = []
    address = f"{os.getenv('BACKEND_URL')}/get_manufacturers"
    manufacturer_options = httpx.get(address).json()
    manufacturer_options.append("Add entry")
    manufacturer = col2.selectbox("Manufacturer", options=manufacturer_options)
    if manufacturer == manufacturer_options[-1]:
        col_2_1, col_2_2 = col2.columns(2)
        manufacturer_name = col_2_1.text_input("Manufacturer name")
        if col_2_2.button("submit"):
            address = f"{os.getenv('BACKEND_URL')}/create_car_manufacturer"
            body_params = {"name": manufacturer_name}
            httpx.post(address, params=body_params)
    else:
        address = f"{os.getenv('BACKEND_URL')}/get_car_models/{manufacturer}"
        resp = httpx.get(address)
        st.info(resp)
        # print(resp)
        options = resp.json()
        options.append("Add entry")
        car_model = col2.selectbox("Model", options=options)
        if car_model == options[-1]:
            col_2_1, col_2_2 = col2.columns(2)
            car_model_name = col_2_1.text_input("Model name")
            if col_2_2.button("submit"):
                address = f"{os.getenv('BACKEND_URL')}/create_car_model"
                body_params = {"manufacturer_name": manufacturer, "model_name": car_model_name}
                httpx.post(address, params=body_params)
                
        

        # amodel = col2.selectbox("Model", options=["Add entry"])

    # images = [np.random.rand(100, 100)] * 10
    # if images == None:
    #     images = []
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

    # mock streamlit pure html and javascript
    image_html = open("templates/reffed_image.html").read().format(href="https://www.huggingface.co", image_src="app/static/hug.jpg")
    st.markdown(image_html, unsafe_allow_html=True)
    script_html = open("templates/inline_script.html").read().format(open("static/js/onload.js").read())
    # st.markdown(script_html, unsafe_allow_html=True) # Javascript does not execute with this one
    html(script_html, height=0)
    st.markdown("nevim")
    
# zobrazí auta v databázi
@ctx.route(ROUTES.BROWSE_CARS)
def browse_cars_view():
    st.title("Car browser")
    ENDPOINT = "/car_data"
    response = httpx.get(f"{os.getenv('BACKEND_URL')}{ENDPOINT}")
    st.session_state["selected_car"] = None

    cars = response.json()

    ITEMS_PER_PAGE = 20

    st.warning(f"#cars: {len(cars)}")
    for thing in cars:
        st.info(f"{thing}")
    
@ctx.route(ROUTES.LOGIN_SCREEN)
def login_screen():
    st.title("Přihlášování")

@ctx.route(ROUTES.PHOTO_GALLERY)
def photo_gallery():
    st.title("Galerie")
