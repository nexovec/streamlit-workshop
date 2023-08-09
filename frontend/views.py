import streamlit as st
import numpy as np
from PIL import Image
import random
from streamlit.components.v1 import html
import httpx
import os
import json

rq = httpx.AsyncClient()

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
    manufacturer = col2.selectbox("Manufacturer", options=["Add entry"])
    amodel = col2.selectbox("Model", options=["Add entry"])
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

def browse_cars_view():
    st.title("Car browser")
    with st.spinner():
        ENDPOINT = "/car_data"
        car_datas = httpx.get(f"{os.getenv('BACKEND_URL')}{ENDPOINT}")
        parsed_data = json.loads(car_datas.read())
    for car in parsed_data:
        st.info(car)
    

def browse_users_view():
    st.title("User browser")

def browse_photo_gallery():
    st.title("Photo gallery")
