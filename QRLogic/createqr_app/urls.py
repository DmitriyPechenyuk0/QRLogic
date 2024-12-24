from createqr_app.views import render_ceateqr_app
from django.urls import path, include

urlpatterns=[
    path("/create", render_ceateqr_app, name="createqr_app")
]