from math import ceil

import delorean
from django.conf import settings
from django.db import models as m

from project.utils.xdatetime import utcnow


class Calendar(m.Model):
    name = m.TextField(unique=True)
    description = m.TextField(null=True, blank=True)
    ical_url = m.URLField(null=True, blank=True, unique=True, verbose_name="iCal URL")
    ical = m.TextField(null=True, blank=True, verbose_name="iCal", editable=False)
    synced_at = m.DateTimeField(null=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.name!r} @ {self.synced_at}"

    class Meta:
        verbose_name_plural = "Calendars"
        ordering = ("name",)


class Event(m.Model):
    uid = m.TextField(null=True, blank=True, editable=False)
    start = m.DateTimeField(editable=False)
    end = m.DateTimeField(editable=False)
    summary = m.TextField(editable=False)
    calendar = m.TextField(editable=False)

    def __str__(self):
        return f"{self.calendar}: {self.summary} @ {self.start} ~ {self.end}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__} #{self.pk}: {self.day_number} -- {self.slots}"
        )

    @property
    def day_number(self) -> int:
        return (self.start.date() - utcnow().date()).days

    @property
    def slots(self) -> str:
        morning_local = delorean.parse("09:00:00", timezone=settings.TIME_ZONE)
        morning_utc = morning_local.shift("UTC").datetime.hour
        grid_offset = 2

        slot0 = self.start.hour - morning_utc + grid_offset
        slot1 = ceil(self.end.hour + self.end.minute / 60) - morning_utc + grid_offset
        return f"{slot0} / {slot1}"
