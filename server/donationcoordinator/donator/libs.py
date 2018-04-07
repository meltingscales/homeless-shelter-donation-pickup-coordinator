# general-purpose library functions used by ``donator`` class.

import copy
import json
import os

from bs4 import BeautifulSoup as bs
from django.conf import settings

from donationcoordinator.libs import wrap

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

    def flatten_dict(self, d: dict):
        """Modifies a non-flat dict, ``d``, and flattens it.
                Example:
            f_d({
                    'food': {
                        'meat': 0,
                        'cheese': 0
                        },
                    'not food': {
                        'dirt': 0,
                        'legos': 0
                        }
                })
                ->
                {'meat':1, 'cheese':3, 'dirt':1, 'legos':1}
            )

        """
        for key, val in d.items():
            print(key)
            print(val)

    def apply_flat_dict_rec(self, d: dict, flat: dict) -> dict:
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

        if self.is_item_dict_list(d):  # it's a list of items!
            for key in d:
                if key in flat:  # if key is in our POST
                    d[key] = flat[key]  # overwrite the number
        else:
            for key in d:
                self.apply_flat_dict_rec(d[key], flat)

    def to_html_rec(self, dictionary: dict):
        """Recursive method. See ``to_html()``."""
        d = copy.deepcopy(dictionary)
        ret = ''

        keys = list(d.keys())
        # print("Dict's keys:")
        # print(keys)

        for key in keys:
            elt: dict = d[key]

            ret += f'<li class="{key.replace(" ",ItemList.space_replacer)}">'
            ret += wrap(key, "a")

            ekl = list(elt.keys())

            # print("elt's keys:")
            # print(ekl)

            # keys are numbers, stop recursing
            if ekl[0] and isinstance(elt[ekl[0]], int):
                ret += self.itemDictToUL(elt)

            else:
                ret += wrap(self.to_html_rec(elt), 'ul')

        return ret

    def is_item_dict_list(self, dictionary: dict):
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

    def dictToJSONItems(self, dictionary: dict):
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
            ret[item] = self.dictToJSONItems(dictionary[item])

        return ret

    def from_file(self, path: str = None):
        """Given a JSON file's location , return an
        ItemList with all zeroes from that file."""
        if settings.configured:
            if not path:
                path = default_items_json_path

        with open(path, 'r') as file:
            d = json.load(file)

            return self.dictToJSONItems(d)

    def itemToLI(self, item: str, number=0):
        """Given an item in string form, return an HTML <li> elt that
        represents that item."""
        ret = ""

        safeName = item.replace(" ", self.space_replacer)  # cannot have spaces in CSS classes

        attrs = ["type", "name", "value"]
        vals = ["number", safeName, number]

        ret += wrap(item, "label")  # add label
        ret += wrap(None, "input", attrs, vals)  # add input elt

        ret = wrap(ret, "li", "class", safeName)  # wrap it in an <li>

        return ret

    def itemDictToUL(self, items: dict):
        """Given a dict of string:int items, return an HTML <ul> elt
        that represents that list of items"""

        ret = ""

        # print("itemDictToUL() passed:")
        # print(items)

        for key, val in items.items():
            ret += self.itemToLI(key, val)

        ret = wrap(ret, "ul", "class", self.endpoint_class)

        return ret

    def itemListToUL(self, items: list):
        """Given a list of string items, return an HTML <ul> elt that
        represents that list of items."""

        ret = ""

        for item in items:
            ret += self.itemToLI(item)

        ret = wrap(ret, "ul")

        return ret

    def __init__(self, val=None):

        from donator.models import Items

        if val is None:  # they passed us nothing
            self.template = self.from_file()
            self.data = self.template

        elif isinstance(val, str):  # they passed us a path
            self.data = self.from_file(val)
            self.template = self.data

        elif isinstance(val, dict):  # it's a dict
            self.data = val

        elif isinstance(val, Items):  # it's an Items object
            self.data = val.data

    def to_html(self):
        """Turn ``self`` into an HTML form element."""
        elt = self.to_html_rec(self.data)

        # elt = wrap(elt, 'ul', 'class', 'root')
        return bs(elt, 'html.parser').prettify()

    def apply_flat_dict(self, flat):
        self.apply_flat_dict_rec(self.data, flat)


class OrgItemList(ItemList):
    priority_categories = 5

    def itemToLI(self, item: str, selected):

        ret = ""

        safeName = item.replace(" ", self.space_replacer)  # cannot have spaces in CSS classes
        ret += wrap(item, "label")  # add label

        max = OrgItemList.priority_categories
        for i in range(max):
            attrs = ["type", "name", "value"]
            vals = ["radio", safeName, i]

            if i is selected:
                attrs.append("checked")  # check the one that is selected.

            ret += wrap(None, "input", attrs, vals)  # add one radio input

        ret = wrap(ret, "li", "class", safeName)  # wrap it in an <li>

        return ret
