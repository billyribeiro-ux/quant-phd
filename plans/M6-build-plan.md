# M6 build plan: Measure-Theoretic Probability (planner output, 2026-10-28)

Unit: **M6 · Measure-Theoretic Probability** · tier M · 150 h · prerequisites M4, M5 (closure M1, M2, M4, M5, P0.1) ·
no Atlas milestone · no debate · grading `both` (autograder for the numerical verification engine, rubric for the
typeset proofs) · output directory `course/modules/M/M6/` (part code `M`, as M1) · lab twins `tests/labs/M6/`.

Planner: Haiku, plan only. No lesson content, no git operations, no commits, no changes outside `plans/M6-build-plan.md`.
Executors: Haiku builders, then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes
a ledger. Branch at planning: `claude/fanout-b3`.

Evidence convention: every curriculum statement cites `file:line` read during planning. Anything not in the curriculum is
marked **NOT IN CURRICULUM**. Architect decisions on M1, E1, AC4, M5, M7 are reused where the same issue arises (§9).

---

## 0. Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part M, code `M`, title "Mathematics"; STUDIO-M requires M7, M8 (not M6) | `curriculum/01-foundations.yaml:70-76` (studio id at :74) |
| M6 id `M6`, title "Measure-Theoretic Probability" | `curriculum/01-foundations.yaml:261-262` |
| Tier `M`, hours `150` | `curriculum/01-foundations.yaml:263-264` |
| Prereqs `[M4, M5]` | `curriculum/01-foundations.yaml:265` |
| Core text: sigma-algebras, Lebesgue integral, MCT and DCT, Fubini, Radon–Nikodym, conditional expectation as L2 projection, filtrations, discrete-time martingales, optional stopping, martingale convergence | `curriculum/01-foundations.yaml:266-269` |
| `introduces` has **15** concepts (not 14): sigma-algebra, probability-space, lebesgue-integral, monotone-convergence-theorem, dominated-convergence-theorem, fubini-theorem, radon-nikodym-theorem, conditional-expectation-l2, filtration, martingale, stopping-time, optional-stopping-theorem, doob-maximal-inequality, martingale-convergence-theorem, doubling-strategy | `curriculum/01-foundations.yaml:270-285` (one per line 271-285) |
| Sources (free text, not keys): Williams, *Probability with Martingales* (1991); Billingsley, *Probability and Measure*, anniversary ed. (2012) | `curriculum/01-foundations.yaml:286-288` |
| Lab: "Martingale betting-system simulator: why doubling strategies fail under finite capital." | `curriculum/01-foundations.yaml:289` |
| Project "Proof portfolio: martingales": prove optional stopping (bounded case), Doob's maximal inequality and the martingale convergence theorem, then verify each numerically on simulated paths. Deliverable "Typeset proofs plus verification notebook." Grading `both` | `curriculum/01-foundations.yaml:290-297` (brief 292-295, deliverable 296, grading 297) |
| No `debate:` key | `curriculum/01-foundations.yaml:261-297` (absent) |
| No `atlas` key on the project; no Atlas milestone names M6 | `curriculum/meta.yaml` (no `M6` match anywhere; planner grep) |
| JSON row mirrors the YAML (id at line 6500; hours 150; prereqs M4, M5; 15 `introduces`; sources; lab; grading `both`) | `curriculum/curriculum.json:6500` |
| Topological position 20 (after M5 at 13, M4 at 12) | `curriculum/curriculum.json` `topological_order` |
| Hub row in the rendered curriculum | `CURRICULUM.md:244` (`M6 · Measure-Theoretic Probability · M · 150 h · ← M4, M5`) |
| Downstream: AP1 requires M6 | `curriculum/03-markets.yaml:268` (prereqs `[M6, AP2, FC1, FC2, M8, E4]`, module AP1) |
| Downstream: SC1 requires M6 | `curriculum/03-markets.yaml:509` (prereqs `[M6]`, module SC1) |

**Count check.** The curriculum hours 150 (`:264`) are the only figure the tools check. The plan derives lesson and
project counts below from them; the 15-concept count matches the rows in §2 one-to-one.

### 0.1 Prerequisite closure (computed)

Planner walk of `curriculum/curriculum.json` (`parts[].modules[].prereqs`): closure of M6 = **{M1, M2, M4, M5, P0.1}**.
Concepts usable without definition (68 in total):

- M1 (14): `exponential-and-logarithm`, `compounding-frequency`, `continuous-compounding`, `present-value`,
  `discount-factor`, `geometric-series`, `annuity`, `perpetuity`, `growing-perpetuity`, `amortization-schedule`,
  `quantifiers`, `direct-proof`, `proof-by-contradiction`, `mathematical-induction`.
- M2 (13): `limit`, `derivative`, `taylor-theorem`, `definite-integral`, `partial-derivative`, `gradient`, `jacobian`,
  `hessian`, `multiple-integral`, `implicit-function-theorem`, `envelope-theorem`, `finite-difference-derivative`,
  `automatic-differentiation`.
- M4 (19): `random-variable`, `expectation`, `variance`, `independence`, `correlation`, `covariance-matrix`, `skewness`,
  `kurtosis`, `quantile-function`, `moment-generating-function`, `characteristic-function`, `normal-distribution`,
  `multivariate-normal`, `student-t-distribution`, `conditional-expectation-elementary`, `law-of-large-numbers`,
  `central-limit-theorem`, `heavy-tailed-distribution`, `infinite-variance-clt-failure`.
- M5 (11): `completeness-of-reals`, `cauchy-sequence`, `epsilon-delta-continuity`, `uniform-convergence`, `compactness`,
  `metric-space`, `contraction-mapping`, `banach-fixed-point-theorem`, `bellman-operator-contraction`,
  `value-function-iteration`, `riemann-stieltjes-integral`.
- P0.1 (11): `evidence-grade`, `paper-anatomy`, `identification`, `robustness-check`, `replication`, `steelmanning`,
  `project-ladder`, `prerequisite-dag`, `atlas-platform`, `citation-registry`, `notation-conventions`.

Concepts that natural M6 content would use but that lie **outside** the closure (see §8 DAG problems):
`orthogonal-projection`, `vector-space` (M3); `markov-property`, `brownian-motion` (SC1); `test-supermartingale` (S7);
`monte-carlo-integration`, `pseudo-random-number-generator` (M8); `expected-value-game` (PC3).

---

## 1. Hours and the tool rules (feasible; no STOP condition)

Rules (read): lesson `data-hours` 6–12 (`tools/check_pages.py:227-228`); hub `data-hours-lessons + data-hours-project`
must equal the curriculum figure (`check_pages.py:337-338`); project 10–40 % of module hours (`check_pages.py:339-340`,
i.e. **15 to 60 h**); lessons sum to the hub's lessons figure (`check_pages.py:341-342`).

Constraint: lessons L in [6n, 12n] for n lessons, and project 150 − L in [15, 60], so L in [90, 135].

Chosen split: **12 lessons × 9 h = 108 h; project 42 h (28 %)**. Alternatives that also satisfy the rules: 10 × 9 + 60 h
project (40 %, at the limit), or 11 lessons × 9 h with a 51 h project (34 %). Architect decision Q6.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to M6)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3–§8, `plans/M1-build-plan.md`,
`plans/E1-build-plan.md` (§2.1 carried-over verification lessons), `plans/M5-build-plan.md` (Architect decisions),
`plans/CF1-build-plan.md`, this file. Study `course/modules/M/M1/` (hub, project, grader panel, cards) and
`course/modules/AC/AC1/` (cards.json and project layout) for structure. Imitate structure, not wording.
`course/templates/` holds hub.html, lesson.html, project.html, studio.html.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) and
   rounded only at display. A page that shows a rounded figure states its rounding (precedent E1 §2.1.1, AC4 KNOWN 3).
   Probabilities in the labs are exact `Fraction`s; money is integer cents (rule 8).
2. **Lab statements match code and output.** The hypothesis names the result the lab prints; the interpretation names
   only what the printed numbers show (precedent M1 LESSON_TEXT_DEFECTS). Every "checked" claim names the lab, line or
   test that did the check.
3. **Attribute nothing unread.** Cite only the two registry keys in §7. No locator, page, theorem number or equation
   number is typed unless the builder read it in a source that reproduces it. Otherwise the result is stated, cited at
   book level with the locator field left empty, and graded C with basis "standard result, locator not confirmed".
4. **Scope words need a computation.** "every", "all", "never", "always", "almost surely", "any", "converges" and
   "measure theory" are used only where a proof, a finite exact enumeration or a lab computes the claim. Finite
   enumerations are grade C with the basis named, not T (precedent E1 §2.2). A simulation of paths illustrates a theorem;
   it never verifies an almost-sure statement, and the page says so.
5. **Define before use.** Each of the 15 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its
   assigned lesson and never before it. Terms outside the 15 and outside the closure (for example *measurable function*,
   *Lebesgue measure*, *almost surely*, *uniform integrability*, *submartingale*, *L^p space*, *Hilbert space*) appear
   in plain words at first use, with no `<dfn>` and no `data-concept`, per the M7/E1/AC4 precedent (§8, Q2).
6. **Theorem hypotheses explicit.** Every Theorem, Proposition and Lemma block lists its assumptions as numbered
   **Assumptions** (for example: \((\Omega,\mathcal F,\Prob)\) a probability space; \(\tau\) a stopping time with
   \(\tau \le N\) a.s.; \(X\) integrable) before the statement. The optional-stopping and convergence statements state
   each hypothesis, including the integrability condition.
7. **Grader tests demand an exception type only for conditions the page names.** The project spec lists each invalid-input
   condition and the exception type for it (§6.4). Any other invalid input may raise any exception or return a value.
   **Five alternative correct implementations must pass** the suite; the verifier writes them (§6.5).
8. **Integer cents for money.** Every money output of the engine (wealth, stakes, capital, expected final wealth) is an
   `int` number of cents, computed from exact `Fraction`s and rounded once, half up, by the rule stated on the project
   page. No float money, no tolerance on money (precedent E1 rule 8, AC4 Q9).
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own
   container; no element forces the page wider than 360 px (`page_smoke.py` checks it; builders do not run it).
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no
    `if __name__ == "__main__":` guard. `run_labs.py` runs each twin as `python -I -W error <twin>` (precedent E1 rule 10,
    M1 twin `tests/labs/M1/lab-M1-L04-1.py`).
11. **Define the symbols you use, and use only registered macros** (§5).

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. A derivation on the
  page is grade T only if every step is shown (BUILDER_RULES §3.5).
- Concepts: §3 table. `<dfn>` only for the 15 concepts of §3. Links to closure concepts use
  `href="../../../concepts.html#<id>"`; links to earlier lessons of M6 use `href="Lnn.html#def-<id>"`. A lesson never links
  a concept defined later. A concept outside the closure is never linked.
- Labs: code lives once in `tests/labs/M6/lab-M6-Lnn-1.py` and `lab-M6-project-1..3.py`. The page carries `@@LAB:<file>@@`
  and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Lab ids match `lab-M6-<page>-<n>` (`check_pages.py:258`).
  Standard library only (`fractions`, `itertools`, `math`, `random.Random(seed)` for any draw); no NumPy; no network;
  under 10 s in Pyodide; no warnings (`-W error`). Each lab is a finite exact computation or a seeded simulation, and says which.
- Labs use **no data files**. `data-files` is absent. No MANIFEST entry.
- SIMULATED label: only for simulated paths and generated instances (BUILDER_RULES §1.7). Exact enumerations are not labelled SIMULATED.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `notation/notation.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references
  in code comments.
- Banned strings (`tools/check_pages.py:58-72`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the scope",
  "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
  "obviously", "clearly", and any ellipsis outside code.
- Lesson template order (BUILDER_RULES §4.2; `check_pages.py:75` LESSON_SECTIONS): why-it-matters (≤120 words), core
  content, inline lab, canon-breaks, misconceptions (≥3), problems (≥3 in each of mechanics, proof, empirical, research,
  each with `<details class="solution">`), key-results, quiz (8–15 items with explanations), references.
  **No debate brief** (no `debate` key, §0).
- Tier M: rungs 1–2 are kept to the minimum (BLUEPRINT §4; BUILDER_RULES §5.1).
- Output contract: the BUILDER_RULES §10 block, with the hours line filled from §4 and the REFERENCE_REQUESTS,
  NOTATION_REQUESTS, GLOSSARY_REQUESTS, DAG_DEFECTS and KNOWN_LIMITATIONS lines. Report PASS only for checks actually run.
- No `git commit`, no push, no branch changes. Builders write only under `course/modules/M/M6/` and `tests/labs/M6/`.

---

## 3. Outline and file ownership (one row per lesson; concept assignment fixed)

Each concept of `introduces` (§0, lines 271–285) appears in exactly one row. Each lab twin is `tests/labs/M6/lab-M6-Lnn-1.py`.
Lessons 9 h each (inside 6–12, `check_pages.py:227-228`).

| Lesson | Title (working) | Concepts it defines (each once) | Lab twin id and content (one lab per lesson, planner proposal Q8) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Sigma-algebras and measurable events | `sigma-algebra` | `lab-M6-L01-1`: on a 4-point and a 6-point set, generate the sigma-algebra of a partition, count its members (2^k), and check complement and finite-union closure by enumeration (finite check, grade C) | 9 | A |
| L02 | Measure and probability spaces | `probability-space` | `lab-M6-L02-1`: exact `Fraction` check of the probability axioms on a finite space; a set function that fails additivity is rejected by the same check | 9 | A |
| L03 | The Lebesgue integral | `lebesgue-integral` | `lab-M6-L03-1`: integral of a simple function as \(\sum_i a_i\,\mu(A_i)\); dyadic simple-function approximation of \(x^2\) on \([0,1]\) with an error column converging to \(1/3\) (numerical, labelled as such) | 9 | A |
| L04 | Monotone and dominated convergence | `monotone-convergence-theorem`, `dominated-convergence-theorem` | `lab-M6-L04-1`: \(f_n = n\,\indic\{(0,1/n]\}\) on \([0,1]\): \(\int f_n = 1\) for all \(n\) while \(f_n \to 0\) pointwise on \((0,1]\); the domination hypothesis fails and the limit interchange fails | 9 | A |
| L05 | Product measures and Fubini's theorem | `fubini-theorem` | `lab-M6-L05-1`: \(f(x,y)=(x^2-y^2)/(x^2+y^2)^2\) on \([0,1]^2\): both iterated integrals computed in closed form (\(\mp\pi/4\)) and by quadrature; the integrability hypothesis fails (derivation on the page, grade T) | 9 | B |
| L06 | Densities and the Radon–Nikodym theorem | `radon-nikodym-theorem` | `lab-M6-L06-1`: finite space; \(d\nu/d\mu = \nu(\{x\})/\mu(\{x\})\) reproduces \(\nu(A)=\int_A (d\nu/d\mu)\,d\mu\) for all \(2^n\) events (exact); a point with \(\mu=0<\nu\) shows no density exists | 9 | B |
| L07 | Conditional expectation as an L2 projection | `conditional-expectation-l2` | `lab-M6-L07-1`: on a finite space, the L2 projection onto the partition-measurable functions equals the cell-average conditional expectation; orthogonality of the residual checked exactly | 9 | B |
| L08 | Filtrations and discrete-time martingales | `filtration`, `martingale` | `lab-M6-L08-1`: a fair ±1 walk with its natural filtration: \(\E[S_{k+1}\mid\mathcal F_k]=S_k\) checked exactly on a \(2^{10}\)-leaf tree; a biased walk fails the same check | 9 | B |
| L09 | Stopping times | `stopping-time` | `lab-M6-L09-1`: first hitting time of \(+1\) by the fair walk; the event \(\{\tau\le k\}\) is \(\mathcal F_k\)-measurable (checked by enumeration that it depends only on the first \(k\) steps) | 9 | C |
| L10 | Optional stopping and the doubling strategy | `optional-stopping-theorem`, `doubling-strategy` | `lab-M6-L10-1` (**the curriculum lab**): doubling with finite capital \(K\) (integer cents): exact ruin probability, expected final wealth equal to the start under the bounded stopping time, and the unbounded-time counterexample where \(X_\tau=1\) a.s. but \(\E X_\tau=1\neq 0=X_0\) | 9 | C |
| L11 | Doob's maximal inequality | `doob-maximal-inequality` | `lab-M6-L11-1`: \(\Prob(\max_{k\le N}X_k\ge\lambda)\le \E X_N/\lambda\) for a nonnegative submartingale \(X_k=|S_k|\), checked exactly for \(N\le 12\) over a grid of \(\lambda\) | 9 | C |
| L12 | Martingale convergence | `martingale-convergence-theorem` | `lab-M6-L12-1`: dyadic martingale \(M_n=\E[Y\mid\mathcal F_n]\) for \(Y(x)=x\) on \([0,1]\): \(\E[(M_n-Y)^2]=1/(12\cdot 4^n)\) exactly for \(n\le 10\); \(M_n\to Y\) along each path | 9 | C |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split, core reading | none | none | - | A |
| project | Proof portfolio: martingales (`both`) | none | `lab-M6-project-1` (rung 1), `lab-M6-project-2` (rung 2, `class="lab completion"`), `lab-M6-project-3` (rung 3 reference numbers) | 42 | D |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` | none | none | - | D |
| cards | `cards.json` from L01–L12 | none | none | - | E (after A–C) |

Totals: lessons 12 × 9 = **108 h**; project **42 h**; unit **150 h** = curriculum (`curriculum/01-foundations.yaml:264`).
Concept coverage: 1+1+1+2+1+1+1+2+1+2+1+1 = **15**, matching `:271-285`.

**Ordering check.** L02 uses L01's sigma-algebra; L03 uses L02; L04 uses L03; L05 uses L04 and M2 `multiple-integral`;
L06 uses L04; L07 uses L06 and M4 `conditional-expectation-elementary`; L08 uses L02 and M4 `expectation`; L09 uses L08;
L10 uses L08 and L09; L11 uses L08; L12 uses L07 and L08. Doubling is placed in L10 with optional stopping because the
curriculum lab (`:289`) is the finite-capital failure of optional stopping. Architect decision Q7 (alternative: L12).

**Lesson content guidance** (builders decide the argument; each lesson establishes its concept, nothing more):
- L01 covers finite and countable generation; the Borel sets are named in plain words only if used.
- L02 proves the basic consequences of the axioms (monotonicity, continuity from below) for the finite space and states the general case.
- L03 defines the integral for nonnegative simple functions first, then as a supremum (plain prose for "measurable function").
- L04 proves MCT for the nonnegative case by the simple-function approximation; DCT is stated with a proof sketch that names the steps it skips, or proved from MCT (decision Q3).
- L05 states Fubini–Tonelli for finite products and proves the iterated-integral equality for finite sums; the general theorem is stated (Q3).
- L06 states the Radon–Nikodym theorem with its hypotheses (σ-finite, absolutely continuous); proof is not given (Q3); the finite case is proved in the lab.
- L07 defines conditional expectation in L2 as the orthogonal projection (plain prose "inner product", §8 Q1); proves uniqueness a.s. and the tower property for the finite case.
- L08 defines filtrations, adapted processes and martingales; proves the fair walk is a martingale.
- L09 proves \(\{\tau\le k\}\in\mathcal F_k\) for hitting times and the closure properties of stopping times (min, max, and \(\tau+1\)).
- L10 proves the bounded-time optional stopping theorem for a martingale and a bounded stopping time (Assumptions: \(\tau\le N\)); gives the doubling counterexample with the hypothesis that fails.
- L11 proves Doob's inequality for a nonnegative submartingale from the stopping time of first exceedance.
- L12 proves the martingale convergence theorem under \(L^1\)-boundedness via Doob's upcrossing lemma **only if** Q3 approves the length; otherwise the theorem is stated with the assumption list and the L2 special case (bounded second moment) is proved.

**Where the canon breaks** (every lesson): name the hypothesis whose failure breaks the result (doubling, unbounded τ,
non-domination, non-absolute continuity, non-integrability of the Fubini example, no L1 bound).

---

## 4. Hub (`index.html`, Builder A)

- `<html lang="en" data-root="../../../" data-unit="M6" data-page="index">`.
  `<main data-hours-lessons="108" data-hours-project="42">` (sums to 150; project 28 %, inside 10–40 %,
  `check_pages.py:337-340`).
- 4–8 `ol.objectives` items with measurable verbs. Target six: state and prove optional stopping for a bounded stopping time;
  compute Lebesgue integrals of simple functions and apply MCT and DCT to a sequence; decide whether a Fubini interchange is
  justified; construct a conditional expectation as an L2 projection on a finite space; verify the martingale property of a
  given process; bound a maximal function with Doob's inequality.
- Prerequisites: M4 and M5 (and M1, M2, P0.1 through them), with links to the closure concepts
  `../../../concepts.html#<id>` (for example `expectation`, `conditional-expectation-elementary`, `metric-space`,
  `cauchy-sequence`, `multiple-integral`, `limit`). **Links go to concept anchors, not to M4/M5 hub pages**, because those
  pages are not built yet (§8, Q5).
- Placement: `section.quiz#placement data-mastery="0.8"` (the bar used by M1 `plans/M1-build-plan.md` and AP1), with nine
  items. At least two `data-skill` items test what rungs 1–2 teach: the bounded optional-stopping expectation of a stopped
  fair walk, and the completion line of the doubling recursion. The rest test M4 and M5 prerequisites (expectation of a
  discrete variable, conditional expectation for a two-cell partition, Cauchy sequences).
- Lesson map: one card per L01–L12 with `data-progress-key="M6/Lnn"` and `data-hours` text.
- Ladder: four `li` with `span.rung-title` in the order `Worked example`, `Completion problem`, `Independent project`, `Stretch`
  (`check_projects.py:33`).
- Core reading: `ol.reading-list` with `li data-cite` for the two keys in §7 only.

---

## 5. Notation (`notation/notation.json`; binding)

Registered macros this unit uses (read in `notation/notation.json`): `\E` (line 5, expectation), `\Prob` (line 9,
probability measure), `\indic` (line 33, indicator), `\R` and `\N`, `\dto` and `\pto` (lines 45 and 49, convergence in
distribution and in probability).

Registered symbols that M6 must **not** give another meaning (`notation.json` symbols, lines 112–147 and onward):
- **`T`** (line 112) means the number of return observations in S1. M6 uses **N** for a horizon and never T for time.
- **`\mathbb{Q}`** (line 147) means an equivalent martingale measure compared with \Prob (AP1). M6's Radon–Nikodym lesson
  uses **\nu** for the second measure, not \mathbb{Q}.
- **`R^\ast`** (line 132) and **`\Phi, \Phi^{-1}`** (line 117): not used by M6.

Local letters (`notation.json` `about`: sigma, mu are local per lesson): \mu, \nu, \sigma, \tau are defined in each lesson where used.
Stopping time: **\tau**. Filtration: **\mathcal F_n**. Sigma-algebra: **\mathcal F** (on the space \(\Omega\)).

**NOTATION_REQUESTS (for the architect; no macro is added by a builder):**
- almost-sure convergence arrow, e.g. `\xrightarrow{\text{a.s.}}`;
- an L^p norm macro, e.g. `\norm{\cdot}_p` (M5's architect decisions define `\norm` locally, not as a registered macro, `plans/M5-build-plan.md` Architect decisions Q1; the registry does not hold it);
- predictable process symbol (for the doubling bet \(H_k\), which is \(\mathcal F_{k-1}\)-measurable);
- a second-measure symbol if \nu is judged too generic.

---

## 6. Project ladder, spec and grader (Builder D)

Project page: `course/modules/M/M6/project.html`, `<main data-hours-project="42">`. Grading text names **both**:
"Grading: both. The autograder runs the verification engine; the rubric grades the typeset proofs."
Deliverable: typeset proofs plus `martingale_checks.py` (the verification engine). The "verification notebook" of the
curriculum (`:296`) is **not a tool-supported deliverable type**; the plan interprets it as the engine plus its printed
report (Q5). Confirm before Builder D starts.

### 6.1 Ladder (BLUEPRINT §5.1; `check_projects.py:33` requires the order)

- **Rung 1 · Worked example** (`lab-M6-project-1`, skippable on placement): the bounded optional-stopping expectation for one
  fully solved fair walk with a stopping rule \(\tau\le N\): every step annotated with *why* (adaptedness of \(\tau\), the
  stopped-martingale identity, the hypothesis that makes it hold). Exact `Fraction`.
- **Rung 2 · Completion problem** (`lab-M6-project-2`, `class="lab completion"`): the doubling wealth recursion for finite
  capital \(K\) (integer cents) with `___` blanks at the cap and the ruin test; the twin is the completed solution; graded
  instantly.
- **Rung 3 · Independent project**: the proofs (the three named theorems: optional stopping, bounded case; Doob's maximal
  inequality; the martingale convergence theorem) and the engine `martingale_checks.py` (§6.3).
- **Rung 4 · Stretch** (not graded): the same checks for a martingale built from an arbitrary bounded predictable bet, or the
  convergence rate of the dyadic martingale in \(L^p\) for \(p\ne2\), with a stated hypothesis.

### 6.2 Spec (`dl.spec` with dt: Context, Inputs, Required outputs, Constraints, Grading; `check_projects.py:34`)

- **Context:** the proof portfolio for the three martingale theorems that the later modules AP1 and SC1 (`03-markets.yaml:268`,
  `:509`) use, with each theorem's hypotheses checked on generated cases.
- **Inputs:** generated instances from `make_instance(seed)` (§6.3). No dataset. Every instance is **SIMULATED**.
- **Required outputs:** `martingale_checks.py` with the five functions in §6.3; `proofs.html` (typeset, students' own); the
  printed verification report for seed 0.
- **Constraints:** standard library only; integer cents for money; exact `Fraction` for probabilities; every printed number
  computed from unrounded values and rounded once, half up, as the spec states; the proofs state every assumption.
- **Grading:** both. The autograder checks the engine (§6.3); the rubric grades the proofs (§6.5).

### 6.3 Autograder: `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py`

Grader panel: `section.grader-panel#grader data-unit="M6" data-grader="grader/" data-suite="test_project.py"
data-support="instance.py" data-solution="martingale_checks.py" data-starter="starter.py" data-packages=""`
(`check_projects.py:122-135`). No `data-packages`: standard library only.

- `make_instance(seed: int) -> dict`: deterministic. Generates a horizon \(N\in\{4,\dots,10\}\) (so exact enumeration is at most
  \(2^{10}\) leaves), a capital \(K\) in integer cents, a stake schedule in integer cents, and a barrier \(\lambda\) in cents.
  A fair coin (\(p=1/2\)) for every martingale case and a biased coin (\(p\ne 1/2\)) as the non-martingale control. Only valid
  instances: \(N\ge1\), \(K>0\), stakes \(\ge0\) and \(\le\) capital. Docstring: "generated inputs, SIMULATED". Seeds 0–49 must give
  materially different answers, not only different labels.
- `reference.py`: the full solution. Passes every test on seeds 0–49 (`run_graders.py --unit M6 --seeds 0-49`).
- `starter.py`: stubs raising `NotImplementedError`. The suite must fail on it (`run_graders.py` checks this).
- `test_project.py`: property and number checks, each against the instance's own parameters, never a hard-coded answer:
  - optional stopping, bounded case: \(\E X_\tau = X_0\) exactly for every bounded stopping time generated, to `Fraction` equality;
  - Doob's inequality: \(\Prob(\max_{k\le N}X_k\ge\lambda)\le \E X_N/\lambda\) on the grid of \(\lambda\) values, exact;
  - doubling with finite capital: ruin plus win probabilities sum to 1; expected final wealth in integer cents equals the
    rounded exact value (half up, once); no bet exceeds capital;
  - dyadic martingale: \(\E[(M_n-Y)^2]=1/(12\cdot 4^n)\) exactly for \(n\le 10\), and the path values approach \(Y\);
  - the fair walk satisfies the martingale identity; the biased walk does not (the control).
  - edge cases: horizon 1; a stopping time equal to the horizon; capital equal to the first stake.
- Exception table (only these; BUILDER_RULES rule 7, E1 precedent): `ValueError` naming the condition for: \(N<1\); \(K\le0\);
  a stake larger than the capital; \(\lambda\le0\) in Doob; a stopping rule that is not bounded by \(N\) in the bounded
  optional-stopping function. Any other invalid input may raise any exception or return a value; the tests do not assert a type.
- Failure messages name the violated property and hint at the concept. They never print the answer.
- Mutants (ten, §6.6). Five alternative correct implementations (§6.5).

### 6.4 Exception table and integer-cent rule

Rounding: each money output is rounded once, half up, to the nearest cent, from the exact `Fraction`. The page states this
rule (rule 8).

### 6.5 Five alternative correct implementations (verifier-written; must all pass)

Written by the verifier as test-only fixtures under `ledgers/M6/scripts/alternatives/` (precedent: E1 §6, M7 Q7, and not M4's
builder-written variant). (1) Closed-form doubling wealth by a sum over stopping levels; (2) a dictionary dynamic program over
wealth states; (3) recursion over the \(2^N\) paths with `Fraction`; (4) float evaluation with the stated rounding rule, accepted
within 1 cent after the half-up rounding; (5) a matrix (transition) formulation of the finite-capital chain.

### 6.6 Ten student-error mutants (verifier-written; each must fail at least one test)

Written as complete solution modules in `ledgers/M6/mutants/<name>.py`, docstring first line naming the error. Each must be killed
by `test_project.py` on seeds 0–9 (`mutate_graders.py --unit M6 --seeds 0-9`).

1. Lookahead: the doubling bet at step k uses the outcome of step k (the bet is not \(\mathcal F_{k-1}\)-measurable).
2. Stopping not capped at the horizon: \(\tau\) may exceed \(N\), so the bounded optional-stopping hypothesis is silently dropped.
3. Doob's inequality with \(\E X_N^2\) in place of \(\E X_N\) (wrong power in the bound).
4. Capital ignored: a bet larger than the remaining capital is accepted and wealth goes negative.
5. Ruin not counted: expected final wealth is computed over winning paths only.
6. Floor instead of half-up rounding of the expected cents (a one-cent error on some seeds).
7. Maximal probability taken over \(k\le N-1\) (horizon off by one).
8. Dyadic conditional expectation uses the cell's left endpoint instead of the midpoint.
9. Win probability hard-coded to \(1/2\), so the biased control passes the martingale test.
10. A hard-coded answer for seed 0 (returns the seed-0 constant when the seed is 0).

### 6.7 Time budget (`section#hours`, rows must sum to the declared 42)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1 worked example | 3 | Read and annotate one stopped-martingale computation |
| Rung 2 completion | 4 | Fill the cap and ruin lines, then run the instant check |
| Proofs: optional stopping, Doob's inequality, convergence | 17 | Three typeset proofs with every assumption stated (the convergence proof is the longest) |
| Engine `martingale_checks.py` with tests and exact enumeration | 10 | Five functions, exact Fraction and cents, edge cases |
| Verification report for seed 0 | 5 | Printed numbers, rounding statement, what the simulation does and does not show |
| Self-assessment against the exemplars | 3 | Score the rubric, compare with the annotated scoring |
| **Total** | **42** | Equals `data-hours-project` on the hub |

Check: 3 + 4 + 17 + 10 + 5 + 3 = 42.

### 6.8 Rubric (proofs; `both` requires it, `check_projects.py` rubric checks lines 58–73, 138–139)

Five criteria, four observable levels each, with an exemplar at level 4 and at level 2 (exemplars at two or more levels; `data-level`
1–4; `check_projects.py:58-72`):
- C1 Hypotheses: every theorem lists its numbered Assumptions (adaptedness, boundedness of \(\tau\), integrability).
- C2 Proof steps: every step is justified by a named lemma or definition; no step is skipped without a stated gap.
- C3 Numbers: every printed value is recomputed from unrounded values, with its rounding named.
- C4 Scope: the proof claims only what it proves (for example, not almost-sure statements from finite simulations).
- C5 Inequalities and constants: direction and constants are correct (Doob's constant; the \(1/(12\cdot4^n)\) identity).

Exemplars: A (level 4) and B (level 2), with annotations mapping each passage to descriptors. The verifier calibrates them blind
(VERIFIER §2.6; within one level per criterion). The self-assessment form and the divergence display follow S7/AP1.

---

## 7. Cards builder (Builder E, after A–C)

- `course/modules/M/M6/cards.json`, ids `M6-c001` upward, `lesson` in L01–L12, one atomic card per definition, theorem
  statement, key identity, lab result and misconception (BUILDER_RULES §7; `check_pages.py:366-398`).
- Grade T for each proved theorem and derived identity (each with its `basis`, for example
  `"basis": "Lab 10, doubling counterexample"`); grade C with `cite` for a stated-not-proved result (§3, Q3).
- Cards cite a registry key only for a result the lesson states without proof. M6 has no empirical claims.

---

## 8. Registry keys the module may cite

Verified in `references/references.json` (planner read each record):

| Key | Record | Status | Use in M6 |
|---|---|---|---|
| `williams1991probability` | Williams, *Probability with Martingales*; Cambridge University Press; Crossref monograph; year 1991 (`references/references.json:23047`); `used_by: ["M6"]` | verified | curriculum source for the martingale results (L08–L12); book-level citation; a locator only after it is read |
| `billingsley2012probability` | Billingsley, *Probability and measure*; Wiley; Open Library; year 2012 (`references/references.json:2661`); `used_by: ["M6"]` | verified | curriculum source for measure and integration (L01–L06); the curriculum string "anniversary ed." is not confirmed by the record (no edition field; Q4) |

Not usable from M6 without architect approval (Q4): `rudin1976principles` and `abbott2015understanding` (`used_by: ["M5"]`);
`blitzstein2019introduction` (`used_by: ["M4"]`). The M6 pages cite only the two M6 keys.

### 8.1 REFERENCE_REQUESTS

- None is required by the curriculum. Standard results used without proof (Q3) are cited at book level to `billingsley2012probability`
  with no locator and graded C. If the architect wants a locator-level citation for MCT, DCT, Fubini or Radon–Nikodym, the request is
  a locator read from the source (not from memory), through `add_reference.py` if the key needs a new record.
- Builders must not type a theorem number, page or equation number for any result.

---

## 9. Real-data policy

- **No real data.** M6 is measure theory and proof. Labs and the autograder use exact finite spaces, closed forms and generated paths.
- Generated paths and instances are labelled **SIMULATED** on every page and in the grader docstring (BLUEPRINT §5.3).
- No dataset is embedded or read: no `data-files`, no MANIFEST entry, no DATA_REQUESTS.
- No FRED, Treasury or other public series is used. No redistribution check is needed.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

```bash
.venv/bin/python tools/check_pages.py --unit M6             # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit M6
.venv/bin/python tools/check_projects.py --unit M6
.venv/bin/python tools/embed_labs.py course/modules/M/M6/L01.html   # per page, after twins are written
.venv/bin/python tools/run_labs.py --unit M6                # --page L10 for one lesson
.venv/bin/python tools/run_graders.py --unit M6 --seeds 0-49
.venv/bin/python tools/mutate_graders.py --unit M6 --seeds 0-9      # verifier only
.venv/bin/ruff check tests/labs/M6 course/modules/M/M6/grader && .venv/bin/ruff format --check tests/labs/M6
.venv/bin/mypy                                                       # strict, repo configuration
```

Flags as read in each tool: `check_pages` (`--unit`, `--all`, `--page`; `check_pages.py:429`), `check_dag` (`--unit`,
`--all`; `check_dag.py:89`), `check_projects` (`--unit`, `--all`; `check_projects.py:159`), `run_labs` (`--unit`, `--all`,
`--page`; `run_labs.py:119-121`), `run_graders` (`--unit`, `--all`, `--seeds`; `run_graders.py:129-131`), `mutate_graders`
(`--unit`, `--seeds`; `mutate_graders.py:30-32`). The planner did not execute them against M6.

Not run by builders: `page_smoke.py` (verifiers only, quiet machine). Repo-wide gates (`check_pages.py --all`,
`build_site.py --check`, `render_curriculum.py`) are the architect's, once, before merge.

---

## 11. Tooling assumptions that do not hold for M6 (flagged)

1. **No Atlas milestone.** No `atlas` key and no meta entry names M6 (§0). `check_projects.py:144-146` does not apply; no
   `atlas/A*.contract.md` is needed or drafted.
2. **No debate.** `check_pages.py:412` does not require a debate brief.
3. **Both grading.** The rubric and two exemplars are required (`check_projects.py:58-73, 138-139`), not only the autograder.
4. **One curriculum lab, twelve lab twins.** The curriculum names one lab (`:289`); BUILDER_RULES §3.4 requires a numerical check
   for each key formula; the plan adds one per lesson (Q8, M1 precedent).
5. **Prerequisite modules unbuilt.** M4 and M5 have no pages under `course/modules/` and no ledgers (only M1, S7, AC1, AC2, AC4,
   AP1, CF1 exist). Prerequisite links go to concept anchors only (§4).
6. **Tier M rung rule.** Rungs 1–2 are minimal from tier M upward (BLUEPRINT §4). Rung 1 and 2 are kept short (3 h and 4 h).
7. **Notebook deliverable.** "Verification notebook" (`:296`) is not a tool-supported deliverable (§6). Decision needed (Q5).
8. **Runtime.** Exact enumeration to \(2^{10}\) leaves and the \(2^{12}\)-event check in L01/L06 must stay under 10 s in Pyodide; the
   builders time each twin under CPython and report it (a Pyodide timing claim is not made without `page_smoke`).

---

## 12. DAG problems (concepts natural M6 content would use outside the closure)

| Concept | Owner (outside closure) | Where it arises | Default resolution |
|---|---|---|---|
| `orthogonal-projection`, `vector-space` | M3 (`curriculum.json` concepts) | L07: L2 projection needs an inner product | plain prose, no link, no `<dfn>`; DAG_DEFECT recorded (Q1) |
| `markov-property`, `brownian-motion`, `continuous-time-martingale` | SC1 | would appear in a remark on continuous time | not used; M6 is discrete time only |
| `test-supermartingale` | S7 | the doubling counterexample | not used; described in plain words |
| `monte-carlo-integration`, `pseudo-random-number-generator` | M8 | the seeded simulations in labs | plain "seeded simulation" with `random.Random(seed)`; no link |
| `expected-value-game` | PC3 | the doubling strategy as a game | plain prose |

Terms used in prose but in no curriculum concept (NOT IN CURRICULUM as concepts): *measurable function*, *Lebesgue measure*,
*Borel sets*, *almost surely*, *uniform integrability*, *submartingale*, *L^p space*, *Hilbert space*, *Riesz–Fischer
completeness*, *predictable process*, *Doob upcrossing lemma*. Each is defined in plain words at first use, with no `<dfn>` (Q2).

Possible confusion of names: M6's `conditional-expectation-l2` (L07) extends M4's `conditional-expectation-elementary`. The L07 page
links the M4 concept and states the extension; it never redefines it.

---

## 13. Notation conflicts foreseen

- \(T\) for a time horizon collides with the registered S1 meaning (§5). Builders use \(N\).
- \(\mathbb Q\) for a second measure collides with the registered AP1 meaning (§5). Builders use \(\nu\).
- \(\E\) and \(\Prob\) must be the registered macros; a page that writes \(E\) or \(P\) is a defect.
- The almost-sure arrow, the \(L^p\) norm and the predictable-process symbol are not registered (§5 NOTATION_REQUESTS).

---

## 14. Open questions for the architect (numbered; each needs a decision before the named builder starts)

1. **Q1 (DAG, blocks L07 wording only).** The L2 projection needs an inner product, which is M3's `orthogonal-projection` and
   `vector-space` (outside the closure). Options: (a) plain prose with a DAG_DEFECT (planner recommends, per M2/M7/AC4 Q2 precedent);
   (b) add M3 as a prerequisite (curriculum change; M3 is `M1`-only, 150 h, topological index 6). Decide before L07 starts.
2. **Q2 (terms).** Confirm that the terms in §12 are plain prose at first use with no `<dfn>` and no link (M7/E1/AC4 precedent). The
   planner cannot add concepts to the curriculum.
3. **Q3 (proof scope; blocks L04–L06 and L12 and the project proofs).** Which standard results are proved and which are stated?
   Planner recommends: prove MCT (nonnegative case) and the bounded-time optional stopping theorem and Doob's inequality and the
   \(L^2\) martingale convergence case; **state without proof**, graded C with book-level citation and no locator: DCT (or prove it
   from MCT), Fubini–Tonelli beyond finite products, Radon–Nikodym, Riesz–Fischer, and the \(L^1\) convergence theorem (its upcrossing
   proof is long). Per BUILDER_RULES §2.2 and §8, a stated result is never graded T without a precisely cited proof.
4. **Q4 (sources).** Confirm the two keys in §8 only. The curriculum's "anniversary ed. (2012)" string for Billingsley is not
   confirmed by the registry record (no edition field); builders cite the key and do not repeat the edition string. Confirm
   whether `rudin1976principles` or `abbott2015understanding` (`used_by: ["M5"]`) may also be cited from M6.
5. **Q5 (deliverable).** "Typeset proofs plus verification notebook" (`curriculum/01-foundations.yaml:296`): planner proposes
   `proofs.html` plus `martingale_checks.py` and its printed report. A notebook is not a tool-supported deliverable. Confirm.
6. **Q6 (hours).** 12 × 9 h lessons plus a 42 h project (28 %) recommended. Alternatives: 10 × 9 h with a 60 h project (40 %, at the
   limit), or 11 × 9 h with a 51 h project (34 %). Confirm.
7. **Q7 (lesson placement).** Doubling is placed in L10 with optional stopping, so the curriculum lab is the L10 lab. The alternative
   is L12. Confirm.
8. **Q8 (lab count).** One lab per lesson (12 twins) plus three project labs, as in M1 Q2 and M5/M7. Confirm.
9. **Q9 (notation).** Approve the NOTATION_REQUESTS in §5 (almost-sure arrow, L^p norm, predictable process, second-measure symbol),
   and the local use of \(\tau\), \(\mathcal F_n\), \(\nu\). No registered macro is changed by a builder.
10. **Q10 (grader interface).** Freeze the five function signatures of `martingale_checks.py` in this plan before Builder D starts:
    `make_instance(seed) -> dict`; `stopped_value_expectation(instance) -> Fraction`; `doob_max_probability(instance, lam: int) ->
    tuple[Fraction, Fraction]` (probability and bound); `doubling_outcome(instance) -> dict[str, int | Fraction]`;
    `dyadic_martingale_error(instance, n: int) -> Fraction`. Architect to confirm or amend (M7 Q4 precedent).
11. **Q11 (exact versus simulated checks).** The curriculum asks to "verify each numerically on simulated paths" (`:293-295`). A
    simulation cannot verify an almost-sure or \(L^1\) statement. Planner recommends exact enumeration on finite trees plus one
    seeded simulation with a stated tolerance and the limitation stated on the page. Confirm.
12. **Q12 (sequencing).** M4 and M5 are not built. Confirm that M6 may be built now, with its prerequisite links as concept anchors
    (§4), or that M6 waits for the M4 and M5 ledgers to PASS (topological order puts M4 at 12, M5 at 13, M6 at 20).
13. **Q13 (rung length).** Tier M keeps rungs 1–2 minimal (BLUEPRINT §4). Rung 1 is 3 h and rung 2 is 4 h. Confirm.

---

## 15. Blocking issues

None blocks the hours (150 h admits a feasible split, §1). Decisions that must be made before the named builders start:
- **Q3 and Q1** before L04–L07 and L12 (what is proved and how the L2 projection is worded);
- **Q5** before Builder D writes the project spec (the deliverable type);
- **Q10** before Builder D writes `make_instance` and the five signatures;
- **Q12** before any M6 page is merged (the prerequisite pages do not exist yet).

---

## 16. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours).
2. Independent Haiku verifiers in fresh checkouts, slices: L01–L03, L04–L06, L07–L09, L10–L12, project. The project verifier writes
   the ten mutants (§6.6) and the five alternative implementations (§6.5), and runs `mutate_graders.py --unit M6 --seeds 0-9`.
   Scripts that back a row go under `ledgers/M6/scripts/` (VERIFIER_RULES §3).
3. Ledger at `ledgers/M6.verification.json`. Mutants under `ledgers/M6/mutants/`.
4. Branch: `claude/fanout-b3` is merged only when the unit ledger is PASS or its gaps are agreed.

---

## 17. Architect decisions

Pending. Each of Q1–Q13 in §14 needs a decision. Where the architect answers "follow the plan's recommendation", the
recommendation in §14 applies.

## Architect decisions (2026-10-28, binding). Where the plan states a recommendation for an open question, follow it. Defaults for every module: concepts outside the prerequisite closure are plain prose with no link and no dfn; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields only or not at all (never edit a record, never type bibliographic data); no real data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST in plans/<UNIT>-open-items.md; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every grader; not adversarial, no question bank.
Module specifics: 12 lessons and the 42 h project as in the plan; every theorem lists numbered Assumptions; infinite-sample-space results without a proof on the page are stated as numbered Assumptions (no grade, 'not proved here'); no Rudin/Williams locators unless read.
