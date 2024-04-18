#!/bin/bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.4.3
docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.4.3
