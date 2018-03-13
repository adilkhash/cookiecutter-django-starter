{% if cookiecutter.use_celery == 'y' %}
import os
{%- if cookiecutter.use_sentry %}
import raven
from raven.contrib.celery import register_signal, register_logger_signal
{%- endif %}
import celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{cookiecutter.project_slug}}.settings')

{%- if cookiecutter.use_sentry %}
class Celery(celery.Celery):

    def on_configure(self):
        if settings.DSN:
            client = raven.Client(settings.DSN)
            register_logger_signal(client)
            register_signal(client)
        else:
            pass

app = Celery(__name__)
{% else %}
app = celery.Celery(__name__)
{%- endif %}
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
{%- endif %}
