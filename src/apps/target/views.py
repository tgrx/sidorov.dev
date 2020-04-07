from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from project.utils import consts


@cache_control(max_age=consts.AGE_1DAY)
def view_index(request: HttpRequest) -> HttpResponse:
    return render(request, "target/index.html")
