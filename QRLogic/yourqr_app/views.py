from django.shortcuts import render
from createqr_app.models import QrCode
import datetime
# from django.contrib import now
# Create your views here.

def render_yourqr_app(request):
    context = {'page': 'myqr'}
    
    qrcodes = QrCode.objects.filter(owner=request.user.profile)
    for qr in qrcodes:
        if qr.expire_date != datetime.datetime.now():
            context = {'page': 'myqr', 'qrcodes': qrcodes}
        else:
            pass

    if request.user.is_authenticated:
        return render(request, 'yourqr_app/yourqrr.html', context=context)
    
    else:
        return render(request, 'createqr_app/authentication_required.html', context=context)
