"""Write the M7 project-slice fragment (round 1) to ledgers/M7/M7-d.json. Rows carry the evidence named in each row."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/M7/scripts/M7-d-r1/"
P = "course/modules/M/M7/project.html"
G = "course/modules/M/M7/grader/"


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or ""
    return r


rows = [
    row("m7d-lab1-numbers", "2.5-lab / 2.2-numbers", f"{P} lines 56-165; tests/labs/M7/lab-M7-project-1.py", "PASS",
        "Ran the twin under python -I -W error: output equals the embedded expected block (project.html 155-165). Re-derived exactly with Fractions (" + S + "check_lab.py): the KKT system at the active set {3} gives w=(9/11,2/11,0), nu=-21/1100, lower multiplier 9/1100, residuals 0 (stationarity, budget, complementary); objective -3/220 = -0.013636. Step-1 budget-only weights 54/65, 5/26, -3/130 recomputed by a separate Gauss solve. Interpretation (line 166) claims match."),
    row("m7d-lab2-completion", "2.5-lab", f"{P} lines 169-283; lab-M7-project-2.py", "PASS",
        "Twin output diffed line-for-line against twin 1 (identical). Completed blanks reproduce the Lab 1 expected block (lines 271-281). Hypothesis paragraph (171) names the three blanked lines correctly; the interpretation (282) is consistent with the code (residual subtracts lower multiplier after the gradient-plus-budget term)."),
    row("m7d-lab3-certificate", "2.5-lab / 2.4-math", f"{P} lines 369-438; lab-M7-project-3.py", "PASS",
        "Twin output equals lines 435-437. Independent exact recomputation (" + S + "check_lab.py): check B stationarity max 9/550 (= 2 x 9/1100, the change from flipping the multiplier), dual 9/1100; check C stationarity max 1/6250 (components 3/50000, -1/6250, -1/25000), budget 0. Hypotheses (371) and interpretation (438) agree with the numbers."),
    row("m7d-spec-residual-definitions", "2.4-math", f"{P} lines 303-318", "PASS",
        "Re-derived the Lagrangian of the linearized form: r^w = gamma*Sigma*w - mu + nu - lam_l + lam_u + eta + alpha - beta and r^t = kappa - alpha - beta. The test suite (test_project.py 84-102) and the reference (reference.py 164-170) use the same expressions; the reference's plus/minus split (kappa +/- net)/2 satisfies both. Turnover linearization (307) checked: |d|<=tau iff exists t with t>=+-d and sum t<=tau, proof directions correct."),
    row("m7d-spec-residual-wording", "2.9-prose", f"{P} line 311", "FAIL",
        "Line 311 says 'The four certificate fields are the largest absolute value of each residual, defined as follows'. The dual residual (line 315) is max(0, minus the smallest multiplier), and complementary slackness (316) is a max of |lambda g|, so 'the largest absolute value of each residual' does not describe all four fields.",
        "Replace the sentence with: 'The four certificate fields are defined as follows.'"),
    row("m7d-proof-uniqueness-midpoint", "2.4-proofs", f"{P} line 321 (Proposition, last sentence of proof)", "FAIL",
        "The uniqueness step says 'f((w+w')/2) < f(w) for w' != w, which contradicts minimality', but never states that the midpoint point is feasible. Feasibility holds because the constraints are affine in (w,t) and the feasible set is convex (average t with t'). The argument as written has this gap.",
        "Add one sentence: the midpoint of (w,t) and (w',t') is feasible because the constraints are affine in (w,t), so ((w+w')/2, (t+t')/2) is feasible."),
    row("m7d-proof-multiplier-existence", "2.4-math / hypotheses", f"{P} line 322 ('The instances the grader generates have one, because ...')", "FAIL",
        "The paragraph says the multiplier hypothesis holds for the generated instances because Sigma = (A'A+I)/1000 is positive definite. Positive definiteness gives strict convexity and uniqueness, not the existence of multipliers. Existence at the minimizer needs a different argument: the constraints are affine (so linearity gives the KKT multipliers at a minimizer) and the feasible set is bounded by the box. The stated justification does not support the claim.",
        "Justify existence from the affine constraints (linear constraint qualification) and the bounded box, and keep positive definiteness only for uniqueness."),
    row("m7d-spec-tolerance-1e-9", "2.4-spec / architect-a", f"{P} line 318 ('checked with a tolerance of 1e-9'); {G}test_project.py lines 175-186, 301-302 and the start-portfolio named conditions", "FAIL",
        "The page states the starting-portfolio tolerance is 1e-9. The suite only tests perturbations of 1e-6 (test_project.py: _start_sum_off, _upper_below_start, _lower_above_start, _cap_below_start). Variant with TOL = 1e-7 in the reference passes 99/99 on seeds 0-9 (" + S + "tolerance_variant.sh prints 'seeds failing of 10 = 0'). Mutant v03 (1e-5) is killed, so the test only enforces a tolerance between 1e-6 and 1e-5.",
        "Add invalid starting portfolios perturbed by 1e-10 and 1e-8 (must be refused) and valid ones at 1e-10 inside a bound, or state the enforced tolerance on the page."),
    row("m7d-spec-nan-inf-named", "2.4-spec / architect-a", f"{P} line 323 ('a value is NaN or infinite' named as ValueError); {G}test_project.py lines 533-548", "FAIL",
        "The page names 'a value is NaN or infinite' as a condition refused with ValueError. The suite tests non-finite values only for gamma and sigma[0][0] (test_non_finite_number_is_refused_with_value_error, four cases). Mutant v01 (ledgers/M7/mutants/v01_nan_in_mu_silently_zeroed.py: NaN in mu replaced by zero) SURVIVES seeds 0-49 (mutate_graders output: 'SURVIVED v01 ... -> None'). The page's claim is not enforced for mu, w0, lower, upper, sector_caps or turnover_limit.",
        "Parametrize the non-finite test over every numeric field (mu, w0, lower, upper, sector_caps, turnover_limit, sigma entries) and require ValueError, or narrow the page's list to the tested fields."),
    row("m7d-spec-boundary-claim", "2.4-spec / architect-a", f"{P} line 329; {G}test_project.py lines 476-514", "FAIL",
        "The page says each named ValueError condition is 'refused in its invalid form and accepted in its boundary form'. For 7 of the 13 entries in NAMED_CONDITIONS the 'boundary' is lambda case: None, i.e. the unmodified seed case: sigma-symmetric, sigma-positive-definite, gamma-positive-negative, start-sums-to-one, sector-label-in-range, every-sector-has-an-asset, one-entry-per-asset. Four named conditions (non-mapping, missing field, NaN/infinite, no assets) have no boundary test at all (test_a_non_mapping..., test_missing_field..., test_non_finite..., test_no_assets...).",
        "Give each named condition a true boundary (for example Sigma with smallest eigenvalue just above zero, a sector label K-1, a field present with an empty-but-valid value) or reword the page to 'accepted in a valid form' and list the four untested boundaries."),
    row("m7d-spec-named-list-coverage", "2.4-spec", f"{P} line 323 (the enumerated conditions); {G}test_project.py", "PASS",
        "Matched each enumerated condition to a test: mapping, missing field (9 fields), no assets, list one entry short (w0, lower, upper, sector, sigma, mu), symmetric, positive definite, gamma>0, turnover>=0, lower<=upper, start sum, start within bounds, start within sector cap, sector label range, sector without asset. Every enumerated condition has an invalid-case test (the NaN item is covered only for gamma and sigma; see m7d-spec-nan-inf-named)."),
    row("m7d-spec-test-count-and-seeds", "2.9-prose / 2.5", f"{P} line 329 ('It collects 99 checks, the same number for every seed')", "PASS",
        "pytest --collect-only -q over seeds 0..49 (QF_SEED=s, " + S + "run_alts.py workspaces): 50 of 50 seeds report 99 tests. run_graders --unit M7 --seeds 0-49: 'PASS (reference 50/50 seeds, slowest 0.8 s)'. Scratch workspace seed 0: 99 passed."),
    row("m7d-spec-hours", "2.9-structure / hours", f"{P} lines 33, 341-347; course/modules/M/M7/index.html line 29; lesson data-hours", "PASS",
        "Project table 2+3+10+6+7+5 = 33 = data-hours-project. Lesson data-hours 9,9,10,10,10,10,9,10 sum to 77 = data-hours-lessons; 77+33 = 110. No arithmetic inconsistency between hub split and lesson hours (pace not judged, per architect ruling)."),
    row("m7d-spec-other-claims", "2.9-prose", f"{P} lines 297-299, 324-327, 355, 362-363, 474", "PASS",
        "Output keys (lines 297-298) match allocate's contract in test_project.py 125-150. Purity and silence (324) tested by test_allocate_does_not_change_its_argument and test_allocate_prints_nothing_and_warns_nothing. QF_SEED command (362) matches test_project.py line 35. Payload decode (363) works: make_instance(seed)['payload'] is a JSON string. Browser claims (355 saved as you type: grader.js line 58-63 store.put on input; 474 nothing leaves the browser: page_smoke reports zero requests to hosts other than the local server)."),
    row("m7d-hand-cases", "2.4-math / architect-b", f"{G}test_project.py lines 218-246", "PASS",
        "Worked each of the five hand cases by hand: budget only (0.6, 0.4) from w = mu - nu with nu = -0.3; zero turnover (0.5, 0.5); single asset w=1; upper bound binding (0.7, 0.3) from unconstrained (0.35, 0.65) cut at 0.3; turnover binding (0.6, 0.4) from unconstrained (0.7, 0.3). Each matches the comment and the expected values."),
    row("m7d-comparators-and-edges", "2.4-math / architect-b", f"{G}test_project.py lines 372-379", "PASS",
        "Comparators are convex mixes of the solution and the starting portfolio, both feasible (constraints convex), so the test is a valid optimality check and the tolerance 1e-9 is above the rounding used by a correct solver (reference and five alternatives pass)."),
    row("m7d-grader-suite-over-constraint", "2.6-grader / architect-b", f"{G}test_project.py (whole suite); ledgers/M7/scripts/M7-d-r1/alt_core.py", "PASS",
        "Five verifier-written correct solvers run through the unchanged suite on seeds 0-49 (ledgers/M7/scripts/M7-d-r1/run_alts.out.txt): alt1 primal active-set, Bland drops, feasible start at w0; alt2 primal active-set, Dantzig drops; alt3 and alt4 penalty descent (rho 1e4 and 1e6) then exact polish, falling back to the alt1 route when the polish cycles; alt5 primal active-set with the working set built in reverse order. Result: 50/50 seeds pass for all five. CAVEAT: all five use the same validator (shared reference parser, the spec fixes it) and the same sign-form turnover multiplier mapping, so the suite's dependence on the auxiliary-variable multipliers is not separately tested; the fallback count in alt3/alt4 was not logged."),
    row("m7d-mutants-existing", "2.6-mutants", "ledgers/M7/mutants/m01..m10", "PASS",
        "tools/mutate_graders.py --unit M7 --seeds 0-49: m01..m10 all KILLED (see the mutate output in the verifier's log: m01 lab-boundary seed 5, m02 seed 0, m03 seed 0, m04 seed 0, m05 seed 0, m06 seed 0, m07 seed 0, m08 seed 0, m09 seed 0, m10 seed 0)."),
    row("m7d-mutants-new-v02-v04", "2.6-mutants", "ledgers/M7/mutants/v02_second_sector_cap_never_imposed.py, v03_start_tolerance_1e-5.py, v04_weights_rounded_to_six_places.py", "PASS",
        "Written by make_mutants.py (ledgers/M7/scripts/M7-d-r1/make_mutants.py) from the reference by exact substitution. All three KILLED on seeds 0-49: v02 by test_named_condition_boundary_is_accepted[start-within-sector-cap-boundary] (seed 1); v03 by test_named_condition_is_refused_with_value_error[start-sums-to-one-invalid] (seed 0); v04 by test_named_condition_boundary_is_accepted[lower-not-above-upper-boundary] (seed 7)."),
    row("m7d-mutant-v01-survivor", "2.6-mutants", "ledgers/M7/mutants/v01_nan_in_mu_silently_zeroed.py", "FAIL",
        "SURVIVED on seeds 0-49: a silent NaN-to-zero fallback in the vector parser passes the whole suite (mutate_graders output 'SURVIVED v01_nan_in_mu_silently_zeroed.py ... -> None'). The page names NaN as a refused ValueError condition (line 323), so the survivor is a suite gap that the page's statement exposes.",
        "Add NaN in mu (and the other numeric fields) to the non-finite test; re-run mutate_graders, expecting v01 KILLED."),
    row("m7d-grader-run-graders", "2.6-grader", "tools/run_graders.py --unit M7 --seeds 0-49", "PASS",
        "Output: 'run_graders M7: PASS (reference 50/50 seeds, slowest 0.8 s)'. Starter fails the suite per the tool's starter check (tool reports PASS). Scratch run of reference seed 0: 99 passed."),
    row("m7d-grader-mypy", "2.9-gates", "plans/M7-build-plan.md section 12 command: mypy tests/labs/M7 course/modules/M/M7/grader", "FAIL",
        "The plan's command reports 2 errors in course/modules/M/M7/grader/test_project.py: import-not-found for 'constrained_allocator' (line 29) and 'instance' (line 31). The repository's own mypy gate (strict, files=tools,tests in pyproject.toml) passes: 'Success: no issues found in 255 source files'. The grader directory is not in the gate, and the import targets are learner files that do not exist in the checkout.",
        "Either drop the grader from the mypy command or add a per-module override in pyproject.toml for the grader's two learner-side imports; not a builder change."),
    row("m7d-ruff", "2.9-gates", "tests/labs/M7; course/modules/M/M7/grader", "PASS",
        "ruff check: 'All checks passed!'; ruff format --check: '15 files already formatted'."),
    row("m7d-run-labs", "2.5-labs", "tools/run_labs.py --unit M7", "PASS", "run_labs M7: PASS (11/11). Also tests/test_run_labs.py and tests/test_page_smoke.py pass under pytest -k M7 (12 tests)."),
    row("m7d-check-projects-pages-dag", "2.9-gates / DAG", "tools/check_projects.py, check_pages.py, check_dag.py --unit M7", "PASS",
        "check_projects M7: PASS. check_pages M7: PASS (includes cards.json rules). check_dag M7: PASS. The envelope-theorem link in project.html stretch (line 450) is to M2, inside the unit's prerequisite closure. 'covariance' appears only in the no-link disclaimer (line 290); no other closure-outside concept is used by name in project.html."),
    row("m7d-page-smoke-project", "2.5-labs / browser", "tools/page_smoke.py --unit M7 --pages project", "PASS",
        "page_smoke modules/M/M7/project.html: PASS; in-browser grader 'All 99 tests pass on seed 430499647 (0.8 s)'; labs 0.0 s each; zero non-local requests."),
    row("m7d-lab-numbers-cards-subset", "2.2-numbers / 2.7-cards", "course/modules/M/M7/cards.json (numeric claims)", "PASS",
        "Verified against lab outputs and exact recomputation, with the lab that produces each figure: L01 cards c010, c012, c016 (lab 2573 of 3125 pass, 184 negative pairs, 552 = 3 x 184); L02 c026, c027, c028, c029, c030 (lab: Sigma rows, 177/55, 47/55 17/55 -9/55, 177/110, 36 of 36); L03 c046, c047, c049, c050 (recomputed, lab: residuals and grid minima); L04 c060 (7/300 recomputed), c062 (dual -1/2 recomputed), c063 (1331, 21, 27951, grid gap 0 recomputed), c064 (-199/300 recomputed), c067; L05 c084 (midpoint identity recomputed), c086 (x* 3/2 0, mu* 0 5/2, -9/4 recomputed), c087, c088, c089 (lab); L06 c108-c118 (lab numbers, all five gammas; c114 turnover 0.558860 recomputed from printed weights); L07 c130-c137 (lab tables and plan utilities: 400 gives u=130 the largest reward); L08 c151-c157 (lab output). Automated scan (" + S + "card_numbers.py): 9 cards flagged; each flagged fraction appears in the lesson LaTeX source (e.g. L04 199/150 and 49/300 at L04.html 292, 329, 372)."),
    row("m7d-cards-schema", "2.9-structure", "course/modules/M/M7/cards.json", "PASS",
        "159 cards, ids M7-c001..M7-c159 unique, lessons L01-L08 all present (16/19/20/19/24/24/21/18 spread), check_pages PASS. No duplicate fronts. Every card has front and back."),
    row("m7d-cards-grade-field", "2.3-grades / BUILDER_RULES 7", "course/modules/M/M7/cards.json (43 cards, e.g. M7-c001, M7-c002, M7-c013..c016, M7-c031..c033, M7-c037..c039, M7-c046..c047, M7-c051..c053, M7-c065, M7-c069..c071)", "FAIL",
        "43 of 159 cards have no 'grade' key. BUILDER_RULES section 7 and plan section 11 require a grade on every card (T for theorems and derived formulas). check_pages does not check the key when absent. Cards such as M7-c046 (a worked example result) and M7-c053 (a misconception with a numeric claim) carry no grade and no basis.",
        "Add grade T (theorem, definition-level, or derived by proof) or C with basis to all 43 cards."),
    row("m7d-cards-duplicates", "2.7-cards / duplicate scan", "course/modules/M/M7/cards.json: M7-c125 and M7-c138; M7-c149 and M7-c159", "FAIL",
        "Full scan by token Jaccard (threshold 0.55): M7-c125 ('State the backward recursion') and M7-c138 ('Key result: the value function satisfies the backward recursion') test the same fact; M7-c149 ('After n steps of value iteration, what is U^n?') and M7-c159 ('Key result: after n steps value iteration gives the exact value') test the same fact. BUILDER_RULES 7 asks for one fact per card.",
        "Remove M7-c138 and M7-c159, or reword them to test a different fact."),
    row("m7d-cards-vs-lesson-text", "2.7-cards", "course/modules/M/M7/cards.json (all 159) against L01-L08 prose", "UNVERIFIABLE",
        "Not completed: every card's front and back were read, and the numeric and attribution claims were verified (row m7d-lab-numbers-cards-subset), but the theorem-number references and the statements of hypotheses were not each checked against the lesson prose (for example Proposition 3.2 (d) in M7-c023, Remark 3.5 in M7-c107, Theorem 2.3 cross-references in L07 cards). Honest gap for this round.",
        "A full card-by-card read against each lesson (theorem numbers, hypotheses, 'Proved on the page' claims) is needed."),
    row("m7d-cards-cite-attribution", "2.1-citations", "course/modules/M/M7/cards.json M7-c045 and M7-c066 (cite boyd2004convex)", "PASS",
        "Both cards are grade C with cite boyd2004convex and the back says 'with no locator read', which is the honest state. check_pages verifies the key is in the registry. The page content was not checked against the book (no source read in this round)."),
]

mutants = [
    {"description": "Student error m01: the lower bounds are left out of the constraint rows, so short sales are allowed where the box forbids them.", "killed_by": "test_named_condition_boundary_is_accepted[lower-not-above-upper-boundary] (seed 5)"},
    {"description": "Student error m02: the turnover limit is measured from zero, not from the starting portfolio w0.", "killed_by": "test_complementary_slackness_holds (seed 0)"},
    {"description": "Student error m03: the active-set rule drops positive multipliers instead of negative ones, so dual feasibility is never enforced.", "killed_by": "test_wrong_type_is_refused_with_an_exception[mu-text] (seed 0)"},
    {"description": "Student error m04: the quadratic term is written as gamma w' Sigma w (factor-two convention error).", "killed_by": "test_stationarity_holds_in_the_weights (seed 0)"},
    {"description": "Student error m05: the answer for seed 0 is hard-coded and returned for every case.", "killed_by": "test_wrong_type_is_refused_with_an_exception[turnover_limit-text] (seed 0)"},
    {"description": "Student error m06: the turnover limit is halved when the sign constraints are built.", "killed_by": "test_complementary_slackness_holds (seed 0)"},
    {"description": "Student error m07: the sector caps are not imposed.", "killed_by": "test_named_condition_boundary_is_accepted[start-within-sector-cap-boundary] (seed 0)"},
    {"description": "Student error m08: the budget multiplier is reported with the wrong sign.", "killed_by": "test_stationarity_holds_in_the_weights (seed 0)"},
    {"description": "Student error m09: the expected returns enter the gradient with the wrong sign.", "killed_by": "test_certificate_residuals_are_within_tolerance (seed 0)"},
    {"description": "Student error m10: the plus and minus turnover multipliers are reported the other way round.", "killed_by": "test_stationarity_holds_in_the_weights (seed 0)"},
    {"description": "Silent fallback: a NaN expected return is replaced by zero instead of being refused with ValueError.", "killed_by": None, "survived": True},
    {"description": "Only the first sector cap is imposed in the solver; the second sector cap is never applied.", "killed_by": "test_named_condition_boundary_is_accepted[start-within-sector-cap-boundary] (seed 1)"},
    {"description": "Starting-portfolio checks use a tolerance of 1e-5, where the page states 1e-9.", "killed_by": "test_named_condition_is_refused_with_value_error[start-sums-to-one-invalid] (seed 0)"},
    {"description": "The returned weights are rounded to six decimals before the certificate is computed from them.", "killed_by": "test_named_condition_boundary_is_accepted[lower-not-above-upper-boundary] (seed 7)"},
]

frag = {
    "unit": "M7",
    "slice": "M7-d",
    "round": 1,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 1, slice M7-d: project.html, grader, project labs, cards.json; did not build M7)",
    "pin": "c11ae01 (detached checkout /tmp/verifyB1-M7-d; the brief named b4590f6, the task named c11ae01; c11ae01 is the checked-out pin used)",
    "base": "none",
    "checkout": "/tmp/verifyB1-M7-d",
    "scratch": "/tmp/M7-v/d/",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Round 1 of the M7 project slice. Commands run on the pinned checkout with its .venv: check_projects M7 PASS; run_graders M7 seeds 0-49 PASS (50/50); mutate_graders M7 seeds 0-49: 13 of 14 killed (v01 survived); run_labs M7 11/11; page_smoke project PASS; check_pages M7 PASS; check_dag M7 PASS; ruff check and format PASS; mypy repo gate PASS, grader mypy per the plan command FAIL (import-not-found); pytest -k M7 12 passed; pytest --collect-only 99 on seeds 0-49. Alternatives (ledgers/M7/scripts/M7-d-r1/alt_core.py) 5/5 routes pass 50/50 seeds. Not done: a full card-by-card read against lesson prose (row m7d-cards-vs-lesson-text); the sec.gov and external-source checks are not applicable (no registry claim beyond key existence). Ledger validator: no problems.",
    "summary": {
        "rows": len(rows),
        "pass": sum(r["status"] == "PASS" for r in rows),
        "fail": sum(r["status"] == "FAIL" for r in rows),
        "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows),
        "mutants": len(mutants),
        "mutants_survived": sum(1 for m in mutants if m.get("survived")),
    },
}
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, frag["summary"])
