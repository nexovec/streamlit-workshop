FROM python:3.9-slim AS base
ARG USE_VENV_PIP_CACHE

WORKDIR /app
COPY . .

RUN if [ -z "$USE_VENV_PIP_CACHE" ]; then \
    echo "Variable not defined"; \
  else \
    echo "Variable is defined: $USE_VENV_PIP_CACHE"; \
  fi

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir --no-warn-script-location

RUN mkdir -p ~/.streamlit/
RUN echo "[general]"  > ~/.streamlit/credentials.toml && \
    echo "email = \"\""  >> ~/.streamlit/credentials.toml
FROM base AS app
ENTRYPOINT ["streamlit", "run", "webui.py", "--browser.gatherUsageStats", "false", "--server.enableCORS", "true", "--server.port", "5000"]