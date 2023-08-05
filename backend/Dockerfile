FROM python:3.9 AS base
ARG USE_PIP_CACHE
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt --no-warn-script-location

FROM base as environment



FROM environment AS app

COPY . .

# for the frontend
# EXPOSE 5000
# for the backend
EXPOSE 5001

WORKDIR /
ENTRYPOINT ["uvicorn", "--host", "127.0.0.1", "--port", "5001", "--workers", "2", "app.__main__:app"]
# ENTRYPOINT ["python", "."]
# ENTRYPOINT ["streamlit", "run", "webui/index.py", "--browser.gatherUsageStats", "false", "--server.enableCORS", "true", "--server.port", "5000"]