FROM nginx:1.23-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY ./docker/dev/nginx/nginx-entrypoint.sh /nginx-entrypoint.sh
RUN sed -i 's/\r$//g' /nginx-entrypoint.sh
RUN chmod +x /nginx-entrypoint.sh

ENTRYPOINT ["/nginx-entrypoint.sh"]


