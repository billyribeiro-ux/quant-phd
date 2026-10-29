import json, datetime

P = "PASS"
F = "FAIL"
rows = []

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)

S = "ledgers/M2/scripts/M2-d-r11/"

# ---- gates (all re-run on pin f42f432 this round) ----
row("G-check-pages", "gate", "tools/check_pages.py --unit M2", P, S + "check_pages.out: 'check_pages M2: PASS', exit 0.")
row("G-check-dag", "gate", "tools/check_dag.py --all", P, S + "check_dag.out: 'check_dag M2: PASS', exit 0 (all units PASS).")
row("G-check-projects", "gate", "tools/check_projects.py --all", P, S + "check_projects.out: all units PASS, exit 0.")
row("G-run-labs-L19", "2.5-labs", "tools/run_labs.py --unit M2; course/modules/M/M2/L19.html expected block", P,
    S + "run_labs_M2.out: 'run_labs M2: PASS (27/27)', exit 0; expected_vs_twin.py: L19 expected 10 lines equal twin stdout.")
row("G-run-labs-L20", "2.5-labs", "tools/run_labs.py --unit M2; course/modules/M/M2/L20.html expected block", P,
    S + "run_labs_M2.out (27/27); expected_vs_twin.py: L20 expected 8 lines equal twin stdout.")
row("G-run-labs-L21", "2.5-labs", "tools/run_labs.py --unit M2; course/modules/M/M2/L21.html expected block", P,
    S + "run_labs_M2.out (27/27); expected_vs_twin.py: L21 expected 5 lines equal twin stdout.")
row("G-run-labs-L22", "2.5-labs", "tools/run_labs.py --unit M2; course/modules/M/M2/L22.html expected block", P,
    S + "run_labs_M2.out (27/27); expected_vs_twin.py: L22 expected 9 lines equal twin stdout.")
row("G-run-labs-L23", "2.5-labs", "tools/run_labs.py --unit M2; course/modules/M/M2/L23.html expected block", P,
    S + "run_labs_M2.out (27/27); expected_vs_twin.py: L23 expected 11 lines equal twin_L23.out (the changed twin).")
row("G-run-labs-L24", "2.5-labs", "tools/run_labs.py --unit M2; course/modules/M/M2/L24.html expected block", P,
    S + "run_labs_M2.out (27/27); expected_vs_twin.py: L24 expected 25 lines equal twin stdout.")
row("G-twins-isolated", "2.5-labs", "tests/labs/M2/lab-M2-L19-1.py .. lab-M2-L24-1.py under python -I -W error", P,
    S + "twin_L19..L24.out and .err: exit 0 for all six, stderr 0 bytes.")
row("G-page-smoke", "2.9-smoke", "tools/page_smoke.py --unit M2 (covers L19..L24)", P,
    S + "page_smoke_M2.out: 'page_smoke M2: PASS', exit 0. Run for the whole unit, not for the slice alone.")
row("G-ruff", "gate", "ruff check tests/labs/M2/", P, S + "ruff.out: 'All checks passed!', exit 0.")
row("G-ruff-format", "gate", "ruff format --check tests/labs/M2/", P, S + "ruff_format.out: '27 files already formatted', exit 0.")
row("G-mypy", "gate", "mypy --no-incremental (full repo)", P, S + "mypy_full.out: 'Success: no issues found in 255 source files', exit 0.")
row("G-pytest-labs", "gate", "pytest tests/test_labs.py -k M2", P, S + "pytest_labs_M2.out: 27 passed, exit 0.")
row("G-pytest-docs-figures", "gate", "pytest tests/test_docs_figures.py", P, S + "pytest_docs.out: 14 passed, exit 0.")
row("G-verify-refs", "gate", "tools/verify_refs.py --offline", P, S + "verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0.")
row("G-build-site", "gate", "tools/build_site.py --check", P, S + "build_site_check.out: 'site data current: 6 outputs', exit 0.")
row("G-page-vs-twin", "2.5-labs", "course/modules/M/M2/L19..L24.html <code data-run> vs tests/labs/M2/lab-M2-L19..L24-1.py", P,
    S + "page_vs_twin.py: code block equals twin (after rstrip of trailing newline) for all six pages.")

# ---- L19 math and prose (re-read in full this round) ----
row("L19-math-def-ex", "2.4-math", "course/modules/M/M2/L19.html Definition 1.1, Example 1.2, Example 2.2 (lines ~24-38 of text extract)", P,
    "Example 1.2 Hessian [[6,8],[8,4]] recomputed; Example 2.2 f_xy(0,0)=-1, f_yx(0,0)=1 recomputed from f_x(0,y)=-y and f_y(x,0)=x.")
row("L19-math-thm21", "2.4-math", "L19.html Theorem 2.1 (line 70-74 raw) and proof (Steps 1-3, raw lines 80-82)", P,
    "Re-derived: Step 1 MVT twice gives Delta=hk f_xy(xi,eta); Step 2 bound |xi-a|,|eta-b|<=|h|,|k| and distance < delta; Step 3 limit in k then eps-argument. Hypothesis now 'Assuming Assumption 2.1 of Lesson L06'; L06 Assumption 2.1 is the EVT (L06.html line 72) and MVT is Theorem 2.3 (L06.html line 87) — both citations checked.")
row("L19-math-ex22", "2.4-math", "L19.html Example 2.2 (counterexample) and the sentence on f_xy discontinuity", P,
    "f(h,y)=hy(h^2-y^2)/(h^2+y^2) gives f_x(0,y)=-y; f_y(x,0)=x; f_xy(0,0)=-1, f_yx(0,0)=1 recomputed by hand. Exists-off-origin claim holds (nonvanishing denominator).")
row("L19-math-thm31", "2.4-math", "L19.html Theorem 3.1 and proof (raw lines ~95-105)", P,
    "Proof re-derived: phi(0)=phi'(0)=0, phi''(t)=h^T(H(p+th)-H(p))h; MVT twice gives |phi(1)|<=sup|phi''|; |h^T M h|<=(|h1|+|h2|)^2 max|M_ij|<=2|h|^2 max|M_ij|; so |R|<=2|h|^2 omega(|h|). Assumption-2.1 prefix matches the MVT use.")
row("L19-math-prop33", "2.4-math", "L19.html Proposition 3.3 and proof (text lines 52-55)", P,
    "E(s)=(1/6)g'''(theta s)s^3 by Lagrange form (L08 Theorem 2.1 under L08 Assumption 1.1 = EVT, L08.html line 61); E(s)/E(s/2)->8 recomputed: (1/6)/(1/48)=8.")
row("L19-math-remark-R2-R3", "2.4-math", "L19.html Remark 3.2 (line 51), Problems R2 and R3 solutions", P,
    "Remark 3.2 corrected term 1/2 d1 d2 (f_xy+f_yx) recomputed from 1/2 d^T H d; equals d1 d2 f_xy under symmetry. R2: (sum|h_i|)^2<=n|h|^2 by Cauchy-Schwarz, so bound n|h|^2 omega for n=3. R3: m=min over unit circle, bound s^2(m/2-2omega), positive iff omega<m/4 — re-derived.")
row("L19-prose-lab-numbers", "2.3-prose-numbers", "L19.html Lab 1 interpretation (text line 152) vs twin_L19.out", P,
    "2.26e-11, 1.94e-11, ratios 3.9509/3.9750/3.9874 and 7.8836/7.9429/7.9717 match twin output; ratio definition (previous over current) matches lab code previous_first/e1.")
row("L19-scope-words", "2.8-scope", "L19.html scope words (only, all, every, always, exactly) in revised sentences", P,
    "'every h', 'every x' etc. are quantified by the stated hypotheses; no unqualified universal claim introduced in this delta.")
row("L19-canon-misconception-quiz", "2.4-prose", "L19.html Section 4, Section 5 misconceptions, Section 8 quiz", P,
    "Misconception 1 counterexample Example 2.2 consistent with Theorem 2.1 as restated; quiz answers recomputed: f_xy=2 (x^2 y at (1,1)), f_xy=12 (x^3 y at (2,1)), f_xx=2 (e^x y at (0,2)).")

# ---- L19 cards (fail: omit new Assumption 2.1 hypothesis) ----
row("CARDS-L19-theorem-hypotheses", "2.4-cards", "cards.json M2-c282 (Theorem 2.1), M2-c284 (Theorem 3.1), M2-c286 (Proposition 3.3)", F,
    "Lesson statements now begin 'Assuming Assumption 2.1 of Lesson L06 (the extreme value theorem)' (L19.html lines ~70, ~97, ~115) but these card backs state the hypotheses without it (checked with 'Assumption 2.1' substring test: absent).",
    "Prefix each card back's hypotheses with 'Assuming Assumption 2.1 of Lesson 6 (the extreme value theorem)' so the card carries the lesson's hypothesis.")

# ---- L20 ----
row("L20-math-thm12", "2.4-math", "L20.html Theorem 1.2 and proof (text lines 25-30)", P,
    "Split S=(sum xi dx)(sum eta dy)+(sum xi^2 dx)(sum dy) re-derived; limits 1/2*2+1/3*2=5/3. Monotone-integrand Riemann convergence cited to L09 Corollary 2.3 (L09.html line 49, rate bound delta*|f(b)-f(a)|).")
row("L20-math-prop22", "2.4-math", "L20.html Proposition 2.2 and proof (text lines 34-37)", P,
    "int_0^2(xy+x^2)dy=2x+2x^2, int_0^1=5/3; other order int_0^1 = y/2+1/3, int_0^2=5/3 recomputed.")
row("L20-math-ex31", "2.4-math", "L20.html Example 3.1 (text lines 123-126) and Assumption 3.1 (line 210)", P,
    "d/dy[y/(x^2+y^2)]=(x^2-y^2)/(x^2+y^2)^2 and d/dx[-x/(x^2+y^2)] = same; inner integrals 1/(1+x^2) and -1/(1+y^2); outer pi/4 and -pi/4 under arctan facts; f(t,0)=1/t^2 recomputed.")
row("L20-math-prop24", "2.4-math", "L20.html Proposition 2.4 and proof (text lines 115-120)", P,
    "sum_{i<n}(2i+1)^2=n(4n^2-1)/3 induction step rechecked: n(4n^2-1)+3(2n+1)^2=4n^3+12n^2+11n+3=(n+1)(4(n+1)^2-1). x-outer and y-outer both give 5/3-1/(6n^2). Lab output for n=1..32 equals the formula (twin_L20.out).")
row("L20-prose-lab", "2.5-labs", "L20.html Lab 1 prediction (line 41) and expected block", P,
    "Predicted 3/2 and 13/8 for n=1,2 match expected block; the 50-term odd-squares identity claim matches twin code range(1,51).")
row("L20-quiz-misc", "2.4-prose", "L20.html Problems M1-M3, P1-P3, E1-E3, R1-R3 and quiz", P,
    "M1 = 3 both orders; M2 = 2/3 both orders; M3 sum 3/2, error -1/6; quiz 4/3 for int_0^2 int_0^1 xy^2 dx dy recomputed.")
row("L20-problems-res2", "2.4-prose", "L20.html Remark 2.3 and Problem R2 solution (text line ~186)", P,
    "Remark 2.3 leaves the general closed-rectangle statement unproved and uncited; R2 solution consistent with it.")
row("L20-prose-lab-interp", "2.3-prose-numbers", "L20.html Lab 1 interpretation (text line 114)", P,
    "Output lines 107-112 match 'match True' claims; computed sums 3/2, 13/8, 53/32, 213/128, 853/512, 3413/2048 exact.")
row("L20-remark23-no-proof-depends", "2.4-prose", "L20.html Remark 2.3 (text line 39)", P,
    "No later proof in L20 uses the general statement (Theorem 1.2 and Proposition 2.2 are proved directly).")
row("STRUCT-define-before-use", "2.5-structure", "course/modules/M/M2/L20.html line 209 (Example 3.1) uses Assumption 3.1 before its statement on line 210", F,
    "Example 3.1 says 'assuming Assumption 3.1 (inverse tangent, stated below on this page)'; Assumption 3.1 is stated on the next line (L20.html line 210). The term is used before its definition (round-10 finding not yet fixed).",
    "Move the Assumption 3.1 block (line 210) above Example 3.1 (line 209) and drop the words 'stated below on this page'.")

# ---- L21 ----
row("L21-math-thm12", "2.4-math", "L21.html Theorem 1.2 and proof (raw lines 74-80)", P,
    "Re-derived: strict monotonicity in y on [y0-c,y0+c]; I chosen with F(x,y0-c)<0<F(x,y0+c) for |x-x0|<a1 so I x J in R; continuity via sign change; differentiability via MVT in x then in y, giving slope -F_x/F_y. Uniqueness of zero in J comes from strict monotonicity in the proof. Citations to L06 Assumption 2.1 and Theorem 2.3 checked.")
row("L21-math-thm21-ex22", "2.4-math", "L21.html Theorem 2.1 (line 38), Example 2.2 (line 42), Remark 2.3 (line 44)", P,
    "Chain-rule proof valid; -2x/2y = -0.75 at (0.6,0.8) recomputed; closed form g(x)=sqrt(1-x^2) gives -0.6/0.8.")
row("L21-math-ex31-32", "2.4-math", "L21.html Example 3.1 (line ~109) and Example 3.2 (line ~111, raw line 196)", P,
    "Circle at (1,0): F_y=0, F_x=2, dx/dy=-y/sqrt(1-y^2)=0 at y=0 recomputed. Example 3.2: x^2+g(x)^2>0 for x != 0 contradicts F(x,g(x))=0 on an open interval containing 0.")
row("L21-problems", "2.4-prose", "L21.html Research R1 solution (text line 167), P1-P3 and M1-M3 solutions", P,
    "Round-10 FAIL cleared: R1 solution now begins 'Assuming Assumption 1.3 and Assumption 2.1 of Lesson L06' and says the sign rests on P'(y)<0 and Assumption 1.3. dy/dP0 = 1/P'(y) recomputed. M1 slope -1, M2 slope -1, M3 slope -1 recomputed.")
row("L21-prose-lab", "2.3-prose-numbers", "L21.html Lab 1 interpretation (text line 105), expected block and E1-E3", P,
    "Residuals, F_y range 2.40-2.77 and differences 6.2e-13, 5.2e-14, 3.7e-12, 3.9e-12 match twin output lines 101-104; y=0.6823278038 and slope -0.2846930800 at x=1 match output (card M2-c314).")
row("L21-prose-duplicate", "2.5-structure", "course/modules/M/M2/L21.html line 201 (Section 3 bullet 'The slope formula needs F_y')", F,
    "The sentence reads 'There the curve is a graph over \\(y\\), There the curve is a graph over \\(y\\), and the theorem ...' (duplicated clause, confirmed in raw HTML by grep).",
    "Delete the duplicated clause so the sentence reads 'There the curve is a graph over \\(y\\), and the theorem with the roles of the variables exchanged ...'.")

# ---- L22 ----
row("L22-math-lemma-thm13", "2.4-math", "L22.html Lemma 1.2 (proof, raw text) and Theorem 1.3 with proof (text lines 25-36)", P,
    "Lemma proof: a positive derivative gives larger values for small t>0; Theorem proof: chain rule with f_x=0 gives V'=f_a. Re-derived.")
row("L22-math-remark14", "2.4-math", "L22.html Remark 1.4 (text line 38)", P,
    "Apply L21 Theorem 1.2 to G(a,x)=f_x(x,a) with dG/dx = f_xx != 0; zero of f_x(.,a) in J unique because F_y has constant sign on I x J in the L21 proof. Assumption 1.3 and Assumption 2.1 of L06 named correctly.")
row("L22-math-ex15-prop21", "2.4-math", "L22.html Example 1.5 (text line 40), Proposition 2.1 and proof (text lines 150-153)", P,
    "f_x=a/(1+x)-1, x_hat=a-1, V=a ln a-(a-1), V'=ln a recomputed; Proposition 2.1 chain rule V'=g_y c_a+g_a re-derived.")
row("L22-math-ex23-P2", "2.4-math", "L22.html Example 2.3 (text line 157) and P2 solution (text line ~191)", P,
    "V(a)=max(a,0): one-sided derivatives 1 and 0 at a=0 recomputed; formula f_a(1,a)=1 for a>0 consistent with V'=1.")
row("L22-prose-lab", "2.3-prose-numbers", "L22.html Lab 1 interpretation (text line 146), misconception 3 (line 167)", P,
    "x_hat errors 1e-8 and central differences match ln a to 8 decimals (twin_L22.out); 0.5*0.667*1e-16 ~ 3.3e-17 recomputed; sqrt(2.2e-16)~1.5e-8 consistent with 'about 1e-8'.")
row("L22-lab-naive-partial", "2.5-labs", "L22.html Lab 1 Part B expected block (lines 142-145) and lab code lines 126-135", P,
    "Naive partial prints 0 by construction (frozen_product has no a); central difference of V matches a/2 to 5.4e-12 (twin output).")
row("L22-prop21-hypothesis", "2.4-math", "L22.html Proposition 2.1 hypotheses (text line 150)", P,
    "Hypotheses (g C^1 on open U containing graph of c, c C^1, F satisfies H1-H3) are sufficient for the proof given.")

# ---- L23 ----
row("L23-math-prop21", "2.4-math", "L23.html Proposition 2.1 and proof (text lines 27-31)", P,
    "Term-by-term derivatives re-derived: d/dy(1+y)^{-t}=-t(1+y)^{-t-1}; second derivative t(t+1)(1+y)^{-t-2}; signs for positive c_t.")
row("L23-math-prop22", "2.4-math", "L23.html Proposition 2.2 and proof (text lines 32-35)", P,
    "Geometric series with v=1/(1+r): 1-v=rv, sum v^t=(1-v^N)/r, price F(1-v^N)+Fv^N=F recomputed. Par example 50/1.05+1050/1.05^2=1000 recomputed.")
row("L23-math-thm31-prop32-33", "2.4-math", "L23.html Theorem 3.1 (text line 145), Propositions 3.2 (line 149) and 3.3 (line 153), proofs (lines 147-155)", P,
    "Lagrange remainder R=(1/6)P'''(theta)Delta^3 with P'''<0 for positive c_t gives sign -Delta; P-P1 = (1/2)P''(theta)Delta^2 >= 0. Hypothesis statements now carry Assumption 2.1 of L06 for the Lagrange form (L08 Assumption 1.1 = EVT).")
row("L23-prose-numbers", "2.3-prose-numbers", "L23.html Lab 1 interpretation (text line 142), E1/E2 solutions (lines ~364-372), why-it-matters (line 20)", P,
    "108110.895779 cents, 108111 cents, P'=-851466.739529 (diff 1.6e-3), P''=8376648.511919 (diff 1.9), ratios 3.9279/3.9634 and 7.8807/7.9396, differences -15 and +16 cents, exact prices 100000 and 117060 all match twin_L23.out and were recomputed by the twin code. Preview numbers 7.875864 and 77.482001 are printed only.")
row("L23-problems-quiz", "2.4-prose", "L23.html M1-M3, P1-P3, R1-R3 solutions and quiz (text lines 172-250)", P,
    "M2 P'=-c(1+y)^{-2}, P''=2c(1+y)^{-3} recomputed; M3 P'(0.04)=-200/1.04^3 recomputed; P2 P'''<0 recomputed; R2 bound 1/6 M|Delta|^3 with M over wider interval, not computed on page: consistent.")
row("L23-cards-meta-introduces", "2.9-structure", "L23.html meta-row line 38 and description line 7", P,
    "'at par' is defined in Section 1 (raw HTML: 'A bond priced at its face value is said to be at par.'); no concept index entry needed (architect Q8).")
row("L23-notation-F", "2.9-notation", "L23.html face value F in Proposition 2.2 and Section 2", P,
    "F is used for face value only in the L23 page; NOTATION registry (notation/notation.json, 8 entries) has no F entry, so no conflict.")
row("L23-money-int-cents", "2.4-math", "L23.html Section 4 bullet 'Money is rounded once' (text line 161) and Lab 1 Part C", P,
    "Q12: sensitivities are floats with a stated error bound (relative 2^-53, lines 161 and twin docstring); price exact Fraction, rounded once with round() (halves to even). Code checked: price_second_derivative returns float(exact).")
row("L23-E3-exactly-face", "2.4-prose", "L23.html E3 solution (text line ~367): 'because Proposition 2.2 gives exactly face there'", F,
    "Measured with twin code: the lab evaluates at the float 0.04+0.01 = 0.05 (float), whose exact value differs from 1/20 by 1/360287970189639680; the exact price at that float is 100000 - 2.14e-12 cents, not exactly face. The rounded price 100000 is correct. The 'exactly face' attribution is true only at the rational yield 5 percent.",
    "Replace with: 'Proposition 2.2 gives exactly face at the yield 5 percent; the float yield differs from 5 percent by about 3.6e-18, which moves the unrounded price by about 2e-12 cents, so the rounded price is 100000.'")

# ---- L23 cards ----
row("CARDS-c357-rounding", "2.4-cards", "cards.json M2-c357 (How is the bond price rounded to cents?)", F,
    "Back says 'The price, its derivatives and the Taylor terms are exact rational numbers ... so no rounding happens inside the calculation'. Current L23 section 4 and Q12 say P'(y0) and P''(y0) are floats, each rounded once to the nearest double. Card contradicts the lesson.",
    "Rewrite the back: 'The price and the Taylor polynomials are exact rationals computed from the float yields with Fraction; the two sensitivities P' and P'' are floats, each rounded once to the nearest double. The price is rounded to an integer number of cents once, at the end, with halves to even (Section 4).'")
row("CARDS-hypothesis-carry", "2.4-cards", "cards.json M2-c348, M2-c349, M2-c350 (L23); M2-c360, M2-c361, M2-c363, M2-c364 (L24)", F,
    "Lesson statements now begin 'Assuming Assumption 2.1 of Lesson L06 (the extreme value theorem)' (L23.html lines ~145, 149, 153; L24.html lines ~72, 82, 105, 115) but these card backs omit it (substring test: absent).",
    "Add 'Assuming Assumption 2.1 of Lesson 6 (the extreme value theorem)' to each card back's hypotheses.")
row("CARDS-slice-numbers", "2.4-cards", "cards.json: all 96 cards of L19-L24 (ids M2-c280..M2-c387)", P,
    "Every number-bearing back was compared with the twin output or the lesson text (e.g. c287-c289, c313-c314, c328-c329, c341-c346, c382-c385, c311, c301, c300); all match. Non-numeric backs read for consistency; only the five cards named in the FAIL rows are stale.")
row("CARDS-slice-remark-check", "2.4-cards", "cards.json M2-c285 (Remark 3.2), M2-c292, M2-c299, M2-c351", P,
    "c285 coefficient d^T H d matches Remark 3.2; c292 f_xy=f_yx=-1,1 at origin matches Example 2.2; c299 says the general statement is not proved, consistent with Remark 2.3; c351 consistent with Remark 3.4.")

# ---- L24 ----
row("L24-math-thm21", "2.4-math", "L24.html Theorem 2.1 and proof (text lines 25-27)", P,
    "|x| forward/backward/central quotients 1, -1, 0 at every h>0 recomputed with exact Fractions for h=10^-1..10^-6 (output in S/ scripts).")
row("L24-math-prop31-32", "2.4-math", "L24.html Propositions 3.1-3.2 and proofs (text lines 31-40)", P,
    "Taylor forms re-derived: D+ - f' = (1/2) h f''(xi); D0 - f' = (1/12) h^2 (f'''(xi1)+f'''(xi2)), |.|<=(1/6) M3 h^2.")
row("L24-math-prop42-43", "2.4-math", "L24.html Propositions 4.2-4.3 and proofs (text lines 46-52)", P,
    "Minimisers h*=2 sqrt(delta/M2) and (3 delta/M3)^(1/3) re-derived; bound values 2 sqrt(M2 delta) checked; quotient error 2delta/h and delta/h match Definition 4.1 arithmetic.")
row("L24-prose-lab-table", "2.3-prose-numbers", "L24.html Lab 1 interpretation (text line 146), E1-E3 solutions", P,
    "Forward errors 1.406e-1 to 1.359e-5, central fall ~100x per decade to 1e-4, 5.859e-11 at 1e-5, rises to 3.903e-1 at 1e-15 all match twin output. Predicted minimisers 1.807e-8 and 6.257e-6 recomputed. Unrounded central errors 5.858691e-11 (1e-5) and 5.858736e-11 (1e-7) differ by 4.44e-16 (recomputed by script).")
row("L24-problems-quiz", "2.4-prose", "L24.html M1-M3, P1-P3, R1-R3 solutions and quiz (text lines 162-263)", P,
    "M1 quotients h, -h, exact 2; M3 D+ = 12.61, error 0.61 <= 0.63 bound recomputed; R1 overestimate factor 100 gives step h*/10 and round-off 10 sqrt(M2 delta) recomputed; quiz h*=1 for delta=0.5, M2=2 recomputed.")
row("L24-meta-introduces", "2.9-structure", "L24.html meta-row line 38", P, "Concepts introduced match the page content; no undeclared concept link.")
row("L24-AD-link", "2.4-prose", "L24.html R3 solution (text line ~212) and L14 forward-mode AD", P,
    "R3 points to L14 for forward-mode AD; L14 is in the prerequisite closure per check_dag M2: PASS.")
row("L24-solution-unrounded-errors", "2.3-prose-numbers", "L24.html E3 solution (text line 199)", P,
    "5.858691e-11 and 5.858736e-11 differ by 4.4e-16 (one ulp near e) — recomputed by script, see scripts/l24_check.py output.")

# ---- DAG / concepts / notation / refs / hours ----
row("DAG-prereq-use", "2.7-dag", "tools/check_dag.py --all (M2: PASS); L19-L24 concept links", P,
    "check_dag M2 PASS. Concept links in slice pages point to existing anchors (L01, L04, L08, L09, L13, L16, L21, M1 concepts page). L23 uses M1 present value and discount factor (prerequisite).")
row("DAG-links-anchors", "2.7-dag", "data-concept links in L19-L24", P,
    "Definitions: hessian (L19), multiple-integral (L20), implicit-function-theorem (L21), envelope-theorem (L22) each exactly one <dfn>; links resolve to their definitions.")
row("DAG-architect-decisions", "2.7-dag", "plans/M2-build-plan.md 'Architect decisions (binding)' Q2-Q12 vs slice pages", P,
    "Q2: no M3 concept link (none found). Q3: Fubini not cited, stated as unproved (L20 Remark 2.3). Q4: no Lagrange multiplier in L22 (grep: Lagrange only as Taylor form in L23/L24). Q8: duration and convexity unlinked (L23). Q12: floats for sensitivities with stated bound (L23 section 4).")
row("HOURS", "2.6-hours", "course/modules/M/M2/index.html (unchanged since e8b10b8) and L19-L24 data-hours", P,
    "data-hours=10 on each of L19..L24 both at e8b10b8 and f42f432; index card kicker 'L19 · 10 h' ... 'L24 · 10 h' unchanged; no hours arithmetic changed.")
row("STRUCT-process-words", "2.9-structure", "L19-L24 learner text (plain-text extract, grep for verif/builder/round/batch/revis/architect)", P,
    "Only 'verify' appears, in the mathematical sense (L19 Problem P3 'verify that it is symmetric'; L20 Problem R1 'Definition 1.1 is not verified for it'); no process words.")
row("STRUCT-scope-words", "2.8-scope", "L19-L24 scope words (only, all, always, every, any, same, exactly)", P,
    "Universal claims checked: 'the price ... exactly face' is the one false instance, recorded as L23-E3-exactly-face. Others quantified by explicit hypotheses.")
row("STRUCT-define-before-use-other", "2.5-structure", "L19-L24 defined terms, excluding Assumption 3.1 (L20)", P,
    "Assumption 1.3 (L21, line ~25) precedes use in Theorem 1.2; Assumption 1.1 of L22 and L23 are referenced to L08 and L22 correctly; L24 Assumption 4.1 introduced before the Lab uses it.")
row("REF-registry", "2.9-refs", "tools/verify_refs.py --offline; references sections of L19-L24", P,
    "offline integrity 560 entries, 0 problems. Pages cite spivak2008calculus and hubbard2015vector only as curriculum sources with no locator, as the pages state.")
row("NOTATION-registry", "2.9-notation", "notation/notation.json (8 registered symbols) vs L19-L24 symbols", P,
    "Registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q are not used in L19-L24. Local symbols (R remainder in L19; R rectangle in L20; F function in L21/L22 and face in L23) are not program-wide and are not registered.")

# ---- cross-lesson citations that the delta added ----
row("CITE-L06-A21", "2.9-refs", "L06.html Assumption 2.1 (line 72) and Theorem 2.3 (line 87); L08.html Assumption 1.1 (line 61), Theorem 2.1, Theorem 1.2", P,
    "Every new 'Assumption 2.1 of Lesson L06 (the extreme value theorem)' points at L06 line 72, which is the EVT; 'Theorem 2.3 of Lesson 6' is the MVT (line 87); L08 Assumption 1.1 is the EVT (line 61). Checked for L19, L20, L21, L22, L23, L24 uses.")

verdict = "FAIL" if any(r["status"] == F for r in rows) else "PASS"

frag = {
    "unit": "M2",
    "slice": "d",
    "round": 11,
    "verifier": "Haiku 5.5 independent verifier, slice d (L19-L24), round 11",
    "pin": "f42f432",
    "base": "e8b10b8",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB11-M2-d",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyB11-M2-d/ledgers/M2/scripts/M2-d-r11",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": verdict,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [
        "cards.json changed in e8b10b8..f42f432 for ids outside this slice (M2-c111 L08, M2-c389 L08 new, M2-c180 L12, M2-c212 L14, M2-c258 L17); not verified by this slice."
    ],
    "notes": [
        "Delta e8b10b8..f42f432 touches L19, L20, L21, L22, L23, L24 pages, tests/labs/M2/lab-M2-L23-1.py, and cards.json. Lab twins L19-L22 and L24 are byte-identical since e8b10b8; all six pages were re-read in full (plain-text extract plus raw HTML for truncated math) and every changed hunk was read.",
        "Round-10 FAIL STRUCT-define-before-use (L20 Assumption 3.1 forward use) is still present: FAIL carried, not cleared.",
        "Round-10 FAIL L21-problems is cleared (R1 now carries the Assumption prefix).",
        "Round-10 FAIL PLAN-Q12-sensitivity-type is cleared at canon-breaks (L23 section 4 now says floats); the stale card M2-c357 is a new FAIL row.",
        "Not a mutation slice: lab twins are demonstrations, so no mutants were run; project graders are outside slice d.",
        "Not checked: the full text of every card back word-for-word for non-numeric, non-hypothesis cards (read for consistency; no defect found); cards for L08, L12, L14, L17 changed in the delta are outside this slice; the whole-unit course gates beyond the listed ones (run_graders, mutate_graders, page_smoke alone per page) were not run because the slice has no graders; hours were checked only as data-hours values, not as a hub-split recomputation.",
    ],
    "rows": rows,
    "summary": {
        "slice": "d (L19-L24)",
        "verdict": verdict,
        "counts": {
            "rows": len(rows),
            "PASS": sum(1 for r in rows if r["status"] == P),
            "FAIL": sum(1 for r in rows if r["status"] == F),
        },
        "fails": [r["id"] for r in rows if r["status"] == F],
    },
}

import sys
sys.path.insert(0, "tools")
import importlib.util
spec = importlib.util.spec_from_file_location("ledger", "tools/ledger.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
problems = mod.validate(frag, "M2-d")
print("validate:", problems)
json.dump(frag, open("ledgers/M2/M2-d.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("rows", len(rows), "verdict", verdict, "fails", frag["summary"]["fails"])
