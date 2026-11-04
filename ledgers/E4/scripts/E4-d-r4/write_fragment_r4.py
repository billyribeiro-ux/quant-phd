"""Write the round-4 E4 slice-d ledger fragment (ledgers/E4/E4-d.json). Run from the checkout root:
python -I ledgers/E4/scripts/E4-d-r4/write_fragment_r4.py  (after the commands listed in each row's evidence)."""

import datetime
import json
from pathlib import Path

LG = "ledgers/E4/scripts/E4-d-r4/logs"
rows: list[dict[str, str]] = []


def R(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, rid
        row["fix"] = fix
    rows.append(row)


R("E4d-cmd-check-projects", "2.6", "course/modules/E/E4/project.html; grader/", "PASS",
  f"tools/check_projects.py --unit E4 -> 'check_projects E4: PASS', exit 0 ({LG}/check_projects.txt)")
R("E4d-cmd-check-pages", "2.9", "course/modules/E/E4/project.html", "PASS",
  f"tools/check_pages.py --unit E4 -> 'check_pages E4: PASS', exit 0 ({LG}/check_pages.txt)")
R("E4d-cmd-check-dag", "2.9", "course/modules/E/E4/project.html", "PASS",
  f"tools/check_dag.py --unit E4 -> 'check_dag E4: PASS', exit 0 ({LG}/check_dag.txt)")
R("E4d-cmd-run-labs", "2.5", "tests/labs/E4/lab-E4-project-1.py, -2.py, -3.py", "PASS",
  f"tools/run_labs.py --unit E4 -> 'run_labs E4: PASS (12/12)', exit 0 ({LG}/run_labs.txt); the tool checks twin byte-identity with the page code, runs each twin under python -I -W error, and matches the expected block")
R("E4d-cmd-run-graders", "2.6 item 1", "course/modules/E/E4/grader/reference.py", "PASS",
  f"tools/run_graders.py --unit E4 --seeds 0-49 -> 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 ({LG}/run_graders.txt)")
R("E4d-cmd-page-smoke-project", "2.6 item 5; 2.9", "course/modules/E/E4/project.html", "PASS",
  f"tools/page_smoke.py --unit E4 --pages project -> 'page_smoke E4: PASS', exit 0 ({LG}/page_smoke_project.txt)")
R("E4d-cmd-ruff", "gate", "repository (ruff check ., ruff format --check .)", "PASS",
  "ruff check . -> 'All checks passed!'; ruff format --check . -> '553 files already formatted' (this checkout at 9a02b1a plus the round-4 files; ledgers/*/mutants, scripts, alternatives and equivalent are in pyproject extend-exclude)")
R("E4d-cmd-mypy-workspace", "2.6 / BUILDER_RULES 6.2 strict", "repository mypy (tests/labs/E4 and grader)", "PASS",
  f"mypy --no-incremental -> 'Success: no issues found in 385 source files', exit 0 ({LG}/mypy_r4.txt)")
R("E4d-cmd-mypy-plan-command", "gate", "tests/labs/E4; grader", "PASS",
  f"same mypy run as E4d-cmd-mypy-workspace ({LG}/mypy_r4.txt)")
R("E4d-cmd-pytest-relevant", "gate", "tests/test_page_checks.py, test_labs.py, test_run_labs.py, test_memo_exemplars.py", "PASS",
  f"pytest -q on the four modules -> exit 0 ({LG}/pytest_relevant_r4.txt)")
R("E4d-cmd-verify-refs", "2.1", "references/references.json (E4 keys)", "PASS",
  f"tools/verify_refs.py --unit E4 (live Crossref) -> 'live re-verification of E4: 3 of 560 entries, 0 problems', exit 0 ({LG}/verify_refs_E4_r4_live.txt)")
R("E4d-cmd-collect", "2.6 grader count", "course/modules/E/E4/grader/test_project.py", "PASS",
  f"pytest --collect-only in a scratch workspace with reference.py as solver.py -> '30 tests collected' ({LG}/collect_r4.txt); the page says 'runs 30 checks' (project.html:319)")
R("E4d-lab-project-1", "2.5", "course/modules/E/E4/project.html #lab-E4-project-1; tests/labs/E4/lab-E4-project-1.py", "PASS",
  f"run_labs E4 PASS ({LG}/run_labs.txt); the printed values in project.html:57 (gaps +0.053092 and -0.080731, root 0.57937525, tau_bar 0.18904110, informativeness 0.15898618) equal the expected block at project.html:156-170")
R("E4d-lab-project-2", "2.5 completion", "course/modules/E/E4/project.html #lab-E4-project-2; tests/labs/E4/lab-E4-project-2.py", "PASS",
  f"run_labs E4 PASS ({LG}/run_labs.txt); the blank (project.html:217) is the only changed line; the printed gap at 1 (-0.071386), root 0.57052263 and informativeness 0.12466375 agree with the reference at (0.7, 0.14) ({LG}/indep_r4.txt item 3 gives the root to 1e-12)")
R("E4d-lab-project-3", "2.5", "course/modules/E/E4/project.html #lab-E4-project-3; tests/labs/E4/lab-E4-project-3.py", "PASS",
  f"run_labs E4 PASS ({LG}/run_labs.txt); the nine rows of project.html:629-637 equal the printed rows of the expected block (project.html:488-496); 484 of 484 box points ({LG}/indep_r4.txt item 3)")
R("E4d-num-lab-hypotheses", "2.2 (a)", "project.html:57, :176, :375 (Lab hypothesis paragraphs)", "PASS",
  f"Lab 1 and Lab 2 values equal their expected blocks (run_labs). Lab 3 hypothesis: fractions 0.5582/0.6978/0.8373 equal the Proposition 4 closed form at sd 0.500/0.625/0.750, c 0.120 ({LG}/indep_r4.txt item 3); informativeness 1-e^(4c)/2 = 0.19196, 0.14200, 0.08894 for c 0.120, 0.135, 0.150 (hand computation, consistent with the printed grid); printed gaps max 3.55e-14 < 1e-13; bisection vs closed form 2.13e-13 < 1e-12 ({LG}/indep_r4.txt item 3)")
R("E4d-num-exemplar-table", "2.2 (c)", "project.html:625 (Results passage) and :629-637 (table)", "PASS",
  f"all nine table rows equal the Lab 3 printed rows (project.html:488-496) for fraction, informativeness and gap; ratios 0.6978/0.5582 = 1.250090 (displays 1.2501) and 0.8373/0.5582 = 1.500000 (displays 1.5000) ({LG}/indep_r4.txt item 4); unrounded closed-form ratio 0.625/0.5 = 1.250000000000")
R("E4d-num-box-bounds", "2.2 (c)", "project.html:313 (Inputs); grader/instance.py:14-17", "PASS",
  "tau_bar(0.150) = 2e^-0.6 - 1 = 0.09762327 and tau_bar(0.120) = 2e^-0.48 - 1 = 0.23756678 (python math, this round); 1/(1+4*0.75^2) = 0.30769231; the page's 0.097623 <= tau_bar <= 0.237567 and 0.30769 are correct roundings; instance.py:14-16 gives the same values")
R("E4d-prose-lede-directional", "2.9 / 1.2 scope", "project.html:37 (lede)", "PASS",
  f"with the fraction fixed, tau_y = lam^2 tau_e^2/(lam^2 tau_e + a^2 sd^2) falls in sd, so the informativeness falls (Proposition 2); on the interior the fraction is proportional to sd (ratio 1.250000000000 in {LG}/indep_r4.txt item 4) and the informativeness does not depend on sd (Proposition 5)")
R("E4d-math-lemmas", "2.4", "project.html:266-273 (Lemmas 1-3)", "PASS",
  "re-derived: Lemma 1 maximiser x* = (m-p)/(aV) and value -exp(ac)exp(-(m-p)^2/(2V)) with g(x*) = (m-p)^2/(2aV); Lemma 2 integral gives (V/(V+S))^(1/2); Lemma 3 Var(v-p) = V + Var(m-p). The hypotheses (V constant, p measurable, normal Z) are on the page")
R("E4d-math-prop1", "2.4", "project.html:276-278 (Proposition 1, proof steps 1-4)", "PASS",
  f"re-derived steps (1)-(4): kappa = -a/(lam tau_e); x_I = (tau_e s - (tau_v+tau_e)p)/a; x_U = (tau_y y - (tau_v+tau_y)p)/a; D b_s = lam tau_e + (1-lam) tau_y. Numerically the reference price clears the market to <= 2.2e-16 at five (lam, sd) pairs, with demands from covariance-matrix regression ({LG}/indep_r4.txt item 1). The sentence changed in step (1) (information-set inclusion) is correct")
R("E4d-math-prop2", "2.4", "project.html:284-285 (Proposition 2)", "PASS",
  "Cov(v,p) = b_s/tau_v and Var(p) = b_s^2 (1/tau_v + 1/tau_y) give Corr^2 = tau_y/(tau_v+tau_y) (re-derived); lam = 0 case: x_U = -tau_v p/a = u gives p = -a u/tau_v (re-derived)")
R("E4d-math-prop3", "2.4", "project.html:287-291 (Proposition 3)", "PASS",
  f"re-derived: sign G = sign(V_U - e^(2ac) V_I) = sign(tau_bar - tau_y) via the factor (tau_v+tau_y)(tau_v+tau_e)e^(-2ac); G(0+) formula re-derived from the limits b_s/lam -> tau_e/tau_v and b_u -> -a/tau_v. Numerically, the gap by 3-D quadrature with the actual CARA demands equals the reference gap to 1e-10 at three interior points ({LG}/indep_r4.txt item 2)")
R("E4d-math-prop4", "2.4", "project.html:294-296 (Proposition 4)", "PASS",
  f"closed form re-derived (lam^2 (tau_e^2 - tau_bar tau_e) = tau_bar a^2 sd^2). The reference bisection equals the closed form to 2.13e-13 on the 3x3 grid and to 4e-13 relative at sd 1e-6, 1e-9, 1e-12 ({LG}/indep_r4.txt item 3; {LG}/small_noise_probe_r4.txt)")
R("E4d-math-prop5", "2.4", "project.html:299-302 (Proposition 5 and the paragraph at :302)", "PASS",
  "lam* = a sd k(tau_bar) with k(t) = sqrt(t/(tau_e(tau_e-t))) strictly increasing; tau_bar strictly decreasing in c; d lam*/d sd = lam*/sd re-derived; the grid's ratio 1.250000000000 confirms proportionality; informativeness tau_bar/(tau_v+tau_bar) does not depend on sd")
R("E4d-math-assumptions", "2.4", "project.html:257-261 (A1-A5)", "PASS",
  "A1-A5 are numbered and used by Propositions 1-5 (the use-list in the exemplar is checked in E4d2-exemplar-B-C1-annotation); the CARA form is cited to Definition 6.2 of L06 (project.html:259; L06.html:66-67)")
R("E4d-notation", "2.4 / notation", "project.html math spans; notation/notation.json", "PASS",
  "registered symbols (notation.json): T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q. The page uses none of them (grep). Macros used: E, Var, Cov, Corr, Normal, all registered. Local symbols are defined on the page (notation paragraph project.html:253; Propositions 1-5). Note, not a row failure: the information set is \\mathcal F (Lemma 1, Proposition 1 and 3 proofs) and the uninformed term is F_U and F_I; the glyphs differ and the letter is not registered")
R("E4d-banned-phrases", "1.3-1.4 (BUILDER_RULES)", "course/modules/E/E4/project.html", "PASS",
  "grep -i for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, it can be shown, roughly, historically, about 6: no hits")
R("E4d-process-words", "2.9 / learner text", "course/modules/E/E4/project.html", "PASS",
  "grep -i for verif, builder, round N, fixture, agent, ruling, architect, pass N, blind: only 'C2 · Solver and verification' (a rubric criterion name) and a code docstring")
R("E4d-dag-links", "2.9 / DAG", "course/modules/E/E4/project.html", "PASS",
  "every href and fragment target resolves (no missing id); index.html#placement exists; L06.html#def-noisy-rational-expectations-equilibrium, L07.html#def-price-informativeness and concepts.html#expected-utility exist; check_dag E4 PASS")
R("E4d-registry-muth", "2.1", "course/modules/E/E4/project.html reading list (data-cite muth1961rational)", "PASS",
  "references.json: Muth, 'Rational Expectations and the Theory of Price Movements', Econometrica 29(3) 315, 1961, DOI 10.2307/1909635, status verified; live verify_refs E4 PASS; the page attributes no statement to it (project.html:678)")
R("E4d-registry-milgrom", "2.1", "project.html:678, :681", "PASS",
  "references.json: Milgrom & Stokey, 'Information, trade and common knowledge', J. Econ. Theory 26(1) 17-27, 1982, DOI 10.1016/0022-0531(82)90046-1, status verified; the page attributes no statement to it, so no attribution row is needed")
R("E4d-cites-only-registry", "2.1", "project.html data-cite (lines 680-681)", "PASS",
  "only muth1961rational and milgrom1982information are cited; both keys exist in references.json (used_by E4)")
R("E4d-spec-context-sentences", "2.6 spec", "project.html:311 (Context)", "PASS",
  "Context has four sentences (project.html:311)")
R("E4d-spec-questions", "2.6 spec", "project.html:314-321 (Required outputs, Constraints, Grading mode)", "PASS",
  "questions a competent student would ask: (1) which point of the final bracket is the reported fraction, the midpoint (as Exemplar B says at project.html:614) or the endpoint? The spec is silent; the suite's root tolerance (1e-10) accepts either. (2) What is returned for a NaN or infinite information cost? The exception table names only a negative cost, and any behaviour is allowed (project.html:325). Neither question blocks a correct solver; (1) should be stated in Constraints")
R("E4d-spec-ladder", "2.6 ladder", "project.html:40-49 (ladder), :51-305 (rungs 1-2), :308 (rung 3), :668-674 (rung 4)", "PASS",
  "rung 1 is annotated and printed (Lab 1 steps 1-6); rung 2 is the instant completion check (Lab 2 blank); rung 3 is the spec; rung 4 is open-ended (stretch)")
R("E4d-prose-scope-words", "2.9 / 1.2 scope", "course/modules/E/E4/project.html", "PASS",
  "scope words checked at project.html:257, :259, :263, :302, :313, :317, :321, :375, :385: each 'every', 'all', 'any', 'only', 'same' is definitional, computed (484 grid points; the A1 normalization; the CARA wealth factor) or restricts a noun phrase; no unsupported universal claim found")
R("E4d-prose-simulated-labs", "2.8 SIMULATED", "project.html Labs 1-3 (:57, :176, :375) and Inputs (:313); grader/instance.py", "PASS",
  "each lab and the Inputs paragraph say SIMULATED; instance.py docstring says SIMULATED")
R("E4d-prose-simulated-exemplars", "2.8 SIMULATED", "project.html:530", "PASS",
  "the exemplar passage says 'on a SIMULATED instance' (project.html:530)")
R("E4d-hours-project", "2.6 hours", "project.html:33, :343-350 (#hours); course/modules/E/E4/index.html:29", "PASS",
  "hub data-hours-lessons=72 and data-hours-project=28 sum to 100 (curriculum E4 hours 100); project header 28 hours; hours table 1+1+5+8+5+5+3 = 28")
R("E4d-hours-estimate", "2.6 hours", "project.html #hours table", "PASS",
  "verifier estimate: reading and Lab 1-2 about 2 h, derivation of Propositions 1-4 about 6 h, solver and local suite about 4-6 h, grid and display about 5 h, report about 5-6 h, self-assessment 3 h: about 25-28 h, within 30% of 28")
R("E4d-rubric-observable", "2.6 rubric", "project.html:516-526 (#rubric)", "FAIL",
  "C1 level 1 descriptor 'Describes the model in general terms, with no payoff, signal or utility function written down.' (project.html:520) uses the vague qualifier 'in general terms', which no grader can observe; the other descriptors are observable",
  "project.html:520: change 'Describes the model in general terms, with no payoff, signal or utility function written down.' to 'Describes the model in words, with no payoff, signal or utility function written down as a formula.'")
R("E4d-exemplar-A-calibration", "2.6 rubric calibration", "project.html:532-595 (exemplar A, data-scores 2,2,1,2,1)", "PASS",
  "descriptor-level scoring of exemplar A passages: C1 2 (words, no coefficient), C2 2 (method and bracket, no tolerance), C3 1 (sign with no grid), C4 2 (fixed decimals, no rule), C5 1 (caveat, no named limit): equal to the annotations. NOT blind (see E4d4-calibration-blind)")
R("E4d-exemplar-B-calibration", "2.6 rubric calibration", "project.html:597-659 (exemplar B, data-scores 4,4,4,4,4)", "PASS",
  "descriptor-level scoring: C2, C3, C4, C5 at 4 match; C1 scores 3 on the descriptor 'names each result that uses it' (see E4d2-exemplar-B-C1-annotation), within one level of the annotated 4. NOT blind (see E4d4-calibration-blind)")
R("E4d-exemplar-annotations-hidden", "2.6 rubric", "course/assets/js/rubric.js:147-150; project.html data-reveal", "PASS",
  "rubric.js and labs.js are byte-identical to the round-3 pin (git diff 67a2d13..9a02b1a empty); data-reveal attributes unchanged")
R("E4d-grader-exceptions", "2.6 items 3-4", "grader/test_project.py:190-240; grader/reference.py:23-31; project.html:330-331", "PASS",
  "the two named ValueError conditions are tested in both directions; messages equal the table's text; the table names only these two; test_noise_volume_tiny_positive_is_accepted is valid")
R("E4d-grader-messages", "2.6 item 4", "grader/test_project.py:48-67 (expect, must_raise) and every expect() message", "PASS",
  "messages name the property with a hint and contain no numeric answer; the suite passes 30 of 30 on the reference with the browser flags")
R("E4d-grader-oracle", "2.6 item 3", "grader/test_project.py:9-14, 79-170", "PASS",
  "oracle is fixed-point price iteration with quadrature and does not import the reference; it agrees with the reference to the test tolerances on all 50 seeds (run_graders 50/50)")
R("E4d-grader-instances", "2.6 item 2", "grader/instance.py; grader/test_project.py:37-39", "PASS",
  f"20 seeds (0-19): every instance valid, every reference fraction strictly interior, 20 distinct (sd, c) pairs and 20 distinct fractions ({LG}/sample_instances_r4.txt)")
R("E4d-grader-instance-docstring", "1.4 docstring claims", "grader/instance.py:14-17", "PASS",
  "the bound 0 < tau_bar < 0.237567 < 0.30769 <= tau_y(1) is checked numerically (see E4d-num-box-bounds); the docstring says the suite does not re-check it")
R("E4d-grader-test-docstring", "1.4 / 2.2 sentence vs assertion", "grader/test_project.py:9-14, :365, :369-373, :378-386", "PASS",
  "test_fraction_falls_with_the_cost asserts the Proposition 5 monotonicity its docstring names; test_fraction_is_proportional asserts the proportionality its docstring names (reference gives 1.25 exactly)")
R("E4d-grader-reference-docstring", "1.4 docstring claims", "grader/reference.py:3-6, :19-20, :35-87, :89-90, :102-104", "PASS",
  "'200 halvings exceed any relative tolerance' (2^-200 < 1e-60); the lam -> 0 price limit -a u/tau_v (checked algebraically); the hypothetical uninformed agent at lam = 1 matches Proposition 3")
R("E4d-grader-stdlib", "2.6 item 4 / ruling 10", "grader/test_project.py:403-412", "PASS",
  "the test asserts stdlib imports only; reference.py and all five alternatives import only math, sys or nothing")
R("E4d-mutants-existing", "2.6 item 3", "ledgers/E4/mutants/mutant_01..mutant_10", "PASS",
  f"tools/mutate_graders.py --unit E4 --seeds 0-9: all ten builder mutants KILLED ({LG}/mutate_graders_r4_seeds0-9.txt)")
R("E4d-mutants-new", "2.6 item 3", "ledgers/E4/mutants/mutant_d11..mutant_d18", "PASS",
  f"all eight KILLED in the same run ({LG}/mutate_graders_r4_seeds0-9.txt)")
R("E4d2-mutants-r2", "2.6 item 3", "ledgers/E4/mutants/mutant_r2_*.py", "PASS",
  f"all four KILLED in the same run ({LG}/mutate_graders_r4_seeds0-9.txt)")
R("E4d3-mutants-r3", "2.6 item 3", "ledgers/E4/mutants/mutant_r3_*.py", "PASS",
  f"the four round-3 closed-form and boundary mutants KILLED in the same run ({LG}/mutate_graders_r4_seeds0-9.txt)")
R("E4d3-mutant-tolerance-survives", "2.6 item 3; stated stop rule project.html:317", "grader/test_project.py:44 (TOL_ROOT); ledgers/E4/mutants/mutant_r3_tolerance_1e-9.py", "PASS",
  f"the round-3 survivor is now KILLED by test_fraction_is_the_oracle_root[first] (seed 0) with TOL_ROOT = 1e-10 ({LG}/mutate_graders_r4_seeds0-9.txt); on seeds 0-9 in the scratch suite it FAILs 9 seeds ({LG}/scratch_suite_with_small_noise_test_seeds0-9.txt)")
R("E4d-mutants-total", "2.6 item 3", "ledgers/E4/mutants/ (31 mutants)", "FAIL",
  f"30 of 31 KILLED ({LG}/mutate_graders_r4_seeds0-9.txt). The survivor is mutant_r4_absolute_bracket_tolerance (row E4d4-mutant-absolute-tolerance-survives)",
  "add the small-noise test of row E4d4-mutant-absolute-tolerance-survives to grader/test_project.py (text in ledgers/E4/scripts/E4-d-r4/proposed_test_project_with_small_noise_test.py)")
R("E4d-equivalent", "2.6 item 3 (equivalence proof)", "ledgers/E4/equivalent/literal_price_sign.py; ledgers/E4/equivalent/README.md", "PASS",
  "round-3 equivalence (literal b_u sign) is unchanged since the pin; its argument (b_u enters only as b_u*b_u) is re-read and correct")
R("E4d-alternatives", "2.6 item 3 (ruling 10; plan 5.5)", "ledgers/E4/alternatives/alt_1..alt_5.py", "FAIL",
  f"all five pass seeds 0-49 on the current grader ({LG}/alternatives_seeds0-49.txt), but alt_4 is wrong on a valid input (row E4d4-alt4-wrong-on-small-noise); plan section 5.5 says a float alternative wrong on a stated exact rule is a mutant, not an alternative",
  "replace alt_4 with a correct bracketed or damped method, or move it to ledgers/E4/mutants/ (the new small-noise test then kills it)")
R("E4d-starter", "2.6 item 1", "grader/starter.py", "PASS",
  "starter.py raises NotImplementedError; the suite on the starter gives 29 failed and 1 passed (the stdlib test) (scratch run, this round)")
R("E4d-browser-local-parity", "2.6 item 5", "grader/test_project.py; page_smoke", "PASS",
  "page_smoke project PASS (browser path) and local pytest with the browser flags: 30 passed on the reference")
R("E4d-runtime", "2.5 / 2.6 runtime", "grader/test_project.py", "PASS",
  "local run of the 30 tests on the reference: 0.03 s; page_smoke timing PASS")
R("E4d2-exemplar-B-C1-annotation", "2.6 rubric (annotation accuracy)", "project.html:603 (Model passage) and :607 (annotation)", "FAIL",
  "the exemplar says 'Assumption 1 is used in Proposition 1 and Proposition 3', 'Assumption 2 in Proposition 1', 'Assumption 4 in Proposition 1 and Proposition 2', and the annotation says it 'names the results that use it'. The proofs use more: A1 in Proposition 2 (Cov(v,y) = Var(v) and Var(y) = 1/tau_v + 1/tau_y, project.html:285); A2 in Proposition 3 (u normal in Lemma 2 applied at project.html:292) and Proposition 4 (lam* proportional to sigma, project.html:295); A4 in Proposition 3 (m_I - p linear in (s,u), project.html:292)",
  "project.html:603: add Proposition 2 to Assumption 1, Propositions 3 and 4 to Assumption 2, and Proposition 3 to Assumption 4; or change the annotation at :607 so it does not claim the list is complete")
R("E4d3-cara-defined-twice", "1.10 (no concept defined twice)", "course/modules/E/E4/project.html:259 (A3); course/modules/E/E4/L06.html:66-67", "PASS",
  "fixed: project.html:259 links 'Definition 6.2 of Lesson 6' with no <dfn> (grep -c '<dfn' project.html gives 0); L06.html:66-67 is the single <dfn> definition of CARA utility")
R("E4d3-anchors-links", "2.9", "course/modules/E/E4/project.html (all href targets)", "PASS",
  "all href targets resolve (see E4d-dag-links)")
R("E4d3-no-figures-no-data", "2.8", "course/modules/E/E4/project.html", "PASS",
  "no figure, chart or data file is in the page; the only data is the SIMULATED instance from the seed")
R("E4d3-spec-stop-rule-and-constraints", "2.6 spec", "project.html:317 (Constraints)", "PASS",
  "the stop rule (relative 1e-12 or 200 halvings) matches reference.py:19-20 and :135; 'no network' is stated but not enforced by any test (not a fault: no plausible wrong solution needs the network)")
R("E4d3-atlas-studios-na", "2.6 atlas and studios", "atlas/; project.html", "PASS",
  "plans/E4-build-plan.md: no Atlas milestone and no studio for E4; project.html names none")
R("E4d4-mutant-absolute-tolerance-survives", "2.6 item 3; stated stop rule project.html:317", "grader/test_project.py (no test of the relative stop rule at a small root); ledgers/E4/mutants/mutant_r4_absolute_bracket_tolerance.py", "FAIL",
  f"mutate_graders seeds 0-9 SURVIVED ({LG}/mutate_graders_r4_seeds0-9.txt); run_candidates_r4 seeds 0-49 PASS ({LG}/absolute_mutant_seeds0-49.txt). The mutant stops at an absolute bracket width of 1e-12. At sd = 1e-9, c = 0.13 the exact fraction is 9.6562541015e-10, the mutant gives 9.6542862593e-10 (relative error 2.0e-4) and the reference 5.5e-14 ({LG}/small_noise_probe_r4.txt). The box has roots between 0.33 and 0.84, where absolute and relative widths nearly coincide, and test_noise_volume_tiny_positive_is_accepted checks only the range. project.html:317 states the relative rule",
  "add to grader/test_project.py: @pytest.mark.parametrize('sd', [1e-6, 1e-9]) def test_small_noise_root_is_relatively_accurate(sd: float) -> None, which compares run(sd, 0.13)['informed_fraction'] with the Proposition 4 closed form written in the test (not from reference.py) with abs(lam - exact) <= 1e-8 * exact and a failure message that names the relative stop rule. Validated in a scratch copy (see E4d4-proposed-test-validated)")
R("E4d4-alt4-wrong-on-small-noise", "2.6 item 3 (ruling 10; plan 5.5)", "ledgers/E4/alternatives/alt_4.py (damped iteration, clamp at 1e-12, stop at a step of 1e-15)", "FAIL",
  f"valid input sd = 1e-6, c = 0.13: alt_4 returns 1.0000000000e-12 (its clamp) where Proposition 4 gives 9.6562541015e-07; sd = 1e-9 gives 1.0e-12 against 9.6562541015e-10 ({LG}/small_noise_probe_r4.txt). The current suite passes it only because the box has sd >= 0.5. The scratch suite with the new test FAILs alt_4 on seeds 0-9 ({LG}/scratch_suite_with_small_noise_test_seeds0-9.txt)",
  "alt_4 is not a correct alternative: bracket the root inside [0,1] and iterate with a relative stop, or move it to ledgers/E4/mutants/ as a wrong solution")
R("E4d4-alt1-docstring", "1.4 docstring vs code", "ledgers/E4/alternatives/alt_1.py:1", "FAIL",
  "the docstring says 'bisection with an absolute tolerance and a fixed number of steps', but solve_model runs exactly 120 halvings with no tolerance test (alt_1.py:77-84)",
  "alt_1.py:1: change the docstring to 'bisection with a fixed 120 halvings and no tolerance check (the reference's method)'")
R("E4d4-equivalent-price-slope", "2.6 item 3 (equivalence proof; ruling 9)", "ledgers/E4/scripts/E4-d-r4/equivalent_candidate_price_slope.py; ledgers/E4/scripts/E4-d-r4/check_equivalence_r4.py", "FAIL",
  f"candidate: b_s = lam tau_e / D (drops (1-lam) tau_y from Proposition 1's b_s). Proof: for any scalar b in place of b_s, with kappa = b_u/b_s unchanged, Var(v - p_b) = Omega_b = V_I + S_I(b) = V_U + S_U(b) (Lemma 3; residual <= 3.7e-9 at extreme small lam from float cancellation, {LG}/check_equivalence_r4.txt). So F_I(b) = (V_I/Omega_b)^(1/2), F_U(b) = (V_U/Omega_b)^(1/2) and sign G_b(lam) = sign(tau_bar - tau_y(lam)) for every b: 0 sign mismatches on 89,700 interior grid points. The bisection visits the same points and returns the same root; the gap at the root is 0 in both; the largest solver-output difference over 3000 random inputs is 2.3e-13 (float noise). Not killable through solve_model. Ruling 9 admits equivalent/ only for mutants that differ where the page states nothing; this one differs from Proposition 1's b_s formula, so the placement rule does not cover it as written",
  "architect ruling: either amend ruling 9 to admit observational equivalence through the interface (with this proof) and move the candidate to ledgers/E4/equivalent/, or record the deviation; no grader change can kill it")
R("E4d4-calibration-blind", "2.6 rubric calibration (blind scoring)", "project.html:597-659; the verifier's own scoring", "UNVERIFIABLE",
  "the exemplars and annotations were read before this scoring, so the blind scoring the rules require was not performed; descriptor-level scoring (E4d-exemplar-A-calibration, E4d-exemplar-B-calibration) is indicative only",
  "re-run the exemplar scoring with a verifier who has not read project.html:529-659, scoring from the rubric table alone")
R("E4d4-proposed-test-validated", "2.6 item 3 (check of the proposed fix)", "ledgers/E4/scripts/E4-d-r4/proposed_test_project_with_small_noise_test.py", "PASS",
  f"the proposed grader addition was run in a scratch copy only (course files untouched): reference, alt_1, alt_2, alt_3, alt_5 PASS on seeds 0-9; mutant_r4_absolute_bracket_tolerance and mutant_r3_tolerance_1e-9 FAIL; alt_4 FAIL ({LG}/scratch_suite_with_small_noise_test_seeds0-9.txt). The test does not depend on the seed")
R("E4d4-mutants-killed-r4", "2.6 item 3 (new student-error mutants)", "ledgers/E4/mutants/mutant_r4_informed_precision_signal_only.py; mutant_r4_uninformed_variance_uses_signal_precision.py; mutant_r4_unit_fraction_reports_precision.py", "PASS",
  f"three new student-error mutants KILLED for the stated reason ({LG}/mutate_graders_r4_seeds0-9.txt): informed precision drops tau_v (test_indifference_holds_at_an_interior_fraction[first]); uninformed variance uses tau_e (test_gap_is_the_oracle_gap_at_the_reported_fraction[first]; an earlier version referenced an undefined name and was rewritten); unit fraction reports tau_y (test_unit_fraction_is_reported_at_zero_cost)")
R("E4d4-exemplar-B-results-numbers", "2.2 (c)", "project.html:625-659 (Results passage and table)", "PASS",
  "'every printed gap has absolute value below 4e-14' (max 3.55e-14 in the table); '1.2501 and 1.5000' (1.250090 and 1.500000); informativeness constant across noise volumes at each cost (0.1920, 0.1420, 0.0889)")

# ---- mutants from the round-4 mutate log (31 files in ledgers/E4/mutants/)
mutants = []
for line in (Path(LG) / "mutate_graders_r4_seeds0-9.txt").read_text(encoding="utf-8").splitlines():
    if line.startswith(("KILLED ", "SURVIVED ")):
        _, rest = line.split(" ", 1)
        name, tail = rest.split(": ", 1)
        desc, kill = tail.rsplit(" -> ", 1)
        mutants.append({"id": name[:-3], "description": desc, "killed_by": None if kill == "None" else kill})
assert len(mutants) == 31, len(mutants)

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"
killed = sum(1 for m in mutants if m["killed_by"])
fragment = {
    "unit": "E4",
    "slice": "d",
    "round": 4,
    "verifier": "Haiku independent verifier, E4 slice d round 4 (did not build E4)",
    "pin": "9a02b1a",
    "base": "67a2d13 (round-3 pin). Delta since 67a2d13: course/modules/E/E4/project.html (14 lines), grader/instance.py (docstring bound), grader/test_project.py (TOL_ROOT 1e-6 to 1e-10), ledgers/E4/mutants/mutant_r3_*.py (added). Lab twins project-1..3 are byte-identical since 67a2d13 and were re-run anyway.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE4-E4-d",
    "scratch": "/tmp/e4d4-scratch (proposed grader copy only; course files untouched). Every script that backs a row is under ledgers/E4/scripts/E4-d-r4/",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "muth1961rational: record verified (Econometrica 29(3) 315, 1961; DOI 10.2307/1909635); live verify_refs E4 0 problems.",
        "milgrom1982information: record title 'Information, trade and common knowledge' (JET 26(1), 1982), authors Milgrom & Stokey; the page attributes no statement to it.",
    ],
    "freshness_flags": [],
    "notes": [
        "Round-4 mutants: four new student-error mutants in ledgers/E4/mutants/mutant_r4_*.py, one edit each of grader/reference.py (generated by ledgers/E4/scripts/E4-d-r4/make_r4_mutants.py). The price-slope candidate is not in mutants/ (row E4d4-equivalent-price-slope).",
        "Alternatives: all five pass seeds 0-49 on the current grader; alt_4 is nevertheless wrong on small valid noise volumes (row E4d4-alt4-wrong-on-small-noise).",
        "Not blind: the rubric exemplars were read before scoring (row E4d4-calibration-blind).",
        "Not checked: the 350-800 word limit of the report (no report exists in the repository); the browser self-assessment form and its JavaScript beyond page_smoke; the Grossman-Stiglitz paper (not cited by this page); Pyodide execution was taken from page_smoke's PASS, not a separate Pyodide run; the 'no network' constraint (not enforced by a test; not a fault); the Muth and Milgrom abstracts (the page attributes no statement to either).",
        "Spec question (not blocking): the reported point of the final bracket is unspecified (midpoint in Exemplar B; the 1e-10 root tolerance accepts either).",
        "Full repository gates were run only where listed (ruff, mypy, the four relevant pytest modules, check_pages, check_dag, check_projects, run_labs, run_graders, page_smoke for project, verify_refs live for E4, mutate_graders for E4).",
    ],
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants_killed": killed,
        "mutants": len(mutants),
    },
}
Path("ledgers/E4/E4-d.json").write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(fragment["summary"], verdict)
