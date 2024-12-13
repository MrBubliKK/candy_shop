FROM python:3.11-slim

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app
COPY ./celery_app /app/celery_app

CMD ["celery", "-A", "celery_app.worker", "worker", "--loglevel=info"]
