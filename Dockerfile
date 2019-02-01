FROM python:3.6.8-alpine

LABEL Name=districtr-api Version=0.0.1
EXPOSE 5000

# Install gcc for psycopg2
RUN apk add gcc

# This is where we'll put the app:
WORKDIR /app

# Install pipenv
RUN python3 -m pip install pipenv

# Install dependencies from Pipfile
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --deploy

# Copy the app into the container
COPY . /app
ENV FLASK_APP api

# Script to do database migrations and then run app:
RUN chmod +x ./up.sh
ENTRYPOINT [ "./up.sh" ]