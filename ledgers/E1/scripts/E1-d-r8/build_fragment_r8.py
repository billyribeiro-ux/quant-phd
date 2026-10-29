"""Round 8 fragment builder for E1 slice d (verifier-authored; rows reflect this round's runs)."""
import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyB8-E1-d")
S = "ledgers/E1/scripts/E1-d-r8"
PIN = "ce7b3821c288da3dbba5dd4c90fb87dfd6d30089"
PREV = "7aa909e95b757b1abf7b75186d5fa1ed7d1945a4"
CARRY = "Carried from round 7 (%s byte-identical since the previous pin):"
PROJ = "course/modules/E/E1/project.html"
GR = "course/modules/E/E1/grader/"
CARDS = "course/modules/E/E1/cards.json"

def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or ""
    return r

rows = []
R = rows.append
R(row("E1d-proj-lab1-numbers", "2.5-lab", f"{PROJ} lab-E1-project-1 (lines 55-128)", "PASS",
  f"{S}/lab_page_vs_twin_r8.txt: page code equals twin (0 differing lines; trailing newline only). {S}/run_labs.txt: "
  "run_labs E1 PASS 12/12 (twin under python -I -W error matches the expected block). Numbers re-derived by hand "
  "(monopoly 50/70/2500/1250/3750/1250; Cournot 200/3->67, 160/3->53, 20000/9->2222, 40000/9->4444, 5000/9->556; "
  "Bertrand 100/20/0/5000/5000/0)."))
R(row("E1d-proj-lab2-numbers", "2.5-lab", f"{PROJ} lab-E1-project-2 (lines 130-187)", "PASS",
  f"{S}/lab_page_vs_twin_r8.txt: page code differs from the twin only at the two blanks (line 160 'return ___', line 165 "
  "'return half_up(___)'). Blank contents match the interpretation at line 186: (d - rival)/2 and "
  "(a*volume - volume*volume/2)/b - c*volume. Error after 60 steps d/(3*2^60) is about 2.9e-17, below 1e-12. run_labs PASS."))
R(row("E1d-proj-lab3-tie-numbers", "2.5-lab", f"{PROJ} lab-E1-project-3 (lines 189-257)", "PASS",
  f"{S}/lab3_numbers_r8.py -> {S}/lab3_numbers_r8.txt: independent Fraction recomputation reproduces all 12 expected rows "
  "(a=120 and a=121, half-up rounding, 'match' on each row). run_labs PASS (expected block equals twin output)."))
R(row("E1d-proj-lab-twins", "2.5-lab", "tests/labs/E1/lab-E1-project-{1,2,3}.py; project.html data-run blocks", "PASS",
  f"{S}/run_labs.txt: run_labs E1 PASS (12/12). {S}/lab_page_vs_twin_r8.txt: page code equals twin for labs 1 and 3, and "
  "for lab 2 except the blanks. The twins are unchanged since the previous pin (git diff empty)."))
R(row("E1d-proj-prop1", "2.4-math", f"{PROJ} prop-1 (id=prop-1, lines 284-287)", "PASS",
  CARRY % f"{PROJ} lines 284-287 (diff hunks of the previous pin are at lines 53, 390, 540 only)" +
  " Re-derived this round: pi(Q) = -Q^2/b + (d/b)Q, Q*=d/2, f(Q*) = (a+bc)/(2b), pi* = d^2/(4b)."))
R(row("E1d-proj-prop2", "2.4-math", f"{PROJ} prop-2 (id=prop-2, lines 289-292)", "PASS",
  CARRY % f"{PROJ} lines 289-292" +
  " Re-derived this round: best response max(0,(d-q_j)/2); equilibrium excludes q_1=0; q=d/3; fee (a+2bc)/(3b); profit per exchange d^2/(9b); e_{k+1}=-e_k/2 gives |e_k|=d/(3*2^k)."))
R(row("E1d-proj-prop3", "2.4-math", f"{PROJ} prop-3 (id=prop-3, lines 294-297)", "PASS",
  CARRY % f"{PROJ} lines 294-297" +
  " Re-read this round: cases f1<c, f1>c with f2>f1, f1=f2>c, f1=c<f2 each have a profitable deviation; (c,c) equilibrium. Holds for any tie rule with shares in [0,1]."))
R(row("E1d-proj-prop4", "2.4-math", f"{PROJ} prop-4 (id=prop-4, lines 299-302)", "PASS",
  CARRY % f"{PROJ} lines 299-302" + " Re-derived this round: CS = Q^2/(2b); W(d)-W(Q) = (d-Q)^2/(2b); welfare = CS + profit."))
R(row("E1d-proj-prop5", "2.4-math", f"{PROJ} prop-5 (id=prop-5, lines 304-307)", "PASS",
  CARRY % f"{PROJ} lines 304-307" +
  " Re-derived this round: differences d/6, d/3, d/(6b), d/(3b), d^2/(8b)-d^2/(18b)=5d^2/(72b), d^2/(36b); each bound > 1 for d > 6b."))
R(row("E1d-proj-spec-constraints", "2.6-spec", f"{PROJ} dl.spec (lines 312-323)", "PASS",
  CARRY % f"{PROJ} lines 312-323 and {GR}reference.py, {GR}test_project.py" +
  " Interface, key set, int type, ValueError conditions and messages agree with reference.py lines 26-35 and the must_raise phrases; 124 = collect-only count (see E1d-proj-r7-collect-count)."))
R(row("E1d-proj-hours", "2.6-hours", f"{PROJ} #hours (lines 333-349); course/modules/E/E1/index.html line 42", "PASS",
  CARRY % f"{PROJ} lines 333-349 and index.html line 42" +
  " Table sums to 30 (2+3+8+8+6+3); hub 90 lessons + 30 project = 120 (index.html line 31 says 120 hours)."))
R(row("E1d-proj-rubric-structure", "2.6-rubric", f"{PROJ} table#rubric, C6 level 2 (line 393)", "FAIL",
  "Level 2 now reads 'Names one or more of the limits, and states what changes for at most one of them'. Exemplar B fits it. "
  "But a memo that names all three limits and states the change for exactly two of them is not level 3 (level 3 needs 'for each'), "
  "not level 2 (level 2 allows at most one), and not level 1 ('No limit is stated'). Such a memo cannot be placed.",
  "Replace the C6 level-2 descriptor (line 393) with 'Names one or more of the limits, and states what changes for fewer than "
  "three of them', and quote the same text in the exemplar-B annotation (line 543)."))
R(row("E1d-proj-exemplar-blind-scoring", "2.6-rubric", f"{PROJ} #exemplar-a (401-464), #exemplar-b (466-549)", "PASS",
  "Blind scoring by the rubric alone: A = C1 1, C2 2, C3 2, C4 2, C5 1, C6 2; B = C1 4, C2 4, C3 4, C4 4, C5 3, C6 2. These equal "
  "data-scores (line 401: 1,2,2,2,1,2; line 466: 4,4,4,4,3,2). Each annotation is within one level of my score."))
R(row("E1d-proj-exemplar-annotation-C6", "2.6-rubric", f"{PROJ} #exemplar-b Limits annotation (line 543)", "PASS",
  "Line 543 quotes 'names one or more of the limits, and states what changes for at most one of them', which is the text of "
  "the current level-2 descriptor (line 393), and says that B names all three limits with a direction for constant cost only. "
  "The quote must be updated if the descriptor is changed (see E1d-proj-rubric-structure)."))
R(row("E1d-proj-rubric-C3-C5-level2", "2.6-rubric", f"{PROJ} table#rubric C3 level 2 (line 390), C5 level 2 (line 392)", "FAIL",
  "C3 level 2 covers 'one or two structures' or 'no rounding rule', so a memo that reports all three deadweight losses and "
  "states the rounding rule but gives no tie example meets neither level 2 nor level 3. C5 level 2 covers 'a structure without "
  "a justification' or 'a condition without a direction', so a justified recommendation with no condition at all meets neither "
  "level 2 nor level 3.",
  "C3 level 2: 'Reports the deadweight loss of one or two structures, or reports all three without the rounding rule or without a "
  "tie example.' C5 level 2: 'Names a structure without a justification from the numbers, justifies it without naming a condition, "
  "or names a condition without a direction.'"))
R(row("E1d-proj-autograder-reference", "2.6-autograder", f"{GR}reference.py; tools/run_graders.py", "PASS",
  f"{S}/run_graders.txt: 'run_graders E1: PASS (reference 50/50 seeds, slowest 0.2 s)'. Direct run on a workspace with the "
  "reference as market_structure.py and QF_SEED=0: '124 passed' (pytest -q --assert=plain -W error)."))
R(row("E1d-proj-autograder-instances", "2.6-autograder", f"{GR}instance.py", "PASS",
  CARRY % f"{GR}instance.py (no diff against the previous pin)" +
  " Docstring (gap 60..400, b in 1..3, c in 5..60, gap above 6b) matches the generator; round-7 ledger instance_orderings_r7.txt."))
R(row("E1d-proj-mutant-float-rounding", "2.6-mutation", f"{GR}test_project.py test_large_exact_inputs_round_from_exact_values; ledgers/E1/mutants/r6d_m01_*.py", "PASS",
  f"{S}/mutate_E1_seeds0-9_r8_final.txt: 'KILLED r6d_m01_half_up_in_float_wrong_for_large_inputs.py -> ...large_exact_inputs...[monopoly]' (seed 0)."))
for name, label in [("r6d_m02_profit_is_revenue_not_margin", "m02"), ("r6d_m03_a_must_cover_cost_twice", "m03"),
                    ("r6d_m04_welfare_takes_half_consumer_surplus", "m04"), ("r6d_m05_monopoly_fee_sign_error_on_cost", "m05")]:
    R(row(f"E1d-proj-mutant-new-{label}", "2.6-mutation", f"ledgers/E1/mutants/{name}.py", "PASS",
      f"{S}/mutate_E1_seeds0-9_r8_final.txt: KILLED {name}.py (seed 0)."))
R(row("E1d-proj-mutant-existing", "2.6-mutation", "ledgers/E1/mutants/*.py (107 prior mutants)", "PASS",
  f"{S}/mutate_E1_seeds0-9_r8_final.txt: 'mutate_graders E1: PASS (115/115 killed)' with --seeds 0-9 over all 115 files (107 prior and 8 new r8d_m01..m08). 0 SURVIVED lines."))
R(row("E1d-proj-alt-integer-pairs", "2.6-autograder", "ledgers/E1/scripts/E1-d-r6/alt1_integer_pairs.py", "PASS",
  f"{S}/alternatives_seeds0-49_r8.txt: 'alt1_integer_pairs: seeds passed=50 failed=0'. The page allows any exception or value for other invalid input, so no float-input test constrains it."))
R(row("E1d-proj-alt-cramer", "2.6-autograder", "ledgers/E1/scripts/E1-d-r6/alt3_cramer.py", "PASS",
  f"{S}/alternatives_seeds0-49_r8.txt: 'alt3_cramer: seeds passed=50 failed=0'."))
R(row("E1d-proj-alt-decimal", "2.6-autograder", "ledgers/E1/scripts/E1-d-r6/alt2_decimal_half_up.py", "PASS",
  f"{S}/alternatives_seeds0-49_r8.txt: 'alt2_decimal_half_up: seeds passed=50 failed=0'."))
R(row("E1d-proj-alt-trapezoid", "2.6-autograder", "ledgers/E1/scripts/E1-d-r6/alt4_trapezoid_consumer.py", "PASS",
  f"{S}/alternatives_seeds0-49_r8.txt: 'alt4_trapezoid_consumer: seeds passed=50 failed=0'."))
R(row("E1d-proj-r7-alternatives", "2.6-autograder", "ledgers/E1/scripts/alt1..alt5; E1-d-r7/alts/*.py; E1-d-r8/alts/*.py", "PASS",
  f"{S}/alternatives_seeds0-49_r8.txt: 13 candidates over seeds 0-49. Correct exact implementations pass 50/50: alt1_closed_form, alt3_linear_system, alt4_fraction_vertex, alt_r7_integer_arith, alt_r7_scaled_common_denominator, alt_r8_integer_half (integer half-up), alt_r8_simpson_consumer (Simpson on the linear integrand). Two float-based candidates fail on test_large_exact_inputs_round_from_exact_values, alt2_best_response and alt5_float_half_up; the page says each money output is an exact fraction, so these violate the rule and are not over-constraint."))
R(row("E1d-proj-pyodide-local", "2.6-browser", "tools/page_smoke.py --unit E1 --pages project", "PASS",
  "page_smoke E1: PASS; 'in-browser grader: All 124 tests pass on seed 2070576159'. Output in E1-d-r8/page_smoke.txt."))
R(row("E1d-proj-ruff-mypy", "2.6-gates", "tests/labs/E1; course/modules/E/E1/grader; repo", "PASS",
  f"{S}/ruff.txt: 'ruff format --check' 16 files already formatted; ruff check on tests/labs/E1 and grader is clean (its 2 E501 errors are in my scratch script ledgers/E1/scripts/E1-d-r8/make_r8_mutants.py, not in the repo). {S}/mypy.txt: 'Success: no issues found in 255 source files'."))
R(row("E1d-proj-check-gates", "2.6-gates", "tools/check_projects.py, check_pages.py, check_dag.py, run_labs.py, verify_refs.py, build_site", "PASS",
  f"{S}/check_projects.txt: 'check_projects E1: PASS'. check_pages.txt: 'PASS'. check_dag.txt: 'PASS'. run_labs.txt: 'PASS (12/12)'. verify_refs.txt (offline): '560 entries, 0 problems'. verify_refs_E1_live_r8.txt: '1 of 560 entries, 0 problems'. build_site was not re-run (see not-checked)."))
R(row("E1d-proj-reference-varian", "2.6-reference", "references/references.json key varian2014intermediate; project.html #reading", "PASS",
  f"{S}/verify_refs_E1_live_r8.txt: live re-verification of E1: 1 of 560 entries, 0 problems. references.json line 22009 carries the key. The Reading section (lines 567-573) states that no locator is confirmed, so no statement is attributed to it."))
R(row("E1d-proj-notation", "2.6-notation", "notation/notation.json; project.html math (345 \\( \\) spans)", "PASS",
  f"Math spans of project.html: the multiset of 345 spans is identical to the previous pin (checked by script). notation.json registers 8 symbols (T, Phi, gamma_3, gamma_4, R^*, R^{{e*}}, R_f, \\mathbb{{Q}}). The project uses plain a, b, c, d, Q, q, f, W, pi, e_k, none of them a registered symbol, so no reuse conflict."))
R(row("E1d-proj-banned", "2.6-prose", "course/modules/E/E1/project.html; cards.json", "PASS",
  "check_pages E1 PASS (banned strings, page contract). grep for process words in project.html and the labs/grader found only 'memo draft' (a task name at line 343)."))
R(row("E1d-proj-delta-r5", "2.4-delta", f"{PROJ} (hunks at lines 53, 390, 540); {CARDS}", "PASS",
  "Delta 7aa909e..ce7b382 read hunk by hunk. project.html: line 53 adds a pointer to Propositions 1 to 4; line 390 rewrites the C6 level-2 descriptor; line 540 changes the exemplar-B C6 annotation to quote it. No other hunk in the slice. Grader and project twins: no diff."))
R(row("E1d-proj-reading-section", "2.6-prose", f"{PROJ} section 'Reading' (lines 567-573)", "PASS",
  CARRY % f"{PROJ} lines 567-573 (no hunk in this range)" + " Reading section unchanged."))
R(row("E1d-proj-model-propositions-link", "2.6-prose", f"{PROJ} line 53; #model-propositions (line 281)", "PASS",
  "The new sentence links to id model-propositions (line 281), which holds Propositions 1 to 5. Labs 1 to 3 use the closed forms of Propositions 1 to 4 (Lab 1 interpretation line 127, Lab 3 interpretation line 256). Consistent."))
R(row("E1d-proj-l07-consistency", "2.6-cards-lesson", "course/modules/E/E1/L07.html Definitions 1.1 and 1.3; cards E1-c102..c104, c625-c640", "PASS",
  "Lesson 7 text changed in the delta (total surplus now defined in Definition 1.1 as CS+PS; DWL in Definition 1.3). Cards E1-c102 (wording), the total-surplus card and the DWL card agree with the new text (checked against lines 56-81 of L07.html)."))
R(row("E1d-proj-r7-mutants-new", "2.6-mutation", "ledgers/E1/mutants/r7v_m01..m05 (round-7 new mutants)", "PASS",
  f"{S}/mutate_E1_seeds0-9_r8_final.txt: all five KILLED (r7v_m01 by ...large_exact_inputs...[monopoly]; m02 by test_closed_form_matches[deadweight_loss_cents-monopoly]; m03 by welfare_cents-monopoly; m04 by profit_cents-bertrand; m05 by fee_cents-cournot)."))
R(row("E1d-proj-r7-collect-count", "2.6-count", f"{GR}test_project.py; {PROJ} Grading mode (line 322)", "PASS",
  "Collect-only count with QF_SEED=0 and market_structure = reference: '124 tests collected'. Page line 322 says 124. Equal."))
R(row("E1d-proj-r7-gates-lint", "2.6-gates", "repo", "PASS",
  "ruff, ruff format, mypy --no-incremental (repo), run_labs E1, run_graders E1, check_projects/pages/dag, verify_refs offline and live, page_smoke project, pytest tests/test_memo_exemplars.py and tests/test_labs.py -k E1: all pass (E1-d-r8/pytest_memo_labs_E1.txt)."))

# cards
samples = [f"E1-c{n:03d}" for n in range(10, 131, 10)]
for cid in samples:
    R(row(f"E1d-cards-sample-{cid[-3:]}", "2.3-cards", f"{CARDS} {cid}", "PASS",
      CARRY % f"{CARDS} object {cid} (JSON-equal to the previous pin; only E1-c071, c134, c135 removed and E1-c105 changed)" +
      " card text unchanged."))
R(row("E1d-cards-full-scan-duplicates", "2.3-cards", f"{CARDS} (132 cards)", "PASS",
  "Previous FAILs resolved. E1-c134 (repeat of c019) and E1-c135 (repeat of c034) removed; E1-c071 removed. E1-c100 and E1-c105 no longer share content (c105 now asks what Lab 1 checks). E1-c065 (monopoly price, quantity, profit, Lerner) and E1-c088 (volume, fee, profit under each structure) ask different questions. Pairwise difflib scan of all 8,646 pairs: the closest pairs are E1-c097/c098/c099, three different structures."))
R(row("E1d-cards-lab-graded", "2.3-cards", f"{CARDS} grade C cards", "PASS",
  "Count: 14 cards with grade C, each with a basis; 93 T; 25 cards with no grade field. Those 25 are definitional cards ('What is ...?'), and grades apply to claims (BUILDER_RULES grade rules), so no grade is required. Re-counted by script in this round."))
R(row("E1d-cards-numbers-in-lesson", "2.3-cards", f"{CARDS}; L01-L09.html", "PASS",
  CARRY % f"{CARDS} objects other than E1-c105" +
  " Fresh for E1-c105: the numbers 1, 2, 10, 97 and Q = d/2, 2d/3, d appear in L07 line 139 (hypothesis) and Part A (twin lines 8-11, 85, MIDPOINT_COUNTS line 32)."))
R(row("E1d-cards-labels-resolve", "2.3-cards", f"{CARDS} (all labels)", "FAIL",
  "cards_refs_r8.py: all labelled references resolve in their own lesson except E1-c102, which cites 'Section 3' for the misconception. In L07.html the misconceptions are Section 4 (line 323); Section 3 is 'Where the canon breaks' (line 313).",
  "Change 'Section 3' to 'Section 4' in the back of E1-c102 (cards.json) and regenerate if the card source is generated."))
R(row("E1d-cards-c102-section-locator", "2.3-cards", f"{CARDS} E1-c102 back", "FAIL",
  "The back reads '(the misconception that the monopoly profit is the deadweight loss; Section 3).' L07.html line 323 is '<h2 id=\"s4\">4 Misconceptions' and the item at line 326 is the one described. Locator is wrong. Present unchanged at the previous pin.",
  "Edit E1-c102 back: 'Section 3' -> 'Section 4'."))
R(row("E1d-cards-profit-sign-c019", "2.3-cards", f"{CARDS} E1-c019", "PASS",
  CARRY % f"{CARDS} object E1-c019"))
R(row("E1d-cards-hypotheses", "2.3-cards", f"{CARDS} E1-c023, E1-c041, E1-c075", "PASS",
  CARRY % f"{CARDS} objects E1-c023, E1-c041, E1-c075" + " Hypotheses carried in the back text."))
R(row("E1d-cards-delta-r5", "2.3-cards", f"{CARDS} (delta 7aa909e..ce7b382)", "PASS",
  "Delta read: E1-c071 removed (the monopoly reference case duplicate), E1-c105 reworded to the Lab 1 check (verified against twin lines 8-11, 85-93 and the L07 hypothesis line 139), E1-c134 and E1-c135 removed. No other card object changed (JSON compare)."))
R(row("E1d-cards-r7-new-c134-c135", "2.3-cards", f"{CARDS} E1-c134, E1-c135", "PASS",
  "Both cards removed in ce7b382. grep across curriculum, course, tools, tests, references, notation, plans finds no reference to E1-c071, E1-c134 or E1-c135."))
R(row("E1d-cards-lessons-tier", "2.3-cards", f"{CARDS}; L01-L09.html", "PASS",
  "Every card's lesson tag is one of L01..L09 and resolves to its page (cards_refs_r8.py). Note, not a rule breach: E1-c133 (lesson L04) sits after E1-c132 (lesson L09) at the end of the file; the previous pin had the same two out-of-order cards."))
R(row("E1d-cards-c105-basis", "2.3-cards", f"{CARDS} E1-c105 (basis)", "PASS",
  "Grade C; basis reads 'Lab 1, Parts A and B (exact arithmetic)' while the back cites 'Lab 1, Part A'. Part A verifies the claim (twin lines 82-93). The basis is a superset of the citation, not a false claim."))
R(row("E1d-cards-read-complete", "2.3-cards", f"{CARDS} (132 cards)", "UNVERIFIABLE",
  "Round 8 re-read every changed object and all delta hunks, and ran scripted checks over all 132 cards (duplicates, labels, grades, lesson tags). A full line-by-line re-read of all 132 cards against lesson text was not repeated this round, because the file changed only in the four objects listed above.",
  "Re-read all 132 cards against their current lesson text in a round whose scope is the whole cards file."))

mutants = []
for name, desc, killed in [
    ("r8d_m01_half_up_uses_builtin_round_ties_to_even.py", "half_up uses Python round(), ties to even: 70.5 prints 70",
     "test_tie_rounds_up_for_each_output[monopoly-fee_cents-8-1-1] (seed 0)"),
    ("r8d_m02_deadweight_measured_from_monopoly_volume.py", "deadweight loss measured from d/2 instead of d",
     "test_closed_form_matches[deadweight_loss_cents-monopoly] (seed 0)"),
    ("r8d_m03_monopoly_fee_uses_a_plus_c.py", "monopoly fee (a + c)/(2b): c in place of bc",
     "test_closed_form_matches[fee_cents-monopoly] (seed 0)"),
    ("r8d_m04_consumer_surplus_is_Q_times_gap_minus_Q.py", "consumer surplus Q(d-Q)/(2b)",
     "test_closed_form_matches[consumer_surplus_cents-cournot] (seed 0)"),
    ("r8d_m05_gap_forgets_the_factor_b.py", "gap d = a - c, forgetting b",
     "test_closed_form_matches[volume_trades-cournot] (seed 0)"),
    ("r8d_m06_cournot_fee_drops_b_on_cost.py", "Cournot fee (a + 2c)/(3b)",
     "test_closed_form_matches[fee_cents-cournot] (seed 0)"),
    ("r8d_m07_bertrand_volume_is_half_the_gap.py", "Bertrand volume d/2",
     "test_closed_form_matches[volume_trades-bertrand] (seed 0)"),
    ("r8d_m08_structure_message_names_two.py", "unknown-structure message names only monopoly and cournot",
     "test_unknown_structure_raises_value_error[duopoly] (seed 0)"),
]:
    mutants.append({"id": name, "description": desc, "killed_by": killed})

fragment = {
    "unit": "E1",
    "slice": "d",
    "round": 8,
    "verifier": "independent verifier (Haiku 5.5), round 8",
    "pin": PIN,
    "base": PREV,
    "checkout": str(ROOT),
    "scratch": "/tmp/e1d-r8-alt-* (removed after each run); /tmp/e1d-r8-ws (removed)",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice d: course/modules/E/E1/project.html, grader/ (reference, starter, instance, test_project), tests/labs/E1/lab-E1-project-{1,2,3}.py, cards.json (132 cards; 135 at the previous pin, minus E1-c071, E1-c134, E1-c135).",
        "Delta 7aa909e..ce7b382 read hunk by hunk: project.html (lines 53, 390, 540), cards.json (E1-c071, E1-c105, E1-c134, E1-c135), and the lesson changes that cards and the page cite (L07 Definitions 1.1 and 1.3, L07 lesson line 139). Grader and project lab twins are byte-identical to the previous pin.",
        "Mutation: tools/mutate_graders.py --unit E1 --seeds 0-9 over 115 files (107 prior + 8 new r8d): 115/115 killed (" + S + "/mutate_E1_seeds0-9_r8_final.txt). Earlier run with 112 files also all killed.",
        "Alternatives: 13 candidates over seeds 0-49 (" + S + "/alternatives_seeds0-49_r8.txt). 11 pass 50/50 (including 2 new correct ones); the 2 float-based candidates fail on the exact-fraction test, as the page's exact-fraction rule requires.",
        "Rubric: C6 level 2 gap and C3/C5 level 2 gaps are rubric-observability defects; exemplar scores are consistent with the rubric as written (blind re-score equals data-scores).",
        "Cards: E1-c102 locator error ('Section 3' should be 'Section 4') is the only card defect found by scripted cross-reference; c065 and c088 overlap in content but ask different questions.",
        "Not checked: full CI gate (pytest outside the E1 slice; tools/build_site.py not re-run); L01-L09, L08 and L09 labs and prose (other slices; L08 lab docstring and L09 quiz changed in the delta); full line-by-line re-read of all 132 cards (see E1d-cards-read-complete); live browser screenshot of the grader panel; the lab twin of L07 beyond run_labs.",
    ],
    "summary": "E1 slice d verdict FAIL. Fixed since round 7: float-rounding survivor (killed), float-input over-constraint removed, C6 level-2 wording now matches exemplar B, E1-c071/c134/c135 duplicates removed, E1-c105 reworded. Remaining FAILs: (1) C6 level 2 leaves a memo that names all three limits and changes for exactly two unplaceable (E1d-proj-rubric-structure); (2) C3 and C5 level-2 descriptors leave partial memos unplaceable (E1d-proj-rubric-C3-C5-level2); (3) E1-c102 cites Section 3 for the misconception, which is Section 4 (E1d-cards-c102-section-locator, E1d-cards-labels-resolve). E1d-cards-read-complete is UNVERIFIABLE (full re-read not repeated this round).",
}

out = ROOT / "ledgers/E1/E1-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
from collections import Counter
print("rows", len(rows), dict(Counter(r["status"] for r in rows)))
print("mutants", len(mutants))
