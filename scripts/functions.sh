#!/bin/bash


# Configurable options (though we recommend not changing these)
POSTGIS_PORT=49361
POSTGIS_CONTAINER_NAME=healthsites-postgis
QGIS_SERVER_PORT=49362
QGIS_SERVER_CONTAINER_NAME=healthsites-qgis-server
DJANGO_SERVER_PORT=49360
DJANGO_CONTAINER_NAME=healthsites-django
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
        --name="healthsites-manage" \
        --hostname="healthsites-manage" \
        ${OPTIONS} \
        --link ${POSTGIS_CONTAINER_NAME}:${POSTGIS_CONTAINER_NAME} \
        -v /home/${USER}/production-sites/healthsites:/home/web \
        --entrypoint="/usr/bin/python" \
        -i -t konektaz/healthsites \
         /home/web/django_project/manage.py "$@"
}

function run_django_server {
    echo "Running django uwsgi service with options:"
    echo "${@}"
    echo "------------------------------------------"

    docker kill healthsites-django
    docker rm healthsites-django
    docker run \
        --restart="always" \
        --name="${DJANGO_CONTAINER_NAME}" \
        --hostname="${DJANGO_CONTAINER_NAME}" \
        ${OPTIONS} \
        --link ${POSTGIS_CONTAINER_NAME}:${POSTGIS_CONTAINER_NAME} \
        -v /home/${USER}/production-sites/healthsites:/home/web \
        -v /tmp/healthsites-tmp:/tmp/healthsites-tmp \
        -p 49360:49360 \
        -d -t konektaz/healthsites $@
}
