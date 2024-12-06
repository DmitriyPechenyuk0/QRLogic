from django.shortcuts import render

# Create your views here.

def render_home_app(request):

    return render(request, 'home_app/home.html')