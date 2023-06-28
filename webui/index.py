import streamlit as st
import mysql.connector
import os
import pandas as pd

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

st.title("Hello World")
# st.image("static/hug.jpg")

# write html into st.markdown that displays an image that is a static file in the webui/static folder
st.markdown("""
<a href="https://www.huggingface.co" target="_self">
    <img src="app/static/hug.jpg" alt="hug" width="100"/>
</a>
""", unsafe_allow_html=True)
st.markdown("""
<script type="text/javascript" src="app/static/onload.js"></script>
""", unsafe_allow_html=True)

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
