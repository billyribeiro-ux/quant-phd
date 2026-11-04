"""Write the BK4-c round-2 ledger fragment (verifier BK4-c). Run from the checkout root.

Usage: .venv/bin/python ledgers/BK4/scripts/BK4-c-r2/write_fragment_r2.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/BK4/scripts/BK4-c-r2"
O = f"{S}/out"

rows = [
    {"id": "proj-lab1-numbers", "check": "2.5-labs, 2.2-numbers", "location": "course/modules/BK/BK4/project.html:56-139; tests/labs/BK4/lab-BK4-project-1.py",
     "status": "PASS",
     "evidence": f"run_labs --unit BK4 --page project: 'run_labs BK4: PASS (3/3)' ({O}/run_labs_project.out). {S}/twin_vs_page.py ({O}/twin_vs_page.out): twin exit 0, stderr 0 bytes under python -I -W error; page code equals twin; expected block equals twin output. {S}/rederive.py ({O}/rederive.out, 68 OK rows): layers 50000/6000/20000, residual 4000, floored shares 1333/1666/1000, leftover 1, survivors 1334/1666/1000, exact position 38.2, k 39, margin 117088, cover 9750 and 9500 one cent below, 38/40 = 9500 bps. The hypothesis and the interpretation numbers match the printed lines."},
    {"id": "proj-lab2-numbers", "check": "2.5-labs, 2.2-numbers", "location": "course/modules/BK/BK4/project.html:141-190; tests/labs/BK4/lab-BK4-project-2.py",
     "status": "PASS",
     "evidence": f"run_labs completion rule PASS ({O}/run_labs_project.out). {S}/twin_vs_page.py ({O}/twin_vs_page.out): twin exit 0 stderr 0 bytes; 42 page lines, 42 twin lines; lines differing from the twin contain a blank (none differ otherwise); expected block equals twin output (1334/1666/1000, k 39, margin 117088). The two blank expressions, floor(residual*DF_i/pool) and -((-target*count)//10000), are the ones Lab 1 uses (page lines 96 and 115)."},
    {"id": "proj-lab3-numbers", "check": "2.5-labs, 2.2-numbers", "location": "course/modules/BK/BK4/project.html:253-366; tests/labs/BK4/lab-BK4-project-3.py",
     "status": "PASS",
     "evidence": f"Twin exit 0, stderr 0 bytes ({O}/twin_vs_page.out); expected block equals output. {S}/rederive.py ({O}/rederive.out): Part A rows 20000/55000/70000/80000/100000 (layers, survivors, uncovered 12000 at 100000, conservation True); Part B targets 9000/9500/9750: k 36/38/39, margins 105154/111074/117088, covers 9000/9500/9750, one cent below 8750/9250/9500, brute force agrees; Part C margins 111074 and 105154 with past-margin 2 and 4, past-fund 2, past-capital 0, past-survivors 0. Scenario maximum 118151 matches the printed 'largest loss'."},
    {"id": "proj-fixture-tables", "check": "2.4-mathematics, 2.6-tests", "location": "course/modules/BK/BK4/project.html:227-250; course/modules/BK/BK4/grader/test_project.py:281-441, 564-602",
     "status": "PASS",
     "evidence": f"{S}/rederive.py ({O}/rederive.out): all 11 layer-order fixture rows (loss 80 to 300) recomputed under the page's layer order and survivor rule; remainder fixture (loss 1, 2, 3, 4); sizing fixtures 8000 -> 40, 8001 -> 50, 10000 -> 50, 5000 over four losses -> 20; cover fixtures 3333 and 6666. Every row agrees with the page table and with the test expectations (test_project.py fixtures at lines 281-355, 362-428, 564-601, 652-668)."},
    {"id": "proj-named-conditions", "check": "2.6-spec, 2.6-tests, 2.6-failure-messages", "location": "course/modules/BK/BK4/project.html:203-210; course/modules/BK/BK4/grader/test_project.py:448-530, 751-832",
     "status": "PASS",
     "evidence": f"Each named condition has a refusal test (ValueError, message substring: 'at least one scenario is needed', 'target_bps', 'losses cannot be negative', 'loss_cents', 'initial_margin_cents', 'default_fund_cents', 'ccp_capital_cents', 'defaulter_id') and an accept test on the boundary (target 1 and 10000, loss 0, margin 0, fund 0, capital 0, defaulter at lowest and highest id). reference.py:33,45-55,94-96,105-107 raise these messages. Mutants vc04, vc05, vc13, vc14, vc15 are each killed by the matching named-condition test ({O}/mutate_graders_r2.out). Note (not a row): the message check is a substring match on the page's own phrases."},
    {"id": "proj-conventions-prose", "check": "2.2-numbers, 2.9-prose", "location": "course/modules/BK/BK4/project.html:218-226; course/modules/BK/BK4/grader/reference.py:1-13, 43-109",
     "status": "PASS",
     "evidence": f"Layer order, survivor rule with D (the pool), leftover rule, conservation, cover floor, k = ceil(t*S/10000) in integers and the money rule match reference.py line by line. The round-1 symbol T is now D (page line 220; no bare T in the page: {O}/static_checks.out)."},
    {"id": "proj-hours", "check": "2.9-hours", "location": "course/modules/BK/BK4/project.html:34, 370-388; course/modules/BK/BK4/index.html:29",
     "status": "PASS",
     "evidence": "Component rows 2+2+3+3+2+2+1 = 15 (project.html:376-382); data-hours-project=15 (project.html:34, index.html:29); lessons 35 + project 15 = 50. Verifier estimate of the components (rung 1 about 2 h, rung 2 about 2 h, waterfall about 3 h, sizing about 3 h, suite about 2 h, memo about 2 h, self-assessment about 1 h) is 15 h, inside the 30 % tolerance."},
    {"id": "proj-grader-reference-run", "check": "2.6-autograder-1", "location": "course/modules/BK/BK4/grader/reference.py; course/modules/BK/BK4/grader/test_project.py",
     "status": "PASS",
     "evidence": f"tools/run_graders.py --unit BK4 --seeds 0-49: 'run_graders BK4: PASS (reference 50/50 seeds, slowest 0.2 s)' ({O}/run_graders.out)."},
    {"id": "proj-grader-starter-fails", "check": "2.6-autograder-failure-messages", "location": "course/modules/BK/BK4/grader/starter.py; course/modules/BK/BK4/grader/test_project.py:940-963",
     "status": "PASS",
     "evidence": f"{S}/grade_candidates.py on starter.py, seed 0: FAIL, 70 failed and 4 passed ({O}/starter_r2.out). {S}/full_output.py ({O}/starter_full_r2.out, 217 lines): each failure line reads '<test_name>: the student module has no implementation for <function> yet; write it in clearing_house.py.' No docstring text and no traceback from the stub appears."},
    {"id": "proj-collect-count", "check": "2.6-test-count", "location": "course/modules/BK/BK4/project.html:214; course/modules/BK/BK4/grader/test_project.py",
     "status": "PASS",
     "evidence": f"{S}/collect_count.py ({O}/collect_count.out): reference and starter both '74 tests collected'; project.html:214 says 'runs 74 checks'."},
    {"id": "proj-instances", "check": "2.6-autograder-2", "location": "course/modules/BK/BK4/grader/instance.py:22-50",
     "status": "PASS",
     "evidence": f"{S}/rederive.py ({O}/rederive.out), seeds 0-49 (all 50, not a sample): 0 validity problems (ids 1..N with N 4..6, DF >= 1, IM >= 0, K >= 0, S 40..80, defaulter a member); 50 distinct sizing answers (oracle); target_bps values {{9000, 9500, 9750}} (the plan value set is a separate row, proj-plan-conformance). Each case has a loss in the margin, the fund and past the capital (test_project.py:868-881 checks it on both cases)."},
    {"id": "proj-mutants-builder", "check": "2.6-mutation", "location": "ledgers/BK4/mutants/m01_fund_before_margin.py .. m10_seed0_hardcoded.py",
     "status": "PASS",
     "evidence": f"Ten builder mutants (byte-identical since pin 1c1645f3, per git diff --stat 1c1645f3 HEAD). tools/mutate_graders.py --unit BK4 --seeds 0-9 ({O}/mutate_graders_r2.out): all KILLED (m01 by test_each_scenario_matches_the_oracle_on_both_instances; m05 and m06 by test_layers_and_survivor_payments_add_to_the_loss_on_every_scenario; m07 and m09 and m10 by test_margin_matches_the_order_statistic_on_both_instances; m08 by test_two_of_three_scenarios_covered_is_floored_not_rounded)."},
    {"id": "proj-mutants-own", "check": "2.6-mutation", "location": "ledgers/BK4/mutants/vc01_cover_rounded.py .. vc15_negative_capital_accepted.py",
     "status": "PASS",
     "evidence": f"Round-1 verifier mutants vc01-vc10 and round-2 verifier mutants vc12-vc15 (vc12, vc13, vc14, vc15 written by {S}/make_r2_mutants.py: pool includes the defaulter fund; cover_bps returns 0 for no scenarios; target range stops at 9999; negative CCP capital accepted). Every span is a single-change diff from reference.py (diffs in the script output). mutate_graders_r2.out: 24/24 KILLED on seeds 0-9, and vc10 (float arithmetic) is now killed by test_large_cent_shares_are_floored_in_integers. vc11 is not a counted mutant (see proj-mutant-argument)."},
    {"id": "proj-mutant-float", "check": "2.6-mutation", "location": "ledgers/BK4/mutants/vc10_float_arithmetic.py; course/modules/BK/BK4/grader/test_project.py:431-441",
     "status": "PASS",
     "evidence": f"Round-1 survivor now KILLED: mutate_graders_r2.out 'KILLED vc10_float_arithmetic.py ... -> test_large_cent_shares_are_floored_in_integers (seed 0)'. The new test passes on reference.py (run_graders 50/50) and the arithmetic in it was recomputed by {S}/rederive.py (big-case shares before leftover 6055950114045319 and 529746839784068; leftover 1 to member 1, giving 6055950114045320; sum equals the loss)."},
    {"id": "proj-mutant-argument", "check": "2.6-mutation (unstated behaviour)", "location": f"{S}/unstated/vc11_sorts_argument_in_place.py (not in ledgers/BK4/mutants); course/modules/BK/BK4/grader/starter.py:10",
     "status": "PASS",
     "evidence": f"{S}/grade_candidates.py on vc11 (in the round-1 scripts folder): 10/10 seeds pass ({O}/vc11_r2.out). The only statement of the behaviour is starter.py:10 'Nothing may print, warn or change its arguments'. grep of project.html and plans/BK4-build-plan.md finds no statement about argument mutation, so under the ruling the survivor is not a FAIL. Recommended (not required): add a test that margin_for_cover leaves its list unchanged."},
    {"id": "proj-labs-simulated-stdlib", "check": "2.8-simulated-labels", "location": "tests/labs/BK4/lab-BK4-project-1..3.py; course/modules/BK/BK4/grader/instance.py:1-7; project.html:54",
     "status": "PASS",
     "evidence": "All three twins and instance.py are labelled SIMULATED in their docstrings; project.html:54 says all amounts are SIMULATED. Imports are stdlib only (random, dataclasses, fractions, typing). No data-files attribute on the lab sections."},
    {"id": "proj-page-smoke", "check": "2.9-page-smoke", "location": "course/modules/BK/BK4/project.html",
     "status": "PASS",
     "evidence": f"tools/page_smoke.py --unit BK4 --pages project ({O}/page_smoke_project.out): 'page_smoke modules/BK/BK4/project.html: PASS', 'page_smoke BK4: PASS'; labs 0.0 s each; in-browser grader 'All 74 tests pass on seed 296413928. (0.8 s)'."},
    {"id": "proj-check-tools", "check": "2.9-structure, 2.6-rung-tools", "location": "course/modules/BK/BK4/project.html",
     "status": "PASS",
     "evidence": f"tools/check_projects.py --unit BK4 'check_projects BK4: PASS' exit 0; tools/check_dag.py --unit BK4 'check_dag BK4: PASS' exit 0; tools/check_pages.py --unit BK4 'check_pages BK4: PASS' exit 0 ({O}/check_projects.out, check_dag.out, check_pages.out)."},
    {"id": "proj-ruff", "check": "2.9-lint", "location": "tests/labs/BK4; course/modules/BK/BK4/grader",
     "status": "PASS",
     "evidence": f"ruff check tests/labs/BK4 course/modules/BK/BK4/grader: 'All checks passed!' exit 0 ({O}/ruff_check.out). ruff format --check on the same paths: '12 files already formatted' exit 0 ({O}/ruff_format.out)."},
    {"id": "proj-mypy-repo", "check": "2.9-typing", "location": "pyproject.toml [tool.mypy] (files = tools, tests)",
     "status": "PASS",
     "evidence": f"mypy --no-incremental (repo gate): 'Success: no issues found in 385 source files' exit 0 ({O}/mypy_repo_gate.out). The grader is outside the repo gate; see proj-mypy-plan-command for the plan's own command."},
    {"id": "proj-pytest-labs", "check": "2.5-labs", "location": "tests/test_labs.py; tests/test_run_labs.py",
     "status": "PASS",
     "evidence": f"pytest -q tests/test_labs.py tests/test_run_labs.py: all tests pass, exit 0 ({O}/pytest_labs.out)."},
    {"id": "proj-refs", "check": "2.1-citations", "location": "course/modules/BK/BK4/project.html:502-511; references/references.json (duffie2011central, bisndcpmi)",
     "status": "PASS",
     "evidence": f"tools/verify_refs.py --unit BK4: 'live re-verification of BK4: 2 of 560 entries, 0 problems' exit 0 ({O}/verify_refs_unit.out). The page attributes no statement to either key (project.html:501 'This page attributes no statement to either.'). Keys match the planner's record (references/references.json:2853, :7411)."},
    {"id": "proj-banned-and-process-words", "check": "2.9-banned-phrases, 2.9-process-words", "location": "project.html; grader/*.py; tests/labs/BK4/lab-BK4-project-*.py",
     "status": "PASS",
     "evidence": f"{S}/static_checks.py ({O}/static_checks.out): banned strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, ellipses) hits []; process words (builder, verifier, planner, fixer, architect, ruling, round, ledger, fragment, Q-numbers, B-numbers, FINAL, section sign, REFERENCE_REQUEST, DATA_REQUEST, honest-pending, atlas) hits []."},
    {"id": "proj-anchors-links", "check": "2.9-structure-links", "location": "course/modules/BK/BK4/project.html",
     "status": "PASS",
     "evidence": f"{S}/static_checks.py ({O}/static_checks.out): 22 href values, 37 ids; no unresolved in-page anchor and no missing relative file (grader/starter.py, grader/test_project.py, grader/instance.py, index.html#placement, L05.html, ../../../ targets)."},
    {"id": "proj-dag-concepts", "check": "2.9-DAG", "location": "course/modules/BK/BK4/project.html",
     "status": "PASS",
     "evidence": f"{S}/static_checks.py ({O}/static_checks.out): class=concept or <dfn> count 0. check_dag --unit BK4 PASS. The project uses no concept by name from outside the unit's closure (the unit's own terms CCP, margin, default fund, cover are defined in L01-L03)."},
    {"id": "proj-rung-ladder", "check": "2.6-ladder", "location": "course/modules/BK/BK4/project.html:41-50 (ladder), :193-216 (spec), :490-497 (rung 4)",
     "status": "PASS",
     "evidence": "Rung 1: lab-BK4-project-1, fully solved, comments on steps 1-6 (project.html:59-127). Rung 2: lab-BK4-project-2 with class 'lab completion', graded by the instant check (run_labs completion rule, twin_vs_page.out). Rung 3: spec and memo (project.html:193-216, 402-419). Rung 4: stretch, marked not graded (project.html:492). Order matches check_projects.py."},
    {"id": "proj-exemplar-a-calibration", "check": "2.6-rubric-calibration", "location": "course/modules/BK/BK4/project.html:409-419 (rubric), :424-453 (exemplar A)",
     "status": "PASS",
     "evidence": "Blind scoring from the rubric text only, on the memo text of exemplar A (project.html:430-438), before reading the official scores: C1 2 (layers named in order, no cents), C2 2 (margin for a stated target, no k and no cover check), C3 1 (no sharing rule named), C4 2 (margin with no cover), C5 2 (two limits). Official data-scores '2,2,1,2,2' (project.html:424, :426) agree on every criterion, within one level."},
    {"id": "proj-exemplar-b-numbers", "check": "2.2-numbers, 2.6-exemplar", "location": "course/modules/BK/BK4/project.html:455-481 (exemplar B)",
     "status": "PASS",
     "evidence": f"{S}/rederive.py ({O}/rederive.out): 80000 -> 50000/6000/20000, residual 4000, pool 12000, 1334+1666+1000 = 4000 (the printed survivor payments of Lab 1); 9500 bps: exact position 38.0, k 38, margin 111074, cover 9500, one cent below 9250, Part C prints margin 111074; 9000 bps margin 105154 with four past the margin; 111074 - 105154 = 5920 (a difference, base named as this set); 38/40 = 9500 bps. All quoted numbers match the printed lines or a computation on the page."},
    {"id": "proj-rubric-c3-descriptors", "check": "2.6-rubric-observable", "location": "course/modules/BK/BK4/project.html:414 (C3 level 1 and level 2 cells)",
     "status": "PASS",
     "evidence": "Round-1 defect fixed: C3 level 1 now reads 'Names no sharing rule.' and level 2 reads 'Gives survivor amounts, or states the pro rata rule without the leftover rule.' Both are observable and distinct from level 3 ('states both rules ... without the sum'). Note, not a row: a memo that states only the leftover rule and gives no amounts matches no C3 level."},
    {"id": "proj-exemplar-b-calibration", "check": "2.6-rubric-calibration", "location": "course/modules/BK/BK4/project.html:455-481 (exemplar B), :457 (official scores)",
     "status": "PASS",
     "evidence": "Blind scoring of exemplar B memo text (project.html:462-469) from the rubric alone: C1 4 (names the layers in order, gives cents for 80000, states the layer wait), C2 4 (target 9500 bps, k 38, 38th smallest, cover 9500 and 9250), C3 4 (pro rata rule, leftover rule, 1334+1666+1000 = 4000), C4 4 (margin with cover, past-survivor count 0, alternative 105154), C5 4 (names all four limits, no B or C claim, no source). Official data-scores '4,4,4,4,4' (project.html:455, :457) agree on every criterion. Round-1 mismatch on C3 is resolved."},
    {"id": "proj-lab2-learner-text", "check": "2.9-learner-text", "location": "course/modules/BK/BK4/project.html:146-147; tests/labs/BK4/lab-BK4-project-2.py:1-3",
     "status": "PASS",
     "evidence": "The docstring now reads 'Standard library only. The inputs are SIMULATED: illustrative values, not market data.' in both the page and the twin (project.html:146; twin lines 1-3). The false sentence 'This file is the completed solution' is gone. twin_vs_page.out: page code equals the twin except the blanks."},
    {"id": "proj-lab3-claim-checks-rules", "check": "2.5-labs-claims", "location": "course/modules/BK/BK4/project.html:366 (interpretation of Lab 3)",
     "status": "PASS",
     "evidence": "Sentence now reads 'Part A prints the layer amounts and the survivors' payments for five losses, and its conservation column checks that the layers, the survivors' payments and the uncovered loss add to each loss.' Code (project.html:313-320) prints a conservation column computed as total == loss; output shows True on all five rows (project.html:354-358). 'the 100000-cent row is the only row of Part A with an uncovered loss' matches uncovered 12000 only on that row."},
    {"id": "proj-notation-T", "check": "2.4-notation", "location": "course/modules/BK/BK4/project.html:219-220; notation/notation.json (symbols)",
     "status": "PASS",
     "evidence": f"Round-1 defect fixed: the pool is D (project.html:220, 'R >= D', 'R - D', 'R < D'); {S}/static_checks.py ({O}/static_checks.out): 'bare T in page text: []'. notation.json registers T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{{e\\ast}}, R_f and \\mathbb{{Q}}; D, R, L, K, M, S, N, k, t, i and IM_d, DF_d, DF_i, a1-a3 are not registered."},
    {"id": "proj-mypy-plan-command", "check": "2.9-typing (plan command)", "location": "course/modules/BK/BK4/grader/test_project.py:28 and :30",
     "status": "FAIL",
     "evidence": f"Plan section 10 command '.venv/bin/mypy tests/labs/BK4 course/modules/BK/BK4/grader' exits 1: 'Found 2 errors in 1 file (checked 12 source files)' ({O}/mypy_plan_command.out): test_project.py:28 'Cannot find implementation or library stub for module named \"clearing_house\"' and test_project.py:30 'module named \"instance\"' (both import-not-found). The grader is strict-clean in its real layout (run_graders typecheck), and the repo gate is green (proj-mypy-repo).",
     "fix": "Either add '# type: ignore[import-not-found]' to the import lines at grader/test_project.py:28 and :30, or change the plan's section 10 grader command to the scratch-layout typecheck that tools/run_graders.py performs, then rerun the plan command and require exit 0."},
    {"id": "proj-failure-leak", "check": "2.6-failure-messages", "location": "course/modules/BK/BK4/grader/test_project.py (every test has __tracebackhide__; wrapper at :940-963); project.html:399",
     "status": "PASS",
     "evidence": f"Round-1 leak paths closed. The unimplemented wrapper now names test.__name__, not the docstring (test_project.py:953-956; starter output {O}/starter_full_r2.out). {S}/static_checks.py: every test_ function contains __tracebackhide__ (out/static_checks.out, 'tests without __tracebackhide__: []'). Under --assert=plain the failing assertions print only their message: {O}/leak_vc08_full.out (vc08, the 8000 bps fixture: 'E   AssertionError: the margin must be the loss at the position ...', no value) and {O}/leak_probe_mutants.out (m07, vc12, vc14, vc10, vc08: messages name the property, no expected number). Assertion messages in test_project.py contain no answer digits (grep of assert/fail lines: literals appear only as inputs). Docstrings still quote fixture values but are never printed. Page statement project.html:399 ('a failure shows the test's own message and no values') holds in the outputs above."},
    {"id": "proj-plan-conformance", "check": "plan conformance (binding plan sections 5.2, 5.4, 5.5)", "location": "course/modules/BK/BK4/project.html:199, :416, :424, :455; course/modules/BK/BK4/grader/instance.py:39; course/modules/BK/BK4/grader/test_project.py:37, :552-561",
     "status": "FAIL",
     "evidence": "Four deviations from plans/BK4-build-plan.md, none a learner-facing error: (a) plan 5.2 sets target_bps in {9900, 9950, 9975}; project.html:199 (spec Inputs), instance.py:39 and test_project.py:37 use {9000, 9500, 9750}. (b) plan 5.4 gives exemplar-a data-level 4 and exemplar-b data-level 2; project.html:424 has exemplar-a at 2 and :455 has exemplar-b at 4. (c) plan 5.4 criterion 5 level 4 names 'no procyclicality'; project.html:416 names 'no change in margins in stress'. (d) plan 5.5 asks for the brute-force sizing check 'on every seed'; test_project.py:552-561 checks two cases (INST and INST2). The architect decisions block (end of plan) does not record any of these.",
     "fix": "Architect ruling for each of (a) to (d): restore the plan's value, or record the change in the 'Architect decisions' block of plans/BK4-build-plan.md. Items (b) and (c) are wording or ordering choices; (a) and (d) change the tested behaviour or the spec, and (a) changes instance.py, the spec and the target list in test_project.py."},
    {"id": "proj-large-cent-claim", "check": "2.9-prose-vs-numbers (suite text)", "location": "course/modules/BK/BK4/grader/test_project.py:431-440 (docstring line 432; failure label line 440)",
     "status": "FAIL",
     "evidence": f"The docstring says 'above 2**53 cents' and the failure label reads 'a scenario with cents above 2**53'. All values in that case are below 2**53 = 9007199254740992: the loss 6585696953829388, the funds 6692931089932558 and 585467024498971, and the pool 7278398114431529 ({S}/static_checks.py output, last section). Only the intermediate products (for example residual * fund = 4.4e31) exceed 2**53. The label is printed in the learner's failure output ({O}/leak_probe_mutants.out, vc10: 'E   Failed: a scenario with cents above 2**53: ...').",
     "fix": "Change the docstring at test_project.py:432 to 'Survivor shares are exact integer floors, with the leftover cent to the first survivor, where the products residual * default fund exceed 2**53.' and the label at :440 to 'a scenario whose products exceed 2**53'. Re-run run_graders and mutate_graders."},
    {"id": "proj-context-sentences", "check": "2.9-structure (BUILDER_RULES 5.2)", "location": "course/modules/BK/BK4/project.html:197 (spec Context)",
     "status": "FAIL",
     "evidence": f"BUILDER_RULES 5.2 requires the Context to be 2-4 sentences. The Context block has 5 sentences ({S}/static_checks.py, output 'sentences: 5' in {O}/static_checks.out): 'A clearing house novates ...', 'When a member defaults ...', 'You write the simulator ...', 'The cover of a margin is ...', 'One default is simulated at a time ...'.",
     "fix": "Merge two sentences, for example fold 'The cover of a margin is the share of the scenarios whose loss the margin covers in full.' into the sentence that introduces the sizing, so the Context has four sentences or fewer."},
    {"id": "proj-alternatives", "check": "2.6-autograder-alternatives", "location": "ledgers/BK4/scripts/BK4-c-r1/alternatives/*.py; ledgers/BK4/alternatives/*.py; ledgers/BK4/scripts/BK4-c-r2/alternatives/alt_f_heapq_divmod.py, alt_g_bisect_layers.py",
     "status": "PASS",
     "evidence": f"{S}/grade_candidates.py on 12 correct alternatives, seeds 0-49: all PASS 50/50 ({O}/alternatives_0_49.out: five round-1 verifier alternatives and five builder alternatives; {O}/alternatives_r2_0_49.out: two new round-2 verifier alternatives, heapq.nsmallest sizing with divmod shares, and a bisect-based sizing with a loop over the layers). None is over-constrained by the current suite."},
]

mutants = []
for name, desc in [
    ("m01_fund_before_margin", "Student error: the defaulter's default fund is used before its initial margin (layer order swapped)."),
    ("m02_capital_before_fund", "Student error: the CCP capital is used before the defaulter's default fund (layer order swapped)."),
    ("m03_survivors_by_count", "Student error: surviving members pay equal shares by count, not pro rata to their default funds."),
    ("m04_leftover_to_last_survivor", "Student error: the leftover cents go to the last surviving member instead of the first."),
    ("m05_no_remainder_rule", "Student error: survivor shares are truncated and the leftover cents are never paid, so the invariant breaks."),
    ("m06_uncovered_dropped", "Student error: the uncovered loss above the survivors' total is dropped instead of reported."),
    ("m07_floor_index", "Student error: the sizing index is the floor of target times count over 10000, not its ceiling."),
    ("m08_strict_cover", "Student error: the cover counts only losses strictly below the margin, so a loss equal to the margin is not covered."),
    ("m09_largest_loss_always", "Student error: the margin for every target is the largest loss, with no quantile at all."),
    ("m10_seed0_hardcoded", "Student error: the sizing returns the seed-0 margin (73529 cents) for every instance and target."),
    ("vc01_cover_rounded", "Student error: the cover is rounded to the nearest basis point instead of floored."),
    ("vc02_zero_based_index", "Student error: the sizing reads the zero-based position k instead of the k-th smallest loss (k - 1)."),
    ("vc03_sizing_unsorted", "Student error: the sizing picks the k-th loss as given, without sorting the scenarios first."),
    ("vc04_cover_no_refusal", "Student error: cover_bps accepts a negative loss without raising, so the named refusal is missing."),
    ("vc05_target_zero_allowed", "Student error: the target range check starts at 0, so a target of 0 bps is accepted and silently sized."),
    ("vc06_fund_without_min", "Student error: the default fund pays its full contribution even when the loss is smaller, so layers overpay."),
    ("vc07_leftover_to_zero_fund", "Student error: the leftover cent goes to a survivor with a zero default fund, skipping the DF > 0 rule."),
    ("vc08_index_plus_one", "Student error: the sizing index is floor(target times count / 10000) plus one, an off-by-one at exact positions."),
    ("vc09_capital_ignored", "Student error: the CCP capital is left out of the waterfall, so the survivors pay the capital's share."),
    ("vc10_float_arithmetic", "Student error: integer arithmetic replaced by float division (int of a float share, math.ceil of a float index), exact on small cents but not above 2**53."),
    ("vc12_pool_counts_the_defaulter_fund", "Student error: the survivors' pool includes the defaulter's own default fund, so shares are cut by it."),
    ("vc13_cover_of_no_scenarios_is_zero", "Student error: cover_bps returns 0 for an empty scenario set instead of refusing it with ValueError."),
    ("vc14_target_ten_thousand_refused", "Student error: the target range check uses 9999 as its upper limit, so a full target of 10000 bps is refused."),
    ("vc15_negative_capital_accepted", "Student error: a negative CCP capital is not checked, so it is accepted and reduces the layers."),
]:
    mutants.append({"id": name, "description": desc, "file": f"ledgers/BK4/mutants/{name}.py", "killed_by": None})

# killed_by from the round-2 run
out = (ROOT / O / "mutate_graders_r2.out").read_text(encoding="utf-8")
killed = dict(re.findall(r"KILLED (\S+)\.py: .*? -> (\S+ \(seed \d+\))", out))
for m in mutants:
    m["killed_by"] = killed.get(m["id"])
assert all(m["killed_by"] for m in mutants), [m["id"] for m in mutants if not m["killed_by"]]

fragment = {
    "unit": "BK4",
    "slice": "BK4-c",
    "round": 2,
    "verifier": "Claude Haiku 5.5, independent verifier for BK4-c (round 2); did not build BK4",
    "pin": "67c47689c49435bc0e6639e3de4feded5eefdd64",
    "base": "1c1645f3 (round-1 pin, E-BK4-c.round1.json); every project-slice row re-verified this round because project.html, grader/test_project.py and the vc10 mutant changed in 67c47689",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE2-BK4-c",
    "scratch": "temporary workspaces created by run_graders / mutate_graders under the system temp dir, removed after each run",
    "verified_at": "2026-11-04T07:10:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Read in full: project.html (521 lines), grader/instance.py, reference.py, starter.py, test_project.py (963 lines), and the three project lab twins; the page code blocks were compared with the twins by script. "
        "Run this round: check_projects, check_dag, check_pages, run_graders --seeds 0-49, mutate_graders --seeds 0-9 (24 mutants), run_labs --page project, twin runs under python -I -W error, collect-only, page_smoke (project), ruff check and format, mypy (plan command and repo gate), pytest tests/test_labs.py tests/test_run_labs.py, verify_refs --unit BK4 (live, 2 entries). "
        "Exemplar calibration: blind scores were written from the rubric text (project.html:412-416) and the exemplar memo text before the official scores were compared; the memo text was read first in this round, so the blind scores are not independent of having read it. "
        "Not verified by this verifier: the Pyodide runtime itself (page_smoke runs the in-browser grader on the reference only); the self-assessment form behaviour beyond reading rubric.js; the Duffie and Zhu abstract (the page states no finding from it, so gate B2 is not triggered for this slice); the B1 SEC settlement rule (not in this slice). "
        "Non-blocking observations, not rows: (1) a memo that states only the leftover rule matches no C3 level; (2) the grader's message checks are substring matches on the page's own phrases, so a paraphrase of 'at least one scenario is needed' fails; (3) vc11 (margin_for_cover sorts the caller's list) survives and is not counted, per the ruling, because only starter.py:10 states it; (4) Lab 1 says 'the lab checks these numbers', and it checks by printing a True or False line only. "
        "The verifier re-verified every round-1 non-PASS row: proj-mutant-float, proj-failure-leak, proj-lab2-learner-text, proj-lab3-claim-checks-rules, proj-notation-T, proj-rubric-c3-descriptors and proj-exemplar-b-calibration are now PASS; proj-mypy-plan-command and proj-plan-conformance remain FAIL."
    ),
    "summary": (
        "BK4-c round 2: verdict FAIL. "
        f"{sum(r['status'] == 'PASS' for r in rows)} PASS, {sum(r['status'] == 'FAIL' for r in rows)} FAIL, 0 UNVERIFIABLE of {len(rows)} rows. "
        "Mutants: 24/24 killed on seeds 0-9 (10 builder, 10 round-1 verifier including vc10 now killed, 4 new round-2 verifier). "
        "Alternatives: 12/12 correct implementations pass seeds 0-49. Grader: reference 50/50; starter fails with named messages; 74 tests collected and stated. "
        "Failing rows: the plan's mypy command (2 import errors), plan conformance (target set, exemplar levels, C5 wording, every-seed sizing check), the false '2**53' label in the suite, and the 5-sentence Context (2-4 required)."
    ),
}

problems = []
import sys
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

problems = ledger.validate(fragment, "BK4-c")
print("validate:", problems)
path = ROOT / "ledgers/BK4/BK4-c.json"
path.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", path, "rows", len(rows), "mutants", len(mutants), "verdict", fragment["verdict"])
