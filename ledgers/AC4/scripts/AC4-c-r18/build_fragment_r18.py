"""Build ledgers/AC4/AC4-c.json (round 18, slice AC4-c) from the round 17 row ids and the round 18 checks.

Carried rows keep the round 17 PASS evidence only where the cited lines are byte-identical since the previous
pin (the 7143726 hunks touch L05.html lines 97, 336, 350, 359, 445, L06.html lines 52, 65, 259, and card AC4-c061 and
AC4-c074's subject line 65). Every other row is re-checked in this round and its evidence says so.
"""
import json
import sys

checkout = sys.argv[1]
prev = json.load(open("/tmp/fanout-frags/AC4-c.round17.json", encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}
CARRY_PREFIX = ("Carried from round 17 (course/modules/AC/AC4/L05.html and L06.html lines cited here are "
                "byte-identical since the previous pin; the 7143726 hunks touch L05 lines 97, 336, 350, 359, 445 and "
                "L06 lines 52, 65, 259 only): ")
CARRY = {
    "AC4-c-L05-P2-scope", "AC4-c-open-items-path", "AC4-c-L06-lab-docstring-residual", "AC4-c-L06-R1-unanswered",
    "AC4-c-L06-M2-misconception-kg", "AC4-c-cards-c076", "AC4-c-L06-sign-convention", "AC4-c-L05-s4-fixed-error-scale",
    "AC4-c-L05-s5-volume-term", "AC4-c-L05-lab-stale-identity-label", "AC4-c-L05-lab-identity-line",
    "AC4-c-L06-P1-step-reason", "AC4-c-L05-remark23-L06-defs", "AC4-c-L05-definition-1-3-L06", "AC4-c-L05-misc3-split",
    "AC4-c-L06-misc1-mix", "AC4-c-L06-R3-standard", "AC4-c-L06-q4-sufficient", "AC4-c-L06-E1-static-variance",
    "AC4-c-L06-operating-variance-term", "AC4-c-L05-q8-explain", "AC4-c-L06-necessity-unproved", "AC4-c-L06-meta-desc",
    "AC4-c-L05-def11-operating-income", "AC4-c-L05-s3-exactness", "AC4-c-L06-prop21-proof-scope-r7",
    "AC4-c-L06-prop22-r7", "AC4-c-L06-honest-pending-r7", "AC4-c-L05-round7-edits", "AC4-c-L05-s4-relevant-range-r8",
    "AC4-c-L06-P3-r8", "AC4-c-L06-E1-static-variance", "AC4-c-r17-card-c063", "AC4-c-r17-card-c073",
    "AC4-c-r17-card-c133",
}
# Round 18 evidence for every re-checked row (what was run or read, and the result).
NEW = {
    "AC4-c-cmd-check-pages": "Re-run r18 on 7143726: `tools/check_pages.py --unit AC4` printed 'check_pages AC4: PASS' (exit 0; out/check_pages.out).",
    "AC4-c-cmd-check-dag": "Re-run r18: `tools/check_dag.py --all` printed 'check_dag AC4: PASS' among seven units, exit 0 (out/check_dag.out).",
    "AC4-c-cmd-check-projects": "Re-run r18: `tools/check_projects.py --all` printed 'check_projects AC4: PASS', exit 0 (out/check_projects.out).",
    "AC4-c-cmd-run-labs": "Re-run r18: `tools/run_labs.py --unit AC4` printed 'run_labs AC4: PASS (10/10)', exit 0 (out/run_labs.out).",
    "AC4-c-twins-run": "Re-run r18: `.venv/bin/python -I -W error` on the L05 and L06 twins: exit 0, stdout printed in full ; stdout equals each page's expected block (out/embed_expected.out).",
    "AC4-c-page-smoke": "Re-run r18: `tools/page_smoke.py --unit AC4 --pages L05 L06` printed both page PASS lines and 'page_smoke AC4: PASS', exit 0 (out/smoke.out).",
    "AC4-c-lint-types-pytest": "Re-run r18: ruff check and ruff format --check on both twins: 'All checks passed!' and '2 files already formatted'; mypy --no-incremental on both twins: 'Success: no issues found in 2 source files'; pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k \"AC4 or run_labs or page_checks\": 57 passed, exit 0 (out/pytest_full.txt) (out/ruff.out, mypy.out, pytest.out).",
    "AC4-c-citations": "Re-run r18: `tools/verify_refs.py --unit AC4` 'live re-verification of AC4: 2 of 560 entries, 0 problems'; `tools/verify_refs.py --offline` 'offline integrity: 560 entries, 0 problems'. Neither page cites a registry key (L05.html and L06.html references sections say so; grep for data-ref/cite finds only the sentence 'cites no source').",
    "AC4-c-numbers": "Re-derived r18 with python -I: every printed lab value (twins run, out/embed_expected.out) and every changed prose figure: 265000/140000=1.8929 (189.3%), 1300000/1160000=1.120690 (112.1%), 140000/1160000=0.120690 (12.1%), 650/1150=0.565217 (56.5%), 60-56.5217=3.478 (3.5), 300x1660=498000 (M3), 780x2500+520x3400=3718000 and 1560000 material, 1658000 (R2), 1600x0.6=960, 1600x0.4=640 (R1). All match the text.",
    "AC4-c-grades": "Re-read r18: L05 Props 2.1 and 2.2 carry data-grade T with proofs; L05 key-results rows T for Props, C for Lab 1 results (SIMULATED); L06 Props 2.1 and 2.2 T; L06 key-results C for Lab 1 values. No change to any grade in the r18 delta.",
    "AC4-c-math-L05": "Re-derived r18: Prop 2.1 (flexed budget at budgeted units equals master, sum CM_i q_i - F), Prop 2.2 (exact split by add and subtract), P2 (1,500 and 1,900 cents per unit), E1 and E3 quotients (see AC4-c-numbers), R2 flexed profit 1,658,000 (780 and 520 units, 3,718,000 - 1,560,000 - 500,000).",
    "AC4-c-math-L06": "Re-derived r18: Prop 2.1 steps 1-4 (lines 84-88) by symbol; Prop 2.2 (a), (b), (c) and the 50/-50 counterexample; R1 fifth term -(a-pi) sum kg, and E_a + P_a = E + P (R1 solution, checked symbolically); R3 with standard 2.2 kg: CM_A 1400, CMbar 1600, V 240000, M 20000, E -10000, sum 210000 = 1810000 - 1600000.",
    "AC4-c-hours": "Re-run r18: data-hours L01..L08 are 6,7,6,6,7,6,6,6 (sum 50) and index data-hours-lessons=50, data-hours-project=20; L05 declares 7 and L06 declares 6 and the hub split agrees. Hours are design targets (architect ruling); no pace estimate used.",
    "AC4-c-structure": "Re-run r18: check_pages PASS; L05 sections 1-10 and L06 sections 1-9 in template order (s1 to s9 with ids, references at s9), problem tiers mechanics/proof/empirical/research present with M1-M3, P1-P3, E1-E3, R1-R3, quiz with data-cards=cards.json, references present.",
    "AC4-c-banned-phrases": "Re-scan r18 of visible prose of L05.html and L06.html (tags stripped, pre blocks removed) for roughly, about, historically, typically, usually, generally, often, most, half, always, never, all, every, only, exactly, same, drives, offsets, raises, build, verifier, round: each hit read in context; 'about' hits are 'no claim about', 'no finding about'; scope words hit only a computed or stated scope (see AC4-c-r18-scope-rescan).",
    "AC4-c-dag-concepts": "Re-run r18: check_dag AC4 PASS. L05 and L06 link L01 anchors #def-cost-behaviour and #def-contribution-margin, which exist in L01.html (grep id=\"def-\"); operating income is L01 Proposition 2.2 (L01.html line 98); master-budget and flexible-budget anchors are in L05.html.",
    "AC4-c-cards-L05": "Re-verified r18: cards AC4-c059..c068 read against the current L05 text. c061 changed in 7143726 (front now 'What sign convention does this lesson use for variances?') and was re-checked (AC4-c-r18-card-c061). The rest match: c062 (static +140,000 contains +265,000; flexible -125,000), c063 (flexed fixed 500,000 at 1,150), c067 (+140,000, +265,000, -125,000), c068 (500,000).",
    "AC4-c-cards-dup-scan": "Re-run r18 (python -I over cards.json): 134 cards, no duplicate ids, no duplicate fronts; the 7143726 delta changed fronts/backs of c008, c018, c061, c095, c096, c125 only (cards.json diff).",
    "AC4-c-cards-L06": "Re-verified r18: AC4-c069..c081, c110..c112 and c133 read against the current L06 text. Unchanged cards match their subjects. c074 (contribution variance) subject changed in 7143726 (Definition 1.2 now says 'In this model material is the only variable cost'); the card drops that scope: see AC4-c-r18-c074-scope (FAIL).",
    "AC4-c-quiz-keys": "Re-run r18 against the current quiz: L05 items 2 (11600), 3 (1925000), 5 (-125000), 7 (112.1 with E3 explain 1,300,000/1,160,000 = 1.12069), 9 (1658000, R2) and L06 items 2 (249000), 3 (-75000), 5 (40000), 6 (2800), 8 (1400): each key equals the printed value or the explain arithmetic.",
    "AC4-c-lab-L05-output": "Re-run r18: twin stdout equals L05 expected block (string equal, out/embed_expected.out 'expected block equals run output: True'); embedded code equals the twin (True).",
    "AC4-c-lab-L06-output": "Re-run r18: twin stdout equals L06 expected block (True); embedded code equals the twin (True). Lab 1 prints budget_contribution 1660000, sales_price_variance -40000, sales_volume_variance 249000, sales_mix_variance 16000, efficiency_variance -75000, operating_profit_variance 140000, check lines 0/0/249000/249000.",
    "AC4-c-L05-hypothesis-causal": "Re-read r18 (L05.html line 97, changed in 7143726): '1,660 cents (1,660,000 cents on 1,000 budgeted units, as the lab prints)' matches master_contribution 1660000 printed by the twin; 1,660 is the average (1,660,000 / 1,000), which the parenthesis states; 150 x 1,660 = 249,000 and 249,000 + 16,000 = 265,000 match; 'Lab 1 prints that 265,000 as one figure' matches volume_and_mix_variance 265000.",
    "AC4-c-L06-lab-docstring-residual": "Carried from round 17 (tests/labs/AC4/lab-AC4-L06-1.py lines 28-29 and 98-99 byte-identical since the previous pin; the twin is unchanged in 7143726).",
    "AC4-c-lab-alt-impl": "Re-run r18: alt01 (r7), alt01..alt05 (r8), alt06..alt08 (r17), and the three new alternatives alt_r18_a (scaled-integer mix), alt_r18_b (price and efficiency from totals), alt_r18_c (material from total kg) all print the expected block exactly (runner status SAME; out/rerun_all_mutants.out, out/r18_alts.out).",
    "AC4-c-L05-lab-mutants": "Re-run r18: n04 and n05 (r7 and r8 copies) and s05 print DIFF from the L05 expected block; ne04 and ne05 (r17) DIFF; the new r18 mutant r18_m05_L05_master_fixed_at_actual prints DIFF (out/r18_mutants.out, out/rerun_all_mutants.out).",
    "AC4-c-L06-interp-sentences": "Re-verified r18 (L06.html line 259, changed in 7143726): 56.5% = 650/1150 (0.5652); 60 - 56.5217 = 3.478 rounds to 3.5; volume 150 x 1,660 = 249,000; 690 and 460 check units are 60% and 40% of 1,150; mix +16,000 = -60,000 + 76,000 (per-product paragraph); efficiency 2,950 vs 2,800 kg. The lab states no fact about real firms (lab docstring).",
    "AC4-c-L06-why-def12": "Re-verified r18 (L06.html lines 52 and 65, changed in 7143726): 'in this model' scope on the contribution is defined in Section 1 (line 65, 'In this model material is the only variable cost'), consistent with L05 Section 2 (L05.html line 63: 'the material is variable'; the fixed overhead is F).",
    "AC4-c-L06-section1-ref": "Re-verified r18: the L06 Section 1 opening (line 56) cites L05 Definition 1.3 (present at L05.html line 59); line 52 and line 65 wording as above.",
    "AC4-c-L06-scope-when-zero": "Re-verified r18 (line 52 changed in 7143726): the why-it-matters sentence now reads 'which in this model is revenue less the cost of the material used'; the scope of zero terms in Propositions 2.1 and 2.2 (lines 79, 92-98) unchanged and read.",
    "AC4-c-L06-E1-static-variance": "Carried from round 17 (L06.html E1 prompt line 354 byte-identical since the previous pin; the L06 hunks in 7143726 are lines 52, 65, 259 only).",
    "AC4-c-L05-cards-verbatim-check": "Re-verified r18: AC4-c059..c068 compared with the current L05 text. c061 (the changed card) matches Definition 1.3 (line 59 of L05.html: 'Every variance in this lesson is stated as its effect on operating profit'); its back is the same as before. c063 and c068 numbers match Lab 1 printed values.",
    "AC4-c-L06-q4-sufficient": "Carried from round 17 (L06.html quiz item 4 at line 440 byte-identical since the previous pin; L06 hunks are lines 52, 65, 259).",
    "AC4-c-L05-q8-explain": "Carried from round 17 (L05.html quiz item 8 at line 454 byte-identical since the previous pin; the L05 quiz change in 7143726 is item 7 at line 445).",
    "AC4-c-L05-s3-exactness": "Carried from round 17 (L05.html line 93 section 3 paragraph byte-identical since the previous pin).",
    "AC4-c-L05-misc3-split": "Carried from round 17 (L05.html misconception 3 at line 270 byte-identical since the previous pin).",
        "AC4-c-L06-prop21-proof-scope-r7": "Carried from round 17 (L06.html Proposition 2.1 proof lines 83-88 byte-identical since the previous pin).",
    "AC4-c-L06-prop22-r7": "Carried from round 17 (L06.html Proposition 2.2 lines 92-98 byte-identical since the previous pin).",
    "AC4-c-L05-round7-edits": "Carried from round 17 (L05.html lines 49, 67, 77-78, 251-254 byte-identical since the previous pin).",
    "AC4-c-L06-P1-step-reason": "Carried from round 17 (L06.html P1 solution byte-identical since the previous pin).",
    "AC4-c-embedded-code-r8": "Re-run r18 (out/embed_expected.py via embed_and_expected_r18.py): the embedded code of L05.html and L06.html equals the twins after html.unescape (True, True); both expected blocks equal the run output (True, True).",
    "AC4-c-r17-delta": "Round 18 delta fefbf8b..7143726 for the slice (`git diff --stat fefbf8b 7143726` filtered to AC4 L05, L06, cards, twins): L05.html hunks at lines 97, 336, 350, 359, 445; L06.html hunks at lines 52, 65, 259; cards.json entries AC4-c061 (front), and c008, c018, c095, c096, c125 (other lessons); tests/labs/AC4/lab-AC4-L07-1.py (not this slice). Every changed subject is re-checked in this round.",
    "AC4-c-r17-card-c061": "Changed card AC4-c061 (front reworded in 7143726 to 'What sign convention does this lesson use for variances?'): matches L05 Definition 1.3 ('this lesson'); back equals Definition 1.3 (actual minus budget; favourable positive).",
    "AC4-c-r17-card-c063": "Carried from round 17 (cards.json entry AC4-c063 byte-identical since the previous pin; cited Lab 1 figures unchanged).",
    "AC4-c-r17-card-c073": "Carried from round 17 (cards.json entry AC4-c073 byte-identical since the previous pin; cited Definition 1.2 efficiency bullet and Proposition 2.2(c) unchanged).",
    "AC4-c-r17-card-c133": "Carried from round 17 (cards.json entry AC4-c133 byte-identical since the previous pin; cited sentence in Proposition 2.2 proof unchanged).",
    "AC4-c-r17-ne-mutants": "Re-run r18: ne01..ne07 (r17) via run_mutants.py: ne01 ERR, ne02 ERR, ne03 DIFF, ne04 DIFF, ne05 DIFF, ne06 SAME (equivalent on Lab 1 inputs, actual price equals 500 per kg), ne07 SAME (equivalent on Lab 1: 0.6 and 0.4 exact).",
    "AC4-c-r17-alt-impl": "Re-run r18: alt06, alt07 (L05), alt08 print the expected block (SAME).",
    "AC4-c-r17-prose-rescan": "Full read r18 of L05.html and L06.html prose, lines 43-274 and 296-488 (both pages), with each changed sentence re-derived (see AC4-c-r18-scope-rescan). Lines 97, 336, 350, 359, 445 (L05) and 52, 65, 259 (L06) are the only changed lines; all other prose re-read and unchanged.",
    "AC4-c-r17-lab-claims": "Re-verified r18: L05 line 97 'Lab 1 prints that 265,000 as one figure' (volume_and_mix_variance 265000 printed); L06 line 259 'the lab raises an error if they do not' (decompose raises ValueError, twin lines 97-99); 'the lab uses 2,950 kg where the standard allowed is 2,800 kg' (twin printed inputs).",
    "AC4-c-L05-lab-identity-line": "Carried from round 17 (tests/labs/AC4/lab-AC4-L05-1.py identity comment and assert, lines 92-97, byte-identical since the previous pin).",
    "AC4-c-L06-R1-unanswered": "Carried from round 17 (L06.html R1 solution byte-identical since the previous pin).",
    "AC4-c-L06-meta-desc": "Carried from round 17 (L06.html meta description line 7 byte-identical since the previous pin).",
    "AC4-c-L05-s4-relevant-range-r8": "Carried from round 17 (L05.html Section 4 bullet 1 byte-identical since the previous pin).",
    "AC4-c-L06-honest-pending-r7": "Carried from round 17 (L06.html honest-pending paragraph at line 490 and references at 484-488 byte-identical since the previous pin).",
    "AC4-c-open-items-path": "Carried from round 17 (L05.html honest-pending paragraph at line 470 byte-identical since the previous pin).",
    "AC4-c-L06-operating-variance-term": "Carried from round 17 (L06.html E1 prompt line 354 and E1 solution byte-identical since the previous pin).",
    "AC4-c-L06-R3-standard": "Carried from round 17 (L06.html R3 solution byte-identical since the previous pin); its numbers re-derived this round (see AC4-c-math-L06).",
    "AC4-c-L06-misc1-mix": "Carried from round 17 (L06.html misconception 1 byte-identical since the previous pin); its numbers 1,500 x (-100) + 1,900 x 100 = +40,000 re-derived this round.",
    "AC4-c-L06-necessity-unproved": "Carried from round 17 (L06.html Proposition 2.2 proof, line 98, byte-identical since the previous pin).",
    "AC4-c-L05-def11-operating-income": "Carried from round 17 (L05.html Definition 1.1 line 49 byte-identical since the previous pin).",
    "AC4-c-L05-definition-1-3-L06": "Carried from round 17 (L05.html Definition 1.3 line 59 byte-identical since the previous pin).",
    "AC4-c-L05-remark23-L06-defs": "Carried from round 17 (L05.html Remark 2.3 line 87 byte-identical since the previous pin).",
    "AC4-c-L05-s4-fixed-error-scale": "Carried from round 17 (L05.html Section 4 bullet 2 byte-identical since the previous pin).",
    "AC4-c-L05-s5-volume-term": "Carried from round 17 (L05.html Section 4 bullet 3 and Section 5 byte-identical since the previous pin).",
    "AC4-c-L05-lab-stale-identity-label": "Carried from round 17 (tests/labs/AC4/lab-AC4-L05-1.py lines 92-97 byte-identical since the previous pin).",
    "AC4-c-L05-P2-scope": "Carried from round 17 (L05.html P2 solution byte-identical since the previous pin).",
        "AC4-c-L06-P3-r8": "Carried from round 17 (L06.html P3 solution byte-identical since the previous pin).",
            "AC4-c-mutants-new-r8": "Re-run r18: r8 s01..s05 are all non-SAME (ValueError or DIFF) on their pages (out/rerun_all_mutants.out).",
    "AC4-c-alt-impl-r8": "Re-run r18: r8 alt01..alt05 print the expected block (SAME).",
            }


FAIL = {
    "AC4-c-lab-L06-mutants": (
        "FAIL",
        "Re-run r18 (out/rerun_all_mutants.out): the AC4-c-r7 and AC4-c-r8 copies of m04_sales_price_uses_budget_units.py print "
        "the L06 expected block exactly (SAME). Every other earlier L06 mutant raises ValueError or differs (killed). "
        "The survivor is the sales-price formula on budget units; see AC4-c-r17-m04-survivor.",
        "Make Lab 1 detect a sales-price variance computed on budget units: print the per-product sales price variances "
        "(-65,000 for A and +25,000 for B) or change the inputs so that the budget-unit and actual-unit sums differ, then regenerate the expected block with embed_labs.py --refresh.",
    ),
    "AC4-c-r17-m04-survivor": (
        "FAIL",
        "Mutant m04_sales_price_uses_budget_units (ledgers/AC4/mutants/AC4-c-r7 and AC4-c-r8) prints the expected block "
        "unchanged (run_mutants.py: SAME). The page states the sales price variance as SP = sum_i (p_a,i - p_b,i) q_a,i: "
        "L06.html line 67 (Definition 1.2, bullet 1) and the lab docstring line 23 of tests/labs/AC4/lab-AC4-L06-1.py. "
        "The twin uses units_actual at line 79, but on Lab 1 inputs (-100 x 600 + 50 x 400 = -40,000 = -100 x 650 + 50 x 500) the budget-unit variant gives the same printed total, so Lab 1 cannot tell the two apart.",
        "Change Lab 1 so the two formulas differ (for example print per-product sales price variances, which are -65,000 and +25,000 on actual units, or use an actual unit mix whose budget-unit sum differs), regenerate the expected block, and re-run the mutant.",
    ),
    "AC4-c-r18-c074-scope": (
        "FAIL",
        "cards.json AC4-c074 (lesson L06): back 'Actual contribution is actual revenue less the cost of the material used'. "
        "L06.html line 65 (Definition 1.2, changed in 7143726) now says 'In this model material is the only variable cost, so the contribution is revenue less the cost of the material used'. "
        "The card states the identity without the model scope the lesson now gives it, so a student can read it as a general definition.",
        "Edit cards.json AC4-c074 back to: 'T = C_a - C_b, the actual contribution less the budget contribution. In this model, where material is the only variable cost, actual contribution is actual revenue less the cost of the material used, and budget contribution is the sum of CM_i x q_b,i (Definition 1.2).' Then re-run the card check.",
    ),
}
EXTRA_ROWS = [
    ("AC4-c-r18-recheck-E1-E3-R1-L05", "2.2 numbers and 2.4 math: changed L05 problems E1, E3, R1 (lines 336, 350, 359)",
     "course/modules/AC/AC4/L05.html lines 336, 350, 359",
     "PASS",
     "Re-derived r18: E1 265,000/140,000 = 1.8929 -> 1.893 and 189.3% (one decimal of the percent, 189.29); the sentence 'the fraction exceeds one because the flexible variance of -125,000 offsets part of it' checked (265,000 - 125,000 = 140,000). E3 1,300,000/1,160,000 = 1.120690 -> 112.1%; 140,000/1,160,000 = 0.120690 -> 12.1%. R1 prompt: 1,600 units split 0.6/0.4 = 960 and 640 (correct); the solution makes no claim about the split and says the function is not valid if a second shift adds fixed cost (consistent with Section 4)."),
    ("AC4-c-r18-L06-def12-model-scope", "2.9 scope: 'In this model material is the only variable cost' (changed Definition 1.2)",
     "course/modules/AC/AC4/L06.html line 65; L05.html line 63; tests/labs/AC4/lab-AC4-L05-1.py lines 19-22 (cost behaviour used here)",
     "PASS",
     "L05.html line 63: 'In this case the material is variable ... The fixed overhead is F', and the L05 twin docstring: 'Cost behaviour used here: material is variable ... Fixed overhead does not change with units'. So the only variable cost in the case is material, and the L06 scope sentence is supported by the page and the lab. The why-it-matters sentence (L06 line 52) carries the same scope."),
    ("AC4-c-r18-L05-hypothesis-1660-average", "2.5 lab hypothesis wording: '1,660 cents' per unit (changed L05 line 97)",
     "course/modules/AC/AC4/L05.html line 97; tests/labs/AC4/lab-AC4-L05-1.py output master_contribution 1660000",
     "PASS",
     "1,660 is the budget average contribution per budgeted unit (1,660,000 / 1,000, the printed master_contribution). The sentence attaches it to the parenthesis '1,660,000 cents on 1,000 budgeted units, as the lab prints', which is printed. The average is not printed as a per-unit number and not defined in L05 (it is defined as CMbar in L06 Definition 1.1), so the phrase is a prediction with its basis stated, not a result."),
    ("AC4-c-r18-scope-rescan", "2.9 scope words in changed and unchanged prose (only, every, all, exactly, same, about, raises, offsets, never, always)",
     "course/modules/AC/AC4/L05.html and L06.html visible prose (tags stripped; scan output in out/)",
     "PASS",
     "Each hit read in context: 'every step of the lab is whole-number arithmetic' (L05 section 3; twin uses integer cents and Fraction only for L06 mix); 'the lab raises an error if they do not' (decompose raises ValueError, L06 twin line 98-99); 'all mix' (misconception 1: SP = E = 0 at budget prices and standard kg, so T = M = 40,000); 'Lab 1's check line uses exactly these units' (check_on_mix uses 690 and 460); 'the same for any mix of those 1,300 units' (V depends only on Q_a: M3); 'the four terms always suffice' is a quiz distractor. No hit is unsupported."),
    ("AC4-c-r18-mutants-rerun", "2.5 lab mutants: re-run every earlier AC4-c mutant and alternative (r7, r8, r17)",
     "ledgers/AC4/mutants/AC4-c-r7, AC4-c-r8, AC4-c-r17; scripts/AC4-c-r18/out/rerun_all_mutants.out",
     "PASS",
     "All 30 earlier mutant files (AC4-c-r7 9, AC4-c-r8 14, AC4-c-r17 7) were run with python -I -W error against the page's expected block (run_mutants.py). 26 are killed (ValueError or DIFF). The two survivors are the m04 sales-price file in AC4-c-r7 and AC4-c-r8, recorded as FAIL in AC4-c-r17-m04-survivor and AC4-c-lab-L06-mutants. ne06 and ne07 print the expected block and are equivalent on Lab 1 (AC4-c-r17-ne-mutants). Alternatives alt01 (r7), alt01..alt05 (r8), alt06..alt08 (r17) all print the expected block."),
    ("AC4-c-r18-new-mutants", "2.5 at least 3 NEW student-error mutants of my own (round 18)",
     "ledgers/AC4/mutants/AC4-c-r18/r18_m01..m05; ledgers/AC4/scripts/AC4-c-r18/make_r18_mutants.py; out/r18_mutants.out",
     "PASS",
     "Five new non-equivalent student-error mutants, all killed: m01 mix contribution at actual prices (ValueError, residual), m02 volume at actual average contribution (ValueError, non-whole cents), m03 sales-price sign reversed (ValueError), m04 operating-profit variance omits the fixed-cost variance (DIFF: 150000 printed for 140000), m05 master budget fixed overhead taken at actual 510,000 (DIFF). The mutant files are committed under ledgers/AC4/mutants/AC4-c-r18/."),
    ("AC4-c-r18-equivalent-proof", "2.5 equivalent mutants need a proof row (r18 m06 and r17 ne06, ne07)",
     "ledgers/AC4/mutants/AC4-c-r18/r18_m06_L06_allowance_floor_equivalent.py; ledgers/AC4/mutants/AC4-c-r17/ne06, ne07",
     "PASS",
     "r18_m06 replaces the exact fraction 1150 x 600 / 1000 with floor division. Both products are whole on Lab 1 (690 and 460; 1150 x 600 = 690,000 and 1150 x 400 = 460,000 are divisible by 1000), so the printed output is unchanged (SAME). It is outside the printed inputs only: on other inputs with a fractional allowance the residual check raises ValueError (L06 twin lines 98-99). ne06 (literal 500 for the efficiency price) is equal to the actual price because the case states the actual price equals the standard (L05 twin docstring; L06 line 13). ne07 (budget shares to two places) is exact because 0.6 and 0.4 have two decimal places. These three stay out of the mutants list."),
    ("AC4-c-r18-alt-impl-3", "2.5 three NEW correct alternative implementations (over-constraint check)",
     "ledgers/AC4/mutants/AC4-c-r18/alts/alt_r18_a_L06_mix_scaled_integers.py, alt_r18_b_L06_price_and_efficiency_totals.py, alt_r18_c_L05_material_from_total_kg.py; out/r18_alts.out",
     "PASS",
     "a: the mix written as one scaled-integer sum over Q_b with a single division (Fraction, whole_cents check kept); b: sales price as a difference of two revenue totals and efficiency from total kilograms minus total standard allowance; c: L05 material computed from the total standard kilograms. All three print the expected block exactly (SAME). No test constraint in the twin rejects a correct alternative."),
    ("AC4-c-r18-embed-check", "2.5 embedded code equals the twins and expected blocks equal the run output (round 18)",
     "course/modules/AC/AC4/L05.html line 98-220 and L06.html line 113-244; scripts/AC4-c-r18/embed_and_expected_r18.py",
     "PASS",
     "html.unescape of the data-run code block equals the twin text (L05 and L06: True). The expected block equals the stdout of python -I -W error on each twin (True, True)."),
    ("AC4-c-r18-seed-no-network", "2.5 labs: no network, seeded, under 10 s in Pyodide (round 18)",
     "tests/labs/AC4/lab-AC4-L05-1.py, lab-AC4-L06-1.py; out/smoke.out",
     "PASS",
     "The twins import only dataclasses, typing and fractions and make no random or network calls (read in full); page_smoke runs both labs in the Pyodide runtime with 0.0 s per lab (out/smoke.out: 'lab lab-AC4-L05-1: 0.0 s', 'lab lab-AC4-L06-1: 0.0 s')."),
]
NOTES = [
    "Previous-round fragment: /tmp/fanout-frags/AC4-c.round17.json (pin fefbf8b). Delta fefbf8b..7143726 on this slice: L05.html lines 97, 336, 350, 359, 445; L06.html lines 52, 65, 259; cards.json AC4-c061 (front) and entries of other lessons; tests/labs/AC4 changes are L07 only (not this slice).",
    "Carried rows: only where the cited lines are byte-identical since fefbf8b; every row whose subject is one of the changed lines or a whole page is re-checked in round 18 and says so.",
    "Mutants: 33 student-error mutants in the list (r7 9, r8 14, r17 5, r18 5); 31 killed, 2 survivors (m04 in r7 and r8), recorded as FAIL. Equivalents (r17 ne06, ne07; r18 m06) are proof rows outside the list. Alternatives are not counted as mutants.",
    "Card c074 subject changed in 7143726 and the unchanged card no longer matches the lesson scope: FAIL AC4-c-r18-c074-scope.",
    "Lesson hours: L05 7 and L06 6; sum with L01..L08 is 50 = index data-hours-lessons 50. No pace estimate used.",
]
CNC = [
    "Full-repo pytest and mypy not run: only tests/test_labs.py, tests/test_run_labs.py and tests/test_page_checks.py with -k AC4 or run_labs or page_checks (57 passed) and mypy on the two twins.",
    "No external source consulted: neither lesson cites a registry key, and no published figure is checked.",
    "Browser visual rendering not checked beyond page_smoke (Chromium and Pyodide).",
    "The Lab 1 survivor (m04) is not fixed (verifier role: report, do not modify the lab). The card c074 is not edited.",
    "Project slices, grader and other AC4 lessons were outside this slice and were not re-verified.",
]

rows = []
for pid, prow in prev_rows.items():
    if pid in FAIL:
        st, ev, fix = FAIL[pid]
        rows.append({"id": pid, "check": prow["check"], "location": prow["location"], "status": st,
                     "evidence": ev, "fix": fix})
    elif pid in NEW:
        rows.append({"id": pid, "check": prow["check"], "location": prow["location"], "status": "PASS",
                     "evidence": NEW[pid]})
    elif pid in CARRY:
        rows.append({"id": pid, "check": prow["check"], "location": prow["location"], "status": "PASS",
                     "evidence": CARRY_PREFIX + prow["evidence"]})
    else:
        raise SystemExit(f"row {pid} has no round 18 decision")
rows.append({"id": "AC4-c-r18-c074-scope", "check": "2.9 card AC4-c074 scope (round 18 change to the contribution definition)",
             "location": "course/modules/AC/AC4/cards.json AC4-c074; course/modules/AC/AC4/L06.html line 65",
             "status": "FAIL", "evidence": FAIL["AC4-c-r18-c074-scope"][1], "fix": FAIL["AC4-c-r18-c074-scope"][2]})
for rid, check, loc, st, ev in [(r[0], r[1], r[2], r[3], r[4]) for r in EXTRA_ROWS]:
    rows.append({"id": rid, "check": check, "location": loc, "status": st, "evidence": ev})

# Rows whose round 17 evidence is replaced: keep ids; the fail rows above carry their own fix.
MUT_STATUS = {}
for line in open(f"{checkout}/ledgers/AC4/scripts/AC4-c-r18/out/rerun_all_mutants.out", encoding="utf-8").read().splitlines() + \
        open(f"{checkout}/ledgers/AC4/scripts/AC4-c-r18/out/r18_mutants.out", encoding="utf-8").read().splitlines():
    status, page, path = line.split(None, 2)
    MUT_STATUS[path] = (status, page)
mutants = []
for path, (status, page) in sorted(MUT_STATUS.items()):
    if "/alt" in path or path.endswith("ne06_L06_efficiency_at_actual_price_equivalent.py") or \
            path.endswith("ne07_L06_budget_shares_rounded_to_two_places.py") or \
            path.endswith("r18_m06_L06_allowance_floor_equivalent.py"):
        continue
    if status == "SAME":
        killed = ""
    elif status == "ERR":
        killed = "ValueError (non-zero exit, residual check)"
    else:
        killed = "DIFF from the page's expected block"
    mutants.append({"id": path.split("/", 1)[1].replace(".py", ""), "description": f"{page} student-error mutant ({path})",
                    "killed_by": killed, "file": f"ledgers/AC4/mutants/{path}"})
fragment = {
    "unit": "AC4", "slice": "AC4-c", "round": 18,
    "verifier": "independent Haiku verifier, slice AC4-c (L05, L06 and their lab twins), round 18; did not build AC4",
    "pin": "7143726", "base": "fefbf8b",
    "previous_ledger": "/tmp/fanout-frags/AC4-c.round17.json (pin fefbf8b)",
    "checkout": checkout, "scratch": "/tmp/AC4-v/AC4-c",
    "verified_at": "2026-10-28T00:00:00Z",
    "rows": rows, "mutants": mutants,
    "registry_flags": ["Live verify_refs --unit AC4: 2 of 560 entries, 0 problems; offline 560 entries, 0 problems; neither AC4-c page cites a registry key."],
    "freshness_flags": [],
    "notes": NOTES, "could_not_check": CNC,
}
fails = [r["id"] for r in rows if r["status"] != "PASS"]
fragment["summary"] = f"rows {len(rows)}: pass {len(rows)-len(fails)}, fail {len(fails)} ({', '.join(fails)}); mutants {len(mutants)}: killed {sum(1 for m in mutants if m['killed_by'])}"
fragment["verdict"] = "FAIL" if fails else "PASS"
json.dump(fragment, open(f"{checkout}/ledgers/AC4/AC4-c.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(fragment["summary"], fragment["verdict"])
