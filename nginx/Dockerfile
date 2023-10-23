FROM nginx:1.25.2

WORKDIR /home/project/

RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
