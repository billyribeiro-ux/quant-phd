"""Slice e, round 3: write the E4 slice-e ledger fragment (ledgers/E4/E4-e.json) from the rows verified at pin 67a2d13.

Usage (from the checkout root): python -I ledgers/E4/scripts/E4-e-r3/build_fragment.py
Each row cites the command output in ledgers/E4/scripts/E4-e-r3/out/ or the lesson/card locator it checked by hand.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path

OUT = "ledgers/E4/scripts/E4-e-r3/out"
rows: list[dict[str, str]] = []


def row(row_id: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    entry = {"id": row_id, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        entry["fix"] = fix or ""
    rows.append(entry)


row("E4-e-r1-scan-structure", "2.7-scan", "course/modules/E/E4/cards.json (all 220 entries)", "PASS",
    f"Command: python -I ledgers/E4/scripts/E4-e-r3/card_scan.py course/modules/E/E4/cards.json references/references.json; "
    f"{OUT}/run_slice_e_r3.out lines 1-12: cards=220; ids E4-c001..E4-c220 unique and in order of creation; 0 duplicate id, "
    "front, back or normalised front; cards per lesson L01 18, L02 22, L03 15, L04 25, L05 27, L06 31, L07 21, L08 38, L09 23 "
    "(sum 220); grades T 146, C 20, none 54; the only cite key muth1961rational is in references/references.json; every T or C "
    "card has a basis. Delta since round-2 pin 67c47689: cards.json diff of 162 lines (c011, c013, c025, c036, c044, c048, c061, "
    "c063, c064, c067, c077, c091-c093, c107, c119, c120, c141-c145, c156, c174, c176, c196, c199, c203, c209, c210 edited; "
    "c212-c220 appended). Every hunk was read against the current lesson text (rows below).")
row("E4-e-r1-card-references", "2.7-references", "cards.json front/back vs L01-L09 text", "PASS",
    f"Command: python -I ledgers/E4/scripts/E4-e-r3/card_refs.py course/modules/E/E4/cards.json scratch/txt (scratch/txt from "
    f"html_to_text.py); {OUT}/run_slice_e_r3.out lines 13-19: references checked=200 missing=0. Cross-lesson items re-read in "
    "their own lesson: c054 and c074 'Assumption A3' (L04 and L05 bullets); c075, c076 'Assumption A1/A2' (L05.txt lines 0019-0020); "
    "c176 'Definition 7.1' (L07.txt line 0019).")
row("E4-e-r1-numbers", "2.2-numbers", "cards.json numeric tokens vs lesson text", "PASS",
    f"Command: python -I ledgers/E4/scripts/E4-e-r3/card_numbers.py; {OUT}/run_slice_e_r3.out lines 20-54: numeric tokens checked=350 "
    "missing=1. The one miss, 3/32 in E4-c037, is typeset as \\tfrac{3}{32} in scratch/txt/L02.txt (Misconception 2) and equals "
    "1/8 - 1/32 by hand. The OTHER lines are LaTeX-typeset fractions or values printed in another E4 lesson, each read in its line. "
    "New card numbers (c212, c213: 56, 340/3, 235/4) are in L01 text and in the lab printout. The second claim (0,60,120,30) of "
    "c212 appears in the lab source embedded on L01.html (tests/labs/E4/lab-E4-L01-1.py line 26), which is part of the page, not in "
    "the prose. indep_checks.py re-derives the block values (row E4-e-r2-indep-checks).")
row("E4-e-r1-cite-muth1961rational", "2.1-citation",
    "references/references.json entry muth1961rational; E4-c099; course/modules/E/E4/L05.html line 295", "PASS",
    "Plain curl at round 3: curl -s https://api.crossref.org/works/10.2307/1909635 returned title 'Rational Expectations and the "
    "Theory of Price Movements', container Econometrica, volume 29, issue 3, page 315, author Muth, published-print 1961-07. "
    "references/ unchanged since pin 1c1645f3 (git diff 1c1645f3 67a2d13 -- references is empty). L05.html line 295 cites the key "
    "with data-locator='title'; the E4-c099 back claims only the title use, which matches L05.txt line 0065.")
row("E4-e-r1-verify-refs", "2.1-registry", "references/references.json (whole registry, offline integrity)", "PASS",
    f"Command: .venv/bin/python tools/verify_refs.py --offline; {OUT}/run_slice_e_r3.out line 364: "
    "'offline integrity: 560 entries, 0 problems'.")
row("E4-e-r1-check-pages", "2.9-structure", "tools/check_pages.py --unit E4 (includes check_cards); tools/check_dag.py --unit E4",
    "PASS", f"Commands at pin 67a2d13: check_pages.py --unit E4 -> 'check_pages E4: PASS'; check_dag.py --unit E4 -> "
    f"'check_dag E4: PASS' ({OUT}/run_slice_e_r3.out lines 154-157).")
row("E4-e-r1-run-labs", "2.5-labs", "tests/labs/E4/lab-E4-L0[1-9]-1.py (the labs whose printed values the cards cite)", "PASS",
    f"Command: tools/run_labs.py --unit E4 -> 'run_labs E4: PASS (12/12)' ({OUT}/run_slice_e_r3.out line 159). run_twins.sh "
    f"(python -I -W error on all nine twins) exit 0, output lines 160-352. Page code blocks equal their twins on all nine pages "
    "(ledgers/E4/scripts/E4-e-r3/page_twin_equal.py: equal=[True] x9, trailing newline ignored). Every number a card quotes from a lab "
    "was matched to the printed output, including the L06 twin whose docstring changed in this delta (printed values unchanged).")
row("E4-e-r2-delta", "2.7-delta", "git diff 67c47689 67a2d13 -- course/modules/E/E4 tests/labs/E4", "PASS",
    "16 files changed (cards.json 162 lines; L01-L09.html; tests/labs/E4/lab-E4-L06-1.py; grader and project files, out of slice). "
    "The lesson hunk set is saved at ledgers/E4/scripts/E4-e-r3/delta_lessons_r3.diff (301 lines) and read in full. Hunks that touch a "
    "cited claim were re-checked against the card: the L03 key-results row now reads MRS_12 = 4, MRS_13 = 2, MRS_23 = 1/2 (this fixes "
    "the round-2 note on 0-based labels and matches E4-c046); the L08 Res 1 solution is unchanged (see E4-e-r1-card-E4-c176); the L09 "
    "Res 3 solution is unchanged (see E4-e-r3-c209).")
row("E4-e-r2-notation", "2.4-notation", "cards.json symbols vs notation/notation.json", "PASS",
    f"Command: python -I ledgers/E4/scripts/E4-e-r3/notation_check.py; {OUT}/notation_check.out: registered symbols T, Phi, gamma_3, "
    "gamma_4, R^*, R^{e*}, R_f, Q; standalone T in card text 0; no Greek gamma; no other registered symbol in a card. The 4 superscript "
    "transposes (^T, L04 cards) are matrix transposes, not the registered T (number of observations).")
row("E4-e-r2-twins-isolated", "2.5-labs", "tests/labs/E4/lab-E4-L0[1-9]-1.py run with python -I -W error", "PASS",
    f"Command: sh ledgers/E4/scripts/E4-e-r3/run_twins.sh -> exit 0 (nine blocks; {OUT}/run_slice_e_r3.out lines 160-352).")
row("E4-e-r2-indep-checks", "2.2-numbers",
    "ledgers/E4/scripts/E4-e-r3/indep_checks.py (re-derives the card numbers from the closed forms)", "PASS",
    f"Command: python -I ledgers/E4/scripts/E4-e-r3/indep_checks.py; {OUT}/run_slice_e_r3.out lines 55-153: 'FAILS: 0 []'. Stdlib "
    "Fractions; covers L01 340/3, 56, 596/3, 235/4; L02 prices, wealth, ratios 16/9 and 16/7, 3/32; L03 MRS 4, 2, 1/2 and grid counts; "
    "L04 ranks; L05 fixed points and ratios; L06 theta, b = 7/9, V_U = 2/3, x_I = 1/7, residual -9/85; L07 sweeps; L08 G(0), G(1), "
    "boundary gaps and Corr^2 at lam*; L09 counts 500, 625, 15625 and the two-prior receipts.")
row("E4-e-r2-ruff-scripts", "lint", "ledgers/E4/scripts/E4-e-r3/*.py", "PASS",
    f"Commands: .venv/bin/ruff check ledgers/E4/scripts/E4-e-r3 -> 'All checks passed!'; .venv/bin/ruff format --check "
    f"ledgers/E4/scripts/E4-e-r3 -> '8 files already formatted' ({OUT}/ruff.out).")
row("E4-e-r2-cards-211", "2.7-card", "cards.json E4-c211 (L09, Problem Res 2)", "PASS",
    "Back re-derived: x(H) = 1, x(L) = -t, t = theta/(1 - theta), theta = (p + r)/2. Trader 1 receipt (p - theta)/(1 - theta) > 0 iff "
    "theta < p; trader 2 receipt (theta - r)/(1 - theta) > 0 iff theta > r. Matches L09.html Res 2 solution and indep_checks.py.")
row("E4-e-r2-grades", "2.3-grades",
    "cards.json E4-c141..E4-c145 grades vs L07 key-results row (course/modules/E/E4/L07.html; scratch/txt/L07.txt line 0130)", "PASS",
    "Round-2 FAIL is resolved: c141-c145 are C with basis 'Finite check: L07 lab (Lab 1), Parts A to E', and the L07 key-results row "
    "(L07.txt line 0130) grades the same base-instance and sweep values C 'Finite check: Lab 1, Parts A to E (exact)'. The lesson legend "
    "(L07.txt line 0013) defines C as 'single study or finite check', and the signs of the responses are graded T (Proposition 7.7, "
    "L07.txt line 0038; key results line 0128). Every other graded card was re-graded against BLUEPRINT section 3 and its lesson "
    "key-results row: T cards are theorems or exact derivations on the page, C cards are lab finite checks or SIMULATED draws. Not "
    "scored: c186 combines a T statement with C lab numbers; its grade is conservative, not a mismatch.")
row("E4-e-r1-card-E4-c016", "2.7-card",
    "cards.json E4-c016 (L01); L01 Misconception 3 (scratch/txt/L01.txt line 0073); tests/labs/E4/lab-E4-L01-1.py main()", "PASS",
    "Lab main() calls check_probabilities(STATE_PROBABILITIES) before Part A (lab-E4-L01-1.py lines 59-61); Proposition 1.4 uses no "
    "probability (L01.html Proposition 1.4 proof). The card matches L01.txt line 0073.")
row("E4-e-r1-card-E4-c099", "2.7-card", "cards.json E4-c099 (L05); L05.txt line 0065", "PASS",
    "Front and back match L05.txt line 0065: the title use of Muth (1961) only; no result of the paper is used. Registry key verified "
    "above.")
row("E4-e-r1-card-E4-c206", "2.7-card",
    "cards.json E4-c206 (L09); L09.txt lines 0059-0060; tests/labs/E4/lab-E4-L09-1.py Part B", "PASS",
    f"Corollary 2.3 and the Lab 1 Part B counts (500 strictly accepted at state 1; none nonnegative on the meet) match L09.txt line 0060 "
    f"and {OUT}/run_slice_e_r3.out; Example 2.4 (private acceptance) matches L09.txt line 0051.")
row("E4-e-r1-cards-001-010", "2.7-cards", "cards.json E4-c001..E4-c010 (L01)", "PASS",
    "Each card re-read against L01.txt lines 0018-0047 (Definitions 1.1-1.9, Propositions 1.4, 1.7, 1.8, 1.10). T grades for "
    "Propositions 1.4, 1.7, 1.8 and 1.10 match BLUEPRINT section 3 (proved on the page).")
row("E4-e-r1-cards-011-020", "2.7-cards", "cards.json E4-c011..E4-c020 (L01, L02)", "PASS",
    "c011 and c013 (edited) re-checked against Lab 1 Parts B and D (340/3, 596/3, 235/4). c014, c015, c016 checked against Remark "
    "1.11, Misconception 1 and Misconception 3 and the lab. c017-c020 re-read against L02 Section 1 and Definitions 2.1-2.2.")
row("E4-e-r1-cards-021-030", "2.7-cards", "cards.json E4-c021..E4-c030 (L02)", "PASS",
    "c025 (edited) re-checked against the Lemma 2.4 proof (L02.txt lines 0034-0036); c021-c024 against Definitions 2.2-2.3 and A5; "
    "c026-c030 against Proposition 2.5, Corollary 2.7, Propositions 2.8 and 2.9.")
row("E4-e-r1-cards-031-040", "2.7-cards", "cards.json E4-c031..E4-c040 (L02, L03)", "PASS",
    "c031-c038 re-checked against Example 2.11, Lab 2 Parts B-D and the three L02 misconceptions (L02.txt lines 0074-0081); c037 uses "
    "Misconception 2 and 3/32 = 1/8 - 1/32. c039, c040 against Definitions 3.1-3.2.")
row("E4-e-r1-cards-041-050", "2.7-cards", "cards.json E4-c041..E4-c050 (L03)", "PASS",
    "c044 (edited) against Proposition 3.4 Step 1; c048 (edited, grade C) against Lab 3 Part B. c049 derivatives 1/12 and 1/4 "
    "re-derived from Problem R2 (L03.txt line 0110). c041-c043, c045-c047 against Definition 3.3, Proposition 3.4 (a)/(b), Remark 3.5, "
    "Example 3.6 and Lab 3 Part A.")
row("E4-e-r1-cards-051-060", "2.7-cards", "cards.json E4-c051..E4-c060 (L03, L04)", "PASS",
    "c051, c052 against L03 Misconceptions 2 and 3 and Proposition 3.4. c053-c060 against Definition 1.1, Lemma 1.2, Definition 1.3, "
    "Theorem 1.4, Proposition 1.5 and Corollary 1.6 (L04.txt lines 0017-0037).")
row("E4-e-r1-cards-061-070", "2.7-cards", "cards.json E4-c061..E4-c070 (L04)", "PASS",
    "c061, c063, c064, c067 (edited) checked against Lemma 2.1, Example 2.2 (L04.txt lines 0042-0044), Example 2.3 (line 0046) and "
    "Remark 3.2 (line 0056). c065 against Lab 1 Part C; c066 against Remark 3.1; c068, c069 against Propositions 4.1 and 4.2 (lines 0060-0066).")
row("E4-e-r1-cards-071-080", "2.7-cards", "cards.json E4-c071..E4-c080 (L04, L05)", "PASS",
    "c070-c073 against L04 Misconceptions (L04.txt lines 0069-0079). c074-c076 against L05 Assumptions A1-A3 (L05.txt lines 0019-0021); "
    "c077 (edited) against Definition 1.1 (L05.txt line 0023); c078-c080 against Definitions 1.1 and 1.2.")
row("E4-e-r1-cards-081-090", "2.7-cards", "cards.json E4-c081..E4-c090 (L05)", "PASS",
    "c081-c090 re-derived against Lemma 2.1, Proposition 2.2, Corollary 2.3, Lemma 3.1, Propositions 3.2 and 3.3 and the base fixed "
    "point (L05.txt lines 0029-0052). c083 closed form: c0* = alpha/(beta + varsigma) = 4 and c1* = -delta/(beta + varsigma) = -3/10 at "
    "the base parameters.")
row("E4-e-r1-cards-091-100", "2.7-cards", "cards.json E4-c091..E4-c100 (L05, L06)", "PASS",
    f"c091, c092, c093 (edited) checked against the printed Lab 1 Parts B, C, D paths and ratios ({OUT}/run_slice_e_r3.out, the run_labs "
    "output) and the error definition e_k = c_k - c*. c094 against Part E. c095 against Remark 4.1. c096-c098 against Corollary 2.3, "
    "Proposition 2.2 and the L05 Misconceptions (L05.txt lines 0068-0075). c099 see E4-e-r1-card-E4-c099.")
row("E4-e-r1-cards-101-110", "2.7-cards", "cards.json E4-c101..E4-c110 (L06)", "PASS",
    "c101-c106 against Definitions 6.1-6.2 and A2-A4 (L06.txt lines 0019-0029). c107 (edited) against the A4 text (L06.txt line 0029) "
    "and the probability-one quiz item (L06.html). c108 against Assumption G (line 0031). c109 against Definition 6.6 (line 0051). c110 "
    "against Lemma 6.2.")
row("E4-e-r1-cards-111-120", "2.7-cards", "cards.json E4-c111..E4-c120 (L06)", "PASS",
    "c111-c113 against Lemmas 6.3 and 6.4 (L06.txt lines 0040-0046). c114, c115 against Proposition 6.7 (a) and (b). c116, c117 against "
    "Corollary 6.8. c118, c119 (edited), c120 (edited) against Example 6.9 (L06.txt line 0066) and Lab 1 Parts A-C.")
row("E4-e-r1-cards-121-130", "2.7-cards", "cards.json E4-c121..E4-c130 (L06, L07)", "PASS",
    "c121 against Remark 6.10 (L06.txt line 0068). c122-c125 against Lab 1 Parts C, D, E (16 grid points, residual -9/85, slopes "
    "0.426617 and 0.761928 within tolerance). c126-c129 against Remark 6.10 and the L06 Misconceptions (L06.txt lines 0083-0093). "
    "c130 against Definition 7.1 (L07.txt line 0019).")
row("E4-e-r1-cards-131-140", "2.7-cards", "cards.json E4-c131..E4-c140 (L07)", "PASS",
    "c131-c136 against Definitions 7.1 and 7.2, Lemmas 7.3 and 7.4 and Remark 7.5 (L07.txt lines 0019-0031). c137-c140 against "
    "Propositions 7.6 and 7.7 and Remarks 7.8 and 7.9 (L07.txt lines 0034-0044).")
row("E4-e-r1-cards-141-150", "2.7-cards", "cards.json E4-c141..E4-c150 (L07)", "PASS",
    f"c141-c145 values re-derived (rho^2 4/9, 1/3, 1/6, 1/18, 1/66; Var(p) 729/1444 and 35937/4802; lam sweep 1/6, 1/3, 9/22; a sweep "
    f"4/9, 1/3, 1/6) against the Lab 1 printout (L07.txt line 0048; {OUT}/run_slice_e_r3.out). Grades now agree with the lesson "
    "(E4-e-r2-grades). c146 (SIMULATED, C) against Part F. c147-c150 against Remark 7.9, Proposition 7.7 and the L07 Misconceptions "
    "(L07.txt lines 0058-0068).")
row("E4-e-r1-cards-151-160", "2.7-cards", "cards.json E4-c151..E4-c160 (L08)", "PASS",
    "c151-c155 against A1, A2, A3 (L08.txt lines 0020-0024) and A5 (line 0122-0123). c156 (edited) against Lemma 2.1 (line 0030: W_0' "
    "is the constant). c157 against Lemma 2.2 (line 0034); c158 against Fact 2.3 (line 0038).")
row("E4-e-r1-cards-161-170", "2.7-cards", "cards.json E4-c161..E4-c170 (L08)", "PASS",
    "c159, c160 against Corollary 2.4 (L08.txt lines 0043-0047). c161 against Lemma 2.5. c162, c163 are checked in "
    "E4-e-r3-c162-c163-basis. c164-c166 against Corollary 3.2 and Lemma 3.3 (a), (b), (c) (lines 0070-0074). c167 against "
    "Proposition 4.1 (lines 0077-0080). c168 against Proposition 4.2. c169 against Definition 4.3. c170 against Proposition 4.4.")
row("E4-e-r1-cards-171-180", "2.7-cards", "cards.json E4-c171..E4-c180 (L08)", "FAIL",
    "c171-c175 and c177-c180 pass (Lemma 4.5, Definition 4.6, the paradox definition, Proposition 5.1(a)-(c), Proposition 5.2(a)-(c), "
    "and the G(0), G(1) closed forms). E4-c176 FAILS: its back says the correlation is undefined because Var(p) = 0, but the L08 Res 1 "
    "solution (course/modules/E/E4/L08.html line 685; L08.txt line 0201) still ends 'so Corr(v,p)^2 = 0'. See E4-e-r1-card-E4-c176.",
    "Fix the lesson, not the card: in course/modules/E/E4/L08.html line 685, replace the final '\\(\\Corr(v, p)^2 = 0\\)' with 'the "
    "correlation is undefined, because \\(\\Var(p) = 0\\) (Definition 7.1 of Lesson L07 requires positive variances)'. Then re-run "
    "check_pages --unit E4 and card_refs.py.")
row("E4-e-r1-card-E4-c176", "2.7-card", "cards.json E4-c176 (L08); course/modules/E/E4/L08.html line 685 (Res 1 solution)", "FAIL",
    "The card back says the correlation is undefined because Var(p) = 0 (Definition 7.1 of L07 requires positive variances). Under "
    "sigma_u^2 = 0 and lambda = 0 the price is constant, so the card is correct. The lesson contradicts it: L08.html line 685 says the "
    "price 'is a function of u alone, which is independent of v, so Corr(v,p)^2 = 0'; L08.txt line 0201 is the same.",
    "Change L08.html line 685 as stated in E4-e-r1-cards-171-180. Keep E4-c176 as it is.")
row("E4-e-r1-cards-181-190", "2.7-cards", "cards.json E4-c181..E4-c190 (L08, L09)", "PASS",
    f"c181 (SIMULATED residual 1.332e-15; slope 0.1595 vs 0.1605, difference 0.0010 <= 0.02), c182-c184 (Part C root at cost 0.15, gap "
    f"1.83e-15, Corr 0.088941; boundary gaps 7.71e-03 and -6.71e-03; Part D zero count and equilibrium flags False) match the printed "
    f"output ({OUT}/run_slice_e_r3.out). c185 against Proposition 5.1(a) and Problem Emp 3 (G(1) = ln(5/3)/4). c186-c188 against "
    "Definition 4.6, Proposition 5.2(b), Lemma 3.3(a) and the grid counts.")
row("E4-e-r1-cards-191-200", "2.7-cards", "cards.json E4-c191..E4-c200 (L09)", "PASS",
    "c189-c195 against B1, B2, B3 and Definitions 1.1 and 1.2 (L09.txt lines 0018-0027). c196 against Definition 2.2. c197 against "
    "Theorem 2.1 (line 0031). c198 against Corollary 2.3 (line 0037). c199 (edited) against Proof 1 (L09.html line 355). c200 (Example "
    "2.4) re-derived: M(1) = {1,2,3}, g_1(1) = 1/2, g_2(1) = 1/3, g_1(3) = -2.")
row("E4-e-r1-cards-201-210", "2.7-cards", "cards.json E4-c201..E4-c210 (L09)", "FAIL",
    "c201-c208 and c210 pass (Lab 1 Part B counts 500, 0, 625, 0; 5^6 = 15625; zero-posterior bets x(3) = 0 and x(2) = -x(1) giving "
    "5 * 5^3 = 625; Misconceptions 1-3; Res 1 derivation S_1 >= 0 and -S_1 - k pi(M) >= 0). E4-c209 FAILS: see E4-e-r3-c209.",
    "See E4-e-r3-c209.")
row("E4-e-r3-c209", "2.7-card", "cards.json E4-c209 (L09 Problem Res 3); course/modules/E/E4/L09.html line 419", "FAIL",
    "The card back says the proof of Theorem 2.1 'uses that the set is a union of cells of both partitions and that every cell has "
    "positive prior probability'. The lesson's Res 3 solution (L09.html line 419; L09.txt line 0120) says 'The proof of Theorem 2.1 "
    "uses only that M is a union of cells of both partitions.' The proof uses pi(D) > 0 (L09.txt line 0033: 'because pi(D) > 0 by B1') "
    "and Proof 1 says the step uses it too (L09.txt line 0086). The lesson's 'only' is false, and card and lesson disagree. The card's "
    "wording is the correct one.",
    "In course/modules/E/E4/L09.html line 419, change 'uses only that M is a union of cells of both partitions' to 'uses that M is a "
    "union of cells of both partitions and that every cell has positive prior probability (Assumption B1)'. Keep E4-c209 as it is.")
row("E4-e-r2-cards-211-round3", "2.7-card", "cards.json E4-c211 (L09, Problem Res 2) re-checked this round", "PASS",
    "Same row as E4-e-r2-cards-211 above, re-verified against the current text: the card and L09.html Res 2 agree.")
row("E4-e-r3-c162-c163-basis", "2.7-card",
    "cards.json E4-c162 (basis, line 1211) and E4-c163 (basis, line 1219); course/modules/E/E4/L08.html lines 151-158 (Proposition 3.1)",
    "FAIL",
    "Proposition 3.1 is an ordered list (L08.html lines 153-156, <ol type=\"a\">): item (a) is the uniqueness statement 'Suppose "
    "sigma_u^2 > 0. If p = alpha + beta_p s - varpi u with beta_p != 0 clears the market ... then varpi/beta_p = kappa ...'; item (b) "
    "is the existence statement 'The price p* clears the market in every state'. The proof says 'This proves (a)' for uniqueness and "
    "'running it backwards ... gives (b)' for existence (L08.txt lines 0059-0063). E4-c162 (existence) cites 'Proposition 3.1 (a)' and "
    "E4-c163 (uniqueness) cites 'Proposition 3.1 (b)': the two basis labels are swapped. The statements of c162 and c163 are correct.",
    "In cards.json, change the basis of E4-c162 to 'Proposition 3.1 (b), proof in §3' and the basis of E4-c163 to 'Proposition 3.1 (a), "
    "proof in §3'. Then re-run card_refs.py and check_pages --unit E4.")
row("E4-e-r3-c212-c220", "2.7-card", "cards.json E4-c212..E4-c220 (new in this delta)", "PASS",
    "c212 (value 56 of (0,60,120,30) at (1/2,1/3,1/4,1/5): 0 + 20 + 30 + 6 = 56; Lab 1 Part B value_of_other 56); c213 (equality flag "
    "False; 340/3 and 235/4); c214 (Lab 3 Part B: 2 Pareto improvements; the first, (2,4,3)/(2,4,1), is feasible and both agents are "
    "strictly better off by ln arithmetic); c215 (Lemma 2.1: pivots = rank); c216 ((0,0,1) not attainable, augmented rank 3, Example "
    "2.2); c217 (fourth row (1,2,3) = e_1 + 2e_2 + 3e_3, Example 2.3); c218 (Remark 3.2: kernel nonzero when rank < J); c219 (Lab 1 "
    "Part C prints c0* = 5/2, c1* = -3/16; L05.txt line 0055); c220 (x_U = (b p - p)/(a V_U) = -1/7 with b = 7/9, p = 3/7, V_U = 2/3; "
    "clearing identity; Example 6.9 in L06.txt line 0066). Ids unique; T for derived results, C only where the basis names a lab.")
row("E4-e-r3-duplicate-scan", "2.7-meta", "cards.json duplicate scan (fronts, backs, normalised fronts) and card-to-card overlap",
    "PASS", f"{OUT}/run_slice_e_r3.out lines 3-8: duplicate id/front/back and normalised front all 0. Overlapping pairs (c011/c212, "
    "c013/c213, c048/c214, c202/c203) state different claims or different counts and are kept.")

ids = [r["id"] for r in rows]
duplicated = sorted({i for i in ids if ids.count(i) > 1})
if duplicated:
    raise SystemExit(f"duplicate row ids: {duplicated}")
fails = [r for r in rows if r["status"] != "PASS"]
fragment = {
    "unit": "E4",
    "slice": "e",
    "round": 3,
    "verifier": "independent verifier (Haiku 5.5), slice e: all 220 cards in course/modules/E/E4/cards.json against lessons L01-L09",
    "pin": "67a2d13e7575608e95b2e34a9c7c2a82c61b117b",
    "base": "67c47689c49435bc0e6639e3de4feded5eefdd64 (round 2 pin, fragment frags/E-E4-e.round2.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE3-E4-e",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE3-E4-e/scratch",
    "verified_at": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "verdict": "FAIL" if fails else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: all 220 cards. Each card was checked against the lesson text it cites (L01-L09 rendered by html_to_text.py into scratch/txt). "
        "Full text was read for L01, L05, L07 and L03 lines 1-135, L04 lines 1-110, L02 lines 1-100, L06 lines 1-110, L08 lines 1-205 and "
        "L09 lines 1-140. Problem and quiz sections after those spans were not re-read this round; cards cite only the spans listed.",
        "Mutation testing does not apply to a card slice (no grader); mutants is empty.",
        "Ruling used: a C grade on a finite check of exact instances is accepted when the lesson legend (L07.txt line 0013) uses C for "
        "'single study or finite check'.",
    ],
    "summary": {
        "cards": 220,
        "rows": len(rows),
        "pass": len(rows) - len(fails),
        "fail": len(fails),
        "unverifiable": 0,
        "failing_row_ids": [r["id"] for r in fails],
        "failing_card_ids": ["E4-c176", "E4-c209", "E4-c162", "E4-c163"],
    },
}
Path("ledgers/E4/E4-e.json").write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "fail", len(fails), "verdict", fragment["verdict"])
