# FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
# RUN apk --update add bash nano
# ENV STATIC_URL /static
# ENV STATIC_PATH /var/www/app/static
# RUN pip install -r /var/www/requirements.txt
# EXPOSE 80
# EXPOSE 443

# CMD ["flask","run","--host","0.0.0.0"]



FROM python:3.7-slim


WORKDIR /app
COPY ./requirements.txt requirements.txt

RUN apt-get clean \
    && apt-get -y update \
    && pip install --upgrade pip  \
    && apt-get -y install python3-dev \
    && apt-get -y install uwsgi-plugins-all \
    && apt-get -y install build-essential \
    && pip install -r requirements.txt \
    && rm -rf /var/cache/apk/*

COPY . /app

CMD ["uwsgi", "--ini", "uwsgi.ini", "--enable-threads"]