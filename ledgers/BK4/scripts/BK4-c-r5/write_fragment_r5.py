"""Writes the round-5 fragment ledgers/BK4/BK4-c.json for slice c (project.html, grader, project labs, mutants).

The mutant list is parsed from out/mutate_seeds0-9_all44.out, the exact output of
`tools/mutate_graders.py --unit BK4 --seeds 0-9` on the pin, so every killed_by is copied, not typed.
Usage: python -I write_fragment_r5.py <checkout>
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
OUT_DIR = ROOT / "ledgers/BK4/scripts/BK4-c-r5/out"
MUTATE = OUT_DIR / "mutate_seeds0-9_all44.out"

mutants = []
for line in MUTATE.read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, description, killed = m.groups()
    description = description.replace("Student error: ", "", 1).rstrip(".")
    killed_by = None if killed.strip() == "None" else killed.strip()
    mutants.append({"id": name[:-3], "description": description, "killed_by": killed_by})
assert len(mutants) == 44, len(mutants)

S = "ledgers/BK4/scripts/BK4-c-r5/out/"
R = lambda i, check, loc, status, evidence, fix="": {  # noqa: E731
    "id": i, "check": check, "location": loc, "status": status, "evidence": evidence,
    **({"fix": fix} if fix else {}),
}

rows = [
    R("proj-lab1-numbers", "2.5-labs, 2.2-numbers", "course/modules/BK/BK4/project.html:56-139; tests/labs/BK4/lab-BK4-project-1.py", "PASS",
      f"run_labs.py --unit BK4 --page project: PASS (3/3) ({S}run_labs_project.out); twin run directly with python -I -W error: exit 0, output in {S}twins_project_direct.out; "
      f"independent re-derivation scripts/BK4-c-r5/rederive_r5.py ({S}rederive_r5.out) gives layers 50000/6000/20000, residual 4000, floored shares 1333/1666/1000 with leftover 1 to member 1, exact position 191/5, k=39, margin 117088, cover 9750 at the margin and 9500 one cent below."),
    R("proj-lab2-numbers", "2.5-labs, 2.2-numbers", "course/modules/BK/BK4/project.html:141-190; tests/labs/BK4/lab-BK4-project-2.py", "PASS",
      f"run_labs PASS for lab-BK4-project-2 (completion rule: every page line equals the twin line or has a blank); twin output {S}twins_project_direct.out: survivor shares {{1: 1334, 3: 1666, 4: 1000}}, k = 39, margin 117088. The interpretation's tolerance claim: 1e-6 times (1 + 117088) = 0.117 cents, below one cent, so a wrong cent fails (run_labs tolerance rule, tools/run_labs.py docstring)."),
    R("proj-lab3-numbers", "2.5-labs, 2.2-numbers", "course/modules/BK/BK4/project.html:252-366; tests/labs/BK4/lab-BK4-project-3.py", "PASS",
      f"run_labs PASS; twin output {S}twins_project_direct.out: Part A five rows (conservation True x5, 12000 uncovered in the 100000 row); Part B 40 scenarios, largest loss 118151, margins 105154/111074/117088 with k 36/38/39, covers 9000/9500/9750, one cent below 8750/9250/9500, brute force agrees x3; Part C counts (past margin, past fund, past capital, past survivors) = (2,2,0,0) at 9500 and (4,2,0,0) at 9000. All reproduced independently in {S}rederive_r5.out (partA, brute, partC lines)."),
    R("proj-fixture-tables", "2.4-mathematics, 2.6-tests", "course/modules/BK/BK4/project.html:229-250; course/modules/BK/BK4/grader/test_project.py:281-441", "PASS",
      f"Layer-order table: all 11 rows (losses 80..300) recomputed in {S}rederive_r5.out (fixture lines) and each equals the page row; remainder fixture (defaulter 4, survivors 1,2,3 with 1 cent): loss 1 -> {{1:1,2:0,3:0}}, loss 2 -> {{1:1,2:1,3:0}}, loss 4 -> 1 uncovered; sizing fixtures 40/50/50 and 20; cover fixtures 3333 and 6666 (20000/3 floored). Each row has an isolated test in test_project.py; reference passes (run_graders 50/50)."),
    R("proj-named-conditions", "2.6-spec, 2.6-tests, 2.6-failure-messages", "course/modules/BK/BK4/project.html:203-212; test_project.py:459-597, 839-933", "PASS",
      "Each named condition of the six bullets (project.html:205-210) has a must_refuse test, and each has an accepting test on the other side of its limit (zero loss, zero margin, zero fund, zero capital, target 1, target 10000, one scenario, the lowest and highest defaulter id, the non-contiguous member). Suite run: 83 passed (scripts out/run_graders_seeds0-49.out)."),
    R("proj-conventions-prose", "2.2-numbers, 2.9-prose", "course/modules/BK/BK4/project.html:219-223; course/modules/BK/BK4/grader/reference.py:1-109", "PASS",
      "Layer order, survivor rule, conservation, cover and sizing bullets (project.html:219-223) match reference.py lines 36-109 and rederive_r5.py. The Money bullet (project.html:224) is row proj-money-integer-claim."),
    R("proj-hours", "2.9-hours", "course/modules/BK/BK4/project.html:373-388 (table#hours); course/modules/BK/BK4/index.html:29", "PASS",
      "Rationale hours 2+2+3+3+2+2+1 = 15 (project.html:376-383), equal to data-hours-project=15 (project.html:34); index.html:29 data-hours-lessons=35, data-hours-project=15, 35+15=50; check_pages.py --unit BK4 PASS. Hours are design targets (ruling), so only the arithmetic is checked."),
    R("proj-grader-reference-run", "2.6-tests, 2.8-gate", "course/modules/BK/BK4/grader/reference.py; course/modules/BK/BK4/grader/test_project.py", "PASS",
      f"run_graders.py --unit BK4 --seeds 0-49: PASS (reference 50/50 seeds) ({S}run_graders_seeds0-49.out); direct QF_SEED=0 pytest: 83 passed."),
    R("proj-grader-starter-fails", "2.6-tests", "course/modules/BK/BK4/grader/starter.py; course/modules/BK/BK4/grader/test_project.py:1063-1086", "PASS",
      "run_candidates_r5.py on starter.py: passed 0/50 seeds; the failure names the test and the missing function (test_waterfall_returns_plain_int_money: 'the student module has no implementation for waterfall yet'), with no traceback (test_project.py:1063-1086)."),
    R("proj-collect-count", "2.6-tests", "course/modules/BK/BK4/project.html:214; course/modules/BK/BK4/grader/test_project.py", "PASS",
      "pytest --collect-only -q on test_project.py: 83 tests collected; project.html:214 says 'runs 83 checks'. Equal."),
    R("proj-instances", "2.6-instances, 2.2-numbers", "course/modules/BK/BK4/grader/instance.py:22-50", "PASS",
      f"scripts/BK4-c-r5/sample_instances_r5.py ({S}sample_instances_r5.out): seeds 0-49 all valid (ids 1..N with N in 4..6, defaulter a member, DF >= 1, IM >= 0, K >= 0, S in 40..80, integer non-negative losses, target in {{9000,9500,9750}}, the three designed scenarios in place). Materiality: 50 distinct sizing answers over seeds 0-49, 49 differ from seed 0; 48 distinct total-uncovered values. 20 sampled seeds listed with their answers in the same file."),
    R("proj-mutants-builder", "2.6-mutants", "ledgers/BK4/mutants/m01_fund_before_margin.py .. m10_seed0_hardcoded.py", "PASS",
      f"mutate_graders.py --unit BK4 --seeds 0-9 ({S}mutate_seeds0-9_all44.out): m01-m10 all KILLED."),
    R("proj-mutants-own", "2.6-mutants", "ledgers/BK4/mutants/r3a..r3f, r4a..r4h, r5a..r5f, vc01..vc15 (no vc11)", "FAIL",
      f"mutate_graders.py --unit BK4 --seeds 0-9 over 44 mutants: 42 killed. SURVIVED r5c_sizing_drops_zero_losses_before_counting.py and r5d_cover_denominator_excludes_zero_losses.py, each passing 50/50 seeds ({S}r5_mutants_seeds0-49.out). Both are plausible student errors that the page's definitions reject (project.html:222-223). Details in rows proj-zero-loss-sizing and proj-zero-loss-cover. The other 42 mutants, including the six new ones r5a, r5b, r5e, r5f, are killed.",
      "Add the two zero-loss fixtures named in rows proj-zero-loss-sizing and proj-zero-loss-cover to test_project.py; the candidate was run on a scratch copy and both mutants then fail while reference and alt1-alt5 pass (out/candidate_zero_loss_tests.out)."),
    R("proj-large-cent-claim", "2.2-numbers, 2.6-tests", "course/modules/BK/BK4/grader/test_project.py:442-451", "PASS",
      f"rederive_r5.py ({S}rederive_r5.out): loss x fund = 4.4e31 > 2**53 (the test's docstring claim holds). Floors 6055950114045319 and 529746839784068, leftover 1 to member 1, giving 6055950114045320 and 529746839784068 as the test expects."),
    R("proj-mutant-float", "2.6-mutants, 2.2-money", "ledgers/BK4/mutants/vc10_float_arithmetic.py; course/modules/BK/BK4/grader/test_project.py:442-451", "PASS",
      "vc10_float_arithmetic.py KILLED by test_large_cent_shares_are_floored_in_integers (seed 0), per the mutate output."),
    R("proj-mutant-argument", "2.6-mutants, 2.6-purity", "ledgers/BK4/mutants/r4f_sizing_sorts_caller_list_in_place.py; course/modules/BK/BK4/project.html:203; test_project.py:1034-1040", "PASS",
      "r4f_sizing_sorts_caller_list_in_place.py KILLED by test_margin_for_cover_and_cover_bps_do_not_change_their_list_argument (seed 0). The purity sentence (project.html:203) is now tested for the list argument."),
    R("proj-labs-simulated-stdlib", "2.6-simulated, 2.9-data", "tests/labs/BK4/lab-BK4-project-1..3.py; course/modules/BK/BK4/project.html:54; grader/instance.py:1-7", "PASS",
      "The three twins import only random (lab-BK4-project-1 line 7, -2 line 6, -3 line 8), read in full; each is labelled SIMULATED in its module docstring (line 3 of each twin) and in the page text (project.html:54, 194-199); run_labs PASS."),
    R("proj-page-smoke", "2.9-links, 2.10-browser", "course/modules/BK/BK4/project.html", "PASS",
      f"page_smoke.py --unit BK4 --pages project: PASS, including the in-browser grader ('All 83 tests pass') and the three project labs under Pyodide ({S}page_smoke_project.out)."),
    R("proj-check-tools", "2.10-gates", "course/modules/BK/BK4/project.html", "PASS",
      f"check_pages.py --unit BK4: PASS; check_dag.py --unit BK4: PASS; check_projects.py --unit BK4: PASS ({S}check_pages.out, check_dag.out, check_projects.out)."),
    R("proj-ruff", "2.10-gates", "tests/labs/BK4; course/modules/BK/BK4/grader", "PASS",
      f"ruff check tests/labs/BK4 course/modules/BK/BK4/grader: All checks passed; ruff format --check: 12 files already formatted ({S}ruff_check_slice.out, ruff_format_slice.out)."),
    R("proj-mypy-repo", "2.10-gates", "pyproject.toml [tool.mypy]", "PASS",
      f"mypy --no-incremental (repository): Success, no issues found in 385 source files ({S}mypy_repo.out)."),
    R("proj-pytest-labs", "2.10-gates", "tests/test_labs.py; tests/test_run_labs.py", "PASS",
      f"pytest -q tests/test_labs.py tests/test_run_labs.py -k labs: all passed ({S}pytest_labs_slice.out). tests/test_memo_exemplars.py covers S7 only and passed ({S}pytest_memo_page_checks.out)."),
    R("proj-refs", "2.3-citations", "course/modules/BK/BK4/project.html:501-505 (reading list); references/references.json:7411 (duffie2011central), :2853 (bisndcpmi)", "PASS",
      f"verify_refs.py --offline (whole registry): 560 entries, 0 problems ({S}verify_refs_offline_all.out). Both keys exist. The page attributes no statement to either source (project.html:501). Live Crossref or issuer re-resolution was not run by this verifier."),
    R("proj-banned-and-process-words", "2.9-prose", "course/modules/BK/BK4/project.html; grader/*.py; tests/labs/BK4/lab-BK4-project-*.py", "PASS",
      "grep, case-insensitive, for every banned string (BUILDER_RULES 1.3-1.4) and for process words (build, builder, verif, round, REQUEST, planner, fixer, architect, TODO, TBD, ...) and for '...': no hit in learner text. The only hits are 'rounded' and 'rounding' (arithmetic). reference.py's docstring names BLUEPRINT, a design document; it is not a planning reference and is not learner text."),
    R("proj-anchors-links", "2.9-links", "course/modules/BK/BK4/project.html", "PASS",
      "Every fragment link target exists: index.html#placement (index.html), and in project.html the ids ladder, spec, grader-section, report, rubric-heading, self-assessment, stretch, conventions, fixtures, h-spec. The file links grader/starter.py, grader/test_project.py and grader/instance.py exist."),
    R("proj-dag-concepts", "2.14-DAG", "course/modules/BK/BK4/project.html", "PASS",
      "grep: project.html has no <dfn>, no data-concept and no class=\"concept\" link, so no concept is used by link outside the closure; check_dag.py --unit BK4 PASS."),
    R("proj-rung-ladder", "2.1-structure", "course/modules/BK/BK4/project.html:41-50 (ladder), :193-216 (spec), :490-497 (rung 4)", "PASS",
      "check_projects.py --unit BK4 PASS. The ladder lists rungs 1 to 4 in order; rung 4 (line 492) is marked not graded; rung 2 is a completion lab (line 141)."),
    R("proj-exemplar-a-calibration", "2.7-rubric-calibration", "course/modules/BK/BK4/project.html:424-453 (exemplar A), :408-417 (rubric)", "UNVERIFIABLE",
      "Not blind. The annotations (project.html:442-451) were read before scoring. Scoring from the descriptors and the exemplar body text gives C1 2, C2 2, C3 1, C4 2, C5 2, which equals data-scores 2,2,1,2,2 (line 424). A blind calibration (annotations hidden) was not performed, so the calibration requirement (VERIFIER 2.6 rubric 2) is not met by this verifier.",
      "A fresh verifier that did not read the annotations scores exemplar A blind against the rubric (lines 408-417) and must land within one level on every criterion of the annotations at lines 442-451."),
    R("proj-exemplar-b-numbers", "2.2-numbers, 2.7-rubric", "course/modules/BK/BK4/project.html:455-481 (exemplar B), :422 and :457 (disclosure), :467 (5920)", "FAIL",
      "Every number in exemplar B is printed by Lab 1 or Lab 3 or follows from the instance inputs (38.0 = 9500 x 40 / 10000; 1334, 1666, 1000; 4000; 12000; 111074; 105154; 117088; 9250; 2 and 4 scenarios). The exception is 5920 cents (project.html:467), the difference 111074 - 105154 (rederive_r5.out, 'difference'). The memo rule at line 404 allows a difference of printed numbers, but the disclosure at lines 422 and 457 says the exemplar quotes only printed numbers or numbers the instance inputs give by computation, which 5920 is not on its face.",
      "Amend the disclosure at project.html:422 and :457 to 'or a difference or ratio of two printed numbers, as line 404 allows', or remove the 5920 sentence at line 467."),
    R("proj-rubric-c3-descriptors", "2.7-rubric", "course/modules/BK/BK4/project.html:414", "PASS",
      "C3 level descriptors (4: pro rata and leftover rules with the sum that checks them; 3: the same without the sum; 2: one rule, or survivor amounts; 1: no sharing rule) are observable as written (line 414)."),
    R("proj-exemplar-b-calibration", "2.7-rubric-calibration", "course/modules/BK/BK4/project.html:455-481 (exemplar B), :457 (official scoring)", "UNVERIFIABLE",
      "Not blind, for the same reason as proj-exemplar-a-calibration. Scoring from the descriptors gives C1 4, C2 4, C3 4, C4 4, C5 4, which equals data-scores 4,4,4,4,4 (line 455). Blind calibration was not performed.",
      "A fresh verifier that did not read the annotations (lines 471-479) scores exemplar B blind and must land within one level on every criterion."),
    R("proj-lab2-learner-text", "2.9-prose", "course/modules/BK/BK4/project.html:146-147, :186; tests/labs/BK4/lab-BK4-project-2.py:1-3", "PASS",
      "Learner text of Lab 2 (docstring lines 1-3 of the twin, page lines 146-147 and 186) contains no process word and no planning reference."),
    R("proj-lab3-claim-checks-rules", "2.2-numbers, 2.9-prose", "course/modules/BK/BK4/project.html:253-366 (Lab 3 hypothesis and interpretation)", "PASS",
      "Each Lab 3 claim checked against the twin output and rederive_r5.out: five waterfall rows and conservation True in each; the 100000 row is the only uncovered row; three sizing indices 36, 38, 39; margins 105154, 111074, 117088; covers at the margins 9000, 9500, 9750 and one cent below 8750, 9250, 9500 (each short of its target); brute force agrees for each target; Part C counts as printed."),
    R("proj-notation-T", "2.13-notation", "course/modules/BK/BK4/project.html; notation/notation.json (symbols)", "PASS",
      "grep: no registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}, \\R) appears in project.html. The page's local symbols (L, S, M, t, k, D, R, K, Lambda, IM_d, DF_d, a1 to a3) are not registered in notation.json."),
    R("proj-failure-leak", "2.6-failure-messages", "course/modules/BK/BK4/grader/test_project.py; project.html:398-399", "PASS",
      "grep: no failure message interpolates a computed answer (only condition names, targets and seed-free labels). Every test and helper that can fail carries __tracebackhide__ (AST check: all 83 tests have it). The page's command uses --assert=plain (project.html:398-399)."),
    R("proj-plan-conformance", "2.9-plan", "plans/BK4-build-plan.md:458, :438-446, :476-482, :515-517, :743-748; plans/BK4-open-items.md; course/modules/BK/BK4/project.html:208, :223; grader/test_project.py:714-722, :903-910", "FAIL",
      "(i) plan 5.5 (line 517) requires monotonicity 'on each seed'; test_margin_is_non_decreasing_in_the_target (test_project.py:714-722) checks INST and INST2 only. (ii) plan 5.3 (line 458) says the period convention is 'stated once'; project.html has no statement of it (grep 'period' finds only line 469). (iii) plan 5.2 (lines 438-446) names five exception conditions; the page and the suite also require cover_bps with empty losses (project.html:208, test_project.py:903-910), which the plan does not list. (iv) builder edits to the binding plan (lines 419, 478, 481, 515 per plans/BK4-open-items.md) have no Architect ruling; the open-items file says the ruling is pending.",
      "Architect rules on (i) to (iv) and records each in the Architect decisions block. If (i) stands, extend the monotonicity test to seeds 0-49. If (ii) stands, add the period sentence to the conventions. If (iii) stands, amend plan 5.2. Revert any plan edit that is not ratified."),
    R("proj-sizing-duplicate-losses", "2.6-tests, 2.2-numbers", "course/modules/BK/BK4/project.html:223; course/modules/BK/BK4/grader/test_project.py:670-682, 784-788", "PASS",
      "Recomputed: margin_for_cover([5,5,10,20], 5000) = 5 (k = 2), margin_for_cover([5,5,5,9,12], 6000) = 5 (k = 3), cover_bps([5,5,10,20], 5) = 5000. The tests assert these values and the reference passes them."),
    R("proj-context-sentences", "2.6-spec", "course/modules/BK/BK4/project.html:196-197 (spec Context)", "PASS",
      "The Context sentences describe the layer order (project.html:197) that reference.py implements, and the statement 'The autograder checks the cent results and the cover values, not the docstring or the imports' is true of test_project.py (no test reads a docstring)."),
    R("proj-alternatives", "2.6-alternatives", "ledgers/BK4/alternatives/alt1_comprehensions.py .. alt5_bisection.py", "PASS",
      f"run_candidates_r5.py, seeds 0-49: alt1 to alt5 each pass 50/50 ({S}alternatives_seeds0-49.out). Each read in full: alt1 (sorted() and comprehensions, ceiling by (x+9999)//10000), alt2 (ClearingHouse class returning the frozen Waterfall), alt3 (Fraction with math.floor and math.ceil on exact values), alt4 (integer two-pass with itertools.islice), alt5 (bisection over integer margins on the cover predicate, no sort). They differ in algorithm, as the plan 5.5 list asks."),
    R("proj-mypy-plan-command", "2.10-gates", "course/modules/BK/BK4/grader/test_project.py:28, :30", "PASS",
      f"mypy --no-incremental tests/labs/BK4 course/modules/BK/BK4/grader: Success, no issues found in 12 source files ({S}mypy_slice_plan_cmd.out)."),
    R("proj-survivor-leftover-order", "2.6-mutants, 2.6-spec", "ledgers/BK4/mutants/r4a_leftover_in_mapping_order.py; course/modules/BK/BK4/grader/test_project.py:421-429", "PASS",
      "r4a_leftover_in_mapping_order.py KILLED by test_leftover_cent_goes_to_the_lowest_id_when_the_dictionaries_list_members_out_of_order (seed 0). The round-4 gap is closed."),
    R("proj-silence-named-refusals", "2.6-tests, 2.9-prose", "ledgers/BK4/mutants/r4g_debug_print_on_defaulter_refusal.py; r4h_debug_print_on_uncovered_loss.py; course/modules/BK/BK4/grader/test_project.py:982-1031", "PASS",
      "r4g KILLED by test_refused_inputs_print_nothing_before_they_raise (seed 0); r4h KILLED by test_the_module_prints_nothing_on_valid_inputs (seed 0). The docstring count error in that test is row proj-refusal-count-docstring."),
    R("proj-refusal-count-docstring", "2.6-tests, 2.9-prose", "course/modules/BK/BK4/grader/test_project.py:994", "FAIL",
      f"The docstring of test_refused_inputs_print_nothing_before_they_raise says 'Each of the thirteen named refusals'. The AST of the test lists 15 refusal entries (lines 997-1026; {S}count_refusals_r5.out).",
      "Change 'thirteen' to 'fifteen' in the docstring at test_project.py:994, or drop the count."),
    R("proj-remainder-spec", "2.6-spec", "course/modules/BK/BK4/project.html:248 (remainder fixture); course/modules/BK/BK4/grader/test_project.py:362-368", "PASS",
      "The page now names the defaulter as member 4 with no margin, fund or capital (project.html:248), and remainder_case uses defaulter 4 (test_project.py:362-368). The fixture values match the page (see proj-fixture-tables)."),
    R("proj-rubric-c5-descriptor", "2.7-rubric", "course/modules/BK/BK4/project.html:416 (C5 level 3)", "PASS",
      "C5 level 3 now reads 'states the direction in which each one biases the sized margin or the cover', which an observer can check (higher or lower). The round-4 vague descriptor is fixed."),
    R("proj-money-integer-claim", "2.9-prose, 2.2-numbers", "course/modules/BK/BK4/project.html:224 (also :203, :222, :250)", "FAIL",
      "project.html:224 says 'The exact value of every output is an integer, so no output is rounded.' That is false for two outputs: a survivor's share is R x DF / D, not an integer (rederive_r5.out: exact shares 4000/3, 5000/3), and a cover is floored (project.html:222 and :250, '6666.67 ... the floor of 20000 / 3'). Line 203 says 'no rounding step appears' while the same paragraph floors a share.",
      "Rewrite project.html:224 to: 'Every amount is an int number of cents. The margin, the layers and the uncovered loss are exact integers. A survivor's share and a cover are exact fractions, floored to an integer; the floor is the only rounding in the simulator.' Make line 203 agree."),
    R("proj-zero-loss-sizing", "2.6-tests, 2.2-numbers, 2.6-mutants", "course/modules/BK/BK4/grader/test_project.py:604-727 (sizing tests; no zero-loss fixture); course/modules/BK/BK4/project.html:223", "FAIL",
      f"Mutant r5c_sizing_drops_zero_losses_before_counting.py survives on seeds 0-9 and on 0-49 (passed 50/50; {S}r5_mutants_seeds0-49.out). The page defines the sizing as the k-th smallest of the S scenario losses (project.html:223) and a loss of zero is a valid scenario (project.html:207-209). No test asserts a sizing answer on a list containing a zero loss: the only zero-loss sizing check is must_accept on [0, 0] (test_project.py:900). No seeded instance has a zero loss (zero_losses_in_instances.out).",
      "Add to test_project.py: assert margin_for_cover([0, 10, 20, 30], 5_000) == 10 (k = 2 over all four scenarios). Verified on a scratch copy: reference and alt1 to alt5 pass, and r5c fails (scripts/BK4-c-r5/candidate_zero_loss_tests.py; out/candidate_zero_loss_tests.out)."),
    R("proj-zero-loss-cover", "2.6-tests, 2.2-numbers, 2.6-mutants", "course/modules/BK/BK4/grader/test_project.py:736-789 (cover tests; zero-loss only at :932); course/modules/BK/BK4/project.html:222", "FAIL",
      f"Mutant r5d_cover_denominator_excludes_zero_losses.py survives on 0-9 and on 0-49 (passed 50/50; {S}r5_mutants_seeds0-49.out). The page divides the cover by S, the number of scenarios (project.html:222), and that count includes zero losses. The only zero-loss cover check is must_accept on [0, 0] with margin 0 (test_project.py:932), which does not check the value.",
      "Add to test_project.py: assert cover_bps([0, 0, 5, 9], 0) == 5_000 (the two zero losses count in the four-scenario denominator). Verified on a scratch copy as above (out/candidate_zero_loss_tests.out)."),
]

fragment = {
    "unit": "BK4",
    "slice": "BK4-c",
    "round": 5,
    "verifier": "Claude Haiku 5.5, independent verifier for BK4-c (round 5); did not build BK4",
    "pin": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f",
    "base": "9a02b1af (round-4 pin; previous fragment /Users/billyribeiro/.fanout/frags/E-BK4-c.round4.json, used as context only, no PASS row carried)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE5-BK4-c",
    "scratch": "/tmp/bk4c5, /tmp/bk4c5_zero (suite and candidate copies; not part of the ledger)",
    "verified_at": "2026-11-04T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Read in full this round: project.html (521 lines), grader/instance.py, reference.py, starter.py, test_project.py (1086 lines), "
        "the three project twins, the five alternatives (alt1 to alt5), and the delta 9a02b1af..7376a5e for the slice (project.html hunks, "
        "test_project.py hunks). No previous PASS row was carried: every PASS row was re-derived or re-run this round. "
        "Mutants: 44 in ledgers/BK4/mutants (38 previous, 6 new: r5a to r5f). Two new student-error mutants survive (r5c, r5d). "
        "Calibration was not blind (the annotations were read first), so both exemplar calibration rows are UNVERIFIABLE. "
        "Not checked: a live verify_refs run (network); the self-assessment form in a real browser (page_smoke only); the Duffie and Zhu abstract "
        "(the page makes no statement attributed to it, so no attribution row needed it); hours beyond arithmetic (ruling); "
        "the lesson-level text (other slices)."
    ),
    "summary": (
        "BK4-c round 5: verdict FAIL. 39 PASS, 7 FAIL, 2 UNVERIFIABLE of 48 rows. Mutants: 42/44 killed on seeds 0-9 "
        "(survivors r5c and r5d, both FAIL rows). Alternatives: alt1 to alt5 and the reference pass 50/50 seeds; starter fails 50/50. "
        "Reference: 83 tests collected and passing; the page says 83."
    ),
}

path = ROOT / "ledgers/BK4/BK4-c.json"
path.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", path, "rows", len(rows), "mutants", len(mutants))
