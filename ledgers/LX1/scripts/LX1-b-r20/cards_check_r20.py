"""Round 20 card check for LX1 lessons L01, L03, L04 (slice b).

Checks: unique ids over the whole cards.json; lesson in L01..L04; grade present for each card; basis non-empty; every cite
key exists in references/references.json; every decimal or integer token in front and back appears in the lesson page text
(math spans included, tags stripped); reports cards whose text differs from the cd4dd7df pin (git show).
Run from the checkout root: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r20/cards_check_r20.py
"""
import html
import json
import re
import subprocess
from collections import Counter

cards = json.load(open("course/modules/LX/LX1/cards.json", encoding="utf-8"))
refs = json.load(open("references/references.json", encoding="utf-8"))
keys = set()
for r in (refs if isinstance(refs, list) else refs.get("entries", refs.values())):
    if isinstance(r, dict) and "key" in r:
        keys.add(r["key"])
print("cards", len(cards), "unique ids", len({c["id"] for c in cards}) == len(cards), "registry keys", len(keys))
print("per lesson", dict(Counter(c["lesson"] for c in cards)))
pages = {}
for L in ("L01", "L03", "L04"):
    t = open(f"course/modules/LX/LX1/{L}.html", encoding="utf-8").read()
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    pages[L] = html.unescape(re.sub(r"<[^>]+>", " ", t))
old = json.loads(subprocess.run(["git", "show", "cd4dd7df:course/modules/LX/LX1/cards.json"], capture_output=True, text=True, check=True).stdout)
oldmap = {c["id"]: c for c in old}
changed = [c["id"] for c in cards if oldmap.get(c["id"]) != c]
print("cards differing from cd4dd7df:", changed, "| new ids:", [c["id"] for c in cards if c["id"] not in oldmap])
problems = []
for c in cards:
    if c["lesson"] not in ("L01", "L02", "L03", "L04"):
        problems.append((c["id"], "lesson"))
    if not c.get("grade") or not c.get("basis"):
        problems.append((c["id"], "grade/basis"))
    for k in c.get("cite", []):
        if k not in keys:
            problems.append((c["id"], f"cite {k} not in registry"))
    if c["lesson"] in pages:
        text = c["front"] + " " + c["back"]
        for tok in set(re.findall(r"\d[\d,]*(?:\.\d+)?", text)):
            tok2 = tok.rstrip(",")
            if tok2 not in pages[c["lesson"]].replace(",", "") and tok2.replace(",", "") not in pages[c["lesson"]].replace(",", ""):
                problems.append((c["id"], f"number {tok2} not found in {c['lesson']}.html text"))
print("problems:", problems)
