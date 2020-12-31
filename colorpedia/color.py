from dataclasses import dataclass
from typing import Any, Dict, FrozenSet, Iterable, Set, Union

from colorpedia.converters import (
    hsl_to_rgb_shades,
    rgb_to_cmyk,
    rgb_to_hex,
    rgb_to_hsl,
    rgb_to_hsv,
    rgb_to_names,
)


@dataclass(eq=True, unsafe_hash=True)
class Color:
    r: int
    g: int
    b: int

    def __post_init__(self):
        self.rgb = (self.r, self.g, self.b)
        self.names, self.is_name_exact = rgb_to_names(*self.rgb)
        self.name = "/".join(self.names)
        self.hex = rgb_to_hex(*self.rgb)
        self.hsv = rgb_to_hsv(*self.rgb)
        self.hsl = rgb_to_hsl(*self.rgb)
        self.cmyk = rgb_to_cmyk(*self.rgb)

    def get_shades(self, size: int) -> Iterable["Color"]:
        h, s, l = self.hsl
        return (Color(*rgb) for rgb in hsl_to_rgb_shades(h, s, l, size))

    def get_dict(self, keys: Union[FrozenSet, Set]) -> Dict[str, Any]:
        result = {}
        if "hex" in keys:
            result["hex"] = self.hex
        if "rgb" in keys:
            result["rgb"] = self.rgb
        if "hsl" in keys:
            result["hsl"] = self.hsl
        if "hsv" in keys:
            result["hsv"] = self.hsv
        if "cmyk" in keys:
            result["cmyk"] = self.cmyk
        if "name" in keys:
            result["name"] = self.name
        if "is_name_exact" in keys:
            result["is_name_exact"] = self.is_name_exact
        return result
