# FOR DOCKER BUILDS IN ARM64/M1 MACS: 
# https://stackoverflow.com/questions/66920645/exec-format-error-when-running-containers-build-with-apple-m1-chip-arm-based
# RUN: docker buildx build --platform linux/amd64 -t notion-cms-image .


FROM python:3.8

ENV PYTHONUNBUFFERED True

WORKDIR /app

COPY . ./

ADD . /app

RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app