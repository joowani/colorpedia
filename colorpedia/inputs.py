import re
from typing import Optional, Union

from colorpedia.exceptions import InputValueError
from colorpedia.hexcodes import HEX_REGEX


def validate_indent_width(value: int):
    if type(value) == int and 0 <= value <= 8:
        return value
    raise InputValueError("indent width", "an integer between 0 and 8")


def validate_boolean_flag(value: Optional[bool]):
    if value is True or value is False or value is None:
        return value
    raise InputValueError("boolean flag", "True, False or no value")


def validate_shades_count(value: Union[bool, int]) -> int:
    if (type(value) in (bool, int)) and 0 <= value <= 100:
        return value
    raise InputValueError("shades count", "an integer between 0 and 100")


def validate_editor(value: Optional[str]):
    if value is None or (type(value) == str and len(value) > 0 and " " not in value):
        return value
    raise InputValueError("editor", "a shell-executable command without whitespaces")


def validate_rgb_value(value: int) -> int:
    if type(value) == int and 0 <= value <= 255:
        return value
    raise InputValueError("RGB value", "an integer between 0 and 255")


def normalize_degree_angle(value: Union[float, int]) -> float:
    if (type(value) in (float, int)) and 0 <= value <= 360:
        return value / 360
    raise InputValueError("degree angle", "a float between 0.0 and 360.0")


def normalize_hex_code(value: str) -> str:
    if type(value) == int:
        if value == 0:
            return "000000"
        else:
            value = str(value)
    if type(value) == str and re.search(HEX_REGEX, value):
        return value if len(value) == 6 else "".join(c * 2 for c in value)
    raise InputValueError("hex code", f"a string matching {HEX_REGEX}")


def normalize_percent_value(value: Union[float, int]) -> float:
    if (type(value) in (float, int)) and 0 <= value <= 100:
        return value / 100
    raise InputValueError("percent value", "a float between 0.0 and 100.0")
