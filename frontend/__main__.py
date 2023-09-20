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

import views
import routing

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

streamlit_menu_items = {
    # "Get help": "<url>",
    # 'Report a bug': "<url>",
    # 'About': "<url>",
}

st.set_page_config("Streamlit workshop", layout="wide", initial_sidebar_state="expanded", page_icon="🚗", menu_items=streamlit_menu_items)
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

ctx = routing.Routing_Context(default=views.ROUTES.CREATE_CAR)

home_btn = st.sidebar.button("Základy", use_container_width=True)
car_create_btn = st.sidebar.button("Přidej auto", use_container_width=True)
car_listings_btn = st.sidebar.button("Zobraz auta", use_container_width=True)
login_btn = st.sidebar.button("Přihlášení", use_container_width=True)
others_btn = st.sidebar.button("Ostatní", use_container_width=True)

if home_btn:
    ctx.redirect(views.ROUTES.HOME)

if car_create_btn:
    ctx.redirect(views.ROUTES.CREATE_CAR)

if car_listings_btn:
    ctx.redirect(views.ROUTES.BROWSE_CARS)

if login_btn:
    ctx.redirect(views.ROUTES.LOGIN_SCREEN)
if others_btn:
    ctx.redirect(views.ROUTES.PHOTO_GALLERY)

selected_car_id = st.session_state.get(views.CAR_DETAIL_ID)

ctx.render()
