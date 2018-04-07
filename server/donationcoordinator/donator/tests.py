import json
import os

from django.test import TestCase

# Create your tests here.
from donationcoordinator import settings
from donator.libs import ItemList, OrgItemList


class TestItemList(TestCase):
    # location of base datafile that dictates structure of all other files
    items_location = os.path.join(settings.PROJECT_ROOT, "static/data/items.json")
    # output for donator items html
    html_output = os.path.join(settings.PROJECT_ROOT, 'static/data/_items.html')
    # output for donator items data that's stored
    items_output = os.path.join(settings.PROJECT_ROOT, 'static/data/_items_donator.json')

    def test_itemlist(self):
        print(os.path.abspath(self.items_location))

        flat = {'bleach': 3, 'cereal': 3, 'dental dams': 3}

        itemList = ItemList(self.items_location)  # initialize ItemsList from path

        print("List of items ready for serializing into database:")
        print(itemList.data)

        with open(self.items_output, 'w+') as file:
            jsondata = json.dumps(itemList.data, indent=4, sort_keys=True)
            file.write(jsondata)

        print("Form elt:")
        print(itemList.to_html())

        itemList.apply_flat_dict(flat)

        print("List of items after we apply a simulated JSON form's POST data")
        print(itemList.data)

        with open(self.html_output, 'w+') as file:  # open file to write test HTML
            file.write(itemList.to_html())


class TestOrgItemList(TestCase):
    # location of base datafile that dictates structure of all other files
    items_location = os.path.join(settings.PROJECT_ROOT, "static/data/items.json")
    # output for org items html
    html_output = os.path.join(settings.PROJECT_ROOT, 'static/data/_items_org.html')
    # output for org items data that's stored
    items_output = os.path.join(settings.PROJECT_ROOT, 'static/data/_items_org.json')

    def test_orgitemlist(self):
        print(os.path.abspath(self.items_location))

        flat = {'bleach': 3, 'cereal': 3, 'dental dams': 3}

        org_items_list = OrgItemList(self.items_location)  # initialize ItemsList from path

        print("List of items ready for serializing into database:")
        print(org_items_list.data)

        with open(self.items_output, 'w+') as file:
            jsondata = json.dumps(org_items_list.data, indent=4, sort_keys=True)
            file.write(jsondata)

        print("Form elt:")
        print(org_items_list.to_html())

        org_items_list.apply_flat_dict(flat)

        print("List of items after we apply a simulated JSON form's POST data")
        print(org_items_list.data)

        with open(self.html_output, 'w+') as file:  # open file to write test HTML
            file.write(org_items_list.to_html())
