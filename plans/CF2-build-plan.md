# CF2 build plan: Cost of Capital & Capital Structure (2026-11-09)

Unit: **CF2 · Cost of Capital & Capital Structure** · tier U · 80 h · prerequisites **CF1, AP2** (`curriculum/02-economics-finance-core.yaml:703`) · no debate key · no Atlas milestone · grading **both** (`yaml:732`) · output directory `course/modules/CF/CF2/` (part code `CF`) · lab twins `tests/labs/CF2/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits, no edits outside this file. Executors: Haiku builders, then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger. Structure follows `plans/E5-build-plan.md` sections 0-13. Nearest built prerequisite plan read: `plans/CF1-build-plan.md` (whole) and its architect decisions (lines 248-249).

Evidence convention: every curriculum statement cites `file:line` read during planning. A tool fact was checked by reading the tool source or by running `tools/coursekit.py` through `.venv/bin/python -I` (`prerequisite_closure`, `concept_owner`, `unit`). Anything not in the curriculum or the registry is marked **NOT IN CURRICULUM** or **NOT ESTABLISHED**. The planner did not read any paper listed in section 7; every attribution there is a lead for a builder who must read the abstract first.

**Status: BLOCKING ISSUES EXIST (section 0.3).** The hours are feasible. Three decisions are needed before the builders start: the project's data (B1), whether E2 becomes a prerequisite so the pecking-order lesson can name adverse selection (B2), and the Modigliani-Miller source gap (B3, which can be accepted as a named honest gap).

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| CF2 id and title | `curriculum/02-economics-finance-core.yaml:699-700`; `curriculum/curriculum.json:8105-8106` (object opens 8105, `"id": "CF2"` at 8106) |
| Tier `U`, hours `80` | `yaml:701-702` |
| Prereqs `[CF1, AP2]` | `yaml:703` |
| Core: "WACC and its estimation error, Modigliani–Miller, tax shields, trade-off vs. pecking order, market timing, leverage dynamics." | `yaml:704-706` |
| `introduces` has **10** concepts: wacc, wacc-estimation-error, modigliani-miller-propositions, interest-tax-shield, levered-unlevered-beta, financial-distress-costs, trade-off-theory, pecking-order-theory, market-timing-capital-structure, leverage-dynamics | `yaml:707-717` (one per line 708-717); the JSON row (`curriculum.json:8106` onward) matches |
| Sources, six free-text strings: Modigliani & Miller (1958); Modigliani & Miller (1963); Myers (1984); Myers & Majluf (1984); Fama & French (2002); Baker & Wurgler (2002) | `yaml:718-724` |
| Lab: "MM with taxes and distress costs: the optimal-leverage curve." | `yaml:725` |
| Project "Cost-of-capital estimation under uncertainty"; brief: "Estimate one firm's WACC with full error propagation (beta, ERP, spreads), and show the valuation range the error implies."; deliverable "Estimation code plus memo."; grading `both` | `yaml:726-732` (title 727, brief 728-730, deliverable 731, grading 732) |
| No `debate:` key and no `atlas:` key on CF2 | `yaml:699-732` (absent) |
| No Atlas milestone names CF2 (0 of the `atlas` entries mention CF2) | `curriculum.json` `atlas` array (planner check) |
| CF2 is required by the bachelor's credential, the Corporate Finance I course map, the PhD first-year "Corporate Finance Theory" group, and the "Corporate Issuers" topic | `curriculum/meta.yaml:62` (BS-FIN requires), `:76` (course map, with CF1), `:130` (PHD-FIN first-year sequence, with CF3, CF5, E2, E4), `:157` (topic) |
| E2 is grouped with CF3 in "Corporate Finance II: Payout & Governance" | `curriculum/meta.yaml:77` |
| Modules that require CF2: CF3 `[CF2, E2]`, CF4 `[CF2, AC2]`, CF9 `[CF2, FC2]`, CR1 `[CF2, SC3]` | `yaml:737`, `yaml:772`, `yaml:930`; `curriculum/03-markets.yaml:883` |
| Prerequisite closure of CF2 (computed): **AC1, AP2, CF1, CS1, E1, E3, M1, M2, M3, M4, M7, P0.1, S0, S1** (14 units); **184** usable concepts (sum of the closure's `introduces`) | `tools/coursekit.py` `prerequisite_closure("CF2")` and `unit(...)`, run by the planner |
| Closure of the candidates B2 and B4: E2 closure `{E1, M1, M2, M4, P0.1}`; S2 closure `{CS1, M1, M2, M3, M4, P0.1, S0, S1}`; FI1 closure `{AC1, CF1, M1, M2, P0.1}`. None contains CF2, so adding any of them creates no cycle | `coursekit.prerequisite_closure` (planner run) |
| Topological order: CF1 index 11, AP2 index 34, CF2 index 44 | `curriculum/curriculum.json` `topological_order` |
| Build state: CF1 built (`course/modules/CF/CF1/` with `grader/`); **AP2 not built** (`course/modules/AP/` holds only AP1); E2 built; S2, FI1, CF3, CF4 not built | `ls course/modules/...` (planner run) |
| Concept anchors exist in `course/concepts.html` for AP2 concepts `capm`, `beta`, `equity-risk-premium`, `security-market-line`, and for `covariance-matrix`, `delta-method`, `growing-perpetuity`, `adverse-selection`, `signaling`, `ols-estimator` (one `id` each) | `grep -c 'id="<id>"' course/concepts.html` (planner run) |
| CF1 is the built prerequisite: its prereqs are `[M1, AC1]`; its ten concepts include `depreciation-tax-shield`, `monte-carlo-npv`, `fisher-relation` (usable in CF2) | `yaml:673` (prereqs of the CF1 block, which opens at `yaml:669`); `plans/CF1-build-plan.md:1-13` (CF1 plan, closure and architect decision Q1, line 249) |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 80 h (`yaml:702`). Tool rules (`tools/check_pages.py`):

- lesson `data-hours` 6-12 (check_lesson, `check_pages.py:219-227`);
- hub `data-hours-lessons + data-hours-project = 80` (`check_hub`, `check_pages.py:325-340`);
- project share 10-40% of 80, i.e. 8 to 32 h (`check_pages.py:339-340`);
- lessons sum to the hub's lessons figure.

Chosen split: **9 lessons × 7 h = 63 h; project 17 h (21.25%)**. 63 + 17 = 80. Feasible. The split is set in section 1; the alternative 8 × 8 h + 16 h is recorded as Q1. No STOP condition on hours.

### 0.3 Blocking issues and source gaps

**B1. The project's beta, equity-premium and spread inputs have no embedded source.** The only embedded snapshots are `fx_daily`, `fx_monthly` and `ust_daily` (`tools/data_sources.yaml` dataset ids at lines 19 and 91; `course/assets/data/market/MANIFEST.json` lists three datasets). The project needs firm and market return series (beta), an equity risk premium, and a credit spread. None is in `tools/data_sources.yaml`, and none appears in `rejected:` (`data_sources.yaml:119-`), which lists only the French library and Open Source Asset Pricing. BLUEPRINT §5.3 names no equity-return or spread source as cleared. BUILDER_RULES §6.6 forbids embedding until the issuer's redistribution grant is quoted from the issuer's page. The planner did not read any issuer page and names none from memory.
- **Plan's default:** (a) the risk-free rate is the embedded `ust_daily` series `cmt_10y` (real, redistributable; section 6); (b) returns, ERP and spreads come in **bring-your-own-data** mode (documented CSV schema, validated in the browser, never leaves the browser; BUILDER_RULES §6.6); (c) labs and the autograder use SIMULATED data (BUILDER_RULES §1.7). The architect decides whether a verified redistributable return or spread source is added first.

**B2. The pecking-order lesson needs adverse selection and signalling, which sit outside the closure.** `pecking-order-theory` (yaml:715) is defined on information asymmetry. The concepts that name it, `adverse-selection` and `signaling` (and `screening`, `moral-hazard`), are owned by **E2** (`yaml` E2 `introduces`, read through `coursekit.unit("E2").introduces`). E2 is built and not in the closure. E2 is already in the course of CF3 (`meta.yaml:77`) and in the PhD group with CF2 (`meta.yaml:130`). Adding E2 to CF2's `prereqs` creates no cycle (E2's closure has no CF2 or CF1 or AP2).
- **Plan's default:** plain prose, no link, no `<dfn>` for E2 concepts; the pecking-order lesson describes asymmetric information in words (section 4, D1). **Recommended:** add E2 to CF2's prerequisites (a curriculum change; Q2).

**B3. Modigliani and Miller (1958) and (1963) cannot be admitted by any route the program allows.** Both are curriculum sources (`yaml:719-720`) with no registry key. The review queue carries them as "no candidate established identity" (`references/review_queue.json:545` for 1958; `:598` for 1963; `references/SEED_REPORT.md:38-39`). The candidate DOIs in the queue are different articles (titles such as "Forecasting Uses of Anticipatory Data on Investment and Sales", `review_queue.json:557`), so they must not be admitted. The research run of 2026-10-27 found no record: "AER 1958 has no DOI in Crossref or OpenAlex; the only allowed route would be AEA, which is behind a bot check" (`plans/reference-queue-research-2026-10-27.md:33-34`). `references/authorities.yaml:37` does list `aeaweb.org`, so a human could admit a stable AEA page; that is the architect's action, not the builders'.
- **Plan's default:** CF2 cites **no** M&M key. The Modigliani-Miller propositions are derived on the page (grade T, numbered assumptions). Any sentence that attributes a result to M&M is a naming sentence with no claim and no grade (the pattern of FINAL-ARCHITECT-RULINGS ruling 39). The gap is named in KNOWN-ISSUES. **Recommended:** accept as a named honest gap (Q6).

Non-blocking, but the architect should see them:

- **N1. AP2 is unbuilt.** CF2 links AP2 concepts through `concepts.html` anchors, which exist (section 0.1). The hub may not link an AP2 page, because none exists. Same precedent as E5 §11 item 6.
- **N2. The Federal Reserve is retiring the download route.** `tools/data_sources.yaml:8-10` says the Board plans to remove its "Build Your Package" option the week of 2026-11-09, which is today. The snapshot is pinned by SHA-256 and `fetch_data.py --check` is offline, so the gate is unaffected. A `--fetch` refresh or the weekly CI job may fail. The owner should know this.
- **N3. Brealey is not cited.** CF1 architect decision Q3 (`plans/CF1-build-plan.md:249`): do not cite `brealey2022principles`, because its record conflicts with the curriculum string. The same rule applies to CF2.
- **N4. "About three lessons per builder."** With five builders A-E (E owns the project), four lesson builders can take three, two, two and two lessons for nine lessons. Section 1 does this.
- **N5. Meta observation, not a defect.** CF2 (tier U) sits in the PhD first-year group "Corporate Finance Theory" (`meta.yaml:130`). The same pattern as E5 §11 item 10. The plan takes no action.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

9 lessons × 7 h = 63 h; project 17 h; total 80 h. The ten concepts (`yaml:708-717`) each appear in exactly one row.

| Lesson | Title (working) | Concepts it defines (`yaml:708-717`) | Lab (twin id, `tests/labs/CF2/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | The cost of capital: the WACC identity | `wacc` | `lab-CF2-L01-1`: exact WACC of a stated capital structure in `fractions.Fraction`; weights sum to one; WACC equals the weighted average of the two costs (planner proposal) | 7 | Builder A |
| L02 | Beta: estimation, unlevering and relevering | `levered-unlevered-beta` | `lab-CF2-L02-1`: SIMULATED returns; beta as sample covariance over sample variance; exact unlever-relever round trip (planner proposal) | 7 | Builder A |
| L03 | Error in the cost of capital | `wacc-estimation-error` | `lab-CF2-L03-1`: SIMULATED; delta-method variance of WACC against a seeded Monte Carlo; the gap equals the omitted second-order term (planner proposal) | 7 | Builder A |
| L04 | Modigliani-Miller without taxes | `modigliani-miller-propositions` | `lab-CF2-L04-1`: exact Proposition I (value independent of leverage) and Proposition II (cost of equity slope) on a D/E grid (planner proposal) | 7 | Builder B |
| L05 | The interest tax shield and MM with corporate tax | `interest-tax-shield` | `lab-CF2-L05-1`: exact PV of the shield for permanent debt equals tax rate × debt; WACC path with and without the shield (planner proposal) | 7 | Builder B |
| L06 | Financial distress and the trade-off theory | `financial-distress-costs`, `trade-off-theory` | **`lab-CF2-L06-1` = the curriculum lab (`yaml:725`)**: optimal-leverage curve in a stated model; the optimum by a finite grid (grade C, basis named) | 7 | Builder C |
| L07 | The pecking order | `pecking-order-theory` | `lab-CF2-L07-1`: exact funding waterfall (internal cash, debt, equity) under a stated issue-cost ranking; the ranking is an assumption, the ordering a derivation (planner proposal) | 7 | Builder C |
| L08 | Market timing in capital structure | `market-timing-capital-structure` | `lab-CF2-L08-1`: SIMULATED, seeded; issuance rule keyed to market-to-book; resulting leverage path (planner proposal) | 7 | Builder D |
| L09 | Leverage dynamics and target adjustment | `leverage-dynamics` | `lab-CF2-L09-1`: exact partial-adjustment path toward a target, geometric convergence, half-life (planner proposal) | 7 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 63/17 | none | none | - | Builder A |
| project | Cost-of-capital estimation under uncertainty (`both`, section 5) | none | `lab-CF2-project-1` (rung 1), `lab-CF2-project-2` (rung 2, `class="lab completion"`), `lab-CF2-project-3` (rung 3 check) | 17 | Builder E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` (section 5.5) | none | none | - | Builder E |
| cards | `cards.json` from L01-L09 | none | none | - | Builder F (after A-E) |

Ownership rule: each builder writes only its own lesson files and twins. Builder A writes the hub after L01-L03 exist. Builder E writes the project, grader, rubric and exemplars, and does not depend on lesson text beyond the concept names in section 1.

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses only, section 4):
- L01 uses CF1/M1 `present-value`, `annuity` (cost of debt as a discount rate, plain prose) and AP2 `capm`, `security-market-line`, `equity-risk-premium` (links to `concepts.html`).
- L02 uses L01 (`wacc`, link `L01.html#def-wacc`), AP2 `beta` (`concepts.html`), M4 `covariance-matrix`, `variance`, S1 `estimator`, `consistent-estimator`.
- L03 uses L01, L02 (`levered-unlevered-beta`), S1 `delta-method`, `confidence-interval`, `bootstrap`; M4 `covariance-matrix`.
- L04 uses L01, L02; M1 `present-value`, `growing-perpetuity`. No E2, S2 or FI1 concept.
- L05 uses L04 (`modigliani-miller-propositions`); CF1 `depreciation-tax-shield` only as a contrast (link allowed, CF1 is a prerequisite).
- L06 uses L05 (`interest-tax-shield`) and L04.
- L07 uses L06 (`trade-off-theory`) for contrast; E2 concepts only if Q2 is approved, otherwise plain prose.
- L08 uses L07 (`pecking-order-theory`) and L01 (`wacc`) for the discount rate.
- L09 uses L06 (`trade-off-theory`) for the target and M1 `geometric-series`.
- Project uses every lesson's concept (links `L0n.html#def-<id>`) and M1 `growing-perpetuity`, `present-value`; S1 `delta-method` for the error step.

Hours check: 9 × 7 = 63 (hub `data-hours-lessons="63"`); project 17 (`data-hours-project="17"`); total 80.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to CF2)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `plans/E5-build-plan.md` (its section 2 precedent), `plans/CF1-build-plan.md` (its architect decisions, lines 248-249), `plans/FINAL-ARCHITECT-RULINGS.md`, `/Users/billyribeiro/.fanout/fixer-rules.md`, this file. Study `course/modules/CF/CF1/` for the layout, the hub, the project and the grader (CF1 is built). Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`, or exact decimal reading of the inputs) and rounded only at display. A page that shows a rounded figure states its rounding rule (fixer-rules line 6). Every WACC, beta, standard error and valuation carries its rounding rule.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only what the printed numbers show. Precedent: M1 LESSON_TEXT_DEFECTS; fixer-rules line 7 (labs call `main()` at top level; re-embed after any twin change).
3. **Attribute nothing unread.** Only registry keys in section 7 may be cited. Each citation names a claim the builder has read in the abstract (VERIFIER §2.1). Where the abstract was not read, the sentence is an ungraded naming sentence ("this page has not read the paper and cites it for no result"). No page, table, coefficient, year or DOI is typed from memory. A grade-C span needs a registry key or an explicit page-level basis (fixer-rules line 8).
4. **Scope words need a computation, a witness or an explicit hypothesis, or are removed** (fixer-rules line 9). Banned unless computed: every, all, always, never, any, same, only, exactly, "in practice", "firms use", "the market". CF2 scope (confirm, Q11): a single firm; closed-form static models for MM and the tax shield; a constant-leverage WACC; a trade-off optimum computed on a stated grid; no option model, no structural credit model, no dividends (CF3), no valuation of FCFF beyond a growing perpetuity (CF4).
5. **Define before use.** Each of the ten concepts is defined once with `<dfn id="def-<id>" data-concept="<id>">` in its assigned lesson, and never before it. Terms outside the ten (weighted average, equity beta, debt beta, market-to-book, book leverage, credit spread, the valuation range, half-life, target leverage) are defined in prose at first use with a plain `<dfn>` and no `data-concept` (`tools/check_dag.py` skips a `<dfn>` without `data-concept`).
6. **Assumptions are numbered.** Every Theorem, Proposition and Derivation lists its numbered Assumptions (A1, A2, ...) before the statement, and each result that uses an assumed fact says "Assuming A_k" (fixer-rules line 12). Assumptions the builders must state: perfect capital markets (MM); no corporate taxes (MM without taxes); riskless debt; cash flows independent of financing; interest fully deductible at the corporate rate τ_c in (0,1) (taxes); permanent debt at a constant level (shield and WACC formula); debt beta zero in unlevering; constant leverage ratio D/V in the WACC formula; weights at market values; no distress costs unless the lesson adds them (trade-off); a stated issue-cost ranking (pecking order); a stated market-to-book rule (timing); a constant target and a constant adjustment speed λ in (0,1] (dynamics).
7. **Grader rule.** Applies to the project grader (section 5.5), not to the lessons.
8. **Money is integer cents** (fixer-rules line 14). Any money amount shown or returned (cash flows, debt, equity, valuation range) is an integer number of cents. Rounding is round-half-up on the exact value and is stated on the page. Rates are decimals, never rounded inside the engine.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own container; `<wbr>` or `min-inline-size:0` where a long symbol would overflow (fixer-rules line 14). Escape `$` as `\$` inside math.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` and has no `if __name__ == "__main__":` guard. `run_labs.py` runs each twin under `python -I -W error` with no network (`tools/run_labs.py` lines 51-60; M1 twin `tests/labs/M1/lab-M1-L04-1.py` is the model).
11. **Yield and rate statements are basis-explicit.** Every rate is stated with its unit (decimal per year, or percent per year as published) and its basis. For `cmt_10y` the builder states "as published by H.15, percent per year, not converted"; the compounding convention is not claimed unless the builder reads the H.15 page and quotes it (Q8).
12. **Lesson hours.** `<html data-hours="7">` on each lesson; the sum is 63 (section 1).
13. **Target-leverage and expectation notation.** Any "expected" quantity is written with a local symbol or with the registered macro `\E` (section 2.3), never with a bare `E`.
14. **Carry-over from fixer-rules.** Process words absent from learner text (build, builder, round, verifier, REQUESTS, unit report); no planning references in code comments (E5 precedent). No `window.confirm`, CDN, remote font or iframe. No figures and no new JS kernels (Q10).

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. A grade-B or grade-C claim names its published counter-evidence where one exists (BUILDER_RULES §2.5). Until the counter-evidence key is admitted, the claim is graded C with its design named, or it is removed.
- Concepts: section 1 table only; `<dfn>` for the ten concepts with `data-concept`, plus plain `<dfn>` for other terms.
- Prerequisite links: `href="../../../concepts.html#<id>"` for CF1, AP2, M1, M4, S1 concepts; `href="Lnn.html#def-<id>"` for earlier CF2 lessons. A lesson never links a concept defined in a later lesson. No link to an AP2, E2 or CF1 hub page, because those pages are either unbuilt or not part of CF2's link set.
- Labs: code lives once in `tests/labs/CF2/lab-CF2-Lnn-1.py` (and `lab-CF2-project-1..3.py`). The page carries `@@LAB:<file>@@` and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-CF2-<page>-<n>` (`check_pages.py` `check_lesson`). Standard library only (`fractions`, `math`, `random.Random(seed)`); seeded RNG only; no network; under 10 s in Pyodide; no warnings under `-W error`.
- SIMULATED label: on every lab, figure or grader instance that uses generated data (L02, L03, L08, project worked example and completion problem, exemplars). Exact closed-form labs (L01, L04, L05, L06 model, L07, L09) are labelled "model" and are not labelled SIMULATED.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`, `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Banned strings (`tools/check_pages.py` lines 58-72, `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known", "obviously", "clearly", and any ellipsis `...` outside code.
- Percent changes state the base and direction. Growth rates state the convention (log or simple, per year or per period).
- A finite enumeration (the L06 grid, the L08 simulation) is grade C with its basis named, not grade T (precedent: M1 L06).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration (precedent: CF1 KNOWN 3).
- Quiz explanations are read against their lesson (precedent: CF1 KNOWN 6).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10 output contract.

### 2.3 Notation (binding; `notation/notation.json`)

| Registered symbol or macro | Registered meaning (locator) | CF2 conflict and rule |
|---|---|---|
| `T` | number of return observations in a sample (`notation/notation.json` symbols array from line 110; entry S1) | **Conflict risk.** Beta and standard-error samples use `N`; a horizon uses `H`; never bare `T` for sample length or for a time index in CF2. |
| `R_f` | gross riskless return (AP1) | **Do not use.** The net risk-free rate is written `r_f`, and the lesson states once that `R_f` is the registered gross symbol and is not used. |
| `R^\ast`, `R^{e\ast}`, `\mathbb{Q}` | AP1 registered symbols | Not used. |
| `\Phi`, `\Phi^{-1}` (M4); `\gamma_3`, `\gamma_4` (M4) | standard normal CDF; skewness, kurtosis | Not used. Plain `\gamma` stays free. |
| `\E` (macro, `\mathbb{E}`) | expectation operator | Used for expectation. The equity value is **not** written `E` in expectation context; see the local-symbol row. |
| `\Var`, `\Cov`, `\Corr` (macros) | variance, covariance, correlation | Use these macros for the delta-method formulas. |
| `\se` (macro) | standard error | Use for every standard error in L03 and the project. |
| `\R` (macro) | real numbers | Standard. |

Local symbols (allowed; each defined on the lesson where it first appears and never redefined): `D` debt at market value; `E` equity at market value (roman, in capital and value context, never inside `\E`); `V = D + E`; `\tau_c` corporate tax rate in (0,1) (not `\tau` used elsewhere in the program); `r_E` cost of equity; `r_D` pre-tax cost of debt; `r_f` net risk-free rate; `\beta_L`, `\beta_U` levered and unlevered equity beta; `\beta_D` debt beta (zero by Assumption); `\mathrm{ERP}` equity risk premium; `s` credit spread; `r_{\mathrm{WACC}}`; `g` growth; `\lambda` adjustment speed; `\bar{D}/\bar{V}` target leverage (defined in L09).

NOTATION_REQUESTS: none expected. If a builder needs a symbol with a registered meaning, the builder renames it locally rather than request a change (E3 ruling 29 pattern, fixer-rules line 15).

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

Each lesson follows the §4.2 structure of BUILDER_RULES: why it matters (120 words max); core content in numbered sections (Definition, Theorem, Proof, Example, Remark); inline lab; where the canon breaks; misconceptions (3 or more); problem set (3 or more in each of the Mechanics, Proof, Empirical and Research tiers, each with a full worked solution in `<details class="solution">`); key-results table; quiz (8-15 items with explanations). **No debate brief** is required (no `debate` key, `yaml:699-732`). The two-sided rule still applies to the contested empirical claims in L06-L08.

Registry keys by lesson (section 7 holds the full list): L01-L05 cite none for definitions. L06 may cite `leland1994corporate` (optional, paper level). L06, L07 and L08 cite `fama2002testing`, `myers1984corporate`, `myers1984capital`, `baker2002market` only after their abstracts are read and only with the counter-evidence rule.

- **L01 · `wacc`.** Cost of equity by CAPM (AP2 concepts `capm`, `security-market-line`, `equity-risk-premium`: links to `concepts.html`); cost of debt as the discount rate that equates the debt's promised cash flows to its market value (M1 `present-value`, `annuity`; plain prose, no FI1 link, D4); the WACC identity `r_WACC = (E/V) r_E + (D/V) r_D (1 - tau_c)`. Derivation T conditional on A1 (weights at market values), A2 (constant D/V), A3 (no other claims). Canon breaks: constant leverage (examined in L05). Misconception: WACC is the cost of debt plus cost of equity.
- **L02 · `levered-unlevered-beta`.** Beta as `Cov(r_i, r_m)/Var(r_m)`, with the n−1 normalisation on both terms so it cancels (T); the sample analogue as an estimator (S1 `estimator`, `consistent-estimator`). Unlevering and relevering under A7 (debt beta zero) and permanent debt: `beta_U = beta_L / (1 + (1 - tau_c) D/E)` and its inverse, derived in the lesson (the derivation is the builder's; the planner states the target formula for the grader, section 5.5, and the architect rules if the derivation differs). Lab `lab-CF2-L02-1`, SIMULATED. Canon breaks: a stable beta, the debt-beta assumption. Misconception: beta of a levered firm is the asset risk.
- **L03 · `wacc-estimation-error`.** Propagation of the estimation error of beta, ERP and spread into WACC by the delta method (S1 `delta-method`); the variance formula with weights and tax treated as known (A8); the covariance term between beta and ERP; **the omitted second-order term** (the product of beta and ERP) stated and shown exact: for jointly normal inputs the exact variance of WACC exceeds the linearised one by `w_E^2 (Var(beta) Var(ERP) + Cov(beta, ERP)^2)`, where `w_E = E/V`; the bootstrap as an alternative (S1 `bootstrap`, `confidence-interval`, no key needed). Lab `lab-CF2-L03-1`, SIMULATED: delta-method variance against 20,000 seeded Monte Carlo draws; the gap printed and matched to the second-order formula. Grade of the Monte Carlo output: C (SIMULATED, named lab). Canon breaks: linearisation, normality of the estimates, fixed weights. Misconception: a 95% range is WACC ± 2 standard errors without an assumption of normality.
- **L04 · `modigliani-miller-propositions`.** Without taxes and under A1 (perfect capital markets), A4 (no distress costs), A5 (cash flows independent of financing): Proposition I (firm value independent of leverage) by arbitrage and by the WACC identity; Proposition II (cost of equity linear in D/E with slope r_A - r_D, where r_A is the unlevered cost of capital) by substitution (T). The M&M attribution is a naming sentence only (B3, section 7). Lab `lab-CF2-L04-1`, exact `Fraction`. Canon breaks: perfect markets, no taxes. Misconception: leverage raises the cost of equity so value is unchanged (a correct conclusion with the proof, not with the sentence).
- **L05 · `interest-tax-shield`.** Under A6 (permanent debt at constant D), A8, and A9 (interest fully deductible at tau_c): the tax shield per period `tau_c r_D D`; its PV at r_D equals `tau_c D` (T); value `V_L = V_U + tau_c D` (T conditional on A6-A9); the WACC path with leverage (exact). Remark: the 1963 correction in the curriculum source list is not cited (B3). Canon breaks: permanent debt, the tax shield's discount rate, personal taxes omitted. Misconception: the shield is the full interest paid. Contrast with CF1 `depreciation-tax-shield`. Lab `lab-CF2-L05-1`, exact.
- **L06 · `financial-distress-costs`, `trade-off-theory`. Carries the curriculum lab.** Distress costs as a stated function of leverage (direct and indirect; the functional form is a model choice, stated); the trade-off optimum as the maximum of `V_U + tau_c D - PV(distress)` over a stated grid of D (grade C: enumeration, basis named). Lab `lab-CF2-L06-1` = the curriculum lab, "MM with taxes and distress costs: the optimal-leverage curve": prints the curve and the grid optimum; checks the optimum is interior for the stated parameters and states the grid step. Empirical: `fama2002testing` (grade B for "tests of trade-off and pecking-order predictions", counter-evidence required, section 7); `leland1994corporate` optional, paper level, its model not reproduced. Canon breaks: the distress-cost function, the grid. Misconception: optimal leverage is where the tax shield equals the distress cost at the margin (true only in the stated model; the lab shows the condition).
- **L07 · `pecking-order-theory`.** Financing hierarchy: internal funds, then debt, then equity, under asymmetric information (adverse selection; E2 concepts only if Q2 is approved, otherwise plain prose, D1). `myers1984corporate` (paper level after abstract) and `myers1984capital` (paper level after abstract) cited for the framing; `fama2002testing` (grade B, counter-evidence required) for the tests. Lab `lab-CF2-L07-1`: an exact funding waterfall under a stated issue-cost ranking; the ordering is derived from the ranking (T conditional on the ranking, an assumption A10). Canon breaks: the ranking is an assumption; the empirical evidence is mixed by design of the tests in `fama2002testing`'s own framing (read the abstract first). Misconception: pecking order implies no target leverage.
- **L08 · `market-timing-capital-structure`.** Equity issuance when market-to-book is high; the persistence of leverage differences from past issuance timing; `baker2002market` (grade B, counter-evidence required; abstract read first). Lab `lab-CF2-L08-1`, SIMULATED, seeded: a mechanical issuance rule against a SIMULATED market-to-book path; the leverage path it produces. Interpretation limited to the rule's mechanics, not to firms. Canon breaks: the market-to-book measure, mispricing vs. risk. Misconception: market timing shows that managers beat the market.
- **L09 · `leverage-dynamics`.** Target adjustment: `D_{t+1} - D_t = lambda (D*_t - D_t)` with lambda in (0,1] (A11, constant target and speed); the closed-form geometric convergence `D_t - D* = (1 - lambda)^t (D_0 - D*)` (T); the half-life `ln(1/2)/ln(1 - lambda)` (derivation T); the link to the trade-off target from L06. Lab `lab-CF2-L09-1`, exact. Empirical adjustment speeds: not claimed (topic-level counter-evidence request R6). Canon breaks: constant target, constant speed. Misconception: a low speed means the firm does not target leverage. Note the name collision risk with CF3 `lintner-partial-adjustment` (section 4, D6): CF2 uses its own equation and name.

Lesson-level constraints: each lesson's "Where the canon breaks" names at least one model limit and what changes without it. No lesson uses an E4, E6 or CF3-to-CF9 concept.

---

## 4. DAG problems (concepts that natural CF2 content would use outside the closure)

Prerequisite closure of CF2 (computed): **{AC1, AP2, CF1, CS1, E1, E3, M1, M2, M3, M4, M7, P0.1, S0, S1}**, with **184 usable concepts**. Owners from `curriculum/curriculum.json` `concepts` and each unit's `introduces` (planner check). "Later" means the module requires CF2 (cannot be used without a cycle).

| Ref | Concept(s) | Owner | In closure? | Natural CF2 use | Resolution (default) | Recommendation |
|---|---|---|---|---|---|---|
| D1 | `adverse-selection`, `signaling`, `screening`, `moral-hazard` | E2 (built; closure `{E1, M1, M2, M4, P0.1}`, no cycle) | no | pecking order, L07 | plain prose, no link, no dfn | **add E2 as a CF2 prerequisite (Q2)** |
| D2 | `ols-estimator`, `errors-in-variables`, `omitted-variable-bias` | S2 (not built; closure `{CS1, M1-M4, P0.1, S0, S1}`, no cycle) | no | beta as a regression slope; attenuation bias | beta defined as `Cov/Var` (M4 `covariance-matrix`, `variance`, both in closure); sample analogue (S1 `estimator`); attenuation in plain prose, not as a concept | no add (Q3) |
| D3 | `yield-to-maturity`, `bond-price-yield`, `spot-rate`, `yield-conventions` | FI1 (not built; closure `{AC1, CF1, M1, M2, P0.1}`, no cycle) | no | cost of debt | cost of debt as the rate that prices the debt's promised cash flows (M1 `present-value`, `annuity`), plain prose | no add (Q4) |
| D4 | `free-cash-flow-to-firm`, `fcff-dcf-valuation`, `valuation-error-sources`, `enterprise-to-equity-bridge`, `real-option` | CF4 (**later**: requires CF2) | no; cycle | valuation range | the cash flow is a stated first-period amount; value is a growing perpetuity (M1 `growing-perpetuity`); no CF4 term | none (cycle) |
| D5 | `gordon-growth-model`, `dividend-discount-model`, `free-cash-flow-to-equity` | FC4 (requires AP2, AC2, CF1; closure not computed) | no | the perpetuity formula | `growing-perpetuity` (M1); the term "Gordon growth model" not used | no add |
| D6 | `agency-costs`, `lintner-partial-adjustment`, `free-cash-flow-agency`, `dividend-signaling`, `payout-irrelevance` | CF3 (**later**: requires CF2) | no; cycle | agency in the trade-off; target adjustment | plain prose; L09 uses its own equation and name | none (cycle). Name-collision note in section 11 |
| D7 | `merton-structural-model`, `distance-to-default`, `credit-spread-puzzle`, `default-prediction`, `gz-credit-spread` | CR1 (**later**: requires CF2), CR3, CR4 | no; cycle | credit spread and distress | distress described in words; spread is a BYOD input (section 5) | none (cycle) |
| D8 | `chapter-11-bankruptcy` | CF5 (**later**) | no; cycle | distress outcomes | not used | none (cycle) |
| D9 | `black-scholes-formula`, `option-greeks`, `risk-neutral-probability`, `real-option` | FC2 / DV1 / CF4 | no | equity as a call option (Merton view) | not used; out of CF2 scope (Q11) | none |
| D10 | `ridge-regression`, `covariance-shrinkage`, `bayesian-replication-shrinkage` | QR3 / PR1 / F5 | no | shrinkage of beta | not used; the stretch uses `bootstrap` (S1, in closure) | none |
| D11 | `monte-carlo-integration` | M8 | no | Monte Carlo of WACC | not used; the simulation uses `random.Random(seed)` and CF1 `monte-carlo-npv` (in closure) for the NPV-distribution analogy only | none |
| D12 | `term-spread`, `duration`, `term-structure` (FI1) | FI1 | no | spread of debt over the risk-free term | not used | none |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Rows D1 (Q2), D2 (Q3), D3 (Q4) need the architect's confirmation.** `check_dag.py` checks linked uses only (tool docstring, `tools/check_dag.py` lines 1-20). An unlinked use of D1-D12 passes the tool, so the verifier reads every lesson for these names (VERIFIER §2.9).

---

## 5. Project (`project.html`, Builder E): `both`, ladder, spec, time budget, rubric, grader

### 5.1 Ladder (BLUEPRINT §5.1; `check_projects.py` requires the order, `tools/check_projects.py:33`)

1. **Rung 1, worked example** (`lab-CF2-project-1`, SIMULATED): one fully solved, annotated estimate for a SIMULATED firm: beta, unlevered beta, WACC, and the delta-method standard error of WACC. Each step carries a "why" note. Full length (tier U; BLUEPRINT §4 minimum applies from tier M).
2. **Rung 2, completion** (`lab-CF2-project-2`, `class="lab completion"`, SIMULATED): the relevering line and the WACC error line are removed (`___`). Graded instantly. Its twin is the completed solution; every page line equals the twin line or contains a blank (`tools/run_labs.py` docstring; architect ruling 11). `check_projects.py:89-90` requires a completion lab or a quiz (`section.lab.completion` or `section.quiz`).
3. **Rung 3, independent project** (graded by autograder and rubric): the engine (`wacc_engine.py`, section 5.5) and the memo (section 5.4). `lab-CF2-project-3` is the rung-3 check: it recomputes the default state of the memo's worked case from the same inputs, including the risk-free rate from `ust_daily` (section 6), and prints the table the memo must reproduce.
4. **Rung 4, stretch** (optional, not graded): a bootstrap estimate of beta's standard error (S1 `bootstrap`) compared with the delta-method value; or a second firm with the same rules. Open-ended, no ceiling, suitable for the portfolio.

### 5.2 Spec (`dl.spec`; `check_projects.py` requires the terms context, inputs, required outputs, constraints, grading, lines 34 and 38-49)

- **Context.** A corporate analyst must estimate one firm's cost of capital with its error and show the valuation range the error implies. The engine computes the estimates; the memo states the choices and the range.
- **Inputs.** Five inputs, each with a named source or the SIMULATED label, and a stated transform:
  1. risk-free rate: the 10-year constant-maturity yield `cmt_10y` from the embedded `ust_daily.csv`, the observation on or before the valuation date (real data; section 6);
  2. firm and market returns: bring-your-own-data CSV, columns `date, firm_return, market_return`, decimal per period, at least 36 periods;
  3. equity risk premium: bring-your-own-data, a single decimal per year with its source and date;
  4. credit spread: bring-your-own-data, a decimal per year over the risk-free rate, with its source and date;
  5. balance sheet and cash flow: market value of equity and of debt in integer cents, the tax rate `tau_c` in [0, 1), the next-period cash flow in integer cents, growth `g` as a decimal.
  The CSV schemas are documented on the page and validated in the browser; the files never leave the browser (BUILDER_RULES §6.6). Labs and the grader use SIMULATED data.
- **Required outputs.** `wacc_engine.py` with the functions in section 5.5 (names fixed by the architect, Q5); `memo.md` (one to two pages) with the WACC, its standard error, the valuation range in integer cents, and the stated assumptions; the rule for rounding in the memo.
- **Constraints.**
  - Money is integer cents; rates are decimals; every number in the memo cites its input, its date and its transform.
  - No Atlas component (section 8). The engine is standard library only (`data-packages=""`).
  - No claim about a series beyond its source's coverage (for example, the `ust_daily` sample ends 2026-09-30, `ust_daily` MANIFEST `last`).
  - Every SIMULATED or BYOD number is labelled as such.
- **Grading.** "Grading: both. The autograder runs the engine's test suite; the rubric grades the memo." The words "autograder" and "rubric" appear verbatim (`check_projects.py:38` requires `autograd` and `rubric` in the spec's grading entry).
- **Reading list** (`ol.reading-list`, registry keys only, section 7): `fama2002testing`, `baker2002market`, `myers1984corporate`, `myers1984capital`; `leland1994corporate` optional; `damodaran2012investment` optional (book level, no locator). No other key.

### 5.3 Time budget (`<table id="hours">`, sums to 17 h; every row needs a one-line rationale; `check_projects.py:107-118`)

| Component | Hours | Rationale |
|---|---|---|
| Read the spec, set up, run the starter against the suite | 1 | Confirms the interface and the failure messages before coding |
| Rung 1 and rung 2 labs (worked example, completion) | 1 | Reproduces the worked estimate and fills the blanks |
| Data intake: CSV schemas, validation, the `cmt_10y` lookup, the spread and ERP records | 3 | Four schemas documented and validated; one real series read with its date |
| Beta and unlevering: `beta_ols`, `unlever_beta`, `relever_beta`, and their tests | 2 | Covariance-over-variance, the n-1 normalisation, the round trip |
| WACC and cost of equity: `cost_of_equity`, `cost_of_debt`, `wacc` and their tests | 2 | CAPM, after-tax debt, market-value weights |
| Error propagation: `wacc_delta_variance` against the seeded Monte Carlo | 3 | Delta formula, covariance term, the second-order gap |
| Valuation range: `valuation_range`, rounding in cents, edge cases and error classes | 2 | Growing perpetuity, half-up rounding, the r > g boundary |
| Memo (rubric) | 2 | One page; every number cited with its date and transform |
| Self-assessment against exemplars | 1 | Score the memo with the rubric, then compare with exemplar-a and exemplar-b |
| **Total** | **17** | Equals `data-hours-project` on the hub |

### 5.4 Rubric (`table.rubric#rubric-memo`, `check_projects.py` `rubric_problems`, lines 58-72)

Five criteria. Each criterion is one table row: the name in a `th` and exactly four `td` cells for levels 4 down to 1 (the tool counts `td` cells). Every level descriptor is observable.

| Criterion | Level 4 | Level 3 | Level 2 | Level 1 |
|---|---|---|---|---|
| 1 Data and provenance | Names each of the five inputs with its source (or SIMULATED label), its date or valuation date, and its transform | Names every input with its source; one of date or transform missing | Names some inputs with sources | "uses the data" |
| 2 Beta and weights | States the unlevering assumptions (A7, permanent debt), the market-value weights and the D/E used, and applies `unlever_beta` to the stated values | States the formula and the values; one assumption missing | Applies a formula with no assumption stated | "adjusts the beta" |
| 3 WACC and its error | Reports WACC, its delta-method standard error, the covariance treatment of beta and ERP, and states the omitted second-order term | Reports WACC and its standard error; covariance treatment missing | Reports WACC only | "gives a range" |
| 4 Valuation range | States the cash flow in integer cents, growth `g`, the WACC band with multiplier k, both endpoint values in integer cents (half-up), and that r > g at both endpoints | States the range; k or rounding missing | States a range without its derivation | "a sensible range" |
| 5 Limits and evidence | Names the constant-leverage, permanence, debt-beta and linearisation limits used, and for each grade-B or C claim names the counter-evidence key or states the claim is graded C with its design named | Names the limits; one grade-B claim lacks its counter-evidence | Names one limit | "notes some caveats" |

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, full memos on a SIMULATED firm, annotated with the descriptors each passage meets or misses. Self-assessment form (`section.rubric-self`, `data-rubric="rubric-memo"`, `data-exemplars="exemplar-a exemplar-b"`, as in CF1). The page shows where the student's scores diverge from the exemplar scores. Calibration: a dedicated scorer, not a verifier who has read the annotations, scores both exemplars blind from a stripped copy within one level per criterion (architect ruling 23; ruling 15). The page keeps its annotations for learners.

Not adversarial: the curriculum deliverable is "Estimation code plus memo." (`yaml:731`). No question bank (Q9).

### 5.5 Autograder (`section.grader-panel#grader`, `check_projects.py:122-136`)

Panel attributes (CF1 pattern, `course/modules/CF/CF1/project.html`): `data-unit="CF2" data-grader="grader/" data-suite="test_project.py" data-support="instance.py" data-solution="wacc_engine.py" data-starter="starter.py" data-packages=""`. Required files (`check_projects.py:122-136`): `grader/test_project.py`, `grader/starter.py`, `grader/instance.py` (defines `make_instance(seed: int)`), `grader/reference.py`. Grader design follows `course/modules/CF/CF1/grader/` (built): instance, reference, starter, test.

**`grader/instance.py`.** `make_instance(seed: int) -> dict`, deterministic from `random.Random(seed)`. Fields: `firm_returns`, `market_returns` (decimal, 36 to 60 periods), `risk_free` (decimal per year, in [0.01, 0.08]), `erp` (decimal per year, in [0.02, 0.08]), `spread` (decimal, in [0.005, 0.05]), `debt_market_cents`, `equity_market_cents` (positive integers; D/E in [0.05, 3]), `debt_book_cents` (different from the market value in every seed), `tax_rate` (in [0, 0.45]), `cash_flow_cents` (positive integer), `growth` (in [0, 0.03]), with `wacc - growth >= 0.02` by construction. Validity: every seed valid. Answers differ across seeds: WACC differs by at least 0.005 between seed pairs in a sample of 50 seeds (the test checks materially different answers, not just labels).

**`grader/reference.py`.** Full solution. Functions and conditions (each named condition raises **ValueError** and nothing else; fixer-rules line 19: the page names the error type for every condition, a test demands only the type the page names, and no other exception type is required):
- `beta_ols(firm, market) -> float`: sample covariance over sample variance, both with n-1; ValueError if lengths differ, if n < 2, or if the market variance is zero.
- `unlever_beta(beta_levered, debt_cents, equity_cents, tax_rate) -> float` = `beta_L / (1 + (1 - tau_c) D/E)`; ValueError if D < 0, E <= 0, or tax rate outside [0, 1).
- `relever_beta(beta_unlevered, debt_cents, equity_cents, tax_rate) -> float` = inverse; same ValueError conditions.
- `cost_of_equity(risk_free, beta, erp) -> float` = `r_f + beta ERP`.
- `cost_of_debt(risk_free, spread) -> float` = `r_f + s`.
- `wacc(debt_cents, equity_cents, cost_equity, cost_debt, tax_rate) -> float`; ValueError if D < 0, E < 0, D + E <= 0, or tax rate outside [0, 1).
- `wacc_delta_variance(debt_cents, equity_cents, beta, erp, var_beta, var_erp, cov_beta_erp, var_spread, tax_rate) -> float`: the linearised variance with weights and tax treated as known (A8); ValueError on negative variances or on `var_beta * var_erp < cov_beta_erp**2`.
- `valuation_range(cash_flow_cents, growth, wacc_mid, wacc_se, k=1.0) -> (int, int)`: value = `C_1 / (r - g)`, endpoints at `r = wacc_mid ± k·wacc_se`, low value at the high rate, rounded half-up to integer cents on the exact value; ValueError if the cash flow is not a positive integer, if `k < 0`, if `wacc_se < 0`, or if either endpoint rate is at or below `growth`.

Rates are read as exact decimals (`Fraction` of the decimal string) in the reference, so the half-up rule is unambiguous (the pattern of FINAL-ARCHITECT-RULINGS ruling 35; the page states it in one sentence).

**`grader/starter.py`.** The same names, each `raise NotImplementedError`; each test that calls one of them fails with a named property, not a stack trace.

**`grader/test_project.py`.** Property and number tests. Planned list (the verifier may add tests; each new test is named on the page in the same change; fixer-rules line 19):
1. `test_beta_recovers_noise_free_slope`: firm = a * market + b with no noise; the estimate equals a to 1e-12.
2. `test_beta_uses_one_normalisation`: covariance and variance use the same divisor, so a doubled sample gives the same beta (kills M06).
3. `test_beta_rejects_short_and_flat_series`: n = 1 and zero market variance raise ValueError; n = 2 with variance is accepted (both directions).
4. `test_unlever_hand_value`: a fixed fixture (D/E = 1, tau_c = 0.25, beta_L = 1.2 gives beta_U = 1.2 / 1.75) to 1e-12 (kills M01).
5. `test_relever_inverts_unlever`: round trip for every seed in 0-49 within 1e-12 (kills M02).
6. `test_zero_debt_leaves_beta`: D = 0 gives beta_U = beta_L.
7. `test_tax_rate_boundaries`: 0 accepted, 1 rejected, -0.01 rejected.
8. `test_wacc_hand_value`: fixed fixture for weights and rates (kills M04, M05).
9. `test_wacc_equals_cost_of_equity_without_debt`: D = 0 gives r_E.
10. `test_wacc_rejects_nonpositive_capital`: D + E = 0 rejected; D + E > 0 accepted (both directions).
11. `test_wacc_uses_market_values`: the instance's book debt and market debt give different weights; the engine must use market (kills M03 by seed).
12. `test_delta_variance_matches_exact_moments`: for jointly normal (beta, ERP) with covariance c, the exact variance of WACC minus the linearised variance equals `w_E^2 (Var(beta) Var(ERP) + c^2)` to 1e-12 (kills M07 when c ≠ 0).
13. `test_monte_carlo_within_four_standard_errors`: 20,000 seeded draws; the MC variance is within four MC standard errors of the exact moment (runtime under 5 s in Pyodide).
14. `test_zero_inputs_zero_variance`: all variances zero gives zero.
15. `test_valuation_growing_perpetuity`: value = C/(r - g) for a fixed fixture (kills M08, r + g).
16. `test_valuation_half_up_in_cents`: a fixture whose exact value is a half-cent under exact decimal arithmetic rounds up (kills M09).
17. `test_valuation_range_brackets_base_value`: low <= base <= high for every seed.
18. `test_wider_error_wider_range`: doubling `wacc_se` widens the range.
19. `test_k_boundaries`: k = 0 gives a point value; k = -0.1 raises ValueError.
20. `test_rate_at_or_below_growth_rejected`: endpoint r = g and r < g raise ValueError; r = g + 1e-9 accepted (both directions).
21. `test_cash_flow_must_be_positive_integer_cents`: 0, -1, and 1.5 raise ValueError; 1 accepted.
22. `test_large_cents_accepted`: cash flow and debt of 10**18 cents accepted and rounded correctly (architect ruling 36, threshold family).
23. `test_instances_valid_and_different`: seeds 0-49 valid; answers differ (section 5.5).
24. `test_messages_name_the_rule_not_the_answer`: each failing assertion names the property and never prints the expected value (`__tracebackhide__` in helpers; fixer-rules line 19).
Runtime: each test under 5 s in Pyodide; the whole suite under 60 s.

**Ten student-error mutants** (single-change copies of the reference; under `ledgers/CF2/mutants/` at verification; first docstring line names the student error; killed by `tools/mutate_graders.py --unit CF2 --seeds 0-9`):

| ID | Student error (single change) | Expected killer |
|---|---|---|
| M01 | unlever without the (1 - tau_c) term: `beta_L / (1 + D/E)` | test 4 |
| M02 | relever with the sign of the debt term reversed | test 5 |
| M03 | book debt in the weights and in D/E where market values are required | test 11 (seeded) |
| M04 | WACC weights swapped: E/V on r_D and D/V on r_E | test 8 |
| M05 | pre-tax cost of debt in WACC (no (1 - tau_c) on r_D) | test 8 |
| M06 | beta with n-1 on the covariance and n on the variance | test 2 |
| M07 | delta-method variance drops the covariance term between beta and ERP | test 12 (requires c ≠ 0 in the test fixture) |
| M08 | growing perpetuity with `r + g` in the denominator | test 15 |
| M09 | valuation in cents by truncation instead of round-half-up | test 16 |
| M10 | hard-coded answer for seed 0: returns the seed-0 range for every seed | test 17 and test 23 (seed loops) |

Every mutant must fail at least one test (architect ruling 9: a survivor that violates a stated behaviour is killed by a new test; a survivor that differs only where the page states nothing goes to `ledgers/CF2/equivalent/` with a README proof). M07 and M06 must be checked for equivalence at the instance values: if an instance has c = 0 for every seed, M07 is equivalent and must be killed by the fixture of test 12 instead.

**Five alternative correct implementations** (different styles; each passes seeds 0-49; architect ruling 10):
- A1 loop-based beta on deviations from the means (no `sum` of products over a list comprehension).
- A2 exact `Fraction` arithmetic in the WACC and unlevering core, float only at the return.
- A3 delta variance by a central finite-difference gradient of WACC (step stated; tolerance on the variance 1e-9 relative).
- A4 class-based design (a `CapitalStructure` dataclass with methods wrapping the same formulas).
- A5 valuation range computed by evaluating the growing perpetuity at the two endpoint rates instead of the closed form in k (same half-up rounding).

**Tolerances (stated on the page).** Beta, WACC and variance: absolute 1e-12 on exact hand fixtures; 1e-9 relative across seeds for alternatives. Monte Carlo: four standard errors. Valuation: exact integer cents, no tolerance.

### 5.6 Integrity

The page states that the suite is public and that integrity rests on per-seed instances (BUILDER_RULES §5.3 item 6). The reference is not deployed (`grader/reference.py` is tracked; FINAL-ARCHITECT-RULINGS ruling 4 applies once a deploy step exists).

---

## 6. Real-data policy

- **Embedded and used: `ust_daily` (`tools/data_sources.yaml:91-116`; `course/assets/data/market/ust_daily.csv`; MANIFEST entry `ust_daily`).** The column `cmt_10y` is the 10-year Treasury constant-maturity yield, percent per year, as published by the Board's H.15 release (series RIFLGFCY10_N.B, `data_sources.yaml:116`). Licence quote: "Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information." (`data_sources.yaml:96-97`; licence page `:98`). The `note` (`:100-107`) states that the constant maturity names "U.S. Treasury" as its source and that a U.S. Treasury series is a work of the U.S. Government (17 U.S.C. 105(a)). MANIFEST: `retrieved` 2026-10-20; rows 6690; columns `tbill_3m`, `cmt_10y`; first 2000-01-03; last 2026-09-30.
  - Use in CF2: the risk-free rate of the project's rung 3 check (`lab-CF2-project-3`, `data-files="ust_daily.csv"`) and of the memo's input 1. The lab reads `data/ust_daily.csv` as `Path("data") / "ust_daily.csv"`. No other lab reads it.
  - Basis: the builder states "as published, percent per year, not converted" (section 2.1 item 11). A compounding or day-count claim is not made unless the builder reads and quotes the H.15 release notes (Q8).
  - Only `cmt_10y` is used. `tbill_3m` is on a discount basis (`data_sources.yaml:101`) and is not used for CF2.
- **Not embedded, no grant found:** firm and market returns, an equity risk premium, a credit spread, and the firm's balance sheet. `data_sources.yaml` has no entry and no rejection record for these (B1). Labs and the autograder use SIMULATED data. The project uses bring-your-own-data for them.
- **Honest-pending note** on the project's data page and on L02-L03: "The estimation of beta, the equity risk premium and the credit spread needs return and spread series that no redistributable source is embedded for yet. The labs and the grader use a generated firm labelled SIMULATED (BUILDER_RULES §1.7). Only the risk-free rate is real data." Cited to the DATA_REQUESTS (below).
- **DATA_REQUESTS (for the architect; the planner names no source and no licence from memory):** (1) firm and market total-return series, each with issuer URL, quoted licence sentence, licence page and transform (BUILDER_RULES §6.6 steps 1-5); (2) an equity risk premium series with the same five fields; (3) a corporate credit-spread series with the same five fields. The BLUEPRINT §5.3 candidates (FRED series under their owners' terms; Shiller's data; Treasury yields direct) must each be checked before use.
- No `data-files` attribute on any lab except `lab-CF2-project-3`. No MANIFEST entry is added by builders.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (each verified in `references/references.json`; the planner read each record)

| Key | Record (as read) | Locator | Use in CF2 | Rule |
|---|---|---|---|---|
| `myers1984capital` | Myers, "The Capital Structure Puzzle", JF 39(3) 574-592 | `references.json:17697` (source string `:17724`) | L06 trade-off framing; reading list | paper level; read the abstract before any attribution; grade C with design named unless a locator is read |
| `myers1984corporate` | Myers & Majluf, "Corporate financing and investment decisions when firms have information that investors do not have", JFE 13(2) 187-221 | `:17734` (source `:17764`) | L07 pecking order framing; reading list | paper level; abstract first |
| `fama2002testing` | Fama & French, "Testing Trade-Off and Pecking Order Predictions About Dividends and Debt", RFS 15(1) 1-33 | `:8610` (source `:8640`) | L06, L07 evidence; reading list | empirical; grade B only with counter-evidence named (R4); until then C with the design named |
| `baker2002market` | Baker & Wurgler, "Market Timing and Capital Structure", JF 57(1) 1-32 | `:1428` (source `:1458`) | L08 evidence | empirical; grade B only with counter-evidence (R5); until then C |
| `leland1994corporate` | Leland, "Corporate Debt Value, Bond Covenants, and Optimal Capital Structure", JF 49(4) 1213-1252 | `:15562` | L06 optional, paper level for the structural trade-off model | used_by currently CR1; the architect updates `used_by` (Q12); the model is not reproduced |
| `damodaran2012investment` | Damodaran, *Investment valuation: tools and techniques for determining the value of any asset*, 2012 (book) | `:6388` | optional WACC practice, book level | grade C, locator required; not required |
| `graham2001theory` | Graham & Harvey, "The theory and practice of corporate finance: evidence from the field", JFE 60(2-3) 187-243 | `:10981` | optional CFO practice on capital structure | used_by CF1; quote no figure unless the locator is read (CF1 decision) |

Not cited by CF2: `brealey2022principles` (N3); `lintner1965valuation` (AP2's key, not needed); `merton1974pricing` (CR1 scope); `jensen1976theory` (CF3 scope); `miller1961dividend` (CF3 scope); `glasserman2003monte` (M8 scope, optional for the Monte Carlo method if the builder reads the locator).

### 7.2 Not admitted

- **Modigliani & Miller (1958), AER 48(3), and (1963), AER 53(3)** (`yaml:719-720`). Not in the registry (`review_queue.json:545` and `:598`; `SEED_REPORT.md:38-39`). No admissible route (research run, `plans/reference-queue-research-2026-10-27.md:33-34`). CF2 cites no M&M key. Propositions derived on the page (T). See B3.

### 7.3 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- **R1** {doi: null, authors: "Modigliani and Miller (lead only)", year: "1958 and 1963 (lead only)", title: "the cost-of-capital and corporate-tax papers named in yaml:719-720 (lead only; record not typed)", venue: "American Economic Review (lead only)", needed_for: "L04 and L05 attribution of Proposition I, Proposition II and the tax result", confidence: "the source string exists; the record cannot be admitted by any route in plans/reference-queue-research-2026-10-27.md:33-34; a stable AEA page admitted by a human is the only route"}.
- **R2** {doi: null, authors: "Literature on information asymmetry and financing order (lead only; no author typed)", year: "not typed", title: "tests of the pecking-order and trade-off models beyond fama2002testing", venue: "not typed", needed_for: "L06 and L07 counter-evidence to fama2002testing (BUILDER_RULES §2.5)", confidence: "the need is certain; no record identified by this planner"}.
- **R3** {doi: null, authors: "Literature on market-timing persistence (lead only)", year: "not typed", title: "evidence on market-timing effects on leverage beyond baker2002market", venue: "not typed", needed_for: "L08 counter-evidence", confidence: "the need is certain; no record identified"}.
- **R4** {doi: null, authors: "Literature on the magnitude of financial distress costs (lead only)", year: "not typed", title: "empirical estimates of distress costs", venue: "not typed", needed_for: "L06 counter-evidence for the distress-cost function's size", confidence: "the need is certain; no record identified"}.
- **R5** {doi: null, authors: "Literature on estimation error in beta and the equity risk premium (lead only)", year: "not typed", title: "precision of beta and ERP estimates", venue: "not typed", needed_for: "L03 and the project's memo criterion 5", confidence: "the need is certain; no record identified"}.
- **R6** {doi: null, authors: "Literature on leverage adjustment speed (lead only)", year: "not typed", title: "estimates of target-adjustment speed for corporate leverage", venue: "not typed", needed_for: "L09 (the lesson makes no empirical speed claim without it)", confidence: "the need is certain; no record identified"}.
- **R7** {doi: null, authors: "Literature on debt betas (lead only)", year: "not typed", title: "evidence on the beta of corporate debt", venue: "not typed", needed_for: "L02 justification of the debt-beta-zero assumption (A7)", confidence: "the need is certain; no record identified"}.

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4). Until resolved, the lessons teach the models by derivation, cite empirical claims at C with the design named, or delete them.

---

## 8. Atlas milestone

None. No `atlas:` key on CF2 (`yaml:699-732`) and no Atlas entry names CF2 (section 0.1). No `atlas/CF2.contract.md` is needed. The project does not use Atlas (B2 pattern; the CF2 brief says nothing about Atlas, `yaml:728-730`).

---

## 9. Cards builder (Builder F, after A-E)

- `course/modules/CF/CF2/cards.json`, ids `CF2-c001` upward, `lesson` in L01-L09, one card per definition, theorem statement, key formula, key result and misconception (BUILDER_RULES §7). `check_pages.py` `check_cards` checks the id prefix, lesson existence, grades and registry keys (`check_pages.py:366` onward).
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example `"basis": "Lab L05, Derivation 2 (exact)"`.
- Cite a registry key only for an empirical or attributed claim. `cite` is `[]` where the card is a model result. No card cites an M&M key (none exists, section 7.2).
- Cards for a SIMULATED result name the SIMULATED lab in `basis`, and their grade is C.
- A card and the key-results row it mirrors carry the same grade and basis.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit CF2            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit CF2
.venv/bin/python tools/check_projects.py --unit CF2
.venv/bin/python tools/run_labs.py --unit CF2               # --page L02 for one lesson
.venv/bin/python tools/run_graders.py --unit CF2 --seeds 0-49
.venv/bin/python tools/embed_labs.py course/modules/CF/CF2/L01.html                          # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/CF/CF2/L06.html --refresh lab-CF2-L06-1  # after editing a twin
.venv/bin/ruff check tests/labs/CF2 course/modules/CF/CF2/grader && .venv/bin/ruff format --check tests/labs/CF2 course/modules/CF/CF2/grader
.venv/bin/mypy tests/labs/CF2 course/modules/CF/CF2/grader  # strict, repository configuration
```

- `run_graders.py --unit CF2` runs because CF2's grading is `both` (`tools/run_graders.py:138-139` skips units whose grading is not `autograder` or `both`; CF1 precedent, `plans/CF1-build-plan.md:19`).
- Verifier only, on a quiet machine: `.venv/bin/python tools/mutate_graders.py --unit CF2 --seeds 0-9`; `.venv/bin/python tools/page_smoke.py --unit CF2` (timing-sensitive; not run by builders); `.venv/bin/python tools/verify_refs.py --unit CF2` (VERIFIER §2.1); `.venv/bin/python tools/fetch_data.py --check` (offline; required because the project reads `ust_daily`).
- Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`, `render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`, and the full gate in CLAUDE.md.

Flag checks: `check_pages.py`, `check_dag.py`, `check_projects.py` and `run_labs.py` accept `--unit`; `embed_labs.py` accepts pages and `--refresh [LAB_ID ...]`. The planner did not execute the builder commands on CF2 (CF2 is not built); only the coursekit closure, the concept owners and the anchor checks were run (section 0.1).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **AP2 is unbuilt** (section 0.1). CF2 links AP2 concepts through `concepts.html` anchors, which exist. The hub's prerequisite list cannot link an AP2 page.
2. **`check_dag` sees linked uses only** (section 4). Unlinked uses of D1-D12 pass the tool; the verifier reads for them.
3. **No debate.** `check_pages.py` requires a debate brief only when the entry has a `debate` key (the CF1 and E5 precedent); CF2 has none. The two-sided rule still applies to the grade-B and grade-C claims in L06-L08.
4. **No Atlas.** `check_projects.py` skips the Atlas contract check when the project has no `atlas` key (`check_projects.py:144-146`).
5. **Rung 2 must be graded instantly.** `check_projects.py` accepts a completion lab or a quiz (the plan uses a completion lab, architect ruling 11).
6. **Grader panel and files.** `check_projects.py:122-136` requires the five panel attributes and the four grader files; `data-solution` (`wacc_engine.py`) is a student file and is not checked for existence by the tool, so the builder must still ship a reference solution at `grader/reference.py`.
7. **Pyodide packages.** The grader and labs use only the standard library, so `data-packages=""` (CF1 pattern). The architect confirms that the Pyodide runner accepts an empty package list (CF1 open item 6, not checked by the planner).
8. **Frontier of the closure.** Concepts of CF3, CF4, CF5, CR1 and CR3 are unusable (they require CF2; section 4). A builder who needs one of them has found a DAG defect.
9. **Name collision.** CF2's `leverage-dynamics` (target adjustment, leverage) and CF3's `lintner-partial-adjustment` (dividends) are different objects. CF2 defines no concept named after Lintner. The architect is told once so that CF3 is not blocked by CF2's wording.
10. **Board removal of the download route** (N2). The pinned snapshot keeps the gate offline-valid; a refresh may fail.

---

## 12. Open questions for the architect (numbered; recommended decision for each)

1. **Q1 (BLOCKING, lesson count and hours).** Confirm 9 lessons × 7 h and a 17 h project (21%). **Recommended: yes.** It gives the "about three per builder" split (A 3, B 2, C 2, D 2). Alternative: 8 × 8 h and a 16 h project (20%, CF1 ratio), which gives A 2, B 2, C 2, D 2 and departs from the three-per-builder instruction.
2. **Q2 (BLOCKING, D1).** Add E2 to CF2's prerequisites so that `adverse-selection` and `signaling` may be linked in L07. **Recommended: yes** (curriculum change; E2 closure has no CF2, so no cycle; E2 is built; CF3 and the PhD group already tie E2 to CF2-CF3, `meta.yaml:77` and `:130`). Default if not approved: plain prose in L07, no link.
3. **Q3 (D2).** Add S2 as a prerequisite for the OLS and attenuation content? **Recommended: no.** Beta is defined as covariance over variance in closure; attenuation bias is plain prose; S2 is unbuilt and large (120 h).
4. **Q4 (D3).** Add FI1 for the yield concepts? **Recommended: no.** The cost of debt is the rate that prices the promised cash flows, using M1 `present-value` and `annuity`. FI1 is unbuilt and large (90 h).
5. **Q5 (interface).** Approve the module-local engine name `wacc_engine.py` and the function names and signatures in section 5.5. **Recommended: yes.**
6. **Q6 (B3, sources).** Accept the Modigliani-Miller source gap as a named honest gap: CF2 cites no M&M key; propositions derived (T); the gap is listed in KNOWN-ISSUES. **Recommended: accept.** Alternative: a human admits a stable AEA page through `add_reference.py`. The builders must not attempt either.
7. **Q7 (data, B1).** Confirm: `ust_daily` `cmt_10y` as the real risk-free rate; returns, ERP and spreads in bring-your-own-data mode; SIMULATED labs and grader; DATA_REQUESTS R1-R3 of section 6. **Recommended: yes.** No real firm is shown.
8. **Q8 (basis).** Confirm the basis convention for `cmt_10y`: "as published, percent per year, not converted" (default). A compounding claim requires reading the H.15 release notes first, which the planner did not do. **Recommended: default.**
9. **Q9 (adversarial).** Confirm the project is not adversarial (no question bank): the deliverable is "Estimation code plus memo." (`yaml:731`). **Recommended: confirm.**
10. **Q10 (figures).** No live figures and no new JS kernels (architect default; CF1 Q6 precedent). **Recommended: confirm.**
11. **Q11 (scope).** Confirm the CF2 scope: single firm; static closed-form MM and tax-shield models; constant leverage; permanent debt; debt beta zero; the trade-off optimum on a stated grid; pecking order and market timing described and tested by the stated labs only; no option, structural credit, dividend or FCFF model. **Recommended: confirm.**
12. **Q12 (registry used_by).** `leland1994corporate` is used by CR1 and would be cited by CF2 (optional, L06). The architect updates `used_by` through the registry tooling, or CF2 does not cite it. **Recommended: cite only if the architect updates `used_by`; otherwise omit.**
13. **Q13 (notation).** Confirm the rules of section 2.3: `\tau_c` for the corporate tax rate; `r_f` net with `R_f` not used; `T` never used for samples or taxes; `\Var`, `\Cov`, `\se` macros for the delta formulas; `\E` only as the expectation operator. **Recommended: confirm; no NOTATION_REQUESTS.**
14. **Q14 (valuation range and money).** Confirm: range multiplier k = 1 standard error by default (the user sets k; no normal-distribution claim is made); money in integer cents, round-half-up on the exact value; rates read as exact decimals. **Recommended: confirm.**
15. **Q15 (mutants and alternatives).** Confirm the ten mutants M01-M10 and five alternatives A1-A5 of section 5.5. **Recommended: confirm.** The verifier may replace a mutant only with one the architect approves.
16. **Q16 (Atlas).** Confirm that CF2 has no Atlas milestone and no contract. **Recommended: confirm** (no Atlas entry names CF2).
17. **Q17 (meta).** Observation only: CF2 (tier U) is in the PhD first-year group (`meta.yaml:130`), as is E5 (`meta.yaml:133`, E5 plan §11 item 10). **No action.**

---

## 13. After the builders

1. Orchestrator integrates; runs the section 10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L03 (includes the error lab), L04-L05, L06-L07 (includes the curriculum lab), L08-L09, project (grader mutants, alternatives and rubric calibration by a dedicated blind scorer, architect ruling 23). Failing rows return to the builder who owns the file, with only the failing rows.
3. Ledger at `ledgers/CF2.verification.json`; verifier scripts archived under `ledgers/CF2/scripts/` (VERIFIER §3); mutants under `ledgers/CF2/mutants/`; equivalents with a README under `ledgers/CF2/equivalent/`.
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1-B3 must be resolved or named as honest gaps first (B3 may be named under Q6).

Architect decisions: pending (section 12). This plan is the planner's proposal.
