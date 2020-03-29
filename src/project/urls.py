from datetime import datetime
from pathlib import Path

import pytz
import requests
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from ipware import get_client_ip

CSS: Path = settings.REPO_DIR / "style.css"
CSS_DARK: Path = settings.REPO_DIR / "style_dark.css"
CSS_LIGHT: Path = settings.REPO_DIR / "style_light.css"
CSS_MOB: Path = settings.REPO_DIR / "style_mob.css"
FAVICON: Path = settings.REPO_DIR / "favicon.png"
HTML_INDEX: Path = settings.REPO_DIR / "index.html"
HTML_PROJECTS: Path = settings.REPO_DIR / "projects.html"
HTML_RESUME: Path = settings.REPO_DIR / "resume.html"
HTML_THOUGHTS: Path = settings.REPO_DIR / "thoughts.html"
JPG_ME: Path = settings.REPO_DIR / "me.jpg"

CACHE_AGE_1MINUTE = 60
CACHE_AGE_1HOUR = CACHE_AGE_1MINUTE * 60
CACHE_AGE_1DAY = CACHE_AGE_1HOUR * 24
CACHE_AGE_1MONTH = CACHE_AGE_1DAY * 30
DAYLIGHT = range(0, 24)


@cache_control(max_age=CACHE_AGE_1DAY)
def view_index(*_args, **__kwargs):
    with HTML_INDEX.open() as src:
        return HttpResponse(src.read())


@cache_control(max_age=CACHE_AGE_1DAY)
def view_projects(*_args, **__kwargs):
    with HTML_PROJECTS.open() as src:
        return HttpResponse(src.read())


@cache_control(max_age=CACHE_AGE_1DAY)
def view_resume(*_args, **__kwargs):
    with HTML_RESUME.open() as src:
        return HttpResponse(src.read())


@never_cache
def view_thoughts(*_args, **__kwargs):
    with HTML_THOUGHTS.open() as src:
        return HttpResponse(src.read())


@cache_control(max_age=CACHE_AGE_1MONTH)
def view_me_jpg(*_args, **__kwargs):
    with JPG_ME.open("rb") as src:
        return HttpResponse(src.read(), content_type="image/jpeg")


@cache_control(max_age=CACHE_AGE_1MONTH)
def view_favicon(*_args, **__kwargs):
    with FAVICON.open("rb") as src:
        return HttpResponse(src.read(), content_type="image/png")


@cache_control(max_age=CACHE_AGE_1MINUTE * 10)
def view_css_theme(request, *_args, **__kwargs):
    hour = get_user_hour(request)
    css = CSS_LIGHT if (hour in DAYLIGHT) else CSS_DARK
    with css.open() as src:
        return HttpResponse(src.read(), content_type="text/css")


@cache_control(max_age=CACHE_AGE_1DAY)
def view_css(*_args, **__kwargs):
    with CSS.open() as src:
        return HttpResponse(src.read(), content_type="text/css")


@cache_control(max_age=CACHE_AGE_1DAY)
def view_css_mob(*_args, **__kwargs):
    with CSS_MOB.open() as src:
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
    path("css_mob/", view_css_mob),
    path("favicon/", view_favicon),
    path("me/", view_me_jpg),
    path("projects/", view_projects),
    path("resume/", view_resume),
    path("theme/", view_css_theme),
    path("thoughts/", view_thoughts),
]
