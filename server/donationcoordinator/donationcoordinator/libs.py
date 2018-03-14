# list of very, very widely-used general general-purpose functions


def wrap(thing: str, tag: str, attrs: list = None, vals: list = None, quotes: str = '"'):
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
    if not attrs and not vals:  # they done passed nothing in!!!
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
        v = vals[i] if i <= len(vals)-1 else None

        ret += a
        if v:
            ret += f"={quotes}{v}{quotes} "

    ret += f">{thing}</{tag}>"

    return ret


if __name__ == '__main__':
    print(wrap("burger", "bacon"))

    print(wrap("click me", "a", "href", "google.com"))
    print(wrap("click me", "a", ["href", "clicked"], ["google.com"]))
    print(wrap("click me", "a", ["href", "clicked"], ["google.com", "true"]))
