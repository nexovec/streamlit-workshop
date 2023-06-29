import streamlit as st
import mysql.connector
import os
import pandas as pd
from streamlit.components.v1 import html

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
    
st.set_page_config("Zčekni auto", layout="wide", initial_sidebar_state="expanded", page_icon="🚗", menu_items=streamlit_menu_items)
st.title("Hello World")

# write html into st.markdown that displays an image that is a static file in the webui/static folder
# st.image("static/hug.jpg")
image_html = open("templates/reffed_image.html").read().format(href="https://www.huggingface.co", image_src="app/static/hug.jpg")
st.markdown(image_html, unsafe_allow_html=True)
script_html = open("templates/inline_script.html").read().format(open("static/js/onload.js").read())
# st.markdown(script_html, unsafe_allow_html=True) # Javascript does not execute with this one
html(script_html, height=0) 
st.markdown("Hello World")

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
cursor = connection.cursor(buffered=True)
generator = cursor.execute("SHOW DATABASES")
tables = [] if generator is None else generator.fetchall()
df = pd.DataFrame(tables)
st.table(df)
# for tablename in tables:
#     st.write(tablename)

try:
    cursor.close()
    connection.close()
except Exception as e:
    st.error(e)
