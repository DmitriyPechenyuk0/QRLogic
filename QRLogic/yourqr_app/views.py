from django.shortcuts import render

# Create your views here.

def render_yourqr_app(request):
    context = {'page': 'myqr'}
    return render(request, 'yourqr_app/yourqrr.html', context)
