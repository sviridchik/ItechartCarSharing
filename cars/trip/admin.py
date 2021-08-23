from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.TripLog)
admin.site.register(models.TripPrice)
admin.site.register(models.Trip)