"""For each E2 card in L07-L09, list numbers on the card back that do not occur in the lesson text (verifier slice E2-c)."""
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1])  # checkout root
cards = json.loads((root / "course/modules/E/E2/cards.json").read_text(encoding="utf-8"))
texts = {}
for lesson in ("L07", "L08", "L09"):
    raw = (root / f"course/modules/E/E2/{lesson}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<(?=[\s0-9=(])", "&lt;", raw)
    texts[lesson] = re.sub(r"<[^>]+>", " ", raw)
missing = []
for c in cards:
    if c["lesson"] not in texts:
        continue
    for num in set(re.findall(r"\d[\d,.]*\d|\d", c["back"])):
        core = num.rstrip(".,")
        if core not in texts[c["lesson"]] and core not in c["front"]:
            missing.append((c["id"], c["lesson"], core))
for m in sorted(missing):
    print(*m)
print("numbers checked; missing:", len(missing))
