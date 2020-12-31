from colorsys import hls_to_rgb as _hls_to_rgb
from colorsys import hsv_to_rgb as _hsv_to_rgb
from colorsys import rgb_to_hls as _rgb_to_hls
from colorsys import rgb_to_hsv as _rgb_to_hsv
from sys import maxsize
from typing import Iterable, List, Tuple

from colorpedia.hexcodes import HEX_CODE_TO_NAMES, NAME_TO_HEX_CODE
from colorpedia.palettes import PALETTES


def cmyk_to_rgb(c: float, m: float, y: float, k: float) -> Tuple[int, int, int]:
    """Convert CMYK (Cyan Magenta Yellow Black) to RGB (Red Green Blue).

    :param c: Cyan (0.0 to 1.0 inclusive).
    :param m: Magenta (0.0 to 1.0 inclusive).
    :param y: Yellow (0.0 to 1.0 inclusive).
    :param k: Black/Key (0.0 to 1.0 inclusive).
    :return: RGB tuple.
    """
    r = 255 * (1.0 - c) * (1.0 - k)
    g = 255 * (1.0 - m) * (1.0 - k)
    b = 255 * (1.0 - y) * (1.0 - k)

    return round(r), round(g), round(b)


def rgb_to_cmyk(r: int, g: int, b: int) -> Tuple[float, float, float, float]:
    """Convert RGB (Red Green Blue) to CMYK (Cyan Magenta Yellow Black).

    :param r: Red (0 to 255 inclusive).
    :param g: Green (0 to 255 inclusive).
    :param b: Blue (0 to 255 inclusive).
    :return: CMYK tuple.
    """
    if r == 0 and g == 0 and b == 0:
        return 0, 0, 0, 1

    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255

    cmy_min = min(c, m, y)
    c = (c - cmy_min) / (1 - cmy_min)
    m = (m - cmy_min) / (1 - cmy_min)
    y = (y - cmy_min) / (1 - cmy_min)
    k = cmy_min

    return c, m, y, k


def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    """Convert hexadecimal color code to RGB (Red Green Blue).

    :param hex_code: Hex color code without the hash (#) prefix.
    :return: RGB tuple.
    """
    r = int(hex_code[:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)
    return r, g, b


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB (Red Green Blue) to hexadecimal color code.

    :param r: Red (0 to 255 inclusive).
    :param g: Green (0 to 255 inclusive).
    :param b: Blue (0 to 255 inclusive).
    :return: Hexadecimal color code.
    """
    return f"{r:02x}{g:02x}{b:02x}".upper()


def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    """Convert HSL (Hue Saturation Lightness) to RGB (Red Green Blue).

    :param h: Hue (0.0 to 1.0 inclusive).
    :param s: Saturation (0.0 to 1.0 inclusive).
    :param l: Lightness (0.0 to 1.0 inclusive).
    :return: RGB tuple.
    """
    r, g, b = _hls_to_rgb(h, l, s)
    return round(r * 255), round(g * 255), round(b * 255)


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """Convert RGB (Red Green Blue) to HSL (Hue Saturation Lightness).

    :param r: Red (0 to 255 inclusive).
    :param g: Green (0 to 255 inclusive).
    :param b: Blue (0 to 255 inclusive).
    :return: HSL tuple in degree angle and percent (e.g. 360.0, 95.0, 5.0).
    """
    h, l, s = _rgb_to_hls(r / 255, g / 255, b / 255)
    return h, s, l


def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
    """Convert HSV (Hue Saturation Brightness) to RGB (Red Green Blue).

    :param h: Hue (0.0 to 1.0 inclusive).
    :param s: Saturation (0.0 to 1.0 inclusive).
    :param v: Brightness (0.0 to 1.0 inclusive).
    :return: RGB tuple.
    """
    r, g, b = _hsv_to_rgb(h, s, v)
    return round(r * 255), round(g * 255), round(b * 255)


def rgb_to_hsv(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """Convert RGB (Red Green Blue) to HSV (Hue Saturation Brightness).

    :param r: Red (0 to 255 inclusive).
    :param g: Green (0 to 255 inclusive).
    :param b: Blue (0 to 255 inclusive).
    :return: HSV tuple.
    """
    return _rgb_to_hsv(r / 255, g / 255, b / 255)


def name_to_rgb(name: str) -> Tuple[int, int, int]:
    """Convert CSS3 color name to RGB (Red Green Blue).

    :param name: CSS3 color name.
    :return: RGB tuple.
    """
    try:
        return hex_to_rgb(NAME_TO_HEX_CODE[name])
    except KeyError:
        raise ValueError("Unknown color name (expecting a CSS3 color name)")


def rgb_to_names(r: int, g: int, b: int) -> Tuple[Tuple[str, ...], bool]:
    """Convert RGB (Red Green Blue) to the nearest CSS3 name(s).

    :param r: Red (0 to 255 inclusive).
    :param g: Green (0 to 255 inclusive).
    :param b: Blue (0 to 255 inclusive).
    :return: Color name(s) and a boolean indicating exact match.
    """
    try:
        return HEX_CODE_TO_NAMES[f"{r:02x}{g:02x}{b:02x}".upper()], True
    except KeyError:
        minimum_diff = maxsize
        nearest_names: Tuple = tuple()

        for hex_code, names in HEX_CODE_TO_NAMES.items():
            _r, _g, _b = hex_to_rgb(hex_code)

            dr = (_r - r) ** 2
            dg = (_g - g) ** 2
            db = (_b - b) ** 2
            diff = dr + dg + db

            if diff < minimum_diff:
                minimum_diff = diff
                nearest_names = names

        return nearest_names, False


def palette_to_rgbs(palette: str) -> List[Tuple[int, int, int]]:
    """Return the hex codes in the given palette in sorted order.

    :param palette: Palette name.
    :return: List of RGB tuples.
    """
    try:
        return [hex_to_rgb(hex_code) for hex_code in PALETTES[palette]]
    except KeyError:
        raise ValueError(f'Unknown color palette "{palette}"')


def hsl_to_rgb_shades(
    h: float, s: float, l: float, size: int
) -> Iterable[Tuple[int, int, int]]:
    """Yield RGBs ranging in lightness (shades) given an HSL.

    :param h: Hue (0.0 to 1.0 inclusive).
    :param s: Saturation (0.0 to 1.0 inclusive).
    :param l: Lightness (0.0 to 1.0 inclusive).
    :param size: Range (positive integer).
    :return: RGB tuple iterator.
    """
    if size > 1:
        for x in range(size):
            r, g, b = _hls_to_rgb(h, x / (size - 1), s)
            yield round(r * 255), round(g * 255), round(b * 255)
    else:
        r, g, b = _hls_to_rgb(h, l, s)
        yield round(r * 255), round(g * 255), round(b * 255)
