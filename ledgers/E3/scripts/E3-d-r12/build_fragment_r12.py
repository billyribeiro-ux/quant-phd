"""Build the round-12 E3-d fragment (ledgers/E3/E3-d.json) from the evidence files of this round.

Rows are written from the commands and outputs listed in each evidence string; the mutant list is parsed from
out of the tools/mutate_graders.py run (mutate_E3_0-9.out) plus the four r12v mutants run on seed 0.
"""

from __future__ import annotations

import ast
import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
LOG = ROOT / "ledgers/E3/scripts/E3-d-r12/mutate_E3_0-9.out"
OUT = ROOT / "ledgers/E3/E3-d.json"
P = "PASS"
F = "FAIL"

ROUND11_PREFIX = "Carried from round 11 (project.html:1-209 and 214-391, grader/instance.py, grader/starter.py, reference lines 1-19, 24-269 byte-identical since ccaeeaf): "


def carried(text: str) -> str:
    return ROUND11_PREFIX + text


ROWS: list[dict[str, str]] = [
    # ---- gates (re-run on the pin 329c1d7)
    dict(id="gate-check-pages", check="gate: tools/check_pages.py --unit E3", location="course/modules/E/E3/*.html", status=P,
         evidence="ledgers/E3/scripts/E3-d-r12/check_pages_E3.out: 'check_pages E3: PASS', EXIT 0."),
    dict(id="gate-check-dag", check="gate: tools/check_dag.py --unit E3", location="course/modules/E/E3/", status=P,
         evidence="ledgers/E3/scripts/E3-d-r12/check_dag_E3.out: 'check_dag E3: PASS', EXIT 0."),
    dict(id="gate-check-projects", check="gate: tools/check_projects.py --unit E3", location="course/modules/E/E3/project.html", status=P,
         evidence="ledgers/E3/scripts/E3-d-r12/check_projects_E3.out: 'check_projects E3: PASS', EXIT 0."),
    dict(id="gate-run-labs-project", check="gate: tools/run_labs.py --unit E3 --page project", location="course/modules/E/E3/project.html Labs 1-3; tests/labs/E3/lab-E3-project-1..3.py", status=P,
         evidence="ledgers/E3/scripts/E3-d-r12/run_labs_project.out: 'run_labs E3: PASS (3/3)', EXIT 0."),
    dict(id="gate-page-smoke-project", check="gate: tools/page_smoke.py --unit E3 --pages project (Chromium, Pyodide, in-browser grader)", location="course/modules/E/E3/project.html grader panel (#grader)", status=F,
         evidence="Three runs, each 'in-browser grader: 49 of 50 tests pass on seed <S>' and 'page_smoke E3: FAIL (1 pages)' (ledgers/E3/scripts/E3-d-r12/page_smoke_project_run1..3.out; seeds 1313442603, 699963905, 1134419741). The labs in the same run pass. Re-run of the page's own runPytest through browser_grader_seed.py: seeds 0, 117910760 (x2), 1313442603, 699963905 each 49/50 with the same failure: test_estimate_on_a_fixed_26_response_participant_is_a_maximum: RuntimeError 'the observed information is not positive definite at the estimate' (ledgers/E3/scripts/E3-d-r12/browser_grader_seed.py). The same reference passes 50/50 locally under CPython for PYTHONHASHSEED 0..19 (fixed-26 test, probe in the same folder). The failure does not depend on the seed: the test's data are fixed.",
         fix="Make the fixed 26-response test independent of floating-point rounding: its participant's estimate lies on the boundary gamma -> 0 (gamma_hat 5.0e-8 on the reference, 1e-7..1e-16 on correct alternatives), where the observed information in the zeta direction is about 2 ulp of the objective (-1.776e-5 = 2*ulp(f)/h^2). Replace the fixture with a participant whose estimate is interior (gamma_hat well inside (0,1), e.g. 0.05 to 0.95, with a PD observed information), or drop the observed-information check for this fixture and keep the score and local-maximum checks. Then re-run page_smoke three times."),
    dict(id="gate-run-graders-seeds-0-49", check="gate: tools/run_graders.py --unit E3 --seeds 0-49 (reference passes the whole suite on every seed)", location="course/modules/E/E3/grader/reference.py; test_project.py", status=F,
         evidence="ledgers/E3/scripts/E3-d-r12/run_graders_E3_0-49.out: 'FAIL E3: reference fails on seed 14: ... FAILED test_project.py::test_estimate_on_a_second_participant_is_also_a_maximum' and 'run_graders E3: FAIL (reference 49/50 seeds, slowest 18.2 s)', EXIT 1. Round-11 PASSED; the round-12 reference change (_maximise raises at a stall or a non-converged search, reference.py:274-287) makes seed 14's second participant fail.",
         fix="Either make the reference converge on seed 14's second participant (the 9 non-gradable seeds of 0-399 are listed in row ref-suite-fails-generator-seeds), or change the gate and project.html:367 ('a pass on seeds 0 to 49') so that seed 14 is named as non-gradable by the reference. Then re-run run_graders 0-49."),
    dict(id="gate-collect-46", check="pytest --collect-only test_project.py equals the page's check count (project.html:213 says 50)", location="course/modules/E/E3/grader/test_project.py; project.html:213", status=P,
         evidence="ledgers/E3/scripts/E3-d-r12/collect_only_r12.out: '50 tests collected'. project.html:213 states 'runs 50 checks'. (Row id kept from round 9; the count is now 50.)"),
    dict(id="gate-reference-seed0", check="reference.py as elicit.py, QF_SEED=0, pytest --assert=plain -W error (full suite)", location="course/modules/E/E3/grader/reference.py", status=P,
         evidence="run_suite.sh reference.py 0: '50 passed in 14.35s', EXIT=0 (ledgers/E3/scripts/E3-d-r12/out/scans/suite_scan_0_399.txt line 'seed=0 EXIT=0')."),
    dict(id="gate-starter-fails", check="starter.py as elicit.py must fail the suite", location="course/modules/E/E3/grader/starter.py", status=P,
         evidence="run_suite.sh starter.py 0: '48 failed, 2 passed', EXIT=1."),
    dict(id="gate-ruff", check="ruff check and ruff format --check on grader/ and tests/labs/E3", location="course/modules/E/E3/grader; tests/labs/E3", status=P,
         evidence="ledgers/E3/scripts/E3-d-r12/ruff_check.out: 'All checks passed!' and '15 files already formatted', EXIT 0."),
    dict(id="gate-mypy-strict-grader", check="mypy --strict on the grader (reference, instance, starter; and test_project.py with elicit.py)", location="course/modules/E/E3/grader/", status=P,
         evidence="ledgers/E3/scripts/E3-d-r12/mypy_grader_strict.out: 'Success: no issues found in 3 source files', EXIT 0; mypy --strict test_project.py elicit.py instance.py: 'Success: no issues found in 3 source files'."),
    dict(id="gate-mypy-repo", check="mypy --no-incremental (repository, strict)", location="repository", status=P,
         evidence="ledgers/E3/scripts/E3-d-r12/mypy_repo.out: 'Success: no issues found in 385 source files', EXIT 0."),
    dict(id="gate-verify-refs-offline", check="tools/verify_refs.py --offline", location="references/references.json", status=P,
         evidence="ledgers/E3/scripts/E3-d-r12/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', EXIT 0. The live run was not made by this verifier (see notes)."),
    dict(id="gate-pytest-relevant", check="pytest tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_labs.py -k E3", location="project.html exemplars and lab twins", status=P,
         evidence="ledgers/E3/scripts/E3-d-r12/pytest_relevant.out: 15 passed (dots), EXIT 0."),
    dict(id="gate-mutate-existing-112", check="tools/mutate_graders.py --unit E3 --seeds 0-9 over every mutant file present at its start (161 files)", location="ledgers/E3/mutants/", status=F,
         evidence="ledgers/E3/scripts/E3-d-r12/mutate_E3_0-9.out: 'mutate_graders E3: FAIL (158/161 killed)'. Survivors: r11_03 (gamma clamped at 0.999; no page sentence states a gamma upper clamp and no participant the suite can draw has gamma_hat above 0.999: max over own and second participants of seeds 0-399 is 0.9864, scan in out/scans and max_gamma_scan.py), r12d_01 (killed on seeds 14 and 108, outside the window), r12d_04 (killed on seed 108, outside the window; seed 14 passes it).",
         fix="r12d_01 and r12d_04 are killed only by seeds outside the window 0-9. Add a fixed (seed-independent) fixture for the stalled search of seed 108's own participant (as LOW_KAPPA and LARGE_LAMBDA are fixed), so the suite fails a search that returns a non-stationary point without depending on the seed. The gamma-clamp mutant r11_03 is not a stated behaviour and is not a FAIL on its own."),
    dict(id="gate-mutants-count", check="at least 3 mutants and student-error mutants in the ledger", location="ledgers/E3/mutants/", status=P,
         evidence="ledgers/E3/mutants/*.py: 165 files (161 at the mutate run's start plus 4 r12v written by this verifier: r12v_01..04, run on seed 0 each, all killed)."),
    # ---- mutants (round-11 ids)
    dict(id="mut-r11d-01-identification-reads-only-the-a-lotteries", check="student-error mutant (loss aversion accepted only from A-side mixed lotteries) must be killed", location="ledgers/E3/mutants/r11d_01_identification_reads_only_the_a_lotteries.py", status=P,
         evidence="ledgers/E3/scripts/E3-d-r12/mutate_E3_0-9.out: KILLED (seed 0 on test_estimate_accepts_a_mixed_lottery_on_the_b_side_alone)."),
    dict(id="mut-r11d-02-newton-stops-on-likelihood-gain", check="student-error mutant (maximiser stops when one Newton step gains < 1e-9 in log-likelihood) must be killed", location="ledgers/E3/mutants/r11d_02_newton_stops_when_the_likelihood_gain_is_below_1e9.py", status=P,
         evidence="Round-11 FAIL (survived seeds 0-9). Now KILLED on seed 0 by test_estimate_on_a_fixed_26_response_participant_is_a_maximum (run_suite.sh, 'FAILED ... 1 failed, 49 passed'). Caveat: that kill is by the fixed-26 test (row grader-fixed-26-boundary-observed-information)."),
    dict(id="mut-r11d-03-crra-final-wealth-minus-prize", check="student-error mutant (CRRA final wealth = wealth minus prize) must be killed", location="ledgers/E3/mutants/r11d_03_crra_final_wealth_is_wealth_minus_each_prize.py", status=P,
         evidence="ledgers/E3/scripts/E3-d-r12/mutate_E3_0-9.out: KILLED (seed 0)."),
    dict(id="mut-r11d-04-twelve-response-lab3-table", check="student-error mutant (estimate returns the Lab 3 table for any 12-response questionnaire) must be killed", location="ledgers/E3/mutants/r11d_04_twelve_response_questionnaire_returns_the_lab3_table.py", status=P,
         evidence="Round-11 FAIL (survived seeds 0-9). Now KILLED on seed 0 by test_estimate_on_the_b_side_twelve_response_set_is_a_maximum (run_suite.sh, '1 failed, 49 passed')."),
    dict(id="ref-suite-fails-generator-seeds", check="2.6 autograder: the page's statement on generator seeds 0-399 (nine seeds not gradable by the reference) is exact", location="course/modules/E/E3/project.html:211, 213; grader/reference.py:274-287", status=P,
         evidence="Full suite per seed, 0-399, reference.py as elicit.py (out/scans/suite_scan_0_399.txt): 391 EXIT=0; the failing seeds are exactly {14, 89, 110, 235, 373} (second participant fails) and {108, 157, 165, 269} (own participant fails), the nine seeds the page names. Estimate-level scan (out/scans/scan_est_*.out) gives the same nine. The page's mechanism claims hold: seed 157 stops at a point where -H is not PD (Cholesky fails) with score (3.2e-3, -5.4e-2, 1.9e-4); seeds 108, 165, 269 stop with score above 1e-5 (instrumented copy, scripts/probe_failing_seeds_final_point.py). The own participant of 14, 89, 110, 235, 373 is fine (scan). Not measured: seeds 400 and above, which a browser seed (31-bit, FNV-1a of the workspace ID) can take."),
    dict(id="mut-d10-01-identification-reads-only-b", check="student mutant: identification counts a mixed lottery only on the B side", location="ledgers/E3/mutants/d10_01_identification_reads_only_the_b_lotteries.py", status=P,
         evidence="ledgers/E3/scripts/E3-d-r12/mutate_E3_0-9.out: KILLED (seed 0)."),
    dict(id="grader-large-lambda-docstring", check="grader docstring for the seed-49 test is true", location="course/modules/E/E3/grader/test_project.py:664-668", status=P,
         evidence="Lines 1-900 of test_project.py byte-identical since ccaeeaf (git diff ccaeeaf 329c1d7 starts at line 903). Seed 49 reference estimate: lambda_hat 20.6864 (run in se49.py with QF_SEED=49), above 10 as the docstring says."),
    dict(id="exemplar-word-count-B", check="project.html claim of the memo-text word counts (Exemplar B 450)", location="course/modules/E/E3/project.html:648 (claim); exemplar-b memo", status=P,
         evidence="Recounted from the page with a stdlib parser (tags removed with and without spacing): exemplar-a memo 117 words, exemplar-b memo 450 words (ad hoc script, same counts both ways)."),
    dict(id="exemplar-word-count-A", check="word count of Exemplar A memo text", location="course/modules/E/E3/project.html:648", status=P,
         evidence="Recount: 117 words (see exemplar-word-count-B). The Exemplar A instrument sentence changed (same 14 words)."),
    dict(id="grading-mode-48-checks", check="the count of checks on the page equals the collect-only count (row id kept from round 11)", location="course/modules/E/E3/project.html:213; grader/test_project.py", status=P,
         evidence="project.html:213 now says 'runs 50 checks'; collect-only = 50 (collect_only_r12.out)."),
    dict(id="grading-mode-tolerance-phrases", check="the tolerance sentences of project.html:213 match the tests", location="course/modules/E/E3/project.html:213; grader/test_project.py", status=P,
         evidence="Constants read from the suite: score 2e-5 (test_project.py:581, 684, 957), local-maximum 0.1 percent and 1e-9 (591, 598), loglik 1e-7 (554, 631, 674, 947), SE 10 percent, recovery 4 SE and 47 of 50 (601-614), dominance one cent (DOMINANCE_SLACK = 1, line 1242). All match the sentences of line 213."),
    dict(id="lab3-hypothesis-and-twin", check="Lab 3 hypothesis and the instruction 'replace the body of the function estimate ... keep m'", location="course/modules/E/E3/project.html:395-402, 417-606; tests/labs/E3/lab-E3-project-3.py", status=P,
         evidence="run_labs E3 PASS; page code equals twin (run_labs); twin runs under python -I -W error (exit 0); instruction lines 395-402 unchanged by the delta."),
    dict(id="ladder-skill-checks-claim", check="ladder text matches index.html", location="course/modules/E/E3/project.html:42; index.html:142", status=P,
         evidence=carried("project.html:42 and index.html not in the round-12 delta (git diff names only project.html, grader and lab twins in E3 slice files).")),
    dict(id="lab1-inputs-notation", check="Lab 1 inputs named on the page equal the twin constants", location="course/modules/E/E3/project.html:53; tests/labs/E3/lab-E3-project-1.py", status=P,
         evidence=carried("lab-E3-project-1.py unchanged; run_labs PASS and twin isolation exit 0 this round.")),
    dict(id="nearest-cent-docstring-lab1", check="nearest-cent statement of Lab 1", location="course/modules/E/E3/project.html:74; tests/labs/E3/lab-E3-project-1.py", status=P,
         evidence=carried("project.html:74 and lab-E3-project-1.py unchanged in the delta; run_labs PASS.")),
    dict(id="grader-dominance-sentence", check="project.html:213 dominance sentence (one cent) matches the tests", location="course/modules/E/E3/project.html:213; grader/test_project.py:1242, 1245-1290", status=P,
         evidence="The dominance sentence is byte-identical in the delta; DOMINANCE_SLACK = 1 cent (test_project.py:1242) used in _engine_respects (line 1285-1287); the first- and second-order tests pass for the reference (suite, seed 0)."),
    dict(id="grader-tolerances-vs-page", check="project.html:213 tolerances match the suite's constants and checks", location="course/modules/E/E3/project.html:213; grader/test_project.py", status=P,
         evidence="See grading-mode-tolerance-phrases (same constants re-read this round)."),
    dict(id="grader-local-max-kink-claim", check="docstring of the local-maximum test", location="course/modules/E/E3/grader/test_project.py:586-588", status=P,
         evidence=carried("lines 586-588 byte-identical; the local-maximum test passes for the reference on seed 0 and on 391 seeds of 0-399.")),
    dict(id="identification-convention-zero-prize", check="identification convention statement (lambda-free CE without a gain or without a loss)", location="course/modules/E/E3/project.html:223; grader/test_project.py", status=P,
         evidence=carried("project.html:223 unchanged.")),
    dict(id="models-definition-change", check="Models convention matches L06 Definitions 1.2-1.3 and reference.py", location="course/modules/E/E3/project.html:220; grader/reference.py:64", status=P,
         evidence=carried("project.html:220 and reference.py:64 unchanged in the delta (the reference delta is at lines 20-23 and 270-287).")),
    dict(id="questionnaire-fraction-contract", check="questionnaire probability contract and the engine's Fraction reading", location="course/modules/E/E3/project.html:207, 273", status=P,
         evidence=carried("project.html:207 and 273 unchanged in the delta.")),
    dict(id="questionnaire-grammar", check="export refusal grammar", location="course/modules/E/E3/project.html:340", status=P,
         evidence=carried("project.html:340 unchanged in the delta.")),
    dict(id="questionnaire-js-browser", check="questionnaire JS behaviour as described", location="course/modules/E/E3/project.html:245-353", status=P,
         evidence=carried("project.html:245-353 unchanged in the delta; not re-run in a real browser click-through (see notes).")),
    dict(id="questionnaire-js-syntax", check="inline questionnaire script parses", location="course/modules/E/E3/project.html:249-355", status=P,
         evidence=carried("project.html:249-355 unchanged in the delta; page_smoke loads the page with zero console errors in each run.")),
    dict(id="hours-arithmetic", check="hours split sums to the declared project hours and the hub", location="course/modules/E/E3/project.html:33, 362-370; index.html:29", status=P,
         evidence="1 + 1 + 3 + 4 + 3 + 2 = 14 (project.html:362-370, lines unchanged); the hub figure 14 of 70 unchanged. The deliverable sentence in the same table (line 367, 'a pass on seeds 0 to 49') is a separate row."),
    dict(id="hours-estimate-30pct", check="2.6 hours: the verifier's own estimate is within 30 percent of the declared 14 hours", location="course/modules/E/E3/project.html:362-370", status=P,
         evidence=carried("hours table lines unchanged; the verifier's own estimate is unchanged (design targets are rulings, not re-estimated).")),
    dict(id="exemplar-b-model-identification", check="Exemplar B identification statements", location="course/modules/E/E3/project.html:707, 719", status=P,
         evidence=carried("lines 707 and 719 unchanged (the delta changes line 711 and 714 only in exemplar B's annotations).")),
    dict(id="exemplar-b-interpretation", check="Exemplar B interpretation statements", location="course/modules/E/E3/project.html:731, 742", status=P,
         evidence="Line 731 now reads 'largest score component at the estimate is 4.00e-10 (Lab 3)'; Lab 3 prints 'largest score component at the estimate: 4.00e-10' and gamma_hat 0.6352, lambda_hat 6.1503, kappa_hat 2.0201, se 0.32/9.59/1.86, log-likelihood -7.1445 (run lab-E3-project-3.py); lambda se 9.59 > lambda_hat 6.15 as stated. Line 742 unchanged."),
    dict(id="exemplar-scores-annotations", check="exemplar official scores and annotations match the rubric", location="course/modules/E/E3/project.html:648-763 (annotation at line 714)", status=F,
         evidence="The exemplar-b C1 annotation (project.html:714, 'Misses C1 level 4: the memo does not list all twelve pairs and does not show the mixed-sign pairs; the instrument file does.') contradicts the memo at line 709: 'Pair 3 sets 18800 cents ... both lotteries mix a gain and a loss' and 'Eleven of the twelve pairs contain a mixed lottery'. Re-derived from tests/labs/E3/lab-E3-project-3.py by scripts/lab3_data_check.py: pair 3 has both lotteries mixed; 11 mixed pairs; prizes -18700..19000. The scores data-scores 3,3,4,3,3 and 2,2,1,2,1 match the official-scoring lines.",
         fix="Edit project.html:714 so the level-4 miss names only what the memo lacks: 'Misses C1 level 4: the memo does not list all twelve pairs; the instrument file does.' Keep the level-4 descriptor at line 638 consistent."),
    dict(id="notation", check="every symbol vs notation/notation.json (T, R*, Phi, gamma_3, ... never reused with another meaning)", location="course/modules/E/E3/project.html (math)", status=P,
         evidence="notation/notation.json lists 8 symbols (\\gamma_3, \\gamma_4 among them), none of which the E3 page uses; the E3 page uses bare \\gamma, \\lambda, \\kappa, \\zeta, \\hat\\lambda, w, which are not registered and do not collide with a registered symbol."),
    dict(id="scope-words", check="scope words (only, all, every, any, exactly) carry their computation", location="course/modules/E/E3/project.html:213 ('an estimate that returns one fixed table for any twelve responses fails it'), 221-223, 683, 695, 719", status=F,
         evidence="Probe scripts/constant_table_probe_mk.py: an elicit.py whose estimate returns, for every input, the reference's estimate of the B-side twelve-response set passes test_estimate_on_the_b_side_twelve_response_set_is_a_maximum ('1 passed'). So 'an estimate that returns one fixed table for any twelve responses fails it' (line 213) is true only for tables that are not that set's own maximum. The other scope words checked (every, all, exactly) carry their computation as before.",
         fix="Reword line 213: 'an estimate that returns a table chosen in advance fails it unless that table is this set's own maximum' (or 'and fails the suite on the fixed 26-response participant'). Re-check the sentence after the edit."),
    dict(id="process-words", check="no process words in learner text", location="course/modules/E/E3/project.html", status=P,
         evidence="grep of the added lines (git diff ccaeeaf 329c1d7 -- project.html) for round, verif*, builder, audit, todo, draft, tbd, pending, review, architect, gate, ledger: no matches ('our' matches only 'your'/'four')."),
    dict(id="concept-links-definitions", check="concept links resolve to their definitions", location="course/modules/E/E3/project.html:53, 213, 220, 222", status=P,
         evidence="The 3 concept links on the page (certainty-equivalent, crra-utility, first-order-stochastic-dominance, prospect-theory x2) are unchanged; the anchor id=\"def-first-order-stochastic-dominance\" exists in course/modules/E/E3/L04.html (count 1)."),
    dict(id="fixed-case-data-claims", check="Exemplar B data claims: prize range, prizes per lottery, quoted pairs, and the mixed count", location="course/modules/E/E3/project.html:707 (Exemplar B instrument)", status=P,
         evidence="scripts/lab3_data_check.py on tests/labs/E3/lab-E3-project-3.py: 12 answers; prizes -18700..19000; 2 or 3 prizes per lottery; 11 mixed pairs; pair 0 A (6200 p 9/10, -15100 p 1/10), B three prizes; pair 3 A (18800 p 3/4, -12500 p 1/4), B (16500 p 2/5, -17700 p 3/5), both mixed. All match the memo."),
    dict(id="grader-instances-sample-20", check="2.6 autograder item 2: 20 sampled seeds give valid instances that differ materially", location="course/modules/E/E3/grader/instance.py (make_instance)", status=P,
         evidence=carried("instance.py unchanged; run_graders check_instances passed in the run (no 'not deterministic' or identical-instance FAIL lines).")),
    dict(id="dag-unlinked-names", check="MLE, Hessian and Fisher-type terms are prose (Architect decision)", location="course/modules/E/E3/project.html", status=P,
         evidence="The delta adds no concept link (grep of +/- lines for 'concept': only the existing line 213 link text). Architect decisions (plans/E3-build-plan.md:669): concepts outside the closure are plain prose."),
    dict(id="citations-reading", check="reading section and cited keys match the lessons", location="course/modules/E/E3/project.html:782-789; L02.html:616; L05.html", status=P,
         evidence=carried("project.html:782-789 unchanged; verify_refs --offline 0 problems.")),
    dict(id="rubric-levels-vs-annotations", check="every annotation names a descriptor of its stated level", location="course/modules/E/E3/project.html:611-617, 648-763", status=F,
         evidence="Same defect as exemplar-scores-annotations: the exemplar-B level-4 annotation (project.html:714) says the memo 'does not show the mixed-sign pairs', but the memo (line 709) shows pair 3 with both lotteries mixed. The C1 level-4 descriptor (line 638) now reads 'shows the mixed-sign pairs'.",
         fix="As for exemplar-scores-annotations: edit project.html:714; the annotation must not claim an absence the memo contradicts."),
    dict(id="lab1-prose-numbers", check="Lab 1 prose numbers", location="course/modules/E/E3/project.html:57, 148", status=P,
         evidence=carried("project.html:57 and 148 unchanged; run_labs PASS for Lab 1.")),
    dict(id="lab2-prose-numbers", check="Lab 2 prose numbers", location="course/modules/E/E3/project.html:153, 197", status=P,
         evidence=carried("project.html:153 and 197 unchanged; run_labs PASS for Lab 2.")),
    dict(id="lab3-prose-numbers", check="Lab 3 prose numbers", location="course/modules/E/E3/project.html:395, 607-614, 708, 719, 731", status=P,
         evidence="Lab 3 output (run lab-E3-project-3.py): answers 12; mixed-sign answers 11; gamma_hat 0.6352; se_gamma 0.32; lambda_hat 6.1503; se_lambda 9.59; kappa_hat 2.0201; se_kappa 1.86; log-likelihood -7.1445; largest score component 4.00e-10; domain True. The page's printed expected block (lines 611-617) is identical to the output; prose at 607-614 and 731 matches."),
    dict(id="lab-twins-isolated", check="each project twin runs alone under python -I -W error", location="tests/labs/E3/lab-E3-project-1..3.py", status=P,
         evidence="python -I -W error on each twin: EXIT 0 (lab-E3-project-1, -2, -3)."),
    dict(id="lab-page-code-equals-twin", check="page code equals its twin (Lab 2 is a completion lab)", location="course/modules/E/E3/project.html Labs 1-3", status=P,
         evidence="run_labs E3 --page project PASS (3/3)."),
    dict(id="lab-expected-equals-output", check="expected block equals the twin's output", location="course/modules/E/E3/project.html Labs 1-3", status=P,
         evidence="run_labs E3 PASS; Lab 3 expected block (project.html:611-617) equals the twin's printed output line by line."),
    dict(id="instance-docstring-claims", check="instance.py docstring claims", location="course/modules/E/E3/grader/instance.py:1-33, 45-52, 148-261", status=P,
         evidence=carried("instance.py unchanged in the delta.")),
    dict(id="grader-messages-never-print-answer", check="failure messages name the property and never print an answer", location="course/modules/E/E3/grader/test_project.py:45-64, 251-285 and the new tests 903-1010", status=P,
         evidence="New tests use expect() with property messages only (test_project.py ~lines 934-968); the reference's RuntimeError texts name the step, no values. Pytest run with --assert=plain shows no values."),
    dict(id="grader-gamma0-exact-convention", check="gamma = 0 exact half-cent convention", location="project.html:221; grader/test_project.py:144-149; grader/reference.py", status=P,
         evidence=carried("project.html:221, test_project.py:144-149 unchanged; the suite passes the reference on 391 seeds.")),
    dict(id="grader-seed49-se-docstring-numbers", check="seed-49 standard-error numbers in the docstring", location="grader/test_project.py:1163-1175 (moved by +95 lines; docstring unchanged)", status=P,
         evidence="Recomputed with the suite's helpers at QF_SEED=49 (se49.py): se_gamma 0.09474 (h=1e-5), 0.07983 (h=1e-6); se_lambda 135.0541, 97.6747 (-27.7 percent); gamma change -15.7 percent. All match the docstring."),
    dict(id="grader-allA-docstring", check="all-A degenerate-set numbers in the docstring", location="grader/test_project.py:1003-1010 (moved from 903-910; text unchanged)", status=P,
         evidence=carried("docstring text byte-identical; the all-A test runs and passes for the reference (suite, seed 0).")),
    dict(id="grader-seed30-kappa-below-one", check="fixed participant seed 30 has kappa below 1", location="grader/instance.py; grader/test_project.py:36", status=P,
         evidence=carried("test_project.py:36 unchanged.")),
    dict(id="grader-seed49-lambda-above-ten", check="fixed participant seed 49 has lambda_hat above 10", location="grader/test_project.py:37, 664-694", status=P,
         evidence="Reference lambda_hat 20.6864 at seed 49 (se49.py output)."),
    dict(id="grader-recovery-47-of-50", check="recovery threshold", location="grader/test_project.py:601-616", status=P,
         evidence="The reference passes test_estimate_recovers_... in the run_graders 0-49 run (only seed 14 fails, on test_estimate_on_a_second_participant_is_also_a_maximum; ledgers/E3/scripts/E3-d-r12/run_graders_E3_0-49.out) and on seed 0 (50 passed)."),
    dict(id="grader-second-participant-and-clamp", check="second participant and the clamp checks", location="grader/test_project.py:619-642; instance.py", status=P,
         evidence=carried("test_project.py:619-642 unchanged; the suite is run on the reference for 400 seeds (out/scans/suite_scan_0_399.txt).")),
    dict(id="convention-whole-cents", check="whole-cent convention", location="project.html:221; grader/reference.py:71-73, 118-128", status=P,
         evidence=carried("project.html:221 and reference.py:71-73, 118-128 unchanged.")),
    dict(id="concept-links-definitions-carried", check="concept links at project.html:205, 207", location="course/modules/E/E3/project.html:205, 207", status=P,
         evidence=carried("lines 205 and 207 unchanged.")),
    dict(id="rung1-lab-answers-claim", check="Lab 1 prints what project.html:44 says", location="course/modules/E/E3/project.html:44; tests/labs/E3/lab-E3-project-1.py", status=P,
         evidence=carried("project.html:44 unchanged; run_labs PASS for Lab 1.")),
    dict(id="relaxed-test-kills-unchanged", check="local-maximum test (lambda move restored) kills the lambda-frozen mutants", location="course/modules/E/E3/grader/test_project.py:586-598", status=P,
         evidence="Mutate run: r9_01, r9_02, r9_03 KILLED (scripts/E3-d-r12/mutate_E3_0-9.out); test lines 586-598 unchanged."),
    dict(id="mut-r9-01-lambda-frozen-at-grid-value", check="student-error mutant", location="ledgers/E3/mutants/r9_01_lambda_frozen_at_its_grid_value.py", status=P,
         evidence="mutate_E3_0-9.out: KILLED (seed 0)."),
    dict(id="mut-r9-02-lambda-climbs-downhill", check="student-error mutant", location="ledgers/E3/mutants/r9_02_lambda_climbs_downhill.py", status=P,
         evidence="mutate_E3_0-9.out: KILLED (seed 0)."),
    dict(id="mut-r9-03-lambda-reported-as-its-log", check="student-error mutant", location="ledgers/E3/mutants/r9_03_lambda_reported_as_its_log.py", status=P,
         evidence="mutate_E3_0-9.out: KILLED (seed 0)."),
    dict(id="mut-r9-04-convergence-ignores-lambda", check="within-tolerance candidate (not a grader mutant; kept out of ledgers/E3/mutants)", location="ledgers/E3/scripts/E3-d-r9/within_tolerance/r9_04_convergence_ignores_lambda.py", status=P,
         evidence=carried("candidate file and its scripts unchanged; not counted as a mutant.")),
    dict(id="mut-d10-02-likelihood-uses-crra-ce", check="student mutant: the likelihood uses CRRA certainty equivalents", location="ledgers/E3/mutants/d10_02_likelihood_uses_crra_certainty_equivalents.py", status=P,
         evidence="mutate_E3_0-9.out: KILLED (seed 0)."),
    dict(id="mut-d10-03-estimate-drops-pure-responses", check="student mutant: the estimator drops responses with two pure lotteries", location="ledgers/E3/mutants/d10_03_estimate_drops_the_pure_responses_first.py", status=P,
         evidence="mutate_E3_0-9.out: KILLED (seed 0)."),
    dict(id="mut-e8-01-se-diagonal-only", check="student-error mutant", location="ledgers/E3/mutants/e8_01_se_from_inverse_of_the_diagonal_only.py", status=P,
         evidence="mutate_E3_0-9.out: KILLED."),
    dict(id="mut-e8-02-crra-zero-wealth-allowed", check="student-error mutant", location="ledgers/E3/mutants/e8_02_crra_allows_final_wealth_of_exactly_zero.py", status=P,
         evidence="mutate_E3_0-9.out: KILLED."),
    dict(id="mut-e8-03-prospect-loss-weight-on-gains", check="student-error mutant", location="ledgers/E3/mutants/e8_03_prospect_loss_weight_also_scales_the_gain_branch.py", status=P,
         evidence="mutate_E3_0-9.out: KILLED."),
    dict(id="mut-e8-04-prospect-adds-wealth", check="student-error mutant", location="ledgers/E3/mutants/e8_04_prospect_model_adds_wealth_to_each_prize.py", status=P,
         evidence="mutate_E3_0-9.out: KILLED."),
    dict(id="mut-e8-05-model-name-type-error", check="student-error mutant", location="ledgers/E3/mutants/e8_05_model_name_error_raises_type_error.py", status=P,
         evidence="mutate_E3_0-9.out: KILLED."),
    # ---- alternatives
    dict(id="alt-1-2-3-5-seeds-0-9", check="alternatives 1c, 2c, 3 (and 5) pass the full suite on seeds 0-9 (architect: five correct alternatives must pass)", location="ledgers/E3/scripts/E3-d-r10/alts/, E3-d-r11/alts/", status=F,
         evidence="Full suite, seed 0 (out/alts_s0/): alt1c_zoom_then_reference_newton: 1 failed (fixed-26: 'observed information is not positive definite'); alt2c_newton_fd1e-6_damped: 1 failed (same); alt3_nelder_mead_v2: 1 failed (same). Their maximisers return points with max score 3.6e-9 to 1e-7 (probe26_alternatives.py: gamma_hat 1e-7 to 1e-16), so they are correct stationary-point solvers rejected by the fixed-26 check. alt5_exp_log_float: 50 passed. alt2 (4 fails), alt2b (4 fails), alt3_nelder_mead (4 fails) are not correct at the given seeds. Seeds 1-9 not run for these (see notes).",
         fix="Fix the fixed-26 fixture (row grader-fixed-26-boundary-observed-information); then re-run alt1c, alt2c, alt3_v2, alt4b on seed 0 and seeds 1-9."),
    dict(id="alt-4-bisection-seeds-0-9", check="alternative 4b: prospect CE by bisection to full precision, then the half-up rule passes seeds 0-9", location="ledgers/E3/scripts/E3-d-r10/alts/alt4b_bisection_full_precision/elicit.py", status=F,
         evidence="Full suite, seed 0: alt4b_bisection_full_precision: 1 failed, fixed-26 (observed information not PD); the rest pass (49). Probe: gamma_hat 6.9e-12, max score 2.5e-9 (probe26_alternatives.py), a correct stationary point. Seeds 1-9 not run.",
         fix="As for alt-1-2-3-5-seeds-0-9."),
    dict(id="alt-6-finite-difference-step-1e-4", check="alternative 6 (FD step 1e-4 in the optimiser, Hessian and standard errors)", location="ledgers/E3/scripts/E3-d-r10/alts/alt6_fd_step_1e-4/elicit.py", status=P,
         evidence="Full suite, seed 0: '50 passed in 15.97s', EXIT 0. Seeds 1-9 not run in this round (see notes)."),
    dict(id="alt-7-armijo-newton-seeds-0-9", check="alternative 7 (round 11): finer grid, damped Newton with Armijo backtracking", location="ledgers/E3/scripts/E3-d-r11/alts/alt7_armijo_newton/elicit.py", status=P,
         evidence="Full suite, seed 0: '50 passed in 365.23s', EXIT 0 (out/alts_s0/alt7_armijo_newton.s0.out). Seeds 1-9 not run in this round (see notes)."),
    dict(id="alt-lambda-local-max-restored-on-alternatives", check="the lambda move in the local-max test holds on the alternatives", location="course/modules/E/E3/grader/test_project.py:586-598", status=P,
         evidence="The local-maximum test passes for alt5_exp_log_float, alt6_fd_step_1e-4 and alt7_armijo_newton on seed 0 (full suite). Other alternatives fail other named tests (above)."),
    dict(id="alt-cross-seed-likelihood", check="alternatives' likelihood vs the reference on seeds 0-49", location="course/modules/E/E3/grader/test_project.py:619-642", status=P,
         evidence="test_second_participant likelihood checks pass for alt5_exp_log_float, alt6, alt7 on seed 0; the cross-seed likelihood test passes for those three."),
    # ---- new round-12 rows
    dict(id="grader-fixed-26-boundary-observed-information", check="fixed 26-response participant: the estimate passes the maximum checks, including the observed-information positive definiteness the estimate requires", location="course/modules/E/E3/grader/test_project.py:903-1000 (FIXED_26_ANSWERS, test_estimate_on_a_fixed_26_response_participant_is_a_maximum); reference.py:303-306", status=F,
         evidence="Reference estimate on FIXED_26_ANSWERS: gamma_hat 5.0e-8 (xi0 = -16.81), score ~5e-8, observed-information zeta entry -1.776357e-5 = -2*ulp(f0)/h^2 with f0 = -5.27973882568198 (ulp 8.88e-16), so its sign is set by 2 units of rounding (scripts/noise.py output; the same run shows the two Hessian entries at +/- h). CPython: pass for PYTHONHASHSEED 0..19 (scripts). Pyodide (page): fails deterministically on every run (10 of 10 browser grader runs). Correct alternatives end at other points of the same flat boundary (gamma_hat 1e-7 to 1e-16, xi1 up to 31.5) with score below 4e-8 and the same PD failure (alt1c, alt2c, alt3_v2, alt4b; scripts/probe26_alternatives.py). The test therefore demands a PD observed information at a point the open domain does not attain (gamma -> 0), which the page does not state.",
         fix="Replace the fixture by a participant whose MLE is interior (gamma_hat away from 0, lambda and kappa identified), or assert only the score and local-maximum checks on it. Keep the 'search that stops early fails' property (r11d_02 and r12v_01 are killed by it on seed 0; keep them killed)."),
    dict(id="hours-table-pass-seeds-0-49", check="project.html:367: 'a pass on seeds 0 to 49 of the autograder' as a deliverable is attainable with the course's own solution", location="course/modules/E/E3/project.html:367; project.html:211 ('Nine of the seeds 0 to 399 are not gradable by the course's own solution')", status=F,
         evidence="The reference fails seed 14 (second participant) in the same suite (run_graders 0-49 FAIL, row gate-run-graders-seeds-0-49); project.html:211 and 213 say seed 14 is not gradable by the course's own solution. The deliverable of line 367 is therefore unattainable with the course's own solution on seed 14.",
         fix="Change line 367 to 'a pass on seeds 0 to 49 of the autograder, except seed 14, which the course's own solution does not pass' (or fix the reference so seed 14 passes, then keep the sentence)."),
    dict(id="architect-five-alternatives-pass", check="architect decision (plans/E3-build-plan.md:669): five alternative correct implementations pass the grader", location="ledgers/E3/scripts/E3-d-r10/alts/, E3-d-r11/alts/; project.html suite", status=F,
         evidence="On seed 0 (full suite), the alternatives that are correct stationary-point solvers and pass every test: alt5_exp_log_float, alt6_fd_step_1e-4, alt7_armijo_newton (3). Four more correct solvers (alt1c, alt2c, alt3_nelder_mead_v2, alt4b) fail only the fixed-26 check (row grader-fixed-26-boundary-observed-information). Fewer than five pass.",
         fix="Fix the fixed-26 fixture (row grader-fixed-26-boundary-observed-information), then count the passing alternatives on seeds 0-9."),
]

VERIFIED_AT = datetime.now(UTC).replace(microsecond=0).isoformat()


def mutants_from_log() -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    pattern = re.compile(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$")
    for line in LOG.read_text(encoding="utf-8").splitlines():
        m = pattern.match(line)
        if not m:
            continue
        status, name, desc, killed = m.groups()
        killed_by = None if killed.strip() == "None" else killed.strip()
        found.append({"name": name.removesuffix(".py"), "description": desc.strip(), "killed_by": killed_by})
    return found


def main() -> None:
    mutants = mutants_from_log()
    # the mutate run's survivors, with their kills outside the window (see the gate row)
    extra_kill = {
        "r12d_01_search_failure_returns_the_grid_start": "test_estimate_on_a_second_participant_is_also_a_maximum (seed 14; outside the 0-9 window)",
        "r12d_04_stalled_search_returned_without_the_score_check": "test_score_is_zero_at_the_estimate (seed 108; outside the 0-9 window)",
    }
    for m in mutants:
        if m["name"] in extra_kill and m["killed_by"] is None:
            m["killed_by"] = extra_kill[str(m["name"])]
            m["note"] = "survived the mutate window 0-9; killed by a seed outside it (see gate-mutate-existing-112)"
        if m["name"] == "r11_03_gamma_hat_clamped_below_one_minus_1e3":
            m["note"] = "survives 0-9; no page sentence states a gamma upper clamp; no participant the suite draws reaches gamma_hat > 0.999 (max 0.9864 over 0-399)"
    r12v = {
        "r12v_01_five_newton_steps_then_returns_the_point_reached": "test_estimate_recovers_the_true_parameters_within_four_standard_errors_on_47_of_50_seeds (seed 0; run separately, outside the mutate run)",
        "r12v_02_search_stops_once_every_score_component_is_below_one_ten_thousandth": "test_score_is_zero_at_the_estimate (seed 0; run separately)",
        "r12v_03_b_response_contributes_log_p_of_a": "test_log_likelihood_matches_oracle_at_the_true_parameters (seed 0; run separately)",
        "r12v_04_reported_gamma_is_one_minus_gamma": "test_reported_log_likelihood_is_the_likelihood_at_the_estimate (seed 0; run separately)",
    }
    for name, kill in r12v.items():
        path = ROOT / "ledgers/E3/mutants" / f"{name}.py"
        doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or ""
        mutants.append({"name": name, "description": doc.splitlines()[0], "killed_by": kill, "note": "written by this verifier"})
    rows = [dict(r) for r in ROWS]
    for r in rows:
        if r["status"] != P:
            r.setdefault("fix", "")
        else:
            r.pop("fix", None)
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in (P, F)}
    fragment = {
        "unit": "E3",
        "slice": "d",
        "round": 12,
        "verifier": "Claude Haiku 5.5, independent verifier for E3-d, round 12 (did not build E3; read verifier-rules.md and VERIFIER_RULES.md)",
        "pin": "329c1d7feac5479403c351e64587c867278452cc",
        "base": "ccaeeaf (round-11 pin); delta ccaeeaf..329c1d7 read hunk by hunk for project.html, grader/reference.py, grader/test_project.py, tests/labs/E3/lab-E3-project-3.py, and the seven r11 mutant files",
        "checkout": "/Users/billyribeiro/.fanout/wt/verifyD12-E3-d",
        "scratch": "/Users/billyribeiro/.fanout/scratch/E3-d-r12",
        "verified_at": VERIFIED_AT,
        "verdict": "FAIL",
        "rows": rows,
        "mutants": mutants,
        "registry_flags": [],
        "freshness_flags": [],
        "notes": NOTES,
        "summary": f"E3-d round 12 at 329c1d7: {len(rows)} rows: {counts[P]} PASS, {counts[F]} FAIL, 0 UNVERIFIABLE. Mutants: {len(mutants)} listed (161 at the mutate run's start + r12v_01..04), killed {sum(1 for m in mutants if m.get('killed_by'))}; r11_03 is the one survivor with no stated behaviour.",
    }
    OUT.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote", OUT, counts, len(mutants))


NOTES = (
    "Round 12 (E3-d) at 329c1d7 (delta ccaeeaf..329c1d7 read in full for the slice: project.html hunks at lines 211, 213, 563-606 (Lab 3 code and output), 633-638 (rubric C1), 656 (Exemplar A), 714 (Exemplar B C1 annotation), 733 (Exemplar B estimates); grader/reference.py (_maximise stall and non-convergence branches, lines 274-287, and _STATIONARY); grader/test_project.py lines 903-1000 (two fixtures: FIXED_26_ANSWERS and the B-side twelve-response set, two tests); tests/labs/E3/lab-E3-project-3.py (estimate and main); seven new mutant files (r11d/r11 series, byte-level 308-321 lines each). Lines of project.html outside the hunks, instance.py, starter.py and the lab twins 1-2 are byte-identical to the round-11 pin. Browser evidence: page_smoke for project run three times (49/50 each, random seeds) and browser_grader_seed.py on seeds 0, 117910760 (twice), 1313442603, 699963905 (49/50 each; the same test each time). Local CPython passes the same test under 20 PYTHONHASHSEED values. Suite scan 0-399 (full suite, 400 runs): 391 pass; the nine failing seeds equal the page's list. Mutate run (tools/mutate_graders.py --unit E3 --seeds 0-9, started first in the background): 158/161 killed. Four r12v mutants written by this verifier (make_r12v_mutants.py) and killed on seed 0. Alternatives: a runner (run_alts_r12.sh) was started for all 14 alternatives on seeds 0-9; the seed-0 full-suite results are complete for all 14 (out/alts_s0), seeds 1-9 are partial (out/alts_summary_partial.txt, still growing when this fragment was written; the runner could not be stopped by this verifier). Not checked: the live verify_refs run; a real click-through of the questionnaire in a browser; alternatives on seeds 1-9 for all but the first three (alt1 and the others are partial); the reference on seeds 400 and above (the browser can draw any 31-bit seed); the r12d_01..04 mutants were written by an earlier pass in this checkout (untracked) and were run by this verifier with run_suite.sh. Observation (not a row): on seed 49 the reference's estimate (lambda 20.69, log-likelihood -126.0315) is a local maximum; a stationary point at lambda about 7.22 has log-likelihood -125.93 (round-11 evidence), and the page calls the estimate maximum-likelihood while its checks are local (project.html:213)."
)


if __name__ == "__main__":
    main()
