from django.db import models

# Create your models here.
class Apartment(models.Model):
    apartament_id = models.TextField(default="", unique=True)
    place = models.TextField(default="")
    description = models.TextField(default="")
    price = models.FloatField(default=0.0)
    area = models.FloatField(default=0.0)
    price_per_m = models.FloatField(default=0.0)
    rooms = models.TextField(default="")
    offer_url = models.TextField(default="")

    def __str__(self):
        return f"{self.place}, {self.area}"

class FavoriteApartment(models.Model):
    apartament = models.ForeignKey(
        Apartment, to_field="apartament_id", on_delete=models.CASCADE)
    def __str__(self):
        return self.apartment.place