class ColorpediaError(Exception):
    """Generic Colorpedia exception."""


class ConfigFileError(ColorpediaError):
    """Configuration file cannot be accessed, created or updated."""

    def __init__(self, msg, err: Exception = None):
        if isinstance(err, OSError):
            msg = f"{msg}: {err.strerror} (errno: {err.errno})"
        elif err:
            msg = f"{msg}: {err}"
        super(ConfigFileError, self).__init__(msg)


class ConfigKeyError(ColorpediaError):
    """Configuration key is invalid."""

    def __init__(self, key: str):
        super(ConfigKeyError, self).__init__(f'Bad configuration key "{key}"')


class ConfigValueError(ColorpediaError):
    """Configuration value is invalid."""

    def __init__(self, key: str, exp: str):
        super(ConfigValueError, self).__init__(
            f'Bad value for configuration key "{key}" (expecting {exp})'
        )


class InputValueError(ColorpediaError):
    """Invalid input value from user."""

    def __init__(self, name: str, exp):
        super(InputValueError, self).__init__(f"Bad {name} (expecting {exp})")
