docker build -t llm-service .

docker stop llm-service

docker rm llm-service

docker run -d --name llm-service -p 8001:8001 --network argy-network llm-service