import asyncio
import math
import time
from ._color import ansi_fg, lerp_rgb
from ._tty import hidden_cursor, resolve_stream

BLOCKS = [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]

def fade_diff(diff_text: str, steps: int = 18, fps: int = 45, use_tty: bool = False) -> None:
    """Cross-fades unified diff lines: (-) bright crimson -> dim ash, (+) dark green -> neon emerald."""
    stream = resolve_stream(use_tty)
    lines = diff_text.strip().splitlines()
    if not lines:
        return
    n = len(lines)

    with hidden_cursor(stream):
        for step in range(1, steps + 1):
            t = 1.0 - (1.0 - (step / steps)) ** 3
            out = []
            for line in lines:
                if line.startswith("-"):
                    rgb = lerp_rgb((255, 50, 80), (90, 35, 45), t)
                elif line.startswith("+"):
                    rgb = lerp_rgb((15, 40, 25), (0, 255, 136), t)
                else:
                    rgb = (150, 160, 175)
                out.append(f"{ansi_fg(rgb, line)}\033[0m\033[K")

            stream.write("\n".join(out))
            stream.flush()
            time.sleep(1.0 / max(1, fps))
            if step < steps and n > 1:
                stream.write(f"\033[{n - 1}A\r")
            elif step < steps:
                stream.write("\r")
        stream.write("\n")
        stream.flush()


def fade_meter(
    label: str,
    target_pct: float,
    width: int = 30,
    steps: int = 24,
    use_tty: bool = False,
) -> None:
    """Animates a sub-character (240-step) TrueColor heatmap bar from 0% to target_pct."""
    stream = resolve_stream(use_tty)
    target_pct = max(0.0, min(100.0, target_pct))

    with hidden_cursor(stream):
        for s in range(1, steps + 1):
            cur_pct = target_pct * (1.0 - (1.0 - s / steps) ** 3)
            filled_exact = (cur_pct / 100.0) * width
            full_cells = int(filled_exact)
            rem_idx = int((filled_exact - full_cells) * 8)

            bar_visual = []
            for cell in range(width):
                ratio = cell / max(1, width - 1)
                if ratio < 0.5:
                    rgb = lerp_rgb((0, 255, 136), (255, 170, 0), ratio * 2.0)
                else:
                    rgb = lerp_rgb((255, 170, 0), (255, 34, 85), (ratio - 0.5) * 2.0)

                if cell < full_cells:
                    bar_visual.append(ansi_fg(rgb, "█"))
                elif cell == full_cells and rem_idx > 0:
                    bar_visual.append(ansi_fg(rgb, BLOCKS[rem_idx]))
                else:
                    bar_visual.append(ansi_fg((45, 50, 60), "─"))

            stream.write(
                f"\r  \033[1m{label:<18}\033[0m │{''.join(bar_visual)}\033[0m│ "
                f"\033[1m{cur_pct:5.1f}%\033[0m"
            )
            stream.flush()
            time.sleep(0.018)
        stream.write("\n")
        stream.flush()


class MultiAgentHUD:
    """Pins N agent rows in the terminal and animates their status states concurrently."""
    def __init__(self, agents: list[dict[str, str]], use_tty: bool = False):
        self.agents = agents
        self.stream = resolve_stream(use_tty)

    async def run_for(self, duration: float = 2.5):
        t0 = time.perf_counter()
        num_rows = len(self.agents)
        with hidden_cursor(self.stream):
            while (time.perf_counter() - t0) < duration:
                el = time.perf_counter() - t0
                lines = []
                for idx, ag in enumerate(self.agents):
                    w = 0.5 * (math.sin(el * 6.0 - idx * 0.8) + 1.0)
                    state = ag.get("state", "idle")
                    if state == "done":
                        badge = ansi_fg((0, 255, 136), "✔ [DONE]  ")
                        msg = ansi_fg((110, 220, 160), ag["status"])
                    elif state == "active":
                        rgb = lerp_rgb((0, 240, 255), (255, 0, 127), w)
                        badge = ansi_fg(rgb, "◈ [ACTIVE]")
                        msg = ansi_fg(rgb, ag["status"])
                    else:
                        g = int(68 + 68 * w)
                        badge = ansi_fg((g, g, g), "○ [IDLE]  ")
                        msg = ansi_fg((g, g, g), ag["status"])
                    lines.append(f"  {badge}\033[0m \033[1m{ag['name']:<12}\033[0m │ {msg}\033[0m\033[K")

                self.stream.write("\n".join(lines) + "\n")
                self.stream.flush()
                await asyncio.sleep(1.0 / 30.0)
                self.stream.write(f"\033[{num_rows}A\r")
            self.stream.write(f"\033[{num_rows}B\n")
            self.stream.flush()
