"""Round-10 fragment builder for BK4-c (writes ledgers/BK4/BK4-c.json). Rows and verdicts are the verifier's own
judgements; this script only assembles the JSON and parses the mutation output for the mutants list.
Usage: python make_fragment_r10.py <repo_root>"""

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
O = "ledgers/BK4/scripts/BK4-c-r10/out"
mut_out = (root / O / "mutate_graders_bk4_full.out").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mut_out:
    m = re.match(r"(KILLED|SURVIVED) (\S+?)\.py: (.*) -> (.*)$", line)
    if m:
        name, desc, killed = m.group(2), m.group(3), m.group(4)
        mutants.append({
            "name": name,
            "description": desc,
            "killed_by": killed if m.group(1) == "KILLED" else None,
        })

P = "PASS"
F = "FAIL"
R = []


def row(rid, check, location, status, evidence, fix=None):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        d["fix"] = fix
    R.append(d)


row("proj-lab1-numbers", "2.5 lab", "course/modules/BK/BK4/project.html:56-139; tests/labs/BK4/lab-BK4-project-1.py", P,
    f"run_labs --unit BK4: 'run_labs BK4: PASS (8/8)' ({O}/run_labs_bk4.out). lab_twin_check_r10.py: page code equals twin, "
    f"twin exit 0 under python -I -W error with 0 stderr bytes, stdout equals expected block ({O}/lab_twin_check_r10.out). "
    f"rederive_r10.py re-derives layers 50000/6000/20000, residual 4000, shares 1333/1666/1000 + 1 leftover, k=39, margin 117088, "
    f"cover 9750 at it and 9500 one cent below ({O}/rederive_r10.out).")
row("proj-lab2-numbers", "2.5 lab", "course/modules/BK/BK4/project.html:141-190; tests/labs/BK4/lab-BK4-project-2.py", P,
    f"lab_twin_check_r10.py: the page differs from the twin only at the two blanks (share line and index line, each '___'; "
    f"unified diff in {O}/lab_twin_check_r10.out); the twin output equals the expected block. Blank expressions equal Lab 1 lines. "
    f"course/assets/js/labs.js:42-51 compares tokens with |a-b| <= tol*(1+|b|); at tol 1e-6 the largest printed value 117088 gives 0.117, under one cent.")
row("proj-lab3-numbers", "2.5 lab", "course/modules/BK/BK4/project.html:252-366; tests/labs/BK4/lab-BK4-project-3.py", P,
    f"lab_twin_check_r10.py: page code equals twin, expected equals output. rederive_r10.py: Part A rows (20000/55000/70000/80000/100000, uncovered 12000 only at 100000); "
    f"Part B (k, margin, cover, cover-below) = (36,105154,9000,8750), (38,111074,9500,9250), (39,117088,9750,9500); brute force agrees; "
    f"Part C past-counts (2,2,0,0) at 9500 and (4,2,0,0) at 9000. Largest loss 118151.")
row("proj-fixture-tables", "2.4 math", "course/modules/BK/BK4/project.html:229-250; grader/test_project.py:162-368", P,
    "rederive_r10.py: all 11 layer-order rows (losses 80..300) match, incl. 300 -> survivors 40/60, uncovered 20; remainder 1/2/3/4 cents "
    "-> {1:1}, {1:1,2:1}, {1,1,1}, {1,1,1}+uncovered 1; sizing 8000->40, 8001->50, 10000->50, four-loss 5000->20; covers 3333, 6666 (20000//3).")
row("proj-named-conditions", "2.9 structure", "course/modules/BK/BK4/project.html:201, :203-212; grader/test_project.py:459-1059", P,
    "The six named conditions (page :205-210) each have a must_refuse test and an accepted-side must_accept test (test_project.py:459-566, :867-961, refusal list :1024-1055). "
    "must_refuse is called only for named conditions (grep of call sites; the defaulter tests use the page's 'not one of the member ids' condition, and the member ids are the keys of default_fund_cents per page :201).")
row("proj-conventions-prose", "2.4 math", "course/modules/BK/BK4/project.html:219-224; grader/reference.py:57-80, :91-109", P,
    "Layer formulas a1,a2,a3,R (page :219) equal reference.py:57-60; survivor rule (:220) equals reference.py:62-80; cover (:222) equals reference.py:108-109; "
    "sizing index (:223) equals reference.py:99 (-((-t*S)//10000)); money (:224) integer. Verified by reading and by rederive_r10.py.")
row("proj-hours", "2.9 hours", "course/modules/BK/BK4/project.html:34, :36, :373-386 (table#hours); course/modules/BK/BK4/index.html:39-42, :160-174", P,
    "Component hours 2+2+3+3+2+2+1 = 15 (rederive_r10.py 'hours sum' OK); eyebrow and data-hours-project=15. Hub: five lessons x 7 h (data-hours=7 in L01-L05) = 35; 35+15 = 50; 15/50 = 30 % (index.html:42). "
    "Independent estimate: rung 1 and 2 labs 1.5-2 h each, waterfall with fixtures 2.5-3 h, sizing and cover 2.5-3 h, edge cases and suite 2-3 h, memo 2-2.5 h, self-assessment 1 h: 13.5 to 16.5 h, within 30 % of 15.")
row("proj-grader-reference-run", "2.6 autograder", "course/modules/BK/BK4/grader/reference.py; grader/test_project.py", P,
    f"run_graders --unit BK4 --seeds 0-49: 'run_graders BK4: PASS (reference 50/50 seeds, slowest ...)' ({O}/run_graders_bk4.out); "
    "local pytest of reference in a scratch copy with QF_SEED=0: '86 passed'.")
row("proj-grader-starter-fails", "2.6 autograder", "course/modules/BK/BK4/grader/starter.py; grader/test_project.py:1091-1114", P,
    "Starter run in scratch (QF_SEED=3): 82 failed, 4 passed (the 4 passes are tests that touch no student function: frozen-dataclass shape, seeded-case validity). "
    "All 82 failure lines read 'has no implementation for <name>' (15 cover_bps, 25 margin_for_cover, 42 waterfall); run_graders reports no 'starter passes' problem.")
row("proj-collect-count", "2.6 autograder", "course/modules/BK/BK4/project.html:214; grader/test_project.py", P,
    "pytest --collect-only -q on the reference scratch copy: '86 tests collected'; page :214 says 86 checks, warnings as errors (-W error in the page's flags).")
row("proj-instances", "2.6 autograder", "course/modules/BK/BK4/grader/instance.py:22-50", P,
    "instance_sample_r10.py over seeds 0-19: all valid (N 4-6, ids 1..N, funds >= 1 cent, S 40-80, target in {9000,9500,9750}, three designed regions); 20 distinct sizing margins, 20 distinct loss sets. Output in " + O + "/instance_sample_r10.out.")
row("proj-mutants-builder", "2.6 mutation", "ledgers/BK4/mutants/m01..m10", P,
    f"tools/mutate_graders.py --unit BK4 --seeds 0-9: 67/67 killed ({O}/mutate_graders_bk4_full.out). The ten builder mutants are KILLED in that output.")
row("proj-mutants-own", "2.6 mutation", "ledgers/BK4/mutants/n1..n4, r3a..r4h", P,
    f"Same run: all listed mutants KILLED (see the mutants array of this fragment).")
row("proj-mutants-round7", "2.6 mutation", "ledgers/BK4/mutants/s01..s05", P, f"Same run: s01..s05 KILLED.")
row("proj-mutants-round8", "2.6 mutation", "ledgers/BK4/mutants/t8a..t8e", P, f"Same run: t8a..t8e KILLED.")
row("proj-mutants-round9", "2.6 mutation", "ledgers/BK4/mutants/v9a..v9e", P, f"Same run: v9a..v9e KILLED.")
row("proj-mutants-round10", "2.6 mutation", "ledgers/BK4/mutants/x10a..x10d (written by ledgers/BK4/scripts/BK4-c-r10/make_r10_mutants.py)", P,
    "Four new student-error mutants, each one exact edit of the reference: x10a pool from survivors' margins (killed by test_layers_and_survivor_payments_add_to_the_loss_on_every_scenario), "
    "x10b cover counts strictly below (killed by test_two_of_three_scenarios_covered_is_floored_not_rounded), x10c defaulter listed among survivors (killed by test_survivor_keys_are_the_members_other_than_the_defaulter), "
    "x10d uncovered ignores the CCP capital (killed by test_layers_and_survivor_payments_add_to_the_loss_on_every_scenario). All four KILLED in " + O + "/mutate_graders_bk4_full.out.")
row("proj-large-cent-claim", "2.6 autograder", "course/modules/BK/BK4/grader/test_project.py:442-451", P,
    "test_large_cent_shares_are_floored_in_integers passes on reference; vc10 float mutant KILLED by it (mutate output line).")
row("proj-mutant-float", "2.6 mutation", "ledgers/BK4/mutants/vc10_float_arithmetic.py; grader/test_project.py:442-451", P,
    "vc10 KILLED by test_large_cent_shares_are_floored_in_integers (" + O + "/mutate_graders_bk4_full.out).")
row("proj-mutant-argument", "2.6 mutation", "ledgers/BK4/mutants/r4f_sizing_sorts_caller_list_in_place.py; grader/test_project.py:1062-1068", P,
    "r4f KILLED by test_margin_for_cover_and_cover_bps_do_not_change_their_list_argument.")
row("proj-labs-simulated-stdlib", "2.5 labs", "tests/labs/BK4/lab-BK4-project-1..3.py; course/modules/BK/BK4/project.html:54, :56-58, :141-146, :252-258", P,
    "The three lab twins import only 'random' (grep of import lines); each states SIMULATED inputs; no file is read (project.html:54).")
row("proj-page-smoke", "2.9 smoke", "course/modules/BK/BK4/project.html", P,
    f"page_smoke.py --unit BK4 --pages project: 'page_smoke modules/BK/BK4/project.html: PASS'; labs 0.0 s each; in-browser grader 'All 86 tests pass' ({O}/page_smoke_bk4_project.out).")
row("proj-check-tools", "2.9 structure", "course/modules/BK/BK4/project.html", P,
    f"check_projects.py --unit BK4: PASS; check_pages.py --all: 'check_pages BK4: PASS' ({O}/check_pages_all.out).")
row("proj-ruff", "gate", "tests/labs/BK4; course/modules/BK/BK4/grader; ledgers/BK4", P,
    f"ruff check: 'All checks passed!'; ruff format --check: '12 files already formatted' ({O}/ruff_check.out, ruff_format.out).")
row("proj-mypy-repo", "gate", "pyproject.toml [tool.mypy]", P,
    f"mypy --no-incremental: 'Success: no issues found in 385 source files' ({O}/mypy_repo.out).")
row("proj-mypy-plan-command", "gate", "course/modules/BK/BK4/grader/test_project.py:28, :30", P,
    "run_graders typecheck (mypy --strict on reference.py, instance.py, starter.py) emitted no FAIL line in the PASS run ("
    + O + "/run_graders_bk4.out).")
row("proj-pytest-labs", "gate", "tests/test_labs.py; tests/test_run_labs.py", P,
    f"pytest -q tests/test_labs.py tests/test_run_labs.py: all dots, exit 0 ({O}/pytest_labs.out).")
row("proj-refs", "2.1 citations", "course/modules/BK/BK4/project.html:501-506; references/references.json", P,
    f"anchors_refs_r10.py: data-cite keys duffie2011central and bisndcpmi exist in references.json entries. verify_refs.py --unit BK4 (live): '2 of 560 entries, 0 problems' ({O}/verify_refs_live_bk4.out). "
    f"verify_refs.py --offline (whole registry): '560 entries, 0 problems' ({O}/verify_refs_offline_all.out). The page attributes no statement to either source.")
row("proj-banned-and-process-words", "2.9 prose", "course/modules/BK/BK4/project.html; grader/*.py; tests/labs/BK4/lab-BK4-project-*.py", P,
    "grep of BUILDER_RULES 1.3 strings (TODO, TBD, lorem, for brevity, beyond the scope, studies show, obviously, clearly, roughly, historically, it can be shown, ellipsis): no prose hits; "
    "the only '...' hits are Python type annotations (test_project.py:37, :1091). Process words (builder, verifier, planner, agent): none.")
row("proj-anchors-links", "2.9 structure", "course/modules/BK/BK4/project.html", P,
    f"anchors_refs_r10.py: 26 hrefs, 0 unresolved anchors or files ({O}/anchors_refs_r10.out).")
row("proj-dag-concepts", "2.9 DAG", "course/modules/BK/BK4/project.html", P,
    f"check_dag.py --all: 'check_dag BK4: PASS' ({O}/check_dag_all.out). The page links Lesson 1, Lesson 3, Lesson 5 (lesson-nav, :514-517) and the hub; no concept link is added in this round.")
row("proj-rung-ladder", "2.6 ladder", "course/modules/BK/BK4/project.html:41-50, :193-216, :490-497", P,
    "Four rungs in order (worked example, completion, independent project, stretch); rung 1 annotated (Lab 1); rung 2 graded instantly (Lab 2 data-run plus expected); rung 3 spec; rung 4 not graded. check_projects BK4: PASS.")
row("proj-exemplar-a-calibration", "2.6 rubric calibration", "course/modules/BK/BK4/project.html:424-453 (exemplar A), :408-417 (rubric)", P,
    "Blind scoring from memo prose only (ledgers/BK4/scripts/BK4-c-r10/blind_memo_text_r10.py output): C1 2 (four layers named in order, no scenario cents), C2 2 (rule with target, no value of k, no cover check), "
    "C3 1 (no rule named, no amounts), C4 2 (margin with no cover, no alternative), C5 2 (two limits). Blind 2,2,1,2,2 equals official 2,2,1,2,2 (page :427). Caveat: I read the page, annotations included, before this blind pass.")
row("proj-exemplar-b-calibration", "2.6 rubric calibration", "course/modules/BK/BK4/project.html:455-481 (exemplar B), :457 (official scoring)", P,
    "Blind from memo prose: C1 4 (layers in order, cents for 80000 scenario, waits rule), C2 4 (bps target, k 38, 38th smallest, cover at margin and one cent below), C3 4 (pro rata and leftover rules, sum 4000), "
    "C4 4 (one margin with cover, zero past survivors and uncovered, one alternative), C5 4 (four limits, directions stated, no B/C claim, no source). Blind 4,4,4,4,4 equals official 4,4,4,4,4 (page :458). "
    "The C5 level 4 depends on reading 'no known direction' (page :470) as a stated direction; see proj-rubric-c5-descriptor.")
row("proj-exemplar-b-numbers", "2.2 numbers", "course/modules/BK/BK4/project.html:457-469", P,
    f"rederive_r10.py: 38.0 = 9500*40/10000; 111074-105154 = 5920; 9500-9000 = 500; 9250 one cent below 111074; 9000 margin 105154 leaves 4 past; 9500 margin leaves 2 past; 0 past capital and survivors; 1334+1666+1000=4000; "
    f"inputs 30000/50000/40000/20000, 4000/6000/5000/3000, 20000 and 12000 pool match the lab code; SIMULATED label present ({O}/rederive_r10.out).")
row("proj-rubric-c1-levels", "2.6 rubric", "course/modules/BK/BK4/project.html:412 (C1 row, data-criterion C1)", P,
    "rubric_enum_r10.py (ledgers/BK4/scripts/BK4-c-r10/rubric_enum_r10.py, output out/rubric_enum_r10.out): 32 valid feature combinations of the C1 descriptors, 0 gaps, 0 overlaps. "
    "Round-9 gap (two or three layers with scenario cents) is closed by the 'Names two or three of the layers' cell.")
row("proj-rubric-c2-levels", "2.6 rubric", "course/modules/BK/BK4/project.html:413 (C2 row, data-criterion C2)", F,
    "rubric_enum_r10.py: 99 valid combinations, 7 gaps, 0 overlaps. Realistic memo matching no level: 'Target 9500 bps; k = 38; the margin is the 38th smallest loss; the cover at that margin is 9500 bps.' "
    "Features T, Tb, K, P, C1c, S true; M (a numeric margin) and C2c (one cent below) false. L4 needs C2c, L3 needs 'the margin' as a value (M), L2 needs no k or no cover check; no level applies. "
    "(The 'the margin' in the L3 cell is a numeric value under a strict reading; a rule alone matches only L2, whose trailing condition fails.)",
    "In the L3 cell replace 'States the target, the value of k and the margin' with 'States the target, the value of k, and the margin (its value, or the sizing rule that gives it)'. "
    "Then the memo above is L3, and no combination in the enumeration is left without a level.")
row("proj-rubric-c3-descriptors", "2.6 rubric", "course/modules/BK/BK4/project.html:414 (C3 row, data-criterion C3)", F,
    "rubric_enum_r10.py: 24 valid combinations, 3 gaps, 0 overlaps. Realistic memo matching no level: 'The survivors share the residual equally, so each pays one third.' "
    "It names a sharing rule (O true) that is neither pro rata nor leftover; L1 requires 'Names no sharing rule', L2 requires amounts with no rule or exactly one of pro rata and leftover. No level applies, with or without survivor amounts.",
    "In the L2 cell (:414) add: 'or names a sharing rule other than pro rata or leftover, with or without survivor amounts'.")
row("proj-rubric-c4-descriptors", "2.6 rubric", "course/modules/BK/BK4/project.html:415 (C4 row, data-criterion C4)", F,
    "rubric_enum_r10.py: 10 valid combinations, 1 gap (two or more margins recommended). The round-9 gap (one margin with cover and no alternative) is closed by the L2 cell. "
    "Memo: 'I recommend 111074 cents (9500 bps) and, as a fallback, 105154 cents (9000 bps), both with their covers.' It matches no level: L1 needs no margin, L2 needs a margin with no cover or one margin with no alternative, L3/L4 need one margin.",
    "In the L2 cell (:415) add: 'or recommends more than one margin'.")
row("proj-rubric-observable-wording", "2.6 rubric", "course/modules/BK/BK4/project.html:412-416", P,
    "Each cell read against the observable test. Vague-word hits checked: none beyond the specific gaps recorded in the C2-C5 rows (see those). Words such as 'names', 'states', 'gives', 'checks' name visible content.")
row("proj-rubric-c5-descriptor", "2.6 rubric", "course/modules/BK/BK4/project.html:416 (C5 row); :470 (exemplar B limits)", F,
    "rubric_enum_r10.py: 20 valid combinations, 0 gaps, 0 overlaps under the reading that 'states the direction' is satisfied by a direction for each named limit. "
    "Observability defect: exemplar B's fixed-set sentence (page :470) gives 'its error on the sized margin has no known direction'. The L4 and L3 cells demand 'states the direction in which each one biases'. "
    "A strict reader counts that sentence as no direction, so exemplar B scores L2 on C5 (it names four limits, and direction is missing for one), against the official 4. The cells do not say whether 'no known direction' counts.",
    "In the L4 and L3 cells of C5 (:416) add: 'a statement that the direction is not known counts as stating it'. Alternatively re-word page :470 to state a direction (for example, 'the error is two-sided').")
row("proj-exemplar-annotations-agree", "2.6 rubric", "course/modules/BK/BK4/project.html:424-481 (aside.annotation)", P,
    "Exemplar A annotations: C1 meets 2, C2 meets 2 and misses 3, C3 meets 1, C4 meets 2, C5 meets 2 (equal data-scores 2,2,1,2,2). Exemplar B annotations: all meets 4 (equal data-scores 4,4,4,4,4).")
row("proj-rubric-self-form", "2.6 rubric", "course/modules/BK/BK4/project.html:484-488", P,
    "section#self-assessment data-rubric='rubric' and data-exemplars='exemplar-a exemplar-b' reference existing ids (table#rubric :408, article#exemplar-a :425, article#exemplar-b :456).")
row("proj-lab2-learner-text", "2.5 lab", "course/modules/BK/BK4/project.html:146-147, :186; tests/labs/BK4/lab-BK4-project-2.py", P,
    "The 'token by token' and 1e-6 tolerance claim matches course/assets/js/labs.js:42-51 (|a-b| <= tol*(1+|b|)); the largest printed number 117088 gives 0.117, under one cent. The line 'a wrong cent fails' holds (difference 1 > 0.117).")
row("proj-lab3-claim-checks-rules", "2.5 lab", "course/modules/BK/BK4/project.html:253-366 (Lab 3 hypothesis and interpretation)", P,
    "Each hypothesis and interpretation sentence checked against the printed output (" + O + "/rederive_r10.out and lab_twin_check_r10.out): Part A True columns, Part B 36/38/39 indices, brute force agreement, Part C counts.")
row("proj-notation-T", "2.4 notation", "course/modules/BK/BK4/project.html; notation/notation.json", P,
    "notation.json symbols: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q. The page uses no symbol with a registered meaning (grep: N, S, L, D, R, K, M, k, t, Lambda, DF_i, IM_d, DF_d, a1-a3, L_s). Bare R is not registered (R_f and R^* are).")
row("proj-failure-leak", "2.6 autograder", "course/modules/BK/BK4/grader/test_project.py (all tests and helpers)", P,
    "Failure text read in the whole file: messages name the property, never the expected value. Under the page's flags (-q --assert=plain -W error, no --tb) pytest hides the test frames (__tracebackhide__), so the literal expected values in five asserts are not shown "
    "(broken-cover demo in scratch /tmp/bk4r10_leak: failure lines show only the message). The docstring claim is a separate row (proj-grader-docstring-named-variables).")
row("proj-grader-docstring-named-variables", "2.6 autograder", "course/modules/BK/BK4/grader/test_project.py:9-14 (docstring), :687, :691, :701, :809, :816", F,
    "The module docstring says 'each expected value is held in a named variable, so a failing line shows the name and not the value'. Five asserts compare with literals: "
    "line 687 'got_four == 5', 691 'got_five == 5', 701 'got == 10', 809 and 816 'got == 5_000'. Under the page's flags the literal is not printed (frames hidden), so no answer leaks; the docstring is still false for these tests (grep 'assert .*== <literal>').",
    "Hold each literal in a named variable (for example 'want = 5_000'; 'assert got == want') in those five tests, or correct the docstring at lines 12-14. Severity low.")
row("proj-sizing-duplicate-losses", "2.4 math", "course/modules/BK/BK4/project.html:223; grader/test_project.py:682-694", P,
    "test_repeated_losses_each_count_as_a_scenario_in_the_sizing: [5,5,10,20] at 5000 gives 5 (k=2); [5,5,5,9,12] at 6000 gives 5 (k=3); both match the order statistic over all S losses (rederive by hand and oracle).")
row("proj-context-sentences", "2.9 prose", "course/modules/BK/BK4/project.html:197; grader/reference.py", P,
    "Context sentence scoped 'In this model' and matches reference waterfall order. No external factual claim without a key.")
row("proj-alternatives", "2.6 autograder", "ledgers/BK4/alternatives/alt1..alt5", P,
    f"run_alts_r10.py: each of five alternatives passes 50/50 seeds 0-49 ({O}/alternatives_r10.out): comprehensions, class-based, Fraction, integer two-pass, bisection.")
row("proj-survivor-leftover-order", "2.6 autograder", "course/modules/BK/BK4/grader/test_project.py:411-429; ledgers/BK4/mutants/r4a_leftover_in_mapping_order.py", P,
    "r4a KILLED by test_leftover_cent_goes_to_the_lowest_id_when_the_dictionaries_list_members_out_of_order (mutate output).")
row("proj-silence-named-refusals", "2.6 autograder", "course/modules/BK/BK4/grader/test_project.py:1010-1059; mutants r4g, r4h", P,
    "test_the_module_prints_nothing_on_valid_inputs and test_refused_inputs_print_nothing_before_they_raise pass on reference; r4g and r4h KILLED.")
row("proj-refusal-count-docstring", "2.6 autograder", "course/modules/BK/BK4/grader/test_project.py:1021-1022", P,
    "Docstring 'Each named refusal in the list below raises ValueError' matches the list (15 entries, each a named condition or a named input of one).")
row("proj-remainder-spec", "2.4 math", "course/modules/BK/BK4/project.html:248; grader/test_project.py:362-368, :371-388; grader/reference.py:74-80", P,
    "Remainder fixture (1, 2, 3, 4 cents) equals rederive_r10.out; the leftover rule matches reference.py:74-80 (ascending id, DF>0).")
row("proj-money-integer-claim", "2.4 math", "course/modules/BK/BK4/project.html:203, :224; grader/test_project.py:128-132, :186-194", P,
    "'every computation is integer arithmetic' matches reference.py (no float, // only); test_waterfall_returns_plain_int_money and checked_int enforce int outputs.")
row("proj-zero-loss-sizing", "2.6 mutation", "course/modules/BK/BK4/grader/test_project.py:697-703; ledgers/BK4/mutants/r5c_*", P,
    "r5c KILLED by test_zero_losses_are_scenarios_in_the_sizing.")
row("proj-zero-loss-cover", "2.6 mutation", "course/modules/BK/BK4/grader/test_project.py:812-816; ledgers/BK4/mutants/r5d_*", P,
    "r5d KILLED by test_zero_losses_are_in_the_cover_denominator.")
row("proj-round7-prose-delta", "2.9 structure", "course/modules/BK/BK4/project.html (delta c93dd526..00a84795: hunks at :54, :412-416, :420, :442-446, :468, :470, :478)", P,
    "Every hunk of project.html in the round delta read: :54 scenario sentence (Lesson 3 cross-reference; 'scenario set' defined at L03:134); :412-416 rubric cells (rows C1-C5, see rows above); :420 grade scale, equal to L01:40-46; "
    ":442-446 and :478 annotations; :468 the added '9500 bps' cover sentence (verified by Lab 3 Part B); :470 limits sentence (directions verified by logic: one default raises losses, a close-out raises losses, stress margin moves).")
row("proj-local-run", "2.6 autograder", "course/modules/BK/BK4/project.html:397-399", P,
    "The local command QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py reproduces: 86 passed on reference (scratch copy, QF_SEED=0).")
row("proj-spec-signatures", "2.9 structure", "course/modules/BK/BK4/grader/starter.py:29-47; course/modules/BK/BK4/project.html:201", P,
    "Starter names and signatures match the page (waterfall, margin_for_cover, cover_bps, Waterfall fields) and reference.py.")
row("proj-spec-inputs-instance", "2.6 autograder", "course/modules/BK/BK4/project.html:199; grader/instance.py", P,
    "Page :199 ranges (N 4-6; funds >= 1 cent; 40-80 losses; targets 9000/9500/9750) match instance.py:25-39 (checked on seeds 0-19 by instance_sample_r10.py).")
row("proj-l03-crossref", "2.9 DAG/refs", "course/modules/BK/BK4/project.html:223; course/modules/BK/BK4/L03.html:134, :151-164", P,
    "Page :223 cites Lesson 3 for the cover definition and the sizing rule with its proof; L03 defines the scenario set (:134), states Proposition 2.3 (sized margin is an order statistic, :151) and proves it (:164).")

import datetime
VERIFIED_AT = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
frag = {
    "unit": "BK4",
    "slice": "BK4-c",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent verifier for BK4-c (round 10); did not build BK4",
    "pin": "00a84795f276456fce19d4181373cc4efba11a36 (HEAD of claude/fanout-b3 at verification; detached checkout)",
    "base": "c93dd526025c6dffd34c54cd2c89eb62a890f885 (round-9 pin; fragment /Users/billyribeiro/.fanout/frags/E-BK4-c.round9.json used as context; every row re-run or re-read this round, no PASS row carried)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE10-BK4-c",
    "scratch": "/tmp/bk4r10_coll.*, /tmp/bk4r10_starter.*, /tmp/bk4r10_leak (scratch copies; scripts that back rows are under ledgers/BK4/scripts/BK4-c-r10/)",
    "verified_at": VERIFIED_AT,
    "verdict": "FAIL",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta c93dd526..00a84795 for the slice: project.html (lines 54, 412-416, 420, 442-446, 468, 470, 478), plans/BK4-build-plan.md (5.2 cover_bps empty row; 5.3 period bullet removed), "
        "and new mutants v9a-v9e. Grader, instance, starter, reference, lab twins (BK4 project) and alternatives are byte-identical to the round-9 pin. "
        "Re-run this round: check_projects, check_pages --all, check_dag --all, run_labs (8/8), run_graders 0-49, mutate_graders 0-9 (67/67, including four new x10 mutants), "
        "alternatives 0-49 (5 x 50/50), page_smoke project (PASS), ruff, mypy --no-incremental, pytest labs, verify_refs offline (560, 0 problems) and live BK4 (2 entries, 0 problems). "
        "Round-9 FAILs: proj-rubric-c1-levels now PASS; proj-plan-conformance now PASS (ruling items 2 and 3 applied; item 1 as built); proj-rubric-c4-descriptors and proj-rubric-c5-descriptor remain FAIL on new gaps. "
        "Blind exemplar scoring: I read the full page, annotations included, before the blind pass, so separation is imperfect; the scores were then taken from memo prose only (blind_memo_text_r10.py). "
        "Not checked: a Pyodide session outside page_smoke (in-browser flags could differ from the local flags; not verified); the visual page (no figures); the full text of duffie2011central and bisndcpmi (the page makes no claim from them); the Lesson 3 proof (another slice); "
        "whether 'a limit of the simulator' includes limits outside the four named (the four are read as the set counted, which the 'three of the four' wording implies). "
        "No retrieval cards in this slice. The rubric enumeration encodes my reading of each cell; its results depend on that reading, and the cell-level fixes are stated in the failing rows."
    ),
    "summary": "",
}
statuses = [r["status"] for r in R]
frag["summary"] = (f"BK4-c round 10: {statuses.count(P)} PASS, {statuses.count(F)} FAIL of {len(R)} rows; "
                   f"mutants {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed. "
                   "FAIL: proj-rubric-c2-levels (rule-only sizing memo matches no level), proj-rubric-c3-descriptors (other sharing rule matches no level), "
                   "proj-rubric-c4-descriptors (two recommended margins match no level), proj-rubric-c5-descriptor ('no known direction' not counted as a direction, so exemplar B's C5 level depends on an unstated reading), "
                   "proj-grader-docstring-named-variables (docstring claims all expected values are named; five literal asserts).")
out = root / "ledgers/BK4/BK4-c.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, len(R), "rows", len(mutants), "mutants")
