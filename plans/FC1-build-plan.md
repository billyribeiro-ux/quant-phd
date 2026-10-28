# FC1 build plan: Haiku builders in parallel (planner output, 2026-10-28)

Unit: **FC1 · The Financial System, Markets & Instruments** · tier U · 70 h · prerequisites P0.1, E1 · no Atlas milestone ·
no debate · grading `autograder` · output directory `course/modules/FC/FC1/` (part code `FC`) · lab twins `tests/labs/FC1/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits, no check tools executed (read-only inspection
of the sources below). Executors: Haiku builders, then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies
and never writes a ledger.

Status: a planner's proposal. Section 10 lists decisions the architect must make before builders start. One of them
(Q1, the project's scope against the prerequisite graph) is blocking for the project builder.

Evidence convention: every curriculum statement cites `file:line` read during planning. Anything not in the curriculum is
marked **NOT IN CURRICULUM**. Registry facts cite `references/references.json` by key. Closed forms in section 5 are planner
derivations to be re-derived by the builder and checked by the verifier.

---

## 0. Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part FC, code `FC`, title "Finance Core" | `curriculum/02-economics-finance-core.yaml:348-349` (`code: FC` at 348) |
| STUDIO-FC requires FC1 and FC2; studio is not part of this unit | `curriculum/02-economics-finance-core.yaml:350-353` (`requires` at 353) |
| FC1 id, title | `curriculum/02-economics-finance-core.yaml:363-364` |
| Tier `U`, hours `70` | `curriculum/02-economics-finance-core.yaml:365-366` |
| Prereqs `[P0.1, E1]` (no others) | `curriculum/02-economics-finance-core.yaml:367` |
| Core text: money and credit creation, intermediaries, exchanges vs. OTC, instrument taxonomy across equities, rates, credit, FX, commodities and derivatives, order types, clearing and settlement | `curriculum/02-economics-finance-core.yaml:368-371` |
| `introduces` has 10 concepts (listed in section 2) | `curriculum/02-economics-finance-core.yaml:372-382` |
| Sources: Mishkin (13th ed., 2022); Harris, *Trading and Exchanges* (2003); McLeay, Radia & Thomas (2014), BoE QB Q1 (free text, not keys) | `curriculum/02-economics-finance-core.yaml:383-386` |
| Lab: "Trace one trade from order entry to settlement." | `curriculum/02-economics-finance-core.yaml:387` |
| Project "Instrument cash-flow engine"; brief: represent bonds, futures, swaps and options as dated cash-flow or payoff objects with a common interface, and test each against hand-computed examples; deliverable "Tested module."; grading `autograder` | `curriculum/02-economics-finance-core.yaml:388-395` (grading at 395) |
| No `debate` key on FC1 | `curriculum/02-economics-finance-core.yaml:363-395` (absent) |
| No `atlas` key on FC1; FC1 is named by no Atlas milestone (the atlas block starts at `meta.yaml:198`; no `FC1` in `curriculum.json` `atlas`) | `curriculum/02-economics-finance-core.yaml:388-395`; `curriculum/meta.yaml:198` |
| JSON row mirrors the YAML (hours 70, prereqs P0.1 and E1, 10 concepts, sources, lab, project, grading autograder) | `curriculum/curriculum.json:7727` (`"id": "FC1"`) |
| All 10 concepts map to module FC1 in `concepts` | `curriculum/curriculum.json` `concepts` (e.g. `bank-money-creation` at 1417, `bond-price-yield` at 1553 belongs to FI1, see section 7) |
| BS-FIN credential requires FC1; course map "Financial Markets & Institutions" lists FC1 | `curriculum/meta.yaml:62` and `:79` |
| FC2 prereqs `[M4, CF1]`; FC2 introduces `futures-contract`, `interest-rate-swap`, `option-payoff` | `curriculum/02-economics-finance-core.yaml:396-400` and `:409`, `:411`, `:412`; `curriculum.json:7763` |
| FI1 prereqs `[M2, CF1]` | `curriculum/03-markets.yaml` (FI1 block; `curriculum.json` row, planner read) |
| Topological positions: FC1 index 26, FC2 index 27, FI1 index 18 | `curriculum/curriculum.json` `topological_order` (planner read) |

### 0.1 Prerequisite closure (computed)

Planner walk of `curriculum.json` prereqs (same algorithm as `tools/coursekit.py` `prerequisite_closure`, lines 239-249):
closure of FC1 = **{E1, M1, M2, P0.1}**. Concepts usable without definition:

- E1 (13): `utility-maximization`, `profit-maximization`, `competitive-equilibrium`, `price-elasticity`,
  `comparative-statics`, `monopoly`, `cournot-competition`, `bertrand-competition`, `economic-surplus`,
  `deadweight-loss`, `pareto-efficiency`, `externality`, `public-good` (`curriculum/02-economics-finance-core.yaml:26-39`;
  E1 entry starts at line 18, prereqs at 22).
- M2 (13): `limit`, `derivative`, `taylor-theorem`, `definite-integral`, `partial-derivative`, `gradient`, `jacobian`,
  `hessian`, `multiple-integral`, `implicit-function-theorem`, `envelope-theorem`, `finite-difference-derivative`,
  `automatic-differentiation` (`curriculum/01-foundations.yaml:133` onward for `derivative`).
- M1 (14): includes `present-value` (`curriculum/01-foundations.yaml:100`), `discount-factor`, `annuity`, `perpetuity`,
  `growing-perpetuity`, `amortization-schedule`, `exponential-and-logarithm`, `compounding-frequency`,
  `continuous-compounding`, `geometric-series` (`:102`), `quantifiers`, `direct-proof`, `proof-by-contradiction`,
  `mathematical-induction`.
- P0.1 (11): `evidence-grade`, `paper-anatomy`, `identification`, `robustness-check`, `replication`, `steelmanning`,
  `project-ladder`, `prerequisite-dag`, `atlas-platform`, `citation-registry`, `notation-conventions`.

Consequence: the closure is large (51 concepts) and includes M2, which is a real advantage over CF1 (see section 7). The
concepts that the curriculum's own FC1 content and project need, and that lie outside the closure, are listed in section 7.

---

## 1. Feasibility of the hours (no conflict; no STOP)

The curriculum figure is 70 h (`curriculum/02-economics-finance-core.yaml:366`). Tool rules:

- each lesson `data-hours` 6-12 (`tools/check_pages.py` line 227);
- hub `data-hours-lessons + data-hours-project = 70` (`check_pages.py` lines 337-338);
- project share 10-40 % of 70, i.e. 7 to 28 h (`check_pages.py` lines 339-340);
- lessons sum to the hub's lessons figure (`check_pages.py` lines 341-342).

Chosen split: **5 lessons × 10 h = 50 h; project 20 h (28.6 %)**. Feasible. The hours rule does not trigger a STOP.

---

## 2. Binding rules for every builder

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `VERIFIER_RULES.md` §2 (what will be checked), this
file. Study `course/modules/M/M1/` (hub, project, grader panel), `course/modules/AC/AC4/` (both-free autograder unit, SIMULATED
cases) and `course/modules/AC/AC2/` (lab-id and hours conventions) for layout only. `course/templates/` holds the skeletons.
Imitate structure, not wording. `course/modules/FC/` does not exist yet (verified by listing).

### 2.1 Lessons learned from the verification campaigns (binding)

These come from `plans/E1-build-plan.md` §2.1 (each item was a real defect in an earlier campaign) and from the task's
own list. Each is binding for every FC1 builder and verifier.

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) and rounded
   only at display. A page that shows a rounded figure says which rounding it uses (half up, to the cent). Precedents:
   AC4 KNOWN LIMITATION 3, CF1 L01 Remark 5.2 (E1 plan §2.1 item 1).
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only
   what the printed numbers show. Precedent: M1 LESSON_TEXT_DEFECTS (a "checked directly" phrase with no lab behind it).
3. **Attribute nothing unread.** Only keys in section 6 may be cited. No locator, page, table or coefficient is typed unless
   the builder has read it in a source that reproduces it. A textbook result without a confirmed locator is either a
   derivation on the page (grade T) or cited at book level with no locator. No bibliographic data from memory.
4. **Scope words need a computation or an explicit hypothesis.** "every", "all", "never", "always", "any", "across" (the
   core text's "across equities, rates, credit, FX, commodities and derivatives", `yaml:370`), "market structure", "clearing
   and settlement" are used only where a proof, a finite check, a lab or an explicit enumeration makes the claim. An
   enumeration is grade C with its basis named, not grade T.
5. **Define before use.** Each of the 10 concepts in section 2.2 is defined with `<dfn id="def-<id>" data-concept="<id>">`
   in its assigned lesson and never before it. A lesson uses a concept only after the lesson that defines it. Terms
   outside the 10 concepts may appear in prose and, if emphasised, as a plain `<dfn>` without `data-concept` (`check_dag.py`
   skips it; `tools/check_dag.py`, the `<dfn>` loop in `check_unit`, which skips a `<dfn>` with no `data-concept`).
6. **Proposition hypotheses explicit.** Every Theorem and Proposition lists its assumptions before its statement, as numbered
   **Assumptions** (A1, A2, ...). Each assumed fact is named and numbered. Example: the deposit-multiplier result assumes a
   constant reserve ratio in (0, 1] and that every loan is redeposited in full.
7. **Grader tests demand an exception type only for conditions the page names** (section 5.4). Any other invalid input may
   raise any exception or return. **Five alternative correct implementations must pass** the suite (section 5.6).
8. **Integer cents for money.** Every money output of the engine is an `int` in cents, computed from exact `Fraction`s and
   rounded once, half up, by the rule stated on the project page. No float money, no tolerance on money. Labs use the same
   rule. Precedent: E1 §2.1 item 8, AC4 Q9/Q10.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own
   container; no element forces the page wider than 360 px. Enforced by `page_smoke.py` (lines 341-343, horizontal scroll
   check at the 360 px viewport from `VIEWPORTS`, line 67). Builders do not run `page_smoke.py`; verifiers do.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no
    `if __name__ == "__main__":` guard. `run_labs.py` runs each twin as `python -I -W error <twin>` (`tools/run_labs.py`
    line 55). Precedent: `tests/labs/M1/lab-M1-L04-1.py` line 73 is `main()`; its `def main()` is at line 40.
11. **Mutants: ten, not three.** The verifier's binding minimum is three (`tools/mutate_graders.py` lines 41-43 fail below
    three). The task that commissioned this plan requires **ten** student-error mutants, so FC1 uses ten (section 5.5).

### 2.2 Concepts (exactly the 10 in `introduces`, each defined once)

Each concept is defined in exactly one lesson (section 3). `<dfn>` only for these 10. No other concept gets `data-concept`.

### 2.3 Standing rules

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key from section 6, or a derivation on the
  page. Claims about what firms or markets do are graded C at most unless a registry source with a confirmed locator says it.
- Concepts: prerequisite links `href="../../../concepts.html#<id>"` for E1, M2, M1 and P0.1 concepts; `href="Lnn.html#def-<id>"`
  for earlier FC1 lessons. A lesson never links a concept defined in a later lesson (`check_dag.py`, BUILDER §4.1).
  A term outside the closure is plain prose, with no `<a class="concept">` (section 7).
- Labs: code lives once in `tests/labs/FC1/lab-FC1-Lnn-1.py` (and `lab-FC1-project-1..3.py`). The page carries
  `@@LAB:<file>@@` and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output by hand. Lab ids must
  match `lab-FC1-<page>-<n>` (`check_pages.py` line 258). Standard library only (`fractions`, `itertools`, `math`, `random`
  with a fixed seed if any); no network; under 10 s in Pyodide; no warnings (`-W error`, `run_labs.py` line 55).
- SIMULATED label: only for generated data (BUILDER §1.7). Exact computations and closed-form checks are not labelled SIMULATED.
  Generated filers, portfolios, order flows and trade records are labelled **SIMULATED** on the figure, the hypothesis and the
  project page.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references in
  code comments (E1 §2.2 standing rule).
- Banned strings (`tools/check_pages.py` lines 58-72): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the scope",
  "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
  "obviously", "clearly", and any ellipsis `...` outside code.
- Percent changes state the base and the direction. Hub lesson titles match each lesson's `<h1>` at integration.
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `notation/notation.json`). Request changes; do not write them.
- Notation: use only macros in `notation/notation.json` (section 4.1). See section 4.2 for symbols FC1 must not reuse.
- Money: integer cents (section 2.1 item 8). Basis-point rates are integers (`coupon_bps`, `yield_bps`); the conversion
  rule is stated on the page.

---

## 3. Outline and file ownership (the planner's split; the architect confirms, Q7)

Lessons: 5 × 10 h = 50 h. Concepts: 10, each in exactly one row. Hub `data-hours-lessons="50"`; project 20 h.

| Lesson | Title (working) | Concepts it defines (`introduces`, yaml 373-382) | Lab (twin id, `tests/labs/FC1/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Money, banks and financial intermediaries | `bank-money-creation`, `financial-intermediary` | `lab-FC1-L01-1`: a stylised bank balance-sheet recursion with a constant reserve ratio; the total deposit expansion against the geometric-series closed form, exact in `Fraction` (M1 `geometric-series` is linked) | 10 | Builder A |
| L02 | Markets, exchanges, OTC and the instrument taxonomy | `exchange-vs-otc`, `asset-class-taxonomy` | `lab-FC1-L02-1`: a fixed register of instruments coded to one asset class and one venue type; a check that every entry has exactly one of each and that the counts reconcile (a consistency check, flagged as such, Q11) | 10 | Builder A |
| L03 | Dealers, market makers and the bid–ask spread | `market-maker`, `bid-ask-spread` | `lab-FC1-L03-1`: a seeded quote sequence for a dealer; round-trip spread income equals spread × volume when inventory returns to zero, checked in integer cents | 10 | Builder B |
| L04 | Order types and the limit order book | `order-types`, `limit-order-book` | `lab-FC1-L04-1`: a seeded price-time-priority matching of market, limit and stop orders on one book; share conservation and the best bid/ask after each event | 10 | Builder B |
| L05 | Clearing, settlement and the trade lifecycle | `clearing-and-settlement`, `trade-lifecycle` | `lab-FC1-L05-1` (**the curriculum lab**, yaml 387): trace one seeded trade from order entry through matching, clearing and settlement, with each state and its business-day offset printed | 10 | Builder C |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 50 / 20 | none | none | - | Builder A |
| project | Instrument cash-flow engine (autograder, section 5) | none | `lab-FC1-project-1` (rung 1), `lab-FC1-project-2` (rung 2, `class="lab completion"`), `lab-FC1-project-3` (rung 3 check) | 20 | Builder D |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` | none | none | - | Builder D |
| cards | `cards.json` from L01-L05 | none | none | - | Builder E (after A-D) |

Ownership rule: each builder writes only its own lesson files and twins. Builder A writes the hub after L01-L02 exist, so the
lesson map is right; the cross-check runs at integration. Builder D's grader is independent of the lessons and of the engine
interface is frozen in section 5.2 before any builder starts.

Coverage check: 2+2+2+2+2 = 10 concepts, each in exactly one row, matching the 10 entries at `curriculum/02-economics-finance-core.yaml:373-382`.

Ordering check (no lesson links a later definition):
- L01 uses M1 `geometric-series` and `present-value`; no FC1 concept.
- L02 uses L01's `financial-intermediary` only in prose (a link is allowed to an earlier lesson).
- L03 uses L02's `exchange-vs-otc` (dealers quote on exchanges and OTC) and E1 `bertrand-competition` in prose; the spread is
  defined here.
- L04 uses L03's `bid-ask-spread` (the best bid and ask); `order-types` is defined here before `limit-order-book`.
- L05 uses L04's `order-types` and `limit-order-book` for the matching step and `clearing-and-settlement` (its own
  definition, first in the lesson). The `trade-lifecycle` definition closes the lesson.

Not in this table: the curriculum does not assign a debate; no lesson carries a debate brief.

---

## 4. Hub (`index.html`, Builder A)

- `<html lang="en" data-root="../../../" data-unit="FC1" data-page="index">`;
  `<main data-hours-lessons="50" data-hours-project="20">` (sums to 70; project 28.6 %, inside 10-40 %).
- 4-8 measurable objectives (`ol.objectives`). Target six, with measurable verbs. Example: "Compute the total deposit expansion
  implied by a reserve ratio." "Classify an instrument by asset class and venue." "Trace one trade from order entry to
  settlement."
- Prerequisites: P0.1 and E1, linked to their concept anchors in `../../../concepts.html#<id>` for the concepts the hub uses.
  Do not link an unbuilt E1 or M2 page: check whether `course/modules/E/` exists before linking. (At planning it does not;
  link concept anchors only.)
- Placement: `section.quiz#placement` with `data-unit="FC1" data-page="placement" data-mastery="0.8"` (the AC4/M1/E1 bar),
  nine items. At least two items carry `data-skill` and test what rungs 1-2 teach: the worked example's cash-flow line for a
  coupon bond, and the completion problem's variation-margin line for a futures position. The rest test P0.1 and E1 and M1
  prerequisites: present value of a single cash flow, the equilibrium price of a market, the geometric-series sum.
- Lesson map: one `card` link per L01-L05 with `data-progress-key="FC1/Lnn"` and a `data-hours` text. `href="L01.html"` etc.
  must each appear (`check_pages.py` lines 359-361 require the lesson map links).
- Ladder: `ol.ladder` with four `li` and `span.rung-title` in order: Worked example, Completion problem, Independent project,
  Stretch (`check_projects.py` line 33, `RUNGS`; `check_pages.py` ladder rule).
- Core reading: `ol.reading-list` with `li data-cite` keys from section 6 only.
- Tier U keeps rungs 1-2 at full length (BLUEPRINT §4: the minimum applies from tier M upward). Placement skips rungs 1-2
  for students who pass (BUILDER §5.1).

---

## 5. Project (`project.html`, Builder D): ladder, spec, grader

### 5.1 Ladder (BLUEPRINT §5.1; `check_projects.py` line 33 requires the order)

1. **Rung 1, worked example** (`lab-FC1-project-1`): one fully solved, annotated SIMULATED instrument set: a 3-period coupon
   bond, a short futures position over a 3-day settlement path, a 2-period swap and a call at expiry. Each step has a "why"
   annotation. Cents, rounded per section 5.3.
2. **Rung 2, completion** (`lab-FC1-project-2`, `class="lab completion"`): the variation-margin line of the futures object and
   the coupon-timing line of the bond are removed (`___`). Graded instantly. Its twin is the completed solution; every page
   line equals the twin line or contains a blank (`run_labs.py` completion rule, as in E1 §5.1).
3. **Rung 3, independent project** (graded, autograder only): the engine `instruments.py` to the section 5.2 interface. A short
   written "conventions" block in the module docstring (sign convention, period indexing, rounding rule) is part of the
   submission, not a rubric.
4. **Rung 4, stretch** (optional, not graded): a callable bond or a cash-flow reconciliation of two instruments on one ledger,
   with a stated hypothesis. No ceiling. Not graded.

### 5.2 Spec (`dl.spec`; `check_projects.py` lines 34 and 38-49 require the terms and the grading word)

Terms: Context (2-4 sentences), Inputs, Required outputs, Constraints, Grading.

- **Context.** A back office receives dated cash-flow and payoff records for four instrument types and must book them through
  one interface before reconciliation. The engine turns each instrument into a list of dated amounts in integer cents.
- **Inputs.** Generated SIMULATED parameters from `grader/instance.py` (no real data, section 9).
- **Common interface (planner proposal, frozen by Q9 before building).** `instruments.py` exposes:
  - events convention: every instrument's `events()` returns `list[tuple[int, int]]`, that is `(period, amount_cents)`, sorted by
    period, with `period` an integer in `1..periods` and the amount signed from the holder's side (positive = inflow). A zero
    amount is allowed and kept.
  - `Bond(face_cents: int, coupon_bps: int, periods: int)` with `events() -> list[tuple[int, int]]`: a coupon of
    `face_cents * coupon_bps / 10000`, rounded half up, at each period, and the face at the last period.
  - `bond_price_cents(bond: Bond, yield_bps: int) -> int`: present value at a per-period yield, discounting each event by
    `(1 + yield_bps/10000) ** -period` (the M1 discount factor), summed exactly in `Fraction`, rounded once half up.
  - `Future(settlement_prices_cents: list[int], multiplier_cents: int, side: int)` with `events()` giving the daily variation
    margin `side * multiplier_cents * (p_t - p_{t-1})` for `t = 1..n-1` (the list has `n` prices; `n >= 2`).
  - `Swap(notional_cents: int, fixed_bps: int, floating_bps: list[int], side: int)` with `events()`: the net period amount
    `side * notional_cents * (floating_bps[t-1] - fixed_bps) / 10000`, rounded half up. `side = +1` receives floating.
  - `Option(kind: str, strike_cents: int, underlying_at_expiry_cents: int, side: int, expiry_period: int)` with `events()`
    giving one amount at `expiry_period`: `side * max(S - K, 0)` for a call and `side * max(K - S, 0)` for a put. No premium and
    no option pricing model (Black-Scholes is FC2's, not in the closure).
- **Required outputs.** `instruments.py` with the classes and function above, plus a short `README` section in the module docstring.
  No other files are required by the grader.
- **Constraints.**
  - Integer cents: every money output is an `int`, computed from exact `Fraction`s and rounded once, half up, to the nearest cent.
  - Valid input (exception table, section 5.4 only).
  - Standard library only; no network; the same code runs in Pyodide and under pytest.
- **Grading.** Autograder (`grader/test_project.py`, dual-mode). The spec must name the autograder (`check_projects.py`
  `GRADING_WORDS`, lines 36-38: `autograder` requires the word "autograd"; the rubric is not required).
- **Reading list.** `ol.reading-list` cites `mishkin2021economics` and `harris2002trading` only if Q3 is decided (section 6).
  Otherwise the reading list is empty, and the spec says so.

### 5.3 Rounding and conventions (stated once; used in every output)

- Period indexing: periods are integers `1..n`; `period 0` is the settlement date (no event). Stated on the page.
- Half-up rounding: `round_half_up(x) = floor(x + 1/2)` on the exact `Fraction`, with the sign rule for negatives stated as
  "round half away from zero" (planner choice, Q9 confirms). One rounding per output, never per intermediate term.
- Signs: all amounts are from the holder's side; `side = +1` long or receiving, `side = -1` short or paying.

### 5.4 Exception table (grader tests demand these, and only these)

| Condition the page names | Exception | Message must name |
|---|---|---|
| `periods < 1` or `face_cents <= 0` for a bond | `ValueError` | the rule violated, for example "periods must be at least 1" |
| `side` not in `{+1, -1}` | `ValueError` | the allowed values |
| `kind` not in `{"call", "put"}` | `ValueError` | the allowed names |
| `Future` with fewer than 2 prices | `ValueError` | "a futures path needs at least two prices" |

Any other invalid input may raise any exception or return; the tests do not require a type for it.

### 5.5 Grader design (Builder D)

Files (`course/modules/FC/FC1/grader/`): `instance.py`, `reference.py` (the full solution; excluded from deployment,
BLUEPRINT §7), `starter.py` (stubs raising `NotImplementedError`), `test_project.py`. The student file is `instruments.py`.
Grader panel on `project.html`: `<section class="grader-panel" id="grader" data-unit="FC1" data-grader="grader/"
data-suite="test_project.py" data-support="instance.py" data-solution="instruments.py" data-starter="starter.py">`
(`check_projects.py` lines 123-136 require these attributes and the files). `data-packages` is empty: standard library only
(tooling assumption T2, section 8).

- `instance.py`: `make_instance(seed: int) -> dict` (the exact signature `check_projects.py` line 136 tests). Deterministic per seed
  from `random.Random(seed)`. Generates: a bond (face, coupon, periods, a yield), a futures path (two to five prices),
  a swap (notional, fixed rate, floating resets), an option (strike, expiry price, expiry period, side). Every seed valid.
  Labelled **SIMULATED** in the docstring: generated inputs, not market data. Seeds 0-49 give materially different answers (the
  bond price, the margin total and the option payoff change, not only the labels). Verifier checks 20 sampled seeds.
- `reference.py`: the full solution with `Fraction` and one half-up rounding per output. Passes every test on seeds 0-49.
- `starter.py`: stubs that raise `NotImplementedError`. The suite must fail on it, naming the property, not a stack trace.
- `test_project.py` (properties and numbers; each test recomputes its expected value from the instance's own parameters with an
  oracle written separately from `reference.py`; no hard-coded answers):
  - bond: coupon count and amounts equal the generating parameters; principal at the last period; events sorted and
    within `1..periods`;
  - bond price equals the closed form `sum(c * v**t) + F * v**n` with `v = 1 + y`, computed in `Fraction` and rounded
    once, to the cent;
  - futures: total variation margin equals `side * multiplier * (p_n - p_1)` exactly (telescoping identity), on every seed;
  - swap: the net events sum to the notional times the sum of floating-minus-fixed, rounded per period, and the sign flips
    with `side`;
  - option: payoff is non-negative for the holder, zero out of the money, and equals `side * (S - K)` in the money;
  - integer output: every money value is an `int`;
  - hand-computed fixtures: one fixed fixture per instrument, hand-computed on the page (not seed-derived), e.g. a 100.00 face
    bond with a 5 % coupon, one period; these are permitted alongside the seed tests (Q10);
  - exception table (section 5.4): only the named conditions raise `ValueError` naming the condition.
  - Failure messages name the violated property and hint at the concept. They never print the answer.
- Dual mode: the same suite runs in Pyodide and under pytest; each test under 5 s in Pyodide; the suite under 60 s.
- **Five alternative correct implementations** (must all pass; the verifier writes them as test-only fixtures in a scratch
  checkout and archives the scripts under `ledgers/FC1/scripts/`): (1) a list-comprehension implementation of each `events()`;
  (2) a class-based implementation with methods returning generators; (3) a `Fraction`-throughout implementation with one final
  half-up rounding; (4) an integer-only implementation using integer division for the half-up rule; (5) a float implementation
  that applies the same half-up rule to the exact value of each output. No test is tolerance-based on money.
- **Mutants (ten).** The verifier writes ten complete solution modules to `ledgers/FC1/mutants/*.py`, each opening with a
  one-line docstring that names the error. `tools/mutate_graders.py --unit FC1 --seeds 0-9`. Each must fail at least one test:
  1. bond price discounts each coupon with the annual yield per period (yield not divided by periods per year);
  2. bond price uses the nominal yield as the effective per-period rate in the wrong compounding convention;
  3. principal omitted at maturity;
  4. last coupon omitted (off-by-one period);
  5. futures margin sign not flipped for the short side;
  6. futures margin computed on price levels, not changes, with the first price included;
  7. swap with the payer and receiver legs reversed;
  8. put payoff computed as `max(S - K, 0)` (call formula);
  9. rounding by truncation toward zero instead of half up (breaks the cent checks where the fraction ends in `.5`);
  10. a hard-coded answer for seed 0 (the bond price written as a constant).

### 5.6 Time budget (`<table id="hours">`, sums to 20 h; every row needs a one-line rationale)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 1 | One solved SIMULATED instrument set, annotated line by line |
| Rung 2, completion problem | 2 | Fill the variation-margin and coupon-timing lines, then run the instant check |
| Bond object and `bond_price_cents` | 4 | Coupon schedule, principal, discounting, half-up rounding |
| Futures object | 3 | Telescoping margin, side sign, path validation |
| Swap object | 3 | Net legs, per-period rounding, side convention |
| Option object | 3 | Payoff at expiry for call and put, side convention |
| Edge cases and the suite on seeds 0-9 | 2 | Exception table, instance validity, local pytest run |
| Self-check against the conventions block | 2 | Re-read the conventions (section 5.3) against the code |
| **Total** | **20** | Equals `data-hours-project` on the hub |

---

## 6. Registry keys the module may cite

Only keys in `references/references.json` may be cited (`check_pages.py` checks registry keys; BUILDER §2.1). Verified in the
registry during planning (read, `references/references.json`, dict `entries`):

| Key | Registry record (as read) | Use in FC1 | Status |
|---|---|---|---|
| `mishkin2021economics` | Mishkin, *Economics of Money, Banking, and Financial Markets*, Pearson, ISBN 9780136894285, Open Library, **year 2021**; `notes.year`: curriculum "2022", record "2021"; `used_by: ["FC1"]` | the curriculum's textbook (yaml 384) for money creation and intermediaries (L01), with locators only after a builder reads them | **Year conflict** with the curriculum string. Decision Q3 |
| `harris2002trading` | Harris, *Trading and Exchanges: Market Microstructure for Practitioners*, Oxford University Press, DOI 10.1093/oso/9780195144703.001.0001, Crossref, **year 2002**; `notes.year`: curriculum "2003", crossref "2002"; `used_by: ["FC1"]` | the curriculum's market-structure book (yaml 385) for L02-L05 | **Year conflict**. Decision Q3 |
| `ifrsndifrs` | IFRS Standards (AC1) | not used on FC1 pages | not used |

Keys needed but **not in the registry** (`REFERENCE_REQUESTS`; the planner typed no bibliographic record for them):

- **McLeay, Radia & Thomas (2014), Bank of England Quarterly Bulletin Q1** (curriculum yaml 386). Not in `references.json`.
  `references/SEED_REPORT.md` line 35 records "no candidate established identity" and names the route: verify against
  OpenAlex or the publisher's stable URL, then add a manual entry. `bankofengland.co.uk` is an allow-listed issuer domain
  (`references/authorities.yaml`, line 23). Needed for: the bank-money-creation claim in L01 (grade A or B only if admitted).
  Until admitted, the claim is grade C with no citation, or left out. Confidence in the citation string: as given, unverified.
- **A settlement-cycle source** for L05 (any factual statement about settlement periods, for example "T+1"). Topic only:
  the registry holds no settlement-cycle source. `sec.gov` is allow-listed (`authorities.yaml` line 13). Needed for: L05
  settlement facts. Until admitted, the lesson states the settlement period as a parameter of the lab, not as a fact.
- **A market-quality or spread-evidence source** for L03 and L04, if a builder wants a graded empirical claim. Topic only. None
  is proposed: naming one from memory would be a fabrication. Until admitted, such claims are grade D ("It is widely claimed...")
  or left out.

Keys belonging to other modules that FC1 must **not** cite: `bouchaud2018trades`, `obizhaeva2013optimal`, `toth2011anomalous`
(MS3 scope), `andersen2014vpin` (MS1 scope), `harris2014private` (PM1 scope), `cftc1999hedge` (GM5 scope).

---

## 7. DAG risk and the project scope (must be reported; not patched by the builder)

### 7.1 Concepts the curriculum's FC1 content needs that lie outside the closure

The closure is {E1, M1, M2, P0.1} (section 0.1). The following concepts belong to modules that are **not** in the closure. FC1
may not link them (`check_dag.py` rejects a link outside the closure). Builders describe the idea in plain words, with no
`data-concept`, and the verifier reads for the names (VERIFIER §2.9, because `check_dag.py` checks linked uses only).

| Concept | Owner (module, file) | Where FC1 needs it | Resolution in this plan |
|---|---|---|---|
| `futures-contract`, `futures-margining` | FC2 (`yaml:409-410`) | project `Future` object; L05 trade lifecycle | plain prose, DAG_DEFECT (Q1) |
| `interest-rate-swap` | FC2 (`yaml:411`) | project `Swap` object | plain prose, DAG_DEFECT (Q1) |
| `option-payoff` | FC2 (`yaml:412`) | project `Option` object | plain prose, DAG_DEFECT (Q1) |
| `bond-price-yield`, `yield-to-maturity` | FI1 (`03-markets.yaml:28-29`) | project `Bond` and `bond_price_cents` | plain prose, DAG_DEFECT (Q2) |
| `central-counterparty`, `settlement-cycle` | BK4 (`yaml:1081`, `:1085`) | L05 clearing and settlement | plain prose, DAG_DEFECT (Q4) |
| `order-book-data-structure` | CS2 (`01-foundations.yaml:435`) | L04 limit order book (price levels) | plain prose, DAG_DEFECT |
| `spread-decomposition`, `roll-spread-estimator` | MS1 (`04-quant.yaml:444`) | L03 spread (beyond the definition) | not used; plain prose only if needed |
| `deposit-franchise`, `bank-reserves` | BK1, FI4 | L01 (reserve ratio language) | plain prose; the reserve ratio is a lab parameter |
| `duration`, `day-count-convention`, `clean-and-dirty-price` | FI1 | project bond object (dating, accrued interest) | not used: the bond uses integer periods and no accrued interest |
| `arbitrage-opportunity`, `cost-of-carry-forward-price` | FC2 | project futures and swap, if no-arbitrage language is used | not used |
| `fx-market-structure`, `fx-forward-points` | X1 | L02 FX row of the taxonomy | plain prose, no FX claims beyond the taxonomy |
| `credit-default-swap`, `repo-haircut`, `swap-spread` | CR2, FI4 | L02 taxonomy (credit and rates rows) | plain prose, names only |

### 7.2 In-closure concepts FC1 can use with links

- E1: `bertrand-competition` (L03 dealer competition), `competitive-equilibrium` (L03), `economic-surplus` (not needed unless
  used), `price-elasticity` (not needed).
- M1: `present-value`, `discount-factor`, `geometric-series`, `compounding-frequency`, `annuity` (project bond sum).
- M2: `derivative` (for the sensitivity of a bond price in the stretch rung, optional).

### 7.3 The blocking structural conflict (Q1)

The project brief (yaml 388-395) asks for bonds, futures, swaps and options as dated cash-flow or payoff objects. Three of the four
object types (futures, swaps, options) are introduced by FC2 (`yaml:409-412`), and bond pricing needs FI1 concepts (`03-markets.yaml:28-29`).
FC2 is topologically after FC1 (index 27 vs 26). FI1 is topologically before FC1 (index 18), but FC1's closure does not include it.
The hours are feasible (section 1); the scope and the graph are not. The project builder cannot link these concepts, and the
curriculum sequence has FC1 teaching objects that its own later module defines.

Options the architect must choose from (the planner does not choose silently):
(a) keep the brief, define the mechanics in plain prose with no links, and record DAG_DEFECT rows (the default in this plan);
(b) add FC2 (or FI1) to FC1's prerequisites (a curriculum change: FC2 is 90 h and needs M4, CF1; FI1 is 90 h and needs M2, CF1;
    neither depends on FC1, so no cycle, but the closure grows);
(c) move the futures, swap and option objects to FC2 and keep only the bond in FC1 (a curriculum change).

---

## 8. Real-data policy and tooling assumptions

### 8.1 Real data

- The curriculum names no dataset for FC1 (yaml 363-395 has no data field).
- Default: **no embedded data**. Labs and grader use generated, labelled SIMULATED inputs; no `data-files` attribute; no
  MANIFEST entry; no `DATA_REQUESTS` line.
- Option (Q8): two cleared snapshots exist in `course/assets/data/market/MANIFEST.json`: `ust_daily` (H.15 3-month bill and
  10-year constant-maturity yield, retrieved 2026-10-20, licence quote and `licence_url` `https://www.federalreserve.gov/disclaimer.htm`)
  and `fx_daily` (H.10, retrieved 2026-10-19). Either could illustrate L02 (a rates or FX row). If used: list the file in `data-files`,
  open it as `data/<file>`, cite the MANIFEST citation and retrieval date in the hypothesis and the figure source line, and the
  verifier opens `licence_url` and checks the quote (VERIFIER §2.8). The `ust_daily` note (`tools/data_sources.yaml` lines 100-103)
  says the constant-maturity series names a U.S. Treasury source; a builder must read that note before use.
- Bring-your-own-data mode is not needed for FC1.

### 8.2 Tooling assumptions that do not hold, or are not verified

1. **Pyodide package list.** `run_graders.py` imports numpy at module level (`tools/run_graders.py` line 35). The FC1 grader and labs
   are standard-library only, so `data-packages=""` is intended. Not verified that the Pyodide runner accepts an empty list.
2. **Solution path.** The `run_graders.py` docstring (lines 15-16) gives `atlas/<module>.py` for Atlas milestones. FC1 has no Atlas
   milestone, so the solution is unit-local (`data-solution="instruments.py"`, AP1/AC4 pattern). Not verified in the code path
   (`workspace()`, lines 51-61) beyond that reading.
3. **No 360 px check in `check_pages.py`.** The no-horizontal-scroll rule is enforced by `page_smoke.py` only (lines 341-343). Builders
   do not run `page_smoke.py`; the verifier does, on a quiet machine.
4. **Lesson section list.** `check_pages.py` line 75 requires the sections `why-it-matters`, `canon-breaks`, `misconceptions`,
   `problems`, `key-results`, `quiz` and `references`. A lesson needs a `references` section even when it cites one key.
5. **Debate.** No `debate` key (yaml 363-395), so `check_pages.py` line 412 does not require a debate brief.
6. **Atlas.** No `atlas` key (yaml 388-395) and no milestone names FC1, so `check_projects.py` lines 144-146 skip the contract check.
   No `atlas/FC1.contract.md` is needed, and none is drafted.
7. **Grading words.** `autograder` requires the word "autograd" in the spec's grading entry (`check_projects.py` lines 36-38, 41-49).
   No rubric is required, so no exemplars and no self-assessment form.

---

## 9. Real-data, notation and cards

### 9.1 Notation (`notation/notation.json`, binding; BUILDER §3.1-3.2)

Registered symbols and macros (read, `notation/notation.json`; 8 symbols, 26 macros):
- Symbols: `T` (number of return observations, S1); `\Phi, \Phi^{-1}` (M4); `\gamma_3`, `\gamma_4` (M4); `R^\ast`, `R^{e\ast}`, `R_f`,
  `\mathbb{Q}` (AP1).
- Macros usable on FC1 pages: `\E`, `\Prob`, `\Var`, `\Cov`, `\Corr`, `\R`, `\N`, `\indic`, `\Normal`, `\iid`, `\dto`, `\pto`,
  `\argmax`, `\argmin`, `\tr`, `\diag`, `\SR`, `\hSR`, `\PSR`, `\DSR`, `\PBO`, `\FWER`, `\FDR`, `\FDP`, `\se`, `\emgamma`.

### 9.2 Foreseen notation conflicts (builders must avoid)

- **`T`.** Bond maturity and the number of periods are the obvious use. `T` is the registered number of observations. Use `n`
  (local, defined per lesson) for the number of periods and `\tau` for a maturity in years.
- **`R_f`** (gross riskless return, AP1). A bill or deposit rate in L01 or L02 must not be written `R_f` unless it is that quantity.
  Use `r` or `y` for rates, defined on first use.
- **`\mathbb{Q}`** (risk-neutral measure, AP1). Never use `Q` for a quantity or quote on an FC1 page.
- **`\Phi`, `\gamma_3`, `\gamma_4`, `R^\ast`, `R^{e\ast}`** (M4, AP1). Not needed on FC1; do not reuse them.
- **`\SR`, `\hSR`, `\se`, `\emgamma`** macros. `\emgamma` has no meaning given in the registry excerpt the planner read; do not
  use it. `\SR` is a Sharpe ratio (not on FC1).
- **`p`, `c`, `F`, `v`, `y`** are local letters (`notation.json` `about`: letters whose meaning is conventionally local are
  defined in each lesson). Define each on first use in its lesson. Section 5.2 uses `face_cents`, `coupon_bps`, `yield_bps`
  in code, which are not math symbols.

### 9.3 Cards builder (Builder E, after A-D)

- `course/modules/FC/FC1/cards.json`: ids `FC1-c001` upward (`check_pages.py` line 381 regex `FC1-c\d{3}`), `lesson` in `L01`-`L05`,
  `front`, `back`, `grade` (T/A/B/C/D/X), and `cite` (registry keys from section 6) or `basis` (a lab or problem that establishes the
  result, for example `"basis": "Lab L01-1 (exact)"`).
- One card per definition, theorem statement, key formula, key result (with its grade) and misconception (BUILDER §7). Each lesson
  contributes at least one card (`check_pages.py` lines 395-398). No duplicates.
- Cards cite only keys in section 6, and only after Q3 is decided.

---

## 10. Open questions for the architect (numbered; decide before the builders start)

1. **(BLOCKING, project) Scope against the graph.** Futures, swaps and options (FC2) and bond pricing (FI1) are outside FC1's closure
   (section 7.3). Options (a) plain prose plus DAG_DEFECT rows (the plan's default), (b) add FC2 or FI1 to FC1's prerequisites
   (curriculum change), (c) move the derivative objects to FC2. Blocks the project builder's `Future`, `Swap`, `Option` and the
   bond's yield pricing until decided.
2. **Bond pricing.** If Q1 is (a), `bond_price_cents` uses M1 `present-value`, `discount-factor` and `compounding-frequency` (all in
   the closure) and no FI1 concept. Confirm that the bond object is priced by the discount-factor route and no yield-to-maturity
   concept is defined in FC1.
3. **Registry year conflicts (`mishkin2021economics`, `harris2002trading`).** Options: (a) apply the CF1 Q3 precedent (cite only keys
   whose record matches the curriculum string; this excludes both, so FC1 cites no textbook); (b) apply the AC4 Q5 precedent (cite
   the key, state only the registry's own year, make no edition claim). Planner recommends (b): both records match on title and
   author, and the difference is the year alone. Architect decides; builders cite only what Q3 allows.
4. **McLeay, Radia & Thomas (2014) and the BoE route.** Admit through `tools/add_reference.py` by the Bank of England's stable URL
   (`bankofengland.co.uk` is allow-listed), or drop the claim. Until admitted, the L01 bank-money-creation claim is grade C without a
   citation or is left out. Builders do not type the record from memory.
5. **Settlement facts (L05).** Admit an SEC or equivalent primary source through `add_reference.py`, or keep the settlement period as a
   lab parameter with no factual claim. The planner recommends the second until the source is admitted.
6. **Lab count.** One lab per lesson (five twins) plus three project labs, per the M1 and E1 precedent (architect Q2). Confirm.
7. **Hours split.** 5 × 10 h lessons and a 20 h project (28.6 %). Alternative: six lessons (8, 8, 8, 8, 9, 9) with the same 20 h
   project. The five-lesson split keeps each pair of concepts in one lesson. Confirm.
8. **Real data.** Default: none (section 8.1). Alternative: `ust_daily` for the L02 rates row, or `fx_daily` for the FX row, each with
   the licence quote read by the verifier. Confirm none or name the dataset.
9. **Frozen interface and conventions.** Freeze the `instruments.py` classes, the `events()` convention, the `bond_price_cents` signature,
   and the rounding rule (half away from zero for negatives, once per output; section 5.3) before building. Precedent: E1 Q5/Q6.
10. **Hand-computed fixtures.** Permit one hand-computed fixture per instrument in `test_project.py` alongside the seed-derived tests
    (section 5.5). The fixtures are not seed answers and are stated on the project page. Confirm.
11. **Lab for L02 (weak).** The taxonomy has no formula. The plan's lab is a consistency check (every entry coded once, counts reconcile).
    Confirm it is acceptable under BUILDER §3.4 (a numerical check per key formula) or request a different check.
12. **Scope words.** The core text says "across equities, rates, credit, FX, commodities and derivatives" (yaml 370). The plan covers
    the enumerated classes only, with no claim of completeness beyond them. Confirm (scope words need a computation, section 2.1 item 4).
13. **Mutant count.** The plan follows the task's ten mutants; the verifier minimum is three (`mutate_graders.py` lines 41-43). Confirm
    ten as the FC1 requirement.
14. **Course-level studio.** STUDIO-FC requires FC1 and FC2 (yaml 353). Not part of this unit. Confirm it stays out.

---

## 11. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

```bash
.venv/bin/python tools/check_pages.py --unit FC1            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit FC1
.venv/bin/python tools/check_projects.py --unit FC1
.venv/bin/python tools/run_labs.py --unit FC1               # --page L05 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/FC/FC1/L01.html                       # per page, after twins are written
.venv/bin/python tools/embed_labs.py course/modules/FC/FC1/L05.html --refresh lab-FC1-L05-1   # after editing a twin
.venv/bin/python tools/run_graders.py --unit FC1 --seeds 0-49
.venv/bin/ruff check tests/labs/FC1 course/modules/FC/FC1/grader && .venv/bin/ruff format --check tests/labs/FC1 course/modules/FC/FC1/grader
.venv/bin/mypy tests/labs/FC1 course/modules/FC/FC1/grader
```

Verifier only (not builders): `.venv/bin/python tools/mutate_graders.py --unit FC1 --seeds 0-9`, `.venv/bin/python tools/verify_refs.py --unit FC1`
(registry identity), and `.venv/bin/python tools/page_smoke.py --unit FC1` on a quiet machine. Repo-wide gates
(`check_pages.py --all`, `check_dag.py --all`, `build_site.py --check`, `render_curriculum.py`) are the architect's, once, before any merge.

Flags: `check_pages.py`, `check_dag.py`, `check_projects.py` accept `--unit` and `--all`; `run_labs.py` accepts `--unit`, `--all`,
`--page` (`tools/run_labs.py` lines 119-121 per the E1 plan); `run_graders.py` accepts `--unit`, `--all`, `--seeds` (lines 129-131);
`mutate_graders.py` accepts `--unit`, `--all`, `--seeds` (lines 30-32). The planner did not execute these commands.

---

## 12. After the builders

1. Orchestrator integrates; runs the section 11 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02, L03-L04, L05 with the cards, project (with ten mutants and the five
   alternative implementations). Failing rows return to the owning builder with only the failing rows.
3. Ledger at `ledgers/FC1.verification.json`; verifier scripts archived under `ledgers/FC1/scripts/` (VERIFIER §3).
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. Never merged incomplete
   (an unfinished unit breaks `check_pages --all`).

---

## 13. Builder output contract (BUILDER §10), pre-filled

```
UNIT: FC1
HOURS: lessons=50 project=20 total=70 (curriculum=70)
REFERENCE_REQUESTS: McLeay, Radia & Thomas (2014); a settlement-cycle primary source; a spread-evidence source (topic only)
NOTATION_REQUESTS: none expected (section 9.2 lists the conflicts to avoid)
GLOSSARY_REQUESTS: terms outside the 10 concepts used in plain prose (for example "stop order", "dealer inventory", "variation margin") (section 3)
DATA_REQUESTS: none (default); see section 8.1 if Q8 changes this
CONTRACT_CHANGE_REQUESTS: none (no Atlas milestone)
DAG_DEFECTS: the rows in section 7.1 (futures-contract, futures-margining, interest-rate-swap, option-payoff, bond-price-yield,
  yield-to-maturity, central-counterparty, settlement-cycle, order-book-data-structure, and the others listed there)
KNOWN_LIMITATIONS: the registry year conflicts (Q3); the absent McLeay record (Q4); the project scope conflict (Q1, blocking)
```

---

## Architect decisions

Pending (section 10). This plan is the planner's proposal. Until Q1 is decided, the project builder does not start. Lessons L01-L05 may
start once Q3-Q6 are decided.

## Architect decisions (2026-10-28, binding). Where the plan states a recommendation for an open question, follow it. Defaults for every module: concepts outside the prerequisite closure are plain prose with no link and no dfn; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields only or not at all (never edit a record, never type bibliographic data); no real data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST in plans/<UNIT>-open-items.md; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every grader; not adversarial, no question bank.
Module specifics: the project covers cash instruments only (a trade-lifecycle and order-book simulator); futures, swaps and options objects are described in plain prose as later material (FC2); bond pricing by the M1 discount-factor route; mishkin2021economics and harris2002trading are cited by key with the registry's own year only; McLeay, Radia and Thomas is a REFERENCE_REQUEST, not cited.
