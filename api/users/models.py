from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from main.models import BaseModel

# Create your models here.
class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # username = models.CharField(max_length=150)
    # id = models.IntegerField(primary_key=True,auto_created=True, verbose_name='id')
    date_of_birth = models.DateField(verbose_name='date_of_birth',blank = True)
    # email = models.EmailField(max_length=255, verbose_name="email")
    is_admin = models.BooleanField(verbose_name='is_admin', default=False,blank = True)
    dtp_times = models.IntegerField(verbose_name='dtp_times', default=0,blank = True)