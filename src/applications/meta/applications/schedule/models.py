from django.db import models as m


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


class Busy(m.Model):
    uid = m.IntegerField(unique=True)
    start = m.DateTimeField()
    end = m.DateTimeField()
    slot0 = m.PositiveSmallIntegerField()
    slot1 = m.PositiveSmallIntegerField()
