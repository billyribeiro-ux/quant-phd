# M3 build plan: Linear Algebra (planner output, 2026-10-28)

Unit: **M3 · Linear Algebra** · tier F · 150 h · prerequisites M1 · no Atlas milestone · grading `both` (autograder for the
covariance-matrix engine, rubric for the comparison report) · output directory `course/modules/M/M3/` (part code `M`, as M1).
Owner: orchestrator (architect). Executors: Claude Haiku builders, then independent Haiku verifiers (VERIFIER_RULES). A builder
never verifies and never writes a ledger. No git commit, no push.

Status of this file: a planner's proposal. Section 9 lists **blocking** issues that need an architect decision before the
affected lessons are built. Section 10 lists open questions. No lesson content is written here.

Evidence convention: `file:line` for every curriculum or tool fact. Anything not found in the curriculum is marked
**NOT IN CURRICULUM**.

## 0. Evidence for the curriculum facts used below

| Fact | Evidence |
|---|---|
| Entry M3: id, title "Linear Algebra", tier F, hours 150, prereqs [M1] | `curriculum/01-foundations.yaml:157-161` |
| Core text: vector spaces, linear maps, eigendecomposition, spectral theorem, SVD, PSD matrices, projections, least-squares geometry, PCA | `curriculum/01-foundations.yaml:162-164` |
| Twelve introduced concepts, one line each | `curriculum/01-foundations.yaml:166-177` |
| Sources: Axler (2024, 4th ed.); Strang (2023, 6th ed.) | `curriculum/01-foundations.yaml:178-180` |
| Lab: "PCA of the U.S. Treasury curve (embedded data): level, slope, curvature." | `curriculum/01-foundations.yaml:181` |
| Project "Covariance-matrix doctor", brief, deliverable "Tested module plus a comparison report.", grading `both` | `curriculum/01-foundations.yaml:182-189` (`grading: both` at 189) |
| No `debate` key on M3 | `curriculum/01-foundations.yaml:157-190` (no `debate:` line) |
| No `atlas:` key on the M3 project; the Atlas list names no M3 (its only `module: M...` hit is `MS3` at line 236) | `curriculum/01-foundations.yaml:182-189`; `curriculum/meta.yaml:198-276` |
| JSON row mirrors the YAML (hours 150 at line 6390; lab at 6413; id at 6387) | `curriculum/curriculum.json:6387-6413` |
| Rendered CURRICULUM.md agrees | `CURRICULUM.md:226` ("M3 · Linear Algebra · F · 150 h · ← M1") |
| Prerequisite closure of M3 = {M1, P0.1} (computed from `curriculum.json` `prereqs`, planner script run in session) | M1 prereqs P0.1 (`curriculum/01-foundations.yaml:87-91` per the M1 plan); M3 prereqs [M1] (line 161) |
| Direct dependents of M3: M7, M8, S2 | `curriculum/01-foundations.yaml` M7 prereqs [M2, M3], M8 prereqs [M2, M3, CS1, FC2], S2 prereqs [S1, M3] (lines 302, 332, 663 per the grep this session) |
| Topological position: M3 follows M1 (position 6 vs 2; M4 at 12) | `curriculum/curriculum.json` `topological_order` |
| Concepts with owners relevant to M3 text: `covariance-matrix`, `correlation`, `variance`, `expectation`, `random-variable` all M4; `cholesky-decomposition`, `ieee-754-floating-point` M8; `mean-variance-optimization`, `quadratic-programming` M7; `minimum-variance-portfolio` AP2; `covariance-shrinkage` PR1; `ols-estimator` S2; `discount-factor`, `present-value` M1 | `curriculum/curriculum.json` `concepts` dict (each entry carries `module`) |
| No concept registered for: basis, span, rank, determinant, inner product, norm, eigenvalue, singular value, matrix, trace | `curriculum/curriculum.json` `concepts` (search for these terms returns no entry) |
| Registry: `axler2024linear` (verified, Crossref DOI 10.1007/978-3-031-41026-0, year 2024, `used_by: ["M3"]`) | `references/references.json:1208` |
| Registry: `strang2023introduction` (verified, Open Library, year 2023, `used_by: ["M3"]`) | `references/references.json:21415` |
| Registry: `gurkaynak2007us` (verified, `used_by: ["FI1"]`), `nelson1987parsimonious` (verified, `used_by: ["FI1"]`) | `references/references.json:11264`, `:17886` |
| No registry key for Higham (nearest correlation matrix), Litterman & Scheinkman (level, slope, curvature), Eckart & Young | searched `references/references.json` (no match) |
| Embedded data: `ust_daily` has **two** series, `tbill_3m` and `cmt_10y`; no other tenor | `course/assets/data/market/MANIFEST.json:63-` (columns list), `tools/data_sources.yaml:91-` (series block: `tbill_3m`, `cmt_10y`) |
| Licence for H.15 (Board's public-domain statement; U.S. Treasury CMT note) is quoted and checked | `tools/data_sources.yaml:91-` (licence quote, `licence_url`, note) |
| Embedded H.10 daily FX (six currencies; cleared) exists | `tools/data_sources.yaml` (`fx_daily`, first entry); MANIFEST `fx_daily` columns AUD, CAD, CHF, EUR, GBP, JPY |
| No Atlas milestone; no `atlas/*.contract.md` for M3 is needed; the `atlas/` folder holds only A8 and A15 | `ls atlas/` (A15.contract.md, A8.contract.md) and `curriculum/meta.yaml` atlas block |

Hours conflict check: the curriculum's 150 h **can** satisfy the tool rules (Section 2). Not a conflict; no STOP needed.

## 1. Rules for every builder (binding; BUILDER_RULES adapted to M3)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `VERIFIER_RULES.md` §2 (what a verifier checks),
this file, and `plans/M1-build-plan.md` (the closest worked example: tier F, grading `both`, standard-library-style labs,
no Atlas). Study `course/modules/M/M1/` for layout and `course/templates/` for markup. Study `course/modules/AC/AC4/` only for
the rubric-memo pattern. Imitate structure, not wording.

### 1.1 Lessons learned from the verification campaigns (AC2, AC1, M1, AC4, CF1). Binding for M3.

These are the defect classes those campaigns found. Each builder checks its own pages against every item before handing off.

1. **Numbers come from unrounded values.** Every printed number is computed from unrounded values and then rounded for display.
   A derived number (a percentage, a variance share, a difference) is never computed from a displayed, rounded value. The
   lab prints the unrounded value or states the rounding rule.
2. **Lab statements match code and output.** Each lab's hypothesis, interpretation and key-results row says exactly what the
   code computes and what the printed output shows, with the same tolerance and the same index. A claim "the eigenvalues
   sum to the trace" is checked by the lab, or it is not written.
3. **Attribute nothing unread.** A claim is attributed to a registry key only with a `data-locator` that a builder has read in a
   source that reproduces it. Otherwise the statement carries no attribution, or it is a derivation on the page. The
   M1 and AC2 open items show this was the most frequent defect.
4. **Scope words need a computation.** Words such as "generic", "typically", "almost always", "for every matrix", "in practice",
   "stable", "robust", "always" are used only when the lab or proof shows the scope. A lab that tests 200 random matrices does
   not support "for every matrix". Write the tested scope in the sentence ("for the 200 seeded 3x3 matrices in Lab 4").
5. **Define before use.** A term or symbol is defined (plain prose or `<dfn>`) before its first use on the page, and a
   concept is never linked before the lesson that defines it (`check_dag.py`). This applies to plain terms too (Section 10,
   Q4).
6. **Proposition hypotheses explicit.** Every theorem and proposition lists its hypotheses in the statement: the field
   (real), the dimension, symmetry, finiteness, the tolerance. A proof uses only the listed hypotheses. "Symmetric" is stated
   for every use of the spectral theorem.
7. **Grader tests demand an exception type only for conditions the page names.** The spec lists the exact invalid inputs that
   must raise `ValueError` (Section 5.2). A test asserts `ValueError` only for those. For any other input a test asserts a
   property, never a particular exception.
8. **Five alternative correct implementations must pass.** Every grader test is implementation-neutral: it checks properties
   and tolerances, not one algorithm's output, unless the spec fixes the algorithm. The verifier must run the suite against
   five alternative correct solutions (Section 5.4) on seeds 0-49 and report them.
9. **Integer cents for money.** M3 has no money quantity. If any appears (none is planned), it is `int` cents, never float.
   Weights and correlations are floats with a stated tolerance.
10. **No horizontal scroll at 360 px.** Matrices, KaTeX `pmatrix` displays, code blocks and tables sit in a box that wraps or
    scrolls inside itself. The page itself never scrolls horizontally. `page_smoke.py` checks this; builders check it by reading
    the stylesheet and by a Chromium screenshot if the builder has one, and say which.
11. **Labs call `main()` at top level.** Every lab twin ends with a bare `main()` call (the M1 pattern:
    `tests/labs/M1/lab-M1-L06-1.py:72`), so the output is printed when the twin runs under Pyodide and CPython. A twin that
    only defines `main` prints nothing and fails the lab check.

### 1.2 Binding rules from the BUILDER_RULES, restated for M3

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key. Theorems and derivations are grade T and
  need a complete proof or derivation on the page (BUILDER_RULES §3.5). Do not cite a source for a result you derive.
- Keys: cite only `axler2024linear` and `strang2023introduction` as curriculum sources, plus keys verified in
  `references/references.json` whose claim is shown to be theirs (Section 7). Never type bibliographic data, a page, a table, or
  a number from memory.
- Concepts: each of the 12 concepts in Section 2 is defined once with `<dfn id="def-<id>" data-concept="<id>">` in the lesson
  assigned to it. Linked elsewhere with `<a class="concept" data-concept="<id>" href="Lnn.html#def-<id>">` for an earlier lesson
  of M3, or `href="../../../concepts.html#<id>"` for M1 and P0.1 concepts. A lesson never links a concept defined in a later
  lesson. A concept owned outside the closure is never linked (Section 9, B1-B3).
- Labs: code lives once, in the twin `tests/labs/M3/lab-M3-Lnn-1.py`. The page carries `@@LAB:lab-M3-Lnn-1.py@@` and
  `@@OUT:...@@` markers and `tools/embed_labs.py` fills them. Never type an expected output. Lab ids must match
  `lab-M3-<page>-<n>` (`check_pages.py` line 258). Seeded RNGs only. No network. Under 10 s in Pyodide.
- Lab runtime: NumPy is needed for eigendecomposition and SVD. The runtime lists NumPy and SciPy among the vendored packages
  (`tools/vendor_spec.yaml:59`: `packages: [numpy, scipy, pytest]`). A lab that uses NumPy declares it with `data-packages="numpy"`
  as AP1 does (`course/modules/AP/AP1/project.html:53`). Use NumPy only for linear-algebra routines the lab then checks. Do not
  use NumPy's `linalg` as the definition of a quantity the page proves. Section 10, Q3 asks the architect to confirm.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*.json`, `references/*.json`, `MANIFEST.json`). Never edit `curriculum/*.yaml`, `tools/data_sources.yaml`
  or `atlas/`; request changes in the output contract.
- Do not run `page_smoke.py` (verifiers run it on a quiet machine). Targeted checks only (Section 8).
- No `git commit`, no push. The output contract is BUILDER_RULES §10.

## 2. Outline and file ownership

### 2.1 Hours split (derived, checked against the tool rules)

Constraints, from `tools/check_pages.py`:
- each lesson declares 6-12 study hours (line 227-228);
- the hub's `data-hours-lessons` + `data-hours-project` equals the curriculum's 150 (line 337-338);
- the project is 10-40% of module hours, i.e. 15 h to 60 h (line 339-340);
- lessons sum to the hub's `data-hours-lessons` (line 341-342).

Feasible region: with project p and lessons L = 150 - p, the number of lessons n must satisfy 6n <= L <= 12n. With p = 45 (30%) and
L = 105, n must be 9 to 17; n = 9 is chosen (below). Other feasible splits (for example 8 lessons at 90-96 h with a 54-60 h project,
or 10 lessons with a 30 h project) are listed in Section 10, Q5. **The curriculum's 150 h is satisfiable; no STOP is needed.**

### 2.2 Lesson outline (proposed; the architect fixes it)

Twelve concepts (`curriculum/01-foundations.yaml:166-177`), each in exactly one lesson. Lesson hours sum to 105; project 45;
total 150. Lab twin per lesson (one lab per lesson, as the M1 Q2 decision); the curriculum's own lab is in L08.

| Lesson | Title (working) | Concepts it defines (`<dfn>`) | Lab twin id | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Vector spaces: spans, bases and dimension | `vector-space` | `tests/labs/M3/lab-M3-L01-1.py`: span and independence checked by rank of seeded integer vectors in R^3 and R^4 | 11 | Builder A |
| L02 | Linear maps and their matrices | `linear-map` | `lab-M3-L02-1.py`: the matrix of one map in two bases; change-of-basis identity checked to 1e-12 | 11 | Builder A |
| L03 | Eigendecomposition | `eigendecomposition` | `lab-M3-L03-1.py`: eigenpairs of a 3x3 matrix with a known spectrum, residual \(\|Av-\lambda v\|\) printed | 12 | Builder B |
| L04 | The spectral theorem for symmetric matrices | `spectral-theorem` | `lab-M3-L04-1.py`: orthogonal eigenvectors and \(A = Q\Lambda Q^{\top}\) reconstruction on seeded symmetric matrices | 12 | Builder B |
| L05 | Positive-semidefinite matrices | `positive-semidefinite-matrix` | `lab-M3-L05-1.py`: PSD test by eigenvalues; quadratic-form sampling; a counterexample matrix | 12 | Builder B |
| L06 | The singular value decomposition | `singular-value-decomposition` | `lab-M3-L06-1.py`: SVD singular values equal the square roots of the eigenvalues of \(A^{\top}A\) | 11 | Builder C |
| L07 | Orthogonal projections and least squares | `orthogonal-projection`, `least-squares-projection` | `lab-M3-L07-1.py`: projection matrix \(P=A(A^{\top}A)^{-1}A^{\top}\) against the normal equations; residual orthogonal to columns | 11 | Builder C |
| L08 | Principal component analysis and the yield-curve factors | `principal-component-analysis`, `level-slope-curvature` | `lab-M3-L08-1.py` (**the curriculum lab**): PCA of the U.S. Treasury curve, level, slope, curvature. **Blocked on data (B2)** | 12 | Builder C |
| L09 | Nearest correlation matrices and eigenvalue clipping | `nearest-correlation-matrix`, `eigenvalue-clipping` | `lab-M3-L09-1.py`: a non-PSD matrix repaired by clipping; repaired matrix PSD with unit diagonal | 12 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours 105 + 45 | none | none | - | Builder A |
| project | Covariance-matrix doctor: four-rung ladder, autograder spec, comparison-report rubric | none | `lab-M3-project-1` (rung 1), `lab-M3-project-2` (rung 2, completion), `lab-M3-project-3` (rung 3 check) | 45 | Builder E |
| grader | `grader/reference.py`, `starter.py`, `instance.py`, `test_project.py` | none | none | - | Builder E |
| cards | `cards.json` from L01-L09 | none | none | - | Builder F (after A-D) |

Totals: lessons 11+11+12+12+12+12+11+12+12 = 105 h; project 45 h (30%, inside 10-40%); unit 150 h.
Concept coverage: L01 1, L02 1, L03 1, L04 1, L05 1, L06 1, L07 2, L08 2, L09 2 = 12, matching the
12 entries at `curriculum/01-foundations.yaml:166-177`. Each concept is in exactly one row.

Ordering: L02 needs L01's vector space; L03 needs L02's linear map; L04 needs L03's eigenpairs; L05 needs L04's spectral
decomposition; L06 uses L04-L05 (the singular values of \(A\) are square roots of eigenvalues of \(A^{\top}A\), which is PSD by L05);
L07 uses L01 (span, dimension) and L02; L08 uses L04 (spectral theorem), L06 (SVD) and L07 (projection); L09 uses L05 (PSD) and L03.
No lesson links a later definition. `check_dag.py` checks this.

### 2.3 Lesson content guidance (what each must establish; builders decide the argument)

- **L01.** Vector space axioms over \(\mathbb{R}\); subspace test; span; linear independence; basis; dimension. Proofs T. Lab
  checks rank-based independence on seeded integer vectors (exact arithmetic with `fractions.Fraction`, not floats).
- **L02.** Linear map and its matrix with respect to bases; the matrix of a composition is the product; change of basis
  \(B = S^{-1}AS\). Derivation T. Lab checks the identity to a stated tolerance.
- **L03.** Eigenvalue and eigenvector definitions; characteristic polynomial; diagonalisation when a basis of eigenvectors
  exists. Only the statement "diagonalisable with eigenvalues ..." is claimed when the lab shows it. Lab reports residuals.
- **L04.** Spectral theorem for real symmetric matrices, hypotheses explicit (real, symmetric, finite-dimensional). The statement
  T with a complete proof sketch labelled as a sketch if a full proof is too long (the proof must name the steps it skips). Lab
  reconstructs \(A\) from \(Q\Lambda Q^{\top}\).
- **L05.** PSD definition \(x^{\top}Ax \ge 0\) for all \(x\); equivalence to nonnegative eigenvalues for symmetric \(A\) (T).
  Lab tests PSD by eigenvalues and by sampling quadratic forms; sampling supports only the tested seeds (scope rule).
  **Do not use Cholesky** (M8 concept, Section 9 B4).
- **L06.** SVD \(A = U\Sigma V^{\top}\); singular values; relation to eigenvalues of \(A^{\top}A\) (T). Low-rank approximation is
  stated and not proved unless the proof is written in full; if the Eckart-Young statement appears, it is labelled with its
  hypotheses and marked grade T only with a complete proof. No registry key exists for it (Section 7).
- **L07.** Orthogonal projection onto a subspace; projection matrix formula when \(A\) has full column rank (T); least squares as
  orthogonal projection; normal equations (T). Lab compares with a direct solver on seeded data.
- **L08.** PCA as the spectral decomposition of a symmetric PSD matrix of centred data; explained variance shares computed from
  **unrounded** eigenvalues (rule 1.1.1); level, slope and curvature as interpretations of the loadings, stated as properties of
  the lab's output, not as theorems about all yield curves. **Requires the multi-tenor data (B2) before the curriculum's lab can be
  run as written.** The covariance matrix that PCA needs is an M4 concept (B1): the lesson uses the formula for the centred
  data matrix \(X^{\top}X/(T-1)\) as a computed matrix and does not name the M4 concept, unless the architect decides otherwise.
- **L09.** Nearest correlation matrix in the Frobenius norm (the problem statement only, with the definition of a correlation
  matrix as a symmetric PSD matrix with unit diagonal, grade T as a definition). Eigenvalue clipping then rescaling to unit
  diagonal; the rescaled matrix is not, in general, the Frobenius-nearest one, and the lab shows that on seeded examples. The
  alternating-projection method is a named method without a registry key (Section 7, REFERENCE_REQUEST).

## 3. Hub (`index.html`, Builder A)

- `<main data-hours-lessons="105" data-hours-project="45">` (sums to 150; project 30%).
- 4-8 measurable objectives (verbs such as "compute", "decide", "prove", "diagnose").
- Prerequisites: M1 linked to its page; P0.1 concepts linked from the closure as needed.
- Placement diagnostic: `<section class="quiz" id="placement" data-unit="M3" data-page="placement" data-mastery="0.8">`, the
  same bar as M1 (`course/modules/M/M1/index.html`). At least two `data-skill` items test what rungs 1-2 teach (the worked
  example's task: a rank and eigenpair check; the completion problem's missing step). Other items test M1 content.
- Lesson map linking L01-L09; project ladder `ol.ladder` with four rungs in order.
- Tier F keeps rungs 1-2 at full length (BLUEPRINT §4: minimum only from tier M upward).
- Hub notes state the **SIMULATED** and blocked-data status of L08 and the project (Section 6).

## 4. Project ladder (Builder E)

Per BUILDER_RULES §5.1 and the M1 precedent (`plans/M1-build-plan.md`):

1. **Rung 1, worked example** (`lab-M3-project-1`): a fully solved, annotated run of the reference on one SIMULATED covariance
   matrix. Each step carries a "why" note: centring, forming the matrix, the eigenvalues, the PSD check, the clipping, the
   rescaling.
2. **Rung 2, completion** (`section.lab.completion`, `lab-M3-project-2`): the same task with two steps removed (`___`), for example
   the rescaling and the PSD check. Graded instantly. Its twin is the completed solution; each non-blank line equals the twin's
   line (BUILDER_RULES §6.1).
3. **Rung 3, independent project** (graded). (a) The autograded engine `covariance_doctor.py` (Section 5). (b) The comparison report,
   rubric-graded (Section 5.5). `lab-M3-project-3` is the rung-3 check.
4. **Rung 4, stretch**: open-ended, not graded. Example: repair a matrix built from the cleared H.10 FX data, with a stated
   hypothesis about the repair's effect on weights, or a weighted-norm variant. No ceiling.

Time budget (`<table id="hours">`, declared 45 h, one-line rationale per row; `check_projects.py` requires rows with hours, a
total row that equals `data-hours-project`, and a rationale on each row):

| Component | Hours | Rationale |
|---|---|---|
| Rung 1 worked example | 2 | Read and annotate one reference run |
| Rung 2 completion | 3 | Fill two steps and pass the instant check |
| Engine: PSD check, clipping, projection, min-eigenvalue (rung 3a) | 14 | Four functions, edge cases, tests against the reference |
| Comparison of weights across the repairs (rung 3a, second part) | 8 | Compute weights for each repair and check the properties in the grader |
| Comparison report (rung 3b draft and revision) | 12 | Two-page report against the rubric |
| Self-check against the grader and the rubric (rung 3c) | 6 | Run the suite; score two exemplars blind; compare |
| **Total** | **45** | Equals `data-hours-project` |

## 5. Grader design (Builder E)

### 5.1 Grading mode

`grading: both` (`curriculum/01-foundations.yaml:189`). The spec's grading entry names both "autograder" and "rubric"
(`tools/check_projects.py`, `GRADING_WORDS` and `grading_problems`). The page carries
`section.grader-panel` with `data-unit="M3" data-grader="grader/" data-suite="test_project.py" data-support="instance.py"
data-solution="covariance_doctor.py" data-starter="starter.py" data-packages="numpy"` (AP1 pattern,
`course/modules/AP/AP1/project.html:178`). The solution file is unit-local, not `atlas/`.

### 5.2 Frozen interface (proposal; the architect freezes it)

The solution module `covariance_doctor.py` (student file) exposes:

- `min_eigenvalue(matrix: list[list[float]]) -> float`: the smallest eigenvalue of the symmetric matrix.
- `is_psd(matrix: list[list[float]], tol: float = 1e-10) -> bool`: True when every eigenvalue is at least \(-\text{tol}\).
- `clip_repair(matrix: list[list[float]], floor: float = 0.0) -> list[list[float]]`: eigenvalues below `floor` set to `floor`,
  then rescaled to unit diagonal (\(D^{-1/2} X D^{-1/2}\)).
- `projection_repair(matrix: list[list[float]], tol: float = 1e-10, max_iter: int = 500) -> list[list[float]]`: an
  alternating-projection (or any other) approximation of the Frobenius-nearest correlation matrix.
- `comparison_weights(corr: list[list[float]], vols: list[float]) -> list[float]`: weights \(w\) proportional to \(\Sigma^{-1}\mathbf{1}\)
  with \(\Sigma = D C D\), normalised to sum to 1 (name and concept: Section 9 B3).

**Exceptions named in the spec (the only ones a test may assert as `ValueError`):**
- non-square input;
- asymmetric input beyond the tolerance 1e-9;
- a volatility \(\le 0\) in `comparison_weights` (the vols are the only inputs with a positivity rule);
- length mismatch between `corr` and `vols`.
Every other invalid input is outside the spec: no test asserts an exception type for it.

### 5.3 Instances (`grader/instance.py`)

`make_instance(seed: int) -> dict[str, Any]`: deterministic; generates a \(k\times k\) (k in {3,4,5}) symmetric matrix that is
**not PSD** by construction (a planted pairwise-estimation error), vols in a stated range, and a clipping-target reference
checked by the reference only. Every instance is valid under the spec. Labelled **SIMULATED** in the docstring and on the page.
Seeds 0-49 give materially different matrices (BUILDER_RULES §5.3). The reference passes every test on seeds 0-49.

### 5.4 Test suite (`grader/test_project.py`) and implementation neutrality

Each test checks properties and numbers with stated tolerances. Required tests (minimum set):

- `clip_repair` output is symmetric, has unit diagonal to 1e-9, and is PSD to tol.
- `projection_repair` output is symmetric, unit diagonal, PSD to tol, and its Frobenius distance to the input is at most that of
  `clip_repair`'s output plus 1e-6 (the nearest matrix property; an implementation-neutral test).
- When the input is already a PSD correlation matrix, both repairs return it to tolerance (identity).
- `min_eigenvalue` agrees with the generating parameters on planted spectra (not with the reference's output).
- `comparison_weights` sums to 1 and reproduces the planted weights on a matrix built from known weights.
- Edge cases: `k = 1` (the repairs return `[[1.0]]`); no idempotence test unless the spec states the property.
- Failure behaviour: the four named `ValueError` conditions only; every other test asserts properties.

Five alternative correct implementations (the verifier runs them, Section 11): (1) `numpy.linalg.eigh`-based clipping; (2) a
Jacobi eigenvalue routine in pure Python; (3) alternating projections with a different stopping rule; (4) clipping computed in
`fractions.Fraction` on the rational planted inputs and converted to float; (5) a `min_eigenvalue` by shifted power
iteration. All five must pass seeds 0-49. (The fifth is a proposal; the verifier may substitute any correct one.)

Mutants the verifier must write (VERIFIER_RULES §2.6), at least three, each killed:
1. clipping that sets negative eigenvalues to zero but skips the diagonal rescaling (unit diagonal violated);
2. comparison weights using \(\Sigma\) instead of \(\Sigma^{-1}\mathbf{1}\) (wrong direction);
3. `is_psd` testing `min_eigenvalue >= 0` with no tolerance on a planted zero eigenvalue (rounding flips the verdict);
4. a hard-coded answer for seed 0;
5. projection that returns the clipping output unchanged (fails the Frobenius-nearest test on instances where clipping is
   not nearest).

### 5.5 Comparison report (rubric)

- 4-7 criteria, each with four **observable** levels (quote-checked by `check_projects.py` rubric rules). Candidate criteria:
  (1) every repair's PSD and unit-diagonal status is reported with the tolerance used; (2) each weight change is tied to a number
  in the output table; (3) the report states which repair is the Frobenius-nearest one and why, with the test that shows it;
  (4) the report separates SIMULATED from data-backed results; (5) limitations of the repair (the clipping rescaling is not
  nearest) are stated; (6) the recommendation follows from the numbers and names what would change it.
- Exemplars at **level 4 and level 2**, fully written, with annotations mapping passages to descriptors.
- Self-assessment form; the page shows where the student's scoring diverged from the exemplar scoring.
- Question bank: **not required** (the report is not adversarial). Architect may decide otherwise (Section 10, Q7).

## 6. Real-data policy and honest gaps

- **Curriculum's own lab (L08) needs data that is not embedded.** `ust_daily` has two series (`tbill_3m`, `cmt_10y`;
  `course/assets/data/market/MANIFEST.json:63-` and `tools/data_sources.yaml:91-`). Level and slope need at least two tenors,
  and **curvature needs at least three** (a PCA of two series has two components, so no third factor can be identified). The
  lab as written cannot be run on embedded data alone. See Section 9, B2.
- The H.15 licence is cleared (`tools/data_sources.yaml`, licence quote and `licence_url`). A richer H.15 curve would fall under
  the same quoted statement. Adding it requires an edit to `tools/data_sources.yaml` (architect) and a `fetch_data.py --fetch
  --only <id>` run (BUILDER_RULES §6.6). The H.15 series identifiers for other tenors are **NOT verified** here; they must be read
  from the release's own XML, not typed from memory.
- **Project data.** The project's "empirical correlation matrices" are SIMULATED (generated instances, §5.3). A real-data
  variant is possible with `fx_daily` (six cleared H.10 spot series; `tools/data_sources.yaml`, first dataset entry). Whether
  pairwise-complete estimation on that data yields a non-PSD matrix is **not known** and must be computed, not assumed.
- Bring-your-own-data mode is not needed if the architect approves B2's new dataset.
- The **honest-pending** wording: if B2 is not resolved, L08 states that the curriculum lab's curvature factor is **not** shown on
  the embedded data, names DATA_REQUEST B2, and runs only level and slope on the two embedded series. This keeps the page true;
  it does not meet the curriculum's lab text (Section 10, Q1).
- No figure may plot data it does not show. Every figure carries a source line with the MANIFEST retrieval date for real data
  (BUILDER_RULES §6.4).

## 7. Registry keys the module may cite

| Key | Status | Use in M3 |
|---|---|---|
| `axler2024linear` | verified (Crossref, year 2024; `references/references.json:1208`; `used_by: ["M3"]`) | the curriculum's first source. Cite for any statement about vector spaces, eigenvalues and the spectral theorem **only with a confirmed locator**. Otherwise uncited derivation |
| `strang2023introduction` | verified (Open Library, year 2023; `references/references.json:21415`; `used_by: ["M3"]`) | the second curriculum source. Same rule |
| `gurkaynak2007us` | verified (`references/references.json:11264`; `used_by: ["FI1"]`) | optional for L08's yield-curve context (grade C). Needs an architect decision to add M3 to `used_by`; not required by the tool, which checks only that a key is verified (`check_pages.py` checks the key exists and is verified) |
| `nelson1987parsimonious` | verified (`references/references.json:17886`; `used_by: ["FI1"]`) | optional for L08's level-slope-curvature interpretation. Same rule; a locator must be confirmed |
| `velleman2019prove` | verified (M1) | proof technique in L01-L02 if a builder wants it; not required |

Unresolved candidates (REFERENCE_REQUESTS, Section 12): nothing in §7 above is required for the curriculum to be covered. The
numerical and empirical claims the lessons need beyond the two textbooks are listed as requests, not cited.

## 8. Commands for this unit (check M3 only; run each once, after its files exist)

```bash
cd /Users/billyribeiro/dev/quant-phd
.venv/bin/python tools/check_pages.py --unit M3            # --page L08 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit M3
.venv/bin/python tools/check_projects.py --unit M3
.venv/bin/python tools/run_labs.py --unit M3               # --page L08 for one lesson
.venv/bin/python tools/run_graders.py --unit M3 --seeds 0-49
.venv/bin/python tools/embed_labs.py course/modules/M/M3/L01.html   # per page, after twins are written; --refresh <lab-id> after a twin edit
.venv/bin/ruff check tests/labs/M3 course/modules/M/M3/grader && .venv/bin/ruff format --check tests/labs/M3
.venv/bin/mypy                                              # strict, repo configuration (CLAUDE.md gate)
```

Verifiers only: `.venv/bin/python tools/mutate_graders.py --unit M3 --seeds 0-9`, `.venv/bin/python tools/page_smoke.py --unit M3` (the `--unit` form is BUILDER_RULES §9)
(quiet machine). Architect, once before merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`,
`build_site.py --check`, `render_curriculum.py` and `verify_refs.py --offline` (CLAUDE.md gate list).

Flags confirmed against the tools' argparse blocks this session: `check_pages.py --unit/--all/--page`
(lines 429-431); `check_dag.py --unit/--all` (89-90); `check_projects.py --unit/--all` (159-160); `run_labs.py --unit/--all/--page`
(119-121); `run_graders.py --unit/--all/--seeds` (129-131); `mutate_graders.py --unit/--all/--seeds` (30-32); `embed_labs.py pages
--refresh` (130-131). The planner did not execute any gate; the commands are not yet run against M3.

## 9. Blocking issues (architect decision needed before the named part is built)

- **B1 (DAG, blocking for L08, L09 and the project).** The concepts `covariance-matrix`, `correlation`, `variance` and `expectation`
  are owned by M4 (`curriculum/curriculum.json` concepts dict; M4 prereqs [M2]). M3's closure is {M1, P0.1}. PCA of a yield-change
  covariance matrix, the "empirical correlation matrix" of the project brief and the correlation-matrix definition in L09 all use
  them. `check_dag.py` flags only **linked** concepts, but BUILDER_RULES §1.10 treats a concept used outside the closure as a
  DAG_DEFECT. Options: (a) use the formula \(X^{\top}X/(T-1)\) for centred data and the word "correlation" only as a plain
  descriptor, with no concept link (planner's preference, Section 10 Q2); (b) a curriculum change making M4 (or a subset) a
  prerequisite of M3 (not the planner's to make; it would also move M3 later in the topological order); (c) an approved DAG_DEFECT
  request.
- **B2 (data, blocking for the curriculum lab text in L08 and the rung-3 check).** `ust_daily` embeds two series only
  (`course/assets/data/market/MANIFEST.json:63-`); curvature cannot be identified from two series. The architect must decide: (a)
  request a cleared multi-tenor H.15 dataset (DATA_REQUEST, Section 12) and add it to `tools/data_sources.yaml`; or (b) accept the
  honest-pending variant of L08 (level and slope only) and a curriculum-text change request.
- **B3 (DAG, blocking for the project's "downstream portfolio weights" step).** The brief asks to "compare the effect of each repair
  on downstream portfolio weights" (`curriculum/01-foundations.yaml:185-188`). The natural weights (minimum-variance or mean-variance)
  are owned by AP2 (`minimum-variance-portfolio`), M7 (`mean-variance-optimization`, `quadratic-programming`) and PR1
  (`equal-weight-portfolio`); none is in M3's closure. The planner proposes `comparison_weights` as a closed-form
  \(w \propto \Sigma^{-1}\mathbf{1}\) stated as a formula with no concept name (Section 5.2). Architect decision required.
- **B4 (DAG, not blocking, a rule to enforce).** `cholesky-decomposition` and `ieee-754-floating-point` are M8 concepts. L05 and the
  labs must not name them, and must not use Cholesky as a PSD test (eigenvalues only). Floating-point tolerance is stated as a
  tolerance, not as IEEE 754 theory.

## 10. Open questions for the architect (numbered)

1. **Q1 (L08 lab).** Choose B2 option (a) or (b). The planner recommends (a): a DATA_REQUEST for a cleared H.15 multi-tenor curve,
   with the lab kept as written. Until then, L08 uses the honest-pending variant.
2. **Q2 (B1).** Choose B1 option (a), (b) or (c). The planner recommends (a) with the M4 concept not named and not linked, and a
   curriculum change request if the architect wants the dependence explicit.
3. **Q3 (NumPy in labs).** Confirm NumPy is allowed in labs and the project (`data-packages="numpy"`), as AP1 does, with the
   linear-algebra routines used only as checks of the proofs (not as definitions). The alternative (standard library only, with
   pure-Python eigen and SVD routines) is possible but is a large build cost; the planner recommends NumPy.
4. **Q4 (undefined plain terms).** Terms in the core text or the lessons that are not in `introduces` and not registered:
   basis, span, rank, determinant, inner product, norm, eigenvalue, singular value, matrix, trace, orthogonal. Confirm they are
   plain prose with no `<dfn>` (the AC4 and M1 precedent, `plans/AC4-build-plan.md` Q4, `plans/M1-build-plan.md` Q3), or request
   curriculum concepts. Note: `vector-space`, `linear-map`, `eigendecomposition`, `spectral-theorem`, `singular-value-decomposition`
   are registered and each is defined. "Eigenvalue" and "singular value" are plain words, not registered, and L03 and L06 must define them in prose or the curriculum must register them.
5. **Q5 (hours split).** Confirm 105 + 45 (9 lessons; project 30%). Alternatives: 8 lessons at 90-96 h with a 54-60 h project (merge
   L01/L02 and L07/L08 would break the concept grouping); 10 lessons with a 30 h project. The planner recommends 9 lessons.
6. **Q6 (solution file and frozen interface).** Confirm `covariance_doctor.py` and the five signatures in §5.2. The ValueError list in
   §5.2 is the only exception contract.
7. **Q7 (adversarial).** Confirm the comparison report is not adversarial (no 15-angle question bank). If it is, add the bank.
8. **Q8 (embedded project data).** Confirm the project uses SIMULATED instances only, with an optional rung-4 real-data variant on
   `fx_daily`. The planner has not computed whether that data yields non-PSD matrices.
9. **Q9 (level-slope-curvature grading).** The interpretation of level, slope and curvature is a grade-C or B claim. Confirm whether
   `nelson1987parsimonious` and `gurkaynak2007us` may be added to M3's `used_by` (FI1 owns them now), and whether a locator-level
   claim is required. The planner recommends grade C with no locator until one is confirmed.
10. **Q10 (concept scope in PCA).** Confirm L08 defines PCA on a generic symmetric PSD matrix of centred data (M3 concepts only), with
    the data matrix formula stated, rather than a sample covariance matrix (M4 concept).

## 11. After the builders

1. Orchestrator integrates; runs §8 commands once; fixes cross-lesson defects (DAG, links, hours).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L03, L04-L06, L07-L09, project. The project verifier writes at
   least three mutants per round and runs the five alternative implementations (§5.4). Failing rows return to a builder with only
   the failing rows.
3. Ledger at `ledgers/M3.verification.json`; scripts archived under `ledgers/M3/scripts/` (VERIFIER_RULES §3).
4. Merge only when the unit ledger is PASS or its gaps are agreed. Branch: a feature branch, not `main`.

## 12. Builder deliverables and REFERENCE_REQUESTS

Builders return the BUILDER_RULES §10 contract. Requests the planner has already identified (none is cited as fact until admitted):

- **REFERENCE_REQUEST R1.** Higham (2002), "Computing the nearest correlation matrix: a problem from finance", *IMA Journal of
  Numerical Analysis*. From recall; title, venue and year NOT verified. Needed for L09's nearest-correlation method. Confidence
  that the work exists: moderate. Architect to look up through Crossref before any use.
- **REFERENCE_REQUEST R2.** Litterman and Scheinkman (1991), "Common Factors Affecting Bond Returns", *Journal of Fixed Income*.
  From recall; NOT verified. Needed for L08's level, slope and curvature attribution. Confidence: moderate. Architect to look up.
- **REFERENCE_REQUEST R3.** A verified source for the Eckart-Young (low-rank) statement, if L06 states it. Needed for L06 only if the
  statement is written. Confidence: high that the theorem exists; the record is missing.
- **DATA_REQUEST D1 (B2).** A cleared H.15 multi-tenor CMT dataset (source URL `https://www.federalreserve.gov/releases/h15/data/FRB_h15_xml.zip`,
  the same release family as `ust_daily`), licence as quoted in `tools/data_sources.yaml`, transform: daily CMT yields for the tenors
  the architect selects (at least three for curvature). Series identifiers **to be read from the release XML by the builder or the
  architect; not typed here.**
- **GLOSSARY_REQUESTS (plain terms, Q4).** basis, span, rank, determinant, inner product, norm, eigenvalue, singular value, orthogonal
  matrix, trace, centred data matrix.
- **DAG_DEFECTS.** B1 (M4 concepts), B3 (AP2, M7, PR1 concepts). B4 is a rule, not a defect.
- **CONTRACT_CHANGE_REQUESTS.** None (no Atlas milestone).
- **NOTATION_REQUESTS.** None expected. Use standard KaTeX: \(\top\) for transpose, \(\Lambda\), \(\Sigma\), \(\mathbf{1}\). Confirm each
  against `notation/notation.json` before use (BUILDER_RULES §3.1-3.2).

## 13. Cards builder (Builder F, after A-D)

- `course/modules/M/M3/cards.json`, ids `M3-c001` upward, `lesson` in L01-L09, one card per definition, theorem statement, key formula,
  key result and misconception (BUILDER_RULES §7).
- Grade T for every theorem and derivation. A card whose result is a lab output carries `basis` naming the lab (for example
  `"basis": "Lab 3 (residuals)"`) and grade C, as the M1 cards did (`plans/M1-open-items.md`, Builder E).
- `cite` only for an empirical claim, with a verified key and a confirmed locator. M3 has few empirical claims; most cards have no `cite`.
- `check_pages.py` checks id prefix, lesson existence, grades and registry keys.

## 14. Honest gaps the pages must state

- L08's curriculum lab cannot be run with curvature on embedded data (B2) unless D1 is approved.
- Level-slope-curvature attributions are not sourced until R2 or a locator-level reading exists; they are grade C.
- The nearest-correlation method (L09) is a named method without a registry key (R1); its properties are stated as tested properties.
- The project's correlation matrices are SIMULATED. A real-data check is a rung-4 stretch.
- Labs print results for seeded inputs. Each lab's interpretation says the claim is about those inputs (scope rule, §1.1.4).

## Architect decisions (2026-10-28, binding)
B1/Q2: covariance is the formula X'X/(T-1) with no concept link and no M4 prerequisite. B2/Q1: the L08 lab uses a SIMULATED generated yield-curve panel (three or more tenors), labelled SIMULATED; record a DATA_REQUEST for a cleared multi-tenor H.15 dataset in plans/M3-open-items.md; do not invent series IDs. B3: closed-form weights with no concept name. B4 confirmed. Q3: NumPy yes. Q4: basis, span, rank, determinant, inner product, norm, eigenvalue, singular value and trace are plain prose. Q5: 9 lessons / 105 h and a 45 h project. Q6: `covariance_doctor.py`, signatures as in plan 5.2. Q7: not adversarial. Q8: SIMULATED instances only (no rung-4 real-data variant). Q9: do not add used_by; cite only axler2024linear and strang2023introduction. Q10: PCA on a generic symmetric PSD matrix of centred data. Higham and Litterman-Scheinkman are REFERENCE_REQUESTS only: not cited, not named in learner text.
