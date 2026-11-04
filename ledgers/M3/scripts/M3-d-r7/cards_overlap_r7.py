"""Round-7 verifier (slice d): token-overlap scan of all M3 cards (front + back), Jaccard on word sets, plus exact
duplicate fronts/backs. Prints every pair at or above 0.40 for reading. Usage: .venv/bin/python -I <this file>."""

import json
import re
from pathlib import Path

cards = json.loads((Path.cwd() / "course/modules/M/M3/cards.json").read_text(encoding="utf-8"))
STOP = {"the", "a", "an", "of", "is", "to", "and", "in", "for", "that", "with", "it", "by", "as", "on", "or", "be", "this",
        "not", "are", "true", "false", "from", "does", "do", "what", "which", "when", "if", "its", "each", "at", "than"}


def words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP}


pairs = []
for i, a in enumerate(cards):
    wa = words(a["front"] + " " + a["back"])
    for b in cards[i + 1 :]:
        wb = words(b["front"] + " " + b["back"])
        j = len(wa & wb) / len(wa | wb)
        if j >= 0.40:
            pairs.append((j, a["id"], b["id"]))
pairs.sort(reverse=True)
for j, x, y in pairs:
    ca = next(c for c in cards if c["id"] == x)
    cb = next(c for c in cards if c["id"] == y)
    print(f"{j:.2f} {x} {y} | {ca['front']} || {cb['front']}")
print("pairs >= 0.40:", len(pairs))
