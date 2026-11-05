"""Compose the round-12 fragment ledgers/BK4/BK4-c.json (verifier BK4-c, round 12) from the evidence in out/.

Usage: python3 -I write_fragment_r12.py <checkout>. Every row id of the round-11 fragment is kept; two rows are added.
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CK = Path(sys.argv[1])
OUT = CK / "ledgers/BK4/scripts/BK4-c-r12/out"
S = "ledgers/BK4/scripts/BK4-c-r12"
ROUND11_IDS = [
    "proj-lab1-numbers", "proj-lab2-numbers", "proj-lab3-numbers", "proj-fixture-tables", "proj-named-conditions",
    "proj-conventions-prose", "proj-hours", "proj-grader-reference-run", "proj-grader-starter-fails",
    "proj-collect-count", "proj-instances", "proj-mutants-builder", "proj-mutants-own", "proj-mutants-round7",
    "proj-mutants-round8", "proj-mutants-round9", "proj-mutants-round10", "proj-mutants-round11",
    "proj-large-cent-claim", "proj-mutant-float", "proj-mutant-argument", "proj-labs-simulated-stdlib",
    "proj-page-smoke", "proj-check-tools", "proj-ruff", "proj-mypy-repo", "proj-mypy-plan-command",
    "proj-pytest-labs", "proj-refs", "proj-banned-and-process-words", "proj-anchors-links", "proj-dag-concepts",
    "proj-rung-ladder", "proj-exemplar-a-calibration", "proj-exemplar-b-calibration", "proj-exemplar-b-numbers",
    "proj-rubric-c1-levels", "proj-rubric-c2-levels", "proj-rubric-c3-descriptors", "proj-rubric-c4-descriptors",
    "proj-rubric-c5-descriptor", "proj-rubric-observable-wording", "proj-exemplar-annotations-agree",
    "proj-rubric-self-form", "proj-lab2-learner-text", "proj-lab3-claim-checks-rules", "proj-notation-T",
    "proj-failure-leak", "proj-grader-docstring-named-variables", "proj-sizing-duplicate-losses",
    "proj-context-sentences", "proj-spec-context-length", "proj-alternatives", "proj-survivor-leftover-order",
    "proj-silence-named-refusals", "proj-refusal-count-docstring", "proj-remainder-spec", "proj-money-integer-claim",
    "proj-zero-loss-sizing", "proj-zero-loss-cover", "proj-round7-prose-delta", "proj-local-run",
    "proj-spec-signatures", "proj-spec-inputs-instance", "proj-l03-crossref", "proj-placement-claim",
    "proj-grade-scale-citation", "proj-autograder-claims",
]
assert len(ROUND11_IDS) == 68, len(ROUND11_IDS)

P = "course/modules/BK/BK4/project.html"
ROWS = {
    "proj-lab1-numbers": ("2.5 lab", f"{P}:56-139; tests/labs/BK4/lab-BK4-project-1.py", "PASS",
        "`.venv/bin/python tools/run_labs.py --unit BK4` PASS (out/run_labs_BK4.txt). Twin run `python -I -W error` exit 0, empty stderr (out/twin_project-1.out, .stderr). recompute_r12.py (out/recompute_r12.txt): layers 50000/6000/20000, residual 4000; survivors {1:1334,3:1666,4:1000}; target 9550 gives exact 191/5 = 38.2, k 39, margin 117088, cover 9750, one cent below 9500."),
    "proj-lab2-numbers": ("2.5 lab", f"{P}:141-190; tests/labs/BK4/lab-BK4-project-2.py", "PASS",
        "run_labs PASS; completion rule holds (two `___` blanks; every other page line equals the twin line, tools/run_labs.py check_lab). Expected block equals twin output. Tolerance claim: labs.js:50 bound is 1e-6*(1+117088) = 0.117 cent < 1 cent, so a wrong cent fails."),
    "proj-lab3-numbers": ("2.5 lab", f"{P}:252-366; tests/labs/BK4/lab-BK4-project-3.py", "PASS",
        "Twin run exit 0, empty stderr (out/twin_project-3.out, .stderr); output equals the expected block. recompute_r12.py: Part A rows and conservation True; Part B margins 105154/111074/117088 with k 36/38/39, covers 9000/9500/9750, one cent below 8750/9250/9500; Part C at 111074: 2,2,0,0 and at 105154: 4,2,0,0 (past margin, past fund, past capital, past survivors)."),
    "proj-fixture-tables": ("2.4 math", f"{P}:229-250; grader/test_project.py fixture tests", "PASS",
        "recompute_r12.py: all 11 layer-order fixture rows (80..300) OK; remainder fixture (1,2,3,4 cents) OK; sizing fixtures 8000->40, 8001->50, 10000->50, 5000 on four losses->20 OK; cover 3333 and 6666 (20000/3 = 6666.67) OK."),
    "proj-named-conditions": ("2.9 structure", f"{P}:201-212; grader/test_project.py refusal tests", "PASS",
        "The six Constraints bullets match the 15 refusal cases in test_refused_inputs_print_nothing_before_they_raise and the boundary tests (target 0/1/10000/10001, loss 0/-1, margin 0/-1, fund 0/-1, capital 0/-1, defaulter below/inside/above/lowest/highest). reference.py messages name each input."),
    "proj-conventions-prose": ("2.4 math", f"{P}:219-224 (conventions bullets); grader/reference.py:57-109", "PASS",
        "Re-derived every convention line (layer order a1,a2,a3,R; survivors floor and leftover to first positive fund in ascending id; conservation; cover floor; sizing k=ceil(tS/10000); money). Round-12 change at :219 ('three layers and then the surviving members') matches the four steps. Limits sentence (page line 470, exemplar B) re-derived: a larger loss cannot lower the k-th smallest loss nor raise the count at or below M, so omission biases margin down and cover up."),
    "proj-hours": ("2.9 hours", f"{P}:34, :36, :373-386 (table#hours); course/modules/BK/BK4/index.html:42, :161-174", "PASS",
        "Components 2+2+3+3+2+2+1 = 15 = data-hours-project and the hub; 5 lessons x 7 h = 35; 15/50 = 30 %. Independent estimate: Rung 1 about 2 h, Rung 2 about 2 h, layers and sharing 2-4 h, sizing and cover 2-3 h, suite edge cases 2-3 h, memo 2-3 h, self-assessment 1 h: total 14-18 h, within 30 % of 15."),
    "proj-grader-reference-run": ("2.6 autograder", "course/modules/BK/BK4/grader/reference.py; grader/test_project.py", "PASS",
        "`.venv/bin/python tools/run_graders.py --unit BK4 --seeds 0-49` -> 'run_graders BK4: PASS (reference 50/50 seeds)' (out/run_graders_BK4.txt). Local pytest `-I -m pytest -W error --assert=plain` on reference.py: 50/50 (out/alts_seeds_0-49.txt)."),
    "proj-grader-starter-fails": ("2.6 autograder", "course/modules/BK/BK4/grader/starter.py", "PASS",
        "starter run (out/starter_and_collect.txt): 82 failed, 4 passed; the 4 passes are non-function checks (frozen dataclass fields, seeded-case validity). Failure text names the test property, for example 'has no implementation for margin_for_cover yet', with no traceback."),
    "proj-collect-count": ("2.6 autograder", f"{P}:214; grader/test_project.py", "PASS",
        "`pytest --collect-only -q test_project.py` -> '86 tests collected' (out/starter_and_collect.txt). Page line 214 says 86 checks."),
    "proj-instances": ("2.6 autograder", "course/modules/BK/BK4/grader/instance.py:22-50", "PASS",
        "instance_check_r12.py (out/instance_check_r12.txt): seeds 0-49 all valid (ids 1..N, N in 4..6, DF >= 1000, IM >= 10000, K >= 0, S in 40..80, targets in 9000/9500/9750, defaulter a member); all 50 seeds contain the three regions; 50 distinct margin answers and 48 distinct uncovered totals."),
    "proj-mutants-builder": ("2.6 mutation", "ledgers/BK4/mutants/m01..m10", "PASS",
        f"`tools/mutate_graders.py --unit BK4 --seeds 0-9` ({S}/out/mutate_BK4_seeds0-9_r12.txt): all KILLED; see mutants list."),
    "proj-mutants-own": ("2.6 mutation", "ledgers/BK4/mutants/n1..n4, r3a..r5f", "PASS",
        "Same run: every n- and r-series mutant KILLED (out/mutate_BK4_seeds0-9_r12.txt)."),
    "proj-mutants-round7": ("2.6 mutation", "ledgers/BK4/mutants/s01..s05", "PASS", "Same run: s01..s05 KILLED."),
    "proj-mutants-round8": ("2.6 mutation", "ledgers/BK4/mutants/t8a..t8e", "PASS", "Same run: t8a..t8e KILLED (t8e by test_waterfall_does_not_change_its_arguments)."),
    "proj-mutants-round9": ("2.6 mutation", "ledgers/BK4/mutants/v9a..v9e", "PASS", "Same run: v9a..v9e KILLED."),
    "proj-mutants-round10": ("2.6 mutation", "ledgers/BK4/mutants/x10a..x10d", "PASS", "Same run: x10a..x10d KILLED."),
    "proj-mutants-round11": ("2.6 mutation", "ledgers/BK4/mutants/y11a..y11d", "PASS", "Same run: y11a..y11d KILLED (y11c by test_each_scenario_matches_the_oracle_on_both_instances)."),
    "proj-large-cent-claim": ("2.6 mutation", f"{P}:203-224; grader/test_project.py test_large_cent_shares_are_floored_in_integers", "PASS",
        "recompute_r12.py: loss*fund1 = 6.6e31 > 2**53 (True). Floor shares 6055950114045319 and 529746839784068, leftover 1 to member 1 gives 6055950114045320: the test's expected values; the parts sum to the loss 6585696953829388."),
    "proj-mutant-float": ("2.6 mutation", "ledgers/BK4/mutants/vc10_float_arithmetic.py", "PASS",
        "Same run: vc10 KILLED by test_large_cent_shares_are_floored_in_integers (seed 0)."),
    "proj-mutant-argument": ("2.6 mutation", "ledgers/BK4/mutants/r4f_sizing_sorts_caller_list_in_place.py; grader/test_project.py", "PASS",
        "Same run: r4f KILLED by test_margin_for_cover_and_cover_bps_do_not_change_their_list_argument (seed 0)."),
    "proj-labs-simulated-stdlib": ("2.5 lab", f"tests/labs/BK4/lab-BK4-project-1..3.py; {P}:54, :56-58, :141-146, :252-258", "PASS",
        "Labs import only `random` (standard library); SIMULATED label stated in the rungs intro and each lab docstring; no file read."),
    "proj-page-smoke": ("2.9 structure", P, "PASS",
        f"`.venv/bin/python tools/page_smoke.py --unit BK4 --pages project` PASS (out/page_smoke_project.txt): labs in Pyodide, in-browser grader 'All 86 tests pass'."),
    "proj-check-tools": ("2.6 autograder", P, "PASS",
        "check_projects --unit BK4 PASS; check_pages --unit BK4 PASS; check_dag --unit BK4 PASS (out/check_*_BK4.txt)."),
    "proj-ruff": ("2.6 autograder", "tests/labs/BK4; course/modules/BK/BK4/grader", "PASS",
        "`ruff check` and `ruff format --check` on both: 'All checks passed', '12 files already formatted' (out/ruff_bk4_project.txt)."),
    "proj-mypy-repo": ("2.6 autograder", "pyproject.toml [tool.mypy]", "PASS",
        "`mypy --no-incremental tests/labs/BK4 course/modules/BK/BK4/grader`: 'Success: no issues found in 12 source files' (out/mypy_bk4_project.txt)."),
    "proj-mypy-plan-command": ("2.6 autograder", "course/modules/BK/BK4/grader/test_project.py:28, :30", "PASS",
        "The two import-not-found ignores are present with their comments; the plan's mypy command exits 0."),
    "proj-pytest-labs": ("2.5 lab", "tests/test_labs.py", "PASS",
        "`pytest -q tests/test_labs.py -k BK4`: 8 passed (out/pytest_labs_BK4.txt)."),
    "proj-refs": ("2.1 citations", f"{P} reading list (data-cite duffie2011central, bisndcpmi); references/references.json:2854, :7412", "PASS",
        "`verify_refs.py --unit BK4` (live): '3 of 560 entries, 0 problems'; `verify_refs.py --offline`: '560 entries, 0 problems' (out/verify_refs_*). The page states no claim from either key."),
    "proj-banned-and-process-words": ("2.9 structure", f"{P}; grader/*.py; tests/labs/BK4/lab-BK4-project-*.py", "PASS",
        "grep for the BUILDER_RULES 1.3-1.4 banned strings (TODO, TBD, lorem, for brevity, beyond the scope, it is important to note, clearly, obviously, ellipsis, ...): no hit. Process words (builder, verifier, ledger, round, ruling): no hit. Substring hits 'we' (in were/would) are not pronouns."),
    "proj-anchors-links": ("2.9 structure", P, "PASS",
        "Every in-page anchor (#spec, #conventions, #grader-section, #report, #rubric-heading, #self-assessment, #stretch) exists; relative targets index.html, index.html#placement, L01.html, L03.html, L05.html, grader/*.py, ../../../review.html and the assets exist."),
    "proj-dag-concepts": ("2.9 DAG", P, "PASS",
        "The page has no data-concept link and no dfn. Names outside the closure (order statistic, close-out, stress) are plain prose; no curriculum concept id matches 'order statistic' (grep curriculum/*.yaml)."),
    "proj-rung-ladder": ("2.6 structure", f"{P}:41-50, :193-216, :491-497", "PASS",
        "Rungs 1-4 in order; rung 2 completion lab graded instantly (class 'lab completion'); rung 3 spec, autograder and memo; rung 4 stated not graded."),
    "proj-exemplar-a-calibration": ("2.6 rubric", f"{P} exemplar-a (data-level 2, data-scores 2,2,1,2,2)", "PASS",
        "Blind scores from the rubric and the memo prose only: C1 2, C2 2, C3 1, C4 2, C5 2; official 2,2,1,2,2; all within one level. Disclosure: the data-level/data-scores attributes and the start of the official-scoring line were visible in a grep preview before the blind extraction (out/blind_exemplars_text.txt), so the blindness is imperfect."),
    "proj-exemplar-b-calibration": ("2.6 rubric", f"{P} exemplar-b (data-level 4, data-scores 4,4,4,4,4)", "PASS",
        "Blind scores: C1 4, C2 4, C3 4, C4 4, C5 4 (the memo meets every level-4 descriptor on the blind text); official 4,4,4,4,4. Same disclosure as exemplar-a."),
    "proj-exemplar-b-numbers": ("2.2 numbers", f"{P}:456-478 (exemplar B memo)", "PASS",
        "Each number re-derived: pool 12000; 1333/1666/1000 floored, leftover 1 to member 1 -> 1334, sum 4000; k 38 (9500*40/10000 = 38); margin 111074 and cover 9500 (one cent below 9250); 105154 (9000) and 117088 (9750); 2 scenarios past 111074, 4 past 105154; 0 past capital and 0 past survivors; 5920 = 111074-105154; 500 bps = 9500-9000. All printed by Lab 3 or derived from inputs."),
    "proj-rubric-c1-levels": ("2.6 rubric", f"{P}:412 (C1 row)", "PASS", "Each level descriptor observable (layers named in order, cents for a stated scenario, statement that a layer waits for the one before)."),
    "proj-rubric-c2-levels": ("2.6 rubric", f"{P}:413 (C2 row)", "PASS", "Observable: target in basis points, value of k, sorted position, cover at the margin and one cent below."),
    "proj-rubric-c3-descriptors": ("2.6 rubric", f"{P}:414 (C3 row)", "PASS", "Observable: names pro rata and leftover rules, the survivors' sum to the residual; level 2 names the rules it omits."),
    "proj-rubric-c4-descriptors": ("2.6 rubric", f"{P}:415 (C4 row)", "PASS", "Observable: one margin with cover, the count past survivors or uncovered, one alternative; fallback counted as a second recommendation."),
    "proj-rubric-c5-descriptor": ("2.6 rubric", f"{P}:416 (C5 row); :470 (exemplar B limits)", "PASS", "Observable: four named limits, direction per limit, counter-evidence statement or 'cites none'; level 1 names no limit."),
    "proj-rubric-observable-wording": ("2.6 rubric", f"{P}:408-416", "PASS", "No vague descriptor ('good', 'some', 'adequate') in any level cell; each cell names a countable or checkable item."),
    "proj-exemplar-annotations-agree": ("2.6 rubric", f"{P}:425-478 (aside.annotation)", "PASS",
        "Exemplar A annotations: C1 L2, C2 L2 and miss L3, C3 L1, C4 L2, C5 L2 = blind scores. Exemplar B annotations: all L4 = blind scores."),
    "proj-rubric-self-form": ("2.6 rubric", f"{P}:484-488; course/assets/js/rubric.js", "PASS",
        "section.rubric-self has data-rubric, data-exemplars and data-store-key; rubric.js reads data-exemplars and stores through store.js; no POST or sendBeacon in course/assets/js (grep fetch: only same-origin assets)."),
    "proj-lab2-learner-text": ("2.5 lab", f"{P}:141-147, :186; tests/labs/BK4/lab-BK4-project-2.py", "PASS",
        "Hypothesis and interpretation match the code: share is residual*fund//pool; index -((-target*count)//10000); the printed lines agree with Lab 1."),
    "proj-lab3-claim-checks-rules": ("2.5 lab", f"{P}:253-366 (Lab 3 hypothesis and interpretation)", "PASS",
        "Every claim checked against out/p3 and recompute_r12.py: Part A 20000/55000/70000/80000/100000 rows; three sizing indices 36, 38, 39; one-cent-below covers fall short; Part C counts; 'conservation True in every row'; '100000-cent row only uncovered row'."),
    "proj-notation-T": ("2.4 notation", f"{P} (no math delimiters); notation/notation.json", "PASS",
        "project.html has no \\( or \\[ math; symbols L, S, k, t, M, K, R, D, DF_i, IM_d, Lambda are plain code text, none collides with a registered symbol (T, R^ast, Phi, gamma_3, gamma_4, Q, R_f, R^{e ast})."),
    "proj-failure-leak": ("2.6 autograder", "course/modules/BK/BK4/grader/test_project.py (asserts and helpers)", "PASS",
        "Helpers check_waterfall, must_refuse, checked_int carry messages with no expected value; assertion messages name the property; --assert=plain hides values. Only inputs appear (for example 'seeded scenario with loss N')."),
    "proj-grader-docstring-named-variables": ("2.6 autograder", "grader/test_project.py:1-17 (docstring) and its asserts", "PASS",
        "Expected values are named (want, want_survivors, want_uncovered, expected); the docstring claim holds for every assert read. Threshold literals (3, 40..80) are bounds, not expected answers."),
    "proj-sizing-duplicate-losses": ("2.4 math", f"{P}:223; grader/test_project.py test_repeated_losses_*; mutants r3a, r3e", "PASS",
        "Repeated losses each count in S: [5,5,10,20] at 5000 -> 5; [5,5,5,9,12] at 6000 -> 5 (recomputed); mutants r3a/r3e KILLED."),
    "proj-context-sentences": ("2.9 structure", f"{P}:197 (spec Context dd)", "PASS",
        "scripts/BK4-c-r12/context_sentences.py -> 4 sentences (out/context_sentences.txt), within BUILDER_RULES 5.2 (2-4)."),
    "proj-spec-context-length": ("2.9 structure", f"{P}:197 (dd of dt 'Context' in the spec)", "PASS",
        "Round-11 FAIL cleared: the dd now has 4 sentences (round 11 counted 5). scripts/BK4-c-r12/context_sentences.py output in out/context_sentences.txt."),
    "proj-alternatives": ("2.6 autograder", "ledgers/BK4/alternatives/alt1..alt5", "PASS",
        "run_impls.py (out/alts_seeds_0-49.txt): alt1 comprehensions, alt2 class ClearingHouse, alt3 Fraction, alt4 integer two-pass, alt5 bisection: each 50/50 seeds 0-49; reference 50/50."),
    "proj-survivor-leftover-order": ("2.6 autograder", "grader/test_project.py:411-429; mutants r4a, s01", "PASS",
        "test_leftover_cent_goes_to_the_lowest_id_when_the_dictionaries_list_members_out_of_order and test_remainder_of_*: suite run passes reference and alternatives; r4a, s01 KILLED."),
    "proj-silence-named-refusals": ("2.6 autograder", "grader/test_project.py:1010-1059; mutants r4g, r4h", "PASS",
        "test_the_module_prints_nothing_on_valid_inputs and test_refused_inputs_print_nothing_before_they_raise present; mutants r4g, r4h KILLED."),
    "proj-refusal-count-docstring": ("2.6 autograder", "grader/test_project.py:1021-1022", "PASS",
        "The docstring 'Each named refusal in the list below' is true: the list holds all 15 named cases (the 6 named conditions with their sides)."),
    "proj-remainder-spec": ("2.4 math", f"{P}:248; grader/test_project.py:362-388; reference.py", "PASS",
        "Remainder fixture recomputed (out/recompute_r12.txt): loss 1 -> {1:1,2:0,3:0}; loss 2 -> {1:1,2:1,3:0}; loss 4 -> each 1, uncovered 1. Matches the page and the tests."),
    "proj-money-integer-claim": ("2.4 math", f"{P}:203, :224; grader/test_project.py (test_waterfall_returns_plain_int_money)", "PASS",
        "Reference and alternatives are integer-only and pass; the page claim is true of the reference. The float sizing index that the suite does not catch is recorded as FAIL row proj-mutant-float-index, not here."),
    "proj-zero-loss-sizing": ("2.6 mutation", "grader/test_project.py test_zero_losses_are_scenarios_in_the_sizing; mutant r5c", "PASS",
        "[0,10,20,30] at 5000 -> 10 (recomputed); r5c KILLED."),
    "proj-zero-loss-cover": ("2.6 mutation", "grader/test_project.py test_zero_losses_are_in_the_cover_denominator; mutant r5d", "PASS",
        "[0,0,5,9] at margin 0 -> 5000 (recomputed); r5d KILLED."),
    "proj-round7-prose-delta": ("2.9 structure", f"{P} delta 11d7077a..5db69a9: hunks at :197, :219, :470", "PASS",
        "Round-12 prose delta re-read: Context (:197) now 4 sentences; layer-order bullet (:219) 'four steps, three layers and then the surviving members' matches the code; exemplar B Limits (:470) claims re-derived (direction and 'cannot lower / cannot raise' statements are correct)."),
    "proj-local-run": ("2.6 autograder", f"{P}:395-400", "PASS",
        "Local command uses QF_SEED, pytest -q -p no:cacheprovider --assert=plain -W error test_project.py: the same flags as run_impls.py (out/alts_seeds_0-49.txt)."),
    "proj-spec-signatures": ("2.6 autograder", f"{P}:201; grader/starter.py:29-47", "PASS",
        "Signatures on the page (waterfall(loss_cents, defaulter_id, initial_margin_cents, default_fund_cents, ccp_capital_cents); margin_for_cover(losses_cents, target_bps); cover_bps(losses_cents, margin_cents)) equal starter.py."),
    "proj-spec-inputs-instance": ("2.6 autograder", f"{P}:199; grader/instance.py", "PASS",
        "Page inputs (N 4..6; DF >= 1 cent; 40..80 losses; targets 9000/9500/9750; SIMULATED) match instance.py and the validity check."),
    "proj-l03-crossref": ("2.9 DAG", f"{P}:223; course/modules/BK/BK4/L03.html:134, :143-146, :151-164", "PASS",
        "Lesson 3 defines the margin cover (margin cover level, dfn at :134), assumptions A3 and A4 (:143-146), and Proposition 2.3 with its proof (:151-164). The project's pointer is accurate."),
    "proj-placement-claim": ("2.9 structure", f"{P}:43; course/modules/BK/BK4/index.html (#placement, data-mastery 0.8, two data-skill items)", "PASS",
        "index.html has id placement, data-mastery=0.8 and exactly two data-skill items, so 'the mastery bar and both skill checks' is accurate."),
    "proj-grade-scale-citation": ("2.3 grades", f"{P}:420 (rubric paragraph); course/modules/BK/BK4/L01.html:40-46", "PASS",
        "L01 scale: B 'published, not settled', C 'working paper, practitioner research or single sample'. The page paraphrases B as 'published but not settled' (wording only)."),
    "proj-autograder-claims": ("2.9 structure", f"{P}:389-392, :520", "PASS",
        "The grader panel and footer claims hold: the suite runs in the browser (grader.js, py-worker.js); no POST or sendBeacon in course/assets/js."),
}
NEW_ROWS = {
    "proj-mutant-float-index": ("2.6 mutation", f"ledgers/BK4/mutants/r12b_sizing_index_float.py; {P}:203, :224; grader/test_project.py (no test with a float-sensitive index)", "FAIL",
        "The mutant computes the index as math.ceil(target_bps / 10_000 * count). run_mutate (out/mutate_BK4_seeds0-9_r12.txt) prints SURVIVED r12b_sizing_index_float.py -> None. It violates the page's stated rule: project.html:203 'every computation is integer arithmetic, so no float appears' and :224 'The sizing index is an exact fraction rounded up to an integer'. Float rounding gives 2800/10000*50 = 14.000000000000002, so ceil = 15; the exact index is 14 (scripts: write checks in float_index_probe_test.txt). No test in test_project.py uses a target/count pair where the float index differs on the page domain (the seeded cases use 9000/9500/9750 and 40-80 scenarios, where the two indices agree; checked for all S 40..80).",
        "Add to grader/test_project.py a test that asserts margin_for_cover(list(range(1, 51)), 2_800) == 14 (message: the index is the exact ceiling of target * S / 10000, computed in integers). Verified in a scratch copy: the test fails on r12b and passes on reference.py and on alt1..alt5. Then update page line 214 from 86 to 87 checks (the collect-only count must equal the page), and rerun run_graders, mutate_graders and page_smoke."),
    "proj-mutants-round12": ("2.6 mutation", "ledgers/BK4/mutants/r12a_survivor_share_rounded_up.py, r12c_only_one_leftover_cent.py, r12d_uncovered_added_to_first_survivor.py; scripts/BK4-c-r12/make_r12_mutants.py", "PASS",
        "Verifier-written mutants: r12a (survivor share ceiling) KILLED by test_layers_and_survivor_payments_add_to_the_loss_on_every_scenario; r12c (one leftover cent only) KILLED by the same test; r12d (uncovered added to first survivor) KILLED by the same test. Each docstring's first line names the student error. r12b is recorded in proj-mutant-float-index."),
}
ALL = {**ROWS, **NEW_ROWS}
missing = [i for i in ROUND11_IDS if i not in ALL]
assert not missing, missing
order = ROUND11_IDS + [i for i in NEW_ROWS]

rows = []
for rid in order:
    check, location, status, evidence = ALL[rid][:4]
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = ALL[rid][4] if len(ALL[rid]) > 4 else NEW_ROWS[rid][3]
    rows.append(row)
# the FAIL row carries its fix in the fourth tuple slot of NEW_ROWS
fail = [r for r in rows if r["status"] != "PASS"]
assert len(fail) == 1 and fail[0]["id"] == "proj-mutant-float-index", fail
fail[0]["fix"] = NEW_ROWS["proj-mutant-float-index"][4]
fail[0]["evidence"] = NEW_ROWS["proj-mutant-float-index"][3]

# mutants from the 75-mutant run
text = (OUT / "mutate_BK4_seeds0-9_r12.txt").read_text(encoding="utf-8")
mutants = []
for line in text.splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+)\.py: (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    killed_by = None if killer.strip() == "None" else re.sub(r"\s*\(seed \d+\)$", "", killer.strip())
    mutants.append({"id": name, "description": desc, "killed_by": killed_by, "status": status})
assert len(mutants) == 75, len(mutants)

frag = {
    "unit": "BK4",
    "slice": "BK4-c",
    "round": 12,
    "verifier": "Claude Haiku 5.5, independent verifier E12 for BK4-c (round 12); did not build BK4",
    "pin": "5db69a9b (HEAD of claude/fanout-b3; detached checkout)",
    "base": "11d7077a (round-11 pin); delta 11d7077a..5db69a9b for the slice: project.html (3 changed lines), ledgers/BK4/mutants y11a..y11d (listed as added), plans/FINAL-ARCHITECT-RULINGS.md (4 lines, read in full)",
    "checkout": str(CK),
    "scratch": "/tmp/bk4c_r12",
    "verified_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Read in full: project.html (522 lines), grader/instance.py, reference.py, starter.py, test_project.py (1116 lines), "
        "alternatives alt1..alt5 (all five read). Mutant bodies were not each read line by line; their docstrings were checked "
        "by AST and their verdicts by the mutate tool. Exemplars scored blind from the rubric text and the memo prose after "
        "stripping annotations, but the data-level/data-scores attributes and the official-scoring prefix of exemplar A were "
        "visible in a grep preview before the extraction (disclosed). Not checked: a visual render (the page has no figures); "
        "a Pyodide run on more than the one seed that page_smoke's in-browser grader used; alternatives other than the five "
        "builder implementations plus the reference; the Lesson 3 proof text beyond Proposition 2.3 (another slice); the "
        "abstract of duffie2011central (the page states no claim from it)."
    ),
    "summary": "",
}
statuses = [r["status"] for r in rows]
frag["summary"] = (
    f"BK4-c round 12: {statuses.count('PASS')} PASS, {statuses.count('FAIL')} FAIL, 0 UNVERIFIABLE of {len(rows)} rows; "
    f"mutants {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed (75 listed by tools/mutate_graders.py --unit BK4 --seeds 0-9, including four verifier mutants r12a..r12d); "
    "FAIL: proj-mutant-float-index (the float sizing index r12b survives; the page forbids float arithmetic). "
    "The round-11 FAIL proj-spec-context-length is cleared (Context now 4 sentences). Reference 50/50; five builder alternatives 50/50; collect 86 = page; starter fails with named messages; labs, check tools, ruff, mypy, page_smoke PASS."
)
out_path = CK / "ledgers/BK4/BK4-c.json"
out_path.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out_path, "rows", len(rows), "mutants", len(mutants))
