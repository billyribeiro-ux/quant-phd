import json, sys
from datetime import datetime, timezone
CARRY_L20 = "Carried from round 2 (course/modules/M/M2/L20.html and tests/labs/M2/lab-M2-L20-1.py byte-identical since the previous pin): "
CARRY_L24 = "Carried from round 2 (course/modules/M/M2/L24.html and tests/labs/M2/lab-M2-L24-1.py byte-identical since the previous pin): "
CARRY_LAB20 = "Carried from round 2 (course/modules/M/M2/L20.html and tests/labs/M2/lab-M2-L20-1.py byte-identical since the previous pin): "
rows = []
def R(id_, check, location, status, evidence, fix=None):
    row = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)

# 2.5/command rows (run fresh on pin aa3c26c)
R("M2-d-cmd-check-pages", "2.9-structure", "course/modules/M/M2/L19.html ... L24.html", "PASS",
  "tools/check_pages.py --unit M2 --page Lnn for L19..L24: 'check_pages M2 Lnn: PASS' for all six (run this round).")
R("M2-d-cmd-check-dag", "2.9-dag", "course/modules/M/M2/ (slice links and dfn ids)", "PASS",
  "tools/check_dag.py --unit M2: 'check_dag M2: PASS'. Concept links on L19-L24 read with grep of data-concept: L19 derivative, gradient, partial-derivative, taylor-theorem; L20 definite-integral, limit; L21 derivative, partial-derivative; L22 derivative, implicit-function-theorem, partial-derivative; L23 derivative, discount-factor, geometric-series, present-value, taylor-theorem; L24 derivative, finite-difference-derivative, taylor-theorem. Each dfn id appears once (def-hessian, def-multiple-integral, def-implicit-function-theorem, def-envelope-theorem).")
R("M2-d-cmd-run-labs", "2.5-labs", "tests/labs/M2/lab-M2-L19-1.py ... lab-M2-L24-1.py", "PASS",
  "tools/run_labs.py --unit M2 --page L19, L20, L21, L22, L23, L24: 'run_labs M2: PASS (1/1)' each.")
R("M2-d-cmd-twins-isolated", "2.5-labs", "tests/labs/M2/lab-M2-L19-1.py ... lab-M2-L24-1.py", "PASS",
  "Each twin run as python -I -W error: exit 0, empty stderr (this round). Seeded/no network: docstrings state standard library only, no randomness.")
R("M2-d-cmd-expected-match", "2.5-labs", "course/modules/M/M2/L19.html ... L24.html (pre.expected)", "PASS",
  "ledgers/M2/scripts/M2-d-r3/lab_output_match.py: run each twin and check each printed line appears in its page: L19 10/10, L20 8/8, L21 5/5, L22 9/9, L23 11/11, L24 25/25 lines found, 0 missing.")
R("M2-d-cmd-embed-match", "2.5-labs", "course/modules/M/M2/L19.html ... L24.html (data-run block)", "PASS",
  "Same check as M2-d-cmd-expected-match against the data-run blocks: 0 missing lines on all six pages (the printed output is the embedded output).")
R("M2-d-cmd-page-smoke", "2.9-structure", "tools/page_smoke.py --unit M2 --pages L19 L20 L21 L22 L23 L24 --skip-sweep", "PASS",
  "'page_smoke M2: PASS'; each lab reported under 0.1 s in the run, runtime boot 1.1 s with numpy (wall 13.96 s for the whole command).")
R("M2-d-cmd-ruff-mypy", "2.5-labs", "tests/labs/M2/", "PASS",
  ".venv/bin/ruff check tests/labs/M2/: 'All checks passed!'; ruff format --check: '27 files already formatted'; .venv/bin/mypy --no-incremental tests/labs/M2/: 'Success: no issues found in 27 source files'.")
R("M2-d-cmd-pytest-labs", "2.5-labs", "tests/test_labs.py, tests/test_run_labs.py (-k M2)", "PASS",
  "pytest -q tests/test_labs.py tests/test_run_labs.py -k M2: 27 passed. (tests/test_page_checks.py -k M2 printed no summary line; not counted as evidence.)")
R("M2-d-cmd-verify-refs", "2.1-citations", "references/references.json (keys spivak2008calculus, hubbard2015vector)", "PASS",
  "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'; tools/verify_refs.py --unit M2: 'live re-verification of M2: 2 of 560 entries, 0 problems'.")
R("M2-d-2.1-keys-used", "2.1-citations", "course/modules/M/M2/L19.html ... L24.html (References sections)", "PASS",
  "Each of L21-L24 References section states that no locator is confirmed and no statement is attributed; L19 and L20 cite no registry key in prose except as the curriculum sources list; grep of the slice for Spivak/Hubbard shows no locator or theorem number attributed to them.")

# 2.2 numbers
R("M2-d-num-L19", "2.2-numbers", "course/modules/M/M2/L19.html Lab 1 interpretation; Misconception 2; Remark 3.2", "PASS",
  "Recomputed (ledgers/M2/scripts/M2-d-r3/recheck.py): grad (0.474680, 1.898721), Hessian f_xx 0.412180, f_xy 2.148721, f_yy 1.0 at (0.5, 0.25); printed errors 2.26e-11 and 1.94e-11 and ratios 3.9509/3.9750/3.9874 and 7.8836/7.9429/7.9717 match the lab output line for line. Ratio basis stated: error at the step twice as large over error at the current step (lab code: previous over current).")
R("M2-d-num-L20", "2.2-numbers", "course/modules/M/M2/L20.html Theorem 1.2, Proposition 2.4, Lab 1, E1 to E3", "PASS",
  "Recomputed with fractions: midpoint sums 3/2, 13/8, 53/32, 213/128 and errors -1/6, -1/24, -1/96, -1/384 equal 5/3 - 1/(6n^2); the midpoint sum of x^2 on [0,1] is 1/3 - 1/(12 n^2) (n=1: 1/4 checked by hand).")
R("M2-d-num-L21", "2.2-numbers", "course/modules/M/M2/L21.html Lab 1 interpretation; E2; Example 2.2", "PASS",
  "Lab output y=0.9168754789, 0.8351223485, 0.6823278038, 0.4533976515 and F_y 2.771982 to 2.396714 match the printed sentence 'between about 2.4 and 2.8'; differences 6.2e-13, 5.2e-14, 3.7e-12, 3.9e-12 match the printed values, the last two largest. Example 2.2 slope -0.75 recomputed from -2x/2y at (0.6, 0.8).")
R("M2-d-num-L22", "2.2-numbers", "course/modules/M/M2/L22.html Lab 1 interpretation; misconception 3", "PASS",
  "Recomputed: f_xx(x*=0.5, a=1.5) = -a/(1+x*)^2 = -0.666667; 0.5 x 0.666667 x 1e-16 = 3.33e-17 (page: 3.3e-17). Part B largest printed error 5.4e-12 equals the printed value. ln a values 0.40546511, 0.69314718, 1.09861229, 1.38629436 match. Sensitivity estimate for the golden-section location resolution, sqrt(2 eps |f|/|f_xx|) = 8.5e-9, is consistent with the printed 1e-8 offset (basis: this arithmetic, not a printed value).")
R("M2-d-num-L23", "2.2-numbers", "course/modules/M/M2/L23.html Lab 1 interpretation; Abstract; E3", "PASS",
  "Recomputed with Decimal at 50 digits: P(0.04) = 108110.895779355..., rounds to 108111; P'(0.04) = -851466.7395286 (central difference agrees to 1.6e-3); P''(0.04) = 8376648.511919 (difference 1.9); errors e1 = 403.77 and e2 = -15.06 at +0.01, e2 = +16.01 at -0.01; exact prices 100000 and 117060; preview ratios -P'/P = 7.8759 and P''/P = 77.482 (printed as 7.875864 and 77.482001).")
R("M2-d-num-L24", "2.2-numbers", "course/modules/M/M2/L24.html Lab 1 hypothesis and interpretation; Remark 4.4", "PASS",
  "Recomputed: 2 sqrt(delta/e) = 1.8076e-8 with delta = 2.220446e-16 (half ulp of e, checked with math.ulp); (3 delta/e)^(1/3) = 6.2578e-6 (page: 6.3e-6). Printed errors 1.359e-5 at h=1e-5 and 1/2 e h = 1.359e-5; 6.603e-9 at 1e-8; 2.154e-7 at 1e-9; 5.859e-11 at 1e-5 and 1e-7.")

# 2.3 grades
R("M2-d-grade-L19-L20-L22-L23-L24", "2.3-grades", "course/modules/M/M2/L19.html ... L24.html (grade spans, key-results tables)", "PASS",
  "Key-results rows read: Theorem 2.1 T (proved), Example 2.2 T (computed), Theorem 3.1 T, Proposition 3.3 T, Lab-derived rows (L19 Lab 1 numbers, L22 Lab 1, L23 Lab 1, L24 Lab 1) carry C in cards and are labelled as lab results on the page. No grade T on a lab-only result found.")
R("M2-d-grade-L21-assumed-result", "2.3-grades", "course/modules/M/M2/L21.html Theorem 1.2 (data-grade T) and its proof", "PASS",
  "Theorem 1.2 is graded T and its proof is on the page (Existence, Continuity, Differentiability paragraphs). The round-2 'Assumed result 1.2' wording no longer appears in L21 (grep: no match).")

# 2.4 mathematics
R("M2-d-math-L19-thm2.1", "2.4-math", "course/modules/M/M2/L19.html Theorem 2.1 and proof; Example 2.2", "PASS",
  "Statement now lists the hypotheses the proof uses (f_x, f_y, f_xy exist on the disc; f_xy continuous at p). Step 1 mean value argument, Step 2 bound with delta/2 radii (|(xi,eta)-p| < delta/sqrt2 < delta), Step 3 limit in k then h all re-derived. Example 2.2 values f_xy(0,0) = -1, f_yx(0,0) = 1 re-derived from f_x(0,y) = -y and f_y(x,0) = x.")
R("M2-d-math-L19-thm3.1-prop3.3", "2.4-math", "course/modules/M/M2/L19.html Theorem 3.1, Remark 3.2, Proposition 3.3 and proof", "PASS",
  "phi(1)=R(h) and phi'' bound 2|h|^2 omega(|h|) re-derived (|h1|+|h2|)^2 <= 2|h|^2; Prop 3.3: E(s)/E(s/2) -> (1/6)/(1/48) = 8 re-derived.")
R("M2-d-math-L19-solutions", "2.4-math", "course/modules/M/M2/L19.html problem set M1-M3, P1-P3, E1-E3, R1-R3 and quiz answers", "PASS",
  "Recomputed: Hessian of x^3+2xy^2-y at (1,2) = [[6,8],[8,4]]; x^2+xy+y^2 has zero remainder; g''(0)=2 for x^2y; f_xy of x^2y^3 = 6xy^2; e^x y Hessian; R3 threshold omega(|s|) < m/4 gives positivity; quiz f_xy(2,1) for x^3y = 12; R2 constant c = dimension-dependent. No error found.")
R("M2-d-math-L19-misconception2", "2.4-math", "course/modules/M/M2/L19.html Section 5 Misconception 2", "PASS",
  "Cross term 2 f_xy h1 h2 with f_xy(0.5,0.25) = e^0.5 + 0.5 = 2.149; with d=(0.6,-0.8) and s=0.1 the dropped term is about 5e-3, far above the printed second-order error 1.57e-4, so dropping it would change the printed errors (claim holds).")
R("M2-d-math-L20-thm1.2-prop2.2-2.4", "2.4-math", CARRY_L20 + "course/modules/M/M2/L20.html Theorem 1.2, Proposition 2.2, Proposition 2.4",
  "PASS", "Carried from round 2 (L20 page and its lab byte-identical). Re-derived this round: integral 5/3; iterated integrals 5/3 both orders; Prop 2.4 proof sums (2*(1/2) + 2*(1/3 - 1/(12n^2))) = 5/3 - 1/(6n^2) (recheck.py).")
R("M2-d-math-L20-def-not-apply", "2.4-math", CARRY_L20 + "course/modules/M/M2/L20.html Section 3, Example 3.1", "PASS",
  "Carried from round 2. Re-derived this round: int_0^1 f dy = 1/(1+x^2), int_0^1 f dx = -1/(1+y^2), outer values pi/4 and -pi/4 (antiderivatives y/(x^2+y^2), -x/(x^2+y^2)); f(t,0)=1/t^2.")
R("M2-d-math-L20-scope", "2.4-math", CARRY_L20 + "course/modules/M/M2/L20.html introduction and Section 3", "PASS",
  "Carried from round 2. Section 3 scope sentences re-read: rectangles only; no claim for curved regions; Remark 2.3 general statement not proved and not used.")
R("M2-d-math-L21-thm2.1-ex3.2", "2.4-math", "course/modules/M/M2/L21.html Theorem 1.2 (proof of F_y != 0 on I x J), Theorem 2.1, Example 3.2", "PASS",
  "Round-2 FAIL fixed: Theorem 1.2 now states F_y != 0 on I x J and the proof gives F_y > 0 on I x J because F_y > 0 on R; Theorem 2.1 proof cites Theorem 1.2 for the division. Continuity and differentiability paragraphs re-derived (MVT twice, h*(F_x) + (y2-y1)*F_y = 0). Example 3.2 re-derived: x^2 + y^2 = 0 has no real y for x != 0.")
R("M2-d-math-L21-R1-hypothesis", "2.4-math", "course/modules/M/M2/L21.html Research R1 (solution) and Lab 1 hypothesis", "PASS",
  "Lab hypothesis now cites Theorem 1.2 and F_y = 3y^2 + x > 0 for x,y > 0 (re-derived). The R1 solution's sign computation dy/dP0 = 1/P'(y) is correct; its dependence on L23 Proposition 2.1 is recorded as a separate FAIL row (M2-d-prose-L21-R1-forward-ref).")
R("M2-d-math-L22-lemma-thm1.3-ex1.5", "2.4-math", "course/modules/M/M2/L22.html Lemma 1.2, Theorem 1.3, Remark 1.4, Example 1.5", "PASS",
  "Proof of Theorem 1.3 chain-rule step re-derived; Remark 1.4 uses Theorem 1.2 of L21 with F(a,x)=f_x and F_x = f_xx != 0 (re-derived). Example 1.5: f_x = a/(1+x) - 1 zero at x = a-1; V = a ln a - (a-1), V' = ln a.")
R("M2-d-math-L22-proposition-2.1-ex2.2-2.3", "2.4-math", "course/modules/M/M2/L22.html Proposition 2.1, Example 2.2, Example 2.3, Problems M1-M3, P1-P3", "PASS",
  "Example 2.2 F_x = a - 2x, x* = a/2, V = a^2/4, V' = a/2 = f_y c_a. Example 2.3: V(a) = max(a,0), one-sided derivatives 1 and 0 at 0 (P2). M1 x*=a, V=a^2/2; M2 x*=a+3/2, V'=3; M3 F=x(a-x)/2, V=a^2/8, V'=a/4. All re-derived.")
R("M2-d-math-L23-prop2.1-3.1-3.2-3.3", "2.4-math", "course/modules/M/M2/L23.html Proposition 2.1, Theorem 3.1, Proposition 3.2, Proposition 3.3 and proofs", "PASS",
  "Proposition 2.1 signs (all terms negative/positive when c_t > 0) and P''' < 0 re-derived; Lagrange remainder 1/6 P'''(theta) Delta^3 gives the sign of -Delta; Prop 3.3 remainder (1/2)P''(theta) Delta^2 >= 0 re-derived.")
R("M2-d-math-L23-prop2.2", "2.4-math", "course/modules/M/M2/L23.html Proposition 2.2 statement and proof", "PASS",
  "Statement: coupons yF for t < N and F added at N; at yield = coupon rate price = F. Proof with v = 1/(1+y), 1-v = yv and geometric sum (1-v^N)/y re-derived; y = 0 case covered.")
R("M2-d-math-L23-quiz-essential", "2.4-math", "course/modules/M/M2/L23.html section 8 quiz item (L23q8) and its explanation", "PASS",
  "Round-2 FAIL fixed. Stem now asks which hypothesis 'guarantees' P'(y) < 0 and the explanation gives a counterexample: c1 = -1, c2 = 1000, N = 2, y = 0.04: P'(y) = -[1*(-1)*1.04^-2 + 2*1000*1.04^-3] = -1777.07 (recomputed), negative, so positivity of all cash flows is sufficient, not necessary (as the explanation says).")
R("M2-d-math-L24-prop3.1-3.2-thm2.1", "2.4-math", CARRY_L24 + "course/modules/M/M2/L24.html Theorem 2.1, Propositions 3.1, 3.2 and proofs", "PASS",
  "Carried from round 2 (L24 page byte-identical). Re-derived this round: D+ and D- of |x| are 1 and -1 for every h>0; Lagrange truncation bounds (1/2)M2 h and (1/6)M3 h^2 re-derived.")
R("M2-d-math-L24-derivative-def", "2.4-math", CARRY_L24 + "course/modules/M/M2/L24.html Section 1 (definition of the derivative)", "PASS",
  "Carried from round 2. Re-read this round: central quotient converges whenever f' exists (average of the one-sided quotients); converse fails at |x| (central quotient 0 with no derivative).")
R("M2-d-math-L24-prop4.2-4.3", "2.4-math", CARRY_L24 + "course/modules/M/M2/L24.html Propositions 4.2 and 4.3 and their proofs", "PASS",
  "Carried from round 2. Re-derived this round: g(h)=Ah+B/h minimum 2 sqrt(AB) at sqrt(B/A); A=M2/2, B=2delta gives h*=2 sqrt(delta/M2); C=M3/6, B=delta gives h*^3 = 3 delta/M3. M2 > 0 and M3 > 0 hypotheses are on the page.")
R("M2-d-math-L24-R1-R2-solutions", "2.4-math", "course/modules/M/M2/L24.html Research R1 and R2 solutions", "PASS",
  "R1: at h = h*/10, 2delta/h = 10 sqrt(M2 delta) (recomputed). R2: |D+| <= L and |D0| <= L from the Lipschitz inequality, valid at the kink.")
R("M2-d-math-L20-def-not-apply-2", "2.4-math", CARRY_L20 + "course/modules/M/M2/L20.html Problems M1-M3, P1-P3, R1-R3", "PASS",
  "Carried from round 2. Re-derived this round: M1 both orders 3; M2 both orders 2/3; M3 midpoint sum 3/2; P1 induction step (4n^3+12n^2+11n+3)/3; R3 tag example f(x)=x one cell gives 1 vs 1/2.")

# 2.5 labs
R("M2-d-lab-L19", "2.5-labs", "course/modules/M/M2/L19.html Lab 1 hypothesis, interpretation; tests/labs/M2/lab-M2-L19-1.py", "PASS",
  "Lab prints a central difference Hessian error 2.26e-11 and asymmetry 1.94e-11; the page's interpretation of the ratio definition now matches the lab code (previous over current error). The lab tests one function and one direction, as the page says.")
R("M2-d-lab-L20-overreach", "2.5-labs", CARRY_LAB20 + "course/modules/M/M2/L20.html Lab 1 interpretation and E2", "PASS",
  "Carried from round 2. Lab code uses six n values and n<=50 identity: the page says so.")
R("M2-d-lab-L21", "2.5-labs", "course/modules/M/M2/L21.html Lab 1 hypothesis and interpretation; lab-M2-L21-1.py", "PASS",
  "Hypothesis cites Theorem 1.2 (fixed). The lab checks four x values and one relation, as the page says; Newton from y=1 gives monotone convergence (F(x,1)=x>0, F convex and increasing in y>0). The uniqueness gap is stated in E3.")
R("M2-d-lab-L22-count", "2.5-labs", "course/modules/M/M2/L22.html Lab 1 interpretation and last sentence; lab-M2-L22-1.py", "PASS",
  "Page says Part A at four values of a and Part B at three values of a, and no other objectives; code PARAMETERS_A has 4 values, PARAMETERS_B has 3.")
R("M2-d-lab-L22-naive-constant", "2.5-labs", "course/modules/M/M2/L22.html Lab 1 hypothesis; lab-M2-L22-1.py line naive_partial = 0.0", "PASS",
  "Note: the printed 'naive partial' is a hard-coded 0.0 in the lab (comment: x*y has no a), not a computed quantity. The page says the lab prints it, which is accurate; no computation claimed. Recorded as a note, not a failure.")
R("M2-d-lab-L23", "2.5-labs", "course/modules/M/M2/L23.html Lab 1 hypothesis, interpretation; lab-M2-L23-1.py", "PASS",
  "Lab docstring and code agree: price rounded half to even via round(); previews printed only and not defined in the page (page says so). Printed 100000 exact at +0.01 and 117060 at -0.01 match.")
R("M2-d-lab-L24", "2.5-labs", CARRY_L24 + "course/modules/M/M2/L24.html Lab 1 hypothesis and interpretation; lab-M2-L24-1.py", "PASS",
  "Carried from round 2. Re-checked this round: decade grid results and the 'tied at printed digits' sentence (5.859e-11 at 1e-5 and 1e-7) match the output.")

# 2.9 prose
R("M2-d-prose-L19-schwarz", "2.9-prose", "course/modules/M/M2/L19.html Misconception 3 heading; Section 4", "PASS",
  "Misconception 3 and Section 4 bullets match the statements of Theorem 2.1 and Example 2.2 (re-read).")
R("M2-d-prose-L19-central-difference", "2.9-prose", "course/modules/M/M2/L19.html Lab 1 hypothesis, Section 4, Misconception 3", "PASS",
  "Lab hypothesis: central differences at step 1e-5 reproduce Hessian to about 1e-10 (printed 2.26e-11). Consistent.")
R("M2-d-prose-L19-hypothesis-count", "2.9-prose", "course/modules/M/M2/L19.html Section 4 bullet 1", "PASS",
  "Round-2 FAIL fixed: Section 4 now says 'two hypotheses' and lists both, matching Theorem 2.1 as stated.")
R("M2-d-prose-L20-thm1.2-cite", "2.9-prose", CARRY_L20 + "course/modules/M/M2/L20.html Theorem 1.2 proof and Section 1", "PASS",
  "Carried from round 2. L09 Corollary 2.3 (monotone f, any Riemann sum within delta|f(b)-f(a)| of the integral) re-read this round in course/modules/M/M2/L09.html and supports the cited use.")
R("M2-d-prose-L21-process-word", "2.9-prose", "course/modules/M/M2/L21.html References and Section 2; cards", "PASS",
  "Word search for process words (round, build, builder, verifier, unit report, REQUEST) in L19-L24 pages returned no process-word use.")
R("M2-d-prose-L21-assumed-name", "2.9-prose", "course/modules/M/M2/L21.html Lab 1 hypothesis and E3", "PASS",
  "Round-2 FAIL fixed: lab hypothesis and E3 now say 'Theorem 1.2'; grep for 'Assumed' in L19-L24 returns nothing.")
R("M2-d-prose-L21-R1-forward-ref", "2.9-prose", "course/modules/M/M2/L21.html line 301 (Research R1 statement) and line 303 (solution)", "FAIL",
  "Research R1 in L21 says 'By Lesson L23, Proposition 2.1, P'(y) < 0 for all y > -1' and its solution relies on L23 Proposition 2.1 ('which Lesson L23, Proposition 2.1 proves when every cash flow is positive'). L23 is the later lesson (L23 header: 'Lesson 23 of 24'; its Proposition 2.1 is at course/modules/M/M2/L23.html). The bond price P(y) is not defined in L21 before this point, and a reader at L21 has no proof of the sign it uses. The plan's ordering check (plans/M2-build-plan.md, section 3) lists L21 prerequisites L04, L16, L18 only.",
  "Either move Research R1 to L23 (after Proposition 2.1) or restate it with P'(y) < 0 as a stated hypothesis of the problem, and remove the reference to L23 Proposition 2.1 from the L21 solution.")
R("M2-d-prose-L22-uniqueness", "2.9-prose", "course/modules/M/M2/L22.html Section 2 bullets and Misconception 2", "PASS",
  "Section 2 bullets: uniqueness is not assumed; the kink at a=0 (Example 2.3) is where maximizers are not unique. Consistent with P2 and the quiz.")
R("M2-d-prose-L22-misconception3", "2.9-prose", "course/modules/M/M2/L22.html Misconception 3 (changed text)", "PASS",
  "Changed sentence re-derived: 0.5 x 0.666667 x 1e-16 = 3.3e-17; ½|f_xx|e^2 is the leading-order change at an interior maximum (f_x = 0).")
R("M2-d-prose-L23-units", "2.9-prose", "course/modules/M/M2/L23.html Lab 1 interpretation; Section 1", "PASS",
  "Units: prices in cents, yield shift 0.01 = 100 basis points as defined in Definition 1.1. Printed P'(y0) = -851466.74 cents per unit of yield (checked).")
R("M2-d-prose-L23-exponentials", "2.9-prose", "course/modules/M/M2/L23.html Section 4 bullet 1 and Lab 1 hypothesis", "PASS",
  "Section 4 bullet on the rounding and float terms agrees with the lab docstring (round half to even only at the final price).")
R("M2-d-prose-L24-problem-ref", "2.9-prose", CARRY_L24 + "course/modules/M/M2/L24.html Section 5 bullet 3", "PASS",
  "Carried from round 2. Problem P3 (sqrt(1+x) - 1 rewrite) is the problem named in Section 5 bullet 3.")
R("M2-d-scope-words-L21-L24", "2.9-prose", "course/modules/M/M2/L19.html ... L24.html introductions and Sections 4-5", "PASS",
  "Scope words checked: 'every' and 'all' in L21-L24 are each followed by a proof or a stated hypothesis (e.g. L21 'for every x in I' after Theorem 1.2; L22 'for each a'; L23 'for every shift' after Proposition 3.3; L24 'at every step' with the explicit |x| computation). Note, not failure: L19 Section 4 and card c291 say 'under continuity of the Hessian alone'; Theorem 3.1 also assumes twice differentiability, which the sentence does not repeat.")
R("M2-d-banned-phrases", "2.9-prose", "course/modules/M/M2/L19.html ... L24.html", "PASS",
  "Searched for 'roughly half', 'about 6%', 'historically', 'typically', 'generally', ellipses in prose: none. '...' occurrences are inside code blocks or a mathematical sum.")
R("M2-d-dag-prose-names", "2.9-dag", CARRY_L20 + "course/modules/M/M2/L20.html Remark 2.3 ('often called Fubini's theorem')", "PASS",
  "Carried from round 2. Remark 2.3 names the general statement without a citation and says it is not proved; consistent with the architect's Q3 ruling.")
R("M2-d-dag-links", "2.9-dag", "course/modules/M/M2/L19.html ... L24.html concept links and dfn", "PASS",
  "Concept links enumerated (see M2-d-cmd-check-dag). Jacobian (L21 R2), Hessian (L22 R2) and L19-L22 forward or backward references appear as prose, not as concept links, consistent with Q5-Q7.")
R("M2-d-dag-closure", "2.9-dag", "course/modules/M/M2/L19.html ... L24.html (concepts used by name)", "PASS",
  "Each lesson's cited earlier lessons are in the closure: L19 uses L16, L17, L04, L08; L21 uses L04, L16, L18 (prose), and L23 is the forward reference recorded in M2-d-prose-L21-R1-forward-ref; L22 uses L04, L16, L21, L19 (prose); L23 uses M1 and L08; L24 uses L13, L04, L08, L14 (prose, R3).")
R("M2-d-struct-hours", "2.9-structure", "course/modules/M/M2/L19.html ... L24.html data-hours and header", "PASS",
  "data-hours=10 on all six pages and header '10 study hours'; matches plan section 3 (10 h per lesson). No hours arithmetic inconsistency with the hub split.")

# 2.7 cards
R("M2-d-cards-duplicate-scan", "2.7-cards", "course/modules/M/M2/cards.json (376 cards; this slice 97 cards c280-c375 and c377)", "PASS",
  "No duplicate id, front or back across the 376 cards (python scan this round). Slice cards: L19 15, L20 13, L21 15, L22 15, L23 20, L24 19; the card c376 belongs to L01 and is outside this slice.")
R("M2-d-cards-L19-L20", "2.7-cards", "course/modules/M/M2/cards.json M2-c280..c307 (c285 at lines 2000-2005)", "FAIL",
  "Card M2-c285 (Remark 3.2) says the second-order expansion along one direction 'needs the whole Hessian'. Remark 3.2 says the mixed partial enters 'whenever d1 d2 != 0', and for d = (1,0) the expansion uses only f_xx (g''(0) = d^T H d = f_xx). The card is graded T and is an overgeneral scope claim. Round-2 c292 is fixed and re-verified (M2-c292 now lists the Theorem 2.1 hypotheses correctly).",
  "Change to: 'g''(0) = d^T H(p) d. For a generic direction (d1 d2 != 0) all three entries enter; along a coordinate axis only the diagonal entry does.'")
R("M2-d-cards-L21", "2.7-cards", "course/modules/M/M2/cards.json M2-c308..c322", "PASS",
  "Every card re-read against L21: c309 hypotheses/conclusion match Theorem 1.2 (now with F_y != 0 on I x J implied by the proof); c313-c314 numbers match lab output; c315 'proved in Section 1 from the mean value theorem and continuity' matches the proof; c319 'does not show it necessary' matches Section 3.")
R("M2-d-cards-L22", "2.7-cards", "course/modules/M/M2/cards.json M2-c323..c337", "PASS",
  "Every card re-read against L22: c326 matches Remark 1.4; c328/c329 numbers match lab output; c332 matches Example 2.3 and P2; c334 'every point of [0,1] is a maximizer at a=0' matches Example 2.3; c336 matches Misconception 3.")
R("M2-d-cards-L23", "2.7-cards", "course/modules/M/M2/cards.json M2-c338..c357", "PASS",
  "Every card re-read against L23: c341-c346 numbers match lab output and recompute; c344 exact price at +0.01 is 100000; c346 preview statement 'lab establishes this for these shifts only' matches Remark 4.4-style scope; c349 sign statement matches Proposition 3.2; c356 matches Section 4 bullet 2. Card c357 matches Section 4 bullet 3.")
R("M2-d-cards-L24", "2.7-cards", "course/modules/M/M2/cards.json M2-c358..c377 (c370 at lines 2597-2600)", "FAIL",
  "Round-2 cards c363/c364 fixed (M2 > 0 and M3 > 0 now in the hypotheses) and PASS. Card M2-c370 says 'M_3 approximately e for the central step (f''' = exp, so M_3 = e as well)'. The lesson (course/modules/M/M2/L24.html Lab 1 hypothesis) says 'M_3 approximately e'. sup of exp on [1-h0, 1+h0] is e^(1+h0) > e, so the equality is not established; the card contradicts the lesson's approximation.",
  "Change the parenthetical to: '(f''' = exp, so M_3 is approximately e on a small interval about 1)' so that card and lesson both say approximately.")

# mutants: none (lesson slice; no project grader)
frag = {
    "unit": "M2",
    "slice": "M2-d",
    "round": 3,
    "verifier": "independent verifier (Haiku), round 3, slice M2-d (L19-L24 and their lab twins); did not build M2",
    "pin": "aa3c26c",
    "base": "1817191",
    "previous_ledger": "/tmp/fanout-frags/B-M2-d.round2.json",
    "checkout": "/tmp/verifyB3-M2-d (detached at aa3c26c)",
    "scratch": "/tmp/M2-v/d-r3",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since pin 1817191: changed slice files L19.html, L21.html, L22.html, L23.html and cards.json; identical: L20.html, L24.html, tests/labs/M2/lab-M2-L19-1.py .. lab-M2-L24-1.py. Changed cross-referenced files: L08, L09, L10, L13, L14, L16, L17, L18 (prose and assumption wording only; Lagrange/Corollary 2.3 statements re-read on the current pin).",
        "Round-2 FAIL rows: M2-d-math-L21-thm2.1-ex3.2, M2-d-math-L23-quiz-essential, M2-d-prose-L19-hypothesis-count, M2-d-prose-L21-assumed-name, M2-d-cards-L24 (c363, c364), and M2-d-cards-L19-L20 (c292): all re-verified; the first four and c363/c364 are PASS now; M2-d-cards-L19-L20 is FAIL on c285 (new witness).",
        "No mutants: slice d is a lesson slice (no project grader), so the project mutant requirement does not apply.",
        "Not checked: live Crossref/registry re-fetch beyond tools/verify_refs.py --unit M2; the SEC or publisher sources (none cited in the slice); page_smoke sweep (--skip-sweep was used, per the slice command); mypy and pytest on the whole repository (only the M2 twins and tests selected by -k M2).",
        "Note (not a failure): the L22 lab prints a hard-coded naive partial 0.0; the page describes it as printed, which is accurate.",
        "Note (not a failure): c291 and L19 Section 4 say 'under continuity of the Hessian alone'; Theorem 3.1 also assumes twice differentiability. Recorded in the scope-words row.",
    ],
    "summary": "",
}
counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
frag["summary"] = (f"Round 3, slice M2-d: {len(rows)} rows, PASS {counts.get('PASS',0)}, FAIL {counts.get('FAIL',0)}. "
    "FAIL rows: M2-d-cards-L19-L20 (c285 overclaims 'needs the whole Hessian'); M2-d-prose-L21-R1-forward-ref (L21 Research R1 relies on L23 Proposition 2.1, a later lesson); "
    "M2-d-cards-L24 (c370 states M_3 = e where the lesson says M_3 approximately e). Round-2 FAIL rows re-verified and fixed: M2-d-math-L21-thm2.1-ex3.2, M2-d-math-L23-quiz-essential, M2-d-prose-L19-hypothesis-count, M2-d-prose-L21-assumed-name, M2-d-cards-L24 (c363, c364).")
json.dump(frag, open(sys.argv[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(rows), counts)
