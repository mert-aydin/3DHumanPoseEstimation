FROM python:3.9-slim-buster

LABEL maintainers="Mert Aydın & Sadık Kuzu"

ENV PYTHONUNBUFFERED=1

WORKDIR /cv

COPY requirements.txt .

RUN : \
    && apt update -y \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt install -y --no-install-recommends libgl1-mesa-glx libglib2.0-0 make \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && :

COPY Makefile .
COPY main*.py .
