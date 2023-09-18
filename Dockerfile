FROM python:3.9-slim

WORKDIR /app

ADD Capabilities Capabilities

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r Capabilities/requirements.txt

EXPOSE 8910

ENTRYPOINT python ./Capabilities/app.py