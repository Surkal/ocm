FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y python3 python3-pip jq firefox-geckodriver xvfb && \
    rm -rf /var/lib/apt/lists/*

ENV WORKING_DIR=/home/app/src
RUN mkdir -p $WORKING_DIR
WORKDIR $WORKING_DIR

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt $WORKING_DIR
COPY /src $WORKING_DIR
RUN pip3 install --no-cache-dir -r requirements.txt

ENV FLASK_APP app.py

EXPOSE 5000

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]