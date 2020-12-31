from colorpedia.palettes import PALETTES


def test_palette():
    for name, hex_codes in PALETTES.items():
        assert isinstance(name, str)
        assert name.islower()
        assert len(name) > 0
        assert len(hex_codes) > 0
        assert len(hex_codes) == len(
            set(hex_codes)
        ), f'duplicate hex code in palette "{name}"'
        for hex_code in hex_codes:
            assert isinstance(hex_code, str)
            assert hex_code.isdigit() or hex_code.isupper()
