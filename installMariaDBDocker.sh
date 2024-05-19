#!/bin/bash
docker pull mariadb
docker run -d \
  --name mariadb \
  -e MYSQL_ROOT_PASSWORD=changeme \
  -e MYSQL_DATABASE=projectdb447 \
  -e MYSQL_USER=projectuser \
  -e MYSQL_PASSWORD=changeme \
  -p 3306:3306 \
  mariadb