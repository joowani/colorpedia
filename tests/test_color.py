import pytest

from colorpedia.color import Color


def test_color_black():
    color = Color(0, 0, 0)
    assert color.name == "black"
    assert color.names == ("black",)
    assert color.is_name_exact is True
    assert color.hex == "000000"
    assert color.cmyk == (0, 0, 0, 1)
    assert color.rgb == (0, 0, 0)
    assert color.hsl == (0, 0, 0)
    assert color.hsv == (0, 0, 0)


def test_color_dimgray():
    color = Color(100, 100, 100)
    assert color.name == "dimgray/dimgrey"
    assert color.names == ("dimgray", "dimgrey")
    assert color.is_name_exact is False
    assert color.hex == "646464"
    assert color.cmyk == (0.0, 0.0, 0.0, 0.607843137254902)
    assert color.rgb == (100, 100, 100)
    assert color.hsl == (0.0, 0.0, 0.39215686274509803)
    assert color.hsv == (0.0, 0.0, 0.39215686274509803)


def test_color_darkslateblue():
    color = Color(50, 100, 150)
    assert color.name == "darkslateblue"
    assert color.names == ("darkslateblue",)
    assert color.is_name_exact is False
    assert color.hex == "326496"
    assert color.cmyk == (
        0.6666666666666667,
        0.3333333333333335,
        0.0,
        0.4117647058823529,
    )
    assert color.rgb == (50, 100, 150)
    assert color.hsl == (
        0.5833333333333334,
        0.5000000000000001,
        0.39215686274509803,
    )
    assert color.hsv == (
        0.5833333333333334,
        0.6666666666666667,
        0.5882352941176471,
    )


def test_color_white():
    color = Color(255, 255, 255)
    assert color.name == "white"
    assert color.names == ("white",)
    assert color.is_name_exact is True
    assert color.hex == "FFFFFF"
    assert color.cmyk == (0, 0, 0, 0)
    assert color.rgb == (255, 255, 255)
    assert color.hsl == (0.0, 0.0, 1.0)
    assert color.hsv == (0.0, 0.0, 1.0)


@pytest.mark.parametrize(
    ("r", "g", "b", "shades_count"),
    ((0, 0, 0, 1), (30, 40, 50, 1), (30, 40, 50, 5), (255, 255, 255, 5)),
)
def test_color_get_shades(r, g, b, shades_count):
    color = Color(r, g, b)
    colors = set(color.get_shades(shades_count))
    assert len(colors) == shades_count
    assert shades_count == 1 or Color(0, 0, 0) in colors
    assert shades_count == 1 or Color(255, 255, 255) in colors


@pytest.mark.parametrize(("r", "g", "b"), ((0, 0, 0), (10, 20, 30), (255, 255, 255)))
def test_color_to_dict(r, g, b):
    color = Color(r, g, b)

    assert color.get_dict(set()) == {}
    assert color.get_dict({"foo", "bar"}) == {}
    assert color.get_dict({"rgb"}) == {"rgb": (r, g, b)}

    keys = {"hex", "rgb", "hsl", "hsv", "cmyk", "name", "is_name_exact"}
    assert set(color.get_dict(keys).keys()) == keys
