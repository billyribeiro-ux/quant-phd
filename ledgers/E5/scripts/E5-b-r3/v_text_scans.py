"""Structural and text scans for E5 slice b (L04-L06): banned phrases, process words, figures, headings,
navigation titles, concept links and anchors, hub hours, card duplicates and card coverage counts."""
import collections
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
E5 = ROOT / "course/modules/E/E5"
LESSONS = ("L04", "L05", "L06")
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly"]
PROCESS = re.compile(r"\b(build|builder|round|verifier|REQUESTS?|unit report|planner|architect|fixer)\b", re.I)


def visible(path):
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw)))


bad_banned = []
process_hits = []
for L in LESSONS:
    p = E5 / f"{L}.html"
    t = visible(p)
    for b in BANNED:
        if b.lower() in t.lower():
            bad_banned.append((L, b))
    for m in PROCESS.finditer(t):
        process_hits.append((L, m.group(0)))
    tw = (ROOT / f"tests/labs/E5/lab-E5-{L}-1.py").read_text(encoding="utf-8")
    for b in BANNED:
        if re.search(r"\b" + re.escape(b) + r"\b", tw):
            bad_banned.append((L, "twin:" + b))
print("banned-phrase hits (pages and twins):", bad_banned)
print("process-word hits in learner text:", process_hits)
print("ellipsis outside code in pages:", [L for L in LESSONS if "..." in visible(E5 / f'{L}.html')])
print("svg/img/chart elements:", {L: len(re.findall(r"<svg|<img|class=\"chart\"", (E5 / f"{L}.html").read_text(encoding="utf-8"))) for L in LESSONS})

h1 = {L: re.findall(r"<h1>([^<]*)</h1>", (E5 / f"{L}.html").read_text(encoding="utf-8"))[0] for L in ("L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08")}
hub = (E5 / "index.html").read_text(encoding="utf-8")
for L in LESSONS:
    print(L, "h1:", h1[L], "| hub card title matches:", f'<span class="card-title">{h1[L]}</span>' in hub)
for L, nxt, prv in (("L04", "L05", "L03"), ("L05", "L06", "L04"), ("L06", "L07", "L05")):
    t = (E5 / f"{L}.html").read_text(encoding="utf-8")
    print(L, "nav next title matches h1 of", nxt, ":", f"{nxt} · {h1[nxt]}" in t)
    print(L, "nav prev title matches h1 of", prv, ":", f"{prv} · {h1[prv]}" in t)
for L in LESSONS:
    print(L, "study-hours eyebrow:", re.findall(r"(\d+) study hours", (E5 / f"{L}.html").read_text(encoding="utf-8")))
hours_lessons = re.findall(r'data-hours-lessons="(\d+)"', hub)
hours_project = re.findall(r'data-hours-project="(\d+)"', hub)
print("hub hours-lessons", hours_lessons, "hours-project", hours_project, "sum", int(hours_lessons[0]) + int(hours_project[0]))

cards = json.loads((E5 / "cards.json").read_text(encoding="utf-8"))
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
backs = collections.Counter(c["back"].strip().lower() for c in cards)
ids = collections.Counter(c["id"] for c in cards)
print("cards total", len(cards), "unique ids", len(ids), "duplicate fronts", [k for k, v in fronts.items() if v > 1],
      "duplicate backs", [k for k, v in backs.items() if v > 1])
print("T-graded cards without basis:", [c["id"] for c in cards if c.get("grade") == "T" and not c.get("basis")])
print("L04-L06 card counts:", {L: sum(1 for c in cards if c["lesson"] == L) for L in LESSONS})
print("L04-L06 card ids:", [c["id"] for c in cards if c["lesson"] in LESSONS])

defs = {L: re.findall(r'id="(def-[^"]+)" data-concept="([^"]+)"', (E5 / f"{L}.html").read_text(encoding="utf-8")) for L in LESSONS}
print("concept definitions (dfn with data-concept) in L04-L06:", defs)
links = {L: re.findall(r'<a (?:class="concept" )?data-concept="([^"]+)" href="([^"]+)"', (E5 / f"{L}.html").read_text(encoding="utf-8")) for L in LESSONS}
for L in LESSONS:
    print(L, "concept links (concept, href):", links[L])
