import pytest

from colorpedia.color import Color
from colorpedia.config import Config
from colorpedia.formatters import (
    format_cmyk,
    format_get_view,
    format_hex,
    format_hsl,
    format_hsv,
    format_list_view,
    format_name,
    format_rgb,
)

default_config = Config()

custom_config = Config()
custom_config.uppercase_hex_codes = False
custom_config.get_view_keys = frozenset(("name", "hex"))
custom_config.list_view_keys = frozenset(("name", "hex"))
custom_config.approx_name_suffix = "*"
custom_config.set_flags(units=True)


@pytest.mark.parametrize(
    ("c", "m", "y", "k", "expected"),
    (
        (0.000, 0.010, 0.020, 0.030, "C:0   M:1   Y:2   K:3  "),
        (0.104, 0.204, 0.304, 0.404, "C:10  M:20  Y:30  K:40 "),
        (0.106, 0.206, 0.306, 0.406, "C:11  M:21  Y:31  K:41 "),
        (1.000, 1.000, 1.000, 1.000, "C:100 M:100 Y:100 K:100"),
    ),
)
def test_format_cmyk(c, m, y, k, expected):
    assert format_cmyk(default_config, c, m, y, k) == expected


@pytest.mark.parametrize(
    ("c", "m", "y", "k", "expected"),
    (
        (0.000, 0.010, 0.020, 0.030, "C:0%   M:1%   Y:2%   K:3%  "),
        (0.104, 0.204, 0.304, 0.404, "C:10%  M:20%  Y:30%  K:40% "),
        (0.106, 0.206, 0.306, 0.406, "C:11%  M:21%  Y:31%  K:41% "),
        (1.000, 1.000, 1.000, 1.000, "C:100% M:100% Y:100% K:100%"),
    ),
)
def test_format_cmyk_with_units(c, m, y, k, expected):
    assert format_cmyk(custom_config, c, m, y, k) == expected


@pytest.mark.parametrize(
    ("hex_code", "expected"),
    (
        ("ffffff", "#FFFFFF"),
        ("FFFFFF", "#FFFFFF"),
        ("0f0f0f", "#0F0F0F"),
        ("0F0F0F", "#0F0F0F"),
    ),
)
def test_format_hex(hex_code, expected):
    assert format_hex(default_config, hex_code) == expected
    assert format_hex(custom_config, hex_code) == expected.lower()


@pytest.mark.parametrize(
    ("h", "s", "l", "expected"),
    (
        (0.0, 0.010, 0.020, "H:0   S:1   L:2  "),
        (0.5, 0.200, 0.300, "H:180 S:20  L:30 "),
        (0.5, 0.206, 0.306, "H:180 S:21  L:31 "),
        (1.0, 1.001, 1.001, "H:360 S:100 L:100"),
    ),
)
def test_format_hsl(h, s, l, expected):
    assert format_hsl(default_config, h, s, l) == expected


@pytest.mark.parametrize(
    ("h", "s", "l", "expected"),
    (
        (0.0, 0.010, 0.020, "H:0°   S:1%   L:2%  "),
        (0.5, 0.200, 0.300, "H:180° S:20%  L:30% "),
        (0.5, 0.206, 0.306, "H:180° S:21%  L:31% "),
        (1.0, 1.001, 1.001, "H:360° S:100% L:100%"),
    ),
)
def test_format_hsl_with_units(h, s, l, expected):
    assert format_hsl(custom_config, h, s, l) == expected


@pytest.mark.parametrize(
    ("h", "s", "v", "expected"),
    (
        (0.0, 0.010, 0.020, "H:0   S:1   V:2  "),
        (0.5, 0.200, 0.300, "H:180 S:20  V:30 "),
        (0.5, 0.206, 0.306, "H:180 S:21  V:31 "),
        (1.0, 1.001, 1.001, "H:360 S:100 V:100"),
    ),
)
def test_format_hsv(h, s, v, expected):
    assert format_hsv(default_config, h, s, v) == expected


@pytest.mark.parametrize(
    ("h", "s", "v", "expected"),
    (
        (0.0, 0.010, 0.020, "H:0°   S:1%   V:2%  "),
        (0.5, 0.200, 0.300, "H:180° S:20%  V:30% "),
        (0.5, 0.206, 0.306, "H:180° S:21%  V:31% "),
        (1.0, 1.001, 1.001, "H:360° S:100% V:100%"),
    ),
)
def test_format_hsv_with_units(h, s, v, expected):
    assert format_hsv(custom_config, h, s, v) == expected


@pytest.mark.parametrize(
    ("r", "g", "b", "expected"),
    (
        (0, 1, 2, "R:0   G:1   B:2  "),
        (10, 20, 30, "R:10  G:20  B:30 "),
        (255, 255, 255, "R:255 G:255 B:255"),
    ),
)
def test_format_rgb(r, g, b, expected):
    assert format_rgb(default_config, r, g, b) == expected


@pytest.mark.parametrize(
    ("r", "g", "b", "expected"),
    (
        (0, 1, 2, "R:0    G:1    B:2   "),
        (10, 20, 30, "R:10   G:20   B:30  "),
        (255, 255, 255, "R:255  G:255  B:255 "),
    ),
)
def test_format_rgb_with_units(r, g, b, expected):
    assert format_rgb(custom_config, r, g, b) == expected


def test_format_name():
    assert format_name(default_config, "foo", False) == "foo (approx)"
    assert format_name(default_config, "foo", True) == "foo"
    assert format_name(custom_config, "foo", False) == "foo*"
    assert format_name(custom_config, "foo", True) == "foo"


@pytest.mark.parametrize(("r", "g", "b"), ((0, 0, 0), (10, 20, 30), (255, 255, 255)))
def test_get_view(r, g, b):
    color = Color(r, g, b)

    view = format_get_view(default_config, color)
    assert "Name" in view
    assert "Hex" in view
    assert "RGB" in view
    assert "HSL" in view
    assert "HSV" in view
    assert "CMYK" in view

    view = format_get_view(custom_config, color)
    assert "Name" in view
    assert "Hex" in view
    assert "RGB" not in view
    assert "HSL" not in view
    assert "HSV" not in view
    assert "CMYK" not in view


@pytest.mark.parametrize(("r", "g", "b"), ((0, 0, 0), (10, 20, 30), (255, 255, 255)))
def test_list_view(r, g, b):
    color = Color(r, g, b)

    view = format_list_view(default_config, color)
    assert len(view.split("|")) == len(default_config.list_view_keys)

    view = format_list_view(custom_config, color)
    assert len(view.split("|")) == len(custom_config.list_view_keys)
