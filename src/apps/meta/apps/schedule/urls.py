from django.urls import path

from apps.meta.apps.schedule.apps import ScheduleConfig
from apps.meta.apps.schedule.views import IndexView

app_name = ScheduleConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
