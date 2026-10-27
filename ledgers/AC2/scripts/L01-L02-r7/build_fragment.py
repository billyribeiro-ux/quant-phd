"""Build ledgers/AC2/L01-L02.json (round 7) from the round-6 rows: carry L01-only rows, re-verify the rest."""
import json, pathlib, sys

ROOT = pathlib.Path(sys.argv[1])
prev = json.load(open("/tmp/ac2-frags/L01-L02.round6.json", encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}

CARRY = ("Carried from round 6 (course/modules/AC/AC2/L01.html, tests/labs/AC2/lab-AC2-L01-1.py, "
         "atlas/A15.contract.md, references/ byte-identical since ff9284f): ")
L01_ONLY = {
    "L01-def1-1", "L01-facts-shape", "L01-tag-table", "L01-real-tag-switch", "L01-real-repeated-comparatives",
    "L01-real-10K-A-restatement", "L01-real-ties", "L01-fp-q4-real", "L01-window-real", "L01-def-2-1-M1",
    "L01-as-of-proofs", "L01-tag-priority-proof", "L01-lab-output-recomputed", "L01-numbers-prose",
    "L01-M2-M3-cutoffs", "L01-R2-growth", "L01-misconceptions", "L01-quiz", "L01-honest-data-page",
    "L01-no-registry-edgar", "L01-problem-M2-lab-claim", "L01-lab-365-comment", "L01-key-tie-grade",
    "L01-E3-l03-cross-ref",
}

R7 = {}  # id -> (status, check, location, evidence)
def put(i, status, check, location, evidence):
    R7[i] = dict(id=i, check=check, location=location, status=status, evidence=evidence)

# ---- changed subjects: re-verified in round 7 (L02.html and index.html changed; read in full) ----
put("L02-canon-section5", "PASS", "2.4 / prose", "L02.html section 5, bullet 1 (line 666)",
    "R7 re-read line 666: 'average total assets over average equity by contract' now matches atlas/A15.contract.md line 92 (leverage = average total_assets / average equity) and Definition 3.1 (line 620). The algebra 'average assets over average equity equals one plus average liabilities over average equity' holds because A_t = L_t + E_t at both year ends (simulated filer: tl + eq = ta in make_filer) and averaging is linear. 'every liability raises the leverage factor' is a ceteris-paribus statement (equity held fixed); non-blocking note, not failed. Round-6 FAIL is fixed.")
put("L02-quiz", "PASS", "2.2 / 2.4 quiz answers", "L02.html quiz (lines 822-885), esp. L02q3 explanation (line 842)",
    "R7 re-read the quiz. L02q3 explanation (line 842) now reads 'the factor is average total assets over average equity, and total assets equal total liabilities plus equity in each year', matching contract line 92. Keys recomputed: q2 750/280 = 2.6786; q4 2(1.2)/2.2 = 1.0909; q6 120/900 x 360 = 48; q9 gross margin 0.3706 (2024 row, line 599); q8 ValueError for 2020-12-31 printed (line 610); q7 DSO 43.28 (line 599/601 and Example 4.2). PASS; round-6 FAIL is fixed.")
put("L02-definition-4-1-title", "PASS", "2.4 definitions / category label", "L02.html line 652 (Definition 4.1 block title)",
    "R7: the title is now '(four ratios)' (line 652). It names no category, so the round-6 incomplete-category defect (DSO under no label) is removed. Definition body (line 653) re-read: current ratio, debt to assets and DSO use year-end items; gross margin uses no balance; matches gross_margin() and the table header (line 593).")
put("L02-definition-4-1", "PASS", "2.4 definitions / timing basis and count", "L02.html Definition 4.1 (lines 651-654); Example 4.2 (lines 656-659)",
    "R7 re-read lines 651-659 (title changed, body unchanged). Three year-end ratios and one flow ratio, 365-day count, 364/371-day remark, match lab header line 593 and twin functions current_ratio, debt_to_assets, days_sales_outstanding, gross_margin. PASS.")
put("L02-definition-4-1-note", "PASS", "2.4 Definition 4.1 other ratios", "L02.html Definition 4.1 (line 653); cards AC2-c134, c135",
    "R7 re-read line 653 and cards AC2-c134 (DSO, 365, 364/371 remark), AC2-c135 (current ratio, debt to assets), AC2-c136 (gross margin) against it. All match. PASS.")
put("L02-cards", "PASS", "2.7 cards (L02)", "cards.json, lesson L02 (18 cards: c017-c031, c134-c136)",
    "R7 entry comparison ff9284f vs HEAD (scripts/L01-L02-r7/build_fragment.py and the inline diff): only AC2-c024 changed among L02 cards (c024 re-verified below); c017-c023, c025-c031, c134-c136 identical. c024 back text re-read: 'Total assets equal liabilities plus equity in each year, so average assets over average equity equals one plus average liabilities over average equity, and rises with every liability' (T). Same ceteris-paribus scope as L02-canon-section5 (non-blocking). PASS.")
put("L01-L02-cards-changed", "PASS", "2.7 changed cards", "cards.json: AC2-c014, c026, c031, c120 (L01/L02 entries)",
    "R7 entry-level comparison of cards.json at ff9284f and HEAD (script L01-L02-r7 inline, output: changed ids c024, c075, c107): c014, c026, c031, c120 identical. PASS.")
put("L01-L02-cards-c134-c136", "PASS", "2.7 new cards (L02 Definition 4.1)", "cards.json: AC2-c134, AC2-c135, AC2-c136",
    "R7 re-read c134-c136 against Definition 4.1 (line 653); identical to ff9284f. PASS.")
put("L01-L02-cards-duplicates", "PASS", "2.7 full duplicate scan of cards.json", "course/modules/AC/AC2/cards.json (140 cards)",
    "R7 run: ledgers/AC2/scripts/L01-L02-r7/slice_checks.py output 'cards 140 unique ids 140 duplicate fronts 0'. PASS.")
put("L02-hours", "PASS", "hours", "L02.html line 2 (data-hours=10) and line 34; index.html card 'L02 · 10 h' (line 147)",
    "R7 re-read: data-hours=\"10\", eyebrow '10 study hours', hub card 'L02 · 10 h'. PASS.")
put("L02-defs", "PASS", "2.4 definitions and ids", "L02.html Definition 1.1 (line 57), Definition 3.1 (line 619), Definition 4.1 (line 652)",
    "R7 re-read lines 55-58, 618-623, 651-654. Concept ids def-financial-ratio-analysis and def-dupont-decomposition present; check_pages AC2 PASS (scripts/L01-L02-r7/check_pages.txt). PASS.")
put("L02-prop-1-2", "PASS", "2.4 mathematics", "L02.html Proposition 1.2 (line 66) and proof (lines 70-71)",
    "R7 re-read. Quotient of money items unchanged under scaling by kappa != 0; quotient of averages unchanged since the factor kappa cancels. Shares excluded as stated. PASS.")
put("L02-remark-2-1", "PASS", "2.4 mathematics", "L02.html Remark 2.1 (lines 80-83); Problem R3 (line 794); key results row (line 809)",
    "R7 recomputed: E_bar/E_t = (1 + 1/1.2)/2 = 0.9167; ROE_avg/ROE_ye = 2(1.2)/2.2 = 1.0909 (9.1%). PASS.")
put("L02-theorem-3-2", "PASS", "2.4 mathematics (DuPont identity)", "L02.html Definition 3.1 (lines 618-623), Theorem 3.2 (lines 625-628), proof (630-633)",
    "R7 re-read. Cancellations need the same averages in turnover and leverage (line 632). Lab 1 identity_ok True in every year (lab output). PASS.")
put("L02-lab-output-recomputed", "PASS", "2.2 numbers / lab recomputation", "L02.html expected block (lines 587-612) vs twin tests/labs/AC2/lab-AC2-L02-1.py",
    "R7: running tests/labs/AC2/lab-AC2-L02-1.py under python -I -W error prints exactly the expected block (script slice_checks.py: 'L02.html expected block equals twin stdout: True'). PASS.")
put("L02-prose-numbers", "PASS", "2.2 numbers in prose", "L02.html lines 637, 647, 658, 667, 682, 686, 713, 755, 769, 794",
    "R7 recomputed with ledgers/AC2/scripts/L01-L02-r7/check_l02_numbers.py: Example 3.3 product 0.173738 (printed 0.1738, one digit off, as stated); ROE gap 0.1925/0.1820 = 5.77% (5.8%); DSO restated 43.80 x 1131.9/1145.5 = 43.28; margins 0.1228 and 0.1214; Remark 2.1 1.0909. Lab-printed shares 88.1/6.5/5.4 sum to 100. PASS.")
put("L02-E1-rounding-note", "PASS", "2.2 numbers in prose (E1)", "L02.html E1 solution (line 755)",
    "R7 recomputed: 0.1925/0.2100-1 = -8.3%; 0.1738/0.1925-1 = -9.7%; 0.1237/0.1738-1 = -28.8%. Largest is the last. PASS.")
put("L02-E2-E3", "PASS", "2.4 mathematics / empirical", "L02.html E2 solution (line 762); E3 solution (line 769)",
    "R7: ln(0.0874/0.1179) = -0.2993 and ln(0.1237/0.1738) = -0.3400 on the printed four-digit values, as the text says; lab prints unrounded -0.2997 and -0.3401. E3: 0.12 x 365 = 43.80; 43.80 x 1131.9/1145.5 = 43.28. PASS.")
put("L02-M-problems", "PASS", "2.4 worked answers (M1-M3)", "L02.html M1 (line 705), M2 (712), M3 (719)",
    "R7 recomputed: M1 avg A 750, avg E 280, NM 0.1, AT 0.6667, lev 2.6786, ROE 0.1786, ROA 0.0667; M2 48.67 and 48.00, 365/360 = 1.0139 (1.4%); M3 1.60 and 0.36. PASS.")
put("L02-P-problems", "PASS", "2.4 proofs", "L02.html P1 (line 730), P2 (line 737), P3 (line 744)",
    "R7 re-read; algebra checked (cancellations; log of product). PASS.")
put("L02-R-problems", "PASS", "2.4 mathematics / prose", "L02.html R1 (780), R2 (787), R3 (794)",
    "R7 re-read. R2 says the A15 table has no short-term debt item; atlas/A15.contract.md line 171 ('A deliberate simplification: no short-term debt') and line 117 say the same. PASS.")
put("L02-twin-tie-rule", "PASS", "2.4 lab code vs contract (standardizer)", "tests/labs/AC2/lab-AC2-L02-1.py (carried twin, byte-identical since ff9284f); L02.html line 88-586 embedded copy",
    "R7: embedded L02 code equals the twin byte-for-byte (script check); twin run prints 'ValueError (conflicting tie)' and 'no error (equal-valued tie)' as the hypothesis (line 87) states. PASS.")
put("L02-penman-grade-C", "PASS", "2.3 grades (L02 claims)", "L02.html lines 62, 669, 811",
    "R7 re-read: each Penman claim is class claim data-grade=C with 'passage locator not confirmed'. The key-results row (line 811) grade C. PASS (judged on the page's own C grade).")
put("L02-canon-misc-scope", "PASS", "2.4 scope words (only/all/as much as)", "L02.html line 666 ('as much as'), line 678 ('all fall together'), line 730, line 780, line 794, lines 82, 850",
    "R7: 'Payables and deferred revenue raise it as much as borrowings do' is per dollar under A = L + E with equity fixed (non-blocking note, with the ceteris-paribus scope of L02-canon-section5); 'all fall together' verified from the printed table (net margin, turnover and leverage fall in each pair 2021-22, 22-23, 23-24); 'gap comes only from timing' (line 82) holds for constant growth. PASS.")
put("L02-misconception1-label", "PASS", "2.4 prose (misconception 1 factor label)", "L02.html line 678",
    "R7 re-read: 'The factor is an accounting ratio of total assets to equity' omits the averaging that Definition 3.1 and the canon bullet now state. Not a false fact; non-blocking wording note for the builder (add 'average' for consistency).")
put("L02-misconceptions", "PASS", "2.4 / prose (claims about what Lab 1 shows)", "L02.html Misconceptions 1-4 (lines 676-691)",
    "R7 re-read lines 676-691: 5.8% gap (0.1925 vs 0.1820 = 5.77%), mismatched product 0.1838 (lab line 602), comparison claim tied to Section 1. PASS.")
put("L02-example-4-2", "PASS", "2.2 / 2.4 claims about the filings", "L02.html Example 4.2 (line 658); Section 5 bullet 3 (line 668); quiz q7 (lines 864-870)",
    "R7 recomputed DSO 43.28, net margins 0.1228 (139.034/1131.891) and 0.1214 (139.034/1145.5). Restated revenue 1,145.5 vs filed 1,131.9 USD m (lab line 601 and twin 10-K/A row). PASS.")
put("L02-quiz-Q7", "PASS", "2.4 quiz key / premise matches the lab", "L02.html quiz item L02q7 (lines 864-870)",
    "R7 re-read. The no-cut-off standardizer includes the 10-K/A restated revenue; key and explanation match Example 4.2. PASS.")
put("L02-lab-header-gross-margin-basis", "PASS", "2.2 / 2.4 lab label and hypothesis vs Definition 4.1", "L02.html line 87; line 593; twin line 422",
    "R7 re-read: hypothesis (line 87) and printed header (line 593) match gross_margin() and Definition 4.1. PASS.")
put("L02-banned-phrases", "PASS", "2.9 structure and prose (BUILDER_RULES 1.2/1.3)", "L02.html learner text; index.html; L01.html",
    "R7: slice_checks.py grep for roughly/historically/typically/builder/this build/build report/unit report/REQUESTS: no hits in index.html, L01.html, L02.html. Number-free 'about' phrases checked by reading lines 1-895. PASS.")
put("L02-quiz-numbers", "PASS", "2.2 quiz numeric keys", "L02.html quiz items q2 (line 830), q4 (844), q6 (858), q9 (881)",
    "R7: keys 2.6786 (tol 0.0002, 750/280 = 2.67857), 1.0909 (tol 0.0005, 2.4/2.2), 48 (tol 0.5), 0.3706 (tol 0.0002, line 599). PASS.")
put("L02-c024-card", "PASS", "2.7 changed card AC2-c024", "cards.json AC2-c024 (back text)",
    "R7 re-read c024: algebra holds (average A = average L + average E); 'rises with every liability' is ceteris-paribus, same scope as L02-canon-section5 (non-blocking). Grade T is for an identity proved on the page (Definition 3.1 and averaging). PASS.")
put("L02-quiz-q3-explain", "PASS", "2.4 quiz explanation L02q3", "L02.html line 842",
    "R7: the option (line 839) and explanation (line 842) now use average assets over average equity; consistent with contract line 92. PASS.")
put("L02-access-statements", "PASS", "honest data / access statements in learner text and plans", "L02.html Definition/section text (none); plans/AC2-open-items.md lines 10, 16 and 24 (cited by the hub and c107); course/modules/AC/AC2/index.html line 169",
    "R7 reproduced with plain curl (ledgers/AC2/scripts/L01-L02-r7/access_check.sh, output access_check.txt): https://www.sec.gov/os/webmaster-faq 403; https://www.sec.gov/os/accessing-edgar-data 403; https://doi.org/10.2308/tar-9505096112 302 to publications.aaahq.org/accounting-review/article/70/2/193/18940/Detecting-Earnings-Management which returns 403; https://doi.org/10.2469/faj.v55.n5.2296 302 to www.tandfonline.com/doi/full/10.2469/faj.v55.n5.2296 which returns 403; data.sec.gov companyfacts CIK0000320193 returns 200. The statements match. No challenge page was inspected or bypassed.")
put("L01-L02-hub-card-jones", "PASS", "2.1 citation claim vs readable source (architect ruling f)", "index.html line 149 (L06 card)",
    "R7 re-read the new card text: 'The modified Jones model as the A15 contract defines it (registry key dechow1995detecting), its estimation, and a planted manipulation that the model is tested to recover.' The contract defines modified_jones (atlas/A15.contract.md line 123 cites dechow1995detecting by key and title; OLS without intercept, lines 123-128). The card no longer states what the paper evaluates, so the round-6 UNVERIFIABLE (DOI 403) does not apply. 'tested to recover' matches L06 Lab 1 ('Recovering a planted manipulation', which asks whether the regression recovers it); the lab is SIMULATED. Judged on the card's own claims.")
put("L01-L02-hub-hours", "PASS", "2.9 structure / hours", "index.html lines 29, 31, 144-151; L01.html line 2 (data-hours=9); L02.html line 2 (data-hours=10)",
    "R7: lesson hours in the cards 9+10+8+9+8+10+10+12 = 76 = data-hours-lessons; project 34; 76+34 = 110 = Tier U header. PASS.")
put("L01-L02-hub-prereqs", "PASS", "DAG / prerequisites", "index.html lines 35, 60-64",
    "R7 re-read lines 35 and 60-64; prerequisites AC1, S0, S2 (S2 carries S1 and M3). check_dag AC2 PASS (scripts/L01-L02-r7/check_dag.txt). PASS.")
put("L01-L02-hub-placement-count", "PASS", "2.9 structure / placement diagnostic", "index.html lines 70-136",
    "R7 re-read all nine items: 4 AC1 (Pq1, gross margin, Pq3, Pq4), 2 S0 (median, Pq6), 3 skill checks (rung 1 as-of, two rung-2 DuPont and ROIC). Count nine. PASS.")
put("L01-L02-hub-links", "PASS", "2.9 structure / navigation", "index.html; L01.html; L02.html",
    "R7: all 15 relative hrefs in index.html resolve (slice_checks.py: 'unresolved []'); check_pages AC2 PASS.")
put("L01-L02-hub-objectives", "PASS", "2.9 structure / coverage of objectives", "index.html lines 48-55",
    "R7 re-read the six objectives. Each objective names a lesson or the project (L01 standardize, L02 ratios, L03 ROIC, L04/L05 accruals, L06 discretionary models, L07/L08 scores). PASS.")
put("L01-L02-hub-honest-pending", "PASS", "honest data / SIMULATED claims", "index.html lines 167-169; L01.html line 599; L02.html line 613",
    "R7 re-read index.html 167-169 ('SIMULATED data only, for now'; no figure is a real company's) and L02.html line 613 (interpretation labelled SIMULATED). L01 line 599 carried. PASS.")
put("L01-L02-sec-reuse-statement-access", "PASS", "honest data / external source access", "index.html line 169",
    "R7 reproduced: plain curl to https://www.sec.gov/os/webmaster-faq and https://www.sec.gov/os/accessing-edgar-data returned 403 (ledgers/AC2/scripts/L01-L02-r7/access_check.txt). The hub says the statement 'has not been read from the SEC page by automated access', which matches. PASS.")
put("L01-L02-data-request-open", "PASS", "honest data / status claim", "index.html line 169; plans/AC2-open-items.md lines 1-10",
    "R7 re-read open-items DATA_REQUESTS row: OPEN; the 403 statement is reproduced (row above). PASS.")
put("L01-L02-hub-core-reading", "PASS", "2.1 citations / rendered bibliography and authored prose", "index.html lines 172-180 (refs.js rendering); line 177",
    "R7 re-read the reading list (keys penman2013financial, sloan1996stock, dechow1995detecting, piotroski2000value, beneish1999detection) and the title 'Detecting Earnings Management' without authors (ruling 1); verify_refs --unit AC2 (live) '7 of 560 entries, 0 problems'; --offline '560 entries, 0 problems'. PASS.")
put("L01-L02-hub-penman-c", "PASS", "2.3 grades (Penman 2013 claims)", "index.html line 175 (core-reading list)",
    "R7 re-read lines 172-180: the hub states no grade for Penman; the grades live in L02 lines 62, 669, 811 (C). PASS.")
put("L01-L02-check-pages-dag", "PASS", "2.9 structure / DAG", "course/modules/AC/AC2",
    "R7 run: tools/check_pages.py --all -> 'check_pages AC2: PASS'; tools/check_dag.py --all -> 'check_dag AC2: PASS' (scripts/L01-L02-r7/check_pages.txt, check_dag.txt).")
put("L01-L02-pagesmoke", "PASS", "2.5 labs / runtime", "tools/page_smoke.py --unit AC2 --pages L01 L02 index",
    "R7 run: 'page_smoke AC2: PASS'; lab-AC2-L01-1 and lab-AC2-L02-1 each 0.0 s (scripts/L01-L02-r7/page_smoke.txt).")
put("L01-L02-run-labs", "PASS", "2.5 labs / twin identity", "tools/run_labs.py --unit AC2 --page L01 and --page L02",
    "R7 run: 'run_labs AC2: PASS (1/1)' for L01 and for L02 (scripts/L01-L02-r7/run_labs_L01.txt, run_labs_L02.txt).")
put("L01-L02-twins-isolated", "PASS", "2.5 labs / run alone", "tests/labs/AC2/lab-AC2-L01-1.py; lab-AC2-L02-1.py",
    "R7: python -I -W error on each twin exits 0 (twin_L01.txt, twin_L02.txt); L01 prints the ValueError lines, L02 prints the lab output shown above.")
put("L01-L02-ruff-mypy-pytest", "PASS", "2.9 gates (slice twins and tests)", "tests/labs/AC2/lab-AC2-L01-1.py; lab-AC2-L02-1.py; pytest subset",
    "R7 run: ruff check tests/labs/AC2 'All checks passed!'; mypy --no-incremental on both twins 'Success: no issues found in 2 source files'; pytest -k 'AC2 or L01 or L02' over tests/test_labs.py, test_run_labs.py, test_page_smoke.py, test_page_checks.py: 22 passed (exit 0).")
put("L01-L02-notation", "PASS", "2.4 notation conformity", "index.html; L01.html; L02.html",
    "R7: L02 new text uses \\bar A, \\bar E forms in Definition 3.1 unchanged; the rewritten canon bullet and quiz use words for averages, consistent with notation used elsewhere. PASS.")
put("L01-L02-process-jargon", "PASS", "2.9 learner text: no process words", "index.html; L01.html; L02.html",
    "R7 grep (slice_checks.py): no 'builder', 'this build', 'build report', 'unit report', 'REQUESTS' in the three pages. PASS.")
put("L01-L02-lab-numbering", "PASS", "2.9 lab numbering per page", "L01.html; L02.html",
    "R7: L02 lab is 'Lab 1' (line 86); L01 lab 'Lab 1' per carried page; cross-references 'Lab 1' on L02 refer to its own lab. PASS.")
put("L01-L02-ladder-rungs", "PASS", "2.9 hub ladder rungs 1-2 vs project page", "index.html lines 154-160; project.html lines 42-47",
    "R7 re-read index ladder items; project.html byte-identical since ff9284f (git diff quiet). PASS.")
put("L01-L02-placement-mastery", "PASS", "2.9 placement arithmetic vs the scoring code", "index.html line 68 (data-mastery 0.8), lines 70, 118, 127, 132; course/assets/js/quiz.js lines 67-78",
    "R7: quiz.js sets overall = correct / items.length >= mastery and the skill-check condition; 8/9 = 0.889 passes, 7/9 = 0.778 fails, so 'eight correct, since seven is 78%' is right. 'No placement item tests S2' holds (all nine read). PASS.")
put("L01-L02-verify-refs", "PASS", "2.1 citations: verify_refs live and offline", "tools/verify_refs.py --unit AC2 (live); tools/verify_refs.py --offline",
    "R7 run: live 'live re-verification of AC2: 7 of 560 entries, 0 problems'; offline 'offline integrity: 560 entries, 0 problems' (scripts/L01-L02-r7/verify_refs_live_AC2.txt, verify_refs_offline.txt).")
put("L01-L02-run-graders", "PASS", "2.5 autograder (command row)", "tools/run_graders.py --unit AC2",
    "R7 run: 'run_graders AC2: PASS (reference 50/50 seeds, slowest 0.3 s)' (run_graders_AC2.txt).")
put("L01-L02-companyfacts-fetch", "PASS", "2.1 real-data check: file fetched by the verifier (plain curl)", "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json",
    "R7 plain curl: HTTP 200 (access_check.txt). The file was not parsed for this slice; the real-data use is an open item (plans/AC2-open-items.md) and the hub says every filer is SIMULATED.")
put("L01-L02-lab-fidelity-sim", "PASS", "honest data / SIMULATED results (rule e)", "L01.html key results (lines 754-760); L02.html key results (lines 806-811)",
    "R7 re-read L02 key results: rows 806-809 are T on the page (proofs and Remark 2.1); row 810 is C with 'Lab 1 (SIMULATED)'; row 811 is C (Penman). L01 rows carried. PASS.")
put("L01-L02-hub-ladder-seeds", "PASS", "2.9 claim vs what the tests enforce (architect ruling a)", "index.html line 161 ('Instances are generated from your workspace seed')",
    "R7 re-read line 161; the grader and its seeds are byte-identical since ff9284f (git diff quiet on course/modules/AC/AC2/grader); run_graders 50/50 seeds PASS. PASS.")
put("L01-L02-no-contrary", "PASS", "2.1 Beneish constants not presented as established", "L02.html; index.html; cards AC2-c107 (L08, out of slice)",
    "R7 grep: 'Beneish' appears in L02.html zero times; index.html lines 54, 151, 161 and 179 name the M-score and the reading only, with no constant. No Beneish constant appears in L01, L02 or the hub. PASS.")

# ---- carried L01 rows (byte-identical subjects since ff9284f) ----
rows = []
for rid, r in prev_rows.items():
    if rid in R7:
        continue
    if rid in L01_ONLY or rid in ("L01-cards", "L01-cross-ref-reference-request", "L01-banned-about-90"):
        if rid == "L01-banned-about-90":
            put(rid, "PASS", r["check"], "L01.html; L02.html; index.html",
                "R7 re-ran the banned-word scan (slice_checks.py): no hits on the three pages; L01.html carried byte-identical.")
            continue
        if rid == "L01-cards":
            put(rid, "PASS", r["check"], "cards.json lesson L01 entries c001-c016, c120",
                CARRY + "cards.json entries AC2-c001..c016 and c120 identical at ff9284f and HEAD (R7 entry comparison: only c024, c075, c107 changed). " + r["evidence"])
            continue
        if rid == "L01-cross-ref-reference-request":
            put(rid, "PASS", r["check"], r["location"],
                "R7 re-read plans/AC2-open-items.md line 22 (SEC company-facts documentation row, unchanged text) and L01.html lines 66, 850. " + r["evidence"])
            continue
        put(rid, "PASS", r["check"], r["location"], CARRY + r["evidence"])
        continue

# ---- anything round 6 had that R7 did not handle must fail closed ----
missing = [rid for rid in prev_rows if rid not in R7 and rid not in {x["id"] for x in rows}]
assert not missing, missing

out_rows = []
for rid in prev_rows:
    if rid in R7:
        out_rows.append(R7[rid])
    else:
        out_rows.append(dict(id=rid, check=prev_rows[rid]["check"], location=prev_rows[rid]["location"],
                             status=prev_rows[rid]["status"], evidence=CARRY + prev_rows[rid]["evidence"]))
for rid, row in R7.items():
    if rid not in prev_rows:
        out_rows.append(row)

for row in out_rows:
    if row["status"] == "PASS" and row["id"] in R7:
        pass

frag = dict(
    unit="AC2", slice="L01-L02", round=7,
    verifier="independent round-7 verifier for AC2 slice L01-L02 (fresh context; round-6 fragment read as context only; L02.html read in full, index.html read in full; L01 subject carried by byte-identity)",
    pin="6adfd01", base="ff9284f", checkout="/tmp/verify-ac2r7-l12", scratch="/tmp/ac2-v/l12/r7",
    verified_at="2026-10-27", verdict=None,
    mutants=[], registry_flags=[], freshness_flags=[],
    notes=[
        "Delta ff9284f..6adfd01 for this slice: L02.html (Definition 4.1 title line 652; canon bullet 1 line 666; quiz q3 option line 839 and explanation line 842); index.html line 149 (L06 card); cards.json c024 (L02), c075 and c107 (not this slice); plans/AC2-open-items.md (DATA_REQUESTS and REFERENCE_REQUESTS rows). L01.html, both L01/L02 twins, tests/labs, grader, project.html, atlas, references are byte-identical since ff9284f (git diff --quiet).",
        "All four round-6 non-PASS rows are now PASS on re-verification: L02-canon-section5 and L02-quiz (the average-based leverage factor is now stated and matches contract line 92), L02-definition-4-1-title ('(four ratios)' names no category), L01-L02-hub-card-jones (the card no longer asserts what the paper evaluates; it cites the contract's definition).",
        "Every access statement was reproduced with plain curl and recorded URLs (access_check.txt). The Beneish DOI redirects to tandfonline.com (403); the Dechow DOI redirects to publications.aaahq.org (403); the SEC pages return 403. No bypass was attempted.",
        "Non-blocking wording notes (PASS): the 'every liability raises the leverage factor' and 'as much as borrowings' statements in canon bullet 1 and card c024 hold ceteris paribus (equity fixed); misconception 1 (line 678) describes the factor without 'average'. The builder may add those qualifiers; they do not change any number or claim.",
        "Rows carried from round 6 are limited to subjects byte-identical since ff9284f (L01.html, the L01 twin, atlas, references, project.html, grader, and L01 card entries); every L02, hub, open-items and command row was re-run or re-read in this round.",
        "Honest gaps unchanged: the dechow1995detecting paper body, the Beneish paper, the Penman passage locator and the workspace-ID-to-seed mapping are not readable by plain curl; they are labelled UNCONFIRMED or C in the pages.",
    ],
    rows=out_rows,
)
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in out_rows:
    counts[r["status"]] += 1
frag["summary"] = {"rows": len(out_rows), **{k.lower(): v for k, v in counts.items()}}
frag["verdict"] = "PASS" if counts["PASS"] == len(out_rows) else "FAIL"
dst = ROOT / "ledgers/AC2/L01-L02.json"
dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(out_rows), counts)
