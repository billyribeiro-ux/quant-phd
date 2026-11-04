# E4 build plan: General Equilibrium & Information in Markets (planner output, 2026-11-03)

Unit: **E4 · General Equilibrium & Information in Markets** · tier M · 100 h · prerequisites E2, E3, M7 · no Atlas milestone ·
no debate key · grading `both` (autograder for the solver, rubric for the write-up) · output directory `course/modules/E/E4/`
(part code `E`) · lab twins `tests/labs/E4/` · ledger `ledgers/E4.verification.json` (fragments `ledgers/E4-<slice>.json`,
mutants `ledgers/E4/mutants/`, alternatives `ledgers/E4/alternatives/`, equivalents `ledgers/E4/equivalent/`).

Planner: Haiku, plan only. This file is the only file written. No curriculum, registry, notation, course or git edits, no
commit, no push. Executors: Haiku builders A to E (lessons, hub, project, grader) and F (cards), then independent Haiku
verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every curriculum fact cites `file:line` read during planning. Tool facts cite the tool source file and
line. Anything not in the curriculum is marked **NOT IN CURRICULUM**. Closed forms in §5 are not sourced; the builder derives
them and the verifier re-derives them. The planner read no paper and typed no bibliographic data from memory.

**Status: no hard blocker for the build. Two architect decisions are needed before their owners start:** B1 (the Grossman and
Stiglitz 1980 record, which blocks attribution in L08) and B2 (the project model, which the curriculum does not name). The
hours are feasible (§0.2).

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part E, code `E`, title "Economics" | `curriculum/02-economics-finance-core.yaml:3-4` |
| E4 id `E4`, title "General Equilibrium & Information in Markets" | `curriculum/02-economics-finance-core.yaml:124-125`; `curriculum/curriculum.json:7458` (`"id": "E4"`) |
| Tier `M`, hours `100` | `curriculum/02-economics-finance-core.yaml:126-127` |
| Prereqs `[E2, E3, M7]` | `curriculum/02-economics-finance-core.yaml:128`; `curriculum.json` E4 row, prereqs at lines 7462-7466 |
| Core: "Arrow–Debreu, complete vs. incomplete markets, rational expectations, the Grossman–Stiglitz paradox, the no-trade theorem." | `curriculum/02-economics-finance-core.yaml:129-131` |
| `introduces` has **9** concepts, each listed in §1 | `curriculum/02-economics-finance-core.yaml:133-141` |
| Sources: four strings (Mas-Colell, Whinston & Green 1995; Muth 1961; Grossman & Stiglitz 1980; Milgrom & Stokey 1982) | `curriculum/02-economics-finance-core.yaml:143-146` |
| Lab: "Grossman–Stiglitz equilibrium: fraction informed vs. information cost." | `curriculum/02-economics-finance-core.yaml:147` |
| Project "Price-informativeness model"; brief: "Solve a noisy rational-expectations model numerically, and show how price informativeness responds to noise-trader volume and information cost."; deliverable "Solver plus write-up."; grading `both` | `curriculum/02-economics-finance-core.yaml:148-154` (title 149, brief 150-152, deliverable 153, grading 154) |
| No `debate:` key and no `atlas:` key on E4 | `curriculum/02-economics-finance-core.yaml:124-154` (absent) |
| No Atlas entry names E4 (the 20 entries name CS1, CS3, S0, S4, FI1, DV4, F1, S7, QR2, MS3, PR2, PR4, FI3, CR1, AC2, CF4, QR3, GM1, SR3, GM4) | `curriculum/curriculum.json` `atlas` array |
| No dataset is named for E4 | `curriculum/02-economics-finance-core.yaml:124-154` (no data field) |
| Prerequisite closure of E4 (run by the planner with `tools/coursekit.py` `prerequisite_closure("E4")`): **{E1, E2, E3, M1, M2, M3, M4, M7, P0.1}** | planner run output |
| Usable concepts in that closure (sum of each module's `introduces`): E1 13, E2 12, E3 12, M1 14, M2 13, M3 12, M4 19, M7 10, P0.1 11 = **116** | `curriculum/curriculum.json` `parts` (planner count) |
| All 9 E4 concepts map to module E4 in `concepts` (planner check with `concept_owner`) | `curriculum/curriculum.json` `concepts` |
| Built prerequisites at planning: E1, E2, E3, M1 to M7 have `course/modules/` directories | `course/modules/E/`, `course/modules/M/` (directory listing) |
| Downstream users of E4: AP1 (`[M6, AP2, FC1, FC2, M8, E4]`), AP6 (`[AP5, E4]`), MS1 (`[E4, S1]`), SR1 (`[BK1, E4]`) | `curriculum/03-markets.yaml:268`, `:399`, `:434` (`04-quant.yaml:434`); `curriculum/05-macro-alternatives.yaml:437` |
| E4 is a requirement of the PhD credential, and sits in two first-year groups | `curriculum/meta.yaml:123` (PHD-FIN requires), `:130` (Corporate Finance Theory group), `:132` (Microeconomic Theory group) |
| Topological order positions: M7 at 14, E2 at 23, E3 at 24, E4 at 29 | `curriculum/curriculum.json` `topological_order` (planner read) |
| Nearest built prerequisite: E3 (plan `plans/E3-build-plan.md`); E2 is also a built direct prerequisite (`plans/E2-build-plan.md`). E3 is the structural template: it is a built `both`-graded prerequisite with a grader directory | `course/modules/E/E3/grader/` and `course/modules/E/E2/grader/` exist |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 100 h (`curriculum/02-economics-finance-core.yaml:127`). Tool rules:

- lesson `data-hours` 6 to 12 (`tools/check_pages.py` `check_lesson`, lines 219-228);
- hub `data-hours-lessons + data-hours-project = 100` (`tools/check_pages.py` `check_hub`, lines 332-338);
- project share 10 to 40% of 100, i.e. 10 to 40 h (`tools/check_pages.py` lines 339-340);
- lessons sum to the hub's lessons figure (`tools/check_pages.py` lines 341-342).

**Chosen split: 9 lessons × 8 h = 72 h; project 28 h (28%).** 72 + 28 = 100. Feasible. No STOP condition on hours.

### 0.3 Blocking and non-blocking issues

**B1 (architect; blocks attribution in L08 and the reading list, not the rest of the build). Grossman & Stiglitz (1980), AER 70(3) has no registry record.**
- Curriculum string: `curriculum/02-economics-finance-core.yaml:145`.
- The seed report lists it as unresolved, used by E4 and AP8 (`references/SEED_REPORT.md:31`); the review queue entry is `references/review_queue.json:109`, with "no candidate established identity".
- The review queue candidates are different articles. Candidate `10.2307/2296900` (DOI at `references/review_queue.json:133`) carries the title "The Existence of Futures Markets, Noisy Rational Expectations and Informational Externalities" (`:135`), which is not the requested title. Candidate `10.2307/128830` (`:119`) is a different article as well.
- The registry's `grossman1980takeover` (`references/references.json:11099`) is Grossman & Hart, Bell Journal of Economics 11(1), used by CF5. **It must not be cited or admitted as the Grossman–Stiglitz paper.**
- Plan default: L08 teaches the paradox as a result of the stated model (grade T, conditional on the listed assumptions). The attribution is graded C with the page-level basis "no registry key; REFERENCE_REQUEST R-E4-1". The reading list omits the paper until it is admitted (§7).

**B2 (architect; blocks the project's model, not the lessons). The curriculum names no model.**
- The brief asks to "solve a noisy rational-expectations model numerically" (`yaml:150-152`) and names noise-trader volume and information cost as the two drivers (`yaml:152`), but names no functional form, no information structure and no solver.
- Planner default: the CARA-normal noisy rational-expectations model described in §5.2 (proposal, §12 Q5).

**B3 (architect; non-blocking). The Mas-Colell record's authors conflict with the curriculum string.**
- Registry: `references/references.json:16579`, key `mascolell1995microeconomic`, book, verified by Open Library, year 1995, publisher Oxford University Press, `used_by: ["E4"]`. Its `authors` list is **Mas-Colell only**.
- Curriculum string: `yaml:143`, "Mas-Colell, Whinston & Green, Microeconomic Theory (1995)". The identity rule of VERIFIER §2.1 fails on the author list.
- Default: cite the key only, with no co-author names typed in prose, or do not cite it. The builders never edit the record. The architect decides on a correction through the registry tools (§12 Q12).

**B4 (non-blocking). No real data.** The curriculum names no dataset (`yaml:124-154`). No DATA_REQUEST is raised. Generated instances and seeded draws are labelled SIMULATED (§6).

**Non-blocking observations:**
- E4 appears in two first-year groups (`meta.yaml:130`, `:132`). No action; §12 Q15.
- `references/references.json` contains a registry record for `milgrom1982information` (`references/references.json:17291`, JET 26(1), 1982, Milgrom & Stokey) whose record matches the curriculum string at `yaml:146`. It is usable (§7.1).
- The registry macro for the reals is `\R` (`notation/notation.json:25-28`). Architect ruling 1 (`plans/FINAL-ARCHITECT-RULINGS.md:3-5`) requires `\R` and forbids `\mathbb{R}` in module pages.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

9 lessons × 8 h = 72 h; project 28 h; total 100 h. The nine concepts map one to one onto the nine lessons (`yaml:133-141`),
so each concept is defined in exactly one lesson.

| Lesson | Title (working) | Concept it defines (`introduces`) | Lab twin id (`tests/labs/E4/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Arrow–Debreu securities and state-contingent payoffs | `arrow-debreu-security` (`yaml:133`) | `lab-E4-L01-1`: a claim's payoff decomposed into Arrow–Debreu security payoffs state by state, and its value as the sum of state-weighted security prices, exact in `Fraction` | 8 | Builder A |
| L02 | Arrow–Debreu equilibrium | `arrow-debreu-equilibrium` (`yaml:134`) | `lab-E4-L02-1`: a two-agent, two-state exchange economy with log utility; equilibrium prices by market clearing, exact in `Fraction`; budget and market residuals printed as zero | 8 | Builder A |
| L03 | The first welfare theorem | `first-welfare-theorem` (`yaml:135`) | `lab-E4-L03-1`: at the L02 equilibrium, equality of marginal rates of substitution checked exactly; a finite grid of feasible allocations searched for a Pareto improvement (finite enumeration, grade C with its basis) | 8 | Builder A |
| L04 | Complete and incomplete markets | `market-completeness` (`yaml:136`) | `lab-E4-L04-1`: rank of a payoff matrix by exact Gaussian elimination; complete iff rank equals the number of states; one incomplete and one complete example | 8 | Builder B |
| L05 | Rational-expectations equilibrium | `rational-expectations-equilibrium` (`yaml:137`) | `lab-E4-L05-1`: the coefficient fixed point of a linear-normal one-period model with rational expectations, solved exactly and checked by iterating the map from a stated start | 8 | Builder B |
| L06 | Noisy rational-expectations equilibrium | `noisy-rational-expectations-equilibrium` (`yaml:138`) | `lab-E4-L06-1`: the price coefficients of the noisy model against a seeded sample regression; the population values exact, the sample values **SIMULATED** and tolerance printed | 8 | Builder C |
| L07 | Price informativeness | `price-informativeness` (`yaml:139`) | `lab-E4-L07-1`: the squared correlation between payoff and price as the noise volume varies, from population formulas; a seeded **SIMULATED** check | 8 | Builder C |
| L08 | The Grossman–Stiglitz paradox | `grossman-stiglitz-paradox` (`yaml:140`) | `lab-E4-L08-1` (**the curriculum lab**, `yaml:147`): the informed fraction λ*(c) by bisection with a stated tolerance over a grid of information costs; the indifference gap printed at each point | 8 | Builder D |
| L09 | The no-trade theorem | `no-trade-theorem` (`yaml:141`) | `lab-E4-L09-1`: a finite-state common-prior model with two partitions; every candidate trade on a grid checked against the posteriors (finite enumeration, grade C with its basis) | 8 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours 72/28 | none | none | – | Builder A (after L03 exists) |
| project | Price-informativeness model (`both`), §5 | none | `lab-E4-project-1` (rung 1), `lab-E4-project-2` (rung 2, `class="lab completion"`), `lab-E4-project-3` (rung 3 check) | 28 | Builder E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` | none | none | – | Builder E |
| cards | `cards.json` from L01 to L09 | none | none | – | Builder F (after A to E) |

**Ownership rule.** Each builder writes only its own lesson files and twins. Builder A writes the hub after L03 exists.
Builder E writes the project, its rubric, exemplars and grader, and does not depend on the lessons' prose. Builder F writes only
`cards.json`.

**Why four lesson builders and not three.** The brief asks for about three lessons per builder. Five builders (A to E) with the
last one owning the project leave four builders for nine lessons: 3, 2, 2, 2. A larger spread would need 15 or more lessons,
and 15 lessons of 6 h cost 90 h, which exceeds the 72 h lesson budget. §12 Q2 records this.

Ordering check (every use of a concept is inside the closure or an earlier lesson of E4; `check_dag.py` checks linked uses,
§4 covers unlinked ones):
- L01 uses M3 `linear-map`, `vector-space` (the payoff matrix) and M4 `random-variable`.
- L02 uses L01 `arrow-debreu-security`, E1 `utility-maximization` and `competitive-equilibrium`, E3 `expected-utility`, M7 `lagrange-multiplier` and `kkt-conditions` (the budget problem), M2 `derivative`.
- L03 uses L02 `arrow-debreu-equilibrium`, E1 `pareto-efficiency`, M2 `gradient` (marginal rates).
- L04 uses L01 `arrow-debreu-security`, M3 `linear-map` and rank, and L03 only for the contrast in its Remark.
- L05 uses M4 `expectation`, `variance`, `conditional-expectation-elementary`, `normal-distribution`, and L04 `market-completeness` only where the information set is compared.
- L06 uses L05 `rational-expectations-equilibrium`, M4 `covariance-matrix`, `multivariate-normal`, M3 `least-squares-projection`, `orthogonal-projection`.
- L07 uses L06 `noisy-rational-expectations-equilibrium`, M4 `correlation`, `variance`.
- L08 uses L07 `price-informativeness`, E3 `expected-utility`, `certainty-equivalent`, `arrow-pratt-risk-aversion`, E1 `competitive-equilibrium`, M2 `derivative`.
- L09 uses L02 `arrow-debreu-equilibrium`, E1 `pareto-efficiency`, M4 `conditional-expectation-elementary`, E2 `adverse-selection` (contrast only).

Hours check: 9 × 8 = 72 (hub `data-hours-lessons="72"`); project 28 (hub `data-hours-project="28"`); total 100.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to E4)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3 to §8, `VERIFIER_RULES.md` §2 (what the verifier checks),
`plans/FINAL-ARCHITECT-RULINGS.md`, `/Users/billyribeiro/.fanout/fixer-rules.md`, this file, and `plans/E3-build-plan.md`
(the nearest built prerequisite's plan, whose precedents this plan adopts). Study `course/modules/E/E3/` (hub, lessons, project,
grader panel, rubric) and `course/modules/M/M1/` for layout. Imitate structure, not wording. `course/templates/` holds the four
skeletons.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier unit)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) or from floats
   stated to full precision, and rounded only at display. A page that shows a rounded figure states its rounding rule. Precedent:
   E3 §2.1 item 1, E5 §2.1 item 1, AC4 KNOWN LIMITATION 3, CF1 L01 Remark 5.2. For E4 this covers every informed fraction, every
   correlation and every indifference gap.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints; the interpretation names only what
   the printed numbers show. Every "checked", "verified" or "shown" claim names the lab, line or test that did it. Precedent: M1
   LESSON_TEXT_DEFECTS.
3. **Attribute nothing unread.** Cite only the registry keys in §7.1. No locator, page, table, equation number, coefficient or
   date is typed unless the builder has read it. A result from a source the builder has not read is either a derivation on the
   page (grade T, conditional on the stated assumptions) or is named "not stated here". Precedent: E3 §2.1 item 3; fixer rule
   "Attribute nothing you have not read". The Grossman–Stiglitz paper is not in the registry (B1): its paradox is taught as a
   model result, and no attribution is typed.
4. **Scope words need a computation, a witness or an explicit hypothesis.** "every", "all", "never", "always", "any", "only",
   "same", "drives", "exactly", "in general", "market structures", "welfare" are used only where a derivation, a finite check or a
   lab computes the claim. E4 scope (confirm, §12 Q20): competitive price-taking; one risky asset in the project; a static
   one-period or two-date setting; finite-state examples in the labs; the CARA-normal model in L08 and the project; no claim
   that equilibrium exists in general, unless stated as an Assumption.
5. **Define before use.** Each of the nine concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned
   lesson, and never before it. Terms outside the nine (the payoff matrix, the posterior, the informed fraction, the noise
   supply, the signal, the information cost, the correlation between payoff and price, "noise traders", "informationally
   efficient", CARA utility) are defined in prose at first use with a plain `<dfn>` and no `data-concept` (`tools/check_dag.py`
   skips a `<dfn>` without `data-concept`).
6. **Propositions state every hypothesis, numbered.** Every Theorem, Proposition, Lemma and Derivation block lists numbered
   Assumptions (A1, A2, …) before the statement, and its proof cites them by number. Examples the builders must state: finite
   states and strictly positive state probabilities (L01 to L03, L09); strictly increasing, strictly concave, differentiable utility
   on the stated domain (L02, L03); the rank condition for completeness (L04); the linear-normal information structure and a
   nonzero noise variance (L05 to L08); the sign-change and continuity condition behind any bracketing bisection (L08, §4 D4).
7. **Grader rule.** Applies to the project grader (§5.4). A test may demand an exception type only for a condition the page names.
   The page names two conditions (§5.4). Every other invalid input may raise any exception or return.
8. **Money.** E4 has no money output. Informed fractions, prices, correlations and utilities are dimensionless floats or
   exact rationals, and each carries its rounding rule. If the builder introduces a currency unit, it is integer cents, rounded
   once, half up, stated on the page (fixer rule, "Money is integer cents").
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own container;
   no element widens the page past 360 px. `page_smoke.py` is the verifier's check; builders do not run it.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":`
    guard. `run_labs.py` runs each twin as `python -I -W error <twin>` with no network. Precedent: M1 twin
    `tests/labs/M1/lab-M1-L04-1.py`; E3 §2.1 item 11.
11. **Lab hypotheses before runs.** Each lab's `p.hypothesis` states the expected result before the expected-output block is
    embedded. Every RNG is seeded with `random.Random(seed)`. The standard library only (`fractions`, `math`, `random`,
    `itertools`); no NumPy or SciPy in labs; under 10 s in Pyodide.
12. **Bisection is stated, not assumed.** A lab or the solver that uses bisection states its bracket, its tolerance, its stop
    rule and the sign-change assumption. The printed indifference gap at the reported root is the evidence. Precedent: E3 §6.4
    (bisection with a stated tolerance).
13. **Graded-instantly completion problem.** The rung-2 completion lab (`class="lab completion"`) shows `___` blanks. Every page
    line equals its twin line or contains a blank (`tools/run_labs.py` completion rule).
14. **Architect rulings apply.** Ruling 1: use the macro `\R`, never `\mathbb{R}`. Ruling 2: card ids need not be sequential.
    Ruling 9: a mutant that survives and violates a stated behaviour gets a new test; a mutant that differs only where the page
    states nothing goes to `ledgers/E4/equivalent/` with a README proof. Ruling 10: five correct alternative implementations
    must pass seeds 0 to 49 (§5.5). HOURS ruling: declared hours are design targets; do not change them to match an estimate.
    LAB MUTANTS ruling: lab twins are demonstrations, and mutation testing applies to the project grader only.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- **Evidence.** Every claim carries a grade (T, A, B, C, D or X, BLUEPRINT §3) and a registry key or a derivation. A B- or C-graded
  claim names its published counter-evidence (BUILDER_RULES §2.5). **No registry record exists for the model results in §3,
  and none is claimed.** Empirical claims about rational expectations, price informativeness, the paradox or the no-trade result
  are C at most, with the basis named, or are removed (§7.2).
- **Concept links.** Prerequisite closure concepts (E1, E2, E3, M1 to M4, M7, P0.1): `<a class="concept" data-concept="<id>"
  href="../../../concepts.html#<id>">`. Earlier E4 lessons: `href="Lnn.html#def-<id>"`. A lesson never links a concept defined in
  a later lesson. There is no link to an E1, E2 or E3 hub page: the convention in BUILDER_RULES §4.1 links to `concepts.html` anchors
  for prerequisite modules.
- **Labs.** Code lives once in `tests/labs/E4/lab-E4-Lnn-1.py` (and `lab-E4-project-1..3.py`). The page carries `@@LAB:<file>@@`
  and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-E4-<page>-<n>`
  (`tools/check_pages.py` lab-id rule). Lab ids are numbered in display order.
- **SIMULATED label.** Required on any lab, figure or grader instance that uses generated data or seeded draws (L06, the L07
  sample check, `instance.py`, the rung-1 worked example, exemplars). Exact population computations are not labelled SIMULATED.
- **Never hand-edit generated files**: `CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `notation/notation.json`, `MANIFEST.json`. Request changes in the output contract.
- **Learner-visible text.** No process words in the page (build, builder, round, verifier, REQUESTS, unit report) and no planning
  references in code comments (E3 §2.2 precedent).
- **Banned strings** (`tools/check_pages.py` lines 58-73 `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the
  scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well
  known", "obviously", "clearly", and any ellipsis `...` outside code.
- **Percent changes** state the base and the direction. **Growth or return rates** state their convention. **Correlations** state
  the sample or the population.
- **A finite enumeration is grade C with its basis named**, not grade T (M1 L06 precedent). Used in L03, L09 and the project's
  instance guard.
- **Hub lesson titles** match each lesson's `<h1>` at integration (CF1 KNOWN 3 precedent). **Quiz explanations** are read against
  their lesson (CF1 KNOWN 6 precedent).
- **No `git commit`, no push.** The builder reports files written, commands run with exact output, and every gap in the BUILDER_RULES
  §10 output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered macros and symbols that E4 must use or must not reuse (`notation/notation.json`):

| Registered item | Registered meaning (locator) | E4 rule |
|---|---|---|
| `\E` (macro) | expectation operator (`notation.json:5-8`) | Use the macro for every expectation. Never write raw `\mathbb{E}`. |
| `\Var`, `\Cov`, `\Corr` (macros) | variance, covariance, correlation (`notation.json:13-24`) | Use the macros. The squared correlation in L07 and the project is written `\Corr(\cdot)^2`. |
| `\R` (macro) | real numbers (`notation.json:25-28`) | **Use `\R` (architect ruling 1).** |
| `\Normal` (macro) | normal distribution (`notation.json:37-40`) | Use for every normal law. |
| `\indic` (macro) | indicator function (`notation.json:33-36`) | Use for indicators of states. |
| `\argmax`, `\argmin` (macros) | argmax and argmin (`notation.json:53-60`) | Use if an argmax is written. |
| `T` | number of return observations (`notation.json:111-115`, module S1) | **Never used.** Horizons and sample sizes are written `n`; two dates are "t = 0 and t = 1". |
| `\Phi`, `\Phi^{-1}` | standard normal CDF and its inverse (`notation.json:116-120`, M4) | **Not used.** The normal CDF is not needed. |
| `\gamma_3`, `\gamma_4` | skewness and kurtosis (`notation.json:121-130`, M4) | **Not used.** Plain `\gamma` is not used either. |
| `R^\ast`, `R^{e\ast}`, `R_f` | SDF return, projection of 1, gross riskless return (`notation.json:131-145`, AP1) | **Not used.** The riskless return is not needed. |
| `\mathbb{Q}` | equivalent martingale measure (`notation.json:146-150`, AP1) | **Not used.** Do not write `Q` for a measure. |

Local symbols (allowed; each defined on the lesson where it first appears and never redefined): `v` payoff (the risky asset's
liquidation value, the fundamental), `p` price, `s` signal, `\varepsilon` signal noise, `u` noise-trader supply, `\sigma_u` its
standard deviation, `c` information cost, `\lambda` the informed fraction (the unit's own local symbol; E3's λ is a different
unit's local symbol and is not cross-referenced), `a` the CARA coefficient, `\rho` the correlation between payoff and price,
`x` a demand, `\pi_i` a state probability, `\mu` a mean. A symbol with a registered meaning above is never reused with another
meaning.

NOTATION_REQUESTS: **none.** The plan needs no new macro. An optional `\CE` macro for the certainty equivalent would repeat
E3's note (E3 §4); it is not requested.

---

## 3. Lesson content plan (what each lesson must establish; the builder decides the argument)

For each lesson the builder writes the BUILDER_RULES §4.2 structure in order: why it matters (at most 120 words), numbered
core sections of Definition, Theorem, Proof, Example and Remark blocks, the inline lab (before "where the canon breaks"), where
the canon breaks (at least one model limit and what changes without it), misconceptions (at least 3), problem set (at least 3
each in Mechanics, Proof, Empirical and Research, each with a `<details class="solution">` of at least 15 words), key-results
table (claim, grade, keys), quiz (8 to 15 items, each with an explanation), and references (`<ol data-references>` of registry
keys). **No debate brief**: E4 has no `debate` key (§0.1).

- **L01 `arrow-debreu-security`.** A state-contingent claim is a payoff vector over finitely many states. An Arrow–Debreu security
  pays one unit in one state and zero otherwise (definition). Any payoff is the sum of security payoffs weighted by its state
  values (T, one line; Assumption A1: finite state space). The value of a claim is the sum of the security prices weighted by the
  payoff (T, linearity). **Do not use the term "state price"**: it is owned by AP1 (§4 D2). The lab computes the decomposition
  and the value exactly.
- **L02 `arrow-debreu-equilibrium`.** Two agents, finitely many states and one good per state. Each agent maximises expected
  utility (E3 `expected-utility`) subject to a budget set priced at the Arrow–Debreu security prices. Equilibrium is an allocation
  and a price vector at which each agent's demand is optimal and markets clear (definition; existence is **an assumption**, not
  a theorem, §4 D4). Walras' law is stated as a derivation from the budget constraints (T). The lab's log-utility example is solved
  by the builder; the planner has not derived its demands. Market clearing is plain prose (§4 D9).
- **L03 `first-welfare-theorem`.** At an equilibrium allocation, marginal rates of substitution are equal across agents, and no
  feasible allocation Pareto-dominates it (statement with Assumptions A1 to A3, proof by the first-order conditions; grade T under
  the stated assumptions). The Pareto claim in the lab is a finite enumeration on a grid (grade C with its basis). The lesson states
  the model's limits: no transaction costs, complete preferences, no externalities (E1 `externality` is in the closure and may be
  linked as the limit).
- **L04 `market-completeness`.** Markets are complete when the payoff matrix of traded securities has rank equal to the number
  of states (definition, with a derivation that complete markets span every payoff, T in the finite case, Assumption A1). Incomplete
  markets are those with rank strictly below the number of states. The lab's exact rank computation is the evidence. The lesson
  states what changes when markets are incomplete (equilibrium need not be efficient): **this is stated as a consequence the lesson
  does not prove**. Remove it unless the builder proves it on a stated finite example (§12 Q18).
- **L05 `rational-expectations-equilibrium`.** In a linear-normal one-period model, agents' expectations of the price are the
  conditional expectations under the equilibrium price map (definition; M4 `conditional-expectation-elementary`, `normal-distribution`).
  The rational-expectations equilibrium is a fixed point of the coefficient map (definition and an existence claim **only for the
  stated linear family**, Assumption A2). The lab checks the fixed point exactly. The model's source is Muth (1961), cited at paper
  level only (key `muth1961rational`, §7.1). No empirical claim about rational expectations is made (§7.2 R-E4-3).
- **L06 `noisy-rational-expectations-equilibrium`.** Add a noise-trader supply `u` (a normal random variable independent of the
  payoff) to the price map. The price then reveals the payoff only with noise, and agents' conditional expectations become a
  linear projection (M3 `least-squares-projection`, `orthogonal-projection`; M4 `covariance-matrix`, `multivariate-normal`).
  The population coefficients are derived (T, conditional on the stated normal model). The lab compares them with a seeded
  sample regression, labelled **SIMULATED**, and prints the tolerance. The term "noise traders" is defined in plain prose (§4 D6).
- **L07 `price-informativeness`.** The measure is the squared correlation between the payoff and the price, \(\Corr(v,p)^2\),
  in the model (definition, M4 `correlation`). It lies in \([0,1]\) (T, Cauchy–Schwarz on the stated moments). How it responds to
  the noise volume is **not asserted in advance**: the lesson derives the population formula and reports the sign that the
  formula gives on the stated parameter range (§12 Q7). The lab sweeps the noise volume using the exact formula; the seeded
  check is SIMULATED.
- **L08 `grossman-stiglitz-paradox`.** Informed agents pay a cost `c` to observe the signal. Informed and uninformed agents have
  equal expected utility at the equilibrium fraction λ* (definition of the indifference condition). The paradox is stated as a
  result of the model: prices reveal the signal only when enough agents are informed, and the informed earn a return that must
  compensate the cost, so prices cannot be fully informative when information is costly (grade T, conditional on Assumptions A1
  to A4 of the model; the attribution is C with the basis "no registry key; REFERENCE_REQUEST R-E4-1"). The **curriculum lab** is
  here: λ*(c) by bisection with a stated bracket, a stated tolerance and the indifference gap printed. The boundary rule is stated
  on the page (§12 Q8). The lesson's conclusions are limited to the model.
- **L09 `no-trade-theorem`.** Two agents with a common prior, and partitions of a finite state space that give each agent's
  information. A posterior is a conditional probability (M4 `conditional-expectation-elementary`; Bayes' rule written as a
  quotient of probabilities, §4 D1). The no-trade result is stated for a finite model with its Assumptions (common prior,
  common knowledge of the partitions, rational updating, and the stated trading rule): T in the finite model. The attribution to
  Milgrom and Stokey (1982) is at paper level only (key `milgrom1982information`, §7.1); the builder reads the abstract before
  naming the paper's claim, and the general claim is graded B with its counter-evidence named or is removed (§7.2 R-E4-2). The lab
  enumerates candidate trades on a grid (grade C, finite).

Lesson-level constraint: no lesson uses an E6 term (equilibrium determinacy, New Keynesian, dynamic IS) or an E8 term (open
economy). Those are outside E4 and not in its closure.

---

## 4. DAG problems (concepts natural E4 content would use outside the closure)

Closure of E4 (computed, §0.1): {E1, E2, E3, M1, M2, M3, M4, M7, P0.1}, 116 usable concepts. Owners below are from
`curriculum/curriculum.json` `concepts`.

| Ref | Concept or term | Owner (outside closure) | Where natural E4 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `bayesian-inference` (S1, `curriculum.json` `concepts`) | S1 | posterior beliefs in L09 and the signal extraction in L06 | Bayes' rule written as the quotient of probabilities, and posteriors as conditional distributions (M4 `conditional-expectation-elementary`). Plain prose, no link, no S1 name. §12 Q3 (alternative: add S1 as a prerequisite; a curriculum change, not proposed). |
| D2 | `state-price`, `stochastic-discount-factor`, `law-of-one-price`, `fundamental-theorem-of-asset-pricing` (AP1) | AP1 | the Arrow–Debreu security price vector (L01, L02) | E4 writes "Arrow–Debreu security price vector" and never "state price". E4 does not define any AP1 term. §12 Q4. |
| D3 | `efficient-markets-hypothesis` (FC3) | FC3 | the paradox's name is about informational efficiency (L08) | Plain prose "informationally efficient" defined with a plain `<dfn>` in L08. No link. |
| D4 | `banach-fixed-point-theorem`, `completeness-of-reals` (M5) | M5 | existence of equilibria and the continuity needed for bisection (L02, L05, L08) | Existence is a numbered Assumption, never a theorem. The bisection's sign-change and continuity condition is stated as Assumption A-bisect. No M5 name. §12 Q14. |
| D5 | `martingale`, `martingale-convergence-theorem` (M6) | M6 | prices as martingales (not needed) | Not used. |
| D6 | `noise-trader-risk` (AP7) | AP7 | "noise traders" in L06 and the project (a different object: behavioural risk) | Plain `<dfn>` "noise traders" with no `data-concept`. The phrase "noise-trader risk" is never used. |
| D7 | CARA utility (no curriculum concept; E3 defines only `crra-utility`) | none | the Grossman–Stiglitz-type model (L08, project) | Plain `<dfn>` "constant absolute risk aversion (CARA) utility" in L06 or L08, no `data-concept`. Not a DAG defect (no owner). |
| D8 | common knowledge (no curriculum concept) | none | the no-trade result (L09) | Plain prose. No link. |
| D9 | Walras' law and market clearing (no curriculum concept; E1 owns `competitive-equilibrium`) | none (E1 for the equilibrium term) | L02 | Plain prose beyond E1's `competitive-equilibrium`. No link beyond it. |
| D10 | `two-fund-separation` (AP2), `diagnostic-expectations` (AP7), `equilibrium-determinacy` (E6), the price-impact and informed-trading terms of MS1 (`probability-of-informed-trading`) | AP2, AP7, E6, MS1 | not needed; some are name collisions with rational expectations | Not used. E4 does not discuss determinacy (§2.2). |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Each row needs the architect's confirmation (§12 Q3, Q4, Q14).**
`check_dag.py` checks linked uses only (`tools/check_dag.py` docstring); an unlinked use of D1 to D10 passes the tool, so the
verifier reads every lesson and the project for these names (VERIFIER §2.9).

---

## 5. Project (`project.html`, Builder E): ladder, spec, model, grader, rubric

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py` requires the order)

1. **Rung 1, worked example** (`lab-E4-project-1`, SIMULATED instance): one fully solved, annotated run of the solver on one
   generated instance, with a "why" note on each step: the informed-fraction equation, the bracket, the bisection, the indifference
   gap, the informativeness. From tier M upward, rungs 1 and 2 are kept to the minimum (BUILDER_RULES §5.1, after the table).
2. **Rung 2, completion** (`lab-E4-project-2`, `class="lab completion"`, SIMULATED instance): the indifference-gap line of the
   bisection is removed (`___`). Graded instantly. Its twin is the completed solution; every page line equals the twin line or
   contains a blank.
3. **Rung 3, independent project (graded):** (a) the autograded solver `solver.py` to the §5.2 interface, and (b) the write-up
   `report.md`, rubric-graded (§5.4). `lab-E4-project-3` is the rung-3 check: it calls the solver on the reference case and prints
   the informed fraction and the informativeness for the noise and cost grid the report must use.
4. **Rung 4, stretch** (optional, not graded): a second information structure (for example, costly information that also
   reduces the noise of the signal), with the comparison stated as a hypothesis before it is run.

### 5.2 Spec (`dl.spec`; `tools/check_projects.py` requires the terms and both grading words, lines 38 to 49)

Terms: Context (2 to 4 sentences), Inputs, Required outputs, Constraints, Grading, Reading list.

- **Context.** A market for a risky asset has informed and uninformed investors. Informed investors pay a cost to observe a
  signal of the payoff. Noise traders add a random supply. The question is how the equilibrium price's informativeness responds to
  the noise volume and to the information cost, and why the informed fraction takes the value it does.
- **Inputs.** No dataset (§6). The instance supplies the parameters of §5.3: risk aversion `a`, prior precision, signal precision,
  noise-trader standard deviation `sigma_u`, information cost `c`. The student's grid of noise volumes and costs is written in
  `report.md`.
- **Model (planner proposal, B2, §12 Q5).** One risky asset with payoff `v` normal with prior mean and precision. Noise-trader supply
  `u` normal with mean zero and standard deviation `sigma_u`, independent of `v`. A signal `s = v + eps` with normal noise and a
  stated precision. Competitive CARA investors with coefficient `a`. A fraction `lambda` of investors observe the signal at cost `c`.
  The equilibrium price is a linear function of the signal and the noise supply in the model. **The planner has not derived any
  equation of this model.** The builder derives the equilibrium, the informed-fraction condition and the informativeness formula
  (`Corr(v,p)^2`), and the verifier re-derives them. The source of this model is REFERENCE_REQUEST R-E4-1, and the page cites no
  registry key for it until that request is resolved.
- **Required outputs.**
  - `solver.py` with the frozen interface below.
  - `report.md` with the sections named in the rubric (§5.4).
  - Frozen interface (§12 Q9):
    - `solve_model(noise_sd: float, info_cost: float) -> dict[str, float]`, returning exactly the keys `informed_fraction`,
      `price_informativeness` and `indifference_gap`. `informed_fraction` lies in `[0, 1]`; `price_informativeness` is the squared
      correlation between payoff and price, in `[0, 1]`; `indifference_gap` is the expected-utility difference between the
      informed and the uninformed investor at the reported fraction.
    - The instance's other parameters (risk aversion, prior and signal precision) are read from the instance by the grader and
      passed through a module-level `DEFAULTS` mapping, or are fixed in the module, as the builder states on the page.
- **Constraints.**
  - Floats at full precision inside the solver; the report displays a stated number of significant digits and states the rule.
  - Valid input and the exception table (§5.4); no other exception type is required.
  - Standard library only; no network; the same code runs in Pyodide and under pytest.
  - The solver's bisection tolerance is a documented constant on the page, not an argument of the interface.
- **Grading.** Autograder (`grader/test_project.py`, dual-mode) for `solver.py`; rubric (`rubric-memo`, §5.4) for the report. The spec
  names both "autograder" and "rubric" (`tools/check_projects.py` `GRADING_WORDS`, line 38).
- **Reading list.** `ol.reading-list` cites `muth1961rational` and `milgrom1982information` only (registry keys, §7.1). The
  Grossman–Stiglitz paper is added only after REFERENCE_REQUEST R-E4-1 is resolved. `mascolell1995microeconomic` is not cited
  while B3 is open.

### 5.3 Instance generator and validity (`grader/instance.py`, Builder E)

- `make_instance(seed: int) -> dict[str, float]`. Deterministic: `random.Random(seed)` only. Generates valid parameters inside
  documented ranges. The docstring says **SIMULATED**.
- Validity per seed: every parameter positive and finite; the informed fraction of the reference solution lies strictly inside
  `(0, 1)`, so that the indifference test is meaningful (an identification guard); the informed-fraction root is bracketed with
  a sign change (checked in `instance.py`); and the instance's parameters stay in the ranges the grader documents.
- Distinctness: `run_graders` requires that no two of the first 20 seeds produce identical instances (`tools/run_graders.py`
  `check_instances`, lines 79 to 105), and that `make_instance` is deterministic (same lines).
- Exact parameter ranges and the guard's numerical thresholds are written on the page, not in the tests.

### 5.4 Grader (`course/modules/E/E4/grader/`, Builder E)

**Files:** `instance.py`, `reference.py` (the full solution; excluded from deployment, BLUEPRINT §7), `starter.py` (stubs that raise
`NotImplementedError`; the suite must fail on it), `test_project.py`. No Atlas path.

**Grader panel** on `project.html`: `<section class="grader-panel" id="grader" data-unit="E4" data-grader="grader/"
data-suite="test_project.py" data-support="instance.py" data-solution="solver.py" data-starter="starter.py"></section>`.
`data-packages` is empty (standard library only). `tools/run_graders.py` reads these attributes (`panel()`, lines 43 to 49).

**Exception table** (grader tests demand these, and only these; ruling 19 of `/Users/billyribeiro/.fanout/fixer-rules.md`):

| Condition the page names | Exception | Message must name |
|---|---|---|
| `noise_sd` not positive (or not finite) | `ValueError` | "noise volume must be positive" |
| `info_cost` negative | `ValueError` | "information cost must be nonnegative" |

Any other invalid input may raise any exception or return. Each named condition gets its own isolated test, in both directions of
its inequality (for example, `noise_sd = 0` and `noise_sd = 1e-12` are tested separately, and `info_cost = 0` is valid).

**Test properties** (`test_project.py`; each test recomputes its expectation from the instance's parameters with an oracle written
separately from `reference.py`):
- indifference: when `0 < informed_fraction < 1`, `|indifference_gap| <= 1e-8`;
- range: `informed_fraction` in `[0, 1]`; `price_informativeness` in `[0, 1]`; all output values finite floats;
- boundary rule: the page's rule for `informed_fraction` equal to 0 or 1 holds on the instance grid;
- cost monotonicity: `informed_fraction` is nonincreasing in `info_cost` on a fixed grid (the builder derives this and the verifier
  checks it; the test is written only if the page states the derivation);
- informativeness formula: `price_informativeness` equals the squared correlation of payoff and price computed from the instance's
  own population moments, to `1e-8`;
- noise response: **no direction is asserted in advance** (§12 Q7); the test checks the report's stated sign against the solver's
  values on the grid only if the page states it;
- independence of the solver from its method: the reference and the five alternatives (§5.5) agree on `informed_fraction` and
  `price_informativeness` within `1e-6` on seeds 0 to 49;
- hard-coded answer detection: values change across seeds 0 to 49 (not one value for all seeds);
- failure messages name the violated property and hint at the concept (for example "the indifference gap should vanish at an interior
  fraction: check the informed-minus-uninformed utility difference"); a failing check **never prints the expected value**
  (`__tracebackhide__` in the helpers, as in E3 §6.7). The collect-only count of the suite is quoted on the page.

**Dual mode.** Identical suite in Pyodide (pytest in Pyodide) and under local pytest; each test under 5 s in Pyodide; the suite under 60 s.

**Integrity.** Never claim the tests are secret. Integrity rests on per-seed instances (BUILDER_RULES §5.3 item 6).

### 5.5 Student-error mutants and alternatives (written by the verifier, not the builder)

**Ten student-error mutants** (verifier writes each as a complete module to `ledgers/E4/mutants/<name>.py`, each docstring's first
line naming the student error; `tools/mutate_graders.py --unit E4 --seeds 0-9` must kill all ten):
1. Informed fraction solved from the uninformed investor's expected utility (the wrong side of the indifference condition).
2. Information cost subtracted in levels, not in the units of the expected utility (the cost's units are wrong).
3. The noise standard deviation used as a variance (`sigma_u` squared once too often, or not squared where it is needed).
4. Price informativeness computed as the price precision (inverse variance) rather than the squared correlation.
5. Bisection with no sign-change check: returns the upper bracket when no root exists (the boundary rule is violated).
6. Search on the open interval with the boundary cases dropped: returns 0.5 when the true fraction is 0.
7. Uninformed investors ignore the price (use the prior only), removing learning from the price.
8. Hard-coded answer for seed 0 (a constant returned for the seed-0 instance).
9. Bisection stopped after a fixed 20 steps with no tolerance check (the indifference gap then exceeds `1e-8` on most instances).
10. Price sign error in the noise term (the noise enters the price with the wrong sign), which changes the informativeness.

The verifier may add one standard-error or wrong-tolerance mutant; those are not counted in the ten. A mutant that differs from the
reference only where the page states nothing is moved to `ledgers/E4/equivalent/` with a README proof (ruling 9).

**Five alternative correct implementations** (verifier writes each to `ledgers/E4/alternatives/alt_<n>.py`; each passes seeds 0 to 49,
ruling 10):
1. Bisection on the informed fraction with the indifference gap (the reference's style).
2. Brent or secant root-finding on the same gap, with a sign-change check.
3. Grid scan on the fraction followed by bisection refinement.
4. Damped fixed-point iteration on the informed fraction with a convergence check.
5. A solver parameterised by precisions instead of variances, with a different bracket and the same outputs.

Each alternative is a float implementation of the same model. The page's exact-rule rule (ruling 10): a float-based alternative that
is wrong on a stated exact rule is a mutant, not an alternative.

### 5.6 Rubric (memo; `both` requires it, `tools/check_projects.py` `rubric_problems`, lines 58 to 72)

Five criteria in one `table.rubric#rubric`, each with four observable levels (level 4 down to level 1). Each level descriptor names
something a grader can see.

1. **Model specification.** States the payoff, the signal, the noise supply, the preferences and the definition of equilibrium, with
   numbered assumptions. Level 4: lists each assumption with a number and states which result uses it. Level 1: "describes the model".
2. **Solver and verification.** States the root-finding method, the bracket, the tolerance and the stop rule. Level 4: reports the
   indifference gap at each reported point. Level 1: "the solver works".
3. **Comparative statics.** Reports how the informed fraction and the informativeness respond to noise and cost, with the sign and
   the grid. Level 4: states each sign as the solver gives it on the stated grid and says which points the sign holds on. Level 1:
   "prices become more informative".
4. **Numerical rigour and rounding.** States the display rule and computes every number from unrounded values. Level 4: names the
   number of significant digits shown and the rule. Level 1: "rounds the numbers".
5. **Limits and evidence.** Names the model's limits (CARA utility, the normal information structure, the single risky asset, the
   exogenous noise supply, price-taking). Level 4: grades every empirical claim, names its registry key or says "no registry key;
   not claimed". Level 1: "notes some caveats".

**Exemplars** at two levels: `exemplar-a` (`data-level="2"`) and `exemplar-b` (`data-level="4"`), excerpts of reports on a SIMULATED
instance, each annotated with the descriptors it meets or misses, with `data-scores` and `data-criterion` as in M1
(`course/modules/M/M1/project.html`). Self-assessment form `section.rubric-self` with `data-rubric="rubric"`
`data-exemplars="exemplar-a exemplar-b"`. The page shows where the student's scores diverge from the exemplar scores. Calibration: the
verifier scores both exemplars blind, within one level per criterion (VERIFIER §2.6).

**Adversarial question bank:** not required (§12 Q15). The report is not an investment-committee defence.

### 5.7 Time budget (`<table id="hours">`, sums to 28 h; every row has a one-line rationale; `tools/check_projects.py` lines 107 to 118)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 1 | One solved SIMULATED instance, annotated line by line (tier M keeps rung 1 minimal) |
| Rung 2, completion problem | 1 | Fill the indifference-gap line, then run the instant check |
| Model derivation: equilibrium, informed-fraction condition, informativeness | 5 | Derive the price map and the two conditions from §5.2, with numbered assumptions |
| `solver.py` and the local test run | 8 | Implement the frozen interface, pass seeds 0 to 49, handle the two named exceptions |
| Comparative-statics grid | 5 | Run the solver on the noise and cost grid the report uses, record the gaps |
| Write-up `report.md` | 5 | Model, method, results, limits, graded claims |
| Self-assessment against exemplars | 3 | Score the report with the rubric, then compare with `exemplar-a` and `exemplar-b` |
| **Total** | **28** | Equals `data-hours-project` on the hub |

---

## 6. Real-data policy

- **No embedded or bring-your-own dataset.** The curriculum names none (`yaml:124-154`). `tools/data_sources.yaml` and the
  three embedded snapshots (`fx_daily`, `fx_monthly`, `ust_daily`, `course/assets/data/market/MANIFEST.json`) are not relevant to this
  model. No DATA_REQUEST is raised, and no MANIFEST entry is added.
- **SIMULATED everywhere data is generated:** the L06 sample check, the L07 seeded check, every instance from `make_instance`, the
  rung-1 worked example, the rung-2 completion instance and the exemplars. Each carries a visible **SIMULATED** label.
- **No `data-files`** on any lab.
- **No figures.** No live figure and no new JS kernel (architect default; §12 Q16). A λ*(c) curve would need a kernel and a test under
  `tests/test_figure_kernels.py` first (BUILDER_RULES §6.4).

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (verified in `references/references.json`; checked by the planner)

| Key | Record (as read) | Curriculum string | Status and use in E4 |
|---|---|---|---|
| `muth1961rational` | "Rational Expectations and the Theory of Price Movements", Econometrica, 1961, volume 29, issue 3 (`references/references.json:17659`); `used_by: ["E4"]` | "Muth (1961), Econometrica 29(3)" (`yaml:144`) | **Matches.** L05 and L06 at paper level; reading list. |
| `milgrom1982information` | "Information, trade and common knowledge", Journal of Economic Theory, 1982, volume 26, issue 1, Milgrom & Stokey (`references/references.json:17291`); `used_by: ["E4"]` | "Milgrom & Stokey (1982), JET 26(1)" (`yaml:146`) | **Matches.** L09 at paper level, only after the abstract is read; reading list. |
| `mascolell1995microeconomic` | Open Library book "Microeconomic theory", 1995, Oxford University Press (`references/references.json:16579`); authors **Mas-Colell only**; `used_by: ["E4"]` | "Mas-Colell, Whinston & Green, Microeconomic Theory (1995)" (`yaml:143`) | **Conflict (B3).** Cite the key only, with no co-author names, or do not cite. Not in the reading list while B3 is open. |

**Keys in the registry that E4 must not cite** (not curriculum-listed for E4, or a different paper): `grossman1980takeover`
(`references.json:11099`, Grossman & Hart, used by CF5; not the 1980 AER paper, B1); `milgrom1982theory` (`used_by` E2; Milgrom & Weber);
`rothschild1976equilibrium` (E2); `kyle1985continuous` (MS1); `lucas1978asset` (AP3); `harrison1979martingales` (AP1).

### 7.2 REFERENCE_REQUESTS (lead only; no bibliographic record typed by the planner)

- **R-E4-1 (blocking attribution in L08 and the project reading list).** {doi: null, authors: "Grossman and Stiglitz (lead only, from
  `yaml:145`)", year: "1980 (curriculum string)", title: "On the Impossibility of Informationally Efficient Markets (curriculum string)",
  venue: "American Economic Review, volume 70, issue 3 (curriculum string; record not typed)", needed_for: "L08 attribution of the
  paradox and the model, and the project's reading list", confidence: "the curriculum string exists; the registry has no record (B1);
  the review-queue candidates are different articles (`review_queue.json:109-135`) and must not be admitted". Resolution: the architect runs
  `tools/add_reference.py` by DOI after the identity check.
- **R-E4-2 (needed only if L09 keeps a general claim graded B).** {doi: null, authors: "not typed", year: "not typed", title: "empirical
  evidence on speculative trade and common priors (topic only)", venue: "not typed", needed_for: "two-sided treatment of the general
  no-trade claim (BUILDER_RULES §2.5)", confidence: "the need is certain; no record identified by this planner". Default: remove the
  general claim, keep the finite-model theorem (T).
- **R-E4-3 (needed only if any empirical sentence about rational expectations or price informativeness is kept).** {doi: null,
  authors: "not typed", year: "not typed", title: "empirical evidence on rational expectations and on the informativeness of prices
  (topic only)", venue: "not typed", needed_for: "counter-evidence for a B or C claim", confidence: "the need is certain; no record
  identified". Default: no empirical claim is made in E4.

No request is raised for Arrow and Debreu's own papers or for an existence theorem: the curriculum names neither (`yaml:124-154`)
and the plan does not cite them. Attribution to them is not used.

The architect resolves each request through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page;
`references/authorities.yaml`; BUILDER_RULES §2.4). Until then the lessons teach the models by derivation, the paradox as a model
result, and each empirical sentence is removed or graded C with its basis named.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for E4 (§0.1: no `atlas:` key at `yaml:124-154`; no Atlas entry names E4). No
`atlas/E4.contract.md` is needed. `check_projects.py` skips the contract check when the project names no `atlas` key
(`tools/check_projects.py` lines 122 to 146, E3 §12 item 1 precedent).

---

## 9. Cards builder (Builder F, after A to E)

- `course/modules/E/E4/cards.json`, ids `E4-c001` upward (sequential ids are not required, architect ruling 2), `lesson` in L01 to
  L09. One card per definition, theorem statement, key formula, key result and misconception (BUILDER_RULES §7).
  `check_pages.py` `check_cards` (line 366) checks the id prefix, the lesson existence, the grades and the registry keys.
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example
  `"basis": "Lab 3, Derivation 2 (exact)"`.
- Cite a registry key only for an attributed claim (`muth1961rational` on L05 and L06; `milgrom1982information` on L09 only after the
  abstract is read). `cite` is `[]` where the card is a model result.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`. No card cites the Grossman–Stiglitz paper (B1).

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit E4            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit E4
.venv/bin/python tools/check_projects.py --unit E4
.venv/bin/python tools/run_labs.py --unit E4               # --page L08 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/E/E4/L01.html                          # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/E/E4/L08.html --refresh lab-E4-L08-1   # after editing a twin
.venv/bin/python tools/run_graders.py --unit E4 --seeds 0-49                               # after grader files exist
.venv/bin/ruff check tests/labs/E4 course/modules/E/E4/grader && .venv/bin/ruff format --check tests/labs/E4
.venv/bin/mypy tests/labs/E4 course/modules/E/E4/grader                                     # strict, repository configuration
```

Verifier only, on a quiet machine: `.venv/bin/python tools/mutate_graders.py --unit E4 --seeds 0-9` (the ten mutants, §5.5),
`.venv/bin/python tools/ledger.py --unit E4 --check` (after fragments exist), `.venv/bin/python tools/page_smoke.py --unit E4`
(timing-sensitive; not run by builders), and `.venv/bin/python tools/verify_refs.py --unit E4` (the unit ledger's registry run,
VERIFIER §2.1).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`,
and the full gate in CLAUDE.md. `tools/fetch_data.py --check` is not needed (no dataset).

Flags checked by the planner in the tool sources: `check_pages.py` (`--unit`, `--all`, `--page`), `check_dag.py` (`--unit`,
`--all`), `check_projects.py` (`--unit`, `--all`), `run_labs.py` (`--unit`, `--all`, `--page`), `run_graders.py` (`--unit`, `--all`,
`--seeds`, default 0 to 49), `mutate_graders.py` (`--unit`, `--all`, `--seeds`, default 0 to 9; line 42 enforces three mutants
minimum), `ledger.py` (`--unit`, `--check`). The planner did not execute these commands.

---

## 11. Tooling assumptions that do not hold for E4 (flagged)

1. **No Atlas milestone.** No `atlas:` key on E4 (`yaml:124-154`); no Atlas entry names E4. `check_projects.py` skips the contract
   check (lines 122 to 146). No `atlas/E4.contract.md` is drafted.
2. **No debate.** E4 has no `debate:` key, so `check_pages.py` `check_unit` (line 412) does not require a debate brief. The
   attribution and the paradox are contested in the literature, so the two-sided rule (BUILDER_RULES §2.5) applies anyway.
3. **Two grading modes.** `grading: both` requires the grader panel, the autograder words, the rubric and two exemplars at two
   levels (`check_projects.py` lines 122 to 139; `GRADING_WORDS` line 38; `rubric_problems` lines 58 to 72).
4. **Ten mutants and five alternatives are not enforced by a tool.** `mutate_graders.py` enforces three mutants (line 42); the ten
   and the five are verifier duties recorded in the ledger's `mutants` list.
5. **One curriculum lab, nine twins.** The curriculum names one lab (`yaml:147`). The plan adds one lab per lesson (E3 precedent) and
   three project labs. The curriculum lab is `lab-E4-L08-1` (§1).
6. **Prerequisite pages are built** (E1, E2, E3, M1 to M7). The hub and lessons still link prerequisite concepts through
   `concepts.html` anchors only (BUILDER_RULES §4.1), not through E2 or E3 hub pages.
7. **`check_dag` sees linked uses only.** Unlinked names of out-of-closure concepts (§4) pass the tool. The verifier reads every
   lesson and the project for them.
8. **Labs must be exact or stated-precision.** Standard library only. Float results print their rounding rule and, where a lab compares
   with an exact value, an error column.
9. **No tool checks the economics.** Nothing in `tools/` checks the equilibrium, the indifference condition or the Bayes steps. The labs,
   the grader's oracle and the verifier do (VERIFIER §2.4, §2.5).
10. **Registry strings.** Two of the four curriculum sources match their records (`yaml:144`, `yaml:146`). The Mas-Colell record
    conflicts on authors (B3). The Grossman–Stiglitz string has no record (B1). `check_pages.py` checks only that each key is verified;
    the identity check is the verifier's (VERIFIER §2.1).

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **Lesson count and hours.** RECOMMENDED: 9 lessons × 8 h = 72 h and a 28 h project (28%). Alternative within the rules: 8 lessons ×
   9 h and a 28 h project (then one lesson must carry two concepts, and the §1 table changes). Hours stay as declared once set (HOURS
   ruling).
2. **File ownership.** RECOMMENDED: Builder A owns L01 to L03 and the hub; B owns L04 and L05; C owns L06 and L07; D owns L08 and L09;
   E owns the project, grader and project labs; F owns cards. The spread of 3, 2, 2, 2 is the closest split of nine lessons to the
   brief's "about three per builder" that the hour rule allows (§1).
3. **D1, Bayesian inference (S1).** RECOMMENDED: Bayes' rule as a quotient of probabilities and posteriors as conditional distributions
   (M4 `conditional-expectation-elementary`), plain prose, no S1 link. Alternative: add S1 as a prerequisite of E4 (a curriculum change,
   not proposed).
4. **D2, state prices (AP1).** RECOMMENDED: E4 uses "Arrow–Debreu security price vector" and never "state price"; AP1 owns the term.
   Confirm that E4 defines no AP1 concept.
5. **Project model (B2).** RECOMMENDED: the CARA-normal one-risky-asset noisy rational-expectations model of §5.2, with `solver.py`
   exposing `solve_model(noise_sd, info_cost)`. The curriculum names no model (`yaml:150-152`). Decision needed before the project is built.
6. **Informativeness measure.** RECOMMENDED: the squared correlation between payoff and price (`\Corr(v,p)^2`, M4 `correlation`) as
   the single measure of price informativeness, and the informed fraction as the second output. No other measure.
7. **Noise and cost responses.** RECOMMENDED: no sign is asserted in advance. The report states the sign that the derived formula gives,
   and the verifier confirms it numerically on the grid. The cost monotonicity test (§5.4) is written only if the derivation states it.
8. **Boundary rule for the informed fraction.** RECOMMENDED: `informed_fraction = 0` when the informed investor's net benefit is
   nonpositive as the fraction tends to zero; `= 1` when it is nonnegative at one; interior otherwise. The page states the rule; no
   exception is raised.
9. **Solver interface (freeze before building).** RECOMMENDED: `solve_model(noise_sd: float, info_cost: float) -> dict[str, float]`
   with exactly the three keys of §5.2; `ValueError` only for the two conditions of §5.4 (precedent E3 Q4 and §6.3 of E3).
10. **Mutant count and location.** RECOMMENDED: the ten mutants of §5.5 under `ledgers/E4/mutants/`, with the verifier's optional extra
    mutant not counted; equivalents under `ledgers/E4/equivalent/` with README proofs (ruling 9).
11. **Alternatives.** RECOMMENDED: five alternatives under `ledgers/E4/alternatives/`, each passing seeds 0 to 49 (ruling 10). This
    satisfies the fixer rule's minimum of three. If the suite exceeds 60 s in Pyodide, the seeds window is the architect's call (E3
    used 0 to 9, ruling 10).
12. **Mas-Colell record conflict (B3).** RECOMMENDED: cite the key with the registry's own fields only, or do not cite. Do not put the
    three-author string in prose. The architect may correct the curriculum string or the record through the registry tools; builders
    never edit the record.
13. **Grossman–Stiglitz admission (B1).** RECOMMENDED: the architect admits the paper by DOI through `tools/add_reference.py` after the
    identity check against the title, authors, year and volume in `yaml:145`. Until then L08 teaches the model result and states the
    attribution as "not cited" with the page-level basis. This blocks attribution only.
14. **Bisection assumption (D4).** RECOMMENDED: state the sign-change and continuity condition as a numbered Assumption, and do not name the
    intermediate value theorem (M5 is outside the closure). Alternative: add M5 as a prerequisite (a curriculum change, not proposed).
15. **Adversarial question bank.** RECOMMENDED: none. The report is not an investment-committee defence or a debate.
16. **Figures.** RECOMMENDED: none in E4. A figure of the informed fraction against cost would need a kernel and a test first.
17. **CARA utility and other plain terms.** RECOMMENDED: CARA utility, "noise traders", "informationally efficient", "posterior",
    "common knowledge" and "Walras' law" are plain `<dfn>` terms with no `data-concept` (E1 and E3 precedent). No glossary request.
18. **Incomplete-market efficiency claim (L04).** RECOMMENDED: remove the consequence that equilibrium need not be efficient under
    incomplete markets, unless the builder proves it on a stated finite example. No registry source is needed for it.
19. **SIMULATED labelling.** RECOMMENDED: as §2.2 and §6. Exact population formulas are not labelled SIMULATED.
20. **Scope.** RECOMMENDED: competitive price-taking; one risky asset in the project; static and two-date settings; finite-state labs; the
    CARA-normal model for L08 and the project; no general-existence claim. Confirm (§2.1 item 4).
21. **Neither a Lagrangian nor a Bellman recursion is needed beyond M7.** RECOMMENDED: use M7 `lagrange-multiplier` and `kkt-conditions`
    only where the budget problem needs them (L02); no dynamic programming.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01 to L03 (with the hub), L04 to L05, L06 to L07, L08 to L09 (includes
   the curriculum lab `lab-E4-L08-1`), the project (the rubric and exemplar calibration, the ten mutants and five alternatives, and the
   grader's runs), and the cards. Failing rows return to the owning builder, with only the failing rows.
3. Ledger at `ledgers/E4.verification.json`, built from fragments under `ledgers/E4-<slice>.json` (`tools/ledger.py --unit E4 --check`).
   Verifier scripts are archived under `ledgers/E4/scripts/` (VERIFIER §3). Mutants under `ledgers/E4/mutants/`, alternatives under
   `ledgers/E4/alternatives/`, equivalents under `ledgers/E4/equivalent/`.
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 and B2 must be resolved, or
   named as honest gaps, first. B3 is a named gap if it stays open.

Architect decisions: pending (§12). This plan is the planner's proposal. Where a question has a RECOMMENDED decision, that decision
is the default that the builders follow until the architect says otherwise.

## Architect decisions (2026-11-03, binding). Where the plan states a recommendation for an open question, follow it. Defaults for every module: concepts outside the prerequisite closure are plain prose with no link and no dfn; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields only or not at all (never edit a record, never type bibliographic data); no real data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST in plans/<UNIT>-open-items.md; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every grader; not adversarial, no question bank. plans/FINAL-ARCHITECT-RULINGS.md and ~/.fanout/fixer-rules.md bind every builder. No reference is admitted in this batch: a statement whose source is a REFERENCE_REQUEST is not made, or it is taught as a model result with no attribution.
Module specifics: 9 lessons x 8 h + 28 h project; builders A: L01-L03 and index; B: L04-L05; C: L06-L07; D: L08-L09; E: project and grader; F: cards. The project model is the CARA-normal noisy rational-expectations model with solve_model(noise_sd, info_cost) as the plan proposes; the paradox is taught as a model result and Grossman and Stiglitz is not cited. Bayes' rule is used without linking S1; Arrow-Debreu security price vector is the term (state price belongs to AP1); the bisection continuity is a numbered Assumption.
