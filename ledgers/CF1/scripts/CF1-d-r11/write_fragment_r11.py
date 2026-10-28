"""Write the round-11 CF1-d fragment from the round-10 rows plus this round's evidence.

Usage (run with -I): write_fragment_r11.py <checkout> <round10 fragment> <mutate output>
Carried rows keep their id and get the 'Carried from round 10' prefix only when the cited subject is unchanged
in the diff af08ad1..91946cf (checked with git diff -U0). Every other row gets evidence written this round.
"""

import json
import pathlib
import re
import sys

CHECKOUT = pathlib.Path(sys.argv[1])
PREV = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
MUT_OUT = pathlib.Path(sys.argv[3]).read_text(encoding="utf-8").splitlines()
PREFIX = "Carried from round 10 (cited subject byte-identical since the previous pin af08ad1, checked with git diff -U0): "
S = "ledgers/CF1/scripts/CF1-d-r11/"

FRESH = {
    "proj-test-count-72": ("PASS", "project.html line 192 states 118 checks. Re-counted this round: runone.py collect and collect_seeds.py (scripts CF1-d-r11) give '118 tests collected' for QF_SEED 0, 1, 7, 49 and 134675774 on the reference solution."),
    "proj-count-cause-wording": ("PASS", "project.html line 192: the count does not depend on the seed because no parametrize list's length depends on the seed. Confirmed: collect_seeds.py gives 118 on five seeds; the two parametrize lists (grader/test_project.py lines 476-480 and 712-716) are literal tuples, not seed-derived."),
    "proj-collect-count-50-seeds": ("PASS", "Count 118 on every seed tried (collect_seeds.py, scripts CF1-d-r11); run_graders.out: reference 50/50 seeds PASS for seeds 0-49."),
    "proj-page-smoke": ("PASS", "page_smoke_project_full.out (tools/page_smoke.py --unit CF1 --pages project): lab lab-CF1-project-1/2/3 run, 'in-browser grader: All 118 tests pass on seed 872856147', page_smoke modules/CF/CF1/project.html: PASS, page_smoke CF1: PASS."),
    "proj-named-errors-untested": ("PASS", "project.html line 213 (Named errors) now includes 'a payback with fewer than two flows'. grader/test_project.py test_payback_rejects_fewer_than_two_flows (parametrized empty, outlay-only) enforces it; reference.py raises ValueError for both (runone.py check, check_claims.py). Other named errors are enforced by the parametrized invalid-project and must_raise tests as in round 10."),
    "proj-named-errors-tax-share-one": ("PASS", "project.html line 213: tax rate 1.0 and share 1.0 refused, 0 valid. grader test_invalid_project_raises_a_named_error[tax-one] and the share-one parameter; mutants fix9_01 (tax-one) killed in mutate_all_r11.out."),
    "proj-mutants-killed": ("PASS", "mutate_all_r11.out (tools/mutate_graders.py --unit CF1 --seeds 0-9): every mutant in ledgers/CF1/mutants/ except m58 is KILLED, including m01-m57 and fix9_01-10, fix10_01-10. m58 is a FAIL row of its own (proj-mutant-m58-zero-flow-time-index)."),
    "proj-mutants-round9-new": ("PASS", "mutate_all_r11.out: m48-m53 KILLED (seed 0)."),
    "proj-mutants-round10-new": ("PASS", "mutate_all_r11.out: m54-m57 KILLED (seed 0)."),
    "proj-alternatives-correct": ("PASS", "run_graders-style re-run this round: all 15 engines in ledgers/CF1/scripts/CF1-d-r9/alts and CF1-d-r10/alts pass seeds 0-4 on the round-11 grader (runone.py solve); see variants run in this round."),
    "proj-alternatives-round10": ("PASS", "ledgers/CF1/scripts/CF1-d-r10/alts/alt_r10_1..5: PASS on seeds 0-4 on the round-11 grader (runone.py solve)."),
    "proj-mc-mean-three-se-false-failure": ("PASS", "Carried from round 10 (the test body of test_monte_carlo_mean_is_the_affine_identity_on_the_same_draws and project.html line 209 are byte-identical since af08ad1; the grader lines moved by the round-11 insertions above them): the test is in grader/test_project.py and passes on the reference (runone.py solve, seeds 0-2) and on alt_r11_3."),
    "proj-banned-phrases": ("PASS", "Grep over project.html, L01.html, L02.html, L05.html, L06.html, index.html and cards.json for roughly, historically, typically, usually, generally, '...', 'about 6', builder, verifier, REQUEST: no hits in the changed passages. Matches for 'round' are the concept names 'round late' (L01 Remark 1.3) and 'round the factor last' (L01 Remark 5.2), which predate this round."),
    "proj-process-words-r10": ("PASS", "Process-word grep (builder, verifier, round, REQUEST) over project.html, L01.html, L02.html, cards.json: no process words in the changed text; the only 'round' matches are the concept names above."),
    "proj-tolerance-six-checks-enumerated": ("PASS", "project.html line 209 (Tolerances) says 'Nine checks use an absolute floor of 1e-6 cents'. Counted this round: absolute=1e-6 usages in grader/test_project.py at the functions test_depreciation_shield..., test_working_capital_investment_and_recovery..., test_single_year_project..., test_working_capital_flow_in_each_year..., test_real_flows_at_the_real_rate..., test_tax_credit_is_paid_when_ebitda_is_zero..., test_monte_carlo_draws..., test_monte_carlo_mean... (eight functions; the working-capital function holds two checks): nine checks."),
    "proj-irr-grid-close-pair-example": ("PASS", "project.html line 209/207 example recomputed (check_claims.py, scripts CF1-d-r11): flows -100, 220.1, -121.11 have roots 0.1 and 0.101 (exact 0.1000000000001 and 0.10099999999987), and reference irr_roots returns [] for them; flows -100, 221, -122.1 return [0.1000000000000123, 0.10999999999999743]. Grid ratio 1e8**(1/4000) = 1.0046158 matches the page's 1.0046158 (5 dp 1.00462)."),
    "proj-spec-formulas-and-window": ("PASS", "Carried from round 10 (project.html line 207 and grader/reference.py byte-identical): the window and grid were recomputed this round (grid ratio 1.0046158; sample k=1000 is x=0.01, rate 99, check_claims.py)."),
    "proj-structure-and-gates": ("PASS", "check_projects.out, check_pages.out, check_dag.out (round 11): check_projects CF1 PASS, check_pages CF1 PASS, check_dag CF1 PASS; mypy.out 'Success: no issues found in 13 source files'; ruff.out 'All checks passed!' and '13 files already formatted'."),
    "proj-ruff-format": ("PASS", "ruff.out (round 11): ruff check course/modules/CF/CF1/grader tests/labs/CF1 'All checks passed!'; ruff format --check: 13 files already formatted."),
    "proj-mypy-grader-gate": ("PASS", "mypy.out (round 11, mypy --no-incremental course/modules/CF/CF1/grader tests/labs/CF1): Success: no issues found in 13 source files."),
    "proj-verify-refs": ("PASS", "verify_refs_offline.out: 560 entries, 0 problems. verify_refs_cf1_live.out: live re-verification of CF1: 2 of 560 entries, 0 problems."),
    "proj-check-dag": ("PASS", "check_dag.out (round 11): check_dag CF1: PASS."),
    "proj-page-smoke-labs": ("PASS", "page_smoke_project_full.out: labs lab-CF1-project-1, -2, -3 run in the browser; in-browser grader 118 of 118 pass on seed 872856147."),
    "proj-run-labs": ("PASS", "run_labs.out (round 11): run_labs CF1: PASS (9/9); each CF1 twin run under python -I -W error exits 0 and matches its round-10 copy (twin_lab-CF1-*.out)."),
    "cards-missing-grade-or-basis": ("PASS", "cards_scan.py (round 11, run -I): every card has grade T or C (74 T, 26 C), and every card has a cite or basis; cards.json changed only at CF1-c012, which keeps grade T and basis."),
    "cards-duplicate-scan": ("PASS", "cards_scan.py: duplicate ids [], duplicate fronts [], ids sequential CF1-c001..c100; and a backs-duplicate scan (python -I) gives none."),
    "cards-cite-keys-and-locators": ("PASS", "cards_scan.py: 'cite keys missing from registry []'. cite keys unchanged this round except the c012 text."),
    "cards-numbers-in-lesson": ("PASS", "Re-run this round (python -I): every number in every card's front and back appears in its lesson HTML (0 misses over 100 cards)."),
    "cards-grade-semantics": ("PASS", "Grades re-counted this round: T 74, C 26. CF1-c012 (T) rests on Proposition 3.1, which is a T result in L01.html line 98; the new back text states only the Proposition's conclusion for C0 < 0."),
    "cards-count-vs-plan": ("FAIL", "Re-counted this round (cards_scan.py): 100 cards, per lesson L01 18, L02 16, L03 15, L04 20, L05 16, L06 15. plans/CF1-build-plan.md section 12 (line 240) says 'the planner expects four to six per lesson'. Every lesson is 2.5 to 5 times that expectation; no change to the plan or cards this round."),
    "cards-c012-npv-falls-scope": ("PASS", "cards.json CF1-c012 (back: 'For a conventional stream with a negative date-0 outlay (C_0 < 0), NPV falls strictly as the rate rises and tends to C_0 (Proposition 3.1)') agrees with L01.html Proposition 3.1 (lines 95-102: conventional = C_t >= 0 for t>=1 with one positive, strictly decreasing, tends to C_0), with Remark 3.2 (line 111) and the table row at line 459. Consequence checked: with C_0 < 0 the NPV tends to a negative limit, so a positive NPV at a low rate is negative at some higher rate, as the card says."),
    "cards-c065-payback-basis": ("PASS", "Carried from round 10 (cards.json entry CF1-c065 and L05.html line 86 byte-identical since af08ad1)."),
    "cards-changed-c071-lesson-agreement": ("PASS", "cards.json CF1-c071 back: 'It states no finding from its registered source on corporate practice, Graham and Harvey (2001)'. Agrees with L05.html line 233 ('This lesson states no finding from it') and the changed meta description line 7 ('why this lesson states no finding on firm practice'). The registry title of graham2001theory is 'The theory and practice of corporate finance: evidence from the field' (references/references.json)."),
    "cards-changed-c071-c084": ("PASS", "Carried from round 10 (cards.json CF1-c071 and CF1-c084 byte-identical since af08ad1); checked again against L05 line 233 and 236 (line 236 changed to 'read the registered source'; card c071 does not quote it)."),
    "cards-misconception-locator": ("PASS", "cards.json: no card carries a misconception locator field; each card with a misconception basis points to a lesson section. L01.html misconception list (line 335-338) changed in wording only; the misconception still exists and its 'Lab 1, Part A' numbers agree with L01 line 407 and the L01 lab output (7000.00 at 0.00, -46.94 at 0.20)."),
    "lesson-l01-conventional-rewrites": ("PASS", "Changed passages re-verified this round: L01.html line 111 (Remark 3.2), line 322 (rate-is-an-input bullet: 'NPV falls as r rises, so with a negative date-0 outlay the decision can change with r'; numbers 1,211.49 at 0.15 and -46.94 at 0.20 match tests/labs/CF1 lab-CF1-L01-1 output lines 6-7), line 338 (misconception: conventional stream with negative date-0 outlay; prints 7,000.00 at 0.00 and -46.94 at 0.20, matching the lab output lines 3 and 7), line 439 (R2 solution: 'Corollary 4.2 supports ranking by NPV under Assumption 4.0'; Corollary 4.2 at line 137-138 states the larger NPV leaves more cash at period 0 under Assumption 4.0). Lines 7, 51, 174-175, 371, 407 are byte-identical since af08ad1 (carried)."),
    "lesson-l02-canon-earnings-claim": ("PASS", "L02.html line 280 now reads 'The lab takes revenue and cash cost as its inputs and does not start from net income.' L02 Lab 2 code (lines 217-219 per the round-10 row, unchanged) builds ebitda = revenue - cash cost, ebit = ebitda - depreciation, tax = rate * ebit, ocf = ebit - tax + depreciation: revenue and cash cost are the inputs and no net-income line is computed. The round-10 FAIL (claim 'uses no earnings line' against EBIT) is withdrawn by this rewrite."),
    "lesson-l02-references-concept-claim": ("PASS", "L02.html line 508 (References) now says EBITDA and EBIT (Section 2), operating cash flow (Definition 2.1) and net working capital (Definition 3.1) are defined in its text, and that NPV is defined in Lesson 1 (<a href=L01.html#def-net-present-value>Definition 1.1</a>). Checked: L02 Section 2 defines EBITDA/EBIT (line 85-91), Definition 2.1 is at line 90, Definition 3.1 is in Section 3 (line 122 per the round-10 row), L01.html line 57-59 is 'Definition 1.1 (net present value)' with id def-net-present-value. Concepts accrual-accounting, balance-sheet, depreciation-and-amortization remain in AC1 (carried)."),
    "lesson-l02-accrual-definition": ("PASS", "Carried from round 10 (the accrual-accounting definition sentence of L02.html line 280 and AC1 course/modules/AC/AC1/L01.html def-accrual-accounting, byte-identical since af08ad1; the edited second sentence of the same bullet is re-verified under lesson-l02-canon-earnings-claim)."),
    "lesson-l05-rewrites": ("PASS", "Changed lines re-verified: L05.html line 7 meta description ('why this lesson states no finding on firm practice') agrees with section 4 (line 233). Line 236 now reads 'read the registered source, locate the passage, and then grade the claim it supports' and is consistent with the registry record of graham2001theory. Lines 107 and 117 are byte-identical since af08ad1 (carried)."),
    "lesson-l06-rewrites": ("PASS", "L06.html line 223 now reads 'Propositions 2.1 and 2.3 hold for the model they are stated for. The limits below concern the model and its inputs, except the quantile bullet, which concerns the estimator.' Checked against the bullets at lines 226-228: the independence bullet and the sampling-error bullet concern the model and its inputs; the tail-quantile bullet (line 228) concerns the estimator, as stated. Lines 129, 138, 147 are byte-identical since af08ad1 (carried)."),
    "index-card-and-hub-wording": ("PASS", "index.html lines 140 and 142 (card titles): 'Inflation and Real Cash Flows' matches L03.html h1 (line 35); 'Payback and What Firms Actually Use' matches L05.html h1 (line 36); the card bodies agree with the L05 section 4 wording ('no finding stated') and with cards CF1-c071. The rest of the card block is byte-identical since af08ad1 (carried)."),
    "index-ladder-rung1-worked-example": ("FAIL", "Re-verified this round (still FAIL). The hub ladder is index.html line 151 (not 161): rung 1 'Worked example' reads 'A year-1 worked after-tax operating cash flow and working-capital line on a small project ... Lab 2 prints the later years and the NPV of the same project.' The project page rung 1 is Lab 1 (project.html lines 42-44 and 56-131): a three-year SIMULATED project that prints every year's flow (twin_lab-CF1-project-1.out lines 4-6) and an NPV of 926.00 at 10 percent (step 7). The completion problem Lab 2 (project.html line 135) prints the later years and the NPV only as its expected output after the blanks are filled (twin_lab-CF1-project-2.out). The hub's rung 1 description is a different exercise from Lab 1."),
    "lesson-l02-why-section3-ref": ("PASS", "Carried from round 10 (L02.html line 48 and the Section 3 heading line 119 and Definition 3.1 line 122 byte-identical since af08ad1)."),
    "lesson-l02-rewrites": ("PASS", "Carried from round 10 (L02.html lines 67, 76, 85, 94 byte-identical since af08ad1; the changed lines 280 and 508 are re-verified under their own rows)."),
    "lesson-l02-r1-same-period-fraction": ("PASS", "Carried from round 10 (L02.html lines 385-390 byte-identical since af08ad1)."),
    "proj-exemplar-b-evidence-line": ("PASS", "Carried from round 10 (project.html line 436 byte-identical since af08ad1)."),
}

NEW_ROWS = [
    {
        "id": "proj-mutant-m58-zero-flow-time-index",
        "check": "2.6 mutation: student error that drops zero flows before discounting in npv (new this round)",
        "location": "course/modules/CF/CF1/project.html line 209 (Conventions, Net present value: 'the sum over t of the flow at t divided by (1 + r) ** t'); grader/test_project.py (no npv test with a zero flow)",
        "status": "FAIL",
        "evidence": "ledgers/CF1/mutants/m58_npv_drops_zero_flows_from_the_time_index.py (a complete capbudget module, the reference with npv = sum over the nonzero flows, enumerated from zero) SURVIVES all of seeds 0-9 (mutate_all_r11.out). Witness: npv(0.1, [-100, 0, 121]): reference -1.4e-14 (= 0), m58 9.999999999999986 (= 10). The spec sentence 'the sum over t of the flow at t divided by (1 + r) ** t' fixes the time index of a zero flow, so the mutant violates a stated behaviour and the suite does not test it.",
        "fix": "Add to grader/test_project.py: def test_npv_keeps_a_zero_flow_in_its_time_index(): assert abs(npv(0.1, [-100.0, 0.0, 121.0])) <= 1e-9 with a message citing the Net present value bullet; re-run mutate_graders --unit CF1 (m58 must be killed)."
    },
    {
        "id": "proj-mutants-round11-new",
        "check": "2.6 mutation: two new student-error mutants m59 and m60 (project slice)",
        "location": "ledgers/CF1/mutants/m59_monte_carlo_reseeds_at_seed_plus_draw_index.py; ledgers/CF1/mutants/m60_fisher_nominal_clamped_at_zero.py; generator ledgers/CF1/scripts/CF1-d-r11/make_alts_and_mutants_r11.py",
        "status": "PASS",
        "evidence": "mutate_all_r11.out: 'KILLED m59 ... -> test_monte_carlo_draws_follow_the_seeded_gauss_stream (seed 0)' and 'KILLED m60 ... -> test_fisher_round_trip_is_exact (seed 0)'. Both errors are named by the spec: the single seeded stream random.Random(seed).gauss (project.html line 209, Monte Carlo NPV) and the exact Fisher identity (line 209, The Fisher relation)."
    },
    {
        "id": "proj-alternatives-round11",
        "check": "2.6 alternatives: five new correct implementations (over-constraint probe)",
        "location": "ledgers/CF1/scripts/CF1-d-r11/make_alts_and_mutants_r11.py (alt_r11_1..5 written to the round-11 scratch dir)",
        "status": "PASS",
        "evidence": "runone.py solve on seeds 0-9: alt_r11_1_npv_horner_from_last_flow (Horner from the last flow), alt_r11_2_payback_fsum_prefix_cutoff (fsum prefix sums with cutoff -1e-9), alt_r11_3_monte_carlo_affine_identity (NPV as a + b*m), alt_r11_4_fisher_expanded_sum (real + inflation + real*inflation), alt_r11_5_operating_flow_algebraic_form (EBITDA*(1-tax) + depreciation*tax): 10 of 10 PASS each."
    },
    {
        "id": "proj-grader-new-tests-r11",
        "check": "2.4 grader tests added this round are justified by the spec and pass the reference",
        "location": "course/modules/CF/CF1/grader/test_project.py: test_irr_zero_flow_keeps_its_place_in_the_time_index, test_irr_root_on_a_grid_sample_is_reported_once, test_discounted_payback_is_infinite_when_only_the_undiscounted_flows_recover, test_payback_rejects_fewer_than_two_flows, test_tax_rate_just_below_zero_is_refused, test_working_capital_share_just_below_zero_is_refused, test_revenue_just_below_zero_is_refused, test_real_flows_are_deflated_under_negative_inflation, test_monte_carlo_refuses_zero_draws, test_monte_carlo_refuses_a_rate_at_or_below_minus_one, test_monte_carlo_refuses_a_volatility_just_below_zero",
        "status": "PASS",
        "evidence": "Each new test's expected value re-derived: NPV = -100 + 110/(1+r)^2 has root sqrt(1.1)-1 = 0.0488088 (reference returns 0.04880884817); discounted flows 41.67 and 41.67 at 20 percent give cumulative -16.67 (payback inf, reference matches); grid sample k=1000 of 4000 gives x = 0.01, rate 99 (1e-4 * 100). The spec states each rule: IRR roots by sign change on the 4,001-point grid (project.html line 207), payback inf (line 208), 'tax rate at least 0' (line 189), 'inflation above -1' and negative inflation deflation (line 194 and Real flows bullet), Monte Carlo 'fewer than two draws' and volatility (line 213). Reference passes all of them (run_graders 50/50; runone.py collect 118); alt_r11_1..5 pass."
    },
    {
        "id": "proj-tolerance-nine-recount",
        "check": "2.9 numbers in prose: 'Nine checks use an absolute floor of 1e-6 cents' (project.html line 209)",
        "location": "course/modules/CF/CF1/project.html line 209; grader/test_project.py lines 411, 421, 427, 436, 450, 470, 600, 671, 705",
        "status": "PASS",
        "evidence": "Re-counted this round with awk over the file: absolute=1e-6 at lines 411 (depreciation shield), 427 (working-capital sum/year-1 flow), 436 (one-year project), 450 (working-capital flow each year), 470 (real-rate NPV), 600 (zero-EBITDA tax credit), 671 (Monte Carlo draws), 705 (Monte Carlo mean); the abs-floor for the working-capital sum at line 421 is in the same function as line 427. Nine checks named in the spec."
    },
    {
        "id": "proj-spec-count-118-hub",
        "check": "2.9 figure quoted in prose: 'collects 118 checks' (project.html line 192)",
        "location": "course/modules/CF/CF1/project.html line 192 (Grading mode)",
        "status": "PASS",
        "evidence": "Recounted this round: 118 tests collected (runone.py collect; collect_seeds.py for five seeds). The figure matches the page."
    },
]

# carried rows whose cited subject is outside the changed lines (see git diff -U0 hunks)
rows = []
for row in PREV["rows"]:
    rid = row["id"]
    if rid in FRESH:
        status, evidence = FRESH[rid]
        new = dict(row)
        new["status"] = status
        new["evidence"] = evidence
        if status != "PASS":
            new["fix"] = row.get("fix", "see evidence")
        else:
            new.pop("fix", None)
        rows.append(new)
        continue
    if rid in {"index-ladder-rung1-worked-example", "cards-count-vs-plan"}:
        continue  # handled in FRESH
    new = dict(row)
    new["evidence"] = PREFIX + row["evidence"]
    new.pop("fix", None)
    rows.append(new)

for extra in NEW_ROWS:
    rows.append(extra)

# fixed FAIL rows get their fix text from the round-10 row (index and cards)
fixes = {r["id"]: r.get("fix") for r in PREV["rows"]}
for r in rows:
    if r["status"] == "FAIL" and not r.get("fix"):
        r["fix"] = fixes.get(r["id"]) or "see evidence"
r_index = [r for r in rows if r["id"] == "index-ladder-rung1-worked-example"][0]
r_index["fix"] = ("Rewrite index.html lines 151-152 (the project ladder): rung 1 = 'Lab 1 on the project page: a three-year "
                  "SIMULATED machine project, every year's flow and the NPV at 10 percent (926.00 dollars)'; rung 2 = "
                  "'Lab 2 on the project page: the after-tax cash-flow line of that same project with its three blanks'.")
r_index["location"] = "course/modules/CF/CF1/index.html line 151 (The project ladder, Worked example); course/modules/CF/CF1/project.html lines 42-44 (Rung 1) and lines 56-131 (Lab 1)"

mutants = []
for line in MUT_OUT:
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    path = f"ledgers/CF1/mutants/{name}"
    mutants.append({
        "file": path,
        "description": desc,
        "killed_by": killed if status == "KILLED" else "SURVIVED: no test on seeds 0-9 (see proj-mutant-m58-zero-flow-time-index)",
    })

frag = {
    "unit": "CF1",
    "slice": "CF1-d",
    "round": 11,
    "verifier": "independent verifier (Haiku), round 11 of the CF1 slice d (project page, grader, project labs, cards)",
    "pin": "91946cf (detached, /tmp/verify11-CF1-d)",
    "base": "af08ad1 (round-10 pin, delta computed with git diff -U0 af08ad1 91946cf)",
    "checkout": "/tmp/verify11-CF1-d",
    "scratch": "/tmp/CF1-v/d11",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": PREV.get("registry_flags", []),
    "freshness_flags": [],
    "notes": (
        "Delta af08ad1..91946cf for this slice: project.html lines 192 (count 106 to 118) and 213 (payback clause); "
        "grader/test_project.py +77 lines in four insertions (no deletions); cards.json CF1-c012 only; L01 lines 111, 322, 338, 439; "
        "L02 lines 280, 508; L05 lines 7, 236; L06 line 223; index.html lines 140, 142. tests/labs/CF1 and plans unchanged. "
        "Carried rows cite lines outside these hunks or grader test functions whose bodies are unchanged (insertions only). "
        "Commands run this round (outputs in ledgers/CF1/scripts/CF1-d-r11/): runone.py collect (118); collect_seeds.py (118 on five seeds); "
        "runone.py solve on the reference (seeds 0-2); run_graders --unit CF1 --seeds 0-49 (50/50); mutate_graders --unit CF1 --seeds 0-9 (79 of 80 KILLED; m58 survives); "
        "page_smoke --unit CF1 --pages project (in-browser 118 of 118); run_labs CF1 (9/9); each CF1 twin under python -I -W error (exit 0, identical to round 10); "
        "check_projects, check_pages, check_dag (CF1 PASS); ruff check and format --check; mypy --no-incremental on grader and labs; "
        "verify_refs --offline (560 entries, 0 problems) and verify_refs --unit CF1 (2 of 560, 0 problems); cards_scan.py; check_claims.py (IRR examples, zero-flow witness, payback inf); "
        "alternatives: 15 earlier engines and 5 new engines pass. "
        "Not checked: the full repository gate (only CF1 files); lesson prose beyond the changed sentences and the card-agreement checks in their rows; "
        "hours beyond arithmetic (architect ruling: design targets); registry live checks beyond CF1 entries; the in-browser check on the other pages; "
        "the L02 Lab 2 code lines beyond the cited ones; the four new L01 Remark and table wording was checked for numbers and claims only, not for prose style. "
        "The n01-n03 mutants in ledgers/CF1/mutants/CF1-a-r10/ are in a subfolder and are not run by mutate_graders (not in this slice)."
    ),
    "summary": "",
}
pass_n = sum(1 for r in rows if r["status"] == "PASS")
fail_n = sum(1 for r in rows if r["status"] != "PASS")
frag["summary"] = (
    f"CF1-d round 11: FAIL. Rows {len(rows)}: PASS {pass_n}, non-PASS {fail_n} "
    f"(index-ladder-rung1-worked-example, cards-count-vs-plan, proj-mutant-m58-zero-flow-time-index). "
    f"Mutants {sum(1 for m in mutants if m['killed_by'].startswith('test_') or '(seed' in m['killed_by'])}/{len(mutants)} killed; "
    f"m58 survives. Round-10 FAIL lesson-l02-canon-earnings-claim now PASS (sentence rewritten and checked)."
)
out = CHECKOUT / "ledgers/CF1/CF1-d.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, len(rows), "rows", len(mutants), "mutants")
