FROM ubuntu:14.04

MAINTAINER Airwallex

LABEL version="1.5" description="Parser of Source of Truth"


RUN apt-get update
#RUN apt-get -y upgrade

RUN apt-get install -y python-dev python-pip libpq-dev
RUN apt-get -y install postgresql postgresql-contrib

#RUN mkdir -p /app
ADD . /app
ENV HOME /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

#HEALTHCHECK --interval=5s --timeout=2s --start-period=20m --retries=3 \
#    CMD curl --fail http://localhost:5000/login || exit 1

ENTRYPOINT ["python"]
CMD ["app.py"]



