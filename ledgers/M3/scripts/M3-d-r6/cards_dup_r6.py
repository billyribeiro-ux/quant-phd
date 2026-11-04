"""Round-6 verifier: card structure, duplicate fronts/backs, and near-duplicate pairs by token overlap."""
import json, re, sys
from pathlib import Path
cards = json.loads(Path("course/modules/M/M3/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)))
keys = {k for c in cards for k in c}
print("keys", sorted(keys))
print("fronts unique", len({c["front"] for c in cards}), "backs unique", len({c["back"] for c in cards}))
def toks(s):
    return set(re.findall(r"[a-z]+", s.lower())) - {"the","a","of","and","is","to","in","for","if","on","that","by","with","as","it","its","an","be","are","or","this","whether","which","what","how","does","do","so","any","each","every","then","all"}
pairs = []
for i in range(len(cards)):
    for j in range(i+1, len(cards)):
        a, b = cards[i], cards[j]
        ta = toks(a["front"]+" "+a["back"]); tb = toks(b["front"]+" "+b["back"])
        if not ta or not tb: continue
        jac = len(ta & tb) / len(ta | tb)
        if jac >= 0.45:
            pairs.append((round(jac,2), a["id"], b["id"], a["front"][:70], b["front"][:70]))
for p in sorted(pairs, reverse=True):
    print(p)
print("pairs >=0.45:", len(pairs))
