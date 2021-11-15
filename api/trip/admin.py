from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.TripPrice)
admin.site.register(models.Trip)
admin.site.register(models.TripLog)
