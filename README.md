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

<details>
    <summary>Expand</summary>

For visualization of this example get postman and send a get request to localhost:3000/movies \
send a post request to localhost:3000/favorites choose json format, adding via raw body format {"name": , "type": , "url" :} \
Check via get request to favorites if it was saved correctly and voila good job

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

## 4) Multicontainers 
Building and running multicontainer apps - development-only setup!

We base this on an application example app that takes customer goals, saves them and deletes them again if needed. Like a small goal - to do list. 
It will run a back and front end and be based on a mongodb server. End-goal is: \
- Each container communicating not through a locally published port 
- Database = Data must persist & limited Access
- Backend = Data persisting, live source code update
- Frontend = live source code update

        4-multi-container-app
    
<details>
    <summary>Expand</summary>

### Basic set-up
1) MongoDB Service dockerization 
Run of the dockerhub mongodb image:latest will automatically pull the image and build the container. Optional - publish the port as long as backend isnt dockerized this node api will talk to database as if run on local machine \
    
        no network: docker run --name mongodb -d --rm -p 27017:27017 mongo 

    
2)  Dockerize Backend  refer to docker file 

        no network: docker run --name goals-back --rm -d -p 80:80 backend_image_name

    
3) Dockerize Frontend, refer to docker file again, older version might need an -it interactive mode flag during run 

        no network: docker run --name react-goals -d --rm  -p 3000:3000 frontend-image_name

### Network optimization
Create a network and run all containers connected to the network w/o port publishing, only the frontend needs publishing because we want to ultimately interact with it on our local host machine. In order to have endpoints in frontend application reachable we need to publish port 80 on the backend application, so that that application is still available on local host, front-end needs to due to how react works. Frontend part that runs in container doesnt care about the network so no network addition necessary

        Docker network create goals-net

        Docker run --name mongodb --rm -d --network goals-net mongo

        Docker run --name goals-back --rm -d --network goals-net -p 80:80 backend_img_name

        Docker run --name goals-front --rm -d -p 3000:3000 -it frontend_img_name


### Volume addition 

**Database** \
If database is stopped, goals are deleted due to container removal. Data needs to be detached, refer to documentation to see that data is stored in :/data/db. Add named volume to secure data, and refer to documentation for authentication/security for limited access
(if version with volume is run before without credentials delete and restart)

        Docker run --name mongodb --rm -d --network goals-net -v data:/data/db -e MONGO_INITDB_ROOT_USERNAME=username -e MONGO_INITDB_ROOT_PASSWORD=secret mongo
    
**Backend**
Log files should persist via named volume in working dir(or bind depends on what you want) and live source code update via bind mount. 
Change app.js to restart server with every change by introducing nodemon, and running via start 

        Docker run --name goals-back --rm -d --network goals-net -p 80:80 -v logs:/app/logs -v "full_path:/app" -v /app/node_modules -e MONGODB_USERNAME=name -e MONGODB_PASSWORD=password backend_img_name

**Frontend**
We want live source code update via bind mount 

        Docker run --name goals-front --rm -d -p 3000:3000 -it -v "\full_path_to_src:/app/src" frontend 
</details>


## 5) Elegant Composing and using "Utility" Containers
Avoid running endlessly long docker run commands whenever a container is started, using docker compose. This chapter also has a sample project with everything learned so far included. Based on a Laravel & PHP framework. 

continued Example 
        4-multi-container-app 
        6-Laravel-example

<details>
    <summary>Expand</summary>

**Docker Compose**
It is one config file + orchestration commmands (build, start, stop) to run an application based on x-numbers of containers. Not suited to manage multiple containers on different hosts
Follows a strict keyword composition and set indentation rules/ docker extention for codes might be helpful.

- Two blanks indicates child parent relationship \
- Service children are containers and by default when using docker compose containers are removed upon stopping \
- Usually no network required because compose will automatically create a new environment for all services specified in compose file and will add them to said network. \

Run command is simply 
     docker-compose up -d

Stop and delete all containers and the default network, -v flag to also delete all volumes
    docker-compose down (-v)

Force a rebuild of images with
    docker-compose --build

All options with docker-compose up --help

**Utility Container**
Say we have the case that we need to create a json file, but npm init requires node to be installed, however the entire point of docker is that we dont need to have dependencies on our local machine. Node is an official image on docker though

    docker run -it -d node 

Docker exec command allows to run certain commands inside a running container besides default command. Override default command, which is executable with npm init. Note though that the project is created in the container to which we have no access. But we can create a dockerfile, assign a workdir and mirror that. 

    docker exec -it -v path_to_project:/app node_container_name npm init

Alternatively use a docker compose via run to run individual containers, be aware that containers are not automatically removed, add --rm

    docker-compose run/(exec) service_name command_of_our_choice \
    docker-compose run --rm npm init


**Laravel Example**
Quick look at laravel reveals that dependencies are a nightmare. Target setup: some host machine folder with source code. Three application containers. One PHP interpreter container to which Host machine folder is exposed. A Nginx web server container, connected to the PHP Interpreter. A MySQL database container is then exposed to the PHP Interpreter as well
Also we need 2 utility containers. A "composer" container (package manager), a "npm" container and a "Laravel Artisan" container. A total of 6 containers

Get the official command on laravel and tweak it, . = /var/www/html as root folder

    docker-compose run --rm composer create-project laravel/laravel .

Adjust the .env to use the selected usernames and password set in mysql.env in the ./env folder 
like so 
    DB_CONNECTION=mysql
    DB_HOST=mysql 
    DB_PORT=3306 
    DB_DATABASE=homestead 
    DB_USERNAME=homestead 
    DB_PASSWORD= 

Add these to the myself env 

    MYSQL_DATABASE=homestead 
    MYSQL_USER=homestead 
    MYSQL_PASSWORD 

run

    docker-compose up -d --build server

to test of initial set-up

run 

    docker-compose run --rm artisan migrate 

to test artisan. 

Refer heavily to the individual docker files and read the comments there to understand in-depth
</details>



## 6) Deployment 
This chapter will show how to use containers on remote machines/cloud/web 

    7-easy-node-deploy

<details>
    <summary>Expand</summary>

**Things to look out for**
- Dont use bind mounts in production
- Containerized apps might need a build step
- Multi-container projects might need to be split across multiple hosts/remote machines
- Trade-offs between control and responsibility (self managed remote host or managed)

Be aware of the many many docker hosting providers \
The three major ones are: aws, azure, google cloud

**Node Example - Manual Deployment**
1) Create and launch EC2 instance, go to aws and launch a linux AMI server. Create a Key pair and download the .pem file and move towards project folder


2) Connect via ssh or putty on windows, install docker and run container \

    https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html
    get the host name from starting the instance and looking at the ssh client tab 

Update all pacakges on remote machine, install docker and run it

    sudo yum update -y
    sudo amazon-linux-extras install docker
    sudo service docker start 

3) Bring the local image onto that remote machine \
    Option 1: Deploy source code, copy/push everything onto remote machine and build it there = Too complex! \
    Option 2: Build image ahead of time locally and deploy built image \

    Push image as learned earlier to dockerhub, remember docker tag can rename images
        
        docker push dockerhub_name/deploy_example_name

    On the remote machine run 

        sudo docker run -d --rm -p 80:80 dockerhub_name/deploy_example_name

4) Configure security group to explose all required ports to www \
Test it by first editing security group the instance belongs to, inbound rules to http from ssh. Run the IPv4 address of the instance in the browser and the node app should be visible

5) Update the app by building again, uploading and pulling the newest version which is cumbersome 

6) Manual because instance/configuration/connecting/installing Docker had to be done manually. Also since you fully own the remote machine you are responsible for its security, and have to keep essentials software updated/manage security/firewall. Also sshing into machine can be annoying

**Managed Service ECS**

Also use the 7-easy-node-deploy example to play around 

Creation, management, updating is done automatically so monitoring and scaling is simplified. But now one uses Docker + service by cloud provider, follow new rules of that service. Meaning deploying/running containers isnt done via docker commands anymore. Read up on tools cloud provider gives us for the service. 

1) Run the config wizard on custom container configuration and enter details. Port mapping only needs one number since container internal port is automatically mapped to same outside port

Compatability Fargate is a serverless launch mode, no real EC2 instance but instead store container and run settings, whenever there is request container is started up, request is handled and container is stopped again. This can be switched to EC2 mode. 

Load Balancer manages redirecting incoming requests, queue the up and running containers behind scenes, not needed right now. Every task is excecuted by a service

Cluster is the overall network in which our services run. For multicontainer app, one could group multiple containers in one cluster so they can talk to eachother and belong to eachother logically

Once Run we can check the public Ip under details and voila. For updates go to Task-definitions, and create a new revision, leave everything unchanged, create same task again and aws will pull again, select update service under actions (keeping all settings)

**Multicontainer-Deployment**
We wont use docker-compose for deployment, AWS or Azure need extra information which are not part of the Compose file, compose is great for managing and running multiple containers on the same machine but for cloud services with potentially multiple machines working together we hit the compose limit. 

We need to manually deploy the services. We cannot find container IP by container name feature so this has to be changed first in app.js. If containers are run in same task then they are guaranteed to run on the same machine, but ecs will not create a docker network but will allow to use localhost as address inside container 

Create an ECS cluster (surrounding network for containers thereafter). Create a running task and be sure to add "node,app.js" as command in environment since we do not need nodemon for live code updates anymore.

Also add all the environmental variables for mongodb such as username, password and url = localhost (feature from aws), but mongodb in development (docker feature)
For a second "service" go and add another container during task creation in ecs, in our case mongodb with port 27017 (default port) and also add the env vars MONGO_INITDB_ROOT_USERNA ME and MONGO_INITDB_ROOT_PASSWORD. 
Set up an application load balancer making sure you use the vpc of the service, IP as target group and port 80 then select it for the task creation. Unsures we have an unchanging domain

Task-creation: container name:port goals-backend:80:80 and choose a target group that is the same as the load balancer

Update ( in case of code changes) by visiting cluster/services -> select service -> update -> force new deployment -> skip to review -> update service

**EFS volumes**
Save non-persistent data e.g when we update code and update the service data is lost. Add volume at task definitions -> create new revision -> leave settings -> add volume -> EFS volume, elastic file system -> create new file system -> add vpc ( same as for ecs) costumize-> confirm first page, change network access add security group (create new add to vpc and add inbound rule, NFS source == goals security group) -> add mount point (newly created) to mongodb container click on name to open config and add mount point to new volume. Dont forget to create new task revision to update 

Watch if two mongodb container (update code) write at the same time to the same fiel system it clashes. Manually remove and stop currently running task, so to be deployed task can become active 
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

**Useful Docker Commands**
Stopping all containers
    docker stop $(docker ps -aq)

Removing all images
    docker image prune -a
    docker rmi $(docker images -q)