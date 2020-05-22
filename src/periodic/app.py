import os

from celery import Celery
from dynaconf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **_kwargs):
    from periodic import tasks

    sender.add_periodic_task(
        settings.CELERY_BEAT_INVITATION,
        tasks.invite_all_users.delay(),
        name=tasks.invite_all_users.__name__,
    )

    sender.add_periodic_task(
        17, tasks.sync_calendars.s(), name=tasks.sync_calendars.__name__,
    )
