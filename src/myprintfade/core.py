import math
import random
import time
from ._color import EASINGS, ansi_fg, hex_to_rgb, lerp_rgb
from ._tty import hidden_cursor, resolve_stream
from .themes import THEMES

GLITCH_GLYPHS = "01#$%&*@!?<>~^/+"

def print_fade(
    message: str,
    delay: float = 0.02,
    fade_steps: int = 12,
    mode: str = "wave",
    theme: str = "cyberpunk",
    start_color: str | None = None,
    end_color: str | None = None,
    gradient_end_color: str | None = None,
    easing: str = "ease_out",
    fade_out: bool = False,
    hold_time: float = 0.6,
    use_tty: bool = False,
) -> None:
    """
    1D TrueColor terminal fade engine. Backward-compatible with myprintfade v0.2.
    Modes: 'wave', 'glitch', 'sequential', 'block'.
    """
    stream = resolve_stream(use_tty)
    t_bg, t_mid, t_fg = THEMES.get(theme, THEMES["cyberpunk"])
    c_start = hex_to_rgb(start_color or t_bg)
    c_end = hex_to_rgb(end_color or t_mid)
    c_grad = hex_to_rgb(gradient_end_color or t_fg)
    ease_fn = EASINGS.get(easing, EASINGS["ease_out"])
    n = len(message)

    if n == 0:
        stream.write("\n")
        stream.flush()
        return

    with hidden_cursor(stream):
        if mode == "sequential":
            locked = ""
            for i, ch in enumerate(message):
                target_rgb = lerp_rgb(c_end, c_grad, i / max(1, n - 1))
                if ch == " ":
                    locked += " "
                    continue
                for step in range(1, fade_steps + 1):
                    t = ease_fn(step / fade_steps)
                    cur_rgb = lerp_rgb(c_start, target_rgb, t)
                    stream.write(f"\r{locked}{ansi_fg(cur_rgb, ch)}\033[0m")
                    stream.flush()
                    time.sleep(delay / max(1, fade_steps))
                locked += ansi_fg(target_rgb, ch)

        elif mode in ("wave", "glitch"):
            total_frames = n + fade_steps
            for frame in range(1, total_frames + 1):
                buf = []
                for i, ch in enumerate(message):
                    if ch == " ":
                        buf.append(" ")
                        continue
                    c_step = frame - i
                    target_rgb = lerp_rgb(c_end, c_grad, i / max(1, n - 1))
                    if c_step <= 0:
                        continue
                    elif c_step < fade_steps:
                        t = ease_fn(c_step / fade_steps)
                        cur_rgb = lerp_rgb(c_start, target_rgb, t)
                        disp = random.choice(GLITCH_GLYPHS) if (mode == "glitch" and t < 0.75) else ch
                        buf.append(ansi_fg(cur_rgb, disp))
                    else:
                        buf.append(ansi_fg(target_rgb, ch))
                stream.write("\r" + "".join(buf) + "\033[0m")
                stream.flush()
                time.sleep(delay)

        elif mode == "block":
            for step in range(1, fade_steps + 1):
                t = ease_fn(step / fade_steps)
                buf = []
                for i, ch in enumerate(message):
                    target_rgb = lerp_rgb(c_end, c_grad, i / max(1, n - 1))
                    cur_rgb = lerp_rgb(c_start, target_rgb, t)
                    buf.append(ansi_fg(cur_rgb, ch))
                stream.write("\r" + "".join(buf) + "\033[0m")
                stream.flush()
                time.sleep(delay)

        if fade_out:
            time.sleep(hold_time)
            for step in range(fade_steps, -1, -1):
                t = ease_fn(step / max(1, fade_steps))
                buf = []
                for i, ch in enumerate(message):
                    target_rgb = lerp_rgb(c_end, c_grad, i / max(1, n - 1))
                    cur_rgb = lerp_rgb(c_start, target_rgb, t)
                    buf.append(ansi_fg(cur_rgb, ch))
                stream.write("\r" + "".join(buf) + "\033[0m")
                stream.flush()
                time.sleep(delay)
            stream.write("\r" + (" " * n) + "\r")
        else:
            stream.write("\n")
        stream.flush()


def fade_banner(
    banner_text: str,
    theme: str = "cyberpunk",
    mode: str = "radial",
    steps: int = 24,
    fps: int = 45,
    use_tty: bool = False,
) -> None:
    """Renders a 2D shader-style multi-line ASCII banner fade in-place."""
    stream = resolve_stream(use_tty)
    bg_hex, mid_hex, fg_hex = THEMES.get(theme, THEMES["cyberpunk"])
    c_bg, c_mid, c_fg = hex_to_rgb(bg_hex), hex_to_rgb(mid_hex), hex_to_rgb(fg_hex)

    lines = banner_text.splitlines() or [banner_text]
    height = len(lines)
    width = max((len(line) for line in lines), default=1)
    cx, cy = width / 2.0, height / 2.0
    max_dist = math.hypot(cx, cy) or 1.0

    with hidden_cursor(stream):
        for step in range(1, steps + 1):
            progress = step / steps
            out_lines = []
            for y, line in enumerate(lines):
                row_buf = []
                for x, ch in enumerate(line):
                    if ch == " ":
                        row_buf.append(" ")
                        continue
                    if mode == "radial":
                        dist = math.hypot((x - cx) * 0.5, y - cy) / max_dist
                        local_t = (progress * 1.6) - (dist * 0.6)
                    else:
                        diag = ((x / max(1, width)) + (y / max(1, height))) * 0.5
                        local_t = (progress * 1.5) - (diag * 0.5)

                    local_t = max(0.0, min(1.0, local_t))
                    if local_t <= 0.0:
                        row_buf.append(" ")
                    elif local_t < 0.6:
                        rgb = lerp_rgb(c_bg, c_mid, local_t / 0.6)
                        g_ch = random.choice(GLITCH_GLYPHS) if local_t < 0.35 else ch
                        row_buf.append(ansi_fg(rgb, g_ch))
                    else:
                        rgb = lerp_rgb(c_mid, c_fg, (local_t - 0.6) / 0.4)
                        row_buf.append(ansi_fg(rgb, ch))
                out_lines.append("".join(row_buf) + "\033[0m")

            stream.write("\n".join(out_lines))
            stream.flush()
            time.sleep(1.0 / max(1, fps))
            if step < steps:
                if height > 1:
                    stream.write(f"\033[{height - 1}A\r")
                else:
                    stream.write("\r")
        stream.write("\n")
        stream.flush()
