"""Build the round-9 E4 slice-d ledger fragment from the verifier's logs (rows are written by hand below).

Run: python3 -I build_fragment_r9.py <repo-root>
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
L = "ledgers/E4/scripts/E4-d-r9/logs"
PIN = __import__("subprocess").run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

R = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)


CMD = "ledgers/E4/scripts/E4-d-r9/logs/"
# ---- commands run this round
row("E4d-cmd-check-projects", "2.6-structure", "course/modules/E/E4/project.html; course/modules/E/E4/grader/", "PASS",
    f"`.venv/bin/python tools/check_projects.py --unit E4` -> 'check_projects E4: PASS', exit 0 ({CMD}check_projects.txt).")
row("E4d-cmd-check-pages", "2.9-structure", "course/modules/E/E4/project.html", "PASS",
    f"`tools/check_pages.py --unit E4` -> 'check_pages E4: PASS', exit 0 ({CMD}check_pages.txt).")
row("E4d-cmd-check-dag", "2.9-dag", "course/modules/E/E4/project.html", "PASS",
    f"`tools/check_dag.py --unit E4` -> 'check_dag E4: PASS', exit 0 ({CMD}check_dag.txt).")
row("E4d-cmd-run-labs", "2.5-labs", "tests/labs/E4/lab-E4-project-1.py, -2.py, -3.py", "PASS",
    f"`tools/run_labs.py --unit E4` -> 'run_labs E4: PASS (12/12)', exit 0 ({CMD}run_labs.txt).")
row("E4d-cmd-run-graders", "2.6-autograder", "course/modules/E/E4/grader/reference.py", "PASS",
    f"`tools/run_graders.py --unit E4 --seeds 0-49` -> 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.5 s)', exit 0 ({CMD}run_graders.txt).")
row("E4d-cmd-page-smoke-project", "2.9-smoke", "course/modules/E/E4/project.html", "PASS",
    f"`tools/page_smoke.py --unit E4 --pages project` run alone -> 'in-browser grader: All 42 tests pass', 'page_smoke E4: PASS', exit 0 ({CMD}page_smoke_project.txt).")
row("E4d-cmd-ruff", "gate", "course/modules/E/E4 and tests/labs/E4", "PASS",
    f"`.venv/bin/ruff check` -> 'All checks passed!'; `ruff format --check` -> '16 files already formatted' ({CMD}ruff_check.txt, {CMD}ruff_format.txt).")
row("E4d-cmd-mypy-workspace", "gate", "tests/labs/E4 and course/modules/E/E4/grader", "PASS",
    f"`.venv/bin/mypy --no-incremental course/modules/E/E4/grader tests/labs/E4` -> 'Success: no issues found in 16 source files', exit 0 ({CMD}mypy.txt).")
row("E4d-cmd-mypy-plan-command", "gate", "tests/labs/E4; grader", "PASS",
    f"Same mypy run as E4d-cmd-mypy-workspace ({CMD}mypy.txt).")
row("E4d-cmd-pytest-relevant", "gate", "tests/test_memo_exemplars.py, test_page_checks.py, test_labs.py, test_run_labs.py", "PASS",
    f"`.venv/bin/python -m pytest -q` on the four files -> all dots, exit 0 ({CMD}pytest_relevant.txt).")
row("E4d-cmd-verify-refs", "2.1-citations", "references/references.json (E4 keys: muth1961rational, milgrom1982information)", "PASS",
    f"`tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0 ({CMD}verify_refs_offline.txt). Live run not repeated (no reference record changed in the delta).")
row("E4d-cmd-collect", "2.6-autograder", "course/modules/E/E4/grader/test_project.py", "PASS",
    f"Scratch copy (instance.py, test_project.py, reference.py as solver.py): `pytest --collect-only -q` -> '42 tests collected' ({CMD}collect.txt). Equals the page's '42 checks' (project.html Grading mode).")
row("E4d-lab-project-1", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-1; tests/labs/E4/lab-E4-project-1.py", "PASS",
    f"Page code equals the twin line for line (98 lines, 0 differing, {CMD}lab_twin_check_r9.txt); twin run `python -I -W error` exit 0, 0 bytes stderr; output equals the expected block.")
row("E4d-lab-project-2", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-2; tests/labs/E4/lab-E4-project-2.py", "PASS",
    f"Page code (63 lines) differs from the twin only at the blanked return line (`return ___`); twin run `-I -W error` exit 0; output equals the expected block ({CMD}lab_twin_check_r9.txt).")
row("E4d-lab-project-3", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-3; tests/labs/E4/lab-E4-project-3.py", "PASS",
    f"Page code equals the twin (114 lines, 0 differing); twin run `-I -W error` exit 0; output equals the expected block, including 484 of 484 ({CMD}lab_twin_check_r9.txt).")
row("E4d-num-lab-hypotheses", "2.2-numbers", "course/modules/E/E4/project.html:57, :176, :376", "PASS",
    "Lab 1 hypothesis (+0.053092, -0.080731, 0.57937525, -3.45199422, 0.18904110, 0.15898618) equals the expected block; Lab 2 (+0.037435, -0.071386, 0.57052263, 0.12466375) equals its expected block; Lab 3 table values 0.5582/0.6978/0.8373 at cost 0.120 and 0.1920/0.1420/0.0889 informativeness and |gap| < 1e-13 equal the printed block ({CMD}lab_twin_check_r9.txt, {CMD}numbers_r9.txt).")
row("E4d-num-exemplar-table", "2.2-numbers", "course/modules/E/E4/project.html Exemplar B table and passage (:629-641)", "PASS",
    f"All nine table rows equal the Lab 3 printed rows; ratios 0.6978/0.5582 = 1.25009 and 0.8373/0.5582 = 1.50000; unrounded ratio 1.2500000000 and 1.5000000000 ({CMD}numbers_r9.txt); 'every printed gap below 4e-14': max 3.55e-14.")
row("E4d-num-box-bounds", "2.2-numbers", "course/modules/E/E4/project.html:314; course/modules/E/E4/grader/instance.py:14-17", "PASS",
    f"Recomputed: tau_bar(0.150) = 0.09762327, tau_bar(0.120) = 0.23756678, 1/(1+4*0.75^2) = 0.3076923 ({CMD}numbers_r9.txt).")
row("E4d-prose-lede-directional", "2.3-grades", "course/modules/E/E4/project.html:37 (lede)", "PASS",
    "Lede: the fraction rises with the noise on the interior and the informativeness does not depend on the noise there. Checked against Prop 4 (lambda* = a sigma k(tau_bar), linear in sigma) and Prop 2/4 (informativeness tau_bar/(tau_v+tau_bar) has no sigma); Lab 3 table: at each cost the informativeness is constant over the three noise volumes.")
row("E4d-math-lemmas", "2.4-mathematics", "course/modules/E/E4/project.html:265-273 (Lemmas 1-3)", "PASS",
    "Re-derived by hand: Lemma 1 (g(x*) = (m-p)^2/(2aV), -a g(x*) = -(m-p)^2/(2V)); Lemma 2 (integral gives (V/(V+S))^(1/2)); Lemma 3 (law of total variance).")
row("E4d-math-prop1", "2.4-mathematics", "course/modules/E/E4/project.html:276-283", "PASS",
    "Re-derived step (3): coefficient on u is (1-lambda) tau_y kappa - D b_s kappa - a = -lambda tau_e kappa - a, so kappa = -a/(lambda tau_e); step (1) tower property E[v|s,p] = E[v|s]; b_s formula reproduces Lab 1 printed b_s = 0.39718750 and tau_y = 0.18904110.")
row("E4d-math-prop2", "2.4-mathematics", "course/modules/E/E4/project.html:285-287", "PASS",
    "Re-derived Corr(v,p)^2 = (b_s^2/tau_v^2)/((1/tau_v) b_s^2 (1/tau_v + 1/tau_y)) = tau_y/(tau_v+tau_y); lambda = 0 case gives b_s = 0 and Corr = 0.")
row("E4d-math-prop3", "2.4-mathematics", "course/modules/E/E4/project.html:288-293", "PASS",
    "Re-derived: sign G = sign(V_U - e^{2ac} V_I); multiplying by (tau_v+tau_y)(tau_v+tau_e)e^{-2ac} gives tau_bar - tau_y; G(0+) formula from Omega -> 1/tau_v + a^2 sigma^2/tau_v^2, V_U -> 1/tau_v, b_u -> -a/tau_v (b_s/lambda -> tau_e/tau_v). Reference gap_at_zero agrees with the oracle to 1.1e-16 over seeds 0-49 (measure_oracle_gap0_r9.txt).")
row("E4d-math-prop4", "2.4-mathematics", "course/modules/E/E4/project.html:295-298", "PASS",
    "Re-derived lambda* = a sigma sqrt(tau_bar/(tau_e(tau_e - tau_bar))) from tau_y(lambda*) = tau_bar; interior informativeness 1 - e^{2ac} tau_v/(tau_v+tau_e) equals tau_bar/(tau_v+tau_bar) numerically (numbers_r9.txt). Bisection vs closed form on the 3x3 grid: largest 2.1e-13.")
row("E4d-math-prop5", "2.4-mathematics", "course/modules/E/E4/project.html:300-301", "PASS",
    "d lambda*/d sigma = lambda*/sigma (linear); tau_bar strictly decreasing in c, k(t)^2 = t/(tau_e(tau_e-t)) strictly increasing, so lambda* decreasing in c; informativeness tau_bar/(tau_v+tau_bar) has no sigma.")
row("E4d-math-assumptions", "2.4-mathematics", "course/modules/E/E4/project.html:257-262 (A1-A5)", "PASS",
    "All five read in full. A3 wealth-shift argument checked (common w_0 multiplies every expected utility by exp(-a w_0) > 0). A4 b_s != 0 for lambda > 0 is consistent with Prop 1 denominators.")
row("E4d-notation", "2.4-notation", "course/modules/E/E4/project.html (math spans, 393 spans); notation/notation.json", "PASS",
    f"Registered symbols (T, Phi, gamma_3, gamma_4, R^*, R^{{e*}}, R_f, Q) do not occur in the page. Registered macros used: \\E, \\Var, \\Cov, \\Corr, \\Normal. Local symbols (tau, lambda, sigma, a, c, u, v, p, s, x, w, Omega, V_I, V_U, G, F_I, F_U, kappa, b_s, b_u, D, beta) are defined on the page (Notation paragraph and the proofs). No collision found ({CMD}numbers_r9.txt and the macro/symbol scan in this round).")
row("E4d-banned-phrases", "2.9-prose", "course/modules/E/E4/project.html; grader/*.py; tests/labs/E4/lab-E4-project-*.py", "PASS",
    "grep for TODO, TBD, lorem, for brevity, omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, 'about <n>', roughly, historically, ellipsis: no hit in the page or the labs. Only '0.09762327...' style truncations in instance.py and project.html (decimal digits, not omitted content).")
row("E4d-process-words", "2.9-prose", "course/modules/E/E4/project.html; grader/*.py; labs", "PASS",
    "grep for round, verifier, builder, ruling, architect, audit, previous, fixed in, fixer, mutant, alternative in the page: only 'rounded', 'round(' in code and the ordinary word 'rounds' in the rubric's notation. No process word in learner text.")
row("E4d-dag-links", "2.9-dag", "course/modules/E/E4/project.html", "PASS",
    "check_dag PASS (E4d-cmd-check-dag). Concept links: noisy-rational-expectations-equilibrium -> L06.html#def-noisy-rational-expectations-equilibrium (L06.html:169); price-informativeness -> L07.html#def-price-informativeness (L07.html:62); expected-utility -> concepts.html (index). CARA cited as Definition 6.2 of Lesson 6 (L06.html:66); not redefined with dfn (grep: no dfn in project.html).")
row("E4d-registry-muth", "2.1-citations", "course/modules/E/E4/project.html:684; references/references.json", "PASS",
    "Key muth1961rational present: Muth, 'Rational Expectations and the Theory of Price Movements', Econometrica 29(3), 1961, doi 10.2307/1909635, verified_by crossref (read this round). The page attributes no statement to it (project.html:682).")
row("E4d-registry-milgrom", "2.1-citations", "course/modules/E/E4/project.html:685; references/references.json", "PASS",
    "Key milgrom1982information present: 'Information, trade and common knowledge', Journal of Economic Theory 26(1), 1982, pp. 17-27, doi 10.1016/0022-0531(82)90046-1, verified_by crossref (read this round). The page attributes no statement to it.")
row("E4d-cites-only-registry", "2.1-citations", "course/modules/E/E4/project.html data-cite (:684-685)", "PASS",
    "The only data-cite keys are muth1961rational and milgrom1982information; both are registry keys (E4d-registry-muth, -milgrom). mascolell1995microeconomic is not cited (grep).")
row("E4d-spec-context-sentences", "2.6-spec", "course/modules/E/E4/project.html:312 (Context)", "PASS",
    "Context has four sentences, within the 2 to 4 required; read in full.")
row("E4d-spec-questions", "2.6-spec", "course/modules/E/E4/project.html:314-322 (Inputs, Required outputs, Constraints, Grading mode)", "PASS",
    "Questions a competent student would still ask: (1) whether solve_model must accept integer or numpy inputs (not stated; no test depends on it); (2) the value of the gap at lambda* = 1 (answered: hypothetical uninformed agent, Prop 3); (3) the solver's stop rule and tolerance (answered in Constraints). No blocking gap found; see E4d3-spec-stop-rule-and-constraints for the enforceability of the stop rule.")
row("E4d-spec-ladder", "2.6-spec", "course/modules/E/E4/project.html:40-49, :51-305, :308, :669-675", "PASS",
    "Rung 1 = Lab 1 (one instance, six printed steps, each with an interpretation); Rung 2 = Lab 2 (one blank, class 'lab completion'); Rung 3 = spec, autograder, report; Rung 4 = stretch (two items). Read in full this round.")
row("E4d-prose-scope-words", "2.4-scope", "course/modules/E/E4/project.html:326 (Exception table paragraph)", "PASS",
    f"Round-8 FAIL re-verified: the page now limits the 'no upper bound' claim to noise volumes from a positive value up to 1e150 and information costs from 0 up to 350. Probe: 168-point grid over sd in [1e-300, 1e150] x c in [0, 350] and 20000 random points (log-uniform sd, uniform c, seed 9): 0 invalid outputs ({CMD}probe_scope_r9.txt, {CMD}scope_dense_r9.txt). Outside the range the solver raises ZeroDivisionError (sd 1e154, from 1/tau_y after the a^2 sd^2 term overflows) and OverflowError (c >= 355), as the page says ('may raise any exception').")
row("E4d-prose-simulated-labs", "2.5-labs", "course/modules/E/E4/project.html:57, :176, :314, :375", "PASS",
    "Each lab's hypothesis states its inputs are SIMULATED or stated values; grep finds no open( in the three project twins (numbers_r9.txt).")
row("E4d-prose-simulated-exemplars", "2.8-data", "course/modules/E/E4/project.html:530 (exemplar intro)", "PASS",
    "Exemplar intro: 'Two report excerpts on a SIMULATED instance' (read this round).")
row("E4d-hours-project", "2.9-hours", "course/modules/E/E4/project.html:33, :35, :341-352; course/modules/E/E4/index.html:29", "PASS",
    "Eyebrow 28 h, data-hours-project 28, #hours total 28; hub data-hours-lessons 72 + data-hours-project 28 = 100 (index.html:29).")
row("E4d-hours-estimate", "2.6-hours", "course/modules/E/E4/project.html #hours (:344-351)", "PASS",
    "Components 1+1+5+8+5+5+3 = 28 (recomputed). Own estimate per component (rung 1 about 1 h, rung 2 about 1 h, derivation of Props 1-5 about 5 h, solver with tests about 8 h, grid about 5 h, report about 5 h, self-assessment about 3 h) gives 28 h, within 30%.")
row("E4d-rubric-observable", "2.6-rubric", "course/modules/E/E4/project.html:517-527 (#rubric)", "PASS",
    "Five criteria, four levels each, read in full. Every descriptor names something a grader can see (for example C2 level 2 'no tolerance or stop rule'; C3 level 1 'a sign with no grid and no derivation'). No vague descriptor found.")
row("E4d-exemplar-A-calibration", "2.6-rubric-calibration", "course/modules/E/E4/project.html:533-597 (Exemplar A, data-scores 2,2,1,2,1)", "UNVERIFIABLE",
    "Blind scoring not possible for this verifier: the official scoring line (project.html:538) and the annotations were displayed by this round's full read before any score was given. Not scored.",
    "A fresh verifier with no prior read of project.html must score Exemplar A from a text extract with data-scores, data-reveal and annotation elements removed, then compare within one level per criterion.")
row("E4d-exemplar-B-calibration", "2.6-rubric-calibration", "course/modules/E/E4/project.html:598-661 (Exemplar B, data-scores 4,4,4,4,4)", "UNVERIFIABLE",
    "Blind scoring not possible: the official scoring line (project.html:603) and the Model annotation were displayed by this round's full read.",
    "Same as E4d-exemplar-A-calibration: a fresh verifier scores Exemplar B from a stripped extract.")
row("E4d-exemplar-annotations-hidden", "2.6-rubric", "course/assets/js/rubric.js:147-150; project.html data-reveal and .annotation", "PASS",
    f"rubric.js unchanged since 0dee921a (`git diff --stat 0dee921a c93dd526 -- course/assets/js/` empty); project.html has two data-reveal elements (grep this round); the annotation and the exemplar scores are hidden by the form (rubric.js:147-150, read).")
row("E4d-grader-exceptions", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:191-234, :242-280; reference.py:26-34; project.html:326-332", "PASS",
    "Named conditions tested in both directions: noise 0, -SD, inf, nan rejected; 1e-12 accepted; cost -0.01 and -1e-12 rejected; cost 0 accepted. Only the two named conditions demand ValueError (six must_raise calls). Re-run: 42/42 on the reference, seeds 0, 7, 49 (ledgers/E4/scripts/E4-d-r9/logs/ref_seed*.txt).")
row("E4d-grader-messages", "2.6-autograder", "course/modules/E/E4/grader/test_project.py (every expect() and pytest.fail call)", "PASS",
    "Read in full. Each hint names the property. The only f-strings are in must_raise, where the message prints the condition label, not a value (grep).")
row("E4d-grader-oracle", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:79-170", "PASS",
    "Oracles read in full: fixed-point price (oracle_price), moments (oracle_regressions), quadrature (_NODES trapezoid over the standard normal), gap, informativeness, bisection root. The module does not import reference.py (the import block at the top of the file names only ast, importlib, math, os, sys, pytest); the closed form in the small-noise tests is written from the page formula.")
row("E4d-grader-instances", "2.6-autograder", "course/modules/E/E4/grader/instance.py; test_project.py:37-40", "PASS",
    f"Draws over seeds 0-49: noise_sd in [0.503, 0.741], info_cost in [0.12, 0.149]; 50 distinct instances ({CMD}numbers_r9.txt). run_graders instance checks PASS (E4d-cmd-run-graders).")
row("E4d-grader-instance-docstring", "2.6-autograder", "course/modules/E/E4/grader/instance.py:1-21", "PASS",
    "Docstring numbers recomputed (E4d-num-box-bounds). It says the bound is derived there and not re-checked by the suite, which is accurate (the suite has no bound test).")
row("E4d-grader-test-docstring", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:481-484 (tiny-root docstring)", "PASS",
    f"2^-200 = 6.22e-61; 6.22e-61 / 1e-12 = 6.2e-49. Probe of the reference's loop ({CMD}probe_scope_r9.txt): the tolerance limb fires for roots 6.3e-49 and above and not for 6.2e-49 and below.")
row("E4d-grader-reference-docstring", "2.6-autograder", "course/modules/E/E4/grader/reference.py:21-23", "PASS",
    "Same 6e-49 threshold (probe). The comment at :22-23 is accurate.")
row("E4d-grader-stdlib", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:436-445; ledgers/E4/alternatives/*.py", "PASS",
    f"test_solver_imports_only_the_standard_library passes on the reference and on alt_1..alt_5 and alt_v9_1..3 (50/50 seeds each, {CMD}alternatives_builder_seeds0-49.txt, {CMD}alternatives_v9_seeds0-49.txt).")
row("E4d-runtime", "2.6-autograder", "course/modules/E/E4/grader/test_project.py", "PASS",
    "run_graders slowest reference seed 0.5 s; in-browser suite 0.8 s (page_smoke). Under the 5 s per test and 60 s suite limits.")
row("E4d-browser-local-parity", "2.6-autograder", "course/modules/E/E4/grader/test_project.py; tools/page_smoke.py", "PASS",
    f"In-browser: 42 of 42 pass (page_smoke, seed 954794812). Local: `python -I -W error -m pytest -q --assert=plain` with QF_SEED 0, 7, 49 on the reference: 42 passed each ({CMD}ref_seed0.txt, ref_seed7.txt, ref_seed49.txt).")
row("E4d2-exemplar-B-C1-annotation", "2.3-grades", "course/modules/E/E4/project.html:604-607 (Exemplar B Model passage)", "UNVERIFIABLE",
    "Partly checked: Props 1 to 5 each state 'Assume A1 to A5' (project.html:279-301). The exemplar's proposition-by-proposition mapping of A1 to A5 was not checked against each proof in this round, and the exemplar is part of the blind calibration, which is itself UNVERIFIABLE.",
    "Check each proposition's use of A1 to A5 against its proof, then amend the Exemplar B annotation to match or drop the mapping.")
row("E4d3-cara-defined-twice", "2.9-prose", "course/modules/E/E4/project.html:259 (A3); course/modules/E/E4/L06.html:57, :66", "PASS",
    "CARA is cited as Definition 6.2 of Lesson 6 on the page and not defined with <dfn> there (grep: zero dfn in project.html). L06.html:66 is the only definition (<dfn>constant absolute risk aversion (CARA) utility</dfn>).")
row("E4d3-anchors-links", "2.9-structure", "course/modules/E/E4/project.html (href targets)", "PASS",
    "check_pages PASS (E4d-cmd-check-pages); internal anchors #spec, #model, #exceptions, #report, #grader-section, #rubric, #self-assessment, #lab-E4-project-3 exist in the page.")
row("E4d3-no-figures-no-data", "2.8-data", "course/modules/E/E4/project.html", "PASS",
    f"grep for img, svg, canvas, iframe, figure, data-file: 0 hits ({CMD}numbers_r9.txt). No dataset cited.")
row("E4d3-spec-stop-rule-and-constraints", "2.6-spec", "course/modules/E/E4/project.html:318 (Constraints); grader/test_project.py (no test of the stop rule); ledgers/E4/alternatives/alt_4.py:82-93", "FAIL",
    "The 6e-49 claim in Constraints is correct (probe_scope_r9.txt). The stop rule the Constraints state ('stops when the bracket is narrower than 1e-12 times its upper end, or after 200 halvings'; 'the bisection on lambda') is not enforced: alt_4 (secant steps with a relative step stop, not the bracket rule) passes 50/50 seeds (alternatives log); mutant_v9_02 (stop rule on the lower end) survives seeds 0-9; equivalent/mutant_r6_09 (never stops early) survives. Their outputs differ from the reference by at most about 2.3e-13 and are not observable at the grader's tolerances.",
    "Either (a) reword Constraints so the stop rule is an accuracy requirement ('the reported lambda* lies within 1e-12 relative of the root'), which the grader already tests, and say that the method is free; or (b) keep the method and add a test that observes the bracket rule, which no output-level test can do. Architect decision (ruling 9 of plans/E4-build-plan.md).")
row("E4d3-atlas-studios-na", "2.6-atlas", "atlas/, studios", "PASS",
    "No atlas key on E4 (check_projects skips the contract check); no studio file in this slice (E4d-cmd-check-projects PASS).")
row("E4d-mutants-existing", "2.6-mutation", "ledgers/E4/mutants/ (68 files, pre-round-9 names)", "PASS",
    f"`tools/mutate_graders.py --unit E4 --seeds 0-9` -> 68 of 68 pre-existing mutants KILLED (rounds 1-8 files; {CMD}mutate_graders_seeds0-9_r9.txt, first run before the round-9 additions).")
row("E4d-mutants-new", "2.6-mutation", "ledgers/E4/mutants/mutant_r7_02_*.py, mutant_r7_03_*.py", "PASS",
    "Both KILLED in the round-9 run (r7_02 by test_noise_volume_far_above_one_is_accepted; r7_03 by test_info_cost_above_one_is_accepted).")
row("E4d2-mutants-r2", "2.6-mutation", "ledgers/E4/mutants/mutant_r2_*.py", "PASS", "All r2 mutants KILLED in the round-9 mutation run (" + CMD + "mutate_graders_seeds0-9_r9_final.txt).")
row("E4d3-mutants-r3", "2.6-mutation", "ledgers/E4/mutants/mutant_r3_*.py", "PASS", "All r3 mutants KILLED in the round-9 mutation run.")
row("E4d3-mutant-tolerance-survives", "2.6-mutation", "ledgers/E4/mutants/mutant_r3_tolerance_1e-9.py", "PASS",
    "KILLED: test_fraction_is_the_oracle_root[first] (seed 0) in the round-9 run.")
row("E4d-mutants-total", "2.6-mutation", "ledgers/E4/mutants/ (74 files)", "FAIL",
    f"`tools/mutate_graders.py --unit E4 --seeds 0-9` -> 'mutate_graders E4: FAIL (72/74 killed)', exit 1 ({CMD}mutate_graders_seeds0-9_r9_final.txt). Survivors: mutant_v9_02_stop_rule_relative_to_lower_end.py, mutant_v9_06_gap_at_zero_from_tiny_fraction.py (rows E4d9-mutant-v9-02, E4d9-mutant-v9-06).",
    "Kill mutant_v9_06 with a gap-at-0 test at 1e-14 against the oracle (see E4d9-mutant-v9-06); mutant_v9_02 is an architect item (E4d3-spec-stop-rule-and-constraints).")
row("E4d-equivalent", "2.6-mutation", "ledgers/E4/equivalent/literal_price_sign.py; mutant_r7_01_reports_bracket_lower_end.py; README.md", "PASS",
    f"literal_price_sign: bitwise identical to the reference on 59 of 59 points (`bitwise_equiv_r9.py`, {CMD}bitwise_literal_price_sign.txt). Proof: b_u enters the solver only as b_u*b_u (informed_term var_gap), and (-x)*(-x) == x*x exactly in IEEE arithmetic, so no output can differ. mutant_r7_01 (reports the lower end of the final bracket) differs bitwise on 59/59 points by at most the final bracket width, and the page allows any point of the final bracket ('The reported lambda* lies in the final bracket', project.html:318); passes 50/50 seeds ({CMD}equiv_r7_01_seeds0-49.txt).")
row("E4d-alternatives", "2.6-alternatives", "ledgers/E4/alternatives/alt_1.py .. alt_5.py", "PASS",
    f"Each run as solver.py under the suite, seeds 0-49: alt_1 50/50, alt_2 50/50, alt_3 50/50, alt_4 50/50, alt_5 50/50 ({CMD}alternatives_builder_seeds0-49.txt).")
row("E4d-starter", "2.6-autograder", "course/modules/E/E4/grader/starter.py", "PASS",
    f"starter.py (raises NotImplementedError) passes 0/50 seeds; the one passing test is the import check ({CMD}starter_seeds0-49.txt).")
row("E4d4-alt4-wrong-on-small-noise", "2.6-alternatives", "ledgers/E4/alternatives/alt_4.py", "PASS",
    f"alt_4 passes 50/50 seeds (including the tiny-root tests) ({CMD}alternatives_builder_seeds0-49.txt). Its stop rule is a secant step size, not the page's bracket rule; that is recorded under E4d3-spec-stop-rule-and-constraints.")
row("E4d4-alt1-docstring", "2.6-alternatives", "ledgers/E4/alternatives/alt_1.py:1-3", "PASS",
    "Docstring 'bisection with the page's stop rule (relative bracket width 1e-12, or 200 halvings)' matches the loop 'while hi - lo > 1e-12 * hi and halvings < 200'.")
row("E4d4-equivalent-price-slope", "2.6-mutation", "ledgers/E4/scripts/E4-d-r4/check_equivalence_r4.py", "PASS",
    "Carried from round 8 (ledgers/E4/scripts/E4-d-r4/check_equivalence_r4.py byte-identical since 0dee921a; the file is present at the pin, and the price-slope equivalence it argues is the one recorded in literal_price_sign.py, now bitwise-checked in E4d-equivalent).")
row("E4d4-calibration-blind", "2.6-rubric-calibration", "course/modules/E/E4/project.html:533-597 (Exemplar A)", "UNVERIFIABLE",
    "Same as E4d-exemplar-A-calibration: not scored blind.",
    "Same as E4d-exemplar-A-calibration.")
row("E4d4-proposed-test-validated", "2.6-autograder", "course/modules/E/E4/grader/test_project.py (small-noise tests)", "PASS",
    "The small-noise tests exist (test_small_noise_root_is_relatively_accurate, test_tiny_noise_root_is_relatively_accurate with 1e-30, 1e-40 added in the delta); the reference passes all (42/42, seeds 0, 7, 49).")
row("E4d4-mutants-killed-r4", "2.6-mutation", "ledgers/E4/mutants/mutant_r4*.py", "PASS", "All r4 and r4f mutants KILLED in the round-9 run.")
row("E4d4-exemplar-B-results-numbers", "2.2-numbers", "course/modules/E/E4/project.html:629-641", "PASS", "Same check as E4d-num-exemplar-table: values equal the Lab 3 printed values.")
row("E4d5-mutant-bracket-floor", "2.6-mutation", "ledgers/E4/mutants/mutant_r5_bracket_floor_1e-12.py", "PASS", "KILLED in the round-9 run (test_tiny_noise_root_is_relatively_accurate[1e-12], seed 0).")
row("E4d5-mutant-sixty-halvings", "2.6-mutation", "ledgers/E4/mutants/mutant_r5_sixty_halvings_no_tolerance.py", "PASS", "KILLED in the round-9 run.")
row("E4d5-mutant-uninformed-precision", "2.6-mutation", "ledgers/E4/mutants/mutant_r5_uninformed_posterior_precision_informed.py", "PASS", "KILLED in the round-9 run (test_indifference_holds...).")
row("E4d5-calibration-B-blind", "2.6-rubric-calibration", "course/modules/E/E4/project.html:598-661 (Exemplar B)", "UNVERIFIABLE",
    "Same as E4d-exemplar-B-calibration: not scored blind.", "Same as E4d-exemplar-B-calibration.")
row("E4d6-mutant-06", "2.6-mutation", "ledgers/E4/mutants/mutant_r6_06_cost_scales_whole_gap.py", "PASS", "KILLED in the round-9 run (test_unit_fraction_is_reported_with_a_positive_cost).")
row("E4d6-mutant-07", "2.6-mutation", "ledgers/E4/mutants/mutant_r6_07_unit_informativeness_discounted_by_cost.py", "PASS", "KILLED in the round-9 run (test_unit_fraction_is_reported_with_a_positive_cost).")
row("E4d6-mutants-new-killed", "2.6-mutation", "ledgers/E4/mutants/mutant_r6_0*.py", "PASS", "All r6 mutants 01-07 KILLED in the round-9 run.")
row("E4d6-spec-variants-08-09", "2.6-mutation", "ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py; mutant_r6_09_always_200_halvings.py; README.md", "FAIL",
    f"r6_08 (reports the lower end of the final bracket): PASS by the page's 'lies in the final bracket' (project.html:318); passes 50/50 seeds. r6_09 (never stops early; 200 halvings always): passes 50/50 seeds and differs from the reference by up to 2.3e-13 on 62 of 64 points (measure_equiv_r9.txt), but it violates the stated stop rule ('stops when the bracket is narrower than 1e-12 times its upper end, or after 200 halvings', project.html:318), and no output test can see the step count. Same class as E4d3-spec-stop-rule-and-constraints.",
    "Architect decision with E4d3-spec-stop-rule-and-constraints: reword the stop rule as an accuracy requirement, or accept r6_09 as an output-equivalent implementation within tolerance by ruling.")
row("E4d6-stop-rule-measured", "2.6-autograder", "grader/reference.py:22-23, :138; ledgers/E4/alternatives/alt_5.py", "PASS",
    "reference.py implements the page's stop rule: 'while high - low > BISECTION_TOLERANCE * high and steps < MAX_BISECTION_STEPS'. alt_5 implements the same test (hi - lo <= 1e-12*hi break, 200 steps).")
row("E4d6-alt-extra-damped", "2.6-alternatives", "ledgers/E4/scripts/E4-d-r6/candidates/damped_fixed_point_log_r6.py", "PASS",
    f"Run as solver.py over seeds 0-49: 50/50 pass ({CMD}alt_extra_damped_r6_seeds0-49.txt).")
row("E4d6-rung1-why", "2.9-prose", "course/modules/E/E4/project.html:171 (Lab 1 interpretation)", "PASS",
    f"Each of the six steps is given a reason. The 2^-53 claim re-checked by replaying the Lab 1 loop: width is 2^-53 first at halving 53 and stays there through halving 60 ({CMD}lab1_width_check_r9.txt).")
row("E4d7-midpoint-untested", "2.6-autograder", "course/modules/E/E4/project.html:318; ledgers/E4/equivalent/mutant_r7_01_reports_bracket_lower_end.py", "PASS",
    "The page now says 'the reported lambda* lies in the final bracket' (project.html:318), which the lower-end variant satisfies (E4d-equivalent).")
row("E4d7-cost-above-one-rejected", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:242-253; project.html:326", "PASS",
    "test_info_cost_above_one_is_accepted: run(0.6, 2.0) -> fraction 0, gap matches oracle; passes on the reference; mutant_r7_03 KILLED.")
row("E4d7-noise-above-one-rejected", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:357-370", "PASS",
    "mutant_r7_02 KILLED by test_noise_volume_far_above_one_is_accepted / test_unit_fraction... (round-9 run).")
row("E4d7-alt5-docstring", "2.6-alternatives", "ledgers/E4/alternatives/alt_5.py:1-2", "PASS",
    "Docstring 'with the same bracket [0, 1]' matches 'lo, hi = 0.0, 1.0'; alt_5 50/50.")
row("E4d7-lab1-bracket-width", "2.5-labs", "course/modules/E/E4/project.html:171", "PASS",
    "Lab 1 prints 1.110e-16 after 60 halvings (run_labs / twin output); equals 2^-53 (lab1_width_check_r9.txt).")
row("E4d7-lab2-blank", "2.5-labs", "course/modules/E/E4/project.html:244", "PASS",
    "The only changed line of Lab 2 against its twin is the blank (lab_twin_check_r9.txt).")
row("E4d7-instance-bound", "2.8-data", "course/modules/E/E4/grader/test_project.py; grader/instance.py:1-21; project.html:314", "PASS",
    "tau_bar(0.150) 0.097623, tau_bar(0.120) 0.237567, 1/(1+4*0.75^2) 0.307692 (numbers_r9.txt); seeds 0-49 draws in [0.503, 0.741] x [0.120, 0.149] (numbers_r9.txt).")
row("E4d7-lab3-closed-form-sentence", "2.5-labs", "course/modules/E/E4/project.html:376 (Lab 3 hypothesis)", "PASS",
    "Largest bisection-vs-closed-form difference printed 2.1e-13 (twin output), and re-derived 2.1e-13 (numbers_r9.txt); 'to within 1e-12' holds.")
row("E4d7-test-count", "2.6-autograder", "course/modules/E/E4/project.html:320 (Grading mode); grader/test_project.py", "PASS",
    "Page says 42 checks; collect-only count is 42 (collect.txt).")
row("E4d8-no-upper-bound", "2.4-scope", "course/modules/E/E4/project.html:326; grader/reference.py:122-151; grader/test_project.py:261-279", "PASS",
    "Round-8 FAIL resolved by the page's new range qualifier; see E4d-prose-scope-words for the probe. The new tests test_noise_volume_far_above_one_is_accepted (sd 50, 1000) and test_info_cost_far_above_one_is_accepted (c 10, 50) pass on the reference.")
row("E4d8-cap-100-survives", "2.6-mutation", "ledgers/E4/mutants/mutant_r8_01_cap_100_halvings.py; project.html:318", "PASS",
    "KILLED in the round-9 run (test_tiny_noise_root_is_relatively_accurate[...]).")
row("E4d8-noise-cap-10-survives", "2.6-mutation", "ledgers/E4/mutants/mutant_r8_02_noise_above_ten_rejected.py; project.html:326", "PASS",
    "KILLED in the round-9 run (test_noise_volume_far_above_one_is_accepted).")
row("E4d8-cost-cap-5-survives", "2.6-mutation", "ledgers/E4/mutants/mutant_r8_03_cost_above_five_rejected.py; project.html:326", "PASS",
    "KILLED in the round-9 run (test_info_cost_far_above_one_is_accepted).")
row("E4d8-mutants-r8-killed", "2.6-mutation", "ledgers/E4/mutants/mutant_r8_04_integer_zero_fraction.py; mutant_r8_05_informativeness_at_unit_precision.py", "PASS",
    "Both KILLED in the round-9 run.")
row("E4d8-alternatives-r8", "2.6-alternatives", "ledgers/E4/alternatives/alt_r8_a.py, alt_r8_b.py (cited by round 8)", "UNVERIFIABLE",
    "Cited files do not exist at the pin c93dd52: ledgers/E4/alternatives/ holds alt_1..alt_5 only. Not re-verified; not carried.",
    "Commit alt_r8_a.py and alt_r8_b.py to ledgers/E4/alternatives/ (or drop the citation); this round's alt_v9_1..3 are the replacement correct alternatives.")
row("E4d8-tiny-root-reference", "2.6-autograder", "course/modules/E/E4/grader/reference.py; ledgers/E4/scripts/E4-d-r9/numbers_r9.py", "PASS",
    "solve_model(1e-30, 0.13): informed_fraction 9.656254101544045e-31 vs closed form 9.656254101546876e-31, relative difference 2.93e-13 (numbers_r9.txt; the round-8 figure 2.9e-13 reproduces).")
row("E4d8-lab3-twin-page", "2.5-labs", "course/modules/E/E4/project.html:377-503; tests/labs/E4/lab-E4-project-3.py", "PASS",
    "Page code equals the twin (114 lines, 0 differing); twin runs `-I -W error` exit 0; output equals the expected block (lab_twin_check_r9.txt).")

# ---- new round-9 rows
row("E4d9-mutant-v9-02", "2.6-mutation", "ledgers/E4/mutants/mutant_v9_02_stop_rule_relative_to_lower_end.py", "FAIL",
    "Student error: bisection stop rule measured against the lower end of the bracket. SURVIVED seeds 0-9 (final mutation run). Outputs are bitwise identical to the reference on seeds 0-49 and differ only when the bracket width crosses the threshold in one step (measure_v9_r9.txt: max difference 0). No test observes it. The stated stop rule (project.html:318) is violated.",
    "Architect item with E4d3-spec-stop-rule-and-constraints. If the stop rule stays a stated behaviour, the page must state an observable quantity (the accuracy claim) for the grader to test.")
row("E4d9-mutant-v9-06", "2.6-mutation", "ledgers/E4/mutants/mutant_v9_06_gap_at_zero_from_tiny_fraction.py", "FAIL",
    f"Student error: the gap at fraction 0 taken as the gap at fraction 1e-12. SURVIVED seeds 0-9. Measured: |G(1e-12) - G(0)| up to 3.9e-14 on seeds 0-49 and 1.6e-12 on a wider grid ({CMD}measure_oracle_gap0_r9.txt); the reference agrees with the oracle's gap at 0 to 1.1e-16 on seeds 0-49. The page requires 'the limit of Proposition 3' (project.html:318).",
    "Add to test_project.py a test that the reported gap at fraction 0 equals oracle_gap(0, sd, cost) to 1e-14 (the reference's error is 1.1e-16 on seeds 0-49, so it passes; this mutant differs by up to 3.9e-14). Builder must re-run run_graders and mutate_graders before accepting.")
row("E4d9-equivalent-r6-08-09-docstrings", "2.6-mutation", "ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py; mutant_r6_09_always_200_halvings.py (docstring first line)", "FAIL",
    "The first docstring line of both files reads 'Reference solution for the E4 project ...', copied from reference.py, so it does not describe the one edit each file makes (lam = low; no relative stop). README.md documents both edits correctly.",
    "Replace the first docstring line of each file with its one-line description of the edit (for example 'Variant: reports the lower end of the final bracket.'). Not editable by the verifier (outside mutants/).")
row("E4d9-mutants-v9-killed", "2.6-mutation", "ledgers/E4/mutants/mutant_v9_01, _03, _05, _07", "PASS",
    f"KILLED in the round-9 run: v9_01 by test_gap_is_the_oracle_gap_at_the_reported_fraction[first] (seed 0); v9_03 by test_fraction_is_the_oracle_root[first] (seed 0); v9_05 by test_unit_fraction_is_reported_at_zero_cost (seed 0); v9_07 by test_tiny_noise_root_is_relatively_accurate[1e-11] (seed 0) ({CMD}mutate_graders_seeds0-9_r9_final.txt).")
row("E4d9-mutant-docstrings", "2.6-mutation", "ledgers/E4/mutants/*.py (74 files) against grader/reference.py", "PASS",
    f"`{CMD}mutant_summary_r9.txt`: each mutant's first docstring line matches its code edit (changed-line counts 2 to 23). The equivalent-folder docstring defect is recorded separately (E4d9-equivalent-r6-08-09-docstrings).")
row("E4d9-alternatives-v9", "2.6-alternatives", "ledgers/E4/alternatives/alt_v9_1_interior_gap_zero.py, alt_v9_2_log_space.py, alt_v9_3_grid_then_bisect.py", "PASS",
    f"Written by this verifier as correct alternatives; each passes the suite on seeds 0-49, 50/50 ({CMD}alternatives_v9_seeds0-49.txt). alt_v9_1 (interior gap reported as exact 0.0) is a correct answer, since Prop 3 gives G(lambda*) = 0; the reference's own interior gap is at most 4.4e-14 (measure_v9_r9.txt). It was a mutant in the first run and is moved to alternatives. alt_v9_2 (log-space Gaussian terms) and alt_v9_3 (grid scan then bisection) are the cross-checks for over-constraint.")

# ---- mutants list from the final mutation run
mutants = []
for line in (root / L / "mutate_graders_seeds0-9_r9_final.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    killed_by = None if killer.strip() == "None" else killer.strip()
    mutants.append({"name": name, "description": desc, "killed_by": killed_by, "status": status})

counts = {}
for r in R:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
verdict = "PASS" if counts.get("PASS", 0) == len(R) else "FAIL"
killed = sum(1 for m in mutants if m["killed_by"])
fragment = {
    "unit": "E4",
    "slice": "d",
    "round": 9,
    "verifier": "Haiku independent verifier, E4 slice d, round 9 (did not build E4; fresh checkout)",
    "pin": PIN,
    "base": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3 (round-8 pin). Delta in the slice: project.html (12 lines: A1, A3, the Inputs, Required outputs, Constraints, Grading mode and the exception table), grader/test_project.py (+31 lines: four new tests and a docstring), ledgers/E4/alternatives/alt_1.py, alt_2.py, ledgers/E4/equivalent/README.md and two variants, mutant files r8_01..r8_05. All hunks read; every previous non-PASS row re-verified.",
    "checkout": str(root),
    "scratch": "/tmp/e4r9ref, /tmp/e4r9ref2 (reference as solver.py, scratch copies of instance.py and test_project.py); per-solver runs use a tempdir removed on exit (run_solver_seeds.py)",
    "verified_at": "2026-11-05T04:24:16+00:00",
    "verdict": verdict,
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Full page read (project.html lines 1-702) and full grader read (test_project.py, reference.py, instance.py, starter.py). Lab twins compared line by line with the page code (lab_twin_check_r9.py).",
        "Mutation gate: 74 mutants in ledgers/E4/mutants, 72 killed; survivors v9_02 and v9_06 (rows E4d9-mutant-v9-02, -06). The 68 pre-existing mutants are all killed.",
        "Moved from mutants to alternatives: mutant_v9_04 (interior gap reported as 0.0) is a correct answer at a root and is now alt_v9_1_interior_gap_zero.py.",
        "Not checked: a blind scoring of Exemplar A and Exemplar B (see the four UNVERIFIABLE calibration rows); the Pyodide interpreter itself (page_smoke runs the in-browser suite through the repo tool); a live verify_refs run (references unchanged in the delta).",
        "Questions the spec leaves open for a student (none blocks a grader): integer inputs to solve_model; the value at lambda* = 1 is explained (hypothetical uninformed agent) so not open.",
    ],
    "summary": {
        "rows": len(R),
        "pass": counts.get("PASS", 0),
        "fail": counts.get("FAIL", 0),
        "unverifiable": counts.get("UNVERIFIABLE", 0),
        "mutants": len(mutants),
        "mutants_killed": killed,
    },
}
out = root / "ledgers/E4/E4-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(R), counts, "mutants", len(mutants), "killed", killed, "verdict", verdict)
