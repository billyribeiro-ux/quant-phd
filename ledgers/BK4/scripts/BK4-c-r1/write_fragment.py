"""Write the BK4 slice-c round-1 ledger fragment (verifier BK4-c r1). Output: ledgers/BK4/BK4-c.json.

The rows cite the scripts and output files under ledgers/BK4/scripts/BK4-c-r1/.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/BK4/scripts/BK4-c-r1"
OUT = f"{S}/out"
GRADER = "course/modules/BK/BK4/grader/test_project.py"
PAGE = "course/modules/BK/BK4/project.html"


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> dict[str, str]:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix or ""
    return item


rows = [
    row("proj-lab1-numbers", "2.5-labs, 2.2-numbers",
        f"{PAGE}:56-139",
        "PASS",
        f"run_labs --unit BK4 --page project: PASS (out/run_labs_project.out). Twin lab-BK4-project-1 exit 0, stderr 0 bytes under python -I -W error. "
        "Hypothesis and interpretation numbers re-derived: layers 50000/6000/20000, residual 4000, pool 12000, floored shares 1333/1666/1000, leftover 1, "
        "9550 bps x 40 = 38.2, k=39, margin 117088, cover 9750 at margin and 9500 one cent below (printed lines match the expected block)."),
    row("proj-lab2-numbers", "2.5-labs, 2.2-numbers",
        f"{PAGE}:141-191",
        "PASS",
        "run_labs completion rule PASS (out/run_labs_project.out): every page line equals the twin line or contains a blank. Twin output 1334/1666/1000, k=39, margin 117088, "
        "matching the hypothesis. Blank expressions re-derived: floor(residual*DF_i/pool) and -((-target*count)//10000)."),
    row("proj-lab3-numbers", "2.2-numbers, 2.5-labs",
        f"{PAGE}:253-368",
        "PASS",
        "Twin lab-BK4-project-3 exit 0 (stderr 0 bytes). Part A rows recomputed by hand: 55000 -> fund 5000; 70000 -> fund 6000 + capital 14000; 80000 -> survivors 1334/1666/1000; "
        "100000 -> residual 24000, pool 12000, uncovered 12000 (out/run_labs_project.out). Part B margins 105154/111074/117088 for 9000/9500/9750 bps, k 36/38/39, "
        "covers 9000/9500/9750 and one cent below 8750/9250/9500 (all below target), brute force agrees. Part C past-counts 2/2/0/0 and 4/2/0/0 match the interpretation."),
    row("proj-fixture-tables", "2.4-mathematics, 2.6-spec-fixtures",
        f"{PAGE}:230-251; {GRADER}:161-327, 334-372, 502-533, 572-579",
        "PASS",
        "Every row of the layer-order table (losses 80..300) recomputed by hand under the page's layer order and survivor rule (e.g. 181 -> survivor 1 pays 1 via the leftover; 300 -> residual 120 > pool 100, uncovered 20). "
        "Remainder fixture (R=1,2,4), sizing fixtures (8000->40, 8001->50, 10000->50, 5000->20 on 4 losses) and cover fixtures (3333, 6666) recomputed. "
        "Each fixture row has its own test (lines 275-327, 343-367, 502-533, 572-579); reference passes (out/run_graders.out)."),
    row("proj-named-conditions", "2.6-spec-exception-table",
        f"{PAGE}:204-213; {GRADER}:396-462, 651-705, 707-733",
        "PASS",
        "Each named condition has a refusal test with the message naming the input and an accept test on the boundary: empty losses (651, 707), target 0 and 10001 refused, 1 and 10000 accepted (665-690), "
        "negative loss in margin_for_cover and cover_bps (693-727), negative loss/margin/fund/capital in waterfall (396-453), defaulter not a member and smallest/largest id accepted (456-468). "
        "No test requires an exception type for any other input."),
    row("proj-conventions-prose", "2.4-mathematics, 2.9-prose",
        f"{PAGE}:218-226",
        "PASS",
        "Layer order, survivor rule, conservation, cover floor, k = ceil(t*S/10000) and money rules match course/modules/BK/BK4/grader/reference.py:43-109 line by line; "
        "tests in test_project.py cover each sentence (conservation 226-242; oracle 245-252; cover 572-625)."),
    row("proj-hours", "2.6-hours",
        f"{PAGE}:371-388; course/modules/BK/BK4/index.html:29",
        "PASS",
        "Declared components 2+2+3+3+2+2+1 = 15 h (matches data-hours-project=15 on project.html:34 and index.html:29; lessons 35 + project 15 = 50). "
        "Verifier estimate: rung 1 1.5 h, rung 2 1 h, waterfall and sharing 2.5 h, sizing 1.5 h, named conditions and suite 2 h, memo 2.5 h, self-assessment 1 h = 12 h, 20% below 15 h (inside the 30% bound)."),
    row("proj-grader-reference-run", "2.6-autograder-1",
        f"{S}/out/run_graders.out; {GRADER}",
        "PASS",
        "tools/run_graders.py --unit BK4 --seeds 0-49: 'run_graders BK4: PASS (reference 50/50 seeds, slowest 0.2 s)' (out/run_graders.out). "
        "Pyodide: page_smoke reports 'in-browser grader: All 73 tests pass' (out/page_smoke_project.out)."),
    row("proj-grader-starter-fails", "2.6-autograder",
        f"course/modules/BK/BK4/grader/starter.py; {S}/out/starter_raw.out",
        "PASS",
        "Starter run (grader_support.py starter): '69 failed, 4 passed' with NotImplementedError rewritten as named failures. The suite fails on the empty implementation."),
    row("proj-collect-count", "2.9-structure",
        f"{PAGE}:215; {GRADER}",
        "PASS",
        "grader_support.py collect: '73 tests collected'; page says 'runs 73 checks' (project.html:215)."),
    row("proj-instances", "2.6-autograder-2 (instances)",
        "course/modules/BK/BK4/grader/instance.py:22-50",
        "PASS",
        f"{S}/instance_checks.py over seeds 0-49 (all 50 checked, not a 20-seed sample): 0 validity problems (ids 1..N with N in 4..6, DF>=1, IM>=0, K>=0, defaulter a member, S in 40..80, "
        "integer non-negative losses, target in {9000,9500,9750}, a loss inside margin, inside fund and past capital in every case). Sizing answers: 50 distinct values; 47 seeds with a positive uncovered total; 48 distinct uncovered totals."),
    row("proj-mutants-builder", "2.6-mutation",
        "ledgers/BK4/mutants/m01..m10",
        "PASS",
        f"Each file re-diffed against reference.py: exactly one span differs (the layer swap, equal shares, last-survivor leftover, truncation, dropped uncovered, floor index, strict cover, largest loss, seed-0 constant). "
        f"tools/mutate_graders.py --unit BK4 --seeds 0-9: all 10 KILLED ({S}/out/mutate_graders.out)."),
    row("proj-mutants-own", "2.6-mutation (>=3 new student-error mutants)",
        "ledgers/BK4/mutants/vc01..vc09",
        "PASS",
        "Nine new single-span student-error mutants written by this verifier (make_mutants.py): cover rounded (vc01), zero-based index (vc02), unsorted sizing (vc03), "
        "no negative-loss refusal in cover_bps (vc04), target 0 accepted (vc05), fund paid without min (vc06), leftover to zero-fund member (vc07), index+1 (vc08), capital ignored (vc09). "
        "All 9 KILLED on seed 0 (out/mutate_graders.out)."),
    row("proj-mutant-float", "2.6-mutation; plan 2.1 item 8; project.html:204,225",
        f"ledgers/BK4/mutants/vc10_float_arithmetic.py; {GRADER}",
        "FAIL",
        f"vc10 (int of a float share, math.ceil of a float index) SURVIVES: 50/50 seeds pass (out/grade_vc10_0_49.out) and mutate_graders reports 'SURVIVED vc10' (out/mutate_graders.out). "
        f"The page states the behaviour it violates: project.html:204 'every computation is integer arithmetic, so no float ... appears' and :225 'the exact value of every output is an integer'. "
        f"A float share differs from the exact floor on large cents: waterfall(6585696953829388, 3, {{1:0,2:0,3:0}}, {{1:6692931089932558,2:585467024498971,3:0}}, 0) gives "
        f"{{1: 6055950114045319, 2: 529746839784069}} under float and {{1: 6055950114045320, 2: 529746839784068}} under exact arithmetic (out/float_probe.out, out/probe_large_cents_test.out).",
        f"Add to {GRADER} a test (name: test_large_cent_shares_are_floored_in_integers) that calls sol.waterfall(6_585_696_953_829_388, 3, {{1: 0, 2: 0, 3: 0}}, "
        f"{{1: 6_692_931_089_932_558, 2: 585_467_024_498_971, 3: 0}}, 0) and checks survivor_cents == {{1: 6_055_950_114_045_320, 2: 529_746_839_784_068}} and uncovered 0 "
        f"(the probe in {S}/probe_large_cents_test.py: reference passes, vc10 fails 1 test). Then re-run mutate_graders --unit BK4 --seeds 0-9."),
    row("proj-mutant-argument", "2.6-mutation (starter docstring)",
        f"{S}/unstated_mutants/vc11_sorts_argument_in_place.py; course/modules/BK/BK4/grader/starter.py:10",
        "PASS",
        "vc11 (margin_for_cover sorts the caller's list) passes 10/10 seeds (out/grade_vc11_0_9.out). The only statement of the behaviour is starter.py:10 'Nothing may print, warn or change its arguments'; "
        "project.html and the plan do not state it, so under FINAL-ARCHITECT-RULINGS 9 the survivor is not a FAIL and it is kept out of mutants/. Recommended: add a margin_for_cover argument-immutability test."),
    row("proj-labs-simulated-stdlib", "2.5-labs, 2.2-SIMULATED",
        "tests/labs/BK4/lab-BK4-project-1..3.py; grader/instance.py:1-7",
        "PASS",
        "All three twins and instance.py are labelled SIMULATED in their docstrings; project.html:54 states all amounts are SIMULATED. Imports are standard library only (random, fractions not used); the only seed is random.Random(1) or random.Random(f'BK4-clearing-house/<seed>'). No file read, no network."),
    row("proj-page-smoke", "2.9-structure, 2.5-labs (runtime and console)",
        f"{S}/out/page_smoke_project.out",
        "PASS",
        "tools/page_smoke.py --unit BK4 --pages project: 'page_smoke modules/BK/BK4/project.html: PASS', 'page_smoke BK4: PASS' (labs 0.0 s each, in-browser grader 73 tests pass)."),
    row("proj-check-tools", "2.9-structure",
        f"{S}/out/check_projects.out; {S}/out/check_pages.out; {S}/out/check_dag.out",
        "PASS",
        "check_projects --unit BK4: PASS; check_pages --unit BK4: PASS; check_dag --unit BK4: PASS (exit 0 each)."),
    row("proj-ruff", "gate (ruff)",
        f"tests/labs/BK4; course/modules/BK/BK4/grader",
        "PASS",
        "ruff check: 'All checks passed!'; ruff format --check: '12 files already formatted' (out/ruff_check.out, out/ruff_format.out)."),
    row("proj-mypy-repo", "gate (mypy)",
        "pyproject.toml [tool.mypy] files = tools, tests",
        "PASS",
        "mypy --no-incremental (repo gate): 'Success: no issues found in 385 source files' (out/mypy_repo_gate.out). The grader is outside the repo gate; in its layout "
        "(test_project.py, instance.py, reference.py as clearing_house.py) mypy --strict is clean (out/mypy_grader_layout.out)."),
    row("proj-pytest-labs", "gate (pytest labs)",
        "tests/test_labs.py; tests/test_run_labs.py",
        "PASS",
        "pytest -q tests/test_labs.py tests/test_run_labs.py: all tests pass (out/pytest_labs.out)."),
    row("proj-refs", "2.1-citations",
        "project.html:502-511 (data-cite duffie2011central, bisndcpmi); references/references.json (keys at lines 2853 and 7411)",
        "PASS",
        "tools/verify_refs.py --unit BK4 (live): 'live re-verification of BK4: 2 of 560 entries, 0 problems' (out/verify_refs_unit.out). "
        "The page attributes no statement to either source (project.html:502), so no attribution row applies. The Duffie & Zhu registry record is the Crossref record (doi 10.1093/rapstu/rar001, 2011)."),
    row("proj-banned-and-process-words", "2.9-prose; BUILDER_RULES 1.3-1.4",
        f"{PAGE}; {GRADER}; tests/labs/BK4/lab-BK4-project-*.py",
        "PASS",
        "grep of banned strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, important to note, studies show, experts agree, well known, obviously, clearly, ellipsis) and process words (build, builder, verifier, round, REQUESTS, unit report) returns no hit in the project page, grader or labs (only 'rounded'/'rounding' in arithmetic comments)."),
    row("proj-anchors-links", "2.9-structure",
        f"{PAGE}; course/modules/BK/BK4/index.html:71 (id placement)",
        "PASS",
        f"{S}/anchor_check.py: 'anchor problems: none' (in-page ids 37, index ids 17, placement anchor present, grader and L05 files exist)."),
    row("proj-dag-concepts", "2.9-DAG (check_dag, concepts)",
        PAGE,
        "PASS",
        "project.html contains no class=\"concept\" link and no <dfn>; check_dag --unit BK4 PASS (out/check_dag.out). No concept is used outside the closure."),
    row("proj-rung-ladder", "2.6-spec ladder",
        f"{PAGE}:41-50 (ladder), :195-216 (spec), :489-498 (rung 4)",
        "PASS",
        "Rung 1 is a fully solved, annotated lab (Lab 1 comments steps 1-6). Rung 2 is a completion lab graded by its instant check (run_labs completion rule). Rung 3 is the spec with the frozen interface (starter.py matches project.html:202). Rung 4 is open-ended and not graded (project.html:493)."),
    row("proj-exemplar-a-calibration", "2.6-rubric-2 (blind calibration)",
        f"{PAGE}:425-454, 474-479 (exemplar A) and rubric {PAGE}:409-419",
        "PASS",
        "Blind scoring from the rubric text alone (done after reading the annotations, which were not used for the scores): C1 2 (layers named in order, no amounts), C2 2 (margin for a stated target, no cover check), "
        "C3 1 (no sharing rule, no survivor amount), C4 2 (margin with no cover), C5 2 (two limits). Official scores 2,2,1,2,2 agree within one level on every criterion."),
    row("proj-exemplar-b-numbers", "2.2-numbers in exemplars",
        f"{PAGE}:456-470",
        "PASS",
        "Numbers recomputed: 30000/50000/40000/20000 margins, 4000/6000/5000/3000 funds, 20000 capital, pool 12000, residual 4000, 38.0 = 9500*40/10000, 111074 = 38th smallest (out/run_labs_project.out, Lab 3 Part B/C), "
        "9250 one cent below, 117088 and 105154, difference 5920 = 111074-105154 (derived), 500 bps step, 2 past margin, 0 past survivors (Lab 3 Part C). All match."),
    row("proj-rubric-c3-descriptors", "2.6-rubric-1 (every level descriptor observable)",
        f"{PAGE}:415 (C3 level 1 and level 2 cells), :464 (exemplar B waterfall text)",
        "FAIL",
        "C3 level 1 requires BOTH 'names no sharing rule' AND 'gives no survivor amount'; level 2 is 'states the pro rata rule only'. A memo that gives survivor amounts but states no rule (the exemplar B waterfall paragraph, project.html:464: 'The survivors pay 1334, 1666 and 1000 cents') matches neither descriptor, so the level is not observable.",
        "Make level 1 'names no sharing rule' (drop the survivor-amount clause), and make level 2 read 'gives survivor amounts, or states the pro rata rule without the leftover rule'. Keep the four levels distinct and re-run the calibration of both exemplars."),
    row("proj-exemplar-b-calibration", "2.6-rubric-2 (blind calibration within one level)",
        f"{PAGE}:458 (official 4 on C3), :462-470 (memo text), :476 (annotation)",
        "FAIL",
        "Official scoring gives C3 = 4 and the annotation at project.html:476 says the memo 'states the pro rata rule and the leftover rule'. The memo text (lines 462-470) contains neither rule: grep for 'pro rata' and 'leftover' in lines 456-482 returns only line 476. "
        "Blind C3 score from the rubric is 1 or 2, which is 2-3 levels from the official 4 (VERIFIER 2.6 item 2 requires within one level). The other four criteria (C1 4, C2 4, C4 4, C5 4) agree.",
        "Add the pro rata rule (share = floor(R * DF_i / T)) and the leftover rule (one cent each to the first survivors with DF > 0, ascending id) to the exemplar B waterfall paragraph, and show that 1334 + 1666 + 1000 = 4000, the residual of Lab 1. "
        "Or lower the official C3 score to match the text. Then re-check the annotation at line 476."),
    row("proj-lab2-learner-text", "2.2 (lab statement) and 2.9 (prose)",
        f"{PAGE}:146-147 (page code docstring); tests/labs/BK4/lab-BK4-project-2.py docstring",
        "FAIL",
        "The docstring shown in the Lab 2 code (the page version has the two blanks) says: 'This file is the completed solution. The page shows the same code with two blanks'. The displayed file is not the completed solution, so the learner-visible text is false for the file on the page (run_labs confirms the page equals the twin except the blanks).",
        "Replace the sentence in the docstring of both the twin tests/labs/BK4/lab-BK4-project-2.py and the page with a neutral description (for example 'Rung 2 completion: the default of Lab 1, with the survivor share and the sizing index left for you to fill in.'). Then run tools/embed_labs.py course/modules/BK/BK4/project.html --refresh lab-BK4-project-2 and tools/run_labs.py --unit BK4 --page project."),
    row("proj-lab3-claim-checks-rules", "2.2 (sentences about what a lab checks)",
        f"{PAGE}:367 (interpretation of Lab 3 Part A)",
        "FAIL",
        "The interpretation says 'Part A checks the layer rules on five losses'. The Part A code (project.html:313-321) only computes the layers and the survivors and prints them, and prints one identity (conservation). No layer rule is asserted or compared.",
        "Rewrite the sentence to what the code does, for example: 'Part A prints the layer amounts for five losses, and its conservation column checks that the layers and the survivors' payments add to each loss.'"),
    row("proj-notation-T", "2.9 notation (rule 13); notation/notation.json:111-113; plan 2.3",
        f"{PAGE}:221 (the 'Survivors' convention)",
        "FAIL",
        "The page uses bare T as the sum of the surviving default funds ('Let T be the sum ... R >= T ... R - T ... R < T'). notation/notation.json:111-113 registers T as the number of return observations (module S1), and the plan (section 2.3) forbids a bare T. The symbols D (no record) and F are not registered.",
        "Rename the symbol in project.html:221 to an unregistered letter such as D (sum of the surviving default funds), including R >= D, R - D and R < D. The grader needs no change (it uses pool and total_fund)."),
    row("proj-mypy-plan-command", "gate note: plan section 10 grader typecheck",
        f"{S}/out/mypy_plan_command.out; {GRADER}:27-29",
        "FAIL",
        "The plan's command 'mypy tests/labs/BK4 course/modules/BK/BK4/grader' reports 'Found 2 errors in 1 file': test_project.py:27 cannot find module clearing_house and :29 cannot find module instance (import-not-found). "
        "The repository gate (pyproject files = tools, tests) is green and the grader is strict-clean in its real layout (out/mypy_grader_layout.out).",
        "Either typecheck the grader in a scratch layout as tools/run_graders.py does (copy test_project.py, instance.py and reference.py as clearing_house.py), or add '# type: ignore[import-not-found]' to the two imports at test_project.py:27 and :29. Then rerun the plan command."),
    row("proj-failure-leak", "2.6-autograder-4 (failure messages never leak the answer); test_project.py:12-13; project.html:400",
        f"{GRADER}: docstrings 316, 321, 326, 503, 510, 524, 573, 578, 598; failing lines 317, 322, 327, 504, 511, 518, 525, 533, 538, 574, 579, 589, 599; {PAGE}:400",
        "FAIL",
        "A failure prints the test's docstring and its asserting line. Observed: the starter run (out/starter_raw.out:33) prints 'A residual of 20 ... gives the survivors 8 and 12', and line 35 prints '10 and 15'; "
        "a learner run with vc08 prints 'the fourth loss, 40' and 'assert sol.margin_for_cover([10, 20, 30, 40, 50], 8_000) == 40' (reproduced in the checkout); vc09 prints 'gives the survivors 8 and 12' for test_fixture_loss_200. "
        "test_project.py:12-13 says 'it never prints an expected value' and project.html:400 says a failure 'shows ... no values'. Both statements are false.",
        "(1) Remove numeric answers from the docstrings listed (state the rule, not the number). (2) Put each expected value in a named variable on an earlier line (for example want = 40) so the failing line shows the name, not the value; the expect_fixture calls take variables. "
        "(3) In the unimplemented wrapper (test_project.py:825-848) print only the property name, not the docstring. (4) Confirm with a scan that no docstring or failing line holds an answer, then re-run run_graders, mutate_graders and the starter run."),
    row("proj-plan-conformance", "plan (binding) sections 5.2, 5.4, 5.5",
        f"{PAGE}:200, :417, :425, :456; course/modules/BK/BK4/grader/instance.py:39; {GRADER}:36, :489-499",
        "FAIL",
        "Four deviations from the binding plan, none a learner-facing defect: (a) plan 5.2 sets target_bps in {9900, 9950, 9975}; the page (project.html:200), instance.py:39 and test_project.py:36 use {9000, 9500, 9750}. "
        "(b) Plan 5.4 gives exemplar-a data-level 4 and exemplar-b data-level 2; the page has exemplar-a at 2 (project.html:425) and exemplar-b at 4 (:456). "
        "(c) Plan 5.4 criterion 5 level 4 names 'no procyclicality'; the page names 'no change in margins in stress' (:417). "
        "(d) Plan 5.5 asks for the brute-force sizing check 'on every seed'; test_project.py:489-499 checks two cases (INST, INST2).",
        "Architect ruling required for each of (a) to (d): either restore the plan's value or record the change in the Architect decisions block of plans/BK4-build-plan.md. Items (b) and (c) are wording or ordering choices; (a) and (d) change the tested behaviour or the spec."),
]

mutants = [
    {"id": "m01_fund_before_margin", "description": "Student error: the defaulter's default fund is used before its initial margin (layer order swapped).", "file": "ledgers/BK4/mutants/m01_fund_before_margin.py", "killed_by": "test_each_scenario_matches_the_oracle_on_both_instances (seed 0)"},
    {"id": "m02_capital_before_fund", "description": "Student error: the CCP capital is used before the defaulter's default fund (layer order swapped).", "file": "ledgers/BK4/mutants/m02_capital_before_fund.py", "killed_by": "test_each_scenario_matches_the_oracle_on_both_instances (seed 0)"},
    {"id": "m03_survivors_by_count", "description": "Student error: surviving members pay equal shares by count, not pro rata to their default funds.", "file": "ledgers/BK4/mutants/m03_survivors_by_count.py", "killed_by": "test_each_scenario_matches_the_oracle_on_both_instances (seed 0)"},
    {"id": "m04_leftover_to_last_survivor", "description": "Student error: the leftover cents go to the last surviving member instead of the first.", "file": "ledgers/BK4/mutants/m04_leftover_to_last_survivor.py", "killed_by": "test_each_scenario_matches_the_oracle_on_both_instances (seed 0)"},
    {"id": "m05_no_remainder_rule", "description": "Student error: survivor shares are truncated and the leftover cents are never paid, so the invariant breaks.", "file": "ledgers/BK4/mutants/m05_no_remainder_rule.py", "killed_by": "test_layers_and_survivor_payments_add_to_the_loss_on_every_scenario (seed 0)"},
    {"id": "m06_uncovered_dropped", "description": "Student error: the uncovered loss above the survivors' total is dropped instead of reported.", "file": "ledgers/BK4/mutants/m06_uncovered_dropped.py", "killed_by": "test_layers_and_survivor_payments_add_to_the_loss_on_every_scenario (seed 0)"},
    {"id": "m07_floor_index", "description": "Student error: the sizing index is the floor of target times count over 10000, not its ceiling.", "file": "ledgers/BK4/mutants/m07_floor_index.py", "killed_by": "test_margin_matches_the_order_statistic_on_both_instances (seed 0)"},
    {"id": "m08_strict_cover", "description": "Student error: the cover counts only losses strictly below the margin, so a loss equal to the margin is not covered.", "file": "ledgers/BK4/mutants/m08_strict_cover.py", "killed_by": "test_two_of_three_scenarios_covered_is_floored_to_6666_bps (seed 0)"},
    {"id": "m09_largest_loss_always", "description": "Student error: the margin for every target is the largest loss, with no quantile at all.", "file": "ledgers/BK4/mutants/m09_largest_loss_always.py", "killed_by": "test_margin_matches_the_order_statistic_on_both_instances (seed 0)"},
    {"id": "m10_seed0_hardcoded", "description": "Student error: the sizing returns the seed-0 margin (73529 cents) for every instance and target.", "file": "ledgers/BK4/mutants/m10_seed0_hardcoded.py", "killed_by": "test_margin_matches_the_order_statistic_on_both_instances (seed 0)"},
    {"id": "vc01_cover_rounded", "description": "Student error: the cover is rounded to the nearest basis point instead of floored.", "file": "ledgers/BK4/mutants/vc01_cover_rounded.py", "killed_by": "test_two_of_three_scenarios_covered_is_floored_to_6666_bps (seed 0)"},
    {"id": "vc02_zero_based_index", "description": "Student error: the sizing reads the zero-based position k instead of the k-th smallest loss (k - 1).", "file": "ledgers/BK4/mutants/vc02_zero_based_index.py", "killed_by": "test_margin_matches_the_order_statistic_on_both_instances (seed 0)"},
    {"id": "vc03_sizing_unsorted", "description": "Student error: the sizing picks the k-th loss as given, without sorting the scenarios first.", "file": "ledgers/BK4/mutants/vc03_sizing_unsorted.py", "killed_by": "test_margin_matches_the_order_statistic_on_both_instances (seed 0)"},
    {"id": "vc04_cover_no_refusal", "description": "Student error: cover_bps accepts a negative loss without raising, so the named refusal is missing.", "file": "ledgers/BK4/mutants/vc04_cover_no_refusal.py", "killed_by": "test_negative_loss_is_refused_in_cover_bps (seed 0)"},
    {"id": "vc05_target_zero_allowed", "description": "Student error: the target range check starts at 0, so a target of 0 bps is accepted and silently sized.", "file": "ledgers/BK4/mutants/vc05_target_zero_allowed.py", "killed_by": "test_target_of_zero_is_refused_in_margin_for_cover (seed 0)"},
    {"id": "vc06_fund_without_min", "description": "Student error: the default fund pays its full contribution even when the loss is smaller, so layers overpay.", "file": "ledgers/BK4/mutants/vc06_fund_without_min.py", "killed_by": "test_each_scenario_matches_the_oracle_on_both_instances (seed 0)"},
    {"id": "vc07_leftover_to_zero_fund", "description": "Student error: the leftover cent goes to a survivor with a zero default fund, skipping the DF > 0 rule.", "file": "ledgers/BK4/mutants/vc07_leftover_to_zero_fund.py", "killed_by": "test_a_member_with_no_default_fund_is_skipped_by_the_remainder_rule (seed 0)"},
    {"id": "vc08_index_plus_one", "description": "Student error: the sizing index is floor(target times count / 10000) plus one, an off-by-one at exact positions.", "file": "ledgers/BK4/mutants/vc08_index_plus_one.py", "killed_by": "test_fixture_five_losses_at_8000_bps_gives_forty (seed 0)"},
    {"id": "vc09_capital_ignored", "description": "Student error: the CCP capital is left out of the waterfall, so the survivors pay the capital's share.", "file": "ledgers/BK4/mutants/vc09_capital_ignored.py", "killed_by": "test_each_scenario_matches_the_oracle_on_both_instances (seed 0)"},
    {"id": "vc10_float_arithmetic", "description": "Student error: integer arithmetic replaced by float division (int of a float share, math.ceil of a float index), exact on small cents but not above 2**53.", "file": "ledgers/BK4/mutants/vc10_float_arithmetic.py", "killed_by": None},
]

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["PASS"] == len(rows) and all(m["killed_by"] for m in mutants) else "FAIL"

fragment = {
    "unit": "BK4",
    "slice": "BK4-c",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for BK4-c (project.html, grader, project labs, mutants, alternatives); did not build BK4",
    "pin": "1c1645f3b00eada2fb54d39c86d5d949e15b4fbc",
    "base": "1c1645f3 (first verification of slice c; no previous fragment)",
    "checkout": str(ROOT),
    "scratch": "/tmp/bk4c-* (temporary workspaces created by the scripts; removed after each run)",
    "verified_at": "2026-11-04T03:56:04+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Read in full: project.html (522 lines), grader/instance.py, reference.py, starter.py, test_project.py (848 lines), the three project lab twins and the project page code blocks. "
        "Exemplar calibration: the blind scores were derived from the rubric text in project.html:409-419 and the exemplar memo text in :425-482; the annotations were read in the same pass, so the blind scoring is not independent of them. "
        "Plan deviations and the one survivor not counted as a FAIL are listed as separate rows. "
        "Not checked by this verifier: Pyodide itself beyond page_smoke (which runs the in-browser grader on the reference only, not on alternatives or mutants); the Pyodide runtime limit per test beyond the 0.8 s suite time; "
        "whether the browser self-assessment form stores data (page_smoke does not exercise it); Duffie and Zhu's abstract (the page states no finding from it, so the plan's B2 gate is not triggered for this slice); "
        "live freshness of 2025-2026 literature (no debate brief; not required for BK4). Hours were estimated by the verifier (ruling: hours are design targets; only arithmetic inconsistencies fail, and there are none)."
    ),
    "summary": (
        f"BK4-c round 1: verdict {verdict}. {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE of {len(rows)} rows. "
        f"Mutants: 20 in ledgers/BK4/mutants (10 builder, 9 verifier, 1 verifier survivor): 19 killed on seeds 0-9; vc10 float arithmetic survives. "
        "Alternatives: 5 verifier-written and 5 builder-written correct implementations each pass seeds 0-49 (50/50). Failing rows: float survivor, failure-message leak, Lab 2 learner text, Lab 3 Part A claim, bare T notation, rubric C3 descriptor, exemplar B C3 calibration, plan-conformance (four items), mypy plan command."
    ),
}

problems: list[str] = []
for r in rows:
    if r["status"] != "PASS" and not r.get("fix", "").strip():
        problems.append(f"no fix for {r['id']}")
out = ROOT / "ledgers" / "BK4" / "BK4-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out.relative_to(ROOT), counts, "verdict", verdict, "problems", problems)
