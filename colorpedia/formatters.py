from colorpedia.color import Color
from colorpedia.config import Config


def format_degree(value: float) -> str:
    return f"{value:<3.0f}"


def format_degree_with_unit(value: float) -> str:
    string = f"{value:.0f}°"
    return f"{string:<4s}"


def format_percent(value: float) -> str:
    return f"{value:<3.0f}"


def format_percent_with_unit(value: float) -> str:
    string = f"{value:.0f}%"
    return f"{string:<4s}"


def format_get_color(config: Config, r: int, g: int, b: int) -> str:
    h = config.get_view_color_height
    w = config.get_view_color_width
    line = f'\033[48;2;{r};{g};{b}m{" " * w}\033[0m'
    return "\n".join(line for _ in range(h))


def format_list_color(config: Config, r: int, g: int, b: int) -> str:
    return f'\033[48;2;{r};{g};{b}m{" " * config.list_view_color_width}\033[0m'


def format_name(config: Config, name: str, is_exact: bool) -> str:
    return name if is_exact else f"{name}{config.approx_name_suffix}"


def format_cmyk(config: Config, c: float, m: float, y: float, k: float) -> str:
    if config.display_percent_symbol:
        p = format_percent_with_unit
    else:
        p = format_percent

    return f"C:{p(c * 100)} M:{p(m * 100)} Y:{p(y * 100)} K:{p(k * 100)}"


def format_hsv(config: Config, h: float, s: float, v: float) -> str:
    if config.display_degree_symbol:
        d = format_degree_with_unit
    else:
        d = format_degree

    if config.display_percent_symbol:
        p = format_percent_with_unit
    else:
        p = format_percent

    return f"H:{d(h * 360)} S:{p(s * 100)} V:{p(v * 100)}"


def format_hsl(config: Config, h: float, s: float, l: float) -> str:
    if config.display_degree_symbol:
        d = format_degree_with_unit
    else:
        d = format_degree

    if config.display_percent_symbol:
        p = format_percent_with_unit
    else:
        p = format_percent

    return f"H:{d(h * 360)} S:{p(s * 100)} L:{p(l * 100)}"


def format_hex(config: Config, hex_code: str) -> str:
    if config.uppercase_hex_codes:
        return "#" + hex_code.upper()
    else:
        return "#" + hex_code.lower()


def format_rgb(config: Config, r: int, g: int, b: int) -> str:
    r_str = f"{r:<4d}" if config.display_degree_symbol else f"{r:<3d}"
    g_str = f"{g:<4d}" if config.display_percent_symbol else f"{g:<3d}"
    b_str = f"{b:<4d}" if config.display_percent_symbol else f"{b:<3d}"
    return f"R:{r_str} G:{g_str} B:{b_str}"


def format_get_view(config: Config, color: Color) -> str:
    keys = config.get_view_keys
    buf = []
    if "name" in keys:
        buf.append(f"Name : {format_name(config, color.name, color.is_name_exact)}")
    if "hex" in keys:
        buf.append(f"Hex  : {format_hex(config, color.hex)}")
    if "rgb" in keys:
        buf.append(f"RGB  : {format_rgb(config, *color.rgb)}")
    if "hsl" in keys:
        buf.append(f"HSL  : {format_hsl(config, *color.hsl)}")
    if "hsv" in keys:
        buf.append(f"HSV  : {format_hsv(config, *color.hsv)}")
    if "cmyk" in keys:
        buf.append(f"CMYK : {format_cmyk(config, *color.cmyk)}")
    if "color" in keys:
        buf.append("\n" + format_get_color(config, *color.rgb))
    return "\n".join(buf)


def format_list_view(config: Config, color: Color) -> str:
    keys = config.list_view_keys
    buf = []
    if "color" in keys:
        buf.append(format_list_color(config, *color.rgb))
    if "hex" in keys:
        buf.append(format_hex(config, color.hex))
    if "rgb" in keys:
        buf.append(format_rgb(config, *color.rgb))
    if "hsl" in keys:
        buf.append(format_hsl(config, *color.hsl))
    if "hsv" in keys:
        buf.append(format_hsv(config, *color.hsv))
    if "cmyk" in keys:
        buf.append(format_cmyk(config, *color.cmyk))
    if "name" in keys:
        buf.append(format_name(config, color.name, color.is_name_exact))
    return "|".join(buf)
