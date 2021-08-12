from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='id')
    date_of_birth = models.DateField(verbose_name='date_of_birth')
    email = models.CharField(max_length=255, verbose_name="email")
    is_admin = models.BooleanField(verbose_name='is_admin', default=False)
    dtp_times = models.IntegerField(verbose_name='dtp_times', default=0)


