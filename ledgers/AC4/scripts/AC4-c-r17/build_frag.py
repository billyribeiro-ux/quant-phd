"""Build the round-17 AC4-c fragment from the round-8 rows (carry rules applied) plus this round's fresh rows."""
import json
import sys

checkout = sys.argv[1]
prev = json.load(open("/tmp/fanout-frags/AC4-c.round16.json", encoding="utf-8"))  # file content is round 8 (pin 2c8162b)
PREFIX = ("Carried from round 16 (course/modules/AC/AC4/L05.html, course/modules/AC/AC4/L06.html, "
          "tests/labs/AC4/lab-AC4-L05-1.py, tests/labs/AC4/lab-AC4-L06-1.py byte-identical since the previous pin 2c8162b): ")
FRESH = {
    "AC4-c-cmd-check-pages": "Re-run r17 on pin fefbf8b: `.venv/bin/python tools/check_pages.py --unit AC4` printed 'check_pages AC4: PASS' (exit 0).",
    "AC4-c-cmd-check-dag": "Re-run r17: `tools/check_dag.py --unit AC4` printed 'check_dag AC4: PASS' (exit 0).",
    "AC4-c-cmd-check-projects": "Re-run r17: `tools/check_projects.py --unit AC4` printed 'check_projects AC4: PASS' (exit 0).",
    "AC4-c-cmd-run-labs": "Re-run r17: `tools/run_labs.py --unit AC4 --page L05` and `--page L06` each printed 'run_labs AC4: PASS (1/1)' (exit 0).",
    "AC4-c-twins-run": "Re-run r17: `.venv/bin/python -I -W error tests/labs/AC4/lab-AC4-L05-1.py` and the L06 twin both exit 0 with empty stderr; stdout equals the page's expected block (string comparison, both MATCH).",
    "AC4-c-page-smoke": "Re-run r17: `tools/page_smoke.py --unit AC4 --pages L05 L06` printed 'page_smoke modules/AC/AC4/L05.html: PASS', '... L06.html: PASS', 'page_smoke AC4: PASS' (exit 0).",
    "AC4-c-lint-types-pytest": "Re-run r17: `ruff check` and `ruff format --check` on both twins passed; `mypy --no-incremental` on both twins: 'Success: no issues found in 2 source files'; `pytest -q tests/test_labs.py -k AC4` 10 passed; `pytest -q tests/test_run_labs.py tests/test_page_checks.py` 47 passed in 0.04s.",
    "AC4-c-citations": "Re-run r17: `tools/verify_refs.py --unit AC4` 'live re-verification of AC4: 2 of 560 entries, 0 problems'; `tools/verify_refs.py --offline` 'offline integrity: 560 entries, 0 problems'. Neither L05 nor L06 has a data-references entry and both state 'This lesson cites no registry source'.",
    "AC4-c-numbers": "Re-derived r17 with python -I: all printed lab figures, every prose figure in L05 and L06 (sections 2-5, Misconceptions, Problem set, Key results, quiz keys) recomputed from integers; no rounding involved except 189.3%, 112.1%, 56.5% and 3.5 points (56.52 and 3.478 unrounded), all consistent.",
    "AC4-c-grades": "Re-read r17: L05 Props 2.1 and 2.2 are T with proofs (lines 66-84); L06 Props 2.1 and 2.2 are T (lines 77-99); every Lab-derived result (key-results tables L05 line 389-390, L06 lines 409-410, cards) is C with basis naming Lab 1 (SIMULATED).",
    "AC4-c-math-L05": "Re-derived r17: Prop 2.1 (line 69-74), Prop 2.2 (line 78-84), P2 (line 318), E1 265000/140000=1.893, E3 1300000/1160000=1.12069 and 140000/1160000=0.12069, R2 1,658,000 (line 368). All match.",
    "AC4-c-math-L06": "Re-derived r17: Prop 2.1 Steps 1-4 (lines 84-88) recomputed by symbol; Prop 2.2 (lines 93-98) incl. the 50/-50 counterexample; R1 fifth term (line 381, E_a+P_a=E+P checked); R3 (line 395): CM_A=1400, CMbar=1600, V=240000, M=20000, E=-10000, sum 210000 = 1810000-1600000.",
    "AC4-c-hours": "Re-run r17: L01..L08 data-hours 6,7,6,6,7,6,6,6 sum to 50 = index data-hours-lessons=50; index line 142 says 'six or seven study hours each', consistent. Pace estimate not used (architect ruling).",
    "AC4-c-structure": "Re-run r17: check_pages PASS for AC4 (contract, sections, ids, alt text); L05 sections 1-10 and L06 sections 1-9 present in the template order with key-results table and retrieval quiz.",
    "AC4-c-banned-phrases": "Re-read r17 of L05.html and L06.html visible prose via grep for roughly/about/historically/typically/usually/generally/often/most/some/many/half/ellipsis/builder/verifier/round: no banned hit in prose (only code, math, 'about' absent). check_pages banned-string check PASS.",
    "AC4-c-dag-concepts": "Re-run r17: check_dag AC4 PASS. L05 uses L01 concepts cost-behaviour, contribution-margin (L01 line 59, 88); operating income is L01 line 98; relevant range L01 line 59. L06 uses master-budget and flexible-budget defined in L05 (L05 lines 49, 54).",
    "AC4-c-cards-L05": "Re-verified r17: cards.json AC4-c059..c068 read in full against L05 text. c061 (sign convention) matches Definition 1.3 line 59; c063 (flexed fixed overhead 500,000 at 1,150 units) matches lab output 'flexed_revenue ... fixed 500000' and line 267; the other eight cards unchanged since 2c8162b and match.",
    "AC4-c-cards-dup-scan": "Re-run r17 (python -I over cards.json): 134 cards, no duplicate ids, no duplicate fronts; every grade C card has a basis; cards without a grade are definitions with no claim.",
    "AC4-c-cards-L06": "Re-verified r17: AC4-c069..c081 and c110..c112 read in full against L06 text; new card AC4-c133 and changed card AC4-c073 re-verified in their own rows; others unchanged and matching.",
    "AC4-c-quiz-keys": "Re-run r17 against L05 quiz items 2,3,5,7,9 (11600, 1925000, -125000, 112.1, 1658000) and L06 items 2,3,5,7,9 (249000, -75000, 40000, 2800, 1400): each recomputed from the lab output or the page's own numbers.",
    "AC4-c-lab-L05-output": "Re-run r17: twin output equals the L05 page's expected block (string MATCH); the hypothesis numbers (1,160,000; 1,300,000; 140,000; 265,000; 249,000; 16,000) equal the printed values; interpretation figures (1,425,000; -125,000) equal printed values.",
    "AC4-c-lab-L06-output": "Re-run r17: twin output equals the L06 expected block (string MATCH); the hypothesis figures (-40,000; +249,000; +16,000; -75,000; +150,000; +140,000) equal the printed values.",
    "AC4-c-lab-L06-mutants": "Re-run r17 of the 10 AC4-c-r7 files plus the 9 AC4-c-r8 files against the L06 expected block (run_mutants.py): m01, m02, m03, n01, n02, n03, s01, s02, s03, s04 (AC4-c-r7 and AC4-c-r8 copies) raise ValueError (killed). m04_sales_price_uses_budget_units (AC4-c-r7 and AC4-c-r8) prints the expected block unchanged: sales_price = (-100*600)+(50*400) = -40,000 equals (-100*650)+(50*500) = -40,000 on Lab 1 inputs. SURVIVES. See AC4-c-r17-m04-survivor.",
    "AC4-c-lab-alt-impl": "Re-run r17: alternatives alt01 (r7) and alt01..alt05 (r8) print the expected block exactly (SAME); new alt06..alt08 (AC4-c-r17) also SAME.",
    "AC4-c-L05-lab-mutants": "Re-run r17: n04_L05_fixed_overhead_flexes_with_units, n05_L05_flexed_uses_actual_kg (r7 and r8 copies) and s05_L05_flexed_budget_at_budget_units print output that differs from the L05 expected block (DIFF, killed).",
    "AC4-c-mutants-new-r8": "Re-run r17: r8 s01..s05 each raise ValueError (killed); r8 s05 prints a DIFF output. All killed.",
    "AC4-c-alt-impl-r8": "Re-run r17: r8 alt01..alt05 print the expected block (SAME) on the L06 twin; all five are correct alternatives and pass.",
    "AC4-c-L05-lab-identity-line": "",
    "AC4-c-cards-c076": "Carried from round 16 (entry AC4-c076 of course/modules/AC/AC4/cards.json byte-identical since the previous pin 2c8162b; the file changed only at other entries):",
    "AC4-c-L05-cards-verbatim-check": "Re-verified r17: AC4-c059..c068 read in full against the L05 page; c061 and c063 changed since 2c8162b and were re-checked (AC4-c-r17-card-c061, AC4-c-r17-card-c063); c059, c060, c062, c064 to c068 byte-identical and matching the text (Def 1.1, Def 1.2, misconception 1, Prop 2.1, Prop 2.2, Lab 1 lines 221-237).",
}
NEW_ROWS = [
    {"id": "AC4-c-r17-delta", "check": "Delta 2c8162b..fefbf8b for this slice's paths", "location": "course/modules/AC/AC4/L05.html, L06.html, tests/labs/AC4/lab-AC4-L05-1.py, lab-AC4-L06-1.py, cards.json, tools/",
     "status": "PASS", "evidence": "`git diff --stat 2c8162b fefbf8b` over the slice: L05.html, L06.html, both twins, index.html, tools/ and the L05/L06 cards show no change except cards.json (134 insertions, 27 deletions: existing entries c003, c004, c008, c012, c014, c017, c029, c038, c040, c042, c043, c044, c045, c058, c061, c063, c073, c102 reworded; c120 to c134 added). Mutant directories AC4-c-r17 added. Previous pin fragment is labelled round 8 (see notes)."},
    {"id": "AC4-c-r17-card-c061", "check": "Changed card AC4-c061 (front reworded, back unchanged)", "location": "course/modules/AC/AC4/cards.json AC4-c061; course/modules/AC/AC4/L05.html line 59 (Definition 1.3)",
     "status": "PASS", "evidence": "Front 'What sign convention is used for variances?' asks the same thing as Definition 1.3 (line 59). Back: actual minus budget for profit lines, cost lines enter so a higher cost reduces profit, positive favourable, negative unfavourable: matches line 59 word for word in substance."},
    {"id": "AC4-c-r17-card-c063", "check": "Changed card AC4-c063 (back reworded)", "location": "course/modules/AC/AC4/cards.json AC4-c063; L05.html line 267; lab output flexed_revenue line 'fixed 500000'",
     "status": "PASS", "evidence": "Back: 'In Lab 1 the flexed fixed overhead at 1,150 units is 500,000 cents, the same as the master budget at 1,000 units.' Printed 'flexed_revenue 3325000 material 1400000 fixed 500000' (r17 run of tests/labs/AC4/lab-AC4-L05-1.py); master contribution 1,660,000 less master operating profit 1,160,000 = 500,000 (L05 line 267). Basis matches the card."},
    {"id": "AC4-c-r17-card-c073", "check": "Changed card AC4-c073 (back adds 'Total' and a Proposition 2.2(c) pointer)", "location": "course/modules/AC/AC4/cards.json AC4-c073; L06.html Definition 1.2 line 70 and Proposition 2.2(c) line 93",
     "status": "PASS", "evidence": "E = -pi x sum(kg - s q) is Definition 1.2 (line 70). 'Total kilograms used above the total standard allowance ... make E negative' is the sufficient condition of Proposition 2.2(c) (line 93: if sum kg > sum s q then E negative; 'No converse is claimed'). The card states a sufficient condition, not a necessary one. Verified with python -I: 2950 > 2800 gives E = -75,000."},
    {"id": "AC4-c-r17-card-c133", "check": "New card AC4-c133 (zero efficiency with offsetting deviations)", "location": "course/modules/AC/AC4/cards.json AC4-c133; L06.html Proposition 2.2 proof line 98",
     "status": "PASS", "evidence": "Line 98: 'If one product uses 50 kg above its allowance and another uses 50 kg below its allowance, the sum in Definition 1.2 is zero, so E = 0, while kg != s q for each product.' Card back matches. Grade T is a proof, correct. Computed: (+50) + (-50) = 0, E = 0."},
    {"id": "AC4-c-r17-ne-mutants", "check": "Seven new student-error and equivalent mutants of my own (AC4-c-r17 ne01..ne07), run against the L05 and L06 expected blocks",
     "location": "ledgers/AC4/mutants/AC4-c-r17/ne01..ne07; ledgers/AC4/scripts/AC4-c-r17/make_mutants.py and run_mutants.py",
     "status": "PASS", "evidence": "ne01 (efficiency over product B only) ValueError residual; ne02 (unweighted average contribution) ValueError; ne03 (operating-profit variance with fixed sign flipped) prints 160000 DIFF; ne04 (flexed budget fixed at actual 510,000) DIFF; ne05 (flexed revenue at actual price) DIFF. ne06 (efficiency at actual price, written as a literal 500 product) and ne07 (budget shares rounded to 2 dp) print the expected block: both are EQUIVALENT on Lab 1 inputs (price a = pi = 500 per the lab docstring line 111, and shares 0.6 and 0.4 are exact at 2 dp). Not counted as survivors (equivalent mutants with reason)."},
    {"id": "AC4-c-r17-alt-impl", "check": "Three new correct alternatives (alt06..alt08) must pass",
     "location": "ledgers/AC4/mutants/AC4-c-r17/alt06..alt08",
     "status": "PASS", "evidence": "alt06 (mix by cross-multiplication, Fraction, whole_cents), alt07 (L05 flexed contribution as per-product CM times units, minus fixed), alt08 (volume as sum of CM_i(Q_a m_i - q_b,i)): each prints exactly the expected block (SAME); no over-constraint on the cutoff or on the algebraic route."},
    {"id": "AC4-c-r17-m04-survivor", "check": "Mutant m04: sales price variance uses budget units instead of actual units",
     "location": "tests/labs/AC4/lab-AC4-L06-1.py line 79 (decompose, sales_price); course/modules/AC/AC4/L06.html Definition 1.2 line 67 and lab docstring line 135 ('SP = sum_i (p_a,i - p_b,i) * q_a,i')",
     "status": "FAIL", "evidence": "The mutant is ledgers/AC4/mutants/AC4-c-r8/m04_sales_price_uses_budget_units.py (and the AC4-c-r7 copy). Its sales_price is sum((p_a - p_b) * q_b) = (-100*600)+(50*400) = -40,000, which equals the correct (-100*650)+(50*500) = -40,000 for Lab 1. The mutant's residual is 0 and every printed line equals the expected block (SAME). Definition 1.2 (line 67) and the docstring (line 135) state the formula with q_a, and L06 line 262 states the per-product figures -65,000 and +25,000 on actual units, which the lab does not print or check. A student who makes this error passes Lab 1.",
     "fix": "Make the lab detect it: print the per-product sales price variances (-65,000 and +25,000 on actual units) and/or change one Lab 1 input so budget-unit and actual-unit price variances differ; re-run tools/embed_labs.py --refresh for L06 and the run_labs/page_smoke gates."},
    {"id": "AC4-c-r17-prose-rescan", "check": "Full read of L05.html and L06.html prose after the round-16 changes in cards (pages unchanged) with scope-word and cause-direction scan",
     "location": "course/modules/AC/AC4/L05.html lines 43-254, 262-271, 336, 350; L06.html lines 52-108, 259-291, 318-398",
     "status": "PASS", "evidence": "Read all of both pages line by line. Checked: 'exceeds one because the flexible variance offsets part' (L05 line 336: 265,000-125,000=140,000, correct direction); 'understates the cost' (L05 line 246/R1: correct when fixed cost rises); 'the volume variance is the largest of the four in size' (L06 line 259: 249,000 > 75,000 > 40,000 > 16,000); 'the mix ... 56.5% against 60%, a gap of 3.5 points (60-56.52=3.48)' (L06 line 259: 650/1150=56.52%, rounding to 3.5 correct); '1,500 and 1,900 cents per unit' (P2 line 318). No new error found in any sentence."},
    {"id": "AC4-c-r17-lab-claims", "check": "Lab-prints claims in prose (what Lab 1 prints or checks)", "location": "L05.html line 97 and 238, 263, 267, 271; L06.html line 112, 119-120, 259; tests/labs/AC4/lab-AC4-L05-1.py line 191-197; lab-AC4-L06-1.py line 119-120, 140-141, 231-241",
     "status": "PASS", "evidence": "L05 line 97 'Lab 1 prints that 265,000 as one figure' (volume_and_mix_variance 265000, printed); L05 line 192-193 'holds by construction ... not checked here' (no assert on it; true). L06 line 119-120 'fails loudly if any reported variance is not a whole number' (whole_cents on volume and mix; price and efficiency are integers by construction; claim holds). L06 line 259 'the lab raises an error if they do not' (decompose raises ValueError on residual; killed mutants confirm)."},
]
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in FRESH:
        if rid == "AC4-c-L05-lab-identity-line":
            pass
        if FRESH[rid]:
            r = dict(r)
            r["evidence"] = FRESH[rid]
            if rid == "AC4-c-lab-L06-mutants":
                r["status"] = "FAIL"
                r["fix"] = "See AC4-c-r17-m04-survivor: the L06 lab does not detect a sales-price formula that uses budget units."
            if rid == "AC4-c-cards-c076":
                r["status"] = "PASS"
            rows.append(r)
            continue
    r = dict(r)
    if rid in ("AC4-c-cards-c076",):
        pass
    r["evidence"] = PREFIX + r["evidence"]
    rows.append(r)
rows += NEW_ROWS
# Fix the one carried row whose cited subject is not the page (keep carried prefix with its own wording)
for r in rows:
    if r["id"] == "AC4-c-cards-c076":
        r["evidence"] = FRESH["AC4-c-cards-c076"] + " AC4-c076 text: 'False. Efficiency compares actual kilograms with the standard allowed...' read in full and matches Lab 1 (2,950 kg, 2,800 kg, -75,000)."
        r["status"] = "PASS"
    if r["id"] == "AC4-c-L05-lab-identity-line":
        r["evidence"] = PREFIX + r["evidence"]
for r in rows:
    if r["id"] == "AC4-c-L05-lab-identity-line" and not r["evidence"].startswith("Carried"):
        pass
fails = [r for r in rows if r["status"] != "PASS"]
mutants = [
 {"id": "m01_efficiency_sign", "description": "L06 efficiency variance sign flipped", "killed_by": "ValueError residual -150000 cents", "file": "ledgers/AC4/mutants/AC4-c-r7/m01_efficiency_sign.py"},
 {"id": "m02_mix_uses_actual_units_not_budget_share", "description": "L06 mix uses actual units", "killed_by": "ValueError residual -249000 cents", "file": "ledgers/AC4/mutants/AC4-c-r7/m02_mix_uses_actual_units_not_budget_share.py"},
 {"id": "m03_volume_uses_budget_contribution_of_A", "description": "L06 volume uses budget contribution of A", "killed_by": "ValueError residual 24000 cents", "file": "ledgers/AC4/mutants/AC4-c-r7/m03_volume_uses_budget_contribution_of_A.py"},
 {"id": "m04_sales_price_uses_budget_units", "description": "L06 sales price variance on budget units (-40,000 by coincidence on Lab 1 inputs)", "killed_by": "SURVIVED: prints the expected block", "file": "ledgers/AC4/mutants/AC4-c-r7/m04_sales_price_uses_budget_units.py"},
 {"id": "n01_L06_mix_uses_budget_total", "description": "L06 mix share from budget total", "killed_by": "ValueError residual -249000 cents", "file": "ledgers/AC4/mutants/AC4-c-r7/n01_L06_mix_uses_budget_total.py"},
 {"id": "n02_L06_efficiency_allowance_on_budget_units", "description": "L06 standard allowance on budget units", "killed_by": "ValueError residual 200000 cents", "file": "ledgers/AC4/mutants/AC4-c-r7/n02_L06_efficiency_allowance_on_budget_units.py"},
 {"id": "n03_L06_volume_uses_actual_mix_average", "description": "L06 volume at actual-mix average", "killed_by": "ValueError non-whole cents 5775000/23", "file": "ledgers/AC4/mutants/AC4-c-r7/n03_L06_volume_uses_actual_mix_average.py"},
 {"id": "n04_L05_fixed_overhead_flexes_with_units", "description": "L05 flexed fixed overhead scales with units", "killed_by": "DIFF from expected block", "file": "ledgers/AC4/mutants/AC4-c-r7/n04_L05_fixed_overhead_flexes_with_units.py"},
 {"id": "n05_L05_flexed_uses_actual_kg", "description": "L05 flexed budget uses actual kilograms", "killed_by": "DIFF from expected block", "file": "ledgers/AC4/mutants/AC4-c-r7/n05_L05_flexed_uses_actual_kg.py"},
 {"id": "alt01_mix_written_as_sum_minus_total", "description": "alternative correct implementation, r7", "killed_by": "PASS (SAME as expected block)", "file": "ledgers/AC4/mutants/AC4-c-r7/alt01_mix_written_as_sum_minus_total.py"},
 {"id": "r8_s01_L06_mix_share_from_actual_total", "description": "L06 mix shares from actual total", "killed_by": "ValueError residual 16000 cents", "file": "ledgers/AC4/mutants/AC4-c-r8/s01_L06_mix_share_from_actual_total.py"},
 {"id": "r8_s02_L06_volume_at_actual_mix_margin", "description": "L06 volume at actual-mix margin", "killed_by": "ValueError non-whole cents 5775000/23", "file": "ledgers/AC4/mutants/AC4-c-r8/s02_L06_volume_at_actual_mix_margin.py"},
 {"id": "r8_s03_L06_efficiency_allowance_on_budget_units", "description": "L06 allowance on budget units (same as n02)", "killed_by": "ValueError residual 200000 cents", "file": "ledgers/AC4/mutants/AC4-c-r8/s03_L06_efficiency_allowance_on_budget_units.py"},
 {"id": "r8_s04_L06_actual_revenue_at_budget_price", "description": "L06 actual revenue at budget price", "killed_by": "ValueError residual 40000 cents", "file": "ledgers/AC4/mutants/AC4-c-r8/s04_L06_actual_revenue_at_budget_price.py"},
 {"id": "r8_s05_L05_flexed_budget_at_budget_units", "description": "L05 flexed budget at budget units", "killed_by": "DIFF from expected block", "file": "ledgers/AC4/mutants/AC4-c-r8/s05_L05_flexed_budget_at_budget_units.py"},
 {"id": "r8_alt01_to_alt05", "description": "five alternative correct implementations (mix sum, cross-check, float-then-round, per-product weights, per-product efficiency loop)", "killed_by": "PASS (SAME as expected block) for all five", "file": "ledgers/AC4/mutants/AC4-c-r8/alt01..alt05"},
 {"id": "ne01_L06_efficiency_only_product_B", "description": "NEW r17: efficiency summed over product B only", "killed_by": "ValueError residual", "file": "ledgers/AC4/mutants/AC4-c-r17/ne01_L06_efficiency_only_product_B.py"},
 {"id": "ne02_L06_unweighted_average_contribution", "description": "NEW r17: unweighted average contribution in volume variance", "killed_by": "ValueError residual", "file": "ledgers/AC4/mutants/AC4-c-r17/ne02_L06_unweighted_average_contribution.py"},
 {"id": "ne03_L06_operating_variance_fixed_sign", "description": "NEW r17: operating-profit variance with fixed-cost sign flipped", "killed_by": "DIFF: operating_profit_variance printed 160000 (expected 140000)", "file": "ledgers/AC4/mutants/AC4-c-r17/ne03_L06_operating_variance_fixed_sign.py"},
 {"id": "ne04_L05_flexed_fixed_at_actual", "description": "NEW r17: flexed budget carries actual fixed overhead", "killed_by": "DIFF from expected block", "file": "ledgers/AC4/mutants/AC4-c-r17/ne04_L05_flexed_fixed_at_actual.py"},
 {"id": "ne05_L05_flexed_revenue_at_actual_price", "description": "NEW r17: flexed revenue at actual selling price", "killed_by": "DIFF from expected block", "file": "ledgers/AC4/mutants/AC4-c-r17/ne05_L05_flexed_revenue_at_actual_price.py"},
 {"id": "ne06_L06_efficiency_at_actual_price_equivalent", "description": "NEW r17: efficiency at a literal 500 (equal to the actual price on Lab 1 inputs); EQUIVALENT on these inputs", "killed_by": "EQUIVALENT (prints the expected block; actual price equals standard, lab docstring line 111)", "file": "ledgers/AC4/mutants/AC4-c-r17/ne06_L06_efficiency_at_actual_price_equivalent.py"},
 {"id": "ne07_L06_budget_shares_rounded_to_two_places", "description": "NEW r17: budget shares rounded to 2 dp; EQUIVALENT on Lab 1 (0.6 and 0.4 exact)", "killed_by": "EQUIVALENT (prints the expected block)", "file": "ledgers/AC4/mutants/AC4-c-r17/ne07_L06_budget_shares_rounded_to_two_places.py"},
 {"id": "alt06_L06_mix_by_cross_multiplication", "description": "NEW r17 alternative: mix by cross-multiplication", "killed_by": "PASS (SAME)", "file": "ledgers/AC4/mutants/AC4-c-r17/alt06_L06_mix_by_cross_multiplication.py"},
 {"id": "alt07_L05_flexed_via_per_product_contribution", "description": "NEW r17 alternative: flexed contribution per product", "killed_by": "PASS (SAME)", "file": "ledgers/AC4/mutants/AC4-c-r17/alt07_L05_flexed_via_per_product_contribution.py"},
 {"id": "alt08_L06_volume_as_sum_of_budget_share_margins", "description": "NEW r17 alternative: volume as sum of CM_i(Q_a m_i - q_b,i)", "killed_by": "PASS (SAME)", "file": "ledgers/AC4/mutants/AC4-c-r17/alt08_L06_volume_as_sum_of_budget_share_margins.py"},
]
out = {
 "unit": "AC4", "slice": "AC4-c", "round": 17,
 "verifier": "independent Haiku verifier, slice AC4-c (L05, L06 and their lab twins), round 17; did not build AC4",
 "pin": "fefbf8b", "base": "2c8162b", "previous_ledger": "/tmp/fanout-frags/AC4-c.round16.json (content is round 8, pin 2c8162b)",
 "checkout": "/tmp/verify17-AC4-c (detached, pinned at fefbf8b)", "scratch": "/tmp/verify17-AC4-c/out_*.txt",
 "verified_at": "2026-10-28T00:00:00Z",
 "verdict": "FAIL" if fails else "PASS",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": ["Live verify_refs --unit AC4: 2 of 560 entries, 0 problems; offline 560 entries, 0 problems; neither AC4-c page cites a registry key."],
 "freshness_flags": [],
 "notes": [
  "Previous-round fragment: /tmp/fanout-frags/AC4-c.round16.json is labelled round 8 with pin 2c8162b (identical to AC4-c.round8.json); it is used as the base for carry rules. The previous pin is therefore 2c8162b.",
  "Delta 2c8162b..fefbf8b for the slice: only course/modules/AC/AC4/cards.json changed. L05.html, L06.html, both twins, index.html and tools/ are byte-identical to 2c8162b.",
  "Carried rows: every carried row cites L05.html, L06.html or a twin, all byte-identical since 2c8162b, so the carry prefix names those files. Card rows were re-verified where their entries changed.",
  "Mutant handling: run_mutants.py ran all 10 AC4-c-r7 and all 9 AC4-c-r8 files and all 10 AC4-c-r17 files. The one survivor (m04) is a FAIL row. ne06 and ne07 are equivalent on the Lab 1 inputs.",
  "Lesson hours: L05 7 and L06 6; sum with L01..L08 is 50 = index data-hours-lessons 50. No pace estimate used.",
  "Concept links: L05 and L06 use L01 concepts (cost-behaviour, contribution-margin, operating income, relevant range) as defined in L01 lines 59, 88, 98.",
 ],
 "could_not_check": [
  "Full-repo pytest and mypy not run (only tests/test_labs.py -k AC4, tests/test_run_labs.py, tests/test_page_checks.py, and mypy on the two twins).",
  "No external source consulted: neither lesson cites a registry key; no published figure is checked.",
  "Browser visual rendering not checked beyond page_smoke (which loads Chromium and runs the labs in Pyodide).",
  "project.html, grader and the other AC4 slices were outside this slice and were not re-verified.",
  "Mutant m04 cannot be killed by the L06 lab as printed; the verifier did not modify the lab (verifier role: report, do not fix).",
 ],
 "summary": f"rows {len(rows)}: pass {len(rows)-len(fails)}, fail {len(fails)}",
}
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out["summary"], out["verdict"])
