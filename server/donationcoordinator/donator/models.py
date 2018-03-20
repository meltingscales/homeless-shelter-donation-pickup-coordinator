# Create your models here.

from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField
import django.contrib.gis.db.models as geomodels

from . import libs


class Items(models.Model):
    """
    A list of goods such as clothing, food, toiletries.
    This list belongs to a single ``Home``.
    """
    data = JSONField()

    @staticmethod
    def default_object():
        return Items.objects.create(
            data=libs.ItemList.from_file()
        )

    def as_html(self):
        return libs.ItemList(self.data).to_html()


class HomeLocation(models.Model):
    """This model will be saved in a GeoDjango database."""
    recorded_at = models.DateTimeField()
    location = geomodels.PointField()


class Home(models.Model):
    """
    One of a ``User`` 's (possibly) many ``Home`` s.

    For example, I (Henry) live on-campus and at my condo.
    I can have two ``Home`` s that I have different ``Items`` in,
    since my condo and dorm have different stuff I can give away.

    One ``Home`` has one ``Items`` ...since you can only have one 'pile of stuff to give away' per house...normally.
    """
    name = models.TextField()
    street = models.TextField()
    city = models.TextField()
    zipCode = models.TextField()
    state = models.TextField()
    country = models.TextField()
    location = models.OneToOneField(HomeLocation, blank=True, null=True, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='homes', blank=True, null=True)
    items: Items = models.OneToOneField(Items, null=True, on_delete=models.PROTECT)  # stuff they wanna give away
    user: User = models.ForeignKey(User, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return u'/donator/my-homes/%i' % self.id

    def save(self, *args, **kwargs):
        if self.items is None:
            self.items = Items.default_object()

        return super().save(*args, **kwargs)

    def __str__(self):
        ret = f"{self.name} at {self.street}, {self.city}, {self.state}, {self.zipCode}."
        ret += f" Owned by {self.user.username}."

        return ret
