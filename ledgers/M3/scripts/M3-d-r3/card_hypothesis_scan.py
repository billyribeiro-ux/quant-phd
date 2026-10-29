"""Round-3 card scan (verifier): for every card, the labelled blocks it cites and whether each statement now opens with
an 'Assuming ...' hypothesis, and whether the card text carries that hypothesis (F1..F4, 'Assum', 'Under F1')."""

import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/M/M3"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
pages = {p.stem: html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", p.read_text(encoding="utf-8")))) for p in root.glob("L0*.html")}
ref_re = re.compile(r"\b(Definition|Proposition|Theorem|Lemma|Corollary|Remark|Example)\s+(\d+\.\d+)")
statements: dict[str, str] = {}
for name, text in pages.items():
    for m in re.finditer(r"(Definition|Proposition|Theorem|Lemma|Corollary|Remark|Example) (\d+\.\d+)", text):
        key = f"{m.group(1)} {m.group(2)}"
        if key not in statements or (name in key or True):
            tail = text[m.end(): m.end() + 140]
            statements.setdefault(key, f"{name}: {tail}")
for c in cards:
    blob = c["front"] + " " + c["back"]
    refs = [f"{m.group(1)} {m.group(2)}" for m in ref_re.finditer(blob)]
    for r in dict.fromkeys(refs):
        st = statements.get(r, "MISSING")
        assumed = bool(re.search(r"\bAssuming\b|Assumption|under F1|Under F1|assuming F1", st))
        carried = bool(re.search(r"F1|F2|F3|F4|[Aa]ssum|[Uu]nder F", blob))
        if assumed and not carried:
            print(f"{c['id']} {c['lesson']} cites {r} whose statement is hypothesis-laden [{st[:110]}...] but card has no hypothesis")
