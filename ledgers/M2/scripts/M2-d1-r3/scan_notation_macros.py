"""Scan L19-L21 pages and their cards for notation, macro, banned-phrase and duplicate-card evidence.

Usage: python -I scan_notation_macros.py <repo-root>. Reads notation/notation.json for the registered macros
and symbols, lists every LaTeX control word used in the three lesson pages and cards.json, counts \\mathbb,
checks each math segment for registered single-symbol collisions, greps the banned phrases of BUILDER_RULES
1.3-1.4, and reports duplicate card ids and duplicate normalised fronts over the whole M2 card file.
"""
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
notation = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
registered_macros = set(notation["macros"])
print("registered macros:", sorted(registered_macros))
pages = {n: (root / f"course/modules/M/M2/L{n}.html").read_text(encoding="utf-8") for n in (19, 20, 21)}
cards_text = (root / "course/modules/M/M2/cards.json").read_text(encoding="utf-8")
sources = {f"L{n}.html": s for n, s in pages.items()}
sources["cards.json"] = cards_text
for name, text in sources.items():
    words = Counter(re.findall(r"\\[A-Za-z]+", text))
    unregistered = sorted(w for w in words if w in {"\\mathbb"})
    print(f"{name}: control words={len(words)} \\mathbb count={text.count('mathbb')} "
          f"registered-macros-used={sorted(w for w in words if w in registered_macros)} "
          f"forbidden={unregistered}")
collisions = Counter()
for name, s in pages.items():
    segments = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", s, re.S)
    for a, b in segments:
        m = a or b
        for label, pat in (("T", r"(?<![A-Za-z\\])T(?![A-Za-z])"), ("Phi", r"\\Phi"), ("gamma_3/4", r"\\gamma_[34]"),
                           ("R^ast", r"R\^\{?\\ast"), ("R_f", r"R_f"), ("Q", r"\\mathbb\{Q\}|\bQ\b"),
                           ("E", r"\\E\b"), ("Prob", r"\\Prob")):
            if re.search(pat, m):
                collisions[(name, label)] += 1
print("registered-symbol collisions in math segments:", dict(collisions) or "none")
banned = re.compile(
    r"TODO|TBD|lorem|for brevity|beyond the scope|details omitted|left as an exercise|you can add more|"
    r"it is important to note|studies show|experts agree|it is well known|obviously|clearly", re.I)
for name, text in sources.items():
    hits = banned.findall(text)
    print(f"banned phrases in {name}: {len(hits)}")
cards = json.loads(cards_text)
ids = [c["id"] for c in cards]
print("cards:", len(cards), "duplicate ids:", [k for k, v in Counter(ids).items() if v > 1] or "none")
norm = Counter(re.sub(r"[^a-z0-9]", "", c["front"].lower()) for c in cards)
dups = [c["id"] for c in cards if norm[re.sub(r"[^a-z0-9]", "", c["front"].lower())] > 1]
print("cards with a duplicate normalised front:", dups or "none")
for c in cards:
    if c["lesson"] in ("L19", "L20", "L21"):
        for field in ("front", "back"):
            if re.search(r"\\[A-Za-z]|\$", c[field]):
                print("LaTeX-like text on card", c["id"], field)
