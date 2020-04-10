from typing import Dict

from django.http import HttpRequest

from project.utils.consts import DAYLIGHT
from project.utils.xdatetime import get_user_hour


def user_hour(request: HttpRequest) -> Dict[str, int]:
    hour = get_user_hour(request)
    ctx = {
        "user_hour": hour,
        "daylight_hours": DAYLIGHT,
    }

    return ctx
