FROM python:3.8.0-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Install pyscopg2 dependencies
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev 

RUN pip install --upgrade pip
COPY . /usr/src/app
RUN pip install -r requirements.txt

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]

