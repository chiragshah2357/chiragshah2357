"""Shared pieces for the SVG generators: palettes, the SVG wrapper that embeds fonts, and small helpers."""
import html
import re

import fonts

THEMES = {
    "dark": dict(bg="#0b0d10", panel="#12161b", panel2="#181d24", ink="#efe9dd", ink2="#b3ad9f", ink3="#767166", rule="#272d35",
                 accent="#ff5a36", flood="#5aa9ff", ok="#3fd0a0", warn="#f2b84b", violet="#a98bff"),
    "light": dict(bg="#f1ece1", panel="#fbf8f1", panel2="#f3eee3", ink="#14110f", ink2="#4a443c", ink3="#8a8377", rule="#d9d2c3",
                  accent="#d9381e", flood="#1d4e89", ok="#14876a", warn="#b87a10", violet="#6a4fd6"),
}
SERIF = "KPSerif,Georgia,'Times New Roman',serif"
MONO = "KPMono,ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def esc(s) -> str:
    return html.escape(str(s), quote=False)


def anim(attr, values, key_times=None, dur="1s", begin="0s", repeat="indefinite", fill="remove", extra=""):
    """A SMIL <animate>. `values` is a list; `key_times` a list in [0, 1] of the same length (or None for even spacing)."""
    v = ";".join(str(x) for x in values)
    kt = f' keyTimes="{";".join(f"{t:.4f}" for t in key_times)}"' if key_times else ""
    rep = f' repeatCount="{repeat}"' if repeat else ""
    return f'<animate attributeName="{attr}" values="{v}"{kt} dur="{dur}" begin="{begin}"{rep} fill="{fill}" {extra}/>'


def slot_times(i, n, total, ramp=0.012):
    """keyTimes + opacity values that show item i of n for its slice of a looping timeline."""
    a, b = i / n, (i + 1) / n
    if n == 1:
        return [0.0, 1.0], [1, 1]
    if i == 0:
        return [0.0, b - ramp, b, 1.0], [1, 1, 0, 0]
    if i == n - 1:
        return [0.0, a, a + ramp, 1.0], [0, 0, 1, 1]
    return [0.0, a, a + ramp, b - ramp, b, 1.0], [0, 0, 1, 1, 0, 0]


def svg(width, height, body, theme, texts, title="", desc="", css="", defs=""):
    """Wrap `body` in an <svg> with embedded fonts. `texts` maps font key -> every string drawn in it (for subsetting)."""
    t = THEMES[theme]
    faces = fonts.faces({k: "".join(v) if isinstance(v, (list, tuple)) else v for k, v in texts.items()})
    base = (f".s{{font-family:{SERIF};font-weight:600}}.si{{font-family:{SERIF};font-style:italic;font-weight:400}}"
            f".m{{font-family:{MONO};font-weight:400}}.mb{{font-family:{MONO};font-weight:800}}"
            "@media (prefers-reduced-motion:reduce){*{animation:none!important}}")
    head = f"<title>{esc(title)}</title>" if title else ""
    head += f"<desc>{esc(desc)}</desc>" if desc else ""
    out = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}" role="img">{head}<style>{faces}{base}{css}</style><defs>{defs}</defs>{body}</svg>')
    return re.sub(r">\s+<", "><", out)


def card_bg(w, h, t, r=18, stroke=True):
    s = f' stroke="{t["rule"]}" stroke-width="1"' if stroke else ""
    return f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{r}" fill="{t["panel"]}"{s}/>'


def dots(id_, t, step=20, r=1.0, op=0.8):
    return f'<pattern id="{id_}" width="{step}" height="{step}" patternUnits="userSpaceOnUse"><circle cx="{step / 2}" cy="{step / 2}" r="{r}" fill="{t["rule"]}" opacity="{op}"/></pattern>'
