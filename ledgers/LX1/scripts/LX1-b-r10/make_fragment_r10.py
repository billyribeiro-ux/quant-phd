"""Writes the round-10 LX1-b fragment (ledgers/LX1/LX1-b.json) from the rows verified in this round.

Usage: python3 -I make_fragment_r10.py <checkout>
"""
import json
import sys
from datetime import datetime, UTC
from pathlib import Path

root = Path(sys.argv[1])
O = "ledgers/LX1/scripts/LX1-b-r10/out/"
G = "ledgers/LX1/scripts/LX1-b-r10/"
PASS, FAIL = "PASS", "FAIL"
rows = []


def row(rid, check, location, status, evidence, fix=""):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != PASS:
        r["fix"] = fix
    rows.append(r)


row("lx1b-check-pages", "2.9 structure", "course/modules/LX/LX1/L03.html; course/modules/LX/LX1/L04.html", PASS,
    f"tools/check_pages.py --unit LX1 -> 'check_pages LX1: PASS', exit 0 ({O}check_pages.out), run on pin 00a84795.")
row("lx1b-check-dag", "2.9 DAG", "course/modules/LX/LX1/L03.html; course/modules/LX/LX1/L04.html", PASS,
    f"tools/check_dag.py --unit LX1 -> 'check_dag LX1: PASS', exit 0 ({O}check_dag.out). The pass depends on the L04 "
    "placeholder dfn; see row lx1b-L04-bretton-definition.")
row("lx1b-dag-links", "2.9 DAG links", "L03.html:37, :90 (L02 anchors); L04.html:37, :105 (exponential-and-logarithm, L03 lender link)", PASS,
    "L03.html meta-row links debt-deflation and gold-standard to L02.html#def-debt-deflation and L02.html#def-gold-standard "
    "(read at L03.html:37 and the Section 1 paragraph at :54); L04.html:37 links concepts.html#exponential-and-logarithm "
    "(M1 concept, in closure). check_dag PASS (out/check_dag.out).")
row("lx1b-dag-outside-closure", "2.9 DAG closure", "L03.html (whole page); L04.html:328", PASS,
    f"{G}prose_scan.sh -> {O}prose_scan.out: outside-closure names of plan section 4 occur on L04.html:328 ('covered interest', "
    "plain prose, no link, no data-concept, no parity formula) and zero hits on L03.html. Read in full this round.")
row("lx1b-run-labs", "2.5 labs", "tests/labs/LX1/lab-LX1-L03-1.py; tests/labs/LX1/lab-LX1-L04-1.py", PASS,
    f"tools/run_labs.py --unit LX1 -> 'run_labs LX1: PASS (7/7)', exit 0 ({O}run_labs.out).")
row("lx1b-twin-alone-L03", "2.5 labs", "tests/labs/LX1/lab-LX1-L03-1.py", PASS,
    f"{G}gates_r10.sh copies the twin alone to /tmp/lx1b-r10/L03 and runs .venv/bin/python (CPython 3.14.8) -I -W error: "
    f"{O}twin_L03.err is 0 bytes; {O}twin_L03.out has 56 lines. Twin reads no file (no open/csv in the source).")
row("lx1b-twin-alone-L04", "2.5 labs", "tests/labs/LX1/lab-LX1-L04-1.py", PASS,
    f"Run alone from /tmp/lx1b-r10/L04 with only data/fx_monthly.csv, .venv/bin/python -I -W error: {O}twin_L04.err 0 bytes; "
    f"{O}twin_L04.out has 17 lines, equal to the expected block.")
row("lx1b-twin-equals-page-code", "2.5 labs", "L03.html data-run block (:150-326) and expected block (:327-382); L04.html data-run block (:115-300) and expected block (:301-317)", PASS,
    f"{G}compare_pages_twins.py -> {O}compare_pages_twins.out: 'L03: page code == twin ... True; expected block == live twin "
    "output: True'; 'L04: ... True; ... True'; RESULT PASS.")
row("lx1b-page-smoke-L03", "2.9 / 2.5 page_smoke", "course/modules/LX/LX1/L03.html", PASS,
    f"tools/page_smoke.py --unit LX1 --pages L03 L04 -> 'page_smoke modules/LX/LX1/L03.html: PASS', exit 0 ({O}page_smoke_L03_L04.out).")
row("lx1b-page-smoke-L04", "2.9 / 2.5 page_smoke", "course/modules/LX/LX1/L04.html", PASS,
    f"Same run: 'page_smoke modules/LX/LX1/L04.html: PASS' and 'page_smoke LX1: PASS' ({O}page_smoke_L03_L04.out).")
row("lx1b-ruff-mypy", "2.5 gates", "tests/labs/LX1/lab-LX1-L03-1.py; tests/labs/LX1/lab-LX1-L04-1.py", PASS,
    f"ruff check tests/labs/LX1: 'All checks passed!' ({O}ruff_check.out); ruff format --check: '7 files already formatted' "
    f"({O}ruff_format.out); mypy --no-incremental on both twins: 'Success: no issues found in 2 source files' ({O}mypy_L03_L04.out).")
row("lx1b-pytest", "2.5 gates", "tests/test_labs.py; tests/test_page_checks.py (-k LX1)", PASS,
    f"pytest tests/test_labs.py tests/test_page_checks.py -q -k LX1 -> seven dots, exit 0 ({O}pytest_LX1.out).")
row("lx1b-verify-refs", "2.1 citations", "references/references.json; L03.html:405, :640; L04.html:565-570", PASS,
    f"tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' ({O}verify_refs_offline.out); "
    f"tools/verify_refs.py --unit LX1 -> 'live re-verification of LX1: 3 of 560 entries, 0 problems' ({O}verify_refs_unit_LX1.out).")
row("lx1b-citations-L03", "2.1 citations", "L03.html:405, :630, :640; references/references.json friedman1963monetary", PASS,
    "Only key cited: friedman1963monetary (L03.html section 10 and data-cite at :405). Registry title 'A monetary history of the "
    "United States 1867-1960', year 1963, type book; the page quotes the title and cites book level only; no passage is attributed. "
    "Registry lists Friedman only (flag N2). Credit-channel source (Bernanke 1983) is not cited by key: section 5 says the lesson cites no source for an empirical claim.")
row("lx1b-citations-L04", "2.1 citations / 2.8 data", "L04.html section 9 (:565-570)", PASS,
    "Section 9 cites no registry key and gives the dataset's citation string as its MANIFEST entry records it, which BUILDER_RULES "
    "section 6.6 (line 373, 'Cite the dataset's citation and MANIFEST's retrieval date') requires. Text matches "
    "course/assets/data/market/MANIFEST.json fx_monthly.citation and tools/data_sources.yaml.")
row("lx1b-fetch-check", "2.8 data", "course/assets/data/market/fx_monthly.csv; course/assets/data/market/MANIFEST.json", PASS,
    f"tools/fetch_data.py --check -> 'fetch_data: 3 datasets, 0 problems', exit 0 ({O}fetch_check.out).")
row("lx1b-fx-rebuild", "2.8 data / reproducibility", "course/assets/data/market/fx_monthly.csv; MANIFEST.json (fx_monthly sha256 60572240...)", PASS,
    "Live rebuild in a scratch copy (/tmp/lx1b-r10-fetch, copy of tools/ and course/assets/data/market/ only): "
    "tools/fetch_data.py --fetch --only fx_monthly -> 'built fx_monthly: 669 rows, 67392 bytes, 1971-01 to 2026-09' "
    f"({O}fetch_rebuild_fx_monthly.out). Rebuilt sha256 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e equals "
    "the checkout's MANIFEST sha256 and the checkout csv (shasum -a 256), byte for byte. raw_sha256 differs: rebuilt "
    "1c312d2fc1de99f174c26178a2cb1f0f0f6a4a08b6dce25b043603fec9a3f24a vs recorded 8f370f9c57b73e1c0b68a2ee72ddecd3abaffb21fa627fcfd4f8a3612798c6a8 "
    "(issuer's live file changed since retrieved 2026-10-19; provenance only, not compared, BUILDER_RULES 6.6). Checkout MANIFEST not edited.")
row("lx1b-fx-licence", "2.8 licence", "tools/data_sources.yaml fx_monthly (licence, licence_url); MANIFEST.json fx_monthly.licence; https://www.federalreserve.gov/disclaimer.htm", PASS,
    f"Plain curl of https://www.federalreserve.gov/disclaimer.htm -> HTTP 200 ({O}curl_fed_code.out), saved as {O}fed_disclaimer.html. "
    "The page contains 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and "
    "distributed without permission. Please cite to the Board as the source of the information.' This grants redistribution. "
    "The MANIFEST licence string is the same quote.")
row("lx1b-fx-guard", "2.5 labs (fail-loud input)", "tests/labs/LX1/lab-LX1-L04-1.py load_column, parse_rate, month_index", PASS,
    f"{G}guard_L04.py -> {O}guard_L04.out: blank GBP cell (1995-12) exit 1 ValueError; cell '1.5e2' exit 1; skipped month exit 1; "
    "missing GBP column exit 1; unchanged file exit 0.")
row("lx1b-fx-gbp-clean", "2.8 data", "course/assets/data/market/fx_monthly.csv (GBP column)", PASS,
    f"{G}indep_L04.py -> {O}indep_L04.out: 669 rows, 0 blank GBP cells, all rates positive; first 1971-01, last 2026-09.")
row("lx1b-honest-data", "2.8 honest data", "L03.html:76, :148-152; L04.html:7, :113-114, :568", PASS,
    "L03 is SIMULATED with an honest-pending note at :76 and reads no series (twin has no file access). L04 Part A is labelled "
    "SIMULATED; Parts B to D read only the embedded fx_monthly.csv (GBP). No fabricated rows.")
row("lx1b-L04-simulated-label", "2.5 / 2.8 SIMULATED", "L04.html:7, :113-114, :568; twin docstring lines 23-28; output line 1", PASS,
    f"Heading L04.html:111 'Part A SIMULATED'; hypothesis at :114 says 'labelled SIMULATED (a constructed model check, not data)'; "
    f"{O}twin_L04.out line 1 reads 'Part A: SIMULATED model check, not data: a parity held at 2.0000 dollars per pound'.")
row("lx1b-L04-manifest-note", "2.8 data", "tests/labs/LX1/lab-LX1-L04-1.py docstring lines 3-8, 117-129; L04.html:115-122", PASS,
    "Docstring states the file is the H.10 snapshot, retrieved 2026-10-19, 669 months, GBP as USD per pound (MANIFEST columns and "
    "transform: CAD, CHF, DKK, JPY, NOK, SEK inverted; GBP direct). Checked against MANIFEST.json fx_monthly.")
row("lx1b-open-items-missing", "2.9 / 2.6 open items", "plans/LX1-open-items.md", PASS,
    "plans/LX1-open-items.md lists D-1 (L03 data request), the Bretton Woods definition and the architect question, and N1/N2 "
    "reference requests (read in full, 2237 bytes).")
row("lx1b-num-L03-depth", "2.2 numbers", "L03.html:149, :383, :487-491, :545-546, :574-577, :593-596, :610", PASS,
    f"Re-derived with {G}indep_L03.py -> {O}indep_L03.out: depth X exact 0.0920460 -> 9.20; depth Y exact 0.0268671 -> 2.69 "
    "(exact 2.6867 in E1 correct); difference exact 6.517884 -> 6.52 (unrounded), shown values give 6.51 (interpretation line 383 "
    "states both). Ratio 3.425970 -> 3.4260. Quiz numbers agree.")
row("lx1b-num-L03-path", "2.2 numbers", "L03.html expected block (:327-382); M1 (:437-443); M2 (:444-450); M3 (:451-458); E1 (:487-493); quiz 1274345", PASS,
    f"V_12 = 1274345.2124 cents -> 1274345 (indep_L03.out). Expected block (:327-382) equals live output (compare_pages_twins PASS). "
    "Path values: X index 0.7847, Y index 0.9224 from (49/50)^4 = 5764801/6250000 exact (M1). V_4 = 1084165.7847 -> 1084166; "
    "N_4 = 3915834.2153 -> 3915834; L_4 = 0.2768671 -> 0.2769 (M3). Rounding V_4 and N_4 first gives 1084166, 3915834 and 0.2769, as M2 and M3 state. "
    "E3 count of unchanged indices for Y in t=5..12 is 8.")
row("lx1b-num-L04-stats", "2.2 numbers", "L04.html expected block (:301-317), :321, :469-472, quiz (:479-560)", PASS,
    f"{G}indep_L04.py -> {O}indep_L04.out: window one sd 0.027935278 -> 0.027935; window two sd 0.024699501 -> 0.024700 "
    "(321 changes, first change 2000-01); max |change| w1 0.13584567 at 1985-03 -> 0.135846; w2 -0.09657474 at 2008-10 -> -0.096575; "
    "zero changes 1976-07, 2012-07, 2019-11 (count 3, nonzero 665); telescoping error 5.6e-16 and 7.8e-16 (<1e-12). All match the expected block.")
row("lx1b-num-L04-display-diff", "2.2 numbers (display vs unrounded)", "L04.html:318, :343-345, expected line 316", PASS,
    "Diff of unrounded sds = -0.003235777 -> -0.003236 (printed). Subtracting the rounded figures 0.024700 - 0.027935 = -0.003235; "
    "the interpretation (line 318) says the printed-figure subtraction gives -0.003235, which is correct. Ratio 0.884168808 -> 0.8842.")
row("lx1b-num-L04-derived", "2.2 numbers (derived on page)", "L04.html:368, :375, :400, :425, :450, :536, :559", PASS,
    "M1 ln 1.1 = 0.0953101798 -> 0.095310; 0.1 - ln 1.1 = 0.0046898 -> 0.004690. M2 mean 1/150 = 0.006667; sum of squared dev "
    "0.0012667 = 19/15000; sd = sqrt(19/30000) = 0.025166115 -> 0.025166. E2 exp(-0.0965747)-1 = -0.092057965 -> -0.092058. "
    "R2 tanh(0.13584567/2) = 0.06781857 -> 0.067819; bound at h=0.0678 = ln(1.0678/0.9322) = 0.13580835 -> 0.135808 (does not reach 0.135846). "
    "Quiz 0.1358 consistent. All recomputed by python3 -I one-liners this round.")
row("lx1b-scope-start", "2.4 scope words", "L04.html:330 (window start bullet; line 321 in the current file); card LX1-c063", PASS,
    "'The start of window two is the first month from which the other two embedded snapshots ... have data, since both begin on "
    "2000-01-03' matches MANIFEST first dates (fx_daily and ust_daily both 2000-01-03). The 'convention' claim is stated as a convention, not a finding.")
row("lx1b-math-L03", "2.4 mathematics", "L03.html:94-143, :393-396, :67, :121, :145", PASS,
    "Lemma 3.1: y(C-x)-x(C-y) = C(y-x) re-derived. Prop 3.2(a)-(c) re-derived; (c) at m=0 gives depth 0. Corollary 3.3 (V_{m'} < V_m, V_m < C) and "
    "Corollary 3.4 (common factor beta*phi cancels) re-derived. Assumption 1.2 inequality keeps N_t>0 (N_t = C - V_t). Notation checked.")
row("lx1b-math-L04", "2.4 mathematics", "L04.html:58-107 (Def 1.1, Prop 1.2, Remark 1.3, Def 2.1, Prop 2.2, Remark 2.3); :389-413 (P1-P3)", PASS,
    "Telescoping induction and cancellation proof re-derived. Prop 2.2 hypotheses state n>=2 and x_t=kappa at the month before the window's first change and at each later month (the changed text at :92), which the proof uses. "
    "P2 band bound (ln((1+h)/(1-h)) form) and P3 (ln(1+u) <= u with derivative sign) re-derived.")
row("lx1b-math-problems", "2.4 mathematics / 2.9 problems", "L03.html:437-531 (M1-M3, P1-P3, E1-E3, R1-R3); L04.html:364-459", PASS,
    "Every worked solution re-derived this round (see lx1b-num-* rows). L03 R1 solution (:516) changed this round: it states no new result and follows from Remark 4.2 and Assumption 1.3. "
    "L03 R2 (:523) proof re-derived (G strictly increasing, Prop 3.2(a)). L04 R3 solution (:457) changed this round: calls the 2000-01 choice a convention; no number is stated.")
row("lx1b-grades", "2.3 grades", "L03.html:542-546, :82-89, :405; L04.html:469-472, :105", PASS,
    "Key results: T for Prop 3.2, Cor 3.3, Cor 3.4 (proved); C for lab readings (SIMULATED Part B/D values); L04 C for lab-read dispersions and zero-change months. Proof-backed results are T; lab outputs are C and name the lab.")
row("lx1b-notation", "2.4 notation", "L03.html (278 math segments); L04.html (150 math segments)", PASS,
    f"{O}prose_scan.out: registered symbols T, Phi, gamma, R_f, R^*, Q absent (0 hits) in both pages. Local symbols D, N, V, L, C, G, ell, psi, f, H, m, delta, phi, beta, kappa, x, h are each defined before use. notation/notation.json has 8 symbols and no clash.")
row("lx1b-concepts-defs", "2.9 DAG / definitions", "L03.html:82, :87, :390; L04.html:59, :85, :86", PASS,
    "Each concept's dfn appears once: L03 def-leverage, def-external-finance-premium, def-credit-channel-depression, def-central-bank (plain), def-lender-of-last-resort; L04 Bretton Woods dfn with pending text (see lx1b-L04-bretton-definition). check_dag: no duplicate definitions.")
row("lx1b-banned-phrases", "2.9 prose", "L03.html; L04.html", PASS,
    f"{O}prose_scan.out: zero hits for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly. Ellipses at L03.html:162 are inside the data-run block (:150-326) and the docstring at :254.")
row("lx1b-process-words", "2.9 prose (process words)", "L03.html; L04.html", PASS,
    "grep of learner text for builder, verifier, round, ledger, planner, DATA_REQUEST, REFERENCE_REQUEST, TODO, TBD returns none. The word pending appears in L03.html:76 (the honest-pending note label, a declared data status) and in the Bretton Woods status at L04.html:38 and :86 (see lx1b-L04-bretton-definition).")
row("lx1b-structure", "2.9 structure", "L03.html sections 1-10; L04.html sections 1-9", PASS,
    "BUILDER_RULES 4.2 order checked: why-it-matters (L03 119 words, L04 116 words, both at most 120); core sections 1-3 with labs; canon breaks; misconceptions (4 each); problem set (Mechanics, Proof, Empirical, Research, 3 each); key results; quiz (11 items each, with explanations); references. No debate key on LX1, so no debate brief. check_pages PASS.")
row("lx1b-quiz-explanations", "2.9 quiz", "L03.html quiz (:553-636); L04.html quiz (:479-560)", PASS,
    "L03: 11 items, 11 explanations, 6 correct options marked data-correct, and each numeric answer matches the printed or exact value (2.69 tol 0.005; 12; 3.426 tol 0.0005; 1274345 tol 0.5; 8). L04: 11 items, 11 explanations; numeric answers 3, 321, 0.027935, 0.095310, 0.1358 match.")
row("lx1b-L03-remark42-solvency", "2.4 / 2.9", "L03.html:67 (Assumption 1.2); :394-395 (Remark 4.2)", PASS,
    "Assumption 1.2 V_m < N_0 + D; Prop 3.2(a) V_t <= V_m; so V_t < N_0 + D and N_t > 0 each period (C = N_0 + D, N_t = C - V_t). Re-derived.")
row("lx1b-L03-ratio-claims", "2.3 / 2.4 claims", "L03.html:404 (functional-form bullet); :523 (R2); :117-121 (Prop 3.2 proof)", PASS,
    "Functional-form bullet: premium = phi*(L_t-L_0)^2 gives depth = beta*phi*(bracket)^2, so the ratio is the square of the Corollary 3.4 ratio; differs unless the ratio is 1. Re-derived. Slope change leaves the ratio unchanged (phi cancels). Correct.")
row("lx1b-L03-r1-no-result", "2.9 no unproved result", "L03.html:516 (R1 solution, changed this round)", PASS,
    "R1 solution now says a facility would act on a solvent borrower's premium, needs an insolvent-borrower case excluded by Assumption 1.2, and needs an Assumption 1.3 term. It states no number and no new result. Consistent with Remark 4.2.")
row("lx1b-L04-bretton-definition", "2.9 DAG / concept definition / plan decision", "L04.html:38, :86; plans/LX1-build-plan.md section 12 item 9 and Architect decisions; plans/LX1-open-items.md; tools/check_dag.py:75", FAIL,
    "Unchanged in substance since round 9 and re-verified this round. L04.html:86 is '<dfn id=\"def-bretton-woods-system\" data-concept=\"bretton-woods-system\">Bretton Woods system</dfn>: <em>definition pending.</em>', and :38 introduces it as 'definition pending'. "
    "Plan section 12 item 9 (RECOMMENDED, which the binding Architect decisions adopt) says the L04 page 'states only the lab's facts and the first MANIFEST month' until B3 is resolved. "
    "tools/check_dag.py:75 requires every introduced concept to have a dfn, so the placeholder is what makes check_dag pass. plans/LX1-open-items.md asks the architect to confirm this reading. "
    "No ruling exists: git diff c93dd526..HEAD shows no change to plans/LX1-*.md or plans/FINAL-ARCHITECT-RULINGS.md. The verifier cannot decide this.",
    "Architect ruling required, then either: (a) record in plans/LX1-build-plan.md 'Architect decisions' an approved exemption for the pending placeholder, and make tools/check_dag.py honour it, so this row can pass; or (b) remove the dfn at L04.html:86, the placeholder text at :38 and :86, and the bretton-woods-system data-concept uses, and drop bretton-woods-system from LX1's introduces list (a curriculum change). Re-verify after either.")
row("lx1b-L04-prediction-tested", "2.5 labs (hypothesis)", "L04.html:114 (hypothesis); lab-LX1-L04-1.py Parts A and C", PASS,
    "The hypothesis predicts nonzero GBP dispersion in both windows and says the lab does not assert it. Part C prints 0.027935 and 0.024700, both nonzero; the lab asserts no such test. Part A is the zero-dispersion model check, as Proposition 2.2 states.")
row("lx1b-L03-lab-checks-overreach", "2.5 labs (claims vs code)", "L03.html:145, :383; twin Parts B-D", PASS,
    "Section text says Part B prints whether X is deeper, Part C checks adjacent ordering, Part D prints the ratio and makes no equality test. Twin code matches (print_economy, depth, never_falls/strict_steps, Part D loop with no assert). Interpretation (:383) accurately says Part C checks adjacent pairs.")
row("lx1b-L03-misconception-scope", "2.9 claims", "L03.html:418 (misconception 2); proof L03.html:130", PASS,
    "Misconception 2: the ordering follows from the parity durations (Cor 3.3 proof uses V_m, closed form, V_m<N_0+D, Lemma 3.1, Prop 3.2(b)); the model cannot say whether parity causes a deeper fall. Matches the proof text.")
row("lx1b-L04-A2-before-defined", "2.9 terms before definition", "L04.html:85 (Definition 2.1), :92-99, :398, :446", PASS,
    "Assumption (A2) is named and defined in Definition 2.1 before Proposition 2.2 uses it. The later month-range wording (:84) matches Proposition 2.2's hypothesis (:92). No term used before its definition except where explicitly forward-referenced.")
row("lx1b-L04-keyresults-locator", "2.3 key results", "L04.html:469-472 (key results rows 3 and 4)", PASS,
    "Row 3 cites Lab 1 Parts C and D with values 0.027935, 0.024700, 0.8842 (verified in lx1b-num-L04-stats); row 4 cites Part B for three zero months (verified).")
row("lx1b-cards-l03-l04", "2.7 cards", "course/modules/LX/LX1/cards.json (48 L03/L04 cards: 28 L03, 20 L04)", PASS,
    "All 48 L03/L04 cards read this round and checked against the current lesson text. No duplicate ids or fronts in the 78-card file. Removed this round: LX1-c069 and LX1-c075 (L04; both restate facts also in Section 3 and Lab 1 Part B). Added: LX1-c080 (L03, central bank 'issues the currency', matches L03.html:389-390). Card numbers 9.20, 2.69, 3.4260, 1274345, 0.027935, 0.024700, 0.8842, -0.096575, 665/668 all appear in their lesson. Card-only prose claims re-derived. Central bank card now present (round 9 gap closed).")
row("lx1b-delta-hunks", "delta reading (round 9 pin c93dd526 to 00a84795)", "L03.html :51 (why-it-matters), :320 (Part D print in the code block, twin line 171), :379 and :387 (expected block), :390 (central bank dfn), :516 (R1 solution); L04.html :51 (why-it-matters), :82-92 (Def 2.1, Prop 2.2), :114 (lab hypothesis), :456 (R3 solution); cards.json L03/L04 entries LX1-c069 and LX1-c075 (removed), LX1-c080 (added)", PASS,
    "git diff c93dd526 00a84795 for each slice file, read hunk by hunk; every changed line re-read and re-verified (rows above). The lab twin for L04 is unchanged in this delta (git diff lists only the L03 twin, Part D print at line 171). The L04 twin docstring defect (lx1b-L04-twin-docstring-float, twin line 111) is in an unchanged line, found this round. Cards outside L03/L04 (L01/L02 entries, e.g. c008, c022, c024, c081) belong to slice a and were not verified here.")
row("lx1b-L03-partD-label", "2.5 labs (printed text vs code)", "tests/labs/LX1/lab-LX1-L03-1.py:171; course/modules/LX/LX1/L03.html:383 and expected block (:327-382)", PASS,
    f"The Part D print text changed in this round to 'for three values of the product beta * phi'. Code (:172-174) loops over three (phi, beta) pairs with product 1/2, 1, 3, matching the label. Expected block shows the same label (compare_pages_twins PASS).")
row("lx1b-L03-line121-lab-formula", "2.4 / 2.5 (lab does not evaluate part (b))", "L03.html:121 (Prop 3.2 paragraph); :145; tests/labs/LX1/lab-LX1-L03-1.py depth()", PASS,
    "Section text says the lab does not evaluate Prop 3.2(b) itself. Twin depth() takes the max over depth_path (:109-111), with no closed form. Claim holds.")
row("lx1b-L03-why-ordering", "2.9 claims", "L03.html:51 (why-it-matters)", PASS,
    "States that the ordering follows from Assumptions 1.1 to 1.3 (Corollary 3.3) and is not evidence about any economy. Consistent with proof and the honest-pending note.")
row("lx1b-L04-spot-only", "2.8 data register", "L04.html:328 ('Exchange rates only'); tools/data_sources.yaml fx_monthly note", PASS,
    "data_sources.yaml fx_monthly note: 'Spot rates only, as for fx_daily.' Page says the series is spot-only. Quoted correctly. No forward column in MANIFEST columns (AUD..SEK).")
row("lx1b-L03-honest-pending-source", "2.8 honest data", "L03.html:76 (honest-pending note)", PASS,
    "Note states the curriculum names data but no redistributable series for gold-standard adherence or output depth is embedded; MANIFEST ids are fx_daily, fx_monthly, ust_daily only (read this round). The lab stays SIMULATED.")
row("lx1b-L04-twin-docstring-float", "2.5 labs (docstring vs code)", "tests/labs/LX1/lab-LX1-L04-1.py:111 and :113; course/modules/LX/LX1/L04.html:225 and :227 (same text, embedded)", FAIL,
    "Docstring of log_changes says 'The ratio is an exact Fraction; only the logarithm is a float.' The code at :113 is math.log(float(rate / previous)): the exact Fraction ratio is converted to a float BEFORE the logarithm. The sentence is false about the code, and it appears in the learner-visible code block (L04.html:225). Found this round; the line is unchanged from the pin of round 9.",
    "Change twin line 111 to: 'The ratio is an exact Fraction, converted once to a float before the logarithm. Each change is dated by the later month.' Then run tools/embed_labs.py course/modules/LX/LX1/L04.html --refresh lab-LX1-L04-1 so that the page code equals the twin (compare_pages_twins must print True). The expected block does not change (output unchanged). Re-run run_labs, ruff, mypy, and the twin-alone run.")

verdict = PASS if all(r["status"] == PASS for r in rows) else FAIL
frag = {
    "unit": "LX1",
    "slice": "LX1-b",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-b (L03, L04 and lab twins), round 10; did not build LX1 or LX1-b",
    "pin": "00a84795",
    "base": "c93dd526 (round-9 pin); delta read hunk by hunk for L03.html, L04.html, cards.json L03/L04 entries, both twins",
    "checkout": str(root),
    "scratch": "/tmp/lx1b-r10 (gates_r10.sh twin runs, guard copies); /tmp/lx1b-r10-fetch (live fx_monthly rebuild, scratch only)",
    "verified_at": datetime.now(UTC).isoformat(timespec="seconds"),
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "friedman1963monetary: registry record lists Friedman only (book, Princeton 1963); curriculum string 'Friedman & Schwartz (1963)' (curriculum/06-profession-capstone.yaml:37). Pages cite the key and the title only. Architect may correct via tools/add_reference.py (plan N2).",
        "Bernanke (1983), AER 73(3) (curriculum/06-profession-capstone.yaml:38): no registry record (plan B2, REFERENCE_REQUEST 2). L03 makes no empirical attribution to it.",
        "Bretton Woods (plan B3, REFERENCE_REQUEST 3): no registry source. L04 defines nothing historical; the placeholder dfn is the open question (row lx1b-L04-bretton-definition).",
    ],
    "freshness_flags": [],
    "notes": [
        "LX1 is rubric-only (no autograder): run_graders.py prints 'no autograder (grading: rubric)' (out/run_graders.out, exit 0). No grader mutants apply; the lab twins are demonstrations. mutants is empty by design.",
        "Not checked: a fresh Crossref re-resolution beyond verify_refs --unit LX1 (3 entries, live, 0 problems); L01, L02, project.html, index.html and cards outside L03/L04 belong to other slices; a Pyodide run (page_smoke ran the lab in its own harness, exit 0).",
        "Twins run under CPython 3.14.8 (.venv) only in this round; the round-9 run under python3 3.15.0 was not repeated (gate script uses the venv interpreter).",
        "Scripts: ledgers/LX1/scripts/LX1-b-r10/ (gates_r10.sh, compare_pages_twins.py, guard_L04.py, prose_scan.sh, cards_dump.py, indep_L03.py, indep_L04.py, make_fragment_r10.py, out/).",
    ],
    "summary": "",
}
n_fail = sum(1 for r in rows if r["status"] == FAIL)
frag["summary"] = (f"LX1-b round 10 on 00a84795 (delta from c93dd526): verdict {verdict}. {len(rows)} rows: "
                   f"pass={len(rows)-n_fail} fail={n_fail} unverifiable=0. Non-PASS: lx1b-L04-bretton-definition (architect ruling "
                   "outstanding, unchanged), lx1b-L04-twin-docstring-float (new: false docstring sentence in the learner-visible lab code).")
out = root / "ledgers/LX1/LX1-b.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "verdict", verdict)
