from django.urls import path, include
from yourqr_app.views import render_yourqr_app

urlpatterns= [
    path('yourqr/', render_yourqr_app, name= 'yourqr_app'),
]