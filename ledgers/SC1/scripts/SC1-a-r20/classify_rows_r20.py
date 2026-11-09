"""SC1-a round 20: classify each round-19 row. A row is 'touched' when its cited location names a changed file or changed
line since cd4dd7df (changed lines: L02.html:285, L03.html:51, cards.json ids c030 c031 c210 c221 c224 c243), names a
whole file without line numbers, or cites ledgers/tests/commands. Other rows may be carried.
Usage (checkout root): python3 -I ledgers/SC1/scripts/SC1-a-r20/classify_rows_r20.py"""
import json
import re

prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-SC1-a.round19.json", encoding="utf-8"))
CHANGED = {"course/modules/SC/SC1/L02.html": {285}, "course/modules/SC/SC1/L03.html": {51}}
FILES = ("index.html", "L01.html", "L02.html", "L03.html")
RANGE = re.compile(r":(\d+)(?:-(\d+))?")
touched, carried = [], []
for r in prev["rows"]:
    loc = r.get("location") or ""
    text = loc + " " + (r.get("evidence") or "")
    reasons = []
    if re.search(r"cards\.json|ledgers/|tests/|tools|cmd|gate|command|see command|page_smoke|run_labs|twin|lab-mutants|mutants|verify_refs", loc):
        reasons.append("tooling/cards/labs subject")
    cur = None
    for piece in re.split(r";|,(?=\s*:)|\s\(", loc):
        m = re.search(r"(index|L01|L02|L03)\.html", piece)
        if m:
            cur = "course/modules/SC/SC1/" + m.group(1) + ".html"
            if not re.search(r"\.html:\d", piece):
                reasons.append(f"whole-file reference {m.group(1)}.html")
        rng = RANGE.search(piece)
        if rng and cur in CHANGED:
            a, b = int(rng.group(1)), int(rng.group(2) or rng.group(1))
            if any(a <= x <= b for x in CHANGED[cur]):
                reasons.append(f"cites changed line in {cur.split('/')[-1]}")
    (touched if reasons else carried).append((r["id"], "; ".join(sorted(set(reasons)))))
print("touched", len(touched))
for i, why in touched:
    print("  T", i, "|", why)
print("carried", len(carried))
for i, _ in carried:
    print("  C", i)
