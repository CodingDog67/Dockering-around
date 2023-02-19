FROM node

WORKDIR /app 

COPY package.json .

RUN npm install

COPY . .

EXPOSE 80

# VOLUME ["folder inside container"] Anynomous volume, no idea where the data is on host machine (which is intentinally since we
# should not mess with the data ourselved), managed by docker
# only exists as long as our container exists.
## VOLUME ["/app/feedback"] <-- command   

#Named volumed created during run command

#Docker command to see the volumes is "docker volume ls"


CMD ["node","server.js"]