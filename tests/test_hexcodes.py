import re

from colorpedia.hexcodes import HEX_CODE_TO_NAMES, HEX_REGEX, NAME_TO_HEX_CODE


def test_hex_codes():
    for hex_code, names in HEX_CODE_TO_NAMES.items():
        assert isinstance(names, tuple)
        assert isinstance(hex_code, str)
        assert len(names) > 0
        assert len(hex_code) == 6
        assert hex_code.isdigit() or hex_code.isupper()
        assert re.search(HEX_REGEX, hex_code)
        for name in names:
            assert name.lower()
            assert NAME_TO_HEX_CODE[name] == hex_code
        assert names == tuple(sorted(names))
