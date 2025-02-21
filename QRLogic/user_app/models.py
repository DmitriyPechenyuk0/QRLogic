from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.CharField(max_length=255,null=False)
    subscription_expires = models.DateField()


# subscription

# 0 - without
# 1 - free
# 2 - standart
# 3 - pro   