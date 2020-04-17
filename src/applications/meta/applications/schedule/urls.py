from django.urls import path

from applications.meta.applications.schedule import views
from applications.meta.applications.schedule.apps import ScheduleConfig

app_name = ScheduleConfig.label

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]
