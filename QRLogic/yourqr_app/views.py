from django.shortcuts import render
from createqr_app.models import QrCode
# Create your views here.

def render_yourqr_app(request):
    context = {'page': 'myqr'}
    
    qrcodes = QrCode.objects.filter(owner=request.user.profile)
    context = {'page': 'myqr', 'qrcodes': qrcodes}

    if request.user.is_authenticated:
        return render(request, 'yourqr_app/yourqrr.html', context=context)
    
    else:
        return render(request, 'createqr_app/authentication_required.html', context=context)
