FROM python:3.10 AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM base AS backend

# RUN pip install --upgrade pip
# COPY ./backend/requirements.txt ./requirements.txt
# RUN pip install -r requirements.txt --no-warn-script-location

# COPY ./sql .
COPY backend .

EXPOSE 80
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "80", "--workers", "2", "--reload", "server:app"]

FROM base AS frontend
# TODO: supply pip cache location with a default value as ARG
# TODO: supply pip server location with a default value as ARG
# TODO: supply server port with a default value as ARG
# WORKDIR /app

# RUN pip install --upgrade pip
# COPY ./frontend/requirements.txt ./requirements.txt
# RUN pip install -r requirements.txt --no-warn-script-location

RUN mkdir -p ~/.streamlit/
RUN echo "[general]"  > ~/.streamlit/credentials.toml && \
    echo "email = \"\""  >> ~/.streamlit/credentials.toml

ENV STREAMLIT_SERVER_ENABLE_STATIC_SERVING=TRUE
# COPY ./sql .
COPY frontend .
EXPOSE 80
ENTRYPOINT ["streamlit", "run", "__main__.py", "--browser.gatherUsageStats", "false", "--server.port", "80"](venv)