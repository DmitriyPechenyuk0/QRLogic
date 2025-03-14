from django.db import models
from django.contrib.auth.models import User
from user_app.models import Profile
from django.utils.timezone import now
# Create your models here.

# Creating a model. | Створення моделі
class QrCode(models.Model):
    # Створюємо поле у якому буде зберігатись дата прострочення QR коду
    expire_date = models.DateTimeField(null=True, blank=True)
    # Створюємо поле у якому буде зберігатись дата створення QR коду
    create_date = models.DateTimeField(null=True, blank=True)
    # Creating a relationship between the QrCode and Profile models. | Створюємо зв'язок між моделями QrCode та Profile.
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE)
    # Створюємо поле у якому буде зберігатись назва QR коду
    name = models.CharField(max_length=255, null=True)
    # Створюємо поле у якому буде зберігатись url до якого веде QR код
    url = models.URLField(max_length=255, null=True)
    # Створюємо поле у якому буде зберігатись колір тіла QR коду
    color = models.CharField(max_length=255, null=True, blank=True)
    # Створюємо поле у якому буде зберігатись колір підложки QR коду
    background_color = models.CharField(max_length=255, null=True, blank=True)
    # Створюємо поле у якому буде зберігатись стиль квадратів у центрі QR коду
    body_style = models.CharField(max_length=255 ,null=True, blank=True)
    # Створюємо поле у якому буде зберігатись стиль квадратів по кутах QR коду
    square_style = models.CharField(max_length=255 ,null=True, blank=True)
    # Створюємо поле у якому буде зберігатись тип QR коду (Комерсійні / стандартні)
    type_qr = models.CharField(max_length=255,null=True, blank=True)
    # Створюємо метод за допомогою якого будемо визначати чи не прострочився QR код
    def expired(self):
        return self.expire_date and now().date() > self.expire_date
    # Перезаписуємо "магічний" метод __str__ щоб коректніше відображались об'єкти
    def __str__(self):
        return f'{self.owner.user.username}_{self.pk}'