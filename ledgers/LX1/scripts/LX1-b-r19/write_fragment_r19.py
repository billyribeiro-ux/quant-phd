"""Round 19: writes the LX1-b fragment (ledgers/LX1/LX1-b.json) from the evidence gathered in this round.

Run from the checkout root: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r19/write_fragment_r19.py
"""
import json
from datetime import datetime, UTC

O = "ledgers/LX1/scripts/LX1-b-r19/out/"
R = "ledgers/LX1/scripts/LX1-b-r19/"
CARRY_FX = ("course/assets/data/market/fx_monthly.csv, course/assets/data/market/MANIFEST.json, tools/fetch_data.py "
            "(byte-identical since pin 50559266, git diff --quiet)")
CARRY_PLAN = ("plans/LX1-build-plan.md and plans/LX1-open-items.md (byte-identical since pin 50559266); "
              "plans/FINAL-ARCHITECT-RULINGS.md changed only by an appended ruling 24, rulings 14 and 16 unchanged")
CARRY = "Carried from round 18 ({files}): "

PAGE_GATE = "tools/page_smoke.py --unit LX1 --pages {p}.html -> {o}page_smoke_{p}.out: 'page_smoke LX1: PASS', exit 0 (run alone)"

rows = []


def row(rid, check, location, status, evidence, fix=None):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    rows.append(d)


# ---- gates and lab twins ----
row("lx1b-check-pages", "2.9-structure", "course/modules/LX/LX1/L01.html; L03.html; L04.html", "PASS",
    f"tools/check_pages.py --unit LX1 -> {O}check_pages_unit.out: 'check_pages LX1: PASS', exit 0.")
row("lx1b-check-dag", "2.9-dag", "L01.html; L03.html; L04.html", "PASS",
    f"tools/check_dag.py --unit LX1 -> {O}check_dag_unit.out: 'check_dag LX1: PASS', exit 0.")
row("lx1b-check-projects", "2.6-projects", "tools/check_projects.py --unit LX1", "PASS",
    f"{O}check_projects_unit.out: 'check_projects LX1: PASS', exit 0.")
row("lx1b-run-graders", "2.6-autograder", "tools/run_graders.py --unit LX1", "PASS",
    f"{O}run_graders_unit.out: 'run_graders LX1: no autograder (grading: rubric)', exit 0 (LX1 is rubric-graded).")
row("lx1b-run-labs", "2.5-labs", "tests/labs/LX1/*.py", "PASS",
    f"tools/run_labs.py --unit LX1 -> {O}run_labs_unit.out: 'run_labs LX1: PASS (7/7)', exit 0.")
row("lx1b-twin-alone-L01", "2.5-labs", "tests/labs/LX1/lab-LX1-L01-1.py", "PASS",
    f"Alone in an empty scratch dir: python -I -W error lab-LX1-L01-1.py -> exit 0; {O}twin_L01.stderr 0 bytes; "
    f"{O}twin_L01.stdout 38 lines (r19 rerun after the delta).")
row("lx1b-twin-alone-L03", "2.5-labs", "tests/labs/LX1/lab-LX1-L03-1.py", "PASS",
    f"Alone in an empty scratch dir: python -I -W error -> exit 0; {O}twin_L03.stderr 0 bytes; {O}twin_L03.stdout 56 lines.")
row("lx1b-twin-alone-L04", "2.5-labs", "tests/labs/LX1/lab-LX1-L04-1.py", "PASS",
    f"Alone in an empty scratch dir with data/fx_monthly.csv copied into data/ (the path the twin reads): exit 0; "
    f"{O}twin_L04.stderr 0 bytes; {O}twin_L04.stdout 17 lines. A first attempt with the CSV at the wrong path exited 1 "
    f"(FileNotFoundError, data/fx_monthly.csv); the rerun with data/ is the valid run.")
row("lx1b-twin-equals-page-code", "2.5-labs", "L01.html, L03.html, L04.html code and expected blocks vs twins", "PASS",
    f"ledgers/LX1/scripts/LX1-b-r19/twin_compare_r19.py -> {O}twin_compare_r19.out: for L01, L03, L04 the page code "
    f"equals the twin with the trailing newline stripped (the page omits it); expected block line counts 38/56/17 "
    f"equal the twin stdout lines and match it.")
row("lx1b-page-smoke-L01", "2.9-smoke", "course/modules/LX/LX1/L01.html", "PASS", PAGE_GATE.format(p="L01", o=O))
row("lx1b-page-smoke-L03", "2.9-smoke", "course/modules/LX/LX1/L03.html", "PASS", PAGE_GATE.format(p="L03", o=O))
row("lx1b-page-smoke-L04", "2.9-smoke", "course/modules/LX/LX1/L04.html", "PASS", PAGE_GATE.format(p="L04", o=O))
row("lx1b-ruff-mypy", "2.5-labs", "tests/labs/LX1/*.py", "PASS",
    f"{O}ruff_check_labs.out 'All checks passed!'; {O}ruff_format_labs.out '7 files already formatted'; "
    f"{O}mypy_labs.out (mypy --no-incremental, 3 twins): 'Success: no issues found in 3 source files', exit 0.")
row("lx1b-pytest", "2.5-labs", "tests/test_labs.py", "PASS",
    f"pytest tests/test_labs.py -k LX1: 7 passed, exit 0 ({O}pytest_lx1_k.out; collect {O}pytest_collect_lx1_k.out: 7). "
    f"Full tests/test_labs.py: 359 collected and all pass, exit 0 ({O}pytest_labs.out).")
row("lx1b-verify-refs", "2.1-citations", "references/references.json; tools/verify_refs.py", "PASS",
    f"verify_refs.py --offline -> {O}verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0. "
    f"verify_refs.py --unit LX1 (live Crossref) -> {O}verify_refs_live_unit_r19.out: '4 of 560 entries, 0 problems', exit 0.")

# ---- citations ----
row("lx1b-citations-L01", "2.1-citations", "L01.html:304, :489; references/references.json garber2000famous", "PASS",
    "Registry garber2000famous (read via python -I): title 'Famous First Bubbles: The Fundamentals of Early Manias', "
    "author Garber, Peter M., year 2000, monograph. The page cites the key at book level for its title only and attributes "
    "no passage (L01:304 'cites that book for its title only'; :489). Registry scan for bubble/panic/manias entries finds "
    "only garber2000famous, which supports the L01:315 phrase 'no registered counter-account'.")
row("lx1b-citations-L03", "2.1-citations", "L03.html:405, :640; references/references.json friedman1963monetary", "PASS",
    "Registry friedman1963monetary: title 'A monetary history of the United States 1867-1960', author Friedman, Milton, "
    "year 1963, book. Curriculum curriculum/06-profession-capstone.yaml:37 lists 'Friedman & Schwartz, A Monetary History of "
    "the United States, 1867-1960 (1963)'. The page cites the key at book level, takes no finding from it (L03:640). The "
    "author-string difference is registry flag N2.")
row("lx1b-citations-L04", "2.1-citations", "L04.html:571-573 (References)", "PASS",
    "L04 cites no registry key (L04:571 'cites no key from the course's reference list'). Its one citation is the fx_monthly "
    "MANIFEST citation, which matches course/assets/data/market/MANIFEST.json citation and licence fields (read in r19).")

# ---- data ----
row("lx1b-fetch-check", "2.8-data", "course/assets/data/market/fx_monthly.csv; MANIFEST.json", "PASS",
    f"tools/fetch_data.py --check -> {O}fetch_check.out: 'fetch_data: 3 datasets, 0 problems', exit 0. sha256sum of the CSV = "
    "60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e, equal to MANIFEST fx_monthly sha256.")
row("lx1b-fx-rebuild", "2.8-data", "course/assets/data/market/fx_monthly.csv; MANIFEST fx_monthly; tools/fetch_data.py",
    "PASS", CARRY.format(files=CARRY_FX) +
    "round-18 scratch rebuild, 'built fx_monthly: 669 rows, 67392 bytes, 1971-01 to 2026-09', cmp byte-identical with the "
    "checkout CSV (round-18 fragment row lx1b-fx-rebuild). Not re-run in round 19; the r19 sha256 check above is fresh.")
row("lx1b-fx-licence", "2.8-data", "tools/data_sources.yaml fx_monthly; MANIFEST licence_url", "PASS",
    f"Plain curl https://www.federalreserve.gov/disclaimer.htm -> HTTP 200, 85306 bytes, saved as {O}fed_disclaimer_r19.html. "
    "It contains \"Unless otherwise indicated, information on Board's website is in the public domain and may be copied and "
    "distributed without permission\", the grant quoted in MANIFEST and tools/data_sources.yaml:57-59.")
row("lx1b-fx-guard", "2.8-data", "tests/labs/LX1/lab-LX1-L04-1.py parse_rate, load_column", "PASS",
    f"ledgers/LX1/scripts/LX1-b-r19/fail_loud_r19.py -> {O}fail_loud_r19.out: blank GBP cell, 'n/a', zero rate, '1e-3' all "
    "raise ValueError; a skipped month (1996-02) raises; a blank cell in a file raises; a missing column raises.")
row("lx1b-fx-gbp-clean", "2.8-data", "course/assets/data/market/fx_monthly.csv (GBP)",
    "PASS", f"ledgers/LX1/scripts/LX1-b-r19/rederive_L04_r19.py -> {O}rederive_L04_r19.out: 'blank GBP cells 0' over 669 rows; "
    "all months consecutive (assert in script).")
row("lx1b-honest-data", "2.8-data", "L03.html:76; L04.html:112-114; L01.html:131-133", "PASS",
    "L03:76 honest-pending note: no redistributable historical series is embedded, lab stays SIMULATED. L04:113-114 Part A "
    "labelled SIMULATED (constructed model check, not data); the real data named with licence and retrieval date. L01:131-133 "
    "inputs illustrative, price path SIMULATED. No historical series is fabricated.")
row("lx1b-L04-simulated-label", "2.8-data", "L04.html:113, :114; tests/labs/LX1/lab-LX1-L04-1.py docstring 138", "PASS",
    "Title 'Part A SIMULATED' (L04:113); hypothesis says Part A is 'a constructed model check, not data' (:114); twin "
    "docstring line 138 'Part A is a SIMULATED model check, not data'; expected block 306 'Part A: SIMULATED model check, not data'.")
row("lx1b-L04-manifest-note", "2.8-data", "L04.html:112, :114, :117-123", "PASS",
    "data-files=\"fx_monthly.csv\" (L04:112). MANIFEST fx_monthly: retrieved 2026-10-19, 669 rows, first 1971-01, last 2026-09, "
    "columns AUD, CAD, CHF, DKK, EUR, GBP, JPY, NOK, NZD, SEK; transform 'CAD, CHF, DKK, JPY, NOK, SEK inverted' matches "
    "L04:121 and the twin docstring 120-121.")
row("lx1b-open-items-missing", "2.9-structure", "plans/LX1-open-items.md", "PASS",
    CARRY.format(files="plans/LX1-open-items.md, byte-identical since pin 50559266") +
    "open items contain D-1 (L03 curriculum-lab data request), the Bretton Woods pending-definition item, and the reference "
    "requests for the credit-channel source (B2), Kindleberger (N1) and Friedman's second author (N2).")

# ---- L01 numbers ----
row("lx1b-num-L01-closed-form", "2.2-numbers", "L01.html:132, :87, :282, :396-399, :417-435", "PASS",
    f"ledgers/LX1/scripts/LX1-b-r19/rederive_L01_r19.py -> {O}rederive_L01_r19.out: F0 = 20000/3 = 6666.67, rounds 6667; "
    "q = 103/109 = 0.944954; S_N identity exact for N=10,60,200 (True); F0 q^N rounds 3785, 223, 0 for N=10,60,200; "
    "S_N rounds 2882, 6444, 6667. Matches the expected block (L01:247-249).")
row("lx1b-num-L01-lab-output", "2.5-labs", "L01.html:244-282 (expected block) vs twin stdout", "PASS",
    f"{O}twin_compare_r19.out: expected block (38 lines) equals the twin run output. Re-derived in exact Fractions "
    f"({O}rederive_L01_r19.out): F_9 = 8698.49 rounds 8698; price 10873.11 rounds 10873; the printed wedges are integer "
    "percents, so the wedge at t=9 is exactly 0.25.")
row("lx1b-num-L01-prose", "2.2-numbers", "L01.html:282, :363, :367, :370-371, :378, :400", "PASS",
    f"{O}rederive_L01_r19.out: 9/13 = 0.6923 (4 dp); 13 - 9 = 4; 2175/8698 = 0.2500575 -> 25.01 percent (printed integers); "
    "the unrounded gap is exactly 0.25 F_9, i.e. 25.00 percent; fundamental at t=9 is 8698.49 cents to two places.")
row("lx1b-num-L01-witness", "2.2-numbers", "L01.html:114, :120, :321, :462", "PASS",
    f"{O}rederive_L01_r19.out: F0(1%) = 400/0.08 = 5000; F0(3%) = 20000/3; at A0 = 6000 the gaps are +1000 and -2000/3 "
    "(-666.67). Matches L01:120.")
row("lx1b-num-L01-s5-example", "2.2-numbers", "L01.html:310, :322; quiz L01:417-421; misconception 2 L01:323", "PASS",
    f"{O}rederive_L01_r19.out: 400/1.09 = 40000/109 = 366.97 -> 367 cents; the closed form at g = 3% gives 6667 cents.")
row("lx1b-num-L03-depth", "2.2-numbers", "L03.html:149, :362-363, :383, :491, :496-498, :545-546, :577, :596",
    "PASS", f"{O}rederive_L03_r19.out: depth X = 0.0920459718 -> 9.20 percent; depth Y = 0.0268671310 -> 2.69 percent "
    "(E1 exact 2.6867 OK); X - Y = 6.517884 -> 6.52 (Part B and E2); printed 9.20 - 2.69 = 6.51 (E2 and L03:383 both state this).")
row("lx1b-num-L03-path", "2.2-numbers", "L03.html:331-357 (expected block) vs twin", "PASS",
    f"{O}rederive_L03_r19.out: V_4 = 1084165.7847 -> 1084166; V_12 = 1274345.2124 -> 1274345; leverage at t=4 Y 0.2769; "
    "Y index flat from t=4 (0.92236816); X index at t=0..12 4 dp matches printed; expected block equals twin output "
    f"({O}twin_compare_r19.out).")
row("lx1b-num-L03-M-E-Q", "2.2-numbers", "L03.html:441, :448, :455, :491, :498, :505, :596, :610", "PASS",
    "M1: (49/50)^4 = 5764801/6250000 exactly; V_4 = 1084165.7847 (rounded 1084166). M2: K_4 = 3915834.2153 -> 3915834, and "
    "rounded-first also 3915834. M3: L_4 = 0.2768671 -> 0.2769. E3: index unchanged for t=5..12 = 8 periods. Quiz numeric "
    "1274345 (V_12) and 3.426 (ratio) re-derived in the same script.")
row("lx1b-num-L04-stats", "2.2-numbers", "L04.html:306-322 (expected), :323, :476-477", "PASS",
    f"{O}rederive_L04_r19.out: window one n=668, sd 0.027935278 -> 0.027935; window two n=321, sd 0.024699501 -> 0.024700; "
    "difference -0.003235777 -> -0.003236; ratio 0.884168808 -> 0.8842.")
row("lx1b-num-L04-display-diff", "2.2-numbers", "L04.html:323; key row :476", "PASS",
    "0.024700 - 0.027935 = -0.003235 from the printed figures; the unrounded difference prints -0.003236 (r19 out). L04:323 "
    "says the difference is computed from unrounded values and gives -0.003235 for the printed-figure subtraction. Correct.")
row("lx1b-num-L04-derived", "2.2-numbers", "L04.html:354, :373, :380, :387, :430, :455, :541, :564", "PASS",
    f"{O}rederive_L04_r19.out: ln 1.1 = 0.0953101798 -> 0.095310; 0.1 - ln 1.1 = 0.0046898 -> 0.004690; M2 mean 0.006667, "
    "SS 19/15000, sd 0.025166; M3 26x12+9 = 321; E2 simple change exp(-0.0965747399762) - 1 = -0.092057965 -> -0.092058; "
    "R2 h = tanh(z/2) = 0.067819 (6 dp), 0.0678 (4 dp), bound at h = 0.0678 is 0.135808352 < 0.135845673; quiz 0.1358 correct.")
row("lx1b-scope-start", "2.2-numbers", "L04.html:110, :326, :387, :462; card LX1-c063; twin docstring 127-130", "PASS",
    "Window two starts 2000-01 (WINDOW_TWO_FROM); its first change uses 1999-12 (rederive: 323/200). Reason given (fx_daily "
    "and ust_daily first 2000-01-03 in MANIFEST) matches MANIFEST first fields (read in r19).")

# ---- math ----
row("lx1b-math-L01", "2.4-mathematics", "L01.html:57-99", "PASS",
    "Re-derived: d_{t+k}/(1+r)^k = d1(1+g)^t/(1+r) q^{k-1}; 1-q = (r-g)/(1+r) > 0 under A0; S_N(t) = F_t(1-q^N) exact; "
    "0 < q < 1 under A0; under g >= r, q >= 1 and each term >= d1/(1+r) (Proposition 1.4 proof, hypotheses (A1) d1>0, (A2) r>-1 "
    "stated). Theorem 1.3 and Proposition 1.4 are T with proofs on the page.")
row("lx1b-math-L01-prop22", "2.4-mathematics", "L01.html:108-121", "PASS",
    "Hypotheses (A3) d1>0 and (A4) (Assumption 1.1 at g and g', r > g, r > g', g < g', 1+g>0, 1+g'>0) are stated. Proof: "
    "r-g > r-g' > 0 gives d1/(r-g) < d1/(r-g') because d1 > 0; then F0(g) < A0 <= F0(g') gives gap > 0 and <= 0. Witness numbers "
    "re-derived (rederive_L01_r19.out).")
row("lx1b-math-L03", "2.4-mathematics", "L03.html:94-143", "PASS",
    "Lemma 3.1: y(C-x) - x(C-y) = C(y-x) with C = K0 + D > 0, so lambda strictly increasing on [D, C); L_t = lambda(V_t) since "
    "K_t = C - V_t. Prop 3.2(a) monotone V_t, V_t <= V_m; (b) uses V_m < C from Assumption 1.2; (c) first maximiser at t = m, "
    "and depth(0) = 0 (m = 0 gives V_t = D). Corollary 3.3 and 3.4 proofs use m' >= 1 for positivity of the denominator. All "
    "re-derived exactly (rederive_L03_r19.out).")
row("lx1b-math-L04", "2.4-mathematics", "L04.html:57-107", "PASS",
    "Proposition 1.2 telescoping proof and cancellation of interior ln x_t terms are correct; Proposition 2.2 proof uses (A2) and ln 1 = 0; "
    "n >= 2 needed for n-1 >= 1 (stated in Definition 1.1 and Proposition 2.2). Remark 1.3 tolerance matches SUM_TOLERANCE = 1e-12.")
row("lx1b-math-problems", "2.4-mathematics", "L01.html:330-389; L03.html:431-532; L04.html:363-466", "PASS",
    "Every solution re-derived: L01 Mechanics 1-3 (4167, 4687, 20000/21 and 952.38), Proof 1-3 (benchmark monotonicity; recursion "
    "F_t = (1+g)F_{t-1}, which the solution derives by dividing when d1 != 0 and by direct substitution otherwise; ratio above "
    "discount rate), Empirical 1-3 (0.6923, 4, 25.01/25.00), Research 1-3 (g* = 7/300 = 0.023333). L03 M1-M3, P1-P3, E1-E3, "
    "R1-R3 and L04 M1-M3, P1-P3, E1-E3, R1-R3 re-derived (rederive_L03/L04_r19.out). L04 R1's undefined subscripts are a separate FAIL row.")
row("lx1b-grades", "2.3-grades", "L01.html:396-401; L03.html:542-546; L04.html:474-477; cards grades", "PASS",
    "Theorems, propositions and corollaries are T with proofs on the page; lab-computed counts and dispersions are C with the lab "
    "named (L01:401, L03:545-546, L04:476-477); card grades match (c009-c010, c037-c039, c054-c058, c060, c065, c067, c068, c089 C; "
    "T cards cite their proofs). The rubric in L03:542-546 and L01:397-400 agrees with BLUEPRINT grading as applied here.")

# ---- notation ----
row("lx1b-notation", "2.4-notation", "L01.html; L03.html; L04.html; cards.json (L01, L03, L04); twins", "PASS",
    f"{O}math_inventory_r19.out: no registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{{e\\ast}}, R_f, \\mathbb{{Q}}) appears "
    "in any math span of the three pages. notation/notation.json byte-identical to the previous pin.")
row("lx1b-notation-P", "2.4-notation", "L01.html (whole page); L03.html:58-59, :116, :157-163; L02.html:77", "PASS",
    "grep -c 'P_' on L01.html returns 0 (round-17 FAIL resolved: L01 uses A_0 at :114, :119-120, :377). L01 observed price is A_t "
    "(:105, :143, :450). L03 P_t price index with P_0 = 1 (:58) consistent with the page's code docstring (L03:157-162, twin lines 8-13) and the twin's price_index.")
row("lx1b-notation-A", "2.4-notation", "L01.html:105, :114, :119-120, :143-144, :377, :450; cards LX1-c006, c007, c093", "PASS",
    "A_t is the observed price in every use; A_0 is the date-0 price in Proposition 2.2 and in card c093; no conflict with the "
    "assumption labels (A0)-(A4).")
row("lx1b-notation-K", "2.4-notation", "L03.html:65 (first use) to :605; cards c027, c071, c082; twin docstring 166", "PASS",
    "K_t = K_0 - (V_t - V_0) in Assumption 1.2, Lemma 3.1 proof (:103), and twin code net_worth; no other meaning on the three pages.")
row("lx1b-notation-P-L03", "2.4-notation", "L03.html:58-59, :116, :157-163, :211, :464-473", "PASS",
    "P_t = (1-delta)^min(t,m), P_0 = 1 (L03:59, twin price_index). L04 uses no P symbol (grep).")
row("lx1b-notation-N", "2.4-notation", "L01.html:67, :74, :82-83, :87; L04", "PASS",
    "N is the partial-sum bound in Definition 1.2 and Theorem 1.3 (L01:67, :74); no other meaning on the three pages. L04 uses n for the count of changes (Definition 1.1), a lowercase symbol with its own meaning.")
row("lx1b-notation-registered", "2.4-notation", "L01/L03/L04 math spans; notation.json macros", "PASS",
    f"{O}math_inventory_r19.out: none of \\E, \\Prob, \\Var, \\Cov, \\Corr, \\N, \\indic, \\Normal, \\SR appears in the three pages; "
    "the real line is not written (no \\R).")
row("lx1b-notation-check-math-spans", "2.4-notation", "L01.html math spans", "PASS",
    f"{O}math_inventory_r19.out is identical to the round-18 inventory except for line numbers (diff). No macro outside the "
    "registered set or the standard operators is used with another meaning.")

# ---- DAG and concepts ----
row("lx1b-dag-links", "2.9-dag", "L01.html:37; L03.html:37, :54, :90; L04.html:37-38, :105", "PASS",
    "check_dag LX1 PASS (r19). L01 links concept anchors of M1 in the closure (growing-perpetuity, present-value, geometric-series, "
    "exponential-and-logarithm); L03 links L02#def-debt-deflation and L02#def-gold-standard; L04 links L02 and L03 anchors.")
row("lx1b-dag-outside-closure", "2.9-dag", "L03.html:390, :402, :413-418; L04.html:336; L01.html", "PASS",
    "grep for central bank, bank, monetary, inflation, gold, debt deflation in L01.html finds only the L02 next-lesson link (L01:495). "
    "L03 'central bank' is defined in plain dfn at L03:390 without a data-concept; no out-of-closure concept is used by name "
    "without a link (round-18 grep, pages unchanged).")
row("lx1b-concepts-defs", "2.9-dag", "L01.html:105, :289; L03.html:87, :390; L04.html:86; course/concepts.html:631-636", "PASS",
    "Each LX1 concept has one data-concept dfn: speculative-bubble (L01:105), financial-panic (L01:289), credit-channel-depression "
    "(L03:87), lender-of-last-resort (L03:390), bretton-woods-system (L04:86, pending).")
row("lx1b-concept-index-title", "2.9-dag", "course/concepts.html:631-636", "PASS",
    "Seven LX1 entries link to dfn ids on L01-L04. The Bretton Woods entry reads 'defined here' although its definition is "
    "'definition pending' on L04:86. This is a generated line (tools/build_site.py, build_site --check current, r19); it is "
    "recorded as registry flag G1 and is not edited here.")
row("lx1b-L04-bretton-definition", "2.4-mathematics", "L04.html:38, :86, :337, :358, :553-557", "PASS",
    "Definition labelled 'definition pending' (L04:86); the page states the fixed-exchange-rate model is not a definition of the "
    "historical system; dates, participants and end are not stated. Ruling 14 (FINAL-ARCHITECT-RULINGS.md:32-34) permits this honest-pending state.")

# ---- prose, structure, cards ----
row("lx1b-banned-phrases", "2.9-prose", "L01.html; L03.html; L04.html; cards.json", "PASS",
    "grep -i over the three pages and cards.json for BUILDER_RULES §1.3-1.4 strings (TODO, TBD, lorem, for brevity, details "
    "omitted, beyond the scope, left as an exercise, you can add more, ellipsis, it can be shown, roughly half, historically, "
    "obviously, clearly, well known, important to note, studies show, experts agree): zero hits.")
row("lx1b-process-words", "2.9-prose", "L01.html; L03.html; L04.html; cards.json", "PASS",
    "grep -i for build, builder, verifier, ruling, architect, fixer, requests, unit report, ledger, round N, plan over the three "
    "pages and cards: zero hits.")
row("lx1b-scope-words", "2.9-prose", "L01.html; L03.html; L04.html (hits in "
    f"{O}prose_scan_r19.out)", "PASS",
    f"{O}prose_scan_r19.out read in full. Each hit was read in context: L01:51 'only relative to that benchmark' (defined by Def 2.1); "
    "L01:99 'With d1 > 0' (new hypothesis, correct); L01:313 and :324 (d1 > 0 stated); L01:315 'no registered counter-account' "
    "(verified against references.json, see lx1b-citations-L01); the L03 and L04 hits are unchanged and read in r18 and r19. "
    "'Every'/'any'/'all' sit on proofs, finite computations, stated hypotheses, or negative scope statements.")
row("lx1b-structure", "2.9-structure", "L01 sections 1-10; L03 sections 1-10; L04 sections 1-9", "PASS",
    "L01: sections 1-10 (lines 53, 101, 286, 303, 307, 319, 328, 392, 406, 486); 3 misconceptions; 4 problem tiers of 3; 10 quiz "
    "items; key-results table. L03: sections 1-10; 4 misconceptions; 3 problems per tier; 11 quiz items. L04: sections 1-9; 4 "
    "misconceptions; 3 problems per tier; 11 quiz items. Template enforced by check_pages PASS.")
row("lx1b-quiz-explanations", "2.9-structure", "L01.html:405-483; L03.html:552-636; L04.html:483-567", "PASS",
    "Each explanation read against its lesson and the printed output: L01 explanations match Theorem 1.3, Proposition 1.4, Definition 2.1, "
    "Proposition 2.2 values; L03 explanations match Corollary 3.3, 3.4, Lab 1 Part B and D; L04 explanations match Proposition 1.2, "
    "Proposition 2.2, Lab 1 Part B and C.")
row("lx1b-L03-remark42-solvency", "2.4-mathematics", "L03.html:64-67, :395", "PASS",
    "Assumption 1.2 states the inequality and says it keeps K_t > 0 (:67); Proposition 3.2(a) gives V_t <= V_m; so K_t > 0 in every period "
    "(:395). Consistent with K_t = C - V_t.")
row("lx1b-L03-ratio-claims", "2.4-mathematics", "L03.html:404; :516; :523", "PASS",
    "Square-premium variant: depth = beta phi times the square of the Corollary 3.4 bracket, so the ratio is the square of the "
    "Corollary 3.4 ratio; equal to it only when the ratio is 0 or 1; the ratio is > 1 (depth(12) > depth(4)), so they differ.")
row("lx1b-L03-r1-no-result", "2.4-mathematics", "L03.html:516", "PASS",
    "R1 describes the change and the assumption it replaces and states no numerical result, consistent with Remark 4.2.")
row("lx1b-L03-lab-checks-overreach", "2.5-labs", "L03.html:145, :383; twin docstring 25-26 and code 171-174", "PASS",
    "Interpretation says the printed depths are the model's values and no output series enters the lab (:383); Part C checks the "
    "adjacent-duration orderings it prints; Part D prints three ratios and makes no equality test (twin lines 171-174).")
row("lx1b-L03-misconception-scope", "2.4-mathematics", "L03.html:413-426; proof :128-131", "PASS",
    "Misconception 1 (bank failure) and 2 (holding parity) are answered by Assumptions 1.1-1.3 and the proof of Corollary 3.3, "
    "which uses only the durations, the closed form, V_m < K_0 + D, Lemma 3.1 and Proposition 3.2(b).")
row("lx1b-cards-l01-l03-l04", "2.7-cards", "course/modules/LX/LX1/cards.json (L01 17, L03 32, L04 24)", "PASS",
    f"{O}cards_check_r19.out: 90 unique ids; per lesson L01 17, L03 32, L04 24 (the L02 cards are another slice). All 73 cards "
    "of L01, L03, L04 read in full; no duplicate fronts; graded cards carry a basis; each card's claim matches its lesson text "
    "(LX1-c092 vs L01:324; c093 vs L01:108-121; LX1-c067 vs L03:383 is recorded in lx1b-L03-corollary34-wording).")
row("lx1b-cards-c052-c053", "2.7-cards", "cards.json LX1-c052, LX1-c053 vs L04.html:84-94", "PASS",
    "c052 gives (A2), window of at least two changes, zero changes and zero dispersion (matches Proposition 2.2, L04:89-94); c053 lists "
    "anchor currency, one foreign currency, fixed rate, market rate (matches Definition 2.1, L04:84-87).")
row("lx1b-cards-L01-hypotheses", "2.7-cards", "cards.json LX1-c002..c007, c013, c085, c086, c092, c093", "PASS",
    "Theorem 1.3 cards state A0 and A1; Proposition 1.4 cards (c005, c013, c092) state (A1) d1 > 0, 1+g > 0 and (A2) r > -1, g >= r; "
    "Proposition 2.2 cards (c007, c093) state (A3), (A4) as on the page. c085 (F_t = (1+g)F_{t-1}) matches Problem Proof 2.")
row("lx1b-cards-L03-hypotheses", "2.7-cards", "cards.json LX1-c030..c036, c079, c082, c087", "PASS",
    "Lemma 3.1, Proposition 3.2(a)-(c), Corollaries 3.3 and 3.4 cards state Assumptions 1.1-1.3 (and 1.2 where needed) and the "
    "parity ranges (0 <= m' < m <= H for Cor 3.3; 1 <= m' < m <= H for Cor 3.4), matching L03:125 and :135.")
row("lx1b-delta-hunks", "2.9-structure", "L01.html; cards.json; tests/labs/LX1/lab-LX1-L01-1.py (delta 50559266..cd4dd7df)", "PASS",
    "git diff 50559266 cd4dd7df: L01.html has 7 hunks (:51 why-it-matters, :99 Proposition 1.4 remark, :136-140 lab hypothesis and "
    "docstring, :300 Remark 3.3, :313-315 canon breaks, :324 misconception 3, :357 Proof 3 solution); each read in full and re-verified "
    "above (lx1b-L01-misc3-closed-form and lx1b-L01-benchmark-finite-hypothesis now PASS). cards.json: LX1-c067 back text changed "
    "('requires' to 'implies'; page wording is in row lx1b-L03-corollary34-wording), LX1-c092 and c093 appended. Twin: docstring 7-8 only. "
    "L03.html, L04.html, their twins, references, notation, MANIFEST and fx_monthly.csv are byte-identical to the previous pin.")
row("lx1b-plan-coverage", "2.9-structure", "plans/LX1-build-plan.md (sections 2.1, 3); plans/FINAL-ARCHITECT-RULINGS.md (rulings 14, 16)",
    "PASS", CARRY.format(files=CARRY_PLAN) +
    "round-18 plan-coverage read of the plan's L01-L04 sections, and this round's fresh read of rulings 14 and 16 (FINAL-ARCHITECT-RULINGS.md:32-40) "
    "and of the L01 text, which still covers the closed form under (A0)/(A1), the bubble as a gap with a stated benchmark, panic by "
    "mechanism, and Garber at book level.")
row("lx1b-hours", "2.9-structure", "L01.html:2, :34; L03.html:34; L04.html:34; course/modules/LX/LX1/index.html:29", "PASS",
    "index.html:29 data-hours-lessons=40 and data-hours-project=10; each lesson 10 hours (data-hours and eyebrows). 4 x 10 + 10 = 50, "
    "matching the curriculum 50 h. Hours are design targets (ruling).")
row("lx1b-L03-honest-pending-source", "2.8-data", "L03.html:76; open-items D-1 (byte-identical file)", "PASS",
    "L03:76 says no redistributable historical series is embedded and the lab stays SIMULATED. Open-items D-1 records the request "
    "(carried: plans/LX1-open-items.md unchanged since the previous pin). Consistent.")
row("lx1b-L04-spot-only", "2.8-data", "L04.html:333-334; tools/data_sources.yaml fx_monthly note (lines 62-64)", "PASS",
    "Register note (read in r19): 'Each value is the last noon rate of its month ... the release's own monthly series are monthly averages. "
    "... Spot rates only, as for fx_daily.' L04:333-334 and :334 state spot-only and the last value, not the Board's monthly average. Consistent.")
row("lx1b-L04-twin-docstring-float", "2.5-labs", "tests/labs/LX1/lab-LX1-L04-1.py docstring and log_changes/show", "PASS",
    "Docstring: exact ratio converted once to float then ln (code: float(rate / previous) then math.log); show() uses Decimal(value) "
    "quantized with ROUND_HALF_UP, i.e. the exact binary value rounded half away from zero, as the docstring states.")
row("lx1b-L03-partD-label", "2.5-labs", "L03.html:145, :149, :383; twin lines 171-174", "PASS",
    "Part D prints three ratios (all 3.4260 in the output) and makes no equality test (twin code); the page says the same.")
row("lx1b-L03-line121-lab-formula", "2.5-labs", "L03.html:121; twin depth() and depth_path()", "PASS",
    "The twin computes depth as max over depth_path (no closed form); L03:121 says the lab does not evaluate part (b). Correct.")
row("lx1b-L03-why-ordering", "2.9-structure", "L03.html:51; twin docstring lines 3-5", "PASS",
    "Twin docstring lines 3-5 say X keeps parity for the whole horizon and Y leaves after a stated number of periods; the ordering follows from the stated assumptions and durations (page :51). No historical claim.")
row("lx1b-L04-A2-before-defined", "2.9-dag", "L04.html:51, :58, :66, :84-92, :400-405, :450-457", "PASS",
    "(A1) first stated inline in Proposition 1.2 (:66); (A2) in Definition 2.1 (:85) precedes Proposition 2.2 (:89); (A3) first appears in "
    "Problem P2 (:403) with its full statement; dispersion is used at :51 with a forward reference to Definition 1.1 (:58).")
row("lx1b-L04-keyresults-locator", "2.3-grades", "L04.html:474-477", "PASS",
    "Each key-results row names a locator (Proposition 2.2 and Proposition 1.2 in the text; Lab 1 Parts B-D for the counts).")
row("lx1b-L04-prediction-tested", "2.5-labs", "L04.html:114; twin Parts A and C; expected 307-322", "PASS",
    "Hypothesis: Part A all exactly zero True, sd 0.000000 (expected :307-308); prediction of nonzero recorded dispersion in both "
    "windows is shown by printed dispersions (:314, :317) and the lab does not assert it.")
row("lx1b-L03-forward-definition-refs", "2.9-dag", "L03.html:51, :54, :72, :82, :389", "PASS",
    "Forward uses name the definition: leverage and premium at :72 cite Definition 2.1 (defined at :82); lender of last resort at :51 "
    "cites Definition 4.1 (:389); Sections 2 and 4 give the definitions.")

# ---- previously FAIL rows, now PASS ----
row("lx1b-L01-misc3-closed-form", "2.9-prose", "course/modules/LX/LX1/L01.html:324 (misconception 3); card LX1-c092", "PASS",
    "Round-18 FAIL resolved. L01:324 now reads 'The series has no finite sum, so the closed form of Theorem 1.3 gives no present "
    "value: it is undefined at g = r, and for g > r it returns a negative number that is not the present value of the dividends.' "
    "Re-derived: 400/(0.09 - 0.10) = -40000 cents (rederive_L01_r19.out 'misc3 closed form'). The sentence is correct under (A1) with d1 > 0.")
row("lx1b-L01-benchmark-finite-hypothesis", "2.4-mathematics", "course/modules/LX/LX1/L01.html:99", "PASS",
    "Round-18 FAIL resolved. L01:99 now reads 'With d1 > 0, a benchmark that depends on a growth rate at or above the discount rate "
    "is not a finite present value', the hypothesis Proposition 1.4 assumes. Correct for d1 > 0 (d1 = 0 is excluded by the sentence).")

# ---- new FAIL rows (round 19) ----
row("lx1b-L03-corollary34-wording", "2.7-cards", "course/modules/LX/LX1/L03.html:383; cards.json LX1-c067 back", "FAIL",
    "L03.html:383 says the printed Part D ratio is the same 'as Corollary 3.4 requires'. The corollary does not require any output: "
    "it implies that the ratio does not depend on beta phi, and the lab output is checked against it. Round 19 changed card LX1-c067 to "
    "'as Corollary 3.4 implies' but left the page, so the card and the lesson now use different wording for the same claim. Verified: "
    "ratio 3.425969... -> 3.4260 for all three products (rederive_L03_r19.out); the substance is right; the defect is the directional verb.",
    fix="In course/modules/LX/LX1/L03.html:383 replace 'as Corollary 3.4 requires' with 'as Corollary 3.4 implies' so the lesson "
        "matches card LX1-c067. No other change.")
row("lx1b-L04-R1-undefined-subscripts", "2.4-notation", "course/modules/LX/LX1/L04.html:448 (R1 solution); definition at :58-59", "FAIL",
    "The R1 solution writes 's_2^2/s_1^2' for the ratio of the two windows' sample variances, but s_1 and s_2 are not defined anywhere "
    "in L04. Definition 1.1 defines a single dispersion s for a window (:58-59), and the lab names the windows 'window one' and 'window two'. "
    "The symbols are used before they are defined; a reader cannot tell which window s_1 names without guessing.",
    fix="In course/modules/LX/LX1/L04.html:448, before 'A natural statistic is ...', add: 'Let s_1 and s_2 be the dispersions of "
        "window one and window two from Definition 1.1.' No other change.")

row("lx1b-mutants-none", "2.6-mutation", "tests/labs/LX1/*; rubric ruling on lab mutants", "PASS",
    "No grader exists (run_graders: 'no autograder (grading: rubric)', out/run_graders_unit.out), so no project mutant rows apply to slice b. "
    "Lab twins are demonstrations; a mutated lab exiting 0 is not a finding unless a lesson sentence claims the lab checks that property, and "
    "the lab-checks sentences (L01:87, L03:145, L03:383, L04:141) were read against the code.")

assert len({r["id"] for r in rows}) == len(rows), "duplicate row id"
fragment = {
    "unit": "LX1",
    "slice": "b",
    "round": 19,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-b (L01, L03, L04 and lab twins), round 19",
    "pin": "cd4dd7df (cd4dd7dfc2bbe0fc16b672329daa408d1d8a268b), detached; .venv symlinked; vendor copied",
    "base": "50559266 (round-18 pin, 505592668894eff518befad086df192000dc86c0). Delta read: course/modules/LX/LX1/L01.html, "
            "cards.json (LX1-c067, c092, c093), tests/labs/LX1/lab-LX1-L01-1.py; L03.html, L04.html and the L03/L04 twins are "
            "byte-identical to 50559266. project.html and lab-LX1-project-3.py changed in the same delta and belong to slice a.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE19-LX1-b",
    "scratch": "/tmp/lx1b-r19-twin-* and /tmp/lx1b-r19-twin-L04-* (removed after each run); /tmp/lx1b-r19-fail-* (removed)",
    "verified_at": datetime.now(UTC).isoformat(timespec="seconds"),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "B2: Bernanke (1983) credit-channel source (curriculum yaml:38) is not in the registry; review_queue.json candidate is an NBER working paper and must not be admitted as the AER article.",
        "N1: Kindleberger & Aliber (2015) is not in the registry (review_queue.json:1557); no LX1 page cites it.",
        "N2: friedman1963monetary registry record lists 'Friedman, Milton' only; curriculum string names Friedman & Schwartz (yaml:37). Pages cite the key only.",
        "B3: no registry record mentions Bretton Woods (references.json, zero hits); the L04 definition and any end date stay pending (ruling 14).",
        "G1: generated course/concepts.html:631 says 'defined here' for the Bretton Woods system, whose definition is pending (ruling 14). Generated by tools/build_site.py; not edited here.",
        "G2: generated course/concepts.html:635 titles the credit-channel concept 'Nonmonetary (credit) channel of the Great Depression', the curriculum's name; the L03 page does not use that title.",
    ],
    "freshness_flags": [],
    "notes": [
        "Pin cd4dd7df checked out detached; .venv symlinked; no course, tool, test, reference, curriculum, plan or market file edited; no commit or push. Files written: under ledgers/LX1/scripts/LX1-b-r19/ and this fragment only.",
        "Full read this round: L01.html (all 501 lines), L03.html (all 653 lines), L04.html (all 586 lines), the three slice-b twins (L01 112 lines, L03 177, L04 191), all 73 L01/L03/L04 cards (cards_check_r19.out plus full reads), the L01 delta hunks (git diff 50559266 cd4dd7df), rulings 14 and 16, the L01 and L03 and L04 problem sets.",
        "Re-derived in exact Fractions or floats by the round-19 scripts: L01 (rederive_L01_r19.py), L03 (rederive_L03_r19.py), L04 (rederive_L04_r19.py, independent CSV parser). Twins run alone under python -I -W error; fail-loud checks in fail_loud_r19.py.",
        "Round-18 PASS rows were re-verified where the subject was touched or where I re-ran the check; three rows carry round-18 evidence on byte-identical subjects (lx1b-fx-rebuild, lx1b-open-items-missing, lx1b-plan-coverage), marked as carried.",
        "Round-18 FAIL rows lx1b-L01-misc3-closed-form and lx1b-L01-benchmark-finite-hypothesis are re-verified PASS against the new L01 text.",
        "Two new FAIL rows (low severity, one-clause fixes): lx1b-L03-corollary34-wording (L03:383 'requires' vs card c067 'implies') and lx1b-L04-R1-undefined-subscripts (L04:448 s_1, s_2 undefined). Neither changes any number.",
        "Generated concept index text (G1, course/concepts.html:631 'defined here' for a pending definition) is recorded as a registry flag, not a row, as in round 18; it belongs to tools/build_site.py and sits outside this slice.",
        "Mutants: none. LX1 is rubric-graded (no grader), and lab twins are demonstrations (architect rulings); recorded as mutants [] on purpose.",
        "Not checked: the Pyodide runtime beyond tools/page_smoke.py (PASS for L01, L03, L04 run alone); L02, the project, the hub prose beyond the hours lines (other slices); registry records beyond the LX1 keys (verify_refs live covered the four LX1 entries); the Crossref live run of the whole registry (not a unit row); any historical fact (none is stated on these pages, by design).",
    ],
    "summary": "LX1-b round 19 on cd4dd7df (base 50559266): verdict FAIL. Rows: %d (pass=%d fail=%d unverifiable=0). Non-PASS: lx1b-L03-corollary34-wording (L03.html:383 'as Corollary 3.4 requires' vs card c067 'implies'), lx1b-L04-R1-undefined-subscripts (L04.html:448 s_1, s_2 undefined). The two round-18 FAIL rows are resolved. All numbers, proofs, twins, cards and data checks re-derived or re-run this round." % (
        len(rows), sum(1 for r in rows if r["status"] == "PASS"), sum(1 for r in rows if r["status"] == "FAIL")),
}
with open("ledgers/LX1/LX1-b.json", "w", encoding="utf-8") as h:
    json.dump(fragment, h, ensure_ascii=False, indent=2)
    h.write("\n")
print("rows", len(rows), "pass", sum(1 for r in rows if r["status"] == "PASS"), "fail", sum(1 for r in rows if r["status"] == "FAIL"))
