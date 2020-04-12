from django.urls import include
from django.urls import path

from apps.meta.apps import MetaConfig
from apps.meta.views import IndexView

app_name = MetaConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("schedule/", include("apps.meta.apps.schedule.urls")),
]
