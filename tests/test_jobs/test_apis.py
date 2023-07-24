"""Test job apis."""
from server.main import app
from server.jobs.service import JobService
from httpx import AsyncClient
import pytest
from mongomock_motor import AsyncMongoMockClient
from beanie import init_beanie
from server.jobs.models import Celery_Taskmeta
from fastapi import HTTPException
from beanie import Document
from beanie.odm.queries.cursor import BaseCursorQuery
import celery
from pydantic import Field



#  Test cases 
#  API: "/jobs"
#  Function: get_jobs

@pytest.mark.anyio
async def test_get_jobs(monkeypatch):
    """
    Validate successfull response on get all jobs from the db
    """
    async def mock_find_jobs(JobService):
      return [{"_id": "some_id", "status": "SUCCESS", "result": "/path/image.png"}]
    monkeypatch.setattr(JobService, "find_jobs", mock_find_jobs)
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        client = AsyncMongoMockClient()
        await init_beanie(document_models=[Celery_Taskmeta], database=client.get_database(name="db"))
        response = await ac.get("/jobs")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_jobs_404(monkeypatch):
    """
    Validate jobs not found 
    """
    async def mock_find(BaseCursorQuery):
          return []
    monkeypatch.setattr(BaseCursorQuery, "to_list", mock_find)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        client = AsyncMongoMockClient()
        await init_beanie(document_models=[Celery_Taskmeta], database=client.get_database(name="db"))
        response = await ac.get("/jobs")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Jobs not found'}


@pytest.mark.anyio
async def test_get_jobs_500(caplog, monkeypatch):
    """
    Validate exceptions
    """
    async def mock_find(BaseCursorQuery):
          raise Exception("Some exception happened")
    monkeypatch.setattr(BaseCursorQuery, "to_list", mock_find)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        client = AsyncMongoMockClient()
        await init_beanie(document_models=[Celery_Taskmeta], database=client.get_database(name="db"))
        response = await ac.get("/jobs")
    assert response.status_code == 500
    assert response.json() == {'detail': 'Server Error'}
    assert "Exception: Some exception happened" in caplog.text

    
#  Test cases 
#  API: "/jobs/{job_id}"
#  Function: get_jobs_status

@pytest.mark.anyio
async def test_get_jobs_status(monkeypatch):
    """
    Validate successfull response on get job by id from celery AsyncResult
    """
    async def mock_find_job_status(JobService, job_id):
      return {"status": "SUCCESS"}
    monkeypatch.setattr(JobService, "find_job_status", mock_find_job_status)
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        client = AsyncMongoMockClient()
        await init_beanie(document_models=[Celery_Taskmeta], database=client.get_database(name="db"))
        response = await ac.get("/jobs/simple_id")
    
    assert response.status_code == 200
    assert response.json() == {'status': 'SUCCESS'}

# TODO: complete test case
# @pytest.mark.anyio
# async def test_get_jobs_status_500(caplog, monkeypatch):
#     """
#     Validate AsyncResult
#     """
#     class MockAsyncResult():
#         def __init__(self):
#           self.id =  "simple_job_id"
#         def get(self):
#             return self.id

#     monkeypatch.setattr("celery.result.AsyncResult", lambda x: MockAsyncResult())
    
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get("/jobs/simple_id")
#     assert response.status_code == 200
  

#  Test cases 
#  API: "/image"
#  Function: post_image

@pytest.mark.anyio
async def test_post_image(monkeypatch):
    """
    Validate successfull image upload
    """
    class MockAsyncResult():
        def __init__(self):
          self.id =  "simple_job_id"
        def get(self):
            return self.id
    monkeypatch.setattr("server.jobs.tasks.demension_image.delay", lambda x: MockAsyncResult())
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        with open("tests/test_data/sample1.png", "rb") as f:
            response = await ac.post("/jobs/image", files={"fileb": ("sample1.png", f, "image/*")})

    assert response.status_code == 200
    assert response.json() == {"job_id": "simple_job_id"}

@pytest.mark.anyio
async def test_invalid_file_type(monkeypatch):
    """
    Validate invalid file type with txt file
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        with open("tests/test_data/sample.txt", "rb") as f:
            response = await ac.post("/jobs/image", files={"fileb": ("filename.txt", f, "image/*")})

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file input"}


@pytest.mark.anyio
async def test_post_image_500(monkeypatch):
    """
    Exception on read task result
    """
    class MockAsyncResult():
        def __init__(self):
          self.id =  "simple_job_id"
          raise Exception("Some Exception")
        def get(self):
            return self.id
    monkeypatch.setattr("server.jobs.tasks.demension_image.delay", lambda x: MockAsyncResult())
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        with open("tests/test_data/sample1.png", "rb") as f:
            response = await ac.post("/jobs/image", files={"fileb": ("sample1.png", f, "image/*")})

    assert response.status_code == 500
    assert response.json() == {'detail': 'Server Error'}


#  Test cases 
#  API: "/image/{job_id}"
#  Function: get_image

@pytest.mark.anyio
async def test_get_image(monkeypatch):
    """
    Validate get image by job id
    """
    async def mock_find_image(JobService, job_id):
      return "tests/test_data/sample1.png"
    monkeypatch.setattr(JobService, "find_image", mock_find_image)
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        client = AsyncMongoMockClient()
        await init_beanie(document_models=[Celery_Taskmeta], database=client.get_database(name="db"))
        response = await ac.get("/jobs/image/simple_id")

    assert response.status_code == 200

  
@pytest.mark.anyio
async def test_invalid_image_path(monkeypatch):
    """
    Validate invalid image file path
    (Invalid result from db)
    """
    async def mock_get(Celery_Taskmeta):
        class Dict2Class(object):
          def __init__(self, my_dict):
              for key in my_dict:
                  setattr(self, key, my_dict[key])
        dct = {
          "_id": "356ad650-39c6-43d1-bfe2-7a1e140193ed",
          "status": "SUCCESS",
          "result": "\"/invalid/path.png\""
        }
        return Dict2Class(dct)
        
    monkeypatch.setattr(Celery_Taskmeta, "get", mock_get)
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        client = AsyncMongoMockClient()
        await init_beanie(document_models=[Celery_Taskmeta], database=client.get_database(name="db"))
        response = await ac.get("/jobs/image/simple_id")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Image not found'}


@pytest.mark.anyio
async def test_invalid_get_job_id(monkeypatch):
    """
    Validate invalid job id
    """
    async def mock_get(Celery_Taskmeta):
      return {}
    monkeypatch.setattr(Celery_Taskmeta, "get", mock_get)
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        client = AsyncMongoMockClient()
        await init_beanie(document_models=[Celery_Taskmeta], database=client.get_database(name="db"))
        response = await ac.get("/jobs/image/simple_id")

    assert response.status_code == 400
    assert response.json() == {'detail': 'Invalid job id or job still pending'}
