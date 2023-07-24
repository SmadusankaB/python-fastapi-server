from server.config import settings
from server.jobs.models import Celery_Taskmeta
from server.jobs import tasks
from PIL import Image
from celery import current_app as current_celery_app
from celery.result import AsyncResult
from fastapi import HTTPException
from server.exception import CustomException
import logging
import os
import time

logger = logging.getLogger(settings.LOGGER_NAME)


class JobService:
    """
    A class used to represent a JobService
    """

    async def find_jobs(self):
        """
        Find all jobs in db, process result and send
        """
        try:
            res = await Celery_Taskmeta.find({}).to_list()
            if not res:
                raise CustomException(
                    status_code=404, message="Jobs not found"
                )
            logger.info("Jobs found")
            return res
        except CustomException as e:
            logger.error(f"CustomException: {e}")
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            logger.error(f"Exception: {e}")
            raise HTTPException(status_code=500, detail="Server Error")

    async def find_job_status(self, job_id):
        """
        Find specific job in db by job id, process result and send.
        job_id: str
            Id of job to query db
        """
        try:
            logger.info("Find job status by job id")
            job = AsyncResult(job_id, app=current_celery_app)
            if not job:
                raise CustomException(
                    status_code=400, message=f"Result not found for {job_id}"
                )
            state = job.state
            if not state:
                raise CustomException(
                    status_code=400, message=f"Invalid Job status for {job_id}"
                )
            logger.info(f"Job status for {job_id} {state}")

            # To ensure that resources are released, you must eventually call get() or forget()
            # on EVERY AsyncResult instance returned after calling a task.
            # job.forget()

            # TODO: find and send most accurate state
            # if state == 'PENDING':
            # inspector = current_celery_app.control.inspect()
            # r = inspector.query_task(job_id)
            # scheduled = list(inspector.scheduled().values())[0]
            # active = list(inspector.active().values())[0]
            # reserved = list(inspector.reserved().values())[0]
            # #registered = list(inspector.registered().values())[0]
            # lst = [*scheduled, *active, *reserved]
            # for i in lst:
            #   if i['id'] == job_id:
            #     return {"status": state}
            # raise CustomException(status_code=400, message="Invalid job id")
            # return {"status": f"{state} or invalid job id"}
            return {"status": state}
        except CustomException as e:
            logger.error(f"CustomException: {e}")
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            logger.error(f"Exception: {e}")
            raise HTTPException(status_code=500, detail="Server Error")

    async def upload_image(self, fileb):
        """
        Validate image file comming through request and store it in the server.
        If image is successfully stored, trigger the celery task to be run in background.

        Parameter
        ---------
        fileb: binary
            Image file that needs to converted to thumbnail

        Returns
        -------
        job_id: str
            Id of celery job
        """
        try:
            logger.info("Uploading image")

            if not fileb:
                raise CustomException(
                    status_code=400, message="Invalid file input"
                )

            img_file = fileb.file
            img_name = fileb.filename

            if not img_file:
                raise CustomException(
                    status_code=400, message="Invalid file input"
                )

            if not img_name:
                raise CustomException(
                    status_code=400, message="Invalid file input"
                )
            logger.info(f"Image file name {img_name}")

            # Check whether image file is valid or not
            if allowed_file(img_name):
                logger.debug(f"Upload destination {settings.UPLOADS_DEST}")
                is_exist = os.path.exists(settings.UPLOADS_DEST)
                logger.info(f"Destination exist {is_exist}")

                if not is_exist:
                    os.makedirs(settings.UPLOADS_DEST)
                    logger.info("The new directory is created!")

                timestr = time.strftime("%Y%m%d_%H%M%S")
                path = f"{settings.UPLOADS_DEST}/{timestr}_{img_name}"
                logger.debug(f"Image path {path}")
                img_PIL = Image.open(img_file)
                img_PIL.save(path)

                is_file_exist = os.path.exists(path)
                logger.debug(f"Image file exist {is_file_exist}")
                if not is_file_exist:
                    raise Exception("Image upload failed")

                job = tasks.demension_image.delay(path)
                logger.info("Celery Job submitted successfully")
                logger.info(f"Job info {job}")
                return {"job_id": job.id}

        except CustomException as e:
            logger.error(f"CustomException: {e}")
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            logger.error(f"Exception: {e}")
            raise HTTPException(status_code=500, detail="Server Error")

    async def find_image(self, job_id):
        """
        Find celery task by task id and return image file path.

        Parameter
        ---------
        job_id: str
            Id of job to query db

        Returns
        -------
        path: str
            File path of the thumbnail
        """

        try:
            logger.info("Find thumbnail by job id")
            res = await Celery_Taskmeta.get(job_id)
            logger.debug(f"Job result {res}")
            if not res:
                raise CustomException(
                    status_code=400,
                    message="Invalid job id or job still pending",
                )

            # backword slash course errors
            img_name = res.result.replace('"', "")
            logger.debug(f"Thumbnail name {img_name}")
            path = f"{settings.UPLOADS_DEST}/{img_name}"
            is_exist = os.path.exists(path)
            logger.info(f"Valid thumbnail path {is_exist}")

            if not is_exist:
                raise CustomException(
                    status_code=404, message="Image not found"
                )
            return path

        except CustomException as e:
            logger.error(f"CustomException: {e}")
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            logger.error(f"Exception: {e}")
            raise HTTPException(status_code=500, detail="Server Error")


def allowed_file(filename):
    """
    Validate image file by file extension

    Parameter
    ---------
    filename: str
        Name of the image file

    Returns
    -------
    is_correct_file: bool
        Return True if image is valid, otherwise False
    """
    logger.info(f"Allowed file extensions {settings.ALLOWED_EXTENSIONS}")
    is_correct_file = (
        "." in filename
        and filename.rsplit(".", 1)[1] in settings.ALLOWED_EXTENSIONS
    )
    if not is_correct_file:
        raise CustomException(status_code=400, message="Invalid file input")
    logger.info(f"Valid file {is_correct_file}")
    return is_correct_file
