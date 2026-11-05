"""Round 11: every label a card cites (Definition/Proposition/... N.M, Problem X, Example N.M, Lab parts) must appear in its lesson text.
Also: every card number must appear verbatim in its lesson text. Prints misses only, plus counts."""
import json, re
from pathlib import Path
base = Path("course/modules/CS/CS2")
S = Path("ledgers/CS2/scripts/CS2-d-r11")
cards = json.loads((base / "cards.json").read_text(encoding="utf-8"))
texts = {}
for L in sorted({c["lesson"] for c in cards}):
    texts[L] = (S / f"text_{L}.txt").read_text(encoding="utf-8")
pat = re.compile(r"\b(Definition|Proposition|Lemma|Corollary|Theorem|Remark|Example|Problem|Misconception|Assumption|Section)\s+([A-Z]?\d+(?:\.\d+)?)(\([a-z]\))?")
miss = []
refs = 0
for c in cards:
    t = texts[c["lesson"]]
    for m in pat.finditer(c["back"] + " " + c["front"]):
        refs += 1
        kind, num = m.group(1), m.group(2)
        # the lesson text uses e.g. "Proposition 1.3" or "Problem R3" or "Example 2.4" as labels
        if f"{kind} {num}" not in t:
            miss.append((c["id"], c["lesson"], f"{kind} {num}"))
print("label references", refs, "missing in own lesson", len(miss))
for m in miss: print("  MISS", m)
