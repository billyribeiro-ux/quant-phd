"""Round-2: every href and concept anchor in L03/L04 resolves; concept definitions and their module."""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
mod = root / "course/modules/AC/AC2"
for page in ("L03", "L04"):
    html = (mod / f"{page}.html").read_text(encoding="utf-8")
    for href in sorted(set(re.findall(r'href="([^"]+)"', html))):
        if href.startswith("http") or href.startswith("#"):
            if href.startswith("#"):
                ok = re.search(rf'id="{re.escape(href[1:])}"', html) is not None
                print(page, "in-page", href, ok)
            continue
        target, _, frag = href.partition("#")
        path = (mod / target).resolve() if not target.startswith("../") else (mod / target).resolve()
        exists = path.exists()
        frag_ok = None
        if frag and exists:
            frag_ok = re.search(rf'id="{re.escape(frag)}"', path.read_text(encoding="utf-8")) is not None
        print(page, href, "file", exists, "anchor", frag_ok)
concepts = json.loads((root / "curriculum/curriculum.json").read_text(encoding="utf-8"))
def walk(o, out):
    if isinstance(o, dict):
        if "concepts" in o and isinstance(o["concepts"], (dict, list)):
            pass
        for k, v in o.items():
            out.append((k, v))
            walk(v, out)
    elif isinstance(o, list):
        for v in o:
            walk(v, out)
ids = ["balance-sheet", "income-statement", "statement-articulation", "xbrl-standardization", "financial-ratio-analysis",
       "dupont-decomposition", "return-on-invested-capital", "accrual-accounting", "cash-flow-statement",
       "depreciation-and-amortization", "outlier-detection", "robust-statistics", "missing-data-mechanisms",
       "gaap-vs-ifrs", "accruals", "earnings-quality"]
text = json.dumps(concepts)
for c in ids:
    print("concept", c, "in curriculum.json:", f'"{c}"' in text)
for c in ("return-on-invested-capital", "accruals", "earnings-quality"):
    print("defined in", c, [p for p in ("L03", "L04") if f'id="def-{c}"' in (mod / f"{p}.html").read_text(encoding="utf-8")])
