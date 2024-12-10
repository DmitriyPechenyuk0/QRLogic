from django.shortcuts import render

# Create your views here.

def render_managesub_app(request):
    return render(request, 'managesub_app/managesub.html')

