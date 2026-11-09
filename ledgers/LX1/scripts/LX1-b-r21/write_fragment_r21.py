"""Build the LX1 slice-b round-21 fragment (ledgers/LX1/LX1-b.json) from the rows decided in this round."""

import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = ROOT / "ledgers/LX1/scripts/LX1-b-r21/out"
R20 = "Carried from round 20 (files byte-identical since the round-20 pin d1083bf1): "
FRESH = "Re-run this round: "
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- commands run this round (exact outputs under the scripts dir) ----
row("lx1b-check-pages", "2.9-structure", "course/modules/LX/LX1/L01.html; L03.html; L04.html",
    "PASS", FRESH + "tools/check_pages.py --unit LX1 -> ledgers/LX1/scripts/LX1-b-r21/out/check_pages.out: 'check_pages LX1: PASS', exit 0.")
row("lx1b-check-dag", "2.9-dag", "course/modules/LX/LX1/L01.html; L03.html; L04.html",
    "PASS", FRESH + "tools/check_dag.py --unit LX1 -> out/check_dag.out: 'check_dag LX1: PASS', exit 0.")
row("lx1b-check-projects", "2.6-projects", "tools/check_projects.py --unit LX1",
    "PASS", FRESH + "tools/check_projects.py --unit LX1 -> out/check_projects.out: PASS, exit 0 (project page is slice a).")
row("lx1b-run-graders", "2.6-autograder", "tools/run_graders.py --unit LX1",
    "PASS", FRESH + "out/run_graders.out: 'run_graders LX1: no autograder (grading: rubric)', exit 0.")
row("lx1b-run-labs", "2.5-labs", "tests/labs/LX1/lab-LX1-L01-1.py; lab-LX1-L03-1.py; lab-LX1-L04-1.py",
    "PASS", FRESH + "tools/run_labs.py --unit LX1 -> out/run_labs.out: 'run_labs LX1: PASS (7/7)', exit 0.")
for L in ("L01", "L03", "L04"):
    row(f"lx1b-twin-alone-{L}", "2.5-labs", f"tests/labs/LX1/lab-LX1-{L}-1.py",
        "PASS", FRESH + f"ledgers/LX1/scripts/LX1-b-r21/run_twins_r21.sh: python -I -W error on the twin from an empty scratch dir "
        f"(L04 with a data/fx_monthly.csv copy) -> out/twin_{L}.out ends 'exit 0', out/twin_{L}.err is 0 bytes.")
row("lx1b-twin-equals-page-code", "2.5-labs",
    "course/modules/LX/LX1/L01.html, L03.html, L04.html code and expected blocks vs twins",
    "PASS", FRESH + "ledgers/LX1/scripts/LX1-b-r21/twin_compare_r21.py -> out/twin_compare_r21.out: page code equals twin after the "
    "trailing newline (111/176/190 lines vs 112/177/191); expected blocks (38, 56, 17 lines) equal the twin stdout exactly.")
for L in ("L01", "L03", "L04"):
    row(f"lx1b-page-smoke-{L}", "2.9-smoke", f"course/modules/LX/LX1/{L}.html",
        "PASS", FRESH + f"tools/page_smoke.py --unit LX1 --pages {L} -> out/page_smoke_{L}.out: 'page_smoke modules/LX/LX1/{L}.html: PASS', exit 0.")
row("lx1b-ruff-mypy", "2.5-labs", "tests/labs/LX1/*.py",
    "PASS", FRESH + "ruff check tests/labs/LX1 -> out/ruff_check.out 'All checks passed!'; ruff format --check -> out/ruff_format.out "
    "'7 files already formatted'; mypy --no-incremental tests/labs/LX1 -> out/mypy.out 'Success: no issues found in 7 source files'.")
row("lx1b-pytest", "2.5-labs", "tests/test_labs.py",
    "PASS", FRESH + "python -m pytest tests/test_labs.py -q -> out/pytest_labs.out, 100%, exit 0.")
row("lx1b-verify-refs", "2.1-citations", "references/references.json; tools/verify_refs.py",
    "PASS", FRESH + "verify_refs.py --offline -> out/verify_refs_offline.out '560 entries, 0 problems'; verify_refs.py --unit LX1 (live) -> "
    "out/verify_refs_live_LX1.out '4 of 560 entries, 0 problems', exit 0.")
row("lx1b-citations-L01", "2.1-citations", "course/modules/LX/LX1/L01.html:304, :489; references/references.json garber2000famous",
    "PASS", "Re-read this round: L01:304 and :489 cite the title only; record garber2000famous (Garber, Famous First Bubbles, 2000, "
    "DOI 10.7551/mitpress/2958.001.0001, verified_by crossref) matches the title and year; the curriculum sources string (curriculum/curriculum.json LX1) lists the same book. No passage is attributed.")
row("lx1b-citations-L03", "2.1-citations", "course/modules/LX/LX1/L03.html:640, :405; references/references.json friedman1963monetary",
    "PASS", "Re-read this round: L03 section 10 and the canon-breaks bullet cite the key and the title only and type no author. "
    "Registry record friedman1963monetary lists Friedman only; the registry-flag is recorded in registry_flags, not a page failure.")
row("lx1b-citations-L04", "2.1-citations", "course/modules/LX/LX1/L04.html:569-575 (References)",
    "PASS", "Re-read this round: L04 references cite no registry key and give the MANIFEST citation for fx_monthly, which matches course/assets/data/market/MANIFEST.json (citation, retrieved 2026-10-19).")
row("lx1b-fetch-check", "2.8-data", "course/assets/data/market/fx_monthly.csv; MANIFEST.json",
    "PASS", FRESH + "tools/fetch_data.py --check -> out/fetch_check.out: 'fetch_data: 3 datasets, 0 problems', exit 0.")
row("lx1b-fx-rebuild", "2.8-data", "course/assets/data/market/fx_monthly.csv; MANIFEST fx_monthly; tools/fetch_data.py",
    "PASS", R20 + "git diff --quiet d1083bf1 6d22ff56 -- course/assets/data/market tools/fetch_data.py tools/data_sources.yaml is silent. "
    "Round 19 rebuilt the CSV from the live feed in a scratch copy and the bytes matched the MANIFEST sha256; not repeated this round.")
row("lx1b-fx-licence", "2.8-data", "tools/data_sources.yaml fx_monthly; MANIFEST licence_url",
    "PASS", FRESH + "plain curl -sS -L https://www.federalreserve.gov/disclaimer.htm -> HTTP 200 (out/fed_disclaimer_r21.curl, out/fed_disclaimer_r21.html); the page contains 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.', the quoted licence in MANIFEST and tools/data_sources.yaml.")
row("lx1b-fx-guard", "2.8-data", "tests/labs/LX1/lab-LX1-L04-1.py load_column, parse_rate",
    "PASS", FRESH + "ledgers/LX1/scripts/LX1-b-r21/fail_loud_L04_r21.py -> out/fail_loud_L04_r21.out: blank GBP cell, text cell, missing month, zero rate and missing GBP column each raise ValueError; 'all raise: True'.")
row("lx1b-fx-gbp-clean", "2.8-data", "course/assets/data/market/fx_monthly.csv (GBP)",
    "PASS", FRESH + "the twin's load_column (which raises on a blank, text, zero or non-consecutive month) runs clean (out/twin_L04.out exit 0); rederive_r21.py: 669 rows 1971-01 to 2026-09, 668 changes, header has GBP.")
row("lx1b-honest-data", "2.8-data", "course/modules/LX/LX1/L03.html:76; L04.html:112-114; L01.html:131-133",
    "PASS", FRESH + "L03:76 honest-pending note (no redistributable series; lab SIMULATED); L04:112-114 labels Part A SIMULATED and states Parts B to D read only fx_monthly.csv; L01:131-133 labels the price path SIMULATED.")
row("lx1b-L04-simulated-label", "2.8-data", "course/modules/LX/LX1/L04.html:113, :114; tests/labs/LX1/lab-LX1-L04-1.py docstring",
    "PASS", FRESH + "L04:113 heading 'Lab 1 · Part A SIMULATED'; :114 hypothesis; lab docstring at L04.html:138-139 calls Part A a SIMULATED model check, not data.")
row("lx1b-L04-manifest-note", "2.8-data", "course/modules/LX/LX1/L04.html:112, :114, :117-123",
    "PASS", FRESH + "MANIFEST.json fx_monthly: rows 669, first 1971-01, last 2026-09, retrieved 2026-10-19, sample month_end, invert [CAD, CHF, DKK, JPY, NOK, SEK]; fx_daily and ust_daily first 2000-01-03; tools/data_sources.yaml note: 'Each value is the last noon rate of its month ... the release's own monthly series are monthly averages', 'Spot rates only'.")
row("lx1b-open-items-missing", "2.9-structure", "plans/LX1-open-items.md",
    "PASS", FRESH + "read in full: D-1 (L03 data request), Bretton Woods definition pending, B2 credit-channel record, N1 Kindleberger and Aliber, N2 Friedman record.")
row("lx1b-plan-coverage", "2.9-structure", "plans/LX1-build-plan.md §2.1, §3; plans/FINAL-ARCHITECT-RULINGS.md rulings 14, 16",
    "PASS", R20 + "plans/LX1-build-plan.md byte-identical. FINAL-ARCHITECT-RULINGS.md changed only by the added ruling 26 (hunk @@ -71,3 +71,10 @@); rulings 14 and 16 re-read this round (lines 32-38) and unchanged. L01 P_t not used; L03 P_t is the price index; L01 observed price A_t (ruling 16). L04 'definition pending' dfn for bretton-woods-system (ruling 14).")
row("lx1b-hours", "2.9-structure", "course/modules/LX/LX1/L01.html:2, :34; L03.html:2, :34; L04.html:2, :34; index.html:31",
    "PASS", FRESH + "data-hours=\"10\" on L01, L03 and L04; eyebrows '10 study hours'; index 'Module LX1 · Tier U · 50 hours' (curriculum hours 50 = 4 x 10 + project). Hub split is checked by check_pages PASS.")
row("lx1b-delta-hunks", "2.9-structure", "git diff d1083bf1 6d22ff56 for slice b; round-20 hunks L03:142, :383; L04:448; cards c092",
    "PASS", "Round-20 hunks: L03.html:142, :383 and L04.html:448 are byte-identical in d1083bf1..6d22ff56 (git diff silent for those files); the card c092 hunk is re-verified in lx1b-cards-c092-hypothesis.")
row("lx1b-delta-r21", "2.9-structure", "git diff d1083bf1 6d22ff56 for slice b: L01.html (:96, :99, :310-324, :339-350, :396-399, :439-457); cards.json c052, c053, c059, c083, c086, c092",
    "PASS", FRESH + "every hunk read: out/delta_d1083bf1_6d22ff56_slice_b.diff (159 lines). L01:99, :313, :324, :396-399, :439 add r > -1 and 1 + g > 0 to the g >= r case (correct); L01:96 and :350 cite (A0) for 1 + g > 0 correctly; L01:342 lists the hypotheses of Proposition 1.4 for Mechanics 3 (correct); L01:457 rewords the quiz 8 prompt without changing its answer; L01:445 changed to 'Since r > -1' and is still incomplete (lx1b-quiz-explanations). Cards: c052, c053, c059, c083 change \\bar{x} to xbar only (text matches L04:85-92); c086 and c092 carry the hypotheses (re-verified).")
row("lx1b-num-L01-closed-form", "2.2-numbers", "course/modules/LX/LX1/L01.html:132, :87, :282, :396-399, :417-435",
    "PASS", FRESH + "ledgers/LX1/scripts/LX1-b-r21/rederive_r21.py -> out/rederive_r21.out: F0 = 20000/3 (rounds 6667); q = 103/109 (0.944954); S_N identity exact for N = 10, 60, 200; F0 q^N rounds 3785, 223, 0; F2 = 7072.67 (7073); 250/0.06 = 4166.67 (4167); F3 at 250 = 4686.93 (4687); S10 at 100, r = g = 5% = 20000/21; g* = 7/300 = 0.023333.")
row("lx1b-num-L01-lab-output", "2.5-labs", "course/modules/LX/LX1/L01.html:244-282 (expected block) vs twin stdout",
    "PASS", FRESH + "out/twin_compare_r21.out expected == twin stdout (38 lines); rederive_r21.out reproduces the gaps [-200, 68, 141, 146, 301, 0, -398, 2050, 676, 2175, 2151, -92, 285], 9 of 13 positive, max 2175 at t = 9, and 13 of 13 under 1 percent.")
row("lx1b-num-L01-prose", "2.2-numbers", "course/modules/LX/LX1/L01.html:282, :363, :367, :370-371, :378, :400",
    "PASS", FRESH + "rederive_r21.out: 9/13 = 0.6923; 13 - 9 = 4; F9 = 8698.4879 (8698.49), 0.25 F9 = 2174.62; 2175/8698 = 0.250057 (25.01 percent); 1.03^9 = 1.30477318; g* = 0.023333 (2.33 and 2.3333 percent).")
row("lx1b-num-L01-witness", "2.2-numbers", "course/modules/LX/LX1/L01.html:114, :120, :321, :462",
    "PASS", FRESH + "rederive_r21.out: F0(1 percent) = 400/0.08 = 5000; F0(3 percent) = 20000/3 = 6666.67; gaps +1000 and -2000/3 at A0 = 6000; Part C t = 0 alternative fundamental 5000.")
row("lx1b-num-L01-s5-example", "2.2-numbers", "course/modules/LX/LX1/L01.html:310, :322; quiz L01.html:417-421; misconception :322-323",
    "PASS", FRESH + "400/1.09 = 40000/109 = 366.97 (367); closed form at g = 3 percent = 6666.67 (6667); quiz 2 answer 6666.67; quiz 3 answer 7072.67.")
row("lx1b-num-L03-depth", "2.2-numbers", "course/modules/LX/LX1/L03.html:149, :362-363, :383, :491, :496-498, :545-546, :577, :596",
    "PASS", FRESH + "ledgers/LX1/scripts/LX1-b-r21/rederive_r21.py (exact Fractions): depth X = 9.204597 percent (9.20), depth Y = 2.686713 percent (2.69), difference 6.517884 (6.52 from unrounded; printed 9.20 - 2.69 = 6.51, disclosed at L03:383), ratio X/Y = 3.425970 (3.4260), same for phi = 1/2, 1 and 3; V12 = 1274345.2124 (1274345); V4 = 1084165.7847 (1084166).")
row("lx1b-num-L03-path", "2.2-numbers", "course/modules/LX/LX1/L03.html:331-357 (expected block) vs model equations",
    "PASS", FRESH + "ledgers/LX1/scripts/LX1-b-r21/l03_partA_r21.py -> out/l03_partA_r21.out: 26 Part A rows (both economies, t = 0 to 12) recomputed from P_t, V_t, K_t, L_t, psi_t, f_t with exact Fractions: 0 mismatches; baseline 0.2500.")
row("lx1b-num-L03-M-E-Q", "2.2-numbers", "course/modules/LX/LX1/L03.html:441, :448, :455, :491, :498, :505, :596, :610",
    "PASS", FRESH + "rederive_r21.out: P4 = 5764801/6250000 = 0.92236816; K4 = 3915834.2153 (3915834); L4 = 0.2768671 (0.2769); E1 exact 2.6867; E2 6.517884 and printed 6.51; E3 eight periods; quiz 8 V12 exact 1274345.2124.")
row("lx1b-num-L04-stats", "2.2-numbers", "course/modules/LX/LX1/L04.html:306-322 (expected), :323, :476-477",
    "PASS", FRESH + "rederive_r21.out (own csv reader, math.log, fsum): s1 = 0.027935277918 (0.027935), s2 = 0.024699501388 (0.024700), 668 and 321 changes, zero months 1976-07, 2012-07, 2019-11, largest |change| 0.135845673 at 1985-03 and -0.096574740 at 2008-10; ratio 0.884168808 (0.8842); difference -0.003235777 (-0.003236).")
row("lx1b-num-L04-display-diff", "2.2-numbers", "course/modules/LX/LX1/L04.html:323; key row :476",
    "PASS", FRESH + "rederive_r21.out: printed s2 - s1 from printed figures = 0.024700 - 0.027935 = -0.003235, while the unrounded difference rounds to -0.003236; disclosed at L04:323 and in misconception 2.")
row("lx1b-num-L04-derived", "2.2-numbers", "course/modules/LX/LX1/L04.html:354, :373, :380, :387, :430, :455, :541, :564",
    "PASS", FRESH + "rederive_r21.out: ln 1.1 = 0.0953101798; 0.1 - ln 1.1 = 0.0046898 (0.004690); M2 sd = 0.025166; E2 simple change exp(-0.0965747400) - 1 = -0.0920580 (-0.092058); R2 tanh(0.0679228) = 0.0678186 (0.067819, 4 dp 0.0678); bound at h = 0.0678 = 0.1358084 (0.135808); quiz 'ln 1.1' 0.095310.")
row("lx1b-scope-start", "2.2-numbers", "course/modules/LX/LX1/L04.html:110, :326, :387, :462; card LX1-c063; lab docstring at L04.html:127-130",
    "PASS", FRESH + "rederive_r21.out and the twin: window two's first change (dated 2000-01) uses the 1999-12 rate; the start month 2000-01 is the first month of fx_daily and ust_daily (MANIFEST first 2000-01-03). The wording at L04:110 is a separate row (lx1b-L04-window-two-wording).")
row("lx1b-math-L01", "2.4-mathematics", "course/modules/LX/LX1/L01.html:57-99",
    "PASS", FRESH + "Assumption 1.1 (A0 gives r > g > -1 and 1 + r > 0), Definition 1.2, Theorem 1.3 (q in (0,1) under A0; 1 - q = (r-g)/(1+r)), Proposition 1.4 (q >= 1 from g >= r and 1 + r > 0; terms >= d1/(1+r) > 0) re-derived line by line.")
row("lx1b-math-L01-prop22", "2.4-mathematics", "course/modules/LX/LX1/L01.html:104-121",
    "PASS", FRESH + "Proposition 2.2 hypotheses (A3) and (A4) include r > g, r > g', 1 + g > 0, 1 + g' > 0, g < g'; the ordering proof is correct; the witness numbers were re-derived.")
row("lx1b-math-L03", "2.4-mathematics", "course/modules/LX/LX1/L03.html:94-143",
    "PASS", FRESH + "Lemma 3.1 identity C(y-x)/((C-x)(C-y)) re-derived; Proposition 3.2 (a), (b), (c) and Corollaries 3.3 and 3.4 re-derived against L03:94-143; each hypothesis used appears in the statement (A1 for V_t, A2 for V_m < C, A3 for beta phi > 0).")
row("lx1b-math-L04", "2.4-mathematics", "course/modules/LX/LX1/L04.html:57-107",
    "PASS", FRESH + "Proposition 1.2 telescoping and Remark 1.3; Proposition 2.2 (a) and (b) with n >= 2; each step re-derived, including the denominator n - 1 >= 1.")
row("lx1b-math-problems", "2.4-mathematics", "course/modules/LX/LX1/L01.html:330-389; course/modules/LX/LX1/L03.html:431-532; course/modules/LX/LX1/L04.html:355-470",
    "PASS", FRESH + "every problem and solution on the three pages read; each number re-derived in rederive_r21.py or by hand (see the num rows); L01 Proof 2 and Mechanics 3 now carry the hypotheses; L03 P1-P3, R1-R3 and L04 P1-P3, R1-R2 re-checked.")
row("lx1b-grades", "2.3-grades", "course/modules/LX/LX1/L01.html:397-401; L03.html:542-546; L04.html:474-477; cards grades",
    "PASS", FRESH + "round-20 FAIL (L01:399, 'No finite benchmark when g >= r ...' graded T without its hypotheses) is fixed: L01:399 now lists d_1 > 0, 1 + g > 0, r > -1 and g >= r. Re-graded every key-results row and every graded card: T for proved statements, C for SIMULATED lab outputs and the L04 data results (basis named).")
row("lx1b-notation", "2.4-notation", "course/modules/LX/LX1/L01.html; L03.html; L04.html; notation/notation.json",
    "PASS", FRESH + "registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q and the registered macros: none used in the three pages. Locally defined letters (S, N, m, lambda, h, s, ell, A, B, P, V, K, L, phi, beta, delta, psi, f, G, C, H) are each defined in their lesson before use.")
row("lx1b-notation-P", "2.4-notation", "course/modules/LX/LX1/L01.html (whole page); course/modules/LX/LX1/L03.html:58-59, :116, :157-163; L04 none",
    "PASS", FRESH + "P_t appears only in L03 as the price index (ruling 16); L01 and L04 do not use P_t.")
row("lx1b-notation-A", "2.4-notation", "course/modules/LX/LX1/L01.html:105, :114, :119-120, :143-144, :377, :450; cards LX1-c006",
    "PASS", FRESH + "A_t is the observed price in L01 only (Definition 2.1 and Proposition 2.2); no other use in slice b.")
row("lx1b-notation-K", "2.4-notation", "course/modules/LX/LX1/L03.html:65 (first use) to :605; cards c027, c071, c082",
    "PASS", FRESH + "K_t is borrower net worth (Assumption 1.2) with K_0 the baseline; no conflicting use.")
row("lx1b-notation-P-L03", "2.4-notation", "course/modules/LX/LX1/L03.html:58-59, :116, :157-163, :211, :464-473",
    "PASS", FRESH + "P_t = (1 - delta)^min(t, m) defined at Assumption 1.1 and used consistently (see lx1b-num-L03-path).")
row("lx1b-notation-N", "2.4-notation", "course/modules/LX/LX1/L01.html:67, :74, :82-83, :87; course/modules/LX/LX1/L04.html (none)",
    "PASS", FRESH + "N is the partial-sum horizon in L01 (defined in Definition 1.2 and Theorem 1.3); L04 uses n for window counts.")
row("lx1b-notation-registered", "2.4-notation", "course/modules/LX/LX1/L01.html; L03.html; L04.html",
    "PASS", FRESH + "no registered symbol (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) and no registered macro appears in slice b (symbol inventory of all math spans).")
row("lx1b-notation-check-math-spans", "2.4-notation", "course/modules/LX/LX1/L01.html; L03.html; L04.html math spans",
    "PASS", FRESH + "symbol inventory of every \\(...\\) span on the three pages (printed by grep in this round): no unregistered macro, no collision with a registered symbol.")
row("lx1b-dag-links", "2.9-dag", "course/modules/LX/LX1/L01.html:37; L03.html:37, :54, :90; L04.html:37, :105, :336",
    "PASS", FRESH + "data-concept links: L01 growing-perpetuity, present-value, geometric-series, exponential-and-logarithm (M1, in closure {E1, E5, FC1, M1, M2, P0.1} computed from curriculum.json); L03 debt-deflation, gold-standard (L02); L04 gold-standard (L02), lender-of-last-resort (L03), exponential-and-logarithm (M1), bretton-woods-system (LX1). Anchors resolve (see lx1b-r20-dfn-anchors).")
row("lx1b-dag-outside-closure", "2.9-dag", "course/modules/LX/LX1/L04.html:122 ('forward-rate'); course/modules/LX/LX1/L04.html R1 solution (p-value)",
    "FAIL", FRESH + "name scan of the three pages against the curriculum concept index (curriculum/curriculum.json concepts) and the plan's §4 table (D1-D15). Outside the closure {E1, E5, FC1, M1, M2, P0.1}: 'forward rate' (concept forward-rate, owner FI1) appears by name at L04:122 ('no forward-rate column (a forward rate is an exchange rate agreed now for exchange at a later date)'), and 'p-value' (concept p-value, owner S1) appears by name in the L04 R1 solution. Neither is in plan §4 D1-D15, and the plan's own text uses 'spot rate' and 'standard deviation' as plain terms, so those two are not flagged. The round-20 scan covered only D1-D15 names.",
    "Judgement row (DAG rule 14). Either rephrase without the concept names (L04:122: 'no column of exchange rates for delivery at a later date'; R1: describe the tail probability without the term 'p-value') or record a plain-prose decision for forward-rate and p-value as rows D16-D17 in plans/LX1-build-plan.md §4 for the architect to confirm.")
row("lx1b-concepts-defs", "2.9-dag", "course/modules/LX/LX1/L01.html:105, :290; L03.html:87, :390; L04.html:86",
    "PASS", FRESH + "each of the seven introduced concepts has exactly one data-concept dfn across L01-L04: speculative-bubble and financial-panic (L01), gold-standard and debt-deflation (L02), credit-channel-depression and lender-of-last-resort (L03), bretton-woods-system (L04, pending per ruling 14). grep of dfn ids: no duplicate.")
row("lx1b-concept-index-title", "2.9-dag", "course/concepts.html:631-636",
    "PASS", "Re-read this round: concepts.html lists the LX1 concepts as 'defined here' (Bretton Woods system, Debt deflation, Financial panic, Gold standard, Lender of last resort, Nonmonetary (credit) channel of the Great Depression, Speculative bubble). Generated file, not edited.")
row("lx1b-L04-bretton-definition", "2.4-mathematics", "course/modules/LX/LX1/L04.html:38, :86, :337, :358, :553-557",
    "PASS", FRESH + "the 'definition pending' dfn (L04:86) states the fixed-exchange-rate model separately and says it is not a definition of the historical system; L04:337 and :358 do not state a historical fact; L04:553-557 name no source; ruling 14 permits this.")
row("lx1b-banned-phrases", "2.9-prose", "course/modules/LX/LX1/L01.html; L03.html; L04.html",
    "PASS", FRESH + "ledgers/LX1/scripts/LX1-b-r21/prose_scan_r21.py: 'ellipsis outside code/math: 0', 'banned-literal hits: 0' on each page.")
row("lx1b-process-words", "2.9-prose", "course/modules/LX/LX1/L01.html; L03.html; L04.html",
    "PASS", FRESH + "prose_scan_r21.py output: no build, builder, verifier, REQUESTS or unit-report term in learner text; the 'round' hits are arithmetic ('rounds to 6667 cents').")
row("lx1b-scope-words", "2.9-prose", "course/modules/LX/LX1/L01.html; L03.html; L04.html",
    "PASS", FRESH + "prose_scan_r21.py: 225 scope/process hits (75 / 80 / 70) read in full; each sits in a derivation, a lab sentence, a definition, a hypothesis list or a misconception, and the claim holds (the g >= r sentences are re-checked in lx1b-L01-prop14-hypotheses).")
row("lx1b-structure", "2.9-structure", "course/modules/LX/LX1/L01.html; L03.html; L04.html",
    "PASS", FRESH + "each page has header, grade legend, why-it-matters, numbered assumptions, definitions and results, a lab with SIMULATED label where generated, canon-breaks, misconceptions, problem set in tiers, key results, quiz and references, in the order the round-20 row recorded.")
row("lx1b-quiz-explanations", "2.9-structure", "course/modules/LX/LX1/L01.html:439-445 (quiz 6); L01.html:405-483; L03.html:552-636; L04.html:483-567",
    "FAIL", FRESH + "L01 quiz 6 prompt (:439) now lists d_1 > 0, 1 + g > 0, r > -1 and g >= r, which is correct. The explanation (:445) reads 'Since r > -1, each discounted term is at least d_1/(1 + r) > 0'. That sentence gives the bound from r > -1 alone, but the bound needs q^(k-1) >= 1, which needs g >= r (q >= 1). Counterexample to the stated inference: d_1 = 1, r = 9 percent, g = 0 satisfies r > -1 and not g >= r; the k = 2 term is 1/1.09^2 = 0.8417 < 1/1.09 = 0.9174. Other quiz explanations (L01 1-5, 7-10; L03 1-11; L04 1-10) agree with their lessons.",
    "L01.html:445: replace the explanation with 'Since g >= r and r > -1, q = (1 + g)/(1 + r) >= 1, so each discounted term d_1 q^(k-1)/(1 + r) is at least d_1/(1 + r) > 0 (Proposition 1.4).'")
row("lx1b-L03-remark42-solvency", "2.4-mathematics", "course/modules/LX/LX1/L03.html:64-67, :395",
    "PASS", FRESH + "Remark 4.2: K_t = C - V_t with C = K_0 + D; V_t <= V_m < C by Proposition 3.2(a) and Assumption 1.2, so K_t > 0 each period (re-derived).")
row("lx1b-L03-ratio-claims", "2.3-grades", "course/modules/LX/LX1/L03.html:404; :516; :523",
    "PASS", FRESH + "the ratio statements in the lesson match Part D's three printed ratios (3.4260 each) and Corollary 3.4; no equality is claimed beyond the printed digits.")
row("lx1b-L03-r1-no-result", "2.4-mathematics", "course/modules/LX/LX1/L03.html:516",
    "PASS", FRESH + "R1 solution states that a facility would need a new term and a new proof and asserts no result about it.")
row("lx1b-L03-lab-checks-overreach", "2.5-labs", "course/modules/LX/LX1/L03.html:145, :383; twin docstring lines 25-26 and code 171-174",
    "PASS", FRESH + "the twin's Part D computes and prints the three ratios with no equality test; Part C checks adjacent orderings only; the interpretation at L03:383 says 'as Corollary 3.4 implies', which is what the printed digits show.")
row("lx1b-L03-misconception-scope", "2.4-mathematics", "course/modules/LX/LX1/L03.html:413-426; proof :128-131",
    "PASS", FRESH + "misconceptions 1-4 re-read: no bank or failure in the model; the Corollary 3.3 proof uses only m, m', the closed form of V_m, the bound V_m < K_0 + D, Lemma 3.1 and Proposition 3.2(b); the lending misconception matches Definition 4.1; the beta-proportionality matches Proposition 3.2(b).")
row("lx1b-cards-l01-l03-l04", "2.7-cards", "course/modules/LX/LX1/cards.json (L01 17, L03 32, L04 24)",
    "PASS", FRESH + "ledgers/LX1/scripts/LX1-b-r21/cards_check_r21.py -> out/cards_check_r21.out: 90 cards, unique ids, per lesson L01 17, L02 17, L03 32, L04 24; new ids none; every number in the changed cards appears in its lesson. The script also lists 28 ungraded cards (grade or basis None); these are definitional or restated-lesson cards, which the round-20 row also accepted as the builder's convention.")
row("lx1b-cards-c052-c053", "2.7-cards", "cards.json LX1-c052, LX1-c053, LX1-c059, LX1-c083 vs course/modules/LX/LX1/L04.html:84-94",
    "PASS", FRESH + "text-only change \\bar{x} -> xbar in four cards; each back still matches L04 Definition 2.1, Proposition 2.2 and Remark 2.3.")
row("lx1b-cards-L01-hypotheses", "2.7-cards", "cards.json LX1-c002..c007, c013, c085, c086, c092, c093",
    "PASS", FRESH + "each front states the hypotheses of its result: c002, c003 (A0, A1); c004 (A0); c005 (A1 with d_1 > 0 and 1 + g > 0; A2 with r > -1 and g >= r); c007, c086, c093 (A3, A4 with r > g, r > g', 1 + g > 0, 1 + g' > 0); c013 and c092 (Proposition 1.4 hypotheses in full); c085 (Assumption 1.1). The round-20 FAIL on c092 is fixed.")
row("lx1b-cards-L03-hypotheses", "2.7-cards", "cards.json LX1-c030..c036, c079, c082, c087",
    "PASS", FRESH + "each card's hypotheses (Assumptions 1.1 to 1.3 and Lemma/Proposition/Corollary 3.x) re-read against L03:94-143 and match; c067 matches L03:383.")
row("lx1b-cards-c092-hypothesis", "2.7-cards", "course/modules/LX/LX1/cards.json LX1-c092 (front)",
    "PASS", FRESH + "front now reads 'With d_1 > 0, 1 + g > 0, r > -1 and g >= r (Proposition 1.4), ...'; back unchanged and matches L01:324 (400/(0.09 - 0.10) = -40000 cents).")
row("lx1b-L01-prop14-hypotheses", "2.4-mathematics", "course/modules/LX/LX1/L01.html:99, :313, :324, :399, :439 (and :445, tracked in lx1b-quiz-explanations)",
    "PASS", FRESH + "the round-20 hypothesis omissions are fixed at L01:99, :313, :324, :399 and :439; each g >= r statement now carries d_1 > 0, 1 + g > 0, r > -1. The remaining gap in the quiz explanation at :445 is a separate FAIL row (lx1b-quiz-explanations).")
row("lx1b-L01-misc3-closed-form", "2.9-prose", "course/modules/LX/LX1/L01.html:324 (misconception 3); card LX1-c092",
    "PASS", FRESH + "misconception 3 now reads 'Under g >= r with d_1 > 0, 1 + g > 0 and r > -1, each discounted dividend is at least d_1/(1 + r) > 0' and its evidence cites Proposition 1.4 with its hypotheses.")
row("lx1b-L01-benchmark-finite-hypothesis", "2.4-mathematics", "course/modules/LX/LX1/L01.html:99",
    "PASS", FRESH + "L01:99 now carries d_1 > 0, 1 + g > 0, r > -1 and g >= r; the counterexample d_1 = 1, r = -2, g = -1/2 is outside the stated hypotheses.")
row("lx1b-mutants-none", "2.6-mutation", "tests/labs/LX1/*; course/modules/LX/LX1/project.html (slice a)",
    "PASS", "No mutants are required in slice b: LX1 is rubric-graded (run_graders: no autograder) and lab twins are demonstrations (ruling in the verifier brief). Recorded as no mutants.")
row("lx1b-r20-L03-independent-derivation", "2.2-numbers", "course/modules/LX/LX1/L03.html Lemma 3.1, Prop 3.2, Cor 3.3-3.4",
    "PASS", FRESH + "rederive_r21.py and l03_partA_r21.py (exact Fractions): depths, Part A table, ratio; no mismatch.")
row("lx1b-r20-L01-lab-replay", "2.5-labs", "tests/labs/LX1/lab-LX1-L01-1.py",
    "PASS", FRESH + "twin run under python -I -W error exit 0; stdout equals the page's expected block.")
row("lx1b-r20-L04-lab-replay", "2.5-labs", "tests/labs/LX1/lab-LX1-L04-1.py",
    "PASS", FRESH + "twin run under python -I -W error exit 0 with a data/ copy; stdout equals the page's expected block.")
row("lx1b-r20-L04-R2-band", "2.2-numbers", "course/modules/LX/LX1/L04.html:452-455 (R2 solution); quiz L04.html:541-564",
    "PASS", FRESH + "tanh(0.135846/2) = 0.067819; rounded 0.0678; bound 0.135808 < 0.135846; the statement 'does not quite reach' is correct.")
row("lx1b-r20-L04-proof-P2-P3", "2.4-mathematics", "course/modules/LX/LX1/L04.html:393-418 (proof problems P2, P3)",
    "PASS", FRESH + "P2 band bound and P3 ln(1+u) <= u re-derived (f' = -u/(1+u) sign analysis).")
row("lx1b-r20-L03-M-proof-P1-P3", "2.4-mathematics", "course/modules/LX/LX1/L03.html:431-520 (M1-M3, P1-P3, E1-E3, R1-R3)",
    "PASS", FRESH + "M1 to M3 and P1 to P3 re-derived; E1 to E3 and R1 to R3 read against the printed output.")
row("lx1b-r20-fail-loud-L04", "2.8-data", "tests/labs/LX1/lab-LX1-L04-1.py load_column",
    "PASS", FRESH + "out/fail_loud_L04_r21.out: 'all raise: True' (blank, text, missing month, zero rate, missing GBP column).")
row("lx1b-r20-scope-words-readthrough", "2.9-prose", "course/modules/LX/LX1/L01.html; L03.html; L04.html",
    "PASS", FRESH + "out/prose_scan_r21.out read in full; each hit is inside a derivation, a model or lab sentence, a definition or a misconception.")
row("lx1b-r20-dfn-anchors", "2.9-dag", "course/modules/LX/LX1/L01.html; L03.html; L04.html",
    "PASS", FRESH + "every href with a fragment on the three pages resolves: L02 #def-debt-deflation, #def-gold-standard; L03 #def-lender-of-last-resort; L04 #def-bretton-woods-system; L01 dfn ids present.")
row("lx1b-r20-sampled-cards", "2.7-cards", "course/modules/LX/LX1/cards.json (all 73 L01/L03/L04 cards read this round)",
    "PASS", FRESH + "all 73 cards read in full this round against their lessons; no card contradicts its lesson.")
row("lx1b-r20-licence-page-curl", "2.8-data", "https://www.federalreserve.gov/disclaimer.htm (plain curl)",
    "PASS", FRESH + "curl -sS -L returned HTTP 200 and the quoted licence text (out/fed_disclaimer_r21.curl).")
row("lx1b-L04-window-two-wording", "2.9-prose", "course/modules/LX/LX1/L04.html:110 (Section 3 introduction)",
    "FAIL", FRESH + "L04:110 says window one 'start[s] from the first month of the snapshot, 1971-01' (its base month, the rate of the change dated 1971-02 is the 1971-01 rate) and window two 'start[s] from the first month in which the other two embedded snapshots have data', which is 2000-01. The code (twin lines 127-130, rate_before_two = rate of 1999-12) and L04:326 say window two's first change, dated 2000-01, uses the 1999-12 rate. The same phrase therefore names a different object for the two windows (base month in one, first dated month in the other). Low severity, wording only.",
    "L04.html:110: rewrite the window-two sentence as 'Window two is the changes dated 2000-01 to 2026-09; its first change uses the rate of 1999-12, and 2000-01 is the first month in which the other two embedded snapshots have data.'")

registry_flags = [
    "friedman1963monetary: registry record authors lists Friedman only (verified_by openlibrary); the curriculum source string (curriculum/curriculum.json LX1 sources) reads 'Friedman & Schwartz, A Monetary History ... (1963)'. Not re-resolved this round; pages cite the key and type no author, so no page row fails. Architect may correct the record via tools/add_reference.py (round-20 N2).",
    "Bernanke (1983), AER 73(3), credit-channel source (B2): no registry record; review_queue.json candidate is an NBER working paper and must not be admitted as the AER article. L03 makes no empirical credit-channel claim.",
    "Kindleberger and Aliber (2015) (N1): not in the registry; no LX1 page cites it.",
    "Bretton Woods system definition and end date (B3): no admitted source; L04 carries the ruling-14 'definition pending' dfn. Honest gap until a REFERENCE_REQUEST is resolved.",
    "Bubble-existence counter-account: no registered key addresses bubble existence; kaldor1939speculation is not treated as a counter-account.",
]

notes = [
    "Round 21 pin 6d22ff56 (round-20 pin d1083bf1). Delta d1083bf1..6d22ff56 for slice b: L01.html (Proposition 1.4 hypothesis fixes at :99, :313, :324, :342, :350, :396-399, :439, :445, :454, :457) and cards.json (c052, c053, c059, c083, c086, c092). plans/FINAL-ARCHITECT-RULINGS.md gained ruling 26 only. L03.html, L04.html, the twins, tests, data, MANIFEST, tools/fetch_data.py and the LX1 plan are byte-identical to d1083bf1. Full delta saved at ledgers/LX1/scripts/LX1-b-r21/out/delta_d1083bf1_6d22ff56_slice_b.diff.",
    "Full read this round: L01.html (all 501 lines), L03.html (all 653), L04.html (all 586), the three twins, all 73 L01/L03/L04 cards. Page lab code equals the twin up to the trailing newline and each expected block equals the twin stdout.",
    "Independent re-derivations (own Fraction and Decimal code, not the lab's helpers): rederive_r21.py (L01 closed forms, witnesses, Part B gaps and counts, Part C; L03 depths, ratios, V and K and L values; L04 statistics, zero months, extremes, band and quiz numbers) and l03_partA_r21.py (26 Part A rows, 0 mismatches).",
    "Open FAILs for the builder: lx1b-quiz-explanations (L01:445 explanation omits g >= r), lx1b-dag-outside-closure (judgement: forward rate and p-value named outside the closure with no plan decision), lx1b-L04-window-two-wording (L04:110, LOW). All other round-20 FAIL rows are fixed.",
    "Mutants: none. LX1 is rubric-graded and the lab twins are demonstrations, so no grader mutants apply to slice b (verifier rules, rulings).",
    "Gates on the pin: check_pages, check_dag, check_projects, run_graders, run_labs, each twin alone under python -I -W error, page_smoke for L01, L03, L04, ruff check and format, mypy --no-incremental, pytest tests/test_labs.py, verify_refs --offline and --unit LX1 (live), fetch_data --check: all PASS, exit 0.",
    "Cards: check script flags 28 ungraded cards (grade or basis None). Definitional and restated-lesson cards; accepted under the round-20 convention, not a failure.",
    "Scratch: /tmp/lx1b-r21-L01, /tmp/lx1b-r21-L03, /tmp/lx1b-r21-L04 were created per twin run and removed. No other scratch.",
]

summary_fail = [r["id"] for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "LX1",
    "slice": "b",
    "round": 21,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-b (L01, L03, L04 and lab twins), round 21",
    "pin": "6d22ff56 (6d22ff56fcf3a28e40c82952b25a0c3760f92cbc), detached; .venv symlinked; vendor present",
    "base": "d1083bf1 (round-20 pin). Delta d1083bf1..6d22ff56 touches slice b in course/modules/LX/LX1/L01.html and course/modules/LX/LX1/cards.json (c052, c053, c059, c083, c086, c092); plans/FINAL-ARCHITECT-RULINGS.md (ruling 26 added).",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE21-LX1-b",
    "scratch": "/tmp/lx1b-r21-L01, /tmp/lx1b-r21-L03, /tmp/lx1b-r21-L04 (created per run and removed)",
    "verified_at": "2026-11-09T07:30:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": registry_flags,
    "freshness_flags": [],
    "notes": notes,
    "summary": (
        f"LX1-b round 21 on 6d22ff56 (base d1083bf1): verdict FAIL. Rows: {len(rows)} "
        f"(pass={sum(r['status'] == 'PASS' for r in rows)} fail={sum(r['status'] == 'FAIL' for r in rows)} "
        f"unverifiable=0). Non-PASS: {', '.join(summary_fail)}. All round-20 FAIL rows except the quiz-explanation residue are fixed. "
        "Mutants: 0 (rubric unit, twins are demonstrations)."
    ),
}
dest = ROOT / "ledgers/LX1/LX1-b.json"
dest.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", dest, "rows", len(rows), "fails", summary_fail)
