# general-purpose library functions used by ``donator`` class.

import copy
import os

from bs4 import BeautifulSoup as bs
from django.conf import settings

from donationcoordinator.libs import *


class ItemList:
    data = {  # default items list
        'root': {
            'food': {
                'slugs': 0,
                'meat': 0,
                'leaves': 0,
                'berries': 0, },
            'not food': {
                'legos': 0,
                'dirt': 0,
                'glowsticks': 0, },
        },
    }

    @staticmethod
    @hashable_lru
    def to_html_rec(dictionary: dict):
        """Recursive method. See ``to_html()``."""
        d = copy.deepcopy(dictionary)
        ret = ''

        keys = list(d.keys())
        # print("Dict's keys:")
        # print(keys)

        if len(keys) == 1 and keys[0] == 'root':
            ret += '<ul class="root">\n'
            elt = d[keys[0]]

            # print("we got root. its elt:")
            # print(elt)

            ret += ItemList.to_html_rec(elt) + "\n"

            ret += '</ul>' + "\n"

            return ret

        for key in keys:
            elt: dict = d[key]

            ret += f'<li class="{key}">\n'
            ret += f'<a>"{key}"</a>\n'

            ekl = list(elt.keys())

            # print("elt's keys:")
            # print(ekl)

            # keys are numbers, stop recursing
            if ekl[0] and isinstance(elt[ekl[0]], int):
                ret += ItemList.itemDictToUL(elt)

            else:
                ret += f"<ul>\n"
                ret += ItemList.to_html_rec(elt) + "\n"
                ret += f"</ul>\n"

        return ret

    @staticmethod
    @hashable_lru
    def dictToJSONItems(dictionary: dict):
        """Given a list of items and item categories, convert
        it into a list that has number values.

        Example:
            {'root':
                {'food':
                    ['beef',
                    'beans',
                    'slugs'],
                'not food':
                    ['legos',
                    'dirt',
                    'glowsticks']
                }
            }

            ->

            {'root':
                {'food':
                    {'beef': 0,
                    'beans': 0,
                    'slugs': 0},
                'not food':
                    {'legos': 0,
                    'dirt': 0,
                    'glowsticks': 0}
                }
            }"""
        ret = {}

        if isinstance(dictionary, list):
            for item in dictionary:
                ret[item] = 0

            return ret

        for item in dictionary:
            ret[item] = ItemList.dictToJSONItems(dictionary[item])

        return ret

    @staticmethod
    def from_file(path: str = None):
        """Given a JSON file's location , return an
        ItemList with all zeroes from that file."""
        if settings.configured:
            if not path:
                path = os.path.join(settings.PROJECT_ROOT, settings.STATICFILES_DIRS[0], r'data\items.json')

        with open(path, 'r') as file:
            d = json.load(file)

            return ItemList.dictToJSONItems(d)

    @staticmethod
    def itemToLI(item: str, number=0):
        """Given an item in string form, return an HTML <li> elt that
        represents that item."""
        ret = ""

        safeName = item.replace(" ", "-")  # cannot have spaces in CSS classes

        attrs = ["type", "name", "value"]
        vals = ["number", safeName, number]

        ret += wrap(item, "label") + "\n"  # add label
        ret += wrap(None, "input", attrs, vals) + "\n"  # add input elt

        ret = wrap(ret, "li", "class", safeName)  # wrap it in an <li>

        return ret

    @staticmethod
    def itemDictToUL(items: dict):
        """Given a dict of string:int items, return an HTML <ul> elt
        that represents that list of items"""

        ret = ""

        # print("itemDictToUL() passed:")
        # print(items)

        for key, val in items.items():
            ret += ItemList.itemToLI(key, val) + "\n"

        ret = wrap("\n" + ret, "ul")

        return ret

    @staticmethod
    def itemListToUL(items: list):
        """Given a list of string items, return an HTML <ul> elt that
        represents that list of items."""

        ret = ""

        for item in items:
            ret += ItemList.itemToLI(item) + "\n"

        ret = wrap("\n" + ret, "ul")

        return ret

    def __init__(self, val):
        if isinstance(val, str):  # they passed us a path
            self.data = ItemList.from_file(val)

        elif isinstance(val, dict):
            self.data = val

    def to_html(self):
        """Turn ``self`` into an HTML form element."""
        return bs(ItemList.to_html_rec(self.data), 'html.parser').prettify()


if __name__ == '__main__':
    itemsLoc = "../static/data/items.json"

    itemList = ItemList(itemsLoc)  # initialize ItemsList from path

    print("List of items ready for serializing into database:")
    print(itemList.data)

    print("Form elt:")
    print(itemList.to_html())

    with open('../static/data/items_autogen.html', 'w+') as file:
        file.write(itemList.to_html())
