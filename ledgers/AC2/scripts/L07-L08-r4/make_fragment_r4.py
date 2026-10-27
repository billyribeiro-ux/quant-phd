"""Round-4 fragment writer for slice L07-L08 (pin 2607c60). Reads the round-3 fragment, re-decides every row,
adds new rows, writes ledgers/AC2/L07-L08.json. Evidence strings name the command, file and line used."""
import json
import sys

SRC = "/tmp/ac2-frags/L07-L08.round3.json"
OUT = sys.argv[1]
d = json.load(open(SRC, encoding="utf-8"))
old = {r["id"]: r for r in d["rows"]}

R = "Round 4 (pin 2607c60): "
CARRY = "Carried from round 3 ({files} lines {lines} byte-identical since 4a8690a; the 4a8690a..2607c60 hunks do not touch them): "
L07 = "course/modules/AC/AC2/L07.html"
L08 = "course/modules/AC/AC2/L08.html"

def carry(rid, files, lines):
    return dict(old[rid], status="PASS", evidence=CARRY.format(files=files, lines=lines) + old[rid]["evidence"])

def passrow(rid, evidence):
    base = old.get(rid, {})
    return {"id": rid, "check": base.get("check", "2.1-citation"), "location": base.get("location", ""),
            "status": "PASS", "evidence": R + evidence}

def failrow(rid, location, check, evidence, fix):
    return {"id": rid, "check": check, "location": location, "status": "FAIL", "evidence": R + evidence, "fix": fix}

over = {}
# ---- command rows: re-run this round (logs in /tmp/ac2-v/L07-L08-r4/logs) ----
over["L07-L08-cmd-pin"] = passrow("L07-L08-cmd-pin", "git -C /tmp/verify-ac2r4-l78 rev-parse --short HEAD -> 2607c60; git status --short -> '?? .venv' only (logs/pin.txt). Delta 4a8690a..2607c60 read hunk by hunk: L07.html, L08.html, cards.json, lab-AC2-L07-1.py, lab-AC2-L08-1.py, plans/AC2-open-items.md, and others outside this slice.")
over["L07-L08-cmd-run_labs"] = passrow("L07-L08-cmd-run_labs", ".venv/bin/python tools/run_labs.py --unit AC2 -> 'run_labs AC2: PASS (11/11)', exit 0 (logs/run_labs.txt).")
over["L07-L08-cmd-twins"] = passrow("L07-L08-cmd-twins", ".venv/bin/python -I -W error tests/labs/AC2/lab-AC2-L07-1.py and lab-AC2-L08-1.py: exit 0, empty stderr (logs/twin-L07.txt, twin-L08.txt).")
over["L07-L08-cmd-embed"] = passrow("L07-L08-cmd-embed", "ledgers/AC2/scripts/L07-L08-r4/embed_check.py: embedded data-run code == twin (L07 True, L08 True); expected block == twin stdout (L07 True, L08 True) (logs/embed_check.txt).")
over["L07-L08-cmd-page_smoke"] = passrow("L07-L08-cmd-page_smoke", "tools/page_smoke.py --unit AC2 --pages L07 L08: 'page_smoke modules/AC/AC2/L07.html: PASS', 'L08.html: PASS', 'page_smoke AC2: PASS', exit 0 (logs/page_smoke.txt).")
over["L07-L08-cmd-check_pages_dag_projects"] = passrow("L07-L08-cmd-check_pages_dag_projects", "tools/check_pages.py --all, check_dag.py --all, check_projects.py --all: AC2 PASS in each, exit 0 (logs/check_pages.txt, check_dag.txt, check_projects.txt).")
over["L07-L08-cmd-lint_mypy"] = passrow("L07-L08-cmd-lint_mypy", "ruff check on both twins: 'All checks passed!' exit 0; ruff format --check: '2 files already formatted' exit 0; mypy --no-incremental on both twins: 'Success: no issues found in 2 source files' (logs/ruff_check.txt, ruff_format.txt, mypy.txt).")
over["L07-L08-cmd-pytest"] = passrow("L07-L08-cmd-pytest", ".venv/bin/pytest -q -k 'AC2 or ac2 or L07 or L08': all dots, exit 0 (logs/pytest.txt). (Shell 'timeout' is not installed on this machine; the run was repeated without it.)")
over["L07-L08-cmd-verify_refs"] = passrow("L07-L08-cmd-verify_refs", "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'; tools/verify_refs.py --unit AC2 (live, Crossref): 'live re-verification of AC2: 7 of 560 entries, 0 problems'; both exit 0 (logs/verify_refs_*.txt).")

# ---- citations ----
over["L07-L08-cite-piotroski2000value"] = passrow("L07-L08-cite-piotroski2000value", "references/references.json key piotroski2000value re-read: verified_by crossref, title 'Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers', author Piotroski, Journal of Accounting Research 38, DOI 10.2307/2672906. Matches the lesson's citation. Paper text re-read by plain curl (Ivey-hosted PDF, HTTP 200; ledgers/AC2/scripts/L07-L08-r4/ and /tmp/ac2-v/L07-L08-r4/piotroski-layout.txt).")
over["L07-L08-cite-sloan1996stock"] = passrow("L07-L08-cite-sloan1996stock", "references/references.json key sloan1996stock re-read: crossref, Accounting Review 71(3), DOI 10.2308/tar-9608042309. L07 line 108 attributes the claim to Piotroski p. 8 citing Sloan; Piotroski PDF p. 8 re-read: 'Sloan [1996] shows that earnings driven by positive accrual adjustments ... is a bad signal about future profitability'. Sloan's own passage not read; the lesson says so.")
over["L07-L08-cite-beneish1999detection"] = passrow("L07-L08-cite-beneish1999detection", "references/references.json key beneish1999detection re-read: crossref, title 'The Detection of Earnings Manipulation', Financial Analysts Journal, volume 55, issue 5, pages 24-36, DOI 10.2469/faj.v55.n5.2296; author list Beneish only. L08 line 56 states the same bibliographic data. The model content is not verified (registry_flags).")
over["L07-L08-loc-p1-p3-7.5-23"] = passrow("L07-L08-loc-p1-p3-7.5-23", f"{L07} line 104 claim span re-read: 'mean-return gain of at least 7.5% a year ... and a 23% annual return to a long-short strategy over 1976 to 1996'. Piotroski PDF p. 1 abstract: 'increased by at least 7.5% annually' and 'generates a 23% annual return between 1976 and 1996'; p. 3 repeats both (pdftotext -layout). The period is attached only to the 23%, as the paper's sentences do.")
over["L07-L08-loc-p12-1448-396"] = passrow("L07-L08-loc-p12-1448-396", f"{L07} line 106 re-read; PDF p. 12: 'number of observations equals 1,448 and 396, respectively' (pdftotext -layout).")
over["L07-L08-loc-p7-n2-optimal"] = carry("L07-L08-loc-p7-n2-optimal", L07, "98")
over["L07-L08-loc-p9-n5-cutoff"] = carry("L07-L08-loc-p9-n5-cutoff", L07, "341 (unchanged; the key-results rows 432-435 are re-verified under L07-L08-grade-L07)")
over["L07-L08-loc-p7-ex-ante-quote"] = carry("L07-L08-loc-p7-ex-ante-quote", L07, "102")
over["L07-L08-loc-p7-distress-average"] = carry("L07-L08-loc-p7-distress-average", L07, "102")
over["L07-L08-loc-keyresults-2.3"] = passrow("L07-L08-loc-keyresults-2.3", f"{L07} key-results row 1 locator 'Piotroski (2000), §2.3, pp. 6-10' re-read: PDF p. 6 heading '2.3 FINANCIAL PERFORMANCE SIGNALS USED TO DIFFERENTIATE HIGH BM FIRMS'; the signal definitions run pp. 6-10 (pdftotext). The row's separate claim 'matches the paper's conditions' is FAILed as L07-L08-r4-signals-match-claim.")
over["L07-L08-loc-signal-groups"] = passrow("L07-L08-loc-signal-groups", f"{L07} line 86: PDF p. 8 heading '2.3.2 Financial Performance Signals: Leverage, Liquidity, and Source of Funds' (pdftotext -layout, p. 8); the three groups are the paper's (§2.3.1-2.3.3).")
over["L07-L08-loc-scaling-p7-p8-p9"] = carry("L07-L08-loc-scaling-p7-p8-p9", L07, "65")
over["L07-L08-loc-proxies-p7-p8-p9"] = passrow("L07-L08-loc-proxies-p7-p8-p9", f"{L07} §2 items 1-3 (lines 93-95) re-read: item 1 NI before extraordinary items (PDF p. 7, verified); item 2 EQOFFER 'did not issue common equity in the year preceding portfolio formation' (PDF p. 9, verified line 400-401 of the layout text); item 3 ALEVER on total long-term debt over average total assets (PDF p. 8, verified).")
over["L07-L08-loc-p11-sample"] = passrow("L07-L08-loc-p11-sample", f"{L07} line 102 and line 410-411 (R1): PDF p. 11 '3.1 SAMPLE SELECTION: Each year between 1976 and 1996 ... highest BM quintile'; '14,043 high BM firms across the 21 years'; p. 11 '3.2 CALCULATION OF RETURNS ... one-year (two-year) buy-and-hold returns earned from the beginning of the fifth month' (R1 text verified).")
over["L07-L08-loc-p12-groups-bootstrap"] = passrow("L07-L08-loc-p12-groups-bootstrap", f"{L07} lines 106, 419 and misconception 3 (line 356): PDF p. 12 'FSCORE equals 8 or 9' high group and 'FSCORE equals 0 or 1' low group; bootstrap of pseudo-portfolios with 1,448 and 396 observations (pdftotext p. 12).")
over["L07-L08-loc-sloan-p8"] = passrow("L07-L08-loc-sloan-p8", f"{L07} line 108 locator 'Piotroski p. 8, citing Sloan (1996)': PDF p. 8 'Sloan [1996] shows that earnings driven by positive accrual adjustments ... is a bad signal' (pdftotext).")
over["L07-L08-loc-access-claims-L08"] = passrow("L07-L08-loc-access-claims-L08", f"{L08} line 93 access statements re-run by plain curl this round: doi.org/10.2469/faj.v55.n5.2296 -> 302 to tandfonline.com; tandfonline full-text URL -> 403; ResearchGate search -> 403; SSRN paper URL -> 403; JSTOR 2672906 -> 200 with 'Challenge' / 'enable JavaScript' page. Statements match.")
over["L07-L08-loc-beneish-constants-label"] = passrow("L07-L08-loc-beneish-constants-label", f"Every place the constants or the -1.78 threshold appear is labelled: {L08} lines 56, 60, 89, 93-97 (UNCONFIRMED / candidate wording), 421-436 (§3 worked M, 'With the unconfirmed candidate constants'), 488 (misconception 2), 530 (E1), 566-567 (key results, C and D), 609 (quiz 5, 'The constants are unconfirmed'); lab docstring lines 114-118 and constants 133-144 (UNCONFIRMED). Round-4 line numbers.")
over["L07-L08-beneish-published-wording"] = carry("L07-L08-beneish-published-wording", L08, "56 and 60 (key-results row at line 566 is re-verified under L07-L08-grade-L08)")
over["L07-L08-beneish-cutoffs"] = carry("L07-L08-beneish-cutoffs", L08, "97")
over["L07-L08-beneish-tata-disagreement"] = passrow("L07-L08-beneish-tata-disagreement", f"{L08} R1 solution (line 545) now says 'The intercept and all eight weights come from the same single secondary page, so the whole set needs checking against the paper, not only the TATA weight.' Consistent with line 93 (one page, nine values).")
over["L07-L08-build-report-refs"] = passrow("L07-L08-build-report-refs", f"{L07} line 344 and {L08} line 478 each point once to plans/AC2-open-items.md (grep -c: 1 per page). Open-items rows for Mohanram 2005, Dechow/Beneish-Lee-Nichols and joint use are present (plans/AC2-open-items.md lines 17-19, 25). Neither page names those works in its text.")

# ---- math ----
over["L07-L08-math-signals-vs-contract"] = passrow("L07-L08-math-signals-vs-contract", f"{L07} lines 56-86: the ratios and table conditions (s1-s9) compared with atlas/A15.contract.md piotroski_f_score (lines 135-143): same conditions, same scaling (beginning assets for ROA, CFO, ATO; average assets for LEV). The paper-match claim is FAILed separately (L07-L08-r4-signals-match-claim).")
over["L07-L08-math-proxies-stated"] = passrow("L07-L08-math-proxies-stated", f"{L07} §2 (lines 90-96) vs atlas/A15.contract.md 'Departures from the published definitions' (lines 162-169): three proxies named (NI tag, equity proxy, debt tag) with the same page locators (p. 7-8, p. 9, p. 8). Consistent.")
over["L07-L08-math-P1"] = passrow("L07-L08-math-P1", f"{L07} P1 (lines 378-381) re-proved: s4=1 iff CFO_t/TA_{{t-1}} > NI_t/TA_{{t-1}} iff CFO_t > NI_t (TA_{{t-1}} > 0). Paper ACCRUAL and F-ACCRUAL (PDF p. 8) checked.")
over["L07-L08-math-P2"] = passrow("L07-L08-math-P2", f"{L07} P2 (lines 382-385): each signal is an indicator; the ratios are money/money and invariant; s7 compares counts. Re-checked by the scale line of lab-AC2-L07-1 (400/400 unchanged, logs/twin-L07.txt).")
over["L07-L08-math-P3"] = passrow("L07-L08-math-P3", f"{L07} P3 (lines 386-389): recomputed exactly (recompute.py): LEV_t = 300/950 = 0.3158, LEV_t-1 = 310/1050 = 0.2952, so s5 = 0 although debt fell. Matches.")
over["L07-L08-math-worked-firm"] = passrow("L07-L08-math-worked-firm", f"{L07} §4 (lines 307-335), M1 (364-366), M2 (368-370), M3 (372-374), E2 (398-400), recomputed with exact Fractions (recompute.py, logs/recompute.txt): ROA_t 0.10636, ROA_t-1 0.0660, CFO* 0.08727, LEV 0.22957/0.31429, CR 2.2/2.0, GM 0.35/0.30, ATO 1.4182/1.32; vector (1,1,1,0,1,1,1,1,1), F=8; M2 (0,1,0,1,1,1,1,1,1), F=7; E2 118/1100=0.10727 > 0.10636; E3 LEV 300/1150=0.2609 < 0.3143.")
over["L07-L08-math-E1-count"] = passrow("L07-L08-math-E1-count", f"{L07} E1 (line 396): lab output lists 24 at score 8 and 7 at score 9, 31/400 = 0.0775 (logs/twin-L07.txt lines 'score 8: 24', 'score 9: 7').")
over["L07-L08-misconception-score-zero"] = failrow("L07-L08-misconception-score-zero", f"{L07} misconception 1 (line 352) and card AC2-c103",
    "2.4-math",
    "Line 352 now reads 'The score mixes sign tests (s1, s2, s4) and change tests (s3, s5 to s9).' s4 is CFO*_t > ROA_t, a comparison of two same-year levels (P1: s4=1 iff CFO_t > NI_t). The same paragraph calls s4 'a level test', and the lesson's §1 table gives no sign condition for it. The paragraph therefore contradicts itself. The same terms differ across pages: L07 line 341 calls s1, s2 'sign tests at zero'; L08 line 443 calls s1, s2, s4 'level tests'. The F=2 example itself was recomputed and is correct (s1=s2=1, s3=s4=...=s9=0).",
    "Use one taxonomy on both pages: s1 and s2 are sign tests at zero; s4 is a same-year level comparison; s3 and s5-s9 are change tests. In line 352 write 'The score mixes sign tests (s1, s2), a same-year comparison (s4) and change tests (s3, s5 to s9).' Make L08 line 443 use the same words.")
over["L07-L08-math-L08-indices"] = passrow("L07-L08-math-L08-indices", f"{L08} lines 78-85 (eight index definitions) vs atlas/A15.contract.md beneish_m_score (lines 146-154) and the lab's beneish_indices (lab lines 197-210): identical formulas (DSRI, GMI, AQI, SGI, DEPI, SGAI, LVGI, TATA).")
over["L07-L08-math-prop4.2"] = passrow("L07-L08-math-prop4.2", f"{L08} Proposition 4.2 (lines 446-449) and proof (450-453) re-read: Bayes and total probability steps are valid; formula ps/(ps+(1-p)(1-sigma)) recomputed (0.0917 at p=0.01, sigma=0.95, s=0.5).")
over["L07-L08-math-prop4.3"] = passrow("L07-L08-math-prop4.3", f"{L08} Proposition 4.3 (lines 457-464): AND f1 f2 and OR 1-(1-f1)(1-f2) under independence. Recomputed: 0.0050 and 0.1450 (lab output).")
over["L07-L08-math-L08-P3"] = passrow("L07-L08-math-L08-P3", f"{L08} P3 (lines 520-523): AND sensitivity <= min(s1,s2) and OR sensitivity >= max(s1,s2) hold without independence (both are set inclusions).")
over["L07-L08-math-worked-M"] = passrow("L07-L08-math-worked-M", f"{L08} §3 (lines 417-439): every index recomputed exactly (DSRI 1.5, GMI 1.142857, AQI 1.083333, SGI 1.2, DEPI 1.090909, SGAI 1.0, LVGI 0.979167, TATA 0.033333). M exact = -1.559271 -> -1.5593. Displayed terms (line 436 with four-decimal indices, unrounded products) sum to -1.559430 -> -1.5594 as stated at line 437 and quiz item 5. Recompute in logs/recompute.txt.")
over["L07-L08-math-base-rate-table"] = passrow("L07-L08-math-base-rate-table", f"{L08} lab base-rate table (lab lines 306-320 and output 399-409) recomputed with Fractions for all nine rows: PPV and false flags per 1000 match (e.g. 0.001/0.95 -> 0.0099, 49.95; 0.01/0.95 -> 0.0917, 49.50; 0.05/0.95 -> 0.3448, 47.50).")
over["L07-L08-math-E2-E3-E1"] = passrow("L07-L08-math-E2-E3-E1", f"{L08} E1 (527-530): -1.5067 - (-2.4747) = 0.9680. E2 (531-534): 0.3448/0.0099 = 34.8, about 35 (exact-fraction ratio 34.79). E3 (535-538): corrected to per 1,000 clean firm-years = 1000 x FPR = 50; population count 49.50 explained by 1-p = 0.99. Correct.")
over["L07-L08-math-dependence-sign"] = passrow("L07-L08-math-dependence-sign", f"{L08} §4 dependence paragraph (line 466, sign of dependence only), misconception 3 (line 490) and quiz item 10 (line 654). Re-derived: positive correlation raises P(A and B) above f1 f2 and lowers P(A or B) below f1+f2-f1f2; example f1=0.10, f2=0.05 with disjoint flags gives AND 0 and OR 0.15. The scale-related claim on the same line is FAILed separately (L07-L08-r3-margin-overlap).")
over["L07-L08-math-growth-claim"] = passrow("L07-L08-math-growth-claim", f"{L08} §5 'Growth is a confound' (line 476): witness revenue 1000->1500, receivables 100->150, SG&A 150->225 gives DSRI = 1.0 and SGAI = 1.0 (recomputed exactly) and SGI = 1.5. Card AC2-c118 same.")

# ---- lab ----
over["L07-L08-lab-L07-1"] = passrow("L07-L08-lab-L07-1", f"{L07} hypothesis (line 114) and lab note (line 110) now claim only the scale-invariance check and the printed distribution; the 0-9 range is attributed to proof P2. lab-AC2-L07-1 code (lines 115-281) has no range assertion. Output reproduced (embed check True; twin run exit 0). Interpretation (line 302) consistent.")
over["L07-L08-lab-L08-1-overreach"] = passrow("L07-L08-lab-L08-1-overreach", f"{L08} hypothesis (line 106) now says 'higher median M' (lab output: planted -1.5067 vs clean -2.4747) and names sensitivity 0.5 with PPV 0.0917 at prevalence 0.01, specificity 0.95; PPV defined in Definition 4.1 (line 101). Lab main() prints 'section 4 check ... True' (lines 368-372). Interpretation (line 413) says the separation is a property of the generator.")
over["L07-L08-lab-L08-1-run"] = passrow("L07-L08-lab-L08-1-run", f"lab-AC2-L08-1 run (logs/twin-L08.txt) and printed labels (lab lines 352-383) match {L08} lines 384-412 (embed check True).")
over["L07-L08-num-L07-lab-distribution"] = passrow("L07-L08-num-L07-lab-distribution", f"{L07} lab output lines 289-300 (score distribution, mean 5.6475, 400/400) reproduced by the twin run (logs/twin-L07.txt).")

# ---- grades ----
over["L07-L08-grade-L07"] = passrow("L07-L08-grade-L07", f"{L07} key-results rows (lines 428-436): T rows are P1, P2 and the worked/M2 arithmetic; C rows are paper claims with locators (p. 1, 3, 7, 8, 9, 12). Row 1 still says the contract 'matches the paper's conditions' (FAILed as L07-L08-r4-signals-match-claim); the grade itself is consistent.")
over["L07-L08-grade-L08"] = passrow("L07-L08-grade-L08", f"{L08} key-results (lines 562-568): the constants row now says 'candidate values from one secondary web page' (C); threshold row D; T rows are Definition 1.1, Propositions 4.2 and 4.3 and P3; registry row C. Consistent with §2.")
over["L07-L08-struct-sections"] = passrow("L07-L08-struct-sections", "tools/page_smoke.py PASS on both pages; check_pages AC2 PASS; section list and numbering checked by reading (§1-§10, problem tiers M/P/E/R).")
over["L07-L08-struct-counts"] = passrow("L07-L08-struct-counts", "check_pages AC2 PASS; quiz items: L07 10 items, L08 10 items (read in full).")
over["L07-L08-struct-banned-phrases"] = passrow("L07-L08-struct-banned-phrases", "Case-insensitive grep of both pages for TODO, TBD, lorem, 'for brevity', 'beyond the scope', 'roughly', 'historically', 'typically', 'clearly', 'obviously', 'it is important', 'studies show': no hit. Remaining 'about' uses are arithmetic (E2 'about 35', quiz 'about 0.09' with its explanation 0.0917). Ellipses in L07 are Python code or the sentence 'such as ... '.")
over["L07-L08-struct-uses-metadata"] = passrow("L07-L08-struct-uses-metadata", f"{L07} line 38 and {L08} line 38 'Uses' links resolve to L02/L04/concepts; no change this round.")
over["L07-L08-dag-check_dag"] = passrow("L07-L08-dag-check_dag", "tools/check_dag.py --all: 'check_dag AC2: PASS', exit 0 (logs/check_dag.txt).")
over["L07-L08-dag-order"] = passrow("L07-L08-dag-order", f"Concept links in {L07} and {L08} (financial-ratio-analysis, accruals, accrual-accounting, bayesian-inference, robust-statistics, bootstrap, piotroski-f-score, beneish-m-score) point to earlier lessons or defined concepts; no new concept introduced before use this round (Definition 4.1 with PPV now precedes the lab, line 101 vs 104).")
over["L07-L08-hours"] = passrow("L07-L08-hours", f"{L07} data-hours=10 and {L08} data-hours=12 unchanged this round. Own estimate: L07 reading of 12 paper pages plus lab and 17 problems about 10 h; L08 about 12 h. Within +/-30 percent.")

# ---- cards ----
over["L07-L08-cards-L07-A"] = passrow("L07-L08-cards-L07-A", "cards.json AC2-c089 to c101 (L07) checked against their lesson text. c094 and c097 changed: c097 now attributes the 7.5% gain to the 'high book-to-market sample over 1976 to 1996' with locators 'Abstract, p. 1; sample period p. 11'; the sample period is on PDF p. 11 and the 7.5% is the abstract's high-BM result. Other cards match (c089 omits the group name 'source of funds', no error). Carried unchanged: c089-c093, c095, c096, c098-c101 (byte-identical since 4a8690a).")
over["L07-L08-cards-L07-B"] = failrow("L07-L08-cards-L07-B", "cards.json AC2-c130 (L07); c102-c105, c126, c127 checked and correct", "2.7-cards",
    "AC2-c130 asks 'Do the contract's nine signal conditions match the paper's' and answers 'They match the paper's conditions as the lesson reads them ... Graded C.' Lesson §2 and atlas/A15.contract.md (lines 162-169) say the equity signal s7 is a proxy: it tests shares outstanding, while the paper's EQOFFER tests common equity issuance (PDF p. 9). The answer omits this exception. c102 (F=8), c103 (F=2 example, recomputed), c104 (400/400), c105, c126 (1,448/396, p. 12), c127 (F=7 recomputed) are correct.",
    "Rewrite c130: 'Do the contract's conditions match the paper's?' -> 'Six conditions (s1-s6, s8, s9) match the paper's definitions, with the input tags of §2; s7 is a share-count proxy for the paper's EQOFFER (§2, item 2). Graded C.'")
over["L07-L08-cards-L08-A"] = passrow("L07-L08-cards-L08-A", "cards.json AC2-c106 to c115 and c129 (L08) checked against L08 text: c107 'the intercept and all eight weights come from one secondary web page' matches §2; c109 D grade matches §2; c110-c112 match Propositions 4.2, 4.3 and P3; c113-c114 match the base-rate table (0.0917; PPV below 0.1 at prevalence 0.001 for specificity up to 0.95); c108 matches registry; c115, c129 correct.")
over["L07-L08-cards-L08-B"] = passrow("L07-L08-cards-L08-B", "cards.json AC2-c116 to c119 checked: c116 matches §4 and misconception 3; c117 medians -2.4747 and -1.5067 match the lab output; c118 numbers recomputed (DSRI = SGAI = 1.0, SGI = 1.5); c119 matches the corrected bullet (TATA scaled by total assets, net income less CFO). The c119 claim is correct; the lesson bullet it mirrors is FAILed separately (L07-L08-r2-balance-sheet-accrual).")
over["L07-L08-cards-coverage"] = passrow("L07-L08-cards-coverage", "cards.json L08 cards (c106-c119, c129, c131-c133, c139, c140) vs Definition 4.1 (lines 99-102): PPV, AND and OR rules now have cards c139, c140; prevalence (c129), sensitivity (c131), specificity (c132), screen (c133) cover Definition 4.1.")
over["L07-L08-cards-dupes"] = passrow("L07-L08-cards-dupes", "ledgers/AC2/scripts/L07-L08-r4/card_scan.py over course/modules/AC/AC2/cards.json: 140 cards, ids c001-c140 each once, no duplicate front or back text (logs/card_scan.txt).")
over["L07-L08-rubric-or-project"] = passrow("L07-L08-rubric-or-project", "Not applicable: this slice has no project and no grader; checked that L07 and L08 contain no project section.")

# ---- round-2 rows ----
over["L07-L08-r2-us-claim"] = passrow("L07-L08-r2-us-claim", f"grep -c 'U\\.S\\.' on {L07} and {L08}: 0 hits.")
over["L07-L08-r2-uncited-assertions"] = passrow("L07-L08-r2-uncited-assertions", f"{L08} why-it-matters (line 52) now reads 'A screen that flags manipulators also flags firms that are not manipulating' with the rate and prevalence cited to Proposition 4.2; the 'many firms' count is gone.")
over["L07-L08-r2-paper-design-claim"] = carry("L07-L08-r2-paper-design-claim", L08, "474 ('The paper's sample design is not confirmed, so no prevalence from the paper is used.')")
over["L07-L08-r2-constants-provenance"] = failrow("L07-L08-r2-constants-provenance", f"{L08} line 93 (and key-results row 566)", "2.1-citation",
    "Line 93 says the page 'cites other sources for its coefficient formula and does not cite the 1999 paper for it'. Re-fetched by plain curl (HTTP 200, 2026-10-27). The footnote numbering: the formula sentence and the 8-variable sentence cite [1] and [2]. Reference [1] is 'Messod D. Beneish. \"The Detection of Earnings Manipulation\". Scribd. Retrieved 2017-01-08', i.e. an undated Scribd copy with the 1999 paper's title and author; reference [2] is ycharts.com. The page gives no journal, volume or locator for the formula. So 'does not cite the 1999 paper' is not supported: the formula is cited to a Scribd document under the paper's title. (The round-3 note that [1] is ycharts misread the numbering.) Line 93 also says 'Secondary web sources give' (plural) for one page.",
    "Replace the clause with the page's actual citation: 'the coefficient formula is cited to an undated Scribd document titled The Detection of Earnings Manipulation by Beneish, and to ycharts.com; neither gives a journal locator'. Change 'Secondary web sources give' to 'The page gives'. Keep the UNCONFIRMED grade D/C wording.")
over["L07-L08-r2-balance-sheet-accrual"] = failrow("L07-L08-r2-balance-sheet-accrual", f"{L08} line 477 ('Accruals are measured twice' bullet)", "2.4-math",
    "Line 477 says TATA 'is the cash-flow accrual measure of the A15 contract's earnings-quality section (atlas/A15.contract.md)'. The contract's section (atlas lines 108-131) defines accruals_cash_flow = (net_income - cfo) / AVERAGE total_assets; TATA (contract line 154, M-score section) is (net_income - cfo) / total_assets at t, year-end. The two measures have the same numerator but a different denominator, so the lesson's 'it is the ... measure' is an identity the contract does not state. (Card AC2-c119 and §1 line 89 are correct.)",
    "Write: 'TATA has the numerator of the contract's cash-flow accrual measure (accruals_cash_flow, atlas lines 108-111) but divides by year-end total assets, not average total assets (atlas line 154).'")
over["L07-L08-r2-def41-before-use"] = passrow("L07-L08-r2-def41-before-use", f"{L08} Definition 4.1 (lines 99-102) now defines PPV, AND and OR rules; the first use in the lab hypothesis (line 106) and table header (line 373) comes after it.")
over["L07-L08-r2-lab-L08-table-claim"] = passrow("L07-L08-r2-lab-L08-table-claim", f"{L08} lab hypothesis (line 106) now states sensitivity 0.5 with the PPV 0.0917 (prevalence 0.01, specificity 0.95); lab base-rate section hard-codes sensitivity 0.5 (lab line 312), consistent.")
over["L07-L08-r2-threshold-row"] = passrow("L07-L08-r2-threshold-row", f"{L08} key-results threshold row (line 567): 'one secondary web page gives -1.78; not confirmed against the paper', grade D, consistent with §2 line 97.")
over["L07-L08-r2-wiki-constants"] = passrow("L07-L08-r2-wiki-constants", f"Wikipedia 'Beneish M-score' re-fetched by plain curl this round (HTTP 200): formula 'M-score = -4.84 + 0.92 x DSRI + 0.528 x GMI + 0.404 x AQI + 0.892 x SGI + 0.115 x DEPI -0.172 x SGAI + 4.679 x TATA - 0.327 x LVGI'; threshold 'The threshold value is -1.78'. 4.697 and -2.22: absent. {L08} lines 93-97 and lab constants 133-144 match.")
over["L07-L08-r2-jstor-statement"] = passrow("L07-L08-r2-jstor-statement", f"{L07} line 104 'The JSTOR record ... could not be read (bot check)': plain curl of jstor.org/stable/2672906 returns 200 with a Challenge page ('enable JavaScript'). Statement matches.")
over["L07-L08-r2-process-words"] = passrow("L07-L08-r2-process-words", f"Case-insensitive grep on {L07}, {L08} and cards.json AC2-c089..c140 for builder, this build, REQUEST, unit report: no hit. plans/AC2-open-items.md referenced once per page.")
over["L07-L08-r2-lab-numbering"] = carry("L07-L08-r2-lab-numbering", f"{L07} and {L08}", "lab headings 'Lab 1 · ...' (L07 line 113, L08 line 105)")
over["L07-L08-r2-links"] = carry("L07-L08-r2-links", f"{L07} and {L08}", "all links; check_pages AC2 PASS re-run this round (logs/check_pages.txt)")
over["L07-L08-r2-bayes-S1-and-total-probability"] = passrow("L07-L08-r2-bayes-S1-and-total-probability", f"{L08} Bayesian-inference link (line 455) and Proposition 4.2 proof (line 452: Bayes' rule and total probability stated before use).")
over["L07-L08-r2-quiz-keys"] = passrow("L07-L08-r2-quiz-keys", f"{L07} quiz (lines 444-518): keys 1 (CFO*>ROA), 2 (0.10636 vs 117/1100), 3 (high BM 1976-1996, p. 11), 4 (8), 5 (ratios cancel), 6 (possibly 0), 7 (equity signal tests shares, not issuance), 8 (C-graded 1976-1996 result), 9 (7), 10 (cutoffs are a choice) all verified. {L08} quiz (lines 575-655): PPV 0.0917 (tolerance 0.0005), AND 0.0050, sensitivity bound, M -1.5593 (tolerance 0.0005), DSRI, prevalence, planted gap, positive correlation: verified.")

# ---- round-3 rows ----
over["L07-L08-r3-piotroski-fetch"] = passrow("L07-L08-r3-piotroski-fetch", "Piotroski (2000) PDF re-fetched by plain curl this round: HTTP 200, application/pdf (Ivey-hosted URL; ledgers/AC2/scripts/L07-L08-r2/make_fragment_r2.py). pdftotext -layout read for pp. 1-14.")
over["L07-L08-r3-quotes"] = passrow("L07-L08-r3-quotes", f"{L07} claim quotations re-checked against PDF text: p. 7 'the stated ex ante implication of each signal is conditioned on the fact that these firms are financially distressed at some level'; p. 7 n. 2 'factor analysis may more aptly extract an optimal combination of signals'; p. 9 n. 5 'stronger return results than the liquidity metric and aggregate score used in the paper'.")
over["L07-L08-r3-wiki-fetch"] = passrow("L07-L08-r3-wiki-fetch", "Wikipedia 'Beneish M-score' (https://en.wikipedia.org/wiki/Beneish_M-score), plain curl, HTTP 200, read 2026-10-27 (round 4 re-read). Constants and -1.78 present; 4.697 and -2.22 absent (wiki.html grep). Footnote numbering checked; see L07-L08-r2-constants-provenance for the citation point.")
over["L07-L08-r3-access"] = passrow("L07-L08-r3-access", "Access statuses re-run this round by plain curl (see L07-L08-loc-access-claims-L08): 302 then 403 (tandfonline), 403 (ResearchGate), 403 (SSRN), JSTOR 200 challenge.")
over["L07-L08-r3-recompute-L07"] = passrow("L07-L08-r3-recompute-L07", f"Independent exact recomputation (ledgers/AC2/scripts/L07-L08-r4/recompute.py, logs/recompute.txt) of {L07} worked firm, M1-M3, E1-E3, P3 and the misconception example (ROA 0.15 vs 0.20). All match.")
over["L07-L08-r3-recompute-L08"] = passrow("L07-L08-r3-recompute-L08", f"Exact recomputation of {L08} §3 worked M (-1.559271 exact; -1.559430 with displayed-term products), the base-rate table, E1-E3, AND/OR, growth witness and the PPV quiz value (logs/recompute.txt). All match.")
over["L07-L08-r3-contract-departures"] = passrow("L07-L08-r3-contract-departures", f"atlas/A15.contract.md 'Departures from the published definitions' (lines 162-169) vs {L07} §2 (lines 90-96): NI tag, equity proxy (shares rise, p. 9), debt tag (p. 8). Match.")
over["L07-L08-r3-registry-no-fscore-study"] = passrow("L07-L08-r3-registry-no-fscore-study", "references/references.json (560 entries): keyword scan for f-score, fscore, piotroski, beneish returns only beneish1999detection and piotroski2000value. No out-of-sample F-score study is registered. Matches L07 line 344.")
over["L07-L08-r3-open-items-content"] = passrow("L07-L08-r3-open-items-content", "plans/AC2-open-items.md: rows for Beneish (line 16), Mohanram 2005 (line 17), Dechow, Ge, Larson & Sloan 2011 (line 18), Beneish, Lee & Nichols 2013 (line 19), out-of-sample F-score tests (line 25), joint use (line 26). Each marked OPEN; these names appear only in that file (ruling 2).")
over["L07-L08-r3-from-recall-L07"] = passrow("L07-L08-r3-from-recall-L07", f"{L07} line 344 now says 'A search for out-of-sample tests is an open item listed in plans/AC2-open-items.md; none is read here.' No author or year typed into learner text (grep: Mohanram, Dechow, Lee, Vorst: 0 hits in L07, L08, cards.json).")
over["L07-L08-r3-from-recall-L08"] = passrow("L07-L08-r3-from-recall-L08", f"{L08} line 478 now says 'Studies of the joint use are an open item listed in plans/AC2-open-items.md; none is read here.' No names in learner text (grep 0 hits).")
over["L07-L08-r3-stock-funded-example"] = passrow("L07-L08-r3-stock-funded-example", f"{L07} §2 item 2 (line 94) now gives a stock split (rise in shares with no common equity issued) as the disagreement example and drops the stock-funded acquisition. A stock-funded acquisition is an equity issuance, so the two agree; the new example is the one that disagrees. The paper's EQOFFER definition (PDF p. 9) supports the consequence: no common equity issued means EQOFFER = 1.")
over["L07-L08-r3-lab-checks-integer"] = passrow("L07-L08-r3-lab-checks-integer", f"{L07} line 110 and hypothesis (line 114) now list only the scale check and the distribution; the 0-9 range is attributed to P2. Code (lab lines 115-281) has no range check; claim matches.")
over["L07-L08-r3-lab-docstring-pages"] = passrow("L07-L08-r3-lab-docstring-pages", "lab-AC2-L07-1 docstring (lines 119-120) now reads 'pp. 7-10 (printed pages)'. PDF printed page headers equal PDF page numbers for pp. 1-14 (pdftotext); the definitions run pp. 7 (ROA, CFO), 8 (ACCRUAL, leverage, source of funds), 9 (EQOFFER, liquidity), 10 (composite). Correct.")
over["L07-L08-r3-period-7.5"] = passrow("L07-L08-r3-period-7.5", f"{L07} line 104 claim span now attaches 1976-1996 only to the 23% strategy; key-results row (line 432) drops the period from the 7.5%. Card c097 places the 7.5% in 'the high book-to-market sample over 1976 to 1996' with 'sample period p. 11' (PDF p. 11: 'Each year between 1976 and 1996' and '14,043 high BM firms across the 21 years'). Accepted as the sample attribution.")
over["L07-L08-r3-R2-track-growth"] = passrow("L07-L08-r3-R2-track-growth", f"{L08} R2 solution (line 549) now says SGI is 'the growth term' and DSRI and SGAI respond to receivables or SG&A growing relative to revenue (§5). Consistent with §5 line 476 and the witness.")
over["L07-L08-r3-signs-of-improvement"] = passrow("L07-L08-r3-signs-of-improvement", f"{L08} §4 (line 443) now: 'counts favourable signs ... some are level tests (s1, s2, s4) and the rest are change tests'. Consistent with the change-test/level-test split (see L07-L08-misconception-score-zero for the L07 wording to fix).")
over["L07-L08-r3-margin-overlap"] = failrow("L07-L08-r3-margin-overlap", f"{L08} §4 paragraph (line 466)", "2.4-math",
    "The rewritten sentence says 'the F-score's ROA and CFO are scaled by total assets, the same base as the M-score's indices.' Two errors. (1) ROA and CFO are scaled by BEGINNING-of-year total assets (L07 §1 lines 58-59; contract lines 136-138), whereas TATA, AQI and LVGI use year-end TA_t. (2) Not all eight M-score indices use total assets: DSRI, GMI, SGI and SGAI use revenue or gross margin, DEPI uses depreciation and PP&E (L08 lines 78-85; lab lines 197-210). The 'same base' claim is therefore false as written.",
    "Delete the scaling clause, or write: 'ROA and CFO are scaled by beginning-of-year total assets, and TATA, AQI and LVGI by year-end total assets.'")
over["L07-L08-r3-eight-year-on-year"] = passrow("L07-L08-r3-eight-year-on-year", f"{L08} why-it-matters (line 52) now: 'eight ratios, seven of them year-on-year'. TATA (single-year, line 89) is the one not year-on-year; the seven others compare year t with t-1 (checked against lines 78-85).")
over["L07-L08-r3-weights-only-source"] = passrow("L07-L08-r3-weights-only-source", f"{L08} line 89 now: 'The intercept and the eight weights are the numbers that depend on the source, and they cannot yet be confirmed.' The intercept is included (contract BENEISH_INTERCEPT, line 158).")
over["L07-L08-r3-used-in-lab-only"] = passrow("L07-L08-r3-used-in-lab-only", f"{L08} line 95 now: 'They are used only to show the arithmetic, always under the UNCONFIRMED label: in the lab, in the §3 worked M, in misconception 2 and in quiz item 5.' Checked: lab (lines 133-144), §3 (lines 431-436), misconception 2 (line 488, '-1.5593'), quiz item 5 (line 607-609). Also E1 (lab output) and the key-results row; no other use found.")
over["L07-L08-r3-PPV-before-defined"] = passrow("L07-L08-r3-PPV-before-defined", f"PPV defined in {L08} Definition 4.1 (line 101), before the lab (line 104) and its hypothesis (line 106) and table header (line 373). Proposition 4.2 (line 447) gives the formula.")
over["L07-L08-r3-as-much-as"] = passrow("L07-L08-r3-as-much-as", f"{L08} §4 (line 455) now: 'Proposition 4.2 shows that the PPV depends on both prevalence and specificity.' The 'as much as' comparison is gone.")
over["L07-L08-r3-lab-docstring-follows-beneish"] = passrow("L07-L08-r3-lab-docstring-follows-beneish", f"lab-AC2-L08-1 docstring (lines 110-112) now: 'Index definitions are the contract's definitions (atlas/A15.contract.md, beneish_m_score); the paper's own definitions were not read.' No claim that they follow Beneish (1999).")
over["L07-L08-r3-prop-4.2-page-locator"] = carry("L07-L08-r3-prop-4.2-page-locator", L08, "54-56 and 438 (unchanged text)")

# ---- new rows ----
new_rows = [
    failrow("L07-L08-r4-signals-match-claim", f"{L07} key-results row 1 (line 428, Source column '(matches the paper's conditions)') and §2 lead (line 90, 'The contract encodes the paper's conditions')",
        "2.1-citation",
        "Key-results row 1 says the contract's piotroski_f_score 'matches the paper's conditions' at grade C. But §2 (lines 90-95) and the contract's 'Departures' (atlas lines 162-169) say the equity signal s7 is a proxy: it tests shares outstanding did not rise, while the paper's EQOFFER is 1 when the firm 'did not issue common equity in the year preceding portfolio formation' (PDF p. 9, verified). The conditions do not all match; the claim is false for s7 and needs its exception.",
        "Write: 'the contract's conditions match the paper's for s1-s6, s8 and s9, with the input tags of §2; s7 is a share-count proxy for EQOFFER (§2, item 2).'"),
    passrow("L07-L08-r4-eqoffer-p9", f"{L07} §2 item 2 (line 94): EQOFFER 'did not issue common equity in the year preceding portfolio formation' verified on PDF p. 9 (pdftotext line 400-401). Buybacks offsetting issuance and a share-count rise without issuance are consequences of that definition; no page of the paper discusses splits."),
    passrow("L07-L08-r4-wiki-threshold-cite", f"{L08} line 97: 'The Wikipedia page gives a threshold of -1.78 ... citing Beneish (1999) without a locator.' Re-fetched page: 'The threshold value is -1.78 for the model whose coefficients are reported above. (see Beneish 1999, Beneish, Lee, and Nichols 2013, and Beneish and Vorst 2020)'. Statement matches; graded D."),
    passrow("L07-L08-r4-pdf-printed-pages", "Piotroski PDF pages 1-14 (pdftotext -layout): the running headers show printed page numbers equal to PDF page numbers (e.g. PDF p. 9 header '9', p. 12 header '12'). Locators p. 1, 3, 6, 7, 8, 9, 11, 12 used in the lesson are therefore the printed numbers."),
]

rows = []
for r in d["rows"]:
    rid = r["id"]
    if rid in over:
        rows.append(over[rid])
    else:
        rows.append(carry(rid, "the slice", "unchanged"))
LOC = {
    "L07-L08-r4-eqoffer-p9": f"{L07} line 94 (§2 item 2); paper PDF p. 9",
    "L07-L08-r4-wiki-threshold-cite": f"{L08} line 97",
    "L07-L08-r4-pdf-printed-pages": "Piotroski (2000) PDF, running headers pp. 1-14",
}
for nr in new_rows:
    if not nr.get("location"):
        nr["location"] = LOC[nr["id"]]
rows += new_rows
missing = [i for i in over if i not in old and i not in {x["id"] for x in new_rows}]
assert not missing, missing
frag = {
    "unit": "AC2",
    "slice": "L07-L08",
    "round": 4,
    "verifier": "round-4 independent verifier for slice L07-L08 (did not build AC2; shares no context with the builders or the round-1 to round-3 verifiers)",
    "pin": "2607c60",
    "base": None,
    "previous_ledger": "round 3, pin 4a8690a: 108 rows, 83 PASS, 25 FAIL (overwritten by this round's fragment)",
    "checkout": "/tmp/verify-ac2r4-l78 (detached worktree at 2607c60; .venv symlinked)",
    "scratch": "/tmp/ac2-v/L07-L08-r4",
    "verified_at": "2026-10-27T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "beneish1999detection: registry verifies title, journal, volume 55, issue 5, pages 24-36 (Crossref). Model content (intercept, eight weights, cut-offs) is not verified; the page labels them UNCONFIRMED. The -1.78 threshold and every constant come from one secondary web page (Wikipedia), whose coefficient formula is cited to an undated Scribd copy titled as the paper and to ycharts.com."
    ],
    "freshness_flags": [],
    "notes": (
        "Round 4 (pin 2607c60). Delta read hunk by hunk: L07.html (lines 94, 104, 110, 114, 344, 352, 356, 432), L08.html (lines 52, 89, 93, 95, 101, 106, 443, 455, 466, 477, 478, 545, 549, 536-538, 566), lab-AC2-L07-1.py and lab-AC2-L08-1.py docstrings, and cards c094, c097, c103, c107, c119, c139, c140. "
        "Re-run this round: run_labs AC2, both twins under -I -W error, embed check, page_smoke, check_pages/check_dag/check_projects, ruff check and format, mypy, pytest -k AC2/L07/L08, verify_refs offline and live (AC2). "
        "Plain curl this round: Wikipedia Beneish M-score (200; constants, -1.78, footnote numbering read), Piotroski Ivey PDF (200; pdftotext pp. 1-14), tandfonline/doi/ResearchGate/SSRN/JSTOR statuses. "
        "Exact Fraction recomputation of every worked number, the base-rate table and the M-score (ledgers/AC2/scripts/L07-L08-r4/recompute.py). "
        "Cards: 140 in total; 40 are L07/L08; 14 of the 40 carry no grade field (c089, c090, c103, c106, c115, c116, c118, c119, c129, c131-c133, c139, c140): these are definitional or derived cards; no rule in the brief requires a grade on them, so they are noted, not failed. "
        "Round 3 FAIL rows fixed and re-verified: 22 (see the PASS rows). Still failing: L07-L08-misconception-score-zero (new wording), L07-L08-r2-constants-provenance (new wording, see its evidence), L07-L08-r3-margin-overlap (new wording). New FAIL: L07-L08-r4-signals-match-claim, L07-L08-cards-L07-B (c130), L07-L08-r2-balance-sheet-accrual. "
        "Not checkable: the Sloan (1996) passage and the Beneish (1999) table (paper unreachable: UNVERIFIABLE by the brief's rule; the lessons say so). Scripts: ledgers/AC2/scripts/L07-L08-r4/. Scratch and logs: /tmp/ac2-v/L07-L08-r4/."
    ),
    "summary": {},
}
counts = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows),
          "fail": sum(r["status"] == "FAIL" for r in rows),
          "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows)}
frag["summary"] = counts
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(counts)
