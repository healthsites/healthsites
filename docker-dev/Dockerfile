#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM ubuntu:trusty
MAINTAINER Tim Sutton<tim@linfiniti.com>

RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN  dpkg-divert --local --rename --add /sbin/initctl
#RUN  ln -s /bin/true /sbin/initctl

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not with to use caching
ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng

RUN apt-get -y update
RUN apt-get -y install openssh-server libpq5 python-gdal python-geoip python python-dev python-distribute python-pip python-psycopg2 npm
RUN mkdir /var/run/sshd

#-------------Application Specific Stuff ----------------------------------------------------
# Open port 22 so linked containers can see it and 8000 for django test server
EXPOSE 22 8000
ADD start.sh /start.sh
RUN chmod 0755 /start.sh

RUN npm -g install yuglify
# Shameless duplication from REQUIREMENTS because that file is not visible in
# the docker build scope.
RUN pip install Django==1.7.1 psycopg2 pytz django-braces django-model-utils django-pipeline nodeenv


CMD /start.sh

# You should be able to log in to this container and set it up as a remote
# python environment in pycharm - user and password will be docker
# NOTE: This docker container is meant for development only!
