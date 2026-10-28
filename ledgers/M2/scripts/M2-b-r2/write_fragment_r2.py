"""Writes ledgers/M2/M2-b.json (round 2, slice M2-b). Rows and evidence as recorded by the verifier."""
import json
import sys
from datetime import datetime, timezone

P = "PASS"
F = "FAIL"
CARRY = "Carried from round 1 (%s byte-identical since the previous pin):"

R1_PAGES = "the cited blocks of course/modules/M/M2/%s.html (hunks of git diff c11ae01..1817191 at other lines only)"

rows = []

def row(rid, check, location, status, evidence):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})

# Commands, re-run on pin 1817191
row("M2b-cmd-check_pages", "tools/check_pages.py --unit M2 --page Lnn, nn = 07..12",
    "tools/check_pages.py; course/modules/M/M2/L07.html to L12.html", P,
    "Re-run on the pin: check_pages M2 L07: PASS, L08: PASS, L09: PASS, L10: PASS, L11: PASS, L12: PASS (each printed on its own line).")
row("M2b-cmd-check_dag", "tools/check_dag.py --unit M2", "tools/check_dag.py; concept links in the six pages", P,
    "Re-run: 'check_dag M2: PASS'. git diff c11ae01..1817191 adds 0 lines containing data-concept or class=\"concept\" in L07-L12, so the concept links are unchanged.")
row("M2b-cmd-run_labs", "tools/run_labs.py --unit M2", "tools/run_labs.py; ledgers/M2/scripts/M2-b-r2/run_labs.txt", P,
    "Re-run: 'run_labs M2: PASS (27/27)', exit 0.")
row("M2b-cmd-twins-isolated", "each slice twin under python -I -W error in isolation",
    "tests/labs/M2/lab-M2-L07-1.py to lab-M2-L12-1.py", P,
    "Re-run from /tmp with env -i: return codes 0 for L07, L08, L09, L10, L11, L12. Twins unchanged since the previous pin (git diff c11ae01..1817191 touches no file under tests/labs/M2/ for these six).")
row("M2b-cmd-page_smoke", "tools/page_smoke.py --unit M2 --pages L07..L12",
    "tools/page_smoke.py; ledgers/M2/scripts/M2-b-r2/page_smoke.txt", P,
    "Re-run: each of the six pages 'page_smoke modules/M/M2/Lnn.html: PASS', 'page_smoke M2: PASS', exit 0.")
row("M2b-cmd-ruff-mypy", "ruff check, ruff format --check and mypy --no-incremental on the six twins",
    "tests/labs/M2/lab-M2-L07-1.py to lab-M2-L12-1.py", P,
    "Re-run: ruff check 'All checks passed!'; ruff format --check '6 files already formatted'; mypy 'Success: no issues found in 6 source files'.")
row("M2b-citations-none", "no registry key cited in the slice pages",
    "course/modules/M/M2/L07.html to L12.html", P,
    "grep -c -E 'data-cite|spivak|hubbard|velleman' returns 0 for each of the six pages. Each page's references section says no registry key is cited; L08 line 345 states this. No citation to verify live (verify_refs --unit M2 has nothing to check for this slice).")
row("M2b-embed-output", "printed-output blocks match a real run of each twin",
    "course/modules/M/M2/L07.html to L12.html; ledgers/M2/scripts/M2-b-r2/ (embed_match.py from M2-b-r1)", P,
    "embed_match.py with /tmp/m2-v/b2/twinNN.txt (real run output): L07 43/43, L08 17/17, L09 22/22, L10 26/26, L11 10/10, L12 21/21 lines found verbatim.")
row("M2b-embed-code", "code blocks match the twin files",
    "course/modules/M/M2/L07.html to L12.html vs tests/labs/M2/lab-M2-Lnn-1.py", P,
    "embed_match.py with the twin as second argument: L07 100/100, L08 66/66, L09 73/73, L10 66/66, L11 46/46, L12 60/60 twin lines found.")
row("M2b-hours", "declared hours and hub split arithmetic",
    "course/modules/M/M2/L07.html to L12.html (data-hours); course/modules/M/M2/index.html (data-hours-lessons, data-hours-project)", P,
    "Each of L07 to L12 has data-hours=10 (6 of 6 pages, grep). Hub data-hours-lessons=240 (24 x 10) and data-hours-project=60, sum 300, which equals the curriculum block hours of 300 (plans/M2-build-plan.md section 0). Pace not judged (architect ruling).")
row("M2b-grades", "every graded claim T with proof or read-off C naming the lab",
    "course/modules/M/M2/L07.html to L12.html (data-grade spans; Key results tables)", P,
    "Changed grade-bearing blocks re-read: L07 Key-results rows (Prop 1.4 T with proof; Lab 1 part A check says 27 pairs of x and k, matching the twin's 3 x 9 = 27 checks), L08 Thm 2.1/Cor 2.2 proofs present, L10 Cor 3.1 proof, L11 Lemma 1.1 proof present. No graded claim relies on a SIMULATED lab reading.")
row("M2b-banned-phrases", "banned phrases and scope words (BUILDER_RULES 1.2/1.3)",
    "course/modules/M/M2/L07.html to L12.html; text from ledgers/M2/scripts/M2-b-r1/extract_text.py", P,
    "grep -i for roughly, about <number>, historically, it is important, studies, typically, generally, usually: no hit in learner text. The remaining ellipses are quiz-stem cloze (L07 lines 392-439, L10 294-334, L08 289-332, L12 305-312) and the lab docstring 'n = 1, 2, 4, ..., 128' in L09 (sequence notation, every printed row 1..128 appears in the output table). Scope words in changed sentences were each checked against a computation (see the numbers, math and lab rows).")
row("M2b-process-words", "no process words in learner text",
    "course/modules/M/M2/L07.html to L12.html", P,
    "grep -i for builder, verifier, round, REQUEST, unit report over the extracted text: no hit.")
row("M2b-structure", "template sections, misconception count, why-it-matters length <= 120 words",
    "course/modules/M/M2/L07.html to L12.html", P,
    "why-it-matters word counts (re-counted from the current pages): L07 106, L08 94, L09 107, L10 118, L11 96, L12 110 (limit 120). Each page has 3 class=\"misconception\" items. check_pages PASS for all six.")
row("M2b-math-L07", "re-derive propositions, lemmas, examples and proofs of L07",
    "course/modules/M/M2/L07.html (Prop 1.4, Lemma 1.6, Ex 1.5, Prop 2.3, Thm 3.2, Ex 2.4, Ex 4.1, Prop 4.2, Remark 2.2, Section 5, problems)", P,
    "Changed parts re-derived: Prop 4.2 proof (g'(h)=2|h|, one-sided quotients +2 and -2, and 'Proposition 2.2 of Lesson 3' checked: the M2 L03 page's Proposition 2.2 is the two-sided limit needs both one-sided limits); Section 5 bullets: |x|>=1 gives |error| >= 1/|1-x| (x^(n+1) has absolute value >= 1); Matching-derivatives bullet with h(x)=T_n+x^(n+1) checked. Unchanged blocks: " + (R1_PAGES % "L07") + " carried from round 1.")
row("M2b-math-L08", "re-derive L08 theorem, corollary, examples and remark",
    "course/modules/M/M2/L08.html (Thm 2.1, Cor 2.2, Ex 2.3, Ex 2.4, Remark 3.3, problems)", P,
    "Changed sentences re-checked: Example 2.3 closed form solves (1-xi)^(n+2)=1-x, which is the Lagrange equality with f^(n+1)=(n+1)!/(1-t)^(n+2) (exact remainder x^(n+1)/(1-x)); Remark 3.3 values 5.625, 8.4375, 0.9, 0.54 recomputed (python, round-2 script). Thm 2.1 proof and Cor 2.2 proof unchanged since round 1 (" + (R1_PAGES % "L08") + ").")
row("M2b-math-L10", "re-derive L10 theorems, corollary, examples and problems",
    "course/modules/M/M2/L10.html (Thm 1.2, Thm 2.1 proof, Ex 2.2, Cor 3.1, Ex 3.2, Prop 4.1, problems)", P,
    "Cor 3.1 k=0 case now 'F(x)=x, F'=1' and k>=1 case by monotonicity of t^k - s^k = (t-s) sum t^(k-1-j) s^j on 0<=s<=t, integrable on [a,b] with 0<=a (Lesson 9, Thm 2.2); the power-rule citation (Lesson 7, Example 1.3) states the rule for positive integer exponents, and k=0 is handled directly. Problem 'F and G antiderivatives' (F-G constant on (a,b), continuity at a and b gives equality) and problem 'F nondecreasing derivative bounds' ((b-a)f(a) <= F(b)-F(a) <= (b-a)f(b) by MVT and monotone f) re-derived. The intro hypothesis gap is a separate row (M2b-L10-intro-hypotheses).")
row("M2b-math-L11", "re-derive L11 lemmas, corollaries, theorems and examples",
    "course/modules/M/M2/L11.html (Lemma 1.1, Cor 1.2, Thm 2.1, Ex 2.2, Thm 3.1, Ex 3.2-3.3, problems)", P,
    "Lemma 1.1 (sum and scalar multiple): epsilon-argument on the common refinement R re-derived; the bracket |int(f+g)-int f - int g| < 2 epsilon and the c<0 swap of U and L are valid. Changed problem solution: N^2 >= 666667 gives N >= 817 and 2/(3*816^2) = 1.0012175e-6 (round-2 script), N=817 gives 9.98768e-7. Residual 8/3 - 2.6666666663 = 4e-10 consistent with the page's 4e-10 (10-digit display). Unchanged blocks: " + (R1_PAGES % "L11") + ".")
row("M2b-math-L12", "re-derive L12 definitions, lemmas and theorems, and the research problem",
    "course/modules/M/M2/L12.html (Def 1.1, Remark 1.2, Lemma 2.1, Thm 2.2, Lemma 3.1, Lemma 3.2, Thm 3.3, Research problem p-series)", P,
    "Thm 2.2: F=-1/((p-1)x^(p-1)), F'=x^(-p) re-derived (w'=(p-1)^2 x^(p-2), F'=w'/w^2). Lemma 3.1 terms >= 1/2^(m+1). Research problem: lower sum L = sum_{k=2}^N k^(-p) <= int_1^N x^(-p) <= 1/(p-1), so partial sums bounded for integer p >= 2 (page states p >= 2 at the Key results and intro). Changed items re-checked: Misc 2 'Each integral' bullet fails (see M2b-L12-each-integral-scope). Carried from round 1 for the unchanged blocks: " + (R1_PAGES % "L12") + ".")
row("M2b-numbers-L07", "displayed numbers recomputed from unrounded values",
    "course/modules/M/M2/L07.html Research/Problem 'The error ratio in the lab table' solution (line ~453); Section 2 example 10/7 - 1.3 = 9/70 and 2.5307e-6", P,
    "Re-run ledgers/M2/scripts/M2-b-r2/recompute_numbers_r2.py: 0.0010414286/0.0034714286 = 0.300000005761 (the page's 0.300000006 is this to 9 decimals; agreement to 8 significant figures, consistent with the 10-decimal display). (3/10)^11/(7/10) = 2.53067e-6 -> 2.5307e-6 (five significant figures). The earlier wrong claim 'to ten digits' is removed.")
row("M2b-numbers-L08", "displayed numbers recomputed from unrounded values",
    "course/modules/M/M2/L08.html Ex 2.3 / Ex 2.4 / Remark 3.3 / Empirical rows / quiz", P,
    "Re-run: 1-(3/4)^(1/4) = 0.0693951; (1/2)^(1/5) = 0.8705506 so xi = 0.1294494; 0.7^(1/7) = 0.9503228 so xi = 0.0496772, which the lab prints as 0.049677; 8.4375 and 5.625 and 0.9 and 0.54 recomputed (Remark 3.3); 4/27 = 0.148148 and 1/12 = 0.083333 (Example 4.x problem) recomputed.")
row("M2b-numbers-L09", "displayed numbers recomputed from unrounded values",
    "course/modules/M/M2/L09.html Section 4 bullets, Empirical rows, problem 'How many parts for a tolerance'", P,
    "Re-run: U_128 = 33153/98304 = 0.337249756 (printed 0.33724976); U_128-1/3 = 385/98304; 25/384 = 0.06510417; 1/3072 = 0.00032552; 151/15000 = 0.010067; 154/15606 = 0.009868 (n = 51 gives (3n+1)/(6n^2) = 0.0098680 < 0.01 and n = 50 gives 0.0100667 > 0.01, so 51 is the least n); 1/n <= 0.01 iff n >= 100. Lab part B mesh 0.19 with 10 subintervals: sum of widths 1, mesh = max (i/10)^2 - ((i-1)/10)^2 = 0.19.")
row("M2b-numbers-L10", "displayed numbers recomputed from unrounded values",
    "course/modules/M/M2/L10.html Empirical 'Expected size of the central-difference error', Empirical gap rows", P,
    "Re-run (round-2 script, 60-digit Decimal): truncation error h^2 F'''(0.3)/6 = 3.501E-13 matches the page's 3.5e-13. Lab part B 0.49707921 and 0.50293859, difference 0.00585938 vs 3/512 = 0.005859375 consistent with the printed digits (carried from round 1 for the unchanged Empirical blocks).")
row("M2b-numbers-L11", "displayed numbers recomputed from unrounded values",
    "course/modules/M/M2/L11.html Problem 'number of midpoint parts' solution (N = 816 and N = 817 values)", P,
    "Re-run: 2/(3*816^2) = 1.0012175e-6, which rounds to 1.0012 x 10^-6 (the page now says 1.0012); 2/(3*817^2) = 9.98768e-7 -> 9.988e-7; smallest N with 2/(3N^2) <= 1e-6 is 817. Round-1 FAIL (1.0011) is fixed.")
row("M2b-numbers-L12", "displayed numbers recomputed from unrounded values",
    "course/modules/M/M2/L12.html Empirical, Misconceptions, Key results", P,
    "Re-run: 1/3072 = 0.00032552 (L12 shows 0.00032552 in the part C printed table); H_16384 - 1 = 9.28130671 (lab part C prints 9.28130671, above the bound 7 at m = 14); 1/b and 1/(2b^2) exact in the 10-decimal display (lab part A and B output).")
row("M2b-lab-L07", "lab intro, part descriptions and docstrings vs the code and output",
    "course/modules/M/M2/L07.html Misconceptions item 2 and the lab intro; tests/labs/M2/lab-M2-L07-1.py", P,
    "Round-1 FAIL fixed. Page now says Lab 1 part A checks the closed form against the recursion at x = 3/10, -1/2, 9/10 (code: POINTS_A and derivative_by_recursion; printed 'part A: formula equals recursion at all 27 checks (x in 3/10, -1/2, 9/10; k = 0 to 8)') and that part B builds T_n from the closed form at 0 (code: taylor_poly uses derivative_formula(k, 0)). Output 'part A' line matches. Part D docstring matches output (quotients 2 and -2).")
row("M2b-lab-L08", "lab intro, part descriptions and docstring vs code and output",
    "course/modules/M/M2/L08.html lab intro and part B description; tests/labs/M2/lab-M2-L08-1.py docstring", P,
    "Intro: 133 points (part A) = 19 x 7; 70 points for part B (x <= 1/2, k=1..10, n=0..6 = 70); table rows of part C (x = 0.30 at n=5 gives xi 0.049677 and remainder 0.00104143; x=0.90 at n=1 gives 8.10000000 and xi 0.535841, matching card M2-c107). Output matches code. Unchanged intro block carried from round 1.")
row("M2b-lab-L09", "lab intro and the page's description of Lab 1 part B against the code",
    "course/modules/M/M2/L09.html Section 4 bullet 2 (line 266) and the lab intro (line 97); tests/labs/M2/lab-M2-L09-1.py part_b", P,
    "Code part_b: points = [(i/n)^2 for i in range(n+1)] with n = 10, so 10 subintervals and 11 points; mesh 0.19 printed 'mesh = 0.19000000'. Page now says '10 subintervals (11 points)'. Round-1 FAIL fixed.")
row("M2b-lab-L10", "lab intro and part descriptions vs code and output",
    "course/modules/M/M2/L10.html lab intro; tests/labs/M2/lab-M2-L10-1.py", P,
    "Intro block and twin unchanged since the previous pin (the L10 hunks are at lines 52, 105, 250, 320, 356, none in the lab intro). Re-run output 'part A' Riemann bracket and part B 'U_128 - L_128 = 0.00585938' consistent (see numbers row).")
row("M2b-lab-L12", "lab intro and the paragraph 'Parts A and B use exact fractions' vs code and output",
    "course/modules/M/M2/L12.html lab intro and paragraph at its line 148; tests/labs/M2/lab-M2-L12-1.py", P,
    "Re-run output: part A 0.9999 with error 0.0001, b times error 1.0000 at b=10, 100, 1000, 10000; part B b^2 times error 0.5000; part C H_N - 1 >= m/2 for m=1..14 with 'True' on each row. Paragraph and code (Fraction in parts A and B) match. Intro and paragraph lines unchanged since the previous pin.")
row("M2b-L09-lab-prints", "page claim 'which Lab 1 prints' vs part_a",
    "course/modules/M/M2/L09.html line 265 (Section 4 bullet 1)", P,
    "Page now: 'Lab 1, part A asserts this formula and prints U_128 = 0.33724976'. part_a asserts U_n - 1/3 = (3n+1)/(6n^2) (raise on mismatch) and prints U_128 0.33724976 (run output). Round-1 FAIL fixed.")
row("M2b-L09-intro-scope", "intro scope: Corollary 2.3 hypotheses",
    "course/modules/M/M2/L09.html why-it-matters paragraph (line 52)", P,
    "Intro now says 'bounds the error of a Riemann sum (Section 1) of a monotone function by the mesh times the total change of the function (Corollary 2.3)', which carries the monotone hypothesis of Corollary 2.3. Round-1 FAIL fixed.")
row("M2b-L09-s4-no-equal", "universal claim 'Upper and lower sums ... do not equal it' (Section 4 bullet 1)",
    "course/modules/M/M2/L09.html Section 4 bullet 1", P,
    "Bullet now reads 'Upper and lower sums bracket the integral.' and gives x^2 with no equality claim beyond 'they do not equal it at any finite n (Example 3.2)', which holds since U_n - 1/3 = (3n+1)/(6n^2) > 0 and L_n - 1/3 = -(3n-1)/(6n^2) < 0 for all n >= 1. Round-1 FAIL fixed.")
row("M2b-L09-p-overstate", "problem 'How many parts for a tolerance' solution",
    "course/modules/M/M2/L09.html problem 'How many parts for a tolerance' solution", P,
    "Solution now says the bound 1/n needs n >= 100 (sufficient), and separately that the Riemann sums of the uniform partition lie in [L_n, U_n] and 1/3 lies there too, so |R - 1/3| <= max(U_n - 1/3, 1/3 - L_n) = (3n+1)/(6n^2) < 0.01 for n = 51. Re-derived: monotone f makes every tag value lie in [m_i, M_i]. Round-1 FAIL fixed.")
row("M2b-L09-numbers-ok", "L09 lemmas, Theorem 2.2, Corollary 2.3, examples, problems re-derived",
    "course/modules/M/M2/L09.html Lemma 1.1, Lemma 1.2, Def 1.3, Thm 2.2, Cor 2.3, Ex 3.2, Lemma 3.1, problems", P,
    "Re-derived: refinement inequalities; Lemma 1.2 via common refinement; Thm 2.2 telescoping and integrability bound n > (b-a)|f(b)-f(a)|/eps; Cor 2.3; Ex 3.2 (U_n, L_n, U_n - L_n = 1/n); x(1-x) at n=2 gives 1/8 and 1/8 with integral 1/6 by Lesson 10 Thm 2.1; problems 'x on [0,2]' (U=5/2, L=3/2), 'x^3 on [0,1]' (9/16, 1/16), '1/(1+x)' (5/6, 7/12, 1/4); Lemma 3.1 induction algebra (n+2)(2n+3) = 2n^2+7n+6.")
row("M2b-L07-tangent-xref", "Remark 2.2 cross-reference and card M2-c082",
    "course/modules/M/M2/L07.html line 114 (Remark 2.2); course/modules/M/M2/cards.json M2-c082", P,
    "The phrase 'tangent line of Lesson 4' is removed: Remark 2.2 now says 'where f'(0) is the derivative of Lesson 4 at the point 0', and Lesson 4 Definition 1.1 defines the derivative at a point (course/modules/M/M2/L04.html, extracted). grep -i tangent returns no hit in L07 to L12. Card M2-c082 matches. Round-1 FAIL fixed.")
row("M2b-L07-term-before-def", "terms used before definition (Taylor polynomial)",
    "course/modules/M/M2/L07.html why-it-matters (line 52) and Definition 2.1 (Section 2)", P,
    "Why-it-matters now reads 'A Taylor polynomial (Definition 2.1, in Section 2)', an explicit forward pointer to the definition; the term is registered in the page's Introduces line as a term of prose. Round-1 FAIL fixed.")
row("M2b-L07-heading-sign", "problem title vs problem content (E3)",
    "course/modules/M/M2/L07.html problem 'The sign of the degree-10 error at three points'", P,
    "Title changed from 'Where the error at degree 10 changes sign' to 'The sign of the degree-10 error at three points'. Solution signs re-derived: x^11/(1-x) at 3/10 positive, at -1/2 negative (numerator negative, 1-x > 0), at 2 negative (1-x = -1). Lab prints 0.0000025307 (part B) and -2048 (part C); it prints no value at -1/2, which the page says. Round-1 FAIL fixed.")
row("M2b-L08-scope-only", "universal 'only' claim in why-it-matters",
    "course/modules/M/M2/L08.html why-it-matters (line 52)", P,
    "Sentence now reads 'the approximation is controlled when its error can be bounded (Corollary 2.2)', no universal 'only'. Round-1 FAIL fixed.")
row("M2b-L08-notation", "undefined x_j in Misconception 1",
    "course/modules/M/M2/L08.html Misconception 1 (line 257)", P,
    "Now reads 'between x_0 and y_j', and y_j is defined in the Theorem 2.1 proof (y_0 = x, y_{j+1} strictly between x_0 and y_j). Round-1 FAIL fixed.")
row("M2b-L10-mvt-endpoints", "continuity needed on the closed interval (Section 5 bullet 2)",
    "course/modules/M/M2/L10.html line 250 (Section 5 bullet 2); card M2-c143", P,
    "Now: MVT applied on each closed subinterval [x_(i-1), x_i] whose endpoints include interior points x_1 to x_(n-1), so F must be continuous at every point of [a,b]. Consistent with the theorem's hypothesis 'F continuous on [a,b]' (Theorem 2.1, line 47). Card M2-c143 agrees. Round-1 FAIL fixed.")
row("M2b-L10-intro-limit-of-sums", "why-it-matters: 'Lesson 9 defined the integral as a limit of sums'",
    "course/modules/M/M2/L10.html line 52", P,
    "Now: 'Lesson 9 defined the integral as the common value of the supremum of lower sums and the infimum of upper sums', which is Lesson 9 Definition 1.3 (I_* and I^*). Round-1 FAIL fixed.")
row("M2b-L10-cor31-citation", "Corollary 3.1 proof citation (Lesson 7, Example 1.3)",
    "course/modules/M/M2/L10.html line 105 (proof of Corollary 3.1)", P,
    "Now: 'power rule for positive integer exponents (Lesson 7, Example 1.3 ...)' with k=0 handled directly by F(x)=x, F'=1. Lesson 7 Example 1.3 (course/modules/M/M2/L07.html line 40) states the rule for positive integer exponents. Round-1 FAIL fixed.")
row("M2b-L10-intro-hypotheses", "why-it-matters states the fundamental theorem's hypotheses (line 52)",
    "course/modules/M/M2/L10.html line 52 (why-it-matters); Theorem 2.1 statement at line 47", F,
    "Intro says 'if a function F has derivative f and f is integrable, then the integral of f ... is the change in F across it', and names only integrability as 'the hypothesis that is easy to forget'. Theorem 2.1 also requires F continuous on the closed interval [a,b] (line 47), and Section 5 bullet 2 gives that as a second easy-to-forget hypothesis. Fix: state 'F continuous on [a,b] and differentiable with derivative f on (a,b), and f integrable' in the intro, or name both hypotheses.")
row("M2b-L11-misc3-only", "Misconception 3: 'proves integrability for polynomials (Corollary 1.2)'",
    "course/modules/M/M2/L11.html line 238 (Misconception 3)", F,
    "Corollary 1.2 (course/modules/M/M2/L11.html, statement at line 41-43) states integrability only on [0, b] with b >= 0 for polynomials. Lemma 1.1 covers sums and scalar multiples, and Lesson 9 Theorem 2.2 covers monotone functions. The sentence 'this lesson proves integrability for polynomials' therefore overstates: it does not cover polynomials on an interval [a, b] with a < 0. Fix: 'for polynomials on [0, b] with b >= 0 (Corollary 1.2)'. Round-1 FAIL was about 'only'; the 'only' is removed but the polynomial scope is not.")
row("M2b-L12-each-integral-scope", "scope bullet: 'Every integral in this lesson is over an interval [a,b] on which the integrand is monotone'",
    "course/modules/M/M2/L12.html line 242 (Misconception 2) vs problem 'An integral at a finite endpoint' at line 353", F,
    "The bullet claims every integral in the lesson is over [a,b] with a monotone integrand and lists [1,b], [2,b], [a,b] with a>0 and [eps,1]. The problem at line 353 defines and uses int_0^1 f = lim_{eps->0+} int_eps^1 f for f = x^(-2), an integral over (0,1] whose integrand is not integrable on [0,1] and is not one of the listed forms. Fix: name the (0,1] case, or drop 'every'. Round-1 FAIL unchanged in substance.")
row("M2b-L12-intro-test", "why-it-matters: 'closes with a test that uses the integral to decide whether an infinite series converges'",
    "course/modules/M/M2/L12.html line 52", P,
    "Now: 'It closes with a research problem that bounds the partial sums of the p-series by an integral, for integers p >= 2', which matches the Research problem 'A series tested by an integral' (line 261-265). Round-1 FAIL fixed.")
row("M2b-cards-dupes", "full duplicate scan of cards (cards.json, 377 entries; script ledgers/M2/scripts/M2-b-r1/card_dupes.py)",
    "course/modules/M/M2/cards.json M2-c099 (line 686) and M2-c134 (line 933), restating M2-c065 (line 448) and M2-c066 (line 455)", F,
    "No exact duplicate fronts or backs. The scan finds two cross-lesson restatements of the same theorem with the same hypotheses and conclusion: Rolle's theorem (M2-c099, L08 Theorem 1.2, vs M2-c065, L06 Theorem 2.2) and the mean value theorem (M2-c134, L10 Theorem 1.2, vs M2-c066, L06 Theorem 2.3). Fix: retire one card of each pair, or make the L08 and L10 card ask about its use in that lesson (the Remark 1.3 and Remark 1.3 wording).")
row("M2b-cards-L07", "cards M2-c075 to M2-c096 vs L07.html", "course/modules/M/M2/cards.json M2-c075 to M2-c096", P,
    "Changed cards M2-c081 (T_n back: 'k = 0, 1, up to n') and M2-c082 (T_1 back: 'derivative of Lesson 4 at 0') agree with L07 Definition 2.1 and Remark 2.2. Unchanged cards re-read against the lesson: c085 0.0000025307 and -2048 printed in part B and C; c093 27 checks; c094 g''(0) does not exist; c096 approximation holds for |x| < 1.")
row("M2b-cards-L08", "cards M2-c097 to M2-c114 vs L08.html", "course/modules/M/M2/cards.json M2-c097 to M2-c114", P,
    "Changed card M2-c099 (front 'Remark 1.3: where is the proof of Theorem 1.2 given?', back: proof in Lesson 6, EVT assumed) matches L08 Remark 1.3 and L06 line 43. Other cards re-read: c104 ratio 2^(n+2)(1-x) in [2^(n+1), 2^(n+2)); c107 R_1(0.9) = 8.1 and xi = 0.535841 (lab part C rows); c110 limit iff x < 1/2.")
row("M2b-cards-L09", "cards M2-c115 to M2-c132 vs L09.html", "course/modules/M/M2/cards.json M2-c115 to M2-c132", P,
    "Changed cards M2-c115 (partition back, 'x_0 < x_1 < ... < x_n' wording only) and M2-c131 (upper and lower sums of x^2 never reach the integral at any finite n, Section 4) agree with L09 Section 4. Unchanged cards: c130 mesh 0.19 with 10 subintervals; c125 U_128 = 0.33724976 and L_128 = 0.32943726 (lab part A table).")
row("M2b-cards-L10", "cards M2-c133 to M2-c147 vs L10.html", "course/modules/M/M2/cards.json M2-c133 to M2-c147", P,
    "Changed cards M2-c134 (Remark 1.3 wording: MVT of Lesson 6, used in that form only) and M2-c143 (continuity on the closed interval, the corrected rationale) agree with the current L10 text. c140 3/(4n) matches the lab part B form (f = 1/(1+x)^2 nonincreasing). The round-1 FAIL on c143 is fixed.")
row("M2b-cards-L11", "cards M2-c148 to M2-c164 vs L11.html", "course/modules/M/M2/cards.json M2-c148 to M2-c164; M2-c163 at line 1142", F,
    "Changed cards c156 and c157 (midpoint values agree with 1/60 and 8/3 to 1e-06) and c163 agree with the lesson text, but c163's back repeats 'proves integrability for polynomials (Corollary 1.2)', whose statement covers only [0, b] with b >= 0 (course/modules/M/M2/L11.html line 43). Fix together with M2b-L11-misc3-only: 'for polynomials on [0, b] with b >= 0 (Corollary 1.2)'. c151 (1/60, 1/30 via Beta-type integral) and c152 re-checked.")
row("M2b-cards-L12", "cards M2-c165 to M2-c180 vs L12.html", "course/modules/M/M2/cards.json M2-c165 to M2-c180", P,
    "No card in this range changed since the previous pin. Carried from round 1 (the cards M2-c165 to M2-c180 byte-identical since the previous pin; the lesson blocks cited by them are unchanged except the intro and misconception 2, which the cards do not quote): all 16 cards re-read against the current L12 text, including c174 (lower sum on the unit partition equals H_N - 1) and c179 (Problem L12-R3 bound 1 + 1/(p-1)).")

# Hunt rows that exist only in round 2
verdict = "FAIL" if any(r["status"] != P for r in rows) else "PASS"
frag = {
    "unit": "M2",
    "slice": "M2-b",
    "round": 2,
    "round_note": "round 2 (re-verification after the batch 2 fixes at 1817191); previous pin c11ae01; round 1 fragment /tmp/fanout-frags/B-M2-b.round1.json used as context only",
    "verifier": "Haiku 5.5 independent verifier (M2-b round 2)",
    "pin": "1817191",
    "base": "c11ae01",
    "checkout": "/tmp/verifyB2-M2-b",
    "scratch": "/tmp/m2-v/b2",
    "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "verdict": verdict,
    "scripts_dir": "ledgers/M2/scripts/M2-b-r2/",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Lab slice: no project grader, so no student-error mutants are written (architect ruling: mutation testing applies to project graders only). ledgers/M2/mutants/ is the project verifier's directory and was not touched.",
        "Architect ruling on hours applied: pace not judged; only the hub split arithmetic is checked (240 + 60 = 300 = curriculum block hours).",
        "Not checked: live verify_refs for M2 (no citations in this slice); Pyodide timing beyond page_smoke's PASS; visual rendering of pages; the full text of L07 and L08 Example blocks not touched since round 1 was not re-read word by word, only their numbers and the changed sentences.",
        "Two round-1 rows (M2b-numbers-L10, M2b-numbers-L12, M2b-lab-L10, M2b-lab-L12, M2b-hours, M2b-embed-*) are re-run on the pin rather than carried wholesale."
    ],
    "summary": "",
}
frag["summary"] = "%d rows: %d PASS, %d FAIL" % (len(rows), sum(r["status"] == P for r in rows), sum(r["status"] == F for r in rows))
path = sys.argv[1]
with open(path, "w", encoding="utf-8") as fh:
    json.dump(frag, fh, indent=2, ensure_ascii=False)
print(frag["summary"], verdict)
