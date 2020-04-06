from django.contrib import admin
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import include
from django.urls import path
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache

from project.utils import consts
from project.views import view_css_theme


@cache_control(max_age=consts.AGE_1DAY)
def view_projects(request: HttpRequest) -> HttpResponse:
    return render(request, "projects.html")


@cache_control(max_age=consts.AGE_1DAY)
def view_resume(request: HttpRequest) -> HttpResponse:
    return render(request, "resume.html")


@never_cache
def view_thoughts(request: HttpRequest) -> HttpResponse:
    return render(request, "thoughts.html")


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
