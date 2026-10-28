"""Build ledgers/CF1/CF1-d.json for round 15 (slice CF1-d) from the round-14 fragment and this round's evidence."""

import json
import pathlib
import re

CHECKOUT = pathlib.Path("/tmp/verify15-CF1-d")
PREV = json.loads(pathlib.Path("/tmp/fanout-frags/CF1-d.round14.json").read_text(encoding="utf-8"))
MUT_OUT = pathlib.Path("/tmp/CF1-v/d15/mutate2.out").read_text(encoding="utf-8").splitlines()

CARRY_PREFIX = "Carried from round 14 (course/modules/CF/CF1/project.html lines and grader/test_project.py test bodies cited here are outside the round-15 hunks; cards.json entries cited here other than CF1-c054, c056, c058, c060, c094; all other cited files byte-identical since the previous pin, grader line numbers shifted by the round-15 insertions, tests re-found by name): "

# Rows re-verified or re-run in round 15: id -> (status, evidence).
NEW = {
    "proj-test-count-72": ("PASS", "Re-verified round 15: project.html line 192 now reads 'collects 138 checks'; pytest --collect-only -q on grader/reference.py (copied by the grader workspace of tools/run_graders.py, /tmp/CF1-v/d15/collect.py) prints '138 tests collected' under QF_SEED=0."),
    "proj-spec-count-118-hub": ("PASS", "Re-verified round 15: project.html line 192 states 138; the collected count on the reference is 138 (see proj-test-count-72). No '118' remains in the page."),
    "proj-count-cause-wording": ("PASS", "Re-verified round 15: the stated cause ('no parametrize list's length depends on the seed') is checked by collecting the reference and the starter for seeds 0-49 (/tmp/CF1-v/d15/collect.py with S=0..49): 138 on every seed for both, so no list length varies with the seed."),
    "proj-collect-count-50-seeds": ("PASS", "Re-verified round 15: collect-only on reference and starter for QF_SEED 0 to 49 gives 138 for all 100 runs (output tally: 100 x '138')."),
    "r13-collect-count-126": ("PASS", "Re-verified round 15: the page count (line 192, 138) equals the collected count (138). The round-13 figure 126 is superseded by the round-15 count."),
    "proj-grader-reference-50-seeds": ("PASS", "Re-run round 15: tools/run_graders.py --unit CF1 --seeds 0-49 printed 'run_graders CF1: PASS (reference 50/50 seeds, slowest 0.6 s)' (/tmp/CF1-v/d15/run_graders.out)."),
    "proj-mutants-killed": ("PASS", "Re-run round 15: tools/mutate_graders.py --unit CF1 --seeds 0-9 printed 'mutate_graders CF1: PASS (136/136 killed)' over all 136 flat files in ledgers/CF1/mutants/ (133 previous plus the 3 new r15e mutants), output /tmp/CF1-v/d15/mutate2.out."),
    "r13-mutants-full-run": ("PASS", "Re-run round 15: 136/136 killed (/tmp/CF1-v/d15/mutate2.out). The round-14 survivor r14v_01_rate_above_one_read_as_percent is now KILLED by test_npv_reads_a_rate_above_one_as_a_decimal_per_year (seed 0)."),
    "r14-mutant-r14v-01-rate-above-one-read-as-percent": ("PASS", "Re-run round 15: 'KILLED r14v_01_rate_above_one_read_as_percent.py: ... -> test_npv_reads_a_rate_above_one_as_a_decimal_per_year (seed 0)'. The new test is justified by project.html line 190 ('every rate is a decimal per year'); npv(2.0, [-100, 0, 300]) = -66.67 in the reference (-100 + 300/9), which the test asserts."),
    "index-ladder-rung1-worked-example": ("PASS", "Re-verified round 15: course/modules/CF/CF1/index.html line 151 now reads 'including an NPV of 926.00 dollars at 10 percent (step 7)'. tests/labs/CF1/lab-CF1-project-1.py prints 'step 7, NPV at 0.10: 926.00 dollars' (line 4 of the expected block); the claim no longer says the example ends at 926.00, and steps 8 and 9 are printed after it. project.html line 55 ('(step 7)') matches the same output."),
    "cards-count-vs-plan": ("FAIL", "Re-verified round 15 (unchanged finding): cards.json has 103 entries; per lesson L01 18, L02 17, L03 16, L04 20, L05 17, L06 15. plans/CF1-build-plan.md line 240 says 'the planner expects four to six per lesson', and plans/CF1-build-plan.md is byte-identical since the previous pin. Every lesson is over the planned range."),
    "proj-tolerance-nine-recount": ("PASS", "Re-verified round 15 after the grader line shift: project.html line 209 says 'Nine checks use an absolute floor of 1e-6 cents'. The absolute=1e-6 checks in grader/test_project.py are at lines 504 (every year's flow, shield), 514 (working-capital sum), 520 (year-1 flow), 529 (one-year project), 543 (working-capital each year), 563 (real-rate NPV), 708 (zero-EBITDA tax credit), 779 (Monte Carlo draws), 813 (Monte Carlo mean): nine, matching the page's list."),
    "proj-exemplar-a-quote": ("PASS", "Re-verified round 15: project.html line 405 (Exemplar A, 1 Recommendation annotation) now reads 'The rate is given as \"the 10 percent rate\", with no basis.' The quoted phrase appears in the Exemplar A recommendation (line 404: 'which is above the 10 percent rate'); the rest of the annotation is unchanged."),
    "cards-missing-grade-or-basis": ("PASS", "Re-run round 15 on course/modules/CF/CF1/cards.json: 103 entries, every entry has a grade and a basis or cite; no entry lacks either (python -I check, /tmp/CF1-v/d15)."),
    "cards-duplicate-scan": ("PASS", "Re-run round 15: 103 unique ids and 103 unique fronts after the five rewritten fronts (c054, c056, c058, c060, c094); no duplicates."),
    "cards-numbers-in-lesson": ("PASS", "Re-verified round 15 for the five changed cards: 189.04 (L04 line 330), 680.27 (L04 lines 322 and 413), 27,272.73 and 18,181.82 (L04 line 135), 0.200000 and 0.100000 (L04 lines 281-292, Lab 1 output). Every number on the five changed cards appears in L04 or its lab output."),
    "cards-grade-semantics": ("PASS", "Re-verified round 15: CF1-c056 is grade C with basis 'Lab 1 (SIMULATED cash flows)', which is correct for a result read off a SIMULATED lab. CF1-c054, c058, c060 and c094 are T with bases that are proved or computed in L04 (Theorem 4.1, Corollary 2.2, Proposition 3.3, Example 4.2)."),
    "proj-irr-close-roots-missed": ("PASS", "Re-run round 15 on grader/reference.py: irr_roots([-100, 220.1, -121.11]) == [] (the page says neither root is returned), irr_roots([-100, 221, -122.1]) == [0.1000000000000123, 0.10999999999999743] (the page says 0.1 and 0.11 are both returned). Both match project.html line 207."),
    "proj-irr-grid-close-pair-example": ("PASS", "Re-run round 15 (same command as proj-irr-close-roots-missed): both close-pair examples of project.html line 207 reproduce, and 1 + r grid factor 1e8 ** (1/4000) = 1.0046157902783952 (page: 1.0046158 and 1.00462 rounded)."),
    "proj-lab3-recomputed-numbers": ("PASS", "Re-run round 15: /tmp/CF1-v/d15/xcheck_mc.py calls grader/reference.py npv_monte_carlo(rung-1 project, 0.10, 2000, 42, 0.2): mean 885.85, sd 2445.52, se 54.68, 787 negative, lowest -4808.83, highest 13800.44 (all as printed by Lab 3, output /tmp/CF1-v/d15/lab-CF1-project-3.py.out); IRR 0.153177; two-root flow 0.1 and 0.2; payback 2.37 and 2.7535."),
    "proj-lab1-twin-output": ("PASS", "Re-run round 15: 'python -I -W error tests/labs/CF1/lab-CF1-project-1.py' exits 0; its output equals the page's expected block (checked by exact comparison, MATCH)."),
    "proj-lab2-completion-twin": ("PASS", "Re-run round 15: lab-CF1-project-2.py under python -I -W error exits 0; output equals the page's expected block (MATCH)."),
    "proj-lab3-sanity-run": ("PASS", "Re-run round 15: lab-CF1-project-3.py under python -I -W error exits 0; output equals the page's expected block (MATCH)."),
    "proj-pytest-lab-helper": ("PASS", "Re-run round 15: tools/run_labs.py --unit CF1 prints 'run_labs CF1: PASS (9/9)'; the three project twins exit 0 under python -I -W error; the expected blocks match the printed output."),
    "proj-page-smoke": ("PASS", "Re-run round 15: tools/page_smoke.py --unit CF1 prints 'page_smoke CF1: PASS'."),
    "proj-check-dag": ("PASS", "Re-run round 15: tools/check_dag.py --all prints 'check_dag CF1: PASS' (and AC4, AP1 PASS)."),
    "proj-structure-and-gates": ("PASS", "Re-run round 15: tools/check_projects.py --all prints 'check_projects CF1: PASS'; tools/check_pages.py --all prints 'check_pages CF1: PASS'; tools/check_dag.py --all prints 'check_dag CF1: PASS'."),
    "proj-verify-refs": ("PASS", "Re-run round 15: tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'; tools/verify_refs.py --unit CF1 (live): 'live re-verification of CF1: 2 of 560 entries, 0 problems'. references/references.json is byte-identical since cef676e."),
    "proj-mypy-grader-gate": ("PASS", "Re-run round 15: mypy --no-incremental --strict on grader/reference.py, instance.py, starter.py: 'Success: no issues found in 3 source files'."),
    "proj-ruff-format": ("PASS", "Re-run round 15: ruff check and ruff format --check on course/modules/CF/CF1/grader and tests/labs/CF1: 'All checks passed!' and '13 files already formatted'."),
    "proj-mc-draw-method-unenforced": ("PASS", "Re-run round 15: test_monte_carlo_draws_follow_the_seeded_gauss_stream (grader line 770 onward, unchanged body) is KILLED by the round-15 mutant r15e_02 (sorted draws) and r13v_01; project.html line 209 states the draw order."),
    "proj-mutants-round11-new": ("PASS", "Re-run round 15: all m59 and m60 mutants are in the 136-file run; both KILLED (mutate2.out)."),
    "r13-mutants-r13d-killed": ("PASS", "Re-run round 15: r13d_01..r13d_10 are in the 136-file run; all KILLED (mutate2.out)."),
    "proj-alternatives-correct": ("PASS", "Re-run round 15: all 41 alternative engines from ledgers/CF1/scripts/*/alts/ (rounds 9 to 15) PASS 50/50 seeds (/tmp/CF1-v/d15/allalts.out)."),
    "proj-alternatives-round10": ("PASS", "Re-run round 15: alt_r10_1..5 are in the 41-engine run; all PASS 50/50 seeds."),
    "r13-prior-alternatives-rerun": ("PASS", "Re-run round 15: all 41 prior alternatives PASS 50/50 seeds (/tmp/CF1-v/d15/allalts.out)."),
    "r13-alternatives-new": ("PASS", "Re-run round 15: alt_r13v_a/b/c are in the 41-engine run; all PASS 50/50 seeds."),
    "r14-alternatives-new": ("PASS", "Re-run round 15: the round-14 alternatives are in the 41-engine run; all PASS 50/50 seeds."),
    "proj-equivalent-mutant-proof": ("PASS", "Re-verified round 15: ledgers/CF1/mutants/ has 136 flat mutant files, all KILLED by mutate_graders (136/136). No equivalent mutant is listed in the mutants list; the earlier equivalence proofs (round 13 and before) are unchanged because their cited subjects are unchanged."),
    "r13-run-graders-50": ("PASS", "Re-run round 15: tools/run_graders.py --unit CF1 --seeds 0-49 PASS (reference 50/50)."),
    "r13-twins-under-python-I-W-error": ("PASS", "Re-run round 15: the three project twins run under python -I -W error with exit 0; run_labs CF1 PASS 9/9."),
    "proj-named-errors-untested": ("PASS", "Re-verified round 15: each named error paragraph line of project.html line 210 (rate at or below -1 in NPV, payback, Fisher, Monte Carlo) now has parametrized tests that include -2 values (test_npv_rejects_rates_at_or_below_minus_one, test_fisher_rejects_rates_at_or_below_minus_one, test_monte_carlo_refuses_a_rate_at_or_below_minus_one). The page's list is still a subset of what the tests check."),
    "r13-rate-minus-one-named-errors": ("PASS", "Re-verified round 15: test_npv_rejects_rates_at_or_below_minus_one (nan, inf, -1, -2), test_fisher_rejects_rates_at_or_below_minus_one (real and inflation at -1 and -2), test_monte_carlo_refuses_a_rate_at_or_below_minus_one (-1, -2) match project.html line 210. Mutant r15e_01 (real rate -1 accepted) is KILLED by the Fisher real-minus-one case."),
}

ROWS_NEW = [
    {
        "id": "r15-delta-coverage",
        "check": "2.9 / delta coverage: every hunk of slice d read",
        "location": "git diff cef676e c093bf5 for course/modules/CF/CF1/project.html (hunks at lines 192 and 405), grader/test_project.py (five hunks: new tests after line 136 and after line 185; test_irr_rejects_all_zero_flows; the Fisher and Monte Carlo parametrize lists), cards.json (CF1-c054, c056, c058, c060, c094)",
        "status": "PASS",
        "evidence": "Every hunk was read in full (git diff cef676e c093bf5 -- course/modules/CF/CF1/project.html course/modules/CF/CF1/cards.json tests/labs/CF1 course/modules/CF/CF1/grader). The project labs under tests/labs/CF1 and the grader's instance.py and reference.py are unchanged in this delta. Other changed files (index.html, L05.html, L06.html, L01-L04 hunks) belong to other slices; index.html line 151 is checked in index-ladder-rung1-worked-example and L06.html lines 209-211 in r13-l06-unrounded-difference-basis.",
    },
    {
        "id": "r15-grader-rate-above-one-test",
        "check": "2.6-spec / ruling (a),(b): new test test_npv_reads_a_rate_above_one_as_a_decimal_per_year",
        "location": "course/modules/CF/CF1/grader/test_project.py (new test after test_npv_of_a_single_flow_is_that_flow); course/modules/CF/CF1/project.html line 190 ('every rate is a decimal per year')",
        "status": "PASS",
        "evidence": "The spec sentence on line 190 states the rate convention, so a rate of 2.0 is 200 percent a year. The reference returns npv(2.0, [-100, 0, 300]) = -66.666... = -100 + 300/9, which the test asserts. The reference passes on 50 seeds and the alternatives pass too (50/50). The mutant r14v_01 that divides rates above 1 by 100 is KILLED by this test.",
    },
    {
        "id": "r15-grader-irr-low-end-zero-test",
        "check": "2.6-spec / ruling (a): new test test_irr_does_not_report_a_zero_at_the_low_end_of_the_window",
        "location": "course/modules/CF/CF1/grader/test_project.py (new test after test_irr_does_not_report_a_tangent_root_at_the_window_end); course/modules/CF/CF1/project.html line 207 ('neither is a zero exactly at an end of the window')",
        "status": "PASS",
        "evidence": "The test asserts irr_roots([-0.0001, 1.0]) == []: NPV(r) = -0.0001 + 1/(1+r) has its zero at x = 0.0001, which is rate 9999, the low-x end of the window (the page's window 0.0001 to 10000, rates -0.9999 to 9999). The page says such a zero is not reported. The reference returns [] (run_graders 50/50), and alternative alt_r15e_a (cumulative-product grid, endpoints exact) also passes 50/50.",
    },
    {
        "id": "r15-grader-zero-flow-two-zeros",
        "check": "2.6-spec: test_irr_rejects_all_zero_flows now parametrized with [0,0,0] and [0,0]",
        "location": "course/modules/CF/CF1/grader/test_project.py test_irr_rejects_all_zero_flows; project.html line 209 ('an IRR request with fewer than two flows, or with every flow zero')",
        "status": "PASS",
        "evidence": "[0.0, 0.0] has two flows (not fewer than two) and every flow is zero, so the named error applies. The reference raises ValueError for it (every flow is zero check); the test passes on 50 seeds.",
    },
    {
        "id": "r15-grader-fisher-and-mc-below-minus-one",
        "check": "2.6-spec / ruling (a),(b): new Fisher parametrize cases (-2.0 real and inflation) and Monte Carlo case -2.0",
        "location": "course/modules/CF/CF1/grader/test_project.py test_fisher_rejects_rates_at_or_below_minus_one and test_monte_carlo_refuses_a_rate_at_or_below_minus_one; project.html line 210 (named errors: 'a rate at or below −1 in an NPV, a discounted payback, a Fisher conversion or a Monte Carlo request')",
        "status": "PASS",
        "evidence": "The named-error paragraph covers every rate at or below -1, so -2 is inside the stated rule. The reference refuses these inputs (50/50 seeds). Alternatives that refuse at or below -1 pass. Mutant r15e_01 (real rate exactly -1 accepted by a strict check) is KILLED by test_fisher_rejects_rates_at_or_below_minus_one[real-minus-one].",
    },
    {
        "id": "r15-page-count-138",
        "check": "2.9 / page count equals the collected count after the round-15 additions",
        "location": "course/modules/CF/CF1/project.html line 192 ('collects 138 checks'); course/modules/CF/CF1/grader/test_project.py",
        "status": "PASS",
        "evidence": "pytest --collect-only on the reference via the grader workspace prints 138 tests for seeds 0-49 (100 of 100 runs, all 138). The count changes by +6 relative to the previous 132: two new tests, one extra zero case, two extra Fisher cases and one extra Monte Carlo case.",
    },
    {
        "id": "r15-exemplar-a-annotation-quote",
        "check": "2.9 prose: Exemplar A annotation rewritten ('is given as' instead of 'is named only as')",
        "location": "course/modules/CF/CF1/project.html line 405 (Exemplar A, 1 Recommendation annotation)",
        "status": "PASS",
        "evidence": "The annotation says 'The rate is given as \"the 10 percent rate\", with no basis.' The quoted phrase appears verbatim in line 404 ('which is above the 10 percent rate'). The annotation's level-2 claim (the NPV is not stated with its rate) matches line 404, which states only the IRR.",
    },
    {
        "id": "r15-cards-c054-c056-c058-c060-c094",
        "check": "2.7 cards: five rewritten fronts and backs agree with L04 and its lab output",
        "location": "course/modules/CF/CF1/cards.json CF1-c054, CF1-c056, CF1-c058, CF1-c060, CF1-c094; course/modules/CF/CF1/L04.html Theorem 4.1 (line 126), Corollary 2.2 (line 85), Example 3.2 (line 101), Proposition 3.3 (line 107), Example 4.2 (line 134), Lab 1 output (lines 271-292)",
        "status": "PASS",
        "evidence": "c054: 'two projects, each with an outlay at t = 0 and one inflow at t = 1, all four amounts positive' is Theorem 4.1's set-up; the back's r* = dC/dK - 1 with dK nonzero and dC/dK positive is its statement. c056: the front names the flows -100,000, 230,000, -132,000 (L04 line 101), and the back's 'bisected to 0.100000 and 0.200000' and 'crossover 0.200000' are Lab 1 lines 281-282 and 292; grade C with basis Lab 1 is correct. c058: P's NPV at 5 per cent is -680.27 (recomputed: -100000 + 230000/1.05 - 132000/1.05^2 = -68027.2 cents = -680.27 dollars); IRRs 10 and 20 per cent (recomputed: both NPVs are zero); Corollary 2.2 is stated under Theorem 2.1, whose hypothesis is C0 < 0, Ct >= 0 and some Ct > 0 (L04 lines 75 and 79); the card's shorthand is an outlay followed by non-negative inflows, and P has a negative t = 2 flow, so it does not satisfy it. c060: NPV of P at 15 per cent is 189.04 (recomputed 189.036); the average of 10 and 20 is 15. c094: NPVs 18,181.82 for A and 27,272.73 for B at 10 per cent (recomputed 130000/1.1 - 100000 and 250000/1.1 - 200000) match Example 4.2 (L04 line 135).",
    },
    {
        "id": "r15-cards-numbers-and-grades",
        "check": "2.7 cards: the 103 cards after the rewrites (ids, fronts, grades, bases)",
        "location": "course/modules/CF/CF1/cards.json (103 entries: 74 T, 29 C)",
        "status": "PASS",
        "evidence": "Re-run round 15 with python -I: 103 entries, 103 unique ids, 103 unique fronts, every entry has a grade and a cite or basis. Lesson counts: L01 18, L02 17, L03 16, L04 20, L05 17, L06 15 (see cards-count-vs-plan).",
    },
    {
        "id": "r15-lab3-two-root-and-mc-numbers",
        "check": "2.2 numbers in prose: project.html line 373 (Lab 3 interpretation) and line 434 numbers after the round-15 rerun",
        "location": "course/modules/CF/CF1/project.html lines 373 and 424; tests/labs/CF1/lab-CF1-project-3.py",
        "status": "PASS",
        "evidence": "Recomputed by /tmp/CF1-v/d15/xcheck_mc.py from grader/reference.py: 15.3177 percent IRR (0.153177), 787 of 2,000 negative draws (39.35 percent: 787/2000 = 0.3935), standard deviation 2,445.52 over mean 885.85 = 2.76 (2445.52/885.85 = 2.7611). Line 424: NPV of the rung-1 project at 10 per cent is 926.00 (Lab 1 step 7), and each flow after t = 0 is positive (3150, 4000, 5000), so the NPV strictly falls with the rate and crosses zero once.",
    },
    {
        "id": "r15-irr-window-lab3-scope",
        "check": "2.4-math / 2.9 prose: 'Lab 3 searches only rates from −0.5 to 1.0' (project.html line 373)",
        "location": "course/modules/CF/CF1/project.html line 373; tests/labs/CF1/lab-CF1-project-3.py roots() (grid -0.5 to 1.0 step 0.0005)",
        "status": "PASS",
        "evidence": "The lab's roots() builds grid = [-0.5 + 0.0005 * k for k in range(3001)], so it searches rates from -0.5 to 1.0. The word 'only' is accurate for that function.",
    },
    {
        "id": "r15-mutants-r15e-new",
        "check": "2.6 mutation: three new student-error mutants written by this verifier",
        "location": "ledgers/CF1/mutants/r15e_01_fisher_real_rate_of_minus_one_accepted.py; r15e_02_monte_carlo_returns_draws_sorted.py; r15e_03_payback_fraction_from_discounted_cumulative_undiscounted.py; script /tmp/CF1-v/d15/make_mutants_r15e.py",
        "status": "PASS",
        "evidence": "tools/mutate_graders.py --unit CF1 --seeds 0-9 (output /tmp/CF1-v/d15/mutate2.out): 'KILLED r15e_01 ... -> test_fisher_rejects_rates_at_or_below_minus_one[real-minus-one] (seed 0)'; 'KILLED r15e_02 ... -> test_monte_carlo_draws_follow_the_seeded_gauss_stream (seed 0)'; 'KILLED r15e_03 ... -> test_discounted_payback_uses_discounted_flows (seed 0)'. Each is a plausible student error; each is caught.",
    },
    {
        "id": "r15-alternatives-three-new",
        "check": "2.6 / ruling (b): three new alternative correct engines pass the suite (over-constraint check)",
        "location": "/tmp/CF1-v/d15/alts/alt_r15e_a_irr_grid_cumulative_product.py, alt_r15e_b_monte_carlo_affine_in_multiplier.py, alt_r15e_c_payback_accumulate_next.py (generated by /tmp/CF1-v/d15/make_alts.py)",
        "status": "PASS",
        "evidence": "/tmp/CF1-v/d15/run_alts.py on the three engines: each 'PASS 50/50 seeds'. (a) IRR grid built by cumulative multiplication with exact window ends; (b) Monte Carlo from the affine identity a + b*m, with the same seeded draws; (c) payback from itertools.accumulate and next(). The three are not the reference's code paths and differ in numerical method.",
    },
    {
        "id": "r15-alternatives-rerun-all-prior",
        "check": "2.6 / ruling (b): all prior alternatives re-run",
        "location": "ledgers/CF1/scripts/*/alts/*.py (41 files, rounds 9 to 15; copied to /tmp/CF1-v/d15/allalts/)",
        "status": "PASS",
        "evidence": "/tmp/CF1-v/d15/run_alts.py /tmp/CF1-v/d15/allalts: 41 of 41 'PASS 50/50 seeds' (output /tmp/CF1-v/d15/allalts.out).",
    },
    {
        "id": "r15-tolerance-claims-carried-check",
        "check": "2.9 prose: 'the Monte Carlo mean equals a + b times the mean of the multipliers' (project.html line 209) against its test",
        "location": "course/modules/CF/CF1/project.html line 209; grader/test_project.py test_monte_carlo_mean_is_the_affine_identity_on_the_same_draws (line 802)",
        "status": "PASS",
        "evidence": "The test computes at_zero and at_one from the same flows and expected_mean = at_zero + (at_one - at_zero) * mean(multipliers), with the multipliers from random.Random(SEED) in the same order. This is the page's stated identity.",
    },
    {
        "id": "r15-banned-phrase-scan",
        "check": "2.9 banned phrases in the round-15 changed passages and the cards",
        "location": "course/modules/CF/CF1/project.html (lines 192, 405); cards.json (five rewritten entries); grader/test_project.py new comments",
        "status": "PASS",
        "evidence": "grep for roughly, 'about <digit>', historically, ellipsis, builder, verifier, round, unit report, build over project.html, cards.json and index.html: one hit, project.html line 188 'of about 600 to 900 words', which is the memo's length target from the specification, not a computed figure, so it is not a banned claim. No process words in the changed passages.",
    },
]


def mutants_from_output():
    out = []
    for line in MUT_OUT:
        if not line.startswith("KILLED "):
            continue
        body = line[len("KILLED ") :]
        name, rest = body.split(": ", 1)
        desc, killed = rest.rsplit(" -> ", 1)
        out.append(
            {
                "file": f"ledgers/CF1/mutants/{name}",
                "description": desc,
                "killed_by": killed,
            }
        )
    return out


rows = []
for row in PREV["rows"]:
    rid = row["id"]
    if rid in NEW:
        status, evidence = NEW[rid]
        new_row = dict(row)
        new_row["status"] = status
        new_row["evidence"] = evidence
        rows.append(new_row)
        continue
    new_row = dict(row)
    if row["status"] == "PASS":
        new_row["evidence"] = CARRY_PREFIX + row["evidence"]
    rows.append(new_row)
rows.extend(ROWS_NEW)

mutants = mutants_from_output()
registry_flags = PREV.get("registry_flags", [])

frag = {
    "unit": "CF1",
    "slice": "CF1-d",
    "round": 15,
    "verifier": "independent verifier (Haiku), round 15 of CF1 slice d (project page incl. case-memo rubric, grader, project labs, cards.json; project slice needs mutants)",
    "pin": "c093bf5 (detached, /tmp/verify15-CF1-d)",
    "base": "cef676e (round-14 pin); delta computed with git diff cef676e c093bf5 and read per hunk",
    "checkout": "/tmp/verify15-CF1-d",
    "scratch": "/tmp/CF1-v/d15",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": registry_flags,
    "freshness_flags": [],
    "notes": "Scripts: ledgers/CF1/scripts/CF1-d-r15/e/ (make_alts.py, make_mutants_r15e.py, run_alts.py, collect.py, xcheck_mc.py, build_fragment.py) and the outputs in ledgers/CF1/scripts/CF1-d-r15/e/out/. Mutants r15e_01..03 in ledgers/CF1/mutants/. registry_flags are carried unchanged: references/references.json is byte-identical since cef676e.",
    "summary": "",
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] != "PASS")
frag["summary"] = (
    f"CF1-d round 15: {len(rows)} rows, {n_pass} PASS, {n_fail} non-PASS (cards-count-vs-plan). "
    f"Mutants {sum(1 for m in mutants if m.get('killed_by'))}/{len(mutants)} killed. "
    "Previously failing rows r13-mutants-full-run, r14-mutant-r14v-01-rate-above-one-read-as-percent and "
    "index-ladder-rung1-worked-example now PASS. Collect count 138 and the 41 prior plus 3 new alternatives all pass."
)
out_path = CHECKOUT / "ledgers/CF1/CF1-d.json"
out_path.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", n_pass, "fail", n_fail, "mutants", len(mutants))
