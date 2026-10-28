"""Round-9 fragment writer for AC4-e. Each row's status and evidence are stated here, with the command output it cites."""
import json
import re
from pathlib import Path

ROOT = Path("/tmp/verify9-AC4-e")
PREV = json.loads(Path("/tmp/fanout-frags/AC4-e.round8.json").read_text(encoding="utf-8"))
OUT = Path("/tmp/ac4-v/e9")
PROJ_CARRY = "course/modules/AC/AC4/project.html lines outside the round-9 hunks (146, 260, 324, 359) byte-identical since 2c8162b"
GRADER_CARRY = "course/modules/AC/AC4/grader/ and tests/labs/AC4/ and references/ byte-identical since 2c8162b (git diff --quiet)"
CARDS_CARRY = "course/modules/AC/AC4/cards.json entries other than AC4-c061 (line 436) byte-identical since 2c8162b"

# mutants: parsed from the round-9 run of tools/mutate_graders.py
mut_rows = []
for line in (OUT / "mutate46.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (m\d\d\w*)\.py: (.*) -> (.*)$", line)
    if m:
        mut_rows.append({"id": m.group(2), "file": f"ledgers/AC4/mutants/{m.group(2)}.py",
                         "description": m.group(3), "killed_by": m.group(4), "status": m.group(1)})
assert len(mut_rows) == 46, len(mut_rows)
killed = {r["id"]: r["killed_by"] for r in mut_rows if r["status"] == "KILLED"}
assert len(killed) == 46
def kb(prefix):
    ids = [i for i in killed if i.split("_")[0] in prefix]
    return "; ".join(f"{i.split('_')[0]} {killed[i].split(' (seed')[0]}" for i in sorted(ids))
mut_ids = lambda lo, hi: [f"m{n:02d}" for n in range(lo, hi + 1)]
def mk(lo, hi):
    return "; ".join(f"{k.split('_')[0]} killed by {killed[k].split(' (seed')[0]}" for k in sorted(killed) if int(k[1:3]) in range(lo, hi + 1))

RERUN = "Re-run round 9 (tools/mutate_graders.py --unit AC4 --seeds 0-9, output /tmp/ac4-v/e9/mutate46.out: 46/46 killed)"

NEW = {
 "proj-autograder-reference": ("PASS", "Re-run round 9: ledgers/AC4/scripts/AC4-e-r9/collect.py grader/reference.py 0 -> '296 passed in 0.08s'; tools/run_graders.py --unit AC4 --seeds 0-49 -> 'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.2 s)' (/tmp/ac4-v/e9/run_graders.out)."),
 "proj-collect-count": ("PASS", "Re-run round 9 (collect.py): 'test_project.py: 296'. project.html line 265 reads 'collects <strong>296 checks</strong>'. Equal."),
 "proj-autograder-alternatives": ("PASS", "Re-run round 9 (ledgers/AC4/scripts/AC4-e-r9/run_alts.py on alt_a, b, c, e, f, g, h, i, j and the new alt_k): all ten pass 296 tests on seeds 0-9 and 25 (/tmp/ac4-v/e9/alts.out, 10 'PASS all'). alt_k (new, make_mutants_r9.py) rounds with Decimal ROUND_HALF_UP at 60 digits instead of integer arithmetic; the rest differ in validation and in computation order."),
 "proj-instances": ("PASS", "Re-run round 9: tools/run_graders.py --unit AC4 --seeds 0-49 reports PASS; instance.py unchanged since 2c8162b (git diff --quiet)."),
 "proj-alt-instance-coverage": ("PASS", "Re-run round 9: run_graders AC4 PASS over seeds 0-49 with the starter excluded from the reference run (/tmp/ac4-v/e9/run_graders.out); starter.py unchanged since 2c8162b."),
 "proj-mutants-m01-m06": ("PASS", RERUN + " " + mk(1, 6)),
 "proj-mutant-m07-empty-name": ("PASS", RERUN + " " + mk(7, 7)),
 "proj-mutants-m08-m11": ("PASS", RERUN + " " + mk(8, 11)),
 "proj-mutant-m12-duplicate-names": ("PASS", RERUN + " " + mk(12, 12)),
 "proj-mutants-m13-m20": ("PASS", RERUN + " " + mk(13, 20)),
 "proj-mutants-m15-m19": ("PASS", RERUN + " " + mk(15, 19)),
 "proj-mutants-m21-m24": ("PASS", RERUN + " " + mk(21, 24)),
 "proj-mutants-m21-m24-equivalence": ("PASS", RERUN + " m21-m24 are not equivalent: each is killed (" + mk(21, 24) + ")."),
 "proj-mutants-m25-m29": ("PASS", RERUN + " " + mk(25, 29)),
 "proj-mutants-r6-new": ("PASS", RERUN + " " + mk(30, 34)),
 "proj-mutant-descriptions": ("PASS", RERUN + ": every docstring's first line is the description printed in mutate46.out, and each is KILLED."),
 "proj-spec-empty-name-claim": ("PASS", RERUN + " m07 " + killed["m07_empty_name_accepted"] + "; the test test_empty_product_name_raises_value_error is in the 296 collected (collect.py)."),
 "proj-spec-fresh-objects-claim": ("PASS", RERUN + " m27 " + killed["m27_master_returns_cached_object"] + "; test_master_returns_fresh_objects collected and passing on the reference."),
 "proj-spec-clarity-and-errors": ("PASS", "Re-run round 9: Constraints line (project.html line 263) unchanged; grader unchanged since 2c8162b. Boolean and product-field kills re-run: m35 " + killed["m35_bool_accepted_in_product_fields"] + "; m36 " + killed["m36_flexible_accepts_bool_units"] + "; m39 " + killed["m39_bool_actual_inputs_refused_only_by_master"] + "; m40 " + killed["m40_zero_budget_units_refused_only_by_master"] + "."),
 "proj-messages-bare-asserts": ("PASS", "Re-run round 9: ledgers/AC4/scripts/AC4-e-r9/scan_r9.py -> 'asserts without message: []' (/tmp/ac4-v/e9/scan.out)."),
 "proj-messages-no-leak": ("PASS", "Carried from round 8 (" + GRADER_CARRY + "): messages at test_project.py lines 591, 671 and 684 unchanged; the messages name the field or the function, never a reference value."),
 "proj-rubric-exhaustive": ("PASS", "Carried from round 8 (" + PROJ_CARRY + "): the rubric rows (C1 to C5, four levels each, lines 314-318) are outside the round-9 hunks; the table has five criterion rows (data-criterion C1..C5), re-read in round 9."),
 "proj-rubric-scoring-rule": ("PASS", "Carried from round 8 (" + PROJ_CARRY + "): line 308 'Scoring rule.' read in round 9, unchanged."),
 "proj-rubric-C4-observation": ("PASS", "Carried from round 8 (" + PROJ_CARRY + "): the C4 descriptors (line 317) and the exemplar B threshold sentence are outside the round-9 hunks; the threshold itself is re-derived in proj-exemplar-B-threshold."),
 "proj-calib-A-scores": ("PASS", "Re-run round 9: article exemplar-a has data-level=\"1\" and data-scores=\"2,2,2,1,2\" (line 326); the verdict text at line 328 reads 'C1 2 · C2 2 · C3 2 · C4 1 · C5 2'. Equal."),
 "proj-calib-A-annotation": ("PASS", "Carried from round 8 (" + PROJ_CARRY + "): annotation lines 345-350 unchanged. Exemplar A's memo text 'the plant earned more on the units it sold more of' (line ~336) is quoted exactly in the C2 annotation; the mix sign in the memo ('+462,857') is the wrong sign the C1 annotation names, and the lab output is -462,857 (project.html line 143 area)."),
 "proj-calib-B-scores": ("PASS", "Re-run round 9: article exemplar-b data-level=\"3\" and data-scores=\"4,4,3,4,4\" (line 357); verdict text at line 359 reads 'C1 4 · C2 4 · C3 3 · C4 4 · C5 4'. Equal."),
 "proj-calib-B-annotation": ("PASS", "Carried from round 8 (" + PROJ_CARRY + "): annotation lines 377-382 unchanged; each annotation's claim re-read against the memo: volume and price figures, the 53,000 and 167,000 consequence, and the 5,400 threshold (see proj-exemplar-B-threshold)."),
 "proj-memo-structure-length": ("PASS", "Re-run round 9: ledgers/AC4/scripts/AC4-e-r9/scan_r9.py -> exemplar-a memo 321 words, exemplar-b memo 412 words (whitespace split after stripping tags), both inside 300-600; headings Result, Causes, Recommendation (A) and Result, Causes, Assumptions, Recommendation (B)."),
 "proj-exemplar-B-consequences": ("PASS", "Re-run round 9: Assumptions paragraph (exemplar B, line ~370): '210 cents' is labelled 'If the actual input price were 210 cents'; (210 - 200) x 5,300 = 53,000; 220,000 - 53,000 = 167,000 (python -I calc, /tmp/ac4-v/e9/calc/check_lines.py)."),
 "proj-exemplar-B-threshold": ("PASS", "Re-run round 9 (check_lines.py with the reference's variance_decomposition): Deluxe budget price 5,400 gives sales_mix 0; 5,399 gives +129; 5,000 gives +51,429. Margin: 5,400 - 5 x 200 = 4,400 = Standard's 5,000 - 3 x 200. The sign turns favourable below 5,400, as the memo says."),
 "proj-reading-list-sentence": ("PASS", "Carried from round 8 (" + PROJ_CARRY + "): dt 'Reading list' line 266, dd line 267 unchanged."),
 "proj-hours": ("PASS", "Re-run round 9: project.html table rows 1+2+2+6+4+2+2+1 = 20 (the Total row says 20); index.html data-hours-lessons=\"50\", data-hours-project=\"20\" (line 29) and the eyebrow '50 h lessons · 20 h project (28.6% of 70 h)'; 50 + 20 = 70; 20/70 = 28.6%. Arithmetic consistent (architect ruling: pace not checked)."),
 "proj-ladder-lede": ("PASS", "Carried from round 8 (" + PROJ_CARRY + "): line 42 unchanged; index.html not in the delta (git diff --quiet)."),
 "proj-simulated-and-data": ("PASS", "Re-run round 9: run_labs AC4 PASS (10/10); Lab 1 'SIMULATED' label at project.html lines 53-56 and Inputs line 252 unchanged since 2c8162b."),
 "proj-equal-margin-branch": ("PASS", "Carried from round 8 (" + GRADER_CARRY + "): test_project.py lines 463-480 unchanged; suite passes on the reference (296 passed)."),
 "proj-grader-equal-margin-comment": ("PASS", "Carried from round 8 (" + GRADER_CARRY + "): test_project.py lines 472-474 unchanged."),
 "proj-rubric-C2-terms": ("PASS", "Carried from round 8 (" + PROJ_CARRY + "): line 308 scoring rule and line 315 C2 row unchanged."),
 "proj-exemplar-overall-level": ("PASS", "Re-run round 9: intro sentence 'overall levels 1 and 3' (line 324, the sentence unchanged apart from the universal clause) matches data-level=\"1\" (exemplar A, line 326) and data-level=\"3\" (exemplar B, line 357)."),
 "proj-citations-reading": ("PASS", "Re-run round 9: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (/tmp/ac4-v/e9/verify_refs_offline.out). references/ unchanged since 2c8162b. The live run was not repeated this round (see notes)."),
 "proj-mutants-r7-new": ("PASS", RERUN + " m35 and m36 " + killed["m35_bool_accepted_in_product_fields"] + " / " + killed["m36_flexible_accepts_bool_units"] + "; m37 " + killed["m37_master_warns"]),
 "proj-autograder-rerun-mutants-m01-m37": ("PASS", RERUN + ". Full set now m01-m46 (46 files in ledgers/AC4/mutants)."),
 "proj-mutants-r8-new": ("PASS", RERUN + " m38-m40: " + mk(38, 40)),
 "proj-spec-coverage-claims": ("PASS", "Re-run round 9: collect count 296 equals line 265 'collects 296 checks' (collect.py). The coverage clauses (each ValueError, purity, silence) are the test names in the 296, unchanged since 2c8162b."),
 "proj-stretch-two-inputs": ("PASS", "Carried from round 8 (" + PROJ_CARRY + "): the 'Two inputs' bullet at line 399 unchanged; its identity re-derived in round 8 (stretch_r8.py) and not affected by the round-9 hunks."),
 "proj-stretch-spending": ("PASS", "Carried from round 8 (" + PROJ_CARRY + "): the 'A spending variance' bullet at line 398 unchanged; it now supports the round-9 claims at lines 146 and 260 (input price and fixed overhead variances are the stretch items)."),
 "proj-stretch-list-intact": ("PASS", "Carried from round 8 (" + PROJ_CARRY + "): the Rung 4 list (lines 396-401, three bullets, in order) unchanged; the stretch section is 'section id=\"stretch\"' at line 395."),
 "proj-lab-1": ("PASS", "Re-run round 9: run_labs AC4 PASS (10/10). The Lab 1 code and expected output (lines 53-145) are byte-identical; only the interpretation line 146 changed (see proj-lab-1-interpretation)."),
 "proj-lab-1-interpretation": ("PASS", "Re-run round 9 on the changed line 146: 'Standard rose from 71.4% of budgeted total units (1,000 of 1,400) to 80.0% of actual total units (1,200 of 1,500)': 1000/1400 = 71.43%, 1200/1500 = 80.0%, correct to 1 dp. 'Standard earns 4,400 cents of margin per unit against Deluxe's 8,000': 5000 - 3x200 = 4400, 9000 - 5x200 = 8000. Mix -462,857 = 2,680,000 - 3,142,857 (computed by check_lines.py). Price +180,000 = 240,000 - 60,000; efficiency -40,000 = 200 x (5,100 - 5,300) with the standard 5,100 = 3x1200 + 5x300. 'The lab does not compute what a different input price would do': the Lab 1 code has one INPUT_PRICE and no price term. 'the stretch section asks you to add one': stretch bullet 1 (line 398) asks for an input price variance. 1/7 cent: exact flexed profit 3,142,857 1/7 (check_lines.py). Sum 180,000 + 542,857 - 462,857 - 40,000 = 220,000."),
 "proj-lab-2": ("PASS", "Re-run round 9: run_labs AC4 PASS (10/10); the Lab 2 blanks and expected output (lines 149-243) unchanged."),
 "proj-purity-order-dependence": ("PASS", "Re-run round 9: the purity and order tests are in the 296 collected and pass on the reference (run_graders AC4 PASS); test_project.py unchanged since 2c8162b."),
 "proj-card-c020": ("PASS", "Carried from round 8 (" + CARDS_CARRY + "): entry AC4-c020 (lines 134-138) unchanged."),
 "proj-card-c078": ("PASS", "Carried from round 8 (" + CARDS_CARRY + "): entry AC4-c078 (lines 553-557) unchanged; L06 Proposition 2.1 (L06.html line 78) unchanged."),
 "proj-cards-structure": ("PASS", "Re-run round 9: ledgers/AC4/scripts/AC4-e-r9/cards_r9.py -> 119 cards, 119 unique ids, three key sets (31 without grade, 45 grade T without basis, 43 grade C with basis), lessons L01-L08 all have their .html files, grades in {T, C}."),
 "proj-cards-duplicates": ("PASS", "Re-run round 9: scan_r9.py -> 'duplicate fronts: [] duplicate backs: []'; ids sequential AC4-c001..c119."),
 "proj-cards-sample": ("PASS", "Carried from round 8 (" + CARDS_CARRY + "): sampled entries c010 to c080 (c061 is re-checked separately) unchanged."),
 "proj-cards-targeted": ("PASS", "Carried from round 8 (" + CARDS_CARRY + "): entries c062, c063, c064, c066, c067, c075, c076 unchanged."),
 "proj-cards-number-format": ("PASS", "Carried from round 8 (" + CARDS_CARRY + "): entries c101, c102, c109 unchanged."),
 "proj-cards-changed-lessons": ("PASS", "Re-run round 9 for AC4-c061 (L05, the only changed card): front 'What sign convention does this lesson use for variances?' matches L05 Definition 1.3 (L05.html line 58-59: 'Every variance in this lesson is stated as its effect on operating profit...'). Back: 'A variance is actual minus budget for each line that adds to profit, and cost lines enter with the sign that makes a higher cost reduce profit. A positive variance is favourable ... A negative variance is unfavourable.' Matches Definition 1.3 text. Other L05 cards (c059-c068) and L06 cards carried: " + CARDS_CARRY + "."),
 "proj-card-c091": ("PASS", "Carried from round 8 (" + CARDS_CARRY + "): entry AC4-c091 (line 641) unchanged."),
 "proj-banned-phrases": ("PASS", "Re-run round 9: scan_r9.py -> 'banned hits: []' over project.html text (tags stripped) and every card front and back."),
 "proj-page-smoke": ("PASS", "Re-run round 9: tools/page_smoke.py --unit AC4 --pages project.html -> 'page_smoke AC4: PASS' (Chromium, light and dark, 360 px; /tmp/ac4-v/e9/page_smoke.out)."),
 "proj-check-projects": ("PASS", "Re-run round 9: tools/check_projects.py --all -> 'check_projects AC4: PASS' (plus CF1, AP1)."),
 "proj-check-pages": ("PASS", "Re-run round 9: tools/check_pages.py --unit AC4 -> 'check_pages AC4: PASS'; --all lines show AC4 PASS."),
 "proj-check-dag": ("PASS", "Re-run round 9: tools/check_dag.py --all -> 'check_dag AC4: PASS'."),
 "proj-ruff-mypy": ("PASS", "Re-run round 9: ruff check and ruff format --check on course/modules/AC/AC4/grader and tests/labs/AC4 -> 'All checks passed!', '14 files already formatted'; mypy --no-incremental -> 'Success: no issues found in 153 source files'."),
 "proj-run-labs-ac4": ("PASS", "Re-run round 9: tools/run_labs.py --unit AC4 -> 'run_labs AC4: PASS (10/10)'."),
 "proj-inputs-every-number-int": ("PASS", "Re-run round 9: the Conventions paragraph (line 260) keeps the sentence 'every number it returns is an int'; the reference returns ints throughout (_nearest_cent and all dict values are int; the grader's type checks pass on the reference and on alt_k)."),
 "proj-exemplar-intro-universal-claim": ("FAIL", "Round 9 check of the new universal clause at line 324: 'Every other figure they state is either derived from those figures or labelled as a what-if'. Exemplar B's figures all check: 2,820,000 (derived), 1,500/1,400/1,000/400 units, 71.4%/80.0%/28.6%/20.0% (derived), 53,000 and 167,000 (labelled 'If the actual input price were 210 cents'), 5,400 (derived threshold). Exemplar A states '+462,857 cents' for the mix variance; the derived value is -462,857 (lab step 6), so that figure is not derived from the case figures. Its annotation calls the sign wrong, so the universal 'every ... derived' clause is contradicted by the exemplar's own annotation."),
 "proj-stretch-two-inputs-scope": ("PASS", "Carried from round 8 (" + PROJ_CARRY + "): the 'Two inputs' bullet (line 399) unchanged."),
 "proj-grader-comments": ("PASS", "Carried from round 8 (" + GRADER_CARRY + "): test_project.py lines 43-44 unchanged."),
}
NEW["proj-exemplar-intro-universal-claim"] = ("FAIL", NEW["proj-exemplar-intro-universal-claim"][1])
FIX = ("Reword line 324 so the universal clause holds for both exemplars, for example: 'Apart from Exemplar A's mix sign, which its annotation marks wrong, every other figure they state is derived from those figures or labelled as a what-if.' Or state the exemplar's own errors separately. Verifier does not fix.")

rows = []
for r in PREV["rows"]:
    rid = r["id"]
    if rid in NEW:
        status, evidence = NEW[rid]
    else:
        raise SystemExit(f"round-8 row without round-9 disposition: {rid}")
    row = {"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = FIX
    rows.append(row)

# new rows of round 9
rows.append({"id": "proj-mutants-r9-new", "check": "Round-9 student-error mutants m41-m46 are killed on seeds 0-9",
             "location": "ledgers/AC4/mutants/m41_mix_uses_budgeted_units.py; m42_zero_actual_units_refused.py; m43_flexed_revenue_at_actual_price.py; m44_total_is_flexed_minus_master.py; m45_fixed_overhead_twice_in_flexed.py; m46_half_even_rounding.py",
             "status": "PASS", "evidence": RERUN + " New mutants (generated from the reference by make_mutants_r9.py, one error each): " + mk(41, 46) + "."})
rows.append({"id": "proj-autograder-alt-decimal", "check": "A Decimal half-up implementation (different valid algorithm) passes the suite",
             "location": "ledgers/AC4/scripts/AC4-e-r9/alt_k.py; course/modules/AC/AC4/grader/test_project.py",
             "status": "PASS", "evidence": "Re-run round 9 (run_alts.py): alt_k.py PASS all, 296 passed on seeds 0-9 and 25 (/tmp/ac4-v/e9/alts.out)."})
rows.append({"id": "proj-conventions-no-spending-claim", "check": "Conventions paragraph: 'no input price variance and no fixed overhead variance; the stretch section asks you to add them'",
             "location": "course/modules/AC/AC4/project.html line 260 (Conventions, fourth paragraph); line 398 (stretch bullet 1)",
             "status": "PASS", "evidence": "Re-run round 9 on the changed line 260: the Inputs paragraph says the input price is the standard price and the price paid, and the fixed overhead is the same in both periods, so the case holds both at budget (consistent). Stretch bullet 1 asks to 'Add an input price variance and a fixed overhead variance' (line 398). The 'every number it returns is an int' clause is unchanged."})
rows.append({"id": "proj-exemplar-B-verdict", "check": "Exemplar B verdict (changed line 359): 'reports each variance with its sign, ties each variance to the case, states both assumptions and says which costs vary, and gives a reversing threshold'",
             "location": "course/modules/AC/AC4/project.html line 359 (exemplar B verdict); exemplar B memo lines 362-375",
             "status": "PASS", "evidence": "Re-run round 9: each of the four variances (sales volume +542,857, sales price +180,000, efficiency -40,000, sales mix -462,857) and the total +220,000 is stated with its sign in the Result and Causes; each is tied to a case figure; Assumptions gives fixed overhead (5,000,000 both periods) and the input price (200); 'Costs vary with units in proportion to the standard input per unit' says which vary; the Recommendation gives the 5,400 threshold (checked above). The verdict's 'does not test the variable-cost assumption' is consistent with the memo text."})
rows.append({"id": "proj-card-c061", "check": "AC4-c061 (changed front, lesson L05) matches L05 Definition 1.3", "location": "course/modules/AC/AC4/cards.json line 436 (AC4-c061); course/modules/AC/AC4/L05.html lines 58-59 (Definition 1.3)",
             "status": "PASS", "evidence": "Re-run round 9: L05.html line 59 'Every variance in this lesson is stated as its effect on operating profit. A variance is actual minus budget for each line that adds to profit, and the cost lines enter with the sign that makes a higher cost reduce profit. A positive variance is favourable ... A negative variance is unfavourable.' The card's question 'this lesson' matches 'in this lesson'; the card's back matches the definition (cost lines enter with the sign that makes a higher cost reduce profit)."})
rows.append({"id": "proj-lab-1-interpretation-second-clause", "check": "Lab 1 interpretation: 'the lab does not compute what a different input price would do'",
             "location": "course/modules/AC/AC4/project.html line 146", "status": "PASS",
             "evidence": "Re-run round 9: the Lab 1 code uses one INPUT_PRICE (line 'INPUT_PRICE = 200') for standard and actual cost and has no price-variance step, so it computes no alternative price. Covered by proj-lab-1-interpretation."})

rows.append({"id": "proj-lab-1-run-line146-untouched", "check": "Lab 1 expected output unchanged by the round-9 edit", "location": "course/modules/AC/AC4/project.html lines 53-145 (the code and the pre block)",
             "status": "PASS", "evidence": "Re-run round 9: the diff 2c8162b..96dd532 touches project.html only at lines 146, 260, 324, 359; run_labs AC4 PASS (10/10)."})

mutants = [{"id": r["id"], "file": r["file"], "description": r["description"], "killed_by": r["killed_by"]} for r in mut_rows]
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
counts = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": sum(r["status"] != "PASS" for r in rows),
          "non_pass_ids": [r["id"] for r in rows if r["status"] != "PASS"], "mutants": len(mutants), "mutants_killed": len(killed)}
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
for old in PREV["rows"]:
    assert old["id"] in ids, old["id"]
frag = {
 "unit": "AC4", "slice": "AC4-e", "round": 9,
 "verifier": "Claude Haiku 5.5 (independent verifier, round 9, slice AC4-e; did not build AC4)",
 "pin": "96dd532", "base": "2c8162b (round-8 pin; previous fragment /tmp/fanout-frags/AC4-e.round8.json used as context; carried rows state the cited lines or files byte-identical since 2c8162b)",
 "previous_ledger": "/tmp/fanout-frags/AC4-e.round8.json", "checkout": "/tmp/verify9-AC4-e", "scratch": "/tmp/ac4-v/e9",
 "verified_at": "2026-10-28T13:00:00+00:00", "verdict": verdict,
 "rows": rows, "mutants": mutants, "registry_flags": [], "freshness_flags": [],
 "notes": [
  "Delta 2c8162b..96dd532 for this slice: project.html (hunks at lines 146, 260, 324, 359 only) and cards.json (AC4-c061 front only). grader/, tests/labs/AC4/, references/, index.html and L01-L08 are byte-identical (git diff --quiet).",
  "Round-8 FAIL proj-exemplar-intro-universal-claim is re-verified: exemplar B's figures now pass; exemplar A's mix figure '+462,857' is not derived from the case and still breaks the universal clause. One FAIL remains.",
  "New mutants m41-m46 (six, each a single student error written from the reference by ledgers/AC4/scripts/AC4-e-r9/make_mutants_r9.py): 46/46 killed on seeds 0-9. Survivors: none.",
  "Alternatives: ten correct implementations (alt_a, b, c, e, f, g, h, i, j, and the new alt_k with Decimal rounding) pass 296 tests on seeds 0-9 and 25.",
  "Not checked: the live verify_refs run (not repeated; references unchanged, offline integrity 560 entries 0 problems); the full line-by-line read of L01-L08 (outside this slice, only the L05 Definition 1.3 cited by the changed card was re-read); the carried rows in the exemplar and rubric sections were not re-derived beyond the lines the delta touches; Pyodide beyond page_smoke's Chromium run; the registry entries for the reading list.",
  "Not applied: no fixes made (the verifier does not fix). The fix for the one FAIL is on the row.",
  "The round-8 scripts were copied from /tmp/verify8-AC4-e and their paths rewritten to this checkout (ledgers/AC4/scripts/AC4-e-r9/)."
 ],
 "summary": counts,
}
Path(ROOT / "ledgers/AC4/AC4-e.json").write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(json.dumps(counts))
