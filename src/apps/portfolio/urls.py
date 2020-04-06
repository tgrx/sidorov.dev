from django.urls import path

from apps.portfolio.views import view_portfolio

urlpatterns = [
    path("", view_portfolio, name="portfolio"),
]
