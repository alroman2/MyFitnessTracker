FROM ubuntu:22.04
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg libsm6 libxext6 libgl1

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3.10
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y pip

RUN pip install asgiref==3.5.0
RUN pip install autopep8==1.6.0
RUN pip install Django==4.0.6
RUN pip install django-cors-headers==3.13.0
RUN pip install djangorestframework==3.13.1
RUN pip install requests==2.28.1
RUN pip install urllib3==1.26.11
RUN pip install gunicorn==20.1.0
RUN pip install sqlparse==0.4.2
RUN pip install psycopg2-binary==2.9.3
RUN pip install tzdata

RUN apt install -y git

RUN mkdir /backend

WORKDIR /backend
COPY . /backend/

EXPOSE 8080