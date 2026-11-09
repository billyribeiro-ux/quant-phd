"""Writes the round-20 LX1 slice-b fragment (ledgers/LX1/LX1-b.json). Evidence cites repo paths under ledgers/LX1/scripts/LX1-b-r20/."""
import json
from datetime import datetime, UTC

O = "ledgers/LX1/scripts/LX1-b-r20/out/"
SC = "ledgers/LX1/scripts/LX1-b-r20/"
L01 = "course/modules/LX/LX1/L01.html"
L03 = "course/modules/LX/LX1/L03.html"
L04 = "course/modules/LX/LX1/L04.html"
CARDS = "course/modules/LX/LX1/cards.json"
rows = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- command rows (re-run this round on pin d1083bf1) ----
row("lx1b-check-pages", "2.9-structure", f"{L01}; {L03}; {L04}", "PASS",
    f"tools/check_pages.py --unit LX1 -> {O}check_pages.out: 'check_pages LX1: PASS', exit 0.")
row("lx1b-check-dag", "2.9-dag", f"{L01}; {L03}; {L04}", "PASS",
    f"tools/check_dag.py --unit LX1 -> {O}check_dag.out: 'check_dag LX1: PASS', exit 0.")
row("lx1b-check-projects", "2.6-projects", "tools/check_projects.py --unit LX1", "PASS",
    f"tools/check_projects.py --unit LX1 -> {O}check_projects.out: PASS, exit 0 (project page is slice a).")
row("lx1b-run-graders", "2.6-autograder", "tools/run_graders.py --unit LX1", "PASS",
    f"tools/run_graders.py --unit LX1 -> {O}run_graders.out: 'run_graders LX1: no autograder (grading: rubric)', exit 0.")
row("lx1b-run-labs", "2.5-labs", "tests/labs/LX1/lab-LX1-L01-1.py; lab-LX1-L03-1.py; lab-LX1-L04-1.py", "PASS",
    f"tools/run_labs.py --unit LX1 -> {O}run_labs.out: 'run_labs LX1: PASS (7/7)', exit 0.")
for L in ("L01", "L03", "L04"):
    row(f"lx1b-twin-alone-{L}", "2.5-labs", f"tests/labs/LX1/lab-LX1-{L}-1.py", "PASS",
        f"Twin run alone: cd to a scratch dir, python -I -W error tests/labs/LX1/lab-LX1-{L}-1.py -> {O}twin_{L}.out, exit 0 "
        f"(L04 with data/fx_monthly.csv copied into the scratch dir, because the twin reads data/ relative to cwd).")
row("lx1b-twin-equals-page-code", "2.5-labs", f"{L01}, {L03}, {L04} code and expected blocks vs twins", "PASS",
    f"{SC}twin_compare_r20.py -> {O}twin_compare_r20.out: page code equals twin (trailing newline stripped) for L01, L03, L04; "
    "expected block equals twin stdout for all three (38, 56, 17 lines). Strict byte equality is False only because the page "
    "block has no final newline; run_labs strips it.")
for L in ("L01", "L03", "L04"):
    row(f"lx1b-page-smoke-{L}", "2.9-smoke", f"course/modules/LX/LX1/{L}.html", "PASS",
        f"tools/page_smoke.py --unit LX1 --pages {L} -> {O}page_smoke_{L}.out: 'page_smoke modules/LX/LX1/{L}.html: PASS', exit 0.")
row("lx1b-ruff-mypy", "2.5-labs", "tests/labs/LX1/*.py", "PASS",
    f"ruff check tests/labs/LX1 -> {O}ruff_check.out 'All checks passed!'; ruff format --check -> {O}ruff_format.out '7 files already formatted'; "
    f"mypy --no-incremental tests/labs/LX1 -> {O}mypy.out 'Success: no issues found in 7 source files'.")
row("lx1b-pytest", "2.5-labs", "tests/test_labs.py", "PASS",
    f"python -m pytest tests/test_labs.py -q -> {O}pytest_labs.out, exit 0 (100%).")
row("lx1b-verify-refs", "2.1-citations", "references/references.json; tools/verify_refs.py", "PASS",
    f"tools/verify_refs.py --offline -> {O}verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'. "
    f"tools/verify_refs.py --unit LX1 (live Crossref) -> {O}verify_refs_live_LX1.out: '4 of 560 entries, 0 problems'.")
row("lx1b-citations-L01", "2.1-citations", f"{L01}:304, :489; references/references.json garber2000famous", "PASS",
    f"Registry record garber2000famous (title 'Famous First Bubbles: The Fundamentals of Early Manias', Garber, 2000, DOI "
    f"10.7551/mitpress/2958.001.0001, verified_by crossref) matches the page title and year at {L01}:489; the page states it "
    "cites the title only (line 304, :489). No passage is attributed, so no claim needs a locator check. Live verify_refs LX1 PASS.")
row("lx1b-citations-L03", "2.1-citations", f"{L03}:405, :640; references/references.json friedman1963monetary", "PASS",
    f"Registry record friedman1963monetary (title 'A monetary history of the United States 1867-1960', year 1963, authors "
    f"Friedman only, Open Library, ISBN 0691041474) matches {L03}:640 (title, key, no second author typed). The page takes "
    "no finding from it (:640). Live verify_refs LX1 PASS.")
row("lx1b-citations-L04", "2.1-citations", f"{L04}:571-573 (References)", "PASS",
    f"{L04}:571-573 cites no registry key; the one citation is the MANIFEST citation for fx_monthly, read against "
    "course/assets/data/market/MANIFEST.json ('Board of Governors ... G.5/H.10 Foreign Exchange Rates (noon buying rates in New York)', "
    "retrieved 2026-10-19). Matches.")
row("lx1b-fetch-check", "2.8-data", "course/assets/data/market/fx_monthly.csv; MANIFEST.json", "PASS",
    f"tools/fetch_data.py --check -> {O}fetch_check.out: 'fetch_data: 3 datasets, 0 problems', exit 0.")
row("lx1b-fx-rebuild", "2.8-data", "course/assets/data/market/fx_monthly.csv; MANIFEST fx_monthly; tools/fetch_data.py", "PASS",
    "Carried from round 19 (fx_monthly.csv, MANIFEST.json, tools/fetch_data.py and tools/data_sources.yaml byte-identical since "
    "cd4dd7df: `git diff --quiet cd4dd7df HEAD -- course/assets/data/market tools/fetch_data.py tools/data_sources.yaml` is silent). "
    "Round 19 rebuilt the CSV from the live feed in a scratch copy and the bytes matched the MANIFEST sha256; a live rebuild was not "
    "repeated this round.")
row("lx1b-fx-licence", "2.8-data", "tools/data_sources.yaml fx_monthly; MANIFEST licence_url", "PASS",
    f"plain curl https://www.federalreserve.gov/disclaimer.htm -> HTTP 200 (recorded in {O}fed_disclaimer_r20.html). The page contains "
    "'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without "
    "permission. Please cite to the Board as the source of the information.' This is the quoted licence in the MANIFEST and "
    "tools/data_sources.yaml fx_monthly entry: a redistribution grant.")
row("lx1b-fx-guard", "2.8-data", "tests/labs/LX1/lab-LX1-L04-1.py load_column, parse_rate", "PASS",
    f"{SC}fail_loud_L04_r20.py -> {O}fail_loud_L04_r20.out: blank GBP cell, text cell, missing month, zero rate and missing GBP "
    "column each raise ValueError. 'all raise: True'.")
row("lx1b-fx-gbp-clean", "2.8-data", "course/assets/data/market/fx_monthly.csv (GBP)", "PASS",
    f"{SC}rederive_L04_r20.py -> {O}rederive_L04_r20.out: 'GBP blank cells 0'; 669 rows 1971-01 to 2026-09; consecutive months True.")
row("lx1b-honest-data", "2.8-data", f"{L03}:76; {L04}:112-114; {L01}:131-133", "PASS",
    f"Re-read this round. {L03}:76 honest-pending note (no redistributable gold or output series; the lab is SIMULATED). "
    f"{L04}:112-114 labels Part A SIMULATED and states Parts B to D read only fx_monthly.csv. {L01}:131-133 labels the price path SIMULATED.")
row("lx1b-L04-simulated-label", "2.8-data", f"{L04}:113, :114; tests/labs/LX1/lab-LX1-L04-1.py docstring", "PASS",
    f"{L04}:113 heading 'Lab 1 · Part A SIMULATED'; :114 hypothesis says Part A is a constructed model check and Parts B to D are not SIMULATED; "
    "twin docstring states Part A is a SIMULATED model check, not data.")
row("lx1b-L04-manifest-note", "2.8-data", f"{L04}:112, :114, :117-123", "PASS",
    f"{L04}:114 names the dataset, licence owner, retrieval date 2026-10-19 and MANIFEST id; {L04}:117-123 states the window and "
    "MANIFEST facts, checked against MANIFEST.json (first 1971-01, last 2026-09, 669 rows, fx_daily/ust_daily first 2000-01-03).")
row("lx1b-open-items-missing", "2.9-structure", "plans/LX1-open-items.md", "PASS",
    "plans/LX1-open-items.md exists and carries D-1 (L03 data request), the Bretton Woods pending definition, and the three "
    "reference requests (credit channel B2, Kindleberger N1, Friedman record N2), as the L03 and L04 honest-pending notes cite.")
row("lx1b-plan-coverage", "2.9-structure", "plans/LX1-build-plan.md §2.1, §3; plans/FINAL-ARCHITECT-RULINGS.md rulings 14, 16", "PASS",
    "Plan §2.1 items 1-12 read against the pages: 1 (numbers unrounded, per-number rule stated), 2 (lab statements checked), "
    "3 (no unread attribution), 4 (scope words, reviewed in lx1b-scope-words), 5 (7 concepts defined once), 6 (numbered assumptions), "
    "8 (integer cents: L01 Part A/B, L03 Parts A-B), 9 (page_smoke PASS), 10 (twins call main() unguarded, no __main__), "
    f"11 (basis-explicit), 12 (fail loud, {SC}fail_loud_L04_r20.out). Ruling 14 permits the 'definition pending' dfn for "
    f"bretton-woods-system ({L04}:86). Ruling 16: P_t in L03 (price index), A_t in L01 (observed price), both as ruled.")
row("lx1b-hours", "2.9-structure", f"{L01}:2, :34; {L03}:2, :34; {L04}:2, :34; course/modules/LX/LX1/index.html:29", "PASS",
    "Each lesson page: data-hours=\"10\" (L01 :2, L03 :2, L04 :2) and the eyebrow reads 10 study hours; hub split 40/10 is checked by check_pages PASS.")
row("lx1b-delta-hunks", "2.9-structure", "git diff cd4dd7df d1083bf1 for slice b: L03.html:142, :383; L04.html:448; cards.json LX1-c092",
    "PASS", f"Delta saved at {O}delta_cd4dd7df_d1083bf1_LX1.diff (72 lines). Every hunk in slice b read and re-verified: "
    f"L03:142 (Part D description now says X over Y; matches twin Part D code 'ratio of depths X to Y'); L03:383 (Part D "
    f"interpretation 'as Corollary 3.4 implies'; Corollary 3.4 proves the RHS does not depend on beta or phi); L04:448 (R1 "
    f"solution now defines s_1, s_2 from Definition 1.1 at {L04}:58-59); cards.json c092 (see lx1b-cards-c092-hypothesis, FAIL).")

# ---- prior-round rows, re-verified (subjects changed or re-read this round) ----
row("lx1b-num-L01-closed-form", "2.2-numbers", f"{L01}:132, :87, :282, :396-399, :417-435", "PASS",
    f"{SC}rederive_L01_r20.py -> {O}rederive_L01_r20.out: F0 = 20000/3 (rounds 6667); q = 103/109; S_N identity exact for N=10,60,200 "
    "(True); F0 q^N rounds 3785, 223, 0; F2 = 7072.67 rounds 7073; 250/0.06 = 4166.67 -> 4167 (Mech 1); F3 = 4686.93 -> 4687 (Mech 2); "
    "S10 = 20000/21 (Mech 3); g* = 0.023333 (Research 1).")
row("lx1b-num-L01-lab-output", "2.5-labs", f"{L01}:244-282 (expected block) vs twin stdout", "PASS",
    f"{O}twin_compare_r20.out: expected block equals twin stdout (38 lines). Independent gaps and counts in {O}rederive_L01_r20.out "
    "reproduce the twin: gaps [-200, 68, 141, 146, 301, 0, -398, 2050, 676, 2175, 2151, -92, 285], 9 of 13 positive, largest 2175 at t=9, "
    "13 of 13 under 1 percent.")
row("lx1b-num-L01-prose", "2.2-numbers", f"{L01}:282, :363, :367, :370-371, :378, :400", "PASS",
    f"{SC}rederive_L01_r20.py: 9/13 = 0.6923 (Empirical 1); 13-9=4 (Empirical 2); 2175/8698 = 25.0057 percent -> 25.01; "
    "unrounded fundamental at t=9 = 8698.4879 -> 8698.49; gap 0.25 x fundamental = exactly 25.00 percent (Empirical 3 arithmetic, "
    "verified by hand against the exact Fraction 0.25 wedge at t=9, twin line 't = 9: wedge +0.25'); 1.03^9 check.")
row("lx1b-num-L01-witness", "2.2-numbers", f"{L01}:114, :120, :321, :462", "PASS",
    f"Proposition 2.2 witness: 400/0.08 = 5000 cents, 400/0.06 = 6666.67 cents, gaps +1000 and -2000/3 (exact arithmetic). "
    f"Twin output {O}twin_L01.out Part C line 't =  0: alternative fundamental 5000 cents' agrees with the 1 percent benchmark.")
row("lx1b-num-L01-s5-example", "2.2-numbers", f"{L01}:310, :322; quiz {L01}:417-421; misconception 2 {L01}:323", "PASS",
    f"400/1.09 = 40000/109 = 366.9724770642 -> 367, and the closed form at g = 3 percent = 6666.67 -> 6667 ({SC}problem_checks_r20.py, "
    f"{O}problem_checks_r20.out line 'L01 s5 example').")
row("lx1b-num-L03-depth", "2.2-numbers", f"{L03}:149, :362-363, :383, :491, :496-498, :545-546, :577, :596", "PASS",
    f"{SC}rederive_L03_r20.py -> {O}rederive_L03_r20.out: depth X exact 9.204597 -> 9.20; depth Y 2.686713 -> 2.69; difference "
    "6.517884 -> 6.52 (printed depths differ by 6.51, as line 383 says); Part C depths 0.64 ... 9.20 match; ratio 3.425969 -> 3.4260 "
    "for products 1/2, 1, 3 and for six (phi, beta) pairs (one distinct value).")
row("lx1b-num-L03-path", "2.2-numbers", f"{L03}:331-357 (expected block) vs twin", "PASS",
    f"{SC}compare_L03_partA_r20.py -> {O}compare_L03_partA_r20.out: 26 Part A rows (economies X and Y, t=0..12) of the twin output "
    "match the independent Fraction derivation ({SC}rederive_L03_r20.py) in index, real debt, leverage, premium and output fall: 0 mismatches.")
row("lx1b-num-L03-M-E-Q", "2.2-numbers", f"{L03}:441, :448, :455, :491, :498, :505, :596, :610", "PASS",
    f"{SC}problem_checks_r20.py -> {O}problem_checks_r20.out: M1 P4 = 5764801/6250000 = 0.92236816, V4 = 1084165.7847 -> 1084166; "
    "M2 K4 = 3915834.2153 -> 3915834; M3 L4 = 0.2768671 -> 0.2769; quiz real debt X at t=12: 1274345.2124 -> 1274345; E1 exact depth "
    "2.6867; E2 difference 9.20-2.69 = 6.51 vs 6.517884 -> 6.52.")
row("lx1b-num-L04-stats", "2.2-numbers", f"{L04}:306-322 (expected), :323, :476-477", "PASS",
    f"{SC}rederive_L04_r20.py -> {O}rederive_L04_r20.out: sd window one 0.027935278 -> 0.027935; window two 0.024699501 -> 0.024700; "
    "668 changes; 321 changes; 3 exact zeros 1976-07, 2012-07, 2019-11; 665 nonzero; largest |change| 0.1358457 at 1985-03; "
    "0.0965747 at 2008-10 (signed -); telescoping error < 1e-15 both windows.")
row("lx1b-num-L04-display-diff", "2.2-numbers", f"{L04}:323; key row {L04}:476", "PASS",
    f"{O}rederive_L04_r20.out: unrounded difference -0.00323578 -> -0.003236; difference of printed sds = -0.003235 "
    f"(page line 323 says so); ratio 0.8841688 -> 0.8842.")
row("lx1b-num-L04-derived", "2.2-numbers", f"{L04}:354, :373, :380, :387, :430, :455, :541, :564", "PASS",
    f"{SC}problem_checks_r20.py -> {O}problem_checks_r20.out: ln 1.1 = 0.095310; simple change 0.1; difference 0.004690 (M1, misconception 3); "
    "M2 mean 0.006667, sd 0.025166; E2 simple change -0.092058; R2 h = tanh(z/2) = 0.067819 -> 0.0678 (4 dp), bound at 0.0678 = 0.135808 -> 0.1358; "
    "quiz 0.095310; M3 321.")
row("lx1b-scope-start", "2.2-numbers", f"{L04}:110, :326, :387, :462; card LX1-c063; twin docstring 127-130", "PASS",
    "Window two starts 2000-01 because fx_daily and ust_daily begin 2000-01-03 (MANIFEST.json first fields); the change dated "
    "2000-01 uses the 1999-12 rate (rederive_L04_r20.py dict lookup). Stated as a convention with its reason (lines 387, 462).")
row("lx1b-math-L01", "2.4-mathematics", f"{L01}:57-99", "PASS",
    f"Re-read: Assumption 1.1 (A0, A1); Theorem 1.3 proof: q in (0,1) under A0, 1-q = (r-g)/(1+r), S_N = F*_t (1-q^N); "
    "Definition 1.2 series. All steps re-derived. Non-hypothesis claims are correct; the Proposition 1.4 issue is in lx1b-L01-prop14-hypotheses.")
row("lx1b-math-L01-prop22", "2.4-mathematics", f"{L01}:104-121", "PASS",
    "Proposition 2.2 hypotheses (A3) d1>0, (A4) r>g, r>g', 1+g>0, 1+g'>0, g<g'. Proof: r-g > r-g' > 0, reciprocal inequality, "
    "gap signs. Re-derived; witness numbers in lx1b-num-L01-witness.")
row("lx1b-math-L03", "2.4-mathematics", f"{L03}:94-143", "PASS",
    "Lemma 3.1 identity lambda(y)-lambda(x) = C(y-x)/((C-x)(C-y)) re-derived; Prop 3.2 (a),(b),(c) proofs re-derived under Assumptions 1.1-1.3; "
    "Cor 3.3 proof (V_m' < V_m < C) correct; Cor 3.4 ratio cancels beta*phi (both depths carry the factor). Hypotheses stated for each.")
row("lx1b-math-L04", "2.4-mathematics", f"{L04}:57-107", "PASS",
    "Proposition 1.2 (A1 positivity) telescoping proof by cancellation and induction (problem P1) correct; Proposition 2.2 under (A2) correct; "
    "Remark 1.3 tolerance statement matches the twin's SUM_TOLERANCE = 1e-12.")
row("lx1b-math-problems", "2.4-mathematics", f"{L01}:330-389; {L03}:431-532; {L04}:363-466", "PASS",
    f"Every worked solution re-derived or checked by {SC}problem_checks_r20.py and {SC}rederive_*_r20.py. Proof problems P1-P3 (L04) "
    "and Proof 1-3 (L01) re-read: Proof 3 (L01) correctly carries r > -1 in its hypotheses, which shows the omission elsewhere is a slip.")
row("lx1b-grades", "2.3-grades", f"{L01}:396-401; {L03}:542-546; {L04}:474-477; cards grades", "FAIL",
    f"Grades re-graded against BLUEPRINT §3 (T for proved results, C for lab outputs, C for L04 data results). Every grade matches. "
    f"The one FAIL is the key-results row at {L01}:399 ('No finite benchmark when g >= r and d1 > 0', grade T): the T result is Proposition 1.4, "
    "whose hypotheses include r > -1 and 1+g > 0, and the summary omits them.",
    fix=f"{L01}:399: change the row to 'No finite benchmark when d_1 > 0, 1 + g > 0, r > -1 and g >= r'.")
row("lx1b-notation", "2.4-notation", f"{L01}; {L03}; {L04}; cards (L01, L03, L04); twins", "PASS",
    "notation/notation.json symbols: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. Scan of the math spans of the three pages "
    f"({SC}out/ scan outputs) finds none of them; the only starred symbol is F^{{\\ast}}_t (L01), which is not registered. Macros \\E and \\Prob not used.")
row("lx1b-notation-P", "2.4-notation", f"{L01} (whole page); {L03}:58-59, :116, :157-163; L02.html:77", "PASS",
    "P_t is the price index in L03 (P_t = (1-delta)^min(t,m)); L01 uses A_t for the observed price (ruling 16). L04 does not use P.")
row("lx1b-notation-A", "2.4-notation", f"{L01}:105, :114, :119-120, :143-144, :377, :450; cards LX1-c006, c007, c093", "PASS",
    "A_t is the observed price (Definition 2.1). The assumption labels (A0)-(A4) and (A1)/(A2) are labels, not symbols of the price path; no conflict.")
row("lx1b-notation-K", "2.4-notation", f"{L03}:65 (first use) to :605; cards c027, c071, c082", "PASS",
    "K_t is borrower net worth, K_0 baseline (Assumption 1.2, first use line 65). Cards and quiz use the same meaning.")
row("lx1b-notation-P-L03", "2.4-notation", f"{L03}:58-59, :116, :157-163, :211, :464-473", "PASS",
    "P_t price index; the same symbol in Assumption 1.1 and in the lab. Consistent with ruling 16.")
row("lx1b-notation-N", "2.4-notation", f"{L01}:67, :74, :82-83, :87; {L04}", "PASS",
    "N is a number of terms in the partial sums S_N (L01), and L04 uses n for counts. No registered meaning of N or n is changed.")
row("lx1b-notation-registered", "2.4-notation", f"{L01}; {L03}; {L04} math spans; notation/notation.json macros", "PASS",
    "Registered macros (\\E, \\Prob, \\Var, \\Cov, \\R) do not occur in the math spans of these pages; no registered symbol changes meaning.")
row("lx1b-notation-check-math-spans", "2.4-notation", f"{L01}.html math spans", "PASS",
    f"Math spans scanned by {SC}prose_scan_r20.py (MATH markers) and the symbol inventory above: no unregistered macro, no reuse of a registered symbol.")
row("lx1b-dag-links", "2.9-dag", f"{L01}:37; {L03}:37, :54, :90; {L04}:37-38, :105", "PASS",
    "Every data-concept link resolves: L01 uses growing-perpetuity, present-value, geometric-series, exponential-and-logarithm (all M1 per "
    "curriculum/curriculum.json concepts); L03 links L02 #def-debt-deflation and #def-gold-standard; L04 links L02 #def-gold-standard and L03 #def-lender-of-last-resort. "
    "Anchors verified present (grep id=\"def-...\").")
row("lx1b-dag-outside-closure", "2.9-dag", f"{L03}:390, :402, :413-418; {L04}:336; {L01}", "PASS",
    "Scan for the D1-D15 concept names (bank-run, fire-sale, leverage-cycle, banking-crisis, covered/uncovered-interest-parity, "
    "efficient-markets, moral-hazard, fisher, bank reserves, credit-default-swap, term-spread, crisis-mechanism-map, expectation, "
    "sovereign-default) on the three pages: none found. 'bank failures' (L03 misconception 1) is a phrase, not a concept name, and "
    "is plain prose.")
row("lx1b-concepts-defs", "2.9-dag", f"{L01}:105, :289; {L03}:87, :390; {L04}:86; course/concepts.html:631-636", "PASS",
    "Each of the 7 concepts has exactly one data-concept dfn across L01-L04: speculative-bubble, financial-panic (L01); gold-standard, "
    "debt-deflation (L02); credit-channel-depression, lender-of-last-resort (L03); bretton-woods-system (L04, pending per ruling 14). "
    "grep of dfn ids across L01-L04 finds no duplicate.")
row("lx1b-concept-index-title", "2.9-dag", "course/concepts.html:631-636", "PASS",
    "course/concepts.html identical to cd4dd7df (git diff --quiet). The entries (lines 631-636) link the defining lesson anchors "
    "(L04 #def-bretton-woods-system, L02 #def-debt-deflation, L01 #def-financial-panic, L02 #def-gold-standard, L03 #def-lender-of-last-resort, L03 #def-credit-channel-depression) and match the dfn ids above.")
row("lx1b-L04-bretton-definition", "2.4-mathematics", f"{L04}:38, :86, :337, :358, :553-557", "PASS",
    f"{L04}:86 is the 'definition pending' dfn. Ruling 14 (plans/FINAL-ARCHITECT-RULINGS.md:32-34) permits this honest-pending state for LX1 L04 "
    f"bretton-woods-system; the page states the fixed-exchange-rate model is not a definition of the historical system ({L04}:86) and "
    "that no date for the end is stated (quiz item 10, {L04}:553-557). Open item recorded in plans/LX1-open-items.md.")
row("lx1b-banned-phrases", "2.9-prose", f"{L01}; {L03}; {L04}; cards.json", "PASS",
    f"{SC}prose_scan_r20.py -> {O}prose_scan_r20.out: ellipsis outside code/math 0 on each page; banned-literal hits 0 "
    "(TODO, TBD, lorem, for brevity, details omitted, left as an exercise).")
row("lx1b-process-words", "2.9-prose", f"{L01}; {L03}; {L04}; cards.json", "PASS",
    f"{SC}prose_scan_r20.py: no build, builder, verifier, round (as process), REQUESTS or unit-report word in learner text. "
    "The 'rounds' hits are arithmetic verbs.")
row("lx1b-scope-words", "2.9-prose", f"{L01}; {L03}; {L04} (hits in {O}prose_scan_r20.out)", "PASS",
    f"{SC}prose_scan_r20.py: 225 hits (scope/process words) read one by one: 'every', 'all', 'any', 'only', 'exactly', 'never', "
    "'same', 'the first', 'shows', 'proves' each sit inside a derivation, a lab sentence, a definition or a misconception, and the "
    "claim is supported. Exception: the 'grow without bound' sentences (L01:313, :324) are covered by lx1b-L01-prop14-hypotheses.")
row("lx1b-structure", "2.9-structure", f"{L01} sections 1-10; {L03} sections 1-10; {L04} sections 1-9", "PASS",
    "Each page has: header, grade legend, why-it-matters, definitions/theorems with numbered assumptions, lab (SIMULATED where generated), "
    "canon-breaks, misconceptions (3, 4, 4), problem set (3 per tier in each lesson), key results, quiz (10, 11, 11 items), references.")
row("lx1b-quiz-explanations", "2.9-structure", f"{L01}:439-445 (quiz 6); {L01}:405-483; {L03}:552-636; {L04}:483-567", "FAIL",
    f"Read against each lesson. L01 quiz 6: prompt at {L01}:439 'Which statement follows from Proposition 1.4 when d1 > 0 and g >= r?' and "
    f"explanation at :445 ('Each discounted term is at least d1/(1+r)') both omit r > -1 and 1+g > 0, which Proposition 1.4 requires. "
    "Other quiz explanations (L01, L03, L04) agree with their lessons, verified against the lab outputs.",
    fix=f"{L01}:439: prompt to 'Which statement follows from Proposition 1.4 when d_1 > 0, 1 + g > 0, r > -1 and g >= r?'; "
        f"{L01}:445: name the hypothesis r > -1 (it is what makes each term at least d_1/(1+r) > 0).")
row("lx1b-L03-remark42-solvency", "2.4-mathematics", f"{L03}:64-67, :395", "PASS",
    "Remark 4.2: K_t = C - V_t, V_t <= V_m < C by Prop 3.2(a) and Assumption 1.2, so K_t > 0 each period. Re-derived.")
row("lx1b-L03-ratio-claims", "2.4-mathematics", f"{L03}:404; :516; :523", "PASS",
    "Canon-breaks ratio claims (depends on the shape, not the scale; squared premium gives the squared ratio, which differs from the "
    "ratio whenever the ratio is not 0 or 1; ratio X over Y is above 1) re-derived: depth ratio 3.426 > 1, so the square differs.")
row("lx1b-L03-r1-no-result", "2.4-mathematics", f"{L03}:516", "PASS",
    "Problem R1 states no new result; the extension description is prose with no claim about a facility's effect.")
row("lx1b-L03-lab-checks-overreach", "2.5-labs", f"{L03}:145, :383; twin docstring 25-26 and code 171-174", "PASS",
    "Part D code computes ratios and prints them; no equality test (verified in twin source lines 171-174). Interpretation 'as Corollary 3.4 implies' "
    "does not overreach the printed equality (three values, same to four decimals).")
row("lx1b-L03-misconception-scope", "2.4-mathematics", f"{L03}:413-426; proof :128-131", "PASS",
    "Misconceptions 1-4 re-read: no bank or failure in the model (Assumption 1.2), Corollary 3.3 proof uses only m, m', V_m formula and the bound, "
    "lending misconception matches Definition 4.1, and beta proportionality matches Prop 3.2(b).")
row("lx1b-cards-l01-l03-l04", "2.7-cards", f"{CARDS} (L01 17, L03 32, L04 24)", "PASS",
    f"{SC}cards_check_r20.py -> {O}cards_check_r20.out: 90 cards in total, unique ids, 73 cards for L01/L03/L04 (17/32/24); "
    "every cited key exists in the registry (560 entries); every number in front/back appears in its lesson text. "
    "Duplicate scan: no duplicate fronts or backs.")
row("lx1b-cards-c052-c053", "2.7-cards", f"cards.json LX1-c052, LX1-c053 vs {L04}:84-94", "PASS",
    f"Carried from round 19 (cards c052 and c053 byte-identical to cd4dd7df per {O}cards_check_r20.out 'cards differing from cd4dd7df: "
    f"['LX1-c092']'; {L04}:84-94 unchanged, the only L04 hunk is :448). c053 re-read this round against Definition 2.1 "
    "(anchor currency, fixed exchange rate, market rate): matches.")
row("lx1b-cards-L01-hypotheses", "2.7-cards", f"cards.json LX1-c002..c007, c013, c085, c086, c092, c093", "FAIL",
    f"c002-c007, c013, c085, c086, c093 re-read against L01 and match. c092 does not: its front omits the hypotheses of Proposition 1.4 "
    "(see lx1b-cards-c092-hypothesis).",
    fix="cards.json LX1-c092: restore the hypotheses of Proposition 1.4 in the front (d_1 > 0 and 1 + g > 0; r > -1 and g >= r).")
row("lx1b-cards-L03-hypotheses", "2.7-cards", "cards.json LX1-c030..c036, c079, c082, c087", "PASS",
    f"Each card's hypothesis (Assumptions 1.1-1.3; Lemma/Proposition/Corollary 3.x) re-read against {L03}:58-143 and matches; "
    f"c067 re-read against {L03}:383 (now 'as Corollary 3.4 implies'; card back says 'as Corollary 3.4 implies'): match.")
row("lx1b-cards-c092-hypothesis", "2.7-cards", "course/modules/LX/LX1/cards.json LX1-c092 (front)", "FAIL",
    "Front: 'With d_1 > 0 and g >= r, what does the closed form d_1/(r - g) give as the present value of the dividends?' Back: 'No present value.' "
    "Proposition 1.4 needs (A1) d_1 > 0 and 1 + g > 0, and (A2) r > -1 and g >= r. Without r > -1 the back is false: with d_1 = 1, r = -2, "
    f"g = -1/2 (d_1 > 0 and g >= r hold, 1 + g > 0 holds), the partial sums are -1, -0.5, ... -> -2/3 ({SC}rederive_L01_r20.py output "
    f"'counterexample', {O}rederive_L01_r20.out line 'S_1, S_2, S_10, S_40'), so the series converges and has a finite present value. "
    "The card before 50559266..cd4dd7df had the full hypotheses; the later edit dropped them.",
    fix="cards.json LX1-c092 front: 'With d_1 > 0, 1 + g > 0, r > -1 and g >= r (Proposition 1.4), what does the closed form d_1/(r - g) give "
        "as the present value of the dividends?' Back unchanged.")
row("lx1b-L01-prop14-hypotheses", "2.4-mathematics", f"{L01}:99, :313, :399, :439, :445 (see also :324)", "FAIL",
    f"Lesson prose and summaries state 'With d_1 > 0 and g >= r, the partial sums grow without bound / no finite benchmark' without "
    f"r > -1 (and 1+g > 0), which Proposition 1.4 (line 91) and its proof (line 96, q >= 1 needs 1+r > 0) require. Counterexample with "
    f"d_1 = 1, r = -2, g = -1/2: S_N(0) -> -2/3 (finite), not +infinity ({O}rederive_L01_r20.out). Proof 3 (L01 :357) carries r > -1 correctly.",
    fix=f"{L01}:99, :313, :399 and :439/:445: add 'r > -1 and 1 + g > 0' to each statement of the g >= r case (as Proposition 1.4 does); "
        f"keep the Proposition 1.4 statement at :91 as it is.")
row("lx1b-L01-misc3-closed-form", "2.9-prose", f"{L01}:324 (misconception 3); card LX1-c092", "FAIL",
    f"Misconception 3: 'Under g >= r with d_1 > 0, each discounted dividend is at least d_1/(1 + r), so the partial sums grow without bound.' "
    "The inference needs 1 + r > 0 (q >= 1 and d_1/(1+r) > 0). Counterexample d_1 = 1, r = -2, g = -1/2 (the same as "
    "lx1b-L01-prop14-hypotheses): partial sums converge to -2/3, not +infinity. The evidence sentence cites Proposition 1.4, which has r > -1.",
    fix=f"{L01}:324: state 'Under g >= r with d_1 > 0, r > -1 and 1 + g > 0, ...'; the card fix is in lx1b-cards-c092-hypothesis.")
row("lx1b-L01-benchmark-finite-hypothesis", "2.4-mathematics", f"{L01}:99", "FAIL",
    "'With d_1 > 0, a benchmark that depends on a growth rate at or above the discount rate is not a finite present value' omits r > -1: "
    "the counterexample (d_1 = 1, r = -2, g = -1/2) gives a finite present value -2/3 under the closed form d_1/(r-g) = -2/3.",
    fix=f"{L01}:99: add 'and r > -1 and 1 + g > 0' to the hypothesis.")
row("lx1b-mutants-none", "2.6-mutation", "tests/labs/LX1/*", "PASS",
    "Lessons and lab twins carry no grader; LX1 is rubric-only (curriculum/06-profession-capstone.yaml:49), and lab twins are demonstrations "
    "(VERIFIER/ruling). No mutants are listed for slice b.")

# ---- new round-20 checks ----
row("lx1b-r20-L03-independent-derivation", "2.2-numbers", f"{L03} Lemma 3.1, Prop 3.2, Cor 3.3-3.4", "PASS",
    f"{SC}rederive_L03_r20.py (closed form of Prop 3.2(b) vs path maximum: equal for m=0..12; ratio constant over 6 (phi,beta) pairs).")
row("lx1b-r20-L01-lab-replay", "2.5-labs", f"tests/labs/LX1/lab-LX1-L01-1.py", "PASS",
    f"{SC}rederive_L01_r20.py replays the seeded wedges with Fractions and reproduces every printed Part B and Part C count.")
row("lx1b-r20-L04-lab-replay", "2.5-labs", "tests/labs/LX1/lab-LX1-L04-1.py", "PASS",
    f"{SC}rederive_L04_r20.py reproduces the printed sds, difference, ratio, zero months and extremes from the CSV (independent of the lab's helpers).")
row("lx1b-r20-L04-R2-band", "2.2-numbers", f"{L04}:452-455 (R2 solution); quiz {L04}:563-565", "PASS",
    f"{SC}problem_checks_r20.py: h = tanh(z/2) = (e^z - 1)/(e^z + 1) = 0.0678186; bound at h = 0.0678 is 0.1358084, short of z = 0.1358457; "
    "d/dh ln((1+h)/(1-h)) = 2/(1-h^2) > 0 (strictly increasing), so the smallest h is the closed form.")
row("lx1b-r20-L04-proof-P2-P3", "2.4-mathematics", f"{L04}:393-418 (proof problems P2, P3)", "PASS",
    "P2 band bound |l_t| <= ln((1+h)/(1-h)) re-derived (upper and lower ratio bounds, log monotone). P3 ln(1+u) <= u with equality only at u = 0 "
    "re-derived via f'(u) = -u/(1+u); the sign of f' on (-1,0) and (0,inf) is correct.")
row("lx1b-r20-L03-M-proof-P1-P3", "2.4-mathematics", f"{L03}:431-520 (M1-M3, P1-P3, E1-E3, R1-R3)", "PASS",
    "P1 monotone P_t and V_t; P2 depth(0)=0 when m=0; P3 lambda difference identity: each re-derived (manual and "
    f"{SC}problem_checks_r20.py). R1-R3 read; R2's generalisation to G(V_t) is correct (Prop 3.2(a) and strictly increasing G).")
row("lx1b-r20-fail-loud-L04", "2.8-data", "tests/labs/LX1/lab-LX1-L04-1.py load_column", "PASS",
    f"{SC}fail_loud_L04_r20.py: 5 mutated CSVs all raise ValueError (see {O}fail_loud_L04_r20.out).")
row("lx1b-r20-scope-words-readthrough", "2.9-prose", f"{L01}; {L03}; {L04}", "PASS",
    f"{SC}prose_scan_r20.py output read in full (234 lines); each scope hit is inside a derivation, a model/lab sentence, a definition or a misconception, except the g >= r sentences already logged.")
row("lx1b-r20-dfn-anchors", "2.9-dag", f"{L01}; {L03}; {L04}", "PASS",
    "All anchors used by links exist: L02 #def-gold-standard, #def-debt-deflation; L03 #def-lender-of-last-resort, #def-credit-channel-depression; L04 #def-bretton-woods-system; L01 #def-speculative-bubble, #def-financial-panic.")
row("lx1b-r20-sampled-cards", "2.7-cards", f"{CARDS} sampled LX1-c001, c009, c029, c037, c045, c053, c061, c067, c071, c085, c093",
    "PASS", "Sample of 11 of 73 cards (one per ~7) re-read against the lesson text: each back matches its lesson statement and number (c001 definition; "
    "c009 and c037 lab outputs; c029 Definition 2.2; c045 Definition 4.1; c053 Definition 2.1; c061 Problem M1; c071 Assumption 1.2; c085 recursion; c093 Proposition 2.2 witness).")
row("lx1b-r20-licence-page-curl", "2.8-data", "https://www.federalreserve.gov/disclaimer.htm (plain curl)", "PASS",
    f"HTTP 200 (curl -sS -L); quote present once in {O}fed_disclaimer_r20.html. No bot check or login was encountered or bypassed.")

verdict = "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS"
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment = {
    "unit": "LX1",
    "slice": "b",
    "round": 20,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-b (L01, L03, L04 and lab twins), round 20",
    "pin": "d1083bf1 (d1083bf142be6e33189af7de81d83719288ed2fb), detached; .venv symlinked; vendor copied",
    "base": "cd4dd7df (round-19 pin). Delta cd4dd7df..d1083bf1 touches slice b in L03.html:142, :383; L04.html:448; cards.json LX1-c092 (saved as out/delta_cd4dd7df_d1083bf1_LX1.diff). L01.html and both twins L01 and L03/L04 twins are byte-identical to cd4dd7df; the L03 and L04 twins are byte-identical too.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE20-LX1-b",
    "scratch": "/tmp/lx1b-r20-twin-L0{1,3,4} (removed after each run); no other scratch",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "friedman1963monetary: registry record lists Friedman only; curriculum string names Friedman & Schwartz (plan N2). Pages cite the key only; the architect may correct the record via tools/add_reference.py.",
        "B2: Bernanke (1983) AER 73(3) credit-channel source is not in references/references.json (review_queue.json:1610 candidate is an NBER working paper and must not be admitted as the AER article). L03 makes no empirical credit-channel claim.",
        "N1: Kindleberger & Aliber (2015) not in the registry (review_queue.json:1557). No LX1 page cites it.",
        "B3: no admitted source for the Bretton Woods definition or end date. L04 carries the ruling-14 'definition pending' dfn; this is an honest gap to be closed by a REFERENCE_REQUEST.",
        "Bubble-existence counter-account (REFERENCE_REQUEST 4): no registered key addresses bubble existence. kaldor1939speculation (X3) is a 1939 speculation-and-stability paper and is not treated as a counter-account.",
    ],
    "freshness_flags": [],
    "notes": [
        "Round 20 ran every command row on d1083bf1: check_pages, check_dag, check_projects, run_labs, run_graders (no autograder), each twin alone under python -I -W error (L04 with a data/ copy), page_smoke for L01, L03, L04 alone, ruff check and format, mypy --no-incremental, pytest tests/test_labs.py, verify_refs --offline and --unit LX1 (live), fetch_data --check. All PASS.",
        "Full read this round: L01.html all lines (lab code compared to the twin by script, expected block compared to twin stdout); L03.html all lines; L04.html all lines. Twins L01, L03, L04 read in full. All 73 L01/L03/L04 cards checked by script; 11 sampled and read against the lesson; cards.json diff vs cd4dd7df is c092 only.",
        "Independent re-derivations (own Fraction code, not the lab's helpers): L01 numbers and the seeded Part B/C replay; L03 closed form vs path maximum and Part A table (26 rows, 0 mismatches); L04 statistics, zero months, extremes, telescoping; worked-solution and quiz numbers.",
        "Round-19 FAIL rows resolved: lx1b-L03-corollary34-wording (L03:383 now 'as Corollary 3.4 implies', matching card c067 and Corollary 3.4), lx1b-L04-R1-undefined-subscripts (L04:448 now defines s_1, s_2 from Definition 1.1 at :58-59).",
        "New defect class found this round: a hypothesis omission in Proposition 1.4 (r > -1, 1 + g > 0) across L01:99, :313, :324, :399, quiz 6 (:439/:445) and card LX1-c092. Round 19 carried these rows as PASS; the counterexample (d_1=1, r=-2, g=-1/2) shows they fail. Rows are FAIL, not carried.",
        "Scope and notation scans, DAG links and outside-closure name scan, banned-phrase scan, sampled cards: PASS as listed.",
        "Mutants: none. LX1 is rubric-only and lab twins are demonstrations (rulings); no grader mutants apply to slice b.",
    ],
    "summary": (
        f"LX1-b round 20 on d1083bf1 (base cd4dd7df): verdict {verdict}. Rows: {len(rows)} (pass={counts['PASS']} "
        f"fail={counts['FAIL']} unverifiable={counts['UNVERIFIABLE']}). Non-PASS: lx1b-L01-prop14-hypotheses, lx1b-L01-misc3-closed-form, "
        "lx1b-L01-benchmark-finite-hypothesis, lx1b-quiz-explanations, lx1b-grades (key-results row L01:399), lx1b-cards-c092-hypothesis, "
        "lx1b-cards-L01-hypotheses. Root cause: Proposition 1.4's (A2) r > -1 and (A1) 1+g > 0 are dropped in prose, quiz and card. "
        "Round-19 FAILs (L03 Corollary 3.4 wording, L04 R1 subscripts) are fixed and PASS."
    ),
}
with open("ledgers/LX1/LX1-b.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(rows), counts, verdict)
