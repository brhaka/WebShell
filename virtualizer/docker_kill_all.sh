docker ps -q | xargs -r docker kill
docker system prune -a