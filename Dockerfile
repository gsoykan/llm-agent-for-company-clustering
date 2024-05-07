FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

#RUN apt-get update && apt-get install -y
#gcc python3-dev
#&& apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000