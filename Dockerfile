FROM python:3.4.9-wheezy

MAINTAINER Zach Yam "zach.yam@cognite.com"

RUN pip install requests

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
