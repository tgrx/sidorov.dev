from celery import chord
from celery.utils.log import get_task_logger

from periodic.app import app
from periodic.utils.xmodels import drop_slots
from periodic.utils.xmodels import get_all_calendars
from periodic.utils.xmodels import get_single_calendar
from periodic.utils.xmodels import insert_slots
from project.utils.safeguards import safe

logger = get_task_logger(__name__)


@app.task
def sync_all_calendars():  # pragma: no cover
    logger.info("start syncing calendars")

    calendars = get_all_calendars()
    logger.debug(f"calendars to proceed: {sorted(_elm.name for _elm in calendars)}")

    sync_group = (sync_single_calendar.s(calendar.id) for calendar in calendars)
    harmonize = chord(sync_group)
    logger.debug("chord is created")

    harmonize(sync_slots.s())
    logger.debug("harmonize is started")

    logger.debug("done")


@app.task
@safe
def sync_single_calendar(cal_id):  # pragma: no cover
    logger.debug(f"syncing calendar, pk={cal_id}")

    from applications.meta.applications.schedule.utils import sync_calendar

    calendar = get_single_calendar(cal_id)
    logger.debug(f"calendar with pk={cal_id} found: {calendar}")

    sync_calendar(calendar)
    logger.info(f"calendar {calendar} has been synced")


@app.task
@safe
def sync_slots(*_args, **_kwargs):  # pragma: no cover
    logger.debug(f"syncing slots")

    from applications.meta.applications.schedule.utils import (
        build_merged_slots_map,
    )
    from applications.meta.applications.schedule.utils import build_slots_map
    from applications.meta.applications.schedule.utils import extract_events
    from applications.meta.applications.schedule.utils import get_days

    drop_slots()
    logger.debug(f"previous slots have been dropped")

    days = get_days()
    calendars = get_all_calendars()
    logger.debug(f"nr of calendars: {len(calendars)}")

    events = extract_events(calendars, days)
    logger.debug(f"nr of events: {len(events)}")

    slots_map = build_slots_map(events, days)
    logger.debug(f"slots map has been built")

    merged_slots_map = build_merged_slots_map(slots_map)
    logger.debug(f"merged slots map has been built")

    insert_slots(merged_slots_map)
    logger.debug(f"new slots have been inserted")

    logger.info(f"slots have been synced")
