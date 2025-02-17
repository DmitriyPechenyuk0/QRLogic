from django.shortcuts import render, redirect
import os
from django.contrib.auth.decorators import login_required
from user_app.models import Profile
from createqr_app.models import QrCode
from QRLogic import settings
from datetime import datetime





# Create your views here

@login_required
def render_yourqr_app(request):
    profile = Profile.objects.get(user=request.user)
    qrcodes = QrCode.objects.filter(owner=profile).order_by('-create_date')
    context = {'page': 'myqr'}
    if request.method == "POST":
        date_filter = request.POST.get('date_filter')
        if date_filter:  
                selected_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
                qrcodes = qrcodes.filter(create_date__date=selected_date)



    url_filter = request.POST.get('url_filter')
    if url_filter:
        qrcodes = qrcodes.filter(url__icontains=url_filter)

    qr_images = []
    for qr in qrcodes:
        image_url = f"{settings.MEDIA_URL}{request.user.username}_{request.user.id}/{qr.name}"  
        qr_images.append({
            'name': qr.name,
            'image_url': image_url,
            'url': qr.url,
            'date': qr.create_date
        })

    context = {
        'page': 'myqr',
        'qrcodes': qrcodes,
        'qr_images': qr_images  
    }

    return render(request, 'yourqr_app/yourqrr.html', context)

