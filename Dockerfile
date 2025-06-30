FROM python:3.12

WORKDIR /work

COPY requirements.txt /work/requirements.txt
COPY server /work/Client

EXPOSE 8080

RUN apt-get update && apt-get install -y \
    cmake \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

CMD ["python", "Client/app.py"]