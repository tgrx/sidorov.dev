from django.contrib import admin
from django.urls import include
from django.urls import path

from project.views import view_css_theme

urlpatterns = [
    # --- admin urls ---
    path("admin/", admin.site.urls),
    # --- static views ---
    path("theme/", view_css_theme, name="theme"),
    # --- pages ---
    path("", include("apps.index.urls", namespace="index")),
    path("portfolio/", include("apps.portfolio.urls", namespace="portfolio")),
    path("resume/", include("apps.resume.urls", namespace="resume")),
    path("thoughts/", include("apps.thoughts.urls", namespace="thoughts")),
]
