from django.shortcuts import render, redirect
import os
from django.contrib.auth.decorators import login_required
from user_app.models import Profile
from createqr_app.models import QrCode
from QRLogic import settings





# Create your views here.

@login_required
def render_yourqr_app(request):
    profile = Profile.objects.get(user=request.user)
    qrcodes = QrCode.objects.filter(owner=profile).order_by('-create_date')

    for qr in qrcodes:
        filepath = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{request.user.id}/{qr.name}")
        if os.path.exists(filepath):
            qr.image_url = f"{settings.MEDIA_URL}{request.user.username}_{request.user.id}/{qr.name}"
            context ={
                'page': 'myqr',
                'qrcodes': qrcodes,
                'qrimage': qr.image_url
            }
        

    context = {
        'page': 'myqr',
        'qrcodes': qrcodes
    }

    return render(request, 'yourqr_app/yourqrr.html', context)
