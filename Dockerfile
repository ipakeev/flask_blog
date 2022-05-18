FROM python:3.9.11-alpine
RUN apk add --no-cache libpq-dev postgresql-libs gcc musl-dev postgresql-dev libffi-dev

ENV PYTHONBUFFERED=1
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT python main.py