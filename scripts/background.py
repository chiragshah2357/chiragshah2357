"""The Background panel: two course tracks with a concrete line under each, the work notes, and the stack chips.

This used to be two panels (Background, Stack). They were doing one job — "what I have learned and what I
reach for" — so they are one panel now, which is also ~300px less scroll. The 'ml algorithms' chip row was
dropped because the ML track above already names those algorithms.
"""
import fonts
from common import THEMES, card_bg, esc, svg

W = 1000
ML_TRACK = ["Linear / logistic", "KNN", "Random forest", "AdaBoost / XGBoost", "NLP"]
RAG_TRACK = ["Parsing", "Chunking", "Vector stores", "Hybrid search", "HyDE", "Agentic RAG", "Corrective RAG"]
ML_NOTE = "27 sections · regression to ensembles to unsupervised to NLP · one project packaged and deployed"
RAG_NOTE = "Parsing to agentic retrieval, with the notes kept as a reference I still use"
WORK = ["Worked with agent harnesses, like DeepSeek Harness.",
        "Contributed to open-source hackathons with an award-winning Japanese college undergrad."]
STACK = [
    ("languages", ["Python", "C / C++", "SQL", "Java (beginner)"]),
    ("ml + data", ["scikit-learn", "NumPy", "pandas", "SciPy"]),
    ("llm + rag", ["LangChain", "LangGraph", "Qdrant", "Pinecone", "MCP", "DeepSeek Harness"]),
    ("web + infra", ["FastAPI", "Flask", "React", "Vite", "Docker", "Git"]),
]


def label_lines(text, width=15):
    """Wrap a node label onto lines of at most `width` characters, never splitting around a ' / '."""
    out, cur = [], ""
    for w in text.split(" "):
        if cur and len(cur) + 1 + len(w) > width:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return out + [cur]


def background(theme):
    t = THEMES[theme]
    body = [None,   # placeholder for the panel, whose height is known only at the end
            f'<text x="56" y="52" class="m" font-size="14" fill="{t["ink3"]}" letter-spacing="0.4">'
            f'// courses · stack · hackathons</text>']
    mono_text = ["// courses · stack · hackathons", "still going", ML_NOTE, RAG_NOTE] + WORK
    serif_text, bold_text = [], []
    css = (".nd{animation:pop .5s ease backwards;transform-box:fill-box;transform-origin:center}"
           "@keyframes pop{from{opacity:0;transform:scale(.3)}}"
           ".chip{animation:rise .5s ease backwards;transform-box:fill-box}"
           "@keyframes rise{from{opacity:0;transform:translateY(8px)}}")

    def track(y, title, status, nodes, step, note, dashed_to=None):
        serif_text.append(title)
        bold_text.append(status)
        body.append(f'<text x="56" y="{y}" class="s" font-size="25" fill="{t["ink"]}">{esc(title)}</text>')
        tw = fonts.measure("serif", title, 25)
        pw = fonts.measure("monob", status, 12) + 24
        px = 56 + tw + 18
        body.append(f'<rect x="{px:.1f}" y="{y - 19}" width="{pw:.1f}" height="26" rx="13" fill="{t["accent"]}" '
                    f'fill-opacity="0.14" stroke="{t["accent"]}" stroke-opacity="0.7"/>'
                    f'<text x="{px + pw / 2:.1f}" y="{y - 1.5}" text-anchor="middle" class="mb" font-size="12" '
                    f'fill="{t["accent"]}" letter-spacing="0.8">{esc(status)}</text>')
        ly = y + 44
        x_first, x_last = 124, 124 + step * (len(nodes) - 1)
        body.append(f'<line x1="{x_first}" x2="{x_last}" y1="{ly}" y2="{ly}" stroke="{t["accent"]}" stroke-width="2.5" '
                    f'stroke-dasharray="{x_last}" stroke-dashoffset="0">'
                    f'<animate attributeName="stroke-dashoffset" from="{x_last}" to="0" dur="1.2s" fill="freeze"/></line>')
        if dashed_to:
            body.append(f'<line x1="{x_last}" x2="{dashed_to}" y1="{ly}" y2="{ly}" stroke="{t["ink3"]}" stroke-width="2" stroke-dasharray="3 7"/>')
            body.append(f'<text x="{dashed_to + 12}" y="{ly + 5}" class="m" font-size="13" fill="{t["ink3"]}">still going</text>')
        for i, label in enumerate(nodes):
            cx = x_first + step * i
            last = i == len(nodes) - 1
            body.append(f'<g class="nd" style="animation-delay:{0.15 * i:.2f}s"><circle cx="{cx}" cy="{ly}" r="{9 if last else 7}" '
                        f'fill="{t["accent"] if last else t["panel"]}" stroke="{t["accent"]}" stroke-width="2.5"/></g>')
            for k, line in enumerate(label_lines(label)):
                body.append(f'<text x="{cx}" y="{ly + 30 + k * 16}" text-anchor="middle" class="m" font-size="13" '
                            f'fill="{t["ink"] if last else t["ink2"]}">{esc(line)}</text>')
                mono_text.append(line)
        body.append(f'<text x="56" y="{ly + 68}" class="m" font-size="13" fill="{t["ink3"]}">{esc(note)}</text>')

    track(104, "Krish Naik · AI / ML course", "IN PROGRESS · UP TO NLP", ML_TRACK, 140, ML_NOTE, dashed_to=124 + 140 * 4 + 150)
    track(260, "Krish Naik · RAG course", "UP TO CORRECTIVE RAG", RAG_TRACK, 124, RAG_NOTE)

    # ---- work notes
    y = 404
    body.append(f'<line x1="56" x2="{W - 56}" y1="{y - 24}" y2="{y - 24}" stroke="{t["rule"]}"/>')
    for i, line in enumerate(WORK):
        ly = y + 6 + i * 32
        body.append(f'<rect x="56" y="{ly - 11}" width="9" height="9" rx="2" fill="{t["accent"]}"/>'
                    f'<text x="80" y="{ly}" class="m" font-size="15" fill="{t["ink"]}">{esc(line)}</text>')
    y += 6 + len(WORK) * 32

    # ---- stack chips
    body.append(f'<line x1="56" x2="{W - 56}" y1="{y}" y2="{y}" stroke="{t["rule"]}"/>')
    y += 26
    cols = [t["flood"], t["warn"], t["ok"], t["violet"]]
    x0, x1 = 224, W - 56
    chip_text, n = "", 0
    for r, (label, items) in enumerate(STACK):
        lines, cur, x = [], [], x0          # flow the chips onto as many lines as the row needs
        for it in items:
            w = fonts.measure("monob", it, 15) + 28
            if cur and x + w > x1:
                lines.append(cur)
                cur, x = [], x0
            cur.append((it, w))
            x += w + 9
        lines.append(cur)
        c = cols[r % len(cols)]
        body.append(f'<text x="56" y="{y + 21}" class="m" font-size="13" fill="{t["ink3"]}" letter-spacing="1">{label.upper()}</text>')
        for li, line in enumerate(lines):
            x = x0
            for it, w in line:
                body.append(f'<g class="chip" style="animation-delay:{0.06 * n:.2f}s">'
                            f'<rect x="{x:.1f}" y="{y + li * 40}" width="{w:.1f}" height="31" rx="15.5" fill="{c}" '
                            f'fill-opacity="0.12" stroke="{c}" stroke-opacity="0.65"/>'
                            f'<text x="{x + w / 2:.1f}" y="{y + li * 40 + 21}" text-anchor="middle" class="mb" '
                            f'font-size="15" fill="{t["ink"]}">{esc(it)}</text></g>')
                x += w + 9
                n += 1
                chip_text += it
        y += (len(lines) - 1) * 40 + 31
        if r < len(STACK) - 1:
            body.append(f'<line x1="56" x2="{W - 56}" y1="{y + 13}" y2="{y + 13}" stroke="{t["rule"]}" stroke-dasharray="2 5"/>')
            y += 28
    H = y + 40
    body[0] = card_bg(W, H, t, r=22)

    texts = {"serif": "".join(serif_text),
             "mono": "".join(mono_text) + "".join(l.upper() for l, _ in STACK),
             "monob": "".join(bold_text) + chip_text}
    return svg(W, H, "".join(body), theme, texts, title="Background and stack", css=css,
               desc="Krish Naik's AI/ML course, studied up to NLP and still in progress — 27 sections, regression through "
                    "ensembles and unsupervised learning to NLP, with one project packaged and deployed. His RAG course, up to "
                    "corrective RAG. Worked with agent harnesses like DeepSeek Harness. Contributed to open-source hackathons "
                    "with an award-winning Japanese college undergrad. Stack: "
                    + "; ".join(f'{l}: {", ".join(i)}' for l, i in STACK))
