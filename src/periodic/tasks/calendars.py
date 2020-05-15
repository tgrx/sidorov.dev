from celery.utils.log import get_task_logger

from periodic.app import app

logger = get_task_logger(__name__)


@app.task
def sync_calendars():
    from applications.meta.applications.schedule.models import Calendar

    logger.debug("start syncing calendars")

    for calendar in Calendar.objects.all():
        logger.debug(f"syncing now: {calendar}")
        calendar.sync()
        logger.debug(f"done: {calendar} at {calendar.synced_at}")
