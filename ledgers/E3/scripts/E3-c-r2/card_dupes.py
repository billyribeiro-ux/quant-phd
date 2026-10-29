"""Full duplicate scan over the E3 cards (fronts and backs): exact duplicates and near-duplicate fronts (ratio >= 0.8)."""
import difflib, json, pathlib
cards = json.loads(pathlib.Path("/tmp/verifyC2-E3-c/course/modules/E/E3/cards.json").read_text(encoding="utf-8"))
norm = lambda s: " ".join(s.lower().split())
seen = {}
for c in cards:
    k = norm(c["front"])
    if k in seen:
        print("EXACT front duplicate:", seen[k], c["id"])
    seen.setdefault(k, c["id"])
pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        r = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
        if r >= 0.8:
            pairs.append((round(r, 2), a["id"], b["id"], a["front"][:60], b["front"][:60]))
for p in pairs:
    print("near-duplicate front", p)
print("cards", len(cards), "near pairs", len(pairs))
