from celery.utils.log import get_task_logger

from periodic.app import app
from periodic.utils.xmodels import drop_events
from periodic.utils.xmodels import get_all_calendars
from periodic.utils.xmodels import get_single_calendar
from project.utils.safeguards import safe

logger = get_task_logger(__name__)


@app.task
def sync_all_calendars():
    logger.info("start syncing calendars")

    drop_events()
    logger.debug("existing events have been dropped")

    calendars = get_all_calendars()
    logger.debug(f"calendars to proceed: {sorted(_elm.name for _elm in calendars)}")

    for calendar in calendars:
        sync_single_calendar.delay(calendar.id)
        logger.info(f"calendar to sync: {calendar}")

    logger.debug("done")


@app.task
@safe
def sync_single_calendar(cal_id):
    logger.debug(f"syncing calendar, pk={cal_id}")

    from applications.meta.applications.schedule.utils import create_events
    from applications.meta.applications.schedule.utils import sync_calendar

    calendar = get_single_calendar(cal_id)
    logger.debug(f"calendar with pk={cal_id} found: {calendar}")

    sync_calendar(calendar)
    logger.debug(f"calendar {calendar} has been populated")

    create_events(calendar)
    logger.debug(f"events from calendar {calendar} have been created")

    logger.info(f"calendar {calendar} has been synced")
