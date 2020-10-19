FROM python:3.7 as base

ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y postgresql-client-11
RUN pip install -r requirements.txt --no-cache-dir 
COPY . /app/

CMD /app/bin/entrypoint.sh


