from datetime import datetime

import pytz
import requests
from django.http import HttpRequest
from ipware import get_client_ip


def get_user_hour(request: HttpRequest) -> int:
    ip = get_client_ip(request)[0]
    resp = requests.get(f"http://ip-api.com/json/{ip}")
    payload = resp.json()
    at_this_moment = datetime.now()

    if "timezone" not in payload:
        hour = at_this_moment.hour
    else:
        tz_name = payload["timezone"]
        tz = pytz.timezone(tz_name)
        hour = pytz.utc.localize(datetime.now()).astimezone(tz).hour

    return hour
