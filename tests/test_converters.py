import itertools
from typing import Tuple

import pytest

from colorpedia import (
    cmyk_to_rgb,
    hex_to_rgb,
    hsl_to_rgb,
    hsl_to_rgb_shades,
    hsv_to_rgb,
    name_to_rgb,
    palette_to_rgbs,
    rgb_to_cmyk,
    rgb_to_hex,
    rgb_to_hsl,
    rgb_to_hsv,
    rgb_to_names,
)
from colorpedia.hexcodes import HEX_CODE_TO_NAMES

RGB_VALS = list(itertools.product([0, 100, 255], repeat=3))


def add_clamped(value: int) -> int:
    return min(value + 1, 255)


def sub_clamped(value: int) -> int:
    return max(value - 1, 0)


@pytest.mark.parametrize("rgb", RGB_VALS)
def test_rgb_cmyk(rgb: Tuple[int, int, int]):
    assert cmyk_to_rgb(*rgb_to_cmyk(*rgb)) == rgb


@pytest.mark.parametrize("rgb", RGB_VALS)
def test_rgb_hex(rgb: Tuple[int, int, int]):
    assert hex_to_rgb(rgb_to_hex(*rgb)) == rgb


@pytest.mark.parametrize("rgb", RGB_VALS)
def test_rgb_hsl(rgb: Tuple[int, int, int]):
    assert hsl_to_rgb(*rgb_to_hsl(*rgb)) == rgb


@pytest.mark.parametrize("rgb", RGB_VALS)
def test_rgb_hsv(rgb: Tuple[int, int, int]):
    assert hsv_to_rgb(*rgb_to_hsv(*rgb)) == rgb


@pytest.mark.parametrize(
    "name",
    (
        HEX_CODE_TO_NAMES["F08080"][0],
        HEX_CODE_TO_NAMES["48D1CC"][0],
        HEX_CODE_TO_NAMES["556B2F"][0],
        HEX_CODE_TO_NAMES["87CEFA"][0],
        HEX_CODE_TO_NAMES["9ACD32"][0],
    ),
)
def test_rgb_name(name: str):
    r, g, b = name_to_rgb(name)
    names, is_name_exact_match = rgb_to_names(r, g, b)
    assert name in names
    assert is_name_exact_match

    for names, is_name_exact_match in [
        rgb_to_names(add_clamped(r), g, b),
        rgb_to_names(r, add_clamped(g), b),
        rgb_to_names(r, g, add_clamped(b)),
        rgb_to_names(sub_clamped(r), g, b),
        rgb_to_names(r, sub_clamped(g), b),
        rgb_to_names(r, g, sub_clamped(b)),
    ]:
        assert name in names
        assert not is_name_exact_match

    with pytest.raises(ValueError) as err:
        name_to_rgb(f"not {name}")
    assert "Unknown color name" in str(err.value)


@pytest.mark.parametrize("palette", ("red", "green", "blue"))
def test_palette_to_rgbs(palette: str):
    rgb = name_to_rgb(palette)
    assert rgb in palette_to_rgbs(palette)

    with pytest.raises(ValueError) as err:
        palette_to_rgbs(palette + "invalid")
    assert "Unknown color palette" in str(err.value)


@pytest.mark.parametrize(
    ("h", "s", "l", "shades_count"),
    (
        (0.0, 0.0, 0.0, 1),
        (0.0, 0.0, 0.0, 5),
        (0.5, 0.5, 0.5, 1),
        (0.5, 0.5, 0.5, 5),
        (1.0, 1.0, 1.0, 1),
        (1.0, 1.0, 1.0, 5),
    ),
)
def test_hsl_to_rgbs(h, s, l, shades_count):
    rgbs = set(hsl_to_rgb_shades(h, s, l, shades_count))
    assert len(rgbs) == shades_count
    assert shades_count == 1 or (0, 0, 0) in rgbs
    assert shades_count == 1 or (255, 255, 255) in rgbs
