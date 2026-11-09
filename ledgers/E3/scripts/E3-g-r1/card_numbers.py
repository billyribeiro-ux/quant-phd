"""Round-15 verifier: every number token on a slice card (L05-L08) must appear in its lesson text, and ids are unique."""
import json
import re
import subprocess
import sys

root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/E/E3/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)) == len(ids))
dup_fronts = {}
for c in cards:
    dup_fronts.setdefault(c["front"].strip().lower(), []).append(c["id"])
print("duplicate fronts", [v for v in dup_fronts.values() if len(v) > 1])
texts = {}
for L in ("L05", "L06", "L07", "L08"):
    out = subprocess.run([sys.executable, "-I", f"{root}/ledgers/E3/scripts/E3-g-r18/strip.py", f"{root}/course/modules/E/E3/{L}.html"], capture_output=True, text=True).stdout
    texts[L] = out
num_re = re.compile(r"\d+(?:\.\d+)?(?:/\d+)?")
for c in cards:
    if c["lesson"] not in texts:
        continue
    body = c["front"] + " " + c["back"]
    missing = []
    for tok in sorted(set(num_re.findall(body))):
        if tok in ("1", "0", "2", "3"):
            continue
        if tok not in texts[c["lesson"]]:
            missing.append(tok)
    if missing:
        print(c["id"], c["lesson"], "numbers not in lesson text:", missing)
print("done")
