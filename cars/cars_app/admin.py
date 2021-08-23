from django.contrib import admin

# Register your models here.
from cars_app import models

admin.site.register(models.Cars)
admin.site.register(models.ViewedCars)
