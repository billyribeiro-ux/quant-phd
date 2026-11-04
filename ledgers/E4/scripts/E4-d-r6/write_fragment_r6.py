"""Write the E4 slice-d round-6 verifier fragment ledgers/E4/E4-d.json from the logs of this round.

Every row cites a command, a script under ledgers/E4/scripts/E4-d-r6/ or a repository line. The mutant list is read from
the mutation log of this round. Usage: python -I write_fragment_r6.py <checkout-root>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
L = "ledgers/E4/scripts/E4-d-r6/logs"
S = "ledgers/E4/scripts/E4-d-r6"
P = "course/modules/E/E4/project.html"
G = "course/modules/E/E4/grader"


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> dict[str, str]:
    out = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        out["fix"] = fix or ""
    return out


CALIB_FIX = ("Calibrate from a passage-only extract (no annotation, no official scoring line) that a verifier reads before "
             "the annotated page; the fresh verifier then scores blind and records the scores in its own fragment. This "
             "round's verifier had already read the official scoring lines of project.html:533-660 before scoring, so the "
             "blind requirement cannot be met here.")

rows: list[dict[str, str]] = [
    row("E4d-cmd-check-projects", "2.6-structure", f"{P}; {G}/", "PASS",
        f"tools/check_projects.py --unit E4 -> 'check_projects E4: PASS' ({L}/check_projects.txt)"),
    row("E4d-cmd-check-pages", "2.9-structure", P, "PASS",
        f"tools/check_pages.py --unit E4 -> 'check_pages E4: PASS' ({L}/check_pages.txt)"),
    row("E4d-cmd-check-dag", "2.9-DAG", P, "PASS", f"tools/check_dag.py --unit E4 -> 'check_dag E4: PASS' ({L}/check_dag.txt)"),
    row("E4d-cmd-run-labs", "2.5-labs", "tests/labs/E4/lab-E4-project-1.py, -2.py, -3.py", "PASS",
        f"tools/run_labs.py --unit E4 -> 'run_labs E4: PASS (12/12)', exit 0 ({L}/run_labs.txt); each project twin alone "
        f"under python -I -W error exits 0 ({L}/twin_lab-E4-project-{{1,2,3}}.txt)"),
    row("E4d-cmd-run-graders", "2.6-autograder", f"{G}/reference.py", "PASS",
        f"tools/run_graders.py --unit E4 --seeds 0-49 -> 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)' ({L}/run_graders.txt)"),
    row("E4d-cmd-page-smoke-project", "2.9-smoke", P, "PASS",
        f"tools/page_smoke.py --unit E4 --pages project (run alone) -> 'page_smoke E4: PASS'; in-browser grader 'All 34 tests pass' ({L}/page_smoke_project_r6.txt)"),
    row("E4d-cmd-ruff", "conventions", "repository", "PASS",
        f".venv/bin/ruff check . -> 'All checks passed!'; ruff format --check . -> '553 files already formatted' ({L}/ruff_check_r6.txt, {L}/ruff_format_r6.txt)"),
    row("E4d-cmd-mypy-workspace", "conventions", "tests/labs/E4 and course/modules/E/E4/grader", "PASS",
        f"mypy --no-incremental tests/labs/E4 course/modules/E/E4/grader -> 'Success: no issues found in 16 source files' ({L}/mypy_r6.txt)"),
    row("E4d-cmd-mypy-plan-command", "conventions", "tests/labs/E4; grader", "PASS",
        f"same mypy run as E4d-cmd-mypy-workspace ({L}/mypy_r6.txt)"),
    row("E4d-cmd-pytest-relevant", "conventions", "tests/test_memo_exemplars.py, test_page_checks.py, test_labs.py, test_run_labs.py", "PASS",
        f"pytest -q -p no:cacheprovider on the four modules -> all dots, exit 0 ({L}/pytest_relevant_r6.txt)"),
    row("E4d-cmd-verify-refs", "2.1-citations", "references/references.json (E4 keys)", "PASS",
        f"tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' ({L}/verify_refs_offline_r6.txt); "
        f"tools/verify_refs.py --unit E4 (live) -> 'live re-verification of E4: 3 of 560 entries, 0 problems' ({L}/verify_refs_E4_live_r6.txt)"),
    row("E4d-cmd-collect", "2.6-autograder", f"{G}/test_project.py", "PASS",
        f"pytest --collect-only with reference.py copied as solver.py -> '34 tests collected'; the same run passes 34 of 34 ({L}/collect_r6.txt); {P}:320 says 34 checks"),
    row("E4d-lab-project-1", "2.5-labs", f"{P} #lab-E4-project-1; tests/labs/E4/lab-E4-project-1.py", "PASS",
        f"{S}/lab_page_vs_twin_r6.py: code_equal_twin=True, expected_equal_output=True, exit 0 ({L}/lab_page_vs_twin_r6.txt); the Lab 1 numbers recomputed in {L}/model_checks_r6.txt"),
    row("E4d-lab-project-2", "2.5-labs", f"{P} #lab-E4-project-2; tests/labs/E4/lab-E4-project-2.py", "PASS",
        f"{S}/lab_page_vs_twin_r6.py: completion=True; the only page line differing from the twin is 'return ___' (every other line equal); expected block equals twin output ({L}/lab_page_vs_twin_r6.txt)"),
    row("E4d-lab-project-3", "2.5-labs", f"{P} #lab-E4-project-3; tests/labs/E4/lab-E4-project-3.py", "PASS",
        f"{S}/lab_page_vs_twin_r6.py: code and expected block equal twin and its run ({L}/lab_page_vs_twin_r6.txt); 9 printed rows equal the independent values in {L}/model_checks_r6.txt"),
    row("E4d-num-lab-hypotheses", "2.2-numbers", f"{P}:57, :176, :375 (Lab hypothesis paragraphs)", "PASS",
        f"Lab 1 numbers recomputed independently ({L}/model_checks_r6.txt, 'Lab 1' line): lambda*=0.57937525, tau_bar=tau_y=0.18904110, informativeness 0.15898618, b_u/b_s=-3.45199422, gap(0+)=+0.053092, gap(1)=-0.080731. Lab 2 ('Lab 2' line): lambda*=0.57052263, informativeness 0.12466375, gap(0+)=+0.037435, gap(1)=-0.071386. Lab 3 values equal the closed form (E4d-math-prop4)."),
    row("E4d-num-exemplar-table", "2.2-numbers", f"{P} Results passage and table (Exemplar B, :~626-641)", "PASS",
        f"every table row equals the Lab 3 printed row ({L}/twin_lab-E4-project-3.txt); ratios 0.6978/0.5582 = 1.25009 (displays 1.2501), 0.8373/0.5582 = 1.50000 (displays 1.5000); exact ratios 1.250000000000 and 1.500000000000 ({L}/model_checks_r6.txt, Prop 5 section)"),
    row("E4d-num-box-bounds", "2.2-numbers", f"{P} Inputs paragraph (:314); {G}/instance.py:14-17", "PASS",
        f"tau_bar(0.150)=0.0976232722, tau_bar(0.120)=0.2375667836, tau_y(1) at sd=0.75 = 0.3076923077 ({L}/model_checks_r6.txt, 'box bounds'); the page's 0.097623 <= tau_bar <= 0.237567 and 0.30769 match; all 50 seeds satisfy 0 < tau_bar < tau_y(1) ('instance seeds' section)"),
    row("E4d-prose-lede-directional", "2.9-prose", f"{P}:37 (lede)", "PASS",
        "at fixed lambda, tau_y = lambda^2 tau_e^2/(lambda^2 tau_e + a^2 sd^2) falls as sd rises (Proposition 1 formula); on the interior tau_y = tau_bar (Proposition 4), which does not depend on sd, so informativeness is constant in sd (Lab 3 prints 0.1920 at sd 0.500, 0.625, 0.750)"),
    row("E4d-math-lemmas", "2.4-mathematics", f"{P}:265-273 (Lemmas 1-3)", "PASS",
        f"Lemma 1 (line 266) now states the hypothesis 'v is conditionally normal given F' that its proof uses (proof line 267 uses the normal mgf). Re-derived: g(x)=x(m-p)-(a/2)x^2 V, g'(x)=0 at x*=(m-p)/(aV), -a g(x*)=-(m-p)^2/(2V). Lemma 2 integral re-derived; numerical check S=0.3,V=1: 0.8770580193 both ({L}/model_checks_r6.txt). Lemma 3 is the total-variance identity with V constant."),
    row("E4d-math-prop1", "2.4-mathematics", f"{P}:276-283 (Proposition 1, steps 0-4)", "PASS",
        f"exact Fraction check: the clearing residual lambda*x_I+(1-lambda)*x_U-u, with x_I, x_U from Lemma 1 and the conditional means of steps (1)-(2), is identically zero for (lambda, sigma) = (1/2,3/5), (3/10,7/10), (9/10,1/4), (1,3/2), (1/100,1) ({L}/model_checks_r6.txt); steps (0)-(4) re-derived by hand, including the uniqueness step"),
    row("E4d-math-prop2", "2.4-mathematics", f"{P}:285-287 (Proposition 2)", "PASS",
        f"Corr(v,p)^2 computed from Cov and Var of the linear price equals tau_y/(1+tau_y) exactly (Fraction) for five (lambda, sigma) pairs ({L}/model_checks_r6.txt); the lambda=0 case re-derived (x_U=u, p=-a u/tau_v)"),
    row("E4d-math-prop3", "2.4-mathematics", f"{P}:288-294 (Proposition 3)", "PASS",
        f"gap computed from Omega = Var(v-p) = 1 + Var(p) - 2 Cov(v,p) equals reference.indifference_gap to 1.1e-16 at 20 (sd, c, lambda) points ({L}/model_checks_r6.txt, 'gap values' section); G(0+) closed form equals gap at lambda=1e-9 to 1e-11; the sign identity and the G(0+) limit re-derived"),
    row("E4d-math-prop4", "2.4-mathematics", f"{P}:295-299 (Proposition 4)", "PASS",
        f"bisection vs closed form on the 3x3 grid: worst |difference| 4.4e-16; small noise (sd 1e-6, 1e-9, 1e-12) relative differences below 1e-15 ({L}/model_checks_r6.txt)"),
    row("E4d-math-prop5", "2.4-mathematics", f"{P}:300-302 (Proposition 5 and paragraph)", "PASS",
        f"d lambda*/d sigma = lambda*/sigma by the closed form (lambda* proportional to sigma); ratios 1.250000000000 and 1.500000000000 ({L}/model_checks_r6.txt); k(t) strictly increasing and tau_bar strictly decreasing in c re-derived"),
    row("E4d-math-assumptions", "2.4-mathematics", f"{P}:256-262 (A1-A5), :276, :285, :288, :295, :300 (use of each assumption), :604-606 (Exemplar B use-list)", "PASS",
        "A1-A5 are numbered (ol.assumptions); each proposition states 'Assume A1 to A5' or names its hypotheses; the Lemmas state their hypotheses; the normalization argument in A1 and the wealth-shift argument in A3 are checked against Lemma 1 (demand and utility depend on v-p only)"),
    row("E4d-notation", "2.4-notation", f"{P} math spans; notation/notation.json", "PASS",
        f"macros in math spans: Corr, Cov, E, Normal, Var (registered: notation/notation.json:5 '\\\\E', :13-22 '\\\\Var' '\\\\Cov' '\\\\Corr', :37 '\\\\Normal') and standard TeX; no T, \\\\Phi, \\\\gamma, R^\\\\ast, \\\\mathbb symbol ({S}/prose_scan_r6.txt counts symbols=0); local symbols tau, lambda, sigma, kappa, Omega, V_I, V_U, tau_bar are defined in the notation paragraph (:~243) or at first use"),
    row("E4d-banned-phrases", "2.9-prose", P, "PASS", f"{S}/prose_scan_r6.py over visible prose: banned=0 hits ({L}/prose_scan_r6.txt)"),
    row("E4d-process-words", "2.9-prose", P, "PASS",
        f"{S}/prose_scan_r6.py: process-word pattern hits only at line 522, the rubric criterion name 'C2 · Solver and verification' (a learner-facing term, not a build-process word); no builder, round, fixture, ruling, architect, blind or REQUEST in visible prose ({L}/prose_scan_r6.txt)"),
    row("E4d-dag-links", "2.9-DAG", P, "PASS",
        f"{S}/links_check_r6.py: 35 hrefs (27 distinct) all resolve, no problems ({L}/links_check_r6.txt); data-concept links: expected-utility (E3 via concepts.html, in the closure), noisy-rational-expectations-equilibrium (L06, earlier lesson), price-informativeness (L07, earlier lesson)"),
    row("E4d-registry-muth", "2.1-citations", f"{P} reading list (:681)", "PASS",
        "references/references.json muth1961rational: Muth, 'Rational Expectations and the Theory of Price Movements', Econometrica 29(3):315, 1961, DOI 10.2307/1909635, status verified; live verify_refs for E4 0 problems"),
    row("E4d-registry-milgrom", "2.1-citations", f"{P}:682", "PASS",
        "references/references.json milgrom1982information: Milgrom & Stokey, 'Information, trade and common knowledge', J. Econ. Theory 26(1):17-27, 1982, DOI 10.1016/0022-0531(82)90046-1, status verified; the page attributes no statement to it (:322, :677-680)"),
    row("E4d-cites-only-registry", "2.1-citations", f"{P} data-cite (:681-682)", "PASS",
        "grep of data-cite in project.html: exactly two occurrences, muth1961rational and milgrom1982information, both registry keys"),
    row("E4d-spec-context-sentences", "2.9-prose", f"{P}:312 (Context)", "PASS", "Context dd has four sentences (2-4 required)"),
    row("E4d-spec-questions", "2.6-spec", f"{P}:316-322 (Required outputs, Constraints, Grading mode)", "FAIL",
        "Questions a competent student would have to ask: (1) which point of the final bracket is reported as informed_fraction: Constraints (:318) gives only the stopping rule, and the midpoint appears only in Exemplar B's Method passage (:614-616); the autograder accepts any point within 1e-8 relative, so the answer exists but the spec does not state it. (2) None other: the constants, the exceptions, the gap at 0 and at 1, the informativeness at 0 and at 1, and the output keys are all stated.",
        "In the Constraints entry (project.html:318) state the reported point, for example 'report the midpoint of the final bracket (any point of it satisfies the stated tolerance)'. Rebuild and re-run check_pages and page_smoke."),
    row("E4d-spec-ladder", "2.6-spec", f"{P}:40-49 (ladder), :51-305, :308, :669-675", "PASS",
        "ladder order is rung 1 worked example (Lab 1), rung 2 completion (Lab 2, class lab completion, graded by run_labs), rung 3 spec (:308), rung 4 stretch (:669); the rung-1 'why' content is judged in E4d6-rung1-why"),
    row("E4d-prose-scope-words", "2.9-prose", P, "PASS",
        f"every scope word in visible prose (grep, 60+ hits, {L}/prose_scan_r6.txt and this round's scan) checked: 'every instance' (:314) is backed by the box bound (E4d-num-box-bounds); 'every number' and 'exactly the keys' are tested (test_project.py:178-179, :216-218); 'at all 484 points' (:376) is computed by Lab 3; 'every printed gap' (:626) is the table max 3.55e-14; the A1 and A3 normalization 'every' statements are derivations (Lemma 1)"),
    row("E4d-prose-simulated-labs", "2.9-prose", f"{P} Labs 1-3 (:57, :176, :375) and Inputs (:313)", "PASS",
        "Lab 1, Lab 2 and Lab 3 hypotheses and the Inputs paragraph say SIMULATED; grader/instance.py:1 says 'All values are SIMULATED'"),
    row("E4d-prose-simulated-exemplars", "2.9-prose", f"{P}:530 (exemplar intro)", "PASS", "the exemplar intro says 'on a SIMULATED instance' and names the Lab 3 grid point"),
    row("E4d-hours-project", "2.6-hours", f"{P}:33 (eyebrow), :341-352 (#hours); course/modules/E/E4/index.html:29; curriculum.json E4 hours 100", "PASS",
        "hub data-hours-lessons=72 and data-hours-project=28 sum to 100 (= curriculum hours); project header 28; hours table rows 1+1+5+8+5+5+3 = 28; project share 28% is within 10-40%"),
    row("E4d-hours-estimate", "2.6-hours", f"{P} #hours table (:341-352)", "PASS",
        "verifier estimate, read from the specification and the labs: reading and Labs 1-3 about 3 h; derivation of Propositions 1-5 and Lemmas 1-3 about 7 h; solver and local suite 4-6 h; grid runs and display 3-4 h; write-up 4-6 h; self-assessment 2-3 h; total 23-29 h, within 30% of 28 h (19.6 to 36.4)"),
    row("E4d-rubric-observable", "2.6-rubric", f"{P}:517-527 (#rubric), C1 level 1 descriptor (:521)", "PASS",
        "all 20 descriptors are observable; C1 level 1 now reads 'Omits at least one of the payoff, the signal, the noise supply, the preferences or the equilibrium condition', separating it from level 2 ('gives the equilibrium condition in words only'); C3 level 1 ('no grid and no derivation') is separated from level 2 ('with its grid')"),
    row("E4d-exemplar-A-calibration", "2.6-rubric", f"{P}:533-597 (Exemplar A, data-scores 2,2,1,2,1)", "UNVERIFIABLE",
        "Blind scoring could not be done in this session: this verifier read the Exemplar A official scoring line and annotations (:534, :~541-595) before scoring. Rubric-only scoring from the descriptors gives C1 2, C2 2, C3 1, C4 2, C5 1, which equals data-scores; but that is not a blind score.",
        CALIB_FIX),
    row("E4d-exemplar-B-calibration", "2.6-rubric", f"{P}:598-661 (Exemplar B, data-scores 4,4,4,4,4)", "UNVERIFIABLE",
        "Blind scoring could not be done in this session: this verifier read the Exemplar B official scoring line (:600) and the Model passage and annotation (:603-607) before scoring. Rubric-only scoring gives C1 4, C2 4, C3 4, C4 4, C5 3 (C5 level 3 requires that each derived claim be graded; the passage names its basis but gives no T/A/B grade); the annotated 4 is within one level, which the calibration allows, but the score is not blind.",
        CALIB_FIX),
    row("E4d-exemplar-annotations-hidden", "2.6-rubric", "course/assets/js/rubric.js:147-150; project.html data-reveal and .annotation", "PASS",
        "rubric.js setRevealed hides '.annotation, [data-reveal]' until the form reveals them; rubric.js is byte-identical to the round-5 pin (git diff 7376a5e..4bd8cb9 empty for course/assets/js)"),
    row("E4d-grader-exceptions", "2.6-autograder", f"{G}/test_project.py:191-234; {G}/reference.py:30-33; {P}:328-329", "PASS",
        "noise volume 0, negative, inf, nan are rejected with ValueError; 1e-12 and 1e-9 (tiny positive) are accepted; info cost -0.01 and -1e-12 rejected, 0.0 accepted; messages contain the table's text; the page names only these two conditions"),
    row("E4d-grader-messages", "2.6-autograder", f"{G}/test_project.py:49-68 and every expect() call", "PASS",
        "all failure messages name a property or the condition label and carry no computed value (read every expect()/pytest.fail call this round; pytrace=False and __tracebackhide__)"),
    row("E4d-grader-oracle", "2.6-autograder", f"{G}/test_project.py:79-170", "PASS",
        "the oracle (fixed-point price, moment regressions, 1001-node trapezoid over the standard normal) does not import solver.py; the reference's gap values agree with an independent Omega form to 1e-16 ({L}/model_checks_r6.txt), and the reference passes every oracle test"),
    row("E4d-grader-instances", "2.6-autograder", f"{G}/instance.py; {G}/test_project.py:37-40", "PASS",
        "seeds 0-49: every instance inside the box, 0 < tau_bar < tau_y(1), 50 distinct (sd, cost) pairs ({L}/model_checks_r6.txt); seeds 0-19 print distinct informed fractions 0.375 to 0.827 (same log)"),
    row("E4d-grader-instance-docstring", "2.6-autograder", f"{G}/instance.py:1-21", "PASS",
        "the box bounds 0.097623 and 0.237567 (unrounded 0.0976232722, 0.2375667836), 1/(1+4*0.75^2) = 0.30769 and the interior claim are recomputed ({L}/model_checks_r6.txt)"),
    row("E4d-grader-test-docstring", "2.6-autograder", f"{G}/test_project.py:9-15, :366, :379, :439, :450-451", "PASS",
        "the module docstring's 'recomputed by oracle functions' is true for every test except the closed-form Proposition 4 checks, which the docstring names; test_fraction_falls_with_the_cost asserts the monotonicity its docstring names; test_fraction_is_proportional asserts the proportionality its docstring names; the tiny-root docstring matches the stop rule"),
    row("E4d-grader-reference-docstring", "2.6-autograder", f"{G}/reference.py:3-10, :22-23, :92-93, :105-107", "PASS",
        "the units sentence is correct (uninformed expected utility in [-1,0) because 0 < F_U <= 1); the 200-halving comment is correct (2^-200 = 6.2e-61, so the relative tolerance is reached for roots above 6.2e-49); the gap-at-zero limit and the lambda=1 hypothetical agent match Proposition 3"),
    row("E4d-grader-stdlib", "2.6-autograder", f"{G}/test_project.py:404-413; reference.py; ledgers/E4/alternatives/*.py", "PASS",
        "the suite asserts stdlib-only imports and passes for the reference; ast check: alt_1..alt_5 import only math (grep of imports this round)"),
    row("E4d-mutants-existing", "2.6-mutation", "ledgers/E4/mutants/mutant_01..mutant_10", "PASS",
        f"tools/mutate_graders.py --unit E4 --seeds 0-9: all ten builder mutants KILLED ({L}/mutate_graders_r6_seeds0-9.txt)"),
    row("E4d-mutants-new", "2.6-mutation", "ledgers/E4/mutants/mutant_d11..mutant_d18, mutant_d6_01..d6_10", "PASS",
        f"all KILLED in {L}/mutate_graders_r6_seeds0-9.txt"),
    row("E4d2-mutants-r2", "2.6-mutation", "ledgers/E4/mutants/mutant_r2_*.py", "PASS", f"all four KILLED ({L}/mutate_graders_r6_seeds0-9.txt)"),
    row("E4d3-mutants-r3", "2.6-mutation", "ledgers/E4/mutants/mutant_r3_*.py", "PASS", f"all four KILLED ({L}/mutate_graders_r6_seeds0-9.txt)"),
    row("E4d3-mutant-tolerance-survives", "2.6-mutation", f"{G}/test_project.py:44 (TOL_ROOT); ledgers/E4/mutants/mutant_r3_tolerance_1e-9.py", "PASS",
        f"KILLED by test_fraction_is_the_oracle_root[first] (seed 0) ({L}/mutate_graders_r6_seeds0-9.txt)"),
    row("E4d-mutants-total", "2.6-mutation", "ledgers/E4/mutants/ (61 mutants)", "FAIL",
        f"tools/mutate_graders.py --unit E4 --seeds 0-9 -> 'mutate_graders E4: FAIL (59/61 killed)' ({L}/mutate_graders_r6_seeds0-9.txt). The two survivors are the verifier's round-6 mutants 06 and 07 (E4d6-mutant-06, E4d6-mutant-07). The round-5 survivors (bracket floor 1e-12 and sixty halvings) are now KILLED.",
        "Add the test in ledgers/E4/scripts/E4-d-r6/proposed_unit_fraction_positive_cost_test.txt to grader/test_project.py; it kills mutants 06 and 07 on every seed tried and passes the reference and all five alternatives (E4d-alternatives)."),
    row("E4d-equivalent", "2.6-mutation", "ledgers/E4/equivalent/literal_price_sign.py; README.md", "PASS",
        f"{S}/equivalent_literal_sign_r6.py: the literal-sign variant and the reference agree on 3000 random inputs with largest absolute output difference 0.0 ({L}/equivalent_literal_sign_r6.txt); the README proof (b_u enters only as b_u*b_u) is consistent with reference.py:73"),
    row("E4d-alternatives", "2.6-alternatives", "ledgers/E4/alternatives/alt_1..alt_5.py", "PASS",
        f"{S}/run_candidates_r6.py seeds 0-49: reference, alt_1, alt_2, alt_3, alt_4, alt_5 each 50/50 pass ({L}/alternatives_seeds0-49.txt). Note: plan §5.5 names alt 4 as damped fixed-point; the file is a secant method. The extra damped fixed-point candidate (E4d6-alt-extra-damped) passes 50/50, so the over-constraint check covers that algorithm too."),
    row("E4d-starter", "2.6-autograder", f"{G}/starter.py", "PASS",
        f"starter.py raises NotImplementedError; run_candidates_r6.py on starter.py: 'starter.py: FAIL (0/50 seeds pass)', as required ({L}/starter_seeds0-49.txt)"),
    row("E4d-browser-local-parity", "2.6-autograder", f"{G}/test_project.py; tools/page_smoke.py", "PASS",
        f"local pytest: 34 passed (QF_SEED=0, --assert=plain -W error); in-browser: 'All 34 tests pass' ({L}/page_smoke_project_r6.txt)"),
    row("E4d-runtime", "2.6-autograder", f"{G}/test_project.py", "PASS",
        "local suite 0.04 s for 34 tests; in-browser 0.8 s (page_smoke); every test is far below the 5 s and 60 s limits"),
    row("E4d2-exemplar-B-C1-annotation", "2.6-rubric", f"{P}:603-607 (Exemplar B Model passage and annotation)", "PASS",
        "the use-lists now agree with the propositions: A2 is used in Propositions 1 to 4 (Proposition 2 at lambda=0 uses clearing; Proposition 3 uses the normal noise; Proposition 4 uses sigma); A3 in 1 to 3 (through a and Lemma 1); A4 and A5 in 1 to 3; the 'names the results' annotation is correct"),
    row("E4d3-cara-defined-twice", "2.9-prose", f"{P}:259 (A3); course/modules/E/E4/L06.html:66-67", "PASS",
        "project.html has 0 <dfn> elements; L06.html:67 holds the single <dfn>constant absolute risk aversion (CARA) utility</dfn> (Definition 6.2)"),
    row("E4d3-anchors-links", "2.9-DAG", f"{P} (all href targets)", "PASS", f"{S}/links_check_r6.py: every href target and fragment resolves ({L}/links_check_r6.txt)"),
    row("E4d3-no-figures-no-data", "2.8-figures", P, "PASS",
        "no svg, img or data-files on project.html (prose_scan external count 0); the only data is the SIMULATED instance from the seed"),
    row("E4d3-spec-stop-rule-and-constraints", "2.6-spec", f"{P}:318 (Constraints)", "PASS",
        f"the stop rule (1e-12 times the upper end, or 200 halvings) matches {G}/reference.py:21-22 and :138; 'no network' is stated and not enforced by any test (a stated limit, not a grader fault)"),
    row("E4d3-atlas-studios-na", "2.6-atlas", "curriculum/curriculum.json (atlas array, E4 entry); project.html", "PASS",
        "no Atlas entry names E4 and the E4 curriculum entry has no atlas key; no studio applies; no contract check is required"),
    row("E4d4-mutant-absolute-tolerance-survives", "2.6-mutation", f"{G}/test_project.py:437-446; ledgers/E4/mutants/mutant_r4_absolute_bracket_tolerance.py", "PASS",
        f"KILLED by test_small_noise_root_is_relatively_accurate[1e-06] (seed 0) ({L}/mutate_graders_r6_seeds0-9.txt)"),
    row("E4d4-alt4-wrong-on-small-noise", "2.6-alternatives", "ledgers/E4/alternatives/alt_4.py", "PASS", f"alt_4 passes seeds 0-49 ({L}/alternatives_seeds0-49.txt)"),
    row("E4d4-alt1-docstring", "2.6-alternatives", "ledgers/E4/alternatives/alt_1.py:1", "PASS",
        "docstring 'bisection with a fixed 120 halvings and no tolerance check' matches solve_model (range(120), no stop test)"),
    row("E4d4-equivalent-price-slope", "2.6-mutation", "ledgers/E4/scripts/E4-d-r4/check_equivalence_r4.py (candidate b_s = lambda tau_e / D)", "PASS",
        "re-run this round: 'sign mismatches of the gap on the interior grid: 0 of 89700'; 'largest |difference| in any solver output over 3000 random inputs: 2.27e-13' (the candidate is not in mutants/: its outputs agree with the reference within the root tolerance)"),
    row("E4d4-calibration-blind", "2.6-rubric", f"{P}:533-597 (Exemplar A)", "UNVERIFIABLE",
        "Exemplar A was not scored blind in this session (see E4d-exemplar-A-calibration): the official scoring was read first.",
        CALIB_FIX),
    row("E4d4-proposed-test-validated", "2.6-mutation", f"{G}/test_project.py:421-446 (the round-4 proposed small-noise test)", "PASS",
        "the test is in the grader and the suite passes 34 of 34 for the reference; the round-4 survivor it targets is now killed"),
    row("E4d4-mutants-killed-r4", "2.6-mutation", "ledgers/E4/mutants/mutant_r4_*.py, mutant_r4f_*.py", "PASS", f"all KILLED ({L}/mutate_graders_r6_seeds0-9.txt)"),
    row("E4d4-exemplar-B-results-numbers", "2.2-numbers", f"{P} Results passage and table (Exemplar B)", "PASS",
        f"'every printed gap has absolute value below 4e-14' (table max 3.55e-14); '1.2501 and 1.5000' (1.250090, 1.500000); informativeness 0.1920, 0.1420, 0.0889 constant across sd within each cost ({L}/twin_lab-E4-project-3.txt)"),
    row("E4d5-mutant-bracket-floor", "2.6-mutation", "ledgers/E4/mutants/mutant_r5_bracket_floor_1e-12.py", "PASS",
        f"now KILLED by test_tiny_noise_root_is_relatively_accurate[1e-12] (seed 0) ({L}/mutate_graders_r6_seeds0-9.txt)"),
    row("E4d5-mutant-sixty-halvings", "2.6-mutation", "ledgers/E4/mutants/mutant_r5_sixty_halvings_no_tolerance.py", "PASS",
        f"now KILLED by test_tiny_noise_root_is_relatively_accurate[1e-11] (seed 0) ({L}/mutate_graders_r6_seeds0-9.txt)"),
    row("E4d5-mutant-uninformed-precision", "2.6-mutation", "ledgers/E4/mutants/mutant_r5_uninformed_posterior_precision_informed.py", "PASS",
        f"KILLED by test_indifference_holds_at_an_interior_fraction[first] (seed 0) ({L}/mutate_graders_r6_seeds0-9.txt)"),
    row("E4d5-calibration-B-blind", "2.6-rubric", f"{P}:598-661 (Exemplar B)", "UNVERIFIABLE",
        "Exemplar B was not scored blind in this session: this verifier read the Exemplar B official scoring line and its Model passage and annotation before scoring. Round 5's blind score is not carried forward because the subject (the passages and annotations) was re-read and is not a fresh blind score.",
        CALIB_FIX),
    # ---- round-6 rows (new mutants, new candidate, spec-compliant variants, the rung-1 'why' check)
    row("E4d6-mutant-06", "2.6-mutation", f"ledgers/E4/mutants/mutant_r6_06_cost_scales_whole_gap.py; {G}/test_project.py (no test at lambda*=1 with cost > 0)", "FAIL",
        f"student error: the whole gap multiplied by exp(a c). It SURVIVES seeds 0-9 ({L}/mutate_graders_r6_seeds0-9.txt). It violates the stated behaviour 'indifference_gap is the gap of Proposition 3 at lambda*' (project.html:316-317) at lambda* = 1 with a positive cost; the existing unit-fraction test (test_unit_fraction_is_reported_at_zero_cost) uses cost 0, where exp(a c) = 1, so no test reaches the mutated branch. Sign-preserving, so the root is unaffected.",
        "Add the test in ledgers/E4/scripts/E4-d-r6/proposed_unit_fraction_positive_cost_test.txt (run(0.6, 0.05): lambda*=1 by Proposition 4 since tau_bar=0.6375 >= tau_y(1)=0.4098; checks the gap against oracle_gap(1.0, 0.6, 0.05)). Validated: kills this mutant on seeds 0-9 and passes the reference, alt_1..alt_5 and the damped candidate (logs/validate_proposed_test_r6.txt)."),
    row("E4d6-mutant-07", "2.6-mutation", f"ledgers/E4/mutants/mutant_r6_07_unit_informativeness_discounted_by_cost.py; {G}/test_project.py", "FAIL",
        f"student error: at lambda* = 1 the informativeness is multiplied by exp(-c). It SURVIVES seeds 0-9 ({L}/mutate_graders_r6_seeds0-9.txt). It violates the stated 'price_informativeness is Corr(v,p)^2 at lambda*' (project.html:316-317, Proposition 2); the only unit-fraction test uses cost 0, so exp(-c) = 1 there.",
        "Same test as E4d6-mutant-06: its informativeness assertion at (0.6, 0.05) against oracle_informativeness(1.0, 0.6) kills this mutant (logs/validate_proposed_test_r6.txt)."),
    row("E4d6-mutants-new-killed", "2.6-mutation", "ledgers/E4/mutants/mutant_r6_01..mutant_r6_05 (memorised answers; informativeness share at 1; fraction rounded; zero-fraction gap at one; sd not squared)", "PASS",
        f"all five KILLED on seed 0 ({L}/mutate_graders_r6_seeds0-9.txt): r6_01 by test_noise_volume_zero_is_rejected, r6_02 by test_unit_fraction_is_reported_at_zero_cost, r6_03 by test_gap_is_the_oracle_gap_at_the_reported_fraction[first], r6_04 by test_zero_fraction_is_reported_above_the_cost_threshold, r6_05 by test_indifference_holds_at_an_interior_fraction[first]"),
    row("E4d6-spec-variants-08-09", "2.6-mutation", "ledgers/E4/equivalent/mutant_r6_08_bracket_reports_lower_end.py; mutant_r6_09_stop_rule_never_relative.py; ledgers/E4/equivalent/README.md", "PASS",
        f"both are spec-compliant: outputs differ from the reference within the bisection tolerance (worst relative 5.0e-13 in lambda on 20,030 inputs, worst absolute 1.25e-13 elsewhere; {L}/equivalence_within_tolerance_r6.txt); the nested-bracket proof and the no-test-separates argument are in the README; they are documented, not counted as mutants"),
    row("E4d6-stop-rule-measured", "2.6-autograder", "grader/reference.py:22-23, :138; ledgers/E4/alternatives/alt_5.py", "PASS",
        f"worst relative error against the Proposition 4 closed form over 4,000 interior inputs: reference 7.4e-13, alt_5 7.4e-13, variant 09 5.0e-13, variant 08 1.2e-12 (relative to the root; at most 1e-12 relative to the upper end, the stated rule) ({L}/alt5_error_vs_closed_form_r6.txt). Passing the grader at 1e-8 does not depend on the reported point."),
    row("E4d6-alt-extra-damped", "2.6-alternatives", "ledgers/E4/scripts/E4-d-r6/candidates/damped_fixed_point_log_r6.py", "PASS",
        f"damped fixed-point iteration on log(lambda) (the algorithm plan §5.5 item 4 names): 50/50 seeds pass ({L}/damped_candidate_seeds0-49.txt)"),
    row("E4d6-rung1-why", "2.6-spec", f"{P}:171 (Lab 1 interpretation, steps 1-6)", "FAIL",
        "BUILDER_RULES §5.1 requires rung 1 'annotated with why at every step', and plan §5.1 asks for a why note on each step. The interpretation paragraph says what each printed line is ('Step 2 evaluates ... checks the sign change', 'Step 4 prints the root') and gives a reason only for the sign-change check and the ratio check. It gives no why for step 1 (inputs), the halving (why a bisection, and why 60 halvings reach float resolution), the zero gap as the defining condition of the informed fraction, or the informativeness as the measure of Proposition 2.",
        "Add one 'why' clause per step to the Lab 1 interpretation paragraph (project.html:171): step 1 the inputs fix the model; step 2 the bisection needs a sign change at the ends; step 3 each halving halves the bracket, and 60 halvings reach the float resolution 1.1e-16; step 4 the zero gap is the indifference condition of Proposition 3; step 5 the ratio is Proposition 1's coefficient identity; step 6 the informativeness is Corr(v,p)^2 of Proposition 2."),
]

mutant_lines = (root / L / "mutate_graders_r6_seeds0-9.txt").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mutant_lines:
    if not (line.startswith("KILLED ") or line.startswith("SURVIVED ")):
        continue
    head, _, rest = line.partition(": ")
    name = head.split(" ", 1)[1]
    desc, _, killed = rest.rpartition(" -> ")
    killed_by = None if line.startswith("SURVIVED") else killed.split(" (seed")[0].strip()
    mutants.append({"id": name.removesuffix(".py"), "description": desc, "killed_by": killed_by})
fails = [r for r in rows if r["status"] != "PASS"]
counts = {k: sum(1 for r in rows if r["status"] == k) for k in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
fragment = {
    "unit": "E4",
    "slice": "d",
    "round": 6,
    "verifier": "Haiku independent verifier, E4 slice d, round 6 (did not build E4)",
    "pin": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07",
    "base": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f (round-5 pin). Delta in this slice since 7376a5e: course/modules/E/E4/project.html (Lab 1 interpretation, Rung 3 Constraints/Grading mode wording, Lemma 1 hypothesis and Proposition 1 step (0), C1 level 1 descriptor, A1/A3/A5 wording, Exemplar B Model passage and use-lists, Proposition 4 and Lab 2 lead-in), grader/reference.py (docstrings only), grader/test_project.py (module docstring; new test_tiny_noise_root_is_relatively_accurate), ledgers/E4/alternatives/alt_5.py (lo=0.0), ledgers/E4/mutants/ (new d6_01..10 and r5 files). Lab twins project-1..3, instance.py, starter.py, rubric.js, references.json, notation.json and course/assets/js are byte-identical to the round-5 pin.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE6-E4-d",
    "scratch": "/tmp/e4r6-collect-* and /tmp/e4r6-prop-* (temporary copies for the collect-only count and the proposed-test validation; removed)",
    "verified_at": "2026-11-04T19:47:52+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "muth1961rational: record verified (Econometrica 29(3):315, 1961, DOI 10.2307/1909635); live verify_refs for E4 keys: 3 entries, 0 problems this round.",
        "milgrom1982information: record verified (JET 26(1):17-27, 1982, Milgrom & Stokey); the page attributes no statement to it.",
    ],
    "freshness_flags": [],
    "notes": [
        "Round 6 re-verified every row from scratch on the pin. Every round-5 non-PASS row was re-checked: E4d-math-lemmas, E4d-rubric-observable, E4d2-exemplar-B-C1-annotation, E4d-alternatives, E4d5-mutant-bracket-floor and E4d5-mutant-sixty-halvings are now PASS with evidence; E4d-mutants-total is FAIL again on two new survivors (round-6 mutants 06 and 07); E4d4-calibration-blind stays UNVERIFIABLE.",
        "Blind calibration: this verifier had read the official scoring lines and annotations of both exemplars (project.html:533-661) before scoring, so the calibration rows are UNVERIFIABLE, not PASS. The rubric-only scores (A: 2,2,1,2,1; B: 4,4,4,4,3) are recorded in the rows for the record; B's C5 gives 3 because the passage names its basis but grades nothing, and the annotated 4 is within one level.",
        "Spec-compliant variants 08 and 09 are documented in ledgers/E4/equivalent/README.md and not counted as mutants (outputs within the stated bisection tolerance; measured in logs/equivalence_within_tolerance_r6.txt and logs/alt5_error_vs_closed_form_r6.txt).",
        "Plan deviation (not a fault): ledgers/E4/alternatives/alt_4.py is a secant method, where plan §5.5 item 4 names damped fixed-point; the damped fixed-point candidate in scripts/E4-d-r6/candidates passes 50/50 seeds.",
        "Model checks: the proofs of Lemmas 1-3 and Propositions 1-5 were re-derived by hand, Proposition 1's clearing identity and Proposition 2's squared correlation were checked in exact rational arithmetic, and Propositions 3-5 were checked numerically against an independent Omega-based gap (logs/model_checks_r6.txt). No mathematical defect was found in this round.",
        "Learner-visible clarity: two items are FAIL with fixes (spec does not state the reported point of the final bracket; Lab 1 interpretation lacks a why for each step). Both are wording fixes.",
        "Not checked: the in-browser Pyodide run was checked only by page_smoke (no manual browser session); the self-assessment form's JavaScript behaviour was not exercised beyond the rubric.js source; the live registry run covered the three E4 keys only (E4 keys as the tool reports them); the Assumption-1 normalization argument is accepted as a derivation at the level of a short argument, not an exhaustive proof.",
    ],
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": len(mutants),
        "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
        "non_pass_ids": [r["id"] for r in fails],
    },
}
out = root / "ledgers/E4/E4-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(fragment["summary"], indent=1))
