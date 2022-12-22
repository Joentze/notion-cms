FROM python:3.8

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT app:app