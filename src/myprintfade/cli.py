import argparse
import sys
from .core import fade_banner, print_fade
from .themes import THEMES
from .widgets import fade_diff, fade_meter

def main():
    parser = argparse.ArgumentParser(description="myprintfade v2.0 — TrueColor CLI Fade Engine")
    parser.add_argument("text", nargs="?", help="Text or message to fade (reads stdin if omitted)")
    parser.add_argument("-m", "--mode", choices=["wave", "glitch", "sequential", "block", "banner", "diff"], default="wave")
    parser.add_argument("-t", "--theme", choices=list(THEMES.keys()), default="cyberpunk")
    parser.add_argument("-s", "--steps", type=int, default=12, help="Fade interpolation steps")
    parser.add_argument("-d", "--delay", type=float, default=0.02, help="Frame delay in seconds")
    parser.add_argument("--meter", type=float, metavar="PCT", help="Render a heatmap meter (0-100%%) using TEXT as label")

    args = parser.parse_args()
    content = args.text if args.text is not None else sys.stdin.read().rstrip("\n")

    if args.meter is not None:
        fade_meter(label=content or "Progress", target_pct=args.meter)
    elif args.mode == "banner":
        fade_banner(content, theme=args.theme, steps=args.steps)
    elif args.mode == "diff":
        fade_diff(content, steps=args.steps)
    else:
        print_fade(content, delay=args.delay, fade_steps=args.steps, mode=args.mode, theme=args.theme)

if __name__ == "__main__":
    main()
