#smaller node image
FROM node:14-alpine 

WORKDIR /app

#similar to CMD but if a command after docker run is added e.g npm install is appended instead of overwritten
#so in the run command we only need to specify init instead of npm init, or install express = installing the express dependency --> pacakge-lock.json --save
ENTRYPOINT [ "npm" ]