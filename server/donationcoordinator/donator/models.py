# Create your models here.

from datetime import datetime

import django.contrib.gis.db.models as geomodels
from django.conf import settings
from donationcoordinator.models import Location, LocationFields
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.db import models
from django.db.models import Manager
from django.db.models.signals import post_save
from django.dispatch import receiver
from jsonfield import JSONField

from . import libs

chicagolatlon = (41.8781, -87.6298,)


class User(AbstractUser):
    test = models.CharField(max_length=50, blank=True)
    org = models.OneToOneField('org.Org', null=True, blank=True, on_delete=models.CASCADE)

    def org_or_none(self):
        # print(f"org_or_none on {self.username}")
        try:
            return self.org
        except Exception as e:
            print(e)
            return None

    def __str__(self, o=True):
        ret = ''

        ret += f'[{self.pk}] : {self.username}'

        org = self.org_or_none()

        if org:
            ret += f' owns Org {org.name}.'

        return ret


class Profile(models.Model):
    objects = models.Manager

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

    def __str__(self):
        s = f"Profile of user f{str(self.user)}. Preview of bio:"

        b = str(self.bio)
        upper = 100
        if len(b) < upper:
            upper = len(b)

        s += "'" + b[0:upper] + "'"

        return s


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


class HomeLocation(Location):
    def get_home(self):
        """Return the `Home` that has this `HomeLocation`."""
        return Home.objects.filter(location=self)


class HomeManager(models.Manager):
    def create_home(self, name, street, city, zipCode, state, country, location, image, items, user):
        home = Home(name, street, city, zipCode, state, country, location, image, items, user)

        return home


class Home(LocationFields, models.Model):
    """
    One of a ``User`` 's (possibly) many ``Home`` s.

    For example, I (Henry) live on-campus and at my condo.
    I can have two ``Home`` s that I have different ``Items`` in,
    since my condo and dorm have different stuff I can give away.

    One ``Home`` has one ``Items`` ...since you can only have one 'pile of stuff to give away' per house...normally.
    """
    objects = HomeManager()

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

    @staticmethod
    def get_homes_locations_near(lat=chicagolatlon[0], lon=chicagolatlon[1], radius=5) -> models.QuerySet:
        """Given `lat`, `lon`, and `radius`, return a list of dicts of

        [
            {
                'home': homes,
                'location': homeLocation,
                'distance': 1.23,
            },
            (...)
        ]

        that are within `radius` miles of `lat`,`lon`.
        """
        bpoint = Point(x=lat, y=lon)

        ret = []  # return dict

        # all within x miles
        homeLocations = HomeLocation.objects.filter(location__distance_lt=(bpoint, Distance(mi=radius)))

        homeLocation: HomeLocation
        for homeLocation in homeLocations:  # construct return dict
            homepoint = homeLocation.location

            dist = bpoint.distance(homepoint)

            ret.append({
                'home': homeLocation.get_home(),
                'location': homeLocation,
                'distance': dist,
            })

        return ret
