from datetime import datetime
from datetime import timedelta
from typing import Union

import pytz
import requests
from django.db import models as m


class Calendar(m.Model):
    name = m.TextField(unique=True)
    description = m.TextField(null=True, blank=True)
    ical_url = m.URLField(null=True, blank=True, unique=True, verbose_name="iCal URL")
    ical = m.TextField(null=True, blank=True, verbose_name="iCal")
    synced_at = m.DateTimeField(null=True, blank=True)
    synced = m.BooleanField(default=False)

    def __str__(self):
        return f"{self.__class__.__name__}: {(self.name or '-')!r}"

    class Meta:
        verbose_name_plural = "Calendars"
        ordering = ("name",)

    def sync(self, force: bool = False) -> None:
        """Synchronizes the calendar content, if needed"""
        if not self.ical_url:
            self.synced = False
            self.save()
            return

        atm = datetime.utcnow().astimezone(pytz.UTC)
        next_sync_time = self.get_next_sync() if not force else atm

        if (next_sync_time - atm).total_seconds() > 5:  # FIXME: magic
            return

        ical = self.download_ical()
        if not ical:
            self.synced_at = atm
            self.synced = False
            self.save()
            return

        self.ical = ical
        self.synced_at = atm
        self.synced = True
        self.save()

    def get_next_sync(self) -> datetime:
        if self.synced_at:
            return self.synced_at + timedelta(minutes=5)  # FIXME: magic
        return datetime.utcnow().astimezone(pytz.UTC)

    def download_ical(self) -> Union[str, None]:
        if not self.ical_url:
            return None

        resp = requests.get(self.ical_url)
        if resp.status_code != 200:
            return None

        return resp.content.decode()
