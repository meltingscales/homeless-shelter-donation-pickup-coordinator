from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_org = models.BooleanField(default=False)
    is_donator = models.BooleanField(default=False)