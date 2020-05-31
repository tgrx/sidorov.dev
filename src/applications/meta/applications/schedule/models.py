from datetime import timedelta

from delorean import Delorean
from django.db import models as m


class Calendar(m.Model):
    name = m.TextField(unique=True)
    description = m.TextField(null=True, blank=True)
    ical_url = m.URLField(null=True, blank=True, unique=True, verbose_name="iCal URL")
    ical = m.TextField(null=True, blank=True, verbose_name="iCal", editable=False)
    synced_at = m.DateTimeField(null=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.name!r} @ {self.synced_at}"

    class Meta:
        ordering = ("name",)


class Slot(m.Model):
    day = m.PositiveSmallIntegerField()
    slot0 = m.PositiveSmallIntegerField()
    slot1 = m.PositiveSmallIntegerField()

    @property
    def slots(self) -> str:
        return f"{self.slot0 + 2}/{self.slot1 + 2}"

    def __str__(self):
        d = Delorean().midnight.date() + timedelta(days=self.day - 1)
        h0 = self.slot0 + 9
        h1 = self.slot1 + 9
        return f"{self.__class__.__name__}({self.day}, {self.slots}) - {d} {h0:02d}~{h1:02d}"

    class Meta:
        ordering = ("day", "slot0", "slot1")
