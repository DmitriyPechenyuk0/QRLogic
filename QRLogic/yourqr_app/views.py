from django.shortcuts import render

# Create your views here.

def render_yourqr_app(request):
    context = {'page': 'myqr'}
    if request.user.is_authenticated:
        return render(request, 'yourqr_app/yourqrr.html', context=context)
    else:
        return render(request, 'createqr_app/authentication_required.html', context=context)
