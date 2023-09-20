FROM python:3.10 AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM base AS backend
COPY backend .

EXPOSE 80
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "80", "--workers", "2", "--reload", "server:app"]

FROM base AS frontend
RUN mkdir -p ~/.streamlit/
RUN echo "[general]"  > ~/.streamlit/credentials.toml && \
    echo "email = \"\""  >> ~/.streamlit/credentials.toml

ENV STREAMLIT_SERVER_ENABLE_STATIC_SERVING=TRUE
COPY frontend .
EXPOSE 80
ENTRYPOINT ["streamlit", "run", "__main__.py", "--browser.gatherUsageStats", "false", "--server.port", "80"](venv)
