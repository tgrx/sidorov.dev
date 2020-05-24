from typing import List


def get_auth_profile_model() -> type:
    from applications.onboarding.models import AuthProfile as _Model

    return _Model


def get_all_calendars() -> List:
    from applications.meta.applications.schedule.models import Calendar

    return Calendar.objects.all()


def get_single_calendar(calendar_id):
    from applications.meta.applications.schedule.models import Calendar

    return Calendar.objects.get(pk=calendar_id)


def drop_events():
    from applications.meta.applications.schedule.models import Event

    Event.objects.all().delete()
