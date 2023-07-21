# TODO: actually use this as a launcher
# TODO: move debugger in here
if not __name__ == "__main__":
    raise Exception("This file is not meant to be imported.")

import subprocess
import os
from threading import Thread, Event
from fastapi import FastAPI
import uvicorn

# FRONTEND

cwd = os.path.dirname(__file__)
os.chdir(cwd)
# cwd = os.getcwd()
os.environ["STREAMLIT_SERVER_ENABLE_STATIC_SERVING"] = "true"

## DEFAULT VALUES ARE FOR LOCAL TESTING, SUPPLY YOUR OWN ##
# FIXME: the if statement breaks the compose build
# if os.environ.get("DOCKER_COMPOSE") != 1:
#     os.environ["DB_HOST"] = "172.28.194.111" if os.environ.get("DB_HOST") is None else os.environ.get("DB_HOST")
#     os.environ["SECRETS_PATH"] = "../secrets" if os.environ.get("SECRETS_PATH") is None else os.environ.get("SECRETS_PATH")
############################################################

cmd = ["streamlit", "run", "webui.py", "--browser.gatherUsageStats", "false", "--server.port", "5000"]

print(f"LAUNCHER WORKING DIRECTORY: {os.getcwd()}")
def run_frontend():
    subprocess.run(cmd, cwd=cwd, env=os.environ, check=True)

frontend_thread = Thread(target=run_frontend)
frontend_thread.start()

# BACKEND

app = FastAPI(title="Launcher", version="0.1.0", description="Launcher for the Streamlit app.")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"message": "OK"}

@app.get("/stop")
async def stop():
    exit(0)
    # return {"message": "OK"}

uvicorn.run(app, host="0.0.0.0", port=5001)