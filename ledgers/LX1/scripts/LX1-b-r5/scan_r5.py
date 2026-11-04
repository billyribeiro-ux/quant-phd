"""Verifier round 5 text scans for LX1 slice b (L03, L04): notation, banned phrases, process words,
outside-closure concept names, and every link target. Usage: python3 -I scan_r5.py <checkout>"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
pages = ["course/modules/LX/LX1/L03.html", "course/modules/LX/LX1/L04.html", "course/modules/LX/LX1/cards.json"]
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
macros = set(reg["macros"])
seg = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.S)
registered_bad = re.compile(r"(?<![A-Za-z])T(?![A-Za-z])|\\Phi|\\gamma|\\ast|R_f|R\^\{?e|\\mathbb\{Q\}")
for p in pages[:2]:
    t = (root / p).read_text(encoding="utf-8")
    segs = [m.group(1) or m.group(2) for m in seg.finditer(t)]
    used = sorted({m for s in segs for m in re.findall(r"\\[A-Za-z]+", s)})
    reg_macro_used = sorted(u for u in used if "\\" + u.lstrip("\\") in macros or u in macros)
    print(p, "math segments:", len(segs), "registered-symbol hits:", [s for s in segs if registered_bad.search(s)])
    print("  macros used:", used)
    print("  registered macros used:", reg_macro_used)
    # single-letter symbols used in math
    letters = sorted({ch for s in segs for ch in re.findall(r"(?<![\\A-Za-z])[A-Za-z](?![A-Za-z])", s)})
    print("  single-letter symbols in math:", "".join(letters))
    # banned phrases
    banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
              "you can add more", "it is important to note", "studies show", "experts agree", "well known",
              "obviously", "clearly", "it can be shown"]
    hits = [b for b in banned if b.lower() in re.sub(r"<[^>]+>", " ", t).lower()]
    print("  banned phrase hits:", hits)
    ell = re.findall(r"\.\.\.", re.sub(r"<pre.*?</pre>", "", t, flags=re.S))
    print("  ellipsis outside code:", len(ell))
    proc = ["plans/", "tools/", "open item", "D-1", "B1", "B2", "B3", "N1", "N2", "N3", "N4", "builder", "fixer",
            "verifier", "ledger", "architect", "round ", "REQUEST"]
    plain = re.sub(r"<[^>]+>", " ", t)
    print("  process-word hits:", [w for w in proc if w in plain])
    # outside-closure concept names (plan §4 D1-D15) in visible text, and links
    names = ["bank run", "bank-run", "fire sale", "leverage cycle", "banking crisis", "currency crisis",
             "covered interest parity", "uncovered interest parity", "efficient markets", "moral hazard",
             "Fisher", "bank reserves", "central bank balance", "balance sheet", "credit default swap",
             "network contagion", "term spread", "expectation", "fx market", "sovereign default"]
    print("  outside-closure names:", {n: plain.lower().count(n.lower()) for n in names if n.lower() in plain.lower()})
    dfns = re.findall(r'<dfn id="([^"]+)"', t)
    print("  dfn ids:", dfns, "unique:", len(dfns) == len(set(dfns)))
    dc = re.findall(r'data-concept="([^"]+)"', t)
    print("  data-concept values:", sorted(set(dc)))
    hrefs = re.findall(r'href="([^"]+)"', t)
    print("  hrefs:", hrefs)
    for h in hrefs:
        if h.startswith("http"):
            print("  EXTERNAL HREF", h)
        elif "#" in h and not h.startswith("#") and not h.startswith("../"):
            f, frag = h.split("#", 1)
            target = (root / "course/modules/LX/LX1" / f).resolve()
            ok = target.exists() and f'id="{frag}"' in target.read_text(encoding="utf-8")
            print("   link", h, "target ok:", ok)
        elif h.startswith("#"):
            print("   in-page", h, "present:", f'id="{h[1:]}"' in t)
