"""Round 24 AC4-a fragment builder: carries round-23 rows by the byte-identical rule, re-runs command rows, adds r24 rows."""
import json
from pathlib import Path

ROOT = Path("/tmp/verify24-AC4-a")
prev = json.loads(Path("/tmp/fanout-frags/AC4-a.round23.json").read_text(encoding="utf-8"))
L02_PREFIX = ("Carried from round 23 (course/modules/AC/AC4/L02.html cited lines byte-identical since the previous pin 503d139; "
              "the only changed line of L02.html is 311): ")
OTHER_PREFIX = ("Carried from round 23 (course/modules/AC/AC4/index.html, L01.html, cards.json byte-identical since the previous pin 503d139): ")
RERUN = {
    "AC4-a-cmd-check-pages": "Re-run round 24: tools/check_pages.py --unit AC4 rc=0, 'check_pages AC4: PASS' (ledgers/AC4/scripts/AC4-a-r24/out/check_pages.out).",
    "AC4-a-cmd-check-dag": "Re-run round 24: tools/check_dag.py --all rc=0; 'check_dag AC4: PASS' (out/check_dag.out).",
    "AC4-a-r19-cmd-check-projects": "Re-run round 24: tools/check_projects.py --unit AC4 rc=0, 'check_projects AC4: PASS' (out/check_projects.out).",
    "AC4-a-cmd-run-labs": "Re-run round 24: tools/run_labs.py --unit AC4 rc=0, 'run_labs AC4: PASS (10/10)' (out/run_labs.out).",
    "AC4-a-cmd-twins-isolated": "Re-run round 24: python -I -W error on tests/labs/AC4/lab-AC4-L01-1.py and lab-AC4-L02-1.py, rc=0 both, stderr empty (out/twin_L01.out, twin_L02.out; .err files 0 bytes).",
    "AC4-a-cmd-twin-output-equals-page": "Re-run round 24: check_twins_cards.py: L01 expected 20 lines equal=True; L02 expected 13 lines equal=True (out/twins_cards.out). L02 twin output line 311 unrelated; no lab line changed.",
    "AC4-a-cmd-page-smoke": "Re-run round 24: tools/page_smoke.py --unit AC4 on index, L01, L02: 'page_smoke AC4: PASS' rc=0 (out/page_smoke.out).",
    "AC4-a-cmd-pytest-labs-lint": "Re-run round 24: pytest -q -k AC4 rc=0 (10 passed, out/pytest_ac4.out); ruff check tests/labs/AC4 'All checks passed!'; ruff format --check 10 files already formatted (out/ruff_*.out).",
    "AC4-a-cmd-verify-refs": "Re-run round 24: verify_refs.py --unit AC4 'live re-verification of AC4: 2 of 560 entries, 0 problems' rc=0; --offline '560 entries, 0 problems' rc=0 (out/verify_refs_*.out).",
    "AC4-a-r18-cmd-build-site-check": "Re-run round 24: tools/build_site.py --check 'site data current: 6 outputs' rc=0 (out/build_site_check.out).",
    "AC4-a-banned-phrases": "Re-run round 24 on index.html, L01.html, L02.html (grep roughly|about N|historically|typically|usually|half|ellipsis|build|builder|verifier|round|requests): the hits are 'half' in Lab code docstring 'half up' (L02.html:203, L01.html:170) and in problem text 'each makes half of the units' (L02.html:367, 417, 419) and 'Proposition 5.1 requires constant shares' with a shown calculation; no banned phrase. The rewritten line 311 contains no banned term.",
}
ROW_CHANGED = {
    "AC4-a-L02-misconceptions": ("FAIL",
        "Round 24 re-judged the rewritten sentence (L02.html:311, the only changed line). The new wording reads 'Within a segment that has a zero, a plan's operating income is non-negative exactly when its volume is at or above that segment's zero (Proposition 4.1)'. The numbers check: recompute_311.py (out/recompute_311.out) gives the lower zero 88.89, the upper zero 2,088.89, OI(2001) = -1,186.50 USD, and the iff holds on 0..2000 and on 2001..5000 with the segment's own zero. The defect is scope: the sentence restricts the segment but not the plan's volume ('its volume' has no locator), and it sits directly after the 2,001-unit example that lies above the lower zero and loses money. Read as a general claim about the plan's volume it is false for 2,001 units. Proposition 4.1 supports only the in-segment claim, so the sentence must say that the volume lies in that segment.",
        "Rewrite L02.html:311 to: 'For a plan whose volume lies in a segment that has a zero, operating income is non-negative exactly when that volume is at or above the segment's zero (Proposition 4.1); a segment with no zero has operating income of one sign throughout.' Apply the same change to card AC4-c135, then re-run check_pages, build_site --check and this row."),
    "AC4-a-cards-L01-L02": ("FAIL",
        "Round 24: cards.json is unchanged since 503d139 (git diff --stat empty), so AC4-c135 is still 'Exactly when the volume is at or above that segment's zero (Proposition 4.1).' with no statement that the volume lies in the segment. check_twins_cards.py (out/twins_cards.out) shows 39 L01/L02 cards, unique ids, zero duplicate fronts. The card set is otherwise byte-identical to round 23 and not re-judged here.",
        "Change AC4-c135 back to say the plan's volume lies in that segment (see AC4-a-L02-misconceptions), keep grade T and the Proposition 4.1 locator, then re-run check_twins_cards.py."),
    "AC4-a-r23-card-c135": ("FAIL",
        "Round 24: cards.json AC4-c135 is byte-identical to round 23 ('Exactly when the volume is at or above that segment's zero (Proposition 4.1)'), so the round-23 defect is not fixed: the back does not restrict the volume to the segment, while the front is 'In a segment that has a zero'. A student who applies the back to 2,001 units gets the wrong answer (OI = -1,186.50 USD, out/recompute_311.out). Grade T is not supported for the unrestricted reading.",
        "Rewrite the back as 'Exactly when the volume, which lies in that segment, is at or above that segment's zero (Proposition 4.1).' and keep grade T."),
}
NEW_ROWS = [
    {"id": "AC4-a-r24-delta-scan", "check": "delta scan 503d139..23cbd6a for the AC4-a slice",
     "location": "course/modules/AC/AC4/ (index.html, L01.html, L02.html, cards.json), tests/labs/AC4/, references/references.json, tools/",
     "status": "PASS",
     "evidence": "git diff --stat 503d139 23cbd6a -- course/modules/AC/AC4 tests/labs/AC4 plans references/references.json tools: one file changed, course/modules/AC/AC4/L02.html, 1 insertion and 1 deletion at line 311 (the misconception 3 sentence). Read in full (git diff 503d139 23cbd6a -- course/modules/AC/AC4). No other AC4-a file, lab twin, card or registry entry changed."},
    {"id": "AC4-a-r24-line311-numbers", "check": "recompute the numbers and scope claims of the rewritten L02.html:311 sentence",
     "location": "course/modules/AC/AC4/L02.html:311; Lab 1 (lab-AC4-L02-1.py) constants",
     "status": "PASS",
     "evidence": "ledgers/AC4/scripts/AC4-a-r24/recompute_311.py (out/recompute_311.out): margin 1,350 cents (27/50 ratio); lower zero 88.89; upper zero 2,088.89 > 2000; OI(2001) = -118,650 cents = -1,186.50 USD; iff 'OI >= 0 exactly when Q >= segment zero' holds on 0..2000 for the lower segment and on 2001..5000 for the upper segment. The numbers and the in-segment claim are correct; the scope defect is recorded in AC4-a-L02-misconceptions."},
    {"id": "AC4-a-r24-mutants-new", "check": "three NEW student-error lab-twin mutants (r24)",
     "location": "ledgers/AC4/mutants/AC4-a-r24/L02_t01_floor_instead_of_ceiling.py, L02_t02_sensitivity_fixed_plus_one_cent.py, L02_t03_margin_uses_only_price_check.py",
     "status": "PASS",
     "evidence": "Run under python -I -W error against the unmutated twin stdout (ledgers/AC4/scripts/AC4-a-r24/out/mutants_r24.out and the r24 loop): t01 floor gives first_whole_unit 88, KILLED by stdout; t02 sensitivity with 1 cent gives a different printed value, KILLED; t03 margin check 'margin < 0' gives ZeroDivisionError rc=1 on the zero-margin case, KILLED (the lab's own ValueError path is no longer reached)."},
    {"id": "AC4-a-r24-mutants-committed", "check": "every committed AC4-a lab-twin mutant re-run (r18 to r24)",
     "location": "ledgers/AC4/mutants/AC4-a-r18 .. AC4-a-r24 (33 files); out/mutants_r24.out",
     "status": "PASS",
     "evidence": "run_mutants_r24.py: 29 KILLED, 4 SURVIVED (stdout identical, rc=0): AC4-a-r21/L01_p01_high_chosen_by_cost, AC4-a-r21/L02_p03_first_whole_unit_by_round, AC4-a-r21/L02_p04_zero_counted_as_loss, AC4-a-r22/L01_q01_residual_uses_low_month_only. Lab twins are out of scope under the architect ruling; no lesson sentence claims the lab checks these properties, so PASS as equivalent on the printed input."},
]

rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in ROW_CHANGED:
        status, ev, fix = ROW_CHANGED[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev, "fix": fix})
        continue
    if rid in RERUN:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": RERUN[rid]})
        continue
    if rid == "AC4-a-r23-mutants-committed":
        rows.append({"id": rid, "check": "every committed AC4-a lab-twin mutant re-run (r18 to r22), carried", "location": r["location"],
                     "status": "PASS", "evidence": "Re-run round 24 (see AC4-a-r24-mutants-committed): 29 of 33 KILLED, the same 4 equivalent survivors."})
        continue
    if r["status"] != "PASS":
        # previously FAIL rows not in ROW_CHANGED: none expected
        raise SystemExit(f"unhandled non-PASS row {rid}")
    loc = r["location"]
    prefix = L02_PREFIX if "L02" in loc else OTHER_PREFIX
    rows.append({"id": rid, "check": r["check"], "location": loc, "status": "PASS", "evidence": prefix + r["evidence"]})
rows += NEW_ROWS

mutants = prev["mutants"] + [
    {"id": "AC4-a-r24/L02_t01_floor_instead_of_ceiling", "description": "NEW student-error: first whole volume taken by floor instead of ceiling",
     "killed_by": "KILLED (stdout differs; first_whole_unit 88)"},
    {"id": "AC4-a-r24/L02_t02_sensitivity_fixed_plus_one_cent", "description": "NEW student-error: sensitivity computed with a 1-cent fixed-cost change",
     "killed_by": "KILLED (stdout differs)"},
    {"id": "AC4-a-r24/L02_t03_margin_uses_only_price_check", "description": "NEW student-error: zero-margin check written as 'margin < 0'",
     "killed_by": "KILLED (rc=1, ZeroDivisionError in the zero-margin case)"},
]
mutants = [m for m in mutants if m["id"] != "AC4-a-r18..r22 (27 committed lab-twin mutants)"]
mutants.insert(0, {"id": "AC4-a-r18..r24 committed lab-twin mutants (33 files)",
                   "description": "committed lab-twin mutants of L01 and L02 (ledgers/AC4/mutants/AC4-a-r18..r24)",
                   "killed_by": "29 KILLED; 4 SURVIVED with identical stdout and rc=0, recorded as equivalent or out of scope (out/mutants_r24.out)"})

fails = [r for r in rows if r["status"] != "PASS"]
n = len(rows)
frag = {
    "unit": "AC4", "slice": "AC4-a", "round": 24,
    "verifier": "independent verifier (Haiku), round 24",
    "pin": "23cbd6a", "base": "503d139",
    "checkout": "/tmp/verify24-AC4-a", "scratch": "/tmp/AC4-v/AC4-a",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": "FAIL" if fails else "PASS",
    "rows": rows, "mutants": mutants,
    "registry_flags": [], "freshness_flags": [],
    "notes": [
        "Delta 503d139..23cbd6a for AC4-a: one changed line, course/modules/AC/AC4/L02.html:311 (misconception 3). cards.json, index.html, L01.html and tests/labs/AC4 unchanged. All row ids from round 23 are kept.",
        "Carry rule: a round-23 PASS is carried only when its cited lines are byte-identical; rows that cite L02.html carry the L02 prefix because the one changed line 311 is not among their cited lines. Command rows and the banned-phrase row were re-run.",
        "Scope judgement: the rewritten line 311 gives correct numbers and an in-segment claim, but 'its volume' is not restricted to the segment; the same unrestricted wording remains in card AC4-c135. Both are FAIL with the fix in the row.",
        "Lab mutants: the four survivors are out of scope under the architect ruling on lab twins. Three new lab-twin mutants were written and killed. The project-slice grader rule does not apply to this slice.",
        "Not checked: L03 to L08 and cards of other slices; project.html and the grader; live access to external sources (none needed: the registry checks were run by verify_refs and no page was fetched); Pyodide wall-clock beyond page_smoke's own timer; hour figures were not failed on pace (design targets) and no hub or lesson hour changed.",
    ],
    "summary": (f"Slice AC4-a round 24 (pin 23cbd6a, base 503d139): {n} rows, {n - len(fails)} PASS, {len(fails)} FAIL "
                f"({', '.join(r['id'] for r in fails)}). The only delta is the rewritten L02.html:311 sentence; its numbers recompute, "
                "but its scope ('its volume') is still unrestricted and card AC4-c135 has the same wording. All command rows re-run and pass "
                "(check_pages, check_dag, check_projects, run_labs 10/10, twins equal embedded output, page_smoke, pytest, ruff, verify_refs live and offline, build_site --check). "
                "Mutants: 29 of 33 lab-twin mutants killed, 4 equivalent or out of scope; 3 new killed."),
}
out = ROOT / "ledgers/AC4/AC4-a.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", n, "fails", [r["id"] for r in fails])
