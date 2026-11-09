"""Write the round-3 verifier fragment for E1 slice d (ledgers/E1/E1-d.json) from the run outputs in this directory."""

from __future__ import annotations

import json
import pathlib
import re
from datetime import UTC, datetime

CHECKOUT = pathlib.Path(__file__).resolve().parents[4]
S = CHECKOUT / "ledgers/E1/scripts/E1-d-r3"
OUT = CHECKOUT / "ledgers/E1/E1-d.json"

PIN = "8196077d5f56c3919d33e69888176d197d378ad4"
BASE = "aeb512b65b7774b59b84f836a13984fcfe9d0d1f"


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> dict:
    out = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        out["fix"] = fix or ""
    return out


ROWS = [
    row(
        "E1d-r1-ladder", "2.6-spec",
        "course/modules/E/E1/project.html lines 40-49 (ladder), 55-259 (rungs), 311 (spec), 365 (memo), 559 (stretch)",
        "PASS",
        "Rung 1 Lab 1 at line 55 with a comment on each step (lines 97, 101, 103, 105, 113); rung 2 completion lab at line 130 "
        "with two blanks; rung 3 spec line 311 and memo line 365; stretch line 559. tools/check_projects.py --unit E1: "
        "'check_projects E1: PASS' (scripts/E1-d-r3/check_projects.out). The placement of Lab 3 inside the skippable section "
        "is a separate FAIL row (E1d-r3-lab3-placement).",
    ),
    row(
        "E1d-r1-spec-precedence", "2.6-spec", "course/modules/E/E1/project.html line 321 (Constraints); grader/test_project.py lines 251-291",
        "PASS",
        "Line 321: 'When more than one of these conditions holds, a ValueError whose message names any one of them is accepted.' "
        "Each invalid case in the table violates exactly the condition it names: (20,2,10), (19,2,10), (-3,1,1) violate only a <= bc; "
        "(10,0,5), (10,-1,5) pass the a check and fail b; (10,2,0), (10,2,-1) pass a and b and fail c. Reference (grader/reference.py "
        "lines 26-35) and seed-0 run of the suite on the reference: '124 passed' (scripts/E1-d-r3/ref_seed0.out).",
    ),
    row(
        "E1d-r1-spec-tests-align", "2.6-spec", "course/modules/E/E1/project.html lines 318-323; grader/test_project.py",
        "PASS",
        "Each stated check maps to a test: exact keys (test_outcome_has_exactly_the_six_keys, line 111), int types (118), closed forms "
        "(125-131), orderings (134-184), exact cent ties (198-222), half-cent values (333-350), large exact inputs (323-330), "
        "standard-library rule (353-364), purity (235-240, 367-381), smallest b and c (294-319), second instance (390-398), "
        "ValueError table (251-291). Collect-only: 124 tests (scripts/E1-d-r3/collect_only.out).",
    ),
    row(
        "E1d-r1-hours", "2.9-hours", "course/modules/E/E1/project.html lines 340-346 and data-hours-project line 33; course/modules/E/E1/index.html line 29",
        "PASS",
        "Table rows 2+3+8+8+6+3 = 30 (lines 340-345); project.html line 35 says 30 hours; index.html line 29 has "
        "data-hours-lessons=90 and data-hours-project=30; 90+30 = 120, and the table's 'Equals ... 30 of the module's 120' (line 346) is consistent.",
    ),
    row(
        "E1d-r1-lab1-run", "2.5-lab", "course/modules/E/E1/project.html lines 55-128; tests/labs/E1/lab-E1-project-1.py",
        "PASS",
        "tools/run_labs.py --unit E1 --page project: 'run_labs E1: PASS (3/3)' (scripts/E1-d-r3/run_labs_project.out). "
        "scripts/E1-d-r3/project_labs_r3.out: page code equals twin (0 differing lines); twin run under python -I -W error exits 0 "
        "with empty stderr; twin output equals the expected block (True).",
    ),
    row(
        "E1d-r1-lab2-completion", "2.5-lab", "course/modules/E/E1/project.html lines 130-187; tests/labs/E1/lab-E1-project-2.py lines 28, 33",
        "PASS",
        "project_labs_r3.out: the page differs from the twin only on the two blanks: twin line 28 'return (d - rival) / 2' vs page "
        "'return ___' (line 160); twin line 33 'return half_up((a * volume - volume * volume / 2) / b - c * volume)' vs page "
        "'return half_up(___)' (line 165). Twin output equals the expected block (True); page_smoke lab-E1-project-2 passes (scripts/E1-d-r3/page_smoke.out).",
    ),
    row(
        "E1d-r1-lab3-run", "2.5-lab", "course/modules/E/E1/project.html lines 189-258; tests/labs/E1/lab-E1-project-3.py",
        "PASS",
        "project_labs_r3.out: page code equals twin (0 differing lines); twin output equals the expected block (True), "
        "all 12 lines (a = 120 and a = 121). Values re-derived with exact Fractions in scripts/E1-d-r3/rederive_r3.out.",
    ),
    row(
        "E1d-r1-lab1-prose", "2.5-lab", "course/modules/E/E1/project.html lines 57, 64-67, 127",
        "PASS",
        "rederive_r3.out (independent exact computation, not the reference module), a = 120: monopoly volume 50, fee 70, profit 2500, "
        "CS 1250, W 3750, DWL 1250; Cournot volume 200/3 (67), fee 160/3 (53), profit 20000/9 (2222), CS 20000/9 (2222), W 40000/9 (4444), "
        "DWL 5000/9 (556); Bertrand volume 100, fee 20, profit 0, CS 5000, DWL 0. Each prose figure at lines 57 and 127 matches.",
    ),
    row(
        "E1d-r1-lab2-prose", "2.5-lab", "course/modules/E/E1/project.html lines 132, 138-139, 186",
        "PASS",
        "Error recurrence e_{k+1} = -e_k/2 from the reaction map (Proposition 2 proof, line 292); after 60 steps |q_60 - d/3| = d/(3*2^60) "
        "= about 2.9e-17 < 1e-12, and the lab prints True (run_labs output). 40000/9 = 4444.44 and 160/3 = 53.33 as printed (rederive_r3.out).",
    ),
    row(
        "E1d-r1-lab3-prose", "2.5-lab", "course/modules/E/E1/project.html lines 191, 198-200, 257",
        "PASS",
        "rederive_r3.out: a = 121 monopoly fee 141/2 = 70.5 -> 71, volume 101/2 = 50.5 -> 51, profit 10201/4 = 2550.25 -> 2550; "
        "a = 120 monopoly welfare 3750 and Cournot welfare 4444. 200/3 = 66.67 and 202/3 = 67.33 both lie in (66.5, 67.5) (line 257).",
    ),
    row(
        "E1d-r1-prop1", "2.6-proof", "course/modules/E/E1/project.html lines 285-288 (Proposition 1)",
        "PASS",
        "Re-derived: pi(Q) = -Q^2/b + (d/b)Q; pi' = (d-2Q)/b; pi'' = -2/b, so Q* = d/2 is the unique maximiser on Q >= 0; fee (a+bc)/(2b); "
        "pi(d/2) = d^2/(4b) because f - c = d/(2b). Exact check at a = 120, b = 1, c = 20 gives Q* = 50, f = 70, pi = 2500 (rederive_r3.out).",
    ),
    row(
        "E1d-r1-prop2", "2.6-proof", "course/modules/E/E1/project.html lines 290-293 (Proposition 2)",
        "PASS",
        "Re-derived line by line: best-response derivative (d-2q_i-q_j)/b; the q_1 = 0 case gives q_2 = d/2 and then q_1 = d/4 > 0, a "
        "contradiction (line 292); subtraction gives q_1 = q_2; 2q = d - q gives d/3; e_{k+1} = -e_k/2 so |e_k| = d/(3*2^k); fee (a+2bc)/(3b); "
        "each exchange's profit d^2/(9b). Exact check at a = 120: Cournot volume 200/3, fee 160/3 (rederive_r3.out).",
    ),
    row(
        "E1d-r1-prop3", "2.6-proof", "course/modules/E/E1/project.html lines 295-297 (Proposition 3)",
        "PASS",
        "Case analysis re-read; the cases f1 < c, f1 > c with f2 > f1, f1 = f2 > c, and f1 = c < f2 are exhaustive for f1 <= f2, and each "
        "non-(c,c) case has a profitable deviation as the proof states. Grid check (scripts/E1-d-r3/bertrand_grid_r3.py, output "
        "bertrand_grid_r3.out): a = 40, b = 1, c = 10, all 6561 profiles on a half grid over [0, 40] with deviations on a 1/64 grid over "
        "[0, 40]: the only equilibrium is (10, 10).",
    ),
    row(
        "E1d-r1-prop4", "2.6-proof", "course/modules/E/E1/project.html lines 299-302 (Proposition 4)",
        "PASS",
        "Integrals re-derived: CS = int_0^Q (Q-t)/b dt = Q^2/(2b); G(x) = (ax - x^2/2)/b; W(x) = G(x) - cx; W'(x) = (d-x)/b; "
        "W(d) - W(Q) = (d-Q)^2/(2b); f(Q)Q = G(Q) - Q^2/(2b) gives CS + profit = G(Q) - cQ. rederive_r3.py section 4: the deadweight-loss "
        "identities hold exactly on 2000 random whole-number cases (scripts/E1-d-r3/rederive_r3.out).",
    ),
    row(
        "E1d-r1-prop5", "2.6-proof", "course/modules/E/E1/project.html lines 305-307 (Proposition 5)",
        "PASS",
        "Each difference re-derived: fee gap d/(6b), Cournot fee minus c d/(3b), DWL d^2/(8b) and d^2/(18b), profit gap d^2/(36b), "
        "W(2d/3) - W(d/2) = 5d^2/(72b). Bounds in the proof (d/6 > b >= 1; d/(6b) > 1; d^2/(18b) > 2b; 5d^2/(72b) > 5b/2; d^2/(36b) > b; "
        "2d^2/(9b) > 8b) re-checked by hand. rederive_r3.out: 0 strict-order failures over 10000 instance seeds and over 220200 "
        "whole-number cases (b 1..10, c 1..60, gap 6b+1..400).",
    ),
    row(
        "E1d-r1-conventions", "2.6-spec", "course/modules/E/E1/project.html line 329 (Conventions)",
        "PASS",
        "Mapping checked against the statements: Propositions 1-3 give volume, fee and profit of each structure; Proposition 4 gives CS, "
        "welfare and DWL. Monopoly d/2 and (a+bc)/(2b); Cournot 2d/3 and (a+2bc)/(3b); Bertrand d and c; all match Propositions 1-3.",
    ),
    row(
        "E1d-r1-notation", "13-notation", "course/modules/E/E1/project.html math spans (348 \\( ... \\) spans); notation/notation.json",
        "PASS",
        "notation.json registers T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. The page's math uses only the commands "
        "\\cdot \\max \\mapsto \\int \\big \\pi \\ge \\square \\le \\in \\lfloor \\rfloor and letters a b c d e f g i j k n q t x G Q W (counted "
        "by script). None of the registered symbols appears; plain Q is a quantity, not \\mathbb{Q}. e_k is defined at its first use "
        "(Proposition 2), G and W in the Proposition 4 proof, f_1 and f_2 in Proposition 3.",
    ),
    row(
        "E1d-r1-dag", "14-dag", "course/modules/E/E1/project.html line 370 (brief); course/modules/E/E1/L05.html, L06.html, L07.html h1",
        "PASS",
        "tools/check_dag.py --unit E1: 'check_dag E1: PASS' (scripts/E1-d-r3/check_dag.out). The brief's 'Lessons 5 to 7' are L05 Monopoly "
        "Pricing, L06 Oligopoly: Cournot and Bertrand, L07 Surplus and Deadweight Loss. project.html has no concept links (grep 'concept' empty).",
    ),
    row(
        "E1d-r1-process-words", "12-process-words", "course/modules/E/E1/project.html (whole file)",
        "PASS",
        "grep -i for verifier, builder, 'round N', TODO, placeholder, agent, AI, FIXME: no matches. tools/check_pages.py --unit E1: "
        "'check_pages E1: PASS' (scripts/E1-d-r3/check_pages.out).",
    ),
    row(
        "E1d-r1-citation", "3-attribution", "course/modules/E/E1/project.html lines 568-574 (Reading); references/references.json key varian2014intermediate (line 22012)",
        "PASS",
        "Line 570: 'No passage locator from it has been confirmed, so the propositions attribute no statement to it.' No statement is attributed. "
        "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (scripts/E1-d-r3/verify_refs_offline.out).",
    ),
    row(
        "E1d-r1-autograder-reference", "2.6-autograder", "course/modules/E/E1/grader/reference.py; tools/run_graders.py",
        "PASS",
        "tools/run_graders.py --unit E1 --seeds 0-49: 'run_graders E1: PASS (reference 50/50 seeds, slowest 0.2 s)' (scripts/E1-d-r3/run_graders.out). "
        "Suite on reference as market_structure.py, seed 0: '124 passed' (scripts/E1-d-r3/ref_seed0.out).",
    ),
    row(
        "E1d-r1-autograder-count", "2.6-autograder", "course/modules/E/E1/project.html line 323; grader/test_project.py",
        "PASS",
        "pytest --collect-only -q test_project.py in a scratch copy (grader files plus reference as market_structure.py): '124 tests collected' "
        "(scripts/E1-d-r3/collect_only.out). The page says 124 checks.",
    ),
    row(
        "E1d-r1-autograder-instances", "2.6-autograder", "course/modules/E/E1/grader/instance.py lines 3-13; project.html line 317",
        "PASS",
        "rederive_r3.out: over seeds 0..9999, b in [1,3], c in [5,60], gap in [60,400], zero invalid cases, gap > 6b on every seed. "
        "The docstring (instance.py lines 3-13) and page line 317 agree with these ranges.",
    ),
    row(
        "E1d-r1-autograder-messages", "2.6-autograder", "course/modules/E/E1/grader/test_project.py lines 9-12, 50-102, 114-398",
        "PASS",
        "Read all 124 test bodies. check(), must_raise() and pytest.fail messages name the property and interpolate no expected value; the "
        "only interpolated text is the parametrised input and the condition name. The docstring (lines 9-12) matches exact() line 71 "
        "('fee is the inverse demand at the volume'). The oracle imports only market_structure, instance and pytest, not reference.",
    ),
    row(
        "E1d-r1-autograder-browser", "2.6-autograder", "course/modules/E/E1/project.html lines 355, 361-362, 587; course/assets/js/python.js line 4; course/assets/js/grader.js line 18",
        "PASS",
        "tools/page_smoke.py --unit E1 --pages project: 'page_smoke E1: PASS'; in-browser 'All 124 tests pass' and labs 0.0 s each "
        "(scripts/E1-d-r3/page_smoke.out). python.js line 4 TIMEOUT_MS = 120000 matches the 120 seconds of line 321. grader.js saves the "
        "learner's code through store.js (IndexedDB) and only issues GET requests for suite files (grader.js line 18); no upload path, "
        "so the footer claim (line 587) holds.",
    ),
    row(
        "E1d-r1-mutants-existing", "2.6-mutants", "ledgers/E1/mutants/ (142 files at this pin); tools/mutate_graders.py --unit E1 --seeds 0-49",
        "PASS",
        "scripts/E1-d-r3/mutate_all_0_49.out: 'mutate_graders E1: PASS (142/142 killed)', exit 0. The 136 files that existed before this "
        "round, plus the 6 round-3 mutants, are all killed on seeds 0-49.",
    ),
    row(
        "E1d-r1-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r1_m01..m06*.py",
        "PASS",
        "All six round-1 mutants are KILLED in the same run (mutate_all_0_49.out).",
    ),
    row(
        "E1d-r2-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r2_m01..m05*.py",
        "PASS",
        "The five round-2 student-error mutants are KILLED in the same run (mutate_all_0_49.out).",
    ),
    row(
        "E1d-r3-mutants-new", "2.6-mutants", "ledgers/E1/mutants/e1d_r3_m01..m06*.py (generated by scripts/E1-d-r3/make_mutants_r3.py from grader/reference.py)",
        "PASS",
        "Six new student-error mutants, each a single replacement in reference.py (the script asserts each pattern matches once): "
        "m01 Python round() so a tie goes to even; m02 deadweight from half_up(volume); m03 strict a < b*c accepts a = bc; "
        "m04 structure lowercased, so 'Monopoly' is accepted; m05 consumer surplus = fee*volume; m06 float rounding. All six KILLED on seeds 0-49 "
        "(mutate_all_0_49.out, killed_by column of this fragment).",
    ),
    row(
        "E1d-r1-alternatives", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r2/alternatives/ alt_a, alt_b, alt_c, alt_d_decimal_quantize, alt_d_iterate_cutoff, alt_e, alt_g",
        "PASS",
        "scripts/E1-d-r3/alternatives_r2_folder_seeds_0_9.out: each of these seven correct alternatives passes test_project.py on seeds 0-9 "
        "(exit 0 for every seed, run with python -I, --assert=plain -W error).",
    ),
    row(
        "E1d-r2-alternatives-new", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r2/alternatives/alt_f_cournot_iteration_200.py",
        "PASS",
        "alt_f takes the Cournot quantity from 200 best-response steps, which is inexact by d/(3*2^200). It fails "
        "test_tie_rounds_up_for_each_output[cournot-consumer_surplus_cents-31-4-1] on every seed 0-9 (alternatives_r2_folder_seeds_0_9.out). "
        "The page requires each money output to be an exact fraction computed from a, b and c (line 321), so the rejection is the specification, "
        "not an over-constraint.",
    ),
    row(
        "E1d-r3-alternatives", "2.6-alternatives", "ledgers/E1/scripts/E1-d-r3/alternatives/alt_r3_a_decimal_half_up.py, alt_r3_b_integer_rounding.py, alt_r3_c_cramer_simpson.py",
        "PASS",
        "Three new correct alternatives written this round: Decimal at 60 digits with ROUND_HALF_UP; integer numerator and denominator rounded "
        "by (2n+m)//(2m) with no Fraction; Cramer's rule for the Cournot system with Simpson integrals and a different check order. Each passes "
        "test_project.py on seeds 0-9 (alternatives_seeds_0_9.out, 30 of 30 runs exit 0).",
    ),
    row(
        "E1d-r1-rubric-structure", "2.6-rubric", "course/modules/E/E1/project.html lines 385-396 (rubric table)",
        "PASS",
        "Six criteria, four levels each. Each level 4 begins 'Everything in level 3'; every level 2 and level 3 descriptor names a checkable element "
        "(for example C3 level 3: 'the rounding rule stated in cents and one example of a tie'). Descriptors are observable.",
    ),
    row(
        "E1d-r1-rubric-C6-observable", "2.6-rubric", "course/modules/E/E1/project.html line 394 (C6 level 2); line 544 (Exemplar B annotation)",
        "PASS",
        "C6 level 2 reads 'Names one or more of the limits. What changes without each limit need not be stated at this level.' Observable: "
        "one can check whether one to three limits are named.",
    ),
    row(
        "E1d-r1-exemplar-annotations", "2.6-rubric", "course/modules/E/E1/project.html lines 412-413 (Exemplar A C4), 477 (Exemplar B C4), 424-461 (A annotations), 510-546 (B annotations)",
        "PASS",
        "Factual check of each annotation's stated reason against its passage; no exemplar level was scored here (ruling 23). Round-1 FAIL fixed: "
        "line 413 now says the welfare ordering 'gives no printed numbers or differences'; Exemplar A's Summary (line 408) states only the sign "
        "('welfare is lower under monopoly'), with no printed numbers, so the reason is correct. Line 477 now names the missing element ('It gives no "
        "printed difference; the Comparison passage gives them'); the Summary does give the printed fees and welfare of monopoly and Cournot. "
        "Lines 461, 544-546 agree with the Limits passages (lines 461, 540) and with the stated limits. Lines 437-450 agree with the Derivations "
        "and Welfare passages (433, 445).",
    ),
    row(
        "E1d-r1-data-simulated", "11-data", "course/modules/E/E1/project.html lines 53, 62, 195, 317; grader/instance.py line 3",
        "PASS",
        "Page: 'No data file is read ... not market data' (53), 'not market data' (62, 195), 'It is SIMULATED ... None of it is exchange data' (317). "
        "instance.py line 3: 'returns a SIMULATED case'. No open() or fetch of data in the three labs.",
    ),
    row(
        "E1d-r1-gates", "gates", "repository gates on checkout 8196077d (slice-scoped)",
        "PASS",
        "check_pages E1 PASS; check_dag E1 PASS; check_projects E1 PASS; run_labs E1 --page project PASS (3/3); run_graders E1 --seeds 0-49 PASS "
        "(50/50); page_smoke project PASS; mutate_graders E1 --seeds 0-49 142/142 killed; verify_refs --offline 560 entries, 0 problems; "
        "ruff check and ruff format --check on the 3 project twins and grader PASS; mypy --no-incremental on the 3 twins PASS; "
        "pytest tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_labs.py tests/test_run_labs.py PASS. Logs in scripts/E1-d-r3/.",
    ),
    row(
        "E1d-r1-structure-order", "2.5-structure", "course/modules/E/E1/project.html section order (lines 40, 51, 261, 311, 334, 352, 358, 365, 559, 568)",
        "PASS",
        "Section order: ladder, rungs, model, spec, hours, autograder, local run, memo, stretch, reading, references. tools/check_projects.py "
        "--unit E1: PASS. (The Lab 3 placement inside the rungs section is recorded separately in E1d-r3-lab3-placement.)",
    ),
    row(
        "E1d-r1-atlas-studio", "2.5-structure", "course/modules/E/E1/project.html (whole file)",
        "PASS",
        "grep -i -E 'atlas|studio' course/modules/E/E1/project.html: no matches.",
    ),
    row(
        "E1d-r1-docstring-units", "2.5-lab", "course/modules/E/E1/project.html line 159; tests/labs/E1/lab-E1-project-2.py line 27",
        "PASS",
        "Both read 'q_i = (d - q_j) / 2, in trades' (page line 159; twin line 27). The diff between page code and twin shows no difference on that line.",
    ),
    row(
        "E1d-r3-lab3-placement", "2.5-structure",
        "course/modules/E/E1/project.html line 42 (ladder: skip rungs 1 and 2), lines 51-259 (section id=rungs 'Rungs 1 and 2'), "
        "lines 189-258 (lab-E1-project-3), line 53 ('Both labs use the reference case'), line 319 (run_report.py = Lab 3), line 367 (memo numbers are Lab 3's)",
        "FAIL",
        "Lab 3 sits inside section id='rungs', whose heading is 'Rungs 1 and 2'. Line 42 tells a placed learner to skip rungs 1 and 2. "
        "BUILDER_RULES 5.1 says rung 3 is 'Never' skippable, and the plan (E1-build-plan.md section 5.2 item 3) calls lab-E1-project-3 the "
        "'rung-3 check'. The spec at line 319 requires run_report.py, which is Lab 3 with a changed call, and line 367 says the memo's numbers "
        "are the ones Lab 3 prints. A placed learner therefore skips a required deliverable template. Line 53 says 'Both labs' while the section "
        "holds three labs. check_projects.py does not test placement, so it passes.",
        "Move the lab-E1-project-3 section (lines 189-258) out of section id='rungs', for example to just before section id='spec' or into the memo "
        "section before 'The brief' (line 369), and give it its own rung-3 heading. Change line 53 to name Labs 1 and 2 only. Re-run "
        "tools/check_projects.py --unit E1, tools/run_labs.py --unit E1 --page project and tools/page_smoke.py --unit E1 --pages project.",
    ),
    row(
        "E1d-r3-run-report", "2.5-lab", "course/modules/E/E1/project.html lines 191, 195-197, 319; tests/labs/E1/lab-E1-project-3.py",
        "PASS",
        "Copied the Lab 3 twin to run_report.py, replaced closed_form_outcome with outcome from grader/reference.py as market_structure.py, and ran "
        "it with -W error: exit 0, empty stderr, and its output equals the Lab 3 expected block (scripts/E1-d-r3/run_report_check.out). This "
        "matches the claim 'Your run_report.py must print the same lines' (line 191).",
    ),
    row(
        "E1d-r3-starter-signature", "2.6-autograder", "course/modules/E/E1/grader/starter.py line 16; project.html line 319",
        "PASS",
        "starter.py: 'def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:'; page line 319 gives the same signature and the same "
        "six keys.",
    ),
    row(
        "E1d-r3-numbers-prose", "2.2-numbers", "course/modules/E/E1/project.html prose numbers: lines 57, 127, 132, 139, 186, 191, 257, 287-307, 317, 329, 400-550 (exemplar text)",
        "PASS",
        "Every number in the lab, proposition and specification prose re-derived exactly by scripts/E1-d-r3/rederive_r3.py (the a=120 and a=121 "
        "tables, 40000/9, 160/3, 10201/4, 5000/9, 555.56, 277.8, the +17/+33 trades and -17/-33 cents and +694/+556 cents differences in exemplar B "
        "line 517). No mismatch found.",
    ),
    row(
        "E1d-r3-scope-words", "2.4-scope", "course/modules/E/E1/project.html lines 283, 321, 323",
        "PASS",
        "'Each proposition lists the assumptions its proof uses' (283): the proofs use only a > bc > 0, b > 0, d > 0, q_i >= 0, f_i in [0, a/b] "
        "and Q in [0, d], all listed. 'Any other invalid input may raise any exception or return a value' (321) matches the test file, which "
        "demands ValueError only for the four named conditions. 'Each is graded T' (283) is consistent with the proofs read.",
    ),
    row(
        "E1d-r3-terms-before-definition", "2.4-defs", "course/modules/E/E1/project.html lines 37, 53, 57, 133-140 (Lab 2 hypothesis), 265-279 (Definitions)",
        "PASS",
        "Terms used in the rungs before the Definitions (monopoly, Cournot, Bertrand, fee, volume, welfare, deadweight loss) are pointed to the "
        "model section by the lede (line 37: 'Each output is defined in the model section'), line 53 ('defined under Definitions'), and "
        "the Constraints (line 57). Proposition 2 is cited by name where used (line 132).",
    ),
]


def mutant_entries() -> list[dict]:
    text = (S / "mutate_all_0_49.out").read_text(encoding="utf-8")
    entries = []
    pattern = re.compile(r"^(KILLED|SURVIVED) (\S+?): (.*?) -> (.*)$", re.M)
    for status, name, description, killed in pattern.findall(text):
        entries.append(
            {
                "id": name.removesuffix(".py"),
                "description": description,
                "killed_by": killed if status == "KILLED" else None,
            }
        )
    return entries


def main() -> None:
    mutants = mutant_entries()
    assert len(mutants) == 142, len(mutants)
    fragment = {
        "unit": "E1",
        "slice": "d",
        "round": 3,
        "verifier": "verifyS3-E1-d (Haiku 5.5)",
        "pin": PIN,
        "base": BASE,
        "checkout": str(CHECKOUT),
        "scratch": "/tmp/e1d_r3",
        "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "verdict": "FAIL",
        "rows": ROWS,
        "mutants": mutants,
        "registry_flags": [],
        "freshness_flags": [],
        "notes": (
            "Round 3 on 8196077d. Previous pin 9294b914 (round 2). Delta 9294b914..8196077d within the slice: "
            "course/modules/E/E1/project.html (lines 304-307 Proposition 5 proof extended; lines 409-412 and 474-477 annotations changed) and "
            "five new ledgers/E1/mutants/e1d_r2_m01..m05 files were added earlier in the delta. grader/*, tests/labs/E1/lab-E1-project-1..3.py "
            "are byte-identical to 9294b914 (git diff empty). Every row was re-verified this round from the files and command outputs in "
            "scripts/E1-d-r3/, not carried. Exemplar scoring is not done here (ruling 23): the rubric-calibration and blind-scoring rows of "
            "round 2 are not carried. Not run: the full repository gate (full pytest suite, full ruff, full mypy, live verify_refs), "
            "the live Chrome UI (page_smoke used the repository's Chromium run), and any commit or push. The checkout has an untracked "
            ".venv symlink and the new files under ledgers/E1/scripts/E1-d-r3/ and ledgers/E1/mutants/."
        ),
        "summary": (
            "Slice d round 3 at 8196077d: verdict FAIL. 1 FAIL row: E1d-r3-lab3-placement (Lab 3 sits inside the skippable "
            "'Rungs 1 and 2' section while the spec requires run_report.py from it). All numeric, proof, grader, lab, mutant "
            "(142/142 killed) and alternative (correct engines pass seeds 0-9) checks PASS."
        ),
    }
    counts: dict[str, int] = {}
    for r in ROWS:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    fragment["summary"] += f" Rows: {len(ROWS)} ({counts})."
    OUT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote", OUT, "rows", len(ROWS), counts, "mutants", len(mutants))


if __name__ == "__main__":
    main()
