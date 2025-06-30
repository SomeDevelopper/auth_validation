FROM python:3.12-slim

WORKDIR /work

RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libgl1 \
    libboost-all-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /work/requirements.txt
COPY server /work/Client

EXPOSE 5005

RUN pip install --no-cache-dir -r requirements.txt && rm -rf /root/.cache/pip

CMD ['python', 'server/app.py']
