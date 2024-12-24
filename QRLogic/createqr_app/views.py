from django.shortcuts import render

# Create your views here.


def render_ceateqr_app(request):
    return render(request, 'createqr_app/createqrr.html')