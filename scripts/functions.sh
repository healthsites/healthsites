#!/bin/bash

# Configurable options you probably want to change are stored in config.sh
source ${BASH_SOURCE%/*}/config.sh

# Configurable options (though we recommend not changing these)
# Root directory of this git project
PROJECT_DIR=$(readlink -fn -- "${BASH_SOURCE%/*}/..")
GIS_DATA_DIR=${PROJECT_DIR}/webmaps

# This is configured in the dockerfile
DJANGO_UWSGI_INTERNAL_PORT=49360
# To run in test mode, simply set the test mode env var in your script
# e.g.
#
# TEST_MODE=1 scripts/create_docker_env.sh
#

if [ -n "${TEST_MODE+1}" ]
then
    # If the TEST env var is set we run on different ports etc.
    echo "Running test site configuration."
    echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    BASE_PORT=$((BASE_PORT + 100))
    POSTGIS_PORT=${BASE_PORT}
    POSTGIS_CONTAINER_NAME=test-${PROJECT}-postgis
    BASE_PORT=$((BASE_PORT + 1))

    QGIS_SERVER_PORT=${BASE_PORT}
    QGIS_SERVER_CONTAINER_NAME=test-${PROJECT}-qgis-server
    BASE_PORT=$((BASE_PORT + 1))

    DJANGO_SERVER_PORT=${BASE_PORT}
    DJANGO_CONTAINER_NAME=test-${PROJECT}
    BASE_PORT=$((BASE_PORT + 1))
else
    # Production mode
    echo "Running produciton site configuration."
    echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    # for test deployment we run 100 ports above prod
    POSTGIS_PORT=${BASE_PORT}
    POSTGIS_CONTAINER_NAME=${PROJECT}-postgis
    BASE_PORT=$((BASE_PORT + 1))

    QGIS_SERVER_PORT=${BASE_PORT}
    QGIS_SERVER_CONTAINER_NAME=${PROJECT}-qgis-server
    BASE_PORT=$((BASE_PORT + 1))

    DJANGO_SERVER_PORT=${BASE_PORT}
    DJANGO_CONTAINER_NAME=${PROJECT}
    BASE_PORT=$((BASE_PORT + 1))
fi

DJANGO_DEV_SERVER_SSH_PORT=${BASE_PORT}
BASE_PORT=$((BASE_PORT + 1))
DJANGO_DEV_SERVER_HTTP_PORT=${BASE_PORT}
BASE_PORT=$((BASE_PORT + 1))
DJANGO_DEV_CONTAINER_NAME=${PROJECT}-dev

OPTIONS="-e DATABASE_NAME=gis -e DATABASE_USERNAME=${PG_USER} -e DATABASE_PASSWORD=${PG_PASS} -e DATABASE_HOST=${POSTGIS_CONTAINER_NAME} -e DJANGO_SETTINGS_MODULE=core.settings.prod_docker"

function clean {
    echo "Cleaning away old pyc etc files."
    echo "-------------------------------------------------"
    find . -name '*~' -exec rm {} \;
    find . -name '*.pyc' -exec rm {} \;
    find . -name '*.pyo' -exec rm {} \;
    find . -name '*.orig' -exec rm {} \;
}

function get_postgis_image {
    echo "Getting docker postgis image if you don't already have it"
    echo "---------------------------------------------------------"
    if docker images | awk '{ print $1 }' | grep "^kartoza/postgis$" > /dev/null
    then
        echo "PostGIS docker image is already available, using that."
    else
        echo "Building PostGIS docker image"
        docker build -t kartoza/postgis git://github.com/kartoza/docker-postgis
    fi
}

function get_qgis_desktop_image {
    echo "Getting docker QGIS desktop image if you don't already have it"
    echo "--------------------------------------------------------------"
    if docker images | awk '{ print $1 }' | grep "^kartoza/qgis-desktop$" > /dev/null
    then
        echo "QGIS Desktop docker image is already available, using that."
    else
        echo "Fetching QGIS Desktop docker image"
        docker pull kartoza/qgis-desktop
    fi
}

function get_qgis_server_image {
    echo "Getting docker QGIS server image if you don't already have it"
    echo "--------------------------------------------------------------"
    if docker images | awk '{ print $1 }' | grep "^kartoza/qgis-server" > /dev/null
    then
        echo "QGIS Server docker image is already available, using that."
    else
        echo "Fetching QGIS Server docker image"
        docker pull kartoza/qgis-server
    fi
}

function build_django_image {
    echo "Getting docker django image if you don't already have it"
    echo "---------------------------------------------------------"
    if docker images | awk '{ print $1 }' | grep "^${ORGANISATION}/${PROJECT}" > /dev/null
    then
        echo "Django docker image is already available, using that."
    else
        echo "Building Django Server docker image"
        cd ${PROJECT_DIR}/docker-prod
        ./build.sh
        cd -
    fi
}

function build_django_dev_image {
    echo "Getting docker django DEVELOPER image if you don't already have it"
    echo "------------------------------------------------------------------"
    if docker images | awk '{ print $1 }' | grep "^${ORGANISATION}/${PROJECT}-dev" > /dev/null
    then
        echo "Django docker image is already available, using that."
    else
        echo "Building Django Server docker image"
        cd ${PROJECT_DIR}/docker-dev
        ./build.sh
        cd -
    fi
}

function restart_postgis_server {

    echo "Starting docker postgis container for public data"
    echo "-------------------------------------------------"
    get_postgis_image

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
    get_qgis_server_image


    # Note reference to PostGIS db may break when running in testmode
    # since the pg link as test- prefixed to it so QGIS project files
    # may not work.
    chmod -R a+rX ${GIS_DATA_DIR}
    docker kill ${QGIS_SERVER_CONTAINER_NAME}
    docker rm ${QGIS_SERVER_CONTAINER_NAME}
    docker run \
        --restart="always" \
        --name="${QGIS_SERVER_CONTAINER_NAME}" \
        --hostname="${QGIS_SERVER_CONTAINER_NAME}" \
        --link ${POSTGIS_CONTAINER_NAME}:${POSTGIS_CONTAINER_NAME} \
        -d -t \
        -v ${GIS_DATA_DIR}:/web \
        -p ${QGIS_SERVER_PORT}:80 \
        kartoza/qgis-server

    echo "You can now consume WMS services at this url"
    echo "http://localhost:${QGIS_SERVER_PORT}/cgi-bin/qgis_mapserv.fcgi?map=/web/foo.qgs"
}

function run_qgis_desktop {
    echo "Running QGIS Desktop"
    echo "--------------------"
    get_qgis_desktop_image
    xhost +
    # Home is mounted so QGIS finds your Qt and QGIS settings
    # /web is mounted as it is also available in the QGIS Server
    # context, so anything you put there (e.g. .qgs projects)
    # will be made available to the QGIS server instance.

    docker run --rm --name="qgis-desktop-${PROJECT}" \
        -i -t \
        -v ${HOME}:/home/${USER} \
        -v ${GIS_DATA_DIR}:/web \
        --link ${POSTGIS_CONTAINER_NAME}:${POSTGIS_CONTAINER_NAME} \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -e DISPLAY=unix$DISPLAY \
        kartoza/qgis-desktop:latest
    xhost -
}

function manage {
    echo "Running django management command"
    echo "---------------------------------"
    build_django_image

    docker run \
        --rm \
        --name="${PROJECT}-manage" \
        --hostname="${PROJECT}-manage" \
        ${OPTIONS} \
        --link ${POSTGIS_CONTAINER_NAME}:${POSTGIS_CONTAINER_NAME} \
        -v ${PROJECT_DIR}:/home/web \
        --entrypoint="/usr/bin/python" \
        -i -t ${ORGANISATION}/${PROJECT} \
         /home/web/django_project/manage.py "$@"
}

function bash_prompt {
    echo "Running bash prompt in django container"
    echo "---------------------------------------"
    build_django_image

    docker run \
        --rm \
        --name="${PROJECT}-bash" \
        --hostname="${PROJECT}-bash" \
        ${OPTIONS} \
        --link ${POSTGIS_CONTAINER_NAME}:${POSTGIS_CONTAINER_NAME} \
        -v ${PROJECT_DIR}:/home/web \
        --entrypoint="/bin/bash" \
        -i -t ${ORGANISATION}/${PROJECT} \
        -s
}

function run_django_server {
    echo "Running django uwsgi service with options:"
    echo "${@}"
    echo "------------------------------------------"
    build_django_image

    docker kill ${DJANGO_CONTAINER_NAME}
    docker rm ${DJANGO_CONTAINER_NAME}
    docker run \
        --restart="always" \
        --name="${DJANGO_CONTAINER_NAME}" \
        --hostname="${DJANGO_CONTAINER_NAME}" \
        ${OPTIONS} \
        --link ${POSTGIS_CONTAINER_NAME}:${POSTGIS_CONTAINER_NAME} \
        -v ${PROJECT_DIR}:/home/web \
        -p ${DJANGO_SERVER_PORT}:${DJANGO_UWSGI_INTERNAL_PORT} \
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

    docker kill ${DJANGO_DEV_CONTAINER_NAME}
    docker rm ${DJANGO_DEV_CONTAINER_NAME}
    docker run \
        --restart="always" \
        --name="${DJANGO_DEV_CONTAINER_NAME}" \
        --hostname="${DJANGO_DEV_CONTAINER_NAME}" \
        ${OPTIONS} \
        --link ${POSTGIS_CONTAINER_NAME}:${POSTGIS_CONTAINER_NAME} \
        -v ${PROJECT_DIR}:/home/web \
        -p ${DJANGO_DEV_SERVER_SSH_PORT}:22 \
        -p ${DJANGO_DEV_SERVER_HTTP_PORT}:${DJANGO_DEV_SERVER_HTTP_PORT} \
        -d -t ${ORGANISATION}/${PROJECT}-dev $@
}
