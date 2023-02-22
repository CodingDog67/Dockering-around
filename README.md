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


## 2) Data Management, Volumes and Bind Mounts

    Learning how to create Volume and manage data and data survival 

    2-data-volumes-feedback-app

Images are read only (Code + Environment), not changeable once built \
Temp app data (user input) is stored in containers with read/write access. Dynamic, changing and cleared regularly \
Permanent App data (User accounts eg)fetched/produced in running container, store in files/database/ most not be lost if 
container stops/restarts, read/write, stored with container + volumes

### Volumes
Managed by Docker, used fot persistent data one does not need to edit directly, e.g user accounts, feedback text etc

Check Data_volumes_feedback_app to see an example for volumes \
Problem if container is removed, all created data in the container is lost, using volumes structures for this problem. 

Volumes = folders on the host machine which are mounted (made available) into containers  /some_path(host) -> /app/user_data
Connect a folder outside the container with a folder inside, changes are made to either a reflected in both. Volumes but only named, persist if a container is shut down.

See the volumes: 

    docker volume ls

Create an anonymous volume: \

    docker run -v /app/data or inside the dockerfile via VOLUME

Create a named volume during first-time running a container: \

    docker run -v data:/app/data

Create a Bind Mount: \

    docker run -v /path/to/code:/app/code

Removing Anonymous Volumes: \

    docker volume rm VOL_NAME** or **docker volume prune

### Bind Mounts
Managed by yourself = you define folder/path on host machine \
Used for presistent/editable data e.g source code

Create a bind mount during via run container command: \

    docker run -d -p 3000:80 --rm --name feedback-app  -v feedback:/app/feedback -v "absolute_path_to_project_folder:/app" -v /app/node_modules image_name( this is created by npm install)

    shortcut: -v "%cd%":/app

First **-v feedback:/app/feedback** will create a named volume managed by docker for the feedback files. If we omit this we get copies on our local machine as well in the original app/path but this is not desired since we dont want to manage them by ourselves

Second **-v "absolute_path_to_project_folder:/app"** This will override everything in the container app folder with the local machine folder. We use it to sync the code in real time e.g when we change the feedback.html and reload we see the change immediately. But that also means everything in the docker file e.g run npm install is rendered useless.

Third **-v /app/node_modules image_name** To counter the effect of the bind mount previously mentioned, have an anonymous volume running in parallel, longer path wins and gets priority. This will ensure that the npm install content stays alive. 


### Side notes
Code changes to the .js file are not reflected in real time, due to a nodejs specific problem, visit **server.js** and **package.json** to see. In short use a package which watches the file system and restarts the node server whenever sth changes. Add to jsonfile: 

     "devDependencies": {"nodemon":"2.0.20" } 