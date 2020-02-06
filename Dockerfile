FROM python:3.7

RUN mkdir /code
WORKDIR /code

COPY requirements.txt setup.py tox.ini ./
RUN pip install -r requirements.txt
RUN pip install -e .

COPY cloudm cloudm/
COPY migrations migrations/

EXPOSE 5000
