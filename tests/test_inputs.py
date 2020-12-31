import pytest

from colorpedia.exceptions import InputValueError
from colorpedia.hexcodes import HEX_REGEX
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


@pytest.mark.parametrize("arg", [True, False])
def test_validate_boolean_flag(arg):
    assert validate_boolean_flag(arg) is arg


@pytest.mark.parametrize("bad_arg", (1, "1", max, []))
def test_validate_boolean_flag_bad_arg(bad_arg):
    with pytest.raises(InputValueError) as err:
        # noinspection PyTypeChecker
        validate_boolean_flag(bad_arg)
    assert str(err.value) == "Bad boolean flag (expecting True, False or no value)"


@pytest.mark.parametrize("arg", ("vim", "vi"))
def test_validate_editor_flag(arg):
    assert validate_editor(arg) == arg


@pytest.mark.parametrize("bad_arg", (1, "vim -i", True, False, max, []))
def test_validate_editor_flag_bad_arg(bad_arg):
    with pytest.raises(InputValueError) as err:
        validate_editor(bad_arg)
    assert (
        str(err.value)
        == "Bad editor (expecting a shell-executable command without args)"
    )


@pytest.mark.parametrize("arg", tuple(range(9)))
def test_validate_indent_width(arg):
    assert validate_indent_width(arg) == arg


@pytest.mark.parametrize("bad_arg", (9, -1, "1", True, False, max, None, []))
def test_validate_indent_width_bad_arg(bad_arg):
    with pytest.raises(InputValueError) as err:
        validate_indent_width(bad_arg)
    assert str(err.value) == "Bad indent width (expecting an integer between 0 and 8)"


@pytest.mark.parametrize(
    ("arg", "expected"),
    ((100, 100), (10, 10), (0, 0), (True, True), (False, False)),
)
def test_validate_shades_count(arg, expected):
    assert validate_shades_count(arg) == expected


@pytest.mark.parametrize("bad_arg", ("1", 101, -1, max, None, []))
def test_validate_shades_count_bad_arg(bad_arg):
    with pytest.raises(InputValueError) as err:
        validate_shades_count(bad_arg)
    assert str(err.value) == "Bad shades count (expecting an integer between 0 and 100)"


@pytest.mark.parametrize(("arg", "expected"), ((0, 0), (100, 100), (255, 255)))
def test_validate_rgb_value(arg, expected):
    output = validate_rgb_value(arg)
    assert isinstance(output, int)
    assert output == expected


@pytest.mark.parametrize("bad_arg", (256, -1, "1", "255", True, False, max, None, []))
def test_validate_rgb_value_bad_arg(bad_arg):
    with pytest.raises(InputValueError) as err:
        validate_rgb_value(bad_arg)

    assert str(err.value) == "Bad RGB value (expecting an integer between 0 and 255)"


@pytest.mark.parametrize(
    ("arg", "expected"),
    ((100.0, 1.0), (100, 1.0), (55.5, 0.555), (55, 0.55), (0.0, 0.0)),
)
def test_normalize_percent(arg, expected):
    output = normalize_percent_value(arg)
    assert isinstance(output, float)
    assert output == expected


@pytest.mark.parametrize(
    "bad_arg", ("100", 101.0, -1.0, -1, True, False, max, None, [])
)
def test_normalize_percent_bad_arg(bad_arg):
    with pytest.raises(InputValueError) as err:
        normalize_percent_value(bad_arg)

    assert (
        str(err.value) == "Bad percent value (expecting a float between 0.0 and 100.0)"
    )


@pytest.mark.parametrize(("arg", "expected"), ((360.0, 1.0), (180.0, 0.5), (0.0, 0.0)))
def test_normalize_degree_angle(arg, expected):
    output = normalize_degree_angle(arg)
    assert isinstance(output, float)
    assert output == expected


@pytest.mark.parametrize("bad_arg", ("360", 361, -1, True, False, max, None, []))
def test_normalize_degree_angle_bad_arg(bad_arg):
    with pytest.raises(InputValueError) as err:
        normalize_degree_angle(bad_arg)
    assert "Bad degree angle" in str(err.value)


@pytest.mark.parametrize(
    ("arg", "expected"),
    (("ABC", "AABBCC"), ("ABCDEF", "ABCDEF"), ("FFFFFF", "FFFFFF")),
)
def test_normalize_hex_code(arg, expected):
    assert normalize_hex_code(arg) == expected


@pytest.mark.parametrize(
    "bad_arg", ("", "F", "FF", "FFFFFH", "#FFFFFF", True, False, max, None, [])
)
def test_normalize_hex_code_bad_arg(bad_arg):
    with pytest.raises(InputValueError) as err:
        normalize_hex_code(bad_arg)

    assert str(err.value) == f"Bad hex code (expecting a string matching {HEX_REGEX})"
