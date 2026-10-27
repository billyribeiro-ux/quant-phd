"""Writes the round-3 fragment ledgers/AC2/L07-L08.json (overwrites round 2). Every row keeps its round-2 id.
Run: .venv/bin/python -I ledgers/AC2/scripts/L07-L08-r3/make_fragment_r3.py  (from the checkout root)"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
R = []

def row(id_, check, location, status, evidence, fix=None):
    d = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, id_
        d["fix"] = fix
    R.append(d)

P = "PASS"; F = "FAIL"
# ---- round-2 ids: commands ----
row("L07-L08-cmd-pin", "2.9-structure", "repository (checkout /tmp/verify-ac2-l78)", P,
    "git -C /tmp/verify-ac2-l78 rev-parse --short HEAD -> 4a8690a; git status --short -> '?? .venv', '?? ledgers/AC2/' only (no tracked file modified).")
row("L07-L08-cmd-run_labs", "2.5-lab", "tools/run_labs.py --unit AC2", P,
    "Re-run this round: exit 0, 'run_labs AC2: PASS (11/11)' (logs/run_labs.txt).")
row("L07-L08-cmd-twins", "2.5-lab", "tests/labs/AC2/lab-AC2-L07-1.py, lab-AC2-L08-1.py", P,
    "Re-run this round: .venv/bin/python -I -W error on each twin: exit 0 (logs/twin-L07.txt, twin-L08.txt; stderr empty).")
row("L07-L08-cmd-embed", "2.5-lab", "course/modules/AC/AC2/L07.html, L08.html (data-run and expected blocks) vs twins", P,
    "ledgers/AC2/scripts/L07-L08-r3/embed_check.py: embedded code == twin and expected block == twin stdout, both labs: True (ALL True).")
row("L07-L08-cmd-page_smoke", "2.9-structure", "tools/page_smoke.py --unit AC2 --pages L07 L08", P,
    "Re-run this round: 'page_smoke modules/AC/AC2/L07.html: PASS', 'page_smoke modules/AC/AC2/L08.html: PASS', 'page_smoke AC2: PASS' (logs/page_smoke.txt).")
row("L07-L08-cmd-check_pages_dag_projects", "2.9-structure", "tools/check_pages.py, check_dag.py, check_projects.py --all", P,
    "Re-run this round: check_pages AC2 PASS, check_dag AC2 PASS, check_projects AC2 PASS (exit 0 each; logs/).")
row("L07-L08-cmd-lint_mypy", "2.5-lab", "the two twins", P,
    "Re-run this round: ruff check, ruff format --check (exit 0 each); mypy --no-incremental: 'Success: no issues found in 2 source files'.")
row("L07-L08-cmd-pytest", "2.5-lab", ".venv/bin/pytest -q -k 'AC2 or ac2 or L07 or L08'", P,
    "Re-run this round: exit 0, all dots, 100% (logs/pytest.txt).")
row("L07-L08-cmd-verify_refs", "2.1-citation", "tools/verify_refs.py --unit AC2 (live) and --offline (no unit)", P,
    "Re-run this round: --offline 'offline integrity: 560 entries, 0 problems'; --unit AC2 live 'live re-verification of AC2: 7 of 560 entries, 0 problems'.")
row("L07-L08-cite-piotroski2000value", "2.1-citation", "references/references.json key piotroski2000value; L07 data-cite", P,
    "Registry: Crossref-verified, Journal of Accounting Research 38, title and author Piotroski match the page's citation. The page's locators were read in the Ivey-hosted PDF (rows L07-L08-r3-piotroski-fetch, L07-L08-r3-quotes).")
row("L07-L08-cite-sloan1996stock", "2.1-citation", "references/references.json key sloan1996stock; L07 line 108 claim span", P,
    "Registry key verified (Accounting Review 71(3)). L07 line 108 attributes the accrual claim to Piotroski p. 8 citing Sloan and says Sloan's own passage was not read; Piotroski p. 8 text read (pdftotext p. 8: 'Sloan [1996] shows that earnings driven by positive accrual adjustments ... is a bad signal').")
row("L07-L08-cite-beneish1999detection", "2.1-citation", "references/references.json key beneish1999detection; L08 data-cite", P,
    "Registry verified (title, FAJ 55(5), pages 24-36). The entry is cited for the constants as UNCONFIRMED; the paper itself was not read (rows L07-L08-r3-access, L08-r3-attribution).")
row("L07-L08-loc-p1-p3-7.5-23", "2.2-numbers", "L07.html line 104 (claim span 'Abstract, p. 1; p. 3')", P,
    "PDF p. 1 abstract: 'increased by at least 7.5% annually'; 'generates a 23% annual return between 1976 and 1996'. Same sentences in the introduction, p. 3. Both located by pdftotext (quote_check.py). The period attached to 7.5% is a separate row.")
row("L07-L08-loc-p12-1448-396", "2.2-numbers", "L07.html line 106 (claim span 'p. 12 (1,448 and 396 observations)')", P,
    "PDF p. 12: 'number of observations equals 1,448 and 396, respectively' (quote_check.py, page 12).")
row("L07-L08-loc-p7-n2-optimal", "2.1-citation", "L07.html line 98 (claim span 'p. 7, n. 2')", P,
    "PDF p. 7 footnote 2: 'these signals do not represent, nor purport to represent, the optimal set of performance measures ... factor analysis may more aptly extract an optimal combination of signals, but such an approach has costs in terms of implementability' (pdftotext -layout, p. 7).")
row("L07-L08-loc-p9-n5-cutoff", "2.1-citation", "L07.html line 341 claim span; key-results row; card AC2-c100", P,
    "PDF p. 9 footnote 5: 'A specification where the current ratio cutoff equals 1.5 yields stronger return results than the liquidity metric and aggregate score used in the paper' (quote_check.py: page 9). Footnote, not main result: matches.")
row("L07-L08-loc-p7-ex-ante-quote", "2.1-citation", "L07.html line 102 (claim span, quote)", P,
    "Quote matched exactly on PDF p. 7 (quote_check.py: page 7).")
row("L07-L08-loc-p7-distress-average", "2.1-citation", "L07.html line 102 (sentences on distress, leverage, p. 6/p. 7)", P,
    "'The average high BM firm is financially distressed' on p. 6; leverage negative implication 'seem more plausible than the benefits garnered through a reduction of agency costs' on p. 7 (quote_check.py).")
row("L07-L08-loc-keyresults-2.3", "2.1-citation", "L07.html key-results row 1 (source 'Piotroski (2000), §2.3, pp. 6–10')", P,
    "Section 2.3 starts p. 6 and its 2.3.4 composite score ends on p. 10 (pdftotext pages 6-10).")
row("L07-L08-loc-signal-groups", "2.1-citation", "L07.html lines 86 and 50-90 (table groups; 'source-of-funds heading on p. 8')", P,
    "Profitability heading 2.3.1 on p. 7; 'Leverage, Liquidity, and Source of Funds' heading 2.3.2 on p. 8; Operating Efficiency 2.3.3 on p. 9 (pdftotext). Operating-efficiency page not cited on the page but the three groups are the paper's own.")
row("L07-L08-loc-scaling-p7-p8-p9", "2.1-citation", "L07.html line 65 (pp. 7, 8, 9)", P,
    "ROA and CFO scaled by beginning-of-year total assets (p. 7); ATURN scaled by beginning-of-year total assets (p. 9); leverage by average total assets (p. 8) (pdftotext).")
row("L07-L08-loc-proxies-p7-p8-p9", "2.1-citation", "L07.html §2 items 1-3 (lines 93-95)", P,
    "Net income before extraordinary items (p. 7); EQOFFER 'did not issue common equity in the year preceding portfolio formation' (p. 9); LTD over average total assets (p. 8). The EQOFFER example is a separate row.")
row("L07-L08-loc-p11-sample", "2.1-citation", "L07.html line 102 (p. 11) and line 411 (R1)", P,
    "p. 11: 'Each year between 1976 and 1996 ... retain firms in the highest BM quintile'; 'fifth month' return start on p. 11-12.")
row("L07-L08-loc-p12-groups-bootstrap", "2.1-citation", "L07.html lines 106, 419 and misconception 3 (line 356)", P,
    "p. 12: high F-score 8 or 9, low 0 or 1; bootstrap of pseudo-portfolios (1,000 repetitions) and the 1,448 / 396 counts.")
row("L07-L08-loc-sloan-p8", "2.1-citation", "L07.html line 108 (locator 'Piotroski p. 8, citing Sloan (1996)')", P,
    "p. 8 contains 'Sloan [1996] shows that earnings driven by positive accrual adjustments (i.e., profits are greater than cash flow from operations) is a bad signal' (pdftotext p. 8).")
row("L07-L08-loc-access-claims-L08", "2.1-citation", "L08.html line 93 (access sentence)", P,
    "Re-run this round with plain curl: doi.org/10.2469/faj.v55.n5.2296 -> HTTP 302 to tandfonline.com; tandfonline doi/full -> 403; ResearchGate login -> 403; SSRN abstract -> 403; JSTOR stable/2672906 -> 200 with a challenge page ('Challenge' in body). Matches the sentence. No bypass attempted.")
row("L07-L08-loc-beneish-constants-label", "2.1-citation", "L08.html lines 56, 60, 87, 89, 93-99, 417-436, 480, 487, 522, 552-558, 565, 599-608, lab docstring 113-117, lab constants 132-143", P,
    "Every place the candidate constants appear carries UNCONFIRMED (or 'unconfirmed candidate constants'): text, display (line 430), quiz q5 (line 607), misconception 2 (line 487), key-results row 5, cards c107 and c109. No place presents them as Beneish's values. (The attribution sentence on line 93 is a separate row.)")
row("L07-L08-beneish-published-wording", "2.3-grade", "L08.html lines 56, 60, 554", P,
    "Line 56 'intercept and the eight weights have not been confirmed ... so §2 treats them as unconfirmed'; line 60 'constants of §2, which are unconfirmed'; key-results row 5 'UNCONFIRMED'.")
row("L07-L08-beneish-tata-disagreement", "2.1-citation", "L08.html line 544 (R1 solution)", F,
    "R1 reads: 'The TATA weight, which comes from one secondary page, is the first value to check.' But all nine values (intercept and eight weights) come from the same single Wikipedia page (line 93; wiki.txt). Singling out TATA implies a different source status for the other weights, and 'first value to check' gives no reason. Checked: wiki constants all present (wiki_and_access_check.py).",
    fix="State that the intercept and all eight weights come from the same single secondary page, and that the check should cover the full set; delete the TATA-only sentence.")
row("L07-L08-beneish-cutoffs", "2.1-citation", "L08.html line 97", P,
    "Wikipedia threshold sentence (wiki.txt): 'The threshold value is -1.78 for the model whose coefficients are reported above. (see Beneish 1999, Beneish, Lee, and Nichols 2013, and Beneish and Vorst 2020)'. The page says 'citing Beneish (1999) without a locator': Beneish 1999 is one of three cited works; acceptable, graded D.")
row("L07-L08-build-report-refs", "2.1-citation", "L07.html line 344; L08.html line 477 (pointers to plans/AC2-open-items.md)", P,
    "Both pointers now name plans/AC2-open-items.md (exists). The file's table lists the out-of-sample item (Mohanram 2005 as candidate) and the joint-use item. Once per page. The bibliographic naming in these sentences is a separate row.")
row("L07-L08-math-signals-vs-contract", "2.4-math", "L07.html lines 56-86 (ratios, Definition 1.1, table) vs atlas/A15.contract.md piotroski_f_score (lines 135-145)", P,
    "Contract conditions 1-9 and the ratio definitions (ROA, CFO/TA_{t-1}, LEV with average TA, CR, GM, ATO/TA_{t-1}) match the page's table order and formulas (checked line by line).")
row("L07-L08-math-proxies-stated", "2.1-citation", "L07.html §2 (lines 90-96); contract 'Departures from the published definitions' (lines 162-168)", P,
    "Contract lists the three proxies (NetIncomeLoss; shares change for equity issuance; LongTermDebtNoncurrent) with page numbers pp. 7-8, p. 9, p. 8; the page says the same. Note the EQOFFER example is separately failed.")
row("L07-L08-math-P1", "2.4-math", "L07.html P1 (lines 378-381)", P,
    "Re-derived: s4=1 iff CFO/D > NI/D with D = TA_{t-1} > 0 iff CFO > NI. ACCRUAL = NI - CFO so ACCRUAL < 0 iff CFO > NI (p. 8). Correct.")
row("L07-L08-math-P2", "2.4-math", "L07.html P2 (lines 382-385)", P,
    "Re-derived: each ratio (ROA, CFO*, ATO, GM, LEV, CR) is money/money so invariant under k; s1-s6, s8, s9 compare such ratios or zero; s7 compares counts. Integer 0..9 because each s_i in {0,1}. Correct.")
row("L07-L08-math-P3", "2.4-math", "L07.html P3 (lines 386-389)", P,
    "Recomputed exactly (Fractions): LEV_t = 300/950 = 6/19 = 0.3158, LEV_{t-1} = 310/1050 = 31/105 = 0.2952; s5 = 0. Correct.")
row("L07-L08-math-worked-firm", "2.4-math", "L07.html §4 (lines 307-335), M1 (364-366), M2 (368-370), M3 (372-374), E2 (398-400)", P,
    "Independent exact recomputation (independent_labs.py): ROA 117/1100, 66/1000; CFO* 96/1100; LEV 264/1150 and 330/1050; CR 528/240 and 440/220; GM 546/1560 and 396/1320; ATO 1560/1100 and 1320/1000; vector (1,1,1,0,1,1,1,1,1), F = 8. M2 (NI=-20): (0,1,0,1,1,1,1,1,1), F = 7. M3 invariance holds. E2: 118/1100 > 117/1100, F = 9. All match.")
row("L07-L08-math-E1-count", "2.2-numbers", "L07.html E1 (line 396) and Lab 1 output (lines 289-300)", P,
    "Lab output score 8: 24, score 9: 7; 31/400 = 0.0775 (independent_labs.py reproduces 24 and 7).")
row("L07-L08-misconception-score-zero", "2.4-math", "L07.html misconception 1 (line 352) and card AC2-c103", F,
    "The signal-count claims are right (s1, s2 sign tests; s3 and s5-s9 change tests; s4 a same-year level test; F = 2 in the example). But the same paragraph ends 'The score sorts changes within a population', which the paragraph itself contradicts (s1, s2 and s4 are level tests).",
    fix="Replace 'The score sorts changes within a population' with a statement that it mixes sign tests (s1, s2, s4) and change tests (s3, s5-s9).")
row("L07-L08-math-L08-indices", "2.4-math", "L08.html lines 78-85 (eight index list); atlas/A15.contract.md beneish_m_score (lines 146-156)", P,
    "All eight index formulas match the contract line by line (DSRI, GMI, AQI, SGI, DEPI, SGAI, LVGI, TATA). The lab docstring's claim about Beneish (1999) is a separate row.")
row("L07-L08-math-prop4.2", "2.4-math", "L08.html Proposition 4.2 and proof (lines 445-452), P1 (line 514)", P,
    "Bayes and total probability: PPV = ps/(ps+(1-p)(1-sigma)). Re-derived; numeric 0.0917 at s=0.5, p=0.01, sigma=0.95 (exact 0.091743).")
row("L07-L08-math-prop4.3", "2.4-math", "L08.html Proposition 4.3 and proof (lines 456-463), P2 (line 518)", P,
    "Under independence AND = f1 f2, OR = 1-(1-f1)(1-f2). Re-derived; 0.10 x 0.05 = 0.0050; OR = 0.145.")
row("L07-L08-math-L08-P3", "2.4-math", "L08.html P3 (lines 519-523)", P,
    "AND sensitivity <= min(s1, s2) and OR sensitivity >= max(s1, s2) by monotonicity of intersection and union; no independence used. Correct.")
row("L07-L08-math-worked-M", "2.2-numbers", "L08.html §3 display (lines 430-436) and quiz row 5 explanation (line 608)", P,
    "Exact M (Fractions, worked_L08.py) = -28815329/18480000 = -1.559271 -> rounds to -1.5593. Displayed indices rounded to 4 dp: displayed terms sum to -1.55943 -> -1.5594. The page states both and says M is computed from unrounded values. Acceptable.")
row("L07-L08-math-base-rate-table", "2.2-numbers", "L08.html lab output (lines 398-411) and base-rate table in Lab 1", P,
    "Exact recomputation (independent_labs.py): PPV and flags per 1000 for all nine prevalence/specificity rows match the printed table (e.g., 0.001/0.95: 0.009911, 49.95; 0.01/0.95: 0.091743, 49.50; 0.05/0.95: 0.344828, 47.50).")
row("L07-L08-math-E2-E3-E1", "2.4-math", "L08.html E1 (lines 527-529), E2 (531-533), E3 (535-537)", F,
    "E1: 0.9680 = -1.5067 - (-2.4747) (recomputed: 0.968). E2: 0.3448/0.0099 = 34.8 (recomputed 34.79), about 35 correct. E3 FAILS: the question asks for false flags 'per 1,000 clean firm-years', and the answer gives 49.50 from 1000(1-p)FPR, which is per 1,000 firm-years of the whole population. Per 1,000 clean firm-years the count is 1000 x FPR = 50, independent of prevalence, so the solution's 'the count depends on prevalence' contradicts the question's own unit.",
    fix="Ask for flags per 1,000 firm-years (population), or change the answer to 1000 x FPR = 50 per 1,000 clean firm-years and delete the prevalence remark.")
row("L07-L08-math-dependence-sign", "2.4-math", "L08.html §4 paragraph (line 465), misconception 3 (line 489), quiz row 10 (line 653)", P,
    "Positive correlation raises the AND rate above f1 f2 and lowers the OR rate; negative reverses. Joint-law example (never both flag): AND 0 and OR 0.15 are both feasible (0.10 + 0.05 <= 1). Correct. The sentence on overlapping inputs is a separate row.")
row("L07-L08-math-growth-claim", "2.4-math", "L08.html §5 bullet 'Growth is a confound' (line 475); card AC2-c118", P,
    "Witness recomputed: revenue 1000->1500, receivables 100->150, SG&A 150->225 gives DSRI = (150/1500)/(100/1000) = 1, SGAI = (225/1500)/(150/1000) = 1, SGI = 1.5. The bullet's 'change only when ... grow faster or slower than revenue' is an identity and correct. The R2 sentence is a separate row.")
row("L07-L08-lab-L07-1", "2.5-lab", "lab-AC2-L07-1 (hypothesis line 114, code 115-281, interpretation line 302) and lines 110", F,
    "Code and output reproduce (embed_check.py; independent_labs.py). But line 110 says 'The lab checks two properties the contract requires: the score is an integer from 0 to 9, and every signal is unchanged ...'. The code has no check of the 0-9 range (main() only prints the distribution and the scale count), so the lab does not check the first property. The same overclaim is in the hypothesis at line 114.",
    fix="Say the lab checks scale invariance and prints the score distribution; state the integer range as a consequence of the definition (P2), not a lab check.")
row("L07-L08-lab-L08-1-overreach", "2.5-lab", "lab-AC2-L08-1 hypothesis (line 106) and main() lines 352-371", F,
    "Code reproduces the printed output (embed_check.py). The hypothesis says the check 'reproduces the §4 PPV of 0.0917 at prevalence 0.01 and specificity 0.95'; the PPV also needs the sensitivity 0.5 that the lab hard-codes (base_rate_table), which the hypothesis omits; and PPV is first defined later, in Proposition 4.2 (line 447).",
    fix="Add 'sensitivity 0.5' to the hypothesis and state that §4 gives the formula.")
row("L07-L08-lab-L08-1-run", "2.5-lab", "lab-AC2-L08-1 run and labels (lines 382-411)", P,
    "Re-run: twin stdout equals the expected block (embed_check.py). Labels 'UNCONFIRMED' and 'illustrative sensitivity' appear with the output. No network use.")
row("L07-L08-num-L07-lab-distribution", "2.2-numbers", "L07.html lab output lines 289-300", P,
    "Independent recomputation (independent_labs.py, exact Fractions on the generator's floats): distribution [0,0,2,16,60,108,109,74,24,7], mean 5.6475, scale invariance 400/400. Matches the printed output.")
row("L07-L08-grade-L07", "2.3-grade", "L07.html claim spans and key-results rows (lines 425-436)", P,
    "Grades: T for proofs and worked arithmetic; C for paper results (7.5%, 23%, footnotes, sloan attribution); the period issue is a separate row.")
row("L07-L08-grade-L08", "2.3-grade", "L08.html key-results table (lines 558-568)", F,
    "Row 5 says 'candidate values from secondary sources' (plural). All constants come from one secondary Wikipedia page (line 93; §2 says 'one secondary web page'). Other rows (T, C, D) match their proofs and sources.",
    fix="Change 'secondary sources' to 'one secondary web page'.")
row("L07-L08-struct-sections", "2.9-structure", "L07.html, L08.html", P,
    "Sections 1-10 with key results, quiz and references in order on both pages (grep of section headings).")
row("L07-L08-struct-counts", "2.9-structure", "L07.html, L08.html", P,
    "L07: 3 misconceptions, M1-M3, P1-P3, E1-E3, R1-R3, 10 quiz items; L08: 3 misconceptions, M1-M3, P1-P3, E1-E3, R1-R3, 10 quiz items. Counts of Lab 1 on each page: 1.")
row("L07-L08-struct-banned-phrases", "2.9-structure", "L07.html, L08.html (case-insensitive scan)", P,
    "Scan for 'roughly half', 'about 6%', 'historically', ellipsis, 'U.S.', 'clearly', 'obviously', 'typically', 'usually' etc.: none found in learner text. 'many firms' (L08 line 52) is treated as a separate row.")
row("L07-L08-struct-uses-metadata", "2.9-structure", "L08.html line 38 ('Uses') and L07.html line 38", P,
    "L07 uses financial-ratio-analysis, accruals, accrual-accounting, cash-flow-statement, balance-sheet; L08 uses piotroski-f-score, accruals, depreciation-and-amortization. All resolve (links row).")
row("L07-L08-dag-check_dag", "DAG", "tools/check_dag.py --all (AC2)", P,
    "Re-run this round: check_dag AC2 PASS.")
row("L07-L08-dag-order", "DAG", "L07.html, L08.html uses and concept links", P,
    "bootstrap owned by S2 (S2 uses it; S2 in closure). robust-statistics introduced in S0 (curriculum/01-foundations.yaml line 595). bayesian-inference in S1 (line 644). depreciation-and-amortization in AC1 (curriculum/02-economics-finance-core.yaml line 534). piotroski-f-score defined in L07. All are in AC2's closure.")
row("L07-L08-hours", "2.9-structure", "L07.html data-hours=10; L08.html data-hours=12; index.html data-hours-lessons=76", P,
    "Sum of lesson data-hours L01-L08 = 9+10+8+10+9+8+12+10 = 76 (matches index). Own estimate: L07 about 9-11 h, L08 about 11-13 h; declared values within 30%.")
row("L07-L08-cards-L07-A", "2.7-cards", "cards.json AC2-c089 to AC2-c101 (lesson L07)", F,
    "Checked each card against its lesson text. c097 says the 7.5% gain is 'for 1976 to 1996 (Abstract, p. 1)': the abstract's 7.5% sentence has no period (pdftotext p. 1, p. 3). The 1976-1996 sample is on p. 11 for the whole study; the attribution to the 7.5% figure is not in the cited locator. Others match (c089-c096, c098-c101 checked).",
    fix="Give the period as the sample (p. 11) for the study, or drop 'for 1976 to 1996' from the 7.5% card.")
row("L07-L08-cards-L07-B", "2.7-cards", "cards.json AC2-c102 to AC2-c105, AC2-c126, AC2-c127, AC2-c130", P,
    "c102 (F=8, s4 fails), c103 (F=2 example, s3, s5-s9 change tests, s4 level; matches §6), c104 (400/400), c105 (within-sample), c126 (1,448 / 396, p. 12), c127 (F=7; s1 and s3 fall to 0, s4 rises to 1; other signals unchanged; matches M2 and the s4 correction), c130 (pp. 7-10).")
row("L07-L08-cards-L08-A", "2.7-cards", "cards.json AC2-c106 to AC2-c115 and AC2-c129 (lesson L08)", P,
    "c106 (screen, not probability), c107 (one secondary source, unconfirmed), c108 (registry verifies title/journal/volume/issue/pages), c109 (D threshold), c110-c113 (PPV formula and 0.0917), c114 (PPVs below 0.1 at prevalence 0.001 for spec up to 0.95 at sensitivity 0.5 matches table), c115, c129. All match the page.")
row("L07-L08-cards-L08-B", "2.7-cards", "cards.json AC2-c116, AC2-c117, AC2-c118, AC2-c119", P,
    "c116 (correlation effects, match §4 and misconception 3), c117 (medians -2.4747 / -1.5067, match output), c118 (witness values match recomputation), c119 (TATA is the cash-flow accrual NI - CFO over TA; L04 defines the cash-flow accrual NI - CFO (L04 line 386), so 'same family' holds).")
row("L07-L08-cards-coverage", "2.7-cards", "cards.json (L08 cards) vs Definition 4.1 (lines 99-102)", P,
    "Definition 4.1 terms: false-positive rate (c132), specificity (c132), sensitivity (c131), prevalence (c129), screen (c133). All covered.")
row("L07-L08-cards-dupes", "2.7-cards", "ledgers/AC2/scripts/L07-L08-r3/card_scan.py over all 138 AC2 cards", P,
    "138 unique ids, sequential AC2-c001..c138; the only near-duplicate pairs over threshold are c052/c055 (other lessons, different content) and c089/c106 (same question template, different answers). No duplicate in L07/L08.")
row("L07-L08-rubric-or-project", "2.6-project", "not applicable (no project in this slice)", P,
    "Slice has no project or grader; mutation check not applicable.")
row("L07-L08-r2-us-claim", "2.1-citation", "L07.html line 104 (no 'U.S.' in learner text)", P,
    "'U.S.' absent from L07 and L08 (grep). 'one market' remains as a grade rationale, not a source claim.")
row("L07-L08-r2-uncited-assertions", "2.9-structure", "L08.html line 52 (why-it-matters lead)", F,
    "The lead says 'A screen that flags manipulators will flag many firms that are not manipulating'. No calculation or citation supports 'many'; the count depends on the false-positive rate and prevalence (Proposition 4.2 and the table). The other r2 sentence (line 456) is gone.",
    fix="State the dependence on FPR and prevalence, or show the base-rate table value that makes 'many' concrete.")
row("L07-L08-r2-paper-design-claim", "2.1-citation", "L08.html (r2 line 427)", P,
    "The 'paper's design targets' sentence has been removed; the receivables footprint wording in §3 and M1 is not attributed to the paper.")
row("L07-L08-r2-constants-provenance", "2.3-grade", "L08.html line 93", F,
    "Line 93 says the intercept and weights are 'candidate values that one secondary web page attributes to the paper'. Checked (wiki.html refs): the coefficient formula is cited to [1] ycharts.com 'Beneish M Score Definition' and [2] Beneish, Farber, Glendening, Shaw (2023), The Accounting Review. Beneish (1999) appears only in the threshold sentence (line 97 source). So the page misattributes the coefficients to the 1999 paper.",
    fix="Say: 'one secondary web page gives these values; its coefficient formula cites a ycharts.com web page and a 2023 Beneish et al. paper, not Beneish (1999); the 1999 paper is not read.'")
row("L07-L08-r2-balance-sheet-accrual", "2.4-math", "L08.html line 476; card AC2-c119", P,
    "TATA is now labelled a cash-flow-approach accrual measure (NI - CFO over TA), which is the correct family (L04 line 386 defines the cash-flow accrual NI - CFO).")
row("L07-L08-r2-def41-before-use", "2.9-structure", "L08.html Definition 4.1 (lines 99-102) vs lab hypothesis (line 106) and first use", P,
    "Definition 4.1 (sensitivity, specificity, FPR, prevalence) precedes the lab (line 104) and §2 use. (PPV is a different term, defined later: separate row.)")
row("L07-L08-r2-lab-L08-table-claim", "2.5-lab", "lab-AC2-L08-1 hypothesis (line 106)", F,
    "The hypothesis claims the PPV check reproduces the §4 value 0.0917 at prevalence 0.01 and specificity 0.95 without the sensitivity 0.5 that determines it (the lab hard-codes 0.5).",
    fix="Add 'sensitivity 0.5' to the hypothesis.")
row("L07-L08-r2-threshold-row", "2.3-grade", "L08.html key-results row (line 566)", P,
    "'UNCONFIRMED: ... one secondary web page gives −1.78; not confirmed against the paper' graded D, consistent with the Wikipedia threshold (wiki.txt).")
row("L07-L08-r2-wiki-constants", "2.1-citation", "L08.html lines 93, 95, 97; lab docstring lines 113-117; lab constants lines 132-143", P,
    "Wikipedia values (wiki_and_access_check.py): intercept -4.84; DSRI 0.92; GMI 0.528; AQI 0.404; SGI 0.892; DEPI 0.115; SGAI -0.172; TATA 4.679; LVGI -0.327; threshold -1.78. Present. 4.697 and -2.22 absent. Lab constants equal these.")
row("L07-L08-r2-jstor-statement", "2.1-citation", "L07.html line 104 ('The JSTOR record ... could not be read (bot check)')", P,
    "Re-run with plain curl: https://www.jstor.org/stable/2672906 -> HTTP 200 with a challenge page. Matches. No bypass attempted.")
row("L07-L08-r2-process-words", "2.9-structure", "L07.html, L08.html (case-insensitive)", P,
    "No 'builder', 'this build', 'REQUESTS', 'unit report' in learner text; 'the build report' removed; the lab docstring has no process words.")
row("L07-L08-r2-lab-numbering", "2.9-structure", "L07.html, L08.html lab headings and text", P,
    "Each page has 'Lab 1'; other lessons' labs are referred to as 'Lesson N's lab' on these pages where cited.")
row("L07-L08-r2-links", "2.9-structure", "L07.html and L08.html internal and concept links", P,
    "Every href target file exists and every #anchor exists (link scan this round, zero missing).")
row("L07-L08-r2-bayes-S1-and-total-probability", "DAG", "L08.html line 454 (Bayesian inference link), Proposition 4.2 proof (line 451)", P,
    "bayesian-inference is an S1 concept (curriculum/01-foundations.yaml line 644) in the closure; the law of total probability is proved on the page (line 451).")
row("L07-L08-r2-quiz-keys", "2.4-math", "L07.html quiz (lines 444-518), L08.html quiz (lines 575-655)", P,
    "Keys re-checked: L07 q1 (s4), ROA 0.10636 (tolerance 1e-4), q3, F=8, q5, q6, q7 (departure = equity signal wording), q8, F=7 (M2), q10. L08 q1 0.0917, q2 tolerance 5e-4, q3 0.0050, q4, q5 -1.5593 (tolerance 5e-4; exact -1.559271), q6-q10. All keys correct.")

# ---- round-3 new rows ----
row("L07-L08-r3-piotroski-fetch", "2.1-citation", "Piotroski (2000) Ivey-hosted PDF (URL in ledgers/AC2/scripts/L07-L08-r2/make_fragment_r2.py)", P,
    "Plain curl -L: HTTP 200, application/pdf, 876,917 bytes, 41 pages (/tmp/ac2-v/L07-L08-r3/src/piotroski.pdf). pdftotext: pages 1-12 read in full.")
row("L07-L08-r3-quotes", "2.1-citation", "L07.html claim quotations (lines 98, 102, 341) and page locators", P,
    "ledgers/AC2/scripts/L07-L08-r3/quote_check.py: 'stated ex ante implication ... financially distressed at some level' p. 7; 'stronger return results than the liquidity metric and aggregate score' p. 9; footnote 2 p. 7 (layout text); 'Sloan [1996] shows ...' p. 8; 'average high BM firm is financially distressed' p. 6; 1,448 and 396 p. 12; 7.5% and 23% p. 1. All present on the stated pages.")
row("L07-L08-r3-wiki-fetch", "2.1-citation", "Wikipedia 'Beneish M-score' (https://en.wikipedia.org/wiki/Beneish_M-score), plain curl", P,
    "HTTP 200 this round; constants and the -1.78 threshold present; 4.697 and -2.22 absent (wiki_and_access_check.py; log wiki_and_access_check.txt).")
row("L07-L08-r3-access", "2.1-citation", "L08.html line 93 access statuses", P,
    "See L07-L08-loc-access-claims-L08 (re-run: doi 302 -> tandfonline 403; ResearchGate 403; SSRN 403; JSTOR challenge).")
row("L07-L08-r3-recompute-L07", "2.2-numbers", "L07.html Lab 1 output, §4, M1-M3, E1-E3, P3", P,
    "ledgers/AC2/scripts/L07-L08-r3/independent_labs.py (own code, exact Fractions on the twin's generator floats): signal vectors for six firms, score distribution, mean 5.6475, scale invariance 400/400, worked-firm vector and F, M2, P3, E2, E3, E1 all reproduced.")
row("L07-L08-r3-recompute-L08", "2.2-numbers", "L08.html Lab 1 output, §3 worked M, base-rate table, E1-E3, AND/OR", P,
    "independent_labs.py and worked_L08.py: planted[0] indices and M -1.3869, clean median -2.4747, planted median -1.5067 (gap 0.968), base-rate table (9 rows), AND 0.005, OR 0.145, worked M exact -1.559271 (displayed-sum -1.5594). All match.")
row("L07-L08-r3-contract-departures", "2.1-citation", "atlas/A15.contract.md 'Departures from the published definitions' (lines 162-168) vs L07 §2", P,
    "Contract page numbers pp. 7-8 (income before extraordinary items), p. 9 (issued common equity), p. 8 (LTD) match L07 §2 locators.")
row("L07-L08-r3-registry-no-fscore-study", "2.1-citation", "references/references.json (560 entries)", P,
    "Title search for Piotroski/F-score/fundamental/Beneish/manipulation: only piotroski2000value and beneish1999detection; no F-score study outside the paper. The L07 sentence 'the registry holds no verified study of the F-score outside the paper's sample' is correct.")
row("L07-L08-r3-open-items-content", "2.1-citation", "plans/AC2-open-items.md (REFERENCE_REQUESTS rows for Mohanram, Dechow/Beneish, joint use, out-of-sample)", P,
    "The file lists the out-of-sample item and the joint-use item as OPEN, and labels the names 'from recall'. The pages' description of them matches the file.")
row("L07-L08-r3-from-recall-L07", "2.9-structure", "L07.html line 344 ('Mohanram 2005, from recall and unverified')", F,
    "Bibliographic data (author, year) typed from memory into learner text. CLAUDE.md: 'Never type bibliographic data from memory'; the source is not in references.json, so it cannot be cited, and the page should not name it.",
    fix="Remove the author and year; say the candidate counter-evidence is not in the registry and point to the open-items file.")
row("L07-L08-r3-from-recall-L08", "2.9-structure", "L08.html line 477 ('Dechow, Ge, Larson & Sloan 2011; Beneish, Lee & Nichols 2013 ... from recall')", F,
    "Same defect: two bibliographic items typed from memory into learner text, neither in references.json.",
    fix="Remove the names and years; keep the open-items pointer only.")
row("L07-L08-r3-stock-funded-example", "2.1-citation", "L07.html §2 item 2 (line 94)", F,
    "The paper's EQOFFER is 'did not issue common equity in the year preceding portfolio formation' (p. 9). A stock-funded acquisition is an issuance of common equity, so EQOFFER = 0, and s7 = 0 when the share count rises: they agree, not disagree. The sentence 'The paper's text does not address that case' is therefore wrong (the main-text definition covers it; the appendix's 'raised equity capital' wording is a different phrasing). The true disagreement example is a share-count rise with no issuance, e.g. a stock split.",
    fix="Replace the stock-funded example with a stock split (count rises, no equity issued, s7 = 0 and EQOFFER = 1) and drop 'does not address'.")
row("L07-L08-r3-lab-checks-integer", "2.5-lab", "L07.html line 110 and hypothesis line 114", F,
    "See L07-L08-lab-L07-1: the 0-9 integer property is not a lab check.", fix="See L07-L08-lab-L07-1.")
row("L07-L08-r3-lab-docstring-pages", "2.1-citation", "lab-AC2-L07-1 docstring (line 120): 'pp. 8-10 (printed pages)'", F,
    "The signal definitions the lab implements begin on p. 7 (ROA and CFO scaled by beginning assets, p. 7; the page itself cites p. 7 for them at line 93). 'pp. 8-10' omits p. 7.",
    fix="Change to 'pp. 7-10'.")
row("L07-L08-r3-period-7.5", "2.1-citation", "L07.html line 104 claim span ('both for 1976 to 1996'); key-results row 5 (line 432); card AC2-c097", F,
    "The abstract (p. 1) and p. 3 give '7.5% annually' with no period; the 23% sentence has '1976 and 1996'. The 1976-1996 sample is on p. 11 for the study as a whole. The claim that the 7.5% is 'for 1976 to 1996' is an attribution the cited locators do not state.",
    fix="Cite p. 11 for the sample period and say the sample period applies to the paper's results, or drop 'both for 1976 to 1996' for the 7.5% figure.")
row("L07-L08-r3-R2-track-growth", "2.4-math", "L08.html R2 solution (line 548)", F,
    "'compare the indices within growth tercile, since SGI and the receivables and SG&A indices track growth (§5)'. §5 (line 475) says DSRI and SGAI change only when receivables or SG&A grow faster or slower than revenue, and gives the proportional-growth witness where both equal 1. They do not 'track growth' in general.",
    fix="Say DSRI and SGAI respond to growth in receivables or SG&A relative to revenue, not to growth itself; SGI is the growth term.")
row("L07-L08-r3-signs-of-improvement", "2.4-math", "L08.html §4 paragraph (line 442)", F,
    "'The F-score counts signs of improvement in profitability, leverage, liquidity and efficiency'. Signals s1, s2 and s4 are level tests (L07 misconception 1), so the F-score does not count only improvements.",
    fix="Say the F-score counts favourable signs: some level tests (s1, s2, s4) and some change tests.")
row("L07-L08-r3-margin-overlap", "2.4-math", "L08.html §4 paragraph (line 465)", F,
    "'the F-score's profitability tests overlap with the M-score's margin and asset items'. F-score profitability tests are ROA, CFO and accruals (L07 §1 groups); gross margin enters the F-score as s8 in the operating-efficiency group, not a profitability test.",
    fix="Name the actual overlap: ROA and CFO use total assets (the M-score's asset base), and s4 and TATA both compare NI with CFO.")
row("L07-L08-r3-eight-year-on-year", "2.9-structure", "L08.html why-it-matters (line 52)", F,
    "'a linear score from eight year-on-year ratios'. TATA is a single-year ratio (line 89 says so: 'TATA is a single-year accrual level'); the contract's definition also has TATA on year t only.",
    fix="Say 'eight ratios, seven of them year-on-year'.")
row("L07-L08-r3-weights-only-source", "2.3-grade", "L08.html line 89", F,
    "'Its weights are the only numbers that depend on the source, and they are the only numbers that cannot yet be confirmed.' The intercept is also a source-dependent constant (§2; contract BENEISH_INTERCEPT). The sentence leaves it out.",
    fix="Say 'the intercept and the eight weights'.")
row("L07-L08-r3-used-in-lab-only", "2.3-grade", "L08.html line 95 ('They are used in the lab only, under a label, to show the arithmetic.')", F,
    "False. The candidate constants are also used in the §3 worked M (lines 430-436), misconception 2 (line 487), quiz item 5 (line 607) and the key-results text. Each is labelled unconfirmed, but 'the lab only' is wrong.",
    fix="Say 'used only to show the arithmetic, always under the UNCONFIRMED label (lab, §3, misconception 2, quiz 5)'.")
row("L07-L08-r3-PPV-before-defined", "2.9-structure", "L08.html lab hypothesis (line 106) and lab table header (line 373) use PPV; Proposition 4.2 (line 447) defines it", F,
    "PPV is used in §1-2 text and the lab before its definition in §4; the lab hypothesis also cites '§4' for a value that comes after it.",
    fix="Define PPV in §2 (or in Definition 4.1) or move the lab's PPV check after Proposition 4.2.")
row("L07-L08-r3-as-much-as", "2.4-math", "L08.html §4 paragraph (line 454)", F,
    "'Proposition 4.2 shows that the PPV depends on prevalence as much as on specificity.' The proposition shows dependence on both; 'as much as' is a comparison nothing on the page computes.",
    fix="Drop 'as much as', or show the two sensitivities of the table (e.g. 0.0481 to 0.3356 across specificity at p = 0.01 versus 0.0099 to 0.3448 across prevalence at spec 0.95).")
row("L07-L08-r3-lab-docstring-follows-beneish", "2.1-citation", "lab-AC2-L08-1 docstring line 111 ('which follow Beneish (1999)')", F,
    "The index definitions are the contract's; the paper was not read (line 93 says so), so 'which follow Beneish (1999)' is a claim about a source the page did not read. Per the brief, an unreadable published fact is UNVERIFIABLE, which counts as FAIL.",
    fix="Say 'which are the contract's definitions (atlas/A15.contract.md, beneish_m_score); the paper's own definitions are not confirmed'.")
row("L07-L08-r3-prop-4.2-page-locator", "2.4-math", "L08.html line 54-56 and §3 'Two things' (line 438)", P,
    "Re-checked: 'the TATA term is small because accruals are a small share of assets' (0.156 of M, accrual 0.033 of TA) and 'DSRI is the largest index (1.5000)' (other indices 0.98-1.20) match the worked values.")

NOTES = (
    "Round 3 (pin 4a8690a). Piotroski (2000) re-fetched by plain curl (HTTP 200, 41 pages) and read in full for pp. 1-12 "
    "(pdftotext); every quoted phrase and locator re-checked (quote_check.py). Beneish (1999): doi.org 302 to tandfonline 403; "
    "ResearchGate 403; SSRN 403; JSTOR challenge (200). Wikipedia 'Beneish M-score' (plain curl, 200): constants and -1.78 "
    "present; 4.697 and -2.22 absent; its coefficient formula cites ycharts [1] and Beneish et al. 2023 [2], not Beneish (1999). "
    "Both labs re-run (twins, run_labs, embed check); independent Fraction recomputation of every lab output, worked number, "
    "table and proof value (independent_labs.py, worked_L08.py). Source of the failing items: text of lines cited per row. "
    "Scripts: ledgers/AC2/scripts/L07-L08-r3/. Scratch: /tmp/ac2-v/L07-L08-r3/."
)

fragment = {
    "unit": "AC2",
    "slice": "L07-L08",
    "round": 3,
    "verifier": "round-3 independent verifier for slice L07-L08 (did not build AC2; shares no context with the builders, round-1 or round-2 verifiers)",
    "pin": "4a8690a",
    "base": None,
    "previous_ledger": "round 2, pin bc3226e: 83 rows, 67 PASS, 16 FAIL (overwritten by this round's fragment)",
    "checkout": "/tmp/verify-ac2-l78 (detached worktree at 4a8690a)",
    "scratch": "/tmp/ac2-v/L07-L08-r3",
    "verified_at": "2026-10-27T18:30:00+00:00",
    "verdict": "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [
        "beneish1999detection: registry verifies title, journal, volume 55, issue 5, pages 24-36 (Crossref live this round, unit AC2). Model content (intercept, eight weights, cut-offs) is not verified; the page labels them UNCONFIRMED. The -1.78 threshold is from one secondary web page only."
    ],
    "freshness_flags": [],
    "notes": NOTES,
    "summary": {},
}
n_fail = sum(1 for r in R if r["status"] != "PASS")
fragment["summary"] = {"rows": len(R), "pass": len(R) - n_fail, "fail": n_fail, "unverifiable": 0}
out = ROOT / "ledgers" / "AC2" / "L07-L08.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, fragment["summary"])
