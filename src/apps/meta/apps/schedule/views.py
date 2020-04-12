from datetime import date
from datetime import datetime
from datetime import timedelta
from typing import Collection
from typing import NamedTuple
from typing import Text
from typing import Tuple

import pytz
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView
from icalevents import icalevents

from apps.meta.apps.schedule.models import Calendar
from project.utils.consts import AGE_1MINUTE
from project.utils.xdatetime import get_user_tz


class DateRange(NamedTuple):
    end: date
    start: date


class Event(NamedTuple):
    calendar: Calendar
    end: datetime
    slot0: int
    slot1: int
    start: datetime
    summary: Text


class Day(NamedTuple):
    date: date
    number: int
    events: Tuple[Event]


class Schedule(NamedTuple):
    days: Tuple[Day]
    end: date
    last_update: datetime
    start: date


@method_decorator(cache_control(max_age=AGE_1MINUTE * 5), name="get")
class IndexView(TemplateView):
    template_name = "schedule/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        schedule = self.get_schedule()
        ctx["schedule"] = schedule

        utz = get_user_tz(self.request)
        ctx["utz"] = utz

        return ctx

    def get_schedule(self) -> Schedule:
        dates = self.get_date_range()
        calendars = self.get_calendars()
        last_update = min([calendar.synced_at for calendar in calendars] or [None])
        events = self.collect_events(calendars, dates)
        days = self.group_days(events, dates)

        schedule = Schedule(
            days=days, end=dates.end, last_update=last_update, start=dates.start,
        )
        return schedule

    def get_date_range(self) -> DateRange:
        reset_time_args = dict(hour=0, microsecond=0, minute=0, second=0,)
        start = datetime.utcnow().replace(**reset_time_args).astimezone(pytz.UTC).date()
        end = start + timedelta(days=8)  # FIXME: magic
        return DateRange(end=end, start=start)

    def get_calendars(self) -> Tuple[Calendar]:
        calendars = tuple(Calendar.objects.all())
        for calendar in calendars:
            calendar.sync()
        return calendars

    def collect_events(
        self, calendars: Collection[Calendar], dates: DateRange
    ) -> Tuple[Event]:
        all_events = []
        populated_calendars = filter(lambda calendar: calendar.ical, calendars)
        for calendar in populated_calendars:
            calendar_events = icalevents.events(
                end=dates.end, start=dates.start, string_content=calendar.ical.encode(),
            )
            urgent_events = filter(lambda event: not event.all_day, calendar_events)
            events = [
                Event(
                    calendar=calendar,
                    end=event.end,
                    slot0=(event.start).astimezone(pytz.timezone("Europe/Minsk")).hour
                    - 9
                    + 2,  # FIXME: magic
                    slot1=(event.end).astimezone(pytz.timezone("Europe/Minsk")).hour
                    - 9
                    + 2,  # FIXME: magic
                    start=event.start,
                    summary=event.summary,
                )
                for event in urgent_events
            ]
            all_events.extend(events)

        return tuple(all_events)

    def group_days(self, events: Collection[Event], dates: DateRange) -> Tuple[Day]:
        groups = {}
        this_day = dates.start
        while this_day < dates.end:
            next_day = this_day + timedelta(days=1)
            groups[this_day] = tuple(
                event for event in events if this_day <= event.start.date() < next_day
            )
            this_day = next_day

        days = tuple(
            Day(date=day, number=(day - dates.start).days + 1, events=events)
            for day, events in groups.items()
        )
        return days
