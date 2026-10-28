"""Build the round-23 M1-a fragment from the round-18 fragment (pin 7143726) plus fresh rows."""
import json
import sys

OLD = "/tmp/fanout-frags/M1-a.round22.json"
OUT = "/tmp/verify23-M1-a/ledgers/M1/fragments_out_r23.json"
d = json.load(open(OLD, encoding="utf-8"))
CARRY = ("Carried from round 22 (course/modules/M/M1/index.html, L01.html, L02.html, L03.html, tests/labs/M1/"
         "lab-M1-L01-1.py, lab-M1-L02-1.py, lab-M1-L03-1.py byte-identical to pin 7143726 since the previous pin; "
         "L01-L03 cards equal as JSON, 76 of 76, checked by ledgers/M1/scripts/M1-a-r23/cards_compare.py): ")
# rows re-verified fresh this round (command rows, and rows touching L04/L05 or the changed cards file)
FRESH = {
    "M1A-cmd-check_pages", "M1A-cmd-check_dag", "M1A-cmd-run_labs", "M1A-cmd-twin-isolated",
    "M1A-cmd-page_smoke", "M1A-cmd-ruff-mypy", "M1A-cmd-verify_refs", "M1A-cmd-pytest-labs",
    "M1A-lesson-structure-claim", "M1A-r7-hub-hours-sentence", "M1A-hours", "M1A-hours-total",
    "M1A17-hub-lessons-hours", "M1A-brief-prereq-note", "M1A-curriculum-concepts",
    "M1A17-cards-grades-basis", "M1A-cards-L01-L03",
}
rows = []
for r in d["rows"]:
    r = dict(r)
    if r["id"] in FRESH:
        r["evidence"] = "Re-verified in round 23: " + r["evidence"]
    else:
        assert r["status"] == "PASS", r["id"]
        r["evidence"] = CARRY + r["evidence"]
    rows.append(r)
print("carried/fresh-prefixed rows", len(rows), file=sys.stderr)
json.dump({"rows": rows}, open("/tmp/M1-v/M1-a/r23/old_rows.json", "w"), ensure_ascii=False, indent=1)
