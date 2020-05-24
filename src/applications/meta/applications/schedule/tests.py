from django.db import IntegrityError
from django.test import Client
from django.test import TestCase

from applications.meta.applications.schedule.models import Calendar
from applications.meta.applications.schedule.views import IndexView
from project.utils.xtests import TemplateResponseTestMixin


class Test(TemplateResponseTestMixin, TestCase):
    def setUp(self) -> None:
        self.cli = Client()

    def test_get(self):
        self.validate_response(
            url="/meta/schedule/",
            expected_view=IndexView,
            expected_view_name="meta:schedule:index",
            expected_template="schedule/index.html",
        )

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

        self.assertEqual(str(cal), f"Calendar #{cal.pk}: '{data['name']}' @ None")
