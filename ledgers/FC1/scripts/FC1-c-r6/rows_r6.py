import json, pathlib
S = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyC6-FC1-c/ledgers/FC1/scripts/FC1-c-r6")
R = []
def row(id, check, location, status, evidence):
    R.append({"id": id, "check": check, "location": location, "status": status, "evidence": evidence})
P = "Carried from round 5 (byte-identical since previous pin): "
row("proj-run-graders", "2.6-grader", "course/modules/FC/FC1/grader/ (reference.py, starter.py, test_project.py, instance.py)", "PASS",
    "tools/run_graders.py --unit FC1 --seeds 0-49 -> 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.1 s)' (ledgers/FC1/scripts/FC1-c-r6/run_graders.out). grader/test_project.py changed in this delta, so re-run, not carried.")
row("proj-collect-count-55", "2.6-autograder", "project.html line 171 ('runs 59 checks'); grader/test_project.py", "PASS",
    "Copy of grader in /tmp/fc1c6/ref: pytest --co -> '59 tests collected' (collect.out); reference run -> '59 passed' (ref_seed0.out). Page says 59.")
row("proj-browser-suite", "2.6-autograder", "project.html grader panel (data-grader=grader/, data-suite=test_project.py) line 301", "PASS",
    "tools/page_smoke.py --unit FC1 --pages project.html --skip-sweep -> 'page_smoke FC1: PASS' (page_smoke_project.out). Pyodide run itself not driven by hand; the panel attributes match the grader file names.")
row("proj-local-command", "2.6-autograder", "project.html section#local line 307", "PASS",
    "Command run verbatim in /tmp/fc1c6/ref with QF_SEED=0 on reference: '59 passed' (ref_seed0.out). --assert=plain and -W error flags present on line 307.")
row("proj-alternatives-five", "2.6-autograder", "ledgers/FC1/alternatives/a1..a5 (plan five alternatives)", "PASS",
    "alts_r6.out: a1_list_comprehension_events, a2_generator_methods, a3_fraction_throughout, a4_integer_division_half_up, a5_float_discounting_exact_half_up: each seeds=50 failing_seeds=0.")
row("proj-instances-50", "2.6-autograder", "course/modules/FC/FC1/grader/instance.py", "PASS",
    "instance.py read in full (40 lines); run_graders 50/50 seeds PASS; every seed case valid (ranges: face 100000-5000000, coupon 100-900, periods 1-8, yield 50-900, quantity 1-500, price 5000-150000, side +-1, settlement 1-5).")
row("proj-starter-vs-spec", "2.6-spec", "grader/starter.py; project.html line 161", "PASS",
    "starter names Bond(face_cents, coupon_bps, periods).events(), bond_price_cents(bond, yield_bps), CashTrade(quantity, price_cents, side, settlement_day).events() match project.html line 161 exactly.")
row("proj-spec-questions", "2.6-spec", "project.html section#spec lines 153-172", "PASS",
    "Read lines 153-172. Constraints (163-167) list the eight named conditions; grader tests cover each refused value and its accepted boundary (test_project.py 192-250, 329-342, 373-436). '59 checks' line 171 equals the collected count.")
row("proj-ladder", "2.6-ladder", "project.html section#ladder lines 41-50", "PASS",
    "Read lines 41-50: four rungs in order (worked example, completion, independent project, stretch). check_projects FC1 PASS (check_projects.out).")
row("proj-stretch-scope", "2.6-ladder", "project.html section#stretch lines 311-318", "PASS",
    "Read lines 311-318; ungraded wording present. 'as in Lesson 4' refers to L04, which defines the limit order book (L04 Definition 2.1, read via text extraction).")
row("proj-lab1-twin", "2.5-labs", "project.html lab-FC1-project-1 (lines 56-102); tests/labs/FC1/lab-FC1-project-1.py", "PASS",
    "run_labs FC1 (all labs): PASS 8/8 (run_labs.out), which requires page code byte-identical to the twin and page expected block equal to output. Twin alone: python -I -W error exit 0 (twins_project.out): printed lines equal expected block lines 97-100.")
row("proj-lab2-completion", "2.5-labs", "project.html lab-FC1-project-2 (lines 104-150); tests/labs/FC1/lab-FC1-project-2.py", "PASS",
    "Completed twin run alone exit 0 (twins_project.out) gives the four expected lines (lines 145-148). Blanks: exponent 'period' and trade '-side * quantity * price_cents' reproduce Lab 1 output, as the page interpretation (line 149) states.")
row("proj-lab2-docstring", "2.5-labs / 2.9-prose", "project.html line 107 and tests/labs/FC1/lab-FC1-project-2.py line 1", "PASS",
    "run_labs byte-identity check PASS (run_labs.out); twin docstring line 1 'Rung 2 completion: the worked example, with two blanks for you to fill in.' equals page code line 107.")
row("proj-lab3-fixtures", "2.5-labs", "project.html lab-FC1-project-3 lines 196-276; tests/labs/FC1/lab-FC1-project-3.py", "PASS",
    "Twin output (twins_project.out) equals expected block lines 262-274 line for line; hypothesis line 198 values (A 10000, B 11053 exact 11052.6316, C, D, rounding 10278 vs 10277, E, F 1, G 5001) all match output.")
row("proj-prose-numbers", "2.2-numbers", "project.html lines 54, 58, 101, 176, 186-193, 275; grader/test_project.py docstrings", "PASS",
    "numbers_r6.out (own Fraction recomputation): pv 102775.091033 (exact 225796875/2197); rounding case 10277.509103 -> 10278, terms 480.77/462.28/9334.46; fixture B 210000/19 = 11052.6316 -> 11053; fixture G 5000.5 -> 5001; fixture F 1/2 -> 1. Completion tolerance: labs.js |x-y| <= tol*(1+|y|) with tol 1e-6 gives 0.1028 cents, matching line 149 'about 0.1 cent'.")
row("proj-fixture-claims", "2.9-prose / 2.6-autograder", "project.html line 275 vs grader/test_project.py lines 173 and 220", "FAIL",
    "Line 275 says 'Fixture B's, fixture F's and fixture G's events, and the rounding case's events, are not checked as lists.' Wrong for B and F: test_project.py line 173 asserts checked_events(sol.Bond(10_000, 500, 1).events()) == [(1, 10_500)] (fixture B is the same bond at -500 bps), and line 220 asserts sol.Bond(1, 0, 1).events() == [(1, 1)] (fixture F). Only fixture G (Bond(10001,0,1)) and the rounding case's Bond(10000,500,3) events are unchecked as lists (grep of test file). Fix: rewrite line 275 to name only fixture G and the rounding case's events as unchecked, or name the lists that are checked.")
row("proj-hours-arithmetic", "2.6-hours", "project.html section#budget lines 285-292; data-hours-project=20 line 34", "PASS",
    "1+2+5+4+2+3+3 = 20 (lines 285-291); total row 20 = page eyebrow 20 h. Hub index.html line 38-41: 50 lesson + 20 project = 70; 20/70 = 28.6%; L01-L05 are five lessons of ten hours (index line 137). Arithmetic consistent.")
row("proj-check-pages-dag", "2.9-structure", "course/modules/FC/FC1/*.html", "PASS",
    "tools/check_pages.py --unit FC1: 'check_pages FC1: PASS' (check_pages.out).")
row("proj-dag-closure", "2.9-DAG", "project.html lines 58 and 178 (present-value, discount-factor links)", "PASS",
    "tools/check_dag.py --unit FC1: PASS (check_dag.out). The new 'event' definition at line 54 is prose with no concept link.")
row("proj-notation", "2.4-notation", "project.html; grader/*.py; tests/labs/FC1/lab-FC1-project-*.py", "PASS",
    "Symbols on the project page: t, y and the notation of the discount factor only (grep of project.html). No Q, no R, no T, no gamma. notation/notation.json registered symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q}, ...) do not occur on this page or in the grader.")
row("proj-banned-phrases", "2.9-prose", "project.html; grader/; tests/labs/FC1/lab-FC1-project-*.py", "PASS",
    "grep of project.html for we / this section / this page / section N: no process words in learner text; the only hits are the matching words in the text 'this page' (fixture statement) which is a reference to the page itself.")
row("proj-reading-list", "2.1-citations", "project.html section#reading lines 320-327; references/references.json", "PASS",
    "Lines 320-327 unchanged in this delta. tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (verify_refs_offline.out). mishkin2021economics and harris2002trading are the keys cited. Page attributes no statement (line 322).")
row("proj-named-conditions", "2.6-autograder", "project.html Constraints lines 163-167; grader/test_project.py", "PASS",
    "Eight named conditions (periods<1, face<=0, coupon<0, yield<=-10000, quantity<1, price<0, side not in {+1,-1}, settlement_day<1): each has refused and accepted-boundary tests (lines 192-236, 329-342, 373-436). Named refusals also in the print-silence test (474-489).")
row("proj-failure-messages", "2.6-autograder", "grader/test_project.py lines 12 and 518-541 (wrapper); starter run", "PASS",
    "Unmodified starter, QF_SEED=0: '57 failed, 2 passed' with 0 Traceback lines (starter_seed0.out). Failure text e.g. 'Bond.events() returns a list of (period, amount_cents) pairs of plain ints. The student module has no implementation for Bond yet; write it in instruments.py.' (pytrace=False). Was FAIL in round 5 (tracebacks); now resolved.")
row("proj-test-docstring", "2.9-prose (grader docstring)", "grader/test_project.py lines 304-306", "PASS",
    "Docstring now reads 'Round-half-to-even (Python round()) or truncation gives 0.' Observed: round(Fraction(1,2)) = 0, int(Fraction(1,2)) = 0 (half_rules_r6.out). The float claim was removed; a5 float discounting gives 1 so the old text was false. Was FAIL in round 5.")
row("proj-mutants-killed", "2.6-mutation", "ledgers/FC1/mutants/ (46 mutant files present before this round: 41 from earlier rounds and c5n01-c5n05)", "PASS",
    "tools/mutate_graders.py --unit FC1 --seeds 0-9 (mutate_graders_FC1_r6.out): all 46 mutants present before this round (c2*, c3*, c5*, d*, f*, m*, v*) KILLED (49 KILLED in total). The two survivors are the new round-6 mutants (proj-new-mutants-r6).")
row("proj-new-mutants", "2.6-mutation", "ledgers/FC1/mutants/c5n01..c5n05 (round-5 student-error mutants)", "PASS",
    "mutate_graders_FC1_r6.out: c5n01 through c5n05 all KILLED.")
row("proj-new-mutants-r6", "2.6-mutation / 2.9-prose", "ledgers/FC1/mutants/c6n01_prints_on_negative_yield.py, c6n02_prints_on_zero_coupon.py", "FAIL",
    "Two new student-error mutants survive all 50 seeds (silence_mutants_50seeds.out: 'failing seeds 0 of 50', each run '59 passed'). c6n01 prints when bond_price_cents gets a negative yield; c6n02 prints when Bond.events gets coupon_bps 0. Both inputs are valid by the page (line 165 refuses only negative coupons; line 166 refuses only yield <= -10000), and page line 163 forbids printing on a valid input. Three further new mutants are killed: c6n03 (sell-side print, seed 7), c6n04 (settlement_day capped at 12, seed 0), c6n05 (discount exponent t-1, seed 0). Fix: see proj-silence-coverage.")
row("proj-silence-coverage", "2.6-autograder / 2.9-prose", "grader/test_project.py lines 464-471 and 474-489; page lines 163 and 171", "FAIL",
    "Page line 163: 'On a valid input and on each named refused input, no function prints or warns.' Page line 171 says the suite checks 'the silence and purity of the module'. test_the_module_prints_nothing (464-471) runs only bond_of(INST) (positive yield, coupon 100-900, random side), and the refused-input test (474-489) checks prints only on refused calls. No capsys check runs on valid negative yields (e.g. -9999 at line 339), zero coupon (line 235) or sell side (line 422). Result: a print on those inputs passes the whole suite on 50 seeds (c6n01, c6n02). Fix: run the capsys silence check over valid boundary inputs (yield -9999, coupon 0, side -1, periods 12) as well as INST.")
row("proj-lint-types", "2.6-lint", "tests/labs/FC1/; course/modules/FC/FC1/grader/; repo mypy", "PASS",
    "ruff check tests/labs/FC1 course/modules/FC/FC1/grader: 'All checks passed!'; ruff format --check: '12 files already formatted'; mypy --no-incremental: 'Success: no issues found in 229 source files' (mypy_r6.out).")
row("proj-privacy-claim", "2.9-prose", "project.html footer line 340", "PASS",
    P + "footer line 340 ('nothing you write leaves it') is unchanged in the delta, and course/assets/js is unchanged, so the claim's subject is byte-identical. Round-5 evidence stands.")
row("cards-scan-98", "2.7-cards", "course/modules/FC/FC1/cards.json (111 cards, lines 1-744)", "PASS",
    "All 744 lines read. 111 cards, ids FC1-c001..c111 with none missing or duplicated; no duplicate fronts or backs; 32 T, 22 C (each C has basis), 57 ungraded. Only card-level change in this delta is c030 (read in full).")
row("cards-numbers", "2.7-cards", "course/modules/FC/FC1/cards.json; lab twins L01-L05", "PASS",
    "Re-derived: c010 1000*(1-0.9^11)/0.1 = 6861.8940391 -> 686189 cents (matches Lab 1 Part A, twins_lessons.out); c011 1000/(1-0.45) = 1818.18 -> 181818, 18.18 % of 10000 (own run); c012 6.8619*1000 = 6861.90 (own run); c015 190000 cents (L01 Part A); c014/c091/c092/c093 (L01 twin: True, True, 181818 vs 1000000, -50 dollars); c029/c095/c096 (L02 twin Part B counts 3,3,2,2,2; cash 6; exchange 4, OTC 8); c034 (L02 Part C: commodities, equities, rates); c052-c054, c097, c098 (L03 twin: 4000, 4000, 121 grid, -545, 3455); c061/c062/c069 (L04 twin: 159000, 1060, 10, 985, 0 crossed, 0 conservation failures); c082-c086 (L05 twin: 216 at 10060, 2172960, Wed 2026-10-28 to Fri 2026-10-30 by datetime, 0.20881062 -> 0.209, 14282414, 68398886). c043 Example 2.5: hV=2*200=400, mid-move -1000, P=-600 (own arithmetic; lesson text line 120-121).")
row("cards-labels-and-hypotheses", "2.7-cards", "course/modules/FC/FC1/cards.json (every cited Definition/Remark/Example/Proposition/Problem/Assumption/Corollary label)", "PASS",
    "Programmatic check of every such label on each card against its lesson's extracted text. All resolve, except labels written in the lesson's own shorthand ('A1 (trades at the quote)' under 'A1 to A3', 'B3', 'R2 · Where the sign assumption fails' in L05, 'Assumption 2.0' for A1-A3 in L01). c089's 'Problem R2' is L05 R2 (line 517), not the L04 one.")
row("cards-misconception-refs", "2.7-cards / 2.9-prose", "course/modules/FC/FC1/cards.json c017 back; course/modules/FC/FC1/L01.html lines 336-339 (misconception 3)", "FAIL",
    "Card c017 back: 'It is funding from the owners and not a holding (misconception 3).' Current L01 misconception 3 (lines 336-339) no longer says this: it says 'Listing equity as an asset as well as the residual would count it twice in the identity of Remark 1.2'. grep of L01.html for 'funding' and 'owners' returns nothing. The card cites the misconception for a claim its locator does not make. Other misconception references (L02 1-3, L03 1-3, L04 1-3, L05 1-4) match unchanged lesson text. Fix: rewrite c017 back to 'No. Equity is the residual, assets minus liabilities (Definition 1.1). Listing it as an asset as well would count it twice (misconception 3).'")
row("cards-grades-and-basis", "2.7-cards / BUILDER 7", "course/modules/FC/FC1/cards.json c030 (changed), c033, c034, c014, c029", "PASS",
    "c030 now 'the key-results table grades it C': L02.html line 407 has the key-results row 'The four combinations of form and venue all occur (Example 3.1)' graded C with basis 'a hand reading of register entries 1, 3, 4 and 6'. Entries checked in the Lab 2 twin lines 23-39: 1 equities/cash/exchange, 3 equities/derivative/exchange, 4 rates/cash/otc, 6 rates/derivative/otc. c033 entries 3,5,6,8,10,11 are the six derivatives and carry equities, rates, credit, fx, commodities. grades and basis fields present on all C cards.")
row("cards-lesson-agreement", "2.7-cards", "course/modules/FC/FC1/cards.json c042, c058, c081, c089, c093, c101, c067 vs changed lesson text", "PASS",
    "c042 'Under A1 to A3' matches the changed Corollary 2.4 hypothesis (L03.html line 110). c058 matches L04 M3 solution wording (sell stop at or below stop price). c081 matches Remark 2.3 (L05 line 100). c089 matches L05 Problem R2 and Proposition 2.1(ii). c093 matches Remark 4.2 test (L01 line 165-166 'test, not a legal rule'). c067 Remark 2.4 text unchanged. c017 is the exception: see cards-misconception-refs.")
row("cards-notation-Q", "2.4-notation / plan 9.2", "course/modules/FC/FC1/cards.json c039 back ('V = 2Q, where Q is the volume that customers buy') and c042 back ('P = C = sQ')", "FAIL",
    "Still present, unchanged since round 5 (cards.json delta is c030 only). Plan line 474: 'Never use Q for a quantity or quote on an FC1 page.' notation/notation.json entry 7 registers \\mathbb{Q} (risk-neutral measure, AP1). Q here is the customer buy volume. Fix: use an unregistered letter for the customer buy volume in both cards and in L03 Remark 2.2 and Corollary 2.4 (lesson slice; cards and lesson must change together).")
row("mutant-d-set", "2.6-mutation", "ledgers/FC1/mutants/d01..d07", "PASS",
    "mutate_graders_FC1_r6.out: all d01..d07 KILLED (seeds 0-9).")
row("proj-reference-deployment", "2.6-deployment (cross-unit)", "BLUEPRINT.md lines 399-400; course/modules/FC/FC1/grader/reference.py (git-tracked)", "FAIL",
    P + "BLUEPRINT.md line 400 'excludes every grader/reference.py'. git ls-files lists course/modules/FC/FC1/grader/reference.py; no .vercelignore or vercel.json in the repo; grep of tools/build_site.py and tools/coursekit.py finds no exclusion of reference.py. Still FAIL. Fix: add an exclusion of grader/reference.py to the publish step (tools/build_site.py) or move reference solutions out of course/.")
json.dump(R, open(S / "rows_r6.json", "w"), indent=1, ensure_ascii=False)
from collections import Counter
print(Counter(r["status"] for r in R), len(R))
