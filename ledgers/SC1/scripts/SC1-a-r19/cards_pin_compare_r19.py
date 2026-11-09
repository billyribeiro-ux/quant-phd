"""SC1-a round 19: cards.json at the pins (56cc575a, 700bf33f, 50559266, HEAD = cd4dd7df) read with git show (no temp files
are kept beyond the run); counts per pin; JSON equality of every L01-L03 record between 50559266 and HEAD; the list of
changed, added and removed ids across the whole file. Usage (from the checkout root): python3 -I <this file>."""

import collections
import json
import os
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))


def cards_at(rev):
    raw = subprocess.run(["git", "-C", ROOT, "show", f"{rev}:course/modules/SC/SC1/cards.json"], capture_output=True,
                         text=True, check=True).stdout
    return json.loads(raw)


out = []
pins = {}
for rev in ("56cc575a", "700bf33f", "50559266", "HEAD"):
    cards = cards_at(rev)
    pins[rev] = {c["id"]: c for c in cards}
    l = collections.Counter(c["lesson"] for c in cards if c["lesson"] in ("L01", "L02", "L03"))
    out.append(f"{rev}: total {len(cards)}, distinct ids {len(pins[rev])}, L01-L03 {sum(l.values())} "
               f"(L01 {l['L01']}, L02 {l['L02']}, L03 {l['L03']})")
a, b = pins["50559266"], pins["HEAD"]
out.append("removed since 50559266: " + str([(i, a[i]["lesson"]) for i in sorted(set(a) - set(b))]))
out.append("added since 50559266: " + str([(i, b[i]["lesson"]) for i in sorted(set(b) - set(a))]))
changed = [(i, a[i]["lesson"]) for i in sorted(a) if i in b and a[i] != b[i]]
out.append("changed records since 50559266: " + str(changed))
l13 = [i for i in a if a[i]["lesson"] in ("L01", "L02", "L03")]
out.append(f"L01-L03 records at 50559266: {len(l13)}; JSON-identical at HEAD: "
           f"{sum(1 for i in l13 if i in b and a[i] == b[i])}")
named = ["SC1-c011", "SC1-c012", "SC1-c013", "SC1-c029", "SC1-c032", "SC1-c034", "SC1-c035", "SC1-c054", "SC1-c060",
         "SC1-c207", "SC1-c210", "SC1-c220", "SC1-c232", "SC1-c233", "SC1-c234", "SC1-c017"]
out.append("r14 and c017 records JSON-identical 50559266 vs HEAD: " + str({i: a[i] == b[i] for i in named}))
text = "\n".join(out)
print(text)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "cards_pin_compare_r19.out"), "w",
          encoding="utf-8") as f:
    f.write(text + "\n")
