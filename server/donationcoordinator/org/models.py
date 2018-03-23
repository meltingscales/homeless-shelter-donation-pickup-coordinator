import markdown
from django.db import models

# Create your models here.
from donator.models import User


class Org(models.Model):
    description = models.TextField(max_length=500, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)

    def markdownify(self):
        return markdown.markdown(self.description, safe_mode='escape')

    def ownername(self):
        userQS = User.objects.filter(org=self)

        if len(userQS) is 0:
            return None
        
        user = userQS[0]  # get user from queryset
        return user.username
