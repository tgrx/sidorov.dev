from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

HTML_INDEX: Path = settings.REPO_DIR / "index.html"
HTML_PROJECTS: Path = settings.REPO_DIR / "projects.html"
HTML_RESUME: Path = settings.REPO_DIR / "resume.html"
HTML_THOUGHTS: Path = settings.REPO_DIR / "thoughts.html"
JPG_ME: Path = settings.REPO_DIR / "me.jpg"


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


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", view_index),
    path("resume/", view_resume),
    path("projects/", view_projects),
    path("thoughts/", view_thoughts),
    path("me/", view_me_jpg),
]
