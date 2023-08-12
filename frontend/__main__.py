import streamlit as st
import debugpy
import os
import logging
import asyncio

import views
# import mysql.connector
# import pandas as pd
# from streamlit.components.v1 import html
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import models
# import numpy as np
# from PIL import Image
# import random
# import httpx


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

st.set_page_config("Check-da-car", layout="wide", initial_sidebar_state="expanded", page_icon="🚗", menu_items=streamlit_menu_items)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.sidebar.title("Navigation")

username = "Your Name" # TODO: authentify

car_create_form = st.sidebar.button("Home", use_container_width=True)
car_create_form = st.sidebar.button("Add new car", use_container_width=True) or car_create_form
st.info(f"selected car: {st.session_state.get('selected_car')}")
if car_create_form:
    views.create_car_view()
viewed_car_detail = st.session_state.get("selected_car")
car_listings_btn = st.sidebar.button("Browse cars", use_container_width=True)
if viewed_car_detail is not None:
    views.car_detail_view(viewed_car_detail)
elif car_listings_btn:
    views.browse_cars_view()
if st.sidebar.button("See users", use_container_width=True):
    st.title("Browse users")
if st.sidebar.button("Gallery", use_container_width=True):
    st.title("Image gallery")
st.sidebar.markdown(f"Logged in as :red[{username}]")
