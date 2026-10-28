# AC4 build plan: Haiku builders in parallel (planner output, 2026-10-27)

Unit: **AC4 · Managerial & Cost Accounting for Decisions** · tier U · 70 h · prerequisites AC1 · no Atlas milestone ·
grading `both` (autograder for the budget and variance engine, rubric for the management memo) · output directory
`course/modules/AC/AC4/` (part code `AC`, as for AC2). Owner: orchestrator (architect). Executors: Claude Haiku builders,
then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Status of this file: a planner's proposal. Open questions in §10 need an architect decision before builders start.
No lesson content is written here.

## 0. Evidence for the curriculum facts used below (file and line read)

| Fact | Evidence |
|---|---|
| Entry: id, title, tier U, hours 70, prereqs [AC1] | `curriculum/02-economics-finance-core.yaml` lines 614-618; `curriculum/curriculum.json` lines 8007-8013 (`hours` at 8010) |
| Core text (cost behaviour through EVA) | yaml lines 619-623 |
| Twelve introduced concepts, one per entry | yaml lines 624-636; `curriculum.json` concepts dict, each with `"module": "AC4"` (12 hits) |
| Sources: Datar & Rajan (2021); Cooper & Kaplan (1988) [V]; Kaplan & Cooper (1998) | yaml lines 637-640 |
| Lab: "CVP break-even under mixed cost structures." | yaml line 641 |
| Project: "Budget and variance engine", deliverable "Tested model plus management memo.", grading `both` | yaml lines 642-649 (`grading: both` at 649); `curriculum.json` lines 8035-8040 |
| No `debate` key on AC4 | yaml lines 614-649 (no `debate:` line in range; the three debate lines in the file are at 270, 311, 460, none in AC4) |
| No `atlas:` key on AC4 project; no Atlas milestone names AC4 | yaml lines 614-649; `curriculum/meta.yaml` atlas list lines 194-265 (only A15 names AC2 at 255-258) |
| BS-FIN credential requires AC4; course map "Managerial Accounting" | `curriculum/meta.yaml` lines 62 and 73 |
| No module lists AC4 as a prerequisite; STUDIO-AC requires only AC2 | yaml line 507 (`requires: [AC2]`); no `prereqs` containing AC4 in any yaml |
| Topological position: after S0, before CF1 | `curriculum/curriculum.json` `topological_order` (AC4 follows S0) |
| AC4 prerequisite closure: AC1 and P0.1 only | yaml line 618 (`prereqs: [AC1]`); AC1 block (yaml 518-523) has `prereqs: [P0.1]`; P0.1 has empty prereqs (read from `curriculum.json` `parts` modules, planner script run in session) |

## 1. Rules for every builder (binding; BUILDER_RULES adapted to AC4)

- Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `VERIFIER_RULES.md` §2 (what a verifier
  will check), this file. Study `course/modules/AC/AC2/` (template, lab embedding, cards, grader panel),
  `course/modules/S/S7/` (rubric memo, two exemplars, self-assessment) and `course/modules/AP/AP1/` (grader panel with a
  unit-local solution file, not an Atlas path). Imitate structure, not wording.
- **Evidence.** Every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key. The only AC4 keys in
  `references/references.json` are `datar2020horngrens` and `kaplan1998cost` (both `used_by: ["AC4"]`). Prerequisite
  keys (AC1, e.g. `ifrsndifrs`) may be cited where the claim is theirs. Anything else goes to `REFERENCE_REQUESTS`.
  Never type bibliographic data, a page, a table or a number from memory.
- **Textbook claims.** A definition or identity taught in the textbook is cited to `datar2020horngrens` with a
  `data-locator` only after the builder has read the locator in a source that reproduces it. Otherwise the claim
  is a derivation on the page (grade T where it is an algebraic identity, e.g. break-even volume \(F/(p-v)\)) and no
  locator is invented.
- **Practice and empirical claims.** Claims about what firms do (ABC adoption, budget slack, transfer-pricing
  practice) are graded C or B at most. The one primary article in the curriculum, Cooper & Kaplan (1988), is not in the
  registry (§6). Until it is admitted, a claim that depends on it is written as unsourced practitioner lore (grade D,
  "It is widely claimed...") or left out.
- **Numbers.** Every number is computed live (lab), derived on the page, or quoted with a confirmed locator. All
  case numbers are generated and labelled **SIMULATED**. No number may look like a real company's figures.
- Concepts (BUILDER_RULES §1.10, §4.1): each of the 12 concepts in §2 is defined exactly once, with
  `<dfn id="def-<id>" data-concept="<id>">`, in the lesson assigned below, and linked elsewhere with
  `<a class="concept" data-concept="<id>" href="Lnn.html#def-<id>">` (earlier lessons of AC4) or
  `href="../../../concepts.html#<id>"` (AC1 and P0.1 concepts). A lesson never links a concept defined later.
  Terms outside the 12 concepts and outside AC1 are NOT defined with `<dfn>` (check_dag would reject a dfn for a concept
  the module does not introduce). See §10, question 4.
- **Prerequisite closure.** Only AC1 and P0.1 concepts are usable without definition. Concepts from S2 (`ols-estimator`),
  AC2 (`return-on-invested-capital`), CF2 (`wacc`) are outside the closure (verified in curriculum.json `concepts`:
  `ols-estimator` module S2; `return-on-invested-capital` module AC2; `wacc` module CF2). Do not link them. See §10.
- Labs: code lives once in its twin `tests/labs/AC4/lab-AC4-Lnn-1.py` (numbered in display order); the page carries
  `@@LAB:<file>@@` and `@@OUT:<file>@@` and `tools/embed_labs.py` fills them. Labs run in Pyodide (standard library,
  seeded, no network, under 10 s) and under CPython identically. Prefer `fractions.Fraction` or integer cents for
  reconciliation checks (the reconciliation of variances must hold exactly, not to a float tolerance).
- Money in any shared code: `int` cents (BUILDER_RULES money rule is stated for Rust/PG/TS; this planner recommends
  the same for Python so the grader's reconciliation is exact). Architect to confirm, §10.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`,
  `course/concepts.html`, `course/assets/data/*.json`, `references/*.json`, `MANIFEST.json`). Never edit
  `curriculum/*.yaml`; request changes.
- Do not run `page_smoke.py` (builder rules: verifiers run it on a quiet machine). Targeted checks only (§8).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the
  BUILDER_RULES §10 output contract.
- Banned strings (BUILDER_RULES §1.3-1.4) apply to all prose: no TODO, TBD, "for brevity", "it is important to note",
  "studies show", "it is well known".

## 2. Outline and file ownership (proposed; the architect fixes it)

Hours: lessons 50 + project 20 = 70 (curriculum line 617 gives 70). Eight lessons of 6 or 7 h, each inside the 6-12 h
rule (check_pages.py line 228). Every concept of the 12 is assigned to exactly one lesson.

| Lesson | Title (working) | Concepts it defines (from `introduces`, yaml 624-636) | Hours | Lab twin id | Owner |
|---|---|---|---|---|---|
| L01 | Cost behaviour and contribution margin | `cost-behaviour`, `contribution-margin` | 6 | `tests/labs/AC4/lab-AC4-L01-1.py`: fit a mixed cost on a SIMULATED monthly history (high-low, then a second method, see §10 Q3) | Builder A |
| L02 | Cost-volume-profit analysis and break-even | `cost-volume-profit-analysis`, `break-even-point` | 7 | `lab-AC4-L02-1.py`: CVP break-even under mixed cost structures (the curriculum lab, yaml 641) | Builder A |
| L03 | Relevant costs for decisions | `relevant-cost` | 6 | `lab-AC4-L03-1.py`: make-or-buy and keep-or-drop on a SIMULATED case with sunk and avoidable costs | Builder B |
| L04 | Activity-based costing | `activity-based-costing` | 6 | `lab-AC4-L04-1.py`: volume-based versus activity-based unit costs on two SIMULATED products | Builder B |
| L05 | Master and flexible budgets | `master-budget`, `flexible-budget` | 7 | `lab-AC4-L05-1.py`: master budget, then the flexed budget at actual volume | Builder C |
| L06 | Budget variance analysis (price, volume, mix, efficiency) | `budget-variance-analysis` | 6 | `lab-AC4-L06-1.py`: four-way decomposition that reconciles exactly to total profit variance | Builder C |
| L07 | Transfer pricing | `transfer-pricing` | 6 | `lab-AC4-L07-1.py`: feasible transfer-price range under a capacity constraint, SIMULATED divisions | Builder D |
| L08 | Performance measurement: residual income and EVA | `residual-income`, `economic-value-added` | 6 | `lab-AC4-L08-1.py`: residual income and EVA on SIMULATED divisional data (capital charge per §10 Q1) | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 50 / 20 | none | — | none | Builder A |
| project | Budget and variance engine: four-rung ladder, autograder spec, memo rubric | none | 20 | `lab-AC4-project-1` (rung 1, worked example), `lab-AC4-project-2` (rung 2, completion) | Builder E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` | none | — | none | Builder E |
| cards | `cards.json`, one atomic card per definition, key identity, key result and misconception of L01-L08 | none | — | none | Builder F (after A-D) |

Ownership rule: a builder writes only its own lesson files and twins. The hub is written by Builder A after its own
lessons exist, so the lesson map links are right. Builder E's grader files are independent of the lessons.

Hours check: 6 + 7 + 6 + 6 + 7 + 6 + 6 + 6 = 50 (lessons); project 20; total 70 = curriculum. Project share 20/70 = 28.6%,
inside the 10-40% rule (check_pages.py lines 339-340). Lessons sum to hub `data-hours-lessons="50"` (check_pages.py
line 341).

Each lesson follows BUILDER_RULES §4.2 in order: why it matters (≤120 words), core content, inline labs, where the canon
breaks, misconceptions (≥3), problem set (≥3 in each of Mechanics, Proof, Empirical, Research, each with
`<details class="solution">`), key-results table, quiz (8-15 items). No debate brief: AC4 has no `debate` key (§0).

Content guidance per lesson (what each must establish; builders decide the argument):
- **L01**: the three cost behaviours; linear cost function \(TC = F + vQ\) in units stated; the contribution margin as
  \(p - v\) per unit and as a total; mixed-cost decomposition with the method's error stated.
- **L02**: CVP identities; break-even \(Q^\ast = F/(p-v)\) derived; margin of safety; the curriculum lab on a mixed
  cost structure; sensitivity to a change in fixed cost.
- **L03**: relevant cost as differential future cost; sunk cost exclusion; keep-or-drop with a capacity constraint.
- **L04**: cost pools, cost drivers, two-stage allocation; cross-subsidy from volume-based allocation (proved on the
  SIMULATED case, not asserted from literature).
- **L05**: master budget as the operating plan; flexible budget as the same cost function at actual activity; the
  reason the master budget cannot be compared directly with actuals.
- **L06**: price, volume, mix and efficiency variances; the identity that the four sum exactly to the total profit
  variance (T-grade, proved on the page); unfavourable/favourable sign convention stated once and used throughout.
- **L07**: the minimum and maximum transfer price under capacity, with the opportunity-cost argument; the
  conditions under which the range is empty.
- **L08**: residual income \(RI = \text{operating income} - \text{capital charge}\) and EVA with its capital charge and
  adjustments; the accounting choices that change both measures (defined on the page, not sourced to a number).

## 3. Project ladder (Builder E), per BLUEPRINT §5 and the AC2 / S7 examples

Hours are 20 (yaml 648 is the deliverable text; the 20 h is this planner's split, see §4).

- **Rung 1, worked example** (`lab-AC4-project-1`, skippable on placement): one fully solved SIMULATED case: master
  budget, flexed budget, four variances, reconciliation line by line, with a "why" annotation at each step.
- **Rung 2, completion** (`lab-AC4-project-2`, `class="lab completion"`): the same case with the mix and efficiency
  lines removed (`___`); graded instantly by the grader's properties on the completed lines. Its twin is the
  completed solution.
- **Rung 3, independent project** (graded): (a) the autograded engine `budget_engine.py` (§5), (b) the management
  memo, rubric-graded (§5, rubric).
- **Rung 4, stretch** (optional, open-ended): e.g. extend the engine to a rolling forecast or to a two-stage transfer
  price with a stated hypothesis. No ceiling; not graded.

Placement: the hub quiz (`data-mastery="0.8"`, matching S7 line pattern) includes items marked `data-skill` for the
rung 1-2 task (the variance reconciliation and the completion lines), per BUILDER_RULES §5.1.

## 4. Time budget (sums to 20 h)

| Component | Hours |
|---|---|
| Rung 1, worked example (read and annotate) | 1 |
| Rung 2, completion problem | 2 |
| Rung 3a, autograded engine (model, edge cases, reconciliation) | 8 |
| Rung 3b, management memo (draft and revision) | 6 |
| Rung 3c, self-check against the grader and the rubric | 3 |
| **Total** | **20** |

check_projects.py requires the components to sum to the declared 20 (time budget rule in its docstring).

## 5. Grader design (Builder E)

**Grading mode:** `both` (yaml 649). The spec must name the autograder and the rubric, or check_projects fails
(check_projects.py lines 38-50).

**Autograder (`budget_engine.py`, the student file).** Proposed interface (no Atlas contract exists, so the spec is the
only contract; the architect freezes it, §10 Q8):

- `master_budget(case: dict[str, Any]) -> dict[str, Any]`: budgeted units, revenue and cost by product, in integer cents.
- `flexible_budget(case: dict[str, Any], actual_units: int) -> dict[str, Any]`: the same cost function at actual volume.
- `variance_decomposition(case: dict[str, Any]) -> dict[str, int]`: keys `sales_price`, `sales_volume`, `sales_mix`,
  `efficiency`, `total`, with `sales_price + sales_volume + sales_mix + efficiency == total` exactly.

**Instances (`grader/instance.py`).** `make_instance(seed: int) -> dict[str, Any]`: deterministic; generates two or
three products with per-unit standard quantities and prices, fixed overhead, budgeted and actual volumes, an actual
mix that differs from budget, and an actual efficiency that differs from standard. Every instance is valid
(positive quantities, mix sums to actual units). Labelled SIMULATED in the spec. Seeds 0-49 must yield materially
different answers (BUILDER_RULES §5.3).

**Reference (`grader/reference.py`).** Full solution; must pass `run_graders.py --seeds 0-49`.

**Tests (`grader/test_project.py`).** Property and number checks:
- exact reconciliation: the four variances sum to the total profit variance with zero residual on every seed;
- sign convention: favourable variances are positive and unfavourable negative;
- flexible budget at actual volume reproduces the master budget when actual volume equals budgeted volume;
- mix variance is zero when actual mix equals budgeted mix, and efficiency is zero when actual quantities equal standard;
- edge cases: a single product (mix must be zero); zero actual units;
- failure behaviour: `ValueError` naming the violated condition for invalid input (negative units, mix not summing to
  units).

No test may pass a hard-coded answer; each checks values against the instance's own generating parameters.

**Starter (`grader/starter.py`).** Stubs that raise `NotImplementedError`; the suite must fail on it.

**Mutants (verifier requirement, VERIFIER_RULES §2.6).** The verifier writes at least three plausible wrong solutions, for
example: mix folded into price (mix variance omitted); flexible budget built from budgeted rather than actual units; a
sign flip on the efficiency variance; a per-unit rather than total contribution margin; rounding that breaks exact
reconciliation. Each must fail a test.

**Dual mode.** Identical suite in Pyodide and CPython; each test under 5 s in Pyodide, suite under 60 s.

**Rubric (memo, Builder E).** 4-7 criteria, each with four observable levels, for example: (1) the decomposition is
reconciled and each variance is named with its sign; (2) the cause of each variance is tied to a cited number in the
case; (3) the cost-behaviour assumptions and their limits are stated; (4) the recommendation follows from the numbers
and names what would change it; (5) the memo's audience-appropriate structure. Exemplars at level 4 and level 2 with
annotations; a self-assessment form; the page shows where the student's scoring diverged from the exemplar scoring.
Adversarial question bank: not required unless the architect classes the memo as adversarial (§10 Q9).

**Grader panel** (`project.html`, following AP1, not S7/AC2): `data-unit="AC4" data-grader="grader/"
data-suite="test_project.py" data-support="instance.py" data-solution="budget_engine.py" data-starter="starter.py"
data-packages="" `. The solution path names a unit-local file, not `atlas/`, because AC4 has no Atlas milestone (§7).

## 6. Registry keys and requests

**Usable now (verified records, in `references/references.json`):**

| Key | Record | Use | Flag |
|---|---|---|---|
| `datar2020horngrens` | Datar & Rajan, *Horngren's Cost Accounting*, Pearson, ISBN 9780136708230, Open Library; record year 2020; `notes.year`: curriculum "2021", record "2020" | textbook definitions and worked conventions, with locators only after confirmation | year mismatch with the curriculum string (§10 Q5) |
| `kaplan1998cost` | Kaplan, *Cost & effect*, Harvard Business School Press, ISBN 0875847889; record year 1998; one author in the record | ABC and integrated cost systems | record lists Kaplan only; curriculum string says "Kaplan & Cooper" (§10 Q5) |
| `ifrsndifrs` | IFRS Standards (primary, used by AC1) | only if a page needs a standard reference | none |

**Unresolved (REFERENCE_REQUESTS):**

- Cooper & Kaplan (1988), "Measure Costs Right: Make the Right Decisions", *Harvard Business Review* 66(5), marked [V]
  in the curriculum (yaml line 639). Not in the registry. `references/SEED_REPORT.md` line 37 and
  `references/review_queue.json` line 490 (`used_by: AC4`, flags `["V"]`, reason: "no candidate established identity").
  The queue's candidates (for example a 1988 book on illicit drugs) do not match. Request: manual admission by an
  authoritative stable URL, with the HBR record. Needed for: ABC motivation and any practitioner claim in L04 (grade C).
  Confidence the citation string is correct: as given by the curriculum, unverified.
- No registry source is named for residual income, EVA, transfer pricing or budgeting beyond the textbook. The
  curriculum names none (yaml lines 637-640). A primary empirical source on performance measures or ABC outcomes would
  be a REFERENCE_REQUEST if a builder needs a graded empirical claim. None is proposed here, because naming one from
  memory would be a fabrication.
- Candidate for the L08 link between residual income and valuation: `ohlson1995earnings` (verified, currently
  `used_by: ["AC3", "CF4"]`). Usable only if the verifier confirms the claim against the paper. Not in the AC4 registry
  list yet; the architect decides whether AC4 may add it to `used_by`.

## 7. Real-data policy and Atlas

- **Real data: none.** No dataset in `course/assets/data/market/MANIFEST.json` relates to managerial accounting (its
  three entries are `fx_daily`, `fx_monthly`, `ust_daily`, `tools/data_sources.yaml` lines 19, 53, 91). The curriculum
  names no data source for AC4 (yaml 637-640). Company cost data is internal and not redistributable. Therefore:
  - all cases are generated and labelled **SIMULATED** on every page, in every figure and in the grader spec;
  - `data-files` is not used (no lab reads a snapshot); check_pages' data rule is then vacuous for AC4;
  - no `DATA_REQUESTS` entry is needed for the unit. If the architect wants a real-company exercise, a request is
    raised under `DATA_REQUESTS` and the page shows an explicit honest-pending note. Not proposed.
- **Atlas: none.** `curriculum/meta.yaml` atlas list (lines 194-265) has no entry for AC4 and the AC4 project has no
  `atlas:` key (yaml 642-649). `check_projects.py` lines 144-146 (Atlas contract check) therefore do not apply. No
  `atlas/A*.contract.md` is written for AC4.

## 8. Commands for this unit (check AC4 only; run each once, after the relevant files exist)

```bash
.venv/bin/python tools/check_pages.py --unit AC4            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit AC4
.venv/bin/python tools/check_projects.py --unit AC4
.venv/bin/python tools/run_labs.py --unit AC4                # --page L02 while building
.venv/bin/python tools/run_graders.py --unit AC4 --seeds 0-49
.venv/bin/python tools/embed_labs.py course/modules/AC/AC4/L01.html   # per page, after twins are written
.venv/bin/ruff check tests/labs/AC4 course/modules/AC/AC4/grader && .venv/bin/ruff format --check tests/labs/AC4
.venv/bin/mypy                                               # strict, repo configuration
```

Not run by builders: `page_smoke.py` (verifiers only). Gate-level checks that cover AC4 across the repo
(`check_pages.py --all`, `build_site.py --check`, `render_curriculum.py`) are the architect's, once, before merge.

Commands above are the repo's own flags, as read in each tool's argparse block: check_pages.py (`--unit`, `--all`,
`--page`), check_dag.py (`--unit`, `--all`), check_projects.py (`--unit`, `--all`), run_labs.py (`--unit`, `--all`, `--page`),
run_graders.py (`--unit`, `--all`, `--seeds`), embed_labs.py (pages, `--refresh`). The planner did not execute them;
they are not verified against AC4 yet.

## 9. Tooling assumptions that do not hold for AC4 (flagged)

1. **No Atlas milestone.** `check_projects.py` Atlas branch and `run_graders.py` (solution path from `atlas/`, per its
   docstring lines 1-25) do not apply. The grader panel must point at a unit-local solution file (AP1 pattern,
   `data-solution="sdf_recovery.py"` in `course/modules/AP/AP1/project.html`).
2. **No debate tag.** `check_pages.py` debate check (its line 412) is not triggered; no debate brief is required.
3. **No embedded data.** The data checks are vacuous; real-data policy is SIMULATED throughout.
4. **Prerequisite closure is thin.** Only AC1 and P0.1. Several natural tools are outside it (OLS, ROIC, WACC), see §10.
5. **Not a foundations module.** Tier U with `both` grading, so no "no autograder" exception is needed. Unlike a
   foundations module, AC4 has a rubric memo and an autograder, so the rubric path of check_projects must be exercised.
6. **No primary empirical source in the registry.** The unit's evidence base is one textbook, one book and one
   unresolved HBR article. Expect many grade C/D claims and few A/B. This is an honest gap, not a build defect.

## 10. Open questions for the architect

1. **EVA and residual income need a cost of capital.** The capital charge is WACC-like. `wacc` is introduced by CF2
   (curriculum.json concepts), which is outside AC4's closure (AC1, P0.1). Options: (a) state the capital charge as a
   given input rate in L08, defining no cost-of-capital concept; (b) add a prerequisite (curriculum change, not
   proposed here); (c) a forward link, which BUILDER_RULES §4.1 forbids. Planner recommends (a) and a curriculum
   request to make the dependence explicit.
2. **Residual income uses invested capital.** `return-on-invested-capital` is AC2 (curriculum.json concepts), not in
   the closure. Recommend L08 define the capital base in prose as an input, not link ROIC.
3. **OLS in the mixed-cost lab.** `ols-estimator` is S2 (curriculum.json concepts), not in the closure. L01's lab should
   use the high-low method only, or the architect accepts an unlinked least-squares step, which the verifier would have
   to flag. Planner recommends high-low only, with the method's error stated.
4. **Undeclared concepts.** `standard-cost`, `opportunity-cost`, `sunk-cost`, `incremental-cost`, `overhead-allocation`,
   `invested-capital` and `capital-charge` are not in curriculum.json `concepts` (verified). They may be used in prose
   but may not be defined with `<dfn>` (check_dag's rule). Options: teach them as plain terms, or request curriculum
   concepts (curriculum change). Planner needs a decision because L03, L04 and L06 depend on `opportunity-cost` and
   `sunk-cost`.
5. **Registry string mismatches.** (a) `datar2020horngrens` record year 2020 versus curriculum "2021"
   (`references.json` `notes.year`). (b) `kaplan1998cost` record author list is Kaplan only, while the curriculum string
   is "Kaplan & Cooper". Architect to resolve through the registry tools; builders cite the key only and do not change it.
6. **Cooper & Kaplan (1988)** unresolved (§6). Blocks grade-C ABC motivation in L04 unless admitted. Architect decision.
7. **Solution file name.** Proposed `budget_engine.py`; confirm. The reference is excluded from deployment
   (BLUEPRINT §7), as for other units.
8. **Frozen grader interface.** §5's three function signatures are a proposal; with no Atlas contract, the architect
   freezes them in the spec (and may request an `atlas/` contract, though the curriculum names no milestone).
9. **Adversarial or not.** A management memo is not an IC defense; no 15-angle question bank is required. If the
   architect classes the memo as adversarial, add the bank (check_projects, adversarial rule).
10. **Integer cents in Python.** Confirm that the grader and labs use integer cents or `Fraction`, so reconciliation is
    exact, as the planner recommends. (BUILDER_RULES states the i64 money rule for Rust/PG/TS.)
11. **Hours split.** 50 lessons / 20 project is the planner's split of the curriculum's 70. No pilot calibration exists
    for AC4. Alternative: 7 lessons of ~7 h with the project at 20 h. The 8-lesson split is recommended because it keeps
    each concept group within a single lesson.
12. **Observation for another unit.** `curriculum/02-economics-finance-core.yaml` line 593 (AC3 core text) names "the
    residual-income link", and AC3's closure (prereqs AC2, S6; yaml line 590) does not include AC4. This is plain text
    rather than a concept link, so check_dag will not flag it, but the architect may want AC3's text to avoid a concept
    AC4 introduces, or AC4 to precede AC3 in the prerequisite graph. Not in AC4's scope; reported only.

## 11. After the builders

1. Orchestrator integrates; runs the §8 commands once; fixes cross-lesson defects (DAG, links, hours).
2. Independent Haiku verifiers in fresh checkouts, slices: L01-L02, L03-L04, L05-L06, L07-L08, project. The project
   verifier writes at least three mutants per round (VERIFIER_RULES §2.6). Failures return to a builder with only the
   failing rows. Scripts that back a row go under `ledgers/AC4/scripts/` (VERIFIER_RULES §3).
3. Branch: a feature branch (not main), merged only when the unit ledger is PASS or its gaps are agreed.

## Architect decisions (2026-10-27, binding)
Q1: the capital charge is a stated input rate (no WACC link). Q2: invested capital is a stated input (no ROIC link, no AC2 dependency). Q3: high-low method only; no OLS. Q4: undeclared terms are plain prose. Q5/Q6: do not admit Cooper & Kaplan; make no claim that needs it; cite `datar2020horngrens` and `kaplan1998cost` by key with the registry's own record, and say nothing about edition or authors beyond what the registry holds. Q7: `budget_engine.py`; freeze the three proposed signatures in the plan before building. Q8: the memo is rubric-graded with exemplars at two levels; no question bank unless BUILDER_RULES requires one for `both` (read it and follow it). Q9: integer cents. Q10: 50/20 split, eight lessons confirmed.
