from datetime import datetime
from pathlib import Path

import pytz
import requests
from django.conf import settings
from django.contrib import admin
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from ipware import get_client_ip

CACHE_AGE_1MINUTE = 60
CACHE_AGE_1HOUR = CACHE_AGE_1MINUTE * 60
CACHE_AGE_1DAY = CACHE_AGE_1HOUR * 24
CACHE_AGE_1MONTH = CACHE_AGE_1DAY * 30
DAYLIGHT = range(9, 21)


@cache_control(max_age=CACHE_AGE_1DAY)
def view_index(request):
    return render(request, "index.html")


@cache_control(max_age=CACHE_AGE_1DAY)
def view_projects(request):
    return render(request, "projects.html")


@cache_control(max_age=CACHE_AGE_1DAY)
def view_resume(request):
    return render(request, "resume.html")


@never_cache
def view_thoughts(request):
    return render(request, "thoughts.html")


def render_static(file_path: Path, content_type: str) -> HttpResponse:
    if not file_path.is_file():
        full_path = file_path.as_posix()
        raise Http404(f"file '{full_path}' not found")

    with file_path.open("rb") as fp:
        content = fp.read()

    response = HttpResponse(content, content_type=content_type)
    return response


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


def get_theme_css(hour: int) -> Path:
    css = "theme_light.css" if (hour in DAYLIGHT) else "theme_dark.css"
    css_path = settings.PROJECT_DIR / "static" / "css" / css
    return css_path


@cache_control(max_age=CACHE_AGE_1MONTH)
def view_me_jpg(_request):
    return render_static(settings.PROJECT_DIR / "static" / "me.jpg", "image/jpeg")


@cache_control(max_age=CACHE_AGE_1MONTH)
def view_favicon(*_args, **__kwargs):
    return render_static(settings.PROJECT_DIR / "static" / "favicon.png", "image/png")


@cache_control(max_age=CACHE_AGE_1MINUTE * 10)
def view_css_theme(request):
    hour = get_user_hour(request)
    css = get_theme_css(hour)
    return render_static(css, "text/css")


@cache_control(max_age=CACHE_AGE_1DAY)
def view_css(_request):
    return render_static(
        settings.PROJECT_DIR / "static" / "css" / "base.css", "text/css"
    )


@cache_control(max_age=CACHE_AGE_1DAY)
def view_css_mob(_request):
    return render_static(
        settings.PROJECT_DIR / "static" / "css" / "responsive.css", "text/css"
    )


urlpatterns = [
    # --- admin urls ---
    path("admin/", admin.site.urls),
    # --- static views ---
    path("css/", view_css),
    path("css_mob/", view_css_mob),
    path("favicon/", view_favicon),
    path("me/", view_me_jpg),
    path("theme/", view_css_theme),
    # --- pages ---
    path("", view_index, name="index"),
    path("projects/", view_projects, name="projects"),
    path("resume/", view_resume, name="resume"),
    path("thoughts/", view_thoughts, name="thoughts"),
]
