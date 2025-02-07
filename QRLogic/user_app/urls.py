from user_app.views import render_signin, render_signup, logout_render
from django.urls import path, include

urlpatterns= [
    path('signup/', render_signup, name= 'signup'),
    path('signin/', render_signin, name='signin'),
    path('logout/', logout_render, name='logout')
    
]