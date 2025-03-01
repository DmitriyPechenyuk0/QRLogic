from django.shortcuts import render
from django.http import HttpRequest
# Create your views here.

def render_home_app(request: HttpRequest):
    context = {'page': 'home'}

    return render(request, 'home_app/home.html', context=context)