"""Write the round 10 slice-c ledger fragment ledgers/M3/M3-c.json and validate it with tools/ledger.py.

Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-c-r10/write_fragment_r10.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

OUT = "ledgers/M3/scripts/M3-c-r10/out/"
SCRIPTS = "ledgers/M3/scripts/M3-c-r10/"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


# ---- gates (fresh at pin 47a36d8) ----
row("GATE-01", "2.9-gate", "tools/check_pages.py --unit M3; --unit M3 --page L07, L08, L09", "PASS",
    f"{OUT}check_pages_M3.out 'check_pages M3: PASS' exit 0; check_pages_L07.out, _L08.out, _L09.out each 'PASS' exit 0. "
    "why-it-matters word counts (script-free count on the page): L07 109, L08 114, L09 116 words (limit 120).")
row("GATE-02", "2.9-gate", "tools/check_dag.py --unit M3", "PASS", f"{OUT}check_dag_M3.out 'check_dag M3: PASS' exit 0.")
row("GATE-03", "2.6-gate", "tools/check_projects.py --unit M3", "PASS",
    f"{OUT}check_projects_M3.out 'check_projects M3: PASS' exit 0 (unit gate; the M3 project is slice d).")
row("GATE-04", "2.5-labs", "tools/run_labs.py --unit M3", "PASS", f"{OUT}run_labs_M3.out 'run_labs M3: PASS (12/12)' exit 0.")
row("GATE-05", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py run alone as python -I -W error",
    "PASS", f"{OUT}twin_vs_page.out: each twin exit=0, stderr_bytes=0; direct runs take 0.06 s each (time -p). Exit 0.")
row("GATE-06", "2.5-labs", "ruff check and ruff format --check on the three slice-c twins", "PASS",
    f"{OUT}ruff_check_labs.out 'All checks passed!' exit 0; {OUT}ruff_format_labs.out '3 files already formatted' exit 0.")
row("GATE-07", "2.4-gate", ".venv/bin/mypy --no-incremental", "PASS",
    f"{OUT}mypy.out 'Success: no issues found in 385 source files' exit 0.")
row("GATE-08", "2.9-gate", "tools/page_smoke.py --unit M3 --pages L07, then L08, then L09 (each alone)", "PASS",
    f"{OUT}page_smoke_L07.out, page_smoke_L08.out, page_smoke_L09.out: each 'page_smoke M3: PASS' exit 0.")
row("GATE-09", "2.1-citations", "tools/verify_refs.py --offline (whole registry)", "PASS",
    f"{OUT}verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' exit 0. Slice c cites no registry key.")
row("GATE-10", "2.5-labs", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k 'M3 or run_labs or page' -q",
    "PASS", f"{OUT}pytest_relevant.out: all dots, exit 0.")
row("GATE-11", "2.9-gate", "tools/build_site.py --check (concept rename and generated site data)", "PASS",
    f"{OUT}build_site_check.out 'site data current: 6 outputs' exit 0.")
row("GATE-12", "2.9-gate", "tools/render_curriculum.py then git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json",
    "PASS", f"{OUT}render.out 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h'; {OUT}render_diff.out exit 0 "
    "(regeneration left both files byte-identical).")
row("GATE-13", "2.8-data", "tools/fetch_data.py --check", "PASS", f"{OUT}fetch_data_check.out '3 datasets, 0 problems' exit 0.")

# ---- labs ----
row("LAB-L07-EMBED", "2.5-labs", "course/modules/M/M3/L07.html section#lab-M3-L07-1 vs tests/labs/M3/lab-M3-L07-1.py", "PASS",
    f"{OUT}twin_vs_page.out 'L07 page code == twin: True', 'L07 expected == output: True' ({SCRIPTS}twin_vs_page.py).")
row("LAB-L08-EMBED", "2.5-labs", "course/modules/M/M3/L08.html section#lab-M3-L08-1 vs tests/labs/M3/lab-M3-L08-1.py", "PASS",
    f"{OUT}twin_vs_page.out 'L08 page code == twin: True', 'L08 expected == output: True'.")
row("LAB-L09-EMBED", "2.5-labs", "course/modules/M/M3/L09.html section#lab-M3-L09-1 vs tests/labs/M3/lab-M3-L09-1.py", "PASS",
    f"{OUT}twin_vs_page.out 'L09 page code == twin: True', 'L09 expected == output: True'.")
row("LABSTMT-L07", "2.5-labs", "L07.html line 125 (hypothesis); code 126-192; expected 193-203; interpretation 204", "PASS",
    "Hypothesis read against the twin: n = 12, seed 7, intercept and two regressors; P symmetric and idempotent; Py = A beta; "
    "residual orthogonal to columns; Pythagorean identity; agreement with the direct solver to 1e-9; coefficients and residual "
    "to 4 decimals; A^T y to 2 decimals; duplicated column gives rank 2 of 3 and a null-direction pair with equal fits (code "
    "lines 183-189 use dup = [a0, a1, a1], i.e. the second regressor replaced by a copy of the first, as stated). Output "
    "lines 194-203 match the twin run.")
row("LABSTMT-L08", "2.5-labs", "L08.html line 146 (hypothesis); code 147-269; expected 270-283; interpretation 284", "PASS",
    "Hypothesis matches the twin: T = 750, six tenors 0.25 to 10, planted scales 8, 4, 2 bp and noise 0.5 bp (code 167-199); "
    "M PSD, MV = V Lambda, Z^T Z/(T-1) = Lambda, eigenvalue sum = trace (lines 220-229); shares from unrounded eigenvalues "
    "(231-235); planted shapes matched with distinct components (238-246); doubling (248-253); 0.25-year column times 10 "
    "(254-259); E1 bound with M11 and trace printed (260-266). Expected block equals the twin output.")
row("LABSTMT-L09", "2.5-labs", "L09.html line 190 (hypothesis); code 191-332; expected 333-345; interpretation 346", "PASS",
    "Hypothesis matches the twin: C0 not PSD with witness -2.4; clipped B has ||C0-B||_F^2 = sum of squared negative eigenvalues "
    "(prints 0.6400000000 both); R is a correlation matrix (True); for the 23 non-PSD matrices among 40 seeded 5x5 matrices, "
    "counts of is_correlation passes and strictly-closer cases (prints 23 of 23 and 23 of 23). Non-PSD cut NONPSD_TOL = 1e-9 "
    "(code line 308) matches the hypothesis.")
row("LABSTMT-RUNTIME", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py (imports, seeds, network, runtime)",
    "PASS", "Static read: imports are numpy (and numpy.typing) only. Seeds explicit: default_rng(7), default_rng(8), "
    "default_rng(20261028). No network or file reads. Each twin runs in 0.06 s (time -p), under 10 s.")
row("LABDOC-L09", "2.2-lab-prose", "tests/labs/M3/lab-M3-L09-1.py docstring claims 1-4 (page lines 191-211) vs code and output",
    "PASS", f"Claim 1: 'x^T C0 x = -2.400000; C0 is not PSD: True' ({OUT}run_labs / twin output). Claim 2: ||C0-B||_F^2 = "
    "0.6400000000 = sum of squared negative eigenvalues (printed). Claim 3: 'R = rescaled B is a correlation matrix: True'. "
    "Claim 4: generator (off-diagonal 0.5 + symmetrised N(0, 0.35) noise, unit diagonal, size 5, seed 20261028) matches "
    "code lines 271-279; repair procedure and is_correlation tolerances match lines 248-266.")
row("LABDOC-L09-TOL", "2.2-lab-prose", "L09.html lines 190 and 346 vs twin constants TOL=1e-12, FEASIBLE_TOL=1e-8, NONPSD_TOL=1e-9",
    "PASS", "Twin lines 220-222 define the three constants; L09.html line 190 quotes 10^{-12} and -10^{-8}; line 346 quotes "
    "10^{-12}, -10^{-8} and -10^{-9}. All match.")

# ---- numbers (re-derived by ledgers/M3/scripts/M3-c-r10/m3c_r10_numbers.py, output in out/m3c_r10_numbers.out) ----
NUM = f"{OUT}m3c_r10_numbers.out"
row("NUM-L07", "2.2-numbers", "L07.html lines 199-203 (expected), 222 (residual 0.8951), 302 (A^T y), 307-309 (intercept 1.3325), M2 line 252",
    "PASS", f"{NUM}: QR-route beta 1.3325 0.8488 -0.4120; residual norm 0.8951; A^T y 18.38 3.10 -17.60. M2 exact (Fractions): "
    "beta0 = 7/6, beta1 = 1/2, fitted 7/6, 5/3, 13/6; residuals -1/6, 1/3, -1/6 sum to 0 (checked by hand in the script's exact block).")
row("NUM-L07-M", "2.2-numbers", "L07.html line 350 (rank 2 of 3) and the duplicated-column check", "PASS",
    f"{NUM}: singular values of the duplicated A^T A 12.9139, 8.9701, 7.13e-32; rank 2.")
row("NUM-L08", "2.2-numbers", "L08.html lines 275, 284 (75.9, 18.1, 5.2; cosines 0.9994, 0.9985, 0.9990), 282 (0.7587, 0.9791), "
    "283 and 391 (0.9483; 13.6818; 88.2028), 391 (sum 99.2, 0.15), 304 (min cosine 0.9985), 432 and 434 (key results)",
    "PASS", f"{NUM}: SVD-route shares 75.872815, 18.088840, 5.161927 (round to 75.9, 18.1, 5.2); |cos| 0.999381, 0.998544, "
    "0.999019 (round to 0.9994, 0.9985, 0.9990); first share after x10 on 0.25y column 0.979145 (0.9791); bound 0.948346 "
    "(0.9483), with M11 13.6818 and trace 88.2028 reproduced; doubled-panel shares equal to 2e-16. E3 sum 99.2 and bound 0.15 "
    "follow from the 0.05-per-entry rounding.")
row("NUM-L09", "2.2-numbers", "L09.html lines 52, 336, 345-347, 401 (M3), 444 (0.9798), 452 (0.25, 0.5), 494-497, 175-177 (Example 3.6)",
    "PASS", f"{NUM}: C0 eigenvalues -0.8, 1.9, 1.9; ||C0-B||_F^2 = 0.64; R off-diagonal 0.5, 0.5, -0.5; ||C0-R||_F = 0.9797958971 "
    "= sqrt(0.96) (0.9798); Example 3.6 A0 = [[1.1,1.1],[1.1,1.1]], ||A-A0||^2 = 0.04, ||A-R||^2 = 0.08; non-PSD count 23 of 40; "
    "first non-PSD index 0: ||A-R|| 0.175527, ||A-W|| 0.163280. M3 by hand: [[4,2],[2,9]] has trace 13, det 32, roots (13 +- sqrt 41)/2, "
    "so both positive; C = [[1,1/3],[1/3,1]].")
row("ALT-L09", "2.5-labs (robustness)", "tests/labs/M3/lab-M3-L09-1.py repair procedure vs alternative correct procedures",
    "PASS", f"{NUM}: (i) eig-route clip (np.linalg.eig, real part, QR reconstruction) agrees with eigh clip to 2.0e-15; "
    "(ii) alternating projections re-run with tolerance 1e-10 and with tolerance 1e-14 and 5000 steps: passes 23 of 23 and "
    "closer 23 of 23 in each rule; minimum margin ||A-R|| - ||A-W|| = 3.9e-5 (positive, so the 'all 23' claim is not an artefact "
    "of the stopping rule); the first case W has smallest eigenvalue -7.1e-13 and converges in 28 steps.")
row("ALT-L08", "2.5-labs (robustness)", "L08.html Lab 1 eigh-based PCA vs an SVD route", "PASS",
    f"{NUM}: singular values of the centred panel give the same shares (75.872815, 18.088840, 5.161927) and cosines as the "
    "lab's eigh route to the printed precision; the planted shapes are rebuilt by Gram-Schmidt rather than the lab's projections.")

# ---- mathematics ----
row("MATH-L07", "2.4-math", "L07.html Definition 1.1 (60), Theorem 1.2 (64-71) and proof (75-81), Theorem 1.3 (84-85) and proof (88-90), "
    "Remark 1.4 (93-95), Definition 2.1 (103-104), Theorem 2.2 (107-113) and proof (117-120)", "PASS",
    "Re-derived line by line: G symmetric, x^T G x = ||Ax||^2 > 0; invertibility via V Lambda^-1 V^T and V V^T = I, which is "
    "L06.html Fact 1.2 (lines 64-66: Q^T Q = I implies Q Q^T = I). A^T(y-p) = 0; uniqueness of p; (c) P^T = P and P^2 = P; "
    "Theorem 1.3 expansion; Remark 1.4 with w = 0; Theorem 2.2 (a)-(c) with the proof's two directions. No gap found.")
row("MATH-L08", "2.4-math", "L08.html Proposition 1.1 (61-62), Proposition 1.2 (71-72), Definition 1.3 (82), Theorem 1.4 (86-93), "
    "Theorem 2.1 and proof (100-113), Corollary 2.2 (116-117), Proposition 2.3 and proof (121-127), Remark 2.4 (131-133), "
    "Section 3 (137) and Definition 3.1 (141)", "PASS",
    "Re-derived: Prop 1.1 (x^T M x = ||X~x||^2/(T-1)); Prop 1.2; Theorem 1.4 Z^T Z = (T-1) V^T M V = (T-1) Lambda; "
    "Theorem 2.1 (a) equality case via sum (lambda_1 - lambda_i) alpha_i^2 = 0 and (b) via lambda_i <= lambda_k for i >= k; "
    "Prop 2.3 (M -> c^2 M, c^2 > 0 preserves order); Remark 2.4 (M_jj > 0 from x = e_j + t e_l; M' = kappa M forces kappa = c "
    "and then M_jj(c^2 - c) = 0, false for c != 0, 1); Section 3: with two values tau^2 = -ab iota + (a+b) tau, so the curvature "
    "shape vanishes; with three values a quadratic with leading coefficient 1 cannot vanish at three points. Definition 3.1 "
    "normalization needs nonzero shapes, which the three-value hypothesis gives.")
row("MATH-L09", "2.4-math", "L09.html Definition 1.1 (59-60), Definition 1.2 (64-65), Lemma 1.3 and proof (74-82), Definition 2.1 "
    "(89-90), Remark 2.2 (95), Example 2.3 (99-105), Definition 3.1 (112-115), Propositions 3.2-3.5 and proofs (119-171), "
    "Example 3.6 (174-177), Methods 1 and 2 (182-184)", "PASS",
    "Re-derived: Lemma 1.3 needs only Q^T Q = I and tr(XY) = tr(YX); Prop 3.2 (a) PSD and eigenvalues max(lambda, eps), (b) "
    "x^T A_eps x >= eps ||x||^2; Prop 3.3 (a) sum over lambda < eps of (eps - lambda)^2 and (b) equality iff no lambda < eps; "
    "Prop 3.4 congruence with D^{-1/2}, needs positive diagonal (stated); Prop 3.5 quadratic form along e_i + t e_j with delta = "
    "|b_ij|/(1+b_jj); Example 3.6 numbers; canon-break 3 monotonicity of the distance in eps (each term (eps - lambda)^2 "
    "grows with eps and new terms appear) is correct.")
row("PROP23-HYP", "2.4-math", "L08.html Proposition 2.3 statement (122), proof (127), E2 (384), key row 432", "PASS",
    "Hypotheses stated: real X, c nonzero, sum of eigenvalues > 0 for the shares. E2 and key row 432 restate them; the proof uses "
    "centred data of cX = c X~ and M -> c^2 M.")
row("KEY-L08-430", "2.9-key-results", "L08.html key-results row 430 vs Theorem 1.4 (line 87)", "PASS",
    "Row states the scores identity and shares summing to 1 under a positive eigenvalue sum; Theorem 1.4 states the same with the same hypotheses.")
row("PROB-L07", "2.4-math", "L07.html problems M1-M3, P1-P3, E1-E3, R1-R3 (lines 241-336)", "PASS",
    f"Every solution re-derived; E1-E3 numbers match {NUM}; R1 existence argument (Theorem 3.7 of Lesson 1, L01.html line 161) "
    "checked; R2 linearity; R3 identities; P3 null-space argument.")
row("PROB-L08", "2.4-math", "L08.html problems M1-M3, P1-P3, E1-E3, R1-R3 (lines 323-419)", "PASS",
    "Every solution re-derived by hand. M1: X~ = [[-2,-3],[0,-1],[2,4]], M = [[4,7],[7,13]], trace 17, det 3, eigenvalues "
    "(17 +- sqrt 277)/2 (script output). E1 bound 100 M11/(S0 + 99 M11) = 0.948346. E3: rounding error at most 0.05 per "
    "rounded share, sum bound 0.15 (99.2 +- 0.15). R1 tie argument. R3 rank argument.")
row("PROB-L09", "2.4-math", "L09.html problems M1-M3, P1-P3, E1-E3, R1-R3 (lines 379-479)", "PASS",
    "Every solution re-derived. M1 eigenvalues 1.6, 0.4; M2 4.88 (= 2.2^2 + 0.2^2); M3 (13 +- sqrt 41)/2 and C_12 = 1/3; P1 bound "
    "via t = +/-1; P2 trivial null space; P3 convexity; E1 -2.4 term by term; E2 0.9798 (script); E3 0.5 from Prop 3.3(a); "
    "R1 split; R2 diag(1,4) -> identity; R3 norm identity.")

# ---- grades ----
row("GRADE-L07", "2.3-grades", "L07.html block titles (64, 84, 108; Remark 1.4 at 93 has the key-results T at 348) and key-results table (346-350)",
    "PASS", "Theorems 1.2, 1.3, 2.2 and Remark 1.4 are T with complete proofs under the stated hypotheses (F1-F4 and independent "
    "columns, as written); the Lab 1 row (350) is C and labelled a finite numerical check on a SIMULATED design.")
row("GRADE-L08", "2.3-grades", "L08.html block titles (61, 71, 86, 100, 116, 121) and key-results table (428-434)", "PASS",
    "Propositions 1.1, 1.2, Theorem 1.4, Theorem 2.1, Corollary 2.2, Proposition 2.3 are T with proofs; the two lab rows (433, 434) "
    "are C and say SIMULATED and one simulated panel.")
row("GRADE-L09", "2.3-grades", "L09.html block titles (59, 63, 70, 89, 111, 118, 147, 159, 174) and key-results table (488-497)", "PASS",
    "Definitions 1.1, 1.2, Lemma 1.3, Propositions 3.2-3.5 and Examples 2.3 and 3.6 are T (exact arithmetic on the page); the two "
    "seeded-run rows (496, 497) are C with 'finite seeded check' and 'one machine run'.")

# ---- citations, cross-references, DAG, notation ----
row("CITE-L07-L09", "2.1-citations", "L07.html, L08.html, L09.html (no data-cite or data-locator attributes; empty data-references lists)",
    "PASS", "grep -c 'data-cite|data-locator' on the three pages: 0 each (grep run this round). The references paragraphs say no result "
    "is attributed to an outside source.")
row("XREF-EARLIER", "2.9-xref", "earlier-lesson cross-references in L07, L08, L09", "PASS",
    "Each locator read this round in the checkout: L01 Theorem 3.7 (line 161, spanning list vs independent list); L01 vector space "
    "(line 57); L03 Definition 1.1 (line 61, eigenvalue and eigenvector) and def-eigendecomposition (line 109); L04 Definition 1.1 "
    "(line 68, transpose and symmetry), Theorem 2.3 (spectral theorem, id def-spectral-theorem); L05 Definition 1.4 (line 71-72), "
    "Theorem 2.1 (line 108-110: PSD iff every eigenvalue nonnegative); L06 Definition 1.1 (line 59, orthogonal matrix), Fact 1.2 "
    "(line 64), Proposition 2.4 (line 126, Frobenius and trace), Remark 2.5 (line 228, sign freedom).")
row("DAG-PSD-REDEF", "2.9-dag", "course/modules/M/M3/L09.html line 56 versus L05.html Definition 1.4 (line 71)", "PASS",
    "L09 line 56 links L05 (href L05.html#def-positive-semidefinite-matrix) and does not define PSD; the only dfn ids on L09 are "
    "def-nearest-correlation-matrix and def-eigenvalue-clipping.")
row("NOTATION-R", "2.9-notation", "L07, L08, L09 math using \\R", "PASS",
    "notation/notation.json macros: \\R = real numbers. Census this round (grep -o -E): \\R used on L07 (13) and L08 (6), meaning as registered.")
row("NOTATION-OPNAME", "2.9-notation", "registered \\tr and \\diag: L08 lines 56-72, 137; L07 lines 56-, 332; L09 lines 56, 176, 182",
    "PASS", "Registered macros \\tr (matrix trace) and \\diag (diagonal matrix) are used with those meanings. \\operatorname (L08 line 402) "
    "and \\mathrm (L09 one use) are standard KaTeX.")
row("NOTATION-T", "2.9-notation", "L08.html Section 1 (line 56: T x n matrix, T >= 2) and Lab 1 (T = 750)", "PASS",
    "Registered symbol T: 'number of return observations (periods) in a sample' (notation.json symbols). L08 uses T for the number of "
    "rows (observations) of the data matrix; consistent in the lab (T_DAYS = 750).")
row("NOTATION-AST", "2.9-notation", "L09.html lines 90 and 93 (C^{\\ast}: nearest correlation matrix)", "PASS",
    "Registered R^{\\ast} (SDF return) is not used on the three pages; C^{\\ast} is a different symbol, local to the lesson.")
row("NOTATION-Q", "2.9-notation", "L07 and L09 orthogonal Q; \\mathbb{Q} registered for a probability measure", "PASS",
    "Plain Q is lesson-local (notation.json about: conventionally local letters are defined where used); \\mathbb{Q} does not "
    "appear on the three pages (grep, this round).")
row("NOTATION-OTHER", "2.9-notation", "all control sequences in math on the three pages", "PASS",
    "Census this round (grep -o -E '\\\\[A-Za-z]+'): L07 top, beta, hat, in, gamma, R, Lambda, perp, diag; L08 top, lambda, tilde, sum, "
    "alpha, Lambda, tau, iota, boldsymbol, bar, overline, kappa, Gamma, cos, tr, diag; L09 top, varepsilon, lambda, Lambda, sqrt, "
    "max, min, delta, ast, mathrm, tfrac. None is a registered symbol with another meaning. Greek letters are lesson-local per "
    "notation.json 'about'. The registered \\gamma_3, \\gamma_4, \\Phi, R_f, \\E, \\Var and \\Cov are not used.")
row("DEF-L08-CLOSE", "2.9-structure", "L08.html Definition 3.1 (141), quiz item L08q9 (505-511)", "PASS",
    "Quiz item states the level-like rule with the unique-largest |cos| condition; its explanation matches Definition 3.1, including the tie case.")
row("DEF-L08-MATCH", "2.2-lab-prose", "L08.html Definition 3.1 (141), canon-break (292), quiz explanation (511), lab main() match loop (twin lines 238-246)",
    "PASS", "The lab computes argmax of |cos| per planted shape and prints 'the three planted shapes match three different components: True'; "
    "the text and the lab agree.")
row("DAG-LINKS", "2.9-dag", "L07.html, L08.html, L09.html meta rows (lines 38-39)", "PASS",
    "check_dag M3 PASS (GATE-02). L07 uses L01 vector space; L08 uses L03, L04, L05; L09 uses L03, L04, L05; Introduces links point to "
    "the lesson's own dfn ids.")
row("DAG-M4", "2.9-dag", "L07-L09 covariance, variance, correlation, expectation, floating-point wording", "PASS",
    "grep -i for variance, covariance, expectation, Cholesky, IEEE, floating on the three pages: only L09 line 497 'floating point' "
    "as a plain descriptor of the one-machine lab run. The registered IEEE 754 concept (curriculum M8) is not used by name or link.")
row("DAG-PROSE-UNLINKED", "2.9-dag", "L09.html line 60 and other unlinked uses of positive semidefinite", "PASS",
    "Each PSD mention after L09 line 56 refers to the concept defined in L05 (Definition 1.4), so no concept is used before its lesson.")
row("CONCEPT-L08-LSC", "2.9-dag/2.3-grades", "course/modules/M/M3/L08.html line 39 (Introduces link text), line 141 (dfn id=def-level-slope-curvature); "
    "curriculum/curriculum.json concepts['level-slope-curvature'].name (line 3510) and concept index (line 6405); "
    "curriculum/01-foundations.yaml line 175; course/concepts.html line 139; course/assets/data/glossary.json line 1095",
    "PASS", "Round 9 FAIL is fixed by commit c829fb1f. The registered name is now 'Level-like, slope-like and curvature-like principal "
    "directions' in yaml (line 175), curriculum.json (lines 3510, 6405), the generated concepts.html (line 139) and glossary.json "
    "(line 1095); the L08 Introduces text and dfn text match it. The id is defined once (L08 line 141). grep finds no old name "
    "in the slice or its concept outputs.")
row("DEFINE-BEFORE-USE", "2.9-prose", "first uses of tenor, trace, cosine, PSD, eigenvalue clipping, orthogonal, Frobenius, correlation "
    "matrix, nearest correlation matrix, column space, null space, positive definite, congruence, residual, fitted vector", "PASS",
    "tenor and yield change defined in L08 line 56 before Section 3; trace and Frobenius from L06 Proposition 2.4 (cross-referenced); "
    "orthogonal matrix from L06 Definition 1.1; PSD from L05 Definition 1.4; eigenvalue clipping and nearest correlation matrix "
    "defined on L09 (lines 90, 113); column space defined in L07 line 56; null space is the kernel of Lesson 2, Definition 1.3 (L02.html line 71); congruence and its meaning "
    "given in L09 line 368; residual and fitted vector defined in L07 line 100. The symbol \\overline{\\tau^2} is covered by row "
    "DEFINE-L08-OVERLINE.")
row("DEFINE-L08-OVERLINE", "2.9-prose (terms before definition)", "course/modules/M/M3/L08.html line 137 (the centred squared tenors "
    "\\tau^{2} - \\overline{\\tau^{2}}\\,\\boldsymbol{\\iota}_n)", "FAIL",
    "The round-10 wording uses \\overline{\\tau^{2}}, the mean of the squared tenors, but the paragraph defines only \\bar\\tau, the "
    "mean of the tenors (line 137: 'Let tau_1..tau_n be the tenors and bar-tau their mean'). Grep: \\overline occurs once on the page, "
    "at line 137. The lab computes quad.mean() = (1/n) sum tau_j^2 (twin line 181-182), so the intended meaning is clear, but the "
    "symbol is undefined on the page.",
    "In L08.html line 137, after 'their mean' add a definition such as: 'and \\(\\overline{\\tau^{2}} = \\frac{1}{n}\\sum_{j=1}^{n}\\tau_j^{2}\\) "
    "the mean of the squared tenors'. Re-run check_pages --unit M3 --page L08 and page_smoke after the edit.")
row("PLAIN-REDEF", "2.9-dag", "L09.html line 68 (orthogonal matrices cross-reference) and line 56", "PASS",
    "L09 has no dfn or definition block for orthogonal matrix or transpose; both are cross-references to Lesson 4 and Lesson 6.")

# ---- prose ----
row("PROSE-PROCESS", "2.9-prose", "L07, L08, L09 learner text (banned and process-word sweep, including the round 10 sentences)",
    "PASS", "check_pages M3 L07, L08, L09 PASS (GATE-01). Grep this round for TODO, TBD, lorem, for brevity, details omitted, beyond the "
    "scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, "
    "clearly, it can be shown, round, verifier, builder, ruling, fixed, revised, corrected: no hit in learner text (only 'Fixed points "
    "of P' heading, 'fixed seed' and 'Previous' nav labels).")
row("PROSE-ELLIPSIS", "2.9-prose", "quiz stems ending in an ellipsis (L07 lines 398, 412; L08 445, 459, 505; L09 527, 536) and the L08 "
    "Section 3 curvature argument", "PASS",
    "Each stem ending in '...' is completed by its option list (a completion cue, not omitted content). The nonzero-curvature argument "
    "in L08 line 137 is complete (quadratic x^2 - beta x - alpha with leading coefficient 1 and three distinct roots).")
row("PROSE-SCOPE", "2.9-prose", "scope words on the three pages (always 7, only 33, exactly 17, every 83, all 66, any 38) and the round 10 "
    "hypothesis phrases", "PASS",
    "Each changed sentence checked: L08 line 137 (at least three distinct values; exactly two values gives the identity; one value "
    "gives zero slope); L09 line 52 ('in all 23' is the 23 counted in Lab 1, output 23 of 23 both counts); L07 line 210 ('for any A' "
    "holds because A beta ranges over W; Theorem 1.3's expansion uses only y - p perp W and p - w in W). The 'always' occurrences "
    "are misconceptions or distractors, and 'not always' (L09 line 7 and 353) is supported by the 23 lab cases. 'Exactly' uses "
    "were each checked against a proof or an explicit hypothesis.")
row("PROSE-REMARK-2.4", "2.9-prose", "L08.html Remark 2.4 (131-133) and its last sentences", "PASS",
    "The remark proves M is not a multiple of M after a single-column rescaling (M_jj > 0 argument, c not 0 or 1, M_jl not 0 "
    "hypothesis) and says the lab does not establish a general rule; the lab prints one case (first share 0.7587 -> 0.9791).")
row("STRUCT-WHY", "2.9-structure", "L07 line 52, L08 line 52, L09 line 52 why-it-matters", "PASS",
    "Word counts this round: L07 109, L08 114, L09 116 (each at most 120; GATE-01).")
row("STRUCT-ORDER", "2.9-structure", "L07, L08, L09 section order and counts (BUILDER_RULES 4.2)", "PASS",
    "Order: why it matters, numbered core sections, inline lab, canon-breaks, misconceptions (3 each), problem set (M/P/E/R, 3 each, "
    "worked solutions in details.solution), key results (grade and source columns), retrieval quiz (9, 9 and 11 items: 8-15), "
    "references, then nav. No debate brief: the M3 curriculum entry carries no debate key.")
row("HOURS", "2.9-hours", "L07.html data-hours 11, L08.html 12, L09.html 12; index.html data-hours-lessons 105", "PASS",
    "grep data-hours: L01 12, L02 11, L03 12, L04 12, L05 12, L06 11, L07 11, L08 12, L09 12, sum 105 = index data-hours-lessons 105; "
    "data-hours-project 45; total 150 = hub 'Tier F · 150 hours' and curriculum M3 hours 150.")
row("DATA-CLAIM", "2.8-data", "L08.html canon-break (line 291) 'The program does not yet embed a multi-tenor series ...' and Lab 1 heading (145)",
    "PASS", "course/assets/data/market/MANIFEST.json (read this round): fx_daily, fx_monthly, ust_daily; ust_daily columns "
    "['tbill_3m', 'cmt_10y'] (two series), so no series with three or more tenors is embedded. fetch_data --check: 3 datasets, 0 problems.")
row("HONEST-GAP", "2.8-data", "L08.html canon-break (line 291) and Section 1 note (line 52)", "PASS",
    "Canon-break states the curriculum Treasury-curve lab is not run and that the three-component claim is not made for any real curve; "
    "the gap is stated.")
row("SIMULATED-LABELS", "2.8-data", "L07 lab (124-128), L08 lines 145-151 and twin docstring, L09 lines 190, 199 and twin docstring",
    "PASS", "Each lab title or hypothesis carries SIMULATED (L07 line 124, L08 line 145, L09 line 190 'SIMULATED seeded'); the twin "
    "docstrings say SIMULATED and name the seeds; key-results rows for the labs say SIMULATED.")
row("DELTA-READ", "2.0-delta", "delta 1e272e5a..47a36d8c for slice c: L07.html (line 437), L08.html (lines 6, 36, 137, 141), "
    "L09.html (lines 52, 597), cards.json (M3-c127, M3-c167), curriculum/01-foundations.yaml (175), curriculum/curriculum.json (3510, 6405), "
    "tests/labs/M3 twins (unchanged; project-1 and project-2 changed, slice d)", "PASS",
    f"git diff 1e272e5a 47a36d8c read hunk by hunk; saved as {OUT}delta_slice_c_r10.diff (128 lines). Every changed hunk in the slice "
    "was re-read and re-verified in the rows above. The lab twins L07-L09 are byte-identical across the delta.")
row("HYP-L08-DEF31", "2.4-math/2.9-structure", "L08.html Section 3 (line 137) and Definition 3.1 (line 141)", "PASS",
    "Section 3 assumes at least three distinct tenor values (forces n >= 3) and gives the two-value identity; Definition 3.1 assumes the "
    "same before saying orthonormal and matched.")

# ---- cards ----
CARDS = f"{OUT}cards_L07_L09.txt"
row("CARDS-DUP-SCAN", "2.7-cards", "course/modules/M/M3/cards.json (all 202 cards)", "PASS",
    f"{SCRIPTS}cards_extract.py -> {CARDS}: total 202, duplicate ids 0, duplicate fronts 0; slice cards 71. Near-duplicate read: the "
    "pairs on the 23 seeded matrices (M3-c163, M3-c175) and on Corollary 2.2 (M3-c136, M3-c201) ask different questions.")
row("CARDS-READ-L07-L09", "2.7-cards", "course/modules/M/M3/cards.json, the 71 cards with lesson L07, L08 or L09 (M3-c115 to M3-c207)",
    "PASS", f"All 71 cards read this round against the current lesson text ({CARDS}). Hypotheses, grades, numbers and locators agree with "
    "the lesson; every card number (1.3325, 0.8488, -0.4120, 0.8951, 75.9/18.1/5.2, 0.9994/0.9985/0.9990, 0.7587/0.9791, 23 of 40, "
    "0.175527/0.163280, 0.64, 0.08, 0.04, 0.9798, rank 2 of 3) appears in its lesson or its lab output.")
row("CARD-C127", "2.7-cards / 2.4-math (hypothesis)", "course/modules/M/M3/cards.json entry M3-c127 (L07, grade T); L07.html misconception 1 "
    "(line 222) and Remark 1.4 (lines 93-95)", "PASS",
    "Round 9 FAIL is fixed: the back now reads 'Assuming F1 to F4 of Lesson 4 and independent columns of A' in both places, matching "
    "misconception 1 (line 222), which states the same hypotheses; the grade T matches Remark 1.4.")
row("CARD-C167", "2.7-cards / 2.2-claims (tolerance)", "course/modules/M/M3/cards.json entry M3-c167 (L09, grade C, basis Lab 1); "
    "L09.html misconception 3 (line 372) and canon-break 2 (line 353)", "PASS",
    "Round 9 FAIL is fixed: the back is now qualified 'In a SIMULATED Lab 1 case, a matrix that passes the lab check (smallest eigenvalue "
    "at least -1e-8) is strictly closer to the input, so up to that tolerance ...', matching misconception 3 (line 372) and canon-break 2 "
    "(line 353). The grade C matches the lab-based basis; the lab output 23 of 23 supports it (run this round).")

# ---- hub (new this round) ----
row("HUB-L08-TITLE", "2.9-structure (cross-page title agreement)",
    "course/modules/M/M3/index.html line 155 (hub card for L08)", "FAIL",
    "The hub card still reads 'Principal Component Analysis and the Yield-Curve Factors'. The L08 h1 (L08.html line 36), its <title> "
    "(line 6) and the L07 and L09 nav links (L07.html line 437, L09.html line 597) now read 'Principal Component Analysis and Level-like, "
    "Slope-like and Curvature-like Directions'. The title changed in commit c829fb1f and the hub was not updated (grep this round). "
    "No generator for the hub was found under tools/.",
    "In course/modules/M/M3/index.html line 155 replace 'Principal Component Analysis and the Yield-Curve Factors' with "
    "'Principal Component Analysis and Level-like, Slope-like and Curvature-like Directions'. The hub is outside the three lesson pages; "
    "its owning slice must make the edit, then re-run check_pages --unit M3.")

fragment = {
    "unit": "M3",
    "slice": "c",
    "round": 10,
    "verifier": "independent Haiku verifier (round 10), checkout verifyD10-M3-c",
    "pin": "47a36d8c78633793ccc762ae19dcd5e19b780d19",
    "base": "1e272e5a641f18412703b37778a44db6f7391a69",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD10-M3-c",
    "scratch": f"{SCRIPTS} and {OUT} in the checkout",
    "verified_at": "2026-11-05",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "FULL verification of L07, L08, L09, their three lab twins and the 71 slice cards at pin 47a36d8, with the delta from 1e272e5 "
        "read in full (out/delta_slice_c_r10.diff). Round 9 FAILs CONCEPT-L08-LSC, CARD-C127 and CARD-C167 are now PASS; "
        "CARDS-READ-L07-L09 is PASS after a full re-read. Two new FAILs: DEFINE-L08-OVERLINE (undefined \\overline{\\tau^2} in L08 "
        "Section 3, line 137) and HUB-L08-TITLE (stale L08 title on the hub card, index.html line 155, outside the three pages). "
        "Slice c has no project graders, so no mutation rows (mutants empty); project-level files belong to slice d. The path "
        "ledgers/M3/M3-c.json already held a round 18 fragment (pin 8f80909, an ancestor of HEAD); it is overwritten in this checkout as assigned."
    ),
    "summary": "M3 slice c round 10 at pin 47a36d8: 74 rows (pass=72 fail=2 unverifiable=0). Non-PASS: DEFINE-L08-OVERLINE (L08.html line 137, undefined \\overline{\\tau^2}), HUB-L08-TITLE (index.html line 155, stale L08 title).",
}

problems = ledger.validate(fragment, "M3-c")
Path("ledgers/M3/M3-c.json").write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", sum(r["status"] == "PASS" for r in rows), "fail", sum(r["status"] == "FAIL" for r in rows))
print("validate:", problems)
