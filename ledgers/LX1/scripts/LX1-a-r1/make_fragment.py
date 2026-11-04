"""LX1-a round 1: writes ledgers/LX1/LX1-a.json from the rows verified in this round (evidence cites out/ files)."""
import json
import pathlib

P = "PASS"
F = "FAIL"
S = "ledgers/LX1/scripts/LX1-a-r1/out/"
rows = []

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)

# ---- command rows (run by this verifier at the pin)
row("LX1a-cmd-check_pages", "tools/check_pages.py --unit LX1", "course/modules/LX/LX1/index.html, L01.html, L02.html", P,
    f"Run at 1c1645f3: exit 0, output 'check_pages LX1: PASS' ({S}check_pages.txt; command in ledgers/LX1/scripts/LX1-a-r1/run_cmds.sh).")
row("LX1a-cmd-check_dag", "tools/check_dag.py --unit LX1", "unit DAG (hub, L01, L02)", P,
    f"Run at 1c1645f3: exit 0, 'check_dag LX1: PASS' ({S}check_dag.txt).")
row("LX1a-cmd-check_projects", "tools/check_projects.py --unit LX1", "project.html (not in this slice; command row only)", P,
    f"Run at 1c1645f3: exit 0, 'check_projects LX1: PASS' ({S}check_projects.txt).")
row("LX1a-cmd-run_labs", "tools/run_labs.py --unit LX1", "tests/labs/LX1 (7 twins; slice owns 2)", P,
    f"Run at 1c1645f3: 'run_labs LX1: PASS (7/7)' ({S}run_labs_unit.txt).")
row("LX1a-cmd-twins-isolated", "python -I -W error on each slice twin", "tests/labs/LX1/lab-LX1-L01-1.py, lab-LX1-L02-1.py", P,
    f"Run by ledgers/LX1/scripts/LX1-a-r1/lab_check.py: both twins exit 0 with empty stderr; output in {S}lab_check.txt.")
row("LX1a-cmd-page_smoke", "tools/page_smoke.py --unit LX1 --pages index L01 L02", "index.html, L01.html, L02.html", P,
    f"Run at 1c1645f3: 'page_smoke modules/LX/LX1/index.html: PASS', '...L01.html: PASS', '...L02.html: PASS'; lab timings 0.0 s (under 10 s); 'page_smoke LX1: PASS' ({S}page_smoke_index_L01_L02.txt).")
row("LX1a-cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental on tests/labs/LX1", "tests/labs/LX1", P,
    f"ruff check: 'All checks passed!'; ruff format --check: '7 files already formatted'; mypy: 'Success: no issues found in 7 source files' ({S}ruff_labs.txt, {S}ruff_format_labs.txt, {S}mypy_labs.txt).")
row("LX1a-cmd-pytest", "pytest tests/test_labs.py tests/test_page_checks.py tests/test_run_labs.py tests/labs/LX1", "tooling tests for labs and page checks", P,
    f"Run at 1c1645f3: exit 0, all dots, no failures ({S}pytest_relevant.txt).")
row("LX1a-cmd-verify_refs-live", "tools/verify_refs.py --unit LX1 (live)", "references/references.json: friedman1963monetary, eichengreen1992golden, garber2000famous", P,
    f"Run at 1c1645f3: 'live re-verification of LX1: 3 of 560 entries, 0 problems' ({S}verify_refs_live.txt). reinhart2009this has used_by E9, so the unit run does not include it (see registry_flags).")
row("LX1a-cmd-verify_refs-offline", "tools/verify_refs.py --offline (whole registry)", "references/references.json", P,
    f"Run at 1c1645f3: 'offline integrity: 560 entries, 0 problems' ({S}verify_refs_offline_full.txt).")
row("LX1a-cmd-fetch_data-check", "tools/fetch_data.py --check", "course/assets/data/market/MANIFEST.json, fx_monthly.csv", P,
    f"Run at 1c1645f3: 'fetch_data: 3 datasets, 0 problems' ({S}fetch_data_check.txt). The rebuild of the fx_monthly sha256 from a live fetch was not run in this slice (L04 slice owner).")

# ---- labs
row("LX1a-lab-L01-1", "2.5 lab: lab-LX1-L01-1 (SIMULATED fundamental, finite sum, gap)", "L01.html lines 126-279; tests/labs/LX1/lab-LX1-L01-1.py", P,
    f"Twin exit 0 under -I -W error; page code equals twin (lab_check.txt: page_code_equals_twin=True); expected block equals twin output (expected_equals_output=True). Heading says SIMULATED; RNG seeded (SEED 20261103); no network or data file. Hypothesis sentences (F_0 = 20000/3 -> 6667; q = 103/109; S_N identity for N=10,60,200; 200-term sum rounds to 6667; Part C count changes) match the printed lines. Every printed value recomputed independently with Fraction and Decimal in ledgers/LX1/scripts/LX1-a-r1/l01_numbers.py ({S}l01_numbers.txt).")
row("LX1a-lab-L02-1", "2.5 lab: lab-LX1-L02-1 (SIMULATED real value of fixed nominal debt)", "L02.html lines 133-279; tests/labs/LX1/lab-LX1-L02-1.py", P,
    f"Twin exit 0 under -I -W error; page code equals twin; expected block equals output (lab_check.txt). Heading says SIMULATED; SEED 20261104; illustrative debt 1,000,000 cents = 10,000.00 CU; no data file read. Every V_t, the six falling and six rising periods, the largest step 42236 cents at t=12, P_12 = 94.70509914..., and 100/P_12 = 1.05590935... recomputed independently (ledgers/LX1/scripts/LX1-a-r1/l02_numbers.py; {S}l02_numbers.txt). Hypothesis and interpretation sentences match the output.")

# ---- numbers in prose (one row per number group)
row("LX1a-num-L01-closed-form-sums", "2.2 numbers: Theorem 1.3 closed form and Lab 1 Part A", "L01.html lines 73-74, 128, 240-245, 278", P,
    f"F_0 = 20000/3 = 6666.67 cents, rounds to 6667; q = 103/109; N=10 sum 2882, F_0 q^10 = 3784.57 rounds to 3785; N=60 sum 6444, residual 223; N=200 sum 6667, residual 0. Recomputed (l01_numbers.txt).")
row("LX1a-num-L01-prop22-witness", "2.2 numbers: Proposition 2.2 witness and misconception 1", "L01.html lines 116, 317, 459", P,
    "d_1=400, r=9%: F_0(1%)=5000, F_0(3%)=20000/3=6666.67; gap at P_0=6000 is +1000 under 1% and -2000/3 under 3%. Recomputed (l01_numbers.txt).")
row("LX1a-num-L01-canon-breaks-367", "2.2 numbers: single-dividend stream", "L01.html lines 306, 318", P,
    "400/1.09 = 40000/109 = 366.97, rounds to 367; closed form at g=3% is 6666.67, rounds to 6667. Recomputed (l01_numbers.txt).")
row("LX1a-num-L01-lab-counts", "2.2 numbers: 9 of 13 and 13 of 13 gap periods; differences", "L01.html lines 278, 358-363, 396", P,
    "Lab 1 Part B prints 9 of 13 above fundamental and Part C prints 13 of 13; 13-9 = 4. Matches expected block lines 260 and 276 of L01.html.")
row("LX1a-num-L01-empirical-shares", "2.2 numbers: 9/13 = 0.6923, 2175/8698 = 25.01%, 2.33%", "L01.html lines 358-359, 366-367, 374", P,
    "9/13 = 0.692307... to four places 0.6923; 2175/8698 = 0.25005748... so 0.250057 to six places and 25.01 percent to two places; threshold g* = 0.09 - 400/6000 = 7/300 = 0.023333, 2.33 percent. Recomputed (l01_numbers.txt). The base stated for the percentage (fundamental at t=9, rounded to 8698) matches Lab 1 Part B.")
row("LX1a-num-L01-mechanics", "2.2 numbers: Mechanics 1-3 solutions", "L01.html lines 329-337", P,
    "250/0.06 = 12500/3 = 4166.67 rounds to 4167; 1.04^3 = 1.124864; 250*1.124864/0.06 = 4686.93 rounds to 4687; 100/1.05 = 2000/21 per term; S_10 = 20000/21 = 952.38. Recomputed (l01_numbers.txt).")
row("LX1a-num-L01-quiz-numeric", "2.2 numbers: L01 retrieval quiz numeric items", "L01.html lines 414-432", P,
    "F_0 6666.67 (tolerance 0.01); F_2 = 7072.67 rounds to 7073 (lab t=2 prints 7073); q 0.944954; g* 0.023333. All match recomputation within stated tolerance (l01_numbers.txt).")
row("LX1a-num-L02-real-values", "2.2 numbers: Lab 1 real values and hand computations", "L02.html lines 255-277, 318-334, 375-383, 452-460, 485-488", P,
    "V_1 = 1010101 (1000000*100/99 = 1010101.0101); M1 V_1 = 2500; M2 V_2/V_1 = 18/17; M3 2000*100/95 = 2105.2631 rounds to 2105; E3 100/94.7051 = 1.0559093 and 100/94.70509914 = 1.05590935, both 1.055909 to six places; quiz 1.25, 1010101, 18/17 = 1.0588235294. All recomputed (l02_numbers.txt).")
row("LX1a-num-L02-counts", "2.2 numbers: falling and rising periods and largest step", "L02.html lines 270-273, 297, 370, 474", P,
    "Changes -1,+1,+1,+3,-4,-1,+2,-4,-3,+3,+2,-4: falls at t=1,5,6,8,9,12 (six) and rises at the same six periods; largest step 42236 at t=12; all twelve changes non-zero. Recomputed (l02_numbers.txt).")
row("LX1a-num-hub-placement", "2.2 numbers: placement diagnostic answers and arithmetic", "index.html lines 75-151", P,
    "Ten items; prerequisite split 1 P0.1, 1 E1, 2 M1, 1 M2, 2 E5, 1 FC1 plus 2 skill checks; answers 1000 (perpetuity 100/0.10), 0.1 (110/100-1), 100 (10050-9950), 800 (1000/1.25), discount factor and ln derivative as printed. 8 of 10 = 80 percent; 7 of 10 = 70 percent.")
row("LX1a-num-hub-hours", "2.9 hours arithmetic", "index.html lines 29, 40-43, 182-197", P,
    "data-hours-lessons=40 = 4 x 10 (L01 and L02 data-hours=10 confirmed; L03/L04 not in slice); data-hours-project=10; 40+10=50 = curriculum hours (curriculum.json LX1 hours 50); 10/50 = 20 percent; hours table 1+1+2+1.5+2.5+2 = 10.")

# ---- mathematics
row("LX1a-math-L01-thm1.3", "2.4 math: Theorem 1.3 closed form and partial-sum identity", "L01.html lines 70-85", P,
    "Re-derived: sum_{k>=1} d_1(1+g)^{t+k-1}/(1+r)^k = d_1(1+g)^t/(r-g) under (A0); 1-q=(r-g)/(1+r) > 0; S_N(t)=F_t(1-q^N) exact; checked by Fraction identity in Lab 1 Part A ({S}l01_numbers.txt). Assumptions (A0),(A1) listed.")
row("LX1a-math-L01-prop1.4", "2.4 math: Proposition 1.4 divergence when g >= r", "L01.html lines 89-97", P,
    "q >= 1 since 1+g >= 1+r > 0; each term d_1 q^{k-1}/(1+r) >= d_1/(1+r) > 0; S_N >= N d_1/(1+r) -> infinity. Hypotheses (A1) d_1>0, 1+g>0 and (A2) r>-1, g>=r are listed inline. Proof complete.")
row("LX1a-math-L01-prop2.2", "2.4 math: Proposition 2.2 monotonicity of the benchmark in growth", "L01.html lines 108-117", P,
    "Proof correct: r-g > r-g' > 0 when g<g', reciprocal reversal, multiplication by d_1>0. Witness recomputed. Proposition is T (exact statement about the benchmark). Numbering of its hypotheses is a separate row.")
row("LX1a-math-L01-problems", "2.4 math: L01 problem set solutions (Proof 1-3, Research 1-3)", "L01.html lines 341-383", P,
    "Each solution re-derived: strict monotonicity of d_1/(r-g) in g; benchmark recursion F_t=(1+g)F_{t-1}; term ratio q^{k-1} with q>1 when g>r; growth threshold g*=2.33 percent; the three bubble-claim inputs. No error found in the algebra.")
row("LX1a-math-L02-prop1.2", "2.4 math: Proposition 1.2 gold price 1/kappa", "L02.html lines 62-73", P,
    "Under (A1) kappa grams cost one unit so one gram costs 1/kappa; proof uses (A1) at every date. Correct as stated.")
row("LX1a-math-L02-prop2.1-cor3.2", "2.4 math: Proposition 2.1 real-value identity, Corollary 3.2", "L02.html lines 86-124", P,
    "V_t/V_{t-1} = P_{t-1}/P_t by cancellation of D P_0 (A2 positive integer D, A3 positive P_t); telescoping for (b) correct; V_t > V_{t-1} iff P_t < P_{t-1} because V_{t-1} > 0 and P_t > 0. Verified exactly in Lab 1 Parts B-D.")
row("LX1a-math-L02-problems", "2.4 math: L02 problem set solutions (M1-M3, P1-P3, E1-E3, R1-R3)", "L02.html lines 316-412", P,
    "Each worked solution re-derived. M1 2500, M2 18/17, M3 2105, P1 monotone implication, P2 induction, P3 rescaling invariance, E1 six negative changes, E2 1010101, E3 1.055909, R1 finite-check argument, R2 real value D constant under index-linked payment, R3 two indices. No algebra error found. Notation issue on T is a separate row.")

# ---- notation
row("LX1a-notation-L01", "2.4 notation vs notation/notation.json", "L01.html (all math), index.html", P,
    "Registered symbols (notation.json symbols: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) do not appear in L01 or the hub. Local symbols d, g, r, F, B, P, q, S_N (N, S are local per notation.json 'about'), k, j, s, t are defined on first use. No registered macro is used; \\ast appears only as F^\\ast, a different symbol from R^\\ast.")
row("LX1a-notation-L02-T", "2.3 notation: symbol T", "L02.html lines 92, 98, 350-352 (P2, Prop 2.1(b)), key-results table line 422", F,
    "L02 uses T as a time horizon: 'for every T >= 1, V_T/V_0 = P_0/P_T' (Prop 2.1(b)), 'Suppose V_T / V_0 = P_0 / P_T' in P2, and P_T, V_T in the key-results row. notation.json symbols[0] registers T as 'number of return observations (periods) in a sample' (module S1), and plans/LX1-build-plan.md section 2.3 says T is not used and a horizon is H.",
    "Rename the horizon T to H everywhere in L02.html (Proposition 2.1(b) statement and proof, Problem P2, the key-results row, and any P_T or V_T subscripts). The lab twin already uses HORIZON and needs no change; re-run check_pages after the edit.")
row("LX1a-notation-hub", "2.3 notation: hub symbols", "index.html lines 50-151", P,
    "Hub uses only D, P_t, r, k, x as local symbols in the placement items and no registered symbol.")

# ---- DAG and concepts
row("LX1a-dag-links", "2.9 DAG: concept links and anchors", "index.html; L01.html; L02.html", P,
    "Every data-concept/anchor in the slice resolves to a curriculum concept whose owner is in the closure {E1, E5, FC1, M1, M2, P0.1} or LX1 (concept_owner_check.txt): derivative M2, comparative-statics E1, price-index-inflation E5, national-accounts E5, business-cycle E5, growing-perpetuity/present-value/geometric-series/exponential-and-logarithm M1, evidence-grade and project-ladder P0.1. Anchors resolve in course/concepts.html. check_dag PASS.")
row("LX1a-dag-outside-closure", "2.9 DAG: outside-closure concept names used by name without link", "index.html, L01.html, L02.html", P,
    "Grep over the three pages for the D1-D15 names (bank run, fire sale, leverage, banking crisis, currency crisis, covered/uncovered interest parity, efficient markets, moral hazard, Fisher, bank reserves, central bank, credit default, contagion, term spread, expectation, exchange rate, sovereign, deposit insurance, bailout): zero hits. 'lender of last resort' and 'credit channel' appear only in the hub overview, as LX1 concepts.")
row("LX1a-dag-defined-once", "2.9 DAG: each LX1 concept defined once in its lesson", "L01.html def-speculative-bubble, def-financial-panic; L02.html def-gold-standard, def-debt-deflation", P,
    "Each data-concept dfn appears once in the slice, in the assigned lesson (plan section 1 order: speculative-bubble, financial-panic in L01; gold-standard, debt-deflation in L02). Plain dfn for parity, convertibility, nominal debt, real value, fundamental value (no data-concept). The hub introduces the two L02 concepts by forward link to #def in L02, stated as such.")

# ---- structure and prose
row("LX1a-struct-hub", "2.9 structure: hub sections (BUILDER_RULES 4.1)", "index.html", P,
    "Objectives (six, measurable verbs), prerequisites with links, placement diagnostic (10 items, mastery 0.8), lesson map (four cards; the L01 and L02 card titles match their h1, L03 and L04 titles not checked), project ladder (four rungs), data status, hours table, core reading. Hours split 40/10 and percentage 20 percent.")
row("LX1a-struct-L01-L02", "2.9 structure: lesson sections (BUILDER_RULES 4.2) and counts", "L01.html; L02.html", P,
    "Order: why-it-matters (109 and 98 words, at most 120), numbered core sections, inline lab, where the canon breaks, misconceptions (3 each), problem set (3 problems in each of the four tiers, all with details.solution), key-results table, retrieval quiz (10 items each, explanations present), references. No debate brief (LX1 has no debate key).")
row("LX1a-prose-banned", "2.9 banned phrases (BUILDER_RULES 1.3-1.4; check_pages BANNED list)", "index.html, L01.html, L02.html", P,
    "Scan (ledgers/LX1/scripts/LX1-a-r1/prose_scan.py, out/prose_scan.txt): no TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, or ellipsis outside code.")
row("LX1a-prose-process-words", "2.9 process words in learner text", "index.html, L01.html, L02.html", P,
    "Scan for build, builder, verify, round (as a process word), REQUEST, planner, fixer: no process use. The one hit of 'round' (L01 lab hypothesis: 'should round to 6667 cents') is the arithmetic verb.")
row("LX1a-claim-E5-prop1.7", "2.1 attribution: E5 Proposition 1.7 cited in placement item 7", "index.html line 130 (explain text) vs course/modules/E/E5/L01.html line 93-96", P,
    "E5 L01.html Proposition 1.7 (closed-economy saving equals investment): under (A0) and (A1) closed economy, S_p + S_g = I. Hub explain text ('private plus public saving equals investment in a closed economy') matches.")
row("LX1a-claim-registry-records", "2.1 attribution: registry records for the keys cited in the slice", "index.html reading list; L01.html line 299, 485; L02.html line 515; references/references.json entries", P,
    "friedman1963monetary: 'A monetary history of the United States 1867-1960', first author Friedman, 1963, status verified; the hub types Friedman only and does not type Schwartz (plan N2). eichengreen1992golden: 'Golden fetters: the gold standard and the Great Depression, 1919-1939', 1992, verified; L02 title string matches exactly. garber2000famous: 'Famous First Bubbles: The Fundamentals of Early Manias', 2000, DOI 10.7551/mitpress/2958.001.0001, verified; L01 cites title only. reinhart2009this: title and 2009 match the hub's optional reading entry.")
row("LX1a-claim-attribution-readings", "2.1 attribution: no passage attributed to an unread work", "L01.html line 299, 310, 485; L02.html line 513-515; index.html line 201", F,
    "Pages say no passage is read (L01 line 299 and 485; L02 line 513-515). L01 line 310 says 'The unit's reading list supplies the historical and empirical debate'. No work on the reading list has been read for this unit (the pages say so), so the sentence attributes content to unread works.",
    "Replace the sentence in L01.html line 310 with: 'The reading list names the sources for that debate. This lesson has not read them, and it does not settle the debate.'")
row("LX1a-claim-fed-licence", "2.8 data: fx_monthly licence and licence_url", "index.html line 178; tools/data_sources.yaml lines 57-64; MANIFEST fx_monthly", P,
    f"Plain curl of https://www.federalreserve.gov/disclaimer.htm: HTTP 200, 85306 bytes; the sentence 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission' is on the page (archived at {S}disclaimer.htm). Hub quotation matches the registry licence text. The grant permits copying and redistribution.")
row("LX1a-claim-fx-note-blanks", "2.8 data: fx_monthly note, euro start, GBP column blanks", "index.html line 178-179; tools/data_sources.yaml lines 62-64; course/assets/data/market/fx_monthly.csv", P,
    "Note: 'Each value is the last noon rate of its month ... The euro starts in January 1999. Spot rates only.' Hub matches. CSV: 669 data rows; EUR first non-blank 1999-01 with 336 blanks; GBP 0 blanks, so the hub's 'Lesson 4 uses a column with no blank cells' holds for GBP (the column L04 reads, tests/labs/LX1/lab-LX1-L04-1.py line 42).")
row("LX1a-claim-P0.1-not-released", "2.9 claims: P0.1 'not yet released' links", "index.html lines 35, 61, 68; course/concepts.html anchors", P,
    "course/concepts.html lists 'Evidence grade (T/A/B/C/D/X) · not yet released' and 'Four-rung project ladder · not yet released', the anchors the hub links to. Hub wording matches.")
row("LX1a-claim-simulated-labels", "2.5 labels: SIMULATED on generated-number labs and figures", "L01.html line 127, L02.html line 134, index.html lines 37, 171, 178-179", P,
    "Both slice labs carry SIMULATED in their headings and their prose; the hub states which labs are SIMULATED. The hub sentence 'Every other lab runs on SIMULATED numbers' is a separate FAIL row (project-3 reads real data).")
row("LX1a-data-figures", "2.8 data and figures: one row per figure", "index.html, L01.html, L02.html", P,
    "No <svg>, <figure>, or data-chart in the three pages (grep count 0 each). No live figures or kernels, as plan section 12 item 13 decided. Nothing to check.")
row("LX1a-scope-words", "2.9 / rule 4 scope words: every, all, any, only, exactly, same, never, most, usual", "index.html, L01.html, L02.html", P,
    "Every scope word in the slice was read in context (ledgers/LX1/scripts/LX1-a-r1/out/scope_context.txt, from scope_context.py). Universal claims are backed by a derivation (for every t, every k, every path under A3), a finite lab check, or are stated as a hypothesis. The remaining scope words are PASS. The exceptions are separate FAIL rows: L01 line 51 ('usual first test', 'most claims'), L01 line 300 ('only quantitative tool'), hub line 33 ('historian or regulator').")

# ---- FAIL rows
row("LX1a-hub-fc1-title", "2.9 hub: prerequisite titles match the curriculum", "index.html line 35", F,
    "Hub reads 'FC1 Financial Markets and Instruments'. curriculum/curriculum.json (parts -> modules, id FC1) title is 'The Financial System, Markets & Instruments', and FC1's own h1 (course/modules/FC/FC1/index.html) says the same.",
    "Change the hub text to 'FC1 The Financial System, Markets & Instruments'.")
row("LX1a-hub-fx-one-lab", "2.9 hub: count of labs reading embedded data", "index.html lines 33, 37, 178-179", F,
    "Hub says one embedded series is used 'in one lab' (line 33), 'used in Lesson 4' (line 37), and 'Every other lab runs on SIMULATED numbers' (line 37). course/modules/LX/LX1/project.html has data-files=\"fx_monthly.csv\" and lab-LX1-project-3 (tests/labs/LX1/lab-LX1-project-3.py line 38, DATA_PATH data/fx_monthly.csv) reads it. So fx_monthly is read by L04 and by the project's rung-3 check, and two labs are not SIMULATED.",
    "Reword line 33 to 'in two labs' (or 'in Lesson 4 and the project's rung-3 check'), reword line 37 to name both uses, and replace 'Every other lab runs on SIMULATED numbers' with 'The labs of Lessons 1 to 3 and project rungs 1 and 2 run on SIMULATED numbers'. Make the same change to the Data status section (lines 178-179: 'read in Lesson 4' becomes 'read in Lesson 4 and in the project rung-3 check').")
row("LX1a-hub-derivative-claim", "2.9 hub: concept usage claim", "index.html line 66; L01.html", F,
    "Hub says 'From M2: the derivative, used for monotonicity in Lesson 1.' L01.html has no data-concept derivative link and no use of the derivative: monotonicity (Problem Proof 1) is shown by reciprocals, and L01's meta line lists no M2 concept (grep -i 'derivative' on L01.html returns no line; the only 'monoton' hit is a problem title).",
    "Delete the derivative bullet from the hub prerequisite list, or add a derivative link where L01 uses it (for example in Problem Proof 1).")
row("LX1a-hub-L03-concept-claim", "2.9 hub: concept usage claim for Lesson 3", "index.html line 64; L03.html (cross-slice read)", F,
    "Hub says national accounts and the business cycle are used 'in Lesson 3'. In L03.html 'national account' and 'business cycle' occur zero times and there is no data-concept for either (grep counts 0 and 0 on the page).",
    "Either add the E5 national-accounts and business-cycle links where L03 uses them (L03 builder), or remove those two concepts from the hub's E5 bullet.")
row("LX1a-hub-historian-regulator", "2.9 unsourced generalization", "index.html line 33", F,
    "Lede: 'Each topic is taught as a mechanism that a historian or a regulator would use to explain an episode.' This is a claim about how historians and regulators work, with no key, locator or computation.",
    "Delete 'that a historian or a regulator would use', so the sentence reads 'Each topic is taught as a mechanism for explaining an episode.'")
row("LX1a-L01-usual-first-test", "2.9 unsourced generalization (rule 4 and 3)", "L01.html line 51", F,
    "Why-it-matters: 'A price above a benchmark is the usual first test for a bubble, and most claims of a bubble depend on the choice of benchmark.' Both generalizations about the literature have no registry key, no locator and no computation.",
    "Replace with the lesson's own derived statement: 'A price above a benchmark is a gap only relative to that benchmark, and the sign of the gap depends on the benchmark chosen (Proposition 2.2).'")
row("LX1a-L01-gap-integer-cents", "2.4 definition: units of the gap", "L01.html line 105", F,
    "Definition 2.1 says the gap 'is measured in the currency unit of the dividends, here in integer cents'. The gap B_t = P_t - F_t is not integer-valued in general: F_0 = 20000/3 cents (Theorem 1.3, Lab 1 Part A). The lab rounds gaps to whole cents for display only.",
    "Replace 'here in integer cents' with 'in cents; Lab 1 reports it rounded to whole cents'.")
row("LX1a-L01-prop22-unnumbered-assumptions", "2.1 item 6: numbered assumptions before each Proposition", "L01.html lines 108-110", F,
    "Proposition 2.2 lists its hypotheses inline without numbers ('Assume d_1 > 0 ... each with the same discount rate r satisfying r > g, r > g', 1 + g > 0 and 1 + g' > 0'). plans/LX1-build-plan.md section 2.1 item 6 requires numbered Assumptions (A1, A2, ...) before the statement of every Proposition.",
    "Number the hypotheses inside the statement, for example (A1) d_1 > 0; (A2) r > g and r > g' with 1 + g > 0 and 1 + g' > 0; then state the conclusion.")
row("LX1a-L01-only-quantitative-tool", "2.4 scope: 'only' claim", "L01.html lines 299-300", F,
    "'The benchmark of Section 1 is the only quantitative tool in this lesson.' Section 2 computes gaps and Lab 1 computes sums, counts and gaps, so the scope word is contradicted by the lesson's own computations.",
    "Replace with: 'The benchmark of Section 1 is the quantitative object this lesson uses for bubbles.'")
row("LX1a-L02-prop12-no-lab-check", "3.4 BUILDER_RULES: numerical check per key formula", "L02.html lines 62-73, 421 (key-results row 1), lab-LX1-L02-1", F,
    "Proposition 1.2 (currency price of gold is 1/kappa) is a key result graded T, but no lab prints or checks 1/kappa: Lab 1 code (L02.html lines 136-239) computes only real values of the debt. BUILDER_RULES 3.4 requires a numerical check per key formula, and plans/LX1-build-plan.md section 2.1 names the lab as the check.",
    "Add a short printed check to lab-LX1-L02-1 (for example, a parity kappa and the printed price 1/kappa in Fractions), then run tools/embed_labs.py L02.html --refresh lab-LX1-L02-1 and cite the printed line in the Proposition 1.2 row.")
row("LX1a-L02-CU-undefined", "2.9 term defined before use", "L02.html line 135 and twin docstring line 140", F,
    "'10,000.00 CU' is used with no definition of CU anywhere on the page or in the twin.",
    "Write '10,000.00 currency units (CU)' at first use, or write 'currency units' in full.")

verdict = "PASS" if all(r["status"] == P for r in rows) else "FAIL"
counts = {"rows": len(rows), "pass": sum(r["status"] == P for r in rows), "fail": sum(r["status"] == F for r in rows),
          "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows)}
fragment = {
    "unit": "LX1",
    "slice": "LX1-a",
    "round": 1,
    "verifier": "Haiku independent verifier, LX1 slice a, round 1 (did not build LX1)",
    "pin": "1c1645f3",
    "base": "none (first independent verification of this slice)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE1-LX1-a (detached at 1c1645f3, .venv symlinked)",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE1-LX1-a/ledgers/LX1/scripts/LX1-a-r1/out",
    "verified_at": "2026-11-03",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "friedman1963monetary: registry record lists Friedman as the only author (plan N2); the slice cites the key only and does not type Schwartz. Correction, if wanted, is an add_reference.py change by the architect.",
        "reinhart2009this: registry used_by is E9, not LX1; the hub lists it as optional core reading (plan section 5.2 allows it). verify_refs --unit LX1 does not re-resolve it; it was checked only by the whole-registry offline integrity run."
    ],
    "freshness_flags": [],
    "notes": [
        "Slice = hub index.html, L01.html, L02.html, tests/labs/LX1/lab-LX1-L01-1.py and lab-LX1-L02-1.py. Not in slice and not verified: L03, L04, project.html, cards.json, project labs, the rung-3 fx_monthly check, and the rebuild of the fx_monthly sha256 (L04 slice).",
        "Cross-slice reads, for the claims the hub makes about other pages only: L03.html (grep for national account and business cycle), project.html data-files, tests/labs/LX1/lab-LX1-project-3.py line 38, L04 twin column (line 42), course/modules/E/E5/L01.html Proposition 1.7, course/modules/FC/FC1/index.html h1.",
        "The rubric and the autograder rules do not apply to LX1 (rubric-only). mutants is empty by design; no grader exists, so no mutation run was made.",
        "Plain curl only: no bot check, login or paywall was bypassed. The Federal Reserve page was fetched once and archived under out/.",
        "Lab twins are demonstrations, so no mutation testing applies (ruling). The lab-to-prose checks were performed by hand and by scripts listed in run_cmds.sh and the .py files of ledgers/LX1/scripts/LX1-a-r1/.",
        "Notation: L01 and L02 reuse the Assumption labels (A1) and (A2) for different hypotheses in different lessons (L01 Assumption 1.1, L02 Proposition 1.2 and 2.1). This is not a symbol collision under notation.json, so it is not a FAIL, but a reader may confuse them."
    ],
    "summary": {"counts": counts, "commands_run": 11, "lab_twins_run": 2, "scripts": [
        "ledgers/LX1/scripts/LX1-a-r1/run_cmds.sh", "lab_check.py", "l01_numbers.py", "l02_numbers.py",
        "concept_owner_check.py", "prose_scan.py", "make_fragment.py"]},
}
out = pathlib.Path("ledgers/LX1/LX1-a.json")
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts, verdict)
