"""Verifier (round 17): builds ledgers/M7/M7-d.json from the round-17 checks. Rows are the verifier's own findings."""

import json
import re
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD17-M7-d")
S = "ledgers/M7/scripts/M7-d-r17/"
PIN = "aa6597255304919b9c4e5e5ca07763ae3e13d45c"
CARRY = "Carried from round 16 ({what} byte-identical since the previous pin e896b7a4):"

rows = []


def row(rid, check, location, evidence, status="PASS", fix=""):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


def carry(rid, check, location, what, extra=""):
    row(rid, check, location, CARRY.format(what=what) + " " + extra if extra else CARRY.format(what=what))


RUN = f"v17_run_graders_M7_0-49.log"
MUT = "v17_mutate_graders_M7_0-9_final.log"
LABS = "v17_run_labs_M7.log"
SMOKE = "v17_page_smoke_project.log"

# --- 2.6-spec / math / labs of the project page
carry("PRJ-D1-01", "2.6-spec", "course/modules/M/M7/grader/instance.py (make_instance)", "instance.py",
      f"Fresh: run_graders M7 seeds 0-49 PASS ({S}{RUN}); the reference accepts all 1,500 generator seeds with no failed certificate ({S}v17_sweep_20000rand_1500seeds.log).")
carry("PRJ-D1-02", "2.6-spec", "project.html:298-300; grader/test_project.py output_shape (now 180-207)",
      "project.html:298-300 and grader/test_project.py output_shape",
      "The page keys and the test's output_shape are unchanged (AST comparison of test_project.py: output_shape SAME); 347 collected and passing.")
carry("PRJ-D1-03", "2.4-math", "project.html:309", "project.html:309",
      "Line 309 is not in the changed-line set {55, 321, 326, 332, 450} (git diff -U0 e896b7a4 aa659725). Re-derived: sum|d_i| <= tau iff some t has t_i >= |d_i|, sum t_i <= tau.")
carry("PRJ-D1-04", "2.4-math", "project.html:310-313", "project.html:310-313",
      "Lines 310-313 not changed; re-derived dL/dw_i and dL/dt_i from L = f + sum lam_j g_j + nu(sum w - 1) (agrees with reference.py:305-311).")
carry("PRJ-D1-05", "2.4-math", "project.html:310,314-319; grader/test_project.py inequality_pairs (now 122-136)",
      "project.html:310,314-319 and test_project.py inequality_pairs", "Six inequality groups unchanged; inequality_pairs SAME by AST.")
carry("PRJ-D1-06", "2.4-math", "project.html:320; grader/test_project.py recomputed_certificate (now 160-171)",
      "project.html:320 and recomputed_certificate", "Line 320 (dual floor sentence) unchanged; recomputed_certificate SAME; the floor is applied in both (reference.py:289).")
row("PRJ-D1-07", "2.4-math", "project.html:317-321; test_project.py recomputed_certificate (160-171), assert_kkt (232-261)",
    "Re-verified: line 321 changed (now: tolerance 1e-8 on each certificate field; value agreement to 1e-9). test_project.py TOL = 1e-8 (line 38), agreement 1e-9 (test_certificate_agrees_with_the_recomputed_residuals), both functions SAME by AST. The reference passes all 50 seeds ({S}{RUN}).")
carry("PRJ-D1-08", "2.4-math", "project.html:323-325 (Proposition, T, proof)", "project.html:323-325",
      "Lines 323-325 unchanged; re-read: convexity of L in (w,t), f(y) >= L(y,s) >= L(w,t) = f(w), midpoint argument for uniqueness; hypotheses complete. Grade T supported.")
carry("PRJ-D1-09", "2.4-math", "project.html:325; grader/instance.py:3-4,39-43", "project.html:325 and instance.py",
      "Hypotheses match instance.py (Sigma = (A'A+I)/1000, SIMULATED label); instance.py byte-identical.")
row("PRJ-D1-10", "2.6-spec", "project.html:326; grader/reference.py _parse (now 56-111)",
    "Re-verified: project.html:326 changed (named-conditions sentence). Each named refusal in the current _parse raises ValueError: not a mapping (58), missing field (61), no assets (65), gamma not positive (68), turnover limit negative (71), sigma row count (74), sigma not square (77), not symmetric (79), not positive definite (81), w0/lower/upper length (86), lower above upper (88), sector label range (100), sector has no asset / cap without asset (103), start sum != 1 (105), start outside a bound (107), start breaks a sector cap (110). Non-finite values (44-45) raise ValueError. Other invalid inputs raise TypeError (wrong type) or are accepted with any exception by the suite.")
row("PRJ-D1-11", "2.6-spec", "grader/test_project.py NAMED_CONDITIONS (now 648-664), OTHER_SIDE_REFUSED (now 750-773)",
    "Re-verified: NAMED_CONDITIONS changed (the start-tolerance pairs replaced by equal-to-start and seed-case valid forms). Every invalid form is refused with ValueError and every valid form accepted on seeds 0-49 ({S}{RUN}); each invalid mutation is caught by the suite's named-condition tests in the mutation run ({S}{MUT}). OTHER_SIDE_REFUSED content unchanged (AST SAME).")
row("PRJ-D1-12", "2.6-spec", "project.html:326,332; test_project.py EXACT_BOUNDARIES (now 668-675), NAMED valid forms",
    "Re-verified: EXACT_BOUNDARIES now = lower-equals-start, upper-equals-start, cap-equals-start, gamma-just-inside-zero (gamma 1e-9). The start-sum-inside-low-side entry is removed. The page (line 332) names a bound or cap equal to the starting weight, a starting sum of exactly one, a turnover limit of zero and gamma of 1e-6 and 1e-9 as valid; each has a test that passes on the reference (347 passing on seeds 0-49).")
row("PRJ-D1-13", "2.5-lab", "project.html:53-168; tests/labs/M7/lab-M7-project-1.py",
    f"Re-verified: line 55 (hypothesis) changed to say step 2 holds at zero the assets with a negative budget-only weight. The twin computes held = [i for i if free[i] < 0] and prints 'step 2 assets held at zero: [2]' (matches the page expected block, project.html:157). Twin run under python -I -W error: step 1 weights 54/65, 5/26, -3/130, third weight negative, the bound binds at the answer (9/11, 2/11, 0). run_labs M7 PASS 11/11 ({S}{LABS}).")
carry("PRJ-D1-14", "2.5-lab", "project.html:170-285; tests/labs/M7/lab-M7-project-2.py", "project.html:170-285 and the Lab 2 twin",
      f"Lines unchanged and no diff in tests/labs/M7; run_labs M7 PASS 11/11 this round ({S}{LABS}).")
carry("PRJ-D1-15", "2.5-lab", "project.html:372-445; tests/labs/M7/lab-M7-project-3.py", "project.html:372-445 and the Lab 3 twin",
      f"Lines unchanged (the changed line 450 is outside); run_labs M7 PASS ({S}{LABS}).")
carry("PRJ-D1-16", "2.9-hours", "project.html:33,338-354; course/modules/M/M7/index.html:29; curriculum/01-foundations.yaml M7 hours 110",
      "project.html:33 and 338-354, index.html and the curriculum", "No diff in curriculum/ or index.html; hours split 77 + 33 unchanged.")
carry("PRJ-D1-17", "2.9-structure", "project.html:40-49", "project.html:40-49", "Lines unchanged.")
row("PRJ-D1-18", "2.6-spec", "project.html:288-336",
    "Re-verified: the changed lines 321, 326 and 332 are the statements checked in PRJ-D1-07, -10 and -12 (all agree with the suite: 347 tests, eight hand cases, tolerance 1e-8 on fields, exact start).")
row("PRJ-D1-19", "2.9-structure", "course/modules/M/M7/grader/ (instance.py, reference.py, starter.py, test_project.py)",
    f"Re-verified: all four files present; run_graders M7 PASS checks that the starter fails the suite ({S}{RUN}).")
row("PRJ-D1-20", "2.9-structure", "project.html; tools/page_smoke.py --unit M7 --pages project",
    f"page_smoke M7 PASS for project.html: in-browser grader 'All 347 tests pass' ({S}{SMOKE}).")
row("PRJ-D1-21", "2.4-notation", "project.html symbols vs notation/notation.json",
    "Re-verified on changed sentences (lines 55, 321, 326, 332, 450): no symbol outside notation/notation.json is introduced; the only changed symbol-bearing text is \\(10^{-8}\\) (unchanged form) and words.")
carry("PRJ-D1-22", "2.9-dag", "project.html:456 (envelope-theorem link); course/modules/M/M7/index.html",
      "project.html:456 and index.html", f"check_dag M7 PASS this round ({S}v17_check_dag_M7.log).")
row("PRJ-D1-23", "2.9-prose", "project.html; tools/check_pages.py BANNED list",
    f"check_pages M7 PASS ({S}v17_check_pages_M7.log); no banned phrase in the changed sentences (read).")
carry("PRJ-D1-24", "2.6-spec", "project.html:364-366 (local run and decode commands)", "project.html:364-366", "Lines unchanged.")
carry("PRJ-D1-25", "2.6-autograder", "grader/starter.py:18-20; project.html:301", "starter.py and project.html:301",
      "starter.py and line 301 unchanged.")
carry("PRJ-D1-26", "2.6-autograder", "grader/instance.py (make_instance)", "instance.py", "Byte-identical; seeds 0-49 pass.")
row("PRJ-D1-27", "2.6-autograder", "grader/test_project.py:37; grader/reference.py:23; project.html:300,321",
    "Re-verified: test_project.py:37 SEED; reference.py:23 REQUIRED (the old TOL line 23 is removed); project.html:300 unchanged; project.html:321 (1e-8 on fields) matches test_project.py TOL = 1e-8 (line 38).")
row("PRJ-D1-28", "2.6-autograder", "grader/test_project.py assert and pytest.fail messages (for example 1007, 1061, 1094, 1102, 1103, 1109)",
    "Re-verified: messages in the changed tests name the property ('the refusal must carry a message', 'allocate must not change the case it is given', ...) and print no expected value; the suite passes under --assert=plain -W error and under default pytest assertions (347 passed, seed 0).")
row("PRJ-D1-29", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke) and CPython (run_graders)",
    f"CPython: run_graders M7 seeds 0-49 PASS, reference 50/50 ({S}{RUN}). Pyodide: page_smoke PASS, 'All 347 tests pass' ({S}{SMOKE}).")
row("PRJ-D1-30", "2.5-lab", "tests/labs/M7/lab-M7-project-1..3.py; tests/test_labs.py -k M7",
    f"run_labs M7 PASS 11/11 ({S}{LABS}); pytest tests/test_labs.py -k M7: 11 passed, exit 0 ({S}v17_pytest_labs_M7.log).")
row("PRJ-D1-31", "2.6-spec", "project.html:332; grader/test_project.py HAND_CASES (now 280-337)",
    f"Re-verified: HAND_CASES has 8 entries (budget only, zero turnover, single asset, upper bound binding, turnover binding, degenerate box with zero turnover, turnover limit of one billionth, upper bound one billionth above the start). The page says eight (line 332). All 8 pass on seeds 0-49 ({S}{RUN}).")
row("PRJ-D1-32", "2.6-atlas", "project.html; curriculum/01-foundations.yaml M7 entry; check_projects --unit M7",
    f"check_projects M7 PASS ({S}v17_check_projects_M7.log).")
carry("PRJ-D1-33", "2.1-citations", "project.html:465-466 (reading list); references/references.json",
      "project.html:465-466 and references/references.json", "Lines unchanged; verify_refs --offline: 560 entries, 0 problems this round.")
row("PRJ-D1-34", "2.9-structure", "project.html:338-354; tools/check_pages.py --unit M7",
    f"check_pages M7 PASS ({S}v17_check_pages_M7.log); lines 338-354 unchanged.")
row("PRJ-D1-35", "2.6-mutation", "ledgers/M7/mutants/ (all files)",
    f"tools/mutate_graders.py --unit M7 --seeds 0-9: PASS (215/215 killed) ({S}{MUT}). The three new mutants v17_01..03 are included.")
row("PRJ-D1-36", "2.6-mutation", "ledgers/M7/mutants/ (all families)",
    f"Same run: every file in ledgers/M7/mutants/ is KILLED (215 of 215) ({S}{MUT}).")
row("PRJ-D1-37", "2.6-mutation", "ledgers/M7/equivalent/r04_budget_left_out_of_primal_residual.py; ledgers/M7/equivalent/README.md proof 6 and F0",
    "Re-verified under ruling 35 (the starting portfolio is exactly feasible). (a) reference.py:104-110 refuses any start whose sum, bounds or caps are off exactly; the search starts at w0 (reference.py:203) and budget.p = 0 keeps the sum exactly one (F0). (b) All 3,050 cases (seeds 0-49 and 3,000 page-valid random exact-decimal cases) give 0 differences between r04 and the reference in every output field, and the reference's exact budget gap is 0 on every answer ({S}v17_equiv_3050.log). The B1 start of the round-16 row is outside the contract (ruling 35), so the equivalence rests on the exact-start contract, as the README states. Retraction of the round-14 record is in place (ledgers/M7/mutant_equivalence_r14.json).")
row("PRJ-D1-38", "2.6-autograder", "ledgers/M7/scripts/M7-d-r12fix/methods/alt_2_pg, alt_3_admm, alt_4_ipm, alt_5_dual; M7-d-r11/alts/alt2, alt6, alt9; M7-d-r12/alts/alt_r12_1, alt_r12_2; M7-d-r10/alts/alt_B, alt_J",
    f"Five correct alternatives of different styles pass seeds 0-49 on the current 347-check suite (50/50 each, {S}v17_alts_all_seeds0-49.log): projected gradient (alt_2_pg), ADMM (alt_3_admm), interior point (alt_4_ipm), dual ascent (alt_5_dual) (ruling 19 front ends; the front-end KKT path is used on 13, 45, 45 and 41 of seeds 0-49, the active-set fallback otherwise), and scaled float with exact polish (r11 alt6, alt9). Exact active-set variants alt2, alt_r12_1, alt_r12_2, alt_B, alt_J also pass. Failing candidates fail on page-valid inputs, not on over-constraint: the exact candidates alt1, alt8, alt_G, alt_H, alt_I and the round-14 alt1 and alt3 (ADMM) return the start (0.5, 0.5) on 'upper bound one billionth above the start' (certified complementary slackness 1e-6; the worked answer (0.5+1e-9, 0.5-1e-9) has a strictly lower objective); the round-14 alt4 (interior point) returns the start on 'turnover limit of one billionth' (complementary slackness 5e-7); float candidates raise RuntimeError on the gamma 1e-9 boundary (for example alt_r12_3, seed 1, 'working set dependent'). The suite does not over-constrain.")
row("PRJ-D1-39", "2.9-structure", "BLUEPRINT.md:400-401; course/modules/M/M7/grader/reference.py; .github/workflows/ci.yml",
    "Note only (ruling 4): no deploy step exists; BLUEPRINT.md and .github/workflows/ci.yml have no diff since e896b7a4. Recorded for the owner, not a defect of this slice.")

# --- previous-round rows, re-verified or carried
carry("PRJ-R4-01", "2.9-prose", "grader/test_project.py docstrings and messages",
      "grader/test_project.py docstrings and messages of the unchanged tests",
      "Docstrings of the changed tests re-read this round (exact_sum; _lower_just_above_upper, whose docstring says the start lies below its lower bound: upper = w0 < lower = w0 + 1e-12, true; _lower_above_upper_last_asset; _start_above_upper_last_asset).")
carry("PRJ-R5-01", "2.4-math", "project.html:456 frontier bullet", "project.html:456", "Line unchanged.")
carry("PRJ-R5-02", "2.6-spec", "grader/test_project.py comments and messages (old 275, 277, 295-296, 301, 303-305; now +6)",
      "the comments and messages at those lines", "No hunk above old line 327 except the +6-line helper insertion.")
row("PRJ-R5-03", "2.9-prose", "project.html:450 ('does not test' paragraph)",
    "Re-verified: the changed paragraph still states that no case reads a data file and that every case carries the SIMULATED label (instance label and every hand-case label, test_project.py hand_case base).")
carry("PRJ-R5-04", "2.9-structure", "project.html:349-350", "project.html:349-350", "Lines unchanged.")
row("PRJ-R5-05", "2.6-mutation", "ledgers/M7/mutants/r5_01..r5_05", f"Killed in {S}{MUT}.")
row("PRJ-R6-01", "2.6-gate", "tools/check_projects.py --all (M7 entry)", f"check_projects M7 PASS ({S}v17_check_projects_M7.log).")
row("PRJ-R6-02", "2.6-gate", "tools/check_pages.py --all (M7 entry)", f"check_pages M7 PASS ({S}v17_check_pages_M7.log).")
row("PRJ-R6-03", "2.9-dag", "tools/check_dag.py --all (M7 entry)", f"check_dag M7 PASS ({S}v17_check_dag_M7.log).")
carry("PRJ-R7-01", "2.6-mutation", "grader/test_project.py degenerate box hand case (lines before old 327 unchanged); mutants r7_06_*",
      "the degenerate box hand case", f"Mutants killed in {S}{MUT}.")
carry("PRJ-R7-02", "2.9-prose", "grader/test_project.py:295-296 comment", "the comment at old 295-296", "Text unchanged.")
row("PRJ-R7-03", "2.9-prose", "grader/test_project.py position-group comment (old 916-921, now 920-926)",
    "Re-verified: the comment changed; it now names the start-outside-a-bound and start-on-a-bound tests, and the test names match (test_start_outside_a_bound_is_refused_at_every_position, test_start_on_a_bound_is_accepted_at_every_position).")
row("PRJ-R7-04", "2.6-mutation", "ledgers/M7/mutants/r7_01..r7_05", f"Killed in {S}{MUT}.")
row("PRJ-R7-05", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke)", f"page_smoke PASS ({S}{SMOKE}).")
row("PRJ-R7-06", "2.8-data", "project.html; grader/instance.py", f"instance.py byte-identical; page_smoke PASS ({S}{SMOKE}).")
carry("PRJ-R7-07", "2.6-hours", "project.html:344-350", "project.html:344-350", "Lines unchanged.")
carry("PRJ-R8-01", "2.6-autograder", "grader/test_project.py _observed_call (now 66-83), purity tests (now 1090-1094), every_allocate_call_is_pure (now 87-110)",
      "_observed_call, every_allocate_call_is_pure and test_allocate_does_not_change_its_argument", "AST SAME.")
carry("PRJ-R8-02", "2.6-autograder", "grader/test_project.py test_the_same_case_gives_the_same_answer (now 1106-1109)",
      "test_the_same_case_gives_the_same_answer", "AST SAME.")
row("PRJ-R8-03", "2.6-mutation", "ledgers/M7/mutants/v8_03_budget_multiplier_zero_when_start_is_optimal.py", f"Killed in {S}{MUT}.")
carry("PRJ-R8-04", "2.6-spec", "grader/test_project.py hand cases before old line 327 (now about 302-317)",
      "the hand cases above old line 327", "Text unchanged; the removed entries start at old 327.")
carry("PRJ-R9-01", "2.6-autograder", "grader/test_project.py _observed_call (now 66-83) vs pytest.raises(Exception) tests",
      "_observed_call and the pytest.raises(Exception) tests", "AST SAME.")
carry("PRJ-R9-02", "2.9-prose", "grader/test_project.py purity fixture docstring (now 66-110)", "the purity fixture", "AST SAME.")
carry("PRJ-R9-03", "2.6-autograder", "grader/test_project.py @wraps decorator (now 87-110) and the block at old 319-326",
      "the @wraps decorator and the block at old 319-326", "Lines before old 327 unchanged.")
carry("PRJ-R9-04", "2.9-prose", "project.html:167 (Lab 1 interpretation)", "project.html:167",
      f"Line unchanged; it says step 2 holds at zero the weight that the prediction names, which matches the changed hypothesis (line 55) and the twin output.")
carry("PRJ-R9-05", "2.4-math", "project.html:324 (proof)", "project.html:324", "Line unchanged.")
row("PRJ-R9-06", "2.6-autograder", "ledgers/M7/scripts/M7-d-r11/alts/ and alts_suite_r11*.log",
    "Re-run this round on the current suite: alt6 and alt9 pass 50/50 and alt2 passes 50/50 (" + S + "v17_alts_all_seeds0-49.log). See PRJ-D1-38.")
row("PRJ-R9-07", "2.6-mutation", "ledgers/M7/mutants/ (final folder)", f"215 files, all KILLED ({S}{MUT}).")
row("PRJ-R9-08", "2.9-structure", "grader/test_project.py (collected count); project.html:332",
    f"Collected 347 on every seed 0-49 ({S}v17_collect_seeds0-49.log); project.html:332 says 347.")
row("PRJ-R9-09", "2.5-lab", "project.html:53-285, 372-445; tests/labs/M7/lab-M7-project-1..3.py", f"run_labs M7 PASS 11/11 ({S}{LABS}).")
row("PRJ-R9-10", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke)", f"page_smoke PASS, 347 in-browser ({S}{SMOKE}).")
carry("PRJ-R9-11", "2.9-prose", "grader/test_project.py hand-case comments (old 274-311)", "the hand-case comments above old line 327",
      "Text unchanged.")
row("PRJ-R10-01", "2.6-autograder", "ledgers/M7/scripts/M7-d-r10/alts/ alt_B, alt_G, alt_H, alt_I, alt_J",
    f"Re-run: alt_B and alt_J pass 50/50 ({S}v17_alts_all_seeds0-49.log). alt_G, alt_H, alt_I fail 0/50 but are wrong, not over-constrained: on 'upper bound one billionth above the start' they return (0.5, 0.5), certified with complementary slackness 1e-6 (suite rejects it); the worked answer (0.5+1e-9, 0.5-1e-9) has a strictly lower objective. See PRJ-D1-38.")
row("PRJ-R10-02", "2.6-autograder", "ledgers/M7/scripts/M7-d-r10/alts/ alt_A, C, D, E, F (float alternatives)",
    f"Re-run this round: each fails 0/50 ({S}v17_alts_all_seeds0-49.log) on page-valid inputs: the gamma boundary tests (RuntimeError 'working set dependent' or 'did not converge', a scale-dependent cutoff) and the one-billionth hand cases (the start returned, certified complementary slackness 5e-7 or 1e-6). Under ruling 10 these are mutants, not alternatives; the suite is right to reject them.")
row("PRJ-R10-03", "2.6-mutation", "ledgers/M7/mutants/r10_01..r10_03", f"Killed in {S}{MUT}.")
row("PRJ-R10-04", "2.6-autograder", "ledgers/M7/mutants/ full set", f"215 of 215 killed ({S}{MUT}).")
row("PRJ-R10-05", "2.6-autograder", "tools/run_graders.py --unit M7 --seeds 0-49; mypy strict on the grader",
    f"run_graders M7 PASS ({S}{RUN}); mypy --no-incremental on the repository: no issues in 385 files ({S}v17_mypy_repo.log).")
row("PRJ-R10-06", "2.9-structure", "repo gates: ruff check ., ruff format --check ., mypy --no-incremental, verify_refs --offline",
    f"ruff check . PASS ({S}v17_ruff_check_repo.log); ruff format --check . PASS, 554 files ({S}v17_ruff_format_repo.log); mypy PASS ({S}v17_mypy_repo.log); verify_refs --offline: 560 entries, 0 problems ({S}v17_verify_refs_offline.log).")
row("PRJ-R11-01", "2.6-autograder", "over-constraint: ledgers/M7/scripts/M7-d-r11/alts/ (nine solvers)",
    "Re-run: alt2, alt6, alt9 pass 50/50; alt1 and alt8 fail on the billionth-start cases (wrong answers, see PRJ-R10-01); alt3, alt4, alt5, alt7 pass 48, 41, 46, 49 of 50 and fail only on the gamma boundary tests (float defects on page-valid gamma; see PRJ-R10-02). Five correct alternatives pass (PRJ-D1-38).")
row("PRJ-R11-02", "2.6-mutation", "ledgers/M7/mutants/r11_01, r11_03, r11_05, r11_06", f"Killed in {S}{MUT}.")
row("PRJ-R11-03", "2.6-spec", "project.html:326 (gamma valid form) vs test_project.py EXACT_BOUNDARIES and NAMED_CONDITIONS",
    "Re-verified: the page names gamma of 1e-6 and 1e-9 as valid; NAMED_CONDITIONS uses gamma 1e-6 (gamma-positive-negative boundary) and EXACT_BOUNDARIES uses gamma 1e-9 (gamma-just-inside-zero); both pass on the reference.")
row("PRJ-R11-04", "2.6-autograder", "grader/test_project.py assertion style under default pytest mode",
    "Re-run this round with default pytest assertions (no --assert=plain) and -W error on seed 0: 347 passed.")
row("PRJ-R12-01", "2.6-autograder", "grader/instance.py (make_instance) seeds 0-49", f"run_graders M7 seeds 0-49 PASS ({S}{RUN}).")
row("PRJ-R12-02", "2.6-autograder", "plans/M7-build-plan.md section 7.4 item 2 (five alternatives, different methods)",
    "Four front-end methods (projected gradient, ADMM, interior point, dual ascent; ruling 19) each pass 50/50 on the current suite, with the active-set fallback on the other seeds; with the scaled float exact-polish alternative, five alternatives of different style pass (PRJ-D1-38).")
row("PRJ-R12-03", "2.6-autograder", "over-constraint check: exact and float active-set alternatives on seeds 0-49",
    f"Re-run this round ({S}v17_alts_all_seeds0-49.log): every failing alternative is wrong on a page-valid input (one-billionth cases return the start with complementary slackness 1e-6 or 5e-7; float candidates fail at the gamma boundary tests). No correct alternative is rejected.")
row("PRJ-R12-04", "2.6-autograder", "over-constraint check: float alternatives r12 alt 3-7 (solver defects on valid gamma inputs)",
    f"Re-run: alt_r12_3..7 pass 37-41 of 50; each failure is on the valid gamma = 1e-9 or 1e-6 boundary tests (RuntimeError 'working set dependent' or certificate). Defects of the alternatives, not over-constraint ({S}v17_alts_all_seeds0-49.log).")
row("PRJ-R12-05", "2.6-mutation", "new student-error mutants v12_02, v12_03, v12_04, v12_05 (ledgers/M7/mutants/)", f"Killed in {S}{MUT}.")
row("PRJ-R12-06", "2.6-mutation", "equivalence proof: v12_01 (dual residual reported without the floor at zero)",
    "ledgers/M7/equivalent/v12_01 has the same code as q04 (only the docstring differs; dual = -min at line 291). Proof 1: min over inequality multipliers is 0 on every reference answer (F2), so the two reports are both 0. 0 differences of 3,050 cases ({S}v17_equiv_3050.log).")
row("PRJ-R12-07", "2.6-autograder", "grader/test_project.py collect-only, seeds 0-49", f"347 collected on every seed 0-49 ({S}v17_collect_seeds0-49.log).")
row("PRJ-R12-08", "2.5-lab", "project.html lab code and expected blocks vs tests/labs/M7/lab-M7-project-1..3.py", f"run_labs M7 PASS ({S}{LABS}).")
row("PRJ-R12-09", "2.4-math", "project.html Lab 1 and Lab 3 printed numbers",
    f"Lab 1 twin output (54/65, 5/26, -3/130; held [2]; 9/11, 2/11, 0; nu -21/1100; objective -3/220) matches the page expected block; run_labs PASS ({S}{LABS}). Lab 3 unchanged.")
carry("PRJ-R12-10", "2.4-math", "project.html:323-325 Proposition (grade T)", "project.html:323-325", "Lines unchanged; proof re-read.")
carry("PRJ-R12-11", "2.6-spec", "project.html:292-300 inputs and outputs vs instance.py and test_project.py",
      "project.html:292-300, instance.py and output_shape", "Lines unchanged.")
row("PRJ-R12-12", "2.6-spec", "project.html:326 named conditions vs test_project.py tables",
    "Re-verified: the page's named list (line 326) matches _parse (see PRJ-D1-10) and the NAMED and EXACT tables (see PRJ-D1-11, -12); the valid forms are the boundary or the seed case as the page says.")
row("PRJ-R12-13", "2.6-autograder", "Pyodide timing (plan 7.4; BUILDER_RULES 5.3.4)",
    f"In-browser suite: 347 tests, 6.7 s on the page_smoke seed ({S}{SMOKE}), within the 60 s suite limit. Per-test in-browser time not measured separately (noted, not a row failure).")
carry("PRJ-R12-14", "2.1-citations", "project.html:465-466 reading list keys", "project.html:465-466 and references/references.json", "Lines unchanged.")
carry("PRJ-R12-15", "2.9-dag", "project.html:310 'defined in Lesson 3' link", "project.html:310", "Line unchanged; check_dag M7 PASS this round.")
row("PRJ-R14-01", "2.6-mutation", "ledgers/M7/mutant_equivalence_r14.json; ledgers/M7/equivalent/",
    "The r04 entry of the round-14 record carries status 'retracted in round 16 (ruling 35)' and a retraction text, and the equivalence now rests on README proof 6 under the exact-start contract. That contract is verified (PRJ-D1-37: 0 differences of 3,050 cases, exact budget gap 0). The record and the folder agree.")
carry("PRJ-R14-02", "2.4-math", "project.html:167, 172, 310 (multiplier references) vs project.html:310 Conventions",
      "project.html:167, 172 and 310", "Lines unchanged; line 167 matches the step-2 hypothesis.")
carry("PRJ-R14-03", "2.5-lab", "project.html:444 (Lab 3 interpretation) vs project.html:412 and the printed line",
      "project.html:412 and 444", "Lines unchanged; run_labs PASS.")
row("PRJ-R14-04", "2.5-lab", "project.html:169-285 (Lab 2) completion blanks vs twin tests/labs/M7/lab-M7-project-2.py",
    f"run_labs M7 PASS: the Lab 2 page code equals the twin and the expected blocks equal the twin's output ({S}{LABS}).")
row("PRJ-R14-05", "2.6-mutation", "ledgers/M7/mutants/w14d_01..w14d_03", f"Killed in {S}{MUT}.")
row("PRJ-R14-06", "2.6-autograder", "grader/test_project.py: 347 checks, identical for every seed (project.html:332)",
    f"Collected 347 on every seed 0-49 ({S}v17_collect_seeds0-49.log); project.html:332 says 347.")
row("PRJ-R14-07", "2.6-autograder", "project.html:450 'every case carries the SIMULATED label'",
    "Re-verified: every make_instance label and every hand_case base label carries 'SIMULATED'.")
row("PRJ-R14-08", "2.6-autograder", "project.html:326 'other invalid inputs... raise an exception that carries a message'",
    "Re-verified: the sentence is unchanged in substance; test_wrong_type_is_refused_with_an_exception and the other-invalid tests assert that the exception carries a message (test_project.py:1007, 1061).")
row("PRJ-R14-09", "2.6-rubric", "curriculum/01-foundations.yaml:327 (grading autograder); tools/check_projects.py rubric block",
    f"check_projects M7 PASS ({S}v17_check_projects_M7.log); no diff in curriculum/.")
row("PRJ-R14-10", "2.6-atlas", "curriculum/meta.yaml atlas block; project.html", f"check_projects M7 PASS ({S}v17_check_projects_M7.log); no diff in curriculum/.")
carry("PRJ-R14-11", "2.9-hours", "project.html:344-350 (verifier estimate)", "project.html:344-350", "Lines unchanged.")
row("PRJ-R14-12", "2.6-gate", "tools/check_pages.py --unit M7; tools/check_dag.py --unit M7; tools/check_projects.py --unit M7",
    f"All three PASS this round ({S}v17_check_pages_M7.log, v17_check_dag_M7.log, v17_check_projects_M7.log).")
row("PRJ-R14-13", "2.6-autograder", "Pyodide per-test time (plan 7.3: under 5 s each, 60 s per suite)",
    f"In-browser suite 6.7 s for 347 tests ({S}{SMOKE}). Per-test not separately timed (noted).")
row("PRJ-R14-14", "2.6-autograder", "run_labs --unit M7; pytest tests/test_labs.py -k M7",
    f"run_labs M7 PASS 11/11 ({S}{LABS}); pytest tests/test_labs.py -k M7: 11 passed ({S}v17_pytest_labs_M7.log).")
row("PRJ-R14-15", "2.6-autograder", "over-constraint: the five alternatives of plan 7.4.2 (ruling 19)",
    "Five correct alternatives pass 50/50 on seeds 0-49 (PRJ-D1-38), including the four ruling-19 front ends. The four front-ends are the named methods of plan 7.4.2.")
row("PRJ-R14-16", "2.6-autograder", "over-constraint: ledgers/M7/scripts/M7-d-r14/alts/ (five and five repaired)",
    f"Re-run: the repaired float alternatives A, C, D, E, F fail 0/50 on page-valid inputs (gamma boundary tests and one-billionth hand cases; defects, PRJ-R10-02); the five-set requirement is met by other alternatives (PRJ-D1-38). ({S}v17_alts_all_seeds0-49.log)")
carry("PRJ-R14-18", "2.1-citations", "references/references.json (boyd2004convex, stokey1989recursive)",
      "references/references.json", "No diff; verify_refs --offline 560 entries, 0 problems this round.")
row("PRJ-R15-01", "2.6-autograder", "course/modules/M/M7/grader/reference.py:206 (initial working set, exact zero slack) and :1-8 docstring",
    "Re-verified at the new location: the initial admission requires b - a.x == 0 exactly (reference.py:206), and the docstring (lines 1-12) now states the exact start (no snapping).")
row("PRJ-R15-02", "2.6-mutation", "ledgers/M7/equivalent/r05_turnover_total_slackness_term_zeroed.py; v10_02_complementary_slackness_signed_not_absolute.py; README proofs 7 and 8",
    f"Proofs 7 and 8 re-read against reference.py:279-300 and F5. 0 differences of 3,050 exact-start cases for both files ({S}v17_equiv_3050.log).")
row("PRJ-R15-03", "2.6-mutation", "ledgers/M7/mutants/r15_01..r15_03", f"Killed in {S}{MUT}.")
row("PRJ-R15-04", "2.6-mutation", "ledgers/M7/equivalent/ (q04, r02, r04, s12_03, v10_01, v11_01, v12_01)",
    f"All seven: 0 differences from the reference on 3,050 exact-start cases ({S}v17_equiv_3050.log). r04 is equivalent under ruling 35 (PRJ-D1-37).")
row("PRJ-R16-01", "2.6-autograder", "course/modules/M/M7/grader/reference.py (fallback snapping removed; _parse exact; docstring 8-10)",
    f"Re-verified: the snapping path is gone (reference.py:203 starts at w0; no fallback to an unsnapped start). 21,500 page-valid cases (1,500 generator seeds and 20,000 random exact-decimal cases) give 0 certificate failures at 1e-8 with the independent recomputation (v17_sweep.py; a negative control rejects perturbed outputs, v17_control.py). The docstring now matches (reference.py:8-10).")
row("PRJ-R16-02", "2.6-mutation", "ledgers/M7/equivalent/v16d_01_snap_ignores_sector_caps.py, v16d_02_turnover_guard_dropped_from_snap.py, v16d_03_sector_excess_all_from_first_member.py",
    f"Under ruling 35 these differ from the reference only on starts the exact contract refuses; 0 differences of 3,050 exact-start cases ({S}v17_equiv_3050.log). Proof 9 of the README.")
row("PRJ-R16-03", "2.9-structure", "project.html:332 counts vs test_project.py HAND_CASES and collect-only",
    "Eight hand cases in HAND_CASES; 347 collected; the page says eight and 347.")
row("PRJ-R16-04", "2.9-prose", "grader/test_project.py new hand-case comments (HAND_CASES, now 316-337)",
    "Re-derived the numbers in the comments: 'turnover limit of one billionth' -> the start in place has complementary slackness |kappa * 1e-9| with kappa = 500 (optimal ν = 499.5), i.e. 5e-7 (the comment says about 5e-7); 'upper bound one billionth above the start' -> u0 = 1000 and 1000 * 1e-9 = 1e-6 (the comment says about 1e-6). Worked answers match the reference's outputs.")

# --- mutants: the 215 files of ledgers/M7/mutants, from the final run log
mutants = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+?): (.*?) -> (.*)$")
for line in (ROOT / S / MUT).read_text(encoding="utf-8").splitlines():
    m = pat.match(line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    if status == "KILLED":
        mutants.append({"id": name, "description": desc, "killed_by": killed})
    else:
        mutants.append({"id": name, "description": desc, "killed_by": ""})

fragment = {
    "unit": "M7",
    "slice": "d",
    "round": 17,
    "verifier": "Haiku 5.5 independent verifier (round 17, slice d, delta verification); did not build M7-d",
    "pin": PIN,
    "base": "e896b7a4 (round-16 pin; fragment /Users/billyribeiro/.fanout/frags/D-M7-d.round16.json, context only)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD17-M7-d",
    "scratch": "ledgers/M7/scripts/M7-d-r17/ (helpers v17_lib.py, v17_sweep.py, v17_equiv.py, v17_run_parallel.py; work dirs under /private/tmp/v17m7d-*)",
    "verified_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta e896b7a4..aa659725 for slice d: project.html lines 55, 321, 326, 332, 450; grader/reference.py (exact start, snapping removed, TOL removed); "
        "grader/test_project.py (start-tolerance tests replaced by exact-boundary tests; HAND_CASES 12 -> 8; 370 -> 347 checks); "
        "ledgers/M7/equivalent/ (18 files with README, r04 and the snapping-path mutants); ledgers/M7/mutants/ (three new v17_01..03, all killed). "
        "Ruling 35 (exact starting portfolio) applied; rulings 4, 9, 10, 19, 22, 25 read. "
        "Counts: 215 mutants killed by mutate_graders --unit M7 --seeds 0-9 (no survivor). Equivalence: 18 files, 0 differences of 3,050 cases, exact budget gap 0 on every reference answer. "
        "Alternatives: 51 candidates re-run on seeds 0-49; passing: alt_2_pg, alt_3_admm, alt_4_ipm, alt_5_dual, alt6 and alt9 (r11), alt2, alt_r12_1, alt_r12_2, alt_B, alt_J. "
        "Observations (not rows): alt_2_pg and alt_5_dual take about 42 s per suite run alone on seed 1 (60 s limit), mostly in the active-set fallback. "
        "Not checked: the live Crossref run (verify_refs without --offline); the deploy configuration (ruling 4); the full repository pytest (only tests/test_labs.py -k M7); "
        "cards (outside slice d); Pyodide per-test timing (only the suite total is measured in page_smoke); the r16/r16fix logs of the builders were not re-used as evidence."
    ),
    "summary": {},
}
counts = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": sum(r["status"] == "FAIL" for r in rows)}
fragment["summary"] = {**counts, "mutants": len(mutants), "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
                       "equivalent_files": 18}
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", counts, "mutants", fragment["summary"]["mutants"], "killed", fragment["summary"]["mutants_killed"])
