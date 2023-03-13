FROM php:8-fpm-alpine

#standard folder on webservers to serve your website from, will use this for folder which should hold final application
WORKDIR /var/www/html

#add a snapshot of code also here
COPY src .

#php extensions we need
RUN docker-php-ext-install pdo pdo_mysql

#no command on entrypoint here, command/entry point of base img will be used == php base img here we will incoke php interpreter

RUN addgroup -g 1000 laravel && adduser -G laravel -g laravel -s /bin/sh -D laravel
USER laravel

#command to change ownership and controlling who is allowed to read/write to folders, -R = recursive
RUN chown -R www-data:www-data /var/www/html