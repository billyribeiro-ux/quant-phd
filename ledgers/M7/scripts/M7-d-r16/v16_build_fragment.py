"""Round-16 verifier: assemble ledgers/M7/M7-d.json (slice d, round 16) from the rows and logs of this round.

Mutant entries are read from the mutate_graders log of this round (v16_mutate_graders_M7_0-9.log). Run from the
repository root: .venv/bin/python -I ledgers/M7/scripts/M7-d-r16/v16_build_fragment.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path.cwd()
S = "ledgers/M7/scripts/M7-d-r16/"
CARRY = "Carried from round 15 (subject byte-identical since the previous pin dde0486b): "
CARRY_D1 = "Carried from round 15 (the cited subject is byte-identical since the previous pin dde0486b): "

P = "PASS"
F_ = "FAIL"
rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


# ---- slice-d rows of round 15 (PRJ-D1-xx) ----
row("PRJ-D1-01", "2.6-spec", "course/modules/M/M7/grader/instance.py (make_instance)", P,
    CARRY_D1 + "instance.py. 50 seeds deterministic, labelled SIMULATED and feasible (instances50_collect50_r15.py, "
    "round 15); run_graders.py --unit M7 --seeds 0-49 PASS this round (" + S + "v16_run_graders_M7_0-49.log).")
row("PRJ-D1-02", "2.6-spec", "project.html:298-300; grader/test_project.py output_shape (174-201)", P,
    CARRY_D1 + "project.html:298-300 and test_project.py:174-201 (the only project.html hunks are lines 332 and 450, "
    "the only test_project.py hunk is the HAND_CASES insertion after line 311). The three keys, seven multiplier keys, "
    "four certificate keys and list lengths match.")
row("PRJ-D1-03", "2.4-math", "project.html:309", P,
    CARRY_D1 + "project.html:309 unchanged. Re-derived: sum|d_i| <= tau iff some t has t_i >= |d_i|, sum t_i <= tau.")
row("PRJ-D1-04", "2.4-math", "project.html:310-313", P,
    CARRY_D1 + "project.html:310-313 unchanged. Re-derived dL/dw_i and dL/dt_i from L = f + sum lam_j g_j + nu(sum w - 1).")
row("PRJ-D1-05", "2.4-math", "project.html:310,314-319; grader/test_project.py inequality_pairs (116-130)", P,
    CARRY_D1 + "six inequality groups identical to inequality_pairs (116-130), which the delta does not touch.")
row("PRJ-D1-06", "2.4-math", "project.html:320; grader/test_project.py recomputed_certificate (154-165)", P,
    CARRY_D1 + "project.html:320 (dual floor) and recomputed_certificate (154-165) unchanged; the floor is applied in both.")
row("PRJ-D1-07", "2.4-math", "project.html:317-321; test_project.py recomputed_certificate (154-165), assert_kkt (226-255)", P,
    CARRY_D1 + "the four fields and tolerances (1e-8 bounds, 1e-9 agreement) agree; the functions are unchanged.")
row("PRJ-D1-08", "2.4-math", "project.html:323-325 (Proposition, T, proof)", P,
    CARRY_D1 + "lines 323-325 unchanged; re-read this round: convexity of L in (w,t), f(y) >= L(y,s) >= L(w,t) = f(w), "
    "midpoint argument for uniqueness; hypotheses complete. Grade T supported.")
row("PRJ-D1-09", "2.4-math", "project.html:325; grader/instance.py:3-4,39-43", P,
    CARRY_D1 + "hypotheses match instance.py (Sigma = (A'A+I)/1000, SIMULATED label).")
row("PRJ-D1-10", "2.6-spec", "project.html:326; grader/reference.py _parse (old lines 54-109)", P,
    CARRY_D1 + "project.html:326 unchanged; reference.py _parse is outside every changed hunk (hunks at old lines 5-9, 18-24, "
    "192-207). Each named refusal in _parse raises ValueError.")
row("PRJ-D1-11", "2.6-spec", "grader/test_project.py NAMED_CONDITIONS (now 714-728), OTHER_SIDE_REFUSED (now 831-854)", P,
    CARRY_D1 + "tables unchanged (content at old 637-651 and 754-777, shifted by the +77 HAND_CASES insertion). "
    "Other invalid inputs accept any Exception with a message.")
row("PRJ-D1-12", "2.6-spec", "project.html:326,332; test_project.py EXACT_BOUNDARIES (now 751-757), NAMED valid forms", P,
    "Re-read this round: project.html:332 (\"a bound or a cap equal to the starting weight, and a starting sum inside "
    "the tolerance on either side\") against EXACT_BOUNDARIES = lower-equals-start, upper-equals-start, cap-equals-start, "
    "start-sum-inside-low-side, gamma-just-inside-zero, and the high-side start sum in the NAMED valid forms. "
    "test_named_condition_boundary_is_accepted and test_named_exact_boundary_is_accepted pass on the reference "
    "(seed 7: 370 passed, " + S + "v16_doc_command_reference_seed7.log).")
row("PRJ-D1-13", "2.5-lab", "project.html:53-168; tests/labs/M7/lab-M7-project-1.py", P,
    "run_labs.py --unit M7: PASS 11/11 (" + S + "v16_run_labs_M7.log). " + S + "v16_twin_vs_page.log: page code == twin, "
    "twin exits 0 under python -I -W error with empty stderr, stdout == expected block.")
row("PRJ-D1-14", "2.5-lab", "project.html:170-285; tests/labs/M7/lab-M7-project-2.py", P,
    S + "v16_twin_vs_page.log: page code differs from the twin only in the three blanked lines (residual, signs, dual_feasible); "
    "the completed twin's stdout equals the expected block.")
row("PRJ-D1-15", "2.5-lab", "project.html:372-445; tests/labs/M7/lab-M7-project-3.py", P,
    S + "v16_twin_vs_page.log: Lab 3 page code == twin; output == expected block (project.html:441-443). Lab text unchanged "
    "since round 15, where 9/550, 9/1100 and 1/6250 were re-derived by hand.")
row("PRJ-D1-16", "2.9-hours", "project.html:33,338-354; course/modules/M/M7/index.html:29; curriculum/01-foundations.yaml M7 hours 110", P,
    CARRY_D1 + "project.html:33 and 344-350 unchanged (33 = 2+3+10+6+7+5); index.html and the curriculum are unchanged in the delta.")
row("PRJ-D1-17", "2.9-structure", "project.html:40-49", P,
    CARRY_D1 + "ladder lines 40-49 unchanged; rung 1 annotated, rung 2 completion, rung 3 specification, rung 4 stretch.")
row("PRJ-D1-18", "2.6-spec", "project.html:288-336", P,
    "Re-read this round in full (288-336, including the changed line 332: 370 checks, twelve hand cases, six testing the "
    "starting tolerance) against instance.py and reference.py. No clarifying question arises from re-reading. The "
    "certificate defect that remains on page-valid inputs is recorded as PRJ-R16-01, not as a spec-clarity defect.")
row("PRJ-D1-19", "2.9-structure", "course/modules/M/M7/grader/ (instance.py, reference.py, starter.py, test_project.py)", P,
    CARRY_D1 + "the grader file list is unchanged; project.html:359 names the same four files.")
row("PRJ-D1-20", "2.9-structure", "project.html; tools/page_smoke.py --unit M7 --pages project", P,
    "page_smoke.py --unit M7 --pages project: PASS (" + S + "v16_page_smoke_project.log): runtime boot, labs 1-3, "
    "in-browser grader: All 370 tests pass (3.8 s).")
row("PRJ-D1-21", "2.4-notation", "project.html symbols vs notation/notation.json", P,
    "Re-read this round: the changed lines 332 and 450 introduce no math symbol; the other page symbols are unchanged "
    "(round 15 checked T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q against notation/notation.json).")
row("PRJ-D1-22", "2.9-dag", "project.html:456 (envelope-theorem link); course/modules/M/M7/index.html", P,
    "check_dag.py --unit M7: PASS (" + S + "v16_check_dag_M7.log); project.html:456 unchanged.")
row("PRJ-D1-23", "2.9-prose", "project.html; tools/check_pages.py BANNED list", P,
    "check_pages.py --unit M7: PASS (" + S + "v16_check_pages_M7.log). The changed lines 332 and 450 were read for banned phrases: none.")
row("PRJ-D1-24", "2.6-spec", "project.html:364-366 (local run and decode commands)", P,
    "QF_SEED=7 pytest -q -p no:cacheprovider --assert=plain -W error test_project.py on the reference copy: 370 passed "
    "(" + S + "v16_doc_command_reference_seed7.log).")
row("PRJ-D1-25", "2.6-autograder", "grader/starter.py:18-20; project.html:301", P,
    "starter.py raises NotImplementedError (unchanged). The same documented command on the starter: 367 failed, 3 passed "
    "(" + S + "v16_doc_command_starter_seed7.log); project.html:301 'the suite fails on the starter' holds.")
row("PRJ-D1-26", "2.6-autograder", "grader/instance.py (make_instance)", P,
    CARRY_D1 + "instance.py byte-identical; run_graders PASS on seeds 0-49 this round.")
row("PRJ-D1-27", "2.6-autograder", "grader/test_project.py:37; grader/reference.py:23; project.html:300,321", P,
    "test_project.py:37 TOL = 1e-8 (feasibility, stationarity, complementary; agreement 1e-9); reference.py:23 "
    "TOL = Fraction(1, 10**9) (only its comment changed); project.html:300 and 321 state the same values.")
row("PRJ-D1-28", "2.6-autograder", "grader/test_project.py assert and pytest.fail messages", P,
    CARRY_D1 + "messages at old 60-77, 174-201, 231-255, 434-443 and 1108-1121 (later ones shifted +77) are unchanged; "
    "each names a property or an index and prints no expected value. Default mode on seed 3: 370 passed "
    "(" + S + "v16_default_mode_reference_seed3.log).")
row("PRJ-D1-29", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke) and CPython (run_graders)", P,
    "CPython: run_graders.py --unit M7 --seeds 0-49: PASS, reference 50/50. Pyodide: page_smoke PASS, 370 tests pass in-browser.")
row("PRJ-D1-30", "2.5-lab", "tests/labs/M7/lab-M7-project-1..3.py; tests/test_labs.py -k M7", P,
    "run_labs.py --unit M7: PASS 11/11; pytest tests/test_labs.py -k M7: 11 passed, exit 0 (" + S + "v16_pytest_labs_M7.log).")
row("PRJ-D1-31", "2.6-spec", "project.html:332; grader/test_project.py HAND_CASES (274-383)", P,
    "All 12 HAND_CASES entries (collect and label check: " + S + "v16_collect_and_labels.log) pass on the reference (seed 7: 370 passed). "
    "The six new worked answers were re-derived by hand this round: turnover limit 1e-9 -> (0.5+5e-10, 0.5-5e-10); upper "
    "bound 0.5+1e-9 -> (0.5+1e-9, 0.5-1e-9); lower bound 0.5+5e-10 with mu=-1000 -> (0.5+5e-10, 0.5-5e-10); sector-0 cap "
    "0.6-5e-10 with a lower bound 0.3 -> (0.3, 0.3-5e-10, 0.4+5e-10); zero turnover -> start; binding sector cap -> "
    "(0.3-2.5e-10, 0.3-2.5e-10, 0.4+5e-10). Reference outputs match each within 1e-8 (" + S + "v16_hand_case_comments.log). "
    "NOTE: the reference's answer for the lower-bound and binding-cap cases carries a budget residual of up to 5e-10 "
    "(the snap does not restore the budget); it is inside the 1e-8 tolerance.")
row("PRJ-D1-32", "2.6-atlas", "project.html; curriculum/01-foundations.yaml M7 entry; check_projects --unit M7", P,
    "check_projects.py --unit M7: PASS (" + S + "v16_check_projects_M7.log).")
row("PRJ-D1-33", "2.1-citations", "project.html:465-466 (reading list); references/references.json", P,
    CARRY_D1 + "references/references.json and project.html:465-466 unchanged. verify_refs.py --offline: 560 entries, 0 problems "
    "this round (" + S + "v16_verify_refs_offline.log). The live Crossref run is not repeated; its round-15 result is carried.")
row("PRJ-D1-34", "2.9-structure", "project.html:338-354; tools/check_pages.py --unit M7", P,
    "Time-budget table 338-354 unchanged; check_pages.py --unit M7 PASS (" + S + "v16_check_pages_M7.log).")
row("PRJ-D1-35", "2.6-mutation", "ledgers/M7/mutants/ (all files)", P,
    "tools/mutate_graders.py --unit M7 --seeds 0-9 (this round, after the new mutants were added): 221/221 killed (" + S +
    "v16_mutate_graders_M7_0-9.log). The new round-16 mutants (r16_01..10, the verifier's v16d_01..03) are included.")
row("PRJ-D1-36", "2.6-mutation", "ledgers/M7/mutants/ (all families)", P,
    "Same run: every file in ledgers/M7/mutants/ is KILLED (221 of 221; ledger mutants list = this log).")
row("PRJ-D1-37", "2.6-mutation", "ledgers/M7/equivalent/r04_budget_left_out_of_primal_residual.py; ledgers/M7/equivalent/README.md proof 6", F_,
    "r04 is NOT equivalent. The budget gap enters the reference primal residual (reference.py:305-306), and a start that sums "
    "to 1+1e-9 with asset 0 1e-9 below its lower bound (decimal values, accepted by the page's 1e-9 starting checks) gives "
    "a budget gap of 2e-9: reference primal 2e-9, r04 primal 0, difference 2e-9 > the 1e-9 agreement tolerance "
    "(" + S + "v16_minimal_cases.log B1; " + S + "v16_r04_probe.log). A sweep case of seed 17 (idx 459) gives 1.5e-9 "
    "(" + S + "v16_sweep_1500_seed17.log). The grader suite does not kill r04: 370 passed on every seed 0-9 "
    "(" + S + "v16_r04_suite_seeds0-9.log). README proof 6 and its 'measured 1.000e-09' claim are false. The other "
    "eight files: sweeps of 2,737 answered page-valid cases (" + S + "v16_sweep_1500_seed16.log, _seed17.log) show no "
    "difference above 1e-9 for q04, r02, r05, s12_03, v10_01, v10_02, v11_01, v12_01; proofs 1-5, 7 and 8 re-read and "
    "checked against F2, F4, F5 (reference.py:232-260, 271-277, 305-326).",
    "Move r04 to ledgers/M7/mutants/ (its docstring's first line names the student error) and add a grader hand case "
    "for the B1 start (w0 = [0.499999999, 0.500000002], lower = [0.5, -1], mu = [0, 0], sigma = I, gamma = 1, tau = 2): the "
    "primal residual must include the 2e-9 budget gap. Re-run mutate_graders --unit M7. Correct README proof 6 and the "
    "measured-bound sentence (the measured maxima are 1.5e-9 and 2e-9).")
row("PRJ-D1-38", "2.6-autograder", "ledgers/M7/scripts/M7-d-r11/alts/ alt1..alt9; M7-d-r12fix/methods; M7-d-r14/alts; M7-d-r12fix/alts_repaired; M7-d-r10/alts", F_,
    "Re-run on seeds 0-49 against the current suite (370 tests). Pass 50/50: r11 alt6 and alt9 (scaled float, exact polish), "
    "the projected-gradient front end (r12fix methods/alt_2_pg.py; r14 alts/alt2). Fail 0/50: r11 alt1, alt2, alt8; r14 alt1, "
    "alt3, alt4, alt5; r12fix methods alt_3_admm, alt_4_ipm, alt_5_dual; r12fix alts_repaired A, C, D, E, F; r12 alt_r12_1, "
    "alt_r12_2; r10 alt B, G, H, I, J (" + S + "v16_alts_r11_seeds0-49.log, v16_alts_plan742_seeds0-49.log, "
    "v16_alts_ruling19_methods_seeds0-49.log, v16_alts_repaired_r10_r12_seeds0-49.log). The failures are page-valid "
    "start-breach hand cases (lower bound one billionth, binding sector cap) and the turnover case: the answer is "
    "uncertified (complementary slackness 5e-7 or 1e-7, " + S + "v16_show_alt.log). Exact active sets without the snap "
    "and the ADMM/IPM/dual front ends accept an answer without a complementary-slackness check. These are not "
    "over-constraint: the page's certificate tolerance (project.html:321) rejects them. Alternatives not re-run (float "
    "r10 A, C-F; r11 alt3, 4, 5, 7; r12 alt_r12_3..7) failed on the r15 suite and the suite only grew, so they still fail. "
    "Result: 4 files pass, of 2 styles (projected gradient; scaled float with exact polish). Five correct alternatives "
    "of different styles are not present.",
    "Provide at least five correct alternatives of different styles that pass seeds 0-49 on the current suite. Fix the "
    "front-end acceptance test of the ruling-19 methods (add the complementary-slackness check); make the exact active "
    "sets snap a within-tolerance start as reference._snapped_start does and admit only rows with exactly zero slack. "
    "Re-run run_parallel.py on seeds 0-49.")
row("PRJ-D1-39", "2.9-structure", "BLUEPRINT.md:400-401; course/modules/M/M7/grader/reference.py; .github/workflows/ci.yml", P,
    "NOTE, not a FAIL (ruling 4, owner deploy-time item): the repository has no deploy step that excludes grader/reference.py; "
    ".gitignore, .github/workflows/ci.yml and the tools are unchanged in the delta. Recorded for the owner.")

# ---- carried rows of earlier rounds (ids kept) ----
row("PRJ-R4-01", "2.9-prose", "grader/test_project.py docstrings and messages", P,
    CARRY + "module docstring (1-10), _observed_call and messages unchanged; the new hand-case comments were checked this round "
    "(numbers in " + S + "v16_hand_case_comments.log).")
row("PRJ-R5-01", "2.4-math", "project.html:456 frontier bullet", P,
    CARRY + "project.html:456 unchanged; envelope-theorem link resolves (check_dag PASS).")
row("PRJ-R5-02", "2.6-spec", "grader/test_project.py comments and messages (275, 277, 295-296, 301, 303-305)", P,
    CARRY + "test_project.py lines 275-305 are before the HAND_CASES insertion (after line 311), byte-identical.")
row("PRJ-R5-03", "2.9-prose", "project.html:450 ('does not test' paragraph)", P,
    "Re-read this round: 'the hand-worked cases in the suite' is accurate (HAND_CASES, 12 entries). 'every case carries the "
    "SIMULATED label' holds: all 12 hand cases carry a SIMULATED label (" + S + "v16_collect_and_labels.log).")
row("PRJ-R5-04", "2.9-structure", "project.html:349-350", P,
    CARRY + "project.html:349-350 unchanged.")
row("PRJ-R5-05", "2.6-mutation", "ledgers/M7/mutants/r5_01..r5_05", P,
    "Killed in this round's full run (" + S + "v16_mutate_graders_M7_0-9.log: 221 of 221 KILLED).")
row("PRJ-R6-01", "2.6-gate", "tools/check_projects.py --all (M7 entry)", P,
    "check_projects.py --unit M7: PASS (" + S + "v16_check_projects_M7.log).")
row("PRJ-R6-02", "2.6-gate", "tools/check_pages.py --all (M7 entry)", P,
    "check_pages.py --unit M7: PASS (" + S + "v16_check_pages_M7.log).")
row("PRJ-R6-03", "2.9-dag", "tools/check_dag.py --all (M7 entry)", P,
    "check_dag.py --unit M7: PASS (" + S + "v16_check_dag_M7.log).")
row("PRJ-R7-01", "2.6-mutation", "grader/test_project.py degenerate box hand case (306-311); mutants r7_06_*", P,
    CARRY + "the degenerate box case (306-311) is unchanged; its mutants are KILLED in this round's full run.")
row("PRJ-R7-02", "2.9-prose", "grader/test_project.py:295-296 comment", P,
    CARRY + "comment unchanged (before the insertion).")
row("PRJ-R7-03", "2.9-prose", "grader/test_project.py:916-921 comment (now 993-998)", P,
    CARRY + "comment text unchanged; content shifted by the +77 insertion.")
row("PRJ-R7-04", "2.6-mutation", "ledgers/M7/mutants/r7_01..r7_05", P,
    "KILLED in this round's full run (" + S + "v16_mutate_graders_M7_0-9.log).")
row("PRJ-R7-05", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke)", P,
    "page_smoke.py --unit M7 --pages project: PASS, 370 tests pass in-browser (" + S + "v16_page_smoke_project.log).")
row("PRJ-R7-06", "2.8-data", "project.html; grader/instance.py", P,
    CARRY + "project.html data attributes and instance.py unchanged; the case is SIMULATED.")
row("PRJ-R7-07", "2.6-hours", "project.html:344-350", P,
    CARRY + "hours table unchanged (2+3+10+6+7+5 = 33).")
row("PRJ-R8-01", "2.6-autograder", "grader/test_project.py:60-77, 1114-1121 (now 1191-1198) and purity fixture (80-104)", P,
    CARRY + "functions and messages unchanged; the purity fixture is unchanged.")
row("PRJ-R8-02", "2.6-autograder", "grader/test_project.py:1108-1112 (now 1185-1189) and purity fixture", P,
    CARRY + "unchanged.")
row("PRJ-R8-03", "2.6-mutation", "ledgers/M7/mutants/v8_03_budget_multiplier_zero_when_start_is_optimal.py", P,
    "KILLED in this round's full run (" + S + "v16_mutate_graders_M7_0-9.log).")
row("PRJ-R8-04", "2.6-spec", "grader/test_project.py:302-311", P,
    CARRY + "lines 302-311 unchanged (before the insertion).")
row("PRJ-R9-01", "2.6-autograder", "grader/test_project.py:60-77 (_observed_call) vs pytest.raises(Exception) tests", P,
    CARRY + "_observed_call and the tests are unchanged.")
row("PRJ-R9-02", "2.9-prose", "grader/test_project.py:82-89 docstring", P,
    CARRY + "docstring unchanged.")
row("PRJ-R9-03", "2.6-autograder", "grader/test_project.py:92 (@wraps) and the block at old 319-326", P,
    CARRY + "unchanged text, shifted by the +77 insertion.")
row("PRJ-R9-04", "2.9-prose", "project.html:167 (Lab 1 interpretation)", P,
    CARRY + "project.html:167 unchanged; Lab 1 output re-checked by run_labs and the twin check this round.")
row("PRJ-R9-05", "2.4-math", "project.html:324 (proof)", P,
    CARRY + "project.html:324 unchanged; re-read this round.")
row("PRJ-R9-06", "2.6-autograder", "ledgers/M7/scripts/M7-d-r11/alts/ and alts_suite_r11*.log", F_,
    "Re-run this round: alt1, alt2, alt8 now fail 0/50; alt6 and alt9 pass 50/50 (" + S + "v16_alts_r11_seeds0-49.log). See PRJ-D1-38.",
    "See PRJ-D1-38.")
row("PRJ-R9-07", "2.6-mutation", "ledgers/M7/mutants/ (final folder)", P,
    "221 of 221 KILLED in this round's full run (" + S + "v16_mutate_graders_M7_0-9.log).")
row("PRJ-R9-08", "2.9-structure", "grader/test_project.py (collected count); project.html:332", P,
    "Collected count is 370 on every seed 0-49 (" + S + "v16_collect_and_labels.log); project.html:332 says 370.")
row("PRJ-R9-09", "2.5-lab", "project.html:53-285, 372-445; tests/labs/M7/lab-M7-project-1..3.py", P,
    "run_labs PASS 11/11 and the page-versus-twin check (" + S + "v16_run_labs_M7.log, v16_twin_vs_page.log).")
row("PRJ-R9-10", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke)", P,
    "page_smoke PASS this round (" + S + "v16_page_smoke_project.log).")
row("PRJ-R9-11", "2.9-prose", "grader/test_project.py:274-311 hand-case comments", P,
    CARRY + "comments at 274-311 unchanged; the six new comments were checked numerically this round (" + S + "v16_hand_case_comments.log).")
row("PRJ-R10-01", "2.6-autograder", "ledgers/M7/scripts/M7-d-r10/alts/ alt_B, alt_G, alt_H, alt_I, alt_J (exact Fraction active sets)", F_,
    "Re-run this round: each now fails 0/50 (" + S + "v16_alts_repaired_r10_r12_seeds0-49.log) on the lower-bound and "
    "binding-cap hand cases with complementary slackness above 1e-8 (the start breach is not snapped; alt_B on the "
    "lower-bound and binding-cap cases; alt_B seed 0: " + S + "v16_alt_B_suite_seed0.log).",
    "Snap a start that breaches a bound or cap within 1e-9 as reference._snapped_start does, and admit only rows with exactly "
    "zero slack (see PRJ-R16-01 for the remaining fallback defect).")
row("PRJ-R10-02", "2.6-autograder", "ledgers/M7/scripts/M7-d-r10/alts/ alt_A, C, D, E, F (float alternatives)", P,
    CARRY + "these failed on the round-15 suite (0/50); the delta only added HAND_CASES entries, so each still fails "
    "(superset argument; not re-run this round). Classified as student errors, as in round 15.")
row("PRJ-R10-03", "2.6-mutation", "ledgers/M7/mutants/r10_01..r10_03", P,
    "KILLED in this round's full run (" + S + "v16_mutate_graders_M7_0-9.log).")
row("PRJ-R10-04", "2.6-autograder", "ledgers/M7/mutants/ full set", P,
    "221 of 221 KILLED (" + S + "v16_mutate_graders_M7_0-9.log).")
row("PRJ-R10-05", "2.6-autograder", "tools/run_graders.py --unit M7 --seeds 0-49; mypy --strict on grader", P,
    "run_graders PASS, reference 50/50 (" + S + "v16_run_graders_M7_0-49.log). mypy --no-incremental --strict on reference.py and "
    "starter.py: no issues (" + S + "v16_mypy_M7_grader.log).")
row("PRJ-R10-06", "2.9-structure", "repo gates: ruff check ., ruff format --check ., mypy --no-incremental, verify_refs --offline", P,
    "ruff check . PASS (" + S + "v16_ruff_check_repo.log); ruff format --check . 554 files formatted (" + S + "v16_ruff_format_repo.log); "
    "mypy --no-incremental: 385 files, no issues (" + S + "v16_mypy_repo.log); verify_refs --offline 560 entries, 0 problems.")
row("PRJ-R11-01", "2.6-autograder", "over-constraint: ledgers/M7/scripts/M7-d-r11/alts/ (nine solvers)", F_,
    "Re-run this round: alt6 and alt9 pass 50/50; alt1, alt2, alt8 fail 0/50; alt3, alt4, alt5, alt7 failed the round-15 suite "
    "and still fail (superset). Fewer than five correct alternatives remain (" + S + "v16_alts_r11_seeds0-49.log). See PRJ-D1-38.",
    "See PRJ-D1-38.")
row("PRJ-R11-02", "2.6-mutation", "ledgers/M7/mutants/r11_01, r11_03, r11_05, r11_06", P,
    "KILLED in this round's full run (" + S + "v16_mutate_graders_M7_0-9.log).")
row("PRJ-R11-03", "2.6-spec", "project.html:326 (gamma valid form) vs test_project.py EXACT_BOUNDARIES and NAMED_CONDITIONS", P,
    CARRY + "project.html:326 unchanged; the gamma tables are unchanged (gamma-just-inside-zero at 1e-9, NAMED at 1e-6).")
row("PRJ-R11-04", "2.6-autograder", "grader/test_project.py assertion style under default pytest mode", P,
    "Default mode, seed 3: 370 passed (" + S + "v16_default_mode_reference_seed3.log).")
row("PRJ-R12-01", "2.6-autograder", "grader/instance.py (make_instance) seeds 0-49", P,
    CARRY + "instance.py byte-identical; run_graders PASS on seeds 0-49 this round.")
row("PRJ-R12-02", "2.6-autograder", "plans/M7-build-plan.md section 7.4 item 2 (five alternatives, different methods)", F_,
    "Front-end ADMM, IPM and dual-ascent solvers (r12fix methods) fail 0/50 on the current suite; only projected gradient "
    "passes among the four methods (" + S + "v16_alts_ruling19_methods_seeds0-49.log). The five-alternative requirement "
    "is not met. See PRJ-D1-38.",
    "Add the complementary-slackness check to the acceptance test of the three failing front ends; re-run on seeds 0-49.")
row("PRJ-R12-03", "2.6-autograder", "over-constraint check: exact and float active-set alternatives on seeds 0-49", P,
    "Re-checked this round: the exact and float active-set alternatives that fail the current suite fail on page-valid "
    "inputs with an uncertified answer (complementary slackness above 1e-8, " + S + "v16_show_alt.log), so the grader is not "
    "over-constrained. Their pass counts are in " + S + "v16_alts_*.log.")
row("PRJ-R12-04", "2.6-autograder", "over-constraint check: float alternatives r12 alt 3-7 (solver defects on valid gamma inputs)", P,
    CARRY + "alt_r12_3..7 failed on the round-15 suite (37-41 of 50 seeds) and the delta only adds tests; not re-run.")
row("PRJ-R12-05", "2.6-mutation", "new student-error mutants v12_02, v12_03, v12_04, v12_05 (ledgers/M7/mutants/)", P,
    "KILLED in this round's full run (" + S + "v16_mutate_graders_M7_0-9.log).")
row("PRJ-R12-06", "2.6-mutation", "equivalence proof: v12_01 (dual residual reported without the floor at zero)", P,
    "ledgers/M7/equivalent/v12_01 differs from the reference only in the dual report line (diff). Proof 1: min m = 0 by F2. "
    "Sweep of 2,737 answered page-valid cases: 0 difference above 1e-9 (" + S + "v16_sweep_1500_seed16.log, _seed17.log).")
row("PRJ-R12-07", "2.6-autograder", "grader/test_project.py collect-only, seeds 0-49", P,
    "370 collected on every seed 0-49 (" + S + "v16_collect_and_labels.log).")
row("PRJ-R12-08", "2.5-lab", "project.html lab code and expected blocks vs tests/labs/M7/lab-M7-project-1..3.py", P,
    S + "v16_twin_vs_page.log: page code == twin for labs 1 and 3; lab 2 differs only in the three blanks; expected == output for all three.")
row("PRJ-R12-09", "2.4-math", "project.html Lab 1 and Lab 3 printed numbers", P,
    CARRY + "lab text unchanged; outputs re-checked by the twin run this round.")
row("PRJ-R12-10", "2.4-math", "project.html:323-325 Proposition (grade T)", P,
    CARRY + "lines 323-325 unchanged; re-read this round.")
row("PRJ-R12-11", "2.6-spec", "project.html:292-300 inputs and outputs vs instance.py and test_project.py", P,
    "Re-read this round (292-300) against instance.py and test_project.py output_shape.")
row("PRJ-R12-12", "2.6-spec", "project.html:326 named conditions vs test_project.py tables", P,
    CARRY + "the tables are unchanged in content; the page's list (326) is unchanged; re-read this round.")
row("PRJ-R12-13", "2.6-autograder", "Pyodide timing (plan 7.4; BUILDER_RULES 5.3.4)", P,
    "page_smoke in-browser grader: 370 tests in 3.8 s (" + S + "v16_page_smoke_project.log).")
row("PRJ-R12-14", "2.1-citations", "project.html:465-466 reading list keys", P,
    CARRY + "references/references.json and project.html:465-466 unchanged (verify_refs offline PASS).")
row("PRJ-R12-15", "2.9-dag", "project.html:310 'defined in Lesson 3' link", P,
    "check_dag.py --unit M7: PASS (" + S + "v16_check_dag_M7.log).")
row("PRJ-R14-01", "2.6-mutation", "ledgers/M7/mutant_equivalence_r14.json; ledgers/M7/equivalent/", F_,
    "The round-14 record lists r04 as equivalent on an exact argument ('budget gap exactly zero on every reference output'). "
    "That is false: B1 (" + S + "v16_minimal_cases.log) gives a 2e-9 budget gap distinguishing r04, and the README's "
    "corrections section does not retract r04's entry. The equivalent/ folder now exists (9 files).",
    "Retract the r04 entry in the round-14 record (or supersede the record with the round-16 equivalence section) and move "
    "r04 to ledgers/M7/mutants/ (PRJ-D1-37).")
row("PRJ-R14-02", "2.4-math", "project.html:167, 172, 310 (multiplier references) vs project.html:310 Conventions", P,
    CARRY + "lines 167, 172 and 310 unchanged.")
row("PRJ-R14-03", "2.5-lab", "project.html:444 (Lab 3 interpretation) vs project.html:412 and the printed line", P,
    CARRY + "lines 412 and 444 unchanged; Lab 3 output re-checked by the twin run.")
row("PRJ-R14-04", "2.5-lab", "project.html:169-285 (Lab 2) completion blanks vs twin tests/labs/M7/lab-M7-project-2.py", P,
    S + "v16_twin_vs_page.log: only the three blanks differ; the completed twin's output equals the expected block.")
row("PRJ-R14-05", "2.6-mutation", "ledgers/M7/mutants/w14d_01..w14d_03", P,
    "KILLED in this round's full run (" + S + "v16_mutate_graders_M7_0-9.log).")
row("PRJ-R14-06", "2.6-autograder", "grader/test_project.py: 370 checks, identical for every seed (project.html:332)", P,
    "Re-checked: 370 collected on each of seeds 0-49 (" + S + "v16_collect_and_labels.log); project.html:332 says 370.")
row("PRJ-R14-07", "2.6-autograder", "project.html:450 'every case carries the SIMULATED label'", P,
    "All 12 HAND_CASES carry a SIMULATED label; instance cases are SIMULATED (" + S + "v16_collect_and_labels.log).")
row("PRJ-R14-08", "2.6-autograder", "project.html:326 'other invalid inputs... raise an exception that carries a message'", P,
    CARRY + "project.html:326 unchanged; the tests are unchanged.")
row("PRJ-R14-09", "2.6-rubric", "curriculum/01-foundations.yaml:327 (grading autograder); tools/check_projects.py rubric block", P,
    CARRY + "curriculum unchanged; check_projects.py --unit M7 PASS this round.")
row("PRJ-R14-10", "2.6-atlas", "curriculum/meta.yaml atlas block; project.html", P,
    CARRY + "curriculum/meta.yaml and project.html atlas lines unchanged.")
row("PRJ-R14-11", "2.9-hours", "project.html:344-350 (verifier estimate)", P,
    CARRY + "hours table unchanged.")
row("PRJ-R14-12", "2.6-gate", "tools/check_pages.py --unit M7; tools/check_dag.py --unit M7; tools/check_projects.py --unit M7", P,
    "All three PASS this round (" + S + "v16_check_pages_M7.log, v16_check_dag_M7.log, v16_check_projects_M7.log).")
row("PRJ-R14-13", "2.6-autograder", "Pyodide per-test time (plan 7.3: under 5 s each, 60 s per suite)", P,
    "In-browser suite: 370 tests in 3.8 s (" + S + "v16_page_smoke_project.log).")
row("PRJ-R14-14", "2.6-autograder", "run_labs --unit M7; pytest tests/test_labs.py -k M7", P,
    "run_labs PASS 11/11; pytest tests/test_labs.py -k M7: 11 passed (" + S + "v16_run_labs_M7.log, v16_pytest_labs_M7.log).")
row("PRJ-R14-15", "2.6-autograder", "over-constraint: the five alternatives of plan 7.4.2 (ruling 19)", F_,
    "Re-run on seeds 0-49: only alt2 (projected gradient) passes 50/50; alt1, alt3, alt4, alt5 fail 0/50 (" + S +
    "v16_alts_plan742_seeds0-49.log). See PRJ-D1-38.",
    "See PRJ-D1-38.")
row("PRJ-R14-16", "2.6-autograder", "over-constraint: ledgers/M7/scripts/M7-d-r14/alts/ (five and five repaired)", F_,
    "Re-run on seeds 0-49: the repaired float alternatives (r12fix alts_repaired A, C, D, E, F) now fail 0/50 "
    "(" + S + "v16_alts_repaired_r10_r12_seeds0-49.log); the five-set requirement is not met. See PRJ-D1-38.",
    "See PRJ-D1-38.")
row("PRJ-R14-18", "2.1-citations", "references/references.json (boyd2004convex, stokey1989recursive)", P,
    CARRY + "references.json unchanged; verify_refs offline PASS this round.")
row("PRJ-R15-01", "2.6-autograder", "course/modules/M/M7/grader/reference.py:232 (initial working set, exact zero slack) and :21, :1-8 docstring", P,
    "Fixed for the two reported inputs: case A (mu=[1000,0], tau=1e-9) now returns (0.5+5e-10, 0.5-5e-10) and case E "
    "(upper=[0.5+1e-9, 2]) returns (0.5+1e-9, 0.5-1e-9), both certified by the independent recomputation "
    "(" + S + "v16_probe_named.log). The hand cases were added (test_project.py 316-337). The docstring claim that the "
    "start is exactly feasible is still false on the fallback branches; that remaining defect is PRJ-R16-01.")
row("PRJ-R15-02", "2.6-mutation", "ledgers/M7/equivalent/r05_turnover_total_slackness_term_zeroed.py; v10_02_complementary_slackness_signed_not_absolute.py; README proofs 7 and 8", P,
    "Re-proved and re-checked. Proof 7: kappa > 0 forces an eta_s > 0 row into the working set, which is tight (F5), so "
    "sum|d| = tau and the term is 0. Proof 8: each product is non-negative (F3, F5 on the signs of d). Sweep of 2,737 "
    "answered page-valid cases: 0 differences above 1e-9 for both (" + S + "v16_sweep_1500_seed16.log, _seed17.log). "
    "The argument covers the fallback branches because it uses only F4 (sign-row slacks are non-negative) and F5. "
    "Files are regenerated from the round-16 reference (README 'Corrections').")
row("PRJ-R15-03", "2.6-mutation", "ledgers/M7/mutants/r15_01..r15_03", P,
    "KILLED in this round's full run (" + S + "v16_mutate_graders_M7_0-9.log).")
row("PRJ-R15-04", "2.6-mutation", "ledgers/M7/equivalent/ (q04, r02, r04, s12_03, v10_01, v11_01, v12_01)", F_,
    "Seven of the eight listed files are equivalent on the sweep (0 differences above 1e-9). r04 is not (B1, 2e-9 > 1e-9; "
    "PRJ-D1-37). The round-15 claim 'observed max difference 8e-14 on 400 cases' does not cover B1 or the seed-17 case.",
    "See PRJ-D1-37: move r04 to ledgers/M7/mutants/ and kill it.")

# ---- rows new in round 16 ----
row("PRJ-R16-01", "2.6-autograder", "course/modules/M/M7/grader/reference.py:216 and :220 (fallback returns the unsnapped start); :250-259 (blocking admits the violated row); docstring :8-10 and :197-206", F_,
    "Page-valid starts whose sector or bound breach cannot be snapped (turnover guard at :220, or room < excess at :215-216) "
    "return w0 unrepaired. The violated row then enters the working set at step 0 with a large multiplier, and the "
    "reference's own certificate exceeds 1e-8. Minimal case G (" + S + "v16_minimal_cases.log): gamma=1, sigma=I, mu=[-1000,0], "
    "w0=[0.5,0.5], lower=[0.5000000005,-1], upper=[2,2], sector=[0,0], sector_caps=[2], turnover_limit=0 (decimal values; "
    "start check passes by 5e-10 inside TOL): reference weights [0.5,0.5], lower multiplier 1000, complementary slackness "
    "5e-07 > 1e-8, independent recomputation certified=False. The H control (turnover 5e-10, same start) is certified. "
    "Sweep: 23 of 2,737 page-valid answered cases exceed 1e-8 (seed 16: 13; seed 17: 10; max 1.36e-6), all on the fallback "
    "branches (room 4, turnover guard 19) (" + S + "v16_cert_fail_analysis_seed16.log, _seed17.log, v16_snap_path_seed16.log, "
    "_seed17.log). No suite test has tau = 0 or a snap move above tau with a large gradient, so the suite passes. The "
    "docstring's 'so the search starts exactly feasible' is false on these branches and for the budget (the start sum is not "
    "snapped: B1/B2 give a 2e-9 budget gap, " + S + "v16_r04_probe.log).",
    "Make every page-valid start certify within 1e-8. Options: when the turnover guard refuses the snap, do not admit a "
    "violated row with a free multiplier (it cannot be satisfied exactly); or allow the snap when moved <= tau + TOL and "
    "re-check the sign rows; or restore the budget after snapping. Add G and sweep case seed 16 idx 15 (a tolerance-level "
    "sector breach with asset 2 pinned at its lower bound) as hand cases. Correct the docstring. Re-run run_graders "
    "0-49, mutate_graders and the alternatives.")
row("PRJ-R16-02", "2.6-mutation", "ledgers/M7/mutants/v16d_01_snap_ignores_sector_caps.py, v16d_02_turnover_guard_dropped_from_snap.py, v16d_03_sector_excess_all_from_first_member.py", P,
    "Three verifier-written student-error mutants of the reference's start snap (generated by " + S + "v16_make_mutants.py). "
    "Each fails at least one test on every seed 0-9 (hand cases: binding sector cap, zero turnover with sector breach, "
    "sector breach at a lower bound) (" + S + "v16_mutate_graders_M7_0-9.log: KILLED).")
row("PRJ-R16-03", "2.9-structure", "project.html:332 counts vs test_project.py HAND_CASES and collect-only", P,
    "HAND_CASES has 12 entries (" + S + "v16_collect_and_labels.log); 6 new of them test the starting tolerance; 370 collected "
    "on every seed 0-49; project.html:332 says twelve, six and 370.")
row("PRJ-R16-04", "2.9-prose", "grader/test_project.py new hand-case comments (316-383)", P,
    "Each comment's numbers were checked against the reference output (" + S + "v16_hand_case_comments.log): the turnover case "
    "leaves complementary 5e-7 for the start-in-place answer (kappa = 500 minimal, from the two sign rows); the upper-bound "
    "case leaves 1e-6 (lambda_u = 1000); the zero-turnover case has sector-0 multiplier 1000.1 and sector-1 multiplier 0.")

# ---- mutants ----
mutants: list[dict[str, str]] = []
log = (ROOT / S / "v16_mutate_graders_M7_0-9.log").read_text(encoding="utf-8").splitlines()
for line in log:
    if line.startswith("KILLED "):
        body = line[len("KILLED "):]
        name, rest = body.split(": ", 1)
        desc, killed = rest.rsplit(" -> ", 1)
        mutants.append({"id": name, "description": desc, "killed_by": killed})
    elif line.startswith("SURVIVED "):
        body = line[len("SURVIVED "):]
        name, rest = body.split(": ", 1)
        mutants.append({"id": name, "description": rest.split(" -> ")[0], "killed_by": ""})

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"
commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
fragment = {
    "unit": "M7",
    "slice": "d",
    "round": 16,
    "verifier": "Haiku 5.5 independent verifier (round 16, slice d, delta verification); did not build M7-d",
    "pin": commit,
    "base": "dde0486b (round-15 pin; fragment /Users/billyribeiro/.fanout/frags/D-M7-d.round15.json, context only)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD16-M7-d",
    "scratch": "ledgers/M7/scripts/M7-d-r16/ (plus /private/tmp/v16-m7d and /private/tmp/v16-alts, copies only)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta e896b7a4 against dde0486b for slice d: project.html (lines 332 and 450), grader/reference.py (docstring, TOL "
        "comment, _snapped_start, initial working set), grader/test_project.py (+77 HAND_CASES lines), ledgers/M7/equivalent/ "
        "(README and nine files), ledgers/M7/mutants/ (r15_01..03, r16_01..10 added). Every hunk was read. Rows whose cited "
        "subject is byte-identical are carried with the carry prefix; rows whose subject changed or whose status was FAIL were "
        "re-verified. Rulings applied: 4 (PRJ-D1-39 noted, not failed); 9 and 22 (equivalence folder with README); 19 (front-end "
        "solvers in M7-d-r12fix/methods checked); 10 (float alternatives wrong on a stated rule are not alternatives); 25 "
        "(measured bounds not accepted where a page-valid input exceeds the stated accuracy); 26 and 30 (delta round). The rulings "
        "file lines 19-26 were read in full; ruling 10's text is available in plans/FINAL-ARCHITECT-RULINGS.md item 10. "
        "Observations (not rows): the snapped start leaves a budget residual of up to 5e-10 on two hand cases (inside tolerance; "
        "README F3(a)); the test comment at test_project.py 'turnover limit of one billionth' is numerically correct. "
        "Not checked: the live Crossref run (verify_refs --unit M7) was not repeated; the deploy configuration (ruling 4); "
        "the full repository pytest suite (only tests/test_labs.py -k M7); Chromium page_smoke for other units; cards "
        "(out of slice); the r04 probe's decimal reading is the reference's (reference.py:46), not a page-stated rule; "
        "alternatives r10 A-F, r11 alt3/4/5/7 and r12 alt_r12_3..7 were not re-run (superset argument)."
    ),
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": len(mutants),
        "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
    },
}
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), counts, "mutants", len(mutants))
sys.path.insert(0, "tools")
import ledger  # noqa: E402

print("validate:", ledger.validate(json.loads(out.read_text(encoding="utf-8")), "M7-d"))
