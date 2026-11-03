"""Round-4 verifier (E3-d): writes ledgers/E3/E3-d.json (round 4) from the outputs saved in ledgers/E3/scripts/E3-d-r4/.

Statuses are the verifier's judgements, each backed by the named output file or script. Mutants are read from
mutate_E3_r4_final.out (the tool's own KILLED / SURVIVED lines at this pin, 89 mutant files).
Run from the checkout: .venv/bin/python ledgers/E3/scripts/E3-d-r4/write_fragment_E3-d-r4.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
D = "ledgers/E3/scripts/E3-d-r4"
PIN = "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b"

mutants = []
for line in (ROOT / D / "mutate_E3_r4_final.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+)\.py: (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    killed_by = None if killer.strip() == "None" else re.sub(r"\s+", " ", killer.strip())
    mutants.append({"id": name, "description": desc, "killed_by": killed_by})

R = []


def row(id_, check, location, status, evidence, fix=""):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)


# ---- gates -------------------------------------------------------------------------------------------------------
row("gate-check-dag", "tools/check_dag.py --unit E3", "course/modules/E/E3/*.html", "PASS",
    f"{D}/check_dag_E3.out: 'check_dag E3: PASS', EXIT 0 (run at {PIN}).")
row("gate-check-projects", "tools/check_projects.py --unit E3", "course/modules/E/E3/project.html", "PASS",
    f"{D}/check_projects_E3.out: 'check_projects E3: PASS', EXIT 0.")
row("gate-check-pages", "tools/check_pages.py --unit E3", "course/modules/E/E3/project.html", "PASS",
    f"{D}/check_pages_E3.out: 'check_pages E3: PASS', EXIT 0.")
row("gate-run-labs-project", "tools/run_labs.py --unit E3 --page project; then --unit E3", "project.html labs 1-3", "PASS",
    f"{D}/run_labs_project.out 'run_labs E3: PASS (3/3)'; {D}/run_labs_E3_all.out 'PASS (11/11)'.")
row("gate-run-graders-seeds-0-49", "tools/run_graders.py --unit E3 --seeds 0-49",
    "grader/reference.py, grader/test_project.py", "PASS",
    f"{D}/run_graders_E3_0_49_verifier.out: 'reference 50/50 seeds, slowest 13.7 s', EXIT 0.")
row("gate-collect-45", "pytest --collect-only grader/test_project.py", "grader/test_project.py; project.html:203", "PASS",
    f"{D}/collect_only_r4.out: '45 tests collected'; project.html:203 says 45 checks; 45 top-level def test_ (grep -c).")
row("gate-page-smoke-project", "tools/page_smoke.py --unit E3 --pages project", "course/modules/E/E3/project.html", "PASS",
    f"{D}/page_smoke_project.out: 'in-browser grader: All 45 tests pass on seed 941900901', 'page_smoke E3: PASS', EXIT 0.")
row("gate-mypy-strict", "mypy --no-incremental (repository configuration)", "repo", "PASS",
    f"{D}/mypy_strict.out: 'Success: no issues found in 331 source files', EXIT 0.")
row("gate-ruff-check", "ruff check . (repo)", "repo", "PASS",
    f"{D}/ruff_check.out 'All checks passed!', EXIT 0 (re-run repo-wide at {PIN}: 'All checks passed!').")
row("gate-ruff-format", "ruff format --check . (repo)", "ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py:3",
    "FAIL",
    f"{D}/ruff_format.out: '1 file would be reformatted, 473 files already formatted' (exit 1), at {PIN}. The file is "
    "outside E3-d; the same failure was recorded in round 3.",
    "Owner M3 runs ruff format on ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py; E3-d did not edit it.")
row("gate-pytest-page-memo-docs", "pytest tests/test_page_checks.py tests/test_memo_exemplars.py tests/test_docs_figures.py "
    "tests/test_labs.py tests/test_run_labs.py", "tests/", "PASS",
    f"{D}/pytest_pages_memo_labs.out: 380 passing tests (380 dots, no failures), 'EXIT 0'. (test_memo_exemplars.py covers S7 only; it "
    "does not check E3 exemplars.)")
row("gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json", "PASS",
    f"{D}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', EXIT 0. No reference was changed, so no live run was needed.")
row("gate-no-network-in-page", "grep and scan for network references", "course/modules/E/E3/project.html", "PASS",
    f"{D}/page_text_scans_r4.out (5): no URLs, no fetch/XHR/WebSocket/sendBeacon/window.open; Blob and "
    "URL.createObjectURL only (project.html:332-339); localStorage only in the head theme script (project.html:8).")
row("gate-mutate-tool-E3-existing", "tools/mutate_graders.py --unit E3 --seeds 0-9 (84 pre-existing mutants)",
    "ledgers/E3/mutants/", "PASS",
    f"{D}/mutate_E3_r4_final.out: all 84 pre-existing mutants KILLED (the 88/89 total includes them). "
    f"{D}/mutate_E3_seeds0-9.txt at {PIN} before the new files: 'PASS (84/84 killed)'.")
row("gate-mutants-r4-new-killed", "tools/mutate_graders.py --unit E3 --seeds 0-9 (new round-4 mutants e3d4_01..04)",
    "ledgers/E3/mutants/e3d4_01..04", "PASS",
    f"{D}/mutate_E3_r4_final.out: e3d4_01 killed by test_reported_log_likelihood_is_the_likelihood_at_the_estimate; "
    "e3d4_02 killed by test_probabilities_must_be_nonnegative_and_sum_to_exactly_one; e3d4_03 killed by "
    "test_crra_requires_wealth_plus_every_prize_to_stay_positive; e3d4_04 killed by "
    "test_estimate_recovers_the_true_parameters_within_four_standard_errors_on_47_of_50_seeds (seeds 0, 1 raise in estimate).")
row("gate-mutants-r3-new", "round-3 mutants e3d3v_01..04 re-run", "ledgers/E3/mutants/e3d3v_01..04", "PASS",
    f"{D}/mutate_E3_r4_final.out: all four KILLED (CRRA inverse, kappa key, estimate probability checks, Hessian forward differences).")
row("gate-mutants-count", "mutant count and killed count at this pin", "ledgers/E3/mutants/ (89 files)", "PASS",
    f"{D}/mutant_docstrings_r4.out: 89 mutant files; 88 KILLED, 1 SURVIVED (row mut-e3d4-05-reported-kappa-clamp).")
row("gate-mutants-docstrings", "first docstring line of every mutant names a student error", "ledgers/E3/mutants/*.py",
    "PASS", f"{D}/mutant_docstrings_r4.out: 'first-line problems: none' over 89 files.")

# ---- alternatives -------------------------------------------------------------------------------------------------
row("alt-1", "alternative 1: grid, compass search, Newton polish", "ledgers/E3/scripts/run_alternatives.py ALT1 (in ALTERNATIVES)",
    "PASS", f"{D}/alternatives_0-9_r4.out: 'alt1: PASS (10/10 seeds)'.")
row("alt-2", "alternative 2: grid and Newton", "ledgers/E3/scripts/run_alternatives.py ALT2",
    "PASS", f"{D}/alternatives_0-9_r4.out: 'alt2: PASS (10/10 seeds)'.")
row("alt-3", "alternative 3: grid, Nelder-Mead restarted, Newton polish", "ledgers/E3/scripts/run_alternatives.py ALT3",
    "PASS", f"{D}/alternatives_0-9_r4.out: 'alt3: PASS (10/10 seeds)'.")
row("alt-4", "alternative 4 (bisection inversion of the prospect value), seeds 0-9",
    "ledgers/E3/scripts/run_alternatives.py ALT4", "PASS",
    f"{D}/alt4_seeds_0_1_2_3_4_r4.out 'alt4: PASS (5/5 seeds)' and {D}/alt4_seeds_5_6_7_8_9_r4.out 'alt4: PASS (5/5 seeds)' "
    "(run as two parallel halves; seed 7 is in the second half and passes). The round-3 one-off failure at seed 7 "
    "did not recur in three re-runs (round 3: single seed-7 rerun and seeds 0-9 parallel rerun; round 4: this run). "
    "Its original cause was not captured; the script now prints the failing pytest output. Caveat: not identified.")
row("alt-5", "alternative 5 (Decimal half-up rounding of the float value), seeds 0-9",
    "ledgers/E3/scripts/run_alternatives.py ALT5", "PASS",
    f"{D}/alt5_seeds_0-9_r4.out: 'alt5: PASS (10/10 seeds)', EXIT 0.")

# ---- labs and prose numbers ---------------------------------------------------------------------------------------
row("lab-twin-1", "lab-E3-project-1: page code equals twin; expected block equals twin output",
    "project.html:57-137; tests/labs/E3/lab-E3-project-1.py", "PASS",
    f"{D}/page_code_vs_twin_r4.out: 'page code == twin' True; twin run under python -I -W error exit 0, stderr empty; "
    "expected block == stdout.")
row("lab-twin-2", "lab-E3-project-2: page code vs twin; expected block", "project.html:141-186; tests/labs/E3/lab-E3-project-2.py",
    "PASS", f"{D}/page_code_vs_twin_r4.out: page differs from twin only at the two ___ blanks (page lines 14-15 of the code); "
    "twin exit 0; expected block == stdout.")
row("lab-twin-3", "lab-E3-project-3: page code equals twin; expected block equals output",
    "project.html:381-577; tests/labs/E3/lab-E3-project-3.py", "PASS",
    f"{D}/page_code_vs_twin_r4.out: 'page code == twin' True; twin exit 0; expected block == stdout. The rename theta to xi "
    "is identical in the twin and the page.")
row("lab1-prose-numbers", "Lab 1 numbers in prose (project.html:57, 138) recomputed independently",
    "project.html:57, 138", "PASS",
    f"{D}/recompute_numbers_r4.out: CRRA 496/500, 3000/-513, 2166/1244; prospect -30/500, 3000/-762, 2144/140; "
    "P(A) 0.480149, 0.637452, 0.574613; log-likelihood -2.302315; pair-2 B prospect CE -762.1406 (rounds to -762).")
row("lab2-prose-numbers", "Lab 2 numbers in prose (project.html:143, 187) recomputed independently", "project.html:143, 187", "PASS",
    f"{D}/recompute_numbers_r4.out: z = -0.14; log A -0.765595182; log B -0.625595182; sigmoid 0.465057055.")
row("lab3-prose-numbers", "Lab 3 estimates, SEs, log-likelihood and score: own optimiser and own Hessian",
    "project.html:383, 571-578, 694-705", "PASS",
    f"{D}/lab3_independent_r4.out (own Nelder-Mead, 36 starts): optimum gamma 0.635210, lambda 6.150316, kappa 2.020107, "
    "loglik -7.144517; SE at steps 1e-4 and 1e-5: gamma 0.3190, lambda 9.594, kappa 1.8638 (print 0.32, 9.59, 1.86); "
    f"{D}/recompute_numbers_r4.out LAB3 lines: 11 of 12 pairs mixed (pair 4 pure), prize range -18700..19000, sizes {{2,3}}. "
    "The coordinate-search block in recompute_numbers_r4.py is not a valid optimiser (it drifts to lambda 1.7e15, loglik "
    "-7.1524 below the page's -7.1445) and is superseded by lab3_independent_r4.py.")
row("exemplar-word-counts", "word counts of the exemplar memo texts (project.html:610)", "course/modules/E/E3/project.html:610",
    "FAIL", f"{D}/exemplar_words_variants_r4.out: Exemplar A 103 (str.split, tags removed, headings included) matches. "
    "Exemplar B: 409 with headings (398 without); no reading of the rule gives 554 (variants 409, 414, 424, 600, 630, 737). "
    "Round 3 recorded 408 and PASS; that did not match the page either.",
    "project.html:610: change 'that of Exemplar B is 554 words' to the count the page's own rule gives (409), or state the "
    "rule that yields 554.")
row("exemplar-b-instrument-facts", "exemplar B facts (project.html:671) from Lab 3 data", "project.html:671", "PASS",
    f"{D}/recompute_numbers_r4.out: prize range -18700..19000; lottery sizes {{2,3}}; pair 0 A (6200, -15100) 9/10 1/10, "
    "B has three prizes; pair 3 A (18800, -12500) 3/4 1/4, B (16500, -17700) 2/5 3/5, both mixed; 11 mixed pairs.")
row("seed49-docstring-numbers", "seed-49 numbers in test_project.py:876-884", "grader/test_project.py:876-884", "PASS",
    f"{D}/seed49_docstring_r4.out: se_lambda 135.05 (1e-5), 97.67 (1e-6); se_gamma 0.09474, 0.07983; reverse order +1.28% "
    "(136.78) and +0.42% (98.09); -27.68% and -15.73%. All match the docstring. test_project.py is byte-identical to the "
    "round-3 pin (sha1 1ef2c31e).")
row("hours-arithmetic", "hours split sums to the declared total; hub split", "project.html:347-362; index.html:29", "PASS",
    "project.html:352-357 rows 1+1+3+4+3+2 = 14 = project.html:358 total = data-hours-project (project.html:33); "
    "index.html:29 data-hours-lessons=56, data-hours-project=14, total 70. Hours are design targets (ruling): no 30% test.")
row("notation", "every symbol against notation/notation.json", "project.html (all math)", "PASS",
    "notation/notation.json: no page macro is registered in use; \\Phi (project.html:738) matches the registered standard "
    "normal CDF (M4). gamma, lambda, kappa, zeta, xi, alpha, delta, w, W, CE, z, P are not registered and each is defined "
    "in the text where first used; no \\E, \\R, \\mathbb on the page.")
row("citations-reading", "reading section and cites (project.html:745-751) against lessons", "course/modules/E/E3/project.html:745-751",
    "FAIL", "Claims checked: kahneman1979prospect is a claim in L07.html:80 (grade C, data-cite); ellsberg1961risk claim in "
    "L08.html:133 (C); gilboa1989maxmin claim in L08.html:67 (data-cite); pratt1964risk is named, with no key, in L02 "
    "(no key string in L02). But the page says pratt1964risk and epstein1989substitution are 'cited by no lesson', and L05.html:609 "
    "now names epstein1989substitution in <code> ('The registry holds the Epstein and Zin paper under the key ...'); "
    "L06.html:531 does the same for kahneman1979prospect. As written, the page's unqualified 'cited' contradicts L05.",
    "project.html:745: reword 'pratt1964risk and epstein1989substitution are cited by no lesson' to 'are attached to no claim "
    "in any lesson' (or remove the key from L05.html:609 and keep the claim-free sentence).")
row("concept-links", "concept anchors used by the page", "project.html:53", "PASS",
    "def-prospect-theory at L06.html:68; def-certainty-equivalent at L02.html; def-crra-utility at L03.html:88; all three "
    "owned by E3 (curriculum.json concepts), before the project in order.")
row("lesson-references", "lesson locators the page quotes", "project.html:53, 210", "PASS",
    "L03.html:173 Proposition 2.7 (T, affine transformations leave CEs unchanged); L06.html:61 Definition 1.2 (x^alpha for "
    "x>=0, -lambda(-x)^delta for x<0; page's alpha=delta=1-gamma, gamma<1 gives alpha>0); L06.html:68 Definition 1.3 (W := "
    "sum p_i v(x_i)). Note: Definition 1.3 assumes p_i > 0 and the page allows p = 0; the zero term is 0, so no defect.")
row("conventions-vs-grader", "exception table and conventions (project.html:208-230) against grader tests", "project.html:208-230; grader/test_project.py",
    "PASS", "Named exceptions: test_model_name_must_be_crra_or_prospect (286-297, contains 'crra','prospect'); probabilities 300-355, "
    "460-466, 772-777 ('probabilities must sum to 1'); wealth 358-381 ('wealth plus prize must stay positive'); estimate "
    "empty and no mixed lottery 609-688. Whole cents floor(c+1/2): 260-270. Choice probability 819-831. Identification 614-688.")
row("tolerance-disclosure", "tolerances stated on project.html:203 against grader/test_project.py", "project.html:203 vs "
    "grader/test_project.py:195, 223-236, 430, 434", "FAIL",
    "The page says a certainty equivalent is compared with the oracle's whole cent exactly, except the log limit (half cent, "
    "test_project.py:175) and homogeneity (half cent, 207), and dominance (one cent, DOMINANCE_SLACK at 956-959). Not disclosed: test_project.py:195 "
    "(CRRA risky-lottery check) accepts |engine - oracle| <= half a cent; test_project.py:223-236 (prospect bracket) accepts "
    "a value within half a cent of the exact sure amount, with slack 1e-9 relative. test_project.py:430 and :434 use an "
    "absolute 1e-9, stricter than the 1e-9 times max(1,|x|) that the page states for |x| > 1. The SE (10%), log-likelihood "
    "(1e-7), score (2e-5), local-maximum (0.1 percent, 1e-9) and recovery (4 SE, 47 of 50) tolerances are stated correctly.",
    "State on project.html:203 the half-cent rule for test_project.py:195 and the bracket check of :223-236, and the absolute "
    "1e-9 of :430 and :434; or tighten :195 and :223-236 to exact equality with floor(x+1/2) and state the rest.")
row("hub-instrument-count", "instrument size: hub vs project spec vs plan", "index.html:146 vs project.html:197, 354, 600; "
    "plans/E3-build-plan.md:412, 442", "FAIL",
    "index.html:146 (unchanged since round 3): 'design an instrument of at least 12 mixed-sign pairs'. project.html:197 now "
    "requires 'at least 12 pairs' and at least one pair with a mixed lottery; project.html:354 agrees with 197. The plan "
    "(:442 'Choose at least 12 mixed-sign pairs'; :412 'at least 12 pairs with mixed-sign lotteries') still says 12 mixed-sign "
    "pairs. The hub and the spec disagree.",
    "Align index.html:146 with project.html:197 (at least 12 pairs, at least one mixed-sign lottery), or change project.html "
    "197, 354 and rubric C1 (600) to the plan's 'at least 12 mixed-sign pairs'; then re-run check_pages.")
row("dag-unlinked-names", "unlinked concept names against the closure {E1,M1,M2,M4,P0.1} and plan section 7", "project.html (whole page)",
    "PASS", f"{D}/page_text_scans_r4.out (1): names present are derivative, hessian, partial derivative, limit (M2), identification "
    "(P0.1), normal distribution (M4), and E3's own ambiguity aversion, certainty equivalent, CRRA utility, expected utility, "
    "loss aversion, probability weighting. 'Maximum likelihood' appears only in the meta description (plain prose, plan "
    "section 7 allows it). Logit, Epstein-Zin and maxmin are not curriculum concepts.")
row("process-words", "process words and BUILDER_RULES 1.3-1.4 banned strings", "project.html", "PASS",
    f"{D}/page_text_scans_r4.out (2),(3): no verif, builder, fixer, audit, planner, architect, ledger, TODO, placeholder; "
    "'round' occurs only as 'unrounded'/'rounding'; no banned string. 'the brief' is the spec's own document name.")
row("scope-words", "scope words (only, every, all, exactly, any) against computations", "project.html:44, 201, 203, 213, 676", "PASS",
    "'every certainty equivalent' (44): Lab 1 prints all six. 'every money output is an int' (201): tests 155, 173, 216, 291, "
    "387-396. 'every named invalid input' (201): exception table tests. 'only when' (213): necessity holds because a pure-lottery "
    "CE does not depend on lambda (checked by hand and by Lab 3 reasoning); lab output has no lambda-only effect. 'all twelve' "
    "(676) is true (the memo lists two pairs).")
row("round2-spec-zeta-before-definition", "zeta defined at first use", "project.html:203", "PASS",
    f"{D}/page_text_scans_r4.out (7): first zeta on the page is 'in the coordinates \\(\\zeta=\\log(\\gamma/(1-\\gamma))\\)' (203).")
row("round2-spec-kinks-claim", "no kink claim on the page or in the grader", "project.html; grader/*.py", "PASS",
    f"{D}/page_text_scans_r4.out (4): 'kink' absent from the page and from grader/*.py.")
row("round2-spec-ruling6-kappa-wording", "kappa wording (ruling 6)", "project.html:195", "PASS",
    "project.html:195: 'its inverse 1/kappa, in units of $100, is the choice-noise scale that the likelihood needs'; consistent "
    "with z = kappa dCE / 10000 (cents) = kappa (dCE in $100).")
row("round2-grader-named-conditions-tested", "named conditions have tests", "grader/test_project.py:663-688", "PASS",
    "test_a_gain_of_zero_probability_does_not_make_a_lottery_mixed present (663-688); mutant e3d2_01 KILLED in the final run.")
row("round2-grader-kinks-docstrings", "docstrings do not claim kinks", "grader/test_project.py:474-536", "PASS",
    "No 'kink' in the file (scan 4); the file is byte-identical to the round-3 pin (sha1 1ef2c31e).")
row("round2-grader-seed49", "seed-49 sentence matches the recomputed numbers", "grader/test_project.py:876-884", "PASS",
    "See seed49-docstring-numbers.")
row("round2-grader-every-model-comments", "comments on which models the suite uses", "grader/test_project.py:960-968", "PASS",
    "'The increasing models that this suite uses' and 'The concave, increasing models that this suite uses' (960-968); no claim "
    "of all models; file byte-identical to the round-3 pin.")
row("round2-mut-e3d2-01", "mutant e3d2_01 (gain of zero probability counts as mixed)", "ledgers/E3/mutants/e3d2_01_*.py", "PASS",
    f"{D}/mutate_E3_r4_final.out: KILLED.")
row("round2-mut-first-docstring-r10n", "first docstring lines of all mutants", "ledgers/E3/mutants/*.py", "PASS",
    f"{D}/mutant_docstrings_r4.out: 89 files, no first line that starts with 'Reference', 'Single-change' or 'Student-error', none missing.")
row("exemplar-scores-consistent", "exemplar calibration (rubric, excluded from this slice)", "project.html:612-725", "UNVERIFIABLE",
    "Not checked. The assignment excludes the rubric ('No cards, no rubric'), and I had read the annotations (project.html:612-725) "
    "before any scoring, so a blind calibration was not possible in this checkout.",
    "A verifier who has not read the annotations re-scores both exemplars from the rubric table alone and compares with data-scores "
    "(this slice excludes it).")

# ---- new checks (round 4) ----------------------------------------------------------------------------------------
row("mut-e3d4-05-reported-kappa-clamp", "mutant e3d4_05: reported kappa_hat clamped to at least 1, mutate window 0-9",
    f"ledgers/E3/mutants/e3d4_05_reported_kappa_clamped_at_one.py; {D}/mutate_E3_r4_final.out", "FAIL",
    "SURVIVED in the window: all 45 tests pass on seeds 0-9 (run by hand with the same flags, and by the tool). The mutant "
    "differs from the reference only when the true kappa is below 1. The generator produced one such seed in 0-49 (seed 30; "
    f"{D}/instance_check_r4.out), none in 0-9. On seed 30 the suite fails 3 tests (test_reported_log_likelihood..., "
    "test_score_is_zero_at_the_estimate, test_estimate_is_a_local_maximum; run by hand), so the defect is a gap in the window, not an equivalent mutant. The page states "
    "the score (2e-5) and local-maximum checks (project.html:203), which this mutant violates on seed 30.",
    "Add to the suite a participant with kappa below 1 that every window includes (a fixed case such as make_instance(30), or a "
    "seed in 0-9 with kappa < 1 chosen by the generator), so that a reported-kappa clamp fails inside seeds 0-9; then re-run "
    "tools/mutate_graders.py --unit E3 --seeds 0-9 (expect 89/89).")
row("mut-e3d4-04-clamped-objective-killed-by-crash", "mutant e3d4_04 killed", "ledgers/E3/mutants/e3d4_04_*.py", "PASS",
    "KILLED (estimate raises RuntimeError on seeds 0 and 1 when log kappa is clamped in the objective): the kill is by crash, "
    "which the tool counts; reported, not a finding.")
row("instance-validity-20-seeds", "sample 20 instances: validity and material difference", "course/modules/E/E3/grader/instance.py",
    "PASS", f"{D}/instance_check_r4.out: 20 sampled seeds all valid (exact probabilities summing to 1, 2 or 3 prizes, "
    "500-50000 magnitude, 200 pairs, at least 100 mixed); 20 of 20 distinct (gamma, lambda, kappa) and distinct answers. "
    "instance.py is byte-identical to the round-3 pin.")
row("questionnaire-dom-stub", "questionnaire script behaviour (load, refuse incomplete export, export shape)", "project.html:239-343",
    "PASS", f"{D}/questionnaire_dom_stub_r4.out: 14 of 14 checks pass under a minimal DOM stub in node (load, status text, "
    "refusal with missing choices, export only when all chosen, exact export shape, bad-file messages); node --check OK. "
    "Gap: not run in a real browser (see not-checked).")
row("grader-messages-no-leak", "failure messages name the property and carry no values", "grader/test_project.py", "PASS",
    "expect() and must_raise() messages (test_project.py:43-62) name the condition and never format an expected value; hints in "
    "tests 1008, 1023, 1040 name the property. pytest uses --assert=plain with pytrace=False.")
row("pyodide-and-local-parity", "same suite passes in Pyodide and locally", "grader/test_project.py", "PASS",
    f"{D}/page_smoke_project.out (in-browser 45/45 on seed 941900901); local pytest 45 passed (run_graders 50/50 on the reference; "
    "alternatives 1-5 on seeds 0-9).")
row("grader-files-unchanged", "grader files against the round-3 pin", "course/modules/E/E3/grader/*.py", "PASS",
    "test_project.py (sha1 1ef2c31e...), instance.py (831983b0...), starter.py (6cc0a61d...) are byte-identical to a007712; "
    "reference.py changed only by renaming theta to xi in _objective, _maximise and estimate (git diff a007712 4eb6788).")
row("starter-signatures", "starter.py signatures match project.html:199", "grader/starter.py; project.html:199", "PASS",
    "starter.py defines certainty_equivalent_cents(model, prizes_cents, probabilities, params, wealth_cents) -> int, "
    "log_likelihood(responses, params) -> float, estimate(responses) -> dict[str, float]: the page's signatures.")
row("spec-clarifying-questions", "questions a competent student would still have", "project.html:193-206", "PASS",
    "No question that the page leaves open for a named condition. Unnamed invalid inputs (mismatched list lengths, a choice "
    "other than A or B, missing params keys) may raise or return, per project.html:219, so they are not questions. "
    "Hours: design targets, not checked beyond arithmetic.")
row("ladder-rungs", "project ladder (rung 1 solved, rung 2 instant, rung 3 scope, rung 4 open)", "project.html:40-49", "PASS",
    "Rung 1 Lab 1 with interpretation; Rung 2 Lab 2 with expected block; Rung 3 spec, grader, report; Rung 4 stretch. Tier U, so "
    "rungs 1-2 stay at full length (plan line 35).")
row("page-anchors-links", "in-page and cross-file links resolve", "project.html", "PASS",
    f"{D}/page_text_scans_r4.out (8): 12 in-page anchors all resolve; index.html#placement exists; L02, L03, L06, L08, index, review "
    "targets exist with their anchors.")
row("figures-and-data-na", "figures, charts and data files", "project.html", "PASS",
    f"{D}/page_text_scans_r4.out (6): 0 svg, figure, img or data-files on the page; not applicable.")
row("atlas-studio-na", "Atlas milestone and studio sections", "project.html; plans/E3-build-plan.md:3", "PASS",
    "Plan line 3: 'no Atlas milestone'; the page has no studio section. Not applicable.")

verdict = "PASS" if all(r["status"] == "PASS" for r in R) else "FAIL"
counts = {s: sum(1 for r in R if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment = {
    "unit": "E3",
    "slice": "d",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-d, round 4 (did not build E3)",
    "pin": PIN,
    "base": "a007712fdbfc8b4851123f4de76b5310ac5a9e64 (round-3 pin); delta a007712..4eb6788: project.html, grader/reference.py, "
            "tests/labs/E3/lab-E3-project-3.py, tests/labs/E3/lab-E3-L08-1.py, 11 mutant files, ledgers/E3/scripts/run_alternatives.py, "
            "and lesson files L05-L08 (lesson locators read)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD4-E3-d",
    "scratch": "/tmp/e3d_r4_* (scratch copies only)",
    "verified_at": "2026-11-03T16:03:20Z",
    "verdict": verdict,
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        f"Counts: rows {len(R)} (pass {counts['PASS']}, fail {counts['FAIL']}, unverifiable {counts['UNVERIFIABLE']}); "
        f"mutants {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed. Mutation run: {D}/mutate_E3_r4_final.out "
        "(tools/mutate_graders.py, seeds 0-9, 89 files at this pin). Alternatives: 5 of 5 pass on seeds 0-9 (alt4 in two halves). "
        "Gates re-run at the pin (see rows). Two tracked files in ledgers/E3/scripts/E3-d-r4 were present at the pin from an earlier "
        "attempt; I did not use them as evidence and restored run_graders_E3_0_49.out to its committed content (my output is "
        "run_graders_E3_0_49_verifier.out). "
        "Could not check: a real browser run of the questionnaire and the autograder panel (DOM stub and page_smoke only); the rubric "
        "and exemplar calibration and cards (excluded by the assignment); live verify_refs; hours beyond arithmetic; the full repo "
        "pytest suite (only the five test files that cover pages, memos, labs and docs); an unidentified round-3 alt-4 flake (not "
        "reproduced in four runs); a blind exemplar re-score."
    ),
    "summary": (
        f"E3-d round 4 at {PIN}: verdict {verdict}. FAIL rows: gate-ruff-format (outside slice, M3 file), exemplar-word-counts "
        "(554 vs 409), citations-reading ('cited by no lesson' vs L05), tolerance-disclosure (undisclosed half-cent checks and "
        "1e-9 absolute), hub-instrument-count (index.html:146 vs project.html:197), mut-e3d4-05-reported-kappa-clamp (survives "
        "seeds 0-9). UNVERIFIABLE: exemplar-scores-consistent (rubric excluded, not blind). Mutants 88/89 killed. Alternatives 5/5 PASS."
    ),
}
out = ROOT / "ledgers/E3/E3-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "| verdict", verdict, "| rows", len(R), counts, "| mutants", len(mutants),
      sum(1 for m in mutants if m["killed_by"]), "killed")
