import os

from stdimage.utils import render_variations
from tests.models import ManualVariationsModel


class TestRenderVariations(object):
    def test_render_variations(self, image_upload_file):
        ManualVariationsModel.objects.all().delete()
        instance = ManualVariationsModel.objects.create(
            image=image_upload_file
        )
        path = instance.image.thumbnail.path
        assert not os.path.exists(path)
        render_variations(
            app_label='tests',
            model_name='manualvariationsmodel',
            field_name='image',
            file_name=instance.image.name
        )
        assert os.path.exists(path)
