# Dockerfile

FROM python:3.5-alpine

COPY . /app

RUN pip3 install -r /app/requirements.txt

EXPOSE 8000

WORKDIR /app/paperserver

CMD ["gunicorn", "admin.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
