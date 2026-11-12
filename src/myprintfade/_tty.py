import os
import sys
from contextlib import contextmanager
from typing import TextIO

def resolve_stream(use_tty: bool = False) -> TextIO:
    """Returns sys.stdout by default, or direct /dev/tty handle when isolating MCP stdio."""
    if not use_tty:
        return sys.stdout
    try:
        if os.name == "nt":
            return open("CONOUT$", "w", encoding="utf-8")
        return open("/dev/tty", "w", encoding="utf-8")
    except OSError:
        return sys.stderr

@contextmanager
def hidden_cursor(stream: TextIO | None = None):
    """Hides the terminal cursor during animations and restores it safely on exit."""
    target = stream or sys.stdout
    target.write("\033[?25l")
    target.flush()
    try:
        yield target
    finally:
        target.write("\033[?25h\033[0m")
        target.flush()
