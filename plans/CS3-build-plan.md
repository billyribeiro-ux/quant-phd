# CS3 build plan: Data, Databases & SQL (planner output, 2026-10-28)

Unit: **CS3 · Data, Databases & SQL** · tier F · 80 h · prerequisites CS1 · Atlas milestone **A2** (data layer) ·
grading `autograder` · output directory `course/modules/CS/CS3/` (part code `CS`).
Planner: Haiku, plan only. No lesson content, no git operations, no commit. Executors: Haiku builders, then independent
Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

**Status: BLOCKED for the project (Atlas A2 contract missing) and for the L04 curriculum lab (runtime not supported).
Lessons L01-L03 and L05-L08 can start. See §9.**

## 0. Curriculum facts (file and line read during planning)

| Fact | Evidence |
|---|---|
| Entry CS3: id, title "Data, Databases & SQL", tier F, hours 80, prereqs [CS1] | `curriculum/01-foundations.yaml:450-454` |
| Core text: relational model, SQL, joins, window functions, ASOF joins, indexing, columnar storage, Parquet, DuckDB | `curriculum/01-foundations.yaml:455-457` |
| Nine introduced concepts, one per entry | `curriculum/01-foundations.yaml:458-467` |
| Sources: Codd (1970), *Communications of the ACM* 13(6); Raasveldt & Mühleisen (2019), 'DuckDB: an Embeddable Analytical Database', Proceedings of the 2019 International Conference on Management of Data | `curriculum/01-foundations.yaml:468-470` (free text; cite registry keys only, §6) |
| Lab: "ASOF JOIN of trades to quotes in DuckDB-WASM." | `curriculum/01-foundations.yaml:471` |
| Project: "Atlas A2: data layer", deliverable "Atlas at milestone A2.", grading `autograder`, `atlas: A2` | `curriculum/01-foundations.yaml:472-480` |
| No `debate` key on CS3 (so no debate brief; `check_pages.py` line 412 keys on `u.entry.get("debate")`) | `curriculum/01-foundations.yaml:450-480` (absent) |
| JSON row mirrors the YAML (hours 80, prereqs ["CS1"], nine introduces, sources, lab, project grading autograder, atlas "A2") | `curriculum/curriculum.json` `parts[2].modules[2]` |
| Nine concepts assigned to module CS3 in the concept index | `curriculum/curriculum.json` `concepts` (keys listed in §3) |
| Atlas A2 row: module CS3, "Data layer", delivers "DuckDB store, point-in-time schema, ingestion for FRED / French / Shiller / Treasury / EDGAR, data manifest with hashes." | `curriculum/meta.yaml:203-206` (A2 entry starts line 203); `CURRICULUM.md:169` |
| CS1 prereqs [P0.1]; CS1 introduces 12 concepts (the closure's Python concepts) | `curriculum/01-foundations.yaml:382-402` |
| P0.1 has no prereqs and introduces 11 concepts (incl. evidence grade, Atlas platform, citation registry) | `curriculum/01-foundations.yaml:6-30` |
| Registry keys with `used_by: ["CS3"]`: `codd1970relational` (Crossref, DOI 10.1145/362384.362685, Communications of the ACM 13(6), pp. 377-387) and `raasveldt2019duckdb` (Crossref, DOI 10.1145/3299869.3320212) | `references/references.json` entries (verified by planner) |
| Topological order: CS3 at position 8, after CS1 (3) and P0.1 (0) | `curriculum/curriculum.json` `topological_order` |
| Hours are consistent with the tool rules (see §4): 80 = 64 lessons + 16 project (20%) | derived; no conflict, so no STOP |

Not in the curriculum (stated plainly): no page-level reading list beyond the two sources; no named dataset for the
lab; no rubric; no debate; no DuckDB version; no Parquet specification source; no SQL standard source; no data
redistribution statement.

## 1. Rules for every builder (binding; BUILDER_RULES adapted to CS3)

- Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `VERIFIER_RULES.md` §2, this file. Study
  `course/modules/M/M1/` (lesson structure, cards, grader), `course/modules/AC/AC2/` (lab-id and Atlas-free conventions),
  `course/modules/AC/AC4/` (`both`/autograder panel) and `course/modules/S/S7/` (reference template). Imitate structure,
  not wording.
- **Evidence.** Every claim carries a grade (T/A/B/C/D/X) and a registry key. The only CS3 keys are
  `codd1970relational` and `raasveldt2019duckdb` (§6). Neither planner nor builder has read either paper in this plan:
  **a builder cites a number, a table, a figure or a quotation from either source only after reading the locator in the
  paper or in a source that reproduces it.** Otherwise the statement is a derivation on the page or is left out.
  Attribute only what the abstract or the paper states; state the sample, system and version. A claim about DuckDB
  behaviour that is not in the paper is cited to DuckDB's own documentation only if that document is in the registry
  (it is not, §6), so it is written as a description of the implementation under test, with the version pinned.
- **Derivations are grade T** when they are algebraic or set-theoretic (for example, the closure of a relation under
  selection and projection, or the window frame identity). Full proof on the page. Do not cite a textbook for a result
  the page derives.
- **Concepts.** Each of the nine concepts in §3 is defined exactly once, `<dfn id="def-<id>" data-concept="<id>">`, in
  its assigned lesson. Prerequisite concepts (CS1 and P0.1, §5) are usable without definition and linked to
  `../../../concepts.html#<id>`. Earlier CS3 lessons link `Lnn.html#def-<id>`. A lesson never links a later definition.
- **Labs.** Code lives once, in its twin `tests/labs/CS3/lab-CS3-Lnn-1.py` (lesson number, display order). The page carries
  `@@LAB:<file>@@` and `@@OUT:<file>@@`, and `tools/embed_labs.py` fills them. Never type expected output. Labs are seeded
  (`random.Random(seed)`), use the standard library plus NumPy and pandas only where the lab needs them (both are in
  Pyodide per CS1), need no network, run under 10 s in Pyodide, and print the same bytes under CPython.
  **Every twin calls `main()` at module top level** (no `if __name__ == "__main__":` guard), so the Pyodide runner and
  CPython print the same output. Lab ids match `lab-CS3-<page>-<n>` (`check_pages.py` line 258).
- **Scope words need a computation.** Each of "always", "never", "every", "all", "guarantees", "faster", "optimal", "safe"
  and "no look-ahead" must be backed by a lab run, a proof, or a counted quantity in the same section. "Faster" must be
  backed by a counted quantity (rows read, comparisons, bytes), never a wall-clock time, because timings are not
  reproducible under Pyodide.
- **Numbers recomputed from unrounded values.** Any number printed in a readout or table is computed from unrounded
  intermediate values, and the page states the rounding used.
- **Lab statements match code and output.** The hypothesis states the expected result before the run. The
  interpretation says what the output does not show.
- **Define before use.** Terms outside §3 and §5 (for example SHA-256, B-tree, normalization, primary key, foreign key,
  transaction, ACID, seeded randomness) are plain prose. They are not `<dfn>`-marked (check_dag rejects a definition for a
  concept the module does not introduce, AC4 precedent Q4).
- **Proposition hypotheses explicit.** Every proposition states its hypotheses in the statement: for the ASOF rule, that
  the right-hand table is sorted by time within each key, and the tie rule (strict or non-strict inequality) is stated.
- **Grader tests demand an exception type only for conditions the page names.** A test asserts a specific exception class
  only when the spec names that condition (for example, "a negative row count raises `ValueError`"). For every other
  invalid input the test asserts only that some exception is raised with a message naming the violated property. Every
  test must pass five alternative correct implementations (§7.5).
- **Money in integer cents.** Any amount of money (notional, cost, fee, size in currency) is a Python `int` count of
  cents, never a `float`. Prices of securities are stored as `decimal.Decimal` strings in the fixtures, with the tick
  size stated. The i64/BIGINT rule of BUILDER_RULES applies to Rust, PG and TS; the same discipline is applied here.
- **No horizontal scroll at 360 px.** Wide SQL result tables and labs' printed output must wrap or use a scrollable
  container that is not the document. `page_smoke.py` (line 341) fails on `document.documentElement.scrollWidth`
  exceeding the viewport. Builders keep code and tables within 360 px by line length and column count, and the page
  smoke check is the verifier's.
- **Labs call `main()` at top level** (see the labs rule above).
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`,
  `course/concepts.html`, `course/assets/data/*.json`, `references/*.json`, `course/assets/data/market/MANIFEST.json`,
  `course/assets/vendor/LOCK.json`). Never edit `curriculum/*.yaml`.
- Banned strings (BUILDER_RULES §1.3-1.4) in all prose: TODO, TBD, lorem, "for brevity", "it is important to note",
  "studies show", "it is well known", "obviously", "clearly", "beyond the scope".
- Do not run `page_smoke.py` (verifiers run it on a quiet machine). Targeted checks only (§8).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap or request in the
  BUILDER_RULES §10 output contract.

## 2. Outline and file ownership (proposed; the architect fixes it)

Hours: lessons 64 + project 16 = 80 (curriculum `curriculum/01-foundations.yaml:453`). Eight lessons of 8 h, each inside
the 6-12 h rule (`check_pages.py` lines 221-228). Project 16 h = 20% (inside 10-40%, `check_pages.py` lines 339-340).
Lessons sum to hub `data-hours-lessons="64"` (`check_pages.py` line 341).

| Lesson | Title (working) | Concepts it defines (§3) | Lab twin id (`tests/labs/CS3/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | The relational model | `relational-model` | `lab-CS3-L01-1.py`: relations as sets of tuples; selection, projection, natural join on a SIMULATED table; closure check | 8 | Builder A |
| L02 | SQL joins | `sql-join` | `lab-CS3-L02-1.py`: inner, left, right and full join row counts on generated key multisets, with the duplicate-key multiplication identity checked | 8 | Builder A |
| L03 | SQL window functions | `sql-window-function` | `lab-CS3-L03-1.py`: rolling sum by `ROWS BETWEEN` frame, checked against a self-join reference | 8 | Builder A |
| L04 | ASOF joins | `asof-join` | `lab-CS3-L04-1.py`: the curriculum lab, trades to the last prior quote, with the tie rule stated (see §9 BLOCK-2 on runtime) | 8 | Builder B |
| L05 | Point-in-time data | `point-in-time-data` | `lab-CS3-L05-1.py`: a generated revision history; as-of reads versus latest-value reads, count of look-ahead rows | 8 | Builder B |
| L06 | Database indexes | `database-index` | `lab-CS3-L06-1.py`: a sorted-key index versus a full scan, counted in comparisons and rows touched (not seconds) | 8 | Builder B |
| L07 | Columnar storage and the Parquet format | `columnar-storage`, `parquet-format` | `lab-CS3-L07-1.py`: row layout versus column layout, bytes touched for a one-column query; Parquet structure in the open question (§9 Q4) | 8 | Builder C |
| L08 | The data manifest | `data-manifest` | `lab-CS3-L08-1.py`: a manifest of generated snapshots with SHA-256 over bytes; a single flipped byte is detected | 8 | Builder C |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 64 / 16 | none | none | - | Builder A |
| project | Atlas A2: data layer (autograder) | none | `lab-CS3-project-1..3` (rungs 1-3) | 16 | Builder D |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` | none | none | - | Builder D |
| cards | `cards.json` from L01-L08 | none | none | - | Builder E (after A-C) |

Concept coverage: 1+1+1+1+1+1+2+1 = **9**, each in exactly one row, matching the nine entries at
`curriculum/01-foundations.yaml:458-467`.

Ordering: L04 defines `asof-join` before L05 uses it for the point-in-time read. L06 precedes L07 (an index is a
physical structure; the columnar lesson contrasts it with a row layout). L08 uses the Parquet file of L07 as a snapshot
format. No lesson links a later definition.

## 3. Concepts (from `curriculum/01-foundations.yaml:458-467`; `curriculum.json` concepts with `module: CS3`)

| Concept id | Name (curriculum) | Lesson |
|---|---|---|
| `relational-model` | Relational model | L01 |
| `sql-join` | SQL joins | L02 |
| `sql-window-function` | SQL window functions | L03 |
| `asof-join` | ASOF join | L04 |
| `point-in-time-data` | Point-in-time data | L05 |
| `database-index` | Database index | L06 |
| `columnar-storage` | Columnar storage | L07 |
| `parquet-format` | Parquet file format | L07 |
| `data-manifest` | Data manifest (source, licence, retrieval time, hash) | L08 |

## 4. Hub (`index.html`, Builder A)

- `<main data-hours-lessons="64" data-hours-project="16">`.
- 4-8 measurable objectives. Prerequisites: CS1 (linked, with its concepts), and the P0.1 concepts the lessons use.
- Placement diagnostic: `<section class="quiz" id="placement" data-unit="CS3" data-page="placement" data-mastery="0.8">`,
  matching the AP1 and M1 bar. At least two `data-skill` items test what rungs 1-2 teach (the worked example's query and
  the completion problem's missing join condition). The rest test CS1 (types, functions, pandas index alignment).
- Lesson map linking L01-L08. Project ladder with four rungs (`ol.ladder`).
- Tier F keeps rungs 1-2 at full length (BLUEPRINT §4: minimum from tier M upward).
- Hub must not claim a DuckDB-WASM run anywhere until §9 BLOCK-2 is resolved.

## 5. Prerequisite closure and DAG

Closure: CS1 (`prereqs: [P0.1]`, `curriculum/01-foundations.yaml:386`) and P0.1 (no prereqs, `:6-30`). Usable without
definition:

- From CS1 (`curriculum/01-foundations.yaml:391-402`): `python-function-scope`, `python-data-structures`,
  `python-class`, `structural-protocol`, `type-hints`, `python-exceptions`, `python-modules-packages`,
  `numpy-vectorization`, `pandas-index-alignment`, `simple-return`, `log-return`, `unit-test`.
- From P0.1 (`:9-26`): `evidence-grade`, `paper-anatomy`, `identification`, `robustness-check`, `replication`,
  `steelmanning`, `project-ladder`, `prerequisite-dag`, `atlas-platform`, `citation-registry`, `notation-conventions`.

Outside the closure, do not link or define: CS2 (algorithms: B-trees and sorting are CS2 territory, so the index lesson
uses only prose and the CS2 concept is not named as a concept), CS4 `deterministic-computation` ("seeded randomness"),
`continuous-integration`, `property-based-testing`, `dependency-pinning`, `bit-for-bit-reproducibility`. The labs may
call `random.Random(seed)` but must not link or define CS4's concept.

DAG risks to check: the project's `data-manifest` and `point-in-time-data` are CS3 concepts used in the project page;
the project page is after the lessons, so the links are `Lnn.html#def-<id>` (legal). Other modules'
`curriculum/04-quant.yaml:26` and `:572-585` use point-in-time and ASOF text; those modules are not in CS3's closure
unless their prerequisites include CS3 (`curriculum.json` lists CS4 and QR1 as CS3 dependents). The planner did not
verify whether those are in topological order after CS3 (`topological_order` places CS3 at 8). `check_dag.py` decides;
flagged as §9 Q7.

## 6. Registry keys the module may cite

| Key | Status (planner read) | Use in CS3 |
|---|---|---|
| `codd1970relational` | verified, Crossref, DOI 10.1145/362384.362685, `used_by: ["CS3"]`, pages 377-387, vol 13 issue 6 | relational model (L01): the origin of the model, cited for the definition of a relation and for the claim the paper makes. Locators needed for any quotation |
| `raasveldt2019duckdb` | verified, Crossref, DOI 10.1145/3299869.3320212, `used_by: ["CS3"]` | DuckDB as an embeddable analytical engine (L07, L08, project). Cite for the design claim the abstract makes; no performance number without a verified locator |

Not in the registry (for the curriculum's free-text sources, no key exists): ISO/IEC 9075 (the SQL standard, window
functions and ASOF semantics are not in it), the Apache Parquet format specification, DuckDB documentation for ASOF
join and window frame semantics, the SQLite documentation. Each is a REFERENCE_REQUEST candidate (§10). The planner did
not verify any of them and types no bibliographic data here.

Other keys in the registry (`keshav2007read`, `dunlosky2013improving`) belong to P0.1 and may be cited for learning
claims only if the page makes them; they are not CS3 keys.

## 7. Project ladder and grader design (Builder D)

### 7.1 Spec and grading

- `project.html` names the grading as `autograder` in its spec; `check_projects.py` `GRADING_WORDS["autograder"]` requires
  the word "autograd" in the grading entry (`tools/check_projects.py` lines 37-50). No rubric is required; no exemplars.
- The spec contains Context (2-4 sentences), Inputs (MANIFEST IDs or generated fixtures; see §8), Required outputs
  (module names and signatures, §7.4), Constraints, Grading mode, and the reading list (registry keys in §6 only).
- `grader` panel: `data-unit="CS3" data-grader="grader/" data-suite="test_project.py" data-support="instance.py"
  data-solution="<name>" data-starter="starter.py"`. The solution file name is open (§10 Q5). Atlas path: see BLOCK-1.

### 7.2 Ladder (Builder D, `lab-CS3-project-1..3`)

1. **Rung 1, worked example** (`lab-CS3-project-1`): a fully solved, annotated load of one generated snapshot into a
   store, with the manifest row written, each step explained.
2. **Rung 2, completion** (`lab-CS3-project-2`, `class="lab completion"`): the same load with the ASOF lookup and the
   manifest hash step as `___`. Graded instantly. Its twin is the completed solution, and every line equals the twin's
   or contains a blank (BUILDER_RULES §6.1).
3. **Rung 3, independent project** (graded): the Atlas A2 data layer to the contract (BLOCK-1). `lab-CS3-project-3` is the
   rung-3 check.
4. **Rung 4, stretch** (not graded): an extra source adapter or a partitioned columnar layout with a stated hypothesis.

### 7.3 Time budget (declared 16 h; each row needs a one-line rationale on the page)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1 worked example | 1 | Read and annotate one load |
| Rung 2 completion | 2 | Fill the ASOF and hash steps, run the instant check |
| Store and point-in-time schema (tables, keys, as-of view) | 4 | Write the DDL and the as-of query; check against the reference |
| Ingestion adapters for five sources, offline fixtures | 4 | One parser per source shape (FRED, French, Shiller, Treasury, EDGAR); tested on fixtures |
| Manifest with hashes and a verifier | 3 | Source, licence, retrieval time, SHA-256 of bytes; tamper detection |
| Self-check against the grader | 2 | Run `pytest` locally and in Pyodide; fix |
| **Total** | **16** | Equals `data-hours-project` on the hub |

### 7.4 Required interface (proposed; frozen only when BLOCK-1 is resolved)

Frozen names are proposals: the Atlas contract is the authority. Until then the grader cannot be written against it.

- `atlas.dataset.store` (proposed module name, to be fixed by the contract): `open_store(path: str) -> Store`, where
  `Store` has `ingest(source: str, payload: bytes, retrieved: str) -> ManifestRow` and `asof(key: str, t: str) -> dict`.
- `make_instance(seed: int) -> dict` in `grader/instance.py`. Deterministic per seed; generates **fixture payloads** in the
  five source shapes plus the expected manifest and the expected as-of answers. Every fixture is labelled **SIMULATED**
  in its docstring.
- Money: any notional or fee is int cents. Quoted prices are `Decimal` strings with the tick size stated.

### 7.5 Tests (`grader/test_project.py`)

- Properties and numbers: the as-of lookup equals a brute-force reference on every seed; ingestion of each generated
  payload reproduces the expected row count and the expected sum of a numeric column (exact for ints, to a stated
  tolerance for decimals); the manifest hash equals SHA-256 of the stored bytes.
- Invariants: no look-ahead (no as-of answer uses a row with a time later than `t`); the manifest's retrieval time is not
  earlier than the payload's own timestamp; ingesting the same payload twice produces the same manifest row
  (idempotence).
- Edge cases: an empty right-hand table (the as-of answer is absent, not an error); ties at the same timestamp (the tie
  rule from the spec); a key with no prior quote.
- Failure behaviour: a payload whose bytes change after ingestion fails the hash check. A negative row count raises
  `ValueError` (the spec names this condition). For any other invalid input, the test asserts that some exception is
  raised and its message names the violated property. The test never asserts a specific exception class the spec does
  not name.
- **Five alternative correct implementations must pass** (BUILDER_RULES §5.3 applied to CS3). The verifier writes them:
  (1) a binary-search as-of over sorted lists; (2) a linear merge over sorted streams; (3) an in-memory dict of sorted
  lists with `bisect`; (4) a `pandas.merge_asof` wrapper; (5) a SQLite-backed store (standard library `sqlite3`) that
  does the as-of by a correlated subquery. Each must pass every test on seeds 0-49, or the test is over-specified.
- Hard-coded answers are forbidden: each expected value is recomputed from the instance's own generating parameters.
- Each test finishes under 5 s in Pyodide; the whole suite under 60 s (BUILDER_RULES §5.3.4).

### 7.6 Mutants (verifier; at least three, each must be killed)

1. Look-ahead: the as-of lookup uses `<=` on a later row or does not sort the right-hand table, so it returns a future quote.
2. Tie rule inverted: the lookup takes the first of two same-time quotes instead of the last, and the spec's tie rule
   is violated.
3. Hash of the wrong bytes: the manifest hashes the header line only, so a changed row is not detected.
4. Rounding breaks exactness: a decimal sum rounded before the total, so the total differs from the sum of rows.
5. Hard-coded answer for seed 0.

### 7.7 Starter

`grader/starter.py` raises `NotImplementedError` in every function; the suite must fail on it (`run_graders.py` checks this).

## 8. Real-data policy

- **No embedded real data in CS3 labs or the grader.** The curriculum names no dataset for the labs (`:471`). The project
  brief names five issuers (`:474-476`). Of those, only the Federal Reserve H.10 and H.15 releases are cleared for embedding
  (BLUEPRINT §5.3, lines 297-302; `tools/data_sources.yaml` ids `fx_daily`, `fx_monthly`, `ust_daily` are the three
  existing entries). Kenneth French and Open Source Asset Pricing are checked and not cleared (BLUEPRINT lines 303-309).
  Shiller and SEC EDGAR are candidates, not cleared (BLUEPRINT lines 310-317).
- Therefore the grader's ingestion adapters are tested on **generated fixtures in the five issuers' shapes, labelled
  SIMULATED**. The spec says that live ingestion is the student's own action, not embedded, not graded, and needs no
  network in grading.
- The labs use generated trades, quotes, revision histories and snapshots, each labelled SIMULATED on the page.
- BLOCK-1 applies to the project only. Lessons do not depend on it.
- No `data-files` attribute is needed on any lab, so no MANIFEST entry is needed for CS3 (`check_pages.py` line 163-184
  is vacuous). If the architect wants a cleared series (for example an H.15 yield) in a lab, that is a `DATA_REQUESTS`
  item, and the lab lists it in `data-files`.
- No `DATA_REQUESTS` entry is proposed by the planner.

## 9. Blocking issues and tooling assumptions that do not hold

### BLOCKING

- **BLOCK-1 · Atlas A2 contract is missing.** `atlas/` contains only `A8.contract.md` and `A15.contract.md`
  (`ls atlas`). The project names `atlas: A2` (`curriculum/01-foundations.yaml:480`), so `check_projects.py` lines 144-146
  will fail with "Atlas milestone A2 has no contract". The planner did not draft it (per the orchestrator's instruction).
  Architect must write `atlas/A2.contract.md`. The A1 contract (CS1's milestone, `CURRICULUM.md:168`, `curriculum/meta.yaml:199-202`) is also
  missing, and the cumulative A1-A2 suite cannot be run without it (VERIFIER §2.6). The A15 contract already says A2
  "will supply the loader that downloads and stores that JSON" (`atlas/A15.contract.md` lines 7-8), so A2's loader API
  is a cross-unit interface; the A2 contract must freeze it.
- **BLOCK-2 · The curriculum lab needs a SQL runtime that does not exist here.** The lab is "ASOF JOIN of trades to quotes in
  DuckDB-WASM" (`:471`). `tools/run_labs.py` lines 70-71 return "runtime ... has no local runner yet" for any runtime
  other than `python`. DuckDB-WASM is not vendored: no `duck` entry in `course/assets/vendor/LOCK.json` or
  `tools/vendor_spec.yaml` (planner grep, zero hits). BLUEPRINT line 347 says DuckDB-WASM "join[s] the lock file with the
  first SQL ... modules", which is this unit. Options in §10 Q1. L04 cannot pass `run_labs.py` as a `sql` lab until the
  architect decides.

### Unverified tooling assumptions (must be checked before builders rely on them)

- **U-1 · DuckDB in Pyodide.** The project's store is "a DuckDB store" (`:474`). Whether a DuckDB Python build runs in the
  Pyodide runtime is **not verified** by the planner. No `duckdb` or `pyarrow` entry appears in `course/assets/vendor/LOCK.json`
  (planner grep). If it does not run, the dual-mode grader (BUILDER_RULES §5.3.4) cannot use DuckDB in the browser, and the
  store must be a standard-library store. See §10 Q2.
- **U-2 · Parquet in Pyodide.** No `pyarrow` in the lock file. Whether any Parquet reader runs in Pyodide is unverified.
- **U-3 · `run_graders.py` solution path.** The panel's `data-solution` name is read by the tool; the AC4 plan notes
  `run_graders.py` takes the solution path from `atlas/` for Atlas units (`plans/AC4-build-plan.md` §9 item 1). CS3 is an
  Atlas unit, so its solution path resolution is the Atlas one, which needs BLOCK-1 resolved first.
- **U-4 · Units of the hub.** `check_pages.py` line 341 requires lessons to sum to the hub; the planner did not run the tool.

### Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

```bash
.venv/bin/python tools/check_pages.py --unit CS3             # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit CS3
.venv/bin/python tools/check_projects.py --unit CS3          # fails on BLOCK-1 until atlas/A2.contract.md exists
.venv/bin/python tools/run_labs.py --unit CS3                # --page L04 fails on BLOCK-2 until resolved
.venv/bin/python tools/run_graders.py --unit CS3 --seeds 0-49
.venv/bin/python tools/mutate_graders.py --unit CS3 --seeds 0-9   # verifier only
.venv/bin/python tools/embed_labs.py course/modules/CS/CS3/L01.html   # per page, after twins exist
.venv/bin/ruff check tests/labs/CS3 course/modules/CS/CS3/grader && .venv/bin/ruff format --check tests/labs/CS3
.venv/bin/mypy                                               # strict, repo configuration
```

Not run by builders: `page_smoke.py` (verifiers only). Architect-only gates before merge: `check_pages.py --all`,
`build_site.py --check`, `render_curriculum.py`, `verify_refs.py --offline`.

The planner did not execute any of these commands; flags are taken from the tools' code as read in `plans/AC4-build-plan.md` §8 and
`plans/M1-build-plan.md` §Commands, and are not re-verified for CS3.

## 10. Open questions for the architect

1. **(BLOCK-2) L04 runtime.** Choose one: (a) add a `sql` runner to `run_labs.py`, vendor DuckDB-WASM through
   `tools/vendor_spec.yaml` and `fetch_vendor.py`, and run the curriculum lab as written; (b) keep the lab `python`, run a
   pure-Python ASOF reference with the same tie rule, and show the SQL as a listing that is labelled not run (BUILDER_RULES
   §1.6: pseudocode is never styled as runnable), and state on the page that the curriculum's DuckDB-WASM lab is not run;
   (c) defer L04's lab. Planner recommends (b) for now, with (a) as a later unit of work, because (a) is a build-tool change.
2. **(U-1) Store engine in the grader.** Does the project store use DuckDB (requires confirming that it runs in Pyodide),
   or the standard-library `sqlite3` (runs everywhere, but then the deliverable "a DuckDB store" is not met)? The curriculum
   names DuckDB (`:474`), so the planner's default is DuckDB locally with a DuckDB-free grader path; the architect must confirm.
3. **(BLOCK-1) A2 contract.** Write `atlas/A2.contract.md` (and confirm A1's contract) before project work. Confirm the
   interface names in §7.4 or replace them. The planner did not draft it.
4. **(L07) Parquet lab.** Parquet needs a binary reader; no Parquet library is confirmed in Pyodide (U-2). Options: (a) the
   lab models row versus column layout by counted bytes of a generated table and describes the Parquet footer in prose
   without reading a file; (b) a pure-Python footer reader on a fixture file the lab cannot generate in Pyodide, which is not
   allowed; (c) request a Parquet library. Planner recommends (a).
5. **Solution file name.** Proposed `atlas_a2_store.py` or the name the A2 contract fixes; confirm after Q3. The reference
   stays excluded from deployment (BLUEPRINT §7).
6. **Hours split.** 64 lessons / 16 project (20%) with eight lessons of 8 h. Confirm. The alternative of seven lessons of
   about 9 h is possible, but puts two concepts in one lesson in the middle of the sequence.
7. **DAG (cross-unit).** `curriculum/04-quant.yaml:26` and `:572-585` use point-in-time and ASOF text for modules whose
   position is not confirmed to follow CS3 by the planner. Confirm with `check_dag.py`; if a module before CS3 uses these
   terms as concepts (not text), it is a DAG defect.
8. **Undeclared terms.** Hash, SHA-256, primary and foreign keys, transactions, normalization, B-tree are plain prose (§1).
   Confirm that "relational model" (`relational-model`) covers keys, so that keys need no separate concept.
9. **Integer cents and prices.** Confirm that quoted prices are `Decimal` strings and money is int cents (§1).
10. **Registry gaps.** Confirm whether the architect will request admission of the Apache Parquet specification, the SQL
    standard, and DuckDB's documentation through `add_reference.py` (REFERENCE_REQUESTS, §11). No CS3 claim may cite them
    until admitted.

## 11. REFERENCE_REQUESTS (candidates; not verified, no bibliographic data typed here)

- Apache Parquet format specification (needed for L07 if any footer layout is stated). DOI: unknown to the planner.
  Confidence the source is needed: high. Confidence in any citation string: none.
- ISO/IEC 9075 (SQL standard, window functions and joins). Confidence needed: medium. Identity: unknown to the planner.
- DuckDB documentation for the ASOF join and the window frame. Needed only if the page states DuckDB semantics. Identity: unknown.
- Codd (1970) and Raasveldt & Mühleisen (2019): already registered (§6), no request.

## 12. Verifier notes (for the CS3 verifier, VERIFIER_RULES §2)

- Row per lab, per number, per claim span, per proposition. Mutants per §7.6 (at least three; five recommended).
- The verifier reads the Codd and DuckDB records by their locators before citing them (§1).
- Verifier scripts archived under `ledgers/CS3/scripts/` (VERIFIER_RULES §3).

## 13. After the builders

1. Orchestrator integrates; resolves BLOCK-1 and BLOCK-2 first (architect); runs the §9 commands once; fixes DAG, links, hours.
2. Independent Haiku verifiers in fresh checkouts, slices: L01-L02, L03-L04, L05-L06, L07-L08, project.
3. Ledger at `ledgers/CS3.verification.json`; the branch is merged only when the ledger is PASS or its gaps are named and agreed.
