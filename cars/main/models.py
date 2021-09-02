import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.TimeField(auto_now_add=True, blank=True)
    updated_at = models.TimeField(auto_now=True, blank=True)


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # username = models.CharField(max_length=150)
    id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='id')
    date_of_birth = models.DateField(verbose_name='date_of_birth')
    email = models.EmailField(max_length=255, verbose_name="email")
    is_admin = models.BooleanField(verbose_name='is_admin', default=False)
    dtp_times = models.IntegerField(verbose_name='dtp_times', default=0)
