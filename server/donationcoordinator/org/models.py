import markdown
from django.db import models

# Create your models here.
from donator.models import User


class Org(models.Model):
    bio = models.TextField(max_length=500, blank=True)
    name = models.TextField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def markdownify(self):
        return markdown.markdown(self.bio, safe_mode='escape')

    def ownername(self):
        user = User.objects.filter(org=self)
        print(user)
        if len(user) is 0:
            return None
        return user.username
