# M7 build plan: Optimization (2026-10-28)

Unit: **M7 · Optimization** · tier F · 110 h · prerequisites M2, M3 · no Atlas milestone · grading `autograder` ·
output directory `course/modules/M/M7/` (part code `M`, title "Mathematics", `curriculum/01-foundations.yaml:70-71`).
Planner: Haiku, plan only. No lesson content, no git operations, no ledger. Executors: Haiku builders, then independent
Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence: every curriculum statement cites `file:line` read during planning. Anything not in the curriculum is marked
as such. Architect decisions on AC4 and M1 are reused where the same issue arises (cited in §9 and §10).

**Status: one blocking DAG question (B1, §3) must be decided before the L06 builder and the project builder start.
Hours do not conflict with the tool rules (§5).**

## 1. Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part M, code `M`, title "Mathematics"; studio STUDIO-M requires `[M7, M8]` | `curriculum/01-foundations.yaml:70-76` |
| M7 id, title "Optimization", tier F, hours 110, prereqs `[M2, M3]` | `curriculum/01-foundations.yaml:298-302` |
| M7 core text: convex sets and functions, Lagrange multipliers, KKT conditions, duality, quadratic programming, dynamic programming and the Bellman equation | `curriculum/01-foundations.yaml:303-305` |
| M7 introduces 10 concepts (one per entry) | `curriculum/01-foundations.yaml:306-316` |
| M7 sources (free text): Boyd & Vandenberghe (2004); Stokey & Lucas (1989) | `curriculum/01-foundations.yaml:317-319` |
| M7 lab (the curriculum lab): "Efficient frontier via QP with and without a short-sale constraint." | `curriculum/01-foundations.yaml:320` |
| M7 project "Constrained allocator": build a mean-variance allocator supporting box, turnover and sector constraints; verify KKT at every returned solution | `curriculum/01-foundations.yaml:321-325` |
| Deliverable "Tested module plus KKT-certificate output." | `curriculum/01-foundations.yaml:326` |
| Project grading `autograder` (so no rubric, no exemplars, no question bank) | `curriculum/01-foundations.yaml:327` |
| M7 has no `debate` key, so no debate brief is required | `curriculum/01-foundations.yaml:298-327` (absent; `check_pages.py` line 412 keys on `debate`) |
| No Atlas milestone names M7 (the 20 atlas entries are in `curriculum/meta.yaml`; grep finds no `M7`) | `curriculum/meta.yaml` (atlas block); the M7 block has no `atlas:` key, `curriculum/01-foundations.yaml:321-327` |
| JSON row for M7 mirrors the YAML (hours 110, prereqs, 10 introduces, sources, lab, grading autograder) | `curriculum/curriculum.json:6540-6578` (hours at 6543) |
| Rendered CURRICULUM.md line for M7 | `CURRICULUM.md:250` (`- **M7 · Optimization** · F · 110 h · ← M2, M3`) |
| STUDIO-M is a U-tier studio of 60 h, `autograder`, requiring M7 and M8 | `CURRICULUM.md:210`; `curriculum/01-foundations.yaml:74-77` |
| Downstream modules that list M7 as a prerequisite (for context, not for M7's build) | `curriculum/02-economics-finance-core.yaml:128, 195`; `curriculum/03-markets.yaml:227, 649`; `curriculum/04-quant.yaml:627` |
| Topological position: after M2 and M3 (index 14 in `topological_order`) | `curriculum/curriculum.json` `topological_order` (`M7` at index 14; `M2` at 5, `M3` at 6) |
| Registry key `boyd2004convex`: verified, Crossref monograph, Boyd & Vandenberghe, year 2004, `years` [2004, 2013], `used_by: ["M7"]` | `references/references.json:3648` |
| Registry key `stokey1989recursive`: verified, Crossref monograph, authors Stokey, Lucas, Prescott, year 1989, `used_by: ["M7"]` | `references/references.json:21295` |

Conclusion on the curriculum: the entry is complete and internally consistent. It names no data, no Atlas milestone,
no debate and no rubric. Everything the module needs beyond that is a planning choice, listed in §10.

## 2. Prerequisite closure and what may be used without definition

Computed from `curriculum/curriculum.json` (`prereqs`, `introduces`): closure of M7 = `{P0.1, M1, M2, M3}`.

| Closure module | Concepts it introduces (usable without definition, linkable) | Locator |
|---|---|---|
| M1 (F, 100 h, prereq P0.1) | `quantifiers`, `direct-proof`, `proof-by-contradiction`, `mathematical-induction`, `exponential-and-logarithm`, ... | `curriculum/01-foundations.yaml:87-110` |
| M2 (F, 300 h, prereq M1) | `limit`, `derivative`, `taylor-theorem`, `definite-integral`, `partial-derivative`, `gradient`, `jacobian`, `hessian`, `multiple-integral`, `implicit-function-theorem`, `envelope-theorem`, `finite-difference-derivative`, `automatic-differentiation` | `curriculum/curriculum.json` (module M2 `introduces`) |
| M3 (F, 150 h, prereq M1) | `vector-space`, `linear-map`, `eigendecomposition`, `spectral-theorem`, `singular-value-decomposition`, `positive-semidefinite-matrix`, `orthogonal-projection`, `least-squares-projection`, `principal-component-analysis`, `level-slope-curvature`, `nearest-correlation-matrix`, `eigenvalue-clipping` | `curriculum/curriculum.json` (module M3 `introduces`) |
| P0.1 (F, 6 h) | `evidence-grade`, `paper-anatomy`, `identification`, `robustness-check`, `replication`, `steelmanning`, `project-ladder`, `prerequisite-dag`, `atlas-platform`, `citation-registry`, `notation-conventions` | `curriculum/01-foundations.yaml:15-26` (P0.1 `introduces` block) |

Concepts the module needs that are **outside** the closure (a link to any of them fails `check_dag.py`; prose use is
not caught by the tool, see §8 T3):

| Concept id | Owner | Why it is tempting | Outside closure because |
|---|---|---|---|
| `covariance-matrix`, `variance`, `correlation`, `multivariate-normal` | M4 (`curriculum.json` concepts) | mean-variance needs a covariance input; the curriculum lab needs one | M4 is not in M7's closure (**B1**, §3) |
| `dynamic-programming` | CS2 | the core text says "dynamic programming" (`:303-305`) | CS2 is not in the closure; its concept is algorithmic, not the economic recursion |
| `contraction-mapping`, `bellman-operator-contraction`, `value-function-iteration`, `policy-iteration` | M5, M5, M5, SC6 | the infinite-horizon Bellman equation is usually proved by contraction | M5 and SC6 are not in the closure (§3, B2) |
| `efficient-frontier` | AP2 | the curriculum lab is titled "Efficient frontier" (`:320`) | AP2 is not in the closure; use the words as prose, not a link |
| `newtons-method` | M8 | a natural solver for the KKT system | M8 is not in the closure |
| `convexity` | FI1 | name collision with `convex-function` (M7) | different concept; do not link |

Useful closure tools that M7 should use, since they are already in the closure: `hessian`, `gradient`,
`implicit-function-theorem`, `envelope-theorem` (M2), `positive-semidefinite-matrix`, `eigendecomposition`,
`spectral-theorem`, `orthogonal-projection` (M3), `mathematical-induction` (M1, for backward induction in L07), and
`limit` (M2; the M1 Q1 problem about `limit` does not arise for M7).

## 3. DAG problems and blocking issues

**B1 (blocking for L06 and the project, decision needed before those builders start).** The mean-variance QP
(`mean-variance-optimization`, `curriculum/01-foundations.yaml:313`) needs a covariance input, and the curriculum lab
(`:320`) needs expected returns and a covariance matrix. The covariance concept is `covariance-matrix`, owned by M4
(`curriculum.json` concept index). M4 is not in M7's closure (§2). The planner cannot change `prereqs`.
- Option (a) **recommended**, the same pattern the architect chose for AC4 Q1/Q2 (`plans/AC4-build-plan.md`, architect
  decisions): M7 takes a given symmetric positive-definite matrix \(\Sigma\) and a given vector \(\mu\) as inputs. The
  pages state that M7 does not estimate them and that estimation is outside the unit. The word "covariance" may appear
  in prose only in that sentence, with no link. The generator produces \(\Sigma\) as \(A^{\top}A + \varepsilon I\), which
  uses only `positive-semidefinite-matrix` and `eigendecomposition` (M3).
- Option (b): a curriculum change adding M4 to M7's `prereqs`. This is an architect or curriculum decision; the planner
  does not propose it, because it would also change M7's hours and the credential maps (`curriculum/meta.yaml`).
- Option (c): a forward link to M4. Forbidden by BUILDER_RULES §1.10 and `check_dag.py`.

**B2 (decision, not blocking L01 to L05 or L07).** The infinite-horizon Bellman equation (`bellman-equation`,
`:313-316`, core `:305`) needs the contraction property to prove existence and uniqueness of the value function.
The contraction concept is M5's (`bellman-operator-contraction`, `contraction-mapping`), so it cannot be linked.
- Option (a) **recommended**: L08 proves the finite-horizon recursion completely (induction, which is in closure) and
  states the infinite-horizon result only as a cited statement from `stokey1989recursive`, with the locator marked
  "not confirmed" and the grade at most C. Nothing is attributed to a locator that has not been read. The lab runs value
  iteration on a finite-state problem and reports the error numerically, with the convergence claim stated as an
  observation, not a proof (the same treatment as M1 Q1 for the compounding limit).
- Option (b): drop the infinite-horizon statement. Option (c) forward link: forbidden.

No other DAG defect was found. Every concept M7 introduces appears in exactly one row of the outline (§4), and no
closure concept is used in a way that needs a later definition.

## 4. Outline and file ownership (proposal; the architect fixes it)

Lesson hours are derived, not guessed. The hub declares lessons + project = 110 h (`check_pages.py` lines 337-338).
Project = 33 h (30 %, inside the 10-40 % band at `check_pages.py` line 339). Lessons = 77 h, split across 8 lessons of
9 or 10 h, inside the 6-12 h rule (`check_pages.py` line 227). Eight lessons follow the M1 and AC4 pattern and keep each
concept group inside one lesson, with the proof tools first.

| Lesson | Title (working) | Concepts it defines (each once) | Hours | Lab twin id | Owner |
|---|---|---|---|---|---|
| L01 | Convex sets and convex functions | `convex-set`, `convex-function` | 9 | `lab-M7-L01-1`: convexity inequalities on a grid for a PSD and an indefinite quadratic; Hessian eigenvalue sign | Builder A |
| L02 | Lagrange multipliers for equality constraints | `lagrange-multiplier` | 9 | `lab-M7-L02-1`: minimum-variance weights under a budget constraint; gradient parallel to the constraint normal, checked to tolerance | Builder A |
| L03 | The KKT conditions | `kkt-conditions` | 10 | `lab-M7-L03-1`: KKT residuals (stationarity, primal, dual, complementary slackness) for a two-asset problem with a non-negativity constraint, at the active and the inactive solution | Builder B |
| L04 | Lagrangian duality | `lagrangian-duality` | 10 | `lab-M7-L04-1`: dual function on a grid; weak duality holds; the duality gap is zero for the convex QP under Slater's condition | Builder B |
| L05 | Quadratic programming | `quadratic-programming` | 10 | `lab-M7-L05-1`: equality-constrained QP solved from its KKT linear system in exact `Fraction` arithmetic, checked against brute-force active-set enumeration | Builder C |
| L06 | Mean-variance optimization and linear portfolio constraints | `mean-variance-optimization`, `linear-portfolio-constraints` | 10 | `lab-M7-L06-1` (**the curriculum lab**): efficient frontier as a QP with and without the short-sale constraint, on a SIMULATED \(\mu\), \(\Sigma\) (B1) | Builder C |
| L07 | The principle of optimality and finite-horizon dynamic programming | `principle-of-optimality` | 9 | `lab-M7-L07-1`: backward recursion on a finite-state toy problem, checked against brute-force enumeration of plans | Builder D |
| L08 | The Bellman equation | `bellman-equation` | 10 | `lab-M7-L08-1`: finite-horizon Bellman recursion, and value iteration on a finite-state problem with the error reported (B2) | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split | none | - | none | Builder A |
| project | Constrained allocator (`autograder`) | none | 33 | `lab-M7-project-1` (rung 1), `lab-M7-project-2` (rung 2, completion), `lab-M7-project-3` (rung-3 check) | Builder E |
| grader | `grader/reference.py`, `starter.py`, `instance.py`, `test_project.py` | none | - | none | Builder E |
| cards | `cards.json` from L01-L08 | none | - | none | Builder F (after A-D) |

Totals: lessons 9+9+10+10+10+10+9+10 = 77 h; project 33 h; unit 110 h. Matches `curriculum/01-foundations.yaml:301`.

Concept coverage: 2+1+1+1+1+2+1+1 = 10 concepts, each in exactly one row, matching the ten entries at
`curriculum/01-foundations.yaml:307-316`.

Ordering: L02 before L03 (KKT uses the multiplier); L01 before L03 (convexity makes KKT sufficient); L03 before L04
(duality uses KKT); L05 uses L03 and L04; L06 uses L05 (the QP) and the constraint forms from L03; L07 before L08 (the
Bellman equation is the principle of optimality applied recursively). No lesson links a definition in a later lesson.

Concept group rule for Builder B and C: `lagrange-multiplier` is defined in L02 and may be used in L03 by link
`href="L02.html#def-lagrange-multiplier"`; a lesson never links a concept defined later.

## 5. Hours budget

**Lessons (77 h).** Each lesson declares `data-hours` (6-12, `check_pages.py` line 227). Hub
`<main data-hours-lessons="77" data-hours-project="33">` (sums to 110; `check_pages.py` lines 337-342).

**Project (33 h, 30 %).** `check_projects.py` requires the components to sum to the declared total and every row to
carry a one-line rationale (`tools/check_projects.py`, time-budget block in `check_unit`, and its docstring).

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate a solved 3-asset QP) | 2 | One fully solved instance, annotated at each step |
| Rung 2, completion problem (fill the stationarity and dual-sign lines) | 3 | Eight to ten lines with blanks, graded instantly |
| Core solver: equality and inequality QP, active-set search | 10 | The main algorithmic work; tests in §7 check it |
| Linear constraints: box, sector, turnover as auxiliary variables | 6 | Linearization of \(|w_i - w_{0,i}|\) (see Q5) and sector sums |
| KKT certificate output and the test suite | 7 | Certificate fields, residuals, edge-case tests |
| Self-check against the grader and a short write-up of the certificate | 5 | Run the suite; explain each residual in one paragraph |
| **Total** | **33** | Equals `data-hours-project` on the hub |

## 6. Hub (index.html, Builder A)

- `<main data-hours-lessons="77" data-hours-project="33">`.
- 4-8 measurable objectives (verbs such as "derive", "check", "solve", "certify"); prerequisite links to M2 and M3 with
  concept links `href="../../../concepts.html#<id>"`; M1 and P0.1 are reached through them.
- Placement diagnostic: `<section class="quiz" id="placement" data-unit="M7" data-page="placement" data-mastery="0.8">`,
  the M1 bar (`course/modules/M/M1/index.html` line 67). At least two `data-skill` items test what rungs 1-2 teach (the
  worked example's QP and the completion step's KKT lines); the others test M2 and M3 (gradients, Hessians, PSD
  matrices, eigenvalues).
- Lesson map linking L01-L08 (`data-progress-key="M7/Lnn"`, as in `course/modules/M/M1/index.html` lines 151-158).
- Project ladder: `ol.ladder` with four `span.rung-title` entries in order (`check_projects.py` requires the four rung
  titles, in order: "Worked example", "Completion", "Independent", "Stretch").
- Tier F keeps rungs 1-2 at full length (BLUEPRINT §4: minimum only from tier M upward).

## 7. Project ladder and grader design (Builder E)

**Grading: `autograder` only** (`curriculum/01-foundations.yaml:327`). No rubric, no exemplars, no question bank, and no
self-assessment form are required. The spec must say "autograder" in its grading entry (`check_projects.py`,
`GRADING_WORDS` and `grading_problems`, lines 38-51). A rubric would be extra scope, so none is planned.

### 7.1 Ladder (BUILDER_RULES §5.1, the M1 and AC4 pattern)

1. **Rung 1, worked example** (`lab-M7-project-1`): a fully solved 3-asset problem with box bounds, every KKT line
   annotated with why it holds.
2. **Rung 2, completion** (`lab-M7-project-2`, `class="lab completion"`): the same problem with the stationarity
   line and two dual-sign lines replaced by `___`; the twin is the completed solution (`run_labs.py` rule for completion
   labs).
3. **Rung 3, independent project** (graded): `constrained_allocator.py` (Q4), autograded by `grader/test_project.py`.
   `lab-M7-project-3` is the rung-3 check that runs the reference's certificate on one seed.
4. **Rung 4, stretch** (open-ended, not graded): for example, a parametric frontier traced by changing \(\gamma\), with
   the multiplier as the shadow price of the budget constraint (the envelope theorem, `envelope-theorem`, M2, usable).

### 7.2 Specification (`project.html`)

The spec (`dl.spec`, with `dt` terms "Context", "Inputs", "Required outputs", "Constraints", "Grading") must state:

- **Objective convention (Q3).** Minimize \( \tfrac{\gamma}{2} w^{\top}\Sigma w - \mu^{\top} w \) over \(w \in \mathbb{R}^n\),
  with \(\gamma > 0\), \(\Sigma\) symmetric positive definite, \(\mu\) given, and all returns in one stated period.
- **Constraints.** Budget \( \mathbf{1}^{\top} w = 1 \); box \( l \le w \le u \) (with the long-only case \(l = 0\));
  turnover \( \sum_i |w_i - w_{0,i}| \le \tau \); sector caps \( \sum_{i \in S_k} w_i \le c_k \).
- **Certificate.** For every returned solution: primal residual, stationarity residual \( \|\nabla f + \sum \lambda_i \nabla g_i
  + \nu \mathbf{1}\| \), dual feasibility (multipliers of inequality constraints \(\ge 0\)), and complementary slackness
  \(|\lambda_i g_i(w)|\). The tolerance is stated in the spec (proposed \(10^{-8}\) after scaling; Q6).
- **Failure behaviour.** Infeasible constraints, a non-positive-definite \(\Sigma\), or a wrong-shaped input raise
  `ValueError` naming the violated condition. The spec names `ValueError` only for these cases (see §7.4 on exception
  types).
- **Reading list:** `ol.reading-list` with `li data-cite="boyd2004convex"` and `li data-cite="stokey1989recursive"` (see §9
  for what each may support).
- **Inputs.** Generated only (SIMULATED, §9). No dataset, no MANIFEST entry.

### 7.3 Grader files

- `grader/instance.py`: `make_instance(seed: int) -> dict[str, Any]`, deterministic. It generates \(n\) in {3, 4, 5} assets,
  \(\mu\), \(\Sigma = A^{\top}A + \varepsilon I\) with \(\varepsilon > 0\) (so \(\Sigma\) is positive definite by the M3
  criterion), an initial portfolio \(w_0\), box bounds, sector labels with caps, and \(\tau\). Every instance is feasible,
  checked inside the generator. The docstring says **SIMULATED: generated inputs, not market data.** Seeds 0-49 must
  change the answers (which constraints bind, the active set), not only the labels (BUILDER_RULES §5.3).
- `grader/reference.py`: the full solution. It passes every test on seeds 0-49 (`run_graders.py --seeds 0-49`).
- `grader/starter.py`: stubs that raise `NotImplementedError`. The starter must fail the suite (`run_graders.py` checks
  this).
- `grader/test_project.py`: pytest suite, property and number checks:
  - KKT certificate: each residual below the spec tolerance on every seed in the suite; \(\lambda_i \ge 0\) for
    inequality constraints.
  - Objective value equals the reference optimum to a stated relative tolerance. Because \(\Sigma\) is positive definite,
    the minimizer is unique, so the test may compare \(w\) itself, not only the objective.
  - Budget and box are satisfied; turnover is at most \(\tau\) to tolerance; sector caps hold.
  - Edge cases: with no binding constraint the answer equals the unconstrained solution \(w = \frac{1}{\gamma}\Sigma^{-1}(\ldots)\)
    plus the budget correction (closed form); with \(\tau = 0\) the solution is \(w_0\) when \(w_0\) is feasible.
  - Invalid input (non-PD \(\Sigma\), infeasible constraints) raises `ValueError` (the one exception type the spec names).
  - Failure messages name the property violated and hint at the concept (for example "stationarity fails: check the sign
    of the multiplier term"). They never print the answer.
- Each test finishes in under 5 s in Pyodide, the suite in under 60 s (BUILDER_RULES §5.3.4).

### 7.4 Exception and acceptance rules for the suite (binding)

1. A test demands a specific exception type **only** for a condition the page names. The spec names `ValueError` for the
   three conditions in §7.2. For every other invalid case, the suite accepts any exception that carries a message, and
   it fails only if the solver returns a silent wrong answer.
2. **Five alternative correct implementations must pass.** The suite must accept any correct method, so it checks
   properties and values, never the iterate path or one solver's internal fields. The verifier writes five independent
   correct solvers, each a different method, for example: (1) active-set enumeration in exact `fractions.Fraction`
   arithmetic; (2) projected gradient with a tight stopping rule; (3) ADMM; (4) log-barrier interior point; (5) a dual
   ascent on the Lagrangian of §L04. Each must pass the whole suite on seeds 0-49. Where they are stored is Q7.
3. Mutants (VERIFIER §2.6, at least three, each must fail a test). Suggested by the builder, written by the verifier:
   1. the non-negativity constraint dropped (short sales allowed where the spec forbids them);
   2. turnover measured from the wrong reference, for example \(w\) instead of \(w_0\);
   3. dual sign flipped (\(\lambda_i \le 0\) accepted), so KKT dual feasibility is never tested;
   4. objective with \(\tfrac12 \gamma\) replaced by \(\gamma\) in the quadratic term (a factor-2 convention error);
   5. a hard-coded answer for seed 0.

   Each mutant is written as a complete module in `ledgers/M7/mutants/<name>.py` with a docstring first line naming the
   error; `tools/mutate_graders.py --unit M7 --seeds 0-9` runs them.
4. **Dual mode.** The identical suite runs in Pyodide and under local pytest (`--assert=plain -W error`). Any numpy use
   needs `data-packages="numpy"` on the lab or panel that uses it, as `course/modules/AP/AP1/project.html` line 53 does.

### 7.5 Grader panel (`project.html`, AP1 pattern: a unit-local solution file, not an Atlas path)

```html
<section class="grader-panel" id="grader" data-unit="M7" data-grader="grader/" data-suite="test_project.py"
         data-support="instance.py" data-solution="constrained_allocator.py" data-starter="starter.py"></section>
```

`check_projects.py` requires `data-unit`, `data-grader`, `data-suite`, `data-support`, `data-solution`, `data-starter` and
the files `reference.py`, `instance.py`, the suite and the starter (`tools/check_projects.py` lines 122-135). The Atlas
branch does not apply (no `atlas:` key).

## 8. Labs, figures, data and writing rules (binding for M7)

### 8.1 Labs

- Code lives once in its twin `tests/labs/M7/lab-M7-Lnn-1.py` (and `lab-M7-project-n.py`). The page carries
  `@@LAB:<file>@@` and `@@OUT:<file>@@` and `tools/embed_labs.py` fills them. Never type an expected output.
- **Labs call `main()` at top level**, as the M1 and AC1 twins do (`tests/labs/M1/lab-M1-L04-1.py` ends with a bare
  `main()`; AC1 twins end the same way). `run_labs.py` runs each twin as `python -I -W error` (`tools/run_labs.py`
  lines 54-56) and the page code is the same text, so an `if __name__ == "__main__":` guard would print nothing in
  Pyodide. Do not use the guard.
- Seeded RNGs only (a fixed `SEED` constant); no network; under 10 s in Pyodide.
- Each lab's hypothesis is stated before the code runs, and the hypothesis must match what the code prints (for example,
  if the hypothesis says "residuals below 1e-9", the printed residual column must show that).
- Each lab's interpretation says what the output does not show (for example, a finite grid does not prove optimality).
- Solvers in labs and in the reference: prefer `fractions.Fraction` (exact KKT solves for small \(n\)) or float with an
  explicit tolerance stated on the page. Q6.
- Completion lab (`class="lab completion"`): every line equals the twin's line or contains `___`.
- Ruff and mypy strict apply to the twins (`tests/labs/M7`, `course/modules/M/M7/grader`).

### 8.2 Numbers, scope and attribution rules (from the AC2, AC1, M1, AC4 and CF1 verification rounds)

1. **Numbers recomputed from unrounded values.** A percentage, ratio or difference in prose is computed from the
   unrounded value, then rounded for display. A rounded number is never fed back into a later computation.
2. **Lab statements match code and output.** Every "shows", "confirms" or "equals" claim names the printed line that
   carries it. A claim with no printed line is removed.
3. **Scope words need a computation.** "every", "always", "all", "never", "any", "for each" are allowed only where the
   text names the set checked and the code checks that set. "KKT holds at every returned solution" is allowed only as
   "on each of the seeds 0-49 in the suite". Words without a computation behind them are deleted.
4. **Attribute nothing unread.** Boyd & Vandenberghe and Stokey, Lucas & Prescott are cited only for a claim whose
   locator the builder has confirmed in a source that reproduces it. Otherwise the claim is a derivation on the page
   (grade T with a full proof) or is stated as unconfirmed, at grade C or lower. No locator is invented.
5. **Define before use.** "feasible set", "active set", "dual function", "Slater condition", "shadow price" and "KKT
   certificate" are defined at their first appearance in the lesson where they are needed. A `<dfn>` is used only for
   the ten concepts of §4. Undeclared terms (see §2 table) are plain prose, with no `<dfn>` and no link (AC4 architect
   decision Q4).
6. **Proposition hypotheses explicit.** Each proposition or theorem states every hypothesis. Required for:
   - KKT sufficiency: \(f\) and \(g_i\) convex, \(h\) affine, the point feasible, and the multipliers satisfying the KKT
     conditions; conclusion: the point is optimal.
   - KKT necessity: an additional constraint qualification (Slater's condition for convex problems, stated as a
     hypothesis, not assumed silently).
   - Strong duality for the convex QP: Slater's condition.
   - Equality-constrained QP closed form: \(\Sigma\) positive definite (so the KKT matrix is nonsingular, stated and
     checked in the code).
7. **Integer cents for money.** M7 has no money in the curriculum entry. If the spec adds a notional or a trade list
   in currency, every amount is an integer number of cents, with largest-remainder rounding of trades, and the grader
   checks that the rounded trades sum to the rounded total. Q8. Without that spec change, no currency amounts appear.
8. **No horizontal scroll at 360 px.** Every table is either narrow enough to fit at 360 px or is wrapped in a
   block that wraps its cells. KaTeX display equations are split across lines where needed. Figures use
   `course/assets/js/chart.js` and draw at the container width.
9. **Labels legible at 360 px.** Figures follow BUILDER_RULES §6.4; no figure is needed unless it teaches a mechanism
   (for example, the feasible polytope with the KKT point, or the frontier). If a figure is drawn, its caption states
   the one thing to see, and it is labelled "computed from the formula; no data" (M1 plan §6, point 6).
10. **Banned phrases** (`tools/check_pages.py` `BANNED`, lines 58-72+): no TODO, TBD, lorem, "for brevity", "details
    omitted", "beyond the scope", "left as an exercise", "you can add more", "it is important to note", "studies show",
    "experts agree", "it is well known", "obviously", "clearly".
11. Lessons: "Why it matters" at most 120 words (`check_pages.py` line 244); at least 3 misconceptions, each with the
    wrong belief and why it is wrong (`check_code`, misconception block, around line 280); problem sets with at least 3
    problems in each of Mechanics, Proof, Empirical and Research tiers, each with a `<details class="solution">` of at
    least 15 words (`check_code`, problem-set block, around lines 286-295); a quiz of 8-15 items with explanations
    (`check_code`, quiz block, lines 299-309). An "Empirical" problem in M7 uses generated data and says SIMULATED.

## 9. Registry keys the module may cite, and real-data policy

### 9.1 Keys

| Key | Status | Use in M7 | Flag |
|---|---|---|---|
| `boyd2004convex` | verified, Crossref monograph (`references/references.json:3648`), `used_by ["M7"]` | convex sets and functions (L01), KKT and duality (L03, L04), QP (L05). Cite with a `data-locator` only when the locator is confirmed; otherwise cite for the statement of a general result the page proves itself. | Record year 2004, `years` [2004, 2013]. The page cites the 2004 printing as the curriculum string does (`:317-319`); Q9 |
| `stokey1989recursive` | verified, Crossref monograph (`references/references.json:21295`), `used_by ["M7"]` | the Bellman equation and the recursive formulation (L07, L08), and only the infinite-horizon statement in L08 (B2) | Record authors Stokey, Lucas, Prescott; curriculum string "Stokey & Lucas" (`:317-319`). Q9 |
| `markowitz1952portfolio` | verified (`used_by ["AP2"]`) | would be the natural historical source for mean-variance (L06) | Not curriculum-listed for M7. Use needs architect approval and a confirmed locator (Q10). Default: not cited |
| `pham2009continuous` | verified (`used_by ["SC6"]`) | none planned | Not curriculum-listed for M7. Not cited |
| `velleman2019prove` | verified (`used_by ["M1"]`) | proof technique in L07 induction | Only if the architect approves; not curriculum-listed for M7; the M1 pages cite it with no locator read (`plans/M1-open-items.md`). Default: not cited |

Registry rule: `check_pages.py` accepts only keys whose `status` is `verified` (`tools/coursekit.py` `registry_keys`,
line 164-166). A key is cited by its record only; the builder never types a title, year, author list, page or
coefficient from memory.

### 9.2 REFERENCE_REQUESTS

- None required by the curriculum. Both curriculum sources are registered.
- Optional, architect decision (Q11): the original KKT papers (Karush's 1939 thesis; Kuhn & Tucker 1951) are not in the
  registry. The planner does not propose attributing KKT to them. If the architect wants the attribution, the request is
  made with a DOI or a stable URL found through Crossref, never from memory.

### 9.3 Real-data policy

- **No real data.** M7 is optimization theory and algorithms. Nothing in the curriculum entry calls for market data
  (`curriculum/01-foundations.yaml:298-327`). No `data-files` attribute on any lab. No MANIFEST entry. No DATA_REQUESTS.
- Every instance, \(\mu\), \(\Sigma\), \(w_0\), sector map and cost figure is generated from the seed, labelled
  **SIMULATED** in the lab, in the grader docstring and on the project page (BLUEPRINT §5.3; BUILDER_RULES §1.7).
- An example that uses a real asset (for example, a named ETF) is not allowed, because the inputs would look like real
  market data.

## 10. Atlas milestone

- **None.** No atlas entry names M7 (`curriculum/meta.yaml`, atlas block, grep returns no `M7`), and the M7 entry has no
  `atlas:` key (`curriculum/01-foundations.yaml:321-327`). No `atlas/<A-ID>.contract.md` is needed and none is drafted.
  The Atlas branch in `check_projects.py` (lines 144-146) does not run.
- Q4 asks the architect to confirm that the solution file is unit-local (`constrained_allocator.py`), not an Atlas file.

## 11. Cards (Builder F, after A-D)

- `course/modules/M/M7/cards.json`, ids `M7-c001` upward, `lesson` in L01-L08 (`check_pages.py` lines 366-400).
- One card per definition (10 concepts), theorem statement, key formula (KKT conditions, the duality identity, the
  Bellman recursion), the worked-example result and each misconception (BUILDER_RULES §7).
- Grade T for each theorem and each derived formula, with `"basis"` naming the lab or problem that establishes a numerical
  result, for example `"basis": "Lab 3, Problem E2 (simulation)"`. `cite` lists a registry key only for an empirical
  or historical claim; M7 has none, so `cite` is empty.
- The `check_cards` rule requires each non-T card to have `cite` or `basis`. Every card needs `front` and `back` (this
  is checked in the code, not in BUILDER_RULES §7, which also lists `grade`, `lesson`, `cite`).

## 12. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

```bash
.venv/bin/python tools/check_pages.py --unit M7          # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit M7
.venv/bin/python tools/check_projects.py --unit M7
.venv/bin/python tools/run_labs.py --unit M7             # --page L04 for one lesson
.venv/bin/python tools/run_graders.py --unit M7 --seeds 0-49
.venv/bin/python tools/embed_labs.py course/modules/M/M7/L01.html            # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/M/M7/L06.html --refresh lab-M7-L06-1
.venv/bin/ruff check tests/labs/M7 course/modules/M/M7/grader && .venv/bin/ruff format --check tests/labs/M7
.venv/bin/mypy tests/labs/M7 course/modules/M/M7/grader                    # strict; confirm the paths first
.venv/bin/python tools/mutate_graders.py --unit M7 --seeds 0-9             # verifier only
```

Notes:
- `check_pages`, `check_dag` and `check_projects` accept `--unit` (`tools/check_pages.py` line 429, `tools/check_dag.py`
  line 89, `tools/check_projects.py` line 159). `run_labs.py` takes `--unit` and `--page`; `run_graders.py` takes
  `--unit` and `--seeds`; `mutate_graders.py` takes `--unit` and `--seeds` (plan M1 §Commands, read in session).
- `page_smoke.py` is not run by builders (timing-sensitive). Verifiers run it on a quiet machine.
- The five alternative implementations (§7.4) are not run by any command above; see T2.
- Commands are the repo's own; the planner did not execute them.

## 13. Tooling assumptions that do not hold for this module type (flagged)

- **T1. No Atlas milestone.** `check_projects.py` Atlas branch does not apply (fine). The grader panel must use a
  unit-local solution file (AP1 pattern). `run_graders.py` takes the solution path from the panel (`tools/run_graders.py`
  lines 51-61 and its docstring), so this holds.
- **T2. `run_graders.py` tests only the reference solution.** It copies `data-solution` into a workspace and runs the
  suite (`tools/run_graders.py` lines 51-61). It has no mode for five alternative solutions. The five alternative
  implementations (§7.4.2) therefore need either a pytest module under `tests/` that copies each alternative into a
  temporary workspace, or an extension of `run_graders.py`. Both are tooling changes, not a builder decision (Q7).
- **T3. `check_dag.py` cannot see prose use.** Its docstring says "A concept used by name without a link cannot be
  detected statically; the verifier reads for it" (`tools/check_dag.py` lines 5-19). So a sentence in L06 that names
  "covariance matrix" as a concept passes the tool and fails only on a verifier's reading. The §2 table is the list the
  verifier reads against.
- **T4. The grader panel parser fails with an exception rather than a FAIL row when `data-support` is missing.**
  `tools/check_projects.py` line 131 calls `grader.get("data-support").split()` with no `None` guard. The panel must carry
  `data-support` (it does, §7.5). Recorded as a tooling defect for the architect; not a blocker.
- **T5. No rubric checks.** Because the grading is `autograder`, the rubric checks in `check_projects.py` (lines 138-139)
  do not run. No exemplars are needed (correct for this unit).
- **T6. `grader/reference.py` is excluded from deployment** (BLUEPRINT §7). The five alternates in T2 must not be placed in
  `course/` for the same reason.
- **T7. Concept index.** `check_dag.py` uses `concept_owner()` for the whole curriculum. The M7 pages may only define
  the ten concepts of §4; a `<dfn>` for `covariance-matrix` or `dynamic-programming` fails the tool (the `<dfn>` loop
  in `check_unit`, `tools/check_dag.py`).
- **T8. Hub hours.** `check_hub` computes the lesson sum from the `data-hours` declared on each lesson page
  (`check_pages.py` lines 341-342). Every lesson must declare `data-hours` exactly as the hub's split implies.

## 14. Open questions for the architect (numbered)

1. **B1, covariance input.** Confirm option (a): \(\mu\) and \(\Sigma\) are given inputs, M7 does not estimate them, and
   the word "covariance" appears only in that disclaimer with no link. This blocks L06 and the project. Option (b) is a
   curriculum change (add M4 to `prereqs`).
2. **B2, infinite-horizon Bellman.** Confirm option (a): L08 proves the finite-horizon recursion and states the
   infinite-horizon result only as a cited, unconfirmed-locator statement at grade C or lower. Or option (b): omit it.
3. **Objective convention and units.** Confirm the objective \(\tfrac{\gamma}{2}w^{\top}\Sigma w - \mu^{\top}w\) with one
   stated period and no annualization (the curriculum fixes neither, `curriculum/01-foundations.yaml:320-325`).
4. **Frozen interfaces.** Freeze the grader interface before builders start (AC4 Q8 precedent): `make_instance(seed:
   int) -> dict[str, Any]` (keys to be listed in the spec), and `allocate(instance: dict[str, Any]) -> dict[str, Any]`
   returning `weights`, `multipliers` and `certificate`. Confirm the file name `constrained_allocator.py` and that the
   solution file is unit-local (no `atlas/` path, §10).
5. **"Turnover" as a linear constraint.** The curriculum says "linear portfolio constraints (box, turnover, sector)"
   (`curriculum/01-foundations.yaml:313`). The turnover constraint \(\sum_i |w_i - w_{0,i}| \le \tau\) is convex and
   piecewise linear, but it is linear only after introducing \(t_i \ge \pm(w_i - w_{0,i})\), \(\sum_i t_i \le \tau\). Confirm
   that M7 teaches this linearization (the planner recommends yes) and that the spec states it.
6. **Numeric policy.** Exact `Fraction` solves for small \(n\) (\(n \le 5\)) in labs and tests, or float with a stated
   tolerance (proposed \(10^{-8}\) after scaling)? Confirm, and confirm that `numpy` is used only with `data-packages`.
7. **Five alternative implementations.** Confirm where they live (proposed: `tests/graders/M7/`, run by a pytest module
   that copies each one into a temporary workspace, so `course/` never ships them), who writes them (the independent
   verifier, never the builder), and whether T2 is solved by a test module or by extending `run_graders.py`.
8. **Money.** Confirm that M7 has no currency amounts. If the spec adds a notional or a trade list, confirm integer cents
   with largest-remainder rounding (BUILDER_RULES money rule, applied to Python as AC4 Q10 decided).
9. **Source strings.** (a) `boyd2004convex`: the record's `years` include 2013; confirm the page cites the 2004 printing
   as the curriculum string does. (b) `stokey1989recursive`: the record lists three authors (Stokey, Lucas, Prescott) and
   the curriculum string is "Stokey & Lucas". Confirm that the key may be cited as is, with the same treatment as AC4 Q5
   (builders cite the key only and do not change the record).
10. **Markowitz (1952).** `markowitz1952portfolio` is verified but `used_by ["AP2"]`. Confirm whether M7 may cite it for
    the mean-variance origin in L06. Default: no citation.
11. **KKT attribution.** Confirm that no historical attribution of KKT is made (default), or raise a REFERENCE_REQUEST
    through Crossref for the original sources.
12. **Undeclared terms in prose.** Confirm that `dynamic-programming`, `efficient-frontier`, `newtons-method`,
    `contraction-mapping`, `covariance-matrix` and `turnover` are plain prose with no `<dfn>` and no link (AC4 Q4
    precedent). The verifier reads for them (T3).
13. **Lab count.** Confirm one lab per lesson (eight twins) plus three project labs (M1 Q2 precedent). The curriculum
    names one lab (`:320`), and BUILDER_RULES §3.4 asks for a numerical check of every key formula.
14. **Hours split.** Confirm 77 h lessons / 33 h project (30 %, M1 Q6 precedent), or an alternative within 10-40 %.
    Alternative: seven lessons of 11 h each.
15. **Placement and tier F.** Confirm that tier F keeps rungs 1-2 at full length (BLUEPRINT §4), and that the placement
    `data-mastery` is 0.8 (M1 precedent).
16. **Downstream dependency (for the architect, not M7's build).** `curriculum/01-foundations.yaml:298-327` gives M7 no
    rubric, so any downstream module that expects a rubric-graded M7 result would not find one. No action is requested
    here; reported as an observation.

## 15. Blocking issues (summary)

- **B1 (blocking L06 and the project).** Covariance input is outside M7's closure. Needs the architect's decision (Q1).
- **B2 (not blocking L01-L05, L07).** Infinite-horizon Bellman needs contraction, which is M5. Needs Q2 before L08.
- No curriculum conflict with the hours rules. The 110 h figure can satisfy the tool rules (lessons 77 h in eight
  6-12 h lessons, project 33 h = 30 %). The planner did not need to stop on the hours.

## 16. After the builders

1. Orchestrator integrates; runs the §12 commands once; fixes cross-lesson defects (DAG, links, hours).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02, L03-L04, L05-L06, L07-L08, project. The project
   verifier writes at least three mutants and the five alternative implementations (§7.4, Q7). Failing rows return to
   the builder only.
3. Ledger at `ledgers/M7.verification.json`; scripts that back rows under `ledgers/M7/scripts/`; mutants under
   `ledgers/M7/mutants/`.
4. Branch: a feature branch, not `main`. Merged only when the unit ledger is PASS or its remaining gaps are named and
   agreed.

## Architect decisions (2026-10-28, binding)
B1/Q1: mu and Sigma are given inputs; covariance appears only in a no-link disclaimer; no M4 prerequisite. B2/Q2: prove the finite-horizon recursion; omit the infinite-horizon result (say it is not treated here). Q3: objective (gamma/2) w'Sigma w - mu'w, one period, no annualization. Q4: `constrained_allocator.py`, freeze make_instance(seed) and allocate(instance) in the plan. Q5: teach the auxiliary-variable linearization of turnover. Q6: exact Fraction solves for small n; floats with tolerance 1e-8 where stated; NumPy needs data-packages. Q7: alternative implementations live under ledgers/M7/scripts/ (verifier-written). Remaining questions: follow the plan's recommendation.
