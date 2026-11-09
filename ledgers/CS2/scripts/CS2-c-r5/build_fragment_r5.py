# Builds ledgers/CS2/CS2-c.json (round 5). Evidence strings cite the scripts and outputs kept in this directory.
import json, datetime
S = "ledgers/CS2/scripts/CS2-c-r5/"
P = "PASS"; F = "FAIL"
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)

row("C-01", "2.9 structure: check_pages (unit, per page, --all)", "course/modules/CS/CS2/L09.html, L10.html, L11.html, cards.json", P,
    "tools/check_pages.py --unit CS2 -> 'check_pages CS2: PASS'; --unit CS2 --page L09/L10/L11 -> PASS each; --all -> 27 PASS lines, 0 FAIL (%scheck_pages_unit.txt, check_pages_L09/L10/L11.txt, check_pages_all.txt)." % S)
row("C-02", "2.9 DAG: check_dag and concept links", "L09.html:38,65; L10.html:38-39,67; L11.html:38-39,76", P,
    "tools/check_dag.py --unit CS2 -> 'check_dag CS2: PASS'; --all 0 FAIL (%scheck_dag.txt, check_dag_all.txt). Links: mathematical-induction -> concepts.html (M1, now a CS2 prereq: curriculum.json CS2 prereqs [CS1, M1]); big-O -> L01.html#def-big-o-complexity; comparison-sorting and binary-search -> L04.html#def-comparison-sorting / #def-binary-search. Each dfn once: L09.html:65, L10.html:67, L11.html:76. tools/build_site.py --check -> 'site data current: 6 outputs', exit 0 (%sbuild_site_check.txt)." % (S, S))
row("C-03", "2.5 labs: page code equals twin; expected block equals output", "L09.html:119-219; L10.html:118-212; L11.html:142-260", P,
    "tools/run_labs.py --unit CS2 --page L09 / L10 / L11 -> 'run_labs CS2: PASS (1/1)' each; unit run -> PASS (14/14) (%srun_labs_L09.txt, run_labs_L10.txt, run_labs_L11.txt, run_labs_unit.txt). Expected blocks L09.html:206-217, L10.html:206-210, L11.html:257-258 were also compared by eye with the twin outputs in %stwin_L09.out, twin_L10.out, twin_L11.out." % (S, S))
row("C-04", "2.5 labs: twins alone under python -I -W error", "tests/labs/CS2/lab-CS2-L09-1.py, lab-CS2-L10-1.py, lab-CS2-L11-1.py", P,
    ".venv/bin/python -I -W error on each twin: exit 0 for L09, L10, L11; stderr 0 bytes each; stdout saved as %stwin_L09/L10/L11.out. Twins are byte-identical to the previous pin (git diff edbb7aa8 dde0486b lists no tests/labs/CS2/lab-CS2-L09/L10/L11 hunk)." % S)
row("C-05", "2.5/2.9 page_smoke on L09, L10, L11 alone", "L09.html, L10.html, L11.html", P,
    "tools/page_smoke.py --unit CS2 --pages L09 L10 L11 -> 'page_smoke modules/CS/CS2/L09.html: PASS', L10 PASS, L11 PASS, 'page_smoke CS2: PASS' (%spage_smoke.txt)." % S)
row("C-06", "gate: ruff check and ruff format --check", "tests/labs/CS2/lab-CS2-L09-1.py, L10, L11", P,
    "ruff check on the three twins -> 'All checks passed!' exit 0; ruff format --check -> '3 files already formatted' exit 0 (%sruff.txt)." % S)
row("C-07", "gate: mypy --no-incremental (strict config)", "three twins; repository", P,
    ".venv/bin/mypy --no-incremental -> 'Success: no issues found in 385 source files', exit 0 (%smypy_full.txt)." % S)
row("C-08", "gate: relevant pytest", "tests/test_labs.py -k 'CS2 and (L09 or L10 or L11)'; tests/test_docs_figures.py; tests/test_page_checks.py; tests/test_run_labs.py; tests/test_page_smoke.py", P,
    "pytest tests/test_labs.py -k 'CS2 and (L09 or L10 or L11)' -> 3 passed (%spytest_labs_summary.txt). pytest tests/test_docs_figures.py tests/test_page_checks.py tests/test_run_labs.py tests/test_page_smoke.py -> 69 passed (%spytest_subsets_summary.txt). test_figure_kernels.py not run (no figure on these pages)." % (S, S))
row("C-09", "2.1 registry integrity; keys cited on the slice", "L09.html:446; L10.html:445; L11.html:495; references/references.json", P,
    "No data-cite attribute on L09-L11 (grep count 0 in each page) and no cite field on the 49 L09-L11 cards, so the slice cites no registry key. tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' exit 0 (%sverify_refs_offline.txt). The live per-unit verify_refs run was not made (see notes)." % S)
row("C-10", "2.9 hours arithmetic", "L09/L10/L11.html line 2 (data-hours) and line 35 (eyebrow); course/modules/CS/CS2/index.html:29", P,
    "data-hours L09=10, L10=8, L11=7, matching eyebrows at L09.html:35, L10.html:35, L11.html:35. Hub index.html:29 data-hours-lessons=100, data-hours-project=30, total 130 = curriculum.json CS2 hours 130. Sum of L01-L11 data-hours (8+9+10+10+9+9+10+10+10+8+7) = 100.")
row("C-11", "2.5 lab L09 hypothesis and interpretation vs code and output", "L09.html:121, 218; tests/labs/CS2/lab-CS2-L09-1.py:24-27, 30-70", P,
    "Hypothesis claims checked against twin_L09.out and L09.html:206-217: offset 0 all three relative errors < 1e-14 (9.258e-16, 2.819e-17, 7.286e-15); two-pass smallest at each offset; naive relative error ~7e-15 rising to 1.000; naive exactly 0.000000e+00 at 1e9; Welford below naive at each offset. Printed-value readings in L09.html:218 match the output. The unprinted numbers in L09.html:218 are reported in C-74.")
row("C-12", "2.5 lab L10 hypothesis and interpretation vs code and output", "L10.html:120, 211; lab-CS2-L10-1.py:71-76", P,
    "twin_L10.out: all 200 positions match for w in {1,2,5,13,30}; operations min/max 399/399, 398/399, 398/398, 397/398, 396/397 vs bound 400; largest single-push removals 1,2,5,6,6 (equals w for w=1,2,5 only); largest deque size 1,2,5,8,10. Hypothesis (no bound asserted, operations counted) and interpretation sentences match the code (lab-CS2-L10-1.py:71-76 AssertionError, 48 operations count, 75-76 size assertion).")
row("C-13", "2.5 lab L10 twin docstrings", "tests/labs/CS2/lab-CS2-L10-1.py:1-9, 21-26", P,
    "Docstring claims re-read against code: window holds min(w, i+1) values (brute() lines 56-59); operations are appends plus removals (line 48); largest single-push removals and 2N printed (lines 49, 79); min-mode values strictly increase front to back (class docstring lines 22-25 agree with the step (1) test at line 39).")
row("C-14", "2.5 lab L11 hypothesis, code claims, interpretation, expected block", "L11.html:144, 259-260; lab-CS2-L11-1.py:3-4, 99-108", P,
    "Hypothesis (L11.html:144, edited in the delta) is exactly the assertion at lab-CS2-L11-1.py:99 (below > qN+eps*N or at_or_below < qN-eps*N raises): both inequalities checked for nine probes at two epsilons, so excess and deficit are each held to eps as fractions of N (worst_excess/N and worst_deficit/N printed, lines 101-108). twin_L11.out matches L11.html:257-258; interpretation figures 0.0212, 0.0442, 0.0000, 500, 220 match.")
row("C-15", "2.3/2.4 Lemma 1.3 (sum of squares identity) grade and proof", "L09.html:72-80", P,
    "Re-derived by hand: expand sum (x_i - m)^2 = sum x_i^2 - 2m sum x_i + n m^2; with m = xbar, sum x_i = n xbar gives sum x_i^2 - n xbar^2. Hypotheses (1)-(3) listed at L09.html:74. Grade T correct (proved on page).")
row("C-16", "2.4 Theorem 2.1 (one step) and its algebra", "L09.html:84-95", P,
    "Re-derived: n M_n = (n-1) M_{n-1} + x_n; with d = x_n - M_{n-1}, x_n - M_n = d(n-1)/n; the S-update adds d^2(n-1)/n, equal to the change in the true sum of squares computed from Lemma 1.3 (expansion checked line by line at L09.html:93-94). Numerically: Welford estimates agree with the exact Fraction variance to 9e-16 at offset 0 (%snumbers_r5.out)." % S)
row("C-17", "2.4 Theorem 2.2 induction and its cited induction principle", "L09.html:97-105; course/modules/M/M1/L06.html:60,64", P,
    "L09.html:104 cites 'Theorem 1.2 of M1 Lesson 6'. M1/L06.html:64 is Theorem 1.2 (the induction principle): if P(n0) and P(k) implies P(k+1) then P(n) for all n >= n0. Base case and step match.")
row("C-18", "2.4 Corollary 2.3 (six operations, O(1))", "L09.html:107-115; tests/labs/CS2/lab-CS2-L09-1.py:36-39", P,
    "Counted the six operations in the proof (L09.html:114): subtraction, division, addition for M; subtraction, multiplication, addition for S. The twin's welford_variance (lines 35-39) performs the same six operations per value. The claim is an operation count, not a time (page says so).")
row("C-19", "2.4 problem sets L09 (M1-M3, P1-P3, E1-E3, R1-R3)", "L09.html:254-352", P,
    "Recomputed: M1 sum 40, S_8 = 32, 32/7 = 4.5714, 32/8 = 4 (L09.html:258); M2 M_3 = 2, S_3 = 2 (265); M3 S_4 = 1, pop var 1/4 (272); P1 S_2 = d^2/2 (283); P2 (290); P3 combined-SS formula, a(m_A-m)^2 + b(m_B-m)^2 = ab Delta^2/(a+b) re-derived (297); E2 product 8.08e-17 (numbers_r5.out); R1 weighted update and example 0.75 (336) re-derived; R3 0.24 and 2.4 (350). E1 digits are reported in C-74.")
row("C-20", "2.4 L10 Theorem 2.2 (deque invariant) and Theorem 2.3 (front is rolling min)", "L10.html:72-92", P,
    "Proofs re-read step by step (base case uses w >= 1; inductive steps (a)-(c); D_i = S_i both inclusions). invariants_r5.py (%sinvariants_r5.out): 3000 seeded series, w in 1..6, n in 1..30, values with ties in 0..4: 0 violations of D_i = S_i, of front = rolling minimum, or of the front being the latest minimal position." % S)
row("C-21", "2.4 L10 Theorem 2.4 and Corollary 2.5(a),(b),(c)", "L10.html:96-114", P,
    "Proof of Theorem 2.4 re-derived (n appends, at most n removals, one stopping comparison per insertion). Corollary 2.5(c) example: l10_extra.py (%sl10_extra.out) confirms that for w = 1..7 the series x_0 < ... < x_(w-1) then a smaller value makes the last insertion remove w entries. Step (3) removals on an increasing series equal n - w (checked for n in {6,10,25}, w in {1,2,3,5}). Randomized run in invariants_r5.out: deque size never exceeds w." % S)
row("C-22", "2.2/2.4 L10 problem sets (M1-M3, P1-P3, E1-E3, R1-R3)", "L10.html:247-341", P,
    "M1 rolling minimum 3,1,1,1,1 (numbers_r5b.out); M2 trace [(0,3)],[(1,1)],[(1,1),(2,4)],[(3,1)],[(3,1),(4,5)] reproduced by brute_min_deque_trace (numbers_r5b.out); M3 total 8 <= 10. E1 (w=1 gives 2n-1; 399 on the lab series) checked on 20 random series; E2 removals [0,0,0,0,0,5] (numbers_r5b.out); E3 total 19 for a decreasing series of 10 values for every w tested; R2 trace [(1,1),(2,4)] (numbers_r5b.out); R3 n - w (l10_extra.out). P1-P3 and R1 proofs re-derived.")
row("C-23", "2.4 L11 Lemma 2.3 (partial sums below one)", "L11.html:95-104", P,
    "Telescoping 1/((h+1)(h+2)) = 1/(h+1) - 1/(h+2) re-derived; partial sum 1 - 1/(H+2) < 1 for every H >= 0 (L11.html:98, 103).")
row("C-24", "2.4 L11 Theorems 2.2(a),(b), 2.4 and 2.5", "L11.html:84-127", P,
    "Proofs re-read line by line (L11.html:91-93, 111-115, 122-126). invariants_r5.py (%sinvariants_r5.out): 60 seeded instances (eps = k/20, k/30 or k/50 with k in {1,2,3,5,10,20} and 0 < eps < 1, n up to 600, ties), 2870 probe values: 0 violations of -E <= Rhat - R <= 0 and -E <= Rhat^- - R^- <= 0, of E <= eps n, of total weight = n, and of the Theorem 2.5 counts at 21 q values." % S)
row("C-25", "2.4 L11 Corollary 2.6 and the growth closed form", "L11.html:129-137", P,
    "numbers_r5b.out: L = 29 for n=1e9, closed form (L+1)(L+2)(L+3)/(3 eps) + (L+1) = 198430.0; L = 12 for n=5000, closed form 18213.0; exact sum of (k_h - 1) over h=0..12 = 18187 (= 20*910 - 13). Growth O((log2 n)^3/eps) follows from the formula. The inequality k_h - 1 <= (h+1)(h+2)/eps + 1 holds since k_h < 2((h+1)(h+2)/(2 eps)+1).")
row("C-26", "2.2/2.4 L11 problem sets", "L11.html:289-392", P,
    "numbers_r5b.out: M1 k = 20, 60, 120 for eps = 1/10; M3 40 adds give level sizes [0, 20], total weight 40, compactions [2, 0]; E1 39 adds give stored 29, total weight 39, one compaction, E = 1 (3.9 = eps n). E2: capacities 40, 120, 240, 400, 600; per-level compactions on the seeded stream [125, 20, 5, 1, 0] = the level bounds floor(5000/(k_h 2^h)) [125, 20, 5, 1, 0], total 151. E3: stored 500 (eps 1/20) and 220 (eps 1/10) for four different streams (seeded uniform, sorted, reversed, another seed). R1 and R2 algebra re-derived (R2: the odd-position change is 2^h(2 ceil(c/2) - c) in {0, 2^h}). R3 18187. P1-P3 re-derived.")
row("C-27", "2.2 L09 prose numbers and key-results numbers (unrounded)", "L09.html:52,117,218,224-225,235,239,309,315,322,366", P,
    "numbers_r5.out: exact variance 0.087281101227 (offset 0), 0.0872811009301 (offset 1e9); relative errors 9.258e-16, 2.819e-17, 7.286e-15 (offset 0), 8.852e-11, 4.357e-17, 1.418e-2 (1e6), 7.449e-8, 1.269e-14, 1.0 (1e9); math.ulp(2e21) = 262144.0; 1.27e-14, 7.45e-8 match. Values that the lab does not print are reported separately in C-74; the printed-value numbers are correct.")
row("C-28", "2.2 L09 misconception-2 ratios", "L09.html:239", P,
    "numbers_r5.out ratio NV/W from unrounded relative errors: 7.8697 (offset 0), 1.60251e8 (1e6), 1.34241e7 (1e9). Prose: about 8, 1.6e8, 1.3e7 and the two-digit factors 7.87, 1.60e8, 1.34e7 are reproduced from the unrounded values.")
row("C-29", "2.2 L10 prose numbers, key results and quiz numbers", "L10.html:52,61,120,211,228,232,356,397; quiz L10.html:375-397", P,
    "Printed totals 396-399 and bound 400 (twin_L10.out); largest deque size 10 for window 30; largest single-push removal 5 for window 5 and 6 for windows 13 and 30; quiz answers 1 (position 4 minimum), 19 (= 2n-1 for n=10), 400 (= 2 x 200), 7 (= n - w for n = 10, w = 3) recomputed (numbers_r5b.out, l10_extra.out).")
row("C-30", "2.2 L11 prose numbers, worked examples and quiz", "L11.html:52,137,259,265-267,276,280,299,313,349,354,356,364,390,406,442,447,477-479,488", P,
    "Recomputed in numbers_r5b.out and numbers_r5.out: 198430, 18213, 18187, 500, 220, 151, 0.0212 and 0.0442 (twin_L11.out), 3.9, 2730/0.15 = 18200 then + 13, 40/120/240, 20/60/120, 29, 1, 18187, 500 and 1000 with R^-(1000)=500 <= 550 and R(1000)=1000 >= 450, and 450 with R^-(450)=449 <= 550, R(450)=450 >= 450.")
row("C-31", "2.3 grades L09 claim spans and key results", "L09.html:73,85,98,108,362-366", P,
    "Re-graded against BLUEPRINT 3: Lemma 1.3, Theorems 2.1-2.2 and Corollary 2.3 are proved on the page (T); key-results row 366 rests only on Lab 1 output (C with basis naming the lab), as ruling 13 requires. The key-results rows mirror cards c119-c122 and c124 with the same grade and basis.")
row("C-32", "2.3 grades L10 claim spans and key results", "L10.html:73,85,97,107,352-356", P,
    "Theorems 2.2-2.4 and Corollary 2.5 are proved on the page (T); row 356 is lab output only (C naming Lab 1). Mirrored cards c130-c134 (T) and c231 (C) carry the same grades and basis.")
row("C-33", "2.3 grades L11 claim spans and key results", "L11.html:85,96,107,118,130,402-406", P,
    "Theorems 2.2, 2.4, 2.5 and Lemma 2.3 and Corollary 2.6 are proved on the page (T); row 406 is lab output only (C naming Lab 1). Mirrored cards c145-c149 (T) and c198, c200 (C) match.")
row("C-34", "2.3 Lemma 1.3 claim markup", "L09.html:73", P, "L09.html:73 is '<span class=\"block-title claim\" data-grade=\"T\">Lemma 1.3'.")
row("C-35", "2.3 Lemma 2.3 claim markup", "L11.html:96", P, "L11.html:96 is '<span class=\"block-title claim\" data-grade=\"T\">Lemma 2.3'.")
row("C-36", "2.9 DAG usage by name outside the prerequisite closure", "L09.html:38,60,65,104; L10.html:38,67,94,108; L11.html:38,62-63,76", P,
    "CS2 prerequisites are now [CS1, M1] (curriculum.json), so mathematical-induction (M1) is in the closure. L09-L11 use big-O (L01) and comparison sorting and binary search (L04, in unit). Variance and quantile-function (M4) appear as plain formulas and prose with no dfn and no link, as architect issue 2 and Q2 require (grep: no data-concept=\"variance\" or \"quantile-function\" on the slice).")
row("C-37", "2.4 notation vs notation/notation.json", "L09.html, L10.html, L11.html; notation/notation.json", P,
    "No registered macro (\\\\E, \\\\Prob, \\\\Var, \\\\R, \\\\N, \\\\indic, ...) and no registered symbol (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\\\mathbb{Q}) occurs on the three pages (grep of every \\\\macro: only sum, times, bar, ge, le, cdot, mathrm, text, sigma, ldots, Delta, lt, approx, texttt, frac, Bigl/Bigr, pm, in, min, max, subseteq, cup, ne, log, cdots, varepsilon, hat, lfloor, rfloor, lceil, rceil). Local letters (R, R^-, hat R, E, C_h, P_h, B_h, W_i, D_i, S_i, H, L, k_h, sigma) are each defined in the lesson where first used (Def 1.1, Def 2.1, Thm 2.2, Thm 2.4, Lemma 2.3, Cor 2.6). No collision.")
row("C-38", "2.1 attributions: cross-unit citations", "L09.html:104; L10.html:79; course/modules/M/M1/L06.html:60,64", P,
    "No author, year, title or venue appears in L09-L11 (grep for Cormen, Knuth, Greenwald, Khanna, Welford, Technometrics, 1962, 2001 returns nothing). The only cross-unit attribution is M1 Lesson 6 Theorem 1.2 (M1/L06.html:64), read in full above.")
row("C-39", "2.9 process words, unfinished text, terms before definition", "L09.html, L10.html, L11.html; cards.json", P,
    "grep for TODO, TBD, lorem, for brevity, left as an exercise, beyond the scope, details omitted, it is important to note, obviously, clearly, well known, studies show, experts agree, builder, verifier, ledger, round, delta, ellipsis in prose: no hit in the learner text (two matches are code variables in twins L09 and in L11 code docstring, not learner prose). Terms: compaction, level, weight, window, deque are defined before their core use (Def 1.1, Def 2.1 in each lesson).")
row("C-40", "2.9 scope words (every, all, always, never, exact, any, only, stable, optimal)", "L09.html:52-238; L10.html:61-231; L11.html:52-275", P,
    "Every universal claim is proved for all inputs (Theorem 2.2 and Lemma 2.3 in L09; Theorems 2.2-2.4 and Cor 2.5 in L10; Theorems 2.2-2.5 in L11 with 'for every stream') or is scoped to the lab stream (L09.html:218, L10.html:211, L11.html:259, L11.html:140). 'Stable' appears only as a question measured by the lab (L09.html:224). 'Optimal' is disclaimed (L11.html:266).")
row("C-41", "2.9 structure L09: section order, minimum counts, quiz", "L09.html", P,
    "Order: why-it-matters (52), s1 (54), s2 Theorem 2.1-2.2 and Corollary 2.3 (82-115), inline Lab 1 (119-219), s3 canon (222), s4 misconceptions (231; 3 items), s5 problems (248; M1-M3, P1-P3, E1-E3, R1-R3), s6 key results (356; 5 rows), s7 quiz (372; 9 items), s8 references, lesson navigation. why-it-matters under 120 words (check_pages). No debate key in CS2 curriculum (plan section 0).")
row("C-42", "2.9 structure L10: section order, minimum counts, quiz", "L10.html", P,
    "Order: why-it-matters (52), s1 (54), s2 Definition 2.1-Theorem 2.4 and Corollary 2.5 (63-114), inline Lab 1 (118-212), s3 canon (214; 3 items), s4 misconceptions (223; 3 items), s5 problems (241; 12 problems in four tiers), s6 key results (346; 5 rows), s7 quiz (362; 10 items), navigation.")
row("C-43", "2.9 structure L11: section order, minimum counts, quiz", "L11.html", P,
    "Order: why-it-matters (52), s1 (54-68), s2 Definition 2.1-Corollary 2.6 (70-138), inline Lab 1 (142-260), s3 canon (262; 3 items), s4 misconceptions (271; 3 items), s5 problems (289; 12 problems in four tiers), s6 key results (396; 5 rows), s7 quiz (412; 10 items), navigation (previous L10 only; last lesson of the unit).")
row("C-44", "2.7 cards sample (1 in 10): CS2-c116 (L09)", "cards.json:792 (CS2-c116)", P,
    "'What is an online statistic?' matches L09 Section 1 (L09.html:56). Atomic, checkable, grade T as a definition.")
row("C-45", "2.7 cards sample (1 in 10): CS2-c126 (L09)", "cards.json:857 (CS2-c126)", P,
    "'Does Welford's update give the exact variance in floating point?' matches L09 misconception 2 (L09.html:238-239) and hypothesis 3 of Theorem 2.2; T correct.")
row("C-46", "2.7 cards sample (1 in 10): CS2-c135 (L10)", "cards.json:920 (CS2-c135)", P,
    "Back now lists the w values and the lower value; matches Corollary 2.5(c) (L10.html:108) and the series checked in l10_extra.out (last insertion removes w entries for w = 1..7). Grade T correct.")
row("C-47", "2.7 cards sample (1 in 10): CS2-c200 (L11)", "cards.json:1233 (CS2-c200)", P,
    "Correctness of the card: the twin asserts all nine probes at both epsilons (lab-CS2-L11-1.py:99) and twin_L11.out prints 'all 9 probes pass'. Triviality of the card is reported in C-63.")
row("C-48", "2.7 cards sample (1 in 10): CS2-c205 (L11)", "cards.json:1241 (CS2-c205)", P,
    "'20 items' at level 1 after 40 adds with eps = 1/10 matches Problem M3 (L11.html:313) and the recomputation in numbers_r5b.out (level sizes [0, 20]).")
row("C-49", "2.7 card CS2-c207 hypotheses (round-2 FAIL)", "cards.json:1248 (CS2-c207)", P,
    "Hypotheses listed (values in order, exact arithmetic, n >= 1, eps in (0,1), 0 <= q <= 1, capacities) are those of Theorem 2.5; statement R(v) >= qn is correct (Theorem 2.5 upper count). Duplicate of c148's fact is reported in C-53.")
row("C-50", "2.7 cards CS2-c151, CS2-c235, CS2-c217 hypotheses (round-2 FAIL)", "cards.json:1025 (c151), 1378 (c235), 1326 (c217)", P,
    "c151 and c235 list the hypotheses of Theorem 2.2 and Corollary 2.6 (values in order, eps in (0,1) with the capacities, exact arithmetic, n >= 1), and the numbers 198430 and 18187 are correct. c217 states 1 <= n < k_0 and the Problem P3 hypotheses (L11.html:336-338).")
row("C-51", "2.7 card CS2-c138 hypotheses", "cards.json:934 (CS2-c138)", P,
    "'Assume w >= 1, real values with no NaN and exact comparisons' matches Theorem 2.2 hypotheses (L10.html:74).")
row("C-52", "2.7 card CS2-c225 hypotheses", "cards.json (CS2-c225, absent)", P,
    "CS2-c225 is absent from cards.json at the pin (removed in 55d171e9..dde0486b); no card left to check. Its duplicate fact with c118 is resolved (C-68).")
row("C-53", "2.7 full duplicate scan (whole deck, 204 cards)", "cards.json:1004 (CS2-c148), 1248 (CS2-c207)", F,
    "cards_scan_r5.py (%scards_scan_r5.out): 200 cards, 200 unique ids, all ids well formed, every non-T card has basis or cite. Near-duplicate scan (difflib on front+back, ratio >= 0.55 or front >= 0.7): 36 pairs; the pairs inside L09-L11 are (CS2-c146, c149), (c143, c226), (c148, c207). The first two ask different facts. CS2-c207 (front 'Why can the deficit ... never be positive') restates the R(v) >= qn conclusion of CS2-c148 (back: 'the query returns a stored v with R(v) >= qn ... Theorem 2.5') and is the same fact asked a second time." % S,
    "Delete CS2-c207 or change it to a fact not on CS2-c148, for example the sign bound of Theorem 2.4 (-E <= Rhat(v) - R(v) <= 0) with its per-compaction reason, and keep its back free of the R(v) >= qn conclusion.")
row("C-54", "2.7 numbers on L09-L11 cards appear in their lesson", "cards.json (L09-L11 cards)", P,
    "Each number checked against its lesson: 0.087281 (L09.html:207-217 output); 9.258e-16, 8.852e-11, 7.449e-08 (L09.html:207,211,215); 40, 120, 240 (L11.html:356); 20, 60, 120 (L11.html:299); 198430 (L11.html:52,276); 500, 1000, 550, 450 (L11.html:280); 500, 220, 5000 (L11.html:257-258); 20, 10, 40 (L11.html:313); 396-399, 400 (L10.html:206-210); 10 and 30 (L10.html:210); 18187 (L11.html:389); six (L09.html:114).")
row("C-55", "2.7 cards agree with CURRENT lesson text and key-results grades", "cards.json (all 49 L09-L11 cards); L09.html:226, 224-226; L10.html:108; L11.html:119, 137, 299, 356", P,
    "All 49 L09-L11 cards read against the current pages. c216 ('must not return 0') agrees with the delta-edited canon bullet L09.html:226 ('must raise an error rather than return 0'). c150 (now T) agrees with M1 (L11.html:299) and E2 (L11.html:356). c135 agrees with L10.html:108. c148 agrees with Theorem 2.5 (L11.html:119). c151 agrees with the closed form in L11.html:137. Key-results rows and cards mirror each other (grade and basis).")
row("C-56", "2.9 why-it-matters, hub links, lesson navigation", "L09.html:52,452-453; L10.html:52,451-452; L11.html:52,500-502; index.html:153-155", P,
    "Why-it-matters paragraphs read; navigation L09 (prev L08, next L10), L10 (prev L09, next L11), L11 (prev L10). Hub cards index.html:153-155 show L09 10 h, L10 8 h, L11 7 h.")
row("C-57", "2.7 card CS2-c236 hypotheses (round-2 FAIL)", "cards.json:1385 (CS2-c236)", P,
    "Hypotheses listed (sorted buffer, even-numbered items kept, c items at most v) are those of the Theorem 2.4 proof (L11.html:113). Statement 0 or -2^h re-derived.")
row("C-58", "2.4/2.9 L11 Section 3 bullet 3 and Problem P3: hypothesis n >= 1 (round-2 FAIL)", "L11.html:267; L11.html:335-338", P,
    "Section 3 bullet 3 states 1 <= n < k_0 and the eps = 0 extension; P3 (L11.html:336) states 1 <= n < k_0. Both consistent with the proof (no compaction, E = 0).")
row("C-59", "2.7 card is not trivia (round-2 FAIL): CS2-c195", "cards.json (CS2-c195, absent)", P,
    "CS2-c195 is absent from cards.json at the pin (no card left to check).")
row("C-60", "2.7 card is not trivia (round-2 FAIL): CS2-c199", "cards.json (CS2-c199, absent)", P,
    "CS2-c199 is absent from cards.json at the pin (no card left to check).")
row("C-61", "2.9 cross-reference: L11 eps=0 extension 'Section 3, Misconception 2' (round-3 FAIL)", "L11.html:65", P,
    "L11.html:65 says the eps = 0 case is used in Section 3, Section 4 (Misconception 2) and Problem P3. Section 3 bullets 1 and 3 (L11.html:265, 267), Misconception 2 (L11.html:280) and P3 (L11.html:338) do use it.")
row("C-62", "2.9 cross-reference: L11 'Section 3 says what that check does' (round-3 FAIL)", "L11.html:140", P,
    "L11.html:140 now says 'the interpretation after Lab 1 says what that check does and does not show'; the interpretation is at L11.html:259.")
row("C-63", "2.7 trivia (BUILDER_RULES 7): cards whose whole answer is one printed reading of Lab 1", "cards.json:841 (CS2-c124), 1217 (CS2-c194), 1233 (CS2-c200), 1354 (CS2-c231), 1370 (CS2-c234)", F,
    "Five cards are a single printed reading of Lab 1 with no mechanism: c124 'Exactly 0.0, although the exact sample variance is 0.087281 as printed'; c194 'Yes. It is 9.258e-16 at offset 0, 8.852e-11 at offset 10^6 and 7.449e-08 at offset 10^9'; c200 'Yes, at both epsilons (Lab 1)'; c231 'Yes. The totals lie between 396 and 399 across the five windows'; c234 'Its largest size is 10, below the window size of 30, on the lab series'. The round-3/4 fixers removed the same class (c123, c136, c154, c193). Each value is correct (C-47 and C-27) and each grade is C with basis, so only the card style fails.",
    "Rewrite or delete each as a mechanism or a checkable result, for example c124 -> 'Why is the naive estimate exactly 0.0 at offset 10^9?' (answer: the rounding of the two running sums exceeds S_n, L09 E1); c200 and c231 -> delete (already in the key-results rows); c194 and c234 -> delete or rewrite around the mechanism. Keep basis and grade C.")
row("C-64", "2.6 mutation testing (project graders only)", "tests/labs/CS2/lab-CS2-L09-1.py, L10, L11", P,
    "Not applicable to lesson pages and lab twins (VERIFIER_RULES 2.6 and the ruling: mutation testing applies to project graders only). The slice contains no grader; no mutant is listed.")
row("C-65", "2.3 grade of CS2-c150 (capacities) against BLUEPRINT 3 and ruling 13", "cards.json:1018 (CS2-c150); L11.html:75, 299, 356", P,
    "Grade T now. The capacities are direct evaluations of Definition 2.1 (k_h = 2 ceil((h+1)(h+2)/(2 eps))), worked by hand in Problem M1 (eps = 1/10, L11.html:299) and in the E2 solution (eps = 1/20: 40, 120, 240, L11.html:356). Ruling 13 (a value derived by hand in a numbered Example is T with the Example as basis) is met; the card names M1 for the eps = 1/10 values.")
row("C-66", "2.7 attribution of the closed form to Corollary 2.6 (card c151 and L11 why-it-matters)", "cards.json:1025 (CS2-c151); L11.html:52, 131, 137", P,
    "Card c151 and L11.html:52 now say 'Corollary 2.6 and its proof' and 'the closed-form bound from the proof of Corollary 2.6'; the formula is derived at L11.html:137 from the Corollary's sum. Attribution correct.")
row("C-67", "2.7 card CS2-c135 front notation", "cards.json:920 (CS2-c135)", P,
    "The front 'Which series makes one insertion remove all w entries of the deque?' has no notation. The back writes x_0 through x_(w-1) in the same plain-text index style as the rest of the deck (for example c116-c120 use x_i). No KaTeX macro is required on a card.")
row("C-68", "2.7 duplicate fact across cards: CS2-c225 and CS2-c118", "cards.json (CS2-c225 removed; CS2-c118)", P,
    "CS2-c225 is absent at the pin; CS2-c118 (Welford's recursion) is the only card for that fact in the L09 deck (full scan, cards_scan_r5.out).")
row("C-69", "2.8 data and labels: no data-files; SIMULATED labels present", "L09.html:218; L10.html:211; L11.html:259; twin docstrings lab-CS2-L09-1.py:1-12, lab-CS2-L10-1.py:1-9, lab-CS2-L11-1.py:1-10", P,
    "grep data-files on L09-L11: 0. SIMULATED appears in L09.html:218, L10.html:211 ('SIMULATED integer series, seeded') and L11.html:259 ('The stream is SIMULATED'). No figure or chart on the three pages (page_smoke sweep found none to sweep).")
row("C-70", "2.9 Section 3 canon-break claims (three bullets per lesson)", "L09.html:224-226; L10.html:217-219; L11.html:265-267", P,
    "Three bullets in each lesson's canon-breaks section, each with a claim and its computation or proof (checked against numbers_r5 and numbers_r5b outputs).")
row("C-71", "2.9 misconceptions (at least 3 per lesson)", "L09.html:233-244; L10.html:226-236; L11.html:274-285", P,
    "Three misconceptions in each lesson (L09: 234, 238, 242; L10: 227, 231, 235; L11: 275, 279, 283), each with the wrong belief, correction and evidence.")
row("C-72", "2.5 lab statements do not overreach (interpretation sentences)", "L09.html:218; L10.html:211; L11.html:259", P,
    "L09.html:218 limits the claim to one stream and one seed and disclaims general stability; L10.html:211 disclaims tightness and time; L11.html:259 disclaims other q and other streams. Unprinted digits in the same paragraphs are C-74.")
row("C-73", "2.9 quiz keys: answers, tolerances and explanations", "L09.html:372-442; L10.html:362-440; L11.html:412-491", P,
    "Numeric keys recomputed: L09 4.5714 (32/7, tol 0.001), 2, 6, 0.25 (tol 0.0005); L10 1, 19, 400, 7; L11 20, 29, 1, 18187. Multiple-choice data-correct options match the page (L09 q1, q4, q6, q8, q9; L10 q1, q4, q6, q7, q8, q10; L11 q1, q3, q6, q7, q8, q10). Explanations cite the right items.")
row("C-74", "2.2 numbers in prose or expected output that the lab does not produce (interpretation and solutions)", "L09.html:218 (2.0000000020427e21, 3.2e6 difference, 0.0872811009301, 174.4749); L09.html:235 and 308 (0.0872811); L09.html:315 (unrounded 0.08728110122738864 and 9.25811790803366e-16)", F,
    "Every value is correct: numbers_r5.out gives exact sum of squares 2.0000000020427e+21, computed-minus-exact -3.23e6, exact variance 0.0872811009301 (13 dp) and 0.0872811 (7 sig), (n-1)*exact variance 174.474921, math.ulp(2e21) 262144.0, unrounded exact variance 0.08728110122738864, unrounded relative error 9.25811790803366e-16, product 8.080587e-17. But twin_L09.out prints none of them (only 0.087281 at 6 digits and the relative errors at 3 digits), and the page does not derive them. Under VERIFIER 2.2(a) a number must be produced by a lab or shown as a calculation.",
    "Either print these values in lab-CS2-L09-1.py (exact sums of squares, the computed running sum, the 13-digit exact variance, the unrounded relative error) and re-embed with tools/embed_labs.py --refresh lab-CS2-L09-1, or restate the prose with the printed digits (0.087281, about 2 x 10^21, about 174.5, about 8.1 x 10^-17 for the E2 product).")

frag = {
  "unit": "CS2", "slice": "c", "round": 5,
  "verifier": "Haiku independent verifier, CS2-c round 5 (delta verification; did not build CS2; no builder context)",
  "pin": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
  "base": "edbb7aa8de20e6d2f3035c463a79a318c22623c4 (round-4 pin; round-4 fragment /Users/billyribeiro/.fanout/frags/S-CS2-c.round4.json, read as context only)",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyS5-CS2-c (detached at dde0486b; .venv symlinked; vendor copied)",
  "scratch": "/tmp/cs2c-r5 (working copies); every script and output that backs a row is kept in ledgers/CS2/scripts/CS2-c-r5/",
  "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
  "verdict": "FAIL",
  "rows": rows,
  "mutants": [],
  "registry_flags": [],
  "freshness_flags": [],
  "notes": (
    "Delta edbb7aa8..dde0486b for the slice, every hunk read: L09.html:226 (canon bullet 3 wording: must raise an error rather than return 0); L10.html:52 (why-it-matters now cites Definition 1.1); L11.html:52 (why-it-matters reworded; the closed-form attribution to 'the proof of Corollary 2.6' is now correct); L11.html:144 (hypothesis now states that both inequalities are checked, so excess and deficit are each held to eps; checked against the assertion at lab-CS2-L11-1.py:99-108); L11.html:363 (E3 solution: stored counts 500 and 220 are count-determined; checked on four streams). Cards in the delta: c135 back, c150 (now T), c151 back, removed c123, c136, c154, c193, c225 (L09-L11), plus changes outside the slice (c103, c229, c241-c243, c006-c057, c218). The twins L09-L11 are byte-identical across the delta. Every previous non-PASS row (C-63, C-65, C-66, C-67, C-68) was re-verified from scratch; every row was re-run on the pin, so no PASS row is carried. Ruling 26 is noted for the orchestrator: the three FAIL rows are LOW (C-53 card duplicate, C-63 card style, C-74 presentation of unprinted digits); no blocking row (no false or unproved statement, missing hypothesis, wrong number, over-graded claim, failing gate, surviving non-equivalent mutant, or lab statement the code does not support) was found. Under VERIFIER_RULES section 4 the verdict is FAIL because a FAIL row exists. Mutants: none, since mutation testing applies to project graders only (no grader in this slice). Not checked: (a) the live verify_refs run for CS2 (it is a network run; the slice cites no key); (b) render_curriculum.py --check and the full site build beyond build_site.py --check; (c) hub index.html beyond the hours and card-link lines; (d) lesson L01-L08, cards of other lessons and the project (other slices); (e) lab code lines inside the three pages were checked by run_labs byte-equality, not by eye; (f) visual screenshots (page_smoke geometry only; there are no figures on these pages); (g) pytest run for the full suite (subsets only); (h) run_graders (no project grader in this slice)."
  ),
  "summary": "CS2 slice c, round 5 (L09-L11, twins, cards), pin dde0486b. 74 rows: PASS 71, FAIL 3 (all LOW, none blocking). Gates on the pin all PASS: check_pages (unit, each page, --all), check_dag (unit, --all), check_projects, run_labs (L09, L10, L11 and unit 14/14), twins under -I -W error, page_smoke L09/L10/L11, ruff, mypy --no-incremental (385 files), pytest subsets (69 + 3), verify_refs --offline (560 entries, 0 problems), build_site --check. Round-4 FAILs C-65, C-66, C-67, C-68 are now PASS; C-63 remains FAIL for five trivia cards (c124, c194, c200, c231, c234)."
}
out = "ledgers/CS2/CS2-c.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(frag, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("wrote", out, len(rows), "rows")
