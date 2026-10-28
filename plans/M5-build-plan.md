# M5 build plan: Real Analysis (planner output, 2026-10-28)

Unit: **M5 · Real Analysis** · tier U · 130 h · prerequisites M2 · no Atlas milestone · grading `both`
(autograder for the contraction solver, rubric for the proof write-up) · output directory `course/modules/M/M5/`
(part code `M`, as M1). Planner: Haiku, plan only. No lesson content. No git operations. Executors: Haiku builders,
then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Status: a planner's proposal. §11 lists open questions for the architect. §0.3 lists one DAG conflict that must be
decided before any lesson is written.

Evidence convention: every curriculum fact below cites `file:line` read during planning. "Not in the curriculum" is
stated where it applies. The planner did not read Abbott or Rudin; no locator from either book is asserted.

---

## 0. Curriculum facts (read, with locators)

### 0.1 The entry

| Fact | Locator |
|---|---|
| Part M, code `M`, title "Mathematics" | `curriculum/01-foundations.yaml` (part block, M1 at :71 region); `curriculum/curriculum.json` `parts[1]` (code `M`) |
| M5 id, title "Real Analysis", tier U, hours 130, prereqs `[M2]` | `curriculum/01-foundations.yaml:230-234` |
| M5 core text: completeness of R, sequences and series, continuity, uniform convergence, compactness, metric spaces, fixed-point theorems (Banach), Riemann–Stieltjes | `curriculum/01-foundations.yaml:235-237` |
| M5 introduces 11 concepts | `curriculum/01-foundations.yaml:238-249` |
| Sources: Abbott, *Understanding Analysis*, 2nd ed. (2015); Rudin, *Principles of Mathematical Analysis*, 3rd ed. (1976) (free text) | `curriculum/01-foundations.yaml:250-252` |
| Lab: "Banach fixed-point iteration solving a Bellman equation." | `curriculum/01-foundations.yaml:253` |
| Project "Contraction-mapping solver": prove the Bellman operator for a discounted savings problem is a contraction, then implement value-function iteration with a certified error bound; deliverable "Proof plus a tested solver."; grading `both` | `curriculum/01-foundations.yaml:254-260` |
| No `debate` key on M5 (so no debate brief; `check_pages.py` keys on `u.entry.get("debate")`) | `curriculum/01-foundations.yaml:230-261` (absent); `tools/check_pages.py` near line 412 |
| No `atlas` key on the project; no Atlas milestone names M5 | `curriculum/meta.yaml` atlas block (A1-A20 lines, none naming M5); `tools/check_projects.py` lines 144-146 |
| The JSON row mirrors the YAML (id, tier U, hours 130, prereqs `["M2"]`, 11 introduces, sources, lab, project grading both, part M) | `curriculum/curriculum.json`, object with `"title": "Real Analysis"` at line 6466 (`parts[1].modules[4]`) |
| Rendered CURRICULUM.md line | `CURRICULUM.md:238` |
| Downstream: M6 requires `[M4, M5]` | `curriculum/01-foundations.yaml:265` |

Tier rank: U is rank 2, M is rank 3 (`curriculum/curriculum.json` `tiers`). BLUEPRINT §4 and §5.1 reduce rungs 1-2
"from tier M upward", so **M5 keeps rungs 1-2 at full length**.

### 0.2 Prerequisite closure and concept assignment

- Closure of M5 (computed from `curriculum.json` `prereqs`): **M1, M2, P0.1** (M2 → M1 → P0.1).
- Concepts available without definition (closure owners): M1 `discount-factor` (`01-foundations.yaml:101`),
  `geometric-series`, `mathematical-induction`, `present-value`; M2 `limit` (`:132`), `definite-integral` (`:135`),
  `derivative`, `gradient`, `multiple-integral`, `taylor-theorem`, others; P0.1 concepts (`:…` P0.1 block).
- Concepts used by name in the curriculum text but **outside the closure**:
  - `bellman-equation`: owner **M7** (`curriculum/curriculum.json` `concepts` at line 1457; yaml `curriculum/01-foundations.yaml:316`).
  - `principle-of-optimality`: owner **M7** (`curriculum.json` concepts; yaml `:315`).
  - `dynamic-programming`: owner **CS2** (`curriculum.json` concepts).
  - `expected-utility` (E3), `crra-utility` (E3), `utility-maximization` (E1): owners outside the closure.
  - None of these may be linked or defined in M5 (`tools/check_dag.py` rejects a link to a non-closure concept).

### 0.3 DAG conflict that must be decided (blocking for the lab and project wording)

The curriculum's M5 lab (`:253`) says "solving a **Bellman equation**", and the project (`:257`) says "discounted
savings problem". The term *Bellman equation* is the concept `bellman-equation` owned by M7 (`:316`), which is not in
M5's closure. M5 introduces only the *operator* concept `bellman-operator-contraction` (`:247`, "Contraction property
of the discounted Bellman operator"). The M5 pages can define the operator by an explicit formula, and the operator
is M5's own object. They cannot link or define the M7 term. Recommendation is in §11 Q1.

Also flagged: the notation registry binds the symbol `T` to "number of return observations" (S1), so the Bellman
operator must not be written `T` (see §7.4).

### 0.4 The curriculum's hours and the tool rules: no conflict

- Hub split: lessons 104 h, project 26 h, total 130 h (matches `:233`).
- Project share 26/130 = 20.0%, inside the 10-40% band (`tools/check_pages.py` `check_hub`, the `0.10 <= project_h / u.hours <= 0.40` rule).
- Ten lessons of 10 or 11 h: each inside the 6-12 h rule (`tools/check_pages.py` `check_lesson`, `6 <= declared <= 12`).
- Lesson hours plus project hours equal the curriculum figure (`check_hub`, `abs(lessons_h + project_h - u.hours) < 1e-9`).

So the curriculum hours can satisfy the tool rules. **No STOP is required.**

---

## 1. Rules for every builder (binding; BUILDER_RULES adapted to M5)

- Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `VERIFIER_RULES.md` §2 (what a verifier will
  check), this file. Study `course/modules/M/M1/` (template, lab embedding, grader panel, rubric), `course/modules/AC/AC2/`
  (lab-id and hours conventions), `course/modules/AC/AC4/` (grader and rubric with a unit-local solution file).
  `course/templates/` holds `hub.html`, `lesson.html`, `project.html`, `studio.html`. Imitate structure, not wording.
- **Proofs over citations (attribute nothing unread).** No builder has read Abbott or Rudin. The registry records for
  both keys carry bibliographic identity only (`references/references.json`; §7). So:
  - every theorem used (completeness of R, Cauchy criterion, Bolzano–Weierstrass, extreme value theorem, uniform limit of
    continuous functions is continuous, Banach fixed-point theorem, completeness of the bounded continuous functions
    under the sup norm) is **T-graded with a complete proof on the page**, its hypotheses listed explicitly
    (BUILDER_RULES §3.3);
  - no `data-locator` is attached to Abbott or Rudin unless the builder has read that locator in a source that reproduces
    it. A claim that cannot be proved on the page is graded C at most and says what is unconfirmed, or it is left out;
  - every "non-theorem claim" that is cited needs a key and a locator (`tools/check_pages.py` claims rule).
- **Evidence grades.** Mathematics is T (proved) or a derivation shown in full (BUILDER_RULES §3.5). "It can be shown that"
  is banned unless the showing follows at once. Remarks on history or on applications are graded and cited, or left out.
- **Scope words need a computation.** Words such as "dense", "generic", "almost surely", "in practice", "fast", "stable",
  "certified" are used only where a proof or a lab computes the claim on the page.
- **Define before use.** The 11 concepts in §3 are defined once, with `<dfn id="def-<id>" data-concept="<id>">`, in the
  lesson assigned there. Other terms the lesson needs (supremum, bounded, sup norm, complete metric space, utility
  function, policy, grid) are defined in plain prose at first use, with no `<dfn>` and no `data-concept` attribute, because
  `tools/check_dag.py` rejects a `<dfn>` for a concept M5 does not introduce (BUILDER_RULES §1.10). Define each such term
  in the lesson where it first appears, before any use in that lesson.
- **Concept links.** Closure concepts (M1, M2, P0.1) link to `../../../concepts.html#<id>`; earlier M5 lessons link to
  `Lnn.html#def-<id>`. A lesson never links a concept defined later (`tools/check_dag.py`, order check).
- **Proposition hypotheses explicit.** Every theorem, lemma and proposition lists its hypotheses in a numbered list before
  the statement's conclusion. Example form: "Let \(X\) be a complete metric space and \(T\colon X\to X\) a contraction
  with modulus \(\beta\in(0,1)\)." No hypothesis may be left implicit; the proof uses only listed hypotheses.
- **Notation.** Use only macros in `course/assets/data/notation.json` (BUILDER_RULES §3.1). Registered symbols keep their
  meaning: `T` is registered as a sample length (S1), so the Bellman operator is not written `T`. Requests for new macros
  go to `NOTATION_REQUESTS` (§7.4). `\gamma_3`, `\gamma_4` are registered (M4): avoid `\gamma` for anything else.
  `\beta` is a conventionally local letter (the notation registry's `about` text) and may be defined per lesson.
- **Numbers.** Every number is computed live (a lab), derived on the page, or quoted with a locator the builder has read.
  Compare numbers against **unrounded** values: a printed decimal is rounded only at the last step, and any quoted rounded
  figure is recomputed from the unrounded value (per the AC2/AC1/M1/AC4/CF1 verification lessons). Tolerances are stated.
- **Lab statements match code and output.** The hypothesis states the expected result before running, and it is the
  thing the code actually prints or checks. The interpretation names only what the printed output shows.
- **Labs.** Code lives once in its twin `tests/labs/M5/lab-M5-Lnn-1.py` (project labs `lab-M5-project-n.py`). The page
  carries `@@LAB:<file>@@` and `@@OUT:<file>@@`, and `tools/embed_labs.py` fills them. Never type expected output.
  - Labs are seeded, use **standard library only** (`fractions.Fraction`, `math`, `itertools`, `decimal` as needed; no NumPy,
    per the M1 precedent), run under 10 s in Pyodide, and need no network.
  - **Labs call `main()` at top level** (the M1 twins end with `def main() -> None: ...` followed by a bare `main()`).
  - Exact checks (identities, rational brackets) use `fractions.Fraction`, not floats. Float checks state the tolerance.
  - Lab ids match `lab-M5-<page>-<n>` (`tools/check_pages.py` lab-id rule), numbered in display order on each page.
- **Grader tests demand an exception type only for conditions the page names.** A test that expects `ValueError` checks
  only the invalid-input conditions the specification lists by name; any other failure is a plain assertion that names
  the property. Five alternative correct implementations (for example: synchronous and in-place sweeps, loop and
  vectorized forms, two tie-break rules for argmax, stopping on the a-posteriori bound and on a residual with the bound
  reported) must all pass. A test may not depend on one iteration count or one floating-point ordering.
- **Integer cents for money.** M5 has no currency quantity. The savings model is in dimensionless consumption units (§5.2).
  If any currency value enters a page or the grader, it is `int` cents (BUILDER_RULES money rule, Python form). Confirm
  in §11 Q9.
- **No horizontal scroll at 360 px.** Lab output, proof displays and the grader panel wrap or scroll inside their own
  box. `tools/page_smoke.py` checks `scrollWidth − innerWidth` at 360 px (its line 341-343). Builders do not run
  `page_smoke.py`; verifiers run it on a quiet machine.
- **Figures (optional).** If a lesson includes a figure, use `figures-Lnn.js` with `course/assets/js/chart.js`, axes with
  units, a source line that reads "computed from the formula; no data", and a caption that states the one thing to see
  (BUILDER_RULES §6.4). The default is no figure. Recommended only in L07 (contraction error against the bound) and L09
  (certified bound against actual error).
- **Problem sets.** Each lesson has at least three problems in each of Mechanics, Proof, Empirical and Research, each with a
  full worked solution in `<details class="solution">` (BUILDER_RULES §4.2 item 7). That is 12 problems and 12 worked
  solutions per lesson, 120 in total. This is the largest writing load in the unit (§11 Q12). Empirical problems are
  computed in a lab twin or a figure, on generated data labelled as generated (§8).
- **Hub, lessons, project** follow `course/templates/` and BUILDER_RULES §4.
- **Banned strings** (BUILDER_RULES §1.3-1.4) apply to all prose: TODO, TBD, lorem, "for brevity", "beyond the scope",
  "it is important to note", "studies show", "it is well known", "obviously", "clearly".
- Never hand-edit generated files: `CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`,
  `course/concepts.html`, `course/assets/data/*.json` (including `glossary.json`, `notation.json`, `references.json`),
  `references/*.json`. Never edit `curriculum/*.yaml`; request changes.
- Do not run `page_smoke.py`. Targeted checks only (§9).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10
  output contract.

---

## 2. Outline and file ownership (proposed; the architect fixes it)

Hours: lessons 104 (ten lessons of 10-11 h) plus project 26 = 130. Concept coverage: 11 concepts, each in exactly one row.

| Lesson | Title (working) | Concepts it defines (from `introduces`, `:238-249`) | Hours | Lab twin id | Owner |
|---|---|---|---|---|---|
| L01 | Completeness of the real numbers | `completeness-of-reals` | 10 | `tests/labs/M5/lab-M5-L01-1.py`: a bisection that brackets the supremum of a bounded set, with `Fraction` brackets and a printed width per step | A |
| L02 | Sequences, Cauchy sequences and series | `cauchy-sequence` | 10 | `lab-M5-L02-1.py`: Cauchy test on partial sums; a sequence that is not Cauchy, with the index where the test fails | A |
| L03 | Continuity in epsilon–delta form | `epsilon-delta-continuity` | 10 | `lab-M5-L03-1.py`: a delta for \(x^{2}\) at \(x_0=2\) checked on a grid, against the bound \(|x^2-4|\le 5|x-2|\) on \(|x-2|\le 1\) (the bound is proved on the page) | A |
| L04 | Metric spaces | `metric-space` | 10 | `lab-M5-L04-1.py`: metric axioms checked exhaustively on a finite sample for the Euclidean metric on \(\mathbb{R}^2\) and the sup metric on a grid of \(C[0,1]\) | B |
| L05 | Uniform convergence | `uniform-convergence` | 10 | `lab-M5-L05-1.py`: \(f_n(x)=x^n\) on \([0,1]\) (sup distance 1 for every \(n\)) against \([0,a]\), \(a<1\) (sup distance \(a^{n}\)) | B |
| L06 | Compactness | `compactness` | 10 | `lab-M5-L06-1.py`: bisection extracts a convergent subsequence from a bounded sequence; the maximum of a continuous function on a grid of \([0,1]\) is attained at a printed grid point | B |
| L07 | Contraction mappings and the Banach fixed-point theorem | `contraction-mapping`, `banach-fixed-point-theorem` | 11 | `lab-M5-L07-1.py`: Banach iteration for \(\cos\) on \([0,1]\); the modulus \(\sup|f'|\) computed on a grid; the a priori error bound against the actual error | C |
| L08 | The discounted Bellman operator is a contraction | `bellman-operator-contraction` | 11 | `lab-M5-L08-1.py` (**the curriculum lab**): fixed-point iteration of the discounted Bellman operator on a finite grid; the contraction ratio \(\le\beta\) checked on seeded random pairs | C |
| L09 | Value-function iteration with a certified error bound | `value-function-iteration` | 11 | `lab-M5-L09-1.py`: iteration stopped by the a posteriori bound; the actual error against a 10⁻¹² solve of the same grid operator | E |
| L10 | The Riemann–Stieltjes integral | `riemann-stieltjes-integral` | 11 | `lab-M5-L10-1.py`: Riemann–Stieltjes sums for \(\int_0^1 x\,dG(x)\) with \(G(x)=x^{2}\), against the closed form 2/3 derived on the page | E |

Totals: lessons 6·10 + 4·11 = 104 h; project 26 h; unit 130 h (= `curriculum.json` hours 130).

Concept coverage: 1+1+1+1+1+1+2+1+1+1 = 11 = the 11 entries at `curriculum/01-foundations.yaml:239-249`.

Ordering check (each lesson uses only earlier definitions or closure concepts):
- L02 uses `completeness-of-reals` (L01) and the M2 `limit`.
- L03 uses the M2 `limit` and sequences (L02).
- L04 uses `cauchy-sequence` (L02) and continuity (L03) for "continuous maps between metric spaces".
- L05 uses `metric-space` (L04) for the sup distance and continuity (L03) for "a uniform limit of continuous functions is continuous".
- L06 uses `metric-space` (L04) and continuity (L03) for the extreme value theorem.
- L07 uses `metric-space` (L04), `cauchy-sequence` (L02) and `completeness-of-reals` (L01) for complete metric spaces.
- L08 uses `contraction-mapping` and `banach-fixed-point-theorem` (L07), compactness (L06) for bounded continuous functions on a
  compact grid, uniform convergence (L05) for completeness of the function space, and `discount-factor` (M1).
- L09 uses L08 and L07.
- L10 uses the M2 `definite-integral` and `limit`. It does not need L01-L09, so it is placed last, as the curriculum lists it.

Owner rule: a builder writes only its own lesson files and twins. The hub is written by Builder A after its lessons exist,
so the lesson-map links are right. Builder D's grader files are independent of the lessons.

---

## 3. Lesson content: what each lesson must establish (the builder decides the argument)

- **L01.** Supremum property of \(\mathbb{R}\) as the completeness axiom; nested-interval and bisection consequences, each
  proved from the axiom. Bounded sets and the supremum are plain-prose terms, not concepts.
- **L02.** Sequences; Cauchy sequences; in \(\mathbb{R}\), Cauchy ⇔ convergent (proved, using L01); series as sequences of partial
  sums; the Cauchy criterion for series. Core-text item "sequences and series" is taught here as prose (§11 Q3).
- **L03.** Continuity at a point and on a set in epsilon–delta form, linked to M2's `limit`; sequential characterization;
  continuous functions on compact sets are deferred to L06.
- **L04.** Metric axioms; open and closed sets in a metric space as plain-prose terms defined on the page; sup metric on bounded
  functions; Cauchy sequences and completeness in a metric space.
- **L05.** Pointwise vs uniform convergence; uniform limit of continuous functions is continuous (proved); Weierstrass M-test
  (stated and proved only if used in L08; otherwise left out). Canon break: pointwise limits of continuous functions need not be
  continuous.
- **L06.** Sequential compactness; Bolzano–Weierstrass in \(\mathbb{R}\) (proved by bisection); extreme value theorem for a
  continuous function on a compact set (proved); the finite-grid case used in the project. Canon break: bounded does not imply
  compact in infinite dimensions (shown with a sequence of unit vectors in a sup-metric space of sequences; proof on the page).
- **L07.** Contraction with modulus \(\beta\in(0,1)\); Banach fixed-point theorem with uniqueness, existence and the a priori
  bound \(\operatorname{d}(x_n,x^\ast)\le \beta^{n}\operatorname{d}(x_0,x_1)/(1-\beta)\) (proved on the page; the constant is
  derived there, not quoted); convergence of the iteration; the modulus of a differentiable map is \(\sup|f'|\) on an interval (proved
  by the mean value theorem, whose statement is cited to the calculus of M2 with a `data-locator` only if confirmed, otherwise
  proved or stated as a named prerequisite).
- **L08.** The discounted savings model in explicit formulas: state \(k\) on a finite grid, feasible successors, utility \(u\),
  discount \(\beta\in(0,1)\). The discounted Bellman operator \((\mathcal{B}V)(k)=\max_{k'\text{ feasible}}\{u(c)+\beta V(k')\}\) is defined
  by this formula (notation request: §7.4). Contraction proof with the sup norm: \(\|\mathcal{B}V-\mathcal{B}W\|_\infty\le\beta\|V-W\|_\infty\)
  (proved). The space: real vectors on a finite grid, or bounded continuous functions on a compact interval (§11 Q2).
- **L09.** Value-function iteration \(V_{n+1}=\mathcal{B}V_n\). A posteriori bound \(\|V_{n}-V^\ast\|_\infty\le\frac{\beta}{1-\beta}\|V_{n}-V_{n-1}\|_\infty\)
  (derived on the page from L07). Stopping rule and the certified error. The certified bound is a bound on the distance to the fixed point
  of the operator the solver iterates (the grid fixed point); discretization error is not certified and is stated as a limitation.
- **L10.** Riemann–Stieltjes integral \(\int f\,dG\) defined by partitions and tags (for \(G\) of bounded variation and \(f\)
  continuous, the limit exists; proof or precise statement with hypotheses stated). Worked identity: when \(G\) is continuously
  differentiable, \(\int f\,dG=\int f\,G'\,dx\) (proved on the page under the hypotheses listed). The lab's closed form for
  \(G(x)=x^{2}\) is the identity applied, with the value 2/3 computed on the page.
- **Canon-break sections** (every lesson): one place where the result fails if a hypothesis is dropped (for example, the Banach theorem
  without completeness, or a contraction with \(\beta=1\)), with a counterexample on the page.
- **Misconceptions** (≥3 per lesson), for example: "pointwise convergence preserves continuity" (L05); "a small step
  \(\|V_{n+1}-V_n\|\) bounds the error" (L09, the sound bound has the factor \(\beta/(1-\beta)\)); "any bounded sequence converges"
  (L06).

No debate brief is required (no `debate` key, §0.1).

---

## 4. Hub (`index.html`, Builder A)

- `<main data-hours-lessons="104" data-hours-project="26">` (sums to 130; project 20.0%).
- 4-8 measurable objectives (for example: "Prove" completeness-based results; "Construct" a metric; "Certify" an iteration's error).
- Prerequisites: M2 (with the M2 `limit`, `definite-integral` concept links) and, through M2, M1 `discount-factor` (linked to the
  closure concepts page).
- Placement diagnostic: `<section class="quiz" id="placement" data-unit="M5" data-page="placement" data-mastery="0.8">`,
  matching the AP1 bar (`course/modules/AP/AP1/index.html:77`). Include at least two items marked `data-skill`, one for the
  rung-1 task (a fixed-point proof with a certified bound) and one for the rung-2 missing step (the contraction inequality), and
  the rest testing M2 and M1 prerequisites.
- Lesson map links L01-L10. Project ladder `ol.ladder` with the four rung titles in order (§5.1).
- Declared study hours per lesson are in each `<html data-hours>`.

---

## 5. Project ladder and grader design (Builder D)

### 5.1 Ladder (BLUEPRINT §5.1; full rungs 1-2 because tier U < M)

1. **Rung 1, worked example** (`lab-M5-project-1`, skippable on placement): a fully solved and annotated case on a 3-point grid:
   the contraction inequality checked step by step, one iteration of \(\mathcal{B}\), the a posteriori bound, with a "why" note at
   each step.
2. **Rung 2, completion problem** (`lab-M5-project-2`, `class="lab completion"`): the same case with the modulus step and the bound
   line replaced by `___`. Graded instantly; the completed twin is the solution. `tools/check_projects.py` requires a
   `section.lab.completion` or a quiz for rung 2.
3. **Rung 3, independent project** (graded): the library `contraction_solver.py` (§5.2), autograded, plus the proof write-up
   (rubric-graded, §5.4). `lab-M5-project-3` is the rung-3 check.
4. **Rung 4, stretch** (optional, no ceiling, not graded): for example, Howard policy iteration with a certified bound, or a
   measured convergence rate against \(\beta\) on a family of instances.

### 5.2 Specification (`project.html`; the spec must name grading as autograder and rubric)

- **Context.** A discounted savings problem: a planner chooses how much of today's output to save, and the value of a state is the
  discounted utility of the best plan from it. The state grid and parameters are generated per seed; there is no currency.
- **Inputs.** Generated parameters from `make_instance(seed)` (§5.3): discount factor \(\beta\in(0,1)\), production parameter
  \(\alpha\in(0,1)\), a strictly increasing grid of states, a tolerance. No data files; no MANIFEST entries.
- **Required outputs.** `contraction_solver.py` with the signatures frozen in §5.3, and a proof write-up `proof.md` (or
  `proof.pdf`) with the sections: Setting, Contraction, Fixed point, Certified bound, Numerical check, Limitations.
- **Constraints.** Standard library only in the grader (NumPy optional locally, not in the browser; §11 Q10). Each test under 5 s in
  Pyodide and the suite under 60 s. Invalid inputs fail loudly (§5.3).
- **Grading mode.** Both: the autograder checks `contraction_solver.py`; the rubric grades the proof write-up and the self-assessment.
- **Reading list** (`ol.reading-list`, registry keys only): `abbott2015understanding`, `rudin1976principles` (§7.1).
- **Time budget** (`<table id="hours">`, 26 h; every row needs a rationale; components sum to 26):

| Component | Hours | Rationale |
|---|---|---|
| Rung 1 worked example | 1 | Read and annotate one three-point case |
| Rung 2 completion | 2 | Fill the modulus and bound lines, then run the instant check |
| Proof write-up (contraction, Banach use, certified bound) | 8 | Four theorems with complete proofs, each with its hypotheses |
| Solver implementation and property tests | 7 | Bellman operator, iteration, stopping rule, edge cases |
| Self-check against the grader and the numerical check | 3 | Run the suite on own instances; reconcile the numbers in the write-up |
| Memo revision and self-assessment | 5 | Revise against the rubric; score against two exemplars |
| **Total** | **26** | Equals `data-hours-project` on the hub |

### 5.3 Grader design (`grader/`)

- **Frozen signatures** (proposed; the architect freezes them, §11 Q7):
  - `make_instance(seed: int) -> dict[str, Any]` in `grader/instance.py`. Returns `beta: float` in \((0,1)\), `alpha: float` in \((0,1)\),
    `grid: list[float]` strictly increasing and positive, `tol: float > 0`. Deterministic per seed. Generates only valid instances.
    Labelled in the docstring: "generated parameters; not data".
  - `bellman_operator(params: dict[str, float], grid: list[float], values: list[float]) -> list[float]` in `contraction_solver.py`.
  - `solve(params: dict[str, float], grid: list[float], tol: float, max_iter: int) -> dict[str, Any]` returning `value` (list of floats),
    `iterations` (int), `certified_error` (float), `converged` (bool).
- **Named invalid-input conditions** (the only ones a test may expect as `ValueError`, §1): \(\beta\notin(0,1)\); `tol <= 0`; `max_iter < 1`;
  a grid that is not strictly increasing; a grid or value vector of unequal length. All other failures are plain assertions.
- **Tests** (`grader/test_project.py`, property and number checks, each with a message that names the property and gives a concept hint,
  never the answer):
  1. contraction property on seeded random pairs: \(\|\mathcal{B}V-\mathcal{B}W\|_\infty\le\beta\|V-W\|_\infty\) to a stated tolerance;
  2. fixed-point residual: \(\|\mathcal{B}V_{\text{out}}-V_{\text{out}}\|_\infty\le\) `tol`;
  3. certified bound: \(\|V_{\text{out}}-V_{\text{ref}}\|_\infty\le\) `certified_error`, where \(V_{\text{ref}}\) is computed by the test's own
     independent loop at tolerance \(10^{-12}\) from the instance's parameters (not from the student's code);
  4. iteration budget: `iterations` does not exceed the a priori count from \(\beta\) and `tol` by more than one;
  5. a closed-form family (if kept, §11 Q2): the test computes the known value function from the instance's parameters and checks it;
  6. invalid input: the named `ValueError` conditions above, and no silent acceptance.
  - Tests must not pass a hard-coded answer. Seed 0 is not special.
- **Five alternative correct implementations must pass** (BUILDER_RULES §5 and the §1 rule above): synchronous (Jacobi) sweep; in-place
  (Gauss–Seidel) sweep; loop and vectorized forms; two tie-break rules for the argmax; stopping on the certified bound and on the
  residual with the bound reported.
- **Dual mode.** The identical suite runs in Pyodide and locally (`QF_SEED` pattern as in `course/modules/M/M1/grader/test_project.py`
  docstring). Warnings are failures in both.
- **Starter** (`grader/starter.py`): every function raises `NotImplementedError`; the suite must fail on it (`run_graders.py` checks this).
- **Reference** (`grader/reference.py`): full solution; passes every test on seeds 0-49 (`run_graders.py --unit M5 --seeds 0-49`).
- **Mutants** (verifier writes at least three per round, VERIFIER_RULES §2.6; each must fail at least one test). Suggested by the planner:
  1. \(\beta\) applied as \(1/\beta\), or omitted from the update;
  2. certified bound uses \(\|V_n-V_{n-1}\|\) without the factor \(\beta/(1-\beta)\), an unsound bound;
  3. stopping on \(\|V_{n+1}-V_n\|\le\) `tol` and reporting `certified_error = tol`;
  4. maximisation over infeasible successors (feasibility not enforced);
  5. nearest-grid-point lookup in place of exact feasibility, changing the fixed point;
  6. off-by-one in the iteration count;
  7. a hard-coded answer for seed 0.
- **Failure messages** name the violated property and never print the expected value.

### 5.4 Rubric (the proof write-up; `table.rubric`, exemplars, self-assessment)

- Six criteria, four observable levels each (4-7 required by `tools/check_projects.py` `rubric_problems`). Planner's criteria:
  - C1 **Assumptions**: the setting states the space, the metric, the grid or compact interval, the continuity and boundedness of \(u\) and the
    constraint set, and \(\beta\in(0,1)\). Level 4 names all five; level 1 names none.
  - C2 **Contraction**: each inequality step is written and justified by a named property.
  - C3 **Completeness**: the space is shown complete, with the proof or the finite-dimensional reason.
  - C4 **Certified bound**: derived from the contraction, not asserted; the constant is shown.
  - C5 **Numerical check**: every number in the write-up is printed by the solver run, with the seed and tolerance stated.
  - C6 **Limitations**: discretization error, grid resolution and the sense in which the bound is certified are stated.
- **Exemplars** at level 4 and level 2 (`data-level="4"` and `data-level="2"`), fully written, with annotations mapping each passage to the
  descriptors it meets or misses, and `data-scores` per criterion, as in `course/modules/M/M1/project.html` (exemplar-a at line 341,
  exemplar-b at line 405).
- **Self-assessment form.** The student scores themselves, then sees the annotated exemplar scores, and the page shows where the scoring
  diverged.
- **Question bank**: not required unless the architect classes the write-up as adversarial (§11 Q8).

---

## 6. Cards builder (Builder E, after A-D)

- `course/modules/M/M5/cards.json`, ids `M5-c001` upward, `lesson` in L01-L10 (`tools/check_pages.py` cards rule: unit prefix, lesson
  exists, valid grades and keys).
- One card per definition, theorem statement, key formula, key numerical result and misconception (BUILDER_RULES §7).
- Grade T for every theorem and derived formula, with `"basis"` naming the lab or the proof section (for example
  `"basis": "Lab 8, Section 3 (proof)"`). `cite` is empty on every card, because M5 makes no empirical claim.
- Each card tests one fact, and its back is checkable against the lesson text.

---

## 7. Registry keys, notation and glossary

### 7.1 Keys the module may cite (verified in `references/references.json`)

| Key | Record (references.json) | Status | Use in M5 |
|---|---|---|---|
| `abbott2015understanding` | Abbott, *Understanding Analysis* (Springer), DOI `10.1007/978-1-4939-2712-8`, year 2015, `used_by: ["M5"]` | verified (Crossref) | curriculum-listed; reading list; a claim is attributed to it only with a locator the builder has read. Otherwise no attribution |
| `rudin1976principles` | Rudin, *Principles of mathematical analysis*, McGraw-Hill, year 1976, Open Library, `used_by: ["M5"]` | verified (Open Library) | curriculum-listed; reading list; same locator rule |
| `stokey1989recursive` | Stokey, Lucas & Prescott, *Recursive Methods in Economic Dynamics*, DOI `10.2307/j.ctvjnrt76`, year 1989, `used_by: ["M7"]` | verified (Crossref) | **not** curriculum-listed for M5; exists, so it could be cited; the source string is "Stokey & Lucas" while the record lists three authors. Use only if the architect approves (§11 Q6) |

Notes: the records carry no edition field; the curriculum's edition strings ("2nd ed.", "3rd ed.") appear only in `source_strings`,
and the planner did not verify an edition. Builders cite the key only. The curriculum's free-text `sources` field is not a citation.

### 7.2 REFERENCE_REQUESTS

- None required. The curriculum names no source beyond the two registered books. A builder who needs a source for a specific claim
  (for example, a named sufficient condition for a contraction in a dynamic model) records a request with a DOI or ISBN, the
  authors, year, title, venue, the reason and its confidence. It is not cited until admitted through `tools/add_reference.py`.

### 7.3 Real-data policy

- No real data is needed. M5 is analysis. `course/assets/data/market/MANIFEST.json` has no entry relevant to M5 (checked by the
  planner through the manifest's three entries, `tools/data_sources.yaml`). No `data-files` attribute on any lab, so the
  `check_pages.py` data rule is vacuous.
- The grader instances and lab cases are **generated model parameters**, labelled as generated (not data) on the page and in the
  docstring. Where a generated case is displayed as numbers, it carries a visible **SIMULATED** label (BUILDER_RULES §1.7).
- No `DATA_REQUESTS`.

### 7.4 NOTATION_REQUESTS (macros the unit needs; `notation/notation.json` as shipped to the site)

The registry defines 26 macros and 8 symbols (`course/assets/data/notation.json`). The following are needed and not registered:

| Request | Meaning | Needed for |
|---|---|---|
| `\norm` (or `\lVert\cdot\rVert_\infty`) | sup norm \(\|\cdot\|_\infty\) on bounded functions or grid vectors | L05, L07, L08, L09 |
| `\mathcal{B}` | the discounted Bellman operator (not `T`: registered to S1 as sample length) | L08, L09, project |
| `\mathcal{C}` | continuous functions on a compact set, or the bounded continuous functions | L05, L08 |

Already registered and usable: `\R` (real numbers), `\N` (natural numbers). Built-in KaTeX operators (`\sup`, `\max`, `\min`,
`\operatorname`) are not macros and need no request. `\beta` is a locally defined letter; `\gamma` is registered (M4) and avoided.

### 7.5 GLOSSARY_REQUESTS

- None. `course/assets/data/glossary.json` is generated by `tools/build_site.py` from every `<dfn data-concept>` on built pages
  (`tools/build_site.py` line 11 and the glossary section at line 245). The M5 glossary entries appear when the pages are built.
  The glossary currently has no M5 entries (for example, no key `cauchy-sequence`), which is expected before the build.

---

## 8. Atlas

- **No Atlas milestone.** No Atlas entry names M5 (`curriculum/meta.yaml` atlas block; §0.1). The project has no `atlas` key.
  `tools/check_projects.py` lines 144-146 therefore skip the contract check. **No `atlas/A*.contract.md` is needed or drafted.**
- The grader's solution path is a unit-local file (`contraction_solver.py`), as in the AC4 and AP1 pattern. Not `atlas/`.

---

## 9. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

```bash
.venv/bin/python tools/check_pages.py --unit M5           # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit M5
.venv/bin/python tools/check_projects.py --unit M5
.venv/bin/python tools/run_labs.py --unit M5              # --page L08 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/M/M5/L01.html   # per page, after the twins exist; --refresh <lab-id> after edits
.venv/bin/python tools/run_graders.py --unit M5 --seeds 0-49
.venv/bin/python tools/mutate_graders.py --unit M5 --seeds 0-9      # verifier only
.venv/bin/ruff check tests/labs/M5 course/modules/M/M5/grader && .venv/bin/ruff format --check tests/labs/M5 course/modules/M/M5/grader
.venv/bin/mypy                                            # the repo gate (strict); the architect runs it once
```

Flags confirmed in each tool's argparse block: `check_pages.py`, `check_dag.py`, `check_projects.py` take `--unit` (or `--all`);
`run_labs.py` takes `--unit`, `--all`, `--page`; `run_graders.py` takes `--unit`, `--all`, `--seeds`; `mutate_graders.py` takes `--unit`,
`--seeds`. The planner did not run `embed_labs.py`, `run_graders.py` or `mutate_graders.py`.

Gate-level checks across the repository (`check_pages.py --all`, `check_dag.py --all`, `build_site.py --check`, `render_curriculum.py`) are the
architect's, once, before merge.

### 9.1 Observed state at planning time (read-only runs, 2026-10-28)

| Command | Output (exact, last line) | Meaning |
|---|---|---|
| `.venv/bin/python tools/check_pages.py --unit M5` | `FAIL M5: M5 is not built (…/course/modules/M/M5/index.html missing)` · `check_pages M5: FAIL (1 problems)` | expected before the build |
| `.venv/bin/python tools/check_dag.py --unit M5` | `FAIL M5: 'uniform-convergence' is introduced by M5 but never defined with <dfn> on its pages` (and 10 more) · `check_dag M5: FAIL (11 problems)` | expected: the 11 concepts are not yet defined |
| `.venv/bin/python tools/check_projects.py --unit M5` | `FAIL M5: project.html is missing` · `check_projects M5: FAIL (1 problems)` | expected before the build |
| `.venv/bin/python tools/run_labs.py --unit M5` | `run_labs M5: PASS (0/0)` | vacuous until twins exist |

---

## 10. Tooling assumptions that do not hold for M5 (flagged)

1. **No Atlas milestone.** `check_projects.py` atlas branch does not apply (§8).
2. **No debate.** `check_pages.py` debate rule is not triggered (§0.1).
3. **Grading `both`.** `check_projects.py` `grading_problems` requires the spec's grading entry to name both "autograder" and
   "rubric"; the rubric table and two exemplars are required (`rubric_problems`).
4. **One curriculum lab, ten lesson labs.** The curriculum names one lab (`:253`). BUILDER_RULES §3.4 ("every key formula gets a numerical
   check in a lab") needs more. The plan adds one lab per lesson (13 twins including project labs), following the M1 architect decision.
5. **Full rungs 1-2.** Tier U is below M, so the minimal-rungs rule (BLUEPRINT §4, §5.1) does not apply.
6. **`check_dag.py` cannot see names.** It detects links and `<dfn>` only. A name used without a link (for example "Bellman equation",
   "utility function", "dynamic programming", "supremum") passes the tool, so the verifier reads for it (VERIFIER_RULES §2.9).
7. **Locator-free attribution.** `check_pages.py` checks that keys are in the verified registry and locators are non-empty. It does not
   check that a locator is correct. The no-locator-without-reading rule (§1) is enforced by the verifier, not by the tool.
8. **`data-files` checks are vacuous.** No lab reads data.
9. **Glossary is generated.** Builders never hand-edit `glossary.json` (§7.5).

---

## 11. Open questions for the architect (numbered)

1. **Bellman equation (DAG, blocking for L08, L09 and the project wording).** The curriculum lab (`:253`) and project brief (`:257`)
   use the term "Bellman equation", which is M7's concept (`bellman-equation`, `:316`; not in M5's closure). Recommendation: M5 defines
   the discounted Bellman operator by an explicit formula (its own concept `bellman-operator-contraction`, `:247`), states the fixed-point
   relation \(V=\mathcal{B}V\) in prose, and does not link or define `bellman-equation`. The lab title on the page reads "fixed point of the
   discounted Bellman operator" to match the curriculum's lab content without the M7 term. Alternatives: (a) a curriculum change moving
   `bellman-equation` or adding it to M5's prerequisites (not proposed here); (b) a forward link (forbidden by BUILDER_RULES §4.1). Architect
   to confirm (a)-recommendation.
2. **The savings model and the certified target (blocking for the grader).** (i) Utility: the curriculum names none. A utility unbounded
   below or with a singularity at zero (for example \(\ln c\) on a grid that includes 0) makes the operator undefined on the grid. The spec must
   fix a bounded utility on the finite feasible set, or a compact state interval with \(u\) continuous and bounded there. (ii) Space: finite grid
   in \(\mathbb{R}^{n}\) with the sup norm (planner's recommendation for the solver) and the bounded-continuous-function space as the proof's
   setting (L07, L08). (iii) The certified bound is a bound to the fixed point of the grid operator the solver iterates. It is not a bound to
   the continuous problem's value function; discretization error is a stated limitation. Architect to confirm (iii) and fix (i).
3. **Core text not in `introduces` (`:236`).** "sequences and series" and "fixed-point theorems" (plural, parenthetical "(Banach)") are in the core
   text but not in `introduces` (`:238-249`). Recommendation: "sequences and series" is taught as prose in L02 with no `<dfn>` (the M1
   precedent, Q3). The fixed-point scope is read as Banach only. Confirm, or request curriculum concepts (the planner cannot change the curriculum).
4. **Riemann–Stieltjes placement.** L10 does not feed the project. It is placed last, as the curriculum lists it. Confirm, or move it before L07
   (no hours change).
5. **Hours split 104 / 26 (20%).** Confirm, or choose another split inside 10-40% (13 to 52 h of project).
6. **Registry: `stokey1989recursive`.** It is verified and useful for L07-L09 (Bellman and contraction methods), but its `used_by` is M7 and its
   source string ("Stokey & Lucas") differs from the record's three authors. The planner did not add M5 to `used_by`. Architect decides whether
   M5 may cite it (via the registry tools), or it stays out.
7. **Frozen grader signatures (§5.3) and solution file name `contraction_solver.py`.** Confirm, freeze in the spec, and confirm no Atlas contract.
8. **Adversarial?** The proof write-up is not an IC defense or a debate. No 15-angle question bank is planned (AC4 Q9 precedent). Confirm.
9. **Money.** M5 has no currency. Confirm the savings model is dimensionless; the integer-cents rule is then vacuous for M5 (AC4 Q10 precedent
   applies only if a currency value appears).
10. **Standard library only in the grader and labs (no NumPy).** The M1 precedent. NumPy is available in Pyodide per BLUEPRINT §6, but the
    planner recommends the standard library for the grid sizes (at most a few hundred points) and for exact `Fraction` checks. Confirm.
11. **Labs: one per lesson (13 twins).** Confirm (M1 Q2 precedent).
12. **Workload.** BUILDER_RULES §4.2 requires at least 12 problems with worked solutions per lesson (120 in total). This is a rule, not a choice.
    Confirm no relaxation, or accept the load across Builders A-E.
13. **Figures.** None planned by default. Confirm, or ask for one each in L07 and L09.
14. **Lessons' owners.** Builder A: L01-L03 and hub; B: L04-L06; C: L07-L08; D: project and grader; E: L09-L10 and cards (cards run after A-D).

---

## 12. Reused architect decisions (precedent, for this unit)

- One lab per lesson, the curriculum lab in its named lesson (M1 Q2; §2, L08).
- Undeclared terms are plain prose, never `<dfn>` (AC4 Q4; §1).
- Only curriculum-listed or verified keys for the unit; no extra source without architect approval (M1 Q4; §7.1).
- No link to a concept outside the prerequisite closure (M1 Q1 pattern; §0.2, §0.3).
- Grader signatures are frozen in the spec before builders start (AC4 Q7; §5.3).
- Hours split confirmed by the architect before the hub is written (M1 Q6, AC4 Q10; §11 Q5).
- No question bank unless the architect classes the write-up as adversarial (AC4 Q8, Q9; §11 Q8).
- Integer cents apply to any currency value only (AC4 Q10; §11 Q9).

---

## 13. After the builders

1. Orchestrator integrates; runs the §9 commands once; fixes cross-lesson defects (DAG, links, hours).
2. Independent Haiku verifiers in fresh checkouts, slices: L01-L03, L04-L06, L07-L08, L09-L10, project. The project verifier writes at
   least three mutants per round (VERIFIER_RULES §2.6); failures return to a builder with only the failing rows. Scripts that back a row go
   under `ledgers/M5/scripts/` (VERIFIER_RULES §3).
3. Branch: a feature branch, not `main`. Merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. The unit is never
   merged incomplete, because an unfinished unit breaks `check_pages.py --all`.

## Architect decisions (2026-10-28, binding)
Q1: the discounted Bellman operator is defined by formula; the page wording avoids the concept name 'bellman-equation' (M7's). Q2: the savings model is a finite grid of capital values with utility u(c)=sqrt(c) for c>=0; the certified bound is to the grid operator's fixed point (state this). Q3: sequences and series are prose. Q4: Riemann-Stieltjes last. Q5: 104/26 hours. Q6: do not cite stokey1989recursive. Q7: `contraction_solver.py`, freeze signatures in the plan before building. Q8: not adversarial, no question bank. Q9: dimensionless model, no integer cents. Q10: standard library only. Notation: do not use T for the operator; use \mathcal{B}, define \mathcal{B}, \mathcal{C} and \norm locally in the page (NOTATION_REQUESTS recorded in plans/M5-open-items.md, no registered macro change). Lesson ownership: A L01-L03 and the hub, B L04-L06, C L07-L08, E L09-L10, D project and grader, F cards.
