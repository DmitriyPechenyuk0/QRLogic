from django.shortcuts import render, get_object_or_404
from createqr_app.models import QrCode
import datetime,os
from user_app.models import Profile
from QRLogic import settings
from django.http import HttpRequest
# from django.contrib import now
# Create your views here.

def render_yourqr_app(request: HttpRequest):
    context = {'page': 'myqr'}

    profile = Profile.objects.get(user=request.user)
    qrcodess = QrCode.objects.filter(owner=request.user.profile)
    qrcodes = QrCode.objects.filter(owner=profile).order_by('-create_date')
    for qr in qrcodess:
        if qr.expire_date != datetime.datetime.now():
            context = {'page': 'myqr', 'qrcodes': qrcodess}

    qrcodes = QrCode.objects.filter(owner=profile).order_by('-create_date')

    if request.method == "POST" and "delete_qr" in request.POST:
        qr_id = request.POST.get("delete_qr")
        qr = get_object_or_404(QrCode, id=qr_id, owner__user=request.user)
         
        file_path = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{request.user.id}", qr.name)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        qr.delete()


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

    if request.user.is_authenticated:
        return render(request, 'yourqr_app/yourqrr.html', context=context)
    
    else:
        return render(request, 'createqr_app/authentication_required.html', context=context)
