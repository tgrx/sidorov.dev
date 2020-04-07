from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache


@never_cache
def view_index(request: HttpRequest) -> HttpResponse:
    return render(request, "thoughts/index.html")
