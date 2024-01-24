FROM ubuntu:18.04 AS prod
MAINTAINER Irwan Fathurrahman<meomancer@gmail.com>

# Pandoc needed to generate rst dumps, uic compressor needed for django-pipeline
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev gdal-bin gettext libcurl4-openssl-dev libssl-dev yui-compressor git vim

ENV PATH /usr/local/bin:$PATH

ADD deployment/docker/uwsgi.conf /uwsgi.conf

RUN apt-get install locales -y && \
    echo "en_ZA.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen en_ZA.UTF-8
ENV LANG en_ZA.UTF-8
ENV LANGUAGE en_ZA:en
ENV LC_ALL en_ZA.UTF-8

ADD deployment/docker/REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip3 install --upgrade pip && pip install --upgrade pip
RUN pip install -r /REQUIREMENTS.txt

RUN apt-get install nodejs-dev node-gyp libssl1.0-dev -y
RUN apt-get install npm -y
RUN npm -g install yuglify

RUN ln -s /usr/bin/python3 /usr/local/bin/python

ADD django_project /home/web/django_project

# Open port 8080 as we will be running our uwsgi socket on that
EXPOSE 8080

WORKDIR /home/web/django_project
CMD ["uwsgi", "--ini", "/uwsgi.conf"]


# --------------------------------------------------------------
# DEVELOPMENT
# --------------------------------------------------------------
FROM prod AS dev

# This section taken on 2 July 2015 from
# https://docs.docker.com/examples/running_ssh_service/
# Sudo is needed by pycharm when it tries to pip install packages
RUN apt-get update && apt-get install -y openssh-server sudo
RUN mkdir /var/run/sshd
RUN echo 'root:docker' | chpasswd
RUN sed -i 's/^PermitRootLogin */#PermitRootLogin /' /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# End of cut & paste section

ADD deployment/docker/REQUIREMENTS-dev.txt /REQUIREMENTS-dev.txt
RUN pip install -r /REQUIREMENTS-dev.txt

# --------------------------------------------------------
# Open ports as needed
# --------------------------------------------------------

# Open port 8080 as we will be running our django dev server on
EXPOSE 8080
# Open port 22 as we will be using a remote interpreter from pycharm
EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
