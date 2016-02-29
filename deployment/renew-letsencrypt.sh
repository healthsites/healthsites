#!/bin/bash
DOMAIN='-d staging.healthsites.io'
EMAIL='dimas@kartoza.com'
DIRECTORY=$1

cd $DIRECTORY

# stop running nginx
sudo docker stop cyanolakes-web

# run Let's Encrypt use the standalone plugin
sudo /opt/letsencrypt/./letsencrypt-auto certonly --standalone --agree-tos --text --email $EMAIL $DOMAIN

# start the nginx server again
sudo make web
