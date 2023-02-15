# Dockering around

Indept tutorial with commented sample codes on how to use docker 

## 1) Images and containers

   Understanding Images and Containers, how to run/start/stop/remove/attached/detach
   
    1-nodejs-example
    1-python-rng
   
### Deleting images and containers 

Listing images by **docker images**, and containers by **docker ps** 

Either run a docker **rm all_the_container_names** you want to remove found via docker ps -a. \
Similarly **docker rmi** removes images by img id, but only if no (even stopped) container is based on that image anymore

**docker image prune** removes all unused images

**docker --rm run image_name** add the --rm flag in the run command will remove as soon as container is stopped

### Tagging/naming images/containers 
**docker image inspect img_id** to get metadata 

name container by: \
**docker run --name own_name img_id**
e.g docker run -p 3000:80 -d --rm --name kiki_goals 568dceade80f   see docker run --help for clarification of -d and --rm

name images by: \
**docker build -t goals:latest_kiki .** 
name : tag principle, name defines a group of possible mor specialized images e.g python, tag defines a specialized image within group of images e.g python version \
New containers can be run by defining the tag instead of image ID

