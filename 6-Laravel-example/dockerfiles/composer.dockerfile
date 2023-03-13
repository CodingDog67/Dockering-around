FROM composer:latest

WORKDIR /var/www/html

# flag will ensure we run this even with some non vital dependencies are missing
ENTRYPOINT [ "composer", "--ignore-platform-reqs" ]

RUN addgroup -g 1000 laravel && adduser -G laravel -g laravel -s /bin/sh -D laravel
USER laravel