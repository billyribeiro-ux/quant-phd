"""Attach the fix field to every non-PASS row of the round-7 fragment. Run from the checkout root."""
import json, pathlib
p = pathlib.Path("ledgers/AC4/AC4-e.json")
d = json.loads(p.read_text(encoding="utf-8"))
FIX = {
    "proj-spec-clarity-and-errors": "Add a boolean case (True) to test_product_field_not_a_whole_number_raises_value_error for the five product fields and to the flexible_budget actual-units argument test; or narrow line 263 to the fields the tests cover. Re-run m35 and m36 (must be KILLED).",
    "proj-spec-coverage-claims": "Make line 265 match the tests: after the boolean fix above, 'each named ValueError' is enforced; otherwise name the uncovered boolean cases.",
    "proj-stretch-two-inputs": "Change the bullet to 'show that the sales price, sales volume, sales mix and the two efficiency variances add to the total when each actual input price equals its standard, and state the input price variances that close the gap otherwise'.",
    "proj-mutants-r7-new": "Add boolean cases for product fields and the actual-units argument so that m35 and m36 are KILLED by mutate_graders.py --unit AC4 --seeds 0-9.",
    "proj-stretch-spending": "Replace 'add to the total exactly when it is not' with 'add to the total exactly, whether or not the actual input price is the standard'.",
    "proj-autograder-rerun-mutants-m01-m37": "Fix proj-mutants-r7-new (m35, m36); re-run mutate_graders.py --unit AC4 --seeds 0-9 to 37/37 KILLED.",
}
for r in d["rows"]:
    if r["status"] != "PASS":
        r["fix"] = FIX[r["id"]]
p.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("fixes attached:", sum(1 for r in d["rows"] if r.get("fix")))
