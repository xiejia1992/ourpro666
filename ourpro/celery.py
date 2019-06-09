from __future__ import absolute_import,unicode_literals
import os
from celery import Celery, platforms
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ourpro.settings")
app = Celery('ourpro')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
platforms.C_FORCE_ROOT = True


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
