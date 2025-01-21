from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def render_signup(request):
    context = {'page': 'signup'}
    if request.method == 'POST':
        username = request.POST.get('login')
        email = request.POST.get('email')   
        password = request.POST.get('password')  
        try:
            User.objects.create_user(username=username,  password=password, email=email)
            return redirect('/user/signin/')

        except IntegrityError:
            context = {'integrity_error': True}
    return render(request, 'user_app/signup.html', context=context)

def render_signin(request):
    context = {'page': 'signin'}
    if request.method == 'POST':
        username = request.POST.get('login')   
        password = request.POST.get('password')  
        password_confirmation = request.POST.get('confirmpassword')

        if password == password_confirmation:
            
            user = authenticate(request=request, username=username, password=password)

            if user:
                login(request=request, user=user)
                print("loginning")
                return redirect('/')
            else:
                context = {'user_error': True}

    return render(request, 'user_app/signin.html', context=context)

def logout_render(request):

    logout(request)
    return redirect('/')



