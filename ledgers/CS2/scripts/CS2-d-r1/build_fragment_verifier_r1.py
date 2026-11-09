"""Build ledgers/CS2/CS2-d.json (closing delta verification, round 1) from the rows and the mutate log.

Run from the checkout root: .venv/bin/python ledgers/CS2/scripts/CS2-d-r1/build_fragment_verifier_r1.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = Path(__file__).resolve().parent
MUTATE_LOG = SCRIPTS / "mutate_CS2_0-9_verifier_r1.txt"
OUT = ROOT / "ledgers" / "CS2" / "CS2-d.json"
PIN = "d9de2fe5eea982d14cd9f922a61676b847506fbc"
BASE = "2a805c831410ab77c38c227f7e121e8537193ce9"
CARRY = "Carried from round 1 (byte-identical since the previous pin 2a805c83, checked by git diff --quiet 2a805c83 HEAD -- on the file or the cited path): "

ROWS = [
    {
        "id": "proj-prose-numbers",
        "check": "2.2 numbers in prose (classes a, b, c): counts, hours, lab numbers, exemplar scores",
        "location": "course/modules/CS/CS2/project.html:33, :211, :265-341, :366, :377; grader/test_project.py",
        "status": "PASS",
        "evidence": "Re-verified (project.html changed in 3 hunks). :211 says 176 checks; collect-only gives 176 for each seed 0-49 (ledgers/CS2/scripts/CS2-d-r1/collect_counts_seeds_0_49_r1.txt). Ten named conditions at :209 (items (1) to (10)). Lab 3 numbers recomputed with Python Fraction: exact mean 110046/11 = 10004.181818, exact sample variance 8.313636, last-4 minimum 10001.0 and maximum 10006.3, target ceil(5.5 - 1.1) = 5, 5th smallest 10003.2; the lab run output (tests/labs/CS2/lab-CS2-project-3.py, python -I -W error, rc 0) matches the page block line for line. Exemplar data-scores :366 (1,1,2,1,1,1) and :377 (4,4,4,4,4,4). data-hours-project=30 at :33 unchanged. grep for 175 or 176 under course/modules/CS/CS2 and curriculum finds no stale project count.",
    },
    {
        "id": "proj-line145-amortized",
        "check": "2.2 amortized-cost sentence",
        "location": "course/modules/CS/CS2/project.html:145",
        "status": "PASS",
        "evidence": CARRY + "project.html:145 lies in the Lab 1 section (lines 53-146), above the first changed hunk (line 206); base evidence unchanged.",
    },
    {
        "id": "proj-line386-design-note",
        "check": "design note paragraph (sketch limits sentence)",
        "location": "course/modules/CS/CS2/project.html:387-388 (was 386-387; shifted by one line by the lab 3 embed hunk at :267)",
        "status": "PASS",
        "evidence": CARRY + "paragraph text unchanged, only its line number moved from 386-387 to 387-388 (git diff hunks @@ -267,8 +267,9 @@ and @@ -335,7 +336,7 @@ change one line each; no hunk touches the paragraph).",
    },
    {
        "id": "proj-exemplar-b-claims",
        "check": "exemplar B annotated claims",
        "location": "course/modules/CS/CS2/project.html:377-392 (was 376-391)",
        "status": "PASS",
        "evidence": CARRY + "exemplar B block unchanged; only the line numbers moved by +1. Calibration of B: see proj-rubric-calibration.",
    },
    {
        "id": "proj-process-words",
        "check": "no process words in learner text",
        "location": "course/modules/CS/CS2/project.html (whole page, with the three changed hunks)",
        "status": "PASS",
        "evidence": "Re-verified: grep -n -i -E 'verifier|round [0-9]|ruling|verif' course/modules/CS/CS2/project.html returns no line. The new text (the ddof wording at :209, the NaN clause at :211, the lab 3 docstring and interpretation) contains no process word.",
    },
    {
        "id": "proj-banned-phrases",
        "check": "banned strings in visible prose (BUILDER_RULES 1.3-1.4)",
        "location": "course/modules/CS/CS2/project.html",
        "status": "PASS",
        "evidence": "Re-run: .venv/bin/python tools/check_pages.py --unit CS2 printed 'check_pages CS2: PASS' (the banned-string check is part of check_pages).",
    },
    {
        "id": "proj-rubric-observable",
        "check": "rubric rows observable (C1 to C6)",
        "location": "course/modules/CS/CS2/project.html:351-358 (was 350-357)",
        "status": "PASS",
        "evidence": CARRY + "rubric table unchanged; only line numbers moved by +1 after the lab 3 embed hunk.",
    },
    {
        "id": "proj-ladder-scope",
        "check": "four-rung ladder in order and scope",
        "location": "course/modules/CS/CS2/project.html:40-190",
        "status": "PASS",
        "evidence": CARRY + "lines 40-190 are above the first changed hunk (206); check_projects CS2 PASS re-run.",
    },
    {
        "id": "proj-notation",
        "check": "NOTATION: symbols vs notation/notation.json",
        "location": "course/modules/CS/CS2/project.html (changed hunks at :209, :211, :265-275, :336)",
        "status": "PASS",
        "evidence": "Re-verified: the changed text uses only symbols already on the page (variance(ddof), mean(), n, q, epsilon, the stream names). notation/ is byte-identical since 2a805c83 (git diff --quiet). No new symbol introduced.",
    },
    {
        "id": "proj-dag-concepts",
        "check": "DAG: concepts used outside the prerequisite closure",
        "location": "curriculum/01-foundations.yaml:417-421; course/modules/CS/CS2/project.html",
        "status": "PASS",
        "evidence": "curriculum/ byte-identical since 2a805c83. check_dag CS2 re-run: PASS. The changed text introduces no concept beyond NaN, mean and variance, which the page already used.",
    },
    {
        "id": "proj-reading-citation",
        "check": "reading and citation locators",
        "location": "course/modules/CS/CS2/project.html:409-415 (was 408-414)",
        "status": "PASS",
        "evidence": CARRY + "the Reading paragraph is unchanged; references/ byte-identical since 2a805c83; verify_refs --offline re-run: 560 entries, 0 problems.",
    },
    {
        "id": "proj-spec-completeness",
        "check": "specification names context, inputs, outputs, constraints, grading mode",
        "location": "course/modules/CS/CS2/project.html:194-224; 238",
        "status": "PASS",
        "evidence": "Re-verified: the changed Constraints sentence (ddof case now 'returns no value') and the Grading mode sentence (176 checks, NaN-after-one-value clause) remove no required output. check_projects CS2 re-run: PASS.",
    },
    {
        "id": "proj-context-length",
        "check": "context paragraph length and content",
        "location": "course/modules/CS/CS2/project.html:196",
        "status": "PASS",
        "evidence": CARRY + "line 196 is above the first changed hunk.",
    },
    {
        "id": "proj-hours",
        "check": "time budget components sum to declared project hours (30) and the hub figure",
        "location": "course/modules/CS/CS2/project.html:33, :227-245",
        "status": "PASS",
        "evidence": "Re-verified: lines 227-245 unchanged (no hunk), data-hours-project=30 at :33 unchanged, check_projects CS2 re-run PASS (it checks that the components sum to the declared hours and that the hub figure equals them).",
    },
    {
        "id": "proj-named-conditions",
        "check": "named conditions (1) to (10) each have a test that raises ValueError",
        "location": "course/modules/CS/CS2/project.html:209; grader/test_project.py",
        "status": "PASS",
        "evidence": "Re-verified from the changed :209: (1) mean and variance before any value: test_welford_mean_before_any_value_raises (171), variance_before_any_value (175), population_variance_before_any_value (179); (2) variance(1) with one value: test_welford_sample_variance_of_one_value_raises (183); (3) update NaN: test_welford_nan_update_raises (215), nan_first_value (221); (4) window below 1 and False: test_rolling_window_zero_raises (459), negative (463), boolean_false (467); (5) push NaN: test_rolling_nan_push_raises (487), nan_first_push (493); (6) min/max before push: 479, 483; (7) epsilon outside (0,1) with NaN, infinities and booleans: test_sketch_epsilon_outside_open_interval_raises (683, parametrised 0.0, 1.0, 1.5, -0.1, -1e-6, nan, inf, -inf), test_sketch_boolean_epsilon_raises (688); (8) add NaN: test_sketch_nan_add_raises (800), nan_first_add (805); (9) quantile outside [0,1], NaN, infinities: 701, 706, 711, 717; (10) quantile on empty sketch: 736, 741. Line numbers at d9de2fe5. Reference: 176 passed on seeds 0-9.",
    },
    {
        "id": "proj-line195-inputs",
        "check": "inputs paragraph matches the generator",
        "location": "course/modules/CS/CS2/project.html:198; grader/instance.py:27-41",
        "status": "PASS",
        "evidence": CARRY + "project.html:198 and grader/instance.py (byte-identical) unchanged.",
    },
    {
        "id": "proj-exemplar-namely-sentence",
        "check": "exemplar sentence naming the stream",
        "location": "course/modules/CS/CS2/project.html:364 (was 363)",
        "status": "PASS",
        "evidence": CARRY + "sentence unchanged; line moved by +1.",
    },
    {
        "id": "proj-inventory-test-claims",
        "check": "every test-inventory claim on the page is in the suite",
        "location": "course/modules/CS/CS2/project.html:211; grader/test_project.py",
        "status": "PASS",
        "evidence": "Re-verified: the new claim 'a NaN after one value (with variance(1) still refused and mean() still giving that value)' maps to test_welford_refused_nan_leaves_the_accepted_state (grader/test_project.py:225-232); the 176 count matches collect-only for seeds 0-49.",
    },
    {
        "id": "grader-instance",
        "check": "instance generator deterministic and seed-varying",
        "location": "course/modules/CS/CS2/grader/instance.py",
        "status": "PASS",
        "evidence": CARRY + "grader/instance.py byte-identical (git diff --quiet). run_graders CS2 0-49 re-run: PASS (reference 50/50).",
    },
    {
        "id": "instance-docstring-counts",
        "check": "instance.py docstring counts (offset groups)",
        "location": "course/modules/CS/CS2/grader/instance.py:8-14",
        "status": "PASS",
        "evidence": CARRY + "instance.py byte-identical.",
    },
    {
        "id": "instance-distinct-seeds",
        "check": "instances differ across seeds",
        "location": "course/modules/CS/CS2/grader/instance.py",
        "status": "PASS",
        "evidence": CARRY + "instance.py byte-identical; run_graders re-run on 50 seeds PASS.",
    },
    {
        "id": "grader-reference",
        "check": "reference.py passes the suite on every seed",
        "location": "course/modules/CS/CS2/grader/reference.py",
        "status": "PASS",
        "evidence": CARRY + "reference.py byte-identical. Re-run: reference copied as streamstats.py, suite on seeds 0-9 gives 176 passed each; run_graders CS2 0-49 PASS.",
    },
    {
        "id": "grader-starter",
        "check": "starter raises NotImplementedError and checks fail on it",
        "location": "course/modules/CS/CS2/grader/starter.py",
        "status": "PASS",
        "evidence": CARRY + "starter.py byte-identical; run_graders re-run PASS.",
    },
    {
        "id": "grader-tests-rank",
        "check": "rank-guarantee tests cover the claimed probes, streams, epsilons and witnesses",
        "location": "course/modules/CS/CS2/grader/test_project.py:870-952 (was 859-943; shifted by +9 after the inserted test at :225)",
        "status": "PASS",
        "evidence": "Re-verified: the rank tests are unchanged in body and moved by +9 lines (test_sketch_rank_guarantee_on_short_streams 870, with_ties 887, wide_epsilon 901, float-target witness 916, seven-decimal witness 934). Suite on the reference: 176 passed for seeds 0-9. Rank-related standing mutants (d10_03, r7_02, r12f_10, r15_08) are KILLED in the 179/179 run.",
    },
    {
        "id": "grader-docstring-delta",
        "check": "test module docstring (suite description and run command)",
        "location": "course/modules/CS/CS2/grader/test_project.py:1-14",
        "status": "PASS",
        "evidence": CARRY + "the module docstring is above the inserted test (diff hunk @@ -222,6 +222,15 @@).",
    },
    {
        "id": "grader-messages-no-expected-value",
        "check": "failing checks name the property and never print the expected value",
        "location": "course/modules/CS/CS2/grader/test_project.py (pytest.fail and must_raise messages)",
        "status": "PASS",
        "evidence": "Re-verified for the changed test: its messages are 'a NaN update after one value', 'variance(1) after one value and a refused NaN', 'mean() after a refused NaN' and 'after a refused NaN, mean() must describe the values added so far.'; none prints a value. The rest of the file is unchanged.",
    },
    {
        "id": "grader-wide-eps-docstring",
        "check": "wide-epsilon test docstring",
        "location": "course/modules/CS/CS2/grader/test_project.py:901-913 (was 892-904)",
        "status": "PASS",
        "evidence": CARRY + "body unchanged; moved by +9 lines.",
    },
    {
        "id": "grader-classes-never-print",
        "check": "classes never print and hold their own state",
        "location": "course/modules/CS/CS2/grader/test_project.py:253-290 and :954-968 (were 244-281 and 945-959)",
        "status": "PASS",
        "evidence": CARRY + "test bodies unchanged; moved by +9 lines; suite PASS on the reference.",
    },
    {
        "id": "grader-infinite-input",
        "check": "infinite inputs: outcome allowed only where the page states one",
        "location": "course/modules/CS/CS2/grader/test_project.py:440-453 (was 431-444)",
        "status": "PASS",
        "evidence": CARRY + "test body unchanged; moved by +9 lines.",
    },
    {
        "id": "equiv-m14_01",
        "check": "rank_target_without_clamp.py is extensionally equal to the reference",
        "location": "ledgers/CS2/equivalent/rank_target_without_clamp.py; ledgers/CS2/equivalent/README.md (m14_01 section, lines 102-113)",
        "status": "PASS",
        "evidence": "Re-verified: the mutant file is byte-identical since 2a805c83; the README m14_01 section has no hunk in the delta and its argument was re-read (every stored g is at least 1, so for any target at most 1 both versions return values[0]). run_alts_r1.py 0-49: rank_target_without_clamp.py 50/50 seeds pass (ledgers/CS2/scripts/CS2-d-r1/alts_repointed_and_equiv_verifier_r1.txt).",
    },
    {
        "id": "gate-mutate-cs2",
        "check": "standing mutant set is killed on seeds 0-9",
        "location": "ledgers/CS2/mutants/ (179 files)",
        "status": "PASS",
        "evidence": "Re-run: .venv/bin/python tools/mutate_graders.py --unit CS2 --seeds 0-9 printed 'mutate_graders CS2: PASS (179/179 killed)' (ledgers/CS2/scripts/CS2-d-r1/mutate_CS2_0-9_verifier_r1.txt). The count is 179, not the 178 or 181 of the base fragment, because r15_04 and r15_06 live in equivalent/.",
    },
    {
        "id": "gate-run-graders",
        "check": "run_graders CS2 seeds 0-49 (reference passes every seed, time limit, clean generator)",
        "location": "course/modules/CS/CS2/grader/",
        "status": "PASS",
        "evidence": "Re-run: .venv/bin/python tools/run_graders.py --unit CS2 --seeds 0-49 printed 'run_graders CS2: PASS (reference 50/50 seeds, slowest 0.2 s)'.",
    },
    {
        "id": "gate-check-projects",
        "check": "check_projects CS2",
        "location": "course/modules/CS/CS2/project.html",
        "status": "PASS",
        "evidence": "Re-run: .venv/bin/python tools/check_projects.py --unit CS2 printed 'check_projects CS2: PASS'.",
    },
    {
        "id": "gate-check-dag",
        "check": "check_dag CS2",
        "location": "curriculum/01-foundations.yaml CS2 prerequisites [CS1, M1]; course/modules/CS/CS2/",
        "status": "PASS",
        "evidence": "Re-run: .venv/bin/python tools/check_dag.py --unit CS2 printed 'check_dag CS2: PASS'.",
    },
    {
        "id": "gate-check-pages",
        "check": "check_pages CS2",
        "location": "course/modules/CS/CS2/",
        "status": "PASS",
        "evidence": "Re-run: .venv/bin/python tools/check_pages.py --unit CS2 printed 'check_pages CS2: PASS'.",
    },
    {
        "id": "gate-run-labs",
        "check": "run_labs CS2 (page code equals twin; twin output equals expected block)",
        "location": "tests/labs/CS2/lab-CS2-project-{1,2,3}.py",
        "status": "PASS",
        "evidence": "Re-run: .venv/bin/python tools/run_labs.py --unit CS2 printed 'run_labs CS2: PASS (14/14)'. Twins alone: python -I -W error from a scratch directory, rc 0 and 0 bytes of stderr for lab-CS2-project-1, -2 and -3.",
    },
    {
        "id": "gate-page-smoke",
        "check": "page_smoke CS2 project page in the browser (light and dark, desktop and 360 px)",
        "location": "course/modules/CS/CS2/project.html",
        "status": "PASS",
        "evidence": "Re-run: .venv/bin/python tools/page_smoke.py --unit CS2 --pages project (the --pages argument takes the page stem, so the path form runs nothing). Output: 'in-browser grader: All 176 tests pass on seed 1053280735', 'page_smoke modules/CS/CS2/project.html: PASS', 'page_smoke CS2: PASS' (ledgers/CS2/scripts/CS2-d-r1/page_smoke_CS2_project_verifier_r1.txt).",
    },
    {
        "id": "gate-ruff-mypy",
        "check": "ruff check, ruff format --check, mypy --no-incremental",
        "location": "whole repository (incl. grader/, tests/labs/CS2/, ledgers/CS2/mutants/)",
        "status": "PASS",
        "evidence": "Re-run: ruff check 'All checks passed!'; ruff format --check '555 files already formatted'; mypy --no-incremental 'Success: no issues found in 386 source files'.",
    },
    {
        "id": "gate-verify-refs",
        "check": "verify_refs --offline",
        "location": "references/references.json",
        "status": "PASS",
        "evidence": "Re-run: .venv/bin/python tools/verify_refs.py --offline printed 'offline integrity: 560 entries, 0 problems'.",
    },
    {
        "id": "gate-collect-count",
        "check": "collect-only count of test_project.py per seed (must equal the page count)",
        "location": "course/modules/CS/CS2/grader/test_project.py; project.html:211",
        "status": "PASS",
        "evidence": "Re-run for seeds 0-49 with the reference as streamstats.py: 50 of 50 lines 'seed=N 176 tests collected' (ledgers/CS2/scripts/CS2-d-r1/collect_counts_seeds_0_49_r1.txt, script collect_counts_r1.sh). The base row's count of 175 is corrected to 176 (the count changed with the inserted test).",
    },
    {
        "id": "gate-pytest-relevant",
        "check": "relevant pytest: tests/test_labs.py, tests/test_page_smoke.py, tests/test_page_checks.py -k CS2",
        "location": "tests/test_labs.py; tests/test_page_smoke.py; tests/test_page_checks.py",
        "status": "PASS",
        "evidence": "Re-run: .venv/bin/pytest tests/test_labs.py tests/test_page_smoke.py tests/test_page_checks.py -k CS2 -q printed 14 dots and '[100%]' with no failure.",
    },
    {
        "id": "gate-local-pytest",
        "check": "local pytest of the grader against the reference (warnings as errors)",
        "location": "course/modules/CS/CS2/grader/test_project.py",
        "status": "PASS",
        "evidence": "Re-run: reference copied as streamstats.py into a scratch directory, QF_SEED=0..9, pytest -q -p no:cacheprovider --assert=plain -W error: '176 passed' for each seed.",
    },
    {
        "id": "labs-project-1",
        "check": "lab 1 page code, twin, output",
        "location": "course/modules/CS/CS2/project.html:53-146; tests/labs/CS2/lab-CS2-project-1.py",
        "status": "PASS",
        "evidence": CARRY + "lab 1 section and its twin are byte-identical; run_labs CS2 (14/14) and the isolated twin run re-run PASS.",
    },
    {
        "id": "labs-project-2",
        "check": "lab 2 page code, twin, output",
        "location": "course/modules/CS/CS2/project.html:148-189; tests/labs/CS2/lab-CS2-project-2.py",
        "status": "PASS",
        "evidence": CARRY + "lab 2 section and its twin are byte-identical; run_labs CS2 (14/14) re-run PASS.",
    },
    {
        "id": "labs-project-3",
        "check": "lab 3 page code, twin, expected block equal to output",
        "location": "course/modules/CS/CS2/project.html:262-341; tests/labs/CS2/lab-CS2-project-3.py",
        "status": "PASS",
        "evidence": "Re-verified (twin changed: docstring and one interpretation sentence). Isolated run (python -I -W error): rc 0, no stderr. Output lines 'count 11', 'exact mean 10004.181818', 'exact sample variance 8.313636', 'welford mean 10004.181818', 'welford sample variance 8.313636', 'welford mean within 1e-9 of exact: True', 'last 4 values minimum 10001.0 maximum 10006.3', 'median target rank k = 5 of 11 with epsilon 0.1', 'the 5th smallest value is 10003.2' equal the page's expected block. run_labs CS2 14/14 PASS (page code equals twin). The new docstring says the minimum, maximum and answer print to one decimal and the mean, variance and Welford values to six: both match the print statements.",
    },
    {
        "id": "proj-rubric-calibration",
        "check": "blind calibration of exemplars A and B within one level on every criterion",
        "location": "course/modules/CS/CS2/project.html:366 (exemplar-a data-scores=1,1,2,1,1,1), :377 (exemplar-b data-scores=4,4,4,4,4,4); plans/KNOWN-ISSUES.md:35",
        "status": "PASS",
        "evidence": "Blind scorer file ~/.fanout/blind/CS2-d.json (ruling 23; read, not re-scored): A = [1,1,2,1,1,1], exact match to :366; B = [3,3,3,4,4,4], within one level of :377 on every criterion (C1 to C3 are 3 against 4, the gap listed in plans/KNOWN-ISSUES.md:35 and unchanged since 2a805c83).",
    },
    {
        "id": "grader-new-mutants",
        "check": "every new mutant names its student error on line 1 and is killed",
        "location": "ledgers/CS2/mutants/r14_01..03, r15_01..03, r15_05, r15_07, r15_08; ledgers/CS2/equivalent/r15_04, r15_06",
        "status": "PASS",
        "evidence": "Re-verified: line 1 of r15_05 is 'Sample variance of one value divides by zero instead of raising ValueError.' and of r15_08 is 'Quantile rank target uses float q times n, so q = 0.1, n = 20, epsilon = 0.05 gives target 1, not 2.' (the banner is gone). r14_01..03 and r15_01..03 name their errors on line 1. r15_04 and r15_06 are in equivalent/ (ruling 40). All 179 mutants in mutants/ are KILLED on seeds 0-9 (mutate_CS2_0-9_verifier_r1.txt).",
    },
    {
        "id": "grader-alternatives",
        "check": "correct alternative implementations pass the grader (over-constraint check)",
        "location": "ledgers/CS2/scripts/CS2-d-r15/alts/alt_r15_A..E (eight files, both variants of A, B and C)",
        "status": "PASS",
        "evidence": "Re-run on seeds 0-49 with run_alts_r1.py: all 8 files '50/50 seeds pass; failing seeds: []' (ledgers/CS2/scripts/CS2-d-r1/alts_verifier_current_0-49_r1.txt). The base row's count of five is corrected to eight.",
    },
    {
        "id": "grader-alt-r12-A-F",
        "check": "round-12 alternatives A to G pass the current grader (repointed where stale)",
        "location": "ledgers/CS2/scripts/CS2-d-r12/alts/alt_r12_A, B, F, G; ledgers/CS2/scripts/CS2-d-r1/alts_repointed_verifier_r1/alt_r12_C, D, E, alt_r7_06",
        "status": "PASS",
        "evidence": "Re-run on seeds 0-49: A, B, F, G each 50/50 (alts_verifier_current_0-49_r1.txt). The committed C, D, E and r7_06 copies in alts_repointed_current_r1/ hard-code the deleted worktree /Users/billyribeiro/.fanout/wt/verifyG1-CS2-d, so they fail to load (1 error, 0/50) and are retired under ruling 18. The same files with only that path changed to this checkout (alts_repointed_verifier_r1/) each pass 50/50 (alts_repointed_and_equiv_verifier_r1.txt).",
    },
    {
        "id": "grader-guarantee-battery",
        "check": "final-state rank-guarantee battery on reference, r15_04 and r15_06",
        "location": "ledgers/CS2/scripts/CS2-d-r15/guarantee_battery_r15.py and guarantee_battery_r15.txt; course/modules/CS/CS2/grader/reference.py; ledgers/CS2/equivalent/r15_04_*.py, r15_06_*.py",
        "status": "PASS",
        "evidence": CARRY + "reference.py, equivalent/r15_04 and equivalent/r15_06 are byte-identical and the battery script and output (CS2-d-r15) are unchanged. Recorded output: checks=15300 violations=0 for each of the three. The locator is corrected from ledgers/CS2/mutants/r15_04, r15_06 to ledgers/CS2/equivalent/ (moved in 2a805c83).",
    },
    {
        "id": "mut-survivors",
        "check": "previously surviving student-error mutants are killed",
        "location": "ledgers/CS2/mutants/r12f_10, r7_02, r8v_02, r9v_03",
        "status": "PASS",
        "evidence": "Re-verified in the 179/179 run (mutate_CS2_0-9_verifier_r1.txt): r12f_10 KILLED by test_sketch_rank_guarantee_on_short_streams[1-0.05] (seed 2); r7_02 KILLED by test_sketch_rank_guarantee_at_each_probe[4] (seed 3); r8v_02 KILLED by test_welford_every_short_prefix_matches_exact[3] (seed 2); r9v_03 KILLED by test_sketch_rank_guarantee_at_each_probe[4] (seed 5).",
    },
    {
        "id": "mut-r15-survivors",
        "check": "r15_07 (NaN checked after state change) is a real mutant and is killed",
        "location": "ledgers/CS2/mutants/r15_07_welford_nan_checked_after_state_change.py; grader/test_project.py:225-232; project.html:216",
        "status": "PASS",
        "evidence": "Re-verified: r15_07 is back in mutants/ with a student-error line 1. Against it the suite gives '1 failed, 175 passed' on each seed 0-9 (suite_on_source_r1.sh); the reference gives 176 passed. The mutate log line: KILLED r15_07 -> test_welford_refused_nan_leaves_the_accepted_state (seed 0). Basis: project.html:216 says both statistics describe every value added so far, and a refused NaN is not a value added (ruling 40).",
    },
    {
        "id": "equiv-r15-04-06-proof",
        "check": "r15_04 and r15_06 moved to equivalent/ with the proof or measurement the README claims",
        "location": "ledgers/CS2/equivalent/README.md (r15_04, r15_06 sections; Status); ledgers/CS2/equivalent/r15_04_*.py, r15_06_*.py",
        "status": "PASS",
        "evidence": "Ruling 40 applies: the README states both are measured, not proved, and gives the scope of the searches in those words. Re-run of the searches: r15_04_06_extra.py (root argument = checkout) printed reference, r15_04 and r15_06 each 'exhaustive small streams 43688 violations 0' (4+16+...+4^7 = 21,844 streams times two epsilons) and 'random long streams 120 violations 0' (ledgers/CS2/scripts/CS2-d-r1/r15_04_06_extra_verifier_rerun_r1.txt). The battery is carried (checks=15300 violations=0). Both files pass the grader on seeds 0-49 (equiv_r15_04_06_verifier_0-49_r1.txt), consistent with the README claim that the six files are not killed by the grader.",
    },
]

MUTANTS_REGEX = re.compile(r"^KILLED (?P<file>[^:]+)\.py: (?P<desc>.*) -> (?P<test>\S+ \(seed \d+\))$")


def mutants_from_log() -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for line in MUTATE_LOG.read_text(encoding="utf-8").splitlines():
        if not line.startswith("KILLED "):
            continue
        m = MUTANTS_REGEX.match(line)
        if m is None:
            sys.exit(f"unparsed mutate line: {line[:120]}")
        stem = m.group("file")
        out.append(
            {
                "id": stem,
                "description": m.group("desc"),
                "file": f"ledgers/CS2/mutants/{stem}.py",
                "killed_by": m.group("test"),
            }
        )
    return out


def main() -> None:
    mutants = mutants_from_log()
    if len(mutants) != 179:
        sys.exit(f"expected 179 KILLED lines, got {len(mutants)}")
    on_disk = sorted(p.stem for p in (ROOT / "ledgers" / "CS2" / "mutants").glob("*.py"))
    if on_disk != sorted(m["id"] for m in mutants):
        sys.exit("mutate log and mutants/ directory differ")
    rows_pass = sum(1 for r in ROWS if r["status"] == "PASS")
    fragment = {
        "unit": "CS2",
        "slice": "d",
        "round": 1,
        "verifier": "independent verifier (Haiku), CS2 slice d, round 1: closing delta verification (rulings 30, 37, 38a, 39, 40); did not build CS2",
        "pin": PIN,
        "base": BASE,
        "checkout": str(ROOT),
        "scratch": "ledgers/CS2/scripts/CS2-d-r1",
        "verified_at": "2026-11-09T19:03:31+00:00",
        "verdict": "PASS" if rows_pass == len(ROWS) else "FAIL",
        "rows": ROWS,
        "mutants": mutants,
        "registry_flags": [],
        "freshness_flags": [
            "The committed copies ledgers/CS2/scripts/CS2-d-r1/alts_repointed_current_r1/alt_r12_C, alt_r12_D, alt_r12_E and alt_r7_06 hard-code /Users/billyribeiro/.fanout/wt/verifyG1-CS2-d, a deleted worktree, and fail to load here (1 error, 0/50). Likewise alts_repointed_r1/ hard-codes verifyF11-CS2-d. Fix: retire these committed copies, or repoint them to a live checkout; the repointed copies in alts_repointed_verifier_r1/ pass 50/50.",
            "The mutants/ count is 179. The base fragment said 178 (and 181 in its row text); r15_04 and r15_06 live in equivalent/ and r15_07 is back in mutants/.",
            "cards.json changed in 2a805c83 and d9de2fe5 (outside slice d, belongs to the lesson slices).",
        ],
        "notes": [
            "Delta scope (ruling 30): git diff 2a805c83..d9de2fe5 over the slice paths. Changed: project.html (Constraints ddof wording at :209; Grading mode 175 to 176 and the NaN-after-one-value clause at :211; lab 3 embed docstring and one interpretation sentence); grader/test_project.py (test_welford_refused_nan_leaves_the_accepted_state inserted at :225, +9 lines); tests/labs/CS2/lab-CS2-project-3.py (docstring and interpretation wording only); ledgers/CS2/equivalent/README.md; ledgers/CS2/mutants r15_05 and r15_08 (line 1 now names the error), r15_07 (moved back from equivalent/); plans/FINAL-ARCHITECT-RULINGS.md (rulings 38a, 39, 40 appended; 30 and 37 unchanged). cards.json and plans/E3-open-items.md changed but are outside slice d.",
            "Ruling 37: no new mutants were authored in this closing round. The standing set (179 files in mutants/) was re-run on seeds 0-9; all 179 are KILLED. The base survivor r15_07 is killed by the new test (rule 40).",
            "Ruling 40 applied to r15_04 and r15_06: measured, not proved, and the README says so in those words. The README lemmas (0 to 3) were re-read; the algebra of Lemma 3 holds (K - 1 <= floor(t), and floor(t) + floor(2 eps n) <= floor(qn + eps n) since t + 2 eps n = qn + eps n). The d8_01, d8_02, d9_04 and rank_target_without_clamp files pass the grader on seeds 0-49, so the README statement that none is killed holds for all six.",
            "Alternatives on the current grader (seeds 0-49, alts_verifier_current_0-49_r1.txt): 13 pass (CS2-d-r1/alts alt_a; CS2-d-r15/alts eight files; CS2-d-r12/alts A, B, F, G). Four fail for reasons the page forbids and are retired under ruling 18: alt_b and alt_d return 9998.0 for a window of 2.5 (named no whole number, must raise); alt_c returns finite statistics after an infinite value; alt_e (float cutoff sketch) violates the rank guarantee at q = 0.1, n = 20, epsilon = 0.05. Four repointed copies (C, D, E, r7_06) pass 50/50 once the path is changed. The ruling 18 phrase 'the nine passing alternatives' equals the nine PASS lines of CS2-d-fix-r1/alts_0-49_fix.txt; the full current passing set is 17 counting the repointed copies.",
            "Blind calibration (ruling 23): ~/.fanout/blind/CS2-d.json was read and matched against project.html:366 and :377, not re-scored.",
            "Lesson pages L01 to L11 and cards.json belong to the lesson slices and were not verified here.",
        ],
        "summary": "CS2 slice d closing delta (round 1, verifier checkout d9de2fe5, base 2a805c83): PASS. Rows: 53 (53 PASS). The three base FAIL rows (grader-new-mutants, mut-r15-survivors, equiv-r15-04-06-proof) are re-verified and PASS: r15_05 and r15_08 docstrings fixed; r15_07 killed by test_welford_refused_nan_leaves_the_accepted_state on seeds 0-9; r15_04 and r15_06 accepted as measured-not-proved under ruling 40. Gates re-run and PASS: check_pages, check_dag, check_projects, run_graders 0-49, run_labs 14/14, twins under python -I -W error, page_smoke (project, 176 in browser), ruff, ruff format, mypy, verify_refs, collect-only 176 for seeds 0-49, pytest -k CS2 subset, local pytest seeds 0-9. Mutants: 179/179 killed on seeds 0-9. No new mutants (ruling 37).",
    }
    OUT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT} rows={len(ROWS)} pass={rows_pass} mutants={len(mutants)} verdict={fragment['verdict']}")


if __name__ == "__main__":
    main()
