"""Embed fonts in SVGs.

GitHub shows README images as plain <img>, which cannot load web fonts, so every SVG carries its own fonts as a base64
@font-face. To keep each file small, a variable font is pinned to one weight and subset to just the characters that SVG uses.
The source fonts (SIL Open Font Licence 1.1) are in assets/fonts/.
"""
import base64
import io
from functools import lru_cache
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

SRC = Path(__file__).resolve().parent.parent / "assets" / "fonts"

# key -> (file, axis values, CSS family name, CSS weight, CSS style)
SPECS = {
    "serif":  ("fraunces-latin-full-normal.woff2", {"wght": 600, "opsz": 72, "SOFT": 0, "WONK": 0}, "KPSerif", 600, "normal"),
    "serifi": ("fraunces-latin-full-italic.woff2", {"wght": 380, "opsz": 72, "SOFT": 0, "WONK": 1}, "KPSerif", 400, "italic"),
    "mono":   ("jetbrains-mono-latin-wght-normal.woff2", {"wght": 450}, "KPMono", 400, "normal"),
    "monob":  ("jetbrains-mono-latin-wght-normal.woff2", {"wght": 800}, "KPMono", 800, "normal"),
}


@lru_cache(maxsize=None)
def _instance(key: str) -> bytes:
    file, axes, *_ = SPECS[key]
    font = TTFont(SRC / file, recalcTimestamp=False)   # recalcTimestamp=False: otherwise "modified" is stamped with the clock and every build differs
    present = {a.axisTag for a in font["fvar"].axes}
    font = instancer.instantiateVariableFont(font, {k: v for k, v in axes.items() if k in present}, inplace=False)
    buf = io.BytesIO()
    font.flavor = None
    font.save(buf)
    return buf.getvalue()


def face(key: str, text: str) -> str:
    """One @font-face rule holding `text`'s glyphs only."""
    _, _, family, weight, style = SPECS[key]
    chars = "".join(sorted(set(text) | set(" .,-")))
    font = TTFont(io.BytesIO(_instance(key)), recalcTimestamp=False)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga"]
    opts.name_IDs = []
    opts.notdef_outline = False
    opts.hinting = False
    sub = subset.Subsetter(opts)
    sub.populate(text=chars)
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"@font-face{{font-family:{family};font-weight:{weight};font-style:{style};src:url(data:font/woff2;base64,{b64}) format('woff2')}}"


def faces(text_by_key: dict) -> str:
    return "".join(face(k, t) for k, t in text_by_key.items() if t)


@lru_cache(maxsize=None)
def _metrics(key: str):
    font = TTFont(io.BytesIO(_instance(key)), recalcTimestamp=False)
    return font.getBestCmap(), font["hmtx"], font["head"].unitsPerEm


def measure(key: str, text: str, size: float) -> float:
    """Advance width of `text` in px (no kerning), so layouts can be computed instead of guessed."""
    cmap, hmtx, upm = _metrics(key)
    return sum(hmtx[cmap.get(ord(c), ".notdef")][0] for c in text) * size / upm
