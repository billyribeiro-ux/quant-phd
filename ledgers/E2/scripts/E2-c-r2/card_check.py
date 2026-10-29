"""Every number on a slice card back must occur in its lesson text (run with python -I from the checkout)."""
import json
import re

cards = json.load(open("course/modules/E/E2/cards.json", encoding="utf-8"))
txt = {f: open(f"/tmp/e2-v2/c/{f}.txt", encoding="utf-8").read() for f in ["L07", "L08", "L09"]}
bad = []
for c in cards:
    if c["lesson"] not in txt:
        continue
    for n in set(re.findall(r"\d+(?:\.\d+)?", c["back"])):
        if n not in txt[c["lesson"]] and n not in ("1", "0"):
            bad.append((c["id"], n))
print("card numbers not found:", bad)
