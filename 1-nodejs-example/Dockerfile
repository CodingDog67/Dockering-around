# from blah blah needs to be a local image on on docker hub, cached locally after first time dl
FROM node

WORKDIR /app

#copy this seperate from serve js to unsure changes in server do not need to re-run npm install, needed for npm install 
COPY package.json /app 

#if not told run will run ino root folder, therefore workdir
RUN npm install 

# specify two paths, all folder, subfolders should be copied into image first dot, second path inside image 
# where it should be stored, will be created and will contain all folders/subfolders == copy all fiels into image
# with workdir = /app, copy . ./ would work as well
COPY . /app

#docker container is isolated = own internal network, therefor expose 
#declares intention to expose, but expose is done with -p during run command
EXPOSE 80

#run container based on image therefore dont want to run this everytime image is created
#should always be last command in docker file
CMD ["node", "server.js"]


#notes:
# images are layer based = when rebuild image only instructions where something changes and instructions after are re-evaluated
# each instruction is a layer 


# docker run -p 3000:80 id e.g (initial container start can interact with, output shown)  ATTACHED listening to the output -d will detach
# docker start (restart container/ detached) DETACHED or -a will attach
# docker attach running_container_name will attach
# docker logs running_container_name is an option too 

