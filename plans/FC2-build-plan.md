# FC2 build plan: Derivatives Fundamentals (2026-10-28)

Unit: **FC2 · Derivatives Fundamentals** · tier U · 90 h · prerequisites M4, CF1 · no Atlas milestone · no debate ·
grading `both` (autograder for the arbitrage scanner, rubric for the findings note) · output directory
`course/modules/FC/FC2/` (part code `FC`) · lab twins `tests/labs/FC2/` · cards `course/modules/FC/FC2/cards.json`.
Branch `claude/fanout-b3`. Planner: Haiku, plan only. No lesson content, no git operations, no commits. Executors:
Haiku builders, then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every curriculum statement cites `file:line` read during planning. Anything not in the curriculum
is marked **NOT IN CURRICULUM**. Planner-proposed formulas in §5 are hand statements for the builder to re-derive and
the verifier to re-check; they are not sourced.

Status: `course/modules/FC/` does not exist; `ledgers/FC2/` does not exist. Nothing is built.

---

## 0. Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part FC, code `FC`, title "Finance Core"; STUDIO-FC requires FC1, FC2 (the studio is a separate unit, not in this plan) | `curriculum/02-economics-finance-core.yaml:348` (code), `:350-353` (studio, `requires` at 353) |
| FC2 id `FC2`, title "Derivatives Fundamentals", tier `U`, hours `90` | `curriculum/02-economics-finance-core.yaml:396-399` |
| Prereqs `[M4, CF1]` | `curriculum/02-economics-finance-core.yaml:400` |
| Core text: forwards, futures, swaps, option payoffs, no-arbitrage forward pricing, put–call parity, one- and multi-period binomial pricing, Black–Scholes | `curriculum/02-economics-finance-core.yaml:401-404` |
| `introduces` has 14 concepts (listed in §3) | `curriculum/02-economics-finance-core.yaml:405-419` |
| Sources: three free-text strings (Hull 11th ed. 2021; Stoll 1969; Cox, Ross & Rubinstein 1979) | `curriculum/02-economics-finance-core.yaml:420-423` |
| Lab (one sentence): "Binomial price converging to Black–Scholes." | `curriculum/02-economics-finance-core.yaml:424` |
| Project "Arbitrage scanner": "Given an embedded option-chain snapshot, detect put–call parity and convexity violations net of a stated cost model, and explain each one found." Deliverable "Scanner plus a findings note." Grading `both` | `curriculum/02-economics-finance-core.yaml:425-431` (brief 427-429, deliverable 430, grading 431) |
| No `debate:` key on FC2 | `curriculum/02-economics-finance-core.yaml:396-431` (absent) |
| No `atlas:` key on FC2; no atlas entry names FC2 (the atlas block starts at line 198; the only FC2 mentions in `meta.yaml` are lines 62, 85, 160, all in credential and topic maps) | `curriculum/02-economics-finance-core.yaml:396-431`; `curriculum/meta.yaml:198` onward |
| JSON row for FC2: `parts[5].modules[1]`, `"part": "FC"`, hours 90, prereqs M4 and CF1, 14 `introduces`, the three sources, the lab, the project with grading `both` | `curriculum/curriculum.json` `parts[5].modules[1]` (the `concepts` map gives each of the 14 concepts owner FC2) |
| M4 is tier F, hours 120, prereq M2 (so the M4 closure reaches M2 and M1) | `curriculum/01-foundations.yaml:190-194` |
| CF1 prereqs are `[M1, AC1]` in the JSON row (the architect added AC1 to CF1, per the CF1 plan's binding decisions) | `curriculum/curriculum.json` (CF1 row); `plans/CF1-build-plan.md` "Architect decisions" |

### 0.1 Prerequisite closure (computed)

`tools/coursekit.py` `prerequisite_closure("FC2")` run by the planner returned
`['AC1', 'CF1', 'M1', 'M2', 'M4', 'P0.1']` (`coursekit.py:239-249`).

Concepts usable without definition, from the closure's `introduces` (`curriculum.json`):

- **M2** (13): `limit`, `derivative`, `taylor-theorem`, `definite-integral`, `partial-derivative`, `gradient`,
  `jacobian`, `hessian`, `multiple-integral`, `implicit-function-theorem`, `envelope-theorem`,
  `finite-difference-derivative`, `automatic-differentiation`.
- **M4** (19): `random-variable`, `expectation`, `variance`, `independence`, `correlation`, `covariance-matrix`,
  `skewness`, `kurtosis`, `quantile-function`, `moment-generating-function`, `characteristic-function`,
  `normal-distribution`, `multivariate-normal`, `student-t-distribution`, `conditional-expectation-elementary`,
  `law-of-large-numbers`, `central-limit-theorem`, `heavy-tailed-distribution`, `infinite-variance-clt-failure`.
- **M1** (14): `exponential-and-logarithm`, `compounding-frequency`, `continuous-compounding`, `present-value`,
  `discount-factor`, `geometric-series`, `annuity`, `perpetuity`, `growing-perpetuity`, `amortization-schedule`,
  `quantifiers`, `direct-proof`, `proof-by-contradiction`, `mathematical-induction`.
- **CF1** (10): `net-present-value`, `internal-rate-of-return`, `multiple-irr-problem`, `payback-period`,
  `incremental-cash-flow`, `net-working-capital`, `depreciation-tax-shield`, `fisher-relation`,
  `real-vs-nominal-cash-flows`, `monte-carlo-npv`.
- **AC1** (12): `double-entry-bookkeeping`, `accrual-accounting`, `balance-sheet`, `income-statement`,
  `cash-flow-statement`, `statement-articulation`, `depreciation-and-amortization`, `gaap-vs-ifrs`,
  `revenue-recognition`, `lease-accounting`, `stock-based-compensation`, `deferred-taxes`. (No FC2 need; listed
  for completeness.)
- **P0.1** (11): `evidence-grade`, `paper-anatomy`, `identification`, `robustness-check`, `replication`,
  `steelmanning`, `project-ladder`, `prerequisite-dag`, `atlas-platform`, `citation-registry`,
  `notation-conventions`.

### 0.2 Concepts FC2 natural content would use that lie OUTSIDE the closure (DAG table; summary in §9)

Owners from `curriculum.json` `concepts`:

| Concept (owner) | Where FC2 content needs it | Resolution in this plan |
|---|---|---|
| `exchange-vs-otc` (FC1), `clearing-and-settlement` (FC1), `market-maker` (FC1), `bid-ask-spread` (FC1), `trade-lifecycle` (FC1), `order-types` (FC1) | forward vs. futures market structure (L02, L03); the clearing house behind margining (L03); the cost model in the project (bid-ask half spread) | **Recommended: add FC1 to FC2's prerequisites** (§7 Q2). Otherwise plain prose, no link, `DAG_DEFECT` per term |
| `bond-price-yield` (FI1), `forward-rate` (FI1), `day-count-convention` (FI1), `yield-conventions` (FI1), `par-yield` (FI1) | swap valuation from discount factors (L03); the day-count convention in the project | Use M1 `discount-factor` and `present-value` only; state the day-count as an explicit input; plain prose; `DAG_DEFECT` |
| `convexity` (FI1; the concept's text is not read by the planner, so its scope is unverified) | name collision with "convexity in strike" (L05) | FC2 uses `option-arbitrage-bounds` for strike convexity and writes "convexity in strike" in plain words; no link to FI1 (§6.2) |
| `brownian-motion` (SC1), `geometric-brownian-motion` (SC2), `itos-lemma` (SC2) | Black–Scholes derivation (L07) | Not derived. The formula is stated and used; its agreement with the binomial limit is a numerical observation (lab); `KNOWN_LIMITATIONS` (§7 Q3) |
| `lognormal-distribution`, `short-selling`, `put-option`, `call-option`, `risk-free-rate`, `no-arbitrage-principle`, `standard-deviation`, `volatility` | used in prose | **Not registered concepts** (no entry in `concepts`); plain prose, plain `<dfn>` without `data-concept` (accepted: `tools/check_dag.py` line 47 skips a `<dfn>` with no `data-concept`) |
| `law-of-one-price` (AP1), `equivalent-martingale-measure` (AP1), `stochastic-discount-factor` (AP1) | arbitrage and risk-neutral language (L01, L06) | Not used as concepts; FC2's `risk-neutral-probability` is scoped to the one-period binomial (§6.4) |
| `martingale` (M6), `stopping-time` (M6), `optional-stopping-theorem` (M6) | early exercise (L04) | Plain words only; no claim requiring optional stopping |
| `convex-function`, `convex-set` (M7) | convexity in strike (L05) | Plain words: second difference over an evenly or unevenly spaced grid, defined in L05 |
| `bracketing-root-finder` (M8), `newtons-method` (M8), `ieee-754-floating-point` (M8) | implied-volatility inversion (L08); float alternatives in the grader (§5.6) | Bisection described in plain words, no link; `KNOWN_LIMITATIONS` that the root-finder theory is not taught |
| `option-greeks`, `delta-hedging` (DV1); `early-exercise-boundary` (DV4); `trinomial-tree` (DV4) | later modules | Not used |

No concept FC2 needs is missing from both the closure and the plain-prose list. The DAG defects are structural, not
fatal: see §7 Q2 and Q3.

---

## 1. Feasibility of the hours (no conflict, no STOP)

The curriculum figure is 90 h (`curriculum/02-economics-finance-core.yaml:399`). Tool rules:

- each lesson `data-hours` 6–12 (`tools/check_pages.py` line 227);
- hub `data-hours-lessons + data-hours-project = 90` (`tools/check_pages.py` line 337);
- project share 10–40 % of 90, i.e. 9 to 36 h (`tools/check_pages.py` lines 339–340);
- lessons sum to the hub's lessons figure (`tools/check_pages.py` lines 341–342).

Chosen split (§2): **8 lessons, 60 h; project 30 h (33 %)**. Lessons 6+8+9+7+8+8+8+6 = 60. Feasible.

---

## 2. Outline (one row per lesson; the concept assignment is fixed; each concept in exactly one row)

| Lesson | Title (working) | Concepts defined here (`<dfn>`, each exactly once) | Lab twin id (`tests/labs/FC2/<id>.py`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Arbitrage and the no-arbitrage principle | `arbitrage-opportunity` | `lab-FC2-L01-1`: a finite two-date, two-state price set on exact `Fraction`s; a zero-cost portfolio with a strictly positive payoff in every state is detected and its profit reported; a consistent set reports none | 6 | Builder A |
| L02 | Forward contracts and the cost of carry | `forward-contract`, `cost-of-carry-forward-price` | `lab-FC2-L02-1`: forward price \(F=S e^{r\tau}\) (continuous compounding, no income); the replicating portfolio (buy the asset, borrow) reproduces the forward payoff in every state; a mispriced forward is exploited with zero net cash flow | 8 | Builder A |
| L03 | Futures, margining and swaps | `futures-contract`, `futures-margining`, `interest-rate-swap` | `lab-FC2-L03-1`: a seeded SIMULATED futures price path; daily variation-margin cash flows sum to the terminal settlement; a swap's fixed leg from discount factors and the par-rate identity \(R_{\mathrm{par}}=(1-\mathrm{DF}_N)/\sum_i\mathrm{DF}_i\) checked exactly | 9 | Builder A |
| L04 | Option payoffs and American versus European exercise | `option-payoff`, `american-option` | `lab-FC2-L04-1`: call and put payoff and profit tables at expiry on a price grid; the exercise comparison for one contract with and without early exercise (the payoff argument only; the theorem waits for L05) | 7 | Builder B |
| L05 | Put–call parity and model-free bounds | `put-call-parity`, `option-arbitrage-bounds` | `lab-FC2-L05-1`: the parity residual on a constructed synthetic price set (exactly zero by construction and checked by the portfolio payoff, not by the formula alone); bounds and strike convexity checked on an evenly spaced strike grid | 8 | Builder B |
| L06 | One- and multi-period binomial pricing | `binomial-option-pricing`, `risk-neutral-probability` | `lab-FC2-L06-1`: one-period replicating portfolio value equals the risk-neutral discounted expectation; multi-period backward induction on a recombining tree in `Fraction`, checked against a direct replication for a two-step tree | 8 | Builder C |
| L07 | The Black–Scholes formula and the binomial limit | `black-scholes-formula` | `lab-FC2-L07-1` (**the curriculum lab**, `curriculum/02-economics-finance-core.yaml:424`): binomial price for a stated list of step counts against the closed-form Black–Scholes value, error column printed; closed form uses `math.erf` (standard library) | 8 | Builder C |
| L08 | Implied volatility | `implied-volatility` | `lab-FC2-L08-1`: bisection inversion of a Black–Scholes price to a stated tolerance; round trip recovers the input volatility; a price outside the no-arbitrage bounds is rejected with a named condition | 6 | Builder C |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 60/30 | none | none | none | Builder A |
| project | Arbitrage scanner (`both`, §4) | none | `lab-FC2-project-1` (rung 1, worked), `lab-FC2-project-2` (rung 2, `class="lab completion"`), `lab-FC2-project-3` (rung 3 check) | 30 | Builder D |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` | none | none | none | Builder D |
| cards | `cards.json` from L01–L08 | none | none | none | Builder E (after A–D) |

Concept count: 1+2+3+2+2+2+1+1 = 14 = `introduces` (`curriculum/02-economics-finance-core.yaml:405-419`). Every concept appears in one row.

Hours: 6+8+9+7+8+8+8+6 = 60 (lessons; hub `data-hours-lessons="60"`); project 30 (hub `data-hours-project="30"`); 90 total.

Ordering check (no lesson links a concept defined later):
- L02 uses L01 (`arbitrage-opportunity`) and M1 (`continuous-compounding`, `present-value`).
- L03 uses L02 (`cost-of-carry-forward-price`) for the futures-forward relation, and M1 (`discount-factor`) for the swap.
- L04 uses L01 for the no-arbitrage language and M1 for nothing else.
- L05 uses L02 (cost of carry), L04 (`option-payoff`, `american-option`), and M2 (`finite-difference-derivative` for the strike grid).
- L06 uses L01, L02, L05 (`option-arbitrage-bounds` for the monotone pricing argument, optional), and M4 (`expectation`).
- L07 uses L06 (`binomial-option-pricing`, `risk-neutral-probability`), M4 (`normal-distribution`, `central-limit-theorem` in prose), M2 (`limit`).
- L08 uses L07 (`black-scholes-formula`) and L05 (`option-arbitrage-bounds`).

---

## 3. Hub (`index.html`, Builder A)

- `<html lang="en" data-root="../../../" data-unit="FC2" data-page="index">`;
  `<main data-hours-lessons="60" data-hours-project="30">` (sums to 90; project 33 %).
- 4–8 `ol.objectives` items, measurable verbs. Target six, for example: derive the no-arbitrage forward price from a
  replicating portfolio; construct the payoff and profit of a call, a put and a futures position; apply put–call
  parity and the model-free bounds to a price set; compute a one-period and a two-period binomial price; state the
  Black–Scholes formula and check it against a binomial price; invert a Black–Scholes price for implied volatility.
- Prerequisites: M4, CF1 (with links to the closure concepts used on the hub:
  `../../../concepts.html#normal-distribution`, `…#present-value`, `…#discount-factor`, `…#net-present-value`, and
  any other concept the hub names).
- Placement: `<section class="quiz" id="placement" data-unit="FC2" data-page="placement" data-mastery="0.8">` with
  at least nine items (`tools/check_pages.py` lines 351–353: `data-mastery` and two or more `data-skill` items). At
  least two `data-skill` items test what rungs 1–2 teach (the worked example's parity-based check and the completion
  problem's missing forward-price line). The rest test M4 and CF1 prerequisites (`expectation`, `variance`,
  `normal-distribution`, `net-present-value`, `discount-factor`). The 0.8 bar matches the M1, E1 and CF1 precedent.
- Lesson map: one link per L01–L08 (`href="Lnn.html"`) and one to `project.html`.
- Ladder: `<ol class="ladder">` with four `li` and `span.rung-title` in the order `Worked example`, `Completion problem`,
  `Independent project`, `Stretch` (`tools/check_projects.py` line 33).
- Rungs 1–2 keep standard length, because FC2 is tier U. BUILDER_RULES §5.1 makes them minimal only from tier M upward
  (the same rule E1 applied at tier F).

---

## 4. Project: "Arbitrage scanner" (Builder D)

### 4.1 Ladder (BLUEPRINT §5.1)

1. **Rung 1, worked example** (`lab-FC2-project-1`, skippable on placement): one fully solved, annotated scan of a
   six-contract SIMULATED chain: the parity gap for each strike, the convexity test on the strike grid, the net-of-cost
   decision, and the explanation line for each finding. A "why" annotation at every step.
2. **Rung 2, completion** (`lab-FC2-project-2`, `class="lab completion"`): the same scan with the parity-gap line and
   the cost-netting line replaced by `___`. Graded instantly. The twin is the completed solution; every page line equals
   the twin line or contains a blank (`tools/run_labs.py` completion rule, as in E1).
3. **Rung 3, independent project** (graded): (a) the autograded module `scanner.py` to the §4.3 interface;
   (b) the findings note, rubric-graded (§4.6). `lab-FC2-project-3` is the rung-3 check: it calls the scanner on the
   reference SIMULATED chain and prints the findings table.
4. **Rung 4, stretch** (optional, not graded): extend the scanner to a chain with a known discrete dividend, with the
   parity adjustment stated as a hypothesis before it is run; or a calendar-spread check (NOT IN CURRICULUM as a
   concept; plain words only).

### 4.2 Spec (`dl.spec`; `tools/check_projects.py` lines 34–49)

Terms present (in this order, with these words): **Context**, **Inputs**, **Required outputs**, **Constraints**,
**Grading**.

- **Context.** A desk wants a daily check of one expiry's European option quotes for model-free violations, net of the
  cost it actually pays to trade them. Each finding must be explained, not only listed.
- **Inputs.** A SIMULATED chain in a documented JSON-like dict: `spot_cents` (int), `df_ppm` (int, the discount factor to
  expiry in parts per million, supplied rather than computed, so the parity check is exact), `strikes_cents` (strictly
  increasing ints), `call_cents` and `put_cents` (ints, quotes in cents), and a `cost` dict: `fee_cents_per_contract`
  (int) and `half_spread_cents` (int, paid per leg). Integer basis points are used for any rate, and no dividends
  (assumption A1, §5.2). The chain is labelled **SIMULATED** on the page.
- **Required outputs.** `scanner.py` with the three functions in §4.3, and `findings.md` (the memo).
- **Constraints.** Integer cents everywhere. Each money output is computed from exact `Fraction`s and rounded once, half
  up, to the nearest cent (rule stated on the page, in the spec and in the module docstring). Standard library only.
  The same code runs in Pyodide and under pytest. Invalid input raises the exception types in §4.4.
- **Grading.** Autograder (`grader/test_project.py`, dual mode) and rubric (`findings.md`, §4.6). The spec must name
  both the autograder and the rubric (`tools/check_projects.py` lines 38–49).
- **Reading list.** `ol.reading-list`: `cox1979option`, `stoll1969relationship`, `hull2021options` (§5.4 for the
  registry status of each).

### 4.3 Interface (planner proposal; the architect freezes it, §7 Q7)

- `parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int`:
  the cent-rounded value of \(C - P - (S - K\,\mathrm{df})\), with `df = df_ppm / 1_000_000`, computed in `Fraction`.
- `convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]`: the indices \(j\)
  (strictly interior) at which the discounted second difference of call prices is negative, as in §5.3. Output is a
  list of indices, not money, so no rounding.
- `scan(chain: dict[str, object]) -> list[dict[str, object]]`: one record per finding with keys `kind` (`"parity"` or
  `"convexity"`), `strike_cents` (int), `gross_cents` (int), `net_cents` (int, after the cost in §5.3), and
  `explanation` (a non-empty string naming the rule and the assumption it depends on). Every returned record is a finding,
  and a finding is returned only if `net_cents > 0` (strict).

### 4.4 Exception table (grader tests demand these types, and only these)

| Condition the page names | Exception | Message must name |
|---|---|---|
| `strikes_cents` not strictly increasing, or any strike `<= 0` | `ValueError` | "strikes must be strictly increasing and positive" |
| `df_ppm` not in `1..1_000_000` | `ValueError` | "df_ppm must lie in 1..1000000" |
| `len(strikes_cents) != len(calls_cents)` | `ValueError` | the two lengths |
| `fee_cents_per_contract < 0` or `half_spread_cents < 0` | `ValueError` | "cost terms must be non-negative" |

Any other invalid input may raise any exception or return. The grader's tests do not require a type for those.

### 4.5 Time budget (`<table id="hours">`, rows sum to 30; each row needs a one-line rationale)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One solved SIMULATED chain, annotated line by line |
| Rung 2, completion problem | 3 | Fill the parity-gap line and the cost-netting line, then run the instant check |
| Derivations: parity, bounds, the cost-netting rule (proofs in §5) | 5 | Write the proofs with the assumptions named |
| `scanner.py` (three functions, exact arithmetic, the exception table) | 9 | Implement to §4.3 and §4.4; pass the suite on seeds 0–49 |
| Edge cases, local pytest runs on the student's seed | 3 | Ties at half a cent, one-strike chains, boundary costs |
| Findings note (rubric) | 5 | Explain each finding, its assumption, and what would settle it |
| Self-assessment against exemplars | 3 | Score the note, then compare with exemplar level 4 and level 2 |
| **Total** | **30** | Equals `data-hours-project` on the hub |

### 4.6 Rubric (`findings.md`; `both` requires it, `tools/check_projects.py` lines 58–71)

Five criteria, four observable levels each (level 4 down to level 1). Every descriptor names something a grader can see:

1. **Each finding is reproduced.** Level 4: every finding lists its strike, the gross and net amounts in cents, and the
   leg prices used. Level 1: "lists some violations".
2. **Cost netting.** Level 4: states the cost model and says for each finding whether it survives the cost.
3. **Assumptions.** Level 4: names the assumptions each finding depends on (European exercise, one expiry, no income,
   the supplied discount factor).
4. **Model-free versus model-dependent.** Level 4: separates findings that use only no-arbitrage rules from any that
   need a model input.
5. **Explanation and settlement.** Level 4: for each finding, a data error versus a true violation, with the check that
   would settle it. Level 1: "the market is inefficient".

Exemplars: `data-level="4"` and `data-level="2"`, fully written on a SIMULATED chain, each annotated with the descriptors
it meets or misses. Self-assessment form (`section.rubric-self`, as in E1 §5.5). The page shows where the student's
scores diverge from the exemplars' scores. No question bank: the note is not an IC defence or a debate (§7 Q9).

### 4.7 Grader panel (`project.html`)

`<section class="grader-panel" id="grader" data-unit="FC2" data-grader="grader/" data-suite="test_project.py"
data-support="instance.py" data-solution="scanner.py" data-starter="starter.py" data-packages="">`. Standard library
only, so `data-packages` is empty. The grader panel must point at `grader/instance.py` defining
`make_instance(seed: int)` (`tools/check_projects.py` lines 122–136). No Atlas path (no milestone; the check at
`tools/check_projects.py` lines 144–146 does not apply).

---

## 5. Mathematics and grader design

### 5.1 Notation for the unit (BUILDER_RULES §3.2; `notation/notation.json`)

Registered symbols that FC2 must respect (their meanings are binding):

| Registered | Meaning (`notation/notation.json`) | FC2 consequence |
|---|---|---|
| `T` (`symbols[0]`, module S1) | number of return observations | FC2 **must not** use `T` for time to expiry. Use \(\tau\) |
| `R_f` (`symbols[6]`, AP1) | gross riskless return for the period, the reciprocal of the price of a sure payoff of 1 | The one-period binomial uses \(R_f = 1+r_{\text{per period}}\). The continuously compounded rate is \(r\), not \(R_f\) |
| `\mathbb{Q}` (`symbols[7]`, AP1) | a probability measure, by default an equivalent martingale (risk-neutral) measure | The risk-neutral probabilities are written under \(\mathbb{Q}\). FC2 does not claim EMM theory (AP1's) |
| `\Phi` (`symbols[1]`, M4) | standard normal CDF | Black–Scholes uses \(\Phi\) with that meaning |
| `\gamma_3`, `\gamma_4` (`symbols[2,3]`) | skewness, kurtosis | FC2 must not use \(\gamma\) for the option Greek; use \(\Gamma\) if an option gamma appears (optional) |
| `R^\ast` (`symbols[4]`, AP1) | the SDF return | do not use an asterisk on \(R\) |
| macros `\E`, `\Prob`, `\Var`, `\Normal`, `\indic` (`macros`) | expectation, probability, variance, normal distribution, indicator | Use them; do not redefine |

Local letters (not registered; each lesson defines the ones it uses, `notation/notation.json` `about`): \(S\) spot, \(K\)
strike, \(F\) forward price, \(C\), \(P\) call and put prices, \(\sigma\) volatility, \(\tau\) time to expiry, \(r\)
continuously compounded rate, \(u\), \(d\) binomial multipliers, \(p\) (local; FC2 does not use \(p\) for the SDF of
AP1), \(\mathrm{df}\) discount factor, \(\delta\) a dividend yield (used only in the optional stretch). FC2 does not use
\(q\) for a dividend yield, because \(q\) is the natural letter for the risk-neutral probability.

NOTATION_REQUESTS: none required. If the builder needs a symbol that a registered one already carries, use the
local letter above and say so in the lesson.

### 5.2 Assumptions (named, numbered, per proposition; BUILDER rule for T-graded results)

Every T-graded proposition lists the assumptions it uses, by number. Planner's proposed global numbering, used in
every lesson and in the project:

- **A1.** No dividends, storage costs or other income on the underlying over the life of the contract.
- **A2.** No transaction costs, no bid–ask spread, no short-sale constraint, and unlimited borrowing and lending at the
  riskless rate, except where a lesson or the project adds a cost explicitly.
- **A3.** No arbitrage: any portfolio with zero cost and non-negative payoff in every state has zero payoff in every
  state. (The "no-arbitrage principle", a hypothesis, not a fact.)
- **A4.** The riskless rate is constant over the life of the contract, continuously compounded at rate \(r\), so the
  discount factor to expiry is \(e^{-r\tau}\).
- **A5.** European exercise (only at expiry) unless the proposition says otherwise.
- **A6.** (L06 and L07 only) The one-period binomial: \(0 < d < R_f < u\), and the stock takes one of two values at the
  next date. Multi-period: recombining tree with the same \(u\) and \(d\).
- **A7.** (L07 and L08 only) The Black–Scholes model: lognormal terminal price with volatility \(\sigma\), constant \(\sigma\)
  and \(r\), no dividends. Stated as a model assumption, not derived (§7 Q3).

Each lesson uses the numbering above and does not invent a second scheme.

### 5.3 Planner's proposed statements and closed forms (for the builder to derive; the verifier re-derives)

All hand statements; the builder re-derives each in full (BUILDER_RULES §3.5) and the verifier checks each.

1. **Forward price (L02, T under A1–A4).** \(F = S e^{r\tau}\). Derivation: the portfolio "long the asset, short a forward at
   \(F\)" has payoff \(S_\tau - F\) at expiry; the replicating portfolio "buy the asset, borrow \(S\) at \(r\)" costs zero
   net and pays \(S_\tau - S e^{r\tau}\) at expiry; by A3 the two forward prices must coincide.
2. **Put–call parity, European, same strike and expiry (L05, T under A1–A5).** \(C - P = S - K e^{-r\tau}\). Derivation
   from the portfolio "long call, short put, short the asset, lend \(K e^{-r\tau}\)" whose payoff is zero in every state
   at expiry, so its zero-cost value is zero by A3.
3. **Model-free bounds (L05, T).** Under A2–A5: \(C \le S\); \(C \ge \max(S - K e^{-r\tau}, 0)\); \(P \le K e^{-r\tau}\);
   \(P \ge \max(K e^{-r\tau} - S, 0)\). Each follows from one dominance argument written out in full.
4. **Convexity in strike (L05, T under A2–A5).** For strikes \(K_1 < K_2 < K_3\) with \(K_2 = \lambda K_1 + (1-\lambda) K_3\),
   \(\lambda = (K_3 - K_2)/(K_3 - K_1)\): \(C(K_2) \le \lambda C(K_1) + (1-\lambda) C(K_3)\). The proof is a payoff
   dominance on the butterfly position. A discrete second difference is taken with the unequal-grid weights above, not
   with a fixed step.
5. **One-period binomial (L06, T under A3, A6).** With \(p^\ast = (R_f - d)/(u - d)\) (written under \(\mathbb{Q}\) as
   \(\mathbb{Q}(\text{up}) = p^\ast\)), the value is \(V_0 = \mathbb{E}^{\mathbb{Q}}[V_1]/R_f\). Derivation: the replicating
   portfolio (\(\Delta\) shares, \(B\) bonds) solves two linear equations; the solution is unique because \(u \ne d\).
6. **Multi-period binomial (L06, T under A3, A6).** Backward induction on the recombining tree gives the same value as
   the discounted \(\mathbb{Q}\)-expectation of the terminal payoff, because each node satisfies item 5.
7. **Black–Scholes formula (L07, stated; not derived).** \(C = S\,\Phi(d_1) - K e^{-r\tau}\Phi(d_2)\), with
   \(d_1 = [\ln(S/K) + (r + \sigma^2/2)\tau]/(\sigma\sqrt{\tau})\), \(d_2 = d_1 - \sigma\sqrt{\tau}\). Only the formula is
   claimed; the binomial agreement is a numerical observation (lab L07). Under A7 the claim is graded T as a formula
   only if derived; otherwise grade C with the citation `black1973pricing` only after §7 Q4 is decided.
8. **Put value (L05/L07).** Use item 2 (parity) and item 7; do not restate the put formula as an independent result.
9. **Swap par rate (L03, T under the single-curve discount-factor model).** With \(\mathrm{DF}_i\) the discount factors to
   the \(N\) payment dates, the fixed rate \(R\) that gives the fixed leg equal to the floating leg solves
   \(R = (1 - \mathrm{DF}_N)/\sum_{i=1}^{N}\mathrm{DF}_i\) per unit period, under the assumption (named as A8 in L03) that
   the floating leg resets at par. The telescoping sum \(\sum_i (\mathrm{DF}_{i-1} - \mathrm{DF}_i) = \mathrm{DF}_0 - \mathrm{DF}_N\)
   is the proof. The forward rate it implies is written in plain words (no `forward-rate` link).
10. **Futures margining (L03, T as an accounting identity).** The sum of daily variation-margin flows equals the terminal
    settlement minus the initial price, when no interest accrues on the margin account (A8' in L03: margin is not
    remunerated, stated).

### 5.4 Registry keys the unit may cite (verified in `references/references.json`; §6 for status)

| Key | Record (as read) | Use in FC2 | Flag |
|---|---|---|---|
| `hull2021options` | Hull, "Options, Futures, and Other Derivatives", 2021, ISBN 9780136940166, `used_by` FC2, verified | The curriculum's textbook source (`curriculum/02-economics-finance-core.yaml:421`). Book-level conventions only, no locator until read | The record has no edition field; "11th ed." from the curriculum string is unverified in the registry (§7 Q5) |
| `stoll1969relationship` | Stoll, "THE RELATIONSHIP BETWEEN PUT AND CALL OPTION PRICES", 1969, DOI 10.1111/j.1540-6261.1969.tb01694.x, `used_by` FC2, verified | Parity attribution (`curriculum/02-economics-finance-core.yaml:422`). The parity result itself is graded T by §5.3 item 2 | The record has no volume or issue; "JF 24(5)" is unverified in the registry |
| `cox1979option` | Cox, Ross & Rubinstein, "Option pricing: A simplified approach", 1979, DOI 10.1016/0304-405x(79)90015-1, `used_by` FC2, verified | Binomial model attribution (`curriculum/02-economics-finance-core.yaml:423`) | The record has no volume or issue; "JFE 7(3)" unverified in the registry |
| `black1973pricing` | Black & Scholes, "The Pricing of Options and Corporate Liabilities", 1973, DOI 10.1086/260062, verified, `used_by` DV1 | Primary source for the Black–Scholes formula (L07, L08) | **Not curriculum-listed**; FC2 is not in its `used_by`. Needs an architect decision (§7 Q4) |
| `merton1973theory` | Merton, "Theory of Rational Option Pricing", 1973, verified, `used_by` DV1 | Not recommended for FC2 | Not curriculum-listed; no use planned |
| `harrison1979martingales` | Harrison & Kreps, "Martingales and arbitrage in multiperiod securities markets", 1979, verified, `used_by` AP1 | Not recommended; EMM is AP1's concept | Not curriculum-listed |

The unit cites only the three curriculum-listed keys by default. `black1973pricing` is added only after the architect
decides §7 Q4. No other key may be cited.

Keys that belong to other modules and must not be cited from FC2: `harris2002trading` and `mishkin2021economics` (FC1),
`shleifer1997limits` (AP1, AP6), `ross1976arbitrage` (AP2).

### 5.5 Grader design (Builder D)

Files: `course/modules/FC/FC2/grader/`: `instance.py`, `reference.py` (the solution; excluded from deployment,
BLUEPRINT §7), `starter.py` (`NotImplementedError` stubs; the suite must fail on it), `test_project.py`.

- **`instance.py`**: `make_instance(seed: int) -> dict[str, object]`. Deterministic from `random.Random(seed)`. Generates a
  SIMULATED chain: six or seven strikes on an evenly spaced grid, a spot, a `df_ppm`, call and put quotes generated from a
  parity-consistent price plus a planted violation on a seed-dependent subset of strikes (some with a parity violation,
  some with a convexity violation, some with none), and a cost model. Every generated chain is valid
  (strictly increasing strikes, `df_ppm` in range, cost terms non-negative). The generator **never produces an exact
  half-cent tie** (`gross` with denominator 2 at the cent), so that the float alternatives in §5.6 are not penalised for
  rounding ties; the tests that require a half-cent tie build it by hand in `test_project.py`. Labelled **SIMULATED**
  in the docstring. Seeds 0–49 give materially different findings (different strikes flagged, different net amounts).
- **`reference.py`**: the full solution; `Fraction` throughout, one half-up rounding per money output. Passes every test on
  seeds 0–49 (`run_graders.py --unit FC2 --seeds 0-49`).
- **`test_project.py`** (properties and numbers; no hard-coded answers; each test recomputes the expected value by an oracle
  written apart from `reference.py`, from the instance's own generating parameters):
  - parity: `parity_gap_cents` equals the exact \(C - P - S + K\,\mathrm{df}\) rounded half up, for every strike;
  - a parity-consistent chain (no planted violation) gives an empty parity finding list;
  - a planted parity violation is found with the planted gross amount;
  - convexity: `convexity_violations` agrees with an exhaustive check over all interior triples for chains of length ≤ 7;
  - net-of-cost rule: a finding is kept if and only if `net_cents > 0`; a violation with `gross == fee + spread` is **not**
    kept (boundary test, hand-built);
  - integer output: every money key is an `int`; every output rounded once, half up (a hand-built half-cent case);
  - edge cases: one-strike chain (no convexity findings), `df_ppm = 1_000_000` (zero rate, parity reduces to \(C - P = S - K\));
  - exception table §4.4: each named condition raises `ValueError` whose message names the condition; no other exception type
    is required.
  - Failure messages name the violated property and hint at the concept. They never print the answer.
- **Dual mode.** The same suite runs in Pyodide and under pytest; each test under 5 s in Pyodide; the suite under 60 s.
- **Five alternative correct implementations** (all must pass; the verifier writes them as test-only fixtures in its
  scratch checkout and archives the scripts under `ledgers/FC2/scripts/`):
  1. `Fraction` throughout (the reference's approach, written independently);
  2. integer-only arithmetic with an explicit half-up division helper;
  3. float arithmetic with the same half-up rounding rule applied to the float result, using the generator's no-tie property;
  4. convexity by adjacent differences on the strike grid (an equally spaced grid specialisation, valid for the generated chains only where the spacing is equal — the test set includes an unequal-grid case the implementation must handle to pass);
  5. the parity check through the forward price, \(F = S/\mathrm{df}\), comparing \((F - K)\,\mathrm{df}\) with \(C - P\).
  Alternative 4 counts only if it handles unequal strike spacing. The verifier's unequal-grid test is part of the suite;
  an implementation that fails it is replaced by another correct one, so the five stay five.

### 5.6 Mutants (ten, each a complete module under `ledgers/FC2/mutants/`; each must be killed; VERIFIER §2.6 requires at least three, so ten is the stricter bar)

1. parity with the strike not discounted (uses \(K\) instead of \(K\,\mathrm{df}\));
2. parity sign flipped (\(S - C + P\));
3. the cost charged once per chain instead of per leg;
4. costs ignored (gross violations reported as findings);
5. convexity on the input order of strikes, not the sorted order (kills on a shuffled-strike test);
6. convexity tested with the first difference instead of the second;
7. rounding by truncation toward zero instead of half up (killed by the hand-built half-cent test);
8. `df_ppm` read as parts per thousand (\(\mathrm{df} = \mathrm{df\_ppm}/1000\));
9. the net-of-cost rule uses `>=` (boundary test, `gross == fee + spread`);
10. a hard-coded answer for seed 0, returning seed 0's findings for any seed.

Each mutant's docstring's first line names its error. `mutate_graders.py --unit FC2 --seeds 0-9` must report every mutant killed.

### 5.7 Lab numerics (Builders A–C)

- Every lab is standard library only (`fractions`, `math`, `random`), seeded where random (`random.Random(seed)`), no network,
  no warnings under `python -I -W error` (`tools/run_labs.py` line 55), under 10 s in Pyodide.
- Every twin ends with an unconditional `main()` call at module top level and has no `if __name__ == "__main__":` guard,
  because the runner executes the twin as a script (`tools/run_labs.py` line 55).
- Exact labs (L01–L06, L08's round trip where exact) print exact values; closed forms that use `math.erf` (L07) print to
  a stated number of decimals and the hypothesis says so. Numbers in prose come from unrounded values and state the rounding
  used at display (E1 §2.1 item 1).
- Labels: SIMULATED only where data is generated (the project chain, the L03 futures path). Exact computations are not labelled
  SIMULATED.

---

## 6. Lesson content rules specific to FC2

1. **Prose numbers.** Every number is computed from `Fraction`s or stated as a model input; display rounding is stated.
2. **Convexity name.** The phrase "convexity" in FC2 means convexity in strike only, and is written "convexity in strike"
   on first use in L05. No link to FI1's `convexity`, whose scope the planner did not verify.
3. **Scope words.** "every", "all", "never", "any" are used only where a proof, a finite check or a lab computes the claim
   (E1 §2.1 item 4). "No-arbitrage" is a hypothesis (A3), never a fact about markets.
4. **Risk-neutral probability.** Defined in L06 for the one-period binomial and the multi-period tree only (`risk-neutral-probability`,
   "Risk-neutral probability (binomial)"). It is not the AP1 equivalent martingale measure. The builder writes "in the binomial
   model, the probabilities under which the discounted stock is a martingale" as a remark, not a theorem.
5. **American exercise.** L04 defines the concept and gives the payoff argument for a contract with no income. The result that
   early exercise of a non-dividend call is never optimal is proved in L05 from the bounds (§5.3 item 3), not stated in L04.
6. **Black–Scholes.** L07 states the formula, names A7, and establishes the agreement with the binomial limit as a numerical
   observation only. The derivation via Brownian motion is not taught (§7 Q3). No claim of a theorem about convergence.
7. **Swaps.** L03 uses the single-curve discount-factor model (A8 in L03). It names the simplification and does not discuss
   multi-curve pricing (FI6's `multi-curve-discounting` is outside the closure).
8. **Money.** Integer cents for every money output of the project; option quotes in cents; the L03 futures path in integer
   ticks or cents (stated). Float money is not allowed in any shared code.
9. **Layout.** No horizontal scroll at 360 px: wide tables wrap or sit in a scrolling container; code blocks scroll inside their
   own container; KaTeX display blocks scroll in their container.
10. **Labs run top-level `main()`** (§5.7).

---

## 7. Open questions and blocking issues (numbered; each needs a decision before the builders start)

**BLOCKING (for the project spec, not for the lessons):**

- **B1. The project brief names data the program cannot embed.** The brief says "Given an embedded option-chain snapshot"
  (`curriculum/02-economics-finance-core.yaml:427-429`). `course/assets/data/market/MANIFEST.json` holds three snapshots only
  (`fx_daily`, `fx_monthly`, `ust_daily`; `tools/data_sources.yaml` lines 19, 53, 91), none of them options data.
  BLUEPRINT §5.3 and BUILDER_RULES §6.6 allow an embedded snapshot only with a quoted redistribution statement. No such
  statement exists for an option-quote source in the registry or in `tools/data_sources.yaml`. `cboe.com` is on
  `references/authorities.yaml` as an allow-listed issuer domain (identity only); the planner did not read its data terms and
  makes no claim about them. **Planner recommendation:** the project uses a **SIMULATED** chain generated by `instance.py`,
  plus a documented bring-your-own-chain schema (validated by `scan`'s input checks, data never leaves the browser), and a
  `DATA_REQUESTS` entry for a candidate options-quote source whose licence must be quoted before any embedding. The project
  page carries the honest-pending note. The architect decides; this changes the spec's Inputs (§4.2) only.

**Non-blocking decisions:**

- **Q2 (DAG).** Add FC1 to FC2's prerequisites? (FC1 is at `curriculum/02-economics-finance-core.yaml:363`.) Without it, the forward/futures market-structure words, the clearing house,
  and the bid–ask cost model (`exchange-vs-otc`, `clearing-and-settlement`, `bid-ask-spread`, `market-maker`) are plain prose
  with a `DAG_DEFECT` each. Adding FC1 pulls in P0.1 and E1 (already in the graph; no cycle, since neither depends on FC2;
  `curriculum/02-economics-finance-core.yaml:14-40` is E1 and `:64-72` is FC1's prereqs `[P0.1, E1]`). **Recommended** (the CF1
  precedent, §0). Hours unchanged.
- **Q3 (DAG and claim scope).** Black–Scholes is not derived: `brownian-motion` (SC1), `geometric-brownian-motion`,
  `itos-lemma` (SC2) are outside the closure, and there is no registered concept for lognormal distributions. Recommended:
  state the formula under A7, use it, and record the binomial agreement as a numerical observation (L07 lab). Record a
  `KNOWN_LIMITATIONS` line that the formula is not derived. Alternative: add SC1 to FC2 (large change; not proposed).
- **Q4 (registry).** Admit `black1973pricing` for FC2 (the primary Black–Scholes source; `used_by` currently DV1)? Recommended
  **yes**, cited at book level in L07 and L08 with no locator, and FC2 added to its `used_by`. `merton1973theory` and
  `harrison1979martingales` are not admitted for FC2.
- **Q5 (registry identity).** The registry records for `hull2021options`, `stoll1969relationship`, and `cox1979option` carry
  no edition, volume or issue (`references/references.json`). The curriculum strings ("11th ed.", "JF 24(5)", "JFE 7(3)") are
  therefore unverified in the registry. Recommended: the verifier checks them through `tools/verify_refs.py --unit FC2`; the
  builders cite only the keys, at book or paper level, and quote no edition or volume until the registry confirms it.
- **Q6 (conventions).** Rates in integer basis points; time to expiry in integer days over a stated year-length (365);
  discount factor supplied as `df_ppm` so the parity check is exact. The day-count concept is FI1's (outside the closure),
  so the convention is stated as an input in plain words. Confirm.
- **Q7 (interface).** Freeze the three `scanner.py` signatures in §4.3 and the chain schema in §4.2 before building. (The
  architect may rename them; the builders must not change them afterwards.)
- **Q8 (money).** Integer cents with one half-up rounding per output, and `df_ppm` integer ppm, as the planner recommends.
  Confirm, or choose `Fraction` throughout (then no money key is an `int`, which conflicts with the cents rule).
- **Q9 (adversarial).** The findings note is not an IC defence or a debate. No question bank; `tools/check_projects.py`
  requires one only when the page carries `id="question-bank"` (line 140). Confirm.
- **Q10 (hours).** 60 h lessons (8 lessons: 6, 8, 9, 7, 8, 8, 8, 6) and a 30 h project (33 %). Alternative: 9 lessons of about
  6.7 h. The 8-lesson split keeps each concept group together. Confirm.
- **Q11 (labs).** One lab per lesson (eight twins) plus three project labs, the M1, E1 and CF1 precedent. The curriculum names
  one lab (line 424). Confirm.
- **Q12 (plain terms).** Confirm that plain `<dfn>` without `data-concept` is accepted for unregistered terms such as
  "lognormal distribution", "short sale", "put", "call", "risk-free rate", "no-arbitrage principle" (`tools/check_dag.py`
  line 47). Each goes to `GLOSSARY_REQUESTS` for the architect to decide whether to add a glossary entry.
- **Q13 (mutant count).** The orchestrator asks for ten student-error mutants. VERIFIER §2.6 asks for at least three. This plan
  adopts ten, which satisfies both. Confirm.
- **Q14 (`risk-neutral-probability` scope).** Confirm that FC2 defines the one-period and multi-period binomial probabilities
  only, and does not touch AP1's `equivalent-martingale-measure` (§6.4).
- **Q15 (Atlas).** None. No `atlas/FC2.contract.md` is needed or drafted. `tools/check_projects.py` line 144 checks an Atlas
  contract only when the project names one; FC2 names none (`curriculum/02-economics-finance-core.yaml:425-431`).

---

## 8. Registry, references and requests

### 8.1 REFERENCE_REQUESTS (topics only; no bibliographic data typed here)

- R1: a primary rule source for futures variation margin and daily settlement (topic: how a clearing house settles a futures
  position daily). Candidate domain: `cftc.gov` (allow-listed issuer). Needed for L03's margining claim. Confidence the source
  exists: high; the citation string is not typed.
- R2: an empirical source for any graded-B or graded-C claim about listed-option parity deviations in practice ("where the
  canon breaks", L05). Needed only if such a claim is written; none is written by default.
- R3: no request for swap conventions: Hull (curriculum-listed) covers the topic at book level.

### 8.2 DATA_REQUESTS

- D1: an options-quote source with an issuer statement permitting copying and redistribution, quoted in `licence` with its
  page in `licence_url`; the snapshot, the MANIFEST entry and the transform are then built by `tools/fetch_data.py`. None is
  cleared now. Until cleared, the project uses SIMULATED chains (§7 B1). Source URL, series, licence and transform: **to be
  supplied by the architect after reading the terms**; the planner did not read any candidate's terms.

### 8.3 Registry key table

See §5.4. Only the three curriculum-listed keys are usable by default; `black1973pricing` after §7 Q4.

---

## 9. DAG problems (concepts natural FC2 content would use outside the closure)

The full table is §0.2. Summary:

- Outside the closure and needed: FC1 (six concepts), FI1 (five concepts, plus the name collision with `convexity`), SC1/SC2
  (Brownian motion, GBM, Itô), AP1 (law of one price, EMM, SDF), M6 (martingale, stopping time), M7 (convex function and set),
  M8 (root finders, Newton, floating point), DV1/DV4 (Greeks, delta hedging, early-exercise boundary).
- Each row has a resolution in §0.2: a recommended prerequisite (FC1, §7 Q2), plain prose, or a stated limitation (Black–Scholes,
  §7 Q3). No row blocks the lessons. The builders report each plain-prose use as a `DAG_DEFECT` line in the output contract.

---

## 10. Cards (Builder E, after A–D)

- `course/modules/FC/FC2/cards.json`: ids `FC2-c001` upward (`tools/check_pages.py` lines 366–398), `lesson` in
  `L01`–`L08`, each lesson with at least one card (the check "no cards for <lesson>").
- One atomic card per definition, key formula or theorem, and misconception (BUILDER_RULES §7). Each card tests one fact;
  no trivia.
- Grade **T** for every derived result (parity, bounds, convexity, one-period and multi-period binomial, the swap par identity,
  margining identity); set `basis` to the lab or the problem that establishes the numerical check (for example
  `"basis": "Lab 5, Problem 2 (exact)"`), per the E1 precedent.
- Grade **A–D** only for an empirical or attributed claim, and cite a registry key (`cite`). FC2 has few such claims. The only
  citable keys are §5.4's (with §7 Q4 for `black1973pricing`).
- `check_pages.py` checks the unit prefix, the lesson existence, the grades, the registry keys and the duplicates.

---

## 11. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

```bash
cd /Users/billyribeiro/dev/quant-phd
.venv/bin/python tools/check_pages.py --unit FC2            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit FC2
.venv/bin/python tools/check_projects.py --unit FC2
.venv/bin/python tools/run_labs.py --unit FC2               # --page L07 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/FC/FC2/L01.html          # per page, after twins are written
.venv/bin/python tools/embed_labs.py course/modules/FC/FC2/L07.html --refresh lab-FC2-L07-1   # after a twin edit
.venv/bin/python tools/run_graders.py --unit FC2 --seeds 0-49
.venv/bin/ruff check tests/labs/FC2 course/modules/FC/FC2/grader && .venv/bin/ruff format --check tests/labs/FC2 course/modules/FC/FC2/grader
.venv/bin/mypy tests/labs/FC2 course/modules/FC/FC2/grader   # strict; confirm the configured paths before running
```

Verifier only (not builders):

```bash
.venv/bin/python tools/mutate_graders.py --unit FC2 --seeds 0-9
.venv/bin/python tools/verify_refs.py --unit FC2
.venv/bin/python tools/page_smoke.py --unit FC2             # on a quiet machine
```

Flags, as read by the planner: `check_pages.py`, `check_dag.py`, `check_projects.py` take `--unit` (and `--all`);
`run_labs.py` takes `--unit`, `--all`, `--page` (`tools/run_labs.py` lines 119–121); `run_graders.py` takes `--unit`, `--all`,
`--seeds` (lines 129–131, default 0–49); `mutate_graders.py` takes `--unit`, `--all`, `--seeds` (lines 30–32, default 0–9);
`embed_labs.py` takes pages and `--refresh [LAB_ID ...]` (lines 130–131). The planner did not execute these commands.

Not run by builders: `page_smoke.py`, `check_pages.py --all`, `build_site.py --check`, `render_curriculum.py`. Repo-wide gates
are the architect's, once, before merge.

---

## 12. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** FC2 names none (§7 Q15). `check_projects.py` skips the contract check (line 144).
2. **No debate.** No `debate:` key (`curriculum/02-economics-finance-core.yaml:396-431`), so `check_pages.py` line 412 does not
   require a debate brief.
3. **Grading `both` on a tier-U module.** The rubric and exemplars are required (`check_projects.py` lines 58–71, 138–139).
4. **One curriculum lab, eight lessons.** The per-lesson labs are planner proposals (§7 Q11).
5. **Data.** The brief's embedded chain cannot be built as written (§7 B1).
6. **Lesson hub placement items.** The placement diagnostic needs two `data-skill` items on rung-1/2 skills (`check_pages.py`
   lines 351–353); the planner's list in §3 satisfies this.
7. **Closure.** The closure is `AC1, CF1, M1, M2, M4, P0.1` and omits FC1, so the FC1 concepts in §0.2 are unlinked (§7 Q2).
8. **Labs must be exact.** `Fraction` code for L01–L06; `math.erf` for L07 with a stated display precision.

---

## 13. After the builders

1. Orchestrator integrates; runs §11's commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01–L02, L03–L04, L05–L06, L07–L08, project (with ten mutants and the
   five alternative implementations, §5.5–§5.6), cards. Failing rows return to the owning builder only.
3. Ledger at `ledgers/FC2.verification.json`; verifier scripts archived under `ledgers/FC2/scripts/` (VERIFIER §3); mutants under
   `ledgers/FC2/mutants/`.
4. Merge only when the unit ledger is PASS, or its remaining gaps are named and agreed. A half-built FC2 is not merged, because
   `check_pages --all` checks built units.

---

## 14. Builder assignments (owner letters, fixed)

- **Builder A:** L01, L02, L03, hub (`index.html`).
- **Builder B:** L04, L05.
- **Builder C:** L06, L07, L08.
- **Builder D:** project page, grader (`instance.py`, `reference.py`, `starter.py`, `test_project.py`), mutants and alternative-implementation fixtures
  (verifier-only items stay with the verifier).
- **Builder E (after A–D):** `cards.json`.

Each builder writes only its own files and twins. No builder edits `curriculum/*.yaml`, `references/*.json`, `notation/notation.json`,
`MANIFEST.json` or any generated file; requests go in the output contract.

## Output contract reminder (BUILDER_RULES §10)

Each builder reports `UNIT: FC2`, the files written, `HOURS: lessons=<h> project=<h> total=<h> (curriculum=90)`, the self-check
lines with the exact output of each command it ran (not PASS for a check it did not run), and the `REFERENCE_REQUESTS`,
`NOTATION_REQUESTS`, `GLOSSARY_REQUESTS`, `DATA_REQUESTS`, `CONTRACT_CHANGE_REQUESTS`, `DAG_DEFECTS` and `KNOWN_LIMITATIONS` lines.
Known limitations the planner expects: Black–Scholes not derived (§7 Q3); the project chain is SIMULATED (§7 B1); the registry's
edition and volume fields are missing (§7 Q5); plain-prose terms outside the closure (§0.2).

## Architect decisions (2026-10-28, binding). Where the plan states a recommendation for an open question, follow it. Defaults for every module: concepts outside the prerequisite closure are plain prose with no link and no dfn; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields only or not at all (never edit a record, never type bibliographic data); no real data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST in plans/<UNIT>-open-items.md; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every grader; not adversarial, no question bank.
Module specifics: FC1 is added to FC2's prerequisites in the curriculum (done, regenerated); the option chain is SIMULATED with a bring-your-own-chain schema and a DATA_REQUEST; Black-Scholes is stated as a formula with the binomial agreement shown as a numerical observation; maturity is tau (never T); convexity in strike does not link FI1's convexity.
