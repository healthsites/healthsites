#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on debian
FROM python:2.7.8
MAINTAINER Tim Sutton<tim@kartoza.com>

RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN  dpkg-divert --local --rename --add /sbin/initctl
#RUN  ln -s /bin/true /sbin/initctl

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not with to use caching
ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng

RUN apt-get -y update

#-------------Application Specific Stuff ----------------------------------------------------

RUN apt-get -y install libpq5 python-gdal python-geoip \
    python python-dev python-distribute python-pip \
    python-psycopg2 npm nodejs rpl
RUN npm -g install yuglify

# Debian is messed up and aliases node as nodejs
# So when yuglify is installed it references the wrong node binary...
# lets fix that here...

RUN rpl "env node" "env nodejs" /usr/local/lib/node_modules/yuglify/bin/yuglify

ADD REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install -r /REQUIREMENTS.txt
RUN pip install uwsgi

ADD uwsgi.conf /uwsgi.conf

# Open port 49360 as we will be running our uwsgi socket on that
EXPOSE 49360

WORKDIR /home/web/django_project
# You could put --protocol=http as a parameter (to test it directly)
# when running e.g. docker run inasafe/inasafe --protocol=http
# or any other wsgi parameters and they will be tagged on to the
# the end of the entrypoint.

# Under normal usage you would supply no additional params and
# use nginx on the host to forward in the traffic.
# Entrypoint is preferred but we use CMD
# as fig run does not currently correctly
# overload entrypoint
CMD ["uwsgi", "--ini", "/uwsgi.conf"]
