# Create your models here.
from pprint import pprint

from django.contrib.auth.models import AbstractUser
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.db import models
from jsonfield import JSONField

from donationcoordinator.libs import calc_dist_p_miles
from donationcoordinator.models import Location, LocationFields
from .libs import ItemList

chicagolatlng = (41.8781, -87.6298,)


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
            data=ItemList.from_file()
        )

    def as_html(self):
        return ItemList(self.data).to_html()

    def apply_list(self, list):
        """Apply a key-value list of item:number pairs to self."""
        itemsList = ItemList(self)  # make itemsList
        newdata = itemsList.apply_flat_dict(list)

        self.data = newdata

        self.save()


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

    name = models.CharField(max_length=100)
    location = models.OneToOneField(HomeLocation, blank=True, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='homes', blank=True, null=True)
    items: Items = models.OneToOneField(Items, null=True, on_delete=models.CASCADE)  # stuff they wanna give away
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return u'/donator/my-homes/%i' % self.id

    def save(self, *args, **kwargs):  # when Home is saved

        if self.items is None:  # if no items, make default one.
            self.items = Items.default_object()

        self.location = HomeLocation.from_fields(  # unconditionally create new lat,lng from fields
            HomeLocation,
            street=self.street,
            city=self.city,
            zipCode=self.zipCode,
            state=self.state,
            country=self.country,
        )

        super().save(*args, **kwargs)

    def __str__(self):
        ret = f"[{self.pk}] {self.name} at {self.street}, {self.city}, {self.state}, {self.zipCode}."
        ret += f" Owned by {self.user.username}."

        return ret

    @staticmethod
    def get_homes_locations_near(lat=chicagolatlng[0], lng=chicagolatlng[1], radius=5) -> models.QuerySet:
        """Given `lat`, `lng`, and `radius`, return a list of dicts of

        [
            {
                'home': homes,
                'location': homeLocation,
                'distance': 1.23,
            },
            (...)
        ]

        that are within `radius` miles of `lat`,`lng`.
        """
        bpoint = Point(x=lat, y=lng)

        ret = []  # return dict

        dist = Distance(mi=radius)
        print(dist)

        # all within x miles
        homeLocations = HomeLocation.objects.filter(
            point__distance_lte=(bpoint, dist))

        homeLocation: HomeLocation
        for homeLocation in homeLocations:  # construct return dict
            homepoint = homeLocation.point

            print(bpoint)
            print(homepoint)

            dist = calc_dist_p_miles(bpoint, homepoint)

            ret.append({
                'home': homeLocation.get_home(),
                'location': homeLocation,
                'distance': dist,
            })

        pprint(ret)

        return ret
