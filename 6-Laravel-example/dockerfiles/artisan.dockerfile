FROM php:8-fpm-alpine

#standard folder on webservers to serve your website from, will use this for folder which should hold final application
WORKDIR /var/www/html

#php extensions we need
RUN docker-php-ext-install pdo pdo_mysql
