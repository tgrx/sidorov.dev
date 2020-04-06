from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import include
from django.urls import path
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from project.utils import consts
from project.utils.xdatetime import get_user_hour

STATIC_DIR = settings.PROJECT_DIR / "static"


@cache_control(max_age=consts.AGE_1DAY)
def view_projects(request: HttpRequest) -> HttpResponse:
    return render(request, "projects.html")


@cache_control(max_age=consts.AGE_1DAY)
def view_resume(request: HttpRequest) -> HttpResponse:
    return render(request, "resume.html")


@never_cache
def view_thoughts(request: HttpRequest) -> HttpResponse:
    return render(request, "thoughts.html")


def render_static(file_path: Path, content_type: str) -> HttpResponse:
    if not file_path.is_file():
        full_path = file_path.as_posix()
        raise Http404(f"file '{full_path}' not found")

    with file_path.open("rb") as fp:
        content = fp.read()

    response = HttpResponse(content, content_type=content_type)
    return response


def get_theme_css(hour: int) -> Path:
    css = "theme_light.css" if (hour in consts.DAYLIGHT) else "theme_dark.css"
    css_path = STATIC_DIR / "css" / css
    return css_path


@cache_control(max_age=consts.AGE_1MINUTE * 10)
def view_css_theme(request: HttpRequest) -> HttpResponse:
    hour = get_user_hour(request)
    css = get_theme_css(hour)
    return render_static(css, "text/css")


urlpatterns = [
    # --- admin urls ---
    path("admin/", admin.site.urls),
    # --- static views ---
    path("theme/", view_css_theme, name="theme"),
    # --- pages ---
    path("", include("apps.index.urls")),
    path("projects/", view_projects, name="projects"),
    path("resume/", view_resume, name="resume"),
    path("thoughts/", view_thoughts, name="thoughts"),
]
