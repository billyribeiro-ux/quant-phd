"""Write the round-5 ledger fragment ledgers/E4/E4-d.json from the logs of this round (verifier E4 slice d, round 5).

Usage: python -I ledgers/E4/scripts/E4-d-r5/write_fragment_r5.py <checkout-root>
Mutant rows are parsed from logs/mutate_graders_r5_seeds0-9.txt, so the counts equal the tool's output.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

root = Path(sys.argv[1]).resolve()
S = "ledgers/E4/scripts/E4-d-r5"
L = f"{S}/logs"

mutate_lines = (root / L / "mutate_graders_r5_seeds0-9.txt").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mutate_lines:
    m = re.match(r"(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    mutants.append(
        {
            "id": name[:-3],
            "description": desc,
            "killed_by": None if killer.strip() == "None" else killer.strip(),
        }
    )
assert len(mutants) == len(list((root / "ledgers/E4/mutants").glob("*.py"))), "mutant count mismatch"

R = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)


# ---- commands
row("E4d-cmd-check-projects", "2.6-structure", "course/modules/E/E4/project.html; grader/",
    "PASS", f"tools/check_projects.py --unit E4 -> 'check_projects E4: PASS', exit 0 ({L}/check_projects.txt)")
row("E4d-cmd-check-pages", "2.9-structure", "course/modules/E/E4/project.html",
    "PASS", f"tools/check_pages.py --unit E4 -> 'check_pages E4: PASS', exit 0 ({L}/check_pages.txt); visible-prose "
    "banned-phrase scan re-run independently (15 BANNED patterns, 0 hits)")
row("E4d-cmd-check-dag", "2.9-DAG", "course/modules/E/E4/project.html",
    "PASS", f"tools/check_dag.py --unit E4 -> 'check_dag E4: PASS', exit 0 ({L}/check_dag.txt)")
row("E4d-cmd-run-labs", "2.5-labs", "tests/labs/E4/lab-E4-project-1.py, -2.py, -3.py",
    "PASS", f"tools/run_labs.py --unit E4 -> 'run_labs E4: PASS (12/12)', exit 0 ({L}/run_labs.txt)")
row("E4d-cmd-run-graders", "2.6-autograder", "course/modules/E/E4/grader/reference.py",
    "PASS", f"tools/run_graders.py --unit E4 --seeds 0-49 -> 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)',"
    f" exit 0 ({L}/run_graders.txt)")
row("E4d-cmd-page-smoke-project", "2.9-smoke", "course/modules/E/E4/project.html",
    "PASS", f"tools/page_smoke.py --unit E4 --pages project -> 'page_smoke E4: PASS' (in-browser grader: 32 tests pass) ({L}/page_smoke_project_r5.txt)")
row("E4d-cmd-ruff", "conventions", "repository",
    "PASS", f"ruff check . -> 'All checks passed!'; ruff format --check . -> '553 files already formatted' ({L}/ruff_check_r5.txt, {L}/ruff_format_r5.txt)")
row("E4d-cmd-mypy-workspace", "conventions", "tests/labs/E4 and course/modules/E/E4/grader",
    "PASS", f".venv/bin/mypy --no-incremental tests/labs/E4 course/modules/E/E4/grader -> 'Success: no issues found in 16 source files' ({L}/mypy_r5.txt); the mutants also pass mypy ({L}/mypy_r5_with_mutants.txt is the pre-fix run with one error, since corrected)")
row("E4d-cmd-mypy-plan-command", "conventions", "tests/labs/E4; grader",
    "PASS", f"same mypy run as E4d-cmd-mypy-workspace ({L}/mypy_r5.txt)")
row("E4d-cmd-pytest-relevant", "conventions", "tests/test_memo_exemplars.py, test_page_checks.py, test_labs.py, test_run_labs.py",
    "PASS", f"pytest -q on the four modules -> all dots, exit 0 ({L}/pytest_relevant_r5.txt)")
row("E4d-cmd-verify-refs", "2.1-citations", "references/references.json (E4 keys)",
    "PASS", f"tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' ({L}/verify_refs_offline_all_r5.txt); "
    f"tools/verify_refs.py --unit E4 (live Crossref) -> 'live re-verification of E4: 3 of 560 entries, 0 problems' ({L}/verify_refs_E4_live_r5.txt)")
row("E4d-cmd-collect", "2.6-autograder", "course/modules/E/E4/grader/test_project.py",
    "PASS", f"pytest --collect-only with reference.py as solver.py -> '32 tests collected' ({L}/collect_r5.txt); project.html:316-321 now says 32 checks")

# ---- labs and numbers
row("E4d-lab-project-1", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-1; tests/labs/E4/lab-E4-project-1.py",
    "PASS", f"run_labs E4 PASS ({L}/run_labs.txt); the expected block (project.html Lab 1) equals the twin output; the lab text is unchanged since the round-4 pin")
row("E4d-lab-project-2", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-2; tests/labs/E4/lab-E4-project-2.py",
    "PASS", f"run_labs E4 PASS ({L}/run_labs.txt); recomputed this round with reference.py at (0.70, 0.14): gap at 0 = +0.03743519 (prints +0.037435), gap at 1 = -0.07138567 (prints -0.071386), root 0.5705226300 (prints 0.57052263), informativeness 0.12466375 (log {L}/lab2_check_r5.txt)")
row("E4d-lab-project-3", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-3; tests/labs/E4/lab-E4-project-3.py",
    "PASS", f"run_labs E4 PASS ({L}/run_labs.txt); the nine expected rows (project.html:488-496) equal the twin's output; "
    "the 22 by 22 box count 484 of 484 is the twin's printed line; the exemplar grid (project.html:629-637) equals those rows")
row("E4d-num-lab-hypotheses", "2.2-numbers", "project.html:57, :176, :375 (Lab hypothesis paragraphs)",
    "PASS", "Lab 1 values equal its expected block (run_labs); Lab 2 values equal its expected block; Lab 3 fractions 0.5582/0.6978/0.8373 at cost 0.120 "
    "equal 2 sigma sqrt(tbar/(1-tbar)) with tbar = 2e^(-0.48)-1 = 0.2375668 (recomputed this round); informativeness 1-e^(4c)/2 = 0.1920, 0.1420, 0.0889 for c = 0.120, 0.135, 0.150 (recomputed this round)")
row("E4d-num-exemplar-table", "2.2-numbers", "project.html Results passage (Exemplar B) and table",
    "PASS", "every table row equals the Lab 3 printed row (fraction to 4 decimals, informativeness, gap); ratios 0.6978/0.5582 = 1.25009 (displays 1.2501) and 0.8373/0.5582 = 1.50000 (displays 1.5000), exact 1.25 and 1.5 recomputed; the largest printed gap 3.55e-14 is below 4e-14")
row("E4d-num-box-bounds", "2.2-numbers", "project.html Inputs paragraph; grader/instance.py:14-17",
    "PASS", "tau_bar(0.150) = 2e^-0.6 - 1 = 0.09762327 and tau_bar(0.120) = 2e^-0.48 - 1 = 0.23756678; 1/(1+4*0.75^2) = 0.30769231 (python math, this round); the page's bounds 0.097623, 0.237567, 0.30769 are correct roundings")
row("E4d-prose-lede-directional", "2.9-prose", "project.html:37 (lede)",
    "PASS", "with the fraction fixed, tau_y = lam^2 tau_e^2/(lam^2 tau_e + a^2 sd^2) falls in sd, so informativeness falls (Proposition 2 and Lab 3); on the interior the fraction is proportional to sd (Lab 3 printed table: 0.5582 -> 0.6978 -> 0.8373 at cost 0.120, ratio 1.25 and 1.50 of the noise volumes, {L}/run_labs.txt; re-derived from Proposition 4) and the informativeness does not depend on sd (Proposition 5)")

# ---- maths
row("E4d-math-lemmas", "2.4-mathematics", "project.html:266-273 (Lemmas 1-3)",
    "FAIL", f"Lemma 1 is graded T, and its proof (project.html:268) needs that v - p is conditionally normal given F so that E[exp(-a x(v-p)) | F] = exp(-a x(m-p) + a^2 x^2 V/2). The statement lists only 'V = Var(v|F) > 0 is a constant', and conditional normality appears only as the example 'as it is when v is conditionally normal'. Counterexample with V constant and v-p = d +/- sqrt(V) (equiprobable, d = 1, V = 1, a = 2): the lemma's demand is 0.5 and its value -exp(-d^2/(2V)) = -0.606531; the actual utility at 0.5 is -0.567668, and the utility has no maximiser on [-20, 20] (sup -0.5, reached only as x grows) ({S}/lemma1_counterexample_r5.py; {L}/lemma1_counterexample_r5.txt). Lemma 2 and Lemma 3 re-derived and correct (Lemma 3 needs only p F-measurable and V constant).",
    fix="project.html:266: add 'and v is conditionally normal given F' to the hypotheses of Lemma 1 (before 'Then the optimal demand is'), and change 'as it is when v is conditionally normal' to a plain statement that the normal case is the one used in Proposition 1, 3 (joint normality of (v, s, u) under A1, A2, A4)")
row("E4d-math-prop1", "2.4-mathematics", "project.html:276-278 (Proposition 1, steps 1-4)",
    "PASS", "steps (1)-(4) re-derived by hand this round: x_I = (tau_e s - (tau_v+tau_e)p)/a; x_U = (tau_y y - (tau_v+tau_y)p)/a; clearing gives b_s = (lam tau_e+(1-lam)tau_y)/D and kappa = -a/(lam tau_e); tau_y from the variance of eps + kappa u. Independent check this round: the reference price coefficients (b_s, b_u) equal the test suite's fixed-point clearing oracle (oracle_price, test_project.py:117-130) to 1.0e-14 at 15 (lam, sd) pairs (lam in {0.1, 0.3, 0.57, 0.9, 1.0}, sd in {0.5, 0.7, 1.0}); script inline in this round's log {L}/oracle_price_check_r5.txt")
row("E4d-math-prop2", "2.4-mathematics", "project.html:284-285 (Proposition 2)",
    "PASS", "Cov(v,p) = b_s/tau_v, Var(p) = b_s^2(1/tau_v+1/tau_y), Corr^2 = tau_y/(tau_v+tau_y) re-derived; lambda = 0 case: clearing gives x_U = -tau_v p/a = u, so p = -a u/tau_v, independent of v (re-derived)")
row("E4d-math-prop3", "2.4-mathematics", "project.html:287-291 (Proposition 3)",
    "PASS", "sign G = sign(V_U - e^(2ac) V_I) = sign(tau_bar - tau_y) via the factor (tau_v+tau_y)(tau_v+tau_e)e^(-2ac) re-derived; G(0+) re-derived from b_s/lam -> tau_e/tau_v and b_u -> -a/tau_v; Omega = V_I + S_I = V_U + S_U holds by Lemma 3 for the informed (F = (s,p)) and uninformed (F = p) sets")
row("E4d-math-prop4", "2.4-mathematics", "project.html:294-296 (Proposition 4)",
    "PASS", f"lam^2 (tau_e^2 - tau_bar tau_e) = tau_bar a^2 sd^2 re-derived; reference bisection vs closed form: max relative difference 1.26e-11 over the probe grid sd in [1e-12, 5], c in [0, 0.5] ({S}/probe_alts_r5.py; {L}/probe_alts_r5.txt)")
row("E4d-math-prop5", "2.4-mathematics", "project.html:299-302 (Proposition 5 and the paragraph at :302)",
    "PASS", "lam* = a sd k(tau_bar), k(t) = sqrt(t/(tau_e(tau_e-t))) strictly increasing on (0, tau_e); tau_bar strictly decreasing in c; d lam*/d sd = lam*/sd; grid ratio 1.25 and informativeness constant in sd re-derived (Lab 3 printed table)")
row("E4d-math-assumptions", "2.4-mathematics", "project.html:257-261 (A1-A5) and :302 paragraph",
    "PASS", "A1-A5 are numbered and each proposition states A1 to A5; the use-lists in Exemplar B are checked in E4d2-exemplar-B-C1-annotation (one omission there); the CARA form is Definition 6.2 of L06 (L06.html:66-67, text read this round)")
row("E4d-notation", "2.4-notation", "project.html math spans; notation/notation.json",
    "PASS", "macros used (\\Corr, \\Cov, \\E, \\Normal, \\Var, \\mathcal, \\operatorname, \\text, \\sigma, \\sim) are all registered in notation.json 'macros' (checked by script this round); no registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) is used on the page; local symbols (Omega, tau_bar, tau_y, V_I, V_U, S_I, F_I, F_U, G, D, kappa) are defined on the page")

# ---- prose and structure
row("E4d-banned-phrases", "2.9-prose", "course/modules/E/E4/project.html",
    "PASS", "check_pages E4 PASS and an independent scan of the visible prose (outside pre/code) against the 15 BANNED patterns of tools/check_pages.py: 0 hits")
row("E4d-process-words", "2.9-prose", "course/modules/E/E4/project.html",
    "PASS", "grep for verif, builder, round, fixture, agent, ruling, architect, pass N, blind: only 'C2 · Solver and verification' (a rubric criterion name) and a code docstring; no process words in learner text")
row("E4d-dag-links", "2.9-DAG", "course/modules/E/E4/project.html",
    "PASS", "every href and fragment resolves (script this round over all hrefs, files and anchors: no problems); data-concept targets noisy-rational-expectations-equilibrium (L06.html), price-informativeness (L07.html), expected-utility (concepts.html) exist; check_dag E4 PASS")
row("E4d-registry-muth", "2.1-citations", "project.html reading list (data-cite muth1961rational)",
    "PASS", "references.json: Muth, 'Rational Expectations and the Theory of Price Movements', Econometrica 29(3) 315, 1961, DOI 10.2307/1909635 (status verified); live verify_refs E4: 0 problems; the page attributes no statement to it")
row("E4d-registry-milgrom", "2.1-citations", "project.html:678, :681",
    "PASS", "references.json: Milgrom & Stokey, 'Information, trade and common knowledge', J. Econ. Theory 26(1) 17-27, 1982, DOI 10.1016/0022-0531(82)90046-1; live verify_refs E4 PASS; the page attributes no statement to it")
row("E4d-cites-only-registry", "2.1-citations", "project.html data-cite (lines 680-681)",
    "PASS", "only muth1961rational and milgrom1982information are cited; both keys exist in references.json")
row("E4d-spec-context-sentences", "2.9-prose", "project.html:311 (Context)",
    "PASS", "Context has four sentences (project.html:311)")
row("E4d-spec-questions", "2.6-spec", "project.html:314-321 (Required outputs, Constraints, Grading mode)",
    "PASS", "questions a competent student would ask: (1) which point of the final bracket is reported (midpoint in Exemplar B, which is not the spec; the spec and the suite (TOL_ROOT 1e-10 absolute) accept either, and both are within 1e-12 relative); (2) what is returned for an input the exception table does not name (the table says any exception or value). No blocking gap.")
row("E4d-spec-ladder", "2.6-spec", "project.html:40-49 (ladder), :51-305, :308, :668-674",
    "PASS", "rung 1 annotated and printed (Lab 1); rung 2 is the instant completion check (Lab 2); rung 3 is the spec; rung 4 is open-ended (stretch)")
row("E4d-prose-scope-words", "2.9-prose", "course/modules/E/E4/project.html",
    "PASS", "scope words at project.html:257, :259, :263, :302, :313, :317, :321, :375, :385 checked: each is definitional, computed (484 grid points, A1 normalization, CARA wealth factor) or restricts a noun phrase; the new lede (:37) and Exemplar B sentences contain no unsupported universal")
row("E4d-prose-simulated-labs", "2.9-prose", "project.html Labs 1-3 (:57, :176, :375) and Inputs (:313)",
    "PASS", "each lab and the Inputs paragraph says SIMULATED; grader/instance.py docstring says SIMULATED")
row("E4d-prose-simulated-exemplars", "2.9-prose", "project.html:530",
    "PASS", "the exemplar intro says 'on a SIMULATED instance' and the grid point of Lab 3")
row("E4d-hours-project", "2.6-hours", "project.html:33, :343-350 (#hours); course/modules/E/E4/index.html:29; curriculum.json (E4 hours 100)",
    "PASS", "hub data-hours-lessons=72 and data-hours-project=28 sum to 100 (curriculum.json: E4 hours 100, script this round); project header 28 hours; hours table 1+1+5+8+5+5+3 = 28")
row("E4d-hours-estimate", "2.6-hours", "project.html #hours table",
    "PASS", "verifier estimate: reading and Labs 1-2 about 2 h, derivation of Propositions 1-4 about 6 h, solver and local suite about 4-6 h, grid and display about 5 h, report about 5-6 h, self-assessment 3 h: about 25-28 h, within 30% of 28")
row("E4d-rubric-observable", "2.6-rubric", "project.html:516-526 (#rubric), C1 level 1 descriptor (:520)",
    "FAIL", "C1 level 1 'Describes the model in words, with no payoff, signal or utility function written down as a formula.' overlaps level 2 'States the payoff, the signal, the noise supply and the preferences, and gives the equilibrium condition in words only.' A report that states all four items in words, with no formulas, satisfies the literal text of both levels, so the level cannot be scored from the report alone. The round-4 wording ('in general terms') was replaced, but the boundary is still not observable.",
    fix="project.html:520: replace the level 1 descriptor with 'Omits at least one of the payoff, the signal, the noise supply or the preferences.' (observable: the four items are checkable), and keep level 2 as 'States the four items in words, and gives the equilibrium condition in words only.'")
row("E4d-exemplar-A-calibration", "2.6-rubric", "project.html:532-595 (exemplar A, data-scores 2,2,1,2,1)",
    "PASS", "descriptor-level scoring of the Exemplar A passages with the rubric table: C1 2 (words, no coefficient), C2 2 (method and bracket, no tolerance), C3 1 (sign with no grid), C4 2 (fixed decimals, no rule), C5 1 (caveat, no named limit): equal to the data-scores. NOT blind: the official verdict paragraph (project.html:530) was read before scoring; see E4d4-calibration-blind")
row("E4d-exemplar-B-calibration", "2.6-rubric", "project.html:597-659 (exemplar B, data-scores 4,4,4,4,4)",
    "PASS", "blind: the Exemplar B passage was extracted with script ({S}/exemplar_passages_r5.py exemplar-b, no annotation, no verdict) and scored from the rubric table before its annotation was read. Scores: C1 3 (lists A1-A5 with numbers, but the A2 list omits Proposition 2; level 4 not met), C2 4, C3 4, C4 4, C5 4. Each within one level of the annotated 4, so calibration passes; the C1 content defect is E4d2-exemplar-B-C1-annotation")
row("E4d-exemplar-annotations-hidden", "2.6-rubric", "course/assets/js/rubric.js:147-150; project.html data-reveal",
    "PASS", "rubric.js and labs.js are byte-identical to the round-4 pin (git diff 9a02b1a..7376a5e empty for course/assets/js); data-reveal attributes present (project.html:532, :597)")
row("E4d-grader-exceptions", "2.6-autograder", "grader/test_project.py:190-240; grader/reference.py:23-31; project.html:330-331",
    "PASS", "the two named ValueError conditions are tested in both directions (zero, negative, infinite, NaN noise volume; negative and -1e-12 cost; zero and tiny positive accepted); messages equal the table text; the table names only these two")
row("E4d-grader-messages", "2.6-autograder", "grader/test_project.py:48-67 and every expect() message",
    "PASS", "messages name the property with a hint and carry no numeric answer (read every expect() in this round); suite passes 32 of 32 on the reference (run_graders 50/50 seeds)")
row("E4d-grader-oracle", "2.6-autograder", "grader/test_project.py:9-14, 79-170",
    "PASS", "oracle is fixed-point price iteration with a 1001-node trapezoid quadrature and does not import the reference; formulas for regressions, alpha_u and the informativeness re-derived; agrees with the reference on 50 seeds (run_graders 50/50)")
row("E4d-grader-instances", "2.6-autograder", "grader/instance.py; grader/test_project.py:37-39",
    "PASS", f"seeds 0-19 this round: every instance inside the box, every reference fraction strictly interior, 20 distinct (sd, c) pairs and 20 distinct fractions ({L}/sample_instances_r5.txt; script {S}/sample_instances_r5.py)")
row("E4d-grader-instance-docstring", "2.6-autograder", "grader/instance.py:14-17",
    "PASS", "bound 0 < tau_bar < 0.237567 < 0.30769 <= tau_y(1) recomputed (E4d-num-box-bounds); the docstring says the suite does not re-check it, and test_project.py does not")
row("E4d-grader-test-docstring", "2.6-autograder", "grader/test_project.py:9-14, :365, :369-373, :378-386, :421-444",
    "PASS", "test_fraction_falls_with_the_cost asserts the Proposition 5 monotonicity its docstring names; test_fraction_is_proportional asserts the proportionality its docstring names; test_small_noise_root_is_relatively_accurate names the relative stop rule and asserts it")
row("E4d-grader-reference-docstring", "2.6-autograder", "grader/reference.py:3-10, :19-21, :35-90, :102-104",
    "PASS", "the new units sentence (reference.py:9-10) is correct: uninformed expected utility = -F_U in [-1, 0) because 0 < F_U <= 1; informed = -exp(ac) F_I can lie below -1; '200 halvings exceed any relative tolerance' (2^-200 < 1e-60)")
row("E4d-grader-stdlib", "2.6-autograder", "grader/test_project.py:403-412; reference.py; ledgers/E4/alternatives/*.py",
    "PASS", "the test asserts stdlib imports only; reference.py and all five alternatives import only math (checked by ast this round, {L}/stdlib_imports_r5.txt)")
row("E4d-mutants-existing", "2.6-mutation", "ledgers/E4/mutants/mutant_01..mutant_10",
    "PASS", f"tools/mutate_graders.py --unit E4 --seeds 0-9: all ten builder mutants KILLED ({L}/mutate_graders_r5_seeds0-9.txt)")
row("E4d-mutants-new", "2.6-mutation", "ledgers/E4/mutants/mutant_d11..mutant_d18",
    "PASS", f"all eight KILLED in the same run ({L}/mutate_graders_r5_seeds0-9.txt)")
row("E4d2-mutants-r2", "2.6-mutation", "ledgers/E4/mutants/mutant_r2_*.py",
    "PASS", f"all four KILLED in the same run ({L}/mutate_graders_r5_seeds0-9.txt)")
row("E4d3-mutants-r3", "2.6-mutation", "ledgers/E4/mutants/mutant_r3_*.py",
    "PASS", f"all four KILLED in the same run ({L}/mutate_graders_r5_seeds0-9.txt)")
row("E4d3-mutant-tolerance-survives", "2.6-mutation", "grader/test_project.py:44 (TOL_ROOT); ledgers/E4/mutants/mutant_r3_tolerance_1e-9.py",
    "PASS", f"KILLED by test_fraction_is_the_oracle_root[first] (seed 0) in the same run ({L}/mutate_graders_r5_seeds0-9.txt)")
row("E4d-mutants-total", "2.6-mutation", "ledgers/E4/mutants/ (44 mutants)",
    "FAIL", f"42 of 44 KILLED ({L}/mutate_graders_r5_seeds0-9.txt). The two survivors are verifier mutants written this round: mutant_r5_bracket_floor_1e-12 and mutant_r5_sixty_halvings_no_tolerance (rows E4d5-mutant-bracket-floor and E4d5-mutant-sixty-halvings).",
    fix="add the relative tiny-root test to grader/test_project.py: @pytest.mark.parametrize('sd', [1e-11, 1e-12]) with the closed form of Proposition 4 and abs(lam - exact) <= 1e-8 * exact (validated in a scratch copy, {S}/scratch_tiny_root_test_r5.py; {L}/scratch_tiny_root_test_r5.txt: reference and alt_1..alt_4 pass, alt_5 and both survivors fail)")
row("E4d-equivalent", "2.6-mutation", "ledgers/E4/equivalent/literal_price_sign.py; ledgers/E4/equivalent/README.md",
    "PASS", "round-4 equivalence argument re-read: b_u enters the reference only as b_u*b_u (reference.py informed_term); the file is byte-identical to the round-4 pin; not in mutants/")
row("E4d-alternatives", "2.6-alternatives", "ledgers/E4/alternatives/alt_1..alt_5.py",
    "FAIL", f"all five pass seeds 0-49 on the current grader ({S}/run_candidates_r5.py; {L}/alternatives_seeds0-49.txt). alt_1..alt_4 are correct on the small-noise probe (worst relative error 4.3e-13 on interior roots, {L}/probe_alts_r5.txt). alt_5 is wrong on a valid input: its bisection starts at lo = 1e-12 (alt_5.py solve_model), so for noise_sd = 1e-12, info_cost = 0.15 it returns 1.0000000000e-12 where the boundary rule and Proposition 4 give 6.578285721e-13 (relative error 0.52; {L}/probe_alts_r5.txt). The valid domain of noise_sd is every positive finite value (project.html:318-319 and the exception table at :330-331), and the page's Constraints say the bisection brackets the root in [0,1] (project.html:317).",
    fix="ledgers/E4/alternatives/alt_5.py solve_model: start the bisection at lo = 0.0 (the gap at 0 is the limit of Proposition 3, which the boundary check already evaluates), or move alt_5 to ledgers/E4/mutants/ as a wrong solution; then the tiny-root test in E4d-mutants-total kills it")
row("E4d-starter", "2.6-autograder", "grader/starter.py",
    "PASS", "starter.py raises NotImplementedError; run_graders confirms the starter fails the suite (run_graders E4 PASS includes the 'starter passes the suite' check)")
row("E4d-browser-local-parity", "2.6-autograder", "grader/test_project.py; page_smoke",
    "PASS", f"page_smoke project PASS and its in-browser grader line 'All 32 tests pass' ({L}/page_smoke_project_r5.txt); local pytest with the browser flags on the reference: run_graders 50/50")
row("E4d-runtime", "2.6-autograder", "grader/test_project.py",
    "PASS", "run_graders slowest local suite 0.2 s (limit 60 s); page_smoke timing PASS")
row("E4d2-exemplar-B-C1-annotation", "2.6-rubric", "project.html:603 (Model passage) and :607 (annotation)",
    "FAIL", "Exemplar B lists 'Assumption 2 in Propositions 1, 3 and 4' and its annotation (:607) says it 'names the results that use it'. Proposition 2 also uses A2: its lambda = 0 case uses the market-clearing condition of A2 ('clearing gives x_U = -tau_v p/a = u', project.html:285), and its Var(y) = 1/tau_v + 1/tau_y step uses the independence of u and v from A2. The round-4 items for A1, A4 and A2 (Propositions 3 and 4) are now present; this one is not.",
    fix="project.html:603: change 'Assumption 2 in Propositions 1, 3 and 4' to 'Assumption 2 in Propositions 1, 2, 3 and 4'")
row("E4d3-cara-defined-twice", "2.9-prose", "course/modules/E/E4/project.html:259 (A3); course/modules/E/E4/L06.html:66-67",
    "PASS", "project.html has no <dfn> (grep count 0); L06.html:67 is the single <dfn>constant absolute risk aversion (CARA) utility</dfn> (Definition 6.2)")
row("E4d3-anchors-links", "2.9-DAG", "course/modules/E/E4/project.html (all href targets)",
    "PASS", "all href targets resolve (script this round)")
row("E4d3-no-figures-no-data", "2.8-figures", "course/modules/E/E4/project.html",
    "PASS", "no svg or img in project.html (grep count 0); the only data is the SIMULATED instance from the seed")
row("E4d3-spec-stop-rule-and-constraints", "2.6-spec", "project.html:317 (Constraints)",
    "PASS", "the stop rule (relative 1e-12 or 200 halvings) matches reference.py:20-21 and :136; 'no network' is stated but not enforced by any test (not a fault: no plausible wrong solution needs the network)")
row("E4d3-atlas-studios-na", "2.6-atlas", "atlas/; project.html",
    "PASS", "plans/E4-build-plan.md: no Atlas milestone and no studio for E4; project.html names none")
row("E4d4-mutant-absolute-tolerance-survives", "2.6-mutation", "grader/test_project.py (test_small_noise_root_is_relatively_accurate); ledgers/E4/mutants/mutant_r4_absolute_bracket_tolerance.py",
    "PASS", f"round-4 survivor now KILLED by test_small_noise_root_is_relatively_accurate[1e-06] (seed 0) ({L}/mutate_graders_r5_seeds0-9.txt)")
row("E4d4-alt4-wrong-on-small-noise", "2.6-alternatives", "ledgers/E4/alternatives/alt_4.py",
    "PASS", f"alt_4 rewritten (secant steps inside the sign-change bracket, relative stop 1e-13 x); on the probe grid (sd from 1e-12 to 5) its worst relative error on interior roots is 4.3e-13 and it has no boundary mismatch ({L}/probe_alts_r5.txt); passes seeds 0-49 ({L}/alternatives_seeds0-49.txt)")
row("E4d4-alt1-docstring", "2.6-alternatives", "ledgers/E4/alternatives/alt_1.py:1",
    "PASS", "docstring now reads 'bisection with a fixed 120 halvings and no tolerance check'; solve_model runs range(120) with no tolerance test (alt_1.py:77-84)")
row("E4d4-equivalent-price-slope", "2.6-mutation", "ledgers/E4/scripts/E4-d-r4/equivalent_candidate_price_slope.py; ledgers/E4/scripts/E4-d-r4/check_equivalence_r4.py",
    "PASS", f"candidate b_s = lam tau_e / D (drops (1-lam) tau_y). Argument: for any b, kappa = b_u/b_s is unchanged, Var(v-p_b) = V_I + S_I(b) = V_U + S_U(b) (Lemma 3 applies for any p, measurable with respect to the information set), so the gap is Omega_b^(-1/2) times a factor whose sign is sign(tau_bar - tau_y), and the root is the same. At lam = 1 the candidate's b_s is unchanged. Re-run this round ({L}/equivalence_price_slope_r5.txt): identity residual 3.73e-9 (float), 0 sign mismatches on 89,700 interior grid points, largest solver-output difference 2.27e-13 over 3000 random inputs. Not a fault: no output of solve_model distinguishes it beyond float noise, so it cannot fail a test. Placement in ledgers/E4/equivalent/ is the architect's call (as for literal_price_sign.py); it is not counted in mutants.")
row("E4d4-calibration-blind", "2.6-rubric", "project.html:530-595 (Exemplar A) and the verifier's own scoring",
    "UNVERIFIABLE", "Exemplar A's official verdict paragraph (project.html:530) was read before its passage was scored, so Exemplar A was not scored blind. Exemplar B was scored blind (E4d-exemplar-B-calibration). The rule needs both blind, so the calibration row cannot be PASS.",
    fix="a verifier who has not read project.html:529-595 (Exemplar A verdict and annotations) scores Exemplar A's passages from the rubric table alone and compares with data-scores 2,2,1,2,1")
row("E4d4-proposed-test-validated", "2.6-mutation", "grader/test_project.py:421-444 (the round-4 proposed test, now in the grader)",
    "PASS", f"the test is in the grader; with it, reference and alt_1..alt_5 pass seeds 0-49 (alt_5 fails only at noise_sd 1e-12, which the test does not cover) and the round-4 mutants fail ({L}/mutate_graders_r5_seeds0-9.txt)")
row("E4d4-mutants-killed-r4", "2.6-mutation", "ledgers/E4/mutants/mutant_r4_informed_precision_signal_only.py; mutant_r4_uninformed_variance_uses_signal_precision.py; mutant_r4_unit_fraction_reports_precision.py; mutant_r4f_*.py",
    "PASS", f"all KILLED ({L}/mutate_graders_r5_seeds0-9.txt)")
row("E4d4-exemplar-B-results-numbers", "2.2-numbers", "project.html Results passage (Exemplar B) and table",
    "PASS", "'every printed gap has absolute value below 4e-14' (max 3.55e-14); '1.2501 and 1.5000' (1.250090 and 1.500000); informativeness 0.1920, 0.1420, 0.0889 constant across the noise volumes at each cost")

# ---- round-5 verifier mutants (the tool rows)
row("E4d5-mutant-bracket-floor", "2.6-mutation", "ledgers/E4/mutants/mutant_r5_bracket_floor_1e-12.py (the bisection starts at lo = 1e-12); grader/test_project.py:212-216",
    "FAIL", f"verifier student-error mutant: the bisection starts at a lower end of 1e-12. It SURVIVES seeds 0-9 ({L}/mutate_graders_r5_seeds0-9.txt). At cost 0.15 it is wrong for every noise_sd below about 1.5e-12 (valid inputs, project.html:330-331; the root is 0.66 noise_sd there), and the page states that the bisection brackets the root in [0,1] (project.html:317). test_noise_volume_tiny_positive_is_accepted (sd = 1e-12) checks only the range of the outputs, so the survivor passes. Killed by the scratch tiny-root test ({L}/scratch_tiny_root_test_r5.txt).",
    fix="the tiny-root test in E4d-mutants-total (sd 1e-11 and 1e-12, relative 1e-8 against the closed form)")
row("E4d5-mutant-sixty-halvings", "2.6-mutation", "ledgers/E4/mutants/mutant_r5_sixty_halvings_no_tolerance.py (the loop runs 60 halvings, no relative check); grader/test_project.py:436-444",
    "FAIL", f"verifier student-error mutant: a fixed 60 halvings (as Lab 1 does) with no relative stop rule. It SURVIVES seeds 0-9 ({L}/mutate_graders_r5_seeds0-9.txt): its absolute width 2^-60 gives a relative error below 1e-8 for every root above about 4e-11, so the 1e-9 test does not see it. The stop rule is stated at project.html:317 (stops when the bracket is narrower than 1e-12 times its upper end). Killed by the scratch tiny-root test ({L}/scratch_tiny_root_test_r5.txt).",
    fix="the tiny-root test in E4d-mutants-total")
row("E4d5-mutant-uninformed-precision", "2.6-mutation", "ledgers/E4/mutants/mutant_r5_uninformed_posterior_precision_informed.py",
    "PASS", f"KILLED by test_indifference_holds_at_an_interior_fraction[first] (seed 0) ({L}/mutate_graders_r5_seeds0-9.txt). The first draft of this mutant referenced an undefined tau_e and was killed by a NameError; it was corrected to SIGNAL_PRECISION and killed by the intended test.")
row("E4d5-calibration-B-blind", "2.6-rubric", "project.html:597-659 (Exemplar B)",
    "PASS", "see E4d-exemplar-B-calibration (the blind scoring of Exemplar B, C1 3 against annotated 4, within one level)")

mutant_ids = [m["id"] for m in mutants]
counts = {s: sum(1 for r in R if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if all(r["status"] == "PASS" for r in R) else "FAIL"
killed = sum(1 for m in mutants if m["killed_by"])

frag = {
    "unit": "E4",
    "slice": "d",
    "round": 5,
    "verifier": "Haiku independent verifier, E4 slice d, round 5 (did not build E4)",
    "pin": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f",
    "base": "9a02b1a (round-4 pin). Delta in this slice since 9a02b1a: course/modules/E/E4/project.html (10 lines: lede, Constraints count 32, Grading mode, C1 descriptor, Assumption use-lists), grader/reference.py (docstring units), grader/test_project.py (oracle_gap docstring, test_small_noise_root_is_relatively_accurate), ledgers/E4/alternatives/alt_1..alt_5.py, ledgers/E4/mutants/mutant_r4f_*.py (added). Lab twins project-1..3 are byte-identical since 9a02b1a and were re-run.",
    "checkout": str(root),
    "scratch": "/tmp/e4r5-* (temporary copies for the tiny-root scratch test; removed). The course files are untouched. Every script that backs a row is under ledgers/E4/scripts/E4-d-r5/ (and the round-4 equivalence script under ledgers/E4/scripts/E4-d-r4/).",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": R,
    "mutants": mutants,
    "registry_flags": [
        "muth1961rational: record verified (Econometrica 29(3) 315, 1961; DOI 10.2307/1909635); live verify_refs E4 0 problems this round.",
        "milgrom1982information: record title 'Information, trade and common knowledge' (JET 26(1), 1982), authors Milgrom & Stokey; the page attributes no statement to it.",
    ],
    "freshness_flags": [],
    "notes": [
        "Round 5 changed the E4 project slice: the Lemma 1 hypothesis gap, the C1 rubric boundary, the Exemplar B use-list (A2 and Proposition 2), the alt_5 bracket floor, and the tiny-noise grader gap are new FAIL rows.",
        "Round-4 fixes verified this round: the relative small-noise test is now in the grader and kills the absolute-tolerance mutant; alt_1 docstring fixed; alt_4 rewritten and now correct on the probe grid; C1 'in general terms' removed; the grader count (32) matches collect-only.",
        "Scratch validation of the fix (not part of the course): a relative test at noise_sd 1e-11 and 1e-12 (cost 0.15, relative 1e-8 against the Proposition 4 closed form) passes the reference and alt_1..alt_4 on seeds 0-9 and fails alt_5 and both verifier survivors ({L}/scratch_tiny_root_test_r5.txt). alt_2 is within 7.8e-9 relative of the reference at noise_sd 1e-12, close to the 1e-8 tolerance.",
        "Calibration: Exemplar B scored blind from its passage text before its annotation was read (C1 3 against annotated 4, within one level); Exemplar A was not blind (its verdict paragraph was read first), so E4d4-calibration-blind is UNVERIFIABLE.",
        "Equivalent candidate (price slope, E4d4-equivalent-price-slope) is observationally equivalent through solve_model (proof and randomized check in the row) and is not a fault; its placement is the architect's call.",
        "Spec question (not blocking): which point of the final bracket is reported (the midpoint, as Exemplar B says, or the endpoint); both are within 1e-12 relative and the spec does not say.",
        "Not checked: a Pyodide run by hand (page_smoke's in-browser grader PASS was used); the self-assessment form's JavaScript beyond page_smoke; the 350-800 word limit (no report exists in the repository); the Muth and Milgrom abstracts (the page attributes no statement to either); a blind scoring of Exemplar A.",
        "Rows PASS by carry-forward: none. Every round-4 row was re-verified against the round-5 subject, except the notation, equivalence and reference-registry rows, whose subjects were re-run this round as well.",
    ],
    "summary": {
        "rows": len(R),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants_killed": killed,
        "mutants": len(mutants),
    },
}

out = root / "ledgers/E4/E4-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(R), counts, "mutants", killed, "/", len(mutants), "verdict", verdict)
