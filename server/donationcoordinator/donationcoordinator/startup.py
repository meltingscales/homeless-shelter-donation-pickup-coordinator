from datetime import datetime
from pprint import pprint

from donator.models import User, Profile, Home
from org.models import Org


class Startup:
    """This class will primarily be used to create a collection of test Users, Homes, Orgs, etc. to
    set up my server for testing."""

    @staticmethod
    def delete_all_homes():
        allHomes = Home.objects.all()
        print("Deleting these homes:")
        pprint(allHomes)
        allHomes.delete()

    @staticmethod
    def delete_all_users():
        allUsers = User.objects.all()
        print("Deleting these users:")
        pprint(allUsers)
        allUsers.delete()

    @staticmethod
    def delete_all_orgs():
        allOrgs = Org.objects.all()
        print("Deleting these orgs:")
        pprint(allOrgs)
        allOrgs.delete()

    @staticmethod
    def create_test_users():
        henryOrg = Org(
            name="Habitat for Henry",
            street='3241 S Wabash Ave',
            city='Chicago',
            zipCode='60616',
            state='IL',
            country='USA',
            description="""
# HFH: Donate to me

I am a one-man org. Woohoo!

  - Markdown
  - Is
  - Cool
""",
        )

        henryOrg.save()

        henryUser = User.objects.create_user(
            username="henryfbp",
            email="henryfbp@gmail.com",
            password="password123",
            org=henryOrg,
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

        testUser = User.objects.create_user(
            username="testuser",
            email="testuser@test.testing",
            password="testpassword123",
        )
        testProfile = Profile(
            user=testUser,
            bio="I am a test user! Hi!",
            birth_date=datetime.now(),
        )
        testUser.save()

        testUserHome = Home(
            user=testUser,
            name='my test home',
            street='3530 S Wolcott Ave',
            city='Chicago',
            zipCode='60609',
            state='IL',
            country='USA',
        )
        testUserHome.save()
