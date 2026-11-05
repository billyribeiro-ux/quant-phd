"""LX1-b round 11: write the fragment ledgers/LX1/LX1-b.json (rows carry the evidence cited in the final report).

Usage: python -I ledgers/LX1/scripts/LX1-b-r11/make_fragment_r11.py <checkout>
Every row was re-checked this round on pin 11d7077; none is carried from round 10.
"""

import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
O = "ledgers/LX1/scripts/LX1-b-r11/out"
SC = "ledgers/LX1/scripts/LX1-b-r11"
P = "PASS"
F = "FAIL"

rows = []


def row(rid, check, location, status, evidence, fix=""):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


GATE = f"{O}/check_pages.out, {O}/check_dag.out"
row("lx1b-check-pages", "2.9 structure", "course/modules/LX/LX1/L03.html; course/modules/LX/LX1/L04.html", P,
    f"tools/check_pages.py --unit LX1 -> 'check_pages LX1: PASS', exit 0 ({O}/check_pages.out).")
row("lx1b-check-dag", "2.9 DAG", "course/modules/LX/LX1/L03.html; course/modules/LX/LX1/L04.html", P,
    f"tools/check_dag.py --unit LX1 -> 'check_dag LX1: PASS', exit 0 ({O}/check_dag.out).")
row("lx1b-dag-links", "2.9 DAG links", "L03.html:37, :54, :90 (L02 anchors); L04.html:37, :105 (exponential-and-logarithm, L03 lender link), :332", P,
    "Link targets exist: id=\"def-debt-deflation\" and id=\"def-gold-standard\" in course/modules/LX/LX1/L02.html; "
    "id=\"exponential-and-logarithm\" in course/concepts.html; id=\"def-lender-of-last-resort\" at L03.html:390. "
    f"Checked by grep this round; check_dag PASS ({O}/check_dag.out).")
row("lx1b-dag-outside-closure", "2.9 DAG closure", "L03.html (whole page); L04.html:329", P,
    "Named out-of-closure concepts from plans/LX1-build-plan.md section 4 (D1-D15: bank run, fire sale, covered/uncovered "
    "interest parity, moral hazard, Fisher relation, bank reserves, contagion, sovereign default, FX market structure, "
    "etc.) grep to zero hits in both pages this round; the 'covered interest parity' mention of the round-10 pin is gone "
    "(L04.html:329 now names no parity). Linked concepts all in closure or introduced here (check_dag PASS).")
row("lx1b-run-labs", "2.5 labs", "tests/labs/LX1/lab-LX1-L03-1.py; tests/labs/LX1/lab-LX1-L04-1.py", P,
    f"tools/run_labs.py --unit LX1 -> 'run_labs LX1: PASS (7/7)', exit 0 ({O}/run_labs.out).")
row("lx1b-twin-alone-L03", "2.5 labs", "tests/labs/LX1/lab-LX1-L03-1.py", P,
    f"Alone in scratch dir, 'python -I -W error': exit 0, empty stderr ({O}/twin_L03.err, {O}/twin_L03.out).")
row("lx1b-twin-alone-L04", "2.5 labs", "tests/labs/LX1/lab-LX1-L04-1.py", P,
    f"Alone in scratch dir with data/fx_monthly.csv only, 'python -I -W error': exit 0, empty stderr ({O}/twin_L04.err, {O}/twin_L04.out).")
row("lx1b-twin-equals-page-code", "2.5 labs", "L03.html data-run block (:150-326) and expected block (:327-382); "
    "L04.html data-run block (:115-300) and expected block (:302-317)", P,
    f"{SC}/compare_r11.py: page data-run code equals twin source for L03 and L04; expected blocks equal twin stdout line for "
    f"line (56 and 17 lines). Output {O}/compare_r11.out, 'ALL EQUAL'.")
row("lx1b-page-smoke-L03", "2.9 / 2.5 page_smoke", "course/modules/LX/LX1/L03.html", P,
    f"tools/page_smoke.py --unit LX1 --pages L03 -> 'page_smoke modules/LX/LX1/L03.html: PASS', exit 0 ({O}/page_smoke_L03.out).")
row("lx1b-page-smoke-L04", "2.9 / 2.5 page_smoke", "course/modules/LX/LX1/L04.html", P,
    f"tools/page_smoke.py --unit LX1 --pages L04 -> 'page_smoke modules/LX/LX1/L04.html: PASS', exit 0 ({O}/page_smoke_L04.out).")
row("lx1b-ruff-mypy", "2.5 gates", "tests/labs/LX1/lab-LX1-L03-1.py; tests/labs/LX1/lab-LX1-L04-1.py", P,
    f"ruff check: 'All checks passed!' ({O}/ruff_check.out); ruff format --check: '7 files already formatted' ({O}/ruff_format.out); "
    f"mypy --no-incremental on both twins: 'Success: no issues found in 2 source files' ({O}/mypy_L03_L04.out).")
row("lx1b-pytest", "2.5 gates", "tests/test_labs.py; tests/test_page_checks.py (-k LX1)", P,
    f"pytest -q -k LX1: 7 passed, exit 0 ({O}/pytest_LX1.out); collect-only count 7 ({O}/pytest_collect_LX1.out).")
row("lx1b-verify-refs", "2.1 citations", "references/references.json; L03.html:405, :640", P,
    f"tools/verify_refs.py --offline: '560 entries, 0 problems' ({O}/verify_refs_offline.out); --unit LX1 live: "
    f"'4 of 560 entries, 0 problems' ({O}/verify_refs_unit_LX1.out). Registry record friedman1963monetary read in full "
    "(title, Friedman, 1963, book, Open Library URL); used_by includes LX1.")
row("lx1b-citations-L03", "2.1 citations", "L03.html:405, :640 (data-cite friedman1963monetary, the only cite)", P,
    "The one data-cite key exists in references/references.json. Title quoted at L03.html:640 matches the record title exactly. "
    "The page takes no finding from the book and attributes no account to it (L03.html:405, :640).")
row("lx1b-citations-L04", "2.1 citations / 2.8 data", "L04.html section 9 (:565-570)", P,
    "L04 cites no registry key; the only reference is the MANIFEST citation of the fx_monthly dataset, whose title, "
    "issuer, retrieval date (2026-10-19) and MANIFEST entry match course/assets/data/market/MANIFEST.json (fx_monthly).")
row("lx1b-fetch-check", "2.8 data", "course/assets/data/market/fx_monthly.csv; course/assets/data/market/MANIFEST.json", P,
    f"tools/fetch_data.py --check: 'fetch_data: 3 datasets, 0 problems', exit 0 ({O}/fetch_check.out).")
row("lx1b-fx-rebuild", "2.8 data / reproducibility", "course/assets/data/market/fx_monthly.csv; MANIFEST.json (fx_monthly sha256 60572240...)", P,
    f"{SC}/fx_rebuild_r11.sh: tools/fetch_data.py --fetch --only fx_monthly in a scratch copy (git archive 11d7077) rebuilt "
    "669 rows, 67392 bytes, 1971-01 to 2026-09; the rebuilt CSV is byte-identical (cmp; sha256 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e, "
    f"equal to MANIFEST). The rebuilt MANIFEST differs only in retrieved (2026-10-19 -> 2026-11-05) and raw_sha256 "
    f"(8f370f9c... -> 1c312d2f...), the provenance fields BUILDER_RULES 6.6 says are not expected to reproduce. "
    f"Record: {O}/fetch_rebuild_fx_monthly_r11.out. The checkout MANIFEST was not edited.")
row("lx1b-fx-licence", "2.8 licence", "tools/data_sources.yaml fx_monthly (licence, licence_url); MANIFEST.json fx_monthly.licence; "
    "https://www.federalreserve.gov/disclaimer.htm", P,
    f"{SC}/licence_r11.sh: plain curl of https://www.federalreserve.gov/disclaimer.htm returned HTTP 200 ({O}/curl_fed_disclaimer_code.out); "
    f"the page contains the quoted grant 'Unless otherwise indicated, information on Board's website is in the public domain and "
    f"may be copied and distributed without permission. Please cite to the Board as the source of the information.' "
    f"({O}/fed_licence_quote.out). The grant covers redistribution.")
row("lx1b-fx-guard", "2.5 labs (fail-loud input)", "tests/labs/LX1/lab-LX1-L04-1.py load_column, parse_rate, month_index", P,
    f"{SC}/guard_r11.py executes the twin's functions on nine scratch CSVs: blank cell, 'NA', a month gap, a missing GBP column, "
    f"a zero rate, a signed value, an exponent, month 13 each raise ValueError with a message; the good file loads 2 rows ({O}/guard_r11.out).")
row("lx1b-fx-gbp-clean", "2.8 data", "course/assets/data/market/fx_monthly.csv (GBP column)", P,
    f"{SC}/rederive_r11.py: 669 rows, 0 blank GBP cells, months consecutive ({O}/rederive_r11.out).")
row("lx1b-honest-data", "2.8 honest data", "L03.html:76, :148-152; L04.html:7 (meta), :113-114, :568", P,
    "L03 is SIMULATED with an honest-pending note stating no redistributable series is embedded (L03.html:76); L04 Parts B-D read "
    "the embedded GBP column and Part A is labelled SIMULATED (L04.html:114). No fabricated rows.")
row("lx1b-L04-simulated-label", "2.5 / 2.8 SIMULATED", "L04.html:113-114; twin docstring lines 1-30; output line 1", P,
    "The Part A heading and hypothesis carry SIMULATED; the twin prints 'Part A: SIMULATED model check, not data' (twin_L04.out line 1).")
row("lx1b-L04-manifest-note", "2.8 data", "tests/labs/LX1/lab-LX1-L04-1.py docstring; L04.html:115-122", P,
    "Docstring states 669 months 1971-01 to 2026-09, retrieval 2026-10-19, GBP is a direct quote (not in the inverted list "
    "CAD, CHF, DKK, JPY, NOK, SEK of MANIFEST and tools/data_sources.yaml), and no interest-rate or forward column; all verified against MANIFEST and the CSV header.")
row("lx1b-open-items-missing", "2.9 / 2.6 open items", "plans/LX1-open-items.md", P,
    "File present; it lists D-1 (L03 data request), the Bretton Woods pending definition, and the reference requests (read in full).")
row("lx1b-num-L03-depth", "2.2 numbers", "L03.html:149, :383, :487-493 (E1), :545-546 (key results), :553-636 (quiz)", P,
    f"{SC}/rederive_r11.py: depth(12) = 0.0920459718 = 9.2046 %, depth(4) = 0.0268671310 = 2.6867 %; both printed values round "
    f"half up to 9.20 and 2.69 (rederive_r11.out). Ratio 3.425969... prints 3.4260. Unrounded X-Y = 6.517884 (prints 6.52), "
    "printed difference 9.20-2.69 = 6.51 (L03.html:383 states both).")
row("lx1b-num-L03-path", "2.2 numbers", "L03.html expected block (:327-382); M1 (:437-443); M2 (:444-450); M3 (:451-458); E1 (:487-493); quiz (:553-636)", P,
    "Every expected-block value equals the twin's stdout (compare_r11.out). Re-derived: V_4 = 1084165.7847 (prints 1084166), "
    "V_12 = 1274345.2124 (prints 1274345, quiz tolerance 0.5), P_4 = 5764801/6250000 = 0.92236816, N_4 = 3915834.2153 (3915834), "
    "L_4 = 0.2768671 (0.2769), index X t=12 = 0.7847, Y index flat for t=5..12 (8 periods). Quiz 2.69 and 12 match.")
row("lx1b-num-L04-stats", "2.2 numbers", "L04.html expected block (:302-317), interpretation (:319), key results (:470-473), quiz (:479-560)", P,
    "Re-derived with own code (rederive_r11.out): window one n=668, sd 0.027935277917..., window two n=321 sd 0.024699501387..., "
    "zero months 1976-07, 2012-07, 2019-11, largest 0.13584567 at 1985-03, largest window two -0.09657474 at 2008-10, telescoping "
    "residuals < 1e-15. All match the printed lines and the key results rows.")
row("lx1b-num-L04-display-diff", "2.2 numbers (display vs unrounded)", "L04.html:319 (interpretation); misconceptions section (:337-357); quiz (:520-523)", P,
    "Unrounded difference -0.0032357765 prints -0.003236; the two printed sds subtract to -0.003235, as the page says (L04.html:319). "
    "Ratio 0.88416880... prints 0.8842.")
row("lx1b-num-L04-derived", "2.2 numbers (derived on page)", "L04.html:365-371 (M1), :372-378 (M2), :397-403 (P2), :422-428 (E2), :447-453 (R2), :535-537 and :557-560 (quiz)", P,
    "M1: ln 1.1 = 0.0953101798, difference 0.1 - ln 1.1 = 0.0046898 (prints 0.004690). M2: mean 1/150, sum of squared deviations 19/15000, "
    "dispersion sqrt(19/30000) = 0.025166. E2: exp(-0.0965747...) - 1 = -0.09205796 (prints -0.092058). R2: tanh(0.0679228) = 0.06781874 "
    "(prints 0.067819); bound at h = 0.0678 is 0.13580835 (prints 0.135808), below 0.135846. Quiz ln 1.1 and 0.1358 agree.")
row("lx1b-scope-start", "2.4 scope words", "L04.html:331 (window start bullet); card LX1-c063", P,
    "Window two start is described as a convention and the lab computes no other start (L04.html:331; Part C prints one window two). "
    "Consistent with the code (WINDOW_TWO_FROM constant, single start).")
row("lx1b-math-L03", "2.4 mathematics", "L03.html:94-107 (Lemma 3.1, Prop 3.2), :124-142 (Cor 3.3, 3.4), :67, :121, :145", P,
    "Re-derived each proof: Lemma 3.1 difference identity C(y-x)/((C-x)(C-y)) and the N_t = C - V_t identity; Prop 3.2(a) monotone V_t; "
    "(b) closed form equals the depth numerically (0.0920459718 and 0.0268671310, closed form vs max over path); (c) first maximiser t = m. "
    "Cor 3.3 needs V_m < C (Assumption 1.2), supplied. Cor 3.4 cancels beta*phi. Assumption 1.2 inequality V_12 = 1274345 < 5000000 holds.")
row("lx1b-math-L04", "2.4 mathematics", "L04.html:58-107 (Def 1.1, Prop 1.2, Remark 1.3, Def 2.1, Prop 2.2, Remark 2.3)", P,
    "Prop 1.2 telescoping proof and induction (P1) re-derived; Prop 2.2 (a),(b) follow from (A2) with n >= 2; the dispersion formula "
    "uses denominator n-1 matching the lab (sample_sd); the (A2) wording at L04.html:84-92 matches Prop 2.2's hypotheses.")
row("lx1b-math-problems", "2.4 mathematics / 2.9 problems", "L03.html:431-530 (M1-M3, P1-P3, E1-E3, R1-R3); L04.html:359-459 (M1-M3, P1-P3, E1-E3, R1-R3)", P,
    "Every worked solution re-derived: L03 M1-M3 numbers, P1-P3 proofs (P3 expansion checked), E1-E3 (E2 subtraction 9.204597-2.686713=6.517884), "
    "R1-R3 reasoning; L04 P2 bound (both inequalities), P3 (f' sign), R2 closed form and monotonicity, E3 reading of the code.")
row("lx1b-grades", "2.3 grades", "L03.html:124, :134, :543-546 (key results); L04.html:470-473, :105", P,
    "Grades: Cor 3.3, Cor 3.4, Prop 3.2 are T and are proved on the page; the Lab 1 read-offs (9.20, 2.69, 3.4260) are C and name Lab 1 "
    "(L03.html:545-546); the L04 dispersion results are C naming Lab 1 (L04.html:472-473). No lab result is graded T.")
row("lx1b-notation", "2.4 notation", "L03.html (278 math segments); L04.html (150 math segments)", P,
    f"{O}/prose_scan_r11.out: no registered notation macro or symbol (notation/notation.json, 34 entries) is used by either page; "
    "every local symbol (D, N, V, L, C, G, H, m, delta, psi, varphi, beta, ell, f, x, y, s, n, h, kappa, A1-A3) is defined in its lesson before use or at its first use.")
row("lx1b-concepts-defs", "2.9 DAG / definitions", "L03.html:82, :87, :390; L04.html:59, :85, :86", P,
    "check_dag: credit-channel-depression and lender-of-last-resort defined once in L03 (L03.html:87, :390); bretton-woods-system defined once "
    "(L04.html:86) as a pending placeholder, which is the open FAIL row lx1b-L04-bretton-definition.")
row("lx1b-banned-phrases", "2.9 prose", "L03.html; L04.html", P,
    f"{O}/prose_scan_r11.out: fixed-string scan of every BUILDER_RULES 1.3-1.4 phrase (TODO, TBD, lorem, for brevity, details omitted, "
    "beyond the scope, left as an exercise, you can add more, studies show, experts agree, well known, obviously, clearly, can be shown, "
    "roughly, historically, ...) gives zero hits. The two '...' occurrences are sequence notation (0, 1, ..., H; f_0, ..., f_H), not omitted content.")
row("lx1b-process-words", "2.9 prose (process words)", "L03.html; L04.html", P,
    f"{O}/prose_scan_r11.out: builder, verifier, architect, fixer, planner, campaign, checkout, ledger, build plan, open item, "
    "DATA_REQUEST, REFERENCE_REQUEST: zero hits in both pages. 'round' appears only in the code identifier round_half_up and in the word 'round' in the rounding docstring.")
row("lx1b-structure", "2.9 structure", "L03.html sections 1-10; L04.html sections 1-9", P,
    "check_pages PASS; section order matches BUILDER_RULES 4 (summary, sections, lab, canon breaks, misconceptions, problems, key results, quiz, references).")
row("lx1b-quiz-explanations", "2.9 quiz", "L03.html quiz (:553-636); L04.html quiz (:479-560)", P,
    "Each correct option and explanation checked against the page: L03 Q1 P_t after m, Q2 psi_0 = 0, Q5 durations, Q7 beta*phi cancels, Q10 Def 4.1, Q11 no credit-channel size; "
    "numeric answers 2.69 (tol .005), 12, 3.426 (tol .0005), 1274345 (tol .5), 8. L04 Q1 (A2), Q2 zero dispersion, numeric 3 and 321, "
    "0.027935, ln 1.1 0.095310, 0.1358 (tol .00005) all match the output and derivations.")
row("lx1b-L03-remark42-solvency", "2.4 / 2.9", "L03.html:64, :67 (Assumption 1.2); :394-395 (Remark 4.2)", P,
    "Assumption 1.2 V_m < N_0 + D and Prop 3.2(a) give V_t < N_0 + D and N_t > 0 for every t (L03.html:395); the claim that the model "
    "has no illiquidity or collateral term is true of Assumptions 1.1-1.3 as written.")
row("lx1b-L03-ratio-claims", "2.3 / 2.4 claims", "L03.html:404 (functional-form bullet); :516 (R1); :523 (R2); :117-121 (Prop 3.2 proof)", P,
    "Squared-premium ratio: depth ratio becomes r^2 = 11.737 against r = 3.426 (rederive_r11.out), so the claim that it differs whenever r != 1 holds; "
    "slope cancels; Problem R2 proof holds for any strictly increasing G on [D,C).")
row("lx1b-L03-r1-no-result", "2.9 no unproved result", "L03.html:516 (R1 solution)", P,
    "R1 says Prop 3.2 is proved for the model without a lending term and does not carry over without a new proof; it asserts no new result.")
row("lx1b-L04-bretton-definition", "2.9 DAG / concept definition / plan decision", "L04.html:38, :86 (dfn placeholder), :81 (Section 2 intro); "
    "plans/LX1-build-plan.md section 0.3 B3, section 12 item 9, binding Architect decisions (line 633); plans/LX1-open-items.md "
    "('Architect decision needed'); tools/check_dag.py:75 (introduced concept must have a <dfn>)", F,
    "L04.html:86 places <dfn id=\"def-bretton-woods-system\" data-concept=\"bretton-woods-system\">Bretton Woods system</dfn> followed by "
    "'definition pending.' The binding decision (plan line 633) says 'the Bretton Woods definition and end date wait for a request', and "
    "section 12 item 9 says the L04 page 'states only the lab's facts and the first MANIFEST month'. The open-items file records that the "
    "placeholder is a reading the architect must confirm, and no architect ruling exists in plans/FINAL-ARCHITECT-RULINGS.md "
    "(grep for Bretton and LX1: no hit). check_dag passes only because a <dfn> exists. Status unchanged from round 10.",
    "Architect ruling required, one of: (a) admit a primary or survey source for the Bretton Woods system through "
    "tools/add_reference.py (allow-listed issuer or publisher URL) and define the concept from it with a locator; or (b) record in "
    "plans/LX1-build-plan.md that a pending placeholder <dfn> satisfies check_dag, and then this row passes. Until one is recorded, "
    "the row stays FAIL. No builder edit is requested beyond the ruling.")
row("lx1b-L04-prediction-tested", "2.5 labs (hypothesis)", "L04.html:114 (hypothesis); lab-LX1-L04-1.py Parts A and C", P,
    "The hypothesis says Part A returns exactly zero (printed 'all exactly zero: True') and that the recorded column has nonzero dispersion, "
    "which Part C prints (0.027935, 0.024700) and the lab does not assert.")
row("lx1b-L03-lab-checks-overreach", "2.5 labs (claims vs code)", "L03.html:145, :383; twin Parts B-D", P,
    "Part B prints depth, first period, X deeper, difference; Part C checks adjacent non-decrease and strict increase (code lines in twin); "
    "Part D prints one ratio per product with no equality test. Prose says exactly these things. The 'does not evaluate part (b)' statement "
    "holds: the twin computes the depth from the path (max), not from the closed form.")
row("lx1b-L03-misconception-scope", "2.9 claims", "L03.html:418 (misconception 2); proof L03.html:130", P,
    "Corollary 3.3 proof uses only the durations, the closed form, V_m < C, Lemma 3.1 and Prop 3.2(b) (L03.html:130, :418) as stated.")
row("lx1b-L04-A2-before-defined", "2.9 terms before definition", "L04.html:84-92 (Definition 2.1, Prop 2.2 hypotheses), :397-403 (Problem P2), :447-453 (R2)", P,
    "(A2) is defined in Definition 2.1 before Proposition 2.2 uses it; (A3) is introduced as an assumption in Problem P2 before R2 and the quiz use it. "
    "Dispersion is pointed to Definition 1.1 at L04.html:51 before use in Section 2.")
row("lx1b-L04-keyresults-locator", "2.3 key results", "L04.html:470-473 (key results rows 3 and 4)", P,
    "Row 3: 0.027935, 0.024700, ratio 0.8842 match the expected block; row 4: 1976-07, 2012-07, 2019-11 match Part B.")
row("lx1b-cards-l03-l04", "2.7 cards", "course/modules/LX/LX1/cards.json (48 L03/L04 cards: 28 L03, 20 L04)", P,
    f"{SC}/cards_r11.py ({O}/cards_r11.out): 78 cards in the unit, no duplicate id or front; every decimal, date and 3-plus-digit number in each L03/L04 back appears in its lesson (script reports zero misses). "
    "Full read of all 48 L03/L04 cards this round; checked against the current lesson text.")
row("lx1b-cards-c052-c053", "2.7 cards (delta)", "course/modules/LX/LX1/cards.json LX1-c052, LX1-c053", P,
    "Card LX1-c052 (Prop 2.2 hypotheses) and LX1-c053 (Definition 2.1 with (A2) as x_t = kappa from the month before the window's first change) "
    "match L04.html:84-92 verbatim in substance; c059 and c062 agree with Remark 2.3 and Section 4.")
row("lx1b-delta-hunks", "delta reading (round 10 pin 00a84795 to 11d7077)", "L03.html :51 (why-it-matters), :54 (section 1 sentence), :72 (Assumption 1.3), :76 (honest-pending), :124 (Cor 3.3 title); "
    "L04.html :84-92 (Def 2.1, Prop 2.2), :225-226 (twin docstring copy), :329 (Exchange rates bullet); cards.json LX1-c052, LX1-c053 (c012 and c022 are L01/L02, other slices)", P,
    f"git diff 00a84795 11d7077 for course/modules/LX/LX1/L03.html, L04.html, cards.json and tests/labs/LX1/lab-LX1-L04-1.py read hunk by hunk "
    "(the only changes in this slice). Each changed hunk was re-verified above: the Assumption 1.3 'Definition 2.1' pointers, the "
    "'A period on parity' sentence, the Corollary 3.3 title, the Exchange-rates bullet (no covered-interest-parity name), the Definition 2.1 "
    "A2 wording and the twin docstring (now matches the code, which converts once to float before the log).")
row("lx1b-L03-partD-label", "2.5 labs (printed text vs code)", "tests/labs/LX1/lab-LX1-L03-1.py:171; L03.html:383 and expected block", P,
    "twin line 171 prints 'Part D: the ratio of the two depths for three values of the product beta * phi'; the expected block line matches; "
    "the interpretation's three products 1/2, 1, 3 match the code tuples.")
row("lx1b-L03-line121-lab-formula", "2.4 / 2.5 (lab does not evaluate part (b))", "L03.html:121; :145; twin depth()", P,
    "The twin's depth() takes max over depth_path (no closed form), matching the sentence at L03.html:121.")
row("lx1b-L03-why-ordering", "2.9 claims", "L03.html:51 (why-it-matters)", P,
    "'Its ordering follows from Assumptions 1.1 to 1.3 (Corollary 3.3) and is not evidence about any economy' matches Cor 3.3's conditional form.")
row("lx1b-L04-spot-only", "2.8 data register", "L04.html:329 ('Exchange rates only'); tools/data_sources.yaml fx_monthly note", P,
    "data_sources.yaml fx_monthly note: 'Spot rates only, as for fx_daily'; the bullet's spot/forward wording and the no-interest-column claim "
    "match the CSV header (AUD..SEK, no rate column other than FX).")
row("lx1b-L03-honest-pending-source", "2.8 honest data", "L03.html:76 (honest-pending note)", P,
    "States the curriculum names embedded data, none is embedded, the lab is SIMULATED, and it stays SIMULATED until a series is embedded; "
    "matches plans/LX1-open-items.md D-1.")
row("lx1b-L04-twin-docstring-float", "2.5 labs (docstring vs code)", "tests/labs/LX1/lab-LX1-L04-1.py:111-112; "
    "course/modules/LX/LX1/L04.html:225-226 (embedded copy)", P,
    "Round-10 FAIL cleared: the docstring now reads 'The ratio is an exact Fraction, converted once to a float before the logarithm'. "
    "The code is math.log(float(rate / previous)), so the sentence is true. Page copy identical (compare_r11.out, 'page code equals twin source: True').")

fragment = {
    "unit": "LX1",
    "slice": "LX1-b",
    "round": 11,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-b (L03, L04 and lab twins), round 11; did not build LX1 or LX1-b",
    "pin": "11d7077a290f7960b183d3a5a6631af4773888f9",
    "base": "00a84795 (round-10 pin); delta read hunk by hunk. No row carried from round 10: every row re-checked on 11d7077.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE11-LX1-b",
    "scratch": "/tmp/lx1b-r11 (twin runs), /tmp/lx1b-r11-fetch2 (fx_monthly rebuild), /tmp/lx1b-r11-guard, /tmp/lx1b-r11-fed-disclaimer.html",
    "verified_at": "2026-11-05T11:30:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "friedman1963monetary: registry record lists Friedman only (book, 1963); the curriculum string is 'Friedman & Schwartz (1963)' "
        "(curriculum/06-profession-capstone.yaml:37). Pages cite the key and the title only. Architect may correct via tools/add_reference.py (plan N2).",
        "Bernanke (1983), AER 73(3) (curriculum/06-profession-capstone.yaml:38): no registry record (plan B2, REFERENCE_REQUEST 2). L03 makes no empirical attribution to it.",
        "Bretton Woods (plan B3, REFERENCE_REQUEST 3): no registry source. L04 defines nothing historical; the pending placeholder is the open question (row lx1b-L04-bretton-definition).",
    ],
    "freshness_flags": [],
    "notes": [
        "Mutants: none. LX1 is rubric-only; run_graders.py prints 'no autograder (grading: rubric)' (out/run_graders.out). Lab twins are demonstrations, so no mutation testing applies (VERIFIER_RULES 2.5 and the rulings).",
        "Gates run this round (all on 11d7077): check_pages, check_dag, check_projects, run_labs, run_graders, verify_refs --offline and --unit LX1, fetch_data --check, page_smoke for L03 and L04 alone, ruff check and format, mypy --no-incremental on both twins, pytest -k LX1 and its collect-only count. Scripts and outputs: ledgers/LX1/scripts/LX1-b-r11/ (gates_r11.sh, compare_r11.py, rederive_r11.py, guard_r11.py, cards_r11.py, prose_scan_r11.sh, fx_rebuild_r11.sh, licence_r11.sh, make_fragment_r11.py, out/).",
        "Not checked: a Pyodide run of the twins (page_smoke runs its own harness); the hub index.html hours split (outside this slice; 4 x 10 + 10 = 50 is what the slice needs); build_site --check; cards of L01, L02 and the project (other slices); the second author of friedman1963monetary (registry flag, not fixable here); Crossref re-resolution beyond verify_refs --unit LX1.",
        "Not an independent source check of the Fed series: the fx_monthly rebuild reproduces the snapshot bytes from the live issuer feed, which is the rule. The live raw file has changed since 2026-10-19 (raw_sha256 differs), as BUILDER_RULES 6.6 expects.",
    ],
    "summary": "LX1-b round 11 on 11d7077 (delta from 00a84795): verdict FAIL. 58 rows: pass=57 fail=1 unverifiable=0. "
               "Only non-PASS: lx1b-L04-bretton-definition (the Bretton Woods pending <dfn> is an architect decision still unrecorded). "
               "Round-10 FAIL lx1b-L04-twin-docstring-float is cleared (page and twin both fixed).",
}

out = root / "ledgers/LX1/LX1-b.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "pass", sum(r["status"] == P for r in rows), "fail", sum(r["status"] == F for r in rows))
