from django.db import models


# Create your models here.
class Org(models.Model):
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    name = models.TextField(max_length=30, null=True, blank=True)
