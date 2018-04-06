import os

from django.test import TestCase

# Create your tests here.
from donationcoordinator import settings
from donator.libs import ItemList


class TestItemList(TestCase):

    def test_itemlist(self):
        itemsLoc = os.path.join(settings.PROJECT_ROOT, "static/data/items.json")
        htmlloc = os.path.join(settings.PROJECT_ROOT, 'static/data/items_autogen.html')

        print(os.path.abspath(itemsLoc))

        flat = {'bleach': 3, 'cereal': 3, 'dental dams': 3}

        itemList = ItemList(itemsLoc)  # initialize ItemsList from path

        print("List of items ready for serializing into database:")
        print(itemList.data)

        print("Form elt:")
        print(itemList.to_html())

        itemList.apply_flat_dict(flat)

        print("List of items after we apply a simulated JSON form's POST data")
        print(itemList.data)

        with open(htmlloc, 'w+') as file:  # open file to write test HTML
            file.write(itemList.to_html())
