FROM python:3.12-slim

WORKDIR /work

COPY requirements.txt /work/requirements.txt
COPY server /work/Client

EXPOSE 5005

RUN pip install --no-cache-dir -r requirements.txt && rm -rf /root/.cache/pip

CMD ['python', 'server/app.py']
