from django.db import models
from django.contrib.auth.models import User
from user_app.models import Profile
# Create your models here.

class QrCode(models.Model):
    expire_date = models.IntegerField()
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=200)
    color = models.CharField(max_length=255)
    background_color = models.CharField(max_length=255)
    body_style = models.IntegerField()
    frame_style = models.IntegerField()
    square_style = models.IntegerField()
    create_date = models.IntegerField()