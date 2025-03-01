from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
import os, datetime
from django.http import HttpRequest
from QRLogic import settings

# Create your views here.

def render_signup(request: HttpRequest):
    context = {'page': 'signup'}
    if request.method == 'POST':
        username = request.POST.get('login')
        email = request.POST.get('email')   
        password = request.POST.get('password')  
        password_confirmation = request.POST.get('confirmpassword')
        if password == password_confirmation:
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email)
                
                user_qrs = os.path.join(settings.MEDIA_ROOT, f"{user.username}_{str(user.id)}", "QRCodes")
                user_logos = os.path.join(settings.MEDIA_ROOT, f"{user.username}_{str(user.id)}", "Logos")
                
                os.makedirs(user_qrs, exist_ok=True)
                os.makedirs(user_logos, exist_ok=True)

                Profile.objects.create(
                    user=user,
                    subscription = 'free',
                    subscription_expires=datetime.date.today() + datetime.timedelta(weeks=4)
                )

                return redirect('/user/signin/')

            except IntegrityError:
                context = {'integrity_error': True,'page': 'signup'}
        else:
            context = {'password_error': True,'page': 'signup'}
    return render(request, 'user_app/signup.html', context=context)

def render_signin(request: HttpRequest):
    context = {'page': 'signin'}
    if request.method == 'POST':
        username = request.POST.get('login')   
        password = request.POST.get('password')  

        user = authenticate(request=request, username=username, password=password)

        if user:
            login(request=request, user=user)
            return redirect('/')
        else:
            context = {'user_error': True, 'page': 'signup'}

    return render(request, 'user_app/signin.html', context=context)

def logout_render(request):

    logout(request)
    return redirect('/')



