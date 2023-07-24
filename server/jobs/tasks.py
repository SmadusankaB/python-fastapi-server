from PIL import Image
from server.celery import celery_app
from server.config import settings
from celery.exceptions import CeleryError, CeleryWarning
import logging
import os

logger = logging.getLogger(settings.LOGGER_NAME)


thumb_size = (100, 100)


@celery_app.task(bind=True)
def demension_image(self, img_path):
    """
    Task function to create thumbnail images with celery worker

    Parameter
    ---------
    self: task object
        Able to perform task operations
    img_path: str
        Image file path in server

    Returns
    -------
    img_path: str
        Thumbnail file path in server
    """
    try:
        logger.info("Generating thumbnail")
        logger.debug(f"Thumbnail size {thumb_size}")
        # time.sleep(20) # remove this
        with Image.open(img_path) as img:
            img.thumbnail(thumb_size)
            img.save(img_path)
            logger.debug(f"Thumbnail path {img_path}")
            is_file_exist = os.path.exists(img_path)
            logger.info(f"Thumbnail exist {is_file_exist}")
            if not is_file_exist:
                raise Exception("Thumbnail creation failed")
            logger.info("Thumbnail created successfully")
            image_name = os.path.basename(img_path)
            logger.info(f"Thumbnail name {image_name}")
            return image_name
    except CeleryError as e:
        logger.error(f"CeleryError: {e}")
        raise self.retry(countdown=10, exc=e)
    except CeleryWarning as w:
        logger.error(f"CeleryWarning: {w}")
    except Exception as e:
        logger.error(f"Exception: {e}")
        raise self.retry(countdown=10, exc=e)
