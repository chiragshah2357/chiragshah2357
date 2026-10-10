"""The hero nameplate (1000 x 236): name revealed by a scanning bar, role line, tagline.

Deliberately compact so the project cards land above the fold. The only looping animation is the
status dot; the name reveal runs once and freezes.
"""
import fonts
from common import THEMES, anim, card_bg, dots, esc, svg

W, H = 1000, 236
ROLE = "ML / AI engineer · CS undergrad @ MUJ · ex-intern @ Protiviti"
TAG = "Teaching machines to read."
SUB = "RAG pipelines, agents, classical ML — the numbers say what is real."
STATUS = "BUILDING IN PUBLIC · MUMBAI"
EASE = 'calcMode="spline" keySplines=".6 0 .2 1" keyTimes="0;1"'


def hero(theme: str) -> str:
    t = THEMES[theme]
    defs = [dots("dots", t),
            f'<radialGradient id="glow" cx="0.88" cy="0.12" r="0.8"><stop offset="0" stop-color="{t["accent"]}" stop-opacity="0.18"/>'
            f'<stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></radialGradient>',
            f'<linearGradient id="scan" x1="0" x2="1"><stop offset="0" stop-color="{t["accent"]}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{t["accent"]}"/></linearGradient>',
            f'<clipPath id="panel"><rect width="{W}" height="{H}" rx="22"/></clipPath>']
    css = (".pulse{animation:pulse 2.4s ease-in-out infinite}"
           "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}")

    body = [card_bg(W, H, t, r=22),
            f'<g clip-path="url(#panel)"><rect width="{W}" height="{H}" fill="url(#dots)"/>'
            f'<rect width="{W}" height="{H}" fill="url(#glow)"/></g>']

    # ---- top bar
    sw = fonts.measure("mono", STATUS, 13)
    body.append(f'<text x="56" y="46" class="m" font-size="14" fill="{t["ink3"]}" letter-spacing="0.5">chiragshah2357 / README.md</text>')
    body.append(f'<circle cx="{W - 56 - sw - 16:.1f}" cy="42" r="4.5" fill="{t["ok"]}" class="pulse"/>')
    body.append(f'<text x="{W - 56}" y="46.5" text-anchor="end" class="m" font-size="13" fill="{t["ink2"]}" letter-spacing="1">{esc(STATUS)}</text>')
    body.append(f'<line x1="56" x2="{W - 56}" y1="66" y2="66" stroke="{t["rule"]}"/>')

    # ---- name, revealed once by a scanning bar
    size = 86
    defs.append(f'<clipPath id="reveal"><rect x="0" y="78" width="0" height="116">'
                f'{anim("width", [0, W], dur="1.4s", repeat=None, fill="freeze", extra=EASE)}</rect></clipPath>')
    body.append(f'<g clip-path="url(#reveal)"><text x="54" y="150" font-size="{size}" fill="{t["ink"]}" class="s" letter-spacing="-1.6">'
                f'Chirag <tspan class="si" fill="{t["accent"]}">Shah</tspan></text></g>')
    body.append(f'<rect x="-50" y="80" width="50" height="104" fill="url(#scan)" opacity="0.5">'
                f'{anim("x", [-50, W - 50], dur="1.4s", repeat=None, fill="freeze", extra=EASE)}'
                f'{anim("opacity", [0.5, 0.5, 0], dur="1.4s", repeat=None, fill="freeze")}</rect>')

    # ---- role, then the tagline with its one-line gloss
    body.append(f'<text x="56" y="184" class="m" font-size="15" fill="{t["ink2"]}" letter-spacing="0.2">{esc(ROLE)}</text>')
    body.append(f'<text x="56" y="211" class="mb" font-size="15" fill="{t["accent"]}">{esc(TAG)}</text>')
    body.append(f'<text x="{56 + fonts.measure("monob", TAG, 15) + 11:.1f}" y="211" class="m" font-size="15" fill="{t["ink3"]}">{esc(SUB)}</text>')

    texts = {"serif": "Chirag ", "serifi": "Shah",
             "mono": ROLE + SUB + STATUS + "chiragshah2357 / README.md",
             "monob": TAG}
    return svg(W, H, "".join(body), theme, texts, title="Chirag Shah",
               desc="Chirag Shah — ML / AI engineer, CS undergrad at MUJ, ex-intern at Protiviti. Teaching machines to read.",
               css=css, defs="".join(defs))
