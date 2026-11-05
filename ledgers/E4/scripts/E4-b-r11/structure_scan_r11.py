"""Round-11 structural scan of E4 L04-L06 (stdlib). Prints every measurement used in the fragment rows."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE11-E4-b")
PAGES = ["L04", "L05", "L06"]
notation = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
macro_names = set()


def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("macros",) and isinstance(v, (dict, list)):
                if isinstance(v, dict):
                    macro_names.update(v.keys())
                else:
                    for x in v:
                        if isinstance(x, dict) and "name" in x:
                            macro_names.add(x["name"])
                        elif isinstance(x, str):
                            macro_names.add(x)
            walk(v)
    elif isinstance(o, list):
        for x in o:
            walk(x)


walk(notation)
print("notation macro keys sample:", sorted(macro_names)[:60])
print("notation top-level keys:", list(notation.keys())[:20])

banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "..."]
process = ["builder", "verifier", "round", "REQUESTS", "unit report", "fixer", "planner"]

for page in PAGES:
    text = (ROOT / f"course/modules/E/E4/{page}.html").read_text(encoding="utf-8")
    print(f"\n=== {page} lines={text.count(chr(10))}")
    # why it matters
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', text, re.S)
    wim = re.sub(r"<[^>]+>", " ", m.group(1))
    print("why-it-matters words:", len(wim.split()))
    # solutions
    sols = re.findall(r'<details class="solution">(.*?)</details>', text, re.S)
    lens = [len(re.sub(r"<[^>]+>|\\\(|\\\)|\\\[|\\\]", " ", s).split()) for s in sols]
    print("solutions:", len(sols), "min words:", min(lens) if lens else None, "max:", max(lens) if lens else None)
    # quiz items
    print("quiz items:", len(re.findall(r'<li class="item"', text)))
    print("misconceptions:", len(re.findall(r'<li class="misconception"', text)))
    print("key-results rows:", len(re.findall(r"<tr><td>", text)))
    print("problems:", re.findall(r'<div class="problem" id="([^"]+)"', text))
    print("tiers:", re.findall(r'data-tier="([^"]+)"', text))
    print("labs:", re.findall(r'<section class="lab[^"]*" id="([^"]+)"', text))
    print("dfn ids:", re.findall(r'<dfn[^>]*?id="([^"]+)"', text))
    print("dfn (all):", len(re.findall(r"<dfn", text)))
    print("concept links:", sorted(set(re.findall(r'data-concept="([^"]+)" href="([^"]+)"', text)))[:40])
    print("data-cite:", re.findall(r'data-cite="([^"]+)"', text))
    print("data-grade counts:", {g: len(re.findall(rf'data-grade="{g}"', text)) for g in "TABCDX"})
    print("claim spans:", len(re.findall(r'class="block-title claim"', text)))
    low = text.lower()
    for b in banned:
        if b.lower() in low:
            # ellipsis check only outside code
            print("BANNED HIT:", b, [mm.start() for mm in re.finditer(re.escape(b.lower()), low)][:5])
    for p in process:
        if re.search(r"\b" + re.escape(p) + r"\b", re.sub(r"<[^>]+>", " ", text), re.I):
            print("PROCESS WORD candidate:", p)
    print("raw mathbb:", len(re.findall(r"\\mathbb", text)), "mathbf:", len(re.findall(r"\\mathbf", text)),
          "Phi:", len(re.findall(r"\\Phi", text)), "gamma:", len(re.findall(r"\\gamma", text)),
          "R-ast:", len(re.findall(r"R\^\\ast|R\^\{e", text)))
    macros_used = sorted(set(re.findall(r"\\([A-Za-z]+)", text)))
    print("latex commands used:", macros_used)
    print("heading order:", re.findall(r"<h([1-3])", text))
    print("lab count:", len(re.findall(r'class="lab"', text)), "sec ids:", re.findall(r'<section id="([^"]+)"', text))
    print("references data-ref items:", re.findall(r'data-references>(.*?)</ol>', text, re.S)[0][:80] if re.findall(r'data-references>(.*?)</ol>', text, re.S) else None)
