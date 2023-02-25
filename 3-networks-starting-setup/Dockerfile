FROM node

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

CMD ["node", "app.js"]

# note that this container only contains the node app and all the code that belongs to it but not the mongo db database
