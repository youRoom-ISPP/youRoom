from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0, validators=[MinValueValidator(50)])
    numVidas = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)
