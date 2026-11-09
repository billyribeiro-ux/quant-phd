"""Writes ledgers/CS2/CS2-c.json (round 3) from the rows the verifier established (CS2-c r3)."""
import json, sys
S = "ledgers/CS2/scripts/CS2-c-r3/"
rows = []
def row(i, check, loc, status, ev, fix=None):
    r = {"id": f"C-{i:02d}", "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

row(1, "2.9 structure: check_pages (unit and per page)", "L09.html, L10.html, L11.html, cards.json", "PASS",
    f"Re-run at pin 8196077d: .venv/bin/python tools/check_pages.py --unit CS2 -> 'check_pages CS2: PASS' exit 0; --page L09, L10, L11 each PASS exit 0 ({S}check_pages_unit.txt, check_pages_L09.txt, check_pages_L10.txt, check_pages_L11.txt).")
row(2, "2.9 DAG: check_dag and concept links", "L09.html:38,65; L10.html:38-39,67; L11.html:38-39,76", "PASS",
    f"Re-run: tools/check_dag.py --unit CS2 -> 'check_dag CS2: PASS' ({S}check_dag.txt). Links re-read: L09:38 mathematical-induction (concepts.html) and big-O (L01.html#def-big-o-complexity); L11:38 comparison-sorting and binary-search (L04.html#def-comparison-sorting, #def-binary-search), mathematical-induction. Each dfn id occurs once (L09:65, L10:67, L11:76).")
row(3, "2.5 labs: page code equals twin; expected block equals output", "L09.html:119-219; L10.html:118-212; L11.html:142-260", "PASS",
    f"{S}lab_page_vs_twin.py -> {S}lab_page_vs_twin.txt: for L09, L10, L11 'page code == twin (rstrip): True' and 'expected == twin stdout: True' (the page code is unescaped from the data-run block, the expected block from the class=expected block, the stdout from python -I -W error on the twin).")
row(4, "2.5 labs: twins alone under python -I -W error; run_labs", "tests/labs/CS2/lab-CS2-L09-1.py, lab-CS2-L10-1.py, lab-CS2-L11-1.py", "PASS",
    f"python -I -W error <twin>: exit 0 and empty stderr for each ({S}twin_L09.err, twin_L10.err, twin_L11.err are 0 bytes). tools/run_labs.py --unit CS2 --page L09|L10|L11 -> 'run_labs CS2: PASS (1/1)' each ({S}run_labs_L09.txt, run_labs_L10.txt, run_labs_L11.txt).")
row(5, "2.5/2.9 page_smoke (Chromium, Pyodide) on L09, L10, L11 alone", "L09.html, L10.html, L11.html", "PASS",
    f"tools/page_smoke.py --unit CS2 --pages L09 L10 L11 -> each page PASS and 'page_smoke CS2: PASS' exit 0 ({S}page_smoke_L09-L11.txt).")
row(6, "gate: ruff check and ruff format --check", "three twins; repository", "PASS",
    f"ruff check on the three twins 'All checks passed!' ({S}ruff_check.txt); ruff format --check '3 files already formatted' ({S}ruff_format.txt); repository ruff check 'All checks passed!' ({S}ruff_check_repo.txt) and format '553 files already formatted' ({S}ruff_format_repo.txt).")
row(7, "gate: mypy --no-incremental", "three twins; repository", "PASS",
    f"mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files' ({S}mypy_twins.txt); repository: 'Success: no issues found in 385 source files' ({S}mypy_repo.txt).")
row(8, "gate: relevant pytest", "tests/test_labs.py -k CS2; tests/test_figure_kernels.py, tests/test_docs_figures.py", "PASS",
    f"pytest tests/test_labs.py -k CS2 -> 14 tests, all passed, exit 0 ({S}pytest_labs_CS2.txt). pytest tests/test_figure_kernels.py tests/test_docs_figures.py -> 46 tests, all passed, exit 0 ({S}pytest_docs.txt).")
row(9, "2.1 citations: registry integrity and keys cited on the slice", "L09.html:446; L10.html:445; L11.html:495; references/references.json", "PASS",
    f"tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' exit 0 ({S}verify_refs_offline.txt). Each lesson states 'This lesson cites no registry key' and has an empty data-references list; grep finds no data-cite attribute in the three pages. A live run was not needed because the slice cites no key.")
row(10, "2.9 hours arithmetic: hub split against lesson hours", "course/modules/CS/CS2/index.html:143,153-155; L09/L10/L11 data-hours (line 2) and eyebrows (line 35)", "PASS",
    "data-hours L09=10, L10=8, L11=7 match the eyebrows and the hub cards 'L09 · 10 h', 'L10 · 8 h', 'L11 · 7 h' (index.html:153-155). The eleven hub rows 8+9+10+10+9+9+10+10+10+8+7 sum to 100, as index.html:143 states. The 8196077d lede edit on index.html:33 does not touch any hour figure.")
row(11, "2.5 lab L09: hypothesis and interpretation vs code and output", "L09.html:121, 218; tests/labs/CS2/lab-CS2-L09-1.py:1-84", "FAIL",
    f"Hypothesis (L09:121) matches the code and the output: offset 0 errors 9.258e-16, 2.819e-17, 7.286e-15 (all below 1e-14); two-pass most accurate at each offset; naive exactly 0.000000e+00 at 1e9; Welford error rises 9.26e-16 -> 8.85e-11 -> 7.45e-8 and stays below naive. Recomputed independently in {S}l09_numbers_r3.py / l09_numbers_r3.txt (exact sum of squares 2.0000000020427458e21, computed running sum differs by -3231910, math.ulp(2e21)=262144.0, (n-1)s^2 = 174.4749). Interpretation (L09:218) fails on one sentence: 'All values are the same 2000 values, which are the offset plus a seeded uniform draw.' The code is stream(offset) = [offset + rng.random()] (twin line 27; docstring lines 6-7), so the values differ across offsets (0, 1e6, 1e9 shift the same draws); only the 2000 draws are common.",
    "Replace 'All values are the same 2000 values, which are the offset plus a seeded uniform draw.' (L09.html:218) with 'All three offsets use the same 2000 seeded uniform draws, each shifted by its offset.'")
row(12, "2.5 lab L10: hypothesis and interpretation vs code and output", "L10.html:120, 211; tests/labs/CS2/lab-CS2-L10-1.py:62-85", "PASS",
    f"Hypothesis matches the code: the AssertionError lines (twin 72, 74, 76) check brute-force equality at every position and the deque size bound; the bound 2N is printed, not asserted. Interpretation: totals 396-399 (output); largest single-push removal count equals w for w=1,2,5 and is 6 for w=13 and 30; largest deque size 10 at w=30. Independent recomputation with a different implementation: {S}l10_numbers.py / l10_numbers.txt matches every printed value, and the page's worked examples M1, M2, M3 (8 <= 10), E1 (399 = 2n-1), E2 (5 removals), E3 (19), R2 (fronts 4,1,1) and R3 (n-w expiries) all re-derived.")
row(13, "2.5 lab L10: twin docstring states what the lab checks", "tests/labs/CS2/lab-CS2-L10-1.py:1-9", "PASS",
    "Docstring 'Claim checked' (twin lines 3-7) matches the main() code: rolling min and max equal brute force at every position, partial windows included, operations counted and 2N printed, largest single-push removals printed. No assertion of the operation bound, as the page says.")
row(14, "2.5 lab L11: hypothesis, claims in code, interpretation, expected block", "L11.html:144, 259-260; tests/labs/CS2/lab-CS2-L11-1.py:1-112", "PASS",
    f"Assertions at twin lines 91-92 and 99-100 are exactly the two Definition 1.2 inequalities with exact counts and the deficit-at-most-epsilon check. Printed values re-derived in {S}l11_numbers.txt and {S}l11_stream_independence.txt: stored 500 and 220, compactions 151 and 305 (per level 125, 20, 5, 1 for eps=1/20), excess 0.0212 and 0.0442, deficit 0, capacities 40/120/240 and 20/60/120. 'Lesson 4' for binary search matches L04.html's binary-search definition.")
row(15, "2.3/2.4 Lemma 1.3 (sum of squares identity): grade and proof", "L09.html:72-80", "PASS",
    "Re-derived: sum (x_i - m)^2 = sum x_i^2 - 2m sum x_i + n m^2; with m = mean and sum x_i = n mean the result is sum x_i^2 - n mean^2. Grade T, hypotheses (1)-(3) stated and used. Claim markup at L09:73 has data-grade=T.")
row(16, "2.4 Theorem 2.1 (one step of the update) and its algebra", "L09.html:84-95", "PASS",
    "Re-derived the mean step (n M_n = (n-1) M_{n-1} + x_n) and the sum step: with d = x_n - M_{n-1}, x_n - M_n = d(n-1)/n, the true difference of the Lemma 1.3 sums is d^2(n-1)/n, equal to the update increment. Hypothesis (4) used in both parts.")
row(17, "2.4 Theorem 2.2 (induction) and its cited induction principle", "L09.html:97-105; course/modules/M/M1/L06.html:60,64", "PASS",
    "Base case and inductive step re-read. The cited 'Theorem 1.2 of M1 Lesson 6' is the induction principle at M1/L06.html:64 (checked by sed read). Concept link to concepts.html#mathematical-induction resolves to the M1 L06 dfn at L06.html:60.")
row(18, "2.4 Corollary 2.3 (six operations, O(1))", "L09.html:107-115", "PASS",
    "Counted the six operations (subtraction, division, addition; subtraction, multiplication, addition) and the constant c=6 witness for O(1) in n, as the Lesson 1 definition requires. Space claim (three numbers) matches the state triple of Definition 1.2.")
row(19, "2.2/2.4 problem sets L09 (M1-M3, P1-P3, E1-E3, R1-R3)", "L09.html:254-352", "PASS",
    f"Every worked solution re-derived: M1 (sum 40, S8=32, 32/7, 4); M2 (S2=0.5, M3=2, S3=2); M3 (S4=1, population 1/4 = p(1-p)); P1, P2 (constant stream), P3 (merge identity with a(m_A-m)^2+b(m_B-m)^2 = ab Delta^2/(a+b)); E1 (naive zero mechanism, Fraction reference); E2 (unrounded 0.08728110122738864 and 9.25811790803366e-16, product 8.08e-17, from {S}l09_numbers_r3.txt); E3 (qualitative, labelled hypothesis); R1 (weighted recursion, the S_n identity re-derived symbolically, example M2=1.75, S2=0.75); R2 (prose); R3 (p(1-p), S10=2.4, sigma^2=0.24). Hypotheses of every step present.")
row(20, "2.4 L10 Theorem 2.2 (invariant) and Theorem 2.3 (front is rolling extreme)", "L10.html:72-92", "PASS",
    "Re-proved both inclusions of D_i = S_i, the base case, and the strict increase; front equals the window minimum and is the latest minimiser. Hypotheses listed and used.")
row(21, "2.4 L10 Theorem 2.4 (2n bound) and Corollary 2.5 (a), (b), (c)", "L10.html:96-114", "PASS",
    "Counting argument for appends (n) and removals (at most n) and for the step (1) comparisons (removals plus one stop per insertion) re-derived; (a) divides 2n by n; (b) D_i within W_i; (c) example re-run: first w insertions keep w indices, the value below all removes w. Corollary (c) worst push confirmed by {S}l10_numbers.py (E2 example removes 5 at w=5).")
row(22, "2.2/2.4 problem sets L10 (M1-M3, P1-P3, E1-E3, R1-R3), P2 changed in 8196077d", "L10.html:247-341", "PASS",
    "Re-derived all twelve solutions. P2 (changed text) follows from Theorem 2.3: the later of two minimum positions is the latest one and so the front. M1 rolling minimum 3,1,1,1,1; M2 fronts 3,1,1,1,1 and the stated deque states; M3 total 8 <= 10; E1 2n-1 = 399; E2 five removals; E3 2n-1; R1 looser rule argument re-checked (p never removed since later window values exceed m); R2 trace fronts 4,1,1; R3 n-w bound and the increasing-series attainment. Output: {S}l10_numbers.txt.")
row(23, "2.4 L11 Lemma 2.3 (partial sums below one)", "L11.html:95-104", "PASS",
    "Telescoping 1/((h+1)(h+2)) = 1/(h+1) - 1/(h+2) re-derived; sum to H is 1 - 1/(H+2) < 1 for every H >= 0. H=0 gives 1/2 = 1 - 1/2.")
row(24, "2.4 L11 Theorem 2.2 (weight conservation, compaction bound) and Theorem 2.4 (rank error)", "L11.html:84-115", "PASS",
    f"Re-proved: weight conservation (add +1, compaction 0); P_h argument gives C_h k_h 2^h <= n; parity step 2*floor(c/2)-c in {{0,-1}} gives per-compaction change in {{0,-2^h}}; E <= eps n by Lemma 2.3. Stress check {S}l11_theorem_stress.py / l11_theorem_stress.txt: 300 generated streams (random, increasing, decreasing, small-integer) x 4 epsilons x 21 probes: weight = n, E <= eps n, -E <= R-hat - R <= 0, -E <= R-hat^- - R^- <= 0 and both rank inequalities all held.")
row(25, "2.4 L11 Theorem 2.5 (quantile answer) and Corollary 2.6 (memory)", "L11.html:117-138", "PASS",
    f"Re-proved the upper and lower counts of Theorem 2.5 (j* minimality, f first index, the j*=1 case). Corollary 2.6 closed form re-derived: (L+1)(L+2)(L+3)/(3 eps) + (L+1) gives 198430 at L=29, eps=1/20 and 18213 at L=12. Exact sum over h = 0..12 of (20(h+1)(h+2)-1) = 20*910 - 13 = 18187 ({S}l11_numbers.txt). Problem R3's 18187 also confirmed.")
row(26, "2.2/2.4 problem sets L11 (M1-M3, P1-P3, E1-E3, R1-R3)", "L11.html:289-392", "PASS",
    f"M1 capacities 20, 60, 120; M2 query returns 5 (running totals 1, 3, 7 against qn = 3.5); M3 level 1 holds 20 items, weight 40 (script output 'M3 level sizes [0, 20] weight 40'); P1 telescoping; P2 parity; P3 (fixed to 1 <= n < k_0, see C-58); E1 stored 29, weight 39, E = 1 (output 'E1 level sizes [19, 10] stored 29 weight 39 E 1'); E2 per-level bounds 125, 20, 5, 1 summing to 151 equal the per-level counts printed by {S}l11_numbers.txt; E3 direction; R1 level-dependent capacities; R2 odd-position variant (change in {{0, +2^h}}, signs reversed, guarantee re-derived); R3 18187. Output: {S}l11_numbers.txt.")
row(27, "2.2 L09 prose numbers and key results", "L09.html:52,117,218,224-225,235,239,309,315,322,366", "PASS",
    f"Every printed or derived number recomputed from unrounded values by {S}l09_numbers_r3.py: 0.087281 (exact 0.0872811009301336 at 1e9), 2^18 = 262144, 2.0000000020427e21, 3.2e6, 174.5 (174.4749), 9.26e-16, 7.45e-8, 1.27e-14, 2.82e-17, 7.286e-15. Key-results row L09:366 matches the naive 0.0 and Welford 7.449e-8.")
row(28, "2.2 L09 ratios of errors (misconception 2)", "L09.html:239", "PASS",
    "Unrounded ratios naive/Welford: offset 0 7.8700; offset 1e6 1.6026e8; offset 1e9 1.3424e7 (from the unrounded relative errors printed by {S}l09_numbers_r3.txt). Printed as 7.87, 1.60e8, 1.34e7, matching the page, and 'about 8, about 1.6e8, about 1.3e7' in the prose.")
row(29, "2.2 L10 prose numbers and key results", "L10.html:52,61,120,211,228,232,356,397; quiz L10:375-397", "PASS",
    "2n = 400; totals 396-399; largest deque 10 at w=30; largest single removal 5 at w=5; 19 = 2n-1 for n=10; 7 = n-w for n=10, w=3; all re-derived by {S}l10_numbers.py.")
row(30, "2.2 L11 prose numbers, worked examples and quiz", "L11.html:52,137,259,265-267,276,313,349,354,356,364,390,406,442,447,477-479,488", "PASS",
    f"198430 (L=29), 18213 (L=12, = 2730/0.15 + 13), 18187 (Problem R3), 5000, 500, 220, 0.0212, 0.0442, 151 (125+20+5+1), 305, 1000-value example (R^-(500)=499, R(500)=500, R^-(501)=500, R(501)=501, R^-(450)=449, R(450)=450, 550, 450), 3.9, 29, 39, 20, 40, 60, 120 all recomputed in {S}l11_numbers.txt and by hand. The why-it-matters numbers (L11:52) match the Corollary 2.6 closed form.")
row(31, "2.3 grades: L09 claim spans and key results", "L09.html:73,85,98,108,362-366", "PASS",
    "Re-graded independently. Lemma 1.3, Theorems 2.1-2.2 and Corollary 2.3 are proofs on the page (T). Key-results row 366 is a lab reading graded C with basis 'Lab 1 (SIMULATED stream, one seed)' (C is correct for a single-run reading). Other key-results rows T.")
row(32, "2.3 grades: L10 claim spans and key results", "L10.html:73,85,97,107,352-356", "PASS",
    "Theorems 2.2-2.4 and Corollary 2.5 are proved on the page (T). Key-results row 356 is a single-run reading graded C with basis 'Lab 1 (SIMULATED series, one seed)'.")
row(33, "2.3 grades: L11 claim spans and key results", "L11.html:85,96,107,118,130,402-406", "PASS",
    "Theorem 2.2, Lemma 2.3, Theorems 2.4-2.5 and Corollary 2.6 are proved on the page (T). Key-results row 406 is a lab reading graded C with basis 'Lab 1 (SIMULATED stream, one seed)'.")
row(34, "2.3 Lemma 1.3 claim markup (round-2 defect)", "L09.html:73", "PASS",
    "Span is 'block-title claim' with data-grade='T' and the hypotheses are listed in the body (L09:74). Re-checked in the current file.")
row(35, "2.3 Lemma 2.3 claim markup (round-2 defect)", "L11.html:96", "PASS",
    "Span is 'block-title claim' with data-grade='T'; hypotheses ('For every integer H >= 0') stated in the body (L11:97).")
row(36, "2.9 DAG usage: concepts used outside the prerequisite closure", "L09.html:38,60,65,104; L10.html:38,67,94,108; L11.html:38,62-63,76", "PASS",
    "Concepts used: big-O (L01, earlier unit lesson, defined at L01), mathematical-induction (M1 L06, in the CS2 closure after Architect issue 1), comparison-sorting and binary-search (L04, earlier), welford-algorithm, monotonic-deque, quantile-sketch (each defined in its own lesson before use). Variance and quantile are plain formulas, with no dfn and no link (architect decision Q2). 'compaction' first appears at L11:73 inside its definition.")
row(37, "2.6 notation: symbols against notation/notation.json", "L09.html, L10.html, L11.html; notation/notation.json", "PASS",
    f"{S}prose_scan.py / prose_scan.txt: macros used are standard KaTeX only (no registry macro \\\\E, \\\\R, \\\\N, \\\\Var, ...). No registered symbol (T, Phi, gamma_3, gamma_4, R^ast, R^{{e ast}}, R_f, Q) appears in the three pages. Local letters (S, sigma, m, N, W, D, E, H, L, B_h, C_h, P_h, k_h, R(v) as rank) are defined in the lesson where used, as notation.json's 'about' field allows.")
row(38, "2.1 attributions: cross-unit citations", "L09.html:104; L10.html:79; course/modules/M/M1/L06.html:60,64", "PASS",
    "'Theorem 1.2 of M1 Lesson 6' is the induction principle (M1/L06.html:64). Read directly; no bibliographic claim is made.")
row(39, "2.9 prose: process words, unfinished text, terms used before definition", "L09.html, L10.html, L11.html; cards.json", "PASS",
    f"{S}prose_scan.txt: zero banned-phrase hits (TODO, TBD, lorem, studies show, clearly, obviously, can be shown, builder, verifier, round N, ...) in the pages and in the 56 cards. The only ellipses in L11 are sequence notation ('levels h = 0, 1, 2, ...', '2nd, 4th, ..., k_h-th', 'buffer[1::2]'), not omitted content. Terms: compaction first at L11:73 (defined there), amortized defined at L10:94 before Corollary 2.5(a) uses it.")
row(40, "2.9 prose: scope words (every, all, always, only, never, exact, any)", "L09.html:52-238; L10.html:61-231; L11.html:52-275", "PASS",
    "Each scope claim checked against a proof or a computation: 'exact sum of squares' (L09:218, Fraction computed); 'never needed for the minimum' (L10:70, window argument); 'never returns' (L10:218, removal rule); 'always holds one entry' (L10 E3, strictly decreasing); 'every stream' (L11, Theorems 2.4-2.5 plus {S}l11_theorem_stress.txt); 'grows only as a cubic' (L11:52, Corollary 2.6 upper bound); 'not claimed to be optimal' (L11:266). Changed sentences re-checked (L09:218, L10:280, L11:52, L11:267, L11:336-338).")
row(41, "2.9 structure L09: section order, minimum counts, quiz", "L09.html", "PASS",
    "Order: why-it-matters (110 words, <= 120), s1, s2 (lab inline after the proofs), canon-breaks, misconceptions (3), problem set (3 per tier, solutions in details), key results (5 rows), retrieval quiz (9 items, each with explain), references, navigation. data-hours=10.")
row(42, "2.9 structure L10: section order, minimum counts, quiz", "L10.html", "PASS",
    "Order as BUILDER_RULES 4.2. why-it-matters 96 words; misconceptions 3; problem set 3 per tier; key results 5 rows; quiz 10 items with explain; data-hours=8.")
row(43, "2.9 structure L11: section order, minimum counts, quiz", "L11.html", "PASS",
    "Order as BUILDER_RULES 4.2. why-it-matters 120 words (at the limit); misconceptions 3; problem set 3 per tier; key results 5 rows; quiz 10 items with explain; data-hours=7.")
row(44, "2.7 cards sample (1 in 10): CS2-c116 (L09)", "course/modules/CS/CS2/cards.json (id CS2-c116)", "PASS",
    "Front and back read in full; matches L09 Section 1 (online definition, L09:56). T grade for a definition, no hypothesis needed.")
row(45, "2.7 cards sample (1 in 10): CS2-c126 (L09)", "cards.json (CS2-c126)", "PASS",
    "Back agrees with Theorem 2.2 hypothesis (3) and the misconception at L09:238; grade T for a negative statement about the theorem is correct.")
row(46, "2.7 cards sample (1 in 10): CS2-c135 (L10)", "cards.json (CS2-c135)", "PASS",
    "Hypotheses (w >= 1, real values, exact comparisons) and the series x0 < ... < x(w-1) then a smaller value match Corollary 2.5(c) at L10:108 and 113.")
row(47, "2.7 cards sample (1 in 10): CS2-c200 (L11)", "cards.json (CS2-c200)", "PASS",
    "Lab 1 prints 'all 9 probes pass' for both epsilons (L11 expected block, lines 257-258). Key empirical result with basis, C grade. Not trivia in the sense of C-63.")
row(48, "2.7 cards sample (1 in 10): CS2-c205 (L11)", "cards.json (CS2-c205)", "PASS",
    "Level 1 holds 20 items after 40 adds at eps=1/10 (Problem M3, L11:313; script output 'M3 level sizes [0, 20]'). T grade with a worked-problem basis is acceptable.")
row(49, "2.7 card CS2-c207 (round-2 FAIL): hypotheses of 'deficit never positive'", "course/modules/CS/CS2/cards.json (CS2-c207)", "PASS",
    "Back now lists: values added in order, exact arithmetic, n >= 1, epsilon in (0,1), 0 <= q <= 1, and the capacities of Definition 2.1, matching Theorem 2.5's hypotheses (L11:86, 118-119). Round-2 defect fixed.")
row(50, "2.7 cards CS2-c151, CS2-c235, CS2-c217 (round-2 FAIL): hypotheses", "cards.json (CS2-c151, CS2-c235, CS2-c217)", "PASS",
    "All three now carry the hypotheses they use (values added in order, epsilon in (0,1) with Definition 2.1 capacities, exact arithmetic, n >= 1). c217 uses 1 <= n < k_0 as in L11 bullet 3 (L11:267). Round-2 defect fixed.")
row(51, "2.7 card CS2-c138: hypotheses (round-1 fix)", "cards.json (CS2-c138)", "PASS",
    "Back: 'Assume w >= 1, real values with no NaN and exact comparisons. No. It holds only the candidates' matches Theorem 2.2 hypotheses (L10:74).")
row(52, "2.7 card CS2-c225: hypotheses", "cards.json (CS2-c225)", "PASS",
    "Back: 'Assume the stream of Theorem 2.2 and exact arithmetic. The three numbers n, M_n and S_n. No earlier value is kept (Corollary 2.3).' Hypotheses of Corollary 2.3 (L09:109) carried.")
row(53, "2.7 full duplicate scan (all 204 cards in the deck)", "cards.json; ledgers/CS2/scripts/CS2-c-r3/cards_dup_scan.py", "PASS",
    f"{S}cards_dup_scan.txt: 204 cards, 204 unique ids, no exact duplicate front or back. Near-duplicate pairs read: CS2-c201/c202/c198/c234/c154/c193 (distinct printed readings, the trivia question is C-63), CS2-c118 and c225 both state the Welford state triple (distinct questions, noted in notes), others are different facts.")
row(54, "2.7 numbers on L09-L11 cards appear in their lesson", "cards.json (L09-L11 cards)", "PASS",
    "Each number traced: c151 198430 (L11:52, 276); c152 500, 550, 450, 1000 (L11:280); c193 7.87 (L09:239) and printed errors (L09:211, 213, 217); c194 8.852e-11 (L09:211); c198 500, 220 (L11:257-258); c205 40, 20, 10 (L11:313); c235 18187, 5000 (L11:389); c231 396-400 (L10:206-210); c234 10, 30 (L10:232).")
row(55, "2.7 cards agree with the CURRENT lesson text and key-results grades (all 56 L09-L11 cards read)", "cards.json (CS2-c116..c153, c154, c167, c193..c236)", "PASS",
    f"All 56 L09-L11 cards read (cards_L09_L11_dump.txt, 56 cards). Statements, hypotheses and grades agree with the current lesson text, including the 8196077d changes (c207, c217, c236 and the removed c195, c199). Trivia standard is applied separately in C-63.")
row(56, "2.9 prose: why-it-matters, hub links, lesson navigation", "L09.html:52,452-453; L10.html:52,451-452; L11.html:52,500-502", "PASS",
    "why-it-matters word counts 110, 96, 120 (LaTeX stripped). Previous/next links correct (L09 to L08 and L10; L10 to L09 and L11; L11 to L10). L11:52 rewrite re-checked for numbers (C-30).")
row(57, "2.7 card CS2-c236 (round-2 FAIL): hypotheses of the per-compaction identity", "cards.json (CS2-c236)", "PASS",
    "Back now assumes the buffer is sorted and that the compaction keeps the 2nd, 4th, ... items (Definition 2.1), then gives 2^h(2 floor(c/2) - c). Matches the proof of Theorem 2.4 (L11:113). Round-2 defect fixed.")
row(58, "2.4/2.9 L11 Section 3 bullet 3 and Problem P3: hypothesis n >= 1 (round-2 FAIL)", "L11.html:267; L11.html:335-338", "PASS",
    "Both now read '1 <= n < k_0' (L11:267, and P3 statement L11:336 and solution L11:338). The E = 0 argument needs n >= 1 for the statement to be about answers at all. Round-2 defect fixed.")
row(59, "2.7 card is not trivia (round-2 FAIL): CS2-c195", "cards.json (CS2-c195)", "PASS",
    "CS2-c195 is absent from cards.json at 8196077d (grep -c CS2-c195 = 0; the 8196077d diff removes it). Round-2 defect resolved by removal.")
row(60, "2.7 card is not trivia (round-2 FAIL): CS2-c199", "cards.json (CS2-c199)", "PASS",
    "CS2-c199 is absent from cards.json at 8196077d (the 8196077d diff removes it). Round-2 defect resolved by removal.")
row(61, "2.9 cross-reference: L11 ε=0 extension 'Section 3, Misconception 2'", "L11.html:65", "FAIL",
    "L11.html:65 says the ε=0 case 'is used in Section 3, Misconception 2 and Problem P3'. Misconceptions is Section 4 (L11.html:271-272, <h2 id=\"s4\">4 Misconceptions</h2>); Section 3 (L11.html:262-269) has three bullets and uses ε=0 in bullets 1 and 3. Confirmed by prose_scan.txt (heading check True).",
    "Replace 'used in Section 3, Misconception 2 and Problem P3' with 'used in Section 3, in Section 4, Misconception 2, and in Problem P3'.")
row(62, "2.9 cross-reference: L11 'Section 3 says what that check does and does not show'", "L11.html:140", "FAIL",
    "L11.html:140 says 'the lab below checks the guarantee on one seeded stream, and Section 3 says what that check does and does not show'. Section 3 (L11.html:262-269) contains only the three canon-breaks bullets (ranks not values, worst-case bound, E = 0 before the first compaction) and says nothing about the lab check. The statement of what the check does and does not show is the interpretation paragraph after the lab (L11.html:259).",
    "Replace 'and Section 3 says what that check does and does not show' with 'and the interpretation after Lab 1 says what that check does and does not show'.")
row(63, "2.7 trivia (BUILDER_RULES §7): cards whose whole answer is one printed reading of Lab 1", "cards.json CS2-c193, CS2-c198, CS2-c201, CS2-c202, CS2-c234", "FAIL",
    "Same standard as the round-2 rulings on CS2-c195 and CS2-c199 (both removed). Each of these asks only for digits printed by one seeded run, with no mechanism, result or Theorem attached: c193 'By what factor is Welford's relative error below the naive error at offset 0' (answer 7.87); c198 'How many items does the sketch store ... for epsilon = 1/20 and 1/10' (answer 500 and 220); c201 'What is the largest excess of #{x < v} over qN' (answer 0.0212 N and 0.0442 N); c202 'What is the largest deficit ...' (answer 0.0000 N at both epsilons); c234 'What is the largest deque size that Lab 1 prints for window 30?' (answer 10). Evidence of the printed values: lab expected blocks L09:206-217, L10:206-210, L11:257-258.",
    "Rewrite each as a card on the result it illustrates (for example c201: 'Does the lab's printed excess stay below epsilon N for both epsilons?', basis Lab 1), or delete it. Keep the basis tag. Do not add a new trivia card in its place.")

frag = {
    "unit": "CS2",
    "slice": "c",
    "round": 3,
    "round_note": "Round 3 final full verification of CS2 slice c (L09-L11, lab twins, cards) at pin 8196077d (detached, /Users/billyribeiro/.fanout/wt/verifyS3-CS2-c). Previous fragment: /Users/billyribeiro/.fanout/frags/S-CS2-c.round2.json at pin 9294b914. Delta for the slice: L09.html:218 (interpretation), L10.html:280 (P2 solution), L11.html:52,267,336-338 (why-it-matters, bullet 3, P3), cards.json (c163 L08 text, c195 and c199 removed, c207, c217, c236 changed, c237 L08 added), index.html:33 lede (not a slice file). The twins are unchanged (tests/labs/CS2 L04 twin is not in this slice). All command rows were re-run; the round-2 PASS rows were re-verified from the current files, not carried.",
    "verifier": "Haiku independent verifier, CS2-c round 3 (did not build CS2)",
    "pin": "8196077d5f56c3919d33e69888176d197d378ad4",
    "base": "9294b914a51647c66d2dee62c4a112c76ba04900 (round-2 pin; round-2 fragment /Users/billyribeiro/.fanout/frags/S-CS2-c.round2.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS3-CS2-c (detached at 8196077d, .venv symlinked)",
    "scratch": "/tmp/cs2c-r3",
    "verified_at": "2026-11-09T06:45:00Z",
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Verdict FAIL: four rows are FAIL (C-11, C-61, C-62, C-63). Each has a stated fix. The lesson mathematics, the three lab twins and their expected blocks, and the 56 L09-L11 cards are otherwise correct on every point re-derived here.",
        "Lab twins are demonstrations, not grader mutants (VERIFIER_RULES ruling). No project grader is in this slice, so run_graders and tools/mutate_graders.py were not run and no mutants are listed. CS2 project graders belong to slice d/e.",
        "Independent recomputations (each a script in ledgers/CS2/scripts/CS2-c-r3/): l09_numbers_r3.py (Fraction reference, unrounded values, ulp, sum-of-squares error), l10_numbers.py (fresh deque implementation from the Definition 2.1 wording, brute force over every window, every worked example), l11_numbers.py (fresh sketch from Definition 2.1 wording; per-level compaction counts 125/20/5/1 and 250/41/10/3/1; stored counts; closed forms; every worked example), l11_stream_independence.py (stored and compaction counts identical over four streams), l11_theorem_stress.py (Theorems 2.2, 2.4, 2.5 on 300 generated streams, 4 epsilons, 21 probes each), lab_page_vs_twin.py (page code, expected blocks and CPython output), prose_scan.py (banned phrases, scope words, macros, cross-reference locators), cards_dup_scan.py (whole-deck exact and near duplicates), write_fragment_r3.py (this fragment).",
        "Judgment calls, stated so the next verifier can reproduce them: (a) the trivia rule applied to CS2-c193/c198/c201/c202/c234 is the one used by round 2 for c195/c199. CS2-c154 (largest removal count 5 tied to Corollary 2.5(c)), CS2-c150 (capacities computed by Definition 2.1), CS2-c194 (the rise of Welford's error across offsets) and CS2-c200 (all probes pass) are kept as key empirical results. (b) The ellipses in L11 ('levels h = 0, 1, 2, ...', '2nd, 4th, ..., k_h-th') are sequence notation, not omitted content. (c) 'why it matters' of L11 is exactly 120 words after stripping LaTeX, at the limit.",
        "Near-duplicate observation, not a row: CS2-c225 ('What state does a Welford update keep?') and CS2-c118 (Welford's recursion, whose back also gives the state triple) share the same fact. Distinct questions, so C-53 passes; the builder may merge them when rewriting c193-c202.",
        "Not checked: render_curriculum.py and build_site.py --check (curriculum and generated files unchanged in the slice delta); verify_refs live (no registry key in the slice); the hub index.html and the other CS2 slices (A, B, D, E, F); the full repository pytest suite (only the subsets listed in C-08); page_smoke beyond L09-L11 (not run, by instruction to run only the slice pages); visual screenshots (page_smoke geometry checks only, no image review). The Python 3.14 pin is checked against pyproject.toml requires-python '>=3.14' (no .python-version file).",
        "Honest gaps: the sketch and deque theorems are proved on the page and supported by brute-force, stress and exhaustive-count checks; the stress checks support but do not prove the theorems. The 'short list of candidate positions' phrase (L10:52) was judged loose but not a number or scope claim, so it was not failed."
    ],
    "mutants": [],
    "rows": rows,
    "summary": {
        "rows": len(rows),
        "pass": sum(r["status"] == "PASS" for r in rows),
        "fail": sum(r["status"] == "FAIL" for r in rows),
        "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows),
        "mutants_killed": "0/0 (no grader in slice)",
        "failing_ids": [r["id"] for r in rows if r["status"] != "PASS"],
    },
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
}
json.dump(frag, open("ledgers/CS2/CS2-c.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("written", len(rows), "rows; verdict", frag["verdict"], frag["summary"])
