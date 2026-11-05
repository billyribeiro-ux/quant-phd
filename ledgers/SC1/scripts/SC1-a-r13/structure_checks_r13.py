"""Structure, hours, concept, notation, banned-phrase and card-scan checks for SC1 slice a (index, L01-L03, cards).

Run as: .venv/bin/python -I <this file> <checkout root>. Prints every figure the ledger rows cite.
"""
import collections
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
sc1 = root / "course/modules/SC/SC1"
pages = {p: (sc1 / f"{p}.html").read_text(encoding="utf-8") for p in ["index", "L01", "L02", "L03"]}

# hours
print("index data-hours-lessons/project:", re.findall(r'data-hours-(lessons|project)="(\d+)"', pages["index"]))
print("lesson data-hours L01..L08:", [re.search(r'data-hours="(\d+)"', (sc1 / f"L0{i}.html").read_text(encoding="utf-8")).group(1) for i in range(1, 9)])
proj = (sc1 / "project.html").read_text(encoding="utf-8")
hours = re.findall(r"<td class=\"num\">(\d+)</td>", proj)
print("project hour table cells:", hours)

# structure per lesson
for i in range(1, 4):
    h = (sc1 / f"L0{i}.html").read_text(encoding="utf-8")
    tiers = re.findall(r'<div class="tier" data-tier="(\w+)">(.*?)</div>\s*(?=<div class="tier"|</section>)', h, re.S)
    counts = {t: len(re.findall(r'class="problem"', body)) for t, body in tiers}
    quiz = len(re.findall(r'<li class="item"', h.split('id="quiz"')[1]))
    why = re.search(r'<p class="why-it-matters">(.*?)</p>', h, re.S).group(1)
    words = len(re.sub(r"<[^>]+>", "", why).split())
    print(f"L0{i}: problem tiers {counts}; misconceptions {h.count('class=\"misconception\"')}; quiz items {quiz}; why-it-matters tokens {words}")

# placement
q = pages["index"].split('id="placement"')[1].split("</section>")[0]
print("placement items:", len(re.findall(r'<li class="item"', q)), "skill items:", len(re.findall(r'data-skill', q)))

# concepts
dfn = collections.Counter()
for p in sorted(sc1.glob("*.html")):
    for m in re.findall(r'<dfn[^>]*data-concept="([^"]+)"', p.read_text(encoding="utf-8")):
        dfn[m] += 1
print("data-concept dfn across SC1 pages:", len(dfn), "ids; counts:", dict(dfn))

# notation: macros used in slice pages vs registry
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
macros = set(reg["macros"].keys())
used = collections.Counter()
for p, text in pages.items():
    for m in re.findall(r"\\[A-Za-z]+", text):
        used[m] += 1
custom = sorted(m for m in used if m in macros)
print("registered macros used in slice:", custom)
print("registered macros unused here:", sorted(macros - set(used))[:12], "...")
for sym in ["\\Phi", "\\gamma_3", "\\gamma_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}", "T_"]:
    hits = sum(t.count(sym) for t in pages.values())
    print(f"registered symbol {sym!r} occurrences in slice pages: {hits}")

# banned phrases (BUILDER_RULES 1.3-1.4)
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "well known",
          "obviously", "clearly", "it can be shown", "of course", "note that", "crucially", "importantly",
          "interestingly", "in conclusion", "let us", "we now"]
hits = {b: sum(t.lower().count(b) for t in pages.values()) for b in banned}
print("banned-phrase hits:", {b: n for b, n in hits.items() if n}, "(empty dict = none)")

# cards
cards = json.loads((sc1 / "cards.json").read_text(encoding="utf-8"))
print("cards total:", len(cards), "by lesson:", dict(collections.Counter(c["lesson"] for c in cards)))
print("duplicate ids:", [k for k, v in collections.Counter(c["id"] for c in cards).items() if v > 1])
print("duplicate fronts:", [k[:50] for k, v in collections.Counter(c["front"] for c in cards).items() if v > 1])
l123 = [c for c in cards if c["lesson"] in ("L01", "L02", "L03")]
print("L01-L03 cards:", len(l123), "ids:", l123[0]["id"], "...", l123[-1]["id"])
print("L01-L03 cards with grade:", sum(1 for c in l123 if "grade" in c), "cite nonempty:", sum(1 for c in l123 if c["cite"]))
