#!/bin/bash
DOMAIN='-d staging.healthsites.io'
EMAIL='dimas@kartoza.com'

# clone Let's Encrypt repository in /opt
sudo git clone https://github.com/letsencrypt/letsencrypt /opt/letsencrypt

# makes sure fireware allow TCP traffic on port 443
sudo ufw allow 443/tcp

# stop the nginx server
sudo docker stop cyanolakes-web

# run Let's Encrypt use the standalone plugin
sudo /opt/letsencrypt/./letsencrypt-auto certonly --standalone --agree-tos --text --email $EMAIL $DOMAIN

# start the nginx server again
sudo make run

# Modify nginx configuration
# server {
# 	listen 8080 ssl;

# 	server_name healthsites.io;

# 	ssl on;
# 	ssl_certificate /etc/letsencrypt/live/healthsites.io/fullchain.pem;
# 	ssl_certificate_key /etc/letsencrypt/live/healthsites.io/privkey.pem;
# 	ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
# 	ssl_prefer_server_ciphers on;
# 	ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';
# }

# server {
# 	listen 8081;
# 	server_name healthsites.io;
# 	return 301 https://$host$request_uri;
# }

# modify docker-compose on web
# web:
#	volumes:
# 	  ......
#     - /etc/letsencrypt:/etc/letsencrypt
#   ports:
#     - "80:8081"
#     - "443:8080"
