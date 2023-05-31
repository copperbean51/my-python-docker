docker run -dit --name pyshell hoge-image
docker exec -it pyshell /bin/bash


docker system df
docker builder prune


## mount 
docker run -v /home/wlin/workspace/my-docker-py:/devel -it --name= pyimage:20230531 /bin/bash