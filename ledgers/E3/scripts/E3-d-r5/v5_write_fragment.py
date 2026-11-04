"""Writes ledgers/E3/E3-d.json for the round-5 verifier of E3-d (stdlib only; reads this directory's v5_* outputs).

Run from the checkout: python3 -I ledgers/E3/scripts/E3-d-r5/v5_write_fragment.py
"""
import json
import pathlib
import re
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[4]
S = ROOT / "ledgers/E3/scripts/E3-d-r5"
PIN = "440ed3c8216725d498d9c6d7c746907d4d418198"
BASE = "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b"


def read(name: str) -> str:
    return (S / name).read_text(encoding="utf-8")


def alt(name: str, pattern: str) -> str:
    text = read(name)
    m = re.search(pattern, text)
    return m.group(0) if m else "NOT FOUND"


rows: list[dict] = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or ""
    rows.append(r)


CARRY_LAB1 = "Carried from round 4 (project.html:57-138 byte-identical since the previous pin; the delta hunks start at line 200): "

# ---- gates run at the pin
row("gate-check-dag", "tools/check_dag.py --unit E3", "course/modules/E/E3/*.html", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_check_dag.out: 'check_dag E3: PASS', rc=0 at 440ed3c.")
row("gate-check-projects", "tools/check_projects.py --unit E3", "course/modules/E/E3/project.html", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_check_projects.out: 'check_projects E3: PASS', rc=0.")
row("gate-check-pages", "tools/check_pages.py --unit E3", "course/modules/E/E3/project.html", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_check_pages.out: 'check_pages E3: PASS', rc=0 (includes the banned-string scan).")
row("gate-run-labs-project", "tools/run_labs.py --unit E3 --page project", "project.html Labs 1-3", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_run_labs_project.out: 'run_labs E3: PASS (3/3)', rc=0.")
row("gate-run-graders-seeds-0-49", "tools/run_graders.py --unit E3 --seeds 0-49", "grader/reference.py, grader/test_project.py", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_run_graders_0_49.out: 'run_graders E3: PASS (reference 50/50 seeds, slowest 14.5 s)', rc=0.")
row("gate-collect-45", "pytest --collect-only in a grader workspace (reference as elicit.py)", "grader/test_project.py; project.html:203", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_collect_only.out: '45 tests collected'; project.html:203 says 45 checks; grep -c '^def test_' grader/test_project.py = 45.")
row("gate-page-smoke-project", "tools/page_smoke.py --unit E3 --pages project", "course/modules/E/E3/project.html", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_page_smoke_project.out: 'in-browser grader: All 45 tests pass on seed 209491267', 'page_smoke E3: PASS', rc=0.")
row("gate-mypy-strict", "mypy --no-incremental (repo, strict config)", "repo", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_mypy.out: 'Success: no issues found in 331 source files', rc=0.")
row("gate-ruff-check", "ruff check . (repo)", "repo", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_ruff_check_repo.out: 'All checks passed!', rc=0; grader and labs also: v5_ruff_check.out, v5_ruff_format.out ('15 files already formatted').")
row("gate-ruff-format", "ruff format --check . (repo)", "ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py:3", "FAIL",
    "ledgers/E3/scripts/E3-d-r5/v5_ruff_format_repo.out: '1 file would be reformatted, 473 files already formatted', rc=1, at 440ed3c. The file is outside E3-d and unchanged since a007712 (git log -- that path). The same failure was recorded in rounds 3 and 4.",
    "Outside this slice (M3 owner): run `.venv/bin/ruff format ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py`, then re-run `ruff format --check .`.")
row("gate-pytest-page-memo-docs", "pytest: test_page_checks, test_run_labs, test_labs, test_docs_figures, test_memo_exemplars", "tests/", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_pytest_pages_labs_docs.out: all dots, rc=0 (test_page_smoke is covered by the page_smoke tool run above).")
row("gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', rc=0. No reference changed, so no live run was needed.")
row("gate-no-network-in-page", "static scan of project.html", "course/modules/E/E3/project.html", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_page_text_scans.out: urls [] ; fetch( 0, XMLHttpRequest 0, WebSocket 0, sendBeacon 0, window.open 0; localStorage 1 (head theme script, line 8); img/svg/figure/data-files 0.")
row("gate-mutate-tool-E3-existing", "tools/mutate_graders.py --unit E3 --seeds 0-9 (all 92 files present at the pin)", "ledgers/E3/mutants/", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_mutate_E3_full_seeds0-9.out (copy of the run log): 'mutate_graders E3: PASS (92/92 killed)', EXIT 0.")
row("gate-mutants-r4-new-killed", "kill check of e3d4_01..05 (round-4 additions)", "ledgers/E3/mutants/e3d4_0[1-5]_*.py", "PASS",
    "v5_mutate_E3_full_seeds0-9.out: e3d4_01 KILLED by test_reported_log_likelihood_is_the_likelihood_at_the_estimate; e3d4_02 KILLED by test_probabilities_must_be_nonnegative_and_sum_to_exactly_one; e3d4_03 KILLED by test_crra_requires_wealth_plus_every_prize_to_stay_positive; e3d4_04 KILLED by test_estimate_recovers_the_true_parameters_within_four_standard_errors_on_47_of_50_seeds; e3d4_05 KILLED by test_estimate_on_a_second_participant_is_also_a_maximum (seed 0, LOW_KAPPA = seed 30).")
row("gate-mutants-r3-new", "kill check of e3d3v_01..04", "ledgers/E3/mutants/e3d3v_0[1-4]_*.py", "PASS",
    "v5_mutate_E3_full_seeds0-9.out: all four KILLED (crra inverse, kappa key, estimate probability checks, Hessian forward differences).")
row("gate-mutants-count", "ledgers/E3/mutants file count and kill count after this round's additions", "ledgers/E3/mutants/ (96 files)", "FAIL",
    "96 files at 440ed3c: 92 existing (92/92 killed, v5_mutate_E3_full_seeds0-9.out) plus four round-5 student-error mutants e3d5_01..04 (v5_new_mutants.out): e3d5_02, e3d5_03, e3d5_04 KILLED; e3d5_01_zero_prize_counts_as_a_gain_in_the_mixed_test.py SURVIVED seeds 0-9. Killed 95/96.",
    "Kill e3d5_01: add the witness of mut-e3d5-01-zero-prize-mixed-test to test_estimate_needs_a_mixed_sign_lottery (see that row).")
row("gate-mutants-docstrings", "first docstring line of every mutant", "ledgers/E3/mutants/*.py", "PASS",
    "v5_page_text_scans.out: 'mutant files: 96 bad first lines: []'; no first line starts with 'Reference', 'Single-change' or 'Student-error'.")

# ---- alternatives (filled from the runs)
ALT_FILES = [
    ("v5_alternatives_alt1-3-5_0-9.out", "alt-1", "alt1"),
    ("v5_alternatives_alt1-3-5_0-9.out", "alt-2", "alt2"),
    ("v5_alternatives_alt1-3-5_0-9.out", "alt-3", "alt3"),
    ("v5_alternatives_alt1-3-5_0-9.out", "alt-5", "alt5"),
]
alt_status = {}
for fname, rid, name in ALT_FILES:
    line = alt(fname, rf"{name}: (?:PASS|FAIL) \([^)]*\)")
    alt_status[rid] = line
alt4_a = alt("v5_alt4_seeds_0-4.out", r"alt4: (?:PASS|FAIL) \([^)]*\)")
alt4_b = alt("v5_alt4_seeds_5-9.out", r"alt4: (?:PASS|FAIL) \([^)]*\)")
alt_status["alt-4"] = f"seeds 0-4: {alt4_a}; seeds 5-9: {alt4_b}"
for rid, name in [("alt-1", "alt1"), ("alt-2", "alt2"), ("alt-3", "alt3"), ("alt-4", "alt4"), ("alt-5", "alt5")]:
    status = alt_status[rid]
    ok = (f"{name}: PASS" in status and status.count(f"{name}: PASS") == (2 if rid == "alt-4" else 1))
    evidence = (f"run_alternatives.py ({name}, seeds 0-9) at 440ed3c: {status}. Logs: ledgers/E3/scripts/E3-d-r5/"
                + ("v5_alternatives_alt1-3-5_0-9.out" if rid != "alt-4" else "v5_alt4_seeds_0-4.out and v5_alt4_seeds_5-9.out") + ".")
    row(rid, f"alternative correct implementation {name} passes the suite", "ledgers/E3/scripts/run_alternatives.py", "PASS" if ok else "FAIL",
        evidence, None if ok else f"Alternative {name} fails the suite on a seed: the over-constraint is in test_project.py; see the failing output in the log.")

# ---- labs
row("lab-twin-1", "lab twin 1 isolated, expected block", "project.html:57-137; tests/labs/E3/lab-E3-project-1.py", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_twin_project_1.out equals the expected block (script: exact match, True); python3 -I -W error exit 0, v5_twin_project_1.err 0 bytes; run_labs v5_run_labs_project.out PASS (page code == twin).")
row("lab-twin-2", "lab twin 2 isolated, expected block", "project.html:141-186; tests/labs/E3/lab-E3-project-2.py", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_twin_project_2.out equals the expected block; stderr 0 bytes; run_labs PASS (page differs from the twin only at the two ___ blanks, which run_labs accepts).")
row("lab-twin-3", "lab twin 3 isolated, expected block", "project.html:381-577; tests/labs/E3/lab-E3-project-3.py", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_twin_project_3.out equals the expected block (12 answers, 11 mixed, gamma 0.6352, lambda 6.1503, kappa 2.0201, se 0.32/9.59/1.86, loglik -7.1445, score 3.55e-10); stderr 0 bytes; run_labs PASS.")
row("lab1-prose-numbers", "Lab 1 prose numbers", "project.html:57, 138", "PASS",
    CARRY_LAB1 + "fresh: v5_twin_project_1.out prints pair 1 CRRA 496/500 and prospect -30/500, P(A) 0.480149, log P(chosen) -0.733658, total -2.302315; pair 2 prospect 3000/-762, CRRA 3000/-513 (the sure $30 gain is 3000 cents under both models; the B lottery pays 4000 w.p. 1/4 and -2000 w.p. 3/4, read from project.html:111).")
row("lab2-prose-numbers", "Lab 2 prose numbers", "project.html:143, 187", "PASS",
    "Carried from round 4 (project.html:143 and 187 byte-identical since the previous pin); fresh: v5_twin_project_2.out prints -0.765595182 (A), -0.625595182 (B), 0.465057055; z = 2(1500-2200)/10000 = -0.14 by hand.")
row("lab3-prose-numbers", "Lab 3 prose numbers and the printed reference case", "project.html:383, 571-578, 694-705", "PASS",
    "Independent recomputation ledgers/E3/scripts/E3-d-r5/v5_lab3_recompute.py (multistart compass search + Newton, own code, ANSWERS read from project.html): gamma 0.635210, lambda 6.150316, kappa 2.020107, loglik -7.144517; SE at steps 1e-4 and 1e-5: gamma 0.3190, lambda 9.594/9.594, kappa 1.8638, printing 0.32, 9.59, 1.86. Its own score at its point is 4.4e-8 (a different point at the 1e-6 level). The twin prints 3.55e-10, which the page states; the 1e-6 claim holds.")
row("exemplar-word-counts", "word counts of the two exemplar memos", "project.html:610", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_exemplar_words.py: Exemplar A memo 117 words, Exemplar B memo 435 words (runs between spaces, tags removed, headings included); page says 117 and 435. Round 4's 554 is gone. Rubric scoring itself is out of this round's assignment.")
row("exemplar-b-instrument-facts", "facts stated in Exemplar B's instrument passage", "project.html:671", "PASS",
    "project.html:403 (pair 0 A 6200/-15100 with 9/10, 1/10; B three prizes) and :406 (pair 3 A 18800/-12500, 3/4, 1/4; B 16500/-17700, 2/5, 3/5, both mixed); prize range -18700..19000 (v5_lab3_recompute.out); sizes {2,3}; 11 of 12 mixed.")
row("seed49-docstring-numbers", "standard-error figures in the seed-49 docstring", "grader/test_project.py:876-887", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_seed49_se.out (suite's own oracle helpers, QF_SEED=49): se_lambda 135.05 (1e-5) and 97.67 (1e-6); se_gamma 0.09474 and 0.07983; reverse order 136.78 and 98.09; -27.68% and -15.74%; +1.28% and +0.43%. All match the docstring (rounded as written).")
row("hours-arithmetic", "time budget sums to the declared project hours; hub split", "project.html:352-358, 33; index.html:29, 31", "PASS",
    "project.html:352-357 rows 1+1+3+4+3+2 = 14; total cell 358 = 14; data-hours-project 14 (project.html:33); index.html:29 data-hours-lessons 56 and data-hours-project 14, 70 hours (index.html:31). Hours are design targets (ruling): no 30% test.")
row("notation", "every symbol against notation/notation.json", "project.html (all math, 128 spans)", "PASS",
    "ledgers/E3/scripts/E3-d-r5 scan: macros on the page are \\Phi (registered: standard normal CDF; used at project.html:739 with the same meaning), plus \\gamma, \\lambda, \\kappa, \\zeta, \\xi, \\alpha, \\delta, \\hat\\lambda, \\mathrm{CE}, \\ln, \\log, \\sum, \\texttt; none of \\E, \\R, \\Prob, \\Var, \\mathbb, \\N, \\T appears. notation.json registers \\gamma_3 and \\gamma_4 (not used here); gamma is conventionally local and is defined at project.html:195-214. No registered meaning is reused.")
row("citations-reading", "reading section claims about registry keys", "project.html:746-752", "PASS",
    "kahneman1979prospect: claim at L07.html:80 (data-cite, grade C). ellsberg1961risk: claim at L08.html:133 (C). gilboa1989maxmin: claim at L08.html:67 (C). pratt1964risk: appears in no lesson (grep over L01-L08); L02 and L03 use the name Arrow-Pratt with no key. epstein1989substitution: only L05.html:609, in the References section, 'by its registry record only', with no claim. The page's sentences match (round 4's 'cited by no lesson' for epstein is corrected).")
row("concept-links", "concept links resolve to E3 definitions before the project", "project.html:53", "PASS",
    "def-prospect-theory at L06.html:69; def-certainty-equivalent at L02.html:99; def-crra-utility at L03.html:88; check_dag fresh PASS (v5_check_dag.out).")
row("lesson-references", "lesson locators cited by the page", "project.html:53, 210", "PASS",
    CARRY_LAB1.replace("project.html:57-138", "L03.html and L06.html") + "L03.html:173 Proposition 2.7 (T, affine change leaves CEs unchanged); L06.html:61 Definition 1.2; L06.html:68 Definition 1.3 (W = sum p_i v(x_i)); the zero-probability term is 0. Lines project.html:53 and 210 are unchanged in the delta.")
row("conventions-vs-grader", "conventions and named exceptions against the suite", "project.html:208-230; grader/test_project.py", "PASS",
    "Re-read at 440ed3c: model name 287-298 (contains crra, prospect); probabilities 301-356, 461-468, 742-781 ('probabilities must sum to 1'); wealth 359-380 ('wealth plus prize must stay positive'); estimate refusals 612-691; half cent 261-271; choice probability 822-834; identification 617-691.")
row("tolerance-disclosure", "every tolerance the suite applies is disclosed on the page", "project.html:203 vs grader/test_project.py:195-236, 430-435, 1002-1006", "FAIL",
    "The page says 'their tolerances are these'. The prospect check (test_project.py:224-237) accepts a sure amount if the lottery value lies between the values at c-1/2 and c+1/2 with a slack of 1e-9*(1+|value|) in value units. The page states the half-cent condition without that slack. All other tolerances match the page: half cent and 1e-6 cent (176, 196, 208), one cent for dominance (960-962, 1002-1006), 1e-9 log-likelihood (409, 431, 435, 487), 1e-7 reported likelihood (521, 598), 2e-5 score (548), 1e-3 relative moves with 1e-9 absolute (557-564), 10% SE (900). The oracle-to-oracle check at test_project.py:169-172 (0.01 cent plus 1e-5 relative) compares two oracles, not the engine.",
    "project.html:203: after 'the prospect check, which requires the exact sure amount of the oracle to lie within half a cent of the engine's integer' add ', tested in value units with a slack of \\(10^{-9}\\) times one plus the absolute value of the lottery's value'.")
row("hub-instrument-count", "instrument size and mixed-sign requirement agree between hub and page", "index.html:146; project.html:197, 354", "PASS",
    "index.html:146 now reads 'at least 12 pairs with at least one mixed-sign lottery' (changed in 440ed3c); project.html:197 and 354 agree; the round-4 failure is fixed.")
row("dag-unlinked-names", "concepts used without a link or definition", "project.html (whole page)", "PASS",
    "Carried from round 4 (project.html names unchanged: the delta adds prose only about value and logit formulas; Epstein-Zin and maxmin are not curriculum concepts). check_dag fresh PASS (v5_check_dag.out).")
row("process-words", "no process words in learner text", "project.html (visible text)", "PASS",
    "Scan at 440ed3c (visible text, scripts and pre blocks removed): no verif, builder, fixer, audit, planner, architect, ledger, TODO, placeholder; 'round' only in unrounded/rounding; 'brief' is the spec's own document name. check_pages banned-string gate PASS.")
row("scope-words", "scope words (every, all, only, always) have a computation or a hypothesis", "project.html:44, 201, 203, 213", "PASS",
    "Carried from round 4 for lines 44, 201, 213 (byte-identical). Line 203 was re-read: 'for every parameter' is test_project.py:577 (all three); 'every seed window' is the module-level LOW_KAPPA (test_project.py:36); 'only when' at 213 is necessary (pure lotteries give no lambda dependence, test 'pure' sets).")
row("round2-spec-zeta-before-definition", "zeta is defined before first use", "project.html:203", "PASS",
    "project.html:203 is the first zeta on the page and defines it inline ('in the coordinates \\(\\zeta=\\log(\\gamma/(1-\\gamma))\\)'); the other use is at 214.")
row("round2-spec-kinks-claim", "no 'kink' claim", "project.html; grader/test_project.py", "PASS",
    "v5_page_text_scans.out: 'kink' count 0 in project.html and in test_project.py.")
row("round2-spec-ruling6-kappa-wording", "kappa wording at the Context paragraph", "project.html:195", "PASS",
    "Carried from round 4 (project.html:195 byte-identical since the previous pin): 'its inverse 1/kappa, in units of $100' is consistent with z = kappa dCE / 10000 cents.")
row("round2-grader-named-conditions-tested", "named conditions have a test (zero-probability gain)", "grader/test_project.py:663-688", "PASS",
    "Carried from round 4 (lines 663-688 byte-identical since the previous pin): test_a_gain_of_zero_probability_does_not_make_a_lottery_mixed; mutant e3d2_01 killed (v5_mutate_E3_full_seeds0-9.out).")
row("round2-grader-kinks-docstrings", "no kink claims in grader docstrings", "grader/test_project.py:474-536", "PASS",
    "v5_page_text_scans.out: 'kink' count 0 in test_project.py.")
row("round2-grader-seed49", "seed-49 docstring figures", "grader/test_project.py:876-887", "PASS",
    "See seed49-docstring-numbers (fresh recomputation, v5_seed49_se.out).")
row("round2-grader-every-model-comments", "model-scope comments on the first- and second-order checks", "grader/test_project.py:960-971", "PASS",
    "Re-read: 'The increasing models that this suite uses' (966-967) and 'The concave, increasing models that this suite uses' (971); the comments claim no more than the listed models.")
row("round2-mut-e3d2-01", "mutant e3d2_01 killed", "ledgers/E3/mutants/e3d2_01_*.py", "PASS",
    "v5_mutate_E3_full_seeds0-9.out: KILLED by test_a_gain_of_zero_probability_does_not_make_a_lottery_mixed (seed 0).")
row("round2-mut-first-docstring-r10n", "first docstring lines of all mutants", "ledgers/E3/mutants/*.py", "PASS",
    "v5_page_text_scans.out: 96 files, no bad first line. Note: e3d4_05's first sentence wraps onto a second docstring line; the description is still accurate.")
row("mut-e3d4-05-reported-kappa-clamp", "round-4 survivor: reported kappa clamped at one", "ledgers/E3/mutants/e3d4_05_reported_kappa_clamped_at_one.py", "PASS",
    "Now KILLED (seed 0) by test_estimate_on_a_second_participant_is_also_a_maximum: the fixed LOW_KAPPA participant (generator seed 30, kappa 0.635 in ledgers/E3/scripts/E3-d-r5/v5_collect_only.out) reports kappa 1, so the local-maximum move by -1e-3 raises the likelihood. Round-4 survivor closed.")
row("mut-e3d4-04-clamped-objective-killed-by-crash", "clamped objective mutant e3d4_04", "ledgers/E3/mutants/e3d4_04_log_kappa_clamped_at_zero_in_objective.py", "PASS",
    "KILLED by test_estimate_recovers_the_true_parameters_within_four_standard_errors_on_47_of_50_seeds (seed 0), in the full run (v5_mutate_E3_full_seeds0-9.out); not by a crash.")
row("instance-validity-20-seeds", "20 sampled instances are valid and distinct", "course/modules/E/E3/grader/instance.py", "PASS",
    "ledgers/E3/scripts/E3-d-r5/v5_instance_sample.out: seeds 0-19 each 200 answers, probabilities exact and summing to 1, 2 or 3 prizes, 500-50000 magnitude, at least 100 mixed; 20 distinct (gamma, lambda, kappa). instance.py byte-identical to 4eb6788.")
row("questionnaire-dom-stub", "questionnaire script behaviour", "project.html:239-343", "PASS",
    "Carried from round 4 (project.html:239-343 unchanged in the delta; evidence ledgers/E3/scripts/E3-d-r4/questionnaire_dom_stub_r4.out: 14 of 14 checks under a minimal DOM stub). Fresh: page_smoke loads the page with zero console errors (v5_page_smoke_project.out). Not run in a real browser (see notes).")
row("grader-messages-no-leak", "failure messages name the property and never leak values", "grader/test_project.py:43-62 and the new messages at 597-609", "PASS",
    "expect() and must_raise() name the condition; the new second-participant messages (597-609) name the property. The only echoed value is the rejected model name (296), an input, not an answer.")
row("pyodide-and-local-parity", "same suite passes in Pyodide and locally", "grader/test_project.py", "PASS",
    "v5_page_smoke_project.out: in-browser 45/45 (seed 209491267); local run_graders reference 50/50 (v5_run_graders_0_49.out).")
row("grader-files-unchanged", "unchanged grader files and what changed in test_project.py", "course/modules/E/E3/grader/*.py", "PASS",
    "git diff --quiet 4eb6788 440ed3c for instance.py (831983b0), starter.py (6cc0a61d), reference.py: identical. test_project.py changed only at lines 36 (LOW_KAPPA), 427-436 (relative tolerance on two expects), 583-609 (second-participant test loops over INST2 and LOW_KAPPA).")
row("starter-signatures", "starter signatures match the page", "grader/starter.py; project.html:199", "PASS",
    "Carried from round 4 (starter.py byte-identical to 4eb6788; project.html:199 unchanged).")
row("spec-clarifying-questions", "spec is complete enough for a student to need no clarifying question", "project.html:195, 197, 199, 235, 263", "FAIL",
    "Question I would have had to ask: the spec (line 197) says each probability is 'text of the form numerator/denominator that Fraction reads exactly', but line 195 offers 'a sure amount', and the suite builds sure amounts with probability text '1' and '0' (test_project.py:482, 627, 633, 644, 674, 676, 786-787, 792-799; the zero-probability cases). The questionnaire's validator (project.html:263, regex ^\\d+(\\/\\d+)?$) also accepts '1' and '0'. The instance data (grader/instance.py) uses only numerator/denominator text. A student could not tell from the page whether a whole number is a legal probability text, or how a sure amount is written. Other questions checked (identification, zero-probability prizes, invalid inputs, function signatures, output keys) are answered on the page.",
    "project.html:197 (b) and (a): replace 'text of the form numerator/denominator that Fraction reads exactly' with 'text that Fraction reads exactly: numerator/denominator, or a whole number such as 1 or 0 (a sure amount has probability 1)'; make the same change to the instrument's probability form at the same line.")
row("ladder-rungs", "four-rung ladder present and ordered", "project.html:40-49", "PASS",
    "Carried from round 4 (project.html:40-49 unchanged): Rung 1 Lab 1, Rung 2 Lab 2 (completion, instant), Rung 3 spec/grader/report, Rung 4 stretch.")
row("page-anchors-links", "in-page anchors resolve", "project.html", "PASS",
    "v5_page_text_scans.out: 14 in-page anchors, unresolved []; index.html has id=\"placement\" (index.html:66).")
row("figures-and-data-na", "figures and data requirements", "project.html", "PASS",
    "v5_page_text_scans.out: no svg, img, figure or data-files on the page; not applicable.")
row("atlas-studio-na", "atlas and studio requirements", "project.html; plans/E3-build-plan.md:3", "PASS",
    "Carried from round 4 (plans/E3-build-plan.md unchanged since the previous pin): 'no Atlas milestone'; the page has no studio section.")

# ---- new round-5 items
row("mut-e3d5-01-zero-prize-mixed-test", "mixed-sign identification test: a zero prize is not a gain", "grader/test_project.py:617-691 (test_estimate_needs_a_mixed_sign_lottery and neighbours); ledgers/E3/mutants/e3d5_01_zero_prize_counts_as_a_gain_in_the_mixed_test.py", "FAIL",
    "The mutant treats a prize of 0 with positive probability as a gain. It survives seeds 0-9 (v5_new_mutants.out: SURVIVED). The witness set (v5_zero_prize_witness.out): response 0 has prizes_a [0, -100] with probs 1/2, 1/2 and prizes_b [200]; response 1 is pure gain on A and mixed on B only with a gain and a loss. The reference raises ValueError ('need mixed-sign lotteries to identify loss aversion'); the mutant accepts the set. No test calls estimate on a set that has no lottery with a prize above zero and a loss but has a zero prize. The page names this condition: project.html:227 (ValueError when no response has a lottery that mixes a gain and a loss, each with positive probability) and project.html:197 ('a prize above zero and a prize below zero').",
    "Add to test_estimate_needs_a_mixed_sign_lottery in grader/test_project.py a must_raise(ValueError) on a set with one response whose lottery A is prizes [0, -100] with probs ['1/2','1/2'] and lottery B is prizes [200] with probs ['1'], and no other gain. Verify with the mutant (must be KILLED) and the reference (must pass).")
row("proj-new-mutants-killed", "round-5 student-error mutants e3d5_02..04", "ledgers/E3/mutants/e3d5_02..04", "PASS",
    "v5_new_mutants.out: e3d5_02 (gamma SE without coordinate factor) KILLED by test_standard_errors_match_the_coordinate_change_oracle (seed 0); e3d5_03 (logit scale per dollar) KILLED by test_log_likelihood_matches_oracle_at_the_true_parameters (seed 0); e3d5_04 (Newton stops at 1e-3 gradient) KILLED by test_score_is_zero_at_the_estimate (seed 0).")
mutant_lines = []
for name in ("/tmp/E3d_mutate_r5.log", ):
    pass
log = read("v5_mutate_E3_full_seeds0-9.out").splitlines()
new = read("v5_new_mutants.out").splitlines()
mutants = []
for line in log + new:
    m = re.match(r"^(KILLED|SURVIVED) (\S+?)\.py: (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mutants.append({"id": name, "description": desc, "killed_by": None if killed.strip() == "None" else killed.strip()})
seen = set()
mutants = [m for m in mutants if not (m["id"] in seen or seen.add(m["id"]))]

fragment = {
    "unit": "E3",
    "slice": "d",
    "round": 5,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-d, round 5 (did not build E3)",
    "pin": PIN,
    "base": BASE + " (round-4 pin, per D-E3-d.round4.json); delta " + BASE[:7] + ".." + PIN[:7] + ": project.html (lines 203, 593, 610-612, 665-667, 746-750), grader/test_project.py (lines 36, 427-436, 583-609), mutants e3d4_01..05 and g4_01..03 added; lesson, index and cards changes read only where a reading or hub row depends on them",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD5-E3-d",
    "scratch": "/tmp/e3d_r5_scratch (scratch copies only)",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Scripts: ledgers/E3/scripts/E3-d-r5/v5_*.py and .out (all written by this verifier; the other files in that folder were tracked before this round and are not used as evidence). Mutation run: v5_mutate_E3_full_seeds0-9.out (92 files at the start of the run) and v5_new_mutants.out (four new files). Alternatives: alt1, alt2, alt3, alt5 in v5_alternatives_alt1-3-5_0-9.out; alt4 split into seeds 0-4 and 5-9 (v5_alt4_seeds_*.out) because one serial run was too slow on this machine. Could not check: a real browser run of the questionnaire (DOM stub from round 4 only); the rubric, exemplar calibration and cards (excluded by the assignment); live verify_refs (no reference changed); a full repo pytest (only the five pages, labs, docs and memo files); hours beyond arithmetic. The round-4 row exemplar-scores-consistent is excluded, not carried.",
    "summary": "",
}

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
killed = sum(1 for m in mutants if m["killed_by"])
fragment["verdict"] = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 and killed == len(mutants) else "FAIL"
fragment["summary"] = (f"E3-d round 5 at {PIN}: verdict {fragment['verdict']}. Rows {len(rows)} (pass {counts['PASS']}, "
                       f"fail {counts['FAIL']}, unverifiable {counts['UNVERIFIABLE']}). Mutants {killed}/{len(mutants)} killed.")
out = ROOT / "ledgers/E3/E3-d.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), counts, "mutants", killed, "/", len(mutants))
