FROM python:3.11-slim

WORKDIR /app

ADD Capabilities Capabilities

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/* 

RUN pip install -r Capabilities/requirements.txt

RUN python -m spacy download en_core_web_sm

EXPOSE 8910

ENTRYPOINT python ./Capabilities/app.py