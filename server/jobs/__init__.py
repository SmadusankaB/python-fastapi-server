from fastapi import APIRouter

jobs_router = APIRouter(
    prefix="/jobs",
)

# from . import views, models, tasks
from . import apis
