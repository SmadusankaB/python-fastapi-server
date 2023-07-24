import motor.motor_asyncio
from server.config import settings
from beanie import init_beanie
from server.jobs.models import Celery_Taskmeta
import logging
import sys
from pymongo.errors import OperationFailure

logger = logging.getLogger(settings.LOGGER_NAME)


async def connect_db():
    """
    Connect to database, validate connection and initialize beanie with models

    Returns
    -------
    is_correct_file: AsyncIOMotorClient
        Return AsyncIOMotorClient instance
    """
    try:
        logger.info("Connecting to db")
        db_instance = motor.motor_asyncio.AsyncIOMotorClient(
            settings.MONGO_CONNECTION_STRING
        )

        # check auth
        data = await db_instance.server_info()

        logger.debug(f"DB info {data}")
        logger.info("Connected to DB")
        await initialize_beanie(db_instance)
        return db_instance

    except OperationFailure as e:
        logger.error(f"Exception: {e}")
        sys.exit(-1)
    except Exception as e:
        logger.error(f"Exception: {e}")
        sys.exit(-1)


# Initialize beanie with document classes and a database
async def initialize_beanie(db_instance):
    """
    Initialize beanie with models

     Parameter
     ---------
     db_instance: AsyncIOMotorClient
         AsyncIOMotorClient client object needs to be passed with db
    """
    logger.debug(f"Database {settings.DATABASE_NAME}")
    logger.info("Initialize beanie")

    # init_beanie
    await init_beanie(
        database=db_instance[settings.DATABASE_NAME],
        document_models=[Celery_Taskmeta],
    )
    logger.info("Beanie Initialized successfully ")
