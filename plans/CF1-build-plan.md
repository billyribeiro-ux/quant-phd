# CF1 build plan: Haiku builders in parallel (2026-10-27)

Unit: **CF1 · Time Value & Capital Budgeting** · tier U · 60 h · prerequisites M1 only (`curriculum/02-economics-finance-core.yaml:673`, `prereqs: [M1]`; `curriculum/curriculum.json` parts[7].modules[0], `"prereqs": ["M1"]`) · Atlas milestone: **none** (the CF1 entry has no `atlas:` key, `curriculum/02-economics-finance-core.yaml:669-698`) · grading **both** (`curriculum/02-economics-finance-core.yaml:698`) · output directory `course/modules/CF/CF1/` (part code `CF`, `curriculum.json` parts[7].code; `tools/coursekit.py` Unit.directory). Planner: Haiku, written from a full read of the sources listed under "Evidence" below. Owner: orchestrator (architect). Executors: Claude Haiku builders, then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Status at planning: `course/modules/CF/` does not exist and `plans/CF1-build-plan.md` did not exist before this plan. CF1 is in the topological order at index 11 (`curriculum.json` topological_order), after the Pilot modules S7, AP1 and AC2 (`plans/AC2-build-plan.md` is the worked example for this shape).

## Evidence read (every curriculum statement below cites one of these)

- `curriculum/02-economics-finance-core.yaml:655-698`: studio STUDIO-CF (line 655) and the CF1 module entry: id 669, title 670, tier 671, hours 672 (60), prereqs 673, core 674-676, `introduces` 677-687 (ten concepts), `sources` 688-690 (two free-text strings), `lab` 691 (one sentence), `project` 692-698 (title, brief, deliverable, grading both). CF1 has **no `debate` key** and **no `atlas` key** in that block.
- `curriculum/curriculum.json`: the CF1 row at parts[7].modules[0] matches the yaml (hours 60, prereqs M1, the same ten `introduces` entries, part CF); `concepts` maps each of the ten to module CF1.
- `CURRICULUM.md:493`: `- **CF1 · Time Value & Capital Budgeting** · U · 60 h · ← M1`.
- `curriculum/02-economics-finance-core.yaml:655-660` and `curriculum.json` parts[7].studio: the studio STUDIO-CF (The Full Deal, rubric) is not part of CF1 and is not built by this plan.
- `tools/coursekit.py` `prerequisite_closure("CF1")` run by the planner returned exactly `['M1', 'P0.1']`. Consequence in section 7.
- M1 `introduces` (curriculum.json, M1 row): exponential-and-logarithm, compounding-frequency, continuous-compounding, **present-value**, **discount-factor**, geometric-series, **annuity**, **perpetuity**, **growing-perpetuity**, amortization-schedule, quantifiers, direct-proof, proof-by-contradiction, mathematical-induction. CF1 links these; it never redefines them.
- P0.1 `introduces` (curriculum.json): evidence-grade, paper-anatomy, identification, robustness-check, replication, steelmanning, project-ladder, prerequisite-dag, atlas-platform, citation-registry, notation-conventions. No statistics or accounting concept is in the CF1 closure.
- Concepts with the same or near names owned by other modules (must not be redefined in CF1): `depreciation-and-amortization` (AC1), `cash-flow-statement` (AC1), `monte-carlo-integration` (M8), `real-option` (CF4), `wacc` and `interest-tax-shield` (CF2), `cash-conversion-cycle` and `working-capital-days` (CF8), `price-index-inflation` (E5). Found by the planner in `curriculum.json` `concepts`.
- `tools/check_pages.py`: lesson `data-hours` 6-12 (line 227 check); hub `data-hours-lessons` + `data-hours-project` must equal the curriculum hours, project 10-40% (lines 332-340); hub objectives 4-8; placement `section.quiz#placement` with `data-mastery` and two or more `data-skill` items (lines 350-353); ladder with four rungs; cards.json rules (lines 366-398).
- `tools/check_projects.py`: rungs `worked example`, `completion`, `independent`, `stretch` in order (line 33); spec `dl.spec` terms context / inputs / required outputs / constraints / grading (line 34); the grading entry must name **both** "autograder" and "rubric" for `both` (lines 38-49); `section#hours` table with a total row equal to `data-hours-project` (lines 107-118); grader panel attributes `data-unit data-grader data-suite data-solution data-starter` and `grader/instance.py` defining `make_instance(seed: int)` (lines 122-136); rubric: 4-7 criteria, exactly four `td` levels each, exemplars with `data-level` 1-4 at two or more levels (lines 58-72); the Atlas contract check runs only if `atlas` is set (line 144).
- `tools/run_graders.py` line 138: skips units whose grading is `rubric` only; CF1 is `both`, so it runs. Default seeds 0-49 (line 131).
- `tools/check_dag.py` lines 1-20: a concept link must point at a concept the module introduces or at its prerequisite closure, and a module's own concepts may not be linked before their definition.
- `references/references.json`: 560 entries, all with status `verified`; keys used in section 8 were confirmed by the planner by reading the entry.
- `tools/data_sources.yaml` and `course/assets/data/market/MANIFEST.json`: three embedded snapshots only (`fx_daily.csv`, `fx_monthly.csv`, `ust_daily.csv`). None is needed by CF1.
- Reference modules read for structure: `plans/AC2-build-plan.md` (whole), `course/modules/AC/AC2/index.html` (hub: header, objectives, prerequisites, placement, lessons, ladder, reading), `course/modules/AC/AC2/L01.html` (lesson: `data-hours`, section order, inline `section.lab` with `data-runtime`, `block definition|theorem|proof|remark`, `section.quiz#quiz data-cards`), `course/modules/AC/AC2/project.html` (`ol.ladder`, `dl.spec`, `#hours` table, `section.grader-panel`, `ol.reading-list`), `course/modules/AC/AC2/cards.json` (fields id, lesson, front, back; cite, grade, basis when used), `course/templates/hub.html`, `course/templates/README.md`. S7 and AP1 were checked for file layout (`grader/` with `instance.py reference.py starter.py test_project.py`; labs `tests/labs/S7/`, `tests/labs/AP1/`; sol- twins for completion problems in S7 and AP1 only).

## Rules for every CF1 builder (binding; BUILDER_RULES adapted to CF1)

- Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, this file. Study `course/modules/AC/AC2/` and `course/modules/S/S7/` for structure only. Imitate structure, not wording.
- Evidence standard: every claim carries a grade (T/A/B/C/D/X) and a registry key (`data-cite`). Only keys listed in section 8 and only keys confirmed in `references/references.json`. A source not in the registry goes into `REFERENCE_REQUESTS`; never type bibliographic data, a table, a page or a coefficient from memory. The curriculum's `sources` strings are not keys; section 8 maps them.
- Textbook practice ("firms use payback") is graded C at most unless a registry source with a confirmed locator says it. Any number taken from a source needs a `data-locator` the builder has actually read, otherwise the number is left out.
- Concepts: each of the ten CF1 concepts is defined exactly once with `<dfn id="def-<id>" data-concept="<id>">` in its assigned lesson (section 2). M1 and P0.1 concepts are linked: `<a class="concept" data-concept="present-value" href="../../../concepts.html#present-value">`. A concept outside the CF1 closure (AC1, M8, CF2, CF4, CF8, E5, the statistics concepts) is **not linked**; the builder describes the idea in plain words and adds a `DAG_DEFECT` line (section 7).
- Lab code lives once, in `tests/labs/CF1/<lab-id>.py`. The page carries `@@LAB:`/`@@OUT:` markers and `.venv/bin/python tools/embed_labs.py <page>` fills them. Never type expected output. Labs are **standard library only** (`random.Random(seed)` for every random draw), run under 10 s in Pyodide, no network, no warnings.
- Labs and the autograder use **generated cash flows labelled SIMULATED**. No real company is shown. No dataset is embedded (section 9).
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`, `course/assets/data/*.json`, `references/*.json`, `MANIFEST.json`, the market snapshots).
- Never use `window.confirm`, CDN links, remote fonts or iframes.
- Do not run `page_smoke.py` (timing-sensitive; verifiers run it on a quiet machine). Targeted checks only (section 10). Report what actually ran; do not report PASS for a check you did not run.
- No `git commit`, no push, no branch changes. Builders write only under `course/modules/CF/CF1/`, `tests/labs/CF1/`, `tests/` for their own unit tests, and `plans/` is read-only for builders.
- Output contract: the BUILDER_RULES §10 block, with the hours line filled from section 4 and the `REFERENCE_REQUESTS`, `GLOSSARY_REQUESTS`, `DATA_REQUESTS`, `DAG_DEFECTS`, `KNOWN_LIMITATIONS` lines.

## 1. Unit facts (from the curriculum, cited above)

| Field | Value | Source |
|---|---|---|
| Title | Time Value & Capital Budgeting | yaml 670 |
| Tier / hours | U / 60 h | yaml 671-672; CURRICULUM.md:493 |
| Prerequisites | M1 (and, through M1, P0.1) | yaml 673; closure computed in section 7 |
| Core | NPV, IRR and its pitfalls, payback, project cash flows, inflation and real vs. nominal, what CFOs actually do | yaml 674-676 |
| Concepts introduced | 10 (section 2) | yaml 677-687 |
| Sources (curriculum text) | Brealey, Myers & Allen, *Principles of Corporate Finance*, 14th ed. (2023); Graham & Harvey (2001), JFE 60(2-3) | yaml 688-690 |
| Lab (curriculum text) | Multiple-IRR and NPV-vs-IRR ranking conflicts | yaml 691 |
| Project (curriculum text) | "Capital-budgeting engine": tax, depreciation, working capital, real-vs-nominal handling, plus Monte Carlo NPV. Deliverable: "Tested module plus a case memo." Grading: both | yaml 692-698 |
| Debate tag | none | yaml 669-698 (no key) |
| Atlas | none | yaml 669-698 (no key) |

The curriculum names **one** lab. The per-lesson labs in section 2 beyond that one are planner proposals and are marked as such.

## 2. Outline (one row per lesson; the concept assignment is fixed, do not move concepts)

| Lesson | Title (working) | Concepts defined here (each exactly once) | Lab twin id (`tests/labs/CF1/<id>.py`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | The net present value rule and the capital budget | `net-present-value` | `lab-CF1-L01-1`: NPV of a seeded constant-rate project against the M1 annuity closed form (planner proposal) | 8 | Builder A |
| L02 | Project cash flows: incremental, tax, working capital | `incremental-cash-flow`, `net-working-capital`, `depreciation-tax-shield` | `lab-CF1-L02-1`: after-tax incremental cash flows; the shield identity depreciation × tax rate; working-capital investment and recovery sum to zero (planner proposal) | 8 | Builder A |
| L03 | Inflation: real and nominal cash flows | `fisher-relation`, `real-vs-nominal-cash-flows` | `lab-CF1-L03-1`: the same project discounted consistently in real and in nominal terms gives the same NPV; a mixed discounting gives a different one (planner proposal) | 8 | Builder B |
| L04 | Internal rate of return and its pitfalls | `internal-rate-of-return`, `multiple-irr-problem` | `lab-CF1-L04-1`: **the curriculum lab**: multiple IRRs and NPV-vs-IRR ranking conflicts | 8 | Builder B |
| L05 | Payback, and what firms actually use | `payback-period` | `lab-CF1-L05-1`: simple and discounted payback on one project; payback ignores cash flows after the cut-off (planner proposal) | 8 | Builder C |
| L06 | Simulation-based NPV | `monte-carlo-npv` | `lab-CF1-L06-1`: seeded Monte Carlo NPV distribution, checked for convergence against a case with a closed form (planner proposal) | 8 | Builder C |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split, core reading | none | none | none | Builder A |
| project | Capital-budgeting engine (both) | none | `lab-CF1-project-1` (rung 1, worked), `lab-CF1-project-2` (rung 2, completion, `class="lab completion"`), `lab-CF1-project-3` (rung 3 sanity run) | none | Builder D |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` | none | none | none | Builder D |
| cards | `cards.json`: one card per misconception and key result of L01-L06 | none | none | none | Builder E (after A-C) |

Every concept in `introduces` (curriculum yaml 677-687) appears in exactly one row. Lesson count is six, derived from the hours rule in section 4.

Lesson content order inside each lesson: why it matters (120 words max), numbered core sections with Definition/Theorem/Proof/Example/Remark blocks, inline lab, where the canon breaks, misconceptions (3 or more), problem set (3 or more in each of the Mechanics, Proof, Empirical, Research tiers, each with a full worked solution in `<details class="solution">`), key-results table, quiz (8-15 items with explanations), references (registry keys). **No debate brief** is required (CF1 has no `debate` tag, yaml 669-698), so do not write one under that heading.

Required on the L04 page, because of the curriculum lab: the NPV profile must show two sign changes in the cash flows and the case where the IRR ranking and the NPV ranking disagree. The lab output, not the prose, is the evidence.

Theorem-level content (grade T, proved on the page): the NPV additivity over projects; the NPV-to-IRR identity at the root; the Fisher relation as an exact identity `(1+n) = (1+r)(1+π)`; the shield identity `depreciation × t`; the working-capital sum-to-zero identity. Empirical claims (CFO practice, payback use) are graded C or B and carry their two-sided counter-evidence (BUILDER_RULES §2.5).

## 3. Hub (`index.html`, Builder A)

- `<html lang="en" data-root="../../../" data-unit="CF1" data-page="index">`. `<main data-hours-lessons="48" data-hours-project="12">`. The split sums to 60; the project is 20% of module hours (10-40% rule, `check_pages.py` lines 336-340).
- Objectives: 4-8 `ol.objectives` items with measurable verbs (for example: compute NPV and its sensitivity to the discount rate; construct incremental after-tax cash flows; convert between real and nominal cash flows; locate the multiple-IRR problem; compare payback with NPV; estimate an NPV distribution by simulation). Target six.
- Prerequisites: M1 (and P0.1 for the study method), with links to `present-value`, `discount-factor`, `annuity`, `perpetuity`, `growing-perpetuity` in `../../../concepts.html#…`.
- Placement: `section.quiz#placement data-mastery="0.8"` with nine items. At least two `data-skill` items test the skills rungs 1-2 teach (the worked example's NPV-with-tax computation, the completion problem's shield or working-capital line). The rest test M1 prerequisites.
- Lesson map: one `card` link per L01-L06 with `data-progress-key="CF1/Lnn"` and `data-hours` text.
- Ladder: four `li` with `span.rung-title` for `Worked example`, `Completion problem`, `Independent project`, `Stretch`, in that order (`check_projects.py` line 33).
- Core reading: `ol.reading-list` (or `ol#reading`) with `li data-cite` keys from section 8 only.

## 4. Hours split (sums to the curriculum's 60)

| Component | Hours | Basis |
|---|---|---|
| L01 | 8 | NPV rule, annuity cross-check, the lab, the problem set |
| L02 | 8 | cash-flow construction is the largest mechanical topic in CF1 |
| L03 | 8 | Fisher relation and consistency proofs |
| L04 | 8 | IRR pitfalls; the curriculum lab |
| L05 | 8 | payback, evidence on use (two-sided) |
| L06 | 8 | Monte Carlo, error and convergence |
| **Lessons total** | **48** | `data-hours-lessons="48"` |
| Project | 12 | section 6 time budget |
| **Module total** | **60** | = curriculum hours (yaml 672) |

Each lesson `<html data-hours="8">` (6-12 rule, `check_pages.py` line 227). The project `section#hours` table rows must sum to 12 (section 6).

## 5. Lesson labs and figures

- Every lesson has at least one `section.lab` with `id="lab-CF1-Lnn-1"`, `data-runtime="python"`, and the hypothesis, code, expected and interpretation parts (BUILDER_RULES §6.1). Lab numbering is by display order; L04's lab is the curriculum lab.
- Labs read no data files. `data-files` is absent.
- Figures (optional, decided by the architect, section 11): L04 NPV-profile curve with the IRR roots marked; L06 NPV histogram of a seeded run labelled SIMULATED. A figure needs its JS kernel (`stats.js` or a new one) with a test in `tests/test_figure_kernels.py` before it is used (BUILDER_RULES §6.4). If the architect does not approve figures, the NPV profile is a table in L04.

## 6. Project ladder, spec and grader (Builder D)

Project page: `course/modules/CF/CF1/project.html`, `<main data-hours-project="12">`, grading text names **both**: "Grading: both. The autograder runs the engine; the rubric grades the case memo."

- Rung 1 · Worked example: `lab-CF1-project-1`, a fully solved and annotated NPV-with-tax computation on a small SIMULATED project.
- Rung 2 · Completion problem: `lab-CF1-project-2`, `class="lab completion"`, the after-tax cash-flow line with `___` blanks; the twin is the completed solution; graded instantly.
- Rung 3 · Independent project: the `capbudget.py` engine (autograded) plus the case memo (rubric). Scope exactly as the curriculum's project brief (yaml 694-697).
- Rung 4 · Stretch: an NPV under a term structure of discount rates on the same project, with a stated hypothesis. Not real options (`real-option` is CF4's).

`dl.spec` with dt: Context, Inputs, Required outputs, Constraints, Grading (section names must contain those words, `check_projects.py` line 34).

Time budget (`section#hours`, rows must sum to 12):

| Component | Hours |
|---|---|
| Read the spec, set up, run starter against the suite | 1 |
| Labs 1 and 2 (worked, completion) | 1 |
| `after_tax_cash_flows` (incremental, tax shield, working capital, real or nominal flag) | 4 |
| `npv`, `irr_roots`, `payback_period`, `fisher_nominal` | 2 |
| `npv_monte_carlo` (seeded, reproducible) | 1 |
| Edge cases, error classes, local pytest runs on your seed | 1 |
| Case memo (rubric) | 2 |
| **Total** | **12** |

Autograder (`section.grader-panel#grader`, `data-unit="CF1" data-grader="grader/" data-suite="test_project.py" data-support="instance.py" data-solution="capbudget.py" data-starter="starter.py" data-packages=""`). `data-packages` is empty because the grader is standard library only (assumption, section 10).

Grader files (`course/modules/CF/CF1/grader/`):

- `instance.py`: `make_instance(seed: int) -> dict`. Deterministic from `random.Random(seed)`; generates a conventional project (capex, life, revenue and cost paths, tax rate, straight-line depreciation, working-capital share, inflation, nominal discount rate). Every seed valid (positive life, rates above -1). Answers must differ across seeds; the grader checks materially different NPVs over seeds 0-49.
- `reference.py`: full solution. Must pass every test for seeds 0-49.
- `starter.py`: the same function names with `raise NotImplementedError`. Every test that calls one of them fails with a named property, not a stack trace.
- `test_project.py`: pytest properties (planner's proposed design; the architect approves the signatures in section 11):
  - `npv(0, flows) == sum(flows)` to 1e-9;
  - NPV is strictly decreasing in the rate for a conventional flow;
  - every IRR root returned by `irr_roots` has NPV within 1e-8 of zero;
  - a flow with two sign changes returns two roots (Descartes), checked against a grid scan;
  - `after_tax_cash_flows`: the depreciation shield equals depreciation × tax rate in each year; working-capital investment and recovery sum to zero;
  - Fisher round trip: `(1 + fisher_nominal(r, π)) == (1 + r) * (1 + π)`;
  - `npv_monte_carlo` is reproducible for a seed and its mean lies within three standard errors of the deterministic NPV when volatility is zero;
  - invalid input (negative life, rate at or below -1) raises a named error whose message names the rule and gives a hint, never the answer.

Mutants (VERIFIER ledger, at least three, planner's list of plausible student errors): (1) shield with the wrong sign; (2) working capital recovery omitted; (3) real flows discounted at the nominal rate; (4) IRR by bisection that returns only the first root; (5) payback that ignores the fractional year. Each must be killed by at least one test.

Rubric memo (`table.rubric#rubric-memo`): five criteria, each with four observable levels (a level descriptor must name something a grader can see, for example "states the discount rate and its basis in the memo"):

1. Decision rule and recommendation (NPV decision, stated rule).
2. Cash-flow construction (incremental, tax, working capital, real or nominal consistency).
3. Handling of IRR and payback pitfalls (multiple roots, ranking conflicts).
4. Uncertainty (Monte Carlo distribution, assumptions and seed stated).
5. Evidence (every empirical claim graded, with a registry key and a locator).

Exemplars: `data-level="4"` and `data-level="2"` full case memos on a SIMULATED project, annotated with the descriptors each passage meets or misses. Self-assessment form. The memo is not adversarial (curriculum says "Tested module plus a case memo", yaml 697), so no question bank is required.

## 7. DAG risk (must be reported, not patched by the builder)

- `prerequisite_closure("CF1")` returns `['M1', 'P0.1']` (planner, from `tools/coursekit.py`). CF1 may link only M1, P0.1 and its own concepts (`tools/check_dag.py`).
- `incremental-cash-flow`, `net-working-capital` and `depreciation-tax-shield` need straight-line depreciation and balance-sheet working capital. Those are AC1 concepts (`depreciation-and-amortization`, and the balance sheet), not in the closure. The builder defines the mechanism inline, in plain words, **without a link**, and reports a `DAG_DEFECT`.
- `monte-carlo-npv` needs mean, standard error and quantiles. No statistics concept is in the closure (only P0.1 and M1). The builder uses plain words and reports a `DAG_DEFECT`.
- The architect decides whether to add prerequisites (for example AC1 or an S-series module) or accept the defects. The builder never edits `curriculum/*.yaml`.

## 8. Registry keys (verified in `references/references.json` by the planner, status `verified`)

| Key | Record (as read) | Use in CF1 | Status |
|---|---|---|---|
| `graham2001theory` | Graham & Harvey, "The theory and practice of corporate finance: evidence from the field", JFE 60(2-3), 187-243, doi 10.1016/s0304-405x(01)00044-7 | the curriculum's CFO-practice source (yaml 690); L05 and rubric criterion 5 | Exists. Its source string matches the curriculum's text exactly. **No number from it may be quoted** until a builder confirms a locator by reading the paper; until then, grade C, no figures. |
| `brealey2022principles` | Brealey, *Principles of Corporate Finance*, McGraw-Hill, year 2022, ISBN 9781264080946 | the curriculum's textbook source (yaml 688) | Exists, **but the record conflicts with the curriculum string**: the record lists only Brealey and year 2022, and the curriculum cites Brealey, Myers & Allen, 14th ed. (2023). The record's `notes.year` shows "curriculum 2023, record 2022". Flag to the architect (section 11, Q3). Usable for textbook definitions only after the identity is settled. |
| `damodaran2012investment` | Damodaran, *Investment valuation: tools and techniques for determining the value of any asset*, 2012 | optional for NPV and IRR practice; grade C, locator required | Exists. Not required. |
| `glasserman2003monte` | Glasserman, *Monte Carlo Methods in Financial Engineering*, 2003, Springer | L06 Monte Carlo error and convergence (derivation on the page; cite for the method) | Exists. Locator required for any quoted statement. |
| `gordon1956capital` | Gordon & Shapiro, "Capital Equipment Analysis: The Required Rate of Profit", Management Science 3(1), 1956 | optional history of capital-budgeting criteria; grade C | Exists. Not required. |
| `lintner1965valuation` | Lintner, "The Valuation of Risk Assets and the Selection of Risky Investments in Stock Portfolios and Capital Budgets", REStat 47(1), 1965 | optional, the title names capital budgets; grade C | Exists. Not required. |

Keys in the registry that belong to other modules and must **not** be cited as CF1 sources: `myers1984capital` (CF2 scope), `dixit1994investment` (real options, CF4 scope), `harvey2015cross` (asset-pricing factor work). The two curriculum sources are the only textbook and survey sources for CF1.

No CF1 cite may use a key that is not in the table above without a `REFERENCE_REQUESTS` line first.

## 9. Real-data policy

- The curriculum names no dataset for CF1 (yaml 669-698 has no data field).
- The embedded snapshots (`fx_daily.csv`, `fx_monthly.csv`, `ust_daily.csv`, section 1 evidence) are not used.
- All project and lab cash flows are **generated and labelled SIMULATED** on the figure, the lab hypothesis, and the project page. Nothing is shown as a real company's.
- No `DATA_REQUESTS` line is needed. The honest-pending note (BUILDER_RULES §6, the AC2 pattern) is not needed either, because CF1 has no real-filer exhibit. If a builder adds a real company example, the builder must add a `DATA_REQUESTS` line and label it as pending; the planner recommends against it.

## 10. Commands (exact)

Builder self-check, targeted (run once per lesson or file while building; `--page Lnn` while a lesson is in progress):

```bash
cd /Users/billyribeiro/dev/quant-phd
.venv/bin/python tools/check_pages.py --unit CF1            # --page L01 while in progress
.venv/bin/python tools/check_dag.py --unit CF1
.venv/bin/python tools/check_projects.py --unit CF1
.venv/bin/python tools/run_labs.py --unit CF1               # --page L01 likewise
.venv/bin/python tools/run_graders.py --unit CF1 --seeds 0-49
.venv/bin/ruff check tests/labs/CF1 course/modules/CF/CF1/grader && .venv/bin/ruff format --check tests/labs/CF1 course/modules/CF/CF1/grader
.venv/bin/mypy tests/labs/CF1 course/modules/CF/CF1/grader
.venv/bin/python tools/embed_labs.py course/modules/CF/CF1/L01.html   # per page; --refresh <lab-id> after a twin edit
```

Verifier only (not builders): `.venv/bin/python tools/mutate_graders.py --unit CF1 --seeds 0-9`, `.venv/bin/python tools/page_smoke.py --unit CF1` on a quiet machine, and `.venv/bin/python tools/verify_refs.py --unit CF1` for the registry identity check. Full gate (CLAUDE.md) only before the merge, never per builder.

Note on `check_pages --all`: it only checks built units, so a partially built CF1 does not break it (`tools/coursekit.py` `built_units()`). A half-built CF1 must not be merged (AC2 plan, section "After the builders", step 3).

Status today (before any builder runs): `check_pages --unit CF1` reports `CF1 is not built`, and `check_dag`, `check_projects` and `run_graders` fail for the same reason. This is expected and is not a defect.

## 11. Tooling assumptions that do not hold, and open questions for the architect

Assumptions that do not hold cleanly for CF1 (this is a tier-U applied module, not a foundations module, so the autograder path applies):

1. **DAG closure is too small** (section 7). The check tools will reject any link to AC1, M8, E5 or a statistics concept. The builder cannot teach the depreciation shield or Monte Carlo NPV with links. This is the main structural risk.
2. **No Atlas milestone.** `check_projects.py` skips the Atlas contract check (line 144), and no `atlas/CF1.contract.md` is needed. The `capbudget.py` engine is module-local, not an Atlas component.
3. **Registry identity mismatch.** `brealey2022principles` disagrees with the curriculum's citation string (year and author list). `check_pages` checks only that the key is verified, so it passes, but the verifier's identity check will flag it.
4. **Textbook and survey claims.** Graham & Harvey (2001) is cited by key only. The planner did not read it. No figure from it is allowed until a builder confirms the locator.
5. **Rubric plus autograder ("both").** `check_projects` needs both words in the spec's grading entry (lines 38-49). The spec must say "autograder" and "rubric" verbatim.
6. **Pyodide packages.** `run_graders.py` imports numpy itself (line 35), but CF1's grader and labs use only the standard library. `data-packages=""` is the intended value; the architect should confirm the Pyodide runner accepts an empty package list (not checked by the planner).
7. **Lab count.** The curriculum names one lab (yaml 691). Labs L01-L03, L05, L06 and the project labs are planner proposals, not curriculum text.

Open questions (the architect decides; the builders do not):

- **Q1 (DAG).** Add an AC1 prerequisite (for depreciation and balance-sheet working capital) to CF1, or accept a `DAG_DEFECT` and inline definitions without links? Blocks L02.
- **Q2 (DAG).** Add a statistics prerequisite for the Monte Carlo lesson (mean, standard error, quantiles), or accept plain-word use with a `DAG_DEFECT`? Blocks L06.
- **Q3 (registry).** Resolve `brealey2022principles`: its record (year 2022, author Brealey only) does not match the curriculum string (Brealey, Myers & Allen, 14th ed., 2023). Options: correct the record through `add_reference.py`, or cite a different verified key. The planner did not change `references.json`.
- **Q4 (hours).** Six lessons of 8 h and a 12 h project (section 4), or five lessons of 9 h and a 15 h project? The planner recommends six, which keeps the lesson count closest to the curriculum's concept count (10 concepts over 6 lessons).
- **Q5 (project interface).** Approve the module-local engine name `capbudget.py` and the function signatures in section 6, or name them differently. There is no contract file to freeze them against.
- **Q6 (figures).** Approve two figures (L04 NPV profile, L06 NPV histogram), which need new JS kernels and tests (BUILDER_RULES §6.4), or make L04 a table and drop L06's figure.
- **Q7 (references needed).** `REFERENCE_REQUESTS` for topics the registry does not cover (no key on NPV-vs-IRR ranking conflicts, the Fisher relation primary source, or payback evidence). Topic only, no bibliographic data from memory. Specific requests come from the builders' output contracts.
- **Q8 (sources).** Confirm that the curriculum's `sources` (yaml 688-690) are the only source list for CF1, or whether the architect wants `damodaran2012investment` and `glasserman2003monte` added to the reading list.

## 12. Cards (Builder E, after A-C)

`course/modules/CF/CF1/cards.json` follows the AC2 pattern: `id` `CF1-c001` upward, `lesson` in `L01`-`L06`, `front`, `back`, and `cite` (registry keys) or `basis` when the result is established in the lesson's own lab or problem set. Each lesson contributes at least one card, and the planner expects four to six per lesson (one per definition, key result and misconception). Every card cites a key or names its `basis`, and `grade` is a valid BLUEPRINT §3 grade. Duplicates are not allowed.

## 13. After the builders

1. Orchestrator integrates, runs the unit gates once (section 10), and fixes cross-lesson defects (DAG, links, hours).
2. Independent Haiku verifiers in fresh checkouts, slices: L01-L02, L03-L04, L05-L06, project (with at least three mutants per round), and cards. Failures return to the owning builder with only the failing rows.
3. The branch is merged only when the unit ledger is PASS or its gaps are agreed. It is never merged incomplete.

## Architect decisions (2026-10-27, binding)
Q1: AC1 added to CF1's prerequisites in the curriculum (done, regenerated). Q2: no statistics prerequisite; the Monte Carlo lesson defines the few terms it needs in plain words and links no statistics concept. Q3: do not cite `brealey2022principles`; cite only keys whose registry record matches. Q4: six 8 h lessons plus a 12 h project. Q5: `capbudget.py` accepted. Q6: no new figures or JS kernels. Q7: topics only, no bibliographic data from memory. Graham & Harvey: cite by key, quote no figure.
