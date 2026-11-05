"""Round-11 (BK4-c, verifier E11): writes ledgers/BK4/BK4-c.json from the outputs of the scripts in this folder.

Usage: python -I build_fragment_r11.py <repo_root>   (stdlib only). The mutant list is parsed from out/mutate_graders_bk4.out.
"""

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

root = Path(sys.argv[1])
S = "ledgers/BK4/scripts/BK4-c-r11"
O = f"{S}/out"
PAGE = "course/modules/BK/BK4/project.html"


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r


R = []
A = R.append
A(row("proj-lab1-numbers", "2.5 lab", f"{PAGE}:56-139; tests/labs/BK4/lab-BK4-project-1.py", "PASS",
      f"run_labs BK4 PASS (8/8) ({O}/run_labs_bk4.out). {S}/lab_twin_check_r11.py: page code equals twin, twin exit 0 under "
      f"python -I -W error with 0 stderr bytes, stdout equals the expected block ({O}/lab_twin_check.out). "
      f"{S}/rederive_r11.py (own re-derivation from the page rules, {O}/rederive.out): layers 50000/6000/20000, residual 4000, "
      "shares floor 1333/1666/1000 (sum 3999), leftover 1 to member 1, k 39, margin 117088, cover 9750 and 9500 one cent below."))
A(row("proj-lab2-numbers", "2.5 lab", f"{PAGE}:141-190; tests/labs/BK4/lab-BK4-project-2.py", "PASS",
      f"lab_twin_check_r11.py reports page_code_equals_twin=False for Lab 2 only because the two blanks differ: the unified diff "
      f"in {O}/lab_twin_check.out changes exactly the share line and the index line, each to '___'. Every other page line equals "
      "the twin line, which is the completion convention (FINAL-ARCHITECT-RULINGS 11). The completed twin's stdout equals the "
      "expected block (expected_equals_output=True). course/assets/js/labs.js:42-51 compares tokens with |a-b| <= tol*(1+|b|); "
      "at 1e-6 the largest printed value 117088 gives 0.117 cent, under one cent, so a wrong cent fails."))
A(row("proj-lab3-numbers", "2.5 lab", f"{PAGE}:252-366; tests/labs/BK4/lab-BK4-project-3.py", "PASS",
      f"lab_twin_check_r11.py: page code equals twin, expected equals output. {S}/rederive_r11.py: Part A rows 20000/55000/70000/"
      "80000/100000 (uncovered 12000 only at 100000, conservation True); Part B (k, margin, cover, cover one cent below) = "
      "(36,105154,9000,8750), (38,111074,9500,9250), (39,117088,9750,9500) with brute force agreeing; Part C past counts "
      f"(2,2,0,0) at 9500 and (4,2,0,0) at 9000; largest loss 118151 ({O}/rederive.out)."))
A(row("proj-fixture-tables", "2.4 math", f"{PAGE}:229-250; grader/test_project.py (fixture tests)", "PASS",
      f"{S}/rederive_r11.py: all 11 layer-order rows of the page table (losses 80..300) match; remainder fixture 1/2/4 cents "
      f"match; sizing 8000->40, 8001->50, 10000->50, four-loss 5000->20; covers 3333 and 6666 ({O}/rederive.out). "
      f"{S}/fixtures_extra_r11.py: repeated, zero and large-cent fixtures (leftover 1 to member 1) match ({O}/fixtures_extra.out)."))
A(row("proj-named-conditions", "2.9 structure", f"{PAGE}:201-212; grader/test_project.py:459-1059, :1021-1059", "PASS",
      "The six named conditions of the spec (page :205-210) each have a must_refuse test and an accepted-side must_accept test "
      "(margin empty, target 0/1/10000/10001, negative loss in both functions, cover empty, waterfall negatives, defaulter "
      "not a member above/below/between). No must_refuse call is made for an unnamed condition (read of every call site)."))
A(row("proj-conventions-prose", "2.4 math", f"{PAGE}:219-224; grader/reference.py:57-109", "PASS",
      "Layer formulas (page :219) equal reference.py:57-60; survivor rule (:220) equals reference.py:62-80; cover (:222) equals "
      "reference.py:108-109; sizing index (:223) equals reference.py:99; money (:224) integer. Re-derived by rederive_r11.py."))
A(row("proj-hours", "2.9 hours", f"{PAGE}:34, :36, :373-386 (table#hours); course/modules/BK/BK4/index.html:39-42, :160-174", "PASS",
      f"{S}/rederive_r11.py: component hours 2+2+3+3+2+2+1 = 15; eyebrow and data-hours-project 15. Hub: 5 lessons x 7 h = 35; "
      "35+15 = 50; 15/50 = 30 % (index.html:42 and the hours table). Independent estimate (rung 1 and 2 labs 1.5-2 h each, "
      "waterfall with fixtures 2.5-3 h, sizing and cover 2.5-3 h, edge cases and suite 2-3 h, memo 2-2.5 h, self-assessment "
      "1 h) gives 13.5-16.5 h, within 30 % of 15."))
A(row("proj-grader-reference-run", "2.6 autograder", "course/modules/BK/BK4/grader/reference.py; grader/test_project.py", "PASS",
      f"run_graders BK4: PASS (reference 50/50 seeds) ({O}/run_graders_bk4.out). Local run of the browser flags on the reference "
      "in a scratch copy, QF_SEED=0: '86 passed' (pytest -q -p no:cacheprovider --assert=plain -W error)."))
A(row("proj-grader-starter-fails", "2.6 autograder", "course/modules/BK/BK4/grader/starter.py; grader/test_project.py", "PASS",
      "Starter copied to clearing_house.py in a scratch copy with the updated suite, QF_SEED=3: '82 failed, 4 passed'; the 82 "
      "failure lines each read 'has no implementation for <name>' (grep count 82). The 4 passes touch no student function."))
A(row("proj-collect-count", "2.6 autograder", f"{PAGE}:214; grader/test_project.py", "PASS",
      f"pytest --collect-only -q on the scratch copy: '86 tests collected' ({O}/collect_only.out); grep -c '^def test_' = 86; "
      "page :214 says 86 checks."))
A(row("proj-instances", "2.6 autograder", "course/modules/BK/BK4/grader/instance.py:22-50", "PASS",
      f"{S}/instance_sample_r11.py over seeds 0-19 ({O}/instance_sample.out): all valid (N 4-6, ids 1..N, funds >= 1 cent, "
      "S 40-80, target in {9000,9500,9750}); 20 distinct sizing margins and 20 distinct loss sets. Materiality across seeds "
      "0-49 is tested by test_seeded_cases_give_different_margins_across_seeds."))
A(row("proj-mutants-builder", "2.6 mutation", "ledgers/BK4/mutants/m01..m10", "PASS",
      f"tools/mutate_graders.py --unit BK4 --seeds 0-9: PASS (71/71 killed) ({O}/mutate_graders_bk4.out). m01..m10 KILLED."))
A(row("proj-mutants-own", "2.6 mutation", "ledgers/BK4/mutants/n1..n4, r3a..r5f", "PASS",
      "Same run: n1..n4 and r3a..r5f all KILLED (see the mutants list of this fragment)."))
A(row("proj-mutants-round7", "2.6 mutation", "ledgers/BK4/mutants/s01..s05", "PASS", "Same run: s01..s05 KILLED."))
A(row("proj-mutants-round8", "2.6 mutation", "ledgers/BK4/mutants/t8a..t8e", "PASS", "Same run: t8a..t8e KILLED."))
A(row("proj-mutants-round9", "2.6 mutation", "ledgers/BK4/mutants/v9a..v9e", "PASS", "Same run: v9a..v9e KILLED."))
A(row("proj-mutants-round10", "2.6 mutation", "ledgers/BK4/mutants/x10a..x10d", "PASS",
      "Same run: x10a..x10d KILLED (x10a by test_layers_and_survivor_payments_add_to_the_loss_on_every_scenario, x10b by "
      "test_two_of_three_scenarios_covered_is_floored_not_rounded, x10c by test_survivor_keys_are_the_members_other_than_the_defaulter, "
      "x10d by the conservation test)."))
A(row("proj-mutants-round11", "2.6 mutation", "ledgers/BK4/mutants/y11a..y11d (written by scripts/BK4-c-r11/make_r11_mutants.py)",
      "PASS", "Four new verifier mutants, each one edit of reference.py with the student error in the first docstring line: "
      "y11a residual forgets the capital (conservation test), y11b cover divides before multiplying (one-of-three cover test), "
      "y11c survivors pro-rated past the pool (oracle test), y11d unknown defaulter treated as zero exposure (named refusal test). All KILLED in the same run."))
A(row("proj-large-cent-claim", "2.6 mutation", f"{PAGE}; grader/test_project.py (test_large_cent_shares_are_floored_in_integers)", "PASS",
      f"The test passes on the reference (run_graders PASS); vc10 (float arithmetic) is KILLED by it in {O}/mutate_graders_bk4.out. "
      f"{S}/fixtures_extra_r11.py re-derives the large-cent shares (6055950114045320, 529746839784068) with the leftover cent."))
A(row("proj-mutant-float", "2.6 mutation", "ledgers/BK4/mutants/vc10_float_arithmetic.py", "PASS",
      "vc10 KILLED by test_large_cent_shares_are_floored_in_integers (mutate output)."))
A(row("proj-mutant-argument", "2.6 mutation", "ledgers/BK4/mutants/r4f_sizing_sorts_caller_list_in_place.py; grader/test_project.py", "PASS",
      "r4f KILLED by test_margin_for_cover_and_cover_bps_do_not_change_their_list_argument (mutate output); t8e KILLED by the waterfall purity test."))
A(row("proj-labs-simulated-stdlib", "2.5 lab", "tests/labs/BK4/lab-BK4-project-1..3.py; project.html:54, :56-58, :141-146, :252-258", "PASS",
      "grep of import lines: each lab twin imports only random. Each states SIMULATED inputs; no file is read (project.html:54)."))
A(row("proj-page-smoke", "2.9 structure", PAGE, "PASS",
      f"tools/page_smoke.py --unit BK4 --pages project: PASS, labs 0.0 s each, in-browser grader 'All 86 tests pass' ({O}/page_smoke_bk4_project.out)."))
A(row("proj-check-tools", "2.6 autograder", PAGE, "PASS",
      f"check_projects BK4: PASS ({O}/check_projects_bk4.out); check_pages --all: all units PASS ({O}/check_pages_all.out)."))
A(row("proj-ruff", "2.6 autograder", "tests/labs/BK4; course/modules/BK/BK4/grader; ledgers/BK4", "PASS",
      f"ruff check: 'All checks passed!'; ruff format --check: '12 files already formatted' ({O}/ruff_check.out, ruff_format.out)."))
A(row("proj-mypy-repo", "2.6 autograder", "pyproject.toml [tool.mypy]", "PASS",
      f"mypy --no-incremental: 'Success: no issues found in 385 source files' ({O}/mypy_repo.out)."))
A(row("proj-mypy-plan-command", "2.6 autograder", "course/modules/BK/BK4/grader/test_project.py:28, :30", "PASS",
      f"run_graders BK4 PASS includes the strict typecheck of reference.py, instance.py and starter.py ({O}/run_graders_bk4.out)."))
A(row("proj-pytest-labs", "2.5 lab", "tests/test_labs.py; tests/test_run_labs.py", "PASS",
      f"pytest -q tests/test_labs.py tests/test_run_labs.py: all dots, exit 0 ({O}/pytest_labs.out)."))
A(row("proj-refs", "2.1 citations", f"{PAGE} reading list (data-cite duffie2011central, bisndcpmi); references/references.json", "PASS",
      f"verify_refs.py --unit BK4 (live): '3 of 560 entries, 0 problems' ({O}/verify_refs_live_bk4.out, exit 0). "
      f"verify_refs.py --offline (whole registry): 560 entries, 0 problems ({O}/verify_refs_offline_all.out). "
      f"Anchors and data-cite keys: ANCHORS_REFS PASS ({O}/anchors_refs_r11.out, run from ledgers/BK4/scripts/BK4-c-r10/anchors_refs_r10.py). "
      "The page attributes no statement to either source."))
A(row("proj-banned-and-process-words", "2.9 structure", f"{PAGE}; grader/*.py; tests/labs/BK4/lab-BK4-project-*.py", "PASS",
      "grep (case-insensitive) for BUILDER_RULES 1.3-1.4 strings and for process words (round, verifier, builder, fixer, ruling, "
      "architect, plan, TODO, TBD, lorem, for brevity, beyond the scope, obviously, clearly, studies show): no hits in project.html. "
      "Only '...' hits are Python type annotations."))
A(row("proj-anchors-links", "2.9 structure", PAGE, "PASS", f"ANCHORS_REFS PASS, 26 hrefs, 0 unresolved anchors or files ({O}/anchors_refs_r11.out)."))
A(row("proj-dag-concepts", "2.9 DAG", PAGE, "PASS",
      f"check_dag --all: PASS ({O}/check_dag_all.out). 'order statistic', 'novation' and 'pro rata' appear as prose only; grep of "
      "curriculum/*.yaml finds no concept with those names, so no out-of-closure concept is linked or defined."))
A(row("proj-rung-ladder", "2.6 structure", f"{PAGE}:41-50, :193-216, :490-497", "PASS",
      "Four rungs in order: worked example (Lab 1, annotated), completion (Lab 2, data-run plus expected), independent project "
      "(spec, grader, memo), stretch (not graded). check_projects BK4 PASS."))
A(row("proj-exemplar-a-calibration", "2.6 rubric", f"{PAGE} exemplar-a (data-level 2)", "PASS",
      f"Blind scoring from memo prose only ({O}/exemplar_memo_text_r11.out, extracted by {S}/exemplar_memo_text_r11.py, no "
      "annotation or official scoring included): C1 2, C2 2, C3 1, C4 2, C5 2. Official data-scores 2,2,1,2,2: equal on every "
      "criterion. Disclosure: this verifier had read the full page, annotations included, before the blind extraction, so the "
      "separation is imperfect; the score was taken from the prose text only."))
A(row("proj-exemplar-b-calibration", "2.6 rubric", f"{PAGE} exemplar-b (data-level 4)", "PASS",
      f"Blind from memo prose ({O}/exemplar_memo_text_r11.out): C1 4 (four layers in order, cents for the 80000 scenario, the "
      "waits statement), C2 4 (9500 bps, k 38, 38th smallest, cover at margin and one cent below), C3 4 (pro rata and leftover, "
      "sum 4000), C4 4 (one margin with cover, 0 past survivors and 0 uncovered, one alternative), C5 4 (four limits, direction for "
      "each, no B or C claim). Official 4,4,4,4,4: equal. Same disclosure as exemplar A."))
A(row("proj-exemplar-b-numbers", "2.2 numbers", f"{PAGE}:456-478", "PASS",
      f"{S}/rederive_r11.py: 38.0 = 9500*40/10000; 111074-105154 = 5920; 9500-9000 = 500; cover one cent below 111074 is 9250; "
      "margin 105154 leaves 4 past; margin 111074 leaves 2 past; 0 past capital and survivors; 1334+1666+1000 = 4000; inputs "
      "30000/50000/40000/20000 and 4000/6000/5000/3000 and capital 20000 match the Lab 1 MARGIN, FUND and CAPITAL lines."))
A(row("proj-rubric-c1-levels", "2.6 rubric", f"{PAGE}:412 (C1 row)", "PASS",
      f"{S}/rubric_enum_r11.py: C1 32 valid feature combinations, 0 gaps, 0 overlaps (unchanged wording this round)."))
A(row("proj-rubric-c2-levels", "2.6 rubric", f"{PAGE}:413 (C2 row)", "PASS",
      f"{S}/rubric_enum_r11.py: C2 51 valid feature combinations, 0 gaps, 0 overlaps under the round-11 wording. The round-10 gaps "
      "(a rule-only sizing memo with the cover checked at the margin and no one-cent check) now match level 3, whose margin cell "
      "accepts 'its value, or the sizing rule that gives it'."))
A(row("proj-rubric-c3-descriptors", "2.6 rubric", f"{PAGE}:414 (C3 row)", "PASS",
      f"{S}/rubric_enum_r11.py: C3 24 valid feature combinations, 0 gaps, 0 overlaps. The round-10 gap (a memo naming another sharing "
      "rule, 'shares equally') now matches level 2 by its 'names a sharing rule other than pro rata or leftover' clause."))
A(row("proj-rubric-c4-descriptors", "2.6 rubric", f"{PAGE}:415 (C4 row)", "PASS",
      f"{S}/rubric_enum_r11.py: C4 10 valid feature combinations, 0 gaps, 0 overlaps. The round-10 gap (two recommended margins) now "
      "matches level 2 by 'recommends more than one margin (a fallback margin counts as a second recommendation)'."))
A(row("proj-rubric-c5-descriptor", "2.6 rubric", f"{PAGE}:416 (C5 row); :478 (exemplar B limits)", "PASS",
      f"{S}/rubric_enum_r11.py: C5 17 valid feature combinations, 0 gaps, 0 overlaps. The round-10 defect (a stated 'no known direction' "
      "not counted as a direction) is closed by the level-3 clause '(a statement that the direction is not known counts as stating it)'."))
A(row("proj-rubric-observable-wording", "2.6 rubric", f"{PAGE}:408-416", "PASS",
      "Each cell read against the observable test: the verbs (names, states, gives, checks, recommends, compares) denote visible "
      "content of the memo. The fallback-margin and not-known-direction clauses resolve the two boundary readings."))
A(row("proj-exemplar-annotations-agree", "2.6 rubric", f"{PAGE}:425-478 (aside.annotation)", "PASS",
      "Exemplar A annotations: C1 meets 2, C2 meets 2 and misses 3, C3 meets 1, C4 meets 2, C5 meets 2 (data-scores 2,2,1,2,2). "
      "Exemplar B: all meets 4 (data-scores 4,4,4,4,4). Both agree with the blind scores within one level."))
A(row("proj-rubric-self-form", "2.6 rubric", f"{PAGE}:484-488; course/assets/js/rubric.js:8, :87, :97, :219", "PASS",
      "section#self-assessment data-rubric='rubric' and data-exemplars='exemplar-a exemplar-b' reference existing ids (table#rubric, "
      "article#exemplar-a, article#exemplar-b). rubric.js stores the record through store.js (kv, key rubric:<storeKey>), so the "
      "claim 'Your scores stay in this browser' holds in the code."))
A(row("proj-lab2-learner-text", "2.5 lab", f"{PAGE}:146-147, :186; tests/labs/BK4/lab-BK4-project-2.py", "PASS",
      "The 'token by token' and 1e-6 tolerance claim matches course/assets/js/labs.js:42-51 (compareOutput, |a-b| <= tol*(1+|b|)). "
      "The completed twin's output equals the expected block."))
A(row("proj-lab3-claim-checks-rules", "2.5 lab", f"{PAGE}:253-366 (Lab 3 hypothesis and interpretation)", "PASS",
      f"Each sentence checked against {O}/rederive.out and {O}/lab_twin_check.out: Part A True columns; Part B indices 36, 38, 39; "
      "brute-force agreement; Part C counts (2,2,0,0) and (4,2,0,0); 'the only row with an uncovered loss' is 100000."))
A(row("proj-notation-T", "2.4 notation", f"{PAGE}; notation/notation.json", "PASS",
      "notation.json registers T, Phi/Phi^-1, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q (8 entries, read in full). The page uses none of "
      "them with its registered meaning. Its symbols (R residual, D pool, K capital, L loss, S, M, t, k, Lambda, DF_i, IM_d, DF_d, "
      "a1-a3, L_s) are unregistered local letters, not any registered entry."))
A(row("proj-failure-leak", "2.6 autograder", "course/modules/BK/BK4/grader/test_project.py (all asserts and helpers)", "PASS",
      f"Read in full. Round-11 grep of assert comparisons for literal expected values (regex over ==, !=, <, >, in followed by a literal) "
      "returns none that is an expected answer; the five literal asserts of round 10 (lines 687, 691, 701, 809, 816) now compare a "
      "named variable (want_four, want_five, want, want). Remaining literals are rule thresholds (4<=N<=6, 40<=S<=80) and empty strings."))
A(row("proj-grader-docstring-named-variables", "2.6 autograder", "course/modules/BK/BK4/grader/test_project.py:9-14 (docstring) and the asserts", "PASS",
      "The module docstring now says each expected result is held in a named variable. The grep above finds no assert with a literal "
      "expected value (round-10 finding closed). The refactor was read as a diff: every replaced literal keeps its value (for example "
      "want = {1: 1, 2: 0, 3: 0} and want_names equal to the old set)."))
A(row("proj-sizing-duplicate-losses", "2.4 math", f"{PAGE}:223; grader/test_project.py (test_repeated_losses_*)", "PASS",
      f"{S}/fixtures_extra_r11.py: [5,5,10,20] at 5000 gives 5; [5,5,5,9,12] at 6000 gives 5; cover [5,5,10,20] at 5 gives 5000 ({O}/fixtures_extra.out)."))
A(row("proj-context-sentences", "2.9 structure", f"{PAGE}:197 (spec Context); grader/reference.py", "PASS",
      "Content check: the context is scoped to 'In this model' and matches the reference waterfall order. Its length is a separate row "
      "(proj-spec-context-length)."))
A(row("proj-spec-context-length", "2.9 structure", f"{PAGE}:197 (dd of dt 'Context' in the spec)", "FAIL",
      f"{S}/build_fragment_r11.py output: the Context dd splits into 5 sentences: (1) 'In this model, a clearing house novates ...'; (2) "
      "'When a member defaults, ...'; (3) 'You write the simulator ...'; (4) 'One default is simulated at a time ...'; (5) 'The autograder "
      "checks the cent results and the cover values, not the docstring or the imports.' BUILDER_RULES.md section 5.2 requires the spec "
      "Context to be in 2-4 sentences.",
      fix="Edit project.html line 197 so the Context dd has at most four sentences: merge sentence (4) into (3) or (5), or delete "
          "(4) (its content is repeated in the Constraints row). Then re-run check_projects BK4 and page_smoke for project."))
A(row("proj-alternatives", "2.6 autograder", "ledgers/BK4/alternatives/alt1..alt5; scripts/BK4-c-r11/alt6_candidate_scan.py", "PASS",
      f"{S}/run_alts_r11.py: alt1..alt5 each 50/50 seeds 0-49, ALTERNATIVES PASS ({O}/alternatives.out). New verifier alternative "
      f"alt6 (sizing by a scan over distinct losses with an integer cover test, different validation order): 50/50, ALT6 PASS "
      "(run by run_alt6_r11.py)."))
A(row("proj-survivor-leftover-order", "2.6 autograder", "grader/test_project.py:411-429; ledgers/BK4/mutants/r4a_*", "PASS",
      "r4a KILLED by test_leftover_cent_goes_to_the_lowest_id_when_the_dictionaries_list_members_out_of_order; s01 and n3 killed too."))
A(row("proj-silence-named-refusals", "2.6 autograder", "grader/test_project.py:1010-1059; mutants r4g, r4h", "PASS",
      "test_the_module_prints_nothing_on_valid_inputs and test_refused_inputs_print_nothing_before_they_raise pass on the reference; "
      "r4g and r4h KILLED."))
A(row("proj-refusal-count-docstring", "2.6 autograder", "grader/test_project.py:1021-1022", "PASS",
      "The docstring says each named refusal in the list raises ValueError; the list has 15 entries, each a named condition or a "
      "named input of one (read in full)."))
A(row("proj-remainder-spec", "2.4 math", f"{PAGE}:248; grader/test_project.py:362-388; grader/reference.py:74-80", "PASS",
      f"Remainder fixture 1, 2, 3, 4 cents: {S}/rederive_r11.py and {S}/fixtures_extra_r11.py match; the leftover rule equals "
      "reference.py:74-80 (ascending id, DF > 0)."))
A(row("proj-money-integer-claim", "2.4 math", f"{PAGE}:203, :224; grader/test_project.py (test_waterfall_returns_plain_int_money, checked_int)", "PASS",
      "'every computation is integer arithmetic' matches reference.py (// and min/max only, no float); the int checks are in the suite."))
A(row("proj-zero-loss-sizing", "2.6 mutation", "grader/test_project.py (test_zero_losses_are_scenarios_in_the_sizing); ledgers/BK4/mutants/r5c_*", "PASS",
      "test_zero_losses_are_scenarios_in_the_sizing passes on reference; r5c KILLED by it."))
A(row("proj-zero-loss-cover", "2.6 mutation", "grader/test_project.py (test_zero_losses_are_in_the_cover_denominator); ledgers/BK4/mutants/r5d_*", "PASS",
      "Passes on reference; r5d KILLED by it."))
A(row("proj-round7-prose-delta", "2.9 structure", f"{PAGE} delta 00a84795..11d7077a (hunks at :43, :54, :138, :413-416)", "PASS",
      "Every hunk read: :54 floored definition 'floored (rounded down to a whole number)' is correct; :135 the conservation check text "
      f"matches the printed lines in Lab 1 ({O}/run_labs_bk4.out); :413-416 rubric cells, enumerated above; the grader test-file delta "
      "keeps every literal value (diff read)."))
A(row("proj-local-run", "2.6 autograder", f"{PAGE}:397-399", "PASS",
      "The local command QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py gives '86 passed' on "
      "the reference (QF_SEED=0, scratch copy) and '82 failed, 4 passed' on the starter (QF_SEED=3)."))
A(row("proj-spec-signatures", "2.6 autograder", f"{PAGE}:201; grader/starter.py:29-47", "PASS",
      "Starter names, signatures and the Waterfall fields match the page and reference.py."))
A(row("proj-spec-inputs-instance", "2.6 autograder", f"{PAGE}:199; grader/instance.py", "PASS",
      f"Ranges on :199 (N 4-6; funds >= 1 cent; 40-80 losses; targets 9000/9500/9750) match instance.py; {O}/instance_sample.out."))
A(row("proj-l03-crossref", "2.9 DAG", f"{PAGE}:223; course/modules/BK/BK4/L03.html:133-134, :151, :164", "PASS",
      "Read in this round: L03 Definition 2.1 (margin cover level) at :133-134 defines the scenario set and cover; Proposition 2.3 (the "
      "sized margin is an order statistic) at :151 and its proof Part 3 at :164. The page cites Lesson 3 for these, correctly."))
A(row("proj-placement-claim", "2.9 structure", f"{PAGE}:43; course/modules/BK/BK4/index.html:69-71, :150", "PASS",
      "The placement quiz (#placement, data-mastery 0.8) has eight questions, two of them skill checks on rungs 1 and 2; "
      "index.html:150 says a student must reach the placement bar and answer both skill checks to skip rungs 1 and 2. Matches the page."))
A(row("proj-grade-scale-citation", "2.3 grades", f"{PAGE}:420 (rubric paragraph); course/modules/BK/BK4/L01.html:40-46", "PASS",
      "L01 grade legend: B 'published, not settled'; C 'working paper, practitioner research or single sample'. The page's gloss matches."))
A(row("proj-autograder-claims", "2.9 structure", f"{PAGE}:389-392 (grader section), :520 (footer); course/assets/js/grader.js:3, :33, :53, :61; course/assets/js/store.js:122-136", "PASS",
      "'Your code is saved in this browser as you type': grader.js:61 debounces store.put of the draft (400 ms). 'seeded by your workspace ID': "
      "grader.js:3, :53 and store.js:134-136 (FNV-1a of workspace id and unit). 'Nothing you write leaves it': page_smoke reports no external "
      "requests (round-11 run PASS)."))

mutants = []
for line in (root / O / "mutate_graders_bk4.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED (\S+\.py): (.*) -> (\S+) \(seed \d+\)$", line)
    if m:
        mutants.append({"id": m.group(1)[:-3], "description": m.group(2), "killed_by": m.group(3)})
assert len(mutants) == 71, len(mutants)

counts = {s: sum(1 for r in R if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag = {
    "unit": "BK4",
    "slice": "BK4-c",
    "round": 11,
    "verifier": "Claude Haiku 5.5, independent verifier E11 for BK4-c (round 11); did not build BK4",
    "pin": "11d7077a290f7960b183d3a5a6631af4773888f9 (HEAD of claude/fanout-b3 at verification; detached checkout)",
    "base": "00a84795f276456fce19d4181373cc4efba11a36 (round-10 pin; /Users/billyribeiro/.fanout/frags/E-BK4-c.round10.json used as context; every non-PASS row re-verified; every row whose subject changed re-verified)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE11-BK4-c",
    "scratch": "/tmp/bk4r11_coll (collect), /tmp/bk4r11_starter, /tmp/bk4r11_local (scratch copies); the scripts that back rows are under ledgers/BK4/scripts/BK4-c-r11/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if counts["FAIL"] or counts["UNVERIFIABLE"] else "PASS",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta 00a84795..11d7077a for the slice: project.html (6 changed lines: the floored gloss, the conservation sentence in the Lab 1 "
        "interpretation, rubric C2 L3, C3 L2, C4 L2, C5 L3), grader/test_project.py (refactor of literal expected values to named variables "
        "and a docstring sentence; values unchanged), and mutants x10a..x10d (added in round 10). grader/reference.py, starter.py, instance.py, "
        "tests/labs/BK4 and ledgers/BK4/alternatives are byte-identical to the round-10 pin. Round-10 FAILs: the four rubric rows and the "
        "docstring row are re-verified PASS by the round-11 enumeration and grep. Exemplar scoring: this verifier read the full page, annotations "
        "included, before the blind extraction (exemplar_memo_text_r11.py), so the blind separation is imperfect; the scores come from the prose only. "
        "Lab 2 twin check: the twin differs from the page only at the two blanks (ruling 11). The verify_refs call without --unit is the offline "
        "whole-registry run (the --unit option is live-only in this tool). Not checked: a visual render (no figures on this page); a Pyodide "
        "session beyond page_smoke's in-browser grader run; the Lesson 3 proof text (another slice); the full text of duffie2011central and "
        "bisndcpmi (the page makes no claim from them); whether the four named limits are the complete set of simulator limits (read as the set the "
        "rubric names)."
    ),
    "summary": (
        f"BK4-c round 11: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE of {len(R)} rows; "
        f"mutants {len(mutants)}/{len(mutants)} killed (71 listed by tools/mutate_graders.py --unit BK4 --seeds 0-9, including four new "
        "verifier mutants y11a..y11d); five builder alternatives and one verifier alternative pass 50/50 seeds 0-49; reference 50/50; collect 86; "
        "rubric enumeration 0 gaps and 0 overlaps for C1-C5; FAIL: proj-spec-context-length (spec Context has 5 sentences, BUILDER_RULES 5.2 allows 2-4)."
    ),
}
out = root / "ledgers/BK4/BK4-c.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out.relative_to(root), counts, "mutants", len(mutants))
