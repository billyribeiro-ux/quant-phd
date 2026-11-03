"""Write the round-3 slice-c fragment (ledgers/M3/M3-c.json) from the rows the verifier checked.

Run: python -I ledgers/M3/scripts/M3-c-r3/build_fragment_r3.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
S = "ledgers/M3/scripts/M3-c-r3"

P = "PASS"
F = "FAIL"

rows = []


def row(rid, check, location, status, evidence, fix=""):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


# ---- gates (run by the verifier on pin a007712)
row("GATE-01", "gate", "tools/check_pages.py --unit M3", P, f"check_pages M3: PASS, exit 0 ({S}/check_pages_M3.log)")
row("GATE-02", "gate", "tools/check_dag.py --unit M3", P, f"check_dag M3: PASS, exit 0 ({S}/check_dag_M3.log)")
row("GATE-03", "gate", "tools/check_projects.py --unit M3", P,
    f"check_projects M3: PASS, exit 0 ({S}/check_projects_M3.log). Project content is slice d, not checked here")
row("GATE-04", "gate", "tools/run_labs.py --unit M3; --page L07, L08, L09", P,
    f"'run_labs M3: PASS (12/12)' ({S}/run_labs_M3_all.log); 'PASS (1/1)' for L07, L08, L09 ({S}/run_labs_L07.log, run_labs_L08.log, run_labs_L09.log); exit 0 each")
row("GATE-05", "gate", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py", P,
    f"each run alone as python -I -W error from an empty directory (/private/tmp/verifyD3-twin-07, -08, -09): exit 0, stderr 0 bytes ({S}/twin_L07.stdout, twin_L07.stderr, and the L08, L09 pair)")
row("GATE-06", "gate", "ruff check tests/labs/M3; ruff format --check tests/labs/M3", P,
    f"'All checks passed!' and '12 files already formatted' ({S}/ruff_check_twins.log, ruff_format_twins.log)")
row("GATE-07", "gate", "mypy --no-incremental (repository configuration)", P,
    f"'Success: no issues found in 331 source files', exit 0 ({S}/mypy.log)")
row("GATE-08", "gate", "tools/page_smoke.py --unit M3 --pages L07 L08 L09, and each page alone", P,
    f"'page_smoke M3: PASS' for the three pages ({S}/page_smoke_L07-L09.log) and for L07, L08, L09 alone ({S}/page_smoke_L07.log, page_smoke_L08.log, page_smoke_L09.log); lab timings 0.0, 0.0, 0.1 s")
row("GATE-09", "gate", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py", P,
    f"exit 0, no failures ({S}/pytest_relevant.log)")
row("GATE-10", "gate", "tools/verify_refs.py --offline", P,
    f"'offline integrity: 560 entries, 0 problems', exit 0 ({S}/verify_refs_offline.log). The live run needs the network and was not run; L07-L09 cite no registry key")
row("GATE-11", "gate", "tools/run_graders.py --unit M3 --seeds 0-49", P,
    f"'run_graders M3: PASS (reference 50/50 seeds, slowest 0.4 s)' ({S}/run_graders_M3.log). Project content is slice d")

# ---- lab twin and page embed
for n in ("07", "08", "09"):
    row(f"LAB-L{n}-EMBED", "2.5-labs", f"course/modules/M/M3/L{n}.html section#lab-M3-L{n}-1 vs tests/labs/M3/lab-M3-L{n}-1.py", P,
        f"check_embed_r3.py ({S}/check_embed_r3.py, log {S}/check_embed_r3.log): page code block equals the twin text (True), expected block equals the twin's stdout (True), no @@ markers")

# ---- numbers
row("NUM-L07", "2.2-numbers", "course/modules/M/M3/L07.html: Lab 1 outputs (0.8951, 1.3325, 0.8488, -0.4120, rank 2), M2 coefficients 7/6 and 1/2, fitted 7/6, 5/3, 13/6, residuals -1/6, 1/3, -1/6, 25 = 9 + 16, quiz 1.1667", P,
    f"own re-derivation: exact Fraction solve for M2 and numpy pinv for the lab design ({S}/independent_numbers_r3.py, log {S}/independent_numbers_r3.log); exercises checked in {S}/exercise_checks_r3.py (log exercise_checks_r3.log)")
row("NUM-L07-E2", "2.2-numbers", "course/modules/M/M3/L07.html line 299 (E2 solution): '(18.38, 3.10, -17.60)^T computed from the lab's seeded generator to two decimals; the lab does not print this vector'", F,
    f"The vector is not a lab output: the twin prints no A^T y (tests/labs/M3/lab-M3-L07-1.py; expected block lines 'P symmetric ...' to 'two coefficient vectors ...'), and the page does not show its derivation, so it fails rule 2.2 (a) and (c). The values are numerically correct: A^T y = (18.379697, 3.095863, -17.603498) ({S}/exercise_checks_r3.log)",
    "Either (a) add a print line to tests/labs/M3/lab-M3-L07-1.py that prints A^T y to two decimals, run tools/embed_labs.py course/modules/M/M3/L07.html --refresh lab-M3-L07-1, and cite that printed line in E2; or (b) delete the three numbers and the word 'approximately' from E2 and state only that A^T y is far from zero (its entries are far larger than 1e-9), so the check prints False. Then rerun the embed check and run_labs --page L07")
row("NUM-L08", "2.2-numbers", "course/modules/M/M3/L08.html: shares 75.9, 18.1, 5.2; cosines 0.9994, 0.9985, 0.9990; first share 0.7587 to 0.9791; E1 bound 0.9483 from M11 13.6818 and trace 88.2028; E3 sum 99.2", P,
    f"unrounded shares 75.872815, 18.088840, 5.161927 (top-3 sum 99.123581, so |99.2 - 99.1236| = 0.0764 <= 0.15); first share after x10 0.979145; bound 0.948346; printed-input reproduction 0.948346 ({S}/independent_numbers_r3.log); M1 to M3 and E1 to E3 arithmetic in {S}/exercise_checks_r3.log")
row("NUM-L09", "2.2-numbers", "course/modules/M/M3/L09.html: x^T C0 x = -2.4, ||C0-B||^2 = 0.64, R entries +-0.5, ||C0-R||_F = 0.9798, 23 of 40 non-PSD, 23 of 23 feasible and closer, distances 0.175527 and 0.163280, Example 3.6 values 0.04 and 0.08", P,
    f"independent re-implementation of clipping, rescaling and alternating projections reproduces 23/23/23 and the margins ({S}/independent_numbers_r3.log); Example 3.6 and E1 to E3 in {S}/exercise_checks_r3.log")

# ---- mathematics
row("MATH-L07", "2.4-mathematics", "course/modules/M/M3/L07.html Theorem 1.2 (a)-(c), Theorem 1.3, Remark 1.4, Theorem 2.2 (a)-(c), Definition 2.1, proofs, Section 3 claims, R1-R3", P,
    f"every proof read in full and re-derived: G invertible via x^T G x = ||Ax||^2 and the spectral theorem; A^T(y-p) = 0; P^T = P and P^2 = P; Pythagorean expansion; Q^2 = Q; cited Lesson 1 Theorem 3.7 (L01 text line 63) and Lesson 6 Fact 1.2 (L06 text line 21) checked in the earlier pages (textify.py, {S}/textify.py)")
row("MATH-L08", "2.4-mathematics", "course/modules/M/M3/L08.html Proposition 1.1, 1.2, Theorem 1.4, Theorem 2.1 (a)-(b), Corollary 2.2, Proposition 2.3, Remark 2.4, R1-R3, P1-P3", P,
    "every proof read and re-derived, including the Remark 2.4 perturbation argument (M_jj > 0 from x = e_j + t e_l), the R1 maximiser set, the R3 rank-three argument and the Theorem 2.1(b) bound; Definition 3.1 is handled by DEF-31-HYP")
row("MATH-L09", "2.4-mathematics", "course/modules/M/M3/L09.html Lemma 1.3, Propositions 3.2 to 3.5, Examples 2.3 and 3.6, Method 1 and Method 2 statements, R1-R3, P1-P3", P,
    "every proof read and re-derived: trace identity (Lemma 1.3); Prop 3.3(a) per-term difference; Prop 3.5 bracket (delta b_jj < |b_ij|); Prop 3.4 congruence; Example 3.6 A_0, R and distances checked numerically ({S}/exercise_checks_r3.log)")

# ---- problems and quizzes
row("PROB-L07", "2.9-structure", "course/modules/M/M3/L07.html problem set M1-M3, P1-P3, E1-E3, R1-R3; quiz", P,
    f"each worked solution re-derived; quiz data-answer values 1, 1.1667, 16, 0 match ({S}/exercise_checks_r3.log)")
row("PROB-L08", "2.9-structure", "course/modules/M/M3/L08.html problem set M1-M3, P1-P3, E1-E3, R1-R3; quiz", P,
    f"each worked solution re-derived; quiz data-answer values 0.6667, 17, 0.5 match ({S}/exercise_checks_r3.log)")
row("PROB-L09", "2.9-structure", "course/modules/M/M3/L09.html problem set M1-M3, P1-P3, E1-E3, R1-R3; quiz", P,
    f"each worked solution re-derived; quiz data-answer values -2.4, -0.2, 1, 0.04, 0.9798 match ({S}/exercise_checks_r3.log)")

# ---- lab statements and docstrings
row("LABSTMT-L07", "2.5-labs", "course/modules/M/M3/L07.html Lab 1 hypothesis, interpretation, key-results row; twin docstring", P,
    "hypothesis lists six checks at 1e-9, twelve observations, duplicated-column rank; each printed line exists in the twin (expected block); seed 7 and generator scales (0.8, -0.4, 0.3 noise) match the code")
row("LABSTMT-L08", "2.5-labs", "course/modules/M/M3/L08.html Lab 1 hypothesis, interpretation, key-results rows; twin docstring", P,
    "T = 750, six tenors 0.25 to 10, scales 8, 4, 2 bp and noise 0.5 bp, seed 8; every printed claim has a print line in main() and an expected line; 'the three matches are distinct' is len(set(matches)) == 3")
row("LABSTMT-L09", "2.5-labs", "course/modules/M/M3/L09.html Lab 1 hypothesis, interpretation, key-results rows; twin docstring", P,
    "seed 20261028, 40 matrices, 5x5, tolerances 1e-12 / 1e-8 / 1e-9, 500 steps, noise sd 0.35 before symmetrisation; the interpretation's 'to that tolerance' qualifier is present")
row("LABDOC-L09", "2.5-labs / 2.9-structure", "tests/labs/M3/lab-M3-L09-1.py line 17 (Scope paragraph), shown in course/modules/M/M3/L09.html line 210", F,
    f"The round-2 defect is fixed: the closer count now requires is_correlation(alt) (twin lines 125-128). The new sentence 'It shows that R is not the nearest correlation matrix to A in each instance where W passes is_correlation and is strictly closer' states an exact result, but is_correlation is tolerance-based (symmetry and unit diagonal to 1e-12; smallest eigenvalue at least -1e-8). I checked the exact claim numerically ({S}/independent_numbers_r3.log): the smallest eigenvalue of W is -8.9e-13 in those instances, the smallest margin d_R - d_W is 3.9e-5, and an exact repair (clip and rescale of W) is strictly closer than R in 23 of 23, so the sentence is true in substance; the lab itself does not compute that exact competitor, and the docstring drops the tolerance qualifier that the interpretation paragraph keeps ('to that tolerance')",
    "In tests/labs/M3/lab-M3-L09-1.py line 17 insert 'to the tolerances of is_correlation' into the Scope sentence (for example 'R is not the nearest correlation matrix to A, to the tolerances of is_correlation, in each instance where W passes ...'). Then run tools/embed_labs.py course/modules/M/M3/L09.html --refresh lab-M3-L09-1 (the expected output does not change), and rerun the embed check, run_labs --page L09 and the twin alone")

# ---- grades, citations, cross-references, notation, DAG, definitions, prose
row("GRADE-L07", "2.3-grades", "course/modules/M/M3/L07.html grade spans and key-results grades", P,
    "Theorems 1.2, 1.3, 2.2 and Remark 1.4 graded T with proofs on the page; the lab-only key-results row graded C with 'Lab 1 output'")
row("GRADE-L08", "2.3-grades", "course/modules/M/M3/L08.html grade spans and key-results grades", P,
    "Propositions 1.1, 1.2, 2.3, Theorems 1.4, 2.1 and Corollary 2.2 graded T with proofs; the simulation rows graded C and name Lab 1")
row("GRADE-L09", "2.3-grades", "course/modules/M/M3/L09.html grade spans and key-results grades", P,
    "Lemma 1.3, Propositions 3.2 to 3.5 and Examples 2.3 and 3.6 graded T; the seeded 23-of-40 and distance rows graded C with 'Lab 1 output' (one seeded run, floating point)")
row("CITE-L07-L09", "2.1-citations", "course/modules/M/M3/L07.html, L08.html, L09.html", P,
    f"grep -c 'data-cite|data-locator' = 0 on each page; section 8 says 'No result is attributed to an outside source'; no registry key used; the names Higham, Litterman, Eckart, Nelson, Gurkaynak, Axler and Strang do not occur (text dumps)")
row("XREF-EARLIER", "2.9-structure / DAG", "cross-lesson references in L07-L09: L01 Prop 1.4 and Thm 3.7; L03 Def 1.1; L04 F1-F4, Thm 2.3; L05 Def 1.4 and Thm 2.1; L06 Fact 1.2, Remark 2.5 and dot product/norm; L07 Thm 1.2 (used in L08)", P,
    f"each target read in the earlier page's text dump (textify.py, {S}/textify.py): L01 line 31 (subspace), L01 line 63 (Thm 3.7), L03 line 21 (Def 1.1), L04 lines 20-23 (F1-F4), L04 line 51 (Thm 2.3), L05 line 25 (Def 1.4), L05 line 40 (Thm 2.1), L06 line 21 (Fact 1.2), L06 Remark 2.5 (sign freedom)")
row("NOTATION-R", "2.4-notation", "L07, L08, L09 \\mathbb and \\R usage", P,
    f"grep 'mathbb' in the three pages: 0 matches; \\R used 13 times (L07) and 6 times (L08), 0 in L09; the registry macro \\R is in notation/notation.json ({S}/notation_scan_r3.log)")
row("NOTATION-OPNAME", "2.4-notation", "L07, L08, L09 \\tr and \\diag usage", P,
    f"\\tr and \\diag are the registered macros; L09 uses \\tr 11 times and \\diag 14 times; L07 and L08 use \\diag and \\tr ({S}/notation_scan_r3.log). One raw \\operatorname{{span}} remains in L08 (line 402): no registry macro exists for span, so it conforms. The round-2 failure is fixed")
row("NOTATION-T", "2.4-notation", "L08 section 1 (T x n matrix, T - 1, T = 750)", P,
    "notation.json symbol T: 'number of return observations (periods) in a sample' (S1); L08 uses T for the number of observations in a sample, the same meaning")
row("NOTATION-Q", "2.4-notation", "L07 and L09 orthogonal Q; L09 C^{\\ast}", P,
    "plain Q (orthogonal matrix) is not the registered \\mathbb{Q} (AP1 probability measure): different symbol, no collision (judgement). C^{\\ast} in L09 is not the registered R^\\ast; no registered symbol is reused")
row("NOTATION-OTHER", "2.4-notation", "all other symbols in L07-L09 (math spans: 430, 399, 499)", P,
    f"registered symbols R^\\ast, R^{{e\\ast}}, R_f, \\Phi, \\gamma_3, \\gamma_4 do not occur. Other letters are local to the lesson (judgement; scan in {S}/notation_scan_r3.log). In L08 section 3 'F' names a T x 3 factor matrix next to assumption labels F1-F4: local, not a registry collision")
row("DAG-LINKS", "2.9-structure / DAG", "dfn and concept links in L07-L09", P,
    "L07 defines orthogonal-projection and least-squares-projection and links vector-space to L01; L08 defines principal-component-analysis and level-slope-curvature and links eigendecomposition (L03), spectral-theorem (L04), positive-semidefinite-matrix (L05); L09 defines nearest-correlation-matrix and eigenvalue-clipping and links the same three earlier concepts. Each anchor exists (grep 'id=' in L01, L03, L04, L05)")
row("DAG-M4", "2.9-structure / DAG", "covariance, variance, expectation, estimator, portfolio names in L07-L09", P,
    "no M4 or other out-of-closure concept is named or linked in the lesson text. The only 'Covariance-matrix' string is the next-lesson nav link to the project title (curriculum/01-foundations.yaml:182), not a concept link. 'correlation matrix' is the M3 Definition 1.1 in plain prose (architect ruling B1/Q2); 'floating point' is plain (B4)")
row("DEFINE-OTHER", "2.9-structure", "first uses of subspace, column space, normal equations, fitted vector, residual, tenor, cosine, trace, explained share, congruence, Frobenius norm, positive definite, orthonormal, null space", P,
    "each defined before its first use on the page or in an earlier lesson (L01 Prop 1.4, L04 F4, L05 Def 1.4, L06 Def 1.1 and Fact 1.2; in-page Definitions and inline definitions). 'normal equations' is named with its formula on first use")
row("DEF-LOADING", "2.9-structure", "course/modules/M/M3/L08.html line 141 (Definition 3.1: 'A loading vector v is level-like ...') and line 505 (quiz stem 'A loading vector is called level-like when...')", F,
    "'loading vector' is first used in Definition 3.1 and is never defined on the page; Definition 1.3 defines principal directions (the columns of V). Rule 1.1.5 requires a term to be defined before its first use",
    "In Definition 3.1 write 'A principal direction v (a column of V, Definition 1.3) is level-like, slope-like or curvature-like when ...', and change the quiz stem to 'A principal direction is called level-like when...'")
row("DEF-31-HYP", "2.4-mathematics / 2.9-structure", "course/modules/M/M3/L08.html line 141 (Section 3 lead-in and Definition 3.1: 'let the three shapes above be normalized to norm 1 ... orthonormal by construction')", F,
    "The three shapes are nonzero and orthonormal only if there are at least three distinct tenors. With two tenors the centred squared tenors lie in span{iota, tau - tau-bar iota}, the third shape is zero, and it cannot be normalized. The page states no such hypothesis (the text is for general n; the lab uses six tenors)",
    "Add the hypothesis 'the tenors are distinct and n >= 3' before 'Three shapes over the tenors' or in Definition 3.1 (for example 'Assuming F1 to F4 of Lesson 4 and at least three distinct tenors, ...')")
row("TERM-KERNEL-L09", "2.9-structure", "course/modules/M/M3/L09.html line 134 (Proposition 3.2(b) proof: 'so the kernel is trivial') and line 422 (P2 solution: 'a square matrix whose kernel is trivial')", F,
    "'kernel' is not defined in the course (the course's term is the null space, Lesson 4 F4) and is first used here without definition (rule 1.1.5)",
    "Replace with 'Mx = 0 has only the solution x = 0' (the F1 wording), which needs no new term")
row("TERM-KERNEL-L07", "2.9-structure", "course/modules/M/M3/L07.html line 281 (P3 solution: 'a nonzero vector in the kernel of A^T A')", F,
    "'kernel' is used without definition (the course's term is the null space, Lesson 4 F4)",
    "Replace with 'a nonzero gamma with A^T A gamma = 0'")
row("PROSE-PROCESS", "2.9-structure", "learner text of L07-L09", P,
    "grep for builder, verifier, ledger, round, pin, agent, TODO, TBD, lorem, 'for brevity', 'beyond the scope', 'left as an exercise', 'it is important to note', 'studies show', 'experts agree', 'obviously', 'clearly' on the text dumps: no learner-text hits (only 'rounded' and 'unrounded' substrings)")
row("PROSE-ELLIPSIS", "2.9-structure", "quiz stems ending in an ellipsis (L07, L08, L09)", P,
    "each ellipsis ends a quiz stem whose options follow; it stands for the answer, not for omitted content (judgement)")
row("PROSE-SCOPE", "2.9-structure", "scope words (every, all, always, any, same, only, exactly, stable, robust, typically) in L07-L09", P,
    "each use is backed by a proof or a finite check in the same passage: 'every full-column-rank design' (Thm 1.2); 'every nonzero c' (Prop 2.3); 'only when lambda1 is simple' (Thm 2.1(a) equality case and R1); 'the 40 seeded matrices' (Lab 1)")
row("PROSE-FOOTER", "2.9-structure", "course/modules/M/M3/L07.html line 438, L08.html line 529, L09.html line 604 (footer: 'Every claim carries an evidence grade and a registry citation.'), generated by course/templates/lesson.html line 147", F,
    "On these pages no claim carries a registry citation: no data-cite or data-locator, no registry key, and section 8 says 'No result is attributed to an outside source'. The footer is template text used on 30 lesson pages, so the defect is in the template, outside this slice",
    "Template owner: change course/templates/lesson.html line 147 to a statement that is true of every page (for example 'Every claim carries an evidence grade and a source: a theorem, a lab output, or a registry citation where one is given'), or make the footer per page. Builders cannot fix this inside slice c")
row("STRUCT-WHY", "2.9-structure", "why-it-matters paragraphs (L07 line 52, L08 line 52, L09 line 52)", P,
    "word counts 108, 109 and 116, all at or under the 120-word limit (BUILDER 4.2.1), counted from the text dumps")
row("STRUCT-ORDER", "2.9-structure", "section order of L07, L08, L09", P,
    "why-it-matters, core sections, inline lab, canon-breaks, misconceptions (3 each), problem set (Mechanics, Proof, Empirical, Research: 3 problems each), key results, quiz, references (section ids checked by grep)")
row("HOURS", "2.9-structure / hours", "data-hours on L07 (11), L08 (12), L09 (12); hub data-hours-lessons 105", P,
    "lesson hours L01 to L09 sum to 12+11+12+12+12+11+11+12+12 = 105, equal to course/modules/M/M3/index.html data-hours-lessons=\"105\" (grep). The plan table lists L01 at 11 h and the page says 12 h; the sum still matches (slice a). Slice c hours match the plan")
row("DATA-CLAIM", "2.8-data", "course/modules/M/M3/L08.html section 4: 'The program does not yet embed a multi-tenor series from which three or more tenors can be read'", P,
    "course/assets/data/market/MANIFEST.json: fx_daily (AUD, CAD, CHF, EUR, GBP, JPY), fx_monthly (10 currencies), ust_daily (tbill_3m, cmt_10y). No embedded series has three or more tenors; the claim holds")
row("HONEST-GAP", "2.5-labs", "course/modules/M/M3/L08.html section 4 (Treasury lab not run; SIMULATED panel used)", P,
    "the page states the curriculum's Treasury lab is not run and a SIMULATED six-tenor panel is used, consistent with architect decision B2/Q1 in plans/M3-build-plan.md")
row("SIMULATED-LABELS", "2.5-labs", "labs and key-results rows of L07-L09", P,
    "each lab hypothesis, docstring and key-results row that uses generated data says SIMULATED; no lab has a data-files attribute")
row("LAB-RUNTIME-SEEDS", "2.5-labs", "labs L07, L08, L09", P,
    f"seeds 7, 8 and 20261028 fixed in the twins; numpy only; no network; page_smoke lab timings 0.0, 0.0 and 0.1 s ({S}/page_smoke_L07-L09.log)")
row("FIGURES", "2.8-data", "L07-L09 (no SVG figures: grep '<svg' count 0)", P,
    "no charts or interactive figures on these pages; the figure rows do not apply")

mutants = []
n_pass = sum(1 for r in rows if r["status"] == P)
n_fail = sum(1 for r in rows if r["status"] == F)
verdict = "PASS" if n_fail == 0 and n_pass == len(rows) else "FAIL"

fragment = {
    "unit": "M3",
    "slice": "c",
    "round": 3,
    "verifier": "independent Haiku verifier, checkout verifyD3-M3-c",
    "pin": "a007712fdbfc8b4851123f4de76b5310ac5a9e64",
    "base": "c737272f5bdef4a027417989cd52254555e8a0bb",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD3-M3-c",
    "scratch": "/private/tmp (verifyD3-L07.txt, verifyD3-L08.txt, verifyD3-L09.txt text dumps; verifyD3-twin-07..09 empty directories)",
    "verified_at": "2026-11-03T03:45:00Z",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice c: course/modules/M/M3/L07.html, L08.html, L09.html and tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, "
        "lab-M3-L09-1.py. Delta since the round-2 pin c737272f: L07 (why-it-matters, proof, misconception: \\diag and '(defined in Lesson 1)'), "
        "L08 (\\tr, \\diag, and the Definition 1.3, 2.4 and Section 3 text), L09 (Lab 1 closer count, docstring, prose, quiz), "
        "and tests/labs/M3/lab-M3-L09-1.py. Lab twins L07 and L08 are byte-identical since c737272f. No round-2 PASS row was carried: "
        "every row was re-verified in this round. Mutation testing does not apply to lab twins (VERIFIER ruling: demonstrations), so no mutants are listed. "
        "The round-2 fragment's LABDOC-L09 is now narrower (the counting defect is fixed; the tolerance qualifier remains). "
        "NOTATION-OPNAME is fixed. Cards for L07-L09 and the project are slice d and were not checked here."
    ),
    "summary": (
        f"Slice c (L07-L09 and lab twins), round 3: {len(rows)} rows, {n_pass} PASS, {n_fail} FAIL, 0 UNVERIFIABLE. "
        "All gates pass (check_pages, check_dag, check_projects, run_labs 12/12 and per page, twins alone under -I -W error, "
        "embed comparison, ruff, mypy, page_smoke together and alone, relevant pytest, verify_refs offline, run_graders). "
        "Non-PASS: NUM-L07-E2 (unsourced vector), LABDOC-L09 (tolerance qualifier in docstring), DEF-LOADING (undefined term 'loading vector'), "
        "DEF-31-HYP (Definition 3.1 needs at least three distinct tenors), TERM-KERNEL-L07 and TERM-KERNEL-L09 (undefined term 'kernel'), "
        "PROSE-FOOTER (template footer claims a registry citation on every claim)."
    ),
}

out = ROOT / "ledgers" / "M3" / "M3-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "pass", n_pass, "fail", n_fail, "verdict", verdict)
