# list of very, very widely-used general general-purpose functions
import functools
import json
from functools import (lru_cache)
from math import sin, cos, radians, degrees, acos

import googlemaps
from django.conf import settings
from django.contrib.gis.geos import Point


def calc_dist_meters(lat_a, long_a, lat_b, long_b):
    resToMile = calc_dist_miles(lat_a, long_a, lat_b, long_b)
    resToMt = resToMile / 0.00062137119223733

    return resToMt


def calc_dist_miles(lat_a, long_a, lat_b, long_b):
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    long_diff = radians(long_a - long_b)
    distance = (sin(lat_a) * sin(lat_b) +
                cos(lat_a) * cos(lat_b) * cos(long_diff))
    resToMile = degrees(acos(distance)) * 69.09
    return resToMile


def calc_dist_p_meters(p1: Point, p2: Point):
    return calc_dist_meters(p1.x, p1.y, p2.x, p2.y)


def calc_dist_p_miles(p1: Point, p2: Point):
    return calc_dist_miles(p1.x, p1.y, p2.x, p2.y)


def islist(o):
    return type(o) == type([])


def istuple(o):
    return type(o) == type(())


class GoogleMapsClient():
    try:
        key = settings.GEOPOSITION_GOOGLE_MAPS_API_KEY
        client = googlemaps.Client(key=key)
    except Exception as e:
        pass

    @staticmethod
    @lru_cache(maxsize=1024)
    def results(address_string):
        return GoogleMapsClient.client.geocode(address_string)

    @staticmethod
    @lru_cache(maxsize=1024)
    def lat_lon(address_string):
        """Given an address, return a list of lat-lon pairs that belongs to that address."""
        results = GoogleMapsClient.results(address_string)

        latlons = []
        for result in results:
            ll: dict = result['geometry']['location']
            latlons.append(tuple(ll.values()))

        return latlons


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


def wrap(thing: str, tag: str, attrs: list = None, vals: list = None, quotes: str = '"'):
    """
    Wrap a ``thing`` in ``tag``, and also apply an ``attribute`` that might have a ``val``.

    Example 1:
        ``wrap("click me", "a", "href", "google.com")``\n
        ``->``\n
        ``<a href="google.com">click me</a>``\n

    Example 2:
        ``wrap("hi", "a", "checked")``\n
        ``->``\n
        ``<a checked>hi</a>``\n

    Example 3:
        ``wrap("text", "a")``\n
        ``->``\n
        ``<a>text</a>``\n

    Example 4:
        ``wrap(None, "input", ["type", "checked"], "checkbox")``\n
        ``->``\n
        ``<input type="checkbox" checked />``\n

    """
    if (thing and tag) and (not attrs and not vals):  # they done passed nothing in!!!
        return f"<{tag}>{thing}</{tag}>"

    # ensure that attr and val are both lists so we can treat them like it
    if not isinstance(attrs, list):
        attrs = [attrs]
    if not isinstance(vals, list):
        vals = [vals]

    ret = ""

    ret += f"<{tag} "

    # apply ALL vals and attrs
    for i in range(len(attrs)):
        a = attrs[i]
        v = vals[i] if i <= len(vals) - 1 else None

        ret += a
        if v is not None:
            ret += f"={quotes}{v}{quotes} "

    if thing is not None:  # if it's not self-closing
        ret += f">{thing}</{tag}>"
    else:
        ret += "/>"

    return ret


if __name__ == '__main__':
    print(wrap("burger", "bacon"))

    print(wrap("click me", "a", "href", "google.com"))
    print(wrap("click me", "a", ["href", "clicked"], ["google.com"]))
    print(wrap("click me", "a", ["href", "clicked"], ["google.com", "true"]))
    print(wrap(None, "input", ["type", "checked"], "checkbox"))
