from datetime import date
from datetime import datetime
from datetime import timedelta
from math import ceil
from typing import Collection
from typing import NamedTuple
from typing import Text
from typing import Tuple

from delorean import Delorean
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from icalevents import icalevents

from applications.meta.applications.schedule.models import Calendar
from project.utils.consts import AGE_1MINUTE
from project.utils.consts import MSQ


class DateRange(NamedTuple):
    end: datetime
    start: datetime


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


@method_decorator(cache_page(AGE_1MINUTE * 15), name="get")
class IndexView(TemplateView):  # pragma: no cover
    template_name = "schedule/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        schedule = self.get_schedule()
        ctx["schedule"] = schedule

        return ctx

    def get_schedule(self) -> Schedule:
        dates = self.get_date_range()
        calendars = self.get_calendars()
        last_update = Delorean(
            min([calendar.synced_at for calendar in calendars] or [None])
        ).shift(MSQ)
        events = self.collect_events(calendars, dates)
        days = self.group_days(events, dates)

        schedule = Schedule(
            days=days,
            end=dates.end,
            last_update=last_update.datetime,
            start=dates.start,
        )
        return schedule

    @staticmethod
    def get_date_range() -> DateRange:
        start = Delorean().shift(MSQ).midnight
        end = start + timedelta(days=16)  # FIXME: magic
        return DateRange(end=end, start=start)

    @staticmethod
    def get_calendars() -> Tuple[Calendar]:
        calendars = tuple(Calendar.objects.all())
        # for calendar in calendars:
        #     calendar.sync()
        return calendars

    @staticmethod
    def collect_events(
        calendars: Collection[Calendar], dates: DateRange
    ) -> Tuple[Event]:
        all_events = []
        populated_calendars = filter(lambda _c: _c.ical, calendars)

        for calendar in populated_calendars:
            ical = calendar.ical.encode()
            events_parsed = icalevents.events(
                end=dates.end, start=dates.start, string_content=ical,
            )
            events_urgent = filter(lambda _e: not _e.all_day, events_parsed)

            for iev in events_urgent:
                start = Delorean(iev.start).shift(MSQ).datetime
                end = Delorean(iev.end).shift(MSQ).datetime

                event = Event(
                    calendar=calendar,
                    end=end,
                    slot0=start.hour - 9 + 2,  # FIXME: magic
                    slot1=ceil(end.hour + end.minute / 60) - 9 + 2,  # FIXME: magic
                    start=start,
                    summary=iev.summary,
                )
                all_events.append(event)

        return tuple(all_events)

    @staticmethod
    def group_days(events: Collection[Event], dates: DateRange) -> Tuple[Day]:
        groups = {}
        atm = dates.start
        while atm < dates.end:
            day = atm.date()
            atm += timedelta(days=1)
            groups[day] = tuple(_e for _e in events if _e.start.date() == day)

        day = dates.start.date()
        days = tuple(
            Day(date=_d, number=(_d - day).days + 1, events=_e)
            for _d, _e in groups.items()
        )

        return days
