"""Builds ledgers/CF8/CF8-c.json for the CF8-c closing delta, round 1 (pin 2a805c83)."""

import json
import sys

PIN = "2a805c831410ab77c38c227f7e121e8537193ce9"
BASE_PIN = "95f3f8cb21c2cd9fc904430bd30a6b734d01f672"
CARRY = "Carried from round 1 (base F3-CF8-c.round1.json, pin 95f3f8cb; {files} byte-identical since the previous pin 95f3f8cb): "
OUT = "d1_"
G = "ledgers/CF8/scripts/CF8-c-r1/"

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        r["fix"] = fix
    rows.append(r)


PROJ = "project.html, grader/, tests/labs/CF8/, ledgers/CF8/mutants/"

row("proj-ladder", "check_projects --unit CF8", "course/modules/CF/CF8/project.html", "PASS",
    "Re-verified (pin 2a805c83): .venv/bin/python tools/check_projects.py --unit CF8 -> 'check_projects CF8: PASS', exit 0 (" + G + "d1_gates.out). project.html byte-identical to 95f3f8cb (git diff --quiet).")
row("proj-check-pages", "check_pages --unit CF8", "tools/check_pages.py", "PASS",
    "Re-verified (pin 2a805c83): check_pages CF8: PASS, exit 0 (" + G + "d1_gates.out). check_pages is the only tool that reads cards.json, so it is the gate that covers the changed cards.")
row("proj-dag", "check_dag --unit CF8", "project.html concept links", "PASS",
    "Re-verified (pin 2a805c83): check_dag CF8: PASS, exit 0 (" + G + "d1_gates.out).")
row("proj-labs-run", "run_labs --unit CF8; twins under python -I -W error", "project.html lab-CF8-project-1..3; tests/labs/CF8/lab-CF8-project-{1,2,3}.py", "PASS",
    "Re-verified (pin 2a805c83): run_labs --unit CF8 -> 'run_labs CF8: PASS (8/8)', exit 0 (" + G + "d1_run_labs_CF8.out). Each project twin re-run alone with .venv/bin/python -I -W error: exit 0, 0 bytes stderr (" + G + "d1_twin_p1.out, d1_twin_p2.out, d1_twin_p3.out).")
row("proj-lab1-claims", "Lab 1 hypothesis, code and interpretation", "project.html lines 55-168; tests/labs/CF8/lab-CF8-project-1.py", "PASS",
    CARRY.format(files="project.html, grader/, tests/labs/CF8/lab-CF8-project-{1,2,3}.py") + "those files are unchanged, so the lab 1 block and twin are the base text. Supporting re-run: " + G + "d1_twin_p1.out prints 'step 7, peak drawn balance: 3142.86 dollars' and 'step 8, covenant pinch: week 13, headroom -1142.86 dollars', matching the page.")
row("proj-lab2-claims", "Lab 2 hypothesis and interpretation (completion rung)", "project.html lines 172-254; tests/labs/CF8/lab-CF8-project-2.py", "PASS",
    CARRY.format(files="project.html, grader/, tests/labs/CF8/lab-CF8-project-{1,2,3}.py") + "unchanged. Supporting re-run: " + G + "d1_twin_p2.out 'lowest headroom over the horizon: -1142.86 dollars'.")
row("proj-lab3-claims", "Lab 3 hypothesis, docstring and interpretation", "project.html lines 330-454; tests/labs/CF8/lab-CF8-project-3.py", "PASS",
    CARRY.format(files="project.html, grader/, tests/labs/CF8/lab-CF8-project-{1,2,3}.py") + "unchanged. Supporting re-run: " + G + "d1_twin_p3.out 'covenant pinch: week 13, headroom -1642.86 dollars' and 5-day DSO and DPO impacts 5000.00 dollars.")
row("proj-cumulative-docstring", "New docstring of cumulative() reads correctly against its code", "project.html lines 402-407; tests/labs/CF8/lab-CF8-project-3.py lines 75-80", "PASS",
    CARRY.format(files="project.html and the project-3 twin") + "docstring unchanged (git diff empty for both).")
row("proj-spec-data", "Inputs: autograder cases are generated; labs 1-3 cases are written out", "project.html line 264; grader/instance.py; tests/labs/CF8/lab-CF8-project-{1,2,3}.py", "PASS",
    CARRY.format(files="project.html, grader/instance.py and the project twins") + "unchanged.")
row("proj-conventions-rounding", "Conventions 'Rounding' bullet", "project.html line 286", "PASS",
    CARRY.format(files="project.html") + "line 286 unchanged. Gate re-run: run_graders CF8 PASS (reference 50/50 seeds) (" + G + "d1_run_graders_CF8.out).")
row("proj-conventions-windows", "Conventions 'Action cash impact' bullet (DSO and DPO windows)", "project.html line 284", "PASS",
    CARRY.format(files="project.html and grader/") + "line 284 and grader/reference.py action_cash_impact unchanged.")
row("proj-exemplar-A-numbers", "Exemplar A figures", "project.html lines 481-499", "PASS",
    CARRY.format(files="project.html") + "exemplar A text unchanged.")
row("proj-exemplar-B-numbers", "Exemplar B figures", "project.html lines 501-518", "PASS",
    CARRY.format(files="project.html") + "exemplar B text unchanged.")
row("proj-exemplar-calibration", "Exemplar data-scores match official scoring", "project.html line 481 (exemplar-a data-scores=2,2,2,2,2) and line 501 (exemplar-b data-scores=4,4,4,4,4)", "PASS",
    CARRY.format(files="project.html") + "no blind scorer file for CF8 exists in ~/.fanout/blind/ (the ten files there are BK4-c, CS2-d, E1-d, E3-d-fresh, E3-d, E4-d, FC2-d, LX1-c, M5-d, PC3-c), so the base calibration row is carried (ruling 23).")
row("proj-rubric-observable", "Rubric table criteria are observable", "project.html rubric lines 463-475", "PASS",
    CARRY.format(files="project.html") + "rubric table unchanged.")
row("proj-memo-sections", "Memo five-section spec and rubric alignment", "project.html line 460 and spec line 266", "PASS",
    CARRY.format(files="project.html") + "memo section lines unchanged.")
row("proj-hours", "Hours table and page sentence", "project.html hours table lines 297-304; course/modules/CF/CF8/index.html line 29", "PASS",
    "Re-verified (pin 2a805c83): course/modules/CF/CF8/index.html line 29 reads data-hours-lessons=\"40\" data-hours-project=\"10\"; 40 + 10 = 50 (grep); index.html and project.html byte-identical to 95f3f8cb (git diff --quiet), so the project hours table lines 297-304 are unchanged.")
row("proj-reading-bates", "Reading entry for Bates et al.", "project.html line 539; references/references.json key bates2009us", "PASS",
    CARRY.format(files="project.html and references/") + "line 539 and the references/ tree unchanged (git diff --quiet). The paper body was not read; no claim from it is used on the page.")
row("proj-grader-reference", "reference.py passes the suite on every seed", "course/modules/CF/CF8/grader/reference.py", "PASS",
    "Re-verified (pin 2a805c83): run_graders --unit CF8 --seeds 0-49 -> 'run_graders CF8: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 (" + G + "d1_run_graders_CF8.out).")
row("proj-grader-starter", "starter.py docstring and stub", "course/modules/CF/CF8/grader/starter.py", "PASS",
    CARRY.format(files="grader/") + "starter.py unchanged. Gate re-run: page_smoke --unit CF8 --pages project PASS (" + G + "d1_page_smoke_project.out).")
row("proj-grader-alternatives", "Five alternative correct engines pass the suite", "grader/test_project.py vs alternatives alt1..alt5", "PASS",
    CARRY.format(files="grader/") + "grader/test_project.py unchanged; base evidence alternatives_r6.txt (100 passed on seeds 0, 13, 49 each, five engines) is carried and not re-run this round.")
row("proj-grader-mutants", "Mutation testing: existing student-error mutants are all killed", "ledgers/CF8/mutants/ (59 files)", "PASS",
    "Re-verified (pin 2a805c83): tools/mutate_graders.py --unit CF8 -> 'mutate_graders CF8: PASS (59/59 killed)', exit 0, 59 KILLED lines and 0 surviving (" + G + "d1_mutate_graders_CF8.out). No mutant was written this round (ruling 37).")
row("proj-grader-equivalent-r3-04", "Round-3 equivalent mutant not in the mutant set", "grader/test_project.py", "PASS",
    CARRY.format(files="grader/") + "grader/test_project.py and starter.py unchanged.")
row("proj-grader-instances", "instance.py deterministic and varies by seed", "course/modules/CF/CF8/grader/instance.py", "PASS",
    CARRY.format(files="grader/") + "instance.py unchanged; run_graders CF8 PASS re-run on 2a805c83 (" + G + "d1_run_graders_CF8.out).")
row("proj-grader-messages", "must_raise and pytest.fail messages", "grader/test_project.py", "PASS",
    CARRY.format(files="grader/") + "grader/test_project.py unchanged.")
row("proj-grader-exception-table", "Exception types only for conditions the page names", "grader/test_project.py lines 545-606; project.html line 268", "PASS",
    CARRY.format(files="grader/ and project.html") + "unchanged.")
row("proj-grader-stdlib", "Grader and reference are standard library only", "grader/test_project.py lines 767-791; reference.py imports", "PASS",
    CARRY.format(files="grader/") + "unchanged.")
row("proj-test-count", "Test count on the page equals the collect-only count", "project.html line 270 (Grading dd)", "PASS",
    CARRY.format(files="project.html and grader/") + "line 270 unchanged (100 checks); base collect-only count of 100 (ref_pytest_r6.out) is carried.")
row("proj-starter-docstring", "starter.py docstring", "course/modules/CF/CF8/grader/starter.py", "PASS",
    CARRY.format(files="grader/") + "starter.py unchanged. Gate re-run: page_smoke project PASS (" + G + "d1_page_smoke_project.out).")
row("proj-spec-interest-scope", "Interest and fees scope statement", "project.html lines 268 and 285", "PASS",
    CARRY.format(files="project.html") + "lines 268 and 285 unchanged.")
row("proj-pytest-version", "Local-run pytest text", "project.html lines 319-320", "PASS",
    CARRY.format(files="project.html") + "lines 319-320 unchanged.")
row("proj-notation", "Symbols used on the page are CF8-local or registry-consistent", "project.html; notation/ registry", "PASS",
    CARRY.format(files="project.html and notation/") + "both unchanged (git diff --quiet 95f3f8cb HEAD).")
row("cards-count-numbers", "Numbers in cards appear in their lessons", "course/modules/CF/CF8/cards.json, 80 cards", "PASS",
    "Re-verified (pin 2a805c83): " + G + "d1_cards_checks.py (python3 -I, reads the lesson HTML) over all 80 cards: every numeric token in a card's front or back occurs in that card's own lesson after normalising the LaTeX {,} grouping; output " + G + "d1_cards_checks.out, 'checked 80 cards', no NUM NOT IN OWN LESSON line. Changed cards' numbers (881,834; 678,082.19; 4.52; -139,905; 539,905; -608,065; -1,488,640; 88,640; 1,288,640) are in their lessons (L04.html lines 304, 358, 366, 431; L02.html line 157).")
row("cards-lab-numbers", "Numbers cited from labs match lab output", "cards c031, c052, c053, c054, c056, c077 (changed); c010, c011, c040, c042, c057, c069-c073, c075-c080 (carried)", "PASS",
    "Re-verified for the changed cards: c031 and c077 ΔI 678,082.19 and m* 4.52%: d1_twin_L02_1.out lines 11-12 (lab-CF8-L02-1.py, python -I -W error exit 0). c052: 'receipts fall by 881834 cents in week 1' (d1_twin_L04_1.out), and 5 x 1,234,567 / 7 = 881,833.57 (d1_flows_L04.out). c053: week 6 headroom -139905 and draw 539905 (d1_twin_L04_1.out week 6 row). c054: week-6 weekly net flow -608,065 is the least single-week flow and the least cumulative flow is -1,488,640 in week 11 (d1_flows_L04.py / d1_flows_L04.out, derived from the printed liquidity via Theorem 2.1; the lab prints pinch week 11). c056: 'largest weekly shortfall 88640', 'required commitment 1288640' (d1_twin_L04_1.out); required_commitment = max(opening drawn, peak of unconstrained draws) (tests/labs/CF8/lab-CF8-L04-1.py lines 107-110). Carried: unchanged cards, byte-identical lesson text since 95f3f8cb.")
row("cards-sample-lesson-agreement", "Cards agree with the current lesson text", "cards.json c001-c080 (13 changed cards)", "PASS",
    "Re-verified (pin 2a805c83): every changed card (c018, c021, c022, c023, c031, c050, c052, c053, c054, c055, c056, c058, c077) was read against the current lesson HTML, which is byte-identical to 95f3f8cb (no lesson file changed in the delta). Locators: L02.html line 102 (Prop 2.1), 121-127 (Assumption 3.0), 133-143 (Prop 3.2), 146-150 (Cor 3.3), 156-158 (Ex 3.4); L04.html lines 71-72 (Thm 2.1), 87-92 (Cor 2.2), 323-328 (Thm 2.4), 331-333 (Ex 2.5), 349-366 (Misconceptions), 431 (E1); L05.html lines 57-58 (Def 1.1). Carried: the 67 unchanged cards (base evidence).")
row("cards-duplicates-exact", "No exact duplicate cards", "course/modules/CF/CF8/cards.json", "PASS",
    "Re-verified (pin 2a805c83): " + G + "d1_cards_checks.out: 80 unique ids, 0 duplicate (front,back) pairs, 0 duplicate fronts. Near-neighbours of the changed cards asking different quantities: c019/c075, c031/c077, c049/c053 (see cards-near-dup-049-053).")
row("cards-near-dup-049-053", "c049 and c053 are distinct", "cards c049 (cards.json line 352), c053 (line 384)", "PASS",
    "Re-verified (pin 2a805c83): c049 asks whether a draw or repayment changes liquidity (answer: no, Theorem 2.1); c053 asks whether drawing gives more covenant headroom (answer: no, Definition 1.2 and Theorem 2.1, with the week-6 lab figure). The fronts now share the L03-rule clause, but the questions and the quantities differ. c049 is byte-identical to 95f3f8cb (" + G + "d1_cmp_cards.out).")
row("cards-near-dup-034-044", "c034 and c044 are distinct", "cards c034, c044", "PASS",
    CARRY.format(files="cards c034 and c044") + "neither id is in the changed-id list (" + G + "d1_cmp_cards.out: 13 changed ids, none is c034 or c044).")
row("cards-process-words", "No process words in learner text", "cards.json; project.html; project-3 docstring", "PASS",
    "Re-verified (pin 2a805c83): " + G + "d1_cards_checks.py regex scan (round, builder, verifier, revision, this slice, fanout, ruling, blind) over all 80 cards: no hit. project.html and the project-3 twin are byte-identical to 95f3f8cb.")
row("cards-grades-basis", "Grades and basis fields are consistent", "cards.json grade and basis fields", "PASS",
    "Re-verified (pin 2a805c83): grade counts T 26, C 24, no grade 30 (python3 -I Counter over cards.json; unchanged from base). No grade or basis field changed in the delta. Every changed T card cites a labelled result on the page: c018 Proposition 2.1 (L02.html line 102); c021, c023 Proposition 3.2 (line 133); c022 Corollary 3.3 (line 146); c050 Corollary 2.2 (L04.html line 87); c052 Theorem 2.4 (line 323) and Example 2.5 (line 332). Note (not a ruling-26 kind, see notes): c031 and c077 are graded C naming Lab 2 Part B, but Example 3.4 (L02.html lines 156-158) derives ΔI and m* by hand from stated inputs, which ruling 13 grades T.")
row("cards-labels", "Lesson field agrees with each card's cited lesson", "cards.json lesson field", "PASS",
    "Re-verified (pin 2a805c83): lesson counts L01 13, L02 21, L03 15, L04 15, L05 16 (total 80; " + G + "d1_cards_checks.out). No lesson field changed in the delta. Each changed card's content lies in its cited lesson (see cards-sample-lesson-agreement).")
row("cards-hypotheses", "Theorem cards state the hypotheses", "cards c052 (front, cards.json line 376); c016, c021, c022, c023, c027, c043, c053, c055, c056", "PASS",
    "Re-verified from scratch (pin 2a805c83). The base FAIL is closed: c052 front (cards.json line 377) now states Theorem 2.4's assumptions (1) to (5): the L03 rule and 0 <= B0 <= K, 'every receipt is a collection of receivables' (assumption (3), L04.html line 324, used at line 328), weekly sales S (1), DSO slip with the opening receivable unchanged (2), collections given up stay uncollected (4), and no interest, fee or cost (5). The back's dS/7 claim follows from the proof at L04.html line 328. c053 (line 385) and c056 (line 408) now state the L03 rule (Theorem 2.1(1), Theorem 2.3(1)). c021, c022, c023 state Assumption 3.0 with r > 0 (item (5), L02.html line 123) and n >= 1; c027 states r > 0 (Problem R1). c016 states 0 < d < 1 and 0 <= k < N (Proposition 1.3). c055 states the Theorem 2.4 assumptions (line 401). c043 names 'the credit line', which L03 Definition 2.1 defines as the credit line and minimum-cash rule (L03.html line 87), so the rule is named; not a defect. Notes: see notes (c043 wording).")
row("cards-notation-collisions", "Card symbols do not collide with notation registry", "cards.json (changed cards c018, c021-c023, c031, c052, c053, c054, c056, c077)", "PASS",
    "Re-verified (pin 2a805c83): notation/notation.json (unchanged) registers T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. " + G + "d1_cards_checks.py word-boundary scan finds none of these tokens in any card. The changed cards use r, n, d, N_0, N_1, Rev_0, ΔI, ΔRev, m*, A(r,n), B0, K, S, Cum; none is a registry symbol. Rev_0 matches L02 Example 3.4 (L02.html line 157).")
row("cards-section-citations-L04", "Cards cite Section numbers that exist in L04", "cards c050, c052, c053, c054, c055, c056 (basis)", "PASS",
    "Re-verified (pin 2a805c83): L04.html h2 section 1 at line 53, section 3 'Where the canon breaks' at line 342, section 4 'Misconceptions' at line 350. Corollary 2.2 (line 87), Theorem 2.4 (line 323) and Theorem 2.1 lie under Section 1; c053, c054, c056 cite Misconceptions (Section 4); c055 cites Section 3 (line 344-345) and Section 4.")
row("tests-labs-memo", "pytest for labs and memo exemplars", "tests/test_labs.py, tests/test_memo_exemplars.py", "PASS",
    CARRY.format(files="tests/test_labs.py, tests/test_memo_exemplars.py, tests/labs/CF8/") + "unchanged, and no test reads cards.json (grep over tests/ and tools/ finds only tools/check_pages.py). Base run pytest_labs_memo.out carried.")
row("gate-check-pages-unit", "check_pages --unit CF8", "tools/check_pages.py", "PASS",
    "Re-verified (pin 2a805c83): check_pages CF8: PASS, exit 0 (" + G + "d1_gates.out).")
row("gate-verify-refs", "verify_refs --offline", "tools/verify_refs.py", "PASS",
    "Re-verified (pin 2a805c83): verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (" + G + "d1_gates.out). references/ unchanged in the delta.")
row("cards-ruff-mypy", "ruff and mypy", "tests/labs/CF8; course/modules/CF/CF8/grader; repo", "PASS",
    CARRY.format(files="tests/labs/CF8/ and course/modules/CF/CF8/grader/") + "no Python file under those paths changed (git diff --quiet). cards.json is JSON, outside ruff and mypy scope. Base ruff.out and mypy.out (Success: no issues found in 386 source files) carried. The delta's Python changes are in other units (tests/labs/E4, tests/labs/M3, tests/test_lx1_project_lab3.py), not CF8.")
row("gate-build-site-check", "build_site --check (site data current; cards.json changed)", "tools/build_site.py", "PASS",
    "Re-verified (pin 2a805c83): build_site.py --check -> 'site data current: 6 outputs', exit 0 (" + G + "d1_gates.out).")

mutants = [
    {"id": "r6-m1-round-floor", "description": "Money is rounded down (floor) instead of half up, so a half-cent receipt is dropped. (standing)",
     "killed_by": "test_receipts_match_the_day_by_day_oracle (seed 0); re-run 2a805c83 KILLED (" + G + "d1_mutate_graders_CF8.out)"},
    {"id": "r6-m2-pinch-latest-tie", "description": "Covenant pinch takes the latest week on a tie in headroom, not the earliest. (standing)",
     "killed_by": "test_pinch_week_breaks_a_tie_toward_the_earliest_week (seed 0); re-run 2a805c83 KILLED"},
    {"id": "r6-m3-required-equals-peak", "description": "Required commitment is the capped peak, so a commitment that binds is reported as sufficient. (standing)",
     "killed_by": "test_required_commitment_is_the_uncapped_peak_draw (seed 0); re-run 2a805c83 KILLED"},
    {"id": "r6-m4-dpo-window-short", "description": "DPO change postpones one day fewer than the stated days, so the window is off by one. (standing)",
     "killed_by": "test_dpo_lengthening_matches_the_day_oracle (seed 0); re-run 2a805c83 KILLED"},
]

notes = (
    "CF8-c closing delta, round 1 (ruling 30). Base F3-CF8-c.round1.json, pin 95f3f8cb (FAIL: cards-hypotheses, c052 front). "
    "Delta 95f3f8cb..2a805c83 inside the slice paths is course/modules/CF/CF8/cards.json only (13 changed cards, 80 in all, none added or removed): "
    "c018, c021, c022, c023, c031, c050, c052, c053, c054, c055, c056, c058, c077. Every other slice path is byte-identical (git diff --quiet): "
    "project.html, grader/, tests/labs/CF8/, L01-L05.html, course/index.html, references/, notation/, tools/, ledgers/CF8/mutants/. "
    "Verdict: PASS. The base FAIL is closed (c052 now states Theorem 2.4 assumption (3)). "
    "Resolved base observations: (a) c050 and c054 now carry the earlier-week tie clause (Corollary 2.2 states it); "
    "(b) c053 and c056 now carry the L03 rule clause; (c) c021-c023 now state r > 0; (d) c031 and c077 use Rev_0 as L02 Example 3.4 does. "
    "Observations (notes, not ruling-26 FAIL kinds; ruling 30 says observations are notes): "
    "(1) ruling 13 grading: c031 and c077 are graded C naming Lab 2 Part B, but Example 3.4 (L02.html lines 156-158) derives ΔI = 678,082.19 and m* = 4.52 percent by hand from the stated inputs, which ruling 13 grades T with the Example as basis. Under-grading is not a listed FAIL kind, so it is not a FAIL here; the owner may regrade. "
    "(2) c054 ('Is the pinch week the week with the largest outflow? No.') and c056 ('is a commitment that covers the opening drawn balance enough? No.') answer 'No' as 'not in general'; the backs state the general rule and a counterexample, so the reading is consistent, but 'not necessarily' would be exact. "
    "(3) c043 front ('With 0 <= B0 <= K, can minimum cash be breached...') does not restate the L03 rule; it names 'the credit line', which L03 Definition 2.1 defines as the credit line and minimum-cash rule, so the rule is named. Restating it as c049 does would be clearer. "
    "(4) Outside this delta (L02.html, unchanged, not a card): Example 3.4 writes 'm* = 0.10 * 678,082.19 / 1,500,000 = 0.0452' with a rounded value after '='; the exact value is 0.0452055. Owner note only. "
    "Not checked: the five alternative engines were not re-run (grader unchanged; base evidence carried); the Bates paper body; no blind exemplar scorer exists for CF8, so exemplar calibration is carried from base (ruling 23); ruff, mypy and pytest for labs and memo were carried, not re-run, because no Python file under the CF8 paths changed. No new mutants were written (ruling 37)."
)

fragment = {
    "unit": "CF8",
    "slice": "CF8-c",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for CF8-c, closing delta round 1 (did not build CF8)",
    "pin": PIN,
    "base": "F3-CF8-c.round1.json at pin 95f3f8cb (FAIL: cards-hypotheses). Base chain: round-6 fragment C-CF8-c.round6.json at pin 9fd6aed. Delta 95f3f8cb..2a805c83 in slice paths: course/modules/CF/CF8/cards.json only.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyG1-CF8-c",
    "scratch": "/tmp/cf8c-closing-r1 (cards_base.json, cards_head.json, flows_L04.py, twin outputs, gates)",
    "verified_at": sys.argv[1],
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "course/modules/CF/CF8/cards.json changed in the delta (13 cards); every changed card is re-read; other CF8 slice paths are byte-identical since 95f3f8cb.",
        "ledgers/CF8/scripts/CF8-c-r1/ holds the base round's files; this round's files carry the d1_ prefix and do not overwrite them.",
    ],
    "notes": notes,
    "summary": (
        "CF8-c closing delta round 1 (pin 2a805c83): PASS. 49 rows, all PASS: 21 re-verified from scratch on this pin "
        "(gates check_pages, check_dag, check_projects, build_site --check, verify_refs, run_labs 8/8, run_graders 50/50, "
        "page_smoke CF8 and project, mutate_graders 59/59; cards-hypotheses (base FAIL) re-verified and closed; all 13 changed cards "
        "re-read against the lesson HTML) and 28 carried by byte-identical subject. Observations in notes (grade of c031/c077 under ruling 13; "
        "'No' wording of c054/c056; c043 wording); none is a ruling-26 FAIL kind. Mutants: 4 standing, 59/59 killed; no new mutants."
    ),
}

with open(sys.argv[2], "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print("rows", len(rows), "PASS", sum(1 for r in rows if r["status"] == "PASS"))
