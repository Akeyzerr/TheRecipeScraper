# coding: utf-8

def string_handler_byte_to_unicode(res_obj):
    """
    res_obj holds the string data that has to be
    handled differently in python 2.7 and 3.x

    :param res_obj: byte string as in python2 or
                    unicode codes string as in python3
    :return: unicode codes string (formatted for use in the RecipeScraper project)
    """
    try:
        # case python2.7
        result = res_obj.decode("utf-8")
    except AttributeError:
        # case python3.x
        result = res_obj

    return " ".join(result.lower().replace(",", " ").split())


def string_handler_unicode_to_byte(res_obj):
    """
    If the object is a unicode string, encode it as a byte string

    :param res_obj: string or unicode: The object to be converted
    :return: string: Python2/3-agnostic string
    """
    try:
        if isinstance(res_obj, unicode):
            return res_obj.encode("utf-8")
        else:
            return res_obj
    except NameError:
        return res_obj
