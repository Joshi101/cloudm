FROM python:3.7-alpine

RUN mkdir /code
RUN apk add --no-cache gcc \
                       libc-dev \
                       libffi-dev  \
        && rm -rf /var/cache/apk/*
WORKDIR /code
COPY requirements.txt setup.py tox.ini ./
RUN pip install -r requirements.txt
RUN pip install -e .

COPY cloudm cloudm/
COPY migrations migrations/

EXPOSE 5000
