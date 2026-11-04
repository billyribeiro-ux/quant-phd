"""Build the round-5 fragment ledgers/FC2/FC2-d.json from the round-4 row ids and this round's evidence.

Usage: python3 -I ledgers/FC2/scripts/FC2-d-r5/build_fragment_r5.py <repo_root> <round4_fragment_path>
Every round-4 row id is kept. Rows re-run this round carry fresh evidence; rows whose cited subject is byte-identical
to the round-4 pin (4eb6788) carry the prefix 'Carried from round 4 (...)'. Mutants are read from the gate output.
"""

import json
import os
import re
import sys
from datetime import UTC, datetime

root = sys.argv[1]
r4 = json.load(open(sys.argv[2], encoding="utf-8"))
S = "ledgers/FC2/scripts/FC2-d-r5"
CARRY_CARDS = "course/modules/FC/FC2/cards.json per-card JSON byte-identical to 4eb6788 and L0x.html unchanged in 4eb6788..440ed3c"
CARRY_GRADER = "grader/test_project.py byte-identical since the previous pin 4eb6788"

fresh = {
    "fc2d-r2-gate-mutate": (
        "PASS",
        f"Command: tools/mutate_graders.py --unit FC2 --seeds 0-9, rc=0, {S}/mutate_fc2_r5.out: 'mutate_graders FC2: PASS (68/68 killed)'. "
        "65 prior mutants plus the three round-5 mutants w5_a..w5_c.",
    ),
    "fc2d-r2-gate-run-graders": (
        "PASS",
        f"Command: tools/run_graders.py --unit FC2 --seeds 0-49, rc=0, {S}/run_graders.out: 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.2 s)'.",
    ),
    "fc2d-r2-gate-check-projects": (
        "PASS",
        f"Commands: check_projects.py --unit FC2 ({S}/check_projects_fc2.out: 'check_projects FC2: PASS') and --all ({S}/check_projects_all.out, rc=0).",
    ),
    "fc2d-r2-gate-check-dag": (
        "PASS",
        f"Commands: check_dag.py --unit FC2 ({S}/check_dag_fc2.out: 'check_dag FC2: PASS') and --all ({S}/check_dag_all.out, rc=0, FC2 line PASS).",
    ),
    "fc2d-r2-gate-check-pages": (
        "PASS",
        f"Commands: check_pages.py --unit FC2 ({S}/check_pages_fc2.out: 'check_pages FC2: PASS') and --all ({S}/check_pages_all.out: 21 PASS lines, rc=0).",
    ),
    "fc2d-r2-gate-run-labs": (
        "PASS",
        f"Command: tools/run_labs.py --unit FC2, rc=0, {S}/run_labs_fc2.out: 'run_labs FC2: PASS (11/11)'.",
    ),
    "fc2d-r2-lab-twins-isolated": (
        "PASS",
        f"Script {S}/twins_isolated.py (run as python -I), output {S}/twins_isolated.out: lab-FC2-project-1, -2 and -3 twins each copied alone into an empty temp directory and run with python -I -W error: rc 0, stderr_bytes 0.",
    ),
    "fc2d-r2-lab-page-equals-twin": (
        "PASS",
        f"{S}/twins_isolated.out: expected block equals twin stdout for all three project labs (True). Page code equals twin for labs 1 and 3 (True). Lab 2 is a completion lab: {S}/lab2_completion_rule.py (output {S}/lab2_completion_rule.out) shows 89 page lines and 89 twin lines, 3 blank lines (58, 60, 73), no other differing line: 'rule holds: True'.",
    ),
    "fc2d-r2-gate-page-smoke": (
        "PASS",
        f"Command: tools/page_smoke.py --unit FC2 --pages project, rc=0, {S}/page_smoke_project.out: 'page_smoke modules/FC/FC2/project.html: PASS', 'in-browser grader: All 90 tests pass on seed 111818396', labs 1-3 at 0.0 s.",
    ),
    "fc2d-r2-gate-ruff-mypy": (
        "PASS",
        f"Scope: FC2 paths. {S}/ruff_check.out 'All checks passed!' (repo-wide); {S}/ruff_format_fc2.out '15 files already formatted' for tests/labs/FC2, course/modules/FC/FC2, ledgers/FC2; {S}/mypy_labs.out 'Success: no issues found in 11 source files' (mypy --no-incremental tests/labs/FC2); {S}/mypy_grader_strict.out 'Success: no issues found in 3 source files' (mypy --strict on a scratch copy of reference.py as scanner.py, instance.py, test_project.py). Outside the slice: repo-wide 'ruff format --check .' reports 1 file, ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py ({S}/ruff_format.out); not FC2.",
    ),
    "fc2d-r2-gate-pytest-fc2": (
        "PASS",
        f"Command: .venv/bin/python -m pytest tests/labs/FC2 tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py -k 'FC2 or fc2 or project or grader' -q, rc=0, output {S}/pytest_fc2.out (all dots, no failures; the -q summary line is suppressed by the repo's pytest configuration).",
    ),
    "fc2d-r2-gate-verify-refs": (
        "PASS",
        f"{S}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems' rc=0. {S}/verify_refs_unit_FC2.out: 'live re-verification of FC2: 3 of 560 entries, 0 problems' rc=0.",
    ),
    "fc2d-r2-collect-count": (
        "PASS",
        f"Script {S}/collect_count.py (python -I), output {S}/collect_count.out: 'collected 90 for 50 seeds' (seeds 0..49, reference.py as scanner.py, pytest --collect-only). Page states 90 (project.html line 320).",
    ),
    "fc2d-r2-starter-suite-fails": (
        "PASS",
        f"Script {S}/instances_and_links_r5.py, output {S}/instances_and_links_r5.out: starter.py as scanner.py, QF_SEED=0, '82 failed, 8 passed', rc 1.",
    ),
    "fc2d-r2-numbers-lab1": (
        "PASS",
        "Re-derived by hand from the Lab 1 chain (project.html lines 70-77 and 147-162): gaps 120 at 9500, -20 at 11000, zero at 9000, 10000, 10500, 11500; cost 3 x 15 = 45; nets 75 and -25; chord less call at 9500 = 50, 10000 = 100, 10500 = -75 (chord 625, call 700), 11000 = 75; kept 2, net 30 at 10500. Matches the printed expected block and the interpretation line 163 (lines 'four parity gaps exactly zero', 'other three interior strikes on or below the chord'). Also agrees with Lab 2's interpretation (line 274).",
    ),
    "fc2d-r2-numbers-lab3": (
        "PASS",
        "Re-derived by hand from the Lab 3 chain (project.html lines 392-399): gaps 0, -60, 0, 0, 226, 540 at 4000..7000; cost 3 x 20 = 60; chord less call 35 (4500), 470/3 (5000), -188/3 (6000, gross 63 after half-up of 62.67, net 3), 59 (6500); kept 3. Interpretation at line 486 (226/166, 540/480, 63/3, -60 gross equals cost, net 0) and the 'about minus 62.67' value (188/3 = 62.667) agree. Verified with the same arithmetic the twin prints.",
    ),
    "fc2d-r2-numbers-exemplars": (
        "PASS",
        "Exemplar B (project.html lines 526-566): 6500 parity: 151 - 1100 - (5000 - 6175) = 226, net 166; 7000 parity: 90 - 1200 - (5000 - 6650) = 540, net 480; convexity at 6000: (500 + 2 x 151)/3 = 802/3, minus 330 = -188/3, gross 63, net 3; discounted strikes 6175 and 6650 are 6500 x 0.95 and 7000 x 0.95. Exemplar A (lines 590, 602): 226, 540, 63 quoted as 'about' values, all equal to the exact values. Exemplar B 'a cost of 60 cents' = 3 x (8 + 12).",
    ),
    "fc2d-r2-hours": (
        "PASS",
        "project.html table (lines 345-352): 2 + 3 + 5 + 9 + 3 + 5 + 3 = 30 = data-hours-project (line 33) = hub index.html data-hours-project=\"30\"; hub data-hours-lessons=\"60\" = L01..L08 data-hours 6+8+9+7+8+8+8+6 = 60; 60 + 30 = 90 = curriculum/02-economics-finance-core.yaml:399 and curriculum.json FC2 hours 90. Verifier estimate (rule 2.6), component by component: rung 1 1.5-2 h, rung 2 2-3 h, derivations 3-4 h, scanner.py 6-9 h, edge cases 2-3 h, note 4-5 h, self-assessment 2-3 h. Best estimate about 25 h (sum of the midpoints), 17 percent below the declared 30 and inside the 30 percent band [21, 39]. The lowest sum of the ranges (about 20 h) is just below the band, so the declared 30 is at the upper end of the estimate; not a failure.",
    ),
    "fc2d-r2-banned-phrases": (
        "PASS",
        "Grep over project.html for TODO, TBD, lorem, ellipsis placeholders, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'well known', 'obviously', 'clearly', 'historically', 'roughly', 'approximately', 'we', 'our', 'let us': no hits. 'about [0-9]' hits at lines 486 (derived 188/3 rounded to two decimals) and 590 (deliberately weak Exemplar A, value grounded in Lab 3). No process words (builder, verifier, round, pinned).",
    ),
    "fc2d-r2-notation": (
        "PASS",
        "project.html symbols: C, P, S, K, df, D (line 335: 'which the lessons write as D'; L05.html line 59 uses D = discount factor) and the labels P1..P6. None of the registered symbols of notation/notation.json (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) and no registered macro appears on the page (grep for backslash macros and the symbols: no hits). Local letters are defined on the page (conventions, lines 333-336).",
    ),
    "fc2d-r2-dag": (
        "PASS",
        f"{S}/check_dag_fc2.out: 'check_dag FC2: PASS'. Concept links on project.html: arbitrage-opportunity (L01 def-arbitrage-opportunity), put-call-parity and option-arbitrage-bounds (L05 def-put-call-parity, def-option-arbitrage-bounds); all three anchors exist. bid-ask spread (FC1) appears in P6 as plain prose; curriculum/02-economics-finance-core.yaml:400 now lists FC1 as a prerequisite of FC2, so the term is inside the closure (not a DAG violation).",
    ),
    "fc2d-r2-reading-keys": (
        "PASS",
        "project.html reading list (lines 653-657): data-cite hull2021options, stoll1969relationship, cox1979option. references/references.json entries (verified, used_by FC2): cox1979option (DOI 10.1016/0304-405x(79)90015-1), hull2021options (no DOI, year 2021), stoll1969relationship (DOI 10.1111/j.1540-6261.1969.tb01694.x). Cited theorems: 'Theorem 1.2 of Lesson 5' = L05.html line 63 put-call parity; 'Theorem 3.2 of Lesson 5' = L05.html line 115 convexity in strike; 'Theorem 2.2' (instance.py docstring and bounds) = L05.html line 84 model-free bounds (also L05 line 454 lists 0 <= C <= S, C >= max(S - DK, 0), 0 <= P <= DK, P >= max(DK - S, 0)).",
    ),
    "fc2d-r2-scope-curriculum-brief": (
        "FAIL",
        "Re-verified this round. curriculum/02-economics-finance-core.yaml:427-429 still reads 'Given an embedded option-chain snapshot' (unchanged since 4eb6788; the curriculum is not in the delta). project.html line 285 says 'No market data is embedded ... every chain on this page and in the autograder is a simulation, labelled SIMULATED'. plans/FC2-build-plan.md B1 (line 449) records the planner's recommendation of SIMULATED, and the binding architect default (plan 'Architect decisions', line 634) allows SIMULATED with an honest-pending note and a DATA_REQUEST (plans/FC2-open-items.md D1). So the page follows the architect default, but Rung 3 does not match the curriculum scope exactly as the rule requires.",
    ),
    "fc2d-r2-rubric-C2-level2": (
        "PASS",
        "project.html rubric table lines 508-512, read in full this round. Each descriptor names an element a grader can see (legs, cost model, net, classes, labels P1-P6, the check that settles a finding). Observation (not a vague descriptor): C2 level 4 asks for 'the gap between the net and zero'; the net amount is that gap, so the level-4 element is stated only implicitly (Exemplar B's annotation claims it). Recorded in notes.",
    ),
    "fc2d-r2-rubric-calibration": (
        "PASS",
        "Blind scores (rubric text only, read before the exemplar annotations were compared): Exemplar B 4,4,3,3,3 against official 4,4,3,3,3 (data-scores line 520). Exemplar A 2,1,2,2,1 against official 2,1,1,2,1 (data-scores line 584). Only C3 of Exemplar A differs, by one level: the cell for level 1 says 'No assumption named', and the exemplar names 'the discount factor' for the parity findings, which fits level 2 'Names assumptions for some findings'; the annotation's reason ('names no assumption by label') is not the cell wording. Within one level, so the calibration rule passes; recorded in notes.",
    ),
    "fc2d-r2-spec-questions": (
        "PASS",
        "Questions a competent student would still have, read from project.html lines 280-336 and reference.py: (1) which strike a convexity record reports: the interior (middle) strike, answered only by the printed output of Lab 1 ('convexity at strike 10500'); (2) what the gross of a convexity finding is: the magnitude of the chord less the call, answered only by Lab 1's printed 'chord less call -75, gross 75'. Both are answerable from the page; neither is blocking. Every other question checked (rounding, half-cent ties, cost, order of findings, record keys, df range, lengths) is stated.",
    ),
    "fc2d-r2-grader-messages": (
        "PASS",
        "grader/test_project.py lines 139-826 and reference.py lines 24-56 read in full: each ValueError message names its condition (strictly increasing and positive; df_ppm must lie in 1 to 1000000; the two lengths; non-negative cost terms). Assertion texts state the property and never print expected values (--assert=plain in the local and browser commands).",
    ),
    "fc2d-r2-grader-named-conditions-only": (
        "PASS",
        "Every pytest.raises in grader/test_project.py (lines 283-559) names ValueError only, and each one is a named condition of project.html lines 309-316 (strikes, df_ppm, quote lengths, cost terms). No test demands an exception type for an unnamed input (lines 281-298, 301-307, 435-531, 544-559).",
    ),
    "fc2d-r2-instances": (
        "PASS",
        f"Script {S}/instances_and_links_r5.py, output {S}/instances_and_links_r5.out: 40 seeds (0..19 and 1000..1019): all valid (six strikes, strictly increasing, df_ppm in 1..1000000, cost terms non-negative, label SIMULATED); planted kinds vary (none, parity, convexity); 40 distinct (kind, index, amount, strikes, spot, df) tuples.",
    ),
    "fc2d-r2-grader-over-constraint-case": (
        "PASS",
        f"Runner {S}/run_alts_r5.py (copied from the round-4 runner), outputs {S}/alts_r5_alt7.out and {S}/alts_r4_set_at_pin.out. Alternatives pass 50/50 seeds and agree 3000/3000 with reference.py on random chains: round-4 alt1, alt2, alt4, alt5, alt6; the tracked FC2-d-r5/alts alt1..alt5 (committed at the pin); and the new alt7 (cross-multiplied integers, unequal spacing). The float alternative of plan §5.5 item 3 fails one hand-built test (test_parity_exact_tie_at_a_non_dyadic_discount_factor, df 580000, gap 14.5 cents): project.html line 308 states 'computed from exact fractions', so that alternative is not a correct implementation under the page. Not over-constraint; recorded in notes.",
    ),
    "fc2d-r2-grader-over-constraint-trade-verb": (
        "PASS",
        f"Carried from round 4 ({CARRY_GRADER}; the round-4 test removal stays in place): the exact alternatives pass (see fc2d-r2-grader-over-constraint-case) and grader/test_project.py contains no trade-verb test at lines 599-648 in the pinned tree.",
    ),
    "fc2d-r2-alternatives-pass": (
        "PASS",
        "Five or more exact alternatives pass seeds 0..49 (see fc2d-r2-grader-over-constraint-case for the list and outputs). Plan §5.5 alternative 3 (float) is the one that fails; excluded because project.html line 308 requires exact fractions, and the failing test enforces that sentence. Flagged for the architect as a plan-versus-page conflict.",
    ),
    "fc2d-r2-mut-r7-docstrings": (
        "PASS",
        f"Script {S}/mutant_docstrings_r5.py, output {S}/mutant_docstrings_r5.out: 68 mutants; each first docstring line names the error (none flagged), each differs from reference.py in 4 to 8 lines.",
    ),
    "fc2d-r2-mut-new-killed": (
        "PASS",
        f"{S}/mutate_fc2_r5.out: v07_convexity_indices_returned_in_decreasing_order, v08_convexity_scan_skips_first_interior_strike, v09_parity_explanation_omits_P3_no_income, v10_convexity_gross_from_rounded_chord all KILLED.",
    ),
    "fc2d-r2-mut-r5d-resolved": (
        "PASS",
        "ledgers/FC2/mutants has no r5_d file (ls); r5_a, r5_b, r5_c are KILLED in mutate_fc2_r5.out.",
    ),
    "fc2d-r2-mut-equivalents": (
        "PASS",
        "No listed mutant is equivalent: each round-5 mutant is distinguished by a test (w5_a by test_parity_tie_of_one_half_goes_up; w5_b by test_calls_longer_than_strikes_is_rejected; w5_c by test_scan_matches_exhaustive_oracle_second_chain, seed 4). The probe in direction_probe.py is not a listed mutant (see notes).",
    ),
    "fc2d-r2-cards-full-scan": (
        "PASS",
        f"Script {S}/cards_scan_r5.py, output {S}/cards_scan_r5.out: 152 cards; unique ids, unique fronts, unique backs; grades T and C; lessons L01..L08. 37 near-duplicate pairs (ratio >= 0.6 on front or back); the top ones were read: FC2-c005 / FC2-c154 (weak versus strict part of Proposition 2.2, distinct claims), c126 / c131 (lower bound at two parameter sets), c102 / c145 (formula versus whether it is derived), c069 / c070 (convexity versus monotonicity). None duplicates another card.",
    ),
    "fc2d-r2-cards-refs-numbers": (
        "PASS",
        f"{S}/cards_scan_r5.out: every numbered item (Proposition, Theorem, Definition, Remark, Lemma, Example, Assumption, Problem, Section) cited by a card occurs in its lesson text, except FC2-c076 '(Section 5)'. Lesson L05 has the heading '5 Where the canon breaks' (L05.html line 314) and the card cites that section; the number is in the lesson as a heading, not as the literal text 'Section 5'. Not a defect of the card; noted.",
    ),
    "fc2d-r2-cards-lab-numbers": (
        "PASS",
        f"Carried from round 4 ({CARRY_CARDS}; tests/labs/FC2 not in the delta): cards c012, c013, c095, c147, c148 agree with their lab twins as read in round 4.",
    ),
}
fresh["fc2d-r2-autograder-panel-claims"] = (
    "PASS",
    "project.html line 285 ('The autograder panel can load a .py file from your device into the editor, and the file is read in this browser') and line 671 footer: course/assets/js/grader.js line 46 creates an input type=file accept=.py; line 75-80 reads it with file.text() into the editor and saves the draft with store.put; line 88-95 fetches only the suite and support files from the site (base URL) and runs them with runPytest in the browser. No upload call exists in grader.js. Lines 285 and 671 unchanged since 4eb6788.",
)
fresh["fc2d-r2-hub-placement-claim"] = (
    "PASS",
    "project.html line 42 ('Rungs 1 and 2 are optional when you reach the placement bar on the module hub and answer both skill checks') and index.html line 148 ('You may skip them when you reach the placement bar and answer both skill checks'); the hub defines the placement diagnostic (index.html line 68-69, nine questions, mastery bar 80 percent). Both sentences are unchanged since 4eb6788; the rung-skip rule is consistent across the two pages.",
)
card_carry = ["c010", "c132", "c020", "c030", "c041", "c051", "c061", "c071", "c082", "c092", "c102", "c112", "c120", "c142"]
for c in card_carry:
    fresh[f"fc2d-r2-card-{c}"] = (
        "PASS",
        f"Carried from round 4 ({CARRY_CARDS}); card FC2-{c} is read against its lesson text as in round 4. Card id and text unchanged since 4eb6788.",
    )
r4_cards = ["c093", "c123", "c124", "c149", "c150", "c152", "c153"]
for c in r4_cards:
    fresh[f"fc2d-r4-card-{c}"] = (
        "PASS",
        f"Carried from round 4 ({CARRY_CARDS}); the round-4 check of FC2-{c} against its lesson stands. Re-confirmed this round: the per-card JSON object of FC2-{c} is identical at 4eb6788 and 440ed3c (script comparison in this round's notes).",
    )
fresh["fc2d-r4-card-c151"] = (
    "PASS",
    "Re-verified from scratch. course/modules/FC/FC2/cards.json FC2-c151 now reads: bisection of Definition 3.1 'started from a bracket with C(sigma_lo) < C* <= C(sigma_hi) and C* in (L, S), and stopped at tolerance tau_tol', back 'Within tau_tol/2 ... (Proposition 3.2)'. L08.html lines 109 and 114-115: Definition 3.1 bracket C(sigma_lo) < C* and C(sigma_hi) >= C*; Proposition 3.2 hypothesis 'sigma_lo,0 < sigma_hi,0 satisfy the bracket condition of Definition 3.1 with C* in (L, S)', conclusion '|sigma-hat - sigma*| <= tau_tol/2'. The card carries C* in (L, S) and the bracket condition; the round-4 omission is fixed. The model (A7, strict monotonicity of C) is not restated on the card; the front names the implied volatility, which the lesson defines under A7, so this is not counted as a missing hypothesis.",
)
fresh["fc2d-r4-cards-sample"] = (
    "PASS",
    f"Carried from round 4 ({CARRY_CARDS}): the round-4 sample of 14 cards (c010, c132, c020, c030, c041, c051, c061, c071, c082, c092, c102, c112, c120, c142) is unchanged; this round's changed cards are checked in the fc2d-r5 rows.",
)
fresh["fc2d-r4-mut-u4-new-killed"] = (
    "PASS",
    f"{S}/mutate_fc2_r5.out: u4_a_parity_explanation_omits_P6, u4_b_cost_ignores_half_spread, u4_c_discounted_strike_floor_division all KILLED.",
)
fresh["fc2d-r3-instance-docstring-bounds"] = (
    "PASS",
    "grader/instance.py lines 13-18 read this round against _draw and _within_bounds (lines 41-60, 110-111): a draw is rejected for an exact half-cent gap or second difference (_is_half_cent), and for a quote more than half a cent outside the Theorem 2.2 bounds (_within_bounds). Docstring matches code.",
)
fresh["fc2d-r3-scope-changed-hunks"] = (
    "PASS",
    "Delta 4eb6788..440ed3c inside the slice, all hunks read: project.html (line 55; lines 309-316 in the 'Constraints' dd), cards.json (c005, c055, c151 changed; c154 added). No change to grader/, labs, or lessons. Command: git diff 4eb6788 440ed3c -- course/modules/FC/FC2 (39 files; FC2 course files 2 files).",
)
fresh["fc2d-r3-df-ppm-link"] = (
    "PASS",
    "Script check over project.html: 17 internal href='#...' targets, 0 missing (internal link targets listed in instances_and_links_r5.out). The #conventions anchor (line 325) exists; the href in line 55 is unchanged.",
)
fresh["fc2d-r3-mut-new-killed"] = (
    "PASS",
    f"{S}/mutate_fc2_r5.out: q3_a_df_rounded_to_four_places, q3_b_gross_tie_toward_zero, q3_c_convexity_charges_two_legs, q3_d_convexity_explanation_omits_P5 all KILLED.",
)
fresh["fc2d-r3-mut-prior-untracked"] = (
    "PASS",
    f"{S}/mutate_fc2_r5.out: r3_a_half_spread_halved_again, r3_b_puts_longer_than_strikes_accepted, r3_c_net_field_reports_gross, r3_d_parity_explanation_names_P5_for_P4 all KILLED.",
)
fresh["fc2d-r3-footer-no-upload"] = (
    "PASS",
    "Carried from round 4: project.html line 285 (Inputs: 'Nothing on this page uploads a file') and line 671 (footer) are byte-identical in 4eb6788..440ed3c (the delta hunks are at lines 55 and 309-316 only).",
)
fresh["fc2d-r3-exemplar-scores-match-text"] = (
    "PASS",
    "project.html line 520 data-scores '4,4,3,3,3' and line 521 text 'C1 4 C2 4 C3 3 C4 3 C5 3' agree; line 584 '2,1,1,2,1' and line 586 'C1 2 C2 1 C3 1 C4 2 C5 1' agree. Annotations read in full (lines 523-634).",
)

rows = []
for old in r4["rows"]:
    rid = old["id"]
    status, evidence = fresh.get(rid, ("PASS", "unassigned"))
    if rid not in fresh:
        raise SystemExit("no round-5 evidence for " + rid)
    row = {"id": rid, "check": old["check"], "location": old["location"], "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = ("Architect: amend curriculum/02-economics-finance-core.yaml lines 427-429 so the project brief names the SIMULATED chain "
                      "(or record the embedded-snapshot departure in plans/FC2-open-items.md with its architect decision); "
                      "the page's Inputs (line 285) and the scanner contract then match the curriculum scope exactly.")
    rows.append(row)

new_rows = [
    ("fc2d-r5-card-c005", "2.7", "course/modules/FC/FC2/cards.json FC2-c005; L01.html lines 84-85 and 94-95",
     "PASS", "Changed this round (back text). Card: 'p·a ≥ p·b (Proposition 2.2). The result uses A3 and nothing else (Remark 2.3).' L01.html line 85: Proposition 2.2 'Assume A3. If (Xa)_s >= (Xb)_s for every state, then p·a >= p·b'; line 95 Remark 2.3: 'Both results use A3 and nothing else'. Agrees; the strict part was moved to c154 and the card no longer claims it."),
    ("fc2d-r5-card-c055", "2.7", "course/modules/FC/FC2/cards.json FC2-c055; L04.html lines 103-104, 110-111, 258",
     "PASS", "Changed this round. Card: 'Yes: V_A(0) ≥ V_E(0) (Proposition 2.3). The proof gives this weak inequality and nothing more.' L04.html line 104: Proposition 2.3 under A2, A3 and A5, V_A(0) >= V_E(0); line 111 Remark 2.4: 'does not say that the inequality is strict'; line 258: 'Proposition 2.3 proves only V_A(0) >= V_E(0)'. Agrees."),
    ("fc2d-r5-card-c154", "2.7", "course/modules/FC/FC2/cards.json FC2-c154; L01.html lines 84-85, 359-361",
     "PASS", "New this round. Card: strict dominance gives p·a > p·b (Proposition 2.2, strict part). L01.html line 85: 'If in addition (Xa)_s > (Xb)_s for every state, then p·a > p·b'. Proof at lines 361: equality would give a zero-cost theta with a strictly positive payoff in every state, excluded by A3 (Definition 1.1 third condition). Card's reasoning agrees. Grade T is consistent with the lesson's proof."),
    ("fc2d-r5-page-hunk-lab1-hypothesis", "2.9", "course/modules/FC/FC2/project.html line 55",
     "PASS", "Changed sentence: '(both terms are defined under P6 in Conventions and assumptions, below)'. P6 (project.html line 333) defines the fee and the half-spread, and the anchor href='#conventions' exists (line 325). Lab 1 numbers unchanged (fc2d-r2-numbers-lab1)."),
    ("fc2d-r5-page-hunk-error-conditions", "2.6", "course/modules/FC/FC2/project.html lines 309-316 against grader/test_project.py and grader/reference.py",
     "PASS", "New sentence (line 309): 'Each condition is checked in every function that receives the input it names, and the grader checks it in each of those functions.' Checked per bullet: strikes in convexity_violations, scan (test lines 441-487) and parity_gap_cents (301-307); df_ppm in parity_gap_cents (281-298), convexity_violations and scan (489-504); calls length in convexity_violations (507-526) and scan (507-532); puts length in scan only (515-532); cost terms in scan only (550-561). reference.py lines 24-56 and 67-76 and 102-115 implement the same checks in the same functions. Bullet 1 wording matches reference.py lines 53-54 for parity_gap_cents. Claim holds."),
    ("fc2d-r5-mut-w5-new-killed", "2.6", "ledgers/FC2/mutants/w5_a_parity_gap_truncated_toward_zero.py, w5_b_length_check_rejects_only_short_lists.py, w5_c_gross_rounded_up_to_ceiling.py",
     "PASS", f"Written this round by {S}/write_mutants_r5.py (one line changed in reference.py each; asserted once). {S}/mutate_fc2_r5.out: all three KILLED (test_parity_tie_of_one_half_goes_up seed 0; test_calls_longer_than_strikes_is_rejected seed 0; test_scan_matches_exhaustive_oracle_second_chain seed 4). Suite total 68/68."),
    ("fc2d-r5-alt7-cross-multiplied", "2.6", f"{S}/alts/alt7_cross_multiplied_integers.py",
     "PASS", f"New alternative: integer-only, cross-multiplied convexity test N = (K3-K2)C1 + (K2-K1)C3 - (K3-K1)C2 with half-up division; passes 50/50 seeds ({S}/alts_r5_alt7.out) and agrees 3000/3000 with reference.py on random chains including uneven spacing and df 1 and 1000000."),
    ("fc2d-r5-explanation-direction-untested", "2.6", "course/modules/FC/FC2/grader/test_project.py lines 587-600; ledgers/FC2/scripts/FC2-d-r5/direction_probe.py",
     "PASS", f"Probe, not a mutant file: a parity explanation with the trade direction swapped passes the suite on seeds 0..9 ({S}/direction_probe.out: rc 0 for every seed). The spec (project.html line 301) requires the explanation to name the rule and the labels, not the direction; so this survivor is not a grader fault under the ruling. Noted for the architect (optional direction check)."),
]
for rid, check, loc, status, ev in new_rows:
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})

mutate_lines = [l for l in open(os.path.join(root, S, "mutate_fc2_r5.out"), encoding="utf-8") if l.startswith("KILLED ")]
mutants = []
for l in mutate_lines:
    m = re.match(r"KILLED (\S+?)\.py: (.*) -> (\S+) \(seed (\d+)\)", l.strip())
    if not m:
        raise SystemExit("cannot parse " + l)
    mutants.append({"name": m.group(1), "description": m.group(2), "killed_by": f"{m.group(3)} (seed {m.group(4)})"})

ledger = {
    "unit": "FC2",
    "slice": "FC2-d",
    "round": 5,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 5 (did not build FC2)",
    "pin": "440ed3c216725d498d9c6d7c746907d4d418198",
    "base": "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b (round-4 pin); delta inside the slice: course/modules/FC/FC2/project.html lines 55 and 309-316; cards.json FC2-c005, c055, c151 changed and FC2-c154 added; mutants w5_a..w5_c added; no grader, lab, lesson, curriculum or plan change",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD5-FC2-d",
    "scratch": "/tmp/fc2d-r5-mypy (mypy scratch copy); /tmp/fc2d-r5-alt7.py (copy of alt7); all other outputs are under ledgers/FC2/scripts/FC2-d-r5/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 5 on 440ed3c. Delta read in full: project.html lines 55 and 309-316; cards c005, c055 (changed), c151 (changed), c154 (new). "
        "Read in full at the pin: project.html (673 lines), grader/reference.py, starter.py, instance.py, test_project.py (826 lines), the three project lab twins. "
        "Cards: all 152 scanned by script (ids, fronts, backs, near-duplicates, cited numbers); the four changed cards checked against L01, L04, L08 text; 14 round-4 sampled cards and 7 round-4 changed cards carried (per-card JSON identical to 4eb6788). "
        "Mutants: 68 in ledgers/FC2/mutants, 68 killed; three new student-error mutants (w5_a..c) written this round. "
        "Alternatives: round-4 set (six), tracked FC2-d-r5/alts (five, present at the pin), and a new alt7; every exact alternative passes 50/50 seeds and agrees 3000/3000 on random chains; the float alternative of plan §5.5 item 3 fails one hand-built test that enforces the page's 'computed from exact fractions' (project.html line 308). "
        "Observations, not rows: (a) plans/FC2-open-items.md still lists bid-ask-spread as a DAG_DEFECT, but curriculum/02-economics-finance-core.yaml:400 now makes FC1 a prerequisite; (b) the repo-wide 'ruff format --check .' fails on ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py (outside FC2); "
        "(c) the explanation trade direction is not tested (direction_probe.out, survives seeds 0..9); the spec requires labels, not direction; (d) rubric C2 level 4 'gap between the net and zero' is implicit, and Exemplar A's C3 annotation (level 2 by label) differs from the cell wording (level 1 'No assumption named'), within one level; "
        "(e) spec questions: which strike a convexity record reports and what its gross is are answered only by Lab 1's printed output. "
        "Not checked: the full repo gate (render_curriculum.py, build_site.py --check, fetch_data.py --check, full pytest, full mypy, verify_refs over all units); the self-assessment form in a live browser (page_smoke passes the page, the form is static here); lessons L01-L07 beyond the cited passages; the hub index.html beyond the placement sentence. Round-4 ids all kept."
    ),
    "summary": {},
}
counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
ledger["summary"] = {
    "rows": len(rows),
    "pass": counts.get("PASS", 0),
    "fail": counts.get("FAIL", 0),
    "unverifiable": counts.get("UNVERIFIABLE", 0),
    "mutants": len(mutants),
    "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
}
out = os.path.join(root, "ledgers", "FC2", "FC2-d.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(ledger, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("wrote", out, ledger["summary"])
