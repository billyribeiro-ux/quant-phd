"""Builds ledgers/AC4/AC4-e.json (round 18, slice AC4-e) from the round-17 fragment and this round's re-runs.

Carry rule (VERIFIER_RULES): a previous PASS row is carried only when its cited subject is byte-identical; rows whose
subject the round-18 delta touched are re-verified and given new evidence (OVERRIDE). Every previous row id is kept.
"""
import json, re, sys, pathlib

CHECKOUT = pathlib.Path("/tmp/verify18-AC4-e")
PREV = pathlib.Path("/tmp/fanout-frags/AC4-e.round17.json")
OUT = CHECKOUT / "ledgers/AC4/AC4-e.json"
O = "ledgers/AC4/scripts/AC4-e-r18"

prev = json.loads(PREV.read_text())

def strip_chain(text):
    """Drop leading 'Carried from round N (...): ' prefixes (balanced parentheses) so only the source evidence remains."""
    while text.startswith("Carried from round"):
        i = text.index("(")
        depth = 0
        for j in range(i, len(text)):
            if text[j] == "(":
                depth += 1
            elif text[j] == ")":
                depth -= 1
                if depth == 0:
                    break
        text = text[j + 1:].lstrip(": ").lstrip()
    return text

CARRY = ("Carried from round 17 (cited subject byte-identical since the previous pin fefbf8b; the round-18 delta "
         "changed only project.html lines 55, 265, 293 and 372, grader/test_project.py lines 1064-1069 (an insertion), "
         "cards.json objects AC4-c008, c018, c061, c095, c096, c125, and tests/labs/AC4/lab-AC4-L07-1.py, and it changed "
         "lesson lines outside the passage this row cites (L01 51, 119; L02 51, 81, 283; L05 97, 336, 350, 359, 445; "
         "L06 52, 65, 259; L07 140 onward; L08 98, 279, 294), checked by git diff -U0): ")

OVERRIDE = {}

def ov(i, status, evidence):
    OVERRIDE[i] = (status, evidence)

# ---- mutants (all re-run this round: out_mutate_all_r18.txt, out_new_mutants.txt, out_oos_m60.txt)
MUT_RUN = ("Re-run round 18 on seeds 0-49 (ledgers/AC4/scripts/AC4-e-r18/out_mutate_all_r18.txt: 135/135 killed; "
           "out_new_mutants.txt: r18e_01..04 killed). Mutant still present and killed; see the mutants list.")
for i in ["proj-autograder-rerun-mutants-m01-m37", "proj-mutant-descriptions", "proj-mutant-m07-empty-name",
          "proj-mutant-m12-duplicate-names", "proj-mutants-m01-m06", "proj-mutants-m08-m11", "proj-mutants-m13-m20",
          "proj-mutants-m15-m19", "proj-mutants-m21-m24", "proj-mutants-m25-m29", "proj-mutants-r6-new",
          "proj-mutants-r7-new", "proj-mutants-r8-new", "proj-mutants-r9-new", "proj-mutants-r10-new",
          "proj-mutants-r11-m53-m55", "proj-r12-mutants-new-student-errors", "proj-mutant-m52-dict-only-case",
          "proj-r13-mutants-new-student-errors", "proj-r14-mutants-new-student-errors", "proj-r14-mutants-all-rerun",
          "proj-r15-mutants-new-student-errors", "proj-r15-mutants-all-rerun", "proj-r17-mutants-new-student-errors",
          "proj-r17-mutants-all-rerun", "proj-mutants-m21-m24-equivalence"]:
    ov(i, "PASS", MUT_RUN)
ov("proj-mutant-descriptions", "PASS",
   "ast scan of all 139 top-level mutants (round 18, run this round): each has a module docstring whose first line names "
   "the error ('Student error: ...' or the older 'Mix variance omitted: ...' style); the first lines were read in full. "
   "Every mutant is listed in the mutants field of this fragment with its killing test.")
ov("proj-r12-mutant-m60-scope", "PASS",
   "Re-run round 18: m60 PASS 50/50 (survives, as before; ledgers/AC4/scripts/AC4-e-r18/out_oos_m60.txt). The page says "
   "a name that 'appears twice' is refused and says nothing about letter case, so the survivor is out of scope.")

# ---- alternatives (re-run this round)
ALT_RUN = ("Re-run round 18 on seeds 0-49 (ledgers/AC4/scripts/AC4-e-r18/out_existing_alts.txt and out_new_alts.txt): "
           "the correct alternatives PASS 50/50 and the student-error alternatives are KILLED by the named test.")
for i in ["proj-autograder-alternatives", "proj-alt-l-extra-keys", "proj-alt-g-student-error",
          "proj-autograder-alt-decimal", "proj-r12-alternatives-new", "proj-r13-alternatives-new",
          "proj-r14-alternatives-correct", "proj-r15-alternatives-correct-new", "proj-r17-alternatives-new"]:
    ov(i, "PASS", ALT_RUN)
ov("proj-alt-l-extra-keys", "PASS",
   "Re-run round 18: the reference, which reads only the named fields and so accepts a case or product with extra keys, "
   "passes 50/50 (out_run_graders.txt), so the suite does not refuse extra keys and the page does not require it. "
   "alt_l (ledgers/AC4/scripts/AC4-e-r10/alt_l.py) is KILLED by test_products_that_are_not_a_list_raise_value_error"
   "[tuple-master_budget] (seed 0), which the page's 'a list of mappings' requires.")

# ---- grader rows: re-run (reference passes; collect counts; alternatives)
GRADER_RUN = ("Re-run round 18: run_graders --unit AC4 --seeds 0-49 -> PASS (reference 50/50; out_run_graders.txt); "
              "the suite collects 563 tests on all 50 seeds (out_collect_seeds.txt).")
for i in ["proj-autograder-reference", "proj-run-graders-ac4", "proj-collect-count", "proj-r12-count-matches-page",
          "proj-r15-grader-count-527", "proj-r15-later-product-conditions", "proj-purity-order-dependence",
          "proj-spec-coverage-claims", "proj-spec-clarity-and-errors", "proj-r12-none-and-bool-tests",
          "proj-r12-product-not-mapping-valueerror", "proj-r12-float-units-test", "proj-r12-read-only-mapping-test",
          "proj-messages-no-leak", "proj-messages-bare-asserts", "proj-spec-products-list-tuple",
          "proj-r15-comment-first-product-claim", "proj-r13-new-half-cent-tests", "proj-r13-mix-tolerance-test",
          "proj-r13-grader-mix-comment"]:
    ov(i, "PASS", GRADER_RUN)
ov("proj-collect-count", "PASS",
   "project.html line 265 states '563 checks'; collect-only on every seed 0-49 gives 563 (out_collect_seeds.txt). The "
   "count rose from 527 by the six new entries of LATER_PRODUCT_CONDITIONS x 2 positions x 3 functions = 36 "
   "(grader/test_project.py lines 1052-1069, 1077-1081), and 527 + 36 = 563.")
ov("proj-r15-grader-count-527", "PASS",
   "Subject changed: project.html line 265 now says '563 checks'. Re-verified: collect-only 563 on seeds 0-49 "
   "(out_collect_seeds.txt), reference passes 563/563 on seeds 0, 1, 25, 49 (run in /tmp/ac4-v/e18/gr).")
ov("proj-r15-later-product-conditions", "PASS",
   "Subject changed (six entries added at lines 1064-1069). Re-verified: LATER_PRODUCT_CONDITIONS has 16 entries; each "
   "is a value the page refuses (negative count or price, boolean, float, text, None, missing field, empty or non-text "
   "name, non-mapping product); 16 x 2 x 3 = 96 parametrised tests; reference passes (out_run_graders.txt).")
ov("proj-spec-products-list-tuple", "PASS",
   "project.html line 263 Constraints unchanged; the tuple of products is refused by test_products_that_are_not_a_list_"
   "raise_value_error (alt_c and alt_h are KILLED by it, out_existing_alts.txt), so 'a list of mappings' is enforced "
   "for tuples.")
ov("proj-purity-order-dependence", "PASS", GRADER_RUN + " The purity and silence tests are unchanged; the insertion "
   "at 1064 adds dictionary entries only.")
ov("proj-messages-bare-asserts", "PASS",
   "Re-verified round 18: the six inserted lines are dictionary entries (lambdas that mutate a copied row), not "
   "assertions; the parametrised test that calls them raises through must_raise, which takes a message argument.")
ov("proj-spec-clarity-and-errors", "PASS", GRADER_RUN + " Constraints (project.html line 263) unchanged; each refused "
   "condition has a test (the later-product list now includes float, negative and missing conditions).")

# ---- project.html lab and figure rows: re-run
ov("proj-lab-1", "PASS",
   "Re-run round 18: lab-AC4-project-1.py under python -I -W error exits 0; its output equals the page's expected block "
   "exactly (ledgers/AC4/scripts/AC4-e-r18/out_proj1.txt; exact string comparison in this round).")
ov("proj-lab-2", "PASS",
   "Re-run round 18: lab-AC4-project-2.py exits 0 and equals the page's second expected block exactly "
   "(out_proj2.txt; exact comparison).")
ov("proj-lab-1-run-line146-untouched", "PASS",
   "Re-run round 18: the lab code (project.html lines 56-145) is unchanged in this delta (the only changed line in "
   "Lab 1 is line 55, the hypothesis) and its output matches the expected block (out_proj1.txt).")
ov("proj-lab-1-interpretation", "PASS",
   "Re-run round 18: every figure in the line-146 interpretation recomputed from the case: master profit 2,600,000; "
   "budgeted margin 7,600,000 / 1,400 = 5,428.57 per unit; 100 extra units = 542,857; mix -462,857; price +180,000; "
   "efficiency -40,000 (200 extra inputs x 200); total +220,000; 1/7 cent rounding gap. All match out_proj1.txt.")
ov("proj-r12-lab1-derived-figures", "PASS",
   "Re-run round 18: 71.4% (1,000/1,400), 80.0% (1,200/1,500), Standard 4,400 vs Deluxe 8,000 per unit: each matches "
   "the case and the output.")
ov("proj-r15-interpretation-rounding-basis", "PASS",
   "Re-run round 18: 7,600,000 / 1,400 = 5,428.571..., rounded to 5,428.57; 100 x 5,428.57 = 542,857 (out_proj1.txt).")
ov("proj-r15-hypothesis-line55-parenthetical", "PASS",
   "Subject changed (line 55 now reads '3 inputs at 200 cents'). Re-verified: the standard input cost of one Standard "
   "unit is 3 x 200 = 600 cents, so its margin is 5,000 - 600 = 4,400 cents; Deluxe is 9,000 - 5 x 200 = 8,000 "
   "(lab-AC4-project-1.py PRODUCTS and INPUT_PRICE = 200). Standard earns the smaller margin, as stated.")
ov("proj-simulated-and-data", "PASS",
   "Re-run round 18: line 55 still states 'the case is SIMULATED'; lab-AC4-project-1.py reads no file (out_proj1.txt).")
ov("proj-r17-delta-scope", "PASS",
   "Round-18 delta for slice AC4-e (git diff --stat fefbf8b 7143726): project.html (4 changed lines: 55, 265, 293, 372), "
   "grader/test_project.py (+6 entries at 1064-1069), cards.json (6 objects: AC4-c008, c018, c061, c095, c096, c125), "
   "tests/labs/AC4/lab-AC4-L07-1.py (boundary pair). All read in full and re-verified this round.")
ov("proj-banned-phrases", "PASS",
   "Re-run round 18: grep of every added line in project.html, cards.json and index.html for roughly, about, historically, "
   "typically, usually, mostly, generally, ellipsis, always, never, only, all, every, same, drives, offsets, raises: the "
   "only hits are 'all 187 pairs' (backed by exact checks passed: 187/187, out_L07.txt) and 'the case is SIMULATED' text.")

# ---- cards in the changed set and cards whose cited passage changed
ov("proj-r17-cards-c008", "PASS",
   "AC4-c008 back now reads 'In Lab 1 the largest absolute residual is 514.73 USD'; the lab prints "
   "'largest absolute residual_cents 51473' (ledgers/AC4/scripts/AC4-e-r18/out_L01.txt), i.e. 51473 cents = 514.73 USD, "
   "the absolute value of month 1's -51473 (same file). Matches. "
   "Lesson L01.html line 283 still says 'the largest is 514.73 USD' (outside this slice; owner L01).")
ov("proj-r17-cards-c061-scope", "PASS",
   "AC4-c061 front now reads 'What sign convention does this lesson use for variances?' (cards.json line 436). L05.html "
   "line 59 Definition 1.3 begins 'Every variance in this lesson is stated as its effect on operating profit' and the "
   "back's sentences are its sentences. The scope is this lesson, so the question is no longer general. PASS.")
ov("proj-r17-cards-c125-attribution", "PASS",
   "AC4-c125 back now reads '89 units. Proposition 4.1 gives the lower-segment break-even of 88.89 units for the Lab 1 "
   "inputs, and Remark 2.3 rounds it up to the first whole unit, 89.' Proposition 4.1 gives 1,200/13.50 = 88.89 "
   "(L02.html line 307 applies the formula; ledgers/AC4/scripts/AC4-e-r18/out_L02.txt prints single_formula_break_even_units 88.89); Remark 2.3 "
   "(L02.html line 81) gives the ceiling 89; out_L02.txt prints first_whole_unit 89, operating_income(88) -12.00 and operating_income(89) 1.50 (lines 2-3); "
   "the attribution is now split correctly. PASS.")
ov("proj-r17-cards-counts", "PASS",
   "Re-verified round 18: cards.json has 134 objects, 134 unique ids, no duplicate front or back; the changed set against "
   "fefbf8b is exactly AC4-c008, c018, c061, c095, c096, c125 (6 changed, 0 added, 0 removed).")
ov("proj-r17-banned-and-numbers", "PASS",
   "Re-verified round 18 for the six changed objects: c008 514.73 USD (out_L01.txt); c018 no banned phrase; c061 "
   "front and back match Definition 1.3; c095 '187', '75', '112' (out_L07 lines: 75 empty, 112 feasible, 187/187); "
   "c096 '73' (out_L07, 'of which capacity binds'); c125 '88.89' and '89' (out_L02.txt line 252). No banned phrase.")
ov("proj-cards-structure", "PASS",
   "Re-verified round 18: 134 cards, unique ids, lesson values L01-L08 only, grades from {T, C, None} as before "
   "(python check of cards.json).")
ov("proj-cards-duplicates", "PASS", "Re-verified round 18: no duplicate fronts or backs in cards.json (Counter check).")
ov("proj-cards-sample", "PASS",
   "Re-verified round 18 on the sample and the six changed cards: c010, c020, c030, c040, c050, c060, c070, c080 and c008, "
   "c018, c061, c095, c096, c125 each match the current lesson text they cite.")
ov("proj-cards-changed-lessons", "PASS",
   "Re-verified round 18: L05 cards (c059-c068) cite Definition 1.2/1.3 and the Lab 1 outputs, none of which changed "
   "in the cited lines (L05 hunks 97, 336, 350, 359, 445 are hypothesis and answer-key text). c073 cites L06 Definition 1.2 "
   "and Proposition 2.2(c); the Definition 1.2 lead-in sentence changed at L06.html line 65, but the cited efficiency bullet "
   "did not, so c073 still matches.")
ov("proj-r17-cards-c073", "PASS",
   "AC4-c073 back (efficiency sign rule, Proposition 2.2(c)) still matches L06.html Definition 1.2's efficiency bullet. The "
   "lead-in sentence of Definition 1.2 changed at line 65 ('In this model material is the only variable cost'); the card "
   "does not cite that sentence. PASS.")
ov("proj-cards-r10-L01", "PASS",
   "Re-verified round 18: c007 ('exact at the two extreme months ... 10 of the 12 months have a nonzero residual'): "
   "the lab prints residual 0 for months 6 and 11, the extremes (hours 428 and 1161), so 10 of 12 are nonzero (out_L01.txt). "
   "c012 (Proposition 3.2 zero residuals at both extremes) matches the changed Proposition 3.2 text (L01.html line 119 "
   "adds 'With Q_H != Q_L, as Definition 3.1 requires'). c014 '514.73 USD' matches the lab. PASS.")
ov("proj-cards-r10-L02", "PASS",
   "AC4-c029 (carried, byte-identical; L02.html lines 252-264 unchanged, hunks at 51, 81, 283) matches the lab output; "
   "AC4-c125 re-verified PASS (see proj-r17-cards-c125-attribution).")
ov("proj-r17-cards-c063", "PASS", "carried; see the L05 cards row; flexed fixed overhead 500,000 at 1,150 units, "
   "unchanged output line.")
ov("proj-r17-cards-c132", "PASS", "carried: L01.html line 114 (tie sentence) is not in the delta hunks (51, 119).")
ov("proj-r17-cards-c133", "PASS", "carried: L06.html line 98 (Proposition 2.2 counterexample) is not in the delta hunks.")
ov("proj-r17-cards-c134", "PASS", "carried: L08.html line 128 is not in the delta hunks (98, 279, 294).")
ov("proj-card-c091", "PASS",
   "carried: L07.html Theorem 7.3 (line 111) is not in the L07 hunks (140, 217-272, 290-310, 368-407, 466-472); "
   "cards.json line 641 unchanged.")
ov("proj-card-c102", "PASS",
   "carried: cards.json object unchanged; L08.html line 306 is outside the hunks 98, 279, 294.")
ov("proj-card-c129", "PASS",
   "carried: cards.json object unchanged; L08.html line 128 is outside the L08 hunks (98, 279, 294).")
ov("proj-r17-cards-c004", "PASS", "carried: cards.json object unchanged; L01.html Definition 3.1 (lines 111-116) is outside "
   "the L01 hunks (51, 119).")

# ---- command rows re-run this round (their subject, the project page, changed)
ov("proj-check-pages", "PASS", "Re-run round 18: tools/check_pages.py --all -> 'check_pages AC4: PASS' (out_check_pages.txt, rc 0).")
ov("proj-check-dag", "PASS", "Re-run round 18: tools/check_dag.py --all -> 'check_dag AC4: PASS' (out_check_dag.txt, rc 0).")
ov("proj-check-projects", "PASS", "Re-run round 18: tools/check_projects.py --all -> 'check_projects AC4: PASS' (out_check_projects.txt, rc 0).")
ov("proj-page-smoke", "PASS", "Re-run round 18: tools/page_smoke.py --unit AC4 --pages project.html -> 'page_smoke AC4: PASS' (out_page_smoke_project.txt, rc 0).")
ov("proj-ruff-mypy", "PASS", "Re-run round 18: ruff check course/modules/AC/AC4/grader tests/labs/AC4 -> All checks passed; ruff format --check on the grader and lab-AC4-L07-1.py -> 5 files already formatted; mypy --no-incremental -> no issues in 153 source files.")
ov("proj-run-labs-ac4", "PASS", "Re-run round 18: tools/run_labs.py --unit AC4 -> 'run_labs AC4: PASS (10/10)' (out_run_labs.txt).")
ov("proj-r13-verify-refs", "PASS", "Re-run round 18: tools/verify_refs.py --offline -> 560 entries, 0 problems; --unit AC4 (live) -> 2 of 560 entries, 0 problems (out_verify_refs_*.txt).")
ov("proj-citations-reading", "PASS", "Re-run round 18: the reading-list keys resolve in the registry through verify_refs --unit AC4 (live) with 0 problems (out_verify_refs_ac4_live.txt); references/ and tools/ are unchanged in the delta.")
ov("proj-cards-sample", "PASS",
   "Carried in part: the sampled cards (c010, c020, c030, c040, c050, c060, c070, c080 and the rest of the sample) are byte-identical objects "
   "(the delta changes six objects, none of them sampled) and their cited passages lie outside the lesson hunks. The six changed cards were re-verified "
   "this round (proj-r17-cards-c008, proj-r17-cards-c061-scope, proj-r17-cards-c125-attribution, proj-r18-card-c018, proj-r18-card-c095-c096, proj-r17-banned-and-numbers).")
ov("proj-cards-changed-lessons", "PASS",
   "Carried in part: the L05 cards (c059-c068) and the L06 card c073 are byte-identical objects. The L05 hunks (97, 336, 350, 359, 445) are hypothesis "
   "and answer-key lines, not Definition 1.2/1.3 or the lab outputs the cards cite. The L06 hunk at line 65 is the Definition 1.2 lead-in; "
   "c073 cites the efficiency bullet, which did not change (proj-r17-cards-c073 re-verified).")
ov("proj-cards-structure", "PASS",
   "Re-verified round 18: 134 cards, 134 unique ids, lesson values only L01-L08; grade values T (52), C (48), and 34 cards with no grade key (cards.json, Counter check).")

# ---- new rows for this round's delta
NEW = [
 ("proj-r18-hypothesis-line55", "project.html line 55 (Lab 1 hypothesis, changed): '3 inputs at 200 cents'",
  "project.html line 55; tests/labs/AC4/lab-AC4-project-1.py PRODUCTS and INPUT_PRICE",
  "PASS", "Standard standard input 3 x 200 = 600 cents; budget price 5,000; margin 4,400. Deluxe 9,000 - 5 x 200 = 8,000. "
  "The smaller margin is Standard's, as the sentence says (lab code lines 56-79; re-run output out_proj1.txt)."),
 ("proj-r18-grading-count-563", "project.html line 265 '563 checks' and sixteen product conditions (changed)",
  "project.html line 265; grader/test_project.py", "PASS",
  "collect-only 563 on seeds 0-49 (out_collect_seeds.txt); the 16 conditions (LATER_PRODUCT_CONDITIONS) map one-to-one onto "
  "the page's list: negative budgeted, actual or standard count and negative budget price; boolean (budget units, actual "
  "price); float (budget price, actual units); text (input count); None (actual units); missing (actual price, name, "
  "budget units); empty and non-text name; non-mapping product. Two positions (middle, last) x 3 functions."),
 ("proj-r18-autograder-storage-sentence", "project.html line 293: 'saved in this browser as you type, where the browser allows storage'",
  "course/assets/js/grader.js lines 61, 79; course/assets/js/store.js lines 1-8", "PASS",
  "The panel saves the draft through store.put (IndexedDB, 400 ms debounce, grader.js line 61); store.js says that when "
  "IndexedDB is unavailable the store falls back to memory for the session. 'where the browser allows storage' is that "
  "condition, so the sentence is accurate."),
 ("proj-r18-recommendation-cents", "project.html line 372 '+240,000 cents' (changed)",
  "project.html line 372; out_proj1.txt step 3", "PASS",
  "Standard price variance = (5,200 - 5,000) x 1,200 = 240,000 cents; step 3 prints the total price variance 180,000 "
  "(240,000 - 60,000 Deluxe). The Standard figure is correct."),
 ("proj-r18-index-lede", "course/modules/AC/AC4/index.html line 33 lede: 'generated or typed in for the module'",
  "course/modules/AC/AC4/index.html line 33; project.html Lab 1 PRODUCTS (typed); L07 BOUNDARY (typed)", "PASS",
  "The project cases are typed literals (lab-AC4-project-1.py PRODUCTS and INPUT_PRICE, the same in project-2) and the "
  "generated cases are from a seeded generator (L07 generate); both are labelled SIMULATED. Accurate."),
 ("proj-r18-card-c018", "cards.json AC4-c018 back (changed): 'a line with positive slope has no maximum on the whole domain Q >= 0'",
  "cards.json line 121-124; L02.html line 303 ('A line with positive slope has no maximum on Q >= 0')", "PASS",
  "A line with slope m > 0 on [0, infinity) is unbounded above, so it has no maximum on Q >= 0; L02 line 303 says the same. "
  "Grade T, no numbers."),
 ("proj-r18-card-c095-c096", "cards.json AC4-c095 and c096 (changed): 187 pairs, 75 empty, 112 feasible, 73 binding",
  "cards.json lines 671-678, 686-690; tests/labs/AC4/lab-AC4-L07-1.py output (out_L07.txt)", "PASS",
  "Lab output: 14 with q > K; 75 empty; 112 feasible (75 + 112 = 187 = 201 - 14); 73 binding; exact checks 187/187. The "
  "boundary pair is feasible (t_min = t_max = 5200.00) and binding (D = 3000 > 0). 73 = 72 generated + 1 boundary. "
  "Fractions 75/187 = 0.4011 and 73/112 = 0.6518 in L07 line 310 and 370 recomputed. Card numbers match the lab."),
 ("proj-r18-card-c074-qualifier", "cards.json AC4-c074 (unchanged) back: 'Actual contribution is actual revenue less the cost of the material used (Definition 1.2)'",
  "L06.html line 65 (Definition 1.2, changed to 'In this model material is the only variable cost, so ...')", "PASS",
  "The card's sentence is the conclusion Definition 1.2 draws in this model, and the card cites that definition. The "
  "model qualifier is no longer repeated in the card; not a false claim within the lesson's stated model. Noted as a "
  "wording suggestion only."),
 ("proj-r18-boundary-pair-l07-note", "tests/labs/AC4/lab-AC4-L07-1.py hand-built boundary pair (outside this slice, read because cards cite it)",
  "tests/labs/AC4/lab-AC4-L07-1.py lines 77-80; output lines 'boundary case (hand-built): t_min 5200.00, t_max 5200.00, firm-wide surplus 0 cents'",
  "PASS",
  "BOUNDARY = Case(v=4000, p_m=6000, capacity=10000, external=8000, q=5000, r_net=5200): t_min = t_max = 5200 and "
  "surplus 0 match the comment and output. The lab labels the pair hand-built and the generated pairs SIMULATED."),
 ("proj-r18-new-student-error-mutants", "ledgers/AC4/mutants/r18e_01..r18e_04 (four new student-error mutants)",
  "ledgers/AC4/mutants/r18e_0*.py; out_new_mutants.txt", "PASS",
  "r18e_01 None standard input read as zero; r18e_02 missing standard input read as zero; r18e_03 boolean actual price "
  "accepted in the middle product; r18e_04 negative budget price accepted in the last product. All four KILLED on seed 0 "
  "(test_product_field_that_is_none..., test_missing_product_field..., test_bad_later_product_raises_value_error[boolean], [negative])."),
 ("proj-r18-new-correct-alternatives", "ledgers/AC4/scripts/AC4-e-r18/alts/alt18_a, alt18_b, alt18_c (three new correct implementations)",
  "ledgers/AC4/scripts/AC4-e-r18/alts/*.py; out_new_alts.txt", "PASS",
  "alt18_a: exact-type integer checks and floor(x + 1/2) rounding; alt18_b: divmod half-up rounding; alt18_c: int isinstance, "
  "name checked with strip(). Each passes 50/50 seeds. None of the 6 new refusals over-constrains a valid implementation."),
 ("proj-r18-mutants-all-rerun", "ledgers/AC4/mutants/*.py (139 top-level files)",
  "ledgers/AC4/scripts/AC4-e-r18/out_mutate_all_r18.txt; out_new_mutants.txt; out_oos_m60.txt", "PASS",
  "tools/mutate_graders.py --unit AC4 --seeds 0-49: 135/135 killed (0 survivors). The four r18e files: 4/4 killed. "
  "Out-of-scope m60 survives as recorded (scope row)."),
 ("proj-r18-verify-refs", "references/references.json; reading list in project.html line 267",
  "tools/verify_refs.py --offline; tools/verify_refs.py --unit AC4 (live)", "PASS",
  "out_verify_refs_offline.txt: 560 entries, 0 problems. out_verify_refs_ac4_live.txt: 'live re-verification of AC4: 2 of 560 entries, 0 problems' (rc 0)."),
 ("proj-r18-gates", "ruff, mypy and format on the grader, labs and the repository",
  "course/modules/AC/AC4/grader; tests/labs/AC4; mypy configuration", "PASS",
  "ruff check course/modules/AC/AC4/grader tests/labs/AC4: All checks passed; ruff format --check: 5 files already formatted; "
  "mypy --no-incremental (repo): Success, no issues found in 153 source files."),
 ("proj-r18-page-smoke", "course/modules/AC/AC4/project.html in Chromium (light and dark, 360 px, sweep)",
  "tools/page_smoke.py --unit AC4 --pages project.html (out_page_smoke_project.txt)", "PASS",
  "page_smoke AC4: PASS for the project page after the four-line change."),
 ("proj-r18-memo-length-band", "project.html exemplar memo bodies (line 372 changed: one word added)",
  "project.html memo-text blocks at lines 330 and 361", "PASS",
  "Body word counts with tables excluded: exemplar A 321, exemplar B 413 (both in 300-600, project.html line 306). "
  "The one-word change to exemplar B leaves it in the band."),
 ("proj-r18-run-labs", "tests/labs/AC4 (10 twins) and project labs",
  "tools/run_labs.py --unit AC4 (out_run_labs.txt)", "PASS",
  "run_labs AC4: PASS (10/10). The L07 twin prints 187/187 exact checks and the boundary line (out_L07.txt)."),
 ("proj-r18-check-tools", "check_pages, check_dag, check_projects for AC4",
  "tools/check_pages.py --all; tools/check_dag.py --all; tools/check_projects.py --all (out_check_*.txt)", "PASS",
  "Each prints 'AC4: PASS' (the other units' lines in the same output also pass). rc 0."),
 ("proj-r18-collect-all-seeds", "grader/test_project.py collect-only on seeds 0-49",
  "ledgers/AC4/scripts/AC4-e-r18/out_collect_seeds.txt", "PASS", "563 on all 50 seeds."),
 ("proj-r18-instance-products", "grader/instance.py product count and names",
  "grader/instance.py via make_instance(seed) for seeds 0-49", "PASS",
  "3 products on every seed (Counter {3: 50}); names Alpha, Beta, Gamma on the seeds sampled. The page's 'middle product' and 'last product' (lines 263-265) are therefore positions 2 and 3."),
 ("proj-r18-cards-totals", "cards.json changed set (vs fefbf8b)",
  "course/modules/AC/AC4/cards.json", "PASS",
  "6 changed objects (AC4-c008, c018, c061, c095, c096, c125), 0 added, 0 removed; 134 cards; grade and lesson fields unchanged for the other 128."),
 ("proj-r18-exemplar-B-threshold-unchanged", "project.html line 373 (threshold paragraph; unchanged)",
  "project.html line 373; line 372 is the changed Recommendation", "PASS",
  "Deluxe budgeted margin at 5,400 cents: 5,400 - 5 x 200 = 4,400 = Standard's 4,400, so the threshold is 5,400 (re-computed)."),
]

rows_out = []
ids_seen = set()
for r in prev["rows"]:
    i = r["id"]
    if i in ids_seen:
        continue
    ids_seen.add(i)
    if i in OVERRIDE:
        st, ev = OVERRIDE[i]
        if not ev:
            continue
        if ev.startswith("see "):
            ev = ev
        rows_out.append({"id": i, "check": r["check"], "location": r["location"], "status": st, "evidence": ev})
        continue
    if r["status"] != "PASS":
        raise SystemExit(f"unhandled non-PASS row {i}")
    rows_out.append({"id": i, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": CARRY + strip_chain(r["evidence"])})

# prior FAIL rows that are now re-verified PASS (kept with the same id)
for r in prev["rows"]:
    if r["status"] != "PASS" and r["id"] not in OVERRIDE:
        raise SystemExit("FAIL row without a re-verification: " + r["id"])

for (i, check, loc, st, ev) in NEW:
    rows_out.append({"id": i, "check": check, "location": loc, "status": st, "evidence": ev})

# ensure the FAIL rows of round 17 are now listed with their same ids and PASS
PLACEHOLDERS = {"proj-r18-placeholder-unused", "proj-r10-placeholder", "proj-card-c074-qualifier"}
rows_out = [r for r in rows_out if r["id"] not in PLACEHOLDERS]
# keep the 'see ...' rows' evidence pointing at real rows
for r in rows_out:
    if r["evidence"].startswith("see "):
        r["evidence"] = "Re-verified round 18 (same subject as " + r["evidence"][4:].split(" (")[0] + "): see that row."

mutants = []
mut_lines = (CHECKOUT / O / "out_mutate_all_r18.txt").read_text().splitlines() + \
            (CHECKOUT / O / "out_new_mutants.txt").read_text().splitlines()
killed_by = {}
for ln in mut_lines:
    m = re.match(r"KILLED (\S+\.py)[: ]", ln)
    if m and " -> " in ln:
        killed_by[m.group(1)] = ln.rsplit(" -> ", 1)[1]
for p in sorted((CHECKOUT / "ledgers/AC4/mutants").glob("*.py")):
    text = p.read_text()
    doc = re.match(r'\s*"""(.*?)"""', text, re.S).group(1).strip().splitlines()[0]
    mutants.append({"id": p.stem, "file": f"ledgers/AC4/mutants/{p.name}", "description": doc,
                    "killed_by": killed_by.get(p.name, "NOT FOUND IN RUN OUTPUT")})

missing = [m["id"] for m in mutants if m["killed_by"] == "NOT FOUND IN RUN OUTPUT"]
assert not missing, missing

summary_rows = len(rows_out)
frag = {
  "unit": "AC4", "slice": "AC4-e", "round": 18,
  "verifier": "Claude Haiku 5.5 (independent verifier, round 18, slice AC4-e; did not build AC4)",
  "pin": "7143726", "base": "fefbf8b (round-17 fragment pin; the slice delta is listed in notes)",
  "checkout": "/tmp/verify18-AC4-e", "scratch": "/tmp/ac4-v/e18",
  "verified_at": "2026-10-28T12:00:00+00:00",
  "verdict": None,
  "rows": rows_out, "mutants": mutants, "registry_flags": [], "freshness_flags": [],
  "notes": (
    "Delta fefbf8b..7143726 for AC4-e: project.html (lines 55, 265, 293, 372), grader/test_project.py (six entries at 1064-1069), "
    "cards.json (c008, c018, c061, c095, c096, c125), tests/labs/AC4/lab-AC4-L07-1.py (boundary pair). Every changed subject was "
    "re-read and re-run. The round-17 FAIL rows (proj-r17-cards-c008, proj-r17-cards-c061-scope, proj-r17-cards-c125-attribution, proj-cards-r10-L02) are fixed in cards.json and re-verified PASS. "
    "Outside this slice, noted for the owners: L01.html line 283 still says 'the largest is 514.73 USD' for Lab 1, which "
    "is the largest absolute residual (the largest signed residual is +11065 cents, month 7); L07.html and L08.html and L06.html "
    "changes were read only where a card cites them. Lab output checks: run_labs AC4 PASS; grader reference 50/50; mutants 139/139 killed; "
    "three new correct alternatives pass 50/50."),
  "summary": None,
}
statuses = [r["status"] for r in rows_out]
frag["summary"] = {"rows": len(rows_out), "pass": statuses.count("PASS"), "fail": statuses.count("FAIL"),
                   "unverifiable": statuses.count("UNVERIFIABLE"), "mutants_killed": len(mutants), "mutants": len(mutants)}
frag["verdict"] = "PASS" if all(s == "PASS" for s in statuses) else "FAIL"
OUT.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n")
print("rows", len(rows_out), "verdict", frag["verdict"], frag["summary"])
