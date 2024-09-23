from django.db import models


# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    publication = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


