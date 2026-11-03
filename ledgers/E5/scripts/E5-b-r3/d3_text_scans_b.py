"""Round 3 verifier: text scans of the L04-L06 pages (banned phrases, process words, scope words, notation, figures,
citations, why-it-matters word counts, hours, concept uses of curriculum concepts before their introduction).
Run: .venv/bin/python -I ledgers/E5/scripts/E5-b-r3/d3_text_scans_b.py
"""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
E5 = ROOT / "course" / "modules" / "E" / "E5"
PAGES = ["L04", "L05", "L06"]
texts = {p: (E5 / f"{p}.html").read_text(encoding="utf-8") for p in PAGES}

BANNED = [
    "TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
    "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
    "obviously", "clearly", "it can be shown", "…", "...",
]
print("== banned phrases (case-insensitive)")
for p in PAGES:
    hits = [b for b in BANNED if b.lower() in texts[p].lower()]
    print(p, "hits:", hits)

PROCESS = ["round", "verif", "builder", "agent", "audit", "reviewer", "revised", "ledger", "verifier", "orchestrator"]
print("== process words (lines containing them, page prose and code)")
for p in PAGES:
    for i, line in enumerate(texts[p].splitlines(), 1):
        for w in PROCESS:
            if re.search(r"\b" + w, line, re.I):
                print(p, i, w)

SCOPE = ["only", "every", "all ", "always", "any ", "same", "exactly", "drives"]
print("== scope-word count per page (each occurrence is read in the round-3 reading)")
for p in PAGES:
    prose = re.sub(r"<[^>]+>", " ", texts[p])
    c = Counter()
    for w in SCOPE:
        c[w.strip()] = len(re.findall(r"\b" + re.escape(w.strip()) + r"\b", prose, re.I))
    print(p, dict(c))

print("== why-it-matters word counts (limit 120)")
for p in PAGES:
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', texts[p], re.S)
    t = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    print(p, len(t.split()))

print("== data-cite count per page")
for p in PAGES:
    print(p, texts[p].count("data-cite"), re.findall(r'data-cite="([^"]+)"', texts[p]))

print("== svg / chart figures per page")
for p in PAGES:
    print(p, "svg:", texts[p].count("<svg"), "chart:", texts[p].count('class="chart"'))

print("== hours")
print("index", re.findall(r'data-hours-lessons="(\d+)"|data-hours-project="(\d+)"', (E5 / "index.html").read_text(encoding="utf-8")))
for n in range(1, 9):
    s = (E5 / f"L0{n}.html").read_text(encoding="utf-8")
    print(f"L0{n}", re.search(r'data-hours="(\d+)"', s).group(1))
cur = json.loads((ROOT / "curriculum" / "curriculum.json").read_text(encoding="utf-8"))
units: list[dict] = []


def walk(x):
    if isinstance(x, dict):
        if x.get("id") == "E5" and "introduces" in x:
            units.append(x)
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)


walk(cur)
print("curriculum E5 hours", units[0]["hours"], "introduces", sorted(units[0]["introduces"].keys()))

print("== concepts introduced in later E5 lessons and named before them in L04-L06")
checks = {
    "fiscal-multiplier": ["fiscal multiplier", "fiscal"],
    "policy-rate": ["policy rate"],
    "taylor-rule": ["taylor rule", "Taylor"],
    "price-index-inflation": ["inflation rate", "Measured inflation", "measured inflation"],
}
for cid, names in checks.items():
    for p in PAGES:
        found = [n for n in names if n in texts[p]]
        if found:
            print(cid, p, found)
