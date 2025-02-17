from createqr_app.views import render_ceateqr_app
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path("/create", render_ceateqr_app, name="createqr_app")
]


