"""Fold a dark and a light rendering of the same graphic into ONE svg that picks its theme itself.

GitHub's own dark/light image switches (`<picture>` inside links, the `#gh-dark-mode-only` fragments) are unreliable, so each image
carries both themes and shows one with a CSS media query inside the SVG. Both renderings come from the same generator, so they have
the same structure; only the ids need renaming so the two copies do not collide.
"""
import re

_SVG = re.compile(r"^(<svg [^>]*>)(.*?)<style>(.*?)</style><defs>(.*?)</defs>(.*)</svg>$", re.S)
_SWITCH = ".dk{display:none}@media (prefers-color-scheme:dark){.dk{display:inline}.lt{display:none}}"


def _suffix_ids(defs: str, body: str, suffix: str):
    sep = "\x00"
    text = defs + sep + body
    for i in set(re.findall(r'\bid="([^"]+)"', text)):
        text = (text.replace(f'id="{i}"', f'id="{i}{suffix}"').replace(f"url(#{i})", f"url(#{i}{suffix})")
                .replace(f'href="#{i}"', f'href="#{i}{suffix}"'))
    defs, body = text.split(sep)
    return defs, body


def merge_themes(dark: str, light: str) -> str:
    md, ml = _SVG.match(dark), _SVG.match(light)
    if not md or not ml:
        raise ValueError("unexpected svg layout")
    open_tag, head, style, defs_d, body_d = md.groups()
    defs_d, body_d = _suffix_ids(defs_d, body_d, "-d")
    _, _, _, defs_l, body_l = ml.groups()
    defs_l, body_l = _suffix_ids(defs_l, body_l, "-l")
    return (f"{open_tag}{head}<style>{style}{_SWITCH}</style><defs>{defs_d}{defs_l}</defs>"
            f'<g class="dk">{body_d}</g><g class="lt">{body_l}</g></svg>')
