from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.CharField(max_length=255,null=False)
    subscription_expires = models.DateTimeField()
    commerce = models.BooleanField(default=False)
    commerce_cells = models.IntegerField(default=20)

    def __str__(self):
        return self.user.username
    
