# S0 build plan: Haiku builders and verifiers (planner draft, 2026-10-27)

Unit: **S0 · Exploratory Data Analysis & Visualization** · tier F · 50 h · prerequisites CS1 (curriculum) · Atlas
milestone **A3** (Data-quality and EDA reports) · grading `autograder` · output directory `course/modules/S/S0/`.
Phase 2 fan-out (BLUEPRINT §9). Owner: orchestrator (architect). Executors: Claude Haiku builders, then independent
Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence for every curriculum statement below: `curriculum/01-foundations.yaml` lines 585-616 (S0 entry);
`curriculum/curriculum.json` (S0 module object at line 6873; concept entries at lines 2501-2505 and onward);
`curriculum/meta.yaml` lines 207-209 (Atlas A3, module S0). Statements not found in those files are marked
**NOT IN CURRICULUM**.

**Status of the unit today (checked by the planner):** `course/modules/S/S0/` does not exist. `check_pages --unit S0`
fails with "S0 is not built". `check_dag --unit S0` fails with 10 problems (every introduced concept undefined).
`check_projects --unit S0` fails on the missing `project.html`. `run_labs --unit S0` passes trivially (0/0 labs).
`run_graders --unit S0` must be run with `.venv/bin/python` (system python3 lacks NumPy).

## Blocking issues the architect must resolve before fan-out

These are real defects in the curriculum as written, found by reading the DAG. Builders must not work around them
silently. Each one is raised as a `DAG_DEFECT` or `CONTRACT_CHANGE_REQUEST`.

1. **Prerequisite closure is too small for the concepts S0 introduces.** S0 lists `prereqs: [CS1]`
   (`01-foundations.yaml` line 589). The transitive closure of S0 is exactly `{CS1, P0.1}` (checked against
   `curriculum.json`). The concept index assigns the statistical concepts a lesson needs to M4 (Probability), which
   is outside that closure: `quantile-function`, `normal-distribution`, `variance`, `skewness`, `kurtosis`,
   `random-variable`, `expectation` (all `module: M4` in `curriculum.json`'s concept index). The S0 concepts
   `robust-statistics` (median, MAD) and `qq-plot` (theoretical normal quantiles) cannot be taught correctly
   without them. Options: (a) add `M4` to S0's prerequisites (acyclic: the M4 closure is `{M1, M2, P0.1}` and does not
   contain S0, so this creates no cycle; S1 already lists `[M4, S0]` at line 621); this moves S0 after M4 in the order;
   (b) keep S0's prerequisites and restrict the lessons to empirical quantities, with no theoretical quantile
   function. Recommendation: (a). Architect decision required.
2. **The Atlas A3 project depends on the A2 data store, which S0 does not depend on.** The curriculum says A3 is
   "on any Atlas dataset in the store" (`01-foundations.yaml` line 612). The store is Atlas A2 in module CS3
   (`meta.yaml` lines 203-205; `curriculum.json` atlas list: `{"id":"A2","module":"CS3"}`). CS3 is not in S0's
   closure. Options: add `CS3` to S0's prerequisites, or define the A3 input as an in-memory table so that S0
   need not depend on CS3. Architect decision required.
3. **The Atlas contract `atlas/A3.contract.md` does not exist.** `atlas/` holds only `A8.contract.md` and
   `A15.contract.md`. `check_projects.py` line 145 fails the unit without it. The architect must draft it (as for
   A15) before the project builder starts. Also: the cumulative suite A1-A3 (BUILDER_RULES §5.5.3) needs A1 (CS1) and A2
   (CS3) code, which the repository does not contain; the cumulative test can only cover A3 itself until they exist.
4. **Anscombe's quartet values are not confirmed.** The lab needs the four datasets. The planner has no source for
   their values and the builders may not type them from memory (BUILDER_RULES §1.1, §2.6). See the Anscombe row in
   the lab plan.

## Rules for every builder (binding; adapted from AC2 and BUILDER_RULES)

- Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `VERIFIER_RULES.md` §2.5-2.8 (what a
  verifier will check), this file, and `atlas/A3.contract.md` once drafted. Study `course/modules/S/S7/` (template,
  lab embedding, cards, figures, grader layout), `course/modules/AP/AP1/` (project ladder with rung 2 completion lab)
  and `course/modules/AC/AC2/` (Atlas project, hub hours split, `cards.json` shape: `{"id","lesson","front","back"}`).
  Imitate structure, not wording. The AC2 `index.html` line 29 declares `data-hours-lessons` and `data-hours-project`;
  the AC2 lesson `L01.html` line 2 declares `data-hours="9"`.
- Evidence standard: every claim carries a grade (BLUEPRINT §3) and a registry key. The only S0 keys that exist and
  are verified in `references/references.json` are listed in the Registry section below. Anything else goes to
  `REFERENCE_REQUESTS`. Never type bibliographic data, a table, a page, a coefficient or a sample statistic from
  memory.
- Concepts are defined once, `<dfn id="def-<id>" data-concept="<id>">`, in the lesson assigned below (fixed table; do
  not move concepts). Prerequisite concepts are linked, never re-taught. Concepts from M4 are usable only if the
  architect has applied option (a) of Blocking issue 1; until then a lesson that needs them must say so in
  `DAG_DEFECTS`, not define them.
- Lab code lives once, in its twin `tests/labs/S0/<lab-id>.py`; the page carries `@@LAB:`/`@@OUT:` markers and
  `tools/embed_labs.py` fills them. Never type expected output. Labs run in Pyodide (NumPy, pandas if the architect
  allows it, standard library only; under 10 s; seeded; no network).
- **Real data policy (BUILDER_RULES §6.6, BLUEPRINT §5.3):**
  - Cleared and embedded in `course/assets/data/market/` (MANIFEST.json lists `fx_daily`, `fx_monthly`, `ust_daily`):
    - `fx_daily.csv`: issuer Board of Governors of the Federal Reserve System; licence quote in
      `tools/data_sources.yaml` lines 23-27 ("...may be copied and distributed without permission..."), licence page
      `https://www.federalreserve.gov/disclaimer.htm`. Note at lines 28-30: spot rates only; holidays have no row.
    - `ust_daily.csv` (H.15): same Board licence quote (`tools/data_sources.yaml` lines 95-99); the constant-maturity
      yield is a U.S. Treasury series (note at lines 100-104). Cite the MANIFEST retrieval date (2026-10-20 for
      H.15 per the header comment at `tools/data_sources.yaml` lines 9-14) in every source line.
    - `fx_monthly`: cleared, usable.
  - **Not cleared:** Kenneth French Data Library and Open Source Asset Pricing (`tools/data_sources.yaml`
    `rejected`, lines 119-137). Shiller data is a BLUEPRINT §5.3 candidate, not cleared; it must not be embedded
    without a quoted licence and a `DATA_REQUESTS` entry.
  - **No cleared equity price series exists in the repository.** Therefore the split-adjustment and corporate-action
    labs use **SIMULATED** prices, labelled SIMULATED on every figure and in the lab hypothesis, with an honest-pending
    note stating that no cleared equity series is available (DATA_REQUESTS: a cleared daily equity price file with
    split and dividend adjustment factors, source URL, licence quote, transform).
  - Never invent figures that look like a real issuer's or a real index's.
- Do not run `page_smoke.py` (timing-sensitive; verifiers run it on a quiet machine). Targeted checks only:
  `python3 tools/check_pages.py --unit S0`, `check_dag.py --unit S0`, `check_projects.py --unit S0`,
  `run_labs.py --unit S0`, `.venv/bin/python tools/run_graders.py --unit S0 --seeds 0-49`, `ruff`, `mypy`, and the
  unit's tests. Check only your own files while the unit is incomplete.
- No `git commit`, no push. Report files written, exact commands run with their output, and every gap or request
  (`GLOSSARY_REQUESTS`, `DATA_REQUESTS`, `REFERENCE_REQUESTS`, `CONTRACT_CHANGE_REQUESTS`, `DAG_DEFECTS`,
  `KNOWN_LIMITATIONS`) in the BUILDER_RULES §10 output contract.
- Figures: `figures-Lnn.js` drawn with `course/assets/js/chart.js`, numbers from `stats.js` / `multitest.js` only
  when a test in `tests/test_figure_kernels.py` covers them (BUILDER_RULES §6.4). Any "label legibility" sweep is run
  by verifiers, not builders.
- Writing: prose must not contain BUILDER_RULES §1.3-1.4 banned phrases ("it is important to note", "studies show",
  "experts agree", "obviously", "clearly", "TBD" and similar).

## Outline and file ownership (the architect's fixed assignment; do not move concepts between lessons)

Derivation: 10 concepts (`curriculum/01-foundations.yaml` lines 594-603, same keys in `curriculum.json`) are grouped
into five lessons so that each lesson owns 1-3 concepts. Hours are set in the hours section and must sum to 50.

| Lesson | Title (working) | Concepts it defines (from `introduces`) | Lab twin(s) | Owner | Study h |
|---|---|---|---|---|---|
| L01 | Distributions and robust summaries | `empirical-distribution`, `robust-statistics` | `lab-S0-L01-1`: empirical distribution and histogram of `fx_daily` log returns; mean vs median vs trimmed mean under one planted outlier (real data, `data-files="fx_daily.csv"`) | Builder A | 8 |
| L02 | Quantile diagnostics and outliers | `qq-plot`, `outlier-detection` | `lab-S0-L02-1`: Q-Q plot of standardized `ust_daily` daily changes against the normal reference; robust (MAD) outlier flags (real data, `data-files="ust_daily.csv"`). Needs M4 (Blocking issue 1) | Builder A | 7 |
| L03 | Missing data: mechanisms and what they do to estimates | `missing-data-mechanisms` | `lab-S0-L03-1`: MCAR, MAR and MNAR deletion on a SIMULATED return panel; bias of the sample mean under each (SIMULATED label) | Builder B | 6 |
| L04 | Prices as data: stale prices and corporate-action breaks | `stale-price`, `corporate-action-break` | `lab-S0-L04-1`: stale-run detection and a split-adjustment error on a SIMULATED price series (the curriculum's "spotting a split-adjustment error"); honest-pending note for real equity data | Builder B | 8 |
| L05 | Graphical perception and misleading charts | `graphical-perception`, `anscombes-quartet`, `misleading-chart` | `lab-S0-L05-1`: Anscombe's quartet (the curriculum's first lab); **blocked on source values**, see Open question 3. If blocked, the lab must be labelled as a constructed SIMULATED set and must not claim it is Anscombe's data | Builder B | 6 |
| hub | Hub: module map, prerequisites, hours, placement, ladder | none | none | Builder A | (not counted) |
| project | Atlas A3: data-quality reports (autograder) | none | `lab-S0-project-1..3` (rungs 1-3) | Builder C | 15 (project) |
| grader | `grader/reference.py`, `starter.py`, `instance.py`, `test_project.py` | none | none | Builder C | (in project) |
| cards | `cards.json`: one card per misconception and key result of L01-L05 | none | none | Builder D (after A-C) | (not counted) |

Hours: lessons 8 + 7 + 6 + 8 + 6 = **35 h**; project **15 h**; total **50 h** = curriculum (line 588). Each lesson is
inside 6-12 h (`tools/check_pages.py` line 227-228). The project share is 15/50 = 30%, inside 10-40%
(`check_pages.py` lines 339-340). The hub declares `data-hours-lessons="35"` and `data-hours-project="15"`.

Lab-coverage note: the curriculum's single `lab` string (line 608) names two experiments. Their homes are L05
(Anscombe's quartet) and L04 (split-adjustment error). The other lessons' labs are planner proposals, not curriculum
items; the architect should confirm them.

Builder count: S0 is smaller than AC2 (5 lessons, not 8), so three builders plus a cards builder is enough.
Builder A also writes the hub. Builder D writes cards only after A-C report.

## Project ladder and grader design (Builder C)

**Grading mode:** `autograder` (curriculum line 615). `check_projects.py` requires the spec's grading entry to contain
the word "autograd" and the grader directory to exist. No rubric is needed; the curriculum does not ask for one.
Atlas project: contract `atlas/A3.contract.md` is a prerequisite (Blocking issue 3).

**Ladder (BLUEPRINT §5; BUILDER_RULES §5.1; `check_projects.py` RUNGS):**
- Rung 1, worked example: fully solved and annotated profiler on a small generated dataset (SIMULATED), with the rule
  behind every step. Planned time 1.5 h.
- Rung 2, completion: the same profiler with `___` blanks in `flag_stale_prints` and `flag_gaps`; the lab is
  `class="lab completion"`, its twin is the completed solution. Graded instantly. Planned time 1.5 h.
- Rung 3, independent project: the Atlas A3 deliverable, `profile(dataset) -> report` flagging gaps, outliers, stale
  prints and corporate-action breaks on any Atlas dataset, to `atlas/A3.contract.md`. Planned time 10 h.
- Rung 4, stretch: apply the profiler to the cleared `fx_daily` and `ust_daily` snapshots and state a hypothesis
  about holiday gaps (FX rows are absent on New York holidays per `tools/data_sources.yaml` lines 28-30). Not
  graded; portfolio item. Planned time 2 h (not counted in the 15 h, or counted as stated by the architect).
  Total of rungs 1-3 = 13 h, plus 2 h stretch if counted; the spec must state which. Hours to be re-estimated by the
  builder and checked by the verifier (VERIFIER_RULES §2.6, 30% tolerance).

**Grader files (AC2 pattern, `course/modules/AC/AC2/grader/`):**
- `instance.py`: `make_instance(seed: int) -> dict` generating a SIMULATED price-and-volume style table with planted
  gaps, a run of stale prints, an unadjusted split (e.g., a ratio jump with no adjustment factor), an outlier and a
  corporate-action break. Deterministic per seed; every seed gives a valid instance with materially different answers.
- `reference.py`: the full solution; must pass `run_graders.py --unit S0 --seeds 0-49`.
- `test_project.py`: property and number tests: each planted defect is found at the right index; no false flags on
  clean data; invariants (flag indices within range; a split is not reported as an outlier); edge cases (empty table,
  all-missing column) fail loudly with a named property. Each test under 5 s in Pyodide.
- `starter.py`: the rung-2 completion skeleton with blanks.
- Failure messages name the violated property and give a concept hint; they never print the answer (BLUEPRINT §5.3).

**Mutants (at least 3 required; planner's candidate list for Builder C and verifiers):**
1. Stale-print detection with an off-by-one run length (flags runs one short).
2. Outlier rule uses mean and standard deviation instead of the median and MAD, so the outlier masks itself.
3. Split treated as an outlier and not as a corporate-action break (wrong classification).
4. Missing values read as zero returns instead of being reported as gaps.
5. Hard-coded answer for seed 0.

## Cards builder (Builder D)

`course/modules/S/S0/cards.json`, ids `S0-c001` upward, shape `{"id","lesson","front","back"}` as in AC2. One card per
definition (10 concepts), per key result with its grade, and per misconception (BUILDER_RULES §7). Cards for a graded
result cite registry keys or `basis` (for example `"basis": "Lab L04-1 (SIMULATED)"`). Every lesson L01-L05 must have
at least one card (`check_pages.py` lines 395-398). Cards are generated from the finished lessons only.

## Hub (Builder A)

`course/modules/S/S0/index.html` with `data-hours-lessons="35" data-hours-project="15"` in `<main>`, 4-8 measurable
objectives, prerequisites (CS1 link; and M4 and CS3 only if the architect applies Blocking issues 1-2), placement quiz
with `data-mastery="0.8"` (the AC2 value, `course/modules/AC/AC2/index.html` line 68; the S0 value is an architect
choice), lesson map linking L01-L05, and the four-rung ladder. Concept placement is a `<dfn>` in lessons only.

## Registry keys the module may cite

Verified in `references/references.json` by the planner (read directly from the file):

| Key | Work | Identity | Status | Note |
|---|---|---|---|---|
| `tukey1977exploratory` | Tukey, *Exploratory data analysis* (1977), book | OpenLibrary, ISBN 0201076160, publisher Addison-Wesley | verified; `used_by: [S0]` | Curriculum source 1 (line 605) |
| `anscombe1973graphs` | Anscombe, "Graphs in Statistical Analysis", *The American Statistician* 27(1), pp. 17-21 | DOI 10.1080/00031305.1973.10478966 (Crossref) | verified; `used_by: [S0]` | Curriculum source 2 (line 606) |
| `cleveland1984graphical` | Cleveland & McGill, "Graphical Perception...", *JASA* 79(387), pp. 531-554 | DOI 10.1080/01621459.1984.10478080 (Crossref) | verified; `used_by: [S0]` | Curriculum source 3 (line 607) |

Candidates in the registry that are not S0 sources (usable only after the builder reads the paper and grades it):
- `shumway1997delisting` (Shumway, "The Delisting Bias in CRSP Data", *J. Finance* 52, pp. 327-340; DOI
  10.1111/j.1540-6261.1997.tb03818.x; verified; `used_by: [F1]`). Possibly relevant to MNAR missingness in returns (L03).
  Requires a read of the paper before any claim is made.
- `panko1998we` (spreadsheet errors; `used_by: [CF7]`). Relevant to data-quality error rates only if the builder
  reads it. Optional.

Not in the registry and therefore `REFERENCE_REQUESTS` (no bibliographic data typed here; the architect resolves them
through `tools/add_reference.py`):
- A textbook or primary source for robust location and scale (median, MAD, trimmed mean) (`robust-statistics`).
  Confidence the architect should check: low that any single title is correct.
- A primary source for MCAR/MAR/MNAR (`missing-data-mechanisms`). Confidence: low.
- A primary source on stale prices and non-synchronous trading (`stale-price`). Confidence: low.
- A source for corporate-action adjustment of price series (`corporate-action-break`). Confidence: low.
- A source for misleading-chart devices beyond the curriculum's three (`misleading-chart`), including a published
  experimental replication or challenge to Cleveland & McGill's ranking, needed to meet the two-sided rule
  (BLUEPRINT §3: a graded B or C claim must name counter-evidence). Confidence: low.

## Claim grades the planner expects (for builders to confirm, not to copy)

- Cleveland & McGill's perception ranking: a single experimental study (`cleveland1984graphical`). Grade B at most
  until a replication is in the registry; counter-evidence must be named (REFERENCE_REQUESTS above).
- Tukey (1977): methods book; claims about EDA practice are D or C unless tied to a locator.
- Anscombe (1973): the quartet's construction and summary-statistic coincidence are the paper's claim; the values
  themselves must be confirmed against the paper at a locator before quoting them (Open question 3).

## Real-data and SIMULATED plan (summary)

| Lesson / lab | Data | Label |
|---|---|---|
| L01-1 | `fx_daily.csv` (cleared, Board H.10) | real; source line with licence and MANIFEST retrieval date |
| L02-1 | `ust_daily.csv` (cleared, Board H.15; Treasury series) | real; source line with licence and retrieval date |
| L03-1 | generated panel | SIMULATED |
| L04-1 | generated prices with planted stale runs and an unadjusted split | SIMULATED; honest-pending note for real equity data |
| L05-1 | Anscombe values (pending) or a constructed set | blocked; SIMULATED if constructed |
| Project | generated instances per seed; rung 4 uses `fx_daily` / `ust_daily` | SIMULATED for graded instances; real for stretch |

No equity price file is cleared. No Shiller, French or CRSP data may be embedded.

## Commands to check this unit (exact)

From `/Users/billyribeiro/dev/quant-phd`:

```bash
python3 tools/check_pages.py --unit S0              # now: FAIL, "S0 is not built"
python3 tools/check_dag.py --unit S0                # now: FAIL, 10 undefined introduced concepts
python3 tools/check_projects.py --unit S0           # now: FAIL, "project.html is missing"
python3 tools/run_labs.py --unit S0                 # now: PASS (0/0)
.venv/bin/python tools/run_graders.py --unit S0 --seeds 0-49   # system python3 lacks NumPy; use .venv
.venv/bin/python tools/check_pages.py --page L01 --unit S0     # while lessons are in progress
.venv/bin/python tools/run_labs.py --unit S0 --page L04        # per page
.venv/bin/python tools/mutate_graders.py --unit S0 --seeds 0-9 # verifier only (VERIFIER_RULES §2.6)
```

Full gate (once, before merge; not per builder): `ruff check .`, `ruff format --check .`, `mypy`, the S0 tests,
`render_curriculum.py` diff check, `build_site.py --check`, `verify_refs.py --offline`, `fetch_data.py --check`,
`check_pages --all`, `check_dag --all`, `check_projects --all`, and `page_smoke.py --unit S0` by a verifier only.

## Tooling assumptions that do not hold for S0 (report to architect)

- **Autograder: the assumption holds** (curriculum line 615 says `autograder`), so no rubric is needed. This is not a
  foundations module with no autograder. Note the curriculum's grading value is `autograder` only, not `both`.
- **`run_labs.py --unit S0` reports 0/0 today**; the check is vacuous until lessons exist.
- **`run_graders.py` needs the project venv** (NumPy); the system `python3` fails with `ModuleNotFoundError`.
- **`check_projects.py` requires `atlas/A3.contract.md`**, which is absent (Blocking issue 3).
- **Cumulative Atlas suite (BUILDER_RULES §5.5.3)** has no A1 or A2 code to run against; the A3 suite can test only
  A3 until CS1 and CS3 produce code.
- **`check_pages.py` hub split** requires lessons 35 h + project 15 h = 50 h; any change in lesson count must keep
  each lesson 6-12 h.
- **Pyodide runtime:** pandas is not in the AC2 list (NumPy, SciPy, standard library); S0 labs will need pandas for
  `fx_daily` handling unless the builder uses the standard library csv module. The curriculum's CS1 introduces
  pandas (`pandas-index-alignment`, `curriculum.json` CS1 introduces), so use is allowed by the DAG, but Pyodide
  support must be confirmed by `run_labs.py` / `page_smoke.py`.

## After the builders

1. Architect resolves Blocking issues 1-3 and Open questions below; orchestrator integrates; runs the unit gates once.
2. Independent Haiku verifiers (VERIFIER_RULES; slices: L01-L03, L04-L05, project with at least three mutants,
   cards). Verifier scripts archived under `ledgers/S0/scripts/`.
3. Branch merge only when the unit ledger is PASS or its gaps are agreed. Never merge incomplete.

## Open questions for the architect

1. **DAG (Blocking 1):** add `M4` to S0's prerequisites (recommended), or restrict S0's lessons so they need no M4
   concept? Also confirm whether plain "median" and "mean" are elementary (they are not in the concept index; the
   planner did not find an entry for them).
2. **Atlas A3 dependencies (Blocking 2):** add `CS3` to S0's prerequisites, or define A3's input as an in-memory
   table? The Atlas store is A2 (CS3), not S0.
3. **Anscombe's quartet values:** the lab needs the four datasets. Can the architect obtain
   `anscombe1973graphs` (pp. 17-21) so a builder can cite a table locator? Otherwise the lab must be a constructed,
   SIMULATED set that does not claim to be Anscombe's data. Which option?
4. **Atlas A3 contract:** draft `atlas/A3.contract.md` (module paths, signatures, types, units). The curriculum's
   project text (`01-foundations.yaml` lines 610-616) is the only specification found; it contains no signatures.
5. **Equity data:** no cleared equity price file exists. Accept SIMULATED labs and a `DATA_REQUESTS` entry, or
   identify a source whose issuer states redistribution rights (BLUEPRINT §5.3 candidates are not cleared)?
6. **Hours:** accept the 8/7/6/8/6 lesson split with a 15 h project (30%), or prefer six lessons? Six lessons would
   require a concept move or an extra lesson; the planner does not recommend it.
7. **Rung 4 hours:** counted in the 15 h or outside it?
8. **Placement mastery bar** for the hub (`data-mastery`): AC2 uses 0.8; the S0 value is an architect choice.
9. **Registry gaps:** approve the `REFERENCE_REQUESTS` above for lookup via `tools/add_reference.py`.

## Requests (to be filled by the builders' reports)

- REFERENCE_REQUESTS: as listed in the Registry section (robust statistics; missing data; stale prices; corporate-action
  adjustment; misleading charts and a perception replication).
- DATA_REQUESTS: a cleared equity daily price file with split and dividend adjustment factors (source URL, licence
  quote, transform).
- CONTRACT_CHANGE_REQUESTS: none yet; the A3 contract is missing rather than changed.
- DAG_DEFECTS: Blocking 1 (M4 concepts not in S0's closure) and Blocking 2 (CS3 store not in S0's closure).
