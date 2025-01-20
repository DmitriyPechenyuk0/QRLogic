from django.shortcuts import render

# Create your views here.

def render_home_app(request):
    context = {'page': 'home'}

    return render(request, 'home_app/home.html', context=context)