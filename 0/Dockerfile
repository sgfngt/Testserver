FROM ubuntu:20.04

WORKDIR /testserver-app
COPY requirements.txt .

RUN apt update -y
RUN apt install python3.8 -y
RUN apt install python3-pip -y
RUN pip3 install -r requirements.txt

COPY /1 .

COPY wait-for-it.sh /wait-for-it.sh

CMD ["sh", "-c", "/wait-for-it.sh postgres:5432 -- python3 app.py"]
