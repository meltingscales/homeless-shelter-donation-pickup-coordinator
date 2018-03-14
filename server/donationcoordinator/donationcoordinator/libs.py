# list of very, very widely-used general general-purpose functions


def wrap(thing, tag, attr=None, val=None, quotes='"'):
    """
    Wrap a ``thing`` in ``tag``, and also apply an ``attribute`` that might have a ``val``.

    Example 1:
        ``wrap("a", "click me", "href", "google.com")``\n
        ``->``\n
        ``<a href="google.com">click me</a>``\n

    Example 2:
        ``wrap("a", "hi", "checked")``\n
        ``->``\n
        ``<a checked>hi</a>``\n

    Example 3:
        ``wrap("a", "text")``\n
        ``->``\n
        ``<a>text</a>``\n

    """
    if not attr and not val:  # they done passed nothing in!!!
        return f"<{tag}>{thing}</{tag}>"

    ret = ""

    ret += f"<{tag} {attr}"

    if val:
        ret += f"={quotes}{val}{quotes}"

    ret += f">{thing}</{tag}>"

    return ret


if __name__ == '__main__':
    print(wrap("burger", "bacon"))

    print(wrap("click me", "a", "href", "google.com"))
