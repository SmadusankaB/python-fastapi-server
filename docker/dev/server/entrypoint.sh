#!/bin/bash

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

mongo_ready() {
python << END
import sys
import motor.motor_asyncio
import os
import asyncio
import logging

async def check_db():
    dbname = os.environ['DATABASE_NAME']
    user = os.environ['DATABASE_USER']
    password = os.environ['DATABASE_PASSWORD']
    host = os.environ['DATABASE_HOST']
    port = os.environ['DATABASE_PORT']
    logging.debug(f"db: {dbname}")
    logging.debug(f"user: {user}")
    logging.debug(f"host: {host}")
    logging.debug(f"port: {port}")
    
    try:
        logging.info("Check mongo")
        MONGO_CONNECTION_STRING = f"mongodb://{host}:{int(port)}"
        if user and password :
            MONGO_CONNECTION_STRING: str = f'mongodb://{user}:{password}@{host}:{int(port)}'

        db_instance = motor.motor_asyncio.AsyncIOMotorClient(
              MONGO_CONNECTION_STRING
          )

        data = await db_instance.server_info()

    except Exception as err:
        logging.error(f"DB error - {err}")
        sys.exit(-1)
    
    logging.info("Mongo running")
    sys.exit(0)

asyncio.run(check_db())

END
}
until mongo_ready; do
  >&2 echo 'Waiting for Mongo to become available...'
  sleep 1
done
>&2 echo 'Mongo is available'

rabbitmq_ready() {
    echo "Waiting for rabbitmq..."

    while ! nc -z ${RABBITMQ_HOST} ${RABBITMQ_PORT}; do
      sleep 1
    done

    echo "rabbitmq started"
}

rabbitmq_ready

exec "$@"
