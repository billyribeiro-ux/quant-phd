# E1 build plan: Microeconomics (2026-10-28)

Unit: **E1 · Microeconomics** · tier F · 120 h · prerequisite M2 · no Atlas milestone · no debate · grading `both`
(autograder + rubric) · output directory `course/modules/E/E1/` (part code `E`) · lab twins `tests/labs/E1/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits. Executors: Haiku builders, then
independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every curriculum statement below cites `file:line` read during planning. Anything not in the
curriculum is marked **NOT IN CURRICULUM**. Planner-derived closed forms in §6 are hand derivations to be re-derived
by the builder and checked by the verifier; they are not sourced.

---

## 0. Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part E, code `E`, title "Economics"; STUDIO-E requires E6, E7 (not E1) | `curriculum/02-economics-finance-core.yaml:4-8` |
| E1 id `E1`, title "Microeconomics" | `curriculum/02-economics-finance-core.yaml:18-19` |
| Tier `F`, hours `120` | `curriculum/02-economics-finance-core.yaml:20-21` |
| Prereqs `[M2]` (only) | `curriculum/02-economics-finance-core.yaml:22` |
| Core text: "Consumer and producer theory, demand and supply, elasticity, market structures, welfare, externalities, public goods." | `curriculum/02-economics-finance-core.yaml:23-25` |
| `introduces` has 13 concepts (listed in §3) | `curriculum/02-economics-finance-core.yaml:26-39` |
| Sources: one free-text string, "Varian, Intermediate Microeconomics, 9th ed. (2014)" | `curriculum/02-economics-finance-core.yaml:40-41` |
| Lab: "Comparative statics of a market equilibrium." | `curriculum/02-economics-finance-core.yaml:42` |
| Project "Market-structure lab"; brief: "Model an exchange-fee market under monopoly vs. Cournot vs. Bertrand competition, and quantify the welfare and fee outcomes."; deliverable "Model plus memo."; grading `both` | `curriculum/02-economics-finance-core.yaml:43-49` (brief 45-47, deliverable 48, grading 49) |
| No `debate:` key on E1 (no debate brief required) | `curriculum/02-economics-finance-core.yaml:18-49` (absent) |
| No `atlas:` key on the E1 project; no Atlas milestone names E1 (`E1` appears in meta.yaml only at lines 63, 70, 132, 155, none in the atlas block from line 198) | `curriculum/02-economics-finance-core.yaml:43-49`; `curriculum/meta.yaml:198` onward |
| JSON row for E1 matches the YAML (hours 120, prereqs M2, 13 concepts, sources, lab, project, grading both) | `curriculum/curriculum.json:7338` (`"id": "E1"`) |
| All 13 concepts map to module E1 in `concepts` | `curriculum/curriculum.json` `concepts` dict (checked by planner script: 13 owners = E1) |
| Registry key for Varian exists: `varian2014intermediate`, verified, Open Library book, year 2014, `used_by: ["E1"]`, source string matches the curriculum string | `references/references.json` entry `varian2014intermediate` |
| No registry entry for Cournot, Bertrand, Pigou, Coase, Lindahl, Edgeworth (grep of `references/references.json`: 0 hits each); "Samuelson" hits are unrelated (Samuelson 1979, PR3) | `references/references.json` (grep, planner) |
| `mascolell1995microeconomic` is verified but `used_by: ["E4"]` | `references/references.json` entry `mascolell1995microeconomic` |
| `nash1950equilibrium` is verified but `used_by: ["E2"]` | `references/references.json` entry `nash1950equilibrium` |
| Notation registry has no E1 symbols; letters such as `p`, `q`, `c` are local to lessons | `notation/notation.json` (`symbols`, `macros`); its `about` field says local letters are defined per lesson |
| Glossary is generated, present at `course/assets/data/glossary.json` | filesystem (planner `find`) |

### 0.1 Prerequisite closure (computed)

`prerequisite_closure("E1")` in `tools/coursekit.py` walks `prereqs` recursively. Planner recomputed the same walk from
`curriculum/curriculum.json`: closure = **{M2, M1, P0.1}**. Concepts usable without definition are the concepts introduced
by M2 (13), M1 (14) and P0.1 (11), 38 in total:

- M2 (`curriculum/01-foundations.yaml`, JSON row M2): `limit`, `derivative`, `taylor-theorem`, `definite-integral`,
  `partial-derivative`, `gradient`, `jacobian`, `hessian`, `multiple-integral`, `implicit-function-theorem`,
  `envelope-theorem`, `finite-difference-derivative`, `automatic-differentiation`.
- M1: `exponential-and-logarithm`, `compounding-frequency`, `continuous-compounding`, `present-value`,
  `discount-factor`, `geometric-series`, `annuity`, `perpetuity`, `growing-perpetuity`, `amortization-schedule`,
  `quantifiers`, `direct-proof`, `proof-by-contradiction`, `mathematical-induction`.
- P0.1: `evidence-grade`, `paper-anatomy`, `identification`, `robustness-check`, `replication`, `steelmanning`,
  `project-ladder`, `prerequisite-dag`, `atlas-platform`, `citation-registry`, `notation-conventions`.

Concepts that natural E1 content would use but that lie **outside** the closure (see §10 DAG problems):
`lagrange-multiplier`, `kkt-conditions`, `convex-set`, `convex-function` (all M7); `nash-equilibrium` (E2);
`expected-utility` (E3); `arrow-debreu-equilibrium`, `first-welfare-theorem` (E4).

---

## 1. Feasibility of the hours (no conflict)

The curriculum figure is 120 h (`curriculum/02-economics-finance-core.yaml:21`). The tool rules are:

- lessons: each `data-hours` 6-12 (`tools/check_pages.py` line 228);
- hub: `data-hours-lessons + data-hours-project = 120` (`check_pages.py` lines 337-338);
- project share 10-40% of 120, i.e. 12 to 48 h (`check_pages.py` lines 339-340);
- lessons sum to the hub's lessons figure (`check_pages.py` lines 341-342).

Chosen split: **9 lessons × 10 h = 90 h; project 30 h (25%)**. 90 = 9 × 10 satisfies 6-12 per lesson and 90 + 30 = 120.
Feasible; no STOP condition.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to E1)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `plans/M1-build-plan.md` (its Architect
decisions section is binding precedent for the same issues), `plans/AC4-build-plan.md` (§10 decisions), this file.
Study `course/modules/M/M1/` (hub, project, grader panel) and `course/modules/AC/AC4/` for layout. Imitate structure,
not wording. `course/templates/` holds the four skeletons.

### 2.1 Carried-over verification lessons (binding; each one was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) and
   rounded only at display. A page that shows a rounded figure says which rounding it uses. Precedent: AC4 KNOWN
   LIMITATION 3 (rounding half up; a variance differs from the exact fraction by 1/7 cent) and CF1 L01 Remark 5.2.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints; the interpretation
   names only what the printed numbers show. Precedent: M1 LESSON_TEXT_DEFECTS (a "checked directly" phrase with no
   lab behind it).
3. **Attribute nothing unread.** Only `varian2014intermediate` may be cited (§8). No locator, page or table is typed
   unless it was read. A textbook result without a confirmed locator is a derivation on the page (grade T) or is
   cited to the key at the book level with no locator. Precedent: AC2, AC4 §0 rule "never type a page or table from memory".
4. **Scope words need a computation.** "every", "all", "never", "always", "any", "market structures", "welfare",
   "externalities" are used only where a proof, a finite check, or a lab computes the claim. Precedent: the curriculum
   core text uses "market structures" (`yaml:24`), which covers more than the three structures the lessons treat (§10 Q8).
5. **Define before use.** Each of the 13 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its
   assigned lesson and never before it. A lesson uses a concept only after the lesson that defines it. Precedent: CF1
   and M1 open items. `check_dag.py` checks linked uses only, so every unlinked use of a concept name is checked by
   the verifier (VERIFIER §2.9).
6. **Proposition hypotheses explicit.** Every Theorem/Proposition block lists its assumptions (demand intercept
   positive, marginal cost constant, strict concavity where a first-order condition is claimed sufficient) before
   the statement.
7. **Grader tests demand an exception type only for conditions the page names.** The spec lists the invalid-input
   conditions and the exception type for each (§5.4). Any other invalid input may raise any exception or return.
   **Five alternative correct implementations must pass** the suite (closed form, iterated best response, linear-system
   solve, `Fraction` throughout, float with the stated rounding rule). The verifier writes all five (§5.6).
8. **Integer cents for money.** Every money output of the engine (fees, profit, surplus, deadweight loss) is an `int`
   in cents, computed from exact `Fraction`s and rounded once, half up, by the rule stated on the project page. No
   float money, no tolerance on money (precedent: AC4 Q9/Q10, planner recommendation adopted; see §10 Q6).
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their
   own container; no element forces the page wider than 360 px. `page_smoke.py` is the verifier's check.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no
    `if __name__ == "__main__":` guard. `run_labs.py` runs each twin as `python -I -W error <twin>` with no network
    (`tools/run_labs.py`, `run_twin`, around lines 51-60). The M1 twin `tests/labs/M1/lab-M1-L04-1.py` ends with `main()`.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation.
- Concepts: §3 table; `<dfn>` only for the 13 registered concepts. Terms outside the 13 may appear in prose and, if
  emphasised, as plain `<dfn>` without `data-concept` (§10 Q4). No `<a class="concept">` for a term outside the closure.
- Prerequisite links: `href="../../../concepts.html#<id>"` for M2, M1 and P0.1 concepts; `href="Lnn.html#def-<id>"`
  for earlier E1 lessons. A lesson never links a concept defined in a later lesson.
- Labs: code lives once in `tests/labs/E1/lab-E1-Lnn-1.py` (and `lab-E1-project-1..3.py`). The page carries
  `@@LAB:<file>@@` and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output by hand.
  Lab ids must match `lab-E1-<page>-<n>` (`check_pages.py` line 258). Standard library only (`fractions`, `itertools`,
  `math`); seeded RNG if any; no network; under 10 s in Pyodide; no warnings (`-W error`).
- SIMULATED label: only for simulated data (BUILDER_RULES §1.7). Exact computations and closed-form checks are not
  labelled SIMULATED (precedent: M1 and CF1 open-item defects on exact labs).
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`,
  `course/concepts.html`, `course/assets/data/*`, `references/*.json`). Request changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report), no planning
  references in code comments (precedent: M1 defect "Convention (project Q5)"; AC4 KNOWN 9).
- Banned strings (`tools/check_pages.py` lines 58-72): TODO, TBD, lorem, "for brevity", "details omitted",
  "beyond the scope", "left as an exercise", "you can add more", "it is important to note", "studies show",
  "experts agree", "it is well known", "obviously", "clearly", and any ellipsis `...` outside code.
- Percent changes state the base and the direction (precedent: CF1 L07 Misconception 2).
- A finite enumeration is grade C with its basis named, not grade T (precedent: M1 L06 key-results defect).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration (precedent: CF1 KNOWN 3).
- Quiz explanations are read against their lesson (precedent: CF1 KNOWN 6).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES
  §10 output contract.

---

## 3. Outline and file ownership (fixed by this plan; the architect confirms)

Lessons: 9 × 10 h = 90 h. Concepts: 13, each in exactly one row. Concept counts per row sum to 1+1+1+2+1+2+2+1+2 = 13.

| Lesson | Title (working) | Concepts it defines (`introduces`, yaml 26-39) | Lab (twin id, tests/labs/E1/) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Consumer choice | `utility-maximization` | `lab-E1-L01-1`: the consumer optimum on a grid against the closed form; MRS equals the price ratio at the optimum | 10 | Builder A |
| L02 | Producer choice and cost | `profit-maximization` | `lab-E1-L02-1`: profit-maximising output for a cost function with fixed cost; price equals marginal cost | 10 | Builder A |
| L03 | Competitive equilibrium | `competitive-equilibrium` | `lab-E1-L03-1`: linear demand and supply; exact equilibrium with `Fraction`; market clears | 10 | Builder A |
| L04 | Demand responsiveness and comparative statics | `price-elasticity`, `comparative-statics` | `lab-E1-L04-1` (**the curriculum lab**, yaml 42): an equilibrium shift from a demand-intercept change, implicit-function derivative against a finite difference | 10 | Builder B |
| L05 | Monopoly pricing | `monopoly` | `lab-E1-L05-1`: monopoly price on linear demand; the Lerner index equals 1/\|ε\| at the optimum | 10 | Builder B |
| L06 | Oligopoly: Cournot and Bertrand | `cournot-competition`, `bertrand-competition` | `lab-E1-L06-1`: Cournot reaction-function iteration converges to the symmetric quantity; Bertrand fee equals marginal cost | 10 | Builder C |
| L07 | Surplus and deadweight loss | `economic-surplus`, `deadweight-loss` | `lab-E1-L07-1`: surplus integrals in exact arithmetic; deadweight loss of monopoly and Cournot against the competitive benchmark | 10 | Builder C |
| L08 | Pareto efficiency | `pareto-efficiency` | `lab-E1-L08-1`: a two-consumer exchange economy on a grid; the allocations with no Pareto improvement on the grid | 10 | Builder D |
| L09 | Externalities and public goods | `externality`, `public-good` | `lab-E1-L09-1`: a Pigouvian wedge equal to the marginal external cost; vertical summation of willingness to pay for a public good | 10 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 90/30 | none | none | - | Builder A |
| project | Market-structure lab (`both`, §5-§6) | none | `lab-E1-project-1` (rung 1), `lab-E1-project-2` (rung 2, `class="lab completion"`), `lab-E1-project-3` (rung 3 check) | 30 | Builder E |
| grader | `grader/reference.py`, `starter.py`, `instance.py`, `test_project.py` | none | none | - | Builder E |
| cards | `cards.json` from L01-L09 | none | none | - | Builder F (after A-E) |

Ownership rule: each builder writes only its lesson files and twins. Builder A writes the hub after L01-L03 exist, so the
lesson map is right; the hub cross-check runs at integration. Builder E's grader is independent of the lessons.

Ordering check (no lesson links a later definition):
- L01 uses only M2 derivatives and partial derivatives (`derivative`, `partial-derivative`, `gradient`).
- L02 uses L01's consumer language only in prose; the profit function uses `derivative`.
- L03 uses L02 (`profit-maximization`) for the supply curve.
- L04 uses L03 (`competitive-equilibrium`) and M2 (`implicit-function-theorem`).
- L05 uses L02 (profit) and L04 (`price-elasticity`) for the Lerner index.
- L06 uses L05 (`monopoly`) as the benchmark and L04 for reaction slopes.
- L07 uses L03 (demand and supply), L05 and L06 (outcomes), and M2 (`definite-integral`).
- L08 uses L01 (`utility-maximization`) and L07 (`economic-surplus`) in prose.
- L09 uses L07 (`economic-surplus`, `deadweight-loss`) and L08 (`pareto-efficiency`).

Hours check: 9 × 10 = 90 (lessons, hub `data-hours-lessons="90"`); project 30 (hub `data-hours-project="30"`); 120 total.

---

## 4. Hub (`index.html`, Builder A)

- `<main data-hours-lessons="90" data-hours-project="30">` (sums to 120; project 25%).
- 4-8 measurable objectives (verbs such as derive, compute, compare, prove). Example: "Derive the monopoly price from the
  first-order condition on linear demand."
- Prerequisites: M2 with links to the concept index anchors (`../../../concepts.html#<id>`) for the M2 concepts used.
  Do not link an unbuilt M2 page. The M2 unit is not built (`course/modules/M/` has only M1, verified by listing).
- Placement diagnostic: `<section class="quiz" id="placement" data-unit="E1" data-page="placement" data-mastery="0.8">`.
  The bar 0.8 matches the M1 and AP1 precedent (`course/modules/M/M1/index.html`, placement section). At least two
  items carry `data-skill` and test the skills rungs 1-2 teach (the monopoly first-order condition from the worked
  example, and the Cournot reaction-function completion step). The other items test M1 and M2 prerequisites: derivative,
  partial derivative, the implicit-function derivative, exponential growth, and induction-free direct proof.
- Lesson map linking L01-L09 (`href="L01.html"` … `L09.html`), and `project.html`.
- Project ladder: `ol.ladder` with four `rung-title` entries in order (worked example, completion, independent, stretch).
- Tier F: rungs 1-2 keep full length (BLUEPRINT §4: the minimum applies from tier M upward).

---

## 5. Project (`project.html`, Builder E): ladder, spec, grader

### 5.1 Ladder (BLUEPRINT §5.1; check_projects.py line 33 requires the order)

1. **Rung 1, worked example** (`lab-E1-project-1`): one fully solved, annotated monopoly, Cournot and Bertrand
   outcome on the reference case (a = 120, b = 1, c = 20, all integers; cents and trades per §5.2). Each step has a
   "why" annotation.
2. **Rung 2, completion** (`lab-E1-project-2`, `class="lab completion"`): the Cournot reaction-function step and the
   welfare line removed (`___`). Graded instantly. Its twin is the completed solution; every page line equals the twin
   line or contains a blank (`tools/run_labs.py` docstring, completion rule).
3. **Rung 3, independent project** (graded): (a) the autograded engine `market_structure.py` to the §5.3 interface,
   and (b) the memo, rubric-graded (§5.5). `lab-E1-project-3` is the rung-3 check, which calls the engine on the
   reference case and prints the outcome table.
4. **Rung 4, stretch** (optional, not graded): a third symmetric exchange (Cournot with n = 3) with the closed form
   stated and tested, or a demand curve that is not linear, with the outcome comparison stated as a hypothesis.

### 5.2 Spec (`dl.spec`; check_projects.py lines 34-49 require the terms and the grading words)

Terms: Context (2-4 sentences), Inputs, Required outputs, Constraints, Grading.

- **Context.** An exchange sets a per-trade fee for access to a market. The fee-setting structure (one exchange,
  two exchanges competing on quantity, two exchanges competing on fee) changes the trade volume, the fee, and the
  welfare split. The question is how much.
- **Inputs (proposed, §10 Q4).** Integers `a`, `b`, `c` with `a > b*c > 0`:
  - `a` (cents per trade): the choke fee, the fee at which trade volume is zero;
  - `b` (trades per cent): the slope of trade demand;
  - `c` (cents per trade): the constant marginal cost of a trade to the exchange.
  Trade demand is `Q(f) = a - b*f` trades at fee `f` cents, so the inverse demand is `f(Q) = (a - Q)/b`.
  No real data is used (§9).
- **Required outputs.** `market_structure.py` with
  `outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]`, where `structure` is one of `"monopoly"`,
  `"cournot"`, `"bertrand"`. Keys, all `int`: `volume_trades`, `fee_cents`, `profit_cents`, `consumer_surplus_cents`,
  `welfare_cents`, `deadweight_loss_cents`. Plus a memo `memo.md`.
- **Constraints.**
  - Integer cents: each money key is computed from exact `Fraction`s and rounded once, half up, to the nearest cent.
    The rounding rule is stated on the page, in the spec and in the module docstring.
  - Valid input: `a > b*c > 0`, `a`, `b`, `c` integers (see the exception table, §5.4).
  - Standard library only; no network; the same code runs in Pyodide and under pytest.
- **Grading.** Autograder (`grader/test_project.py`, dual-mode) and rubric (`rubric-self`, §5.5). The spec must name
  both the autograder and the rubric (check_projects.py lines 38-49).
- **Reading list.** `ol.reading-list` cites `varian2014intermediate` only (§8).

### 5.3 Planner's reference closed forms (to be re-derived by the builder; §10 Q4)

With `d = a - b*c > 0`:

| Structure | Volume (trades) | Fee (cents) | Derivation (short) |
|---|---|---|---|
| Monopoly | `d/2` | `(a + b*c)/(2*b)` | maximise `(f - c)*Q(f)`; first-order condition `a - 2*b*f + b*c = 0` |
| Cournot, 2 exchanges | `2*d/3` (each `d/3`) | `(a + 2*b*c)/(3*b)` | profit `((a - Q)/b - c)*q_i`; symmetric first-order condition `a - 2*q - b*c - q = 0` with `Q = 2q` |
| Bertrand, 2 exchanges | `d` | `c` | fees undercut to the marginal cost; trade volume is the full demand at `c` |

Checks the planner did by hand (the builder re-derives them; the verifier re-checks them):
- ordering: `d/2 < 2d/3 < d` and `(a + b*c)/(2b) > (a + 2bc)/(3b) > c`; the first difference is `(a - b*c)/(6b) > 0`;
- welfare on the linear demand, with `W(Q) = (a*Q - Q^2/2)/b - c*Q`, gives the deadweight loss against the competitive
  volume `d`: `DWL(Q) = (d - Q)^2 / (2b)`. Monopoly: `d^2/(8b)`. Cournot: `d^2/(18b)`. Bertrand: `0`.

Reference case for rung 1 (a = 120, b = 1, c = 20): `d = 100`; monopoly volume 50, fee 70; Cournot volume 200/3,
fee 160/3; Bertrand volume 100, fee 20. These must be recomputed by the builder with `Fraction`; the planner's values
are the hand check only.

### 5.4 Exception table (grader tests demand these, and only these)

| Condition the page names | Exception | Message must name |
|---|---|---|
| `structure` not one of the three names | `ValueError` | the allowed names |
| `a <= b*c` (no positive trade volume) or `b <= 0` or `c < 0` | `ValueError` | the condition violated, e.g. "a must exceed b*c" |

Any other invalid input may raise any exception or return; the tests do not require a type for it.

### 5.5 Rubric (memo; `both` requires it, check_projects.py `rubric_problems`, lines 58-73)

Six criteria, each with four observable levels (level 4 down to level 1). Examples of required observability:
1. **Model.** States the demand, the cost and the timing of each structure. Level 4: lists `a`, `b`, `c` with units and
   the three structures' assumptions. Level 1: "a simple model".
2. **Derivations.** Shows each first-order condition. Level 4: every step shown, with the fee and volume reproduced.
3. **Welfare.** Reports the deadweight loss against the competitive benchmark, with the integer-cent rule stated.
4. **Comparison.** Orders the three outcomes and states the sign of each difference, with its number.
5. **Recommendation.** Names the structure an exchange regulator should accept and what would change it.
6. **Limits.** States linear demand, constant cost and two exchanges as limits, and what changes without them.

Exemplars: **exemplar-a (level 4)** and **exemplar-b (level 2)**, fully written, annotated with the descriptors they meet or
miss. Self-assessment form (`section.rubric-self`, `data-rubric="rubric"`, `data-exemplars="exemplar-a exemplar-b"`,
as in M1). The page shows where the student's scores diverge from the exemplar scores.

Adversarial question bank: not required (the memo is not an IC defence or debate; §10 Q9).

### 5.6 Time budget (`<table id="hours">`, sums to 30 h)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One solved reference case, annotated line by line |
| Rung 2, completion problem | 3 | Fill the Cournot reaction step and the welfare line, then run the instant check |
| Model derivations (three structures, with proofs) | 8 | First-order conditions, reaction functions, ordering proof |
| Autograded engine `market_structure.py` and the test run | 8 | Implement to §5.2, pass the suite on seeds 0-49, handle the exception table |
| Welfare and fee analysis, memo draft | 6 | Compute surplus and deadweight loss in cents; write the memo |
| Self-assessment against exemplars | 3 | Score the memo, then compare with exemplar-a and exemplar-b |
| **Total** | **30** | Equals `data-hours-project` on the hub |

---

## 6. Grader design (Builder E)

**Files (no Atlas; solution is unit-local, check_projects.py line 145-146 does not apply).**
`course/modules/E/E1/grader/`: `instance.py`, `reference.py` (the solution; excluded from deployment, BLUEPRINT §7),
`starter.py` (stubs that raise `NotImplementedError`), `test_project.py`. The student file is `market_structure.py`
(§10 Q5).

Grader panel on `project.html`, as in M1: `<section class="grader-panel" id="grader" data-unit="E1"
data-grader="grader/" data-suite="test_project.py" data-support="instance.py" data-solution="market_structure.py"
data-starter="starter.py">`. `data-packages` is empty: standard library only.

- **`instance.py`**: `make_instance(seed: int) -> dict[str, int]`, deterministic per seed, returning `a`, `b`, `c` with
  `a > b*c > 0`. Labelled **SIMULATED** in the docstring: generated inputs, not market data. Seeds 0-49 give materially
  different outcomes (the volumes and fees change, not only the labels). Check on 20 sampled seeds by the verifier.
- **`reference.py`**: the full solution with `Fraction` and one half-up rounding per money output. Passes every test on
  seeds 0-49 (`run_graders.py --unit E1 --seeds 0-49`).
- **`starter.py`**: `NotImplementedError` stubs; the suite must fail on it (`run_graders.py` checks this).
- **`test_project.py`** (properties and numbers, no hard-coded answers; each test recomputes its expected value from the
  instance's `a`, `b`, `c` by an oracle written separately from `reference.py`):
  - the three volumes and fees match the §5.3 closed forms to the cent, after the stated rounding;
  - ordering: monopoly volume < Cournot volume < Bertrand volume; monopoly fee > Cournot fee > Bertrand fee = c;
  - Bertrand deadweight loss is 0 on every seed;
  - deadweight loss equals `(d - Q)^2/(2b)` to the cent for all three structures;
  - profit: monopoly profit is at least the sum of the two Cournot exchanges' profits; the Bertrand profit is 0;
  - exception table (§5.4): the named conditions raise `ValueError` naming the condition; no other exception type is
    required;
  - integer output: every money key is an `int`.
  - Failure messages name the violated property and hint at the concept. They never print the answer.
- **Dual mode**: the same suite runs in Pyodide and under pytest; each test under 5 s in Pyodide; the suite under 60 s.
- **Five alternative correct implementations** (must all pass; the verifier writes them as test-only fixtures in its
  scratch checkout and archives the scripts under `ledgers/E1/scripts/`): (1) closed-form, (2) iterated Cournot best response to convergence with the closed form
  as the stop condition, (3) a linear-system solve, (4) `Fraction` throughout, (5) float arithmetic with the same
  half-up rounding rule applied to the exact value of each output. The rule is stated, so no test is tolerance-based.

**Mutants (verifier writes at least three complete modules to `ledgers/E1/mutants/*.py`, VERIFIER §2.6; each must be killed; `mutate_graders.py --unit E1 --seeds 0-9`):**
1. Cournot computed with the monopoly first-order condition (ignores the rival: uses `a - b*c` for the Cournot volume).
2. Bertrand fee set to `c + 1`.
3. Monopoly first-order condition with the wrong factor (`a - b*f = 0`, dropping the `b*c` term).
4. Deadweight loss computed on the fee instead of the volume.
5. Rounding by truncation instead of half up (breaks the cent-exact checks on seeds where the fraction is `.5`).
6. A hard-coded answer for seed 0.

---

## 7. Cards builder (Builder F, after A-E)

- `course/modules/E/E1/cards.json`, ids `E1-c001` upward, `lesson` in L01-L09.
- One card per definition, theorem statement, key formula, key empirical result and misconception (BUILDER_RULES §7).
- Grade T for every derived result. Set `"basis"` to the lab or problem that establishes a numerical result, for example
  `"basis": "Lab 5, Problem 2 (exact)"`.
- Cite a registry key only for an empirical claim. E1 makes few empirical claims: `cite` is `[]` on every card unless a
  lesson makes one and the key is `varian2014intermediate`.
- `check_pages.py` checks the unit prefix, the lesson existence, the grades and the registry keys.

---

## 8. Registry keys the module may cite

| Key | Status | Use in E1 |
|---|---|---|
| `varian2014intermediate` | verified, Open Library book, `used_by: ["E1"]` (`references/references.json`) | the only curriculum source. Cite for definitions and textbook conventions at book level. No locator unless read. Reading list entry in the project |
| `mascolell1995microeconomic` | verified, `used_by: ["E4"]` | not curriculum-listed for E1. Usable only with the architect's approval (§10 Q7). Planner recommends no use |
| `nash1950equilibrium` | verified, `used_by: ["E2"]` | **not for E1**. Its concept belongs to E2 (§10 Q2) |

Keys needed but **not in the registry** (REFERENCE_REQUESTS, §8.1). The planner typed no bibliographic record for them.

### 8.1 REFERENCE_REQUESTS

- {doi: null, authors: "Cournot (lead only; record not typed)", year: "1838 (lead only)", title: "duopoly model, the origin of the reaction-function treatment", venue: "not typed", needed_for: "L06 historical attribution, if the architect permits historical attribution", confidence: "in existence: high; citation string: unverified"}
- {doi: null, authors: "Bertrand (lead only; record not typed)", year: "1883 (lead only)", title: "review of Cournot's model", venue: "not typed", needed_for: "L06 historical attribution, if permitted", confidence: "as above"}
- {doi: null, authors: "Samuelson (lead only; record not typed)", year: "1954 (lead only)", title: "public expenditure and the pure public good", venue: "not typed", needed_for: "L09 public-good attribution, if permitted", confidence: "as above"}
- {doi: null, authors: "Pigou (lead only)", year: "not typed", title: "externality and tax (the Pigouvian wedge)", venue: "not typed", needed_for: "L09 attribution, if permitted", confidence: "as above"}

The architect resolves these through `tools/add_reference.py` by DOI or ISBN or an allow-listed issuer page, or the lessons
teach the concepts with derivations and no historical attribution (recommended, §10 Q7).

---

## 9. Real-data policy

- **No real data.** The curriculum names no dataset for E1 (`curriculum/02-economics-finance-core.yaml:40-41` gives one
  book; no data source appears in `:23-49`). No snapshot in `course/assets/data/market/MANIFEST.json` is about
  microeconomics; the market data there is FX and Treasury series (`tools/data_sources.yaml`, per the AC4 plan §7).
- Lab and grader inputs are generated parameters and exact formulas. The grader's generated cases carry the
  **SIMULATED** label (§6); the labs do not, because they are exact computations (§2.2).
- No `data-files` attribute on any lab; no MANIFEST entry; no `DATA_REQUESTS` entry.
- If a lesson wants a real price or fee series, the request goes to `DATA_REQUESTS` with the source, licence quote and
  transform, and the page carries an honest-pending note. Not proposed.

---

## 10. Open questions for the architect (numbered; each needs a decision before the builders start)

1. **Hours split.** 90 h lessons (9 × 10) and 30 h project (25%). Confirm, or give another split within the rules in §1.
2. **Cournot and Bertrand equilibrium without the name `nash-equilibrium`.** E2 owns `nash-equilibrium`
   (`curriculum/02-economics-finance-core.yaml:59`), and E2 is not in E1's closure. Recommendation: E1 defines a
   Cournot (or Bertrand) equilibrium in words, as a profile of quantities or fees at which each exchange's choice is
   a best response to the others, with no `data-concept` link and no mention of the term "Nash". Alternative: a
   forward link, which BUILDER_RULES §1.10 forbids without a DAG_DEFECT. Decision needed.
3. **Optimisation without Lagrange multipliers or convexity.** `lagrange-multiplier`, `kkt-conditions`, `convex-set` and
   `convex-function` are M7 (outside the closure; `curriculum.json` concept owners). Consumer choice (L01), monopoly
   (L05) and the second-order conditions (L05, L06) use M2 only: substitution of the budget line into the objective,
   the first-order condition, the chain rule for `u(x, y(x))`, and the sign of the second derivative for concavity. The
   implicit-function theorem (M2) gives the comparative statics (L04). Recommendation: this route, with no M7 concept
   and no name for the Lagrangian. Alternative: add M7 to E1's prerequisites, a curriculum change that also pulls M3
   into the closure (`curriculum/02-economics-finance-core.yaml`; M7 prereqs M2, M3 per the JSON row). Not proposed.
4. **Project model and frozen interface.** The curriculum says "exchange-fee market" (`yaml:45-47`) and names no demand
   or cost model, so the model in §5.2-§5.3 is a planner proposal (linear trade demand, constant marginal cost, two
   exchanges). The planner's closed forms (§5.3) are hand checks. Confirm the model, and freeze the
   `outcome(...)` signature and its six keys in this plan before building (precedent: AC4 Q7-Q8).
5. **Solution file name.** Proposed `market_structure.py` (no Atlas contract; unit-local). Confirm.
6. **Money.** Integer cents with one half-up rounding per output, stated on the page (§2.1 item 8). Confirm, or choose
   `Fraction` throughout with no cent rounding (then no money key is an `int`, which conflicts with the cents rule).
7. **Sources and historical attribution.** Only `varian2014intermediate` is curriculum-listed and in the registry. Confirm:
   (a) no other key is cited in E1; (b) `mascolell1995microeconomic` stays with E4; (c) whether the four REFERENCE_REQUESTS
   in §8.1 are admitted, or the lessons teach Cournot, Bertrand, public goods and externalities with derivations and no
   historical attribution (planner recommendation).
8. **Scope of "market structures" and "welfare".** The core text (`yaml:24`) says "market structures". The plan covers
   monopoly, Cournot and Bertrand only; monopolistic competition and perfect-competition entry are not in
   `introduces` and are not taught. "Welfare" means total surplus within E1; the first welfare theorem (E4) is not stated.
   Confirm, because "market structures" and "welfare" are scope words that need a computation (§2.1 item 4).
9. **Adversarial?** The memo is not an IC defence or a debate. No 15-angle question bank. Confirm.
10. **Plain terms outside the 13 concepts.** Terms such as `utility function`, `marginal cost`, `reaction function`,
    `Pareto improvement`, `Edgeworth box`, `market clearing`, `Lerner index` and `public good's free-rider problem` are
    not registered concepts (`curriculum/curriculum.json` `concepts`). They appear in prose, defined at first use in
    the lesson with no `data-concept`. Confirm that a plain `<dfn>` without `data-concept` is accepted by `check_dag.py`
    (it is: the tool skips `<dfn>` without `data-concept`, `tools/check_dag.py` line 47 reads `if not concept: continue`).
    Also confirm the term list is a GLOSSARY_REQUESTS item, or that no glossary entry is needed.
11. **Lesson count and the Pareto lesson.** L08 holds one concept (`pareto-efficiency`) and one lab. An alternative is to
    merge L08 into L07 (surplus, DWL and Pareto) and use the 10 h for a tenth lesson on the exchange economy. Planner
    keeps nine lessons; confirm.

---

## 11. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

```bash
.venv/bin/python tools/check_pages.py --unit E1            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit E1
.venv/bin/python tools/check_projects.py --unit E1
.venv/bin/python tools/run_labs.py --unit E1              # --page L04 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/E/E1/L01.html          # per page, after twins are written
.venv/bin/python tools/embed_labs.py course/modules/E/E1/L04.html --refresh lab-E1-L04-1   # after editing a twin
.venv/bin/python tools/run_graders.py --unit E1 --seeds 0-49
.venv/bin/python tools/mutate_graders.py --unit E1 --seeds 0-9             # verifier only
.venv/bin/ruff check tests/labs/E1 course/modules/E/E1/grader && .venv/bin/ruff format --check tests/labs/E1
.venv/bin/mypy                                            # strict, repository configuration
```

Flags checked by the planner: `check_pages.py`, `check_dag.py`, `check_projects.py` accept `--unit` (and `--all`);
`run_labs.py` accepts `--unit`, `--all`, `--page` (`tools/run_labs.py` lines 119-121); `run_graders.py` accepts
`--unit`, `--all`, `--seeds` (lines 129-131; default seeds 0-49); `mutate_graders.py` accepts `--unit`, `--all`,
`--seeds` (lines 30-32; default 0-9); `embed_labs.py` takes pages and `--refresh [LAB_ID ...]` (lines 130-131).
The planner did not execute these commands.

`page_smoke.py` is not run by builders (timing-sensitive; the verifier runs it on a quiet machine). Repo-wide gates
(`check_pages.py --all`, `check_dag.py --all`, `build_site.py --check`, `render_curriculum.py`) are the architect's, once,
before any merge. Do not run them per builder.

---

## 12. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** The E1 project has no `atlas:` key (`yaml:43-49`) and no atlas entry names E1
   (`meta.yaml:198` onward). `check_projects.py` skips the contract check (lines 144-146). No `atlas/E1.contract.md`
   is needed, and none is drafted here.
2. **No debate.** E1 has no `debate:` key (`yaml:18-49`), so `check_pages.py` line 412 does not require a debate brief.
3. **Foundations-tier grading `both`.** Tier F, but graded `both`, so the rubric and exemplars are required by
   `check_projects.py` (rubric rules at `rubric_problems`, lines 58-73, and the grading check at `grading_problems`, lines 41-49). The M1 precedent applies.
4. **One curriculum lab.** The curriculum names one lab (`yaml:42`); the builder rules want a numerical check per key
   formula (BUILDER_RULES §3.4). The plan adds one lab per lesson (§3), the M1 precedent (architect Q2).
5. **check_dag sees linked uses only.** An unlinked use of `nash-equilibrium`, `lagrange-multiplier` or `convex-function`
   passes `check_dag.py`. The verifier must read every lesson for these names (VERIFIER §2.9; §10 Q2-Q3).
6. **M2 is not built.** The prerequisite is a curriculum node only; `course/modules/M/` contains M1. The hub links the
   M2 concepts through `concepts.html` anchors, not through an M2 page.
7. **Concept-link names for unregistered terms.** Unregistered terms are plain prose or plain `<dfn>` (§10 Q10).
8. **Labs must be exact.** Labs are standard-library `Fraction` code; the Pyodide and CPython runs are identical, so the
   `-W error` run must be warning-free.

---

## 13. DAG problems (concepts that natural content would use outside the closure)

| Concept | Owner | Where the natural content uses it | Resolution in this plan |
|---|---|---|---|
| `nash-equilibrium` | E2 (`curriculum.json` owners) | Cournot and Bertrand equilibrium (L06) | Describe in words, no name, no link (§10 Q2) |
| `lagrange-multiplier`, `kkt-conditions` | M7 | consumer and producer constrained optimisation (L01, L02, L05) | Substitution and first-order conditions with M2 concepts (§10 Q3) |
| `convex-set`, `convex-function` | M7 | concavity and second-order conditions (L05, L06) | Sign of the second derivative (M2 `derivative`, `hessian` if needed) (§10 Q3) |
| `expected-utility`, `first-welfare-theorem` | E3, E4 | risk, welfare theorem (L07, L08) | Not used; the welfare theorem is not stated (§10 Q8) |
| `ols-estimator`, `wacc`, `return-on-invested-capital` | S2, CF2, AC2 | none in E1 content | Not used |

No DAG_DEFECT is raised as a build failure, because each row has a resolution. Each row needs the architect's confirmation (§10 Q2, Q3, Q8).

---

## 14. After the builders

1. Orchestrator integrates; runs the §11 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L03, L04-L05, L06-L07, L08-L09, project. The project
   verifier writes at least three mutants per round (VERIFIER §2.6) and the five alternative implementations (§6).
   Failing rows return to the builder that owns the file, with only the failing rows.
3. Ledger at `ledgers/E1.verification.json`; verifier scripts archived under `ledgers/E1/scripts/` (VERIFIER §3).
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed.

Architect decisions: pending (§10). This plan is the planner's proposal.

## Architect decisions (2026-10-28, binding)
Q1: 9 x 10 h and a 30 h project. Q2: Cournot and Bertrand equilibria are described without naming nash-equilibrium. Q3: M2-only optimisation (substitution and derivatives); no M7 prerequisite. Q4: the plan's linear trade-demand, constant-marginal-cost two-exchange model is accepted; the builder re-derives and the page proves the closed forms. Q5: `market_structure.py`, freeze outcome(structure, a, b, c). Q6: integer cents, one half-up rounding per output. Q7: cite only varian2014intermediate; no historical attribution; no mascolell1995microeconomic. Q8: scope: monopoly, Cournot, Bertrand; welfare = total surplus only. Remaining questions: follow the plan's recommendation.
