from datetime import datetime

from django.test import TestCase

from donator.models import User, Profile


class TestExample(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_can_do_math(self):
        one = 1
        alsoone = 1
        shouldbetwo = one + alsoone

        self.assertEqual(one + alsoone, shouldbetwo)

    def test_create_users(self):
        u = User(
            username="henryfbp",
            email="henryfbp@gmail.com",
            password="password123",
        )
        u.save()

        p = Profile(
            user=u,
            bio="I am Henry, the guy who made this site.",
            birth_date=datetime.now(),
        )

        p.save()

        print("test profile:")
        print(str(p))

        print("Test user:")
        print(str(u))
