#!/bin/sh -x

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
set -o pipefail
set -o nounset


cat <<EOF > /etc/nginx/conf.d/nginx.conf
upstream app_server {
    server ${SERVER_HOST}:8080;
}

upstream rabbitmq_mq {
    server ${RABBITMQ_HOST}:15672;
}

server {
    listen 8080;
    location / {
        proxy_pass http://app_server;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$host;
        proxy_redirect off;
    }
}

server {
    listen 15672;
    location / {
        proxy_pass http://rabbitmq_mq;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$host;
        proxy_redirect off;
    }
}

EOF


exec "$@"
