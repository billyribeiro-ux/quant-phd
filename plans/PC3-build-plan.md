# PC3 build plan: Quant & Finance Interviews (planner draft)

Unit: **PC3 · Quant & Finance Interviews** · tier U · 50 h · prerequisites M4, CS2, FC2 · no Atlas milestone · no debate ·
grading `both` (autograder for the game log and policy, rubric for the post-game analysis) · output directory
`course/modules/PC/PC3/` (part code `PC`) · lab twins `tests/labs/PC3/` · cards `course/modules/PC/PC3/cards.json`.
Planner: Haiku, plan only. No lesson text, no git operations, no commits. Only this file was written. Executors: Haiku builders,
then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every curriculum statement cites `file:line` read during planning. Anything not in the curriculum is
marked **NOT IN CURRICULUM**. Tool-behaviour statements cite the tool source line that was read. Locators marked
"carried" were taken from `plans/E5-build-plan.md` or `plans/FC2-build-plan.md` and were not re-read by this planner.

Status: `course/modules/PC/` does not exist and `ledgers/PC3*` does not exist. Nothing is built. **Two blocking items exist
(§0.3, B1 and B2). The curriculum hours and the registry sources are feasible. No dataset is needed.**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part PC, code `PC`, title "Professional Craft", order 23 | `curriculum/06-profession-capstone.yaml:88-89` |
| PC3 id `PC3`, title "Quant & Finance Interviews", tier `U` | `curriculum/06-profession-capstone.yaml:157-159` |
| Hours `50` | `curriculum/06-profession-capstone.yaml:160` |
| Prereqs `[M4, CS2, FC2]` (only) | `curriculum/06-profession-capstone.yaml:161` |
| Core: "Probability puzzles, expected-value and market-making games, mental math, coding under time pressure, technical finance questions, case interviews." | `curriculum/06-profession-capstone.yaml:162-164` |
| `introduces` has 5 concepts: `expected-value-game`, `market-making-game`, `fermi-estimation`, `timed-coding-interview`, `case-interview` | `curriculum/06-profession-capstone.yaml:165-170` |
| Sources: two free-text strings: "Zhou, A Practical Guide to Quantitative Finance Interviews (2008)"; "Crack, Heard on the Street, 16th ed. (2015)" | `curriculum/06-profession-capstone.yaml:171-173` |
| Lab: "Timed probability drill set with spaced repetition." | `curriculum/06-profession-capstone.yaml:174` |
| Project "Market-making game"; brief: play the in-page market-making game against scripted counterparties with hidden information, and write a post-game analysis of edge and inventory risk | `curriculum/06-profession-capstone.yaml:175-180` (title 176, brief 177-180) |
| Deliverable "Game log plus analysis."; grading `both` | `curriculum/06-profession-capstone.yaml:181-182` |
| No `debate:` key on PC3 | `curriculum/06-profession-capstone.yaml:157-182` (absent) |
| No `atlas:` key on the PC3 project; no atlas entry names PC3 (computed by reading the `atlas` array in `curriculum.json`) | `curriculum/06-profession-capstone.yaml:175-182`; `curriculum/curriculum.json` `atlas` |
| JSON row for PC3 | `curriculum/curriculum.json:11471` (`"id": "PC3"`), `"part": "PC"` |
| The five PC3 concepts are owned by PC3 (`concept_owner`, computed) | `curriculum/curriculum.json` `concepts`; `tools/coursekit.py:235-236` |
| PC3 is required by the bachelor's credential BS-FIN | `curriculum/meta.yaml:63` |
| PC3 is in the course map "Careers & Technical Interviews" (Finance major) | `curriculum/meta.yaml:91` |
| STUDIO-PC requires PC2 only (PC3 is not a studio requirement) | `curriculum/06-profession-capstone.yaml:91-94` |
| Topological position 50 of 134; after CS2, M4, PC1, FC2 | `curriculum/curriculum.json` `topological_order` (computed) |

### 0.2 Prerequisite closure (computed) and the nearest built prerequisite

`tools/coursekit.py` `prerequisite_closure("PC3")` (run by the planner through `.venv/bin/python`; `coursekit.py:239-249`):

**{AC1, CF1, CS1, CS2, E1, FC1, FC2, M1, M2, M4, P0.1}** (11 modules; 141 usable concepts from their `introduces`).

Built status (planner check of `course/modules/`): AC1, CF1, CS2, E1, FC1, FC2, M1, M2, M4 are built; **CS1 is not built**
(`course/modules/` has no `CS/CS1`). `coursekit.built_units()` lists CS2 and FC2 among the built units.

Nearest built prerequisite: **FC2** (`plans/FC2-build-plan.md`, read in full). Reason, computed: FC2's closure is
{AC1, CF1, E1, FC1, M1, M2, M4, P0.1} (8 of PC3's 11 closure modules, plus FC2 itself), against CS2's closure
{CS1, M1, P0.1} (3 modules). M4's closure is {M1, M2, P0.1}. The FC2 plan's layout is the nearest precedent for a
finance unit with a `both` project. The CS2 plan (`plans/CS2-build-plan.md`) is the precedent for the coding content only;
the planner did not read it in full and makes no claim from it.

### 0.3 Blocking issues (architect decision required before builders start)

**B1. The brief says "play the in-page market-making game", and the static site has no play interface.**
- `curriculum/06-profession-capstone.yaml:177-180` requires play against scripted counterparties with hidden information.
- BLUEPRINT §5.1 and §6 (the Pyodide in-page workspace) allow Python in the page. The architect default for every module
  is "no figures or new JS kernels" (`plans/E5-build-plan.md`, architect-decisions block, carried precedent; the FC2 plan
  §0 cites the same default).
- A turn-by-turn clickable game would need a new JS kernel with tests (BUILDER_RULES §6.4).
- **Plan's default (recommended, for the architect to confirm or replace):** the game is a deterministic Python engine
  (`grader/engine.py`) that runs in Pyodide. The student writes `market_maker.py` (a function `quote(state)` that returns a
  bid, an ask and a size for each turn). The page runs the engine for the workspace seed and writes `game_log.json`. The
  student writes `replay(log)`, in the same `market_maker.py`, to replay the log and compute cash flow, inventory and mark-to-market P&L. The post-game analysis
  is `analysis.md`. Play is by code, not by clicking. The project spec says so on its first line.

**B2. "Timed" in the lab and in the coding lesson needs a timer, and the static pages have none.**
- `curriculum/06-profession-capstone.yaml:174` ("Timed probability drill set") and `:163` ("coding under time
  pressure").
- **Plan's default:** no JavaScript timer and no new kernel. The timed element is a stated time budget per item
  (for example 60 seconds), kept by the student's own clock, plus a lab that counts answers and correct answers
  deterministically. The page says so. Architect confirms (Q4).

Non-blocking, but the architect should see them:

- **B3. Hidden information cannot be enforced by a log-based grader.** The fair-value path is generated from the seed, so a
  student who reads `grader/instance.py` can see it. A static site cannot keep its tests secret (BUILDER_RULES §5.3 item 6;
  BLUEPRINT §5.2). The page states this as a KNOWN LIMITATION. No grader test is written for "did not use hidden
  information". Mutants that need it are excluded (§5.6).
- **B4. Registry edition strings.** The curriculum string "Crack, Heard on the Street, 16th ed. (2015)"
  (`curriculum/06-profession-capstone.yaml:173`) has no edition in the registry record `crack2015heard`
  (`references/references.json:6222`, year 2015). The record for `zhou2008practical` (`references/references.json:23402`)
  carries a publisher string "Lulu,]" with a stray bracket. Builders cite the keys only, with no edition and no
  publisher typed in prose (the E5 B4 precedent; registry records are never edited).

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

**6 lessons × 6 h = 36 h; project 14 h; total 50 h.** Project share 28% (inside the 10–40% rule, `tools/check_pages.py:339-340`).
Each lesson is 6 h, inside the 6–12 h rule (`tools/check_pages.py:221-228`).

| Lesson | Title (working) | Concept it defines (`introduces`, `yaml:165-170`) | Lab twin id (`tests/labs/PC3/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Fermi estimation and mental math | `fermi-estimation` | `lab-PC3-L01-1`: the product of stated factor ranges, exact bounds in `Fraction`, the width of the log-error interval | 6 | Builder A |
| L02 | Probability puzzles and conditional reasoning | none (curriculum core text only) | `lab-PC3-L02-1` (**the curriculum lab**, `yaml:174`): a seeded timed-drill set of 12 items, each answer computed by exact enumeration, the score printed | 6 | Builder A |
| L03 | Expected-value games | `expected-value-game` | `lab-PC3-L03-1`: the exact expectation of a multi-stage game by enumeration; a stopping-rule comparison on a finite truncation | 6 | Builder A |
| L04 | Market-making games and inventory risk | `market-making-game` | `lab-PC3-L04-1`: the game engine on seed 0 with a fixed quoting rule; the cash, inventory and P&L identity checked exactly; labelled SIMULATED | 6 | Builder B |
| L05 | Timed coding interviews | `timed-coding-interview` | `lab-PC3-L05-1`: sliding-window maximum by a monotonic deque and by a naive scan on one seeded sequence; the outputs equal, the operation counts printed | 6 | Builder B |
| L06 | Technical finance questions and case interviews | `case-interview` | `lab-PC3-L06-1`: one forward-price check and one case cash-flow calculation in `Fraction`, the net present value rounded only at display | 6 | Builder B |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 36/14 | none | none | none | Builder A |
| project | Market-making game (`both`, §5) | none | `lab-PC3-project-1` (rung 1), `lab-PC3-project-2` (rung 2, `class="lab completion"`), `lab-PC3-project-3` (rung 3 check) | 14 | Builder C |
| grader | `grader/engine.py`, `instance.py`, `reference.py`, `starter.py`, `test_project.py` | none | none | none | Builder C |
| cards | `cards.json` from L01–L06 | none | none | none | Builder F (after A–C) |

Ownership, as the rule "about three lessons per builder" requires: **Builder A** owns L01, L02, L03 and `index.html`.
**Builder B** owns L04, L05, L06. **Builder C** (the last builder that writes files) owns `project.html`, the grader directory
and the three project labs. Builders D and E have no files in this unit (six lessons at 6 h cannot be split across five
builders without fragmenting the lesson sequence). **Builder F** owns `cards.json`. The architect may request a different
split (Q14).

Ordering (no lesson links a concept defined in a later lesson; `check_dag.py` checks linked uses, §4):
- L01 uses only prerequisite concepts (M1 `exponential-and-logarithm`, `compounding-frequency` in prose; M2 `taylor-theorem`
  for the bound on a product of ratios, in prose; M4 `random-variable` for the factor ranges).
- L02 uses M4 `random-variable`, `expectation`, `independence` and `conditional-expectation-elementary` (its definition
  is at `course/modules/M/M4/L04.html:139`). Bayes' rule is derived in L02 from that definition (§4, D1).
- L03 uses L02 (conditional reasoning) and M4 `expectation`, `variance`.
- L04 uses L03 (`expected-value-game`) for the expectation of a fill, FC1 `market-maker` (linked), FC1 `bid-ask-spread`
  (linked), FC1 `limit-order-book` (linked, in prose), and M4 `expectation` for the P&L identity.
- L05 uses CS2 `monotonic-deque`, `big-o-complexity`, `hash-map`, `binary-heap` and CS1 `unit-test` (all linked, all in the closure).
- L06 uses FC2 `forward-contract`, `cost-of-carry-forward-price`, CF1 `net-present-value` (all linked), and L01 (`fermi-estimation`).

Hours check: 6 × 6 = 36 (hub `data-hours-lessons="36"`); project 14 (hub `data-hours-project="14"`); total 50.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to PC3)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3–§8, `plans/FC2-build-plan.md` (its Architect decisions are
binding precedent), `plans/E5-build-plan.md` (its rules §2.1 are carried below), this file. Study `course/modules/FC/FC2/`
for the layout and the hub and project grammar. `course/templates/` holds the four skeletons (hub, lesson, project, studio).

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) and rounded
   only at display, with the rule stated on the page. This covers every probability, expected value, bound, NPV and
   P&L figure.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only
   what the printed numbers show. Never type an expected output; `tools/embed_labs.py` fills it.
3. **Attribute nothing unread.** Only the two registry keys in §7 may be cited, at book level, with no page, problem, edition
   or chapter typed in prose. The planner did not read either book. A problem, an answer or a number "from Zhou" or "from
   Crack" is a fabrication and fails the unit. The reading list names the books only.
4. **Scope words need a computation.** "every", "all", "never", "always", "any", "same", "only" are used only where a proof,
   a finite enumeration or a lab computes the claim. Examples the builders must check: "every fill is at the quote" (true by
   the engine's rule, a test asserts it); "the engine never reveals the fair value" (false as a claim about code; do not
   write it, see B3).
5. **Define before use.** Each of the five curriculum concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its
   assigned lesson, never earlier. Terms outside the five concepts (Bayes' rule, the Fermi factor, the fair game, inventory,
   the spread, the mark-to-market P&L, the stopping rule, the case framework) are defined in prose at first use with a plain
   `<dfn>` and no `data-concept` (`tools/check_dag.py:45-48` skips a `<dfn>` without `data-concept`).
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation lists its numbered Assumptions (A1, A2, …)
   before the statement. Examples: the expectation of a sum needs finite expectations; Bayes' rule needs P(B) > 0; the
   fair-game definition needs a finite game with a finite number of turns.
7. **Grader rule.** The grader rules of BUILDER_RULES §5.3 apply in full (§5.3–§5.6 of this plan).
8. **Money.** Every money value in the game, the log, `replay` and any prose figure is an integer number of cents (`int`
   in Python). Expected values in the labs are `Fraction` in cents, rounded half up once, at display, with the rule stated.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own
   container; no element forces the page wider than 360 px.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no
    `if __name__ == "__main__":` guard. `tools/run_labs.py:50-60` runs each twin as `python -I -W error <twin>` with no network.
11. **Learner text avoids process words.** Fixer-rule 14 bans "build", "builder", "round", "verifier", "REQUESTS" and "unit
    report" in learner text. The game's time index is therefore called a **turn** everywhere in learner text, and `N` is the
    number of turns. The word "round" appears only in code that does not reach the page prose, and the builders avoid it
    there too.
12. **Scope of the game claims.** The game is a model. A lesson or the project never states that a result holds for real
    market makers. Model limits are named in "Where the canon breaks".

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. The unit has no
  empirical claim about interview practice (which firms ask what, how often, how long). **Such claims are not written.** If
  a lesson wants one, it is grade D, flagged "It is widely claimed", and the page says there is no systematic evidence.
  The planner recommends none.
- Concepts: §1 table. `<dfn>` only for the five registered concepts; plain `<dfn>` for other terms (§2.1 item 5).
- Prerequisite links: `href="../../../concepts.html#<id>"` for any concept in the closure (AC1, CF1, CS2, E1, FC1, FC2, M1,
  M2, M4, P0.1; `course/modules/PC/PC3/` is three levels below `course/`). `href="Lnn.html#def-<id>"` for an earlier PC3
  lesson. A lesson never links a concept defined in a later lesson. Concepts outside the closure are plain prose, no link,
  no `<dfn>` (§4).
- Labs: code lives once in `tests/labs/PC3/lab-PC3-Lnn-1.py` (and `lab-PC3-project-1..3.py`). The page carries
  `@@LAB:<file>@@` and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Lab ids match `lab-PC3-<page>-<n>`
  (`tools/check_pages.py`, lesson check). Standard library only (`fractions`, `math`, `random.Random(seed)`, `dataclasses`,
  `collections`); seeded RNG only; no network; under 10 s in Pyodide; no warnings (`-W error`).
- SIMULATED label: on every lab or figure that uses generated game instances (L04, the project's worked example and
  check). The drill items of L02 and the sequences of L05 are generated items, labelled "generated" with the seed.
  No lab uses real data (§6).
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Banned strings (`tools/check_pages.py:58-72`, BANNED): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the
  scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well
  known", "obviously", "clearly", and any three-dot ellipsis outside code.
- Problem sets (BUILDER_RULES §4.2 item 7): at least three problems in each of the Mechanics, Proof, Empirical and Research
  tiers, per lesson, each with a full worked solution inside `<details class="solution">`. For PC3 the Empirical tier uses
  generated instances labelled SIMULATED, and the Research tier is an open design question with a stated criterion. The
  builders report the count per lesson. This is 72 problems in total; it is the largest workload in the unit.
- Misconceptions: at least three per lesson. Retrieval quiz: 8–15 items per lesson, each with an explanation read against
  its lesson (precedent: CF1 KNOWN 6).
- "Checked" or "verified" claims name the lab, the line or the test that did the check.
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10
  output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered macros this unit may use: `\E` (expectation operator), `\Prob`, `\Var`, `\indic` (indicator), `\R` (real numbers),
`\Normal` (normal distribution). Registered symbols this unit must not give another meaning:

| Registered symbol | Registered meaning | PC3 rule |
|---|---|---|
| `T` (S1) | number of return observations | **Not used.** The number of turns is `N`, a local symbol defined in L04 (`N` is local per `notation.json` `about`). Time index `t`. |
| `\Phi`, `\Phi^{-1}` (M4) | standard normal CDF and quantile | Not used. |
| `\gamma_3`, `\gamma_4` (M4) | skewness, kurtosis | Not used. |
| `R^\ast`, `R^{e\ast}`, `R_f` (AP1) | SDF return, projection, gross riskless return | Not used. No risk-free rate appears in PC3. |
| `\mathbb{Q}` (AP1) | risk-neutral measure | Not used. The binomial in FC2 is not repeated. |

Local symbols (defined on the lesson where first used, never redefined): `N` (turns), `t` (turn index), `v_t` (the hidden fair
value in cents), `b_t`, `a_t` (bid and ask in cents), `q_t` (quoted size in units), `I_t` (inventory in units), `C_t` (cash in
cents), `L` (inventory limit), `Q` (maximum quoted size), `p` (a probability of an arrival). `\pi` is not used (E5 uses it for inflation).
NOTATION_REQUESTS: none.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2): why it matters (at most 120 words); core content
in numbered sections of Definition, Theorem, Proof, Example and Remark blocks; the inline lab; where the canon breaks;
misconceptions (at least three); the problem set; the key-results table; the retrieval quiz. No debate brief (no `debate` key,
§0.1).

- **L01 Fermi estimation and mental math** (`fermi-estimation`). Decompose a quantity into a product of factors; state each
  factor as a range; the product's bounds are the product of the factor bounds when every factor is positive (T, a monotone
  product of positive ranges; proof on the page). The log-error of a product is the sum of the factor log-errors
  (`exponential-and-logarithm`, M1). A mental-math bound on `(1+x)^n` for small `x` uses the Taylor remainder (`taylor-theorem`,
  M2; the remainder bound is derived on the page, with Assumption A1: `x` in a stated interval). Every number comes from
  stated factor ranges (no data). Where the canon breaks: a product of many factors with correlated errors. Lab: the bound
  table, exact in `Fraction`. Misconception: "a more precise factor makes the answer more accurate" (it does not, if the
  other factors are rough). No empirical claim.
- **L02 Probability puzzles and conditional reasoning** (no curriculum concept). Sample spaces for finite experiments; events;
  conditional probability defined from the joint distribution, consistent with M4 `conditional-expectation-elementary`
  (`course/modules/M/M4/L04.html:139`); Bayes' rule as a one-line consequence (plain prose, D1, §4); the two-child problem,
  a symmetry argument and a counting argument. Each puzzle's answer is derived (T) and checked by exact enumeration in the lab.
  Where the canon breaks: a puzzle whose wording fixes the sampling rule decides the answer (the assumptions must be written
  out). The curriculum lab (`lab-PC3-L02-1`) is the timed drill set: twelve generated items with exact answers. Misconception:
  "the answer is 1/2 by symmetry" when the sampling rule is not symmetric. No claim about how people answer these puzzles.
- **L03 Expected-value games** (`expected-value-game`). Expected value of a payoff; linearity of expectation over a finite
  sum (`expectation`, M4; Assumption: finite expectations); a game is **fair** when its expected payoff is zero (a definition,
  plain prose); a multi-stage game's expectation by backward induction on a finite tree; a stopping rule that depends on the
  outcomes so far, and the fact that such a rule can change the expected payoff of a fair game. The stopping result is
  shown on a finite truncation in the lab (exact, grade T for the finite case). No martingale language (D2, §4).
  Where the canon breaks: infinite games and unbounded stopping; the lesson's claims stop at finite truncations.
  Lab: exact expectation of a multi-stage game by enumeration; the stopping comparison with the truncation stated.
- **L04 Market-making games and inventory risk** (`market-making-game`). The game's rules, defined once here and restated
  in the project. Rules in integer cents: `N = 20` turns; fair value `v_0 = 10000`; each turn the fair value moves by
  `+5` or `−5` cents with probability 1/2 each (hidden); each turn the maker posts a bid `b_t` and an ask `a_t` with `b_t < a_t`,
  and a size `q_t` in `{0, …, 5}`; then one arrival: with probability 1/2 an uninformed order of one unit (buy or sell,
  probability 1/2 each), otherwise an informed trader arrives; an informed trader buys one unit at the ask if `v_t > a_t` and
  sells one unit at the bid if `v_t < b_t`, and otherwise does nothing. A fill happens only if the quoted size is at least
  one and the inventory limit `|I| ≤ L = 10` is not breached. Cash and inventory update as in §5.2. The P&L at the end is
  `C_N + I_N × v_N` (cents, exact). The model is a discrete-time model with one asset and a fixed tick; the lesson states
  that the arrival probabilities are assumptions (A1–A3), not estimates. Where the canon breaks: adverse selection (E2's
  concept, plain prose, D3) and the single-asset, no-latency model. Lab: the engine on seed 0 with a fixed symmetric rule;
  the identity `P&L = cash flow + inventory mark` checked exactly; labelled SIMULATED.
- **L05 Timed coding interviews** (`timed-coding-interview`). Interview coding: complexity budgets (CS2 `big-o-complexity`),
  choosing a structure (`hash-map`, `binary-heap`, `monotonic-deque`), stating the edge cases before writing code, and
  checking the code on small cases with `unit-test` (CS1). The lesson states what the answer costs and does not claim how
  long an interview allows. Lab: sliding-window maximum by a monotonic deque and by a naive scan on one seeded sequence; the
  outputs are equal; the operation counts (not wall-clock time) are printed. Where the canon breaks: an operation count is
  not a runtime.
- **L06 Technical finance questions and case interviews** (`case-interview`). Technical finance questions restricted to
  the closure: forward prices (`cost-of-carry-forward-price`, FC2), put–call parity (FC2 `put-call-parity`), net present value
  (CF1 `net-present-value`), accounting identities (AC1 `statement-articulation`). The case framework: restate the question,
  state the assumptions, size the market or the cash flows with a Fermi estimate, compute, and state a recommendation with its
  sensitivity. Lab: one forward-price check and one case cash-flow calculation in `Fraction`, the NPV rounded only at display.
  Where the canon breaks: a case answer is only as good as its assumptions, and the lesson names the ones it uses.
  CAPM, duration and DCF questions are excluded by default (§4, D6).

Lesson-level constraint: each lesson's "Where the canon breaks" names at least one model limit and what changes without it.

---

## 4. DAG problems (concepts natural PC3 content would use outside the closure)

Prerequisite closure of PC3: **{AC1, CF1, CS1, CS2, E1, FC1, FC2, M1, M2, M4, P0.1}**, 141 usable concepts (computed).
Owners below are from `curriculum/curriculum.json` `concepts` (computed with `concept_owner`).

| Ref | Concept(s) (owner) | Where natural PC3 content would use it | Resolution in this plan |
|---|---|---|---|
| D1 | `bayesian-inference` (S1, name "Bayesian inference (prior, likelihood, posterior)"); Bayes' rule is not a registered concept | Bayes' rule in L02, the posterior reasoning in L04 (what an informed order reveals) | Bayes' rule derived in L02 from M4 `conditional-expectation-elementary` (conditional distribution, `course/modules/M/M4/L04.html:139`), in plain prose, no link. `bayesian-inference` is not used. **Architect confirms (Q3).** |
| D2 | `martingale`, `stopping-time`, `optional-stopping-theorem`, `probability-space` (M6) | L03 stopping rules; "fair game" in the martingale sense | Plain prose only: "a game is fair when its expected payoff is zero". Finite sample spaces only, so `probability-space` is not used. No martingale word. **Architect confirms (Q4).** |
| D3 | `adverse-selection`, `winners-curse`, `bayesian-nash-equilibrium`, `common-value-auction` (E2) | L04 "where the canon breaks": the informed trader's order is the adverse-selection cost | Mechanism described in plain words, the term used once with its plain description, no `<dfn>`, no link. The description does not define the term. **Architect confirms (Q5).** |
| D4 | `inventory-model`, `probability-of-informed-trading` (MS1); `roll-spread-estimator`, `spread-decomposition` (MS1) | L04 inventory risk; the spread's decomposition | Plain prose, no link. The lesson's inventory rule is written as the game's own cash and inventory identity. **Architect confirms (Q6).** |
| D5 | `kelly-criterion`, `fractional-kelly` (PR3) | bet sizing in EV games (L03), position sizing in the project | Not used. The project's sizing is the quoted size rule (§5.2), not a growth criterion. (The registry keys `kelly1956new` and `maclean2011kelly`, used by PR3, are not cited, §7.) |
| D6 | `financial-ratio-analysis`, `return-on-invested-capital` (AC2); `security-market-line`, `beta` (AP2); `bond-price-yield`, `duration` (FI1); `fcff-dcf-valuation` (CF4); `gordon-growth-model` (FC4) | L06 technical and case questions (CAPM, duration, DCF, ratios) | Excluded by default. L06 uses closure concepts only (FC2, CF1, AC1, M4). The architect may add AP2, FI1 or CF4 as prerequisites (a curriculum change, not proposed here; Q8). |
| D7 | No registered concept for `binomial distribution`, counting, `permutation` or `combination` | L02 counting puzzles | Plain prose; counting is done with explicit enumeration in the lab. `GLOSSARY_REQUESTS` line for the architect (§12, Q9). No link. |
| D8 | `poisson-process` (SC5); `markov-decision-process` (QR5) | order arrivals; policy design as a decision problem | Not used. Arrivals are one Bernoulli draw per turn (plain prose). No Poisson and no MDP language. |
| D9 | `probability-of-informed-trading` (MS1), `limit-order-book` (FC1, in closure), `order-book-data-structure` (CS2, in closure) | L04 and L05 | FC1 and CS2 concepts are linked (in closure). MS1's concept is plain prose (D4). |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Each row needs the architect's confirmation (§12).**
`tools/check_dag.py` checks linked uses only (`tools/check_dag.py:45-48`); an unlinked use of D1–D9 passes the tool, so the
verifier reads every lesson for these terms (VERIFIER §2.9).

---

## 5. Project (`project.html`, Builder C): game and analysis, `both`, ladder, spec, grader and rubric

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py:33` lists the rungs in order)

1. **Rung 1, worked example** (`lab-PC3-project-1`, SIMULATED, skippable on placement): the reference `replay` applied to the
   seed-0 log of a fixed symmetric policy, annotated line by line with a "why" note at each step (the cash flow of each fill, the
   inventory after each turn, the mark at the settlement value). Full length (tier U).
2. **Rung 2, completion** (`lab-PC3-project-2`, `class="lab completion"`, SIMULATED): the same replay with the cash-flow line
   and the mark line replaced by `___`. Graded instantly. The twin is the completed solution; every page line equals the twin
   line or contains a blank (`tools/run_labs.py` completion rule). `tools/check_projects.py:89-90` requires a completion lab or a quiz.
3. **Rung 3, independent project** (graded `both`): (a) `market_maker.py`, holding `quote` (the quoting rule) and `replay` (the replay and the
   decomposition), graded by the autograder on seeds 0–49; (b) `analysis.md`, graded by the rubric (§5.4).
   `lab-PC3-project-3` is the rung-3 check: it runs the reference `play(seed=0)` and prints the record's P&L and the identity
   the student's `replay` must reproduce.
4. **Rung 4, stretch** (optional, not graded): run the policy on seeds 0–199 and report the distribution of the P&L in cents
   (exact quantiles, the method stated), with the question "what changes when the informed share is 0.6". No ceiling.

### 5.2 Spec (`dl.spec`; `tools/check_projects.py:34` requires the terms in order)

The spec's terms, in this order: **Context**, **Inputs**, **Required outputs**, **Constraints**, **Grading**.

- **Context.** A market maker quotes a bid and an ask for one asset over 20 turns. Some counterparties trade on information the
  maker does not see. The maker must explain, from the game log, how much of the result came from the spread, how much from the
  inventory, and what would change the result. The game log is the evidence.
- **Inputs.** One seeded instance from `grader/instance.py` (`make_instance(seed)`), SIMULATED. The workspace seed is derived
  from the student's workspace ID (BUILDER_RULES §5.3 item 1). The public rules are those of L04, restated exactly:
  `N = 20`; `v_0 = 10000` cents; move `±5` cents with probability 1/2 each; `Q = 5` (maximum quoted size); `L = 10` (inventory
  limit); arrivals: uninformed order (1 unit, buy or sell with probability 1/2 each) with probability 1/2, otherwise informed
  trader. No dataset is used (§6).
- **Required outputs.**
  - `market_maker.py` with `quote(state: dict[str, object]) -> tuple[int, int, int]`, returning `(bid_cents, ask_cents, size)`
    for the current turn. The `state` keys are exactly `turn` (int, 1 to 20), `inventory` (int), `cash_cents` (int),
    `max_size` (int, `5`), `limit` (int, `10`), and `history` (list of the earlier turn records, §5.3).
  - `market_maker.py` with `replay(log: dict[str, object]) -> dict[str, int]`, returning exactly the keys `cash_flow_cents`,
    `inventory_end`, `inventory_mark_cents` and `pnl_cents`, with `pnl_cents = cash_flow_cents + inventory_mark_cents` and
    `inventory_mark_cents = inventory_end × settlement_cents`.
  - `game_log.json`, written by the page's runner for the workspace seed (the engine's output; the student does not edit it).
  - `analysis.md`, the post-game analysis (§5.4).
- **Constraints.** Integer cents everywhere. Standard library only. The same code runs in Pyodide and under pytest. Invalid
  input raises the exception types in §5.5. The analysis states its numbers with the turn index or field that produced them.
  The analysis does not claim a result for real market makers.
- **Grading.** `both`: the autograder (`grader/test_project.py`, dual mode: `market_maker.py` on seeds 0–49) and the rubric
  (`analysis.md`, §5.4). Adversarial question bank: not required (Q6).
- **Reading list.** `ol.reading-list`: the two curriculum books as registry keys, `zhou2008practical` and `crack2015heard`, at
  book level, with no page, problem or edition typed (§7).

### 5.3 The game log and the engine (`grader/engine.py`, public)

`grader/engine.py` is the public engine, run in Pyodide and under pytest. Its functions:
- `make_instance(seed)` is in `instance.py` (§5.6).
- `play(quote, seed) -> dict` runs the 20 turns. It calls `quote(state)` once per turn before the arrival is
  resolved. It returns the log: `seed`, `settlement_cents` (`v_N`, revealed at the end), `turns` (a list of 20 records), where a
  turn record has the keys `turn`, `bid_cents`, `ask_cents`, `size`, `arrival` (`"uninformed-buy"`, `"uninformed-sell"`,
  `"informed"` or `"none"`), `filled` (bool), `fill_price_cents` (int or `null`), `inventory_after` (int), `cash_after_cents` (int).
- The engine raises `ValueError` with the stated messages in §5.5 for an illegal quote; nothing else is required of it.

Learner text calls the time index a **turn** (§2.1 item 11). The code may use `turn`.

### 5.4 Rubric (`analysis.md`; `both` requires it, `tools/check_projects.py:58-75`)

Five criteria, four observable levels each (level 4 down to level 1; `tools/check_projects.py:58-75` counts four `td` cells per row):

1. **Decomposition of the P&L.** Level 4: states `cash_flow_cents`, `inventory_mark_cents` and `pnl_cents` for the submitted
   log, each equal to the `replay` output, with the turns that produced each part. Level 1: "the P&L is positive".
2. **Evidence from the log.** Level 4: cites at least three specific turns by number and field (`bid_cents`, `fill_price_cents`,
   `inventory_after`). Level 1: "the log shows the policy works".
3. **Counterfactual.** Level 4: states one change to the policy (for example, the half-spread widened by 5 cents), reruns the engine
   for the same seed, and reports the change in `pnl_cents` in cents. Level 1: "a wider spread would help".
4. **Assumptions and limits.** Level 4: names the arrival probabilities, the inventory limit and the settlement rule the result depends
   on, and states what the model leaves out (adverse selection in its real form, latency, multiple assets). Level 1: "the model is simple".
5. **Self-review.** Level 4: names one check the student ran on their own `replay` (for example the identity in §5.2) and the result of
   that check. Level 1: "I checked it".

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, fully written on a SIMULATED seed, each annotated
with the descriptors it meets or misses. Self-assessment form (`section.rubric-self`, as in FC2 §4.6). The page shows where the
student's scores diverge from the exemplars' scores. No question bank (Q6).

### 5.5 Exception table (grader tests demand these types, and only these; each named condition gets its own test)

| Condition the page names | Exception | Message must name |
|---|---|---|
| `bid_cents >= ask_cents` (a crossed or locked quote) | `ValueError` | "bid must be below ask" |
| `size` not in `0..5` | `ValueError` | "size must lie in 0..5" |
| `replay` given a log whose `turns` length is not 20 | `ValueError` | "a log has exactly 20 turns" |
| `replay` given a fill with `filled == true` and `fill_price_cents` `null` | `ValueError` | "a filled turn needs a fill price" |

Any other invalid input may raise any exception or return. The grader requires no type for those. A breach of the inventory
limit is not an exception: the engine does not fill the order, and the record shows `filled: false`. That behaviour is stated on
the page and tested (§5.6).

### 5.6 Grader design (Builder C)

Files: `course/modules/PC/PC3/grader/`: `engine.py` (public), `instance.py` (public), `reference.py` (the reference `quote` and `replay` in `market_maker.py`; excluded from deployment, BLUEPRINT §7), `starter.py` (`NotImplementedError` stubs for `quote` and `replay`; the suite
must fail on it), `test_project.py`.

- **`instance.py`**: `make_instance(seed: int) -> dict[str, object]`. Deterministic from `random.Random(seed)`, with the draws in a fixed
  order: for each turn, one fair-value move and one arrival type. Returns `seed`, `start_cents = 10000`, `fair_path_cents` (21 integers,
  `v_0` to `v_20`), `arrivals` (20 strings from the four arrival names), `settlement_cents = fair_path_cents[20]`. Labelled
  **SIMULATED** in the docstring. Every generated instance is valid (fair value positive; arrivals from the four names). Seeds 0–49
  give materially different fair paths (the test counts distinct paths over 20 sampled seeds).
- **`reference.py`**: the full reference: `quote` posts a symmetric quote around the last fair value the public history implies
  (the last filled price, or `start_cents` before any fill), with a half-spread of 10 cents and size 1; and `replay` as §5.2. It
  passes every test on seeds 0–49.
- **`test_project.py`** (properties and numbers; no hard-coded answers; each test recomputes the expected value from the instance's
  own parameters by an oracle written apart from `reference.py`):
  - **Legality.** For seeds 0–49, the student's `quote` returns three integers for every turn, `bid < ask`, `0 <= size <= 5`.
    A crossed quote raises `ValueError` naming "bid must be below ask" (isolated test, hand-built quote). A size of 6 raises
    `ValueError` naming "size must lie in 0..5" (isolated test).
  - **Log shape.** `play(policy, seed)` returns exactly 20 turn records; a log of 19 turns raises `ValueError` ("a log has exactly 20
    turns") in `replay` (isolated test). A filled turn with `fill_price_cents = None` raises `ValueError` ("a filled turn needs a fill
    price") (isolated test).
  - **Replay.** For seeds 0–49, the fills in the student's log equal the engine's fills under the stated rules (buy at the ask, sell at the
    bid, one unit, inventory limit).
  - **Inventory limit.** No `inventory_after` exceeds `|10|`. A hand-built order that would breach the limit is recorded `filled: false`
    (both directions of the inequality: an order that reaches 10 fills; one that would reach 11 does not).
  - **Cash identity.** `cash_after` changes by exactly `−ask` on a buy fill and `+bid` on a sell fill (integers).
  - **P&L identity.** `replay(log)` returns `pnl_cents == cash_flow_cents + inventory_end × settlement_cents` exactly, and
    `cash_flow_cents` equals the sum of the fill cash flows from the log (integers).
  - **Mark uses settlement.** A hand-built log whose last quote mid differs from `settlement_cents` gives the mark at `settlement_cents`
    (not at the mid).
  - **Money is integer.** Every money key in `replay` is an `int` (type check, all seeds).
  - **Seed consistency.** The log's `seed` equals the seed the grader ran; a log copied from seed 0 fails for seed 7 (the replay differs).
  - Failure messages name the violated property and hint at the concept. They never print the expected value; each failing check sets
    `__tracebackhide__ = True` (fixer-rule 19).
- **Dual mode.** The same suite runs in Pyodide and under pytest; each test under 5 s in Pyodide; the suite under 60 s.
- **Five alternative correct implementations** (each a `market_maker.py` with `quote` and `replay`, all must pass seeds 0–49; the verifier writes them as
  scratch fixtures and archives the scripts under `ledgers/PC3/scripts/`):
  1. integer-only accounting with a class-based policy (`class Maker`, its `quote` method);
  2. closures: `make_quoter()` returns `quote`; `replay` written as one fold over the turns;
  3. inventory-skewed quotes (both sides shifted by minus one cent per unit of inventory), with the replay written from the cash identity;
  4. size scaled down as `|inventory|` grows (size 0 at the limit), replay with an explicit list accumulator;
  5. threshold quoting (quote only when the spread is at least 10 cents, otherwise size 0), replay with a `dataclasses` record per turn.
  Each alternative is correct by the rules of §5.2; none is required to earn a particular P&L.
- **Mutants (ten, each a complete module under `ledgers/PC3/mutants/`; VERIFIER §2.6 asks for at least three; ten is the bar).** Each
  is a single-change copy of the reference. The first docstring line names the student error.
  1. `replay`: the inventory mark is omitted (P&L is cash only).
  2. `replay`: the sell cash flow sign is flipped.
  3. `replay`: unfilled orders are counted (the `filled` flag is ignored).
  4. `replay`: the mark uses the last quoted mid, not `settlement_cents`.
  5. `replay`: the settlement is rounded to the nearest dime before marking.
  6. `replay`: the last turn is omitted from the loop.
  7. `replay`: a sell adds to inventory (the sign of the inventory update is flipped).
  8. `replay`: a hard-coded result for seed 0 is returned for any log.
  9. `quote`: the quoted size is 6 (above the maximum), so the engine raises `ValueError`.
  10. `quote`: a crossed quote (`bid == ask`) is posted on turn 1 only; the engine raises `ValueError`.
  `tools/mutate_graders.py --unit PC3 --seeds 0-9` (default 0–9, `tools/mutate_graders.py:30-32`) must report every mutant killed,
  and `tools/ledger.py` counts each listed mutant (`tools/ledger.py:47-91`). A mutant that survives and violates a stated rule is killed by
  a new test (architect rule 9). Mutants that need the hidden fair value (for example "the policy reads the fair value") are not in the
  list: they are not detectable from a log (B3), and they are stated as a KNOWN LIMITATION.

### 5.7 Lab numerics (Builders A–C)

- Every lab is standard library only, seeded where random (`random.Random(seed)`), no network, no warnings under `python -I -W error`,
  under 10 s in Pyodide. Every twin ends with an unconditional `main()` call (`tools/run_labs.py:50-60`).
- Exact labs print exact values (`Fraction` rendered as fractions or as cents). Where a value is rounded for display, the rule is
  stated in the hypothesis and the interpretation (E1 §2.1 item 1 precedent).
- Labels: SIMULATED only where a game instance is generated (L04, the project's check and worked example). The drill items of L02 are
  "generated items", the sequence of L05 is "seeded", and neither is called data.

---

## 6. Real-data policy

- **No dataset is used.** PC3's brief names no data (`curriculum/06-profession-capstone.yaml:175-182`). Every number is a puzzle
  answer, a derivation, a game instance or a stated assumption. No file is embedded, and no `data-files` attribute appears on any lab.
  No `MANIFEST.json` entry is added. `DATA_REQUESTS`: none.
- **Honest-pending note**: none is needed, because nothing is claimed as real. The project page states that every instance is
  SIMULATED and generated by `instance.py`, and that the game is a model.

---

## 7. Registry keys and requests

### 7.1 Keys the unit may cite (verified in `references/references.json`; both `used_by` already contain PC3)

| Key | Record (as read) | Status | Use in PC3 |
|---|---|---|---|
| `zhou2008practical` | Zhou, "A practical guide to quantitative finance interviews", year 2008, Open Library record (`references/references.json:23402`); `used_by: ["PC3"]`; source string matches `curriculum/06-profession-capstone.yaml:172` exactly | verified | Reading list; book level only. No problem, answer or page attribution. No edition typed (B4) |
| `crack2015heard` | Crack, "Heard on the street: quantitative questions from Wall Street job interviews", year 2015, Open Library record (`references/references.json:6222`); `used_by: ["PC3"]`; source string matches `curriculum/06-profession-capstone.yaml:173` exactly | verified | Reading list; book level only. No edition typed (B4) |

Registry-verified keys that are **not** curriculum-listed for PC3 and are **not recommended** (they would also need `used_by` updates made
by the architect through the registry tools; the builders never edit a record):
`ho1981optimal` (`references/references.json:12564`, Ho and Stoll 1981, dealer pricing, `used_by: ["MS1"]`), `glosten1985bid`
(`references/references.json:10451`, `used_by: ["MS1"]`), `kyle1985continuous` (`references/references.json:15280`, `used_by: ["MS1"]`),
`kelly1956new` (`references/references.json:14305`, `used_by: ["PR3"]`), `maclean2011kelly` (`references/references.json:16358`,
`used_by: ["PR3"]`). The architect may approve `ho1981optimal` and `glosten1985bid` for L04 at paper level (Q6). Default: not cited.

### 7.2 REFERENCE_REQUESTS

None. No claim in the plan requires a source outside the registry. The only empirical topic (interview practice) is not written (§2.2).

### 7.3 Cite-by-key rule

Builders write the citation as the key only, in the reading list and in the `cite` field of cards. No bibliographic string is typed.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for PC3: no `atlas:` key on the project (`curriculum/06-profession-capstone.yaml:175-182`),
and no entry of the `atlas` array in `curriculum/curriculum.json` names PC3 (computed). `tools/check_projects.py:144-146` checks a
contract only when the project names one. No `atlas/PC3.contract.md` is needed.

---

## 9. Cards builder (Builder F, after A–C)

- `course/modules/PC/PC3/cards.json`, ids `PC3-c001` upward, `lesson` in `L01`–`L06`, at least one card per lesson
  (BUILDER_RULES §7; the "no cards for <lesson>" check).
- One atomic card per definition, theorem statement, key formula and misconception. Each card tests one fact.
- Grade **T** for every derived result (the product bound in L01, the Taylor remainder bound, the expectation of a sum, the fair-game
  definition as a definition, Bayes' rule, the stopping-rule finite example, the forward-price identity, the NPV identity, the game's P&L
  identity). Set `basis` to the lab or the derivation that establishes it, for example `"basis": "Lab L03, Derivation 2 (exact)"`.
- `cite` is `[]` for every card: the unit makes no empirical claim, so no registry key is needed on a card.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
cd /Users/billyribeiro/dev/quant-phd
.venv/bin/python tools/check_pages.py --unit PC3            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit PC3
.venv/bin/python tools/check_projects.py --unit PC3
.venv/bin/python tools/run_labs.py --unit PC3               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/PC/PC3/L01.html           # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/PC/PC3/L02.html --refresh lab-PC3-L02-1   # after a twin edit
.venv/bin/python tools/run_graders.py --unit PC3 --seeds 0-49
.venv/bin/ruff check tests/labs/PC3 course/modules/PC/PC3/grader && .venv/bin/ruff format --check tests/labs/PC3 course/modules/PC/PC3/grader
.venv/bin/mypy tests/labs/PC3 course/modules/PC/PC3/grader   # strict; confirm the configured paths before running
```

Verifier only (not builders; on a quiet machine): `.venv/bin/python tools/mutate_graders.py --unit PC3 --seeds 0-9`,
`.venv/bin/python tools/verify_refs.py --unit PC3`, `.venv/bin/python tools/page_smoke.py --unit PC3`.

Flags, as read by the planner: `check_pages.py`, `check_dag.py` and `check_projects.py` take `--unit` (`tools/check_projects.py`
`main`); `run_labs.py` takes `--unit`, `--page`; `run_graders.py` takes `--seeds` with default 0–49 (`tools/run_graders.py:138-139`
prints "no autograder" only for a unit whose grading is not `autograder` or `both`, so PC3 is run); `mutate_graders.py` takes
`--seeds` with default 0–9 (`tools/mutate_graders.py:32`).

Not run by builders: `page_smoke.py`, `check_pages.py --all`, `build_site.py --check`, `render_curriculum.py`. Repo-wide gates are the
architect's, once, before merge.

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone** (§8). `check_projects.py` skips the contract check (`tools/check_projects.py:144-146`).
2. **No debate.** No `debate:` key (`curriculum/06-profession-capstone.yaml:157-182`), so no debate brief is required.
3. **Grading `both` on a tier-U module.** The rubric and two exemplars at two levels are required (`tools/check_projects.py:58-75`), and
   the spec's grading entry names "autograder" and "rubric" (`tools/check_projects.py:38, 41-50`).
4. **One curriculum lab, six lessons.** The curriculum names one lab (`yaml:174`). The plan adds one lab per lesson (FC2 and E5
   precedent). The curriculum lab is `lab-PC3-L02-1`.
5. **The game is not a figure.** No chart kernel is needed. The game is code (B1).
6. **Hidden information is not enforceable by a log grader** (B3). KNOWN LIMITATION.
7. **`check_dag.py` sees linked uses only** (§4). Unlinked uses of D1–D9 are read by the verifier.
8. **Problem-set workload.** Four tiers × three problems × six lessons = 72 problems with worked solutions (§2.2). The tool does not
   count them; the verifier does (VERIFIER §2.9).
9. **Process words.** "round" is a process word in learner text (fixer-rule 14). The game's time index is "turn" (§2.1 item 11).
10. **`check_projects.py` does not test the game.** The autograder carries the game's correctness; the tool checks only the spec terms,
    the ladder, the rubric and the exemplars.

---

## 12. Open questions for the architect (numbered; each needs a decision before the builders start)

1. **B1, the play interface (BLOCKING).** Confirm the default: a Pyodide engine played by code (`market_maker.py`, `game_log.json`,
   `analysis.md`), no JavaScript game. Alternative: a clickable game, which needs a new JS kernel with tests (BUILDER_RULES §6.4), not
   recommended because the architect default bars new kernels for modules.
2. **B2, timing (BLOCKING for L02 and L05 wording only).** Confirm: no JavaScript timer; "timed" means a stated per-item time budget kept by
   the student, and the lab counts answers deterministically. Alternative: an advisory stopwatch built on the existing page template, if the
   template has one (`course/templates/` was not read by the planner; the verifier checks).
3. **D1, Bayes' rule.** Default: derive Bayes' rule in L02 from M4's conditional distribution (`course/modules/M/M4/L04.html:139`), plain
   prose, no link; `bayesian-inference` (S1) not used. Alternative: add S1 as a prerequisite (a large curriculum change; not proposed).
4. **D2, martingale language.** Default: none. "Fair game" is a definition by zero expected payoff, and the stopping-rule example is finite.
   Alternative: add M6 as a prerequisite (large change; not proposed).
5. **D3, adverse selection.** Default: plain description in L04, no link, no `<dfn>`. Alternative: add E2 as a prerequisite (large change).
6. **D4 and the two MS1 registry keys.** Default: MS1 concepts are plain prose; `ho1981optimal` and `glosten1985bid` are not cited. Alternative: the
   architect approves them at paper level for L04 and adds PC3 to their `used_by` through the registry tool (builders never edit records).
7. **D6, technical questions.** Default: L06 uses closure concepts only (FC2, CF1, AC1, M4). CAPM, duration, DCF and ratio questions are excluded.
   Alternative: add AP2, FI1 or CF4 as prerequisites (a curriculum change).
8. **D6 repeat, prerequisites.** Confirm the closure is unchanged: no prerequisite is added to PC3 by default.
9. **D7, counting vocabulary.** Confirm: counting is plain prose with explicit enumeration; `GLOSSARY_REQUESTS` for "binomial coefficient" if the
   architect wants a glossary entry.
10. **Registry strings (B4).** Confirm: cite both keys with no edition and no publisher in prose (the E5 B4 default). The curriculum string
    "16th ed." stays as the curriculum's own text.
11. **Hours.** Confirm 6 lessons × 6 h = 36 h and a 14 h project (28%). Alternatives within the rules: 5 lessons × 8 h = 40 h and a 10 h project
    (20%); or 6 lessons of 7, 7, 6, 6, 6, 6 h = 38 h and a 12 h project.
12. **Mutant and alternative interpretation.** The grader checks a log and a pair of modules, so the "alternative correct implementations" are five
    policy-and-accounting pairs of different styles (§5.6). Confirm, or name a different reading.
13. **Scope of the game.** Confirm the rules in §3 L04 and §5.2 (N = 20, v_0 = 10000 cents, ±5 cents, Q = 5, L = 10, the arrival probabilities).
    They are planner choices, not curriculum facts (`yaml:174-182` gives none of them).
14. **Builder split.** Confirm: Builder A (L01–L03, `index.html`), Builder B (L04–L06), Builder C (project, grader, project labs), Builder F
    (cards). Builders D and E have no files in this unit.
15. **Adversarial?** The post-game analysis is not an IC defence. The PC2 unit owns the attack-angle bank (its entry starts at `curriculum/06-profession-capstone.yaml:130`;
    the PC2 project brief is in the same entry). No question bank in PC3. Confirm.
16. **Atlas.** Confirm no contract for PC3 (§8).
17. **Glossary.** Terms outside the five concepts are plain `<dfn>` with no `data-concept` (§2.1 item 5). Confirm that no `GLOSSARY_REQUESTS` entry
    is needed beyond the one in Q9.
18. **Hidden information (B3).** Confirm the KNOWN LIMITATION wording: a student who reads `instance.py` can see the fair path; integrity rests on the
    per-seed instances and the rubric's analysis.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01–L02 (includes the curriculum lab), L03–L04, L05–L06, the project (grader:
   ten mutants and five alternative pairs; rubric and exemplar calibration), cards. Failing rows return to the owning builder only, with only
   the failing rows.
3. Ledger at `ledgers/PC3.verification.json`; verifier scripts under `ledgers/PC3/scripts/` (VERIFIER §3); mutants under `ledgers/PC3/mutants/`.
   No `ledgers/PC3/equivalent/` is expected unless a mutant proves equivalent (architect rule 9).
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 and B2 must be resolved first.

Architect decisions: pending (§12). This plan is the planner's proposal.

## Architect decisions (2026-11-03, binding). Where the plan states a recommendation for an open question, follow it. Defaults for every module: concepts outside the prerequisite closure are plain prose with no link and no dfn; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields only or not at all (never edit a record, never type bibliographic data); no real data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST in plans/<UNIT>-open-items.md; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every grader; not adversarial, no question bank. plans/FINAL-ARCHITECT-RULINGS.md and ~/.fanout/fixer-rules.md bind every builder. No reference is admitted in this batch: a statement whose source is a REFERENCE_REQUEST is not made, or it is taught as a model result with no attribution.
Module specifics: 6 lessons x 6 h + 14 h project; builders A: L01-L03 and index; B: L04-L06; C: project, grader and project labs; F: cards. Defaults confirmed: no JavaScript game and no timer; Bayes' rule derived from M4 conditional distribution as plain prose; game constants as the plan states (N = 20, v0 = 10000 cents, 5 cents, Q = 5, L = 10) are planner choices stated as such on the page; the MS1 keys are not cited.
