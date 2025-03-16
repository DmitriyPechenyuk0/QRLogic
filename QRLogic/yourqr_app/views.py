from django.shortcuts import render, get_object_or_404
from createqr_app.models import QrCode
import datetime,os
from user_app.models import Profile
from QRLogic import settings
from django.http import HttpRequest
# Create your views here.

# Creating render function to myqr page. | Створення функції рендерингу для сторінки myqr.
def render_yourqr_app(request: HttpRequest):
    # Passes the page name to the context. | Передається в context назва сторінки. 
    context = {'page': 'myqr'}
    # Creating variables to obtain the user's profile object and all of their QR codes. | Створюємо змінні з отримання об'єкту профілю користувача, та усіх його qr кодів 
    profile = Profile.objects.get(user=request.user)
    qrcodess = QrCode.objects.filter(owner=request.user.profile)
    qrcodes = QrCode.objects.filter(owner=profile).order_by('-create_date')
    # Iterating through the list of qrcodes. | Перебираємо список qrcodess
    for qr in qrcodess:
        # Condition "if" the expiration date of the QR code has not passed. | Умова "якщо" строк придатності qr коду не вийшов
        if qr.expire_date < datetime.datetime.now():
            # Передаємо до щаблону усі qr коди
            context = {'page': 'myqr', 'qrcodes': qrcodess}
    # Checking the method with which the request was sent. | Перевірка на те з яким методом надійшов запит та чи є delete_qr у цьому запиті.
    if request.method == "POST" and "delete_qr" in request.POST:
        # Check whether the request method is correct and if "delete_qr" is present in the request. | Створення змінної з отримуванням даних з запиту.
        qr_id = request.POST.get("delete_qr")
        # Create a variable where we will store the object or a 404 error if the object is not found. | Створюємо змінну у яку запишемо об'єкт чи помилку 404 якщо не має об'єкту
        qr = get_object_or_404(QrCode, id=qr_id, owner__user=request.user)
        # Merging the path to the user's QR code folder and the QR code name. | Об'єднання шляху папки QR кодів користувача та назви QR коду.
        file_path = os.path.join(settings.MEDIA_ROOT, f"{request.user.username}_{request.user.id}", qr.name)
        # Condition: "if" the file exists. | Умова: "якщо" файл існує
        if os.path.exists(file_path):
            # Delete the file. | Видаляємо файл
            os.remove(file_path)
        # Delete the object in DB. | Видаляємо об'єкт у БД 
        qr.delete()

    # Checking the method with which the request was sent. | Перевірка на те з яким методом надійшов запит.
    if request.method == "POST":
        # Creating variable by retrieving data from the request. | Створення змінної з отримуванням даних з запиту.
        date_filter = request.POST.get('date_filter')
        # Condition: "if" date_filter is not empty. | Умова: "якщо" date_filter не є пустим
        if date_filter:  
                # Creating a variable that converts the date defined by the user in the filters. | Створення змінної що конвертує дату визначену користувачем у фільтрах
                selected_date = datetime.datetime.strptime(date_filter, "%Y-%m-%d").date()
                # Creating a variable that filters QR codes by the date specified by the user in the filters. | Створення змінної що фільтрує qr коди за датою яку визначив користувач у фільтрах
                qrcodes = qrcodes.filter(create_date__date=selected_date)


    # Creating variable by retrieving data from the request. | Створення змінної з отримуванням даних з запиту.
    url_filter = request.POST.get('url_filter')
    # Condition: if url_filter is not empty. | Умова: якщо url_filter не є пустим
    if url_filter:
        # This line filters qrcodes, keeping only those records where the url field contains the substring from url_filter. | Цей рядок фільтрує qrcodes, залишаючи лише ті записи, де поле url містить підрядок з url_filter
        qrcodes = qrcodes.filter(url__icontains=url_filter)
    # Creating a variable with a list type. | Створення змінної з типом список
    qr_images = []
    # Iterating through the list of qrcodes. | Перебираємо список qrcodess
    for qr in qrcodes:
        # Creating a variable with the path to the QR code image. | Створюємо змінну з значенням шляху до зображення qr коду
        image_url = f"{settings.MEDIA_URL}{request.user.username}_{request.user.id}/{qr.name}"  
        # Adding the QR code data to the list. | Додаємо до списку данні qr коду
        qr_images.append({
            'name': qr.name,
            'image_url': image_url,
            'url': qr.url,
            'date': qr.create_date
        })
    # Passing data to the template. | Передаємо дані до шаблону.
    context = {
        'page': 'myqr',
        'qrcodes': qrcodes,
        'qr_images': qr_images
    }
    # Checking if the user is registered. | Перевірка на те чи зареєстрований користувач. 
    if request.user.is_authenticated:
        # Display the myqr page to the user. | Відображаємо сторінку myqr користувачу. 
        return render(request, 'yourqr_app/yourqrr.html', context=context)
    # The condition "else". | Умова "інакше".  
    else:
        # Display the auth_required page to the user. | Відображаємо сторінку auth_required користувачу.
        return render(request, 'createqr_app/authentication_required.html', context=context)
