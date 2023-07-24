"""Test celery tasks."""

import pytest
from server.jobs.tasks import demension_image


def test_demension_image():
    """Test for demension_image """
    task = demension_image.apply(args=("tests/test_data/sample1.png",)).get()
    # result of demension_image is image path it self
    assert task, "tests/test_data/sample1.png"

def test_invalid_path():
    """Test for invalid file path """
    try:
        task = demension_image.apply(args=("tests/test_data/sample2.png",)).get()
    except Exception as exc:
        assert f"{exc}", "[Errno 2] No such file or directory: 'tests/test_data/sample2.png'"
        
        
    

        