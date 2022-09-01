FROM python:3.10.4

WORKDIR /app

COPY . .


RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \

  git

RUN pip install poetry

RUN poetry export -f requirements.txt -o requirements.txt --without-hashes

RUN pip install -r requirements.txt

RUN pip uninstall psycopg2

RUN pip3 install psycopg2-binary

CMD uvicorn app:app --reload --host 0.0.0.0 --port ${PORT} --log-level "info"