import os
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from json import dump as json_dump
from json import load as json_load
from pathlib import Path
from typing import Any, Dict, FrozenSet, Optional, Union

from colorpedia.exceptions import ConfigFileError, ConfigKeyError, ConfigValueError

CONFIG_DIR = Path.home() / ".config" / "colorpedia"
CONFIG_FILE = CONFIG_DIR / "config.json"
TMP_CONFIG_FILE = CONFIG_DIR / "config.json.tmp"

VIEW_KEYS = frozenset(("name", "rgb", "cmyk", "hex", "hsv", "hsl", "color"))
JSON_KEYS = frozenset(("is_name_exact", "name", "rgb", "cmyk", "hex", "hsv", "hsl"))
DEFAULT_SHADES_COUNT = 15
GET_VIEW_COLOR_HEIGHT = 10
GET_VIEW_COLOR_WIDTH = 20
LIST_VIEW_COLOR_WIDTH = 20


@dataclass
class Config:
    always_output_json: bool = False
    approx_name_suffix: str = "~"
    default_shades_count: int = DEFAULT_SHADES_COUNT
    display_degree_symbol: bool = False
    display_percent_symbol: bool = False
    get_view_color_height: int = GET_VIEW_COLOR_HEIGHT
    get_view_color_width: int = GET_VIEW_COLOR_WIDTH
    get_view_keys: FrozenSet[str] = VIEW_KEYS
    list_view_color_width: int = LIST_VIEW_COLOR_WIDTH
    list_view_keys: FrozenSet[str] = VIEW_KEYS
    json_keys: FrozenSet[str] = JSON_KEYS
    uppercase_hex_codes: bool = True

    def update(self, data: Dict[str, Any]) -> None:
        if type(data) != dict:
            raise ConfigFileError("Bad JSON: expecting an object")

        def validate_string(name):
            if type(getattr(self, name)) != str:
                raise ConfigValueError(name, "a string")

        def validate_boolean(name):
            if type(getattr(self, name)) != bool:
                raise ConfigValueError(name, "true or false")

        def validate_number(name):
            value = getattr(self, name)
            if not (type(value) == int and 1 <= value <= 100):
                raise ConfigValueError(name, "an integer between 1 and 100")

        def validate_view_keys(name):
            keys = getattr(self, name)
            if not (
                type(keys) in (list, frozenset)
                and len(keys) > 0
                and set(keys).issubset(VIEW_KEYS)
            ):
                raise ConfigValueError(
                    name, f"non-empty array of strings in {list(VIEW_KEYS)}"
                )

        def validate_json_keys(name):
            keys = getattr(self, name)
            if not (
                type(keys) in (list, frozenset)
                and len(keys) > 0
                and set(keys).issubset(JSON_KEYS)
            ):
                raise ConfigValueError(
                    name, f"non-empty array of strings in {list(JSON_KEYS)}"
                )

        for key, val in data.items():
            if hasattr(self, key):
                setattr(self, key, val)
            else:
                raise ConfigKeyError(key)

        validate_string("approx_name_suffix")
        validate_boolean("always_output_json")
        validate_boolean("display_degree_symbol")
        validate_boolean("display_percent_symbol")
        validate_boolean("uppercase_hex_codes")
        validate_number("default_shades_count")
        validate_number("get_view_color_height")
        validate_number("get_view_color_width")
        validate_number("list_view_color_width")
        validate_view_keys("get_view_keys")
        validate_view_keys("list_view_keys")
        validate_json_keys("json_keys")

        self.get_view_keys = frozenset(self.get_view_keys)
        self.list_view_keys = frozenset(self.list_view_keys)
        self.json_keys = frozenset(self.json_keys)

    def dump(self) -> Dict[str, Any]:
        data_dump = {}
        for key, value in self.__dict__.items():
            if isinstance(value, frozenset):
                data_dump[key] = list(value)
            else:
                data_dump[key] = value
        return data_dump

    def set_flags(
        self,
        json: Optional[bool] = None,
        all: Optional[bool] = None,
        units: Optional[bool] = None,
        shades: Optional[Union[bool, int]] = None,
    ) -> None:
        if json is True:
            self.always_output_json = True
        elif json is False:
            self.always_output_json = False

        if all is True:
            self.get_view_keys = VIEW_KEYS
            self.list_view_keys = VIEW_KEYS
            self.json_keys = JSON_KEYS

        if units is True:
            self.display_degree_symbol = True
            self.display_percent_symbol = True
        elif units is False:
            self.display_degree_symbol = False
            self.display_percent_symbol = False

        if shades is False:
            self.default_shades_count = 0
        elif shades is not True and shades is not None:
            self.default_shades_count = shades


def load_config_file() -> Config:  # pragma: no cover
    config = Config()
    try:
        with open(CONFIG_FILE, "r") as fp:
            data = json_load(fp)

    except FileNotFoundError:
        return config
    except ValueError as err:
        raise ConfigFileError("Bad JSON", err)
    except Exception as err:
        raise ConfigFileError(f"Cannot load {CONFIG_FILE}", err)
    else:
        config.update(data)
        return config


def save_config_file(config: Config) -> None:  # pragma: no cover
    data = config.dump()
    try:
        with open(CONFIG_FILE, "w") as fp:
            json_dump(data, fp, sort_keys=True, indent=2)

    except ValueError as err:
        raise ConfigFileError("Bad JSON", err)
    except Exception as err:
        raise ConfigFileError(f"Cannot save {CONFIG_FILE}", err)


def init_config_file() -> Config:  # pragma: no cover
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as err:
        raise ConfigFileError(f"Cannot create {CONFIG_DIR}", err)
    else:
        config = Config()
        save_config_file(config)
        return config


def edit_config_file(editor: str = None):  # pragma: no cover
    editor = editor or os.environ.get("VISUAL") or os.environ.get("EDITOR")
    if editor:
        editor = shlex.split(editor)[0]  # Prevent arbitrary code execution
    elif sys.platform.startswith("win"):
        editor = "notepad"
    else:
        editor = "vi"
    try:
        shutil.copy(CONFIG_FILE, TMP_CONFIG_FILE)
        subprocess.check_call([editor, str(TMP_CONFIG_FILE)])

        with open(TMP_CONFIG_FILE, "r") as fp:
            raw_config = json_load(fp)

    except Exception as err:
        raise ConfigFileError(f"Cannot update {CONFIG_FILE}", err)
    else:
        config = Config()
        config.update(raw_config)
        save_config_file(config)
        return config
    finally:
        try:
            TMP_CONFIG_FILE.unlink()
        except FileNotFoundError:
            pass
