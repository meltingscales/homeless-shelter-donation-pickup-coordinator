# Create your models here.

from datetime import datetime

import django.contrib.gis.db.models as geomodels
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.geos import Point
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from jsonfield import JSONField

from . import libs


class User(AbstractUser):
    test = models.CharField(max_length=50, blank=True)
    org = models.OneToOneField('org.Org', null=True, blank=True, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


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
    recorded_at = models.DateTimeField(default=datetime.now)
    googlemapsjson = JSONField(default={})
    location = geomodels.PointField()

    @staticmethod
    def from_lat_lon(lat, lng, data=None):
        return HomeLocation.objects.create(
            location=Point(x=lat, y=lng),
            googlemapsjson=data,
        )

    def to_lat_lon(self):
        return {
            'lat': self.location.x,
            'lon': self.location.y,
        }

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def to_google_maps_uri(self):
        d = self.to_lat_lon()

        return f"https://www.google.com/maps/search/?api=1&query={d['lat']},{d['lon']}"

    def to_google_maps_iframe(self):
        d = self.to_lat_lon()
        key = settings.GEOPOSITION_GOOGLE_MAPS_API_KEY

        ret = ''
        src = f'https://www.google.com/maps/embed/v1/place?key={key}&q={d["lat"]},{d["lon"]}'

        ret = libs.wrap(ret, 'iframe', ['src'], [src])

        return ret


class HomeManager(models.Manager):
    def create_home(self, name, street, city, zipCode, state, country, location, image, items, user):
        home = Home(name, street, city, zipCode, state, country, location, image, items, user)

        return home


class Home(models.Model):
    """
    One of a ``User`` 's (possibly) many ``Home`` s.

    For example, I (Henry) live on-campus and at my condo.
    I can have two ``Home`` s that I have different ``Items`` in,
    since my condo and dorm have different stuff I can give away.

    One ``Home`` has one ``Items`` ...since you can only have one 'pile of stuff to give away' per house...normally.
    """
    objects = HomeManager()

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

        super().save(*args, **kwargs)

    def __str__(self):
        ret = f"[{self.pk}] {self.name} at {self.street}, {self.city}, {self.state}, {self.zipCode}."
        ret += f" Owned by {self.user.username}."

        return ret
