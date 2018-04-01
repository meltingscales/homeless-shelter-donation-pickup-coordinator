import os

import markdown
from django.conf import settings
from django.db import models

from donationcoordinator.models import LocationFields, Location
from donator.models import User

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


class Org(LocationFields, models.Model):
    description = models.TextField(max_length=5000, blank=True, default=default_markdown)
    name = models.CharField(max_length=30, null=True, blank=True)
    location = models.OneToOneField(OrgLocation, blank=True, null=True, on_delete=models.CASCADE)

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

        self.location = OrgLocation.from_fields(  # unconditionally create new lat,lon from fields
            OrgLocation,
            street=self.street,
            city=self.city,
            zipCode=self.zipCode,
            state=self.state,
            country=self.country,
        )

        super().save(*args, **kwargs)
