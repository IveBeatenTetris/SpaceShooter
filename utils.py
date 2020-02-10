import os

PATH_IMG = os.getcwd() + "\\assets\\images"

def validateDict(user_cfg={}, defaults={}):# dict
    """
    validates a dictionary by comparing it to the default values from another
    given dict.
    """
    validated = {}

    for each in defaults:
        try:
            validated[each] = user_cfg[each]
        except KeyError:
            validated[each] = defaults[each]

    return validated
