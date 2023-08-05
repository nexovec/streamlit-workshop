
# print("INFO:")
# print(__name__)
# print(__main__)
# import subprocess
import os
from threading import Thread, Event
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
import fastapi
import uvicorn
import logging

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

# cmd = ["streamlit", "run", "webui.py", "--browser.gatherUsageStats", "false", "--server.port", "5000"]

# print(f"LAUNCHER WORKING DIRECTORY: {os.getcwd()}")
# def run_frontend():
#     subprocess.run(cmd, cwd=cwd, env=os.environ, check=True)

# frontend_thread = Thread(target=run_frontend)
# frontend_thread.start()

# BACKEND

app = FastAPI(title="Launcher", version="0.1.0", description="Launcher for the Streamlit app.")
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    logger.info("Redirecting to localhost:5002")
    return RedirectResponse("http://localhost:5002")
    # return "Hello there"

@app.get("/health")
async def health():
    return {"message": "OK"}

@app.get("/stop")
async def stop():
    exit(0)
    # return {"message": "OK"}

@app.get("/docs")
async def docs():
    return get_swagger_ui_html()
