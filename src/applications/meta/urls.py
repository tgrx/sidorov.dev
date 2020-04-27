from django.urls import include
from django.urls import path

from applications.meta.apps import MetaConfig
from applications.meta.views import IndexView

app_name = MetaConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("schedule/", include("applications.meta.applications.schedule.urls")),
    path("blog/", include("applications.meta.applications.blog.urls")),
]
