FROM python:3.9.6-buster

WORKDIR /app

ADD . /app

ENV FLASK_APP=transform
ENV FLASK_ENV=production
ENV TZ=Asia/Seoul

RUN pip install -r requirements.txt
RUN flask init-db

CMD ["uwsgi","uwsgi.ini"]