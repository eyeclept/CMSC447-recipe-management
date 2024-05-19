#!/bin/bash
#setup flaks docker
cd ./flaskapp
docker build -t flask:latest .
cd ..
#setup react docker
cd ./reactapp
docker build -t react:latest .
cd ..
#launch docker compose
docker-compose up -d
#setup elastic
docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.4.3
sleep 5
docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-reset-password -b -u elastic | grep "New value:" | awk '{print $3}' > password.txt
docker cp elasticsearch:/usr/share/elasticsearch/config/certs/http_ca.crt ./ca.crt
mv password.txt sharedData
mv ca.crt sharedData

