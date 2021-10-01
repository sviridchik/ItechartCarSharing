import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db import models
from main.models import BaseModel


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(verbose_name='date_of_birth', blank=True)
    is_admin = models.BooleanField(verbose_name='is_admin', default=False, blank=True)
    dtp_times = models.IntegerField(verbose_name='dtp_times', default=0, blank=True)
