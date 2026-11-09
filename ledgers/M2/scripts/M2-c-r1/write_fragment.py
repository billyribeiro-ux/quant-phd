import json

S = "ledgers/M2/scripts/M2-c-r1/"
rows = []

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

# ---- gates and tools (run by this verifier on pin aeb512b) ----
row("M2c-gate-check-pages", "2.9-structure", "course/modules/M/M2/L13.html ... L18.html; cards.json", "PASS",
    "tools/check_pages.py --unit M2 -> 'check_pages M2: PASS'; per page: check_pages.py --unit M2 --page L13 ... L18 -> each 'check_pages M2 Lnn: PASS'.")
row("M2c-gate-check-dag", "2.9-DAG", "course/modules/M/M2/L13.html ... L18.html", "PASS",
    "tools/check_dag.py --unit M2 -> 'check_dag M2: PASS'. dfn ids on the slice: L13 def-finite-difference-derivative, L14 def-automatic-differentiation, L16 def-partial-derivative, L17 def-gradient, L18 def-jacobian; each defined once; L15 defines none. Concept links point to L01, L04, L08, L13, L16, L17 (earlier or same) or to concepts.html#exponential-and-logarithm (owner M1 in curriculum.json).")
row("M2c-gate-run-labs", "2.5-labs", "tests/labs/M2/lab-M2-L13-1.py ... lab-M2-L18-1.py", "PASS",
    "tools/run_labs.py --unit M2 --page L13 ... --page L18: each 'run_labs M2: PASS (1/1)'. Interpreter: .venv/bin/python 3.14.8.")
row("M2c-gate-check-projects", "gate", "course/modules/M/M2/project.html, grader/", "PASS",
    "tools/check_projects.py --unit M2 -> 'check_projects M2: PASS'. Not a slice-c subject; run because the plan's command list includes it.")
row("M2c-gate-page-smoke", "2.9-smoke", "course/modules/M/M2/L13.html ... L18.html", "PASS",
    "tools/page_smoke.py --unit M2 --pages L13 L14 L15 L16 L17 L18, run alone: 'page_smoke modules/M/M2/L13.html: PASS' through L18.html: PASS; 'page_smoke M2: PASS'; lab timings 0.0 s each; runtime boot 1.1 s.")
row("M2c-gate-pytest", "gate", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py", "PASS",
    ".venv/bin/python -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -> all tests pass, exit 0.")
row("M2c-verify-refs", "2.1-citations", "references/references.json: spivak2008calculus, hubbard2015vector", "PASS",
    "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0. The unit-scoped live run (verify_refs.py --unit M2) needs the network and was not used. Plain curl, following the redirect: https://openlibrary.org/isbn/9780914098911.json -> 'Calculus', 2008, 'Publish or Perish, inc' (OL28292750M, matches spivak2008calculus); https://openlibrary.org/isbn/9780971576681.json -> 'Vector Calculus, Linear Algebra, and Differential Forms', 2015, 'Matrix Editions' (OL35954342M, matches hubbard2015vector).")
row("M2c-attribution", "2.1-attribution", "L13-L18 References sections; curriculum/01-foundations.yaml:145-147", "PASS",
    "No slice page has data-cite or attributes a result to a source (grep data-cite: 0 on all six pages). References sections name Spivak and Hubbard & Hubbard only as curriculum sources; curriculum/01-foundations.yaml:145-147 gives 'Spivak, Calculus, 4th ed. (2008)' and 'Hubbard & Hubbard, Vector Calculus, Linear Algebra, and Differential Forms, 5th ed. (2015)', matching references.json titles and years. The pages say no passage locator is confirmed. Named standard results (Cauchy-Schwarz, Lagrange remainder, mean value and intermediate value theorems) are used or proved on the page and are not attributed to a source.")
row("M2c-grades", "2.3-grades", "L13-L18 block-title spans with data-grade", "PASS",
    "Re-graded against BLUEPRINT section 3. Proved results are T: L13 Thm 2.1, 2.2, Prop 3.2, Cor 4.1; L14 Prop 3.1, 5.2; L15 Prop 2.1, 2.2, 3.1, Cor 3.2, Prop 3.5, 3.6; L16 Prop 2.1, 3.1; L17 Thm 2.2, 3.1; L18 Prop 3.2, 3.3, Thm 4.1. Lab results are C with the lab named as basis on every page. Results that rest on Assumption 1 are T with the assumption named, which the rules allow. No A, B, D or X grade is used and I found no over-grade. Registry convention noted under registry_flags.")
row("M2c-data-figures", "2.8-data", "L13-L18", "PASS",
    "grep -c on the six pages: '<svg' 0, 'data-chart' 0, 'data-files' 0. The slice has no dataset, no figure and no simulated data (closed forms, no RNG), so no SIMULATED label is needed and no MANIFEST row applies.")
row("M2c-notation", "13-notation", "L13-L18 math; notation/notation.json", "PASS",
    "notation.json registers T, \\Phi (and inverse), \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. " + S + "macro_census.py over the six pages: registry macro used = \\R only; every registered symbol has 0 hits in slice math. Other macros are standard KaTeX. Slice symbols delta, xi, varepsilon (dual unit in L14), M, B, C_h, D_h, e_i are not registry symbols, each keeps one meaning per lesson. Note: e is Euler's number in L13-L18 and e_i is a basis vector in L16 Def 1.1; standard usage, not a collision.")
row("M2c-banned-scan", "1.3-1.4 banned phrases", "L13-L18 HTML, cards.json (slice cards)", "PASS",
    "grep -i -E 'TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|well known|obviously|clearly|motivat' on the six pages and a script over the slice cards: no hits. One word hit, 'omitted' in the L13 Problem R3 title ('The size of the omitted rounding of the point'), is content, not the banned phrase 'details omitted'. Ellipsis hits are the one code docstring at tests/labs/M2/lab-M2-L15-1.py:34 ('4 pi/count, ...' list continuation, not omitted content) and mathematical dots.")
row("M2c-process-words", "12-process-words", "L13-L18 learner text and cards", "PASS",
    "grep -i -E 'builder|verifier|architect|reviewer|agent|ledger|round [0-9]|Q[0-9]+ ' on the six pages and slice cards: no hits.")
row("M2c-dag-forward-mentions", "2.9-DAG / 1.10", "L15.html:38; L16.html (Section 3 and Section 4 text)", "PASS",
    "L15 'Introduces' line says it prepares 'the gradient of Lesson L17' and L16 names Lesson L18 Theorem 4.1 and Lesson L17's directional derivative. These are plain-text pointers, not concept links or uses before definition (gradient is defined in L17 def-gradient; directional derivative is not a curriculum concept). No link targets a later lesson.")
row("M2c-terms-before-definition", "2.9 / 5-terms", "L14.html:73 vs L14.html:79 (Assumption 1); L18.html:340 (o(|h|))", "PASS",
    "L14 says 'under Assumption 1' at line 73, before the labelled 'Assumption 1.' at line 79 in the same section; the reference is to a labelled assumption that is stated three lines later, and no reader is left without its meaning. Noted, not a defect. L18 Problem R2 uses little-o notation o(|h|), which is not in notation.json and is not defined on the page; standard notation, noted only.")
row("M2c-hours", "2.9-hours", "L13-L18 data-hours; course/modules/M/M2/index.html", "PASS",
    "data-hours=10 on each of L13, L14, L15, L16, L17, L18 (sum 60 for the slice). Lessons are within 6-12 h. Hub split (240 + 60) is checked by check_pages --unit M2 (PASS) and is outside this slice.")
row("M2c-structure", "2.9-structure", "L13-L18 HTML", "PASS",
    "Section order per BUILDER_RULES 4.2 on all six: Why it matters, core sections, Where the canon breaks, Misconceptions, Problem set, Key results, Retrieval quiz (References after the quiz). 'Why it matters' word counts by script: L13 106, L14 102, L15 89, L16 49, L17 83, L18 88 (all <= 120). Each page: 12 solutions in details.solution (3 per tier, tiers Mechanics, Proof, Empirical, Research); 3 misconceptions; quiz items 10, 10, 10, 10, 10, 9 (8-15). Script: " + S + "check_structure.py.")
row("M2c-quiz-keys", "2.9-quiz", "L13-L18 quiz sections", "PASS",
    "Script " + S + "check_quiz_keys.py printed each item with its keyed option and explanation. Every keyed answer is the correct option (e.g. L13 q1 central quotient; L14 q5 'Two forward and one backward'; L15 q9 0.3849002; L17 q7 corner (1,1) at 45 degrees; L18 q5 hypothesis of Thm 4.1). Each item has an explanation div. Answer-only items carry their answer.")
for n, ids in [(13, "Thm 2.1 (h/2 f''(xi)), Thm 2.2 (h^2/6 f'''(xi)), Prop 3.2, Cor 4.1, P3, Example 2.3 bounds, E1, E2, E3, R1, R3, Section 5 claims"),
               (14, "Def 2.1 quotient/exp/sin rules, Prop 3.1 induction, Ex 4.1, Prop 5.2 (reverse pass), P1-P3, E1-E3, R1-R3, Section 6 branch examples"),
               (15, "Prop 2.1, 2.2, Ex 2.4, Ex 3.3, Ex 3.4, Prop 3.5, Prop 3.6, Cor 3.2, P1-P3, E1-E3, R1-R3"),
               (16, "Remark 1.2, Prop 2.1, Prop 3.1, Ex 1.3, M1-M3, P1-P3, E1-E3, R1-R3"),
               (17, "Def 1.1, Ex 1.2, Thm 2.2 (telescoping + MVT), Ex 2.3, Thm 3.1, Section 4 counterexamples, M1-M3, P1-P3, E1-E3, R1-R3"),
               (18, "Prop 3.2, Prop 3.3, Thm 4.1 (telescoping + MVT), Ex 4.2, M1-M3, P1-P3, E1-E3, R1 (f=(x^2+y^2)sin(1/rho)), R3")]:
    pass  # rows written below per lesson with explicit evidence

row("M2c-L13-numbers", "2.2-numbers", "course/modules/M/M2/L13.html (Lab 1 prose, Sections 2-5, Problems)", "PASS",
    "Script " + S + "verify_numbers.py recomputes: e*h/2 = 1.3591409e-2, e*h^2/6 = 4.5304697e-5, e^1.01*0.005 = 1.3728005e-2, e^0.99*h^2/6 = 4.4853908e-5, e^1.01*h^2/6 = 4.5760017e-5 (matches 0.0135914, 0.0137280, 4.4854e-5, 4.5760e-5); unrounded forward/central ratio at 1e-2 = 301.0010 (prose 301.0; printed digits 301.1038 (prose 301.1)); 2.154e-7/6.603e-9 = 32.6215 (32.6); full-precision central errors at 1e-5 and 1e-7 differ by 4.4e-16 (<1e-15); E2 2delta/h = 4.4409e-8 and 4.4409e-7, ratio to e*h/2 at 1e-9 = 326.74 (327); E3 3delta/e = 2.45057e-16, cube root 6.25781e-6 (6.25781e-6); R1 2sqrt(1e-3/e) = 3.83604e-2 (0.038360); R3 2^-53/1e-8 = 1.1102e-8, e times that = 3.0179e-8 (3.0e-8); Cor 4.1 2sqrt(e*delta) = 4.9136e-8 (4.9e-8); Lab 1 predictions 2sqrt(delta/e) = 1.8076e-8 and (3delta/e)^(1/3) = 6.2578e-6; E1 bounds 10e^-0.001 = 9.9900 and 10e^0.01 = 10.1005; central bounds 100e^-0.011 = 98.91 and 100e^0.011 = 101.11; M3 sin(0.01)/0.01 - 1 = -1.66666e-5, (0.01/2)sin(0.01) = 4.9999e-5; P3 B_c(h*) = 3delta/(2h*) follows from M3 h*^2 = 3 delta/h*. Every prose number matches the recomputation to the printed digits.")
row("M2c-L13-theorems", "2.4-math", "L13.html Thm 2.1, 2.2, Prop 3.2, Cor 4.1, P3, Section 5", "PASS",
    "Re-derived by hand: Thm 2.1 Taylor order one, D_h f - f' = (h/2) f''(xi); Thm 2.2 subtraction of the two order-two expansions gives (h^2/12)(f'''(xi+)+f'''(xi-)) = (h^2/6) m, IVT for xi; Prop 3.2 numerator difference <= 2 delta, /h and /2h; Cor 4.1 B'(h) = M/2 - 2delta/h^2, B'' = 4delta/h^3 > 0, B(h*) = 2 sqrt(M delta); P3 h^3 = 3delta/M3, derivative (M3/3)h - delta/h^2. Hypotheses listed in every statement (continuous f'' or f''' on the closed interval; delta > 0, M > 0; h* <= h0). Section 5 kink example: forward quotient 1 and central quotient 0 for |t| at 0 checked.")
row("M2c-L13-lab1", "2.5-labs", "L13.html Lab 1 (lab-M2-L13-1)", "PASS",
    "Twin run under python -I -W error: exit 0, empty stderr. Output recomputed; forward minimum at 1e-08 (6.603e-09), central minimum at 1e-05 (5.859e-11), tie with 1e-07 (5.8587e-11 vs 5.8587e-11) at three digits; the page says the sweep does not resolve it. Predicted steps 1.8e-8 and 6.3e-6 sit at the printed decades. Interpretation claims (forward column falls ~10 per decade, central ~100, growth below 1e-8) match the printed table.")
row("M2c-L14-numbers", "2.2-numbers", "L14.html Example 4.1, Lab 1 prose, E1, Key results", "PASS",
    "e^2 = 7.389056099; 2e^2 = 14.778112198; 3e^2 = 22.167168297; sin 2 = 0.909297427; cos 2 = -0.416146837; quotient pieces 0.454648713 and -0.435397775; f(2) = 15.232760911, f'(2) = 21.731770522 (sum of the three closed-form terms also 21.731770522); lab 21.7317705218 agrees to nine decimals; f2'(1) = 2 exp(sin 1) cos 1 = 2.506761534986893... (Decimal series), so '2.506761534986...' is a correct truncation and ten-decimal rounding gives 2.5067615350; the rounded-factor product 2.3197768247 x 0.5403023059 x 2 = 2.5067615351 as stated; Example 5.1 2 + cos 1 = 2.540302306 and sin 1 = 0.841470985.")
row("M2c-L14-theorems", "2.4-math", "L14.html Def 2.1, Prop 3.1, Prop 5.2, P1-P3, R1-R3", "PASS",
    "Dual formulas re-derived: (a+b e)(c+d e) = ac + (ad+bc) e; quotient tangent (bc-ad)/c^2; exp and sin rules. Prop 3.1 induction: product and quotient cases match the L05 rules; exp case uses Assumption 1 and is stated as assumed. Prop 5.2: two paths for x1 (v2 and cos v1), one path for x2 (v1); the statement restricts to the Example 5.1 graph. Code in the twin implements the same tangent rules (__truediv__ and dexp/dsin match Def 2.1). Branch examples (x if x>0 else -x gives -1; x if x>=0 gives +1; max(x,0) tangents 0 and 1) checked by hand.")
row("M2c-L14-assumption1-order", "5-terms", "L14.html:73 and :79", "PASS",
    "Same-section forward reference to labelled Assumption 1 (see M2c-terms-before-definition). Not a defect.")
row("M2c-L14-lab1", "2.5-labs", "L14.html Lab 1 (lab-M2-L14-1)", "PASS",
    "Twin under python -I -W error: exit 0. Output: grid points 251; max-error booleans True for f1 and f2 at 1e-12 (the boolean is the only evidence of the margin; the lab prints no maxima); values at x=2 and f2'(1) as in Example 4.1 and E1. Prose 'below 1e-12 at every one of the 251 points' is the printed True and is stated as one run.")
row("M2c-L15-numbers", "2.2-numbers", "L15.html Prop 3.5, Lab 1 prose, E1, E3", "PASS",
    "2/(3 sqrt 3) = 0.38490018; 1-degree grid maximum of |cos^2 sin| = 0.38487557, attained at 35, 145, 215 and 325 degrees (page prose: 'the printed 0.3849 is the sampled value at 35, 145, 215 and 325 degrees' is correct); 0.38487557 rounds to 0.3849 and is below 0.38490018; asin(1/sqrt3) = 35.264390 degrees, not on the 1-degree grid (page prose correct); g maximum over samples 0.5 at 45 degrees; f(1/n,1/n) = 1/(2n) (0.05 at n=10, 0.00005 at n=10000); R1 limits along y=mx are 0 and along y=x^2 are 1/2 (checked by algebra).")
row("M2c-L15-theorems", "2.4-math", "L15.html Prop 2.1, 2.2, Ex 2.4, Ex 3.3, Ex 3.4, Prop 3.1, 3.5, 3.6, Cor 3.2, P1-P3, R1-R3", "PASS",
    "Cauchy-Schwarz proof re-derived (t = -x.y/|y|^2); triangle inequality from Cauchy-Schwarz; Example 2.4 ball inclusion with s = r - |x-a|; Example 3.3 bound |f| <= |y| <= |(x,y)|, delta = epsilon; Example 3.4 g(1/k,1/k) = 1/2; Prop 3.5 substitution g = (1/2) sin 2 theta, f = r cos^2 sin, derivative 1 - 3s^2; Prop 3.6 contradiction 1/2 vs 0; P2 uses |y-a| >= |x-a| - |y-x|; P3 delta = sqrt(epsilon). All hypotheses stated.")
row("M2c-L15-lab1", "2.5-labs", "L15.html Lab 1 (lab-M2-L15-1)", "PASS",
    "Twin under python -I -W error: exit 0. Printed table: 0.500000 for max |g| at radii 1e-1 to 1e-6; 0.3849 for max |f|/r; sequence rows 0.500000 and 0.05/0.005/0.0005/0.00005. Interpretation: 'the sample is a lower bound for f' and 'cannot show continuity' are consistent with the printed values and the angles computed above.")
row("M2c-L16-numbers", "2.2-numbers", "L16.html Example 1.3, Prop 2.1 prose, Lab 1 prose, E1, E3, R3", "PASS",
    "F_x(1,2) = 4 + 2e^2 = 18.778112198; F_y(1,2) = 1 + e^2 = 8.389056099; largest |F| on the 12-point grid is at (2,1), 4 + e^2 = 11.389056 (prose 11.4); delta = 8.8818e-16 (half spacing near 11.39), delta/h = 8.9e-11 (prose 8.9e-11); truncation bound (1e-10/6) e^2 = 1.23e-10 (prose 1.2e-10); 8e^2 = 59.112 (prose 59.1); 2 + 3e^2 = 24.167168 (E3); R3 truncation (1e-10/6)*20 = 3.33e-10 and total 4.33e-10.")
row("M2c-L16-theorems", "2.4-math", "L16.html Remark 1.2, Prop 2.1, Prop 3.1, P1-P3, R1-R2", "PASS",
    "Partials of F and derivatives in M1-M3 re-derived; Prop 2.1 proof reduces to Thm 2.2 of L13 with phi(t) = f(t,a2); Prop 3.1: axis quotients of g are 0, so both partials exist and equal 0 at the origin, and g is discontinuous by L15 Ex 3.4; R1 diagonal quotient (1/2)/t; R2 coordinates u,v give f = 2u^2 + 2v^2, df/du = 4u; the misconception on f = xy (partial y, diagonal derivative 2x) checked. Hypotheses stated in every proposition.")
row("M2c-L16-lab1", "2.5-labs", "L16.html Lab 1 (lab-M2-L16-1)", "PASS",
    "Twin under python -I -W error: exit 0. Printed: 12 grid points; booleans True for F_x and F_y error below 1e-6; F_x(1,2) = 18.778112 and F_y(1,2) = 8.389056 by both routes; axis quotients 0.0 at t = 1e-3 and 1e-6. Prose matches the output; the lab is labelled C.")
row("M2c-L17-numbers", "2.2-numbers", "L17.html Example 1.2, Lab 1 prose, E2, E3, R1", "PASS",
    "cos 0.5 = 0.8775825619; gradient (1, 1.8775825619); length 2.1272790782; angle atan(1.8775825619) = 61.960246 degrees (prose 61.9602); unit gradient (0.470084, 0.882622) (prose 0.4701, 0.8826); R1 max-norm sup 1 + 1.8775826 = 2.8775826; rescaled gradient (0.532600, 1) with value 2.410182 (prose 2.4102 and unrounded 2.410182); E3 alpha = 0.039754 degrees = 6.938e-4 rad, 1 - cos alpha ~ alpha^2/2 = 2.408e-7, |w|(1 - cos alpha) = 5.12e-7 (prose 2.4e-7 and 5e-7); E2 truncation 7 * 1e-12/6 = 1.17e-12 (prose 1.2e-12), rounding 1e-16/1e-6 = 1e-10.")
row("M2c-L17-theorems", "2.4-math", "L17.html Def 1.1, Def 2.1, Thm 2.2, Ex 2.3, Thm 3.1, Section 4, M1-M3, P1-P3, E1-E3, R1-R3", "PASS",
    "Thm 2.2 telescoping with the mean value theorem along each coordinate step; q_k within |t| of a, continuity at a of the partials gives the limit. Thm 3.1 identity |w - (u.w)u|^2 = |w|^2 - (u.w)^2 re-derived. Section 4: g(tu) = cos(theta) sin(theta) for all t != 0 so the directional derivative exists only in the four axis directions; R2 f = x^2 y/(x^2+y^4) has D_u f(0) = sin theta for cos theta != 0 and D_(0,1) f(0) = 0, partials not continuous at origin (1/(2y) on x = y^2). E2 mean-value bound on |phi'''| <= 6 + 1 checked. Hypotheses stated.")
row("M2c-L17-lab1", "2.5-labs", "L17.html Lab 1 (lab-M2-L17-1)", "PASS",
    "Twin under python -I -W error: exit 0. Printed gradient (1.000000, 1.877583), magnitude 2.127279, angle 61.96, best sampled direction 62 degrees, booleans True. The page says the 1-degree grid cannot locate the maximum more finely; consistent with E3 (alpha = 0.0398 degrees).")
row("M2c-L18-numbers", "2.2-numbers", "L18.html Ex 4.2, Lab 1 prose, E1, E2, E3, R3", "PASS",
    "Jacobian at (1,2) = [[2,-4],[4,2]]; F(1,2) = (-3,4); expansion F(a+h) - F(a) = (2s1 - 4s2 + s1^2 - s2^2, 4s1 + 2s2 + 2s1 s2) verified algebraically; remainder (s1^2 - s2^2, 2 s1 s2) of length |h|^2 (identity (s1^2-s2^2)^2 + 4 s1^2 s2^2 = (s1^2+s2^2)^2); ratio |k| for u=(0.6,0.8); E1 rounding delta = 4.4409e-16 (half spacing at 4), delta/h = 4.4409e-11 (prose 4.4e-11); R3 bound (M/6)h^2 + delta/h and h* = (3 delta/M)^(1/3) consistent with L13 P3.")
row("M2c-L18-theorems", "2.4-math", "L18.html Def 2.1, Def 3.1, Prop 3.2, Prop 3.3, Thm 4.1, P1-P2, Section 5", "PASS",
    "Prop 3.2 uniqueness by the triangle inequality along a unit vector; Prop 3.3 bound |Ah| <= K|h| with K = sum |A_ij|; Thm 4.1 telescoping with the MVT on each coordinate step, omega(rho) continuity at a, bound sqrt(m) n omega(|h|)|h|. Section 5: g of L15 not differentiable at origin (Prop 3.3 and discontinuity); partial d g/dx = y(y^2-x^2)/(x^2+y^2)^2 equals 1/y on the y-axis (unbounded); R1 f = rho^2 sin(1/rho): differentiable with array 0 (|f|/|h| <= |h|), d f/dx along (rho,0) tends to -1 at rho_k = 1/(2 pi k), not 0. All hypotheses stated.")
row("M2c-L18-lab1", "2.5-labs", "L18.html Lab 1 (lab-M2-L18-1)", "PASS",
    "Twin under python -I -W error: exit 0. Printed: 25 grid points; boolean True; Jacobian rows 2.000000 -4.000000 and 4.000000 2.000000; remainder ratios 1.0000e-01 ... 1.0000e-04 equal |k|. Prose says the check is one direction at one point, which matches the code (u = (0.6, 0.8), a = (1, 2) only).")
row("M2c-L18-R2-result-named", "2.4-math / Problems", "L18.html:338-340 (Problem R2 question and solution)", "FAIL",
    "The question asks: 'State the array that the composition G o F should have at a, and say which result this lesson would need to prove it.' The array J_G(F(a)) J_F(a) is stated. The solution then says the proof 'needs the approximation of Definition 3.1 for G at F(a) applied to F(a+h) - F(a)' and 'the argument left open for a later result' without naming the result. The required answer (the chain rule for differentiable maps: differentiability of G o F at a, not stated or proved in L18) is not given, so the second half of the question is unanswered.",
    "Name the result in the solution: the chain rule for differentiable maps (if F is differentiable at a and G at F(a), then G o F is differentiable at a with array J_G(F(a)) J_F(a)). Say that L18 does not state or prove it, and that its proof is Definition 3.1 applied to G at F(a) with the remainder bound of Problem P2. Keep 'Do not prove it here'.")
row("M2c-L13-prose", "2.2-2.9 prose", "L13.html Sections 5, 6, Misconceptions 1-3, quiz explanations", "PASS",
    "Each misconception and canon-break statement checked against the printed numbers and proofs (e.g. 32.6x growth, 301x ratio, kink at |t| with forward 1 and central 0, rounding of x+h at most 2^-53 giving 1.1e-8 relative step, effect 3.0e-8). Key results grades match the proofs and the lab. Assumption 1 usage list (Example 2.3, M3, E1, E2, E3, R3, Lab 1; Section 5, Lab 1, E3, R1 for the value e) matches the uses in the text.")
row("M2c-L14-prose", "2.2-2.9 prose", "L14.html Sections 5, 6, Misconceptions 1-3, Remark 9, key results, quiz", "PASS",
    "Misconception 2 (reverse mode cost) states only the example count and says the general comparison is not proved; Remark 9 says no registry key is cited. Section 6 four points match the four bullets; key-results rows match the proofs (Prop 5.2 is T for the Example 5.1 graph only).")
row("M2c-L15-prose", "2.2-2.9 prose", "L15.html Sections 4, 5, Key results, quiz", "PASS",
    "Section 4 claims ('direction matters', 'a sample is finite', 'value at the point is separate from the limit') match Examples 3.3-3.4 and Propositions 3.5-3.6. Misconception 1 (axes) and 2 (grid) match Example 3.4 and Lab 1. Key-results rows match the proofs.")
row("M2c-L16-prose", "2.2-2.9 prose", "L16.html Sections 3, 4, Misconceptions 1-3, Key results, quiz", "PASS",
    "Section 4 coordinate example (partial depends on the held variable) re-derived; Misconception 2 (f=xy, partial y, diagonal 2x) re-derived; Lab 1 interpretation matches the printed table.")
row("M2c-L17-prose", "2.2-2.9 prose", "L17.html Sections 4, 5, Key results, quiz", "PASS",
    "Section 4 claims (norm dependence; R1 corner (1,1) at 45 degrees; R2 non-linear directional derivative) re-derived. Misconception 3 matches R1. Key-results rows match the proofs.")
row("M2c-L18-prose", "2.2-2.9 prose", "L18.html Sections 5, 6, Key results, quiz", "PASS",
    "Section 5 claims (sufficient not necessary; directional derivative equals A u; f of R2 of L17 not differentiable) re-derived. Misconceptions 1-3 match Prop 3.3 and the Jacobian definition. The R2 gap is recorded separately (M2c-L18-R2-result-named).")
row("M2c-L13-lab-embed", "2.5-labs", "L13.html section lab-M2-L13-1 vs tests/labs/M2/lab-M2-L13-1.py", "PASS",
    "Script " + S + "check_labs_embed.py: code block equals the twin text and expected block equals the twin's stdout under python -I -W error (exit 0). Result 'L13: ... code_equals_twin=True expected_equals_output=True'.")
row("M2c-L14-lab-embed", "2.5-labs", "L14.html lab-M2-L14-1 vs twin", "PASS", "check_labs_embed.py: L14 code_equals_twin=True expected_equals_output=True.")
row("M2c-L15-lab-embed", "2.5-labs", "L15.html lab-M2-L15-1 vs twin", "PASS", "check_labs_embed.py: L15 code_equals_twin=True expected_equals_output=True.")
row("M2c-L16-lab-embed", "2.5-labs", "L16.html lab-M2-L16-1 vs twin", "PASS", "check_labs_embed.py: L16 code_equals_twin=True expected_equals_output=True.")
row("M2c-L17-lab-embed", "2.5-labs", "L17.html lab-M2-L17-1 vs twin", "PASS", "check_labs_embed.py: L17 code_equals_twin=True expected_equals_output=True.")
row("M2c-L18-lab-embed", "2.5-labs", "L18.html lab-M2-L18-1 vs twin", "PASS", "check_labs_embed.py: L18 code_equals_twin=True expected_equals_output=True.")
row("M2c-labs-lint", "2.5-labs", "tests/labs/M2/lab-M2-L13-1.py ... L18-1.py", "PASS",
    ".venv/bin/ruff check tests/labs/M2/lab-M2-L1[3-8]-1.py -> 'All checks passed!'; ruff format --check -> '6 files already formatted'; .venv/bin/mypy tests/labs/M2/lab-M2-L13-1.py ... L18-1.py --no-incremental -> 'Success: no issues found in 6 source files'.")
row("M2c-labs-data", "2.5-labs", "L13-L18 lab sections", "PASS",
    "No data-files attribute, no network, no RNG in any of the six twins (read in full). Hypothesis and interpretation blocks present on each lab section (check_labs_embed.py). Runtime 0.0 s each in page_smoke.")

# ---- cards (every card in the slice was read; samples are groups of ten in file order) ----
row("M2c-cards-sample-01", "2.7-cards", "cards.json M2-c181 ... M2-c190 (L13)", "PASS",
    "Read in full. Definitions (c181, c184), Theorems 2.1, 2.2, Prop 3.2, Cor 4.1, P3 with hypotheses and grades T, Example 2.3 intervals 0.0135914-0.0137280 and 4.4854e-5-4.5760e-5 (both in L13 Key results), ratio interval 9.990-10.101 (in L13 E1). All numbers appear in L13.html.")
row("M2c-cards-sample-02", "2.7-cards", "cards.json M2-c191 ... M2-c200 (L13)", "PASS",
    "Lab 1 C-cards carry basis; 32.6 and 301 ratios match the printed values (recomputed); smaller-step, central-vs-forward and truncation-only misconceptions match Misconceptions 1-3; c199 (2^-53 point shift, 1.1e-8) and c200 (|t| quotients 1 and 0) match Section 5.")
row("M2c-cards-sample-03", "2.7-cards", "cards.json M2-c201, M2-c380, M2-c381, M2-c202 ... M2-c208 (L13-L14)", "PASS",
    "c201 corner (needs continuous f'' on the interval) matches Thm 2.1; c380 lists the Assumption 1 derivatives and users (a subset of the text's first sentence; consistent); c381 forward error growth 2.154e-7 and 1.548e-6 printed by Lab 1; c202-c204 defs match Def 1.1 and 2.1; c206 Example 4.1 values match L14; c207 grid 0.5+i/100, i=0..250 matches the twin; c208 values match the printed lab output.")
row("M2c-cards-sample-04", "2.7-cards", "cards.json M2-c209 ... M2-c218 (L14)", "PASS",
    "c209 value 2.5067615350 printed; c210 adjoints 2.540302306 and 1 match Ex 5.1; c211 Prop 5.2 hypotheses (Assumption 1, x1, x2 real) match; c212 max(x,0) tangents 0 and 1 match R3; c213-c215 match Section 6 bullets; c216-c218 match Misconceptions 1-3.")
row("M2c-cards-sample-05", "2.7-cards", "cards.json M2-c219 ... M2-c228 (L14-L15)", "PASS",
    "c219 quotient tangent (bc-ad)/c^2 matches Def 2.1; c220 norm definition; c221, c222 Cauchy-Schwarz and triangle inequality statements match Prop 2.1, 2.2; c223 open ball/open set matches Def 2.3; c224 Example 2.4 inclusion; c225 closed disc (Misconception 3); c226 Prop 3.1 hypotheses; c227 Cor 3.2; c228 Example 3.3 bound |f| <= |(x,y)|.")
row("M2c-cards-sample-06", "2.7-cards atomic", "cards.json M2-c229 ... M2-c238 (L15); defect at M2-c234 (line 1658-1662)", "FAIL",
    "M2-c234 is graded T, basis None, and its back combines two facts: the T result g(1/n,1/n) = 1/2 and f(1/n,1/n) = 1/(2n) (Example 3.4 and Problem E3), and the C-grade printed output of Lab 1 ('Lab 1 prints g = 0.500000 and f = 0.050000000 at n = 10, and f = 0.000050000 at n = 10000'). A C-grade lab result sits inside a T card with no basis, and the card is not atomic (BUILDER_RULES section 7: one fact per card; a lab result is named by basis). The other nine cards in the group pass (c229-c233, c235-c238 checked against Examples 3.4, Lab 1 prints, Misconceptions 1-2, Section 4).",
    "Split M2-c234 into two cards: (a) grade T, front 'What is f(1/n,1/n) along the diagonal, and what is g there?', back 'f(1/n,1/n) = 1/(2n) (Problem E3); g(1/n,1/n) = 1/2 for every n (Example 3.4)'; (b) grade C, basis 'Lab 1 (printed output)', front 'What does Lab 1 print for f at n = 10 and n = 10000?', back '0.050000000 and 0.000050000'. Give the new card a fresh id.")
row("M2c-cards-sample-07", "2.7-cards", "cards.json M2-c239 ... M2-c249 (L16)", "PASS",
    "c239 partial definition; c240 Remark 1.2; c241 Example 1.3 values 18.778112198 and 8.389056099; c242 Prop 2.1 hypotheses and conclusion; c244 and c245 Lab 1 printed values with basis; c246 coordinate example (-1); c247 xy misconception; c248 Prop 3.1; c249 Misconception 3. All numbers appear in L16.html.")
row("M2c-cards-sample-08", "2.7-cards", "cards.json M2-c251 ... M2-c260 (L17)", "PASS",
    "c251 gradient definition; c252 Example 1.2 length 2.1272790782 and angle 61.9602 (recomputed); c253 directional derivative definition; c254 Thm 2.2 hypotheses; c255 Example 2.3; c256 Thm 3.1 hypothesis w != 0; c257 Section 4; c258 R1 value 2.8775826 at corner (1,1); c259 Lab 1 62 degrees and 1e-4 agreement; c260 printed gradient and length with basis.")
row("M2c-cards-sample-09", "2.7-cards", "cards.json M2-c261 ... M2-c270 (L17-L18)", "PASS",
    "c261 Lab 1 360 directions with basis; c262-c264 Misconceptions 1-3 of L17; c265 Jacobian definition with Ah; c266 Def 3.1; c267 Prop 3.2; c268 Prop 3.3 with K; c269 Thm 4.1 hypotheses (ball, continuity at a); c270 Example 4.2 Jacobian and remainder |h|^2.")
row("M2c-cards-sample-10", "2.7-cards", "cards.json M2-c271 ... M2-c279, M2-c399 (L18, L14)", "PASS",
    "c271-c273 Lab 1 printed values with basis; c274 D_u F(a) = A u (Section 5); c275 Misconception 1 (existence of partials); c276 f of R2 (L17) not differentiable; c277 R1 sufficiency; c278-c279 Misconceptions 3 and 2; c399 Assumption 1 of L14 (derivatives of exp and sin) consistent with L14 line 36.")
row("M2c-cards-sample-11", "2.7-cards", "cards.json M2-c400, M2-c401, M2-c406, M2-c409, M2-c413", "PASS",
    "c400 Assumption 1 of L17 matches L17 line 26 and the users named there; c401 Assumption 1 of L18 (derivatives of sin and cos) matches L18 Assumption 1; c406 exp and sin of dual numbers match Def 2.1; c409 Assumption 1 of L16 (exp) and its users match L16; c413 continuity definition matches L15 Section 3.")
row("M2c-cards-duplicates", "2.7-cards duplicates", "cards.json (all 394 unit cards, script " + S + "card_dupes.py)", "PASS",
    "Full pairwise front-text scan over all 394 M2 cards: 38 pairs at difflib ratio >= 0.80. None is a duplicate within the slice. Pairs inside L13-L18 are distinct questions (c191/c192, c188/c189, c182/c183, c228/c229 differ in the object or the lesson). The five 'Which derivatives does Assumption 1 of Lesson N assume?' cards (c380, c399, c400, c401, c409) ask the same template for different lessons with different answers; not duplicates.")
row("M2c-cards-numbers", "2.7-cards / 2.2", "cards.json slice cards vs L13-L18 text", "PASS",
    "Every decimal of 4 or more digits on a slice card appears verbatim in its lesson page (script card_dupes.py: 'card decimals absent from lesson text: []' for L13-L18).")
row("M2c-cards-grades", "2.7-cards", "cards.json slice cards", "PASS",
    "All 21 C cards carry a basis; no T card carries a basis. 19 cards have no grade field: definitions and rules (c181, c184, c202, c203, c204, c220, c223, c239, c251, c253, c265, c266, c406, c413) and Assumption cards (c380, c399, c400, c401, c409); BUILDER_RULES section 7 grades only results. Grades match BLUEPRINT section 3 (T proved, C lab).")
row("M2c-cards-coverage", "2.7-cards", "cards.json slice cards vs lesson definitions, theorems, misconceptions", "PASS",
    "Each slice lesson has a card for each definition, each Theorem/Proposition/Corollary, and each of its three misconceptions: L13 (c181, c184, c182, c183, c185, c186, c187, c196-c198); L14 (c202-c203, c205, c210-c211, c216-c218); L15 (c220, c221, c222, c223, c226, c227, c230, c231, c235-c236); L16 (c239, c240, c242, c248, c247, c249, c246); L17 (c251, c253, c254, c256, c262-c264); L18 (c265, c266, c267, c268, c269, c275, c278, c279).")

# ---- structure and quiz-level checks already covered; per-lesson numbers ----
row("M2c-L18-R2-solution-numbers", "2.2-numbers", "L18.html Problem R2 solution", "PASS",
    "The solution states no number beyond J_G J_F and the bound K|h| with K the sum of absolute entries; both checked (K = sum |A_ij|, Prop 3.3).")

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"

frag = {
    "unit": "M2",
    "slice": "c",
    "round": 1,
    "verifier": "Haiku 5.5 independent verifier (fanout S1 slice c, round 1)",
    "pin": "aeb512b65b7774b59b84f836a13984fcfe9d0d1f",
    "base": "none (round 1 by assignment). Git history holds a round-11 fragment for this slice at f42f4329 (ledgers/M2/M2-c.json, PASS); no row was carried from it.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS1-M2-c",
    "scratch": "/tmp/m2c (reading and recomputation only); scripts kept under ledgers/M2/scripts/M2-c-r1/",
    "verified_at": "2026-11-09T02:40:00Z",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "BLUEPRINT section 3 asks for a registry citation key on every substantive claim. M2 L13-L18 cite no key (grade-C lab results carry none; architect Q14/Q15 record 'no registry action'). Architect decision; not a slice defect.",
        "Griewank and Walther (M2 open-items item 11, unverified candidate for the reverse-mode cost) is not in the registry and is cited nowhere on the slice; L14 Misconception 2 and Remark 9 say the general cost is not proved."
    ],
    "freshness_flags": [],
    "notes": (
        "Slice c = L13-L18 pages, the six lab twins tests/labs/M2/lab-M2-L13-1.py to L18-1.py, and their cards (105 of 394 unit cards, all read). "
        "Pages and twins are byte-identical between pin aeb512b and round-11 pin f42f432 (git diff empty for those paths); cards.json changed elsewhere in the unit. "
        "No project grader in this slice, so mutation testing is not applicable (VERIFIER_RULES ruling: lab twins are demonstrations); mutants list is empty by design. "
        "Not run: tools/verify_refs.py --unit M2 (network-only CLI; replaced by offline integrity plus plain-curl live checks of the two named keys); run_graders and mutate_graders (no grader in slice); repository-wide gates (check_pages --all, build_site --check, render_curriculum). "
        "Prior-round state: ledgers/M2/M2-c.json at f42f432 already records 11 rounds; this run was instructed as round 1 and wrote that path in this checkout (the earlier file remains in git history). "
        "Two FAIL rows: M2c-L18-R2-result-named (solution does not name the result) and M2c-cards-sample-06 (card M2-c234 not atomic, mixes a C lab printout into a T card)."
    ),
    "summary": (
        "Slice c round 1: "
        f"{len(rows)} rows, pass={sum(r['status']=='PASS' for r in rows)}, fail={sum(r['status']=='FAIL' for r in rows)}, unverifiable=0. "
        "All recomputed numbers, every lab twin and embed, all gates and page_smoke pass. Two defects: an unanswered half of Problem L18 R2 and a non-atomic card M2-c234."
    ),
}

with open("ledgers/M2/M2-c.json", "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(rows), "verdict", verdict)
