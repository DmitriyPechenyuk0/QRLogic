"""
URL configuration for QRLogic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home_app.views import render_home_app
from contact_app.views import render_contact_app
from managesub_app.views import render_managesub_app
from yourqr_app.views import render_yourqr_app
from createqr_app.views import render_ceateqr_app, qr_redirect
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', render_home_app, name='home_app'),
    
    path('contacts/', render_contact_app, name='contact_app'),
    
    path('managesub/', render_managesub_app, name='managesub_app'),
    
    path('user/', include('user_app.urls')),

    path('myqr/', render_yourqr_app, name= 'myqr_app'),

    path("createqr/", render_ceateqr_app, name="createqr_app"),

    path('qr/<int:qr_code_id>/', qr_redirect, name='qr_redirect'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
