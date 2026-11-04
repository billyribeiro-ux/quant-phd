"""Writes ledgers/BK4/BK4-c.json (round 6) from the verifier's own outputs. Usage: write_fragment_r6.py <checkout>."""
import datetime
import json
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
out_dir = root / "ledgers/BK4/scripts/BK4-c-r6/out"
pin = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()

mutants = []
for line in (out_dir / "mutate_seeds0-9_all48.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+): (.*) -> (.*)$", line)
    if not m:
        continue
    status, fname, desc, killer = m.groups()
    killed_by = ""
    if status == "KILLED":
        killed_by = "seeds 0-9: " + killer.strip()
    else:
        killed_by = ""
    mutants.append({
        "id": fname.removesuffix(".py"),
        "description": desc,
        "file": f"ledgers/BK4/mutants/{fname}",
        "killed_by": killed_by,
        "seeds_0_49": ("survived 50/50 seeds (new_mutants_seeds0-49.out)" if status == "SURVIVED" else
                       "killed on seeds 0-9 by mutate_graders (mutate_seeds0-9_all48.out); see run_candidates for the new four"),
    })

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

O = "ledgers/BK4/scripts/BK4-c-r6/out/"
NEW_FIX = ("Add a test to test_project.py: waterfall(10, 3, {1: 500, 2: 500, 3: 100}, {1: 40, 2: 60}, 30) must raise "
           "ValueError naming defaulter_id. Candidate verified on a scratch copy: reference passes 86 of 86, mutant n1 "
           "fails, alt1 to alt5 pass 50/50 seeds with it (scripts/BK4-c-r6/candidate_defaulter_test_project.py).")

rows = [
 row("proj-lab1-numbers", "2.5-labs, 2.2-numbers", "course/modules/BK/BK4/project.html:56-139; tests/labs/BK4/lab-BK4-project-1.py", "PASS",
     f"run_labs --unit BK4 --page project: PASS (3/3) ({O}run_labs_project.out). page code vs twin: code==twin True, expected==output True ({O}twin_vs_page.out). Twin under python -I -W error: exit 0 ({O}twin_project_1.out). Re-derivation {O}rederive_r6.out: layers 50000/6000/20000, residual 4000, floored shares 1333/1666/1000, leftover 1 to member 1, k 39, margin 117088, cover 9750 at margin and 9500 one cent below."),
 row("proj-lab2-numbers", "2.5-labs, 2.2-numbers", "course/modules/BK/BK4/project.html:141-190; tests/labs/BK4/lab-BK4-project-2.py", "PASS",
     f"Completion rule checked line by line: page code has 42 lines, twin 43; the only differing lines (page 25 and 38) contain '___' (recheck run in this round). Twin output {O}twin_project_2.out: shares {{1:1334,3:1666,4:1000}}, k 39, margin 117088. Expected block == output ({O}twin_vs_page.out). Tolerance 1e-6*(1+117088)=0.117 cent (run_labs rule), so a wrong cent fails."),
 row("proj-lab3-numbers", "2.5-labs, 2.2-numbers", "course/modules/BK/BK4/project.html:252-366; tests/labs/BK4/lab-BK4-project-3.py", "PASS",
     f"Twin exit 0 ({O}twin_project_3.out); expected==output ({O}twin_vs_page.out). Re-derived in {O}rederive_r6.out: Part A rows (5, conservation True, 12000 uncovered only at 100000); Part B k 36/38/39, margins 105154/111074/117088, covers 9000/9500/9750, one cent below 8750/9250/9500, brute force agrees; Part C past-margin/fund/capital/survivors (2,2,0,0) at 9500 and (4,2,0,0) at 9000."),
 row("proj-fixture-tables", "2.4-mathematics, 2.6-tests", "course/modules/BK/BK4/project.html:229-250; course/modules/BK/BK4/grader/test_project.py:281-441", "PASS",
     f"All 11 layer-order rows (losses 80..300) recomputed by an independent oracle ({O}rederive_r6.out 'fixture' lines) and equal the page rows; remainder fixture rows (loss 1, 2, 4) equal; sizing fixtures 40/50/50/20 and cover fixtures 3333 and 6666 equal. Reference passes all 85 tests (run_graders 50/50)."),
 row("proj-named-conditions", "2.6-spec, 2.6-tests, 2.6-failure-messages", "course/modules/BK/BK4/project.html:201, :203-212; course/modules/BK/BK4/grader/test_project.py:459-597, 919-933", "FAIL",
     f"Each of the six named bullets has a must_refuse test and an accepting test on the other side, EXCEPT one direction of 'defaulter_id is not one of the member ids' (project.html:210). Page line 201 says 'the member ids are the keys of default_fund_cents'. Input waterfall(10, 3, {{1:500,2:500,3:100}}, {{1:40,2:60}}, 30): reference raises ValueError ('defaulter_id 3 is not one of the member ids'); mutant n1 (checks margins only) raises KeyError 3 and passes all 85 tests on seeds 0-49 ({O}new_mutants_seeds0-49.out; probe {O}n1_probe_mutant.out vs {O}n1_probe_reference.out). No test uses a defaulter present in one dictionary only.",
     NEW_FIX),
 row("proj-conventions-prose", "2.2-numbers, 2.9-prose", "course/modules/BK/BK4/project.html:219-224; course/modules/BK/BK4/grader/reference.py:1-109", "PASS",
     "Layer order, survivor rule, leftover rule, conservation, cover floor, ceiling index and money bullets (project.html:219-224) match reference.py and the oracle in test_project.py (read in full this round)."),
 row("proj-hours", "2.9-hours", "course/modules/BK/BK4/project.html:373-388 (table#hours); course/modules/BK/BK4/index.html:29", "PASS",
     "Rationale table hours 2+2+3+3+2+2+1 = 15; project.html data-hours-project=15; index.html:29 data-hours-lessons=35 and data-hours-project=15, 35+15=50; 15/50 = 30 % (project.html table total row). Hours are design targets (ruling); arithmetic only."),
 row("proj-grader-reference-run", "2.6-tests, 2.8-gate", "course/modules/BK/BK4/grader/reference.py; course/modules/BK/BK4/grader/test_project.py", "PASS",
     f"run_graders --unit BK4 --seeds 0-49: 'run_graders BK4: PASS (reference 50/50 seeds, slowest 0.2 s)' exit 0 ({O}run_graders_seeds0-49.out). Scratch copy seed 0: 85 passed."),
 row("proj-grader-starter-fails", "2.6-tests", "course/modules/BK/BK4/grader/starter.py; course/modules/BK/BK4/grader/test_project.py:1079-1102", "PASS",
     f"Starter under pytest, seed 0: exit 1, zero Traceback lines, first failure 'test_waterfall_returns_plain_int_money: the student module has no implementation for waterfall yet' ({O}recheck_r6.out). run_candidates on starter: 0/50 seeds ({O}alternatives_seeds0-49.out)."),
 row("proj-collect-count", "2.6-tests", "course/modules/BK/BK4/project.html:214; course/modules/BK/BK4/grader/test_project.py", "PASS",
     "pytest --collect-only -q (scratch copy with test_project.py and instance.py): '85 tests collected'. project.html:214 says 'runs 85 checks'. Equal. Raw def test_ count 85; all 85 carry __tracebackhide__ (AST, recheck_r6.out)."),
 row("proj-instances", "2.6-instances, 2.2-numbers", "course/modules/BK/BK4/grader/instance.py:22-50", "PASS",
     f"Re-checked seeds 0-49 with the page's validity rules ({O}instances_r6.out): invalid seeds none; 50 distinct sizing answers; 49 seeds differ from seed 0 (plan 5.5 requires at least 40)."),
 row("proj-mutants-builder", "2.6-mutants", "ledgers/BK4/mutants/m01_fund_before_margin.py .. m10_seed0_hardcoded.py", "PASS",
     f"tools/mutate_graders.py --unit BK4 --seeds 0-9 over all 48 mutants ({O}mutate_seeds0-9_all48.out): m01-m10 all KILLED (first killing tests listed in the mutants array)."),
 row("proj-mutants-own", "2.6-mutants", "ledgers/BK4/mutants/r3a..r3f, r4a..r4h, r5a..r5f, vc01..vc15 (no vc11), n1..n4", "FAIL",
     f"Round 6 mutate run over 48 mutants: 47 killed on seeds 0-9. r5c and r5d (killed now by test_zero_losses_are_scenarios_in_the_sizing, test_zero_losses_are_in_the_cover_denominator). Four new student-error mutants of my own: n2 (cover_bps skips the negative-loss refusal) KILLED on all 50 seeds; n3 (leftover to highest id first) KILLED; n4 (margin layer pools every member's margin) KILLED; n1 (defaulter checked against margins only) SURVIVED 50/50 seeds ({O}new_mutants_seeds0-49.out). n1 violates project.html:201 and :210 (see proj-named-conditions).",
     "Kill n1: " + NEW_FIX),
 row("proj-large-cent-claim", "2.2-numbers, 2.6-tests", "course/modules/BK/BK4/grader/test_project.py:442-451", "PASS",
     "Recomputed in this round: loss 6585696953829388, funds 6692931089932558 and 585467024498971, D = their sum; residual times fund exceeds 2**53 (product 4.4078e31); floors 6055950114045319 and 529746839784068, leftover 1 to member 1, so 6055950114045320 and 529746839784068 as the test expects."),
 row("proj-mutant-float", "2.6-mutants, 2.2-money", "ledgers/BK4/mutants/vc10_float_arithmetic.py; course/modules/BK/BK4/grader/test_project.py:442-451", "PASS",
     "vc10_float_arithmetic.py KILLED by test_large_cent_shares_are_floored_in_integers (seed 0), mutate_seeds0-9_all48.out."),
 row("proj-mutant-argument", "2.6-mutants, 2.6-purity", "ledgers/BK4/mutants/r4f_sizing_sorts_caller_list_in_place.py; project.html:203; test_project.py", "PASS",
     "r4f KILLED by test_margin_for_cover_and_cover_bps_do_not_change_their_list_argument (seed 0), mutate_seeds0-9_all48.out."),
 row("proj-labs-simulated-stdlib", "2.6-simulated, 2.9-data", "tests/labs/BK4/lab-BK4-project-1..3.py; course/modules/BK/BK4/project.html:54", "PASS",
     "The three twins import only random (lab-BK4-project-1 line 7, -2 line 6, -3 line 8). Each docstring says the inputs are SIMULATED; run_labs PASS."),
 row("proj-page-smoke", "2.9-links, 2.10-browser", "course/modules/BK/BK4/project.html", "PASS",
     f"page_smoke.py --unit BK4 --pages project: PASS; in-browser grader 'All 85 tests pass on seed 738416653'; three labs under Pyodide ({O}page_smoke_project.out)."),
 row("proj-check-tools", "2.10-gates", "course/modules/BK/BK4/project.html", "PASS",
     f"check_pages.py --unit BK4: PASS; check_dag.py --unit BK4: PASS; check_projects.py --unit BK4: PASS ({O}check_pages.out, {O}check_dag.out, {O}check_projects.out)."),
 row("proj-ruff", "2.10-gates", "tests/labs/BK4; course/modules/BK/BK4/grader", "PASS",
     f"ruff check tests/labs/BK4 course/modules/BK/BK4/grader: All checks passed; ruff format --check: 12 files already formatted ({O}ruff_check_slice.out, {O}ruff_format_slice.out)."),
 row("proj-mypy-repo", "2.10-gates", "pyproject.toml [tool.mypy]", "PASS",
     f"mypy --no-incremental (repository): Success, no issues found in 385 source files ({O}mypy_repo.out)."),
 row("proj-pytest-labs", "2.10-gates", "tests/test_labs.py; tests/test_run_labs.py", "PASS",
     f"pytest -q tests/test_labs.py tests/test_run_labs.py -k labs: all passed ({O}pytest_labs_slice.out)."),
 row("proj-refs", "2.3-citations", "course/modules/BK/BK4/project.html:501-505 (reading list); references/references.json:7411 (duffie2011central), :2853 (bisndcpmi)", "PASS",
     f"verify_refs.py --offline: 560 entries, 0 problems ({O}verify_refs_offline_all.out). Both keys present. The page attributes no statement to either source. Live Crossref not run."),
 row("proj-banned-and-process-words", "2.9-prose", "course/modules/BK/BK4/project.html; grader/*.py; tests/labs/BK4/lab-BK4-project-*.py", "PASS",
     "Case-insensitive grep for BUILDER_RULES 1.3-1.4 banned strings and for process words (builder, verif, planner, architect, fixer, TODO, TBD, request, decision): no hit. 'round' hits are arithmetic ('rounded up'). '...' hits are type annotations (test_project.py:37, :1079)."),
 row("proj-anchors-links", "2.9-links", "course/modules/BK/BK4/project.html", "PASS",
     "Every href fragment in project.html (#grader-section, #report, #rubric-heading, #self-assessment, #spec, #stretch, #main) has a matching id; index.html#placement exists (id count 1)."),
 row("proj-dag-concepts", "2.14-DAG", "course/modules/BK/BK4/project.html", "PASS",
     "grep: project.html has no <dfn>, no data-concept and no class=\"concept\" link (count 0); check_dag.py --unit BK4: PASS."),
 row("proj-rung-ladder", "2.1-structure", "course/modules/BK/BK4/project.html:41-50 (ladder), :193-216 (spec), :490-497 (rung 4)", "PASS",
     "check_projects.py --unit BK4: PASS. Ladder rungs 1 to 4 in order; rung 4 (stretch) not graded; rung 2 is a completion lab."),
 row("proj-exemplar-a-calibration", "2.7-rubric-calibration", "course/modules/BK/BK4/project.html:424-453 (exemplar A), :408-417 (rubric)", "UNVERIFIABLE",
     "Not blind: this verifier read the annotations (project.html:442-449) before scoring. Scoring from the descriptors and the passage gives C1 2, C2 2, C3 1, C4 2, C5 2, which equals data-scores 2,2,1,2,2 (line 424). A blind calibration was not possible in this context.",
     "A fresh verifier that has not read the annotations scores exemplar A blind against the rubric (lines 408-417) and lands within one level on every criterion of the annotations."),
 row("proj-exemplar-b-numbers", "2.2-numbers, 2.7-rubric", "course/modules/BK/BK4/project.html:404 (memo rule), :422 and :457 (disclosure), :467 (5920 sentence)", "PASS",
     f"Round 5 FAIL is fixed: the disclosure at :422 and :457 now allows 'a difference of two printed numbers, as the memo rule above allows', and the memo rule at :404 permits a difference or ratio stated with its base. 5920 = 111074 - 105154 (both printed in Lab 3 Part B; {O}rederive_r6.out 'difference'), base 500 bps stated. 38.0 = 9500 x 40 / 10000 is computed from the instance inputs. 4000, 12000, 1333/1666/1000, 1334, 9250, 117088, 105154, 2 and 4 scenarios are printed by Lab 1 or Lab 3. Sums 1334+1666+1000 = 4000 and the 80000 total are checks on printed numbers."),
 row("proj-rubric-c3-descriptors", "2.7-rubric", "course/modules/BK/BK4/project.html:414", "PASS",
     "C3 level descriptors (4: pro rata and leftover rules with the sum that checks them; 3: the same without the sum; 2: one rule or survivor amounts; 1: no sharing rule) are observable as written."),
 row("proj-exemplar-b-calibration", "2.7-rubric-calibration", "course/modules/BK/BK4/project.html:455-481 (exemplar B), :457 (official scoring)", "UNVERIFIABLE",
     "Not blind: the annotations (project.html:471-479) were read before scoring. Scoring from the descriptors gives C1 4, C2 4, C3 4, C4 4, C5 4, which equals data-scores 4,4,4,4,4 (line 455). A blind calibration was not possible in this context.",
     "A fresh verifier that has not read the annotations scores exemplar B blind and lands within one level on every criterion."),
 row("proj-lab2-learner-text", "2.9-prose", "course/modules/BK/BK4/project.html:146-147, :186; tests/labs/BK4/lab-BK4-project-2.py:1-3", "PASS",
     "Learner text of Lab 2 contains no process word and no planning reference (grep, this round)."),
 row("proj-lab3-claim-checks-rules", "2.2-numbers, 2.9-prose", "course/modules/BK/BK4/project.html:253-366 (Lab 3 hypothesis and interpretation)", "PASS",
     f"Each Lab 3 claim checked against the twin output and {O}rederive_r6.out: five rows with conservation True; the 100000 row is the only uncovered row; sizing indices 36/38/39; margins 105154/111074/117088; covers at the margins and one cent below; brute force agrees; Part C lines for 9500 and 9000 only, as the hypothesis now says."),
 row("proj-notation-T", "2.13-notation", "course/modules/BK/BK4/project.html; notation/notation.json (symbols)", "PASS",
     "Registered symbols (T, Phi and Phi^-1, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q) and registered macros are not used in project.html (grep). Page symbols N, S, L, D, M, K, R, k, t, Lambda, i, IM_d, DF_d, DF_i, a1-a3, L_1, L_S are not registered and are defined on the page before use."),
 row("proj-failure-leak", "2.6-failure-messages", "course/modules/BK/BK4/grader/test_project.py; project.html:398-399", "PASS",
     "AST: all 85 tests carry __tracebackhide__ (recheck_r6.out). No failure message interpolates a computed answer (the two new round-6 tests name the idea only). Page command uses --assert=plain (project.html:398-399)."),
 row("proj-plan-conformance", "2.9-plan", "plans/BK4-build-plan.md:458, :437-446, :517, :743-748; plans/BK4-open-items.md; course/modules/BK/BK4/project.html:208; grader/test_project.py:723-733, :919-932", "FAIL",
     "Plan and open-items unchanged since the previous pin (git diff --quiet). (i) plan:517 requires monotonicity 'on each seed'; test_margin_is_non_decreasing_in_the_target (test_project.py:723-733) checks INST and INST2 only. (ii) plan:458 says the period convention is 'stated once'; project.html has no statement of it (grep 'period' finds only :469, 'close-out period'). (iii) plan:437-446 says the named conditions are the only conditions the grader requires an exception for; the page (:208) and test_project.py:919-932 also require cover_bps with empty losses, which the plan's table does not list. (iv) builder edits to plan lines 419, 478, 481, 515 have no Architect ruling (plan:740-748; open-items).",
     "Architect rules on (i) to (iv) and records each in the Architect decisions block. If (i) stands, extend the monotonicity test to seeds 0-49. If (ii) stands, add the period sentence to the conventions. If (iii) stands, amend plan 5.2. Revert any unratified plan edit."),
 row("proj-sizing-duplicate-losses", "2.6-tests, 2.2-numbers", "course/modules/BK/BK4/project.html:223; course/modules/BK/BK4/grader/test_project.py:670-682, :784-788", "PASS",
     "Recomputed: margin_for_cover([5,5,10,20], 5000) = 5 (k 2); margin_for_cover([5,5,5,9,12], 6000) = 5 (k 3); cover_bps([5,5,10,20], 5) = 5000. Tests assert these and reference passes."),
 row("proj-context-sentences", "2.6-spec", "course/modules/BK/BK4/project.html:196-197 (spec Context)", "PASS",
     "Context sentences describe the layer order implemented by reference.py. 'The autograder checks the cent results and the cover values, not the docstring or the imports' is true of test_project.py (no test reads a docstring or an import)."),
 row("proj-alternatives", "2.6-alternatives", "ledgers/BK4/alternatives/alt1_comprehensions.py .. alt5_bisection.py", "PASS",
     f"Re-run on the round-6 suite, seeds 0-49: alt1 to alt5 each 50/50 ({O}alternatives_seeds0-49.out). Byte-identical to the previous pin (git diff --quiet). With the candidate defaulter test, alt1 to alt5 each pass 50/50 (no over-constraint)."),
 row("proj-mypy-plan-command", "2.10-gates", "course/modules/BK/BK4/grader/test_project.py:28, :30", "PASS",
     f"mypy tests/labs/BK4 course/modules/BK/BK4/grader: Success, no issues found in 12 source files, exit 0 ({O}mypy_slice_plan_cmd.out)."),
 row("proj-survivor-leftover-order", "2.6-mutants, 2.6-spec", "ledgers/BK4/mutants/r4a_leftover_in_mapping_order.py; course/modules/BK/BK4/grader/test_project.py:421-429", "PASS",
     "r4a KILLED by test_leftover_cent_goes_to_the_lowest_id_when_the_dictionaries_list_members_out_of_order (seed 0), mutate_seeds0-9_all48.out."),
 row("proj-silence-named-refusals", "2.6-tests, 2.9-prose", "ledgers/BK4/mutants/r4g_debug_print_on_defaulter_refusal.py; r4h_debug_print_on_uncovered_loss.py; course/modules/BK/BK4/grader/test_project.py:994-1031", "PASS",
     "r4g KILLED by test_refused_inputs_print_nothing_before_they_raise (seed 0); r4h KILLED by test_the_module_prints_nothing_on_valid_inputs (seed 0)."),
 row("proj-refusal-count-docstring", "2.6-tests, 2.9-prose", "course/modules/BK/BK4/grader/test_project.py:~1010 (docstring of test_refused_inputs_print_nothing_before_they_raise)", "PASS",
     "Round 5 FAIL is fixed: the docstring now reads 'Each named refusal in the list below raises ValueError...' and carries no count; grep for 'thirteen' or 'fifteen' in test_project.py: none (recheck_r6.out)."),
 row("proj-remainder-spec", "2.6-spec", "course/modules/BK/BK4/project.html:248 (remainder fixture); course/modules/BK/BK4/grader/test_project.py:362-368", "PASS",
     "The page names defaulter 4 with no margin, fund or capital; remainder_case uses defaulter 4; values equal the page (see proj-fixture-tables)."),
 row("proj-rubric-c5-descriptor", "2.7-rubric", "course/modules/BK/BK4/project.html:416 (C5 level 3)", "PASS",
     "C5 level 3 reads 'states the direction in which each one biases the sized margin or the cover', which an observer can check."),
 row("proj-money-integer-claim", "2.9-prose, 2.2-numbers", "course/modules/BK/BK4/project.html:203, :224", "PASS",
     "Round 5 FAIL is fixed. project.html:224 now says the layers, margin and uncovered loss are exact integers, a survivor's share and a cover are exact fractions each floored to an integer, and the sizing index is an exact fraction rounded up. The false sentence 'the exact value of every output is an integer' is gone (grep count 0). Line 203 agrees ('no float appears'; shares and covers floored by integer division). Checked against rederive_r6.out (shares 4000/3 style fractions are floored)."),
 row("proj-zero-loss-sizing", "2.6-tests, 2.2-numbers, 2.6-mutants", "course/modules/BK/BK4/grader/test_project.py:685-692 (test_zero_losses_are_scenarios_in_the_sizing)", "PASS",
     "Round 5 FAIL is fixed: the test asserts margin_for_cover([0, 10, 20, 30], 5000) == 10. r5c_sizing_drops_zero_losses_before_counting.py now KILLED on seed 0 by this test (mutate_seeds0-9_all48.out). Reference passes."),
 row("proj-zero-loss-cover", "2.6-tests, 2.2-numbers, 2.6-mutants", "course/modules/BK/BK4/grader/test_project.py:800-806 (test_zero_losses_are_in_the_cover_denominator)", "PASS",
     "Round 5 FAIL is fixed: the test asserts cover_bps([0, 0, 5, 9], 0) == 5000. r5d_cover_denominator_excludes_zero_losses.py now KILLED on seed 0 by this test (mutate_seeds0-9_all48.out). Reference passes."),
]

fragment = {
    "unit": "BK4",
    "slice": "BK4-c",
    "round": 6,
    "verifier": "Claude Haiku 5.5, independent verifier for BK4-c (round 6); did not build BK4",
    "pin": pin,
    "base": "7376a5e2 (round-5 pin; previous fragment /Users/billyribeiro/.fanout/frags/E-BK4-c.round5.json, used as context; PASS rows were re-derived or re-run, none carried)",
    "checkout": str(root),
    "scratch": "/tmp/bk4c6_scripts, /tmp/bk4c6_ref, /tmp/bk4c6_fix, /tmp/bk4c6_starter, /tmp/bk4c6_n3 (not part of the ledger)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta 7376a5e..4bd8cb9 read in full for the slice: project.html (Constraints, Money, Grading mode, Lab 3 hypothesis and "
        "interpretation, exemplar B disclosure and passage), grader/test_project.py (two new zero-loss tests, one docstring). "
        "Whole files read: project.html (521 lines), grader/test_project.py (1102 lines), reference.py, instance.py, starter.py, "
        "the three project twins, alt1 to alt5 (carried byte-identical, re-run). New student-error mutants n1 to n4 written by the "
        "verifier (scripts/BK4-c-r6/make_r6_mutants.py). n1 SURVIVES: the page's named condition for a defaulter that is not a "
        "member is not tested when the defaulter is present in the margins only. Calibration rows stay UNVERIFIABLE because the "
        "annotations were read in this context. Not run: a live verify_refs (network); blind calibration; the hub site build "
        "(build_site, other slices)."
    ),
    "summary": "",
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
n_un = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
killed = sum(1 for m in mutants if m["killed_by"])
fragment["summary"] = (
    f"BK4-c round 6: verdict FAIL. {n_pass} PASS, {n_fail} FAIL, {n_un} UNVERIFIABLE of {len(rows)} rows. "
    f"Mutants: {killed}/{len(mutants)} killed on seeds 0-9 (survivor n1: defaulter present in margins only). "
    "Alternatives alt1 to alt5 and the reference pass 50/50 seeds; starter 0/50. Test count 85 = page 85."
)
path = root / "ledgers/BK4/BK4-c.json"
path.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", path, "rows", len(rows), "mutants", len(mutants), "killed", killed)
