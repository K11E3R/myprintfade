import asyncio
from .core import fade_banner, print_fade
from .stream import AsyncTokenFader
from .themes import THEMES
from .widgets import fade_diff, fade_meter

try:
    from fastmcp import FastMCP
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise RuntimeError(
            "MCP support requires 'fastmcp'. Install with: pip install 'myprintfade[mcp]'"
        ) from exc

mcp = FastMCP("myprintfade-v2")

@mcp.resource("printfade://themes")
def get_themes() -> dict:
    """Returns all available TrueColor gradient palettes."""
    return THEMES

@mcp.tool()
def render_fade_text(text: str, mode: str = "glitch", theme: str = "cyberpunk") -> str:
    """Renders a 1D TrueColor wave or glitch-cipher text fade to the active terminal (/dev/tty)."""
    print_fade(text, mode=mode, theme=theme, use_tty=True)
    return f"Displayed '{mode}' fade on /dev/tty."

@mcp.tool()
def render_fade_banner(banner_text: str, theme: str = "cyberpunk", mode: str = "radial") -> str:
    """Renders a 2D shader-style multi-line ASCII banner fade to the terminal (/dev/tty)."""
    fade_banner(banner_text, theme=theme, mode=mode, use_tty=True)
    return "Displayed 2D banner on /dev/tty."

@mcp.tool()
def render_code_diff(unified_diff: str) -> str:
    """Cross-fades removed (-) lines out to dim red and added (+) lines in to neon green on /dev/tty."""
    fade_diff(unified_diff, use_tty=True)
    return "Cross-faded code diff on /dev/tty."

@mcp.tool()
def render_heatmap_meter(label: str, percentage: float) -> str:
    """Animates a 240-step sub-pixel TrueColor heatmap bar on /dev/tty."""
    fade_meter(label, target_pct=percentage, use_tty=True)
    return f"Rendered meter '{label}' at {percentage}% on /dev/tty."

@mcp.tool()
async def stream_agent_thought(thought_text: str, theme: str = "matrix") -> str:
    """Streams an agent thought at 60 FPS using AsyncTokenFader on /dev/tty."""
    async with AsyncTokenFader(theme=theme, use_tty=True) as fader:
        words = thought_text.split(" ")
        for i, word in enumerate(words):
            fader.push(word + (" " if i < len(words) - 1 else ""))
            await asyncio.sleep(0.03)
    return "Streamed agent thought to /dev/tty."

def run_server():
    mcp.run()

if __name__ == "__main__":
    run_server()
