# Dockering around

Indept tutorial with commented sample codes on how to use docker 

## 1) Images and containers

   Understanding Images and Containers, how to run/start/stop/remove/attached/detach
   
    1-nodejs-example
    1-python-rng
   
### Deleting images and containers 

Listing images by **docker images**, and containers by **docker ps** 
#### Deleting containers /images

Either run a docker **rm all_the_container_names** you want to remove found via docker ps -a. \
Similarly **docker rmi** removes images by img id, but only if no (even stopped) container is based on that image anymore

**docker image prune** removes all unused images

**docker --rm run container_name** add the --rm flag in the run command will remove as soon as container is stopped
