sudo docker build -t cloud .
sudo docker run -d -p 8001:8001 --name cloud_app cloud