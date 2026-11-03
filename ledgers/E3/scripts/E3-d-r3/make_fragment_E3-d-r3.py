"""Round-3 verifier (E3-d): writes the ledger fragment ledgers/E3/E3-d.json from the round-3 evidence files.

The mutant list is read from the round-3 mutation run (ledgers/E3/scripts/E3-d-r3/mutate_E3_seeds0-9_round3_full.txt),
so every mutant row is the tool's own output. Run from the repository root:
    .venv/bin/python -B ledgers/E3/scripts/E3-d-r3/make_fragment_E3-d-r3.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

S = "ledgers/E3/scripts/E3-d-r3/"
R = "ledgers/E3/scripts/E3-d-r3/"


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> dict[str, str]:
    out = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        out["fix"] = fix or ""
    return out


MUT = Path(S + "mutate_E3_seeds0-9_round3_full.txt").read_text(encoding="utf-8").splitlines()
mutants = []
pattern = re.compile(r"^(KILLED|SURVIVED) (\S+): (.*) -> (.*)$")
for line in MUT:
    m = pattern.match(line)
    if not m:
        continue
    status, name, description, killed = m.groups()
    mutants.append(
        {
            "id": name.removesuffix(".py"),
            "description": description,
            "killed_by": killed if status == "KILLED" else None,
            "file": f"ledgers/E3/mutants/{name}",
            "source": f"tools/mutate_graders.py --unit E3 --seeds 0-9 (round 3, output {S}mutate_E3_seeds0-9_round3_full.txt)",
        }
    )

rows = [
    # ---- gates
    row("gate-check-dag", "tools/check_dag.py --unit E3", "course/modules/E/E3/*.html", "PASS",
        f"{S}check_dag_E3.out: 'check_dag E3: PASS', exit 0."),
    row("gate-check-projects", "tools/check_projects.py --unit E3", "course/modules/E/E3/project.html", "PASS",
        f"{S}check_projects_E3.out: 'check_projects E3: PASS', exit 0."),
    row("gate-check-pages", "tools/check_pages.py --unit E3", "course/modules/E/E3/project.html", "PASS",
        f"{S}check_pages_E3.out: 'check_pages E3: PASS', exit 0."),
    row("gate-run-labs-project", "tools/run_labs.py --unit E3 --page project", "project.html labs 1-3", "PASS",
        f"{S}run_labs_project.out: 'run_labs E3: PASS (3/3)', exit 0; twins alone under python -I -W error via {S}labs_twins_r3.py (out {S}labs_twins_r3.out): exit 0, empty stderr, stdout identical to the expected block in all three."),
    row("gate-run-graders-seeds-0-49", "tools/run_graders.py --unit E3 --seeds 0-49", "grader/reference.py, grader/test_project.py", "PASS",
        f"{S}run_graders_E3_0_49.out: 'run_graders E3: PASS (reference 50/50 seeds, slowest 14.3 s)', exit 0."),
    row("gate-collect-39", "pytest --collect-only on grader/test_project.py (reference as elicit.py, QF_SEED=0)", "grader/test_project.py; project.html:203", "PASS",
        f"{S}collect_count_r3.sh (output {S}extra_checks_r3.out): '45 tests collected in 0.11s'; project.html:203 says 45 checks. The row id is kept from round 2; the count changed from 39 to 45."),
    row("gate-page-smoke-project", "tools/page_smoke.py --unit E3 --pages project", "course/modules/E/E3/project.html", "PASS",
        f"{S}page_smoke_project.out: 'page_smoke modules/E/E3/project.html: PASS', 'in-browser grader: All 45 tests pass on seed 1208574612. (30.6 s)', labs 1-3 run, 'page_smoke E3: PASS', exit 0. Per-test Pyodide time is a separate row (grader-recovery-test-duration)."),
    row("gate-mypy-strict", "mypy --no-incremental (repo)", "repo", "PASS",
        f"{S}mypy.out: 'Success: no issues found in 331 source files', exit 0."),
    row("gate-ruff", "ruff check . ; ruff format --check (E3 paths)", "repo; course/modules/E/E3; ledgers/E3", "PASS",
        f"{S}ruff_check.out: 'All checks passed!', exit 0; {S}extra_checks_r3.out: '4 files already formatted' for course/modules/E/E3 and ledgers/E3. Out of slice, reported in notes: repo-wide 'ruff format --check .' (ruff_format.out) reports ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py."),
    row("gate-pytest-page-memo-docs", "pytest tests/test_page_checks.py tests/test_memo_exemplars.py tests/test_docs_figures.py", "tests/", "PASS",
        f"{S}pytest_pages_memo_docs.out: a line of dots at 100%, 'EXIT 0'."),
    row("gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json", "PASS",
        f"{S}verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0. The live run is the scheduled CI job and was not run here."),
    row("gate-no-network-in-page", "grep for fetch(, http, XMLHttpRequest, sendBeacon in project.html", "project.html questionnaire script (lines 236-343)", "PASS",
        f"{S}extra_checks_r3.out: network tokens in project.html: 0. grader.js line 18 fetches only the same-origin starter and suite (unchanged)."),
    row("gate-mutate-tool-E3", "tools/mutate_graders.py --unit E3 --seeds 0-9 (77 mutant files at a007712)", "ledgers/E3/mutants/", "PASS",
        f"{S}mutate_E3_seeds0-9_round3_full.txt: 77 KILLED, 0 SURVIVED, 'mutate_graders E3: PASS (77/77 killed)', exit 0."),
    row("alt-1", "alternative 1: grid, 26-direction compass search, Newton polish (run_alternatives.py build)", "ledgers/E3/scripts/run_alternatives.py", "PASS",
        f"{S}alternatives_0-9_parallel.out: 'alt1: PASS (10/10 seeds)', exit 0; per-seed lines 'alt1 seed k: pass [45 passed]'. Driver {S}run_alternatives_parallel_r3.py (same build() and pytest flags as the tool)."),
    row("alt-2", "alternative 2: grid then Newton with central differences", "ledgers/E3/scripts/run_alternatives.py", "PASS",
        f"{S}alternatives_0-9_parallel.out: 'alt2: PASS (10/10 seeds)'."),
    row("alt-3", "alternative 3: grid, hand-written Nelder-Mead (restarted), Newton polish", "ledgers/E3/scripts/run_alternatives.py", "PASS",
        f"{S}alternatives_0-9_parallel.out: 'alt3: PASS (10/10 seeds)'."),
    row("alt-4", "alternative 4: bisection inversion of the prospect value (no closed form)", "ledgers/E3/scripts/run_alternatives.py", "PASS",
        f"{S}alternatives_0-9_parallel.out: 'alt4: PASS (10/10 seeds)' (about 5.5 min per seed in pytest)."),
    row("alt-5", "alternative 5: half-cent rule applied to the decimal value of the float", "ledgers/E3/scripts/run_alternatives.py", "PASS",
        f"{S}alternatives_0-9_parallel.out: 'alt5: PASS (10/10 seeds)'."),
    row("alt-se-exact-hessian", "correct SE by an exact-precision observed information (60-digit Decimal, step 1e-20), not the reference's 1e-5 finite difference", "grader/test_project.py:873-902; project.html:214", "PASS",
        f"{S}se_step_probe.py -> {S}se_step_probe.out: exact-Hessian candidate passes the suite's SE rule on all 50 seeds 0-49 ('exact-Hessian candidate fails the suite's SE rule on seeds: []'). Seed 49 deviates from the 1e-6 oracle by 19 to 40 percent but is within 1.1 percent of the 1e-5 oracle. The SE rule is therefore not over-constrained for an exact Hessian on these seeds."),
    # ---- spec
    row("spec-conventions-models", "Models convention vs reference", "project.html:210; grader/reference.py:28-31", "PASS",
        "project.html:210 'with no other spelling accepted'; reference.py:28-31 accepts only 'crra' and 'prospect' and raises ValueError with both names; test_model_name_must_be_crra_or_prospect (test_project.py:286-297) passes on reference."),
    row("spec-whole-cents", "Whole-cent rule floor(c+1/2) and int outputs", "project.html:211; reference.py:71-73,122-128", "PASS",
        "project.html:211 states floor(c+1/2); reference.py:73 _half_up = floor(y+0.5); reference.py:122-124 gamma=0 path floor(expected + Fraction(1,2)); test_half_cent_goes_up_on_exact_halves passes on reference (50/50)."),
    row("spec-exception-table", "Exception table vs reference messages and tests", "project.html:224-227; reference.py:30,60,121,288,291", "PASS",
        "Messages: reference.py:30 names both 'crra' and 'prospect'; reference.py:60 'probabilities must sum to 1 (and be non-negative)' contains the table text; reference.py:121 'wealth plus prize must stay positive'; reference.py:288/291 ValueError for empty responses and no mixed lottery. must_raise in test_project.py:50-62 checks each quoted text."),
    row("spec-identification-claim", "Identification: lambda absent from all-gain or all-loss CE", "project.html:213", "PASS",
        "Derivation: gain branch v=x^(1-gamma) has no lambda; all-loss V=-lambda*S gives CE=-(S)^(1/(1-gamma)) with S=sum p(-x)^(1-gamma), free of lambda. Consistent with reference.py:142-146 and test_project.py:123-127."),
    row("spec-estimation-se-convention", "SE convention: observed information in (zeta, log lambda, log kappa); delta factors", "project.html:214; grader/reference.py:297-315; test_project.py:873-902",
        "PASS", f"Re-derived factors: d gamma/d zeta = gamma(1-gamma), d lambda/d log lambda = lambda, d kappa/d log kappa = kappa (reference.py:313-315 and test lines 893-895). {S}se_step_probe.out: the exact-precision candidate passes on all 50 seeds (alt-se-exact-hessian)."),
    row("spec-score-tolerance-2e-5", "Score below 2e-5 at the estimate, steps 1e-5 and 1e-6", "project.html:203; test_project.py:524-549",
        "PASS", "Test takes min over steps 1e-5 and 1e-6 of the largest component and requires <= 2e-5 (test lines 546-549), as project.html:203 says. Reference passes 50/50 (run_graders_E3_0_49.out). The page no longer claims kinks or smoothness."),
    row("spec-recovery-47-of-50", "Recovery within four SE on at least 47 of 50 seeds", "project.html:203; test_project.py:566-581",
        "PASS", "Test lines 566-581: within = count of seeds with |fit - truth| <= 4*se for all three parameters; requires >= 47. Reference: 50/50 seeds pass (run_graders_E3_0_49.out)."),
    row("spec-stdlib-no-print", "Stdlib only, no network module, nothing printed or warned", "project.html:201; test_project.py:1073-1098",
        "PASS", "Test parses elicit.py imports against sys.stdlib_module_names and NETWORK_MODULES and checks captured stdout/stderr are empty; pytestmark filterwarnings('error'). Reference passes."),
    row("spec-probabilities-exactly-one", "Probabilities non-negative and sum exactly 1; zero allowed", "project.html:215,225; test_project.py:300-355,780-786",
        "PASS", "Tests use exact Fraction offsets of 1/1000, 1/10**13, 1/10**17 and negative probabilities; zero probability allowed (test lines 304-307, 780-786). Killed: e3d1_01, e3d2_03, f01, f02, m10, r4_probability_sum_tolerance_1e12, e3d3_01 (mutate_E3_seeds0-9_round3_full.txt)."),
    row("spec-probabilities-exact-sum-grader-gap-r1", "Round-1 FAIL: float-equality sum check survives the suite", "ledgers/E3/mutants/e3d1_01_prob_sum_float_equal_one.py; test_project.py:300-355",
        "PASS", "e3d1_01 is KILLED by test_probabilities_must_be_nonnegative_and_sum_to_exactly_one (seed 0) in mutate_E3_seeds0-9_round3_full.txt."),
    row("spec-dominance-not-in-page", "Page states no dominance requirement", "project.html", "PASS",
        f"{S}extra_checks_r3.out: 'dominance on the page: 0'."),
    row("spec-grader-exception-types", "Tests demand an exception type only for named conditions", "test_project.py:50-62,286-297,346-367,545-596,682-700",
        "PASS", "must_raise is used only for the five named conditions (model name, probability sum, wealth, empty responses, no mixed lottery, with the zero-probability gain case added in round 3); test_wrong_types_never_return_money_as_a_float (lines 384-396) allows any exception."),
    row("spec-collect-count-matches-page", "Test count on the page equals collect-only count", "project.html:203; collect_count_r3.sh", "PASS",
        "project.html:203 says '45 checks'; collect-only reports 45 (gate-collect-39)."),
    row("spec-signatures-starter", "Starter signatures vs project.html:199", "project.html:199; grader/starter.py:14-35", "PASS",
        "starter.py signatures: certainty_equivalent_cents(model: str, prizes_cents: list[int], probabilities: list[Fraction], params: dict[str, float], wealth_cents: int) -> int; log_likelihood(responses, params) -> float; estimate(responses) -> dict[str, float]. These equal project.html:199. starter.py is byte-identical to round 2 (git diff c737272f a007712f does not list it)."),
    row("spec-questionnaire-browser-claims", "Questionnaire: export only when complete; nothing sent", "project.html:235, 240-342",
        "PASS", "Script: export handler builds 'missing' list and returns with 'No export: pair ... has no choice yet' before any Blob or createObjectURL call (lines 328-332); no network calls (extra_checks_r3.out: network tokens 0); file read via file.text()."),
    row("spec-local-assert-plain-claim", "Local run: --assert=plain shows no values; -W error", "project.html:373-374",
        "PASS", f"{S}extra_checks_r3.out 'E       AssertionError' from pytest --assert=plain on 'assert x == 2' (x = 3): no values shown. A failure via pytest.fail shows only the message."),
    row("spec-lab3-copy-instruction", "Lab 3 copy-and-replace instruction is executable", "project.html:383; lab-E3-project-3 twin main()", "PASS",
        "The instruction names second_order_search, which exists in the lab (tests/labs/E3/lab-E3-project-3.py); the lab prints the same lines as the page's expected block (lab3-output-equals-expected)."),
    row("spec-zeta-used-before-definition", "zeta used before definition (round-2 FAIL)", "project.html:203", "PASS",
        "Round 3: project.html:203 now defines zeta = log(gamma/(1-gamma)) at its first use ('in the coordinates \\(\\zeta=\\log(\\gamma/(1-\\gamma))\\), ...'). The round-2 row is fixed."),
    row("spec-kinks-claim", "Kinks claim in the spec (round-2 FAIL)", "project.html:203", "PASS",
        f"Round 3: 'kink' appears nowhere in project.html or grader/*.py (extra_checks and grep). Derivative check ledgers/E3/scripts/E3-d-r2/kink_check.py (round 2) showed the CE is C^1 across V=0 for gamma>0; the page no longer claims kinks."),
    row("spec-ruling6-kappa-wording", "Architect ruling 6: page must state kappa is the choice-noise scale", "project.html:195; plans/FINAL-ARCHITECT-RULINGS.md item 6", "FAIL",
        f"project.html:195 says kappa is the precision and that its inverse 1/kappa, in units of $100, 'is the choice-noise scale'; the literal ruling requires the page to say that kappa is the choice-noise scale. The page's physics is right (P(A)=1/(1+exp(-kappa*dCE/10000)) makes kappa a precision), so the ruling's words are wrong as written. Literal non-compliance, and the round-2 request for an Architect decision is still open. Evidence for the physics: tests/labs/E3/lab-E3-project-1.py line 69 comment and test_project.py:819-831.",
        "Architect to amend ruling 6 to 'kappa is the choice precision; its inverse, in units of $100, is the choice-noise scale', and the page (project.html:195) then matches. Or, if the ruling stands, rewrite project.html:195 to 'kappa is the choice-noise scale' (wrong physics; not recommended)."),
    row("spec-context-sentences", "Spec Context is 2-4 sentences (BUILDER_RULES 5.2)", "project.html:195 (Context dd)", "FAIL",
        "The Context dd has six sentences: 'A participant answers ... lotteries.', 'Each answer is a noisy signal ...', 'You want three numbers ... precision kappa of the choices.', 'The brief names the first two; ... what the likelihood needs.', 'It is reported with its own standard error.', 'The question is how precisely ... with the standard errors.' BUILDER_RULES 5.2 requires 2-4.",
        "Cut the Context dd to four sentences: move the kappa-as-precision sentence and the standard-error sentence into the Inputs or Constraints dd, or merge them."),
    row("spec-log-likelihood-field", "A competent student needs no clarifying question: the reported log_likelihood", "project.html:199; test_project.py:516-521", "FAIL",
        "project.html:199 lists the estimate's keys and includes log_likelihood, but no sentence on the page says that this field is the log-likelihood at the estimate. test_reported_log_likelihood_is_the_likelihood_at_the_estimate (test_project.py:516-521) requires exactly that. The only statement is the Lab 3 interpretation (project.html:578), which is about the lab's output, not the spec. A student must ask at which parameters the field is evaluated.",
        "Add to project.html:199 (or the Estimation convention at project.html:214): 'log_likelihood is the log-likelihood at the estimate, so the estimate's own parameters.'"),
    # ---- rung 1 and 2
    row("rung1-lab1-twin-equals-page", "Lab 1 page code equals its twin", "project.html:58-130 vs tests/labs/E3/lab-E3-project-1.py", "PASS",
        f"{S}labs_twins_r3.out: 'page code vs twin differing lines: 0' for lab-E3-project-1."),
    row("rung1-lab1-output-equals-expected", "Lab 1 expected block equals twin output", "project.html:131-137", "PASS",
        f"{S}labs_twins_r3.out: 'stdout lines=7 expected lines=7 identical=True', exit 0, empty stderr."),
    row("rung1-lab1-printed-numbers-rederived", "Lab 1 printed numbers recomputed independently", "project.html:131-137; page_numbers_r3.py", "PASS",
        f"{S}page_numbers_r3.out (section 'lab 1 and lab 2'): CRRA A,B 496 500 / 3000 -513 / 2166 1244; prospect A,B -30 500 / 3000 -762 / 2144 140; P(A) 0.480149, 0.637452, 0.574613; log P(chosen) -0.733658, -1.014598, -0.554059; total -2.302315. All match the expected block."),
    row("rung1-hypothesis-numbers", "Numbers stated before running match the output", "project.html:57", "PASS",
        f"496, 500, -30, 500, P(A)=0.480149, -0.733658 and -2.302315 all match {S}page_numbers_r3.out."),
    row("rung1-interpretation-claims", "Lab 1 interpretation sentences match the output", "project.html:138", "PASS",
        "'two lines per pair and one total': twin prints 7 lines (labs_twins_r3.out). Pair 2 sure $30 gain CE 3000 under both models and the -762 prospect CE of B (page_numbers_r3.out). 'a positive multiple' holds for gamma < 1; Lab 1 uses gamma 0.40."),
    row("rung1-intro-locators", "Locators cited for Lessons 2, 3 and 6 exist", "project.html:53; L02.html:99,616; L03.html:88,173,393; L06.html:61,68,88", "PASS",
        "Re-read this round: L02.html:99 defines def-certainty-equivalent; L03.html:88 defines def-crra-utility; L03.html:173 'Proposition 2.7 (affine transformations leave certainty equivalents unchanged)' grade T, proof at L03.html:393 with a > 0; L06.html:61 'Definition 1.2 (the value function)', 68 'Definition 1.3 (prospect value of a lottery)', 88 'Definition 1.6 (loss aversion)'. All concept links resolve (check_dag PASS)."),
    row("rung2-blanks-vs-twin", "Lab 2 page code vs twin: blanks only", "project.html:144-186 vs tests/labs/E3/lab-E3-project-2.py", "PASS",
        f"{S}labs_twins_r3.out: 4 differing lines, exactly the two '___' blanks (page) and the completed expressions (twin)."),
    row("rung2-printed-values", "Lab 2 printed values", "project.html:183-186", "PASS",
        f"{S}page_numbers_r3.out: z=-0.14, log A=-0.765595182, log B=-0.625595182, prob A=0.465057055, prob B=0.534942945; labs_twins_r3.out: lab-E3-project-2 stdout identical to the expected block."),
    row("rung2-interpretation", "Lab 2 interpretation", "project.html:187", "PASS",
        "The blanks 'the first blank is -math.log1p(math.exp(-z))' and 'second -math.log1p(math.exp(z))' match twin lines 14-15; the completed contribution is never positive."),
    # ---- lab 3
    row("lab3-twin-equals-page", "Lab 3 page code equals twin", "project.html:384-570 vs tests/labs/E3/lab-E3-project-3.py", "PASS",
        f"{S}labs_twins_r3.out: 'page code vs twin differing lines: 0' for lab-E3-project-3."),
    row("lab3-output-equals-expected", "Lab 3 expected block equals twin output", "project.html:571-577", "PASS",
        f"{S}labs_twins_r3.out: stdout identical to the expected block (7 lines), exit 0, empty stderr."),
    row("lab3-printed-values-independent", "Lab 3 printed estimates by the reference estimator", "project.html:571-577; grader/reference.py", "PASS",
        f"{S}lab3_reference_r3.py (out {S}lab3_reference_r3.out): reference.estimate on the 12 ANSWERS gives gamma 0.63521, lambda 6.150316, kappa 2.020107, se 0.31897 / 9.593871 / 1.863777, loglik -7.144517; all seven printed digits match. Round 2's scipy check (lab3_indep.py) is not re-run."),
    row("lab3-eleven-of-twelve-mixed", "Eleven of twelve pairs mixed", "project.html:383; lab-E3-project-3 ANSWERS", "PASS",
        f"{S}lab3_reference_r3.out: 'mixed-sign pairs: 11 | non-mixed pair_ids: [4]'; pair 4 has only losses in A and in B; the expected block prints 'mixed-sign answers: 11'."),
    row("lab3-score-claim", "Score near zero, no maximum check", "project.html:578; lab-E3-project-3 main()", "PASS",
        "Expected block prints largest score component 3.55e-10; main() (project.html:531-546, the same code as the twin) has no Hessian sign check, so 'does not check that this point is a maximum' is accurate."),
    row("lab3-standard-error-larger-than-estimate", "se_lambda larger than lambda_hat", "project.html:383,573", "PASS",
        "Printed se_lambda 9.59 > lambda_hat 6.1503 (expected block lines 572-573)."),
    # ---- hours
    row("hours-project-arithmetic", "Project hours sum to hub figure", "project.html:347-362; index.html:29,40", "PASS",
        "Rows 1+1+3+4+3+2 = 14 (project.html:352-358); project.html:33 and index.html:29 data-hours-project=14."),
    row("hours-module-total", "Module hours: lessons 56 + project 14 = 70", "L01-L08.html data-hours; index.html:31", "PASS",
        "Eight lessons each data-hours=7 (56); index.html:31 'Module E3 · Tier U · 70 hours'; curriculum.json E3 hours 70."),
    row("hours-estimate-plausibility", "Each component's time estimated; total within 30 percent of 14", "project.html:352-358", "PASS",
        "Verifier's central estimate: Rung 1 1 h; Rung 2 0.75 h; instrument and questionnaire file 2.5 h; elicit.py and local run 6 h (MLE, exception table, passing the 45 checks); uncertainty and report 3.5 h; self-assessment 1.5 h. Total about 15 h, 7 percent above 14. The plausible range 12 to 19 h stays within 30 percent except at the top end. The elicit.py component is the largest uncertainty. No time-tracking data exists, so this is an estimate."),
    # ---- exemplars and rubric
    row("exemplar-a-scores", "Exemplar A: blind rubric scores vs annotations", "project.html:612-663", "PASS",
        "Verifier's scoring from the rubric text: C1 2 (count and cents scale missing: 'dollars'), C2 2 (no per-response term), C3 1 (no SE), C4 2 (one limit), C5 1 (no grade or key). Official 2,2,1,2,1 (data-scores line 612). All within one level. Annotations were read earlier in the session, so this is not strictly blind."),
    row("exemplar-b-scores", "Exemplar B: blind rubric scores vs annotations", "project.html:665-725", "PASS",
        "Verifier's scoring from the rubric text: C1 3, C2 3 (names the simplification and loss-aversion pairs; precision pairs are only expected, 'a hypothesis for you to test'), C3 4, C4 3, C5 4. Official 3,4,4,3,4. C2 differs by one level, within the calibration tolerance. Not strictly blind (see exemplar-a-scores)."),
    row("rubric-level-text", "Rubric descriptors are observable", "project.html:597-606", "PASS",
        "Each level names a checkable element: count of pairs, cents, per-response term, the three SEs, named limits, a grade and a key. The C4 level 4 direction example and the C3 'when unreliable' element are observable statements."),
    row("exemplar-word-counts", "Exemplar word counts (line 610)", "project.html:610; memo-text divs", "PASS",
        f"{S}page_numbers_r3.out: exemplar-a 103, exemplar-b 408 (whitespace-split, tags removed, headings included); the page says 103 and 408. A literal split on single spaces of the raw source counts newline runs as words (111 and 418), so the rule's wording 'between spaces' is ambiguous in the raw source. The page's numbers follow the natural reading."),
    row("exemplar-numbers-printed-by-lab3", "Exemplar numbers are Lab 3's printed numbers", "project.html:612-725 vs 571-577", "PASS",
        f"{S}lab3_reference_r3.out: 0.6352, 6.1503, 2.0201, SEs 0.32, 9.59, 1.86, loglik -7.1445 match; exemplar-b's score 3.55e-10 matches the expected block line 576."),
    row("exemplar-b-instrument-facts", "Exemplar B facts about the twelve answers", "project.html:668-679; tests/labs/E3/lab-E3-project-3.py ANSWERS", "PASS",
        f"{S}page_numbers_r3.out: prize minimum -18700 and maximum 19000; 2 or 3 prizes per lottery; probabilities sum to exactly 1 for all 24 lotteries; pair 0 and pair 3 values match the memo text."),
    # ---- reading, notation, DAG, process
    row("reading-claims", "Data-cite claim spans and grades", "project.html:746-750; L07.html:80; L08.html:67,133; L02.html:616", "PASS",
        "data-cite keys in E3 lessons: kahneman1979prospect (L07.html:80, grade C, title only), ellsberg1961risk (L08.html:133, grade C, title only), gilboa1989maxmin (L08.html:67). Epstein-Zin key has no data-cite in L05. Pratt (1964) is named in L02.html:616 'for the name only'. Three of five keys cited with a claim: matches project.html:744."),
    row("reading-keys-in-registry", "Reading keys exist in the registry", "references/references.json", "PASS",
        f"{S}extra_checks_r3.out: 5 of the five reading keys found in references/references.json; verify_refs offline PASS."),
    row("notation-registry", "Symbols vs notation/notation.json", "project.html (110 math spans)", "PASS",
        f"notation.json lists 8 program-wide symbols. The page uses \\Phi once (line 737) with the registered meaning 'standard normal CDF'. It uses no \\mathbb, no \\gamma_3 or \\gamma_4, no \\mathbb{{Q}}. Greek letters gamma, lambda, kappa, zeta, theta, alpha and delta are lesson-local per notation.json 'about'."),
    row("rubric-banned-words-and-process", "Banned phrases and process words", "project.html; grader/*.py", "PASS",
        f"{S}extra_checks_r3.out: banned phrases 0 in project.html and every grader file; process words 0 in project.html."),
    row("dag-links", "Concept links resolve", "project.html:53", "PASS",
        "check_dag E3 PASS (check_dag_E3.out); prospect-theory (L06), certainty-equivalent (L02), crra-utility (L03) resolve to definitions."),
    row("dag-unlinked-names", "Concepts used by name outside the closure (plan section 7)", "grader/test_project.py:901; project.html", "FAIL",
        f"Round 3: the project page no longer uses 'delta method', 'Newton's method' or 'kink' (grep and the concept scan: no hits in project.html). One name remains in learner-visible grader text: test_project.py:901 'each standard error must be the delta-method value from the observed information at the estimate'. 'delta method' is curriculum concept delta-method (module S1, curriculum.json), outside the closure {{E1, M1, M2, M4, P0.1}}, and it is not in the plan section 7 prose-only list. Scan: {S}concept_scan_r3.py (out {S}concept_scan_r3.out): 2 hits, both 'delta-method' in test_project.py.",
        "Replace the message with 'each standard error must be the observed-information value carried by the derivative of each change of coordinates'. Do not add the name to plan section 7."),
    # ---- scope
    row("scope-words-prose", "Universal claims in the prose", "project.html prose", "PASS",
        "'every money output is an int' (test_crra_* and test_wrong_types), 'probabilities sum to exactly 1' (tests), 'every named invalid input' (exception tests), 'no function prints or warns' (test_engine_imports...), 'estimate uses the prospect model only' (estimate has no model argument). Each is backed by a test."),
    row("atlas-milestones-na", "Atlas milestones", "curriculum.json E3 entry", "PASS",
        "Not applicable: the E3 curriculum entry has no atlas milestone. Recorded as not applicable, not as a pass of a check."),
    row("studios-na", "Studios", "curriculum.json", "PASS", "Not applicable: E3 is a module, not a studio."),
    row("data-figures-na", "Data and figures", "project.html", "PASS",
        f"{S}extra_checks_r3.out: no <svg>, <img> or data-files on the page. The engine's data is SIMULATED by instance.py (SIMULATED label on the page)."),
    row("lab-runtime", "Lab runtime under 10 s and seeded", "project.html labs 1-3; page_smoke", "PASS",
        "page_smoke_project.out: lab-E3-project-1 0.0 s, lab-E3-project-2 0.0 s, lab-E3-project-3 0.1 s; no randomness in the labs."),
    # ---- grader
    row("grader-test-count", "Test count on page equals collect-only", "grader/test_project.py; project.html:203", "PASS",
        "collect-only 45 = page 45 (gate-collect-39)."),
    row("grader-named-conditions-tested", "Named conditions tested, including the gain of zero probability (round-2 FAIL)", "test_project.py:663-688; project.html:227", "PASS",
        f"Round 3: test_a_gain_of_zero_probability_does_not_make_a_lottery_mixed (test_project.py:663-688) added. mut-e3d2-01 is KILLED by it on seed 0 ({S}mutate_E3_seeds0-9_round3_full.txt)."),
    row("grader-kinks-docstrings", "Docstrings do not claim kinks (round-2 FAIL)", "test_project.py:474-530,535-536", "PASS",
        "grep -i kink on grader/*.py: no hits. test_score_is_zero_at_the_estimate (lines 524-530) states a numerical safeguard, not smoothness."),
    row("grader-seed49-docstring", "Seed-49 numbers in the docstring", "test_project.py:873-884", "PASS",
        f"{S}page_numbers_r3.out (seed 49 section): se_lambda 135.054 (1e-5) and 97.6747 (1e-6): '135.05' and '97.67' match; -27.677% -> '-27.7%'; se_gamma 0.0947359 and 0.0798321 -> '0.09474' and '0.07983'; -15.732% -> '-15.7%'."),
    row("grader-seed49-1.3pct", "Reverse-order sensitivity 1.3 percent and 0.4 percent (round-2 FAIL)", "test_project.py:880-884", "PASS",
        f"{S}page_numbers_r3.out: reverse vs forward se_lambda +1.278% at 1e-5 (135.054 to 136.779) and +0.421% at 1e-6 (97.675 to 98.086). The docstring's '+1.3%' and '+0.4%' with the two steps named are correct."),
    row("grader-every-model-comments", "Comments about model lists (round-2 FAIL)", "test_project.py:960-968", "PASS",
        "Comments now read 'the increasing models that this suite uses' and 'the concave, increasing models that this suite uses'; the lists are named as samples."),
    row("grader-second-participant", "Second participant is not a fixed answer", "test_project.py:35, 584-606", "PASS",
        "INST2 = make_instance(SEED + 7919); test_estimate_on_a_second_participant... runs on INST2 and passes on reference."),
    row("grader-reference-instance-starter", "reference.py, instance.py, starter.py deployable and run (changed in round 2)", "grader/reference.py; grader/instance.py; grader/starter.py", "PASS",
        "reference.py changed only in a comment (line 23); instance.py changed only in a docstring (lines 151-156). Re-run: run_graders 50/50 and the 20-seed instance validity check (instances_20_seeds_r3.out: validity problems none; 20 of 20 distinct true-parameter triples, wealth values, choice vectors and reference estimates)."),
    row("grader-exception-named-only", "Exceptions demanded only for named conditions", "test_project.py:50-62, 286-297, 346-367, 545-596, 682-700", "PASS",
        "must_raise is ValueError only and is used for the five named conditions; wrong-type test allows any exception and then requires int."),
    row("grader-se-oracle-docstring", "SE oracle: docstring vs code", "test_project.py:873-902", "FAIL",
        "The docstring says 'each standard error must match one of the two within 10% relative, as the score check accepts either step'. The code (lines 888-898) accepts a step only if all three standard errors match at that same step. A student whose se_gamma matches the 1e-5 oracle and whose se_lambda matches the 1e-6 oracle passes the docstring's rule and fails the code. The page says nothing about the step for the standard errors.",
        "Either make the code check each standard error against either step (per key, as the docstring says), or change the docstring to 'all three standard errors must match at one of the two steps'."),
    row("grader-recovery-test-duration", "Each test under 5 s in Pyodide (BUILDER_RULES 5.3.4)", "test_project.py:566-581 (test_estimate_recovers_... 47_of_50_seeds)", "FAIL",
        "durations_r3.sh (out durations_r3.out): on seed 0 in CPython the test_estimate_recovers_the_true_parameters_within_four_standard_errors_on_47_of_50_seeds takes 12.68 s (13.02 s in an earlier run); the next test takes 0.18 s. The whole suite takes 13.4 s in CPython and 30.6 s in Pyodide (page_smoke_project.out), so the single test is far above 5 s in the browser too. The per-test Pyodide time was not measured separately; the suite total is what page_smoke reports.",
        "Make the recovery test cheaper in the browser: for example, cache the estimates per seed for the whole run and split the 50-seed sweep so that no single test does 50 full fits, or reduce the per-fit cost of the reference. Re-run page_smoke and report the per-test times."),
    row("grader-failure-messages-no-leak", "Failure messages never leak the answer", "test_project.py (expect/must_raise messages)", "PASS",
        "Seeded-test messages name properties and carry no values. Canned exact cases quote their answer in the message (for example line 253 '-25 cents', line 264 'round half up to 3'), but the same value is printed as a literal in the same test source, so nothing hidden is revealed."),
    row("instances-20-seeds", "Sample 20 seeds: valid and materially different", "course/modules/E/E3/grader/instance.py; ledgers/E3/scripts/E3-d-r3/instances_20_seeds_r3.py", "PASS",
        f"{S}instances_20_seeds_r3.out: 20 seeds; 200 pairs each; prizes integer, 2 or 3 per lottery, magnitudes 500 to 50000; probabilities exact, positive, sum 1; at least 100 mixed pairs; true parameters in stated ranges; 20 of 20 distinct parameter triples, wealth values, choice vectors and reference estimates; validity problems: none."),
    # ---- mutants
    row("mut-e3d2-01", "Round-2 mutant e3d2_01 (gain of zero probability counts as a gain)", "ledgers/E3/mutants/e3d2_01_gain_zero_probability_counts_as_mixed.py", "PASS",
        f"KILLED by test_a_gain_of_zero_probability_does_not_make_a_lottery_mixed (seed 0) in {S}mutate_E3_seeds0-9_round3_full.txt."),
    row("mut-e3d2-02", "Round-2 mutant e3d2_02 (SE from outer product of scores)", "ledgers/E3/mutants/e3d2_02_se_from_outer_product_of_scores.py", "PASS",
        f"KILLED by test_standard_errors_match_the_coordinate_change_oracle (seed 0) in {S}mutate_E3_seeds0-9_round3_full.txt."),
    row("mut-e3d2-03", "Round-2 mutant e3d2_03 (probability sum rounded to twelve places)", "ledgers/E3/mutants/e3d2_03_prob_sum_rounded_to_twelve_places.py", "PASS",
        f"KILLED by test_probabilities_must_be_nonnegative_and_sum_to_exactly_one (seed 0) in {S}mutate_E3_seeds0-9_round3_full.txt."),
    row("mut-min-three-new", "At least three new student-error mutants written this round", "ledgers/E3/mutants/e3d3_01..04", "PASS",
        f"Four new mutants written by {S}make_e3d3_mutants.py: e3d3_01 probability text read through float (killed by test_log_likelihood_matches_oracle...), e3d3_02 prospect ignores lambda (killed by test_prospect_matches_oracle...), e3d3_03 observed information keeps only the diagonal (killed by test_standard_errors_match...), e3d3_04 se_lambda applies the loss factor twice (killed by test_standard_errors_match...). All four KILLED on seed 0."),
    row("mut-all-77-killed", "Every mutant in ledgers/E3/mutants is killed on seeds 0-9", "ledgers/E3/mutants/ (77 files)", "PASS",
        f"{S}mutate_E3_seeds0-9_round3_full.txt: 'mutate_graders E3: PASS (77/77 killed)', exit 0. No survivors; the earlier 73-mutant run (mutate_E3_seeds0-9.txt) also had 73/73."),
    row("mut-first-docstring-r10n", "Mutant first docstring line names the student error (round-2 FAIL)", "ledgers/E3/mutants/r10n04, r10n05, r10n07, e3d1_01..04", "PASS",
        "The tool's own descriptions now name the student error: r10n04 'Probabilities are normalised instead of refused...', r10n05 'The prospect inverse for a non-negative lottery value uses the exponent 1 - gamma...', r10n07 'The standard error of kappa is reported in log kappa...', e3d1_01..04 likewise (mutate_E3_seeds0-9_round3_full.txt)."),
    row("mut-r10n06-equivalent", "Ruling 9: equivalents moved out of mutants/ with a proof", "ledgers/E3/mutants/r10n06_logit_log_term_naive_exp_overflow.py", "PASS",
        "r10n06 is KILLED by test_log_likelihood_stays_finite_for_a_large_choice_precision (seed 0), so it is a real fault for the grader, not an equivalent. ledgers/E3/equivalent/ does not exist at a007712 (round-2 README was removed), and no survivor is left in mutants/."),
    row("mut-e3d1-01-to-04", "Round-1 mutants e3d1_01..04 killed", "ledgers/E3/mutants/e3d1_0*.py", "PASS",
        "All four KILLED on seed 0 (mutate_E3_seeds0-9_round3_full.txt)."),
]

fragment = {
    "unit": "E3",
    "slice": "d",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-d, round 3 (did not build E3; did not see the round-1/2 builders' context)",
    "pin": "a007712fdbfc8b4851123f4de76b5310ac5a9e64",
    "base": "c737272f5bdef4a027417989cd52254555e8a0bb (round-2 pin). Delta c737272f..a007712f read hunk by hunk for project.html, grader/reference.py, grader/instance.py, grader/test_project.py, tests/labs/E3/lab-E3-project-1.py and lab-E3-project-3.py, ledgers/E3/mutants (new e2_0x, e3d2_0x, r10n04-07 edits, equivalent/ removed) and the E3 lesson locators (L02, L03, L06, L07, L08).",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD3-E3-d",
    "scratch": "/tmp/e3d_r3_work (grader copy), /tmp/e3d_r3_collect, /tmp/e3d_r3_assert",
    "verified_at": "2026-11-03T04:30:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 3 on a007712. Re-verified every round-2 FAIL row: spec-zeta-used-before-definition, spec-kinks-claim, "
        "grader-kinks-docstrings, grader-named-conditions-tested, grader-seed49-1.3pct, grader-every-model-comments, "
        "mut-e3d2-01, mut-first-docstring-r10n are PASS now. Still FAIL: spec-ruling6-kappa-wording (ruling wording conflicts "
        "with the physics; Architect decision), dag-unlinked-names (one 'delta-method' remains in learner-visible grader text). "
        "New FAIL rows: spec-context-sentences, spec-log-likelihood-field, grader-se-oracle-docstring, grader-recovery-test-duration. "
        "Out of slice (not counted): repo-wide 'ruff format --check .' reports ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py. "
        "Not checked: live verify_refs (CI job); repo-wide pytest (only the three page, memo and docs modules, and the E3 "
        "gates); the in-browser run in a real browser (page_smoke is headless); Pyodide per-test timing (only the suite total was "
        "measured); alternatives on seeds 10-49 (E3 window is 0-9); the questionnaire UI was read, not clicked; "
        "the rubric calibration used the rubric text after reading the annotations earlier in this session (not strictly blind). "
        "ledgers/E3/scripts/E3-d-r3/ already contained tracked files from another attempt (alt4_failures.py, cards_scan.py, "
        "write_fragment_r3.py, mutate_E3_r3.out and others); they were not used or modified. ledgers/E3/E3-d.json was "
        "overwritten in this checkout only (round-3 fragment; not committed)."
    ),
    "summary": "",
}

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = (
    f"E3-d round 3: verdict FAIL. {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
    f"{counts['UNVERIFIABLE']} UNVERIFIABLE. Mutants {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed. "
    "FAIL rows: spec-ruling6-kappa-wording, spec-context-sentences, spec-log-likelihood-field, dag-unlinked-names, "
    "grader-se-oracle-docstring, grader-recovery-test-duration."
)

out = Path("ledgers/E3/E3-d.json")
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {out}: {len(rows)} rows, {len(mutants)} mutants, verdict {fragment['verdict']}")
