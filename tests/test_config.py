import dataclasses

import pytest

from colorpedia.config import DEFAULT_SHADES_COUNT, JSON_KEYS, VIEW_KEYS, Config
from colorpedia.exceptions import ConfigFileError, ConfigKeyError, ConfigValueError


def test_config_update():
    config = Config()
    config.update(config.dump())
    assert config == Config()


@pytest.mark.parametrize("data", [True, max, None, [], ()])
def test_config_update_bad_data_format(data):
    config = Config()
    with pytest.raises(ConfigFileError) as err:
        # noinspection PyTypeChecker
        config.update(data)
    assert str(err.value).startswith("B")


@pytest.mark.parametrize("key", [f.name for f in dataclasses.fields(Config)])
def test_config_update_bad_value(key):
    config = Config()
    with pytest.raises(ConfigValueError) as err:
        config.update({key: None})
    assert str(err.value).startswith("Bad value for configuration key")


@pytest.mark.parametrize("key", ["bad-" + f.name for f in dataclasses.fields(Config)])
def test_config_update_bad_key(key):
    config = Config()
    with pytest.raises(ConfigKeyError) as err:
        config.update({key: None})
    assert str(err.value).startswith("Bad configuration key")


def test_config_set_flag_json():
    config = Config()
    config.set_flags(json=False)
    assert config.always_output_json is False

    config = Config()
    config.set_flags(json=True)
    assert config.always_output_json is True


def test_config_set_flag_all():
    config = Config()
    view_keys = frozenset(("name", "hex"))
    config.get_view_keys = view_keys
    config.list_view_keys = view_keys
    config.json_keys = view_keys

    config.set_flags(all=None)
    assert config.get_view_keys == view_keys
    assert config.list_view_keys == view_keys
    assert config.json_keys == view_keys

    config.set_flags(all=False)
    assert config.get_view_keys == view_keys
    assert config.list_view_keys == view_keys
    assert config.json_keys == view_keys

    config.set_flags(all=True)
    assert config.get_view_keys == VIEW_KEYS
    assert config.list_view_keys == VIEW_KEYS
    assert config.json_keys == JSON_KEYS


def test_config_set_flag_units():
    config = Config()
    config.set_flags(units=False)
    assert config.display_degree_symbol is False
    assert config.display_percent_symbol is False

    config = Config()
    config.set_flags(units=True)
    assert config.display_degree_symbol is True
    assert config.display_percent_symbol is True


def test_config_set_flag_shades():
    config = Config()
    config.set_flags(shades=True)
    assert config.default_shades_count == DEFAULT_SHADES_COUNT

    config = Config()
    config.set_flags(shades=False)
    assert config.default_shades_count == 0

    config = Config()
    config.set_flags(shades=None)
    assert config.default_shades_count == 15

    config = Config()
    config.set_flags(shades=10)
    assert config.default_shades_count == 10
