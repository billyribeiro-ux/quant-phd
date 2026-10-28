"""Selects which round-35 rows must be re-verified this round (their subject touches the 5aeaaf0..81ff53b delta)."""
import json, re, sys

prev = json.load(open(sys.argv[1], encoding="utf-8"))
CHANGED_FILES = ["project.html", "cards.json", "L03.html", "L04.html", "lab-AC4-L04-1", "ledgers/AC4/mutants", "mutants"]
HOT_IDS = {"proj-card-c078", "proj-r30-card-c023-hypothesis", "proj-r30-rubric-observability"}
HOT_KW = re.compile(r"c023|c078|rubric|C2 level|C4 level|exemplar-a|Exemplar A|mutant|L04|L03|collect|563|pytest|test_memo|"
                    r"page_smoke|run_labs|run_graders|ruff|mypy|verify_refs|check_pages|check_dag|check_projects|"
                    r"banned|changed-lines|c058|c061|c063", re.I)
PROJ_HUNKS = [(312, 318), (340, 352)]


def touches_hunk(text):
    for m in re.finditer(r"(?:project\.html|page)[^;()]*?(?:lines?|line)\s+(\d+)(?:\s*[-–]\s*(\d+))?", text):
        a = int(m.group(1)); b = int(m.group(2) or a)
        for lo, hi in PROJ_HUNKS:
            if a <= hi and b >= lo:
                return True
    return False


hot, carry = [], []
for r in prev["rows"]:
    text = r["location"] + " " + r["evidence"]
    if r["id"] in HOT_IDS or HOT_KW.search(r["id"] + " " + r["location"]) or touches_hunk(text):
        hot.append(r["id"])
    else:
        carry.append(r["id"])
print("HOT", len(hot)); print(" ".join(hot))
print("CARRY", len(carry))
json.dump({"hot": hot, "carry": carry}, open(sys.argv[2], "w"), indent=1)
