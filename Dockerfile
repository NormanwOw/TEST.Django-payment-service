FROM python:3.9.13-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY /pyproject.toml /app

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

LABEL project='django_payment_service' version=1.0