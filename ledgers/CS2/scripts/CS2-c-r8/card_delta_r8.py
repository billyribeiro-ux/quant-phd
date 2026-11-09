"""CS2-c-r8: cards.json delta aa659725 -> 4540351d by id, absent-id checks, L09-L11 numbers and process words."""

from __future__ import annotations

import html
import json
import re
import sys

ROOT = sys.argv[1]
S = ROOT + "/ledgers/CS2/scripts/CS2-c-r8/"
old = {c["id"]: c for c in json.load(open(S + "cards_aa659725.json", encoding="utf-8"))}
new_list = json.load(open(ROOT + "/course/modules/CS/CS2/cards.json", encoding="utf-8"))
new = {c["id"]: c for c in new_list}
print("cards aa659725:", len(old), " cards HEAD:", len(new_list), " unique HEAD:", len(new))
print("added:", sorted(set(new) - set(old)))
print("removed:", sorted(set(old) - set(new)))
print("changed:", sorted(i for i in set(old) & set(new) if old[i] != new[i]))
for absent in ["CS2-c207", "CS2-c225", "CS2-c195", "CS2-c199"]:
    print("absent", absent, absent not in new)
l_cards = [c for c in new_list if c["lesson"] in ("L09", "L10", "L11")]
print("L09-L11 cards:", len(l_cards), "grades:", {g: sum(1 for c in l_cards if c["grade"] == g) for g in "TC"})
print("C cards without basis:", [c["id"] for c in l_cards if c["grade"] == "C" and not c.get("basis")])
print("T cards with basis:", [c["id"] for c in l_cards if c["grade"] == "T" and c.get("basis")])
lesson_text = {}
for L in ("L09", "L10", "L11"):
    raw = open(ROOT + f"/course/modules/CS/CS2/{L}.html", encoding="utf-8").read()
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    lesson_text[L] = re.sub(r"\s+", " ", txt)
num = re.compile(r"\d+(?:\.\d+)?(?:e-?\d+)?")
missing = []
for c in l_cards:
    toks = set(num.findall(c["front"] + " " + c["back"]))
    for t in sorted(toks):
        if t not in lesson_text[c["lesson"]] and t not in ("1", "0", "2", "3"):
            missing.append((c["id"], t))
print("numeric tokens (excluding 0-3) on L09-L11 cards not found in own lesson text:", missing)
pw = re.compile(r"\b(we|we'll|let's|our|I|you|note|recall|round|verifier|builder|orchestrat\w*|TODO|TBD|placeholder)\b", re.I)
hits = [(c["id"], m.group(0)) for c in l_cards for m in pw.finditer(c["front"] + " " + c["back"])]
print("process/unfinished words on L09-L11 cards:", hits)
