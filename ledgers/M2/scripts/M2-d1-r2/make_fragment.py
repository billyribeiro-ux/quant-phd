"""Build ledgers/M2/M2-d1.json (round 2, slice d1: L19, L20, L21 and twins) from the verifier's findings."""
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD2-M2-d1")
S = "ledgers/M2/scripts/M2-d1-r2/"

def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, id_
        r["fix"] = fix
    return r

rows = [
    # ---- round-1 non-PASS rows, re-verified from scratch in round 2 (subject changed) ----
    row("L19-example-2.2-discontinuity", "final-verification", "L19.html:88-89, 393", "PASS",
        "Re-verified in round 2 (subject changed). L19.html:89 now proves f_xy discontinuous at the origin by direct "
        "computation, with no appeal to Theorem 2.1: f_x = yM/D with M = x^4+4x^2y^2-y^4, D = (x^2+y^2)^2; on the diagonal "
        "M/D = 1 and y*d_y(M/D) = -1 at (t,t), so f_xy(t,t) = 0; on the x-axis f_xy(t,0) = 1; f_xy(0,0) = -1. "
        "Re-derived by hand (M_y, D_y, quotient rule) and numerically in " + S + "rederive.out: f_xy at (t,t) = 5.0e-5 for "
        "t = 1e-2; f_xy at (t,0) = 1.0002; f_yx(0,0) = 0.9998 and f_xy(0,0) = -0.9998 by central differences. "
        "The key-results row L19.html:393 (grade T, 'Computed in Example 2.2') needs no assumption prefix, and it has none."),
    row("L19-lab-1-prose-and-docstring", "final-verification", "L19.html:129-136; tests/labs/M2/lab-M2-L19-1.py:4-8", "PASS",
        "Re-verified in round 2. The docstring now reads 'Part A prints the closed-form gradient and Hessian ... the largest "
        "difference ... and the asymmetry', and main() prints exactly those three quantities (" + S + "twin_L19.out lines 1-4: "
        "largest error 2.26e-11, asymmetry 1.94e-11). " + S + "page_vs_twin.out: L19 code == twin and expected == stdout."),
    row("L21-E2-third-derivative", "final-verification", "L21.html:289-291", "PASS",
        "Re-verified in round 2. The solution now bootstraps: F is polynomial; F_y != 0 on I x J; if g is C^k then "
        "g' = -F_x(x,g)/F_y(x,g) is C^k, so g is C^(k+1), hence g is C^infinity and g''' exists. Central-difference "
        "truncation (1/6)h^2 g''' at h = 1e-5 is 1.67e-11 (" + S + "rederive.out: (1/6)h^2 = 1.6667e-11); eps/h = 2.2e-11; "
        "printed 3.9e-12 (twin_L21.out) is below that scale, as the solution says."),
    row("L21-numbering", "final-verification", "L21.html:63,67-69; L22.html:88,369,466,473; L23.html:379; cards M2-c309, M2-c310, M2-c315, M2-c403, M2-c326", "PASS",
        "Re-verified in round 2 (subject changed). L21 now has Assumption 1.2 (IVT, L21.html:63) and Theorem 1.3 (L21.html:67-69); "
        "no 'Assumption 1.3' or 'Theorem 1.2' remains in L21 (grep). Every cross-reference to L21 in the unit agrees: "
        "L22.html:88 and :369 'Theorem 1.3 of Lesson L21 ... Assumption 1.2 ... Assumption 2.1'; L22.html:466 and :473 'Theorem 1.3 of L21'; "
        "L23.html:379 'Assumption 1.2 of Lesson L21' and 'Theorem 2.1 of Lesson L21' (slope formula, L21.html:85); "
        "cards M2-c309 (Theorem 1.3), M2-c310 (Theorem 2.1), M2-c315 and M2-c403 (Assumption 1.2), M2-c326 (L22: Theorem 1.3 "
        "under Assumption 1.2 and Assumption 2.1). No stale reference in index.html, L24, project.html or cards.json (python scan of all card text)."),
    row("L21-key-results-row-1-source", "final-verification", "L21.html:334", "PASS",
        "Re-verified in round 2. Source cell: 'Proved in §2 from the chain rule, using Theorem 1.3 (proved in §1 under Assumption 1.2 "
        "and Assumption 2.1 of Lesson L06)'; the claim cell begins 'Assuming Assumption 1.2 and Assumption 2.1 of Lesson L06'."),
    row("L-mathbb-R", "notation", "L19.html; L20.html; L21.html; cards.json (M2)", "PASS",
        "Re-verified in round 2. grep -c mathbb: L19.html 0, L20.html 0, L21.html 0, cards.json 0. The registered macro \\R is used "
        "(L19.html:55, L20.html:207, L21.html:55). Script: " + S + "rederive.py is not needed for this; command output recorded in the round-2 notes."),

    # ---- gates run by this verifier ----
    row("G-check-pages", "gate", "tools/check_pages.py --unit M2", "PASS",
        S + "check_pages.out: 'check_pages M2: PASS', exit 0 (run this round)."),
    row("G-check-dag", "gate", "tools/check_dag.py --unit M2", "PASS",
        S + "check_dag.out: 'check_dag M2: PASS', exit 0 (run this round). No concept is defined twice; L19-L21 links resolve."),
    row("G-check-projects", "gate", "tools/check_projects.py --unit M2", "PASS",
        S + "check_projects.out: 'check_projects M2: PASS', exit 0 (run this round; M2 has no project page in this slice)."),
    row("G-run-labs", "2.5-labs", "tools/run_labs.py --unit M2", "PASS",
        S + "run_labs_M2.out: 'run_labs M2: PASS (27/27)', exit 0 (run this round). Includes lab-M2-L19-1, L20-1, L21-1."),
    row("G-twins-isolated", "2.5-labs", "tests/labs/M2/lab-M2-L19-1.py, lab-M2-L20-1.py, lab-M2-L21-1.py", "PASS",
        "Each twin run alone as `python -I -W error <twin>` (" + S + "twin_L19.out, twin_L20.out, twin_L21.out, .err files empty). Exit 0 for all three."),
    row("G-page-vs-twin", "2.5-labs", S + "page_vs_twin.py; course/modules/M/M2/L19.html, L20.html, L21.html", "PASS",
        S + "page_vs_twin.out: for L19, L20, L21 the page's data-run code equals the twin source (HTML-unescaped, stripped), and the expected block equals the twin's stdout."),
    row("G-ruff-check-format", "gate", "tests/labs/M2/lab-M2-L19-1.py, L20-1, L21-1", "PASS",
        S + "ruff_check.out 'All checks passed!'; " + S + "ruff_format.out '3 files already formatted'."),
    row("G-mypy-twins", "gate", "tests/labs/M2/lab-M2-L19-1.py, L20-1, L21-1 (mypy --no-incremental)", "PASS",
        S + "mypy_twins.out: 'Success: no issues found in 3 source files'."),
    row("G-page-smoke-L19-L21", "2.5-labs", "tools/page_smoke.py --unit M2 --pages L19 L20 L21", "PASS",
        S + "page_smoke_L19-21.out: L19, L20, L21 each PASS (zero console errors, math renders, no external requests, labs run in Pyodide in ~0.0 s, 360 px and 1280 px, both themes; figure sweep vacuous since no charts)."),
    row("G-pytest-labs-M2", "gate", "tests/test_labs.py -k M2", "PASS",
        S + "pytest_M2_labs.out: 27 selected, all passed, exit 0."),
    row("G-pytest-page-checks", "gate", "tests/test_page_checks.py", "PASS",
        S + "pytest_page_checks.out: 41 passed, exit 0."),
    row("G-verify-refs-offline", "2.1-citations", "tools/verify_refs.py --offline", "PASS",
        S + "verify_refs.out: 'offline integrity: 560 entries, 0 problems'. The live --unit run is not possible offline; no reference was added or changed in this slice, and the pages cite only spivak2008calculus and hubbard2015vector without locators."),

    # ---- numbers re-derived by the verifier ----
    row("NUM-L19", "2.2-numbers", "L19.html:55-250, 255, 268-272, 341, 392-395", "PASS",
        S + "rederive.py / rederive.out (run by verifier). Example 1.2 Hessian [[6,8],[8,4]] at (1,2) and f_x=11, f_y=7; "
        "Lab closed forms f_x = 0.474680, f_y = 1.898721, f_xx = 0.412180, f_xy = 2.148721; Prop 3.3 ratio E(s)/E(s/2) for g = s^3+s^4 "
        "gives 8.38, 8.04, 8.004 at s = 0.1, 0.01, 0.001 (-> 8); Theorem 3.1 bound: sampled worst |R|/(2|h|^2 omega) = 0.129 <= 1; "
        "E1 order estimate eps/h = 2.2e-11 and (1/6)h^2 = 1.7e-11 (L21 E2 uses the same). The prose figures 1.94e-11, 2.26e-11, "
        "3.9509/3.9750/3.9874 and 7.8836/7.9429/7.9717 agree with twin_L19.out."),
    row("NUM-L20", "2.2-numbers", "L20.html:63-71, 82-88, 98-107, 189-215, 296-310, 411", "PASS",
        S + "rederive.out: Prop 2.4 (5/3 - 1/(6n^2) in both orders) holds exactly, with Fractions, for n = 1..60 (beyond the lab's six n). "
        "Theorem 1.2 numeric: random tags, random partitions, N = 10, 100, 1000 give |S - 5/3| = 1.2e-3, 4.7e-4, 1.0e-5. Example 3.1: "
        "int_0^1 f dy = 1/(1+x^2) and int_0^1 f dx = -1/(1+y^2) (numeric to 1e-9 at x,y = 0.3, 0.7); pi/4 = 0.785398. Odd-square sum formula verified by twin."),
    row("NUM-L21", "2.2-numbers", "L21.html:97, 107, 180-184, 184, 189, 288-291, 233-247, 262-267, 283, 306-310, 367-404", "PASS",
        S + "rederive.out: Newton roots x = 0.25, 0.5, 1, 2 give y = 0.9168754789, 0.8351223485, 0.6823278038, 0.4533976515; slopes -0.3307653158, "
        "-0.3221564676, -0.2846930800, -0.1732702316 equal the central differences (diff 6.2e-13, 5.2e-14, 3.7e-12, 3.9e-12). "
        "Example 2.2 slope -0.75; misconception 2 value F_y/F_x = 4/3. M1 F_x = F_y = 3 so slope -1; M2 -1; M3 -1. "
        "Sign grid: F(x,.) has exactly one sign change for each listed x (uniqueness on the grid). F_y range 2.40 to 2.77 matches 'about 2.4 and 2.8'."),

    # ---- mathematics, proofs and grades ----
    row("MATH-L19-thm2.1", "2.4-mathematics", "L19.html:71-84", "PASS",
        "Proof re-derived line by line: Step 1 MVT in x for phi(x) = f(x,b+k) - f(x,b), then MVT in y for psi(y) = f_x(xi,y), giving Delta = hk f_xy(xi,eta) "
        "with |xi-a| <= |h|, |eta-b| <= |k|; Step 2 continuity bound with delta/2 gives distance < delta; Step 3 limit in k gives the difference quotient "
        "defining f_yx(p) within eps. Conclusion f_yx(p) = f_xy(p) follows. Grade T with 'Assuming Assumption 2.1 of Lesson L06' (L19.html:73) is correct; "
        "the MVT of L06 Theorem 2.3 rests on Assumption 2.1 (L06.html)."),
    row("MATH-L19-ex2.2", "2.4-mathematics", "L19.html:87-89", "PASS",
        "Re-derived: f_x(0,y) = -y and f_y(x,0) = x (limits of difference quotients, numerically confirmed in rederive.out); f_xy(0,0) = -1, f_yx(0,0) = 1; "
        "M and D as stated; f_xy(t,t) = 0 and f_xy(t,0) = 1 for t != 0; no limit at origin, so discontinuous."),
    row("MATH-L19-thm3.1", "2.4-mathematics", "L19.html:94-108", "PASS",
        "Proof re-derived: g(t) = f(p+th), g'' = h^T H(p+th) h, phi(t) = g(t)-g(0)-t g'(0)-t^2 g''(0)/2, phi(0) = phi'(0) = 0, phi'' = h^T (H(p+th)-H(p)) h; "
        "MVT twice gives |phi(1)| <= sup|phi''|; |h^T M h| <= (|h1|+|h2|)^2 max|M_ij| <= 2|h|^2 max|M_ij|; so |R| <= 2|h|^2 omega(|h|); omega(r)->0 by continuity. "
        "Non-blocking note: the page never defines 'twice differentiable' for f of two variables; the proof needs f differentiable on N and f_x, f_y differentiable on N, "
        "which is the usual meaning. Recorded in notes, not a row failure."),
    row("MATH-L19-rem3.2", "2.4-mathematics", "L19.html:110-113", "PASS",
        "Re-derived: g(s) = g(0)+g'(0)s+g''(0)s^2/2 + o(s^2) (|h| = |s| for unit d); coefficient (1/2)(d1^2 f_xx + d1 d2 (f_xy+f_yx) + d2^2 f_yy) matches dHd. "
        "Carries 'Assuming Assumption 2.1 of Lesson L06' (L19.html:112)."),
    row("MATH-L19-prop3.3", "2.4-mathematics", "L19.html:115-123", "PASS",
        "Proof re-derived: Lagrange remainder E(s) = g'''(theta s) s^3 / 6; continuity of g''' at 0; E(s)/E(s/2) = (1/6)/(1/48) = 8 limit. Numerically checked with g = s^3+s^4 (rederive.out). Carries the assumption (L19.html:116)."),
    row("MATH-L19-key-results-and-refs", "2.3-grades", "L19.html:391-395, 482-484", "PASS",
        "Four key results: Theorem 2.1 (T, assumption stated), Example 2.2 (T, direct computation), Theorem 3.1 (T, assumption stated), Proposition 3.3 (T, assumption stated). "
        "References paragraph (L19.html:484) names only Lesson L06 Theorem 2.3 and Lesson L08 Theorem 2.1 for the Lagrange form; both checked: "
        "L06.html Theorem 2.3 = mean value theorem, Assumption 2.1 = extreme value theorem; L08.html Theorem 2.1 = Taylor with Lagrange remainder."),
    row("MATH-L20-thm1.2", "2.4-mathematics", "L20.html:62-72", "PASS",
        "Re-derived: product split S = (sum xi Dx)(sum eta Dy) + (sum xi^2 Dx)(sum Dy); limits 1/2, 1/3, 2 and sum Dy = 2 give 5/3. Hypothesis match: x, x^2 nondecreasing on [0,1], y nondecreasing on [0,2], "
        "so L09 Corollary 2.3 (monotone f, every Riemann sum) applies, confirmed at L09.html Corollary 2.3 text. Grade T is correct."),
    row("MATH-L20-prop2.2", "2.4-mathematics", "L20.html:81-89", "PASS",
        "Both iterated integrals = 5/3: int_0^2 (xy+x^2) dy = 2x+2x^2 then int_0^1 = 5/3; int_0^1 (xy+x^2) dx = y/2+1/3 then int_0^2 = 5/3 (verified by Fraction arithmetic)."),
    row("MATH-L20-prop2.4", "2.4-mathematics", "L20.html:193-202", "PASS",
        "Facts (i) sum x_i Dx = 1/2 and (ii) sum (2i+1)^2 = n(4n^2-1)/3 with the induction step (checked: n(4n^2-1)+3(2n+1)^2 = 4n^3+12n^2+11n+3 = (n+1)(4(n+1)^2-1)); "
        "sum x_i^2 Dx = 1/3 - 1/(12n^2); y-direction midpoint exact for linear; both orders give 5/3 - 1/(6n^2). Holds exactly for n = 1..60 (rederive.out)."),
    row("MATH-L20-ex3.1-claims", "2.4-mathematics", "L20.html:210-212", "PASS",
        "d_y[y/(x^2+y^2)] = (x^2-y^2)/(x^2+y^2)^2 and d_x[-x/(x^2+y^2)] = same, so inner integrals 1/(1+x^2) and -1/(1+y^2); outer pi/4 and -pi/4 under Assumption 3.1 (numerically confirmed, rederive.out). "
        "Witness issue is a separate row (L20-example-3.1-witness-outside-domain)."),
    row("MATH-L20-problems-and-remarks", "2.4-mathematics", "L20.html:246-337, 93-94", "PASS",
        "M1 (both orders 3), M2 (2/3 both), M3 (3/2, error -1/6), P1 (odd-square induction), P2 (midpoint exact for linear), P3 (product form), E1-E3 values (-1/24, -1/96, rate n^-2), R1-R3 arguments; Remark 2.3 is ungraded and labelled unproved."),
    row("MATH-L21-thm1.3", "2.4-mathematics", "L21.html:63-81", "PASS",
        "Proof re-derived: sign flip; rectangle R with F_y > 0; strict monotonicity gives sign change at the ends; continuity of F gives a1 and I; Assumption 1.2 gives exactly one zero in J (uniqueness by monotonicity); "
        "continuity of g by squeezing with strict monotonicity; differentiability via MVT in x then y: 0 = h F_x(xi,y2) + (y2-y1) F_y(x1,eta), so (y2-y1)/h = -F_x/F_y(...) -> -F_x/F_y at (x1,y1); "
        "g' continuous. Grade T with Assumption 1.2 and 2.1 prefix (L21.html:69) is correct."),
    row("MATH-L21-thm2.1", "2.4-mathematics", "L21.html:85-93", "PASS",
        "Chain rule on F(x,g(x)) = 0 gives F_x + F_y g' = 0; division by F_y != 0 on I x J. Correct and prefixed."),
    row("MATH-L21-examples", "2.4-mathematics", "L21.html:95-103, 190-197", "PASS",
        "Example 2.2: F_y = 1.6, g' = -0.75 both ways (rederive.out). Example 3.1: at (1,0), F_y = 0, F_x = 2, dx/dy = -y/sqrt(1-y^2) = 0 at y = 0. Example 3.2: x^2 + g(x)^2 > 0 for x != 0. "
        "Section 3 example F = y^3 - x: F_y = 0 at origin and zero set is y = x^(1/3) on R (cube root identity exact)."),
    row("MATH-L21-misconceptions", "2.4-mathematics", "L21.html:208-220", "PASS",
        "Misconception 2: F_y/F_x = 1.6/1.2 = 4/3 (rederive.out) vs -0.75. Misconception 3: exchanged-role formula dx/dy = -F_y/F_x, prefixed by Assumption 1.2 and 2.1."),
    row("MATH-L21-problems", "2.4-mathematics", "L21.html:229-325", "PASS",
        "M1 (-1), M2 (-1), M3 (-1 both ways), P1 (linear case), P2 (circle branch), P3 (no function through origin), E1 (negative sign), E2 (bootstrap and error sizes; checked), "
        "R1 (dy/dP0 = 1/P'(y) < 0 under the stated hypothesis), R2 (system analogue, stated without proof and ungraded), R3 (Taylor bound via L08 Theorem 2.1) all re-derived."),
    row("LAB-L19-1", "2.5-labs", "course/modules/M/M2/L19.html:125-251; tests/labs/M2/lab-M2-L19-1.py", "PASS",
        "Hypothesis predictions checked: Hessian entries at (0.5,0.25) = 0.41218, 2.14872, 1; central-difference error 2.26e-11 <= 1e-10 target; asymmetry 1.94e-11 same order; ratio trends ~4 and ~8 (values 3.9874, 7.9717). "
        "Interpretation matches output; it says the lab tests one function and one direction, which the code does. Lab is SIMULATED-labelled. Runtime 0.0 s in Pyodide (page_smoke)."),
    row("LAB-L20-1", "2.5-labs", "course/modules/M/M2/L20.html:96-190; tests/labs/M2/lab-M2-L20-1.py", "PASS",
        "Predictions 3/2 (n=1), 13/8 (n=2) and formula 5/3 - 1/(6n^2) match exact output lines 182-188. Interpretation: 'six values of n, up to 32' and 'identity up to 50' match main() and the odd-square function. "
        "Lab is SIMULATED-labelled; no randomness; exact Fractions."),
    row("LAB-L21-1", "2.5-labs", "course/modules/M/M2/L21.html:105-185; tests/labs/M2/lab-M2-L21-1.py", "PASS",
        "Hypothesis: F_x = y, F_y = 3y^2+x (code relation_y matches), Newton from y = 1, F_y > 0 at listed x > 0. Predicted differences ~1e-11 or better: observed max 3.9e-12. "
        "Interpretation: four points, one relation, existence supplied by Theorem 1.3 under Assumption 1.2 and 2.1 — matches the text. SIMULATED label present (L21.html:107)."),
    row("GRADES-L19-L21", "2.3-grades", "course/modules/M/M2/L19.html, L20.html, L21.html (every data-grade span)", "PASS",
        "Independent re-grade against BLUEPRINT §3 of each data-grade claim in these pages: theorems and propositions T with complete proofs (or the assumption named); "
        "lab results carry grade C naming the lab (cards M2-c287..c289, c294, c301, c313, c314); Assumption blocks carry no grade; Remark 2.3 ungraded; "
        "no claim is graded above its support. No over-grading and no under-grading found."),
    row("NOTATION-L19-L21", "2.4-notation", "course/modules/M/M2/L19.html, L20.html, L21.html vs notation/notation.json", "PASS",
        "Registered symbols: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q. None appears in L19-L21 math (grep). Registered macros used: \\R only (checked against macros list). "
        "Local letters (R rectangle, N disc, U open set, H Hessian, E error, M, D, omega, eta, xi) are local, not registered. No \\mathbb, no custom macro."),
    row("DAG-L19-L21", "2.9-dag", "course/modules/M/M2/L19.html, L20.html, L21.html", "PASS",
        "check_dag.out PASS. Read by name: L19 uses partial derivative (L16), gradient (L17), derivative (L04), Taylor (L08), all earlier; L20 uses definite integral (L09), FTC (L10), limit (L01), "
        "all earlier; L21 uses derivative (L04), partial derivative (L16), Jacobian (L18), finite differences (L13), Taylor (L19), all earlier. "
        "Prose-only mean value / extreme value / intermediate value theorem are M2 earlier results or assumptions. No forward reference to a later lesson; no multiplier, Fubini, or epsilon-delta concept used."),
    row("STRUCT-L19", "2.9-structure", "course/modules/M/M2/L19.html", "PASS",
        "data-hours=10; why-it-matters 96 words (<=120); Definition/Theorem/Proof/Example/Remark/Proposition blocks; lab section with hypothesis, code, expected, interpretation; "
        "Where the canon breaks; 3 misconceptions; problem tiers Mechanics 3, Proof 3, Empirical 3, Research 3, each with details.solution; key-results table; quiz with 10 items; "
        "nav links L18 and L20; references section. Complete in the order of BUILDER_RULES 4.2."),
    row("STRUCT-L20", "2.9-structure", "course/modules/M/M2/L20.html", "PASS",
        "data-hours=10; why-it-matters 106 words; sections in order; lab; canon-breaks; 3 misconceptions; 3 tiers x 3 problems with solutions; key-results table; quiz 8 items; nav L19/L21."),
    row("STRUCT-L21", "2.9-structure", "course/modules/M/M2/L21.html", "PASS",
        "data-hours=10; why-it-matters 91 words; sections; lab; canon-breaks; 3 misconceptions; tiers 3 x 3; key-results table; quiz 9 items; nav L20/L22."),
    row("PROSE-banned-and-process", "2.9-prose", "course/modules/M/M2/L19.html, L20.html, L21.html, cards M2 slice", "PASS",
        "Scanned for TODO, TBD, lorem, for brevity, beyond the scope, details omitted, left as an exercise, you can add more, it is important to note, studies show, experts agree, "
        "it is well known, obviously, clearly, motivat, ellipsis, builder/verifier/ruling/architect words. Only hits are code '...' in the lab docstring and the word 'verify' as a learner imperative (L19 P3) and 'not verified' in math. No process words."),
    row("SCOPE-words", "2.2-numbers", "L19.html, L20.html, L21.html", "PASS",
        "'always', 'every', 'only', 'all' occur only in wrong-belief titles (L19 misconception 1, L20 misconception 1, L21 misconception 1) or in statements with a proof or a stated range ('for every x in I' after Theorem 1.3). "
        "'approaching 4 / 8' is stated as a trend over four printed step sizes, with the lab limitation stated (L19.html:250)."),
    row("XREF-L21-M2", "2.7-cross-reference", "course/modules/M/M2/L22.html, L23.html, index.html, cards.json (M2)", "PASS",
        "Every L21 reference in other pages and cards carries the renumbered label (see L21-numbering). index.html:164 links L21 (anchor fine). L22 meta links implicit-function-theorem to L21.html#def-implicit-function-theorem (anchor exists, L21.html:59)."),
    row("CARDS-coverage-L19-L21", "2.7-cards", "course/modules/M/M2/cards.json: M2-c280..c322, c402, c403", "PASS",
        "Cards per lesson: L19 13, L20 14 (including M2-c402), L21 16 (including M2-c403). Each definition (c280, c295, c308), theorem (c282, c284, c296, c309, c310), proposition (c286, c298, c300), "
        "remark (c285, c299, c312), example (c302, c311, c317, c318), lab key result (c287-c289, c301, c313, c314), misconception (c292-c294, c304-c306, c320-c322) has a card."),
    row("CARDS-dup-scan", "2.7-cards", "course/modules/M/M2/cards.json (all 393 cards)", "PASS",
        "python scan: 393 cards, no duplicate id, no duplicate front after normalisation (the one apparent duplicate 'P'(y0)' vs 'P''(y0)' is a normalisation artefact, the two fronts differ). Ids non-sequential, allowed by the architect ruling 2."),
    row("CARDS-numbers-in-lesson", "2.7-cards", "course/modules/M/M2/cards.json (L19-L21 cards)", "PASS",
        "Every number and every named item on a card appears in its lesson: e.g., 2.26e-11 and 1.94e-11 (L19.html:250), 6.2e-13 ... 3.9e-12 (L21.html:184), 5/3 - 1/(6n^2) (L20.html:194), "
        "y = 0.6823278038 and -0.2846930800 (twin_L21.out line 3), 53/32 and -1/96 (twin_L20.out). Named items Theorem 1.2, Example 3.1, Assumption 3.1, Remark 3.2 exist."),
    row("CARDS-agree-with-text-L19-L21", "2.7-cards", "course/modules/M/M2/cards.json (L19-L21 cards)", "PASS",
        "Content of each card agrees with the current lesson text (page checked): e.g., c284 Theorem 3.1 bound 2|h|^2 omega(|h|) (L19.html:99), c311 slope -0.75, c313 numbers, c318 Example 3.2, c322 exchanged roles. Only the hypothesis-prefix defects are listed as FAIL rows."),
    row("SIMULATED-labels", "2.8-data", "course/modules/M/M2/L19.html:127, L20.html:98, L21.html:107; figures", "PASS",
        "Each lab's hypothesis names its function or relation as SIMULATED, not market data. No dataset is read (no data-files attribute; no figure on these pages). No data licence question arises."),
    row("HOURS-L19-L21", "2.9-structure", "data-hours on L19, L20, L21", "PASS",
        "Each page declares data-hours=\"10\" (L19.html:2, L20.html:2, L21.html:2) and the eyebrow '10 study hours'. The hub split (240 + 60) is not in this slice and was not checked here."),

    # ---- FAIL rows (new) ----
    row("L19-theorem-2.1-hypothesis-count", "2.9-prose", "L19.html:255", "FAIL",
        "'The statement of Theorem 2.1 has two hypotheses: ...' but the statement (L19.html:73) carries three: 'Assuming Assumption 2.1 of Lesson L06' plus the two listed. The count leaves out the assumed Assumption 2.1.",
        "Change to: 'The statement of Theorem 2.1 has two hypotheses on f, besides the assumed Assumption 2.1 of Lesson L06 that it carries: ...'."),
    row("L19-solutions-omit-assumption-2.1", "2.4-mathematics", "L19.html:305 (M3), 323 (P2), 348 (E2), 355 (E3), 380 (R3), 435 (quiz Q4 explanation), 449 (quiz Q6 explanation)", "FAIL",
        "Worked solutions and quiz explanations apply Remark 3.2 (L19.html:112), Theorem 3.1 (L19.html:97) or Proposition 3.3 (L19.html:116), each conditional on Assumption 2.1 of Lesson L06, without the 'Assuming Assumption 2.1' prefix. "
        "The lesson's own references paragraph (L19.html:484) says each graded statement that uses Assumption 2.1 begins with that phrase, and the L21 solutions carry it consistently. The results themselves are correct (rederive.out).",
        "Prefix each named solution or explanation with 'Assuming Assumption 2.1 of Lesson L06,' (or write the hypothesis in its first sentence)."),
    row("L19-quiz-Q9-circular-answer", "2.9-prose", "L19.html:466-472 (item L19q9)", "FAIL",
        "Question 'Why does the second-order expansion need the cross term f_xy?' has the marked-correct option 'Because of the cross term f_xy h1 h2', which restates the term rather than giving a reason. The explanation (line 472) gives only the formula, so a learner cannot tell the right answer from its wording.",
        "Replace the correct option with 'Because the quadratic form (1/2) h^T H h contains f_xy h1 h2, which is non-zero when f_xy(p) != 0' and keep the two distractors; say in the explanation that the term vanishes only when f_xy(p) = 0."),
    row("L20-example-3.1-witness-outside-domain", "2.4-mathematics", "L20.html:212 (and card M2-c307)", "FAIL",
        "'The integrand is unbounded near the origin: f(t,0) = 1/t^2 for t in (0,1].' The points (t,0) are outside the domain (0,1]^2 of Example 3.1 (L20.html:210), so the stated witness does not show unboundedness on the domain. "
        "The claim is true (for fixed t, f(t,y) -> 1/t^2 as y decreases to 0, numerically confirmed by the formula), but the page does not say so.",
        "Replace the sentence with: 'For fixed t in (0,1], f(t,y) tends to 1/t^2 as y decreases to 0, so f is unbounded on (0,1]^2.'"),
    row("CARD-M2-c307-witness", "2.7-cards", "course/modules/M/M2/cards.json, M2-c307", "FAIL",
        "Back: 'For t in (0, 1], f(t, 0) = 1/t^2, which is unbounded as t tends to 0, so the corner at the origin is not in the domain and the integrand has no bound there.' It uses the off-domain point (t,0), and the final clause does not follow from the stated premises.",
        "Rewrite the back as: 'For fixed t in (0, 1], f(t, y) tends to 1/t^2 as y decreases to 0, so f is unbounded on (0, 1]^2 (Section 3).'"),
    row("L21-E3-solution-incomplete", "2.4-mathematics", "L21.html:297 (E3 solution)", "FAIL",
        "Asked why small residuals do not show that the computed root is the one Theorem 1.3 provides, the solution says only that the output 'does not show that the root is unique' and the lab 'does not check uniqueness'. "
        "It omits the property the root must have (lying in J, the interval of Theorem 1.3, where g(x) is the unique zero) and omits the argument that makes uniqueness hold here: F_y = 3y^2 + x > 0 for x > 0, so F(x,.) is strictly increasing on R and has exactly one zero (rederive.out: one sign change per x on a grid). The solution is not a full worked solution.",
        "Rewrite: a residual shows only that (x,y) is near the zero set; Theorem 1.3's g(x) is the unique zero in J, so the Newton root equals g(x) only if it lies in J, which a residual cannot show; for x > 0, F_y > 0 on R gives exactly one real zero, so the root is g(x) once it lies in J."),
    row("CARDS-L19-hypotheses", "2.7-cards", "course/modules/M/M2/cards.json: M2-c285, M2-c291, M2-c292", "FAIL",
        "Three grade-T cards state results that carry 'Assuming Assumption 2.1 of Lesson 6' on the page and omit it: c285 (Remark 3.2 coefficient, L19.html:112), c291 (Theorem 3.1, L19.html:97), c292 (symmetry of the mixed partials, Theorem 2.1, L19.html:73). The sibling cards c282, c284 and c286 carry it. Rule: cards carry a proposition's hypotheses.",
        "Prefix the back of each of M2-c285, M2-c291, M2-c292 with 'Assuming Assumption 2.1 of Lesson 6,'."),
    row("CARDS-L21-hypotheses", "2.7-cards", "course/modules/M/M2/cards.json: M2-c312, M2-c319, M2-c321, M2-c322", "FAIL",
        "c319 asserts that F_y != 0 is sufficient (Theorem 1.3, L21.html:69, which assumes Assumption 1.2 and 2.1); c321 states the chain-rule slope (Theorem 2.1, L21.html:87); c322 states dx/dy = -F_y/F_x (Misconception 3, L21.html:218, which carries the assumption); "
        "c312 (ungraded) summarises Remark 2.3 (L21.html:102, which begins with the assumption). None of the four cards carries the assumption.",
        "Prefix the back of each of M2-c312, M2-c319, M2-c321, M2-c322 with 'Assuming Assumption 1.2 and Assumption 2.1 of Lesson 6,'."),
]

notes = [
    "Round 2, slice d1 (L19, L20, L21 and their twins). Delta from the round-1 pin 9f5d9865 to c737272 read in full: course/modules/M/M2/L19.html (4 hunks), L20.html (1 hunk), L21.html (64-line change, whole file read), tests/labs/M2/lab-M2-L19-1.py (1 hunk, docstring). Each page and twin was read in full, line by line, not only the hunks; cards for L19-L21 read as a set (M2-c280..c322, c402, c403).",
    "Round-1 non-PASS rows (6) were re-verified from scratch because their subjects changed; all six now pass with evidence cited above. Their ids are kept.",
    "No project grader or mutant exists in this slice (no grader in L19-L21); the mutation rule (VERIFIER_RULES 2.6, ruling 9) does not apply, so mutants is empty. Student-error mutants were not written for lab twins, which are demonstrations (ruling).",
    "Observed, not a row failure: L19 Theorem 3.1 uses 'twice differentiable' for a function of two variables without defining it. The proof needs f differentiable and f_x, f_y differentiable on N, the usual meaning. Optional clarity fix: add one sentence to Definition 1.1.",
    "Out of slice, for the orchestrator: (a) ledgers/M2/M2-d.json (round 14, pin d2b4a87, PASS rows) still carries rows that cite the pre-renumbering text, e.g. 'L21-Assumption1.3-name' (cites Assumption 1.3 at L21.html:63-64) and 'L21-R3-EVT-ref' (cites Theorem 1.2 and Assumption 1.3); 'L21-E2-numbers' describes the pre-fix E2 solution. These rows are stale against c737272 and need re-verification by the slice-d owner before the unit ledger is merged. (b) course/modules/M/M2/index.html:164 card body reads 'When an equation defines one variable as a differentiable function of another, and the implicit derivative.' (incomplete sentence, hub, Builder A). (c) The stale M2-d.json row 'COVERAGE-full-prose-reread' is FAIL and is not this slice's.",
    "Not checked: the dark-theme and visual rendering beyond page_smoke's checks (no figure on these pages); the Spivak and Hubbard passages (no locators are cited on these pages, so no passage was attributed; no network access was used beyond the offline registry check); the hub hour split and L22-L24 content (outside slice d1, only their L21 cross-references were checked); the full-unit page_smoke (run for L19-L21 only, as instructed).",
    "Not run by design: run_graders and mutate_graders (no grader in slice); full gate for M2 beyond the targeted commands above.",
]

frag = {
    "unit": "M2",
    "slice": "d1",
    "round": 2,
    "verifier": "Haiku 5.5 independent verifier, slice d1 (L19-L21 and twins), round 2",
    "pin": "c737272f5bdef4a027417989cd52254555e8a0bb",
    "base": "9f5d9865",
    "checkout": str(ROOT),
    "scratch": str(ROOT / "ledgers/M2/scripts/M2-d1-r2"),
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": "",
}
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag["summary"] = (f"M2-d1 round 2: {len(rows)} rows (pass={counts['PASS']} fail={counts['FAIL']} unverifiable={counts['UNVERIFIABLE']}). "
                   "All gates PASS (check_pages, check_dag, check_projects, run_labs 27/27, twins isolated, page-vs-twin, ruff, mypy, page_smoke L19-L21, pytest). "
                   "Round-1 rows re-verified and PASS. FAIL rows are hypothesis-carrying defects in solutions and cards, one incomplete solution, one circular quiz answer, and two prose witness and count defects.")
out = ROOT / "ledgers/M2/M2-d1.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts, frag["verdict"])
