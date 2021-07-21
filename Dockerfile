# syntax=docker/dockerfile:1

FROM python:3.9.1

WORKDIR /usr/local

COPY . .

COPY ./nltk_data /usr/local/nltk_data

RUN pip install pipenv

RUN pipenv install --system --deploy

CMD ["python", "core.py"]

