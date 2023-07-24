# coding: utf-8

from fastapi.testclient import TestClient


from server.models.response201 import Response201  # noqa: F401


def test_get_ids(client: TestClient):
    """Test case for get_ids

    Read the list of process ids
    """

    headers = {
    }
    response = client.request(
        "GET",
        "/process",
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_image(client: TestClient):
    """Test case for get_image

    Read the status by process id
    """

    headers = {
    }
    response = client.request(
        "GET",
        "/image/{process_id}".format(process_id='process_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_status(client: TestClient):
    """Test case for get_status

    Read the status by process id
    """

    headers = {
    }
    response = client.request(
        "GET",
        "/process/{process_id}".format(process_id='process_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_process_image(client: TestClient):
    """Test case for process_image

    Post image
    """

    headers = {
    }
    data = {
        "file": '/path/to/file'
    }
    response = client.request(
        "POST",
        "/image",
        headers=headers,
        data=data,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

