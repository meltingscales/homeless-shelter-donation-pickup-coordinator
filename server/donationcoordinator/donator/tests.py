import json
import os

from django.test import TestCase

# Create your tests here.
from donationcoordinator import settings
from donator.libs import ItemList


class TestItemList(TestCase):

    def test_itemlist(self):
        # location of base datafile that dictates structure of all other files
        itemsLoc = os.path.join(settings.PROJECT_ROOT, "static/data/items.json")

        # output for donator items html
        html_out = os.path.join(settings.PROJECT_ROOT, 'static/data/_items.html')

        # output for donator items data that's stored
        items_out = os.path.join(settings.PROJECT_ROOT, 'static/data/_items_donator.json')

        print(os.path.abspath(itemsLoc))

        flat = {'bleach': 3, 'cereal': 3, 'dental dams': 3}

        itemList = ItemList(itemsLoc)  # initialize ItemsList from path

        print("List of items ready for serializing into database:")
        print(itemList.data)

        with open(items_out, 'w+') as file:
            jsondata = json.dumps(itemList.data, indent=4, sort_keys=True)
            file.write(jsondata)

        print("Form elt:")
        print(itemList.to_html())

        itemList.apply_flat_dict(flat)

        print("List of items after we apply a simulated JSON form's POST data")
        print(itemList.data)

        with open(html_out, 'w+') as file:  # open file to write test HTML
            file.write(itemList.to_html())
