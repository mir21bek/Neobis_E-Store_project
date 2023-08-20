from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    email = models.EmailField('email address', unique=True)
    activation_token = models.CharField(max_length=255, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Emails'
        verbose_name_plural = 'Email'


class Profile(models.Model):
    profile_user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    city = models.CharField(verbose_name='Город Проживание', max_length=50)
    street = models.CharField(verbose_name='Название улицы', max_length=120)
    house = models.PositiveIntegerField(verbose_name='Номер дома', max_length=5)
    phone_number = models.CharField(verbose_name='Телефон номер', max_length=16)
