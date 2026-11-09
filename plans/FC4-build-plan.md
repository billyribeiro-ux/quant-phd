# FC4 build plan: Investments & Equity Security Analysis (2026-11-09)

Unit: **FC4 · Investments & Equity Security Analysis** · tier U · 90 h · prerequisites AP2, AC2, CF1 · nearest built
prerequisite AC2 (§0.2) · no debate key · grading `both` (autograder and rubric) · output directory
`course/modules/FC/FC4/` · lab twins `tests/labs/FC4/` · grader `course/modules/FC/FC4/grader/` · ledgers `ledgers/FC4/`.
Atlas: the brief names A15 and A16; see §0.3 B1.

Planner: Haiku, plan only. No lesson text, no git operations, no commits, no edits to any file except this plan.
Executors: Haiku builders A to E (content, hub, project, grader), Builder F (cards), then independent Haiku verifiers
(VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every statement about the curriculum cites `file:line` read during planning. Every statement about
the tooling was checked by reading the tool source (`tools/*.py`) or by running `tools/coursekit.py` through
`.venv/bin/python`. Anything not in the curriculum, the registry or the tools is marked **NOT IN CURRICULUM**.

**Status: BLOCKING ISSUES EXIST (§0.3). Hours are feasible (60 h lessons + 30 h project = 90 h). The Atlas wording (B1),
the real-company data (B2) and the prerequisite build order (B6) must be decided before the verification round.
Drafting can start after the architect confirms §12 Q1 to Q4.**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part FC, code `FC`, title "Finance Core", order 5 | `curriculum/02-economics-finance-core.yaml:347-349` |
| FC4 id and title "Investments & Equity Security Analysis" | `yaml:461-462`; `curriculum/curriculum.json:7837-7838` |
| Tier `U`, hours `90` | `yaml:463-464`; `curriculum.json:7839-7840` |
| Prereqs `[AP2, AC2, CF1]` | `yaml:465`; `curriculum.json:7841-7845` |
| Core: "Equity markets and instruments, industry and competitive analysis, the dividend discount model, FCFE and residual-income approaches, multiples, sell-side vs. buy-side research, and the evidence on analyst forecasts and recommendations." | `yaml:466-470` |
| `introduces` has 11 concepts (listed in §1) | `yaml:472-482`; `curriculum.json:7847-7859` |
| Sources: six strings (Gordon & Shapiro 1956; Graham & Dodd 1934; Porter 1979; Womack 1996; Hong & Kubik 2003; Bodie, Kane & Marcus 13th ed. 2024) | `yaml:484-489`; `curriculum.json:7860-7866` |
| Lab: "Gordon-growth sensitivity: value as (r − g) shrinks." | `yaml:490`; `curriculum.json:7868` |
| Project "Initiation-of-coverage report" | `yaml:491-492` |
| Brief: "Write a full sell-side-format initiation on a real public company: industry and competitive analysis, an Atlas-driven model (A15/A16), a price target with bull/base/bear scenarios and probabilities, key risks, and what would change the call." | `yaml:493-497`; `curriculum.json:7871` |
| Deliverable "Initiation report plus model."; grading `both` | `yaml:498-499`; `curriculum.json:7872-7873` |
| No `debate:` key on FC4 | `yaml:461-499` (absent) |
| No `atlas:` key on the FC4 project | `yaml:491-499` (absent) |
| The FC studio (`STUDIO-FC`) requires FC1 and FC2, not FC4 | `yaml:350-353` |
| BS-FIN credential requires FC4 | `curriculum/meta.yaml:62` |
| Course map "Investments" lists AP2, FC3, FC4 | `meta.yaml:78` |
| Topic "Equity Investments" lists FC3, FC4, CF4 | `meta.yaml:158` |
| Track EQR (Equity Research / Asset Management) targets FC4 | `meta.yaml:181-183` |
| CAP0 prereqs include FC4; CAP0 brief names "an initiation report (FC4)" | `curriculum/06-profession-capstone.yaml:192`, `:207` |
| Topological position of FC4 is 56 (0-based) of 134 | `curriculum.json:1036-1171` (array; FC4 at `:1093`); `tools/coursekit.py` `topological_order` |
| Prerequisite closure of FC4 (computed by the planner): {AC1, AC2, AP2, CF1, CS1, E1, E3, M1, M2, M3, M4, M7, P0.1, S0, S1, S2} | `tools/coursekit.py:239-251` (`prerequisite_closure`), run output |
| Closure modules not yet built: AP2, CS1, P0.1, S0, S1, S2 | `course/modules/` listing (built = `index.html` exists, `tools/coursekit.py` `Unit.built`) |
| Direct prerequisites: AP2 (pos 34, unbuilt), AC2 (pos 43, built), CF1 (pos 11, built) | `topological_order` positions; built flags as above |
| All 11 FC4 concepts are owned by FC4 | `curriculum.json` `concepts` (planner check with `tools/coursekit.py` `concept_owner`) |
| Atlas A15 "Fundamentals engine", module AC2 | `curriculum.json:258` (A15 entry) |
| Atlas A16 "Valuation engine", module CF4 (CF4 is at topological position 59, after FC4) | `curriculum.json:264` (A16 entry); topological positions |
| A15's contract says it is consumed by A16 | `atlas/A15.contract.md:10` |
| AC2's project is Atlas A15 (`atlas: A15`) | `yaml:578-585` |
| No `atlas/A16.contract.md` exists | `atlas/` listing (A1, A2, A3, A5, A8, A15 contracts present) |

### 0.2 Hours feasibility and the nearest built prerequisite (no conflict)

The curriculum figure is 90 h (`yaml:464`). Tool rules: lesson `data-hours` 6 to 12 (`tools/check_pages.py:227`); hub
`data-hours-lessons + data-hours-project = 90` (`check_pages.py:337`); project share 10 to 40 %, i.e. 9 to 36 h
(`check_pages.py:340`); lessons sum to the hub's lessons figure (`check_pages.py:341-342`).

Chosen split (§1): **10 lessons × 6 h = 60 h; project 30 h (33 %)**. 60 + 30 = 90. Feasible. The same 60/30 split is
the sibling FC2 plan's split for a 90-hour unit (`plans/FC2-build-plan.md:85-96`; built hub `course/modules/FC/FC2/index.html:29`).
**No STOP condition on hours.**

Nearest built prerequisite. Rule used: the direct prerequisite with the largest topological position among the built
direct prerequisites. AP2 (position 34) is unbuilt. AC2 (position 43) is built and is the nearest. CF1 (position 11)
is built but earlier. Therefore **AC2** is the nearest built prerequisite, and `plans/AC2-build-plan.md` is the plan read
for this file. Lessons the AC2 plan records that FC4 inherits: the real-data rule (AC2 plan, "Real data" bullet: generated
filers labelled SIMULATED with an honest-pending note while the SEC source is not cleared); the A to E ownership pattern;
the grader panel and the rule that unit-level gates fail until every builder finishes (AC2 plan, "Rules for every builder").

### 0.3 Blocking issues (architect decision required before the verification round)

**B1. The brief names Atlas A15 and A16. A16 is outside the closure and has no contract.**
- The brief says "an Atlas-driven model (A15/A16)" (`yaml:495`).
- A15 is AC2's milestone (`curriculum.json:258`; `yaml:578-585`). AC2 is in the closure, so A15 is usable and its
  contract exists (`atlas/A15.contract.md`).
- A16 is CF4's milestone (`curriculum.json:264`). CF4 is at topological position 59, after FC4 (56), and is not in the
  closure. No `atlas/A16.contract.md` exists. A15's contract names A16 as its consumer (`atlas/A15.contract.md:10`).
- `check_projects.py` checks an Atlas contract only when the project names an `atlas` key (`tools/check_projects.py:144-146`).
  Nothing enforces the brief's wording, so the verifier must reject any page that relies on A16.
- **Plan's default:** the project does not require Atlas. A15 is optional for students who completed AC2's project. A16 is
  not used. The architect either accepts this reading or edits `yaml:495` (a curriculum change; builders do not edit
  `curriculum/*.yaml`).

**B2. The brief asks for a real public company. No redistributable fundamentals source is embedded or cleared.**
- Embedded snapshots: `fx_daily`, `fx_monthly`, `ust_daily` only (`tools/data_sources.yaml:19`, `:53`, `:91`;
  `course/assets/data/market/MANIFEST.json` lists exactly these three).
- Rejected sources: French library and Open Source Asset Pricing (`tools/data_sources.yaml:119-`, entries at `:120` and `:132`).
- No EDGAR or fundamentals source is listed in `tools/data_sources.yaml` (grep of the file, planner). The AC2 plan records
  the same gap for EDGAR company facts (`plans/AC2-build-plan.md`, "Real data" bullet).
- **Plan's default:** labs and the autograder use generated companies labelled **SIMULATED**. The student chooses a real
  public company and supplies its statements as a bring-your-own-data CSV that never leaves the browser (BUILDER_RULES §6.6,
  last bullet). The project page carries an honest-pending note naming the missing source. A DATA_REQUEST is raised (§6).

**B3. Porter (1979) and Graham & Dodd (1934) are cited in the curriculum but have no registry record.**
- Curriculum strings: `yaml:485` ("Graham & Dodd, Security Analysis (1934)") and `yaml:486` ("Porter (1979), 'How Competitive
  Forces Shape Strategy', Harvard Business Review 57(2)").
- Neither has a key in `references/references.json` (planner grep of the registry by author and title). Both are in
  `references/review_queue.json` with "no candidate established identity": Graham & Dodd at `:375`, Porter at `:428`.
- The queue's candidates are different documents. For Graham & Dodd the candidates are two "Diary" monographs and a JAMA
  abstract (`review_queue.json:375-`). For Porter the candidates are "In Retreat: The Canadian Forces in the Trudeau Years",
  "Industry Structure and Competitive Strategy: Keys to Profitability" (Financial Analysts Journal, 1980) and an unrelated
  article (`review_queue.json:428-`). **None may be admitted.**
- **Plan's default:** both go to REFERENCE_REQUESTS (§7.2). L02 teaches the five-forces framework as a definition and makes
  no attribution. Graham & Dodd is not cited.

**B4. Bodie, Kane & Marcus: edition year conflict.**
- Curriculum: "Bodie, Kane & Marcus, Investments, 13th ed. (2024)" (`yaml:489`).
- Registry record `bodie2023investments` (`references/references.json:3255`) has year 2023. Its `notes.year` flags
  `curriculum: 2024` vs `record: 2023` (`references.json:3298`).
- **Plan's default:** cite the key only, with no edition and no year in the prose. The architect may correct `yaml:489`
  after checking the edition.

**B5. The Gordon & Shapiro record does not show the dividend-growth formula in its title.**
- Registry record `gordon1956capital` (`references/references.json:10704`) has the title "Capital Equipment Analysis: The
  Required Rate of Profit", Management Science, volume 3, issue 1, pages 102-110, year 1956, DOI 10.1287/mnsc.3.1.102.
- The planner has not read the paper and does not know its content. The title alone does not establish that the paper
  states the growing-perpetuity valuation formula.
- **Plan's default:** L04 derives the formula on the page (grade T, from the M1 growing perpetuity). The builder cites
  `gordon1956capital` for the attribution only after reading the abstract at the record's DOI (VERIFIER §2.1). If the
  abstract does not confirm it, the page makes no attribution.

**B6. Sequencing: the closure is mostly unbuilt.**
- Unbuilt closure modules: AP2 (topological position 34), S1 (22), S2 (28), S0 (9), CS1 (3), P0.1 (0). Built: AC1, AC2, CF1,
  E1, E3, M1, M2, M3, M4, M7.
- FC4 links to AP2 concepts (`capm`, `beta`, `equity-risk-premium`) and to an S1 concept (`estimator-bias-variance`).
  `check_dag.py` accepts a use of a closure concept whatever the owner's build status (`tools/check_dag.py:60-69`).
  `build_site.py` lists every concept in `concepts.html`, built or not (`tools/build_site.py:374-381`), so the link resolves.
  The definition, however, exists only on an unbuilt page, so the link is not verified against a `<dfn>`.
- **Plan's default:** FC4 verification starts only after AP2, S0, S1, S2, CS1 and P0.1 are built. The fan-out in
  topological order already does this (positions 0 to 34 precede 56). Drafting FC4 pages is allowed in parallel.

**B7. Residual income is defined by a built unit outside the closure.**
- AC4 (built; topological position 10; `yaml:614` id) introduces `residual-income` ("Residual income"): `yaml:635`;
  `curriculum.json:8028`; concept map `curriculum.json:4781`. AC4 is not in FC4's closure.
- FC4's `residual-income-valuation-model` (`yaml:478`) is a different concept id. Re-teaching the same content would
  duplicate AC4's definition. See §4 D1.

Non-blocking: none of the other facts block the build.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

10 lessons × 6 h = 60 h; project 30 h; total 90 h. Concept counts per row sum to 1+1+1+1+1+1+1+1+1+2 = 11, each concept in
exactly one row (`yaml:472-482`).

| Lesson | Title (working) | Concepts it defines (`introduces`, `yaml:472-482`) | Lab (twin id, `tests/labs/FC4/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Equity instruments and the residual claim | `equity-instruments` | `lab-FC4-L01-1`: a residual-claim waterfall on an illustrative capital structure; the common-equity value is the firm value less senior claims, floored at zero; SIMULATED label | 6 | Builder A |
| L02 | Industry and competitive analysis | `five-forces-analysis` | `lab-FC4-L02-1`: a Herfindahl-Hirschman index on SIMULATED firm shares, exact in `Fraction`; the index as a derived measure, not a finding about any industry | 6 | Builder A |
| L03 | The dividend discount model | `dividend-discount-model` | `lab-FC4-L03-1`: the finite-horizon DDM as the sum of discounted dividends plus a terminal value, checked against the backward recursion, exact; SIMULATED dividend path | 6 | Builder A |
| L04 | The Gordon growth model and the spread r − g | `gordon-growth-model` | `lab-FC4-L04-1` (**the curriculum lab**, `yaml:490`): the value \(D_1/(r-g)\) as the spread shrinks, exact table; no data | 6 | Builder B |
| L05 | Free cash flow to equity | `free-cash-flow-to-equity` | `lab-FC4-L05-1`: the FCFE identity from earnings, depreciation, capital expenditure, working capital and net borrowing on a SIMULATED path; equity value at the cost of equity | 6 | Builder B |
| L06 | Clean surplus | `clean-surplus-relation` | `lab-FC4-L06-1`: the book-value roll \(B_t = B_{t-1} + NI_t - D_t\) on the L05 path, exact; the cumulative identity checked | 6 | Builder B |
| L07 | Residual-income valuation | `residual-income-valuation-model` | `lab-FC4-L07-1`: the residual-income value equals the dividend value plus the terminal book value, discounted, identity checked exactly on the L05 and L06 path | 6 | Builder C |
| L08 | Valuation multiples | `valuation-multiple` | `lab-FC4-L08-1`: implied equity value from a price-to-earnings multiple and from an enterprise-value multiple through a stated bridge; exact; illustrative label | 6 | Builder C |
| L09 | Scenario-weighted price target | `scenario-weighted-price-target` | `lab-FC4-L09-1`: a bull, base and bear weighted target in exact `Fraction`s, rounded half-up to whole cents; an exact half-cent tie shown | 6 | Builder D |
| L10 | Sell-side research and analyst forecast bias | `sell-side-research`, `analyst-forecast-bias` | `lab-FC4-L10-1`: a seeded SIMULATED forecast panel with a planted bias; the mean error and its standard error computed with the standard library; the lab shows the arithmetic, not evidence about analysts | 6 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 60/30 | none | none | - | Builder A |
| project | Initiation-of-coverage report (`both`, §5) | none | `lab-FC4-project-1` (rung 1, worked), `lab-FC4-project-2` (rung 2, `class="lab completion"`), `lab-FC4-project-3` (rung 3 check) | 30 | Builder E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` (§5.5) | none | none | - | Builder E |
| cards | `cards.json` from L01 to L10 | none | none | - | Builder F (after A to E) |

Ownership rule: each builder writes only its lesson files and twins. Builder A writes the hub after L01 to L03 exist.
Builder E writes the project, the rubric, the exemplars and the grader, and does not depend on the lessons' prose. Builder E
may reuse the lessons' lab twins only by copying their formulas, never by importing another builder's file.

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses, §4):
- L01 uses M1 concepts only in prose.
- L02 uses E1 `cournot-competition`, `bertrand-competition`, `competitive-equilibrium` (linkable; E1 is built and in the closure).
- L03 uses L01 (`equity-instruments`) and M1 `present-value`, `discount-factor` (linkable).
- L04 uses L03 (`dividend-discount-model`) and M1 `growing-perpetuity` (linkable; M1 is built and in the closure).
- L05 uses AC1 `cash-flow-statement`, `depreciation-and-amortization`, `accrual-accounting` and CF1 `net-working-capital`,
  `depreciation-tax-shield` (linkable; in the closure), and AP2 `capm` for the cost of equity (linkable; in the closure).
- L06 uses L05 (`free-cash-flow-to-equity` is not needed; the page uses the earnings and dividend lines of L05 in prose).
- L07 uses L06 (`clean-surplus-relation`) and L03 (`dividend-discount-model`).
- L08 uses L05 and L07 in prose; the enterprise-to-equity bridge is plain prose (§4 D2).
- L09 uses L03 (`present-value`) and L08 (`valuation-multiple`) and M4 `expectation` (linkable).
- L10 uses L02 (`five-forces-analysis`, for the industry context of coverage), L09 (`scenario-weighted-price-target`),
  and S1 `estimator-bias-variance` (linkable; S1 is in the closure but unbuilt, B6).

Hours check: 10 × 6 = 60 (hub `data-hours-lessons="60"`); project 30 (hub `data-hours-project="30"`); 90 total.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to FC4)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3 to §8, `plans/FINAL-ARCHITECT-RULINGS.md`,
`/Users/billyribeiro/.fanout/fixer-rules.md`, `plans/AC2-build-plan.md`, `plans/FC2-build-plan.md` (the 90-hour sibling),
this file. Study `course/modules/FC/FC2/` for layout, the hub and the grader panel. `course/templates/` holds the four
skeletons (`hub.html`, `lesson.html`, `project.html`, `studio.html`). Imitate structure, not wording.
Citation convention in this file: "FINAL n" is ruling n of `plans/FINAL-ARCHITECT-RULINGS.md`; "fixer-rules.md line n" is line n
of `/Users/billyribeiro/.fanout/fixer-rules.md`.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) and rounded
   only at display. A page that shows a rounded figure states its rounding rule. Per-share values and rates are stated with
   their basis (annual or per period; end-of-period discounting unless stated otherwise).
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only
   what the printed numbers show. Precedent: M1 LESSON_TEXT_DEFECTS ("checked directly" with no lab behind it).
3. **Attribute nothing unread.** Only the registry keys in §7.1 may be cited, at book or paper level, and an attribution
   needs the abstract read (VERIFIER §2.1). No page, table, equation, coefficient or date is typed from memory (fixer-rules.md line 8).
   Precedent: AC2 and AC4 ("never type a page or table from memory").
4. **Scope words need a computation.** "every", "all", "never", "always", "any", "same", "only", "exactly", "drives", "offsets"
   are used only where a derivation, a finite check or a lab computes the claim (fixer-rules.md line 9). Scope of FC4: a single
   company, a single discount rate per valuation, end-of-period cash flows, no taxes beyond those inside the cash flows, no
   options, no buybacks inside the DDM (buybacks belong to CF3, §4 D4), no enterprise-value method beyond the bridge in L08.
5. **Define before use.** The 11 concepts are defined with `<dfn id="def-<id>" data-concept="<id>">` in their assigned lesson,
   and never before it. Terms outside the 11 (for example the payout ratio, sustainable growth, the book value of equity,
   return on equity, enterprise value, the terminal value, the Herfindahl index) are defined in prose at first use with a plain
   `<dfn>` and no `data-concept` (`tools/check_dag.py` skips a `<dfn>` without `data-concept`, `check_dag.py:45-47`).
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation block lists its numbered Assumptions (A1, A2, ...)
   before the statement. Examples the builders must state:
   - the growing-perpetuity value needs \(r > g\) and a fixed growth rate \(g\) forever (Gordon, L04);
   - the DDM with terminal value needs \(r > -1\), \(r > g\) and nonnegative dividends (L03);
   - the clean-surplus identity needs \(B_t = B_{t-1} + NI_t - D_t\) for every year (L06);
   - the scenario target needs probabilities \(p_s \ge 0\) summing to exactly 1 (L09).
7. **Grader rule.** Applies in full (§5.5). A test may demand an exception type only for a condition the page names. A
   correct implementation that raises a TypeError on a bad type passes unless the page says ValueError (fixer-rules.md line 19).
8. **Money.** The price target is an integer number of cents. Its arithmetic uses `Fraction` and rounds once, half up, to the
   nearest cent, with the rule stated on the page, in the spec and in the module docstring (the rule the FC2 unit uses:
   `plans/FC2-build-plan.md` §4.2). Per-share values are exact `Fraction`s, shown with a stated number of decimals. No float
   appears in any graded money output.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own
   container; the quiz options use `fieldset` with `min-inline-size:0`; `$` inside math is escaped as `\$` (fixer-rules.md line 14).
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":`
    guard. `run_labs.py` runs each twin as `python -I -W error <twin>` with no network (`tools/run_labs.py` lines 51-60; the M1
    twin `tests/labs/M1/lab-M1-L04-1.py` is the model). Standard library only (`fractions`, `math`, `statistics`,
    `random.Random(seed)`).
11. **Rates and yields are basis-explicit.** Any rate is stated with its unit (decimal per year), its compounding (discrete,
    end-of-period) and its source (the stated constant of the lab, or SIMULATED).
12. **Lab mutants are not required.** Labs are demonstrations; mutation testing applies to graders only (fixer-rules.md line 18; FINAL 9).

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. A B- or C-graded claim
  names its published counter-evidence (BUILDER_RULES §2.5). **The registry holds no record that this plan has checked for
  an analyst-recommendation effect size, a sell-side bias estimate, or a five-forces validity study.** Such claims are either
  derivations (grade T, conditional on the stated model), or graded D as practitioner claims flagged "It is widely claimed",
  or go to REFERENCE_REQUESTS (§7.2) with the counter-evidence lead.
- Concepts: §1 table for the 11 registered concepts. A `<dfn>` with `data-concept` only for those 11. A link `<a class="concept">`
  only for a concept whose owner is in the closure {AC1, AC2, AP2, CF1, CS1, E1, E3, M1, M2, M3, M4, M7, P0.1, S0, S1, S2} (§4).
- Prerequisite links: `href="../../../concepts.html#<id>"` for prerequisite concepts; `href="Lnn.html#def-<id>"` for earlier FC4
  lessons. A lesson never links a concept defined in a later lesson. There is no link to a prerequisite module's hub page,
  because the hubs of AP2, AC2 and CF1 are not all built with the same paths (check before linking; the builder confirms
  `course/modules/AC/AC2/index.html` exists, which it does).
- Labs: code lives once in `tests/labs/FC4/lab-FC4-Lnn-1.py` and `lab-FC4-project-1..3.py`. The page carries `@@LAB:<file>@@`
  and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-FC4-<page>-<n>`.
  Seeded RNG only (`random.Random(seed)`); no network; under 10 s in Pyodide; no warnings (`-W error`).
- SIMULATED label: on every lab, figure or grader instance that uses generated data (L01, L02, L03, L05, L06, L07, L09 (only if
  generated), L10, the project's worked example, the autograder's instances). The closed-form lab L04 is not labelled SIMULATED.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references
  in code comments (precedent: AC2 and M1).
- Banned strings (`tools/check_pages.py:58-73` `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the scope",
  "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
  "obviously", "clearly", and any ellipsis `...` (the check applies outside code; avoid the character everywhere).
- Percent changes state the base and the direction (CF1 L07 Misconception 2 precedent). Growth rates state the convention.
- A finite enumeration (a list of cases, a grid of spreads) is grade C with its basis named, not grade T (M1 L06 precedent).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration (CF1 KNOWN 3 precedent).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10 output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols that FC4 must not give a different meaning (`notation/notation.json`, `symbols` array and `macros` object):

| Registered symbol | Registered meaning (locator) | FC4 conflict and rule |
|---|---|---|
| `T` | number of return observations in a sample (`notation.json:112`, module S1) | **Conflict.** A time horizon is written `N`. Never bare `T` for time or for a terminal date. |
| `R_f` | gross riskless return, reciprocal of the price of a sure payoff of 1 (`notation.json:142`, AP1) | **Conflict risk.** FC4 discounts at net rates. The net riskless rate is written `r_f` (lowercase, stated as net), and the registered `R_f` is never reused for a net rate. Open question Q11. |
| `\E` (macro, `notation.json:5`) | expectation operator | Use the macro for the expectation of a random quantity (the scenario-weighted value in L09, the expectation in L10). Do not write plain `E` for expectation. |
| `\R` (macro, `notation.json:25`) | real numbers | Standard. |
| `R^\ast`, `R^{e\ast}`, `\mathbb{Q}` (AP1); `\Phi`, `\gamma_3`, `\gamma_4` (M4) | as registered | Not used. |

Local symbols (allowed; `notation.json` `about`: letters conventionally local are defined per lesson): `D_t` dividend, `NI_t`
net income, `B_t` book value of equity at the end of year t, `FCFE_t` free cash flow to equity, `k_e` cost of equity,
`r` discount rate per period in the valuation models, `g` growth rate, `N` explicit horizon, `shares` share count, `p_s` and
`v_s` the probability and the value in cents of scenario s, `b` the retention ratio in L04, `ROE` return on equity. Plain
`E` is avoided for earnings to prevent confusion with the expectation macro. Each symbol is defined on the lesson where it
first appears and never redefined.

NOTATION_REQUESTS: none. The plan uses only local symbols and the registered macros `\E` and `\R`.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the BUILDER_RULES §4.2 structure. Mandatory content, by lesson. Grades are the planner's
proposal; the verifier re-grades (BUILDER_RULES §2.2).

- **L01 `equity-instruments`.** Common and preferred equity as claims on the residual after senior claims. Definitions (T by
  definition). The residual-claim payoff \(\max(V - S, 0)\) with \(S\) the senior claims, under the stated payoff rule (T).
  Limits: limited liability, no options, no taxes. Lab L01 (SIMULATED). Where the canon breaks: preferred dividends in arrears,
  a convertible claim (named only; not derived). Misconceptions: at least three, each with its evidence (the lab or the derivation).
- **L02 `five-forces-analysis`.** The concept as a structured checklist of five forces (entry, substitutes, buyers, suppliers,
  rivalry) whose names the page states as the framework's definition. Attribution: none, until the Porter record is admitted
  (B3; §7.2). Competition economics from E1 (Cournot and Bertrand, linkable). The Herfindahl-Hirschman index is a derived
  measure: \(\mathrm{HHI} = \sum_i s_i^2\) on shares \(s_i\) summing to 1, exact (T as a definition; the lab computes it). No empirical
  claim about industry structure and returns (grade C at most, with the counter-evidence named, or removed). Where the canon
  breaks: a static snapshot of one industry; shares measured on one market definition.
- **L03 `dividend-discount-model`.** \(V_0 = \sum_{t=1}^{N} D_t (1+r)^{-t} + TV_N (1+r)^{-N}\) with the terminal value defined
  as a stated value at N (plain prose, §4 D2). Assumptions A1 to A4: \(r > -1\), dividends nonnegative, end-of-period timing,
  total payout equals dividends (no buybacks; §4 D4). The finite identity and the backward recursion \(V_{t-1} = (D_t + V_t)(1+r)^{-1}\)
  agree (T, a derivation). Lab L03: exact check of both forms on a SIMULATED dividend path. Where the canon breaks: payout policy
  is assumed, not modelled; the discount rate is an input here.
- **L04 `gordon-growth-model`.** The growing perpetuity \(D_1/(r-g)\) derived from the M1 growing perpetuity (T; Assumptions:
  \(r > g\), constant \(g\), constant \(r\), dividends equal to a stated \(D_1\)). Sustainable growth as \(g = b \cdot ROE\) under
  the stated identities (plain dfn for the terms; T as an identity under its assumptions). The curriculum lab (`yaml:490`):
  \(D_1/(r-g)\) on a grid of spreads, printed exactly; the sensitivity (value rises without bound as the spread falls to zero)
  is a T derivation, and the lab only tabulates it. Attribution: §0.3 B5. Where the canon breaks: constant growth forever; a
  constant rate; no change in payout.
- **L05 `free-cash-flow-to-equity`.** \(\mathrm{FCFE}_t = NI_t + \mathrm{D\&A}_t - \mathrm{capex}_t - \Delta\mathrm{NWC}_t + \mathrm{net\ borrowing}_t\)
  (an identity from the cash-flow statement; T as a definition of the stated items). Equity value as the present value at the
  cost of equity \(k_e\) (CAPM from AP2, linkable). Theorem (T): if every year's FCFE is paid out as dividends, the FCFE model and
  the DDM are the same calculation. Lab L05 (SIMULATED). Where the canon breaks: negative FCFE, leverage targets, the
  enterprise-value alternative (plain prose, §4 D2).
- **L06 `clean-surplus-relation`.** \(B_t = B_{t-1} + NI_t - D_t\) (the stated accounting identity; T under Assumption: all
  changes in book value go through earnings and dividends). The cumulative form \(B_N = B_0 + \sum_{t\le N} NI_t - \sum_{t \le N} D_t\)
  (T by induction). Lab L06 (SIMULATED path from L05). Where the canon breaks: other comprehensive income, share issues and
  repurchases violate the relation (named only; the page states the assumption that rules them out).
- **L07 `residual-income-valuation-model`.** \(RI_t = NI_t - r B_{t-1}\). \(V_0 = B_0 + \sum_{t=1}^{N} RI_t (1+r)^{-t}\) under the
  stated horizon and no terminal residual income beyond N. Theorem (T): under the L06 clean-surplus assumption, this equals the
  DDM value with the terminal value \(B_N (1+r)^{-N}\), so the two valuations agree exactly (the derivation is the proof; the
  lab checks it on the L05 and L06 path). Attribution to AC4 is not made (§4 D1). Where the canon breaks: the horizon choice
  and the terminal book value.
- **L08 `valuation-multiple`.** Price-to-earnings and enterprise-value-to-EBITDA multiples as implied values: implied price
  \(= \text{multiple} \times \text{metric}\) per share, and the bridge from enterprise value to equity value by net debt
  (plain prose for the bridge, §4 D2). The lab computes the implied values exactly on an illustrative company (labelled
  SIMULATED). Multiples are described as a relative method; no empirical claim about multiples' accuracy (grade D as practice,
  flagged) unless a registry record is admitted. Where the canon breaks: the choice of peer set, the cyclical earnings base.
- **L09 `scenario-weighted-price-target`.** Target \(= \sum_s p_s v_s\) with \(p_s \ge 0\) and \(\sum_s p_s = 1\) exactly. Rounding
  rule: half up to whole cents, exact in `Fraction` (floor of the exact value plus one half). Theorem (T): the target is
  linear in the scenario values. Lab L09 (exact; the half-cent tie is shown). Uses `\E` for the expectation in prose. Where the
  canon breaks: scenarios are the analyst's choice; probabilities are not estimated from data.
- **L10 `sell-side-research` and `analyst-forecast-bias`.** Sell-side versus buy-side incentives, described as a model with
  its assumptions, not as evidence. The forecast-bias definition: mean signed forecast error. The two registry keys
  `hong2003analyzing` (forecasts and career concerns) and `womack1996brokerage` (recommendations and investment value) are cited
  only after the abstract is read (VERIFIER §2.1), and each claim takes the grade its abstract supports (B at most unless the
  replication status is established). Counter-evidence for every B or C claim is required (BUILDER_RULES §2.5; §7.2 request).
  Lab L10: a seeded SIMULATED panel with a planted bias; the mean error and its standard error with `statistics`; the page says
  the lab shows what the estimator computes, not what analysts do. Market efficiency is plain prose (§4 D5).

Lesson-level constraints:
- Each lesson's "Where the canon breaks" section names at least one model limit and what changes without it.
- No lesson uses an E6 or E8 term (New Keynesian, determinacy, open economy) as a concept. No lesson uses a CF4 or CF2 concept as
  a link (§4).
- Each lesson has at least one lab (BUILDER_RULES §3.4; the curriculum names one lab, `yaml:490`, and the plan adds one per lesson,
  as E5 did).

---

## 4. DAG problems (concepts that natural FC4 content would use outside the closure)

Prerequisite closure of FC4 (computed, §0.1): **{AC1, AC2, AP2, CF1, CS1, E1, E3, M1, M2, M3, M4, M7, P0.1, S0, S1, S2}**.
Owners below are from `curriculum.json` `concepts` (planner check). Positions are topological positions (`curriculum.json:1036`).

| Ref | Concept (owner, position) | Where natural FC4 content would use it | Resolution in this plan |
|---|---|---|---|
| D1 | `residual-income` (AC4, position 10, built; `yaml:635`) | L07 (residual income is the AC4 measure) | **DAG question Q5.** Recommended: add AC4 to FC4's prerequisites (`yaml:465`; a curriculum change; AC4 precedes FC4, so no reordering). Default if not added: plain prose, no link, no `<dfn>` for the AC4 term; L07 defines the valuation formula itself. |
| D2 | `terminal-value`, `enterprise-to-equity-bridge`, `free-cash-flow-to-firm`, `fcff-dcf-valuation` (CF4, position 59, after FC4) | L03 terminal value; L05 contrast with FCFF; L08 bridge | Plain prose, no link. CF4 cannot be a prerequisite without reordering. |
| D3 | `wacc` (CF2, position 44, unbuilt; addable without reordering) | L05 choice of discount rate | **DAG question Q6.** Recommended: no change. FCFE is discounted at the cost of equity \(k_e\) from AP2's CAPM, which is in the closure. WACC is named in plain prose as the enterprise-level rate. |
| D4 | `dividends-vs-buybacks`, `payout-irrelevance` (CF3, position 58, after FC4) | L03 assumption that total payout equals dividends | Plain prose; the assumption is stated as Assumption A4. No link. |
| D5 | `efficient-markets-hypothesis`, `anomaly` (FC3, position 42, unbuilt) | L10 (whether analysts' recommendations carry information) | Plain prose, no link. Recommended: no change to the curriculum. FC3 is a sibling primer, not a prerequisite (`yaml:432-460`). |
| D6 | `information-content-of-earnings`, `earnings-surprise`, `post-earnings-announcement-drift` (AC3, position 57, after FC4) | L10 if forecast revisions are discussed | Plain prose, no link; omitted unless the lesson needs them. |
| D7 | `model-sensitivity-table` (CF7, position 77) | L09 scenario tables | Plain prose ("a sensitivity table"), no link. |
| D8 | `cape-ratio` (AP5, position 81); `scenario-pnl` (GM4) | none planned | Not used. |
| D9 | sustainable growth, payout ratio, return on equity, book value of equity, the cost of equity as a term | L04, L05, L06 | No concept id exists for these terms (planner grep of `concepts`). Plain `<dfn>` without `data-concept`, defined at first use. |

Each row has a resolution, so no DAG_DEFECT blocks the drafting. Rows D1 and D3 need the architect's confirmation (§12 Q5, Q6).
`check_dag.py` checks linked uses only (`tools/check_dag.py:60-69`); an unlinked use of D1 to D7 passes the tool, so the
verifier reads every lesson for these names (VERIFIER §2.9).

Missing prerequisite as a DAG question: **AC4 for D1** (Q5). No other missing prerequisite is needed for the content in §3.

---

## 5. Project (`project.html`, Builder E): `both` grading, ladder, spec, time budget, rubric, grader

### 5.1 Ladder (BLUEPRINT §5.1; `check_projects.py` requires the order, `tools/check_projects.py:33` and lines 84-89)

1. **Rung 1, worked example** (`lab-FC4-project-1`, SIMULATED). One fully solved, annotated valuation of a generated company
   (five years of dividends, earnings, book value, FCFE, shares and three scenarios): the Gordon value of the terminal stream,
   the DDM value, the residual-income value, the FCFE value per share, and the scenario target in whole cents. Each step has a
   "why" annotation. Full length (tier U; BLUEPRINT §4 minimum applies from tier M; FC2 precedent).
2. **Rung 2, completion** (`lab-FC4-project-2`, `class="lab completion"`, SIMULATED). The same valuation with three lines
   replaced by `___`: the terminal-value line, the FCFE line and the scenario-weight line. Graded instantly. Its twin is the
   completed solution; every page line equals the twin line or contains a blank (`tools/run_labs.py` completion rule, as in
   FC2 and E1).
3. **Rung 3, independent project** (graded by the autograder and by the rubric):
   (a) the autograded module `valuation.py` to the §5.5 interface; and
   (b) the initiation report, `initiation.md` (memo) plus the model file the student chooses, rubric-graded (§5.4).
   `lab-FC4-project-3` is the rung-3 check: a self-contained twin that prints the expected seed-0 table for the five functions,
   computed from its own formulas (§12 Q12: it does not import the grader).
4. **Rung 4, stretch** (optional, not graded): a second company's valuation with the same rules, or a sensitivity grid over the
   spread \(r-g\) with a stated hypothesis before running it.

### 5.2 Spec (`dl.spec`; `tools/check_projects.py` requires the terms context, inputs, required outputs, constraints, grading;
`check_projects.py:34` and lines 92-104)

- **Context.** A research associate must initiate coverage of one listed public company: an industry analysis, a model, a
  valuation by three methods, a scenario price target in whole cents, the key risks, and the triggers that would change the call.
  The valuation must be reproducible from the functions the student writes.
- **Inputs.** (1) The seeded SIMULATED company of the autograder (`make_instance`), used for all graded numbers. (2) The
  student's real public company, supplied as a bring-your-own-data CSV with a documented schema: fiscal year, net income,
  dividends, book equity, depreciation and amortization, capital expenditure, change in net working capital, net borrowing,
  shares outstanding; money in integer cents; the file never leaves the browser (BUILDER_RULES §6.6). The page validates the
  file and names every missing or misaligned column. (3) The student's own sources, listed by registry key only where a
  registry key exists; any other source is named as the student's own. Optional: the student's AC2 Atlas A15 output, if they
  completed AC2's project (`yaml:578-585`).
- **Required outputs.** `valuation.py` with the five functions of §5.5; `initiation.md` (the memo, stated length 1,500 to 2,500 words,
  §12 Q2); the model file in a format the student chooses. The memo states each valuation's inputs, each rule's output, the
  rounding rule and the cents result.
- **Constraints.** Integer cents for money. Each money output is computed from exact `Fraction`s and rounded once, half up, to the
  nearest cent (rule stated here, in the spec and in the module docstring). Standard library only for `valuation.py`. The same code
  runs in Pyodide and under pytest. Invalid input raises the exception types named in §5.5 and nothing else. Every number in the
  memo cites the input and the rule that produced it. The real company's numbers are the student's responsibility; the page does
  not embed them.
- **Grading.** The project is graded by an autograder (`grader/test_project.py`, dual mode: Pyodide and local pytest) and by a
  rubric (`initiation.md`, §5.4). The spec must name both the autograder and the rubric; `tools/check_projects.py:38-49` requires
  the words "autograd" and "rubric" in this entry.
- **Reading list.** `ol.reading-list` with `data-cite`: `gordon1956capital`, `hong2003analyzing`, `womack1996brokerage`,
  `bodie2023investments` (§7.1 for the status of each). Nothing else.

**Honest-pending note (on the project page):** "The brief asks for a real public company. This project embeds no company
financial statements: no redistributable source for them is in the program's data registry yet. The autograder uses generated
companies labelled SIMULATED. You supply your company's statements from its own filings."

### 5.3 Time budget (`<table id="hours">`, sums to 30 h; every row needs a one-line rationale; `check_projects.py:107-127`)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One solved SIMULATED valuation read line by line with its "why" notes |
| Rung 2, completion problem | 2 | Fill three blanks (terminal value, FCFE, scenario weights), then run the instant check |
| Autograder: `valuation.py` (five functions) and local tests | 6 | Five functions, each with one condition to honour; the student writes and runs the suite locally |
| Company data intake: CSV schema, validation, the basis convention | 3 | Map the company's statements to the schema, fix the validation errors, state the basis (annual, end of period) |
| Industry and competitive analysis with sources | 3 | Five forces applied to named facts; each claim graded and sourced, or stated as the student's own assumption |
| Model and three scenarios with probabilities | 5 | Forecast drivers, the clean-surplus check, the three scenarios, the probabilities summing to exactly 1 |
| Initiation memo: valuation, price target, key risks, call triggers | 6 | 1,500 to 2,500 words; every number cited to its input and rule; triggers stated with thresholds |
| Self-assessment against exemplars | 3 | Score the memo with the rubric, then compare with exemplar-a and exemplar-b |
| **Total** | **30** | Equals `data-hours-project` on the hub; within 30 % of the verifier's estimate of the components (VERIFIER §2.6) |

### 5.4 Rubric (`table.rubric#rubric`, `check_projects.py:58-73`)

Six criteria (4 to 7 allowed). Each criterion is one table row: the criterion name in a `th`, and exactly four `td` cells for
levels 4 down to 1 (the tool counts `td` cells). Every descriptor is observable.

| Criterion | Level 4 (observable) | Level 1 (observable) | Levels 3 and 2 |
|---|---|---|---|
| C1 Industry and competitive analysis | Names each of the five forces, states for each a fact from a cited source or a labelled assumption, and says which force dominates and why | "Describes the industry" | Level 3 misses one of the level-4 elements; level 2 misses two |
| C2 Model integrity | Every forecast line has a stated driver; the clean-surplus identity holds in every year of the model; \(r > -1\) and \(r > g\) are checked and stated | "The model looks reasonable" | As above |
| C3 Valuation and reconciliation | Values the company by the DDM or FCFE model and by residual income; states the difference between the two equity values and explains it | "Uses a valuation method" | As above |
| C4 Scenarios and price target | Three scenarios; probabilities summing to exactly 1; each scenario value in cents; the target by the scenario rule; the rounding rule stated | "Gives a price target" | As above |
| C5 Evidence and grades | Every claim has a grade and a registry key or a derivation; every B or C claim names counter-evidence; an analyst-bias claim names the key read and the scope of its abstract | "Cites some sources" | As above |
| C6 Key risks and call triggers | At least three risks, each with an observable trigger and the valuation change the trigger causes | "Lists risks" | As above |

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, fully written memos on the SIMULATED company
of the autograder (a fictional name, for example "Simco Industrial"), annotated with the descriptors each passage meets or misses.
Self-assessment form (`section.rubric-self`, `data-rubric="rubric"`, `data-exemplars="exemplar-a exemplar-b"`, as in E5, M1 and FC2).
The page shows where the student's scores diverge from the exemplar scores. Calibration: a dedicated blind scorer, not the
verifier, scores both exemplars from a stripping script's output (FINAL 15 and 23); the scores must fall within one level per
criterion. Adversarial question bank: none (§12 Q13).

### 5.5 Autograder design (`grader/`, dual mode)

**Panel.** `section.grader-panel` on `project.html` with `data-unit="FC4"`, `data-grader="grader"`, `data-suite="test_project.py"`,
`data-solution="valuation.py"`, `data-starter="starter.py"`, `data-support="instance.py"`
(required attributes: `tools/check_projects.py:128` and `tools/run_graders.py:43-48`). The reference is the file `reference.py`,
copied as the solution (`tools/run_graders.py:51-62`). Seeds reach the suite through the environment variable `QF_SEED`
(`tools/run_graders.py:73`). The suite runs with `-q -p no:cacheprovider --assert=plain -W error` (`run_graders.py:39`) and must
finish in 60 s locally (`run_graders.py:40`) and under 5 s per test in Pyodide (VERIFIER §2.6).

**Interface (planner proposal; the architect freezes it, §12 Q13).** All money is an integer number of cents; all rates and
per-share values are exact `Fraction`s.

```
gordon_value(d1: Fraction, r: Fraction, g: Fraction) -> Fraction
ddm_value(dividends: Sequence[Fraction], r: Fraction, g: Fraction) -> Fraction
fcfe_value_per_share(fcfe: Sequence[Fraction], shares: Fraction, r: Fraction, g: Fraction) -> Fraction
residual_income_value(book_value_0: Fraction, earnings: Sequence[Fraction], dividends: Sequence[Fraction], r: Fraction) -> Fraction
scenario_price_target_cents(scenarios: Sequence[tuple[Fraction, int]]) -> int
```

**Definitions the page states (exact).**
- `gordon_value` is \(D_1/(r-g)\). `ddm_value` is \(\sum_{t=1}^{N} D_t(1+r)^{-t} + \dfrac{D_N(1+g)}{r-g}(1+r)^{-N}\), end-of-period.
- `fcfe_value_per_share` is the same formula applied to FCFE, divided by `shares`.
- `residual_income_value` is \(B_0 + \sum_{t=1}^{N} RI_t (1+r)^{-t}\) with \(B_t = B_{t-1} + NI_t - D_t\) and \(RI_t = NI_t - r B_{t-1}\); no terminal residual income beyond N.
- `scenario_price_target_cents` is \(\lfloor \sum_s p_s v_s + \tfrac12 \rfloor\) in cents, computed exactly.

**Conditions and the exception each names (each is one isolated test, both directions of every inequality).**

| Function | Condition | Exception the page names |
|---|---|---|
| `gordon_value` | \(d_1 < 0\) | ValueError |
| `gordon_value` | \(r \le g\) (boundary: \(r = g\) is an error; \(r = g + \varepsilon\) is accepted) | ValueError |
| `ddm_value` | `dividends` empty | ValueError |
| `ddm_value` | any \(D_t < 0\) (boundary: \(0\) accepted) | ValueError |
| `ddm_value` | \(r \le g\) (boundary as above) | ValueError |
| `ddm_value` | \(r \le -1\) (boundary: \(-1\) error; \(-1 + \varepsilon\) accepted) | ValueError |
| `fcfe_value_per_share` | `fcfe` empty | ValueError |
| `fcfe_value_per_share` | `shares` \(\le 0\) (boundary: 0 error; a tiny positive value accepted) | ValueError |
| `fcfe_value_per_share` | \(r \le g\) or \(r \le -1\) | ValueError |
| `fcfe_value_per_share` | negative FCFE values | **allowed**; no exception (the page states this) |
| `residual_income_value` | `earnings` empty | ValueError |
| `residual_income_value` | `earnings` and `dividends` of different lengths | ValueError |
| `residual_income_value` | \(r \le -1\) (boundary as above) | ValueError |
| `scenario_price_target_cents` | empty sequence | ValueError |
| `scenario_price_target_cents` | any \(p_s < 0\) (boundary: 0 accepted) | ValueError |
| `scenario_price_target_cents` | \(\sum_s p_s \ne 1\) exactly (boundary: a sum of \(1 + 10^{-12}\) is an error) | ValueError |
| `scenario_price_target_cents` | any \(v_s < 0\) (boundary: 0 accepted) | ValueError |

Any other bad input (for example a float passed where a `Fraction` is expected) is not named on the page, so the suite must not
demand a particular exception for it (fixer-rules.md line 19).

**Instances (`grader/instance.py`).** `make_instance(seed: int) -> dict[str, object]` (the exact signature string is checked by
`tools/check_projects.py`; the instance is deterministic and differs across seeds). It returns a SIMULATED company:
- \(r\) from {0.080, 0.085, 0.090, 0.095, 0.100, 0.105, 0.110, 0.115, 0.120} as exact decimals, \(g\) from {0.020, 0.025, 0.030, 0.035, 0.040} with \(r - g \ge 0.03\);
- five dividends and five earnings, nonnegative dividends, earnings that may be negative in some seeds; five FCFE values that
  may be negative in some seeds; a book value \(B_0\); shares as an integer count of at least 1,000;
- three scenarios with probabilities summing to exactly 1 (for example 1/4, 1/2, 1/4 or a seed-dependent split with denominator 20)
  and integer-cent values.
Every instance is valid. Across seeds 0 to 19 the answers differ materially (`tools/run_graders.py:97` checks the first 20 seeds for
identical instances; the verifier checks 20 sampled seeds, VERIFIER §2.6 item 2).

**Tests (`grader/test_project.py`).** Each test computes its expected value from an independent direct computation in the test
(a loop over the explicit sum, a direct evaluation of the formula), never from a literal. Helpers set `__tracebackhide__ = True`,
and failure messages name the violated property and the concept, never the expected answer (fixer-rules.md line 19). Named tests:

- T-GORDON-VALUE (instance parameters; exact equality with the direct formula).
- T-GORDON-RG-EQUAL (\(r = g\) raises ValueError); T-GORDON-RG-BELOW (\(r < g\) raises ValueError); T-GORDON-D1-NEG (negative \(d_1\) raises ValueError); T-GORDON-D1-ZERO (\(d_1 = 0\) returns 0).
- T-DDM-N1 (one dividend, N = 1, against the direct formula); T-DDM-TIMING (N = 2 and N = 3 checks of the discount exponents, distinguishes a one-period timing error); T-DDM-TERMINAL (terminal uses \(D_N(1+g)\), N = 1 case); T-DDM-TERMINAL-DISCOUNT (N = 2: the terminal value is discounted by \((1+r)^N\), not \((1+r)^{N-1}\)).
- T-DDM-EMPTY, T-DDM-NEG-DIV, T-DDM-ZERO-DIV-ACCEPTED, T-DDM-RG-EQUAL, T-DDM-R-MINUS-ONE, T-DDM-R-MINUS-ONE-PLUS.
- T-FCFE-PER-SHARE (instance; exact); T-FCFE-TERMINAL (N = 1: the terminal uses \(\mathrm{FCFE}_N(1+g)\) once); T-FCFE-NEG-ALLOWED (a negative FCFE stream returns a value and does not raise); T-FCFE-SHARES-ZERO (ValueError); T-FCFE-SHARES-TINY (a positive tiny share count is accepted); T-FCFE-EMPTY; T-FCFE-RG and T-FCFE-R-MINUS-ONE (both ValueError).
- T-RI-CLEAN-SURPLUS-IDENTITY (the residual-income value equals \(\sum D_t(1+r)^{-t} + B_N(1+r)^{-N}\) for an instance where dividends differ from earnings; kills a book roll that ignores dividends); T-RI-CHARGE (an instance where \(B_t \ne B_{t-1}\), so the charge on the beginning book is tested exactly); T-RI-LENGTH (ValueError); T-RI-EMPTY (ValueError); T-RI-R-MINUS-ONE (ValueError at \(-1\), accepted at \(-1 + \varepsilon\)).
- T-PRICE-TIE (values 2 and 3 cents with probabilities 1/2 and 1/2 give 3, the half-up result; kills Python's `round`, which gives 2); T-PRICE-HALF-UP-NONTIE (for a non-tie the nearest cent); T-PRICE-SUM-EXACT (\(\sum p_s = 1 + 10^{-12}\) raises ValueError; kills a float tolerance); T-PRICE-SUM-SHORT (a sum below 1 raises ValueError); T-PRICE-NEG-PROB (ValueError), T-PRICE-ZERO-PROB-ACCEPTED (a zero probability is accepted), T-PRICE-EMPTY (ValueError), T-PRICE-NEG-VALUE (ValueError), T-PRICE-ZERO-VALUE-ACCEPTED.
- T-INSTANCE-VALID (for seeds in `QF_SEED`: \(r > g + 0.03\), nonnegative dividends, probabilities summing to exactly 1, shares at least 1,000). T-SEED-HARDCODE-GUARD (the target for seed 0 is recomputed independently for the instance of the current seed, so a literal answer fails on another seed).

**Collect-only count.** The project page quotes the number of collected tests from `pytest --collect-only -q` in the grader
directory, copied from the actual run (fixer-rules.md line 19). The count is not planned here.

### 5.6 Ten student-error mutants (`ledgers/FC4/mutants/`; single-change copies of the reference)

`tools/mutate_graders.py:42` requires at least three mutants, and reads the first docstring line as the error description
(`mutate_graders.py:47`). Each mutant differs from the reference only where a stated condition is violated (fixer-rules.md line 18;
FINAL 9); none is planned as an equivalent mutant.

| File | First docstring line (student error) | Killed by |
|---|---|---|
| `m01_gordon_sign.py` | gordon_value uses r + g in the denominator (sign error on the growth term) | T-GORDON-VALUE |
| `m02_gordon_boundary.py` | gordon_value accepts r equal to g and divides by zero instead of raising ValueError | T-GORDON-RG-EQUAL |
| `m03_ddm_timing.py` | ddm_value discounts dividend t by (1+r) to the power t-1 (beginning-of-year timing) | T-DDM-TIMING |
| `m04_ddm_no_growth_step.py` | ddm_value sets the terminal value to D_N over (r-g), dropping the one-period growth step | T-DDM-TERMINAL |
| `m05_ddm_terminal_discount.py` | ddm_value discounts the terminal value by (1+r) to the power N-1 | T-DDM-TERMINAL-DISCOUNT |
| `m06_fcfe_double_growth.py` | fcfe_value_per_share applies the growth factor twice to the terminal FCFE | T-FCFE-TERMINAL |
| `m07_ri_ending_book.py` | residual_income_value charges the cost of equity on ending book value B_t instead of B_(t-1) | T-RI-CHARGE |
| `m08_ri_no_dividend_roll.py` | residual_income_value rolls book value forward without deducting dividends (B_t = B_(t-1) + NI_t) | T-RI-CLEAN-SURPLUS-IDENTITY |
| `m09_round_ties_even.py` | scenario_price_target_cents rounds with Python round(), which sends an exact half-cent tie to the even cent | T-PRICE-TIE |
| `m10_sum_tolerance.py` | scenario_price_target_cents accepts probabilities whose sum is within 1e-9 of 1 instead of exactly 1 | T-PRICE-SUM-EXACT |

A hard-coded answer for seed 0 is the verifier's to add (VERIFIER §2.6 item 3 lists it as an example). It is not counted in
the ten. Any survivor is a FAIL (VERIFIER §2.6 item 3). A mutant that differs only where the page states nothing goes to
`ledgers/FC4/equivalent/` with a README proof (FINAL 9), never to `mutants/`.

### 5.7 Five alternative correct implementations (`ledgers/FC4/alternatives/alt_1.py` to `alt_5.py`)

Each must pass seeds 0 to 49 under the run_graders flags (FINAL 10), and each uses a different style. Each is exact (Fraction
arithmetic, integer-cent rounding by the half-up rule). A float-based alternative that is wrong on a stated exact rule is a
mutant, not an alternative (FINAL 10).

| File | Style |
|---|---|
| `alt_1.py` | Procedural loops over the explicit horizon, with a local discount-factor variable |
| `alt_2.py` | Functional: `itertools.accumulate` for the discount factors, `sum` over `zip` |
| `alt_3.py` | Object style: a small `Valuation` class with methods per model, the five functions as thin wrappers |
| `alt_4.py` | Backward recursion for the DDM and FCFE values, \(V_{t-1} = (D_t + V_t)/(1+r)\), with the terminal at N; residual income by a dictionary-keyed book roll |
| `alt_5.py` | Generator and `math.floor` style: half-up rounding as `floor(x + 1/2)` on the exact value, and a generator for the discounted sum |

---

## 6. Real-data policy (B2 applies)

- **Embedded (redistributable, grant quoted):** `fx_daily`, `fx_monthly`, `ust_daily` (`tools/data_sources.yaml:19`, `:53`, `:91`;
  `course/assets/data/market/MANIFEST.json`). None is a company-level series. FC4 uses none of them by default. If L01 or L08 needs a
  riskless-rate example, the builder uses the lab's stated constant, labelled SIMULATED, not `ust_daily`.
- **Not embedded, no grant found:** company financial statements (income, balance sheet, cash flow, shares) and any
  issuer's filings. No such entry is in `tools/data_sources.yaml` (grep, planner), and the French library and Open Source Asset
  Pricing are the only rejected entries (`tools/data_sources.yaml:120`, `:132`). **Not embedded.**
- **Honest-pending note.** On the project page (§5.2) and on L08 and L10: "This program embeds no company financial statements.
  The labs and the autograder use generated companies labelled SIMULATED. The real company is supplied by the student."
- **Bring-your-own-data.** The project's CSV schema (§5.2) is documented on the page and validated in the browser; the file
  never leaves the browser (BUILDER_RULES §6.6, last bullet). Only the schema and the validator are part of the project; no data
  is embedded.
- **DATA_REQUESTS** (for the architect; the planner does not name a licence or a URL from memory): SEC EDGAR company-facts data
  (the source AC2's plan names; `plans/AC2-build-plan.md`, "Real data" bullet). Required fields: source URL, the quoted reuse
  sentence and the page that states it, a series list (income, balance sheet, cash flow, shares), the transform (standardized
  annual statements; AC2's A15 contract). Until a licence is quoted and admitted under `tools/data_sources.yaml`, the data stays
  bring-your-own.
- No `data-files` attribute on any FC4 lab until a dataset is embedded. No MANIFEST entry is added by builders.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

Each key was grepped in `references/references.json` by the planner, and its `key` field matches exactly.

| Key | Record (as read) | Locator | Status | Use in FC4 |
|---|---|---|---|---|
| `gordon1956capital` | Gordon & Shapiro, "Capital Equipment Analysis: The Required Rate of Profit", Management Science, volume 3, issue 1, pages 102-110, 1956, DOI 10.1287/mnsc.3.1.102 | `references/references.json:10704` | verified, `used_by: ["FC4"]`; source string matches `yaml:484` | L04 attribution only after the abstract is read (§0.3 B5). Reading list. |
| `hong2003analyzing` | Hong & Kubik, "Analyzing the Analysts: Career Concerns and Biased Earnings Forecasts", Journal of Finance, volume 58, issue 1, pages 313-351, 2003, DOI 10.1111/1540-6261.00526 | `references/references.json:12727` | verified, `used_by: ["FC4"]`; matches `yaml:488` | L10 forecast bias; abstract to be read before any claim (VERIFIER §2.1). Reading list. |
| `womack1996brokerage` | Womack, "Do Brokerage Analysts' Recommendations Have Investment Value?", Journal of Finance, volume 51, issue 1, pages 137-167, 1996, DOI 10.1111/j.1540-6261.1996.tb05205.x | `references/references.json:23280` | verified, `used_by: ["FC4"]`; matches `yaml:487` | L09 and L10 on recommendations; abstract to be read first. Reading list. |
| `bodie2023investments` | Bodie, Kane & Marcus, "Investments", McGraw-Hill Education, year 2023, ISBN 9781264412662 | `references/references.json:3255`; year note `:3298` | verified, `used_by: ["FC4"]`; year conflict with `yaml:489` (B4) | Book level only; conventions; no edition or year in prose. Reading list. |

Registry keys not planned for FC4: `penman2013financial` (`references/references.json:18944`, used by AC1 and AC2, not an FC4
source string) and `sharpe1964capital` (used by AP2). A key outside this table is not cited without a new plan entry.

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- {doi: null, authors: "Graham and Dodd (lead only; the curriculum string is `yaml:485`)", year: "1934 (curriculum string)", title: "Security Analysis (curriculum string; the book's record is not typed)", venue: "book (curriculum string)", needed_for: "L09 or L10 historical attribution of fundamental analysis, if the architect permits it; not needed for any graded claim", confidence: "The source string exists (`yaml:485`). The registry has no record. The review-queue candidates (`references/review_queue.json:375-`) are not this book and must not be admitted."}
- {doi: null, authors: "Porter (lead only; the curriculum string is `yaml:486`)", year: "1979 (curriculum string)", title: "How Competitive Forces Shape Strategy (curriculum string)", venue: "Harvard Business Review, volume 57, issue 2 (curriculum string; the record is not typed)", needed_for: "L02 attribution of the five-forces framework; without it the page states the framework as a definition with no attribution", confidence: "The source string exists (`yaml:486`). The registry has no record. None of the review-queue candidates (`references/review_queue.json:428-`) is this article, and none may be admitted."}
- {doi: null, authors: "Literature on the value of analysts' recommendations and of analyst forecast accuracy, beyond the two keys in §7.1 (lead only; no author typed)", year: "not typed", title: "published studies that test or contest the two keys' findings", venue: "not typed", needed_for: "L09 and L10 counter-evidence for every B- or C-graded claim (BUILDER_RULES §2.5); without it those claims are removed or graded C", confidence: "The need is certain. No record is identified by this planner."}
- {doi: null, authors: "Literature on the five-forces framework's empirical validity (lead only)", year: "not typed", title: "empirical tests of industry-structure measures and returns", venue: "not typed", needed_for: "L02 two-sided treatment if any empirical sentence is kept (otherwise removed)", confidence: "Optional. No record is identified by this planner."}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4).
Until resolved, the lessons teach the models with derivations and no empirical attribution, and each empirical sentence is
graded C at most with its basis named, or is removed.

### 7.3 Registry flags (for the architect; no edits planned)

- `bodie2023investments`: year conflict (`references.json:3298`, curriculum 2024 vs record 2023), B4.
- `gordon1956capital`: the title does not state the valuation formula; attribution needs the abstract (B5).

---

## 8. Atlas milestone

None for FC4 as planned. The brief names A15 and A16 (`yaml:495`; B1). A15 is AC2's (`curriculum.json:258`; `atlas/A15.contract.md`
exists) and is optional for students who completed AC2. A16 is CF4's (`curriculum.json:264`), is after FC4 in the topological order,
has no contract, and is not used. No contract is drafted here. The project page has no `atlas:` key, so `check_projects.py` skips
the contract check (`tools/check_projects.py:144-146`). The brief's wording is B1.

---

## 9. Cards builder (Builder F, after A to E)

- `course/modules/FC/FC4/cards.json`, ids `FC4-c001` upward (`tools/check_pages.py` `check_cards` checks the id prefix, the lesson
  existence, the grade and the registry keys; `check_pages.py:366-398`), `lesson` in L01 to L10. Every lesson has at least one card
  (`check_pages.py:395-398`).
- One card per definition, theorem statement, key formula, key empirical result and misconception (BUILDER_RULES §7).
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example
  `"basis": "Lab L07, Derivation 2 (exact)"`.
- Cite a registry key only for an empirical or attributed claim (`cite` lists keys from §7.1). `cite` is `[]` where the card is a
  model result.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`.
- Cards and their key-results rows carry the same grade and basis (FINAL 13).

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit FC4            # --page L04 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit FC4
.venv/bin/python tools/check_projects.py --unit FC4
.venv/bin/python tools/run_labs.py --unit FC4               # --page L04 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/FC/FC4/L01.html                          # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/FC/FC4/L04.html --refresh lab-FC4-L04-1  # after editing a twin
.venv/bin/python tools/run_graders.py --unit FC4 --seeds 0-49   # reference on 50 seeds, starter must fail, mypy strict
.venv/bin/python tools/mutate_graders.py --unit FC4 --seeds 0-9 # every mutant must be killed
.venv/bin/ruff check tests/labs/FC4 course/modules/FC/FC4/grader && .venv/bin/ruff format --check tests/labs/FC4 course/modules/FC/FC4/grader
.venv/bin/mypy --no-incremental tests/labs/FC4              # strict, repository configuration
```

Verifier only, on a quiet machine (not run by builders; timing-sensitive): `.venv/bin/python tools/page_smoke.py --unit FC4`
(alone), `.venv/bin/python tools/verify_refs.py --unit FC4` (the unit ledger's run, VERIFIER §2.1). The five alternatives are run
by the verifier in scratch workspaces with the run_graders flags (`tools/run_graders.py:39`) for seeds 0 to 49, the same way
`run_suite` does (`tools/run_graders.py:65-76`). `tools/fetch_data.py --check` is not needed (no dataset is added).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`,
and the full gate in CLAUDE.md. Gate invocations are run once before the push, not after each edit.

Flag checks: `tools/check_pages.py`, `tools/check_dag.py` and `tools/check_projects.py` accept `--unit` (`check_projects.py` `main`).
`tools/run_labs.py` accepts `--unit` and `--page`; `tools/embed_labs.py` accepts pages and `--refresh [LAB_ID ...]`. The planner
did not execute the builder commands; the planner ran only the coursekit closure, the concept-owner and the topological-position
functions, and read the tool sources listed in §0 and §11.

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone for FC4 in the plan.** The brief's A16 is outside the closure and has no contract (B1). `check_projects.py`
   skips the contract check when no `atlas` key is present (`tools/check_projects.py:144-146`).
2. **Closure modules are unbuilt.** AP2, CS1, P0.1, S0, S1 and S2 have no `index.html` (B6). `Unit.built` tests for `index.html`
   (`tools/coursekit.py`, `Unit.built`). `check_dag.py` accepts uses of closure concepts regardless of build status
   (`tools/check_dag.py:60-69`), and `concepts.html` lists every concept (`tools/build_site.py:374-381`), so the link resolves while
   the definition does not exist yet.
3. **check_dag sees linked uses only.** Unlinked uses of the D-rows in §4 pass the tool; the verifier reads for them (VERIFIER §2.9).
4. **Instance check covers the first 20 seeds.** `run_graders.py` checks distinct instances only for `seeds[:20]` (`tools/run_graders.py:97`).
   The verifier samples further seeds by hand (VERIFIER §2.6 item 2).
5. **The mutant directory is fixed.** `mutate_graders.py` reads only `ledgers/FC4/mutants/` (`tools/mutate_graders.py:42-47`).
   Equivalent mutants live in `ledgers/FC4/equivalent/` with a README (FINAL 9), and the alternatives in `ledgers/FC4/alternatives/`
   (no tool reads that path; the verifier runs them by hand).
6. **Rubric counts.** `check_projects.py:58-73` counts `td` cells per criterion row (four levels each) and 4 to 7 criteria (line 63).
   Level descriptors are not checked by the tool; the verifier does (VERIFIER §2.6 rubric item 1).
7. **Grading words.** The spec's grading entry must contain "autograd" and "rubric" for `both` (`tools/check_projects.py:38`, `:40-49`).
8. **The lab twin cannot import the grader.** `run_labs.py` runs each twin in its own workdir (`tools/run_labs.py`, the `data/` workdir
   note in BUILDER_RULES §6.6). The rung-3 twin is therefore self-contained (§12 Q12).
9. **The "first-year" grouping and the track lists** (`meta.yaml:133`, `:181-183`) are not acted on by this plan.

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **Lesson count and hours.** RECOMMENDED: 10 lessons × 6 h = 60 h, project 30 h (33 %), as in §1. This matches the FC2 split for a
   90-hour unit (`plans/FC2-build-plan.md:85-96`). Alternatives within the rules: 8 lessons of 8, 8, 8, 8, 7, 7, 7, 7 h (FC2's
   count) with builders A to D at two each; or 9 lessons of 6 to 7 h with the project at 30 h.
2. **Memo length and project scope.** RECOMMENDED: the memo is 1,500 to 2,500 words, and the autograder has exactly the five functions of §5.5 (no multiples function; multiples are rubric-only).
3. **Atlas wording (B1).** RECOMMENDED: the project does not require Atlas. A15 is optional. A16 is not used. The architect edits `yaml:495`, or accepts this reading (builders never edit `curriculum/*.yaml`).
4. **Real company data (B2).** RECOMMENDED: bring-your-own-data for the student's company (schema, validation, never leaves the browser); autograder and labs on SIMULATED data; honest-pending note on the page; DATA_REQUEST for EDGAR company facts (§6). No embedded fundamentals.
5. **AC4 as a prerequisite for residual income (D1, B7).** RECOMMENDED: add AC4 to FC4's prerequisites (`yaml:465`). AC4 precedes FC4 (position 10 < 56), so no reordering is needed, and this avoids re-teaching AC4's residual-income content. Alternative: plain prose with no link (§4 D1 default).
6. **WACC (D3).** RECOMMENDED: no change. FCFE is discounted at \(k_e\) (AP2's CAPM, in the closure). CF2 is not added.
7. **Porter and Graham & Dodd (B3).** RECOMMENDED: REFERENCE_REQUESTS (§7.2); no admission; the five-forces framework is stated as a definition with no attribution until the record is admitted; Graham & Dodd is not cited.
8. **Bodie edition and year (B4).** RECOMMENDED: cite `bodie2023investments` with no edition or year in prose. The architect may correct `yaml:489` after checking the edition.
9. **Gordon & Shapiro attribution (B5).** RECOMMENDED: the builder reads the abstract at the record's DOI before attributing the valuation formula to `gordon1956capital`. If not confirmed, L04 derives the formula (T) with no attribution.
10. **Build order (B6).** RECOMMENDED: FC4 verification starts only after AP2, S0, S1, S2, CS1 and P0.1 are built. The topological fan-out already places them earlier (positions 0 to 34 before 56). FC4 drafting may proceed in parallel.
11. **Riskless-rate symbol.** RECOMMENDED: write the net riskless rate as `r_f`, stated as net, and never reuse the registered `R_f` (gross) for a net rate (§2.3). The verifier checks the collision. If AP2's page writes the rate differently when built, FC4 follows AP2.
12. **Lab twin and the grader.** RECOMMENDED: `lab-FC4-project-3` is a self-contained twin that prints the seed-0 table from its own formulas; it does not import `grader/reference.py`, because the labs run in their own workdir (§11 item 8).
13. **Question bank and the interface.** RECOMMENDED: no question bank (the brief asks for a report, not a defence; not adversarial; `yaml:493-497`). The five-function interface of §5.5 is frozen by the architect before the grader is built.
14. **Money conventions.** RECOMMENDED: the price target is an integer number of cents, rounded once half up on the exact `Fraction`; per-share values are exact `Fraction`s; no float in any graded money output.
15. **Mutant and alternative counts.** RECOMMENDED: exactly the ten mutants m01 to m10 and the five alternatives alt_1 to alt_5 (FINAL 10 requires five). The verifier may add a hard-coded seed-0 mutant (VERIFIER §2.6 item 3).
16. **Rubric.** RECOMMENDED: six criteria (C1 to C6), exemplars at levels 4 and 2 on the SIMULATED company, blind scoring by a separate scorer (FINAL 15 and 23).
17. **Project hours.** RECOMMENDED: 30 h (§5.3). The planner's component estimate sums to 30 h; the verifier's tolerance is 30 % (VERIFIER §2.6, hours).
18. **Curriculum lab placement.** RECOMMENDED: `lab-FC4-L04-1` in L04, the lesson that defines `gordon-growth-model`. `yaml:490` names no lesson; the architect confirms.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01 to L03; L04 to L06 (includes the curriculum lab); L07 to L08;
   L09 to L10; the project (rubric, instance validity, the ten mutants, the five alternatives). Failing rows return to the builder
   that owns the file, with only the failing rows.
3. A separate blind scorer scores exemplar-a and exemplar-b from the stripping script's output only (FINAL 23).
4. Ledger at `ledgers/FC4.verification.json`; verifier scripts archived under `ledgers/FC4/scripts/` (VERIFIER §3); mutants under
   `ledgers/FC4/mutants/` (10 files, plus any verifier addition); equivalent mutants under `ledgers/FC4/equivalent/` with a README;
   alternatives under `ledgers/FC4/alternatives/`.
5. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1, B2, B3, B5 and B6 must be
   resolved or named as honest gaps first. Merging and pushing are separate acts.

---

## Architect decisions: pending (§12). This plan is the planner's proposal.
