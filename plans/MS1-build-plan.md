# MS1 build plan: Microstructure Theory (planner output, 2026-11-09)

Unit: **MS1 · Microstructure Theory** · tier M · 90 h · prerequisites E4 and S1 · no Atlas milestone · no debate key ·
grading `both` (autograder for the decomposition solver, rubric for the note) · output directory `course/modules/MS/MS1/`
(part code `MS`) · lab twins `tests/labs/MS1/` · ledger `ledgers/MS1.verification.json` (fragments `ledgers/MS1-<slice>.json`,
mutants `ledgers/MS1/mutants/`, alternatives `ledgers/MS1/alternatives/`, equivalents `ledgers/MS1/equivalent/`).

Planner: Haiku, plan only. This file is the only file written. No curriculum, registry, notation, course or git edits, no commit,
no push. Executors: Haiku builders A to E (lessons, hub, project, grader), F (cards), then independent Haiku verifiers
(VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every curriculum fact cites `file:line` read during planning. Tool facts cite the tool file and line.
Anything not in the curriculum is marked **NOT IN CURRICULUM**. The planner read no paper and typed no bibliographic data from
memory. Every formula in §3 and §5 is either a **planner derivation** (worked out by the planner in this file, to be re-derived
by the builder and re-checked by the verifier) or is left to the builder to derive. The planner ran `tools/coursekit.py`
(`prerequisite_closure`, `concept_owner`, `unit`, `built_units`) through `.venv/bin/python` and read the registry, notation
and data-source files. The planner ran no check tool (`check_pages`, `check_dag`, `run_labs`, `run_graders`).

**Status: no blocker for lesson writing. Two architect decisions block the project (B1, B2, §0.3). The hours are feasible (§0.2).**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part MS, code `MS`, order 16, title "Market Microstructure & Execution" | `curriculum/04-quant.yaml:413-415` |
| MS1 id and title "Microstructure Theory" | `curriculum/04-quant.yaml:430-431`; `curriculum/curriculum.json:10292` (`"id": "MS1"`) |
| Tier `M`, hours `90` | `curriculum/04-quant.yaml:432-433` |
| Prereqs `[E4, S1]` (only) | `curriculum/04-quant.yaml:434` |
| Core: "Roll's spread estimator, Kyle, Glosten–Milgrom, inventory models, PIN, the VPIN dispute." | `curriculum/04-quant.yaml:435-437` |
| `introduces` has **8** concepts, one per line: `roll-spread-estimator`, `kyle-model`, `kyles-lambda`, `glosten-milgrom-model`, `inventory-model`, `spread-decomposition`, `probability-of-informed-trading`, `vpin` | `curriculum/04-quant.yaml:438-446` |
| Sources: seven strings: Roll (1984), JF 39(4); Kyle (1985), Econometrica 53(6); Glosten & Milgrom (1985), JFE 14(1); Ho & Stoll (1981), JFE 9(1); Easley, Kiefer, O'Hara & Paperman (1996), JF 51(4); Easley, López de Prado & O'Hara (2012), RFS 25(5); Andersen & Bondarenko (2014), JFM 17 | `curriculum/04-quant.yaml:447-454` |
| Lab: "Kyle equilibrium." (the curriculum lab) | `curriculum/04-quant.yaml:455` |
| Project "Spread decomposition"; brief: "Implement Roll and Glosten–Milgrom-style decompositions on simulated and bring-your-own-data trades, and separate adverse selection from inventory and order-processing costs."; deliverable "Code plus note."; grading `both` | `curriculum/04-quant.yaml:456-463` (title 457, brief 458-461, deliverable 462, grading 463) |
| No `debate:` key on MS1 | `curriculum/04-quant.yaml:430-463` (absent) |
| No `atlas:` key on the MS1 project; no Atlas entry names MS1 (the 20 entries name CS1, CS3, S0, S4, FI1, DV4, F1, S7, QR2, MS3, PR2, PR4, FI3, CR1, AC2, CF4, QR3, GM1, SR3, GM4) | `curriculum/04-quant.yaml:456-463` (absent); `curriculum/curriculum.json` `atlas` array |
| Studio STUDIO-MS requires MS2 and MS3 (MS1 is not a studio requirement) | `curriculum/04-quant.yaml:416-419` |
| MS1 is a direct prerequisite of MS2 (`[MS1, CS2]`) and MS3 (`[MS1, SC6]`) | `curriculum/04-quant.yaml:468`, `:500` |
| Credentials that name MS1: MS-FIN requires it; MS-FIN course "Market Microstructure & Trading"; PHD-FIN requires it; PHD field course "Market Microstructure" | `curriculum/meta.yaml:98`, `:112`, `:124`, `:136` |
| Topological position of MS1 is index 48 (0-based) in the 134-entry list | `curriculum/curriculum.json` `topological_order` (planner read) |
| All 8 MS1 concepts map to module MS1 in `concepts` | `tools/coursekit.py` `concept_owner` (planner run) |
| Prerequisite closure of MS1 (planner run of `prerequisite_closure("MS1")`): **{CS1, E1, E2, E3, E4, M1, M2, M3, M4, M7, P0.1, S0, S1}**, 13 units; **168 usable concepts** in the closure | planner run output |
| Built units in the closure (planner run of `built_units`, which tests `course/modules/<PART>/<ID>/index.html`): E1, E2, E3, E4, M1, M2, M3, M4, M7. **Not built:** CS1, S0, S1, P0.1 | planner run output |
| Nearest built prerequisite: **E4** (direct prerequisite, built, `grading: both`, has `course/modules/E/E4/grader/`, plan `plans/E4-build-plan.md`, read in full by the planner) | `curriculum/02-economics-finance-core.yaml:124-154`; `course/modules/E/E4/grader/`; `plans/E4-build-plan.md` |
| S1 is a direct prerequisite and is tier F, 130 h, prereqs `[M4, S0]` | `curriculum/01-foundations.yaml:619-623` |
| Concept index `course/concepts.html` carries anchors for concepts of unbuilt modules (for example `bayesian-inference`, `maximum-likelihood-estimation`, `estimator`), so links to closure concepts resolve before S1 is built | `course/concepts.html` (planner grep) |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 90 h (`curriculum/04-quant.yaml:433`). Tool rules (planner-read locators; the builder re-reads them):

- lesson `data-hours` 6 to 12 (`tools/check_pages.py` `check_lesson`, line 219; hours read at line 221, rule at 225);
- hub `data-hours-lessons + data-hours-project = 90` (`tools/check_pages.py` `check_hub`, line 325; attributes read at lines 332-335);
- project share 10 to 40% of 90, i.e. 9 to 36 h;
- lessons sum to the hub's lessons figure.

**Chosen split: 8 lessons × 8 h = 64 h; project 26 h (28.9%).** 64 + 26 = 90. Feasible. The split follows the E4 precedent
(`plans/E4-build-plan.md` §0.2, 8 h lessons and a 28% project). **No STOP condition on hours.** The alternative 8 × 9 h and 18 h
(20%) is open question Q1.

### 0.3 Blocking and non-blocking issues

**B1 (architect; blocks the project's data, not the lessons). No redistributable trade-level data is embedded.**
- The brief asks for "simulated and bring-your-own-data trades" (`curriculum/04-quant.yaml:458-461`).
- The embedded snapshots are `fx_daily`, `fx_monthly` and `ust_daily` only (`course/assets/data/market/MANIFEST.json`;
  `tools/data_sources.yaml:19`, `:53`, `:91`). None is a trade or quote series.
- `tools/data_sources.yaml:119` `rejected:` lists the Kenneth French library and Open Source Asset Pricing only. Neither is a trade
  series, and both are refused for redistribution.
- No trade-level source appears in the registry as a dataset (the registry holds papers, not data).
- **Plan default:** every lab and the rung-1 and rung-2 instances use generated trades labelled **SIMULATED**. The project's
  bring-your-own-data mode accepts a student CSV that never leaves the browser (BUILDER_RULES §6.6, last bullet). No DATA_REQUEST
  names a source (the planner names none from memory). Decision in §12 Q3.

**B2 (architect; blocks the project's model, not the lessons). The curriculum names no model for the decomposition.**
- The brief names the two decompositions (Roll; Glosten–Milgrom-style) and the three components (adverse selection, inventory,
  order processing) (`curriculum/04-quant.yaml:458-461`). It names no model, estimator, interface or sign convention.
- **Plan default:** the one-asset repeated-trade model of §5.2 (planner proposal). Its population identities are planner
  derivations (§5.2) that the verifier re-derives. Decision in §12 Q4.

**B3 (non-blocking; the builder follows the default). Concepts outside the closure that natural MS1 content would use.**
- `bid-ask-spread` and `market-maker` belong to FC1 (`curriculum/02-economics-finance-core.yaml:377-378`; FC1 at `:363`).
- `poisson-process` belongs to SC5 (`curriculum/03-markets.yaml:625`; SC5 at `:616`, prereqs `[SC2]`).
- `martingale` belongs to M6 (`curriculum/01-foundations.yaml:281`; M6 at `:262`).
- `ols-estimator` belongs to S2 (`curriculum/01-foundations.yaml:671`; S2 at `:661`).
- Each is handled in §4 by plain prose (no link, no `data-concept`). Adding any of them as a prerequisite is a curriculum change for
  the architect (§12 Q5 to Q8).

**B4 (non-blocking). Registry records match the curriculum strings, with two notes.**
- All seven keys exist with `status: verified` and `used_by` including MS1 (§7.1). Authors match the curriculum strings
  (`references/references.json:592`, `:7505`, `:7554`, `:10453`, `:12566`, `:15282`, `:19991`).
- `kyle1985continuous` (`references/references.json:15282`) has `pages: "1315"` (start page only). The verifier checks the page
  range before any citation carries a range.
- `kyle1985continuous` has the title "Continuous Auctions and Insider Trading". The single-period model taught in L05 is not
  attributed to a section of the paper until the verifier reads the abstract (§2.2, §12 Q12).

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

8 lessons × 8 h = 64 h; project 26 h; total 90 h. Each of the eight concepts is defined in exactly one lesson, in the order
below, which is also the dependency order (every use of a concept is inside the closure or in an earlier lesson).

| Lesson | Title (working) | Concept it defines (`introduces`, `curriculum/04-quant.yaml:438-446`) | Lab twin id (`tests/labs/MS1/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Bid–ask bounce and Roll's spread estimator | `roll-spread-estimator` (`:439`) | `lab-MS1-L01-1`: a SIMULATED trade-price path with bounce; the Roll estimate against the true spread, printed with the sign of the lag-1 covariance | 8 | Builder A |
| L02 | Glosten–Milgrom quotes under asymmetric information | `glosten-milgrom-model` (`:442`) | `lab-MS1-L02-1`: the two-value model with exact `Fraction` posteriors; ask and bid after a stated trade sequence; the adverse-selection gap printed | 8 | Builder A |
| L03 | Inventory and the dealer's quote | `inventory-model` (`:443`) | `lab-MS1-L03-1`: the stated quadratic-penalty inventory model solved by backward induction on a finite grid, exact in `Fraction`; the optimal quote shift by inventory level (finite enumeration, grade C) | 8 | Builder B |
| L04 | Spread decomposition | `spread-decomposition` (`:444`) | `lab-MS1-L04-1`: the regression identities of §5.2 on a SIMULATED trade sample; the three components against their true values, with the identity checked | 8 | Builder B |
| L05 | Kyle's model of informed trading | `kyle-model` (`:440`) | `lab-MS1-L05-1` (**the curriculum lab**, `:455`): the linear equilibrium coefficients solved exactly in `Fraction` for stated parameters; the two equilibrium residuals printed as zero | 8 | Builder C |
| L06 | Kyle's lambda and price impact | `kyles-lambda` (`:441`) | `lab-MS1-L06-1`: a seeded SIMULATED Kyle sample; the regression slope against the population λ, with the standard error printed | 8 | Builder C |
| L07 | The probability of informed trading | `probability-of-informed-trading` (`:445`) | `lab-MS1-L07-1`: the day likelihood checked to sum to one over a truncated support; a grid maximum-likelihood estimate on SIMULATED counts | 8 | Builder D |
| L08 | VPIN and its dispute | `vpin` (`:446`) | `lab-MS1-L08-1`: volume-bucket VPIN on a SIMULATED path, with the bucket rule and the bounds printed | 8 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours 64/26 | none | none | - | Builder A (after L02 exists) |
| project | Spread decomposition (`both`), §5 | none | `lab-MS1-project-1` (rung 1), `lab-MS1-project-2` (rung 2, `class="lab completion"`), `lab-MS1-project-3` (rung 3 check) | 26 | Builder E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` | none | none | - | Builder E |
| cards | `cards.json` from L01 to L08 | none | none | - | Builder F (after A to E) |

**Ownership rule.** Each builder writes only its own lesson files and twins. Builder A writes the hub after L02 exists. Builder E
writes the project, its rubric, exemplars and grader, and does not depend on the lessons' prose. Builder F writes only
`cards.json`.

**Why four lesson builders at two lessons each.** The brief asks for about three lessons per builder. With five builders (A to E)
and the last one owning the project, four builders share eight lessons. Three builders at 3, 3, 2 would leave the fourth of A to D
without a lesson, and the eight concepts map one to one onto eight lessons, so no lesson can be dropped to make the spread
closer to three (§12 Q2). The E5 precedent (`plans/E5-build-plan.md` §1) uses the same 2, 2, 2, 2 split.

Ordering check (every use of a concept is inside the closure or an earlier lesson; `tools/check_dag.py` checks linked uses,
§4 covers unlinked ones):
- L01 uses M4 `random-variable`, `expectation` and the covariance of Definition 1.6 in `course/modules/M/M4/L04.html` (written with `\Cov`;
  no concept id, §4 D5). No out-of-closure concept.
- L02 uses E2 `adverse-selection`, `bayesian-nash-equilibrium` (contrast only), S1 `bayesian-inference` (Bayes' rule for the posterior),
  M4 `conditional-expectation-elementary`.
- L03 uses L02 `glosten-milgrom-model` (the quote-setting logic), M7 `bellman-equation` and `principle-of-optimality`.
- L04 uses L02 `glosten-milgrom-model` and L03 `inventory-model` (the components), L01 `roll-spread-estimator` (the total spread),
  M3 `least-squares-projection` (the regression identities).
- L05 uses E2 `bayesian-nash-equilibrium`, E4 `rational-expectations-equilibrium`, `noisy-rational-expectations-equilibrium`,
  `price-informativeness`, M4 `normal-distribution`, `conditional-expectation-elementary`, `multivariate-normal` (only if needed).
- L06 uses L05 `kyle-model`, M3 `least-squares-projection`, S1 `estimator`, `consistent-estimator`.
- L07 uses L02 `glosten-milgrom-model` (the arrival of informed trades), E2 `adverse-selection` (contrast), S1
  `maximum-likelihood-estimation`, `mle-asymptotic-normality` (prose only), and a plain Poisson distribution (§4 D3).
- L08 uses L07 `probability-of-informed-trading` (the model it extends), M4 `normal-distribution` (or `student-t-distribution`,
  whichever the builder uses for the bulk-volume rule, stated on the page).

Hours check: 8 × 8 = 64 (hub `data-hours-lessons="64"`); project 26 (hub `data-hours-project="26"`); total 90.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to MS1)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3 to §8, `VERIFIER_RULES.md` §2, `plans/FINAL-ARCHITECT-RULINGS.md`,
`/Users/billyribeiro/.fanout/fixer-rules.md`, this file, and `plans/E4-build-plan.md` (the nearest built prerequisite's plan, whose
precedents this plan adopts). Study `course/modules/E/E4/` (hub, lessons, project, grader panel, rubric) and
`course/modules/M/M1/` for layout. `course/templates/` holds the four skeletons. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier unit)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) or from floats
   stated to full precision, and rounded only at display. A page that shows a rounded figure states its rounding rule. Precedent:
   E4 §2.1 item 1, E5 §2.1 item 1. For MS1 this covers every spread, every covariance, every posterior, every λ and every PIN.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints; the interpretation names only what
   the printed numbers show. Every "checked", "verified" or "shown" claim names the lab, line or test that did it. Precedent:
   M1 LESSON_TEXT_DEFECTS.
3. **Attribute nothing unread.** Cite only the registry keys in §7.1, and only at the level of the registry title unless the builder
   has read the abstract. No locator, page, table, equation number, coefficient or date is typed unless read. A result from a source
   not read is a derivation on the page (grade T, conditional on its assumptions) or is named "not stated here". Precedent: E4
   §2.1 item 3; the fixer rule "Attribute nothing you have not read".
4. **Scope words need a computation, a witness or an explicit hypothesis.** "every", "all", "never", "always", "any", "only", "same",
   "drives", "exactly", "in general", "market structures", "welfare", "the spread is" are used only where a derivation, a finite check
   or a lab computes the claim. MS1 scope (confirm, §12 Q17): one risky asset; one-period models (L02, L05, L06) and a repeated
   trade model with i.i.d. signs (L01, L04, the project); the dealer's inventory model is the stated quadratic model of L03; the
   Kyle model is the single-period linear model; no continuous-time model; no multi-asset or multi-venue claim; no claim about the
   level of spreads in any market.
5. **Define before use.** Each of the eight concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned lesson,
   and never before it. Terms outside the eight (bid–ask spread, half-spread, order-processing cost, signed trade, efficient price,
   bid–ask bounce, market maker, volume bucket, bulk-volume classification, Poisson distribution, noise trader, informed trader,
   the lag-1 covariance of price changes) are defined in prose at first use with a plain `<dfn>` and no `data-concept`
   (`tools/check_dag.py` skips a `<dfn>` without `data-concept`, per E4 §2.1 item 5). A plain `<dfn>` never repeats an FC1, FC3,
   M6, SC5 or S2 concept id (§4).
6. **Propositions state every hypothesis, numbered.** Every Theorem, Proposition, Lemma and Derivation lists numbered Assumptions
   (A1, A2, …) before its statement, and its proof cites them by number. Examples the builders must state: the Roll derivation needs
   A1 (efficient-price increments i.i.d., mean zero, variance σ²) and A2 (signs i.i.d. uniform on {−1, +1}, independent of the
   efficient price), A3 (constant half-spread, transaction price equal to efficient price plus half-spread times sign), A4 (no
   price impact); the Glosten–Milgrom quote needs finitely many values, two trader types and zero expected profit for the
   market maker; the Kyle equilibrium needs a linear strategy and zero expected profit (a numbered assumption, not a theorem about all
   equilibria); the PIN likelihood needs the three-day-type arrival model stated as assumptions.
7. **Grader rule.** Applies to the project grader (§5.4). A test may demand an exception type only for a condition the page names
   (§5.4 table). Every other invalid input may raise any exception or return.
8. **Money.** MS1 has no money output. Spreads, prices and components are floats in price units or exact rationals; each carries its
   rounding rule. If a currency unit is introduced, it is integer cents, rounded once, half up, stated on the page (fixer rule).
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own container;
   no element widens the page past 360 px. `page_smoke.py` is the verifier's check; builders do not run it.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":`
    guard. `tools/run_labs.py` runs each twin as `python -I -W error <twin>` with no network. Precedent: M1 `tests/labs/M1/lab-M1-L04-1.py`.
11. **Lab hypotheses before runs.** Each lab's `p.hypothesis` states the expected result before the expected-output block is embedded.
    Every RNG is seeded with `random.Random(seed)`. Standard library only (`fractions`, `math`, `random`, `itertools`, `statistics`
    allowed); no NumPy or SciPy in labs; under 10 s in Pyodide.
12. **Bisection and search are stated, not assumed.** The grid maximum-likelihood search in L07 and any root-finding state the grid,
    the bracket, the tolerance and the stop rule. Precedent: E4 §2.1 item 12.
13. **Graded-instantly completion problem.** The rung-2 completion lab (`class="lab completion"`) shows `___` blanks. Every page line equals
    its twin line or contains a blank (`tools/run_labs.py` completion rule).
14. **Architect rulings apply.** Ruling 1: use the macro `\R`, never `\mathbb{R}`. Ruling 2: card ids need not be sequential. Ruling 9:
    a mutant that survives and violates a stated behaviour gets a new test; one that differs only where the page states nothing goes to
    `ledgers/MS1/equivalent/` with a README proof. Ruling 10: five correct alternatives must pass seeds 0 to 49 (§5.5). Ruling 19 of
    `/Users/billyribeiro/.fanout/fixer-rules.md`: a test demands an exception only for a condition the page names. Ruling 23: blind
    exemplar scoring is done by a dedicated scorer. HOURS ruling: declared hours are design targets. LAB MUTANTS ruling: lab twins are
    demonstrations; mutation testing applies to the project grader only.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- **Evidence.** Every claim carries a grade (T, A, B, C, D or X, BLUEPRINT §3) and a registry key or a derivation. A B- or C-graded claim
  names its published counter-evidence (BUILDER_RULES §2.5). A claim about what a paper shows is made only at the level of its
  registry title, unless the verifier has read its abstract (§7.1). Empirical statements about spreads, price impact, PIN or VPIN
  performance are C at most with a basis named, or are removed (§7.2).
- **Attribution of the models.** Roll, Glosten–Milgrom, Ho–Stoll, Kyle, Easley et al. (1996) and Easley et al. (2012) are cited for their
  models at title level (§7.1). The builder teaches each model as a stated model with its derivation on the page. Where a page says
  "this model is due to", it names the registry key and nothing more.
- **Concept links.** Closure concepts (E1, E2, E4, M1 to M4, M7, S1, CS1, S0, P0.1): `<a class="concept" data-concept="<id>"
  href="../../../concepts.html#<id>">`. Earlier MS1 lessons: `href="Lnn.html#def-<id>"`. A lesson never links a concept defined in a later
  lesson. There is no link to an E4, S1 or CS1 hub page; the convention links to `concepts.html` anchors (BUILDER_RULES §4.1).
- **Labs.** Code lives once in `tests/labs/MS1/lab-MS1-Lnn-1.py` (and `lab-MS1-project-1..3.py`). The page carries `@@LAB:<file>@@` and
  `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-MS1-<page>-<n>`
  (`tools/check_pages.py` lab-id rule). Lab ids are numbered in display order.
- **SIMULATED label.** Required on any lab, figure, grader instance or exemplar that uses generated trades or seeded draws (L01, L04, L06,
  L07, L08, the project's rung-1 and rung-2 instances, `instance.py`, the rung-3 check, the exemplars). Exact population computations
  (L02, L03, L05) are not labelled SIMULATED.
- **Never hand-edit generated files**: `CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `notation/notation.json`, `MANIFEST.json`. Request changes in the output contract.
- **Learner-visible text.** No process words in the page (build, builder, round, verifier, REQUESTS, unit report) and no planning
  references in code comments.
- **Banned strings** (`tools/check_pages.py` lines 58 onward, `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the
  scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
  "obviously", "clearly", and any ellipsis `...` outside code.
- **Percent changes** state the base and the direction. **Growth or return rates** state their convention. **Correlations** state the
  sample or the population. **Spreads** state the units (price units, or basis points with the base price).
- **A finite enumeration is grade C with its basis named**, not grade T (M1 L06 precedent). Used in L03 and in any grid search.
- **Hub lesson titles** match each lesson's `<h1>` at integration. **Quiz explanations** are read against their lesson.
- **No `git commit`, no push.** The builder reports files written, commands run with exact output, and every gap in the BUILDER_RULES
  §10 output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered items MS1 must use or must not reuse (`notation/notation.json`):

| Registered item | Registered meaning (locator) | MS1 rule |
|---|---|---|
| `\E` (macro) | expectation operator (`notation.json:5-8`) | Use the macro for every expectation. Never write raw `\mathbb{E}`. |
| `\Var`, `\Cov`, `\Corr` (macros) | variance, covariance, correlation (`notation.json:13-24`) | Use `\Cov` for the lag-1 covariance and the covariance of the Kyle model. |
| `\R` (macro) | real numbers (`notation.json:25-28`) | **Use `\R` (architect ruling 1).** |
| `\Normal` (macro) | normal distribution (`notation.json:37-40`) | Use for every normal law. |
| `\indic` (macro) | indicator function (`notation.json:33-36`) | Use for indicators of trade signs or of states. |
| `\argmax`, `\argmin` (macros) | argmax and argmin (`notation.json:53-60`) | Use if an argmax is written (L07 grid search). |
| `T` | number of return observations (`notation.json:112`, module S1) | **Never used.** The number of trades is `n`; the time index is `t`. A horizon is written `H` only if needed and then defined. |
| `\Phi`, `\Phi^{-1}` | standard normal CDF and its inverse (`notation.json:117`, M4) | Used only with that meaning (for example, a bulk-volume rule that uses the normal CDF). |
| `\gamma_3`, `\gamma_4` | skewness and kurtosis (`notation.json:122`, `:127`, M4) | **Not used.** Plain `\gamma` is not used either (it is free, but the risk-aversion letter of L03 is `a`). |
| `R^\ast`, `R^{e\ast}`, `R_f` | SDF return, projection of 1, gross riskless return (`notation.json:132`, `:137`, `:142`, AP1) | **Not used.** |
| `\mathbb{Q}` | equivalent martingale measure (`notation.json:147`, AP1) | **Not used.** Do not write `Q` for a measure; `q_t` is the trade sign. |

Local symbols (each defined on the lesson where it first appears and never redefined within MS1):

- `n` the number of trades (never `T`); `t` the trade index; `m_t` the efficient price; `p_t` the transaction price; `d_t` the price
  change `p_t − p_{t−1}`; `q_t` the signed trade (±1, buy +1); `c` the order-processing half-spread; `s` the Roll spread;
  `sigma`, `sigma_u` standard deviations (write `\sigma`, `\sigma_u`); `eta_t` the efficient-price shock.
- `\lambda` is **Kyle's lambda** (price response to order flow, L05 and L06) only. The project and L04 use **`\theta`** for the
  per-trade adverse-selection price impact. `\lambda` and `\theta` are different objects (volume-based and sign-based) and the pages
  say so once, in L06 and in the project spec.
- `I_t` inventory (never `q`, which is the trade sign); `a` the risk-aversion coefficient in L03.
- PIN parameters: `\alpha` (probability of an information event), `\delta` (probability that the event is bad news), `\mu` (informed
  arrival rate), `\varepsilon_b`, `\varepsilon_s` (uninformed buy and sell arrival rates). `\mu` is not used for a mean in MS1.
- VPIN: bucket volume `V`, buy and sell bucket volumes `V^{B}`, `V^{S}`; `\pi` is not used (it reads as the number 3.14 in some pages).

NOTATION_REQUESTS: **none.** The plan uses only local symbols and the registered macros above.

---

## 3. Lesson content plan (what each lesson must establish; the builder decides the argument)

For each lesson the builder writes the BUILDER_RULES §4.2 structure in order: why it matters (at most 120 words), numbered core sections
of Definition, Theorem, Proof, Example and Remark blocks, the inline lab (before "where the canon breaks"), where the canon breaks (at
least one model limit and what changes without it), misconceptions (at least 3), problem set (at least 3 each in Mechanics, Proof,
Empirical and Research, each with a `<details class="solution">`), key-results table (claim, grade, keys), quiz (8 to 15 items, each
with an explanation), and a `<ol data-references>` of registry keys. **No debate brief**: MS1 has no `debate` key (§0.1).

Planner derivations (for the builder to re-derive and the verifier to re-check; these are not text for the lesson):

- **PD1 (repeated-trade model).** Signs `q_t` i.i.d. uniform on {−1, +1}; efficient price `m_t = m_{t−1} + θ q_t + η_t` with `η_t` i.i.d.
  mean zero, variance σ², independent of the signs; transaction price `p_t = m_t + c q_t`; `c > 0`, `θ ≥ 0`. Then
  `d_t = (θ + c) q_t − c q_{t−1} + η_t`.
- **PD2 (covariance).** `E[d_t] = 0`; `Cov(d_t, d_{t−1}) = −c(θ + c)`. Under `θ = 0` this is `−c²`, which gives the Roll spread
  `2√(−Cov) = 2c`.
- **PD3 (regression identities).** `E[d_t q_t] = θ + c`; `E[d_t q_{t−1}] = −c`; the population regressors `q_t`, `q_{t−1}` are
  uncorrelated with unit variance. The population least-squares coefficients on (`q_t`, `q_{t−1}`) are therefore `b0 = θ + c` and
  `b1 = −c`.
- **PD4 (effective half-spread).** `E[q_t (p_t − m_{t−1})] = θ + c`. So the effective half-spread `H = c + θ` is the average signed
  distance from the pre-trade efficient price, and `b0 = H`.

The lesson content:

- **L01 `roll-spread-estimator`.** The bid–ask bounce (plain term): trade prices alternate between the bid and the ask, so price changes
  are negatively autocorrelated. The model of PD1 with `θ = 0` (A1 to A4). Theorem (T under A1 to A4): `Cov(d_t, d_{t−1}) = −c²`, so
  `s = 2√(−Cov)` recovers the spread `2c`. Lag-1 covariance is the M4 covariance (`\Cov`, M4 L04 Definition 1.6). Registry key
  `roll1984simple` at title level only ("A Simple Implicit Measure of the Effective Bid-Ask Spread in an Efficient Market"). The
  lab: SIMULATED, prints the estimate, the true `2c` and the sample covariance sign. Where the canon breaks: with `θ > 0` the
  estimator is not `2c` (PD2), and the lesson states the value `2√(c(θ+c))`. Any empirical use of the estimator is grade C with the
  counter-evidence lead R-MS1-1 (§7.2) named as not yet admitted.
- **L02 `glosten-milgrom-model`.** Two values `v_L < v_H` with a prior; a market maker who sets ask and bid equal to the expected
  value conditional on a buy and on a sell; a fraction of informed traders who buy when the value is high. The posterior is Bayes' rule
  (S1 `bayesian-inference`). Derivation (T under A1 to A4: finite values, two trader types, zero expected profit, one trade per period):
  the ask and the bid in closed form. The lab is exact in `Fraction`: the posterior and the quotes after a stated sequence of trades.
  The lesson states that the expected posterior equals the prior (the law of iterated expectations, M4
  `conditional-expectation-elementary`) without the word "martingale" (§4 D2). Registry key `glosten1985bid` at title level only
  ("Bid, ask and transaction prices in a specialist market with heterogeneously informed traders"). Where the canon breaks: a single
  period, no inventory, no competition beyond zero profit. Empirical claims: C with lead R-MS1-4.
- **L03 `inventory-model`.** A dealer's inventory `I_t` with a quadratic penalty in terminal and running inventory, and a quote
  shift that depends on `I_t`. **The model is the lesson's stated model with a quadratic penalty; it is not claimed to be the
  specification of Ho and Stoll (1981).** The Bellman recursion (M7 `bellman-equation`, `principle-of-optimality`) is derived (T under the
  stated assumptions). The lab solves the recursion on a finite inventory grid by backward induction in exact `Fraction`
  arithmetic, and prints the quote shift per inventory level. The grid solution is a finite enumeration (grade C with its basis). Registry
  key `ho1981optimal` at title level only ("Optimal dealer pricing under transactions and return uncertainty"). Where the canon
  breaks: no risk aversion of the Ho–Stoll type, no return uncertainty, no competition.
- **L04 `spread-decomposition`.** The half-spread splits into order processing `c` and adverse selection `θ`, with `H = c + θ`
  (PD4). Regression identities (PD3): `b0 = H`, `c = −b1`, `θ = b0 + b1`. Theorem (T in the model; A1 to A4 of L01 plus the model's
  constant `c`, `θ`): the components are identified from the transaction prices and the signs. Inventory is absent from this model (the
  decomposition's inventory term is zero by construction, and the lesson says so). The lab: a SIMULATED sample, the three components against
  the true values, and the identity `H = c + θ` checked to rounding. Where the canon breaks: constant `c` and `θ`, i.i.d. signs, no
  inventory, no time variation. Any claim about the size of a real spread component is C with lead R-MS1-3 named.
- **L05 `kyle-model`.** One risky asset with value `v ~ \Normal(p_0, \Sigma_0)`; noise traders with order `u ~ \Normal(0, \sigma_u^2)`
  independent of `v`; an informed trader with a linear order `x = \beta (v - p_0)`; a competitive market maker whose price is the
  conditional expectation of `v` given total order flow `x + u`, a linear map. **The builder derives the equilibrium coefficients
  (the informed trader's `\beta` and the market maker's price slope) and checks zero expected profit.** The result is T under the
  linear-strategy and zero-profit assumptions (A1 to A5, numbered). The lesson states that it is a linear-equilibrium result in the
  linear family, not an existence theorem. Concepts used: E2 `bayesian-nash-equilibrium`, E4 `rational-expectations-equilibrium`,
  `noisy-rational-expectations-equilibrium`, `price-informativeness`, M4 `normal-distribution`, `conditional-expectation-elementary`.
  Registry key `kyle1985continuous` at title level only ("Continuous Auctions and Insider Trading"). The lesson does not attribute
  the single-period version to a section of the paper until the verifier reads the abstract (§12 Q12). **The curriculum lab
  (`lab-MS1-L05-1`, `curriculum/04-quant.yaml:455`) is here:** the coefficients solved exactly in `Fraction` for stated parameters,
  with the two equilibrium residuals printed. Where the canon breaks: a single period, a linear informed strategy, one asset, noise
  traders with a normal law.
- **L06 `kyles-lambda`.** `\lambda` is the slope of the price on total order flow, `p - p_0 = \lambda (x + u)` in the L05 equilibrium. The
  identity `\lambda = \Cov(p, x + u) / \Var(x + u)` is T in the model. The regression slope estimates `\lambda`; the least-squares
  projection is M3 `least-squares-projection` (linked); the OLS formula is written inline (§4 D4). The derived closed form for `\lambda` in
  terms of the L05 parameters is a builder derivation, checked by the lab. The lesson states that `\lambda` (volume) and `\theta` (sign)
  are different objects. The lab: a seeded SIMULATED Kyle sample, the regression slope with its standard error, and the population `\lambda`
  printed. Empirical price-impact claims are C with lead R-MS1-3 named. Where the canon breaks: the linear model, one period, no
  temporary impact.
- **L07 `probability-of-informed-trading`.** The arrival model: on each trading day an information event occurs with probability `\alpha`;
  given an event, the news is bad with probability `\delta`; informed traders arrive at rate `\mu`; uninformed buys and sells arrive at
  rates `\varepsilon_b` and `\varepsilon_s`; arrivals are independent Poisson counts (the Poisson distribution is a plain `<dfn>`, §4 D3).
  The day's buy and sell counts `(B, S)` are the data. **The builder derives the day likelihood as a mixture over the three day types
  (no event; good news; bad news) from the arrival model, and checks it in the lab: the day likelihood sums to one over a truncated
  support, with the truncation and tolerance printed.** PIN is defined as `\alpha \mu / (\alpha \mu + \varepsilon_b + \varepsilon_s)`
  (the lesson's definition, written after the builder checks it against the paper at title level, `easley1996liquidity`, "Liquidity,
  Information, and Infrequently Traded Stocks"). Estimation by maximum likelihood (S1 `maximum-likelihood-estimation` linked). The lab
  runs a grid search on SIMULATED counts, with the grid, the stop rule and the resolution printed. Where the canon breaks: independent
  Poisson arrivals within a day, no intraday pattern, no time-varying parameters; the identification of `(\alpha, \delta, \mu,
  \varepsilon_b, \varepsilon_s)` from the counts is a stated limit (grade C, lead R-MS1-2 for critiques).
- **L08 `vpin`.** Volume-synchronised probability of informed trading: the trade stream is cut into buckets of fixed volume `V`; each
  bucket's volume is split into buy and sell volumes by a bulk-volume rule stated on the page (the builder names the rule and its normal
  or Student-t CDF, both in the closure via M4 `normal-distribution`, `student-t-distribution`). VPIN is the average over buckets of
  `|V^{S} - V^{B}| / V`. Theorem (T): VPIN lies in `[0, 1]`. Registry keys: `easley2012flow` at title level ("Flow Toxicity and
  Liquidity in a High-frequency World") for the measure, and `andersen2014vpin` at title level ("VPIN and the flash crash") for the
  published dispute. The two-sided treatment requires the verifier to read both abstracts before the lesson summarises either finding;
  until then the lesson states only that the two papers examine VPIN and that the second examines it around the flash crash. The lab:
  SIMULATED path, bucket volume and rule printed, VPIN values printed. Where the canon breaks: bucket size, classification error, and
  VPIN is a volume-weighted imbalance, not a probability of informed trading.

Lesson-level constraint: no lesson uses an MS2 term (limit-order-book dynamics, queue position, Regulation NMS, dark pools, payment for
order flow, frequent batch auction) or an MS3 term (square-root impact law, Almgren–Chriss, Obizhaeva–Wang, implementation shortfall).
Those are outside MS1 (§4 D10). "Price impact" in L06 means Kyle's `\lambda`, defined in the lesson.

---

## 4. DAG problems (concepts that natural MS1 content would use outside the closure)

Closure of MS1 (planner run, §0.1): {CS1, E1, E2, E3, E4, M1, M2, M3, M4, M7, P0.1, S0, S1}, 168 usable concepts. Owners below are from
`curriculum/curriculum.json` `concepts` (planner check with `concept_owner`). Topological positions from `topological_order`.

| Ref | Concept or term | Owner (outside closure) | Where natural MS1 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `bid-ask-spread`, `market-maker` (FC1; `curriculum/02-economics-finance-core.yaml:377-378`; FC1 at `:363`; topological 26) | FC1 | the spread in L01 to L04; the dealer in L02 and L03 | Plain `<dfn>` for "bid–ask spread" and "market maker" in L01 and L02. No link and no `data-concept`. The page does not repeat FC1's definition as a concept. §12 Q5 (alternative: add FC1 as a prerequisite; a curriculum change). |
| D2 | `martingale` (M6; `curriculum/01-foundations.yaml:281`; M6 at `:262`; topological 20) | M6 | the efficient price and the expected posterior in L02 | Not used. The word "martingale" never appears. The expected posterior is equal to the prior by the law of iterated expectations (M4 `conditional-expectation-elementary`, linked). §12 Q6. |
| D3 | `poisson-process` (SC5; `curriculum/03-markets.yaml:625`; SC5 at `:616`, prereqs `[SC2]`; topological 67) and the Poisson distribution (no concept id) | SC5 | arrival counts in L07 and L08 | Plain `<dfn>` "Poisson distribution" in L07 with its pmf stated. No link to SC5. §12 Q7 (alternative: add SC5 as a prerequisite; because SC5 sits after MS1 in topological order, that is a curriculum change with ordering consequences). |
| D4 | `ols-estimator` (S2; `curriculum/01-foundations.yaml:671`; S2 at `:661`) | S2 | the regression slope in L04 and L06 | The projection is linked to M3 `least-squares-projection` (`curriculum/01-foundations.yaml:173`). The OLS formula is written inline as the normal equations with a plain `<dfn>` "least-squares slope". No S2 link. §12 Q8. |
| D5 | scalar covariance (no concept id; M4 L04 Definition 1.6, `course/modules/M/M4/L04.html:98`) | M4 (no id) | the lag-1 covariance in L01 and the Kyle covariance in L05 and L06 | Written with `\Cov` and its formula; no concept link because M4 defines it with no `data-concept`. Not a DAG defect. |
| D6 | `dynamic-programming` (CS2; `curriculum/01-foundations.yaml:417`; topological 7) | CS2 | the inventory recursion in L03 | Not used. The recursion is the Bellman equation (M7 `bellman-equation`, `curriculum/01-foundations.yaml:317`, linked). |
| D7 | `kalman-filter` (S3) and `brownian-motion` (SC1) | S3, SC1 | the dynamic Kyle model (continuous time) and filtering | Not used. L05 is single-period; posteriors are normal conditionals (M4). The lesson says that continuous-time versions are not taught. |
| D8 | `order-book-data-structure` (CS2), `limit-order-book`, `order-types` (FC1), `lob-dynamics`, `queue-position` (MS2; `curriculum/04-quant.yaml:472-473`) | CS2, FC1, MS2 | L01 to L04 when describing the venue | Plain prose "limit orders" with no link. The queue and LOB dynamics are MS2 and are not used. |
| D9 | `efficient-markets-hypothesis` (FC3; topological 42) and "informationally efficient" | FC3 | the phrase "efficient price" in L01 and L02 | Plain `<dfn>` "efficient price" (the unobserved value) with no link. The phrase "efficient market" appears only as the registry title of `roll1984simple`. |
| D10 | `square-root-impact-law`, `efficient-execution-frontier`, `implementation-shortfall` (MS3; `curriculum/04-quant.yaml:503-508`; MS3 after MS1) | MS3 | price impact (L06) | Not used. Price impact in MS1 is Kyle's `\lambda` and the project's `\theta`, both defined in MS1. |
| D11 | `tick-data` (QR1; topological 27) | QR1 | the trade data in L01, L04 and the project's BYOD mode | Plain prose "trade-level data" with no link. |
| D12 | `bayesian-inference` (S1), `maximum-likelihood-estimation` (S1), `estimator`, `consistent-estimator` (S1) | S1 (in closure) | L02, L06, L07 | **Not a DAG issue.** S1 is a direct prerequisite (in closure), so these are linked. S1 is not built, so the links go to `concepts.html` anchors only, which exist (§0.1). |
| D13 | `adverse-selection`, `bayesian-nash-equilibrium`, `nash-equilibrium` (E2), `rational-expectations-equilibrium`, `noisy-rational-expectations-equilibrium`, `price-informativeness` (E4) | E2, E4 (in closure) | L02, L05, L06 | **Not a DAG issue.** Linked. |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Rows D1 to D4 need the architect's confirmation (§12 Q5 to Q8).**
`tools/check_dag.py` checks linked uses only (`tools/check_dag.py` docstring); an unlinked use of D1 to D11 passes the tool, so the
verifier reads every lesson and the project for these names (VERIFIER §2.9).

---

## 5. Project (`project.html`, Builder E): ladder, spec, model, grader, rubric

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py` requires the order)

1. **Rung 1, worked example** (`lab-MS1-project-1`, SIMULATED): one fully solved, annotated run of the solver on one generated instance,
   with a "why" note on each step: the price changes, the lag-1 covariance, the Roll spread, the regression normal equations, the three
   components, the adverse share. From tier M upward, rungs 1 and 2 are kept to the minimum (BUILDER_RULES §5.1).
2. **Rung 2, completion** (`lab-MS1-project-2`, `class="lab completion"`, SIMULATED): the line that gives the order-processing component
   from the regression slope (`order_processing = ___`) is removed. Graded instantly. Its twin is the completed solution; every page line equals
   the twin line or contains a blank.
3. **Rung 3, independent project (graded):** (a) the autograded solver `decompose.py` to the §5.2 interface, and (b) the note
   `report.md`, rubric-graded (§5.6). `lab-MS1-project-3` is the rung-3 check: it runs the reference computation on the report's stated
   grid (θ in {0, 0.1, 0.2}, c = 0.1, σ = 0.05, n = 2000, seed 1) and prints the table the note must reproduce.
4. **Rung 4, stretch** (optional, not graded): misclassified signs. Each sign is flipped with a stated probability; the student states
   how the Roll estimate and the regression slope change, as a hypothesis before the run.

### 5.2 Spec (`dl.spec`; `tools/check_projects.py` requires the terms and both grading words, lines 38 and 144-146)

Terms: Context (2 to 4 sentences), Inputs, Required outputs, Constraints, Grading, Reading list.

- **Context.** A dealer quotes a stock. Some trades carry information, so the price moves against the dealer after a trade, and
  some of the spread pays for processing the order. The question is how much of a measured spread is order processing and how much is
  adverse selection, and whether the Roll estimator recovers the spread. The note must answer that with the numbers from the solver.
- **Inputs.** (1) A SIMULATED instance from `make_instance(seed)` (`grader/instance.py`), used by the grader and the labs. (2) A
  bring-your-own-data trade file in CSV, columns `time,price,sign`, with `sign` equal to `-1` or `+1` and a rule for the sign stated in
  the note. The schema is documented on the page and validated in the browser; the file never leaves the browser (BUILDER_RULES §6.6).
  No embedded dataset is used (§6, B1).
- **Model (planner proposal, B2, §12 Q4; planner derivations PD1 to PD4 of §3).** Signs `q_t` i.i.d. uniform on {−1, +1}; efficient price
  `m_t = m_{t−1} + θ q_t + η_t`, with `η_t` i.i.d. normal with mean zero and standard deviation `sigma` (independent of the signs); transaction
  price `p_t = m_t + c q_t`, with `c > 0` and `θ ≥ 0`. The planner has derived the population identities: `Cov(d_t, d_{t−1}) = −c(θ + c)`;
  `b0 = θ + c`; `b1 = −c`; the Roll population value `2√(c(θ + c))`. **The builder re-derives them; the verifier re-derives them
  independently.** No registry key is cited for the model (its attribution is the lesson's and the reading list's concern, §7.2 R-MS1-3).
- **Required outputs.**
  - `decompose.py` with the frozen interface `decompose_trades(prices: list[float], signs: list[int]) -> dict[str, float]`, returning
    exactly the keys:
    - `roll_spread`: `2√(−cov1)` when `cov1 < 0`, otherwise `float("nan")`. Here `d_t = p_t − p_{t−1}` for `t = 2..n`, `mu_d` is the mean of
      the `n − 1` changes, and `cov1 = (1/(n − 2)) Σ_{t=3}^{n} (d_t − mu_d)(d_{t−1} − mu_d)`.
    - `half_spread`: `b0`, the first coefficient of the no-intercept least-squares fit of `d_t` on `(q_t, q_{t−1})` for `t = 2..n`.
    - `order_processing`: `c = −b1`.
    - `adverse_selection`: `θ = b0 + b1`.
    - `adverse_share`: `adverse_selection / half_spread`, and `float("nan")` when `half_spread` equals 0.
  - `report.md`, with the sections named in the rubric (§5.6).
- **Exception table** (the only conditions the grader may demand an exception for; the page names each):

  | Condition the page names | Exception | Message must name |
  |---|---|---|
  | fewer than three trades (`len(prices) < 3`) | `ValueError` | "at least three trades are needed" |
  | a sign not equal to `-1` or `+1` | `ValueError` | "each sign must be -1 or +1" |
  | all signs equal (the regression's normal equations are singular) | `ValueError` | "signs must vary: the regression is singular" |

  The two `nan` rules are returned values, not exceptions, and the tests may demand them. Any other invalid input may raise any
  exception or return.
- **Constraints.** Floats at full precision inside the solver; the note displays a stated number of significant digits and states the
  rule. Standard library only (`math`, `statistics`, `fractions`); no network; the same code runs in Pyodide and under pytest. The
  estimator has no intercept (the convention is stated on the page; a student who adds one changes the answer). Lists are not mutated.
- **Grading.** Autograder (`grader/test_project.py`, dual-mode) for `decompose.py`; rubric (`rubric-memo`, §5.6) for `report.md`. The
  spec names both "autograder" and "rubric" (`tools/check_projects.py` `GRADING_WORDS`, line 38).
- **Reading list.** `ol.reading-list` cites `roll1984simple`, `glosten1985bid`, `ho1981optimal`, `kyle1985continuous`, `easley1996liquidity`,
  `easley2012flow` and `andersen2014vpin` at title level (registry keys, §7.1). Nothing else.

### 5.3 Instance generator and validity (`grader/instance.py`, Builder E)

- `make_instance(seed: int) -> dict[str, object]`. Deterministic: `random.Random(seed)` only. Returns `prices` (list of floats), `signs`
  (list of ints), `n`, and the true `theta`, `c` and `sigma`. The docstring says **SIMULATED**.
- Parameter ranges (builder fixes exact values, states them on the page): `n` between 400 and 2000; `theta` between 0 and 0.5 (inclusive of
  0); `c` between 0.05 and 0.5; `sigma` between 0.01 and 0.1; the starting efficient price 100.0.
- Validity per seed: every price finite; every sign in {−1, +1}; the signs are not all equal (so the regression is defined); `n ≥ 3`;
  parameters inside the documented ranges.
- Distinctness: `tools/run_graders.py` `check_instances` (lines 79 to 105) requires that no two of the first 20 seeds produce identical
  instances, and that `make_instance` is deterministic.
- Seeds 0 to 49 must include at least one instance with `theta = 0` (for the Roll identity test) and at least one whose Roll estimate is
  undefined under the rule (if the seeds include none, the NaN test uses a constructed price list).

### 5.4 Grader (`course/modules/MS/MS1/grader/`, Builder E)

**Files:** `instance.py`, `reference.py` (the full solution; excluded from deployment, BLUEPRINT §7), `starter.py` (stubs that raise
`NotImplementedError`; the suite must fail on it), `test_project.py`. No Atlas path.

**Grader panel** on `project.html`: `<section class="grader-panel" id="grader" data-unit="MS1" data-grader="grader/"
data-suite="test_project.py" data-support="instance.py" data-solution="decompose.py" data-starter="starter.py"></section>`.
`data-packages` is empty (standard library only). `tools/run_graders.py` reads these attributes (`panel()`, line 43).

**Tests** (`test_project.py`). Each test recomputes its expectation from the instance's parameters or from prices with an oracle written
separately from `reference.py`.
- Exception tests, each condition in both directions: `len = 2` raises and `len = 3` is accepted; a sign of `0` and a sign of `2` raise
  and `-1` and `+1` are accepted; all signs equal raises and mixed signs are accepted.
- NaN rules: `cov1` exactly 0 gives `roll_spread` NaN; a price list with `cov1` slightly below 0 gives a finite value; `half_spread` 0 gives
  `adverse_share` NaN (constructed input).
- Oracle agreement: each of the five outputs equals the oracle to `1e-9` relative (`1e-9 * max(1, |expected|)`).
- Identity: `half_spread == order_processing + adverse_selection` to `1e-12 * max(1, |half_spread|)`.
- Population agreement (statistical; the tolerance is a multiple of `sigma / sqrt(n - 1)` that the builder derives and states on the page):
  `half_spread` near `theta + c`; `order_processing` near `c`; `adverse_selection` near `theta`; `roll_spread` near `2 sqrt(c(theta + c))`.
- Invariance: adding a constant to every price leaves all five outputs unchanged; multiplying every price by `k > 0` multiplies
  `roll_spread`, `half_spread`, `order_processing` and `adverse_selection` by `k` and leaves `adverse_share` unchanged.
- Sign of the Roll covariance (boundary): the estimator is finite exactly when `cov1 < 0`.
- Unclipped components: on seeds where the oracle's `adverse_selection` is negative, the solver returns the negative value.
- Hard-coded answer detection: the five outputs take distinct values across seeds 0 to 49.
- Failure messages name the violated property and hint at the concept (for example "the Roll spread should match the lag-one covariance of
  price changes: check the divisor and the mean used"); a failing check **never prints the expected value** (`__tracebackhide__` in the
  helpers, as in E4 §5.4). The collect-only count of the suite is quoted on the page.

**Dual mode.** Identical suite in Pyodide (pytest in Pyodide) and under local pytest; each test under 5 s in Pyodide; the suite under 60 s.

**Integrity.** Never claim the tests are secret. Integrity rests on per-seed instances (BUILDER_RULES §5.3 item 6).

### 5.5 Student-error mutants and alternatives (written by the verifier, not the builder)

**Ten student-error mutants** (the verifier writes each as a complete module to `ledgers/MS1/mutants/<name>.py`; each docstring's first line
names the student error; `tools/mutate_graders.py --unit MS1 --seeds 0-9` must kill all ten):
1. Roll covariance sign flipped: `roll_spread` uses `2√(cov1)` when `cov1 > 0`, so the estimator is inverted.
2. Roll divisor off by one: divides by `n − 1` (the number of price changes) instead of `n − 2` (the number of lag pairs).
3. Roll uses the lag-0 variance of price changes in place of the lag-1 covariance.
4. Roll computed on price levels instead of price changes (no differencing).
5. Regression fitted with an intercept (the page states no intercept).
6. Order-processing component taken as `+b1` (sign error), so `order_processing` is negative on every instance.
7. Adverse selection taken as `b0 − b1` (sign error when combining the two coefficients).
8. Look-ahead regressor: regresses `d_t` on `q_{t+1}` instead of `q_{t−1}`.
9. Hard-coded answer for the seed-0 instance: returns the reference's seed-0 values whenever the first price equals the seed-0 first price.
10. Sign validation missing: accepts a sign of 0 and returns values (no `ValueError`), where the page names the error.

The verifier may add one extra mutant (for example, the Roll NaN rule replaced by 0.0, which violates the stated rule and must be killed by
the boundary test); extra mutants are not counted in the ten. A mutant that differs from the reference only where the page states nothing is
moved to `ledgers/MS1/equivalent/` with a README proof (ruling 9).

**Five alternative correct implementations** (the verifier writes each to `ledgers/MS1/alternatives/alt_<n>.py`; each passes seeds 0 to 49
on the suite, ruling 10). Each uses a different style:
1. Two-pass means and direct sums with `math.fsum` (reference-like style).
2. Single-pass accumulator class (running sums, converted to float at the end; a different numerical path that stays within `1e-9`).
3. Exact `fractions.Fraction` arithmetic on the float inputs, converted to float at the end.
4. The 2 × 2 normal equations solved by Cramer's rule in a small dataclass pipeline.
5. A design-matrix form: rows of `(q_t, q_{t−1})`, the normal equations assembled and solved by Gaussian elimination with partial pivoting,
   with the same no-intercept convention.

Each alternative must give the same answers as the oracle within the tolerance in §5.4. A float-based alternative that is wrong on a stated
exact rule (for example, one that adds an intercept, or that returns 0.0 for an undefined Roll estimate) is a mutant, not an alternative.

### 5.6 Rubric (memo; `both` requires it, `tools/check_projects.py` `rubric_problems`, lines 58 onward)

Five criteria in one `table.rubric#rubric`, each with four observable levels (level 4 down to level 1). Each level descriptor names
something a grader can see.

1. **Model specification.** States the signs, the efficient price, the transaction price and the independence assumptions as numbered
   assumptions, and states which derived result uses which assumption. Level 4: each assumption numbered, each linked to the identity it
   supports. Level 1: "describes the model".
2. **Estimators and identities.** States the Roll formula with its divisor, the no-intercept regression, the two `nan` rules and the
   `ValueError` rules. Level 4: derives `Cov(d_t, d_{t−1}) = −c(θ + c)` and `b0 = θ + c`, `b1 = −c`, and names where each is used. Level 1:
   "the code works".
3. **Results and sign reading.** Reports the five outputs on the stated grid, with the sampling error, and states when the Roll estimate
   exceeds `2c` and why. Level 4: each sign and the grid points it holds on, with the population value beside the estimate. Level 1:
   "the results look plausible".
4. **Numerical rigour and rounding.** States the display rule and computes every number from unrounded values. Level 4: names the number
   of significant digits shown and the rule, and shows one number recomputed from unrounded values. Level 1: "rounds the numbers".
5. **Limits and evidence.** Names the model's limits (constant `c` and `theta`, i.i.d. signs, no inventory, one asset, no time variation,
   sign misclassification) and grades each empirical claim. Level 4: each claim graded B or C names its counter-evidence key, or says
   "no registry key; not claimed". Level 1: "notes some caveats".

**Exemplars** at two levels: `exemplar-a` (`data-level="4"`) and `exemplar-b` (`data-level="2"`), excerpts of notes on a SIMULATED instance,
each annotated with the descriptors it meets or misses, with `data-scores` and `data-criterion` as in M1 (`course/modules/M/M1/project.html`).
Self-assessment form `section.rubric-self` with `data-rubric="rubric"` and `data-exemplars="exemplar-a exemplar-b"`. The page shows where the
student's scores diverge from the exemplar scores. Calibration: a dedicated scorer, which never opens the project page, scores both exemplars
blind by a stripping script (architect ruling 23), within one level per criterion (VERIFIER §2.6).

**Adversarial question bank:** not required (§12 Q14). The note is not an investment-committee defence or a debate.

### 5.7 Time budget (`<table id="hours">`, sums to 26 h; every row has a one-line rationale; `tools/check_projects.py`, hours check)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 1 | One solved SIMULATED instance, annotated line by line (tier M keeps rung 1 minimal) |
| Rung 2, completion problem | 1 | Fill the processing-component line, then run the instant check |
| Model derivation: the identities of §5.2 | 4 | Derive the lag-1 covariance and the regression identities, with numbered assumptions |
| Data intake: the CSV schema, the sign rule, browser validation | 3 | Document the schema, state the sign rule, validate one student file |
| `decompose.py` and the local test run | 8 | Implement the frozen interface, pass seeds 0 to 49, raise the three named exceptions |
| Grid runs for the note | 3 | Run the solver on the θ and c grid the note uses, record the results |
| Write-up `report.md` | 4 | Model, estimators, results, limits, graded claims |
| Self-assessment against exemplars | 2 | Score the note with the rubric, then compare with `exemplar-a` and `exemplar-b` |
| **Total** | **26** | Equals `data-hours-project` on the hub |

---

## 6. Real-data policy (B1 applies)

- **Embedded (redistributable, grant quoted):** `fx_daily`, `fx_monthly`, `ust_daily` (`tools/data_sources.yaml:19`, `:53`, `:91`;
  `course/assets/data/market/MANIFEST.json`). None is a trade or quote series, so none is used by MS1.
- **Not embedded, no grant found:** trade-level data for any security. `tools/data_sources.yaml` `rejected:` (`:119`) lists the French library
  and Open Source Asset Pricing, neither a trade series. **Not embedded.**
- **Honest-pending note** on L01, L04, L06, L07, L08 and on the project's data page: "No trade-level dataset is embedded for this module. The
  examples use generated trades labelled SIMULATED (BUILDER_RULES §1.7). A student may supply a trade file in bring-your-own-data mode."
- **DATA_REQUEST:** none is raised by the planner, because the planner names no source and no licence from memory. If the architect wants an
  embedded real trade series, the builder requests one under `DATA_REQUESTS` with the source URL, the quoted licence sentence, the licence
  page and the transform (BUILDER_RULES §6.6, steps 1 to 5).
- **Bring-your-own-data:** the schema `time,price,sign` is documented on the project page and validated in the browser (BUILDER_RULES §6.6).
- No `data-files` attribute on any lab. No MANIFEST entry is added by builders. No figure: no live figure and no new JS kernel (§12 Q15).

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (verified in `references/references.json`; checked by the planner against the curriculum strings)

| Key | Record (as read) | Curriculum string | Status and use in MS1 |
|---|---|---|---|
| `roll1984simple` | "A Simple Implicit Measure of the Effective Bid‐Ask Spread in an Efficient Market", Roll, JF volume 39, issue 4, 1984, DOI 10.1111/j.1540-6261.1984.tb03897.x (`references/references.json:19991`); `used_by: ["MS1"]` | "Roll (1984), JF 39(4)" (`curriculum/04-quant.yaml:448`) | **Matches.** L01 at title level; reading list. |
| `kyle1985continuous` | "Continuous Auctions and Insider Trading", Kyle, Econometrica volume 53, issue 6, 1985, DOI 10.2307/1913210, page field "1315" (`references/references.json:15282`); `used_by: ["MS1"]` | "Kyle (1985), Econometrica 53(6)" (`:449`) | **Matches** on journal, volume, issue, year. Page range: the record holds only "1315" (B4). L05 and L06 at title level; the single-period version is not attributed to a section until the abstract is read (§12 Q12). |
| `glosten1985bid` | "Bid, ask and transaction prices in a specialist market with heterogeneously informed traders", Glosten and Milgrom, JFE volume 14, issue 1, 1985, pages 71-100 (`references/references.json:10453`); `used_by: ["MS1"]` | "Glosten & Milgrom (1985), JFE 14(1)" (`:450`) | **Matches.** L02 at title level; reading list. |
| `ho1981optimal` | "Optimal dealer pricing under transactions and return uncertainty", Ho and Stoll, JFE volume 9, issue 1, 1981, pages 47-73 (`references/references.json:12566`); `used_by: ["MS1"]` | "Ho & Stoll (1981), JFE 9(1)" (`:451`) | **Matches.** L03 at title level, with the note that the lesson's model is not claimed to be theirs; reading list. |
| `easley1996liquidity` | "Liquidity, Information, and Infrequently Traded Stocks", Easley, Kiefer, O'Hara and Paperman, JF volume 51, issue 4, 1996, pages 1405-1436 (`references/references.json:7505`); `used_by: ["MS1"]` | "Easley, Kiefer, O'Hara & Paperman (1996), JF 51(4)" (`:452`) | **Matches.** L07 at title level; reading list. |
| `easley2012flow` | "Flow Toxicity and Liquidity in a High-frequency World", Easley, López de Prado and O'Hara, RFS volume 25, issue 5, 2012, pages 1457-1493 (`references/references.json:7554`); `used_by: ["MS1"]` | "Easley, López de Prado & O'Hara (2012), RFS 25(5)" (`:453`) | **Matches.** L08 at title level; reading list. |
| `andersen2014vpin` | "VPIN and the flash crash", Andersen and Bondarenko, JFM volume 17, 2014, pages 1-46 (`references/references.json:592`); `used_by: ["MS1"]` | "Andersen & Bondarenko (2014), 'VPIN and the Flash Crash', Journal of Financial Markets 17" (`:454`) | **Matches.** L08 as the published dispute, at title level only until the abstract is read; reading list. |

**Keys in the registry that MS1 must not cite** (a different paper or another unit's): `roll1977critique` (AP2), `cont2010stochastic`
and `brogaard2014high` (MS2), `almgren2001optimal` and `obizhaeva2013optimal` (MS3). Each is `used_by` another unit.

**Abstract reads.** The planner read no abstract. The verifier reads the abstracts of `kyle1985continuous` and `andersen2014vpin` before the
lessons that depend on them are verified (VERIFIER §2.1); the registry titles are the only basis until then.

### 7.2 REFERENCE_REQUESTS (lead only; no bibliographic record typed by the planner)

These are needed only if the named claim is kept at grade B or C. The default is to remove the claim or to state it as a derivation.

- **R-MS1-1 (Roll estimator, counter-evidence).** {doi: null, authors: "not typed", year: "not typed", title: "published evaluations of serial-covariance spread estimators under price impact or time-varying spreads (topic only)", venue: "not typed", needed_for: "two-sided treatment of any empirical use of the Roll estimator in L01 and the project note (BUILDER_RULES §2.5)", confidence: "the need is certain; no record identified by this planner"}.
- **R-MS1-2 (PIN, counter-evidence).** {doi: null, authors: "not typed", year: "not typed", title: "published evaluations of the identification and estimation of the probability of informed trading (topic only)", venue: "not typed", needed_for: "L07 two-sided treatment of any empirical PIN claim", confidence: "the need is certain; no record identified"}.
- **R-MS1-3 (spread decomposition and price impact, empirical).** {doi: null, authors: "not typed", year: "not typed", title: "published empirical decompositions of effective spreads into adverse-selection and processing components (topic only; the planner has an unverified recollection of a 1997 decomposition by Huang and Stoll that it does not type, and the architect may admit it only after a DOI lookup)", venue: "not typed", needed_for: "L04 and L06 any statement about real spread components, and the note's reading list", confidence: "the need is certain; the recollection is unverified and is a lead only"}.
- **R-MS1-4 (Glosten–Milgrom, empirical adverse selection).** {doi: null, authors: "not typed", year: "not typed", title: "empirical tests of adverse selection in quote-setting by market makers (topic only)", venue: "not typed", needed_for: "L02 empirical sentence, if kept at grade B or C", confidence: "the need is certain; no record identified"}.
- **R-MS1-5 (microstructure book level).** {doi: null, authors: "not typed", year: "not typed", title: "a market microstructure textbook (topic only; none named by the planner)", venue: "not typed", needed_for: "book-level reading list entry if the architect wants one", confidence: "optional; no record identified"}.

The architect resolves each request through `tools/add_reference.py` (DOI, ISBN or an allow-listed issuer page; `references/authorities.yaml`;
BUILDER_RULES §2.4). Until then the lessons teach each model by derivation, state each empirical sentence at grade C with its basis, or remove it.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for MS1 (§0.1: no `atlas:` key at `curriculum/04-quant.yaml:456-463`; no Atlas entry names MS1).
No `atlas/MS1.contract.md` is needed. `tools/check_projects.py` skips the contract check when the project names no `atlas` key (lines 144 to 146).

---

## 9. Cards builder (Builder F, after A to E)

- `course/modules/MS/MS1/cards.json`, ids `MS1-c001` upward (sequential ids are not required, architect ruling 2), `lesson` in L01 to L08. One card
  per definition, theorem statement, key formula, key result and misconception (BUILDER_RULES §7). `tools/check_pages.py` `check_cards` checks the
  id prefix, the lesson existence, the grades and the registry keys.
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example `"basis": "Lab 1 and the
  derivation of Theorem 1.1 (exact under A1 to A4)"`.
- Cite a registry key only for an attributed claim (`roll1984simple` on L01; `glosten1985bid` on L02; and so on, at title level). `cite` is
  `[]` where the card is a model result.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`. No card cites a request in §7.2.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit MS1            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit MS1
.venv/bin/python tools/check_projects.py --unit MS1
.venv/bin/python tools/run_labs.py --unit MS1               # --page L05 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/MS/MS1/L01.html                           # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/MS/MS1/L05.html --refresh lab-MS1-L05-1  # after editing a twin
.venv/bin/python tools/run_graders.py --unit MS1 --seeds 0-49                                # after grader files exist
.venv/bin/ruff check tests/labs/MS1 course/modules/MS/MS1/grader && .venv/bin/ruff format --check tests/labs/MS1
.venv/bin/mypy tests/labs/MS1 course/modules/MS/MS1/grader                                   # strict, repository configuration
```

Verifier only, on a quiet machine: `.venv/bin/python tools/mutate_graders.py --unit MS1 --seeds 0-9` (the ten mutants, §5.5),
`.venv/bin/python tools/ledger.py --unit MS1 --check` (after fragments exist), `.venv/bin/python tools/page_smoke.py --unit MS1` (timing-sensitive;
not run by builders), and `.venv/bin/python tools/verify_refs.py --unit MS1` (the unit ledger's registry run, VERIFIER §2.1).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`, and the full
gate in CLAUDE.md. `tools/fetch_data.py --check` is not needed (no dataset is embedded for MS1).

Flags read by the planner in the tool sources: `check_pages.py` (`--unit`, `--page`), `check_projects.py` (`--unit`), `run_graders.py` (`--unit`,
`--seeds`; `parse_seeds` at line 118), `run_labs.py` (`--unit`, `--page`), `embed_labs.py` (pages and `--refresh`), `coursekit.py` (the
functions named in the header). The planner did not execute the builder commands.

---

## 11. Tooling assumptions that do not hold for MS1 (flagged)

1. **No Atlas milestone.** No `atlas:` key on MS1 (`curriculum/04-quant.yaml:456-463`); no Atlas entry names MS1. `check_projects.py` skips the
   contract check (lines 144 to 146). No `atlas/MS1.contract.md` is drafted.
2. **No debate.** MS1 has no `debate:` key, so `check_pages.py` (line 412) does not require a debate brief. The VPIN dispute and the Kyle and PIN
   claims are contested in the literature, so the two-sided rule (BUILDER_RULES §2.5) applies anyway (§3 L08; §7.2).
3. **Two grading modes.** `grading: both` requires the grader panel, the autograder word, the rubric word and two exemplars at two levels
   (`check_projects.py` `GRADING_WORDS` line 38; `rubric_problems` lines 58 onward).
4. **Ten mutants and five alternatives are not enforced by a tool.** The verifier's duties are recorded in the ledger's `mutants` list.
5. **One curriculum lab, eight twins.** The curriculum names one lab (`curriculum/04-quant.yaml:455`). The plan adds one lab per lesson and three
   project labs. The curriculum lab is `lab-MS1-L05-1` (§1).
6. **Closure modules that are not built.** CS1, S0, S1 and P0.1 have no `course/modules/` directory, so their pages do not exist. Links to their
   concepts go to `concepts.html` anchors only, which exist for these concepts (§0.1). E4 is built and is the nearest prerequisite whose plan is
   the template.
7. **`check_dag` sees linked uses only.** Unlinked names of out-of-closure concepts (§4) pass the tool. The verifier reads every lesson and the
   project for them.
8. **Labs must be exact or state their precision.** Standard library only. Float results print their rounding rule and, where a lab compares with an
   exact value, an error column.
9. **No tool checks the economics.** Nothing in `tools/` checks the derivations, the sign conventions or the population identities. The labs, the
   grader's oracle and the verifier do (VERIFIER §2.4, §2.5).
10. **Registry titles only.** The planner read the registry records, not the papers. Every attribution above is at title level until the verifier
    reads the abstract (§7.1).

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **Lesson count and hours.** RECOMMENDED: 8 lessons × 8 h = 64 h and a 26 h project (28.9%). Alternative within the rules: 8 lessons × 9 h and an
   18 h project (20%). Hours stay as declared once set (HOURS ruling).
2. **File ownership.** RECOMMENDED: Builder A owns L01, L02 and the hub; B owns L03 and L04; C owns L05 and L06; D owns L07 and L08; E owns the project,
   grader and project labs; F owns cards. The 2, 2, 2, 2 split is the E5 precedent. A 3, 3, 2 split over three lesson builders would leave one of A to
   D without a lesson and would not match the eight-concept structure.
3. **B1, data.** RECOMMENDED: SIMULATED generated trades for every lab, instance and exemplar; bring-your-own-data for the project's trade file with the
   schema `time,price,sign`; no DATA_REQUEST raised. Alternative: a redistributable trade-level source is read, quoted and added to
   `tools/data_sources.yaml` first.
4. **B2, project model.** RECOMMENDED: adopt the one-asset repeated-trade model of §5.2 (PD1 to PD4) with `decompose_trades(prices, signs)`
   returning the five keys of §5.2. The curriculum names no model (`curriculum/04-quant.yaml:458-461`). Decision needed before the project is built.
5. **D1, bid–ask spread and market maker (FC1).** RECOMMENDED: plain `<dfn>` terms in prose, no link. Alternative: add FC1 to MS1's prerequisites
   (a curriculum change; FC1 at topological 26 is before MS1 at 48, so the order is compatible, but the change is the architect's).
6. **D2, martingale (M6).** RECOMMENDED: not used; the expected posterior is equal to the prior by M4 `conditional-expectation-elementary`. No change.
7. **D3, Poisson process (SC5).** RECOMMENDED: plain `<dfn>` "Poisson distribution" in L07, no link. Alternative: add SC5 as a prerequisite. SC5 sits at
   topological 67, after MS1 at 48, so that change moves MS1 later in the order and is the architect's call.
8. **D4, OLS (S2).** RECOMMENDED: link M3 `least-squares-projection`; write the OLS normal equations inline with a plain `<dfn>`. Alternative: add S2 as a
   prerequisite (a curriculum change).
9. **Notation.** RECOMMENDED: as §2.3. Kyle's lambda is `\lambda`; the project's adverse-selection impact is `\theta`; the number of trades is `n`
   and never `T`; inventory is `I_t`; the trade sign is `q_t`. Confirm that no NOTATION_REQUESTS entry is needed.
10. **Roll undefined-case rule.** RECOMMENDED: `float("nan")` when `cov1 >= 0`, and `float("nan")` for `adverse_share` when `half_spread` is 0; no
    exception for either. Confirm.
11. **Solver interface (freeze before building).** RECOMMENDED: `decompose_trades(prices: list[float], signs: list[int]) -> dict[str, float]` with exactly the
    five keys of §5.2, and `ValueError` only for the three named conditions of §5.2 (fewer than three trades; a sign not in {−1, +1}; all signs equal).
12. **Kyle 1985 model variant.** RECOMMENDED: teach the single-period linear model derived on the page (L05); attribute it to `kyle1985continuous` at
    title level only; the verifier reads the abstract and confirms which model the paper states before any "the paper derives" sentence is kept.
13. **Counter-evidence leads R-MS1-1 to R-MS1-4.** RECOMMENDED: admit none in this batch. Any empirical claim without an admitted key is removed or
    graded C with its basis named (§2.2).
14. **Adversarial question bank.** RECOMMENDED: none. The note is not an investment-committee defence or a debate (E4 precedent).
15. **Figures.** RECOMMENDED: none in MS1. A figure of the Roll estimate against `theta` would need a kernel and a test first (BUILDER_RULES §6.4).
16. **Plain terms.** RECOMMENDED: bid–ask spread, half-spread, order-processing cost, signed trade, efficient price, bid–ask bounce, market maker, volume
    bucket, bulk-volume classification, Poisson distribution, noise trader, informed trader are plain `<dfn>` terms with no `data-concept` (E4 precedent).
    No glossary request.
17. **Scope.** RECOMMENDED: as §2.1 item 4 (one asset; one-period Kyle and Glosten–Milgrom; a repeated-trade model with i.i.d. signs for Roll and the
    project; the stated quadratic inventory model; no continuous time; no multi-asset claim). Confirm.
18. **Curriculum lab placement.** RECOMMENDED: the curriculum lab "Kyle equilibrium." (`curriculum/04-quant.yaml:455`) is `lab-MS1-L05-1` in L05, the Kyle
    lesson. Confirm.
19. **Stretch rung.** RECOMMENDED: misclassified signs (§5.1 rung 4). Confirm.
20. **Registry page range.** RECOMMENDED: the build cites `kyle1985continuous` without a page range. The record holds only "1315"
    (`references/references.json:15282`); the architect may correct the record through the registry tools (builders never edit it).

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01 to L02 (with the hub), L03 to L04, L05 to L06 (includes the curriculum lab
   `lab-MS1-L05-1`), L07 to L08, the project (the rubric and exemplar calibration, the ten mutants and five alternatives, the grader's runs), and
   the cards. Failing rows return to the owning builder, with only the failing rows.
3. Ledger at `ledgers/MS1.verification.json`, built from fragments under `ledgers/MS1-<slice>.json` (`tools/ledger.py --unit MS1 --check`). Verifier
   scripts are archived under `ledgers/MS1/scripts/` (VERIFIER §3). Mutants under `ledgers/MS1/mutants/`, alternatives under
   `ledgers/MS1/alternatives/`, equivalents under `ledgers/MS1/equivalent/`.
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 and B2 must be resolved, or named as honest
   gaps, first. The registry-title-only attributions (§7.1) are a named gap until the abstracts are read.

Architect decisions: pending (§12). This plan is the planner's proposal. Where a question has a RECOMMENDED decision, that decision is the default that
the builders follow until the architect says otherwise.

## Architect decisions (pending, binding once recorded). Where the plan states a recommendation for an open question, follow it. Defaults for every module: concepts outside the prerequisite closure are plain prose with no link and no dfn; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields only or not at all (never edit a record, never type bibliographic data); no real data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST in plans/<UNIT>-open-items.md; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every grader; not adversarial, no question bank. plans/FINAL-ARCHITECT-RULINGS.md and /Users/billyribeiro/.fanout/fixer-rules.md bind every builder. No reference is admitted in this batch: a statement whose source is a REFERENCE_REQUEST is not made, or it is taught as a model result with no attribution.
Module specifics (proposed, pending the architect): 8 lessons × 8 h + 26 h project; builders A: L01 to L02 and index; B: L03 to L04; C: L05 to L06; D: L07 to L08; E: project and grader; F: cards. The project model is the one-asset repeated-trade model of §5.2 with `decompose_trades(prices, signs)`. Kyle's lambda and the project's theta are different symbols. Trade-level data is SIMULATED with bring-your-own-data for the project.
