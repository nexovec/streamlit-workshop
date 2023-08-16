from types import NoneType
from typing import Callable
import streamlit as st
import debugpy
import os
import logging
import asyncio
import httpx
import json
from functools import wraps
# from sqlalchemy_utils.functions import getdot

import views
import routing
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
# TODO: run in a separate file to avoid blocking on reruns (use streamlit.bootstrap)
if os.environ.get("DEBUGGER") is not None:
    try:
        debugpy.listen((DEBUGGER_HOST, DEBUGGER_PORT))
        logging.info("waiting for debugger connection...")
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
st.sidebar.markdown(f"Logged in as :red[{username}]")

routing_key = routing.Routing_Context.SESSION_KEY_PATH
if st.session_state.get(routing_key) is None:
    st.session_state[routing_key] = "create_car"


home_btn = st.sidebar.button("Home", use_container_width=True)
car_create_btn = st.sidebar.button("Add new car", use_container_width=True)
# st.info(f"selected car: {st.session_state.get('selected_car')}")
# views.create_car_view()
# viewed_car_detail = st.session_state.get("selected_car")
car_listings_btn = st.sidebar.button("Browse cars", use_container_width=True)
# views.car_detail_view(viewed_car_detail)
# views.browse_users_view
# browse_cars_view()
users_btn = st.sidebar.button("See users", use_container_width=True)
gallery_btn = st.sidebar.button("Gallery", use_container_width=True)

# car_browsing_btn_list = [st.button()]

# selected_car = st.session_state.get("selected_car")
# if car_create_btn:
views.create_car_view()
# elif car_listings_btn:
views.browse_cars_view()
# elif users_btn:
views.browse_users_view()
# elif gallery_btn:
views.browse_photo_gallery()
# elif viewed_car_detail:
#     views.car_detail_view(viewed_car_detail)
# elif home_btn:
# views.create_car_view()
# elif st.session_state.get("just_arrived") is None:
#     st.error("You have just arrived at the website but I have no default view for you sorry :(")
#     st.session_state["just_arrived"] = False
# elif selected_car is None:
#     # switch to the car detail
#     ENDPOINT = "/car_data"
#     car_datas = httpx.get(f"{os.getenv('BACKEND_URL')}{ENDPOINT}")
#     st.session_state["selected_car"] = views.car_selection(car_datas)
# elif selected_car is not None:
#     views.car_detail_view(selected_car)
# else:
#     param = st.experimental_get_query_params().get("car_id")
#     if param is not None:
#         # view car detail
#         ENDPOINT = "/car_detail"
#         car_datas = httpx.get(f"{os.getenv('BACKEND_URL')}{ENDPOINT}/{param}")
#         assert car_datas
#         for key, val in car_datas.json():
#             st.write(":\t".join([key, val]))
#     else:
#         st.error("Expected a car id to show details, but none is in the params")