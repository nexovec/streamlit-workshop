import streamlit as st
import mysql.connector
import os
import pandas as pd

import debugpy

DEBUGGER_PORT = 5678
DEBUGGER_HOST = "0.0.0.0"
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
secrets = ["db_name", "db_user", "db_password"]
assert os.environ.get("DB_HOST") is not None, f"Please provide url of mariadb through variable DB_HOST"
for secret in secrets:
    path = f"/run/secrets/{secret}"
    condition = os.path.exists(path) and (os.path.isfile(path) or os.path.islink(path))
    assert condition, f"Please provide {secret} through docker secrets"
secrets = {secret: open(f"/run/secrets/{secret}", "r").read().strip() for secret in secrets}
for secret in secrets:
    assert secret != "", f"Secret {secret} must not be empty"
connection = mysql.connector.connect(
    host=os.environ.get("DB_HOST"),
    database=secrets["db_name"],
    user=secrets["db_user"],
    password=secrets["db_password"]
)
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
