from colorpedia.exceptions import (
    ConfigFileError,
    ConfigKeyError,
    ConfigValueError,
    InputValueError,
)


def test_config_file_error() -> None:
    error = ConfigFileError("A")
    assert str(error) == "A"

    error = ConfigFileError("A", FileNotFoundError(1, "B"))
    assert str(error) == "A: B (errno: 1)"

    error = ConfigFileError("A", ValueError("B"))
    assert str(error) == "A: B"


def test_config_key_error() -> None:
    error = ConfigKeyError("A")
    assert str(error) == 'Bad configuration key "A"'


def test_config_value_error() -> None:
    error = ConfigValueError("A", "B")
    assert str(error) == 'Bad value for configuration key "A" (expecting B)'


def test_input_error() -> None:
    error = InputValueError("A", "B")
    assert str(error) == "Bad A (expecting B)"
