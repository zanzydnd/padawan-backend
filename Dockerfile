FROM python:3.9.7

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./requirements_backend.txt

RUN pip install -r requirements_backend.txt

COPY . .

EXPOSE 8000

RUN python3 src/manage.py collectstatic --noinput

CMD python3 src/manage.py migrate && gunicorn padawan.wsgi --chdir src --bind 0.0.0.0 --preload --log-file -