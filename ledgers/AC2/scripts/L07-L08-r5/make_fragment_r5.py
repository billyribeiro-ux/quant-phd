"""Builds ledgers/AC2/L07-L08.json (round 5) from the row table below. Run with the checkout's .venv python -I."""
import json, sys, datetime
sys.path.insert(0, "tools")
import ledger  # noqa: E402

P, F, U = "PASS", "FAIL", "UNVERIFIABLE"
R = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    R.append(r)


PIN = "Round 5 (pin 11b3477): "
row("L07-L08-cmd-pin", "2.9-structure", "repository (checkout /tmp/verify-ac2r5-l78)", P,
    PIN + "git rev-parse --short HEAD -> 11b3477; git status --short -> '?? .venv' only (logs/pin.txt).")
row("L07-L08-cmd-run_labs", "2.5-lab", "tools/run_labs.py --unit AC2", P,
    PIN + "run_labs.py --unit AC2 -> 'run_labs AC2: PASS (11/11)', exit 0 (logs/run_labs.txt).")
row("L07-L08-cmd-twins", "2.5-lab", "tests/labs/AC2/lab-AC2-L07-1.py, lab-AC2-L08-1.py", P,
    PIN + "each twin run as python -I -W error from a scratch dir: exit 0, stderr 0 bytes (logs/twin-L07, twin-L08); stdout equals the page's expected block exactly (533 and 1247 bytes).")
row("L07-L08-cmd-embed", "2.5-lab", "course/modules/AC/AC2/L07.html, L08.html (data-run and expected blocks) vs twins", P,
    PIN + "tools/embed_labs.py has no check mode and rewrites marker-bearing pages, so it was not run on the built pages; instead the page code blocks were unescaped and compared byte-for-byte with the twins (code == twin: True for both) and the expected blocks with the twins' stdout (exact: True for both).")
row("L07-L08-cmd-page_smoke", "2.9-structure", "tools/page_smoke.py --unit AC2 --pages L07 L08", P,
    PIN + "page_smoke --unit AC2 --pages L07 L08 -> 'page_smoke AC2: PASS', exit 0 (logs/page_smoke.txt).")
row("L07-L08-cmd-check_pages_dag_projects", "2.9-structure", "tools/check_pages.py, check_dag.py, check_projects.py --all", P,
    PIN + "all three exit 0; 'check_pages AC2: PASS', 'check_dag AC2: PASS', 'check_projects AC2: PASS' (logs/check_*.txt).")
row("L07-L08-cmd-lint_mypy", "2.5-lab", "the two twins", P,
    PIN + "ruff check: 'All checks passed!'; ruff format --check: '2 files already formatted'; mypy --no-incremental: 'Success: no issues found in 2 source files'; all exit 0.")
row("L07-L08-cmd-pytest", "2.5-lab", ".venv/bin/pytest -q -k 'AC2 or ac2 or L07 or L08'", P,
    PIN + "pytest -q -k 'AC2 or ac2 or L07 or L08' exit 0, 28 tests passed (logs/pytest.txt).")
row("L07-L08-cmd-verify_refs", "2.1-citation", "tools/verify_refs.py --unit AC2 (live) and --offline (no unit)", P,
    PIN + "live: 'live re-verification of AC2: 7 of 560 entries, 0 problems', exit 0; offline: '560 entries, 0 problems', exit 0 (logs/verify_refs_*.txt).")
row("L07-L08-cite-piotroski2000value", "2.1-citation", "references/references.json key piotroski2000value; L07 data-cite", P,
    PIN + "registry: Crossref doi 10.2307/2672906, Journal of Accounting Research vol 38, status verified; L07 cites it at lines 98, 102, 104, 106, 341, 356.")
row("L07-L08-cite-sloan1996stock", "2.1-citation", "references/references.json key sloan1996stock; L07 line 108 claim span", P,
    PIN + "registry key present (title 'Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?', year 1996, status verified); L07 line 108 says Sloan (1996) 'has not been read' and takes the attribution from Piotroski p. 8, which the PDF confirms.")
row("L07-L08-cite-beneish1999detection", "2.1-citation", "references/references.json key beneish1999detection; L08 data-cite (lines 56, 95)", P,
    PIN + "registry: Financial Analysts Journal, vol 55, issue 5, pages 24-36, DOI 10.2469/faj.v55.n5.2296, status verified; L08 lines 56 and 95 cite it with the locator 'passage locator not confirmed'.")
row("L07-L08-loc-p1-p3-7.5-23", "2.1-citation", "L07.html line 104 (claim span 'Abstract, p. 1; p. 3')", P,
    PIN + "pdftotext of the Ivey-hosted PDF (sha256 901d7135..., identical to round 4): p. 1 abstract 'at least 7.5% annually' and '23% annual return between 1976 and 1996'; p. 3 'generates a 23% annual return between 1976 and 1996'.")
row("L07-L08-loc-p12-1448-396", "2.1-citation", "L07.html line 106 (claim span 'p. 12 (1,448 and 396 observations)')", P,
    PIN + "PDF p. 12: 'number of observations equals 1,448 and 396, respectively' (bootstrap design). The 1,448/396 classification sentence is on p. 16, which the lesson does not cite for it.")
row("L07-L08-loc-p7-n2-optimal", "2.1-citation", "L07.html line 98 (claim span 'p. 7, n. 2')", P,
    PIN + "PDF p. 7, footnote 2: 'factor analysis may more aptly extract an optimal combination of signals, but such an approach has costs in terms of implementability' (exact quote at line 98).")
row("L07-L08-loc-p9-n5-cutoff", "2.1-citation", "L07.html line 341 claim span; key-results row (line 435); card AC2-c100", P,
    PIN + "PDF p. 9 footnote 5 (marker after 'liquidity improved'): 'A specification where the current ratio cutoff equals 1.5 yields stronger return results than the liquidity metric and aggregate score used in the paper.' Claim span matches.")
row("L07-L08-loc-p7-ex-ante-quote", "2.1-citation", "L07.html line 102 (claim span, quote)", P,
    PIN + "PDF p. 7 exact: 'the stated ex ante implication of each signal is conditioned on the fact that these firms are financially distressed at some level'.")
row("L07-L08-loc-p7-distress-average", "2.1-citation", "L07.html line 102 (sentences on distress, leverage, p. 6/p. 7)", P,
    PIN + "PDF p. 6: 'The average high BM firm is financially distressed'; PDF p. 7: 'for financially distressed firms, the negative implications of increased leverage seem more plausible than the benefits garnered through a reduction of agency costs'.")
row("L07-L08-loc-keyresults-2.3", "2.1-citation", "L07.html key-results row 1 (line 428; source 'Piotroski (2000), §2.3, pp. 6–10')", P,
    PIN + "PDF: section 2.3 'Financial performance signals' begins p. 6 and 2.3.4 'Composite score' is on p. 10.")
row("L07-L08-loc-signal-groups", "2.1-citation", "L07.html line 86 (groups) and table lines 72-85", P,
    PIN + "PDF: 2.3.1 'Profitability' on p. 7; 2.3.2 'Leverage, Liquidity, and Source of Funds' on p. 8; 2.3.3 'Operating Efficiency' on p. 9. The line 86 page locators (p. 7; source-of-funds heading p. 8) are correct.")
row("L07-L08-loc-scaling-p7-p8-p9", "2.1-citation", "L07.html line 65 (pp. 7, 8, 9)", P,
    PIN + "PDF p. 7: ROA and CFO 'scaled by beginning-of-the-year total assets'; p. 8: leverage is 'total long-term debt to average total assets'; p. 9: ATURN 'scaled by the beginning-of-the-year total assets'.")
row("L07-L08-loc-proxies-p7-p8-p9", "2.1-citation", "L07.html lines 93-95 (§2 items 1-3)", P,
    PIN + "PDF p. 7 (ROA/CFO 'before extraordinary items'), p. 9 (EQOFFER 'did not issue common equity'), p. 8 (leverage on average total assets). Each item's description matches.")
row("L07-L08-loc-p11-sample", "2.1-citation", "L07.html line 102 (p. 11) and line 411 (R1)", P,
    PIN + "PDF p. 11: each fiscal year 1976-1996, 'retain firms in the highest BM quintile'; p. 11 and p. 12: buy-and-hold returns 'from the beginning of the fifth month after the firm's fiscal year-end' (R1 description correct).")
row("L07-L08-loc-p12-groups-bootstrap", "2.1-citation", "L07.html lines 106, 356 (p. 12 groups and bootstrap)", P,
    PIN + "PDF p. 12: 'FSCORE equals 8 or 9' is the high group and '0 or 1' the low group; bootstrap of pseudo-portfolios on p. 12.")
row("L07-L08-loc-sloan-p8", "2.1-citation", "L07.html line 108 (locator 'Piotroski p. 8, citing Sloan (1996)')", P,
    PIN + "PDF p. 8: 'Sloan [1996] shows that earnings driven by positive accrual adjustments ... is a bad signal'.")
row("L07-L08-loc-access-claims-L08", "2.1-citation", "L08.html line 93 (access sentence)", P,
    PIN + "re-run: doi.org/10.2469/faj.v55.n5.2296 -> 302 to www.tandfonline.com/doi/full/...; tandfonline doi/full and doi/abs -> 403; researchgate and SSRN URLs built for this check -> 403; JSTOR 2672906 -> 200 'Client Challenge / JavaScript is disabled' (challenge page, not the record). Statuses agree with the page; see card row below for the JSTOR attribution problem.")
row("L07-L08-loc-beneish-constants-label", "2.1-citation", "L08.html lines 56, 60, 93, 95, 97, 106, 439-443, 530, 566; lab docstring 114-118; constants 133-144", P,
    PIN + "every use of the candidate intercept and weights carries the UNCONFIRMED label (lab docstring and constants, §3 worked M, misconception 2, quiz item 5, E1 solution, key-results row 566).")
row("L07-L08-beneish-published-wording", "2.3-grade", "L08.html lines 56, 60, 95, 566", P,
    PIN + "no sentence calls the constants Beneish's published numbers; line 56 repeats the contract's 'published constants (unconfirmed here)' and line 95 says 'Nothing in this lesson should be read as Beneish's own published number'.")
row("L07-L08-beneish-tata-disagreement", "2.1-citation", "L08.html R1 solution (line 545)", P,
    PIN + "R1 solution: 'The intercept and all eight weights come from the same single secondary page, so the whole set needs checking against the paper, not only the TATA weight.' Consistent with §2.")
row("L07-L08-beneish-cutoffs", "2.1-citation", "L08.html line 97", P,
    PIN + "re-read Wikipedia 'Beneish M-score' (200, plain curl): 'The threshold value is -1.78 for the model whose coefficients are reported above. (see Beneish 1999, Beneish, Lee, and Nichols 2013, and Beneish and Vorst 2020)'. Line 97 matches: named '1999', two other works, no page, graded D.")
row("L07-L08-build-report-refs", "2.1-citation", "L07.html line 344; L08.html line 478 (pointers to plans/AC2-open-items.md)", P,
    PIN + "grep -c 'open-items' gives 1 in each page; plans/AC2-open-items.md rows 17 (Mohanram), 19 (Beneish, Lee & Nichols), 25 (out-of-sample), 26 (joint use) exist.")
row("L07-L08-math-signals-vs-contract", "2.4-math", "L07.html lines 56-86 (ratios, Definition 1.1, table) vs atlas/A15.contract.md piotroski_f_score block", P,
    PIN + "contract: s1 ROA>0; s2 CFO>0; s3 ROA_t>ROA_{t-1}; s4 CFO_t>ROA_t; s5 LEV_t<LEV_{t-1}; s6 CR_t>CR_{t-1}; s7 Sh_t<=Sh_{t-1}; s8 GM; s9 ATO. Page table lines 75-83 matches item for item.")
row("L07-L08-math-proxies-stated", "2.1-citation", "L07.html §2 (lines 90-96); contract 'Departures from the published definitions'", P,
    PIN + "contract lists three departures (net income tag, shares for equity issuance, LongTermDebtNoncurrent); §2 lists the same three at lines 93-95.")
row("L07-L08-math-P1", "2.4-math", "L07.html P1 (lines 378-381)", P,
    PIN + "P1 proof is sound (divide by TA_{t-1} > 0). PDF p. 8: ACCRUAL = (NI - CFO)/beginning TA and FTACCRUAL = 1 if CFO > ROA; the page's claim that these coincide is correct.")
row("L07-L08-math-P2", "2.4-math", "L07.html P2 (lines 382-385)", P,
    PIN + "proof valid; lab check 400/400 (logs/twin-L07.stdout) agrees.")
row("L07-L08-math-P3", "2.4-math", "L07.html P3 (lines 386-389)", P,
    PIN + "recomputed (Fraction): LEV_t = 300/950 = 0.31579 > LEV_{t-1} = 310/1050 = 0.29524, so s5 = 0 (scripts/recompute2.py).")
row("L07-L08-math-worked-firm", "2.4-math", "L07.html §4 (lines 307-335), M1 (364-366), M2 (368-370), M3 (372-374), E2 (398-400)", P,
    PIN + "recomputed with Fraction (ledgers/AC2/scripts/L07-L08-r5/): ROA_t 117/1100 = 0.1064, ROA_{t-1} 66/1000, CFO* 96/1100 = 0.0873, LEV 264/1150 = 0.2296 vs 330/1050 = 0.3143, CR 2.20 vs 2.00, GM 0.35 vs 0.30, ATO 1.4182 vs 1.32; vector (1,1,1,0,1,1,1,1,1), F = 8. M2 vector (0,1,0,1,1,1,1,1,1), F = 7. E2: 118/1100 = 0.10727 > 0.10636.")
row("L07-L08-math-E1-count", "2.2-numbers", "L07.html E1 (line 396) and Lab 1 output (lines 289-300)", P,
    PIN + "output lines 298-299: score 8 = 24, score 9 = 7; 31/400 = 0.0775 (exact).")
row("L07-L08-misconception-score-zero", "2.4-math", "L07.html misconception 1 (line 352); L08.html line 443; card AC2-c103", P,
    PIN + "line 352 now reads 'Signal 4 compares CFO with net income in the same year, which is a same-year comparison, not a change test' and 'The score mixes sign tests (s1, s2), a same-year comparison (s4) and change tests (s3, s5 to s9)'. The round-4 'level test' contradiction is gone, and L08 line 443 uses the same taxonomy. Example recomputed: s1=s2=1, s3..s9=0, F=2.")
row("L07-L08-math-L08-indices", "2.4-math", "L08.html lines 78-85 (eight index list); atlas/A15.contract.md beneish_m_score", P,
    PIN + "all eight index formulas in lines 78-85 match the contract block and the twin's beneish_indices (lines 197-210) term for term.")
row("L07-L08-math-prop4.2", "2.4-math", "L08.html Proposition 4.2 and proof (lines 447-452), P1 (line 515)", P,
    PIN + "PPV = ps/(ps+(1-p)(1-sigma)) derivation from Bayes and total probability is correct; base-rate table reproduces it (Fraction check).")
row("L07-L08-math-prop4.3", "2.4-math", "L08.html Proposition 4.3 and proof (lines 458-463), P2 (line 519)", P,
    PIN + "AND = f1 f2 and OR = 1-(1-f1)(1-f2) under independence: 0.0050 and 0.1450 (exact).")
row("L07-L08-math-L08-P3", "2.4-math", "L08.html P3 (lines 520-523)", P,
    PIN + "min/max bounds on sensitivity of AND/OR hold without independence (proof valid).")
row("L07-L08-math-worked-M", "2.2-numbers", "L08.html §3 display (lines 431-437), quiz item 5 explanation (line 609)", P,
    PIN + "recomputed with Fraction: unrounded indices give M = -1.559271 (rounds to -1.5593); displayed four-decimal indices with exact weights give -1.55943 (rounds to -1.5594). Line 437 states exactly this.")
row("L07-L08-math-base-rate-table", "2.2-numbers", "L08.html lab output (lines 400-409) and base-rate table", P,
    PIN + "all nine rows (PPV, FPR, false flags per 1000) recomputed exactly and match the lab output (logs/recompute2.txt).")
row("L07-L08-math-E2-E3-E1", "2.4-math", "L08.html E1 (lines 530), E2 (534), E3 (536-538)", P,
    PIN + "E1: -1.5067 - (-2.4747) = 0.9680; E2: 0.3448/0.0099 = 34.8 (about 35, ratio of PPVs at equal sensitivity and specificity: 34.79 exact); E3: 1000 x 0.99 x 0.05 = 49.5, and 1000 x FPR = 50 per clean firm-years.")
row("L07-L08-math-dependence-sign", "2.4-math", "L08.html §4 paragraph (line 466), misconception 3 (line 490), quiz item 10 (line 653)", P,
    PIN + "positive correlation raises AND and lowers OR; the worked example f1=0.10, f2=0.05 with disjoint flags gives AND 0 (< 0.0050) and OR 0.15 (> 0.1450): feasible joint law, arithmetic correct.")
row("L07-L08-math-growth-claim", "2.4-math", "L08.html §5 bullet 'Growth is a confound' (line 476); card AC2-c118", P,
    PIN + "witness recomputed: DSRI = (150/1500)/(100/1000) = 1, SGAI = (225/1500)/(150/1000) = 1, SGI = 1.5 exactly.")
row("L07-L08-lab-L07-1", "2.5-lab", "lab-AC2-L07-1 (hypothesis line 114, code 115-281, interpretation line 302)", P,
    PIN + "run: 'signals unchanged under money x1000: 400/400'; hypothesis and interpretation agree with the output; the lab does not test the range 0-9 and the page says so (line 110).")
row("L07-L08-lab-L08-1-overreach", "2.5-lab", "lab-AC2-L08-1 hypothesis (line 106) and main() (lines 334-380)", P,
    PIN + "the lab prints the planted-vs-clean medians and labels them as properties of the generator (interpretation line 413); the base-rate arithmetic is labelled illustrative (sensitivity 0.5, an assumption).")
row("L07-L08-lab-L08-1-run", "2.5-lab", "lab-AC2-L08-1 run and labels (lines 384-412)", P,
    PIN + "run stdout identical to the page block (1247 bytes); 'indices unchanged ... 600/600'; 'section 4 check ... True'.")
row("L07-L08-num-L07-lab-distribution", "2.2-numbers", "L07.html lab output lines 289-300", P,
    PIN + "twin stdout: score 2:2, 3:16, 4:60, 5:108, 6:109, 7:74, 8:24, 9:7; mean 5.6475; identical to the page block.")
row("L07-L08-grade-L07", "2.3-grade", "L07.html claim spans and key-results rows (lines 428-436)", P,
    PIN + "proofs (P1, P2, worked arithmetic) graded T; paper numbers and the Sloan attribution graded C; the Sloan attribution row says 'Sloan (1996) not read'.")
row("L07-L08-grade-L08", "2.3-grade", "L08.html key-results table (lines 562-568)", P,
    PIN + "T for definitions and proofs; C for the constants (UNCONFIRMED, one secondary page); D for the -1.78 threshold; C for the registry row. Matches the brief's ruling (1).")
row("L07-L08-struct-sections", "2.9-structure", "L07.html, L08.html", P,
    PIN + "both pages have sections 1-10 with ids s1-s10, a Lab 1 inside §1, misconceptions, problem set (M, P, E, R tiers), key results, quiz, references.")
row("L07-L08-struct-counts", "2.9-structure", "L07.html, L08.html", P,
    PIN + "L07: 3 mechanics, 3 proof, 3 empirical, 3 research problems; 10 quiz items. L08: the same tiers; 10 quiz items.")
row("L07-L08-struct-banned-phrases", "2.9-structure", "L07.html, L08.html (case-insensitive scan)", P,
    PIN + "grep: no 'roughly', 'historically', 'typically', 'usually', 'as much as', 'U.S.', 'builder', 'this build', 'REQUEST', 'unit report', 'brief', 'round'. 'about' occurrences are shown-calculation or content words ('about 35' with 34.8 computed at L08 534; 'about 0.09' quiz option). The '...' in L07 lines 162 and 249 are Python tuple types inside lab code.")
row("L07-L08-struct-uses-metadata", "2.9-structure", "L08.html line 38 ('Uses') and L07.html line 38", P,
    PIN + "Uses lists resolve (page_smoke, check_pages PASS); L08 introduces the M-score (defined §1).")
row("L07-L08-dag-check_dag", "DAG", "tools/check_dag.py --all (AC2)", P,
    PIN + "check_dag AC2: PASS.")
row("L07-L08-dag-order", "DAG", "L07.html, L08.html uses and concept links", P,
    PIN + "L07 uses financial-ratio-analysis (L02), accruals (L04); L08 uses piotroski-f-score (L07), accruals (L04), depreciation-and-amortization (concepts). No concept is used before its defining module.")
row("L07-L08-hours", "2.9-structure", "L07.html data-hours=10; L08.html data-hours=12; index.html data-hours-lessons=76", P,
    PIN + "declared lesson hours L01 9, L02 10, L03 8, L04 9, L05 8, L06 10, L07 10, L08 12 sum to 76 (index data-hours-lessons=76); project 34; total 110. My own estimate: L07 9-11 h, L08 10-13 h; both declared values fall inside +/-30%.")
row("L07-L08-cards-L07-A", "2.7-cards", "cards.json AC2-c089 to AC2-c101 (lesson L07)", P,
    PIN + "each card read against its lesson line: c093 (buyback example, §2 item 2), c094 (tags, §2), c095 (p. 7), c096 (p. 11), c097 (Abstract p. 1; p. 11 sample period), c098 (Abstract p. 1; p. 3), c099 (Sloan attribution, C), c100 (p. 9 n. 5), c101 (p. 7 n. 2). c089-c092 are definitional (no grade field, noted, not failed).")
row("L07-L08-cards-L07-B", "2.7-cards", "cards.json AC2-c130 (L07); c102-c105, c126, c127 checked and correct", F,
    PIN + "AC2-c130 back reads 'Six conditions (s1 to s6, s8, s9) match the paper's definitions'. The parenthesis lists eight signals (s1, s2, s3, s4, s5, s6, s8, s9); L07 line 90 and key-results line 428 say eight. Cards c102 (F=8), c103 (F=2 example), c104, c105, c126 (1,448/396), c127 (F=7 loss example) are correct.",
    fix="cards.json AC2-c130: change 'Six conditions' to 'Eight conditions'.")
row("L07-L08-cards-L08-A", "2.7-cards", "cards.json AC2-c106 to AC2-c115 and AC2-c129 (lesson L08); AC2-c107 under its own row", P,
    PIN + "c106, c108-c115, c129 checked: c109 (D, no cut-off as a rule), c110-c112 (T, proofs), c113-c114 (C, Lab 1 base-rate table: 0.0917; PPVs below 0.1 at prevalence 0.001 for specificities up to 0.95), c117 (medians -2.4747 / -1.5067, matching output), c108 (registry title/journal/volume/issue/pages). c107 is FAILED under row L07-L08-r5-card-c107-jstor.")
row("L07-L08-cards-L08-B", "2.7-cards", "cards.json AC2-c116, AC2-c117, AC2-c118, AC2-c119", P,
    PIN + "c119 now says TATA 'divides by year-end total assets, where the L04 measure divides by average total assets'; checked against L04.html accruals_cash_flow ('(NI - CFO) / average total assets') and contract accruals_cash_flow. c116, c117, c118 match L08 §4-§5.")
row("L07-L08-cards-coverage", "2.7-cards", "cards.json (L08 cards) vs Definition 4.1 (lines 99-102)", P,
    PIN + "L08 cards cover Definition 4.1 terms (sensitivity c131, specificity c132, prevalence c129, screen c133, PPV c139, AND/OR c140), Propositions 4.2-4.3, the constants, the threshold and the growth and accrual confounds.")
row("L07-L08-cards-dupes", "2.7-cards", "cards.json all 140 AC2 cards (c001-c140)", P,
    PIN + "normalised duplicate scan of fronts and backs over 140 cards: no duplicates (ledgers/AC2/scripts/L07-L08-r5/ and logs). Card ids c001-c140 are unique.")
row("L07-L08-rubric-or-project", "2.6-project", "not applicable (no project in this slice)", P,
    PIN + "L07 and L08 contain no project grader; the project page is outside this slice.")
row("L07-L08-r2-us-claim", "2.1-citation", "L07.html line 104 and whole page (no 'U.S.')", P,
    PIN + "grep 'U\\.S\\.' in L07.html and L08.html: 0 hits.")
row("L07-L08-r2-uncited-assertions", "2.9-structure", "L08.html line 52 (why-it-matters lead)", P,
    PIN + "lead states the contract's definition and that constants are unconfirmed; no uncited figure.")
row("L07-L08-r2-paper-design-claim", "2.1-citation", "L08.html lines 97 and 474", P,
    PIN + "line 97: 'The paper's classification threshold and sample description are not stated here'; line 474: 'The paper's sample design is not confirmed'. No paper design is asserted.")
row("L07-L08-r2-constants-provenance", "2.1-citation", "course/modules/AC/AC2/L08.html line 93 (and key-results row 566)", F,
    PIN + "Wikipedia 'Beneish M-score' (200, plain curl; scratch /tmp/ac2-v/L07-L08-r5/wiki.txt): 'The formula to calculate the M-score is: [1]' (reference 1 = Messod D. Beneish, 'The Detection of Earnings Manipulation', Scribd); 'The Beneish M-score is calculated using 8 variables (financial ratios): [1] [2]' (reference 2 = ycharts.com). So ycharts is cited for the eight-variable list, not for the coefficient formula. Line 93 says the coefficient formula is cited to Scribd 'and to a ycharts.com page'.",
    fix="L08.html line 93: 'The page cites its coefficient formula to an undated Scribd document ... and cites that document and a ycharts.com page for its list of eight variables; neither gives a journal locator.'")
row("L07-L08-r2-balance-sheet-accrual", "2.4-math", "L08.html line 477 ('Accruals are measured twice' bullet)", P,
    PIN + "the r4 failure is fixed: TATA numerator matches accruals_cash_flow (NI - CFO); denominator is year-end TA (TATA definition line 85 and contract), while accruals_cash_flow divides by average TA (contract line 111-112 and L04 line 'accruals_cash_flow').")
row("L07-L08-r2-def41-before-use", "2.9-structure", "L08.html Definition 4.1 (lines 99-102) vs lab hypothesis (line 106) and first use", P,
    PIN + "Definition 4.1 (line 100) precedes the first use of PPV in the lab hypothesis (line 106, which points back to it); line 52 uses 'false-positive rate' and 'Proposition 4.2' in the lead before their definitions: plain-language lead, not a defined-term use, noted.")
row("L07-L08-r2-lab-L08-table-claim", "2.5-lab", "lab-AC2-L08-1 hypothesis (line 106)", P,
    PIN + "run: 'section 4 check: PPV at prevalence 0.01, specificity 0.95 = 0.0917; ... True'.")
row("L07-L08-r2-threshold-row", "2.3-grade", "L08.html key-results row (line 567)", P,
    PIN + "row grades the -1.78 threshold D; Wikipedia gives -1.78 (verified above); the lesson states no rule from it.")
row("L07-L08-r2-wiki-constants", "2.1-citation", "L08.html lines 93, 95, 97; lab docstring lines 114-118; lab constants lines 133-144", P,
    PIN + "all nine values equal the Wikipedia equation: -4.84; 0.92 DSRI, 0.528 GMI, 0.404 AQI, 0.892 SGI, 0.115 DEPI, -0.172 SGAI, -0.327 LVGI, 4.679 TATA (verified in wiki.txt).")
row("L07-L08-r2-jstor-statement", "2.1-citation", "L07.html line 104 ('The JSTOR record ... could not be read (bot check)')", P,
    PIN + "JSTOR stable/2672906 (Piotroski DOI) returns a 'Client Challenge' page with JavaScript disabled message (HTTP 200); the statement is accurate for that record.")
row("L07-L08-r2-process-words", "2.9-structure", "L07.html, L08.html (case-insensitive)", P,
    PIN + "no builder, build, REQUEST, unit report, brief, round or agent in learner text (grep).")
row("L07-L08-r2-lab-numbering", "2.9-structure", "L07.html, L08.html lab headings and text", P,
    PIN + "'Lab 1 · ...' on each page (L07 line 113, L08 line 105); no other lab numbering.")
row("L07-L08-r2-links", "2.9-structure", "L07.html and L08.html internal and concept links", P,
    PIN + "check_pages and page_smoke PASS; the L07 §5 and L08 §5 open-item references are plain code text, not links.")
row("L07-L08-r2-bayes-S1-and-total-probability", "DAG", "L08.html line 455 (Bayesian inference link), Proposition 4.2 proof (line 452)", P,
    PIN + "the Bayesian inference concept link resolves (check_pages); the proof uses Bayes' rule and total probability, both stated in the proof.")
row("L07-L08-r2-quiz-keys", "2.4-math", "L07.html quiz (lines 444-518), L08.html quiz (lines 575-655)", P,
    PIN + "L07 keys: q1 CFO>NI (P1), q2 0.10636 (117/1100), q3 high BM 1976-1996, q4 8, q5 common factor, q6 possibly 0 (P3), q7 equity signal, q8 1976-1996 C result, q9 7, q10 cutoffs a choice. L08 keys: q1 about 0.09, q2 0.0917, q3 0.0050, q4 at most the smaller, q5 -1.5593 (unconfirmed), q6 linear combination, q7 DSRI, q8 low prevalence, q9 generator, q10 higher. Each key re-derived.")
row("L07-L08-r3-piotroski-fetch", "2.1-citation", "Piotroski (2000) Ivey-hosted PDF (https://www.ivey.uwo.ca/media/3775523/value_investing_the_use_of_historical_financial_statement_information.pdf)", P,
    PIN + "plain curl: HTTP 200, application/pdf, 876,917 bytes; sha256 901d713553ddaf5b3cf60475d3a90aeaff5f584a6ceb2d0d33fd918ebed1b4e5, identical to the round-4 copy.")
row("L07-L08-r3-quotes", "2.1-citation", "L07.html claim quotations (lines 98, 102, 341) and page locators", P,
    PIN + "the quotations at lines 98, 102 and 341 match the PDF text (pp. 7, 7 and 9).")
row("L07-L08-r3-wiki-fetch", "2.1-citation", "Wikipedia 'Beneish M-score' (https://en.wikipedia.org/wiki/Beneish_M-score), plain curl", P,
    PIN + "HTTP 200 (98,385 bytes); equation, threshold -1.78 and reference list (Scribd, ycharts.com, Beneish, Lee and Nichols 2013, Beneish and Vorst 2020) as cited above.")
row("L07-L08-r3-access", "2.1-citation", "L08.html line 93 access statuses", P,
    PIN + "statuses re-run this round (see L07-L08-loc-access-claims-L08).")
row("L07-L08-r3-recompute-L07", "2.2-numbers", "L07.html Lab 1 output, §4, M1-M3, E1-E3, P3", P,
    PIN + "Fraction recomputation of §4, M1-M3, E1-E3 and P3 reproduces every printed value.")
row("L07-L08-r3-recompute-L08", "2.2-numbers", "L08.html Lab 1 output, §3 worked M, base-rate table, E1-E3, AND/OR", P,
    PIN + "recompute.py and recompute2.py reproduce the §3 indices (1.5, 1.1429, 1.0833, 1.2, 1.0909, 1.0, 0.9792, 0.0333), M, the base-rate table and the AND/OR rates.")
row("L07-L08-r3-contract-departures", "2.1-citation", "atlas/A15.contract.md 'Departures from the published definitions' vs L07 §2", P,
    PIN + "the contract text lists the three departures with the same page locators (pp. 7-8 and p. 9, p. 8) that L07 §2 uses.")
row("L07-L08-r3-registry-no-fscore-study", "2.1-citation", "references/references.json (560 entries)", P,
    PIN + "entries matching Piotroski, F-score, fundamental analysis, Mohanram, Beneish, Sloan: only piotroski2000value, beneish1999detection, sloan1996stock, dechow1995detecting (no out-of-sample F-score study).")
row("L07-L08-r3-open-items-content", "2.1-citation", "plans/AC2-open-items.md (rows 16-19, 24-26)", P,
    PIN + "rows exist for Beneish constants, Mohanram (from recall, OPEN), Dechow et al. 2011 and Beneish, Lee & Nichols 2013 (from recall, OPEN), dechow1995detecting author question, out-of-sample tests, joint use.")
row("L07-L08-r3-from-recall-L07", "2.9-structure", "L07.html (no 'Mohanram' or 'recall' in learner text)", P,
    PIN + "grep: 0 hits for 'Mohanram' or 'recall' in L07.html. Line 344 names only the open-items file. The round-4 evidence quoted text no longer on the page; the current text complies with the ruling.")
row("L07-L08-r3-from-recall-L08", "2.9-structure", "L08.html (no 'Dechow', 'Lee', or 'recall' in learner text)", P,
    PIN + "grep: 0 hits for 'Dechow', 'Lee', 'Nichols', 'Vorst' and 'recall' in L08.html (and 0 'Dechow' in L07.html); the 2011 and 2013 works appear only in the open-items file (row 18-19).")
row("L07-L08-r3-stock-funded-example", "2.1-citation", "L07.html §2 item 2 (line 94)", P,
    PIN + "stock-split example consistent with EQOFFER 'did not issue common equity'; buyback example consistent with s7 'did not rise'.")
row("L07-L08-r3-lab-checks-integer", "2.5-lab", "L07.html line 110 and hypothesis line 114", P,
    PIN + "lab checks only invariance under x1000 (400/400); the range 0 to 9 is stated as coming from the definition (P2), not from the lab.")
row("L07-L08-r3-lab-docstring-pages", "2.1-citation", "lab-AC2-L07-1 docstring (line 120)", P,
    PIN + "docstring reads 'pp. 7-10 (printed pages)'. Round 4 quoted 'pp. 8-10'; the current text is correct because the signals are defined on pp. 7-10 (ROA p. 7; accrual and leverage p. 8; ATURN and EQOFFER p. 9; composite p. 10).")
row("L07-L08-r3-period-7.5", "2.1-citation", "L07.html line 104 claim span ('both for 1976 to 1996'); key-results rows (lines 432-433); card AC2-c097", P,
    PIN + "7.5% (abstract p. 1, 'at least 7.5% annually') and 23% (p. 1 and p. 3, 1976-1996); the sample period is p. 11. Graded C.")
row("L07-L08-r3-R2-track-growth", "2.4-math", "L08.html R2 solution (line 549)", P,
    PIN + "solution proposes growth terciles and an independence test; consistent with §4-§5.")
row("L07-L08-r3-signs-of-improvement", "2.4-math", "L08.html §4 paragraph (line 443)", P,
    PIN + "line 443 now states s1, s2 sign tests at zero, s4 same-year comparison, s3 and s5-s9 change tests; matches L07 line 86 and §5.")
row("L07-L08-r3-margin-overlap", "2.4-math", "L08.html §4 paragraph (line 466)", P,
    PIN + "line 466: F-score ROA and CFO scaled by beginning-of-year TA; TATA, AQI and LVGI by year-end TA. Verified against L07 line 65, L08 lines 80-84 and the contract. The round-4 'same base' wording is gone.")
row("L07-L08-r3-eight-year-on-year", "2.9-structure", "L08.html why-it-matters (line 52)", P,
    PIN + "'eight ratios, seven of them year-on-year': matches index definitions (lines 78-85), TATA the only single-year index.")
row("L07-L08-r3-weights-only-source", "2.3-grade", "L08.html line 89 (features) and line 93", P,
    PIN + "the constants come from one secondary page (lines 93, 97); line 89 says the intercept and weights 'depend on the source'.")
row("L07-L08-r3-used-in-lab-only", "2.3-grade", "L08.html line 95", P,
    PIN + "line 95 says 'used only to show the arithmetic ... in the lab, in the §3 worked M, in misconception 2 and in quiz item 5'. Also used in E1 (line 530), whose solution labels them unconfirmed; the list covers lab output, so it is not contradicted. Recorded as a scope note in L07-L08-r5-used-only-scope.")
row("L07-L08-r3-PPV-before-defined", "2.9-structure", "L08.html lab hypothesis (line 106) and table header (line 373); Proposition 4.2 (line 447)", P,
    PIN + "Definition 4.1 (line 100) defines PPV before the lab; Proposition 4.2 gives the formula.")
row("L07-L08-r3-as-much-as", "2.4-math", "L08.html §4 paragraph (line 468 region)", P,
    PIN + "grep 'as much as': 0 hits in L07 and L08. The §4 sensitivity sentence now reads 'at most that of either screen' (P3).")
row("L07-L08-r3-lab-docstring-follows-beneish", "2.1-citation", "lab-AC2-L08-1 docstring lines 110-112", P,
    PIN + "the phrase 'which follow Beneish (1999)' is no longer in the docstring; it now says the index definitions are the contract's and 'the paper's own definitions were not read'. Consistent.")
row("L07-L08-r3-prop-4.2-page-locator", "2.4-math", "L08.html lines 54-56 and §3 'Two things' (line 439)", P,
    PIN + "line 56 gives the registry locator (pages 24-36) and says the table is unconfirmed; line 439 explains TATA and DSRI as shown in §3. Proposition 4.2 is a derivation, not a page-cited claim.")
row("L07-L08-r4-signals-match-claim", "2.1-citation", "L07.html key-results row 1 (line 428) and §2 lead (line 90)", P,
    PIN + "rows now say conditions match for s1-s6, s8, s9 and s7 is a share-count proxy (§2 item 2). Checked against PDF pp. 7-9: ROA>0, CFO>0, ΔROA (p. 7-8 AROA), ACCRUAL (p. 8), ΔLEVER (p. 8), ΔLIQUID (p. 9), ΔAMARGIN and ΔATURN (p. 9). The round-4 failure is fixed.")
row("L07-L08-r4-eqoffer-p9", "2.1-citation", "L07.html line 94 (§2 item 2); paper PDF p. 9", P,
    PIN + "PDF p. 9: 'I define the indicator variable EQOFFER as equal to one if the firm did not issue common equity in the year preceding portfolio formation'.")
row("L07-L08-r4-wiki-threshold-cite", "2.1-citation", "course/modules/AC/AC2/L08.html line 97", P,
    PIN + "Wikipedia's threshold citation is 'see Beneish 1999, Beneish, Lee, and Nichols 2013, and Beneish and Vorst 2020' with no page; line 97 reports exactly that.")
row("L07-L08-r4-pdf-printed-pages", "2.1-citation", "Piotroski (2000) PDF running headers pp. 1-14 (and pp. 16-17)", P,
    PIN + "running headers 'VALUE INVESTING n' / 'n JOSEPH D. PIOTROSKI' map each PDF page index to its printed page (checked pp. 1-20).")

# Round-5 rows
row("L07-L08-r5-card-c107-jstor", "2.7-cards", "cards.json AC2-c107 (id at line 772; back field follows)", F,
    PIN + "AC2-c107 back: 'The paper could not be read: the publisher, ResearchGate and SSRN returned HTTP 403, and the JSTOR record did not load.' The paper is Beneish (1999). L08 line 93 attributes the JSTOR client challenge to the companion Piotroski paper (JSTOR 2672906, verified), and records no JSTOR attempt for Beneish.",
    fix="cards.json AC2-c107: replace 'and the JSTOR record did not load' with 'and the JSTOR record of the companion Piotroski paper returned a client challenge'.")
row("L07-L08-r5-used-only-scope", "2.3-grade", "L08.html line 95 ('used only ... in the lab, in the §3 worked M, in misconception 2 and in quiz item 5')", P,
    PIN + "the list omits E1 (line 530), which reads the lab's candidate-constant medians and labels them unconfirmed. Scope note only: E1 reads lab output, the list names 'the lab', and the E1 solution states the label. Not failed.")
row("L07-L08-r5-E1-label", "2.3-grade", "L08.html E1 solution (line 530)", P,
    PIN + "E1 solution: 'the constants are unconfirmed, so the gap is in arithmetic units under candidate weights' (labelled).")

NOTES = (
    "Round 5 (pin 11b3477), slice L07-L08, verifier fresh from round 4. Delta read hunk by hunk: L07.html (lines 86, 90, 341, 352, 428), "
    "L08.html (lines 93, 97, 466, 477), cards.json (c059, c065 are L04/L05 cards outside this slice; c103, c107, c119, c130 in this slice, c123 and c134 outside). "
    "Twins lab-AC2-L07-1.py and lab-AC2-L08-1.py are unchanged since 2607c60 but were re-run this round. Every page was re-read in full (L07 536 lines, L08 673 lines). "
    "No row was carried: the page files changed, so every page-level row was re-verified. Scripts: ledgers/AC2/scripts/L07-L08-r5/ (recompute.py, recompute2.py, make_fragment_r5.py); logs: same folder. "
    "Scratch: /tmp/ac2-v/L07-L08-r5/ (Wikipedia and PDF copies, JSTOR and DOI responses). "
    "FAIL rows: L07-L08-cards-L07-B (c130 says 'Six' for eight conditions), L07-L08-r2-constants-provenance (ycharts cited for the coefficient formula; it is cited for the variable list), L07-L08-r5-card-c107-jstor (JSTOR attribution). "
    "Fixed since round 4: L07-L08-misconception-score-zero, L07-L08-r2-balance-sheet-accrual, L07-L08-r3-margin-overlap, L07-L08-r4-signals-match-claim. "
    "Not checkable: Sloan (1996) passage (paper not read; the lesson says so); Beneish (1999) table and constants (paper unreachable: UNVERIFIABLE by the brief's rule; labelled UNCONFIRMED throughout). "
    "ResearchGate and SSRN statuses were checked on URLs built for this check and returned 403; the page's claim is a statement about access, not about a specific record."
)

frag = {
    "unit": "AC2",
    "slice": "L07-L08",
    "round": 5,
    "verifier": "round-5 independent verifier for slice L07-L08 (did not build AC2; shares no context with the builders or earlier verifiers)",
    "pin": "11b3477",
    "base": None,
    "previous_ledger": "round 4, pin 2607c60: 112 rows, 106 PASS, 6 FAIL (overwritten by this round's fragment)",
    "checkout": "/tmp/verify-ac2r5-l78 (detached worktree at 11b3477; .venv symlinked)",
    "scratch": "/tmp/ac2-v/L07-L08-r5",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": "FAIL",
    "mutants": [],
    "registry_flags": [
        "beneish1999detection: registry verifies title, journal, volume 55, issue 5, pages 24-36 (Crossref). Model content (intercept, eight weights, cut-offs) is not verified; the page labels them UNCONFIRMED. The -1.78 threshold and every constant come from one secondary web page (Wikipedia), whose coefficient formula is cited to an undated Scribd copy and whose eight-variable list is cited to Scribd and ycharts.com."
    ],
    "freshness_flags": [],
    "notes": NOTES,
}
frag["rows"] = R
frag["summary"] = {
    "rows": len(R),
    "pass": sum(1 for r in R if r["status"] == P),
    "fail": sum(1 for r in R if r["status"] == F),
    "unverifiable": sum(1 for r in R if r["status"] == U),
}
problems = ledger.validate(frag, "L07-L08")
print("validate problems:", problems)
out = "ledgers/AC2/L07-L08.json"
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", out, frag["summary"])
