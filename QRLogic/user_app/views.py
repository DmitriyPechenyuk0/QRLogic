from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
import os, datetime
from django.http import HttpRequest
from QRLogic import settings

# Create your views here.
# Creating render function to signup page. | Створення функції рендерингу для сторінки signup.
def render_signup(request: HttpRequest):
    # Passes the page name to the context. | Передається в context назва сторінки.
    context = {'page': 'signup'}
    # Checking the method with which the request was sent. | Перевірка на те з яким методом надійшов запит.
    if request.method == 'POST':
        # Creating variables by retrieving data from the request. | Створення зміних з отримуванням даних з запиту.
        username = request.POST.get('login')
        email = request.POST.get('email')   
        password = request.POST.get('password')  
        password_confirmation = request.POST.get('confirmpassword')
        # Checking if the passwords match. | Перевірка на те чи однакові паролі.
        if password == password_confirmation:
            try:
                # Creating a new user in the database. | Створення нового користувача у базі даних.
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email)
                # Merging the path to a separate "QRCodes" folder for each user. | Об'єднання путі до окремої папки QRCodes для кожного користувача.
                user_qrs = os.path.join(settings.MEDIA_ROOT, f"{user.username}_{str(user.id)}", "QRCodes")
                # Merging the path to a separate "Logos" folder for each user. | Об'єднання путі до окремої папки Logos для кожного користувача.
                user_logos = os.path.join(settings.MEDIA_ROOT, f"{user.username}_{str(user.id)}", "Logos")
                # Creating folders. | Створення папок.
                os.makedirs(user_qrs, exist_ok=True)
                os.makedirs(user_logos, exist_ok=True)
                # Creating a profile for the user. | Створення профілю для користувача.
                Profile.objects.create(
                    user=user,
                    subscription = 'free',
                    subscription_expires=datetime.date.today() + datetime.timedelta(weeks=4)
                )
                # Redirecting the user to the login page. | Переадресація користувача на сторінку авторизації.
                return redirect('/user/signin/')
            # Checking for the IntegrityError. | Перевірка на IntegrityError.
            except IntegrityError:
                # It is passed to the context that the check was successful. | Передаєтся у context те що перевірка спрацювала.
                context = {'integrity_error': True,'page': 'signup'}
        # If the passwords do not match. | Якшо паролі не співпали.
        else:
            # It is passed to the context that the check was successful. | Передаєтся у context те що перевірка спрацювала.
            context = {'password_error': True,'page': 'signup'}
    # Display the signup page to the user. | Відображаємо сторінку signup користувачу.
    return render(request, 'user_app/signup.html', context=context)

# Creating render function to signin page. | Створення функції рендерингу для сторінки signin.
def render_signin(request: HttpRequest):
    # Passes the page name to the context. | Передається в context назва сторінки.
    context = {'page': 'signin'}
    # Checking the method with which the request was sent. | Перевірка на те з яким методом надійшов запит.
    if request.method == 'POST':
        # Creating variables by retrieving data from the request. | Створення зміних з отримуванням даних з запиту.
        username = request.POST.get('login')   
        password = request.POST.get('password')  
        # Checking if a user is registered with such data. | Перевірка на те чи зареєстрований користувач з такими даними.
        user = authenticate(request=request, username=username, password=password)
        # If an account with the user's data is found in the database. | Якщо за даними користувача знайшовся аккаунт у базі даних.
        if user:
            # User authentication into the account. | Авторизація користувача в аккаунт.
            login(request=request, user=user)
            # Redirecting the user to the homepage. | Переадресація користувача на головну сторінку.
            return redirect('/')
        # If no account with the user's data is found in the database. | Якщо за даними користувача не знайшлось аккаунту у базі даних.
        else:
            # Passes the error to the context. | Передаємо у context помилку
            context = {'user_error': True, 'page': 'signup'}
    # Display the page to the user. | Відображаємо сторінку користувачу
    return render(request, 'user_app/signin.html', context=context)
# Creating a function for logging the user out of the account. | Створення функції для виходу користувача з аккаунту
def logout_render(request):
    # Logout | Вихід з системи
    logout(request)
    # Redirecting the user to the homepage. | Переадресація користувача на головну сторінку.
    return redirect('/')



