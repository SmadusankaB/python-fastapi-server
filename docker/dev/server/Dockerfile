FROM python:3.10-slim-buster

# ENV PYTHONUNBUFFERED 1
# ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Additional dependencies
  && apt-get install -y telnet netcat \
  && apt-get install -y procps \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# RUN addgroup --system fastapi \
#   && adduser --system --ingroup fastapi fastapi

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./docker/dev/server/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh
# RUN chown fastapi /entrypoint.sh

COPY ./docker/dev/server/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh
# RUN chown fastapi /start.sh

COPY ./docker/dev/worker/start.sh /start-celeryworker.sh
RUN sed -i 's/\r$//g' /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh
# RUN chown fastapi /start-celeryworker.sh

RUN mkdir /app
# RUN mkdir /app/uploads
# RUN chown fastapi /app/uploads
WORKDIR /app

# copy project code
COPY . .

# RUN chown -R fastapi:fastapi /app

# USER fastapi

ENTRYPOINT ["/entrypoint.sh"]
