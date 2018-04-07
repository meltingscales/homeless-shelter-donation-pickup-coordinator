from datetime import datetime
from pprint import pprint

from donator.models import User, Profile, Home, Items
from org.models import Org
from .libs import islist, istuple


class Startup:
    """This class will primarily be used to create a collection of test Users, Homes, Orgs, etc. to
    set up my server for testing."""

    @staticmethod
    def delete_all_objects(*args):
        """Delete all objects of an ORM class, or list of classes."""

        if (islist(args) or istuple(args)) and len(args) > 1:
            for aclass in list(args):
                Startup.delete_all_objects(aclass)

        else:
            cls = args[0]
            allclsobjects = cls.objects.all()
            print(f"Deleting these '{cls.__name__}'s:")
            pprint(allclsobjects)
            allclsobjects.delete()

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
        henryUser.save()

        henryProfile = Profile(
            user=henryUser,
            bio="I am Henry, the guy who made this cool site.",
            birth_date=datetime.strptime('Aug 1 1997', "%b %d %Y"),
        )
        henryProfile.save()

        henryItems: Items = Items.default_object()

        henryItems.apply_list({  # add some items
            'toilet paper': 3,
            'lettuce': 4,
            'bleach': 10,
        })

        henryItems.save()

        henryHome1 = Home(
            user=henryUser,
            name='Condo',
            street='6060 N Ridge Ave',
            city='Chicago',
            zipCode='60660',
            state='IL',
            country='USA',
            items=henryItems,
        )
        henryHome1.save()

        testuserorg = Org(
            name="Habitat for Test",
            street='1634 W Warren Blvd',
            city='Chicago',
            zipCode='60612',
            state='IL',
            country='USA',
            description="""
        # Test User's Org

        > I am a one-man org. Woohoo!

        """,
        )
        testuserorg.save()

        testUser = User.objects.create_user(
            username="testuser",
            email="testuser@test.testing",
            password="testpassword123",
            org=testuserorg,
        )
        testUser.save()

        testProfile = Profile(
            user=testUser,
            bio="I am a test user! Hi!",
            birth_date=datetime.now(),

        )
        testProfile.save()

        testitems: Items = Items.default_object()

        testitems.apply_list({  # add some items
            'lettuce': 4,
            'eggplant': 200,
        })

        testitems.save()


        testUserHome = Home(
            user=testUser,
            name='my test home',
            street='3530 S Wolcott Ave',
            city='Chicago',
            zipCode='60609',
            state='IL',
            country='USA',
            items=testitems,
        )
        testUserHome.save()
