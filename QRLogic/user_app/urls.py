from user_app.views import render_reg
from user_app.views import render_auth
from django.urls import path, include

urlpatterns= [
    path('signup/', render_reg, name= 'user_app'),
    path('login/', render_auth, name='user_app')
]