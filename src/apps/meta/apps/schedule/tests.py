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
        self.assertTrue(resp.has_header("Cache-Control"))
        self.assertEqual(resp.get("Cache-Control"), f"max-age={60 * 15}")

        self.assertEqual(resp.resolver_match.app_name, "meta:schedule")
        self.assertEqual(resp.resolver_match.url_name, "index")
        self.assertEqual(resp.resolver_match.view_name, "meta:schedule:index")
        self.assertEqual(
            resp.resolver_match.func.__name__, IndexView.as_view().__name__
        )

        self.assertEqual(resp.template_name, ["schedule/index.html"])

    def test_calendar_model(self):
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
