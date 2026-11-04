"""Write the round-4 BK4-c ledger fragment from the verifier's rows and the mutation output.

Usage: write_fragment_r4.py <checkout_root> <fragment_out_path>. Mutant entries are parsed from
ledgers/BK4/scripts/BK4-c-r4/out/mutate_graders_final_r4.out (tools/mutate_graders.py, seeds 0-49).
"""

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
out_path = Path(sys.argv[2])
O = "ledgers/BK4/scripts/BK4-c-r4/out/"
PASS, FAIL = "PASS", "FAIL"


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> dict:
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != PASS:
        r["fix"] = fix
    return r


rows = [
    row("proj-lab1-numbers", "2.5-labs, 2.2-numbers",
        "course/modules/BK/BK4/project.html:56-139; tests/labs/BK4/lab-BK4-project-1.py", PASS,
        f"run_labs --unit BK4 --page project: 'run_labs BK4: PASS (3/3)' ({O}run_labs_project.out). Twin "
        f"`python -I -W error` exit 0, stderr 0 bytes, page code equals twin, page expected block equals twin stdout "
        f"({O}labs_page_vs_twin.out, script labs_page_vs_twin.py). Independent re-derivation "
        f"(rederive_r4.py, {O}rederive_r4.out): residual 4000, shares 1333/1666/1000, leftover to member 1, exact position "
        f"38.2, k 39, margin 117088, covers 9750 and 9500 (86 checks, 0 mismatches)."),
    row("proj-lab2-numbers", "2.5-labs, 2.2-numbers",
        "course/modules/BK/BK4/project.html:141-190; tests/labs/BK4/lab-BK4-project-2.py", PASS,
        f"run_labs project PASS (3/3, {O}run_labs_project.out) applies the completion rule. Page code differs from the "
        f"twin only at the two blanks (labs_page_vs_twin.out). Twin exit 0, stderr 0 bytes, expected equals stdout. "
        f"Completed expressions reproduce 1334/1666/1000 and k 39 (rederive_r4.out)."),
    row("proj-lab3-numbers", "2.5-labs, 2.2-numbers",
        "course/modules/BK/BK4/project.html:252-366; tests/labs/BK4/lab-BK4-project-3.py", PASS,
        f"Page code equals twin (labs_page_vs_twin.out); twin exit 0, stderr 0 bytes; expected equals stdout. "
        f"rederive_r4.out re-derives Part A rows (uncovered 12000 only at 100000; conservation True), Part B targets "
        f"9000/9500/9750 with k 36/38/39, margins 105154/111074/117088, covers at margin and one cent below, brute force "
        f"agreement, and Part C counts (past margin 2 and 4, past fund 2 and 2, past capital 0, past survivors 0)."),
    row("proj-fixture-tables", "2.4-mathematics, 2.6-tests",
        "course/modules/BK/BK4/project.html:229-250; course/modules/BK/BK4/grader/test_project.py:281-441", PASS,
        f"rederive_r4.out recomputes all 11 layer-order rows (project.html:234-244), the remainder rows (1, 2, 3, 4 cents), "
        f"sizing 8000->40, 8001->50, 10000->50, 5000 over four losses->20, and cover 3333 and 6666. Each matches the page and "
        f"the test expectations (test_project.py:281-355, 362-428). run_graders reference 50/50 ({O}run_graders.out)."),
    row("proj-named-conditions", "2.6-spec, 2.6-tests, 2.6-failure-messages",
        "course/modules/BK/BK4/project.html:203-212; course/modules/BK/BK4/grader/test_project.py:448-567", PASS,
        "Round-3 gap closed: test_defaulter_below_the_member_ids_is_refused (test_project.py:548-555, id 0), "
        "test_defaulter_inside_the_id_range_but_not_a_member_is_refused (558-567, id 3 between members 1, 2, 4), and "
        "test_defaulter_that_is_a_member_of_a_non_contiguous_set_is_accepted (570-578). Each named condition now has a refusal "
        "and an accept test on its boundary (project.html:205-210). r3f mutant KILLED at seed 0 (mutate_graders_final_r4.out). "
        "Reference passes all 81 (run_graders.out)."),
    row("proj-conventions-prose", "2.2-numbers, 2.9-prose",
        "course/modules/BK/BK4/project.html:217-226; course/modules/BK/BK4/grader/reference.py:1-109", PASS,
        "Layer order, survivor rule with D (project.html:220), leftover rule, conservation (221), cover floor (222) and "
        "k = ceil(t*S/10000) in integers (223) match reference.py:36-109 line by line and rederive_r4.out. "
        "`grep -n -o '\\bT\\b' project.html` finds no bare T (the page uses D for the pool, not T)."),
    row("proj-hours", "2.9-hours",
        "course/modules/BK/BK4/project.html:373-388 (table#hours); course/modules/BK/BK4/index.html:29", PASS,
        "Rows 2+2+3+3+2+2+1 = 15 (project.html:376-382). index.html:29 data-hours-lessons=35 and data-hours-project=15; 35+15=50; "
        "15/50 = 30 % as the page states (project.html:383). check_pages and check_projects PASS (check_pages.out, "
        "check_projects.out). Per the ruling, hours are checked only for arithmetic."),
    row("proj-grader-reference-run", "2.6-tests, 2.8-gate",
        "course/modules/BK/BK4/grader/reference.py; course/modules/BK/BK4/grader/test_project.py", PASS,
        f"run_graders --unit BK4 --seeds 0-49: 'run_graders BK4: PASS (reference 50/50 seeds, slowest 0.2 s)' ({O}run_graders.out, exit 0)."),
    row("proj-grader-starter-fails", "2.6-tests",
        "course/modules/BK/BK4/grader/starter.py; course/modules/BK/BK4/grader/test_project.py:1017-1040", PASS,
        f"Starter run on seeds 0-49 (run_candidates_r4.py, {O}starter_seeds0-49.out): FAIL on every seed, 77 failed and 4 "
        "passed (the 4 tests never call the module). Every failure is named by _named_when_unimplemented, not a traceback."),
    row("proj-collect-count", "2.6-tests",
        "course/modules/BK/BK4/project.html:214; course/modules/BK/BK4/grader/test_project.py", PASS,
        f"pytest --collect-only -q in a scratch copy: '81 tests collected' ({O}collect.out). project.html:214 states 'runs 81 checks'. Equal."),
    row("proj-instances", "2.6-instances, 2.2-numbers",
        "course/modules/BK/BK4/grader/instance.py:22-50", PASS,
        "instance.py read in full. rederive_r4.py checks the plan 5.5 validity rules on seeds 0-49 (ids 1..N, N 4-6, DF>=1, "
        "IM>=0, K>=0, defaulter a member, S 40-80, non-negative int losses, target in the set): 0 bad seeds. 50 distinct "
        "sizing answers, 49 of 49 differ from seed 0 (rederive_r4.out INFO lines; plan requires at least 40 and 3). "
        "SIMULATED label in make_instance docstring (instance.py:23, 42)."),
    row("proj-mutants-builder", "2.6-mutants",
        "ledgers/BK4/mutants/m01_fund_before_margin.py .. m10_seed0_hardcoded.py", PASS,
        f"mutate_graders --unit BK4 --seeds 0-49 ({O}mutate_graders_final_r4.out): all 10 builder mutants KILLED."),
    row("proj-mutants-own", "2.6-mutants",
        "ledgers/BK4/mutants/vc01_cover_rounded.py .. vc15_negative_capital_accepted.py (vc11 excluded, see proj-mutant-argument)", PASS,
        f"mutate_graders --seeds 0-49 ({O}mutate_graders_final_r4.out): all 14 verifier mutants vc01-vc10, vc12-vc15 KILLED."),
    row("proj-large-cent-claim", "2.2-numbers, 2.6-tests",
        "course/modules/BK/BK4/grader/test_project.py:431-440", PASS,
        "test docstring (line 432) says 'residual * fund exceeds 2**53'. rederive_r4.out: 2**53 = 9007199254740992; loss "
        "6585696953829388 and both funds are below 2**53; R*F1 and R*F2 both exceed it; floored share 6055950114045319 with "
        "the leftover cent giving 6055950114045320 and 529746839784068, matching the test (lines 435-437)."),
    row("proj-mutant-float", "2.6-mutants, 2.2-money",
        "ledgers/BK4/mutants/vc10_float_arithmetic.py; course/modules/BK/BK4/grader/test_project.py:431-441", PASS,
        f"vc10 KILLED at seed 0 by test_large_cent_shares_are_floored_in_integers ({O}mutate_graders_final_r4.out)."),
    row("proj-mutant-argument", "2.6-mutants, 2.6-purity",
        "ledgers/BK4/mutants/r4f_sizing_sorts_caller_list_in_place.py; course/modules/BK/BK4/project.html:214; "
        "course/modules/BK/BK4/grader/test_project.py:258-265, 703-711, 997-1009", FAIL,
        f"Mutant r4f (margin_for_cover sorts the caller's list in place) SURVIVES seeds 0-49 ({O}mutate_graders_final_r4.out; "
        f"run_candidates_r4 on the same file, {O}r4f_seeds0-49.out, PASS on all seeds). project.html:214 says the autograder "
        "checks 'the silence and purity of the module'. The suite checks argument immutability only for waterfall "
        "(test_waterfall_does_not_change_its_arguments, :258-265); margin_for_cover and cover_bps are not checked. "
        "starter.py:10 also says 'Nothing may ... change its arguments', so the rule is stated for all three functions. "
        "Round 3 ruled the same mutant out because only starter.py stated it; this round the page's own 'purity' claim is the "
        "statement.",
        "Add a test that margin_for_cover and cover_bps leave their list argument unchanged (a probe in fix_probes_r4.out "
        "kills r4f, and the reference passes all 84 probe tests). Alternatively, the Architect may rule that 'purity' on "
        "project.html:214 means determinism only, and then the mutant is unstated and must be removed from mutants/."),
    row("proj-labs-simulated-stdlib", "2.6-simulated, 2.9-data",
        "tests/labs/BK4/lab-BK4-project-1..3.py; course/modules/BK/BK4/project.html:54; grader/instance.py:1-7", PASS,
        "The three twins import only random (grep of import lines). project.html:54 states every amount is SIMULATED and no "
        "file is read. run_labs under python -I passes (run_labs_project.out)."),
    row("proj-page-smoke", "2.10-browser",
        "course/modules/BK/BK4/project.html", PASS,
        f"page_smoke --unit BK4 --pages project: PASS, 'All 81 tests pass on seed 959908116' in the in-browser grader ({O}page_smoke_project.out)."),
    row("proj-check-tools", "2.10-gates",
        "course/modules/BK/BK4/project.html", PASS,
        f"check_pages, check_dag and check_projects --unit BK4: all PASS ({O}check_pages.out, check_dag.out, check_projects.out)."),
    row("proj-ruff", "2.10-gates",
        "tests/labs/BK4; course/modules/BK/BK4/grader; repository", PASS,
        f"ruff check and ruff format --check on tests/labs/BK4 and grader: pass ({O}ruff_check.out, ruff_format.out). Repository "
        f"ruff check . 'All checks passed!' and ruff format --check . '553 files already formatted' ({O}ruff_repo.out, ruff_repo_format.out)."),
    row("proj-mypy-repo", "2.10-gates",
        "pyproject.toml [tool.mypy]", PASS,
        f"mypy --no-incremental (repository): 'Success: no issues found in 385 source files' ({O}mypy_repo.out)."),
    row("proj-pytest-labs", "2.10-gates",
        "tests/test_labs.py; tests/test_run_labs.py", PASS,
        f"pytest -q tests/test_labs.py tests/test_run_labs.py: exit 0 ({O}pytest_labs.out)."),
    row("proj-refs", "2.3-citations",
        "course/modules/BK/BK4/project.html reading list; references/references.json (duffie2011central, bisndcpmi)", PASS,
        f"verify_refs --unit BK4 (live): '2 of 560 entries, 0 problems' ({O}verify_refs_live.out). verify_refs --offline: "
        f"'560 entries, 0 problems' ({O}verify_refs_offline.out). The page attributes no statement to either source "
        "(project.html:501)."),
    row("proj-banned-and-process-words", "2.9-prose",
        "course/modules/BK/BK4/project.html; grader/*.py; tests/labs/BK4/lab-BK4-project-*.py", PASS,
        "check_pages BK4 PASS (banned strings). grep -i for verifier, builder, fixer, architect, TODO, draft, placeholder, "
        "lorem: no match in project.html, grader files or twins."),
    row("proj-anchors-links", "2.9-links",
        "course/modules/BK/BK4/project.html", PASS,
        "Internal targets exist: #spec, #report, #stretch, #self-assessment, #rubric-heading, #grader-section, #main (one id each). "
        "index.html#placement (index.html:71). L05.html, index.html, grader/instance.py, starter.py, test_project.py, "
        "../../../review.html (course/review.html) and the katex and css assets all exist."),
    row("proj-dag-concepts", "2.14-DAG",
        "course/modules/BK/BK4/project.html", PASS,
        "check_dag BK4 PASS. grep for data-concept, class=\"concept\" and <dfn in project.html: 0 matches. Terms such as order "
        "statistic and waterfall are plain prose."),
    row("proj-rung-ladder", "2.1-structure",
        "course/modules/BK/BK4/project.html:44-50 (ladder), :193-216 (spec), :490-497 (rung 4)", PASS,
        "Order rung 1 (Lab 1, line 56), rung 2 (completion lab, line 141), rung 3 (spec, line 196), rung 4 stretch, not graded "
        "(line 492). check_projects BK4 PASS."),
    row("proj-exemplar-a-calibration", "2.7-rubric-calibration",
        "course/modules/BK/BK4/project.html:424-453 (exemplar A), :408-417 (rubric)", FAIL,
        "Scored from the passage: C1 2, C2 2, C3 1, C4 2, C5 2, which agree with the official 2,2,1,2,2 within one level. "
        "The blind requirement (VERIFIER 2.6) is NOT met: this verifier read the official scoring line (project.html:426) "
        "before scoring, and the file has no separate passage-only view. Not blind, so not evidence of calibration.",
        "A verifier who has not read project.html:426 or :457 re-scores exemplar A and B from the passage and the rubric only, "
        "and this row is then re-graded. The page's data-reveal design is not what fails; the fail is the process gap in this round."),
    row("proj-exemplar-b-numbers", "2.2-numbers, 2.7-rubric",
        "course/modules/BK/BK4/project.html:455-481 (exemplar B)", PASS,
        "Every number checked against rederive_r4.out: 80000, 50000, 6000, 20000, 4000, 12000; 1334+1666+1000 = 4000; "
        "38.0 = 9500*40/10000 (computed); k 38; margin 111074 (Lab 3 Part B and C); cover 9500 and 9250 one cent below "
        "(Lab 3 Part B); 105154 and 117088; 5920 = 111074 - 105154 (computed difference, stated base 'on this set'); past "
        "margin 2 and 4 (Lab 3 Part C); past survivors 0 (Part C). The setting numbers are inputs in the lab code (allowed by project.html:422)."),
    row("proj-rubric-c3-descriptors", "2.7-rubric",
        "course/modules/BK/BK4/project.html:414", PASS,
        "C3 level 1 'Names no sharing rule.' and level 2 'Gives survivor amounts, or states one of the two rules' are observable. "
        "Exemplar A's C3 score (1) matches level 1."),
    row("proj-exemplar-b-calibration", "2.7-rubric-calibration",
        "course/modules/BK/BK4/project.html:455-481 (exemplar B), :457 (official scoring)", FAIL,
        "Scored from the passage: C1 4, C2 4, C3 4, C4 4, C5 4, which agree with the official 4,4,4,4,4. The blind requirement is "
        "NOT met for the same reason as proj-exemplar-a-calibration (official scoring at project.html:457 read before scoring).",
        "A blind re-scoring by a verifier who has not read project.html:457 (the same fix as proj-exemplar-a-calibration)."),
    row("proj-lab2-learner-text", "2.9-prose",
        "course/modules/BK/BK4/project.html:146-147, :186; tests/labs/BK4/lab-BK4-project-2.py:1-3", PASS,
        "The hypothesis names the blanks and the target outputs. The interpretation's tolerance sentence matches compare_output "
        "(tools/coursekit.py:321-333): numbers within 1e-6*(1+|expected|), other tokens exact. For the largest number in this "
        "lab (117088) the tolerance is 0.117 cent, so a wrong cent fails."),
    row("proj-lab3-claim-checks-rules", "2.2-numbers, 2.9-prose",
        "course/modules/BK/BK4/project.html:253-366 (Lab 3 hypothesis and interpretation)", PASS,
        "Each claim checked against rederive_r4.out and the twin output: conservation True in every row; only the 100000 row "
        "has an uncovered loss; three sizing indices 36, 38, 39; brute force equals the order statistic; Part C 9000 row: 4 "
        "past the margin, 2 past the fund, none past the capital or uncovered. 'The printed values describe this set of 40 "
        "scenarios only' holds (the set is one seeded set)."),
    row("proj-notation-T", "2.13-notation",
        "course/modules/BK/BK4/project.html; notation/notation.json (symbols)", PASS,
        "notation.json registers T (number of return observations), Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f and Q; "
        "project.html uses none of them (grep: no bare T, Q, Phi, gamma or R_f). The page's symbols S, L, t, k, D, DF_i, IM_d, K, R, "
        "a1 to a3, M, Lambda and L_s are not registered, and notation.json:about says such letters are defined in each lesson "
        "where used (project.html:219-223 defines them)."),
    row("proj-failure-leak", "2.6-failure-messages",
        "course/modules/BK/BK4/grader/test_project.py; project.html:399", PASS,
        "86 '__tracebackhide__ = True' lines (grep count). No print call in grader/*.py. Assertion and pytest.fail messages name "
        "the property or the input, never an expected value (read in full: test_project.py:107-157, 546-561, 570-601, 959-1040)."),
    row("proj-plan-conformance", "2.9-plan",
        "plans/BK4-build-plan.md:419, :441-445, :478-481, :515-517, :745-748; plans/BK4-open-items.md:1-30; "
        "course/modules/BK/BK4/project.html:196-212, :223, :414, :424, :455; grader/instance.py:39; grader/test_project.py:552-561, :633-641", FAIL,
        "The binding block (plan:748, '2026-11-03, binding ... Where the plan states a recommendation for an open question, "
        "follow it') is not met. Plan:745-746 still reads 'Pending. No decision has been taken for BK4'. The plan text was edited "
        "without a recorded Architect ruling (git show 67c47689:plans/BK4-build-plan.md:419 gives {9900, 9950, 9975}; current :419 "
        "gives {9000, 9500, 9750}; :478 replaces 'no procyclicality' with 'no change in margins in stress'; :481 swaps the two exemplar levels; :515 replaces 'on every seed' with the two cases INST and INST2; :517 still says 'on each seed', which the suite does not do). Open items: 'Architect may "
        "overrule any of these'. Remaining deviations from the binding plan: target set (page Inputs, instance.py:39); "
        "monotonicity 'on each seed' (plan:517) checked on INST and INST2 only (test_project.py:703-711); the exception table adds "
        "cover_bps with empty losses (project.html:208) beyond plan:441-445; plan 5.3 period convention appears nowhere on the page.",
        "The Architect records a ruling in the plan's Architect decisions block, or the builder restores the binding plan text "
        "and the page, instance.py and suite conform (or the Architect overrules item by item). Do not edit the plan text "
        "without the recorded ruling."),
    row("proj-sizing-duplicate-losses", "2.6-tests, 2.2-numbers",
        "course/modules/BK/BK4/project.html:223; course/modules/BK/BK4/grader/test_project.py:659-671, 773-777", PASS,
        f"Round-3 gap closed: test_repeated_losses_each_count_as_a_scenario_in_the_sizing ([5,5,10,20] at 5000 gives 5; "
        f"[5,5,5,9,12] at 6000 gives 5) and test_repeated_losses_each_count_in_the_cover ([5,5,10,20] at 5 gives 5000). "
        f"r3e (distinct-count sizing) and r3b (distinct-count cover) are KILLED at seed 0 ({O}mutate_graders_final_r4.out). "
        "Re-derived: 5000 of S=4 -> k=2 -> second smallest of all four = 5; distinct-count variant gives 10."),
    row("proj-context-sentences", "2.6-spec",
        "course/modules/BK/BK4/project.html:196-197 (spec Context)", PASS,
        "The Context dd has 4 sentences (split on sentence-final full stops). BUILDER_RULES.md:201 requires 2-4."),
    row("proj-alternatives", "2.6-alternatives",
        "ledgers/BK4/alternatives/alt1..alt5 (5 plan alternatives); course/modules/BK/BK4/grader/reference.py",
        PASS,
        f"run_candidates_r4.py on seeds 0-49 against the current test_project.py ({O}alternatives_seeds0-49.out): alt1 comprehensions, "
        "alt2 class-based, alt3 Fraction, alt4 integer two-pass and alt5 bisection all PASS every seed; reference PASS. The "
        "round-1 and round-2 alternative sets (BK4-c-r1, BK4-c-r2) were not re-run this round."),
    row("proj-mypy-plan-command", "2.10-gates",
        "course/modules/BK/BK4/grader/test_project.py:28, :30 (type-ignore comments)", PASS,
        f"mypy tests/labs/BK4 course/modules/BK/BK4/grader: 'Success: no issues found in 12 source files' ({O}mypy_plan.out)."),
    row("proj-survivor-leftover-order", "2.6-mutants, 2.6-spec",
        "ledgers/BK4/mutants/r4a_leftover_in_mapping_order.py; course/modules/BK/BK4/project.html:201, :220; "
        "course/modules/BK/BK4/grader/test_project.py (no fixture with a non-ascending dictionary)", FAIL,
        f"Mutant r4a (leftover cents follow the dictionary's order) SURVIVES seeds 0-49 ({O}mutate_graders_final_r4.out). The "
        f"page says the member ids are the keys of default_fund_cents (project.html:201) and that leftover cents go 'in ascending "
        f"id order' (:220). A valid call with dictionaries listed out of order distinguishes them: waterfall(1, 4, {{3:1,1:1,2:1,4:0}}, "
        f"same, 0) gives {{1:1,2:0,3:0}} in the reference and {{3:1,1:0,2:0}} in r4a ({O}probe_insertion_order.out). "
        "No grader input is out of order, so the suite cannot tell them apart.",
        "Add a test with the dictionaries in non-ascending insertion order. The proposed test "
        "(test_r4_survivor_order_is_by_id_not_by_dictionary_order) kills r4a and the reference passes (fix_probes_r4.out)."),
    row("proj-silence-named-refusals", "2.6-tests, 2.9-prose",
        "ledgers/BK4/mutants/r4g_debug_print_on_defaulter_refusal.py; ledgers/BK4/mutants/r4h_debug_print_on_uncovered_loss.py; "
        "course/modules/BK/BK4/project.html:203; test_project.py:971-978, 981-994", FAIL,
        f"project.html:203 says: 'On a valid input and on each named refused input, no function prints or warns.' The suite "
        f"checks silence on one valid call with no uncovered loss (:971-978) and on 5 of the 13 named refusals (:981-994). A debug "
        f"print in the defaulter refusal (r4g) and one in the uncovered branch (r4h) both SURVIVE seeds 0-49 "
        f"({O}mutate_graders_final_r4.out).",
        "Extend silence checks to every named refusal (defaulter not a member, each negative amount, empty cover, negative cover "
        "loss) and to a valid call with uncovered_cents > 0. The proposed test (fix_probes_r4.out) kills r4g and r4h, and the "
        "reference passes."),
    row("proj-remainder-spec", "2.6-spec",
        "course/modules/BK/BK4/project.html:248 (remainder fixture); course/modules/BK/BK4/grader/test_project.py:362-368", FAIL,
        "project.html:248 says 'The defaulter has no initial margin, no default fund and no capital' and 'The survivors are members "
        "1, 2 and 3' but never names the defaulter's id. The tests use defaulter 4 (test_project.py:362-368). A competent "
        "student would have to ask which id the defaulter is, and could pick member 1.",
        "Add to project.html:248: 'The defaulter is member 4.' (the fixture's own test uses 4)."),
    row("proj-rubric-c5-descriptor", "2.7-rubric",
        "course/modules/BK/BK4/project.html:416 (C5 level 3)", FAIL,
        "C5 level 3 reads 'Names three of the four limits, and states what each one does to the result.' 'States what each one "
        "does to the result' does not say what counts as a statement (direction, size, or a sentence), so two graders could "
        "score the same memo differently. Every other descriptor is observable.",
        "Replace with 'Names three of the four limits, and states the direction in which each one biases the sized margin or the cover.'"),
]

# Mutants, parsed from the final mutation run (seeds 0-49).
mutants = []
pattern = re.compile(r"^(KILLED|SURVIVED) (\S+): (.*?) -> (.*)$")
for line in (root / O / "mutate_graders_final_r4.out").read_text(encoding="utf-8").splitlines():
    m = pattern.match(line)
    if not m:
        continue
    status, name, description, killer = m.groups()
    killed_by = None if killer.strip() == "None" else killer.strip()
    mutants.append({
        "name": name.removesuffix(".py"),
        "file": f"ledgers/BK4/mutants/{name}",
        "description": description,
        "killed_by": killed_by,
    })

counts = {s: sum(1 for r in rows if r["status"] == s) for s in (PASS, FAIL)}
killed = sum(1 for m in mutants if m["killed_by"])
verdict = FAIL if counts[FAIL] or killed != len(mutants) else PASS
fragment = {
    "unit": "BK4",
    "slice": "BK4-c",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for BK4-c (round 4); did not build BK4",
    "pin": "9a02b1af9f92a060f7fabf7e1b3afb5ea95f45ba",
    "base": "67a2d13e (round-3 pin, E-BK4-c.round3.json). Delta 67a2d13e..9a02b1af read in full for this slice: "
            "project.html (lede, rungs paragraph, Lab 1 and Lab 2 interpretations, spec Context, Constraints, Grading mode, "
            "conventions for cover and sizing, Lab 3 hypothesis, exemplar B sizing paragraph), grader/test_project.py (+77 lines, "
            "7 new tests), plans/BK4-open-items.md (+54 lines, not a ruling). plans/BK4-build-plan.md and the labs are unchanged "
            "since 67a2d13e. No previous PASS row was carried: every row was re-run or re-derived this round.",
    "checkout": str(root),
    "scratch": "temporary directories under /tmp (bk4cand4.*, bk4fix4.*, bk4r4_*), all removed after use.",
    "verified_at": "2026-11-04T13:30:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Read in full this round: project.html (521 lines), grader/instance.py (50), reference.py (109), starter.py (47), "
        "test_project.py (1040 lines), the three project twins (70, 42, 98 lines), plans/BK4-build-plan.md section 5 and the "
        "Architect block, plans/BK4-open-items.md. The delta was read as hunks. Mutants: 38 in ledgers/BK4/mutants (30 earlier "
        "plus r4a to r4e, r4g, r4h); r4f is kept there because the page's 'purity' claim states the behaviour it violates. "
        "Calibration: not blind (see proj-exemplar-*). Not checked: the self-assessment form behaviour in a browser (only "
        "page_smoke console checks ran); the round-1 and round-2 alternative directories; Lesson 3 proof (other slice; only "
        "Definition 2.1 and Proposition 2.3 statement and sentences read by grep); hours beyond arithmetic (ruling)."
    ),
    "summary": (
        f"BK4-c round 4: verdict {verdict}. {counts[PASS]} PASS, {counts[FAIL]} FAIL of {len(rows)} rows. "
        f"Mutants: {killed}/{len(mutants)} killed on seeds 0-49 (survivors r4a, r4g, r4h, r4f; all four are FAIL rows). "
        f"Alternatives: 5/5 plan alternatives and the reference pass seeds 0-49. Reference: 50/50 seeds; collect 81 = page 81."
    ),
}
out_path.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out_path, "verdict", verdict, counts, f"mutants {killed}/{len(mutants)}")
