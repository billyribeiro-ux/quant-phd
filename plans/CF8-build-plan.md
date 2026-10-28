# CF8 build plan: Haiku builders in parallel (planner output, 2026-10-28)

Unit: **CF8 · Working Capital, Treasury & Short-Term Finance** · tier U · 50 h · prerequisites **CF1, AC1** · Atlas milestone:
**none** · grading **both** (autograder for the forecast engine, rubric for the treasurer memo) · output directory
`course/modules/CF/CF8/` (part code `CF`). Owner: orchestrator (architect). Executors: Claude Haiku builders, then
independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Status of this file: planner proposal. Section 10 lists the open questions; the architect decides them before the builders
start. Where a precedent exists (CF1, E1, M1, AC2, AC4 architect decisions), this plan reuses it. No lesson content is written
here. No git operations were run.

Evidence for every curriculum statement is `file:line` read during planning. Anything not in the curriculum is marked as a
planner proposal.

## 0. Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| CF8 id, title, tier U, hours 50 | `curriculum/02-economics-finance-core.yaml:894-897` |
| Prereqs `[CF1, AC1]` | `curriculum/02-economics-finance-core.yaml:898` |
| Core text: cash conversion cycle; receivables and credit policy; inventory; payables and supply-chain finance; cash forecasting; bank lines; commercial paper; "the evidence on corporate cash holdings" | `curriculum/02-economics-finance-core.yaml:899-902` |
| Nine concepts introduced (one per entry, in this order): cash-conversion-cycle, working-capital-days, trade-credit-policy, supply-chain-finance, direct-cash-forecast, revolving-credit-facility, financial-covenant, commercial-paper, precautionary-cash-holdings | `curriculum/02-economics-finance-core.yaml:903-912` |
| Three free-text sources: Opler, Pinkowitz, Stulz & Williamson (1999), JFE 52(1); Bates, Kahle & Stulz (2009), JF 64(5); Brealey, Myers & Allen, 14th ed. (2023) | `curriculum/02-economics-finance-core.yaml:913-916` |
| Lab: "Cash-conversion-cycle decomposition from XBRL." | `curriculum/02-economics-finance-core.yaml:917` |
| Project "13-week cash-flow forecast": a 13-week direct cash forecast and liquidity plan for a stressed company case; size the revolver, identify the covenant pinch point, propose working-capital actions with their cash impact | `curriculum/02-economics-finance-core.yaml:918-923` |
| Deliverable "Forecast model plus treasurer memo."; grading `both` | `curriculum/02-economics-finance-core.yaml:924-925` |
| No `debate:` key and no `atlas:` key on CF8 | `curriculum/02-economics-finance-core.yaml:894-925` (absent) |
| JSON row mirrors the YAML (hours 50, prereqs CF1 and AC1, nine `introduces`, three sources, lab, project, grading both) | `curriculum/curriculum.json:8326` (`"id": "CF8"`) |
| Rendered block agrees | `CURRICULUM.md:535-540` |
| Dependents: CAP0 requires CF8; CF7 lists CF8 among its prerequisites | `curriculum/meta.yaml:62`; `curriculum/02-economics-finance-core.yaml:864` (CF7 prereqs) |
| No Atlas milestone names CF8 (the atlas block lists modules; CF8 appears only in the course map and topic map) | `curriculum/meta.yaml:83`, `:157`; `grep` of `meta.yaml` for `CF8` returns no atlas line |
| CF1 is the other prerequisite; its row | `curriculum/curriculum.json:8070` (`"id": "CF1"`) |
| Prerequisite closure, computed with `coursekit.prerequisite_closure` logic: CF1 pulls M1 and AC1, M1 pulls P0.1, AC1 pulls P0.1 | `curriculum/curriculum.json` prereqs of CF1, M1, AC1, P0.1 |

**Closure (computed): `{CF1, AC1, M1, P0.1}`.** Concepts usable without definition are those introduced by CF1 (10), AC1 (12),
M1 (14) and P0.1 (11). Only these may be linked (`tools/check_dag.py` `check_unit`).

Registry keys for CF8 (from `references/references.json`, read by the planner):

| Key | Record (as read) | Status |
|---|---|---|
| `bates2009us` | Bates, Kahle & Stulz, "Why Do U.S. Firms Hold So Much More Cash than They Used To?", J. Finance 64(5), 1985-2021, doi 10.1111/j.1540-6261.2009.01492.x; `used_by: ["CF8"]`; authors and year match the curriculum string | verified, usable |
| `opler1999determinants` | Opler, "The determinants and implications of corporate cash holdings", JFE 52(1), 3-46, doi 10.1016/s0304-405x(99)00003-3; `used_by: ["CF8"]`; **record author list is "Opler" only**; `notes.authors` records curriculum "Opler & Pinkowitz & Stulz & Williamson" against crossref "Opler" | verified, usable only under Q2 |
| `brealey2022principles` | Brealey, *Principles of Corporate Finance*, McGraw-Hill, record year 2022, ISBN 9781264080946; `notes.year` curriculum "2023", record "2022"; `used_by: ["CF1","CF8"]` | verified, **conflicts with the curriculum string; do not cite** (Q3) |

No registry key covers working capital, trade credit, supply-chain finance, revolving credit, covenants or commercial paper
(title search of `references/references.json`, planner). Those topics go to `REFERENCE_REQUESTS` (section 7).

## 1. Hours (feasible; no STOP condition)

The tool rules (`tools/check_pages.py`, `check_hub`, `check_lesson`):

- each lesson declares 6-12 `data-hours`;
- hub: `data-hours-lessons + data-hours-project = 50`;
- project share within 10-40 % of 50, i.e. 5 to 20 h;
- lessons sum to the hub's lessons figure.

Chosen split (planner proposal, Q1): **five lessons of 8 h = 40 h; project 10 h (20 %)**. This mirrors the CF1 split
(48 + 12 at 60 h, 20 % project) and the E1 precedent of an even lesson split. Feasible. The curriculum figure (50 h) satisfies
every tool rule, so there is no STOP.

Alternative (Q1): four lessons of 9 h plus a 14 h project (28 %). Rejected by the planner because the 13-week forecast is the
largest deliverable and a 14 h project would leave the lessons with 2-3 concepts each. The 10 h project is tight; section 5.6 shows
its budget.

## 2. Binding rules for every builder (BUILDER_RULES adapted to CF8)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `VERIFIER_RULES.md` §2 (what a verifier checks),
`plans/CF1-build-plan.md` (its Architect decisions are binding precedent), `plans/E1-build-plan.md` (§2.1 carried-over verification
lessons), `plans/AC2-build-plan.md` (real-data pattern), `plans/M1-build-plan.md` (Architect decisions), `plans/AC4-build-plan.md`
(§10 decisions), and this file. Study `course/modules/CF/CF1/` and `course/modules/M/M1/` for layout only. Imitate structure, not
wording. `course/templates/` holds the skeletons.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed with `fractions.Fraction` from exact inputs and rounded
   only at display. A page that shows a rounded figure says which rounding it uses (E1 §2.1.1, CF1 L01 Remark 5.2, AC4 KNOWN 3).
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only what
   the printed numbers show (M1 LESSON_TEXT_DEFECTS).
3. **Attribute nothing unread.** A source is cited only for what the builder has read in the source (at least the abstract, with
   the locator the source gives). No page, table, coefficient or sample statistic is typed from memory. A textbook result without a
   confirmed locator is a derivation on the page (grade T) or is cited at book level with no locator. The planner read no CF8 source
   beyond the registry record, so **no attribution to Opler et al. or Bates et al. is licensed by this plan**; the builder reads the
   DOI page or abstract first (E1 §2.1.3).
4. **Scope words need a computation or an explicit hypothesis.** "every", "all", "never", "always", "any", "inventory", "bank
   lines", "the evidence", "liquidity" are used only where a proof, a finite check, a lab, or a stated hypothesis covers them
   (E1 §2.1.4). See Q9 for the core text's scope.
5. **Define before use.** Each of the nine concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned lesson
   (section 3) and never before it. A lesson links a concept only from an earlier or the same lesson.
6. **Proposition hypotheses explicit.** Every Theorem or Proposition block states its hypotheses as numbered **Assumptions** (1, 2,
   3, ...) before the statement. Every graded-T result names each assumed fact.
7. **Grader exception types only where the page names the condition.** The spec lists the three invalid-input conditions in §5.4 and
   the exception type for each. Any other invalid input may raise any exception or return. **Five alternative correct implementations
   must pass** the suite (section 6.4).
8. **Integer cents.** Every money output of the engine (receipts, disbursements, balances, headroom, cash impact) is an `int` in
   cents, computed from exact `Fraction`s and rounded once, half up, by the rule stated on the project page (E1 §2.1.8, AC4 Q9/Q10).
   No float money, no tolerance on money.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own container.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":`
    guard. `run_labs.py` runs each twin as `python -I -W error <twin>` (`tools/run_labs.py` `run_twin`, lines 51-61). Stdlib only, no
    warnings.
11. **Notation registry.** Use no symbol registered in `notation/notation.json` with another meaning. See section 8.2.
12. **Ellipsis ban.** The banned-string pattern `\.\.\.` in `tools/check_pages.py` (line 58 block) matches a literal three-dot ellipsis
    in prose. Use `\ldots` inside KaTeX only.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- **Evidence.** Every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key, or is a derivation on the page. A claim
  graded B or C names its published counter-evidence (BUILDER_RULES §2.5); see Q10.
- **Concepts.** Each of the nine CF8 concepts is defined once in its lesson (section 3). Concepts from the closure (CF1, AC1, M1,
  P0.1) are linked: `<a class="concept" data-concept="<id>" href="../../../concepts.html#<id>">`. Earlier CF8 lessons: `href="Lnn.html#def-<id>"`.
  A concept outside the closure is **not linked**; it is described in plain words, and the builder adds a `DAG_DEFECT` line (section 4).
- **Labs.** Code lives once in its twin `tests/labs/CF8/lab-CF8-Lnn-1.py` (project labs `lab-CF8-project-1..3.py`). The page carries
  `@@LAB:<file>@@` and `@@OUT:<file>@@`; `.venv/bin/python tools/embed_labs.py <page>` fills them. Never type expected output by hand.
  Lab ids match `lab-CF8-<page>-<n>` (`check_pages.py` `check_lesson`). Standard library only (`fractions`, `itertools`, `math`,
  `random.Random(seed)` for any random draw); no network; no `data-files` attribute; under 10 s in Pyodide; warning-free under `-W error`.
- **SIMULATED label.** Every generated case is labelled SIMULATED on the lab hypothesis, on the figure line if any, and on the project page.
  Exact closed-form checks on a generated case are still labelled SIMULATED because the inputs are generated (section 9).
- **Never hand-edit generated files** (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `MANIFEST.json`, market snapshots, `notation/notation.json`). Requests go in the output contract.
- **Learner-visible text.** No process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references in code
  comments (E1 §2.2).
- **Banned strings** (`tools/check_pages.py`, `BANNED` block at line 58): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the
  scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
  "obviously", "clearly", and any literal `...`.
- **Percent changes** state the base and the direction. **Finite enumerations** are grade C with their basis named, not T (E1 §2.2).
- **Every "checked" or "verified" claim** names the lab, line or test that did the check.
- **Hub lesson titles** match each lesson's `<h1>` at integration.
- **No `git commit`, no push.** Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10 output contract.

## 3. Outline and file ownership (planner proposal; the architect fixes it)

| Lesson | Title (working) | Concepts it defines (each exactly once) | Lab twin id (`tests/labs/CF8/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | The cash conversion cycle and working-capital days | `working-capital-days` (defined first), `cash-conversion-cycle` | `lab-CF8-L01-1` = **the curriculum lab**: CCC decomposition (DSO + DIO - DPO) on a SIMULATED filer in company-facts shape | 8 | Builder A |
| L02 | Trade credit, credit policy and supply-chain finance | `trade-credit-policy`, `supply-chain-finance` | `lab-CF8-L02-1`: break-even of a credit-term extension (exact, Fraction) and the implied annual cost of an early-payment discount | 8 | Builder A |
| L03 | The 13-week direct cash-flow forecast | `direct-cash-forecast` | `lab-CF8-L03-1`: 13-week receipts, disbursements, minimum-cash rule and revolver draws on a SIMULATED case; cash identity checked each week | 8 | Builder B |
| L04 | Revolving credit facilities and financial covenants | `revolving-credit-facility`, `financial-covenant` | `lab-CF8-L04-1`: revolver availability, minimum-liquidity covenant headroom, pinch week, and the effect of a DSO slip | 8 | Builder B |
| L05 | Commercial paper and precautionary cash holdings | `commercial-paper`, `precautionary-cash-holdings` | `lab-CF8-L05-1`: seeded simulation of a year's net cash flow; shortfall frequency against cash buffers; labelled SIMULATED | 8 | Builder C |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 40 / 10, reading | none | none | - | Builder C (after A-B) |
| project | 13-week cash-flow forecast (`both`) | none | `lab-CF8-project-1` (rung 1), `lab-CF8-project-2` (rung 2, completion), `lab-CF8-project-3` (rung 3 run) | 10 | Builder D |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` | none | none | - | Builder D |
| cards | `cards.json`, one card per definition, key result and misconception of L01-L05 | none | none | - | Builder E (after A-D) |

Concept coverage: 2 + 2 + 1 + 2 + 2 = 9, each of the nine in `curriculum/02-economics-finance-core.yaml:904-912` in exactly one row.

Ordering check: L01 defines the day-count vocabulary used by L02 (credit terms) and L03 (receipts lag). L02 uses CCC (L01) and the
credit-term break-even uses the closure concept `net-present-value` (CF1, linked). L03 uses DSO and trade-credit terms (L01, L02).
L04 uses the forecast (L03) for the pinch week. L05 uses the revolver (L04) as the backstop in the precautionary-buffer comparison.
No lesson links a later definition.

Lesson content order (BUILDER_RULES §4.2): why it matters (at most 120 words), numbered core sections with Definition, Theorem, Proof,
Example and Remark blocks, inline lab, where the canon breaks, misconceptions (at least 3), problem set (at least 3 in each of Mechanics,
Proof, Empirical, Research, each with a full worked solution in `<details class="solution">`), key-results table, quiz (8-15 items, each
with an explanation), references. **No debate brief**: CF8 has no `debate` key (section 0). Do not write one.

Concept definitions and their home (CF8 closure use):
- L01: uses `balance-sheet` (AC1, linked) for receivables, inventory and payables balances; uses `net-working-capital` (CF1, linked) to
  connect the day counts to the working-capital investment; `income-statement` (AC1, linked) for revenue and cost of sales.
- L02: `net-present-value` (CF1, linked) for the credit-term decision; `present-value` and `discount-factor` (M1, linked) for the discounting.
- L03: `cash-flow-statement` (AC1, linked) for the direct-method contrast; no other closure concept required.
- L04: no closure concept required beyond `balance-sheet`.
- L05: no closure concept. Mean, quantile and standard error are plain words (section 4, Q12).

## 4. DAG problems (concepts natural CF8 content would use outside the closure)

Each row is resolved as plain prose with no link, plus a `DAG_DEFECT` line in the output contract. The architect decides whether to
change the curriculum (Q5).

| Concept | Owner | Where natural CF8 content uses it | Resolution |
|---|---|---|---|
| `xbrl-standardization` ("XBRL data and statement standardization") | AC2 (`curriculum/curriculum.json` `concepts`) | the L01 lab is named "from XBRL" (`curriculum/02-economics-finance-core.yaml:917`) | plain prose "company filings tagged in XBRL" with no link; `DAG_DEFECT` (Q5) |
| `net-working-capital` | CF1 (**in closure**) | L01 working-capital investment | **link it**. Do not redefine. Name collision: CF8 teaches day counts, CF1 teaches the investment. Both are used, one definition each |
| `revolver-circularity`, `debt-schedule` | CF7 (downstream) | interest on the revolver depending on its own balance | out of scope: revolver interest is a stated input rate, not a circular term; no name, no link (Q7) |
| `leverage-dynamics`, `financial-distress-costs`, `leverage` family | CF2 (outside) | a leverage-based covenant | not used; the covenant is minimum liquidity (Q6) |
| `cash-sweep` | CF5 (outside) | sweeping excess cash to repay the revolver | not used; the revolver rule in L03 is stated in prose |
| `liquidity-coverage-ratio` | BK1 (outside) | "liquidity" in covenant prose | "liquidity" means cash plus undrawn revolver, defined in L04 with no link |
| `subscription-line` | PM1 (outside) | none | not used |
| `stress-testing` | PR4 (outside) | the stressed company case | plain phrase "stressed case"; no link |
| `cash-flow-at-risk` | CF9 (outside) | risk of a cash shortfall (L05) | not used; the L05 buffer comparison is plain prose |
| `wacc` | CF2 (outside) | cost of a revolver | not used; the revolver rate is a stated input (no cost-of-capital concept) |
| Statistics terms (mean, quantile, standard error) | S-series (outside) | L05 simulation summaries | plain words, no link, `DAG_DEFECT` (Q12) |

Terms outside the nine CF8 concepts and outside the closure (for example "borrowing base", "net debt", "days payable outstanding" in
plain words) may appear in prose. Emphasised ones use a plain `<dfn>` without `data-concept`; `check_dag.py` skips a `<dfn>` with no
`data-concept` (`check_unit`, `if not concept: continue`).

## 5. Units, labs and the project

### 5.1 Hub (`index.html`, Builder C)

- `<html lang="en" data-root="../../../" data-unit="CF8" data-page="index">`; `<main data-hours-lessons="40" data-hours-project="10">`.
- 4-8 `ol.objectives` with measurable verbs (target six): compute DSO, DIO, DPO and the cash conversion cycle from statements;
  evaluate a credit-term extension by its break-even; construct a 13-week direct cash forecast; size a revolver against a minimum-cash
  rule; locate a covenant pinch point and its headroom; compare a cash buffer with a simulated shortfall distribution.
- Prerequisites: CF1 (and AC1), each linked to `../../../concepts.html#<id>` for the concepts it uses (`net-present-value`,
  `net-working-capital`, `balance-sheet`, `cash-flow-statement`).
- Placement: `section.quiz#placement data-unit="CF8" data-page="placement" data-mastery="0.8"` with nine items. At least two
  `data-skill` items test what rung 1 and rung 2 teach (the worked example's forecast line and the completion problem's revolver
  line). The rest test CF1 and AC1 prerequisites (`check_hub`, placement rule).
- Lesson map: one card link per L01-L05 with `data-progress-key="CF8/Lnn"` and a `data-hours` text.
- Ladder: four `li` with `span.rung-title` for "Worked example", "Completion problem", "Independent project", "Stretch", in that order.
- Core reading: `ol.reading-list` with `li data-cite` keys from section 8.1 only.

### 5.2 Hours split (sums to the curriculum's 50)

| Component | Hours | Basis |
|---|---|---|
| L01 | 8 | DSO, DIO, DPO, CCC identity, the curriculum lab |
| L02 | 8 | credit-term break-even; discount cost; supply-chain finance |
| L03 | 8 | the forecast construction and the minimum-cash rule |
| L04 | 8 | revolver availability and covenant headroom |
| L05 | 8 | buffers and the precautionary motive, two-sided evidence |
| **Lessons total** | **40** | `data-hours-lessons="40"` |
| Project | 10 | section 5.6 |
| **Module total** | **50** | = curriculum hours (yaml 897) |

Each lesson `<html data-hours="8">`.

### 5.3 Lesson labs and figures

- Every lesson has at least one `section.lab` with `id="lab-CF8-Lnn-1"`, `data-runtime="python"`, the `p.hypothesis`, the code,
  `pre.expected` with `data-tolerance`, and `p.interpretation` (`check_lesson`).
- Lab numbering is display order. The curriculum lab is `lab-CF8-L01-1`.
- **No figures** (Q11). A figure would need a JS kernel and a test (BUILDER_RULES §6.4); the architect has not approved any for CF8.

### 5.4 Project spec (`project.html`, Builder D)

Ladder (BLUEPRINT §5.1; `check_projects.py` `RUNGS` order):

1. **Rung 1, worked example** (`lab-CF8-project-1`): one fully solved, annotated 13-week forecast on a SIMULATED stressed case, with a
   "why" note at each step, the revolver draw, the covenant headroom and one working-capital action.
2. **Rung 2, completion** (`section.lab.completion`, `lab-CF8-project-2`): the same case with the revolver draw line replaced by `___`.
   Graded instantly. Its twin is the completed solution; every page line equals the twin line or contains a blank (`run_labs.py`, completion rule).
3. **Rung 3, independent project** (graded): (a) the autograded engine `treasury_forecast.py` to the §5.5 interface and (b) the
   treasurer memo (rubric). `lab-CF8-project-3` is the rung-3 run: it calls the engine on the reference case and prints the outcome table.
4. **Rung 4, stretch** (optional, not graded): the covenant pinch week under a range of DSO slips, with the hypothesis stated first
   (for example, a five-day slip moves the pinch week by at most one week). No ceiling.

`dl.spec` terms (`check_projects.py` `SPEC_TERMS`): **Context** (2-4 sentences, stressed case), **Inputs**, **Required outputs**,
**Constraints**, **Grading**. The grading entry must say "autograder" and "rubric" verbatim (`grading_problems`).

Spec content (planner proposal; the architect freezes it, Q4-Q8):

- **Context.** A manufacturer with a revolving credit facility faces slower collections for thirteen weeks. The treasurer must size the
  revolver, find the week the covenant headroom is smallest, and choose working-capital actions with their cash impact.
- **Inputs.** `make_instance(seed)` output: opening cash, minimum cash, revolver commitment and opening drawn balance, weekly collections
  lag in days, weekly disbursements, and a covenant threshold for minimum liquidity. All money in integer cents; all days in integer days.
- **Day count (Q8).** A 365-day year for DSO, DIO and DPO (`DSO = AR * 365 / Revenue`, the same form for DIO on cost of sales and DPO on
  purchases). One week is 7 days. The horizon is 13 weeks.
- **Covenant (Q6).** Minimum liquidity: cash plus undrawn revolver availability at each week end must be at least the threshold.
  Headroom is liquidity minus threshold, in cents, at week end.
- **Revolver rule (Q7).** Interest is a stated input rate, not circular. If ending cash before a draw would fall below minimum cash,
  the revolver draws the shortfall, capped at availability. A repayment sweeps cash above minimum to the drawn balance, capped at the
  balance. The cap rule is stated on the page (any shortfall beyond the cap is reported as a shortfall, never hidden).
- **Required outputs.** `treasury_forecast.py` with:
  - `forecast(case: dict[str, Any]) -> list[dict[str, int]]`: 13 weekly rows with keys `receipts_cents`, `disbursements_cents`, `draw_cents`,
    `repay_cents`, `ending_cash_cents`, `drawn_balance_cents`, `liquidity_cents`, `headroom_cents`;
  - `revolver_plan(case: dict[str, Any]) -> dict[str, int]`: keys `peak_drawn_cents`, `required_commitment_cents`, `shortfall_cents`;
  - `covenant_pinch(case: dict[str, Any]) -> dict[str, int]`: keys `week` (1-13; ties broken by the earliest week) and `headroom_cents`;
  - `action_cash_impact(case: dict[str, Any], action: str, days: int) -> int`: cash impact in cents of shortening DSO by `days`
    (`action == "dso"`) or lengthening DPO by `days` (`action == "dpo"`), summed over the horizon.
- **Constraints.** Integer cents; each money output computed from exact `Fraction`s and rounded once, half up, to the nearest cent, rule
  stated on the page, in the spec and in the module docstring. Standard library only. No network. Same code in Pyodide and under pytest.
- **Grading.** `both`: the autograder (`grader/test_project.py`, dual mode) and the rubric (`section.rubric-self`, §5.7).
- **Reading list.** `ol.reading-list` with `bates2009us` and `opler1999determinants` (subject to Q2). Nothing else (section 8.1).

### 5.5 Exception table (grader tests demand these, and only these)

| Condition the page names | Exception | Message must name |
|---|---|---|
| horizon other than 13 weeks | `ValueError` | the 13-week horizon |
| revolver commitment negative | `ValueError` | the commitment must be non-negative |
| `action` not `"dso"` or `"dpo"` | `ValueError` | the allowed action names |

Any other invalid input may raise any exception or return. The tests do not require a type for it.

### 5.6 Time budget (`<table id="hours">`, sums to 10 h)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example | 1 | read and annotate one solved forecast |
| Rung 2, completion problem | 1 | fill the revolver draw line and run the instant check |
| `treasury_forecast.py` (forecast, revolver, pinch, action impact) and the suite | 4 | implement to §5.4, pass seeds 0-49, handle the exception table |
| Treasurer memo (rubric) | 3 | the forecast, the revolver size, the pinch week, two actions with cash impact |
| Self-assessment against exemplars | 1 | score the memo, then compare with exemplar-a and exemplar-b |
| **Total** | **10** | equals `data-hours-project` on the hub |

The planner's estimate is the tightest part of CF8. If the builder's estimate exceeds 10 h by more than 30 % (VERIFIER §2.6), the
architect reconsiders Q1 (a 14 h project).

### 5.7 Rubric (memo; `both` requires it; `check_projects.py` `rubric_problems`)

Five criteria, each with four observable levels (level 4 down to level 1), in `table.rubric#rubric-memo`:

1. **Forecast construction.** Every weekly line traces to a case input; the identity opening cash + flows = ending cash is stated.
   Level 4: names each input and the identity. Level 1: "a reasonable forecast".
2. **Revolver sizing.** Peak draw and required commitment, with the minimum-cash rule stated. Level 4: states the rule and the number
   in cents. Level 1: "enough credit".
3. **Covenant pinch point.** Names the week, the headroom in cents, and the covenant definition. Level 4: states the tie-break rule.
4. **Working-capital actions.** Each action with its cash impact in cents and the day-count convention. Level 4: both actions, each with
   its sign and its number.
5. **Recommendation and limits.** Names the action set and what would change it; states SIMULATED inputs and the covenant definition as
   limits. Level 4: names one change that would reverse the recommendation.

Exemplars: **exemplar-a (level 4)** and **exemplar-b (level 2)**, fully written, annotated with the descriptors each passage meets or
misses. Self-assessment `section.rubric-self` with `data-rubric="rubric"` and `data-exemplars="exemplar-a exemplar-b"` (M1, E1 pattern).
The page shows where the student's scores diverge from the exemplar scores.

Adversarial question bank: not required. The memo is not an IC defence or a debate (Q9 of E1 precedent; Q13 below).

### 5.8 Grader design (Builder D)

Files (no Atlas; the solution is unit-local, `check_projects.py` Atlas branch does not apply):
`course/modules/CF/CF8/grader/`: `instance.py`, `reference.py` (excluded from deployment, BLUEPRINT §7), `starter.py`
(`NotImplementedError` stubs; the suite must fail on it, `run_graders.py`), `test_project.py`.

Grader panel on `project.html`: `<section class="grader-panel" id="grader" data-unit="CF8" data-grader="grader/" data-suite="test_project.py" data-support="instance.py" data-solution="treasury_forecast.py" data-starter="starter.py" data-packages="">`.
`data-packages` is empty (standard library only; Q14).

- **`instance.py`**: `make_instance(seed: int) -> dict[str, Any]`, deterministic per seed, valid by construction (positive minimum cash,
  commitment at least the opening drawn balance, collections lag between 20 and 90 days). Docstring: "SIMULATED: generated inputs, not
  company data." Seeds 0-49 must give materially different pinch weeks and cash paths, not only different labels (check on 20 sampled seeds).
- **`reference.py`**: the full solution with `Fraction` and one half-up rounding per money output. Passes every test on seeds 0-49.
- **`test_project.py`** (properties and numbers; each test recomputes its expected value from the instance by an oracle written separately
  from `reference.py`; no hard-coded answer):
  - weekly identity: `ending_cash = opening + receipts - disbursements + draw - repay` to the cent, every week;
  - the revolver never exceeds its commitment; no draw exceeds availability; drawn balance never negative;
  - minimum cash is held in every week where the cap is not binding; a binding cap is reported as `shortfall_cents`, never hidden;
  - covenant pinch week is the argmin of headroom, earliest week on a tie; headroom equals liquidity minus threshold;
  - DSO and DIO shortening by `days` raises cash by the Fraction-exact amount, rounded once; lengthening DPO by `days` does the same;
  - the exception table (section 5.5): the three named conditions raise `ValueError` naming the condition;
  - every money key is an `int`.
  - Failure messages name the violated property and hint at the concept. They never print the answer.
- **Dual mode**: identical suite in Pyodide and pytest; each test under 5 s in Pyodide; the suite under 60 s.
- **Five alternative correct implementations** (all must pass; the verifier writes them as fixtures in a scratch checkout and archives the
  scripts under `ledgers/CF8/scripts/`): (1) a per-week loop with `Fraction`; (2) a float implementation with the stated half-up rule applied
  to the exact value of each output; (3) a closed-form shortfall-then-draw formulation (cumulative shortfall, one draw per week); (4) a
  dictionary-of-lists layout instead of a list of dicts; (5) a generator-based streaming implementation.

**Student-error mutants (verifier writes at least ten complete modules to `ledgers/CF8/mutants/*.py`, each docstring's first line naming
the error; `mutate_graders.py --unit CF8 --seeds 0-9`; every mutant must be killed):**

1. CCC with DPO added instead of subtracted (sign error).
2. DSO computed on cost of sales instead of revenue.
3. 360-day year used where the spec states 365.
4. Revolver draws only when cash is negative, ignoring minimum cash.
5. Revolver repays past the drawn balance (negative balance).
6. Covenant headroom computed on opening rather than ending liquidity.
7. Pinch week tie broken by the latest week instead of the earliest.
8. DSO shortening with the cash sign reversed.
9. DPO lengthening applied to receipts instead of disbursements.
10. One-week lookahead: week w uses week w+1 receipts.
11. Truncation instead of half-up rounding (breaks cent-exact checks on seeds where the fraction is `.5`).
12. A hard-coded answer for seed 0.

Each mutant must fail at least one test; a survivor is a FAIL. Equivalent mutants are listed only with a proof row (VERIFIER §2.6).

### 5.9 Starter and reference hygiene

`starter.py` has the four function names with `raise NotImplementedError`, so every test that calls one of them fails with a named property,
not a stack trace. `reference.py` never appears in deployment (BLUEPRINT §7).

## 6. Labs (what each lab computes; all exact, all standard library)

| Lab | Hypothesis to state before running (planner proposal) | Exact computation |
|---|---|---|
| `lab-CF8-L01-1` (curriculum lab) | the three day counts and the cash conversion cycle decompose the cycle exactly; a change in DSO moves CCC one-for-one | from a SIMULATED filer (company-facts shape, field names generic, no XBRL tag names typed), DSO, DIO, DPO, CCC with `Fraction`; decomposition identity checked |
| `lab-CF8-L02-1` | a credit-term extension has a break-even margin; an early-payment discount has an implied annual cost | break-even margin `m*` from the NPV of the extension, discounted at a stated rate; implied cost of `d/(1-d) * 365/(N-k)` with `Fraction` |
| `lab-CF8-L03-1` | the 13-week cash identity holds every week; the minimum-cash rule fixes the draw | seeded SIMULATED receipts and disbursements; weekly identity checked exactly |
| `lab-CF8-L04-1` | covenant headroom is smallest in the pinch week; a five-day DSO slip lowers receipts by the exact amount | headroom path, argmin, and DSO sensitivity |
| `lab-CF8-L05-1` | the shortfall frequency falls as the cash buffer rises, for a stated volatility | seeded `random.Random` simulation of a year of net flows; frequency against buffers; labelled SIMULATED |
| `lab-CF8-project-1` | rung 1: the reference case outcome | worked forecast, every line printed |
| `lab-CF8-project-2` | rung 2: the completed revolver line | completion twin |
| `lab-CF8-project-3` | rung 3: the engine on the reference case | calls `treasury_forecast.py` |

Labs state their hypothesis before running and their interpretation only after the printed output. Lab 5 seeds every RNG and prints
its seed. No lab reads any data file.

## 7. Cards and registry

### 7.1 Cards builder (Builder E, after A-D)

`course/modules/CF/CF8/cards.json`, ids `CF8-c001` upward, `lesson` in `L01`-`L05`, `front`, `back`, and `cite` (registry keys) or
`basis` for a result the lesson establishes itself (for example `"basis": "Lab 1 (curriculum lab, SIMULATED)"`). Each card tests one fact. Duplicates
are not allowed. Empirical cards cite a key with a grade of B or C and the counter-evidence named (Q10). A card with no registry key
and no `basis` is not allowed.

### 7.2 Registry keys the module may cite

| Key | Use in CF8 | Status |
|---|---|---|
| `bates2009us` | L05 precautionary holdings (evidence on rising cash holdings) and the reading list | cite by key; the record matches the curriculum string. Read the abstract before any claim; grade B at most; counter-evidence required (Q10) |
| `opler1999determinants` | L05 determinants of cash holdings; reading list | cite by key only under Q2. The record author list is "Opler" only; the prose uses the record's title, journal, volume and pages, not the four-author string |
| `net-present-value` (concept, not a key) | L02 | link to CF1 |

Not usable: `brealey2022principles` (CF1 Q3 precedent; the record disagrees with the curriculum string on author list and year). It
remains in `used_by` for CF8, which `check_projects` and the registry check may flag (`registry_flags`).

### 7.3 REFERENCE_REQUESTS (topics only; the architect resolves them through `add_reference.py`)

No bibliographic data is typed from memory. Each request states the topic, the needed lesson and the confidence.

1. Primary source on trade credit and supply-chain finance practice (L02). Grade C at best without it.
2. Primary source on commercial paper: the market's role and its backstop use by firms (L04, L05). Without it, commercial paper is a
   definition only (grade T for the definition, no market claim).
3. Published counter-evidence to Opler et al. and Bates et al. on corporate cash holdings (L05; two-sided rule, BUILDER_RULES §2.5).
4. Source on financial covenants and headroom in credit agreements (L04). Without it, covenant prose is a definition.
5. Source on day-count conventions for DSO, DIO and DPO (L01), only if the builder wants one. The default is that the convention is stated
   on the page (section 5.4), not cited.
6. Textbook source for the CF8 curriculum's third entry (Brealey, 14th ed.). Blocked until the registry record is corrected (Q3); the
   request is for the correction, not a new key.

### 7.4 DATA_REQUESTS

- SEC EDGAR company-facts (XBRL) for real filers, for L01 and the project, if the architect wants real figures. The source URL and the
  reuse statement are not in `tools/data_sources.yaml` (no EDGAR entry; planner grep). The page carries an honest-pending note naming this
  request (AC2 pattern). Until a reuse statement is quoted and the snapshot is recorded in `MANIFEST.json`, every filer is SIMULATED.

## 8. Notation and requests

### 8.1 Symbols the module uses (local, defined per lesson)

Program-wide registered symbols that could collide (`notation/notation.json`, eight entries): `T` (number of return observations, S1),
`\Phi, \Phi^{-1}` (M4), `\gamma_3`, `\gamma_4` (M4), `R^\ast` (AP1), `R^{e\ast}` (AP1), `R_f` (AP1, gross riskless return), `\mathbb{Q}` (AP1).
Registered macros include `\E`, `\Prob`, `\Var`, `\Cov`, `\se`, `\R`, `\indic`, `\SR`, `\PBO`, `\emgamma` (notation macros).

CF8 rules:

- The horizon is **`H`** (`H = 13` weeks), not `T`. Weeks are indexed `w = 1, ..., H`.
- The revolver rate is **`i_{\mathrm{rev}}`** (stated input). Never `R_f`, `r_f` or `R`.
- Revenue, cost of sales, receivables, inventory and payables use the local letters **`\mathrm{Rev}`, `\mathrm{COGS}`, `\mathrm{AR}`, `\mathrm{Inv}`,
  `\mathrm{AP}`**. Never `R` for revenue or return.
- The day counts are written **`\mathrm{DSO}`, `\mathrm{DIO}`, `\mathrm{DPO}`, `\mathrm{CCC}`** (plain LaTeX, not new macros).
- `\se` and `\E` are used only in L05 with their registered meaning. `\Phi` is not used.
- Money symbols are local (for example `C_w` for the cash balance in cents in week `w`); each is defined in the lesson where it first appears.

### 8.2 NOTATION_REQUESTS

- `\mathrm{DSO}`, `\mathrm{DIO}`, `\mathrm{DPO}`, `\mathrm{CCC}`: program-wide registration proposed, because CF7 (`debt-schedule`
  neighbour) and CF8 both use the day counts (Q15). Needed for: L01 and the project.

## 9. Real-data policy

- The curriculum names **no dataset** for CF8 (`curriculum/02-economics-finance-core.yaml:894-925`, no data field).
- No snapshot in `course/assets/data/market/` (`fx_daily.csv`, `fx_monthly.csv`, `ust_daily.csv`) is relevant. No `data-files` attribute on any lab.
- Every generated case is labelled **SIMULATED** on the lab hypothesis, the project page and the grader docstring (BLUEPRINT §5.3).
- The XBRL lab (`lab-CF8-L01-1`) uses a **generated filer in company-facts shape with generic field names**. The builder does not type XBRL
  tag names from memory. If a tag name appears in prose, it is read from the taxonomy source first, or it is left out.
- **Honest-pending note** on L01 and on the project page: "Real company filings in XBRL are not embedded. Their reuse terms are not
  recorded in `tools/data_sources.yaml`; see DATA_REQUESTS." No real company figure appears anywhere.
- No `MANIFEST.json` entry is needed. `DATA_REQUESTS` (section 7.4) is raised.

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder self-check (once per lesson or file while building; `--page Lnn` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit CF8              # --page L01 while in progress
.venv/bin/python tools/check_dag.py --unit CF8
.venv/bin/python tools/check_projects.py --unit CF8
.venv/bin/python tools/run_labs.py --unit CF8                 # --page L01 likewise
.venv/bin/python tools/run_graders.py --unit CF8 --seeds 0-49
.venv/bin/python tools/embed_labs.py course/modules/CF/CF8/L01.html     # per page; --refresh <lab-id> after a twin edit
.venv/bin/ruff check tests/labs/CF8 course/modules/CF/CF8/grader && .venv/bin/ruff format --check tests/labs/CF8 course/modules/CF/CF8/grader
.venv/bin/mypy tests/labs/CF8 course/modules/CF/CF8/grader
```

Verifier only (not builders): `.venv/bin/python tools/mutate_graders.py --unit CF8 --seeds 0-9`;
`.venv/bin/python tools/page_smoke.py --unit CF8` on a quiet machine; `.venv/bin/python tools/verify_refs.py --unit CF8`.

Full gate (CLAUDE.md), once, before any merge, never per builder: `.venv/bin/ruff check . && .venv/bin/ruff format --check .`;
`.venv/bin/mypy`; `.venv/bin/pytest`; `.venv/bin/python tools/render_curriculum.py && git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`;
`.venv/bin/python tools/build_site.py --check`; `.venv/bin/python tools/verify_refs.py --offline`; `.venv/bin/python tools/fetch_data.py --check`;
`.venv/bin/python tools/check_pages.py --all && .venv/bin/python tools/check_dag.py --all && .venv/bin/python tools/check_projects.py --all`.

Notes on the commands (checked by the planner against the tool sources):
- `check_pages`, `check_dag`, `check_projects` accept `--unit` (`check_pages.py` `check_hub`, `check_lesson`; `check_dag.py` `check_unit`;
  `check_projects.py` `check_unit`).
- `run_labs.py` runs each twin as `python -I -W error` (`run_twin`, lines 51-61) with `PYTHONHASHSEED=0` and `PATH=/usr/bin:/bin`.
  Labs must not depend on the environment beyond that.
- `run_graders.py` requires the starter to fail the suite (`grade`, around line 162-166).
- `page_smoke.py` is not run by builders (timing-sensitive).
- The planner did **not** execute any of these commands; they are read from the sources, not run.

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** The CF8 entry has no `atlas:` key and no atlas entry names CF8 (`curriculum/meta.yaml`). No `atlas/CF8.contract.md`
   is needed, and none is drafted here. `check_projects.py` skips the contract check.
2. **No debate.** No `debate:` key (`curriculum/02-economics-finance-core.yaml:894-925`). `check_pages.py` line 412 does not require a debate brief.
3. **Grading `both`.** The spec must say "autograder" and "rubric" verbatim (`grading_problems`). Rubric: 4-7 criteria, four levels each,
   exemplars at two or more levels (`rubric_problems`).
4. **One curriculum lab.** The curriculum names one lab (yaml 917). The five lesson labs and three project labs are planner proposals (BUILDER_RULES §3.4).
5. **`check_dag` sees linked uses only.** An unlinked use of `xbrl-standardization`, `revolver-circularity`, `cash-sweep`, `wacc` or a
   statistics term passes the tool. The verifier reads for them (VERIFIER §2.9).
6. **Registry `used_by` mismatch.** `brealey2022principles` lists CF8 but is not cited (7.2). `opler1999determinants` lists CF8 only.
   The CF1 ledger shows that a key cited by a module not in its `used_by` is a `registry_flags` entry; CF8 must not cite a key whose `used_by`
   lacks CF8 (none in this plan).
7. **Pyodide packages.** `data-packages=""` is intended (stdlib only). The architect should confirm the Pyodide runner accepts an empty list (CF1 Q6).
8. **Problem-set workload.** BUILDER_RULES §4.2.7 requires at least 3 problems in each of four tiers per lesson, each with a worked
   solution: at least 12 worked problems per lesson, 60 in the unit. This is the template minimum, not reduced here.

## 12. Open questions for the architect (numbered; each needs a decision before the builders start)

- **Q1 (hours).** Five lessons of 8 h and a 10 h project (20 %, planner recommendation), or four lessons of 9 h and a 14 h project (28 %)? The
  10 h project is tight for a 13-week forecast with a memo (section 5.6). Confirm.
- **Q2 (registry record, Opler).** `opler1999determinants` records one author ("Opler") against the curriculum's four. Options: (a) cite the key
  with the record's own title, journal, volume and pages, and say nothing about co-authors (planner recommendation, the CF1 Q3 pattern); (b)
  correct the record through `add_reference.py` or `references/corrections.json` first; (c) do not cite it. Decision needed before L05 is drafted.
- **Q3 (registry record, Brealey).** Do not cite `brealey2022principles` (its year and author list conflict with the curriculum string). Confirm.
  The curriculum's third source then has no usable key; the textbook request in 7.3 stands.
- **Q4 (spec frozen).** Approve or amend the four function signatures and their output keys (section 5.4) before building. There is no Atlas contract
  to freeze them against. Module name `treasury_forecast.py` (Q4 also covers the name).
- **Q5 (DAG, XBRL).** The curriculum lab is "from XBRL", but `xbrl-standardization` belongs to AC2, outside the closure (`curriculum.json` `concepts`).
  Option (a) plain prose and a `DAG_DEFECT` (planner recommendation); (b) add AC2 to CF8's prerequisites (a curriculum change; AC2 is 110 h, not proposed).
- **Q6 (covenant definition).** Minimum liquidity (cash plus undrawn revolver) at week end, chosen because it needs no EBITDA or leverage concept
  (CF2 is outside the closure). The curriculum names "financial covenant and headroom" without a type (`yaml:910`). Confirm.
- **Q7 (revolver interest).** A stated input rate, no circularity (CF7 owns the circular case, `revolver-circularity`). Confirm.
- **Q8 (day count and week).** 365-day year for DSO, DIO and DPO; 7-day weeks; 13 weeks as the horizon. Confirm.
- **Q9 (scope of the core text).** The core (yaml 899-902) names "inventory", "bank lines" and "the evidence on corporate cash holdings". The plan
  covers inventory only through DIO (no inventory model, no EOQ), bank lines only as the revolver, and the evidence only through the two
  curriculum papers, with counter-evidence required (Q10). Confirm, because these are scope words (section 2.1 item 4).
- **Q10 (two-sided evidence).** No registry key gives counter-evidence on cash holdings. Options: (a) L05 grades the two papers B at most and
  states a counter-evidence gap, with REFERENCE_REQUEST 7.3(3) open (planner recommendation); (b) admit a counter-evidence source first; (c) grade
  C and make no claim beyond the title. The two-sided rule (BUILDER_RULES §2.5) makes (b) or (c) necessary if the claim is B.
- **Q11 (figures).** None (CF1 Q6 precedent). Confirm.
- **Q12 (statistics terms).** L05 uses mean, quantile and standard error in plain words with no statistics link (CF1 Q2 precedent). Confirm.
- **Q13 (memo type).** The memo is not adversarial; no 15-angle question bank (E1 Q9 precedent). Confirm.
- **Q14 (Pyodide).** Confirm an empty `data-packages` is accepted for a standard-library grader (CF1 Q6, not checked by the planner).
- **Q15 (notation).** Request registration of `\mathrm{DSO}`, `\mathrm{DIO}`, `\mathrm{DPO}`, `\mathrm{CCC}` (section 8.2), or keep them as local
  plain LaTeX. Confirm.
- **Q16 (mutant count).** The brief requires ten student-error mutants (section 5.8 lists twelve candidates). The BUILDER default of three is
  raised to ten here. Confirm.
- **Q17 (name collision).** `net-working-capital` (CF1) and CF8's working-capital content: CF8 links CF1's concept and defines only the day
  counts and the cycle. Confirm, so the verifier does not flag the overlap as a double definition.

## 13. Blocking issues

- **No STOP.** The curriculum hours (50) satisfy every tool rule (section 1). The build may proceed once Q1-Q8 are decided.
- **Blocking for the L05 claims.** Q2 and Q10. Without them, L05 can state only what the builder has read, graded C, with no contested claim.
  L05's lab and definitions do not depend on these.
- **Blocking for the L01 lab's real-data wording.** None: the lab is SIMULATED. Q5 decides the wording of the XBRL reference only.
- **Not blocking, but structural.** `xbrl-standardization` and `revolver-circularity` are owned outside the closure (section 4). The
  architect should decide whether the curriculum lab should name XBRL at all (Q5).

## 14. After the builders

1. Orchestrator integrates; runs the section 10 targeted commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02, L03-L04, L05, project (with at least ten mutants and the five
   alternative implementations), cards. Failures return to the owning builder with only the failing rows.
3. Ledger at `ledgers/CF8.verification.json`; verifier scripts archived under `ledgers/CF8/scripts/`; mutants under `ledgers/CF8/mutants/`.
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. It is never merged incomplete.

## Architect decisions

Pending. This plan is the planner's proposal. The decisions in Q1-Q17 are required before the builders start.

## Architect decisions (2026-10-28, binding). Where the plan states a recommendation for an open question, follow it. Defaults for every module: concepts outside the prerequisite closure are plain prose with no link and no dfn; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields only or not at all (never edit a record, never type bibliographic data); no real data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST in plans/<UNIT>-open-items.md; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every grader; not adversarial, no question bank.
Module specifics: 5 x 8 h lessons and a 10 h project; do not cite opler1999determinants or brealey2022principles; XBRL is plain prose; covenant = minimum liquidity (cash plus undrawn revolver); revolver interest is a stated input rate; 365-day year and 7-day weeks; `treasury_forecast.py`; statistics terms in plain words; counter-evidence for L05 absent, so L05 states only what the lab shows (SIMULATED) and ungraded literature pointers are removed.
