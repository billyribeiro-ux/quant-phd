"""Writes ledgers/AC2/L07-L08.json (verifier round 1, slice L07-L08). Rows reflect the checks run in this checkout."""
import json
from datetime import UTC, datetime

R = []


def row(id_, check, location, status, evidence, fix=None):
    d = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix or ""
    R.append(d)


CMD = "ledgers/AC2/scripts/L07-L08-r1/recompute.py"
row("L07-L08-cmd-pin", "2.9-structure", "repository",
    "PASS", "git -C /tmp/verify-ac2-l78 log -1 --oneline -> 0c14083 (AC2: labs run in the browser). git status: only untracked .venv symlink. No edits to course, tests, references, curriculum or atlas files.")
row("L07-L08-cmd-run_labs", "2.5-lab", "tools/run_labs.py --unit AC2",
    "PASS", ".venv/bin/python tools/run_labs.py --unit AC2 (Python 3.14.8) -> 'run_labs AC2: PASS (11/11)', exit 0. Output saved at /tmp/ac2-v/L07-L08/run_labs.txt.")
row("L07-L08-cmd-twins", "2.5-lab", "tests/labs/AC2/lab-AC2-L07-1.py, lab-AC2-L08-1.py",
    "PASS", "python -I -W error on each twin: exit 0 for both, stderr 0 bytes. stdout equals the page's expected block for each lab (compared line by line with a script; no diff).")
row("L07-L08-cmd-embed", "2.5-lab", "course/modules/AC/AC2/L07.html, L08.html (data-run blocks)",
    "PASS", "Embedded <code> text equals the twin source (strip-compared) for both labs: L07 6202 chars vs twin 6203, L08 10440 vs 10441 (trailing newline only).")
row("L07-L08-cmd-page_smoke", "2.9-structure", "tools/page_smoke.py --unit AC2 --pages L07 L08",
    "PASS", ".venv/bin/python tools/page_smoke.py --unit AC2 --pages L07 L08 -> 'page_smoke modules/AC/AC2/L07.html: PASS', 'page_smoke modules/AC/AC2/L08.html: PASS', 'page_smoke AC2: PASS', exit 0. Lab timings: lab-AC2-L07-1 0.0 s, lab-AC2-L08-1 0.0 s after 1.1 s runtime boot. Log: /tmp/ac2-v/L07-L08/page_smoke.txt.")
row("L07-L08-cmd-check_pages_dag_projects", "2.9-structure", "tools/check_pages.py, check_dag.py, check_projects.py --unit AC2",
    "PASS", "'check_pages AC2: PASS' (exit 0); 'check_dag AC2: PASS' (exit 0); 'check_projects AC2: PASS' (exit 0).")
row("L07-L08-cmd-lint_mypy", "2.5-lab", "the two twins",
    "PASS", ".venv/bin/ruff check and ruff format --check on both twins: 'All checks passed!', '2 files already formatted'. .venv/bin/mypy --no-incremental on both: 'Success: no issues found in 2 source files'. Repo-wide ruff/mypy not run (outside the slice).")
row("L07-L08-cmd-pytest", "2.5-lab", ".venv/bin/pytest -q -k 'AC2 or ac2 or lab or card'",
    "PASS", "The selection ran to 100% with no failures (output shows only progress dots, no F or E). The test count and exit code were not captured.")
row("L07-L08-cmd-verify_refs", "2.1-citation", "tools/verify_refs.py --unit AC2 (live) and --offline",
    "PASS", "'live re-verification of AC2: 5 of 560 entries, 0 problems', exit 0. 'offline integrity: 560 entries, 0 problems', exit 0.")

row("L07-L08-cite-piotroski2000value", "2.1-citation", "references/references.json key piotroski2000value; L07 data-cite",
    "PASS", "Registry: Crossref-verified, Piotroski (2000) 'Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers', Journal of Accounting Research 38 (Supplement). Live verify_refs passes. Attribution read: publicly hosted copy at https://www.ivey.uwo.ca/media/3775523/value_investing_the_use_of_historical_financial_statement_information.pdf (HTTP 200, application/pdf, 876,917 bytes, pdftotext extracted, printed pages match PDF pages 1-41). The JSTOR record was not read: jstor.org/stable/2672906 returns a JavaScript client challenge page (HTTP 200, body 'Client Challenge').")
row("L07-L08-cite-sloan1996stock", "2.1-citation", "references/references.json key sloan1996stock; L07 claim span line 108",
    "PASS", "Registry verified live (Sloan 1996, The Accounting Review 71(3), 289-315). Attribution claim is what Piotroski p. 8 says: 'Sloan [1996] shows that earnings driven by positive accrual adjustments (i.e., profits are greater than cash flow from operations) is a bad signal about future profitability and returns' (pdftotext, PDF p. 8). Sloan itself not read, as the page says.")
row("L07-L08-cite-beneish1999detection", "2.1-citation", "references/references.json key beneish1999detection; L08 data-cite",
    "PASS", "Registry verified live: Beneish (1999) 'The Detection of Earnings Manipulation', Financial Analysts Journal, vol 55, issue 5, pages 24-36, DOI 10.2469/faj.v55.n5.2296. The registry verifies title, journal, volume, issue and pages only; its model content is not verified (the page says so, grade C). CFA Institute research page (rpc.cfainstitute.org, HTTP 200) shows the abstract and states the full article is members-only; it gives no coefficients.")

row("L07-L08-loc-p1-p3-7.5-23", "2.2-numbers", "L07.html lines 104 and 432-433; claim span 'Abstract, p. 1; p. 3'",
    "PASS", "pdftotext of Ivey copy: p.1 'mean return earned by a high book-to-market investor can be increased by at least 7.5% annually through the selection of financially strong high BM firms' and '...generates a 23% annual return between 1976 and 1996'; both repeated on p.3 (same wording). Locators and figures match.")
row("L07-L08-loc-p12-1448-396", "2.2-numbers", "L07.html line 106; claim span 'p. 12 (1,448 and 396 observations); p. 12, bootstrap design'",
    "PASS", "pdftotext p.12: 'number of observations equals 1,448 and 396, respectively' (high = FSCORE 8 or 9; low = 0 or 1, p.12). Bootstrap pseudo-portfolio design on p.12. Corroborated on p.16 ('1,448 observations ... 396 observations').")
row("L07-L08-loc-p7-n2-optimal", "2.2-numbers", "L07.html line 98; claim span 'p. 7, n. 2'",
    "PASS", "Footnote 2 on p.7, read in the rendered page image (pdftoppm -r 110 page 7, /tmp/ac2-v/L07-L08/src/pg-07.png): 'Statistical techniques such as factor analysis may more aptly extract an optimal combination of signals, but such an approach has costs in terms of implementability.' The page quote matches exactly.")
row("L07-L08-loc-p9-n5-cutoff", "2.2-numbers", "L07.html line 341; key-results line 435; card AC2-c100",
    "PASS", "Footnote 5 on p.9, rendered page image: 'A specification where the current ratio cutoff equals 1.5 yields stronger return results than the liquidity metric and aggregate score used in the paper.' Page quote matches; the paper gives it in a footnote, as the page says.")
row("L07-L08-loc-p7-ex-ante-quote", "2.2-numbers", "L07.html line 102; claim span 'the stated ex ante implication ... financially distressed'",
    "FAIL", "pdftotext p.7 and rendered image: the sentence reads 'the stated ex ante implication of each signal is conditioned on the fact that these firms are financially distressed at some level.' The page's quotation stops at 'distressed' and closes the quote, with no ellipsis. The quoted words are accurate but the quotation is truncated.",
    "Quote the full sentence through 'at some level', or end the quote with an ellipsis that marks the omission.")
row("L07-L08-loc-p7-distress-average", "2.2-numbers", "L07.html line 102 (sentence 'High book-to-market firms are on average financially distressed, and a rise in leverage...(p. 7)')",
    "FAIL", "The sentence 'The average high BM firm is financially distressed' is on p.6 (section 2.3 opening, pdftotext PDF page 6). The leverage clause ('the negative implications of increased leverage seem more plausible than the benefits garnered through a reduction of agency costs') is on p.7, verified in the rendered image. The page cites p.7 for the whole sentence.",
    "Cite 'p. 6' for the distress sentence and 'p. 7' for the leverage clause.")
row("L07-L08-loc-keyresults-2.3", "2.1-citation", "L07.html key-results row 1 (source 'Piotroski (2000), §2.3, pp. 7–10')",
    "FAIL", "Section 2.3 heading 'FINANCIAL PERFORMANCE SIGNALS USED TO DIFFERENTIATE HIGH BM FIRMS' is on p.6 (pdftotext PDF page 6). The nine signal definitions run pp.7-9 (2.3.1 on p.7, 2.3.2 on p.8, 2.3.3 on p.9), and the F-score formula is on p.10.",
    "Change the locator to 'Piotroski (2000), §2.3, pp. 6–10'.")
row("L07-L08-loc-signal-groups", "2.1-citation", "L07.html lines 86 and 50-90 (groups and definitions)",
    "PASS", "pdftotext: 2.3.1 Profitability on p.7; 2.3.2 'Leverage, Liquidity, and Source of Funds' heading on p.8 (matches 'source-of-funds heading is on p. 8'); 2.3.3 Operating Efficiency on p.9; F-SCORE sum with the nine signals in the same order on p.10.")
row("L07-L08-loc-scaling-p7-p8-p9", "2.1-citation", "L07.html line 65",
    "PASS", "p.7: ROA and CFO 'scaled by beginning-of-the-year total assets'; p.8: ACCRUAL and leverage: ALEVER uses 'total long-term debt to average total assets'; p.9: ATURN uses 'total sales scaled by beginning-of-the-year total assets'. Locators pp.7, 8, 9 match the sentence as written.")
row("L07-L08-loc-proxies-p7-p8-p9", "2.1-citation", "L07.html §2 items 1-3 (lines 93-95)",
    "PASS", "p.7: ROA/CFO 'as net income before extraordinary items'; p.9: 'EQ_OFFER ... equal to one if the firm did not issue common equity in the year preceding portfolio formation'; p.8: leverage 'ratio of total long-term debt to average total assets'. The page describes each as a departure from the paper that the contract records; matches atlas/A15.contract.md lines 162-167.")
row("L07-L08-loc-p11-sample", "2.1-citation", "L07.html line 102, line 411 (R1)",
    "PASS", "p.11: 'Each year between 1976 and 1996 ... retain firms in the highest BM quintile with sufficient financial statement data'; p.11: one- and two-year buy-and-hold returns from 'the beginning of the fifth month after the firm's fiscal year-end'.")
row("L07-L08-loc-p12-groups-bootstrap", "2.1-citation", "L07.html lines 106, 419 and misconception 3",
    "PASS", "p.12: 'FSCORE equals 8 or 9' high group, 'FSCORE equals 0 or 1' low group; bootstrap of pseudo-portfolios of the same sizes (p.12).")
row("L07-L08-loc-sloan-p8", "2.1-citation", "L07.html line 108 (locator 'Piotroski p. 8, citing Sloan (1996)')",
    "PASS", "Verified above (cite-sloan1996stock): p.8 sentence attributes the 'bad signal' to Sloan (1996).")
row("L07-L08-loc-access-claims-L08", "2.1-citation", "L08.html line 93 ('The publisher page, the DOI resolver, ResearchGate and SSRN each returned HTTP 403 ... JSTOR ... bot check')",
    "FAIL", "Observed 2026-10-27 with plain curl: https://doi.org/10.2469/faj.v55.n5.2296 returns HTTP 302 to https://www.tandfonline.com/doi/full/10.2469/faj.v55.n5.2296, which returns HTTP 403 (so the 403 comes from the publisher, not the resolver). https://www.researchgate.net 403; https://papers.ssrn.com 403. JSTOR (jstor.org/stable/2672906) returns a JavaScript client challenge (consistent with 'bot check'). The sentence's HTTP-status attribution for the DOI resolver is inaccurate.",
    "Write: 'the DOI resolver redirects to the publisher, which returns HTTP 403'.")
row("L07-L08-loc-beneish-constants-label", "2.1-citation", "L08.html lines 56, 60, 87, 89, 93-99, 417-423, 552-558, 599; lab docstring and output; cards AC2-c107, c117",
    "PASS", "Paper unreachable from this build, confirmed: tandfonline 403 (above); CFA full article members-only (rpc.cfainstitute.org page: 'This is available to the following CFA Institute membership classes'); no coefficients shown there. The page labels the intercept and eight weights UNCONFIRMED at grade C in §2, the claim span (line 95), the key-results row 556 and the lab output ('M (UNCONFIRMED constants)'). Source-by-source: Wikipedia (secondary, 2026-10-27) gives intercept -4.84 and weights 0.92, 0.528, 0.404, 0.892, 0.115, -0.172, -0.327 and TATA 4.679 (matching the page). This is not confirmation and the page does not treat it as such.")
row("L07-L08-beneish-published-wording", "2.3-grade", "L08.html line 60 (Definition 1.1: 'the published constants of §2'); key-results row 552 (grade T: 'with published constants')",
    "FAIL", "Two places describe the constants as 'published' without the UNCONFIRMED label. The definition (line 60) and the T-graded key-results row (552) present them as established. Elsewhere on the page they are labelled unconfirmed (§2, line 95, row 556). The T-graded row 552 is a definitional claim, but the word 'published' implies a source the build did not read.",
    "In Definition 1.1 write 'the constants of §2 (unconfirmed in this build)'. In row 552 drop 'with published constants' or add 'UNCONFIRMED'.")
row("L07-L08-beneish-tata-disagreement", "2.1-citation", "L08.html line 93 ('a TATA weight of 4.679 or 4.697, since two sources disagree'); lab docstring lines 108-111",
    "FAIL", "4.679 shown in Wikipedia (https://en.wikipedia.org/wiki/Beneish_M-score, HTTP 200, formula line). The 4.697 figure has no page I could open: the search-result summary says a MarketXL article gives 4.697, but curl cannot resolve marketxl.com (exit 6, DNS) with or without www. The page names no sources for the disagreement. The disagreement is therefore unverifiable from this build.",
    "Name the two secondary sources with URLs and retrieval date, and state which value each shows; or remove 4.697 until a source is read.")
row("L07-L08-beneish-cutoffs", "2.1-citation", "L08.html line 97 ('one source gives -1.78 ... another gives -2.22')",
    "FAIL", "-1.78 appears on Wikipedia as the threshold for the eight-variable model (HTTP 200, 'The threshold value is -1.78'). The -2.22 figure is attributed to a 2026 SSRN paper in a search summary only; papers.ssrn.com returns HTTP 403 and was not read. The page names neither source.",
    "Name each source with URL and retrieval date, or drop the -2.22 statement until it is read.")
row("L07-L08-build-report-refs", "2.1-citation", "L07.html §5 bullet 'Out-of-sample evidence ... recorded in the build report as a reference request'; L08.html §5 'That evidence is a reference request (see the build report)'",
    "UNVERIFIABLE", "No build report with these requests is in the checkout. grep of plans/ and ledgers/ finds no F-score or M-score reference request (plans/reference-queue-research-2026-10-27.md, plans/AC2-build-plan.md lines 15, 55-56 only). The pages' statements about the build report cannot be checked.",
    "Add the reference requests to the build report (REFERENCE_REQUESTS) and cite the file, or remove the sentences.")

row("L07-L08-math-signals-vs-contract", "2.4-math", "L07.html lines 56-86 (ratios, Definition 1.1, table); atlas/A15.contract.md lines 137-143",
    "PASS", "Each of the nine conditions matches the contract: ROA_t>0; CFO*_t>0; ROA_t>ROA_{t-1}; CFO*_t>ROA_t; LEV_t<LEV_{t-1}; CR_t>CR_{t-1}; Sh_t<=Sh_{t-1}; GM_t>GM_{t-1}; ATO_t>ATO_{t-1}, in order. Denominators: ROA, CFO, ATO on TA_{t-1}; LEV on average TA_t. Recomputed in ledgers/AC2/scripts/L07-L08-r1/recompute.py (worked firm and M2 signal vectors).")
row("L07-L08-math-proxies-stated", "2.4-math", "L07.html §2 (lines 90-96); contract lines 162-167",
    "PASS", "The contract names exactly three departures: NetIncomeLoss (not before extraordinary items), share-count proxy for equity issuance, LongTermDebtNoncurrent. L07 §2 states these three, labels each as the contract's choice or proxy, and says they are documentation, not errors. Consistent with the paper's p.7, p.8, p.9 wording (see the locator rows).")
row("L07-L08-math-P1", "2.4-math", "L07.html P1 (line 379-381)",
    "PASS", "Re-derived: CFO*_t > ROA_t is CFO_t/D > NI_t/D with D = TA_{t-1} > 0, equivalent to CFO_t > NI_t. The paper's ACCRUAL < 0 is the same condition (p.8). Correct.")
row("L07-L08-math-P2", "2.4-math", "L07.html P2 (line 383-385)",
    "PASS", "Re-derived: each s_i is an indicator; F is an integer in 0..9. Each ratio is money/money, so unchanged under money -> k money; share counts unchanged; comparisons preserved. Correct. Lab check 400/400 (L07 lab output) is consistent.")
row("L07-L08-math-P3", "2.4-math", "L07.html P3 (line 387-389)",
    "PASS", "recompute.py: LEV_t = 300/950 = 6/19 ~0.3158; LEV_{t-1} = 310/1050 = 31/105 ~0.2952; LEV_t > LEV_{t-1}, so s5 = 0 while LTD fell (300 < 310). Matches the page.")
row("L07-L08-math-worked-firm", "2.4-math", "L07.html §4 (lines 307-335), M1 (364-366), M2 (368-370), M3 (372-374), E2 (398-400), E3 (402-404), quiz rows 2, 4, 9",
    "PASS", "recompute.py (exact Fractions): ROA_t=117/1100; ROA_{t-1}=66/1000; CFO*_t=96/1100; LEV_t=264/1150=132/575; LEV_{t-1}=330/1050=11/35; CR 2.20 vs 2.00; GM 0.35 vs 0.30; ATO 1560/1100 vs 1320/1000; vector (1,1,1,0,1,1,1,1,1), F=8. M1 accrual 21/1100. M2 (NI=-20): (0,1,0,1,1,1,1,1,1), F=7. M3 (x1000): ROA unchanged, F=8. E2: smallest integer CFO=118 gives s4=1 and F=9. E3 (LTD=300): LEV_t=300/1150, s5=1, F=8. All printed values match.")
row("L07-L08-math-E1-count", "2.2-numbers", "L07.html E1 (line 396) and lab output",
    "PASS", "From the lab output: 24 firm-years at score 8 and 7 at score 9, total 31 of 400, 31/400 = 0.0775. Printed mean 5.6475 = 2259/400 (recompute.py). Class (a), computed by Lab 1.")
row("L07-L08-misconception-score-zero", "2.4-math", "L07.html misconception 1 (line 352): 'A firm can score 9 with poor profitability ... and 0 with strong profitability that is flat.'",
    "FAIL", "Signal 1 is 1 whenever ROA_t > 0 (contract, and L07 table row s1). A score of 0 requires s1 = 0, i.e. ROA_t <= 0, so no firm with positive profitability can score 0. The sentence as written is false.",
    "Replace with: 'A firm can score 9 with low but positive profitability that is improving, and 0 only with ROA_t <= 0 and no other signal passing.'")

row("L07-L08-math-L08-indices", "2.4-math", "L08.html lines 78-85 and the eight-index list; atlas/A15.contract.md lines 145-156",
    "PASS", "All eight definitions match the contract text: DSRI; GMI = GM_{t-1}/GM_t; AQI = a_t/a_{t-1} with a_s = 1-(CA_s+PPE_s)/TA_s; SGI; DEPI; SGAI; LVGI = ((CL_t+LTD_t)/TA_t)/(same at t-1); TATA = (NI_t-CFO_t)/TA_t. Recomputed in recompute.py.")
row("L07-L08-math-prop4.2", "2.4-math", "L08.html Proposition 4.2 and proof (lines 436-443), P1 (505)",
    "PASS", "Bayes' rule and the law of total probability are both stated and proved on the page (definition of conditional probability applied twice; two-event partition). PPV = ps/(ps+(1-p)(1-sigma)) follows. recompute.py: all nine base-rate PPVs and flag counts reproduce from the formula with exact fractions. Example 0.005/0.0545 = 10/109 = 0.0917.")
row("L07-L08-math-prop4.3", "2.4-math", "L08.html Proposition 4.3 and proof (lines 448-454), P2 (507-509)",
    "PASS", "Under independence: AND = f1 f2 = 0.005; OR = 1-(1-f1)(1-f2) = 29/200 = 0.1450 for f1 = 0.10, f2 = 0.05. Proof correct for independence among non-manipulators.")
row("L07-L08-math-L08-P3", "2.4-math", "L08.html P3 (lines 511-513)",
    "PASS", "Proof valid without independence: P(F1 and F2 | D) <= min, P(F1 or F2 | D) >= max. Checked on a joint law with b in [0, min(f1, f2)].")
row("L07-L08-math-worked-M", "2.4-math", "L08.html §3 (lines 404-423), quiz row 5, misconception 2",
    "PASS", "recompute.py: exact indices DSRI 3/2, GMI 8/7, AQI 13/12, SGI 6/5, DEPI 12/11, SGAI 1, LVGI 47/48, TATA 1/30. M with the page's candidate constants and TATA 4.679 = -1.5593 (recomputed). Labelled as arithmetic under unconfirmed constants. Information: with TATA 4.697 M = -1.5587 (not printed on the page).")
row("L07-L08-math-base-rate-table", "2.2-numbers", "L08.html lab output (lines 386-395) and lab table",
    "PASS", "recompute.py: for each prevalence {0.001, 0.01, 0.05} and specificity {0.90, 0.95, 0.99}, PPV and false flags per 1000 = 1000(1-p)FPR reproduce the printed 4-dp and 2-dp values exactly (9 of 9 rows). Class (a): computed live by the lab.")
row("L07-L08-math-E2-E3-E1", "2.4-math", "L08.html E1 (518-520), E2 (524), E3 (528)",
    "PASS", "E1: -1.5067 - (-2.4747) = 0.9680. E2: 0.3448/0.0099 = 34.8 (exact 34.79, 'about 35'). E3: 1000 x 0.99 x 0.05 = 49.5. All match.")
row("L07-L08-math-dependence-sign", "2.4-math", "L08.html §4 paragraph (line 456), misconception 3 (line 480), quiz row 10 (lines 637-645), card AC2-c116",
    "FAIL", "The page says that correlated false flags make the AND rate higher than f1 f2 and the OR rate lower, and that 'the direction of the error is known'. This holds only for positive dependence. Witness (recompute.py, joint law over F1,F2 with marginals 0.10, 0.05): b = P(both) = 0 (negative dependence) gives AND FPR 0.0000 < 0.0050 = product, and OR FPR 0.1500 > 0.1450. With b = 0.02 (positive) AND FPR 0.0200 > 0.0050 and OR 0.1300 < 0.1450.",
    "State the claim for positive dependence only: 'Positive correlation of the false flags raises the AND rate above f1 f2 and lowers the OR rate; negative correlation reverses both.' Fix the quiz stem and card AC2-c116 to say 'positively correlated'.")
row("L07-L08-math-growth-claim", "2.9-structure", "L08.html §5 bullet 'Growth is a confound' (line 466) and card AC2-c118",
    "FAIL", "The sentence 'This is the most common false-positive channel for any index built on year-on-year ratios' is an empirical comparative claim with no citation, no grade and no calculation (BUILDER_RULES 1.2 and 1.4). Not present in the registry-cited sources the page uses.",
    "Either cite a verified source for the comparison (grade it) or rewrite as a mechanism: 'Growth moves SGI and the receivables and SG&A indices, so a fast-growing firm can score high without manipulating.' Make card AC2-c118 match.")

row("L07-L08-lab-L07-1", "2.5-lab", "lab-AC2-L07-1 (hypothesis, code, expected, interpretation)",
    "PASS", "Ran the twin and the embedded code: output equals the expected block. Integers 0-9 (counts index over 10 bins, so an out-of-range score would raise). Scale check 400/400 for all SIMULATED firm-years, seed 20260527. Seeded, no network, 0.0 s in Pyodide. Interpretation: 'does not show that a high score predicts returns'. No overreach found.")
row("L07-L08-lab-L08-1-overreach", "2.5-lab", "lab-AC2-L08-1 hypothesis (line 101) vs code main() lines 352-358",
    "FAIL", "The hypothesis says 'every index is unchanged when money is multiplied by 1,000'. The code checks only the first 100 clean firm-years (`clean_pairs[:100]`), and no planted firm. The printed line 'indices unchanged under money x1000 (first 100 clean): 100/100' supports the narrower claim only.",
    "Either check all 300 clean and 300 planted firm-years, or change the hypothesis to 'every index of the first 100 clean firm-years'.")
row("L07-L08-lab-L08-1-run", "2.5-lab", "lab-AC2-L08-1 run and labels",
    "PASS", "Run and expected block match. Planted medians -1.5067 vs clean -2.4747 (class a). All M values labelled 'UNCONFIRMED constants'. Base-rate table labelled illustrative sensitivity 0.5 (an assumption). Seeded, no network, 0.0 s in Pyodide.")

row("L07-L08-num-L07-lab-distribution", "2.2-numbers", "L07.html lab output lines 289-300",
    "PASS", "Class (a): produced by lab-AC2-L07-1 (run). recompute.py: counts sum to 400, mean 2259/400 = 5.6475.")
row("L07-L08-grade-L07", "2.3-grade", "L07.html claim spans and key-results rows",
    "PASS", "Paper-based claims (7.5%, 23%, 1,448/396, footnote results, the optional nature of the signals, the Sloan attribution) graded C: one sample, one period, one market; they cite the paper. Proofs graded T (P1, P2, §4 arithmetic T on stated values). Lab results graded C with basis 'Lab 1'. Grades match BLUEPRINT §3 as applied.")
row("L07-L08-grade-L08", "2.3-grade", "L08.html key-results table and claim spans",
    "PASS", "Constants and threshold graded C and D as UNCONFIRMED (§2). Proofs T. The sensitivity bounds T (P3). The registry-verified citation at C. Only the T-graded definitional row 552 wording is a problem (separate row).")
row("L07-L08-struct-sections", "2.9-structure", "L07.html, L08.html section order",
    "PASS", "Both lessons in BUILDER_RULES 4.2 order: why it matters, core content with inline labs (L07 lab in §3, L08 lab after §2), where the canon breaks (§5), misconceptions (§6), problem set (§7), key results (§8), quiz (§9), references (§10). Debate brief not required (AC2 curriculum entry has no debate field).")
row("L07-L08-struct-counts", "2.9-structure", "L07.html, L08.html",
    "PASS", "Why-it-matters: L07 101 words, L08 97 words (<=120). Misconceptions: 3 each. Problems: M1-M3, P1-P3, E1-E3, R1-R3 in each lesson, each with <details class=solution>. Quiz: 10 items each (8-15). data-hours: L07 10, L08 12 (6-12).")
row("L07-L08-struct-banned-phrases", "2.9-structure", "L07.html, L08.html (grep, case-insensitive)",
    "PASS", "grep for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, roughly, about N%, historically, studies show, it is important to note, experts agree, well known, obviously, clearly, '...', '…', 'it can be shown': no prose hits. The only hits are Python type hints 'tuple[int, ...]' in lab code (code syntax, not an omission).")
row("L07-L08-struct-uses-metadata", "2.9-structure", "L08.html line 38 ('Uses' list)",
    "FAIL", "The 'Uses' metadata lists 'missing-data-mechanisms' (S0) and 'revenue-recognition' (AC1), but neither concept is used in the L08 body (grep: no mention of missing-data mechanisms or revenue recognition beyond the metadata). The metadata overstates what the lesson uses.",
    "Remove 'revenue recognition' and 'missing-data mechanisms' from the Uses list, or add a sentence in the body that uses them.")
row("L07-L08-dag-check_dag", "DAG", "tools/check_dag.py --all (AC2)",
    "PASS", "'check_dag AC2: PASS'. Concepts defined once: piotroski-f-score only at L07 dfn (def-piotroski-f-score), beneish-m-score only at L08 dfn (def-beneish-m-score). Every link target exists: L02 def-financial-ratio-analysis, L04 def-accruals and def-earnings-quality, L06 def-earnings-management and def-modified-jones-model, L07 def-piotroski-f-score, concepts.html anchors.")
row("L07-L08-dag-order", "DAG", "L07.html, L08.html uses",
    "PASS", "Prerequisite closure of AC2 (curriculum.json): AC1, S0, S2; S2 requires S1 and M3, so S1 (bayesian-inference) and S0 (missing-data-mechanisms) are in closure. Each use precedes its definition: L07 uses only L02/L04 and AC1 concepts; L08 uses L04, L06, L07 and AC1 concepts. Note: concepts.html#bayesian-inference is a row marked 'not yet released' (S1 is not built), so the link lands on an unreleased entry. The DAG rule is met; the reader cannot follow it to a lesson.")
row("L07-L08-hours", "2.9-structure", "L07.html data-hours=10; L08.html data-hours=12; index.html data-hours-lessons=76, data-hours-project=34",
    "PASS", "Lesson hours sum to 76 (declared in the hub) + project 34 = 110, equal to the curriculum figure. My estimate for L07: reading the lesson text, 1 lab, 9 problems, 10 quiz items, paper reading: about 9-11 h. For L08: 2 labs, 3 proofs, 9 problems, 10 quiz items: about 10-13 h. Both within +-30% of the declared 10 and 12.")

row("L07-L08-cards-L07-A", "2.7-cards", "cards.json AC2-c089 to AC2-c101 (lesson L07)",
    "PASS", "Each checked against L07 text: c089 definition; c090 scaling (§1); c091 and c092 proofs P1, P2; c093 s7 vs paper EQOFFER (§2, p.9); c094 tags (§2); c095 p.7; c096 p.11; c097 and c098 Abstract p.1 and p.3 figures (graded C, cited); c099 Sloan attribution p.8; c100 p.9 n.5; c101 p.7 n.2. All correct, atomic, cited.")
row("L07-L08-cards-L07-B", "2.7-cards", "cards.json AC2-c102 to AC2-c105, AC2-c126, AC2-c127",
    "PASS", "c102 F=8 and the failing signal (§4, T); c103 misconception 1 (false statement as written in the card, consistent with the lesson's correct reading); c104 scale invariance (Lab 1, C, basis named); c105 misconception 3; c126 1,448/396 (p.12, C); c127 F=7 (M2). All checkable against the lesson.")
row("L07-L08-cards-L08-A", "2.7-cards", "cards.json AC2-c106 to AC2-c115 (lesson L08)",
    "PASS", "c106 definition; c107 unconfirmed constants (C); c108 registry scope (C); c109 cut-off none, D; c110 PPV (T, Prop 4.2); c111 AND/OR (T, Prop 4.3, independence stated); c112 sensitivity bounds (T, P3); c113 PPV 0.0917 (C, basis named); c114 misconception with basis; c115 M not a probability. Correct.")
row("L07-L08-cards-L08-B", "2.7-cards", "cards.json AC2-c116, AC2-c117, AC2-c118, AC2-c119",
    "FAIL", "c116 says correlated false flags push the AND rate above the product: true only for positive correlation (witness in row L07-L08-math-dependence-sign). c118 asserts 'the most common false-positive channel' with no citation or grade (row L07-L08-math-growth-claim). c117 and c119 check out against the lesson (c117 has basis; c119 is a structural statement, not an empirical claim).",
    "Fix c116 to 'positively correlated' and c118 to the mechanism wording (or a cited, graded claim).")
row("L07-L08-cards-coverage", "2.7-cards", "cards.json for L08 (14 cards) vs L08 Definition 4.1",
    "FAIL", "BUILDER_RULES §7 requires one card per definition. L08 Definition 4.1 (screen, false-positive rate, specificity, sensitivity, prevalence) has no card. The L08 cards cover Definition 1.1, Propositions 4.2 and 4.3, P3 and the misconceptions, but not 4.1.",
    "Add a card for the definitions in Definition 4.1 (e.g. 'Define the prevalence p of a screen' with the back 'the share of firm-years that manipulate in the population the screen is applied to').")
row("L07-L08-cards-dupes", "2.7-cards", "ledgers/AC2/scripts/L07-L08-r1/card_dupes.py over all 127 cards",
    "PASS", "127 cards, 127 unique ids, no id gaps. 0 exact duplicate fronts. Token Jaccard >= 0.45: 2 pairs, neither touching L07/L08 (AC2-c085/c086, AC2-c025/c046).")

row("L07-L08-rubric-or-project", "2.6-project", "not applicable (no project in this slice)",
    "PASS", "The slice has no project, mutant or grader files (project.html is out of slice). No mutants required.")

mutants = []
frag = {
    "unit": "AC2",
    "slice": "L07-L08",
    "round": 1,
    "verifier": "independent verifier round 1, slice L07-L08 (did not build AC2; shares no context with the builders)",
    "pin": "0c14083",
    "base": None,
    "checkout": "/tmp/verify-ac2-l78 (detached worktree at 0c14083)",
    "scratch": "/tmp/ac2-v/L07-L08",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "rows": R,
    "mutants": mutants,
    "registry_flags": [
        "beneish1999detection: registry verifies title, journal, volume, issue and pages (Crossref live). Its model content (intercept, eight weights, cut-offs) is not verified; keep grade C and the UNCONFIRMED label."
    ],
    "freshness_flags": [],
    "notes": (
        "Piotroski (2000) is readable: the Ivey-hosted JAR 38 Supplement PDF was downloaded with plain curl (HTTP 200) and "
        "every L07 page locator was checked against pdftotext and rendered images of pp. 7 and 9. Locator failures are on "
        "p. 6 vs p. 7 (distress sentence), the §2.3 page range, and a truncated quotation. Beneish (1999) is unreadable from "
        "this build (tandfonline 403; CFA full text members-only; JSTOR client challenge). Secondary sources show the same "
        "constants as the page (Wikipedia) and could not be checked for the 4.697 and -2.22 figures. Scripts: "
        "ledgers/AC2/scripts/L07-L08-r1/recompute.py, card_dupes.py, make_fragment.py. Lab and page-smoke runs are logged in /tmp/ac2-v/L07-L08."
    ),
}
json.dump(frag, open("/tmp/verify-ac2-l78/ledgers/AC2/L07-L08.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
statuses = [r["status"] for r in R]
print("rows", len(R), {s: statuses.count(s) for s in set(statuses)})
