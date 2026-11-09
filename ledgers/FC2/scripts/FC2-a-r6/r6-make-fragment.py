# Round-6 fragment builder for FC2 slice a (writes ledgers/FC2/FC2-a.json in the checkout only).
import json
S = "ledgers/FC2/scripts/FC2-a-r6/"
C5 = "Carried from round 5 ({files} byte-identical since the previous pin dde0486b): "
def carry(files, ev):
    return C5.format(files=files) + ev
rows = []
def r(id_, check, loc, status, ev):
    rows.append({"id": id_, "check": check, "location": loc, "status": status, "evidence": ev})

GATES = S + "r6-gates.out"
r("FC2a-cmd-check_pages", "2.9 structure; check_pages --unit FC2", "course/modules/FC/FC2/index.html, L01.html, L02.html, L03.html", "PASS",
  "`.venv/bin/python tools/check_pages.py --unit FC2` -> 'check_pages FC2: PASS', rc=0 (" + GATES + ").")
r("FC2a-cmd-check_dag", "2.9 DAG; check_dag --unit FC2", "course/modules/FC/FC2/*.html", "PASS",
  "`tools/check_dag.py --unit FC2` -> 'check_dag FC2: PASS', rc=0 (" + GATES + ").")
r("FC2a-cmd-check_projects", "2.6 project gate, unit level (not judged in slice a)", "course/modules/FC/FC2/project.html", "PASS",
  "`tools/check_projects.py --unit FC2` -> 'check_projects FC2: PASS', rc=0 (" + GATES + ").")
r("FC2a-cmd-run_labs", "2.9 labs; run_labs --unit FC2 and --page L01/L02/L03", "L01.html, L02.html, L03.html lab sections", "PASS",
  "`tools/run_labs.py --unit FC2` -> 'run_labs FC2: PASS (11/11)'; `--page L01`, `--page L02`, `--page L03` each 'PASS (1/1)', rc=0 (" + GATES + ").")
r("FC2a-cmd-twin-direct", "2.9 twins alone under python -I -W error", "tests/labs/FC2/lab-FC2-L01-1.py, lab-FC2-L02-1.py, lab-FC2-L03-1.py", "PASS",
  "`.venv/bin/python -I -W error <twin>` rc=0 for all three; stderr 0 bytes (" + S + "r6-twin-L01/L02/L03.err); stdout in " + S + "r6-twin-L0x.out.")
r("FC2a-cmd-page_smoke", "2.9 browser smoke for slice pages (alone)", "index.html, L01-L03", "PASS",
  "`tools/page_smoke.py --unit FC2 --pages index.html L01.html L02.html L03.html` -> 'page_smoke FC2: PASS', rc=0 (" + GATES + ").")
r("FC2a-cmd-ruff-mypy", "2.9 ruff check/format; mypy --no-incremental on the three twins", "tests/labs/FC2/lab-FC2-L01-1.py..L03-1.py", "PASS",
  "ruff check: 'All checks passed!'; ruff format --check: '3 files already formatted'; mypy --no-incremental: 'Success: no issues found in 3 source files' (" + GATES + ").")
r("FC2a-cmd-pytest", "2.9 relevant pytest", "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_curriculum.py, test_docs_figures.py", "PASS",
  "`.venv/bin/python -m pytest -q` on the five files: all dots, rc=0 (" + GATES + ").")
r("FC2a-cmd-verify_refs", "2.9 registry; verify_refs --offline", "index.html data-cite list (hull2021options, stoll1969relationship, cox1979option)", "PASS",
  "`tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', rc=0 (" + GATES + ").")
r("FC2a-links", "2.9 internal links and anchors", "index.html, L01-L03", "PASS",
  "Script " + S + "r6-anchors.py (python -I, run on the checkout): 72 hrefs checked, 0 missing files, 0 missing anchors (" + S + "r6-anchors.out).")
r("FC2a-twin-equals-page", "2.9 page code equals twin; expected equals output", "L01.html, L02.html, L03.html lab sections", "PASS",
  "Script " + S + "r6-twin-vs-page.py (python -I): page data-run code == twin file, and pre.expected == twin stdout, for L01, L02, L03 (" + S + "r6-twin-vs-page.out); run_labs PASS (" + GATES + ").")
r("FC2a-hub-hours", "hours arithmetic", "index.html data-hours-lessons/project (:29, :39, :41); L01-L08 data-hours (line 2)", "PASS",
  "Re-read this round: index.html:29 data-hours-lessons=60, data-hours-project=30; lesson data-hours 6,8,9,7,8,8,8,6 (L01..L08) sum to 60; 60+30=90; 66.7%/33.3% split at index.html:39 and :41; L03.html:2 data-hours=9. index.html and L01-L08 hour attributes unchanged in the delta except L03 text.")
r("FC2a-hub-placement-arithmetic", "placement quiz arithmetic", "index.html #placement (lines 67-128)", "PASS",
  carry("index.html", "Nine items; six on M4/CF1/M1, one FC1, two skill checks; -100+60/1.1+60/1.21=4.1322; 1/1.1025=0.9070; 7/9=77.8%, 8/9=88.9% (round-5 rederive, ledgers/FC2/scripts/FC2-a-r5/rederive.out; index.html unchanged)."))
r("FC2a-hub-prose", "hub prose: lede, prerequisites, ladder, data status", "index.html:33, :35, :59-63, :150-152, :157-159; project.html:44, :55, :226, :228, :241, :285, :333, :360, :672", "PASS",
  carry("index.html and the cited project.html lines (project.html changed only at line 519, not cited)", "Lede, prerequisite closure, ladder rung text and data statement as in round 5; coursekit closure unchanged (check_dag PASS this round)."))
r("FC2a-structure-lessons", "2.5 lesson structure", "L01.html, L02.html, L03.html", "PASS",
  "Re-read L03.html in full this round (lines 1-529): sections 1-9, meta-row, grade legend, lab section with hypothesis/interpretation, key-results table, quiz with data-cards, references, lesson-nav present. L01/L02 unchanged since round 5 (carried structure).")
r("FC2a-numbers-prose", "numbers in prose vs unrounded values and displayed digits", "L01-L03 prose, solutions, quizzes, key results, hub", "PASS",
  "Re-derived this round by " + S + "r6-rederive.py (python -I; " + S + "r6-rederive.out): L03 margins 39,31,34,-35,34,-13,-36,23,29,-22, balance 84, 4 loss days; DF to six places; par 0.049026 (4.9026 percent); payment 4902625 cents = 49026.25 dollars; value -4415468; M2 DF_3 0.839619; M3 sum 2.6730119, value 2.67 to the cent, 0.0267301; R3 DF_2 0.924642, par 0.039756 (3.9756 percent); flat 3 percent DF_2 0.942596. L01/L02 numbers carried from round 5 (byte-identical pages).")
r("FC2a-L01-math", "mathematics: Sections 1-3 of L01", "L01.html lines 53-146", "PASS",
  carry("L01.html", "Props 2.1, 2.2, 3.2, 3.5 proofs, Example 2.4, Example 3.4 psi formulas, Remark 3.6 boundaries (round 5 line-by-line)."))
r("FC2a-L01-problems", "problem sets and quiz of L01", "L01.html lines 319-520", "PASS",
  carry("L01.html", "M1-M3, P1-P3, E1-E3, R1-R3 solutions and quiz Q1-Q10 (round 5)."))
r("FC2a-L02-math", "mathematics: Sections 1-4 of L02", "L02.html lines 53-268", "PASS",
  carry("L02.html", "Prop 2.2 Cases 1-2, Prop 3.1 proof, Corollary 3.2, Remark 2.5, Example 2.4 (round 5)."))
r("FC2a-L02-problems", "problem sets and quiz of L02", "L02.html lines 300-493", "PASS",
  carry("L02.html", "P1-P3, E1-E3 (value 237.1077), R1-R3, M1-M3, quiz Q1-Q9 (round 5)."))
r("FC2a-L03-math", "mathematics: Sections 1-3 of L03", "L03.html lines 53-150", "PASS",
  carry("L03.html lines 53-150", "Re-read this round: Definition 1.1-1.2, A8', Prop 1.3 and proof (telescoping), Remark 1.4-1.5, Section 2, Definition 3.1, A8 (positivity counterexample n=2 gives 0 = 3/2), Prop 3.2 and proof, Prop 3.3 and proof, Example 3.4 (flat curve, rho=0 case; rederive: par == flat rate exactly for rho in {6,3,0,-1} percent, n=1..7), Prop 3.5 and proof, Remark 3.6. The delta hunks in this file are at lines 51, 298, 306, 318, 328, 385, 463, 506, 509 only (git diff -U0), none inside 53-150."))
r("FC2a-L03-problems", "problem sets of L03", "L03.html:311-414 (M1 :318, M2 :328, E3 :385 changed)", "PASS",
  "Re-verified this round, the subject changed. M1 (three-day path, margins 3, -4, 2; balances -1 = 99-100 and 1 = 101-100) correct. M2 (flat 6 percent, DF_3 = 1/1.191016 = 0.839619) correct. M3 (2.6730119 unrounded; displayed factors sum 2.673011; 2.67 to the cent) correct. P1-P3, E1 (largest loss -36 on day 7; prices 5090, 5054), E2, R1-R3 recomputed (" + S + "r6-rederive.out). E3 (L03.html:385) now says the par rate 4.9026 percent 'is not one of the five typed-in zero rates ... differs from each of them, and it lies strictly between the 4.5 and 5 percent rates. That is a fact of these inputs, not a general rule'; every number re-derived (4902625 cents = 49026.25 dollars; 4.5 < 4.9026 < 5). The round-5 non-sequitur is removed. Residual, not a FAIL: E3 answers 'say why' with a fact of the printed value, not a mechanism; the lesson proves no general mechanism for that (R2 is n=2 only).")
r("FC2a-lab-L01-claims", "lab hypothesis and interpretation claims", "L01.html lab-FC2-L01-1 hypothesis (line 150), interpretation (286); misconceptions", "PASS",
  carry("L01.html and tests/labs/FC2/lab-FC2-L01-1.py", "Printed output (run_labs) matches each hypothesis claim: 0 arbitrage portfolios, state prices 1/20 and 17/20, 302 pairs and 0 violations; Part B 30 portfolios, zero-cost (-5,9) payoffs 22 and 4, state prices -1/5 and 11/10, 38 violations (" + S + "r6-twin-L01.out)."))
r("FC2a-lab-L02-claims", "lab hypothesis and interpretation claims", "L02.html lab-FC2-L02-1 hypothesis (line 121), interpretation (238); Example 2.4; Section 3", "PASS",
  carry("L02.html and tests/labs/FC2/lab-FC2-L02-1.py", "Printed output (" + S + "r6-twin-L02.out): 5126.58; replication equal in four outcomes; net 73.42 in every state; 0 date-0 cash legs; fair quote 0; value 237.11."))
r("FC2a-lab-L03-claims", "lab hypothesis and interpretation claims", "L03.html lab-FC2-L03-1 hypothesis (line 154), interpretation (277); Section 2; misconception 3 (line 305-306)", "PASS",
  "Re-verified: printed output (" + S + "r6-twin-L03.out): identities True; 4 loss days; balance 84; par 0.049026 (4.9026 percent, equals none of the five zero rates); payment 4902625 cents; value -4415468. Hypothesis (line 154) and interpretation (277) lines are unchanged in the delta and match the output. Misconception 3 (line 306), which changed, now states the fact of these inputs and the flat-curve case (Example 3.4), matching the output.")
r("FC2a-grades", "grades: key-results tables, card grades", "L01.html:430-435; L02.html:411-417; L03.html:422-427; cards.json L01-L03 grade fields", "PASS",
  "Re-verified: L03 key-results rows (lines 422-427) unchanged, all T with a source; L03 cards c046 and c050 remain grade C with lab/convention basis (cards.json lines 290-325); c046 and c050 grade fields unchanged; other grade fields carried from round 5 (L01/L02 cards unchanged).")
r("FC2a-notation", "notation registry conflicts", "L01-L03, index.html, cards.json for slice a", "PASS",
  "Re-checked: notation/notation.json (symbols include T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q). grep for Phi, gamma, R^*, R_f, Q in L01-L03 returns none. L03 delta adds no new symbol (R_par, DF_i, A8' and Example 3.4 already used).")
r("FC2a-dag-closure", "DAG: concepts used outside the prerequisite closure", "index.html, L01-L03", "PASS",
  "check_dag FC2 PASS this round (" + GATES + "). The data-concept multiset of L03.html is identical to dde0486b (5 links; diff of sorted lists empty). L01/L02 concept links unchanged (byte-identical pages).")
r("FC2a-data", "data status and sources", "index.html #data (157-159); L01-L03 labs", "PASS",
  "Re-checked: grep 'data-files|data/' in L01.html, L02.html, L03.html returns 0. L03 lab Part A labelled SIMULATED (L03.html:154-157; twin docstring lines 157-158). index.html:159 unchanged and consistent.")
r("FC2a-L02-why-only-price", "why-it-matters claim vs Proposition 2.2", "L02.html:51", "PASS",
  carry("L02.html", "'Under stated conditions, a forward price other than the cost-of-carry price admits an arbitrage.' supported by Prop 2.2 Cases 1-2 (L02.html:98-100)."))
r("FC2a-cards-accuracy", "cards agree with current lesson text", "cards.json FC2-c050 (lines 321-325)", "PASS",
  "Re-verified: c050 front 'Is the par rate of a swap the market's interest rate?' back now 'Not in general. Under A8, R_par is the ratio of Proposition 3.3 ... On a flat curve it equals the flat rate (Example 3.4). In Lab 3, Part B, it is 4.9026 percent, which equals none of the five typed-in zero rates.' Each clause matches L03.html:121-124 (Prop 3.3), :134 (Example 3.4), :154 and :306 (printed 4.9026, none of the zero rates). The counterexample supports 'not in general'. Residual note, not a FAIL: the lesson never defines 'the market's interest rate' and says at L03.html:277 that the typed-in rates are not stated to be market rates.")
r("FC2a-cards-coverage", "card coverage of L01-L03", "cards.json (61 cards for L01-L03)", "PASS",
  "Re-counted this round: L01 18, L02 23, L03 20 (total 61); 172 ids, all unique (python check). Card cross-references re-listed (python): every L03 cited item (Definition 1.1-1.2, A8', Prop 1.3, Remarks 1.4-1.5, Section 2 and 4, Def 3.1, Prop 3.2, 3.3, 3.5, Example 3.4, Problems P2, P3, Lab 3 Part B) exists in L03.html.")
r("FC2a-cards-trivia", "cards test understanding, not trivia", "cards.json FC2-c021, c046", "PASS",
  "c021 unchanged (Example 2.4 computed value with basis). c046 (changed) still asks a computed value with its basis (-4415468 cents = -h sum DF_i, Problem P2; Lab 3 Part B). No restated-label-only card.")
r("FC2a-cards-hypotheses", "cards carry the hypotheses of the proposition they cite", "cards.json FC2-c046 (lines 290-294)", "PASS",
  "Re-verified: c046 front now begins 'Under A8, on the 1,000,000-dollar notional of Lab 3, Part B, ...'. Problem P2 uses Proposition 3.5, which says 'Assume A8' (L03.html:138); the par rate is defined under A8 (L03.html:121). Matches the round-5 requested fix; sibling c044 states A8 too.")
r("FC2a-L01-assumption-first-use", "assumption first-use claims", "L01.html:65-66 (A3 block), :75", "PASS",
  carry("L01.html", "A3 block says it is used alone; first use is Proposition 2.1 (L01.html:75); A1 and A2 defined in L02 Section 1 and first used in Proposition 2.2 (L02.html:93), as stated at L01.html:66."))
r("FC2a-lab-hypothesis-SIMULATED", "SIMULATED labelling", "L03.html lab-FC2-L03-1 (lines 154-158); index.html #data", "PASS",
  carry("L03.html:154-158, index.html, L01.html, L02.html, lab twins", "Part A labelled SIMULATED in hypothesis, twin docstring and output header; no FC2 lab reads market data (grep: data-files 0)."))
r("FC2a-r3-ex34-hypothesis", "Example 3.4 hypotheses", "L03.html:134; cards FC2-c043 (line 276)", "PASS",
  carry("L03.html:134 and cards.json FC2-c043", "Example 3.4 begins 'Assume A8'; rho > -1; rho = 0 handled; c043 front says 'Under A8'."))
r("FC2a-r3-prop32-title", "Proposition 3.2 title and hypothesis", "L03.html:109-110", "PASS",
  carry("L03.html lines 109-110", "'Proposition 3.2 (value of the floating leg)', 'Assume A8'."))
r("FC2a-r3-card-c037-remark14", "card c037 vs Remark 1.4 and Section 4", "cards.json FC2-c037 (lines 245-249); L03.html:82, :286", "PASS",
  carry("cards.json FC2-c037, L03.html:82 and :286", "Back cites Remark 1.4 and Section 4; both say margin requirements are not modelled."))
r("FC2a-r3-L02-sec1-forward-ref", "forward references in L02 Section 1", "L02.html:70-71 (A2), :79-82 (A4)", "PASS",
  carry("L02.html", "A2 refers to A4, defined at L02.html:79-82."))
r("FC2a-r3-L03-def31-forward-ref", "forward reference from Definition 3.1 to A8", "L03.html:100, :104-105", "PASS",
  carry("L03.html lines 100-105", "Definition 3.1 says the floating coupon is set 'by the relation of Assumption A8 below'; A8 at L03.html:104-105."))
r("FC2a-r4-L03-positivity-sentence", "A8 sentence on which hypothesis each proposition uses", "L03.html:105 (A8 block); proofs at :115, :129, :144", "PASS",
  carry("L03.html lines 105, 115, 129, 144", "Non-vanishing used in Prop 3.2; positivity in Props 3.3 and 3.5; n=2 counterexample gives 0 = 3/2 (re-derived: DF_1=1/2, DF_2=-1/2 sum 0, 1-DF_2=3/2)."))
r("FC2a-r4-card-c007-scope", "card c007 scope words", "cards.json FC2-c007 (lines 43-46)", "PASS",
  carry("cards.json FC2-c007", "Answer 'No. Proposition 3.2 runs one way; the lesson does not prove the converse (Remark 3.3).' matches L01.html:123-124."))
r("FC2a-r4-card-c025-c172-overlap", "duplicate cards", "cards.json FC2-c025 (line 164) and FC2-c172 (line 1131)", "PASS",
  carry("cards.json FC2-c025 and FC2-c172", "Distinct questions (V_t of a long forward vs spot S_t at which value is zero)."))
r("FC2a-r4-hub-six-contract", "hub rung text vs project page", "index.html:150; project.html:44, :55", "PASS",
  carry("index.html:150 and project.html lines 44 and 55", "'six-strike SIMULATED chain' matches project.html:44 and :55; project.html changed only at line 519."))
r("FC2a-r4-L02-lab-floats", "lab docstring vs printed values (float vs integer cents)", "tests/labs/FC2/lab-FC2-L02-1.py docstring; L02.html:238", "PASS",
  carry("tests/labs/FC2/lab-FC2-L02-1.py and L02.html", "Docstring states typed-in prices are integer cents and formula prices are floating-point values in cents; page code == twin (this round)."))
r("FC2a-r4-proposition-numbering", "Proposition numbering across lessons", "L01.html and L02.html Proposition 2.2; cards c005, c015, c019, c154", "PASS",
  carry("cards.json FC2-c005, c015, c019, c154; L01.html; L02.html", "Cross-lesson references qualified (L02.html:243 'Proposition 2.1 of Lesson 1'; L01.html:66 'Lesson 2, Section 1')."))
r("FC2a-r4-card-c027-hypothesis", "card c027 carries Proposition 3.1 hypotheses", "cards.json FC2-c027 (line 178)", "PASS",
  carry("cards.json FC2-c027", "Front 'Under A1 to A4 and A3 at each date', the hypothesis of Proposition 3.1 (L02.html:247)."))
r("FC2a-r5-delta-hunks", "delta read hunk by hunk (dde0486b..e896b7a4) for slice a", "course/modules/FC/FC2/L03.html (9 hunks: 51, 298, 306, 318, 328, 385, 463, 506, 509); course/modules/FC/FC2/cards.json FC2-c046, FC2-c050", "PASS",
  "git diff -U0 dde0486b HEAD: L03.html hunks read in full (lines 51, 298, 306, 318, 328, 385, 463, 506, 509), each re-verified above. cards.json slice-a changes are c046 and c050 only (python diff of id-keyed objects). Other cards changed or removed (c059, c060, c081, c082, c176; added c184, c185) belong to L04-L06 and were not judged. index.html, L01.html, L02.html, tests/labs/FC2/lab-FC2-L01-1.py, lab-FC2-L02-1.py, lab-FC2-L03-1.py are byte-identical to dde0486b (git diff --quiet). project.html changed at line 519 only (not cited by slice a).")
r("FC2a-r5-rederive", "independent re-derivation of every printed number in the L01-L03 labs and prose", S + "r6-rederive.py", "PASS",
  "`python3 -I " + S + "r6-rederive.py` -> " + S + "r6-rederive.out reproduces the L03 values (84, 4 loss days, 4.9026 percent, 4902625, -4415468, 2.6730119, 2.67, 3.9756 percent, 0.0267301, flat-curve identity). L01/L02 values carried from round 5 (rederive.out in " + "ledgers/FC2/scripts/FC2-a-r5/" + ") since those pages are byte-identical.")
r("FC2a-r5-build-site", "generated site data current", "course/assets/data/program.json; course/index.html; course/concepts.html", "PASS",
  "`tools/build_site.py --check` -> 'site data current: 6 outputs', rc=0 (" + GATES + ").")
r("FC2a-r5-L03-quiz-q10", "retrieval quiz item Q10 and explanation", "L03.html:503-509", "PASS",
  "Re-verified, the subject changed. Q10 correct option (L03.html:506) now: 'Because the value that Proposition 3.3 gives from all five discount factors is 4.9026 percent, which differs from each of the five typed-in zero rates' (true: printed 0.049026, Lab 3 Part B). Distractors wrong ('lab rounds the zero rates': inputs are exact Fractions in the twin; 'day count is 360': Remark 3.6 says no day count is used). Explanation (L03.html:509) matches the page and Example 3.4. Residual note, not a FAIL: the marked reason restates the fact that the value differs from each rate; it gives no mechanism.")

import datetime
prev = json.load(open("/Users/billyribeiro/.fanout/frags/S-FC2-a.round5.json"))
prev_ids = [x["id"] for x in prev["rows"]]
assert sorted(prev_ids) == sorted(x["id"] for x in rows), (set(prev_ids) ^ set(x["id"] for x in rows))
assert len({x["id"] for x in rows}) == len(rows)
status = [x["status"] for x in rows]
verdict = "PASS" if all(s_ == "PASS" for s_ in status) else "FAIL"
frag = {
  "unit": "FC2",
  "slice": "a",
  "round": 6,
  "verifier": "Haiku independent verifier, FC2-a round 6 (delta verification; did not build FC2; re-verified every round-5 non-PASS row and every row whose subject changed)",
  "pin": "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a",
  "base": "dde0486beeb0312e4ac1cc03aaa02e56644adb24 (round-5 pin, per ~/.fanout/frags/S-FC2-a.round5.json)",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyS6-FC2-a (detached at e896b7a4, .venv symlinked)",
  "scratch": "/Users/billyribeiro/.fanout/wt/verifyS6-FC2-a/ledgers/FC2/scripts/FC2-a-r6",
  "verified_at": "2026-11-09T11:54:01Z",
  "verdict": verdict,
  "rows": rows,
  "mutants": [],
  "registry_flags": [],
  "freshness_flags": [
    "ledgers/FC2/FC2-a.json as committed at 9fd6aed (an earlier round-6 fragment, verdict PASS, 40 rows) predates dde0486b and is superseded by this fragment; it was overwritten in the verifier checkout only and not committed."
  ],
  "notes": [
    "Delta scope: git diff dde0486b..e896b7a4 touches slice a only in course/modules/FC/FC2/L03.html (9 one-line hunks, line count unchanged) and course/modules/FC/FC2/cards.json (FC2-c046 front, FC2-c050 back). index.html, L01.html, L02.html and the three slice-a twins are byte-identical to dde0486b (git diff --quiet).",
    "Round-5 FAIL rows re-verified and now PASS: FC2a-L03-problems (E3 solution), FC2a-r5-L03-quiz-q10 (Q10 option and explanation), FC2a-cards-accuracy (c050), FC2a-cards-hypotheses (c046 now states Under A8).",
    "Residual observations, not findings under the rules: (1) E3 'say why' and Q10 are answered with a fact of the printed value (the par rate differs from each typed-in rate), not with a mechanism; the lesson proves no general mechanism (R2 is n=2 only). (2) c050 asks about 'the market's interest rate', a phrase the lesson never defines; L03.html:277 says the typed-in rates are not stated to be market rates. (3) Twin docstring L03 line 162 reads 'fractions.Fraction values' (stray module reference; cosmetic). Twins are demonstrations, so no mutant or grader ruling applies.",
    "No project grader in slice a: no student-error mutants built; the ruling on lab twins applies.",
    "Ran (round 6, pin e896b7a4): check_pages, check_dag, check_projects, run_labs (unit and per page), twins alone under python -I -W error, page_smoke (four pages), ruff check and format on the twins, mypy --no-incremental on the twins, pytest on test_labs, test_run_labs, test_page_checks, test_curriculum, test_docs_figures, verify_refs --offline, build_site --check; plus scripts r6-anchors.py, r6-twin-vs-page.py, r6-rederive.py.",
    "Not run: full gate (ruff and mypy on the whole repo, the full pytest suite, render_curriculum, verify_refs live); run_graders and mutate_graders (not a project slice); a browser screenshot of L03 (page_smoke only). render_curriculum was not run because no curriculum source changed in the delta.",
    "Hours are design targets; arithmetic consistency checked (60 lesson hours = sum of L01-L08 data-hours; 60/90 = 66.7%)."
  ],
  "summary": {"rows": len(rows), "pass": status.count("PASS"), "fail": status.count("FAIL"), "unverifiable": status.count("UNVERIFIABLE")},
}
json.dump(frag, open("ledgers/FC2/FC2-a.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("rows", len(rows), "verdict", verdict, frag["summary"])
