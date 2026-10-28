import json, re, pathlib
ROOT = pathlib.Path("/tmp/verify13-AC4-e")
OUT = ROOT / "ledgers/AC4/scripts/AC4-e-r13/out"
prev = {r["id"]: r for r in json.load(open("/tmp/fanout-frags/AC4-e.round12.json"))["rows"]}
mut_lines = [l for l in (OUT / "mutate_graders_r13.out").read_text().splitlines() if l.startswith("KILLED ")]
mutants = []
for l in mut_lines:
    body = l[len("KILLED "):]
    fname, rest = body.split(": ", 1)
    desc, killed = rest.split(" -> ", 1)
    mid = fname[:-3]
    subdir = "ledgers/AC4/mutants/" + fname
    mutants.append({"id": mid, "file": subdir, "description": desc, "killed_by": killed.strip()})
MUT_NOTE = ("Round 13 re-run: tools/mutate_graders.py --unit AC4 --seeds 0-9 -> 93/93 KILLED (out/mutate_graders_r13.out); "
            "ledgers/AC4/scripts/AC4-e-r12/run_mutants.py on seeds 0, 1, 25 -> 93 KILLED, 0 SURVIVED (out/run_mutants_seeds_0_1_25.out)")
FN = "course/modules/AC/AC4/grader/test_project.py"
def carry(old_id, subject, files):
    return {"id": old_id, "check": prev[old_id]["check"], "location": prev[old_id]["location"], "status": "PASS",
            "evidence": f"Carried from round 12 ({subject} byte-identical since the previous pin): " + prev[old_id]["evidence"]}
rows = []
def add(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)
def fresh(old_id, location, evidence, status="PASS", fix=None):
    add(old_id, prev[old_id]["check"], location, status, evidence, fix)

PROJ_UNCHANGED = "course/modules/AC/AC4/project.html lines 53-259 and 267-305 and 307-424"
# ---- fresh, mutants
fresh("proj-autograder-rerun-mutants-m01-m37", "ledgers/AC4/mutants (93 files: fx10_*, fx11_*, fx12_*, m01-m61, r13e_01-r13e_04)", MUT_NOTE + ". Every listed mutant is KILLED on seed 0 and on seeds 0, 1 and 25; none survives.")
fresh("proj-mutant-descriptions", "ledgers/AC4/mutants/ (first docstring line of each of the 93 files)", "Re-run round 13 (ledgers/AC4/scripts/AC4-e-r13/checks_r13.py, out/checks_r13.out): all 93 mutants have a non-empty first docstring line; each line names the error, e.g. r13e_01 'Student error: the flexed variable cost is rounded up to the next cent whatever its fraction'. The mutate_graders output prints each description.")
for mid_pat, desc in [("m07","m07"),("m12","m12"),("m21-m24-equivalence","m21-m24"),("m25-m29","m25-m29")]:
    pass
fresh("proj-mutant-m07-empty-name", "ledgers/AC4/mutants/m07_empty_name_accepted.py", "Re-run round 13: " + MUT_NOTE + ". m07 is KILLED.")
fresh("proj-mutant-m12-duplicate-names", "ledgers/AC4/mutants/m12_duplicate_names_accepted_in_two_functions.py", "Re-run round 13: " + MUT_NOTE + ". m12 is KILLED.")
for rid, rng in [("proj-mutants-m01-m06","m01-m06"),("proj-mutants-m08-m11","m08-m11"),("proj-mutants-m13-m20","m13-m20"),("proj-mutants-m15-m19","m15-m19"),("proj-mutants-m21-m24","m21-m24"),("proj-mutants-m21-m24-equivalence","m21-m24"),("proj-mutants-m25-m29","m25-m29"),("proj-mutants-r6-new","m30-m34"),("proj-mutants-r7-new","m35-m37"),("proj-mutants-r8-new","m38-m40"),("proj-mutants-r9-new","m41-m46"),("proj-mutants-r10-new","m47-m50"),("proj-mutants-r11-m53-m55","m53-m55"),("proj-r12-mutants-new-student-errors","m56-m59, m61, fx12_*"),("proj-mutant-m52-dict-only-case","m52")]:
    fresh(rid, f"ledgers/AC4/mutants/ ({rng})", "Re-run round 13: " + MUT_NOTE + f". Every mutant in {rng} is KILLED.")
fresh("proj-r12-mutant-m60-scope", "ledgers/AC4/scripts/AC4-e-r12/out_of_scope/m60_case_name_pairs_refused.py", "Re-run round 13 with run_mutants.py on seeds 0 and 1: m60 SURVIVED (rc 0 on both seeds). It is out of scope: it refuses 'Alpha' with 'alpha', which the page's constraint 'a product name ... appears twice' does not list, and no page sentence says that case-variant names are allowed. Judged out of scope (no sentence violated), so it is not in the mutant list; PASS.")
# ---- new mutants (verifier-written)
add("proj-r13-mutants-new-student-errors", "Four new student-error mutants written this round, each a complete module in ledgers/AC4/mutants with a one-line description",
    "ledgers/AC4/mutants/r13e_01_flexed_variable_cost_rounds_up_always.py; r13e_02_products_not_a_list_is_a_type_error.py; r13e_03_mix_rounds_each_product_term.py; r13e_04_flexible_budget_accepts_empty_names.py (made by ledgers/AC4/scripts/AC4-e-r13/make_r13e.py and make_r13e4.py)",
    "PASS", "All four are KILLED (out/mutate_graders_r13.out): r13e_01 (ceiling of the flexed variable cost) by test_every_grader_seed_reconciles_exactly[6] on seed 0; r13e_02 (TypeError for a non-list products field) by test_products_that_are_not_a_list_raise_value_error[mapping-master_budget] on seed 0; r13e_03 (each product's mix term rounded to a cent) by test_flexed_variable_cost_below_half_a_cent_rounds_down on seed 0; r13e_04 (empty name accepted in flexible_budget) by test_empty_product_name_raises_value_error[flexible_budget] on seed 0. All four also killed on seeds 0, 1 and 25 (out/run_mutants_seeds_0_1_25.out).")
# ---- fresh gate reruns
fresh("proj-autograder-reference", "course/modules/AC/AC4/grader/reference.py; course/modules/AC/AC4/grader/test_project.py",
      "Re-run round 13: tools/run_graders.py --unit AC4 --seeds 0-49 -> 'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.3 s)'. Direct run in /tmp/ac4-v/e13/ref (reference copied to budget_engine.py, QF_SEED=0, pytest -q --assert=plain -W error) -> '461 passed'.")
fresh("proj-collect-count", "course/modules/AC/AC4/project.html line 265 (Grading mode, '461 checks'); course/modules/AC/AC4/grader/test_project.py",
      "Re-run round 13: pytest --collect-only -q for QF_SEED=0..49 with the reference copied in: 9 seeds, 40 seeds and 1 seed each print '461 tests collected' (50 of 50 seeds equal 461). Line 265 says 461 checks: equal.")
fresh("proj-autograder-alternatives", "course/modules/AC/AC4/grader/test_project.py; ledgers/AC4/scripts/AC4-e-r13/alts/alt13_a_integer_divmod.py, alt13_b_fraction_floor.py; ledgers/AC4/scripts/AC4-e-r12/alt_r12_a..e (copied to /tmp/ac4-v/e13/alts12)",
      "Correct alternatives pass on the new suite: alt13_a (integer divmod half-up, explicit type checks) and alt13_b (Fraction floor(x+1/2), numbers.Integral with bool refused) each PASS 50/50 seeds (out/alts12_rerun.out and the run recorded in this round); round-12 alt_r12_a..e each PASS 50/50 (out/alts12_rerun.out). Earlier alternatives re-run on 50 seeds (out/oldalts_rerun.out): every failure is on a test whose rule the page states (read-only Mapping 'a mapping'; tuple or None or number products 'a list of mappings'; None case 'not a mapping'); r8_alt_e and r9_alt_e pass 50/50.")
fresh("proj-alt-l-extra-keys", "ledgers/AC4/scripts/AC4-e-r10/alt_l.py; course/modules/AC/AC4/grader/test_project.py",
      "Re-run round 13 (out/oldalts_rerun.out, r10_alt_l): FAILED on 50 seeds only through test_products_that_are_not_a_list_raise_value_error[tuple-*], a tuple of products, which the page states must raise ValueError ('a list of mappings'). The extra-keys behaviour is not the failing test.")
fresh("proj-autograder-alt-decimal", "ledgers/AC4/scripts/AC4-e-r13/alts/ (alt_r12_a_decimal_half_up.py copied from AC4-e-r12); course/modules/AC/AC4/grader/test_project.py",
      "Re-run round 13: alt_r12_a_decimal_half_up.py -> PASS 50/50 seeds on the current suite (out/alts12_rerun.out).")
fresh("proj-r12-alternatives-new", "ledgers/AC4/scripts/AC4-e-r12/alt_r12_a..e and make_alts_r12.py; out/alts.out",
      "Re-run round 13 on the current suite: alt_r12_a..e each PASS 50/50 seeds (out/alts12_rerun.out).")
add("proj-r13-alternatives-new", "Two further spec-correct alternatives written this round pass the new half-cent and mix tests",
    "ledgers/AC4/scripts/AC4-e-r13/alts/alt13_a_integer_divmod.py; alt13_b_fraction_floor.py",
    "PASS", "alt13_a: integer-only half-up rounding with divmod, explicit type checks, products validated by hand. alt13_b: Fraction arithmetic with floor(x + 1/2), numbers.Integral with bool refused, KeyError turned into ValueError. Each PASS 50/50 seeds under -W error --assert=plain (run_alts_r12.py, out/alts12_rerun.out and the round-13 run). No over-constraint found.")
fresh("proj-r12-cards-c130", "course/modules/AC/AC4/cards.json (AC4-c130 object); course/modules/AC/AC4/L01.html lines 70-76",
      "Carried from round 12 (course/modules/AC/AC4/L01.html and the AC4-c130 object in cards.json byte-identical since the previous pin; cards.json changed only at AC4-c073): " + prev["proj-r12-cards-c130"]["evidence"], status="PASS")
# ---- project page rows, fresh where the subject changed
fresh("proj-spec-products-list-tuple", "course/modules/AC/AC4/project.html line 263 (Constraints) and line 252 ('a list of mappings'); course/modules/AC/AC4/grader/reference.py line 64",
      "Re-run round 13: reference.py unchanged since aebdc15; the suite refuses a tuple of products (test_products_that_are_not_a_list_raise_value_error[tuple-*]), a dict, a string, None and a number, each with ValueError, and the reference passes 461/461 on seed 0. Page line 263 lists 'products are not a list of mappings' and line 252 says 'a list of mappings': the tuple refusal is stated.")
fresh("proj-messages-no-leak", "course/modules/AC/AC4/grader/test_project.py (test_exact_half_cent_in_variable_cost_rounds_up, test_flexed_variable_cost_below_half_a_cent_rounds_down, test_products_that_are_not_a_list_raise_value_error, test_empty_product_name_raises_value_error and the other changed tests)",
      "Re-read round 13: every assertion message in the changed and added tests names the property ('a half cent of variable cost must round up, not down.', 'a third of a cent of variable cost must round down, not up.', 'products given as a NoneType, not a list') and no message prints an expected value. must_raise messages are fixed strings.")
fresh("proj-messages-bare-asserts", "course/modules/AC/AC4/grader/test_project.py",
      "Re-run round 13 (ledgers/AC4/scripts/AC4-e-r13/checks_r13.py, out/checks_r13.out): no bare assert in test_project.py.")
fresh("proj-grader-comments", "course/modules/AC/AC4/grader/test_project.py (comments in test_mix_is_within_one_cent_of_the_exact_fraction and in the new half-cent tests)",
      "The comments of the two new half-cent tests are correct (their arithmetic is re-derived in proj-r13-new-half-cent-tests). The comment of test_mix_is_within_one_cent_of_the_exact_fraction says 'Each rounding moves a flexed amount by less than half a cent'; that is false for an exact half cent (see proj-r13-grader-mix-comment). Other grader comments are unchanged functions (AST-identical), carried in their rows.",
      status="FAIL", fix="Rewrite the comment in test_mix_is_within_one_cent_of_the_exact_fraction: 'Each rounding moves a flexed amount by at most half a cent, so their difference is less than one cent.' (see proj-r13-grader-mix-comment).")
fresh("proj-grader-equal-margin-comment", "course/modules/AC/AC4/grader/test_project.py (test_two_product_shift_to_lower_margin_is_unfavourable, now at line 523)",
      "Carried from round 12 (test_project.py::test_two_product_shift_to_lower_margin_is_unfavourable AST-identical since aebdc15; no changed hunk touches it; the file moved by +56 lines before this function): " + prev["proj-grader-equal-margin-comment"]["evidence"])
fresh("proj-equal-margin-branch", "course/modules/AC/AC4/grader/test_project.py (test_two_product_shift_to_lower_margin_is_unfavourable, now at line 523)",
      "Carried from round 12 (test_project.py::test_two_product_shift_to_lower_margin_is_unfavourable AST-identical since aebdc15): " + prev["proj-equal-margin-branch"]["evidence"])
fresh("proj-spec-clarity-and-errors", "course/modules/AC/AC4/project.html line 263 (Constraints); course/modules/AC/AC4/grader/test_project.py",
      "Re-run round 13: every refused condition on page line 263 has a test in the suite: case not a mapping (test_case_that_is_not_a_mapping_raises_value_error), case without a field (test_missing_case_field_raises_value_error), whole-number check (test_case_field_not_a_whole_number..., test_product_field_not_a_whole_number..., test_product_field_boolean..., test_case_number_given_as_text..., test_product_number_given_as_text...), negative count or amount (test_negative_*), empty product list (test_empty_product_list_raises_value_error), product name not text/empty/duplicate (test_product_name_that_is_not_text..., test_empty_product_name_raises_value_error, test_duplicate_product_names_raise_value_error), no budgeted units (test_zero_budgeted_units_raise_value_error), negative or non-integer actual units to flexible_budget (test_negative_actual_units_argument..., test_non_whole_actual_units_argument..., test_boolean_actual_units_argument...). Products-not-a-list now also covers None and 5.")
fresh("proj-spec-coverage-claims", "course/modules/AC/AC4/project.html line 265 (Grading mode); course/modules/AC/AC4/grader/test_project.py",
      "Re-run round 13: the coverage list (master budget, flexed budget, the four variances and total, reconciliation on seeds 0-49, sign of each variance in both directions, zero-variance, single product, zero-unit, every ValueError, purity and silence) maps to tests that exist and pass on the reference; the count '461 checks' is equal to the collect-only count on all 50 seeds (proj-collect-count).")
fresh("proj-spec-empty-name-claim", "course/modules/AC/AC4/project.html line 263 (Constraints); course/modules/AC/AC4/grader/test_project.py (test_empty_product_name_raises_value_error, now parametrized over the three functions, line 828)",
      "Re-run round 13: empty product name is refused by master_budget, flexible_budget and variance_decomposition (three parametrized cases). r13e_04 (empty name accepted only in flexible_budget) is KILLED. Page line 263 'a product name ... is empty': stated.")
fresh("proj-spec-fresh-objects-claim", "course/modules/AC/AC4/project.html line 263 (Constraints); course/modules/AC/AC4/grader/test_project.py (test_master_returns_fresh_objects, AST-identical, line 244)",
      "Carried from round 12 (test_project.py::test_master_returns_fresh_objects AST-identical since aebdc15; page line 263 unchanged): " + prev["proj-spec-fresh-objects-claim"]["evidence"])
fresh("proj-spec-sign-both-directions", "course/modules/AC/AC4/grader/test_project.py (test_price_variance_is_favourable_when_price_rises, test_price_variance_is_unfavourable_when_every_price_falls, test_efficiency_is_positive/negative..., test_volume_variance_..., test_two_product_shift_to_*, now at lines 453-630)",
      "Carried from round 12 (those test functions AST-identical since aebdc15; no changed hunk touches them; line numbers now +56 to +59): " + prev["proj-spec-sign-both-directions"]["evidence"] + " Re-run round 13: all PASS on the reference.")
fresh("proj-spec-reconcile-seeds", "course/modules/AC/AC4/grader/test_project.py (test_every_grader_seed_reconciles_exactly, parametrized over range(50), line 755)",
      "Re-run round 13: test_every_grader_seed_reconciles_exactly[0..49] all PASS on the reference (461/461). The function is AST-identical since aebdc15.")
fresh("proj-r12-read-only-mapping-test", "course/modules/AC/AC4/grader/test_project.py test_case_that_is_a_read_only_mapping_is_accepted (AST-identical, now at line 966); course/modules/AC/AC4/project.html line 252 ('a mapping')",
      "Carried from round 12 (test_case_that_is_a_read_only_mapping_is_accepted AST-identical since aebdc15): " + prev["proj-r12-read-only-mapping-test"]["evidence"] + " Re-run round 13: the reference passes it; alt_r8_a, r8_alt_b, r9_alt_a, r9_alt_b fail it, as the round-12 note says.")
fresh("proj-r12-none-and-bool-tests", "course/modules/AC/AC4/grader/test_project.py (test_case_field_that_is_none..., test_product_field_that_is_none..., boolean tests, AST-identical); course/modules/AC/AC4/project.html line 263",
      "Carried from round 12 (those test functions AST-identical since aebdc15; page line 263 unchanged): " + prev["proj-r12-none-and-bool-tests"]["evidence"])
fresh("proj-r12-product-not-mapping-valueerror", "course/modules/AC/AC4/grader/test_project.py test_product_that_is_not_a_mapping_raises_value_error (AST-identical); course/modules/AC/AC4/project.html line 263",
      "Carried from round 12 (test_product_that_is_not_a_mapping_raises_value_error AST-identical since aebdc15): " + prev["proj-r12-product-not-mapping-valueerror"]["evidence"] + " Re-run round 13: alt_r8_h fails it with TypeError, as before.")
fresh("proj-r12-float-units-test", "course/modules/AC/AC4/grader/test_project.py test_float_actual_units_argument_raises_value_error (AST-identical); course/modules/AC/AC4/project.html line 263",
      "Carried from round 12 (test_float_actual_units_argument_raises_value_error AST-identical since aebdc15): " + prev["proj-r12-float-units-test"]["evidence"])
fresh("proj-r12-count-matches-page", "course/modules/AC/AC4/project.html line 265; course/modules/AC/AC4/grader/test_project.py",
      "Re-run round 13: line 265 says 461 checks; collect-only gives 461 on all seeds 0-49 (proj-collect-count). Equal.")
fresh("proj-purity-order-dependence", "course/modules/AC/AC4/grader/test_project.py lines 1050-1093 (purity, silence, order, shared-case tests; AST-identical)",
      "Carried from round 12 (the purity, silence, order and shared-case functions are AST-identical since aebdc15; no changed hunk touches lines 1050-1097): " + prev["proj-purity-order-dependence"]["evidence"] + " Re-run round 13: all PASS on the reference, and test_shared_case_is_unchanged_by_the_suite passes.")
fresh("proj-banned-phrases", "course/modules/AC/AC4/project.html (changed lines 260, 265, 306); course/modules/AC/AC4/cards.json (AC4-c073); changed test comments",
      "Re-run round 13: grep -E for 'roughly half', 'about 6%', 'historically', an ellipsis in prose, 'builder', 'verifier', 'unit report', 'REQUESTS' over project.html and grader/*.py: no hit in learner prose (the only '...' hits are Python type annotations tuple[str, ...] in test_project.py lines 42-43). The changed sentences of lines 260, 265, 306 and card c073 contain none of them.")
fresh("proj-rubric-C4-observation", "project.html line 306 (memo intro, now 'For criterion C4 (in the table below), an observation ...'), line 316 and line 373",
      "Re-read round 13: line 306 now restricts the observation and threshold definition to criterion C4. The C4 row (line 317 of project.html, the table row for C4) says 'names, with a threshold figure, an observation that would reverse one of those actions' and level 3 says 'an observation that would change one of them, with no threshold figure'; the definition 'a threshold is that value' is consistent with both. 'observation' is used only in the C4 row and in its exemplar annotations (lines 373, 381). Exemplar B's threshold (5,400 cents) is the one the definition describes. PASS.")
fresh("proj-hours", "course/modules/AC/AC4/project.html lines 277-285 (time-budget table); course/modules/AC/AC4/index.html line 29 (data-hours-lessons=50, data-hours-project=20)",
      "Re-run round 13 arithmetic: project rows 1+2+2+6+4+2+2+1 = 20 (total row 20); lesson declarations data-hours 6+7+6+6+7+6+6+6 = 50 (L01-L08); hub split 50 + 20 = 70 (index.html line 31 says 70 hours). Hub split and lesson hours agree. The hours table and index.html are byte-identical to aebdc15 at these lines.")
fresh("proj-check-pages", "course/modules/AC/AC4/*.html and cards.json", "Re-run round 13: tools/check_pages.py --all -> 'check_pages AC2/AC4/CF1/AP1: PASS' (exit 0; out/check_pages.out).")
fresh("proj-check-dag", "course/modules/AC/AC4/", "Re-run round 13: tools/check_dag.py --all -> 'check_dag AC4: PASS' (exit 0).")
fresh("proj-check-projects", "course/modules/AC/AC4/project.html", "Re-run round 13: tools/check_projects.py --all -> 'check_projects AC4: PASS' (exit 0).")
fresh("proj-page-smoke", "course/modules/AC/AC4/project.html", "Re-run round 13: tools/page_smoke.py --unit AC4 --pages project.html -> 'page_smoke AC4: PASS' rc 0 (out/page_smoke_project_full.out). An earlier run with --skip-sweep also passed (out/page_smoke_project.out).")
fresh("proj-ruff-mypy", "course/modules/AC/AC4/grader; tests/labs/AC4; repository mypy configuration", "Re-run round 13: ruff check on grader and tests/labs/AC4 clean; ruff format --check on grader: '4 files already formatted'; .venv/bin/mypy --no-incremental: 'Success: no issues found in 153 source files' (rc 0; out/mypy_repo.out).")
fresh("proj-run-labs-ac4", "tests/labs/AC4", "Re-run round 13: tools/run_labs.py --unit AC4 -> 'run_labs AC4: PASS (10/10)'.")
fresh("proj-run-graders-ac4", "course/modules/AC/AC4/grader", "Re-run round 13: tools/run_graders.py --unit AC4 --seeds 0-49 -> PASS (reference 50/50 seeds).")
fresh("proj-cards-structure", "course/modules/AC/AC4/cards.json (131 cards)", "Re-run round 13 (ledgers/AC4/scripts/AC4-e-r13/cards_check.py): 131 cards; ids unique; no duplicate fronts or backs (case-insensitive); key sets are the three shapes used in rounds 10-12; lessons L01 18, L02 19, L03 19, L04 15, L05 10, L06 16, L07 16, L08 18. The only changed card is AC4-c073.")
fresh("proj-cards-duplicates", "course/modules/AC/AC4/cards.json", "Re-run round 13 (cards_check.py): no duplicate id, front or back across 131 cards; c073's new back is unique.")
fresh("proj-cards-changed-lessons", "cards.json cards from L05 and L06 (AC4-c059..c068 and the L06 cards, including AC4-c073); course/modules/AC/AC4/L05.html; course/modules/AC/AC4/L06.html",
      "Re-checked round 13: the L06 card AC4-c073 changed this round and its back over-generalises Proposition 2.2(c) (see proj-r13-card-c073-scope). The other L05 and L06 cards in the round-12 sample are unchanged and were carried.", status="FAIL",
      fix="Fix AC4-c073 as in proj-r13-card-c073-scope; then the L05/L06 sample stands.")
# ---- carries: subject byte-identical (project.html lines not in {265, 306}; lessons; labs; instance; starter; reference; references; card objects other than c073)
PH = "course/modules/AC/AC4/project.html lines {} (byte-identical since aebdc15; the only changed project.html lines are 265 and 306)"
carry_list = [
 ("proj-lab-1", PH.format("53-147")),
 ("proj-lab-1-interpretation", PH.format("146")),
 ("proj-r12-lab1-derived-figures", PH.format("146")),
 ("proj-lab-1-interpretation-second-clause", PH.format("146")),
 ("proj-lab-1-run-line146-untouched", PH.format("53-145")),
 ("proj-lab-2", PH.format("149-243") + " and tests/labs/AC4/lab-AC4-project-2.py"),
 ("proj-instances", "course/modules/AC/AC4/grader/instance.py"),
 ("proj-alt-instance-coverage", "course/modules/AC/AC4/grader/instance.py and starter.py"),
 ("proj-r12-cards-c131", "course/modules/AC/AC4/L03.html and the AC4-c131 object in cards.json"),
 ("proj-rubric-exhaustive", PH.format("314-318")),
 ("proj-rubric-scoring-rule", PH.format("308")),
 ("proj-rubric-C2-terms", PH.format("308 and 315")),
 ("proj-calib-A-scores", PH.format("326 and 330-340")),
 ("proj-calib-A-annotation", PH.format("343-351")),
 ("proj-calib-B-scores", PH.format("357 and 363")),
 ("proj-calib-B-annotation", PH.format("377-382")),
 ("proj-exemplar-B-consequences", PH.format("370")),
 ("proj-exemplar-B-threshold", PH.format("373")),
 ("proj-exemplar-B-verdict", PH.format("359 and 362-375")),
 ("proj-memo-structure-length", PH.format("330 onward and 361-373")),
 ("proj-exemplar-intro-universal-claim", PH.format("324 and 370")),
 ("proj-exemplar-overall-level", PH.format("324, 327, 357")),
 ("proj-reading-list-sentence", PH.format("267")),
 ("proj-ladder-lede", PH.format("42") + " and course/modules/AC/AC4/index.html lines 70 and 155"),
 ("proj-simulated-and-data", PH.format("53-56 and 252") + " and tests/labs/AC4/lab-AC4-project-1.py"),
 ("proj-inputs-every-number-int", PH.format("252 and 260")),
 ("proj-stretch-two-inputs-scope", PH.format("399")),
 ("proj-conventions-no-spending-claim", PH.format("260 and 398") + " (this row covers only the no-spending sentence; the mix sentence on line 260 is row proj-r13-spec-mix-sentence)"),
 ("proj-stretch-spending", PH.format("398")),
 ("proj-stretch-two-inputs", PH.format("399")),
 ("proj-stretch-list-intact", PH.format("396-401")),
 ("proj-card-c020", "the AC4-c020 object in cards.json (lines 134-138) and course/modules/AC/AC4/L02.html"),
 ("proj-card-c078", "the AC4-c078 object in cards.json (lines 553-557) and course/modules/AC/AC4/L06.html"),
 ("proj-card-c091", "the AC4-c091 object in cards.json (line 641) and course/modules/AC/AC4/L07.html"),
 ("proj-card-c061", "the AC4-c061 object in cards.json (line 436) and course/modules/AC/AC4/L05.html"),
 ("proj-card-c126-basis", "the AC4-c126 object in cards.json and course/modules/AC/AC4/L03.html"),
 ("proj-card-c102", "the AC4-c102 object in cards.json (lines 718-721) and course/modules/AC/AC4/L08.html"),
 ("proj-card-c129", "the AC4-c129 object in cards.json (line 914) and course/modules/AC/AC4/L08.html"),
 ("proj-cards-sample", "the sampled card objects (c010-c080 except c073) in cards.json and their lessons"),
 ("proj-cards-r10-L01", "the AC4-c003, c012, c014, c120, c127, c128 objects in cards.json and course/modules/AC/AC4/L01.html"),
 ("proj-cards-r10-L02", "the AC4-c029, c125 objects in cards.json and course/modules/AC/AC4/L02.html"),
 ("proj-cards-r10-L03", "the AC4-c038, c040, c042, c043, c122, c123, c124 objects in cards.json and course/modules/AC/AC4/L03.html"),
 ("proj-cards-r10-L04", "the AC4-c045, c121 objects in cards.json and course/modules/AC/AC4/L04.html"),
 ("proj-cards-changed-lessons-r10", "the AC4-c059..c068 objects in cards.json (none is c073) and course/modules/AC/AC4/L05.html and L06.html"),
 ("proj-cards-targeted", "the AC4-c062, c063, c064, c066, c067, c075, c076 objects in cards.json"),
 ("proj-cards-number-format", "the AC4-c101, c102, c109 objects in cards.json"),
]
for rid, subj in carry_list:
    add(rid, prev[rid]["check"], prev[rid]["location"], "PASS",
        f"Carried from round 12 ({subj}): " + prev[rid]["evidence"])
# ---- fresh verifications of references and the alternative mutants re-run
add("proj-citations-reading", prev["proj-citations-reading"]["check"], prev["proj-citations-reading"]["location"], "PASS",
    "Re-run round 13: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (rc 0, out/verify_refs_offline.out); tools/verify_refs.py --unit AC4 (live) -> 'live re-verification of AC4: 2 of 560 entries, 0 problems' (rc 0, out/verify_refs_live_ac4.out). references/references.json and the reading list are byte-identical to aebdc15 (no change in this diff). The reading list says the specification defines each quantity the autograder tests, which the spec's 'Context' and 'Required outputs' support.")
fresh("proj-alt-g-student-error", "ledgers/AC4/scripts/AC4-e-r8/alt_g.py (re-run in /tmp/ac4-v/e13/oldalts/r8_alt_g.py)",
      "Re-run round 13 (out/oldalts_rerun.out): r8_alt_g FAILED on 50 seeds, first failure test_case_that_is_not_a_mapping_raises_value_error[none-*] (a case of None, which the page's 'a case that is not a mapping' requires to raise ValueError). Rejection is correct.")
# ---- new verifications this round
add("proj-r13-spec-mix-sentence", "Conventions: 'The sales mix variance uses the whole-cent flexed profit, so it can differ from the exact, unrounded flexed profit by less than one cent.'",
    "course/modules/AC/AC4/project.html line 260 (Conventions)", "FAIL",
    "The sentence compares a variance with a profit. Read literally it is false: in Lab 1 (project.html line 53-147 output) the sales mix variance is -462857 cents and the exact unrounded flexed profit is 3142857 + 1/7 cents, so they differ by about 3.6 million cents. The claim the grader checks (test_mix_is_within_one_cent_of_the_exact_fraction, 50 seeds) is that the mix variance differs from the mix variance computed with the exact unrounded flexed profit by less than one cent. Re-derived: flexed revenue and flexed variable cost each err by a value in (-1/2, 1/2] cent, so the mix error lies in (-1, 1); the tested bound is correct, the sentence is not.",
    "Replace with: 'The sales mix variance uses the whole-cent flexed profit, so it differs from the mix variance computed with the exact, unrounded flexed profit by less than one cent.'")
add("proj-r13-grader-mix-comment", "Comment in test_mix_is_within_one_cent_of_the_exact_fraction: 'Each rounding moves a flexed amount by less than half a cent, so their difference is less than one cent.'",
    "course/modules/AC/AC4/grader/test_project.py, function test_mix_is_within_one_cent_of_the_exact_fraction (now line 443-449)", "FAIL",
    "The first clause is false when the exact amount ends in one half: test_exact_half_cent_rounds_up (line ~323) computes 1001/2 = 500.5 cents and rounds it to 501, a move of exactly half a cent. The second clause (the difference is less than one cent) is correct: the two errors lie in (-1/2, 1/2] and the difference is strictly less than 1, which the assertion < 1 checks.",
    "Change the comment to: '# Each rounding moves a flexed amount by at most half a cent, so their difference is less than one cent.'")
add("proj-r13-card-c073-scope", "AC4-c073 (lesson L06, 'What is the efficiency variance?'): 'Kilograms used above the standard allowance for the actual output make E negative (Definition 1.2; Proposition 2.2(c)).'",
    "course/modules/AC/AC4/cards.json line 521 (AC4-c073, back); course/modules/AC/AC4/L06.html line 98 (Proposition 2.2 parts (a)-(c) and the counterexample)", "FAIL",
    "Proposition 2.2(c) in L06.html line 98 says E is negative when the SUM of actual kilograms exceeds the SUM of standard kilograms allowed, and the same paragraph gives the counterexample: 50 kg above allowance on one product and 50 kg below on another give E = 0 while no product matches its allowance. The card's wording ('Kilograms used above the standard allowance') reads as a per-product statement, which the lesson refutes. The citation to (c) is right; the scope is not. The change this round added only the '(Definition 1.2; Proposition 2.2(c))' citation; the underlying sentence was already wrong in round 12.",
    "Change to: 'The total kilograms used above the total standard allowance for the actual output make E negative, while an excess on one product offset by a saving on another does not (Definition 1.2; Proposition 2.2(c)).'")
add("proj-r13-new-half-cent-tests", "test_exact_half_cent_in_variable_cost_rounds_up and test_flexed_variable_cost_below_half_a_cent_rounds_down (added this round, lines 349-404)",
    "course/modules/AC/AC4/grader/test_project.py lines 349-404",
    "PASS", "Arithmetic re-derived: test 1 has budgeted variable cost 2 cents (Cord: 2 units x 1 standard x 1 cent) over 4 budgeted units; at 1 unit the flexed variable cost is 2/4 = 1/2 cent, which halves-up to 1; the test asserts 1 and the oracle's flex_variable is 1. Test 2 has budgeted variable cost 1 cent (Pen: 1 x 1 x 1) over 3 budgeted units; at 1 unit it is 1/3 cent, which rounds to 0; asserted 0. Both pass on the reference (461 passed), and both are exercised by the mutants r13e_01 (ceiling) and r13e_03 (per-product rounding), which are KILLED on seeds 0, 1 and 25. The alternatives alt13_a and alt13_b pass 50/50.")
add("proj-r13-mix-tolerance-test", "test_mix_is_within_one_cent_of_the_exact_fraction, parametrized over seeds 0-49 with '< 1' (was '<= 1' in round 12)",
    "course/modules/AC/AC4/grader/test_project.py lines 443-449", "PASS",
    "The strict bound is correct: each flexed amount's rounding error is in (-1/2, 1/2] cent (halves-up), so the difference of two such errors is strictly less than 1. Reference passes all 50 seeds. Alternatives alt13_a, alt13_b and alt_r12_a..e (different rounding code) pass all 50 seeds, so the bound does not over-constrain. The comment on the test is a separate row (proj-r13-grader-mix-comment).")
add("proj-r13-verify-refs", "tools/verify_refs.py --offline and --unit AC4", "references/references.json; course/modules/AC/AC4/project.html reading list", "PASS",
    "Offline integrity 560 entries, 0 problems; live AC4 2 of 560 entries, 0 problems (out/verify_refs_offline.out, out/verify_refs_live_ac4.out). No new citation was added to the page this round.")
add("proj-r13-hours-split", "Hours split: hub 50 lesson hours and 20 project hours; project time table sums to 20", "course/modules/AC/AC4/project.html lines 277-285; course/modules/AC/AC4/index.html lines 29 and 31", "PASS",
    "Recomputed: 1+2+2+6+4+2+2+1 = 20; lessons 6+7+6+6+7+6+6+6 = 50; 50+20 = 70 = index.html line 31. No arithmetic inconsistency. (The architect ruling on pace estimates was applied: no pace-based failure.)")
# ---- write the fragment
rows_out = []
seen = set()
for r in rows:
    assert r["id"] not in seen, r["id"]
    seen.add(r["id"]); rows_out.append(r)
missing = [k for k in prev if k not in seen]
print("missing previous ids:", missing)
extra = [k for k in seen if k not in prev]
print("new ids:", extra)
import sys
sys.path.insert(0, "/tmp/verify13-AC4-e/tools")
statuses = [r["status"] for r in rows_out]
summary = {"rows": len(rows_out), "pass": statuses.count("PASS"), "fail": statuses.count("FAIL"),
           "unverifiable": statuses.count("UNVERIFIABLE"), "mutants_killed": len(mutants), "mutants": len(mutants)}
frag = {
  "unit": "AC4", "slice": "AC4-e", "round": 13,
  "verifier": "Claude Haiku 5.5 (independent verifier, round 13, slice AC4-e; did not build AC4)",
  "pin": "eaf6d87",
  "base": "aebdc15 (round-12 pin; previous fragment /tmp/fanout-frags/AC4-e.round12.json used as context only)",
  "checkout": "/tmp/verify13-AC4-e",
  "scratch": "/tmp/ac4-v/e13",
  "verified_at": "2026-10-28T21:00:00+00:00",
  "verdict": "FAIL" if summary["fail"] else "PASS",
  "rows": rows_out,
  "mutants": mutants,
  "registry_flags": [],
  "freshness_flags": [],
  "notes": ("Delta aebdc15..eaf6d87 for this slice: project.html changed at lines 265 (Grading mode count 402 -> 461) and 306 (memo intro, C4 scope); "
            "cards.json changed at line 521 only (AC4-c073 back, adds 'Proposition 2.2(c)'); grader/test_project.py changed in 3 functions "
            "(test_empty_product_name_raises_value_error, test_mix_is_within_one_cent_of_the_exact_fraction, test_products_that_are_not_a_list_raise_value_error) "
            "and 2 functions were added (the half-cent tests); 87 functions are AST-identical to aebdc15 and carried at function level. "
            "reference.py, instance.py, starter.py, tests/labs/AC4, the lesson pages L01-L08, index.html and references.json are byte-identical. "
            "Line numbers in carried rows refer to aebdc15 for project.html lines after 265 and for test_project.py lines after 348: test functions after line 348 moved by +56 lines, and those after line 442 by +59 (after the mix hunk). "
            "Mutants: 93 flat files in ledgers/AC4/mutants (79 from round 12 list, 9 fx12_* added by the round-12 fixes, and 4 new r13e_* written by this verifier); all 93 KILLED by tools/mutate_graders.py --unit AC4 --seeds 0-9 and by run_mutants.py on seeds 0, 1, 25. m60 (case-variant names refused) survives on seeds 0 and 1 and is out of scope (no page sentence says case-variant names are accepted or refused; it is not listed). "
            "Alternatives: alt13_a and alt13_b (new), alt_r12_a..e (round 12) pass 50/50; earlier alternatives (r8/r9/r10) fail only on tests whose rules the page states. "
            "Commands run this round: check_pages, check_dag, check_projects (--all), run_labs AC4 (10/10), run_graders AC4 (50/50), collect-only (461 on all seeds), reference pytest (461 passed), mutate_graders AC4 seeds 0-9 (93/93), run_mutants seeds 0,1,25 (93/93), ruff check + format, mypy --no-incremental (repo, 153 files, no issues), page_smoke AC4 project.html (default and --skip-sweep), verify_refs --offline and --unit AC4 (live), tests/test_memo_exemplars.py (14 passed; it covers S7, not AC4). "
            "Accidental run: one pytest invocation with no file argument (the grep for AC4 in tests/*.py matched nothing) collected from the repository root, returned rc 0, and printed no summary line; it was not used as evidence. "
            "Not checked: a Pyodide browser run beyond page_smoke; every lesson card back against its lesson (only c073 and the rows carried from round 12 by object); the rendered memo rubric in a browser; the self-assessment form; the full repository pytest suite (not run). "
            "The round-12 claim that the read-only Mapping test is spec-backed is accepted on the page's 'a mapping' (line 252)."),
  "summary": summary,
}
out = pathlib.Path("/tmp/verify13-AC4-e/ledgers/AC4/AC4-e.json")
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n")
import importlib
import ledger  # from tools
print("validate:", ledger.validate(json.loads(out.read_text()), "AC4-e"))
print(summary, frag["verdict"])
