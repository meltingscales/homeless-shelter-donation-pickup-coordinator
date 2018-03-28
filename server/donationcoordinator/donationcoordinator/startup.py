from datetime import datetime

from donator.models import User, Profile


class Startup:
    def create_test_users(self):
        u = User(
            username="henryfbp",
            email="henryfbp@gmail.com",
            password="password123",
        )

        p = Profile(
            user=u,
            bio="I am Henry, the guy who made this site.",
            birth_date=datetime.now(),
        )

        u.save()
