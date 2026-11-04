"""Builds the round-6 fragment ledgers/M3/M3-c.json (slice c: L07-L09 and their lab twins).

Carried rows copy the round-5 evidence verbatim with the carry prefix; they are used only for L07 subjects
(course/modules/M/M3/L07.html, tests/labs/M3/lab-M3-L07-1.py) that are byte-identical between the round-5 pin
440ed3c8 and the round-6 pin 142ecfc2 (git diff --quiet 440ed3c8 142ecfc2 -- <files>).
Every other row was re-derived this round; the logs cited are in ledgers/M3/scripts/M3-c-r6/.
Run from the checkout root: .venv/bin/python ledgers/M3/scripts/M3-c-r6/build_fragment_r6.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path.cwd()
PREV = json.loads(Path("/Users/billyribeiro/.fanout/frags/D-M3-c.round5.json").read_text(encoding="utf-8"))
PREV_ROWS = {r["id"]: r for r in PREV["rows"]}
S = "ledgers/M3/scripts/M3-c-r6/"
L07_FILES = "course/modules/M/M3/L07.html and tests/labs/M3/lab-M3-L07-1.py"
CARRY = "Carried from round 5 ({files} byte-identical since the previous pin 440ed3c8): "

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or ""
    rows.append(r)


def carry(rid: str, new_id: str | None = None) -> None:
    src = PREV_ROWS[rid]
    assert src["status"] == "PASS", rid
    rows.append(
        {
            "id": new_id or rid,
            "check": src["check"],
            "location": src["location"],
            "status": "PASS",
            "evidence": CARRY.format(files=L07_FILES) + src["evidence"],
        }
    )


# ---- gates, run this round on the pin (logs in S) ----
row("GATE-01", "2.9-gate", "tools/check_pages.py --unit M3 and --page L07, L08, L09; --all", "PASS",
    f"'check_pages M3: PASS' EXIT=0 ({S}check_pages_M3.log); 'check_pages M3 L07|L08|L09: PASS' EXIT=0 "
    f"({S}check_pages_L07.log, _L08.log, _L09.log); check_pages.py --all EXIT=0 ({S}check_pages_all_M3.log).")
row("GATE-02", "2.9-gate", "tools/check_dag.py --unit M3", "PASS",
    f"'check_dag M3: PASS' EXIT=0 ({S}check_dag_M3.log).")
row("GATE-03", "2.6-gate", "tools/check_projects.py --unit M3", "PASS",
    f"'check_projects M3: PASS' EXIT=0 ({S}check_projects_M3.log). Project content is another slice.")
row("GATE-04", "2.5-labs", "tools/run_labs.py --unit M3 and --page L07, L08, L09", "PASS",
    f"'run_labs M3: PASS (12/12)' EXIT=0 ({S}run_labs_M3.log); (1/1) PASS for L07, L08, L09 "
    f"({S}run_labs_L07.log, _L08.log, _L09.log).")
row("GATE-05", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py run alone", "PASS",
    f"{S}m3c_r6_twin_vs_page.py runs each twin as python -I -W error from a fresh tempfile directory: L07, L08, L09 "
    f"each exit=0 stderr_bytes=0 (log {S}m3c_r6_twin_vs_page.log).")
row("GATE-06", "2.5-labs", "ruff check and ruff format --check tests/labs/M3", "PASS",
    f"'All checks passed!' EXIT=0 ({S}ruff_check.log); '12 files already formatted' EXIT=0 ({S}ruff_format.log).")
row("GATE-07", "2.5-labs", "mypy --no-incremental (repository configuration)", "PASS",
    f"'Success: no issues found in 331 source files' EXIT=0 ({S}mypy.log).")
row("GATE-08", "2.9-smoke", "tools/page_smoke.py --unit M3 --page L07, then L08, then L09 (each alone)", "PASS",
    f"'page_smoke M3: PASS' EXIT=0 for each page ({S}page_smoke_L07.log, _L08.log, _L09.log); lab timings 0.0 s "
    "(runtime boot 1.1 s with numpy).")
row("GATE-09", "2.1-citations", "tools/verify_refs.py --offline", "PASS",
    f"'offline integrity: 560 entries, 0 problems' EXIT=0 ({S}verify_refs_offline.log). references/ is "
    "byte-identical between the two pins (git diff --quiet 440ed3c8 142ecfc2 -- references/references.json); no live run.")
row("GATE-10", "2.5-labs", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k 'M3 or run_labs or page'",
    "PASS", f"EXIT=0, all selected tests passed ({S}pytest_slice.log). Full suite not run.")
row("GATE-11", "2.6-gate", "tools/run_graders.py --unit M3 --seeds 0-49", "PASS",
    f"'run_graders M3: PASS (reference 50/50 seeds, slowest 0.3 s)' EXIT=0 ({S}run_graders_M3.log). Grader content is "
    "another slice; mutation testing is not part of this slice (lab twins are demonstrations).")

# ---- lab embed and statements ----
row("LAB-L07-EMBED", "2.5-labs", "course/modules/M/M3/L07.html section#lab-M3-L07-1 vs tests/labs/M3/lab-M3-L07-1.py",
    "PASS", f"Fresh this round: {S}m3c_r6_twin_vs_page.py: page_code_equals_twin=True, expected_equals_stdout=True, "
    f"twin stdout 11 lines (log {S}m3c_r6_twin_vs_page.log).")
row("LAB-L08-EMBED", "2.5-labs", "course/modules/M/M3/L08.html section#lab-M3-L08-1 vs tests/labs/M3/lab-M3-L08-1.py",
    "PASS", f"Fresh this round: page_code_equals_twin=True, expected_equals_stdout=True, stdout 14 lines "
    f"({S}m3c_r6_twin_vs_page.log). The page changed this round (lines 52, 122, 384, 430/432) but not the lab section (lines 144-285).")
row("LAB-L09-EMBED", "2.5-labs", "course/modules/M/M3/L09.html section#lab-M3-L09-1 vs tests/labs/M3/lab-M3-L09-1.py",
    "PASS", f"Fresh this round: page_code_equals_twin=True, expected_equals_stdout=True, stdout 13 lines "
    f"({S}m3c_r6_twin_vs_page.log).")
carry("LABSTMT-L07")
row("LABSTMT-L08", "2.5-labs",
    "L08.html Lab 1 hypothesis (line 146), code (147-269), output (270-283), interpretation (284); twin lines 147-269",
    "PASS",
    "Re-read this round. Hypothesis: M PSD, MV=V Lambda, Z^T Z/(T-1)=Lambda, trace identity to 1e-9 (code lines 221-229 print "
    "these with TOL=1e-9); shares from unrounded eigenvalues (line 231-235); argmax matching with distinctness check (lines "
    "240-246); doubling check (248-253); column-ten rescale and E1 bound (254-266). Output lines 271-283 agree; all 'True' "
    "lines match. Interpretation (284) matches output. Runner-up |cos| 0.032, 0.040, 0.040 vs maxima 0.9994/0.9985/0.9990 "
    f"({S}m3c_r6_numbers.log), so the argmax match is the Definition 3.1 match.")
row("LABSTMT-L09", "2.5-labs",
    "L09.html Lab 1 hypothesis (line 193), code (194-335), output (336-348), interpretation (349), key rows (499-500)",
    "PASS",
    "Re-read this round. Hypothesis counts (40 seeded 5x5 matrices; W passes is_correlation to 1e-12 and eigenvalue -1e-8; "
    "strict closeness) match twin lines 79-89, 117-138; output 23 / 23 / 23 and index-0 distances 0.175527 and 0.163280 "
    f"reproduced independently by {S}m3c_r6_numbers.py (log {S}m3c_r6_numbers.log). Witness -2.4 and eigenvalues "
    "-0.8, 1.9, 1.9 reproduced from the characteristic polynomial.")
row("LABDOC-L09", "2.5-labs", "tests/labs/M3/lab-M3-L09-1.py lines 1-21 (docstring) against lines 36, 79-89, 117-138",
    "PASS", "Docstring claims 1-4 match SEED=20261028 (line 36), N_MATRICES=40 (34), SIZE=5 (35), the generator "
    "(0.5 + symmetrised N(0,0.35) noise, diagonal set to 1, lines 79-89) and the clip / alternating-projection / counting "
    "logic (lines 113-138). Unchanged in this round's delta.")
row("LABDOC-L09-TOL", "2.5-labs",
    "tests/labs/M3/lab-M3-L09-1.py lines 16-19 against L09.html line 349 and twin lines 71-76 (is_correlation)", "PASS",
    "Docstring says 'to the tolerance of is_correlation'; is_correlation (lines 71-76) uses TOL=1e-12 for symmetry and "
    "unit diagonal and -FEASIBLE_TOL=-1e-8 for the smallest eigenvalue; page line 349 says 'to that tolerance'. True.")
row("LABSTMT-L09-RUNTIME", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py (imports, seeds, runtime)",
    "PASS", "Imports are numpy and __future__ only (L07 twin lines 17-19; L08 twin lines 16-18; L09 twin lines 23-26). Seeds: default_rng(7) "
    "(L07 twin line 25), default_rng(8) (L08 page line 213), SEED 20261028 (L09 twin line 36). No file or network access. page_smoke lab timings "
    "0.0 s each; each twin ends with a bare main() call (last line of each twin file).")

# ---- numbers ----
carry("NUM-L07")
carry("NUM-L07-M")
row("NUM-L08", "2.2-numbers",
    "L08.html line 284 (shares 75.9/18.1/5.2; cosines 0.9994/0.9985/0.9990), lines 290-291 (0.7587 to 0.9791), E1 (377: bound 0.9483, inputs 13.6818 and 88.2028), E3 (391: sum 99.2, bound 0.15), key rows 433-434",
    "PASS",
    f"Recomputed by SVD of the centred panel, not eigh ({S}m3c_r6_numbers.py, log {S}m3c_r6_numbers.log): unrounded shares "
    "75.872815, 18.088840, 5.161927 -> 75.9, 18.1, 5.2; |cos| 0.999381, 0.998544, 0.999019 -> 0.9994, 0.9985, 0.9990; first "
    "share 0.758728 -> 0.7587 and after column-ten rescale 0.979145 -> 0.9791; E1 bound 100 M11/(trace+99 M11) = 0.948346 -> "
    "0.9483 from unrounded values and from printed inputs 13.6818, 88.2028; printed one-decimal sum 99.2, unrounded sum "
    "99.123581, difference 0.0764 <= 0.15, max single rounding error 0.038 <= 0.05. Doubling and c=-3 shares unchanged to 1e-9.")
row("NUM-L09", "2.2-numbers",
    "L09.html why-it-matters (line 52: 40 inputs, 23 non-PSD), Lab 1 interpretation (349), Example 2.3 (line 107), Example 3.6 (line 179-180), E2 (447: 0.9798), key rows 498-500, R entries (output 342-344)",
    "PASS",
    f"Recomputed in {S}m3c_r6_numbers.log: C0 eigenvalues -0.8, 1.9, 1.9 (characteristic polynomial); x^T C0 x = -2.4; "
    "||C0-B||_F^2 = 0.64 = sum of squared negative eigenvalues; R entries 0.5, 0.5, -0.5 with unit diagonal; "
    "||C0-R||_F = 0.9797958971 -> 0.9798; non-PSD count 23 of 40 (17 PSD), largest min-eigenvalue among non-PSD -7.81e-4 "
    "(below -1e-9 and -1e-8 alike: counts 23 and 23); 23 of 23 alternating-projection outputs pass, 23 of 23 strictly closer; "
    "index-0 distances 0.175527 and 0.163280; Example 3.6 ||A-A0||^2 = 0.04, ||A-R||^2 = 0.08.")

# ---- mathematics ----
row("MATH-L08", "2.4-mathematics",
    "L08.html Proposition 1.1 (61-62), Proposition 1.2 (71-72), Definition 1.3 (82), Theorem 1.4 (86-87), Theorem 2.1 (100-104), proof (110-112), Corollary 2.2 (116-117), Proposition 2.3 (121-122), proof (125-127), Remark 2.4 (131-132); problems M1-M3 (324-342), P1-P3 (349-366), E1-E3 (374-391), R1-R3 (399-416)",
    "PASS",
    "Re-derived this round, every proof read in full: M symmetric and PSD (Prop 1.1); trace identity (1.2); scores Z^TZ=(T-1)Lambda and shares sum to 1 when the eigenvalue sum is positive (1.4); "
    "Rayleigh bound with equality case (2.1a) and k-th maximum (2.1b, uses alpha_i = v_i^T u = 0 for i<k); corollary 2.2; "
    "Prop 2.3 with the hypothesis sum_j lambda_j > 0 that the proof needs for the share formula (see PROP23-HYP); Remark 2.4 "
    "(M_jj > 0 by the e_j + t e_l argument; kappa = c forced by M_jl != 0; c^2 != c). Worked numbers: M1 trace 17, det 3, eigenvalues (17 +- sqrt 277)/2 "
    f"(verified in {S}m3c_r6_numbers.log); M2 shares 2/3, 1/6, 1/6; M3 eigenvalues 18, 9; P1-P3; R1 tie; R2; R3 BGB^T and eigenbasis BQ re-derived. "
    "Remark 2.4's last sentence is clear enough in context (see PROSE-REMARK-2.4).")
row("PROP23-HYP", "2.4-mathematics", "L08.html Proposition 2.3 (line 122), proof (127), E2 solution (384), key row 432 (line 432)", "PASS",
    "The hunk adds the hypothesis sum_j lambda_j > 0 'so that the shares of Definition 1.3 are defined'. Definition 1.3 (line 82) defines shares exactly when that sum is positive, and the proof's formula lambda_k/sum_j lambda_j needs it. "
    "E2 (384) and row 432 state the same condition. The added hypothesis is consistent with the statement and with the proof.")
row("KEY-L08-430", "2.4-mathematics",
    "course/modules/M/M3/L08.html key-results row line 430, against Theorem 1.4 (line 87)", "FAIL",
    "Theorem 1.4 (line 87) reads 'The shares sum to 1 whenever sum_j lambda_j > 0.' Key row 430 reads 'Assuming F1 to F4 of Lesson 4, the scores satisfy Z^T Z/(T-1) = Lambda, and the shares sum to 1' with no condition. "
    "When the eigenvalue sum is 0 the shares are 0/0 and the row's claim is not defined, so the summary drops the hypothesis the theorem lists. "
    "The same edit added this condition to the sibling row 432 but not to row 430, so the table is internally inconsistent.",
    "In course/modules/M/M3/L08.html line 430, change the final clause to 'and the shares sum to 1 whenever the eigenvalue sum is positive' "
    "(keep the T grade and the Theorem 1.4 source). Then re-run check_pages.py --page L08 and check_dag.py --unit M3.")
row("MATH-L09", "2.4-mathematics",
    "L09.html Definition 1.1 (60), Definition 1.2 (65), Lemma 1.3 (74-75; proof 78-84), Definition 2.1 (93), Definition 3.1 (116-118), Propositions 3.2 (122-126; proof 130-134), 3.3 (138-141; proof 146-147), 3.4 (151-152; proof 157-159), 3.5 (163-164; proof 169-173), Examples 2.3 (104-107) and 3.6 (178-180); problems M1-M3 (388-406), P1-P3 (413-429), E1-E3 (438-456), R1-R3 (463-479)",
    "PASS",
    "Re-derived this round: Lemma 1.3 trace-cyclic argument; Prop 3.2 PSD and invertibility (eigenvalues max(lambda, eps)); Prop 3.3(a) squared distance = sum over lambda_i < eps; Prop 3.4 congruence (D^{-1/2} symmetric); "
    "Prop 3.5 off-diagonal argument (uses symmetry and PSD, both listed); Example 3.6 values (eigenvalues 2.2 and -0.2, A0 = 1.1 J, R = J, distances 0.04 and 0.08) reproduced in "
    f"{S}m3c_r6_numbers.log. Problems: M1 eigenvalues 1.6, 0.4; M2 4.88; M3 eigenvalues of B (13 +- sqrt 41)/2 and C entries 1, 1, 1/3; P1 |C_ij| <= 1; P2; P3 convexity; E1 -2.4 term by term; E2 0.9798; E3 0.5; R1 split of the squared norm; R2 diag(1,1); R3 norm >= n. "
    "No hypothesis is missing from the stated results.")

# ---- problem sets ----
carry("MATH-L07")
row("PROB-L08", "2.2-problems", "L08.html problem set M1-M3, P1-P3, E1-E3, R1-R3 (lines 324-416)", "PASS",
    "Three problems per tier, each with a worked solution; every solution re-checked this round (see MATH-L08). E1 bound 0.9483 and E3 sum 99.2 re-derived.")
row("PROB-L09", "2.2-problems", "L09.html problem set M1-M3, P1-P3, E1-E3, R1-R3 (lines 387-479)", "PASS",
    "Three problems per tier, each with a worked solution; every solution re-checked this round (see MATH-L09).")
carry("PROB-L07")

# ---- grades ----
carry("GRADE-L07")
row("GRADE-L08", "2.3-grades", "L08.html grade spans (61, 71, 86, 100, 116, 121) and key-results table (428-434)", "PASS",
    "Proved results (Props 1.1, 1.2, 2.3, Thm 1.4, 2.1, Cor 2.2) are T with proofs on the page; row 432 is T and states the Prop 2.3 condition; rows 433-434 are C and name Lab 1 with the single-panel caveat. "
    "Definition 3.1 claims no grade and cites no source. Row 430 is T but drops a hypothesis: see KEY-L08-430.")
row("GRADE-L09", "2.3-grades", "L09.html grade spans (74, 122, 151, 163) and key-results table (491-500)", "PASS",
    "Proved results and worked examples are T; rows 499-500 are C and name Lab 1 with the seeded finite check.")

# ---- citations and cross-references ----
row("CITE-L07-L09", "2.1-citations", "L07.html, L08.html, L09.html (data-cite, data-locator; references sections)", "PASS",
    "grep -c 'data-cite|data-locator' returns 0 for each of L07, L08, L09 this round. L08 references (line 518) and L09 references (data-references, line 594) state or contain no outside source. Nothing is attributed, so no registry key is checked.")
row("XREF-EARLIER", "2.4-mathematics", "L07, L08, L09 cross-references to earlier lessons", "PASS",
    "Re-grepped this round: L08 line 82 'Theorem 2.3 of that lesson' = L04.html line 130 (Theorem 2.3, spectral theorem); L08 line 137 'Lesson 7, Theorem 1.2' = L07.html line 64; "
    "L08 line 293 'Lesson 6 notes the same sign freedom' = L06.html line 229 (sign flip of u_i and v_i); L09 line 112 'Lesson 4, Theorem 2.3' = L04.html line 130; L09 line 112 'Lesson 3' eigenvalues and eigenvectors = L03.html line 109; "
    "L07 line 75 'Fact 1.2 of Lesson 6' = L06.html line 64; L07 line 320 'Theorem 3.7 of Lesson 1' = L01.html line 161; L09 M1 'Lesson 5, Theorem 2.1' = L05.html line 108 (PSD iff eigenvalues nonnegative). L01, L03, L04, L05, L06 are byte-identical to the round-5 pin.")
row("DAG-PSD-REDEF", "2.9-structure",
    "course/modules/M/M3/L09.html line 56 (Section 1 sentence on positive semidefinite) versus L05.html line 72 (dfn def-positive-semidefinite-matrix)",
    "PASS",
    "Round-5 FAIL is fixed. L09.html line 56 now reads 'a symmetric C is positive semidefinite (Lesson 5)' with the concept link to L05.html#def-positive-semidefinite-matrix; the defining clause x^T C x >= 0 is gone. "
    "No other sentence in L07-L09 restates the definition as a definition (L09 line 60 names PSD as a property of Definition 1.1; L08 Prop 1.1 is a result with a proof).")

# ---- notation ----
row("NOTATION-R", "2.4-notation", "L07, L08, L09 math using \\R", "PASS",
    "\\R is registered (notation/notation.json macros: 'real numbers'); used only for real vector and matrix spaces (macro inventory of the three pages, this round).")
row("NOTATION-OPNAME", "2.4-notation", "L08 line 402 (\\operatorname{span}); L09 line 171 (\\mathrm{sign}); \\tr and \\diag (L08, L09)", "PASS",
    "\\tr and \\diag are registered (macros 'matrix trace' and 'diagonal matrix'). \\operatorname and \\mathrm are standard KaTeX, not registered symbols.")
row("NOTATION-T", "2.4-notation", "L08.html Section 1 (T x n matrix, T >= 2, T = 750 in the lab)", "PASS",
    "Registry symbol T: 'number of return observations (periods) in a sample'. In L08 T counts the rows (observations) of the panel, consistent with that meaning.")
row("NOTATION-AST", "2.4-notation", "L09.html line 93 (C^{\\ast}, nearest correlation matrix)", "PASS",
    "Registry registers R^\\ast (SDF payoff return, AP1), a different symbol; C^{\\ast} is not a registered symbol and does not collide.")
row("NOTATION-Q", "2.4-notation", "L07.html and L09.html (orthogonal Q)", "PASS",
    "Q denotes an orthogonal matrix (Q^TQ = I); no registered symbol Q exists (the registered \\mathbb{Q} is a probability measure, not used here).")
row("NOTATION-OTHER", "2.4-notation", "all control sequences in the three pages' math (macro counts re-taken this round)", "PASS",
    "Greek letters used locally: \\gamma (L07 coefficient vector; the registered symbols are the subscripted \\gamma_3 and \\gamma_4, so no collision), \\beta, \\hat, \\kappa (L08 scalar), \\tau and \\iota (tenors and ones vector, written \\boldsymbol{\\iota}), \\Gamma, \\Lambda, \\varepsilon, \\delta. The registry allows local letters. \\ast only as C^{\\ast} (see NOTATION-AST).")

# ---- definitions and DAG ----
row("DEF-L08-CLOSE", "2.9-structure", "L08.html Definition 3.1 (line 141), quiz item L08q9 (line 507) and explanation (line 511)", "PASS",
    "Re-read this round. Definition 3.1 gives the unique-maximum rule; the quiz asks for 'the one principal direction with the largest absolute cosine'; the explanation states the tie case gives no label.")
row("DEF-L08-MATCH", "2.9-structure", "L08.html Definition 3.1 (line 141); canon-break (line 292); quiz explanation (line 511)", "PASS",
    "Re-read this round. A match requires exactly one principal direction to attain the largest |cos|; ties give no match. Lab 1 matches by argmax on a panel with runner-up |cos| 0.032, 0.040, 0.040 (log "
    f"{S}m3c_r6_numbers.log), so no tie occurs in the printed run.")
row("DAG-LINKS", "2.9-structure", "L07.html, L08.html, L09.html meta rows (lines 38-39)", "PASS",
    f"check_dag M3: PASS ({S}check_dag_M3.log). Targets vector-space (L01), eigendecomposition (L03), spectral-theorem (L04), positive-semidefinite-matrix (L05) are defined earlier. Self-links are the lesson's own dfn ids.")
row("DAG-M4", "2.9-structure", "L07, L08, L09 (covariance, variance, correlation wording)", "PASS",
    "grep over the three pages: no 'covariance', 'variance' or 'expectation' word; 'correlation' appears only as the lesson's own defined term 'correlation matrix' (L09 Definition 1.1, plain descriptor, no link to the M4 concept), the permitted use under architect decision B1/Q2.")
row("DAG-PROSE-UNLINKED", "2.9-structure", "L09.html line 60 and other unlinked uses of 'positive semidefinite'", "PASS",
    "check_dag PASS; no concept used before its lesson. BUILDER_RULES 4.1 would link every use of an earlier concept; the unlinked prose uses are noted for the builder and are not a verifier failure under 2.9.")
row("PLAIN-REDEF", "2.9-structure", "L09.html line 56 and L08.html line 58 (trace); L09.html Definition 1.2a (orthogonal matrix)", "PASS",
    "Plain terms, not registered concepts. Each restatement is equivalent to the earlier definition. Redundancy only.")
row("DEFINE-BEFORE-USE", "2.9-structure", "first uses of tenor, trace, cosine, PSD, eigenvalue clipping, orthogonal, and roadmap terms in why-it-matters (L07 line 52, L08 line 52, L09 line 52)",
    "PASS",
    "Body definitions precede use (tenor and trace L08 56-58; cosine L08 137; PSD via Lesson 5 in L09 line 56; orthogonal L09 line 69 before Lemma 1.3). The why-it-matters paragraphs name later definitions explicitly ('Definition 1.3 of this lesson' in L08 line 52, now with a PCA pointer; 'Definitions 1.2 and 2.1' and 'Method 1, Section 4' in L09 line 52), a roadmap rather than a use before definition.")

# ---- prose ----
row("PROSE-PROCESS", "2.9-structure", "L07, L08, L09 learner text", "PASS",
    "Scan for builder, verifier, architect, ledger, planner, open item, DAG, round: no hits in learner text.")
row("PROSE-ELLIPSIS", "2.9-structure", "quiz stems ending in an ellipsis: L08 lines 445, 459; L09 lines 530, 539 (L08 line 505 'when...' has no ellipsis)", "PASS",
    "Each is a completion stem ('... is' or 'equal to') whose options supply the missing words; not an omitted-content ellipsis.")
row("PROSE-SCOPE", "2.2-scope", "scope words in the changed and unchanged text of L08 and L09", "PASS",
    "Each universal claim is backed by a proof (L08 110-112, 117, 122-127, 131-132; L09 141-147, 159, 164-173) or by the tested scope named in the sentence (L08 line 146 'Doubling every entry'; L09 line 52 'in all 23'; L09 line 356 'not always', supported by the 23 instances). The new Prop 2.3 wording and E2 scope every nonzero c to matrices with positive eigenvalue sum, which the proof covers.")
row("PROSE-REMARK-2.4", "2.2-scope", "L08.html Remark 2.4 last two sentences (line 132)", "PASS",
    "'For c = 1 nothing changes. The shares can then change.' Read literally, 'then' follows c = 1; the paragraph's standing assumption (c not 0 or 1) gives the intended meaning. The existence claim is supported by the one Lab 1 case (output line 282, 0.7587 to 0.9791) and graded C in key row 434. Not false; clarity note for the builder: 'For c other than 0 and 1, the shares can change.'")
row("STRUCT-WHY", "2.9-structure", "L07, L08, L09 why-it-matters (line 52)", "PASS",
    "Tag-stripped word counts this round: L07 110, L08 114, L09 115; all within BUILDER_RULES 150's 'at most 120 words' limit.")
row("STRUCT-ORDER", "2.9-structure", "L07, L08, L09 section order and counts (BUILDER_RULES section 4)", "PASS",
    "Order: why-it-matters, core sections with Definition/Theorem/Proof/Remark blocks, inline lab, canon-breaks, misconceptions (3 each), problem set (3 per tier with worked solutions), key results, retrieval quiz (L07 9 items, L08 9, L09 11), references. M3 has no debate key.")
row("HOURS", "2.9-structure", "L07.html (data-hours 11), L08.html (12), L09.html (12); hub split", "PASS",
    "data-hours 11, 12, 12 match plans/M3-build-plan.md section 2.2. The nine lesson hours sum to 105 (L01-L09: 12, 11, 12, 12, 12, 11, 11, 12, 12) = hub data-hours-lessons 105; project 45; total 150 = curriculum hours.")
row("DATA-CLAIM", "2.8-data", "L08.html canon-break (line 291) and Lab 1 heading (line 145)", "PASS",
    "Claim: the program does not embed a multi-tenor series from which three or more tenors can be read. course/assets/data/market/MANIFEST.json dataset ust_daily has columns tbill_3m and cmt_10y only (2 series). The claim is true.")
row("HONEST-GAP", "2.8-data", "L08.html canon-break (line 291)", "PASS",
    "The curriculum's Treasury lab is stated as not run, and L08 uses a SIMULATED panel, consistent with architect decision B2/Q1 in plans/M3-build-plan.md.")
row("SIMULATED-LABELS", "2.8-data", "L07 lab (lines 124-128), L08 lines 145-151 and twin docstring, L09 lines 52, 193, 202 and twin docstring",
    "PASS", "Every generated input is labelled SIMULATED on the page and in the twin docstring; L07-L09 read no data files (no data-files attribute).")
row("DELTA-READ", "2.9-structure", "delta 440ed3c8..142ecfc2 in this slice", "PASS",
    "git diff 440ed3c8 142ecfc2: L08.html hunks at lines 52, 122, 384 and 430-432 (4 lines changed), L09.html line 56 (1 line). L07.html and all three lab twins are byte-identical. Every hunk was read and re-verified above. The hunk in tests/labs/M3/lab-M3-project-3.py belongs to the project slice and is not in this slice.")

ledger = {
    "unit": "M3",
    "slice": "c",
    "round": 6,
    "verifier": "independent Haiku verifier (round 6), checkout verifyD6-M3-c",
    "pin": "142ecfc2bd27061de18bd67e83df81e69f5c249d",
    "base": "440ed3c8216725d498d9c6d7c746907d4d418198",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD6-M3-c",
    "scratch": "system temp directories created per twin run (tempfile.TemporaryDirectory, removed after each run); one empty /tmp directory removed after use",
    "verified_at": "2026-11-03",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta 440ed3c8..142ecfc2 read hunk by hunk (L08 4 hunks, L09 1 hunk). L08 and L09 were read in full line by line (L08 531 lines, L09 606 lines), "
        "both lab twins re-run alone under python -I -W error, and every number and proof in the changed and affected subjects was re-derived "
        f"(scripts {S}m3c_r6_numbers.py, {S}m3c_r6_twin_vs_page.py). L07.html and its twin are byte-identical to the previous pin, so the round-5 PASS rows for L07 are carried with the prefix. "
        "Mutation testing is not applicable to this slice (lab twins are demonstrations; no grader here). Not checked: cards.json entries for L07-L09 (another slice); project.html, grader/, the hub index and "
        "lab-M3-project-3.py (other slices); a full pytest run (only the selected slice tests); a live verify_refs run; a light and dark 360 px screenshot (page_smoke only); "
        "the reference-match and wording of the project and hub. Remark 2.4's last sentence is a clarity note, not a failure."
    ),
    "summary": "",
}

n = len(rows)
passes = sum(1 for r in rows if r["status"] == "PASS")
fails = sum(1 for r in rows if r["status"] == "FAIL")
unver = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
ledger["summary"] = (
    f"M3 slice c round 6 at pin 142ecfc: {n} rows (pass={passes}, fail={fails}, unverifiable={unver}). "
    "The one FAIL is KEY-L08-430: the L08 key-results row for Theorem 1.4 drops the 'whenever the eigenvalue sum is positive' condition that the theorem states, "
    "while the sibling row 432 was fixed. Every gate passes; all three twins match their pages; the round-5 DAG-PSD-REDEF fail is fixed; the L08 Prop 2.3 hypothesis is consistent."
)
out = ROOT / "ledgers/M3/M3-c.json"
out.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", n, "pass", passes, "fail", fails, "unverifiable", unver)
