from datetime import datetime
from pprint import pprint

from donator.models import User, Profile


class Startup:
    """This class will primarily be used to create a collection of test Users, Homes, Orgs, etc. to
    set up my server for testing."""

    @staticmethod
    def delete_all_users():
        allUsers = User.objects.all()
        print("Deleting these users:")
        pprint(allUsers)
        allUsers.delete()

    @staticmethod
    def create_test_users():
        u = User.objects.create_user(
            username="henryfbp",
            email="henryfbp@gmail.com",
            password="password123",
        )

        u.save()

        p = Profile(
            user=u,
            bio="I am Henry, the guy who made this cool site.",
            birth_date=datetime.strptime('Aug 1 1997', "%b %d %Y"),
        )

        p.save()

        print(u)
