FROM python:3.10.4

WORKDIR /app

COPY . .

RUN pip install poetry

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt

RUN pip install -r requirements.txt

CMD uvicorn app:app --host 0.0.0.0 --port ${PORT}