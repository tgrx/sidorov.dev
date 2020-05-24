from celery.utils.log import get_task_logger

from periodic.app import app
from periodic.utils.xmodels import clear_events
from periodic.utils.xmodels import get_all_calendars
from periodic.utils.xmodels import get_single_calendar

logger = get_task_logger(__name__)


@app.task
def sync_all_calendars():
    logger.debug(f"syncing calendars")

    clear_events()

    calendars = get_all_calendars()
    for calendar in calendars:
        logger.info(f"calendar to sync: {calendar}")

        sync_single_calendar.delay(calendar.id)


@app.task
def sync_single_calendar(cal_id):
    from applications.meta.applications.schedule.utils import create_events
    from applications.meta.applications.schedule.utils import sync_calendar

    calendar = get_single_calendar(cal_id)
    sync_calendar(calendar)
    create_events(calendar)
