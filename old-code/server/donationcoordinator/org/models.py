import os
from datetime import datetime

import markdown
from django.conf import settings
from django.db import models
from jsonfield import JSONField

from donationcoordinator.models import LocationFields, Location
from donator.libs import OrgItemList
from donator.models import User, Home

default_markdown_file = os.path.join(settings.PROJECT_ROOT, settings.STATICFILES_DIRS[0],
                                     'data/default_markdown.txt')
default_markdown = ''

with open(default_markdown_file, 'r') as f:
    for line in f:
        default_markdown += line + "\n"


# Create your models here.

class OrgLocation(Location):
    def get_org(self):
        """Return the `Org` that has this `OrgLocation`."""
        return Org.objects.filter(location=self)


class OrgItems(models.Model):
    data = JSONField()

    @staticmethod
    def default_object():
        return OrgItems.objects.create(
            data=OrgItemList().from_file()
        )

    def as_html(self):
        return OrgItemList(self.data).to_html()


class Org(LocationFields, models.Model):
    description = models.TextField(max_length=5000, blank=True, default=default_markdown)
    name = models.CharField(max_length=30, null=True, blank=True)
    location = models.OneToOneField(OrgLocation, blank=True, null=True, on_delete=models.CASCADE)
    items = models.OneToOneField(OrgItems, null=True, on_delete=models.CASCADE)

    def markdownify(self):
        return markdown.markdown(self.description,
                                 safe_mode='escape',
                                 extensions=[
                                     'tables',
                                     'codehilite',
                                     'smarty',
                                     'fenced_code',
                                     'toc'
                                 ],
                                 )

    def ownername(self):
        userQS = User.objects.filter(org=self)

        if len(userQS) is 0:
            return None

        user = userQS[0]  # get user from queryset
        return user.username

    def save(self, *args, **kwargs):  # when Org is saved

        if self.items is None:  # if no items, make default one.
            self.items = OrgItems.default_object()

        self.location = OrgLocation.from_fields(  # unconditionally create new lat,lng from fields
            OrgLocation,
            street=self.street,
            city=self.city,
            zipCode=self.zipCode,
            state=self.state,
            country=self.country,
        )

        super().save(*args, **kwargs)


class Route(models.Model):
    """A ``Route`` that someone goes along with a vehicle and executes ``Pickup`` events from."""
    org: Org = models.ForeignKey(Org, on_delete=models.PROTECT)
    driver: User = models.OneToOneField(User, on_delete=models.PROTECT)
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(null=True)


class Pickup(models.Model):
    """A single ``Pickup`` event occurring at a single ``Home``."""
    route = models.ForeignKey(Route, on_delete=models.PROTECT)
    home = models.ForeignKey(Home, on_delete=models.PROTECT)
    showed_up: bool = models.BooleanField(default=True)
    donator_approves: bool = models.BooleanField(default=True)
    items_promised: JSONField()
    items_taken: JSONField()
