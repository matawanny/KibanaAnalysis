FROM python:3.7

WORKDIR /app

COPY requirements.txt /app/requirements.txt

COPY . .

RUN pip install -r requirements.txt
