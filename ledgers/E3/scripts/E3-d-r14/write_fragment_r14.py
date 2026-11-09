"""Writes ledgers/E3/E3-d.json (round 14) from the outputs under ledgers/E3/scripts/E3-d-r14/. Run from the repo root."""

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
S = "ledgers/E3/scripts/E3-d-r14"
R = lambda name: f"{S}/{name}"  # noqa: E731
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731

# ---- mutants: the 161 pre-existing ones from the mutate run, plus the four verifier-authored ones -----------------
mutants = []
for line in rd(R("mutate_E3_0-9.out")).splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+)\.py: (.*) -> (.*)$", line)
    if m:
        status, name, desc, killed = m.groups()
        mutants.append({
            "id": name,
            "name": name,
            "description": desc.strip(),
            "killed_by": killed.strip() if status == "KILLED" else None,
            "location": f"ledgers/E3/mutants/{name}.py",
        })
for name in (
    "r14d_01_estimate_uses_only_the_first_twelve_responses",
    "r14d_02_crra_log_case_takes_logs_of_final_wealth_minus_wealth",
    "r14d_03_estimate_memoised_by_response_count",
    "r14d_04_standard_errors_scaled_by_root_n",
):
    first = rd(f"ledgers/E3/mutants/{name}.py").splitlines()[0].strip('"')
    text = rd(R(f"r14_mutants_run/{name}.txt"))
    killer = re.search(r"(test_[a-z0-9_]+)", text.split("\n")[0].split("passed in")[-1] if "passed in" in text else text)
    mutants.append({
        "id": name,
        "name": name,
        "description": first,
        "killed_by": f"{killer.group(1) if killer else 'see file'} (seed 0; killed on every seed 0-9, {R('r14_mutants_run/' + name + '.txt')})",
        "location": f"ledgers/E3/mutants/{name}.py",
    })
assert len(mutants) == 165, len(mutants)
assert all(m["killed_by"] for m in mutants), [m["name"] for m in mutants if not m["killed_by"]]

ROWS = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    ROWS.append(r)


P = "PASS"
# ---- gates -----------------------------------------------------------------------------------------------------------
row("gate-check-pages", "tools/check_pages.py --all", "course/modules/E/E3/project.html", P,
    f"{R('check_pages.out')}: 'check_pages E3: PASS', EXIT=0 (all units PASS; grep for FAIL = 0).")
row("gate-check-dag", "tools/check_dag.py --all", "course/modules/E/E3/", P,
    f"{R('check_dag.out')}: 'check_dag E3: PASS', EXIT=0.")
row("gate-check-projects", "tools/check_projects.py --all", "course/modules/E/E3/project.html", P,
    f"{R('check_projects.out')}: 'check_projects E3: PASS', EXIT=0.")
row("gate-run-labs-project", "tools/run_labs.py --unit E3 --page project", "project.html Labs 1-3", P,
    f"{R('run_labs_project.out')}: 'run_labs E3: PASS (3/3)', EXIT=0.")
row("gate-run-graders-seeds-0-49", "tools/run_graders.py --unit E3 --seeds 0-49", "course/modules/E/E3/grader/", P,
    f"{R('run_graders_0_49.out')}: 'run_graders E3: PASS (reference 50/50 seeds, slowest 16.0 s)', EXIT=0. "
    "Round 12 failed seed 14 (second participant); fixed at 1431aa1d and passing here.")
row("gate-collect-51", "pytest --collect-only, grader workspace with reference.py as elicit.py", "grader/test_project.py; project.html Grading mode", P,
    "Collect run (scratch workspace /tmp/e3d-r14-collect): '51 tests collected'. project.html Grading mode paragraph says 'runs 51 checks'.")
row("gate-suite-scan-0-399", "full suite on reference.py, seeds 0-399 (400 runs)", "grader/test_project.py; project.html Constraints and Grading mode", P,
    f"{R('scan_suite_0_399.txt')}: 392 runs EXIT=0; the eight failing seeds are exactly 89, 108, 110, 157, 165, 235, 269, 373 "
    "(108, 157, 165, 269 fail on their own participant; 89, 110, 235, 373 on the second participant), which is the list the page "
    "names in Grading mode. Seed 14 passes.")
row("gate-starter-fails", "suite on grader/starter.py (stubs), seed 0", "grader/starter.py", P,
    f"{R('run_suite_seeds.sh')} on starter.py seed 0: '48 failed, 3 passed', EXIT=1.")
row("gate-ruff", "ruff check and ruff format --check, grader and project labs", "course/modules/E/E3/grader; tests/labs/E3", P,
    f"{R('ruff_check.out')}: 'All checks passed!' EXIT=0; {R('ruff_format.out')}: '15 files already formatted' EXIT=0.")
row("gate-mypy-repo", "mypy --no-incremental (repository configuration)", "repository", P,
    f"{R('mypy_repo.out')}: 'Success: no issues found in 385 source files' EXIT=0.")
row("gate-mypy-grader-strict", "mypy --strict on test_project.py, instance.py, elicit.py (reference copied as elicit.py)", "grader/", P,
    f"{R('mypy_grader_with_reference.sh')} -> {R('mypy_grader_with_reference.out')}: 'Success: no issues found in 3 source files'. "
    f"Bare invocation without elicit.py fails with import-not-found and unused-ignore errors ({R('mypy_project.out')}); the suite "
    "is not in the repository mypy files list (pyproject.toml), so this is not a repository gate failure.")
row("gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json", P,
    f"{R('verify_refs_offline.out')}: 'offline integrity: 560 entries, 0 problems', EXIT=0. No references were changed in this pin; the live run was not made.")
row("gate-pytest-relevant", "pytest tests/test_page_checks.py tests/test_labs.py -k 'E3 or project'", "tests/", P,
    f"{R('pytest_relevant.out')}: all dots, EXIT=0.")
row("gate-page-smoke-project", "tools/page_smoke.py --unit E3 --pages project, four runs", "course/modules/E/E3/project.html", P,
    f"{R('page_smoke_project_run1.out')} .. run4.out: each ends 'page_smoke E3: PASS' with 'in-browser grader: All 51 tests pass' "
    "(seeds 590117003, 1756867058, 1835041833, 1969236655; 32.6 to 32.9 s each).")
row("gate-mutate-existing-161", "tools/mutate_graders.py --unit E3 --seeds 0-9 (161 mutants present at run start)", "ledgers/E3/mutants/", P,
    f"{R('mutate_E3_0-9.out')}: 161 KILLED, 0 SURVIVED, 'mutate_graders E3: PASS (161/161 killed)', EXIT=0.")
row("gate-mutants-count", "mutant count and kill status", "ledgers/E3/mutants/", P,
    "165 listed mutants: 161 pre-existing plus r14d_01..04 written by this verifier; all 165 killed (see mutants). "
    "The eight files in ledgers/E3/equivalent/ are not counted (ruling 9).")

# ---- labs ------------------------------------------------------------------------------------------------------------
row("lab-1-expected-equals-output", "expected block of Lab 1 equals twin output", "project.html Lab 1 (lab-E3-project-1)", P,
    f"{S}/page_vs_twin_project.py output: 'lab 1: expected block == twin output: True'; twin run {R('twin_project_1.out')}.")
row("lab-2-expected-equals-output", "expected block of Lab 2 equals twin output", "project.html Lab 2 (lab-E3-project-2)", P,
    f"{S}/page_vs_twin_project.py: 'lab 2: expected block == twin output: True'; twin run {R('twin_project_2.out')}.")
row("lab-3-expected-equals-output", "expected block of Lab 3 equals twin output", "project.html Lab 3 (lab-E3-project-3)", P,
    f"{S}/page_vs_twin_project.py: 'lab 3: expected block == twin output: True'; twin run {R('twin_project_3.out')}.")
row("lab-twins-isolated", "python -I -W error on each twin", "tests/labs/E3/lab-E3-project-1..3.py", P,
    f"{R('twin_project_1.out')}, _2, _3: rc=0 each; the .err files are 0 bytes.")
row("lab-page-code-equals-twin", "page code blocks equal twins", "project.html data-run blocks", P,
    f"{S}/page_vs_twin_project.py: lab 1 and lab 3 page code == twin: True. Lab 2 differs only at the two blanks "
    "(the two 'return ___' lines of contribution() against the twin's two return lines), the completion convention of ruling 11.")
row("lab1-prose-numbers", "numbers in the Rung 1 hypothesis, output and interpretation", "project.html:57-75, Lab 1 interpretation", P,
    "Twin output: pair 1 CRRA 496 and 500 cents, prospect -30 and 500; P(A)=0.480149; log P(chosen)=-0.733658; sum -2.302315; "
    "pair 2 sure 3000 cents under both models, lottery prospect CE -762 (B = [4000,-2000] with [1/4,3/4]). All match the page.")
row("lab2-prose-numbers", "numbers in the Rung 2 hypothesis and interpretation", "project.html Lab 2", P,
    "z = 2(1500-2200)/10000 = -0.14; log contributions -0.765595182 (A) and -0.625595182 (B); probabilities 0.465057055 and 0.534942945; "
    "all match the twin output line for line.")
row("lab3-prose-numbers", "numbers and claims of Lab 3, the Rung 3 reference case", "project.html:611-617 and Lab 3 text", P,
    "Twin output: 12 answers, 11 mixed-sign, gamma_hat 0.6352 (se 0.32), lambda_hat 6.1503 (se 9.59), kappa_hat 2.0201 (se 1.86), "
    "log-likelihood -7.1445, largest-score check True. The page's exemplar figures match (0.6352, 6.1503, 2.0201, 0.32, 9.59, 1.86, -7.1445).")
row("lab-hypothesis-claims", "claims about what Lab 3 checks (no maximum check; score threshold)", "project.html Lab 3 interpretation", P,
    "lab-E3-project-3.py prints only the score threshold check and does not test that the point is a maximum, as the page says. "
    "The page's 'the lab prints the threshold rather than a digit' matches the print statement.")

# ---- grader and suite claims -----------------------------------------------------------------------------------------
row("grader-tolerances-vs-page", "each tolerance in the Grading mode paragraph", "grader/test_project.py (constants and tests)", P,
    "Read in full. Constants: CRRA half cent (ONE_CENT 0.5 + TOL 1e-6) in homogeneity, risky-lottery and log-case checks; exact integer equality in "
    "test_crra_within_half_cent; prospect slack 1e-9*(1+|value|); dominance slack 1 cent (DOMINANCE_SLACK); log-likelihood 1e-9 and 1e-7 relative; "
    "score 2e-5 at steps 1e-5 and 1e-6 (min); local-maximum move 0.1 percent and 1e-9; standard error 10 percent (1e-1*value) at 1e-5 or 1e-6. All agree with the page text.")
row("grader-seed49-se-docstring", "seed-49 standard-error numbers in test_standard_errors_match_the_coordinate_change_oracle docstring", "grader/test_project.py docstring (lines 1163-1175 region)", P,
    f"{S}/fixture_numbers_r14.py: seed 49 se_lambda 135.0541 (step 1e-5) and 97.6747 (1e-6); se_gamma 0.09474 and 0.07983. Percent changes -27.7 and -15.7 recomputed.")
row("grader-reverse-order-docstring", "reverse-order summation claim (+1.3 and +0.4 percent) in the same docstring", "grader/test_project.py docstring", P,
    f"{S}/reverse_order_se_r14.py: forward 135.0541 vs reverse 136.7795 (+1.28%) at 1e-5; 97.6747 vs 98.0856 (+0.42%) at 1e-6.")
row("grader-all-A-docstring", "numbers in test_estimate_counts_a_mixed_lottery... docstring (all-A set)", "grader/test_project.py", P,
    f"{S}/fixture_numbers_r14.py: kappa_hat 924.73, se_gamma 692.39, se_lambda 692051.98, se_kappa 1981269.33 (above 1e5 for lambda and kappa). Docstring: 925, about 692, above 10^5. Match.")
row("grader-fixed26-b-side-numbers", "fixed fixtures quoted in comments and the README", "grader/test_project.py; ledgers/E3/equivalent/README.md", P,
    f"{S}/fixture_numbers_r14.py: FIXED_26 gamma 0.653397, lambda 2.914731 (comment: 0.6534, 2.9147); B-side 12 gamma 0.117355 (README 0.1174); "
    "seed 30 kappa_hat 0.897 (< 1); seed 49 lambda_hat 20.686 (> 10); seed 49 gamma 0.706 (README 0.7063 after rounding of 0.706253). Match.")
row("grader-low-kappa-seed30", "LOW_KAPPA participant (seed 30) has kappa below 1", "grader/test_project.py:36", P,
    f"{S}/fixture_numbers_r14.py: seed 30 kappa_hat 0.897268 < 1, so the clamp at 1 is detectable.")
row("grader-large-lambda-seed49", "LARGE_LAMBDA participant (seed 49) has lambda above 10", "grader/test_project.py:37", P,
    f"{S}/fixture_numbers_r14.py: seed 49 lambda_hat 20.686351 > 10 (the page says above 10).")
row("grader-stall-seed108", "seed 108 participant: reference search does not reach a stationary point", "grader/test_project.py:38, 994-1003; project.html Grading mode", P,
    f"{S}/fixture_numbers_r14.py: reference raises RuntimeError on seed 108 (own participant); the test allows any error and checks any returned point. Consistent with the page.")
row("grader-recovery-47", "recovery: four standard errors on at least 47 of seeds 0-49", "grader/test_project.py:596-612", P,
    "Reference within-4SE count 49 of 50 (miss at seed 2, a legitimate estimate outside four SE); count threshold 47 is met. "
    f"Count script: {S}/alts/recovery_count.py output on reference.py.")
row("grader-exception-table", "named-condition exceptions", "grader/test_project.py (must_raise uses); project.html:exceptions table", P,
    "must_raise is used only for: model names (test_model_name...), probabilities summing wrong or negative (several tests), wealth plus prize <= 0 (test_crra_requires...), "
    "no responses and no mixed-sign lottery (test_estimate_needs_responses, test_estimate_needs_a_mixed_sign_lottery, test_a_gain_of_zero_probability...). "
    "Other invalid-input tests accept any exception or a non-float result (test_wrong_types...). Messages match the table text.")
row("grader-messages-no-answer", "failure messages name the property and do not print the expected value", "grader/test_project.py expect() and must_raise()", P,
    "All expect() messages are property statements; the only value echoed is the test's own model name (test_model_name...). No expected value is printed. "
    "pytest uses --assert=plain on the page (project.html Running the suite locally).")
row("grader-no-network-no-print", "imports stdlib only, no network module, no output", "grader/test_project.py:1342-1392", P,
    "NETWORK_MODULES list checked against each ast import of elicit.py; capsys asserts empty stdout and stderr on valid calls. Reference imports only math, collections.abc, fractions, typing.")
row("grader-instances-sample-20", "20 sampled instance seeds: validity and material difference", "grader/instance.py", P,
    f"{S}/instance_sample_r14.py (seeds 0,1,2,7,14,21,33,49,57,64,81,96,108,123,157,200,250,301,350,399): 200 responses each; prizes whole cents 5 to 500 dollars; "
    "probabilities exact and summing to 1; 111 to 157 mixed pairs (>= 100); parameters inside [0.1,0.8], [1,3], [0.5,5]; 20 distinct parameter triples and 20 distinct answer sets. ALL VALID.")
row("grader-dual-mode", "same suite runs in Pyodide and under pytest", "grader/test_project.py; project.html", P,
    "page_smoke in-browser run: 51 of 51 pass on four random seeds, 32.6 to 32.9 s total (under the 60 s bound). Per-test Pyodide timing (under 5 s each) was not measured.")
row("grader-own-mutants-r14d", "verifier-authored student-error mutants (at least three) all killed", "ledgers/E3/mutants/r14d_01..04", P,
    f"{S}/make_r14_mutants.py writes four reference-based mutants: first twelve responses only; CRRA log case uses prizes; estimate memoised by count; "
    f"standard errors times sqrt(n). Each killed on every seed 0-9 ({R('r14_mutants_run/')}).")

# ---- alternatives (ruling 10, seeds 0-9) -----------------------------------------------------------------------------
ALT_NOTE = (f"{S}/alts/make_alts.py builds the engine; run with {S}/run_suite_seeds.sh per seed; outputs in {S}/alts/out/alt_vN_sSEED.txt. ")
for v, desc in (
    ("alt_v1", "Nelder-Mead then Newton (with BFGS rounds), public CE closed form"),
    ("alt_v2", "BFGS from the grid start with Nelder-Mead fallback, then Newton"),
    ("alt_v3", "Gauss-Seidel coordinate bisection sweeps, Newton, Nelder-Mead fallback"),
    ("alt_v4", "Nelder-Mead then Newton; public certainty equivalent by bisection inversion of v"),
    ("alt_v5", "Nelder-Mead then BFGS; half-cent rule on the decimal value of the float"),
):
    row(f"alt-{v[4:]}-seeds-0-9", f"alternative correct implementation {v[-2:]}: {desc}", f"{S}/alts/{v}/elicit.py", P,
        ALT_NOTE + f"Result: 10 of 10 seeds 'EXIT=0 51 passed' (seeds 0 to 9). Engine built by make_alts.py; "
        "see notes for the one repair to alt_v3 seed 4 and the added unused helper in the other four.")

# ---- equivalents (ruling 9) and tie rule ---------------------------------------------------------------------------
row("crra-exact-half-tie-rule", "page rule 'where the value is exact, an exact half cent goes toward plus infinity' for CRRA gamma > 0",
    "project.html Conventions 'Whole cents'; grader/reference.py _half_up and _crra_change", "FAIL",
    f"{S}/crra_exact_half_scan_r14.py (reference copied as elicit.py): 590 of 1770 instances with an exact half-cent CRRA certainty equivalent at gamma = 1/2 "
    "return the lower neighbour. Example: wealth 1 cent, prizes 97 and 391 cents with probability 1/2 each (finals 98 and 392, s = 7): exact CE "
    "219.5 cents, reference returns 219, the page's rule gives 220. Only gamma = 0 is stated to be exact; for gamma > 0 the page says nothing about ties, "
    "and the instance guard keeps such values away from the tests, so no test sees it.",
    "Architect ruling needed. Either (a) state on project.html that for gamma != 0 under the crra model an exact half cent may come out either way, "
    "as for the prospect model, and make the suite accept either neighbour there; or (b) make the engine return the upper neighbour for exact CRRA halves "
    "and add a test with the example above (wealth 1, prizes 97 and 391 cents, gamma 0.5, expected 220).")
row("equiv-tie-mutants-proof", "ledgers/E3/equivalent/ tie-rule mutants f05, m06, r13n01, w05: equivalence proof",
    "ledgers/E3/equivalent/README.md sections 1-4", "FAIL",
    "The README proof (point 2 and 3) rests on the tie rule being unstated for CRRA gamma > 0 and on the exact path being gamma = 0 only. "
    "crra-exact-half-tie-rule shows the page's exact-half sentence does reach CRRA gamma = 1/2 values, where these mutants differ from the "
    "reference whenever the float value is exactly k + 1/2 (and the reference itself fails the page rule on exact values). The equivalence therefore "
    "cannot be claimed until the tie-rule question is settled.",
    "Resolve crra-exact-half-tie-rule first. If the rule for gamma > 0 is unstated, keep the four files in equivalent/ with the README proof amended to quote that sentence; "
    "if it applies, move the four back to ledgers/E3/mutants/ and kill them with the new test.")
row("equiv-gamma-clamp-floor", "ledgers/E3/equivalent/r11_03 (gamma_hat clamped at 0.999) and r12d_03 (floored at 0.001): moved as 'differs only where the page states nothing'",
    "ledgers/E3/equivalent/README.md (round 13 section); project.html Grading mode (local maximum; estimate in (0,1))", "FAIL",
    "Ruling 9 allows the move only where the mutant differs from the reference where the page states nothing. The page states that the estimate is a local maximum "
    "of the likelihood (Grading mode: local maximum check moves gamma by 0.1 percent). A clamped gamma_hat above 0.999 (or floored below 0.001) is not a local "
    "maximum on any participant whose true maximum lies beyond the clamp, so the mutant violates a stated behaviour on those inputs. The README concedes that no "
    "fixture reaches them, so the rule requires a new test (a participant the reference fits with gamma_hat above 0.999 or below 0.001), not an equivalence move.",
    "Build a fixture (a SIMULATED or synthetic response set) whose reference estimate has gamma_hat above 0.999, and another with gamma_hat below 0.001, add a local-maximum "
    "test on it, then move the two files back to ledgers/E3/mutants/ with killed_by set. Alternatively the architect states a bound on gamma_hat on the page, which then makes the clamp a student error.")
row("equiv-stall-e12_03", "ledgers/E3/equivalent/e12_03 (returns the stalled point instead of raising on negligible step): moved as 'differs only where the page states nothing'",
    "ledgers/E3/equivalent/README.md; project.html Grading mode (search that stops before a stationary point must not be returned)", "FAIL",
    "The page states that a search that stops without a stationary point must not be returned as the estimate. On the branch where e12_03 differs (the step becomes "
    "negligible before the score does, with a non-stationary point), the mutant returns exactly that point. No participant in the 800-participant scan or the fixtures "
    "reaches the branch (README evidence), so the mutant survives; by ruling 9 it needs a new test that reaches the branch, not a move to equivalent/.",
    "Find or construct a response set that enters the negligible-step branch with a non-stationary point (for example by a finite-difference Hessian with a step-size "
    "discontinuity), add the score check to the suite on it, and return the file to ledgers/E3/mutants/ with its killer test.")

# ---- rubric and exemplars --------------------------------------------------------------------------------------------
row("rubric-descriptors-observable", "every rubric level descriptor observable (VERIFIER_RULES 2.6 rubric 1)",
    "project.html rubric table: C1 level 4 ('lists the pairs'); C5 levels 4 and 3 ('no locator is invented')", "FAIL",
    "C1 level 4 says 'lists the pairs' without saying every pair. Exemplar B's annotation (project.html Exemplar B, C1 miss) reads it as 'all twelve pairs', so the "
    "descriptor does not fix the scoring. C5 levels 3 and 4 say 'no locator is invented' (level 3 and 4 descriptors, rubric table), which a scorer cannot observe from "
    "the report text alone: it is a fact about the author's reading, not a feature of the memo.",
    "Rewrite C1 level 4 as 'lists every pair of the instrument with prizes in cents and exact probabilities, and shows the mixed-sign pairs'. Rewrite the C5 phrase as an "
    "observable condition, for example 'every locator is one that the report cites with the source's registry key and a page or section it names'.")
row("exemplar-A-annotations", "Exemplar A annotations and official scores consistent with rubric descriptors",
    "project.html Exemplar A (data-scores 2,2,1,2,1)", P,
    "C1: count and scale, no pair, reason for losses = level 2; misses level 3 (dollars, no example pair). C2: value and logit stated, per-response term missing = level 2. "
    "C3: no standard error = level 1. C4: 'names one limit' = level 2 (rubric C4 level 2 text: 'Names one limit.'). C5: no grade or key = level 1. Official 2,2,1,2,1 consistent.")
row("exemplar-B-annotations", "Exemplar B annotations and official scores consistent with rubric descriptors",
    "project.html Exemplar B (data-scores 3,3,4,3,3)", P,
    "C1 level 3 met, level 4 missed (only two pairs listed); C2 level 3 met, level 4 missed (precision identification stated as a hypothesis); C3 level 4 met; "
    "C4 level 3 met, level 4 missed (no direction of bias); C5 level 3 met, level 4 missed (no key or derivation). Official 3,3,4,3,3 consistent with the descriptors.")
row("exemplar-word-counts", "exemplar memo word counts stated on the page", "project.html:Two exemplars paragraph", P,
    f"{S}/wordcount_exemplars.py: Exemplar A memo 117 words, Exemplar B memo 456 words (headings included, tags removed). The page says 117 and 456.")
row("exemplar-B-data-claims", "Exemplar B's data claims (prize range, prizes per lottery, pairs 0 and 3, mixed count)", "project.html Exemplar B Instrument paragraph",
    P, f"{S}/exemplar_b_data_check_r14.py on tests/labs/E3/lab-E3-project-3.py: min prize -18700, max 19000, 2 or 3 prizes per lottery, 11 mixed pairs; pair 0 = 6200 cents at 9/10 and -15100 at 1/10 against three B prizes; pair 3 = 18800 at 3/4, -12500 at 1/4 against 16500 at 2/5, -17700 at 3/5. All as the page says.")
row("exemplar-blind-calibration", "blind scoring of exemplars by the rubric alone, then comparison with the official scores (ruling 23)",
    "project.html rubric and exemplars", "UNVERIFIABLE",
    f"Stripped copy by {S}/strip_exemplars.py (/tmp/e3d-r14-blind/rubric_and_exemplars_stripped.html). Scores from the stripped copy: Exemplar A 2,2,1,2,1; "
    "Exemplar B 3,3,4,3,3; both equal the official scores. Blindness is not established: before stripping, this verifier listed the tags of project.html, which printed the "
    "data-scores and data-level attributes, so it cannot be the blind scorer that ruling 23 requires.",
    "A dedicated scorer that has not opened project.html (ruling 23) must run strip_exemplars.py, score the output, and return its scores; this row is then re-checked against the official scores.")

# ---- structure, prose, DAG, notation ----------------------------------------------------------------------------------
row("hours-arithmetic", "hours table sums to the hub figure and the curriculum", "project.html #hours; index.html data-hours-project", P,
    "Table: 1 + 1 + 3 + 4 + 3 + 2 = 14 (project.html budget table). index.html data-hours-project=14, data-hours-lessons=56, 56 + 14 = 70 = curriculum hours (curriculum/02-economics-finance-core.yaml:91). "
    "Per ruling, component hour estimates are design targets; only arithmetic was checked.")
row("structure-sections", "section order and required parts", "project.html", P,
    "check_projects.py E3 PASS; section order: ladder, rungs 1-2, spec, conventions, exceptions, questionnaire, budget, autograder, local, report (lab 3, brief, rubric, exemplars, self-assessment), stretch, reading.")
row("ladder-rungs", "ladder present; rung 1 solved and annotated; rung 2 instant; rung 3 scope; rung 4 open", "project.html ladder and rungs", P,
    "Rung 1 solved (Lab 1, step comments); rung 2 completion with blanks and instant check (Lab 2); rung 3 spec and grader; rung 4 stretch items listed, not graded.")
row("notation", "symbols vs notation/notation.json", "project.html math", P,
    "notation/notation.json registers \\Phi (standard normal CDF, used with that meaning in Stretch) and \\gamma_3, \\gamma_4 (not used on this page). The page's \\gamma, \\lambda, \\kappa, \\zeta, \\xi, \\alpha, \\delta are unregistered and used with one meaning each.")
row("process-words", "no process words in learner text", "project.html", P,
    "grep (case-insensitive) for verifier, builder, architect, ledger, batch, fanout, round, plan, todo, draft found only 'rounded'/'rounding' (arithmetic) and no process words.")
row("banned-phrases", "BUILDER_RULES 1.3-1.4 banned strings", "project.html", P,
    "Counts: TODO 0, TBD 0, lorem 0, 'for brevity' 0, 'details omitted' 0, 'beyond the scope' 0, 'left as an exercise' 0, 'you can add more' 0, "
    "'it is important to note' 0, 'studies show' 0, 'experts agree' 0, 'it is well known' 0, obviously 0, clearly 0, 'It can be shown' 0, roughly 0, historically 0, "
    "ellipsis 0. 'about' occurs only in lowercase prose.")
row("concept-links-dag", "check_dag and concept links used outside the closure", "project.html concept links (certainty-equivalent, crra-utility, first-order-stochastic-dominance, prospect-theory)", P,
    f"{R('check_dag.out')}: PASS. The links point at L02, L03, L04 and L06 definitions (ids present: L02 def-certainty-equivalent, L03 def-crra-utility, L04 def-first-order-stochastic-dominance, L06 def-prospect-theory and def-loss-aversion).")
row("reading-keys-and-attribution", "reading list keys and the attributions the reading section makes", "project.html Reading section; course/modules/E/E3/L07.html, L08.html, L02.html:616, L05.html:609", P,
    "kahneman1979prospect cited (data-cite) in L07 only; ellsberg1961risk and gilboa1989maxmin in L08 only; pratt1964risk appears in L02 only in the registry-keys sentence (line 616, no claim); "
    "epstein1989substitution appears in L05 line 609 only, registry record only. The page's statements match. No locator or statement is attributed to any source on the page.")
row("cross-lesson-definitions", "cross-lesson definitions and results the page relies on", "project.html Rung 1 and Conventions", P,
    "L03 Proposition 2.7 (affine transformations leave certainty equivalents unchanged) exists and is graded T; L06 Definition 1.2 (value function) and 1.3 (prospect value) match the alpha/delta usage; "
    "L02 def-certainty-equivalent, L03 def-crra-utility, L04 def-first-order-stochastic-dominance, L06 def-prospect-theory and def-loss-aversion exist.")
row("figures", "figures (SVG, figure, canvas)", "project.html", P,
    "grep count of svg, figure and canvas in project.html: 0. No figure to check.")
row("lab-page-claims-about-engine", "claims that the engine is graded on the learner's seed in the browser and locally, and nothing is sent", "project.html Autograder, Running the suite locally, footer", P,
    "page_smoke runs the in-browser grader in Pyodide; no network request is present in the page code (the questionnaire and grader have no fetch). The page's footer and Constraints statements are consistent with the code read.")

# ---- verdict ---------------------------------------------------------------------------------------------------------
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in ROWS:
    counts[r["status"]] += 1
verdict = "PASS" if counts["PASS"] == len(ROWS) else "FAIL"

fragment = {
    "unit": "E3",
    "slice": "d",
    "round": 14,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-d, round 14 (did not build E3; read verifier-rules.md, VERIFIER_RULES.md, CLAUDE.md, E3-build-plan.md section 6, FINAL-ARCHITECT-RULINGS.md)",
    "pin": "1431aa1d842a5d2d05fd5953c098500bf78a4307",
    "base": "329c1d7 (round-12 pin, the latest fragment on disk: /Users/billyribeiro/.fanout/frags/D-E3-d.round12.json). The round-13 fragment named in the brief (D-E3-d.round13.json) does not exist. Delta 329c1d7..1431aa1d read for project.html (26 lines), grader/reference.py (50), grader/test_project.py (56), tests/labs/E3/lab-E3-project-3.py (2), ledgers/E3/mutants (new and renamed files) and ledgers/E3/equivalent (README and 8 files); the whole page and whole grader were read in full regardless.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD14-E3-d",
    "scratch": "/tmp/e3d-r14-* (blind copy, collect, mypy, scan, run and alt workspaces; removed after use)",
    "verified_at": "2026-11-09T07:30:00+00:00",
    "verdict": verdict,
    "rows": ROWS,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 14 (E3-d) at 1431aa1d. Not checked: (1) cards (out of scope for this slice per the brief); (2) the live verify_refs run (no reference changed; offline only); "
        "(3) per-test Pyodide timing under 5 s; (4) a dedicated blind exemplar scorer (ruling 23); (5) a browser click-through of the questionnaire export (the questionnaire JS was read, not run); "
        "(6) seeds 400 and above (the browser can draw any 31-bit seed); (7) alternatives beyond the five verifier-written ones. "
        "Mutants: 161 pre-existing plus r14d_01..04; the eight equivalent/ files are outside the mutant count and three of them (r11_03, r12d_03, e12_03) are contested in rows above. "
        "Alternatives: alt_v3's first run failed seed 4 with a NameError in its own fallback path (fixed: Nelder-Mead added) and its seeds 0-9 were rerun after two fixes (step 1e-5 for "
        "the standard errors, Nelder-Mead fallback when the information is not positive definite); alt_v1, v2, v4 and v5 engines were regenerated after their runs only by "
        "adding an unused helper (_is_pd), so their runs reflect the same searches. The four new verifier mutants were run with run_suite_seeds.sh, not mutate_graders.py, "
        "because they were written after that run's glob. Exemplar blindness is compromised (see exemplar-blind-calibration). Observation (not a row): the reference "
        "on seed 49 has lambda_hat 20.69, and the page's own Constraints claim that all of seeds 0-49 are gradable holds."
    ),
    "summary": (
        f"E3-d round 14 at 1431aa1d: {len(ROWS)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. "
        f"Mutants: {len(mutants)} listed, {sum(1 for m in mutants if m['killed_by'])} killed (161 pre-existing on seeds 0-9, plus 4 verifier-written). "
        "Five verifier alternatives on seeds 0-9: see alt rows. Main FAILs: an exact-half CRRA rounding case the page's own rule covers (590 of 1770 scanned exact halves at gamma = 1/2 return the lower neighbour), three equivalent-moves that violate page-stated local-maximum or stationary-point behaviour, the tie-mutant proof that depends on that rule, one vague rubric descriptor set, and a blind exemplar calibration that was not blind."
    ),
}

out = ROOT / "ledgers/E3/E3-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(ROWS), counts, "mutants", len(mutants))
