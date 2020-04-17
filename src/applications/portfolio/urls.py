from django.urls import path

from applications.portfolio.apps import PortfolioConfig
from applications.portfolio.views import IndexView

app_name = PortfolioConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
