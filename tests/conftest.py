import io
import os

import pytest
from django import conf
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


def pytest_configure():
    os.environ[conf.ENVIRONMENT_VARIABLE] = "tests.settings"

    try:
        import django
        django.setup()
    except AttributeError:
        pass

    from django.test.utils import setup_test_environment

    setup_test_environment()

    from django.db import connection

    connection.creation.create_test_db()


@pytest.fixture
def imagedata():
    img = Image.new('RGB', (250, 250), (255, 55, 255))

    output = io.BytesIO()
    img.save(output, format='JPEG')

    return output


@pytest.fixture
def image_upload_file(imagedata):
    return SimpleUploadedFile(
        'testfile.jpg',
        imagedata.getvalue()
    )
