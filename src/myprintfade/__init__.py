"""
myprintfade v2.0 — TrueColor Terminal Fade Engine, TUI Widgets & MCP Telemetry
"""

from .core import print_fade, fade_banner
from .widgets import fade_diff, fade_meter, MultiAgentHUD
from .decorators import fade_task
from .stream import AsyncTokenFader
from .themes import THEMES

__version__ = "2.0.0"

__all__ = [
    "print_fade",
    "fade_banner",
    "fade_diff",
    "fade_meter",
    "MultiAgentHUD",
    "fade_task",
    "AsyncTokenFader",
    "THEMES",
]
