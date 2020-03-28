from datetime import datetime
from pathlib import Path

import pytz
import requests
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from ipware import get_client_ip

HTML_INDEX: Path = settings.REPO_DIR / "index.html"
HTML_PROJECTS: Path = settings.REPO_DIR / "projects.html"
HTML_RESUME: Path = settings.REPO_DIR / "resume.html"
HTML_THOUGHTS: Path = settings.REPO_DIR / "thoughts.html"
JPG_ME: Path = settings.REPO_DIR / "me.jpg"
CSS_LIGHT: Path = settings.REPO_DIR / "style_light.css"
CSS_DARK: Path = settings.REPO_DIR / "style_dark.css"


def view_index(*_args, **__kwargs):
    with HTML_INDEX.open() as src:
        return HttpResponse(src.read())


def view_projects(*_args, **__kwargs):
    with HTML_PROJECTS.open() as src:
        return HttpResponse(src.read())


def view_resume(*_args, **__kwargs):
    with HTML_RESUME.open() as src:
        return HttpResponse(src.read())


def view_thoughts(*_args, **__kwargs):
    with HTML_THOUGHTS.open() as src:
        return HttpResponse(src.read())


def view_me_jpg(*_args, **__kwargs):
    with JPG_ME.open("rb") as src:
        return HttpResponse(src.read(), content_type="image/jpeg")


def view_css(request, *_args, **__kwargs):
    hour = get_user_hour(request)
    css = CSS_LIGHT if (9 <= hour <= 17) else CSS_DARK
    with css.open() as src:
        return HttpResponse(src.read(), content_type="text/css")


def get_user_hour(request):
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


urlpatterns = [
    path("", view_index),
    path("admin/", admin.site.urls),
    path("css/", view_css),
    path("me/", view_me_jpg),
    path("projects/", view_projects),
    path("resume/", view_resume),
    path("thoughts/", view_thoughts),
]
