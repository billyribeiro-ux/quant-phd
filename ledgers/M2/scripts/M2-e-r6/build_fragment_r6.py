"""Write the round-6 fragment ledgers/M2/M2-e.json from the mutation log and the row evidence recorded in this round.
Run from the checkout root: python ledgers/M2/scripts/M2-e-r6/build_fragment_r6.py"""
import json
import re
from pathlib import Path

ROOT = Path(".").resolve()
S = "ledgers/M2/scripts/M2-e-r6/"
PG = "course/modules/M/M2/project.html"
GR = "course/modules/M/M2/grader/"

rows = [
    # ---- autograder ----
    dict(id="e-auto-run", check="2.6-autograder-1", location=GR + "reference.py",
         status="PASS", evidence=f"tools/run_graders.py --unit M2 --seeds 0-49 -> 'run_graders M2: PASS (reference 50/50 seeds, slowest 0.2 s)' ({S}run_graders_r6.log); suite on reference.py 85 passed for seeds 0,1,7,49 (pytest -I, -W error)."),
    dict(id="e-auto-instances", check="2.6-autograder-2", location=GR + "instance.py",
         status="PASS", evidence=f"{S}sin_ratio_and_instances.py: 100 instances (seeds 0-49 and seed+7919) all satisfy the conditioning and range rules; 70 distinct x0 and 100 distinct face values; answers change with the seed."),
    dict(id="e-mut-existing", check="2.6-mutation-existing", location="ledgers/M2/mutants/ (81 pre-existing mutants)",
         status="PASS", evidence=f"tools/mutate_graders.py --unit M2 --seeds 0-9 ({S}mutate_r6.log): every pre-existing e/f/g/k/m/s/v/x mutant is KILLED; killed_by names are in the log."),
    dict(id="e-mut-new-killed", check="2.6-mutation-new", location="ledgers/M2/mutants/r6_03*, r6_04*, r6_05*",
         status="PASS", evidence=f"Own mutants written from reference.py by {S}make_mutants.py: r6_03 bond price discounts one year short (KILLED by test_price_is_the_half_even_rounding_of_the_exact_price), r6_04 ad_derivative returns value of a constant (KILLED by test_constant_function_has_zero_derivative), r6_05 mixed Hessian entries scaled by a quarter (KILLED by test_hessian_matches_the_analytic_hessian)."),
    dict(id="e-mut-r6_01", check="2.6-mutation-survivor", location=GR + "test_project.py:282-291 (test_large_positive_step_is_accepted); " + PG + ":222",
         status="FAIL", evidence=f"Mutant ledgers/M2/mutants/r6_01_fd_step_silently_capped_at_one.py (fd_derivative uses min(h, 1.0)) SURVIVES seeds 0-9 ({S}mutate_r6.log). project.html:222 states the forward estimate is (f(x+h)-f(x))/h for every h>0, and the mutant breaks that for h>1 (h=1,5,1e6 are tested only for finiteness). {S}probe_survivors.py: a value check at h=1 and h=5 KILLS it.",
         fix="In test_large_positive_step_is_accepted, assert that the returned value equals (f(x+h)-f(x))/h for the forward scheme (and the central quotient for the central scheme) at h=1.0, 5.0 and 1e6, with a relative tolerance of 1e-9 on the expected value."),
    dict(id="e-mut-r6_02", check="2.6-mutation-survivor", location=GR + "test_project.py:533-544 (test_hessian_positive_step_is_accepted); " + PG + ":223",
         status="FAIL", evidence=f"Mutant ledgers/M2/mutants/r6_02_hessian_step_silently_capped_at_a_thousandth.py (hessian_fd uses min(h, 1e-3)) SURVIVES seeds 0-9 ({S}mutate_r6.log). The Hessian test surface (quadratic in each variable) is reproduced exactly by central differences at every step, so the value tests cannot see the step. project.html:223 states the Hessian entries for every h>0. {S}probe_survivors.py: a diagonal-entry check at h=1.0 on a non-polynomial function KILLS it; the reference passes.",
         fix="In test_hessian_positive_step_is_accepted, compare the diagonal and mixed entries at h=1.0 and h=1e-3 with the formulas on project.html:223, evaluated on a non-polynomial test function (for example sin(u)cos(v)), with a tolerance that scales with h^2."),
    dict(id="e-alternatives", check="2.6-over-constraint", location=GR + "test_project.py",
         status="PASS", evidence=f"Five alternative correct modules (Richardson central + complex-step AD; exact-Fraction price and sensitivities; Hessian by gradient-of-central and fsum; Horner recursion with fsum; reordered mixed entries + Richardson central) each pass 50/50 seeds: {S}make_alts.py, {S}make_alts2.py, {S}run_alts.py."),
    dict(id="e-messages", check="2.6-messages", location=GR + "test_project.py",
         status="PASS", evidence="Every require()/pytest.fail message names the violated property and a hint; none prints an expected value (read all 788 lines)."),
    dict(id="e-pyodide-local", check="2.6-same-suite", location=GR + "test_project.py",
         status="PASS", evidence=f"tools/page_smoke.py --unit M2 --pages project: PASS, log line 'in-browser grader: All 85 tests pass'; local pytest (python -I, --assert=plain -W error) 85 passed."),
    dict(id="e-test-count", check="2.6-test-count", location=PG + ":211",
         status="PASS", evidence="pytest --collect-only -q (QF_SEED=0) on the reference copy: '85 tests collected'; project.html:211 says 85."),
    dict(id="e-valueerror-scope", check="2.6-exceptions", location=GR + "test_project.py; " + PG + ":225",
         status="PASS", evidence="ValueError is required only for the three named conditions (step not above zero, scheme not the name forward/central, yield at or below -1). Every other test is a plain acceptance or value check."),
    dict(id="e-scheme-types", check="2.6-spec-accuracy", location=PG + ":211",
         status="FAIL", evidence="project.html:211 says the scheme tests cover 'the scheme given as a string, a bool, a float or bytes'. The suite also tests None and the integer 1 (test_scheme_that_is_not_a_name_raises_value_error parametrize list, test_project.py:334). The list in the spec is incomplete.",
         fix="Change the phrase to: 'with the scheme given as None, an integer, a bool, a float, bytes, or a string other than forward or central'."),
    dict(id="e-hours", check="2.6-hours", location=PG + ":33, :239-245",
         status="FAIL", evidence="Declared 60 h. My component estimates for a competent student: rung 1 about 2 h; rung 2 about 1 h; 3a engine (five functions, dual numbers, tests) about 8-12 h (declared 22); 3a' edge cases about 2-3 h (declared 6); 3b note with derivations A1-A4, the sweep and report/run_report.py about 12-16 h (declared 14); 3c self-check about 2-3 h (declared 8). Total about 27-37 h, which is 38-55 % below 60 h, outside the 30 % rule.",
         fix="Re-estimate the components and the total so that the declared total is within 30 % of the estimate (the time-budget rows at project.html:239-245 and the eyebrow at :35 and :33 move together), or add deliverable scope that justifies the hours."),
    dict(id="e-hours-arith", check="2.6-hours-arithmetic", location=PG + ":239-245",
         status="PASS", evidence="4 + 6 + 22 + 6 + 14 + 8 = 60 = data-hours-project and the hub figure (check_projects.py --unit M2: PASS)."),
    dict(id="e-ladder", check="2.6-ladder", location=PG + ":40-48",
         status="PASS", evidence="tools/check_projects.py --unit M2: PASS. Rung 1 is Lab 1 (fully annotated), rung 2 is a completion lab graded instantly, rung 3 matches curriculum scope, rung 4 is open-ended (three stretch items)."),
    dict(id="e-spec-questions", check="2.6-spec-completeness", location=PG + ":199-212",
         status="PASS", evidence="Questions a competent student would ask: (1) the instance dictionary key names (face_cents, coupon_bps, maturity_years, yield_bps, x0, cubic, surface, point) are not listed on the page; they are visible in grader/instance.py, which the page links. (2) report/run_report.py line format is fixed by Lab 3's printed block; answered by the page. No blocking question remains."),
    dict(id="e-rubric-calibration", check="2.6-rubric-calibration", location=PG + ":412-527",
         status="PASS", evidence="Blind scoring against the rubric (project.html:400-404) with no annotations: Exemplar A 2,1,2,2,2 and Exemplar B 4,4,2,3,4, identical to the official scores (within one level on every criterion)."),
    dict(id="e-rubric-observable", check="2.6-rubric-observable", location=PG + ":400 (C1 level 4), :404 (C5 level 3)",
         status="FAIL", evidence="C1 level 4 requires the floating-point error 'proportional to 1/h with the reason' and gives no test for what counts as the reason. C5 level 3 requires units to be used 'consistently', which has no stated check. Both descriptors are vague.",
         fix="C1 level 4: replace 'with the reason' by 'and gives the reason as the spacing of doubles near the function value divided by the step'. C5 level 3: replace 'uses each unit consistently' by 'quotes each unit in the same form wherever the quantity appears'."),
    dict(id="e-rubric-adversarial", check="2.6-rubric-adversarial", location=PG + ":395-407",
         status="PASS", evidence="Not applicable: the project is not adversarial (no adversarial mode in curriculum/01-foundations.yaml for M2)."),
    dict(id="e-atlas-studio", check="2.6-atlas-studios", location="curriculum/meta.yaml; plans/M2-build-plan.md:22",
         status="PASS", evidence="Not applicable: M2 has no Atlas milestone (plan line 22; grep of meta.yaml atlas block finds no M2 entry) and is a module, not a studio."),
    # ---- labs ----
    dict(id="e-labs-run", check="2.5-labs-run", location="tests/labs/M2/lab-M2-project-{1,2,3}.py",
         status="PASS", evidence="tools/run_labs.py --unit M2: 'run_labs M2: PASS (27/27)'. Each twin run as python -I -W error exits 0 with empty stderr; stdout equals the page expected block (" + S + "lab_compare.py)."),
    dict(id="e-labs-page-twin", check="2.5-page-equals-twin", location=PG + ":58, :107 (Lab 1), :270, :350 (Lab 3)",
         status="PASS", evidence=f"{S}lab_compare.py: page code equals the twin except for the final newline (Labs 1 and 3, whitespace only). Lab 2 keeps its ___ blanks by design (tools/embed_labs.py:18); its twin is the solution, and run_labs checks the line count and the blanks."),
    dict(id="e-lab1-numbers", check="2.2-numbers-lab1", location=PG + ":57, :116",
         status="PASS", evidence="1081108.96 cents (1081108.9578), rounded 1081109, -8514667.40 (-8514667.3953), relative 1.8e-9 (1.56e-2/8514667.40), 83766485.12, relative 1.0e-7 (8.36/83766485.12), duration 7.88 (7.875864): all recomputed and matching the expected block."),
    dict(id="e-lab2-numbers", check="2.2-numbers-lab2", location=PG + ":121, :195",
         status="PASS", evidence="Expected block: second difference 8.400000, difference 5.11e-08 (< 1e-7 claim holds), AD derivative 3.760000, difference 4.44e-16 (< 1e-15 claim holds). Analytic values 8.4 and 3.76 recomputed from the cubic."),
    dict(id="e-lab3-numbers", check="2.2-numbers-lab3", location=PG + ":270, :377",
         status="PASS", evidence="Unrounded price 2721581.2909 -> 2721581; analytic -23407826.805475 (-23407826.81); smallest central error 7.111207e-04 at 1e-6; observed orders 0.984 and 2.000 (log10 ratios recomputed); kink +1, -1, 0; cancellation 8.78e-01 at 1e-12; the 'smaller central than forward at each of twelve steps' claim checked for all 12 rows."),
    dict(id="e-lab3-interpretation", check="2.2-interpretation-lab3", location=PG + ":377",
         status="PASS", evidence="'smallest at 1.490103 at step 1e-8' is the minimum of the forward column (checked); 'below 1e-6 the central error is larger than its minimum at every printed step' checked over 1e-7..1e-12."),
    dict(id="e-report-spec", check="2.6-report-from-spec", location=PG + ":207, :270",
         status="PASS", evidence=f"{S}report_from_spec.py builds report/run_report.py from Lab 3 with the stated replacements (difference -> fd_derivative, exact -> sensitivities(instance)['dprice_dy']) and it prints the Lab 3 expected block exactly (exit 0, -W error)."),
    dict(id="e-exemplar-numbers", check="2.2-numbers-exemplars", location=PG + ":418, :429, :454, :470, :481, :494, :507",
         status="PASS", evidence="Exemplar numbers recomputed: 2721581; -23407827; 7.111207e-04 at 1e-6; 3e-11 relative (7.111e-4/2.3408e7); float spacing 2^-31 = 4.66e-10; 1/(2h) = 5e11 at 1e-12; ulp near 1e8 is 2^-26 = 1.49e-8; 2h = 2e-8 is about 1.3 spacings; errors 1.33e-01 and 5.32e-05 match the expected block."),
    dict(id="e-sin-ratio", check="2.4-math-sin-ratio", location=PG + ":226",
         status="PASS", evidence=f"{S}sin_ratio_and_instances.py: plain central quotient ratio for sin at x0 over 100 instances lies in [3.9999842, 3.9999851], as project.html:226 states."),
    dict(id="e-formulas", check="2.4-math-conventions", location=PG + ":214-227",
         status="PASS", evidence="P'(y) and P''(y) formulas, named ratios, forward/central quotients, Hessian off-diagonal formula with 4h^2, half-to-even rule, ValueError conditions and the tolerance list (each tolerance matches the test code, test_project.py lines 147-660) all checked by the suite and by alternatives."),
    dict(id="e-cards-correct", check="2.7-cards-correct", location="course/modules/M/M2/cards.json (377 cards)",
         status="PASS", evidence=f"Every card read against its lesson's statement, proof, worked example, lab output or key-results row ({S}extract_lesson_text.py, {S}cards_of.py). Numeric cards recomputed where they carry a number (for example M2-c126 0.15933400; M2-c172 9.28130671 = H_16384 - 1; M2-c341/342/343 scaled from the project bond; M2-c224-c231 closed forms; M2-c111 bound 5.625, 8.4375). No card contradicts its lesson."),
    dict(id="e-cards-atomic", check="2.7-cards-atomic", location="course/modules/M/M2/cards.json: M2-c194, M2-c341, M2-c344, M2-c345, M2-c346, M2-c369, M2-c093",
         status="FAIL", evidence="Cards must test one fact (BUILDER_RULES 7). These cards test two or more facts: c194 (smallest forward error and the growth below it), c341 (unrounded and integer price), c344 (price at +0.01 and at -0.01), c345 (first- and second-order errors), c346 (first- and second-order ratios), c369 (smallest forward and smallest central error). c093 tests a count of checks (27 checks), which is trivia.",
         fix="Split each listed card into one card per fact, and replace c093 by a card on the identity the lab checks (the closed form equals the recursion at x = 3/10)."),
    dict(id="e-cards-dup", check="2.7-cards-duplicates", location="course/modules/M/M2/cards.json",
         status="PASS", evidence=f"{S}cards_check.py: 377 unique ids, no duplicate fronts; token-overlap scan (" + "threshold 0.45) found only distinct facts (for example forward vs central quotient cards)."),
    dict(id="e-cards-numbers", check="2.7-cards-numbers", location="course/modules/M/M2/cards.json",
         status="PASS", evidence=f"{S}cards_check.py: every number on every card occurs in its own lesson text (0 missing)."),
    dict(id="e-cards-labels", check="2.7-cards-labels", location="course/modules/M/M2/cards.json",
         status="PASS", evidence=f"{S}cards_labels.py: 489 cited Proposition/Theorem/Lemma/Corollary/Example/Remark/Definition/Assumption/Problem labels checked against the own lesson; no card cites a label its lesson lacks. 66 'Section' or 'Misconception N' references point at unnumbered headings, not at missing items."),
    dict(id="e-cards-grades", check="2.7-cards-grades", location="course/modules/M/M2/cards.json",
         status="PASS", evidence="Cards with grade C carry a basis naming the lab or closed forms (all 'C' cards have basis); grade T cards state proved results whose proofs are on the lesson page; 58 cards have no grade and are definitions or misconceptions."),
    dict(id="e-data-figures", check="2.8-data-figures", location=PG,
         status="PASS", evidence="No data-files attribute and no SVG on project.html (grep); all labs use SIMULATED data with the SIMULATED label in code docstrings and hypotheses."),
    dict(id="e-structure", check="2.9-structure", location=PG,
         status="PASS", evidence="tools/check_pages.py --unit M2: PASS; tools/check_projects.py --unit M2: PASS; tools/page_smoke.py --pages project: zero console errors, math rendered, no external requests (no http(s) URLs in project.html)."),
    dict(id="e-banned-phrases", check="2.9-banned-phrases", location="course/modules/M/M2/*.html, cards.json",
         status="PASS", evidence="BUILDER_RULES 1.3-1.4 scan: no TODO/TBD/lorem/'for brevity'/'details omitted'/'beyond the scope'/'it is important to note'/'obviously'/'clearly' hits; 'About ...' and 'about ...' hits are computed values (1.8e-9, 3e-11) or the word in ordinary use."),
    dict(id="e-dag", check="2.9-dag", location=PG,
         status="PASS", evidence="tools/check_dag.py --unit M2: PASS. The project uses Hessian (L19), finite-difference derivative (L13), automatic differentiation (L14), Taylor's theorem (L08) and the derivative (L04), each defined in a prerequisite lesson. 'Duration' and 'convexity' are previewed in prose only, as plans/M2-build-plan.md Q8 allows."),
    dict(id="e-notation", check="2.4-notation", location=PG,
         status="PASS", evidence="notation/notation.json holds 10 symbols (T, Phi, gamma_3, gamma_4, R^ast, R^e*, R_f, Q, ...). No M2 page or project uses any of them with another meaning (grep)."),
    dict(id="e-citations", check="2.1-citations", location=PG + ":547-551",
         status="PASS", evidence="tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'. tools/verify_refs.py --unit M2 (live): '2 of 560 entries, 0 problems' (" + S + "verify_refs_M2_live.log). The reading list cites spivak2008calculus and hubbard2015vector, and the page attributes no statement to them."),
    dict(id="e-hours-declared-spec", check="2.6-spec-hours-plan", location=PG + ":35",
         status="PASS", evidence="60 hours on the eyebrow and in data-hours-project match curriculum/01-foundations.yaml M2 project entry (check_projects PASS)."),
]

FRAG = {
    "unit": "M2",
    "slice": "e",
    "round": 6,
    "verifier": "independent verifier (Haiku 5.5), slice e",
    "pin": "44f1eb6a417ce687a9b88c7ee917e72566b29892",
    "base": "no round-5 fragment exists in this checkout; /Users/billyribeiro/.fanout/frags/B-M2-e.round5.json is absent",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB6-M2-e",
    "scratch": "/tmp/m2e_r6",
    "verified_at": "2026-10-29T00:56:02Z",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Row ids are new in round 6 (no round-5 fragment was available to keep ids from). "
        "Lab 2 page code keeps its blanks by design (completion lab). "
        "Lessons L18-L22 problem-set tails were not read in full; no card cites them except by labels that exist. "
        "Live citation run done (2 entries). Not run: browser run of the grader panel outside Pyodide page_smoke; no Chrome session."
    ),
    "summary": "",
}

mut_rows = []
for line in (ROOT / S / "mutate_r6.log").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mut_rows.append({
        "name": name,
        "description": desc,
        "killed_by": None if status == "SURVIVED" or killed == "None" else killed,
    })
FRAG["mutants"] = mut_rows
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
FRAG["summary"] = (f"rows={len(rows)} pass={n_pass} fail={n_fail} unverifiable=0; mutants {len(mut_rows) - sum(1 for m in mut_rows if m['killed_by'] is None)}/{len(mut_rows)} killed")
FRAG["rows"] = rows
(ROOT / "ledgers/M2/M2-e.json").write_text(json.dumps(FRAG, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote ledgers/M2/M2-e.json:", FRAG["summary"])
