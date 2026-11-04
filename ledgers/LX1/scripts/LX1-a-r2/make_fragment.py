"""Writes the round-2 verifier fragment for LX1 slice a. Every row cites a script or output under ledgers/LX1/scripts/LX1-a-r2/."""
import json
from datetime import datetime, UTC

S = "ledgers/LX1/scripts/LX1-a-r2"
O = f"{S}/out"
rows = []

def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

# 2.9 / 2.5 command rows
row("LX1a-cmd-check_pages", "tools/check_pages.py --unit LX1", "index.html, L01.html, L02.html (project.html, L03, L04 out of slice)", "PASS",
    f"Run at 67c47689: exit 0, output 'check_pages LX1: PASS' ({O}/check_pages.txt; command in {S}/run_cmds.sh).")
row("LX1a-cmd-check_dag", "tools/check_dag.py --unit LX1", "unit DAG", "PASS",
    f"Run at 67c47689: exit 0, 'check_dag LX1: PASS' ({O}/check_dag.txt).")
row("LX1a-cmd-check_projects", "tools/check_projects.py --unit LX1 (command row; project.html is not in this slice)", "project.html", "PASS",
    f"Run at 67c47689: exit 0, 'check_projects LX1: PASS' ({O}/check_projects.txt).")
row("LX1a-cmd-run_labs", "tools/run_labs.py --unit LX1", "tests/labs/LX1 (7 twins; slice owns 2)", "PASS",
    f"Run at 67c47689: 'run_labs LX1: PASS (7/7)', exit 0 ({O}/run_labs_unit.txt).")
row("LX1a-cmd-twins-isolated", "python -I -W error on each twin, alone", "tests/labs/LX1/lab-LX1-L01-1.py, lab-LX1-L02-1.py", "PASS",
    f"Run alone: L01 exit 0, L02 exit 0, stderr 0 bytes each ({O}/twin_L01-1.txt, {O}/twin_L02-1.txt, {O}/twin_L01-1.err, {O}/twin_L02-1.err). Also .venv python -I -W error on L01 exit 0 ({O}/twin_L01-1_venv.txt).")
row("LX1a-cmd-page_smoke", "tools/page_smoke.py --unit LX1 --pages <page>, one page per run, no other job running", "index.html, L01.html, L02.html",
    "PASS", f"'page_smoke modules/LX/LX1/index.html: PASS', '...L01.html: PASS', '...L02.html: PASS'; 'page_smoke LX1: PASS'; lab lab-LX1-L02-1 0.0 s, runtime boot 1.1 s ({O}/page_smoke_index.txt, {O}/page_smoke_L01.txt, {O}/page_smoke_L02.txt).")
row("LX1a-cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental on tests/labs/LX1", "tests/labs/LX1", "PASS",
    f"ruff check 'All checks passed!' ({O}/ruff_labs.txt); ruff format --check '7 files already formatted' ({O}/ruff_format_labs.txt); mypy 'Success: no issues found in 7 source files' ({O}/mypy_labs.txt).")
row("LX1a-cmd-pytest", "pytest -k 'lab or page or LX1 or dag or project or embed or refs' over tests/", "the tests selected by -k across tests/ (the file list is in the output)", "PASS",
    f"Exit 0, all dots, no failures ({O}/pytest_relevant.txt).")
row("LX1a-cmd-verify_refs-live", "tools/verify_refs.py --unit LX1", "references/references.json: friedman1963monetary, eichengreen1992golden, garber2000famous", "PASS",
    f"'live re-verification of LX1: 3 of 560 entries, 0 problems', exit 0 ({O}/verify_refs_unit.txt). reinhart2009this has used_by E9, so the unit run does not include it (registry flag).")
row("LX1a-cmd-verify_refs-offline", "tools/verify_refs.py --offline", "references/references.json", "PASS",
    f"'offline integrity: 560 entries, 0 problems', exit 0 ({O}/verify_refs_offline.txt).")
row("LX1a-cmd-fetch_data-check", "tools/fetch_data.py --check", "course/assets/data/market/MANIFEST.json, fx_monthly.csv", "PASS",
    f"'fetch_data: 3 datasets, 0 problems', exit 0 ({O}/fetch_data_check.txt). The live rebuild of the fx_monthly sha256 is the L04 slice's check and was not run here.")

# lab rows
row("LX1a-lab-L01-1", "lab twin, page code, expected block, SIMULATED label, seed, no network, runtime", "course/modules/LX/LX1/L01.html section 'Lab 1' (lines ~127-290); tests/labs/LX1/lab-LX1-L01-1.py", "PASS",
    f"Page code equals twin after removing the final newline only; expected block equals twin stdout ({O}/page_twin_check.txt). Twin exit 0, stderr empty ({O}/twin_L01-1.txt). Seed SEED = 20261103; imports math, random, fractions only; no file or network. Hypothesis checks against printed output: F_0 = 20000/3 rounds to 6667; q = 103/109; identity True at N = 10, 60, 200; 200-term sum rounds to closed form True; Part B 9 of 13 positive gaps; Part C 13 of 13; count changes True. Recomputed independently in {S}/numbers_check.py ({O}/numbers_check.txt). Heading and interpretation carry SIMULATED.")
row("LX1a-lab-L02-1", "lab twin, page code, expected block (incl. new Part E), SIMULATED label, seed, no network", "course/modules/LX/LX1/L02.html section 'Lab 1' (lines ~133-300); tests/labs/LX1/lab-LX1-L02-1.py", "PASS",
    f"Page code equals twin after the final newline; expected block equals twin stdout including Part E lines ({O}/page_twin_check.txt). Twin exit 0, stderr empty ({O}/twin_L02-1.txt). Seed 20261104; no data file; SIMULATED heading. Printed values recomputed exactly in {S}/numbers_check.py: V_1 = 1010101; 6 falling and 6 rising periods at the same t; largest cent step 42236 at t = 12; V_12/V_0 = 1.055909 to six places; Part E 5/2 currency units per gram.")

# numbers
row("LX1a-num-L01-closed-form-sums", "2.2 numbers, Theorem 1.3 and Lab 1 Part A", "L01.html lines ~70-80, ~246-260, ~414-432", "PASS",
    f"numbers_check.py: F_0 = 20000/3 (6666.67) rounds to 6667; q = 103/109 = 0.944954; S_10 rounds 2882, F_0 q^10 rounds 3785; S_60 rounds 6444, residual 223; S_200 rounds 6667, residual 0; identity exact for each N ({O}/numbers_check.txt).")
row("LX1a-num-L01-prop22-witness", "2.2 numbers, Proposition 2.2 witness", "L01.html Proposition 2.2 proof (witness paragraph) and Misconception 1", "PASS",
    f"F_0(1%) = 400/0.08 = 5000; F_0(3%) = 20000/3; gap at P_0 = 6000 is +1000 under 1% and -2000/3 under 3% ({O}/numbers_check.txt).")
row("LX1a-num-L01-canon-breaks-367", "2.2 numbers, Section 5 and Misconception 2 (non-constant path)", "L01.html Section 5 bullet 2; Misconception 2", "PASS",
    f"400/1.09 = 40000/109 = 366.97 rounds to 367; closed form at g = 3% rounds to 6667 ({O}/numbers_check.txt).")
row("LX1a-num-L01-lab-counts", "2.2 numbers, Lab 1 counts and largest gap", "L01.html Lab 1 interpretation, Key results row 5, Empirical 2", "PASS",
    f"Lab 1 Part B prints 9 of 13 above fundamental and Part C prints 13 of 13; difference 4 ({O}/numbers_check.txt; expected block lines 'periods with price above...'). Largest gap 2175 at t = 9 is printed and recomputed (wedge +25 percent, F_9 = 8698.49).")
row("LX1a-num-L01-empirical-shares", "2.2 numbers, Empirical 1 and rewritten Empirical 3 (round-2 change)", "L01.html Empirical 1, Empirical 3 solution", "PASS",
    f"9/13 = 0.6923 to four places. Printed integers: 2175/8698 = 0.25005748, 0.250057 to six places, 25.01 percent to two places. Unrounded: F_9 = 400 * 1.03^9 / 0.06 = 8698.4879 (8698.49 to two places); gap = 0.25 F_9 = 2174.62; so the gap is exactly 25.00 percent of the unrounded fundamental, and the printed 25.01 percent comes from rounding the gap (2174.62 to 2175) and the base (8698.49 to 8698). Verified in {O}/numbers_check.txt. Research 1 threshold g* = 7/300 = 2.33 percent, verified.")
row("LX1a-num-L01-mechanics", "2.2 numbers, Mechanics 1-3", "L01.html Mechanics 1, 2, 3 solutions", "PASS",
    f"250/0.06 = 12500/3 = 4166.67 rounds to 4167; 250 * 1.04^3 / 0.06 = 4686.93 rounds to 4687 (1.04^3 = 1.124864); 100/1.05 = 2000/21 per term, S_10 = 20000/21 = 952.38 ({O}/numbers_check.txt).")
row("LX1a-num-L01-quiz-numeric", "2.2 numbers, retrieval quiz numeric answers", "L01.html quiz items 2-5", "PASS",
    f"F_0 = 6666.67 (tolerance 0.01); F_2 = 7072.67 rounds to 7073 (Lab 1 prints 7073 at t = 2); q = 0.9449541 (six places 0.944954, tolerance 1e-6 holds); g* = 0.0233333 (six places 0.023333, tolerance 1e-6 holds) ({O}/numbers_check.txt).")
row("LX1a-num-L02-real-values", "2.2 numbers, Lab 2 values and Problems M1-M3, E2, E3, quiz 3-4 and 8", "L02.html Problems M1-M3, E2, E3; quiz items 3, 4, 7", "PASS",
    f"M1 V_1 = 2500; M2 V_2/V_1 = 18/17; M3 200000/95 = 2105.263 rounds to 2105; E2 V_1 = 1010101.0101 rounds to 1010101; E3 unrounded P_12 = 94.70509914753977, 100/P_12 = 1.05590935 (8 places), printed-index ratio 100/94.7051 = 1.0559093..., difference from unrounded ratio 9.5e-9, so less than one part in a million as stated; quiz 18/17 = 1.0588235294 ({O}/numbers_check.txt).")
row("LX1a-num-L02-counts", "2.2 numbers, Lab 2 counts, Problem E1, quiz 6", "L02.html Problem E1, Key results row 4, quiz item 6", "PASS",
    f"Falls at t = 1, 5, 6, 8, 9, 12 (six); rises at t = 2, 3, 4, 7, 10, 11 (six); all twelve changes non-zero; cent steps listed in {O}/numbers_check.txt; largest one-period rise 42236 at t = 12 (printed).")
row("LX1a-num-hub-placement", "2.2 numbers, hub placement diagnostic", "index.html placement section (items at lines ~77-147)", "PASS",
    f"Ten items: prerequisite items 8 (P0.1 x1, E1 x1, M1 x2, M2 x1, E5 x2, FC1 x1) plus two skill checks, as the intro states. Answers: 1000 = 100/0.10; 0.1 = 110/100 - 1; 100 = 10050 - 9950; 800 = 1000/1.25; discount factor 1/(1+r)^2; derivative of ln x = 1/x. Mastery arithmetic: 8 of 10 = 80 percent, 7 of 10 = 70 percent (computed by hand, consistent with the text).")
row("LX1a-num-hub-hours", "2.9 hours arithmetic", "index.html data-hours-lessons=40, data-hours-project=10, hours table, eyebrow; L01 and L02 data-hours=10", "PASS",
    "40 = 4 x 10 (L01 and L02 data-hours 10 confirmed; L03 and L04 are out of this slice); 40 + 10 = 50 = curriculum hours (curriculum.json LX1 hours 50); 10/50 = 20 percent; hours table 1 + 1 + 2 + 1.5 + 2.5 + 2 = 10 (index.html lines ~186-194). The rung-1 wording of that table is a separate FAIL row.")

# math
row("LX1a-math-L01-thm1.3", "2.4 mathematics, Theorem 1.3 and its proof", "L01.html Assumption 1.1, Definition 1.2, Theorem 1.3 and proof", "PASS",
    "Re-derived: d_{t+k}/(1+r)^k = d_1(1+g)^t q^{k-1}/(1+r); 1 - q = (r-g)/(1+r) > 0 under (A0); S_N(t) = F_t(1 - q^N) exact; 0 < q < 1 so the series converges; checked in Fraction arithmetic in numbers_check.py. Hypotheses (A0) and (A1) are numbered and stated before the statement.")
row("LX1a-math-L01-prop1.4", "2.4 mathematics, Proposition 1.4", "L01.html Proposition 1.4 and proof", "PASS",
    "q >= 1 since g >= r gives 1 + g >= 1 + r > 0; each term d_1 q^{k-1}/(1+r) >= d_1/(1+r) > 0; S_N(0) >= N d_1/(1+r) -> infinity. Hypotheses (A1) with d_1 > 0 and 1 + g > 0 and (A2) r > -1, g >= r are stated before the conclusion. Proof complete.")
row("LX1a-math-L01-prop2.2", "2.4 mathematics, Proposition 2.2 (hypotheses now numbered)", "L01.html Proposition 2.2 hypotheses (A3), (A4), conclusion and proof", "PASS",
    "Proof valid: g < g' gives r - g > r - g' > 0; reciprocal reverses order; multiplication by d_1 > 0 preserves it. The hypotheses are numbered (A3) and (A4), continuing the lesson's sequence (A0-A2 earlier), so the labels are unique within the lesson. Witness re-derived in numbers_check.py. The statement 'for some prices' matches the proof; the round-1 unqualified 'the sign' wording is gone.")
row("LX1a-math-L01-problems", "2.4 mathematics, every worked solution in L01 Problem set", "L01.html Mechanics 1-3, Proof 1-3, Empirical 1-3, Research 1-3", "PASS",
    "Each solution re-derived by hand and in numbers_check.py: Proof 1 (strict monotonicity in g, reciprocal argument correct); Proof 2 (F_t/F_{t-1} = 1+g, division needs d_1 != 0 as stated); Proof 3 (term ratio q^{k-1} with q > 1); Empirical 1-3 (see num rows); Research 1 (g* = 7/300); Research 2-3 are discussion answers with no computed claim beyond Proposition 2.2 and Assumption 1.1, both checked.")
row("LX1a-math-L02-prop1.2", "2.4 mathematics, Proposition 1.2 (currency price of gold)", "L02.html Definition 1.1, Proposition 1.2, proof, Remark 1.3", "PASS",
    "Under (A1) one unit buys kappa grams, so one gram costs 1/kappa; the proof uses (A1) at every date. Lab 1 Part E checks the formula at kappa = 2/5 (prints 5/2 and kappa times price equals 1). Correct as stated.")
row("LX1a-math-L02-prop2.1-cor3.2", "2.4 mathematics, Proposition 2.1(a),(b) and Corollary 3.2", "L02.html Proposition 2.1 and proof, Corollary 3.2 and proof", "PASS",
    "(a): V_t/V_{t-1} = P_{t-1}/P_t by cancellation of the positive factor D P_0 (A2, A3). (b) by telescoping is correct; the algebra is right, although the proof uses T for the horizon (notation row LX1a-notation-L02-T). Corollary 3.2: V_t > V_{t-1} iff P_t < P_{t-1} because V_{t-1} > 0 and P_t > 0. Lab Parts B-D confirm on the path.")
row("LX1a-math-L02-problems", "2.4 mathematics, every worked solution in L02 Problem set", "L02.html Problems M1-M3, P1-P3, E1-E3, R1-R3", "PASS",
    "Each solution re-derived: M1 2500; M2 18/17; M3 2105; P1 monotone implication; P2 induction (H used in the statement; the proof is in H); P3 rescaling invariance; E1 six negative changes; E2 1010101; E3 1.055909; R1 finite-check argument; R2 real value D constant under index-linked payment; R3 two indices, signs of each real-value change. No algebra error found.")

# notation
row("LX1a-notation-L01", "2.4 notation, notation/notation.json symbols and macros", "L01.html (all math), index.html", "PASS",
    f"Registered symbols (notation.json symbols: T, Phi, gamma_3, gamma_4, R^ast, R^{{e ast}}, R_f, Q) do not appear in L01 or the hub. The LaTeX commands used are raw TeX primitives and no registered macro (\\E, \\R, ...) appears ({O}/text_checks.txt). F^{{\\ast}}_t in Theorem 1.3's proof is a local symbol, distinct from the registered R^{{\\ast}}; not a collision. Local symbols d, g, r, F, B, P, q, S_N, k, s, t are defined on first use.")
row("LX1a-notation-L02-T", "2.3 notation, symbol T", "L02.html line 98 (proof of Proposition 2.1(b))", "FAIL",
    f"Round-2 status: the statement (line 92) now uses H, but the proof still uses T as a time horizon: 'for t = 1, ..., T', the products '\\prod_{{t=1}}^{{T}}', 'V_T / V_0' and 'P_0 / P_T'. notation/notation.json symbols[0] registers T as 'number of return observations (periods) in a sample' (module S1). plans/LX1-build-plan.md section 2.3 says a time horizon is H and T is not used ({O}/text_checks.txt, line '-- symbol T in L02').",
    "On L02.html line 98, replace every T with H: 't = 1, ..., H', '\\prod_{t=1}^{H}', 'V_H / V_0' and 'P_0 / P_H' (the statement and Problem P2 already use H). Then re-run check_pages --unit LX1.")
row("LX1a-notation-hub", "2.3 notation, hub", "index.html", "PASS",
    "The hub uses only D, P_t, r, k, x as local symbols in its placement items and no registered symbol (text_checks.txt scan of LaTeX commands: sum, ge, ln only).")

# DAG
row("LX1a-dag-links", "2.9 DAG, linked concept uses resolve to closure owners", "index.html, L01.html, L02.html links with data-concept", "PASS",
    "check_dag LX1 PASS ({O}/check_dag.txt). Every linked concept resolves: price-index-inflation (E5), growing-perpetuity, present-value, geometric-series, exponential-and-logarithm (M1), derivative (M2), comparative-statics (E1), evidence-grade, project-ladder (P0.1); the anchors exist in course/concepts.html (nine ids counted with grep). Links to L02/L01 defs are local.")
row("LX1a-dag-outside-closure", "2.9 DAG, outside-closure names used by name or link (D1-D15)", "index.html, L01.html, L02.html", "PASS",
    f"Grep for bank run, fire sale, leverage, banking/currency crisis, covered/uncovered interest, efficient markets, moral hazard, Fisher, bank reserves, central bank, credit default, contagion, term spread, sovereign, deposit insurance: no matches in the three pages ({O}/text_checks.txt, section 'outside-closure names'). 'liquidity' (L01 Remark 3.2) is a plain word, not a concept.")
row("LX1a-dag-defined-once", "2.9 DAG, each concept defined once in its assigned lesson, never before use", "L01.html def-speculative-bubble, def-financial-panic; L02.html def-gold-standard, def-debt-deflation", "PASS",
    "grep of dfn ids across all LX1 pages: each slice concept appears once, in the assigned lesson (speculative-bubble and financial-panic in L01; gold-standard and debt-deflation in L02). Plain dfn terms (fundamental value, parity, convertibility, nominal debt, real value) have no data-concept. The hub links only.")

# structure
row("LX1a-struct-hub", "2.9 structure, hub template sections", "index.html", "PASS",
    "Sections in order: header with meta-row, objectives (6), prerequisites, placement diagnostic (10 items, mastery 0.8), lessons (four cards; L01 and L02 card titles match their h1 exactly), project ladder (four rungs), data status, hours table, core reading. Hours split 40/10 with 20 percent. check_pages LX1 PASS. Note (not a failing row): two prerequisite <li> items, at index.html lines 63 and 67, have no closing </li>, which browsers tolerate.")
row("LX1a-struct-L01-L02", "2.9 structure, lesson template", "L01.html, L02.html", "PASS",
    "Order: why-it-matters (L01 116 words, L02 102 words, both at most 120); numbered core sections; inline lab with SIMULATED heading; 'where the canon breaks'; misconceptions (three each); problem set with three problems in each of Mechanics, Proof, Empirical, Research, all with details.solution; key-results table; retrieval quiz with 10 items each and explanations; references. Counts from text_checks.txt and direct reads.")

# prose
row("LX1a-prose-banned", "2.9 banned phrases (BUILDER_RULES 1.3-1.4 list in CLAUDE/plan)", "index.html, L01.html, L02.html", "PASS",
    f"grep for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, and ellipsis outside code: no hits ({O}/text_checks.txt, section 'banned').")
row("LX1a-prose-process-words", "2.9 process words in learner text", "index.html, L01.html, L02.html", "PASS",
    f"grep for builder, build, verifier, verify, REQUEST, planner, fixer, unit report, ledger, checkout, pin: no hits ({O}/text_checks.txt).")
row("LX1a-claim-E5-prop1.7", "2.1 attribution: hub placement answer cites E5 Proposition 1.7", "index.html line ~130 (explain text) vs course/modules/E/E5/L01.html line 93-94", "PASS",
    "E5 L01.html Proposition 1.7 (closed-economy saving equals investment): under (A0) Assumption 1.3 and (A1) closed economy, (A2) defines S_p and S_g; conclusion 'S_p + S_g = I' (line 94). The hub sentence 'private plus public saving equals investment in a closed economy' matches.")
row("LX1a-claim-registry-records", "2.1 registry records for the four keys the hub and pages cite", "index.html reading list; L01.html References and Section 4; L02.html References; references/references.json", "PASS",
    "friedman1963monetary: 'A monetary history of the United States 1867-1960', first author Friedman, 1963, verified, used_by LX1 (the hub types Friedman only, plan N2). eichengreen1992golden: 'Golden fetters: the gold standard and the Great Depression, 1919-1939', 1992, verified, used_by LX1. garber2000famous: 'Famous First Bubbles: The Fundamentals of Early Manias', 2000, verified, used_by LX1. reinhart2009this: 'This Time Is Different: Eight Centuries of Financial Folly', 2009, verified; used_by E9 (registry flag). Read with ledgers/LX1/scripts/LX1-a-r2/registry_check.py (output ledgers/LX1/scripts/LX1-a-r2/out/registry_check.txt).")
row("LX1a-claim-attribution-readings", "2.1 attribution: no sentence attributes content to an unread work", "L01.html Section 4 and Section 5 bullet 6; L02.html References; index.html", "PASS",
    "Round-1 FAIL fixed: L01 Section 5 now reads 'The reading list names sources for that debate. This lesson has not read them, and it does not settle the debate.' L01 Section 4 and References cite Garber for title only; L02 References says no passage is read. No sentence in the three pages attributes a claim to Friedman, Eichengreen, Garber or Reinhart: the only hits are the reading-list and References lines (index.html 203-206; L01.html 303 and 489; L02.html 535-537), each stating the title or key only.")
row("LX1a-claim-fed-licence", "2.8 licence of fx_monthly: quoted grant at the issuer page", "index.html Data status; tools/data_sources.yaml lines 57-60; MANIFEST fx_monthly licence_url", "PASS",
    f"Plain curl of https://www.federalreserve.gov/disclaimer.htm: HTTP 200, 85306 bytes; the quoted sentence 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission' is present ({S}/licence_check.sh, {O}/licence_check.txt, page archived at {O}/licence/disclaimer.htm). The hub quote is a truncation at 'without permission.' and matches the page text.")
row("LX1a-claim-fx-note-blanks", "2.8 data claims for fx_monthly: spot-only note, euro start, GBP without blanks", "index.html lines ~178-179; tools/data_sources.yaml lines 62-64; course/assets/data/market/fx_monthly.csv", "PASS",
    f"Note in tools/data_sources.yaml: 'Each value is the last noon rate of its month ... The euro starts in January 1999. Spot rates only.' CSV counts ({O}/csv_check.txt): 669 rows 1971-01 to 2026-09; EUR 336 blanks, first non-blank 1999-01; GBP 0 blanks; the hub's 'Lesson 4 uses the GBP column, which has no blank cells' holds (L04 twin COLUMN = 'GBP', tests/labs/LX1/lab-LX1-L04-1.py line 43).")
row("LX1a-claim-hub-no-other-series", "2.8 data claim: no historical series for gold, prices, output, unemployment or bank failures is embedded", "index.html Data status second paragraph", "PASS",
    "MANIFEST datasets are exactly fx_daily, fx_monthly, ust_daily (ledgers/LX1/scripts/LX1-a-r2/csv_check.py, output ledgers/LX1/scripts/LX1-a-r2/out/csv_check.txt); none is a gold, price-level, output, unemployment or bank-failure series, consistent with the hub sentence and the plan section 6.1.")
row("LX1a-claim-P0.1-not-released", "2.9 claim: P0.1 concepts link to 'not yet released' entries", "index.html lines ~35, 61, 68", "PASS",
    "course/concepts.html contains the text 'not yet released' (grep count 806 matches across the file, including the evidence-grade and project-ladder entries). Hub wording matches.")
row("LX1a-claim-simulated-labels", "2.8 SIMULATED labels on generated-number labs and figures", "L01.html Lab 1 heading; L02.html Lab 1 heading; index.html", "PASS",
    "Both slice labs are headed 'SIMULATED' and their prose says the numbers are seeded draws. The hub states which labs are SIMULATED (Lessons 1-3 and project rungs 1-2) and which is real data (Lesson 4 and rung 3).")
row("LX1a-data-figures", "2.8 figures", "index.html, L01.html, L02.html", "PASS",
    "grep -c for svg, figure and data-chart: 0 in each of the three pages. No live figures or kernels, as plan section 12 item 13 decided. Nothing to check.")
row("LX1a-scope-words", "2.9 / 2.1 scope words (every, all, always, never, any, only, exactly, same, drives, ...)", "index.html, L01.html, L02.html", "PASS",
    "Each scope word in the three pages was read in context (text_checks and direct reads). Universal claims are backed by a derivation (for every t, every k, every path under (A3)), a finite lab check with its counts, or an explicit hypothesis. The round-1 'only quantitative tool' sentence is replaced; no remaining scope word is contradicted by a computation on the pages.")

# hub fixes from round 1 (now verified)
row("LX1a-hub-fc1-title", "2.9 prose: FC1 title matches the curriculum and the FC1 h1", "index.html line 35", "PASS",
    "Round-1 FAIL fixed: hub reads 'FC1 The Financial System, Markets &amp; Instruments'. curriculum/curriculum.json FC1 title 'The Financial System, Markets & Instruments' (title_check.txt); course/modules/FC/FC1/index.html h1 identical.")
row("LX1a-hub-fx-one-lab", "2.8 prose: data count and which labs use the embedded series", "index.html lede, meta-row, Data status", "PASS",
    "Round-1 FAIL fixed: the hub now says the series is used in Lesson 4 and the project's rung-3 check; 'Every other lab' is gone (grep count 0). tests/labs/LX1/lab-LX1-project-3.py reads data/fx_monthly.csv (line 41) and project.html line 281 has data-files=\"fx_monthly.csv\"; L04 has data-files too (L04.html line 112). The labs of L01-L02 read no file.")
row("LX1a-hub-derivative-claim", "2.9 DAG/prose: where each prerequisite concept is used", "index.html line 66", "PASS",
    "Round-1 FAIL fixed: the derivative bullet now says 'tested by placement question 5'. Placement question 5 (the sixth item; items 1-10 in order) asks the derivative of ln x (item at index.html ~line 109), so the claim is true. L01 does not use the derivative and no longer claims to.")
row("LX1a-hub-L03-concept-claim", "2.9 DAG/prose: hub claims about concepts used in Lesson 3", "index.html line 66 (E5 bullet)", "PASS",
    "Round-1 FAIL fixed: the hub's E5 bullet now lists only price indices for Lesson 2. The claim that national accounts and the business cycle are used in Lesson 3 was removed, so nothing the hub asserts about L03 is contradicted (L03 is outside this slice).")
row("LX1a-hub-historian-regulator", "2.2 scope/prose: unsupported generalization about historians and regulators", "index.html lede", "PASS",
    "Round-1 FAIL fixed: the lede now reads 'Each topic is taught as a mechanism for explaining an episode.' grep for historian and regulator: no hits (text_checks.txt).")
row("LX1a-L01-usual-first-test", "2.1 scope: generalization about the literature", "L01.html why-it-matters", "PASS",
    "Round-1 FAIL fixed: the sentence now reads 'A price above a benchmark is a gap only relative to that benchmark, and the sign of the gap can change with the benchmark's assumed growth rate (Proposition 2.2 of this lesson).' Its claim is proved in Proposition 2.2.")
row("LX1a-L01-gap-integer-cents", "2.2 numbers: units of the gap", "L01.html Definition 2.1", "PASS",
    "Round-1 FAIL fixed: the gap is 'measured in cents, the currency unit of the dividends; Lab 1 reports it rounded to whole cents'. The gap is not integer-valued in general (F_0 = 20000/3 cents), and the page now says so.")
row("LX1a-L01-prop22-unnumbered-assumptions", "2.1 item 6: numbered assumptions before a Proposition", "L01.html Proposition 2.2", "PASS",
    "Round-1 FAIL fixed: the hypotheses are an ordered list (A3) d_1 > 0 and (A4) growth-rate conditions, before the conclusion. The numbering continues the lesson's (A0)-(A2) and is unique within the lesson; a reader can cite (A3) and (A4) without confusion.")
row("LX1a-L01-only-quantitative-tool", "2.1 scope: 'only' claim", "L01.html Section 4", "PASS",
    "Round-1 FAIL fixed: the sentence now reads 'The benchmark of Section 1 is the quantitative object that Section 2 uses to define a bubble.' Section 2 computes gaps and Lab 1 computes sums and counts, so no 'only' claim is contradicted.")
row("LX1a-L02-prop12-no-lab-check", "2.5 lab checks a key formula (BUILDER_RULES 3.4)", "L02.html Proposition 1.2, Key results row 1, lab-LX1-L02-1 Part E", "PASS",
    "Round-1 FAIL fixed: Part E prints 'currency price of one gram = 1 / kappa = 5/2 currency units' and 'kappa times the gram price equals 1 exactly: True', and the expected block contains these lines (page_twin_check.txt). Key results row 1 cites Part E. The lab does not test the assumption (A1) for every date, and the interpretation says so.")
row("LX1a-L02-CU-undefined", "2.1 prose: undefined abbreviation CU", "L02.html lab hypothesis and interpretation; tests/labs/LX1/lab-LX1-L02-1.py docstring", "PASS",
    "Round-1 FAIL fixed: 'currency units' is written in full on the page and in the twin docstring; grep -E '\\bCU\\b' over the slice's pages and twins: no hits (text_checks.txt).")

# new FAIL rows found in round 2
row("LX1a-L02-misconception-gold-price", "2.9 prose vs lab output: a sentence about what the lab's model contains", "L02.html misconception 2 (line 323)", "FAIL",
    "The sentence says 'while the model contains no gold price at all, so the lab itself does not link the two prices'. Part E of lab-LX1-L02-1, which the page now prints, computes a gold price: 'currency price of one gram = 1 / kappa = 5/2 currency units' (expected block; twin_L02-1.txt). The sentence is contradicted by the lab's own output.",
    "On L02.html line 323, replace 'while the model contains no gold price at all, so the lab itself does not link the two prices' with 'while the index path of Parts A to D is not linked to the gold price that Part E computes, so the lab does not link the two prices'.")
row("LX1a-hub-E5-title", "2.9 prose: module titles match the curriculum", "index.html line 35 (Prerequisites meta-row)", "FAIL",
    f"Hub writes 'E5 Macroeconomics I'. The curriculum title is 'Macroeconomics I: Aggregates, Cycles & Policy' ({O}/title_check.txt) and course/modules/E/E5/index.html line 32 h1 is the same. The round-1 FAIL for FC1 was the same kind of error and was fixed; this one remains.",
    "On index.html line 35, write 'E5 Macroeconomics I: Aggregates, Cycles &amp; Policy' (as for FC1).")
row("LX1a-hub-hours-rung1", "2.9 prose consistency: hub hours table vs hub ladder and project", "index.html line 188 (hours table, rung 1 row) vs index.html ladder item 1 and project.html lines 44 and 452", "FAIL",
    "Hub hours row says 'One solved SIMULATED path, annotated line by line'. The hub's own ladder (index.html ladder item 1) says the rung 1 worked example is 'over two SIMULATED price paths, periods 0 to 5', and project.html line 44 says 'on two SIMULATED price paths'. project.html line 452 says 'One solved SIMULATED comparison'.",
    "On index.html line 188, change the rationale to 'One solved SIMULATED comparison of two price paths, annotated line by line'.")
row("LX1a-hub-objective-panic", "2.1 scope/accuracy: objective says each definition depends on an assumption", "index.html objective 2 (line 51)", "FAIL",
    "Objective 2 says the reader can 'state the assumption each definition depends on (Lesson 1)'. Definition 3.1 (financial panic, L01.html line ~289) is 'by mechanism' and names no assumption; Remark 3.3 says a benchmark is needed only when one is stated. The objective overstates what the lesson states.",
    "In index.html objective 2, replace 'and state the assumption each definition depends on (Lesson 1)' with 'and state the assumption the bubble definition depends on, while the panic definition rests on its mechanism alone (Lesson 1)'.")

row("LX1a-twin-page-equality", "2.5 page code equals twin; expected block equals output", "L01.html and L02.html lab blocks vs tests/labs/LX1/lab-LX1-L01-1.py and lab-LX1-L02-1.py", "PASS",
    f"{S}/page_twin_check.py: page code equals twin after removing only the final newline (page code ends without a newline, the twin file does) for both labs; expected block equals the twin's stdout for both. Output in {O}/page_twin_check.txt.")
row("LX1a-claim-hub-math-prereqs", "2.9 prerequisite closure and titles", "index.html prerequisites list", "PASS",
    f"Closure of LX1 from curriculum.json prereqs (FC1, E5 -> P0.1, E1, M2, M1) = {{E1, E5, FC1, M1, M2, P0.1}}, as the hub says. Titles of E1, M1, M2, P0.1 in the hub match curriculum.json exactly ({O}/title_check.txt); only E5 is shortened (row LX1a-hub-E5-title).")

PREFIX_NOTE = "No PASS row was carried from round 1: every row was re-derived in round 2."
frag = {
    "unit": "LX1",
    "slice": "LX1-a",
    "round": 2,
    "verifier": "Haiku independent verifier, LX1 slice a, round 2 (did not build LX1)",
    "pin": "67c47689",
    "base": "1c1645f3 (round-1 pin; delta computed with git diff 1c1645f3 67c47689)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE2-LX1-a (detached at 67c47689, .venv symlinked)",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE2-LX1-a/ledgers/LX1/scripts/LX1-a-r2/out",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "friedman1963monetary: registry record lists Friedman as the only author (plan N2). Pages cite the key only and do not type Schwartz. Any correction is an add_reference.py change by the architect.",
        "reinhart2009this: registry used_by is E9, not LX1. The hub lists it as optional core reading. verify_refs --unit LX1 does not re-resolve it; it was checked only by the whole-registry offline run.",
    ],
    "freshness_flags": [],
    "notes": [
        "Slice = hub index.html, L01.html, L02.html, tests/labs/LX1/lab-LX1-L01-1.py and lab-LX1-L02-1.py. Read in full: index.html (213 lines), L01.html (501 lines), L02.html (550 lines), both twins.",
        "Delta from 1c1645f3 to 67c47689 in the slice: index.html (lede, prerequisite bullets, placement item text, ladder, data status), L01.html (why-it-matters, Definition 2.1, Proposition 2.2, interpretations, Empirical 3, Key results, footer), L02.html (Part E, interpretations, misconception text of lab), lab-LX1-L02-1.py (Part E, 'currency units'), plans/LX1-open-items.md (new, not in the slice). Every hunk was read. tools/, curriculum/, references/ and notation/ are unchanged in the delta.",
        "Lab twins are demonstrations; mutation testing does not apply (ruling). LX1 has no grader and no mutants; mutants is empty by design.",
        "Notation: Assumption labels (A0) to (A4) are numbered per lesson; L01 and L02 both use (A1) for different hypotheses. This is not a registered-symbol collision, so it is not a FAIL. Recorded as a reading note.",
        "Cross-slice reads (for claims the hub makes about other pages only): course/modules/LX/LX1/L03.html (grep for national account and business cycle: none), L04.html line 112 data-files, project.html lines 44, 45, 73, 210, 215, 281, 452, tests/labs/LX1/lab-LX1-project-3.py line 41, lab-LX1-L04-1.py line 43, course/modules/E/E5/L01.html lines 93-94, course/modules/E/E5/index.html line 32, course/modules/FC/FC1/index.html line 32.",
        "Not in slice and not verified here: L03, L04 pages and their labs, project.html and its labs, cards.json, the live rebuild of the fx_monthly sha256 (fetch_data --fetch in a scratch copy), page_smoke for L03, L04, project, and the rung-3 check's data.",
        "Plain curl only. The Federal Reserve page was fetched once (HTTP 200) and archived under out/licence/. No bot check, login or paywall was touched.",
        "Verifier posture on the builder's fixes: the L02 proof of Proposition 2.1(b) changed its statement to H but left T in the proof, so the round-1 notation row is still FAIL.",
        PREFIX_NOTE,
    ],
    "summary": {
        "counts": {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows),
                   "fail": sum(r["status"] == "FAIL" for r in rows),
                   "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows)},
        "round1_non_pass_rechecked": 13,
        "round1_fixed_now_pass": 12,
        "round1_still_fail": ["LX1a-notation-L02-T"],
        "commands_run": ["run_cmds.sh (check_pages, check_dag, check_projects, run_labs, ruff, ruff format, mypy, verify_refs live and offline, fetch_data --check)",
                         "page_smoke --unit LX1 --pages (index, L01, L02, alone)", "pytest -k subset", "python -I -W error on both twins",
                         "numbers_check.py", "page_twin_check.py", "text_checks.sh", "csv_check.py", "licence_check.sh", "title_check.txt"],
        "lab_twins_run": 2,
        "scripts": [f"{S}/run_cmds.sh", f"{S}/numbers_check.py", f"{S}/page_twin_check.py", f"{S}/text_checks.sh",
                    f"{S}/csv_check.py", f"{S}/registry_check.py", f"{S}/licence_check.sh", f"{S}/make_fragment.py"],
    },
}
with open("ledgers/LX1/LX1-a.json", "w", encoding="utf-8") as fh:
    json.dump(frag, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), "counts", frag["summary"]["counts"])
