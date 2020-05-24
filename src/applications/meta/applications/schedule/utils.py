from datetime import datetime
from datetime import timedelta
from typing import List
from typing import NamedTuple
from typing import Union

import requests
from delorean import Delorean
from icalevents import icalevents

from applications.meta.applications.schedule.models import Calendar
from applications.meta.applications.schedule.models import Event
from project.utils.consts import MSQ
from project.utils.xdatetime import utcnow


class Day(NamedTuple):
    date: datetime
    date_s: str
    number: int


def get_days() -> List[Day]:
    start = Delorean().shift(MSQ).midnight
    days = []
    for i in range(16):  # FIXME: magic
        date = start + timedelta(days=i)
        day = Day(date=date, date_s=date.strftime("%a, %B %-d"), number=i + 1)
        days.append(day)
    return days


def sync_calendar(calendar: Calendar) -> None:
    if not calendar.ical_url:
        return

    ical = download_ical(calendar)

    calendar.ical = ical
    calendar.synced_at = utcnow()
    calendar.save()


def download_ical(calendar) -> Union[str, None]:
    if not (url := calendar.ical_url):
        return None

    resp = requests.get(url)
    if resp.status_code != 200:
        return None

    return resp.content.decode()


def create_events(calendar: Calendar):
    days = get_days()
    ical = calendar.ical.encode()
    events_parsed = icalevents.events(
        start=days[0].date, end=days[-1].date + timedelta(days=2), string_content=ical
    )
    events_urgent = filter(lambda _e: not _e.all_day, events_parsed)

    all_events = []
    for iev in events_urgent:
        start = Delorean(iev.start).shift(MSQ).datetime
        end = Delorean(iev.end).shift(MSQ).datetime

        event = Event(
            calendar=calendar.name,
            end=end,
            start=start,
            summary=iev.summary,
            uid=iev.uid,
        )
        all_events.append(event)

    Event.objects.bulk_create(all_events)
