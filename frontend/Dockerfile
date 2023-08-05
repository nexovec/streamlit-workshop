FROM python:3.9 AS base
ARG USE_PIP_CACHE
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt --no-warn-script-location

FROM base as environment

RUN mkdir -p ~/.streamlit/
RUN echo "[general]"  > ~/.streamlit/credentials.toml && \
    echo "email = \"\""  >> ~/.streamlit/credentials.toml


FROM environment AS app

# WORKDIR /app
COPY . .

# for the frontend
EXPOSE 5000
# for the backend
# EXPOSE 5001

# ENTRYPOINT ["python", "."]
# ENTRYPOINT ["streamlit", "run", ".", "--browser.gatherUsageStats", "false", "--server.enableCORS", "true", "--server.port", "5000"]
ENTRYPOINT ["streamlit", "run", "__main__.py", "--browser.gatherUsageStats", "false", "--server.port", "5000"]