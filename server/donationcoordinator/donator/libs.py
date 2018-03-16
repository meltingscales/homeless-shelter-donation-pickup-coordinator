# general-purpose library functions used by ``donator`` class.

import copy
import json
from pprint import pprint

from donationcoordinator.libs import *

alreadySeen = {}  # cache for DictToUL function...


def freeze(o):
  if isinstance(o,dict):
    return frozenset({ k:freeze(v) for k,v in o.items()}.items())

  if isinstance(o,list):
    return tuple([freeze(v) for v in o])

  return o


def make_hash(o):
    """
    makes a hash out of anything that contains only list,dict and hashable types including string and numeric types
    """
    return hash(freeze(o))

def getItemTemplate(path: str):
    """Given a ``path``, return the JSON file at that path
    as a dict that represents the list of items."""
    with open(path) as data_file:
        return json.load(data_file)


def itemTemplateToCustomerForm(template: dict):
    """Given an ``ItemTemplate``, return an HTML form that represents
    that ``ItemTemplate``."""
    pass


def itemToLI(item: str, depth=0, s=" "):
    """Given an item in string form, return an HTML <li> elt that
    represents that item."""
    ret = ""

    safeName = item.replace(" ", "-")  # cannot have spaces in CSS classes

    ret += s * depth + wrap(item, "label") + "\n"  # add label
    ret += s * depth + wrap(None, "input", ["type", "name"], ["number", safeName]) + "\n"  # add input elt

    ret = s * depth + wrap(ret, "li", "class", safeName)  # wrap it in an <li>

    return ret


def itemListToUL(items: list, depth=0, s=" "):
    """Given a list of string items, return an HTML <ul> elt that
    represents that list of items."""

    ret = ""

    for item in items:
        ret += itemToLI(item, depth, s) + "\n"

    ret = wrap("\n" + ret, "ul")

    return ret


def dictToUL(dictionary: dict, depth=0, s=" ", dump_cache=False):
    """Given any dictionary of groups of any depth, return an HTML <ul>
    that represents that tree of items and item groups."""

    h = make_hash(dictionary)

    if dump_cache and h in alreadySeen: #they want to dump the cache for an object
        del alreadySeen[h]

    if h in alreadySeen:
        return alreadySeen[h]
    else:
        alreadySeen[h] = dictToUL_rec(dictionary, depth, s)
        return alreadySeen[h]


def dictToUL_rec(dictionary: dict, depth=0, s=" "):
    d = copy.deepcopy(dictionary)
    ret = ''

    keys = list(d.keys())
    print("Dict's keys:")
    print(keys)

    if len(keys) == 1 and keys[0] == 'root':
        ret += s * depth + '<ul class="root">\n'
        elt = d[keys[0]]

        print("we got root. its elt:")
        print(elt)

        ret += s * depth + dictToUL_rec(elt, depth + 1) + "\n"

        ret += s * depth + '</ul>' + "\n"

        return ret

    for key in keys:
        elt = d[key]

        ret += s * depth + f'<li class="{key}">\n'
        ret += s * depth + f'<a>"{key}"</a>\n'
        if isinstance(elt, list):  # if it's a list, stop recursing
            ret += itemListToUL(elt, depth, s)
        else:
            ret += s * (depth + 1) + f"<ul>\n"
            ret += dictToUL_rec(elt, depth + 1) + "\n"
            ret += s * (depth + 1) + f"</ul>\n"

    return ret


if __name__ == '__main__':
    d = getItemTemplate("../static/data/items.json")
    # pprint(d)

    dsimple = getItemTemplate("../static/data/items-simple.json")
    pprint(dsimple)

    # perishable = d['root']['food']['perishable']  # list of perishable food
    # pprint(perishable)
    #
    # perishableElt = itemListToUL(perishable)  # perishable food but as <ul> elt
    # print("Perishable food list: \n" + perishableElt)

    ulElt = dictToUL(d)
    print("Entire <ul> elt:\n" + ulElt)

    with open('../static/data/items_autogen.html', 'w+') as file:
        file.write(ulElt)
