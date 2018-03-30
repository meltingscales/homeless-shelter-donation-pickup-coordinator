from django.db import models
import django.contrib.gis.db.models as geomodels
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.db import models
from django.db.models import Manager
from django.db.models.signals import post_save
from django.dispatch import receiver
from jsonfield import JSONField
from datetime import datetime

from . import libs

class LocationFields(models.Model):

    class Meta:
        abstract = True

    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipCode = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)


class Location(models.Model):
    """This model will be saved in a GeoDjango database."""

    class Meta:
        abstract = True

    recorded_at = models.DateTimeField(default=datetime.now)
    googlemapsjson = JSONField(default={})
    location = geomodels.PointField()

    @staticmethod
    def from_lat_lon(_class, lat, lng, data=None):
        return _class.objects.create(
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
