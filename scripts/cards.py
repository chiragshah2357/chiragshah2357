"""Project cards.

Two shapes. One featured card (1000 x 260) for the headline project, with its numbers in a column of
their own; four smaller cards (480 x 272) laid out two-up. Every card carries a kicker, a title, a short
description, a stat strip of verified numbers, stack chips and a small glyph.

Motion is kept to the two glyphs where it means something (the flood waves, the FAIL/PASS swap) plus the
live dot on the deployed project. Everything else is static.
"""
import fonts
from common import THEMES, card_bg, esc, svg

W, H = 480, 272            # small card
FW, FH = 1000, 260         # featured card
INNER = 424
BODY_W = 300               # description column on a small card; the glyph sits to its right
BODY_WF = 560              # description column on the featured card
CHAR = 14 * 0.6            # mono advance at 14px
CHARF = 15 * 0.6

CARDS = [
    dict(key="leak", featured=True, kicker="ALPACA × LABLAB.AI HACKATHON", title="Liquidity Leak",
         body="An agent that holds a long equity book and defends it with options. "
              "Every risk cap is enforced in code, after the model decides.",
         note="Four calm sessions — the return is mostly book beta, not the overlay.",
         stats=[("+6.5%", "net return, 4 paper sessions"), ("114", "tests"), ("0", "runtime dependencies")],
         chips=["Python", "DeepSeek Harness", "Alpaca", "MCP"], repo="Alpaca-Trading-Hackathon-Final"),
    dict(key="review", kicker="IBM BOB 2.0 HACKATHON", title="Proof-Carrying Review",
         body="A reviewer that reports a bug only when it can prove it with a failing test. No proof, no comment.",
         stat="100% precision · 0 false alarms · 81% recall",
         chips=["Python", "IBM Bob 2.0", "pytest"], repo="IBM-Bob-2.0-Hackathon"),
    dict(key="flood", kicker="COMMIT FOR GOOD HACKATHON", title="Flood-Ready Access",
         body="When floods cut the roads, which villages lose their clinic, and where should medicine go?",
         stat="1,188 villages · 60 floods · 44 tests",
         chips=["Python", "SciPy", "FastAPI", "React"], repo="Commit-for-Good---Kernel-Panic"),
    dict(key="mlproj", kicker="END-TO-END ML · DEPLOYED", title="Exam Score Predictor",
         body="Predicts a student's exam score. Seven regressors compared, then packaged and deployed.",
         stat="7 models · GridSearchCV · live demo",
         chips=["scikit-learn", "Flask", "Render"], repo="FirstMlProject"),
    dict(key="fifa", kicker="DATA SCIENCE", title="World Cup 2026 Predictor",
         body="Chronological ELO from 1980, plus a Poisson model for odds and the likeliest scoreline.",
         stat="1980 onward · ELO + Poisson",
         chips=["Python", "SciPy", "Jupyter"], repo="Fifa-World-Cup-Prediction-2026"),
]

CSS = (".flow{stroke-dasharray:6 6;animation:flow 1.6s linear infinite}@keyframes flow{to{stroke-dashoffset:-24}}"
       ".swapA{animation:sa 4.4s infinite}.swapB{animation:sb 4.4s infinite}"
       "@keyframes sa{0%,45%{opacity:1}55%,100%{opacity:0}}@keyframes sb{0%,45%{opacity:0}55%,100%{opacity:1}}"
       ".live{animation:live 2.4s ease-in-out infinite}@keyframes live{0%,100%{opacity:1}50%{opacity:.3}}")


def wrap(text, per_line):
    lines, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + (1 if cur else 0) <= per_line:
            cur = f"{cur} {w}".strip()
        else:
            lines.append(cur)
            cur = w
    return lines + [cur]


def glyph(key, t):
    ink2, ink3, acc, flood, ok, warn, panel2 = t["ink2"], t["ink3"], t["accent"], t["flood"], t["ok"], t["warn"], t["panel2"]
    if key == "flood":
        waves = "".join(f'<path d="M54,{y} q4,-6 8,0 t8,0 t8,0 t8,0" fill="none" stroke="{flood}" stroke-width="2" '
                        f'stroke-linecap="round" class="flow" style="animation-delay:{i * 0.4}s"/>'
                        for i, y in enumerate((30, 40, 50)))
        return (f'<path d="M2,58 L28,58 L44,38 L58,38" fill="none" stroke="{ink2}" stroke-width="3.5" stroke-linecap="round"/>'
                f'<path d="M78,38 L92,54 L98,54" fill="none" stroke="{ink3}" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="1 7"/>'
                f'{waves}<circle cx="3" cy="58" r="5" fill="{ok}"/><circle cx="97" cy="54" r="6" fill="{acc}"/>'
                f'<path d="M64,33 l8,10 m0,-10 l-8,10" stroke="{acc}" stroke-width="2.5" stroke-linecap="round"/>')
    if key == "review":
        return (f'<rect x="0" y="4" width="100" height="68" rx="9" fill="{panel2}" stroke="{ink3}"/>'
                f'<rect x="12" y="16" width="46" height="5" rx="2.5" fill="{ink3}" opacity="0.6"/>'
                f'<rect x="12" y="28" width="70" height="5" rx="2.5" fill="{acc}" opacity="0.9"/>'
                f'<rect x="12" y="40" width="38" height="5" rx="2.5" fill="{ink3}" opacity="0.6"/>'
                f'<g class="swapA"><rect x="48" y="50" width="42" height="17" rx="8.5" fill="{acc}" fill-opacity="0.2" stroke="{acc}"/>'
                f'<text x="69" y="62.4" text-anchor="middle" class="mb" font-size="11" fill="{acc}">FAIL</text></g>'
                f'<g class="swapB"><rect x="48" y="50" width="42" height="17" rx="8.5" fill="{ok}" fill-opacity="0.2" stroke="{ok}"/>'
                f'<text x="69" y="62.4" text-anchor="middle" class="mb" font-size="11" fill="{ok}">PASS</text></g>')
    if key == "mlproj":   # a served model: window, trend line, live dot
        return (f'<rect x="0" y="6" width="100" height="64" rx="8" fill="{panel2}" stroke="{ink3}"/>'
                f'<line x1="0" y1="24" x2="100" y2="24" stroke="{ink3}"/>'
                f'<circle cx="12" cy="15" r="3.4" fill="{ok}" class="live"/>'
                f'<polyline points="14,60 30,51 46,54 62,40 78,44 92,32" fill="none" stroke="{acc}" stroke-width="2.4" '
                f'stroke-linecap="round" stroke-linejoin="round"/>'
                f'<circle cx="92" cy="32" r="4" fill="{acc}"/>')
    if key == "fifa":     # an ELO ladder
        cols = [flood, acc, ok, warn, t["violet"]]
        return "".join(f'<rect x="2" y="{6 + i * 14}" width="{w}" height="9" rx="4.5" fill="{cols[i]}" fill-opacity="0.85"/>'
                       for i, w in enumerate((92, 76, 62, 46, 30)))
    return ""


def _chrome(t, w, h, r=18):
    """Panel, corner wash and the clip/gradient defs every card shares."""
    body = [card_bg(w, h, t, r=r), f'<g clip-path="url(#cc)"><rect width="{w}" height="{h}" fill="url(#cg)"/></g>']
    defs = (f'<clipPath id="cc"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>'
            f'<radialGradient id="cg" cx="0.9" cy="0.05" r="0.7"><stop offset="0" stop-color="{t["accent"]}" stop-opacity="0.13"/>'
            f'<stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></radialGradient>')
    return body, defs


def _open_link(t, w, h):
    """The 'open ↗' affordance in the bottom-right corner."""
    ax = w - 28 - fonts.measure("monob", "open", 13) - 22
    return (f'<text x="{w - 28}" y="{h - 27.5}" text-anchor="end" class="mb" font-size="13" fill="{t["ink"]}">open</text>'
            f'<path d="M{ax},{h - 21} L{ax + 10},{h - 31} M{ax + 2},{h - 31} H{ax + 10} V{h - 23}" fill="none" '
            f'stroke="{t["accent"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')


def _chips(t, items, y, size=12):
    out, x = [], 28
    for ch in items:
        w = fonts.measure("mono", ch, size) + 20
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="24" rx="12" fill="none" stroke="{t["ink3"]}" stroke-opacity="0.8"/>'
                   f'<text x="{x + w / 2:.1f}" y="{y + 16.5}" text-anchor="middle" class="m" font-size="{size}" fill="{t["ink2"]}">{esc(ch)}</text>')
        x += w + 8
    return "".join(out)


def featured(theme, c):
    """The headline card: text on the left, a column of verified numbers on the right.

    The height follows the text rather than the other way round, so a longer description pushes the card
    taller instead of being quietly clipped.
    """
    t = THEMES[theme]
    lines = wrap(c["body"], int(BODY_WF // CHARF))
    note_y = 140 + (len(lines) - 1) * 23 + 30
    chips_y = note_y + 18
    h = max(FH, chips_y + 48)
    body, defs = _chrome(t, FW, h, r=20)
    body.append(f'<text x="36" y="46" class="m" font-size="12" fill="{t["accent"]}" letter-spacing="1.6">{esc(c["kicker"])}</text>')
    body.append(f'<text x="36" y="104" class="s" font-size="46" fill="{t["ink"]}" letter-spacing="-1">{esc(c["title"])}</text>')
    for i, ln in enumerate(lines):
        body.append(f'<text x="36" y="{140 + i * 23}" class="m" font-size="15" fill="{t["ink2"]}">{esc(ln)}</text>')
    body.append(f'<text x="36" y="{note_y}" class="m" font-size="13" fill="{t["ink3"]}">{esc(c["note"])}</text>')
    body.append(_chips(t, c["chips"], chips_y))
    body.append(_open_link(t, FW, h))
    # the numbers, in their own column behind a rule
    body.append(f'<line x1="644" x2="644" y1="36" y2="{h - 36}" stroke="{t["rule"]}"/>')
    top = (h - (len(c["stats"]) - 1) * 58 - 44) / 2 + 26
    for i, (value, label) in enumerate(c["stats"]):
        y = top + i * 58
        body.append(f'<text x="692" y="{y:.0f}" class="s" font-size="34" fill="{t["ink"]}" letter-spacing="-0.8">{esc(value)}</text>')
        body.append(f'<text x="694" y="{y + 20:.0f}" class="m" font-size="12" fill="{t["ink2"]}" letter-spacing="0.4">{esc(label)}</text>')
    texts = {"serif": c["title"] + "".join(v for v, _ in c["stats"]) + "0123456789",
             "mono": c["kicker"] + c["body"] + c["note"] + "".join(l for _, l in c["stats"]) + "".join(c["chips"]) + "0123456789",
             "monob": "open"}
    return svg(FW, h, "".join(body), theme, texts, title=c["title"], desc=f'{c["body"]} {c["note"]}',
               css=CSS, defs=defs)


def card(theme, c):
    if c.get("featured"):
        return featured(theme, c)
    t = THEMES[theme]
    tsize = 33
    while tsize > 24 and fonts.measure("serif", c["title"], tsize) > INNER:
        tsize -= 1
    body, defs = _chrome(t, W, H, r=18)
    body.append(f'<text x="28" y="40" class="m" font-size="12" fill="{t["accent"]}" letter-spacing="1.6">{esc(c["kicker"])}</text>')
    body.append(f'<text x="28" y="84" class="s" font-size="{tsize}" fill="{t["ink"]}" letter-spacing="-0.6">{esc(c["title"])}</text>')
    body.append(f'<g transform="translate({W - 28 - 100},100)">{glyph(c["key"], t)}</g>')
    for i, ln in enumerate(wrap(c["body"], int(BODY_W // CHAR))[:3]):
        body.append(f'<text x="28" y="{116 + i * 21}" class="m" font-size="14" fill="{t["ink2"]}">{esc(ln)}</text>')
    # stat strip
    body.append(f'<line x1="28" x2="{W - 28}" y1="194" y2="194" stroke="{t["rule"]}"/>')
    body.append(f'<text x="28" y="216" class="mb" font-size="13" fill="{t["accent"]}">{esc(c["stat"])}</text>')
    body.append(_chips(t, c["chips"], H - 44))
    body.append(_open_link(t, W, H))
    texts = {"serif": c["title"],
             "mono": c["kicker"] + c["body"] + "".join(c["chips"]) + "0123456789",
             "monob": "FAILPASSopen" + c["stat"]}
    return svg(W, H, "".join(body), theme, texts, title=c["title"], desc=f'{c["body"]} {c["stat"]}',
               css=CSS, defs=defs)
