# this frontend setup depends on node but it is not a node application
FROM node

#this wont class with backend since it is a different container
WORKDIR /app

COPY package.json .

RUN npm install

COPY . . 

# by default 3000
EXPOSE 3000

# running react start script as seen in package.json, boot up development server to host react app during development
CMD ["npm", "start"]