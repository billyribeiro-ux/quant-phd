# Writes the round-2 fragment for M2-a (pin 1817191). Run from the checkout root:
#   .venv/bin/python -I ledgers/M2/scripts/M2-a-r2/make_fragment_r2.py
import json
import sys
from datetime import datetime, UTC

P = "PASS"
F_ = "FAIL"
rows = []

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)

S = "scripts/M2-a-r2/"
row("M2-a-cmd-pin", "2.9-structure", "repository HEAD; course/modules/M/M2/{index,L01-L06}.html; tests/labs/M2/lab-M2-L01..06-1.py", P,
    "git rev-parse --short HEAD -> 1817191 (detached). Delta from the round-1 pin c11ae01: `git diff --name-only c11ae01 1817191` "
    "lists index.html and L01.html-L06.html of M2 (changed); `git diff --name-only c11ae01 1817191 -- tests/labs/M2 tools references curriculum` is empty, "
    "so the six twins, the tools and the registry are byte-identical to the previous pin. The brief's pin b4590f6 is not the checkout; the fragment records 1817191.")
row("M2-a-cmd-check_pages", "2.9-structure", "tools/check_pages.py --unit M2", P,
    "`.venv/bin/python tools/check_pages.py --unit M2` -> 'check_pages M2: PASS', exit 0 (/tmp/M2-v/a-r2/check_pages.txt).")
row("M2-a-cmd-check_dag", "2.9-structure", "tools/check_dag.py --all", P,
    "`.venv/bin/python tools/check_dag.py --all` exit 0; line 2 'check_dag M2: PASS' (/tmp/M2-v/a-r2/dag.txt).")
row("M2-a-cmd-run_labs", "2.5-lab", "tools/run_labs.py --unit M2; tests/labs/M2/lab-M2-L01..L06-1.py", P,
    "`.venv/bin/python tools/run_labs.py --unit M2` -> 'run_labs M2: PASS (27/27)', exit 0 (/tmp/M2-v/a-r2/labs.txt).")
row("M2-a-cmd-page_smoke", "2.9-structure", "tools/page_smoke.py --unit M2 --pages index L01 L02 L03 L04 L05 L06", P,
    "`.venv/bin/python tools/page_smoke.py --unit M2 --pages index L01 L02 L03 L04 L05 L06` -> PASS for index and L01-L06, 'page_smoke M2: PASS', exit 0; each lab 0.0 s, boot 1.1-1.2 s (/tmp/M2-v/a-r2/smoke.txt).")
row("M2-a-cmd-ruff", "2.5-lab", "tests/labs/M2 (ruff check; ruff format --check)", P,
    "`.venv/bin/python -m ruff check tests/labs/M2` -> 'All checks passed!', exit 0; `ruff format --check tests/labs/M2` -> '27 files already formatted', exit 0 (/tmp/M2-v/a-r2/lint.txt).")
row("M2-a-cmd-mypy", "2.5-lab", "tests/labs/M2 (mypy, strict per pyproject.toml)", P,
    "`.venv/bin/python -m mypy --no-incremental tests/labs/M2` -> 'Success: no issues found in 27 source files', exit 0 (/tmp/M2-v/a-r2/lint.txt).")
row("M2-a-cmd-refs", "2.1-citations", "tools/verify_refs.py --unit M2; tools/verify_refs.py --offline; references/references.json", P,
    "live `tools/verify_refs.py --unit M2` -> 'live re-verification of M2: 2 of 560 entries, 0 problems', exit 0; offline `tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0 (/tmp/M2-v/a-r2/refs_live.txt).")
row("M2-a-cmd-pytest", "2.5-lab", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py (-k 'M2 or m2 or lab')", P,
    "`.venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k 'M2 or m2 or lab'` exit 0, every progress line dots, no F or E (/tmp/M2-v/a-r2/pytest.txt).")
row("M2-a-lab-twins-match", "2.5-lab", "tests/labs/M2/lab-M2-L01-1.py .. lab-M2-L06-1.py; L01..L06.html <code class=language-python> and <pre class=expected>", P,
    f"{S}twin_compare.py (run `.venv/bin/python -I`): each of L01-L06 has one embedded code block and one expected block; embedded==twin True x6; "
    "`python -I -W error` on each twin exits 0; printed stdout == expected block True x6 (/tmp/M2-v/a-r2/twin_compare.txt).")
row("M2-a-lab-L01", "2.5-lab", "tests/labs/M2/lab-M2-L01-1.py; course/modules/M/M2/L01.html lines 87-150", P,
    "Twin output (/tmp/M2-v/a-r2/twin-L01.out): 1.500000/5.000000e-01 at n=1; 1.909091/9.090909e-02 at n=10; least N = 1000; error at 999 = 1.000000e-03, at 1000 = 9.990010e-04. "
    "Hypothesis (line 89) states the same values: 1/2, 1/11, 1/101, N=1000, 1.000000e-3. Interpretation (line 149) C-graded with basis Lab 1. "
    "Docstring (lines 92-96) says the search checks 'for each n from N to 5000 only' and that the every-n claim is proved on the page: matches the code (least_threshold, range to search_limit). "
    f"Recomputed exactly ({S}recompute_r2.py): |a_n-2|=1/(n+1) for n=1..2000; least N=1000; 1/(n+1)<1e-4 iff n>=10000.")
row("M2-a-lab-L02", "2.5-lab", "tests/labs/M2/lab-M2-L02-1.py; course/modules/M/M2/L02.html lines 76-152", P,
    "Output (/tmp/M2-v/a-r2/twin-L02.out) equals the expected block. Hypothesis (line 78): sum error 12/110 ~0.109091, product 32/110 ~0.290909, quotient 54/132 ~0.409091 at n=10; quotient 1.5 at n=1: all recomputed exactly (n=1..500 closed forms, recompute_r2.py). "
    "Interpretation (line 151): 'checks at five indices only', 'at n=10000 the three errors print as 1.000100e-4, 2.999900e-4, 4.998900e-4': matches output. Docstring (lines 81-85) matches code.")
row("M2-a-lab-L03", "2.5-lab", "tests/labs/M2/lab-M2-L03-1.py lines 1-13 and 120; course/modules/M/M2/L03.html lines 115-123 (embedded copy)", F_,
    "Output and numbers match (table 0.810000/2.200000/1.390000 at h=0.1; 0.998001 at h=0.001; gap 1.000400 at h=1e-4; True x3). "
    "But the docstring (twin line 120, embedded at L03.html line ~117-123) says the grid check verifies '|f(x) - 7| < epsilon for lim (3x + 1) = 7'. In the code f is the piecewise function (lines 132-134: x^2 for x<1, 2x otherwise) and the check uses g(x)=3x+1 (lines 137-139, 148-150: `abs(g(x) - 7) < epsilon`). "
    "Read literally, the docstring names the wrong function: at x=2 the piecewise f gives 4, and |f(2)-7| = 3, not below epsilon. The page's own Example 1.2 uses f(x)=3x+1, so the reader meets two meanings of f.",
    "In the twin docstring and in the embedded copy at L03.html, replace '|f(x) - 7| < epsilon' by '|g(x) - 7| < epsilon, where g(x) = 3x + 1', and say the piecewise function is f (or rename g). Then re-embed with tools/embed_labs.py L03.html --refresh lab-M2-L03-1 and rerun twin_compare.")
row("M2-a-lab-L04", "2.5-lab", "tests/labs/M2/lab-M2-L04-1.py; course/modules/M/M2/L04.html lines 67-123", P,
    "Output (/tmp/M2-v/a-r2/twin-L04.out) equals the expected block: 3.310000/3.100000e-01 at h=0.1 ... 3.000003/3.000001e-06 at h=1e-6; error/h at 1e-6 = 3.000001. Hypothesis (line 69) numbers match (3.31, 0.31, 3.000001e-6, 3.000001). "
    "Interpretation (line 122): 'ratio of successive errors tends to 10': error(h)/error(h/10) = (3h+h^2)/(0.3h+0.01h^2) -> 10 (recomputed from the printed table: 10.3, 10.03, ...); PASS.")
row("M2-a-lab-L05", "2.5-lab", "tests/labs/M2/lab-M2-L05-1.py; course/modules/M/M2/L05.html lines 93-168", P,
    "Output (/tmp/M2-v/a-r2/twin-L05.out) equals the expected block: analytic 32.062500000, 0.591836735, 95.062500000; absolute differences 2.350e-07, 3.328e-10, 8.550e-07, all below 1e-6 as the docstring (lines 101-103) and the interpretation (line 167) state. "
    "Hypothesis (line 95): p'=32.0625, q'=29/49 ~0.591837, c'=95.0625, error of order h^2 gives 'order 1e-6 or smaller': all re-derived exactly.")
row("M2-a-lab-L06", "2.5-lab", "tests/labs/M2/lab-M2-L06-1.py; course/modules/M/M2/L06.html lines 113-179", P,
    "Output (/tmp/M2-v/a-r2/twin-L06.out) equals the expected block: 17 grid points; 8 of 16 intervals increasing; 16 of 16 midpoint agreements; f(-1)=2, f(1)=-2. "
    "Hypothesis (line 115): 16 intervals, 4 + 4 increasing, f(-1)=2, f(1)=-2: matches. Interpretation (line 178): midpoints are odd multiples of 1/8, so none is +-1: re-derived.")
row("M2-a-num-hub", "2.2-numbers", "course/modules/M/M2/index.html lines 69-71 (placement), lines 127-133 (skill items)", P,
    "Eight items, six MC and two numeric (count of data-kind). 6/8 = 75 percent, 7/8 = 87.5 percent, 80 percent of 8 = 6.4 so at least 7 correct: all correct. Skill check 1 answer 2: (f(1+h)-f(1))/h = 2+h -> 2 (recomputed). Skill check 2 answer 3.01: (1+h)^3-(1-h)^3 = 6h+2h^3, /(2h) = 3+h^2 = 3.01 at h=0.1 (recomputed exactly).")
row("M2-a-num-hub-hours", "2.2-numbers", "index.html data-hours-lessons=240, data-hours-project=60 (line 29), hours-split (lines 39-42), L01-L06 headers", P,
    "240/(240+60) = 80 percent and 60/300 = 20 percent: the bars at lines 40 (80%, 20%) and the eyebrow '240 h lessons · 60 h project (20%)' agree. Six lesson headers and six hub cards read 10 h (grep 'study hours' and 'L0n · 10 h'): 6 x 10 = 60 of the 240 lesson hours. Arithmetic only (architect ruling: pace not judged).")
row("M2-a-num-L01", "2.2-numbers", "L01.html lines 89, 149, 277-293, 357, 362, 394", P,
    "Every displayed number recomputed from its unrounded value: 1/11=0.0909, 1/101, 1/1000 and 999 at the boundary, 9.990010e-4 = 1/1001 rounded (E1, line 279), E3 1/10000 = 1e-4 (line 293), a_1000 = 2001/1001 = 1.999000999 (quiz, 1.999001), |a_9-2| = 0.1, the threshold N = 3 for 1/0.5 (quiz). All match.")
row("M2-a-num-L02", "2.2-numbers", "L02.html lines 78, 151, 273-289, 371-397", P,
    "Closed forms and values recomputed exactly: sum error at n=10 6/55 = 0.1090909; product error at n=100 302/10100 = 0.02990099 (quiz tolerance 1e-8 contains the exact value); quotient error at n=1 = 3/2; product closed form (3n+2)/(n(n+1)) at n=100 printed 2.990099e-2 (E2 rounding to six digits of the mantissa checked).")
row("M2-a-num-L03", "2.2-numbers", "L03.html lines 114, 172, 266-283, 343-383", P,
    "0.999^2 = 0.998001 (E1); 1 + 4(0.01) - 0.0001 = 1.0399 (E2); gap 1+4h-h^2 at h=0.1 = 1.39 (quiz, tolerance 5e-4); 38 grid points = 2*19 (k=-19..19, k != 0); E3 point x = 2 + 0.095 gives 3*0.095 = 0.285 > 0.1 (recomputed).")
row("M2-a-num-L04", "2.2-numbers", "L04.html lines 69, 122, 236-254, 311-356", P,
    "3+0.3+0.01 = 3.31, error 0.31 (E1); exact error at 1e-5 is 3e-5 + 1e-10 = 3.00001e-5, printed 3.000010e-5 (E2, consistent); error/h = 3+h = 3.000001 at h=1e-6 (E3); Q(0.001)=3.003001 (misconception 3, line 173: 3 + 0.003 + 0.000001). Problem M3 -1/4 recomputed.")
row("M2-a-num-L05", "2.2-numbers", "L05.html lines 95, 167, 176-293", P,
    "p'(1.5) = 32.0625 (2*1.5*3.375 + 3.25*6.75), q'(1.5) = 7.25/12.25 = 29/49 = 0.5918367346 (9 dp 0.591836735, E2), c'(1.5) = 6*1.5*3.25^2 = 95.0625 (E3, Example 2.2). "
    "E1 leading term h^2 p'''/6 with p'''(1.5) = 60*2.25+6 = 141: 1e-8*141/6 = 2.35e-7 (recomputed). Lab-printed double-precision values are reproduced to the printed digits. Note: the exact central-difference error for q at h=1e-4 is -3.331945e-10 and the lab prints 3.328e-10; the 3.5e-13 gap is the lab's double-precision round-off (float minus exact), see recompute_r2.py output.")
row("M2-a-num-L05-lab-size", "2.2-numbers; 2.9-prose", "L05.html misconception 3 (current text 'None of these is h^2 ...')", P,
    "The round-1 sentence 'The error is h^2, which is the size of the central-difference error in Lab 1' is gone. The current sentence gives 2.350e-07, 3.328e-10 and 8.550e-07 as the lab's errors, notes that none is h^2 (= 1e-8), and gives the leading-order reason. Verified against the printed values and the recomputation (ratio of exact error to h^2 q'''/6 = 1.0000000).")
row("M2-a-num-L06", "2.2-numbers", "L06.html lines 115, 178, 226, 204, 353-402", P,
    "2/sqrt(3) = 1.1547 (M2, quiz tolerance 1e-4); 1/sqrt(3) = 0.577 vs midpoint 0.5 (misconception 3); f(-2) = -2, f(-1) = 2, f(1) = -2 (M3, lab); 8 = 4 + 4 intervals (quiz, E1); f(2) = -3 (M1). All recomputed.")
row("M2-a-math-L01", "2.4-math", "L01.html Def 2.1, Prop 2.2 (line 68, proof 73-75), Prop 3.1 (157-163), Ex 4.1 (174), Prop 4.2 (179-186), problems M1-M3, P1-P3, E1-E3, R1-R3", P,
    "Re-derived: uniqueness proof (eps/2 thresholds, n = max); tail proposition (N' = max(N, M)); Example 4.1 (even n, odd m: 2 <= |1-L|+|L+1| < 2); Prop 4.2 with B = max(|a_1|..|a_{N-1}|, |L|+1); M1 13/(n+4) and N = 1297 for eps 0.01 (n > 1296 check); M2 least N = 11 for 1/n^2 < 0.01; P2 sign argument; P3 shift N' = max(1, N-5); R2 floor bound; R3 non-convergence. Every proof step checked; no gaps.")
row("M2-a-math-L02", "2.4-math", "L02.html Prop 1.1 (lines 56-72), Cor 2.2 (164-171), Ex 2.3 (175), Remark 3.1 (181-183), problems M1-M3, P1-P3, R1-R3", P,
    "Re-derived: (i) triangle inequality; (ii) a_n b_n - ab = a_n(b_n-b)+b(a_n-a), bound |a_n|<|a|+1, |b|/(|b|+1)<1 step; (iii) delta=|b|/2, 1/|b_n|<2/|b|, identity (b(a_n-a)-a(b_n-b))/(b b_n), epsilon thresholds sum to eps|b|^2/2 times 2/|b|^2 = eps. "
    "R1 |a_n/b_n| > M (recomputed threshold). Misconception 2 divergence argument via (ii) with constant -1 checked. Scope sentence flagged separately (M2-a-prose-scope-L02-why).")
row("M2-a-math-L03", "2.4-math", "L03.html Def 1.1 (58-60), Ex 1.2 (64), Prop 1.3 (68-75), Cor 1.4 (78-85), Def 2.1, Prop 2.2 (96-102), Ex 2.3 (107), Ex 2.4 (177), problems", P,
    "Re-derived: Ex 1.2 delta = eps/3 gives |3x-6| = 3|x-2| < eps; Prop 1.3 proof with x_n != a; Cor 1.4 both cases x_n = a and 0 < |x_n-a| < delta; Prop 2.2 (only if: right and left sides of Def 1.1; if: delta = min); Ex 2.3 left delta = min(1, eps/2) and |x+1|<2 on (0,1), right delta = eps/2; "
    "P2 delta = min(1, eps/(1+2|a|)); R1 delta = sqrt(eps); R2 bound; R3 reverse triangle inequality. No gaps.")
row("M2-a-math-L04", "2.4-math", "L04.html Def 1.1 (57), Ex 1.2 (64), Prop 2.1 (128-136), Ex 3.1 (145), problems M1-M3, P1-P3, R1-R3", P,
    "Re-derived: Q(h)=2a+h (Ex 1.2); Prop 2.1 proof (tolerance 1 gives |Q|<|f'(a)|+1, delta = min(delta_1, eps/(|f'(a)|+1)), f(x)-f(a) = (x-a)Q(x-a)); Ex 3.1 Q=|h|/h; P1 cube: |Q-3a^2| = |h||3a+h| <= |h|(3|a|+|h|), delta = min(1, eps/(3|a|+1)); R1 x|x| with Q = |h|; M3 1/x gives -1/(2(2+h)) -> -1/4 (recomputed).")
row("M2-a-math-L05", "2.4-math", "L05.html Lemma 1.1 (57-64), Prop 1.2 (69-76), Prop 1.3 (81-88), Prop 2.1 chain rule (174-181), problems P1-P3, R1-R3", P,
    "Re-derived: Lemma (c) choice r' with |M|/2, identity (M(F-L)-L(G-M))/(MG) and bound 2/|M|^2 times the bracket, epsilon thresholds sum to eps|M|^2/2; product-rule add-and-subtract identity; quotient identity (g(a)Q_f - f(a)Q_g)/(g(a)g(a+h)) recomputed symbolically; chain rule G on J-b with G(0)=g'(b), k(h)=0 case, eta/delta choice. "
    "Lemma parts (a) and (b) are proved by the stated substitution into Lesson 2 Prop 1.1 (i) and (ii), which is written out in full there; the epsilon choice for (b) is the one given in (ii) with the same substitution: accepted as a complete proof by reference, not a gap. Round-1 phrase 'the same estimates close the argument' is gone; 'Define G on J' is now 'G on J - b = {k: b+k in J}'. "
    "P1 power rule by induction re-derived; P2 reciprocal; P3 with J = R; R1 central difference of cubic: a h^2 term, verified by expansion; R2 composition domain; R3 quotient from product and reciprocal.")
row("M2-a-math-L06", "2.4-math", "L06.html Prop 1.1 (58-64), Fact 2.1 (72-73), Thm 2.2 (77-83), Thm 2.3 (87-94), Cor 3.1 (102-108), problems M1-M3, P1-P3, R1-R3", P,
    "Re-derived: Prop 1.1 (Q<=0 from the right, Q>=0 from the left, f'(c)>0 contradicts Q<=0 on (0,delta)); Rolle (non-constant case: the extreme value M != f(a) or m != f(a) lies in (a,b), Prop 1.1 applies); MVT via g(x)=f(x)-f(a)-s(x-a) with g(a)=g(b)=0; Cor 3.1 via MVT on [x,y] (x,y in [a,b] gives (x,y) in (a,b)); "
    "R2 |x-1| chord slope 0 with f' = -1 and 1; R3 Lipschitz bound; M1 min at 2, f(2) = -3; M2 c = 2/sqrt(3); M3 f' > 0 on (-2,-1) and end values -2, 2. Fact 2.1 is assumed and listed as a hypothesis of Theorems 2.2 and 2.3 (not graded), which is an honest conditional statement. "
    "The quiz statement of Cor 3.1 (ii) omits continuity on [a,b]: row M2-a-hyp-quiz-L06q5.")
row("M2-a-hyp-quiz-L06q5", "2.4-math; 2.7-cards (quiz hypotheses)", "L06.html quiz item L06q5 (lines 367-375), its explanation (line 374)", F_,
    "The stem 'If f'(x) > 0 on (a, b), what can be said on [a, b]?' has keyed answer 'f is increasing' with explanation 'Corollary 3.1 (ii): a positive derivative on the open interval gives an increasing function.' Corollary 3.1 (line 103) needs f continuous at each point of [a,b]; the stem and explanation drop that hypothesis. "
    "Counterexample (recomputed, /tmp/M2-v/a-r2 recompute_r2.py): f(x)=x on [0,1), f(1)=-5. Then f'=1>0 on (0,1), but f(1/2)=0.5 > f(1)=-5, so f is not increasing on [0,1]. The keyed answer is false without the stated hypothesis.",
    "Add 'and f is continuous at each point of [a, b]' to the stem and to the explanation (or key the answer 'f is increasing on (a, b)'). Re-run check_pages.py --unit M2.")
row("M2-a-hyp-quiz-L01q6-card-c011", "2.4-math; 2.7-cards (hypotheses dropped)", "L01.html quiz item L01q6 (lines 383-389); cards.json M2-c011 (L01)", F_,
    "Proposition 3.1 (L01 line 158) requires a_n -> L. The quiz asks 'If the first term of a sequence is replaced by 10^6, what happens to its limit?' with keyed answer 'The limit does not change' and no hypothesis that the sequence has a limit. "
    "Card M2-c011 says 'Replacing the first term ... leaves the limit 2' for the convergent example, but its front asks the general question 'Do the first terms of a sequence help determine its limit? No.' and the back says 'changing finitely many terms leaves the limit unchanged' without 'if the sequence converges'. For a divergent sequence there is no limit to be unchanged, so the stated answer presupposes convergence.",
    "In the quiz stem add 'a sequence that converges to L'; in card M2-c011 back add 'for a convergent sequence' (or keep the card as the convergent-sequence example).")
row("M2-a-grade-labs", "2.3-grades", "L01-L06 key-results tables; lab interpretation paragraphs; Lemma/Prop grades T", P,
    "Every lab-derived result is graded C with basis Lab n (L01 line 149, L02 151, L03 172, L04 122, L05 167, L06 178; key-results rows graded C). Every T claim has a proof on its page (checked in M2-a-math-L0n). The only ungraded claim, Fact 2.1 (EVT), is labelled as assumed and listed as a hypothesis (L06 line 73).")
row("M2-a-prose-L01-lab-would-print", "2.9-prose; 2.5-lab", "L01.html Problem E3 solution (line 293)", P,
    "Round-1 text 'The lab would print 1.000000 x 10^-4 for the error at n = 9999' is replaced by 'Lab 1 does not print this value, because its search uses the tolerance 0.001 ... no lab run in this lesson checks it'. The claim now matches the lab (which prints only the tolerance-0.001 results).")
row("M2-a-prose-L05-misc-h2", "2.9-prose", "L05.html misconception 3 (round-1 line 210)", P,
    "Round-1 sentence 'The error is h^2, which is the size of the central-difference error in Lab 1' was removed; current text (line ~214) gives the lab's values and says none equals h^2. Checked against the output.")
row("M2-a-prose-L06-exactly", "2.9-prose", "L06.html why-it-matters (line 51) and key-results row 'controls monotonicity' (round-1 line 323)", P,
    "Round-1 'This lesson states exactly when that works' is replaced by 'This lesson states what a derivative test does and does not establish'. Round-1 key row 'The sign of the derivative controls monotonicity' is now 'gives sufficient conditions for monotonicity (Corollary 3.1)', which matches Cor 3.1 (ii)/(iii).")
row("M2-a-prose-L06-each-hypothesis", "2.9-prose", "L06.html canon-breaks (lines 183-187)", P,
    "Round-1 'each hypothesis is needed' is replaced by 'Two dropped hypotheses break Rolle's conclusion, and a third case shows ...'. The two counterexamples (f=x on [0,1) with f(1)=0; f=|x| on [-1,1]) are checked: each drops exactly one hypothesis of Theorem 2.2.")
row("M2-a-prose-L04-only-meaning", "2.9-prose", "L04.html line 60", P,
    "Round-1 'This is the only meaning of derivative used in the unit.' is now 'This is the meaning of derivative used in this lesson.' The scope is now the lesson, not the unit.")
row("M2-a-prose-frequency-claims", "2.9-prose", "index.html line 33; L01.html line 179; L02.html line 51 (round-1 locations)", P,
    "Round-1 'Much of finance concerns rates of change' is now 'Sensitivities are rates of change'. grep over index.html and L01-L06 finds no 'rarely', 'frequent', 'often' or 'usually'. The round-1 frequency sentences are gone.")
row("M2-a-prose-unproved-claims", "2.9-prose; 2.4-math", "L01.html line 214; L02.html line 206; cards M2-c012", P,
    "Round-1 'Boundedness is a necessary condition for a limit' is now backed by Proposition 4.2 (line 179-186, proved). Round-1 'b_n is a sign change of a_n, so it diverges too' is now a proof (lines 206: if b_n -> L then a_n = (-1)b_n -> -L by Prop 1.1 (ii) with the constant -1, contradicting Example 4.1). Card M2-c012 matches Example 4.1 and Misconception 3.")
row("M2-a-prose-banned-scan", "2.9-prose", "index.html and L01-L06 visible text (scripts/M2-a-r2/prose_scan.py)", P,
    "Visible-text scan of 7 pages (~21,000 words) for banned phrases (roughly half, about 6%, historically, studies show, well known, important to note, for brevity, beyond the scope, left as an exercise, TODO, TBD, lorem, typically, in practice, most, small, fast, smooth, often, generally, usually, clearly, obvious, trivial, of course, easy to see) and process words (build, builder, round, verif, REQUEST, unit report, ledger): no hit in learner prose except 'verified citation registry' (P0.1 quiz, a registry term), 'round-off' type words in code, and 'lo, lo + step, ..., hi' in the L06 grid docstring (a list pattern fully specified by the code). Scope words (only, all, every, any, same, always, most, small) were checked in context: the hits are mathematical quantifiers or are followed by a computation or a proof. Two scope sentences fail and are rows M2-a-prose-scope-L02-why and M2-a-defuse-L01-L03 (the latter is a define-before-use item).")
row("M2-a-prose-scope-L02-why", "2.9-prose (scope words without computation)", "L02.html why-it-matters (line 51)", F_,
    "The sentence 'the quotient law is the one where a missed hypothesis gives a wrong answer: it fails when the limit of the denominator is zero (Remark 3.1)' asserts an exclusive claim ('the one') and a wrong answer. Remark 3.1 shows the quotient n diverges; the law gives no value at all (a/0 is undefined), so no wrong value is produced, and the exclusivity is not shown by any computation.",
    "Replace with: 'the quotient law is the only one of the three whose hypothesis can fail for convergent sequences: when the limit of the denominator is zero the quotient can diverge (Remark 3.1).' or drop 'the one' and 'wrong answer'.")
row("M2-a-defuse-L01-L03", "2.9-prose; DAG (define before use)", "L01.html why-it-matters line 51 ('A derivative is the limit of a difference quotient, an integral is the limit of sums'); L03.html why-it-matters line 51 ('a derivative is defined where a limit exists')", F_,
    "The term 'derivative' first appears in L01 line 51 and 'integral' in the same line, both before their definitions (derivative is defined in L04 Definition 1.1; the integral in L09). The BUILDER define-before-use rule (plan section 12) requires a term to be defined or linked at its first appearance and the lesson never to rely on a later definition. The sentences are unlinked and state a definition-like equality. "
    "grep for derivativ/integral in L01-L03 finds only these two lines (L02 has none).",
    "In L01 line 51 either link the words to their later entries (<a href=\"L04.html#s1\">derivative</a>, the integral by name without a definition) or rephrase with 'limit' only. In L03 line 51 link 'derivative' to L04 or say 'a rate of change is defined where a limit exists'.")
row("M2-a-xref-L03-keyrow", "2.9-prose; 2.4-math (key-results)", "L03.html key-results rows (lines 320-321) (round-1 row at line 320)", P,
    "Round-1 row 'A limit of a function gives the limit along every sequence that avoids the point' is now 'If x_n lies in I, x_n != a and x_n -> a, then f(x_n) -> L whenever lim f(x) = L (Proposition 1.3)', which matches Proposition 1.3's hypotheses (line 69). Row 321 matches Corollary 1.4.")
row("M2-a-xref-M1-locators", "2.1-citations (internal cross-references)", "index.html lines 80, 89, 98, 107, 116-125; L01.html line 189; M1 L01 Theorem 3.2 (a), M1 L02, M1 L03, M1 L06", P,
    "M1 L01 line 92-96: 'Theorem 3.2 (negating a nested statement)', (a) = negation of forall-exists is exists-forall-not (checked by reading the statement). M1 L06 is 'Geometric Series and Proof by Induction' (closed form). M1 L03 Definition 1.1 natural logarithm = unique x with e^x = y (inverse). M1 L02 defines lowest terms (line 117-118) and proves sqrt(2) by contradiction (section title 'Proof by contradiction'). All M1 locators read.")
row("M2-a-xref-L13-rounding", "2.9-prose (forward reference)", "L04.html canon-breaks (line 156): 'Lesson 13 treats the effect of rounding on the quotient'", P,
    "L13.html is about finite differences: 'a rounding-error model' and 'Lab on exp at 1 with the rounding turn-up' (L13 meta description and body, grep 'round' 17 hits). The forward reference is accurate.")
row("M2-a-dag-slice", "2.8-DAG", "tools/check_dag.py --all; slice data-concept links; <dfn> anchors (L01 def-limit, L04 def-derivative); course/concepts.html", P,
    "check_dag M2: PASS. Slice links: quantifiers, direct-proof, proof-by-contradiction, mathematical-induction, exponential-and-logarithm (all M1 concepts, anchors in concepts.html), evidence-grade, notation-conventions, project-ladder (P0.1, entries read 'not yet released'). "
    "Own concepts: limit (L01 dfn), derivative (L04 dfn). No slice page links or defines a later-module concept (grep for Riemann, Lebesgue, Fubini, Stieltjes, Lagrange multiplier, duration, convexity, Jacobian, Hessian, matrix, implicit, envelope in L01-L06: only prose, in L01-L06 none). Continuity is used in prose only (Lesson 2) as the plan allows.")
row("M2-a-hub-structure", "2.9-structure", "course/modules/M/M2/index.html", P,
    "Seven objectives (4-8 required); prerequisites M1 and P0.1 linked with concept links; placement section data-unit=M2, data-page=placement, data-mastery=0.8 with eight items (six MC, two numeric data-skill, one of each rung skill); lesson map L01-L24 (24 cards with 10 h); ladder ol.ladder with four rung titles in order (Worked example, Completion problem, Independent project, Stretch); data-status section 'No real data is used in M2'; core reading as data-cite keys spivak2008calculus and hubbard2015vector (both in references/references.json).")
row("M2-a-hub-reading-claim", "2.9-prose; 2.1-citations", "index.html line 193 and reading section", P,
    "'No passage locator from either has been confirmed, so the lessons attribute no statement to them.' grep for Spivak and Hubbard: only in the hub reading list and in the References sections of L01-L06, each stating the same. No locator or theorem number is attributed to either source in L01-L06.")
row("M2-a-hub-banned", "2.9-prose", "index.html visible text", P,
    "Banned-phrase and process-word scan (prose_scan.py) of index.html: no banned phrase; 'small' occurs twice (a finite check of numerators in the placement quiz; 'small steps' in the L13 card, a summary of Lesson 13, out of this slice's scope). 'verified citation registry' is a term. Scope-word hub sentences checked against L01-L06 content.")
row("M2-a-hours", "2.2-numbers; hours", "L01-L06 headers (data-hours=10); index.html hours", P,
    "Every L01-L06 page declares 10 study hours (data-hours and the eyebrow). Hub hours arithmetic: 240 = 24 x 10 (arithmetic only; design targets, not paced).")
row("M2-a-cards-L01-L06", "2.7-cards", "course/modules/M/M2/cards.json (ids M2-c001..c014 L01; c015..c026 L02; c027..c039 L03; c040..c050 L04; c051..c061 L05; c062..c074 L06; c376 L01)", P,
    "75 cards for L01-L06 (14+13+13+11+11+13). Each read against its lesson text: M2-c002 Definition 2.1; c004 Prop 2.2 with thresholds eps/2 and n = max; c005 N > 1/eps (Example 2.3); c006 Lab 1 print 1000 and 1.000000e-03; c009 Example 4.1 chain; c018 Remark 3.1; c019 Misconception 2; c025-c026 lab values; c028 Example 1.2; c033 Example 2.3; c035 lab line; c048-c050 misconceptions and Lab 1; c055-c058 lab values and c057 29/49 with 3.328e-10; c061 Misconception 3; c063 Prop 1.1 hypotheses; c064 Fact 2.1 assumed; c066 MVT hypotheses; c067 Cor 3.1 with hypotheses; c069-c070 Lab 1 values; c072 midpoint; c073 Rolle continuity; c376 Prop 4.2. Every card number appears in its lesson or its lab output. Two cards drop a hypothesis: see M2-a-hyp-quiz-L01q6-card-c011.")
row("M2-a-cards-dup-scan", "2.7-cards", "course/modules/M/M2/cards.json (377 cards; scripts/M2-a-r2/card_dupes.py)", P,
    "Round-1 FAIL claimed M2-c342 and M2-c343 (L23) have identical fronts. Re-checked: their raw fronts are \"In Lab 1, what is P'(y0) ...?\" and \"In Lab 1, what is P''(y0) ...?\", which differ by one prime (the normalising scan that stripped apostrophes reported them equal; that was a false positive). Raw exact-duplicate fronts: none. Normalised duplicate fronts: only that false positive. Highest near-duplicate fronts inside L01-L06 are c015/c016 (0.88, laws (i) and (ii)) and c065/c066 (0.85, Rolle and MVT), all distinct questions.")
row("M2-a-refs-spivak-hubbard", "2.1-citations", "references/references.json keys spivak2008calculus, hubbard2015vector; L01-L06 References sections", P,
    "Registry records read: spivak2008calculus title 'Calculus', Spivak, Publish or Perish, year 2008, status verified, source_strings 'Spivak, Calculus, 4th ed. (2008)'; hubbard2015vector title 'Vector Calculus, Linear Algebra, and Differential Forms: A Unified Approach', Matrix Editions, 2015, verified, source string 'Hubbard & Hubbard, Vector Calculus, Linear Algebra, and Differential Forms, 5th ed. (2015)'. The page titles are the source-string forms. No passage locator is attributed (see M2-a-hub-reading-claim). Offline and live verify_refs PASS (M2-a-cmd-refs).")

summary = {
    "rows": len(rows),
    "pass": sum(1 for r in rows if r["status"] == P),
    "fail": sum(1 for r in rows if r["status"] == F_),
    "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
}
verdict = "PASS" if summary["fail"] == 0 and summary["unverifiable"] == 0 else "FAIL"
fragment = {
    "unit": "M2",
    "slice": "M2-a",
    "round": 2,
    "verifier": "round-2 independent verifier (Haiku), slice M2-a (hub index.html, L01-L06 and their lab twins); did not build M2 and shares no context with the builders",
    "pin": "1817191",
    "base": "none",
    "checkout": "/tmp/verifyB2-M2-a (detached at 1817191; .venv symlinked; vendor copied)",
    "scratch": "/tmp/M2-v/a-r2",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: index.html, L01-L06, tests/labs/M2/lab-M2-L01-1..L06-1.py, and the L01-L06 cards of cards.json (plus a full duplicate scan of cards.json). Delta from c11ae01 (round 1) is index.html and L01-L06.html; the twins, tools and registry are byte-identical, so the twin rows are re-run, not carried.",
        "No row is carried from round 1: every subject (the seven slice pages) changed, so every previous row was re-verified from scratch. Previous non-PASS rows: M2-a-num-L05-lab-size, M2-a-math-L05, M2-a-prose-L01-lab-would-print, M2-a-prose-L05-misc-h2, M2-a-prose-L06-exactly, M2-a-prose-L06-each-hypothesis, M2-a-prose-L04-only-meaning, M2-a-prose-frequency-claims, M2-a-prose-unproved-claims, M2-a-xref-L03-keyrow, M2-a-cards-dup-scan: all re-verified (PASS now, except the round-1 duplicate claim which was a false positive and is recorded as PASS with the correction).",
        "Mutation: the architect ruling limits mutation testing to project graders. This is a lab slice with no grader, so mutants is empty and no mutant was written.",
        "Alternative implementations (five-implementation check): not applicable to a lab slice; the labs are demonstrations, not graders.",
        "Hours: arithmetic only (240 = 24 x 10 and 300 split); pace not judged (architect ruling).",
        "Not checked: the Spivak and Hubbard texts were not read (no locator is claimed; no network access to publisher pages was attempted, per the access rules). The M1 locators were read in the M1 pages, not in the books.",
        "Not checked: lessons L07-L24, the project and the grader, and cards of other lessons (other slices). The full card duplicate scan covers all 377 cards and is recorded once.",
        "Round-1 correction: M2-a-cards-dup-scan claimed M2-c342/c343 have identical fronts. They differ by one prime (P'(y0) vs P''(y0)); the earlier scan normalised apostrophes. Recorded as PASS here.",
        "Double-precision note: the lab's printed q-error 3.328e-10 differs from the exact central-difference error 3.332e-10 by 3.5e-13, the lab's float round-off (recompute_r2.py). The L05 leading-order sentence is correct to 1e-5 relative at h = 1e-4; no row is raised for it.",
    ],
    "summary": summary,
    "rows": rows,
}
path = "ledgers/M2/M2-a.json"
with open(path, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print(json.dumps(summary), verdict)
