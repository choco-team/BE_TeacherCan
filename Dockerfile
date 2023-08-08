FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app/

WORKDIR /app

# ENTRYPOINT [ "uvicorn", "app.main:app", "--host", "0.0.0.0" ]
