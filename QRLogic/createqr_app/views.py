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

# Creating a function that converts a hex to an RGB color. | Створення функції яка конвертує хеш до ргб кольору.
def hex_to_rgb(hex_color):
    # Remove the "#" symbol from the beginning of the string. | Видаляємо символ # з початку рядку.
    hex_color = hex_color.lstrip("#")
    # Return a tuple of three integers. | Повертаємо кортеж з трьох цілих чисел.
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
# Creating a function for monthly QR codes that will redirect the user to the page they specified. | Створення функції для щомісячних qr кодів яка буде переадресовувати користувача на ту сторінку яку він вказав.
def qr_redirect(request, qr_code_id):
    # We store in a variable the object by unique identifier or an error if not found. | Записуємо у змінну об'єкт за унікальним ідентифікатором або помилку якщо не знаходить.
    qr_code = get_object_or_404(QrCode, id=qr_code_id)
    # Checking if the QR code is valid. | Перевірка на те чи дійсний qr код.
    if timezone.now() < qr_code.expire_date:
        # We redirect the user to the URL specified by the user. | Переадресовуємо користувача на юрл який вказував користувач.
        return redirect(qr_code.url)
    # If the QR code is invalid. | Якщо QR код не дійсний.
    else:
        # Display the error "Not found." | Виводимо помилку "Не знайдено".
        return Http404('QR code was expired')
# Creating render function to createqr page. | Створення функції рендерингу для сторінки createqr.
def render_ceateqr_app(request: HttpRequest):
    # Passes the page name to the context. | Передається в context назва сторінки.
    context = {'page': 'createqr'}
    # Creating an array with key phrases by which the link will be recognized. | Створюємо массив з ключовими фраза по яким буде розпізнаватися посилання.
    keywords = [
    "https://", "http://", ".com", ".org", ".net", ".info", ".biz", ".pro",
    ".us", ".uk", ".ru", ".de", ".fr", ".it", ".es", ".cn",
    ".jp", ".br", ".in", ".ca", ".au", ".eu", ".asia",
    ".africa", ".lat", ".scot", ".cat", ".tech", ".app",
    ".dev", ".store", ".blog", ".news", ".xyz"
    ]
    # Checking if the user is registered. | Перевірка на те чи зареєстрований користувач.
    if request.user.is_authenticated:
        # Checking the method with which the request was sent. | Перевірка на те з яким методом надійшов запит.
        if request.method == 'POST':
            # Creating a variable where the user's current monthly subscription will be stored. | Створюємо змінну де буде зберігатися поточна щомісячна підписка користувача.
            sub = request.user.profile.subscription
            # Creating a dictionary with subscription types and their limitations. | Створюємо словник з типом підписок та їх обмеженнями.
            subs_type = {
                'free': 1,
                'standart':10,
                'pro': 50,
            }
            # Creating a variable where the user's current profile will be stored. | Створюємо змінну де буде зберігатися поточний профіль користувача.
            profile = Profile.objects.get(user = request.user)
            # Creating variables by retrieving data from the request. | Створення зміних з отримуванням даних з запиту.
            url = request.POST.get('url')
            # Checking if the input provided by the user is a valid link. | Перевірка на те чи є силкою те що ввів користувач у поле введення.
            if any(key in url for key in keywords):
                # Store in a variable the number of QR codes created under the monthly subscription. | Зберігаємо у змінну кількість створених QR кодів що створені за щомісячною підпискою.
                qr_count = QrCode.objects.filter(owner=request.user.profile, type_qr = 'standart').count()
                # Checking if the user has not exceeded the limits of their subscription. | Перевірка на те чи не вийшов користувач за ліміти своєї підписки.
                if qr_count < subs_type[sub]:
                    # Creating variables by retrieving data from the request. | Створення зміних з отримуванням даних з запиту.
                    light_color= request.POST.get('light-color')
                    dark_color = request.POST.get('dark-color')
                    # Converting hex colors to RGB tuples. | Перетворюємо хеш кольори у ргб кортежі.
                    light_color= hex_to_rgb(light_color)
                    dark_color = hex_to_rgb(dark_color)
                    # Creating variables by retrieving data from the request. | Створення зміних з отримуванням даних з запиту.
                    logo = request.FILES.get("upload")
                    # Creating variables that define the expiration period of the QR code. | Создание переменных которые отвечают за срок действия QR кода.
                    today = datetime.datetime.today()
                    expire = today + datetime.timedelta(days=30)
                    # Creating variables by retrieving data from the request. | Створення зміних з отримуванням даних з запиту.
                    scale = request.POST.get('sizeqr')
                    body = request.POST.get('body')
                    square = request.POST.get('squares')
                    # Creating a dictionary with the names of the QR code "modules." | Створення словнику з назвами "модулів" QR коду.
                    drawers = { 'rounded': RoundedModuleDrawer(),
                                'square': SquareModuleDrawer(),
                                'circle': CircleModuleDrawer(),
                                'gapped': GappedSquareModuleDrawer(),
                                'horizontal': HorizontalBarsDrawer(),
                                'vertical': VerticalBarsDrawer()}
                    # Checking if the user is creating a QR code with a logo. | Перевірка на те чи користувач створює QR код з логотипом.
                    if logo:
                        # Creating the path to the folder where the user's QR codes are stored. | Створення шляху до папки де зберігаються QR коди користувача.
                        filepath_qr = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "QRCodes")
                        # Store in a variable the number of images in the user's QR code folder. | Зберігаємо у змінну кількість зображень у теці qr кодів користувача.
                        all_qrs = [qrcodes for qrcodes in os.listdir(filepath_qr) if qrcodes.endswith('.png')]
                        # Storing the current QR code number in a variable. | Зберігання у змінну номер поточного QR коду.
                        next_nameofqr = len(all_qrs) + 1
                        # Storing the current QR code name in a variable. | Зберігання у змінну назву поточного QR коду.
                        qr_name = f"{next_nameofqr}.png"
                        # Merging the path to the user's QR code folder and the QR code name. | Об'єднання шляху папки QR кодів користувача та назви QR коду.
                        qr_path = os.path.join(filepath_qr, qr_name)
                        # Creating a record in the database about the creation of a QR code. | Створення запису у базі даних про створення QR коду.
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
                        # Creating an object in memory. | Створення об'єкту у пам'яті.
                        out = io.BytesIO()
                        # Creating a QR code image. | Створення зображення QR коду.
                        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
                        # Creating an absolute link to a page using Django's URL handler. | Створення абсолютного посилання на сторінку, використовуючи URL-обробник Django.
                        qr_link = request.build_absolute_uri(reverse('qr_redirect', args=[qri.id]))
                        # Adding data to the QR code. | Додаємо дані до QR коду
                        qr.add_data(qr_link)
                        # Створення QR коду
                        qr.make()
                        # Модіфікуємо qr код
                        qr_code = qr.make_image(
                            image_factory=StyledPilImage,
                            module_drawer=drawers[body],
                            eye_drawer=drawers[square],
                            color_mask=SolidFillColorMask(front_color=dark_color, back_color=light_color))
                        # Зберігання qr коду у об'єкт пам'яті
                        qr_code.save(out, kind='png')
                        out.seek(0)
                        # Відкриваємо зображення 
                        img = Image.open(out).convert('RGBA')
                        # Зберігаємо у змінну шлях до папки 'Logos' користувача 
                        filepath_logo = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "Logos")
                        # Підраховуємо кількість картинок-логотипів користувача
                        all_logos = [logos for logos in os.listdir(filepath_logo) if logos.endswith('.png')]
                        # Вираховуємо наступну назву лого
                        next_nameoflogo = len(all_logos) + 1
                        # Зберігаємо назву файлу логотипу 
                        logo_name = f"{next_nameoflogo}.png"
                        # Зберігаємо шлях до логотипу
                        logo_path = os.path.join(filepath_logo, logo_name)
                        # Зберігаємо лого
                        with open(logo_path, 'wb') as logo_file:
                            for part in logo.chunks():
                                logo_file.write(part)
                        # Зберігаємо шлях від папки media до логотипу
                        logo_url = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{request.user.id}", 'Logos', logo_name)
                        # Зберігаємо змінні висоти та ширини зображення
                        img_width, img_height = img.size
                        # зберігаємо розмір логотипу
                        logo_max_size = img_height // 4
                        # Відкриваємо зображення
                        logo_img = Image.open(logo_url).convert("RGBA")
                        # Зберігаємо у 
                        logo_width, logo_height = logo_img.size
                        # 
                        max_side = max(logo_width, logo_height)
                        # 
                        square_logo = Image.new("RGBA", (max_side, max_side), (255, 255, 255, 0))
                        # 
                        x_offset = (max_side - logo_width) // 2
                        # 
                        y_offset = (max_side - logo_height) // 2
                        # 
                        square_logo.paste(logo_img, (x_offset, y_offset), logo_img)
                        # 
                        square_logo = square_logo.resize((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
                        # 
                        box = ((img_width - logo_max_size) // 2, (img_height - logo_max_size) // 2)
                        # 
                        img.paste(square_logo, box, square_logo)
                        # 
                        img.save(qr_path)
                        # 
                        relative_qr_path = os.path.join('media', os.path.relpath(qr_path, settings.MEDIA_ROOT))
                        # Передаємо до дані шаблону 
                        context={'page': 'createqr',
                                    'logo': logo_url,
                                    'qrcode': '/' + relative_qr_path.replace("\\", "/")}
                        # 
                        return render(request, 'createqr_app/createqrr.html', context=context)
                    # 
                    else:
                        # 
                        filepath_qr = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "QRCodes")
                        # 
                        all_qrs = [qrcodes for qrcodes in os.listdir(filepath_qr) if qrcodes.endswith('.png')]
                        # 
                        next_nameofqr = len(all_qrs) + 1
                        # 
                        qr_name = f"{next_nameofqr}.png"
                        # 
                        qr_path = os.path.join(filepath_qr, qr_name)
                        # 
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
                        # 
                        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
                        # 
                        qr_link = request.build_absolute_uri(reverse('qr_redirect', args=[qri.id]))
                        # 
                        qr.add_data(qr_link)
                        qr.make(fit=True)
                        # 
                        qr_code = qr.make_image(
                            image_factory=StyledPilImage,
                            module_drawer=drawers[body],
                            eye_drawer=drawers[square],
                            color_mask=SolidFillColorMask(front_color=dark_color, back_color=light_color))
                        # 
                        qr_code.save(str(qr_path), kind='png')
                        # 
                        relative_qr_path = os.path.join('media', os.path.relpath(qr_path, settings.MEDIA_ROOT))
                        # 
                        qrio = QrCode.objects.filter(owner=request.user.profile, type_qr = 'standart').order_by('-create_date')
                        qrio = qrio[0]
                        # 
                        context= {'page': 'createqr',
                                    'qrcode': '/' + relative_qr_path.replace("\\", "/"),
                                    'qrio': qrio,
                                    'profile': profile}
                # 
                else:
                    # 
                    context= {'page': 'createqr',
                              'sub_error': 'You have reached the QR code limit!'}
            # 
            elif request.user.profile.commerce == True and not any(key in url for key in keywords):
                # 
                count_of_cells = request.user.profile.commerce_cells
                # 
                qr_codess = QrCode.objects.filter(owner=request.user.profile, type_qr = 'commerce').count()
                # 
                if count_of_cells > qr_codess:
                    # 
                    light_color= request.POST.get('light-color')
                    dark_color = request.POST.get('dark-color')
                    # 
                    light_color= hex_to_rgb(light_color)
                    dark_color = hex_to_rgb(dark_color)
                    # 
                    logo = request.FILES.get("upload")
                    # 
                    today = datetime.datetime.today()
                    expire = today + datetime.timedelta(days=30)
                    # 
                    scale = request.POST.get('sizeqr')
                    body = request.POST.get('body')
                    square = request.POST.get('squares')
                    # 
                    drawers = { 'rounded': RoundedModuleDrawer(),
                                'square': SquareModuleDrawer(),
                                'circle': CircleModuleDrawer(),
                                'gapped': GappedSquareModuleDrawer(),
                                'horizontal': HorizontalBarsDrawer(),
                                'vertical': VerticalBarsDrawer()}
                    # 
                    if logo:
                        # 
                        filepath_qr = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "QRCodes")
                        # 
                        all_qrs = [qrcodes for qrcodes in os.listdir(filepath_qr) if qrcodes.endswith('.png')]
                        # 
                        next_nameofqr = len(all_qrs) + 1
                        # 
                        qr_name = f"{next_nameofqr}.png"
                        # 
                        qr_path = os.path.join(filepath_qr, qr_name)
                        # 
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
                        # 
                        out = io.BytesIO()
                        # 
                        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
                        # 
                        qr.add_data(url)
                        # 
                        qr.make()
                        # 
                        qr_code = qr.make_image(
                            image_factory=StyledPilImage,
                            module_drawer=drawers[body],
                            eye_drawer=drawers[square],
                            color_mask=SolidFillColorMask(front_color=dark_color, back_color=light_color))
                        # 
                        qr_code.save(out, kind='png')
                        # 
                        out.seek(0)
                        # 
                        img = Image.open(out).convert('RGBA')
                        # 
                        filepath_logo = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "Logos")
                        # 
                        all_logos = [logos for logos in os.listdir(filepath_logo) if logos.endswith('.png')]
                        # 
                        next_nameoflogo = len(all_logos) + 1
                        # 
                        logo_name = f"{next_nameoflogo}.png"
                        # 
                        logo_path = os.path.join(filepath_logo, logo_name)
                        # 
                        with open(logo_path, 'wb') as logo_file:
                            for part in logo.chunks():
                                logo_file.write(part)
                        # 
                        logo_url = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{request.user.id}", 'Logos', logo_name)
                        # 
                        img_width, img_height = img.size
                        # 
                        logo_max_size = img_height // 4
                        # 
                        logo_img = Image.open(logo_url).convert("RGBA")
                        # 
                        logo_width, logo_height = logo_img.size
                        # 
                        max_side = max(logo_width, logo_height)
                        # 
                        square_logo = Image.new("RGBA", (max_side, max_side), (255, 255, 255, 0))
                        # 
                        x_offset = (max_side - logo_width) // 2
                        # 
                        y_offset = (max_side - logo_height) // 2
                        # 
                        square_logo.paste(logo_img, (x_offset, y_offset), logo_img)
                        # 
                        square_logo = square_logo.resize((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
                        # 
                        box = ((img_width - logo_max_size) // 2, (img_height - logo_max_size) // 2)
                        # 
                        img.paste(square_logo, box, square_logo)
                        # 
                        img.save(qr_path)
                        # 
                        relative_qr_path = os.path.join('media', os.path.relpath(qr_path, settings.MEDIA_ROOT))
                        # 
                        context={'page': 'createqr',
                                    'logo': logo_url,
                                    'qrcode': '/' + relative_qr_path.replace("\\", "/")}
                        # 
                        return render(request, 'createqr_app/createqrr.html', context=context)
                    # 
                    else:
                        # 
                        filepath_qr = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "QRCodes")
                        # 
                        all_qrs = [qrcodes for qrcodes in os.listdir(filepath_qr) if qrcodes.endswith('.png')]
                        # 
                        next_nameofqr = len(all_qrs) + 1
                        # 
                        qr_name = f"{next_nameofqr}.png"
                        # 
                        qr_path = os.path.join(filepath_qr, qr_name)
                        # 
                        qri = QrCode.objects.create(
                            owner = profile,
                            url= url,
                            name= qr_name,
                            background_color= str(light_color),
                            color= str(dark_color),
                            body_style=body,
                            type_qr = 'commerce'
                        )
                        # 
                        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
                        # 
                        qr.add_data(url)
                        # 
                        qr.make(fit=True)
                        # 
                        qr_code = qr.make_image(
                            image_factory=StyledPilImage,
                            module_drawer=drawers[body],
                            eye_drawer=drawers[square],
                            color_mask=SolidFillColorMask(front_color=dark_color, back_color=light_color))
                        # 
                        qr_code.save(str(qr_path), kind='png')
                        # 
                        relative_qr_path = os.path.join('media', os.path.relpath(qr_path, settings.MEDIA_ROOT))
                        # 
                        qrio = QrCode.objects.filter(owner=request.user.profile, type_qr = 'commerce').order_by('-create_date')
                        qrio = qrio[0]
                        
                        # 
                        context= {'page': 'createqr',
                                    'qrcode': '/' + relative_qr_path.replace("\\", "/"),
                                    'commerce_sub': 'The QR code has been created, and will occupy a slot in the Commerce subscription',
                                    'qrio': qrio,
                                    'profile': profile}
                # 
                else:
                    # 
                    context= {'page': 'createqr', 'sub_error': 'You have reached the QR code limit!'}
            # 
            else:
                # 
                context= {'page': 'createqr', 'sub_error': 'You have reached the QR code limit!'}

                # 
                return render(request, 'createqr_app/createqrr.html', context=context)
        # 
        return render(request, 'createqr_app/createqrr.html', context=context)
    # 
    else:
        # 
        return render(request, 'createqr_app/authentication_required.html',context=context)