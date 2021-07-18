# syntax=docker/dockerfile:1

FROM python:3.9.1

WORKDIR /usr/local

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

COPY ./nltk_data /usr/local/nltk_data

CMD [ "python3",  "core.py"]

