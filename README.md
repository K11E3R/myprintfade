# myprintfade v2.0

Next-gen **24-bit TrueColor terminal fade engine**, **TUI widgets**, **60 FPS async LLM token streamer**, and **Model Context Protocol (MCP)** visual telemetry server.

Fully backward-compatible with `myprintfade` v0.2 (`from myprintfade import print_fade`), upgraded with zero external dependencies for the core engine.

## Features in v2.0
- **1D Wavefront & Glitch Cipher Reveal (`print_fade`)**: Sliding-window TrueColor interpolation with cubic/sine easing and Matrix/Cyberpunk cipher decoding.
- **2D Shader ASCII Banner Fading (`fade_banner`)**: Radial shockwave and diagonal plasma sweeps across multi-line text blocks.
- **Animated Code Diffs (`fade_diff`)**: Simultaneous cross-fade for unified diffs (`-` lines fade to dim ash, `+` lines brighten to neon emerald).
- **240-Step Sub-Pixel Heatmap Meter (`fade_meter`)**: Uses Unicode eighth-blocks (`▏▎▍▌▋▊▉█`) with TrueColor gradients.
- **Zero-Friction `@fade_task` Decorator**: Non-blocking background shimmer spinner that morphs into a completion badge on exit.
- **MCP Server (`myprintfade-mcp`)**: Safely routes live terminal animations to `/dev/tty` (`CONOUT$` on Windows) so `sys.stdout` JSON-RPC streams remain 100% uncorrupted.

## Installation

```bash
# Core library + CLI (Zero external dependencies)
pip install myprintfade

# With Model Context Protocol (MCP) server support
pip install "myprintfade[mcp]"
```

## Quick Start (Python API)

```python
import myprintfade as mpf

# 1. Classic v0.2 call (100% backward compatible)
mpf.print_fade("Hello, World!", delay=0.03, fade_steps=10)

# 2. v2.0 Glitch Cipher Reveal with Theme
mpf.print_fade("ACCESS GRANTED // NODE 04", mode="glitch", theme="cyberpunk")

# 3. 2D Radial Shader Multi-Line Banner
mpf.fade_banner("╔════════════════════╗\n║  MYPRINTFADE v2.0  ║\n╚════════════════════╝", theme="matrix", mode="radial")

# 4. Sub-character TrueColor Heatmap Meter
mpf.fade_meter("VRAM Allocation", target_pct=84.5)

# 5. Animated Unified Code Diff
mpf.fade_diff("- return token == 'secret'\n+ return hmac.compare_digest(token, secret)")

# 6. Background Task Decorator
@mpf.fade_task("Syncing product catalog")
def sync():
    import time; time.sleep(1.2)
sync()
```

## Command-Line Interface (CLI)

```bash
myprintfade "Deploying container stack..." --mode glitch --theme matrix
git diff HEAD~1 | myprintfade --mode diff
myprintfade "VRAM Usage" --meter 82.5
```

## MCP Server Configuration (Claude Desktop / Cursor / FastMCP)

Add to your `claude_desktop_config.json` or MCP client config:

```json
{
  "mcpServers": {
    "myprintfade": {
      "command": "myprintfade-mcp"
    }
  }
}
```
