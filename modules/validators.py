def validate_key_existing(dictionary, key, def_value=0):
    """
    Safety check for the standard library dictionary if
    key exists, and if not, creates it with default val.
    :param dictionary: dict: target dict
    :param key: string
    :param def_value: hashable object
    :return:
    """
    if key not in dictionary:
        dictionary[key] = def_value
