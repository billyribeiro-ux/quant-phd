"""Write the round-17 AC4-e fragment (ledgers/AC4/AC4-e.json) from the round-16 fragment and this round's evidence.

Run: .venv/bin/python -I <this file> <checkout>. Carries every round-16 row id; rows whose cited subject changed
are re-verified with new evidence; new rows are added. Verdict is computed (PASS only if every row PASS).
"""
import ast, glob, json, pathlib, re, sys
from datetime import datetime, timezone

ROOT = pathlib.Path(sys.argv[1])
OUT = ROOT / "ledgers/AC4/scripts/AC4-e-r17/out"
prev = json.load(open("/tmp/fanout-frags/AC4-e.round16.json", encoding="utf-8"))
CARRY = ("Carried from round 16 (course/modules/AC/AC4/project.html, grader/, tests/labs/AC4, L01-L08.html, index.html, "
         "references/ and tools/ byte-identical since the previous pin c093bf5; cards.json objects byte-identical except "
         "AC4-c004, c008, c017, c044, c058, c061, c063, c073, c125, c129): ")

# Re-verified rows: id -> (status, check, location, evidence, fix)
RE = {
 "proj-autograder-rerun-mutants-m01-m37": ("PASS", None, "ledgers/AC4/mutants (125 .py files)",
   "Re-run round 17 on seeds 0-49 (ledgers/AC4/scripts/AC4-e-r17/out/mutate_all_r17.out, new_mutants_r17.out): 121 prior mutants KILLED and 4 new r17e_01..04 KILLED; 0 survivors among 125.", None),
 "proj-mutant-descriptions": ("PASS", None, "ledgers/AC4/mutants/ (125 files)",
   "ast scan of all 125 top-level mutants (round 17): every file has a module docstring whose first line names the error (the 121 older ones name the error, e.g. 'Mix variance omitted: ...'; the four new ones begin 'Student error:').", None),
 "proj-r14-mutants-all-rerun": ("PASS", None, "ledgers/AC4/mutants (125 .py files)",
   "Re-run round 17 on all 125 top-level files (mutate_all_r17.out + new_mutants_r17.out): 125 KILLED, 0 PASS.", None),
 "proj-r15-mutants-all-rerun": ("PASS", None, "ledgers/AC4/mutants/*.py (125 files)",
   "Re-run round 17: 125 of 125 KILLED on seeds 0-49 (mutate_all_r17.out 121 lines KILLED, new_mutants_r17.out 4 KILLED).", None),
 "proj-autograder-reference": ("PASS", None, "course/modules/AC/AC4/grader/reference.py; test_project.py",
   "run_graders.py --unit AC4 --seeds 0-49: 'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.3 s)', rc=0 (out/run_graders.out).", None),
 "proj-collect-count": ("PASS", None, "course/modules/AC/AC4/project.html line 265; grader/test_project.py",
   "collect-only in the reference workspace: '527 tests collected' (out/collect.out class run this round, via AC4-e-r17/collect.py); also 527 on seeds 0, 7, 23, 49 (out/collect_seeds_r17.out).", None),
 "proj-r15-grader-count-527": ("PASS", None, "course/modules/AC/AC4/project.html line 265; grader/test_project.py",
   "Re-run: 527 on seeds 0, 7, 23, 49 (out/collect_seeds_r17.out); project.html line 265 states 527 checks.", None),
 "proj-r12-count-matches-page": ("PASS", None, "course/modules/AC/AC4/project.html line 265; grader/test_project.py",
   "Re-run: collected count 527 on every sampled seed (out/collect_seeds_r17.out) equals the page's '527 checks'.", None),
 "proj-check-pages": ("PASS", None, "course/modules/AC/AC4/*.html and cards.json",
   "check_pages.py --all: 'check_pages AC4: PASS' and rc=0 (out/check_pages.out), with cards.json at 134 cards.", None),
 "proj-check-dag": ("PASS", None, "course/modules/AC/AC4/",
   "check_dag.py --all: 'check_dag AC4: PASS', rc=0 (out/check_dag.out).", None),
 "proj-check-projects": ("PASS", None, "course/modules/AC/AC4/project.html",
   "check_projects.py --all: 'check_projects AC4: PASS', rc=0 (out/check_projects.out).", None),
 "proj-page-smoke": ("PASS", None, "course/modules/AC/AC4/project.html",
   "page_smoke.py --unit AC4 --pages project.html: 'page_smoke AC4: PASS', rc=0 (out/page_smoke_project.out).", None),
 "proj-ruff-mypy": ("PASS", None, "course/modules/AC/AC4/grader; tests/labs/AC4; repository mypy configuration",
   "ruff check and ruff format --check on the grader and the AC4 labs: 'All checks passed!', '14 files already formatted'; mypy --no-incremental: 'Success: no issues found in 153 source files' (out/ruff_mypy.out).", None),
 "proj-run-labs-ac4": ("PASS", None, "tests/labs/AC4",
   "run_labs.py --unit AC4: 'run_labs AC4: PASS (10/10)', rc=0 (out/run_labs.out).", None),
 "proj-run-graders-ac4": ("PASS", None, "course/modules/AC/AC4/grader",
   "run_graders.py --unit AC4 --seeds 0-49: PASS, rc=0 (out/run_graders.out).", None),
 "proj-r13-verify-refs": ("PASS", None, "references/references.json; course/modules/AC/AC4/project.html reading list",
   "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' rc=0; verify_refs.py --unit AC4 (live): '2 of 560 entries, 0 problems' rc=0 (out/verify_refs_*.out).", None),
 "proj-cards-structure": ("PASS", "cards.json is well formed: 134 cards, unique ids, lesson and grade values valid",
   "course/modules/AC/AC4/cards.json (134 cards)",
   "Re-run round 17: 134 cards, 134 unique ids; every lesson is one of L01-L08; every grade is T or C or absent (grade is optional in check_pages.py line 386-388); check_pages AC4 PASS (out/check_pages.out). The round-16 count of 131 is now 134: AC4-c132, c133 and c134 were added.", None),
 "proj-cards-duplicates": ("PASS", None, "course/modules/AC/AC4/cards.json",
   "Re-run round 17: no duplicate front and no duplicate back among the 134 cards (python scan).", None),
 "proj-banned-phrases": ("PASS", None, "course/modules/AC/AC4/project.html; course/modules/AC/AC4/cards.json (13 changed objects)",
   "Re-run round 17 (out/banned_cards_r17.out): the banned-phrase scan of all 134 cards and of project.html prose gives 0 hits; the 13 changed card objects contain only 'all' (inside 'fall') and 'same' (a comparison), neither banned.", None),
 "proj-cards-changed-lessons": ("PASS", None, "cards.json cards from L05 and L06 (AC4-c059..c068 and the L06 cards, including AC4-c073); L05.html; L06.html",
   "Re-verified: AC4-c061 (L05, Definition 1.3 content) and AC4-c063 (L05 lab output) and AC4-c073 (L06 line 98) match their lessons on content; the scope of AC4-c061 is a separate FAIL row (proj-r17-cards-c061-scope). L05/L06 lessons are byte-identical to c093bf5.", None),
 "proj-cards-changed-lessons-r10": ("PASS", None, "cards.json AC4-c059..c068; L05/L06 ids unchanged",
   "Re-verified this round: AC4-c061 and AC4-c063 (the two changed objects in c059..c068) match L05 (Definition 1.3 at L05.html line 58-59; Lab 1 output lines 224-229 and L05.html line 267). The other objects in the range are byte-identical.", None),
 "proj-cards-targeted": ("PASS", None, "cards.json (c062, c063, c064, c066, c067, c075, c076)",
   "Re-verified: AC4-c063 gives 500,000 cents at 1,150 units, matching flexed fixed 500000 at actual units 1150 in out/lab-AC4-L05-1.out line 9 and L05.html line 267; c062, c064, c066, c067, c075, c076 are byte-identical objects (carried).", None),
 "proj-cards-r10-L02": ("FAIL", "proj-cards-r10-L02", "cards.json AC4-c029, c125; L02.html lines 252-257, 264",
   "AC4-c029 matches L02 (byte-identical). AC4-c125 (changed this delta) says '89 units. The arithmetic is Proposition 4.1 applied to the Lab 1 inputs.' The lab prints both single_formula_break_even_units 88.89 (Proposition 4.1) and first_whole_unit 89 (whole-unit rule, Remark 2.3, L02.html line 81); Proposition 4.1 alone gives 88.89 (out/lab-AC4-L02-1.out line 2). See proj-r17-cards-c125-attribution.",
   "Re-attribute AC4-c125 to Proposition 4.1 (88.89) and Remark 2.3 (rounding up to 89); see proj-r17-cards-c125-attribution fix."),
 "proj-card-c061": ("PASS", "AC4-c061 (changed front, lesson L05) matches L05 Definition 1.3", "cards.json line 434-436 (AC4-c061 back is unchanged); L05.html lines 58-59",
   "Back text is byte-identical to L05 Definition 1.3 (line 59). Content matches. The changed front is judged for scope in proj-r17-cards-c061-scope (FAIL).", None),
 "proj-card-c129": ("PASS", None, "cards.json line 914 (AC4-c129); L08.html line 128",
   "Re-verified: AC4-c129 is now the X-only card 'X has residual income of 15 SCU (C = 500, OI = 60, r = 9%).' L08.html line 128: RI_X = 60 - 0.09 x 500 = 15 (60 - 45). Matches; Y moved to AC4-c134.", None),
 "proj-r13-card-c073-scope": ("PASS", None, "course/modules/AC/AC4/cards.json line 518-521 (AC4-c073, back); L06.html line 98",
   "Re-verified: AC4-c073 back now ends '(Definition 1.2; Proposition 2.2(c)).' with the counterexample sentence removed; Proposition 2.2(c) (L06.html line 98) states E is negative when sum kg > sum s q; the zero-E counterexample now lives in AC4-c133 (T). Matches.", None),
 "proj-autograder-alternatives": ("PASS", None, "course/modules/AC/AC4/grader/test_project.py; ledgers/AC4/scripts/AC4-e-r17/out/prior_alts_and_scope_r17.out",
   "Re-run round 17 on seeds 0-49: alt_r12_a..e, alt13_a/b, alt14_a/b, alt15_a/b/c PASS 50/50; alt_l, alt_a..j (student-error refusals of tuples and read-only mappings) KILLED; new alt17_a/b/c PASS 50/50 (alts_r17.out).", None),
 "proj-alt-l-extra-keys": ("PASS", None, "ledgers/AC4/scripts/AC4-e-r10/alt_l.py; course/modules/AC/AC4/grader/test_project.py",
   "Re-run round 17: alt_l KILLED by test_products_that_are_not_a_list_raise_value_error[tuple-master_budget] (prior_alts_and_scope_r17.out); the page's 'a list of mappings' requires refusing a tuple of products.", None),
 "proj-autograder-alt-decimal": ("PASS", None, "ledgers/AC4/scripts/AC4-e-r12/alt_r12_a_decimal_half_up.py; AC4-e-r15/alts/alt15_a_decimal_half_up.py",
   "Re-run round 17: alt_r12_a and alt15_a PASS 50/50 seeds.", None),
 "proj-r12-alternatives-new": ("PASS", None, "ledgers/AC4/scripts/AC4-e-r12/alt_r12_a..e",
   "Re-run round 17: alt_r12_a..e PASS 50/50 each (prior_alts_and_scope_r17.out).", None),
 "proj-r13-alternatives-new": ("PASS", None, "ledgers/AC4/scripts/AC4-e-r13/alts/alt13_a, alt13_b",
   "Re-run round 17: alt13_a and alt13_b PASS 50/50 each.", None),
 "proj-r14-alternatives-correct": ("PASS", None, "ledgers/AC4/scripts/AC4-e-r14/alts/alt14_a, alt14_b",
   "Re-run round 17: alt14_a and alt14_b PASS 50/50 each.", None),
 "proj-alt-g-student-error": ("PASS", None, "ledgers/AC4/scripts/AC4-e-r8/alt_g.py",
   "Re-run round 17: alt_g KILLED by test_products_that_are_not_a_list_raise_value_error[number-master_budget] (seed 0).", None),
 "proj-r15-alternatives-correct-new": ("PASS", None, "ledgers/AC4/scripts/AC4-e-r15/alts/alt15_a, alt15_b, alt15_c",
   "Re-run round 17: alt15_a, alt15_b, alt15_c PASS 50/50 each.", None),
 "proj-lab-1": ("PASS", None, "course/modules/AC/AC4/project.html lines 53-147; tests/labs/AC4/lab-AC4-project-1.py",
   "Twin run under python -I -W error: rc=0; its output equals the page's expected block (lines 137-145) line for line (out/labs_vs_page_r17.out 'lab 1: output==page expected: True').", None),
 "proj-lab-2": ("PASS", None, "course/modules/AC/AC4/project.html lines 149-243; tests/labs/AC4/lab-AC4-project-2.py",
   "Twin run: rc=0; its output equals the page expected block (lines 233-241). The page's blanked code differs from the twin only in the three blanks (efficiency, actual_mix_margin, mix), per the diff in out/labs_vs_page_r17.out.", None),
 "proj-r12-mutant-m60-scope": ("PASS", None, "ledgers/AC4/scripts/AC4-e-r12/out_of_scope/m60_case_name_pairs_refused.py",
   "Re-run round 17: m60 PASS 50/50 (survives, as before). The page says a name that 'appears twice' is refused, not that case differences do; the grader does not test case-differing names, so the survivor is out of scope (prior_alts_and_scope_r17.out).", None),
}

NEW = []
def row(i, status, check, location, evidence, fix=None):
    r = {"id": i, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        r["fix"] = fix
    NEW.append(r)

row("proj-r17-delta-scope", "PASS", "Round-17 delta for AC4 is confined to cards.json (pin c093bf5 to fefbf8b)",
    "course/modules/AC/AC4/cards.json; git diff c093bf5 fefbf8b over project.html, grader, tests/labs/AC4, L01-L08, index.html, references, tools",
    "git diff --quiet c093bf5 fefbf8b -- course/modules/AC/AC4/project.html course/modules/AC/AC4/grader tests/labs/AC4 course/modules/AC/AC4/L0*.html course/modules/AC/AC4/index.html references tools: IDENTICAL. Card-level comparison of cards.json at c093bf5 and fefbf8b (python): 0 removed, 3 added (AC4-c132, c133, c134), 10 changed (AC4-c004, c008, c017, c044, c058, c061, c063, c073, c125, c129), 121 byte-identical objects.")
row("proj-r17-cards-c004", "PASS", "AC4-c004 back after the tie sentence was removed still matches L01 Definition 3.1",
    "cards.json lines 21-25 (AC4-c004); L01.html lines 111-116 (Definition 3.1)",
    "The back gives v-hat, F-hat, H with highest activity, L with lowest, Q_H != Q_L, and 'the two months H and L and no others'. Definition 3.1 (L01.html lines 112-114) states the same formulas and condition and 'uses only the two extreme months'. The removed tie rule is now carried by AC4-c132, which matches Definition 3.1's tie sentence.")
row("proj-r17-cards-c008", "FAIL", "AC4-c008 back: 'In Lab 1 the largest residual is 514.73 USD' names what Lab 1 prints",
    "cards.json AC4-c008 back; L01.html line 238 and line 283; out/lab-AC4-L01-1.out lines 6, 12 and 17",
    "Lab 1 prints 'largest absolute residual_cents 51473' (out/lab-AC4-L01-1.out line 17; L01.html line 238). 51473 cents = 514.73 USD is the absolute value of month 1's residual -51473 (out line 6). The largest signed residual is +11065 cents (month 7, out line 12) = 110.65 USD. The card's bare 'largest residual' therefore gives the absolute figure under the signed label. The lesson's line 283 has the same loose wording (outside this slice).",
    "Change the back to 'In Lab 1 the largest absolute residual is 514.73 USD, so ...' (the lab's own label, out line 17). The lesson sentence at L01.html line 283 should get the same word (owner: L01).")
row("proj-r17-cards-c017", "PASS", "AC4-c017 margin of safety, parenthesised form, matches L02 Definition 3.1",
    "cards.json lines 113-117 (AC4-c017); L02.html line 93 (Definition 3.1)",
    "Back: 'As a share of plan it is (plan less Q*) divided by the plan.' Definition 3.1 (L02.html line 93) gives (Q_plan - Q*)/Q_plan. The change is parentheses only; the units figure and the 'fall before operating income reaches zero' sentence match line 93.")
row("proj-r17-cards-c044", "PASS", "AC4-c044 (grade C) back, with its convention sentence removed, still matches L03",
    "cards.json lines 311-316 (AC4-c044); L03.html lines 367-370 (Section 5 assumptions), line 516 (summary table)",
    "Back: 'the right test for a one-year decision whose effects are the cash flows named here, under the assumptions of Section 5.' Section 5 (L03.html line 367-370) lists four assumptions and says 'The model is one year and has no discounting.' The basis field still records that the rule is a convention with no registry source, so the grade and basis stay C.")
row("proj-r17-cards-c058", "PASS", "AC4-c058 (grade C) back still matches L04 Definition 1.1 stage one",
    "cards.json lines 414-419 (AC4-c058); L04.html line 59 (Definition 1.1), line 481 (summary table)",
    "Back: 'The activity method, which assigns each pool by its own driver (Definition 1.1, stage one).' Definition 1.1 stage one (L04.html line 59) assigns each activity pool 'in proportion to each product's count of that pool's driver'. The convention statement is kept in the basis field ('Convention stated in Definition 1.1 (stage one)').")
row("proj-r17-cards-c061-scope", "FAIL", "AC4-c061 front 'What sign convention is used for variances?' keeps the lesson's scope",
    "cards.json AC4-c061 front (line 436); L05.html line 59 (Definition 1.3: 'Every variance in this lesson is stated as ...')",
    "Round 16 read 'What sign convention does this lesson use for variances?'. The rewrite drops 'this lesson', so the question asks about variances in general. Definition 1.3 states the convention for 'every variance in this lesson' and says the convention applies in L06; the lesson does not claim it is the convention of all variance analysis. The back's 'A variance is actual minus budget ...' is then presented as general.",
    "Restore the scope in the front: 'What sign convention does this lesson use for variances?' (or 'in Lesson L05'). The back is correct as it stands.")
row("proj-r17-cards-c063", "PASS", "AC4-c063 'flexed fixed overhead at 1,150 units is 500,000 cents, the same as the master budget at 1,000 units'",
    "cards.json AC4-c063 back (line 448-452); out/lab-AC4-L05-1.out line 9 and line 14; L05.html line 267",
    "Lab 1 prints 'flexed_revenue 3325000 material 1400000 fixed 500000' for actual_units 1150 (out line 9; 'actual_units 1150' printed earlier). The master fixed figure is not printed as a field; L05.html line 267 derives it: printed master_contribution 1660000 less master_operating_profit 1160000 = 500000. The card's words 'In Lab 1' cover both figures; the derivation is on the lesson page.")
row("proj-r17-cards-c073", "PASS", "AC4-c073 back: efficiency sign rule and the Proposition 2.2(c) reference",
    "cards.json lines 518-521 (AC4-c073 back); L06.html lines 64-72 (Definition 1.2), line 56 (pi), line 98 (Proposition 2.2(c))",
    "'E = -pi x sum over the products of (kg_a,i - s_i q_a,i), where pi is the standard price per kilogram' matches Definition 1.2 with pi defined on L06.html line 56. 'Total kilograms used above the total standard allowance for the actual output make E negative (Definition 1.2; Proposition 2.2(c))': (c) says E is negative when sum kg > sum s q with pi > 0; since E = -pi (sum kg - sum s q), this is an exact sign rule, and the card uses the sufficient direction the proposition states.")
row("proj-r17-cards-c125-attribution", "FAIL", "AC4-c125 'The arithmetic is Proposition 4.1 applied to the Lab 1 inputs' attributes the rounding to 89 to Proposition 4.1",
    "cards.json AC4-c125 back (line 883-886); L02.html line 81 (Remark 2.3, whole units), line 121-130 (Proposition 4.1); out/lab-AC4-L02-1.out lines 2-3",
    "Proposition 4.1 gives the zero of the lower segment: 1,200 / 13.50 = 88.89 (lab prints single_formula_break_even_units 88.89). The whole-volume answer 89 needs the ceiling rule of Remark 2.3 ('the smallest whole volume with OI >= 0 is ceil(Q*)'; L02.html line 81), which the lab prints separately as first_whole_unit 89. The card attributes the whole arithmetic to Proposition 4.1, which is incomplete.",
    "Replace the back with: '89 units. Proposition 4.1 gives the lower-segment break-even of 88.89 units for the Lab 1 inputs, and Remark 2.3 rounds it up to the first whole unit, 89.' Keep grade C with basis Lab 1 (SIMULATED).")
row("proj-r17-cards-c132", "PASS", "AC4-c132 (new, lesson L01): tie on the highest activity takes the earliest such month",
    "cards.json AC4-c132 (lines 935-939); L01.html line 114 (Definition 3.1 tie sentence), lines 177-178 (high_low docstring) and the lab code max/min keys",
    "Definition 3.1 (L01.html line 115): 'A tie on the highest activity takes the earliest such month, and the same rule applies to the lowest.' The card says the same. The lab code selects the earliest tie: high = max(..., key=(activity, -i)) and low = min(..., key=(activity, i)) (L01.html high_low, lines 170-190), so the printed lab output is consistent with the rule.")
row("proj-r17-cards-c133", "PASS", "AC4-c133 (new, lesson L06, T): offsetting excess and shortfall leave E at zero",
    "cards.json AC4-c133; L06.html line 98 (Proposition 2.2 counterexample), line 64-72 (Definition 1.2)",
    "Front: one product 50 kg above and another 50 kg below its allowance. E = -pi (50 + (-50)) = 0. The back says exactly this and 'neither product uses its standard kilograms', which is the premise. L06.html line 98 proves the same counterexample ('the sum in Definition 1.2 is zero, so E = 0, while kg != s q for each product'). Grade T matches the proposition's proof.")
row("proj-r17-cards-c134", "PASS", "AC4-c134 (new, lesson L08, T): division Y residual income 20 SCU",
    "cards.json AC4-c134; L08.html line 128",
    "L08.html line 128: 'Division Y has C = 2,000 and OI = 200 ... RI_Y = 200 - 180 = 20'. The card's C, OI and r match; grade T matches the arithmetic (200 - 0.09 x 2000 = 20).")
row("proj-r17-cards-counts", "PASS", "cards.json: 134 cards, the changed set is exactly the 10 changed and 3 added objects, no duplicates",
    "course/modules/AC/AC4/cards.json",
    "Python comparison of cards.json at c093bf5 and fefbf8b: changed = AC4-c004, c008, c017, c044, c058, c061, c063, c073, c125, c129; added = c132, c133, c134; removed = none. Current file: 134 objects, unique ids and fronts and backs, all ids sorted. Grade values present are T or C; 34 objects carry no grade (optional per check_pages.py).")
row("proj-r17-banned-and-numbers", "PASS", "Every number in the 13 changed or added card objects appears in its lesson; no banned phrase",
    "cards.json (13 objects); L01-L08.html; out/banned_cards_r17.out",
    "Numbers checked by string match against the cited lesson: 514.73 (L01), 51,473 cents, 500,000, 1,150, 1,000, 89, 88.89 (L02 lab), 15, 20, 60, 200, 500, 2,000, 9 percent (L08 line 128), 50 kg (L06 line 98). Banned-phrase scan of the card texts: 0 hits (out/banned_cards_r17.out).")
row("proj-r17-mutants-new-student-errors", "PASS", "Four new student-error mutants written this round are each killed",
    "ledgers/AC4/mutants/r17e_01_flexed_budget_uses_actual_mix.py; r17e_02_flexed_fixed_overhead_scales_with_units.py; r17e_03_efficiency_on_budget_average_standard.py; r17e_04_flexible_units_report_budget_units.py",
    "Each is a complete budget_engine.py generated from grader/reference.py by one exact edit (ledgers/AC4/scripts/AC4-e-r17/make_r17.py; each edit must match once). Killed on seeds 0-49 (out new_mutants_r17.out): r17e_01 by test_every_grader_seed_reconciles_exactly[30]; r17e_02 by test_every_grader_seed_reconciles_exactly[30]; r17e_03 by test_every_grader_seed_reconciles_exactly[30]; r17e_04 by test_flexed_at_actual_total_matches_oracle. The page's Constraints and Required outputs require the flexed budget at the budgeted mix (project.html lines 254-260, Required outputs and Conventions), flexed fixed overhead unchanged (line 259-260 and the Conventions), and the efficiency standard per product (line 259).")
row("proj-r17-alternatives-new", "PASS", "Three new correct alternatives pass the whole suite on seeds 0-49",
    "ledgers/AC4/scripts/AC4-e-r17/alts/alt17_a_divmod_nearest_cent.py; alt17_b_efficiency_and_mix_restated.py; alt17_c_truncate_after_half.py",
    "alt17_a rounds by divmod (q + 1 if 2r >= d); alt17_b restates efficiency and the actual-mix contribution as totals over products; alt17_c uses int(x + 1/2) (exact for the non-negative amounts, as the page states). Each derived from grader/reference.py by one exact edit (make_r17.py). All three: PASS 50/50 seeds (out/alts_r17.out).")
row("proj-r17-mutants-all-rerun", "PASS", "Every committed AC4 mutant is re-run and killed on seeds 0-49",
    "ledgers/AC4/mutants/*.py (125 files)",
    "runfiles.py on all 125 top-level mutants (mutate_all_r17.out): 125 KILLED, 0 PASS. Survivors: none. The four new ones are in new_mutants_r17.out.")
row("proj-r17-prior-alts-rerun", "PASS", "Every prior alternative and the out-of-scope case-name script are re-run",
    "ledgers/AC4/scripts/AC4-e-r12/alt_r12_a..e; AC4-e-r13/alts; AC4-e-r14/alts; AC4-e-r15/alts; AC4-e-r10/alt_l.py; AC4-e-r8/alt_a..j; AC4-e-r12/out_of_scope/m60",
    "out/prior_alts_and_scope_r17.out: every correct alternative PASS 50/50 (r12 a-e, r13 a/b, r14 a/b, r15 a/b/c, r8 alt_e); every student-error refusal KILLED (alt_l, alt_a, b, c, f, g, h, i, j). m60 PASS 50/50 (out of scope, see proj-r12-mutant-m60-scope).")
row("proj-r17-labs-vs-page", "PASS", "Both project labs: twin output equals the page, and the page's lab-2 code differs from its twin only in the three blanks",
    "course/modules/AC/AC4/project.html lines 56-145 and 152-241; tests/labs/AC4/lab-AC4-project-1.py, -2.py",
    "Both twins run under python -I -W error with rc=0. Output of each equals the page expected block (out/labs_vs_page_r17.out). The blanked page code differs from the twin only at 'efficiency = ___', 'actual_mix_margin = ___' and 'mix = ___' (diff printed).")
row("proj-r17-collect-seeds", "PASS", "Grader collect count 527 on seeds 0, 7, 23, 49",
    "course/modules/AC/AC4/grader/test_project.py; out/collect_seeds_r17.out",
    "QF_SEED set; pytest --collect-only in the reference workspace: 527 each seed.")
row("proj-r17-mutant-docstrings", "PASS", "Every top-level mutant carries a module docstring that names its error",
    "ledgers/AC4/mutants/*.py (125 files)",
    "ast.get_docstring on all 125: each has a docstring, and the first line names the error. The four new ones start 'Student error:'.")

# Assemble
rows = []
seen = set()
for r in prev["rows"]:
    i = r["id"]
    if i in RE:
        status, check, loc, ev, fix = RE[i]
        rr = {"id": i, "check": check or r["check"], "location": loc if loc else r["location"], "status": status,
              "evidence": ev}
        if fix:
            rr["fix"] = fix
    else:
        rr = {"id": i, "check": r["check"], "location": r["location"], "status": r["status"],
              "evidence": CARRY + r["evidence"]}
    rows.append(rr)
    seen.add(i)
for r in NEW:
    assert r["id"] not in seen, r["id"]
    rows.append(r)
assert len(rows) == len(set(x["id"] for x in rows))

# mutants
killed = {}
for line in open(OUT / "mutate_all_r17.out", encoding="utf-8"):
    m = re.match(r"KILLED (\S+) -> (.*)$", line.strip())
    if m:
        killed[m.group(1)] = m.group(2)
new_k = {}
for line in open(OUT / "new_mutants_r17.out", encoding="utf-8"):
    m = re.match(r"KILLED (\S+) -> (.*)$", line.strip())
    if m:
        new_k[m.group(1)] = m.group(2)
muts = []
prev_m = {m["file"].split("/")[-1]: m for m in prev["mutants"]}
for p in sorted(glob.glob(str(ROOT / "ledgers/AC4/mutants/*.py"))):
    name = pathlib.Path(p).name
    doc = ast.get_docstring(ast.parse(open(p, encoding="utf-8").read())) or ""
    desc = doc.split("\n")[0].strip()
    kb = killed.get(name) or new_k.get(name)
    assert kb, name
    muts.append({"id": name[:-3], "file": f"ledgers/AC4/mutants/{name}", "description": desc, "killed_by": kb})
assert len(muts) == 125, len(muts)

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
cnt = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag = {
 "unit": "AC4", "slice": "AC4-e", "round": 17,
 "verifier": "Claude Haiku 5.5 (independent verifier, round 17, slice AC4-e; did not build AC4)",
 "pin": "fefbf8b", "base": "c093bf5 (round-16 fragment pin; the course delta since c5daab2 is the same cards.json change)",
 "checkout": str(ROOT), "scratch": "/tmp/ac4-v/e17",
 "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
 "verdict": verdict,
 "rows": rows, "mutants": muts, "registry_flags": [], "freshness_flags": [],
 "notes": ("Delta c093bf5..fefbf8b for this slice is cards.json only: 10 objects changed, 3 added (AC4-c132, c133, c134). "
           "project.html, grader/, tests/labs/AC4, L01-L08, index.html, references and tools are byte-identical. "
           "Round-16 rows are carried with the 'Carried from round 16' prefix unless their cited subject changed, in which case they were re-verified. "
           "Two FAIL rows concern rewritten card text (c008 'largest residual' for the lab's 'largest absolute residual'; c125 attribution of 89 to Proposition 4.1 alone) and one concerns scope (c061 front). "
           "Lesson L01.html line 283 repeats the c008 wording (outside this slice, owner L01). "
           "The mutants are all killed; the four new student-error mutants and three new correct alternatives were written this round by make_r17.py."),
 "summary": {"rows": len(rows), "pass": cnt["PASS"], "fail": cnt["FAIL"], "unverifiable": cnt["UNVERIFIABLE"],
             "mutants_killed": len(muts), "mutants": len(muts)},
}
out = ROOT / "ledgers/AC4/AC4-e.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, frag["summary"], verdict)
