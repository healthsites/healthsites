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

#-------------Application Specific Stuff ----------------------------------------------------

RUN apt-get -y install libpq5 python-gdal python-geoip \
    python python-dev python-distribute python-pip \
    python-psycopg2 npm node rpl
RUN npm -g install yuglify

# Ubuntu is messed up and aliases node as node js
# So when yuglify is installed it references the wrong node binary...
# lets fixt that here...

RUN rpl "env node" "env nodejs" /usr/local/lib/node_modules/yuglify/bin/yuglify

ADD REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install -r /REQUIREMENTS.txt
RUN pip install uwsgi

ADD uwsgi.conf /uwsgi.conf
ADD uwsgi_params /uwsgi_params

# Open port 49360 as we will be running our uwsgi socket on that
EXPOSE 49360


# You could put --protocol=http as a parameter (to test it directly)
# when running e.g. docker run konektaz/healthsites --protocol=http
# or any other wsgi parameters and they will be tagged on to the
# the end of the entrypoint.

# Under normal usage you would supply no additional params and
# use nginx on the host to forward in the traffic.
ENTRYPOINT ["uwsgi", "--ini", "/home/web/docker-prod/uwsgi.conf"]
