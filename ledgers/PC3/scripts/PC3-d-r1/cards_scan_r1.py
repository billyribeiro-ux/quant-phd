"""Whole-file scans of course/modules/PC/PC3/cards.json at the pin (PC3 slice d, round 1)."""
import json, re, subprocess, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(sys.argv[1])
cards = json.loads((ROOT / "course/modules/PC/PC3/cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards))
ids = [c["id"] for c in cards]
print("unique ids:", len(set(ids)) == len(ids), "strictly increasing:", ids == sorted(ids))
keysets = Counter(tuple(sorted(c)) for c in cards)
for k, n in keysets.items():
    print("keyset", n, k)
print("grades:", Counter(c.get("grade", "none") for c in cards))
print("graded cards lacking basis:", [c["id"] for c in cards if "grade" in c and not c.get("basis")])
print("cite non-empty:", [c["id"] for c in cards if c["cite"]])
print("lesson values:", Counter(c["lesson"] for c in cards))
lessons = {}
for n in range(1, 7):
    p = ROOT / f"course/modules/PC/PC3/L0{n}.html"
    lessons[f"L0{n}"] = p.read_text(encoding="utf-8")
print("all cards name an existing lesson:", all(c["lesson"] in lessons for c in cards))
print("every lesson has cards:", all(any(c["lesson"] == l for c in cards) for l in lessons))
fronts = Counter(c["front"] for c in cards)
backs = Counter(c["back"] for c in cards)
print("duplicate fronts:", [f for f, n in fronts.items() if n > 1])
print("duplicate backs:", [b[:60] for b, n in backs.items() if n > 1])
PROC = re.compile(r"\b(round|ruling|verifier|fixer|builder|architect|delta|pin|closing|audit|blocker|FAIL|PASS|sweep|mutant)\b", re.I)
print("process words:", [(c["id"], m.group(0)) for c in cards for f in ("front", "back", "basis") for m in [PROC.search(c.get(f, ""))] if m])
# numeric tokens on each card must appear in its own lesson (stripped of tags)
def strip(s):
    import html
    return html.unescape(re.sub(r"<[^>]+>", " ", s))
miss = []
for c in cards:
    text = strip(lessons[c["lesson"]])
    text_nospace = re.sub(r"\s+", "", text)
    for f in ("front", "back"):
        for tok in re.findall(r"\d+(?:\.\d+)?", c[f]):
            if len(tok) < 2:
                continue
            if tok not in text and tok not in text_nospace:
                miss.append((c["id"], f, tok))
print("card numeric tokens (>=2 chars) not found verbatim in own lesson:", miss)
