"""Section dividers, the activity heatmap and the contact buttons.

The language bar and the stack chips used to live here. The language bar was dropped (primary-language-per-repo
said less than one more project card) and the chips moved into background.py, which is now one merged panel.
"""
from datetime import date

import fonts
from common import THEMES, anim, card_bg, dots, esc, svg

W = 1000


# ------------------------------------------------------------------ section divider
def divider(theme, no, title, note=""):
    t = THEMES[theme]
    h = 76   # a panel of its own, so the title stays readable whatever colour the page behind it is
    tw = fonts.measure("serif", title, 38)
    x_line = 56 + 54 + tw + 24
    body = (card_bg(W, h, t, r=18) +
            f'<text x="36" y="49" class="mb" font-size="20" fill="{t["accent"]}">{no}</text>'
            f'<text x="90" y="52" class="s" font-size="38" fill="{t["ink"]}" letter-spacing="-0.5">{esc(title)}</text>'
            f'<line x1="{x_line - 20}" x2="{W - 36}" y1="40" y2="40" stroke="{t["rule"]}" stroke-width="1.5" stroke-dasharray="{W}" stroke-dashoffset="0">'
            f'<animate attributeName="stroke-dashoffset" from="{W}" to="0" dur="1.1s" fill="freeze"/></line>'
            f'<circle cx="{W - 36}" cy="40" r="4" fill="{t["accent"]}"/>')
    if note:
        body += f'<text x="{W - 36}" y="26" text-anchor="end" class="m" font-size="13" fill="{t["ink3"]}" letter-spacing="0.6">{esc(note)}</text>'
    return svg(W, h, body, theme, {"serif": title, "mono": note + "0123456789", "monob": no}, title=title)


# ------------------------------------------------------------------ activity heatmap + counters
def activity(theme, d):
    t = THEMES[theme]
    H = 396
    days = d["days"]
    first = date.fromisoformat(days[0][0])
    pad = (first.weekday() + 1) % 7            # GitHub weeks start on Sunday
    cells = [None] * pad + days
    cols = (len(cells) + 6) // 7
    left, avail = 56, W - 112
    step = avail / cols
    size = step - 3.2
    top = 196
    nz = sorted(n for _, n in days if n > 0)
    q = [nz[int(len(nz) * f)] for f in (0.25, 0.5, 0.75)] if nz else [1, 2, 3]

    def level(n):
        return 0 if n == 0 else 1 if n <= q[0] else 2 if n <= q[1] else 3 if n <= q[2] else 4

    op = {0: 0.0, 1: 0.30, 2: 0.55, 3: 0.78, 4: 1.0}
    body = [card_bg(W, H, t, r=22)]
    body.append(f'<text x="56" y="52" class="m" font-size="14" fill="{t["ink3"]}" letter-spacing="0.4">// last 12 months · contributions · live from the GitHub API</text>')
    blocks = [(d["total"], "contributions"), (d["commits"], "commits"), (d["prs"], "pull requests"), (d["issues"], "issues opened"), (d["active_days"], "active days")]
    for i, (n, label) in enumerate(blocks):
        x = 56 + i * 178
        body.append(f'<text x="{x}" y="118" class="s" font-size="62" fill="{t["ink"]}" letter-spacing="-1.5">{n}</text>')
        body.append(f'<text x="{x + 2}" y="146" class="m" font-size="14" fill="{t["ink2"]}" letter-spacing="0.5">{label}</text>')
    body.append(f'<line x1="56" x2="{W - 56}" y1="164" y2="164" stroke="{t["rule"]}"/>')
    # grid
    months = []
    for c in range(cols):
        for r in range(7):
            i = c * 7 + r
            if i >= len(cells) or cells[i] is None:
                continue
            ds, n = cells[i]
            x, y = left + c * step, top + r * step
            lv = level(n)
            delay = f"{c * 0.018:.3f}"
            if lv == 0:
                body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{size:.1f}" height="{size:.1f}" rx="3" fill="{t["rule"]}" opacity="0.55" class="c" style="animation-delay:{delay}s"/>')
            else:
                body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{size:.1f}" height="{size:.1f}" rx="3" fill="{t["accent"]}" fill-opacity="{op[lv]}" class="c" style="animation-delay:{delay}s"/>')
            if r == 0 and date.fromisoformat(ds).day <= 7:
                months.append((c, date.fromisoformat(ds).strftime("%b")))
    seen, last_c = [], -9
    for c, m in months:
        if c - last_c >= 3:
            seen.append((c, m))
            last_c = c
    for c, m in seen:
        body.append(f'<text x="{left + c * step:.1f}" y="{top + 7 * step + 18:.1f}" class="m" font-size="12" fill="{t["ink3"]}">{m}</text>')
    foot = (f'longest streak {d["longest_streak"]} days · busiest day {d["busiest"]["count"]} ({d["busiest"]["date"]})'
            f' · {d["open_issues"]} open issue{"" if d["open_issues"] == 1 else "s"}')
    body.append(f'<text x="56" y="{H - 22}" class="m" font-size="13" fill="{t["ink2"]}" letter-spacing="0.3">{foot}</text>')
    lx = W - 56 - 5 * 18 - 90
    body.append(f'<text x="{lx}" y="{H - 22}" text-anchor="end" class="m" font-size="12" fill="{t["ink3"]}">less</text>')
    for i, lv in enumerate((0, 1, 2, 3, 4)):
        fill = f'fill="{t["rule"]}" opacity="0.55"' if lv == 0 else f'fill="{t["accent"]}" fill-opacity="{op[lv]}"'
        body.append(f'<rect x="{lx + 10 + i * 18}" y="{H - 34}" width="13" height="13" rx="3" {fill}/>')
    body.append(f'<text x="{lx + 10 + 5 * 18 + 6}" y="{H - 22}" class="m" font-size="12" fill="{t["ink3"]}">more</text>')
    css = ".c{animation:pop .55s ease backwards}@keyframes pop{from{opacity:0;transform:scale(.4)}}.c{transform-box:fill-box;transform-origin:center}"
    texts = {"serif": "0123456789", "mono": "// last 12 months · contributions · live from the GitHub API contributions commits pull requests issues opened active days " + foot + " less more JanFebMarAprMayJunJulAugSepOctNovDec0123456789"}
    return svg(W, H, "".join(body), theme, texts, title="GitHub activity, last 12 months", css=css,
               desc=f'{d["total"]} contributions in the last year, {d["commits"]} commits, {d["prs"]} pull requests, {d["active_days"]} active days.')


# ------------------------------------------------------------------ contact buttons
def button(theme, label, kind="primary"):
    t = THEMES[theme]
    w, h = 24 + int(fonts.measure("monob", label, 18)) + 52, 54
    fill = t["ink"] if kind == "primary" else t["panel"]   # always a solid fill, so it reads on any page colour
    txt = t["bg"] if kind == "primary" else t["ink"]
    ax, ay = w - 40, h / 2 - 7
    body = (f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="27" fill="{fill}" stroke="{t["ink"]}" stroke-width="1.5"/>'
            f'<text x="26" y="{h / 2 + 6.5}" class="mb" font-size="18" fill="{txt}">{esc(label)}</text>'
            f'<path d="M{ax},{ay + 14} L{ax + 14},{ay} M{ax + 3},{ay} H{ax + 14} V{ay + 11}" fill="none" stroke="{t["accent"]}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    return svg(w, h, body, theme, {"monob": label}, title=label), w, h
