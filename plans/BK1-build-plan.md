# BK1 build plan: Banking & Asset-Liability Management (2026-11-09)

Unit: **BK1 · Banking & Asset-Liability Management** · tier U · 90 h · prerequisites FC1, FI1, AC1 · no Atlas milestone ·
no debate key · grading `both` (autograder for the engine, rubric for the memo) · output directory
`course/modules/BK/BK1/` (part code `BK`) · lab twins `tests/labs/BK1/` · grader `course/modules/BK/BK1/grader/`.
Planner: Haiku, plan only. No lesson text, no git operations, no commits, no check tools run. Executors: Haiku builders,
then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every curriculum fact cites `file:line` read during planning. Anything not in the curriculum is marked
**NOT IN CURRICULUM**. Registry facts cite `references/references.json` by line. Planner-derived facts about the tooling were
read from the tool source, or obtained by running `tools/coursekit.py` through `.venv/bin/python` (`prerequisite_closure`,
`concept_owner`, the `topological_order` list). Closed forms in section 5 are planner derivations for the builder to re-derive
and the verifier to check. Nothing was typed from memory; where a fact is not in the repository it is listed as a request.

**Status: BLOCKING ISSUES EXIST (section 0.3).** The hours are feasible. The Basel III parameters and the bank-level data
are not available from any registry source or redistributable snapshot, and the lesson count against the builder-ownership
instruction needs an architect decision. Decisions Q1 to Q4 and Q9 in section 12 must be made before the affected builders start.

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part BK, code `BK`, title "Financial Institutions", order 8 | `curriculum/02-economics-finance-core.yaml:961-963` (code at 962) |
| STUDIO-BK requires `[BK1, FI1]`; the studio is not part of this unit | `curriculum/02-economics-finance-core.yaml:964-967` (requires at 967) |
| BK1 id and title | `curriculum/02-economics-finance-core.yaml:978-979` |
| Tier `U`, hours `90` | `curriculum/02-economics-finance-core.yaml:980-981` |
| Prereqs `[FC1, FI1, AC1]` (only) | `curriculum/02-economics-finance-core.yaml:982` |
| Core: "Why banks exist, maturity transformation, NIM, interest-rate risk in the banking book, the deposit franchise, capital and liquidity regulation (Basel III, LCR, NSFR)." | `curriculum/02-economics-finance-core.yaml:983-986` |
| `introduces` has 11 concepts (mapped to lessons in section 1) | `curriculum/02-economics-finance-core.yaml:987-998` |
| Sources: five free-text strings (Diamond 1984; Drechsler, Savov & Schnabl 2017 and 2021; Basel III framework (primary); Jiang, Matvos, Piskorski & Seru 2024) | `curriculum/02-economics-finance-core.yaml:999-1004` |
| Lab: "Economic value of equity under parallel and twist shocks." | `curriculum/02-economics-finance-core.yaml:1005` |
| Project "ALM engine"; brief: "Model a bank's repricing gaps, EVE and NII sensitivity, with deposit-beta assumptions made explicit and stress-tested."; deliverable "Tested model plus memo."; grading `both` | `curriculum/02-economics-finance-core.yaml:1006-1012` (title 1007, brief 1008-1010, deliverable 1011, grading 1012) |
| No `debate` key and no `atlas` key on BK1 | `curriculum/02-economics-finance-core.yaml:978-1012` (both absent) |
| No Atlas entry names BK1 | `curriculum/curriculum.json` `atlas` array (planner check: no entry's JSON contains "BK1") |
| JSON row mirrors the YAML (id, tier, hours, prereqs, sources, lab, project, grading) | `curriculum/curriculum.json:8423-8460` (id 8423, hours 8426, prereqs 8427, sources 8446, lab 8453, grading 8458) |
| All 11 concepts map to module BK1 in the concept index | `curriculum/curriculum.json` concept index: `basel-iii-capital` at 1437, `delegated-monitoring` at 2197, `liquidity-coverage-ratio` at 3609 (module BK1); planner count of owners = 11 |
| BK1 is a prerequisite of BK3 and SR1 (both build on BK1) | `curriculum/02-economics-finance-core.yaml:1047` (BK3 `prereqs: [BK1, FI1]`); `curriculum/05-macro-alternatives.yaml:437` (SR1 `prereqs: [BK1, E4]`, SR1 id at 433) |
| BS-FIN credential requires BK1; course map "Financial Markets & Institutions" lists FC1, BK1, FI4, BK4 | `curriculum/meta.yaml:63` and `curriculum/meta.yaml:79` |
| BK1 prerequisite closure (computed): **{AC1, CF1, E1, FC1, FI1, M1, M2, P0.1}** | planner run of `tools/coursekit.py` `prerequisite_closure("BK1")` |
| Concepts usable without definition (closure's `introduces`): **99** (AC1 12, CF1 10, E1 13, FC1 10, FI1 16, M1 14, M2 13, P0.1 11) | planner run, same function; per-module `introduces` in `curriculum.json` |
| Topological positions: BK1 31, FC1 26, FI1 18, AC1 4, CF1 11, E1 16, M1 2, M2 5, P0.1 0, E5 25, E2 23, FC2 30, FI4 33, LX1 36, BK4 32, SR1 49, PR4 86 | `curriculum/curriculum.json` `topological_order` (planner run of `coursekit`) |
| Built units: AC1, AC2, AC4, CF1, CF8, CS2, E1-E5, FC1, FC2, LX1, LX2, M1-M7, S7, SC1, BK4, AP1, PC3; FI1 is **not** built (no `course/modules/FI/`); P0.1 has no module directory | listing of `course/modules/*/` (planner run) |
| Nearest built prerequisite of BK1 (direct prerequisites ranked by topological position; FI1 at 18 is not built): **FC1** (position 26, built). Its plan is `plans/FC1-build-plan.md` (read in full for this plan) | topological positions above; `course/modules/FC/FC1/` exists |
| Sibling module in Part BK, built, with a plan: BK4 (prereq FC1 only) | `curriculum/02-economics-finance-core.yaml:1071-1075`; `plans/BK4-build-plan.md` (grep-located only: lines 28, 41, 45, 48, 374, 587) |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 90 h (`curriculum/02-economics-finance-core.yaml:981`). Tool rules:

- lesson `data-hours` 6-12 (`tools/check_pages.py` line 227);
- hub `data-hours-lessons + data-hours-project = 90` (`check_pages.py` lines 337-338);
- project share 10-40% of 90, i.e. 9 to 36 h (`check_pages.py` lines 339-340);
- lessons sum to the hub's lessons figure (`check_pages.py` lines 341-342).

Chosen split: **6 lessons × 10 h = 60 h; project 30 h (33.3%)**. 60 + 30 = 90. Feasible. No STOP condition on hours.

### 0.3 Blocking issues (architect decision required before the affected builders start)

**B1. Basel III parameters and formulas are not available from the registry.**
- The curriculum core names the LCR, the NSFR and Basel III capital (`yaml:983-986`).
- The only Basel record is `bisndbasel` (`references/references.json:2815`): `verified_by: issuer`, `type: primary`,
  `url: https://www.bis.org/committees/bcbs/standards`, `year: null`, `used_by: ["BK1", "BK4"]`. It verifies the title and the
  issuer of an index page. It does not contain the LCR or NSFR formulas, the HQLA categories, the outflow or inflow weights or any
  capital minimum, and no planner or builder has read those documents.
- Under BUILDER_RULES §1.1-§1.2 and §2.6 no formula, weight or ratio minimum may be typed from memory.
- Default: L05 and L06 define the concepts in words, state that the framework's parameters are not stated in this module,
  and the labs use weights that the page labels as the lab's own ILLUSTRATIVE parameters. Three REFERENCE_REQUESTS (section 7.2,
  R1-R3) name the framework documents for the architect to admit through `tools/add_reference.py`.

**B2. No redistributable bank-level data exists in the repository.**
- The project needs a bank's balance sheet and its deposit behaviour. The only embedded snapshots are `fx_daily`, `fx_monthly`
  and `ust_daily` (`course/assets/data/market/MANIFEST.json:5`, `:63`; `tools/data_sources.yaml:19`, `:53`, `:91`).
- FFIEC call reports are a BLUEPRINT §5.3 candidate, not a cleared source (`BLUEPRINT.md:316`). Their licence has not been read.
- Default: the project's balance sheet is SIMULATED (BUILDER_RULES §1.7), with an honest-pending note and a DATA_REQUEST (section 6).
  The H.15 snapshot `ust_daily` is used only for the observed rate move in lab L03 (section 6).

**B3. Lesson count against the builder-ownership instruction.**
- The instruction asks for about three lessons per builder across Builders A to E, with the last builder owning `project.html`,
  the grader and the project labs. With 90 h and 11 concepts, three lessons per builder for five builders would mean fifteen lessons
  of about 4 h each, below the 6 h minimum of §0.2. The recommended split (section 1) uses six lessons and four of the five builders.
  Decision Q2.

**B4. The project interface must be frozen before the project builder starts** (section 5.2). Decision Q9.

Non-blocking, for the architect to see: N1 DAG defaults for outside concepts (section 4, Q10); N2 Pyodide package list for a
standard-library grader (section 11, item 3, Q14); N3 optional registry keys (Q11).

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms, Q2)

6 lessons × 10 h = 60 h; project 30 h; total 90 h. Concept counts per row sum to 2+2+2+2+1+2 = 11, each concept in exactly
one row (`curriculum/02-economics-finance-core.yaml:987-998`).

| Lesson | Title (working) | Concepts it defines (`introduces`) | Lab (twin id, `tests/labs/BK1/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Why banks exist: delegated monitoring and maturity transformation | `delegated-monitoring`, `maturity-transformation` | `lab-BK1-L01-1`: a two-period maturity-mismatch arithmetic for one bank (fixed-rate asset over three years, funded by one-year deposits); the refinancing gap at the reset, exact in `Fraction`; the parameters are labelled ILLUSTRATIVE model inputs | 10 | Builder A |
| L02 | Net interest margin and the repricing gap | `net-interest-margin`, `repricing-gap` | `lab-BK1-L02-1`: a SIMULATED balance sheet with repricing months; the bucket gaps against the total rate-sensitive gap (identity check); NIM from the definition, exact | 10 | Builder A |
| L03 | Economic value of equity and net interest income sensitivity | `economic-value-of-equity`, `net-interest-income-sensitivity` | `lab-BK1-L03-1` (**the curriculum lab**, `yaml:1005`): EVE under a parallel shock and under a twist shock on the SIMULATED book; the 2022 move of the 3-month and 10-year yields from `ust_daily` as the observed twist (real data, section 6); checks listed in 3.3 | 10 | Builder B |
| L04 | The deposit franchise and deposit beta | `deposit-franchise`, `deposit-beta` | `lab-BK1-L04-1`: NII change for deposit betas of 0, 50% and 100% on the same book; linearity in beta checked exactly; no empirical beta typed | 10 | Builder B |
| L05 | Capital requirements: Basel III | `basel-iii-capital` | `lab-BK1-L05-1`: a capital ratio from its definition; post-loss ratio and the loss that reaches a stated ratio, exact; the ratio threshold is an ILLUSTRATIVE parameter, not a framework value | 10 | Builder C |
| L06 | Liquidity requirements: the LCR and the NSFR | `liquidity-coverage-ratio`, `net-stable-funding-ratio` | `lab-BK1-L06-1`: a liquidity ratio built from stock and flow buckets with ILLUSTRATIVE weights; the change in the ratio under a stated deposit run, exact | 10 | Builder C |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 60 / 30 | none | none | - | Builder A |
| project | ALM engine (`both`: autograder and rubric, section 5) | none | `lab-BK1-project-1` (rung 1), `lab-BK1-project-2` (rung 2, `class="lab completion"`), `lab-BK1-project-3` (rung 3 check) | 30 | Builder E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` | none | none | - | Builder E |
| cards | `cards.json` from L01-L06 | none | none | - | Builder F (after A-E) |

Builder D has no lesson under this split. If the architect releases D, the project's rubric exemplars (section 5.4) are the
natural work, with Builder E keeping `project.html`, the grader and the project labs (the last-builder rule). Q2 records the choice.

Ownership rule: each builder writes only its own lesson files and twins. Builder A writes the hub after L01-L02 exist. Builder E's
grader is independent of the lessons' text; its interface is frozen in section 5.2 before any builder starts.

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses, section 4):
- L01 uses the closure's AC1 `balance-sheet` and FC1 `financial-intermediary` (links allowed, section 2.3) and M1
  `present-value` only in prose.
- L02 uses L01's `maturity-transformation` (link to `L01.html#def-maturity-transformation`); defines `net-interest-margin` and
  `repricing-gap` before any use.
- L03 uses L02's `repricing-gap` and the closure's FI1 `duration` (link to `../../../concepts.html#duration`) and M2 `taylor-theorem`.
- L04 uses L03's `net-interest-income-sensitivity`; defines `deposit-franchise` and `deposit-beta`.
- L05 uses L03's `economic-value-of-equity` in prose only (a capital ratio is not an EVE measure); defines `basel-iii-capital`.
- L06 uses L01's `maturity-transformation` and L04's `deposit-franchise`; defines `liquidity-coverage-ratio` and
  `net-stable-funding-ratio`.

Hours check: 6 × 10 = 60 (hub `data-hours-lessons="60"`); project 30 (hub `data-hours-project="30"`); 90 total.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to BK1)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `plans/E5-build-plan.md` §2 (its carried-over rules),
`plans/FC1-build-plan.md` §2 and §5 (the autograder precedent: integer cents, exception table, five alternatives), this file.
Study `course/modules/AC/AC1/` (a built hub and lesson set) and `course/modules/FC/FC1/` for layout. `course/templates/` holds
the skeletons (`hub.html`, `lesson.html`, `project.html`, `studio.html`, `README.md`). Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) and rounded only
   at display. A page that shows a rounded figure states its rounding rule. Precedents: E5 plan §2.1 item 1; CF1 L01 Remark 5.2.
2. **Money is integer cents, end to end.** Every money output of the engine and of every lab is an `int` in cents, computed from
   exact `Fraction`s and rounded once, half away from zero, by the rule stated on the page (section 5.3). No float money, no tolerance
   on money. Basis-point rates are integers. Precedent: FC1 plan §2.1 item 8; BUILDER_RULES Core guardrails (money = i64).
3. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only what
   the printed numbers show. Precedent: M1 LESSON_TEXT_DEFECTS ("checked directly" with no lab behind it).
4. **Attribute nothing unread.** Only the registry keys in section 7.1 may be cited. Every statement that attributes a finding to
   Drechsler et al., Diamond, or Jiang et al. needs the builder to have read the abstract (VERIFIER_RULES §2.1). No page, table,
   coefficient, weight, ratio minimum or date is typed from memory. Basel III parameters are not stated (section 0.3, B1).
5. **Scope words need a computation or an explicit hypothesis.** "every", "all", "always", "never", "any", "most banks",
   "banks typically", "the deposit franchise protects", "regulators require" are used only where a derivation, a finite check or a
   lab makes the claim, or where the registry source says it (with the locator read). A finite enumeration is grade C with its
   basis named, not grade T (precedent: M1 L06).
6. **Define before use.** Each of the 11 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned lesson,
   never before it. Terms outside the 11 (net interest income, earning assets, rate-sensitive assets and liabilities, risk-weighted
   assets, high-quality liquid assets, outflows, inflows, net worth, deposit run, interest-rate risk in the banking book) are defined
   in prose at first use with a plain `<dfn>` and no `data-concept` (`tools/check_dag.py` skips a `<dfn>` without `data-concept`).
7. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation block lists its numbered Assumptions (A1, A2, ...)
   before the statement. Examples the builders must state: the NII result needs a 12-month horizon and a parallel or stated shock;
   the EVE definition needs a discount convention (monthly compounding of a nominal annual rate, section 5.2); the beta result needs
   beta in [0, 1]; the Taylor approximation needs a differentiable price in the shift.
8. **Grader rule** (section 5.5). Exception types are demanded only for the conditions the page names; the suite has ten
   student-error mutants and five alternative correct implementations; the reference passes seeds 0-49.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll in their own container;
   `page_smoke.py` is the verifier's check (`tools/page_smoke.py`).
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":`
    guard. `run_labs.py` runs each twin as `python -I -W error <twin>` (`tools/run_labs.py` lines 51-60; precedent
    `tests/labs/M1/lab-M1-L04-1.py`).
11. **Rates are basis-explicit.** Any yield or rate is stated with its unit (percent per year, or a decimal, or basis points), its
    compounding or discount basis, and its source. `tbill_3m` is on a discount basis (`tools/data_sources.yaml:101`); the page states
    that the model uses the published rate without conversion, or converts it with the convention written out (Q4).
12. **Failure messages never print the answer** (fixer rules: a failing check names the property and the concept, and prints no
    expected value; `__tracebackhide__` in test helpers).

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key from section 7.1, or a derivation on the page.
  A B- or C-graded claim names its published counter-evidence (BUILDER_RULES §2.5, BLUEPRINT §3). For BK1 the two-sided pair to
  address is the deposit-franchise and deposit-beta claims: Drechsler et al. (2017, 2021) and Jiang et al. (2024). The planner read
  none of their abstracts; the builder reads them before grading any sentence (Q12).
- Concepts: the 11 concepts of section 1 are defined once each. Prerequisite links: `href="../../../concepts.html#<id>"` for
  closure concepts (AC1, CF1, E1, FC1, FI1, M1, M2, P0.1); `href="Lnn.html#def-<id>"` for earlier BK1 lessons. A lesson never links
  a concept defined in a later lesson. Built prerequisite hubs may be linked (`../../FC/FC1/index.html`, `../../AC/AC1/index.html`,
  `../../CF/CF1/index.html`, `../../E/E1/index.html`, `../../M/M1/index.html`, `../../M/M2/index.html`); FI1 and P0.1 have no built
  page, so the hub links their concept anchors only.
- Concepts outside the closure are plain prose with no link and no `data-concept` (section 4).
- Labs: code lives once in `tests/labs/BK1/lab-BK1-Lnn-1.py` (and `lab-BK1-project-1..3.py`). The page carries `@@LAB:<file>@@` and
  `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-BK1-<page>-<n>`
  (`check_pages.py` line 258). Standard library only (`fractions`, `math`, `random.Random(seed)` if any); no network; under 10 s in
  Pyodide; no warnings (`-W error`).
- SIMULATED label: on every lab, figure or project input that uses a generated balance sheet or path (L02, L03, L04, L06 where
  generated, every project input). Exact closed-form checks are not labelled SIMULATED, but a lab whose parameters are model inputs
  says so and uses the word ILLUSTRATIVE for its weights.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `notation/notation.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references in code
  comments (precedent: M1 "Convention (project Q5)").
- Banned strings (`tools/check_pages.py` lines 58-74 `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the
  scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well
  known", "obviously", "clearly", and any ellipsis `...` outside code.
- Percent changes state the base and the direction. Basis points are integers. Hub lesson titles match each lesson's `<h1>` at
  integration.
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10 output
  contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols that BK1 must not give a different meaning (`notation/notation.json`):

| Registered symbol | Registered meaning (locator) | BK1 conflict and rule |
|---|---|---|
| `T` | number of return observations (periods) in a sample (`notation.json:112`, module S1) | **Conflict risk.** Maturity, horizon and the number of periods are not written `T`. Maturity or repricing time in months is `m`; the 12-month horizon is `h`; a number of periods is `n`. |
| `R_f` | gross riskless return for the period (`notation.json:142`, AP1) | Not used. A deposit rate is `r_D`, a market rate is `r`, a policy rate is `i` (defined where used). |
| `\mathbb{Q}` | risk-neutral (equivalent martingale) measure (`notation.json:147`, AP1) | Not used. |
| `R^\ast`, `R^{e\ast}` | SDF-payoff objects (AP1) | Not used. |
| `\Phi`, `\gamma_3`, `\gamma_4` | M4 | Not used. |
| `\E` (macro) | expectation operator (`notation.json:5`) | Used only for an expectation of a random quantity. The EVE and NII are deterministic model outputs and are not written with `\E`. |
| `\R` (macro) | real numbers | Standard. |

Local symbols (allowed; each defined on the lesson where it first appears and never redefined): `A` total assets, `L` liabilities
(not labour), `E` is **not** used for equity (write "net worth" or `NW`, defined on L03), `D` deposits, `\beta` deposit beta (in [0, 1];
integer basis points in code, as `beta_bp`), `\Delta r` a parallel rate shock, `\tau` a time in years, `m` a time in whole months,
`h = 12` the NII horizon in months, `G_b` the repricing gap of bucket `b`, `RSA_b`, `RSL_b` rate-sensitive assets and liabilities of
bucket `b`, `\mathrm{DF}(m)` the discount factor for `m` months, `\mathrm{EVE}` and `\mathrm{NII}`.

NOTATION_REQUESTS: none. The plan uses only local symbols and the registered `\R` macro.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the section structure of BUILDER_RULES §4.2 (items 1-9). Mandatory content, by lesson:

### 3.1 Lesson content

- **L01 `delegated-monitoring`, `maturity-transformation`.** Why a bank exists as an intermediary between savers and borrowers
  (`FC1` `financial-intermediary` linked). The maturity mismatch as arithmetic: a long asset and short funding, the refinancing gap at
  the reset. Diamond (1984) at paper level for the delegated-monitoring framework (`diamond1984financial`). Any claim that delegation
  is optimal or efficient is graded B at most, with the counter-evidence named after the abstract is read. The lab's numbers are
  ILLUSTRATIVE and carry no empirical claim.
- **L02 `net-interest-margin`, `repricing-gap`.** NIM = NII / average earning assets (a definition: T). Repricing buckets with the
  boundary convention (items repricing in months `m` with `0 < m <= 3` fall in the first bucket, and so on, section 5.2). The gap
  identity: bucket gap equals rate-sensitive assets minus rate-sensitive liabilities; the cumulative gap is the sum of bucket gaps
  (T). The lab checks the identity exactly on a SIMULATED table.
- **L03 `economic-value-of-equity`, `net-interest-income-sensitivity`.** EVE as the present value of assets minus present value of
  liabilities under a stated discount convention (a model definition: T in the model). The first-order sensitivity
  `EVE(shifted) - EVE(base) ~ -D_mod * EVE * shift` with the remainder stated, from `taylor-theorem` (M2) and `duration` (FI1,
  linked): a derivation, T, with the Taylor remainder bound shown. The NII sensitivity over a 12-month horizon for a parallel shock
  (T in the model: rate-sensitive positions reset at their months; weight `(h - m)/h` for a reset at month `m <= h`). The
  curriculum lab (`lab-BK1-L03-1`) runs the parallel and the twist cases.
- **L04 `deposit-franchise`, `deposit-beta`.** The deposit franchise as the funding that a bank earns from paying below-market
  rates on non-maturity deposits (definition in words; no empirical value). Deposit beta as the pass-through share of a market-rate
  change into the deposit rate, `beta` in [0, 1] (a definition). The NII effect of a shock is linear in beta (T, a derivation from
  section 5.2). Drechsler et al. (2017, 2021) cited at paper level for the claim that deposit funding and the rate environment interact;
  the grade is set after the abstract is read, with Jiang et al. (2024) named as counter-evidence for any claim about stability.
  No beta value is stated as an empirical fact.
- **L05 `basel-iii-capital`.** The capital ratio as capital over risk-weighted assets (definition, with risk weights as a given input).
  Post-loss ratio and the loss that brings a ratio to a stated level (T, algebra on the page). The Basel III framework's requirements
  are **not stated** in this lesson (`bisndbasel` names the framework; its parameters are not read; section 0.3 B1). The lesson states
  this sentence in the body, as honest pending.
- **L06 `liquidity-coverage-ratio`, `net-stable-funding-ratio`.** Each ratio is defined in words as a stock-or-funding measure over a
  flow-or-requirement measure; the Basel formulas and weights are **not stated** (section 0.3 B1). The lab uses ILLUSTRATIVE weights.
  The change in a ratio under a stated run is exact (T, in the lab's model). A claim that the LCR reduces run risk is not stated: no
  registry source supports it.

### 3.2 Lesson-level constraints

- Each lesson's "Where the canon breaks" section names at least one model limit and what changes without it. Examples the builders
  must cover: static balance sheet (no growth, no new loans); parallel and twist shocks only (no general curve dynamics); the
  deposit beta is constant over the horizon; a bullet cash flow at the reset or maturity month (no amortisation, no prepayment, no
  optionality); EVE carries non-maturity deposits at face (section 5.2).
- Each lesson has at least three Misconceptions, each with the wrong belief, why it is wrong and the evidence (a lab, a derivation or a
  registry key).
- Problem sets: BUILDER_RULES §4.2 item 7 requires at least three problems in each of the Mechanics, Proof, Empirical and Research tiers,
  each with a full worked solution inside `<details class="solution">`. That is twelve problems per lesson, seventy-two in all. This plan
  does not reduce the rule; the workload is recorded as Q15.
- Key-results table: claim, grade, keys (or basis: lab and line).
- Retrieval quiz: 8-15 items per lesson, each with an explanation read against the lesson.
- No lesson uses a term from outside the closure as a link (section 4).

### 3.3 Lab checks (what each lab must demonstrate; the printed output is embedded, never typed)

| Lab | Hypothesis (stated before the run) | Checks the twin performs |
|---|---|---|
| `lab-BK1-L01-1` | The refinancing gap at the reset equals the asset's principal minus the deposit principal rolled over, computed exactly. | Identity of the gap; the gap at two reset dates; no float money. |
| `lab-BK1-L02-1` | The bucket gaps sum to the total rate-sensitive gap; NIM from the definition. | Identity check; a boundary item at exactly 3 months lands in the first bucket. |
| `lab-BK1-L03-1` | EVE under zero shock equals the base PV difference; the twist with equal short and long shifts equals the parallel shift; the observed 2022 twist (`ust_daily`) is applied to the SIMULATED book. | Zero-shock identity; `twist(s, s) == parallel(s)` exactly; the first-order approximation against the exact PV with the remainder printed. |
| `lab-BK1-L04-1` | NII change is linear in beta: the change at beta 50% is half the change at 100%. | Exact linearity on the same book; sign at beta 0. |
| `lab-BK1-L05-1` | The post-loss ratio and the loss that reaches a target ratio, from the definitions. | Substitution check: the ratio at the solved loss equals the target exactly. |
| `lab-BK1-L06-1` | A deposit run of a stated size lowers the liquidity ratio by a computed amount under the lab's ILLUSTRATIVE weights. | The recomputed ratio after the run matches the closed form. |

---

## 4. DAG problems (concepts that natural BK1 content would use outside the closure)

Prerequisite closure of BK1 (computed): **{AC1, CF1, E1, FC1, FI1, M1, M2, P0.1}**, 99 usable concepts (section 0.1). Owners below are
from the concept index (`curriculum/curriculum.json`); the "BK1 cycle" column is the planner's check with `coursekit.prerequisite_closure`.

| Ref | Concept (owner) | Where natural BK1 content would use it | Cycle check | Resolution in this plan |
|---|---|---|---|---|
| D1 | `bank-run`, `uninsured-deposit-run`, `run-on-repo`, `liquidity-spiral` (SR1) | L06 deposit run; L01 refinancing run | **SR1 requires BK1** (`05-macro-alternatives.yaml:437`): BK1 must never depend on SR1 | Plain prose only ("a run on deposits"), no link, no `data-concept`. Q10 records that SR1 is not an option. |
| D2 | `moral-hazard`, `adverse-selection` (E2; prereqs E1, M4; topological 23) | L01 delegated monitoring (the agency problem behind monitoring) | No cycle | Plain prose. Option (Q10): add E2 to BK1's prerequisites (curriculum change). |
| D3 | `policy-rate` (E5; prereqs E1; built; topological 25) | L04 deposit beta and the policy-rate pass-through; L03 shock definition | No cycle | Plain prose "the central bank's policy rate". Option (Q10): add E5 to BK1's prerequisites. |
| D4 | `interest-rate-swap`, `swaption` (FC2 at 30; FI6 later) | L03 and L05 hedging of the banking book | No cycle for FC2 (topological 30 < 31) | Plain prose. Option (Q10): add FC2. |
| D5 | `repurchase-agreement`, `sofr`, `bank-reserves`, `central-bank-balance-sheet`, `repo-haircut` (FI4; prereqs FI1, E5; topological 33) | L06 high-quality liquid assets and reserves | No cycle | Plain prose; no FI4 link. |
| D6 | `lender-of-last-resort` (LX1; prereqs FC1, E5; topological 36) | L06 and L01 (the central-bank backstop) | No cycle | Plain prose. |
| D7 | `stress-testing`, `value-at-risk` (PR4; prereqs PR1, S4; topological 86) | The project's "stress-tested" brief; L03 scenarios | Adding PR4 would pull PR1 and S4 into the closure | Plain prose "scenario stress test", defined on the project page with no link. Q10. |
| D8 | `supplementary-leverage-ratio` (FI4) and the leverage ratio | L05 capital ratio, leverage versus risk-based | No cycle | Plain prose; the leverage ratio is named in words, no number. |
| D9 | `expectation`, `variance` (M4; prereq M2; topological 12) | L03 and the project's dispersion language | No cycle | Plain prose ("expected", "variance" as ordinary words) with no link. |
| D10 | High-quality liquid assets, outflows, inflows, risk-weighted assets, deposit insurance, interest-rate risk in the banking book | L05, L06 | **NOT IN CURRICULUM** as concepts (no concept row exists) | Plain `<dfn>` with no `data-concept` where defined in prose; no formula typed (B1). |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Q10 asks the architect to confirm the defaults.** `check_dag.py`
checks linked uses only (`tools/check_dag.py` module docstring, lines 2-22); an unlinked use of D1-D10 passes the tool, so the verifier reads
every lesson for these names (VERIFIER_RULES §2.9).

In-closure concepts BK1 may use with links, by owner:
- AC1 (built): `balance-sheet`, `double-entry-bookkeeping`, `accrual-accounting`, `statement-articulation`, `deferred-taxes`.
- CF1: `net-present-value`, `fisher-relation`, `real-vs-nominal-cash-flows`.
- E1: `monopoly` (deposit competition as market power, prose), `competitive-equilibrium`.
- FC1 (built): `financial-intermediary`, `bank-money-creation`, `exchange-vs-otc` (not needed unless used).
- FI1: `spot-rate`, `forward-rate`, `yield-to-maturity`, `duration`, `convexity`, `dv01`, `term-spread`, `curve-bootstrapping`.
  FI1 has no built page; the links go to `../../../concepts.html#<id>` (concept anchors exist, e.g. `id="duration"` at
  `course/concepts.html`).
- M1: `present-value`, `discount-factor`, `compounding-frequency`, `continuous-compounding`, `annuity`, `amortization-schedule`.
- M2: `taylor-theorem`, `derivative`, `partial-derivative`.
- P0.1: `evidence-grade`, `identification`, `robustness-check`, `project-ladder`, `citation-registry`.

---

## 5. Project (`project.html`, Builder E): ALM engine, autograder and rubric

### 5.1 Ladder (BLUEPRINT §5.1; `check_projects.py` line 33 requires the order: `RUNGS`)

1. **Rung 1, worked example** (`lab-BK1-project-1`, SIMULATED): one fully solved, annotated run of the engine on a fixed five-position
   SIMULATED book: the repricing gap table, the NII change for +100 bp, the EVE change for +100 bp, each with a "why" annotation. Cents,
   rounded per section 5.3.
2. **Rung 2, completion** (`lab-BK1-project-2`, `class="lab completion"`, SIMULATED): the NII weight line `(h - m) / h` and the deposit
   beta line are removed (`___`). Graded instantly. Its twin is the completed solution; every page line equals the twin line or
   contains a blank (`run_labs.py` completion rule; architect ruling 11 makes this the program's convention).
3. **Rung 3, independent project** (graded: autograder and rubric): the engine `alm.py` to the section 5.2 interface, plus a memo
   `memo.md` with the sections of section 5.4. `lab-BK1-project-3` is the rung-3 check: it recomputes the default state of the
   course's instance from the same inputs and prints the table the engine must produce.
4. **Rung 4, stretch** (optional, not graded): value the non-maturity deposits at a stated deposit rate and discount them (a deposit-value
   extension), with the hypothesis stated before the run. No ceiling. Not graded.

### 5.2 Spec (`dl.spec`; `check_projects.py` lines 34 and 41-49 require the terms and the grading words)

Terms: Context, Inputs, Required outputs, Constraints, Grading, Reading list (`SPEC_TERMS`, line 34).

- **Context.** A bank's asset-liability committee needs an engine that shows how net interest income over twelve months and the
  economic value of equity respond to a parallel or twist rate shock, with the deposit-beta assumption made explicit and
  stress-tested. The memo states the diagnosis the engine supports, with its limits.
- **Inputs.** A SIMULATED instance from `grader/instance.py`, `make_instance(seed) -> dict`, with keys: `positions` (a list of
  dicts with `cents: int`, `months: int | None`, `side: "asset" | "liability"`), `deposits_cents: int`, `beta_bp: int`,
  `base_rate_bp: int`, `shock_bp: int`, `twist_short_bp: int`, `twist_long_bp: int`. No real data (section 6).
- **Interface (planner proposal, frozen by Q9 before the builder starts).** `alm.py` exposes:
  - `Position(cents: int, months: int | None, side: str)`, a frozen dataclass. `months` is the whole number of months to the next
    repricing (floating) or to maturity (fixed); `None` marks a non-rate-sensitive position (cash, equity-like or other non-earning
    items), carried at face in EVE and absent from the gap table. `side` is `"asset"` or `"liability"`.
  - `DepositBook(cents: int, beta_bp: int)`, a frozen dataclass: non-maturity deposits. Their rate moves by `beta_bp / 10000` of a
    parallel market shock.
  - `bucket_index(months: int) -> int`: 0 for `0 < m <= 3`, 1 for `3 < m <= 6`, 2 for `6 < m <= 12`, 3 for `12 < m <= 60`, 4 for
    `m > 60`. The boundary rule is part of the spec.
  - `repricing_gap(positions) -> list[int]`: five integers, cents, asset minus liability per bucket over rate-sensitive positions.
  - `nii_change_cents(positions, deposits, shock_bp: int) -> int`: the 12-month NII change for a parallel shock (section 5.3 formula).
  - `ParallelShift(bp: int)` and `TwistShift(short_bp: int, long_bp: int)`, frozen dataclasses; `eve_cents(positions, deposits,
    base_rate_bp: int, shift) -> int` (section 5.3 formula).
- **Required outputs.** `alm.py` with the functions and classes above, a module docstring with the conventions block (sign, rounding,
  the boundary rule, the discount convention), and `memo.md`. The grader requires only `alm.py`.
- **Constraints.**
  - Integer cents: every money output is an `int`, computed from exact `Fraction`s, rounded once, half away from zero.
  - Valid input: the exception table of section 5.5 only.
  - Standard library only; no network; the same code runs in Pyodide and under pytest.
- **Grading.** Both. The autograder (`grader/test_project.py`, dual-mode) scores `alm.py`; the rubric (section 5.4) scores `memo.md`.
  The spec's grading entry must contain the words "autograder" and "rubric" (`check_projects.py` `GRADING_WORDS`, line 38, and
  `grading_problems`, lines 41-49, require both for `both`).
- **Reading list.** `ol.reading-list` cites `diamond1984financial`, `drechsler2017deposits`, `drechsler2021banking`, `jiang2024monetary`,
  and `bisndbasel` (registry keys only, section 7.1). Nothing else.

### 5.3 Rounding, conventions and formulas (stated once; used in every output)

- Time: `m` is a whole number of months, `m >= 1` for a position (section 5.5, named condition). Rates are nominal annual rates in
  integer basis points; `r = bp / 10000`.
- Discount factor: `DF(m) = (1 + r(m) / 12) ** (-m)` with `r(m) = (base_rate_bp + shift(m)) / 10000`: monthly compounding of a nominal
  annual rate, exact in `Fraction` for integer `m`.
- Shift: `ParallelShift(s)` gives `shift(m) = s` for all `m`. `TwistShift(s, l)` gives `shift(m) = s` for `m <= 3`,
  `shift(m) = l` for `m >= 120`, and linear interpolation in `m` between them (exact in `Fraction`).
- EVE: `EVE = sum over assets of PV_i - sum over liabilities (other than DepositBook) of PV_i - deposits_cents`, where
  `PV_i = cents_i * DF(m_i)` for a positioned item and `PV_i = cents_i` for `months is None`. Deposits are carried at face (a stated
  model limit). Net worth is `A - L` in the same convention (defined on L03; not a separate output).
- NII over horizon `h = 12` months, parallel shock `s` in bp: `NII = sum over assets with 1 <= m <= 12 of cents * s/10000 * (12 - m)/12`
  `minus sum over liabilities with 1 <= m <= 12 of cents * s/10000 * (12 - m)/12` `minus deposits_cents * (beta_bp/10000) * s/10000`.
  Positions with `m > 12` contribute nothing; `None` contributes nothing.
- Rounding: every money output (`repricing_gap` entries, `nii_change_cents`, `eve_cents`) is the exact `Fraction` rounded once to an
  integer number of cents, half away from zero. No intermediate rounding. This is the stated rule on the project page.
- Signs: assets and liabilities enter with their own sign; a rate rise is a positive shock.

### 5.4 Rubric (memo, `table.rubric#rubric`; `check_projects.py` `rubric_problems`, lines 58-73)

Five criteria. Each criterion is one table row: the name in a `th`, and exactly four `td` cells for levels 4 down to 1 (the tool
counts `td` cells). Every level descriptor is observable.

1. **Gap reading.** Level 4: states each bucket's gap in cents from the engine, names the boundary rule and applies it to the item
   that repricing at exactly 3 months. Level 1: "reads the gap table".
2. **Computation and rounding.** Level 4: states the rounding rule, shows the unrounded value for each reported money figure, and
   the discount convention. Level 1: "rounds the numbers".
3. **Deposit beta.** Level 4: states beta as an input in basis points, reports the NII change at two betas, and marks which numbers
   depend on the assumption. Level 1: "discusses deposits".
4. **Shocks and signs.** Level 4: reports the parallel and twist results with their signs, and states why the twist with equal
   shifts equals the parallel case. Level 1: "shows some scenarios".
5. **Limits and evidence.** Level 4: names the model limits used in the diagnosis (static balance sheet, bullet cash flows, face
   value for deposits in EVE, constant beta), and states the counter-evidence for each claim graded B or C, with the registry key.
   Level 1: "notes some caveats".

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, fully written memos on a SIMULATED instance,
annotated with the descriptors each passage meets or misses; the annotations stay in the HTML (architect ruling 15). Self-assessment
form (`section.rubric-self`, `data-rubric="rubric"`, `data-exemplars="exemplar-a exemplar-b"`). The page shows where the learner's
scores diverge from the exemplar scores. Calibration: a dedicated scorer who has not opened the project page scores both exemplars
blind, using a stripping script over the file (architect rulings 15 and 23); the scores must agree within one level per criterion.
Adversarial question bank: not required (the architect default; Q13).

### 5.5 Grader design (Builder E): `course/modules/BK/BK1/grader/`

Files: `instance.py`, `reference.py` (the full solution; excluded from deployment, BLUEPRINT §7 and architect ruling 4), `starter.py`
(stubs raising `NotImplementedError`), `test_project.py`. The student file is `alm.py`. Grader panel on `project.html`:
`<section class="grader-panel" id="grader" data-unit="BK1" data-grader="grader/" data-suite="test_project.py"
data-support="instance.py" data-solution="alm.py" data-starter="starter.py">` (`check_projects.py` lines 123-136 require these
attributes and files; `run_graders.py` `panel`, lines 43-47). `data-packages` is empty (standard library only; Q14).

- `instance.py`: `make_instance(seed: int) -> dict` (the signature `check_projects.py` line 136 tests). Deterministic per seed from
  `random.Random(seed)`. Generates a book of four to six positions, a deposit book with `beta_bp` in `[0, 10000]`, a base rate in
  `[0, 800]` bp, a shock in `[50, 300]` bp, and a twist pair. Every seed valid. Labelled **SIMULATED** in the docstring. The answers
  must change across seeds: `run_graders.py` `check_instances` (lines 79-105) fails if two of seeds 0-19 give identical instances, and
  the verifier checks that the NII and EVE values change, not only labels.
- `reference.py`: the full solution with `Fraction` and one half-away-from-zero rounding per output. Passes every test on seeds 0-49.
- `starter.py`: stubs that raise `NotImplementedError`. The suite fails on it, naming the property, not a stack trace.
- `test_project.py` (properties and numbers; each test recomputes its expected value with an oracle written separately from
  `reference.py`):
  - **Gap identity:** bucket gaps sum to the signed sum of rate-sensitive positions; `None` positions are absent (both directions).
  - **Boundary:** `bucket_index` at 3, 4, 6, 7, 12, 13, 60, 61 (both sides of each edge).
  - **NII:** zero shock gives zero; sign follows the shock; the oracle formula equals the engine on every seed; a deposit-only
    book at beta 0 gives zero; a hand fixture (section 5.3 example: one asset of 1,000,000 cents resetting at month 6, deposits of
    500,000 cents at beta 5000 bp, shock +100 bp, net +2,500 cents, computed by hand on the page).
  - **EVE:** zero shock equals the base PV difference (oracle); **`TwistShift(s, s)` equals `ParallelShift(s)` exactly, on every seed**
    (kills the twist-as-parallel mutant); the EVE sign: assets' PV minus liabilities' PV (kills the sign mutant).
  - **Discounting:** `DF(m)` equals `(1 + r/12) ** -m` in `Fraction`; a hand fixture at `m = 12` with base 1200 bp (computed on the page).
  - **Integer output:** every money value is an `int`.
  - **Exception table (section 5.5):** only the named conditions raise `ValueError`, and the message names the condition.
  - **Rounding:** a fixture whose exact value ends in `.5` cents rounds away from zero (kills the truncation mutant).
  - Failure messages name the violated property and the concept (for example "the gap identity fails: bucket gaps do not sum to the
    rate-sensitive total"), never the expected value (`__tracebackhide__`).
- Dual mode: the same suite runs in Pyodide and under local pytest; each test under 5 s in Pyodide; the suite under 60 s.
- **Five alternative correct implementations** (each must pass seeds 0-49; the verifier writes them under `ledgers/BK1/alternatives/`
  and archives the scripts under `ledgers/BK1/scripts/`): (1) a class-based engine (a `Book` class with methods); (2) a comprehension
  and generator style with `typing.NamedTuple` positions; (3) a `Fraction`-throughout engine with a single final half-away-from-zero
  step written on numerator and denominator (a different code path for the same rule); (4) a month-by-month iterator that builds the
  discount factors by repeated division, exact in `Fraction`; (5) a `decimal.Decimal` engine at precision 60 with `ROUND_HALF_UP`
  applied to the magnitude. An alternative that disagrees with the stated exact rule on any seed is a mutant, not an alternative
  (architect ruling 10); a float-based alternative is not used.
- **Ten student-error mutants** (single-change copies of the reference under `ledgers/BK1/mutants/`, each opening with a one-line
  docstring that names the student error; `tools/mutate_graders.py --unit BK1 --seeds 0-9`; each must fail at least one test):
  1. bucket boundary taken as `[lo, hi)` instead of `(lo, hi]` (a repricing at exactly 3 months lands in the next bucket);
  2. the gap table includes `None` positions, treating them as repricing now;
  3. EVE sign reversed (liabilities minus assets);
  4. simple discounting `1 / (1 + r * m / 12)` in place of monthly compounding;
  5. deposit beta ignored (deposits reprice fully with the shock);
  6. beta used as `1 - beta` (the complement);
  7. the twist applied as a parallel shift using the short shift for every month;
  8. the NII weight `(12 - m)` without the division by 12 (a unit error);
  9. a hard-coded NII answer for seed 0;
  10. rounding by truncation toward zero instead of half away from zero.
- Equivalent mutants (if the verifier finds any that differ only where the page states nothing): they go to `ledgers/BK1/equivalent/`
  with a README proof (architect ruling 9). Mutants that differ only below a stated accuracy follow ruling 25.

### 5.6 Time budget (`<table id="hours">`, sums to 30 h; every row needs a one-line rationale)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One solved SIMULATED book, annotated line by line |
| Rung 2, completion problem | 3 | Fill the NII weight and the beta line, then run the instant check |
| Gap table and boundary rule (`bucket_index`, `repricing_gap`) | 6 | Bucket edges, the boundary test, the gap identity, the rounding of each bucket |
| EVE and the discount convention (`DepositBook`, shifts, `eve_cents`) | 5 | Monthly compounding in `Fraction`, the twist interpolation, the sign convention |
| Deposit beta and stress scenarios (`nii_change_cents`, the beta range check) | 3 | The 12-month weight, the beta range as a named condition, the parallel and twist runs |
| Validation: instance checks and seeds 0-9 locally | 3 | The determinism and seed-variation checks, the exception table, a local pytest run |
| Memo (five rubric sections, exemplars read) | 6 | Five sections with cents, the beta assumption, the limits and the counter-evidence |
| Self-assessment against exemplars | 2 | Score the memo with the rubric, then compare with exemplar-a and exemplar-b |
| **Total** | **30** | Equals `data-hours-project` on the hub |

---

## 6. Real-data policy

- **Embedded and cleared: `ust_daily`** (`course/assets/data/market/ust_daily.csv`; MANIFEST entry at
  `course/assets/data/market/MANIFEST.json:63`). Columns `tbill_3m` and `cmt_10y`, percent per year, daily, 2000-01-03 to 2026-09-30
  (MANIFEST: `rows` 6690, `retrieved` 2026-10-20, `licence_url` `https://www.federalreserve.gov/disclaimer.htm`). The licence quote and
  the notes are at `tools/data_sources.yaml:91-116` (licence 95, note 100-106, transform 108). The Board's grant is quoted there:
  "Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without
  permission." The H.15 `cmt_10y` names the U.S. Treasury as its source, a work of the U.S. Government (`data_sources.yaml:101-105`).
  The planner did not open `licence_url` (no network use in planning); the verifier opens it and checks the quoted text (VERIFIER §2.8).
- **Use in lab `lab-BK1-L03-1` only.** `data-files="ust_daily.csv"` on the section; the file is opened as `data/ust_daily.csv`. The
  observed twist is the 3-month and the 10-year change between two dates present in the file: `2022-01-03` (row 5506 of
  `ust_daily.csv`, values 0.09 and 1.63) and `2022-12-30` (row 5754, values 4.30 and 3.88). The builder recomputes these changes from
  the file; the planner read the two rows only as locators. The lab's hypothesis and interpretation cite the citation string
  ("Board of Governors of the Federal Reserve System, H.15 Selected Interest Rates") and the retrieval date from MANIFEST (2026-10-20).
  The short leg is a discount-basis rate (`data_sources.yaml:101`), so the lab applies the observed changes to the model's rates with
  no basis conversion and says so (Q4). A two-point observed move does not identify a full twist; the page says so.
- **Not embedded, no grant read: bank-level balance sheets and deposit data.** FFIEC call reports are a BLUEPRINT candidate
  (`BLUEPRINT.md:316`), not cleared. **The project is SIMULATED.** Honest-pending note on the project's data section, in the words:
  "No bank-level data is embedded. The balance sheet is generated and labelled SIMULATED. A call-report source has not been checked
  for redistribution." Cited to the DATA_REQUEST in section 7.3.
- **No real rate for the policy rate.** `ust_daily` has no federal funds series (`data_sources.yaml:91-116`); the policy rate is not
  used as data anywhere in BK1.
- **No empirical deposit-beta value** is typed anywhere. Beta is an input to the lab and the project.
- **Bring-your-own-data** is not used for BK1 v1 (Q3). A student-supplied call-report CSV would need a schema, validation in the browser
  and an autograder that accepts it; the hours do not cover that.
- No `data-files` attribute on any lab except `lab-BK1-L03-1`. No MANIFEST entry is added by builders.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

| Key | Record (as read) | Status | Use in BK1 |
|---|---|---|---|
| `diamond1984financial` | Diamond, "Financial Intermediation and Delegated Monitoring", *The Review of Economic Studies* 51(3), DOI 10.2307/2297430, Crossref, year 1984, pages "393" (`references/references.json:6815`); `used_by: ["BK1"]` | verified; source string matches `yaml:1000` | L01 `delegated-monitoring` (paper level); reading list |
| `drechsler2017deposits` | Drechsler, Savov & Schnabl, "The Deposits Channel of Monetary Policy", *QJE* 132(4), DOI 10.1093/qje/qjx019, year 2017 (`references/references.json:7130`); `used_by: ["BK1"]` | verified; source string matches `yaml:1001` | L04 deposit franchise and beta (grade after the abstract is read); reading list |
| `drechsler2021banking` | Drechsler, Savov & Schnabl, "Banking on Deposits: Maturity Transformation without Interest Rate Risk", *JF* 76(3), DOI 10.1111/jofi.13013, year 2021 (`references/references.json:7174`); `used_by: ["BK1"]` | verified; source string matches `yaml:1002` | L01, L03, L04 (grade after the abstract is read); reading list |
| `jiang2024monetary` | Jiang, Matvos, Piskorski & Seru, "Monetary tightening and U.S. bank fragility in 2023: Mark-to-market losses and uninsured depositor runs?", *JFE* 159, DOI 10.1016/j.jfineco.2024.103899, year 2024 (`references/references.json:13636`); `used_by: ["BK1"]` | verified; source string matches `yaml:1004` (case of the title differs only) | L03 and L04 counter-evidence and fragility claims (after the abstract is read); memo; reading list |
| `bisndbasel` | "Basel III: international regulatory framework for banks", Bank for International Settlements, `https://www.bis.org/committees/bcbs/standards`, `verified_by: issuer`, year null (`references/references.json:2815`); `used_by: ["BK1", "BK4"]` | verified at index level only | L05 and L06: names the framework at document level. No parameter, formula or weight is cited to it (B1). |

Year agreement: the registry years match the curriculum strings for the four papers (1984, 2017, 2021, 2024). `bisndbasel` has no year to conflict.
No year or edition conflict is recorded for BK1.

Keys that exist and are used by other modules, not curriculum-listed for BK1 (optional; Q11): `diamond1983bank` (`references/references.json:6775`,
`used_by: ["SR1"]`, Diamond and Dybvig on deposit insurance and runs), `bis2014basel` (`:2695`, `used_by: ["SR4"]`, leverage ratio),
`frb2023fed` (`:9107`, `used_by: ["GM5"]`, the Federal Reserve's review of its supervision of Silicon Valley Bank). Not used by default.

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- R1. The Basel Committee's LCR standard as published on the Bank for International Settlements website (bis.org is allow-listed,
  `references/authorities.yaml:22`). Needed for: L06, the LCR definition, the HQLA categories and the outflow and inflow weights. Until
  admitted, L06 states that the weights are not stated in this module. Confidence in the topic: certain; no record identified by the planner.
- R2. The Basel Committee's NSFR standard, same publisher. Needed for: L06, the NSFR definition and factors. Same status as R1.
- R3. The Basel Committee's capital standard text (the Basel III framework's capital pages, on bis.org). Needed for: L05, the capital
  minimum, the buffers and the risk-weight concept. `bisndbasel` names the framework only. Until admitted, L05 states no minimum.
- R4. The Basel Committee's standard on interest-rate risk in the banking book (bis.org). Needed for: L03, if a claim about the
  regulatory EVE or NII shock sizes is made. Not needed for the v1 build, because the lab and the project use declared scenario
  parameters and claim no regulatory scenario. Its existence is a topic lead only.
- R5. Empirical estimates of deposit pass-through (deposit beta) for the period and the market that L04 and the project's memo would
  discuss. Needed for: any B- or C-graded beta claim with its counter-evidence (BUILDER_RULES §2.5). The planner names no author or record.
- R6. Empirical work on deposit runs and deposit insurance, as counter-evidence to the stability reading of deposits in L01 and L06. Lead
  only; `diamond1983bank` (optional, Q11) is the only registry candidate and is not curriculum-listed for BK1.

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4). Until
resolved, the lessons teach the models by derivation, and each empirical sentence is graded C at most with its basis named, or removed.

### 7.3 DATA_REQUESTS (for the architect; the planner names no licence from memory)

- D-a. A call-report source for bank balance sheets (the BLUEPRINT candidate FFIEC call reports, `BLUEPRINT.md:316`): the issuer's
  URL to be read by the architect, the licence sentence quoted, the licence page, and the transform (BUILDER_RULES §6.6 steps 1-5). Needed
  for: a real-data version of the project's balance sheet, if the architect wants one in a later version. Not needed for v1.
- D-b. Additional constant-maturity tenors from the same H.15 release that holds `cmt_10y` (the release is named in
  `tools/data_sources.yaml:6-7`): for example a short and an intermediate tenor, so that a twist can be identified on more than two
  points. The series identifiers are to be read from the release, not typed here. The same grant text applies only after the
  architect checks the release's terms (`data_sources.yaml:95-100`).
- D-c. The federal funds rate series of the same H.15 release, for the policy-rate pass-through in L04 (`data_sources.yaml:91-116`
  does not embed it). Identifier to be read from the release.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for BK1 (section 0.1). No `atlas/BK1.contract.md` is needed or drafted. The Atlas
contracts A8 and A15 exist (`atlas/`) and are not needed.

---

## 9. Cards builder (Builder F, after A-E)

- `course/modules/BK/BK1/cards.json`, ids `BK1-c001` upward (`check_pages.py` line 381 requires `BK1-c\d{3}`), `lesson` in `L01`-`L06`
  (`check_cards`, lines 366-398), `front`, `back`, `grade` (T/A/B/C/D/X), and either `cite` (registry keys from section 7.1) or `basis`
  (the lab or derivation that establishes the result, for example `"basis": "Lab L02-1 (exact)"`).
- One card per definition, theorem statement, key formula, key result (with its grade) and misconception (BUILDER_RULES §7). Each lesson
  contributes at least one card. No duplicates.
- Grade T for every derivation, with `basis` naming the lab or derivation. `cite` is `[]` for a model result. A card stating a
  paper-level claim cites its registry key and carries the grade set after the abstract is read.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`; cards for an ILLUSTRATIVE-weight result say so in the back.
- Cards for the Basel formulas are not written (B1).

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit BK1            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit BK1
.venv/bin/python tools/check_projects.py --unit BK1
.venv/bin/python tools/run_labs.py --unit BK1               # --page L03 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/BK/BK1/L01.html                          # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/BK/BK1/L03.html --refresh lab-BK1-L03-1  # after editing a twin
.venv/bin/python tools/run_graders.py --unit BK1 --seeds 0-49   # project builder, after reference.py and test_project.py exist
.venv/bin/ruff check tests/labs/BK1 course/modules/BK/BK1/grader && .venv/bin/ruff format --check tests/labs/BK1 course/modules/BK/BK1/grader
.venv/bin/mypy tests/labs/BK1 course/modules/BK/BK1/grader  # strict, repository configuration
```

Verifier only, on a quiet machine: `.venv/bin/python tools/mutate_graders.py --unit BK1 --seeds 0-9` (the ten mutants),
`.venv/bin/python tools/page_smoke.py --unit BK1` (not run by builders; timing-sensitive), `.venv/bin/python tools/verify_refs.py --unit BK1`
(the unit ledger's registry run, VERIFIER §2.1), and `.venv/bin/python tools/fetch_data.py --check` (offline; confirms `ust_daily` against
MANIFEST, BUILDER §6.6).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`, and the
full gate in CLAUDE.md.

Flags: `check_pages.py` and `check_dag.py` accept `--unit`; `check_projects.py` accepts `--unit` (`main`); `run_labs.py` accepts `--unit`
and `--page`; `run_graders.py` accepts `--unit`, `--all`, `--seeds` (lines 126-131); `mutate_graders.py` accepts `--unit` and `--seeds`
(lines 27-39). The planner did not execute the builder commands.

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** No `atlas:` key on BK1 (`yaml:1006-1012`) and no Atlas entry names BK1. `check_projects.py` skips the contract
   check (lines 144-145).
2. **No debate.** BK1 has no `debate:` key (`yaml:978-1012`), so `check_pages.py` does not require a debate brief (lines 412-413). The
   deposit-beta and deposit-franchise claims are contested in the literature, so the two-sided rule (BUILDER_RULES §2.5) applies anyway.
3. **Numpy in the grader runner.** `tools/run_graders.py` imports numpy at module level (line 35) and fingerprints instances with numpy
   (lines 88-96). The BK1 suite and labs are standard-library only, so `data-packages=""` is intended. The planner did not verify that the
   Pyodide runner accepts an empty list or that numpy is not needed in the browser path (Q14; FC1 plan §8.2 item 1 records the same gap).
4. **Rung-2 completion lab.** `check_projects.py` requires a completion lab or a quiz for module projects (lines 89-90, `section.completion`
   or `section.quiz`). The plan uses a completion lab (architect ruling 11).
5. **Placement bar.** `check_hub` requires `section.quiz#placement` with `data-mastery` and at least two `data-skill` items
   (`check_pages.py` lines 350-355). The bar value is the builder's choice; the FC1 plan's 0.8 is a precedent (`plans/FC1-build-plan.md` section 4).
6. **Built links.** Built prerequisite hubs (`course/modules/FC/FC1/`, `AC/AC1/`, `CF/CF1/`, `E/E1/`, `M/M1/`, `M/M2/`) may be linked. FI1 and
   P0.1 have no page (`course/modules/` listing), so the hub links concept anchors only.
7. **check_dag sees linked uses only.** Unlinked uses of D1-D10 (section 4) pass the tool; the verifier reads for them (VERIFIER §2.9).
8. **Studio not in scope.** STUDIO-BK (`yaml:964-976`) requires FI1 as well, and FI1 is not built. The studio is not part of this unit.
9. **Notation is local.** No registered symbol covers bank quantities; the local symbols of section 2.3 are defined on their lessons.
10. **The lab count versus the budget.** Six lesson labs plus three project labs make nine twins. This follows the E5 and FC1 precedents
    (architect Q2 in those plans).

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **(BLOCKING for L05 and L06 Basel content) Basel III parameters.** The LCR, NSFR and capital formulas, weights and minima are not in the
   registry and were not read (section 0.3 B1). **RECOMMENDED:** admit R1-R3 through `tools/add_reference.py` by their bis.org URLs; until
   then, L05 and L06 teach the definitions in words, state that the parameters are not stated in this module, and the labs use ILLUSTRATIVE
   weights labelled as the lab's own. Builders type no number from memory.
2. **(BLOCKING for the builder split) Lesson count and ownership.** The instruction asks for about three lessons per builder across
   Builders A to E. **RECOMMENDED:** six lessons of 10 h, project 30 h; Builder A: L01, L02, index.html; Builder B: L03, L04; Builder C:
   L05, L06; Builder D: released (no lesson); Builder E: `project.html`, grader, project labs; Builder F: cards. The alternative of nine
   lessons of 6 h with a 36 h project (40%, the upper limit at `check_pages.py` line 339) gives three lessons per builder for A to C,
   with D and E as in the recommendation. Both are within the hours rules.
3. **(BLOCKING for the project data) SIMULATED bank.** No bank-level data is cleared (section 6). **RECOMMENDED:** the project and its
   autograder use a generated SIMULATED book with the honest-pending note; no bring-your-own-data mode in v1; D-a (FFIEC) is a request.
4. **Observed twist from `ust_daily`.** **RECOMMENDED:** use the 2022-01-03 to 2022-12-30 change in `tbill_3m` and `cmt_10y` (rows 5506 and
   5754 of `ust_daily.csv`) as the observed twist in `lab-BK1-L03-1`, applied to the SIMULATED book, with no basis conversion, the
   discount basis stated (`data_sources.yaml:101`), and the two-point limit stated on the page. Alternative: drop the observed scenario and
   use declared shocks only.
5. **Scenario sizes.** The parallel shock (100 bp in the lab), the instance ranges (shock 50-300 bp) and the twist pivots (3 and 120 months)
   are declared scenario parameters. **RECOMMENDED:** keep them, state on the page that they are this module's parameters and that no
   regulatory scenario is claimed (R4 is not needed for v1).
6. **Deposit beta.** **RECOMMENDED:** beta is an explicit input in integer basis points in `[0, 10000]`, with a named `ValueError`; the lab
   uses 0, 50% and 100%; no empirical beta is stated unless R5 is admitted and read.
7. **EVE convention.** **RECOMMENDED:** monthly compounding of nominal annual rates; floating and fixed positions as bullets at their
   months; non-rate-sensitive items at face; non-maturity deposits at face (so beta enters NII and not EVE); the model limit stated on
   the page, and the deposit-value extension left to rung 4.
8. **Rounding rule.** **RECOMMENDED:** every money output rounded once, half away from zero, to the cent; no tolerance on money
   (FC1 plan §2.1 item 8 precedent).
9. **Interface freeze.** **RECOMMENDED:** freeze section 5.2 (`Position`, `DepositBook`, `bucket_index`, `repricing_gap`,
   `nii_change_cents`, `ParallelShift`, `TwistShift`, `eve_cents`) and the `make_instance` keys before Builder E starts (FC1 Q9 precedent).
10. **DAG defaults (section 4).** **RECOMMENDED:** keep the defaults (plain prose for D1-D10; no new prerequisites). Options for the
    architect, each a curriculum change: add E5 for `policy-rate` (no cycle); add E2 for moral hazard and adverse selection (no cycle);
    add FC2 for swaps (no cycle). Do not add SR1 (it requires BK1, `05-macro-alternatives.yaml:437`; adding it would be a cycle). Do not add
    PR4 (it pulls in PR1 and S4).
11. **Optional registry keys (section 7.1).** **RECOMMENDED:** cite only the five curriculum keys in v1. `frb2023fed` may be admitted for
    L06 or L03 only after the builder reads it; `diamond1983bank` and `bis2014basel` are not cited by BK1 by default.
12. **Two-sided treatment.** The claims about deposit franchise and deposit beta are contested. **RECOMMENDED:** the builder reads the abstracts
    of `drechsler2017deposits`, `drechsler2021banking` and `jiang2024monetary` before grading any sentence; any claim that cannot be supported
    by an abstract's own finding is graded C with its basis, or removed. The planner read none of the abstracts.
13. **Adversarial project.** **RECOMMENDED:** not adversarial; no question bank (architect default).
14. **Pyodide package list.** **RECOMMENDED:** `data-packages=""`, standard library only. Confirm that the page-smoke runner accepts an empty list
    (section 11, item 3). If not, the grader and labs remain standard-library only and the runner's list is the only change.
15. **Problem-set size.** BUILDER_RULES §4.2 item 7 requires twelve problems per lesson, seventy-two in all, each with a full worked solution.
    **RECOMMENDED:** keep the rule as written and let the builder schedule it; the planner does not reduce it.
16. **Rubric weighting.** The curriculum gives no weights for the autograder and the memo (`yaml:1012`). **RECOMMENDED:** no numeric weights;
    both parts must pass, with the rubric levels shown.
17. **Rung 2 convention.** **RECOMMENDED:** the completion lab with `___` blanks and a completed twin (architect ruling 11).
18. **Notation.** **RECOMMENDED:** no NOTATION_REQUESTS; the local symbols of section 2.3, none registered.
19. **Freshness.** **RECOMMENDED:** the verifier flags 2025-2026 work on deposit beta and deposit franchise in `freshness_flags`
    (VERIFIER §3); no debate brief is required.

---

## 13. After the builders

1. Orchestrator integrates; runs the section 10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
   Builder A's hub is written after L01-L02 exist; Builder F's cards come last.
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02; L03-L04 (includes the curriculum lab and the `ust_daily` licence
   check); L05-L06 (includes the Basel-parameter check: no number may appear that is not from a read source); the project (ten mutants,
   five alternatives, the rubric calibration by a separate blind scorer per architect rulings 15 and 23). Failing rows return to the owning
   builder with only the failing rows.
3. Ledger at `ledgers/BK1.verification.json`; verifier scripts under `ledgers/BK1/scripts/`; mutants under `ledgers/BK1/mutants/`;
   alternatives under `ledgers/BK1/alternatives/`; any equivalent mutant with its proof under `ledgers/BK1/equivalent/` (VERIFIER §3; architect
   rulings 9 and 30).
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1-B4 must be resolved or named as
   honest gaps first. Nothing is merged incomplete (an unfinished unit breaks `check_pages.py --all`).

Architect decisions: pending (section 12). This plan is the planner's proposal.
