"""Writes the round-5 verifier fragment for LX1 slice b (L03, L04 and their lab twins).

Every row cites the file, line, command or script output that backs it; the scripts live in
ledgers/LX1/scripts/LX1-b-r5/. Run with: python3 -I write_fragment_r5.py <checkout>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
S = "ledgers/LX1/scripts/LX1-b-r5/"
CARRY_FX = (
    "Carried from round 4 (course/assets/data/market/fx_monthly.csv, course/assets/data/market/MANIFEST.json, "
    "tools/fetch_data.py and tools/data_sources.yaml are byte-identical since the previous pin 9a02b1af: "
    "git diff --quiet 9a02b1af 7376a5e over them is empty): the round-3 live rebuild (fetch_data --fetch in a "
    "scratch copy, bytes equal the snapshot) is in /Users/billyribeiro/.fanout/frags/E-LX1-b.round3.json, row "
    "lx1b-fx-rebuild. "
)

rows = [
    dict(id="lx1b-check-pages", check="gate", location="course/modules/LX/LX1/L03.html; course/modules/LX/LX1/L04.html",
         status="PASS",
         evidence="Re-run on 7376a5e: tools/check_pages.py --unit LX1 --page L03 -> 'check_pages LX1 L03: PASS' exit 0; "
                  "--page L04 -> 'check_pages LX1 L04: PASS' exit 0; unit-wide -> 'check_pages LX1: PASS' exit 0 (" + S +
                  "gates_pages_dag.out)."),
    dict(id="lx1b-check-dag", check="gate", location="course/modules/LX/LX1/L03.html; course/modules/LX/LX1/L04.html",
         status="PASS",
         evidence="Re-run: tools/check_dag.py --unit LX1 -> 'check_dag LX1: PASS' exit 0 (" + S + "gates_pages_dag.out). "
                  "The rule it applies (tools/check_dag.py lines 73-75) is the one behind lx1b-L04-bretton-definition."),
    dict(id="lx1b-dag-links", check="dag", location="L03.html:37, :54, :90; L04.html:37, :105, :329",
         status="PASS",
         evidence="scan_r5.py over both pages (" + S + "scan_r5.out): L03 links L02.html#def-debt-deflation and "
                  "L02.html#def-gold-standard, both ids present in L02.html; L04 links L02.html#def-gold-standard and "
                  "L03.html#def-lender-of-last-resort (dfn at L03.html:390), both present; L04 links "
                  "../../../concepts.html#exponential-and-logarithm, whose owner is M1 (curriculum/curriculum.json "
                  "concept entry), inside the closure {E1, E5, FC1, M1, M2, P0.1}. No link to a later lesson."),
    dict(id="lx1b-dag-outside-closure", check="dag", location="L03.html:51, :65, :90, :395, :414; L04.html:326",
         status="PASS",
         evidence="scan_r5.out: 'balance sheet' occurs 3 times in L03 as plain prose with no data-concept, link or dfn; "
                  "'covered interest parity' once in L04 (line 326) as plain prose, no formula, no link. None of the "
                  "D1-D15 names of plan section 4 is linked or defined in either page. Plan section 4 resolution: plain prose."),
    dict(id="lx1b-run-labs", check="lab", location="tests/labs/LX1/lab-LX1-L03-1.py; tests/labs/LX1/lab-LX1-L04-1.py",
         status="PASS",
         evidence="Re-run: tools/run_labs.py --unit LX1 -> 'run_labs LX1: PASS (7/7)' exit 0; --page L03 -> 'PASS (1/1)'; "
                  "--page L04 -> 'PASS (1/1)' (" + S + "run_labs.out)."),
    dict(id="lx1b-twin-alone-L03", check="lab", location="tests/labs/LX1/lab-LX1-L03-1.py",
         status="PASS",
         evidence="Run from empty scratch /tmp/lx1b-r5/L03 with .venv Python 3.14.8: python -I -W error <twin> -> exit 0, "
                  "stderr empty (" + S + "twin_L03.err), 56 stdout lines (" + S + "twin_L03.out)."),
    dict(id="lx1b-twin-alone-L04", check="lab", location="tests/labs/LX1/lab-LX1-L04-1.py",
         status="PASS",
         evidence="Run from /tmp/lx1b-r5/L04 with data/fx_monthly.csv copied from course/assets/data/market/ (sha256 "
                  "60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e equals MANIFEST.json:42): python -I -W "
                  "error <twin> exit 0, stderr empty (" + S + "twin_L04.err), 17 stdout lines (" + S + "twin_L04.out)."),
    dict(id="lx1b-twin-equals-page-code", check="lab", location="L03.html data-run block (line 150-326); "
                                                                  "L04.html data-run block (line 113-298)",
         status="PASS",
         evidence="twin_page_compare_r5.py (" + S + "twin_page_compare_r5.out): L03 page code equals the twin after rstrip: "
                  "True; L04 True. Expected blocks equal the twin output line for line: L03 56 lines, L04 17 lines. The "
                  "L04 docstring edit (twin lines 20-26) is in both the twin and the page block."),
    dict(id="lx1b-page-smoke-L03", check="gate", location="course/modules/LX/LX1/L03.html", status="PASS",
         evidence="Re-run: tools/page_smoke.py --unit LX1 --pages L03 -> 'page_smoke modules/LX/LX1/L03.html: PASS' exit 0; "
                  "lab run 0.0 s (" + S + "page_smoke.out)."),
    dict(id="lx1b-page-smoke-L04", check="gate", location="course/modules/LX/LX1/L04.html", status="PASS",
         evidence="Re-run: tools/page_smoke.py --unit LX1 --pages L04 -> 'page_smoke modules/LX/LX1/L04.html: PASS' exit 0; "
                  "lab run 0.0 s (" + S + "page_smoke.out)."),
    dict(id="lx1b-ruff-mypy", check="gate", location="tests/labs/LX1/lab-LX1-L03-1.py; tests/labs/LX1/lab-LX1-L04-1.py",
         status="PASS",
         evidence="ruff check tests/labs/LX1 -> 'All checks passed!' exit 0; ruff format --check tests/labs/LX1 -> "
                  "'7 files already formatted' exit 0; mypy --no-incremental on both twins -> 'Success: no issues found in 2 "
                  "source files' exit 0 (" + S + "ruff_mypy.out)."),
    dict(id="lx1b-pytest", check="gate", location="tests/test_labs.py; tests/test_page_checks.py; tests/test_docs_figures.py",
         status="PASS",
         evidence="pytest tests/test_labs.py -k LX1 -v -> '7 passed, 352 deselected', exit 0 (" + S +
                  "pytest_labs_LX1_v.out). pytest tests/test_page_checks.py tests/test_docs_figures.py -q -> 55 passed "
                  "(dot count), exit 0 (" + S + "pytest_page_docs_summary.out)."),
    dict(id="lx1b-verify-refs", check="citation", location="references/references.json; L03.html data-cite friedman1963monetary",
         status="PASS",
         evidence="Re-run: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' exit 0 ("
                  + S + "fetch_verify_refs.out). Live: tools/verify_refs.py --unit LX1 -> 'live re-verification of LX1: 3 of "
                  "560 entries, 0 problems' exit 0 (" + S + "verify_refs_live_unit.out). references.json is byte-identical "
                  "since 9a02b1af."),
    dict(id="lx1b-fetch-check", check="data", location="course/assets/data/market/fx_monthly.csv; MANIFEST.json",
         status="PASS",
         evidence="Re-run: tools/fetch_data.py --check -> 'fetch_data: 3 datasets, 0 problems' exit 0 (" + S +
                  "fetch_verify_refs.out)."),
    dict(id="lx1b-fx-rebuild", check="data", location="course/assets/data/market/fx_monthly.csv; MANIFEST.json",
         status="PASS", evidence=CARRY_FX + "Re-checked this round: sha256 of fx_monthly.csv 60572240...ffe3e equals "
                                 "MANIFEST.json:42 sha256 (sha256sum)."),
    dict(id="lx1b-fx-licence", check="data", location="tools/data_sources.yaml fx_monthly; MANIFEST.json fx_monthly; "
                                                      "L04.html:112, :566",
         status="PASS",
         evidence="Plain curl -sS -L https://www.federalreserve.gov/disclaimer.htm -> HTTP 200 (" + S +
                  "disclaimer_r5.htm). The page contains the quoted grant: 'Unless otherwise indicated, information on "
                  "Board's website is in the public domain and may be copied and distributed without permission. Please "
                  "cite to the Board as the source of the information.' (grep count 1). The MANIFEST licence_url and "
                  "licence text (MANIFEST.json fx_monthly) match this quote; L04.html:566 citation string matches the "
                  "MANIFEST citation."),
    dict(id="lx1b-fx-guard", check="data", location="tests/labs/LX1/lab-LX1-L04-1.py load_column, parse_rate, month_index",
         status="PASS",
         evidence="guard_and_starts_r5.py (" + S + "guard_and_starts_r5.out) on scratch copies of the CSV: a blank GBP cell, "
                  "'1.2.3', '1.5e2' and '-1.5' at row 300 each exit 1 with ValueError naming 1995-12 and the cell; a "
                  "skipped month (1996-01) exits 1 with 'does not follow the previous month'. A renamed column was not "
                  "re-run this round; the twin's load_column header check is unchanged code (byte-identical code, only the "
                  "docstring changed)."),
    dict(id="lx1b-fx-gbp-clean", check="data", location="course/assets/data/market/fx_monthly.csv (GBP column)",
         status="PASS",
         evidence="recompute_r5.py (" + S + "recompute_r5.out): 669 rows, 1971-01 to 2026-09; blank GBP cells 0; non-decimal "
                  "GBP cells 0. The CSV is byte-identical since 67a2d13e (git diff --quiet 67a2d13e 7376a5e)."),
    dict(id="lx1b-num-L03-depth", check="numbers", location="L03.html:149, :359-362, :383, :487-491 (E1), :545-546, "
                                                             ":574-577, :593-596, :610 (quiz explanation)",
         status="PASS",
         evidence="recompute_r5.py, exact Fractions (" + S + "recompute_r5.out): depth X = 9.204597180413566 percent -> 9.20 "
                  "first at t = 12; depth Y = 2.6867131020835693 -> 2.69 first at t = 4; X minus Y unrounded 6.517884 -> 6.52; "
                  "printed 9.20 - 2.69 = 6.51 (the page's E2 and L03.html:383 say so). Ratio X/Y = 3.425969513929613 -> 3.4260 "
                  "for each of phi*beta = 1/2, 1, 3. V_12 = 1274345.2124 -> 1274345 cents."),
    dict(id="lx1b-num-L03-path", check="numbers", location="L03.html Part A expected block (lines 327-357), M1-M3 (439-455), "
                                                           "E3 (505), quiz (607-611)",
         status="PASS",
         evidence="l03_partA_r5.py (" + S + "l03_partA_r5.out): all 26 printed Part A rows (13 per economy: index, real debt, "
                  "leverage, premium, output fall) recomputed in exact Fractions with own half-up rounding: 0 mismatches. "
                  "M1: P_4 = 5764801/6250000 = 0.92236816; V_4 = 1084165.7847 -> 1084166. M2: N_4 = 3915834.2153 -> 3915834. "
                  "M3: L_4 = 0.2768671 -> 0.2769. E3: economy Y index unchanged for t = 5..12, 8 periods."),
    dict(id="lx1b-num-L04-stats", check="numbers", location="L04.html expected block (lines 299-315), interpretation (316), "
                                                           "window paragraph (319), key results (469-470), quiz (517-534)",
         status="PASS",
         evidence="recompute_r5.py with Decimal at 60 digits from the CSV (" + S + "recompute_r5.out): window one n = 668, "
                  "sd 0.0279352779 -> 0.027935; window two n = 321, sd 0.0246995014 -> 0.024700; zero-change months 1976-07, "
                  "2012-07, 2019-11 (665 nonzero); largest |change| window one 0.1358457 at 1985-03 (positive); window two "
                  "-0.0965747 at 2008-10; ratio 0.8841688 -> 0.8842; identity sum = ln(last/start) within 1e-27 both windows."),
    dict(id="lx1b-num-L04-display-diff", check="numbers", location="L04.html:316 (interpretation), :343 (misconception 2), "
                                                                   "expected line 314",
         status="PASS",
         evidence="recompute_r5.out: unrounded window two minus window one = -0.0032357765 -> -0.003236 (expected line 314, "
                  "page line 316). Subtracting the printed figures 0.024700 - 0.027935 = -0.003235; the page states that "
                  "difference (line 316)."),
    dict(id="lx1b-num-L04-derived", check="numbers", location="L04.html:366 (M1), :373 (M2), :380 (M3), :398 (P2), :423 (E2), "
                                                             ":448 (R2), quiz :531-534 and :554-557",
         status="PASS",
         evidence="recompute_r5.out: ln 1.1 = 0.0953101798 -> 0.095310; 0.1 - ln 1.1 = 0.0046898 -> 0.004690; M2 mean 1/150, "
                  "sum of squared deviations 19/15000, dispersion 0.0251661148 -> 0.025166; M3 321 changes; E2 simple change "
                  "e^(-0.09657474) - 1 = -0.0920580 -> -0.092058; R2 h = tanh(L/2) = 0.0678186 -> 0.067819, and "
                  "ln(1.0678/0.9322) = 0.1358084 -> 0.135808, below 0.135846 as stated; quiz bound 0.1358 (tolerance 0.00005)."),
    dict(id="lx1b-scope-start", check="numbers", location="L04.html:328 (window start bullet); :319; card LX1-c063",
         status="PASS",
         evidence="guard_and_starts_r5.py (" + S + "guard_and_starts_r5.out): window from 1990-01 n = 441 sd 0.026066; from "
                  "2000-01 n = 321 sd 0.024700; from 2010-01 n = 201 sd 0.024101. A different start gives a different "
                  "dispersion, as the bullet says, and the lab computes only the 2000-01 start."),
    dict(id="lx1b-math-L03", check="math", location="L03.html:96-143, :393-396, :67",
         status="PASS",
         evidence="Every proof read line by line. Lemma 3.1: y/(C-y) - x/(C-x) = C(y-x)/((C-x)(C-y)) > 0 for D <= x < y < C; "
                  "N_t = C - V_t so L_t = ell(V_t) (C = N_0 + D > 0 by Assumption 1.2). Prop 3.2(a): V_t = D(1-delta)^(-t) "
                  "strictly increasing for t <= m when m >= 1, flat after m. (b): f_t = beta phi (ell(V_t) - ell(D)) with "
                  "V_t <= V_m < C, so the maximum is f_m. (c): for t < m, V_t < V_m so f_t < f_m. Cor 3.3 and Cor 3.4 proofs "
                  "re-derived. Remark 4.2 solvency: V_m < N_0 + D gives N_t > 0. Numerically the closed form equals the path "
                  "maximum at t = m (recompute_r5.out, 'closed-form check True')."),
    dict(id="lx1b-math-L04", check="math", location="L04.html:58-107 (Definition 1.1, Prop 1.2, Remark 1.3, Definition 2.1, "
                                                   "Prop 2.2)",
         status="PASS",
         evidence="Prop 1.2 proof read line by line (L04.html:69-72): each interior ln x_t appears once with + in l_t and once "
                  "with - in l_(t+1), so the sum telescopes to ln(x_b/x_a) with b - a terms. Prop 2.2 (L04.html:97-101): "
                  "ln(kappa/kappa) = 0; dispersion sqrt(0/(n-1)) = 0 with n >= 2. Remark 1.3: the lab's check is a floating-point "
                  "check with tolerance 1e-12 (twin SUM_TOLERANCE). Identity residuals at 60 digits: 1.8e-28 and 9.4e-29 "
                  "(recompute_r5.out)."),
    dict(id="lx1b-math-problems", check="math", location="L03.html:437-530; L04.html:362-457",
         status="PASS",
         evidence="Each worked solution re-derived: L03 M1-M3 (numbers in lx1b-num-L03-path), P1 (monotone P_t, V_t), P2 "
                  "(m = 0 gives P_t = 1, depth 0), P3 (identity and strict step), E1-E3 (2.69, 2.6867, 6.517884 -> 6.52, "
                  "8 periods), R1 (no result carried over; Lemma 3.1 unaffected), R2 (strictly increasing G with V_m < C, "
                  "argument valid), R3 (no embedded series for the quantities: MANIFEST ids fx_daily, fx_monthly, ust_daily "
                  "only). L04 M1-M3 (numbers in lx1b-num-L04-derived), P1 (telescoping induction; A1 used), P2 (band bound: "
                  "|ell| <= ln((1+h)/(1-h)), h = 0 gives 0), P3 (ln(1+u) <= u, derivative sign argued correctly), E1-E3, R1-R3 "
                  "(the test and the window-start reasoning are consistent with the lab's output)."),
    dict(id="lx1b-grades", check="grades", location="L03.html:96, :107, :124, :134, :542-546; L04.html:65, :90, :467-470",
         status="PASS",
         evidence="Proved on the page and graded T: Lemma 3.1, Prop 3.2, Cor 3.3, Cor 3.4 (L03), Prop 1.2 and Prop 2.2 (L04). "
                  "Lab numbers graded C naming the lab (L03.html:545-546; L04.html:469-470). No claim graded A, B, D or X. "
                  "Model claims are stated as model results; the credit-channel claim is conditional (L03.html:82-89, :405)."),
    dict(id="lx1b-citations-L03", check="citation", location="L03.html:405 (data-cite), :640 (section 10); "
                                                              "references/references.json record friedman1963monetary",
         status="PASS",
         evidence="references/references.json record friedman1963monetary: title 'A monetary history of the United States "
                  "1867-1960', author Friedman (Milton), year 1963, Princeton University Press, status verified, "
                  "verified_by openlibrary. The page cites the key and the title only, types no second author, takes no "
                  "finding from the book (L03.html:640). grep count of 'Bernanke', 'AER', 'American Economic', '1983' in "
                  "L03.html is 0; no unread attribution."),
    dict(id="lx1b-citations-L04", check="citation", location="L04.html:564-566 (section 9)", status="PASS",
         evidence="L04.html:564 cites no registry key. L04.html:566 gives issuer, citation 'G.5/H.10 Foreign Exchange Rates "
                  "(noon buying rates in New York)', snapshot fx_monthly.csv, retrieved 2026-10-19, MANIFEST entry "
                  "fx_monthly; the MANIFEST.json fx_monthly entry has the same citation and retrieved date."),
    dict(id="lx1b-notation", check="notation", location="L03.html (271 math segments) and L04.html (149 math segments)",
         status="PASS",
         evidence="scan_r5.py against notation/notation.json (" + S + "scan_r5.out): no registered symbol (T, \\Phi, \\gamma_3, "
                  "\\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) appears; no registered macro (\\E, \\Prob, \\Var, \\R, ...) "
                  "is used. Local symbols (D, N, V, P, L, C, H, m, n, h, kappa, ell, G) are each defined on their lesson."),
    dict(id="lx1b-concepts-defs", check="dag", location="L03.html:82, :87, :390; L04.html:59, :85, :86",
         status="PASS",
         evidence="dfn ids unique in each page (scan_r5.out). L03 defines def-leverage and def-external-finance-premium "
                  "(plain), def-credit-channel-depression and def-lender-of-last-resort (data-concept), def-central-bank "
                  "(plain). L04 defines plain dfn for monthly log change, dispersion, anchor currency, parity, fixed-parity "
                  "model, and def-bretton-woods-system (data-concept; see lx1b-L04-bretton-definition)."),
    dict(id="lx1b-banned-phrases", check="prose", location="L03.html; L04.html", status="PASS",
         evidence="scan_r5.out: 0 hits for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an "
                  "exercise, you can add more, it is important to note, studies show, experts agree, well known, obviously, "
                  "clearly, it can be shown. 0 ellipses outside code."),
    dict(id="lx1b-process-words", check="prose", location="L03.html; L04.html", status="PASS",
         evidence="scan_r5.out: 0 hits for plans/, tools/, open item, D-1, B1, B2, B3, N1-N4, builder, fixer, verifier, ledger, "
                  "architect, 'round ', REQUEST. 'reference list' and 'registry' wording: 'registry' 0 hits in both pages."),
    dict(id="lx1b-structure", check="structure", location="L03.html sections 1-10; L04.html sections 1-9", status="PASS",
         evidence="check_pages PASS (gates_pages_dag.out). L03 sections 1-10 in order; L04 sections 1-9 in order, lab in "
                  "section 3. Misconceptions: 4 each. Problem tiers: 3/3/3/3 in each page. Quiz: 11 items each. Key results "
                  "table present. Each page has a references section and hours data-hours 10."),
    dict(id="lx1b-quiz-explanations", check="prose", location="L03.html quiz (lines 556-636); L04.html quiz (lines 479-560)",
         status="PASS",
         evidence="Numeric answers checked against the exact values (recompute_r5.out): L03 2.69 (exact 2.686713), 12, 3.426 "
                  "(exact 3.425970), 1274345 (exact 1274345.2124), 8; L04 3, 321, 0.027935 (exact 0.0279352779), 0.095310 "
                  "(exact 0.0953101798), 0.1358 (bound at 0.0678 = 0.1358084). Each explanation read against its lesson "
                  "section; the L03 q11 explanation matches Section 5."),
    dict(id="lx1b-honest-data", check="data", location="L03.html:76, :148; L04.html:7, :111-112, :577",
         status="PASS",
         evidence="L03 heading 'Lab 1 · SIMULATED' (:148), honest-pending note (:76). L04 Part A labelled SIMULATED in the "
                  "heading (:111), hypothesis (:112), footer (:577) and the twin's Part A header; Parts B to D read only "
                  "fx_monthly.csv (twin DATA_PATH; no other file is opened)."),
    dict(id="lx1b-E1-printed-only", check="prose", location="L03.html:487-491 (E1)", status="PASS",
         evidence="E1 says 'Using only the printed output of Lab 1, Part B'; the answer 2.69 and t = 4 are in the expected "
                  "block (lines 359-360). The exact 2.6867 is labelled as the solution's computed value (:491)."),
    dict(id="lx1b-L03-remark42-solvency", check="math", location="L03.html:395 (Remark 4.2); :67 (Assumption 1.2 text)",
         status="PASS",
         evidence="Remark 4.2 derives N_t > 0 from Prop 3.2(a) (V_t <= V_m) and V_m < N_0 + D. Numerically V_12 = 1274345.21 "
                  "< 5000000 cents = N_0 + D (recompute_r5.out, 'remark 4.2 V_12 < N0 + D')."),
    dict(id="lx1b-L03-ratio-claims", check="math", location="L03.html:404 (functional-form bullet); :523 (R2); :130 (Cor 3.3 "
                                                            "proof)",
         status="PASS",
         evidence="Bullet claim 'if the premium is phi times the square of (L_t - L_0), the ratio is the square of the Cor 3.4 "
                  "ratio': recomputed r = 3.4259695, r^2 = 11.737267, and r^2 != r (recompute_r5.out). 'A change of slope cannot "
                  "change the ratio' follows from Cor 3.4 (phi cancels). R2 solution uses V_m < C and the closed form, "
                  "consistent with the page."),
    dict(id="lx1b-L03-r1-no-result", check="math", location="L03.html:513-517 (R1)", status="PASS",
         evidence="R1 says the facility needs a case of insolvency excluded by N_t > 0 (Assumption 1.2, Remark 4.2), a term in "
                  "Assumption 1.3, that Prop 3.2 does not carry over without a new proof, and that Lemma 3.1 is unaffected. "
                  "Consistent with the model and Remark 4.2."),
    dict(id="lx1b-L04-bretton-definition", check="dag", location="L04.html:38 (meta 'Introduces'), :86 (dfn def-bretton-woods-system, "
                                                                  "'definition pending'); plans/LX1-build-plan.md:94, :143-144, "
                                                                  ":287-288, :599-601, :632-633; plans/LX1-open-items.md "
                                                                  "('Architect decision needed')",
         status="FAIL",
         evidence="The page still defines bretton-woods-system with a dfn carrying data-concept, labelled 'definition pending', "
                  "and lists it under 'Introduces'. The round-5 edit only changed 'registry source' to 'source from the course's "
                  "reference list' (L04.html:38, :86); the conflict is unchanged. The binding plan says the definition waits: "
                  "B3 gates it (plan line 94), L04 'defines bretton-woods-system last (B3 gates the definition)' (plan 143-144), "
                  "'the definition of the system is taught only after B3 is resolved' (plan 287-288), section 12 item 9 "
                  "(plan 599-601), and the binding architect line 632-633 ('the Bretton Woods definition and end date wait for a "
                  "request'). tools/check_dag.py lines 73-75 fail any introduced concept that is never defined with a dfn, so "
                  "check_dag passes only with the dfn. The builder's reading is recorded as an architect item in "
                  "plans/LX1-open-items.md, which is not yet ruled. Status unchanged from round 4.",
         fix="Architect ruling required (the verifier does not resolve a plan/tool conflict). One of: (a) confirm in the "
             "build plan that a dfn with data-concept reading 'definition pending' is the intended reading of check_dag and "
             "plan section 12 item 9, and keep the page as it is; (b) change tools/check_dag.py to accept a named deferred "
             "concept (a tool change, not a page change); (c) remove bretton-woods-system from LX1's introduces (a curriculum "
             "change, then remove L04.html:38 and :86). Until one is ruled, the page must not be changed by the builder."),
    dict(id="lx1b-L04-simulated-label", check="data", location="L04.html:7, :111, :112, :577; twin Part A header (twin line 1 "
                                                             "of output)",
         status="PASS",
         evidence="Meta description and footer say Part A is a constructed model check labelled SIMULATED; Parts B to D read the "
                  "embedded GBP column. twin_L04.out line 1 'Part A: SIMULATED model check, not data'."),
    dict(id="lx1b-L04-manifest-note", check="data", location="tests/labs/LX1/lab-LX1-L04-1.py docstring lines 3-8 (page L04.html:115-120); "
                                                             "L04.html:319",
         status="PASS",
         evidence="The docstring says each value is the column's last value in its month, as the MANIFEST transform states "
                  "('month-end (each column's last value in the month)', MANIFEST.json fx_monthly). The inversion list 'CAD, "
                  "CHF, DKK, JPY, NOK and SEK only' matches the MANIFEST transform; GBP is a direct quote. The file has no "
                  "interest-rate or forward-rate column (header read: month, AUD, CAD, CHF, DKK, EUR, GBP, JPY, NOK, NZD, SEK)."),
    dict(id="lx1b-open-items-missing", check="prose", location="plans/LX1-open-items.md", status="PASS",
         evidence="Read in full this round: D-1 (L03 data source not identified), the Bretton Woods pending definition with the "
                  "architect item, the credit-channel reference request, the Kindleberger and Aliber request, and the Friedman "
                  "and Schwartz record note. Byte-identical since the previous pin (git diff --quiet 9a02b1af 7376a5e). No "
                  "learner-facing page names it."),
    dict(id="lx1b-L04-prediction-tested", check="lab", location="L04.html:112 (hypothesis); tests/labs/LX1/lab-LX1-L04-1.py",
         status="PASS",
         evidence="grep -c for assert, sys.exit and __main__ over both twins: 0 each (run this round). The hypothesis says the printed dispersions show the prediction: Part C "
                  "prints them (expected lines 307, 310). The only printed boolean checks are 'all exactly zero: True' and the "
                  "identity booleans, as the hypothesis states."),
    dict(id="lx1b-L03-lab-checks-overreach", check="lab", location="L03.html:145, :383; tests/labs/LX1/lab-LX1-L03-1.py Parts "
                                                                    "B-D (twin lines 159, 168-169, 171-174)",
         status="PASS",
         evidence="grep -c assert and sys.exit over lab-LX1-L03-1.py: 0 and 0. Printed booleans are 'X is deeper than Y: True' "
                  "(Part B), 'depth never falls as the parity duration rises: True' and 'depth rises at every step ...: True' "
                  "(Part C); Part D prints three ratios with no equality test. L03.html:145 describes exactly these prints. "
                  "The one sentence that misdescribes the code is at L03.html:121 (see lx1b-L03-line121-lab-formula)."),
    dict(id="lx1b-L03-misconception-scope", check="prose", location="L03.html:418 (misconception 2); proof L03.html:130",
         status="PASS",
         evidence="The sentence lists what the Cor 3.3 proof uses: the closed form V_m = D(1-delta)^(-m) (Assumption 1.1), "
                  "the bound V_m < N_0 + D (Assumption 1.2), Lemma 3.1 and Prop 3.2(b). The proof at L03.html:130 uses "
                  "V_{m'} = D(1-delta)^(-m') < V_m, V_m < C from Assumption 1.2, Lemma 3.1 and the Prop 3.2(b) formula. The list "
                  "matches the proof."),
    dict(id="lx1b-L04-A2-before-defined", check="dag", location="L04.html:85 (Definition 2.1), :92, :94, :99, :396 (P2), :446 (R2)",
         status="PASS",
         evidence="grep -n '(A2)' L04.html: the first occurrence is inside Definition 2.1 (line 85), with the content stated in the "
                  "same sentence. (A3) first appears in Problem P2 (line 396) with its statement, and R2 (line 446) and the quiz "
                  "(line 555) use it after. (A1) is stated in the hypothesis of Prop 1.2 (line 66)."),
    dict(id="lx1b-L04-keyresults-locator", check="grades", location="L04.html:469 (key results row 3)", status="PASS",
         evidence="The row reads '(Lab 1, Parts C and D)'. Part C prints the two dispersions 0.027935 and 0.024700 (expected lines "
                  "307, 310); Part D prints the ratio 0.8842 (expected line 315)."),
    dict(id="lx1b-cards-l03-l04", check="cards", location="course/modules/LX/LX1/cards.json (46 L03/L04 cards; changed LX1-c041, "
                                                           "c042, c059, c062, c063)",
         status="PASS",
         evidence="All 46 L03/L04 cards read in full (" + S + "cards_dump_r5.txt). cards_l03_l04_r5.py (" + S +
                  "cards_l03_l04_r5.out): 74 cards, 0 duplicate ids, 0 duplicate fronts; every number of two or more "
                  "characters in each L03/L04 card's front and back appears in its lesson text (0 unmatched). Changed cards "
                  "re-read against the current lesson text: c041 (Definition 4.1), c042 (Remark 4.2, Assumptions 1.2-1.3), c059 "
                  "(665 nonzero of 668, Lab 1 Part B), c062 (no historical definition), c063 (2000-01-03 starts). Card c051 writes "
                  "1e-12 where the lesson writes 10^{-12} (Remark 1.3); the same value, not a defect."),
    dict(id="lx1b-delta-hunks", check="delta", location="L03.html (8 hunks: lines 74, 119, 381, 403, 416, 514, 628, 638); "
                                                        "L04.html (8 hunks: lines 36, 49, 60, 84, 110, 133, 314, 562); "
                                                        "tests/labs/LX1/lab-LX1-L04-1.py (1 hunk, docstring lines 23-26); "
                                                        "cards.json (6 hunks)",
         status="PASS",
         evidence="git diff 9a02b1af 7376a5e over the slice, read hunk by hunk: L03 and L04 hunks are wording changes (credit "
                  "channel as 'course's reference list', 'Assumptions 1.1 to 1.3', 'the lab sets under Assumption 1.1', 'Lab "
                  "1, Part A ... (11 monthly changes)', the sentence on the difference computed from unrounded standard deviations "
                  "(L04.html:316), and the 'Section 3' cross-reference in L04.html:51). The L04 twin hunk is the docstring "
                  "only; code unchanged. cards.json hunks: c016 and c023 (slice a), c041, c042, c059, c062, c063 (this slice). "
                  "Outside the slice, tests/labs/LX1/lab-LX1-project-3.py changed (one docstring line and a printed difference), "
                  "and project.html changed; both belong to the project slice and are not checked here. The L03 line 121 "
                  "sentence (lx1b-L03-line121-lab-formula) is unchanged since round 4 and was missed in round 4."),
    dict(id="lx1b-L03-line121-lab-formula", check="lab", location="L03.html:121 (Proposition 3.2 paragraph); L03.html:145; "
                                                                  "tests/labs/LX1/lab-LX1-L03-1.py depth() at lines 109-111 (page L03.html:258-260)",
         status="FAIL",
         evidence="L03.html:121 says 'Part (b) is the formula that Lab 1 evaluates.' The lab never evaluates Proposition 3.2(b): "
                  "depth() at the twin's lines 109-111 (page L03.html:258-260) is max(depth_path(...)), the maximum over the path of f_t computed from the price "
                  "index, the real debt and the leverage (L03.html:253-255), and no line of the twin computes the closed form "
                  "beta*phi*(ell(V_m) - ell(D)). L03.html:145 itself says 'Lab 1 computes each depth from the model's price "
                  "path'. The mathematics is correct (the closed form equals the path maximum at t = m; recompute_r5.out, "
                  "'closed-form check True'); only the sentence about the lab is false. Found in round 5; present unchanged "
                  "since round 4.",
         fix="Replace 'Part (b) is the formula that Lab 1 evaluates' (L03.html:121) with: 'Part (b) is the closed form of the "
             "depth. At t = m it equals the maximum of the output fall that Lab 1 computes from the price path, and the lab "
             "does not evaluate part (b) itself.' Then re-run run_labs and the page code/expected comparison (no code change "
             "is needed)."),
    dict(id="lx1b-L03-why-ordering", check="prose", location="L03.html:51 (why-it-matters paragraph)", status="FAIL",
         evidence="L03.html:51 says Lab 1 prints the depth 'of two model economies, one that stays on parity for longer than the "
                  "other. Its ordering follows from that assumption', where 'that assumption' is Assumption 1.3 (the depth "
                  "definition, L03.html:70-73). The ordering does not follow from Assumption 1.3 alone: Corollary 3.3 needs the "
                  "two parity durations (Assumption 1.1; the lab sets 12 and 4, tests/labs/LX1/lab-LX1-L03-1.py PARITY_X and "
                  "PARITY_Y) and the bound V_m < N_0 + D of Assumption 1.2 (L03.html:130). The page's own statements elsewhere "
                  "(L03.html:383, :418) cite 1.1 and 1.2 as well. Found in round 5.",
         fix="In L03.html:51 replace 'Its ordering follows from that assumption' with 'Its ordering follows from Assumptions 1.1 "
             "to 1.3 (Corollary 3.3)'."),
    dict(id="lx1b-L04-spot-only", check="prose", location="L04.html:326 ('Exchange rates only' bullet); plan section 3 L04 "
                                                           "(plans/LX1-build-plan.md:286-289); tools/data_sources.yaml:62-64",
         status="FAIL",
         evidence="The plan's mandatory L04 content is 'Spot rates only, as the fx_monthly note states (tools/data_sources.yaml:62-64)' "
                  "and, for the canon-breaks section, 'the series is spot-only and has no interest differential'. The page never "
                  "uses the word spot (grep -c spot L04.html: 0). The page covers 'exchange rates only' and the absence of an "
                  "interest-rate column (L04.html:120, :326) but not the spot-only limit, which the dataset note states "
                  "(tools/data_sources.yaml fx_monthly note: 'Spot rates only, as for fx_daily'). Found in round 5 on the plan "
                  "check; the omission predates round 4.",
         fix="In the 'Exchange rates only' bullet (L04.html:326) add: 'The dataset note states that the series is spot-only, so "
             "each value is a spot rate and the series holds no forward rate.' Keep the existing sentence about interest-rate "
             "columns."),
]

fragment = {
    "unit": "LX1",
    "slice": "LX1-b",
    "round": 5,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-b, round 5 (did not build LX1 or LX1-b; re-read L03.html and "
                "L04.html in full, both lab twins line by line against the page blocks, the cards of L03 and L04, and the "
                "slice delta from 9a02b1af; re-verified every round-4 non-PASS row and every row whose subject changed)",
    "pin": "7376a5e2",
    "base": "9a02b1af (round-4 pin); the slice delta since then is L03.html (8 hunks), L04.html (8 hunks), "
            "tests/labs/LX1/lab-LX1-L04-1.py (docstring only), cards.json (6 hunks, 2 of them in slice a)",
    "checkout": str(root),
    "scratch": "/tmp/lx1b-r5 (labs run in /tmp/lx1b-r5/L03 and /tmp/lx1b-r5/L04; guard copies in /tmp/lx1b-r5/guard)",
    "verified_at": "2026-11-04T17:10:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "friedman1963monetary: the registry record lists Friedman only; the curriculum string is 'Friedman & Schwartz (1963)' "
        "(plan N2). The pages cite the key and the title only. The architect may correct the record through tools/add_reference.py.",
        "Bernanke (1983), AER 73(3), the credit-channel source in curriculum/06-profession-capstone.yaml:38: no registry record "
        "(plan B2, REFERENCE_REQUEST 2). L03 makes no empirical credit-channel attribution. The NBER working paper DOI "
        "10.3386/w1054 must not be admitted as the AER article.",
        "Bretton Woods (plan B3, REFERENCE_REQUEST 3): no registry record. L04 gives no historical fact about the system.",
        "fx_monthly sampling wording differs between the MANIFEST transform ('month-end (each column's last value in the month)') "
        "and the dataset note in tools/data_sources.yaml ('last noon rate of its month, sampled from the daily series'). L04 "
        "follows the MANIFEST wording, which is consistent with the MANIFEST; the noon-rate and monthly-average distinction in the "
        "dataset note is not stated on the page.",
    ],
    "freshness_flags": [],
    "notes": (
        "Round 5 on 7376a5e2. Delta since 9a02b1af read hunk by hunk. Whole-page reads of L03.html (653 lines) and L04.html "
        "(579 lines), and of both twins (the page code blocks equal the twins, so the twin read covers the page code). "
        "Every number recomputed by my own scripts: l03_partA_r5.py and recompute_r5.py (exact Fraction for L03, 60-digit Decimal "
        "for L04; neither imports a twin). Gates re-run on this pin, saved in ledgers/LX1/scripts/LX1-b-r5/: check_pages (L03, "
        "L04, unit), check_dag, run_labs (unit, L03, L04), page_smoke (L03, L04), ruff check and format, mypy --no-incremental on "
        "both twins, pytest (test_labs -k LX1; test_page_checks and test_docs_figures), verify_refs --offline and --unit LX1 "
        "(live, 3 entries, 0 problems), fetch_data --check, plain curl of the Federal Reserve disclaimer (HTTP 200, quote present). "
        "Twins run alone under python -I -W error in empty scratch dirs (exit 0, empty stderr, 56 and 17 lines). "
        "Mutation testing: not applicable to lab twins (architect ruling: lab twins are demonstrations); mutants is empty. "
        "Round-4 FAIL lx1b-L04-bretton-definition is unchanged in substance and stays FAIL pending the architect ruling. "
        "Round 4 missed two real defects that were already in the pages: L03.html:121 (lx1b-L03-line121-lab-formula) and "
        "L04.html:326 spot-only omission (lx1b-L04-spot-only); L03.html:51 ordering attribution (lx1b-L03-why-ordering) is "
        "new in this round's reading. Not checked: the L01/L02 pages and cards c016 and c023 (slice a); the hub and index "
        "pages and the hours split of the unit (not in this slice; the L03 and L04 pages carry data-hours 10); project.html "
        "and tests/labs/LX1/lab-LX1-project-3.py (project slice; the twin changed in this delta); the live fetch_data --fetch "
        "rebuild of fx_monthly (carried from round 3, files byte-identical); render_curriculum.py and build_site.py "
        "(no generated file in this slice); the full pytest suite (targeted only, per the verifier rules); a live Crossref "
        "check beyond the repo tool (scheduled CI); the renamed-column guard case (round 3; the code is unchanged). "
        "No 2025-2026 material is cited in these pages, so the freshness check has nothing to flag."
    ),
    "summary": (
        "LX1-b round 5 on 7376a5e2: verdict FAIL. 55 rows: pass=51 fail=4 unverifiable=0. Fails: "
        "lx1b-L04-bretton-definition (architect ruling; plan and check_dag conflict, unchanged since round 4); "
        "lx1b-L03-line121-lab-formula (L03.html:121 says Lab 1 evaluates Part (b); it does not); "
        "lx1b-L03-why-ordering (L03.html:51 attributes the ordering to Assumption 1.3 alone); "
        "lx1b-L04-spot-only (plan-mandated spot-rates-only limit is absent from L04). All gates, both twins, every number, "
        "every proof, the licence quote, the citations and the L03/L04 cards otherwise pass on this pin."
    ),
}

out = root / "ledgers/LX1/LX1-b.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows:", len(rows), "fail:", sum(r["status"] == "FAIL" for r in rows))
