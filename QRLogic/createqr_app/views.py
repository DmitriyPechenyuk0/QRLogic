import segno, os, datetime
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from QRLogic import settings
from user_app.models import Profile
from .models import QrCode

# Create your views here.

@login_required
def render_ceateqr_app(request):
    context = {'page': 'createqr'}
    if request.method == 'POST':

        profile = Profile.objects.get(user = request.user)

        url = request.POST.get('url')

        qr = segno.make_qr(content = url)
        
        filepath = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}")

        all_files = [qrcodes for qrcodes in os.listdir(filepath) if qrcodes.endswith('.png')]
        next_nameofqr = len(all_files) + 1

        qr_name = f"{next_nameofqr}.png"

        qr_path = os.path.join(filepath, qr_name)

        qr.save(out = str(qr_path), kind='png')

        QrCode.objects.create(
            owner = profile,
            url=url,
            name=qr_name,
            # create_date = int(datetime.date.today()),
            # expire_date = int(datetime.date(day=30))
        )

        return render(request, 'createqr_app/createqrr.html', context=context)
    return render(request, 'createqr_app/createqrr.html', context=context)