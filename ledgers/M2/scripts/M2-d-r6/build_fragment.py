# Builds ledgers/M2/M2-d.json (round 6, slice d). Hand-checked row content; no network used.
import json
from datetime import datetime, timezone

P = "PASS"
F = "FAIL"
W = "course/modules/M/M2/"
S = "ledgers/M2/scripts/M2-d-r6/"
rows = []

def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)

# ---- gates and runs (run by this verifier on pin 44f1eb6) ----
row("G-check-pages", "check_pages gate for M2 (structure, cards, links)", "tools/check_pages.py --all",
    P, "Command `.venv/bin/python tools/check_pages.py --all` exit 0; output line `check_pages M2: PASS`.")
row("G-check-dag", "check_dag gate for M2 (prerequisite closure)", "tools/check_dag.py --all",
    P, "Exit 0; output line `check_dag M2: PASS`.")
for p in ["L19", "L20", "L21", "L22", "L23", "L24"]:
    row(f"G-run-labs-{p}", f"run_labs: lab of {p} matches twin, twin output matches page expected block",
        f"tools/run_labs.py --unit M2 --page {p} and {W}{p}.html <section class=\"lab\">",
        P, f"`run_labs M2: PASS (1/1)` for {p}; run_labs checks code byte-identity to tests/labs/M2/lab-M2-{p}-1.py and expected block.")
row("G-twins-isolated", "Each twin alone under python -I -W error, no stderr",
    "tests/labs/M2/lab-M2-L19-1.py .. lab-M2-L24-1.py",
    P, "Exit 0 for all six; outputs saved in " + S + "lab_L*_twin.out.")
row("G-page-smoke", "page_smoke on the six slice pages (Chromium)", "tools/page_smoke.py --unit M2 --pages L19..L24",
    P, "Exit 0; `page_smoke M2: PASS`; each page PASS (" + S + "M2d_smoke.out).")
row("G-ruff", "ruff check and ruff format --check on six twins", "tests/labs/M2/lab-M2-L19-1.py, L20..L24 twins",
    P, "`All checks passed!` and `6 files already formatted`, exit 0.")
row("G-mypy", "mypy --no-incremental on six twins", "tests/labs/M2/lab-M2-L19..L24-1.py",
    P, "`Success: no issues found in 6 source files`, exit 0.")
row("G-pytest-labs", "pytest tests/test_labs.py -k M2", "tests/test_labs.py",
    P, "27 tests passed (all M2 lab checks) under `.venv/bin/pytest -q tests/test_labs.py -k M2`.")
row("G-verify-refs", "verify_refs --offline integrity", "tools/verify_refs.py --offline",
    P, "`offline integrity: 560 entries, 0 problems`, exit 0.")
row("G-build-site", "build_site --check (site data current)", "tools/build_site.py --check",
    P, "`site data current: 6 outputs`, exit 0.")

# ---- L19 ----
row("L19-math-def-ex", "Def 1.1 and Example 1.2 Hessian values; Problems M1-M3, P1-P3", W + "L19.html lines ~50-60, ~330-360",
    P, "Recomputed by hand: f_x=3x^2+2y^2 -> 11 at (1,2); f_y=4xy-1 -> 7; Hessian [[6,8],[8,4]]; M2 quadratic gives [[2,1],[1,2]]; P1 f_xy=f_yx=6xy^2; P3 H=[[e^x y, e^x],[e^x,0]].")
row("L19-math-thm21", "Theorem 2.1 proof (mean value twice, bound, limit in k then h)", W + "L19.html Theorem 2.1 and proof",
    P, "Re-derived each step: Delta=hk f_xy(xi,eta); |xi-a|<=|h|, |eta-b|<=|k|; with |h|,|k|<delta/2 the point is within delta/sqrt2<delta of p; limit in k gives difference quotient of f_y; epsilon argument closes. No gap found.")
row("L19-math-ex22", "Example 2.2 counterexample f_xy(0,0)=-1, f_yx(0,0)=1; discontinuity of f_xy", W + "L19.html lines ~70-80 (Example 2.2)",
    P, "Exact f_x(0,y)=-y and f_y(x,0)=x re-derived; numeric difference quotients (" + S + "check_math.out) give -0.499999999996 vs -0.5 and 0.499999999996 vs 0.5; " + S + "check_fxy.out: f_xy(t,0) -> 1 while f_xy(0,t)=-1 for t=0.1,0.01,0.001, so f_xy is discontinuous at 0 and f_xy(0,0)=-1 as stated.")
row("L19-math-thm31", "Theorem 3.1 remainder bound 2|h|^2 omega(|h|)", W + "L19.html Theorem 3.1 and proof",
    P, "Checked (|h1|+|h2|)^2 <= 2|h|^2 and mean value bound on phi''; phi(1)=s1 phi''(s2) with phi'(0)=0; omega nondecreasing; all steps valid.")
row("L19-math-prop33", "Proposition 3.3 cubic term and E(s)/E(s/2)->8", W + "L19.html Proposition 3.3",
    P, "Lagrange remainder (1/6)g'''(theta)s^3; E(s/2) denominator (1/48)g'''(0)s^3; ratio 8. Correct.")
row("L19-math-remark-R2-R3", "Remark 3.2; Research R2 (n|h|^2 bound) and R3 (m, omega<m/4)", W + "L19.html Remark 3.2, res-2, res-3",
    P, "Re-derived: sum_{i<j}2|h_i||h_j| argument gives n|h|^2; threshold omega(|s|)<m/4 independent of d; R2 bound n=3 correct.")
row("L19-prose-lab-numbers", "Prose numbers vs printed lab output (gradient, Hessian, 2.26e-11, 1.94e-11, ratios)", W + "L19.html lab interpretation; " + S + "lab_L19_twin.out",
    P, "Independent recomputation: f_x=0.474680, f_y=1.898721, f_xx=0.412180, f_xy=2.148721; all printed values in prose match the expected block and the twin output exactly to the printed digits.")
row("L19-scope-words", "Scope words (smooth, small) need a computation", W + "L19.html interpretation and E1",
    P, "'because f is smooth' refers to exp(x)y+xy^2, a closed-form C-infinity function; no unsupported 'always/only' scope. Note only, not a defect.")
row("L19-canon-misconception-quiz", "Canon breaks, misconceptions, quiz answers (2, 12, 2, -1, 8, 0)", W + "L19.html sections 4, 5, 8",
    P, "Quiz answers recomputed: f_xy of x^2y =2; x^3y at (2,1) =12; e^x y f_xx at (0,2)=2; g''(0)=2 for x^2+3xy; all correct.")

# ---- L20 ----
row("L20-math-thm12", "Theorem 1.2 value 5/3 and proof splitting", W + "L20.html Theorem 1.2",
    P, "Recomputed: int_0^1 int_0^2 (xy+x^2) = 5/3; sums converge to (1/2)(2)+(1/3)(2)=5/3; sum of Delta y_j = 2.")
row("L20-math-prop22", "Proposition 2.2 both orders equal 5/3", W + "L20.html Proposition 2.2 and proof",
    P, "y-first inner 2x+2x^2 -> 1+2/3; x-first inner y/2+1/3 -> 1+2/3; both 5/3.")
row("L20-math-prop24", "Proposition 2.4 midpoint error -1/(6n^2) in both orders", W + "L20.html Proposition 2.4 and proof",
    P, "Exact Fraction recomputation (" + S + "check_math.out) n=1,2,3,5,8: 3/2, 13/8, 89/54, 83/50, 213/128, each equal to 5/3-1/(6n^2). Proof: sum (2i+1)^2 = n(4n^2-1)/3 induction step re-derived; midpoint sum of x^2 is 1/3-1/(12n^2).")
row("L20-math-ex31", "Example 3.1 iterated integrals pi/4 and -pi/4 under Assumption 3.1", W + "L20.html Example 3.1",
    P, "d/dy[y/(x^2+y^2)] = (x^2-y^2)/(x^2+y^2)^2 and d/dx[-x/(x^2+y^2)] = same; numeric inner integral at x=0.5 gives 0.800000 = 1/(1+x^2); at x=1 gives 0.500000; outer integrals pi/4 and -pi/4; f(t,0)=1/t^2 correct.")
row("L20-prose-lab", "Lab 1 prose vs output (exact errors -1/6, -1/24, -1/96; six n values; odd-square identity to n=50)", W + "L20.html lab interpretation; " + S + "lab_L20_twin.out",
    P, "Twin output: n=1..32 errors -1/6,-1/24,-1/96,-1/384,-1/1536,-1/6144, both orders match True; prose statements match exactly.")
row("L20-quiz-misc", "Quiz answers and misconception 3 (4/3 for int_0^2 int_0^1 xy^2; 3 for (x+y) integral)", W + "L20.html section 7 and misconceptions",
    P, "int_0^1 xy^2 dx = y^2/2; int_0^2 y^2/2 dy = 4/3; int_0^1 int_0^2 (x+y) dy dx = 3. Correct.")

# ---- L21 ----
row("L21-math-thm12", "Theorem 1.2 (implicit-function theorem) proof: sign, box, uniqueness, continuity, differentiability", W + "L21.html Theorem 1.2 and proof",
    P, "Re-derived: F(x0,y0-c)<0<F(x0,y0+c) and continuity give I; zero unique by strict monotonicity; mean value identity 0 = h F_x(xi,y2) + (y2-y1) F_y(x1,eta) checked; I x J inside R where F_y>0.")
row("L21-math-thm21-ex22", "Theorem 2.1 slope formula, Example 2.2 (-0.75), Remark 2.3", W + "L21.html Theorem 2.1, Example 2.2",
    P, "g'=-F_x/F_y re-derived by chain rule; circle slope -2(0.6)/(2(0.8)) = -0.75; sqrt(1-x^2) derivative -x/sqrt(1-x^2) = -0.75 at 0.6.")
row("L21-math-ex31-32", "Example 3.1 (dx/dy = -y/sqrt(1-y^2), zero at y=0) and Example 3.2 (no implicit function at origin); canon example F=y^3-x", W + "L21.html Examples 3.1, 3.2, Section 3",
    P, "x^2+y^2 with g(0)=0 forces x^2+g^2>0 for x!=0 (no solution); y^3=x gives y=x^(1/3) over R with F_y=3y^2=0 at origin, so the condition is sufficient, not necessary; all checked.")
row("L21-prose-lab", "Lab 1 slopes and residuals vs independent bisection root and formula", W + "L21.html lab interpretation; " + S + "lab_L21_twin.out; " + S + "check_math.out",
    P, "Independent bisection: x=0.25 y=0.9168754789 formula -0.33076532 fd -0.33076532; x=1 y=0.6823278038 slope -0.28469308; all printed digits match. F_y in 2.40..2.77 matches 'between about 2.4 and 2.8'.")
row("L21-problems", "Problems M1-M3, P1-P3, R1 (dy/dP0 = 1/P'(y) < 0), R2 Jacobian, R3 (L08 Theorem 2.1 remainder bound)",
    W + "L21.html problem set", P,
    "M1 slope -1; M2 -1; M3 -1; R1 sign from P'<0 correct; R3 first-order error bound (1/2)sup|g''|dx^2 is the Lagrange bound (L08 Theorem 2.1 is Taylor with Lagrange remainder, verified in L08.html line 90).")

# ---- L22 ----
row("L22-math-lemma-thm13", "Lemma 1.2 and Theorem 1.3 proofs (interior FOC, chain rule)", W + "L22.html Lemma 1.2, Theorem 1.3",
    P, "Lemma one-sided argument valid; chain rule V'=f_x xhat' + f_a with f_x=0 gives V'=f_a. Re-derived.")
row("L22-math-remark14", "Remark 1.4: H3 locally from L21 Theorem 1.2 applied to F=f_x", W + "L22.html Remark 1.4",
    P, "F=f_x is C^1 when f is C^2; partial in x is f_xx != 0; uniqueness of the zero of f_x(.,a) in J follows from F_x != 0 on I x J (strict monotonicity); citation to L21 Theorem 1.2 matches L21.html.")
row("L22-math-ex15-prop21", "Example 1.5 (V'=ln a), Example 2.2 (a/2), M3 (a/4), Proposition 2.1 formula", W + "L22.html Example 1.5, Proposition 2.1, Examples 2.2-2.3, Mechanics M1-M3",
    P, "Recomputed: f_x=a/(1+x)-1 zero at a-1; V=a ln a-(a-1), V'=ln a; x+2y=a gives V=a^2/8, V'=a/4; M1 V=a^2/2; M2 V=3a+9/4, V'=3. All correct.")
row("L22-math-ex23-P2", "Example 2.3 and proof P2 (V=max(a,0), one-sided derivatives 1 and 0)", W + "L22.html Example 2.3, P2",
    P, "a>0 maximizer x=1, V=a; a<0 x=0, V=0; V(h)-V(0)=h for h>0 and 0 for h<0. Correct.")
row("L22-prose-lab", "Lab 1 prose numbers (1e-8 location error, f_xx=-0.666667, 3.3e-17, Part B 5.4e-12)", W + "L22.html lab interpretation and misconception 3; " + S + "lab_L22_twin.out",
    P, "Printed values reproduce the expected block; sqrt(2.2e-16)~1.5e-8; 0.5*0.6667*1e-16=3.3e-17; all match. The explanation is labelled as an explanation.")
row("L22-lab-naive-partial", "Lab 1 Part B prints a naive partial that the code asserts rather than computes",
    W + "L22.html lab hypothesis (line 99) vs " + "tests/labs/M2/lab-M2-L22-1.py lines 99-100", F,
    "Code sets `reduced_partial = x_star` and `naive_partial = 0.0` as literals and prints them (lines 99-103). The page says the lab 'prints the naive partial derivative of x*y with respect to a at fixed x and y, which is 0' as a check; the printed 0 cannot fail and no partial is evaluated. Output still matches the expected block (run_labs PASS).",
    "Compute the naive partial from the objective (for example, a central difference of a -> x*y at fixed x, y, which is 0 by construction of the function), or reword the hypothesis to say the value is a constant written by the lab, and drop the 'reduced F_a' column or compute it from F(x,a)=x(a-x).")
row("L22-prop21-hypothesis", "Proposition 2.1 states every hypothesis explicitly (Architect rule)", W + "L22.html line 226", F,
    "'Let f be continuously differentiable on an open set containing the relevant points' does not name the set, and 'the relevant points' is undefined; the domain of c is not stated ('c continuously differentiable').",
    "Replace with: f is C^1 on an open set U in R^3 containing {(xhat(a), c(xhat(a),a), a) : a in I}, and c is C^1 on an open set containing {(xhat(a), a)}; state both sets in the statement.")

# ---- L23 ----
row("L23-math-prop21", "Proposition 2.1 closed-form P', P'' and signs", W + "L23.html Proposition 2.1 and proof",
    P, "Term-by-term derivative of c_t(1+y)^(-t): -t c_t (1+y)^(-t-1); second derivative t(t+1)c_t(1+y)^(-t-2); signs correct for positive c_t. Numerics: P'(0.04)=-851466.739529, P''=8376648.511919 match the lab.")
row("L23-math-prop22", "Proposition 2.2 price equals face at coupon-rate yield (geometric series)", W + "L23.html Proposition 2.2 and proof",
    P, "v=1/(1+y); 1-v=yv; sum v^t=(1-v^N)/y; yF*sum = F(1-v^N); total F. Numeric: P(0.05)=100000.000000 (check_math.out). Hypothesis text (coupon yF at years t<N plus face in last coupon) is consistent with the proof; the last coupon yF+F is implied.")
row("L23-math-thm31-prop32-33", "Theorem 3.1 (Lagrange remainder), Proposition 3.2 (sign of -Delta), Proposition 3.3 (tangent below price)",
    W + "L23.html Theorem 3.1, Propositions 3.2, 3.3", P,
    "P'''=-sum t(t+1)(t+2)c_t(1+y)^(-t-3) < 0 re-derived; R=(1/6)P'''(theta)Delta^3 has sign of -Delta; P-P1=(1/2)P''(theta)Delta^2 >= 0. Numerics: remainders -15.0608 at +0.01 and +16.0101 at -0.01 (check_math.out), sign of -Delta.")
row("L23-prose-numbers", "Prose numbers in L23 (108110.895779, -851466.74, 8376648.51, 1.9, 7.875864, 77.482001, -1777.07)",
    W + "L23.html why-it-matters, lab interpretation, misconceptions, quiz; " + S + "check_math.out", P,
    "All recomputed independently: 108110.895779; -851466.739529; 8376648.511919; -P'/P=7.875864; P''/P=77.482001; two-cash-flow example P'(0.04)=-1777.068 printed as -1777.07 in the quiz explanation (rounding to two decimals is correct).")
row("L23-problems-quiz", "Mechanics M1-M3, quiz answers (1000, -200, 100000 at coupon rate), Research R1 sign", W + "L23.html problem set and quiz", P,
    "M1: 50/1.05+1050/1.05^2 = 1000.000 (recomputed); M2 derivatives of c(1+y)^-1; M3: P'(0)=-200 for 100(1+y)^-2; R1 dy/dP0=1/P'(y)<0; all correct.")
row("L23-cards-meta-introduces", "Meta line 'Introduces: none (this lesson defines no concept)' against the lesson text",
    W + "L23.html line 38 vs Definition 1.1 (line ~58) and 'at par' sentence (line ~62)", F,
    "Definition 1.1 defines the price function and the sentence 'A bond priced at its face value is said to be at par' defines a term; the meta line says the lesson defines no concept. Also no <dfn>, so the concept index is consistent; the claim in the meta line is not.",
    "Change the meta line to 'Introduces: none as a concept in the index (Definition 1.1 and the term at par are prose definitions)', or add the term to the index and drop the claim.")
row("L23-notation-F", "NOTATION: symbol F used with one meaning per lesson", W + "L23.html line 80 (face value F) and line 361 (R1: F(P_0,y)=P(y)-P_0)", F,
    "The same lesson uses F for the face value (Proposition 2.2, 'face value F', 'F v^N') and for a two-variable function F(P_0, y) in Research problem R1. Not a registered symbol, but the same letter has two meanings within one lesson.",
    "Rename the function in R1 (for example G(P_0, y) = P(y) - P_0) or the face value.")
row("L23-money-int-cents", "Architect decision: bond price in integer cents, 'no float money anywhere' (plans/M2-build-plan.md line 365; Q12 line 312)",
    W + "L23.html Definition 1.1 line 59, Section 4 bullet line 255; tests/labs/M2/lab-M2-L23-1.py lines 34-35 (price returns float), 56-65 (taylor_first/second float money)", F,
    "The page defines P(y) as 'a real number of cents before rounding' and the lab computes money as float throughout (price(), taylor_first(), taylor_second()); only the printed price is an int (price_cents). The binding plan rule says no float money anywhere. Honest disclosure is present on the page, but the rule is not met.",
    "Compute the money path in integers or Fraction/Decimal and round once (price_cents) with the rounding rule stated; or obtain an Architect decision that the Taylor money approximations are sensitivities and record that on the page (Architect Q12).")

# ---- L24 ----
row("L24-math-thm21", "Theorem 2.1 quotients of |x| at 0 and no derivative", W + "L24.html Theorem 2.1 and proof",
    P, "D+=1, D-=-1, D0=0 for every h>0 re-derived; one-sided limits differ; run_labs Part A matches. Correct.")
row("L24-math-prop31-32", "Proposition 3.1 and 3.2 truncation proofs", W + "L24.html Propositions 3.1, 3.2 and proofs",
    P, "Prop 3.2: f(x+h)-f(x-h)=2hf'+(1/6)h^3(f'''(xi1)+f'''(xi2)); D0-f'=(1/12)h^2(...); bound (1/6)M3h^2 correct. Prop 3.1: 1/2 M2 h correct.")
row("L24-math-prop42-43", "Proposition 4.2 and 4.3 minimizers and minimum values; prose constants 1.8e-8 and 6.3e-6",
    W + "L24.html Propositions 4.2, 4.3, lab hypothesis, interpretation", P,
    "A=M2/2, B=2delta: h*=2sqrt(delta/M2), min 2sqrt(M2 delta); C=M3/6, B=delta: h^3=3delta/M3. Numerics: 2sqrt(2.22e-16/e)=1.807e-8, (3*2.22e-16/e)^(1/3)=6.257e-6 (check_math.out). R1 factor-of-10 claim correct (2delta/h* = sqrt(M2 delta)).")
row("L24-prose-lab-table", "Lab 1 Part B prose vs printed table (6.603e-9 at 1e-8, 2.154e-7 at 1e-9, 3.263e-5, 3.903e-1, 5.859e-11 tie with 1e-7)",
    W + "L24.html interpretation and misconception 1; " + S + "lab_L24_twin.out", P,
    "All printed values in prose match the twin output line-for-line; truncation term 0.5*e*1e-5=1.359e-5 matches; central factor-of-100 per decade matches 4.533e-3, 4.530e-5, 4.530e-7, 4.531e-9.")
row("L24-problems-quiz", "Mechanics M1-M3, Proof P1-P3, Empirical E1-E3, Research R1-R3, quiz answers", W + "L24.html problem set and quiz", P,
    "M1 errors h, -h, 0 for x^2; M2 at h=0.5 gives 0 and 1; M3 D+=12.61, error 0.61 <= 0.63; P3 rewrite identity correct; E2 bound 2delta/1e-15 = 0.444 vs printed 0.390 consistent; R2 Lipschitz bound correct; quiz h*=1 correct.")
row("L24-meta-introduces", "Meta line 'Introduces: none (this lesson defines no concept)' against the lesson text",
    W + "L24.html line 38 vs Definition 4.1 and the word 'cancellation' (Section 4)", F,
    "Definition 4.1 defines the error hypothesis and Section 4 introduces 'cancellation' as a named term; the meta line says the lesson defines no concept.",
    "Replace the meta line with the terms actually introduced, or state that these are prose-defined terms without index entries.")
row("L24-AD-link", "Forward reference to automatic differentiation in L14 (research R3)", W + "L24.html research R3; L14.html Definition 1.1", P,
    "L14.html line 58 defines automatic differentiation (def-automatic-differentiation); L24 names it as 'treated in Lesson L14', which is an earlier lesson.")

# ---- cards ----
row("CARDS-slice", "cards.json entries for L19-L24 (97 cards): ids unique, fronts unique, lesson fields, grades, numbers, wording vs lesson text",
    W + "cards.json (M2-c280..c377 for L19-L24)", P,
    "Python check: 97 slice cards, no duplicate ids or fronts; grade-C cards all carry a basis; every number quoted in a card appears in its lesson or in the lab expected block (e.g. 108110.895779, -851466.739529, 7.875864, 2.26e-11, 6.603e-09, 5.859e-11). Each card's answer matches the current lesson text (checked card by card against Propositions, Theorems, Examples, misconceptions and lab interpretation). Out-of-slice note: M2-c376 (lesson L01) sits between L24 cards; not a slice defect.")

# ---- DAG / concepts / registry / hours / structure ----
row("DAG-links-anchors", "Every concept link anchor in L19-L24 resolves to a def id on the target page",
    W + "L19..L24 concept links", P,
    "def-derivative (L04), def-limit (L01), def-definite-integral (L09), def-partial-derivative (L16), def-gradient (L17), def-jacobian (L18), def-taylor-theorem (L08), def-finite-difference-derivative (L13), def-hessian, def-multiple-integral, def-implicit-function-theorem, def-envelope-theorem (own page); concepts.html ids present-value, discount-factor, geometric-series exist.")
row("DAG-prereq-use", "Lessons used in text are earlier in the sequence (L09 Corollary 2.3, L10 FTC, L08 Theorem 2.1, L13, L14, L18, L21)",
    W + "L19..L24 prose", P,
    "L09.html Corollary 2.3 is 'Riemann sums converge at the mesh rate' for monotone f (line 114); L10 Theorem 2.1 is FTC evaluation form (line 74); L08.html Theorem 2.1 is Taylor with Lagrange remainder (line 90); L13 defines finite-difference derivative; L14 defines automatic differentiation; L18 Jacobian; all earlier than the citing lesson.")
row("DAG-architect-decisions", "Architect decisions: Fubini prose-only, no multiplier concept, duration/convexity unlinked",
    W + "L20.html Remark 2.3; L22.html (no multiplier); L23.html lab preview text", P,
    "No dfn or link to fubini-theorem, lagrange-multiplier or duration/convexity anywhere in L19-L24 (grep); Remark 2.3 is prose and graded none.")
row("HOURS", "Hours arithmetic: lesson data-hours and hub split", "course/modules/M/M2/L19..L24.html line 2; course/modules/M/M2/index.html line 29", P,
    "Each slice page data-hours=10 (eyebrow '10 study hours'); hub data-hours-lessons=240 for 24 lessons and data-hours-project=60, consistent with plan Q1.")
row("STRUCT-process-words", "No process words in learner text (round, verifier, builder, draft, TODO, placeholder)", W + "L19..L24.html", P,
    "grep over the six pages: no hits.")
row("STRUCT-scope-words", "Scope words (small, smooth, always, every, only) used only with a computation", W + "L19..L24.html", P,
    "Scope words found: 'smooth' (L19, L24) describe closed-form functions shown in labs; 'small' (L23, L21, L22) cite printed numbers. No unsupported 'always/only'. Notes only.")
row("STRUCT-define-before-use", "Terms defined or linked at first appearance", W + "L19..L24.html", P,
    "Hessian, mesh, tags, value function, (H1)-(H3), Assumption 1.1/3.1/4.1, error hypothesis and cancellation all defined before use within their lesson.")
row("REF-registry", "Cited registry keys exist; no locator attributed from memory",
    W + "L19..L24.html references sections; references/references.json", P,
    "spivak2008calculus and hubbard2015vector are present in references/references.json (verify_refs offline PASS). Pages state no locator is confirmed; no statement is attributed to them.")
row("NOTATION-registry", "Registered symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q, macros) not reused in slice",
    "notation/notation.json vs L19..L24", P,
    "No registered symbol appears in L19..L24 with another meaning (R is used for remainders and rectangles but R^* / R_f / R^{e*} are not used). Locally defined letters (N, M, R, F) are handled per lesson, with the F clash in L23 recorded as a separate row.")

fragment = {
    "unit": "M2",
    "slice": "d",
    "round": 6,
    "verifier": "Haiku 5.5 independent verifier, slice d (L19-L24), round 6",
    "pin": "44f1eb6",
    "base": "44f1eb6",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB6-M2-d",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyB6-M2-d/ledgers/M2/scripts/M2-d-r6",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 6 from scratch (no round-5 fragment exists at /Users/billyribeiro/.fanout/frags/B-M2-d.round5.json, so no PASS was carried). "
        "Read all six lesson pages in full, all six twins, all 97 slice cards. Lab twins are demonstrations; no grader mutation rows "
        "(mutation testing applies to project graders only). Could not check: the project slice; check_projects does not list M2 in its output; "
        "rendered visual layout beyond page_smoke; the Chromium diff of live figures (none on these pages). "
        "Notation: no registered symbol reused; the local F clash in L23 is a FAIL row."
    ),
    "summary": "Slice d (L19-L24): 5 FAIL rows (1 medium: float money vs binding integer-cents rule; 4 low: lab naive partial hard-coded, vague Proposition 2.1 hypothesis, F reused in L23, two 'defines no concept' meta lines). All math re-derived PASS; all gates PASS.",
}

out = "ledgers/M2/M2-d.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=1, ensure_ascii=False)
print("wrote", out, "rows", len(rows), "fails", sum(1 for r in rows if r["status"] == F))
