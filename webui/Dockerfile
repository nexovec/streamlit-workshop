FROM python:3.9-slim AS base
ARG USE_PIP_CACHE
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt --no-warn-script-location

RUN mkdir -p ~/.streamlit/
RUN echo "[general]"  > ~/.streamlit/credentials.toml && \
    echo "email = \"\""  >> ~/.streamlit/credentials.toml

COPY . .

FROM base AS app

EXPOSE 5000
ENTRYPOINT ["python", "."]
# ENTRYPOINT ["streamlit", "run", "webui/index.py", "--browser.gatherUsageStats", "false", "--server.enableCORS", "true", "--server.port", "5000"]