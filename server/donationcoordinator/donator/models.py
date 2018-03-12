# Create your models here.

from django.contrib.auth.models import User
from django.db import models


class Items(models.Model):
    pass


class Home(models.Model):
    """
    One of a ``User``'s (possibly) many ``Home``s.

    For example, I (Henry) live on-campus and at my condo.
    I can have two ``Home``s that I have different ``Items`` in,
    since my condo and dorm have different stuff I can give away.

    One ``Home`` has one ``Items``...since you can only have one 'pile of stuff to give away' per house...normally.
    """
    name = models.TextField()
    street = models.TextField()
    city = models.TextField()
    zipCode = models.TextField()
    state = models.TextField()
    country = models.TextField()
    image = models.ImageField(upload_to='homes', blank=True, null=True)
    items = models.ForeignKey(Items, null=True, on_delete=models.PROTECT)  # stuff they wanna give away
    user = models.ForeignKey(User, default=1, on_delete=models.PROTECT)
