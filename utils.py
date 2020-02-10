import os

PATH = {
    "images": os.getcwd() + "\\img\\"
}
DEFAULT = {
    "player": {
        "image": PATH["images"] + "starship_0.png"
    }
}

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
