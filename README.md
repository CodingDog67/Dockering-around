# Dockering around

Indept tutorial with commented sample codes on how to use docker 

## 1) Images and containers
Understanding Images and Containers, how to run/start/stop/remove/attached/detach

    1-nodejs-example
    1-python-rng
    1- Exercise

<details>
     <summary>Expand</summary>

 

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

</details>

## 2) Data Management, Volumes and Bind Mounts
Learning how to create Volume and manage data and data survival 

    2-data-volumes-feedback-app

<details>
     <summary>Expand</summary>
     
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

   Third **-v /app/node_modules image_name** To counter the effect of the bind mount previously mentioned, have an anonymous volume running in parallel, longer path wins and gets priority. This will ensure that the npm install content stays alive. But this must be specified in the docker run command not the docker file itself then.
  

   ### Side notes
   Code changes to the .js file are not reflected in real time, due to a nodejs specific problem, visit **server.js** and **package.json** to see. In short use a package which watches the file system and restarts the node server whenever sth changes. Add to jsonfile: 

        "devDependencies": {"nodemon":"2.0.20" } 

   Read-only mode by adding :ro, eg docker run -v /path/to/code:/app/code:ro \
   For example for source code, container should not be able to write and change the code. But make sure to exclude all folders that should be changed by the container during run time. Good practice to clarify things. watch the oder :ro needs to be last of all declared volumes. E.g

    docker run -d --rm -p 3000:80 --name feedback-app -v feedback:/app/feedback -v /app/node_modules -v /app/temp -v "path/to/codebase:/app:ro" volumes:latest

   Inspect via **docker volume inspect VOLUME_NAME**

   Bind VS Copy \
   Keep in mind most of the volume command are called during a development process. Once the app is finished bind mounts wont be used and hence we still need the copy . . in the docker file

</details>

## 3) Networking 
Container communication to a service on host machine/the WWW/another container, or in short cross container communication.

    3-networks-starting-setup

For visualization of this example get postman and send a get request to localhost:3000/movies \
send a post request to localhost:3000/favorites choose json format, adding via raw body format {"name": , "type": , "url" :} \
Check via get request to favorites if it was saved correctly and voila good job

<details>
    <summary>Expand</summary>

### Three ways of communications 

WWW \
Requesting from inside a container to WWW will just work 

Local Machine \
Requesting to a local machine server needs a change in domain to be understood by docker. \
**local host** needs to be changed into **host.docker.internal** on the js.script, can be used anywhere where one needs a domain/url like mongodb or html etc etc

Container to Container \
In our example run an image / mongo from dockerhub in this case. For in depth go to docker hub and read the doc. \
Hard way, rebuild everytime to adjust to ip change and manual look up: \
**docker container inspect mongodb** to read out ip address of the container, and use that in the connect part of the js. script\

**Container Networks** for easier and multiple container to container communication. All containers in a docker network can talk to each other and docker will take care of IPs automacially, first create a network, then run containers with the network flag to put them inside the same network.
Container to container connection does not require any published port 

    docker network create mynetwork-net
    docker run --network my_network ...


Side notes: Network behavior can be set via --driver options, default here is bridge and makes the most sense in most cases, for more info look up more information about docker network drivers
</details>

## Multicontainers 
Building and running multicontainer apps

We base this on an application example app that takes customer goals, saves them and deletes them again if needed. Like a smal goal - to do list. 
It will run a back and front end and be based on a mongodb server

<details>
    <summary>Expand</summary>

    1) MongoDB Service dockerization\
    Run of the dockerhub mongodb image:latest will automatically pull the image and build the container. Optional - publish the port as long as backend isnt dockerized this node api will talk to database as if run on local machine

        docker run --name mongodb -d --rm -p 27017:27017 mongo 


    2)  Dockerize Backend app.js, refer to file

    3)

</details>


## Side Notes

**Dockerignore** in order to avoid copying everything. Add an .dockerignore file in the dockerfile folder
add anything that isnt required by your application to execute correctly

**ARGuments and ENVironment vars**
Runtime ENV vars, set in dockerfile or via --env on docker run \
Allows default value but will also allow changed during run command by adding a **--env PORT=8000**
or specify a .env file in the project folder + **--env-file ./.env** option in run command

Build-time ARG, set on docker build via --build-arg
Set in docker file via ARG, speficied or changed during build command via **--build-arg DEFAULT_PORT = 8000**
