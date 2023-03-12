FROM composer:latest

WORKDIR /var/www/html

# flag will ensure we run this even with some non vital dependencies are missing
ENTRYPOINT [ "composer", "--ignore-platform-reqs" ]