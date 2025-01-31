from django.db import models
from django.contrib.auth.models import User
import segno
import os
from io import BytesIO
from django.core.files.base import ContentFile
# Create your models here.


class QrCode(models.Model):
    expire_date = models.IntegerField()
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=200)
    color = models.CharField(max_length=255)
    background_color = models.CharField(max_length=255)
    body_style = models.IntegerField()
    frame_style = models.IntegerField()
    square_style = models.IntegerField()
    create_date = models.IntegerField()


def save(request):
        if request.method == 'POST':
            url = request.POST.get('url')
            qr = segno.make_qr(
                content=url)
            qr.save(out = os.path.abspath(__file__ + f'/../../media/qrcode.png', kind='png'))

    





