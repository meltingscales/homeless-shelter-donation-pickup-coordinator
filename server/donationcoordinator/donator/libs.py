# general-purpose library functions used by ``donator`` class.

import json
from pprint import pprint
from django.conf import settings
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


def itemListToUL(items: list):
    """Given a list of string items, return an HTML <ul> elt that
    represents that list of items."""

    ret = ""

    for item in items:
        ret += wrap(item, "li", "class", item) + "\n"
    ret =  wrap(ret, "ul")

    return ret


if __name__ == '__main__':
    it = getItemTemplate("../static/data/items.json")
    pprint(it)

    perishable = it['food']['perishable']  # list of perishable food
    pprint(perishable)

    perishableElt = itemListToUL(perishable)  # perishable food but as <ul> elt

    print(perishableElt)
