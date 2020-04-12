from collections import namedtuple
from datetime import datetime
from unittest.mock import patch

import pytz
import requests
from django.db import IntegrityError
from django.test import Client
from django.test import TestCase

from apps.meta.apps.schedule.models import Calendar
from apps.meta.apps.schedule.views import IndexView


class Test(TestCase):
    def setUp(self) -> None:
        self.cli = Client()

    def test_get(self):
        resp = self.cli.get("/meta/schedule/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.templates), 3)
        self.assertEqual(
            [_t.name for _t in resp.templates],
            ["schedule/index.html", "meta/index.html", "base.html"],
        )
        self.assertEqual(
            resp.resolver_match.func.__name__, IndexView.as_view().__name__
        )
        self.assertTrue(resp.has_header("Cache-Control"))
        self.assertIn("max-age=0", resp.get("Cache-Control"))

    @patch.object(requests, requests.get.__name__)
    def test_calendar_model(self, mock_requests_get):
        data = {"name": "calendar", "ical_url": "http://xxx.xxx"}

        cal = Calendar(**data)
        cal.save()

        self.assertTrue(cal.pk)
        self.assertTrue(cal.name, data["name"])
        self.assertTrue(cal.ical_url, data["ical_url"])

        with self.assertRaises(IntegrityError):
            cal2 = Calendar(**data)
            cal2.save()

        self.assertEqual(str(cal), f"Calendar: '{data['name']}'")

    @patch.object(requests, requests.get.__name__)
    def test_calendar_sync(self, mock_requests_get):
        mock_response = namedtuple("_", ["status_code", "content"])
        atm = datetime.utcnow().astimezone(pytz.UTC)

        cal = Calendar(name="test")
        cal.save()

        self.assertIsNone(cal.ical)
        self.assertIsNone(cal.synced_at)
        self.assertFalse(cal.synced)

        mock_requests_get.return_value = mock_response(200, b"yyy")
        cal.sync()

        self.assertIsNone(cal.ical)
        self.assertIsNone(cal.synced_at)
        self.assertFalse(cal.synced)
        self.assertIsNone(cal.download_ical())

        cal.ical_url = "https://xxx.xxx"
        cal.save()
        cal.sync()

        self.assertEqual(cal.ical, "yyy")
        self.assertLessEqual((cal.synced_at - atm).total_seconds(), 1)
        self.assertTrue(cal.synced)

        mock_requests_get.return_value = mock_response(200, b"zzz")
        cal.sync()

        self.assertEqual(cal.ical, "yyy")
        self.assertLessEqual((cal.synced_at - atm).total_seconds(), 1)
        self.assertTrue(cal.synced)

        mock_requests_get.return_value = mock_response(500, b"zzz")
        cal.sync(force=True)

        self.assertEqual(cal.ical, "yyy")
        self.assertLessEqual((cal.synced_at - atm).total_seconds(), 1)
        self.assertFalse(cal.synced)
