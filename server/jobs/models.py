# coding: utf-8
from datetime import date, datetime  # noqa: F401
from bson import ObjectId
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import (
    BaseModel,
    Field,
)  # noqa: F401
from beanie import Document


class Response201(BaseModel):
    """
    Response201 - a model defined in OpenAPI
    message: The message of this Response201 [Optional].
    """

    job_id: Optional[str] = Field(alias="job_id", default=None)


Response201.update_forward_refs()


class ResponseError(BaseModel):
    """
    ResponseError - a model defined in OpenAPI
    message: The message of this ResponseError [Optional].
    """

    detail: Optional[str] = Field(alias="detail", default=None)


ResponseError.update_forward_refs()


class Celery_Taskmeta(Document):
    """
    Celery_Taskmeta - a model defined for mondodb
    Broken naming best practice here to support collection in db
    """

    id: str = Field(default_factory=str)
    status: str
    result: str

    class Settings:
        name = "celery_taskmeta"
        orm_mode = True

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "61d63596-c419-4cfd-b1ea-fe8e652c5587",
                "status": "SUCCESS",
                "result": "uploads/sample1.png",
            }
        }


class JobStatus(BaseModel):
    """
    JobStatus - a model defined in OpenAPI
    status: Status of the give job
    """

    status: str = Field(alias="status", default=None)


JobStatus.update_forward_refs()
