from django.test import TestCase

from applications.meta.applications.schedule.models import Calendar
from applications.meta.applications.schedule.models import Slot
from applications.onboarding.models import AuthProfile
from periodic.utils.xmodels import drop_slots
from periodic.utils.xmodels import get_all_calendars
from periodic.utils.xmodels import get_auth_profile_model
from periodic.utils.xmodels import get_single_calendar
from periodic.utils.xmodels import insert_slots


class Test(TestCase):
    def test_get_auth_profile_model(self):
        model = get_auth_profile_model()
        self.assertIs(model, AuthProfile)

    def test_get_all_calendars(self):
        c1 = Calendar(name="Z")
        c2 = Calendar(name="A")
        Calendar.objects.bulk_create([c1, c2])

        cals = list(get_all_calendars())
        self.assertListEqual([c2, c1], cals)

    def test_get_single_calendar(self):
        c1 = Calendar(name="c1")
        c2 = Calendar(name="c2")
        Calendar.objects.bulk_create([c1, c2])

        gc1 = get_single_calendar(c1.pk)
        self.assertEqual(c1, gc1)

        gc2 = get_single_calendar(c2.pk)
        self.assertEqual(c2, gc2)

    def test_drop_slots(self):
        s1 = Slot(day=1, slot0=0, slot1=1)
        s1.save()

        nr_slots = Slot.objects.count()
        self.assertEqual(1, nr_slots)

        drop_slots()

        nr_slots = Slot.objects.count()
        self.assertEqual(0, nr_slots)

    def test_insert_slots(self):
        dataset = {
            1: [(2, 3)],
            4: [(5, 6), (7, 8)],
        }

        insert_slots(dataset)

        nr_slots = Slot.objects.count()
        self.assertEqual(3, nr_slots)
