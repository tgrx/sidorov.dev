from django.urls import path

from apps.meta.apps.schedule import views
from apps.meta.apps.schedule.apps import ScheduleConfig

app_name = ScheduleConfig.label

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]
