"""Mechanical checks of course/modules/BK/BK4/cards.json against the lesson text (stdlib only).

Usage: python3 -I ledgers/BK4/scripts/BK4-d-r1/cards_check.py <repo-root>
Reads cards.json and the lesson text produced by extract_text.py (re-rendered here), and prints:
  1. structure: ids, duplicates, grades, bases, cites, lesson names
  2. every number token in a card (front or back) and whether it occurs in the named lesson's text
  3. every cross-reference token (Definition/Proposition/Remark/Example/Problem/Corollary/Assumption/Lab part)
     in a card and whether it occurs in the named lesson's text (or in the lesson it names, when stated)
  4. near-duplicate fronts (token Jaccard >= 0.5) and exact duplicate backs
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("extract_text", root / "ledgers/BK4/scripts/BK4-d-r3/extract_text.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

from html.parser import HTMLParser  # noqa: E402


def text_of(path):
    r = mod.Render()
    r.feed(Path(path).read_text(encoding="utf-8"))
    return " ".join("".join(r.out).split())


cards = json.loads((root / "course/modules/BK/BK4/cards.json").read_text(encoding="utf-8"))
lessons = {p: text_of(root / f"course/modules/BK/BK4/{p}.html") for p in ("L01", "L02", "L03", "L04", "L05")}
ids = [c["id"] for c in cards]
print(f"cards: {len(cards)}; distinct ids: {len(set(ids))}")
print("id sequence:", ids[0], "..", ids[-1], "; contiguous:", ids == [f"BK4-c{i:03d}" for i in range(1, len(ids) + 1)])
print("per lesson:", {l: sum(1 for c in cards if c["lesson"] == l) for l in lessons})
print("grades:", {g: sum(1 for c in cards if c.get("grade") == g) for g in ("T", "C", "A", "B", "D", "X")},
      "no grade:", sum(1 for c in cards if "grade" not in c))
for c in cards:
    if c.get("grade") and not (c.get("basis") or c.get("cite")):
        print("GRADE WITHOUT BASIS", c["id"])
    if c.get("grade") == "T" and not str(c.get("basis", "")).strip():
        print("T WITHOUT BASIS", c["id"])
    if c.get("grade") == "C" and not str(c.get("basis", "")).strip():
        print("C WITHOUT BASIS", c["id"])
    if "grade" not in c and c.get("basis"):
        print("BASIS WITHOUT GRADE", c["id"])
    if c.get("grade") and c["grade"] != "T" and c.get("cite") is None:
        print("NON-T WITHOUT CITE FIELD", c["id"])

print("\n== numbers not found verbatim in the named lesson text ==")
num_re = re.compile(r"(?<![A-Za-z_\w])(\d[\d,]*(?:\.\d+)?(?:/\d+)?)")
missing_num = []
for c in cards:
    lt = lessons[c["lesson"]]
    for field in ("front", "back", "basis"):
        for tok in num_re.findall(str(c.get(field, ""))):
            t = tok.rstrip(",")
            if t in ("1", "0", "2", "3", "4", "5", "6", "7", "8"):
                pass
            if t not in lt:
                missing_num.append((c["id"], field, t))
for row in missing_num:
    print(*row)
print("count:", len(missing_num))

print("\n== cross-reference tokens not found in the named lesson text ==")
xref_re = re.compile(r"\b(Definition|Proposition|Remark|Example|Problem|Corollary|Assumption|Lab \d)\s+(?:[A-Z]?\d+(?:\.\d+)?|\d)(?:\(\w\))?")
bad = []
for c in cards:
    lt = lessons[c["lesson"]]
    for field in ("front", "back", "basis"):
        for m in xref_re.finditer(str(c.get(field, ""))):
            tok = m.group(0)
            if tok in lt:
                continue
            # allow a token whose local form is in the lesson (e.g. 'Assumption 1.3' inside text)
            other = [l for l, t in lessons.items() if tok in t]
            bad.append((c["id"], c["lesson"], field, tok, other))
for row in bad:
    print(*row)
print("count:", len(bad))

print("\n== duplicates ==")
def toks(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))
pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        ta, tb = toks(a["front"]), toks(b["front"])
        j = len(ta & tb) / max(1, len(ta | tb))
        if j >= 0.5:
            pairs.append((round(j, 2), a["id"], b["id"], a["front"][:70], b["front"][:70]))
for p in sorted(pairs, reverse=True):
    print(*p, sep=" | ")
print("front pairs with Jaccard >= 0.5:", len(pairs))
backs = {}
for c in cards:
    backs.setdefault(c["back"], []).append(c["id"])
print("exact duplicate backs:", [v for v in backs.values() if len(v) > 1])
fronts = {}
for c in cards:
    fronts.setdefault(c["front"], []).append(c["id"])
print("exact duplicate fronts:", [v for v in fronts.values() if len(v) > 1])
