import segno, os, datetime

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from QRLogic import settings
from user_app.models import Profile
from .models import QrCode

# Create your views here.

def render_ceateqr_app(request):
    context = {'page': 'createqr'}
    if request.user.is_authenticated:
        if request.method == 'POST':

            profile = Profile.objects.get(user = request.user)

            url = request.POST.get('url')

            light_color= request.POST.get('light-color')
            dark_color = request.POST.get('dark-color')
            
            logo = request.FILES.get("upload")
            
            if logo:
                filepath_logo = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "Logos")


                all_logos = [logos for logos in os.listdir(filepath_logo) if logos.endswith('.png')]

                next_nameoflogo = len(all_logos) + 1
                logo_name = f"{next_nameoflogo}.png"

                logo_path = os.path.join(filepath_logo, logo_name)
                with open(logo_path, 'wb') as logo_file:
                    for part in logo.chunks():
                        logo_file.write(part)
                
                logo_url = f"/media/{request.user.username}_{request.user.id}/Logos/{logo_name}"

                qr = segno.make(content = url)
                
                filepath_qr = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "QRCodes")

                all_qrs = [qrcodes for qrcodes in os.listdir(filepath_qr) if qrcodes.endswith('.png')]

                next_nameofqr = len(all_qrs) + 1
                qr_name = f"{next_nameofqr}.png"

                qr_path = os.path.join(filepath_qr, qr_name)

                qr.save(out = str(qr_path), kind='png', dark=dark_color, light = light_color)

                QrCode.objects.create(
                    owner = profile,
                    url= url,
                    name= qr_name,
                    background_color= str(light_color),
                    color= str(dark_color)
                )
                context={'page': 'createqr', 'logo': logo_url}
                return render(request, 'createqr_app/createqrr.html', context=context)

            else:
                qr = segno.make(content = url)
                
                filepath_qr = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "QRCodes")

                all_qrs = [qrcodes for qrcodes in os.listdir(filepath_qr) if qrcodes.endswith('.png')]

                next_nameofqr = len(all_qrs) + 1
                qr_name = f"{next_nameofqr}.png"

                qr_path = os.path.join(filepath_qr, qr_name)



                qr.save(out = str(qr_path), kind='png', dark=dark_color, light = light_color)

                QrCode.objects.create(
                    owner = profile,
                    url= url,
                    name= qr_name,
                    background_color= str(light_color),
                    color= str(dark_color)
                )

                return render(request, 'createqr_app/createqrr.html', context=context)
        return render(request, 'createqr_app/createqrr.html', context=context)
    else:
        return render(request, 'createqr_app/authentication_required.html',context=context)