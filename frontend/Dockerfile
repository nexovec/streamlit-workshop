FROM python:3.9 AS base
# TODO: supply pip cache location with a default value as ARG
# TODO: supply pip server location with a default value as ARG
# TODO: supply server port with a default value as ARG
WORKDIR /app

# RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt --no-warn-script-location

FROM base as environment

RUN mkdir -p ~/.streamlit/
RUN echo "[general]"  > ~/.streamlit/credentials.toml && \
    echo "email = \"\""  >> ~/.streamlit/credentials.toml


FROM environment AS app
ENV STREAMLIT_SERVER_ENABLE_STATIC_SERVING=TRUE
COPY . .
EXPOSE 80
ENTRYPOINT ["streamlit", "run", "__main__.py", "--browser.gatherUsageStats", "false", "--server.port", "80"]