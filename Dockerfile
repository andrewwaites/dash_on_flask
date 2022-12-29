FROM python:3.9.4-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
# COPY ../../extra_dash .

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
