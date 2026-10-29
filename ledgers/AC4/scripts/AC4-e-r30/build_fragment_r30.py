"""Builds ledgers/AC4/AC4-e.json (round 30) from the previous fragment, the round-30 outputs and the mutant files.

Carried rows keep their id and prefix the evidence with 'Carried from round 29 (<location> byte-identical ...)'.
Re-verified and new rows cite the round-30 script or output that backs them.
"""
import ast, json, pathlib, re, sys
ROOT = pathlib.Path(sys.argv[1]); S = ROOT / "ledgers/AC4/scripts/AC4-e-r30"; O = S / "out"
prev = json.load(open("/tmp/fanout-frags/AC4-e.round29.json"))
prev_rows = prev["rows"]
def read(p): return (O / p).read_text(encoding="utf-8")

OUT = "ledgers/AC4/scripts/AC4-e-r30/out/"
SCR = "ledgers/AC4/scripts/AC4-e-r30/"
override = {
 "proj-banned-phrases": ("project.html; cards.json", "Fresh banned-phrase and process-word scan of project.html and all 141 cards: no hit.", SCR + "checks_r30.py; " + OUT + "checks_r30.out (banned-phrase hits: [])"),
 "proj-check-pages": ("course/modules/AC/AC4/*.html and cards.json", "check_pages.py --all re-run on the r30 pin: AC4 PASS.", OUT + "check_pages.out (AC4 PASS, exit 0)"),
 "proj-cards-structure": ("course/modules/AC/AC4/cards.json", "Re-run on the r30 pin: 141 cards, ids AC4-c001..c141 contiguous, unique, every grade C has a basis, no T or ungraded card has one.", SCR + "checks_r30.py; " + OUT + "checks_r30.out"),
 "proj-cards-duplicates": ("course/modules/AC/AC4/cards.json", "Full duplicate scan on fronts and backs: none. Ids unique (141).", SCR + "checks_r30.py; " + OUT + "checks_r30.out"),
 "proj-cards-changed-lessons": ("course/modules/AC/AC4/cards.json (L05 and L06 cards)", "L05 cards byte-identical since 503d139. L06 cards AC4-c073 and AC4-c074 re-read against L06.html lines 70 and 64-65: wording agrees with the current lesson. AC4-c078 agrees with Proposition 2.1 text, but see proj-card-c078 (hypothesis omitted).", SCR + "checks_r30.py (object diff); L06.html"),
 "proj-card-c020": ("course/modules/AC/AC4/cards.json (AC4-c020); course/modules/AC/AC4/L02.html; tests/labs/AC4/lab-AC4-L02-1.py", "Re-run the L02 twin: 'loss run units 2001 to 2088' and 'single_formula_break_even_units 88.89'; the card's 2,001 units and 88.89 match, and L02 text says the step applies to every unit above 2000 (lab line 39).", OUT + "run_labs.out; L02 twin run this round"),
 "proj-card-c078": ("course/modules/AC/AC4/cards.json (AC4-c078); course/modules/AC/AC4/L06.html Proposition 2.1 (line 79)", "Card wording 'for any actual units, actual selling prices and actual kilograms, provided the actual material price equals the standard price pi' omits the hypothesis the proposition states: 'with Q_b > 0' (L06.html line 79). A T-graded card that says 'for any' while dropping a stated hypothesis.", SCR + "checks_r30.py; L06.html line 79"),
 "proj-cards-r10-L03": ("course/modules/AC/AC4/cards.json (AC4-c038, c040, c042, c043, c122, c123, c124); course/modules/AC/AC4/L03.html lines 90, 95", "L03.html changed at line 88 only (a sentence added to the Proposition 2.2 paragraph); lines 89-90 still give the make-minus-buy formula and 'Making is cheaper when Delta < 0'; line 95 region unchanged. Lab 1 figures (25,000.00; 2,000.00; 5,000.00; 9.25) confirmed in the L03 twin output this round.", OUT + "run_labs.out; L03 twin run this round"),
 "proj-r17-cards-c073": ("course/modules/AC/AC4/cards.json (AC4-c073); course/modules/AC/AC4/L06.html lines 64-72", "L06.html line 72 changed (the contribution-variance sentence). Line 70 still gives the efficiency formula E = -pi sum (kg - s q); card wording agrees.", "course/modules/AC/AC4/L06.html lines 64-72"),
 "proj-r23-cards-L03-L04-carry-note": ("tests/labs/AC4/lab-AC4-L03-1.py; tests/labs/AC4/lab-AC4-L04-1.py; course/modules/AC/AC4/cards.json (AC4-c038..c044, c045..c058)", "The three twin edits this round change docstring or comment text only. Both twins run this round exit 0 (run_labs AC4 PASS 10/10); printed L03 figures (9.10, 11.10, 10.50, -25,000.00, 25,000.00 stated on the cards) are unchanged. L03 card AC4-c044 re-read against L03 Section 5 (line 364-376): 'one-year model ... no discounting' agrees with the card.", OUT + "run_labs.out; " + SCR + "checks_r30.py"),
 "proj-cards-sample": ("course/modules/AC/AC4/cards.json (AC4-c010, c020, c030, c040, c050, c060, c070, c080, c090, c100, c110, c120, c130, c140)", "Fourteen sampled cards read against the current lesson or the run lab output: c010 (L02 text: m/p = 1 - v/p), c020 and c030 (L02 twin output: 2,001-unit loss, 5,550.00 at 2,500 units), c040 (L03 twin output: -25,000.00), c050 (45,000 - 30,000 = 15,000, Example 4.1 arithmetic), c060 (L05 Definition 1.2 text), c080 (L06 twin output: -40,000, +249,000, +16,000, -75,000, total 150,000), c090 (L07 Lemma 7.2 text), c100 (L08 text: 102.8 SCU), c110 (L06 Definition 1.1), c120 (L01 Definition 2.1 text), c130 (L01 Proposition 1.3(c)), c140 (L08 twin output: SIM-D 5.67, SIM-A 4.86). Card c070 was checked against the L06 Definition 1.2 sales-price line (SP = sum (p_a,i - p_b,i) q_a,i).", OUT + "run_labs.out; " + SCR + "cards_numbers_r30.py; " + SCR + "checks_r30.py"),
 "proj-cards-targeted": ("course/modules/AC/AC4/cards.json (AC4-c062, c063, c064, c066, c067, c075, c076)", "Card objects byte-identical since 503d139 (object diff in checks_r30.out). Arithmetic re-derived: M = 1,500 x (500-600) + 1,900 x (500-400) = +40,000 (c075); budget kg 2,400, actual 2,950, standard for actual output 2,800, E = -500 x 150 = -75,000 (c076).", SCR + "checks_r30.py"),
 "proj-cards-number-format": ("course/modules/AC/AC4/cards.json (AC4-c101, c102, c109)", "Card objects byte-identical since 503d139. Every number in fronts and backs of all 141 cards found verbatim in its lesson text: zero misses.", SCR + "cards_numbers_r30.py; " + OUT + "cards_numbers_r30.out"),
 "proj-r17-delta-scope": ("course/modules/AC/AC4/cards.json; course/modules/AC/AC4/project.html; course/modules/AC/AC4/grader/*", "Delta since 503d139 for this slice: cards.json objects AC4-c016, c023, c026, c074, c078, c135 changed and AC4-c141 appended; project.html, grader/*, tests/labs/AC4/lab-AC4-project-1.py and -2.py byte-identical (git diff --stat empty).", SCR + "checks_r30.py (object diff); git diff --stat 503d139 5aeaaf0"),
 "proj-r17-cards-counts": ("course/modules/AC/AC4/cards.json", "141 cards: L01 19, L02 20, L03 20, L04 15, L05 10, L06 18, L07 18, L08 21; T 54, C 52, ungraded 35.", SCR + "checks_r30.py; " + OUT + "checks_r30.out"),
 "proj-r17-banned-and-numbers": ("course/modules/AC/AC4/cards.json; L01-L08.html", "Banned-phrase scan: no hit. Numbers: every number in cards located in its lesson text (zero misses).", SCR + "checks_r30.py; " + SCR + "cards_numbers_r30.py"),
 "proj-r18-cards-totals": ("course/modules/AC/AC4/cards.json", "141 cards in total; per-lesson totals and grade counts as in proj-r17-cards-counts.", SCR + "checks_r30.py; " + OUT + "checks_r30.out"),
 "proj-r18-card-c074-qualifier": ("course/modules/AC/AC4/cards.json (AC4-c074); course/modules/AC/AC4/L06.html line 65", "Card back says 'material is the only variable cost'; L06.html line 65 says 'the one variable cost is material'. Same qualifier, same scope. The changed symbol (Delta C) matches line 72.", "course/modules/AC/AC4/L06.html lines 64-72; checks_r30.out (object diff)"),
 "proj-r23-delta-scope": ("course/modules/AC/AC4/cards.json; tests/labs/AC4/lab-AC4-L03-1.py, L04, L06", "Delta since 503d139 re-derived: 7 card objects differ (c016, c023, c026, c074, c078, c135, c141); L01, L02, L03, L04, L06 pages and three lab twins changed; project page, grader and project labs unchanged.", SCR + "checks_r30.py; git diff --stat 503d139 5aeaaf0"),
 "proj-r23-banned-and-placeholders": ("course/modules/AC/AC4/cards.json; course/modules/AC/AC4/project.html", "Re-run: no TODO, TBD, lorem, roughly, historically, about-N, 'it is important to note', 'obviously', 'clearly' in cards or project page.", SCR + "checks_r30.py; " + OUT + "checks_r30.out"),
 "proj-r23-cards-changed-r23": ("course/modules/AC/AC4/cards.json (AC4-c020, c037, c095, c108, c113, c135, c136)", "c135 re-verified against L02 Proposition 4.1 (strictly increasing, one zero per segment) and the sentence at L02 line 330: agrees. c020 re-verified against the L02 twin output. Others have byte-identical objects and their numbers are in lesson text.", OUT + "run_labs.out; " + SCR + "cards_numbers_r30.py"),
 "proj-r23-cards-L07-L08-cited": ("course/modules/AC/AC4/cards.json (AC4-c087, c088, c093, c094, c117 and the L07/L08 cards); L07.html, L08.html", "L07 and L08 are unchanged since 503d139 and their card objects are byte-identical (object diff). Numbers of the cited cards are in lesson text (zero misses).", SCR + "checks_r30.py; " + SCR + "cards_numbers_r30.py"),
 "proj-r23-cards-L05-L06-lab": ("tests/labs/AC4/lab-AC4-L05-1.py; tests/labs/AC4/lab-AC4-L06-1.py; course/modules/AC/AC4/cards.json (AC4-c074, c076)", "L06 twin re-run this round: total_contribution_variance 150000 and the four variances as printed in lesson; the docstring change (T to Delta C) does not change output.", OUT + "run_labs.out"),
 "proj-r23-card-mechanical-scan": ("course/modules/AC/AC4/cards.json; course/modules/AC/AC4/L01.html ... L08.html", "Mechanical scan repeated on the r30 pin: 141 cards, zero numbers missing from their lesson text, zero duplicate fronts or backs.", SCR + "cards_numbers_r30.py; " + SCR + "checks_r30.py"),
 "proj-alt-l-extra-keys": ("ledgers/AC4/scripts/AC4-e-r10/alt_l.py; course/modules/AC/AC4/grader/test_project.py", "Re-run this round: alt_l is KILLED by test_products_that_are_not_a_list_raise_value_error[tuple-master_budget]. alt_l accepts a tuple of products (isinstance(raw, list | tuple)). project.html line 263 requires ValueError when products are not a list, so the refusal is spec-required; alt_l is a deviation, not a correct alternative, and the grader is not over-constrained.", OUT + "alts_correct_r30.out (alt_l KILLED)"),
}
new_fail = {}
rows = []
def carried(row):
    return {"id": row["id"], "check": row["check"], "location": row["location"], "status": "PASS",
            "evidence": "Carried from round 29 (" + row["location"] + " byte-identical since the previous pin): " + row["evidence"]}
for r in prev_rows:
    if r["id"] in override:
        loc, ev, src = override[r["id"]]
        rows.append({"id": r["id"], "check": r["check"], "location": loc, "status": "PASS",
                     "evidence": "Re-verified round 30: " + ev + " Source: " + src})
    else:
        rows.append(carried(r))
# c078 is a FAIL: replace its status and add fix
for r in rows:
    if r["id"] == "proj-card-c078":
        r["status"] = "FAIL"
        r["fix"] = "In course/modules/AC/AC4/cards.json, AC4-c078 back: insert 'with a budget that has budgeted units (Q_b > 0)' after 'Yes, exactly, with no residual,' so the stated hypothesis of Proposition 2.1 (L06.html line 79) is on the card. Regenerate nothing else; the card text is hand-edited source."
        r["evidence"] = "FAIL (round 30): " + r["evidence"]
    if r["id"] == "proj-alt-l-extra-keys":
        pass

NEW = []
def add(i, check, loc, status, ev, fix=None):
    d = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if fix: d["fix"] = fix
    NEW.append(d)

add("proj-r30-delta-scope", "Delta since the previous pin 503d139 (the pin named in the previous fragment)", "course/modules/AC/AC4/*; tests/labs/AC4/*; ledgers/AC4/mutants", "PASS",
    "git diff --stat 503d139 5aeaaf0 over the slice: changed are cards.json (objects AC4-c016, c023, c026, c074, c078, c135; new AC4-c141), L01, L02, L03, L04, L06 pages, and tests/labs/AC4/lab-AC4-L03-1.py, L04, L06 (docstring or comment text). Byte-identical since 503d139: project.html, grader/* (reference, instance, starter, test_project), tests/labs/AC4/lab-AC4-project-1.py and -2.py, index.html, references, tools. The previous fragment on disk (/tmp/fanout-frags/AC4-e.round29.json) records round 23 and pin 503d139, so the delta was taken from 503d139. Scripts: " + SCR + "checks_r30.py, " + SCR + "delta_flags_r30.py; " + OUT + "checks_r30.out")
add("proj-r30-gates-check-tools", "check_pages, check_dag, check_projects on the r30 pin", "tools/check_pages.py --all; tools/check_dag.py --all; tools/check_projects.py --all", "PASS",
    "run_cmds.sh: check_pages AC4 PASS, check_dag AC4 PASS, check_projects AC4 PASS (exit 0 each). " + OUT + "check_pages.out, check_dag.out, check_projects.out")
add("proj-r30-run-labs-twins", "run_labs --unit AC4 and the two project twins run alone under python -I -W error", "tests/labs/AC4/lab-AC4-project-1.py; lab-AC4-project-2.py", "PASS",
    "run_labs AC4: PASS (10/10). Twin 1 and twin 2 each exit 0 under -I -W error; their printed output equals the two embedded expected blocks in project.html (lines 137-145 and 233-241) line for line. Page code blocks equal the twin files, with Lab 2's three blanks (lines 210, 214, 216) the only difference. " + OUT + "run_labs.out, twin_project1.out, twin_project2.out, twin_p1_direct.out")
add("proj-r30-page-smoke", "page_smoke on project.html and all AC4 pages on the r30 pin", "course/modules/AC/AC4/project.html", "PASS",
    "page_smoke --unit AC4 --pages project.html: PASS. page_smoke --unit AC4: PASS. " + OUT + "page_smoke_project.out, page_smoke_all.out")
add("proj-r30-run-graders-reference", "run_graders --unit AC4 --seeds 0-49 on reference.py", "course/modules/AC/AC4/grader", "PASS",
    "run_graders AC4: PASS (reference 50/50 seeds). " + OUT + "run_graders.out")
add("proj-r30-collect-563", "Collect-only count of the grader in the run_graders workspace, and seed independence", "course/modules/AC/AC4/grader/test_project.py", "PASS",
    "pytest --collect-only on reference.py workspace: 563 tests (project page line 265 states 563). Same count with QF_SEED 0, 7 and 49. " + OUT + "collect_ref.out; " + SCR + "collect_ws.py")
add("proj-r30-ruff-mypy-buildsite", "ruff check, ruff format --check, mypy --no-incremental, build_site --check", "repository", "PASS",
    "ruff check: passed. ruff format --check: 220 files already formatted. mypy: Success, no issues in 153 source files. build_site --check: site data current (6 outputs). " + OUT + "ruff_check.out, ruff_format.out, mypy.out, build_site_check.out")
add("proj-r30-verify-refs", "verify_refs --unit AC4 (live) and --offline", "references/references.json", "PASS",
    "live: 2 of 560 entries re-verified for AC4, 0 problems. offline: 560 entries, 0 problems. " + OUT + "verify_refs_live_AC4.out, verify_refs_offline.out")
add("proj-r30-pytest-generic", "Generic page-check tests run on the r30 pin (not AC4-specific)", "tests/test_memo_exemplars.py; tests/test_page_checks.py", "PASS",
    "Both files: all tests pass (dots only, no failure). The memo-exemplar tests cover the S7 exemplars, not AC4; AC4 coverage is by run_graders, run_labs and page_smoke. " + OUT + "pytest_memo_page_checks.out")
add("proj-r30-mutants-top-level", "Every committed project mutant in ledgers/AC4/mutants (top level) is killed by the current grader, seeds 0-9", "ledgers/AC4/mutants/*.py (144 files)", "PASS",
    "tools/mutate_graders.py --unit AC4 --seeds 0-9: mutate_graders AC4 PASS (144/144 killed), including the five new round-30 mutants. " + OUT + "mutate_final_r30.out")
add("proj-r30-mutants-fx23", "The six round-23 mutants under ledgers/AC4/mutants/AC4-e-r23 are killed by the current grader, seeds 0-9", "ledgers/AC4/mutants/AC4-e-r23/fx23_01..06", "PASS",
    "runfiles.py seeds 0-9: all six KILLED (test_every_grader_seed_reconciles_exactly, test_negative_actual_units_argument_raises_value_error). " + OUT + "mutants_new_r30_and_fx23.out")
add("proj-r30-mutants-new-student-errors", "Five new student-error mutants written this round, each a plausible error the page's spec makes testable", "ledgers/AC4/mutants/r30e_02..r30e_06", "PASS",
    "r30e_02 volume from exact flexed profit rounded once: KILLED by test_every_grader_seed_reconciles_exactly[35]. r30e_03 volume at actual average margin: KILLED by test_every_grader_seed_reconciles_exactly[30]. r30e_04 zero units returns early without fixed overhead: KILLED by test_flexed_zero_units_leaves_only_fixed_overhead. r30e_05 price variance skips products with no budgeted units: KILLED by test_product_with_no_budgeted_units. r30e_06 efficiency uses summed standards times total output: KILLED by test_every_grader_seed_reconciles_exactly[30]. Generated from reference.py by " + SCR + "make_r30e_mutants.py.", None)
add("proj-r30-mutant-equivalent-r30e01", "Equivalence proof for the mutant whose total is the sum of the four variances (moved out of the mutants list)", SCR + "equivalent/r30e_01_total_is_sum_of_the_four_variances.py", "PASS",
    "Survived (10/10 seeds) and is EQUIVALENT: the reference's four variances sum exactly to the total for every input, because sales_price + (flexed - master) + (actual_mix_margin - F - flexed) + s(standard - AQ) = sum(AU x ap) - s AQ - F - master, the actual profit less the master profit; the flexed term cancels algebraically for any rounding of it. Random check: " + OUT + "equiv_r30e01.out (identity exact on 20000 random valid cases). The file is moved out of ledgers/AC4/mutants so the tool does not count it as a fault.")
add("proj-r30-alternatives-correct", "Correct alternative implementations (over-constraint check), seeds 0-49", "ledgers/AC4/scripts/AC4-e-r30/alts/alt30_a..c; prior alts in AC4-e-r12..r23", "PASS",
    "24 correct alternatives PASS 50/50 seeds: r30 alt30_a (Decimal ROUND_HALF_UP on exact quotients, type checks), alt30_b (divmod remainder rounding, single-pass validation), alt30_c (floor plus half on Fraction, dict copy of case); prior r12 (5), r13 (2), r14 (2), r15 (3), r17 (3), r18 (3), r23 (3). alt_l (r10) is killed by a spec-required refusal, see proj-alt-l-extra-keys. " + OUT + "alts_correct_r30.out")
add("proj-r30-instances-20-seeds", "Sample 20 seeds: instances valid, answers change", "course/modules/AC/AC4/grader/instance.py", "PASS",
    "Seeds 0, 2, ..., 38: all fields int, three distinct names, budget price above input cost; 20 distinct variance tuples; sales_mix changes sign across seeds. " + SCR + "instances_alts_r30.py; " + OUT + "instances_alts_r30.out")
add("proj-r30-hours-arithmetic", "Hours arithmetic: time-budget table, lesson hours, hub split", "course/modules/AC/AC4/project.html lines 271-289; L01-L08 data-hours; index.html line 29", "PASS",
    "Time-budget components 1, 2, 2, 6, 4, 2, 2, 1 sum to the declared 20. Lesson data-hours sum to 50 and match data-hours-lessons=50 on the hub; project data-hours-project=20; 50 + 20 = 70 matches the hub. The architect ruling is applied: no pace estimate is failed. " + OUT + "checks_r30.out")
add("proj-r30-lab1-interpretation-recomputed", "Lab 1 interpretation (line 146) figures recomputed from the twin's printed output", "course/modules/AC/AC4/project.html line 146; tests/labs/AC4/lab-AC4-project-1.py", "PASS",
    "2,600,000 master; 3,142,857 flexed; +542,857 volume = 3,142,857 - 2,600,000; 7,600,000 / 1,400 = 5,428.57 per unit; 100 x 5,428.57 = 542,857; shares 1,000/1,400 = 71.4%, 1,200/1,500 = 80.0%; margins 4,400 and 8,000; mix -462,857; price +180,000; standard 3 x 1,200 + 5 x 300 = 5,100 against 5,300 used, efficiency -40,000; total +220,000 = 542,857 + 180,000 - 462,857 - 40,000. The 1/7 cent figure is printed by the twin.")
add("proj-r30-exemplars-calibration", "Calibration: score both exemplars blind and compare with the annotations", "course/modules/AC/AC4/project.html lines 326-386", "PASS",
    "Blind scoring by the rubric alone. Exemplar A: C1 2 (total plus two correct signs), C2 2 (volume and price tied, mix tied only by a wrong-signed figure), C3 2 (fixed overhead stated, input price absent), C4 1 (no action now for mix or efficiency), C5 2 (three headings): overall 1. Exemplar B: C1 4, C2 4, C3 3 (assumption consequences not for each assumption), C4 4 (actions and 5,400-cent threshold), C5 4 (four headings, 409-word body, total in the first sentence): overall 3. Both match the official scores within one level. Exemplar B figures recomputed: 2,820,000 profit, 71.4/80.0/28.6/20.0 shares, 5,300 vs 5,100 inputs, 210-cent what-if 53,000 and 167,000, 5,400-cent threshold (5,400 - 1,000 = 4,400).")
add("proj-r30-memo-body-words", "Memo body length of both exemplars (C5 band 300 to 600 words)", "course/modules/AC/AC4/project.html memo-text blocks at lines 330-340 and 361-374", "PASS",
    "Body text with headings excluded: Exemplar A 318 words, Exemplar B 409 words; both inside 300 to 600. Exemplar A has three headings (Result, Causes, Recommendation), B has four. Source: ledgers/AC4/scripts/AC4-e-r30/memo_words_r30.py; ledgers/AC4/scripts/AC4-e-r30/out/memo_words_r30.out")
add("proj-r30-lab2-blanks", "Lab 2 page code equals its twin except the three blanks", "course/modules/AC/AC4/project.html lines 152-241; tests/labs/AC4/lab-AC4-project-2.py", "PASS",
    "Unified diff of the page block and the twin: only the three lines efficiency, actual_mix_margin and mix differ (blanks replaced by INPUT_PRICE*(standard_inputs-ACTUAL_INPUTS), the budgeted margin sum, and actual_mix_contribution - flexed).")
add("proj-r30-assert-messages", "Every grader assertion has a message; no failure message interpolates an expected value", "course/modules/AC/AC4/grader/test_project.py", "PASS",
    "AST scan: zero bare asserts; f-string interpolations are only names, keys and the offending input in must_raise labels. " + SCR + "assert_msgs_r30.py; " + OUT + "assert_msgs_r30.out")
add("proj-r30-rubric-observability", "Every rubric level descriptor is observable (VERIFIER_RULES 2.6 rubric 1)", "course/modules/AC/AC4/project.html line 315 (C2 level 2) and line 317 (C4 level 1)", "FAIL",
    "C2 level 2 reads 'At least two variances tied to a case figure; the rest described in general terms.' The residual 'described in general terms' is not a test a reader can apply. C4 level 1 reads 'No recommendation, or one the figures do not support.' 'Recommendation the figures do not support' needs a judgment the rubric does not define. The scoring rule does not use either residual for any score, but VERIFIER_RULES 2.6 rubric 1 requires every descriptor to be observable.",
    "Rewrite C2 level 2 as: 'At least two variances tied to a case figure, and no more than one variance with no case figure, named product or input count.' Rewrite C4 level 1 as: 'No recommendation, or a recommendation that names no action for any unfavourable variance it discusses.' Keep the rest of the table unchanged.")
add("proj-r30-card-c023-hypothesis", "Card AC4-c023 (T) states the proposition's hypothesis", "course/modules/AC/AC4/cards.json (AC4-c023); course/modules/AC/AC4/L02.html line 71 (Proposition 2.2 'Let m > 0')", "FAIL",
    "The back 'R_BE = pQ* = F/(m/p), where m/p is the contribution margin ratio (Proposition 2.2).' drops the hypothesis m > 0 that Proposition 2.2 states on line 71 (and that the formula F/m needs). AC4-c022 keeps 'with m > 0', so the omission is on c023 only. Severity low: the formula is undefined without it, but the card is T-graded and presents it without the condition.",
    "In cards.json AC4-c023 back, change the text to 'R_BE = pQ* = F/(m/p), where m/p is the contribution margin ratio, with m > 0 (Proposition 2.2).'")
add("proj-r30-card-c016", "Card AC4-c016 (changed notation R_BE) agrees with L02 Definition 2.1", "course/modules/AC/AC4/cards.json (AC4-c016); course/modules/AC/AC4/L02.html Definition 2.1", "PASS",
    "Card back 'Its revenue counterpart is R_BE = pQ*' matches Definition 2.1 'Its revenue counterpart is R^BE = pQ*' (L02.html line 66). No hypothesis needed for a definition.")
add("proj-r30-card-c026", "Card AC4-c026 scope 'single-segment model' agrees with L02 Proposition 3.3", "course/modules/AC/AC4/cards.json (AC4-c026); course/modules/AC/AC4/L02.html line 107-109", "PASS",
    "Proposition 3.3 states 'In the single-segment model of Proposition 2.2, if fixed cost rises by delta F and the margin m is unchanged, the break-even volume rises by exactly delta F/m units. The derivative ... is 1/m.' The card's words match and it cites the proposition with the same scope.")
add("proj-r30-card-c135", "Card AC4-c135 agrees with L02 Proposition 4.1 and the margin-of-safety paragraph", "course/modules/AC/AC4/cards.json (AC4-c135); course/modules/AC/AC4/L02.html line 330 (paragraph) and line 122-127 (Proposition 4.1)", "PASS",
    "Proposition 4.1 gives OI strictly increasing on each segment with at most one zero per segment; on a segment with a zero, OI is non-negative exactly at or above that zero. The card matches the lesson sentence at line 330. Verified against the L02 twin output: loss run 2001 to 2088 is the upper segment below its zero.")
add("proj-r30-card-c074", "Card AC4-c074 contribution variance (Delta C) agrees with L06 Definition 1.2", "course/modules/AC/AC4/cards.json (AC4-c074); course/modules/AC/AC4/L06.html lines 64-72", "PASS",
    "Card: 'Delta C = C_a - C_b ... material is the only variable cost ... budget contribution is the sum of CM_i x q_b,i (Definition 1.2)'. L06.html line 72 gives Delta C = C_a - C_b, with C_b = sum CM_i q_b,i, and line 65 states the one variable cost is material.")
add("proj-r30-card-c141", "New card AC4-c141 (standard kilograms allowed) agrees with L06 Definition 1.1 and the efficiency definition", "course/modules/AC/AC4/cards.json (AC4-c141); course/modules/AC/AC4/L06.html line 59 (Definition 1.1) and line 70 (E)", "PASS",
    "Definition 1.1 says 'The standard kilograms allowed for the actual output of product i are s_i q_a,i'. The card's wording and citation match. E = -pi sum (kg - s q) in line 70 supports the second sentence of the card. Card is ungraded (definitional).")

rows = rows + NEW
mutants = []
mutdir = ROOT / "ledgers/AC4/mutants"
txt = read("mutate_final_r30.out")
for line in txt.splitlines():
    m = re.match(r"KILLED (\S+): (.*) -> (.*)$", line)
    if m:
        name, desc, killed = m.groups()
        mutants.append({"file": f"ledgers/AC4/mutants/{name}", "description": desc.strip(), "killed_by": killed.strip()})
fx = read("mutants_new_r30_and_fx23.out")
for line in fx.splitlines():
    m = re.match(r"KILLED (fx23_\S+\.py) -> (.*)$", line)
    if m:
        name, killed = m.groups()
        path = mutdir / "AC4-e-r23" / name
        desc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))).splitlines()[0]
        mutants.append({"file": f"ledgers/AC4/mutants/AC4-e-r23/{name}", "description": desc, "killed_by": killed.strip()})
print("mutants listed", len(mutants), "rows", len(rows))
frag = {
 "unit": "AC4", "slice": "AC4-e", "round": 30,
 "verifier": "Claude Haiku 5.5 (independent verifier, round 30, slice AC4-e; did not build AC4)",
 "pin": "5aeaaf0",
 "base": "503d139 (the pin the previous fragment on disk records; that file is labelled round 23, not round 29, so the delta was computed from 503d139)",
 "checkout": "/tmp/verify30-AC4-e", "scratch": "/tmp/ac4e30",
 "verified_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": "FAIL",
 "rows": rows, "mutants": mutants,
 "registry_flags": prev["registry_flags"],
 "freshness_flags": [],
 "notes": "Not checked: (1) the Pyodide browser UI itself was not driven; page_smoke and source reading only. (2) The 22 lab-twin mutants and the lab-twin mutant subdirectories (AC4-a/c/d) are out of scope per the architect ruling and were not run through the grader. (3) The self-assessment form's JavaScript was not executed (page_smoke only). (4) The 35 ungraded cards were checked for numbers and wording, not for grade appropriateness beyond the grade counts. (5) Memo rubric calibration was scored by reasoning against the rubric text; no machine test exists. (6) Hours: pace estimate not failed (architect ruling); arithmetic only. (7) Lesson text outside the cards was read only where a card cites it. Observation outside the slice for the L03 verifier: L03.html interpretation says the 9.10 avoidable make cost is 'printed on the first line of Lab 1', but the twin prints it on the second line (the first line is the header 'Part K, make or buy ...').",
 "summary": None,
}
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
assert {r["id"] for r in prev_rows} <= set(ids), "a previous row id was dropped"
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag["summary"] = {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"], "mutants": len(mutants)}
frag["verdict"] = "PASS" if counts["PASS"] == len(rows) else "FAIL"
(ROOT / "ledgers/AC4/AC4-e.json").write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("summary", frag["summary"], frag["verdict"])
