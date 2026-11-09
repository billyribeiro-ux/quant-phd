"""Writes the round-18 verifier fragment for LX1 slice b (ledgers/LX1/LX1-b.json). Evidence strings cite the scripts and
output files under ledgers/LX1/scripts/LX1-b-r18/ that back each row. Run from the checkout root with .venv/bin/python -I.
"""

import json
import pathlib

S = "ledgers/LX1/scripts/LX1-b-r18"
O = S + "/out"

P = "PASS"
F = "FAIL"


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    return r


rows = [
    # ---- tool gates (run by me on the pin, outputs in out/)
    row("lx1b-check-pages", "2.9 structure (tool gate)", "course/modules/LX/LX1/L01.html; L03.html; L04.html", P,
        f"{S}/gates_r18.sh -> {O}/check_pages_unit.out: 'check_pages LX1: PASS' (exit 0)."),
    row("lx1b-check-dag", "2.9 DAG (tool gate)", "L01.html; L03.html; L04.html", P,
        f"{O}/check_dag_unit.out: 'check_dag LX1: PASS' (exit 0)."),
    row("lx1b-check-projects", "2.6 project gate (unit only; project slice owned elsewhere)", "tools/check_projects.py --unit LX1", P,
        f"{O}/check_projects_unit.out: 'check_projects LX1: PASS' (exit 0)."),
    row("lx1b-run-graders", "2.6 grader (rubric unit)", "tools/run_graders.py --unit LX1", P,
        f"{O}/run_graders_unit.out: 'run_graders LX1: no autograder (grading: rubric)' (exit 0)."),
    row("lx1b-run-labs", "2.5 labs (tool gate)", "tests/labs/LX1/*.py", P,
        f"{O}/run_labs_unit.out: 'run_labs LX1: PASS (7/7)' (exit 0)."),
    row("lx1b-twin-alone-L01", "2.5 labs (twin alone, CPython 3.14.8, -I -W error)", "tests/labs/LX1/lab-LX1-L01-1.py", P,
        f"{S}/run_twins_r18.sh (empty scratch dir): 'L01 exit=0'; {O}/twin_L01.stderr empty; {O}/twin_L01.stdout 38 lines."),
    row("lx1b-twin-alone-L03", "2.5 labs (twin alone)", "tests/labs/LX1/lab-LX1-L03-1.py", P,
        f"{S}/run_twins_r18.sh: 'L03 exit=0'; {O}/twin_L03.stdout 56 lines; stderr empty."),
    row("lx1b-twin-alone-L04", "2.5 labs (twin alone, with data/fx_monthly.csv as data-files requires)",
        "tests/labs/LX1/lab-LX1-L04-1.py", P,
        f"{S}/run_twins_r18.sh: 'L04 exit=0' with data/fx_monthly.csv copied in; {O}/twin_L04.stdout 17 lines; stderr empty. "
        f"Without the file, the loader fails loud (FileNotFoundError), as the page's data-files contract implies."),
    row("lx1b-twin-equals-page-code", "2.5 labs (page code equals twin; expected block equals output)",
        "L01.html code+expected; L03.html code+expected; L04.html code+expected", P,
        f"{S}/twin_compare_r18.py -> {O}/twin_compare_r18.out: for L01, L03, L04 the page code equals the twin with the "
        f"trailing newline stripped (the convention run_labs.py line 74 uses); the strict byte comparison differs only by "
        f"that final newline. The expected block equals the twin's stdout line for line (38, 56, 17 lines)."),
    row("lx1b-page-smoke-L01", "2.9 page_smoke (page alone)", "course/modules/LX/LX1/L01.html", P,
        f"{O}/page_smoke_L01.out: 'page_smoke modules/LX/LX1/L01.html: PASS', exit 0 (run alone)."),
    row("lx1b-page-smoke-L03", "2.9 page_smoke (page alone)", "course/modules/LX/LX1/L03.html", P,
        f"{O}/page_smoke_L03.out: PASS, exit 0 (run alone)."),
    row("lx1b-page-smoke-L04", "2.9 page_smoke (page alone)", "course/modules/LX/LX1/L04.html", P,
        f"{O}/page_smoke_L04.out: PASS, exit 0 (run alone)."),
    row("lx1b-ruff-mypy", "2.5 static gates on the twins", "tests/labs/LX1/*.py", P,
        f"{O}/ruff_check_labs.out 'All checks passed!'; {O}/ruff_format_labs.out '7 files already formatted'; "
        f"{O}/mypy_nocache.out 'Success: no issues found in 3 source files' (mypy --no-incremental on the three twins)."),
    row("lx1b-pytest", "2.5 labs (pytest)", "tests/test_labs.py", P,
        f"{O}/pytest_lx1.out: 7 dots, all pass; {O}/pytest_lx1_collect.out: 'tests/test_labs.py: 7' (exit 0)."),
    row("lx1b-verify-refs", "2.1 citations (registry run)", "references/references.json; tools/verify_refs.py", P,
        f"{O}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems' (exit 0). Live unit run "
        f"{O}/verify_refs_live_unit_r18.out: 'live re-verification of LX1: 4 of 560 entries, 0 problems' (exit 0). "
        f"{O}/verify_refs_unit.out exit 2 is a usage error (the tool rejects --unit with --offline), not a finding."),
    row("lx1b-citations-L01", "2.1 citations and attribution (L01)", "L01.html:303, :488", P,
        "Garber key garber2000famous: registry title 'Famous First Bubbles: The Fundamentals of Early Manias', author "
        "Garber, Peter M., year 2000 (references/references.json, read via python -I). The page cites the title only, "
        "states no passage, and types no date from the book."),
    row("lx1b-citations-L03", "2.1 citations and attribution (L03)", "L03.html:405, :640", P,
        "friedman1963monetary: registry title 'A monetary history of the United States 1867-1960', author Friedman, Milton, "
        "year 1963. The page cites the key at book level, takes no finding from it, and types no second author. The "
        "Bernanke/AER credit-channel source has no key, and the page makes no empirical credit-channel claim (B2)."),
    row("lx1b-citations-L04", "2.1 citations and data source (L04)", "L04.html section 9 (lines 569-575)", P,
        "The one reference is the fx_monthly MANIFEST citation, matching MANIFEST citation field and licence; no registry key "
        "is cited. Stated as not a registry key on the page."),
    row("lx1b-fetch-check", "2.8 data (offline check)", "course/assets/data/market/fx_monthly.csv; MANIFEST.json", P,
        "tools/fetch_data.py --check: '3 datasets, 0 problems' (exit 0). sha256sum of the CSV = 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e, "
        "equal to the MANIFEST fx_monthly sha256; rows 669, first 1971-01, last 2026-09, retrieved 2026-10-19."),
    row("lx1b-fx-rebuild", "2.8 what is reproducible (rebuild from the live feed)", "tools/fetch_data.py; MANIFEST fx_monthly", P,
        "In scratch copy /tmp/lx1b-r18-rebuild: `fetch_data.py --fetch --only fx_monthly` -> 'built fx_monthly: 669 rows, 67392 "
        "bytes, 1971-01 to 2026-09'; `cmp` against the checkout CSV: byte-identical. Raw download sha256 "
        "1c312d2f...f24a differs from MANIFEST raw_sha256 8f370f9c...c6a8: the issuer's live file changed; raw_sha256 is provenance "
        "only (BUILDER_RULES 6.6, VERIFIER 2.8), and the snapshot rebuilds byte-for-byte. Not refreshed."),
    row("lx1b-fx-licence", "2.8 licence (plain curl of licence_url)", "tools/data_sources.yaml fx_monthly; MANIFEST licence_url", P,
        "`curl -s https://www.federalreserve.gov/disclaimer.htm` -> HTTP 200, 85306 bytes (saved as "
        f"{O}/fed_disclaimer_r18.html). The page contains 'Unless otherwise indicated, information on Board's website is in the "
        "public domain and may be copied and distributed without permission. Please cite to the Board as the source of the "
        "information.' This is the grant the MANIFEST and data_sources.yaml quote."),
    row("lx1b-fx-guard", "2.5 fail loud on bad data (twin loader)", "tests/labs/LX1/lab-LX1-L04-1.py parse_rate, load_column", P,
        f"{S}/fail_loud_r18.sh -> {O}/fail_loud_r18.out: blank GBP cell -> ValueError (exit 1); 'n/a' cell -> ValueError; "
        "skipped month 1996-01 -> ValueError 'does not follow the previous month'; missing GBP column -> ValueError. No silent skip."),
    row("lx1b-fx-gbp-clean", "2.8 data cells (GBP column)", "course/assets/data/market/fx_monthly.csv (GBP)", P,
        f"{S}/rederive_numbers_r18.py -> {O}/rederive_numbers_r18.out: 'GBP blank cells: 0' over 669 rows."),
    row("lx1b-honest-data", "4 honest data / pending states", "L03.html:76; L04.html:112-114; L01.html:131-133", P,
        "L03:76 honest-pending note (no redistributable historical series; lab stays SIMULATED); L04 Part A labelled SIMULATED, "
        "real data named with licence and retrieval date; no fabricated historical series anywhere in the three pages."),
    row("lx1b-L04-simulated-label", "2.8 SIMULATED label", "L04.html:113, :114; twin docstring", P,
        "Title line 113 'Part A SIMULATED'; hypothesis line 114 says Part A is 'a constructed model check, not data'; twin docstring "
        "says Parts B to D read the file. Expected block line 306 'Part A: SIMULATED model check, not data'."),
    row("lx1b-L04-manifest-note", "2.8 dataset note (lab names dataset, licence, retrieval date)", "L04.html:112, :114, :117-123", P,
        "data-files=\"fx_monthly.csv\" (line 112); MANIFEST retrieved 2026-10-19, 669 rows, columns AUD..SEK, transform text 'CAD, "
        "CHF, DKK, JPY, NOK, SEK inverted' matches L04:121 ('inverts CAD, CHF, DKK, JPY, NOK and SEK only, so GBP is a direct quote')."),
    row("lx1b-open-items-missing", "2.5 honest-pending requests exist", "plans/LX1-open-items.md", P,
        "Open items contain D-1 (L03 curriculum-lab data request), the Bretton Woods pending-definition item, and the reference "
        "requests for the credit-channel (B2), Kindleberger (N1) and Friedman second-author (N2) items."),

    # ---- numbers (re-derived with exact Fractions and Decimal; scripts/outputs above)
    row("lx1b-num-L01-closed-form", "1 numbers in prose (L01 closed form, partial sums)", "L01.html:132, :87, :282, :396-399, :417-435", P,
        f"{S}/rederive_numbers_r18.py -> {O}/rederive_numbers_r18.out: F0 = 20000/3 = 6666.67 rounded 6667; q = 103/109 = 0.944954; "
        "identity S_N = F0(1-q^N) exact True for N=10, 60, 200; F0 q^N rounded 3785, 223, 0 (matches lab Part A); F2 = 7072.67 "
        "rounded 7073 (quiz L01:425)."),
    row("lx1b-num-L01-lab-output", "1 lab output vs exact re-run", "L01.html:244-281 (expected block)", P,
        f"{O}/rederive_numbers_r18.out re-runs Parts B and C in exact arithmetic with the same seed and rounding: every wedge, "
        "fundamental, price and gap line equals the expected block; 9 of 13 above (3%), 13 of 13 (1%); largest gap 2175 at t = 9."),
    row("lx1b-num-L01-prose", "1 numbers in prose (L01 counts, percentages, thresholds)", "L01.html:282, :363, :367, :370-371, :378, :400", P,
        "9 of 13 and 13 of 13 (re-run); 9/13 = 0.6923 (4 dp); 13-9 = 4; 2175/8698 = 25.0057% -> 25.01 printed, exact gap 0.25 x "
        "8698.487892 -> 25.00%; fundamental at t=9 8698.487892 -> 8698 and 8698.49 to two places (page). g* = 0.09 - 400/6000 = "
        "0.023333 -> 2.33% and 2.3333%."),
    row("lx1b-num-L01-witness", "1 numbers in prose (Proposition 2.2 witness; misconception 1)", "L01.html:114, :120, :321, :462", P,
        "F0(1%) = 400/0.08 = 5000; F0(3%) = 20000/3 = 6666.67; gap at 6000 = +1000 under 1% and -2000/3 = -666.67 under 3% "
        "(rederive_numbers_r18.out L01 block)."),
    row("lx1b-num-L01-s5-example", "1 numbers in prose (Section 5 and misconception 2)", "L01.html:310, :322; quiz L01:417-421", P,
        "400/1.09 = 366.97 -> 367 cents; 40000/109 = 366.97; formula at g=3% gives 6667 (rederive_numbers_r18.out)."),
    row("lx1b-num-L03-depth", "1 numbers in prose (L03 depths, ratio, difference)", "L03.html:149, :362-363, :383, :491, :496-498, :545-546, :577, :596", P,
        f"{O}/rederive_numbers_r18.out L03 block: depth X 9.204597 -> 9.20; depth Y 2.686713 -> 2.69 (E1 exact 2.6867); X-Y 6.517884 -> "
        "6.52 (Part B and E2); printed 9.20 - 2.69 = 6.51 (E2 wording correct); ratio X/Y 3.425970 -> 3.4260 (Part D, Key row 546, quiz)."),
    row("lx1b-num-L03-path", "1 numbers in prose (L03 path table, leverage, premium)", "L03.html:331-357 (expected block)", P,
        "Expected block equals twin stdout. Re-derived: V_4 = 1084165.7847, index 0.9224, leverage 0.2769, premium 0.0269; "
        "V_12 = 1274345.2124 -> 1274345, leverage 0.3420, premium 0.0920. Y flat from t=4 (index 0.9224 for t=4..12)."),
    row("lx1b-num-L03-M-E-Q", "1 derived numbers (L03 M1-M3, E1-E3, quiz)", "L03.html:441, :448, :455, :491, :498, :505, :610", P,
        "P4 = 5764801/6250000 = 0.92236816 exact; V4 = 1084165.7847 -> 1084166 (M1); K4 = 3915834.2153 -> 3915834, and "
        "the rounded-first route also gives 3915834 (M2); L4 = 0.2768671 -> 0.2769, rounded-first 0.2768672 (M3); E3: index "
        "unchanged for t=5..12, 8 periods; quiz V_12 1274345.2124 (rederive out)."),
    row("lx1b-num-L04-stats", "1 numbers in prose (L04 lab output and key results)", "L04.html:306-322 (expected), :323, :476-477", P,
        f"{O}/rederive_numbers_r18.out L04 block: window one n=668, sd 0.0279353 -> 0.027935; window two n=321, sd 0.0246995 -> 0.024700; "
        "difference -0.0032358 -> -0.003236; ratio 0.8841688 -> 0.8842; largest |change| window one 0.1358457 at 1985-03, window two "
        "0.0965747 at 2008-10 (signed -0.096575); zero months 1976-07, 2012-07, 2019-11 (3; 665 nonzero). Expected block equals twin stdout."),
    row("lx1b-num-L04-display-diff", "1 numbers vs displayed digits (L04 difference and rounding statement)", "L04.html:323; key row :476", P,
        "Subtracting the printed sds 0.024700 - 0.027935 = -0.003235 (page says so at L04:323); the unrounded difference prints "
        "-0.003236 (lab line 321). The page states the difference is computed from unrounded values. Correct."),
    row("lx1b-num-L04-derived", "1 numbers derived on the page (M1-M3, E2, R2, quiz)", "L04.html:354, :373, :380, :387, :430, :455, :541, :564", P,
        "ln 1.1 = 0.0953101798 -> 0.095310; 0.1 - ln 1.1 = 0.0046898 -> 0.004690; M2 mean 0.006667, SSD 19/15000, sd sqrt(19/30000) "
        "= 0.025166; M3 26x12+9 = 321; E2 exp(-0.0965747399762) - 1 = -0.092057965 -> -0.092058; R2 h = tanh(z/2) = "
        "0.067818575 -> 0.067819 (6 dp) and 0.0678 (4 dp); bound ln(1.0678/0.9322) = 0.135808352 -> 0.135808 and 0.1358 (quiz); "
        "0.135846 - 0.135808 = 0.000037 so h = 0.0678 does not reach the largest move, as R2 states."),
    row("lx1b-scope-start", "5 scope of the window-start convention", "L04.html:110, :326, :387, :462; card LX1-c063", P,
        "Window two start is 2000-01 (twin WINDOW_TWO_FROM); its first change uses 1999-12 (dict(rows)['1999-12'] = 323/200 in "
        "rederive out); the reason given (fx_daily and ust_daily start 2000-01-03, MANIFEST) is verified. R3 says the start is "
        "a convention and that a sensitivity check is needed; the lab computes one start only (L04:335)."),

    # ---- mathematics and grades
    row("lx1b-math-L01", "2.4 mathematics (L01 Assumption 1.1, Definition 1.2, Theorem 1.3, Proposition 1.4 and proofs)",
        "L01.html:57-99", P,
        "Re-derived: d_{t+k}/(1+r)^k = d1(1+g)^t/(1+r) q^{k-1}; 1-q = (r-g)/(1+r) > 0; S_N(t) = F_t(1-q^N) exact; q in (0,1) under "
        "A0; q >= 1 under g >= r gives terms >= d1/(1+r) (Proposition 1.4 proof). Hypotheses stated (A0, A1, A2). "
        "Two wording defects in this section are separate FAIL rows (L01.html:99 and :323)."),
    row("lx1b-math-L01-prop22", "2.4 mathematics (L01 Proposition 2.2 and witness)", "L01.html:108-121", P,
        "Hypotheses (A3), (A4) stated; proof: r-g > r-g' > 0 gives d1/(r-g) < d1/(r-g'); A0 - F0(g) > 0 and A0 - F0(g') <= 0; "
        "witness numbers in rederive out."),
    row("lx1b-math-L03", "2.4 mathematics (L03 Lemma 3.1, Proposition 3.2, Corollaries 3.3 and 3.4)", "L03.html:94-143", P,
        "Lemma 3.1 algebra: y(C-x) - x(C-y) = C(y-x), positive for D<=x<y<C; V_m < C gives K_t > 0; Prop 3.2(a) monotone V_t; "
        "(b) closed form equals max f_t (lambda increasing); (c) first maximiser at t=m; Corollary 3.3 and 3.4 follow; "
        "no hypothesis missing (Assumption 1.2 inequality used where needed)."),
    row("lx1b-math-L04", "2.4 mathematics (L04 Definition 1.1, Proposition 1.2, Remark 1.3, Definition 2.1, Proposition 2.2)",
        "L04.html:57-107", P,
        "Telescoping by induction and by cancellation (Proposition 1.2 proof) correct; Proposition 2.2 proof uses (A2) and ln 1 = 0; "
        "n >= 2 needed for n-1 >= 1 (stated). Remark 1.3 tolerance matches SUM_TOLERANCE = 1e-12 in the twin."),
    row("lx1b-math-problems", "2.4 worked problems (every solution)", "L01.html:330-389; L03.html:431-532; L04.html:363-466", P,
        "Every solution re-derived: L01 Mechanics 1-3 (4167, 4687, 20000/21), Proof 1-3 (monotonicity, benchmark recursion, ratio "
        "at g>r), Empirical 1-3 (0.6923, 4, 25.01/25.00), Research 1-3 (g*=0.023333); L03 M1-M3, P1-P3, E1-E3, R1-R3 (R2 proof "
        "uses Proposition 3.2(a) and strict monotonicity of G); L04 M1-M3, P1-P3, E1-E3, R1-R3 (P2 bound, P3 inequality, R2 tanh "
        "identity). One wording gap in L04 R1 (undefined s_1, s_2) is a note, not a row."),
    row("lx1b-grades", "2.3 grades (claim spans and key results)", "L01.html:396-400; L03.html:542-546; L04.html:474-477", P,
        "Theorems and corollaries graded T with their proofs on the page; computed lab outputs graded C with the lab named (L01:400, "
        "L03:545-546, L04:476-477); the Lab-1 count and dispersion rows are C with basis; the definitions carry no grade."),
    row("lx1b-notation", "2.4 notation (vs notation/notation.json; local symbols defined on first use)",
        "L01.html; L03.html; L04.html; cards.json (L01, L03, L04); twins", P,
        f"{O}/math_inventory_r18.out: no registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{{e\\ast}}, R_f, \\mathbb{{Q}}, "
        "\\E) appears in any math span of the three pages; no \\R; the \\ast in F^\\ast (L01:83) is the local fundamental-value symbol, "
        "not R^\\ast. Local symbols: L01 d_s (:59), g, r (:57), F_t (:65), A_t and B_t (:105), S_N(t) (:67); L03 delta, H, m (:58), "
        "P_t (:58, P_0=1), D, V_t, K_t (:66), phi, beta, psi_t, f_t, L_t (:72), lambda, C (:96), G (R2 :521); L04 x_t, ell_t, n, s "
        "(:59), xbar (:85), h (P2 :403), z (R2 :455). Each is defined on its first use."),
    row("lx1b-notation-P", "2.4 notation: P_t is the price level of L02, L03, project; L01 observed price is A_t (ruling 16)",
        "L01.html (whole page); L03.html:58-59, :116, :157-163; L02.html:77", P,
        f"grep for P_ and \\(P in L01.html: no match (round-17 FAIL resolved: L01:114, :119, :120, :377 now use A_0). "
        "L01 observed price is A_t (:105, :143, :450). L03 P_t price index with P_0 = 1 (:58), same meaning as L02 P_t (L02:77)."),
    row("lx1b-notation-A", "2.4 notation A_t (L01 observed price)", "L01.html:105, :114, :119-120, :143-144, :377, :450; cards LX1-c006, c007", P,
        "A_t is the observed price in every use; A_0 is used for the price at date 0 in Proposition 2.2; no conflict with (A0)-(A4) labels, "
        "which are assumption labels."),
    row("lx1b-notation-K", "2.4 notation K_t (net worth, L03)", "L03.html:65 (first use, Assumption 1.2) to :605; cards c027, c071, c082", P,
        "K_t = K_0 - (V_t - V_0) everywhere; consistent with the twin (line 166 docstring); no other meaning on the three pages."),
    row("lx1b-notation-P-L03", "2.4 notation P_t in L03 (price index, P_0 = 1)", "L03.html:58-59, :116, :157-163, :211, :464-473", P,
        "P_t = (1-delta)^min(t,m), P_0 = 1; the twin defines price_index with P_0 = 1; L04 uses no P symbol."),
    row("lx1b-notation-N", "2.4 notation (N is a local symbol, defined on first use)", "L01.html:67, :74, :82-83, :87; L04", P,
        "N is the partial-sum bound (Definition 1.2 at L01:67); the registry says N is local (notation.json 'about'); no other meaning on the pages."),
    row("lx1b-notation-registered", "2.4 registered macros (R, expectation, other macros)", "L01/L03/L04 math spans; macros in notation.json",
        P, "Macro inventory (math_inventory_r18.out): none of \\E, \\Prob, \\Var, \\Cov, \\Corr, \\N, \\indic, \\Normal, \\SR appears in the "
        "three pages; the real line is not written (no \\R); \\ell, \\bar, \\lambda, \\varphi are plain Greek letters, local per notation.json."),

    # ---- DAG, definitions, prose, structure
    row("lx1b-dag-links", "2.9 DAG links (linked uses precede definitions)",
        "L01.html:37; L03.html:37, :54, :90; L04.html:37-38, :105", P,
        "L01 links to concepts.html anchors of M1 (growing-perpetuity, present-value, geometric-series, exponential-and-logarithm: in the "
        "closure). L03 links L02#def-debt-deflation and L02#def-gold-standard (earlier lesson). L04 links concepts.html#"
        "exponential-and-logarithm, L02#def-gold-standard, L03#def-lender-of-last-resort, and its own #def-bretton-woods-system. "
        "check_dag PASS."),
    row("lx1b-dag-outside-closure", "2.9 DAG outside closure (named, not linked)", "L03.html:390, :402, :413-418; L04.html:336", P,
        "Out-of-closure names found by grep on the three pages and cards: 'central bank' (defined in plain dfn at L03:390, no "
        "data-concept, the page's own choice), 'bailout' (L03:402), 'bank failure' (L03:413, :418). None of D1-D15 of the plan "
        "(bank-run, fire-sale, leverage-cycle, covered/uncovered interest parity, efficient markets, moral hazard, fisher, credit-default "
        "swap, term spread, expectation, fx market structure, sovereign default) appears in the three pages or the cards "
        f"(grep saved in {O}/outside_closure_grep_r18.out)."),
    row("lx1b-concepts-defs", "2.9 definitions once and linked (concepts)", "L01.html:105, :289; L03.html:87, :390; L04.html:86; course/concepts.html:631-636", P,
        "Each LX1 concept has one data-concept dfn: speculative-bubble (L01:105), financial-panic (L01:289), credit-channel-depression "
        "(L03:87), lender-of-last-resort (L03:390), bretton-woods-system (L04:86, pending per ruling 14). check_dag PASS."),
    row("lx1b-concept-index-title", "2.9 concept index entries for LX1 concepts", "course/concepts.html:631-636", P,
        "Seven LX1 entries link to the dfn ids on L01-L04 (e.g. :631 #def-bretton-woods-system, :635 #def-lender-of-last-resort). "
        "The Bretton Woods entry reads 'defined here' although its definition is pending (ruling 14); this is generated text from "
        "tools/build_site.py and is a registry-flag note, not a page defect."),
    row("lx1b-L04-bretton-definition", "2.9 honest pending definition (ruling 14)", "L04.html:38, :86, :337, :358, :553-557", P,
        "Definition is labelled 'definition pending'; the page states that the fixed-exchange-rate model is not a definition of the "
        "historical system; the Bretton Woods arrangement's dates, participants and end are not stated (L04:337). No registry record "
        "mentions Bretton Woods (references.json search). Matches ruling 14 and the open items."),
    row("lx1b-banned-phrases", "2.9 banned phrases (BUILDER_RULES 1.3-1.4)", "L01.html; L03.html; L04.html; cards (L01, L03, L04)", P,
        f"{O}/prose_scan_r18.out (python -I prose scan): no TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', "
        "'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', "
        "'obviously', 'clearly'; ellipsis outside code = 0 in all three pages."),
    row("lx1b-process-words", "2.9 no process words in learner text", "L01.html; L03.html; L04.html; cards", P,
        "Scan for build, builder, round (as process), verifier, REQUESTS, unit report, plan, architect, ruling, fixer in prose and cards: "
        "no match (only 'rounds' and 'unrounded' as arithmetic, and 'as Section 3 states'). Twin comments and docstrings are clean."),
    row("lx1b-scope-words", "2.4 scope words (every, all, always, never, any, only, exactly, same, drives)",
        "L01.html; L03.html; L04.html (hits listed in prose_scan_r18.out)", P,
        "Every hit read in context: each 'every'/'any'/'all'/'exactly'/'only' sits on a proof, a finite computation, a stated "
        "hypothesis, or a negative statement about the lesson's own scope (e.g. L01:303-304, L04:333-337). The two universal claims "
        "that lack a hypothesis are separate FAIL rows (L01:99 and L01:323)."),
    row("lx1b-structure", "2.9 structure (BUILDER_RULES 4.2 template and minimum counts)",
        "L01 sections 1-10; L03 sections 1-10; L04 sections 1-9", P,
        "L01: sections 1-10 (lines 53, 101, 285, 302, 306, 318, 327, 391, 405, 485); 3 misconceptions, 4 problem tiers of 3, 10 quiz "
        "items, key-results table. L03: 1-10; 4 misconceptions; 3+ per tier; 11 quiz items. L04: 1-9; 4 misconceptions; 3+ per tier; "
        "11 quiz items. Lab sections with SIMULATED or real-data labels present."),
    row("lx1b-quiz-explanations", "2.9 quiz explanations vs lesson and output", "L01.html:405-483; L03.html:552-636; L04.html:483-567", P,
        "Each explanation read against its lesson and the printed output: L01 explanations match Theorem 1.3, Proposition 1.4, "
        "Definition 2.1 and Proposition 2.2 values; L03 explanations match Corollary 3.3, 3.4 and the printed 2.69, 9.20, 3.4260, "
        "1274345; L04 explanations match the 668/3/321 counts, 0.027935, 0.095310 and 0.135808."),
    row("lx1b-L03-remark42-solvency", "2.4 Remark 4.2 vs Assumption 1.2 and Proposition 3.2(a)", "L03.html:64-67, :395", P,
        "Assumption 1.2 states the inequality and says it keeps K_t > 0 (:67); Proposition 3.2(a) gives V_t <= V_m; so K_t > 0 in every "
        "period (:395). Consistent. Round-17 wording note on :395 is not a defect (Assumption 1.2 says the same at :67)."),
    row("lx1b-L03-ratio-claims", "7 causal and ratio claims (L03)", "L03.html:404; :516; :523", P,
        "Square-premium variant: depth = beta phi times the square of the Corollary 3.4 bracket, so the ratio is the square of the "
        "Corollary 3.4 ratio; equal to it only when the ratio is 0 or 1 (never, since depth(12) > depth(4) > 0); slope cancels. "
        "R2 proof: the largest real debt is V_m at t = m (Proposition 3.2(a)); strict G gives G(V_m') < G(V_m). Both checked."),
    row("lx1b-L03-r1-no-result", "2.4 Research problem R1 claims no result", "L03.html:516", P,
        "R1 describes the change and the assumption it replaces and states no numerical result; consistent with Remark 4.2."),
    row("lx1b-L03-lab-checks-overreach", "2.5 interpretation does not overreach (L03 lab)", "L03.html:145, :383; twin Parts B-D (lines 172-175)", P,
        "Interpretation says the printed depths are the model's values and no output series enters the lab (:383); Part C prints "
        "the two adjacent-duration checks; Part D makes no equality test (twin lines 320-323). No claim about any economy."),
    row("lx1b-L03-misconception-scope", "2.4 misconceptions match the proofs (L03)", "L03.html:413-426; proof :128-131 (Corollary 3.3)", P,
        "Misconception 1 (bank failure) and 2 (holding parity) are answered by Assumptions 1.1-1.3 and the proof of Corollary 3.3, "
        "which uses only the durations, the closed form, V_m < K_0 + D, Lemma 3.1 and Prop 3.2(b). Misconception 4 (9.20 is SIMULATED) matches the lab."),
    row("lx1b-L04-A2-before-defined", "2.9 terms used before definition (L04)", "L04.html:66, :84-92, :400-405, :450-457", P,
        "(A1) is stated inline in Proposition 1.2 (:66); (A2) in Definition 2.1 (:85) precedes Proposition 2.2 (:89); (A3) first appears in "
        "Problem P2 (:403) with its full statement; 'dispersion' is first used at :51 with a forward pointer to Definition 1.1, which is defined at :59."),
    row("lx1b-L04-keyresults-locator", "2.3 key results locators (L04)", "L04.html:474-477", P,
        "Each key-results row names a locator (Proposition 2.2 and Proposition 1.2 in the text; Lab 1 Parts B-D for the counts)."),
    row("lx1b-L04-prediction-tested", "2.5 lab hypothesis matches code and output (L04)", "L04.html:114; twin Parts A and C; expected 307-322", P,
        "Hypothesis: Part A all exactly zero True, sd 0.000000 (expected lines 307-308: 'all exactly zero: True', 'sample standard "
        "deviation: 0.000000'); prediction of nonzero recorded dispersion in both windows is printed (321-322 and 317, 314); the lab does "
        "not assert it (twin docstring 140-143)."),
    row("lx1b-L03-forward-definition-refs", "2.9 terms used before definition (L03; forward pointers)", "L03.html:51, :54, :72, :82", P,
        "Forward uses name the definition: leverage and premium at :72 cite Definition 2.1 (which defines them at :82); lender of last "
        "resort at :51 cites Definition 4.1 (:389); 'Sections 2 and 4 give definitions' (:54)."),
    row("lx1b-cards-l01-l03-l04", "2.7 retrieval cards (all L01, L03, L04 cards read; duplicates)",
        f"course/modules/LX/LX1/cards.json; {O}/cards_check_r18.out", P,
        "All 71 cards for L01 (15), L03 (32) and L04 (24) read in full; ids unique across the 88-card file; graded cards carry a basis "
        "(cards_check_r18.out). No duplicate content; each card matches its lesson's text, numbers and hypotheses."),
    row("lx1b-cards-c052-c053", "2.7 card vs lesson text (c052, c053)", "cards.json LX1-c052, LX1-c053 vs L04.html:84-92", P,
        "c052 gives (A2), window of at least two changes, zero changes and zero dispersion (matches Proposition 2.2 at :89-94); c053 "
        "lists anchor currency, one foreign currency, fixed rate, market rate (matches Definition 2.1 at :85)."),
    row("lx1b-cards-L01-hypotheses", "2.7 cards carry the proposition's hypotheses (L01)", "cards.json LX1-c002..c007, c013, c085, c086", P,
        "Theorem 1.3 cards state A0 and A1; Proposition 1.4 card states (A1) d1>0, 1+g>0 and (A2) r>-1, g>=r; Proposition 2.2 card "
        "states (A3), (A4); c085 (F_t = (1+g)F_{t-1}) matches Problem Proof 2 and holds without the d1 != 0 caveat the problem uses."),
    row("lx1b-cards-L03-hypotheses", "2.7 cards carry the proposition's hypotheses (L03)", "cards.json LX1-c030..c036, c079, c082, c087", P,
        "Lemma 3.1, Proposition 3.2(a)-(c), Corollaries 3.3 and 3.4 cards state Assumptions 1.1-1.3 (and 1.2 where needed) and the "
        "parity ranges (0 <= m' < m <= H; 1 <= m' < m <= H), matching the page."),
    row("lx1b-delta-hunks", "delta since round-17 pin (700bf33f..50559266), slice b paths",
        "L01.html; cards.json; L03.html; L04.html; tests/labs/LX1/*", P,
        "`git diff 700bf33f 50559266 -- course/modules/LX/LX1 tests/labs/LX1`: L01.html, 7 hunks read in full: :60 ('simple convention' "
        "removed), :114 and :119-120 and :377 (P_0 -> A_0, ruling 16), :313 (Section 5 bullet 4 wording), :321 (misconception 1 "
        "wording). cards.json: changed LX1-c037, c038 (first-reached wording removed), c085 and c086 (new fronts/backs), c089 (L04, "
        "largest move in window one); added LX1-c090, c091. L03.html, L04.html and all LX1 slice-b twins are byte-identical to 700bf33f "
        "(empty diff). The project.html and project-3 twin hunks belong to other slices."),
    row("lx1b-plan-coverage", "2.9 plan coverage (LX1 plan section 3 for L01, L03, L04; section 2.1 rules)",
        "plans/LX1-build-plan.md sections 2.1, 3; plans/FINAL-ARCHITECT-RULINGS.md 14, 16", P,
        "L01 covers the closed form under (A0)/(A1), the bubble as a gap with a stated benchmark, panic by mechanism, Garber at book "
        "level with title only (plan 3 L01). L03 teaches the credit channel as a model with no empirical citation (B2) and defines the "
        "lender of last resort (plan 3 L03). L04 covers the telescoping identity, the two windows, and no end date (B3, plan 3 L04). "
        "Rulings 14 and 16 are applied."),
    row("lx1b-hours", "2.9 hours arithmetic (lesson split and hub)", "L01.html:34; L03.html:34; L04.html:34; index.html:29",
        P, "Hub data-hours-lessons=40 and data-hours-project=10 (index.html:29); lessons 10 h each (L01 :2, L03 :2, L04 :2 and eyebrows "
        "at :34). 4 x 10 = 40, 40 + 10 = 50. Hours are design targets (ruling)."),
    row("lx1b-L03-honest-pending-source", "2.8 honest-pending statement vs open items (L03)", "L03.html:76; plans/LX1-open-items.md D-1", P,
        "The page's note says no redistributable historical series is embedded and the lab stays SIMULATED; open-items D-1 records the "
        "request. Consistent."),
    row("lx1b-L04-spot-only", "2.8 dataset description matches the register note", "L04.html:333-334; tools/data_sources.yaml fx_monthly note (62-64)", P,
        "Register note: 'Each value is the last noon rate of its month ... Spot rates only'; L04:333-334 state spot-only and "
        "monthly last value, not the monthly average, as the register note says."),
    row("lx1b-L04-twin-docstring-float", "2.5 twin docstring vs code (floats and rounding)", "tests/labs/LX1/lab-LX1-L04-1.py docstring 135-136; log_changes; show", P,
        "Docstring: exact ratio converted once to float then ln; printed values half away from zero of the exact binary value. Code: "
        "float(rate / previous) then math.log; show() = Decimal(value).quantize(..., ROUND_HALF_UP). Matches."),
    row("lx1b-L03-partD-label", "2.5 lab label vs page (Part D)", "L03.html:145, :149, :383; twin lines 320-323", P,
        "Part D prints three ratios and makes no equality test (twin code lines 320-323); the page says the same; the printed ratios are equal."),
    row("lx1b-L03-line121-lab-formula", "2.4 page claim about what the lab computes (L03 closed form)", "L03.html:121; twin depth() lines 258-260", P,
        "The twin computes depth as max over depth_path (no closed form); page line 121 says the lab does not evaluate part (b). Correct."),
    row("lx1b-L03-why-ordering", "2.5 interpretation (L03 ordering)", "L03.html:51; twin docstring 152-155", P,
        "The ordering follows from the stated assumptions and parity durations (twin docstring; page :51). No historical claim."),
    row("lx1b-notation-check-math-spans", "2.4 notation scan of math spans (L01 local symbols)", "L01.html math spans", P,
        f"{O}/math_inventory_r18.out lists the macros used per page; no macro outside the registered set or the standard operators is "
        "used with another meaning."),
    row("lx1b-mutants-none", "2.6 mutation (rubric unit; no grader; lab twins are demonstrations)", "tests/labs/LX1/*; ruling on lab mutants", P,
        "No grader exists (run_graders: 'no autograder'), so no mutant rows apply to slice b. Lab twins are demonstrations; a mutated "
        "lab exiting 0 is not a finding unless a lesson sentence claims the lab checks that property (fixer rules). Recorded: mutants []."),

    # ---- FAIL rows (2)
    row("lx1b-L01-misc3-closed-form", "2.4 mathematics: misconception statement (L01 Section 6, misconception 3)",
        "course/modules/LX/LX1/L01.html:323", F,
        "Sentence: 'The closed form is not a finite value in that case.' (case: g >= r, d1 > 0). The closed form d1/(r - g) is "
        "not a finite present value there, but it is a finite number for g > r: e.g. d1 = 400, r = 9%, g = 10%, "
        "400/(0.09 - 0.10) = -40000 (exact Fraction arithmetic). It is undefined at g = r. What fails for "
        "g >= r is the series (Proposition 1.4: the partial sums tend to +infinity), not the formula's finiteness. The claim as "
        "written is false for g > r.",
        "Replace the sentence at L01.html:323 with: 'The series has no finite sum, so the closed form of Theorem 1.3 gives no present "
        "value: it is undefined at g = r, and for g > r it returns a negative number that is not the present value of the dividends.'"),
    row("lx1b-L01-benchmark-finite-hypothesis", "2.4 hypothesis of a universal claim (L01 Section 5 intro paragraph)",
        "course/modules/LX/LX1/L01.html:99", F,
        "Sentence: 'A benchmark that depends on a growth rate at or above the discount rate is not a finite present value, and this "
        "lesson does not use one.' The claim needs d1 > 0 (Proposition 1.4 assumes it). With d1 = 0 the dividend stream is identically 0, "
        "its present value is 0 (finite) for every g, so the sentence is false for d1 = 0. The Section 5 bullet at :312 states the "
        "hypothesis correctly; this sentence does not.",
        "Insert the hypothesis: at L01.html:99 change to 'With d1 > 0, a benchmark that depends on a growth rate at or above the "
        "discount rate is not a finite present value, and this lesson does not use one.'"),
]

fragment = {
    "unit": "LX1",
    "slice": "b",
    "round": 18,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-b (L01, L03, L04 and lab twins), round 18",
    "pin": "50559266 (505592668894eff518befad086df192000dc86c0), detached; .venv symlinked; vendor copied",
    "base": "700bf33f334486d7b5b4f22d4f82f3e25d4b39b6 (round-17 pin). Delta read: course/modules/LX/LX1/L01.html, cards.json; L03.html, L04.html and all slice-b twins byte-identical to 700bf33f",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE18-LX1-b",
    "scratch": "/tmp/lx1b-r18-rebuild (fx_monthly rebuild from live feed); /tmp/lx1b-r18-twin-* and /tmp/lx1b-r18-fail-* (removed after each run)",
    "verified_at": "2026-11-09T05:10:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "B2: Bernanke (1983) AER 73(3) credit-channel source (curriculum yaml:38) not in the registry; review_queue.json:1610 candidate is an NBER working paper and must not be admitted as the AER article.",
        "N1: Kindleberger & Aliber (2015) not in the registry (review_queue.json:1557).",
        "N2: friedman1963monetary registry record lists 'Friedman, Milton' only; curriculum string names Friedman & Schwartz (yaml:37). Pages cite the key only.",
        "B3: no registry record mentions Bretton Woods (references/references.json search, zero hits); L04 definition and any end date stay pending (ruling 14).",
        "Generated text: course/concepts.html:631 says 'defined here' for Bretton Woods system, whose definition is pending (ruling 14). Generated by tools/build_site.py; not edited here.",
        "Generated text: course/concepts.html:635 titles the credit-channel concept 'Nonmonetary (credit) channel of the Great Depression', the curriculum's name; the L03 page does not use that title."
    ],
    "freshness_flags": [],
    "notes": [
        "Pin 50559266 checked out detached; .venv symlinked; no course, tool, test, reference, curriculum or market file edited; no commit or push. The only files written are under ledgers/LX1/scripts/LX1-b-r18/ and this fragment.",
        "Full read this round: L01.html (all 500 lines), L03.html (all 653 lines), L04.html (all 586 lines), the three twins (L01 111 lines, L03 177, L04 191), the 71 L01/L03/L04 cards (cards_check_r18.out), plans/LX1-build-plan.md (all), plans/LX1-open-items.md, plans/FINAL-ARCHITECT-RULINGS.md (rulings 13-16 read in full, the rest by heading), ~/.fanout/fixer-rules.md, plans/LX1 section 0-13 read in full.",
        "Previous round's PASS rows were not carried. Every row above was re-derived this round (the task said not to trust them). Round-17 FAIL row lx1b-notation-P is re-verified PASS: L01 now uses A_t and A_0 (ruling 16).",
        "Two FAIL rows (lx1b-L01-misc3-closed-form, lx1b-L01-benchmark-finite-hypothesis) are wording/hypothesis defects of the kind the rules name (universal claims without the hypothesis; numbers and claims checked by re-derivation). All numbers and proofs otherwise re-derived and PASS.",
        "Non-blocking wording (not rows): (i) L03.html:383 says the ratio is the same 'as Corollary 3.4 requires'; the corollary implies the equality rather than requiring the printed output, so 'as Corollary 3.4 implies' is the exact verb. (ii) L04.html R1 solution (:448) uses s_1 and s_2 for the window dispersions without defining them (Definition 1.1 defines one s per window); a one-clause definition would close it. (iii) L01 Section 5 bullet 6 names no counter-account for the bubble debate (plan 2.2 two-sided rule); the page defers to the reading list and says it has not read it, which satisfies the rule as the plan states it.",
        "Hub and project not in this slice; hub hours arithmetic checked only (index.html:29).",
        "Twins: run alone with CPython 3.14.8 via .venv (-I -W error) in empty scratch directories; L04 with data/fx_monthly.csv copied in, as its data-files attribute states.",
        "Live verify_refs run (4 LX1 entries) executed with the repo tool; plain curl used for the Federal Reserve licence page and found the quoted text at HTTP 200. No access block was encountered.",
        "Not checked: the Pyodide runtime itself beyond tools/page_smoke.py (which PASSES for L01, L03, L04); the project and cards of L02 (other slices); the hub prose beyond the hours lines; registry records beyond the four LX1 keys (verify_refs live covered them); the Crossref live-run of the whole registry (not a unit row); any historical fact (none is stated on these pages, by design).",
        "Mutants: none. LX1 is rubric-graded (no grader); lab twins are demonstrations (architect rulings; fixer rules). Recorded as mutants [] on purpose."
    ],
    "summary": (
        "LX1-b round 18 on 50559266 (base 700bf33f): verdict FAIL. Rows: "
        f"{len(rows)} (pass={sum(1 for r in rows if r['status'] == P)} fail={sum(1 for r in rows if r['status'] == F)} unverifiable=0). "
        "Non-PASS: lx1b-L01-misc3-closed-form (L01.html:323: 'the closed form is not a finite value' is false for g > r, e.g. 400/(0.09-0.10) = -40000); "
        "lx1b-L01-benchmark-finite-hypothesis (L01.html:99: universal claim without d1 > 0, false for d1 = 0). The round-17 FAIL lx1b-notation-P is resolved. "
        "All numbers re-derived and matching (exact Fractions and Decimal); both lab twins and the L04 twin alone pass; the fx_monthly snapshot rebuilds byte-for-byte from the live feed; the licence quote is found by plain curl. Mutants: none (rubric unit)."
    ),
}

out = pathlib.Path("ledgers/LX1/LX1-b.json")
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows))
