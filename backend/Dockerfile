FROM python:3.9 AS base
WORKDIR /app

# RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt --no-warn-script-location
FROM base AS app

WORKDIR /app
COPY . .

WORKDIR /
EXPOSE 80
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "80", "--workers", "2", "app.__main__:app"]
