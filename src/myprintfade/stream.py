import asyncio
import time
from ._color import ansi_fg, hex_to_rgb, lerp_rgb
from ._tty import resolve_stream
from .themes import THEMES

class AsyncTokenFader:
    """60 FPS ring-buffer token fader for live streaming LLM chunks."""
    def __init__(self, theme: str = "cyberpunk", fade_duration: float = 0.22, use_tty: bool = False):
        self.theme = theme
        self.fade_duration = fade_duration
        self.stream = resolve_stream(use_tty)
        self.buffer: list[tuple[str, float]] = []
        self._running = False
        self._task: asyncio.Task | None = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def start(self):
        self._running = True
        self.stream.write("\033[?25l")
        self.stream.flush()
        self._task = asyncio.create_task(self._render_loop())

    def push(self, token: str):
        now = time.perf_counter()
        for idx, ch in enumerate(token):
            self.buffer.append((ch, now + idx * 0.008))

    async def _render_loop(self):
        bg_hex, mid_hex, fg_hex = THEMES.get(self.theme, THEMES["cyberpunk"])
        c_bg, c_mid, c_fg = hex_to_rgb(bg_hex), hex_to_rgb(mid_hex), hex_to_rgb(fg_hex)

        while self._running:
            now = time.perf_counter()
            frame_chars = []
            for ch, t0 in self.buffer:
                age = now - t0
                if age < 0:
                    continue
                t = min(1.0, age / max(0.01, self.fade_duration))
                if t < 0.5:
                    rgb = lerp_rgb(c_bg, c_mid, t * 2.0)
                elif t < 1.0:
                    rgb = lerp_rgb(c_mid, c_fg, (t - 0.5) * 2.0)
                else:
                    rgb = c_fg
                frame_chars.append(ansi_fg(rgb, ch))

            self.stream.write("\r" + "".join(frame_chars) + "\033[0m")
            self.stream.flush()
            await asyncio.sleep(1.0 / 60.0)

    async def close(self):
        await asyncio.sleep(self.fade_duration + 0.05)
        self._running = False
        if self._task:
            await self._task
        self.stream.write("\033[?25h\033[0m\n")
        self.stream.flush()
