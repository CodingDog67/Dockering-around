# Dockering around

Indept tutorial with commented sample codes on how to use docker 

## 1) Images and containers

   Understanding Images and Containers, how to run/start/stop/remove/attached/detach
   
    1-nodejs-example
    1-python-rng
    1- Exercise
   
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

re-tagging images by 
**docker tag old_name:tag new_name**
creates clone of old images with new name but will not delete old image

### Pushing docker images on docker hub
1) Log into docker hub and create a repo there, repo = images
2) Rename image to repo name 
3) Log in to docker as admin of the repo 
4) Use the provided push command on docker hub locally


To pull simple go **docker pull name** will always pull the latest image of this repo, can also do docker run if the image isnt there locally docker will check on docker hub


## 2) Data Management and Volumes

    Learning how to create Volume and manage data and data survival 

    2-data-volumes-feedback-app

Images are read only (Code + Environment), not changeable once built \
Temp app data (user input) is stored in containers with read/write access. Dynamic, changing and cleared regularly \
Permanent App data (User accounts eg)fetched/produced in running container, store in files/database/ most not be lost if 
container stops/restarts, read/write, stored with container + volumes

Check Data_volumes_feedback_app to see an example \
Problem if container is removed, all created data in the container is lost, using volumes structures for this problem. 
Volumes = folders on the host machine which are mounted (made available) into containers  /some_path(host) -> /app/user_data
Connect a folder outside the container with a folder inside, changes are made to either a reflected in both. Volumes but only named, persist if a container is shut down.

See the volumes: 

    docker volume ls

Create a named volume during first-time running a container : \

    docker run -d -p 3000:80 --rm --name feedback-app -v saved_feedback:/app/feedback feedback

Removing Anonymous Volumes: \

    docker volume rm VOL_NAME** or **docker volume prune
