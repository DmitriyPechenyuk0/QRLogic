import segno, os, io, qrcode, datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.utils import timezone
from QRLogic import settings
from user_app.models import Profile
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import GappedSquareModuleDrawer,CircleModuleDrawer,SquareModuleDrawer,RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from .models import QrCode
from PIL import Image
from django.http import Http404, HttpRequest
from django.urls import reverse

# Create your views here.

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def qr_redirect(request, qr_code_id):
    qr_code = get_object_or_404(QrCode, id=qr_code_id)
    if timezone.now() < qr_code.expire_date:
        return redirect(qr_code.url)
    else:
        return Http404('QR code was expired')

def render_ceateqr_app(request: HttpRequest):
    context = {'page': 'createqr'}

    keywords = [
    "https://", "http://", ".com", ".org", ".net", ".info", ".biz", ".pro",
    ".us", ".uk", ".ru", ".de", ".fr", ".it", ".es", ".cn",
    ".jp", ".br", ".in", ".ca", ".au", ".eu", ".asia",
    ".africa", ".lat", ".scot", ".cat", ".tech", ".app",
    ".dev", ".store", ".blog", ".news", ".xyz"
    ]

    if request.user.is_authenticated:
        if request.method == 'POST':
            
            sub = request.user.profile.subscription
            


            subs_type = {
                'free': 1,
                'standart':10,
                'pro': 50,
            }


            profile = Profile.objects.get(user = request.user)

            url = request.POST.get('url')

            if any(key in url for key in keywords):
                qr_count = QrCode.objects.filter(owner=request.user.profile, type_qr = 'standart').count()

                if qr_count < subs_type[sub]:
                    light_color= request.POST.get('light-color')
                    dark_color = request.POST.get('dark-color')
                    light_color= hex_to_rgb(light_color)
                    dark_color = hex_to_rgb(dark_color)

                    logo = request.FILES.get("upload")

                    today = datetime.datetime.today()
                    expire = today + datetime.timedelta(days=30)

                    scale = request.POST.get('sizeqr')

                    body = request.POST.get('body')
                    square = request.POST.get('squares')

                    drawers = { 'rounded': RoundedModuleDrawer(),
                                'square': SquareModuleDrawer(),
                                'circle': CircleModuleDrawer(),
                                'gapped': GappedSquareModuleDrawer(),
                                'horizontal': HorizontalBarsDrawer(),
                                'vertical': VerticalBarsDrawer()}

                    if logo:

                        filepath_qr = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "QRCodes")

                        all_qrs = [qrcodes for qrcodes in os.listdir(filepath_qr) if qrcodes.endswith('.png')]

                        next_nameofqr = len(all_qrs) + 1
                        qr_name = f"{next_nameofqr}.png"

                        qr_path = os.path.join(filepath_qr, qr_name)

                        qri = QrCode.objects.create(
                            owner = profile,
                            url= url,
                            name= qr_name,
                            background_color= str(light_color),
                            color= str(dark_color),
                            body_style=body,
                            square_style=square,
                            create_date=today,
                            expire_date=expire,
                            type_qr= 'standart'
                        )
                        out = io.BytesIO()

                        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

                        qr_link = request.build_absolute_uri(reverse('qr_redirect', args=[qri.id]))

                        qr.add_data(qr_link)
                        qr.make()

                        qr_code = qr.make_image(
                            image_factory=StyledPilImage,
                            module_drawer=drawers[body],
                            eye_drawer=drawers[square],
                            color_mask=SolidFillColorMask(front_color=dark_color, back_color=light_color))

                        qr_code.save(out, kind='png')

                        out.seek(0)
                        img = Image.open(out).convert('RGBA')

                        filepath_logo = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "Logos")


                        all_logos = [logos for logos in os.listdir(filepath_logo) if logos.endswith('.png')]

                        next_nameoflogo = len(all_logos) + 1
                        logo_name = f"{next_nameoflogo}.png"

                        logo_path = os.path.join(filepath_logo, logo_name)
                        with open(logo_path, 'wb') as logo_file:
                            for part in logo.chunks():
                                logo_file.write(part)

                        logo_url = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{request.user.id}", 'Logos', logo_name)

                        img_width, img_height = img.size
                        logo_max_size = img_height // 4

                        logo_img = Image.open(logo_url).convert("RGBA")

                        logo_width, logo_height = logo_img.size

                        max_side = max(logo_width, logo_height)
                        square_logo = Image.new("RGBA", (max_side, max_side), (255, 255, 255, 0))

                        x_offset = (max_side - logo_width) // 2
                        y_offset = (max_side - logo_height) // 2
                        square_logo.paste(logo_img, (x_offset, y_offset), logo_img)

                        square_logo = square_logo.resize((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)

                        box = ((img_width - logo_max_size) // 2, (img_height - logo_max_size) // 2)

                        img.paste(square_logo, box, square_logo)

                        img.save(qr_path)

                        relative_qr_path = os.path.join('media', os.path.relpath(qr_path, settings.MEDIA_ROOT))

                        context={'page': 'createqr',
                                    'logo': logo_url,
                                    'qrcode': '/' + relative_qr_path.replace("\\", "/")}

                        return render(request, 'createqr_app/createqrr.html', context=context)

                    else:
                        filepath_qr = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "QRCodes")

                        all_qrs = [qrcodes for qrcodes in os.listdir(filepath_qr) if qrcodes.endswith('.png')]

                        next_nameofqr = len(all_qrs) + 1
                        qr_name = f"{next_nameofqr}.png"

                        qr_path = os.path.join(filepath_qr, qr_name)

                        qri = QrCode.objects.create(
                            owner = profile,
                            url= url,
                            name= qr_name,
                            background_color= str(light_color),
                            color= str(dark_color),
                            body_style=body,
                            square_style=square,
                            create_date=today,
                            expire_date=expire,
                            type_qr= 'standart'
                        )


                        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

                        qr_link = request.build_absolute_uri(reverse('qr_redirect', args=[qri.id]))

                        qr.add_data(qr_link)
                        qr.make(fit=True)
                        qr_code = qr.make_image(
                            image_factory=StyledPilImage,
                            module_drawer=drawers[body],
                            eye_drawer=drawers[square],
                            color_mask=SolidFillColorMask(front_color=dark_color, back_color=light_color))

                        qr_code.save(str(qr_path), kind='png')

                        relative_qr_path = os.path.join('media', os.path.relpath(qr_path, settings.MEDIA_ROOT))

                        context= {'page': 'createqr',
                                    'qrcode': '/' + relative_qr_path.replace("\\", "/")}

            elif request.user.profile.commerce == True and not any(key in url for key in keywords):
                
                count_of_cells = request.user.profile.commerce_cells

                qr_codess = QrCode.objects.filter(owner=request.user.profile, type_qr = 'commerce').count()

                if count_of_cells > qr_codess:
                    light_color= request.POST.get('light-color')
                    dark_color = request.POST.get('dark-color')
                    light_color= hex_to_rgb(light_color)
                    dark_color = hex_to_rgb(dark_color)

                    logo = request.FILES.get("upload")

                    today = datetime.datetime.today()
                    expire = today + datetime.timedelta(days=30)

                    scale = request.POST.get('sizeqr')

                    body = request.POST.get('body')
                    square = request.POST.get('squares')

                    drawers = { 'rounded': RoundedModuleDrawer(),
                                'square': SquareModuleDrawer(),
                                'circle': CircleModuleDrawer(),
                                'gapped': GappedSquareModuleDrawer(),
                                'horizontal': HorizontalBarsDrawer(),
                                'vertical': VerticalBarsDrawer()}

                    if logo:

                        filepath_qr = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "QRCodes")

                        all_qrs = [qrcodes for qrcodes in os.listdir(filepath_qr) if qrcodes.endswith('.png')]

                        next_nameofqr = len(all_qrs) + 1
                        qr_name = f"{next_nameofqr}.png"

                        qr_path = os.path.join(filepath_qr, qr_name)

                        qri = QrCode.objects.create(
                            owner = profile,
                            url= url,
                            name= qr_name,
                            background_color= str(light_color),
                            color= str(dark_color),
                            body_style=body,
                            square_style=square,
                            type_qr = 'commerce'
                        )
                        out = io.BytesIO()

                        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

                        qr.add_data(url)
                        qr.make()

                        qr_code = qr.make_image(
                            image_factory=StyledPilImage,
                            module_drawer=drawers[body],
                            eye_drawer=drawers[square],
                            color_mask=SolidFillColorMask(front_color=dark_color, back_color=light_color))

                        qr_code.save(out, kind='png')

                        out.seek(0)
                        img = Image.open(out).convert('RGBA')

                        filepath_logo = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "Logos")


                        all_logos = [logos for logos in os.listdir(filepath_logo) if logos.endswith('.png')]

                        next_nameoflogo = len(all_logos) + 1
                        logo_name = f"{next_nameoflogo}.png"

                        logo_path = os.path.join(filepath_logo, logo_name)
                        with open(logo_path, 'wb') as logo_file:
                            for part in logo.chunks():
                                logo_file.write(part)

                        logo_url = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{request.user.id}", 'Logos', logo_name)

                        img_width, img_height = img.size
                        logo_max_size = img_height // 4

                        logo_img = Image.open(logo_url).convert("RGBA")

                        logo_width, logo_height = logo_img.size

                        max_side = max(logo_width, logo_height)
                        square_logo = Image.new("RGBA", (max_side, max_side), (255, 255, 255, 0))

                        x_offset = (max_side - logo_width) // 2
                        y_offset = (max_side - logo_height) // 2
                        square_logo.paste(logo_img, (x_offset, y_offset), logo_img)

                        square_logo = square_logo.resize((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)

                        box = ((img_width - logo_max_size) // 2, (img_height - logo_max_size) // 2)

                        img.paste(square_logo, box, square_logo)

                        img.save(qr_path)

                        relative_qr_path = os.path.join('media', os.path.relpath(qr_path, settings.MEDIA_ROOT))

                        context={'page': 'createqr',
                                    'logo': logo_url,
                                    'qrcode': '/' + relative_qr_path.replace("\\", "/")}

                        return render(request, 'createqr_app/createqrr.html', context=context)

                    else:
                        filepath_qr = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "QRCodes")

                        all_qrs = [qrcodes for qrcodes in os.listdir(filepath_qr) if qrcodes.endswith('.png')]

                        next_nameofqr = len(all_qrs) + 1
                        qr_name = f"{next_nameofqr}.png"

                        qr_path = os.path.join(filepath_qr, qr_name)

                        qri = QrCode.objects.create(
                            owner = profile,
                            url= url,
                            name= qr_name,
                            background_color= str(light_color),
                            color= str(dark_color),
                            body_style=body,
                            type_qr = 'commerce'
                        )


                        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

                        qr.add_data(url)
                        qr.make(fit=True)
                        qr_code = qr.make_image(
                            image_factory=StyledPilImage,
                            module_drawer=drawers[body],
                            eye_drawer=drawers[square],
                            color_mask=SolidFillColorMask(front_color=dark_color, back_color=light_color))

                        qr_code.save(str(qr_path), kind='png')

                        relative_qr_path = os.path.join('media', os.path.relpath(qr_path, settings.MEDIA_ROOT))

                        context= {'page': 'createqr',
                                    'qrcode': '/' + relative_qr_path.replace("\\", "/"),
                                    'commerce_sub': 'The QR code has been created, and will occupy a slot in the Commerce subscription'}
                else:
                    context= {'page': 'createqr', 'sub_error': 'You have reached the QR code limit!'}
                                
            else:
                context= {'page': 'createqr', 'sub_error': 'You have reached the QR code limit!'}

                return render(request, 'createqr_app/createqrr.html', context=context)
        return render(request, 'createqr_app/createqrr.html', context=context)
    else:
        return render(request, 'createqr_app/authentication_required.html',context=context)