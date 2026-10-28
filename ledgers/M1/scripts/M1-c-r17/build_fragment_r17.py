"""Build the round-17 fragment for M1 slice c (L06, L07, L08) from the verifier's observed results."""

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(sys.argv[1])
PIN = "fefbf8b"
CARRY_NOTE = "Carried from round 16 (course/modules/M/M1/L06.html, L07.html, L08.html and tests/labs/M1 byte-identical since the previous pin 00745fe): "

ALL_CARDS = (
    "all 66 M1 cards with lesson L06 (12), L07 (24) and L08 (30) read against the current lesson text: "
    "M1-c093..c103, c098/c100 (rewritten), c104 (rewritten), c108 (rewritten), c109..c117, c118/c119/c121/c122/c123/c124 (rewritten), "
    "c120, c125..c129, c130 (rewritten), c131, c132 (rewritten), c133..c143 (c134, c135, c136, c138, c141, c142, c143 rewritten), c146 (rewritten), "
    "new c153..c158, c164..c169, c178, c179"
)

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


row("M1c-cmd-check-pages", "tools/check_pages.py --unit M1", "tools/check_pages.py | tools/check_pages.py --unit M1", "PASS",
    "Run this round: 'check_pages M1: PASS', exit 0 (ledgers/M1/scripts/M1-c-r17/out/check_pages.out).")
row("M1c-cmd-check-dag", "tools/check_dag.py --all", "tools/check_dag.py --all", "PASS",
    "Run this round: check_dag M1, S7, AC1, AC2, AC4, CF1, AP1 all PASS, exit 0 (out/check_dag.out).")
row("M1c-cmd-run-labs", "tools/run_labs.py --unit M1", "tools/run_labs.py --unit M1", "PASS",
    "Run this round: 'run_labs M1: PASS (11/11)', exit 0 (out/run_labs.out).")
row("M1c-cmd-page-smoke", "tools/page_smoke.py --unit M1 --pages L06 L07 L08", "tools/page_smoke.py --unit M1 --pages L06 L07 L08", "PASS",
    "Run this round: page_smoke PASS for modules/M/M1/L06, L07 and L08; exit 0; lab times 0.0 to 0.1 s, runtime boot 1.1 to 1.2 s (out/smoke.out). No live Pyodide browser run was made.")
row("M1c-cmd-twins-isolated", "Each twin under python -I -W error", "tests/labs/M1/lab-M1-L06-1.py, lab-M1-L07-1.py, lab-M1-L08-1.py", "PASS",
    "Run this round: exit 0 for all three; stdout saved as out/lab06.out, lab07.out, lab08.out (lab06 six lines, lab07 sixteen, lab08 eighteen).")
row("M1c-twin-embed", "Page code and expected output equal the twins and the lab stdout", "course/modules/M/M1/L06.html:132-203, 204-209; L07.html:198-312, 313-328; L08.html:151-312, 313-330", "PASS",
    "scripts/M1-c-r17/embed_check.py (out/embed_check.out): code equals twin after one trailing newline (embedding drops the final newline: 2540 vs 2541, 4842 vs 4843, 7401 vs 7402 characters); expected block equals stdout for L06, L07, L08.")
row("M1c-lint-types", "ruff, ruff format, mypy --strict style check and M1 pytest", "tests/labs/M1; course/modules/M/M1", "PASS",
    "ruff check: All checks passed; ruff format --check tests/labs/M1: 11 files already formatted; mypy --no-incremental tests/labs/M1: Success, no issues in 11 files; pytest -k M1: 12 passed (includes the curriculum test and tests/labs M1 L06-L08 twins) (out/lint.out, out/pytest_M1_summary.out).")
row("M1c-refs-live", "tools/verify_refs.py --unit M1 (live) and --offline", "references/references.json (M1 entries)", "PASS",
    "Run this round: live 'live re-verification of M1: 1 of 560 entries, 0 problems' (out/vr_live_M1.out); offline 'integrity: 560 entries, 0 problems' (out/vr_offline.out). L06 to L08 cite no registry key, so no slice entry is checked against a paper.")
row("M1c-citations-none", "No registry citation in L06 to L08", "course/modules/M/M1/L06.html:446, L07.html:556, L08.html:563", "PASS",
    "Each page's <ol data-references></ol> is empty and the learner text names no paper, standard or source. Re-read this round in full.")
row("L06-lab-1", "Lab 1 of L06: code, output and interpretation", "course/modules/M/M1/L06.html:130-211; tests/labs/M1/lab-M1-L06-1.py", "PASS",
    "Re-read in full. 7 ratios x n=1..60 = 420 checks (verified by running the twin); q=1/2,n=3: 7/4; q=-1,n=10: 0; float relative errors 8.048e-16 (q=1.001) and 1.059e-10 (q=1+1e-9) reproduced by scripts/M1-c-r17/recompute_r17.py. The interpretation (line 210) says 'accurate to about' and gives the same values; it disclaims proving the theorem and the general error bound.")
row("L06-canon-breaks", "L06 'Where the canon breaks' bullets", "course/modules/M/M1/L06.html:217-219", "PASS",
    "Bullet 3 cancellation claim is shown by Lab 1 at q=1+1e-9 (1.059e-10). Bullet 4 (Lesson 7 uses a finite formula and an explicit remainder, not an infinite geometric sum) matches L07 Proposition 2.3 and Theorem 2.4. Bullet 2 matches Theorem 1.2 and its proof for the integers.")
row("L06-numbers", "Numbers in L06 prose", "course/modules/M/M1/L06.html:52, 228, 308, 130-211, 301, 315", "PASS",
    "Recomputed: n^2+n+41 prime for n=0..39 (trial division, scripts/M1-c-r17/recompute_r17.py), 40^2+40+41=1681=41^2; E2: q^60 about 1+6e-8, numerator about -6e-8, estimate 1.67e-9 (1e-16/6e-8); at q=1.001 numerator -0.0618, estimate 1.62e-15 (1e-16/0.0618), 'a factor of two' against the observed 8.0e-16 is consistent with the stated estimate; E1 ZeroDivisionError for float 0.0 division; E3 = 1023.")
row("L06-theorem-math", "Definition 1.1, Theorem 1.2, Example 1.3, Remark 1.4, Definition 2.1, Theorem 2.2, Corollary 2.3, Example 2.4", "course/modules/M/M1/L06.html:56-127", "PASS",
    "Re-derived each proof: well-ordering argument (line 70), Example 1.3 algebra (78), Remark 1.4 (84), Theorem 2.2 inductive step (107-108: 1-q^k+q^k(1-q)=1-q^{k+1}), Example 2.4 15/8 both ways.")
row("L06-E-problems", "Problem set (M, P, E, R tiers) with worked solutions", "course/modules/M/M1/L06.html:247-343", "PASS",
    "M1 121 and M2 124 and M3 n=5 (2(1-2^-4)=1.875, 2(1-2^-5)=1.9375) recomputed; P1, P2, P3 and R1 (2k^2+7k+6=(k+2)(2k+3)) re-derived; E2 solution (line 308) checked in L06-numbers; R3 (S_n(-1) parity) checked.")
row("L06-grades", "Grades in the L06 blocks and the key-results table", "course/modules/M/M1/L06.html:63-127, 352-357", "PASS",
    "Theorems and corollaries are T and proved on the page; the lab results at lines 356-357 are C with basis 'Lab 1' (finite check, and floating point one run), consistent with the grade rule.")
row("L06-key-420-grade", "Key-results row: 420 checks graded C; card M1-c099", "course/modules/M/M1/L06.html:353, 356; cards.json M1-c099", "PASS",
    "Row 356 gives 420 checks and grade C with basis Lab 1; card M1-c099 gives 420 checks, 7 ratios, n 1 to 60 (matches the lab output).")
row("L06-structure", "L06 section order, why-it-matters line, retrieval quiz", "course/modules/M/M1/L06.html:52, 54-363", "PASS",
    "Sections 1 to 8 in template order; why-it-matters (line 52) names Lessons 7 and 8; quiz (363-442) has ten items with explanations, each explanation matches its item.")
row("L07-lab-1", "Lab 1 of L07: code, output and interpretation", "course/modules/M/M1/L07.html:195-330; tests/labs/M1/lab-M1-L07-1.py", "PASS",
    "Re-read in full. Output equal to lab stdout. 4 rates x 40 n = 160 pairs, 2 checks each = 320 (interpretation line 329 correct). Part B horizons 1, 5, 10, 50, 100, 200, 400 as printed; Part C refusal message at twin line 56 (the r > g refusal in growing_perpetuity_value) and g = r partial values 925.9259 and 9259.2593 recomputed.")
row("L07-def-2.1-scope", "Definition 2.1 and Definition 3.1 wording", "course/modules/M/M1/L07.html:106, 152", "PASS",
    "Definition 2.1 (value via tail bound |PV_m - V| <= eps for m >= M) matches Theorem 2.4 uniqueness proof and Theorem 3.3; Definition 3.1 gives g > -1, and the text after it gives q > 0 (line 155).")
row("L07-canon-spread-attribution", "L07 canon-breaks bullet 2: value sensitive to the spread", "course/modules/M/M1/L07.html:336", "PASS",
    "C/(0.04)=2500 and C/(0.05)=2000 with C=100; the fall 500/2500 = 20 per cent, stated from 2500 as basis.")
row("L07-canon-conditions-refusal", "L07 canon-breaks bullet 3: closed forms defined by conditions", "course/modules/M/M1/L07.html:337; tests/labs/M1/lab-M1-L07-1.py:22-23, 51-56", "PASS",
    "annuity_closed refuses r <= 0 (twin lines 22-23); growing_perpetuity_value refuses g <= -1 and r <= g (twin lines 51-56); Part C prints the refusal. Statement matches the code.")
row("L07-example-3.5-attribution", "Example 3.5 numbers", "course/modules/M/M1/L07.html:192", "PASS",
    "Recomputed: q = 1.03/1.08 = 0.953704, 100/1.08 = 92.5926, 2000(1-q^10) = 755.0134, 2000 q^10 = 1244.9866, 2000 = 100/0.05. Lab part B prints the same values.")
row("L07-theorem-math", "Theorem 1.2, Proposition 1.4, Lemma 2.2, Proposition 3.2, Proposition 2.3, Theorems 2.4, 3.3, 3.4", "course/modules/M/M1/L07.html:66-188", "PASS",
    "Each proof re-derived: 1-v = r/(1+r) and v/(1-v)=1/r (line 77); Bernoulli induction (116-118); gap C v^m/r (129); Theorem 2.4 choice of M; Theorem 3.3 d = (r-g)/(1+g), q^m <= 1/(1+md) (175-176); Theorem 3.4 bound PV_m >= mC/(1+r) (187).")
row("L07-R1-d-positive", "Problem R1 solution, d > 0", "course/modules/M/M1/L07.html:444", "PASS",
    "d = 1/q - 1 = (r-g)/(1+g) > 0 follows from g < r; the line states d > 0 comes from q < 1 (g < r). Consistent with Theorem 3.3.")
row("L07-E1-ln-digits", "Problem E1 solution: ln digits and N = 161", "course/modules/M/M1/L07.html:419", "PASS",
    "ln(1/q) = ln(1.08/1.03) = 0.0474022; ln 2000 / 0.0474022 = 160.349, so N = 161; recomputed gap at N=160 is 1.0167 (above 1) and at N=161 is 0.9696 (below 1). Lab column at N=200 (0.1527) is in the output.")
row("L07-numbers", "Numbers in L07 prose (Examples 1.3, 1.5, 2.5, 3.5, canon bullet 2, misconceptions, problems)", "course/modules/M/M1/L07.html:82, 97, 145, 192, 336, 346, 354, 369, 376, 383, 408, 426, 433, 458", "PASS",
    "Recomputed: 248.6852 (closed form and direct sum), 273.5537 and 24.8685 (line 97), 772.1735 and 1227.8265 (Example 2.5), M1 842.4728, M2 1250, M3 1666.6667 and 1833.3333, P3 m=39,980 (bound) and m=155.8 so m=156, E2 1537.2451 and 942.6914, R3 2160; misconception 3 2100 vs 2000.")
row("L07-grades", "Grade titles and key-results table in L07", "course/modules/M/M1/L07.html:58-190, 470-476", "PASS",
    "Theorems T and proved; key-results row 476 (seven horizons) graded C with basis Lab 1 part B (floating point, one run).")
row("L07-structure", "L07 section order and why-it-matters", "course/modules/M/M1/L07.html:52, 54-552", "PASS",
    "Sections 1 to 9 in template order; why-it-matters names the closed forms and conditions, consistent with the lesson.")
row("L08-lab-1-hypothesis", "Lab 1 hypothesis (stated before running)", "course/modules/M/M1/L08.html:150; tests/labs/M1/lab-M1-L08-1.py", "PASS",
    "Every prediction is borne out by the output: exact payment 1,498.88 (1498.876313), first interest 1,250.00, drift 27 cents ('well under one CU'), first 1-CU month 183 (before the final month).")
row("L08-lab-1-interpretation", "Lab 1 interpretation paragraph (line 331)", "course/modules/M/M1/L08.html:331; tests/labs/M1/lab-M1-L08-1.py part B", "PASS",
    "Re-run: 27 cents (rounded comparison), 3.41 CU at month 359 (unrounded, first 1 CU at 183), month 360 exact-rounded balance -3.7038 CU, identity month 105 only; 'the only source of difference' (line 331) is the interest rounding: recursion D_k=(1+i)D_{k-1}+rounding error, verified by derivation; the 0.5-cent reference rounding is the lab convention, stated.")
row("L08-R3-drift-identification", "R3 solution: 0.27 CU is the difference of the two printed final payments; decomposition 3.70", "course/modules/M/M1/L08.html:460", "PASS",
    "1498.88 - 1495.18 = 3.70; 1495.45 - 1495.18 = 0.27; 3.70 - 0.27 = 3.43 = 1498.88 - 1495.45; -0.003687118 x 1004.5150425 = -3.7038; 0.27 is the interest-rounding effect because both comparators pay the same cent regular payment (lab line 294-297 vs 298).")
row("L08-identity-count-claim", "Section 4 identity-count claim: 1 of 358 months (month 105)", "course/modules/M/M1/L08.html:338; lab output line 323", "PASS",
    "Re-run: identity holds only at month 105 among months 2..359 (358 months): 357 fail. Matches output 'in 1 of the 358 months ... at months [105]'.")
row("L08-numbers", "Numbers in L08 prose: hypothesis, output table, interpretation, misconceptions, R3", "course/modules/M/M1/L08.html:150, 280-331, 346-365, 368-380", "PASS",
    "Output table rows (months 1, 2, 3, 359, 360) recomputed exactly in integer cents: e.g. month 2 interest 124876 (1,248.76), principal 25012 (250.12), closing 24950100; month 359 closing 148801 (1,488.01). Misconception 1 (248.88, 1,488.01) and effective rate 6.167781% recomputed.")
row("L08-math", "Proofs and problems: Prop 1.2, Prop 2.1, Cor 2.2, Prop 2.3, Prop 2.4, Prop 3.1, P2, R1, R2, R3", "course/modules/M/M1/L08.html:75, 90-125, 132, 380-455, 450-460", "PASS",
    "Re-derived: Prop 2.1 recursion (line 91-93), Cor 2.2 (103), Prop 2.3 (113), Prop 2.4 (123), Prop 3.1 (143); R1 expansion (446) = 1-(1+i)^-(n-k); P2 (403); R2: 1.005^360=6.0225752, factor 1004.5150, balance -5.0226, excess 1.80; R3 B_{n-1}=A/(1+i) (460).")
row("L07-card-c108-q-locator", "Card M1-c108 matches Definition 3.1", "course/modules/M/M1/cards.json M1-c108; course/modules/M/M1/L07.html:150-153", "PASS",
    "Card now reads: C(1+g)^(t-1) at each t >= 1 with g > -1 (Definition 3.1). The earlier wording about q is removed from the card and is stated at line 155. Matches the definition.")
row("L08-decomposition-claim", "Claim: the 0.27 is the interest-rounding part; the 3.70 is the rounding of the regular payment compounded", "course/modules/M/M1/L08.html:357, 460, 528", "PASS",
    "Re-run: the exact-interest variant (lab lines 294-297, cent regular payment) ends at 1,495.18 and the cent schedule at 1,495.45; both use the same regular payment, so the 0.27 difference is interest rounding alone. The 3.70 is (A - regular) x (1.005^360 - 1)/0.005 = -3.7038 CU at month 360 (R3). The decomposition is correct as stated; the quiz option L08q6 is the separate issue (row L08-q6-cause-scope).")
row("L08-key-results-drift", "Key-results row: cent schedule, 27 cents and 3.41 CU", "course/modules/M/M1/L08.html:478", "PASS",
    "Row lists 1,498.88 regular, 1,495.45 final, 27 cents (rounded comparison), 3.41 CU at month 359 (unrounded); each matches the lab output and the re-run.")
row("L08-card-c135", "Card M1-c135: 27 cents, with each exact balance rounded before comparison", "course/modules/M/M1/cards.json M1-c135; course/modules/M/M1/L08.html:331", "PASS",
    "Card now gives 27 cents with rounding before comparison (the second sentence about the cause was removed); matches Lab 1 part B and line 331.")
row("cards-L06-L08-scan", "All L06 to L08 cards against the current lesson text", "course/modules/M/M1/cards.json (lesson field L06, L07, L08)", "PASS",
    ALL_CARDS + ". Cards with a changed text since the previous pin were re-checked (see the changed list in the notes). Every card number appears in its lesson or its lab output.")
row("cards-duplicate-scan", "Near-duplicate scan of L06 to L08 cards", "course/modules/M/M1/cards.json", "PASS",
    "scripts/M1-c-r17/cards_scan.py (out/cards_scan.out): 179 cards, no duplicate id; 22 pairs above similarity 0.6 that involve a L06-L08 card. The top pairs (c118/c154 at N=1 and N=200; c100/c153 at q=1.001 and 1+1e-9; c138/c157 at month 1 and month 360) ask for different facts, so none is a duplicate.")
row("L08-grades", "Grade titles and key-results table in L08", "course/modules/M/M1/L08.html:58-130, 472-478", "PASS",
    "Proved propositions are T; Lab 1 part B figures are C with basis 'Lab 1, part B (one run; illustrative input)'; effective-rate row graded T as an arithmetic result.")
row("L08-structure", "L08 section order and why-it-matters", "course/modules/M/M1/L08.html:52, 54-575", "PASS",
    "Sections 1 to 9 in template order; the why-it-matters line says the illustrative loan is 'not a market quote', which the lab header repeats.")
row("L08-misc3-attribution", "Misconception 3 and its attributions", "course/modules/M/M1/L08.html:355-357", "PASS",
    "0.37 cents = 0.003687 CU per month, excess 3.7038 CU at month 360 (R3); 0.27 CU = 1,495.45 - 1,495.18 from interest rounding; 3.70 - 0.27 = 3.43. The statement that 0.27 is added back by interest rounding is correct (cent schedule and exact-interest variant share the cent regular payment).")
row("slice-banned-phrases", "Banned phrases and scope words in L06 to L08 learner text", "course/modules/M/M1/L06.html, L07.html, L08.html (tags stripped)", "PASS",
    "Scanned for roughly, historically, typically, usually, generally, essentially, clearly, obviously, half, most, only, every, all, same, never, always: no banned phrase. 'about' appears only with a shown figure (e.g. L06 line 210, L08 line 421 '1342.0541 ... about 157 CU'). Ellipses appear only as quiz-stem cloze (L06 lines 415, 424; L07 lines 487, 515; L08 lines 489, 499, 536).")
row("slice-process-words", "No process words in learner text", "course/modules/M/M1/L06.html, L07.html, L08.html (learner text)", "PASS",
    "Scan for build, builder, verifier, round, REQUEST, unit report: none in learner text ('rounded' only).")
row("slice-definitions-math", "Definitions and notation used before definition in L06 to L08", "course/modules/M/M1/L06.html Def 1.1, Def 2.1; L07.html Def 1.1, Def 2.1, Def 3.1, line 56 (v, CU); L08.html Def 1.1, line 56 (A, L, i)", "PASS",
    "Each concept is defined where first used: induction (L06 Def 1.1, used in line 52 only as the lesson topic), geometric series (Def 2.1), v and CU (L07 line 56), q (L07 line 155 before Prop 3.2), monthly rate i (L08 line 56), B_k and p_k (L08 Def 1.1). Terms from earlier lessons are linked (L05, L06, L07).")
row("slice-data-figures", "Data and figures in L06 to L08; lab twins", "course/modules/M/M1/L06.html, L07.html, L08.html; tests/labs/M1/lab-M1-L0{6,7,8}-1.py", "PASS",
    "No external data; the L08 loan is marked ILLUSTRATIVE INPUT, NOT DATA (L08.html:150, lab line 153); the labs are deterministic and use only the standard library and exact fractions.")
row("slice-hours", "Declared hours of L06 to L08 and the hub split", "course/modules/M/M1/L06.html:2, L07.html:2, L08.html:2 (data-hours=9); course/modules/M/M1/index.html:29, 39, 149, 151-158", "PASS",
    "Lesson data-hours: L01 8, L02 9, L03 9, L04 9, L05 8, L06 9, L07 9, L08 9; sum 70 equals data-hours-lessons=70 on the hub (index.html:29), and the hub text (line 149: Lessons 1 and 5 declare 8 hours, the other six declare 9) and card-grid labels (151-158) agree. Arithmetic consistent. Per architect ruling, pace is not judged.")
row("hub-lesson-text-L06-L08", "Hub paragraph and cards for L06 to L08 match the lessons", "course/modules/M/M1/index.html:149, 156-158", "PASS",
    "Titles and descriptions match L06 (Geometric Series and Proof by Induction), L07 (Annuities, Perpetuities and Growing Perpetuities; annuity, perpetuity, growing perpetuity, r > g), L08 (Loan Amortization Schedules; final-payment rule, interest plus principal = payment). 'Lessons 6 and 7 cover ... the closed forms of the payment streams' is supported by L07.")
row("quiz-answers-L06-L08", "Quiz numeric answers and explanations in L06 to L08", "L06.html:376, 390, 395, 409; L07.html:495, 509, 523, 537; L08.html:488, 493, 507, 530, 544", "PASS",
    "Recomputed: L06 63, 1.75, 117, 0; L07 842.47, 1250, 2000, 2160; L08 0.005, 888.49, 796.37, 6.17 (6.1678), 661.85. Every explanation's arithmetic checked against the lesson.")
row("L08-q6-cause-scope", "Quiz item L08q6 correct option gives one cause for the final-payment gap", "course/modules/M/M1/L08.html:525, 528", "FAIL",
    "The correct option says the last payment differs from the regular payment because the exact payment rounded to the cent is compounded and 'the final payment absorbs it'. That accounts for 3.70 CU only. The printed gap is 3.43 CU, and the page's own explanation (line 528) and misconception 3 (line 356) attribute the 0.27 CU difference to interest taken to the cent, which pushes the other way. The option is therefore a partial cause presented as the reason. No other option is a correct cause.",
    "Revise option L08q6 (line 525) to name both effects, for example: 'the regular payment is the exact payment taken to the cent, the difference compounds to 3.70 CU, and interest taken to the cent adds back 0.27 CU, so the final payment is 3.43 CU below the regular payment.' Keep the explanation at line 528.")

with (ROOT / "ledgers/M1/scripts/M1-c-r17/out/rows_check.txt").open("w", encoding="utf-8") as fh:
    fh.write(f"{len(rows)} rows\n")
    for r in rows:
        fh.write(f"{r['status']}\t{r['id']}\n")

fragment = {
    "unit": "M1",
    "slice": "M1-c",
    "round": 17,
    "verifier": "independent verifier round 17 (did not build M1; shares no context with the builders or earlier verifiers)",
    "pin": PIN,
    "base": "00745fe (the round-16 fragment's pin; the M1 slice paths changed at 00745fe..fefbf8b only in cards.json, the hub, and the labs/pages of L01 to L05, the grader and project, none of which are in this slice)",
    "previous_ledger": "/tmp/fanout-frags/M1-c.round16.json (context only; its PASS rows were not trusted and every row was re-checked or carried with the byte-identical rule)",
    "checkout": "/tmp/verify17-M1-c (detached at fefbf8b; .venv symlinked)",
    "scratch": "/tmp/m1-v/M1-c",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta computed with git diff. M1-c paths (course/modules/M/M1/L06.html, L07.html, L08.html, tests/labs/M1/lab-M1-L0{6,7,8}-1.py) are byte-identical since 00745fe and since c093bf5 (the last commit touching M1 paths); fefbf8b and c5daab2 changed no M1 course or lab file. Changed in this slice's subject: cards.json (cards M1-c098, c100, c104, c108, c118, c119, c121, c122, c123, c124, c130, c132, c134, c135, c136, c138, c141, c142, c143, c146 rewritten; c153, c154, c155, c156, c157, c158, c164, c165, c166, c167, c168, c169, c178, c179 added), and the hub index.html (lines 60, 87, 149), which is not a slice page but is the source of the hours row. All changed cards were re-checked against the current lesson text.",
        "Rows carried from round 16 under the byte-identical rule: none. Every row was re-run or re-read this round, because the cards and the hub changed and the page reads were cheap enough to repeat. No row text relies on the earlier round's PASS.",
        "Mutants: not required. The slice is lessons and labs (not a project slice); the round-16 fragment also had no mutants. The project-slice mutant and alternative-implementation requirements do not apply.",
        "Alternative implementations: not run for the labs. The lab checks are fixed exact or floating-point comparisons with stated tolerances; the lab hypotheses and prose claims were checked against an independent recomputation (scripts/M1-c-r17/recompute_r17.py), not against alternative code.",
        "Not checked: no live Pyodide browser run (page_smoke only, with its own timing); the lab timing bar (10 s) is taken from page_smoke output; the grader and project (course/modules/M/M1/grader, project.html) are outside this slice; the hub's algebra prerequisite text (index.html lines 60-63, changed since 00745fe) belongs to another slice and was not checked here; Beneish/SEC rows are not in this slice; no external source is cited by these lessons.",
        "The L08q6 finding is the only FAIL row. It is a learner-facing cause statement that the page's own R3 and misconception 3 contradict as a complete reason. Fix as in the row.",
        "Lab twin embedding strips one trailing newline; the pages' code blocks equal the twins otherwise (embed_check.py output). This is a tooling convention, not a defect.",
    ],
    "summary": {},
}
counts = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": sum(r["status"] == "FAIL" for r in rows), "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows)}
fragment["summary"] = counts
(ROOT / "ledgers/M1/M1-c.json").write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(counts)
