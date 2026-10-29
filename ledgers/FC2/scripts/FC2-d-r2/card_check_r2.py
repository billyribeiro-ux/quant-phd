"""FC2-d round 2: card checks against the current lesson text.

Usage: .venv/bin/python -I ledgers/FC2/scripts/FC2-d-r2/card_check_r2.py <checkout> <scratch>
Writes <scratch>/L01.txt..L08.txt (tag-stripped lesson text), then prints:
  - every number token on a card that does not occur in its own lesson text,
  - cards with no grade field, cards graded T with a SIMULATED basis (architect rule e),
  - duplicate card ids, duplicate fronts.
"""

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
base = root / "course/modules/FC/FC2"
lessons = {}
for n in range(1, 9):
    raw = (base / f"L{n:02d}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    text = re.sub(r"\s+", " ", text)
    lessons[f"L{n:02d}"] = text
    (scratch / f"L{n:02d}.txt").write_text(text, encoding="utf-8")
cards = json.loads((base / "cards.json").read_text(encoding="utf-8"))
missing = []
for c in cards:
    text = c["front"] + " " + c["back"]
    for tok in sorted(set(re.findall(r"\d+(?:\.\d+)?", text))):
        if tok not in lessons[c["lesson"]]:
            missing.append((c["id"], tok))
print("number tokens not found in own lesson text:", missing)
print("cards:", len(cards), "ids unique:", len({c["id"] for c in cards}) == len(cards))
print("no grade field:", [c["id"] for c in cards if "grade" not in c])
print(
    "grade T with SIMULATED basis:",
    [(c["id"], c["basis"]) for c in cards if c.get("grade") == "T" and "SIMULATED" in c.get("basis", "")],
)
print("grade C cards:", [c["id"] for c in cards if c.get("grade") == "C"])
fronts = Counter(c["front"] for c in cards)
print("duplicate fronts:", [f for f, k in fronts.items() if k > 1])
print("per-lesson counts:", Counter(c["lesson"] for c in cards))
