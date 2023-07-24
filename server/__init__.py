from fastapi import FastAPI
from logging.config import dictConfig
import logging
from server.config import settings
from beanie import init_beanie
from server.jobs.models import Celery_Taskmeta


def create_app() -> FastAPI:
    
    from server.log import LogConfig
    dictConfig(LogConfig().dict())
    logger = logging.getLogger(settings.LOGGER_NAME)
    logger.info("Logger initialized")

    app = FastAPI(
        title="Thumbnail Generator (TG)",
        description="FastAPI server to generate image thumbnails",
        version="1.0.0",
    )
    logger.info("App initialized")

    @app.on_event("startup")
    async def startup():
        from server.db import connect_db

        app.db = await connect_db()

    @app.on_event("shutdown")
    async def shutdown():
        app.db.closes()

    from server.jobs import jobs_router

    app.include_router(jobs_router)
    logger.info("Routes configured")

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app
