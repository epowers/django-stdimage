# -*- coding: utf-8 -*-
from __future__ import (absolute_import, unicode_literals)
import resource

from django.core.management import BaseCommand
from django.db.models.loading import get_model
from multiprocessing import Process
import progressbar

from stdimage.utils import render_variations


class MemoryUsageWidget(progressbar.widgets.Widget):
    def update(self, pbar):
        return 'RAM: {0:10.1f} MB'.format(
            resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
        )


class Command(BaseCommand):
    help = 'Renders all variations of a StdImageField.'
    args = '<app.model.field app.model.field>'

    def add_arguments(self, parser):
        parser.add_argument('--replace',
                            action='store_true',
                            dest='replace',
                            default=False,
                            help='Replace existing files.')

    def handle(self, *args, **options):
        replace = options.get('replace')
        for route in args:
            app_label, model_name, field_name = route.rsplit('.')
            model_class = get_model(app_label, model_name)
            queryset = model_class.objects \
                .exclude(**{'%s__isnull' % field_name: True}) \
                .exclude(**{field_name: ''})
            prog = self.get_processbar(queryset.count())
            images = queryset.values_list(field_name, flat=True)
            processes = [
                Process(target=self.render_field_variations, kwargs=dict(
                    prog=prog,
                    app_label=app_label,
                    model_name=model_name,
                    field_name=field_name,
                    file_name=file_name,
                    replace=replace,
                    ))
                for file_name in images
            ]
            [p.start() for p in processes]
            [p.join() for p in processes]
            prog.finish()

    @staticmethod
    def render_field_variations(prog, **kwargs):
        render_variations(**kwargs)
        prog += 1

    def get_processbar(self, count):
        return progressbar.ProgressBar(maxval=count, widgets=(
            progressbar.RotatingMarker(),
            ' | ', MemoryUsageWidget(),
            ' | ', progressbar.ETA(),
            ' | ', progressbar.Percentage(),
            ' ', progressbar.Bar(),
        ))
