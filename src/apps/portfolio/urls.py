from django.urls import path

from apps.portfolio.apps import PortfolioConfig
from apps.portfolio.views import IndexView

app_name = PortfolioConfig.name

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
