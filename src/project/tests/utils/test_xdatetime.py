from datetime import date
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

import pytz
import requests
from delorean import Delorean
from django.http import HttpRequest
from freezegun import freeze_time

from project.utils.xdatetime import DateDelta
from project.utils.xdatetime import get_user_hour
from project.utils.xdatetime import get_user_tz
from project.utils.xdatetime import utcnow


class MockRequestsResponse:
    def __init__(self, json, status_code=200):
        self.__json = json
        self.__status_code = status_code

    def json(self):
        return self.__json

    @property
    def status_code(self):
        return self.__status_code


class Test(TestCase):
    @freeze_time("2020-01-01 12:00:00")
    @patch("project.utils.xdatetime.get_user_tz")
    def test_get_user_hour(self, mock_get_user_tz):
        mock_get_user_tz.return_value = None
        ret = get_user_hour(HttpRequest())
        self.assertEqual(ret, 12)

        mock_get_user_tz.return_value = pytz.timezone("Europe/Minsk")
        ret = get_user_hour(HttpRequest())
        self.assertEqual(ret, 15)

    @freeze_time("2020-01-01 12:00:00")
    @patch("project.utils.xdatetime.get_client_ip")
    @patch.object(requests, requests.get.__name__)
    def test_get_user_tz(self, mock_requests_get, mock_get_client_ip):
        mock_get_client_ip.return_value = [None]

        mock_requests_get.return_value = MockRequestsResponse({"timezone": "UTC"})
        ret = get_user_tz(HttpRequest())
        self.assertEqual(ret, pytz.timezone("UTC"))

        mock_requests_get.return_value = MockRequestsResponse({})
        ret = get_user_tz(HttpRequest())
        self.assertIsNone(ret)

        mock_requests_get.return_value = MockRequestsResponse({"timezone": "UTC"}, 429)
        ret = get_user_tz(HttpRequest())
        self.assertIsNone(ret)

    @freeze_time("2020-01-01 12:00:00")
    def test_utcnow(self):
        atm = utcnow()
        self.assertEqual(
            atm, datetime(year=2020, month=1, day=1, hour=12, tzinfo=pytz.UTC)
        )

    def test_datedelta(self):
        y20m1d1 = date(year=2020, month=1, day=1)
        y20m1d2 = date(year=2020, month=1, day=2)
        y20m1d3 = date(year=2020, month=1, day=3)

        y20m2d1 = date(year=2020, month=2, day=1)
        y20m3d1 = date(year=2020, month=3, day=1)
        y20m4d1 = date(year=2020, month=4, day=1)

        y21m1d1 = date(year=2021, month=1, day=1)
        y21m2d1 = date(year=2021, month=2, day=1)
        y21m3d1 = date(year=2021, month=3, day=1)
        y22m1d1 = date(year=2022, month=1, day=1)
        y22m2d1 = date(year=2022, month=2, day=1)
        y22m3d1 = date(year=2022, month=3, day=1)

        delta = DateDelta.build(start=y20m1d1, finish=y20m1d1)
        self.assertEqual(delta.years, 0)
        self.assertEqual(delta.months, 0)
        self.assertEqual(str(delta), "<1 mo")

        delta = DateDelta.build(start=y20m1d1, finish=y20m1d2)
        self.assertEqual(delta.years, 0)
        self.assertEqual(delta.months, 0)
        self.assertEqual(str(delta), "<1 mo")

        delta = DateDelta.build(start=y20m1d1, finish=y20m1d3)
        self.assertEqual(delta.years, 0)
        self.assertEqual(delta.months, 0)
        self.assertEqual(str(delta), "<1 mo")

        delta = DateDelta.build(start=y20m1d1, finish=y20m2d1)
        self.assertEqual(delta.years, 0)
        self.assertEqual(delta.months, 1)
        self.assertEqual(str(delta), "1 mo")

        delta = DateDelta.build(start=y20m1d1, finish=y20m3d1)
        self.assertEqual(delta.years, 0)
        self.assertEqual(delta.months, 2)
        self.assertEqual(str(delta), "2 mos")

        delta = DateDelta.build(start=y20m1d1, finish=y20m4d1)
        self.assertEqual(delta.years, 0)
        self.assertEqual(delta.months, 3)
        self.assertEqual(str(delta), "3 mos")

        delta = DateDelta.build(start=y20m1d1, finish=y21m1d1)
        self.assertEqual(delta.years, 1)
        self.assertEqual(delta.months, 0)
        self.assertEqual(str(delta), "1 y")

        delta = DateDelta.build(start=y20m1d1, finish=y21m2d1)
        self.assertEqual(delta.years, 1)
        self.assertEqual(delta.months, 1)
        self.assertEqual(str(delta), "1 y 1 mo")

        delta = DateDelta.build(start=y20m1d1, finish=y21m3d1)
        self.assertEqual(delta.years, 1)
        self.assertEqual(delta.months, 2)
        self.assertEqual(str(delta), "1 y 2 mos")

        delta = DateDelta.build(start=y20m1d1, finish=y22m1d1)
        self.assertEqual(delta.years, 2)
        self.assertEqual(delta.months, 0)
        self.assertEqual(str(delta), "2 ys")

        delta = DateDelta.build(start=y20m1d1, finish=y22m2d1)
        self.assertEqual(delta.years, 2)
        self.assertEqual(delta.months, 1)
        self.assertEqual(str(delta), "2 ys 1 mo")

        delta = DateDelta.build(start=y20m1d1, finish=y22m3d1)
        self.assertEqual(delta.years, 2)
        self.assertEqual(delta.months, 2)
        self.assertEqual(str(delta), "2 ys 2 mos")

        delta = DateDelta.build(start=y20m1d1)
        delta_expected = Delorean().date - y20m1d1
        years_expected, _days = divmod(delta_expected.days, 365)
        months_expected = _days // 30
        self.assertEqual(delta.years, years_expected)
        self.assertEqual(delta.months, months_expected)
