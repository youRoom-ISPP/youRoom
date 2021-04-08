from django.db import models

# Create your models here.
class Vidas(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)