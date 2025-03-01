from django.db import models
from django.contrib.auth.models import User
from user_app.models import Profile
from django.utils.timezone import now
# Create your models here.

class QrCode(models.Model):
    expire_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    url = models.URLField(max_length=255, null=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    background_color = models.CharField(max_length=255, null=True, blank=True)
    body_style = models.CharField(max_length=255 ,null=True, blank=True)
    frame_style = models.CharField(max_length=255 , null=True, blank=True)    
    square_style = models.CharField(max_length=255 ,null=True, blank=True)
    type_qr = models.CharField(max_length=255,null=True, blank=True)

    def expired(self):
        return self.expire_date and now().date() > self.expire_date
    
    def __str__(self):
        return f'{self.owner.user.username}_{self.pk}'