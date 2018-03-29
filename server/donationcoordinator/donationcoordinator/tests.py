import django.db.models as models
from django.test import TestCase

from donator.models import User, Home, Profile
from datetime import datetime


class TestExample(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_users(self):
        u = User(
            username="henryfbp",
            email="henryfbp@gmail.com",
            password="password123",
        )

        print("Test user:")
        print(str(u))

        p = Profile(
            user=u,
            bio="I am Henry, the guy who made this site.",
            birth_date=datetime.now(),
        )

        print("test profile:")
        print(str(p))

        u.save()

        print("AFTER SAVING:")

        print("test profile:")
        print(str(p))

        print("Test user:")
        print(str(u))
