import json, re, sys
ROOT = "/tmp/verify8-CF1-d"
old = json.load(open("/tmp/fanout-frags/CF1-d.round7.json"))
old_rows = {r["id"]: r for r in old["rows"]}

PROJ_DELTA = ("project.html lines 192, 205, 209, 213, 433 and grader/test_project.py lines 12, 197-216, 304, 307")
CARRY = ("Carried from round 7 (course/modules/CF/CF1/project.html and grader/test_project.py: cited subject byte-identical "
         "since the previous pin de53f7e; the round-8 delta hunks are " + PROJ_DELTA + "): ")
RERUN = "Re-run round 8 at 2c8162b: "
RECHECK = "Re-verified round 8 at 2c8162b (subject is in the delta or was re-read this round): "

def carry(i, extra=""):
    return CARRY + extra + old_rows[i]["evidence"]

# rows whose subject is in or next to the delta: re-verified this round
rows = {}
def add(i, status, evidence, check=None, location=None, fix=None):
    base = old_rows.get(i, {})
    r = {"id": i, "check": check or base.get("check", ""), "location": location or base.get("location", ""),
         "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows[i] = r

# ---- non-PASS and delta rows
add("proj-irr-window-end-intervals", "PASS", RECHECK +
    "project.html IRR bullet (line 206) states only a sign change between two samples inside the window is reported; "
    "the round-7 mutants m41 (last grid interval dropped) and m42 (first interval dropped) are KILLED on seed 0 by the new "
    "tests test_irr_finds_a_root_in_the_first_grid_interval (grader line 197) and test_irr_finds_a_root_in_the_last_grid_interval "
    "(line 207); reference passes both on 50 seeds (run_graders CF1 PASS 50/50).",
    location="course/modules/CF/CF1/project.html line 206 (IRR roots bullet); grader/test_project.py lines 197-216; ledgers/CF1/mutants/m41, m42")
add("proj-tolerance-rationale", "PASS", RECHECK +
    "The rationale 'that sum several products' is removed (project.html line 209 and grader docstring line 12 now say 'six named checks'). "
    "The six checks with the 1e-6 absolute floor are, by test function: depreciation shield (line 333), working-capital "
    "sum and year-1 flow (345), one-year project (360), working-capital flow in each year (369), real-rate NPV (394), "
    "Monte Carlo draws (501); each uses absolute=1e-6 or abs(total)<=1e-6. The page names exactly these groups.",
    location="course/modules/CF/CF1/project.html line 209 (Tolerances); grader/test_project.py lines 12, 333, 345, 360, 369, 394, 501")
add("proj-fisher-tolerance-zero-cases", "PASS", RECHECK +
    "Page line 209 says the Fisher identity holds to relative 1e-12 with absolute floor 1e-12, including at zero inflation and "
    "zero real rate. grader lines 304 and 307 now use rel=1e-12, absolute=1e-12; line 298 and 319 already do. Reference passes 50 seeds.",
    location="course/modules/CF/CF1/project.html line 209; grader/test_project.py lines 304, 307")
add("proj-tolerance-claim-note", "PASS", RECHECK +
    "Line 209 now states the tolerances the tests apply: relative 1e-9 with 1e-9 floor for NPVs (close() default, grader line 63), "
    "1e-6 floor in the six checks, 1e-9 times sum of absolute flows at IRR roots (line 226-227), 1e-12 Fisher, three standard errors "
    "with n-1 (grader line 'within three standard errors', using variance/(n-1)). Each claim matches its test.",
    location="course/modules/CF/CF1/project.html line 209; grader/test_project.py lines 63, 226-227, 298-308, 339-398, 510")
add("proj-test-count-72", "PASS", RERUN +
    "project.html line 192 says 'collects 76 checks'. pytest --collect-only on the reference (capbudget.py = reference.py) gives "
    "76 tests for QF_SEED 0 and for 49; in-browser page_smoke reports 'All 76 tests pass'. The claim 'the count does not depend on the "
    "seed' is correct; its stated cause is not (see proj-count-cause-wording).",
    location="course/modules/CF/CF1/project.html line 192 (Grading mode); grader/test_project.py")
add("proj-count-cause-wording", "FAIL", RERUN +
    "Line 192 says the count does not depend on the seed 'because every parametrize list in the file is a literal'. The count is "
    "seed-independent (76 at seeds 0 and 49), but not every parametrize list is a literal: grader/test_project.py lines 404-427 "
    "build entries from PROJECT (e.g. PROJECT['revenue'][:-1], PROJECT['cash_costs'][1:]). The accurate cause is that no list's length depends on the seed.",
    location="course/modules/CF/CF1/project.html line 192; grader/test_project.py lines 404-427",
    fix="Replace 'because every parametrize list in the file is a literal' with 'because no parametrize list's length depends on the seed'.")
add("proj-mutants-killed", "PASS", RERUN +
    "tools/mutate_graders.py --unit CF1 --seeds 0-9 over ledgers/CF1/mutants (47 files): 47 of 47 KILLED (output /tmp/cf1-v/d/r8/mutate.out).",
    location="ledgers/CF1/mutants/m01..m47; tools/mutate_graders.py")
add("proj-mutants-round7-new", "PASS", RERUN +
    "m41 and m42 (IRR grid drops an end interval) are KILLED by the new grader tests (see proj-irr-window-end-intervals); m43 "
    "(Fisher divides) and m44 (NPV discounts from period one) are KILLED by test_fisher_round_trip_is_exact and "
    "test_real_flows_at_the_real_rate_equal_nominal_flows_at_the_nominal_rate.",
    location="ledgers/CF1/mutants/m41..m44")
add("proj-mutants-round8-new", "PASS", RERUN +
    "NEW student-error mutants written this round, all KILLED on seed 0: m45_payback_strict_recovery_test (strict '>' so exactly zero "
    "is not recovered) by test_payback_ignores_flows_after_the_cut_off; m46_irr_bisection_stops_at_1e6 by "
    "test_irr_finds_both_roots_of_a_two_sign_change_flow; m47_fisher_inflation_unchecked (inflation of -1 accepted) by "
    "test_fisher_rejects_rates_at_or_below_minus_one[inflation]. Generator: ledgers/CF1/scripts/CF1-d-r8/make_mutants_r8.py.",
    location="ledgers/CF1/mutants/m45..m47; ledgers/CF1/scripts/CF1-d-r8/make_mutants_r8.py")
add("proj-sign-changes-convention", "PASS", RECHECK +
    "New Conventions bullet (project.html line 205): 'Read the flows in time order, skipping zero flows...'. Lab 1 step 6 prints "
    "flows -9000.00, 3150.00, 4000.00, 5000.00 (one sign change); lab-CF1-project-3 defines TWO_ROOT_FLOWS = [-100, 230, -132] "
    "(two sign changes; irr roots print [0.1, 0.2]). Both counts are correct under the definition.",
    location="course/modules/CF/CF1/project.html line 205; tests/labs/CF1/lab-CF1-project-1.py output step 6; tests/labs/CF1/lab-CF1-project-3.py line 24")
add("proj-irr-grid-close-pair-example", "PASS", RECHECK +
    "project.html line 206 example: NPV with roots 0.1 and 0.101 returns [] from irr_roots (reference, grid of 4,001 points); roots 0.1 and 0.11 "
    "return [0.10000000000003, 0.10999999999996]. Computed with ref.py via -I (/tmp/cf1-v/d/r8/grid_claims.py). Neighbour factor 1.0046158 "
    "in 1+r (page says 1.0046): correct to the stated digits.",
    location="course/modules/CF/CF1/project.html line 206")
add("proj-tolerance-six-checks-enumerated", "PASS", RECHECK +
    "Covered in proj-tolerance-rationale (six test functions with absolute 1e-6).",
    location="course/modules/CF/CF1/project.html line 209; grader/test_project.py lines 333-398, 501-513")
add("proj-named-errors-tax-share-one", "PASS", RECHECK +
    "Named-errors paragraph (line 213) says tax_rate and nwc_share at or above 1 are refused; grader parametrize entries tax-one "
    "(tax_rate 1.0) and share-one (nwc_share 1.0) at lines 417-420 expect ValueError; reference.py refuses share and tax at 1.0 (checks 0<=x<1).",
    location="course/modules/CF/CF1/project.html line 213; grader/test_project.py lines 417-420")
add("proj-named-errors-untested", "PASS", RECHECK +
    "Named-errors list (line 213) re-read in full: capex float, life, lengths, negative/non-finite, tax and share bounds, inflation, "
    "empty NPV, IRR (fewer than two flows; all zero), payback first flow, Monte Carlo draws and volatility. Each has a test in the "
    "parametrize lists (lines 404-432) or a named test (lines 233-290, 541-550).",
    location="course/modules/CF/CF1/project.html line 213; grader/test_project.py lines 233-290, 404-432, 541-550")
add("proj-spec-formulas-and-window", "PASS", RECHECK +
    "Conventions (lines 199-215) re-read in full: EBITDA, tax, shield, working capital, real flows, NPV, Fisher, sign changes (new), IRR "
    "window and grid, payback, Monte Carlo, tolerances. Formulas match reference.py after_tax_cash_flows, npv, payback_period, fisher_nominal, npv_monte_carlo.",
    location="course/modules/CF/CF1/project.html lines 199-215; grader/reference.py")
add("proj-error-message-unenforced", "PASS", RECHECK +
    "Constraints (line 190-192) say the autograder checks the exception type and the wording is not graded; must_raise (grader lines 54-60) "
    "checks only ValueError; the named-errors paragraph (line 213) says the same.",
    location="course/modules/CF/CF1/project.html lines 190-192, 213; grader/test_project.py lines 54-60")
add("proj-exemplar-numbers", "PASS", RECHECK +
    "Exemplars A and B re-read in full (lines 400-440). Numbers: 15.32 (15.3177 rounded), 2.37, 2.7535, 750, 1,865.14, 885.85, 2,445.52, "
    "54.68, 787/2,000 = 39.35 percent, -4,808.83, 13,800.44 all match the Lab 1 and Lab 3 printed outputs (run this round).",
    location="course/modules/CF/CF1/project.html lines 400-440")
add("proj-unrounded-gap-claim", "PASS", RECHECK +
    "Exemplar B section 4 (line 433): from unrounded values 925.9955 - 885.8457 = 40.1498 (925.99549 and 885.84568 from the "
    "lab's functions); 40.1498 / 54.6836 = 0.7342 (unrounded SE 54.68359; gap/SE 0.734220). Printed-value form 40.15 / 54.68 = 0.73 correct. "
    "Computed with ledgers/CF1/scripts/CF1-d-r7/unrounded_gap_r7.py run against 2c8162b.",
    location="course/modules/CF/CF1/project.html line 433; tests/labs/CF1/lab-CF1-project-3.py")
add("proj-hours-arithmetic-split", "PASS", RECHECK +
    "index.html data-hours-lessons 48 and data-hours-project 12; L01-L06 data-hours 8 each (6 x 8 = 48); project.html data-hours-project 12; "
    "48 + 12 = 60 and 12 / 60 = 20.0 percent (index.html line 41). Split matches.",
    location="course/modules/CF/CF1/index.html lines 29-41; L01-L06 data-hours; project.html line 33")
add("proj-hours-table", "PASS", RECHECK +
    "Time-budget table (lines 216-234) re-summed: 1 + 1 + 4 + 2 + 1 + 1 + 2 = 12, matching the total row and the page header.",
    location="course/modules/CF/CF1/project.html lines 216-234")
add("proj-lab1-twin-output", "PASS", RERUN +
    "tests/labs/CF1/lab-CF1-project-1.py run under python -I -W error (exit 0): step 6 flows -9000.00, 3150.00, 4000.00, 5000.00; NPV 926.00; "
    "shield PV 1865.14; matches page Lab 1 section (lines 56-131) and the walkthrough.",
    location="tests/labs/CF1/lab-CF1-project-1.py; course/modules/CF/CF1/project.html lines 56-131")
add("proj-lab2-completion-twin", "PASS", RERUN +
    "tests/labs/CF1/lab-CF1-project-2.py run (exit 0): flows and NPV 926.00 match the page's expected output (lines 134-179); the blanks are the tax, operating and working-capital lines.",
    location="tests/labs/CF1/lab-CF1-project-2.py; course/modules/CF/CF1/project.html lines 134-179")
add("proj-lab3-sanity-run", "PASS", RERUN +
    "tests/labs/CF1/lab-CF1-project-3.py run (exit 0): every printed line matches the page's Lab 3 output block (lines 249-375).",
    location="tests/labs/CF1/lab-CF1-project-3.py; course/modules/CF/CF1/project.html lines 249-375")
add("proj-lab3-recomputed-numbers", "PASS", RERUN +
    "Lab 3 output recomputed: IRR of rung-1 0.153177 (15.3177 percent); payback 2.37; discounted 2.7535; 2.76 = 2,445.52 / 885.85 (2.7606); 39.35 percent.",
    location="course/modules/CF/CF1/project.html lines 374, 434; tests/labs/CF1/lab-CF1-project-3.py")
add("proj-two-root-witness", "PASS", RERUN +
    "Two-root flow -100, 230, -132 has roots 0.1 and 0.2 (lab output [0.1, 0.2]); NPV at 0.15 is +0.2 and at 0 is -2 (computed), so the sign between the roots differs from outside: correct.",
    location="course/modules/CF/CF1/project.html line 374; tests/labs/CF1/lab-CF1-project-3.py line 24")
add("proj-lab2-docstring-claim", "PASS", RERUN +
    "tests/labs/CF1/lab-CF1-project-2.py docstring (unchanged since the round-7 pin; lab file byte-identical) describes the blanks as the page describes them.",
    location="tests/labs/CF1/lab-CF1-project-2.py lines 1-10; course/modules/CF/CF1/project.html lines 134-179")
add("proj-pytest-lab-helper", "PASS", RERUN +
    "tools/run_labs.py --unit CF1: PASS (9/9). Twins run under python -I -W error (exit 0).",
    location="tests/labs/CF1/*.py; tools/run_labs.py --unit CF1")
add("proj-grader-reference-50-seeds", "PASS", RERUN +
    "tools/run_graders.py --unit CF1 --seeds 0-49: PASS (reference 50/50 seeds, slowest 0.3 s).",
    location="tools/run_graders.py --unit CF1 --seeds 0-49")
add("proj-alternatives-correct", "PASS", RERUN +
    "Seven alternative correct engines run on seeds 0-49 with run_variants_r6.py (-I): reference (control) 0 of 50 failing; round-7 alts "
    "alt_r7_1 (Fraction payback), alt_r7_2 (20001-point grid, 60 halvings), alt_r7_3 (exp ratio multiplier) 0 of 50 each; new round-8 alts "
    "alt_r8_1 (Horner NPV, expanded Fisher r+i+ri), alt_r8_2 (geometric bisection in x with 1e-13 log stop), alt_r8_3 (math.fsum payback) "
    "0 of 50 each (ledgers/CF1/scripts/CF1-d-r8/alts; output /tmp/cf1-v/d/r8/variants.out).",
    location="ledgers/CF1/scripts/CF1-d-r8/alts/*.py; ledgers/CF1/scripts/CF1-d-r7/alts/*.py")
add("proj-mutant-tangent-survivor", "PASS", RERUN +
    "m09_tangent_root_reported and m24_tangent_within_tolerance_reported: KILLED (tools/mutate_graders.py, seeds 0-9).",
    location="ledgers/CF1/mutants/m09, m24")
add("proj-mutants-round4-new", "PASS", RERUN + "m25-m30 KILLED (mutate_graders 47/47).", location="ledgers/CF1/mutants/m25..m30")
add("proj-mutants-round5-new", "PASS", RERUN + "m31-m35 KILLED (mutate_graders 47/47).", location="ledgers/CF1/mutants/m31..m35")
add("proj-mutants-round6-new", "PASS", RERUN + "m37-m40 KILLED (mutate_graders 47/47).", location="ledgers/CF1/mutants/m37..m40")
add("proj-structure-and-gates", "PASS", RERUN +
    "tools/check_projects.py --all (CF1 PASS, AP1 PASS); tools/check_pages.py --all (CF1 PASS, AP1 PASS); tools/check_dag.py --all (CF1 PASS, AP1 PASS).",
    location="tools/check_projects.py, tools/check_pages.py, tools/check_dag.py --all")
add("proj-check-dag", "PASS", RERUN + "tools/check_dag.py --all: CF1 PASS.", location="tools/check_dag.py --all")
add("proj-page-smoke", "PASS", RERUN +
    "tools/page_smoke.py --unit CF1 --pages project: PASS; in-browser grader reports 'All 76 tests pass on seed 29674390'.",
    location="tools/page_smoke.py --unit CF1 --pages project")
add("proj-verify-refs", "PASS", RERUN +
    "tools/verify_refs.py --offline: 560 entries, 0 problems. tools/verify_refs.py --unit CF1 (live): 2 of 560 entries, 0 problems.",
    location="tools/verify_refs.py --offline; tools/verify_refs.py --unit CF1")
add("proj-ruff-format", "PASS", RERUN +
    "ruff check and ruff format --check on course/modules/CF/CF1/grader and tests/labs/CF1: 'All checks passed!', '13 files already formatted'.",
    location="course/modules/CF/CF1/grader; tests/labs/CF1")
add("proj-mypy-grader-gate", "PASS", RERUN +
    "mypy --no-incremental on the grader and labs: 'Success: no issues found in 13 source files'.",
    location="course/modules/CF/CF1/grader; tests/labs/CF1")
add("proj-banned-phrases", "PASS", RECHECK +
    "Scan of project.html, grader/test_project.py and cards.json for banned/process words (roughly, about, historically, typically, usually, "
    "generally, ellipsis, half, process, verifier, builder, round): only 'about 600 to 900 words' (a deliverable length), 'about' inside "
    "cards.json line 577 and project.html line 373/380 prose; no banned approximations; no process words in learner text.",
    location="course/modules/CF/CF1/project.html; grader/test_project.py; cards.json")
add("proj-cards-c071-not-established", "PASS", RECHECK +
    "CF1-c071 front (changed) 'Does the evidence in Section 4 establish how often firms use payback?' back 'No ... quotes no passage'. "
    "L05 Section 4 (lines 221-237) says the same: the evidence is 'an empirical question'; the lesson states no finding and quotes none.",
    location="course/modules/CF/CF1/cards.json CF1-c071; course/modules/CF/CF1/L05.html section 4")
add("proj-registry-graham-glasserman", "PASS", RECHECK +
    "Exemplar B section 5 (line 437) and references.json: graham2001theory container Journal of Financial Economics, volume 60, issue 2-3, pages 187-243 "
    "(matches the page); glasserman2003monte book title matches.",
    location="course/modules/CF/CF1/project.html Exemplar B section 5; references/references.json entries graham2001theory, glasserman2003monte")
add("cards-count-vs-plan", "FAIL", RECHECK +
    "plans/CF1-build-plan.md section 12 says 'the planner expects four to six per lesson'. cards.json (100 cards) has L01 18, L02 16, "
    "L03 15, L04 20, L05 16, L06 15: every lesson exceeds six. Unchanged from round 7 (the delta changed text, not counts).",
    location="plans/CF1-build-plan.md line 240; course/modules/CF/CF1/cards.json",
    fix="Trim each lesson's deck to four to six cards per plan section 12, or record an architect ruling changing that planned number.")
add("cards-missing-grade-or-basis", "PASS", RERUN +
    "Script: 100 cards, 0 with grade outside T/C or without basis or cite. 74 T, 26 C.",
    location="course/modules/CF/CF1/cards.json")
add("cards-duplicate-scan", "PASS", RERUN +
    "Script: 100 unique ids; no duplicate fronts; no duplicate backs.",
    location="course/modules/CF/CF1/cards.json")
add("cards-cite-keys-and-locators", "PASS", RECHECK +
    "Cited keys graham2001theory (CF1-c071) and glasserman2003monte (CF1-c084) are entries in references/references.json; card locators "
    "match L05 section 4 and L06 Remark 2.4 (both lessons read this round).",
    location="course/modules/CF/CF1/cards.json CF1-c071, CF1-c084; references/references.json")
add("cards-grade-semantics", "PASS", RERUN +
    "Counted: 74 T and 26 C in cards.json (matches old count). T cards cite a lesson Definition/Proposition/Theorem/Problem; C cards cite "
    "Lab 1, SIMULATED output or a source with no confirmed locator.",
    location="course/modules/CF/CF1/cards.json")
add("cards-prose-garbled-c067", "PASS", RECHECK +
    "CF1-c067 front changed to 'For conventional flows at a rate r of zero or more, within a horizon of N years, when is the discounted payback "
    "reached by year N?'; L05 Research problem R2 states the equivalence 'if and only if NPV(r) >= 0' under those conditions; card back matches.",
    location="course/modules/CF/CF1/cards.json CF1-c067; course/modules/CF/CF1/L05.html R2 (line 344-349)")
add("cards-numbers-in-lesson", "PASS", RECHECK +
    "The 12 changed cards (CF1-c001, c021, c033, c034, c065, c067, c071, c074, c084, c088, c097, c098) re-checked against L01-L06 text; the "
    "numbers on c074 (-132231.40, 289367.40), c097 (385535.69) and c098 (121251.71 to 693692.91) are printed by tests/labs/CF1/lab-CF1-L05-1.py "
    "(run this round, exit 0). The other 88 entries are byte-identical since de53f7e and were carried.",
    location="course/modules/CF/CF1/cards.json; tests/labs/CF1/lab-CF1-L05-1.py output")
add("cards-arithmetic-recomputed", "PASS", RECHECK +
    "CF1-c011 (NPV at 20 percent of -1000, 600, 600 = -83.33) and CF1-c016 (-1 + 1.05/1.06 = -0.009434; -1 + 1.05/1.03 = +0.019417) recomputed this round; "
    "CF1-c029 (3000 x 0.25 = 750). Other arithmetic cards byte-identical since de53f7e and carried.",
    location="course/modules/CF/CF1/cards.json CF1-c011, c016, c029")
add("cards-lab-derived-numbers", "PASS", RECHECK +
    "Lab-derived card numbers (CF1-c074, c097, c098) re-matched against tests/labs/CF1/lab-CF1-L05-1.py output this round; other lab-derived "
    "cards byte-identical since de53f7e and carried.",
    location="course/modules/CF/CF1/cards.json CF1-c074, c097, c098; tests/labs/CF1/lab-CF1-L05-1.py")
add("cards-misconception-locator", "PASS", RECHECK +
    "CF1-c011 (Section 7, first misconception of L01), c029 (Section 6, first misconception of L02), c072 and c085 (L05 Section 5 and L06 Section 5) "
    "re-read this round; the other misconception cards byte-identical since de53f7e and carried.",
    location="course/modules/CF/CF1/cards.json; L01-L06 misconception sections")
add("cards-changed-c071-c084", "PASS", RECHECK +
    "CF1-c071 and c084 fronts and backs re-checked against L05 Section 4 and L06 Remark 2.4 (current text): Glasserman named, no result stated; "
    "no normal-approximation claim is made by the lesson (Remark 2.4 says it is not proved, cited or graded).",
    location="course/modules/CF/CF1/cards.json CF1-c071, c084; L05.html Section 4; L06.html Remark 2.4")
add("cards-changed-c014-c037-c047-c057", "PASS", RECHECK +
    "CF1-c014, c037, c047, c057 re-read this round against the current L01, L03, L04 text: the cited passages (L01 Section 1, L03 Theorem 2.2, "
    "L04 Definition 1.1, Remark 5.1) are unchanged in substance by this round's lesson edits (L03 Remark wording for R1 and L04 meta description only).",
    location="course/modules/CF/CF1/cards.json CF1-c014, c037, c047, c057; L01-L04")
add("cards-changed-c016-c044-c051-c052", "PASS", RECHECK +
    "CF1-c016 (L01 R3), c044 (L03 Theorem 2.3), c051 and c052 (L04 Theorem 2.1, Corollary 2.2) re-read this round; numbers in c016 recomputed.",
    location="course/modules/CF/CF1/cards.json CF1-c016, c044, c051, c052")
add("cards-c080-positive-variance-dropped", "PASS", RECHECK +
    "CF1-c080 (L06 Problem P2) re-read; the card states the positive-variance and N >= 2 condition that the solution uses; unchanged.",
    location="course/modules/CF/CF1/cards.json CF1-c080; L06.html Problem P2")
add("cards-changed-c071-lesson-agreement", "PASS", RECHECK +
    "Lesson changes this round checked against the cards that cite those passages: L05 Proposition 2.2 now reads 'when both paybacks exist' and c065 "
    "says the same; L05 section 4 and the quiz item (L05q4) match c065/c071; L06 Remark 2.4 and Section 5 misconception match c084/c085.",
    location="course/modules/CF/CF1/L05.html Prop 2.2, section 4, L05q4; L06.html Remark 2.4; cards.json CF1-c065, c071, c084, c085")

add("proj-tolerance-relative-only", "PASS", RECHECK +
    "Tolerances bullet (line 209) states relative 1e-9 with absolute floor 1e-9 cents for NPVs and flows; close() default (grader line 63) is rel=1e-9, absolute=1e-9; "
    "the 1e-6 floor is used only in the six named checks, as the page says.",
    location="course/modules/CF/CF1/project.html line 209; grader/test_project.py line 63")
add("proj-memo-rubric-caption", "PASS", carry("proj-memo-rubric-caption", "Rubric table and caption outside the delta hunks (re-read this round): "))

# ---- carried rows (subject outside every delta hunk)
for i in ["proj-npv-empty-overconstraint", "proj-capex-float-overconstraint", "proj-capex-negative-untested",
          "proj-wc-timing-unenforced", "proj-exemplar-b-locator", "proj-rung1-step-line-wording", "proj-browser-storage-claim",
          "proj-must-raise-text-claim", "proj-exemplar-b-crossing-claim", "proj-never-prints-or-mutates-unenforced",
          "proj-tangent-root-claim", "proj-tangent-endpoint-reported", "proj-mc-draw-method-unenforced",
          "proj-exemplar-a-quote", "proj-about-39-percent", "proj-registry-reading-list", "proj-high-end-test-spec-justified",
          "proj-equivalent-mutant-proof", "proj-lessons-cross-ref", "proj-irr-close-roots-missed",
          "proj-irr-grid-convention-unenforced", "proj-irr-window-unenforced", "proj-ladder-skip-condition",
          "proj-window-end-high-unenforced", "proj-irr-window-high-end-cover", "proj-stdlib-and-no-instance-import-unenforced"]:
    add(i, "PASS", carry(i))

# carried card rows that are not in the delta
for i in ["cards-misconception-locator"]:
    pass

# ---- re-check of remaining carried project rows
rows_order = [r["id"] for r in old["rows"]]
for i in rows_order:
    if i not in rows:
        raise SystemExit("missing override for " + i)

extra_new = [
    ("proj-sign-changes-convention", None), ("proj-irr-grid-close-pair-example", None),
]
ordered = [rows[i] for i in rows_order] + [rows[i] for i in rows if i not in rows_order]
for r in ordered:
    if not r.get("check"):
        r["check"] = old_rows.get(r["id"], {}).get("check", r["id"])

# mutants
mut_out = open("/tmp/cf1-v/d/r8/mutate.out", encoding="utf-8").read().splitlines()
mutants = []
for line in mut_out:
    m = re.match(r"KILLED (m\d\d)_[^:]*\.py: (.*) -> (.*)$", line)
    if m:
        mutants.append({"file": "ledgers/CF1/mutants/" + line.split(" ", 1)[1].split(":", 1)[0],
                        "description": m.group(2), "killed_by": m.group(3)})
assert len(mutants) == 47, len(mutants)

frag = {
    "unit": "CF1", "slice": "CF1-d", "round": 8,
    "verifier": "Claude Haiku 5.5 (independent verifier, CF1-d round 8; did not build CF1; no shared context with builders or earlier verifiers)",
    "pin": "2c8162b (detached, /tmp/verify8-CF1-d); delta since the round-7 pin de53f7e",
    "base": "de53f7e (round-7 pin; previous fragment /tmp/fanout-frags/CF1-d.round7.json). Delta in slice: project.html lines 192 (Grading mode, 76 checks), 205 (new Sign changes bullet), 209 (Tolerances), 213 (Named errors), 433 (Exemplar B, 4 Uncertainty); grader/test_project.py line 12 (docstring), lines 197-216 (two new IRR tests), lines 304 and 307 (Fisher tolerance); cards.json (12 cards: CF1-c001, c021, c033, c034, c065, c067, c071, c074, c084, c088, c097, c098: front/back wording and number formatting only); lessons L01-L06 wording (context; checked where a card or the page cites them); index.html lines 41, 68, 151, 161 (hub wording; hours split checked, other lines outside the slice).",
    "checkout": ROOT, "scratch": "/tmp/cf1-v/d/r8", "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": ordered,
    "mutants": mutants,
    "registry_flags": [
        "glasserman2003monte: used_by lists M8 only; CF1 cites it (project.html Exemplar B section 5, L06 Remark 2.4, cards CF1-c084). Unchanged since round 7; add CF1 with tools/add_reference.py or confirm the architect's ruling.",
        "damodaran2012investment: used_by lists CF4 only; CF1 lists it in the project reading list (project.html reading section). Unchanged since round 7."
    ],
    "freshness_flags": [],
    "notes": ("Commands run this round on the pin 2c8162b: run_graders --unit CF1 --seeds 0-49 (PASS 50/50); run_labs --unit CF1 (9/9); "
              "mutate_graders --unit CF1 --seeds 0-9 (47/47 killed; output /tmp/cf1-v/d/r8/mutate.out); run_variants_r6.py over 7 alternative engines "
              "(0 failing of 50 each; variants.out); pytest --collect-only on seeds 0 and 49 (76 each); page_smoke --unit CF1 --pages project (PASS); "
              "check_projects, check_pages, check_dag --all (PASS); ruff check and format --check and mypy --no-incremental on grader and labs (PASS); "
              "verify_refs --offline (560, 0 problems) and --unit CF1 live (2 of 560, 0 problems); run_labs twins under python -I -W error (exit 0); "
              "grid_claims.py (grid examples); unrounded_gap_r7.py; cards checks (100 cards: grade/basis, duplicates, 74 T / 26 C); "
              "lab-CF1-L05-1 output for card numbers. Not run: the full repository gate; pytest over tests/ beyond run_labs; browser tests beyond page_smoke; "
              "the lab twins of the lessons except for the card-cited numbers. Not judged: index.html wording other than the hours split; lesson prose beyond "
              "the passages cited by cards or the page; hours design targets (architect ruling). Carried rows use per-subject byte identity against de53f7e. "
              "Note: the grader's 'Monte Carlo SE uses n-1' is checked only by the mean test (not by an engine-level mutant, since the SE is computed in the test)."),
    "summary": ("CF1-d round 8: FAIL. Resolved from round 7: proj-irr-window-end-intervals (m41, m42 now killed by the two new grid-end tests), "
                "proj-tolerance-rationale and proj-tolerance-claim-note (rationale removed; six 1e-6 checks enumerated correctly), "
                "proj-fisher-tolerance-zero-cases (rel and absolute 1e-12 at zero inflation and zero real rate), proj-mutants-killed and "
                "proj-mutants-round7-new (47 of 47 killed). New FAIL: proj-count-cause-wording (the 76-check count is seed-independent, but the stated cause "
                "'every parametrize list is a literal' is wrong: lines 404-427 build entries from PROJECT). Still FAIL: cards-count-vs-plan "
                "(100 cards; 15 to 20 per lesson against the plan's four to six)."),
}
# compute verdict as the ledger does: PASS only if every row is PASS
frag["verdict"] = "PASS" if all(r["status"] == "PASS" for r in ordered) else "FAIL"
json.dump(frag, open(ROOT + "/ledgers/CF1/CF1-d.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(ordered), "non-PASS", [r["id"] for r in ordered if r["status"] != "PASS"], "mutants", len(mutants))
