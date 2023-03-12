FROM php:7.4-fpm-alpine

#standard folder on webservers to serve your website from, will use this for folder which should hold final application
WORKDIR /var/www/html

#php extensions we need
RUN docker-php-ext-install pdo pdo_mysql

#no command on entrypoint here, command/entry point of base img will be used == php base img here we will incoke php interpreter