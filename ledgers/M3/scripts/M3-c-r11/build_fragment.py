"""Round-11 M3 slice c fragment builder (writes ledgers/M3/M3-c.json from the rows recorded by the verifier)."""
import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD11-M3-c")
S = "ledgers/M3/scripts/M3-c-r11"
G = f"{S}/out/gates.out"
LC = f"{S}/out/lab_check.out"
RC = f"{S}/out/recompute.out"
CS = f"{S}/out/cards_scan.out"
PS = f"{S}/out/page_smoke.out"
PT = f"{S}/pytest_c.out"

R = []


def row(rid, check, location, evidence, status="PASS", fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or ""
    R.append(r)


# ---- gates (run fresh at pin ccaeeaf4; outputs in S/out) ----
row("GATE-01", "2.9-gate", "tools/check_pages.py --unit M3; --unit M3 --page L07, L08, L09",
    f"{G}: 'check_pages M3: PASS' rc=0; per page 'check_pages M3 L07/L08/L09: PASS' rc=0.")
row("GATE-02", "2.9-gate", "tools/check_dag.py --unit M3", f"{G}: 'check_dag M3: PASS' rc=0.")
row("GATE-03", "2.6-gate", "tools/check_projects.py --unit M3", f"{G}: 'check_projects M3: PASS' rc=0 (project slice is outside c).")
row("GATE-04", "2.5-labs", "tools/run_labs.py --unit M3 (and --page L07, L08, L09)",
    f"{G}: 'run_labs M3: PASS (12/12)' rc=0; --page L07 (1/1), L08 (1/1), L09 (1/1) each rc=0.")
row("GATE-05", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py run alone",
    f"{LC}: each twin run as `python -I -W error <twin>` gives rc=0, empty stderr, and stdout equal to the page's expected block (three 'expected block == twin output: True').")
row("GATE-06", "2.5-labs", "ruff check tests/labs/M3 course/modules/M/M3/grader; ruff format --check tests/labs/M3",
    f"{G}: 'All checks passed!' rc=0; '12 files already formatted' rc=0.")
row("GATE-07", "2.4-gate", ".venv/bin/mypy --no-incremental", f"{G}: 'Success: no issues found in 385 source files' rc=0.")
row("GATE-08", "2.9-gate", "tools/page_smoke.py --unit M3 --pages L07, then L08, then L09 (each alone)",
    f"{PS}: 'page_smoke modules/M/M3/L0x.html: PASS' and 'page_smoke M3: PASS' rc=0 for L07, L08 and L09 (Pyodide lab boot and numpy preload logged).")
row("GATE-09", "2.1-citations", "tools/verify_refs.py --offline (whole registry, unit has no data-cite)",
    f"{G}: 'offline integrity: 560 entries, 0 problems' rc=0. The live Crossref run was not performed (offline ruling).")
row("GATE-10", "2.5-labs", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k M3",
    f"{PT}: '12 passed, 394 deselected' exit=0 (tests/test_labs.py lab-M3-L07-1, L08-1, L09-1 among the 12 PASSED lines).")
row("GATE-11", "2.9-gate", "tools/build_site.py --check", f"{G}: 'site data current: 6 outputs' rc=0.")
row("GATE-12", "2.9-gate", "tools/render_curriculum.py then git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json",
    f"{G}: 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h' rc=0; diff rc=0 (regenerated files identical to the pin).")
row("GATE-13", "2.8-data", "tools/fetch_data.py --check", f"{G}: 'fetch_data: 3 datasets, 0 problems' rc=0.")

# ---- lab twins, page code, expected blocks (fresh) ----
row("LAB-L07-EMBED", "2.5-labs", "course/modules/M/M3/L07.html section#lab-M3-L07-1 vs tests/labs/M3/lab-M3-L07-1.py",
    f"{LC}: 'L07: page code == twin: True' (after rstrip; the only difference is the trailing newline). Re-derived with ledgers/M3/scripts/M3-c-r11/lab_check.py.")
row("LAB-L08-EMBED", "2.5-labs", "course/modules/M/M3/L08.html section#lab-M3-L08-1 vs tests/labs/M3/lab-M3-L08-1.py",
    f"{LC}: 'L08: page code == twin: True'.")
row("LAB-L09-EMBED", "2.5-labs", "course/modules/M/M3/L09.html section#lab-M3-L09-1 vs tests/labs/M3/lab-M3-L09-1.py",
    f"{LC}: 'L09: page code == twin: True'.")
row("LABSTMT-L07", "2.5-labs", "L07.html line 125 (hypothesis); code 126-192; expected 193-203; interpretation 204; twin docstring 131-139",
    "Every claim in the hypothesis (P symmetric and idempotent, Py = A beta, residual orthogonal to columns, Pythagorean identity, agreement with lstsq, all to 1e-9; coefficients and residual norm to 4 dp; A^T y to 2 dp; duplicated column gives rank 2 and two coefficient vectors with equal fit) is printed by code lines 164-189, and the output in lines 193-203 (checked against lab_check.out) matches. Interpretation (line 204): 'Every check prints True' holds; SIMULATED coefficients 1.5/0.8/-0.4 match lines 152-155.")
row("LABSTMT-L08", "2.5-labs", "L08.html line 146 (hypothesis); code 147-269; expected 270-283; interpretation 284; twin docstring 147-160",
    "Hypothesis: 750 days, six tenors (line 167-168), scales 8/4/2 and noise 0.5 (lines 190-199), PSD/MV=V Lambda/score identity/trace checks (lines 221-229), shares from unrounded eigenvalues printed to 0.1 (231-235), best-matching components and distinct matches (238-246), doubling (248-253), column-0 rescaling by 10 (254-259), E1 bound inputs (260-266). All match code and expected lines 270-283 (lab_check.out). Interpretation numbers 75.9/18.1/5.2, 0.9994/0.9985/0.9990, 0.7587->0.9791, 0.9483, 13.6818, 88.2028 match the printed block.")
row("LABSTMT-L09", "2.5-labs", "L09.html line 190 (hypothesis); code 191-332; expected 333-345; interpretation 346; twin docstring 191-211",
    "Claims 1-4 in the docstring match code lines 283-329: x^T C0 x = -2.4 (285-288), ||C0-B||_F^2 equals the sum of squared negative eigenvalues (290-295), R correlation matrix (297-301), 40 seeded 5x5 matrices, 23 non-PSD, is_correlation counts and strictly-closer counts (303-329). Expected block 333-345 equals the output (lab_check.out).")
row("LABSTMT-RUNTIME", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py (imports, seeds, network)",
    "Imports are numpy and the standard library only; seeds are fixed at 7, 8 and 20261028 (lines 150, 213, 226); no network calls. Each twin exits 0 under python -I -W error (lab_check.out). page_smoke ran each lab in Pyodide and passed (page_smoke.out). Twins end with a bare main() call (lines 192, 269, 332).")
row("LABDOC-L09", "2.2-lab-prose", "tests/labs/M3/lab-M3-L09-1.py docstring lines 191-211 vs code 213-332 (page lines 191-211)",
    "Docstring claim 1 (C0 entries, witness -2.4) = code 283-288. Claim 2 (||C0-B||^2 = sum of squared negative eigenvalues) = code 290-295. Claim 3 (R symmetric, unit diagonal, PSD) = code 297-298. Claim 4: seed 20261028 (line 226), off-diagonal 0.5 plus symmetrised N(0,0.35) noise (274-277), size 5 (225), MAX_ITER 500 and TOL 1e-12 (220, 223). Scope statement matches lines 303-329.")
row("LABDOC-L09-TOL", "2.2-lab-prose", "L09.html lines 190 and 346 vs twin constants TOL, FEASIBLE_TOL, NONPSD_TOL (twin lines 220-222)",
    "TOL = 1e-12, FEASIBLE_TOL = 1e-8, NONPSD_TOL = 1e-9. Page text 'symmetric and unit diagonal to 1e-12, smallest eigenvalue at least -1e-8' (line 190) and 'smallest eigenvalue below -1e-9' (expected block line 342) agree with those constants.")

# ---- numbers (independent recomputation: recompute.py, alternative routes) ----
row("NUM-L07", "2.2-numbers", "L07.html lines 199-203 (expected), 222 (residual 0.8951), 302 (A^T y), 307-309 (intercept 1.3325)",
    f"{RC}: QR-route coefficients 1.3325188 0.8488115 -0.4119637 -> '1.3325 0.8488 -0.4120'; residual norm 0.89512755 -> 0.8951; A^T y 18.3797 3.0959 -17.6035 -> '18.38 3.10 -17.60'; M2 solved to beta0 = 7/6, beta1 = 1/2 and residuals -1/6, 1/3, -1/6 (sum 0, inner product with x 0). Q1 numeric 1.1667 within 0.0005 of 7/6.")
row("NUM-L07-M", "2.2-numbers", "L07.html line 350 (rank 2 of 3) and the duplicated-column check (lab lines 183-189)",
    f"{RC}: singular values of the duplicated design (A with column 2 repeated) are 3.594, 2.995, 7e-17; rank 2 of 3 confirmed by a second route (SVD, not matrix_rank).")
row("NUM-L08", "2.2-numbers", "L08.html lines 275, 282-284 (shares 75.9/18.1/5.2; rescaling 0.7587 -> 0.9791; bound 0.9483; inputs 13.6818, 88.2028), 304 (cos 0.9985), 433",
    f"{RC}: shares via SVD route 75.8728, 18.0888, 5.1619 -> 75.9, 18.1, 5.2; |cos| 0.999381, 0.998544, 0.999019 -> 0.9994, 0.9985, 0.9990; first share 0.75873 -> 0.7587 before and 0.97914 -> 0.9791 after rescaling; bound 100 M11/(trace+99 M11) = 0.948346 with M11 13.681775 and trace 88.202753; the bound lies between 0.7587 and 0.9791 and exceeds the old share.")
row("NUM-L09", "2.2-numbers", "L09.html lines 52, 336, 345-347, 444 (sqrt 0.96), 452, 494-497",
    f"{RC}: C0 eigenvalues -0.8, 1.9, 1.9 (characteristic polynomial and Jacobi rotations agree); ||C0-B||_F^2 = 0.64; R off-diagonal 0.5, 0.5, -0.5; ||C0-R||_F = 0.97979590 -> 0.9798; Example 3.6 squared distances 0.04 and 0.08; first non-PSD index 0 distances 0.17552673 and 0.16328044 -> 0.175527 and 0.163280; 23 of 40 non-PSD; 23 of 23 correlation checks and 23 of 23 strictly closer, recomputed with an independent generator and repair code.")
row("ALT-L09", "2.5-labs (robustness)", "tests/labs/M3/lab-M3-L09-1.py repair procedures vs alternative correct procedures",
    f"{RC}: clipping by a hand-written Jacobi eigen-solver (not numpy eigh) gives the same B (||C0-B||^2 = 0.64) and R (0.5, 0.5, -0.5); the seeded counts 23/23 and 23/23 and the index-0 distances are reproduced by a separate implementation of the generator and of alternating projections.")
row("ALT-L08", "2.5-labs (robustness)", "L08.html Lab 1 eigh-based PCA vs an SVD route",
    f"{RC}: eigenvalues from SVD of the centred panel, s^2/(T-1), equal the eigh eigenvalues to 1e-9; shares, cosines and rescaled share 0.9791 reproduced.")

# ---- math ----
row("MATH-L07", "2.4-math", "L07.html Definition 1.1 (60), Theorem 1.2 (64-71) and proof (75-81), Theorem 1.3 (84-86) and proof (90), Remark 1.4 (94-95), Theorem 2.2 (108-115) and proof (119-120)",
    "Hypotheses are stated (real, independent columns, F1-F4 defined at L04 lines 56-62). Re-derived: G symmetric and x^T G x = ||Ax||^2 > 0 gives invertibility (a); beta = G^{-1}A^T y and A^T(y - p) = 0 (b); P^T = P and P^2 = P (c); cross term vanishes so ||y-w||^2 = ||y-p||^2 + ||p-w||^2 (Thm 1.3); w = 0 gives Remark 1.4; Theorem 2.2 normal equations and uniqueness. The Fact 1.2 of Lesson 6 cited in (a) is VV^T = I for orthogonal V (L06 line 64-70). No gaps found.")
row("MATH-L08", "2.4-math", "L08.html Proposition 1.1 (61-62), Proposition 1.2 (71-72), Definition 1.3 (82), Theorem 1.4 (86-87) and proof (92), Theorem 2.1 (100-105) and proof (110-112), Corollary 2.2 (117), Proposition 2.3 (121-122) and proof (127), Remark 2.4 (131-132), Section 3 (137), Definition 3.1 (141)",
    "Re-derived each step: x^T M x = ||X~x||^2/(T-1) (1.1); tr M = sum ||x~_t||^2/(T-1) (1.2); Z^T Z = (T-1)Lambda (1.4); quadratic-form maximum over unit vectors with ordered lambdas and the k-th direction under orthogonality (2.1 a and b, using alpha_i = v_i^T u); Corollary 2.2; scaling by c^2 (2.3), eigenvalues ordered since c^2 > 0; Remark 2.4 argument (M_jj > 0 from the x = e_j + t e_l calculation; kappa = c forced by the off-diagonal entry, then c^2 = c contradicts c not in {0,1}); cosine and orthogonalization (Section 3); curvature shape nonzero by the at-most-two-roots argument. Hypotheses listed. No gaps found.")
row("MATH-L09", "2.4-math", "L09.html Definition 1.1 (59-60), Definition 1.2 (64-65), Lemma 1.3 (71) and proof (77-81), Definition 2.1 (90), Example 2.3 (101-104), Definition 3.1 (114), Proposition 3.2 (120-121) and proof (127-131), Proposition 3.3 (136-137) and proof (143-144), Proposition 3.4 (149) and proof (154-156), Proposition 3.5 (161) and proof (166-170), Example 3.6 (175-177), Method 2 (184), Remark 2.2 (95)",
    "Re-derived: ||QMQ^T||_F = ||M||_F via tr(XY) = tr(YX) (Lemma 1.3); Example 2.3 witness -2.4 (3 - 5.4); Prop 3.2(a) PSD via sum max(lambda_i, eps) y_i^2; (b) eps ||x||^2 bound; Prop 3.3(a) sum of (eps - lambda_i)^2 over lambda_i < eps; Prop 3.4 congruence with D^{-1/2}; Prop 3.5 bracket: delta b_jj = |b_ij| b_jj/(1+b_jj) < |b_ij| so x^T B x < 0; Example 3.6 eigenpairs (2.2, 1,1 vector), A_0 = 1.1 matrix, R = all ones, distances 0.04 and 0.08. Method 2 claims (500 steps, 1e-12, unit diagonal by construction, PSD not guaranteed) match code lines 248-258. No gaps found.")
row("PROP23-HYP", "2.4-math", "L08.html Proposition 2.3 statement (122), proof (127), E2 solution (384), key-results row (432)",
    "Hypotheses: c nonzero real and sum of eigenvalues > 0 (the shares are defined). Every use (E2, key row 432, misconception 2 at line 308 with c = 2) states the same condition.")
row("KEY-L08-430", "2.9-key-results", "L08.html key-results row 430 vs Theorem 1.4 (line 87)",
    "Row 430 states Z^T Z/(T-1) = Lambda and shares sum to 1 whenever the eigenvalue sum is positive; Theorem 1.4 (line 87) has the same hypotheses (F1 to F4) and conclusions.")

# ---- problem sets ----
row("PROB-L07", "2.4-math", "L07.html problems M1-M3 (241-261), P1-P3 (266-286), E1-E3 (291-311), R1-R3 (316-336), each with <details class=solution>",
    "Twelve problems, three per tier, each with a full solution (12 details blocks counted). Arithmetic re-derived: M1 (P = 1/2 [[1,1],[1,1]], p = (1,1)); M2 (beta = (7/6, 1/2), fitted 7/6, 5/3, 13/6); M3 (P = diag(1,0), 25 = 9 + 16); P1, P2, P3 proofs correct; R1 existence via a maximal independent list of length at most n (Theorem 3.7 of Lesson 1, L01 line of Theorem 3.7); R2 linearity; R3 complement projection.")
row("PROB-L08", "2.4-math", "L08.html problems M1-M3 (323-343), P1-P3 (348-368), E1-E3 (373-393), R1-R3 (398-418)",
    "Twelve problems with solutions. Re-derived: M1 centred rows (-2,-3), (0,-1), (2,4), M = [[4,7],[7,13]], trace 17, det 3, eigenvalues (17 +- sqrt 277)/2; M2 shares 2/3, 1/6, 1/6; M3 9M eigenvalues 18, 9; P3 lambda_1 >= M_11; E1 bound 100 M11/(S0 + 99 M11) = 0.9483; E3 sum 99.2 with 0.15 bound (unrounded sum 99.124 from recompute.out); R1 eigenspace; R2 column shift; R3 B G B^T identity.")
row("PROB-L09", "2.4-math", "L09.html problems M1-M3 (384-402), P1-P3 (409-428), E1-E3 (433-453), R1-R3 (458-478)",
    "Twelve problems with solutions. Re-derived: M1 eigenvalues 1.6, 0.4 (PSD); M2 ||A||_F^2 = 4.88 = 2.2^2 + 0.2^2; M3 roots (13 +- sqrt 41)/2 and c_12 = 1/3; P1 |C_ij| <= 1 via the two choices of t; P2 invertibility from the bound; P3 convexity; E1 -2.4; E2 sqrt(0.96) = 0.9798; E3 distance 0.5 from Proposition 3.3(a); R1 split of the norm; R2 diag(1,4) to identity; R3 norm of a correlation matrix >= n.")

# ---- grades, citations, cross references ----
row("GRADE-L07", "2.3-grades", "L07.html block titles (64 T, 84 T, 108 T); Remark 1.4 (94-95) via key-results rows 346-348 (T); row 350 (C)",
    "Theorem blocks carry data-grade T on the title; the lab-derived row 350 is C and names Lab 1. Re-graded independently: all T results are proved; the numerical lab identities are C. No over-grading.")
row("GRADE-L08", "2.3-grades", "L08.html block titles (61 T, 71 T, 86 T, 100 T, 116 T, 121 T) and key-results table (428-434)",
    "Titles T for Propositions 1.1, 1.2, Theorem 1.4, Theorem 2.1, Corollary 2.2, Proposition 2.3 (all proved on the page). Rows 433 and 434 (lab output on one simulated panel) are C with basis naming Lab 1. Remark 2.4's claim that shares can change is supported by row 434 (C).")
row("GRADE-L09", "2.3-grades", "L09.html block titles (59, 63, 70, 89, 111, 118, 135, 147, 159, 174) and key-results rows 488-497",
    "Lemma 1.3 and Propositions 3.2 to 3.5 are T and proved; Example 2.3 and 3.6 checks are T (computed on the page); rows 496-497 (23 of 23 and index-0 distances) are C with basis naming Lab 1.")
row("CITE-L07-L09", "2.1-citations", "L07.html, L08.html, L09.html (grep: no data-cite, no data-locator; <ol data-references> empty at lines 431, 519, 592)",
    "The pages attribute nothing to an outside source; their references sections say so (L07 430, L08 518, L09 591). No registry key is cited, so none can be unregistered. verify_refs --offline passes (GATE-09).")
row("XREF-EARLIER", "2.9-xref", "earlier-lesson cross-references in L07, L08, L09",
    "Checked each target: L04 F1-F4 (L04.html lines 56-62), L04 Definition 1.1 (transpose and symmetry), L04 Theorem 2.3 (spectral theorem; L04 line 130), L04 Definition 1.2 (inner product, norm, orthogonality); L05 Definition 1.4 (PSD and PD, used as 'positive definite'), L05 Theorem 2.1 (eigenvalue test for PSD); L06 Definition 1.1 (orthogonal matrix), Fact 1.2 (QQ^T = I), Proposition 2.4 (Frobenius norm and trace), L06 line 56 (inner product and norm), L06 Remark 2.5 (sign freedom in an SVD); L03 Definition 1.1; L01 Theorem 3.7 (no longer independent list), L01 Proposition 1.4 (subspace test); L07 Theorem 1.2 (cited from L08 line 137, exists at L07 line 64). All resolve to the cited items.")
row("DAG-PSD-REDEF", "2.9-dag", "course/modules/M/M3/L09.html line 122 (new pointer to Lesson 5, Definition 1.4) and line 56 (link only) versus L05.html line 72 (the only dfn)",
    "The dfn id def-positive-semidefinite-matrix exists only in L05.html (line 72). L09 only links it; the new text at line 122 is a pointer to L05 Definition 1.4, not a redefinition.")
row("NOTATION-R", "2.9-notation", "L07, L08, L09 math using \\R", "\\R is registered in notation/notation.json macros (meaning real numbers) and is used only with that meaning (19 uses in the three pages).")
row("NOTATION-OPNAME", "2.9-notation", "registered \\tr and \\diag: L08 lines 56-72, 137; L07 lines 56, 332; L09 lines 56-65",
    "\\tr and \\diag are registered macros in notation.json and are used with their registered meaning. Greek letters used locally (alpha, beta, gamma, tau, kappa, delta, iota) are not registered program-wide symbols (notation.json 'about' says such letters are defined where used); the registered gamma symbols are \\gamma_3 and \\gamma_4 (skewness and kurtosis), which these pages do not use.")
row("NOTATION-T", "2.9-notation", "L08.html Section 1 (line 56: T x n matrix, T >= 2 observations) and Lab 1 (T_DAYS = 750)",
    "Registered T means the number of return observations (periods) in a sample (notation.json symbols[0]). Here T is the number of observations (daily yield-change rows), the same role; no other meaning is given to T on the pages.")
row("NOTATION-AST", "2.9-notation", "L09.html lines 90 and 93 (C^{\\ast}: nearest correlation matrix)",
    "C^{\\ast} is a different symbol from the registered R^\\ast and R^{e\\ast} (AP1) and is defined on the line where it is used (Definition 2.1).")
row("NOTATION-Q", "2.9-notation", "L07, L09 orthogonal Q (L09 lines 72-81); \\mathbb{Q} registered for a probability measure",
    "Plain Q is used for the orthogonal matrix in L09 Lemma 1.3; \\mathbb{Q} (registered) occurs 0 times in the three pages (grep). No collision.")
row("NOTATION-OTHER", "2.9-notation", "all control sequences in math on L07, L08, L09 (tally of \\(...\\) and \\[...\\] spans)",
    "Tally: \\top, \\lambda, \\varepsilon, \\beta, \\sum, \\lVert, \\rVert, \\tilde, \\Lambda, \\ge, \\in, \\hat, \\times, \\sqrt, \\alpha, \\cdot, \\R, \\diag, \\ldots, \\max, \\gamma, \\ne, \\tr, \\tau, \\frac, \\lt, \\bar, \\boldsymbol, \\iota, \\le, \\Gamma, \\delta, \\gt, \\pm, \\perp, \\kappa, \\cos, \\bigl, \\bigr, \\min, \\approx, \\mapsto, \\cdots, \\overline, \\ast, \\dfrac, \\operatorname, \\mathrm, \\tfrac. Custom macros are only \\R, \\diag, \\tr (registered); the rest are standard KaTeX/LaTeX commands.")
row("DEF-L08-CLOSE", "2.9-structure", "L08.html Section 3 (137), Definition 3.1 (141), quiz item L08q9 (505-511)",
    "Definition 3.1 closes the match rule (exactly one maximiser, otherwise no label); quiz item L08q9 (level-like) states the same rule and its explanation (511) matches Definition 3.1.")
row("DEF-L08-MATCH", "2.2-lab-prose", "L08.html Definition 3.1 (141), canon-break (292), quiz explanation (511), lab matches (238-246, 277-280)",
    "The tie rule is stated identically in the definition (141), canon-break (292: 'no match when two principal directions tie') and quiz explanation (511). The lab prints one argmax per shape and 'match three different components: True' (line 280); no tie occurs on this run, and the page does not claim one does.")
row("DAG-LINKS", "2.9-dag", "L07.html, L08.html, L09.html meta rows (lines 38-39)",
    "Every linked concept is defined earlier or on the same page: vector-space (L01 line 57), eigendecomposition (L03 line 109), spectral-theorem (L04 line 130), positive-semidefinite-matrix (L05 line 72), and the same-page dfn ids of L07, L08, L09. check_dag --unit M3 passes (GATE-02).")
row("DAG-M4", "2.9-dag", "L07-L09 covariance, variance, correlation, expectation wording; curriculum.json concepts: correlation and covariance-matrix owned by M4",
    "No data-concept link or dfn for an M4 concept appears on the three pages (grep of data-concept: only M3, L01, L03, L04, L05 ids). 'Covariance' occurs only as the formula X~^T X~/(T-1) (L08 line 57), with no concept name. 'Correlation matrix' is the plain term defined in L09 Definition 1.1 (line 59-60); this is the planner's option (a) for B1 (plan section 9, section 10 Q2, 'the word correlation only as a plain descriptor, with no concept link'), which the architect's binding ruling covers for covariance. PASS on the architect's ruling; flagged to the architect because the ruling names covariance but not the word correlation.")
row("DAG-PROSE-UNLINKED", "2.9-dag", "L09.html line 60 (positive semidefinite in Definition 1.1) and other plain PSD mentions",
    "Plain 'positive semidefinite' appears after Lesson 5 defines it (L05 line 72), inside the unit's own closure, so no DAG defect. No M4/M7/M8/AP2/PR1 concept is named on the pages (grep: cholesky, IEEE, minimum-variance, mean-variance, shrinkage, OLS absent; 'floating point' at L09 line 497 is a plain tolerance remark, consistent with B4).")
row("CONCEPT-L08-LSC", "2.9-dag/2.3-grades", "course/modules/M/M3/L08.html line 39 (Introduces link text), line 141 (dfn id=def-level-slope-curvature)",
    "Single definition; curriculum.json concept level-slope-curvature has module M3. The principal-component-analysis dfn (L08 line 82) and the L07 and L09 dfns (L07 lines 60, 104; L09 lines 90, 113) are each defined once; curriculum owners: orthogonal-projection, least-squares-projection, principal-component-analysis, level-slope-curvature, nearest-correlation-matrix, eigenvalue-clipping are all M3.")
row("DEFINE-BEFORE-USE", "2.9-prose", "first uses of tenor, trace, cosine, PSD, eigenvalue clipping, orthogonal, Frobenius, explained share (L08 52-58, 137, 141; L09 52-65, 109-116)",
    "Body text defines before use: tenor and yield change (L08 line 56), trace (L08 line 58, L06 Proposition 2.4), cosine (L08 line 137), column space (L07 line 56), Frobenius norm (L09 line 65), eigenvalue clipping (L09 lines 111-116). Why-it-matters paragraphs (L07 52, L08 52, L09 52) name Definitions and Methods by pointer ('Definition 1.3 of this lesson', 'Method 1, Section 4') before the body defines them; that is a forward pointer, not an undefined use.")
row("DEFINE-L08-OVERLINE", "2.9-prose (terms before definition)", "course/modules/M/M3/L08.html line 137 (the centred squared tenors \\tau^{2} - \\overline{\\tau^{2}}\\iota_n)",
    "FIXED since round 10. Line 137 now defines \\overline{\\tau^{2}} = (1/n) sum_j tau_j^2 ('the mean of the squared tenors') before the expression \\tau^{2} - \\overline{\\tau^{2}}\\boldsymbol{\\iota}_n is used in the same sentence. grep: \\overline occurs only on line 137 (definition and use, in that order).")
row("PLAIN-REDEF", "2.9-dag", "L09.html line 68 (orthogonal matrices cross-reference) and line 56 (trace, symmetry)",
    "Cross-references only; no plain term is redefined (eigenvalue, singular value, trace, orthogonal stay plain or cross-referenced to Lesson 6).")

# ---- prose ----
row("PROSE-PROCESS", "2.9-prose", "L07, L08, L09 learner text (banned and process-word sweep)",
    "grep (case-insensitive) for verif, builder, ledger, agent, architect, planner, reviewer, pilot, orchestrat, fragment, scaffold, placeholder, TODO, FIXME, TBD, lorem, 'round ', 'this unit', 'M3-c', 'Lab 1 twin': no process words. One hit, L07 line 212 'the orthogonality check in Lab 1 verifies the algebra', is learner-facing English about the lab.")
row("PROSE-ELLIPSIS", "2.9-prose", "L07.html 398, 412; L08.html 445, 459, 505; L09.html 527, 536 (quiz stems ending in an ellipsis)",
    "Seven quiz stems end with an ellipsis before the answer options (e.g. 'the matrix A^T A is...' followed by 'invertible' / 'not invertible' / 'equal to the identity'). The ellipsis introduces the options; it stands for no omitted content. No TODO, lorem, placeholder or 'for brevity' text. PASS on that reading.")
row("PROSE-SCOPE", "2.9-prose", "scope words on the three pages (always, only, exactly, every, all, any, same, whenever, guarantee, not always, stable, real data, real curve)",
    "Checked each flagged sentence: 'always' appears only inside quoted misconceptions or quiz distractors, or as 'not always' supported by the 23 instances (L09 canon heading; L09 lines 352-353); 'exactly' statements are theorem-level (L08 line 111, 137) or lab-scoped; 'whenever' and 'guarantee' are restricted by the hypotheses stated beside them (L08 293, L09 line 184); 'real data' / 'real curve' sentences disclaim claims (L07 line 204, L08 lines 52, 292, 295). 'Every' and 'all' follow proofs over every vector or every entry, or are scoped to the tested seeds. No unsupported scope claim found.")
row("PROSE-REMARK-2.4", "2.9-prose", "L08.html Remark 2.4 (131-133) and its last sentences",
    "Remark 2.4 proves the non-multiple claim (M' = kappa M impossible when M_jl != 0 and c not in {0, 1}), says the shares 'can then change', and states that the lab shows one case with no general rule. The one-case claim is covered by key-results row 434 (C). Re-derived in the section above (MATH-L08).")
row("STRUCT-WHY", "2.9-structure", "L07 line 52, L08 line 52, L09 line 52 (why-it-matters)",
    "Raw word counts with math kept as typed (ledgers/M3/scripts/M3-c-r11/out/page_smoke and this round's count): L07 110, L08 114, L09 115 words; limit 120 (BUILDER_RULES 4.2(1)).")
row("STRUCT-ORDER", "2.9-structure", "L07, L08, L09 section order and counts (BUILDER_RULES 4.2)",
    "Order: why-it-matters, core sections, inline lab, canon-breaks, misconceptions (3 each), problem set (3 per tier, 12 total with 12 details solutions each), key-results table, quiz (L07 9 items, L08 9, L09 11; every item has an explain block), references, nav. Debate brief not required (curriculum has no debate key for M3).")
row("HOURS", "2.9-hours", "L07.html data-hours 11 (line 2, eyebrow 35), L08.html 12, L09.html 12; index.html line 29 data-hours-lessons 105 and data-hours-project 45",
    "Lesson hours L01 12, L02 11, L03 12, L04 12, L05 12, L06 11, L07 11, L08 12, L09 12 sum to 105, equal to the hub's data-hours-lessons (index.html line 29). 105 + 45 = 150 = the curriculum figure (plan section 0). Project share 45/150 = 30%, inside 10-40%. check_pages --unit M3 passes (GATE-01).")

# ---- data, honesty, simulation ----
row("DATA-CLAIM", "2.8-data", "L08.html canon-break (line 291) 'The program does not yet embed a multi-tenor series from which three or more tenors can be read'",
    "course/assets/data/market/MANIFEST.json entry ust_daily: 'Daily 3-month Treasury bill and 10-year Treasury constant-maturity yields' (two tenors); fx_daily columns are currency series, not tenors. The claim is true on the embedded data.")
row("HONEST-GAP", "2.8-data", "L08.html canon-break (line 291) and the Section 1 note (line 52)",
    "The curriculum's Treasury-curve lab is not run on embedded data; the page states that a SIMULATED six-tenor panel is used instead and that no real curve is claimed. This matches the architect's B2 decision (plan section 9 and 'Architect decisions').")
row("SIMULATED-LABELS", "2.8-data", "L07 lab (docstring line 128, hypothesis line 125), L08 lines 145-151 and twin docstring line 149, L09 lines 190, 199 and 346",
    "Every simulated panel, design and matrix set is labelled SIMULATED in the page and in the twin docstring; key-results rows 433, 434, 496, 497 carry SIMULATED.")

# ---- delta and card rows ----
row("DELTA-READ", "2.0-delta", "delta 47a36d8c..ccaeeaf4 for slice c (git diff)",
    "Byte-identical since the previous pin: L07.html, tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py. Changed and read hunk by hunk: L08.html line 137 (adds the definition of \\overline{\\tau^{2}}), L09.html line 122 (adds 'Lesson 5, Definition 1.4' to Proposition 3.2(b)), course/modules/M/M3/index.html line 155 (L08 card title), cards.json (card M3-c167 back rewritten at line 1146; cards M3-c208 to M3-c213 added at lines 1410-1441). Other changed files in the repo (references.json, curriculum files, CURRICULUM.md, other units' twins and projects) are outside slice c and were covered by the gates (GATE-09, 11, 12, 13) or by the project slice.")
row("HYP-L08-DEF31", "2.4-math/2.9-structure", "L08.html Section 3 (line 137) and Definition 3.1 (line 141)",
    "Definition 3.1 assumes F1 to F4 and at least three distinct tenor values (stated, 'Section 3'); Section 3 proves the curvature shape nonzero under exactly that hypothesis and shows the two-value case gives a zero curvature shape.")
row("CARDS-DUP-SCAN", "2.7-cards", "course/modules/M/M3/cards.json (all 208 cards)",
    f"{CS}: 208 cards, 208 unique ids, no exact duplicate fronts or backs. 19 front pairs with Jaccard >= 0.6 reviewed; the slice-c pairs (c118/c120, c136/c201, c154/c155, c194/c195) ask different facts. Id gaps (c102, c148, c191, c204, c206) are not defects. Grade and basis rules hold (every C card has a basis; no unknown grades).")
row("CARDS-READ-L07-L09", "2.7-cards", "course/modules/M/M3/cards.json, the 77 cards with lesson L07 (21), L08 (28) or L09 (28)",
    "All 77 cards read in full and checked against the current lesson text (extract: ledgers/M3/scripts/M3-c-r11/out/cards_L07_L09.txt). Numbers on cards appear in their lessons (e.g. 1.3325, 0.8951, 0.9994/0.9985/0.9990, 0.7587/0.9791, 0.6400000000, 23, 0.175527/0.163280, 0.08, 0.04, 0.9798 not on a card but in L09 line 444). No card contradicts a lesson; no card is trivia.")
row("CARD-C127", "2.7-cards / 2.4-math", "cards.json entry M3-c127 (line 873, L07, grade T) vs L07.html misconception 1 (lines 220-223) and Remark 1.4 (94-95)",
    "The card back (residual orthogonal to the columns, not zero; Remark 1.4 gives the squared residual as the part of ||y||^2 not captured by ||Py||^2) matches the lesson text and the proof.")
row("CARD-C167", "2.7-cards / 2.2-claims", "cards.json entry M3-c167 (line 1146, L09, grade C, basis Lab 1) vs L09.html misconception 3 (line 372) and the printed output (lines 342-344)",
    "Rewritten card back: an alternating-projection output that passes the lab's correlation check is strictly closer to the input than the clip-and-rescale matrix; grade C; basis names Lab 1 with the 40 seeded matrices. Matches output 23 of 23 and 23 of 23 (lab_check.out) and the misconception text (L09 line 372).")
row("CARDS-NEW-c208-c213", "2.7-cards / 2.4-math", "cards.json M3-c208 (line 1410, L09, T), M3-c209 (L07), M3-c210 to M3-c213 (L08)",
    "c208 gives Method 1 with the Proposition 3.4 and 3.2(a) hypotheses (L09 lines 182); c209 column space (L07 line 56); c210 cosine (L08 line 137); c211 orthogonalization with Lesson 7 Theorem 1.2 (L08 line 137); c212 tenor and c213 yield change in basis points (L08 line 56). All match the current text.")

# ---- hub title and navigation (round 10 FAIL, now fixed) ----
row("HUB-L08-TITLE", "2.9-structure (cross-page title agreement)", "course/modules/M/M3/index.html line 155 (hub card for L08)",
    "FIXED since round 10. Card title now 'Principal Component Analysis and Level-like, Slope-like and Curvature-like Directions', equal to the L08 h1 (L08.html line 36) and <title> (line 6), the L07 next link (L07.html line 437) and the L09 previous link (L09.html line 597). Card titles for L07 ('Orthogonal Projections and Least Squares') and L09 ('Nearest Correlation Matrices and Eigenvalue Clipping') equal their h1s. check_pages passes (GATE-01).")

verdict = "PASS" if all(r["status"] == "PASS" for r in R) else "FAIL"
frag = {
    "unit": "M3",
    "slice": "c",
    "round": 11,
    "verifier": "independent Haiku verifier (round 11), checkout verifyD11-M3-c",
    "pin": "ccaeeaf44bea94b37d912ec1da3c660bb2c55d87",
    "base": "47a36d8c78633793ccc762ae19dcd5e19b780d19",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD11-M3-c",
    "scratch": "ledgers/M3/scripts/M3-c-r11/ (scripts and out/ logs in the checkout)",
    "verified_at": "2026-11-05",
    "verdict": verdict,
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": ("FULL verification of L07, L08, L09 and their three lab twins, round 11, at pin ccaeeaf4. Previous pin 47a36d8c. "
              "Delta read hunk by hunk (L08.html line 137, L09.html line 122, index.html line 155, cards.json c167 and c208-c213). "
              "Both round-10 FAIL rows (DEFINE-L08-OVERLINE, HUB-L08-TITLE) re-verified from scratch and fixed. "
              "All 77 slice cards read; all 208 cards scanned. Every L07-L09 line read. Every number recomputed by an alternative route in "
              "ledgers/M3/scripts/M3-c-r11/recompute.py. Mutants: none, because this is a lab slice (VERIFIER_RULES 2.6 mutation applies to project graders only; project graders belong to the project slice). "
              "Not run here: run_graders and mutate_graders for the M3 project (outside slice c); live verify_refs (offline ruling); visual screenshots (page_smoke PASS relied upon). "
              "Pre-existing tracked files under ledgers/M3/scripts/M3-c-r11/ (from an earlier batch) were left unchanged; ledgers/M3/M3-c.json (previously a round-18 fragment) was overwritten per this assignment."),
    "summary": f"M3 slice c round 11 at pin ccaeeaf4: {len(R)} rows (pass={sum(r['status']=='PASS' for r in R)} fail={sum(r['status']=='FAIL' for r in R)} unverifiable={sum(r['status']=='UNVERIFIABLE' for r in R)}). Non-PASS: none. Both round-10 FAIL rows fixed and re-verified.",
}
out = ROOT / "ledgers/M3/M3-c.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(R), "verdict", verdict)
