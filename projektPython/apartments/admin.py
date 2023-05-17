from django.contrib import admin
from apartments import models
# Register your models here.

admin.site.register(models.Apartment)
admin.site.register(models.FavoriteApartment)