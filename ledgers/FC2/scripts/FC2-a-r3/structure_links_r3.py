"""Round 3 FC2-a: links, anchors, cite keys, data use, banned phrases, structure counts, hours, concept anchors."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = ROOT / "course/modules/FC/FC2"
SLICE = ["index.html", "L01.html", "L02.html", "L03.html"]
regs = json.loads((ROOT / "references/references.json").read_text(encoding="utf-8"))
ents = regs.get("entries", regs) if isinstance(regs, dict) else regs
keys = set(ents.keys()) if isinstance(ents, dict) else {e.get("key") for e in ents}
print("registry keys", len(keys))
fails = 0
BANNED = re.compile(
    r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|"
    r"important to note|studies show|experts agree|well known|obviously|clearly|verifier|builder|planner|"
    r"ledger|fragment|architect|DAG_DEFECT|placeholder|honest-pending|\.\.\.|…",
    re.I,
)
for f in SLICE:
    t = (PAGES / f).read_text(encoding="utf-8")
    ids = set(re.findall(r'\sid="([^"]+)"', t))
    for href in re.findall(r'href="([^"]+)"', t):
        if href.startswith("#"):
            if href[1:] not in ids:
                print("MISSING in-page", f, href)
                fails += 1
        elif href.startswith("http"):
            print("EXTERNAL", f, href)
            fails += 1
        else:
            path, _, frag = href.partition("#")
            target = (PAGES / path).resolve() if path else (PAGES / f)
            if not target.exists():
                print("MISSING file", f, href)
                fails += 1
                continue
            if frag and not re.search(r'\sid="' + re.escape(frag) + '"', target.read_text(encoding="utf-8")):
                print("MISSING fragment", f, href)
                fails += 1
    for k in re.findall(r'data-cite="([^"]+)"', t):
        if k not in keys:
            print("CITE KEY NOT IN REGISTRY", f, k)
            fails += 1
    if re.search(r"data-files|data/", t):
        print("DATA REFERENCE", f)
        fails += 1
    for m in BANNED.finditer(re.sub(r"<[^>]+>", " ", t)):
        print("BANNED/PROCESS WORD", f, repr(m.group(0)))
        fails += 1
    print(f, "ids", len(ids))
concepts = (ROOT / "course/concepts.html").read_text(encoding="utf-8")
for f in SLICE:
    t = (PAGES / f).read_text(encoding="utf-8")
    for c in sorted(set(re.findall(r'concepts\.html#([^"]+)"', t))):
        ok = f'id="{c}"' in concepts
        print("concept anchor", f, c, "OK" if ok else "MISSING")
        fails += 0 if ok else 1
for f in ["L01.html", "L02.html", "L03.html"]:
    t = (PAGES / f).read_text(encoding="utf-8")
    why = re.search(r'<p class="why-it-matters">(.*?)</p>', t, re.S)
    words = len(re.sub(r"<[^>]+>", " ", why.group(1)).split())
    quiz = re.search(r'<section class="quiz".*?</section>', t, re.S).group(0)
    items = len(re.findall(r'<li class="item"', quiz))
    mis = len(re.findall(r'<li class="misconception"', t))
    tiers = {}
    for tier in ["mechanics", "proof", "empirical", "research"]:
        block = re.search(r'data-tier="' + tier + r'">(.*?)</div>\s*</div>', t, re.S).group(1)
        tiers[tier] = len(re.findall(r'class="problem"', block))
    hours = re.search(r'data-hours="(\d+)"', t).group(1)
    print(f, "why_words", words, "quiz_items", items, "misconceptions", mis, "problems", tiers, "data-hours", hours)
hub = (PAGES / "index.html").read_text(encoding="utf-8")
print("hub data-hours-lessons", re.search(r'data-hours-lessons="(\d+)"', hub).group(1), "project", re.search(r'data-hours-project="(\d+)"', hub).group(1))
print("SUMMARY failures", fails)
