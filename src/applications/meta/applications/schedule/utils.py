from datetime import date
from datetime import timedelta
from typing import Dict
from typing import Iterable
from typing import List
from typing import NamedTuple
from typing import Tuple
from typing import Union

import requests
from dateutil.tz import tzutc
from icalevents import icalevents
from icalevents import icalparser

from applications.meta.applications.schedule.models import Calendar
from project.utils.xdatetime import utcnow


class Day(NamedTuple):
    date: date
    date_s: str
    number: int


DaysT = Tuple[Day]
SlotsMapT = Dict[int, List[int]]
RangesMapT = Dict[int, List[Tuple]]


def get_days() -> DaysT:
    start = utcnow().date()
    days = []

    for i in range(16):  # FIXME: magic
        current = start + timedelta(days=i)
        day = Day(date=current, date_s=current.strftime("%a, %B %-d"), number=i + 1)
        days.append(day)

    return tuple(days)


def sync_calendar(calendar: Calendar) -> None:
    if not (url := calendar.ical_url):
        return

    calendar.ical = download(url)
    calendar.synced_at = utcnow()
    calendar.save()


def download(url: str) -> Union[str, None]:
    resp = requests.get(url, timeout=30)  # FIXME: magic
    if resp.status_code != 200:
        return None

    return resp.content.decode()


def extract_events(
    calendars: Iterable[Calendar], days: DaysT
) -> List[icalparser.Event]:
    calendars_with_ical = filter(lambda _c: _c.ical, calendars)
    date_from = days[0].date
    date_to = days[-1].date + timedelta(days=1)
    result = []

    for calendar in calendars_with_ical:
        ical = calendar.ical.encode()
        events = icalevents.events(start=date_from, end=date_to, string_content=ical)
        events_urgent = filter(lambda _e: not _e.all_day, events)
        result.extend(events_urgent)

    return result


def build_slots_map(events: Iterable[icalparser.Event], days: DaysT) -> SlotsMapT:
    day_slots = {day.date: [0] * 14 for day in days}  # FIXME: magic

    for event in events:
        diff = 9  # FIXME: magic
        if isinstance(event.start.tzinfo, tzutc):  # FIXME: magic
            diff = 6  # FIXME: magic
        day = event.start.date()
        slots = day_slots[day]
        h0 = event.start.hour - diff
        h1 = event.end.hour - diff
        if event.end.minute > 0:
            h1 += 1

        slots[h0:h1] = [1] * (h1 - h0)

    day_slots = {
        (day - days[0].date).days + 1: slots for day, slots in day_slots.items()
    }

    return day_slots


def merge_slots(slots: List[int]) -> List[Tuple]:
    if not slots:
        return []

    begin = end = -1
    merged = []

    def _append():
        nonlocal begin
        nonlocal end
        nonlocal merged
        if begin < 0:
            return
        merged.append((begin, end + 1))
        begin = end = -1

    for pos, slot in enumerate(slots):
        if not slot:
            _append()
        else:
            if begin < 0:
                begin = pos
            end = pos
    _append()

    return merged


def build_merged_slots_map(slots_map: SlotsMapT) -> RangesMapT:
    merged = {day: merge_slots(slots) for day, slots in slots_map.items()}
    return merged
