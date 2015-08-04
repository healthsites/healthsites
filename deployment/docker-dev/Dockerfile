#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM konektaz/healthsites
MAINTAINER Tim Sutton<tim@linfiniti.com>

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not with to use caching
ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng

RUN apt-get -y update
RUN apt-get -y install openssh-server
RUN mkdir /var/run/sshd

#-------------Application Specific Stuff ----------------------------------------------------
# Open port 22 so linked containers can see it and 8000 for django test server
EXPOSE 22 8000
ADD start.sh /start.sh
RUN chmod 0755 /start.sh

ADD REQUIREMENTS-dev.txt /REQUIREMENTS-dev.txt
RUN pip install -r /REQUIREMENTS-dev.txt

ENTRYPOINT ["/start.sh"]

# You should be able to log in to this container and set it up as a remote
# python environment in pycharm - user and password will be docker
# NOTE: This docker container is meant for development only!
