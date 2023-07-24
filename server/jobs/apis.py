# coding: utf-8

from typing import Dict, List, Annotated  # noqa: F401
import logging
from server.config import settings
from fastapi import (  # noqa: F401
    Response,
    Path,
    status,
    File,
    UploadFile,
    Request,
    HTTPException,
)
from fastapi.responses import FileResponse
from . import jobs_router
from server.jobs.models import (
    Celery_Taskmeta,
    JobStatus,
    Response201,
    ResponseError,
)

from server.jobs.service import JobService

logger = logging.getLogger(settings.LOGGER_NAME)
job_service = JobService()


@jobs_router.get(
    "",
    responses={
        200: {
            "model": List[Celery_Taskmeta],
            "description": "Successfully read job id list",
        },
        404: {
            "model": ResponseError,
            "description": "Item could not be found",
        },
        400: {"model": ResponseError, "description": "Invalid request"},
        500: {
            "model": ResponseError,
            "description": "Internal servier error occurred",
        },
    },
    tags=["public"],
    summary="Get list of job ids",
    response_model_by_alias=True,
)
async def get_jobs() -> List[Celery_Taskmeta]:
    return await job_service.find_jobs()


@jobs_router.get(
    "/{job_id}",
    responses={
        200: {
            "model": JobStatus,
            "description": "Successfully read job status by job id",
        },
        404: {
            "model": ResponseError,
            "description": "Item could not be found",
        },
        400: {"model": ResponseError, "description": "Invalid request"},
        500: {
            "model": ResponseError,
            "description": "Internal servier error occurred",
        },
    },
    tags=["public"],
    summary="Get job status by job id",
    response_model_by_alias=True,
)
async def get_jobs_status(
    request: Request,
    job_id: str = Path(description="Job Id"),
) -> JobStatus:
    return await job_service.find_job_status(job_id)


@jobs_router.post(
    "/image",
    responses={
        201: {"model": Response201, "description": "If success"},
        400: {"model": ResponseError, "description": "Invalid Input"},
        500: {"model": ResponseError, "description": "Internal servier error"},
    },
    tags=["public"],
    summary="Post image to generate thumbnail",
    response_model_by_alias=True,
)
async def post_image(fileb: UploadFile = File(None)) -> Response201:
    """Submit image to generate thumbnail"""
    return await job_service.upload_image(fileb)


@jobs_router.get(
    "/image/{job_id}",
    responses={
        200: {
            "model": str,
            "description": "Successfully read status by job id",
        },
        404: {
            "model": ResponseError,
            "description": "Item could not be found",
        },
        400: {"model": ResponseError, "description": "Invalid request"},
        500: {
            "model": ResponseError,
            "description": "Internal servier error occurred",
        },
    },
    tags=["public"],
    summary="Get thumbnail image by job id",
    response_model_by_alias=True,
)
async def get_image(
    request: Request, job_id: str = Path(description="Id of the process")
) -> str:
    path = await job_service.find_image(job_id)
    return FileResponse(path)
