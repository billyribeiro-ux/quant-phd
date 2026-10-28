"""Build ledgers/M7/M7-d.json (round 4, slice M7-d) from the outputs of this round's runs.

Inputs: ledgers/M7/scripts/M7-d-r4/mutate_graders_M7_seeds0-49.txt and alternatives_seeds0-49.txt.
Usage: .venv/bin/python ledgers/M7/scripts/M7-d-r4/build_fragment_r4.py <checkout-root>
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
R4 = ROOT / "ledgers/M7/scripts/M7-d-r4"
PAGE = "course/modules/M/M7/project.html"
GRADER = "course/modules/M/M7/grader/test_project.py"
CARRY = "Carried from round 3 (project.html lines 53-166 and tests/labs/M7/lab-M7-project-1.py byte-identical since the previous pin): "

mutants = []
for line in (R4 / "mutate_graders_M7_seeds0-49.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+?): (.*?) -> (.*)$", line)
    if m:
        mutants.append({"id": m.group(2), "description": m.group(3), "killed_by": None if m.group(4) == "None" else m.group(4)})

rows = [
    ("m7d-lab1-numbers", "2.5 labs / 2.2 numbers: Lab 1 printed values and prose", f"{PAGE} lines 53-166; tests/labs/M7/lab-M7-project-1.py", "PASS",
     CARRY + "lines 53-166 are outside every hunk of the aa3c26c..2657ab5 diff; run_labs M7 11/11 PASS; ledgers/M7/scripts/M7-d-r3/lab1_check.py (round 3) recomputes the printed values."),
    ("m7d-lab2-completion", "2.5 labs: Lab 2 completion problem", f"{PAGE} lines 169-283; tests/labs/M7/lab-M7-project-2.py", "PASS",
     "Re-verified (line 171 reworded: 'this paragraph describes'). The two expected blocks at project.html lines 155 and 271 are identical (python: blocks[0]==blocks[1] True), which is the 'line for line' claim. run_labs M7 11/11 PASS; page_smoke project PASS."),
    ("m7d-lab3-certificate", "2.5 labs: Lab 3 certificate", f"{PAGE} lines 369-438; tests/labs/M7/lab-M7-project-3.py", "PASS",
     "Re-verified (lines 373 and 435-438 and twin docstring changed). Twin code lines 24-32 and 46-47 use upper=[0,0,0] with slackness |upper*(w-1)|, so 'bounds 0 <= w_i <= 1' is the code. Check B stationarity 9/550 = 2 x 9/1100 (shown). Check C primal residual is '0' in the expected block, so 'keeps the budget, so the primal residual stays zero' matches. run_labs PASS."),
    ("m7d-spec-residual-definitions", "2.4 math / spec: residual definitions", f"{PAGE} line 311 and lines 303-318; {GRADER}", "PASS",
     "Page lines 303-318 unchanged. Grader residual tests re-run: reference 50/50 seeds (run_graders M7 PASS); mutants m13, v08, w02, w04, m10 killed through test_certificate_* and test_complementary_slackness_holds."),
    ("m7d-spec-residual-wording", "2.9 prose: residual wording", f"{PAGE} line 311", "PASS", "Line 311 unchanged in the delta; the residual names match the test names in grader/test_project.py (test_stationarity_*, test_complementary_slackness_holds, test_certificate_*)."),
    ("m7d-spec-tolerance-agreement-1e-8", "2.4 spec: 1e-8 tolerance agreement", f"{PAGE} line 318; {GRADER} lines 36, 356 ff", "PASS",
     "Page line 318 unchanged; tolerance constants in grader/reference.py line 21 (TOL = 1e-9) and the 1e-8 hand-case tolerance (test_project.py) match the page; reference 50/50 seeds."),
    ("m7d-proof-uniqueness-midpoint", "2.4 math: uniqueness by midpoint", f"{PAGE} line 321", "PASS",
     CARRY.replace("lines 53-166 and tests/labs/M7/lab-M7-project-1.py", "line 321 and its proof text") + "line 321 is outside every hunk. Midpoint argument re-derived: f(mid) < (f(w)+f(w'))/2 = f(w) by strict convexity, contradicting minimality; midpoint feasible because constraints are affine in (w,t)."),
    ("m7d-proof-differentiability", "2.4 math: sufficiency proposition hypotheses and proof", f"{PAGE} lines 320-322", "PASS",
     "Re-derived (line 322 changed). Proof of sufficiency: L(w,t)=f(w)+sum lambda_j g_j+nu(1'w-1) is convex because f convex, lambda_j>=0 and g_j affine; zero gradient gives global minimum of L; for feasible (y,s): f(y) >= L(y,s) >= L(w,t) = f(w). Hypotheses listed at line 320 (f differentiable convex, constraints affine in (w,t), feasible, multipliers signed and complementary) are the ones the proof uses. Uniqueness in w uses strict convexity and minimality; checked. Instance Sigma = (A'A+I)/1000 at grader/instance.py line 41 supports the PD claim."),
    ("m7d-proof-multiplier-existence", "2.4 math / honest gap: existence of multipliers", f"{PAGE} line 322", "PASS",
     "Line 322 now reads 'Existence of multipliers for every generated instance is not proved on this page. The reference was checked on seeds 0 to 49 only: ... (run_graders M7, 50 of 50), which is evidence for those seeds only.' Matches the round-3 FAIL: the sentence no longer misstates the suite scope. run_graders M7 seeds 0-49 PASS 50/50 this round."),
    ("m7d-spec-tolerance-1e-9", "2.4 spec: 1e-9 tolerance on starting-portfolio checks", f"{PAGE} line 318; {GRADER} lines 443-489", "PASS",
     "Page line 318 unchanged. The 1e-9 starting-portfolio tolerance is TOL at grader/reference.py line 21 and used at lines 102-108. Boundary tests start-within-upper/lower/sector-cap and start-sums-to-one exist in the collected list. Mutants m12 (1e-7), m19 (1e-6), v03 (1e-5), w01 (1e-8), s05 (1e-10), x01 (no tolerance) are all killed."),
    ("m7d-spec-nan-inf-named", "2.4 spec: NaN/infinite refusal", f"{PAGE} line 323; {GRADER} lines 611-619", "PASS",
     "Line 323 lists 'a value is NaN or infinite' as a named ValueError condition; collected tests test_non_finite_value_is_refused_with_value_error[gamma|turnover_limit|mu|w0|lower|upper|sector_caps|sigma x nan/+inf/-inf] (24 cases: 8 fields x nan, +inf, -inf) exist. Mutants m11, m24, v01, s07 killed."),
    ("m7d-spec-named-message", "2.9 spec: refusal carries a message", f"{PAGE} line 323", "PASS",
     "Page: 'A named condition is refused with ValueError, and the refusal carries a message.' The suite checks the exception type for named conditions; the message is not required to name the condition on this page, so mutant v06 does not violate this sentence. The plan (line 192) asks for naming; that conflict is recorded in m7d-mutants-new-v06."),
    ("m7d-spec-named-list-coverage", "2.9 spec: named-condition list vs tests", f"{PAGE} lines 323, 329; {GRADER} lines 570-620", "PASS",
     "Line 323 lists the named conditions. Collected names cover each: sigma-symmetric, sigma-positive-definite (incl. the new indefinite case, line 429 insert), gamma-positive, turnover-limit-not-negative, lower-not-above-upper, start-sums-to-one, start-within-upper/lower/sector-cap, sector-label-in-range, every-sector-has-an-asset (incl. the new extra-cap case, line 522 insert), one-entry-per-asset; plus non-mapping, missing field, NaN/inf, no assets, wrong type, float label, empty caps (147 collected)."),
    ("m7d-spec-boundary-claim", "2.4 spec: boundary values accepted", f"{PAGE} lines 323-324, 329; {GRADER} boundary tests", "PASS",
     "Collected boundary tests: lower-equals-start, upper-equals-start, cap-equals-start, start-sum-inside-low-side, plus the *-boundary cases for each named condition. Mutants f02, f03, f04, s03, s09, w03 killed through them."),
    ("m7d-spec-test-count-and-seeds", "2.9 spec: test count and seeds", f"{PAGE} line 329", "PASS",
     "pytest --collect-only on the reference workspace gives 147 tests with QF_SEED 0, 17 and 49 (same count). Page says 'collects 147 checks, the same number for every seed'. Matches."),
    ("m7d-spec-hours", "2.9 hours: arithmetic of hub split and project hours", f"{PAGE} lines 33, 341-347; course/modules/M/M7/index.html line 141", "PASS",
     "Arithmetic only (architect ruling). Lessons: L01 9, L02 9, L03 10, L04 10, L05 10, L06 10, L07 9, L08 10 (data-hours), sum 77; hub line 141 says 77 and '1, 2, 7 declare 9 hours and the others 10'. Project table rows 3+2+10+6+7+5 = 33 (page line 341-347). 77+33 = 110, the hub's module total. Consistent."),
    ("m7d-spec-other-claims", "2.9 prose: other changed claims", f"{PAGE} lines 297-299, 324-327, 355, 362-363", "PASS",
     "Line 355: 'saved in this browser a moment after you stop typing' matches course/assets/js/grader.js line 61 (400 ms debounce after input). Line 362-363 lab interpretation matches the lab output (see m7d-lab3-certificate). Lines 297-299 and 324-327 unchanged or checked against the reference."),
    ("m7d-hand-cases", "2.4 hand-worked cases", f"course/modules/M/M7/grader/test_project.py lines 218-246", "PASS",
     CARRY.replace("lines 53-166 and tests/labs/M7/lab-M7-project-1.py", "lines 218-246 of the grader") + "the hand-case block is above the first hunk (line 426); reference passes 50/50; alternatives core_route1-5, bland, exact_order, first_order pass all five hand cases (alternatives_seeds0-49.txt)."),
    ("m7d-hand-case-tolerance", "2.4 hand-case tolerance 1e-8", f"course/modules/M/M7/grader/test_project.py lines 394-395", "PASS",
     "Lines 394-395 are above the first hunk; the 1e-8 tolerance is what the page states (project.html line 329: 'within 10^-8 of its worked value'). Alternatives pass."),
    ("m7d-comparators-and-edges", "2.4 comparators and edge cases", f"course/modules/M/M7/grader/test_project.py lines 372-379", "PASS",
     "Lines 372-379 are above the first hunk; reference passes; alternatives pass (alternatives_seeds0-49.txt)."),
    ("m7d-grader-suite-over-constraint", "2.5 grader over-constraint: alternatives", "ledgers/M7/scripts/M7-d-r4/run_alts_r4.py (= M7-d-r3/run_alts_r3.py run on this pin); alternatives_seeds0-49.txt", "PASS",
     "Nine alternatives on seeds 0-49: core_route1-5 50/50 each; bland 50/50; exact_order 50/50; first_order 50/50; float_arithmetic 0/50. The float alternative raises RuntimeError('the working set lost independence') at constrained_allocator.py line 233 on valid cases (checked for seeds 0 and 2), so it is an alternative defect, not an over-constraint witness: it does not return numbers satisfying the definitions. Honest gap: no verifier-written float solver that returns valid answers was run."),
    ("m7d-mutants-existing", "2.5 grader mutants: existing m01-m24, f01-f10, s01-s10", "ledgers/M7/mutants/ (f01-f10, m01-m24, s01-s10)", "PASS",
     "All 44 existing mutants of these series killed on seeds 0-49 (mutate_graders_M7_seeds0-49.txt). The only survivor of the whole folder is v06 (row m7d-mutants-new-v06)."),
    ("m7d-mutants-new-v01-v04", "2.5 grader mutants: round-3 verifier mutants v01-v04", "ledgers/M7/mutants/v01_nan_in_mu_silently_zeroed.py, v02_second_sector_cap_never_imposed.py, v03_start_tolerance_1e-5.py, v04_weights_rounded_to_six_places.py", "PASS", "All four KILLED (mutate_graders_M7_seeds0-49.txt)."),
    ("m7d-mutants-new-v05", "2.5 grader mutants: v05", "ledgers/M7/mutants/v05_mu_longer_than_sigma_truncated.py; grader/test_project.py", "PASS", "KILLED by test_named_condition_other_side_is_refused_with_value_error[mu-one-entry-too-many] (seed 0)."),
    ("m7d-mutants-new-v06", "2.5 grader mutants: v06 survives; plan requires naming", "ledgers/M7/mutants/v06_every_refusal_says_invalid_input.py; plans/M7-build-plan.md line 192; course/modules/M/M7/project.html line 323", "FAIL",
     "SURVIVED on seeds 0-49. The plan states the behaviour: 'Infeasible constraints, a non-positive-definite Sigma, or a wrong-shaped input raise ValueError naming the violated condition' (plans/M7-build-plan.md line 192). The page (line 323) says only 'the refusal carries a message', and v06 does carry a message, so the suite and the page agree but the plan's naming requirement is neither in the page nor tested. Fix: either the page states that a named condition's refusal names it and the suite checks it, or the plan's naming sentence is withdrawn for the page and v06 is removed from the mutants folder with that reason written in the plan."),
    ("m7d-mutants-new-v07-v08", "2.5 grader mutants: v07, v08", "ledgers/M7/mutants/v07_starting_sector_cap_never_checked.py; v08_turnover_total_residual_sign_flipped.py", "PASS", "Both KILLED (mutate_graders_M7_seeds0-49.txt)."),
    ("m7d-mutants-new-w01-w07", "2.5 grader mutants: w01-w07", "ledgers/M7/mutants/w01..w07 (w05 removed)", "PASS", "w01, w02, w03, w04, w06, w07 KILLED on seeds 0-49. w05 is absent from the folder (equivalent-mutant row below)."),
    ("m7d-mutants-w05-equivalent", "2.5 equivalent mutants", "ledgers/M7/scripts/M7-d-r3/make_mutants_r3.py (w05 entry removed)", "PASS", "Carried from round 3 (make_mutants_r3.py byte-identical since the previous pin): w05 was not written, so it is not in the mutants list."),
    ("m7d-mutants-new-r4-x01-x03", "2.5 grader mutants: three verifier-written student errors this round", "ledgers/M7/mutants/x01_start_upper_bound_without_tolerance.py; x02_sector_label_upper_off_by_one.py; x03_sector_cap_checked_cumulatively.py; written by ledgers/M7/scripts/M7-d-r4/make_verifier_mutants_r4.py", "PASS",
     "x01 KILLED by test_named_condition_boundary_is_accepted[start-sums-to-one-boundary] (seed 0); x02 KILLED by test_named_condition_is_refused_with_value_error[sector-label-in-range-invalid] (seed 0); x03 KILLED by test_wrong_type_is_refused_with_an_exception[lower-nothing] (seed 0). Each is a plausible student error stated by the page (the 1e-9 starting tolerance, line 318; the label range 0 to K-1, line 323; per-sector caps, line 323)."),
    ("m7d-mutate-tool-verdict", "2.5 mutation gate: tools/mutate_graders.py --unit M7", "tools/mutate_graders.py; ledgers/M7/scripts/M7-d-r4/mutate_graders_M7_seeds0-49.txt", "FAIL",
     "Final line: 'mutate_graders M7: FAIL (60/61 killed)'. Exit status 1. The only survivor is v06 (row m7d-mutants-new-v06). Fix as in that row."),
    ("m7d-grader-run-graders", "2.5 grader: run_graders M7 seeds 0-49", "tools/run_graders.py --unit M7 --seeds 0-49", "PASS", "Output: 'run_graders M7: PASS (reference 50/50 seeds, slowest 1.3 s)'. Starter fails the suite per the same tool."),
    ("m7d-grader-mypy", "2.5 grader: mypy strict", "plans/M7-build-plan.md section 12 command over grader/reference.py, instance.py, starter.py and tests/labs/M7/*.py", "PASS", "'Success: no issues found in 14 source files'."),
    ("m7d-ruff", "2.5 ruff check and format", "tests/labs/M7; course/modules/M/M7/grader", "PASS", "ruff check: 'All checks passed!'; ruff format --check: '15 files already formatted'."),
    ("m7d-run-labs", "2.5 labs: run_labs --unit M7", "tools/run_labs.py --unit M7", "PASS", "'run_labs M7: PASS (11/11)'."),
    ("m7d-check-projects-pages-dag", "2.9 structure and DAG", "tools/check_projects.py, tools/check_pages.py, tools/check_dag.py --unit M7", "PASS", "check_projects M7: PASS; check_pages M7: PASS; check_dag M7: PASS."),
    ("m7d-page-smoke-project", "2.5 labs in Pyodide", "tools/page_smoke.py --unit M7 --pages project", "PASS", "'page_smoke modules/M/M7/project.html: PASS'; in-browser grader 'All 147 tests pass on seed 303689375 (2.1 s)'."),
    ("m7d-pytest-M7", "2.5 pytest -k M7", "tests/test_labs.py (selected by -k M7)", "PASS", "11 passed."),
    ("m7d-lab-numbers-cards-subset", "2.2 card numbers for C cards", "course/modules/M/M7/cards.json (37 C cards, M7-c012 to M7-c157)", "PASS",
     "Carried from round 3 (the 37 C-grade card objects are identical to aa3c26c: python comparison of per-id objects lists only 12 changed cards, all grade T)."),
    ("m7d-cards-schema", "2.7 cards: schema", "course/modules/M/M7/cards.json", "PASS", "143 cards; every card has id, lesson, front, back, grade; the 37 C cards also have basis."),
    ("m7d-cards-grade-field", "2.7 cards: grade field", "course/modules/M/M7/cards.json", "PASS", "Grades: T 106, C 37; no other value."),
    ("m7d-cards-duplicates", "2.7 cards: duplicate scan", "course/modules/M/M7/cards.json", "PASS", "143 unique ids; no duplicate normalized fronts."),
    ("m7d-cards-basis-stale-lab", "2.7 cards: C-card basis names a lab", "course/modules/M/M7/cards.json (M7-c063)", "PASS", "M7-c063 basis 'Lab 1 (exact arithmetic on the listed grids)'; the lab is tests/labs/M7/lab-M7-L04-1.py, unchanged this round."),
    ("m7d-cards-cite-attribution", "2.7 cards: attributions and cites", "course/modules/M/M7/cards.json (M7-c008, c009, c015, c031, c069, c071, c083, c097, c149, c155, c156)", "PASS",
     "The changed cards cite only lesson-defined items (Assumption 1 in L01/L02, Problem P3 in L01, Remark 1.5 and Proposition 1.4 in L04, Definition 3.3 and Theorem 3.1 in L05, Definition 1.1 in L06, Proposition 2.3 and Remark 2.4 in L08). No bibliographic data is cited on the cards."),
    ("m7d-cards-changed-r4", "2.7 cards vs CURRENT lesson text: the 12 changed T cards", "course/modules/M/M7/cards.json: M7-c008, c009, c015, c031, c069, c071, c083, c097, c149, c155, c156 (c092 in its own row)", "PASS",
     "Each card statement and its locator read against the current lesson: c008 vs L01 Proposition 3.2 (i)-(iii) and Assumption 1; c009 vs L01 Example 3.3 and Problem P3 (line 286); c015 vs L01 lines 203, 286; c031 vs L02 Theorem 2.2 and example (line 194); c069 vs L04 Proposition 1.3 and Lab 1 value -199/300 (line 168); c071 vs L04 Remark 1.5 and Proposition 1.4 (line 172); c083 vs L05 Definition 3.3; c097 vs L06 line 276; c149 vs L08 Proposition 2.3 (line 281); c155 vs L08 Proposition 2.3 and Remark 2.4 (line 217); c156 vs L08 Remark 1.5 and Theorem 1.4 (lines 219, 278). Each card number appears in its lesson."),
    ("m7d-cards-c092-hypothesis-dropped", "2.7 cards: hypotheses of Theorem 3.1 dropped", "course/modules/M/M7/cards.json M7-c092; course/modules/M/M7/L05.html Theorem 3.1 (statement: 'Assume Q is symmetric positive semidefinite')", "FAIL",
     "Card back: 'Stationarity together with feasibility and that sign certifies optimality; stationarity alone does not.' The lesson's Theorem 3.1 has the hypothesis Q symmetric positive semidefinite (a convex QP), and Remark 3.2's counterexample is in the same section; without convexity a KKT point need not be optimal (L05 line 257 and Misconception 1). The card drops the hypothesis. Fix: 'For a convex QP (Q symmetric positive semidefinite), stationarity with the sign condition mu >= 0 and feasibility certifies optimality; stationarity alone does not (Theorem 3.1, Remark 3.2).'"),
    ("m7d-cards-vs-lesson-text", "2.7 cards: full read of all 143 cards against L01-L08 prose", "course/modules/M/M7/cards.json (143 cards) against course/modules/M/M7/L01.html-L08.html", "UNVERIFIABLE",
     "Not done this round: a line-by-line read of all 143 cards against the full text of the eight changed lesson pages. The 12 changed cards and the cards citing changed lesson items were read (row m7d-cards-changed-r4); the others carry the round-3 status and are not re-read against the changed lessons. Fix: a full card-by-card read against the current lesson text."),
    ("m7d-registry-and-citations", "2.1 citations", f"{PAGE} lines 459-460; references/references.json", "PASS", "Carried from round 3 (references/references.json and the cited lines 459-460 byte-identical since the previous pin). No external source was read this round."),
    ("m7d-ruling-hours-pace", "architect ruling: hours are design targets", f"{PAGE} lines 341-347", "PASS", "Not graded on pace (architect ruling). Only the arithmetic is checked (row m7d-spec-hours)."),
]

fragment = {
    "unit": "M7",
    "slice": "M7-d",
    "round": 4,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 4, slice M7-d: project.html, grader, project labs, cards.json; did not build M7)",
    "pin": "2657ab5 (detached checkout /tmp/verifyB4-M7-d; previous round pin aa3c26c; delta aa3c26c..2657ab5 covers project.html, grader/test_project.py, cards.json, L01-L08 and index.html, the M7 lab twins L07 and project-3, the M7 mutants folder)",
    "base": "aa3c26c",
    "checkout": "/tmp/verifyB4-M7-d",
    "scratch": "/tmp/M7-v/d/",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": [
        {"id": i, "check": c, "location": loc, "status": st, "evidence": ev, **({} if st == "PASS" else {"fix": fix_text})}
        for (i, c, loc, st, ev), fix_text in zip(
            rows,
            [
                "" if r[3] == "PASS" else (
                    "Fix the refusal messages or withdraw the naming sentence in plans/M7-build-plan.md line 192 for the page; then re-run mutate_graders M7." if r[0] == "m7d-mutants-new-v06"
                    else "Add the convexity hypothesis to M7-c092." if r[0] == "m7d-cards-c092-hypothesis-dropped"
                    else "Re-run mutate_graders M7 after the v06 decision." if r[0] == "m7d-mutate-tool-verdict"
                    else "Read all 143 cards against the current L01-L08 text."
                )
                for r in rows
            ],
        )
    ],
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round-4 delta re-verification (pin 2657ab5 vs aa3c26c). Commands run on the pin: check_projects/check_pages/check_dag M7 PASS; run_labs M7 11/11; run_graders M7 seeds 0-49 50/50; pytest collect 147 at seeds 0, 17, 49; page_smoke project PASS; ruff check and format PASS; mypy --strict plan command PASS; pytest -k M7 11 passed; mutate_graders M7 --seeds 0-49 60/61 (v06 survives); alternatives on seeds 0-49: core routes 1-5, bland, exact_order, first_order 50/50 each, float_arithmetic 0/50 (own RuntimeError on valid cases, not counted). New verifier mutants x01-x03 all killed. The r3 FAIL row m7d-proof-multiplier-existence is now PASS (line 322 reworded). Re-derived: sufficiency proof (project.html line 320-322), Lab 2 vs Lab 1 expected blocks identical, Lab 3 bound docstring vs code, hub hours 77+33=110. Not done: a full read of all 143 cards against the current eight lesson pages (row m7d-cards-vs-lesson-text is UNVERIFIABLE). No external source was read."
    ),
    "summary": {},
}
fragment["summary"] = {
    "rows": len(fragment["rows"]),
    "pass": sum(r["status"] == "PASS" for r in fragment["rows"]),
    "fail": sum(r["status"] == "FAIL" for r in fragment["rows"]),
    "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in fragment["rows"]),
    "mutants": len(mutants),
    "mutants_survived": sum(m["killed_by"] is None for m in mutants),
}
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, fragment["summary"])
