import functools
import math
import threading
import time
from ._color import ansi_fg
from ._tty import hidden_cursor, resolve_stream

def fade_task(label: str, use_tty: bool = False):
    """Decorator that pulses a TrueColor shimmer while the wrapped function executes."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            stream = resolve_stream(use_tty)
            stop_event = threading.Event()
            start_time = time.perf_counter()

            def _pulse_worker():
                frame = 0
                while not stop_event.is_set():
                    frame += 1
                    el = time.perf_counter() - start_time
                    buf = []
                    for i, ch in enumerate(f"⟳ {label} ({el:.1f}s)"):
                        w = 0.5 * (math.sin(frame * 0.25 - i * 0.2) + 1.0)
                        rgb = (int(120 * w), int(140 + 115 * w), 255)
                        buf.append(ansi_fg(rgb, ch))
                    stream.write("\r" + "".join(buf) + "\033[0m\033[K")
                    stream.flush()
                    time.sleep(0.03)

            with hidden_cursor(stream):
                t = threading.Thread(target=_pulse_worker, daemon=True)
                t.start()
                try:
                    result = func(*args, **kwargs)
                    stop_event.set()
                    t.join()
                    total = time.perf_counter() - start_time
                    stream.write(f"\r{ansi_fg((0, 255, 136), f'✔ {label} — Done in {total:.2f}s')}\033[0m\033[K\n")
                    stream.flush()
                    return result
                except Exception as exc:
                    stop_event.set()
                    t.join()
                    stream.write(f"\r{ansi_fg((255, 50, 80), f'✖ {label} — Failed: {exc}')}\033[0m\033[K\n")
                    stream.flush()
                    raise
        return wrapper
    return decorator
