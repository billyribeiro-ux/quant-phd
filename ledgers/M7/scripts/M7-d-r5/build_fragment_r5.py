"""Build ledgers/M7/M7-d.json (round 5, slice M7-d) from the round-4 rows plus the round-5 delta. Usage: python3 build_fragment_r5.py <checkout-root>"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
MUT = root / "ledgers/M7/scripts/M7-d-r5/mutate_graders_M7_seeds0-49_r5.txt"
PRIOR = json.loads(Path("/tmp/fanout-frags/B-M7-d.round4.json").read_text(encoding="utf-8"))
CARRY = "Carried from round 4 (project.html, grader and cards byte-identical in the cited lines since the previous pin 2657ab5): "

overrides: dict[str, dict[str, str]] = {
    "m7d-lab1-numbers": {"status": "PASS", "evidence": "Re-verified on pin 09b8751. Lab 1 code (project.html, the block at line 56 onward) run with python -I -W error via " + "ledgers/M7/scripts/M7-d-r5/project_labs_r5.py: MATCH with the expected block (line 155 area). Hypothesis line 55 (gamma equal to 2; returns 5.0%, 3.0%, -2.0%) matches MU and GAMMA in the code. Step 7 comment ('the value the certificate of the project describes') is loose, but the certificate is the optimality check that certifies this value, so it is not false. Re-derived this round in exact arithmetic: stationarity residuals 0, 0, 0, budget gap 0, objective -3/220 at w=(9/11, 2/11, 0), nu=-21/1100, lambda3=9/1100."},
    "m7d-lab2-completion": {"status": "PASS", "evidence": "Re-verified: the three blanks (residual, signs, dual_feasible) filled with the expressions the hypothesis paragraph (line 171) describes give an output identical to Lab 1 and to the expected block (ledgers/M7/scripts/M7-d-r5/project_labs_r5.py: MATCH)."},
    "m7d-lab3-certificate": {"status": "PASS", "evidence": "Re-verified on pin 09b8751 (line 371 hypothesis changed to 'primal residual'): lab run MATCH; checks A, B, C re-derived by hand: B: asset-3 stationarity = 8/1100 + 22/1100 - 21/1100 + 9/1100 = 18/1100 = 9/550 and dual residual 9/1100; C (re-run this round, exact): stationarity residuals 3/50000, -1/6250, -1/25000, so the max is 1/6250; primal 0 in all three; complementary 0. Interpretation sentences (lines 438) match these values. Docstring line 376-377 'a correct answer has all four residuals at zero' presumes that the answer comes with its KKT multipliers; noted, not a false claim."},
    "m7d-spec-residual-definitions": {"status": "PASS", "evidence": CARRY + "project.html lines 303-318 and grader/test_project.py lines 84-125 (stationarity, recomputed_certificate). Grader residual formula matches page line 310 (rw includes +plus -minus, rt = kappa - plus - minus). Verified by the reference passing run_graders 50/50 and the mutant z06/w02 kills."},
    "m7d-proof-differentiability": {"status": "FAIL", "evidence": "project.html line 322 (the cited subject is byte-identical to round 4, so this is a re-derivation, not a carry): 'Hypotheses: f is differentiable and convex, and strictly convex in w because Sigma is positive definite'. Strict convexity of f(w) = (gamma/2) w'Sigma w - mu'w needs gamma > 0 as well as Sigma positive definite: with gamma = 0 f is linear and the uniqueness conclusion of the proposition fails (f = -mu'w is constant on a segment when mu is orthogonal to its direction). Every valid case has gamma > 0 (named condition, line 323), so the instance claim is true, but the hypothesis list the page gives for the proposition omits gamma > 0. Re-derived the proof on lines 320-321 itself: the sufficiency and midpoint steps are valid under the stated hypotheses.", "fix": "On project.html line 322 write 'strictly convex in w because gamma is positive and Sigma is positive definite' (no grader change)."},
    "m7d-proof-multiplier-existence": {"status": "PASS", "evidence": "Re-verified: line 322 sentence 'Existence of multipliers for every generated instance is not proved on this page' is a scope statement; run_graders M7 seeds 0-49: reference 50/50 (ledger run output). Statement limited to seeds 0 to 49 is correct."},
    "m7d-spec-nan-inf-named": {"status": "PASS", "evidence": "Re-verified: line 323 lists 'a value is NaN or infinite'; the grader test_non_finite_value_is_refused_with_value_error runs 8 fields x 3 values (NON_FINITE_FIELDS, lines 723-731), all ValueError; collected in the 156 count."},
    "m7d-spec-named-message": {"status": "PASS", "evidence": "Re-verified: line 323 'A named condition is refused with ValueError, and the refusal carries a message.' Tests: test_named_condition_is_refused_with_value_error uses pytest.raises(ValueError, match=r'\\S') (lines 599-608); the other invalid inputs use pytest.raises(Exception, match=r'\\S') (lines 797-813), matching 'an exception that carries a message'. The naming requirement was withdrawn (plan section 7.2, round-4 fixer decision) and no test enforces naming."},
    "m7d-spec-named-list-coverage": {"status": "PASS", "evidence": "Re-verified: each of the 13 named conditions on line 323 has a refused test (NAMED_CONDITIONS lines 553-567) and a boundary test (same list, '-boundary' ids). New tests added this round: gamma-positive-just-below-zero, turnover-limit-just-below-zero, lower-over-upper-by-1e-12, lower-over-upper-last-asset, sigma-symmetric-last-pair, sector-label-out-of-range-last-asset, start-within-upper-last-asset, start-within-sector-cap-last-sector (OTHER_SIDE_REFUSED lines 670-692), all collected and killed-mutant tested (y01-y10)."},
    "m7d-spec-boundary-claim": {"status": "PASS", "evidence": "Re-verified: line 323 'the valid form sits on the limit or just inside it, and for the starting portfolio the tolerance is 1e-9'. Boundary tests exist for each named condition (start-within-upper-boundary, start-within-lower-boundary, start-within-sector-cap-boundary, start-sums-to-one-boundary at 5e-10, lines 465-496) and for the exact values (EXACT_BOUNDARIES, lines 577-596, plus gamma-just-inside-zero). Mutants z01, z02, s03, x01 killed through these tests."},
    "m7d-spec-test-count-and-seeds": {"status": "PASS", "evidence": "Re-verified on pin 09b8751: pytest --collect-only on the reference workspace gives 156 for every QF_SEED in 0..49 (computed count: 50 x '156 tests collected'). Page line 329 states 'collects 156 checks, the same number for every seed'. The round-4 value 147 is superseded."},
    "m7d-spec-hours": {"status": "PASS", "evidence": "Arithmetic only (architect ruling). Project table lines 341-347: 2+3+10+6+7+5 = 33, equal to data-hours-project 33 (line 33) and the eyebrow (line 35). Lessons data-hours: L01 9, L02 9, L03 10, L04 10, L05 10, L06 10, L07 9, L08 10 = 77; 77+33 = 110, matching the hub split statement (index.html line 141). Lesson hours changed nowhere in this delta."},
    "m7d-spec-other-claims": {"status": "PASS", "evidence": "Re-verified: 'in this browser a moment after you stop typing' (line 355) is unchanged and matches the 400 ms debounce recorded in round 4 (course/assets/js/grader.js line 61, unchanged in this delta). Line 324 purity statement is covered by test_allocate_does_not_change_its_argument, test_allocate_prints_nothing_and_warns_nothing and test_the_same_case_gives_the_same_answer (lines 837-856). Line 297-299 unchanged."},
    "m7d-hand-cases": {"status": "PASS", "evidence": CARRY + "grader/test_project.py lines 218-246. This round I re-derived the five worked answers by hand: budget only (0.6,0.4) from w=mu+0.3; zero turnover (0.5,0.5); single asset (1.0); upper bound binding (0.7,0.3) from unconstrained (0.35,0.65); turnover binding (0.6,0.4), since the 1-D objective 2w1-1.4 over w1 in [0.4,0.6] is minimised at 0.6."},
    "m7d-hand-case-tolerance": {"status": "PASS", "evidence": CARRY + "grader/test_project.py lines 394-395 (TOL 1e-8 on the worked weights)."},
    "m7d-comparators-and-edges": {"status": "PASS", "evidence": CARRY + "grader/test_project.py lines 372-379 (three comparators y_weight 0, 0.25, 0.75)."},
    "m7d-grader-suite-over-constraint": {"status": "PASS", "evidence": "Ran ledgers/M7/scripts/M7-d-r3/run_alts_r3.py on pin 09b8751 (output ledgers/M7/scripts/M7-d-r5/run_alts_r5_output.txt): core_route1 to core_route5 50/50; bland 50/50; exact_order 50/50; first_order 50/50. float_arithmetic 0/50: its own RuntimeError 'the working set lost independence' is raised on valid seed 2 and on gamma 1e-6 (diagnosed in /tmp/M7-v/d/r5/diag). The grader never refuses a valid output in that run; the failure is the alternative's absolute rank cutoff, so it is not counted as over-constraint evidence. The alternatives cover the rounds' seed range 0 to 49."},
    "m7d-mutants-existing": {"status": "PASS", "evidence": "tools/mutate_graders.py --unit M7 --seeds 0-49 (ledgers/M7/scripts/M7-d-r5/mutate_graders_M7_seeds0-49_r5.txt): every f01-f10, m01-m24, s01-s10 mutant KILLED."},
    "m7d-mutants-new-v01-v04": {"status": "PASS", "evidence": "KILLED on seed 0 or 7 (mutate_graders_M7_seeds0-49_r5.txt): v01 by test_non_finite_value_is_refused_with_value_error[mu-nan]; v02 by test_named_condition_boundary_is_accepted[start-within-sector-cap-boundary] (seed 1); v03 by test_named_condition_is_refused_with_value_error[start-sums-to-one-invalid]; v04 by test_named_condition_boundary_is_accepted[lower-not-above-upper-boundary] (seed 7)."},
    "m7d-mutants-new-v06": {"status": "PASS", "evidence": "v06 was removed from ledgers/M7/mutants/ by the builder (round-4 fixer decision, plans/M7-build-plan.md lines 191-195). The page wording was changed to match the tests: project.html line 323 now says 'the refusal carries a message' and grader tests read 'the refusal must carry a message' (test_project.py lines 805, 813, 822, 829). Under ruling (a) the naming requirement is not enforced by the tests, so a mutant whose messages do not name the condition is a correct solution under the page; removing it is the consistent fix, not a weakened grader."},
    "m7d-mutants-new-w01-w07": {"status": "PASS", "evidence": "All KILLED (mutate_graders_M7_seeds0-49_r5.txt). w05 absent (row m7d-mutants-w05-equivalent)."},
    "m7d-mutants-w05-equivalent": {"status": "PASS", "evidence": CARRY + "ledgers/M7/scripts/M7-d-r3/make_mutants_r3.py (w05 entry removed), byte-identical since the previous pin."},
    "m7d-mutate-tool-verdict": {"status": "FAIL", "evidence": "tools/mutate_graders.py --unit M7 --seeds 0-49 final line: 'mutate_graders M7: FAIL (77/78 killed)'. The only survivor is z05_certificate_hard_coded_to_zero (row m7d-mutants-new-z05). Exit status 1.", "fix": "Fix row m7d-mutants-new-z05."},
    "m7d-grader-run-graders": {"status": "PASS", "evidence": "tools/run_graders.py --unit M7 --seeds 0-49 on pin 09b8751: 'run_graders M7: PASS (reference 50/50 seeds, slowest 1.3 s)'."},
    "m7d-grader-mypy": {"status": "PASS", "evidence": "plans/M7-build-plan.md section 12 command re-run on pin 09b8751: 'Success: no issues found in 14 source files'."},
    "m7d-ruff": {"status": "PASS", "evidence": "ruff check course/modules/M/M7/grader tests/labs/M7: 'All checks passed!'; ruff format --check: '15 files already formatted' (run this round)."},
    "m7d-run-labs": {"status": "PASS", "evidence": "tools/run_labs.py --unit M7 on pin 09b8751: 'run_labs M7: PASS (11/11)'. Project twins 1 to 3 also re-run as described in m7d-lab1-numbers."},
    "m7d-check-projects-pages-dag": {"status": "PASS", "evidence": "tools/check_projects.py, tools/check_pages.py, tools/check_dag.py --unit M7 re-run: check_projects M7: PASS; check_pages M7: PASS; check_dag M7: PASS."},
    "m7d-page-smoke-project": {"status": "PASS", "evidence": "tools/page_smoke.py --unit M7 --pages project re-run: 'page_smoke modules/M/M7/project.html: PASS'; in-browser grader 'All 156 tests pass on seed 1489034551 (1.0 s)'."},
    "m7d-pytest-M7": {"status": "PASS", "evidence": ".venv/bin/python -m pytest -q -k M7 tests/test_labs.py re-run: 11 passed."},
    "m7d-lab-numbers-cards-subset": {"status": "PASS", "evidence": "C-grade cards changed this round: M7-c089 (1089 grid points, 33 values per coordinate, one passing set {2}, grid_points_below_candidate 0: lab output lines 386-393), M7-c093 (lambda = (-36/19, 11/19): L05 interpretation of Lab 1 Part A output), M7-c110 (0.113798, 0.123809, -0.051893, weights: L06 lab output 'equality 1 ...'). All three match the printed output. The other C cards are byte-identical to round 4 (carried)."},
    "m7d-cards-schema": {"status": "PASS", "evidence": "course/modules/M/M7/cards.json re-read: 143 cards, each with id, lesson, front, back, grade; the 37 C cards carry basis."},
    "m7d-cards-grade-field": {"status": "PASS", "evidence": "Grades: T 106, C 37 (python count this round)."},
    "m7d-cards-duplicates": {"status": "PASS", "evidence": "143 unique ids; no duplicate lowercased normalized fronts (python scan this round)."},
    "m7d-cards-basis-stale-lab": {"status": "PASS", "evidence": "M7-c063 basis 'Lab 1 (exact arithmetic on the listed grids)' still names the L04 Lab 1; the lab's only change is a docstring word (tests/labs/M7/lab-M7-L04-1.py line 11), so the basis is unaffected."},
    "m7d-cards-cite-attribution": {"status": "PASS", "evidence": "Changed cards cite only items defined in the lesson text: Theorem 2.3, Lemma 1.3, Definition 3.3, Theorem 3.1, Remark 3.2, Remark 2.4, Example 3.6 (L05 lines 115-175); Proposition 2.1 (L04 line 106; L06 line 90); Remark 2.2 (L06 line 102). No bibliographic attribution introduced."},
    "m7d-cards-changed-r4": {"status": "PASS", "evidence": "Round-5 changed cards (python diff against 2657ab5): M7-c061, c069 (L04), c079, c083, c086, c089, c092, c093 (L05), c102, c110 (L06). Each card statement was read against the current lesson text: c061 vs L04 Prop 2.1 (lines 106-107) incl. hypotheses; c069 vs L04 lines 247 and 287 (-199/300, 49/300); c079 vs L05 Theorem 2.3 (line 115); c083 vs L05 Definition 3.3 (line 156); c086 and Example 3.6 (line 176) with the arithmetic re-derived; c089 vs Lab 1 Part B output; c092 vs Theorem 3.1 (line 141) and Remark 3.2 (line 151); c093 vs Remark 2.4 text (line 420); c102 vs Proposition 2.1 and Remark 2.2 (L06 lines 90-102); c110 vs Lab 1 Part A output. Notation x-hat and x-bar are the lesson's own."},
    "m7d-cards-c092-hypothesis-dropped": {"status": "PASS", "evidence": "M7-c092 back now states 'For a convex QP (Q symmetric positive semidefinite), Theorem 3.1 needs the inequality multipliers to be non-negative and complementary slackness'. L05 Theorem 3.1 (line 141) states Q PSD, mu-bar >= 0 and mu-bar_i (G x-bar - h)_i = 0 for every i. The round-4 FAIL is resolved."},
    "m7d-cards-vs-lesson-text": {"status": "UNVERIFIABLE", "evidence": "Partly re-verified this round: every card whose text changed (10 cards, row m7d-cards-changed-r4) was read against its lesson; every card number of the 143 cards appears in its lesson text after TeX fraction normalization (python scan this round; the only literal misses were TeX forms, e.g. -\\tfrac18 in L03 line 123, and 2/3 in L02 line 346). NOT done: a line-by-line semantic read of all 143 cards against the full text of the eight lesson pages (L01 to L08), so the rest of the cards are not verified for agreement with the current lesson text.", "fix": "Run a full card-by-card read of cards.json against L01 to L08 (each card statement vs its cited definition, theorem and lab output) and record each card id."},
    "m7d-registry-and-citations": {"status": "PASS", "evidence": CARRY + "project.html lines 459-460 (data-cite boyd2004convex, stokey1989recursive) and references/references.json (not in the delta). No external source was read this round."},
    "m7d-ruling-hours-pace": {"status": "PASS", "evidence": "Architect ruling: hours are design targets, not graded on pace. Only the arithmetic is checked (row m7d-spec-hours)."},
}

rows: list[dict[str, str]] = []
for row in PRIOR["rows"]:
    new = dict(row)
    if row["id"] in overrides:
        new.update(overrides[row["id"]])
    elif row["status"] == "PASS":
        new["evidence"] = CARRY + row["evidence"].split("): ", 1)[-1] if "): " in row["evidence"] else CARRY + row["evidence"]
    rows.append(new)

new_rows = [
    {"id": "m7d-mutants-new-z01-z04-z06-z08", "check": "2.5 grader mutants: verifier student-error mutants z01 to z04, z06 to z08 (round 5)", "location": "ledgers/M7/mutants/z01_start_box_checked_without_tolerance.py; z02_start_sector_cap_checked_without_tolerance.py; z03_allocate_prints_a_trace.py; z04_allocate_marks_its_argument.py; z06_sector_multiplier_sign_flipped_in_stationarity.py; z07_weights_returned_in_reverse_order.py; z08_turnover_measured_from_uniform_portfolio.py; written by ledgers/M7/scripts/M7-d-r5/make_verifier_mutants_r5.py", "status": "PASS", "evidence": "All KILLED on seeds 0-49: z01 by test_named_condition_boundary_is_accepted[start-within-upper-boundary] and [start-within-lower-boundary] (seed 0, re-run this round), and the mutate tool's first kill is start-sums-to-one-boundary; z02 by test_named_condition_boundary_is_accepted[start-within-sector-cap-boundary] (seed 0); z03 by test_allocate_prints_nothing_and_warns_nothing; z04 by test_allocate_does_not_change_its_argument (verified directly, seed 0: 'test_allocate_does_not_change_its_argument FAILED'); z06 by test_certificate_agrees_with_the_recomputed_residuals (seed 2); z07 by test_hand_case_matches_its_worked_answer[budget...]; z08 by test_complementary_slackness_holds (seed 0). Output: mutate_graders_M7_seeds0-49_r5.txt."},
    {"id": "m7d-mutants-new-z05", "check": "2.5 grader mutants: z05 certificate typed in as zero survives", "location": "ledgers/M7/mutants/z05_certificate_hard_coded_to_zero.py; course/modules/M/M7/project.html line 298 and line 318; grader/test_project.py lines 356-362", "status": "FAIL", "evidence": "SURVIVED on seeds 0-49: the mutant returns the reference answer with all four certificate fields typed as 0.0, and no test fails. The suite cannot tell it apart, because on every answer the other checks accept the four recomputed residuals are at most 1e-8 and the agreement test (1e-9) compares with the recomputed values, which are exactly zero for the reference. The page states the behaviour the mutant violates: project.html line 298, 'each a number that you compute from your weights and multipliers by the definitions below'. Under Architect ruling (a) a requirement the tests do not enforce must not be claimed; the suite enforces agreement with the recomputed residuals, not computation.", "fix": "Either reword project.html line 298 to the claim the suite enforces ('each must agree, to 1e-9, with the value the suite recomputes from your weights and multipliers'), or add a test that fails a certificate that is not a function of the output (no grader change is made here)."},
    {"id": "m7d-grader-delta-new-tests", "check": "2.7 / 2.5 grader: new round-5 tests trace to named conditions of the page and do not over-constrain", "location": "course/modules/M/M7/grader/test_project.py lines 570-692; course/modules/M/M7/project.html line 323", "status": "PASS", "evidence": "New tests: gamma 1e-9 accepted (valid form just inside zero); gamma -1e-12 and turnover -1e-12 refused ('is not positive', 'the turnover limit is negative'); lower bound one-trillionth above upper refused ('a lower bound lies above its upper bound', no tolerance is stated for bound order); asymmetric last pair refused; sector label K refused; start 2e-9 above a bound and 2e-9 below a cap refused (outside the 1e-9 tolerance). Each is a condition the page names; the valid forms and boundary forms are accepted. Reference passes all 156 checks on seeds 0-49 (run_graders); alternatives core_route1-5, bland, exact_order, first_order pass 50/50 with them."},
    {"id": "m7d-dag-envelope-link", "check": "DAG: concept links in project.html outside the unit's prerequisite closure", "location": "course/modules/M/M7/project.html line 450; plans/M7-build-plan.md lines 62-65 and 178", "status": "PASS", "evidence": "The only concept link is envelope-theorem (concepts.html#envelope-theorem, defined in M2 L22). M2 is in M7's prerequisite closure (plan section 2, M2 row), and the plan's architect decision (line 178) marks it usable. check_dag M7 PASS."},
    {"id": "m7d-lab-hypothesis-delta-r5", "check": "2.5 / 2.2 round-5 prose changes in project labs (hypothesis lines 55, 371; spec line 293, 329)", "location": "course/modules/M/M7/project.html lines 55, 293, 329, 371", "status": "PASS", "evidence": "Line 55: 'gamma, the risk aversion, equal to 2' matches GAMMA = Fraction(2). Line 293: 'No currency amount appears on this page' is true of the page (no currency in M7 text checked by grep). Line 329: 156 verified. Line 371: 'primal residual should stay zero' matches Check C output primal 0."},
]

fragment = {
    "unit": "M7",
    "slice": "M7-d",
    "round": 5,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 5, slice M7-d: project.html, grader, project labs, cards.json; did not build M7)",
    "pin": "09b8751 (detached checkout /tmp/verifyB5-M7-d; previous round pin 2657ab5; delta 2657ab5..09b8751 covers project.html, grader/test_project.py, cards.json, L04, L05, L06 and their M7 lab twins, plans/M7-build-plan.md section 7.2, the M7 mutants folder)",
    "base": "2657ab5",
    "checkout": "/tmp/verifyB5-M7-d",
    "scratch": "/tmp/M7-v/d/r5/",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows + new_rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Round-5 delta verification. Commands run on the pin: check_projects, check_pages, check_dag, run_labs (11/11) M7 PASS; run_graders M7 seeds 0-49 PASS; pytest --collect-only 156 for seeds 0-49; page_smoke project PASS; pytest -k M7 11 passed; ruff check and format PASS; plan's mypy strict command PASS (14 files); mutate_graders M7 seeds 0-49 77/78 killed (z05 survives); run_alts (9 alternatives) on seeds 0-49. Project labs re-run with python -I -W error (ledgers/M7/scripts/M7-d-r5/project_labs_r5.py). Two open items: m7d-cards-vs-lesson-text is only partly verified; float_arithmetic alternative fails by its own RuntimeError and is not counted. No external source was read.",
}

# mutants from the mutate tool output
mut_list = []
for line in MUT.read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if m:
        killed = m.group(4).strip()
        mut_list.append({
            "id": m.group(2),
            "description": m.group(3).strip(),
            "killed_by": killed if m.group(1) == "KILLED" else "SURVIVED on seeds 0-49 (no test failed)",
        })
fragment["mutants"] = mut_list
fragment["summary"] = {
    "rows": len(fragment["rows"]),
    "pass": sum(r["status"] == "PASS" for r in fragment["rows"]),
    "fail": sum(r["status"] == "FAIL" for r in fragment["rows"]),
    "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in fragment["rows"]),
    "mutants": len(mut_list),
    "mutants_survived": sum(m["killed_by"].startswith("SURVIVED") for m in mut_list),
}
out = root / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out, fragment["summary"])
