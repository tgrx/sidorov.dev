from typing import Dict
from typing import List
from typing import Tuple


def get_auth_profile_model() -> type:
    from applications.onboarding.models import AuthProfile as _Model

    return _Model


def get_all_calendars() -> List:
    from applications.meta.applications.schedule.models import Calendar

    return Calendar.objects.all()


def get_single_calendar(calendar_id):
    from applications.meta.applications.schedule.models import Calendar

    return Calendar.objects.get(pk=calendar_id)


def drop_slots():
    from applications.meta.applications.schedule.models import Slot

    Slot.objects.all().delete()


def insert_slots(slots_map: Dict[int, List[Tuple]]):
    from applications.meta.applications.schedule.models import Slot

    objects = []

    for day, ranges in slots_map.items():
        for rng in ranges:
            obj = Slot(day=day, slot0=rng[0], slot1=rng[1])
            objects.append(obj)

    Slot.objects.bulk_create(objects)
