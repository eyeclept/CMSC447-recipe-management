#!/bin/bash
#setup flaks docker
cd ./flaskapp
docker build -t flask:latest .
cd ..
#setup react docker
cd ./reactapp
docker build -t react:latest .
cd ..
#launch docker
docker-compose up
#pull stuff for flask
docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-reset-password -b -u elastic
docker cp elasticsearch:/usr/share/elasticsearch/config/certs/http_ca.crt .