"""Refined carry check: resolve bare SC1 file names to course/modules/SC/SC1/, ignore round-17 evidence artifacts
(ledgers/SC1/scripts/SC1-d-r17/...), and flag a row when a cited subject file changed in 700bf33f..50559266.
Usage: python3 -I carry_check2_r18.py <frag.json> <delta.txt>"""
import json
import re
import sys

frag = json.load(open(sys.argv[1]))
changed = set(line.strip() for line in open(sys.argv[2]) if line.strip())
bare = {"project.html", "L01.html", "L02.html", "L03.html", "L04.html", "L05.html", "L06.html", "L07.html",
        "L08.html", "index.html", "cards.json"}
pat = re.compile(r"((?:course|tests|plans|ledgers|references|tools|curriculum|notation|atlas)/[A-Za-z0-9_./\-]+)")
for r in frag["rows"]:
    text = " ".join([r.get("location", ""), r.get("evidence", "")])
    files = set(m.group(1).rstrip(".,;:)") for m in pat.finditer(text))
    for b in re.findall(r"\b(" + "|".join(re.escape(x) for x in bare) + r")\b", text):
        files.add("course/modules/SC/SC1/" + b)
    files = {f for f in files if not f.startswith("ledgers/SC1/scripts/SC1-d-r17/")}
    hit = sorted(f for f in files if f in changed)
    print(f"{r['status']:4} {r['id']:48} subjects={len(files)} changed={hit}")
