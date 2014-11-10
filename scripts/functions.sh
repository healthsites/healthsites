#!/bin/bash

ORGANISATION=konektaz
PROJECT=healthsites

# Configurable options (though we recommend not changing these)
POSTGIS_PORT=49361
POSTGIS_CONTAINER_NAME=${PROJECT}-postgis

QGIS_SERVER_PORT=49362
QGIS_SERVER_CONTAINER_NAME=${PROJECT}-qgis-server

DJANGO_SERVER_PORT=49360
DJANGO_CONTAINER_NAME=${PROJECT}-django

DJANGO_DEV_SERVER_SSH_PORT=1122
DJANGO_DEV_SERVER_HTTP_PORT=1180
DJANGO_DEV_CONTAINER_NAME=${PROJECT}-django-dev
# Configurable options you probably want to change

PG_USER=docker
PG_PASS=docker
OPTIONS="-e DATABASE_NAME=gis -e DATABASE_USERNAME=${PG_USER} -e DATABASE_PASSWORD=${PG_PASS} -e DATABASE_HOST=${POSTGIS_CONTAINER_NAME} -e DJANGO_SETTINGS_MODULE=core.settings.prod_docker"

# -------------------------
function restart_postgis_server {

    echo "Starting docker postgis container for public data"
    echo "-------------------------------------------------"

    docker kill ${POSTGIS_CONTAINER_NAME}
    docker rm ${POSTGIS_CONTAINER_NAME}
    docker run \
        --restart="always" \
        --name="${POSTGIS_CONTAINER_NAME}" \
        --hostname="${POSTGIS_CONTAINER_NAME}" \
        -e USERNAME=${PG_USER} \
        -e PASS=${PG_PASS} \
        -p ${POSTGIS_PORT}:5432 \
        -d -t \
        kartoza/postgis


    # Todo:  prevent multiple entries in pgpass
    #echo "localhost:${POSTGIS_PORT}:*:${USER}:${PASSWORD}" >> ~/.pgpass

    sleep 20

}


function restart_qgis_server {

    echo "Running QGIS server"
    echo "-------------------"
    WEB_DIR=`pwd`/web
    chmod -R a+rX ${WEB_DIR}
    docker kill ${QGIS_SERVER_CONTAINER_NAME}
    docker rm ${QGIS_SERVER_CONTAINER_NAME}
    docker run \
        --restart="always" \
        --name="${QGIS_SERVER_CONTAINER_NAME}" \
        --hostname="${QGIS_SERVER_CONTAINER_NAME}" \
        --link ${POSTGIS_CONTAINER_NAME}:${POSTGIS_CONTAINER_NAME} \
        -d -t \
        -v ${WEB_DIR}:/web \
        -p ${QGIS_SERVER_PORT}:80 \
        kartoza/qgis-server

    echo "You can now consume WMS services at this url"
    echo "http://localhost:${QGIS_SERVER_PORT}/cgi-bin/qgis_mapserv.fcgi?map=/web/cccs_public.qgs"
}

function manage {
    echo "Running django management command"
    echo "---------------------------------"

    docker run \
        --rm \
        --name="${PROJECT}-manage" \
        --hostname="${PROJECT}-manage" \
        ${OPTIONS} \
        --link ${POSTGIS_CONTAINER_NAME}:${POSTGIS_CONTAINER_NAME} \
        -v /home/${USER}/production-sites/${PROJECT}:/home/web \
        --entrypoint="/usr/bin/python" \
        -i -t ${ORGANISATION}/${PROJECT} \
         /home/web/django_project/manage.py "$@"
}

function bash_prompt {
    echo "Running bash prompt in django container"
    echo "---------------------------------------"

    docker run \
        --rm \
        --name="${PROJECT}-bash" \
        --hostname="${PROJECT}-bash" \
        ${OPTIONS} \
        --link ${POSTGIS_CONTAINER_NAME}:${POSTGIS_CONTAINER_NAME} \
        -v /home/${USER}/production-sites/${PROJECT}:/home/web \
        --entrypoint="/bin/bash" \
        -i -t ${ORGANISATION}/${PROJECT} \
        -s
}

function run_django_server {
    echo "Running django uwsgi service with options:"
    echo "${@}"
    echo "------------------------------------------"

    docker kill ${DJANGO_CONTAINER_NAME}
    docker rm ${DJANGO_CONTAINER_NAME}
    docker run \
        --restart="always" \
        --name="${DJANGO_CONTAINER_NAME}" \
        --hostname="${DJANGO_CONTAINER_NAME}" \
        ${OPTIONS} \
        --link ${POSTGIS_CONTAINER_NAME}:${POSTGIS_CONTAINER_NAME} \
        -v /home/${USER}/production-sites/${PROJECT}:/home/web \
        -v /tmp/${PROJECT}-tmp:/tmp/${PROJECT}-tmp \
        -p 49360:49360 \
        -d -t ${ORGANISATION}/${PROJECT} $@
}


function run_django_dev_server {
    echo "Running django development server with option"
    echo "Access it via ssh on port ${DJANGO_DEV_SERVER_SSH_PORT} of your host"
    echo "Use these connection details:"
    echo ""
    echo "  user: docker"
    echo "  password: docker"
    echo ""
    echo "to log into the container via ssh or when setting up your"
    echo "pycharm remote python environment."
    echo ""
    echo "Access it via http on port ${DJANGO_DEV_SERVER_HTTP_PORT} of your host"
    echo "after starting the dev server like this:"
    echo ""
    echo "python manage.py runserver 0.0.0.0:${DJANGO_DEV_SERVER_HTTP_PORT}"
    echo "------------------------------------------"

    PROJECT_DIR=$(readlink -fn -- "${BASH_SOURCE%/*}/..")
    docker kill ${DJANGO_DEV_CONTAINER_NAME}
    docker rm ${DJANGO_DEV_CONTAINER_NAME}
    docker run \
        --restart="always" \
        --name="${DJANGO_DEV_CONTAINER_NAME}" \
        --hostname="${DJANGO_DEV_CONTAINER_NAME}" \
        ${OPTIONS} \
        --link ${POSTGIS_CONTAINER_NAME}:${POSTGIS_CONTAINER_NAME} \
        -v ${PROJECT_DIR}:/home/web \
        -v /tmp/${PROJECT}-tmp:/tmp/${PROJECT}-tmp \
        -p ${DJANGO_DEV_SERVER_SSH_PORT}:22 \
        -p ${DJANGO_DEV_SERVER_HTTP_PORT}:${DJANGO_DEV_SERVER_HTTP_PORT} \
        -d -t ${ORGANISATION}/${PROJECT}-dev $@
}
