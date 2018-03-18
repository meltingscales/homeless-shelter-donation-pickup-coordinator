# general-purpose library functions used by ``donator`` class.

import copy
import functools
import json
from functools import (lru_cache)
from pprint import pprint

from donationcoordinator.libs import *


def hashable_lru(func):
    cache = lru_cache(maxsize=1024)

    def deserialise(value):
        try:
            return json.loads(value)
        except Exception:
            return value

    def func_with_serialized_params(*args, **kwargs):
        _args = tuple([deserialise(arg) for arg in args])
        _kwargs = {k: deserialise(v) for k, v in kwargs.items()}
        return func(*_args, **_kwargs)

    cached_function = cache(func_with_serialized_params)

    @functools.wraps(func)
    def lru_decorator(*args, **kwargs):
        _args = tuple([json.dumps(arg, sort_keys=True) if type(arg) in (list, dict) else arg for arg in args])
        _kwargs = {k: json.dumps(v, sort_keys=True) if type(v) in (list, dict) else v for k, v in kwargs.items()}
        return cached_function(*_args, **_kwargs)

    lru_decorator.cache_info = cached_function.cache_info
    lru_decorator.cache_clear = cached_function.cache_clear
    return lru_decorator


def getItemTemplate(path: str):
    """Given a ``path``, return the JSON file at that path
    as a dict that represents the list of items."""
    with open(path) as data_file:
        return json.load(data_file)


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


@hashable_lru
def dictToUL(dictionary: dict, depth=0, s=" "):
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

        ret += s * depth + dictToUL(elt, depth + 1) + "\n"

        ret += s * depth + '</ul>' + "\n"

        return ret

    for key in keys:
        elt = d[key]

        ret += s * depth + f'<li class="{key}">\n'
        ret += s * depth + f'<a>"{key}"</a>\n'
        if isinstance(elt, list):  # if it's a list, stop recursing
            ret += itemListToUL(elt, depth + 1, s)
        else:
            ret += s * (depth + 1) + f"<ul>\n"
            ret += dictToUL(elt, depth + 1) + "\n"
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
