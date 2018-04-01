from datetime import datetime
from pprint import pprint

from donator.models import User, Profile, Home


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
        henryUser = User.objects.create_user(
            username="henryfbp",
            email="henryfbp@gmail.com",
            password="password123",
        )

        henryProfile = Profile(
            user=henryUser,
            bio="I am Henry, the guy who made this cool site.",
            birth_date=datetime.strptime('Aug 1 1997', "%b %d %Y"),
        )
        henryProfile.save()

        henryHome1 = Home(
            user=henryUser,
            name='Condo',
            street='6060 N Ridge Ave',
            city='Chicago',
            zipCode='60660',
            state='IL',
            country='USA',
        )
        henryHome1.save()
