from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control


@cache_control(max_age=60 * 60 * 24)
def view_index(request: HttpRequest) -> HttpResponse:
    return render(request, "index/index.html")
