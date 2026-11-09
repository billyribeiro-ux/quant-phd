"""Builds the round-5 fragment ledgers/M2/M2-b.json for M2 slice b (pin dde0486b). Rows are written by hand above the call."""
import json
import sys
from datetime import datetime, timezone

PRIOR = "Carried from round 4 (byte-identical since the previous pin edbb7aa8; identity in ledgers/M2/scripts/M2-b-r5/carry_identity_r5.out): "
CARRY_FILES = {
    "L08": "course/modules/M/M2/L08.html, tests/labs/M2/lab-M2-L08-1.py",
    "L09": "course/modules/M/M2/L09.html, tests/labs/M2/lab-M2-L09-1.py",
    "L11": "course/modules/M/M2/L11.html, tests/labs/M2/lab-M2-L11-1.py",
    "L12": "course/modules/M/M2/L12.html, tests/labs/M2/lab-M2-L12-1.py",
}
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


def carried(rid, check, location, lesson_kinds, prior_evidence):
    files = ", ".join(CARRY_FILES[k] for k in lesson_kinds)
    row(rid, check, location, "PASS", "Carried from round 4 (" + files + " byte-identical since the previous pin edbb7aa8): " + prior_evidence)


G = "ledgers/M2/scripts/M2-b-r5/"

row("RUN-M2-CHECKS", "2.9 gates: check_pages, check_dag, check_projects, run_labs (unit M2), plus --all for the three static gates",
    "tools/check_pages.py --unit M2; tools/check_dag.py --unit M2; tools/check_projects.py --unit M2; tools/run_labs.py --unit M2",
    "PASS",
    G + "g01_check_pages_M2.out: 'check_pages M2: PASS' exit 0; " + G + "g02_check_dag_M2.out: 'check_dag M2: PASS' exit 0; "
    + G + "g03_check_projects_M2.out: 'check_projects M2: PASS' exit 0; " + G + "g04_run_labs_M2.out: 'run_labs M2: PASS (27/27)' exit 0; "
    + "g04b-d (--all): every unit LX1, LX2, PC3 PASS, exit 0. Re-run this round at dde0486b.")

row("LAB-GATES", "2.5 labs: ruff check and format, mypy strict, relevant pytest on the slice twins",
    "tests/labs/M2/lab-M2-L07-1.py .. lab-M2-L12-1.py",
    "PASS",
    G + "g07_ruff_check_M2_twins.out: 'All checks passed!' exit 0; " + G + "g07b_ruff_format_M2_twins.out: '27 files already formatted' exit 0; "
    + G + "g08_mypy_M2_twins.out: 'Success: no issues found in 27 source files' exit 0; "
    + G + "g09_pytest_labs_pagechecks.out: pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_refs.py -k 'M2 or lab or page' exit 0 (all dots, no failures).")

row("PAGE-SMOKE-L07-L12", "2.5/2.9 page_smoke (Chromium, light and dark, 360 px, figure sweep) for L07-L12 alone",
    "tools/page_smoke.py --unit M2 --pages L07 L08 L09 L10 L11 L12",
    "PASS",
    G + "g06_page_smoke_L07_L12.out: six 'page_smoke modules/M/M2/Lnn.html: PASS' lines, 'page_smoke M2: PASS', exit 0. "
    "The six slice pages contain no <svg>, <img>, <canvas> or <figure> (grep count 0 for each), so there is no figure to inspect; the screenshot check is not applicable.")

row("TWIN-ISOLATED", "2.5 labs: each slice twin run alone under python -I -W error from a scratch directory",
    "tests/labs/M2/lab-M2-L07-1.py .. lab-M2-L12-1.py",
    "PASS",
    G + "g05_twins_isolated_L07_L12.out: exit 0 for L07..L12; " + G + "twin_L07..L12.stderr are 0 bytes; stdout line counts 43, 17, 22, 26, 10, 21 (as in round 4).")

row("REFS-OFFLINE", "2.1 citations: verify_refs offline and live for M2; slice cites no registry key",
    "tools/verify_refs.py --offline; tools/verify_refs.py --unit M2; course/modules/M/M2/L07.html..L12.html",
    "PASS",
    G + "g10_verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems' exit 0; " + G + "g15_verify_refs_live_M2.out: 'live re-verification of M2: 2 of 560 entries, 0 problems' exit 0. "
    "grep for data-cite, data-key, data-locator, class=\"claim\" in L07..L12: 0 hits in all six pages (no registry key cited).")

row("DELTA-HUNKS", "2.1-2.9 round-5 delta: every hunk in the slice paths between edbb7aa8 and dde0486b",
    "course/modules/M/M2/L07.html; course/modules/M/M2/L10.html; tests/labs/M2/lab-M2-L07-1.py; course/modules/M/M2/cards.json",
    "PASS",
    "Slice hunks read in full: " + G + "delta_L07_L10_lab.diff and " + G + "delta_cards.diff. L07.html: 6 hunks (meta prose at 140-143; helper and docstring at 229-236, renamed g_prime_formula; part D loop at 243-253; expected block lines 297 and 305; interpretation at 309). "
    "L10.html: 2 hunks (101-102 Corollary 3.1 quantifier 0 <= a <= b; 385-388 key-results row). lab-M2-L07-1.py: 3 hunks (docstring, helper, part D print). "
    "cards.json: slice hunks M2-c085 (T), M2-c129 (T), M2-c137 (0 <= a <= b), appended M2-c422 (L07, C) and M2-c423 (L09, C). Out-of-slice hunks in the same file (M2-c009 L01, c048 L04, c068 L06, c293 L19) and in L02, L03, L05, L06, index.html, project.html and plans/FINAL-ARCHITECT-RULINGS.md, plans/KNOWN-ISSUES.md were read and are not graded here (rulings 27-29 concern E3 only; ruling 26 read).")

row("LAB-L07", "2.5 lab: L07 lab 1 twin, page code equals twin, expected block equals a fresh run, hypothesis and interpretation match the output",
    "course/modules/M/M2/L07.html lab section (line ~160-315); tests/labs/M2/lab-M2-L07-1.py",
    "PASS",
    G + "g04_run_labs_M2.out: run_labs PASS (code byte-identical to twin, twin exit 0 under -I -W error, expected block matches stdout); " + G + "g05 twin output 43 lines. "
    "Hypothesis sentence: parts A to D as printed (27 checks, 0.0000025307 at n=10, errors -2 to -2048, right quotient +2 and left -2 at six steps). "
    "Interpretation sentence: part D evaluates 2|x| at 0 giving 0 = g'(0) from Example 4.1, which matches the code. Part D quotients and parts A-C values recomputed in " + G + "numbers_r5.out.")

row("LAB-L08", "2.5 lab: L08 lab 1 twin, page code equals twin, expected block equals a fresh run",
    "course/modules/M/M2/L08.html lab section; tests/labs/M2/lab-M2-L08-1.py",
    "PASS",
    PRIOR + "round-4 evidence ledgers/M2/scripts/M2-b-r4/g11_lab_match_L07_L12.out ('L08: page_code_eq_twin=True ... expected_eq_output=True ... run_exit=0') and run_labs PASS (27/27) re-run this round in " + G + "g04_run_labs_M2.out.")

row("LAB-L09", "2.5 lab: L09 lab 1 twin, page code equals twin, expected block equals a fresh run",
    "course/modules/M/M2/L09.html lab section; tests/labs/M2/lab-M2-L09-1.py",
    "PASS",
    PRIOR + "round-4 evidence g11 ('L09: page_code_eq_twin=True ... expected_eq_output=True') and run_labs PASS re-run this round in " + G + "g04_run_labs_M2.out. Part B values 0.15933400 and 0.19, and part C -0.00130208 recomputed this round (" + G + "c126_check_r5.out, " + G + "numbers_r5.out).")

row("LAB-L10", "2.5 lab: L10 lab 1 twin, page code equals twin, expected block equals a fresh run; interpretation and hypothesis match output",
    "course/modules/M/M2/L10.html lab section; tests/labs/M2/lab-M2-L10-1.py (twin unchanged since edbb7aa8)",
    "PASS",
    G + "g04_run_labs_M2.out: run_labs PASS (L10 page code equals twin, expected block equals output); " + G + "g05 twin exit 0 under -I -W error, 26 lines. "
    "Recomputed this round (" + G + "numbers_r5.out): part A U_8 -0.8046875, L_8 -1.1796875, U-L 0.375; part B n=128 L 0.497079213, U 0.502938588, U-L 0.005859375 = 3/512; part C f(0.3) = 0.591715976. Hypothesis (3/n, 3/(4n), error within 1e-7) and interpretation (numerical, not a proof) match the code.")

row("LAB-L11", "2.5 lab: L11 lab 1 twin, page code equals twin, expected block equals a fresh run",
    "course/modules/M/M2/L11.html lab section; tests/labs/M2/lab-M2-L11-1.py",
    "PASS",
    PRIOR + "round-4 evidence g11 ('L11: page_code_eq_twin=True ... expected_eq_output=True') and run_labs PASS re-run this round.")

row("LAB-L12", "2.5 lab: L12 lab 1 twin, page code equals twin, expected block equals a fresh run",
    "course/modules/M/M2/L12.html lab section; tests/labs/M2/lab-M2-L12-1.py",
    "PASS",
    PRIOR + "round-4 evidence g11 ('L12: page_code_eq_twin=True ... expected_eq_output=True') and run_labs PASS re-run this round.")

row("LAB-L07-DOC", "2.5 lab statements vs code: helper name and docstring vs its call at x = 0 (round-4 LOW row)",
    "tests/labs/M2/lab-M2-L07-1.py (g_prime_formula, part D); course/modules/M/M2/L07.html:309 (interpretation)",
    "PASS",
    "Fixed in dde0486b. The helper is now g_prime_formula with docstring 'The formula g'(x) = 2|x| from Example 4.1, evaluated at x = 0 too, where it gives 0 = g'(0).' (lab line ~97). grep for the old name g_prime_for_x_nonzero and the old 'second derivative at 0 from' text in course/modules/M/M2 and tests/labs/M2: no hits. run_labs PASS and the twin exit 0 after the change (" + G + "g04, " + G + "g05).")

row("STRUCT-L07", "2.9 structure: template sections, tiers (3 mechanics, 3 proof, 3 empirical, 3 research), quiz 8-15, key-results table, lesson nav",
    "course/modules/M/M2/L07.html",
    "PASS",
    "Read in full this round: why-it-matters (<=120 words, checked by check_pages), sections 1-5, misconceptions 1-3, problem set M1-M3, P1-P3, E1-E3, R1-R3 each with a solution, key-results table (5 rows), quiz with 9 items, references, nav links (L06 and L08). " + G + "g01_check_pages_M2.out PASS.")

row("STRUCT-L08", "2.9 structure: template sections, tiers, quiz 8-15, key-results table, lesson nav",
    "course/modules/M/M2/L08.html",
    "PASS",
    PRIOR + "round-4 evidence (check_pages PASS and full read) and check_pages M2 PASS re-run this round.")

row("STRUCT-L09", "2.9 structure: template sections, tiers, quiz 8-15, key-results table, lesson nav",
    "course/modules/M/M2/L09.html",
    "PASS",
    PRIOR + "round-4 evidence (check_pages PASS and full read) and check_pages M2 PASS re-run this round.")

row("STRUCT-L10", "2.9 structure: template sections, tiers, quiz 8-15, key-results table, lesson nav",
    "course/modules/M/M2/L10.html",
    "PASS",
    "Read in full this round: why-it-matters, sections 1-5, misconceptions 1-3, problem set M1-M3, P1-P3, E1-E3, R1-R3 each with a solution, key-results table (5 rows; see KR-L10), quiz with 10 items, references, nav links (L09, L11). " + G + "g01_check_pages_M2.out PASS.")

row("STRUCT-L11", "2.9 structure: template sections, tiers, quiz 8-15, key-results table, lesson nav",
    "course/modules/M/M2/L11.html",
    "PASS",
    PRIOR + "round-4 evidence (check_pages PASS and full read) and check_pages M2 PASS re-run this round.")

row("STRUCT-L12", "2.9 structure: template sections, tiers, quiz 8-15, key-results table, lesson nav",
    "course/modules/M/M2/L12.html",
    "PASS",
    PRIOR + "round-4 evidence (check_pages PASS and full read) and check_pages M2 PASS re-run this round.")

row("NUM-L07", "2.2 numbers: every number in prose, solutions, quiz and expected blocks recomputed",
    "course/modules/M/M2/L07.html (Example 1.5, 2.4, 3.3, Problems M1-M3, E1-E3, R2, quiz)",
    "PASS",
    G + "numbers_r5.py / " + G + "numbers_r5.out (exact fractions and floats): f(3/10)=10/7; P_1(3/10)=1.3; error 9/70; (3/10)^11/(7/10)=2.5306714e-6 -> 2.5307e-6 to 5 s.f.; f''(1/2)=16, f'''(1/2)=96; P_2(1/2)=7/4, error 1/4; ratio 0.3000000057613 (rel. diff 1.9e-8, 'about 2e-8'); E2 bounds 0.0013020833 (n=8) and 0.0006510417 (n=9); 2^19 < 10^6 <= 2^20; P_3(1/2) error 1/8; quiz 9/70 = 0.128571...; deg-10 error at x=2 is -2048. Lab expected numbers in part B and C match the formulas.")

row("NUM-L08", "2.2 numbers: every number in prose, solutions and expected blocks recomputed",
    "course/modules/M/M2/L08.html",
    "PASS",
    PRIOR + "round-4 evidence (numbers_b.py, g13_numbers_b.out) and the byte-identical page.")

row("NUM-L09", "2.2 numbers: every number in prose, solutions and expected blocks recomputed",
    "course/modules/M/M2/L09.html",
    "PASS",
    PRIOR + "round-4 evidence (numbers_b.py, g13_numbers_b.out). Card-level L09 numbers were recomputed this round in " + G + "numbers_r5.out and " + G + "c126_check_r5.out.")

row("NUM-L10", "2.2 numbers: every number in prose, solutions and expected blocks recomputed",
    "course/modules/M/M2/L10.html (Corollary 3.1 table row, Lab 1 table, Example 2.2, Example 3.2, Problems M1-M3, E1-E3)",
    "PASS",
    G + "numbers_r5.out: U_8=-0.8046875, L_8=-1.1796875, U_8-L_8=0.375=3/8; n=128 part B L=0.497079213, U=0.502938588, U-L=3/512=0.005859375; n=256 part A L=-1.00585175, U=-0.99413300; 1/(1.3)^2 = 0.59171598; F'''(0.3)=6/1.3^4=2.1008; h^2 F'''/6 = 3.50e-13; per-value rounding bound 5.0e-17 (ulp(0.3)/2, ulp(1.3)/2, ulp(0.23)/2 with the sensitivities 0.59, 0.18); difference over 2h = 5.0e-11; F(1)-F(0)=1/6 for x-x^2 (L09 check); G(1)=11/2; 1/2 = F(1)-F(0) for x/(1+x)+5.")

row("NUM-L11", "2.2 numbers: every number in prose, solutions and expected blocks recomputed",
    "course/modules/M/M2/L11.html",
    "PASS",
    PRIOR + "round-4 evidence (numbers_b.py, g13_numbers_b.out).")

row("NUM-L12", "2.2 numbers: every number in prose, solutions and expected blocks recomputed",
    "course/modules/M/M2/L12.html",
    "PASS",
    PRIOR + "round-4 evidence (numbers_b.py, g13_numbers_b.out).")

row("MATH-L07", "2.4 mathematics: every statement, proof, hypothesis, derivation and worked solution",
    "course/modules/M/M2/L07.html (Prop 1.4, Lemma 1.6, Prop 2.3, Example 2.4, Lemma 3.1, Thm 3.2, Ex 3.3, Ex 4.1, Prop 4.2, Remark 4.3, Section 5, Misconceptions 1-3, Problems M1-M3, P1-P3, E1-E3, R1-R3)",
    "PASS",
    "Re-derived this round, line by line: Prop 1.4 induction (quotient rule, (k+1)!/(1-x)^(k+2)); Lemma 1.6 induction ((1-x^(n+1)) + (1-x)x^(n+1) = 1-x^(n+2)); Prop 2.3 ((1-x^(n+1))/(1-x) subtraction); Lemma 3.1 Bernoulli bound 1/(1+mh); Thm 3.2; Ex 3.3 ratio x; Ex 4.1 g' = 2|x| with g'(0)=0 from the quotient |h|; Prop 4.2 one-sided quotients +2/-2 and Prop 2.2 of Lesson 3 (two-sided limit needs both one-sided limits, L03.html:95); Remark 4.3 P_1 = 0; canon-breaks |x|>=1 bound 1/|1-x|; Misconception 2 coefficient f''(0)/2! = 1; problems M1 (2, 6, 16, 96), M2 (P_3 = g), M3 (1/4), P1 (quotient), P2 (induction), P3 (power derivative), E1 (ratio 0.30000000576), E2 (n=9), E3 (signs), R1 (u = 2x-1 expansion), R2 (2^20), R3 (P_1 = 0). L01 Problem M3 (c_n -> 0) confirms the 1/m -> 0 citation (L01.html:240-245).")

row("MATH-L08", "2.4 mathematics: every statement, proof, hypothesis, derivation and worked solution",
    "course/modules/M/M2/L08.html",
    "PASS",
    PRIOR + "round-4 evidence (full re-derivation) and the byte-identical page.")

row("MATH-L09", "2.4 mathematics: every statement, proof, hypothesis, derivation and worked solution",
    "course/modules/M/M2/L09.html",
    "PASS",
    PRIOR + "round-4 evidence (full re-derivation). This round the cross-lesson premises used by Misconception 2 were re-read: Lesson 10 Theorem 2.1 with F = x^2/2 - x^3/3 (F(1)-F(0)=1/6) and Lesson 11 Lemma 1.1 (linearity: finite combinations integrable, L11.html:78) are present.")

row("MATH-L10", "2.4 mathematics: statements, proofs and solutions of L10; quantifiers in statements",
    "course/modules/M/M2/L10.html:101-102 (Corollary 3.1), 385-388 (key-results row), proofs of Thm 1.2, 2.1, Prop 4.1",
    "PASS",
    "Fix verified. Corollary 3.1 now reads 'every integer k >= 0 and every 0 <= a <= b (for a = b, the left side is 0 by the convention of Lesson 9, Definition 1.3, and the right side is 0 by subtraction)'. L09.html:86 states the convention int_a^a f = 0 in Definition 1.3, so the parenthetical is correct. The proof covers a < b through Theorem 2.1 and the monotone integrability (Lesson 9 Thm 2.2) and a = b by the convention. Re-derived this round: Thm 1.2 (MVT, Lesson 6 Theorem 2.3, L06.html:87), Thm 2.1 (telescoping, sandwich, I_* = I^*), Example 2.2, Example 3.2, Prop 4.1, Misconceptions 1-3, Problems M1 (4), M2 (26/3), M3 (1/6), P1-P3, E1-E3 (error budget recomputed), R1 (two-sided bound), R2, R3. The sentence 'The function f need not be continuous' after Theorem 2.1 is true (Volterra-type example) and is not a graded claim; see notes.")

row("MATH-L11", "2.4 mathematics: every statement, proof, hypothesis, derivation and worked solution",
    "course/modules/M/M2/L11.html",
    "PASS",
    PRIOR + "round-4 evidence (full re-derivation) and the byte-identical page.")

row("MATH-L12", "2.4 mathematics: every statement, proof, hypothesis, derivation and worked solution",
    "course/modules/M/M2/L12.html",
    "PASS",
    PRIOR + "round-4 evidence (full re-derivation) and the byte-identical page.")

row("GRADE-L07-L12", "2.3 grades: every claim span graded T with its proof on the page; examples and remarks ungraded",
    "course/modules/M/M2/L07.html..L12.html (data-grade spans, key-results tables)",
    "PASS",
    "Re-checked this round for the changed pages. L07 T spans Prop 1.4, Lemma 1.6, Prop 2.3, Lemma 3.1, Thm 3.2, Prop 4.2 each have a proof on the page. L10 T spans Thm 1.2 (precise cite: Lesson 6 Theorem 2.3, MVT), Thm 2.1, Cor 3.1 (proof on the page; a=b by convention), Prop 4.1, and the key-results rows, which match. L08, L09, L11, L12 pages and the carried rows are byte-identical (carry_identity_r5.out).")

row("CARD-L07", "2.7 cards of L07 (24 cards: c075-c096, c395, c422): content vs lesson, numbers, grade and basis",
    "course/modules/M/M2/cards.json (M2-c085 at lines ~591-596; M2-c422 appended); other L07 cards read in full",
    "PASS",
    "All 24 L07 cards read against L07.html and dumped in " + G + "cards_L07_L10_full_dump.txt. Fix verified: M2-c085 is now T and states the value derived in Example 2.4 (x^11/(1-x) = (3/10)^11/(7/10) = 2.5307e-6 to five significant figures; recomputed in " + G + "numbers_r5.out). "
    "M2-c422 (C, basis 'Lab 1, part B (printed decimals)') states the printed 0.0000025307 at n = 10, which is in the expected block of the page. The C cards c086, c092, c093 are lab-scoped and match the printed output (-2048; +2/-2; 27 checks). "
    "Judged not a defect: c085 (T) and c422 (C) give the same value under the split the round-4 fix suggested; front texts differ. No card contradicts L07.html.")

row("CARD-L08", "2.7 cards of L08 (19 cards: c097..c114, c417): content vs lesson, numbers, grade and basis",
    "course/modules/M/M2/cards.json (M2-c097..c114, M2-c417)",
    "PASS",
    PRIOR + "round-4 evidence (all cards read) and per-card object identity (" + G + "card_identity_r5.out: L08 total 19, identical 19).")

row("CARD-L09", "2.7 cards of L09 (19 cards: c115-c132, c423): content vs lesson, numbers, grades, forward reference",
    "course/modules/M/M2/cards.json:905-914 (M2-c129), M2-c423 (appended); L09.html:280 (Misconception 2)",
    "PASS",
    "All 19 L09 cards read against L09.html and dumped in " + G + "cards_L09_full_dump.txt. Fix verified: M2-c129 is now T and states only the endpoint sums, which are computed on the page (left (0+1/4)/2 = 1/8, right (1/4+0)/2 = 1/8; recomputed exactly). "
    "New M2-c423 is C with basis 'Lesson 10, Theorem 2.1 (forward reference; not derived in Lesson 9)' and states 'both lie below 1/6' with the forward reference marked as not derived in Lesson 9; this matches L09.html:280 and L09.html:479. "
    "Numbers on the cards recomputed: U_128 = 0.337249756 (c125/c128), L_128 = 0.329437256 (c125), U-L = 0.159334 printed as 0.15933400 (c126, " + G + "c126_check_r5.out), mesh 0.19, midpoint n=8 error -0.00130208 (c127), U_n-1/3 = (3n+1)/(6n^2) (c128), 1/3-L_n = (3n-1)/(6n^2) (c131). Quiz q8 unchanged.")

row("CARD-L10", "2.7 cards of L10 (16 cards: c133-c147 (c144 absent), c418, c421): content vs lesson, grades",
    "course/modules/M/M2/cards.json:960-961 (M2-c137)",
    "PASS",
    "All 16 L10 cards read against L10.html and dumped in " + G + "cards_L07_L10_full_dump.txt. Fix verified: M2-c137 now says '0 <= a <= b (for a = b both sides are 0 by the convention of Lesson 9, Definition 1.3)', the same wording as Corollary 3.1. c139-c141 are lab-scoped C and match the printed output (n=256 L -1.00585175, U -0.99413300; part B 3/(4n); central difference 0.59171598). c134, c135, c142, c143, c145-c147, c418 match the page.")

row("CARD-L11", "2.7 cards of L11 (16 cards: c148-c163): content vs lesson, numbers, grade and basis",
    "course/modules/M/M2/cards.json (M2-c148..c163)",
    "PASS",
    PRIOR + "round-4 evidence (all cards read) and per-card object identity (" + G + "card_identity_r5.out: L11 total 16, identical 16).")

row("CARD-L12", "2.7 cards of L12 (17 cards: c165-c180, c398): content vs lesson, numbers, grade and basis",
    "course/modules/M/M2/cards.json (M2-c165..c180, M2-c398)",
    "PASS",
    PRIOR + "round-4 evidence (all cards read) and per-card object identity (" + G + "card_identity_r5.out: L12 total 17, identical 17).")

row("CARD-DUP", "2.7 full scan for duplicate card ids and fronts across the whole deck",
    "course/modules/M/M2/cards.json (all 396 cards)",
    "PASS",
    G + "cards_r5_checks.out: cards old 394, new 396; 'dup ids in new: []'; 'dup fronts in new: []' (fronts compared stripped and lower-cased); added M2-c422 (L07) and M2-c423 (L09); removed none; changed M2-c009, c048, c068, c085, c129, c137, c293.")

row("DAG-L07-L12", "2.9 DAG: concepts used before defined, defined twice, or used outside the prerequisite closure",
    "course/modules/M/M2/L07.html..L12.html",
    "PASS",
    G + "g02_check_dag_M2.out: 'check_dag M2: PASS'. Manual read of the changed text in L07 (Lesson 13 pointer, Lesson 8 remark, Lesson 3 Prop 2.2) and L10 (Lesson 9 Definition 1.3, Lesson 6 Theorem 2.3, Lesson 7 Example 1.3): no concept is used by name before its definition.")

row("XREF-L07-L12", "2.9 internal cross-references (lesson, proposition, example, problem numbers) resolve to the stated result",
    "course/modules/M/M2/L07.html and L10.html changed sentences; L09 and L11 cards",
    "PASS",
    "Checked this round: L06 Theorem 2.3 is the mean value theorem (L06.html:87); L06 Assumption 2.1 is the extreme value theorem (L06.html:72-83); L09 Definition 1.3 with the convention int_a^a f = 0 (L09.html:86); L09 Theorem 2.2 monotone integrands (L09.html:99); L03 Proposition 2.2 two-sided limit needs both one-sided limits (L03.html:95); L01 Problem M3 c_n -> 0 (L01.html:240-245); L08 Theorem 2.1 requires derivatives up to order n+1 on an open interval (card c100 and L08 page); L13 'Finite-Difference Derivative Approximation' (index.html:156); L10 Section 2 is the evaluation form (card c421); L07 Example 1.3 is the polynomial power rule (L07.html, Example 1.3, line 69).")

row("NOT-L09-R", "2.4/notation: symbols introduced in L09 (R, P, Q, S, M_i, m_i, I_*, I^*) vs notation/notation.json",
    "course/modules/M/M2/L09.html Section 1",
    "PASS",
    PRIOR + "round-4 evidence. notation/notation.json is byte-identical; its registered symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q}) belong to modules AP1, M4, S1 and are not used in L09 (plain Q, the partition, is not \\mathbb{Q}).")

row("NOT-GLOBAL", "2.4/notation: every symbol in L07..L12 math vs notation/notation.json",
    "course/modules/M/M2/L07.html..L12.html math",
    "PASS",
    G + "Macro tally of all \\(...\\) and \\[...\\] blocks: only \\R (registered) and standard KaTeX commands; \\mathbb is not used. notation.json has no M2 entries (modules AP1, M4, S1 only). Registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q} do not occur in slice math (plain Q as a partition in L09 is not the registered \\mathbb{Q}). The changed L07/L10 text introduces no new symbol.")

row("PROSE-BANNED", "2.9 banned phrases (BUILDER_RULES 1.3-1.4) in visible prose and cards",
    "course/modules/M/M2/L07.html..L12.html; course/modules/M/M2/cards.json (slice cards)",
    "PASS",
    "Regex scan this round for for brevity, beyond the scope, details omitted, clearly, obviously, well known, can be shown, it is important, studies show, experts agree, TODO, TBD, lorem, left as an exercise, you can add, and ellipses: no hits in the six pages. Full-deck card scan: no slice card hit (hits in other lessons are the math adjective 'fixed').")

row("PROSE-PROCESS", "2.9/rule 12 process words in learner text",
    "course/modules/M/M2/L07.html..L12.html; slice cards",
    "PASS",
    "Regex scan this round for verifier, builder, round N, corrected, fixed, revised: no hits in the six pages or in the slice cards.")

row("HOURS-L07-L12", "2.9 hours: each lesson's declared hours and the hub split",
    "course/modules/M/M2/L07.html..L12.html eyebrow and data-hours; course/modules/M/M2/index.html data-hours-lessons, data-hours-project",
    "PASS",
    "Every M2 lesson has data-hours=10 (L01..L24). index.html has data-hours-lessons=240 (24 x 10) and data-hours-project=60; total 300; project 20% (within 10-40%). check_pages M2 PASS re-run this round.")

carried("LINK-L11-chain", "2.4 link chain of L11 (uses meta-row, Sections 2-3 dependencies)", "course/modules/M/M2/L11.html:38 and Sections 2-3",
        ["L11"], "round-4 evidence for the chain check.")

carried("PROOF-L11-hyp", "2.4 hypotheses of L11 proofs", "course/modules/M/M2/L11.html:83-124", ["L11"], "round-4 evidence for the hypothesis check.")

carried("PROOF-L12-integrability", "2.4 integrability hypotheses in L12 proofs", "course/modules/M/M2/L12.html:81-92 and 217-220", ["L12"], "round-4 evidence for the integrability check.")

row("QUIZ-L07-L12", "2.9 retrieval quiz: item count 8-15, answers and explanations match the lesson, numeric answers within tolerance",
    "course/modules/M/M2/L07.html and L10.html quiz sections; L08, L09, L11, L12 quizzes carried",
    "PASS",
    "L07 quiz: 9 items. Keys rechecked: third derivative 6/(1-x)^4 (Prop 1.4, k = 3); f''(0) = 2; degree-2 polynomial 1 + x + x^2; error of degree 1 at x = 3/10 is 9/70 = 0.128571 (tolerance 1e-6: difference 4.3e-7); g statement; error of degree 3 at x = 1/2 is 1/8; smallest degree 20 for 10^-6 (2^19 < 10^6 <= 2^20). L10 quiz: 10 items. Keys rechecked: F(2)-F(0) = 4; 1/2 for the integral of 1/(1+x)^2; 26/3 for Corollary 3.1 at (1,3); U_8 - L_8 = 0.375; F(1)-F(0) = 1/2 for x/(1+x)+5 (constant cancels). Explanations cite the correct Proposition, Example, Problem or Misconception. L08, L09, L11, L12 quizzes: carried, byte-identical pages.")

row("MUTANTS-NA", "2.6/2.5 mutation testing: applies to project graders only",
    "ledgers/M2/mutants/ (none for this slice)",
    "PASS",
    "Slice b has no project grader; lab twins are demonstrations (VERIFIER_RULES 2.5, architect ruling on mutants). No mutant rows.")

row("KR-L10", "2.4 key-results row 5 (bracket of 3x^2-2 for every partition), source precision",
    "course/modules/M/M2/L10.html:390 (key-results row 5, source cell 'Problem L10-R3; Lab 1, part A (exact fractions)')",
    "FAIL",
    "The row is graded T and the claim is true, but its source cell does not cite the proof of the bracket for every n. Problem L10-R3 (L10.html problem R3) proves only U_n - L_n <= 3/n and equality, not the bracket. Lab 1 part A checks the bracket at nine sampled n. The bracket for every partition is proved on the page by Problem L10-P2 (the sandwich, L10.html problem P2) and by the proof of Theorem 2.1. LOW (citation precision; the grade is correct).",
    "Change the source cell of key-results row 5 to 'Theorem 2.1 proof; Problem L10-P2; Problem L10-R3 (U_n - L_n); Lab 1, part A (exact fractions, sampled n)'. Then re-run check_pages --unit M2 and run_labs --unit M2 (both affected only by the page text). Under ruling 26 this is a LOW row that may be fixed or listed in plans/KNOWN-ISSUES.md.")

# Carried rows: the round-4 PASS evidence is quoted verbatim, under the carry prefix (subject byte-identical since edbb7aa8).
CARRIED_IDS = [
    "LAB-L08", "LAB-L09", "LAB-L11", "LAB-L12",
    "STRUCT-L08", "STRUCT-L09", "STRUCT-L11", "STRUCT-L12",
    "NUM-L08", "NUM-L09", "NUM-L11", "NUM-L12",
    "MATH-L08", "MATH-L09", "MATH-L11", "MATH-L12",
    "CARD-L08", "CARD-L11", "CARD-L12", "NOT-L09-R",
    "LINK-L11-chain", "PROOF-L11-hyp", "PROOF-L12-integrability",
]
with open("/Users/billyribeiro/.fanout/frags/S-M2-b.round4.json", encoding="utf-8") as fh:
    round4 = {r["id"]: r for r in json.load(fh)["rows"]}
by_id = {r["id"]: r for r in rows}
for rid in CARRIED_IDS:
    assert round4[rid]["status"] == "PASS", rid
    by_id[rid]["evidence"] = (
        "Carried from round 4 (" + by_id[rid]["location"] + " byte-identical since the previous pin edbb7aa8; "
        "identity in ledgers/M2/scripts/M2-b-r5/carry_identity_r5.out and card_identity_r5.out): " + round4[rid]["evidence"]
    )
    by_id[rid]["status"] = "PASS"

counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

fragment = {
    "unit": "M2",
    "slice": "b",
    "round": 5,
    "verifier": "independent Haiku verifier, M2 slice b (L07-L12, lab twins and cards), round 5 (delta verification from pin edbb7aa8); fresh context, no builder context",
    "pin": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
    "base": "edbb7aa8de20e6d2f3035c463a79a318c22623c4 (round-4 pin; round-4 fragment /Users/billyribeiro/.fanout/frags/S-M2-b.round4.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS5-M2-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyS5-M2-b/ledgers/M2/scripts/M2-b-r5",
    "verified_at": now,
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta verification (Round 5). Slice paths changed since edbb7aa8: course/modules/M/M2/L07.html, L10.html, cards.json (slice cards M2-c085, c129, c137 changed; M2-c422, c423 added), tests/labs/M2/lab-M2-L07-1.py. L08, L09, L11, L12 pages and their twins, notation/notation.json, references/references.json, BUILDER_RULES.md, VERIFIER_RULES.md and the tools are byte-identical (carry_identity_r5.out). Rows for those files are carried with the round-4 prefix; rows whose subject changed were re-verified from scratch.",
        "Round-4 non-PASS rows, all re-verified: LAB-L07-DOC (fixed: helper renamed g_prime_formula), MATH-L10 (fixed: Corollary 3.1 now 0 <= a <= b), CARD-L07 (fixed: M2-c085 is T with the Example 2.4 value; printed-output claim split to M2-c422 as C), CARD-L09 (fixed: M2-c129 is T for the endpoint sums only; the forward-referenced 1/6 is in M2-c423, C), CARD-L10 (fixed: M2-c137 matches the corrected corollary). Round-4 PASS rows CARD-L08, CARD-L10 duplicate check and CARD-DUP were re-run on the full deck (396 cards, no duplicate id or front).",
        "Open LOW row this round: KR-L10 (key-results row 5 source omits Problem L10-P2 for the bracket). Blocking rows: none (ruling 26 classes: false or unproved statement, missing hypothesis, wrong number, over-grade, failing gate, surviving non-equivalent mutant, lab statement the code does not support). Verdict FAIL follows the verifier-rules rule that every row must be PASS; under ruling 26 the slice is accepted once KR-L10 is fixed or listed in plans/KNOWN-ISSUES.md.",
        "Judged not rows: (a) M2-c423 is C with the forward-reference basis, the grade the round-4 fix asked for; the endpoint sums in it are T by direct computation, so C is conservative and not an over-grade. (b) M2-c085 (T) and M2-c422 (C) state the same value under different grades, the split the round-4 fix suggested; the fronts differ and neither contradicts the page. (c) L10 Theorem 2.1 says 'The function f need not be continuous.' This is true (a Volterra-type example: a differentiable F on [a,b] with bounded, discontinuous F') but the page gives no example or citation; it is a remark, not a graded claim, and is noted only. (d) Lab-scoped C cards: M2-c086, c092, c093 (L07), c125-c127 (L09), c139-c141 (L10) were re-read this round against the printed output and match it; M2-c105-c107 (L08), c156-c158 (L11) and c170-c172 (L12) are carried with CARD-L08, CARD-L11 and CARD-L12 by object identity.",
        "Out of slice, read and not graded here: M2-c009 (L01), c048 (L04), c068 (L06), c293 (L19) card changes; L02, L03, L05, L06 page hunks; index.html and project.html hunks (hours unchanged; placement and rung-2 wording). Also plans/FINAL-ARCHITECT-RULINGS.md rulings 27-29 (E3 only) and plans/KNOWN-ISSUES.md (E3 only).",
        "Not checked: no screenshot was taken (the slice pages have no figures; page_smoke swept the text overflow and console checks). The live verify_refs run covers the registry for M2 (2 of 560 entries touched by the unit), not every registry key. The directory ledgers/M2/scripts/M2-b-r5 already held tracked files from earlier work at the pin; this round's files are the untracked ones named g*.out, cards_r5_checks.*, numbers_r5.*, c126_check_r5.*, carry_identity_r5.*, card_identity_r5.out, delta_*.diff, run_gates_r5.sh, run_r5_commands.sh, build_fragment_b_r5.py and twin_*.std*. Nothing was committed or pushed.",
    ],
    "summary": "M2-b round 5 on pin dde0486b (delta from edbb7aa8): %d rows; PASS %d; FAIL %d (blocking 0; LOW 1: KR-L10). All five round-4 non-PASS rows are fixed and re-verified. Gates re-run this round: check_pages, check_dag, check_projects, run_labs 27/27, check_pages/dag/projects --all, twins isolated under python -I -W error, page_smoke L07-L12 PASS, ruff, mypy strict, pytest subset, verify_refs offline and live M2 (all PASS)." % (len(rows), counts.get("PASS", 0), counts.get("FAIL", 0)),
}

out = sys.argv[1]
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), counts, verdict)
