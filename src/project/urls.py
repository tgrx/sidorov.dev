from django.contrib import admin
from django.urls import include
from django.urls import path

from project.views import view_favicon

urlpatterns = [
    # --- admin urls ---
    path("admin/", admin.site.urls),
    # --- static views ---
    path("favicon.ico", view_favicon, name="favicon"),
    # --- apps ---
    path("", include("apps.target.urls")),
    path("portfolio/", include("apps.portfolio.urls")),
    path("resume/", include("apps.resume.urls")),
    path("thoughts/", include("apps.thoughts.urls")),
]
