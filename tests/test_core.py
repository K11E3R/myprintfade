from myprintfade._color import hex_to_rgb, lerp_rgb
from myprintfade.themes import THEMES

def test_color_lerp():
    c1 = hex_to_rgb("#000000")
    c2 = hex_to_rgb("#FFFFFF")
    mid = lerp_rgb(c1, c2, 0.5)
    assert mid == (127, 127, 127)

def test_themes_exist():
    assert "cyberpunk" in THEMES
    assert "matrix" in THEMES
