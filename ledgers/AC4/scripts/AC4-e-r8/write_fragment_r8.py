"""Write the round-8 AC4-e fragment (ledgers/AC4/AC4-e.json) from the outputs of this round."""
import json
import pathlib
import re
import sys

CHK = pathlib.Path("/tmp/verify8-AC4-e")
OUT_DIR = CHK / "ledgers" / "AC4"
S = "ledgers/AC4/scripts/AC4-e-r8/"
prev = json.loads(pathlib.Path("/tmp/fanout-frags/AC4-e.round7.json").read_text(encoding="utf-8"))
mut_lines = pathlib.Path("/tmp/ac4-v/e8/mutate40.out").read_text(encoding="utf-8").splitlines()

mutants = []
for line in mut_lines:
    m = re.match(r"(KILLED|SURVIVED) (m\d\d)_\S+\.py: (.*?) -> (.*)$", line)
    if not m:
        continue
    status, mid, desc, killed = m.groups()
    fname = [p.name for p in (CHK / "ledgers/AC4/mutants").glob(mid + "_*.py")][0]
    mutants.append({
        "id": mid,
        "file": f"ledgers/AC4/mutants/{fname}",
        "description": desc.split(" Reference solution")[0].strip(),
        "killed_by": None if status == "SURVIVED" else killed.strip(),
    })

CARRY = "Carried from round 7 (course/modules/AC/AC4/project.html lines outside the round-8 hunks at 146, 260-265, 324, 346, 366, 373, 398-399 byte-identical since de53f7e): "
CARRY_TEST = "Carried from round 7 (course/modules/AC/AC4/grader/test_project.py lines outside the round-8 hunks at 584-690 byte-identical since de53f7e): "
RUN = "Re-run round 8 (" + S

def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        r["fix"] = fix
    return r

R = []
R.append(row("proj-autograder-reference", "Reference solution passes the whole suite on the learner-facing grader files",
    "course/modules/AC/AC4/grader/reference.py; course/modules/AC/AC4/grader/test_project.py",
    "PASS", RUN + "collect.py grader/reference.py 0): collect-only 296 tests; seed 0 '296 passed in 0.09s'. tools/run_graders.py --unit AC4 --seeds 0-49: 'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.2 s)'. Output /tmp/ac4-v/e8/run_graders.out."))
R.append(row("proj-collect-count", "The page's test count equals the real collect-only count",
    "course/modules/AC/AC4/project.html line 265 (Grading mode); course/modules/AC/AC4/grader/test_project.py",
    "PASS", RUN + "collect.py): 'test_project.py: 296'. project.html line 265 reads 'collects <strong>296 checks</strong>'. Equal. (Round 7 read 274; the new boolean and product-field tests account for the increase.)"))
R.append(row("proj-autograder-alternatives", "Alternative correct implementations pass the suite (over-constraint check)",
    "course/modules/AC/AC4/grader/test_project.py; ledgers/AC4/scripts/AC4-e-r8/alt_h.py, alt_i.py, alt_j.py (new), alternatives_r4.py -> alt_a/b/c, alt_e/f/g",
    "PASS", RUN + "run_alts.py): nine genuinely different correct implementations pass 296 tests on seeds 0-9 and 25. alt_h: operator.index plus Decimal ROUND_HALF_UP; alt_i: class-based validation with exact Fraction shares; alt_j: products validated before case fields, divmod rounding, no bool allowed. alt_a/b/c (alternatives_r4.py) and alt_e/f/g (fraction, generic validator, class-free) also pass. Log: /tmp/ac4-v/e8/."))
R.append(row("proj-instances", "instance.py is deterministic and its instances differ across seeds",
    "course/modules/AC/AC4/grader/instance.py", "PASS",
    "tools/run_graders.py --unit AC4 --seeds 0-49 reports the instance checks as PASS (run_graders AC4: PASS). The only instance.py change in the delta is a docstring (lines 8-10); the generator body is unchanged."))
R.append(row("proj-alt-instance-coverage", "Starter fails the suite; instances cover the seed range",
    "course/modules/AC/AC4/grader/instance.py; course/modules/AC/AC4/grader/starter.py", "PASS",
    "run_graders.py --unit AC4 --seeds 0-49: starter fails the suite (not reported as a problem), reference 50/50 (/tmp/ac4-v/e8/run_graders.out)."))
for mid, label in [("proj-mutants-m01-m06", "m01-m06"), ("proj-mutant-m07-empty-name", "m07"),
                   ("proj-mutants-m08-m11", "m08-m11"), ("proj-mutant-m12-duplicate-names", "m12"),
                   ("proj-mutants-m13-m20", "m13-m20"), ("proj-mutants-m15-m19", "m15-m19"),
                   ("proj-mutants-m21-m24", "m21-m24"), ("proj-mutants-m21-m24-equivalence", "m21-m24 (not equivalent: each killed)"),
                   ("proj-mutants-m25-m29", "m25-m29"), ("proj-mutants-r6-new", "m30-m34"),
                   ("proj-mutant-descriptions", "docstrings of m01-m40")]:
    R.append(row(mid, f"Mutants {label} are killed by the autograder on seeds 0-9",
        "ledgers/AC4/mutants/ (" + label + ")", "PASS",
        RUN + "mutate_graders.py --unit AC4 --seeds 0-9 -> /tmp/ac4-v/e8/mutate40.out: 40/40 KILLED, PASS. Each listed mutant is killed (killed_by in the mutants list)."))
R.append(row("proj-spec-empty-name-claim", "Constraint: a product name that is empty is refused",
    "course/modules/AC/AC4/project.html line 263 (Constraints); course/modules/AC/AC4/grader/test_project.py test_empty_product_name_raises_value_error (line 616)",
    "PASS", RUN + "mutate40.out): m07_empty_name_accepted KILLED; collect shows the empty-name test in the 296."))
R.append(row("proj-spec-fresh-objects-claim", "master_budget returns a fresh object on each call",
    "course/modules/AC/AC4/project.html line 263; course/modules/AC/AC4/grader/test_project.py line 243 (test_master_returns_fresh_objects)",
    "PASS", RUN + "mutate40.out): m27_master_returns_cached_object KILLED; test_master_returns_fresh_objects in the 296 passing on the reference."))
R.append(row("proj-spec-clarity-and-errors", "Constraints line lists every ValueError the tests enforce, including the whole-number clause for every value (float and bool)",
    "course/modules/AC/AC4/project.html line 263 (Constraints); course/modules/AC/AC4/grader/test_project.py lines 586-591 (boolean case fields), 650-684 (product fields and actual-units argument, incl. test_product_field_boolean_raises_value_error and test_boolean_actual_units_argument_raises_value_error)",
    "PASS", "The Constraints line (project.html line 263) is unchanged; the tests were extended to meet it. Round-7 survivors now killed: m35_bool_accepted_in_product_fields KILLED by test_product_field_boolean_raises_value_error[budget_units-master_budget] (seed 0); m36_flexible_accepts_bool_units KILLED by test_boolean_actual_units_argument_raises_value_error (seed 0). Boolean refusal is tested for input_price_cents, fixed_overhead_cents, actual_inputs_used (case), all five product whole-number fields, and the flexible_budget actual-unit argument, across FUNCTIONS. Negative, missing, zero-budget, duplicate and empty-name clauses also covered by tests (lines 563-739). Source: " + RUN + "mutate40.out)."))
R.append(row("proj-messages-bare-asserts", "Every assert in the grader carries a message",
    "course/modules/AC/AC4/grader/test_project.py", "PASS",
    "ledgers/AC4/scripts/AC4-e-r8/scan_r8.py (output /tmp/ac4-v/e8/scan.out): 'asserts without message: []' over every ast.Assert in test_project.py."))
R.append(row("proj-messages-no-leak", "Assertion and must_raise messages do not reveal reference values",
    "course/modules/AC/AC4/grader/test_project.py (new messages at lines 591, 671, 684)", "PASS",
    "Read the three new messages: '{name}: {field} given as a boolean, where a whole number is required', '{name}: a product's {field} given as a boolean', 'flexible_budget: a boolean given as the actual unit count'. None states a value or result."))
R.append(row("proj-rubric-exhaustive", "The memo rubric has five criteria with four observable levels each",
    "course/modules/AC/AC4/project.html lines 314-318 (rubric rows)", "PASS",
    CARRY + "lines 314-318 are outside all round-8 hunks (146, 260-265, 324, 346, 366, 373, 398-399)."))
R.append(row("proj-rubric-scoring-rule", "Scoring rule for the memo rubric",
    "course/modules/AC/AC4/project.html line 308 (Scoring rule)", "PASS", CARRY + "line 308 unchanged."))
R.append(row("proj-rubric-C4-observation", "C4 observation about exemplar B's recommendation threshold",
    "course/modules/AC/AC4/project.html lines 306, 316, 373", "PASS",
    "Re-run round 8 on line 373 (changed hunk): the threshold 5,400 cents makes Deluxe's budgeted margin 5,400 - 1,000 = 4,400, equal to Standard's 5,000 - 600 = 4,400; below it Deluxe earns less, so the shift toward Standard adds margin. Lines 306 and 316 are outside the round-8 hunks and unchanged since de53f7e."))
R.append(row("proj-calib-A-scores", "Exemplar A official scores and the level it reports",
    "course/modules/AC/AC4/project.html line 326 (data-scores), exemplar A memo lines 330-340", "PASS", CARRY + "lines 326 and 330-340 unchanged."))
R.append(row("proj-calib-A-annotation", "Exemplar A annotation matches the memo text",
    "course/modules/AC/AC4/project.html lines 343-351", "PASS",
    "Re-run round 8 on the changed C2 line 346: 'the memo says the plant earned more on the units it sold more of' matches memo text (line 336). Standard's margin 4,400 < Deluxe 8,000 (lab per-unit margins), so the shift is unfavourable; the C1 'mix sign is also wrong' matches the memo's '+462,857' against the lab's -462,857 (project.html line 143-146 lab output step 6)."))
R.append(row("proj-calib-B-scores", "Exemplar B official scores",
    "course/modules/AC/AC4/project.html line 357 (data-scores), exemplar B Result line ~363", "PASS", CARRY + "lines 357 and 363 unchanged."))
R.append(row("proj-calib-B-annotation", "Exemplar B annotation matches the memo text",
    "course/modules/AC/AC4/project.html lines 377-382", "PASS", CARRY + "lines 377-382 unchanged; the 300-600 word and threshold claims re-read (see proj-exemplar-B-threshold and proj-memo-structure-length)."))
R.append(row("proj-memo-structure-length", "Exemplar memo bodies fall in the rubric's length band and carry the four headings",
    "course/modules/AC/AC4/project.html exemplar A memo-text (line 330 onward) and exemplar B memo-text (lines 361-373)", "PASS",
    "scan_r8.py (scan.out): exemplar A memo-text 321 words, exemplar B memo-text 412 words (whitespace split after stripping tags); both inside the 300-600 band of C5. Headings: Result, Causes, Recommendation (A); Result, Causes, Assumptions, Recommendation (B)."))
R.append(row("proj-exemplar-B-consequences", "Exemplar B states the input price consequence",
    "course/modules/AC/AC4/project.html line 370 (Assumptions)", "PASS",
    CARRY + "line 370 unchanged. Re-derived: 210 - 200 = 10 cents x 5,300 input units = 53,000; 220,000 - 53,000 = 167,000."))
R.append(row("proj-exemplar-B-threshold", "Exemplar B reversing threshold is correct",
    "course/modules/AC/AC4/project.html line 373", "PASS",
    "Re-read the changed sentence: margin at 5,400 = 5,400 - 5 x 200 = 4,400 = Standard's 5,000 - 3 x 200; mix variance zero at equality, favourable below (Deluxe margin lower than Standard). Recomputed with the lab's price and input costs (lab-AC4-project-1 output, step 6 = -462,857)."))
R.append(row("proj-reading-list-sentence", "Reading-list sentence and registry keys",
    "course/modules/AC/AC4/project.html line 267 (Reading list dd; the dt is line 266)", "PASS",
    CARRY + "the dd is unchanged (its line number is 267 in round 8, not 266)."))
R.append(row("proj-hours", "Declared project hours match the hub split and lesson hours",
    "course/modules/AC/AC4/project.html lines 277-285; course/modules/AC/AC4/index.html line 29 (data-hours)", "PASS",
    CARRY + "lines 277-285 unchanged; index.html not in the delta (diff stat)."))
R.append(row("proj-ladder-lede", "Ladder lede and hub links",
    "course/modules/AC/AC4/project.html line 42; course/modules/AC/AC4/index.html lines 70 and 155", "PASS",
    CARRY + "line 42 unchanged; index.html not in the delta."))
R.append(row("proj-simulated-and-data", "Lab 1 is labelled SIMULATED and reads no real data",
    "course/modules/AC/AC4/project.html lines 53-56 and 252 (Inputs); tests/labs/AC4/lab-AC4-project-1.py", "PASS",
    CARRY + "lines 53-56, 252 and the twin unchanged; run_labs AC4: PASS (10/10)."))
R.append(row("proj-equal-margin-branch", "Two-product shift test covers the equal-margin branch",
    "course/modules/AC/AC4/grader/test_project.py lines 463-480", "PASS", CARRY_TEST + "lines 463-480 unchanged; suite passes on the reference (296)."))
R.append(row("proj-grader-equal-margin-comment", "Grader comment on the equal-margin case is accurate",
    "course/modules/AC/AC4/grader/test_project.py lines 472-474", "PASS", CARRY_TEST + "lines 472-474 unchanged."))
R.append(row("proj-rubric-C2-terms", "C2 rubric terms match the scoring rule",
    "course/modules/AC/AC4/project.html line 308 (scoring rule) and line 315 (rubric row C2)", "PASS", CARRY + "lines 308 and 315 unchanged."))
R.append(row("proj-exemplar-overall-level", "Overall levels 1 and 3 match the data-level attributes",
    "course/modules/AC/AC4/project.html line 324 (intro) and article data-level at lines 327 and 357", "PASS",
    "Re-read the intro sentence 'overall levels 1 and 3': exemplar A data-level=1 (line 326-327), exemplar B data-level=3 (line 357). Match. The intro's universal clause is a separate row (proj-exemplar-intro-universal-claim)."))
R.append(row("proj-citations-reading", "Reading-list citations resolve in the registry",
    "course/modules/AC/AC4/project.html reading list; references/references.json (datar2020horngrens, kaplan...)", "PASS",
    CARRY + "references/ byte-identical across the delta (git diff --quiet). Fresh: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (/tmp/ac4-v/e8/verify_refs_offline.out). Live run not repeated (carried; no references change)."))
R.append(row("proj-mutants-r7-new", "Round-7 mutants m35-m37 are killed (boolean acceptance, boolean actual units, a warning)",
    "ledgers/AC4/mutants/m35_bool_accepted_in_product_fields.py; m36_flexible_accepts_bool_units.py; m37_master_warns.py", "PASS",
    RUN + "mutate40.out): m35 KILLED, m36 KILLED, m37 KILLED (warning becomes an error under -W error)."))
R.append(row("proj-autograder-rerun-mutants-m01-m37", "Full mutant set killed on seeds 0-9",
    "ledgers/AC4/mutants (m01-m40)", "PASS", RUN + "mutate40.out): 'mutate_graders AC4: PASS (40/40 killed)'."))
R.append(row("proj-mutants-r8-new", "Round-8 student-error mutants m38-m40 are killed",
    "ledgers/AC4/mutants/m38_flexed_per_unit_rounded_first.py; m39_bool_actual_inputs_refused_only_by_master.py; m40_zero_budget_units_refused_only_by_master.py", "PASS",
    "Generated from the reference by exact replacement (ledgers/AC4/scripts/AC4-e-r8/make_mutants_r8.py). m38 KILLED by test_every_grader_seed_reconciles_exactly[26]; m39 KILLED by test_boolean_input_raises_value_error[actual_inputs_used-flexible_budget]; m40 KILLED by test_zero_budgeted_units_raise_value_error[flexible_budget]. (Two earlier drafts failed to import: fixed by keeping the module docstring first; those are not in the list.)"))
R.append(row("proj-spec-coverage-claims", "Project line 265 claims the suite covers each named ValueError, purity and silence",
    "course/modules/AC/AC4/project.html line 265; course/modules/AC/AC4/grader/test_project.py", "PASS",
    "Each named ValueError now has a test covering every field it names (see proj-spec-clarity-and-errors). Purity (test_functions_do_not_change_their_arguments, m34 KILLED) and silence (test_functions_are_silent, m28 and m37 KILLED) are enforced. Sample of coverage claims re-run in the 296."))
R.append(row("proj-stretch-two-inputs", "Stretch 'Two inputs' bullet states a true identity with its condition",
    "course/modules/AC/AC4/project.html line 399 (Rung 4 Stretch, 'Two inputs')", "PASS",
    "Recomputed: " + S + "stretch_r8.py (output /tmp/ac4-v/e8/stretch.out): 72 two-input cases with every actual input price equal to standard and fixed overhead at budget: 0 mismatches for sales price + volume + mix + two efficiency variances = total. Gap identity over 765 two-input cases with fixed overhead at budget: total minus those five = sum of input price variances (s_k - a_k) x actual input units, 0 mismatches. Round-7 witness: total -2000, five figures 0, input 1 price variance -2000 (the page's 'state the input price variances that close the gap' covers it)."))
R.append(row("proj-stretch-spending", "Stretch 'A spending variance' bullet's exactness claim",
    "course/modules/AC/AC4/project.html line 398 (Rung 4 Stretch, 'A spending variance')", "PASS",
    "Recomputed in " + S + "stretch_r8.py (stretch.out): 1481 one-input random cases, with the actual input price and the fixed overhead both free: price + volume + mix + efficiency + input price variance (s - a) x AQ + fixed overhead variance (budget - actual) = total exactly, 0 mismatches, whether or not a = s. The page now says 'whether or not the actual input price is the standard price', which is what the identity supports."))
R.append(row("proj-stretch-list-intact", "Rung 4 stretch list has its three bullets in order",
    "course/modules/AC/AC4/project.html lines 396-401", "PASS",
    "Read lines 397-401: 'A spending variance', 'Two inputs', 'A rolling forecast' (three li)."))
R.append(row("proj-lab-1", "Lab 1 runs, reproduces its printed steps and holds its claims",
    "course/modules/AC/AC4/project.html lines 53-147; tests/labs/AC4/lab-AC4-project-1.py", "PASS",
    "python -I -W error lab-AC4-project-1.py: exit 0; steps 1-8 print 2600000, 3142857, 180000, 542857, -40000, -462857, '1/7', 220000, True. Recomputed by hand: master 8,600,000 - 1,000,000 - 5,000,000 = 2,600,000; flexed exact 3,142,857 1/7; sums 180,000 + 542,857 - 462,857 - 40,000 = 220,000."))
R.append(row("proj-lab-1-interpretation", "Lab 1 interpretation sentences match the printed output and the case",
    "course/modules/AC/AC4/project.html line 146 (interpretation)", "PASS",
    "Re-read the changed sentence 'rounded to the whole cent by the step 2 rule' against step 2 (3142857) and step 6 (1/7 cent): the whole-cent rule rounds revenue and variable cost, so the profit is whole. Other numbers: 5,300 vs 5,100 input units, 4,400 vs 8,000 margins, 71.4% -> 80.0% (1000/1400, 1200/1500) re-derived."))
R.append(row("proj-lab-2", "Lab 2 (blanked lines) runs and reproduces Lab 1",
    "course/modules/AC/AC4/project.html lines 149-243; tests/labs/AC4/lab-AC4-project-2.py", "PASS",
    "python -I -W error lab-AC4-project-2.py: exit 0; the same eight steps and values as Lab 1. run_labs AC4: PASS (10/10)."))
R.append(row("proj-purity-order-dependence", "Functions do not change arguments or depend on call order",
    "course/modules/AC/AC4/grader/test_project.py (test_functions_do_not_change_their_arguments, test_functions_do_not_reorder_their_products, test_results_do_not_depend_on_call_order)", "PASS",
    CARRY_TEST + "lines 749-790 unchanged; killed m34 and m27 (see mutant rows); suite 296 passes on the reference."))
R.append(row("proj-card-c020", "AC4-c020 (lesson L02) matches its lesson",
    "course/modules/AC/AC4/cards.json lines 134-138 (AC4-c020); course/modules/AC/AC4/L02.html", "PASS",
    "Carried from round 7 (course/modules/AC/AC4/cards.json lines 134-138 and course/modules/AC/AC4/L02.html byte-identical since de53f7e): card text unchanged; L02 not in the delta."))
R.append(row("proj-card-c078", "AC4-c078 (lesson L06, Proposition 2.1) matches its lesson",
    "course/modules/AC/AC4/cards.json lines 553-557 (AC4-c078); course/modules/AC/AC4/L06.html Proposition 2.1", "PASS",
    "Carried from round 7 (cards.json lines 553-557 byte-identical; L06 Proposition 2.1 text not in the round-8 L06 hunks): card says 'Yes, exactly, with no residual ... provided the actual material price equals the standard price'; the L06 proposition carries the same proviso."))
R.append(row("proj-cards-structure", "cards.json structure: unique ids, lesson exists, required fields, grade set",
    "course/modules/AC/AC4/cards.json (119 cards)", "PASS",
    "scan_r8.py (scan.out): 119 cards, 'ids sequential: True'; every card has id, lesson, front, back; grade present on 88 cards (T 45, C 43), absent on 31; check_pages --all AC4: PASS. c091 edited (grade T, no basis field, like the other T cards)."))
R.append(row("proj-cards-duplicates", "No duplicate card fronts, backs or ids",
    "course/modules/AC/AC4/cards.json", "PASS", "scan_r8.py (scan.out): 'duplicate fronts: []' (lower-cased) and 'duplicate backs: []'; ids unique (sequential check)."))
R.append(row("proj-cards-sample", "Sampled cards match their lessons",
    "course/modules/AC/AC4/cards.json (c010, c020, c030, c040, c050, c060, c070, c080 ...)", "PASS",
    "Carried from round 7 (course/modules/AC/AC4/cards.json except the AC4-c091 hunk at line 641, byte-identical since de53f7e): the sampled card texts are unchanged; their lessons L01-L04, L07, L08 are not in the delta. Sampled L05/L06 cards are re-read under proj-cards-changed-lessons."))
R.append(row("proj-cards-targeted", "Cards that quote lesson numbers match the lesson output",
    "course/modules/AC/AC4/cards.json (c062, c063, c064, c066, c067, c075, c076)", "PASS",
    "Re-run round 8: lab-AC4-L05-1 prints static_variance 140000, volume_and_mix 265000, flexible_variance -125000, flexed fixed 500000 (cards c062, c063, c066, c067, c068); lab-AC4-L06-1 prints efficiency -75000, sales price -40000, volume 249000, mix 16000, sum 150000, operating profit 140000 (c076, c080, c081); c075 recomputed 1500 x (-100) + 1900 x 100 = +40,000 with V = 0."))
R.append(row("proj-cards-number-format", "Card numbers use the lesson's number format",
    "course/modules/AC/AC4/cards.json (c101, c102, c109)", "PASS", "Carried from round 7 (course/modules/AC/AC4/cards.json, AC4-c101, c102, c109 byte-identical since de53f7e; the only card hunk is c091 at line 641)."))
R.append(row("proj-cards-changed-lessons", "Cards citing lessons changed in this delta (L05, L06) still match them",
    "course/modules/AC/AC4/cards.json cards from L05 (AC4-c059..c068) and L06 (AC4-c069..c081, c110..c112); L05.html relevant-range bullet; L06.html meta, why-it-matters, interpretation, P3", "PASS",
    "Every L05 and L06 card read against the changed text (L05 relevant range, L06 meta/why/interpretation/P3). No card quotes a changed sentence; the numbers they quote are the lab outputs re-run in round 8 (see proj-cards-targeted). Cards from L01/L02 carried (lessons not in the delta)."))
R.append(row("proj-card-c091", "AC4-c091 (new text, lesson L07, Theorem 7.3 part 1) matches its lesson",
    "course/modules/AC/AC4/cards.json line 641 (AC4-c091); course/modules/AC/AC4/L07.html Theorem 7.3 part 1 (line 114) and Lemma 7.2 proof (line 98)", "PASS",
    "Read the card: 'Exactly the prices t in [t_min, t_max]. On that interval both gains are nonnegative, and outside it at least one gain is negative (Theorem 7.3, part 1).' L07 line 114 states part 1 'the price range that leaves both divisions no worse off is [t_min, t_max]'; line 98 gives Delta_S >= 0 iff t >= t_min and Delta_B >= 0 iff t <= t_max, so outside the interval one gain is negative. Grade T matches the lesson's T claim."))
R.append(row("proj-banned-phrases", "Banned phrases and process words absent from the project page and cards",
    "course/modules/AC/AC4/project.html; course/modules/AC/AC4/cards.json", "PASS",
    "ledgers/AC4/scripts/AC4-e-r8/scan_r8.py (scan.out): 'banned hits: []' over the page text and all 119 cards (roughly half, about 6%, historically, ellipsis, builder, verifier, round, REQUESTS, unit report)."))
R.append(row("proj-page-smoke", "page_smoke passes for the project page in Chromium, light and dark, at 360 px",
    "course/modules/AC/AC4/project.html", "PASS",
    "tools/page_smoke.py --unit AC4 --pages project.html: 'page_smoke AC4: PASS' (/tmp/ac4-v/e8/page_smoke.out, rc 0)."))
R.append(row("proj-check-projects", "check_projects --all passes for AC4",
    "course/modules/AC/AC4/project.html", "PASS", "tools/check_projects.py --all: 'check_projects AC4: PASS'."))
R.append(row("proj-check-pages", "check_pages --all passes for AC4",
    "course/modules/AC/AC4/*.html and cards.json", "PASS", "tools/check_pages.py --all: 'check_pages AC4: PASS'."))
R.append(row("proj-check-dag", "check_dag --all passes for AC4",
    "course/modules/AC/AC4", "PASS", "tools/check_dag.py --all: 'check_dag AC4: PASS'."))
R.append(row("proj-ruff-mypy", "ruff and mypy (repo-wide strict) pass for the grader, labs and pages",
    "course/modules/AC/AC4/grader; tests/labs/AC4; repository mypy configuration", "PASS",
    "ruff check . -> 'All checks passed!'; ruff format --check course/modules/AC/AC4 tests/labs/AC4 -> 14 files already formatted; mypy --no-incremental (repo root) -> 'Success: no issues found in 153 source files'. Note: mypy run on the grader directory alone reports 4 import-not-found / unused-ignore errors; that is an artifact of checking the folder without the repo configuration and is not the gate."))
R.append(row("proj-run-labs-ac4", "run_labs passes for every AC4 lab (10 labs)",
    "tests/labs/AC4", "PASS", "tools/run_labs.py --unit AC4: 'run_labs AC4: PASS (10/10)'."))
R.append(row("proj-inputs-every-number-int", "Every number the engine returns is an int; the inputs are whole cents and units",
    "course/modules/AC/AC4/project.html lines 252 and 260 (Inputs and Conventions)", "PASS",
    "Re-read line 260 (changed): 'every number it returns is an int'. test_master_budget_values_are_integers, test_flexed_budget_returns_integer_cents, test_variances_are_whole_cents pass on the reference; flexible/variance reference returns int via _nearest_cent and integer arithmetic."))
R.append(row("proj-exemplar-intro-universal-claim", "Exemplar intro: 'any other figure they state follows from those figures' is true of both memos",
    "course/modules/AC/AC4/project.html line 324 (exemplars intro); exemplar B Assumptions line 370 ('If the actual input price were 210 cents ...')", "FAIL",
    "The new sentence says both memos use the case figures and that 'any other figure they state follows from those figures'. Exemplar B states a what-if input price of 210 cents (line 370) and the 53,000 and 167,000 that follow from it. 210 cents is not derived from the case (the case's input price is 200 cents, project.html line 252), so the universal clause is false for exemplar B. Exemplar A's figures are all case figures (1,500, 1,400, 5,000, 9,000, 220,000, 542,857, 180,000, 462,857), so only exemplar B falls outside.",
    "Change the sentence to: 'Both use the case figures that Lab 1 computes; every other figure they state is either derived from those figures or labelled as a what-if.' (or drop the universal clause)."))
R.append(row("proj-stretch-two-inputs-scope", "Stretch 'Two inputs' does not assume a fixed-overhead variance",
    "course/modules/AC/AC4/project.html line 399", "PASS",
    "The engine holds fixed overhead at budget (project.html line 260: 'holds the input price and the fixed overhead at budget'; the case has one fixed overhead field used for both periods, so F_actual = F_budget by construction). Under that convention the two-input identity holds with 0 mismatches (stretch_r8.py, F_a = F_b cases)."))

R.append(row("proj-grader-comments", "Grader comments (PRISTINE comment and the rest) are accurate",
    "course/modules/AC/AC4/grader/test_project.py lines 43-44 (PRISTINE comment)", "PASS",
    "Carried from round 7 (course/modules/AC/AC4/grader/test_project.py lines 43-44 outside the round-8 hunks at 584-690, byte-identical since de53f7e); the suite runs on the reference and the starter fails it (run_graders AC4: PASS)."))
assert len(prev["rows"]) == 67
ids_prev = [r["id"] for r in prev["rows"]]
ids_now = {r["id"] for r in R}
missing = [i for i in ids_prev if i not in ids_now]
print("missing prev ids:", missing)
frag = {
    "unit": "AC4",
    "slice": "AC4-e",
    "round": 8,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 8, slice AC4-e; did not build AC4)",
    "pin": "2c8162b",
    "base": "de53f7e (round-7 pin; /tmp/fanout-frags/AC4-e.round7.json used as context; carried rows state the files byte-identical since de53f7e)",
    "previous_ledger": "/tmp/fanout-frags/AC4-e.round7.json",
    "checkout": "/tmp/verify8-AC4-e",
    "scratch": "/tmp/ac4-v/e8",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta de53f7e..2c8162b for this slice: project.html (hunks at lines 146, 260, 265, 324, 346, 365-366, 373, 398-399; the Constraints line 263 is unchanged); cards.json (c091 replaced, line ~643); grader/test_project.py (boolean and product-field tests, line 584 onward); grader/instance.py (docstring only); L05.html and L06.html (cited by cards). reference.py, starter.py, the labs and references/ are unchanged.",
        "Round-7 FAILs: proj-spec-clarity-and-errors, proj-spec-coverage-claims, proj-mutants-r7-new, proj-autograder-rerun-mutants-m01-m37 now PASS (m35, m36 killed; 40/40 killed). proj-stretch-two-inputs and proj-stretch-spending now PASS (recomputed, 0 mismatches). New FAIL this round: the exemplar intro universal clause (line 324) is false for exemplar B's 210-cent what-if.",
        "Mutants: 40 in ledgers/AC4/mutants (m01-m37 copied from the round-7 checkout, not edited; m38-m40 new). mutate_graders.py --unit AC4 --seeds 0-9: 40/40 killed.",
        "Alternatives: nine correct implementations pass 296 on seeds 0-9 and 25 (alt_a/b/c, alt_e/f/g from round 7; alt_h, alt_i, alt_j new this round).",
        "Not checked in full: lesson pages L01-L08 line by line (outside this slice; only the sentences the cards cite and the changed L05/L06 sentences were re-read); the memo rubric beyond the cited lines; the live verify_refs run (carried, references unchanged); Pyodide beyond page_smoke's Chromium run; the registry entries for the reading list (carried); the L05 relevant-range wording beyond the sentence changed (it is not cited by any card); the L06 interpretation and P3 changes are read but their full proof is another slice's subject.",
        "Not applied: no fixes made (the verifier does not fix). Fix for the one FAIL is on the row.",
        "Locator note: the round-7 locator 'project.html line 266 (Reading list dd)' is now line 267 for the dd (266 is the dt); content unchanged.",
    ],
    "summary": {},
}
n = len(R)
statuses = [r["status"] for r in R]
frag["summary"] = {
    "rows": n,
    "pass": statuses.count("PASS"),
    "fail": statuses.count("FAIL"),
    "non_pass_ids": [r["id"] for r in R if r["status"] != "PASS"],
    "mutants": len(mutants),
    "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
}
out = OUT_DIR / "AC4-e.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False), encoding="utf-8")
print("wrote", out, frag["summary"])
