import math
from typing import Callable, Tuple

RGB = Tuple[int, int, int]

EASINGS: dict[str, Callable[[float], float]] = {
    "linear": lambda t: t,
    "ease_in": lambda t: t ** 3,
    "ease_out": lambda t: 1.0 - (1.0 - t) ** 3,
    "sine": lambda t: math.sin((t * math.pi) / 2.0),
}

def hex_to_rgb(hex_str: str) -> RGB:
    h = hex_str.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

def lerp_rgb(c1: RGB, c2: RGB, t: float) -> RGB:
    t = max(0.0, min(1.0, t))
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )

def ansi_fg(rgb: RGB, text: str) -> str:
    return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{text}"
