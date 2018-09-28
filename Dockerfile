FROM python:3.6-alpine

MAINTAINER Zach Yam "zach.yam@cognite.com"

#Install git
RUN apk add curl git unzip bash openssh

COPY kaknas /app/kaknas

COPY manager.py /app/

COPY setup.py /app/

COPY requirements.txt /app/

WORKDIR /app

#Install requirements
RUN pip install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "manager.py", "runserver" ]
