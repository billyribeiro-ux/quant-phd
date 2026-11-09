"""FC1-a round 2: write the fragment ledgers/FC1/FC1-a.json. Row ids are the round-1 ids (kept), plus r2 rows.

Every evidence string names the command, script output file or line range it rests on. Run from the checkout root:
.venv/bin/python -I ledgers/FC1/scripts/FC1-a-r2/build_fragment_r2.py
"""

import json
from pathlib import Path

ROUND1 = Path("/Users/billyribeiro/.fanout/frags/S-FC1-a.round1.json")
OUT = Path("ledgers/FC1/FC1-a.json")
S = "ledgers/FC1/scripts/FC1-a-r2/"
O = S + "out/"

r1 = json.loads(ROUND1.read_text(encoding="utf-8"))
r1_rows = {r["id"]: r for r in r1["rows"]}

EV = {
    "a-r1-gate-check-pages": f"Re-run at 9294b914: tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS', EXIT=0 ({O}check_pages_unit.out); --all -> 'check_pages FC1: PASS' among 27 units, EXIT=0 ({O}check_pages_all.out).",
    "a-r1-gate-check-dag": f"Re-run: tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS' EXIT=0 ({O}check_dag_unit.out); --all EXIT=0 ({O}check_dag_all.out). Six slice dfn ids each occur once (see a-r1-dag-definitions).",
    "a-r1-gate-check-projects": f"Re-run: tools/check_projects.py --unit FC1 -> 'check_projects FC1: PASS' EXIT=0 ({O}check_projects_unit.out). Outside this slice; run for completeness only.",
    "a-r1-gate-run-labs": f"Re-run: tools/run_labs.py --unit FC1 --page L01 / L02 / L03 -> 'run_labs FC1: PASS (1/1)' each, EXIT=0 ({O}run_labs_L01.out, run_labs_L02.out, run_labs_L03.out).",
    "a-r1-twins-isolated": f"Re-run alone: .venv/bin/python -I -W error tests/labs/FC1/lab-FC1-L01-1.py, L02-1, L03-1 each EXIT=0 ({O}twin_L01.out, twin_L02.out, twin_L03.out).",
    "a-r1-page-code-equals-twin": f"{S}lab_equality_r2.py (output {S}lab_equality_r2.out): L01, L02, L03 page <code> equals twin file (after html.unescape, trailing newline ignored) True; page expected block equals the twin's stdout True; 'ALL EQUAL'.",
    "a-r1-page-smoke": f"Re-run: tools/page_smoke.py --unit FC1 --pages index L01 L02 L03 -> PASS for each page, 'page_smoke FC1: PASS' EXIT=0 ({O}page_smoke.out). Lab runtimes 0.0 s in Pyodide timing.",
    "a-r1-ruff-mypy-twins": f"ruff check tests/labs/FC1 -> 'All checks passed!' ({O}ruff_check.out); ruff format --check -> '8 files already formatted' ({O}ruff_format.out); mypy --no-incremental on the three twins -> 'Success: no issues found in 3 source files' ({O}mypy_twins.out).",
    "a-r1-pytest-relevant": f"pytest tests/test_labs.py -k FC1 -> 8 passed, EXIT=0 ({O}pytest_labs_fc1.out); pytest tests/test_page_checks.py tests/test_run_labs.py tests/test_refs.py -> all passed, EXIT=0 ({O}pytest_tooling_subset.out). Full suite not run.",
    "a-r1-verify-refs-offline": f"tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' EXIT=0 ({O}verify_refs_offline.out). Live: tools/verify_refs.py --unit FC1 -> 'live re-verification of FC1: 2 of 560 entries, 0 problems' EXIT=0 ({O}verify_refs_unit_FC1.out). The keys cited by the slice are harris2002trading and mishkin2021economics only.",
    "a-r1-notation-scan": f"{S}slice_scans_r2.py (output {S}slice_scans_r2.out): math segments of index, L01, L02, L03 (16, 246, 33, 306). Symbols T, Q, R_f, Phi, gamma, R^ast: 0 hits. Single letters used are local per notation.json 'about' (A, B, D, E, K, S, W, N, P, V, I, C, O, h, m, c, d, n, q, s, t, ...). Macros outside standard KaTeX: none.",
    "a-r1-process-banned-scan": f"{S}slice_scans_r2.py: banned/process hits [] on all four pages; ellipses outside code/script [] on all four pages.",
    "a-r1-no-external-no-figures": f"{S}slice_scans_r2.py: no https, <img>, <svg>, <iframe>, data-chart, data-files or assets/data marker on index, L01, L02, L03 ({S}slice_scans_r2.out).",
    "a-r1-hub-structure": "Read course/modules/FC/FC1/index.html lines 1-177 in full: six objectives (lines 47-54), prerequisites (57-65), placement quiz with 9 items, 7 prerequisite and 2 data-skill (67-133), lesson map of five cards (138-144), ladder with four rungs (150-155), data status (159-162), core reading (164-171).",
    "a-r1-hub-hours": "index.html line 29: data-hours-lessons=\"50\" data-hours-project=\"20\" (sums to 70 = curriculum.json FC1 hours); line 39-41 split bar 71.4% and 28.6% (50/70 and 20/70 correct). L01.html, L02.html, L03.html line 2: data-hours=\"10\" each.",
    "a-r1-hub-placement-arithmetic": f"index.html lines 69, 72-131 read in full. Re-derived with {S}numbers_r2.py (hub checks OK): 110/1.1=100; 1+1/2+1/4=1.75; 1000*1.05^2=1102.5; coupon 10000*500/10000=500; period-3 flow 10500; 0.8*9=7.2 so eight correct needed; 7/9=77.78 printed as 78 (nearest whole percent, not stated as a rounding rule; advisory only).",
    "a-r1-hub-lesson-titles": "index.html lines 139-141 card titles equal the h1 of L01 (line 35: 'Money, Banks and Financial Intermediaries'), L02 (line 35: 'Markets, Exchanges and the Instrument Taxonomy') and L03 (line 35: 'Dealers, Market Makers and the Bid–Ask Spread').",
    "a-r1-hub-prereq-titles": "curriculum/curriculum.json: P0.1 title 'How to Study This Program' (line 6223-6224); E1 title 'Microeconomics' (7339-7340); FC1 title 'The Financial System, Markets & Instruments', tier U, hours 70, prereqs [P0.1, E1] (7727-7735); Part FC title 'Finance Core' (7709). Hub line 31 and 35 match.",
    "a-r1-hub-reading-and-year": f"index.html lines 164-171 render keys only (data-cite; refs.js renders from the registry). Live verify_refs for FC1: 0 problems ({O}verify_refs_unit_FC1.out). L03 line 564 states the registry year 2002 for harris2002trading, matching the registry. No year or edition stated for mishkin2021economics on any FC1 slice page.",
    "a-r1-hub-rung-claims": "index.html lines 151-154 against project.html line 45-46 (rung 1: 'one bond and one trade, both simulated'; rung 2: 'fill in the two blanks, the discount exponent ... and the trade's cash flow') and tests/labs/FC1/lab-FC1-project-2.py (blanks: exponent of the discount and the settlement cash flow). Rung 1 includes the coupon cash flow (project lab 1, step 1). All claims match.",
    "a-r1-hub-data-status": f"index.html lines 159-162 read. {S}slice_scans_r2.out: no dataset marker on any slice page. No data-files attribute in the FC1 pages (grep over course/modules/FC/FC1/*.html returned none).",
    "a-r1-l01-example-3.3-numbers": f"L01.html lines 122, 127, 403 and key row line 459. {S}numbers_r2.py: S_1=1900, S_2=2710, S_10 exact = 1000*(1-0.9^11)/0.1 = 6861.8940391 (10 places), multiplier 6.8618940391, 4 places 6.8619, 6.8619*1000=6861.90 (rounded-first alternative), cents 686189 = half-up of exact value; all OK.",
    "a-r1-l01-prop-2.2": "L01.html lines 88-96 read. X_t + l_t = rho D_t + (1-rho) D_t = D_t by A1 and the loan definition; summation gives the cumulative statement. Hypotheses (Assumption 2.0) stated. No gap.",
    "a-r1-l01-prop-3.1": f"L01.html lines 102-113 read. Closed form equals the geometric sum (q=1-rho, q != 1 since rho>0); limit d/rho under 0<rho<=1; rho=1 case checked. {S}numbers_r2.py: closed form equals the exact partial sum on 400 random rational cases (rho in (0,1], n in 0..40): OK.",
    "a-r1-l01-prop-3.5": f"L01.html lines 130-143 read. Recursion D_{{t+1}} = phi(1-rho) D_t; (1-kappa)-rho = (1-rho)(1-phi) re-derived; equality iff phi=1 or rho=1. {S}numbers_r2.py: 400 random exact cases confirm limit <= d/rho and equality iff phi=1 or rho=1: OK. Example 3.6 (1818.18; 18.18 percent) re-derived OK.",
    "a-r1-l01-prop-4.1": "L01.html lines 149-162 read. Assets A-lambda, deposits K, equity (K+E-lambda)-K = E-lambda by Remark 1.2; nonnegative iff lambda <= E. Re-derived.",
    "a-r1-l01-problems": f"L01.html lines 349-446 (M1-M3, P1-P3, E1-E3, R1-R3) read and re-derived: M1 100 and 400; M2 1850 (800, 600, 450); M3 -20; E2 2/11 and 18.18 percent; E3 100 dollars. R1 bound: S_n <= d*sum_(t>=0)(1-c)^t = d/c, checked on 300 random paths ({S}numbers_r2.py: OK). The expression '= d/c' is correct when the sum runs over all t >= 0; advisory, not a defect.",
    "a-r1-l01-quiz": f"L01.html lines 466-541: 10 items, each answer and explain re-derived (reserve 100; D_1 800; rho=0 gives n+1; 1.75; 10000; smaller; equity 40; 700). {S}numbers_r2.py L01 quiz checks OK.",
    "a-r1-l01-misconceptions-canon": "L01.html lines 313-341 read: canon-breaks four bullets (lines 316-321) and three misconceptions (328-339) with the stated values 1900, 6.8619 and the equity test. Re-derived OK.",
    "a-r1-l01-lab-hypothesis-interpretation": f"L01.html lines 171 and 310 against {O}twin_L01.out: 6.8619, limit 10.0000 (Part A), 181818 vs 1000000 cents (Part C), True/True/False sign test (Part D). Every printed statement matches the hypothesis and interpretation.",
    "a-r1-l01-key-rows-1-6": "L01.html lines 454-459: rows 1-6 each match the lesson (Prop 2.2, Prop 3.1, Prop 3.5, Remark 3.2, Prop 4.1, Example 3.3), with T grades and bases read by hand (ruling 13 satisfied).",
    "a-r1-l01-why-it-matters": "L01.html line 51: 79 words (limit 120). Forward pointer 'defined in Definition 1.1' is explicit.",
    "a-r1-l01-grade-lab-row7": "NOW PASS. L01.html line 460 grade is C with basis 'Lab 1, Parts A to D (typed-in parameters)'. The row's claim rests only on printed lab output, so C is the grade required by ruling 13 (FINAL-ARCHITECT-RULINGS.md item 13). The round-1 FAIL is resolved.",
    "a-r1-l01-cards-lab-T": "NOW PASS. cards.json FC1-c014, FC1-c092, FC1-c093 and FC1-c125 are grade C with basis naming Lab 1 Part A, C, D and B respectively (scripts check: 'C without basis: []'). Matches key row 7 (C). The round-1 FAIL is resolved.",
    "a-r1-l01-card-c153-locator": "NOW PASS. cards.json FC1-c153 back: 'for an initial deposit d > 0 as in Section 2 (Proposition 3.5)'. L01.html line 84 is where Section 2 takes d > 0. The round-1 FAIL is resolved.",
    "a-r1-l01-cards-other": "All 35 L01 cards read in full: FC1-c001 to c018, c091, c092, c093, c094, c103, c104, c110, c111, c122, c125, c126, c136, c146, c147, c148, c152, c153. Each matches its L01 lesson text and cites the right remark, example or proposition. No wrong statement found.",
    "a-r1-l02-prop-1.4-2.5": "L02.html lines 71-124 read. Proposition 1.4 (E and O disjoint, union is the n trades) and Proposition 2.5 (each entry counted once per axis) re-derived; Assumption 1.3 and Definition 2.1 stated before use.",
    "a-r1-l02-remark-2.6-P2-P3": "L02.html lines 126-129, 331-344. Remark 2.6: an entry with k exposure values makes the total exceed n by k-1; P3 gives |S|-1. Re-derived; P2 double-count |E|+|O| = n+1 re-derived.",
    "a-r1-l02-lab-hypothesis-output": f"L02.html lines 133 and 246 against {O}twin_L02.out and the twin's REGISTER literal read via ast ({S}numbers_r2.py L02 checks all OK): exposure 3,3,2,2,2; form 6,6; venue 4,8; exchange entries 4 (1 cash, 3 derivative) spanning 3 exposure classes; 14 for 13 entries.",
    "a-r1-l02-examples-misconceptions": "L02.html lines 253-256 (Example 3.1: entries 1, 3, 4, 6 give the four combinations, verified against the twin REGISTER) and lines 279-289 (misconceptions 1-3: entries 3, 5, 6, 8, 10, 11 cover all five exposures; exchange entries span commodities, equities, rates).",
    "a-r1-l02-problems": "L02.html lines 299-395: M2 counts (2,1,1,1,0 sum 5), E2 75 percent with base stated, R1 rates entries 4, 5, 6 (confirmed in REGISTER), P2, P3, R3 re-derived. Every problem has a worked solution.",
    "a-r1-l02-key-rows-1-4": "L02.html lines 404-407: rows 1-3 T (Prop 1.4, Prop 2.5, Remark 2.6) and row 4 C (Example 3.1 hand reading, basis named).",
    "a-r1-l02-grade-lab-row5": "NOW PASS. L02.html line 408: row 5 grade C with basis 'Lab 2, Part B (typed-in register)'. Printed counts only, so C is required by ruling 13. The round-1 FAIL is resolved.",
    "a-r1-l02-cards-lab-T": "NOW PASS. cards.json FC1-c029, FC1-c095 and FC1-c096 are grade C with basis 'Lab 2, Part B (typed-in register)'. The round-1 FAIL is resolved.",
    "a-r1-l02-cards-other": "All 24 L02 cards read in full (21 'other' cards: FC1-c019 to c028, c030 to c034, c115, c116, c120, c127, c149, c150; plus c029, c095, c096). Each is correct against the L02 text. The near-duplicate c025/c033 is recorded under a-r1-cards-dup-gaps, not here.",
    "a-r1-l02-forward-pointers": f"L02.html line 270 names Lesson 4 (order types, limit order book) and Lesson 5 (clearing and settlement). L04.html defines def-order-types and def-limit-order-book; L05.html defines def-clearing-and-settlement and def-trade-lifecycle. Pointers accurate; no earlier use of those terms is a formal use.",
    "a-r1-l02-why-it-matters": "L02.html line 50: 104 words (limit 120). Pointer 'Proposition 2.5' (line 50) matches the lesson's Proposition 2.5 at line 117.",
    "a-r1-l03-prop-2.3": "L03.html lines 96-106 read. Proof re-derived: sigma q p - sigma q m_n = sigma q (m_t - m_n) + h q (sigma^2 = 1). Identity checked on 500 random integer sequences with exact arithmetic ({S}numbers_r2.py: OK).",
    "a-r1-l03-cor-2.4-remark-2.2": "L03.html lines 92-116. Remark 2.2 gives V = 2W for a closed sequence; Corollary 2.4 gives P = C = sW with s = 2h; cash of a closed one-mid sequence equals 2h W on random cases ({S}numbers_r2.py: OK). Notation now uses W (the former Q is gone from the page).",
    "a-r1-l03-example-2.5": f"L03.html lines 118-121: C = -9998*100 + 9992*100 = -600; spread term 2*200 = 400; mid-move -1000; profit -600 ({S}numbers_r2.py L03 Example 2.5 checks OK). Key row 3 T with 'Computed by hand' basis.",
    "a-r1-l03-prop-3.2": f"L03.html lines 148-159 read. Asymmetric profiles, symmetric k=0, k=1, k=2 and k>=3 cases re-derived. Brute force over whole-cent grids ({S}numbers_r2.py: c=100 N=1000 to c+10 and c+40; c=0 N=2 to c+10; c=7 N=4 to c+25) gives exactly (c,c), (c+1,c+1), (c+2,c+2).",
    "a-r1-l03-R1-three-dealers": f"L03.html lines 445-451: three-dealer symmetric profiles re-derived; brute force with c=100, N=300, grid c..c+5 ({S}numbers_r2.py) gives (c,c,c) and (c+1,...) equilibria, (c+2,...) not; payoff at (c+2) = 2N/3 OK.",
    "a-r1-l03-lab-output": f"L03.html lines 168, 333 against {O}twin_L03.out. Re-derived in {S}numbers_r2.py from the stated seed protocol: Part A cash 4000, 14 trades; Part B terminal mid 10001, spread capture 4000, mid-move -545, mark-to-mid 3455 = 4000-545. All OK.",
    "a-r1-l03-problems": "L03.html lines 370-462 re-derived: M1 200 = sW; M2 cash -160, spread term 320, mid-move -480; M3 30/5000 = 0.6 percent; E3 0.03 percent; R2 cash 1400, spread 400, mid-move +1000 (only the mid-move term changes); R1 and R3 re-derived.",
    "a-r1-l03-key-rows": "L03.html lines 475-480: row 3 T (Example 2.5, computed by hand), row 4 T (Prop 3.2 proved in section 3), rows 5-6 C naming Lab 1 Parts A/B and Part C; their bases name the same lab parts as cards c052, c053, c098 and c054.",
    "a-r1-l03-misconceptions-canon": "L03.html lines 336-362: canon-breaks (four bullets) and misconceptions 1-3 re-derived; the Example 2.5 numbers, 100 shares times the 10-cent gap, equal -1000.",
    "a-r1-l03-quiz": f"L03.html lines 490-558: 9 items; answers re-derived (4; 200; -1000; closed sequence; 121 pairs; (103,103) with 1500 vs 2000; 1000; tick). {S}numbers_r2.py L03 quiz checks OK.",
    "a-r1-l03-notation-Q": f"NOW PASS. L03 uses W (customer-buy volume) throughout (lines 88, 93, 110, 115 and 340); no plain Q appears in any L03 math segment ({S}slice_scans_r2.out single-letter list for L03). The round-1 advisory is resolved.",
    "a-r1-l03-references-harris": f"L03.html line 341 and 564: registry key harris2002trading, registry year 2002, book level only, no locator. Matches references/references.json and the live verify_refs ({O}verify_refs_unit_FC1.out).",
    "a-r1-l03-why-it-matters": "L03.html line 51: 104 words (limit 120). It uses 'dealer' and 'quoted spread' in plain words before Definitions 1.1 and 1.2, but the same paragraph says 'This lesson defines the dealer and the bid-ask spread'. Accepted as an explicit forward pointer (advisory; see a-r1-define-before-use).",
    "a-r1-l03-cards": "All 39 L03 cards read in full (FC1-c035 to c055, c097, c098, c105-c108, c112, c113, c117, c128-c131, c137-c140, c151). Each is correct against the L03 text and its numbers appear in the lesson or its lab output.",
    "a-r1-cards-grade-convention": f"cards.json: 55 of 98 L01-L03 cards have no grade field, 15 are C, 28 are T (definitions and statements that are not graded results); all 15 cards with grade C have a basis ({S}cards_dup_scan_r2.py: 'C without basis: []'; grades used: T, C, none). Convention accepted.",
    "a-r1-cards-dup-gaps": f"FAIL. cards.json FC1-c025 and FC1-c033 test the same fact, that a derivative carries an exposure of its own: c025 back 'A derivative has an exposure as well. A futures contract on a government bond is a derivative with rates exposure...'; c033 front 'Are derivatives a separate asset class with no exposure of their own?' back 'No... derivatives carry exposures (misconception 2; Remark 2.2)'. A full scan of the 98 slice cards ({S}cards_dup_scan_r2.py) found no other pair testing one fact. Advisory, not counted: c050 and c055 both state that (c+1,c+1) and (c+2,c+2) are equilibria, but c050 asks the full equilibrium set and c055 asks the misconception. Gaps: every definition, theorem, key result and misconception of L01-L03 has at least one card (checked against the lesson section lists).",
    "a-r1-dag-definitions": "dfn with data-concept: L01 def-financial-intermediary (line 59), def-bank-money-creation (line 81); L02 def-exchange-vs-otc (line 58), def-asset-class-taxonomy (line 92); L03 def-market-maker (line 57), def-bid-ask-spread (line 62). Each defined once ({S}slice_scans_r2.out). Links: L01 -> geometric-series (M1, in closure); L03 -> bertrand-competition (E1, in closure); hub -> L01/L02 anchors. concepts.html anchors exist (grep: id=\"bertrand-competition\", id=\"geometric-series\"). check_dag PASS.",
    "a-r1-prose-future-concepts": "L02.html lines 103, 113, 284, 301 name futures contracts, interest rate swaps, credit default swaps and forwards as plain prose examples (no class=concept, no dfn, no link). Architect default for out-of-closure concepts (plans/FC1-build-plan.md, Architect decisions). Accepted.",
    "a-r1-define-before-use": "First formal uses are after their dfn in each lesson. Pre-definition plain-language uses: L01 line 51 ('financial intermediary (defined in Definition 1.1)'), L02 line 50 ('This lesson defines the two kinds of market'), L03 line 51 ('This lesson defines the dealer and the bid-ask spread'); each is an explicit forward pointer in the why-it-matters paragraph. Hub line 33 names limit order book and settlement as overview terms. Accepted as advisory (verifier hunt class 5 checked).",
    "a-r1-scope-words": f"{S}slice_scans_r2.out: every, all, always, never, any, across, drives, only counted per page (L01: every 14, any 10, only 10; L02: every 8, any 9; L03: every 18, any 7). Each strong hit in prose re-read against its proof, computation or explicit hypothesis (listed in the notes). No unsupported universal found.",
    "a-r1-prose-attributions": "No locator, page, table or bibliographic data for a source on L01-L03 except harris2002trading (L03 lines 341, 564, registry year 2002, book level). Hub line 166 names McLeay, Radia & Thomas (2014) as not yet in the registry and not cited; no data-cite. Advisory: the hub types the curriculum's author and year for an unregistered source; not a citation.",
    "a-r1-structure-counts": "L01, L02, L03: why-it-matters (<=120 words), core sections, labs, canon-breaks, misconceptions (3 each), problem set (3 per tier in Mechanics, Proof, Empirical, Research), key-results table, quiz (10, 10, 9 items), references section. Debate brief not required (no debate key).",
    "a-r1-hours-lessons": "L01, L02, L03 data-hours=10 (line 2 each); hub data-hours-lessons=50 for five lessons; sums agree with curriculum 70 total (hub 50 + project 20).",
    "a-r1-mutants-not-applicable": f"Labs are demonstrations, and mutation testing applies to project graders only (FINAL-ARCHITECT-RULINGS, verifier ruling). No grader in this slice. Three scratch lab mutants were run anyway as evidence for the lesson claims that a lab 'checks' something; see a-r2-lab-mutants.",
}

NEW = {
    "a-r2-delta-hunks": ("2.1-round-delta", "course/modules/FC/FC1/{index,L01,L02,L03}.html, cards.json, plans/FINAL-ARCHITECT-RULINGS.md",
        "PASS",
        f"Delta aeb512b6..9294b914 for the slice (git diff --stat): index.html (two hunks: placement prompt at line 86 and its explanation at line 97, Q->q), L01.html (hunks at lines 86, 408-417 for the E2 and E3 prompts and solutions, and 460), L02.html (hunks at lines 50, 392, 407, 408 and 425), L03.html (hunks at lines 80, 88-115, 333, 351, 366, 374, 476, 507 and 520: the Q-to-W rename and wording), cards.json (58 lines: grade changes c014, c092, c093, c125, c029, c095, c096; c153 back; c060/c066/c131/c135/c141 L04 and L03 wording; new c154-c156 are L04). Twins and tests/labs/FC1 unchanged. FINAL-ARCHITECT-RULINGS.md rulings 17-20 added (not FC1). Every slice hunk was read; each affected row was re-verified from scratch (no row carried)."),
    "a-r2-numbers-recompute": ("2.2-numbers", f"{S}numbers_r2.py (output {S}numbers_r2.out)", "PASS",
        "Independent recomputation written from the page statements, not the lab code: 97 checks OK, 0 BAD: hub placement arithmetic; L01 deposit path and cents (100000..686189); S_10 decimals; Example 3.3/3.6; leakage 181790 and 181818; E2 ratio 2/11; M1-M2-M3; Prop 3.1 and 3.5 random exact cases; R1 bound; L02 register counts from the twin's REGISTER literal; L03 Example 2.5, M2, R2, Prop 2.3 and Cor 2.4 random cases; tick game brute force (four grids); three-dealer brute force; the seeded Lab 1 Part A/B values re-derived (cash 4000, 14 trades, terminal 10001, capture 4000, mid-move -545, P&L 3455)."),
    "a-r2-lab-mutants": ("2.5-labs", f"{S}lab_mutants_r2.py; mutant files {S}lab_mutants/mut_L01.py, mut_L02.py, mut_L03.py", "PASS",
        "Three scratch student-error mutants of the lab twins (copies in /tmp/fc1a-r2-mut and archived under lab_mutants/): L01 closed form uses (1-rho)^n instead of (1-rho)^(n+1) -> 'the partial sums equal the closed form exactly for n = 0 to 10: False'; L02 well-formed check accepts two values per axis -> 'malformed entry rejected: False'; L03 spread capture doubled -> 'mark-to-mid P&L equals spread capture plus mid-move term: False'. Each lab-claimed verdict flips, so the lesson sentences that say the lab checks these identities are backed by live checks. Mutants are not stored under ledgers/FC1/mutants (that folder holds project grader mutants)."),
    "a-r2-cards-near-dup-scan": ("2.7-cards", f"{S}cards_dup_scan_r2.py", "PASS",
        "Scan of all 98 L01-L03 cards: ids match FC1-c\\d{3}; no duplicate ids; every C card has a basis; difflib pairs above threshold reviewed by hand. Pairs that look alike on the stem (c036/c137, c108/c113, c048/c113, c013/c122, c053/c097, c095/c096, c110/c111, c152/c153) test different facts and are not duplicates. The one duplicate fact is recorded in a-r1-cards-dup-gaps."),
}

rows = []
for r in r1["rows"]:
    rid = r["id"]
    assert rid in EV, f"no evidence written for round-1 row {rid}"
    status = "FAIL" if rid == "a-r1-cards-dup-gaps" else "PASS"
    row = {"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": EV[rid]}
    if status != "PASS":
        row["fix"] = ("Reword FC1-c025 (cards.json) so it tests only the reason for a second axis: one heading would hide either "
                      "the form or the exposure of a futures contract on a government bond (Remark 2.2). Delete its sentence "
                      "'A derivative has an exposure as well.' Keep FC1-c033 as the single card for misconception 2. Keep all ids. "
                      "No change to any lesson text.")
    rows.append(row)

for rid, (check, loc, status, ev) in NEW.items():
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})

stale = set(EV) - set(r1_rows)
assert not stale, stale

fragment = {
    "unit": "FC1",
    "slice": "FC1-a",
    "round": 2,
    "verifier": "Claude Haiku 5.5 independent verifier, FC1-a round 2 (final full verification; did not build FC1; read verifier-rules.md, VERIFIER_RULES.md, CLAUDE.md, BUILDER_RULES.md, plans/FC1-build-plan.md with its Architect decisions, plans/FC1-open-items.md, plans/FINAL-ARCHITECT-RULINGS.md, and the round-1 fragment as context only)",
    "pin": "9294b914a51647c66d2dee62c4a112c76ba04900",
    "base": "aeb512b6 (round-1 pin). Slice delta aeb512b6..9294b914 read hunk by hunk (see a-r2-delta-hunks). Every round-1 row id is kept; no row carried, every row re-verified from scratch at 9294b914. Five round-1 FAIL rows are now PASS after the fixes; one round-1 PASS row (a-r1-cards-dup-gaps) is FAIL on re-verification.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS2-FC1-a",
    "scratch": "/tmp/fc1a-r2-mut/ (lab mutant copies only)",
    "verified_at": "2026-11-09T04:59:44+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [
        {"id": "lab-mut-L01-closed-form-exponent", "description": "Lab 1 twin closed form uses (1-rho)^n instead of (1-rho)^(n+1): the exact partial-sum check prints False.", "killed_by": "L01 printed verdict 'the partial sums equal the closed form exactly for n = 0 to 10: True' flips to False"},
        {"id": "lab-mut-L02-well-formed-accepts-two-values", "description": "Lab 2 twin well-formed check accepts two values on one axis: the malformed-entry rejection prints False.", "killed_by": "L02 printed verdict 'malformed entry rejected: True' flips to False"},
        {"id": "lab-mut-L03-spread-capture-doubled", "description": "Lab 3 twin spread capture doubled (2*half*V): the mark-to-mid identity prints False.", "killed_by": "L03 printed verdict 'mark-to-mid P&L equals spread capture plus mid-move term: True' flips to False"},
    ],
    "registry_flags": [
        "harris2002trading: curriculum yaml 383-386 year 2003 vs registry year 2002 (registry notes.year conflict, unresolved; the slice states the registry year only)",
        "mishkin2021economics: curriculum year 2022 vs registry record 2021 (notes.year conflict, unresolved; the hub cites the key only)",
        "McLeay, Radia & Thomas (2014), Bank of England Quarterly Bulletin Q1 (curriculum yaml 386): not in references.json; REFERENCE_REQUEST, not cited by any slice page; named in the hub as not cited"
    ],
    "freshness_flags": [],
    "notes": [
        "Scripts backing the rows are under ledgers/FC1/scripts/FC1-a-r2/: gates.sh and out/*.out (gate outputs), lab_equality_r2.py, numbers_r2.py, slice_scans_r2.py, cards_dup_scan_r2.py, lab_mutants_r2.py with lab_mutants/, build_fragment_r2.py, and the tooling pytest and verify_refs outputs in out/.",
        "Gates re-run at 9294b914 and all PASS: check_pages --unit and --all, check_dag --unit and --all, check_projects --unit, run_labs --page L01/L02/L03, twins under python -I -W error, page_smoke for index, L01, L02, L03, ruff check and format, mypy --no-incremental on the three twins, verify_refs --offline and --unit FC1 (live, 0 problems), fetch_data --check, pytest test_labs -k FC1, test_page_checks, test_run_labs, test_refs.",
        "Advisory, not counted: the hub placement sentence 'seven of nine is 78 percent' rounds 77.78 to the nearest whole percent without naming the rule (a-r1-hub-placement-arithmetic).",
        "Advisory, not counted: L01 Problem R1 writes 'S_n <= d sum_t (1-c)^t = d/c'. It is correct when the sum runs over all t >= 0; the lesson could write the infinite sum explicitly.",
        "Advisory, not counted: FC1-c050 and FC1-c055 both state that (c+1,c+1) and (c+2,c+2) are equilibria; they ask different questions.",
        "Advisory, not counted: the L01, L02, L03 why-it-matters paragraphs use three terms in plain words before their definitions, each with an explicit 'defined in' or 'This lesson defines' pointer.",
        "Scope words checked by slice_scans_r2.out and a manual read of each strong hit; no universal claim lacks a proof, computation or hypothesis.",
        "Checked and clean: notation (no registered symbol misused; no Q, T, R_f, Phi or gamma in any slice math), banned phrases (none), ellipses outside code (none), external or data markers (none), hub hours split (50 + 20 = 70), lab code equals twin and expected equals twin stdout, DAG (six dfn, two closure links, no link to a later lesson).",
        "Not checked: rendered screenshots at 360 px and in dark mode beyond page_smoke's automated checks; the full pytest suite; graders and project pages (other slices); L04 and L05 cards (other slices); the hours estimates were checked for arithmetic only, not re-estimated; live Crossref run for entries outside FC1 (not cited by the slice).",
        "Round-1 fragment at /Users/billyribeiro/.fanout/frags/S-FC1-a.round1.json was read as context only; no round-1 PASS row was carried."
    ],
    "summary": "FC1-a round 2 at 9294b914: 75 rows (71 round-1 ids kept and re-verified, 3 new r2 rows... see rows), 74 PASS, 1 FAIL. FAIL: a-r1-cards-dup-gaps (near-duplicate cards FC1-c025 and FC1-c033 test the same fact). The five round-1 FAILs (a-r1-l01-grade-lab-row7, a-r1-l01-cards-lab-T, a-r1-l01-card-c153-locator, a-r1-l02-grade-lab-row5, a-r1-l02-cards-lab-T) are PASS after the fixes applied at 9294b914.",
}

# Make the summary's counts exact
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
fragment["summary"] = (
    f"FC1-a round 2 at 9294b914: {len(rows)} rows ({len(r1['rows'])} round-1 ids kept and re-verified, {len(NEW)} new), "
    f"{n_pass} PASS, {n_fail} FAIL, 0 UNVERIFIABLE. FAIL: a-r1-cards-dup-gaps (FC1-c025 and FC1-c033 test the same fact). "
    "The five round-1 FAILs (a-r1-l01-grade-lab-row7, a-r1-l01-cards-lab-T, a-r1-l01-card-c153-locator, a-r1-l02-grade-lab-row5, "
    "a-r1-l02-cards-lab-T) are PASS after the fixes applied at 9294b914."
)
OUT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", OUT, "rows", len(rows), "pass", n_pass, "fail", n_fail)
