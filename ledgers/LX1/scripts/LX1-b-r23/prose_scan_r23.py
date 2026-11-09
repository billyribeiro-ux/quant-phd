"""Banned-phrase, process-word and scope-word scan of the three LX1 pages and the L01/L03/L04 cards (tags stripped).
Prints every hit with its line number. Run as: python -I script <root>."""
import html
import json
import re
import sys

ROOT = sys.argv[1]
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "it can be shown", "roughly", "historically", "about 6%", "...", "…"]
PROCESS = ["round", "verifier", "builder", "fixer", "ledger", "ruling", "architect", "verified", "audit", "fragment",
           "pin", "delta", "KNOWN-ISSUES", "reviewer", "checkout", "sweep", "LOW", "FAIL", "PASS"]
SCOPE = ["only", "all", "always", "every", "any", "same", "drives", "exactly"]
hits = {"banned": [], "process": [], "scope": []}
for L in ("L01", "L03", "L04"):
    lines = open(f"{ROOT}/course/modules/LX/LX1/{L}.html", encoding="utf-8").read().split("\n")
    for n, raw in enumerate(lines, 1):
        t = html.unescape(re.sub(r"<[^>]+>", " ", raw))
        low = t.lower()
        for p in BANNED:
            if p.lower() in low:
                hits["banned"].append(f"{L}:{n} {p!r}")
        for p in PROCESS:
            if re.search(r"\b" + re.escape(p.lower()) + r"\b", low):
                hits["process"].append(f"{L}:{n} {p!r} | {t.strip()[:90]}")
        for p in SCOPE:
            for m in re.finditer(r"\b" + p + r"\b", low):
                hits["scope"].append(f"{L}:{n} {p}")
cards = json.load(open(f"{ROOT}/course/modules/LX/LX1/cards.json", encoding="utf-8"))
for c in cards:
    if c["lesson"] not in ("L01", "L03", "L04"):
        continue
    text = c["front"] + " " + c["back"]
    for p in BANNED:
        if p.lower() in text.lower():
            hits["banned"].append(f"{c['id']} {p!r}")
    for p in PROCESS:
        if re.search(r"\b" + re.escape(p.lower()) + r"\b", text.lower()):
            hits["process"].append(f"{c['id']} {p!r}")
    for p in SCOPE:
        for m in re.finditer(r"\b" + p + r"\b", text.lower()):
            hits["scope"].append(f"{c['id']} {p}")
for k, v in hits.items():
    print(f"== {k}: {len(v)} hits")
    for x in v:
        print("  ", x)
