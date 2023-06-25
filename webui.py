import streamlit as st
import mysql.connector
import os
import pandas as pd

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
generator = cursor.execute("SHOW TABLES")
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
