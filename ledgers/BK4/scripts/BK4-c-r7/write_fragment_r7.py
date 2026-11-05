"""Writes the BK4 slice-c round-7 ledger fragment from the verifier's rows and the mutate_graders output.

Usage: write_fragment_r7.py <checkout> <verified_at ISO>
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
VERIFIED_AT = sys.argv[2]
OUT_DIR = "ledgers/BK4/scripts/BK4-c-r7/out"
MUT = (ROOT / OUT_DIR / "mutate_seeds0-9_all53.out").read_text(encoding="utf-8")

PAGE = "course/modules/BK/BK4/project.html"
TEST = "course/modules/BK/BK4/grader/test_project.py"
SCRIPTS = "ledgers/BK4/scripts/BK4-c-r7"


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> dict[str, str]:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    return item


ROWS = [
    row("proj-lab1-numbers", "2.5-labs", f"{PAGE}:56-139; tests/labs/BK4/lab-BK4-project-1.py", "PASS",
        f"run_labs --unit BK4 --page project: PASS (3/3) ({OUT_DIR}/run_labs_project.out); twin alone "
        f"'python -I -W error' exit 0 ({OUT_DIR}/twin_project_1.out). Every hypothesis and interpretation number "
        f"(layers 50000/6000/20000, residual 4000, floored shares 1333/1666/1000 with one leftover cent, survivors "
        f"1334/1666/1000, k 39 from exact position 38.2, margin 117088, cover 9750 and 9500 one cent below, 38 of 40 = 95 %) "
        f"re-derived with Fraction in {SCRIPTS}/rederive_r7.py (out/rederive_r7.out 'lab1' lines)."),
    row("proj-lab2-numbers", "2.5-labs", f"{PAGE}:141-190; tests/labs/BK4/lab-BK4-project-2.py", "PASS",
        f"run_labs PASS for the page (completion rule: page code and twin differ only on the two '___' lines). Twin exit 0 "
        f"({OUT_DIR}/twin_project_2.out): shares {{1: 1334, 3: 1666, 4: 1000}}, k 39, margin 117088. Tolerance check: "
        f"1e-6*(1+117088) = 0.117 < 1 cent, and the rule is labs.js compareOutput (token by token, tol*(1+|expected|)), "
        f"which tools/coursekit.py compare_output mirrors."),
    row("proj-lab3-numbers", "2.5-labs", f"{PAGE}:252-366; tests/labs/BK4/lab-BK4-project-3.py", "PASS",
        f"Twin exit 0 ({OUT_DIR}/twin_project_3.out). Part A losses 20000..100000 re-derived (out/rederive_r7.out 'lab3 loss' "
        f"lines, uncovered 12000 only at 100000). Part B k 36/38/39, margins 105154/111074/117088, covers 9000/9500/9750, one "
        f"cent below 8750/9250/9500 (out 'lab3 target'). Part C past-counts [2,2,0,0] at 9500 and [4,2,0,0] at 9000 (out 'partC'). "
        f"Brute-force agreement holds in the twin output."),
    row("proj-fixture-tables", "2.6-spec, 2.6-tests", f"{PAGE}:229-250; {TEST}:281-368", "PASS",
        "All 11 layer-order rows (losses 80..300, page table) recomputed by an independent oracle with no mismatches "
        "(out/rederive_r7.out 'fixture table rows 11 mismatches []'). Remainder fixture (page :248; test :362-368) gives "
        "{1:1,2:0,3:0}, {1:1,2:1,3:0}, 4 cents -> 1 uncovered (out 'remainder'). Sizing fixtures 40/50/50/20 and cover "
        "fixtures 3333/6666 re-derived (out 'sizing', 'cover fixtures')."),
    row("proj-named-conditions", "2.6-spec, 2.6-tests, 2.6-failure-messages", f"{PAGE}:201, :203-212; {TEST}:459-590, 867-960",
        "PASS",
        "Round-6 gap closed. Each named bullet has a must_refuse test and an accepting test on the other side: empty losses "
        "(:867-878, 931-944), target 0 refused / 1 accepted / 10001 refused / 10000 accepted (:883-912), negative loss "
        "refused / 0 accepted (:915-928, 947-960), negative margin, fund, capital and loss refused with the input named and "
        "zero accepted (:459-541), defaulter below / above / between / not in the funds (:549-566, :569-578), defaulter present "
        "in the margins only refused (:581-590, new this round), defaulter at the lowest and highest id and at id 4 accepted "
        "(:593-608). The new refusal is killed by mutant n1 on seed 0 (out/mutate_seeds0-9_all53.out)."),
    row("proj-conventions-prose", "2.9-prose, 2.6-mathematics", f"{PAGE}:219-224; course/modules/BK/BK4/grader/reference.py:36-109",
        "PASS",
        "Layer order (a1, a2, a3, R), survivor rule, leftover rule, conservation, cover floor, ceiling index and money bullets "
        "(page :219-224) match reference.py lines 57-60, 62-80, 99-100 and 108-109 and the independent oracle (out/rederive_r7.out)."),
    row("proj-hours", "2.9-structure, hours", f"{PAGE}:34, :373-386 (table#hours); course/modules/BK/BK4/index.html:29", "PASS",
        "Rationale table 2+2+3+3+2+2+1 = 15; page data-hours-project=\"15\" (:34); index.html:29 data-hours-lessons=\"35\" "
        "data-hours-project=\"15\", so 35 + 15 = 50 and 15/50 = 30 %, as the page's own text states (:383)."),
    row("proj-grader-reference-run", "2.6-autograder 1", f"course/modules/BK/BK4/grader/reference.py; {TEST}", "PASS",
        f"run_graders --unit BK4 --seeds 0-49: 'run_graders BK4: PASS (reference 50/50 seeds, slowest 0.2 s)' exit 0 "
        f"({OUT_DIR}/run_graders_0-49.out). Documented local command "
        "'QF_SEED=12345 pytest -q -p no:cacheprovider --assert=plain -W error test_project.py' on the reference: 86 passed."),
    row("proj-grader-starter-fails", "2.6-autograder, 2.6-failure-messages", "course/modules/BK/BK4/grader/starter.py; "
        f"{TEST}:1091-1114", "PASS",
        f"Starter, seed 0 ({OUT_DIR}/starter_seed0.out): 82 failed, 4 passed (the 4 do not call the stub: dataclass shape and "
        "the three seeded-instance tests), 0 Traceback lines; first failure text 'test_waterfall_returns_plain_int_money: the "
        "student module has no implementation for waterfall yet; write it in clearing_house.py' names the property and the "
        "function, not a stack trace. Starter on seeds 0-49 passes 0/50 (alternatives run)."),
    row("proj-collect-count", "2.6-count", f"{PAGE}:201 (no), :214; {TEST}", "PASS",
        f"pytest --collect-only -q on a scratch copy (test_project.py, instance.py, reference.py as clearing_house.py): "
        f"'86 tests collected' ({OUT_DIR}/collect_only.out). project.html:214 says 'runs 86 checks'. grep '^def test_' = 86."),
    row("proj-instances", "2.6-autograder 2, 2.8-data", "course/modules/BK/BK4/grader/instance.py:22-50", "PASS",
        "Seeds 0-49 re-checked with the page's validity rules (members 1..N with N in 4..6, funds >= 1, margins and capital "
        ">= 0, 40..80 non-negative integer losses, target in {9000, 9500, 9750}): no invalid seed. 50 distinct sizing answers "
        "(out/rederive_r7.out). Plan 5.5 materiality: 48 distinct uncovered totals over seeds 0-49, and every seed contains a "
        "loss in the margin, in the fund, and past the survivors' pool (out/rederive_r7.out 'plan 5.5')."),
    row("proj-mutants-builder", "2.6-mutants", "ledgers/BK4/mutants/m01_fund_before_margin.py .. m10_seed0_hardcoded.py", "PASS",
        f"tools/mutate_graders.py --unit BK4 --seeds 0-9 over all 53 mutants ({OUT_DIR}/mutate_seeds0-9_all53.out): m01 to m10 "
        "all KILLED, each by a named test on seed 0."),
    row("proj-mutants-own", "2.6-mutants", "ledgers/BK4/mutants/ (r3a..r5f, vc01..vc15, n1..n4, s01..s05)", "PASS",
        "Round-6 survivor n1 (defaulter checked against margins only) is now KILLED on seed 0 by "
        "test_defaulter_with_a_margin_but_no_default_fund_is_refused_and_the_message_names_it. The full run over 53 mutants "
        "exits 0 with 53/53 KILLED (out/mutate_seeds0-9_all53.out), so the gate passes. Round-6 kills of r5c and r5d persist."),
    row("proj-mutants-round7", "2.6-mutants", f"ledgers/BK4/mutants/s01..s05 (written by {SCRIPTS}/make_r7_mutants.py)", "PASS",
        "Five new student-error mutants of the reference, one change each, all KILLED on seed 0: s01 leftover to the largest "
        "fund first (test_each_scenario_matches_the_oracle_on_both_instances); s02 shares weighted by margins "
        "(same test); s03 zero-fund survivor omitted (test_a_member_with_no_default_fund_is_skipped_by_the_remainder_rule); "
        "s04 reworded empty-scenario message (test_empty_losses_are_refused_in_margin_for_cover_with_the_scenario_message); "
        "s05 sizing index rounded to nearest (test_margin_matches_the_order_statistic_on_both_instances). Killers in "
        f"{OUT_DIR}/mutate_seeds0-9_all53.out."),
    row("proj-large-cent-claim", "2.6-autograder, 2.6-mutants", f"{TEST}:442-451", "PASS",
        "Recomputed exactly: residual 6585696953829388 times fund 6692931089932558 = 4.4077e31 > 2**53 (out/large_cent_r7.out). "
        "Floored shares 6055950114045319 and 529746839784068, leftover 1 to member 1, giving 6055950114045320 and "
        "529746839784068, which sum to the residual. The test's expected values are the exact integer results."),
    row("proj-mutant-float", "2.6-mutants", "ledgers/BK4/mutants/vc10_float_arithmetic.py; " + TEST + ":442-451", "PASS",
        "vc10 KILLED by test_large_cent_shares_are_floored_in_integers (seed 0) in out/mutate_seeds0-9_all53.out."),
    row("proj-mutant-argument", "2.6-mutants", "ledgers/BK4/mutants/r4f_sizing_sorts_caller_list_in_place.py; "
        f"{PAGE}:203; {TEST}:1062-1068", "PASS",
        "r4f KILLED by test_margin_for_cover_and_cover_bps_do_not_change_their_list_argument (seed 0) (mutate output)."),
    row("proj-labs-simulated-stdlib", "2.8-data, 2.5-labs", f"tests/labs/BK4/lab-BK4-project-1..3.py; {PAGE}:54", "PASS",
        "The three twins import only random (lab-BK4-project-1 line 7, -2 line 6, -3 line 8; grep this round). Each docstring "
        "says SIMULATED (twin 1 line 3 and constants at lines 9-11); page :54 says all amounts are SIMULATED; no file is read."),
    row("proj-page-smoke", "2.9-smoke", PAGE, "PASS",
        f"page_smoke.py --unit BK4 --pages project: PASS ({OUT_DIR}/page_smoke_project.out). In-browser grader: 'All 86 tests "
        "pass on seed 1384226118'. Three labs run under Pyodide, each under 0.1 s."),
    row("proj-check-tools", "2.9-structure, 2.6-ladder", PAGE, "PASS",
        "check_pages.py --unit BK4: PASS; check_dag.py --unit BK4: PASS; check_projects.py --unit BK4: PASS (out/check_pages_unit.out, "
        "check_dag.out, check_projects.out). Note (not a page defect): check_pages.py --page project applies the lesson template "
        "to the project page and reports 11 lesson-only problems (out/check_pages_project.out); the unit-wide run, which applies "
        "the project rules, passes."),
    row("proj-ruff", "2.9-tooling", "tests/labs/BK4; course/modules/BK/BK4/grader", "PASS",
        f"ruff check: 'All checks passed!' (out/ruff_check_slice.out, exit 0). ruff format --check: '12 files already formatted' "
        "(out/ruff_format_slice.out, exit 0)."),
    row("proj-mypy-repo", "2.9-tooling", "pyproject.toml [tool.mypy]", "PASS",
        "mypy --no-incremental (repository): 'Success: no issues found in 385 source files', exit 0 (out/mypy_repo_no_incremental.out)."),
    row("proj-mypy-plan-command", "2.9-tooling", f"{TEST}:28, :30", "PASS",
        "mypy tests/labs/BK4 course/modules/BK/BK4/grader: 'Success: no issues found in 12 source files', exit 0 "
        "(out/mypy_slice_plan_cmd.out)."),
    row("proj-pytest-labs", "2.5-labs", "tests/test_labs.py; tests/test_run_labs.py", "PASS",
        "pytest -q tests/test_labs.py tests/test_run_labs.py -k 'BK4 or labs': all passed, exit 0 (out/pytest_labs_slice.out)."),
    row("proj-refs", "2.1-citations", f"{PAGE}:501-506 (reading list); references/references.json:7411 (duffie2011central), "
        ":2853 (bisndcpmi)", "PASS",
        "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (out/verify_refs_offline.out). Both keys are "
        "present: duffie2011central is crossref-verified (DOI 10.1093/rapstu/rar001); bisndcpmi is issuer-verified at index "
        "level. The page attributes no statement to either (:501-502). Live verify_refs not run (network)."),
    row("proj-banned-and-process-words", "2.9-prose", f"{PAGE}; grader/*.py; tests/labs/BK4/lab-BK4-project-*.py", "PASS",
        "Case-insensitive grep for the BUILDER_RULES 1.3-1.4 banned strings (TODO, TBD, lorem, for brevity, details omitted, "
        "beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is "
        "well known, obviously, clearly, ellipsis) and for process words (builder, verifier, planner, architect, fixer, "
        "request, decision, round, unit report): no prose hit. The only matches are code: tuple[int, ...] (test_project.py:37) "
        "and the ellipsis in a type annotation (test_project.py:1091 code line)."),
    row("proj-anchors-links", "2.9-structure", PAGE, "PASS",
        "Every internal href resolves: all #fragments exist as ids in project.html, and grader/starter.py, grader/test_project.py, "
        "index.html, L05.html and index.html#placement exist (checked by script this round, 0 bad links). "),
    row("proj-dag-concepts", "2.9-DAG", PAGE, "PASS",
        "grep: project.html contains 0 <dfn>, 0 data-concept, 0 class=\"concept\" links. check_dag.py --unit BK4 PASS. No "
        "concept is linked from the project page, so no DAG issue arises here."),
    row("proj-rung-ladder", "2.6-ladder", f"{PAGE}:41-50, :193-216, :490-497", "PASS",
        "check_projects.py --unit BK4: PASS. Rungs 1 to 4 in order (:44-49). Rung 2 is a completion lab (class=\"lab completion\", "
        ":141). Rung 4 is not graded (:492)."),
    row("proj-exemplar-a-calibration", "2.7-rubric-calibration", f"{PAGE}:424-453 (exemplar A), :408-417 (rubric)",
        "UNVERIFIABLE",
        "Not blind. This verifier read the rubric, both exemplars and their annotations (:442-449) before scoring, and no fresh "
        "context was available for a blind pass. Scoring from the descriptors and the passage gives C1 2, C2 2, C3 1, C4 2, C5 2, "
        "which equals data-scores=\"2,2,1,2,2\" (:424) and the official line (:426). Not counted as a calibration result.",
        "A fresh verifier that has not read the annotations scores exemplar A blind against the rubric (:408-417), using only "
        "the passage text (:428-441), and lands within one level of the annotated scores on every criterion."),
    row("proj-exemplar-b-numbers", "2.2-numbers, 2.3-grades", f"{PAGE}:404 (memo rule), :422, :457 (disclosure), :459-470",
        "PASS",
        "Every number in exemplar B is re-derived or printed: 111074 and 105154 (Lab 3 Part B and C), 111074 - 105154 = 5920, "
        "9500 - 9000 = 500 (both printed targets), 1334 + 1666 + 1000 = 4000, k = 38 from exact 38.0, margin 117088 for 9750, "
        "two scenarios past 111074 and four past 105154 (Lab 3 Part C prints 2 and 4). The disclosure at :422 and :457 allows a "
        "difference of two printed numbers, as the memo rule at :404 does (out/rederive_r7.out)."),
    row("proj-rubric-c3-descriptors", "2.7-rubric", f"{PAGE}:414", "PASS",
        "C3 level descriptors (4: pro rata and leftover rules with the sum that checks them; 3: the same without the sum; "
        "2: one rule or survivor amounts; 1: no sharing rule) are observable: each names a statement a reader can find in a memo."),
    row("proj-exemplar-b-calibration", "2.7-rubric-calibration", f"{PAGE}:455-481 (exemplar B), :457 (official scoring)",
        "UNVERIFIABLE",
        "Not blind. The annotations (:471-479) were read before scoring. Scoring from the descriptors and the passage gives C1 4, "
        "C2 4, C3 4, C4 4, C5 4, which equals data-scores=\"4,4,4,4,4\" (:455). Not counted as a calibration result.",
        "A fresh verifier that has not read the annotations scores exemplar B blind (passage at :460-469, descriptors at :408-417) "
        "and lands within one level of the annotated scores on every criterion."),
    row("proj-lab2-learner-text", "2.6-prose, 2.5-labs", f"{PAGE}:146-147, :186; tests/labs/BK4/lab-BK4-project-2.py:1-3", "PASS",
        "Learner text of Lab 2 contains no process word and no planning reference (grep this round)."),
    row("proj-lab3-claim-checks-rules", "2.5-labs, 2.3-prose", f"{PAGE}:253-366 (Lab 3 hypothesis and interpretation)", "PASS",
        "Each Lab 3 claim checked against the twin output and out/rederive_r7.out: five rows with conservation True and the "
        "uncovered 12000 only in the 100000 row; three different indices 36, 38, 39; brute force agrees True for all three; "
        "Part C counts as above. The 'not a proof' sentence matches the twin docstring (tests/labs/BK4/lab-BK4-project-3.py line 5)."),
    row("proj-notation-T", "2.4-notation", f"{PAGE}; notation/notation.json (8 symbols: T, Phi, gamma_3, gamma_4, R^ast, R^{{e ast}}, R_f, Q)",
        "PASS",
        "None of the registered symbols appears on the page as a symbol (grep for bare T, Phi, gamma, Q, R_f: none). The page uses "
        "N, S, k, K, D, R, L, t, Lambda and i as local symbols, each defined on first use (:194-225); none collides with a registered "
        "meaning."),
    row("proj-failure-leak", "2.6-failure-messages", f"{TEST} (all test_ functions; helpers)", "PASS",
        "AST check this round: 94 test and helper functions checked; 91 carry __tracebackhide__. The three without it "
        "(waterfall_of, fixture, remainder_case) contain no assertion and no expected value (they only build inputs), so no "
        "failure they raise can show an answer. No failure message interpolates a computed answer: check_waterfall, must_refuse "
        "and the assertions print only property names and the named inputs."),
    row("proj-plan-conformance", "2.9-plan", "plans/BK4-build-plan.md:419, :437-446, :458, :478, :481, :515-517, :740-748; "
        f"plans/BK4-open-items.md; {PAGE}:208; {TEST}:735-743, :931-944", "FAIL",
        "(i) RESOLVED: plan:517 'monotonicity ... on each seed' is now met by test_margin_is_non_decreasing_in_the_target, "
        "which loops over seeds 0 to 49 and INST, INST2 (test_project.py:735-743). "
        "(ii) OPEN: plan:458 lists the period convention (the settlement date is period 0; the scenario index starts at 1) under "
        "rounding and conventions 'stated once'; project.html Conventions (:217-225) does not state it (grep 'period' hits only "
        ":469, 'close-out period'). "
        "(iii) OPEN: the plan's exception table (plan:439-446) names five conditions and says they are the only ones the grader "
        "requires an exception for; the page (:208) and test_project.py:931-944 add cover_bps with empty losses. "
        "(iv) OPEN: the builder edited the binding plan at commit 67a2d13 (plan lines for the target set 9900/9950/9975 becoming "
        "9000/9500/9750, the exemplar levels, the criterion 5 wording, and the brute-force scope), and plans/BK4-open-items.md "
        "states these are unratified; plan lines 743-746 ('Architect decisions ... Pending') still read Pending, and the binding block at lines 748-749 does not ratify these edits.",
        "Architect records a ruling for (ii), (iii) and (iv) in the plan's Architect decisions block. For (ii), add the period "
        "sentence to project.html Conventions or strike the convention from plan 5.3. For (iii), amend plan 5.2 to list the sixth "
        "condition or remove the cover_bps empty-losses test and its page bullet (:208). For (iv), revert each builder edit to "
        "plans/BK4-build-plan.md that the Architect does not ratify (the target set, the exemplar levels, the criterion 5 wording, "
        "the brute-force scope)."),
    row("proj-sizing-duplicate-losses", "2.6-tests, 2.6-mathematics", f"{PAGE}:223; {TEST}:682-694, :805-816", "PASS",
        "Recomputed: margin_for_cover([5,5,10,20], 5000) = 5 (k 2); margin_for_cover([5,5,5,9,12], 6000) = 5 (k 3); "
        "cover_bps([5,5,10,20], 5) = 5000. The tests assert these values and the page's conventions count S with repeats "
        "(:223, :219 'S scenario losses')."),
    row("proj-context-sentences", "2.9-prose", f"{PAGE}:197 (spec Context); course/modules/BK/BK4/grader/reference.py:36-109", "PASS",
        "Context describes the layer order that reference.py implements (lines 57-60) and that one default is simulated at a "
        "time. 'The autograder checks the cent results and the cover values, not the docstring or the imports' is true: "
        "test_project.py has no docstring or import inspection (grep for __doc__, ast, getsource, inspect: none)."),
    row("proj-alternatives", "2.6-autograder 5", "ledgers/BK4/alternatives/alt1_comprehensions.py .. alt5_bisection.py", "PASS",
        f"Re-run this round on the current suite, seeds 0-49 ({SCRIPTS}/run_candidates_r7.py): alt1 50/50, alt2 50/50, alt3 "
        f"50/50, alt4 50/50, alt5 50/50 ({OUT_DIR}/alternatives_reference_starter_0-49.out). The alternatives are unchanged since "
        "67a2d13 (git log -1 -- ledgers/BK4/alternatives)."),
    row("proj-survivor-leftover-order", "2.6-tests, 2.6-mutants", f"{TEST}:411-429; ledgers/BK4/mutants/r4a_leftover_in_mapping_order.py",
        "PASS",
        "r4a KILLED by test_leftover_cent_goes_to_the_lowest_id_when_the_dictionaries_list_members_out_of_order (seed 0); "
        "n3 KILLED (mutate output)."),
    row("proj-silence-named-refusals", "2.6-tests, 2.6-mutants", f"{TEST}:1010-1059; ledgers/BK4/mutants/r4g_*.py, r4h_*.py", "PASS",
        "r4g KILLED by test_refused_inputs_print_nothing_before_they_raise (seed 0); r4h KILLED by "
        "test_the_module_prints_nothing_on_valid_inputs (seed 0) (mutate output)."),
    row("proj-refusal-count-docstring", "2.9-prose", f"{TEST}:1021-1022", "PASS",
        "The docstring reads 'Each named refusal in the list below raises ValueError and prints nothing on the way.' No count "
        "appears in any test docstring (grep for number words: none)."),
    row("proj-remainder-spec", "2.6-spec, 2.6-tests", f"{PAGE}:248; {TEST}:362-368", "PASS",
        "The page names defaulter 4 with no margin, fund or capital, survivors 1, 2, 3 with 1 cent each; REMAINDER_* in the test "
        "use exactly these values. Losses 1, 2, 4 match the page's sentence (out/rederive_r7.out 'remainder')."),
    row("proj-rubric-c5-descriptor", "2.7-rubric", f"{PAGE}:416 (C5 level 3)", "PASS",
        "Level 3 reads 'names three of the four limits, and states the direction in which each one biases the sized margin or "
        "the cover': an observer can check both parts."),
    row("proj-money-integer-claim", "2.6-spec, 2.6-tests", f"{PAGE}:203, :224; {TEST}:442-451", "PASS",
        "Page :224 says the layers, the margin and the uncovered loss are exact integers, and a share and a cover are exact "
        "fractions floored to integers (:224, :203). reference.py computes them with integer subtraction, min and //. The "
        "no-float claim is held by the 2**53 test (vc10 KILLED)."),
    row("proj-zero-loss-sizing", "2.6-tests, 2.6-mutants", f"{TEST}:697-703; ledgers/BK4/mutants/r5c_*.py", "PASS",
        "test_zero_losses_are_scenarios_in_the_sizing asserts margin_for_cover([0, 10, 20, 30], 5000) == 10 (rederived: k 2, "
        "sorted[1] = 10). r5c KILLED on seed 0."),
    row("proj-zero-loss-cover", "2.6-tests, 2.6-mutants", f"{TEST}:812-816; ledgers/BK4/mutants/r5d_*.py", "PASS",
        "test_zero_losses_are_in_the_cover_denominator asserts cover_bps([0, 0, 5, 9], 0) == 5000 (2 of 4 covered). r5d KILLED on seed 0."),
    row("proj-round7-prose-delta", "2.9-prose, 2.6-spec", f"{PAGE}:38, :214, :404 (the round-7 changes)", "PASS",
        "Delta 4bd8cb94..06994db read in full for project.html (three hunks: lede :38, grading mode :214, memo paragraph :404) and "
        "test_project.py (new test :581-590; monotonicity loop :735-743). The lede's cover reference (#spec), the Conventions "
        "anchors (#conventions) and the count 86 (:214, matches collect-only) are correct. The memo rule's added 'value that the "
        "rules give by computation' clause is consistent with exemplar B's quoting (:457, :467)."),
    row("proj-local-run", "2.6-autograder, 2.9-prose", f"{PAGE}:397-399 (local command)", "PASS",
        "The documented local command, run with the reference as clearing_house.py and QF_SEED=12345, gives '86 passed' (this "
        "round). The page's statement that --assert=plain prints no values is consistent with the suite's helpers."),
    row("proj-spec-signatures", "2.6-spec, 2.6-atlas", "course/modules/BK/BK4/grader/starter.py:29-47; " + PAGE + ":201",
        "PASS",
        "The starter's names and signatures (waterfall with five parameters, margin_for_cover(losses_cents, target_bps), "
        "cover_bps(losses_cents, margin_cents), the Waterfall dataclass with the five named fields) equal the page's Required "
        "outputs (:201) and the plan interface (plan 5.2). Matches reference.py:20-109."),
    row("proj-spec-inputs-instance", "2.6-spec, 2.8-data", f"{PAGE}:199; course/modules/BK/BK4/grader/instance.py:25-39",
        "PASS",
        "The page's Inputs (N from 4 to 6; funds at least 1 cent; 40 to 80 losses; target 9000, 9500 or 9750) match "
        "instance.py: count randint(4,6) (:25), funds randint(1000,8000) (:28), scenarios randint(40,80) (:33), target "
        "choice((9000,9500,9750)) (:39). Verified on 50 seeds (out/rederive_r7.out)."),
    row("proj-l03-crossref", "2.9-prose, 2.4-mathematics", f"{PAGE}:223 (cross-reference to Lesson 3); course/modules/BK/BK4/L03.html:128, :151-174",
        "PASS",
        "The page says Lesson 3 defines the cover and states the sizing rule with its proof under its own assumptions. L03 has "
        "section 2 'Margin cover and the sizing rule' (:128) and Proposition 2.3, the sized margin is an order statistic, graded T "
        "(:151), with its proof (:152-174). The index k = ceil(t S / 10000) matches the page."),
]

MUTANTS = []
for line in MUT.splitlines():
    match = re.match(r"^(KILLED|SURVIVED) (\S+): (.*) -> (.*)$", line)
    if not match:
        continue
    status, name, description, killer = match.groups()
    killed_by = killer.strip() if status == "KILLED" else None
    MUTANTS.append({
        "id": name,
        "file": f"ledgers/BK4/mutants/{name}",
        "description": description.strip(),
        "killed_by": killed_by,
        "seeds": "0-9",
    })

fragment = {
    "unit": "BK4",
    "slice": "BK4-c",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier for BK4-c (round 7); did not build BK4",
    "pin": "06994db16d1ab449bcf29898a7f56cfa999dce57",
    "base": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07 (round-6 pin; previous fragment /Users/billyribeiro/.fanout/frags/E-BK4-c.round6.json, used as context only; no round-6 PASS row carried: every row re-derived or re-run this round)",
    "checkout": str(ROOT),
    "scratch": "/tmp scratch dirs removed; all scripts and outputs are in ledgers/BK4/scripts/BK4-c-r7/ (out/ holds the command output)",
    "verified_at": VERIFIED_AT,
    "verdict": "FAIL",
    "rows": ROWS,
    "mutants": MUTANTS,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta 4bd8cb94..06994db in the slice: project.html (lede, grading mode, memo paragraph), grader/test_project.py (one new "
        "refusal test, monotonicity over seeds 0-49), and four new mutants n1-n4 (n1 was the round-6 survivor). reference.py, "
        "instance.py, starter.py, the three project twins and the alternatives are byte-identical to the round-6 pin. "
        "Read in full this round: project.html (521 lines), grader/test_project.py (1114 lines), reference.py, instance.py, "
        "starter.py, the three project twins (by run and by the page's blocks), alt1 to alt5 (run). "
        "Wrote five new student-error mutants s01 to s05 (scripts/BK4-c-r7/make_r7_mutants.py); all 53 mutants killed on seeds 0-9, "
        "exit 0. Not checked: blind calibration of exemplars A and B (not possible in this context, annotations already read); "
        "the live verify_refs run (network, not run; offline run used); the Lesson 3 proof was checked only at its locator, "
        "not re-derived here (it is the L03 slice's row); the Duffie & Zhu paper was not read (the project makes no claim from it). "
        "Tool note: check_pages --page project applies the lesson template and fails 11 lesson-only checks; the unit-wide run "
        "passes and is the gate."
    ),
    "summary": (
        "BK4-c round 7: verdict FAIL. Rows: total {total}, PASS {p}, FAIL {f}, UNVERIFIABLE {u}. Mutants: 53/53 killed on seeds 0-9 "
        "(mutate_graders exit 0; n1 survivor of round 6 now killed; five new mutants s01-s05 killed). Alternatives alt1-alt5 and "
        "reference pass 50/50 seeds; starter 0/50. Collect-only count 86 equals the page's 86. Remaining non-PASS: "
        "proj-plan-conformance (FAIL: three unratified deviations, and one open process item), and two UNVERIFIABLE "
        "calibration rows (no blind scorer in this context)."
    ),
}

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in ROWS:
    counts[r["status"]] += 1
fragment["summary"] = fragment["summary"].format(total=len(ROWS), p=counts["PASS"], f=counts["FAIL"], u=counts["UNVERIFIABLE"])

ids = [r["id"] for r in ROWS]
assert len(ids) == len(set(ids)), "duplicate row ids"
path = ROOT / "ledgers/BK4/BK4-c.json"
path.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", path, "rows", len(ROWS), "mutants", len(MUTANTS), "killed", sum(1 for m in MUTANTS if m["killed_by"]))
