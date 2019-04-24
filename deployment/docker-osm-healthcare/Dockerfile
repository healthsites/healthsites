# This image is intended to be used as a storage
# only container

FROM byrnedo/alpine-curl
MAINTAINER Tim Sutton <tim@kartoza.com>

RUN mkdir /settings
RUN wget https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf -O settings/country.pbf
ADD mapping.yml /settings/mapping.yml
ADD clip /settings/clip
ADD qgis_style.sql /settings/qgis_style.sql
