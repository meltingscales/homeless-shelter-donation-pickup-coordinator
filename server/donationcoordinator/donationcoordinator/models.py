from datetime import datetime

import django.contrib.gis.db.models as geomodels
from django.conf import settings
from django.contrib.gis.geos import Point
from django.db import models
from jsonfield import JSONField

from donationcoordinator.libs import GoogleMapsClient
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
    point = geomodels.PointField()

    @staticmethod
    def from_lat_lon(_class, lat, lng, data=None):
        return _class.objects.create(
            point=Point(x=lat, y=lng),
            googlemapsjson=data,
        )

    @staticmethod
    def from_fields(_class, **kwargs):
        locString = ','.join(list(dict(kwargs).values()))

        geo_result = GoogleMapsClient.lat_lon(locString)
        geo_result = geo_result[0]  # just use 1st one

        return _class.from_lat_lon(
            _class,
            lat=geo_result[0],
            lng=geo_result[1],
        )

    def to_lat_lon(self):
        return {
            'lat': self.point.x,
            'lon': self.point.y,
        }

    def lat(self):
        return self.point.x

    def lon(self):
        return self.point.y

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
