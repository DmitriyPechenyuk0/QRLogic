from django.shortcuts import render

# Create your views here.

def render_reg(request):
    return render(request, 'user_app/signupp.html')

def render_auth(request):
    return render(request, 'user_app/login.html')


