import os
import time

import pytest
from django.core.management import call_command

from tests.models import ManualVariationsModel, ThumbnailModel


@pytest.mark.django_db
class TestRenderVariations(object):
    def test_no_options(self, image_upload_file):
        obj = ManualVariationsModel.customer_manager.create(
            image=image_upload_file
        )
        file_path = obj.image.thumbnail.path
        call_command(
            'rendervariations',
            'tests.ManualVariationsModel.image'
        )
        assert os.path.exists(file_path)

    def test_multiprocessing(self, image_upload_file):
        file_names = [
            ManualVariationsModel.customer_manager.create(
                image=image_upload_file
            ).image.thumbnail.path
            for _ in range(100)
        ]
        assert not any([os.path.exists(f) for f in file_names])
        call_command(
            'rendervariations',
            'tests.ManualVariationsModel.image'
        )
        assert any([os.path.exists(f) for f in file_names])

    def test_no_replace(self, image_upload_file):
        obj = ThumbnailModel.objects.create(image=image_upload_file)
        file_path = obj.image.thumbnail.path
        assert os.path.exists(file_path)
        before = os.path.getmtime(file_path)
        time.sleep(1)
        call_command(
            'rendervariations',
            'tests.ThumbnailModel.image',
        )
        assert os.path.exists(file_path)
        after = os.path.getmtime(file_path)
        assert before == after

    def test_replace(self, image_upload_file):
        obj = ThumbnailModel.objects.create(image=image_upload_file)
        file_path = obj.image.thumbnail.path
        assert os.path.exists(file_path)
        before = os.path.getmtime(file_path)
        time.sleep(1)
        call_command(
            'rendervariations',
            'tests.ThumbnailModel.image',
            replace=True
        )
        assert os.path.exists(file_path)
        after = os.path.getmtime(file_path)
        assert before != after
