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
                'pro': 100,
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
                        # Adding data to the QR code. | Додаємо дані до QR коду.
                        qr.add_data(qr_link)
                        # Creating the QR code. | Створення QR коду.
                        qr.make()
                        # Modifying the QR code. | Модіфікуємо qr код.
                        qr_code = qr.make_image(
                            image_factory=StyledPilImage,
                            module_drawer=drawers[body],
                            eye_drawer=drawers[square],
                            color_mask=SolidFillColorMask(front_color=dark_color, back_color=light_color))
                        # Storing the QR code in a memory object. | Зберігання qr коду у об'єкт пам'яті.
                        qr_code.save(out, kind='png')
                        out.seek(0)
                        # Opening the image. | Відкриваємо зображення. 
                        img = Image.open(out).convert('RGBA')
                        # Saving the path to the user's 'Logos' folder in a variable. | Зберігаємо у змінну шлях до папки 'Logos' користувача.
                        filepath_logo = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "Logos")
                        # Counting the number of logo images for the user. | Підраховуємо кількість картинок-логотипів користувача.
                        all_logos = [logos for logos in os.listdir(filepath_logo) if logos.endswith('.png')]
                        # Calculating the next logo name. | Вираховуємо наступну назву лого.
                        next_nameoflogo = len(all_logos) + 1
                        # Saving the file name of the logo. | Зберігаємо назву файлу логотипу.
                        logo_name = f"{next_nameoflogo}.png"
                        # Saving the path to the logo. | Зберігаємо шлях до логотипу.
                        logo_path = os.path.join(filepath_logo, logo_name)
                        # Saving the logo. | Зберігаємо лого.
                        with open(logo_path, 'wb') as logo_file:
                            for part in logo.chunks():
                                logo_file.write(part)
                        # Saving the path from the media folder to the logo. | Зберігаємо шлях від папки media до логотипу.
                        logo_url = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{request.user.id}", 'Logos', logo_name)
                        # Saving the height and width variables of the image. | Зберігаємо змінні висоти та ширини зображення.
                        img_width, img_height = img.size
                        # Saving the logo size. | Зберігаємо розмір логотипу.
                        logo_max_size = img_height // 4
                        # Opening the logo image. | Відкриваємо зображення лого.
                        logo_img = Image.open(logo_url).convert("RGBA")
                        # Saving the logo's height and width data into variables. | Зберігаємо у змінні висоти та ширини логотипу дані.
                        logo_width, logo_height = logo_img.size
                        # Taking the maximum value. | Беремо максимальне значення.
                        max_side = max(logo_width, logo_height)
                        # Creating a new layer. | Створюємо новий шар.
                        square_logo = Image.new("RGBA", (max_side, max_side), (255, 255, 255, 0))
                        # Calculating the horizontal offset to center the logo horizontally. | Обчислюємо горизонтальний зсув для центрування логотипу по горизонталі.
                        x_offset = (max_side - logo_width) // 2
                        # Calculating the vertical offset to center the logo vertically. | Обчислюємо вертикальний зсув для центрування логотипу по вертикалі.
                        y_offset = (max_side - logo_height) // 2
                        # Inserting the logo image (logo_img) onto a new layer of the image. | Вставляємо зображення логотипу (logo_img) на новий шар зображення.
                        square_logo.paste(logo_img, (x_offset, y_offset), logo_img)
                        # Resizing the square image to the specified maximum size. | Змінюємо розмір квадратного зображення до заданого максимального розміру.
                        square_logo = square_logo.resize((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
                        # Calculating the coordinates of the top-left corner for inserting the square logo. | Обчислюємо координати верхнього лівого кута для вставки квадратного логотипу.
                        box = ((img_width - logo_max_size) // 2, (img_height - logo_max_size) // 2)
                        # Inserting a square logo image. | Вставляємо квадратне зображення логотипу.
                        img.paste(square_logo, box, square_logo)
                        # Saving the image. | Зберігаємо зображення.
                        img.save(qr_path)
                        # Creating a relative path to the QR code. | Ствоюємо відносний шлях до qr коду.
                        relative_qr_path = os.path.join('media', os.path.relpath(qr_path, settings.MEDIA_ROOT))
                        # Passing data to the template. | Передаємо дані до шаблону .
                        context={'page': 'createqr',
                                    'logo': logo_url,
                                    'qrcode': '/' + relative_qr_path.replace("\\", "/")}
                        # Display the createqr page to the user. | Відображаємо сторінку createqr користувачу.
                        return render(request, 'createqr_app/createqrr.html', context=context)
                    # The condition "else". | Умова "інакше". 
                    else:
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
                        # Creating a QR code image. | Створення зображення QR коду.
                        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
                        # Creating an absolute link to a page using Django's URL handler. | Створення абсолютного посилання на сторінку, використовуючи URL-обробник Django.
                        qr_link = request.build_absolute_uri(reverse('qr_redirect', args=[qri.id]))
                        # Adding data to the QR code. | Додаємо дані до QR коду.
                        qr.add_data(qr_link)
                        # Creating the QR code. | Створення QR коду.
                        qr.make(fit=True)
                        # Modifying the QR code. | Модіфікуємо qr код.
                        qr_code = qr.make_image(
                            image_factory=StyledPilImage,
                            module_drawer=drawers[body],
                            eye_drawer=drawers[square],
                            color_mask=SolidFillColorMask(front_color=dark_color, back_color=light_color))
                        # Saving the QR code. | Зберігання qr коду.
                        qr_code.save(str(qr_path), kind='png')
                        # Creating a relative path to the QR code. | Ствоюємо відносний шлях до qr коду.
                        relative_qr_path = os.path.join('media', os.path.relpath(qr_path, settings.MEDIA_ROOT))
                        # Saving all QR codes to a variable, filtered by date from the most recent to the oldest. | Зберігаємо до змінної усі qr коди з фільтром за датою від останнього до першого.
                        qrio = QrCode.objects.filter(owner=request.user.profile, type_qr = 'standart').order_by('-create_date')
                        # Rewriting the variable with the last object from the filter. | Перезаписуємо змінну на останній об'єкт з фільтру
                        qrio = qrio[0]
                        # Passing data to the template. | Передаємо дані до шаблону.
                        context= {'page': 'createqr',
                                    'qrcode': '/' + relative_qr_path.replace("\\", "/"),
                                    'qrio': qrio,
                                    'profile': profile}
                # The condition "else". | Умова "інакше".
                else:
                    # Passing the error to the template. | Передаємо до шаблону помилку.
                    context= {'page': 'createqr',
                              'sub_error': 'You have reached the QR code limit!'}
            # Checking if the user has a Commerce subscription and if what they entered in the field is not a link. | Перевірка на те чи користувач має підписку Commerce та чи те що він ввін у поле не є посиланням.
            elif request.user.profile.commerce == True and not any(key in url for key in keywords):
                # Saving the number of the user's cells into a variable. | Отримуємо у змінну кількість комірок користувача.
                count_of_cells = request.user.profile.commerce_cells
                # Saving the number of QR code objects with the type "commerce" from the database into a variable. | Отримуємо у змінну кількість об'єктів qr кодів з бази з типом "commerce".
                qr_codess = QrCode.objects.filter(owner=request.user.profile, type_qr = 'commerce').count()
                # Checking if the user has any available cells. | Перевірка на те чи є вільні комірки у користувача
                if count_of_cells > qr_codess:
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
                            type_qr = 'commerce'
                        )
                        # Creating an object in memory. | Створення об'єкту у пам'яті.
                        out = io.BytesIO()
                        # Creating a QR code image. | Створення зображення QR коду.
                        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
                        # Adding data to the QR code. | Додаємо дані до QR коду.
                        qr.add_data(url)
                        # Creating the QR code. | Створення QR коду.
                        qr.make()
                        # Modifying the QR code. | Модіфікуємо qr код.
                        qr_code = qr.make_image(
                            image_factory=StyledPilImage,
                            module_drawer=drawers[body],
                            eye_drawer=drawers[square],
                            color_mask=SolidFillColorMask(front_color=dark_color, back_color=light_color))
                        # Storing the QR code in a memory object. | Зберігання qr коду у об'єкт пам'яті.
                        qr_code.save(out, kind='png')
                        out.seek(0)
                        # Opening the image. | Відкриваємо зображення. 
                        img = Image.open(out).convert('RGBA')
                        # Saving the path to the user's 'Logos' folder in a variable. | Зберігаємо у змінну шлях до папки 'Logos' користувача. 
                        filepath_logo = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{str(request.user.id)}", "Logos")
                        # Counting the number of logo images for the user. | Підраховуємо кількість картинок-логотипів користувача.
                        all_logos = [logos for logos in os.listdir(filepath_logo) if logos.endswith('.png')]
                        # Calculating the next logo name. | Вираховуємо наступну назву лого.
                        next_nameoflogo = len(all_logos) + 1
                        # Saving the file name of the logo. | Зберігаємо назву файлу логотипу.
                        logo_name = f"{next_nameoflogo}.png"
                        # Saving the path to the logo. | Зберігаємо шлях до логотипу. 
                        logo_path = os.path.join(filepath_logo, logo_name)
                        # Saving the logo. | Зберігаємо лого.
                        with open(logo_path, 'wb') as logo_file:
                            for part in logo.chunks():
                                logo_file.write(part)
                        # Saving the path from the media folder to the logo. | Зберігаємо шлях від папки media до логотипу.
                        logo_url = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{request.user.id}", 'Logos', logo_name)
                        # Saving the height and width variables of the image. | Зберігаємо змінні висоти та ширини зображення.
                        img_width, img_height = img.size
                        # Saving the logo size. | Зберігаємо розмір логотипу.
                        logo_max_size = img_height // 4
                        # Opening the logo image. | Відкриваємо зображення лого.
                        logo_img = Image.open(logo_url).convert("RGBA")
                        # Saving the logo's height and width data into variables. | Зберігаємо у змінні висоти та ширини логотипу дані.
                        logo_width, logo_height = logo_img.size
                        # Taking the maximum value. | Беремо максимальне значення.
                        max_side = max(logo_width, logo_height)
                        # Creating a new layer. | Створюємо новий шар. 
                        square_logo = Image.new("RGBA", (max_side, max_side), (255, 255, 255, 0))
                        # Calculating the horizontal offset to center the logo horizontally. | Обчислюємо горизонтальний зсув для центрування логотипу по горизонталі.
                        x_offset = (max_side - logo_width) // 2
                        # Calculating the vertical offset to center the logo vertically. | Обчислюємо вертикальний зсув для центрування логотипу по вертикалі.
                        y_offset = (max_side - logo_height) // 2
                        # Inserting the logo image (logo_img) onto a new layer of the image. | Вставляємо зображення логотипу (logo_img) на новий шар зображення. 
                        square_logo.paste(logo_img, (x_offset, y_offset), logo_img)
                        # Resizing the square image to the specified maximum size. | Змінюємо розмір квадратного зображення до заданого максимального розміру.
                        square_logo = square_logo.resize((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
                        # Calculating the coordinates of the top-left corner for inserting the square logo. | Обчислюємо координати верхнього лівого кута для вставки квадратного логотипу. 
                        box = ((img_width - logo_max_size) // 2, (img_height - logo_max_size) // 2)
                        # Inserting a square logo image. | Вставляємо квадратне зображення логотипу.
                        img.paste(square_logo, box, square_logo)
                        # Saving the image. | Зберігаємо зображення. 
                        img.save(qr_path)
                        # Creating a relative path to the QR code. | Ствоюємо відносний шлях до qr коду.
                        relative_qr_path = os.path.join('media', os.path.relpath(qr_path, settings.MEDIA_ROOT))
                        # Passing data to the template. | Передаємо дані до шаблону .
                        context={'page': 'createqr',
                                    'logo': logo_url,
                                    'qrcode': '/' + relative_qr_path.replace("\\", "/")}
                        # Display the createqr page to the user. | Відображаємо сторінку createqr користувачу. 
                        return render(request, 'createqr_app/createqrr.html', context=context)
                    # The condition "else". | Умова "інакше". 
                    else:
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
                            type_qr = 'commerce'
                        )
                        # Creating a QR code image. | Створення зображення QR коду. 
                        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
                        # Adding data to the QR code. | Додаємо дані до QR коду. 
                        qr.add_data(url)
                        # Creating the QR code. | Створення QR коду.
                        qr.make(fit=True)
                        # Modifying the QR code. | Модіфікуємо qr код.
                        qr_code = qr.make_image(
                            image_factory=StyledPilImage,
                            module_drawer=drawers[body],
                            eye_drawer=drawers[square],
                            color_mask=SolidFillColorMask(front_color=dark_color, back_color=light_color))
                        # Saving the QR code. | Зберігання qr коду.
                        qr_code.save(str(qr_path), kind='png')
                        # Creating a relative path to the QR code. | Ствоюємо відносний шлях до qr коду.
                        relative_qr_path = os.path.join('media', os.path.relpath(qr_path, settings.MEDIA_ROOT))
                        # Saving all QR codes to a variable, filtered by date from the most recent to the oldest. | Зберігаємо до змінної усі qr коди з фільтром за датою від останнього до першого.
                        qrio = QrCode.objects.filter(owner=request.user.profile, type_qr = 'commerce').order_by('-create_date')
                        # Rewriting the variable with the last object from the filter. | Перезаписуємо змінну на останній об'єкт з фільтру
                        qrio = qrio[0]
                        # Passing data to the template. | Передаємо дані до шаблону.
                        context= {'page': 'createqr',
                                    'qrcode': '/' + relative_qr_path.replace("\\", "/"),
                                    'commerce_sub': 'The QR code has been created, and will occupy a slot in the Commerce subscription',
                                    'qrio': qrio,
                                    'profile': profile}
                # The condition "else". | Умова "інакше".
                else:
                    # Passing the error to the template. | Передаємо до шаблону помилку.
                    context= {'page': 'createqr', 'sub_error': 'You have reached the QR code limit!'}
            # The condition "else". | Умова "інакше". 
            else:
                # Passing the error to the template. | Передаємо до шаблону помилку. 
                context= {'page': 'createqr', 'sub_error': 'You have reached the QR code limit!'}

                # Display the createqr page to the user. | Відображаємо сторінку createqr користувачу.
                return render(request, 'createqr_app/createqrr.html', context=context)
        # Display the createqr page to the user. | Відображаємо сторінку createqr користувачу. 
        return render(request, 'createqr_app/createqrr.html', context=context)
    # The condition "else". | Умова "інакше". 
    else:
        # Display the auth_required page to the user. | Відображаємо сторінку auth_required користувачу.
        return render(request, 'createqr_app/authentication_required.html',context=context)