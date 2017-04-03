#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on debian
FROM kartoza/django-base
MAINTAINER Tim Sutton<tim@kartoza.com>

#RUN  ln -s /bin/true /sbin/initctl

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not with to use caching
ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng

RUN apt-get -y update

#-------------Application Specific Stuff ----------------------------------------------------

RUN apt-get -y install libpq5

ADD REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install -r /REQUIREMENTS.txt
RUN pip install uwsgi

RUN apt-get update -y; apt-get -y --force-yes install yui-compressor

# Open port 49360 as we will be running our uwsgi socket on that
EXPOSE 49360

ADD sources.list /etc/apt/sources.list.d/
RUN apt-get update -y
RUN apt-get install vim -y
RUN apt-get install certbot -t jessie-backports -y
ADD rpl-1.5.5.egg-info /usr/lib/pymodules/python2.7/

# You could put --protocol=http as a parameter (to test it directly)
# when running e.g. docker run konektaz/healthsites --protocol=http
# or any other wsgi parameters and they will be tagged on to the
# the end of the entrypoint.

# Under normal usage you would supply no additional params and
# use nginx on the host to forward in the traffic.
WORKDIR /home/web/django_project
CMD ["uwsgi", "--ini", "/uwsgi.conf"]
