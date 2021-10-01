from django.contrib import admin

from .models import Cars, ViewedCars

# Register your models here.
admin.site.register(Cars)
admin.site.register(ViewedCars)
