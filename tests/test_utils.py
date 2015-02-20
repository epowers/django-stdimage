import os

from stdimage.utils import render_variations
from tests.models import ManualVariationsModel
from tests.test_models import IMG_DIR


class TestRenderVariations(object):
    def test_render_variations(self, image_upload_file):
        instance = ManualVariationsModel.objects.create(
            image=image_upload_file
        )
        path = os.path.join(IMG_DIR, 'image.thumbnail.jpg')
        assert not os.path.exists(path)
        render_variations(
            app_label='tests',
            model_name='manualvariationsmodel',
            field_name='image',
            file_name=instance.image.name
        )
        assert os.path.exists(path)
