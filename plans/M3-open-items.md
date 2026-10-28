# M3 open items (builder C: lessons L06 to L08)

Scope: `course/modules/M/M3/L06.html`, `L07.html`, `L08.html` and the twins `tests/labs/M3/lab-M3-L06-1.py`, `lab-M3-L07-1.py`, `lab-M3-L08-1.py`. Not written by this builder: hub, L01 to L05, L09, project, grader, cards.json.

## DATA_REQUEST D1 (architect decision B2, blocks the curriculum's Treasury lab as written)

- Need: a cleared multi-tenor daily yield series with at least three tenors, so that level, slope and curvature can be identified from data.
- Source: the candidate named in the build plan (Section 12), `https://www.federalreserve.gov/releases/h15/data/FRB_h15_xml.zip`. Not verified by this builder; the architect or a verifier must read the release XML.
- Series identifiers: NOT typed here. The architect's decision forbids inventing them. They must be read from the release's own XML.
- Licence: to be confirmed against the H.15 entry in `tools/data_sources.yaml`. This builder did not read that entry.
- Transform: daily constant-maturity yields for the tenors selected, with the end date pinned as `tools/fetch_data.py` requires.
- Effect on this unit: L08 uses a SIMULATED six-tenor panel (seed 8). The L08 page says the curriculum's Treasury lab is not run and makes no claim about real curves.

## Plain terms defined in prose (GLOSSARY_REQUESTS, architect Q4: plain prose, no `<dfn>`)

Defined in the text of the lesson that first uses them; none is a registered concept:
- L06: inner product, norm, unit vector, orthonormal, orthogonal matrix (defined with `<em>`), Gram matrix, column space, singular value, rank, Frobenius norm, trace, similar matrices, characteristic polynomial.
- L07: subspace, orthogonal to a subspace, column space, least-squares solution.
- L08: tenor, yield change, basis point, centred data, trace, cosine, explained share (defined in Definition 1.3, which also defines the principal directions and scores).

## REFERENCE_REQUESTS

- R1 (Higham, nearest correlation matrix): not needed by L06 to L08; not cited or named on these pages. Belongs to L09.
- R2 (Litterman and Scheinkman, level, slope, curvature): not cited. Lesson 8 states the level, slope and curvature shapes as definitions (Definition 3.1) and says that it makes no claim about observed curves. A source would be needed only if a finding about real curves is written.
- R3 (Eckart-Young): not needed. L06 does not state a low-rank approximation theorem, and says so in its canon-breaks list.
- Axler (2024) and Strang (2023) are registry keys for the unit but are not cited on L06 to L08. No result on these pages is attributed to a source, and no locator was read.

## DAG notes

- No concept is linked before its definition on L06 to L08. Links used: `eigendecomposition` (L03), `spectral-theorem` (L04), `positive-semidefinite-matrix` (L05), `vector-space` (L01). Each anchor `def-<id>` exists in the sibling pages as of this writing.
- The word "covariance" and the word "correlation" are not used on L06 to L08 as a description of the data matrix. The matrix is written as the centred cross-product matrix over T minus 1 (architect decision B1). The L09 title, "Nearest Correlation Matrices and Eigenvalue Clipping", is the unit's own concept and is taken from the build plan; the integrator should check it against the title that Builder D finally uses.
- B3 is respected: the comparison weights do not appear on these pages.
- B4 is respected: no Cholesky decomposition and no IEEE 754 theory on these pages.

## Gate status (targeted, this builder)

- `check_pages --page L06`, `L07`, `L08`: PASS.
- `run_labs --page L06`, `L07`, `L08`: PASS, each 1/1.
- `check_dag --unit M3`: PASS at the time of the last run.
- `ruff check` and `ruff format --check` on the three twins: PASS.
- `mypy --no-incremental` on the three twins: PASS.
- `run_graders`, `mutate_graders`, `page_smoke`: not applicable to these pages (the project is another builder's). `page_smoke` was not run, per the brief.
- Not run: `check_projects`, `run_graders`, `mutate_graders`, `page_smoke`.

---

# M3 open items (builder B: lessons L03 to L05)

Scope: `course/modules/M/M3/L03.html`, `L04.html`, `L05.html` and the twins `tests/labs/M3/lab-M3-L03-1.py`, `lab-M3-L04-1.py`, `lab-M3-L05-1.py`. Not written by this builder: hub, L01, L02, L06 to L09, project, grader, cards.json.

## Grade C lab results (architect decision needed)

- Lab results are graded with `<span class="grade" data-grade="C">`, not `span.claim`, and the key-results row names its lab in the Source column. No registry key is cited, because no key describes a lab's output. `check_pages.py` requires a key only on a `span.claim` graded other than T.
- The lesson rule "a grade-C span needs a registry key" and the rule that a result read off a SIMULATED lab is graded C naming the lab conflict for lab output. The architect must choose the form.

## Standing facts (assumed, not proved, no locator)

- L03 F1: the invertibility and determinant criterion, stated for real matrices.
- L04 F1 (extended to complex matrices), F2 (fundamental theorem of algebra, and a complex root for `det(A - lambda I)`), F3 (Gram–Schmidt: every subspace of R^n has an orthonormal basis), F4 (rank–nullity).
- Each is stated as an assumption on its page. None is cited, and this builder did not check `references/references.json` for a key for any of them.

## Plain terms defined in prose (GLOSSARY_REQUESTS, architect Q4)

- L03: eigenvalue, eigenvector, eigenspace, characteristic polynomial, diagonalisable, rank (Definition 2.5), determinant (named in F1, definition taken as given).
- L04: transpose, inner product, norm, orthonormal, orthogonal matrix, null space, complex conjugation, Gram–Schmidt (named in F3).
- L05: quadratic form, Gram matrix (Definition 1.3), positive definite (Definition 1.4), tolerance test (Definition 3.1).

## NOTATION_REQUESTS

- `\top` (transpose) is written as `^{\top}`. It is a standard KaTeX command and is not in `notation/notation.json`. Request registration.
- `\mathbb{C}` (complex numbers) is used in L04 §1 and Lemma 2.1. It is not registered. Request a macro.
- `\operatorname{rank}` and `\binom` are standard KaTeX and are not registered. Confirm whether the registry is meant to cover them.
- `\R` and `\diag` are registered and are used.

## DAG notes

- No DAG defect. Links to `L01.html#def-vector-space` and `L02.html#def-linear-map` resolve. `mathematical-induction` is an M1 concept in the prerequisite closure.
- The covariance matrix (M4) and correlation (M4) are not named on L03 to L05.

## Gate status (this builder, targeted; run after the pages were final)

- `check_pages.py --unit M3 --page L03`, `L04`, `L05`: PASS each.
- `check_pages.py --unit M3`: FAIL on `index.html` (lessons declare 104 h, the hub says 105 h; hub is not this builder's) and `cards.json` missing (Builder F).
- `check_dag.py --unit M3`: PASS.
- `run_labs.py --page L03`, `L04`, `L05`: PASS, 1/1 each. `run_labs.py --unit M3`: FAIL 10/12 on `project.html` (`lab-M3-project-1`, `lab-M3-project-3`), not this builder's.
- `ruff check` and `ruff format --check` on the three twins: PASS. `mypy --no-incremental` on the three twins: PASS.
- `run_graders.py --unit M3 --seeds 0-49`: PASS (reference 50/50).
- `page_smoke.py --unit M3 --pages L03 L04 L05`: PASS (final run). An earlier run failed L04 at 360 px (a quiz fieldset with long option labels); the options were shortened and the long inline math moved to display blocks.

## Builder E (project, grader, labs lab-M3-project-1 to -3)

Scope: `course/modules/M/M3/project.html`, `course/modules/M/M3/grader/` (`instance.py`, `reference.py`, `starter.py`,
`test_project.py`), the twins `tests/labs/M3/lab-M3-project-1.py` to `lab-M3-project-3.py`, and the mutants and alternative
implementations in `ledgers/M3/mutants/` and `ledgers/M3/alternatives/`. Not written by this builder: hub, L01 to L09, cards.json.

### REFERENCE_REQUEST R1 (open, not cited)

- Needed for: a proof that the projection repair (Dykstra's alternating projections, `projection_repair`) converges to the
  Frobenius-nearest correlation matrix. The page does not state that proof. Its C3 criterion says the test checks the
  property on seeded instances and does not prove convergence, and the page cites no source for it.
- Candidate: Higham (2002), "Computing the nearest correlation matrix: a problem from finance". From recall; title, venue and
  year NOT verified here. Architect to look it up through Crossref before any use (this is the plan's R1).

### DATA (none requested)

- The project uses SIMULATED instances (`grader/instance.py`) and the hand-set matrices of Labs 1 to 3 only (architect Q8).
  No real-data variant exists. Rung 4 names no data source.

### Deviations from the build plan (for the architect to accept or reject)

- Plan 5.1 names `data-packages="numpy"` on the grader panel. The project is standard-library only (the reference uses
  cyclic Jacobi rotations, and the labs print the same lines with no NumPy), so the panel declares no packages. NumPy appears
  only inside the alternative implementations in `ledgers/M3/alternatives/` (alt1, alt3), which are not shipped.
- Plan 5.5 candidates were six criteria; the page uses five (C1 PSD and unit diagonal with proofs A1 and A2; C2 weights with
  A3; C3 nearest repair; C4 SIMULATED labelling; C5 limitations and recommendation). Both within the 4-7 rule.
- The ValueError list is the plan's four conditions (Section 5.2) and nothing else; it is applied to every matrix function
  (non-square and asymmetric) and to `comparison_weights` (volatility at or below zero, and length mismatch).

### KNOWN_LIMITATIONS (builder E)

- The nearness test (`test_projection_repair_is_no_farther_than_clipping`) and the clipping witness
  (`test_projection_repair_differs_from_clipping_on_this_instance`, threshold 1e-3; the reference's smallest entry gap on
  seeds 0 to 49 is 5.2e-3 for the first instance) hold on the seeded instances. The second instance (seed + 7919) was
  checked by the suite run on seeds 0 to 49, which passes.
- Mutant m03 (`is_psd` without tolerance) is killed by the tolerance-boundary test on seed 0, and by the planted-zero test on
  34 of seeds 0 to 49 (not on seed 0, where rounding gives a non-negative eigenvalue).
- Mutant m04 (a constant clipping answer) is killed on seed 0 by the non-square test, because the constant ignores its
  input; it is not killed by a seed-specific test.
- Unnamed invalid inputs (an empty matrix, a diagonal that is not positive in the rescaling) raise ValueError in the
  reference. No test asserts it, and the page does not name it.
- The rung-3 lab's matrix (Lab 3) and the instances are SIMULATED; no claim in the report is data-backed.

---

# M3 open items (builder F: cards.json, L01 to L09)

Scope: `course/modules/M/M3/cards.json` (167 cards, ids `M3-c001` to `M3-c167`). Written from the lesson text as it stood at 07:54 on 2026-10-28. Not changed: any lesson, the hub, the project, the grader, the labs.

## Lesson defects found while building the cards (the lesson owner must fix; cards follow the current text)

- **Hub hours (blocking for `check_pages --unit M3`).** `index.html` sets `data-hours-lessons="105"`. The lessons declare 11 + 11 + 12 + 12 + 12 + 11 + 11 + 12 + 12 = 104 h. The plan's sum of 105 (plan §2.2) is an arithmetic error. Architect decision: set the hub to 104 and the project to 46 (46/150 = 31%, inside 10-40%), or change one lesson's declared hours to 12 (hub stays 105). Check output: `FAIL M3: index.html: lessons declare 104 h; the hub says 105 h`.
- **L03, intro and key-results row.** The text says "Lab 1 checks the identities on three fixed matrices". The twin `tests/labs/M3/lab-M3-L03-1.py` uses two fixed matrices (`A_INT` and `B`). Fix the wording to two matrices.
- **L03 Definition 2.5 and L01 Definition 3.3 both define rank.** L01 defines rank as the number of pivots. L03 defines it as the dimension of the span of the columns. Neither lesson proves they agree. Either cite the equivalence as a proved result (it follows from Proposition 3.5 and the pivot argument of L01, if stated), or drop L03's definition and point to L01.
- **L06, Theorem 2.2, Step 5.** It says "the columns of A are A v_j = sigma_j u_j for j <= r and 0 otherwise, so the column space of A is span(u_1..u_r)". The columns of A are not the vectors A v_j. The correct statement: the column space is {A x}, and it equals span{A v_1, ..., A v_n} because v_1..v_n is a basis. Rewrite Step 5.
- **L07, Exercise E2.** The solution states A^T y is approximately (18.38, 3.10, -17.60) for the lab's response. The lab prints neither value. The values are correct (I computed 18.3797, 3.0959, -17.6035 from the lab's own seeded draws), but the page should print them from the lab or show the calculation.
- **SIMULATED label (BLUEPRINT section 5.3).** L01 (seeded integer vectors), L02 (seeded integer pairs) and L06 (seeded normal matrices) generate their inputs, and their lab headings do not carry a visible SIMULATED label. L04, L05 (Part C), L07, L08 and L09 do. Add the label to the L01, L02 and L06 lab headings.
- **L08, Definition 3.1.** "close to 1" is undefined. A threshold, or the statement that the label is a convention, is needed. The card follows the text as written.
- **L02, Remark 2.5** says it "is used in Theorem 4.1". The proof of Theorem 4.1 does not invoke it. Remove the sentence or state the use.

## DATA_REQUEST, REFERENCE_REQUEST and GLOSSARY items

- No new REFERENCE_REQUEST from the cards. Cards cite no registry key. `cite` is omitted on every card, because no locator for `axler2024linear` or `strang2023introduction` has been read (L01 to L09 say so in their References sections).
- The alternating-projection method (L09, Method 2) is named but has no registry key. This is the plan's REFERENCE_REQUEST R1 (Higham 2002). The cards describe it only as the lesson's own procedure, with no attribution.
- GLOSSARY_REQUESTS: none new from the cards. The plain terms in plan Q4 are defined in the lesson text. Rank has two definitions (see above).
