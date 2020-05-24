from math import ceil

from django.db import models as m

from project.utils.xdatetime import utcnow


class Calendar(m.Model):
    name = m.TextField(unique=True)
    description = m.TextField(null=True, blank=True)
    ical_url = m.URLField(null=True, blank=True, unique=True, verbose_name="iCal URL")
    ical = m.TextField(null=True, blank=True, verbose_name="iCal")
    synced_at = m.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name!r}"

    class Meta:
        verbose_name_plural = "Calendars"
        ordering = ("name",)


class Event(m.Model):
    uid = m.UUIDField()
    start = m.DateTimeField()
    end = m.DateTimeField()

    @property
    def day_number(self) -> int:
        return (self.start - utcnow()).days

    @property
    def slots(self) -> str:
        slot0 = (self.start.hour - 9 + 2,)  # FIXME: magic
        slot1 = (ceil(self.end.hour + self.end.minute / 60) - 9 + 2,)  # FIXME: magic
        return f"{slot0} / {slot1}"
