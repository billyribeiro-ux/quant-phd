# BK4 slice d, round 1 (verifier F31): process-word, scope-word, registered-symbol and near-duplicate scans over all cards.
import difflib
import json
import re

ROOT = "/Users/billyribeiro/.fanout/wt/verifyF31-BK4-d"
cur = json.load(open(ROOT + "/course/modules/BK/BK4/cards.json", encoding="utf-8"))
changed = {"BK4-c012", "BK4-c013", "BK4-c032", "BK4-c088", "BK4-c089", "BK4-c107"}
proc = re.compile(r"\b(round|verifier|ruling|rulings|fixed|revised|previous|earlier|draft|TODO|placeholder|pending|we|our|I|me|my|agent|builder|fixer|slice|delta|card|cards)\b", re.I)
print("--- process words (all cards)")
for c in cur:
    for field in ["front", "back", "basis"]:
        for m in proc.finditer(c.get(field, "")):
            print(c["id"], field, repr(m.group(0)), "| ctx:", c[field][max(0, m.start() - 40): m.end() + 40])
scope = re.compile(r"\b(only|every|all|exactly|same|depends only|always|never|any)\b", re.I)
print("--- scope words in changed/added cards")
for c in cur:
    if c["id"] in changed:
        for field in ["front", "back", "basis"]:
            for m in scope.finditer(c.get(field, "")):
                print(c["id"], field, repr(m.group(0)), "| ctx:", c[field][max(0, m.start() - 50): m.end() + 40])
reg = re.compile(r"\\Phi|\\gamma_[34]|\\ast|R_f|\\mathbb\{Q\}|\bT\b|\bQ\b")
print("--- registered-symbol tokens (all cards)")
for c in cur:
    for field in ["front", "back", "basis"]:
        for m in reg.finditer(c.get(field, "")):
            print(c["id"], field, repr(m.group(0)))
print("--- near-duplicate fronts (SequenceMatcher >= 0.55) involving changed cards")
pairs = 0
for i in range(len(cur)):
    for j in range(i + 1, len(cur)):
        a, b = cur[i], cur[j]
        pairs += 1
        if a["id"] in changed or b["id"] in changed:
            r = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
            rb = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
            if r >= 0.55 or rb >= 0.55:
                print(a["id"], b["id"], "front", round(r, 3), "back", round(rb, 3))
print("pairs scanned:", pairs)
ids = [c["id"] for c in cur]
print("id gaps:", [f"c{n:03d}" for n in range(1, 108) if f"BK4-c{n:03d}" not in ids])
