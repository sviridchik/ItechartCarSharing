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
