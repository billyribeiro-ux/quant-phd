"""Round 14: writes ledgers/LX1/LX1-b.json from the round-14 evidence. Run: python -I make_fragment_r14.py <checkout>"""
import json
import sys
from datetime import datetime, timezone

ROOT = sys.argv[1]
S = "ledgers/LX1/scripts/LX1-b-r14"
O = f"{S}/out"
CARRY = ("Carried from round 13 (course/assets/data/market/fx_monthly.csv, course/assets/data/market/MANIFEST.json and "
         "tools/fetch_data.py byte-identical since the previous pin e919577, verified by git diff --quiet e919577 HEAD):")

R = []


def row(id_, check, location, status, evidence, fix=""):
    R.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


row("lx1b-check-pages", "2.9 structure (check_pages)", "course/modules/LX/LX1/L03.html; L04.html",
    "PASS", f"tools/check_pages.py --unit LX1 -> 'check_pages LX1: PASS', exit 0 ({O}/check_pages.out).")
row("lx1b-check-dag", "2.9 DAG (check_dag)", "L03.html; L04.html",
    "PASS", f"tools/check_dag.py --unit LX1 -> 'check_dag LX1: PASS', exit 0 ({O}/check_dag.out); link targets re-checked by {S}/scans_r14.py section 3 (all OK).")
row("lx1b-check-projects", "2.6 unit gate (check_projects)", "course/modules/LX/LX1/project.html (unit gate only)",
    "PASS", f"tools/check_projects.py --unit LX1 -> 'check_projects LX1: PASS', exit 0 ({O}/check_projects.out). Project content is slice e, not checked here.")
row("lx1b-run-graders", "2.6 grader (not applicable)", "tools/run_graders.py --unit LX1",
    "PASS", f"'run_graders LX1: no autograder (grading: rubric)', exit 0 ({O}/run_graders.out). No grader or mutant applies to LX1.")
row("lx1b-dag-links", "2.9 DAG links", "L03.html (L02.html#def-debt-deflation, #def-gold-standard); L04.html (../../../concepts.html#exponential-and-logarithm, L02.html#def-gold-standard, L03.html#def-lender-of-last-resort, #def-bretton-woods-system)",
    "PASS", f"{S}/scans_r14.py section 3 prints OK for every concept href; concepts.html contains id=\"exponential-and-logarithm\" (M1 concept, in closure). Output {O}/../scans_r14.out.")
row("lx1b-dag-outside-closure", "2.9 DAG (outside-closure names, plan section 4 D1-D15)", "L03.html; L04.html",
    "PASS", f"{S}/scans_r14.py section 1 CLOSURE_OUT patterns (bank run, fire sale, leverage cycle, banking crisis, currency crisis, covered/uncovered interest, efficient market, moral hazard, Fisher, bank reserve, credit default, contagion, term spread, expected inflation, sovereign, deposit insurance, central bank balance): none. Plain-prose uses of 'central bank' and 'bank failures' carry no data-concept and no link (L03.html:390 central bank; :414 bank failures; L04.html:336 central bank).")
row("lx1b-run-labs", "2.5 labs (run_labs)", "tests/labs/LX1/lab-LX1-L03-1.py; tests/labs/LX1/lab-LX1-L04-1.py",
    "PASS", f"tools/run_labs.py --unit LX1 -> 'run_labs LX1: PASS (7/7)', exit 0 ({O}/run_labs.out). Imports read: L03 math, fractions only; L04 csv, itertools, math, re, collections.abc, decimal, fractions, pathlib only; no random, no network. Seeded RNG not needed (no randomness).")
row("lx1b-twin-alone-L03", "2.5 labs (twin alone)", "tests/labs/LX1/lab-LX1-L03-1.py",
    "PASS", f"Copied alone to /tmp/lx1b-r14/L03; 'python -I -W error lab-LX1-L03-1.py' exit 0; stderr empty except the exit line ({O}/twin_L03.err, {O}/twin_L03.out).")
row("lx1b-twin-alone-L04", "2.5 labs (twin alone)", "tests/labs/LX1/lab-LX1-L04-1.py",
    "PASS", f"Copied alone with data/fx_monthly.csv to /tmp/lx1b-r14/L04; 'python -I -W error' exit 0; stderr empty except the exit line ({O}/twin_L04.err, {O}/twin_L04.out).")
row("lx1b-twin-equals-page-code", "2.5 labs (page code = twin; expected = output)", "L03.html lines 150-326 (code), 327-382 (expected); L04.html lines 115-305 (code), 306-322 (expected)",
    "PASS", f"{S}/compare_r14.py: 'L03 page data-run code equals twin: True', 'L03 expected block equals twin stdout: True' (56 lines each), 'L04 ... True' (17 lines each), 'ALL EQUAL: True' ({O}/compare_r14.out).")
row("lx1b-page-smoke-L03", "2.9 page_smoke (L03 alone)", "course/modules/LX/LX1/L03.html",
    "PASS", f"tools/page_smoke.py --unit LX1 --pages L03 -> 'page_smoke modules/LX/LX1/L03.html: PASS', exit 0, lab 0.0 s ({O}/page_smoke_L03.out).")
row("lx1b-page-smoke-L04", "2.9 page_smoke (L04 alone)", "course/modules/LX/LX1/L04.html",
    "PASS", f"tools/page_smoke.py --unit LX1 --pages L04 -> 'page_smoke modules/LX/LX1/L04.html: PASS', exit 0, lab 0.0 s ({O}/page_smoke_L04.out).")
row("lx1b-ruff-mypy", "2.5 ruff and mypy (twins)", "tests/labs/LX1/lab-LX1-L03-1.py; lab-LX1-L04-1.py",
    "PASS", f"ruff check tests/labs/LX1 'All checks passed!' exit 0 ({O}/ruff_check.out); ruff format --check '7 files already formatted' exit 0 ({O}/ruff_format.out); mypy --no-incremental on both twins 'Success: no issues found in 2 source files' exit 0 ({O}/mypy_L03_L04.out).")
row("lx1b-pytest", "2.5 pytest (LX1 lab and page tests)", "tests/test_labs.py; tests/test_page_checks.py (-k LX1)",
    "PASS", f"python -m pytest tests/test_labs.py tests/test_page_checks.py -q -k LX1 exit 0 ({O}/pytest_LX1.out); collect-only 'tests/test_labs.py: 7' ({O}/pytest_collect_LX1.out).")
row("lx1b-verify-refs", "2.1 citations (verify_refs)", "references/references.json",
    "PASS", f"tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0 ({O}/verify_refs_offline.out). tools/verify_refs.py --unit LX1: 'live re-verification of LX1: 4 of 560 entries, 0 problems', exit 0 ({O}/verify_refs_unit_LX1.out).")
row("lx1b-citations-L03", "2.1 citations (L03)", "L03.html:405 (span data-cite), :640 (References)",
    "PASS", "Only key friedman1963monetary is cited (grep data-cite: L03.html twice, both friedman1963monetary). Registry record references/references.json: title 'A monetary history of the United States 1867-1960', author Friedman (Milton), year 1963, ISBN 0691041474, status verified (read by Python). The second author is not typed (grep 'Schwartz' in L03/L04: 0). L03 attributes no finding to the book (L03.html:405, :640 say so), so there is no attributed claim to grade.")
row("lx1b-citations-L04", "2.1 citations (L04)", "L04.html section 9 (lines 569-575)",
    "PASS", "L04 cites no registry key. grep -il 'bernanke|kindleberger|eichengreen|garber|reinhart' over L03.html and L04.html: no match (exit 1). The dataset citation is the MANIFEST citation (course/assets/data/market/MANIFEST.json fx_monthly.citation).")
row("lx1b-fetch-check", "2.8 data (fetch_data --check)", "course/assets/data/market/fx_monthly.csv; MANIFEST.json",
    "PASS", f"tools/fetch_data.py --check -> 'fetch_data: 3 datasets, 0 problems', exit 0 ({O}/fetch_check.out).")
row("lx1b-fx-rebuild", "2.8 data (reproducible snapshot)", "course/assets/data/market/fx_monthly.csv; MANIFEST.json fx_monthly (sha256 60572240...)",
    "PASS", CARRY + " round-13 rebuild from the live H.10 feed in a git-archive scratch copy: 'built fx_monthly: 669 rows, 67392 bytes, 1971-01 to 2026-09'; rebuilt sha256 = 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e = MANIFEST sha256 = checkout file (ledgers/LX1/scripts/LX1-b-r13/out/fetch_rebuild_fx_monthly_r13.out). Round 14 did not re-run the rebuild. The inputs are unchanged, and fetch_data --check passes this round (lx1b-fetch-check).")
row("lx1b-fx-licence", "2.8 data (licence quote)", "tools/data_sources.yaml fx_monthly (licence, licence_url); MANIFEST fx_monthly.licence",
    "PASS", f"curl -sS -L https://www.federalreserve.gov/disclaimer.htm -> 'HTTP 200' ({S}/out/guard_licence_r14.out; {O}/curl_fed_disclaimer_code.out). The page contains 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.' (grep quote, {O}/fed_licence_quote.out); identical to the MANIFEST and data_sources.yaml licence text, which grants redistribution.")
row("lx1b-fx-guard", "2.5 labs (fail loud on bad data)", "tests/labs/LX1/lab-LX1-L04-1.py parse_rate, load_column",
    "PASS", f"{S}/guard_licence_r14.sh: a scratch copy with a blank GBP cell (1979-04) exits 1 with 'ValueError: 1979-04: GBP cell is '', not a decimal rate'; a copy with '1.2e0' (1987-08) exits 1 with ValueError ({O}/guard_blank.err, {O}/guard_expo.err). Code read: load_column raises on a missing column, a non-YYYY-MM label and a non-consecutive month; no row is skipped.")
row("lx1b-fx-gbp-clean", "2.8 data (the column read has no blanks)", "course/assets/data/market/fx_monthly.csv (GBP column)",
    "PASS", f"{S}/rederive_r14.py: 'L04 rows 669 ... L04 GBP blanks 0'. Month contiguity is enforced by load_column, and the twin runs to completion on this file (lx1b-twin-alone-L04).")
row("lx1b-honest-data", "2.8 honest data (SIMULATED vs real)", "L03.html:76, :147-152; L04.html:7, :113-114, :120-122",
    "PASS", "L03 is SIMULATED with an honest-pending note (L03.html:76) that no redistributable historical series is embedded; the lab title says SIMULATED (L03.html:148). L04 names its only dataset, licence and retrieval date (L04.html:113-114, :120-122). No historical series is typed in either page.")
row("lx1b-L04-simulated-label", "2.8 SIMULATED labels", "L04.html:113 (lab title), :114 (hypothesis); twin docstring; expected block line 306",
    "PASS", "Part A is labelled SIMULATED in the lab title (L04.html:113), the hypothesis (:114), the twin docstring (lines 138-139) and the expected block (line 306). Parts B-D are not labelled SIMULATED and read only fx_monthly.csv (L04.html:114).")
row("lx1b-L04-manifest-note", "2.8 data (MANIFEST note and transform)", "tests/labs/LX1/lab-LX1-L04-1.py docstring lines 1-30; L04.html:112, :113-114, :326, :333",
    "PASS", "data-files lists fx_monthly.csv (L04.html:112). The docstring and page state the MANIFEST transform (month-end, each column's last value in the month, GBP direct quote, retrieved 2026-10-19, 669 months) and match course/assets/data/market/MANIFEST.json fx_monthly.transform. The spot-only note matches tools/data_sources.yaml fx_monthly note ('Spot rates only, as for fx_daily').")
row("lx1b-open-items-missing", "2.9 open items", "plans/LX1-open-items.md",
    "PASS", "plans/LX1-open-items.md read in full: D-1 (L03 data request), Bretton Woods (pending definition, architect decision requested), reference requests for Bernanke (B2), Kindleberger (N1) and Friedman record (N2). File unchanged since e919577 (git diff).")
row("lx1b-num-L03-depth", "2.2 numbers (L03 Lab 1, Part B and D)", "L03.html Part B (expected lines 358-361), Part D (379-382), key results rows 3-4 (545-546), E1-E2 (489-498), quiz (574-610)",
    "PASS", f"{S}/rederive_r14.py (Fraction arithmetic, independent of the twin): depth X 9.204597 -> 9.20; depth Y 2.686713 -> 2.69; first reached t = 12 and t = 4; difference 6.517884 -> 6.52 while the printed difference 9.20 - 2.69 = 6.51 (E2 states this); ratio X/Y 3.425970 -> 3.4260; the ratio equals 3.425970 at phi = 1/2, 1 and 3 ({O}/rederive_r14.out). Quiz 'exact value 1,274,345.2124' (L03.html:610): rederive gives V_12 = 1274345.2124 cents.")
row("lx1b-num-L03-path", "2.2 numbers (L03 expected path rows)", "L03.html expected block lines 327-357 (economy X and Y paths); M1-M3 (:439-456); P2 (:473); E1 (:491)",
    "PASS", f"{S}/expected_l03_r14.py: 26 rows of the expected block (economies X and Y, t = 0..12: index, real debt, leverage, premium, output fall) recomputed in exact Fractions with half-up display: 'rows checked 26 mismatches 0' ({O}/expected_l03_r14.out). M1: P_4 = (49/50)^4 = 5764801/6250000, V_4 = 1084165.7847 -> 1,084,166. M2: A_4 = 3915834.2153 -> 3,915,834. M3: L_4 = 0.276867 -> 0.2769. Baseline L_0 = 0.2500 (line 329).")
row("lx1b-num-L04-stats", "2.2 numbers (L04 Lab 1, Parts A-C)", "L04.html expected block lines 306-322; interpretation (:323); key results rows 3-4 (:476-477); quiz (:524-528, :505-513)",
    "PASS", f"{S}/rederive_r14.py on the CSV (independent parse): 669 rows, 668 changes, zeros 1976-07, 2012-07, 2019-11, nonzero 665; window one (1971-02..2026-09) sd 0.0279352779 -> 0.027935; window two (2000-01..2026-09, 321 changes, base rate 1999-12 = 323/200) sd 0.0246995014 -> 0.024700; ratio 0.8841688 -> 0.8842; largest |change| window one 0.135846 at 1985-03, window two 0.096575 at 2008-10 (signed -0.096575) ({O}/rederive_r14.out).")
row("lx1b-num-L04-display-diff", "2.2 numbers (display rounding)", "L04.html interpretation (:323); expected line 321",
    "PASS", f"{S}/rederive_r14.py: unrounded difference s2 - s1 = -0.00323578 -> -0.003236 (the printed value); the difference of the two printed figures 0.024700 - 0.027935 = -0.003235, which the interpretation states as the other value. Both correct; the page says which is which (L04.html:323).")
row("lx1b-num-L04-derived", "2.2 numbers (derived on the page)", "L04.html M1 (:373), M2 (:380), M3 (:387), P2 (:405), E2 (:430), R2 (:455), misconception 3 (:354), quiz (:541, :564)",
    "PASS", f"{S}/rederive_r14.py: ln 1.1 = 0.0953101798 -> 0.095310; simple 0.100000; difference 0.004690; M2 mean 1/150 -> 0.006667, dispersion sqrt(19/30000) -> 0.025166; E2 exp(-0.0965747) - 1 = -0.092058; R2 h = tanh(z/2) = 0.067819 for z = 0.135846 (h = 0.0678 gives a bound 0.135808, which does not reach z); quiz bound ln(1.0678/0.9322) = 0.135808 -> 0.1358; M3 count 321.")
row("lx1b-scope-start", "2.4 scope (window two start)", "L04.html:110, :326, :335, :387, :462; card LX1-c063",
    "PASS", f"Window one base is 1971-01 (rows[0]); window two base is 1999-12 and its first change is dated 2000-01 (twin lines 127-130; L04.html:326 states the base explicitly). The phrase 'start from the first month in which the other two snapshots have data' at L04.html:110 is read with the explicit statement at :326 and is not a misstatement. fx_daily and ust_daily begin 2000-01-03 (MANIFEST).")
row("lx1b-math-L03", "2.4 mathematics (L03 lemma, proposition, corollaries)", "L03.html:94-143 (Lemma 3.1, Prop 3.2(a)-(c), Cor 3.3, Cor 3.4), :67, :121, :145",
    "PASS", f"Each proof read. Lemma 3.1 identity y/(C-y) - x/(C-x) = C(y-x)/((C-x)(C-y)) (P3 solution, read). Prop 3.2(a) V_t <= V_m (uses 0 < 1-delta < 1); (b) closed form equals the maximum over the path (rederive_r14.out: closed form m = 4 and m = 12 agree with the path maxima to 6 dp); (c) first maximiser t = m. Cor 3.3 uses V_mprime < V_m and Lemma 3.1; Cor 3.4 divides (b) and cancels beta phi. Hypotheses (Assumptions 1.1-1.3, shared D, A_0, delta, phi, beta) are stated on each corollary.")
row("lx1b-math-L04", "2.4 mathematics (L04 identities, proposition, bounds)", "L04.html:58-107 (Def 1.1, Prop 1.2, Remark 1.3, Def 2.1, Prop 2.2, Remark 2.3)",
    "PASS", f"Prop 1.2 telescoping proof read (cancellation of interior ln x_t terms). Numerically sum of changes minus ln(x_b/x_a) is ~1e-15 for both windows ({O}/rederive_r14.out, 'sum identity' lines). Prop 2.2 (A2 gives ln 1 = 0; dispersion 0 with n >= 2). Remark 1.3 tolerance 1e-12 equals SUM_TOLERANCE in the twin (line 162).")
row("lx1b-math-problems", "2.4 mathematics (problem sets, worked solutions)", "L03.html:431-532 (M1-M3, P1-P3, E1-E3, R1-R3); L04.html:363-466 (mech-1..3, proof-1..3, emp-1..3, res-1..3)",
    "PASS", f"Every problem and worked solution read in this round. Numbers re-derived ({O}/rederive_r14.out, expected_l03_r14.out). P1 (L03) monotonicity; P2 (L03) depth(0) = 0; P3 (L03) identity; R2 (L03) strictly increasing premium ordering; L04 P1 induction; P2 band bound (checked |l_t| <= ln((1+h)/(1-h))); P3 f(u) = ln(1+u) - u sign argument (f' = -u/(1+u)); R2 (L04) h = tanh(z/2) with d/dh ln((1+h)/(1-h)) = 2/(1-h^2) > 0; R1, R3 (L04) and R1-R3 (L03) read for overreach.")
row("lx1b-grades", "2.3 grades", "L03.html:124, :134, :541-546 (key results); L04.html:468-477 (key results); cards grades",
    "PASS", "Re-graded against BLUEPRINT section 3: derived results are T with a proof on the page (L03 Props 3.2, Cors 3.3-3.4; L04 Props 1.2, 2.2). Lab-printed values are C with the lab named (L03 key rows 4-5 (Lab 1 Parts B and D); L04 key rows 3-4, Lab 1 Parts B-D). No empirical claim is graded above C, and none is made.")
row("lx1b-notation", "2.4 notation (local symbols in L03, L04 and cards, against notation/notation.json and L02)", "L03.html; L04.html; cards.json (L03, L04)",
    "PASS", f"{S}/scans_r14.py section 4: L03 math letters ACDGHLPVfkmtxy and greek delta, varphi, beta, psi, lambda; L04 abefhknstuxz and ell, bar{{x}}. Meanings agree with L02 for D (nominal debt), V (real value), P (price index), H (horizon), kappa not used in L03/L04. Lesson-local dummies (L03 k in k -> (1-delta)^k; L04 f(u) in P3; L04 s_1, s_2 dispersions beside L01's d_s index) are not defined in another lesson with a conflicting role and are not used across lessons.")
row("lx1b-concepts-defs", "2.9 concepts (one dfn per concept)", "L03.html:86, :389; L04.html:86",
    "PASS", "dfn data-concept elements: L03 credit-channel-depression (L03.html:86) and lender-of-last-resort (L03.html:389); L04 bretton-woods-system (L04.html:86, placeholder, see lx1b-L04-bretton-definition). Each id appears once (scans_r14 section 3 dfn lists; check_dag PASS). Plain dfn elements without data-concept: leverage, external-finance premium, central bank (L03), anchor currency, fixed exchange rate, fixed-exchange-rate model, monthly log change, dispersion (L04).")
row("lx1b-banned-phrases", "2.9 banned phrases (BUILDER_RULES 1.3-1.4)", "L03.html; L04.html; tests/labs/LX1 twins",
    "PASS", f"{S}/scans_r14.py section 1 (prose with code and expected blocks removed): TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, ellipsis: none. Twin ellipses (L03 twin lines 13 and 105) are inside Python code, which the rule exempts.")
row("lx1b-process-words", "2.9 process words in learner text", "L03.html; L04.html; cards.json (L03, L04); twins",
    "PASS", f"{S}/scans_r14.py section 1 (build, builder, round, verifier, REQUEST, unit report, fixer, planner, architect, ruling): none in prose. grep over the twins and cards: only 'Round a Fraction' (twin code docstring, L03 line 45, a verb) and 'unrounded' (LX1-c065), neither a process word.")
row("lx1b-scope-words", "2.4 scope words (every, all, never, any, only, same, exactly, the first)", "L03.html; L04.html",
    "PASS", f"{S}/scans_r14.py section 2 counts (L03: every 23, any 10, only 7, same 9, never 2, exactly 2, the first 4; L04: every 17, any 8, only 9, same 5, exactly 13, the first 6). Every paragraph of both pages read in full in this round; each universal is bounded by a proof, a finite lab, or 'in the model' (e.g. L03.html:117-118, :145, :395, :402; L04.html:51, :335, :437, :448).")
row("lx1b-structure", "2.9 structure (BUILDER_RULES section 4)", "L03.html sections 1-10; L04.html sections 1-9",
    "PASS", "L03: model (1), definitions (2), closed form and ordering (3), lender (4), canon breaks (5), misconceptions (4), problem set (M 3, P 3, E 3, R 3), key results (8), quiz (9: 11 items), references (10). L04: monthly log changes (1), model (2), recorded column (3), canon breaks (4), misconceptions (5), problem set (mech 3, proof 3, emp 3, res 3), key results (7), quiz (8: 11 items), references (9). Counts read from the page (lines per section).")
row("lx1b-quiz-explanations", "2.9 quiz explanations vs lesson", "L03.html:553-636; L04.html:483-567",
    "PASS", "Each explanation read against its lesson section: L03 Q1 (P_t after m), Q2 (psi_0 = 0), Q3-Q4 (Lab 1 Part B, Prop 3.2(c)), Q5 (Cor 3.3, same beta, phi, delta, D, A_0), Q6 (Part D, Cor 3.4), Q7, Q8 (V_12 = 1274345.2124), Q9 (Problem E3, 8 periods), Q10 (Def 4.1), Q11 (Section 5). L04 Q1 (A2), Q2 (Prop 2.2(b)), Q3 (3 zeros), Q4 (321), Q5 (Prop 1.2), Q6 (27935 = window one, 667 denominator), Q7 (Problem E3), Q8 (ln 1.1), Q9 (window start), Q10 (Section 4), Q11 (band bound).")
row("lx1b-L03-remark42-solvency", "2.4 mathematics (Remark 4.2 solvency)", "L03.html:64-67 (Assumption 1.2); :395 (Remark 4.2)",
    "PASS", f"V_m < A_0 + D with Prop 3.2(a) V_t <= V_m gives V_t < A_0 + D and A_t > 0 in every period. Numbers: V_12 = 1274345.2124 < 5000000 and V_4 = 1084165.7847 < 5000000 ({S}/out/../rederive_r14.out). The chain is correct.")
row("lx1b-L03-ratio-claims", "2.2 claims (ratio of depths under a different premium)", "L03.html:404 (functional-form bullet); :516 (R1); :523 (R2)",
    "PASS", "If psi = phi (L - L_0)^2, each depth is beta phi times the square of the Cor 3.4 bracket, so the ratio is the square of the Cor 3.4 ratio; that differs from it unless the ratio is 1 (here 3.4260), as the page says. Changing phi cancels in the ratio, as the page says (L03.html:404).")
row("lx1b-L03-r1-no-result", "2.4 mathematics (R1 asserts no result)", "L03.html:516 (R1 solution)",
    "PASS", "R1 says Prop 3.2 is not carried over without a new proof and that Lemma 3.1's monotonicity is unaffected while the identity L_t = lambda(V_t) must be checked again. No facility result is asserted.")
row("lx1b-L04-bretton-definition", "2.9 concepts / Architect decisions (Bretton Woods definition pending)", "L04.html:38, :86 (dfn placeholder), :81, :337, :358, :557; plans/LX1-build-plan.md section 0.3 B3, section 12 item 9, Architect decisions (2026-11-03, binding); plans/LX1-open-items.md 'Definitions waiting for a source'; course/concepts.html:631 ('defined here')",
    "FAIL", "Re-verified on 8e5751c: L04.html:86 still places <dfn id=\"def-bretton-woods-system\" data-concept=\"bretton-woods-system\">Bretton Woods system</dfn> followed by 'definition pending.', and course/concepts.html:631 lists the concept as 'defined here'. The binding architect decision says the Bretton Woods definition and end date wait for a request (plan Architect decisions, module specifics). The page waits, but it still marks the concept as defined. The open-items note (plans/LX1-open-items.md) asks the architect to confirm or record a different reading, and no ruling is recorded in plans/FINAL-ARCHITECT-RULINGS.md or the build plan (grep for Bretton, LX1 and B3 finds none there). Registry: 0 'bretton' hits in references/references.json and in review_queue.json.",
    "Architect records a ruling. Either (a) state in plans/LX1-build-plan.md that a concept whose definition is blocked may be carried as a pending dfn that check_dag accepts, or (b) the concept is removed from L04's dfn and concepts.html, with check_dag's requirement changed by the architect. Until the ruling is recorded this row stays FAIL.")
row("lx1b-L04-prediction-tested", "2.5 labs (hypothesis tested by the lab)", "L04.html:114 (hypothesis); twin Parts A and C",
    "PASS", "The hypothesis predicts the model's zero dispersion (printed 'all exactly zero: True', 'model sample standard deviation: 0.000000') and says the recorded column's nonzero dispersion is shown by the printed Part C values, not asserted. The printed Part C values are nonzero (0.027935, 0.024700), so the prediction is shown by the output; the lab does not assert it (L04.html:114, twin Part C).")
row("lx1b-L03-lab-checks-overreach", "2.5 labs (interpretation vs what the lab checks)", "L03.html:145, :383; twin Parts B-D",
    "PASS", "The interpretation (L03.html:383) says the printed depths show what the assumptions imply, not an output fall. The lab prints booleans for ordering and never-falls (Part B, Part C), which the text describes accurately; Part D makes no equality test (L03.html:145).")
row("lx1b-L03-misconception-scope", "2.4 mathematics (misconception 2 proof ingredients)", "L03.html:418 (misconception 2); proof L03.html:124-131 (Cor 3.3)",
    "PASS", "Misconception 2 lists the ingredients of the Cor 3.3 proof (the durations, V_m closed form, V_m < A_0 + D, Lemma 3.1, Prop 3.2(b)); compared with the proof, the list is accurate.")
row("lx1b-L04-A2-before-defined", "2.6/2.4 hypotheses before use", "L04.html:84-92 (Def 2.1, Prop 2.2), :400-405 (P2), :450-457 (R2), :64-66 (Prop 1.2)",
    "PASS", "(A2) stated in Def 2.1 before Prop 2.2; (A3) stated in P2 before R2 uses it; (A1) stated in Prop 1.2 before its use. No assumption is used before its statement.")
row("lx1b-L04-keyresults-locator", "2.3 key results locators", "L04.html:470-477 (key results rows 3 and 4)",
    "PASS", "Row 3 (dispersion values and ratio) cites Lab 1 Parts C and D, which print 0.027935, 0.024700 and 0.8842 (expected block lines 314-322). Row 4 (three zero months) cites Lab 1 Part B (expected line 312).")
row("lx1b-cards-l03-l04", "2.7 retrieval cards (L03 and L04, full scan)", "course/modules/LX/LX1/cards.json (L03: 29 cards; L04: 21 cards)",
    "PASS", f"All 50 L03 and L04 cards read in full. No duplicate id, front or back across the 80 cards (scans_r14 section 5). No card cites a key (cite []). Numbers in backs appear in the lesson (scans_r14 section 5 prints no miss). Each card matches the current lesson text (checked against L03.html Defs 2.1-2.2, Lemma 3.1, Prop 3.2, Cors 3.3-3.4, Def 4.1, Rem 4.2, Assumptions 1.1-1.3; L04.html Defs 1.1, 2.1, Props 1.2, 2.2, Rem 2.3, quiz).")
row("lx1b-cards-c052-c053", "2.7 retrieval cards (named cards)", "cards.json LX1-c052, LX1-c053 vs L04.html:84-92",
    "PASS", "LX1-c052 states Prop 2.2 with (A2), x-bar > 0 and at least two changes, and conclusion 0 and 0, matching L04.html:90-92. LX1-c053 describes Def 2.1 with x-bar as anchor units per unit of the foreign currency, matching L04.html:85.")
row("lx1b-delta-hunks", "2.9 changed subject (e919577..8e5751c)", "course/modules/LX/LX1/L03.html (66 lines), L04.html (3), cards.json (22), tests/labs/LX1/lab-LX1-L03-1.py (14), lab-LX1-L04-1.py (3)",
    "PASS", f"git diff e919577 8e5751c read hunk by hunk for L03, L04, cards (L03, L04 items) and both twins: the N-to-A rename (net worth) in L03 text, twin docstrings and Part A label, and the cards; the Lemma 3.1 and Cor 3.3/3.4 hypothesis wording; the R1 and quiz explanation edits; the L04 forward-rate parenthetical (page and twin docstring) and card LX1-c059. Every hunk checked; no claim changed except as listed. Verified by {O}/compare_r14.out, expected_l03_r14.out, scans_r14.out.")
row("lx1b-L03-partD-label", "2.5 labs (Part D label)", "tests/labs/LX1/lab-LX1-L03-1.py Part D print; L03.html:383 and expected block lines 379-382",
    "PASS", "Part D prints the ratio for phi = 1/2, 1, 3 with beta = 1 and the product in its label; the expected block equals the twin output (compare_r14). The interpretation (L03.html:383) says the printed ratio is the same in all three cases, which the printed block shows (3.4260 three times).")
row("lx1b-L03-line121-lab-formula", "2.2 claims (lab does not evaluate part (b))", "L03.html:120-121 and :145; twin depth() and depth_path()",
    "PASS", "L03.html:121 says the lab does not evaluate Prop 3.2(b) itself; the twin computes the depth as the maximum over the price path (depth(), depth_path()) and does not call a closed form. The statement is accurate.")
row("lx1b-L03-why-ordering", "2.9 prose vs lab (why-it-matters)", "L03.html:51 (why-it-matters)",
    "PASS", "The paragraph says the ordering follows from Assumptions 1.1-1.3 (Cor 3.3) and is not evidence about any economy; consistent with Cor 3.3 and the SIMULATED label (L03.html:148).")
row("lx1b-L04-spot-only", "2.8 data (spot-only, no forward or interest series)", "L04.html:333 (canon breaks), :122-123 (twin docstring); tools/data_sources.yaml fx_monthly note (lines 62-64)",
    "PASS", "data_sources.yaml fx_monthly note: 'Spot rates only, as for fx_daily'. L04.html:333 quotes that statement and states no forward or interest series. The forward-rate parenthetical (L04.html:122-123 and twin docstring line 122-123) defines the term without a claim about the data.")
row("lx1b-L03-honest-pending-source", "2.8 honest-pending note", "L03.html:76 (honest-pending note)",
    "PASS", "The note states that no redistributable historical series for gold-standard adherence or output depth is embedded, and that the lab is SIMULATED. It matches plans/LX1-build-plan.md section 0.3 B1 and plans/LX1-open-items.md D-1.")
row("lx1b-L04-twin-docstring-float", "2.5 labs (docstring vs code: float and rounding)", "tests/labs/LX1/lab-LX1-L04-1.py log_changes, show docstrings and code (lines 223-246)",
    "PASS", "log_changes: exact Fraction ratio, one float conversion, then math.log, dated by the later month (matches the docstring, lines 223-228). show(): Decimal(value).quantize with ROUND_HALF_UP on the exact binary value, for display only (matches the docstring, lines 244-246).")
row("lx1b-plan-coverage", "2.9 plan coverage (plan section 3)", "plans/LX1-build-plan.md section 3 (L03 and L04 content)",
    "PASS", "L03 covers the model (3 assumptions), leverage and the premium (Def 2.1), the credit-channel chain (Def 2.2), the closed form and orderings (Lemma 3.1 to Cor 3.4), the lender of last resort (Def 4.1, Rem 4.2), the canon breaks, the Lab 1 printed values, and the model's limits. L04 covers the log-change identity (Prop 1.2), the model (Def 2.1, Prop 2.2), the two windows and the GBP dispersion (Lab 1), the canon breaks and the open Bretton Woods items (Section 4). Plan section 3's required content is present, and the Bretton Woods definition is pending as the plan allows (B3).")
row("lx1b-concept-index-title", "2.9 concept index", "course/concepts.html:631, :635, :636",
    "PASS", "concepts.html:631 (Bretton Woods system, 'defined here' -> L04#def-bretton-woods-system), :635 (Lender of last resort -> L03), :636 (Nonmonetary (credit) channel of the Great Depression -> L03#def-credit-channel-depression). Each target id exists in its page (scans_r14 section 3). The row's wording on 631 is the subject of lx1b-L04-bretton-definition.")
row("lx1b-notation-registered", "2.4 notation (registered symbols)", "L03.html; L04.html",
    "PASS", f"{S}/scans_r14.py section 4: L03 and L04 use none of T, R_f, Q, Phi, gamma_3, gamma_4, R^*, R^{{e*}} (notation/notation.json symbols). Macros used: \\R, \\ln only; no \\E, \\Prob or \\Var.")
row("lx1b-hours", "2.9 hours arithmetic", "L03.html:2, :34; L04.html:2, :34; hub index.html:160-161",
    "PASS", "data-hours=10 and 'LX1 · Lesson n of 4 · 10 study hours' on both pages; hub cards 'L03 · 10 h' and 'L04 · 10 h'. 4 x 10 = 40 lesson hours, as the plan's split requires.")
row("lx1b-notation-N", "2.4 notation (cross-lesson: N)", "L03.html (former :65-67, :96, :103); cards LX1-c027, c030-c032, c071, c082; L01.html:67, :74, :81 (S_N(t) count)",
    "PASS", f"Fixed on 8e5751c: grep for N_0, N_t, N_4 and a bare N finds none in L03.html, L04.html, tests/labs/LX1/lab-LX1-L03-1.py or the L03/L04 cards. Net worth is now A_t and A_0 (A_t = A_0 - (V_t - V_0); C = A_0 + D); the L03 twin Part A label reads 'A_0 = 4000000 cents' (expected line 328). L01's N remains the count in S_N(t) only. Recheck: {S}/scans_r14.out ('N in L03 (net worth): []').")
row("lx1b-notation-P", "2.4 notation (cross-lesson: P)", "L01.html:105, :114, :119-120, :143-144, :377, :450 (observed price P_t and P_0); L03.html:58-59, :65 (price index P_t and P_0 = 1); L02.html (price index P_t in the debt-deflation identity); project.html (price path P_t)",
    "FAIL", "The symbol P_t has two meanings in the unit. L01 defines P_t as 'an observed price at date t' with the bubble gap B_t = P_t - F_t (L01.html:105) and uses P_0 and P_t as prices throughout (:114-120, :143-144, :377, :450). L02 and L03 use P_t as the price index with P_0 = 1 and V_t = D / P_t (L03.html:58-59, :65; L02 debt-deflation identity). The project uses P_t for a price path. Notation rule 2.4 forbids a registered-or-local symbol reused with another meaning, and this lesson's P_t (L03) is one of the two meanings. Scan: " + S + "/scans_r14.py section 4 (P appears in L01, L02, L03, project).",
    "Rename L01's observed price symbol (P_t, P_0 in L01.html:105-120, :143-144, :377, :450) to a symbol that no LX1 page uses (scan: the lowercase p and the uppercase Y do not occur in any LX1 page's math), or rename the price index in L02, L03 and the project. Then re-run check_pages, scans and the twins (L01 twin unchanged if only prose changes). The L03 page and its twin keep P_t unless the orchestrator chooses the other side.")

ledger = {
    "unit": "LX1",
    "slice": "b",
    "round": 14,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-b (L03, L04 and lab twins), round 14",
    "pin": "8e5751c903f0246115eba746afdf5d71f612bb37",
    "base": "e919577b45b431ce68e1e6533b00b8a301277937 (round-13 pin; delta read hunk by hunk)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE14-LX1-b",
    "scratch": "/tmp/lx1b-r14 (twin runs), /tmp/lx1b-r14-guard (guard copies), /tmp/lx1b-r14-disclaimer.html (licence page), /tmp/lx1b-r14-gates.log",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [
        "friedman1963monetary: registry record lists Friedman only (references/references.json, book, 1963); the curriculum string is 'Friedman & Schwartz (1963)' (curriculum/06-profession-capstone.yaml:37). The pages cite the key and the title only. The architect may correct via tools/add_reference.py (plan N2).",
        "Bernanke (1983), AER 73(3) (curriculum/06-profession-capstone.yaml:38): no registry record (plan B2, REFERENCE_REQUEST 2). L03 makes no empirical attribution to it.",
        "Bretton Woods (plan B3, REFERENCE_REQUEST 3): 0 hits in references/references.json and review_queue.json (grep, round 14). L04 defines no historical fact.",
    ],
    "freshness_flags": [],
    "notes": [
        "Mutants: none. LX1 is rubric-only and lab twins are demonstrations, so mutation testing does not apply to L03 or L04 (VERIFIER_RULES 2.5 and the rulings). Guard tests on the L04 twin (blank cell, non-decimal cell) were run as an evidence check, not as mutants (row lx1b-fx-guard).",
        "Gates run this round on 8e5751c (all exit 0 except as noted): check_pages, check_dag, check_projects, run_labs (7/7), run_graders (rubric), verify_refs --offline and --unit LX1, fetch_data --check, build_site --check ('site data current: 6 outputs'), page_smoke for L03 and L04 alone, ruff check and format, mypy --no-incremental on both twins, pytest -k LX1 and its collect-only. Script: " + S + "/gates_r14.sh; outputs in " + O + "/.",
        "Scripts backing rows (all under " + S + "/): gates_r14.sh, rederive_r14.py (Fraction and Decimal re-derivation), expected_l03_r14.py, compare_r14.py, scans_r14.py, guard_licence_r14.sh, make_fragment_r14.py. Outputs in out/.",
        "Non-findings noted for the orchestrator (benign, lesson-local): L03 k as a dummy index; L04 f(u) as a dummy function in P3; L04 s_1, s_2 dispersions beside L01's s as a dummy index in d_s. No cross-lesson meaning conflict is asserted for them.",
        "Out of slice: project.html (slice e) uses P_t for a price path, part of lx1b-notation-P. L01 (slice a) carries the conflicting P_t definition. The hub index.html card text for L04 ('Spot-rate dispersion from the embedded ... H.10 series') is not checked here (slice a).",
        "Not checked: the hub index.html content beyond the two card titles and hours (slice a); L01 and L02 lessons and their cards (slices a and c); the project, its rubric and exemplars (slice e) and the project twins (slice d); a Pyodide run of the twins outside page_smoke (run_labs runs CPython 3.14 with -I -W error; page_smoke is the page-level check); a live Friedman record check beyond verify_refs --unit LX1 (no Open Library or Crossref fetch by hand); the fx_monthly rebuild was not re-run this round (carried from round 13, byte-identical inputs).",
    ],
    "summary": "LX1-b round 14 on 8e5751c (base e919577): verdict FAIL. Rows: " + str(len(R)) + ". Non-PASS: lx1b-L04-bretton-definition (architect ruling still unrecorded; placeholder dfn), lx1b-notation-P (P_t is an observed price in L01 and a price index in L02, L03 and the project). lx1b-notation-N from round 13 is fixed and PASS.",
}

counts = {s: sum(1 for r in R if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
ledger["counts"] = counts
path = f"{ROOT}/ledgers/LX1/LX1-b.json"
with open(path, "w", encoding="utf-8") as h:
    json.dump(ledger, h, indent=2, ensure_ascii=False)
    h.write("\n")
print("wrote", path, counts)
