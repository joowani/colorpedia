import os
import sys
from distutils.util import strtobool
from json import dumps as json_dumps
from typing import Callable, Iterable, Optional

from fire import Fire
from pkg_resources import get_distribution

from colorpedia.color import Color
from colorpedia.config import (
    CONFIG_FILE,
    Config,
    edit_config_file,
    init_config_file,
    load_config_file,
)
from colorpedia.converters import (
    cmyk_to_rgb,
    hex_to_rgb,
    hsl_to_rgb,
    hsv_to_rgb,
    name_to_rgb,
    palette_to_rgbs,
)
from colorpedia.exceptions import ColorpediaError
from colorpedia.formatters import format_get_view, format_list_view
from colorpedia.hexcodes import NAME_TO_HEX_CODE
from colorpedia.inputs import (
    normalize_degree_angle,
    normalize_hex_code,
    normalize_percent_value,
    validate_boolean_flag,
    validate_editor,
    validate_indent_width,
    validate_rgb_value,
    validate_shades_count,
)
from colorpedia.palettes import PALETTES


def prompt_user(question: str) -> bool:
    while True:
        sys.stdout.write(f"{question} [y/n] ")
        try:
            return strtobool(input().lower())
        except ValueError:
            print('Please respond with "y" or "n"\n')


def print_colors(config: Config, colors: Iterable[Color]):
    if config.always_output_json:
        print(json_dumps([c.get_dict(config.json_keys) for c in colors]))
    else:
        for color in colors:
            print(format_list_view(config, color))


def print_color(config: Config, color: Color):
    if config.default_shades_count:
        print_colors(config, color.get_shades(config.default_shades_count))

    elif config.always_output_json:
        print(json_dumps(color.get_dict(config.json_keys)))
    else:
        print(format_get_view(config, color))


def print_config(config: Config, sort: bool = True, indent: int = 2):
    print(json_dumps(config.dump(), sort_keys=sort, indent=indent))


def get_version(json: Optional[bool] = None):
    """Display Colorpedia CLI version.

    Colorpedia follows Semantic Versioning 2.0.0 (semver.org).

    :param json: Display in JSON format.
    """
    json = validate_boolean_flag(json)
    version = get_distribution("colorpedia").version
    print({"version": version} if json else version)


def init_config(force: bool = False):
    """Initialize or reset Colorpedia configuration.

    Configuration file is located at ~/.config/colorpedia/config.json.

    :param force: Overwrite existing configuration without asking user
        (default: False).
    """
    if CONFIG_FILE.exists() and not force:
        overwrite = prompt_user("Overwrite existing configuration?")
        if not overwrite:
            return
    print_config(init_config_file())


def show_config(sort: bool = True, indent: int = 2):
    """Display Colorpedia configuration.

    Configuration file is located at ~/.config/colorpedia/config.json.

    :param sort: Sort JSON keys (default: True).
    :param indent: JSON indent width (default: 2).
    """
    if not CONFIG_FILE.exists():
        print('Configuration not initialized. Run "color config init".')
    else:
        config = load_config_file()
        validate_boolean_flag(sort)
        validate_indent_width(indent)
        print_config(config, sort=sort, indent=indent)


def edit_config(editor: str = None):
    """Edit Colorpedia configuration using a text editor.

    If --editor flag is not specified, $VISUAL and $EDITOR environment
    variables are checked. If they are not defined, notepad is used on
    Windows and vi on Linux/MacOS.

    :param editor: Text editor to use. Must be a shell executable command.
        Any extra command options are ignored.
    """
    if not CONFIG_FILE.exists():
        print('Configuration not initialized. Run "color config init".')
    else:
        validate_editor(editor)
        config = edit_config_file(editor)
        print_config(config)


def get_palette_func(name: str) -> Callable:
    def function(
        json: Optional[bool] = None,
        all: bool = False,
        units: Optional[bool] = None,
    ):
        config = load_config_file()
        config.set_flags(
            json=validate_boolean_flag(json),
            all=validate_boolean_flag(all),
            units=validate_boolean_flag(units),
        )
        print_colors(config, [Color(*rgb) for rgb in palette_to_rgbs(name)])

    function.__doc__ = "\n".join(
        (
            f'Display colors in palette "{name}".',
            ":param json: Display in JSON format.",
            ":param all: Bypass user configuration and display all keys.",
            ":param units: Bypass user configuration and display units.",
        )
    )
    return function


def get_color_by_name_func(name: str, hex_code: str) -> Callable:
    def function(
        shades: int = 0,
        json: Optional[bool] = None,
        all: bool = False,
        units: Optional[bool] = None,
    ):
        config = load_config_file()
        config.set_flags(
            shades=validate_shades_count(shades),
            json=validate_boolean_flag(json),
            all=validate_boolean_flag(all),
            units=validate_boolean_flag(units),
        )
        print_color(config, Color(*name_to_rgb(name)))

    function.__doc__ = "\n".join(
        (
            f"Display color {name} (hex code #{hex_code.upper()}).",
            ":param json: Display in JSON format.",
            ":param shades: Display different shades of the specified color.",
            ":param all: Bypass user configuration and display all keys.",
            ":param units: Bypass user configuration and display units.",
        )
    )
    return function


def get_color_by_cmyk(
    c: float,
    m: float,
    y: float,
    k: float,
    shades: int = 0,
    json: Optional[bool] = None,
    all: bool = False,
    units: Optional[bool] = None,
):
    """Look up colors by CMYK (Cyan Magenta Yellow Black) values.

    CMYK is a subtractive color model used in color printing. It refers
    to the four ink plates used in color printing: cyan, magenta, yellow,
    and key (black). Values must be between 0.0 and 100.0 inclusive.

    Usage examples:

        color cmyk 100 100 100 100
        color cmyk 0 0 0 0
        color cmyk 10 20 30 40 --shades --json --all --units

    :param c: Cyan % (0.0 to 100.0 inclusive).
    :param m: Magenta % (0.0 to 100.0 inclusive).
    :param y: Yellow % (0.0 to 100.0 inclusive).
    :param k: Black/Key % (0.0 to 100.0 inclusive).
    :param shades: Display different shades of the specified color.
    :param json: Display in JSON format.
    :param all: Bypass user configuration and display all keys.
    :param units: Bypass user configuration and display units.
    """
    config = load_config_file()
    config.set_flags(
        shades=validate_shades_count(shades),
        json=validate_boolean_flag(json),
        all=validate_boolean_flag(all),
        units=validate_boolean_flag(units),
    )
    c = normalize_percent_value(c)
    m = normalize_percent_value(m)
    y = normalize_percent_value(y)
    k = normalize_percent_value(k)
    print_color(config, Color(*cmyk_to_rgb(c, m, y, k)))


def get_color_by_hex(
    hex_code: str,
    shades: int = 0,
    json: Optional[bool] = None,
    all: bool = False,
    units: Optional[bool] = None,
):
    """Look up colors by hexadecimal (web) code.

    The hexadecimal code must be specified without the hash (#) prefix
    and match the regular expression: ^(?:[0-9a-fA-F]{3}){1,2}$

    Usage examples:

        color hex FFFFFF
        color hex FFF
        color hex FFFFFF --shades --json --all --units

    :param hex_code: Hex color code without the hash (#) prefix.
    :param shades: Display different shades of the specified color.
    :param json: Display in JSON format.
    :param all: Bypass user configuration and display all keys.
    :param units: Bypass user configuration and display units.
    """
    config = load_config_file()
    config.set_flags(
        shades=validate_shades_count(shades),
        json=validate_boolean_flag(json),
        all=validate_boolean_flag(all),
        units=validate_boolean_flag(units),
    )
    hex_code = normalize_hex_code(hex_code)
    print_color(config, Color(*hex_to_rgb(hex_code)))


def get_color_by_hsl(
    h: float,
    s: float,
    l: float,
    shades: int = 0,
    json: Optional[bool] = None,
    all: bool = False,
    units: Optional[bool] = None,
):
    """Look up colors by HSL (Hue Saturation Lightness) values.

    Hue is a point on the color wheel from 0 to 360 where 0 is red,
    120 is green, and 240 is blue. Saturation is a percentage value
    where 0% means faded, and 100% means full color. Lightness is a
    percentage value where 0% is black and 100% is white.

    Usage examples:

        color hsl 360 100 100
        color hsl 0 0 0
        color hsl 10 20 30 --shades --json --all --units

    :param h: Hue in degree angle (0.0 to 360.0 inclusive).
    :param s: Saturation % (0.0 to 100.0 inclusive).
    :param l: Lightness % (0.0 to 100.0 inclusive).
    :param shades: Display different shades of the specified color.
    :param json: Display in JSON format.
    :param all: Bypass user configuration and display all keys.
    :param units: Bypass user configuration and display units.
    """
    config = load_config_file()
    config.set_flags(
        shades=validate_shades_count(shades),
        json=validate_boolean_flag(json),
        all=validate_boolean_flag(all),
        units=validate_boolean_flag(units),
    )
    h = normalize_degree_angle(h)
    s = normalize_percent_value(s)
    l = normalize_percent_value(l)
    print_color(config, Color(*hsl_to_rgb(h, s, l)))


def get_color_by_hsv(
    h: float,
    s: float,
    v: float,
    shades: int = 0,
    json: Optional[bool] = None,
    all: bool = False,
    units: Optional[bool] = None,
):
    """Look up colors by HSV (Hue Saturation Brightness/Value) values.

    Hue is a point on the color wheel from 0 to 360 where 0 is red,
    120 is green, and 240 is blue. Saturation is a percentage value
    where 0% means faded, and 100% means full color. Brightness (or
    value) is a percentage value where 0% is black and 100% reveals
    the most color.

    Usage examples:

        color hsv 360 100 100
        color hsv 0 0 0
        color hsv 10 20 30 --shades --json --all --units

    :param h: Hue in degree angle (0.0 to 360.0 inclusive).
    :param s: Saturation % (0.0 to 100.0 inclusive).
    :param v: Brightness/Value % (0.0 to 100.0 inclusive).
    :param shades: Display different shades of the specified color.
    :param json: Display in JSON format.
    :param all: Bypass user configuration and display all keys.
    :param units: Bypass user configuration and display units.
    """
    config = load_config_file()
    config.set_flags(
        shades=validate_shades_count(shades),
        json=validate_boolean_flag(json),
        all=validate_boolean_flag(all),
        units=validate_boolean_flag(units),
    )
    h = normalize_degree_angle(h)
    s = normalize_percent_value(s)
    v = normalize_percent_value(v)
    print_color(config, Color(*hsv_to_rgb(h, s, v)))


def get_color_by_rgb(
    r: int,
    g: int,
    b: int,
    shades: int = 0,
    json: Optional[bool] = None,
    all: bool = False,
    units: Optional[bool] = None,
):
    """Look up colors by RGB (Red Green Blue) values.

    RGB is an additive color model where red, green, and blue lights are
    superimposed together to yield shades of colors. The RGB values must
    be integers between 0 to 255.

    Usage examples:

        color rgb 255 255 255
        color rgb 0 0 0
        color rgb 10 20 30 --shades --json --all --units

    :param r: Red (0 to 255 inclusive).
    :param g: Green (0 to 255 inclusive).
    :param b: Blue (0 to 255 inclusive).
    :param shades: Display different shades of the specified color.
    :param json: Display in JSON format.
    :param all: Bypass user configuration and display all keys.
    :param units: Bypass user configuration and display units.
    """
    config = load_config_file()
    config.set_flags(
        shades=validate_shades_count(shades),
        json=validate_boolean_flag(json),
        all=validate_boolean_flag(all),
        units=validate_boolean_flag(units),
    )
    r = validate_rgb_value(r)
    g = validate_rgb_value(g)
    b = validate_rgb_value(b)
    print_color(config, Color(r, g, b))


class MainCommand(dict):
    """Colorpedia CLI.

    Look up colors using various models:

        color name green
        color hex FFFFFF
        color rgb 255 255 255
        color hsl 360 100 100
        color hsv 360 100 100
        color cmyk 100 100 100 100

    Display different shades:

        color name green --shades
        color hex FFFFFF --shades=5

    Look up color palettes:

        color palette molokai

    Control output with global flags:

        color name red --json --all --units

    Manage user configuration:

        color config init
        color config show
        color config edit
    """


class NameSubCommand(dict):
    """Look up colors by CSS3 name."""


class PaletteSubCommand(dict):
    """Look up color palettes."""


class ConfigSubCommand(dict):
    """Manage CLI configuration."""


def entry_point(name: str):
    try:
        # We need this to get colors working on windows.
        os.system("")
        Fire(
            name=name,
            component=MainCommand(
                {
                    "version": get_version,
                    "config": ConfigSubCommand(
                        {
                            "init": init_config,
                            "edit": edit_config,
                            "show": show_config,
                        }
                    ),
                    "name": NameSubCommand(
                        {
                            name: get_color_by_name_func(name, hex_code)
                            for name, hex_code in NAME_TO_HEX_CODE.items()
                        }
                    ),
                    "palette": PaletteSubCommand(
                        {name: get_palette_func(name) for name in PALETTES.keys()}
                    ),
                    "cmyk": get_color_by_cmyk,
                    "hex": get_color_by_hex,
                    "hsl": get_color_by_hsl,
                    "hsv": get_color_by_hsv,
                    "rgb": get_color_by_rgb,
                }
            ),
        )
    except KeyboardInterrupt:
        print()
    except ColorpediaError as err:
        sys.stderr.write(f"{err}\n")
        sys.exit(1)


def entry_point_color():
    entry_point("color")


def entry_point_colorpedia():
    entry_point("colorpedia")
