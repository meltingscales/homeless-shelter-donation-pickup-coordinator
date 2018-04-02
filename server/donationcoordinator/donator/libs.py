# general-purpose library functions used by ``donator`` class.

import copy
import os

from bs4 import BeautifulSoup as bs

from donationcoordinator.libs import *

default_items_json_path = r'data/items.json'
default_items_json_path = os.path.join(settings.PROJECT_ROOT, settings.STATICFILES_DIRS[0], default_items_json_path)


class ItemList:
    space_replacer = '_'  # what to replace spaces with in the HTML since CSS classes can't have spaces
    endpoint_class = 'items_list'  # to identify the input elt parents

    template = {  # template
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

    data = {  # default items list
        'root': {
            'food': {
                'slugs': 1,
                'meat': 0,
                'leaves': 3,
                'berries': 0, },
            'not food': {
                'legos': 1,
                'dirt': 0,
                'glowsticks': 1, },
        },
    }

    @staticmethod
    def apply_flat_dict_rec(d: dict, flat: dict) -> dict:
        """Recursive method. See ``apply_flat_dict()``.

        Modifies a non-flat dict, ``d``, and applies all keys contained in
        a flat dict, ``flat``.

        Example:
            a_f_d_r(
                {
                    'food': {
                        'meat': 0,
                        'cheese': 0
                        },
                    'not food': {
                        'dirt': 0,
                        'legos': 0
                        }
                },

                {'meat':1, 'cheese':3, 'dirt':1, 'legos':1}
            )

            ->
            dict is modified to now be this:

            {
                    'food': {
                        'meat': 1,
                        'cheese': 3
                        },
                    'not food': {
                        'dirt': 1,
                        'legos': 1
                        }
                },
            """

        if ItemList.is_item_dict_list(d):  # it's a list of items!
            for key in d:
                if key in flat:  # if key is in our POST
                    d[key] = flat[key]  # overwrite the number
        else:
            for key in d:
                ItemList.apply_flat_dict_rec(d[key], flat)

    @staticmethod
    @hashable_lru
    def to_html_rec(dictionary: dict):
        """Recursive method. See ``to_html()``."""
        d = copy.deepcopy(dictionary)
        ret = ''

        keys = list(d.keys())
        # print("Dict's keys:")
        # print(keys)

        for key in keys:
            elt: dict = d[key]

            ret += f'<li class="{key.replace(" ",ItemList.space_replacer)}">\n'
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
    def is_item_dict_list(dictionary: dict):
        """Given a dictionary, tell you if it's a list of numbers of items or not.

        Example:
            {
            'food': {
                'meat': 0,
                'beets': 1
                },
            'not food': {
                'legos': 3,
                'dirt': 1
                }
            }
        ->
        True


        """

        if not isinstance(dictionary, dict):
            return False

        if dictionary == {}:
            return False

        keys = list(dictionary.keys())
        for key in keys:  # i.e. 'food'
            value = dictionary[key]
            if not (isinstance(key, str) and isinstance(value, int)):
                return False

        return True

    @staticmethod
    @hashable_lru
    def dictToJSONItems(dictionary: dict):
        """Given a list of items and item categories, convert
        it into a list that has number values.

        Example:
            {'food':
                ['beef',
                'beans',
                'slugs'],
            'not food':
                ['legos',
                'dirt',
                'glowsticks']
            }

            ->

            {'food':
                {'beef': 0,
                'beans': 0,
                'slugs': 0},
            'not food':
                {'legos': 0,
                'dirt': 0,
                'glowsticks': 0}
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
                path = default_items_json_path

        with open(path, 'r') as file:
            d = json.load(file)

            return ItemList.dictToJSONItems(d)

    @staticmethod
    def itemToLI(item: str, number=0):
        """Given an item in string form, return an HTML <li> elt that
        represents that item."""
        ret = ""

        safeName = item.replace(" ", ItemList.space_replacer)  # cannot have spaces in CSS classes

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

        ret = wrap("\n" + ret, "ul", "class", ItemList.endpoint_class)

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

    def __init__(self, val=None):

        from donator.models import Items

        if val is None:  # they passed us nothing
            self.template = ItemList.from_file()
            self.data = self.template

        elif isinstance(val, str):  # they passed us a path
            self.data = ItemList.from_file(val)
            self.template = self.data

        elif isinstance(val, dict):  # it's a dict
            self.data = val

        elif isinstance(val, Items):  # it's an Items object
            self.data = val.data

    def to_html(self):
        """Turn ``self`` into an HTML form element."""
        elt = ItemList.to_html_rec(self.data)

        # elt = wrap(elt, 'ul', 'class', 'root')
        return bs(elt, 'html.parser').prettify()

    def apply_flat_dict(self, flat):
        ItemList.apply_flat_dict_rec(self.data, flat)


if __name__ == '__main__':
    itemsLoc = "../static/data/items.json"

    flat = {'bleach': 3, 'cereal': 3, 'dental dams': 3}

    itemList = ItemList(itemsLoc)  # initialize ItemsList from path

    print("List of items ready for serializing into database:")
    print(itemList.data)

    print("Form elt:")
    print(itemList.to_html())

    itemList.apply_flat_dict(flat)

    print("List of items after we apply a simulated JSON form's POST data")
    print(itemList.data)

    with open('../static/data/items_autogen.html', 'w+') as file:
        file.write(itemList.to_html())
