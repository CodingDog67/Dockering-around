FROM node

WORKDIR /app

#copy this seperate from serve js to unsure changes in server do not need to re-run npm install, needed for npm install 
COPY package.json /app 

RUN npm install

COPY . /app

EXPOSE 80

CMD ["node", "server.js"]


#notes:
# images are layer based = when rebuild image only instructions where something changes and instructions after are re-evaluated
# each instruction is a layer 


# docker run -p 3000:80 id e.g (initial container start can interact with, output shown)  ATTACHED listening to the output -d will detach
# docker start (restart container/ detached) DETACHED or -a will attach
# docker attach running_container_name will attach
# docker logs running_container_name is an option too 

