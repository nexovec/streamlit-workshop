FROM python:3.9-slim AS base
ARG USE_PIP_CACHE
WORKDIR /app
COPY . .

# FIXME: this doesn't work as intended, the if always executes.
# TODO: add pip cache if any is available
RUN if [ -z "$USE_PIP_CACHE" ]; then \
    echo "USING PIP CACHE IS NOT IMPLEMENTED"; \
  else \
    echo "NOT USING PIP CACHE"; \
  fi

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache --no-warn-script-location

RUN mkdir -p ~/.streamlit/
RUN echo "[general]"  > ~/.streamlit/credentials.toml && \
    echo "email = \"\""  >> ~/.streamlit/credentials.toml
FROM base AS app

EXPOSE 5000
ENTRYPOINT ["python", "."]
# ENTRYPOINT ["streamlit", "run", "webui/index.py", "--browser.gatherUsageStats", "false", "--server.enableCORS", "true", "--server.port", "5000"]