from typing import Optional


class ColorpediaError(Exception):
    """Generic Colorpedia exception."""


class ConfigFileError(ColorpediaError):
    """Configuration file cannot be accessed, created or updated."""

    def __init__(self, message: str, err: Optional[Exception] = None):
        if isinstance(err, OSError):
            message = f"{message}: {err.strerror} (errno: {err.errno})"
        elif err:
            message = f"{message}: {err}"
        super().__init__(message)


class ConfigKeyError(ColorpediaError):
    """Configuration key is invalid."""

    def __init__(self, key: str):
        super().__init__(f'Bad configuration key "{key}"')


class ConfigValueError(ColorpediaError):
    """Configuration value is invalid."""

    def __init__(self, key: str, exp: str):
        super().__init__(f'Bad value for configuration key "{key}" (expecting {exp})')


class InputValueError(ColorpediaError):
    """Invalid input value from user."""

    def __init__(self, name: str, exp: str):
        super().__init__(f"Bad {name} (expecting {exp})")
