# general-purpose library functions used by ``donator`` class.

import copy
import json
from pprint import pprint

from donationcoordinator.libs import *


def getItemTemplate(path: str):
    """Given a ``path``, return the JSON file at that path
    as a dict that represents the list of items."""
    with open(path) as data_file:
        return json.load(data_file)


def itemTemplateToCustomerForm(template: dict):
    """Given an ``ItemTemplate``, return an HTML form that represents
    that ``ItemTemplate``."""
    pass


def itemToLI(item: str):
    """Given an item in string form, return an HTML <li> elt that
    represents that item."""
    ret = ""

    safeName = item.replace(" ", "-")  # cannot have spaces in CSS classes

    ret += wrap(item, "label")  # add label
    ret += wrap(None, "input", ["type", "name"], ["number", safeName])  # add input elt

    ret = wrap(ret, "li", "class", safeName)  # wrap it in an <li>

    return ret


def itemListToUL(items: list):
    """Given a list of string items, return an HTML <ul> elt that
    represents that list of items."""

    ret = ""

    for item in items:
        ret += itemToLI(item) + "\n"

    ret = wrap("\n" + ret, "ul")

    return ret

def dictToUL_rec(dictionary: dict, elts: list):
    pass

def dictToUL(dictionary: dict):
    """Given any dictionary of groups of any depth, return an HTML <ul>
    that represents that tree of items and item groups."""

    d = copy.deepcopy(dictionary)
    ret = ''

    while d:
        for key, value in d.copy().items():
            print(key + ": " + str(value))
            del d[key]

    return ret


if __name__ == '__main__':
    d = getItemTemplate("../static/data/items.json")
    pprint(d)

    perishable = d['food']['perishable']  # list of perishable food
    pprint(perishable)

    perishableElt = itemListToUL(perishable)  # perishable food but as <ul> elt
    print("Perishable food list: \n" + perishableElt)

    ulElt = dictToUL(d)
    print("Entire <ul> elt:\n" + ulElt)
