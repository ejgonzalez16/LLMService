#!/bin/bash

sudo docker build -t llm-service .

sudo docker stop llm-service

sudo docker rm llm-service

sudo docker run -d --name llm-service -p 8001:8001 --network argy-network llm-service

