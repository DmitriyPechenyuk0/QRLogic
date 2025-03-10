from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Creating a model. | Створення моделі
class Profile(models.Model):
    # Creating a relationship between the Profile and User models. | Створюємо зв'язок між моделями Profile та User.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Creating a field where the user's monthly subscription will be stored. | Створюємо поле у якому буде зберігатися щомісячна підписка користувача.
    subscription = models.CharField(max_length=255,null=False)
    # Creating a field where the subscription expiration date will be specified. | Створюємо поле у якому буде вказуватися срок придатності підписки.
    subscription_expires = models.DateTimeField()
    # Creating a field where the status of the user's commercial subscription will be stored. | Створюємо поле у якому буде зберігатися статус коммерсійної підписки користувача.
    commerce = models.BooleanField(default=False)
    # Creating a field where the number of spots for commercial QR codes will be stored. | Створюємо поле у якому буде зберігатися кількість місць під комерсійні QR коди.
    commerce_cells = models.IntegerField(default=20)
    # Creating a "magic function." | Створюємо "магічну функцію".
    def __str__(self):
        # Return the user's username. | Повертаємо юзернейм користувача.
        return self.user.username
    
