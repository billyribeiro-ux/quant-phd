"""Round-16 verifier fragment writer (BK4 slice c). Builds ledgers/BK4/BK4-c.json from the r16 outputs and the
round-15 fragment (carried rows only where the cited subject is byte-identical). Usage: python -I write_fragment_r16.py <root>
"""

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
S = "ledgers/BK4/scripts/BK4-c-r16"
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-BK4-c.round15.json").read_text(encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}
CARRY_FILES = (
    "course/modules/BK/BK4/grader/*.py, tests/labs/BK4/*.py, ledgers/BK4/alternatives/*, and project.html except its three "
    "changed lines :46, :139 and :400 (the only project.html lines in git diff d1e65a02 56cc575a)"
)
CARRY_PREFIX = (
    f"Carried from round 15 ({CARRY_FILES}; byte-identical since the previous pin d1e65a02; "
    "the subject lines are outside the changed hunks and were re-read this round):"
)

FRESH: dict[str, dict[str, str]] = {
    "proj-check-tools": {"location": "course/modules/BK/BK4/project.html", "evidence": f"check_pages --unit BK4: 'check_pages BK4: PASS' exit 0; check_dag --unit BK4: 'check_dag BK4: PASS' exit 0; check_projects --unit BK4: 'check_projects BK4: PASS' exit 0 (all on pin 56cc575a; {S}/out/check_pages.txt, check_dag.txt, check_projects.txt)."},
    "proj-ruff": {"location": "tests/labs/BK4; course/modules/BK/BK4/grader", "evidence": f"ruff check tests/labs/BK4 course/modules/BK/BK4/grader: 'All checks passed!' exit 0 ({S}/out/ruff_check.txt); ruff format --check: '12 files already formatted' exit 0 (out/ruff_format.txt). Repo 'ruff check .': 'All checks passed!' (ledgers/*/scripts and ledgers/*/mutants are in extend-exclude)."},
    "proj-mypy-repo": {"location": "pyproject.toml [tool.mypy]", "evidence": f"mypy --no-incremental (repo): 'Success: no issues found in 385 source files' exit 0 ({S}/out/mypy_repo.txt)."},
    "proj-mypy-plan-command": {"location": "course/modules/BK/BK4/grader/test_project.py:28,:30", "evidence": f"mypy --no-incremental tests/labs/BK4 course/modules/BK/BK4/grader: 'Success: no issues found in 12 source files' exit 0 ({S}/out/mypy_unit.txt)."},
    "proj-pytest-labs": {"location": "tests/test_labs.py; tests/test_run_labs.py; tests/test_page_checks.py; tests/test_memo_exemplars.py", "evidence": f"pytest -q -k 'BK4 or bk4' over the four files: 8 passed, exit 0 ({S}/out/pytest_BK4.txt)."},
    "proj-page-smoke": {"location": "course/modules/BK/BK4/project.html", "evidence": f"page_smoke --unit BK4 --pages project: 'page_smoke BK4: PASS' exit 0; in-browser grader 'All 88 tests pass on seed 938889400'; lab timings 0.0 s each ({S}/out/page_smoke_project.txt)."},
    "proj-refs": {"location": "course/modules/BK/BK4/project.html:503-507 (data-cite duffie2011central, bisndcpmi)", "evidence": f"verify_refs --offline: '560 entries, 0 problems' ({S}/out/verify_refs_offline.txt); verify_refs --unit BK4: 'live re-verification of BK4: 3 of 560 entries, 0 problems' ({S}/out/verify_refs_BK4.txt). The page states no statement attributed to either key (:503)."},
    "proj-anchors-links": {"location": "course/modules/BK/BK4/project.html", "evidence": f"{S}/static_checks_r16.py ({S}/out/static_checks_r16.txt): 18 internal href='#...' targets, 8 distinct, unresolved none. The two new links to #conventions (:46, :139) resolve to id=\"conventions\" (:218)."},
    "proj-banned-and-process-words": {"location": "project.html; grader/*.py; tests/labs/BK4/lab-BK4-project-*.py", "evidence": f"{S}/static_checks_r16.py: process-word hits 'BLUEPRINT' and 'round' only. Locations: grader/reference.py:4 ('BLUEPRINT requires that deployment exclude it'; grader-internal, never shown to learners, not linked from the page; ruling 4 records the deploy step as not a defect) and grader/test_project.py:698 ('round it up', arithmetic). No hit in project.html or the labs. PASS."},
    "proj-dag-concepts": {"location": "course/modules/BK/BK4/project.html", "evidence": f"check_dag --unit BK4: 'check_dag BK4: PASS' ({S}/out/check_dag.txt); static_checks_r16: 0 data-concept and 0 class=\"concept\" on the page. By-name uses (central counterparty, operational risk) are BK4-owned per curriculum/02-economics-finance-core.yaml."},
    "proj-notation-T": {"location": "course/modules/BK/BK4/project.html (Conventions :220-225; Inputs :200; labs)", "evidence": "notation/notation.json lists 8 symbols: T (return observations), \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. The page's symbols (L, S, K, D, R, t, k, M, Lambda, DF_i, IM_d, DF_d, a1-a3, N, i, c) collide with none; the page has 0 TeX math delimiters (static_checks_r16)."},
    "proj-l03-crossref": {"location": "course/modules/BK/BK4/project.html:224,:417,:54; course/modules/BK/BK4/L03.html:143,:151-174,:415-419", "evidence": "project.html:224 defers the sizing proof to Lesson 3: L03.html:151-174 is Proposition 2.3 (the sized margin is an order statistic) with its proof; A3 and A4 at L03.html:143. project.html:417 cites L03 Section 3: L03.html:415 (Section 3 'Where the canon breaks') and :419 ('No close-out period is modelled'). project.html:54 and :58 use 'scenario' and 'cover', defined at L03.html:51 and :134."},
    "proj-grade-scale-citation": {"location": "course/modules/BK/BK4/project.html:421; course/modules/BK/BK4/L01.html:45-46", "evidence": "project.html:421 'B is published but not settled, and C is a working paper, practitioner research or a single sample' matches L01.html:45 ('published, not settled') and :46 ('working paper, practitioner research or single sample') word for word in substance."},
    "proj-reading-list-no-claim": {"location": "course/modules/BK/BK4/project.html:503-507", "evidence": "project.html:503 'This page attributes no statement to either.' and the two data-cite entries at :505-506; no claim, number or locator is attributed to either key anywhere on the page (grep of the page for the two keys: only :505-506)."},
    "proj-lab1-numbers": {"location": "course/modules/BK/BK4/project.html:56-139; tests/labs/BK4/lab-BK4-project-1.py", "evidence": f"Every printed value and interpretation number re-derived with {S}/recompute_r16.py ({S}/out/recompute_r16.txt): layers (50000, 6000, 20000, residual 4000); pool 12000; floored shares 1333/1666/1000 (sum 3999, leftover 1 to member 1); survivor payments 1334/1666/1000; exact position 191/5 = 38.2, k 39, margin 117088; cover 9750 at margin, 9500 one cent below. Interpretation's '38 of 40 scenarios is 95.00 %' (19/20) re-derived. lab-BK4-project-1 run alone under -I -W error: exit 0; page code == twin; stdout == expected block ({S}/out/lab_page_twin_check_r16.txt)."},
    "proj-lab2-numbers": {"location": "course/modules/BK/BK4/project.html:142-190; tests/labs/BK4/lab-BK4-project-2.py", "evidence": f"Completion lab: page code with the two blanks replaced by the twin's expressions equals the twin; twin alone exit 0; stdout equals the expected block (1334/1666/1000; k 39; margin 117088) ({S}/out/lab_page_twin_check_r16.txt). Interpretation's 'a wrong cent fails' checked: tolerance 1e-6*(1+117088) = 0.117 < 1 cent (recompute_r16.py)."},
    "proj-lab3-numbers": {"location": "course/modules/BK/BK4/project.html:253-368; tests/labs/BK4/lab-BK4-project-3.py", "evidence": f"Part A rows re-derived (20000 margin only; 55000 +5000 fund; 70000 +14000 capital; 80000 survivors 1334/1666/1000; 100000 uncovered 12000). Part B: k 36/38/39, margins 105154/111074/117088, covers 9000/9500/9750, one cent below 8750/9250/9500, brute force agrees (recompute_r16.py). Part C: 9500 -> past margin 2, past fund 2, past capital 0, past survivors 0; 9000 -> 4, 2, 0, 0. Twin alone exit 0; stdout equals the expected block ({S}/out/lab_page_twin_check_r16.txt)."},
    "proj-labs-simulated-stdlib": {"location": "tests/labs/BK4/lab-BK4-project-1..3.py; project.html:54,:56-58,:141-146,:252-258", "evidence": "Lab 1 imports random and fractions; Labs 2 and 3 import random; each carries 'The inputs are SIMULATED' in its docstring; the page states SIMULATED at :54 and :200. random.Random(1) seeds every generator. No file read, no network."},
    "proj-lab2-learner-text": {"location": "course/modules/BK/BK4/project.html:143-146,:190", "evidence": "The Lab 2 hypothesis and interpretation (:144, :190) name the two blanks and the expressions the conventions give; the completed expressions are the Lab 1 expressions (checked by substitution). No claim beyond the printed lines."},
    "proj-lab3-claim-checks-rules": {"location": "course/modules/BK/BK4/project.html:255,:367", "evidence": "Every claim in the :255 hypothesis and the :367 interpretation matches the Part A/B/C output: conservation True in every row; the only uncovered row is 100000; three sizing indices 36, 38, 39; 4 past margin and 2 past fund at 9000 bps; no scenario past capital or uncovered (recompute_r16.py)."},
    "proj-rung-ladder": {"location": "course/modules/BK/BK4/project.html:41-50", "evidence": "Round-15-batch hunk at :46 (Rung 2 link '(both defined under Conventions)') read: the anchor #conventions exists (:218) and the sentence is accurate (survivor share Conventions :221; sizing index :224-225). Rung 1 fully solved and annotated (Lab 1); Rung 2 graded instantly (Lab 2 instant check); Rung 3 is the spec; Rung 4 is not graded (:494)."},
    "proj-hours": {"location": "course/modules/BK/BK4/project.html:36,:34,:374-386; course/modules/BK/BK4/index.html:29,:39,:42,:162-174; curriculum/02-economics-finance-core.yaml:1074", "evidence": "Project table components 2+2+3+3+2+2+1 = 15 = data-hours-project 15 = :36 eyebrow; index.html declares 35 lesson + 15 project = 50, '30 %' = 15/50 = 30 % (recomputed); curriculum hours: 50 (line 1074)."},
    "proj-hours-estimates": {"location": "course/modules/BK/BK4/project.html:377-383", "evidence": "Own estimate per component: Rung 1 reading 2 h; Rung 2 2 h; waterfall and survivor sharing 3-4 h (layer order, remainder rule, 11 fixtures); sizing and cover 3 h (order statistic, ceiling index, floored cover); edge cases and the 88-check suite on seeds 0-9 2-3 h; memo 2 h; self-assessment 1 h. Total 13-16 h, inside 15 +/- 30 % (10.5 to 19.5 h)."},
    "proj-named-conditions": {"location": "course/modules/BK/BK4/project.html:204-212; grader/test_project.py:467-596,:892-986", "evidence": "All six named conditions of :206-211 (margin_for_cover empty; target below 1 or above 10000; negative loss in margin_for_cover and cover_bps; cover_bps empty; waterfall negative loss/margin/fund/capital; defaulter not a member below/between/above) have a refusal test naming the input, and each has an accepted boundary test (target 1 and 10000; zero loss; zero margin; zero fund; zero capital; lowest and highest id). Message strings required by the page ('at least one scenario is needed', 'losses cannot be negative') match the tests and the reference."},
    "proj-conventions-prose": {"location": "course/modules/BK/BK4/project.html:220-225", "evidence": "Layer order, survivors, conservation, cover, sizing and money conventions (:220-225) are the formulas in grader/reference.py (waterfall; margin_for_cover; cover_bps) and in the oracles of test_project.py (oracle_waterfall, oracle_sorted_margin, oracle_cover). Reference 50/50 seeds; suite 88/88 on the reference seed 0 (out/reference_seed0.txt)."},
    "proj-fixture-tables": {"location": "course/modules/BK/BK4/project.html:230-251", "evidence": "All 11 rows of the layer-order table (losses 80,100,120,150,151,170,180,181,200,205,300) recomputed by recompute_r16.py and matched; remainder fixture (losses 1, 2, 4) and sizing fixtures (8000 -> 40, 8001 -> 50, 10000 -> 50, four losses at 5000 -> 20) and cover fixtures (3333, 6666) recomputed; the suite's test_fixture_* functions assert the same values (88 pass on reference)."},
    "proj-money-integer-claim": {"location": "course/modules/BK/BK4/project.html:204,:225; grader/test_project.py:128-132,:450-459", "evidence": "checked_int rejects float and bool outputs; test_large_cent_shares_are_floored_in_integers uses products above 2**53 (recomputed: residual * fund = 6.59e15 * 6.69e15 > 2**53) and passes on the reference; the page's 'no float appears' is a constraint the grader enforces through type checks, not a claim about the method."},
    "proj-large-cent-claim": {"location": "course/modules/BK/BK4/grader/test_project.py:450-459", "evidence": "recompute_r16.py: pool 7278398114431529 > loss 6585696953829388, floored shares 6055950114045319 and 529746839784068, one leftover cent to member 1 gives 6055950114045320; the test expects 6055950114045320 and 529746839784068."},
    "proj-sizing-duplicate-losses": {"location": "course/modules/BK/BK4/grader/test_project.py:702-716", "evidence": "[5,5,10,20] at 5000 -> k 2 -> 5; [5,5,5,9,12] at 6000 -> k 3 -> 5 (recomputed); docstring 'a repeated loss is one scenario per occurrence' matches the page rule (:224, S counts every loss)."},
    "proj-zero-loss-sizing": {"location": "course/modules/BK/BK4/grader/test_project.py:719-726", "evidence": "[0,10,20,30] at 5000 -> k 2 -> 10 (recomputed); S counts the zero loss as page :224 requires."},
    "proj-zero-loss-cover": {"location": "course/modules/BK/BK4/grader/test_project.py:836-841", "evidence": "[0,0,5,9] at margin 0 -> 2 of 4 -> 5000 bps (recomputed); the zero losses are in the denominator as page :223 requires."},
    "proj-remainder-spec": {"location": "course/modules/BK/BK4/project.html:221; grader/test_project.py:378-447", "evidence": "The leftover rule (ascending id, DF_i > 0, one cent each) at :221 matches reference.py and the tests test_remainder_of_one_cent..., test_remainder_of_two_cents..., test_residual_equal_to_the_total_fund..., test_residual_above_the_total_fund..., test_a_member_with_no_default_fund..., test_no_survivor_has_a_fund...; the fixture rows of :249 are recomputed (remainder fixture 1, 2, 4)."},
    "proj-survivor-leftover-order": {"location": "course/modules/BK/BK4/grader/test_project.py:428-437", "evidence": "The dictionaries list members 3, 1, 2, 4; the leftover cent goes to member 1 (ascending id) as :221 states; test passes on the reference and is killed by mutants r4a and r14b (out/mutate_graders_r16.txt)."},
    "proj-silence-named-refusals": {"location": "course/modules/BK/BK4/grader/test_project.py:1035-1084", "evidence": f"test_the_module_prints_nothing_on_valid_inputs and test_refused_inputs_print_nothing_before_they_raise pass on the reference (88 passed, {S}/out/reference_seed0.txt); mutants r4g, r4h and r14d (print or warn) are killed (out/mutate_graders_r16.txt)."},
    "proj-refusal-count-docstring": {"location": "course/modules/BK/BK4/grader/test_project.py:1046-1047,:1049-1080", "evidence": "The docstring says 'Each named refusal in the list below'. The list has 15 entries covering each of the six named conditions of project.html:206-211 (margin_for_cover empty/target/negative; cover_bps empty/negative; waterfall negative loss, margin, fund, capital; defaulter above, below, between). Count is not stated on the page."},
    "proj-grader-docstring-named-variables": {"location": "course/modules/BK/BK4/grader/test_project.py:9-15", "evidence": f"Docstring claims checked: every f-string failure message interpolates an input (loss, target, fixture label), never a compared value; expected results are named variables (want, want_survivors, want_uncovered, expected). The plain-assert output in {S}/out/local_run_r16a_target_message_omits_target_bps.txt and local_run_r15b shows the test's message and no compared value."},
    "proj-failure-leak": {"location": "grader/test_project.py (all helpers; :112-157, :1117-1133); plain-assert runs in out/", "evidence": f"Failure messages grep: every pytest.fail/assert message is a property statement or names an input (loss, target, defaulter_id, target_bps, field name). The chained output of a refusal test (out/local_run_r16a_target_message_omits_target_bps.txt lines 15-29) shows the learner's own ValueError text and argument values (inputs), not any compared answer. No compared value is printed by the suite; see proj-local-run for the wording of the page."},
    "proj-context-sentences": {"location": "course/modules/BK/BK4/project.html:198", "evidence": "'The autograder checks the cent results and the cover values, not the docstring or the imports' is true: test_project.py tests Waterfall fields and frozen-ness, the money values and cover values; it has no docstring or import test (grep)."},
    "proj-spec-signatures": {"location": "course/modules/BK/BK4/project.html:202; grader/starter.py:19-45", "evidence": "The Waterfall fields (margin_cents, default_fund_cents, ccp_capital_cents, survivor_cents, uncovered_cents) and the three signatures in :202 match starter.py exactly; test_waterfall_is_a_frozen_dataclass_with_the_named_fields checks the same five names."},
    "proj-spec-inputs-instance": {"location": "course/modules/BK/BK4/project.html:200; grader/instance.py", "evidence": "N in 4..6 with ids 1..N (instance.py: count = randint(4, 6)); default funds >= 1 cent (randint(1000, 8000)); capital >= 0; defaulter in ids; 40-80 scenarios (randint(40, 80)); target in {9000, 9500, 9750}. Sample of 22 cases (20 seeds + two suite cases) all valid: " + f"{S}/instance_sample_r16.py ({S}/out/instance_sample_r16.txt)."},
    "proj-local-run": {"location": "course/modules/BK/BK4/project.html:398-400", "status": "FAIL", "evidence": f"The page's local command (:399) run by me with QF_SEED=3 against the mutant r16a (target-message mutant) and r16c, r16e, and r15b ({S}/out/local_run_*.txt via collect_and_local_run_r16.sh). Each run shows the test's own message, names inputs (e.g. 'seeded scenario with loss 6296', 'margin_for_cover with target 0') and no compared value, so the sentence's 'never the compared values' is right. But the sentence says 'so a failure shows only the test's own message'. For the refusal tests, which call pytest.fail inside an except ValueError block, pytest also prints the learner's own exception ('ValueError: the target must be in the range 1 to 10000, not 0' at out line 23, and 'ValueError: ... not 10001' at line 50), chained by 'During handling of the above exception, another exception occurred' (lines 27 and 54), and the learner's frame with its argument values 'losses_cents = [10, 20], target_bps = 0' (lines 15 and 42). The word 'only' is false for these runs.", "fix": "project.html:400: replace 'so a failure shows only the test's own message, which names the property and may name an input such as a loss or a target, and never the compared values' with 'so a failing check shows the test's own message, which names the property and may name an input such as a loss or a target, and never the compared values; when your code raises the wrong exception, pytest also prints that exception and the arguments of your function'. Re-run the page's command on one refusal mutant to confirm the new sentence matches the output."},
    "proj-autograder-claims": {"location": "course/modules/BK/BK4/project.html:215; grader/test_project.py", "evidence": "The :215 claims checked: 88 checks (collect-only 88, out/collect_only.txt); warnings as errors (-W error, pytestmark filterwarnings); conservation on every scenario of both cases (test loops over all losses); layer order at each fixture row (11 tests); the remainder rule; each named condition on both sides; sizing against the order statistic and against a brute-force search; cover floor; monotonicity; silence; purity. All on the reference: 88 passed."},
    "proj-exemplar-a-calibration": {"location": "course/modules/BK/BK4/project.html:426-455 (exemplar A)", "evidence": f"Blind scoring (ruling 15) from {S}/out/prose/exemplar-a_prose.txt (annotations, verdict and data-level attributes stripped by {S}/extract_memo_prose_r16.py): C1 2 (layers named in order, no cents for any scenario), C2 2 (sizing rule for 9500, no cover check, no k value), C3 1 (no sharing rule, no survivor amount), C4 2 (recommends a margin with no cover), C5 2 (two limits named). Official 2,2,1,2,2: equal. Caveat: the full page had been read before the blind scoring."},
    "proj-exemplar-b-calibration": {"location": "course/modules/BK/BK4/project.html:457-483 (exemplar B)", "evidence": f"Blind scoring (ruling 15) from {S}/out/prose/exemplar-b_prose.txt: C1 4, C2 4 (target, k 38, 38th loss, cover at margin and one cent below), C3 4 (pro rata and leftover rules; 1334+1666+1000 = 4000), C4 4 (one margin with cover 9500, counts 2/0/0, one alternative 105154), C5 4 (all four limits, direction for each; the fixed-set limit states 'no known direction', which the level-3 parenthetical accepts; the level-4 text does not say whether that counts: wording gap, recorded in proj-rubric-c5-descriptor). Official 4,4,4,4,4: equal (within one level on every criterion regardless). Caveat as above."},
    "proj-exemplar-b-numbers": {"location": "course/modules/BK/BK4/project.html:459-471", "evidence": "Every number in exemplar B re-derived or read: inputs 30000/50000/40000/20000, 4000/6000/5000/3000, CCP 20000, pool 12000, 40 losses (instance and lab inputs); 1333/1666/1000 and 1334/1666/1000 and residual 4000 (Lab 1); 38.0 and k 38 (38 x 10000 / 40 = 9500); 111074 (Lab 3 Part B and C, k 38); 9250 one cent below (Lab 3 Part B); 105154, 117088 (Lab 3 Part B); two and four scenarios past the margin (Lab 3 Part C 9500 and 9000); 5920 = 111074 - 105154; 500 bps = 9500 - 9000. All match recompute_r16.py."},
    "proj-exemplar-annotations-agree": {"location": "course/modules/BK/BK4/project.html:444-481 (annotations)", "evidence": "Each annotation's level matches its descriptor text: exemplar A annotations (C1 level 2, C2 level 2 and a miss of level 3, C3 level 1, C4 level 2, C5 level 2) and exemplar B (level 4 on every criterion) agree with the rubric wording at :413-417, and with the blind scores above."},
    "proj-alternatives": {"location": "ledgers/BK4/alternatives/alt1..alt5 (+ alt6 of this round)", "evidence": f"run_candidates_r16.py over seeds 0-49 ({S}/out/alts_seeds0-49.txt): reference 50/50, alt1_comprehensions 50/50, alt2_class_based 50/50, alt3_fraction 50/50, alt4_integer_two_pass 50/50, alt5_bisection 50/50. New alternative alt6_bisect_module.py ({S}/alts/): bisect-based sizing and cover, a while-loop leftover, a tuple-driven layer chain: 50/50."},
    "proj-direction-claims": {"location": "course/modules/BK/BK4/project.html:469,:471", "evidence": "Checked by argument and by the monotone order statistic: a second default's loss can only raise the k-th smallest loss and only lower the count at or below a margin, so the one-default model biases the margin down and the cover up; margins fixed in stress: rising stress margins make the simulated cover low, falling make it high; close-out with growing losses: margin low, cover high. The fixed-set limit is stated as 'no known direction', not claimed."},
    "proj-scope-words": {"location": "course/modules/BK/BK4/project.html:54,:139,:200,:215,:255,:367; labs", "evidence": "'only', 'all', 'every' and 'exactly' in the page are bounded: 'every amount' (integer cents, :54) is the convention; 'all of its amounts are SIMULATED' (:54) is true of the illustrative values; 'it does not show that the rules are correct for any other set' (:139) and 'The printed values describe this set of 40 scenarios only' (:367) are the honest bounds."},
    "proj-numbers-rounding": {"location": "project.html:58,:112-113,:139,:251,:384", "evidence": "38.2 = 191/5 exactly; 95.00 % = 19/20 exact; 6666.67 is floor-to-two-places of 20000/3 (6666.666...); 9750 at margin 117088 and 9500 one cent below; hours 15 of 50 = 30 % exactly. No prose number is rounded away from an unrounded value."},
    "proj-page-prose-delta-ruling": {"location": "plans/BK4-build-plan.md:751; plans/FINAL-ARCHITECT-RULINGS.md 4-5; project.html:200,:209,:426,:457", "evidence": "The binding 2026-11-04 decisions (target set 9000/9500/9750; exemplar levels A 2 and B 4; the empty-losses condition on cover_bps) are as built: project.html:200 (target set), :209 and grader/test_project.py:956-963 (cover_bps empty condition), :426 (data-level 2) and :457 (data-level 4). The plan file is unchanged since d1e65a02 (git diff --name-only)."},
    "proj-grader-reference-run": {"location": "course/modules/BK/BK4/grader/reference.py", "evidence": f"run_graders --unit BK4 --seeds 0-49: 'run_graders BK4: PASS (reference 50/50 seeds, slowest 0.5 s)' exit 0 ({S}/out/run_graders.txt). Suite on the reference seed 0 alone: 88 passed."},
    "proj-grader-starter-fails": {"location": "course/modules/BK/BK4/grader/starter.py", "evidence": f"starter.py run as clearing_house.py at seed 0: 84 failed, 4 passed; each failure names the missing implementation ('the student module has no implementation for waterfall yet'), no traceback ({S}/out/starter_seed0.txt)."},
    "proj-collect-count": {"location": "course/modules/BK/BK4/project.html:215 (88 checks)", "evidence": f"pytest --collect-only -q test_project.py (scratch copy with the reference as clearing_house.py): '88 tests collected', exit 0 ({S}/out/collect_only.txt). The page's '88 checks' equals the collect-only count."},
    "proj-instances": {"location": "course/modules/BK/BK4/grader/instance.py", "evidence": f"Sample of 20 seeds (0-19) plus seeds 7919 and 7920 (the suite's second case for seed 0 is 7919): all 22 valid under page :200 and the instance docstring; each has the three separated regions (margin, fund, past every layer); 22 distinct sized margins. {S}/instance_sample_r16.py, out/instance_sample_r16.txt."},
    "proj-placement-claim": {"location": "course/modules/BK/BK4/project.html:43; course/modules/BK/BK4/index.html:69", "evidence": "index.html:69 is section id=placement (data-mastery 0.8); the placement bar and both skill checks are on the module page; project.html:43 agrees."},
    "proj-page-test-count-line": {"location": "course/modules/BK/BK4/project.html:215", "evidence": "'runs 88 checks' equals collect-only 88 and the in-browser 'All 88 tests pass' (page_smoke, out/page_smoke_project.txt)."},
    "proj-lab-page-twin": {"location": "course/modules/BK/BK4/project.html lab blocks; tests/labs/BK4/lab-BK4-project-1..3.py", "evidence": f"{S}/lab_page_twin_check_r16.py: lab 1 and lab 3 page code equals the twin (trailing newline ignored); lab 2 page code with the two '___' blanks replaced by the twin's expressions equals the twin (ruling 11 convention). Expected blocks equal the twins' stdout (out/lab_page_twin_check_r16.txt)."},
    "proj-twins-alone": {"location": "tests/labs/BK4/lab-BK4-project-1..3.py", "evidence": "Each twin run alone with python -I -W error: exit 0, stderr empty (lab_page_twin_check_r16.txt)."},
}

for mid in [r for r in prev_rows if r.startswith("proj-mutant") or r.startswith("proj-cap-layer")]:
    pass

MUTANT_ROW_IDS = {
    "proj-mutants-builder", "proj-mutants-own", "proj-mutants-round7", "proj-mutants-round8", "proj-mutants-round9",
    "proj-mutants-round10", "proj-mutants-round11", "proj-mutants-round12", "proj-mutants-vc", "proj-mutant-float-index",
    "proj-mutant-float", "proj-mutant-argument", "proj-mutants-round13", "proj-mutant-fund-capped-at-pool",
    "proj-mutants-round14", "proj-mutants-r15",
}
MUTANT_TEXT = (
    f"Re-run this round (tools/mutate_graders.py --unit BK4 --seeds 0-9, pin 56cc575a; {S}/out/mutate_graders_r16.txt): "
    "92 of 92 mutants killed, exit 0, including every mutant this row names; the killer is listed in the mutants field."
)
for rid in MUTANT_ROW_IDS:
    FRESH[rid] = {"location": "ledgers/BK4/mutants/", "evidence": MUTANT_TEXT}
FRESH["proj-mutant-r15c-equivalent"] = None  # carried below
FRESH["proj-round7-prose-delta"] = {"location": "course/modules/BK/BK4/project.html:38,:45,:54,:58,:215", "evidence": "git diff d1e65a02 56cc575a -- course/modules/BK/BK4/project.html changes only :46, :139 and :400; lines :38, :45, :54, :58 and :215 are byte-identical and were re-read this round (the Rung 1 line at :45 and the Lab 1 hypothesis at :58 contain the round-7 numbers, all re-derived in proj-lab1-numbers)."}

# New rows of this round.
NEW_ROWS = [
    {"id": "proj-r16-new-mutants", "check": "2.6 mutation (own mutants)", "location": "ledgers/BK4/mutants/r16a..r16e",
     "status": "PASS", "evidence": f"Five new student-error mutants written from reference.py ({S}/make_mutants_r16.py, each one replacement asserted to match once): r16a target refusal omits target_bps (page :207 says the message names target_bps; killed by test_target_of_zero_is_refused_in_margin_for_cover); r16b defaulter margin read at key defaulter_id-1 (killed by test_each_scenario_matches_the_oracle_on_both_instances); r16c defaulter fund capped at the full loss (killed by the oracle test and fixture test_fixture_loss_120); r16d negative-loss refusal omits loss_cents (page :210 says the message names the input; killed by test_negative_loss_is_refused_and_the_message_names_the_loss); r16e cover_bps sorts the caller's list (page :204 'no function changes any of its arguments'; killed by test_margin_for_cover_and_cover_bps_do_not_change_their_list_argument). All five killed."},
    {"id": "proj-r16-alt6", "check": "2.6 autograder (alternatives)", "location": f"{S}/alts/alt6_bisect_module.py", "status": "PASS",
     "evidence": f"Sixth alternative (bisect-based sizing and cover, while-loop leftover, tuple-driven layer chain, different error texts): 50/50 seeds 0-49 pass ({S}/out/alts_seeds0-49.txt)."},
    {"id": "proj-r16-blind-prose", "check": "2.9 structure (rubric blind)", "location": "course/modules/BK/BK4/project.html:424-489", "status": "PASS",
     "evidence": f"Blind extraction of exemplar memo prose ({S}/extract_memo_prose_r16.py, output in {S}/out/prose/) contains no 'Meets', 'Misses', 'Official' or data-score text; scoring from it is recorded in proj-exemplar-a-calibration and proj-exemplar-b-calibration."},
]


def mutants_from_run() -> list[dict[str, str]]:
    out = []
    text = (root / S / "out/mutate_graders_r16.txt").read_text(encoding="utf-8")
    for line in text.splitlines():
        m = re.match(r"KILLED (\S+?): (.*) -> (.*) \(seed \d+\)$", line)
        if m:
            out.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3)})
    return out


mutants = mutants_from_run()
assert len(mutants) == 92, len(mutants)

rows: list[dict[str, str]] = []
for rid, prow in prev_rows.items():
    if rid in FRESH and FRESH[rid] is not None:
        f = FRESH[rid]
        row = {"id": rid, "check": prow["check"], "location": f["location"],
               "status": f.get("status", "PASS"), "evidence": f["evidence"]}
        if row["status"] != "PASS":
            row["fix"] = f["fix"]
        rows.append(row)
    else:
        status = prow["status"]
        assert status == "PASS", rid
        rows.append({"id": rid, "check": prow["check"], "location": prow["location"], "status": "PASS",
                     "evidence": f"{CARRY_PREFIX} {prow['evidence']}"})
for r in rows:
    if r["status"] == "PASS" and r["evidence"].startswith("Carried") and re.search(r":(46|139|400)\b", r["location"]):
        raise SystemExit(f"carried row cites a changed line: {r['id']}")
rows.extend({"check": r["check"], **{k: v for k, v in r.items() if k != "check"}} for r in NEW_ROWS)

# order: keep previous order, then the new rows
seen = {r["id"] for r in rows}
assert len(seen) == len(rows)
fail_rows = [r for r in rows if r["status"] != "PASS"]
verdict = "PASS" if not fail_rows else "FAIL"
passes = sum(1 for r in rows if r["status"] == "PASS")

fragment = {
    "unit": "BK4",
    "slice": "BK4-c",
    "round": 16,
    "verifier": "Claude Haiku 5.5, independent verifier E16 for BK4-c (round 16); did not build BK4",
    "pin": "56cc575a (detached; the checkout at /Users/billyribeiro/.fanout/wt/verifyE16-BK4-c)",
    "base": "d1e65a02 (round-15 pin; the previous fragment's pin). Delta for the slice: project.html has three hunks only (:43-46 Rung 2 link, :136-139 Lab 1 interpretation link, :397-400 local-run sentence); grader/, tests/labs/BK4/, ledgers/BK4/alternatives/ and the rest of the page byte-identical; ledgers/BK4/mutants gained four round-15 mutants (r15a, r15b, r15d, r15e), all re-run.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE16-BK4-c",
    "scratch": "/tmp/bk4c_r16_* (temporary workspaces, removed); every kept output is under ledgers/BK4/scripts/BK4-c-r16/out/",
    "verified_at": "2026-11-08",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Previous FAIL (proj-local-run, round 15) re-verified from scratch: the round-15 wording 'a failure shows the test's own message and no values' was replaced with 'shows only the test's own message ... and never the compared values'. The compared-value half now holds (no compared value is printed), but 'only' does not: refusal tests chain the learner's own ValueError and frame arguments (out/local_run_r16a...). Fix in the row.",
        "Blind exemplar scoring (ruling 15): memo prose extracted by ledgers/BK4/scripts/BK4-c-r16/extract_memo_prose_r16.py (annotations, verdict paragraphs, data-level/data-scores/data-label dropped). Scores from the prose: A 2,2,1,2,2; B 4,4,4,4,4; both equal the official scores. Caveat: the whole page had been read before scoring, so the scoring was not strictly blind.",
        "C5 level-4 descriptor (project.html:417) requires 'the direction in which each one biases'; exemplar B's fixed-set limit says 'no known direction'. The level-3 parenthetical accepts that statement; the level-4 text does not say so. Scored 4 (official); wording gap recorded, within one level either way.",
        "Exemplar B's Waterfall paragraph uses an initial margin of 50000 and its Recommendation counts use 111074; the paragraph discloses the convention, so the row passes (round-15 note unchanged).",
        "collect-only: the gate line in run_gates.sh failed (exit 2) because the suite imports clearing_house, which is absent in the checkout; re-run in a scratch copy with the reference as clearing_house.py: 88 collected. The gate line was removed and collect_and_local_run_r16.sh added.",
        "Equivalent mutant r15c (float cover floor) remains outside mutants/ with its proof in ledgers/BK4/scripts/BK4-c-r15/equivalent/ (carried; grader/reference.py byte-identical).",
        "reference.py:4 names BLUEPRINT (grader-internal, not learner text, not linked). Ruling 4 records the deploy step as not a defect.",
        "Not checked in this slice: cards.json (changed in 56cc575a, BK4-c012 and BK4-c013 basis text) belongs to another slice; L03.html and L01.html were read only at the cited lines; references/references.json entries were not re-read beyond verify_refs output.",
    ],
    "summary": "",
}
n_total = len(rows)
fragment["summary"] = (
    f"BK4-c round 16: {n_total} rows, {passes} PASS, {n_total - passes} FAIL (proj-local-run: sentence 'shows only the test's own message' contradicted by chained learner exception output); "
    f"mutants {len(mutants)}/{len(mutants)} killed (87 prior + 5 new r16a-e); alternatives 6/6 pass seeds 0-49; reference 50/50; 88 tests collected; all gates exit 0."
)
out = root / "ledgers/BK4/BK4-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", n_total, "pass", passes, "verdict", verdict, "mutants", len(mutants))
