FROM python:3.10

WORKDIR opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt requirements.txt

RUN  mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/ \
     && pip install --upgrade pip \
     && pip install -r requirements.txt

RUN wget https://github.com/stripe/stripe-cli/releases/download/v1.13.8/stripe_1.13.8_linux_x86_64.tar.gz \
    && tar -xvf stripe_1.13.8_linux_x86_64.tar.gz \
    && mv stripe /usr/local/bin/stripe \
    && rm stripe_1.13.8_linux_x86_64.tar.gz

COPY . .

EXPOSE 8000

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
