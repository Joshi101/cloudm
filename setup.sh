#!/bin/bash
set -x

ENV_FILE=''
APP='cloudm'
export repo=/opt/${APP}
ENV_FILE=${repo}/.env
echo "Using docker_env file: $ENV_FILE"
mkdir -p /var/log/cloudm/
mkdir -p /var/media/cloudm/
sudo cp ${repo}/docker/nginx_config /etc/nginx/sites-enabled/
sudo service nginx restart
docker-compose -f ${repo}/docker-compose.yml up -d
