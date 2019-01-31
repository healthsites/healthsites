# This image is intended to be used as a storage
# only container

FROM byrnedo/alpine-curl
MAINTAINER Tim Sutton <tim@kartoza.com>

RUN mkdir /settings
RUN curl -o /settings/country.pbf https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf
ADD mapping.yml /settings/mapping.yml
ADD clip /settings/clip
ADD qgis_style.sql /settings/qgis_style.sql
