"""Write the round-3 BK4-c fragment (ledgers/BK4/BK4-c.json) from the verifier's round-3 evidence."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE3-BK4-c")
O = "ledgers/BK4/scripts/BK4-c-r3/out/"
GATE_NOTE = "mutate_graders BK4 --seeds 0-9"

NOTES = (
    "Read in full this round: project.html (521 lines), grader/instance.py, reference.py, starter.py, test_project.py (963 lines), and the three project twins. Diff since 67c47689 read in full (project.html, test_project.py, lab-BK4-project-3.py, index.html line 140, plan lines 419, 481, 515-517, open-items). Ruling check: vc11 (only starter.py:10 states argument immutability) not counted. Non-blocking: (1) the suite kills the distinct-count and dedupe mutants only incidentally (a valid [0,0] input for r3a; duplicate losses at seeds 8 and 17 for r3b), and the defaulter-id refusal kill for r3c comes from refusing a valid non-contiguous id 4; (2) the grader message checks remain substring matches on the page phrases; (3) test_the_margin_is_an_int uses target 9950, outside the page target set (harmless); (4) the exemplar calibrations are NOT blind this round (the official scores were read before scoring); (5) Pyodide per-test timing and the 60 s suite budget were not measured beyond the page_smoke run (0.8 s for the in-browser grader); (6) the self-assessment form behaviour was not exercised, only its localStorage and fetch calls were read (grader.js fetches local files only); (7) round-2 rows proj-mypy-plan-command, proj-large-cent-claim and proj-context-sentences are now PASS on the new text; proj-plan-conformance remains FAIL; (8) Lesson 3 (other slice) was read only for Definition 2.1 and Proposition 2.3, which the page cites for the cover and sizing rule. Not verified: the Duffie and Zhu abstract (no finding stated from it on this page); the SEC settlement rule (not in this slice)."
)

rows = []

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

row("proj-lab1-numbers", "2.5-labs, 2.2-numbers",
    "course/modules/BK/BK4/project.html:56-139; tests/labs/BK4/lab-BK4-project-1.py", "PASS",
    f"run_labs --unit BK4 --page project: 'run_labs BK4: PASS (3/3)' ({O}run_labs_project.out). Twin run: "
    f"`python -I -W error tests/labs/BK4/lab-BK4-project-1.py` exit 0, stderr 0 bytes ({O}twin_project_1.out/.err); "
    f"expected block equals twin output ({O}expected_vs_twin.out). Independent oracle ({O}rederive_r3.out, 72 OK, 0 MISMATCH): "
    "residual 4000, pool 12000, floored shares 1333/1666/1000, leftover 1 to member 1, survivors 1334/1666/1000; "
    "exact position 38.2, k 39, margin 117088; cover 9750 at the margin, 9500 one cent below; 38/40 = 95.00 %.")

row("proj-lab2-numbers", "2.5-labs, 2.2-numbers",
    "course/modules/BK/BK4/project.html:141-190; tests/labs/BK4/lab-BK4-project-2.py", "PASS",
    f"run_labs project PASS (3/3, {O}run_labs_project.out) applies the completion rule (every page line equals its twin "
    f"line or contains a blank). Twin exit 0, stderr 0 bytes ({O}twin_project_2.out/.err); expected block equals twin output "
    f"({O}expected_vs_twin.out). Completed expressions are floor(residual*DF_i/pool) and -((-target*count)//10000); "
    "they give 1334/1666/1000, k 39, margin 117088 (rederive_r3.out).")

row("proj-lab3-numbers", "2.5-labs, 2.2-numbers",
    "course/modules/BK/BK4/project.html:252-366; tests/labs/BK4/lab-BK4-project-3.py", "PASS",
    f"Twin exit 0, stderr 0 bytes ({O}twin_project_3.out/.err); expected equals output ({O}expected_vs_twin.out). "
    f"Independent oracle ({O}rederive_r3.out): Part A rows 20000/55000/70000/80000/100000 with conservation True and "
    "uncovered 12000 only in the last row; Part B targets 9000/9500/9750 give k 36/38/39, margins 105154/111074/117088, "
    "covers equal to the targets, one cent below 8750/9250/9500, brute force equal; Part C (9500: past margin 2, past "
    "fund 2, capital 0, survivors 0; 9000: past margin 4, past fund 2). Largest loss 118151 "
    f"({O}rederive_r3.out).")

row("proj-fixture-tables", "2.4-mathematics, 2.6-tests",
    "course/modules/BK/BK4/project.html:229-250; course/modules/BK/BK4/grader/test_project.py:281-441", "PASS",
    f"Independent recomputation ({O}rederive_r3.out): all 11 layer-order rows (loss 80 to 300 with margin 100, fund 50, "
    "capital 30, survivors 40/60), the remainder rows (1, 2, 4 cents), sizing 8000->40, 8001->50, 10000->50, 5000 over "
    "four losses->20, and cover 3333 and 6666 (floor of 6666.67). Every row agrees with the page table and with the test "
    "expectations (test_project.py:281-355, 362-428, 564-601). run_graders reference 50/50 (run_graders.out).")

row("proj-named-conditions", "2.6-spec, 2.6-tests, 2.6-failure-messages",
    "course/modules/BK/BK4/project.html:210; course/modules/BK/BK4/grader/test_project.py:516-523", "FAIL",
    "Each named condition except one has a refusal test and an accept test on its boundary (test_project.py:448-530, "
    "751-832). The waterfall condition 'defaulter_id is not one of the member ids' (project.html:210) is tested only for "
    "id 9, above the members (test_project.py:516-523). Nothing tests an id below the member range, so an implementation "
    "that refuses only ids above the largest member id passes the suite: mutant r3f_defaulter_upper_bound_from_max_id.py "
    f"PASSES all seeds 0-49 ({O}r3_mutants_seeds0-49.out) and survives {GATE_NOTE} ({O}mutate_graders_r3_final.out). "
    f"Directly, waterfall with defaulter_id 0 raises KeyError, not the ValueError that project.html:210 requires "
    f"({O}evidence_r3_mutants.out).",
    fix="Add a test beside test_defaulter_that_is_not_a_member_is_refused_and_the_message_names_it (test_project.py:516) "
        "that calls waterfall with defaulter_id 0 (and a value below the member range) and requires ValueError naming "
        "defaulter_id; re-run the mutation gate, which must then kill r3f.")

row("proj-conventions-prose", "2.2-numbers, 2.9-prose",
    "course/modules/BK/BK4/project.html:217-226; course/modules/BK/BK4/grader/reference.py:1-13, 43-109", "PASS",
    "Layer order, survivor rule with D (project.html:220), leftover rule, conservation, cover floor and "
    "k = ceil(t*S/10000) in integers match reference.py line by line and the independent oracle (rederive_r3.out). "
    "`grep -o '\\bT\\b' project.html` returns nothing; no backslash macro appears in the page.")

row("proj-hours", "2.9-hours",
    "course/modules/BK/BK4/project.html:373-388 (table#hours); course/modules/BK/BK4/index.html:29", "PASS",
    "Rows 2+2+3+3+2+2+1 = 15 (project.html table#hours). index.html:29 data-hours-project=\"15\" and "
    "data-hours-lessons=\"35\"; 35 + 15 = 50 (check_pages BK4 PASS, check_projects BK4 PASS: "
    f"{O}check_pages.out, {O}check_projects.out). 15/50 = 30 % as the page states.")

row("proj-grader-reference-run", "2.6-tests, 2.8-gate",
    "course/modules/BK/BK4/grader/reference.py; course/modules/BK/BK4/grader/test_project.py", "PASS",
    f"run_graders --unit BK4 --seeds 0-49: 'run_graders BK4: PASS (reference 50/50 seeds, slowest 0.2 s)' ({O}run_graders.out, exit 0). "
    "Reference copied as clearing_house.py; the browser flags --assert=plain -W error are used by the tool.")

row("proj-grader-starter-fails", "2.6-tests",
    "course/modules/BK/BK4/grader/starter.py; course/modules/BK/BK4/grader/test_project.py:940-963", "PASS",
    f"run_graders PASS includes the starter check. My candidate run on starter.py for seeds 0-49: 70 failed, 4 passed per "
    f"seed (no test calls the module in the 4 passing tests), every failure a named property via _named_when_unimplemented "
    f"({O}r3_mutants_seeds0-49.out).")

row("proj-collect-count", "2.6-tests",
    "course/modules/BK/BK4/project.html:214; course/modules/BK/BK4/grader/test_project.py", "PASS",
    f"pytest --collect-only -q test_project.py in a scratch copy with reference.py as clearing_house.py: '74 tests collected' "
    f"({O}collect.out). project.html:214 states 'runs 74 checks'. Equal.")

row("proj-instances", "2.6-instances, 2.2-numbers",
    "course/modules/BK/BK4/grader/instance.py:22-50", "PASS",
    f"Read in full. My validity script over seeds 0-49 (plan 5.5 rules: ids 1..N, N 4-6, DF>=1, IM>=0, K>=0, defaulter "
    f"a member, S 40-80, non-negative int losses, target in {{9000,9500,9750}}, one loss in each region): no problems "
    f"({O}instance_validity_r3.out). Seeds give 50 distinct sizing answers; 49 differ from seed 0 (plan: at least 40 materiality, "
    "at least 3 distinct). SIMULATED docstring present.")

row("proj-mutants-builder", "2.6-mutants",
    "ledgers/BK4/mutants/m01_fund_before_margin.py .. m10_seed0_hardcoded.py", "PASS",
    f"{GATE_NOTE}: each of the 10 builder mutants KILLED ({O}mutate_graders_r3_final.out; killer test names listed in the mutants array).")

row("proj-mutants-own", "2.6-mutants",
    "ledgers/BK4/mutants/vc01_cover_rounded.py .. vc15_negative_capital_accepted.py (vc11 excluded, see proj-mutant-argument)", "PASS",
    f"{GATE_NOTE}: all 14 verifier mutants in ledgers/BK4/mutants (vc01-vc10, vc12-vc15) KILLED ({O}mutate_graders_r3_final.out). "
    "The round-3 mutants are in rows proj-sizing-duplicate-losses and proj-named-conditions.")

row("proj-mutant-float", "2.6-mutants, 2.2-money",
    "ledgers/BK4/mutants/vc10_float_arithmetic.py; course/modules/BK/BK4/grader/test_project.py:431-441", "PASS",
    f"vc10 KILLED at seed 0 by test_large_cent_shares_are_floored_in_integers ({O}mutate_graders_r3_final.out). Float path on "
    f"the same fixture gives 6055950114045319 and 529746839784069, not the integer answer ({O}large_cent_check.out).")

row("proj-mutant-argument", "2.6-mutants",
    "ledgers/BK4/scripts/BK4-c-r1/unstated_mutants/vc11_sorts_argument_in_place.py; course/modules/BK/BK4/grader/starter.py:10", "PASS",
    "vc11 (margin_for_cover sorts the caller's list) survives. Its only statement is starter.py:10 ('Nothing may print, warn or "
    "change its arguments'); project.html has no such sentence (grep -i argument finds none). Not counted, per the ruling "
    "that a grader mutant is a FAIL only when project.html, the plan or the contract states the behaviour. Non-blocking: "
    "test_waterfall_does_not_change_its_arguments (test_project.py:258) covers waterfall only.")

row("proj-labs-simulated-stdlib", "2.6-simulated, 2.9-data",
    "tests/labs/BK4/lab-BK4-project-1..3.py; course/modules/BK/BK4/project.html:54; grader/instance.py:1-7", "PASS",
    "Labs import only random (seeded random.Random(1)); project.html:54 states every amount is SIMULATED and no file is read; "
    f"run_labs under python -I passes ({O}run_labs_project.out).")

row("proj-page-smoke", "2.10-browser",
    "course/modules/BK/BK4/project.html", "PASS",
    f"page_smoke --unit BK4 --pages project: 'page_smoke modules/BK/BK4/project.html: PASS' ({O}page_smoke_project.out); "
    "in-browser grader: 'All 74 tests pass on seed 1266721441' on the reference.")

row("proj-check-tools", "2.10-gates",
    "course/modules/BK/BK4/project.html", "PASS",
    f"check_projects --unit BK4: PASS; check_dag --unit BK4: PASS; check_pages --unit BK4: PASS ({O}check_projects.out, "
    f"{O}check_dag.out, {O}check_pages.out).")

row("proj-ruff", "2.10-gates",
    "tests/labs/BK4; course/modules/BK/BK4/grader; repository", "PASS",
    f"ruff check and ruff format --check on tests/labs/BK4 and grader: pass ({O}ruff_check.out, {O}ruff_format.out). Repository "
    f"`ruff check .` and `ruff format --check .`: 'All checks passed!' and '553 files already formatted' ({O}ruff_repo.out).")

row("proj-mypy-repo", "2.10-gates",
    "pyproject.toml [tool.mypy]", "PASS",
    f"mypy --no-incremental (repository): 'Success: no issues found in 385 source files' ({O}mypy_repo.out).")

row("proj-pytest-labs", "2.10-gates",
    "tests/test_labs.py; tests/test_run_labs.py", "PASS",
    f"pytest -q tests/test_labs.py tests/test_run_labs.py: exit 0, all tests pass ({O}pytest_labs.out).")

row("proj-refs", "2.3-citations",
    "course/modules/BK/BK4/project.html reading list; references/references.json (duffie2011central, bisndcpmi)", "PASS",
    f"verify_refs --unit BK4 (live): 'live re-verification of BK4: 2 of 560 entries, 0 problems' ({O}verify_refs_live.out). "
    f"verify_refs --offline: '560 entries, 0 problems' ({O}verify_refs_offline.out). The page attributes no statement to either source.")

row("proj-banned-and-process-words", "2.9-prose",
    "course/modules/BK/BK4/project.html; grader/*.py; tests/labs/BK4/lab-BK4-project-*.py", "PASS",
    "check_pages BK4 PASS (banned strings). grep for verifier, builder, fixer, architect, TODO, draft: no match in project.html. "
    "'Stated before running' is the lab hypothesis format, not a process word.")

row("proj-anchors-links", "2.9-links",
    "course/modules/BK/BK4/project.html", "PASS",
    "Internal targets all exist: #spec, #report, #stretch, #self-assessment, #rubric-heading, #grader-section, #main; "
    "index.html#placement (index.html:71 id placement); L05.html; index.html; grader/instance.py, starter.py, test_project.py; "
    "../../../review.html (course/review.html); CSS and vendor files exist.")

row("proj-dag-concepts", "2.14-DAG",
    "course/modules/BK/BK4/project.html", "PASS",
    f"check_dag BK4 PASS ({O}check_dag.out). project.html has no concept link or dfn. Terms such as order statistic and waterfall "
    "are prose; plan line 748 default makes out-of-closure concepts prose-only.")

row("proj-rung-ladder", "2.1-structure",
    "course/modules/BK/BK4/project.html:44-50 (ladder), :193-216 (spec), :490-497 (rung 4)", "PASS",
    f"Order rung 1 (Lab 1, line 56), rung 2 (completion lab, line 141), rung 3 (spec, line 196), rung 4 stretch (not graded); "
    f"check_projects BK4 PASS ({O}check_projects.out).")

row("proj-exemplar-a-calibration", "2.7-rubric-calibration",
    "course/modules/BK/BK4/project.html:424-453 (exemplar A), :408-417 (rubric)", "PASS",
    "Scored from the passage text: C1 2 (layers named, no scenario amount), C2 2 (margin and target, no cover check), C3 1 "
    "(no sharing rule), C4 2 (margin with no cover), C5 2 (two limits). Official 2,2,1,2,2; agreement within one level on every "
    "criterion. CAVEAT: the official scoring line (project.html:426) was visible before I scored, so this is not the blind "
    "calibration of VERIFIER 2.6; the blind requirement is not met in this round.")

row("proj-exemplar-b-numbers", "2.2-numbers, 2.7-rubric",
    "course/modules/BK/BK4/project.html:455-481 (exemplar B)", "PASS",
    "Every number in the passage: 80000, 50000, 6000, 20000, 4000, 12000, 1334+1666+1000 = 4000 (Lab 1 prints the conservation "
    "line); 38.0 = 9500*40/10000, k 38, margin 111074 (Lab 3 Part B/C), cover 9250 one cent below (Lab 3 Part B); 105154 and "
    "117088 (Lab 3 Part B); 5920 = 111074 - 105154 (computed difference, stated base 'on this set'); past margin 2 and 4 (Lab 3 "
    f"Part C). All checked against {O}rederive_r3.out. The setting numbers are the instance inputs in the lab code, allowed by "
    "project.html:479.")

row("proj-rubric-c3-descriptors", "2.7-rubric",
    "course/modules/BK/BK4/project.html:414", "PASS",
    "C3 level 1 'Names no sharing rule.' and level 2 'Gives survivor amounts, or states one of the two rules (pro rata or leftover) "
    "without the other.' are observable; exemplar A's C3 score (1) and annotation match level 1.")

row("proj-exemplar-b-calibration", "2.7-rubric-calibration",
    "course/modules/BK/BK4/project.html:455-481 (exemplar B), :457 (official scoring)", "PASS",
    "Scored from the passage text: C1 4 (names layers in order, 80000 scenario, 'used only after'), C2 4 (target, k 38, 38th "
    "position, cover 9500 and 9250), C3 4 (pro rata and leftover, sum 4000), C4 4 (margin with cover, count 2 and 0, alternative "
    "9000), C5 4 (four limits, no B/C claims). Official 4,4,4,4,4; within one level. CAVEAT: not blind (official scoring visible "
    "before scoring), as for exemplar A.")

row("proj-lab2-learner-text", "2.9-prose",
    "course/modules/BK/BK4/project.html:146-147, :186; tests/labs/BK4/lab-BK4-project-2.py:1-3", "PASS",
    "Hypothesis tells the learner which blanks to fill and the target outputs; the interpretation's 'the instant check compares "
    "the whole printed output, token by token' matches run_labs (numbers within tolerance, other tokens exact).")

row("proj-lab3-claim-checks-rules", "2.2-numbers, 2.9-prose",
    "course/modules/BK/BK4/project.html:253-366 (Lab 3 hypothesis and interpretation)", "PASS",
    f"Every claim checked against {O}rederive_r3.out and the twin output: conservation True in every row; only the 100000 row has "
    "an uncovered loss; three sizing indices 36, 38, 39; brute force agrees with the order statistic; Part C 9000 row: 4 past margin, "
    "2 past fund, none past capital or uncovered. Limit sentence ('the printed values describe this set only') holds.")

row("proj-notation-T", "2.13-notation",
    "course/modules/BK/BK4/project.html; notation/notation.json (symbols)", "PASS",
    "The page uses no bare T (grep). Its symbols are S, L, t, k, D, DF_i, IM_d, K, R, a1 to a3 and the names in the spec. "
    "notation.json registers T (number of return observations), Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f and Q; none is used "
    "with another meaning. The page uses no notation macro.")

row("proj-failure-leak", "2.6-failure-messages",
    "course/modules/BK/BK4/grader/test_project.py; project.html:399", "PASS",
    "79 '__tracebackhide__ = True' lines (74 tests and the helpers, grep count). No print in grader/*.py. Assertion and pytest.fail "
    "messages name the property or the input, never an expected value (read in full: test_project.py:107-157, 546-561, 570-601).")

row("proj-plan-conformance", "2.9-plan",
    "plans/BK4-build-plan.md:419, :441-445, :478-481, :515-517, :745-748; plans/BK4-open-items.md; course/modules/BK/BK4/project.html:196-212, :223, :414, :424, :455; grader/instance.py:39; grader/test_project.py:552-561, :633-641", "FAIL",
    "The binding plan (Architect decisions block, plan:748: 'Where the plan states a recommendation for an open question, follow "
    "it') is not met by the page and suite, and the plan text was edited in 9373ef39 and 67a2d13 to match the build (git diff "
    "67c47689 67a2d13 -- plans/BK4-build-plan.md). The architect block at plan:745-746 still reads 'Pending. No decision has been "
    "taken for BK4', and plans/BK4-open-items.md says 'Architect may overrule any of these'. Deviations: (a) target set plan:419 "
    "{9000,9500,9750} vs the original {9900,9950,9975} (page project.html Inputs; instance.py:39); (b) exemplar levels: original plan "
    "A=4, B=2, page A=2 (project.html:424), B=4 (:455); (c) C5 level-4 wording: original 'no procyclicality', page 'no change in "
    "margins in stress' (project.html rubric row C5); (d) brute-force sizing on every seed (original plan) vs two cases INST and "
    "INST2 (test_project.py:551-561); (e) monotonicity 'on each seed' (plan:517, still in the plan) vs INST and INST2 only "
    "(test_project.py:633-641), NOT recorded in open-items; (f) exception table: the plan lists five named conditions (plan:441-445); "
    "the page and suite add cover_bps empty (project.html:208, test_project.py:815-822), NOT in the plan or open-items; (g) plan 5.3 "
    "period convention (plan:458) appears nowhere on the page (not checked whether required). Decisions 1-4 in open-items are "
    "builder decisions, not an Architect ruling.",
    fix="Either conform the page and suite to the plan's original text (targets, exemplar levels, C5 wording, every-seed brute "
        "force, every-seed monotonicity, the five-condition table), or the Architect records ratification of decisions 1-4 and of "
        "(e)-(g) in the plan's Architect decisions block; revert the plan edits until then.")

row("proj-sizing-duplicate-losses", "2.6-tests, 2.2-numbers",
    "course/modules/BK/BK4/project.html:223; course/modules/BK/BK4/grader/test_project.py (no fixture with repeated losses)", "FAIL",
    "A student who counts distinct losses (k from len(set(losses)), sorted(set(losses))[k-1]) passes the suite on every seed "
    f"tried in the gate window: mutant r3e_sizing_counts_distinct_losses.py SURVIVES {GATE_NOTE} ({O}mutate_graders_r3_final.out) "
    f"and is killed only at seed 17 among 0-49 ({O}r3_mutants_seeds0-49.out). Behaviour: losses [5,5,10,20] at target 5000 give 5 "
    "by the page's rule (k = 2 of S = 4, the second smallest, counted with repetitions), and the mutant gives 10 "
    f"({O}evidence_r3_mutants.out). project.html:223 states the sizing is the k-th smallest of the scenario losses with "
    "k = ceil(t*S/10000) and S the number of scenarios. The one other kill of a dedupe (r3a) is a [0,0] IndexError on a valid "
    "input (test_project.py:809-812), not a property test.",
    fix="Add fixtures with repeated losses to test_project.py (for example [5, 5, 10, 20] at 5000 bps gives 5; [5, 5, 5, 9, 12] at "
        "6000 bps gives 5) with a message that names the scenario count, then re-run mutate_graders --unit BK4 --seeds 0-9; "
        "r3e must be killed in that window.")

row("proj-context-sentences", "2.6-spec",
    "course/modules/BK/BK4/project.html:196-197 (spec Context)", "PASS",
    "The Context dd has 4 sentences (counted by splitting on sentence-final full stops). BUILDER_RULES.md:201 requires 2-4. "
    "The prior 5-sentence text is gone.")

row("proj-alternatives", "2.6-alternatives",
    "ledgers/BK4/alternatives/alt1..alt5 (5); ledgers/BK4/scripts/BK4-c-r1/alternatives (5); ledgers/BK4/scripts/BK4-c-r2/alternatives (2)", "PASS",
    f"run_candidates.py: all 12 alternative correct implementations PASS the suite on every seed 0-49 ({O}alternatives_seeds0-49.out). "
    "Run against the current test_project.py (changed since round 2).")

row("proj-mypy-plan-command", "2.10-gates",
    "course/modules/BK/BK4/grader/test_project.py:28, :30 (type-ignore comments)", "PASS",
    f"`.venv/bin/mypy tests/labs/BK4 course/modules/BK/BK4/grader`: 'Success: no issues found in 12 source files', exit 0 "
    f"({O}mypy_plan.out). The two import-not-found ignores carry the reason in the comment (open-items decision 5).")


import re
ROOT_OUT = ROOT / "ledgers/BK4/scripts/BK4-c-r3/out/mutate_graders_r3_final.out"
mutants = []
for line in ROOT_OUT.read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+\.py): (.*?) -> (.*)$", line)
    if not m:
        continue
    status, fname, desc, killer = m.groups()
    killed_by = killer.strip() if status == "KILLED" else None
    mutants.append({"name": fname[:-3], "file": f"ledgers/BK4/mutants/{fname}", "description": desc.strip(),
                    "killed_by": killed_by})
assert len(mutants) == 30, len(mutants)

# the round-3 seeds 0-49 facts for the new mutants, recorded from r3_mutants_seeds0-49.out
for mu in mutants:
    if mu["name"] == "r3e_sizing_counts_distinct_losses":
        mu["killed_by"] = None
        mu["note"] = "survives seeds 0-9; killed only at seed 17 among 0-49 (test failures 3 at seed 17)"
    if mu["name"] == "r3f_defaulter_upper_bound_from_max_id":
        mu["killed_by"] = None
        mu["note"] = "passes all seeds 0-49; directly raises KeyError instead of ValueError for defaulter_id 0"

fragment = {
    "unit": "BK4",
    "slice": "BK4-c",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for BK4-c (round 3); did not build BK4",
    "pin": "67a2d13e7575608e95b2e34a9c7c2a82c61b117b",
    "base": ("67c47689 (round-2 pin, E-BK4-c.round2.json). Every project-slice row re-verified this round: project.html, "
             "grader/test_project.py, lab-BK4-project-3.py, index.html and plans/BK4-build-plan.md changed in 9373ef39 and "
             "67a2d13; no previous PASS row carried."),
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE3-BK4-c",
    "scratch": ("temporary directories from run_candidates (bk4cand.*, removed after each seed), the collect-only copy "
                "(removed), and /tmp/bk4r3_ev (removed)"),
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": NOTES,
    "summary": None,
}
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment["summary"] = (
    f"BK4-c round 3: verdict FAIL. {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE "
    f"of {len(rows)} rows. Mutants: {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed on seeds 0-9 "
    "(24 round-2 mutants and 6 round-3 mutants; r3e and r3f survive). Alternatives: 12/12 pass seeds 0-49. "
    "Failing rows: proj-named-conditions (defaulter id below the member range untested), proj-sizing-duplicate-losses "
    "(distinct-count sizing survives), proj-plan-conformance (binding plan not met; plan edited without Architect ruling)."
)
out = ROOT / "ledgers/BK4/BK4-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts, len(mutants))
