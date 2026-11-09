"""LX1-b round 15: writes ledgers/LX1/LX1-b.json from the evidence in ledgers/LX1/scripts/LX1-b-r15/ (no network).

Run: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r15/write_fragment_r15.py <checkout>
"""

import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
S = "ledgers/LX1/scripts/LX1-b-r15"
CARRY = "Carried from round 14 ({files} byte-identical since the previous pin): "

R = []


def row(rid, check, location, status, evidence, fix=""):
    R.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


# ---- gates (run this round, outputs in out/)
row("lx1b-check-pages", "2.9 structure (tool gate)", "course/modules/LX/LX1/L03.html; L04.html", "PASS",
    f"tools/check_pages.py --unit LX1 -> 'check_pages LX1: PASS', exit 0 ({S}/out/check_pages.out).")
row("lx1b-check-dag", "2.9 DAG (tool gate)", "course/modules/LX/LX1/L03.html; L04.html", "PASS",
    f"tools/check_dag.py --unit LX1 -> 'check_dag LX1: PASS', exit 0 ({S}/out/check_dag.out). Link targets: lx1b-dag-links.")
row("lx1b-check-projects", "2.6 project gate (unit only)", "course/modules/LX/LX1/project.html", "PASS",
    f"tools/check_projects.py --unit LX1 -> 'check_projects LX1: PASS', exit 0 ({S}/out/check_projects.out). The project is not in this slice.")
row("lx1b-run-graders", "2.6 grader (rubric unit)", "tools/run_graders.py --unit LX1", "PASS",
    f"'run_graders LX1: no autograder (grading: rubric)', exit 0 ({S}/out/run_graders.out). No grader or mutant applies to LX1 (curriculum grading: rubric).")
row("lx1b-dag-links", "2.9 DAG links", "L03.html (L02.html#def-debt-deflation, #def-gold-standard); L04.html (../../../concepts.html#exponential-and-logarithm, L02.html#def-gold-standard, L03.html#def-lender-of-last-resort)", "PASS",
    "grep of id attributes: L02.html has id=\"def-debt-deflation\" and id=\"def-gold-standard\"; L03.html has id=\"def-lender-of-last-resort\" (1 match); course/concepts.html has id=\"exponential-and-logarithm\" (1 match). All link targets exist; check_dag PASS.")
row("lx1b-dag-outside-closure", "2.9 DAG outside closure", "L03.html; L04.html", "PASS",
    f"{S}/scans_r15.py section 3 (outside-closure names in prose): L03 hits 'bailout' (L03.html, Section 5 canon breaks) and 'bank failure' (Misconception 1, Section 6), both plain prose with no link and no data-concept; L04 none. Central bank is a plain dfn (L03.html:390, no data-concept). Concepts D1-D15 of plan section 4 are not linked. Output: {S}/out/scans_r15.out.")
row("lx1b-run-labs", "2.5 labs (tool gate)", "tests/labs/LX1/lab-LX1-L03-1.py; lab-LX1-L04-1.py (and the other LX1 twins)", "PASS",
    f"tools/run_labs.py --unit LX1 -> 'run_labs LX1: PASS (7/7)', exit 0 ({S}/out/run_labs.out).")
row("lx1b-twin-alone-L03", "2.5 labs (alone)", "tests/labs/LX1/lab-LX1-L03-1.py", "PASS",
    f"Copied alone to /tmp/lx1b-r15/L03; 'python -I -W error lab-LX1-L03-1.py' exit 0; stderr empty ({S}/out/twin_L03.err, twin_L03.out has 56 lines).")
row("lx1b-twin-alone-L04", "2.5 labs (alone)", "tests/labs/LX1/lab-LX1-L04-1.py", "PASS",
    f"Copied alone with data/fx_monthly.csv to /tmp/lx1b-r15/L04/data; 'python -I -W error' exit 0; stderr empty ({S}/out/twin_L04.err).")
row("lx1b-twin-alone-L01", "2.5 labs (alone; the L01 twin changed at this pin)", "tests/labs/LX1/lab-LX1-L01-1.py", "PASS",
    f"Copied alone to /tmp/lx1b-r15-l01; 'python -I -W error lab-LX1-L01-1.py' exit 0; stderr empty ({S}/out/twin_L01.err). The L01 prose is slice a's; only the twin run is in this slice.")
row("lx1b-twin-equals-page-code", "2.5 labs (page code = twin; expected = stdout)", "L03.html lines 150-326 (code), 327-382 (expected); L04.html lines 115-305 (code), 306-322 (expected)", "PASS",
    f"{S}/compare_r15.py ({S}/out/compare_r15.out): the L03, L04 and L01 page data-run code equals the twin modulo the final newline (code + newline == twin: True for all three). The L03 and L04 expected blocks equal the twin's stdout when the twin is run alone: True.")
row("lx1b-page-smoke-L03", "2.9 page_smoke (L03 alone)", "course/modules/LX/LX1/L03.html", "PASS",
    f"tools/page_smoke.py --unit LX1 --pages L03 -> 'page_smoke modules/LX/LX1/L03.html: PASS', exit 0, lab 0.0 s ({S}/out/page_smoke_L03.out).")
row("lx1b-page-smoke-L04", "2.9 page_smoke (L04 alone)", "course/modules/LX/LX1/L04.html", "PASS",
    f"tools/page_smoke.py --unit LX1 --pages L04 -> 'page_smoke modules/LX/LX1/L04.html: PASS', exit 0, lab 0.0 s ({S}/out/page_smoke_L04.out).")
row("lx1b-ruff-mypy", "gates (ruff, mypy)", "tests/labs/LX1/*.py", "PASS",
    f"ruff check tests/labs/LX1 -> 'All checks passed!', exit 0; ruff format --check -> '7 files already formatted', exit 0; mypy --no-incremental on the L01, L03 and L04 twins -> 'Success: no issues found in 3 source files', exit 0 ({S}/out/ruff_check.out, ruff_format.out, mypy_labs.out).")
row("lx1b-pytest", "gates (pytest)", "tests/test_labs.py; tests/test_page_checks.py (-k LX1)", "PASS",
    f"python -m pytest tests/test_labs.py tests/test_page_checks.py -q -k LX1 -> '.......', exit 0; collect-only: 'tests/test_labs.py: 7' ({S}/out/pytest_LX1.out, pytest_collect_LX1.out).")
row("lx1b-verify-refs", "2.1 citations (registry integrity)", "references/references.json", "PASS",
    f"tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0; tools/verify_refs.py --unit LX1 -> 'live re-verification of LX1: 4 of 560 entries, 0 problems', exit 0 ({S}/out/verify_refs_offline.out, verify_refs_unit_LX1.out).")
row("lx1b-citations-L03", "2.1 citations (L03)", "L03.html:405 (span data-cite), :640 (References)", "PASS",
    "Read this round: the only data-cite in L03.html is friedman1963monetary (lines 405 and 640; grep -c data-cite = 2). The text at :405 and :640 attributes no finding to the book and states that no passage has been read. Registry fields (title, Friedman, 1963) carried from round 14: " + CARRY.format(files="references/references.json and course/modules/LX/LX1/L03.html").replace("Carried from round 14 (", "").replace(") byte-identical since the previous pin): ", " byte-identical since the previous pin").strip() + ".")
row("lx1b-citations-L04", "2.1 citations (L04)", "L04.html section 9 (lines 569-575)", "PASS",
    "grep -c data-cite course/modules/LX/LX1/L04.html = 0. The References section (L04.html:571-573) cites no registry key and names the dataset by its MANIFEST entry (Board of Governors, G.5/H.10, fx_monthly, retrieved 2026-10-19). The citation string matches course/assets/data/market/MANIFEST.json fx_monthly.citation.")
row("lx1b-fetch-check", "2.8 data (offline snapshot check)", "course/assets/data/market/fx_monthly.csv; MANIFEST.json", "PASS",
    f"tools/fetch_data.py --check -> 'fetch_data: 3 datasets, 0 problems', exit 0 ({S}/out/fetch_check.out).")
row("lx1b-fx-rebuild", "2.8 reproducibility (live rebuild)", "course/assets/data/market/fx_monthly.csv; MANIFEST.json fx_monthly", "PASS",
    f"Live rebuild this round in a scratch copy: {S}/fx_rebuild_r15.sh runs tools/fetch_data.py --fetch --only fx_monthly --keep-raw (no write to the checkout). Result: built fx_monthly 669 rows, 67392 bytes, 1971-01 to 2026-09; the rebuilt CSV is byte-identical to the committed file (cmp: CSV_BYTE_IDENTICAL); sha256 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e in both. The raw download hash today is 1c312d2fc1de99f174c26178a2cb1f0f0f6a4a08b6dce25b043603fec9a3f24a versus raw_sha256 8f370f9c57b73e1c0b68a2ee72ddecd3abaffb21fa627fcfd4f8a3612798c6a8 in the MANIFEST (a provenance record of the 2026-10-19 download; not refreshed, and the snapshot rebuilds byte-for-byte, so this is not a failure). Output: {S}/out/fx_rebuild_r15.out.")
row("lx1b-fx-licence", "2.8 licence (quoted on the issuer's page)", "tools/data_sources.yaml fx_monthly (licence, licence_url); MANIFEST fx_monthly.licence_url", "PASS",
    f"Plain curl this round: {S}/licence_r15.py. https://www.federalreserve.gov/disclaimer.htm -> HTTP 200; quoted text: 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.' (grants redistribution with attribution). https://www.federalreserve.gov/releases/h10/about.htm -> HTTP 200; quotes: 'G.5 provides the monthly release and contains monthly averages of bilateral exchange rates' and 'The data are noon buying rates in New York for cable transfers' (Last Update: February 06, 2023). Output: {S}/out/licence_r15.out.")
row("lx1b-fx-guard", "2.8 data guard (blank and non-decimal cells fail loud)", "tests/labs/LX1/lab-LX1-L04-1.py parse_rate, load_column", "PASS",
    CARRY.format(files="tests/labs/LX1/lab-LX1-L04-1.py and course/assets/data/market/fx_monthly.csv") +
    "ledgers/LX1/scripts/LX1-b-r14/guard_licence_r14.sh: a scratch copy with a blank GBP cell (1979-04) exits 1 with ValueError, as the twin's parse_rate raises for a blank cell (round-14 output in ledgers/LX1/scripts/LX1-b-r14/out/guard_blank.err).")
row("lx1b-fx-gbp-clean", "2.8 data (GBP column)", "course/assets/data/market/fx_monthly.csv (GBP column)", "PASS",
    f"{S}/rederive_r15.py (csv.DictReader, Fraction): 669 rows, GBP blanks 0; month contiguity asserted for all rows. Output: {S}/out/rederive_r15.out.")
row("lx1b-honest-data", "2.8 honest data (SIMULATED vs real)", "L03.html:76, :147-152; L04.html:112-114", "PASS",
    "L03 is SIMULATED with an honest-pending note at L03.html:76 (no redistributable historical gold or output series is embedded; MANIFEST datasets are fx_daily, fx_monthly, ust_daily only). The lab title at L03.html:148 says SIMULATED. L04 reads the embedded fx_monthly.csv (real data, MANIFEST entry, retrieved 2026-10-19); Part A is labelled SIMULATED (L04.html:113).")
row("lx1b-L04-simulated-label", "2.5 labs (SIMULATED label)", "L04.html:113 (title), :114 (hypothesis); twin docstring lines 138-139; expected line 306", "PASS",
    "L04.html:113 'Lab 1 · Part A SIMULATED'; twin docstring 'Part A is a SIMULATED model check, not data'; expected block line 306 'Part A: SIMULATED model check, not data'. Parts B-D label the real column and name fx_monthly.csv.")
row("lx1b-L04-manifest-note", "2.8 data (dataset named in lab)", "L04.html:112 (data-files), :114; twin docstring lines 115-123", "PASS",
    "L04.html:112 data-files=\"fx_monthly.csv\"; the twin opens data/fx_monthly.csv (DATA_PATH). The docstring and the page state the MANIFEST transform (month-end, each column's last value in the month), the retrieval date 2026-10-19, the 669-month range and the inverted currencies (CAD, CHF, DKK, JPY, NOK, SEK): all match course/assets/data/market/MANIFEST.json fx_monthly.")
row("lx1b-open-items-missing", "2.9 open items", "plans/LX1-open-items.md", "PASS",
    CARRY.format(files="plans/LX1-open-items.md") + "the open items D-1 (L03 data request), the Bretton Woods pending definition and the reference requests are present and unchanged.")
row("lx1b-num-L03-depth", "2.2 numbers (L03 depth)", "L03.html:359-362 (expected), :383, :545, Problem E1 :491, E2 :498, quiz :577, :596, :610", "PASS",
    f"{S}/rederive_r15.py (Fraction arithmetic, no twin code): depth X = 0.0920459718 -> 9.20; depth Y = 0.0268671310 -> 2.69; difference unrounded 6.517884 -> 6.52; the difference of the printed depths 9.20 - 2.69 = 6.51 (as stated at L03.html:383 and E2 :498). Exact depth Y 2.686713 -> 2.6867 (E1 :491). V_12 = 1274345.2124 cents -> 1274345 (quiz :610). Output: {S}/out/rederive_r15.out.")
row("lx1b-num-L03-path", "2.2 numbers (L03 path table)", "L03.html:331-343 (X), :345-357 (Y)", "PASS",
    f"{S}/expected_path_r15.py recomputes all 26 rows (index to 4 dp, real debt to the cent, leverage and premium to 4 dp, output fall to 2 dp in percent) with Fraction arithmetic from Assumptions 1.1-1.3, and each row equals the page's expected line: 'economy X rows equal independent recomputation: True', 'economy Y ...: True' ({S}/out/expected_path_r15.out).")
row("lx1b-num-L04-stats", "2.2 numbers (L04 Part C and D)", "L04.html expected lines 306-322; interpretation :323; key results :476-477", "PASS",
    f"{S}/rederive_r15.py on the CSV: window one sd 0.027935277918 -> 0.027935; window two sd 0.024699501388 -> 0.024700; ratio 0.884168808 -> 0.8842; 668 window-one changes, 321 window-two changes; zeros 1976-07, 2012-07, 2019-11 (3), nonzero 665; largest |change| window one 0.135845673 at 1985-03; window two 0.096574740 at 2008-10, signed -0.096575. Telescoping identity gap 5.6e-16 (window one) and 7.8e-16 (window two) <= 1e-12. Output: {S}/out/rederive_r15.out.")
row("lx1b-num-L04-display-diff", "2.2 numbers (difference and its display)", "L04.html:323; expected line 321; misconception 2 :350", "PASS",
    "Unrounded difference s2 - s1 = -0.00323578 -> -0.003236 (printed, expected line 321 and misconception 2). The difference of the two printed figures 0.024700 - 0.027935 = -0.003235, as L04.html:323 states. Output: rederive_r15.out.")
row("lx1b-num-L04-derived", "2.2 numbers (derived on the page)", "L04.html M1 :373, M2 :380, M3 :387, E2 :430, R2 :455, misconception 3 :354, quiz :541, :564", "PASS",
    "M1: 1.375/1.25 = 1.1; ln 1.1 = 0.0953101798 -> 0.095310; simple 0.100000; difference 0.0046898 -> 0.004690. M2: mean 1/150 -> 0.006667; sum of squared deviations 19/15000 (exact); dispersion sqrt(19/30000) = 0.0251661 -> 0.025166. M3: 312 + 9 = 321. E2: exp(-0.0965747400) - 1 = -0.0920580 -> -0.092058. R2: tanh(0.13584567/2) = 0.0678186 -> 0.067819 and 0.0678 when rounded; ln(1.0678/0.9322) = 0.1358084 -> 0.135808 (quiz tolerance 0.1358). Output: rederive_r15.out.")
row("lx1b-scope-start", "2.4 scope (window two start)", "L04.html:110, :326, :335, :387, :462; card LX1-c063 (text changed at this pin)", "PASS",
    "Window one base is 1971-01 (the file's first row); window two base is 1999-12 and its first change is 2000-01 (twin lines 127-130; L04.html:326 states the base). fx_daily and ust_daily first = 2000-01-03 (MANIFEST). Card LX1-c063 (changed at this pin) says 'both begin on 2000-01-03', which matches MANIFEST and L04.html:326.")
row("lx1b-math-L03", "2.4 mathematics (L03 Lemma 3.1, Props 3.2, Cors 3.3-3.4)", "L03.html:94-143 (statements and proofs)", "PASS",
    f"Every proof read. Lemma 3.1 identity y/(C-y) - x/(C-x) = C(y-x)/((C-x)(C-y)) re-derived. Prop 3.2(a) monotone V_t with 0 < 1-delta < 1; (b) closed form equals the maximum (the rederive script shows the bracket equals depth exactly for m = 4 and 12); (c) first attainment at t = m. Cor 3.3: the chain V_m' < V_m < C gives lambda increasing. Cor 3.4: the common factor beta*phi cancels (numerically 3.425970 for all three products). Assumption 1.2 (V_m < A_0 + D) holds for m = 12 (1274345 < 5000000). Output: {S}/out/rederive_r15.out.")
row("lx1b-math-L04", "2.4 mathematics (L04 Def 1.1, Prop 1.2, Remark 1.3, Def 2.1, Prop 2.2, Remark 2.3)", "L04.html:58-107", "PASS",
    "Prop 1.2 telescoping proof read (interior terms cancel; (A1) used). Prop 2.2 (a) and (b) read: ln(1)=0 and dispersion 0 with n >= 2. Remark 1.3 tolerance 1e-12 matches SUM_TOLERANCE in the twin. Numerically the telescoping gap is ~1e-15 in both windows (rederive_r15.out).")
row("lx1b-math-problems", "2.4 mathematics (problem sets)", "L03.html:431-532 (M1-M3, P1-P3, E1-E3, R1-R3); L04.html:363-466", "PASS",
    "Every problem and worked solution read in this round. Numbers re-derived (rederive_r15.out; expected_path_r15.out). L03 M1 P_4 = 5764801/6250000 = 0.92236816 exact; V_4 = 1084165.7847 -> 1084166; A_4 = 3915834.2153 -> 3915834; L_4 = 0.2768671 -> 0.2769. L03 E3: 8 periods of unchanged index for Y (t = 5..12). L04 P2 band bound and P3 inequality re-proved. No solution contradicts its lesson.")
row("lx1b-grades", "2.3 grades", "L03.html:124, :134, :541-546 (key results); L04.html:468-477; cards", "PASS",
    "Re-graded against BLUEPRINT section 3 and ruling 13: L03 Lemma 3.1, Props 3.2 and Cors 3.3-3.4 are T with proofs on the page; the lab-printed depths 9.20 and 2.69 and the ratio 3.4260 are C naming Lab 1 (key results rows 4-5, cards LX1-c037, c038, c039, c067 all C). L04 Prop 1.2 and Prop 2.2 are T; the printed dispersions, the ratio and the zero-change months are C naming Lab 1 (key results rows 3-4; cards c054-c058, c060, c065, c068 all C). Card LX1-c084 has no grade and states no empirical claim (MANIFEST transform only).")
row("lx1b-notation", "2.4 notation (registry and local symbols)", "L03.html; L04.html; cards.json (L03, L04); twins", "PASS",
    f"{S}/scans_r15.py section 4: no registered symbol (T, Phi, gamma_3, gamma_4, R^*, R^{{e*}}, R_f, Q, E, R, Prob, Var, Cov, Corr, N) appears in TeX math of L03 or L04 or in the L03/L04 cards. The 20 'T' matches are grade badges (data-grade=\"T\" and its text), and {S}/out/T_in_math_r15.out counts 0 bare T inside TeX math. The macros used (\\ln, \\operatorname, \\bar, \\tanh, \\lambda, \\psi, \\varphi, \\beta, \\delta, \\ell) are standard LaTeX or local Greek letters.")
row("lx1b-concepts-defs", "2.9 concepts (dfn and links)", "L03.html:86, :389; L04.html:86", "PASS",
    "dfn with data-concept: L03 credit-channel-depression (L03.html:86) and lender-of-last-resort (L03.html:389); L04 bretton-woods-system (L04.html:86). Other terms are plain dfn without data-concept (leverage :82, external-finance premium :82, central bank :390; L04 monthly log change :59, dispersion :59, anchor currency :85, fixed exchange rate :85, fixed-exchange-rate model :85).")
row("lx1b-banned-phrases", "2.9 banned phrases", "L03.html; L04.html; cards (L03, L04)", "PASS",
    f"{S}/scans_r15.py section 1 (prose with code and expected blocks removed, and the 51 L03/L04 cards): no TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', obviously, clearly, or an ellipsis. Output: {S}/out/scans_r15.out.")
row("lx1b-process-words", "2.9 process words", "L03.html; L04.html; cards (L03, L04)", "PASS",
    f"{S}/scans_r15.py section 1: no build, builder, round, verifier, verified, REQUEST, unit report, fixer, planner, architect or ruling in the learner text of L03, L04 or their cards.")
row("lx1b-scope-words", "2.4 scope words", "L03.html; L04.html", "PASS",
    f"{S}/scans_r15.py section 2 gives counts (L03: every 24, any 11, only 9, same 9, never 2; L04: every 19, any 9, only 9, exactly 13). Each L04 hit read in context: 'every monthly change is zero' is Prop 2.2 (A2); 'all exactly zero' is a printed Part A check; 'only' in Part B counts exact zeros; 'the first' refers to a defined window start. L03 'every period' and 'never falls' are proved (Prop 3.2(a); Part C prints the check).")
row("lx1b-structure", "2.9 structure", "L03.html sections 1-10; L04.html sections 1-9", "PASS",
    "L03: model (1), definitions (2), closed form and ordering (3), lender (4), canon breaks (5), misconceptions (4), problem set (M 3, P 3, E 3, R 3), key results (8), quiz (9: 11 items), references (10). L04: monthly log changes (1), fixed-exchange-rate model (2), recorded column (3), canon breaks (4), misconceptions (4), problem set (3 per tier), key results (7), quiz (8: 11 items), references (9). Both: hours data-hours=10; the eyebrow says 'Lesson n of 4 · 10 study hours'.")
row("lx1b-quiz-explanations", "2.9 quiz explanations", "L03.html:553-636; L04.html:483-567", "PASS",
    "Each explanation read against its lesson section: L03 Q1 (P_t after m), Q2 (psi_0 = 0), Q3 and Q4 (Part B), Q5 (Cor 3.3), Q6 (Part D 3.4260), Q7 (Cor 3.4), Q8 (V_12 = 1274345.2124), Q9 (Problem E3, 8 periods), Q10 (Def 4.1), Q11 (Section 5). L04 q1 (A2), q2 (Prop 2.2(b)), q3 (3 zero months), q4 (321), q5 (Prop 1.2), q6 (0.027935 with denominator 667), q7 (no test), q8 (ln 1.1), q9 (2000-01 start), q10 (no historical fact), q11 (0.1358 from R2 and P2). All consistent.")
row("lx1b-L03-remark42-solvency", "2.4 mathematics (Remark 4.2)", "L03.html:64-67 (Assumption 1.2), :395 (Remark 4.2)", "PASS",
    "V_m < A_0 + D with Prop 3.2(a) V_t <= V_m gives V_t < A_0 + D and A_t > 0 in every period. Numbers: V_12 = 1274345.2124 < 5000000 and V_4 = 1084165.7847 < 5000000 (rederive_r15.out: 'V_12 vs C ... True').")
row("lx1b-L03-ratio-claims", "2.4 mathematics (ratio shape claim)", "L03.html:404 (functional-form bullet); :516 (R1); :523 (R2)", "PASS",
    "If psi = phi (L - L_0)^2, each depth is beta*phi times the square of the Cor 3.4 bracket, so the ratio is the square of the Cor 3.4 ratio: 3.425970^2 = 11.737 (rederive_r15.out 'square variant ratio 11.737 vs linear 3.4259'), which differs since the ratio is not 1. A change of slope cannot change the ratio (Cor 3.4). R2's proof uses only strict monotonicity and Prop 3.2(a).")
row("lx1b-L03-r1-no-result", "2.4 mathematics (R1 solution)", "L03.html:516", "PASS",
    "R1 says Prop 3.2 is not carried over without a new proof and that Lemma 3.1's monotonicity is unaffected; the identity L_t = lambda(V_t) must be checked again. This is consistent with Lemma 3.1 and Remark 4.2 and makes no new claim.")
row("lx1b-L04-bretton-definition", "2.9 concepts / Architect ruling 14 (Bretton Woods definition pending)", "L04.html:38, :81, :86, :337, :358, :557; course/concepts.html:631", "PASS",
    "plans/FINAL-ARCHITECT-RULINGS.md item 14 (added at this pin): 'A concept whose definition waits for a source that is not admitted may carry a visible \"definition pending\" dfn (LX1 L04, bretton-woods-system), with the model the lesson does define stated separately. This is an explicit honest-pending state and is not a defect.' L04.html:86 carries the visible 'definition pending' dfn and states that the fixed-exchange-rate model is not a definition of the historical system; L04.html:38 and :81 say the same; :337, :358, :557 state no historical fact. course/concepts.html:631 labels the entry 'defined here' (generated by tools/build_site.py; build_site --check PASS); this label is the tool's, and ruling 14 covers the dfn.")
row("lx1b-L04-prediction-tested", "2.5 labs (hypothesis matches printed output)", "L04.html:114; twin Parts A and C; expected lines 307-322", "PASS",
    "The hypothesis predicts the model's zero dispersion (printed 'all exactly zero: True' line 307; 'model sample standard deviation: 0.000000' line 308) and says the recorded column has nonzero dispersion (Part C prints 0.027935 and 0.024700). The lab does not assert that the column fails (A2); the interpretation says so (L04.html:323).")
row("lx1b-L03-lab-checks-overreach", "2.2 lab claims vs output", "L03.html:145, :383; twin Parts B-D", "PASS",
    "The interpretation (L03.html:383) says the printed depths show what the assumptions imply, not an output fall; the lab prints booleans for X deeper than Y (True), never-falls (True) and strict steps (True) and does not claim history.")
row("lx1b-L03-misconception-scope", "2.9 misconceptions", "L03.html:418 (misconception 2); proof L03.html:124-131 (Cor 3.3)", "PASS",
    "Misconception 2 lists the ingredients of the Cor 3.3 proof (durations, V_m closed form, V_m < A_0 + D, Lemma 3.1, Prop 3.2(b)); compared with the proof at :130, these are the ones used.")
row("lx1b-L04-A2-before-defined", "2.1 rule 5/6 (assumptions and symbols defined before use)", "L04.html:84-92 (Def 2.1, Prop 2.2), :400-405 (P2), :450-457 (R2)", "PASS",
    "(A2) is stated in Def 2.1 (L04.html:85) before Prop 2.2 uses it (:90-92); (A3) is stated in P2 (:403) before R2 uses the bound (:453); (A1) is stated in Prop 1.2 (:66) before its use.")
row("lx1b-L04-keyresults-locator", "2.9 key results locator", "L04.html:476-477", "PASS",
    "Row 3 (dispersions and ratio) cites Lab 1 Parts C and D, which print 0.027935, 0.024700 and 0.8842 (expected block lines 314-322). Row 4 (three zero-change months) cites Lab 1 Part B (expected line 312).")
row("lx1b-cards-l03-l04", "2.7 retrieval cards (all L03 and L04 cards read)", "course/modules/LX/LX1/cards.json (L03: 29 cards; L04: 22 cards)", "PASS",
    f"All 51 L03 and L04 cards read in full this round. Every card number appears in its lesson (for example 9.20, 2.69, 3.4260, 1274345, 0.027935, 0.024700, 0.8842, 0.096575, 0.135846 in the key results or text). No duplicate id, front or back across the 81 cards and no card cites a key (cite []). Near-duplicate fronts (ratio > 0.85) are distinct questions (c037/c038 X vs Y; c055/c056 windows one vs two; c057/c065 ratio vs difference). Output: {S}/out/scans_r15.out section 6.")
row("lx1b-cards-c052-c053", "2.7 retrieval cards (Prop 2.2 and Def 2.1 cards)", "cards.json LX1-c052, LX1-c053 vs L04.html:84-92", "PASS",
    "LX1-c052 states Prop 2.2 with (A2), x-bar > 0, at least two changes, conclusion 0 and 0 (matching L04.html:90-94). LX1-c053 describes Def 2.1 with anchor currency, one foreign currency, x-bar and x_t (matching L04.html:84-85).")
row("lx1b-delta-hunks", "2.9 changed subject (8e5751c..d1e65a0, slice b)", "course/modules/LX/LX1/L04.html (@@ -331,7 +331,7 @@); cards.json (LX1-c063, c064, c084 added); L03.html, twins L03/L04 unchanged", "PASS",
    "git diff 8e5751c9 d1e65a02 for slice b: L04.html has one hunk, line 334 ('Monthly sampling' bullet now says the value is not the Board's monthly average; read and checked against tools/data_sources.yaml fx_monthly note 'the release's own monthly series are monthly averages' and the Board's about.htm 'G.5 provides the monthly release and contains monthly averages'). cards.json: c063 and c064 back-texts shortened, LX1-c084 added (read). L03.html, lab-LX1-L03-1.py, lab-LX1-L04-1.py, tools/*, notation/*, references/*, course/assets/data/market/* are byte-identical. The L01 hunks and the M3 and program.json brief change are outside this slice (L01 twin run alone and checked in lx1b-twin-alone-L01; build_site --check PASS).")
row("lx1b-L03-partD-label", "2.5 labs (Part D label and values)", "tests/labs/LX1/lab-LX1-L03-1.py Part D print; L03.html:380-382, :383", "PASS",
    "Part D prints the ratio for phi = 1/2, 1, 3 with beta = 1 and the product in its label; the expected lines 380-382 equal the twin output (run alone). Exact ratio 3.425970 -> 3.4260 in all three (rederive_r15.out).")
row("lx1b-L03-line121-lab-formula", "2.2 lab claims (closed form not evaluated by the lab)", "L03.html:120-121, :145; twin depth() and depth_path()", "PASS",
    "L03.html:121 says the lab does not evaluate Prop 3.2(b) itself; the twin computes the depth as the maximum over the path (depth, depth_path), with no closed form.")
row("lx1b-L03-why-ordering", "2.9 prose (why it matters)", "L03.html:51", "PASS",
    "The paragraph says the ordering follows from Assumptions 1.1-1.3 (Cor 3.3) and is not evidence about any economy; consistent with Cor 3.3 and the SIMULATED label.")
row("lx1b-L04-spot-only", "2.8 data (spot-only and no forward series)", "L04.html:333; L04.html:122-123 (twin docstring); tools/data_sources.yaml fx_monthly note", "PASS",
    "data_sources.yaml fx_monthly note: 'Spot rates only, as for fx_daily.' L04.html:333 quotes that statement and states no forward or interest series; the file has exchange-rate columns only (its header: month, AUD, CAD, CHF, DKK, EUR, GBP, JPY, NOK, NZD, SEK).")
row("lx1b-L03-honest-pending-source", "2.8 data (honest-pending note)", "L03.html:76", "PASS",
    "The note states that no redistributable historical series for gold-standard adherence or output depth is embedded, and that the lab is SIMULATED; it names the stay-SIMULATED condition. Consistent with plans/LX1-open-items.md D-1 and with the MANIFEST datasets (fx_daily, fx_monthly, ust_daily).")
row("lx1b-L04-twin-docstring-float", "2.5 labs (float use and docstring)", "tests/labs/LX1/lab-LX1-L04-1.py log_changes (lines 223-229), show, docstrings", "PASS",
    "log_changes: exact Fraction ratio, one float conversion, then math.log, dated by the later month; the docstring matches (lines 223-228). show() uses Decimal ROUND_HALF_UP on the exact binary value (lines 244-246) as the docstring states. No random module; no network; no warnings under -W error.")
row("lx1b-plan-coverage", "2.4 plan coverage", "plans/LX1-build-plan.md section 3 (L03 and L04 content)", "PASS",
    "L03 covers the model (3 assumptions), leverage and the premium (Def 2.1), the credit-channel chain (Def 2.2), the closed form and orderings (Lemma 3.1, Prop 3.2(a)-(c), Cor 3.3-3.4), the lender of last resort (Def 4.1, Remark 4.2), the canon breaks and the SIMULATED lab. L04 covers the window definitions, Prop 1.2, Def 2.1, Prop 2.2, Remark 2.3, the real-data lab, the spot-only and monthly-sampling limits, and states no historical fact (B3). Plan section 3 read this round.")
row("lx1b-concept-index-title", "2.9 concept index", "course/concepts.html:631, :635, :636", "PASS",
    CARRY.format(files="course/concepts.html") + "line 631 'Bretton Woods system ... defined here' links L04.html#def-bretton-woods-system (ruling 14 covers the dfn); :635 Lender of last resort -> L03; :636 Nonmonetary credit channel -> L03.")
row("lx1b-notation-registered", "2.4 notation (registered symbols)", "L03.html; L04.html", "PASS",
    f"{S}/scans_r15.py section 4 and T_in_math_r15.out: none of the registered symbols (T, Phi, gamma_3, gamma_4, R^*, R^{{e*}}, R_f, Q) occurs in TeX math of L03 or L04; the registered macros (\\E, \\R, \\Prob, \\Var, \\Cov, \\Corr, \\N, \\indic) are not used by the pages.")
row("lx1b-hours", "2.9 hours arithmetic", "L03.html:2, :34; L04.html:2, :34; hub index.html:160-161", "PASS",
    CARRY.format(files="course/modules/LX/LX1/index.html") + "the hub cards 'L03 · 10 h' and 'L04 · 10 h' (index.html:160-161). Read this round: data-hours=10 and 'LX1 · Lesson n of 4 · 10 study hours' on L03.html and L04.html. 4 x 10 = 40 lesson hours; with the project's 10 h the hub split is 40/10 = 50.")
row("lx1b-notation-N", "2.4 notation (net worth symbol N retired)", "L03.html; L04.html; cards (L03, L04); twins", "PASS",
    f"{S}/scans_r15.py section 5: no N_t, N_0, N_4 or bare N in L03.html, L04.html, the L03 and L04 twins, or the L03/L04 cards. Net worth is A_t in L03 (see lx1b-notation-A).")
row("lx1b-notation-P", "2.4 notation (cross-lesson: P_t price level, ruling 16)", "L01.html:114, :119, :120, :377; cards.json LX1-c007 (L01)", "FAIL",
    f"Ruling 16 (plans/FINAL-ARCHITECT-RULINGS.md, added at this pin): 'P_t is the price level of L02, L03 and the project. L01's observed asset price is A_t.' The round-14 row (FAIL) is not fixed. L01.html still uses P_0 for an observed asset price: line 114 ('for every price P_0 with F_0(g) < P_0 <= F_0(g')'), line 119 (proof: 'A price with F_0(g) < P_0 <= F_0(g') ... P_0 - F_0(g') <= 0'), line 120 ('At P_0 = 6000 cents the gap is +1000 cents'), line 377 (exercise: 'For a price P_0 = 6000 cents'). Card LX1-c007 (L01) also says 'every price P_0 with F_0(g) < P_0 <= F_0(g')'. {S}/scans_r15.py section 5 prints these lines. L02, L03 and project.html use P_t as the price level (correct under ruling 16).",
    "Rename the observed-price P_0 to A_0 at L01.html:114, :119 (both occurrences), :120 and :377, and in card LX1-c007 (front and back). Then re-run check_pages.py --unit LX1, the L01 twin (run_labs), and scans_r15.py section 5 (expected: no P_0 or P_t in L01.html or the L01 cards).")
row("lx1b-notation-A", "2.4 notation (local symbol A_t, redefined across the unit; plan 2.3)", "L01.html:105, :143-144, :450; cards LX1-c006 (L01: observed price); L03.html:65-67, :72, :82, :96, :103, :110, :125, :135, :149, :158, :166-167, :228, :239, :290, :293, :328-329, :395, :418, :446-455, :473, :516, :591, :605 (net worth); cards LX1-c027, c030-c032, c035-c036, c071, c082", "FAIL",
    f"Plan section 2.3 (plans/LX1-build-plan.md): local symbols are 'defined on the lesson where it first appears and never redefined'. Ruling 16 gives A_t to L01's observed asset price (L01.html:105 'let A_t be an observed price at date t'). L03 then defines A_t and A_0 as borrower net worth (L03.html:65 'Borrower net worth is A_t = A_0 - (V_t - V_0)'), so one symbol carries two meanings in LX1 ({S}/scans_r15.py section 5 lists both sets of lines). Registered-symbol rule 13 is not triggered (A is not in notation/notation.json); this row is the plan's own never-redefined rule. Judgment call: the architect may decide otherwise.",
    "Architect chooses one meaning for A_t. Preferred: keep L01's price as A_t (ruling 16) and rename L03's net worth A_t, A_0 to a symbol that no LX1 page uses (scan first), in the L03 page, its twin (Part A label and code), the expected block lines 328-329, and cards LX1-c027, c030-c032, c035-c036, c071, c082; then re-embed with tools/embed_labs.py and re-run check_pages, run_labs and the L03 twin. Alternatively, amend ruling 16 to rename L01's price.")

ids = [r["id"] for r in R]
assert len(ids) == len(set(ids)), "duplicate row id"
pass_rows = [r for r in R if r["status"] == "PASS"]
fail_rows = [r for r in R if r["status"] != "PASS"]
verdict = "PASS" if not fail_rows else "FAIL"
summary = (f"LX1-b round 15 on d1e65a0 (base 8e5751c, round-14 pin): verdict {verdict}. Rows: {len(R)} "
           f"(pass={len(pass_rows)} fail={len(fail_rows)} unverifiable=0). Non-PASS: "
           + "; ".join(f"{r['id']} ({r['short'] if 'short' in r else r['check']})" for r in fail_rows)
           + ". Lab twins are demonstrations (no mutants). Round-14 FAIL lx1b-L04-bretton-definition is PASS under ruling 14.")
frag = {
    "unit": "LX1",
    "slice": "b",
    "round": 15,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-b (L03, L04 and lab twins), round 15",
    "pin": "d1e65a0203e386e3246429ba1cf7e723eb6cfbfa",
    "base": "8e5751c903f0246115eba746afdf5d71f612bb37 (round-14 pin; delta read hunk by hunk)",
    "checkout": str(root),
    "scratch": "/tmp/lx1b-r15 (twin runs), /tmp/lx1b-r15-l01 (L01 twin), /tmp/lx1b-r15-rebuild (live fx_monthly rebuild), /tmp/lx1b-r15-web (licence pages)",
    "verified_at": "2026-11-09T01:28:53Z",
    "verdict": verdict,
    "rows": R,
    "mutants": [],
    "registry_flags": [
        "friedman1963monetary: registry record lists Friedman only; curriculum string names Friedman & Schwartz (curriculum/06-profession-capstone.yaml:37). Pages cite the key only. Architect may correct via tools/add_reference.py (plan N2).",
        "Bernanke (1983), AER 73(3) (curriculum/06-profession-capstone.yaml:38): no registry record (plan B2). L03 makes no empirical credit-channel attribution.",
        "Bretton Woods (plan B3): no registry source; L04 states no historical fact and carries the visible pending dfn (ruling 14).",
    ],
    "freshness_flags": [],
    "notes": [
        "Pin: the checkout was at 9ca1d8cb when handed over; moved to d1e65a02 (the stated pin) with git checkout --detach. No commit, no push.",
        "Mutants: none. Lab twins are demonstrations; mutation testing applies to project graders only (rulings; VERIFIER_RULES 2.5).",
        "Gates run this round (ledgers/LX1/scripts/LX1-b-r15/gates_r15.sh, outputs in out/): check_pages, check_dag, check_projects, run_labs (7/7), run_graders, verify_refs --offline and --unit LX1, fetch_data --check, build_site --check, page_smoke L03 and L04 alone, ruff check and format, mypy --no-incremental (three twins), pytest -k LX1 and collect-only, twins alone under python -I -W error (L01, L03, L04).",
        "Scripts backing rows: rederive_r15.py, expected_path_r15.py, compare_r15.py, scans_r15.py, fx_rebuild_r15.sh, licence_r15.py, write_fragment_r15.py (all under ledgers/LX1/scripts/LX1-b-r15/).",
        "Not checked: the L01 and L02 prose, the project and its twins (slices a, c, d, e); the hub index.html beyond hours; a Pyodide run outside page_smoke (run_labs runs CPython with -I -W error; page_smoke is the page-level check); the Friedman record beyond verify_refs --unit LX1; the concepts.html 'defined here' wording for the pending dfn is generated and not judged here.",
        "Judgment call for the architect: row lx1b-notation-A treats the reuse of A_t (L01 price, L03 net worth) as a breach of plan 2.3 'never redefined'. If the architect rules that local symbols may be reused across lessons, set this row to PASS.",
    ],
    "summary": summary,
}
out = root / "ledgers/LX1/LX1-b.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(R), "pass", len(pass_rows), "fail", len(fail_rows), "verdict", verdict)
