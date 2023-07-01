FROM python:slim

COPY server /server

RUN pip install -r /server/requirements.txt

ARG ENVIRONMENT="Staging"

ARG ECHO_DATA="Default echo"

CMD cd server && python main.py