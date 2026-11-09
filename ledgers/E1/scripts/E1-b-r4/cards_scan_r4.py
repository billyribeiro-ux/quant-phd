"""Round-4 card scan: dup ids, dup normalised fronts across all E1 cards, slice-lesson counts, and label citations per slice card."""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
cards = json.loads((ROOT / "course/modules/E/E1/cards.json").read_text(encoding="utf-8"))
print("total cards", len(cards))
ids = Counter(c["id"] for c in cards)
print("dup ids", [i for i, n in ids.items() if n > 1])
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()
fronts = defaultdict(list)
for c in cards:
    fronts[norm(c["front"])].append(c["id"])
print("dup normalised fronts", [v for v in fronts.values() if len(v) > 1])
slice_cards = [c for c in cards if c["lesson"] in ("L04", "L05", "L06")]
print("slice cards", len(slice_cards), Counter(c["lesson"] for c in slice_cards))
print("slice ids", " ".join(c["id"] for c in slice_cards))
pages = {L: (ROOT / f"course/modules/E/E1/{L}.html").read_text(encoding="utf-8") for L in ("L04", "L05", "L06")}
plain = {L: re.sub(r"<[^>]+>", " ", t) for L, t in pages.items()}
for c in slice_cards:
    labels = sorted(set(re.findall(r"(Definition|Proposition|Theorem|Lemma|Corollary|Remark|Example|Assumption|Problem|Lab|Section|Misconception)\s+(\d+(?:\.\d+)?)", c["back"] + " " + c["front"])))
    missing = []
    for kind, num in labels:
        if kind in ("Section", "Lab", "Misconception"):
            continue
        if not re.search(r"%s\s+%s\b" % (kind, re.escape(num)), plain[c["lesson"]]):
            missing.append(f"{kind} {num}")
    grade = c.get("grade", "-")
    print(c["id"], c["lesson"], "grade=" + str(grade), "cites=" + ";".join(f"{k} {n}" for k, n in labels), "MISSING_IN_LESSON=" + ",".join(missing) if missing else "")
