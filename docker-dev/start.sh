#!/bin/sh

# This script is run inside the container when it starts

# Ensure we have a user who matches the developer who owns this dir
SITE_PATH="/home/web/"

USER_ID=`ls -lahn ${SITE_PATH}/django_project | tail -1 | awk {'print $3'}`
GROUP_ID=`ls -lahn ${SITE_PATH}/django_project | tail -1 | awk {'print $4'}`

groupadd -g ${GROUP_ID} docker
useradd --shell /bin/bash --uid ${USER_ID} --gid ${GROUP_ID} --home ${SITE_PATH} docker
groupadd admin
usermod -a -G admin docker

# set docker user password to 'docker'
echo 'docker:docker' |chpasswd
# Set root password to 'docker'
echo 'root:docker' |chpasswd

# Fix irritation with new geos incompatibility on django 1.4?
#sed -i "/\$.*/ {N; s/\$.*def geos_version_info/\.\*\$\'\)\ndef geos_version_info/g}"  \
#   /usr/local/lib/python2.7/dist-packages/django/contrib/gis/geos/libgeos.py

/usr/sbin/sshd -D
