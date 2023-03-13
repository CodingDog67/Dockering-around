#By adding this docker file we ensure we always copy a snapshot of the config and the source code into the image and wont rely on solely the bind mount
# e.g for deployment where there won't be bind mounts

FROM nginx:stable-alpine

WORKDIR /etc/nginx/conf.d

COPY nginx/nginx.conf .

#no need to specify workdir for nginx.conf as that has been set above, renames this to default.conf
RUN mv nginx.conf default.conf

WORKDIR /var/www/html

COPY src . 

