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
            bio="I am Henry, the guy who made this cool site.",
            birth_date=datetime.strptime('Aug 1 1997', "%b %d %Y"),
        )

        u.save()
