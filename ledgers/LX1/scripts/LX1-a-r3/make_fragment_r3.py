"""Writes the round-3 verifier fragment for LX1 slice a (hub index.html, L01, L02, twins L01-1 and L02-1).

Every row cites a script, an output file under ledgers/LX1/scripts/LX1-a-r3/out/, or a line in the slice.
"""
import json
from datetime import UTC, datetime

S = "ledgers/LX1/scripts/LX1-a-r3"
O = f"{S}/out"
rows = []


def row(id_, check, location, evidence, status="PASS", fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- commands (run by ledgers/LX1/scripts/LX1-a-r3/run_cmds.sh at pin 67a2d13)
row("LX1a-cmd-check_pages", "tools/check_pages.py --unit LX1", "index.html, L01.html, L02.html (L03, L04, project.html are other slices)",
    f"Run at 67a2d13: exit 0, 'check_pages LX1: PASS' ({O}/check_pages.txt; command in {S}/run_cmds.sh).")
row("LX1a-cmd-check_dag", "tools/check_dag.py --unit LX1", "unit DAG",
    f"Run at 67a2d13: exit 0, 'check_dag LX1: PASS' ({O}/check_dag.txt).")
row("LX1a-cmd-check_projects", "tools/check_projects.py --unit LX1", "project.html (not in this slice; command row)",
    f"Run at 67a2d13: exit 0, 'check_projects LX1: PASS' ({O}/check_projects.txt).")
row("LX1a-cmd-run_labs", "tools/run_labs.py --unit LX1", "tests/labs/LX1 (7 twins; slice owns lab-LX1-L01-1 and lab-LX1-L02-1)",
    f"Run at 67a2d13: 'run_labs LX1: PASS (7/7)', exit 0 ({O}/run_labs_unit.txt).")
row("LX1a-cmd-twins-isolated", "python -I -W error on each slice twin, run alone", "tests/labs/LX1/lab-LX1-L01-1.py, lab-LX1-L02-1.py",
    f"Run alone at 67a2d13: L01 EXIT=0 and L02 EXIT=0; the merged stdout+stderr files contain no Warning, error or Traceback text ({O}/twin_L01.txt, {O}/twin_L02.txt). page_twin_check_r3.py reports stderr bytes 0 for both ({O}/page_twin_check_r3.txt).")
row("LX1a-cmd-page_smoke", "tools/page_smoke.py --unit LX1 --pages <page>, one page per run, run sequentially", "index.html, L01.html, L02.html",
    f"'page_smoke modules/LX/LX1/index.html: PASS', '...L01.html: PASS', '...L02.html: PASS', each followed by 'page_smoke LX1: PASS'; lab lab-LX1-L01-1 0.0 s and lab-LX1-L02-1 0.0 s ({O}/page_smoke_index.txt, {O}/page_smoke_L01.txt, {O}/page_smoke_L02.txt).")
row("LX1a-cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental on tests/labs/LX1", "tests/labs/LX1",
    f"ruff check 'All checks passed!' ({O}/ruff_labs.txt); ruff format --check '7 files already formatted' ({O}/ruff_format_labs.txt); mypy 'Success: no issues found in 7 source files' ({O}/mypy_labs.txt).")
row("LX1a-cmd-pytest", "pytest -q -k 'lab or page or LX1 or dag or project or embed or refs' tests", "the tests selected by -k across tests/",
    f"Exit 0, all progress dots, no failures ({O}/pytest_relevant.txt).")
row("LX1a-cmd-verify_refs-live", "tools/verify_refs.py --unit LX1", "references/references.json: friedman1963monetary, eichengreen1992golden, garber2000famous",
    f"'live re-verification of LX1: 3 of 560 entries, 0 problems', exit 0 ({O}/verify_refs_unit.txt). reinhart2009this is not in this run (used_by E9); it was re-resolved by plain curl, see LX1a-claim-registry-records.")
row("LX1a-cmd-verify_refs-offline", "tools/verify_refs.py --offline", "references/references.json (whole registry integrity)",
    f"'offline integrity: 560 entries, 0 problems', exit 0 ({O}/verify_refs_offline.txt).")
row("LX1a-cmd-fetch_data-check", "tools/fetch_data.py --check", "course/assets/data/market/MANIFEST.json, fx_monthly.csv",
    f"'fetch_data: 3 datasets, 0 problems', exit 0 ({O}/fetch_data_check.txt). The live rebuild of the fx_monthly sha256 (fetch_data --fetch in a scratch copy) belongs to the L04 slice and was not run here.")
row("LX1a-cmd-mutate_graders", "tools/mutate_graders.py --unit LX1 --seeds 0-9", "LX1 has no grader (course/modules/LX/LX1 holds cards.json, index.html, L01-L04, project.html; no grader/)",
    f"Exit 0 with no output ({O}/mutate_graders_unit.txt). Mutation testing applies to project graders only (verifier ruling), and LX1 has none, so this slice contributes no grader mutants.")

# ---- labs
row("LX1a-lab-L01-1", "lab twin, page code, expected block, SIMULATED label, seed, no network, runtime",
    "course/modules/LX/LX1/L01.html lines 130-283 (section lab-LX1-L01-1); tests/labs/LX1/lab-LX1-L01-1.py",
    f"page_twin_check_r3.py: page data-run code equals the twin (True); expected block equals twin stdout, 38 lines each (True); exit 0, stderr 0 bytes ({O}/page_twin_check_r3.txt). Seed SEED = 20261103 (twin line 159); imports math, random, fractions only; no file or network. SIMULATED label at L01 line 131. Printed values recomputed independently in numbers_check_r3.py (wedge path, gaps, counts 9 of 13 and 13 of 13, largest gap 2175 at t = 9): all PASS ({O}/numbers_check_r3.txt). Runtime 0.0 s (page_smoke_L01).")
row("LX1a-lab-L02-1", "lab twin, page code, expected block, SIMULATED label, seed, no network, runtime",
    "course/modules/LX/LX1/L02.html lines 133-301 (section lab-LX1-L02-1); tests/labs/LX1/lab-LX1-L02-1.py",
    f"page_twin_check_r3.py: page code equals the twin (True); expected block equals twin stdout, 41 lines each (True); exit 0, stderr 0 bytes ({O}/page_twin_check_r3.txt). Seed 20261104; index path, real values, falls and rises (6 and 6, equal sets), largest rise 42236 at t = 12, telescoped ratio 1.055909 all recomputed exactly in numbers_check_r3.py ({O}/numbers_check_r3.txt). SIMULATED label at L02 line 134. Runtime 0.0 s (page_smoke_L02).")

# ---- numbers in prose
row("LX1a-num-L01-closed-form-sums", "prose numbers vs unrounded values and displayed digits",
    "L01.html lines 87, 120, 132, 246-248, 282 and Theorem 1.3 (line 74)",
    f"Recomputed with Fraction in numbers_check_r3.py: F_0 = 20000/3 cents, rounds to 6667; q = 103/109; N = 10 sum rounds to 2882, residual F_0 q^10 = 3784.57 rounds to 3785; N = 60 sum 6444, residual 223.13 rounds to 223; N = 200 sum 6667, residual 0.08 rounds to 0; identity S_N = F_0(1 - q^N) exact for N = 10, 60, 200 ({O}/numbers_check_r3.txt).")
row("LX1a-num-L01-prop22-witness", "numerical witness in Proposition 2.2 and its misconception",
    "L01.html line 120 (witness), lines 321 and 463 (misconception 1, quiz item 8)",
    f"F_0(1%) = 400/0.08 = 5000; F_0(3%) = 400/0.06 = 20000/3 = 6666.67; at P_0 = 6000 the gaps are +1000 and -2000/3 ({O}/numbers_check_r3.txt: 'witness' checks PASS).")
row("LX1a-num-L01-canon-breaks-367", "quoted PV of a non-constant-growth stream",
    "L01.html line 310 (Section 5 bullet 2) and line 322 (misconception 2)",
    f"400/1.09 = 40000/109 = 366.97, rounds to 367; closed form at g = 3% gives 6667 (PASS in {O}/numbers_check_r3.txt).")
row("LX1a-num-L01-lab-counts", "lab counts stated in prose vs printed output",
    "L01.html lines 132, 282, 364-367, 400 (key results row 5); expected block lines 264-265 and 280-281",
    f"Part B positive gaps 9 of 13 and largest gap 2175 at t = 9; Part C 13 of 13; gap list equals the expected block; 'the count changes' True (PASS in {O}/numbers_check_r3.txt; twin_L01.txt tail shows 'True').")
row("LX1a-num-L01-empirical-shares", "shares, ratios and bases in Empirical 1-3 and Research 1",
    "L01.html lines 363, 367, 371, 378",
    f"Empirical 1: 9/13 = 0.6923; Empirical 2: 13 - 9 = 4; Empirical 3: 2175/8698 = 0.250057 gives 25.01 percent on the printed base, and F_9 = 400 x 1.03^9/0.06 = 8698.4879 gives 8698.49, so 0.25 x F_9 = 2174.62 and the exact gap is 25.00 percent (PASS in {O}/numbers_check_r3.txt). Research 1: g* = 0.09 - 400/6000 = 0.023333 = 2.33 percent (PASS).")
row("LX1a-num-L01-mechanics", "worked solutions of Mechanics 1-3",
    "L01.html lines 332-341",
    f"Mechanics 1: 250/0.06 = 12500/3 = 4166.67, rounds 4167; Mechanics 2: 1.04^3 = 1.124864, 281.216/0.06 = 4686.93, rounds 4687; Mechanics 3: 100/1.05 = 2000/21 per term, ten terms 20000/21 = 952.38 (PASS in {O}/numbers_check_r3.txt).")
row("LX1a-num-L01-quiz-numeric", "numeric quiz items and their tolerances",
    "L01.html lines 418-436",
    f"6666.67 (tol 0.01 vs exact 6666.6667); 7072.67 (tol 0.01 vs exact 7072.6667, rounds 7073); 0.944954 (tol 1e-6 vs 0.94495413); 0.023333 (tol 1e-6 vs 0.0233333) (PASS in {O}/numbers_check_r3.txt).")
row("LX1a-num-L02-real-values", "real values, one-period ratios and worked solutions",
    "L02.html lines 338-358 (M1-M3), 396-400 (E2), 443 and 474-483 (quiz items 3, 4)",
    f"Part B real values recomputed exactly and equal the expected block (13 values); M1: 2000 x 100/80 = 2500; M2: 90/85 = 18/17 = 1.0588235294; M3: 200000/95 = 2105.26 rounds 2105; E2: 1000000 x 100/99 = 1010101.0101, rounds 1010101 (PASS in {O}/numbers_check_r3.txt).")
row("LX1a-num-L02-counts", "period counts, largest rise, horizon ratio and printed index",
    "L02.html lines 300, 319, 390-392, 404-406, 443, 446, 494-496",
    f"Part C: 6 falling and 6 rising periods, both sets [1, 5, 6, 8, 9, 12]; largest one-period rise 42236 cents at t = 12 (steps recomputed); V_12/V_0 = 1.055909353 rounds to 1.055909. Problem E3: the printed index P_12 = 94.7051 and the unrounded 94.7050991475 agree with the page's 94.70509914 ... as a truncation to eight decimals (the page writes an ellipsis); 100/94.70509914 = 1.05590935 and 100/94.7051 = 1.0559093, both 1.055909 to six decimals (PASS in {O}/numbers_check_r3.txt).")
row("LX1a-num-hub-placement", "placement items, answers, tolerances and category counts",
    "index.html lines 73-151",
    "Ten items: prerequisite items P0.1 (1), E1 (1), M1 (2), M2 (1), E5 (2), FC1 (1) = 8, plus two skill checks (data-skill). Numeric answers 1000 (perpetuity 100/0.10), 0.1 (110/100 - 1), 100 (10050 - 9950), 800 (1000/1.25) recomputed. Mastery bar 0.8 = eight of ten (line 75). Quiz derivative item is the fifth item, as line 66 says.")
row("LX1a-num-hub-hours", "hours arithmetic across hub and lessons",
    "index.html lines 29, 40-43, 184-196; L01.html and L02.html line 2 (data-hours=10)",
    "data-hours-lessons=40 and data-hours-project=10 sum to 50; split 80% and 20%; four lessons of 10 h each (cards on lines 158-161); hours table rows 1 + 1 + 2 + 1.5 + 2.5 + 2 = 10 with total row 10 (lines 188-194); rung 1 row now reads 'One solved SIMULATED comparison of two price paths' (line 188).")

# ---- maths
row("LX1a-math-L01-thm1.3", "theorem, hypotheses, proof, key formula",
    "L01.html lines 55-61 (Assumption 1.1), 63-68 (Definition 1.2), 70-75 (Theorem 1.3, grade T on the title), 77-85 (proof)",
    "Hypotheses (A0) r > g and 1 + g > 0, (A1) d_s = d_1(1+g)^{s-1}. Re-derived: d_{t+k}/(1+r)^k = d_1(1+g)^t q^{k-1}/(1+r); finite geometric sum with 1 - q = (r - g)/(1+r) > 0 so q != 1; 0 < q < 1 so q^N -> 0; S_N(t) = F_t(1 - q^N) exact for every N >= 1 and t >= 0. Grade T is correct for a proof on the page.")
row("LX1a-math-L01-prop1.4", "proposition, hypotheses, proof",
    "L01.html lines 89-97 (Proposition 1.4, grade T on the title)",
    "Hypotheses (A1) with d_1 > 0 and 1 + g > 0, and (A2) r > -1 and g >= r. Proof: q = (1+g)/(1+r) >= 1 because 1 + g >= 1 + r > 0; each term d_1 q^{k-1}/(1+r) >= d_1/(1+r) > 0; S_N(0) >= N d_1/(1+r) -> infinity. Complete with the stated hypotheses.")
row("LX1a-math-L01-prop2.2", "proposition, hypotheses, conclusion, proof",
    "L01.html lines 108-121 (Proposition 2.2, hypotheses (A3) and (A4) at lines 110-113, grade T on the title)",
    "Hypotheses (A3) d_1 > 0 and (A4) both growth rates satisfy r > g and r > g', 1 + g > 0, 1 + g' > 0, g < g'. Conclusion F_0(g) < F_0(g') and the sign statement for F_0(g) < P_0 <= F_0(g'). Proof: r - g > r - g' > 0, reciprocals reversed, multiply by d_1 > 0. Every hypothesis used is listed.")
row("LX1a-math-L01-problems", "problem set: Mechanics, Proof, Empirical, Research (three each, worked solutions)",
    "L01.html lines 327-389 (details.solution blocks)",
    "Mechanics 1-3, Proof 1-3, Empirical 1-3, Research 1-3 each have a full worked solution in details.solution. Re-derived: Proof 1 (reciprocal monotonicity), Proof 2 (F_t = (1+g)F_{t-1}), Proof 3 (q > 1 when g > r, terms tend to infinity), Research 3 (three inputs). Numeric solutions are in the LX1a-num rows.")
row("LX1a-math-L02-prop1.2", "proposition, hypothesis, proof, remark",
    "L02.html lines 55-78 (Definition 1.1, Proposition 1.2 with hypothesis (A1), proof, Remark 1.3)",
    "(A1) the issuer keeps the parity at every date. Proof: one unit buys kappa grams, so one gram costs 1/kappa units at each t. Grade T correct. Remark 1.3 (conclusion holds whatever P_t path) follows from the proof, which never uses P_t.")
row("LX1a-math-L02-prop2.1-cor3.2", "proposition, hypotheses, proof (a) and (b), corollary and its proof",
    "L02.html lines 86-99 (Proposition 2.1), 113-124 (Corollary 3.2)",
    "Hypotheses (A2) D a fixed positive integer number of cents, (A3) P_t > 0. (a) V_t/V_{t-1} = P_{t-1}/P_t: D P_0 cancels. (b) For every H >= 1, V_H/V_0 = P_0/P_H: product over t = 1..H telescopes on both sides. The round-2 fault (the proof used T, not H) is fixed: line 98 now uses H throughout. Corollary 3.2: V_t > V_{t-1} iff V_t/V_{t-1} > 1 iff P_{t-1} > P_t, using V_{t-1} > 0 and P_t > 0.")
row("LX1a-math-L02-problems", "problem set: Mechanics, Proof, Empirical, Research (three each, worked solutions)",
    "L02.html lines 332-433",
    "M1-M3, P1-P3, E1-E3, R1-R3 each have details.solution. Re-derived: M1 2500, M2 18/17, M3 2105, P1 (cases P_t = P_{t-1}, P_t > P_{t-1}), P2 induction, P3 rescaling cancels c, E1 six negative changes at t = 1, 5, 6, 8, 9, 12, R2 real value constant at D, R3 opposite signs for the two indices.")

# ---- notation
row("LX1a-notation-L01", "every symbol vs notation/notation.json",
    "L01.html math (all \\( \\) and \\[ \\] segments); index.html; ledgers/LX1/scripts/LX1-a-r3/out/notation_scan.txt",
    "Registered symbols: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. None appears in L01 math (notation_scan.txt). F^{\\ast}_t is a local symbol, not the registered R^\\ast. Local symbols r, g, d, F, S_N, q, N, P, B, w, k are defined in the lesson where first used. Standard TeX commands (\\ge, \\sum, \\frac, \\ast) are not custom macros.")
row("LX1a-notation-L02-T", "the registered symbol T (number of return observations) used as a horizon",
    "L02.html lines 86-98 (Proposition 2.1 and proof (b))",
    f"Round-2 FAIL fixed: the statement and proof (b) now use H (lines 92 and 98). notation_scan.txt reports 'bare T in math segments: 0' for L02. Only the grade label T remains (data-grade and grade-legend spans).")
row("LX1a-notation-L02-Q", "near-collision check: plain Q against registered \\mathbb{Q}",
    "L02.html line 429 (Problem R3: second index Q_t)",
    f"The registered symbol is \\mathbb{{Q}} (risk-neutral measure, AP1). Problem R3 uses the plain letter Q for an index, which is a different TeX symbol and does not take the registered meaning. Reading note only; not a collision under the registry's TeX identity ({O}/notation_scan.txt).")
row("LX1a-notation-hub", "every symbol vs notation/notation.json on the hub",
    "index.html lines 73-151 (placement), 61 (prerequisite closure set)",
    f"Hub math uses only \\sum, \\ge, \\ln and single letters k, r, t, D, P, x; no registered symbol is used ({O}/notation_scan.txt).")

# ---- DAG
row("LX1a-dag-links", "concept links only to the prerequisite closure or to earlier lessons",
    "index.html lines 63-68; L01.html line 37 and dfn lines 65, 105, 289; L02.html line 37 and dfn lines 57, 82, 110",
    f"check_dag LX1: PASS ({O}/check_dag.txt). L01 links growing-perpetuity, present-value, geometric-series, exponential-and-logarithm (M1) and price-index-inflation (E5 in L02) only; no link to a later lesson.")
row("LX1a-dag-outside-closure", "concepts used outside the prerequisite closure, by name or link",
    "index.html, L01.html, L02.html (grep of D1-D15 names in the plan section 4)",
    f"Grep for bank run, fire sale, leverage cycle, banking crisis, currency crisis, covered or uncovered interest parity, efficient markets, moral hazard, Fisher relation, bank reserves, central bank, credit default, contagion, term spread, sovereign, deposit insurance, default: no hits in the three pages ({O}/text_checks.txt).")
row("LX1a-dag-defined-once", "each concept defined once, in its assigned lesson",
    "L01.html def-speculative-bubble (line 105), def-financial-panic (line 289); L02.html def-gold-standard (line 57), def-debt-deflation (line 110)",
    "Each id appears in one dfn only; the hub defines nothing; L02 introduces gold-standard by link to its own §1. check_dag LX1: PASS.")

# ---- structure and prose
row("LX1a-struct-hub", "hub sections, objectives, minimum counts, hours and reading",
    "index.html: objectives (six measurable verbs, lines 49-56), prerequisites (59-71), placement (73-152, ten items), lessons (154-163, four cards), ladder (165-174, four rungs), data (176-180), hours (182-197), reading (199-208)",
    "All required sections present; check_pages LX1: PASS. Section order is objectives, prerequisites, placement, lessons, ladder, data, hours, reading; the built precedent hubs (FC1, E5) use the same order without a separate hours section. BUILDER_RULES 4.1 lists the hub's contents, not an order, so this is recorded as no finding.")
row("LX1a-struct-L01-L02", "lesson structure in BUILDER_RULES 4.2 order, minimums and quiz size",
    "L01.html and L02.html",
    "Why it matters: L01 119 words, L02 102 words (limit 120). Core sections with Definition, Theorem or Proposition, Proof and Remark blocks; one inline lab per lesson, placed in the argument (L01 line 130, L02 line 133); 'Where the canon breaks' section (L01 lines 306-316, L02 lines 303-312); misconceptions 3 each (L01 lines 318-325, L02 lines 314-330); three problems in each of four tiers each with details.solution; key-results table; quiz with 10 items each with explain blocks (L01 lines 406-484, L02 lines 452-531).")

# ---- prose checks
row("LX1a-prose-banned", "banned phrases and ellipses (BUILDER_RULES 1.3-1.4)", "index.html, L01.html, L02.html",
    f"text_checks.txt 'banned' section: no TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, or an ellipsis outside code. No unicode ellipsis in the three pages.")
row("LX1a-prose-process-words", "process words in learner-visible text", "index.html, L01.html, L02.html",
    f"text_checks.txt 'process words' section: no builder, build, verifier, verify, verified, REQUEST, planner, fixer, unit report, ledger, checkout or pin in learner text.")

# ---- claims and attributions
row("LX1a-claim-E5-prop1.7", "placement explanation cites E5 Proposition 1.7",
    "index.html line 130 vs course/modules/E/E5/L01.html lines 93-94",
    "E5 Proposition 1.7 'closed-economy saving equals investment': S_p + S_g = I under a closed economy (X = M = 0). The hub says private plus public saving equals investment in a closed economy. Consistent. E5 title checked at course/modules/E/E5/index.html line 32.")
row("LX1a-claim-registry-records", "citations match registry records (title, author, year) and live resolution",
    "index.html lines 201-207; L01.html line 303 and line 489; L02.html lines 535-537; references/references.json",
    f"verify_refs --unit LX1 live: 3 entries (friedman1963monetary, eichengreen1992golden, garber2000famous) 0 problems. reinhart2009this re-resolved with plain curl of the Crossref record for 10.1515/9781400831722: HTTP 200, title 'This Time Is Different', subtitle 'Eight Centuries of Financial Folly', authors Reinhart and Rogoff, year 2009 ({O}/external_checks_r3.txt). Page strings match the registry: Garber title and year; Friedman 1867-1960 (1963) with the key only (no second author, plan N2); Eichengreen title in L02 identical to the registry, the hub title differs only in capitalisation and dash.")
row("LX1a-claim-attribution-readings", "no passage or figure attributed to an unread source",
    "L01.html lines 303-304 and 489; L02.html lines 535-537; index.html lines 199-208",
    "Each work is cited for its title or registry key only; the hub and L02 say no passage has been read; no page, table or quotation is attributed. Core reading flagged optional for Reinhart and Rogoff (plan 7.1 allows reading-list use).")
row("LX1a-claim-fed-licence", "licence quote and redistribution grant for fx_monthly",
    "index.html lines 178 (Data status); tools/data_sources.yaml lines 57-60; course/assets/data/market/MANIFEST.json licence and licence_url",
    f"Plain curl of https://www.federalreserve.gov/disclaimer.htm: HTTP 200 and the page contains 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission.' The hub quotes this sentence verbatim; MANIFEST and data_sources.yaml carry the same licence text ({O}/external_checks_r3.txt; {O}/licence/disclaimer.htm).")
row("LX1a-claim-fx-note-blanks", "fx_monthly note: spot-only, euro from 1999, GBP has no blank cells",
    "index.html lines 178-179; tools/data_sources.yaml lines 62-64; course/assets/data/market/fx_monthly.csv",
    "CSV: 669 rows, 1971-01 to 2026-09; EUR blank in 336 rows, first non-blank 1999-01; GBP blank in 0 rows, so Lesson 4's GBP choice holds. data_sources.yaml note: 'Each value is the last noon rate of its month ... The euro starts in January 1999. Spot rates only.' Matches the hub.")
row("LX1a-claim-hub-no-other-series", "no historical gold, price, output, unemployment or bank-failure series is embedded",
    "index.html line 179; course/assets/data/market/MANIFEST.json (3 datasets)",
    f"MANIFEST holds fx_daily, fx_monthly and ust_daily only ({O}/fetch_data_check.txt). None is a gold, price, output, unemployment or bank-failure series. The Lesson 3 honest-pending note (L03.html line 76) states the same.")
row("LX1a-claim-P0.1-not-released", "P0.1 is not yet released and its links say so",
    "index.html lines 35, 61, 68; course/concepts.html",
    "No course/modules/P directory exists. course/concepts.html contains the 'not yet released' text 806 times, including the P0.1 entry (line 34-35 section).")
row("LX1a-claim-simulated-labels", "every generated-number lab carries SIMULATED",
    "L01.html line 131; L02.html line 134; index.html lines 37, 169; L03.html line 148 (cross-check)",
    "Lab headings carry SIMULATED; the hypothesis lines and interpretations say the path is seeded and does not describe any economy. The real-data lab (L04) and the project's rung 3 are outside this slice.")
row("LX1a-claim-hub-math-prereqs", "hub prerequisite closure and concept list",
    "index.html lines 61-68",
    "Closure {E1, E5, FC1, M1, M2, P0.1} equals the plan's computed closure (plans/LX1-build-plan.md section 0.1). Each bullet's concept is used in the lessons the bullet names (price index in L02; growing perpetuity, present value and geometric series in L01; exp and log in L01; derivative in placement item 5; comparative statics in placement item 2; FC1 bid-ask spread in placement item 8).")
row("LX1a-hub-L03-concept-claim", "hub prerequisite bullets vs the concepts the lessons use (E5 out-of-closure concepts)",
    "index.html lines 53-55, 62-69; L03.html and L04.html grep",
    "L03 and L04 contain no 'national account' or 'business cycle' (grep count 0 in each), so the hub's prerequisite list is complete for the built lessons. Hub objectives 4 and 5 describe L03 and L04 content, which those slices verify.")
row("LX1a-hub-fc1-title", "hub link text for FC1", "index.html line 35",
    "FC1 index h1 at course/modules/FC/FC1/index.html line 32 reads 'The Financial System, Markets & Instruments'; the hub link text matches.")
row("LX1a-hub-fx-one-lab", "the hub's one-embedded-series claim", "index.html lede (33), meta row (37), Data status (178)",
    "Only fx_monthly is embedded for LX1 (MANIFEST; plan 0.3 B1). It is read by L04 (plan section 3) and by project lab-LX1-project-3 (data-files attribute, project.html line 281). The rung-3 project lab is outside this slice.")
row("LX1a-hub-derivative-claim", "hub claim that M2 derivative is tested by placement question 5", "index.html line 66 and placement item 5 (lines 109-117)",
    "Item 5 asks for the derivative of ln x (answer 1/x, marked data-correct).")
row("LX1a-hub-historian-regulator", "no historian or regulator process words in the hub or lessons", "index.html, L01.html, L02.html",
    f"text_checks.txt: no match.")

# ---- lesson-level claims
row("LX1a-L01-usual-first-test", "why-it-matters opens with the lesson's claim and nothing else", "L01.html line 51",
    "119 words, no motivational opener or rhetorical question; the text states the lesson's three claims (benchmark, growth-rate sign, panic by mechanism) and the lab, and carries the panic wording of Definition 3.1 ('a sudden demand for money or safe assets').")
row("LX1a-L01-gap-integer-cents", "gap units and rounding rule", "L01.html lines 105 (Definition 2.1), 132 (lab hypothesis)",
    "The gap is measured in cents and the lab reports whole cents; rounding is half up, applied once to each exact value, and each printed gap is the difference of two rounded values. Recomputed in numbers_check_r3.py.")
row("LX1a-L01-prop22-unnumbered-assumptions", "Proposition 2.2 hypotheses listed before the statement", "L01.html lines 109-115",
    "Hypotheses (A3) and (A4) are numbered and listed before the statement. The proof uses only d_1 > 0 (A3), r > g, r > g', 1 + g > 0, 1 + g' > 0 and g < g' (A4).")
row("LX1a-L01-only-quantitative-tool", "scope statement of L01 Section 4 (no claim beyond sources read)", "L01.html lines 303-304",
    "Section 4 claims no episode, date, price or outcome (no source read); it states the empirical question is not answered here. The only computation is Lab 1, which is labelled SIMULATED. No 'only' claim is made about the lesson's tools.")
row("LX1a-L02-prop12-no-lab-check", "Proposition 1.2 is not claimed as checked by the lab beyond Part E",
    "L02.html lines 62-68 (Proposition 1.2), 300 (interpretation), 443 (key results row 1)",
    "Lab Part E checks 1/kappa at one parity; the interpretation states the lab does not test (A1), that the parity holds at every date. Key results row 1 says 'Proved in §1, under (A1)'.")
row("LX1a-L02-CU-undefined", "undefined abbreviation CU", "L02.html lab text and twin tests/labs/LX1/lab-LX1-L02-1.py",
    f"text_checks.txt 'CU (expect none)': no CU token in any slice page or the L01 or L02 twin; the lab says 'currency units' in full.")
row("LX1a-L02-misconception-gold-price", "misconception 2 consistent with the code",
    "L02.html line 323 (misconception 2) vs tests/labs/LX1/lab-LX1-L02-1.py Parts A-E",
    "Round-2 FAIL fixed. The line now says the index path of Parts A to D is not linked to the gold price that Part E computes. Code: Parts A-D use no kappa; Part E uses only kappa = 2/5. The index changes in each of its twelve periods (changes list has no zero). The claim and the evidence agree.")
row("LX1a-hub-E5-title", "hub link text for E5 matches the E5 hub", "index.html line 35 vs course/modules/E/E5/index.html lines 6 and 32",
    "Round-2 FAIL fixed. Hub text 'E5 Macroeconomics I: Aggregates, Cycles & Policy' equals the E5 h1 'Macroeconomics I: Aggregates, Cycles & Policy' with the E5 prefix.")
row("LX1a-hub-hours-rung1", "rung 1 hours row consistent with the ladder and project", "index.html lines 169 (ladder item 1), 188 (hours row); project.html lines 44 and 452",
    "Round-2 FAIL fixed. Hours row 'One solved SIMULATED comparison of two price paths' matches ladder item 1 ('over two SIMULATED price paths, periods 0 to 5') and project.html line 452 ('One solved SIMULATED comparison').")
row("LX1a-hub-objective-panic", "objective 2 matches Definition 3.1 and Remark 3.2", "index.html line 51 vs L01.html lines 289 and 294",
    "Round-2 FAIL fixed. Objective 2 now says the bubble definition depends on a stated assumption and the panic definition rests on its mechanism alone; Definition 3.1 says 'The definition names the mechanism only', and Remark 3.2 states the two definitions use different objects.")
row("LX1a-twin-page-equality", "page code and expected block equal the twins", "L01.html lines 133-244; L02.html lines 136-299; tests/labs/LX1/lab-LX1-L01-1.py and lab-LX1-L02-1.py",
    f"page_twin_check_r3.py ({O}/page_twin_check_r3.txt): code equal after the final newline (True for both); expected blocks equal twin stdout (38 and 41 lines, True).")

row("LX1a-data-figures", "figures and charts in the slice (BUILDER_RULES 6.4; VERIFIER 2.8)",
    "index.html, L01.html, L02.html (grep for svg, class=\"chart\", data-figures, data-files)",
    "Grep count 0 for each token in the three pages: the slice has no figure or chart and no live figure. The lab sections (L01.html line 130, L02.html line 133) carry data-runtime only and read no data file, so no dataset licence or source line is owed in this slice.")
row("LX1a-scope-words", "scope words need a computation, a proof or an explicit hypothesis (VERIFIER 2.9, rule 4)",
    "index.html, L01.html, L02.html (grep for only, every, all, always, never, any, same, exactly, drives)",
    "Each universal statement is proved or checked: Theorem 1.3 for every t >= 0 and N >= 1 (proof lines 79-84); Proposition 2.1 for every path under (A3) (proof lines 97-98); Corollary 3.2 for every t >= 1 (proof 123); Proposition 2.2 for every P_0 in the stated interval (proof 119); 'every run prints the same lines' is the seed claim (L01.html lab docstring, line 137). The 'only' uses (L02 lines 60, 491; L01 line 381) are conditional on a named hypothesis or describe a method. No claim of coverage beyond the episodes read (L01 Section 4).")

# ---- round-3 scope rows
row("LX1a-r3-full-read", "every line of the slice read", "index.html (213 lines), L01.html (501 lines), L02.html (550 lines), both twins",
    "Read in full in this round, in chunks, including the head of L02 (lines 1-29). Twins read with the page code compared by script.")
row("LX1a-r3-delta", "round delta since 67c47689 for the slice files", "course/modules/LX/LX1/index.html, L01.html, L02.html; twins",
    "git diff 67c47689 67a2d13e: index.html 12 lines (E5 prerequisite text, objective 2, FC1 and E1 bullet closings, L02 card text, rung 1 hours row), L01.html 10 lines (why-it-matters, Prop 1.4 remark, Lab 1 hypothesis, Research 2 solution, Key results row 6), L02.html 8 lines (Prop 2.1(b), Def 3.1, misconception 2 and 3). Twins unchanged in the delta. Every hunk was read and re-verified (rows above).")

fragment = {
    "unit": "LX1",
    "slice": "LX1-a",
    "round": 3,
    "verifier": "Haiku independent verifier, LX1 slice a, round 3 (did not build LX1)",
    "pin": "67a2d13e",
    "base": "67c47689 (round-2 pin; delta computed with git diff 67c47689 67a2d13e)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE3-LX1-a (detached at 67a2d13e, .venv symlinked)",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE3-LX1-a/ledgers/LX1/scripts/LX1-a-r3/out",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "friedman1963monetary: registry record lists Friedman as the only author (plan N2). Pages cite the key only and do not type Schwartz. Any correction is an add_reference.py change by the architect.",
        "reinhart2009this: registry used_by is E9, not LX1. The hub lists it as optional core reading, which plan 7.1 permits. verify_refs --unit LX1 does not re-resolve it; it was re-resolved this round by plain curl (external_checks_r3.txt).",
    ],
    "freshness_flags": [],
    "notes": [
        "Slice = hub index.html, L01.html, L02.html, tests/labs/LX1/lab-LX1-L01-1.py and lab-LX1-L02-1.py. Full read of all four files in this round.",
        "Round-2 non-PASS rows (LX1a-notation-L02-T, LX1a-L02-misconception-gold-price, LX1a-hub-E5-title, LX1a-hub-hours-rung1, LX1a-hub-objective-panic) were re-derived from scratch and now PASS; their fixes are cited in their rows.",
        "LX1 has no grader and no grader mutants (verifier ruling; plan section 5.4 rubric-only). Lab twins are demonstrations. mutants is empty by design.",
        "Notation: assumption labels (A0)-(A4) are numbered per lesson; L01 and L02 both use (A1) for different hypotheses. Not a registered-symbol collision.",
        "Reading notes (not findings): the hub writes Eichengreen's title in title case and with an en dash, while the registry record is lower case with a hyphen; the page's title and year match. project.html line 275 describes fx_monthly as 'month-end' exchange rates, while the MANIFEST note says 'last noon rate of its month'; this is outside the slice and is for the project slice's verifier to read.",
        "Not checked here: L03 and L04 pages and labs, project.html and its labs, cards.json, the live rebuild of the fx_monthly sha256 (fetch_data --fetch in a scratch copy), the cross-slice concept grids for L03 and L04 (their own slices).",
        "The Crossref request was plain curl with no personal data and no contact address. The Federal Reserve page was fetched once with plain curl (HTTP 200). No bot check, login or paywall was touched.",
    ],
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
        "commands_run": [
            "run_cmds.sh: check_pages, check_dag, check_projects, run_labs, twin L01 and L02 with python -I -W error, ruff check, ruff format --check, mypy --no-incremental, verify_refs --unit LX1, verify_refs --offline, fetch_data --check, pytest -k subset, page_smoke (index, L01, L02, sequential), mutate_graders --unit LX1",
            "numbers_check_r3.py (independent Fraction recomputation of L01 and L02 numbers and the twins' printed values)",
            "page_twin_check_r3.py (page code vs twin; expected block vs twin stdout)",
            "notation_scan.py, text_checks.sh (prose, banned strings, process words, notation, outside-closure names, why-it-matters word counts)",
            "external_checks_r3.sh (plain curl: federalreserve.gov/disclaimer.htm; Crossref record for reinhart2009this)",
        ],
        "scripts": [
            f"{S}/run_cmds.sh",
            f"{S}/numbers_check_r3.py",
            f"{S}/page_twin_check_r3.py",
            f"{S}/notation_scan.py",
            f"{S}/text_checks.sh",
            f"{S}/external_checks_r3.sh",
            f"{S}/make_fragment_r3.py",
        ],
    },
}

with open("ledgers/LX1/LX1-a.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), "verdict", fragment["verdict"])
