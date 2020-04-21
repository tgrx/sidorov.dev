from os import urandom

import delorean
from django.test import TestCase

from applications.resume.models import Framework
from applications.resume.models import Organization
from applications.resume.models import Project
from project.utils.xdatetime import DateDelta


class Test(TestCase):
    def test_project(self):
        placeholder = urandom(4).hex()

        start = delorean.parse("2020-01-01").date
        finish = delorean.parse("2021-03-03").date

        organization = Organization(name=placeholder)

        kw = {
            "name": placeholder,
            "organization": organization,
            "started_at": start,
        }

        prj = Project(**kw)
        self.assertEqual(prj.actual_name, placeholder)
        self.assertTrue(prj.on_air)
        self.assertEqual(str(prj), f"{placeholder!r} @ {placeholder} ({prj.pk})")

        prj = Project(nda_name=f"nda_{placeholder}", **kw)
        self.assertEqual(prj.actual_name, placeholder)

        prj = Project(nda_name=f"nda_{placeholder}", is_under_nda=True, **kw)
        self.assertEqual(prj.actual_name, f"nda_{placeholder}")

        prj = Project(finished_at=finish, **kw)
        self.assertEqual(prj.duration, DateDelta(years=1, months=2))
        self.assertFalse(prj.on_air)

        prj = Project(achievements_text="a\nb\nc\n", **kw)
        self.assertSetEqual(set(prj.achievements), set("abc"))

        prj = Project(responsibilities_text="a\nb\nc\n", **kw)
        self.assertSetEqual(set(prj.responsibilities), set("abc"))

    def test_organization(self):
        placeholder = urandom(4).hex()

        organization = Organization(name=placeholder)
        self.assertEqual(str(organization), f"{placeholder} ({organization.pk})")

    def test_framework(self):
        placeholder = urandom(4).hex()

        framework = Framework(name=placeholder)
        self.assertEqual(str(framework), f"{placeholder}")

        framework = Framework(name=placeholder, version="1.0.0")
        self.assertEqual(str(framework), f"{placeholder} 1.0.0")
