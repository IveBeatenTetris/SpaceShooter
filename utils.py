import pygame as pg
import os

PATH = {
    "images": os.getcwd() + "\\img\\"
}
DEFAULT = {
    "player": {
        "image": PATH["images"] + "starship_0.png",
        "rotation": 90,
        "speed": 2,
        "default_shot": PATH["images"] + "starship_3.png",
        "shooting_speed": 6
    },
    "asteroid_3x2": {
        "image": PATH["images"] + "asteroid_3x2.png"
    }
}

def createText(**kwargs):# pg.surface
    """returns a pg.surface with the text already blitten to it."""
    default = {
        "text": "No Text was passed.",
        "font": "ebrima",
        "size": 16,
        "color": (255, 255, 255),
        "background": None,
        "antialias": True,
        "bold": False,
        "italic": False,
        "wrap": None
    }
    # validating arguments
    cfg = validateDict(kwargs, default)
    # building font-object
    font = pg.font.SysFont(cfg["font"], cfg["size"])
    font.set_bold(cfg["bold"])
    font.set_italic(cfg["italic"])
    # normal render for none-wrapping content
    if not cfg["wrap"]:
        text = font.render(
            cfg["text"],
            cfg["antialias"],
            cfg["color"]
        )
    # wrapping text
    else:
        text = wrapText(
            font = font,
            text = cfg["text"],
            size = cfg["wrap"],
            color = cfg["color"],
            antialias = cfg["antialias"]
        )
    # drawing background if one is given
    surface = pg.Surface((text.get_rect().size), pg.SRCALPHA)
    if cfg["background"]: surface.fill(cfg["background"])
    surface.blit(text, (0, 0))

    return surface
def drawBorder(surface, **kwargs):
    """
    draws a border on the given surface-object and returns it.
    keyword-arguments can be:
        'size'  (int)           :   declares how big the line-size draws the
                                    border.
        'color' (tuple/list)    :   the line-color of the border requiring 3
                                    integers to resemble a color-argument.
        'rect'  (pg.rect/tuple/ :   if this is not given, use the surface's
                list)               dimensions instead.
    example:
        config = (1, (255, 255, 255), [5, 10, 100, 25])
    usage:
        config = (3, (0, 0, 0))
        surf = drawBorder(display, size=config[0], color=config[1])
    """
    # creating a standard-setup for the border
    cfg = validateDict(kwargs, {
        "size"      :   1,
        "color"     :   (0, 0, 0),
        "rect"      :   surface.get_rect()
    })
    # converting into pygame.rect if it's a list or a tuple
    if type(cfg["rect"]) is list or type(cfg["rect"]) is tuple:
        cfg["rect"] = pg.Rect(cfg["rect"])
    # drawing border to the background
    pg.draw.lines(
        surface,
        cfg["color"],
        False,
        [
            cfg["rect"].topleft,
            (cfg["rect"].left, cfg["rect"].height - 1),
            (cfg["rect"].width - 1, cfg["rect"].height - 1),
            (cfg["rect"].width - 1, cfg["rect"].top),
            cfg["rect"].topleft,
        ],
        cfg["size"]
    )

    return surface
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
