"""Duplicate scan over all M2 cards: exact front/back repeats, and token-Jaccard pairs on front+back."""
import json, re, sys
from pathlib import Path
cards = json.loads(Path(sys.argv[1], "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
norm = lambda s: re.sub(r"\s+", " ", s.strip().lower())
fronts = {}
for c in cards:
    fronts.setdefault(norm(c["front"]), []).append(c["id"])
print("exact duplicate fronts:", [v for v in fronts.values() if len(v) > 1])
backs = {}
for c in cards:
    backs.setdefault(norm(c["back"]), []).append(c["id"])
print("exact duplicate backs:", [v for v in backs.values() if len(v) > 1])
tok = {c["id"]: set(re.findall(r"[a-z]+|\d+(?:\.\d+)?", (c["front"] + " " + c["back"]).lower())) for c in cards}
pairs = []
ids = [c["id"] for c in cards]
for i, a in enumerate(ids):
    for b in ids[i + 1:]:
        u = tok[a] | tok[b]
        j = len(tok[a] & tok[b]) / len(u) if u else 0
        if j >= 0.45:
            pairs.append((round(j, 3), a, b))
pairs.sort(reverse=True)
print("pairs with Jaccard >= 0.45:", len(pairs))
for j, a, b in pairs:
    ca = next(c for c in cards if c["id"] == a); cb = next(c for c in cards if c["id"] == b)
    print(j, a, ca["lesson"], "|", ca["front"][:90], "||", b, cb["lesson"], "|", cb["front"][:90])
