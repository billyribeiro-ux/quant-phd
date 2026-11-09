"""Verifier r13: flag card pairs whose front or back share a long common substring (same-fact screen)."""
import difflib
import json
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
def norm(s):
    return " ".join(s.lower().replace("(", " ").replace(")", " ").split())
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        for field in ("front", "back"):
            sm = difflib.SequenceMatcher(None, norm(a[field]), norm(b[field]), autojunk=False)
            m = sm.find_longest_match(0, len(norm(a[field])), 0, len(norm(b[field])))
            if m.size >= 45:
                pairs.append((m.size, a["id"], b["id"], field, norm(a[field])[m.a:m.a + m.size]))
for p in sorted(pairs, reverse=True):
    print(p[0], p[1], p[2], p[3], "|", p[4][:140])
print("pairs flagged:", len(pairs))
