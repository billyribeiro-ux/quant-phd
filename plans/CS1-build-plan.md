# CS1 build plan: Haiku builders in parallel (2026-10-27)

Unit: **CS1 · Programming in Python from Zero** · tier F · 120 h · prerequisite P0.1 · Atlas milestone **A1**
(repository skeleton) · grading `autograder` · output directory `course/modules/CS/CS1/` (part code `CS`, per
`curriculum/curriculum.json` `parts[2]`, module `CS1` at index 0). Phase 2 fan-out (BLUEPRINT §9). Owner:
orchestrator (architect). Executors: Claude Haiku builders, then independent Haiku verifiers (VERIFIER_RULES).
A builder never verifies and never writes a ledger.

Evidence key used below: `C:<file>:<line>` = curriculum source line read; `R:<key>` = registry record read in
`references/references.json`; `T:<file>:<line>` = tooling line read.

## Source facts (all read in full or the cited span)

- Curriculum entry: `curriculum/01-foundations.yaml:382-415`. Hours `:385` (120); prereqs `:386` (`[P0.1]`);
  core `:387-389`; introduces (12 concepts) `:390-402`; sources `:403-405` (two free-text strings, not registry
  keys); lab `:406` ("Vectorized returns computation vs. loops: correctness and speed."); project `:407-415`
  (title "Atlas A1: repository skeleton", grading `autograder` at `:414`, atlas `A1` at `:415`).
- Atlas: `curriculum/meta.yaml:199-201` (`id: A1`, `module: CS1`, title "Repository skeleton", delivers
  "Typed Python package, CLI entry point, test harness, pre-commit, CI config."). **The contract file
  `atlas/A1.contract.md` does not exist** (`ls atlas/` shows only `A8.contract.md`, `A15.contract.md`). The
  AC2 precedent (`atlas/A15.contract.md`, drafted by the architect) therefore has to be repeated for A1.
- Curriculum JSON: CS1 is in `parts[2].modules[0]` (`curriculum/curriculum.json`); the 12 concepts each list
  `module: CS1` in `concepts` (checked for all 12 keys). The `topological_order` lists `CS1` after `P0.1, M1`.
- P0.1 (the only prerequisite): `C:curriculum/01-foundations.yaml:6-38` (hours 6). Its concepts do not overlap
  CS1's 12 concepts (checked by key).
- Curriculum `core` names topics that have **no concept key** in `introduces`: control flow, "types", "files",
  "errors" (as a topic; `python-exceptions` covers errors). See Open question Q3.
- Pyodide runtime: `T:tools/vendor_spec.yaml:53-59` pins Pyodide `314.0.7` with packages
  `[numpy, scipy, pytest]`. **pandas is not vendored.** The curriculum requires pandas (`C:...:398`,
  `pandas-index-alignment`; `C:...:389` "NumPy and pandas fundamentals"). See Open question Q1.
- Repo Python policy: `CLAUDE.md` says Python 3.14+. The registry's Python record is 3.13
  (`R:psfndpython`, `url https://docs.python.org/3.13/reference/index.html`), and the curriculum source says
  "Python 3.13 (primary)" (`C:...:404`). The Pyodide runtime is 314.0.7 (above). See Open question Q2.
- Module hours rules: `T:tools/check_pages.py:227-228` (lesson 6-12 declared hours); `:337-340` (hub
  `data-hours-lessons + data-hours-project` must equal curriculum hours; project 10-40%); `:341-342` (lesson
  hours must sum to the hub's lessons figure).
- Project rules: `T:tools/check_projects.py:33` (RUNGS = worked example, completion, independent, stretch);
  `:41-50` (grading words must match the curriculum mode); `:122-137` (autograder needs
  `section.grader-panel` with `data-unit data-grader data-suite data-solution data-starter`, and files
  `grader/<suite>`, `grader/starter.py`, `grader/reference.py`, `grader/instance.py` defining
  `make_instance(seed: int)`); time budget table `id="hours"` at `:~145-160` with a rationale per row.
- Cards rules: `T:tools/check_pages.py:57` (GRADES = TABCDX); `:366-397` (id `CS1-cNNN`, front and back required,
  `lesson` must exist, any `cite` must be a registry key, a non-T grade needs `cite` or `basis`, every lesson
  needs at least one card).
- Real data cleared for embedding: `course/assets/data/market/MANIFEST.json` datasets `fx_daily` (rows 6706,
  first 2000-01-03, last 2026-09-30, retrieved 2026-10-19, licence quoted, `licence_url`
  `https://www.federalreserve.gov/disclaimer.htm`, note: spot rates only, holidays have no row), `fx_monthly`
  (669 rows, 1971-01 to 2026-09), `ust_daily` (6690 rows, 2000-01-03 to 2026-09-30). The Federal Reserve
  licence quote is in `tools/data_sources.yaml` (lines 1-30 read).
- Finished modules read for structure: `course/modules/S/S7/` (hub `data-hours-lessons="70" data-hours-project="30"`,
  grader panel with `data-solution="atlas/integrity.py"`), `course/modules/AP/AP1/`, and `course/modules/AC/AC2/`
  (hub `data-hours-lessons="76" data-hours-project="34"`; lesson `<html data-unit data-page data-hours="9">`;
  grader panel `data-solution="atlas/fundamentals.py" data-packages="numpy"`; `cards.json` has id/lesson/front/back
  only). Templates: `course/templates/{hub,lesson,project,studio}.html` and `README.md` exist.
- Lab twins: `tests/labs/AC2/lab-AC2-L01-1.py` (naming pattern `lab-<UNIT>-<Lnn>-<n>.py`, and
  `lab-<UNIT>-project-<n>.py`). `tests/labs/CS1/` does not exist yet.

## Rules for every builder (binding; BUILDER_RULES adapted to CS1)

- Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `plans/AC2-build-plan.md`, this file,
  and `atlas/A1.contract.md` once the architect has drafted it (it does not exist yet; do not invent it).
  Study `course/modules/S/S7/` and `course/modules/AC/AC2/` as worked examples of template, labs, cards and grader
  layout. Imitate structure, not wording.
- **Foundations voice.** Students arrive knowing only P0.1 (how to study, evidence grades, DAG, a first Pyodide
  cell). Write for a reader who has never programmed. Every example is runnable in Pyodide and under CPython.
  Do not assume prior Python. Still no filler, no unsourced numbers, no TODO, no "left as an exercise".
- **Evidence standard.** Every substantive claim carries a grade (T/A/B/C/D/X) and a registry key, or a
  `basis` naming the lab or problem that establishes it (BUILDER_RULES §7). Language-semantics claims cite
  `psfndpython` with a `data-locator` (section name). Do not cite anything not in `references/references.json`.
  Programming-practice claims (for example, "unit tests catch regressions") are grade D unless a registry key
  supports them, and then they say so. Never type bibliographic data, a PEP number, or a section number from memory.
- **Concepts** are defined once, `<dfn id="def-<id>" data-concept="<id>">`, in the lesson assigned below. Every
  other use is `<a class="concept" data-concept="<id>" href="Lnn.html#def-<id>">` for an earlier lesson in
  CS1, or `href="../../../concepts.html#<id>"` for P0.1. A lesson never links a concept defined later.
- **No concept outside the list is defined.** Terms the curriculum core names but does not assign (control flow,
  files, types) are taught without a `<dfn>` and are logged in `GLOSSARY_REQUESTS` (Q3).
- **Labs.** Code lives once, in `tests/labs/CS1/lab-CS1-<Lnn>-<n>.py` (twin). Pages carry `@@LAB:<file>@@` and
  `@@OUT:<file>@@` markers; `tools/embed_labs.py` fills them. Never type expected output. Labs are seeded,
  network-free, under 10 s in Pyodide, and print no timing values (see Q4). Labs using a real dataset list it in
  `data-files` and open it as `data/<file>` (BUILDER_RULES §6.6).
- **Real data.** Only `fx_daily` and `ust_daily` (and `fx_monthly` if needed) are embeddable, because their
  issuer's quoted licence grants copying and distribution (`MANIFEST.json`, `tools/data_sources.yaml`). The
  builder must confirm the quote at `licence_url` before citing it (VERIFIER rule 2.8). Everything else is
  generated and labelled **SIMULATED** on every figure and lab that shows it.
- **pandas.** No pandas lab or grader ships until Q1 is resolved. A lesson that teaches pandas writes its lab
  against the curriculum requirement and marks the lab `class="lab pending"` with an honest-pending note naming
  the vendor gap. Do not claim the lab runs in Pyodide.
- No `git commit`, no push. Do not run `page_smoke.py` (timing-sensitive; verifiers run it on a quiet machine,
  AC2 precedent). Targeted checks only: `check_pages.py --unit CS1`, `check_dag.py --unit CS1`,
  `check_projects.py --unit CS1`, `run_labs.py --unit CS1`, `run_graders.py --unit CS1 --seeds 0-49`, `ruff`,
  `mypy` on your twins. Report exact commands and exact output. A check you did not run is reported as not run.
- Output contract: BUILDER_RULES §10 unchanged. Required additional entries: `GLOSSARY_REQUESTS` (Q3),
  `DATA_REQUESTS` (Q1), `CONTRACT_CHANGE_REQUESTS` (A1 contract missing, Q5).

## Outline and file ownership (fixed; do not move concepts between lessons)

Lesson hours follow the table in the next section. Each row's concepts are exactly the `introduces` keys assigned
to it; the twin id is the first lab; further labs (up to 4 per lesson) are optional.

| Lesson | Title (working) | Concepts it defines (from `introduces`) | Lab twin id | Owner | Real data (lab) |
|---|---|---|---|---|---|
| L01 | Functions, control flow and scope | `python-function-scope` | `tests/labs/CS1/lab-CS1-L01-1.py`: a function with a local, a global and a closure; the scope rule shown by output | Builder A | none (SIMULATED toy values) |
| L02 | Built-in data structures | `python-data-structures` | `lab-CS1-L02-1`: list, dict, set, tuple behaviour (mutability, hashing, membership cost stated as an operation count, not time) | Builder A | none |
| L03 | Classes and protocols | `python-class`, `structural-protocol` | `lab-CS1-L03-1`: a class with a method, and a structural protocol satisfied by a class that never names it (duck-typed call checked by output) | Builder A | none |
| L04 | Modules, packages and exceptions | `python-modules-packages`, `python-exceptions` | `lab-CS1-L04-1`: a two-module package imported, a `ValueError` raised and caught with the message checked | Builder B | none |
| L05 | Type hints and static checking | `type-hints` | `lab-CS1-L05-1`: annotated functions; the runtime does not enforce hints, so the lab shows the difference between a hint and a check | Builder B | none |
| L06 | Unit tests with pytest | `unit-test` | `lab-CS1-L06-1`: a small function and its pytest file run through the in-page suite (passing and one deliberately failing test) | Builder B | none |
| L07 | NumPy arrays and vectorization | `numpy-vectorization` | `lab-CS1-L07-1`: array shape, broadcasting and one reduction, checked against a loop for equal results | Builder C | SIMULATED seeded arrays |
| L08 | pandas DataFrames and index alignment | `pandas-index-alignment` | `lab-CS1-L08-1`: align `fx_daily` (EUR, JPY) with `ust_daily`, dropping holidays by index, not position. **Pending Q1** (pandas not vendored) | Builder C | `fx_daily.csv`, `ust_daily.csv` (cleared) |
| L09 | Simple and log returns; vectorized vs. loop | `simple-return`, `log-return` | `lab-CS1-L09-1` (the curriculum lab, C:`:406`): simple and log returns of EUR from `fx_daily`, vectorized and loop versions equal to 1e-12, and the identity `log(1+r) = log return` checked | Builder C | `fx_daily.csv` (cleared); spot rates only, per MANIFEST `note` |
| hub | Module hub | none | none | Builder A | none |
| project | Atlas A1: repository skeleton (autograder) | none | `lab-CS1-project-1..3` (rungs 1-3) | Builder D | none |
| grader | `grader/reference.py`, `starter.py`, `instance.py`, `test_project.py` | none | none | Builder D | SIMULATED seeded price paths |
| cards | `cards.json`: one card per definition, misconception and key result of L01-L09 | none | none | Builder E (after A-C) | none |

Coverage check: 12 concepts assigned, each to exactly one lesson (L01 1, L02 1, L03 2, L04 2, L05 1, L06 1, L07 1,
L08 1, L09 2 = 12). The concepts match `C:curriculum/01-foundations.yaml:390-402` and
`curriculum.json` `concepts` (each `module: CS1`).

Lesson count: **9**. The curriculum does not state a lesson count. The count is derived from the 6-12 hour rule
(`T:tools/check_pages.py:227-228`) and the 12 concepts, grouped by topic. This is a design choice, listed as Q6.

Lab-twin naming. BUILDER_RULES §6.1 says `tests/labs/<UNIT>/lab-<UNIT>-<page>-<n>.py`. The AC2 plan says
`tests/labs/AC2/<lab-id>.py`. Both produce `lab-CS1-L01-1.py`. Use the BUILDER_RULES form.

## Hours (sums to the curriculum's 120 h)

Per `C:curriculum/01-foundations.yaml:385` (120). Project share 36/120 = 30% (inside the 10-40% band,
`T:tools/check_pages.py:339`).

| Unit | Hours | Basis |
|---|---|---|
| L01 Functions, control flow, scope | 10 | First concept lesson; includes control flow and first functions |
| L02 Built-in data structures | 10 | Four containers, mutability, hashing |
| L03 Classes and protocols | 10 | Classes and a structural protocol |
| L04 Modules, packages, exceptions | 9 | Packaging is a prerequisite of the project skeleton |
| L05 Type hints | 9 | Hints, static checking, what the runtime does not check |
| L06 Unit tests | 9 | pytest on the lessons' own functions |
| L07 NumPy | 9 | Arrays, broadcasting, reductions |
| L08 pandas | 9 | Index alignment on real FX and rate calendars |
| L09 Returns | 9 | Simple and log returns; the curriculum lab |
| **Lessons total** | **84** | 10+10+10+9+9+9+9+9+9 |
| Project (Atlas A1) | 36 | Component table below |
| **Total** | **120** | = `C:...:385` |

Project time budget (table `id="hours"`, each row carries a one-line rationale; sums to 36):

| Component | Hours |
|---|---|
| Rung 1 worked example, annotated, read and run | 3 |
| Rung 2 completion problem, graded instantly | 3 |
| Package skeleton: src layout, `pyproject.toml`, importable package | 4 |
| Typed core module: `simple_return`, `log_return`, input validation | 5 |
| CLI entry point (argparse, exit codes, `--help`) | 4 |
| pytest suite: values, invariants, failure on bad input | 5 |
| Lint, format, strict type config, pre-commit | 4 |
| CI workflow running the same gates | 4 |
| Gate run record and zip export/import round trip | 2 |
| Repository hygiene: README, `.gitignore`, licence file | 2 |
| **Total** | **36** |

## Project ladder and grader design (Builder D; `grading: autograder`)

- Rung 1: a fully solved, annotated worked example of the typed core module and its tests on a generated path.
- Rung 2: a completion problem: the CLI `main` and `simple_return` with blanks (`___`); its twin is the completed
  solution; every line equals the twin or contains a blank (BUILDER_RULES §6.1). Class `lab completion`.
- Rung 3: the Atlas A1 repository, to the **A1 contract (to be drafted, Q5)**. Scope in the curriculum:
  "typed modules, a CLI, a pytest suite, formatting and linting config, and CI" (`C:...:407-412`). Rung 3 scope is
  not stricter than that sentence.
- Rung 4: optional stretch, for example a `log_return` edge-case study with a stated hypothesis. No ceiling, not hour-counted.
- Grader panel: `data-unit="CS1" data-grader="grader/" data-suite="test_project.py" data-support="instance.py"
  data-solution="<A1 module path, pending Q5>" data-starter="starter.py" data-packages="numpy"`. Pyodide
  packages: numpy only; pytest is vendored (`T:tools/vendor_spec.yaml:59`).
- `grader/instance.py`: `make_instance(seed: int) -> dict`; deterministic; each seed gives a different positive
  price path (length 5-60) and one invalid case from a fixed list; every valid instance has strictly positive
  prices (SIMULATED, labelled).
- `grader/reference.py`: the full solution. Must pass seeds 0-49 (`run_graders.py --seeds 0-49`).
- `grader/test_project.py` checks **properties and numbers**: simple vs. log values to 1e-12; `log_return == log(1+simple)`
  invariant; nonpositive price raises `ValueError`; CLI exit codes; `pyproject.toml` parses with `tomllib` and
  declares the entry point, strict mypy and ruff sections; CI workflow file exists and runs the gate commands
  (text check, since PyYAML is not in Pyodide).
- Feedback: failures name the property violated and give a concept hint; never the answer.
- Mutants the verifier must kill (at least 3; examples to seed the verifier's round): simple return computed as
  `log`; off-by-one lag in returns; no validation of nonpositive prices; CLI returns 0 on a bad argument.
- Dual mode: the identical suite runs in Pyodide and under local `pytest`. Each test under 5 s, suite under 60 s.

## Cards builder (Builder E; after A-C)

- `course/modules/CS/CS1/cards.json`; ids `CS1-c001` upward (`T:tools/check_pages.py:381`).
- One card per concept definition (12), per misconception (at least 3 per lesson, 27 total), and per key result
  or lab result. Expected total: 45-70 cards. Every lesson has at least one card (`T:tools/check_pages.py:396-398`).
- Fields: `id`, `lesson`, `front`, `back`; and `cite` (registry keys only, `T:...:389-391`) or `basis`
  (lab or problem name) for any non-T grade (`T:...:392-394`). The AC2 example omits `grade` and `cite`; the
  checker accepts that, so either form passes. Use BUILDER_RULES §7 fields.
- No trivia cards. Each back must be checkable against the lesson text.

## Hub (Builder A)

- `index.html` with `<main data-hours-lessons="84" data-hours-project="36">` (`T:tools/check_pages.py:332-342`).
- Objectives (4-8 measurable verbs), prerequisite link to P0.1, hours, placement test (per-module diagnostic on
  the hub; `data-mastery` and `data-skill` items, BUILDER_RULES §5.1), lesson map (L01-L09), project ladder.
- Each lesson page: `<html lang data-root="../../../" data-unit="CS1" data-page="Lnn" data-hours="<h>">`.

## Registry keys the module may cite (each verified to exist in `references/references.json` on 2026-10-27)

| Key | Record read | Use in CS1 | Caveat |
|---|---|---|---|
| `psfndpython` | issuer, verified; `url https://docs.python.org/3.13/reference/index.html` | language semantics (scope, data model, exceptions, modules) | 3.13 record; runtime is 3.14 (Q2) |
| `ramalho2021fluent` | Open Library, verified; year 2021 | idioms and protocols; cite as a book, not as a theorem | **Curriculum says "2022" (`C:...:405`); registry says 2021 and records the mismatch in `notes.year`.** Cite the registry record (2021); architect to decide (Q2b) |
| `harris2020array` | Crossref DOI 10.1038/s41586-020-2649-2, verified | NumPy arrays and vectorization (L07, L09) | none |
| `keshav2007read` | Crossref DOI 10.1145/1273445.1273458, verified | "how to read a paper" for P0-style pointers only | not needed for content |
| `dunlosky2013improving` | Crossref DOI 10.1177/1529100612453266, verified | retrieval practice (quizzes, cards) | none |
| `roediger2006test` | verified (in registry) | retrieval practice | none |
| `freeman2014active` | verified (in registry) | labs inline, active learning | none |
| `sweller1985use` | Crossref DOI 10.1207/s1532690xci0201_3, verified | worked examples (rung 1) | none |
| `kalyuga2003expertise` | Crossref DOI 10.1207/s15326985ep3801_4, verified | expertise reversal (skip rungs with placement) | none |
| `kirschner2006minimal`, `hmelosilver2007scaffolding` | verified (in registry) | scaffolding, project ladder | none |

Keys not in the registry and not usable until added (see REFERENCE_REQUESTS): Python Enhancement Proposals
(typing and protocols), pytest documentation, pandas documentation or the pandas paper, NumPy documentation beyond
`harris2020array`, Campbell-Lo-MacKinlay for returns, and a source for log returns.

## REFERENCE_REQUESTS (never typed from memory; architect runs `add_reference.py`)

- `{doi: null, authors: "to be looked up", year: null, title: "Python Enhancement Proposal for typing (PEP 484) and for protocols (PEP 544)", venue: "peps.python.org (issuer page; allow-list check required)", needed_for: "L03, L05 structural protocol and type hints", confidence: low}`
- `{doi: null, authors: "to be looked up", year: null, title: "pytest documentation", venue: "docs.pytest.org (issuer page; allow-list check required)", needed_for: "L06 unit tests", confidence: low}`
- `{doi: null, authors: "to be looked up", year: null, title: "pandas documentation: indexing and index alignment", venue: "pandas.pydata.org (issuer page; allow-list check required)", needed_for: "L08 pandas index alignment", confidence: low}`
- `{doi: null, authors: "to be looked up (McKinney is a lead, not a source)", year: null, title: "pandas data-structures paper", venue: "to be looked up", needed_for: "L08 provenance of pandas", confidence: low}`
- `{doi: null, authors: "Campbell, Lo, MacKinlay (lead; to be looked up)", year: null, title: "The Econometrics of Financial Markets (book)", venue: "to be looked up", needed_for: "L09 definitions of simple and log returns", confidence: low}`
- `{doi: null, authors: "to be looked up", year: null, title: "a published treatment of simple vs log returns in finance", venue: "to be looked up", needed_for: "L09 grade-B statement that log returns aggregate over time", confidence: low}`

## DATA_REQUESTS and real-data policy

- Embedded and cleared: `fx_daily` (EUR, JPY columns) and `ust_daily` for L08 and L09. Quote the licence from
  `MANIFEST.json` and confirm it at `https://www.federalreserve.gov/disclaimer.htm` (verifier row).
- Note the MANIFEST `note` for `fx_daily`: spot rates only, no interest differential, holidays have no row. The
  L09 lab must say the returns are spot-rate returns, not carry-inclusive.
- No real firm data is used in CS1 (no EDGAR, no prices). Every filer or price path is SIMULATED.
- No new DATA_REQUESTS are needed for CS1 unless Q1 requires a vendored pandas package (a `vendor_spec.yaml`
  change, not a data request).

## NOTATION and GLOSSARY requests

- `GLOSSARY_REQUESTS`: none that are required. Optional: `control flow`, `file` (curriculum core terms without a
  concept key; Q3).
- `NOTATION_REQUESTS`: `r_t` (simple return), `\ell_t` (log return) if the builder wants them in `notation.json`
  (check the file first; the registry is binding and the builder must not redefine a symbol).

## Atlas milestone A1

- `curriculum/meta.yaml:199-201`: "Repository skeleton"; delivers "Typed Python package, CLI entry point, test
  harness, pre-commit, CI config."
- `atlas/A1.contract.md` is absent (see Source facts). The architect must draft it (as done for A15) before
  Builder D writes `grader/reference.py`. Until then, Builder D writes the rung 1-2 material and the grader
  instance generator only.
- Cumulative suite A1 only; there is no earlier milestone.

## Commands (exact)

Run from the repo root with the project venv, per `CLAUDE.md`:

```bash
.venv/bin/python tools/check_pages.py --unit CS1
.venv/bin/python tools/check_dag.py --unit CS1
.venv/bin/python tools/check_projects.py --unit CS1
.venv/bin/python tools/run_labs.py --unit CS1            # --page L03 while lessons are in progress
.venv/bin/python tools/run_graders.py --unit CS1 --seeds 0-49
.venv/bin/ruff check tests/labs/CS1 && .venv/bin/ruff format --check tests/labs/CS1
.venv/bin/mypy tests/labs/CS1
.venv/bin/python tools/embed_labs.py course/modules/CS/CS1/L01.html   # per page, after twins exist
.venv/bin/python tools/page_smoke.py --unit CS1          # verifiers only, on a quiet machine (AC2 precedent)
```

Verified flags: `check_pages.py --unit|--all --page` (`T:tools/check_pages.py:428-431`), `check_projects.py
--unit|--all` (`T:tools/check_projects.py:159-160`), `check_dag.py --unit|--all` (`T:tools/check_dag.py:89-90`),
`run_labs.py --unit|--all --page` (`T:tools/run_labs.py:119-121`), `run_graders.py --unit|--all --seeds`
(`T:tools/run_graders.py:129-131`, default `--seeds 0-49`), `page_smoke.py --unit|--all --pages --skip-labs
--skip-sweep` (`T:tools/page_smoke.py:316-320`), `embed_labs.py <pages> --refresh [lab-id...]`
(`T:tools/embed_labs.py:130-131`). The `.venv` path follows `CLAUDE.md`'s gates block.

## Tooling assumptions that do not hold for CS1 (foundations module)

1. **pandas is not in the Pyodide vendor set** (`T:tools/vendor_spec.yaml:59`). Labs and graders that import pandas
   will fail in-browser. Q1.
2. **The project deliverables are not Pyodide-runnable.** CI config, pre-commit, the installed CLI entry point, and
   `pip install -e` cannot run in the browser. The autograder can only check them structurally
   (`tomllib`, text search). Local `pytest` plus the local gates are the real check. BLUEPRINT §5.1 says
   Atlas is "developed locally, under git"; the in-browser route is for small early projects. Q7.
3. **Python version.** Curriculum 3.13 (`C:...:404`; `R:psfndpython` 3.13), repo policy 3.14+ (`CLAUDE.md`), Pyodide
   314.0.7 (`T:tools/vendor_spec.yaml:55`). Verifier row 2.5 says "CPython 3.14, the Pyodide interpreter version". Q2.
4. **No autograder-free grading path is needed**: grading is `autograder` only (`C:...:414`), so no rubric,
   exemplars or self-assessment are required for CS1. Rubric checks in `check_projects.py` are skipped.
5. **Timing in labs.** The curriculum lab is "correctness and speed" (`C:...:406`). The expected output is
   byte-compared, so a measured time cannot be in it. Q4.
6. **Pages for a foundations module teach with no prior code.** `check_pages.py` requires a lab per lesson and a
   retrieval quiz per lesson (BUILDER_RULES §4.2 item 9); these are satisfied as written.

## Open questions for the architect

- **Q1 (blocking for L08, L09 pandas parts, and grader imports).** Add pandas to `tools/vendor_spec.yaml` packages
  (pandas is not vendored today, `:59`), or accept that L08 uses a NumPy-only index alignment. Decide before
  Builder C starts L08.
- **Q2 (Python version).** Pick 3.13 or 3.14 as the teaching target. Curriculum says 3.13 (`C:...:404`); the
  runtime is 3.14 (`T:...:55`). Also decide whether `R:ramalho2021fluent` (2021) or the curriculum's 2022 edition
  is cited (Q2b; the registry records the mismatch in `notes.year`).
- **Q3 (concepts not assigned).** The core line (`C:...:387-389`) names control flow, files and "types". No concept
  key exists for them (checked against `concepts`). Options: (a) teach without `<dfn>` and accept the gap, (b) the
  architect adds keys to `curriculum/01-foundations.yaml` (would change `curriculum.json` via the renderer; not a
  builder action).
- **Q4 (timing in a lab).** Decide the benchmark rule: print only a correctness equality and an inequality
  (`vectorized_time < loop_time` as True), or a ratio with a tolerance band. The plan assumes the first.
- **Q5 (A1 contract).** `atlas/A1.contract.md` does not exist. The architect drafts it (interface: package name,
  module paths, `simple_return`, `log_return`, CLI entry point name, exit codes). Until then the `data-solution`
  path is a placeholder.
- **Q6 (lesson count).** The plan uses 9 lessons (84 h) and a 36 h project (30%). Alternatives: 8 lessons of 10-11 h
  (merge L04 into L03 and L05 into L06), with the same 36 h project. Architect to choose.
- **Q7 (CI and pre-commit under the browser).** Confirm that these deliverables are graded structurally in the
  autograder and verified locally by the verifier (the verifier runs the real gates), not run in Pyodide.
- **Q8 (cards format).** Builders use the BUILDER_RULES §7 fields (`cite`, `grade`, `basis`); AC2 cards omit them.
  Confirm the standard.
- **Q9 (licence quote for `ust_daily` and `fx_daily`).** The MANIFEST licence string is quoted; the verifier must
  open `licence_url` and find the text there. Confirm the verifier's access (the AC2 plan notes an SEC page that
  automated access could not read; the Federal Reserve page is the same type of check).

## Hard evidence limits (honest gaps)

- I did not read `atlas/A15.contract.md` or the AC2 lab twins; I read the AC2 plan and the AC2 grader and cards
  layout only as listed above.
- I did not read `tools/authorities.yaml` (allow-list). The PEP, pytest and pandas issuer-page requests assume an
  allow-list entry; the architect checks it.
- I did not run any gate. No check output is reported as PASS.
- `course/templates/*.html` were listed, not read; the builder must read them before writing.
