# QR1 build plan: Research Data Engineering (planner output, 2026-11-09)

Unit: **QR1 · Research Data Engineering** · tier M · 60 h · prerequisites [CS3, CS4, S0] · Atlas key: none (the brief
names the Atlas data layer; see B3) · grading `autograder` (no rubric) · output directory `course/modules/QR/QR1/`
(part code `QR`) · lab twins `tests/labs/QR1/` · grader `course/modules/QR/QR1/grader/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits, no file edits other than this plan.
Executors: Haiku builders, then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a
ledger.

**Status: BLOCKING ISSUES EXIST (§0.3). Lessons L01 to L06 and their labs may start once the architect decides B2.
The project (Builder C) must wait for B1 (CS3 unbuilt, A2 contract proposed and uncommitted).**

Evidence convention: `file:line` is a line read by the planner. `[prior plan]` marks a tool or convention fact taken from
a named prior plan that the planner did not re-read. `[planner-derived]` marks an inference the builders must verify.
Anything not in the curriculum is marked **NOT IN CURRICULUM**.

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part QR, code `QR`, order 17, with QR1 and QR2 as its modules | `curriculum/04-quant.yaml:548-549` (order, code) |
| QR1 id, title "Research Data Engineering", tier `M` | `curriculum/04-quant.yaml:566-568` |
| Hours `60` | `curriculum/04-quant.yaml:569` |
| Prereqs `[CS3, CS4, S0]` (only) | `curriculum/04-quant.yaml:570` |
| Core: "Point-in-time databases, corporate actions, tick data, timestamps and time zones, data vintages, alternative-data due diligence." | `curriculum/04-quant.yaml:571-572` |
| `introduces` has 7 concepts: `look-ahead-bias`, `data-vintage`, `bitemporal-data-model`, `timestamp-semantics`, `corporate-action-adjustment-factor`, `tick-data`, `alternative-data-due-diligence` | `curriculum/04-quant.yaml:574-581` |
| Sources: Croushore & Stark (2001), Journal of Econometrics 105(1); "ALFRED real-time database, Federal Reserve Bank of St. Louis (primary)" | `curriculum/04-quant.yaml:582-584` |
| Lab: "DuckDB ASOF JOIN point-in-time merge." | `curriculum/04-quant.yaml:585` |
| Project "Vintage-aware ingestion". Brief: "Extend the Atlas data layer to store and serve real-time data vintages, and prove that a backtest cannot see a revision before its publication date." Deliverable: "Atlas extension plus tests." Grading: `autograder` | `curriculum/04-quant.yaml:586-592` (title 587, brief 588-590, deliverable 591, grading 592) |
| No `debate` key and no `atlas` key on QR1 | `curriculum/04-quant.yaml:566-592` (absent) |
| JSON row for QR1 matches the YAML (hours 60, prereqs CS3, CS4, S0, 7 concepts, grading autograder, part QR) | `curriculum/curriculum.json:10458` (`"id": "QR1"`) |
| QR1 is a requirement of MS-FIN and an elective course "Quantitative Research & Backtesting" with QR2 | `curriculum/meta.yaml:98` (MS-FIN requires), `:114` (course map) |
| QR1 is a prerequisite of F1, of QR2 (QR2 prereqs `[QR1, S7]`), and of a module at `05-macro-alternatives.yaml:286` | `curriculum/04-quant.yaml:24`, `:597`; `curriculum/05-macro-alternatives.yaml:286` |
| The A2 Atlas row: module CS3, "Data layer", delivers a DuckDB store, point-in-time schema, ingestion, data manifest with hashes | `curriculum/meta.yaml:203-206` |
| CS3 (direct prerequisite of QR1) owns A2 and the concepts `asof-join`, `point-in-time-data`, `data-manifest` | `curriculum/01-foundations.yaml:452` (id), `:456` (prereqs `[CS1]`), `:464`, `:468`, `:469` |
| CS3 lab is "ASOF JOIN of trades to quotes in DuckDB-WASM." | `curriculum/01-foundations.yaml:473` |
| CS4 prereqs `[CS2, CS3]` | `curriculum/01-foundations.yaml:483` (id), `:487` (prereqs) |
| S0 prereqs `[CS1]`; S0 owns `stale-price` and `corporate-action-break` | `curriculum/01-foundations.yaml:587` (id), `:591` (prereqs), `:601`, `:602` |
| CS2 prereqs now `[CS1, M1]` (architect change already applied) | `curriculum/01-foundations.yaml:421` |
| Concept owners outside the closure (`curriculum.json` `concepts`, computed with `tools/coursekit.py` `concept_owner`): `survivorship-bias` F1; `bid-ask-spread` FC1; `limit-order-book` FC1; `macro-data-revision` GM1; `llm-lookahead-contamination` QR4; `vectorized-backtest` and `backtest-cost-model` QR2 | planner run of `concept_owner()` |
| Concept owners inside the closure: `asof-join`, `point-in-time-data`, `data-manifest`, `parquet-format` (CS3); `property-based-testing`, `deterministic-computation`, `bit-for-bit-reproducibility` (CS4); `order-book-data-structure`, `event-queue` (CS2); `empirical-distribution`, `outlier-detection`, `stale-price`, `corporate-action-break` (S0) | planner run of `concept_owner()`; the rows above |
| Prerequisite closure of QR1 = {CS1, CS2, CS3, CS4, M1, P0.1, S0} | planner run of `tools/coursekit.py` `prerequisite_closure("QR1")` |
| Built units inside the closure: CS2 and M1 only. CS1, CS3, CS4, S0 and P0.1 have no built pages | planner run of `built_units()`; `course/modules/CS/` holds CS2 only; `course/modules/M/` holds M1 to M7 |
| Nearest built prerequisite: CS2 (in the closure; direct prerequisite of CS4, `:487`) | `plans/CS2-build-plan.md` (429 lines; architect decisions at its end) |
| No `course/modules/QR/`, `tests/labs/QR1/` or `ledgers/QR1/` exists | `ls` run by the planner |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 60 h (`curriculum/04-quant.yaml:569`). Rules `[prior plan]` (E5 §0.2, read there from
`tools/check_pages.py`): lesson `data-hours` 6 to 12; hub `data-hours-lessons + data-hours-project = 60`; project share
10 to 40 % of 60, i.e. 6 to 24 h; lessons sum to the hub's lessons figure.

Chosen split: **6 lessons × 7 h = 42 h; project 18 h (30 %)**. 42 + 18 = 60. Feasible. No hours STOP condition.
Alternatives in §12 Q8.

### 0.3 Blocking issues (architect decision required before the named builder starts)

**B1 · The project depends on CS3's A2 contract and reference, and CS3 is unbuilt (blocks Builder C only).**
- QR1's brief extends "the Atlas data layer" (`curriculum/04-quant.yaml:588-591`). The data layer is A2, delivered in CS3
  (`curriculum/meta.yaml:203-206`), which is a direct prerequisite (`:570`).
- `atlas/A2.contract.md` now exists (untracked; `git status` shows `?? atlas/A2.contract.md`). Its header reads "proposed by
  the architect's assistant, architect to confirm" (`atlas/A2.contract.md:4`). It freezes the store schema (`:106-117`),
  the as-of rule keyed on `retrieved` (`:96-104`), and the error table (`:137-150`).
- `plans/CS3-build-plan.md` is marked BLOCKED for its project (`:8`) and its Q3 decision (`:401`) is proposed, not
  confirmed. No CS3 reference exists under `course/modules/CS/CS3/`.
- Recommended default: Builder A, B may write lessons and labs now. Builder C writes the project only after the architect
  confirms A2 and CS3 is verified. The grader then carries a byte-identical copy of CS3's accepted A2 reference, pinned by
  SHA-256 in its docstring (ruling 9 path for shared code; no cross-unit runtime import in Pyodide). §12 Q1.

**B2 · The curriculum lab names a runtime that does not exist here (blocks Builder A on L03 only).**
- The lab is "DuckDB ASOF JOIN point-in-time merge." (`curriculum/04-quant.yaml:585`).
- `tools/run_labs.py:70-71` returns "has no local runner yet" for any `data-runtime` other than `python` (read by the
  planner).
- DuckDB is not pinned: `requirements-dev.txt` has no `duckdb` (read). It is not in `tools/vendor_spec.yaml` (the Pyodide
  `packages` list is `[numpy, scipy, pytest]`, `tools/vendor_spec.yaml:59`). `course/assets/vendor/LOCK.json` has no
  DuckDB or sqlite entry (planner grep). BLUEPRINT §6 (`BLUEPRINT.md:346-347`) says DuckDB-WASM joins the lock file with
  "the first SQL ... modules"; CS3 is the first, and CS3 is unbuilt.
- The same blocker is recorded in the CS3 plan: its proposed Q1 decision option (b) "governs QR1 as well"
  (`plans/CS3-build-plan.md:387-390`).
- Recommended default: adopt CS3 Q1 option (b), applied to QR1 (`python` lab; a pure-Python ASOF reference with the A2
  tie rule; the SQL shown as a listing labelled "SQL, not run"; the page states that the curriculum's DuckDB lab is not
  run). This departs from the curriculum text at `:585`, so the architect must accept it. §12 Q2.

**B3 · "Atlas extension" and "prove" in the brief (blocks Builder C's spec wording).**
- (a) QR1 has no `atlas:` key (`curriculum/04-quant.yaml:586-592`). It is not an Atlas milestone. A2 is frozen once CS3
  is released (`atlas/A2.contract.md:4-5`). A2's schema is fixed (`:108`: "Column names are part of the contract").
- (b) The brief asks to "prove" that a backtest cannot see a revision before its publication date (`:589-590`), but the
  grading mode is `autograder` (`:592`). An autograder checks properties, not proofs.
- Recommended default: (a) QR1 ships a unit-local module `vintages.py` that consumes A2's public API read-only, adds its
  own table in its own SQLite file, and changes nothing in A2. Any A2 change goes through CONTRACT_CHANGE_REQUESTS
  (BUILDER_RULES §5.5). (b) The no-look-ahead claim is proved on the page as Proposition 2.1 (grade T) in L02, and the
  grader checks the property on 50 seeds. The page says so in one sentence. §12 Q3 and Q4.

**Non-blocking, but the architect should see them:**
- **N1 · Pyodide `sqlite3` is unverified.** `atlas/A2.contract.md:121-124` says the Pyodide build's `sqlite3` is not
  confirmed. QR1's grader uses SQLite through `VintageIndex`. The browser probe must run before the project's Pyodide run.
  §12 Q6.
- **N2 · The ALFRED source is not admitted.** It is a primary source with no registry record: `references/review_queue.json:1325-1328`
  ("primary document: add manually", used by QR1). QR1 cites no ALFRED key until the architect admits one. §7.2.
- **N3 · The DST rule has no source.** `et_to_utc` (§5.2) implements a US daylight-saving convention. No registry record
  covers it. It is stated as the project's convention and is not cited as law. §12 Q7.
- **N4 · The registry record for Croushore & Stark carries no abstract.** The fields are title, authors, year, container,
  volume, issue, pages, DOI and publisher (`references/references.json:6262-6300`). VERIFIER §2.1 requires reading at least
  the abstract before attributing content. §7.1 and §12 Q11.
- **N5 · No curriculum source string needs correcting.** "Croushore & Stark (2001), Journal of Econometrics 105(1)" matches
  the record's container, volume and issue (`references/references.json:6262-6300`).

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

6 lessons × 7 h = 42 h; project 18 h; total 60 h. Concept counts per row sum to 2+2+0+1+1+1 = 7, each concept in exactly
one row (`curriculum/04-quant.yaml:574-581`).

| Lesson | Title (working) | Concepts it defines (`introduces`) | Lab (twin id, `tests/labs/QR1/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Timestamps, time zones and look-ahead bias | `timestamp-semantics`, `look-ahead-bias` | `lab-QR1-L01-1`: local release times with explicit offsets converted to UTC; rows visible at a cut-off counted against a brute-force count. SIMULATED. | 7 | A |
| L02 | Data vintages and the bitemporal model | `data-vintage`, `bitemporal-data-model` | `lab-QR1-L02-1`: a SIMULATED revision path; the value visible at each cut-off against the final revised value; the gap printed. Proposition 2.1 proved on the page. | 7 | A |
| L03 | Point-in-time merge (the curriculum lab) | none (uses CS3 `asof-join`, `point-in-time-data`) | `lab-QR1-L03-1` (**curriculum lab**, §0.3 B2): pure-Python ASOF reference with the A2 tie rule against brute force on seeded trades and vintages; mismatch count printed. SQL listing labelled "SQL, not run". | 7 | A |
| L04 | Corporate actions and adjustment factors | `corporate-action-adjustment-factor` | `lab-QR1-L04-1`: split adjustment of a seeded close series; adjusted return at a pure-split date checked to zero within a stated tolerance. | 7 | B |
| L05 | Tick data | `tick-data` | `lab-QR1-L05-1`: seeded out-of-order trade records; the last trade at each cut-off by `(timestamp, seq)` checked against brute force; the count of answers that arrival order would get wrong printed. SIMULATED. | 7 | B |
| L06 | Alternative-data due diligence | `alternative-data-due-diligence` | `lab-QR1-L06-1`: a SIMULATED panel where names leave at a delisting date; the survivor-only mean and the full-panel mean printed. | 7 | B |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 42/18 | none | none | - | A |
| project | Vintage-aware ingestion (`autograder`) | none | `lab-QR1-project-1` (rung 1), `lab-QR1-project-2` (rung 2, `class="lab completion"`), `lab-QR1-project-3` (rung 3 check) | 18 | C |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py`, `alternatives/` | none | none | - | C |
| cards | `cards.json` from L01 to L06 | none | none | - | F (after A to C) |

Builder letters: **A** writes the hub and L01 to L03. **B** writes L04 to L06. **C** (the last builder) writes `project.html`,
the grader folder, and the project labs; it starts after B1 is resolved. **F** writes `cards.json` after A to C. Builders D and
E are not assigned for QR1: two content builders of three lessons each, and one project builder, match the unit's size.

Ownership rule: a builder writes only its own lesson pages and twins. Builder A also writes the hub after L01 and L02 exist.

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses only, §4):
- L01 uses only CS3 and CS1 concepts for offsets and files (linked, usable) and defines `timestamp-semantics` before
  `look-ahead-bias`.
- L02 uses L01's two concepts. Proposition 2.1 uses the A2 as-of rule as a model only.
- L03 uses L02 (`data-vintage`, `bitemporal-data-model`) and CS3 (`asof-join`, `point-in-time-data`, linked to
  `concepts.html#asof-join`, which is usable because CS3 is in the closure).
- L04 uses S0 `corporate-action-break` and `stale-price` (linked, usable) and L01 time semantics in prose.
- L05 uses CS2 `order-book-data-structure` and `event-queue` (linked, usable) and L01 timestamps.
- L06 uses L02 vintages and CS3 `data-manifest` (linked); the survivorship concept is plain prose (§4 D1).

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to QR1)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3 to §8, `plans/E5-build-plan.md` (its Architect
decisions section is binding precedent), `plans/CS2-build-plan.md` (its Architect decisions section is binding; it is the
nearest built prerequisite and the autograder pattern), `atlas/A2.contract.md` (read-only; for the A2 formats), and this
file. Study `course/modules/CS/CS2/` (grader layout, cards, labs) and `course/modules/M/M1/` (proof-heavy template).
`course/templates/` holds the four skeletons. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every printed number comes from an exact value, or from a float with a stated tolerance
   (ruling 22: the tolerance on the page is the tolerance the grader uses). A page that shows a rounded figure states its
   rounding rule.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints; the interpretation names only
   what the printed numbers show. The M1 defect "checked directly" with no lab behind it is not repeated.
3. **Attribute nothing unread.** Only the registry key `croushore2001real` may be cited (§7.1). Its record has no abstract
   (N4), so a builder may state only the title-level fact at grade C with the key, unless the paper's text has been read and
   the locator is recorded. No page, table or number is typed from memory.
4. **Scope words need a computation.** "every", "all", "never", "always", "any", "exact", "no look-ahead", "stable", "the
   market" and "the revision" are used only where a proof, a finite check or a lab computes the claim. The grader's property
   tests (seeds 0 to 49) back the no-look-ahead claim in the code; the proof backs it on the page.
5. **Define before use.** Each of the 7 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned
   lesson, and never before it. Plain terms outside the 7 (publication time, retrieval time, revision, cut-off, tick, offset,
   the daylight-saving convention) get a plain `<dfn>` with no `data-concept` (`tools/check_dag.py` skips a `<dfn>` without
   `data-concept`, `[prior plan]` E5 §2.1 item 5).
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation lists numbered Assumptions (A1, A2, ...)
   before the statement. Required: Proposition 2.1 (visibility) needs A1 publication times are recorded for every vintage,
   A2 the visible value at cut-off `t` is the vintage with the greatest publication time not after `t`, A3 vintages with
   publication times after `t` are not used in the answer at `t`. Derivation 4.1 (split invariance) needs A1 the event is a
   pure split (no change in value), A2 the ratio is positive.
7. **Grader rule (autograder).** The grader asserts an exception type only for the conditions the spec names (§5.2 list E1 to
   E6). Any other invalid input is asserted to raise some exception whose message names the property (ruling 19, fixer-rules
   line 19).
8. **Money.** QR1 has no money output. Prices are floats with the tolerance stated; a value from the A2 store is returned as
   its exact text (A2 contract `:23`). No money as float.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own
   container. `page_smoke.py` is the verifier's check.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` and has no
    `if __name__ == "__main__":` guard. `run_labs.py` runs each twin as `python -I -W error` with no network (`[prior plan]`
    E5 §2.1 item 10, `tools/run_labs.py:51-60`).
11. **Timestamps use the A2 form.** Every instant in a lab, test or page is `YYYY-MM-DDTHH:MM:SSZ` (`atlas/A2.contract.md:21`).
    A local wall time is written with its zone name and converted by `et_to_utc` (§5.2). A naive timestamp is a named error.
12. **Basis of every rate or return.** Any return is stated as simple or log, per period; any yield is percent per year
    (`[prior plan]` E5 §2.1 item 11).

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation or a lab basis. A
  B- or C-graded claim names its counter-evidence (BUILDER_RULES §2.5). §7.2 lists the requests.
- Concepts: §1 table; `<dfn>` only for the 7 registered concepts, plus plain `<dfn>` for other terms. A `<a class="concept">`
  link only for a concept in the closure {CS1, CS2, CS3, CS4, M1, P0.1, S0} (§4 D1 to D4).
- Prerequisite links: `href="../../../concepts.html#<id>"` for closure concepts; `href="Lnn.html#def-<id>"` for earlier QR1
  lessons. A lesson never links a concept defined in a later lesson. No link to a CS1 or CS3 hub page: those pages are not
  built (`[planner-derived]`; the same rule as E5 §2.2).
- Labs: code lives once in `tests/labs/QR1/lab-QR1-Lnn-1.py` (and `lab-QR1-project-1..3.py`). The page carries
  `@@LAB:<file>@@` and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match
  `lab-QR1-<page>-<n>`. Standard library only (`datetime`, `fractions`, `random.Random(seed)`, `sqlite3` only where the
  project's store is used). Seeded RNG only; no network; under 10 s in Pyodide; `-W error` clean.
- SIMULATED label: on every lab, figure or project fixture that uses generated data. Every lab in this unit uses generated data,
  so every lab carries the label (§6).
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`,
  `course/concepts.html`, `course/assets/data/*`, `references/*.json`, `MANIFEST.json`, `atlas/*.contract.md`). Request changes.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references
  in code comments.
- Banned strings (`tools/check_pages.py` `BANNED`, `[prior plan]` E5 §2.2): TODO, TBD, lorem, "for brevity", "details omitted",
  "beyond the scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree",
  "it is well known", "obviously", "clearly", and any ellipsis outside code.
- A finite enumeration is grade C with its basis named, not grade T (M1 precedent).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration.
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10
  output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols QR1 must not give a different meaning (`notation/notation.json`, `symbols` and `macros`):

| Registered symbol | Registered meaning (locator) | QR1 rule |
|---|---|---|
| `T` | number of return observations in a sample (`notation.json:112-114`, module S1) | **Never used** for a time, a horizon or a count. Time is `t` or `\tau`; the sample size is `n`. |
| `\Phi`, `\gamma_3`, `\gamma_4`, `R^\ast`, `R^{e\ast}`, `R_f`, `\mathbb{Q}` (`notation.json:117-150`) | M4 and AP1 meanings | Not used. |
| `\E`, `\Prob`, `\Var`, `\Cov`, `\Corr` (macros, `notation.json:5-24`) | expectation, probability, variance, covariance, correlation | Used only with their registered meaning. The word "variance" is not needed in QR1. |
| `\R` (macro, `notation.json:25-28`) | real numbers | Standard. |

Local symbols (allowed; defined on the lesson where first used, never redefined): `t` cut-off time, `\tau` publication time,
`s` retrieval time, `v` value (text in A2), `P` price, `r` split ratio, `F` cumulative adjustment factor, `n` sample size.
`\pi` and `i` are not used (no inflation or policy rate in QR1).

NOTATION_REQUESTS: none. The plan uses only local symbols and registered macros.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the BUILDER_RULES §4.2 structure. Mandatory content, by lesson:

- **L01 `timestamp-semantics`, `look-ahead-bias`.** Three instants per datum: the event time, the publication time, and the
  retrieval time. The A2 store keys on retrieval time (`atlas/A2.contract.md:96-104`); a backtest needs publication time.
  UTC normalization with explicit offsets; the A2 `Z` form is the only accepted form. Look-ahead bias defined as use of
  information that was not available at the decision instant. Lab L01-1 (SIMULATED): convert local release times with
  explicit offsets to UTC and count visible rows at a cut-off. Grades: definitions (T by definition); the lab count (C, basis
  "Lab L01-1, SIMULATED"). Where the canon breaks: retrieval time used as publication time; a time without its zone.
- **L02 `data-vintage`, `bitemporal-data-model`.** A vintage is the value of one observation as published at one instant.
  The bitemporal model keeps two times per row: the observation (valid) date and the publication (transaction) time, with
  retrieval as a third time when kept. **Proposition 2.1 (T):** under A1 to A3 of §2.1 item 6, adding any vintage with
  publication time after `t` does not change the visible value at `t`. Proof: the answer is a function of the vintages with
  publication time at most `t` only; a new vintage with publication time after `t` is not in that set. Lab L02-1 (SIMULATED):
  a revision path; the visible value at each cut-off against the final revised value, the gap printed. Citation:
  `croushore2001real` at paper level with grade C and the title-level fact only (N4). Where the canon breaks: a provider that
  overwrites history keeps no vintage; a publication time not recorded.
- **L03 (curriculum lab, no defined concept).** The point-in-time merge: each observation row joins the latest vintage
  published at or before its decision time, with the A2 tie rule (`atlas/A2.contract.md:100-101`) applied to equal
  publication times. Lab L03-1 (SIMULATED, python, §0.3 B2): a pure-Python ASOF reference checked against brute force on seeded
  trades and vintages; the mismatch count printed (zero). The SQL form is shown as a listing labelled "SQL, not run". The
  page states that the curriculum's DuckDB ASOF lab is not run under B2. Grades: C (lab basis). Where the canon breaks:
  unsorted inputs; equal timestamps; a missing decision time.
- **L04 `corporate-action-adjustment-factor`.** For a pure split at ex-date `e` with ratio `r > 0`, the adjusted close before
  `e` is the raw close divided by `r`; on and after `e` it is unchanged. Cumulative factors multiply over events after the
  date. **Derivation 4.1 (T):** under A1 (pure split) and A2 (`r > 0`), the adjusted simple return at `e` is zero. Derivation:
  `P̃_e / P̃_{e-1} = P_e / (P_{e-1}/r) = r P_e / P_{e-1} = r (1/r) = 1`, using `P_e = P_{e-1}/r` for a pure split. Lab L04-1
  (SIMULATED): split adjustment of a seeded close series; the return at each pure-split date printed and checked to zero
  within the stated tolerance (1e-12 relative). Links: S0 `corporate-action-break` (usable). Where the canon breaks: cash
  dividends are not a split and are not claimed here; a mis-recorded ratio.
- **L05 `tick-data`.** A tick is a trade or quote record with an exchange timestamp, a sequence number, a price and a size.
  The last trade at `t` is the record with the greatest `(timestamp, seq)` whose timestamp is at most `t`. Arrival order is not
  the time order. Lab L05-1 (SIMULATED): out-of-order records; the sorted rule checked against brute force; the number of cut-offs
  that arrival order would answer wrongly printed. Links: CS2 `order-book-data-structure` and `event-queue` (usable).
  Where the canon breaks: receipt time versus exchange time; clock resolution; crossed quotes (plain prose; no claim).
- **L06 `alternative-data-due-diligence`.** A checklist of six questions a student asks before a dataset enters a backtest:
  when it became available (publication time), what it covers (delistings, survivorship), whether it is revised, its licence,
  its hash and manifest (CS3 `data-manifest`, linked), and whether it is stable over time. Lab L06-1 (SIMULATED): a panel with
  delistings; the survivor-only mean and the full-panel mean of a period return printed; the gap is a SIMULATED result, not a
  claim about any market. Survivorship (`survivorship-bias`, F1) appears in plain prose (§4 D1). Where the canon breaks: a
  checklist is not a test; a clean licence says nothing about revisions.

Lesson-level constraints:
- Each lesson's "Where the canon breaks" names at least one limit and what changes without it.
- No lesson uses a term from QR2 (backtest architecture, walk-forward, purged CV) or QR4 (LLM look-ahead) as a concept. The
  word "backtest" appears in plain prose only.
- Each lesson has at least 3 misconceptions (BUILDER_RULES §4.2 item 6); L02's first misconception is "the latest vintage is the
  right input for a backtest".

---

## 4. DAG problems (concepts that natural QR1 content would use outside the closure)

Prerequisite closure of QR1 (computed): **{CS1, CS2, CS3, CS4, M1, P0.1, S0}**. Usable concepts are the introduces of those
modules. Owners below are from `curriculum/curriculum.json` `concepts` (planner check).

| Ref | Concept | Owner (outside closure) | Where natural QR1 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `survivorship-bias` | F1 (`curriculum/04-quant.yaml:24` lists F1 after QR1) | L04 and L06 (delisted names drop out of a panel) | Plain prose "survivorship" with no `<dfn>` and no link. Lab L06-1 shows the effect on SIMULATED data. Architect may add F1 as a prerequisite instead (not recommended: F1 pulls a 60 h module). §12 Q10. |
| D2 | `bid-ask-spread` (FC1), `limit-order-book` (FC1) | FC1 | L05 (quotes), L05 order books | Plain prose. L05 uses the CS2 `order-book-data-structure` (usable). |
| D3 | `macro-data-revision` (GM1) | GM1 | L02 (revisions are the reason for vintages) | Plain prose "macroeconomic data revisions", no link. Its citation is not needed. |
| D4 | `vectorized-backtest`, `backtest-cost-model`, `walk-forward-analysis` (QR2) | QR2 | The project's word "backtest"; L02 and L06 | Plain prose "backtest" only. No link. |
| D5 | `llm-lookahead-contamination` (QR4) | QR4 | none | Not used. |
| D6 | `crsp-compustat-structure` (F1) | F1 | L04 and L06 mention CRSP and Compustat as examples of data with corporate actions | Named in prose only, as examples. No definition, no link. |
| D7 | `spread-decomposition`, `roll-spread-estimator` (MS1) | MS1 | none | Not used. |
| D8 | `stale-price`, `corporate-action-break` (S0); `asof-join`, `point-in-time-data`, `data-manifest` (CS3); `order-book-data-structure`, `event-queue` (CS2) | inside the closure | L03 to L06 | Usable. Linked with `concepts.html#<id>`. No DAG issue. |

Each row has a resolution, so no DAG_DEFECT blocks the build. `check_dag.py` checks linked uses only (`[prior plan]` E5 §4).
An unlinked use of D1 to D7 passes the tool, so the verifier reads every lesson for these names (VERIFIER §2.9).

---

## 5. Project (`project.html`, Builder C): autograder, ladder, spec, grader

### 5.1 Ladder (BLUEPRINT §5.1; `check_projects.py` requires the order)

Tier M: rungs 1 and 2 are kept to the minimum (BLUEPRINT §4, `BLUEPRINT.md:222-223`; BUILDER_RULES §5.1 line 188).

1. **Rung 1, worked example** (`lab-QR1-project-1`, SIMULATED): one solved, annotated `visible` query on a three-vintage
   series, with a "why" note at each step. Skippable on a placement pass.
2. **Rung 2, completion** (`lab-QR1-project-2`, `class="lab completion"`, SIMULATED): the `visible_series` filter line (the
   publication-time test) is replaced by `___`. Graded instantly. The twin is the completed solution; every page line equals
   the twin line or contains a blank (`tools/run_labs.py` docstring, `[prior plan]` E5 §5.1).
3. **Rung 3, independent project** (graded by autograder): `vintages.py` to the interface in §5.2 and the tests in §5.4.
   `lab-QR1-project-3` is the rung-3 check: it runs the seed-0 instance and prints the table the grader expects.
4. **Rung 4, stretch** (optional, not graded): a revision-size study on a second SIMULATED series, with the revision size
   stated as a hypothesis; or a corporate-action study with a cash-dividend rule stated and tested.

### 5.2 Spec (`project.html`; the grading entry names "autograder")

- **Context.** A research team stores macro and market data in a point-in-time store. A backtest must never see a value
  before its publication time, and a split must not look like a return. The project extends the store with publication times,
  tick queries and split adjustment, under tests.
- **Inputs.** SIMULATED fixtures only (§6). No file is read from the network.
- **Required outputs.** One file, `vintages.py`, that defines the interface below. No other file is graded.
- **Frozen interface** (the reference must match; names frozen when Builder C writes the spec):
  - `et_to_utc(wall: str) -> str`. `wall` is `YYYY-MM-DD HH:MM` in America/New_York. Returns the A2 `Z` form. The convention
    (stated as the project's rule, §6): daylight time applies from 02:00 local on the second Sunday of March to 02:00 local
    on the first Sunday of November; otherwise standard time (UTC−5); daylight time is UTC−4. A wall time in the spring gap
    does not exist. A wall time in the autumn overlap takes the earlier instant (daylight time).
  - `class VintageIndex(path: str)`: `record(source, series, obs_date, value, published, retrieved) -> None`;
    `visible(source, series, obs_date, t) -> str | None`; `visible_series(source, series, t) -> dict[str, str]`;
    `close() -> None`. `source` is one of the five A2 `SOURCES` (`atlas/A2.contract.md:30`). `obs_date` is `YYYY-MM-DD`.
    `value` is text (A2 keeps value text). `published` and `retrieved` are A2 `Z` instants.
  - `last_trade_at(ticks: list[tuple[str, int, float]], t: str) -> float | None`. Each tick is `(timestamp, seq, price)`. The
    answer is the price of the tick with the greatest `(timestamp, seq)` whose timestamp is at most `t`.
  - `adjust_closes(dates: list[str], closes: list[float], events: list[tuple[str, float]]) -> list[float]`. An event is
    `(ex_date, ratio)`. For each date `d` the adjusted close divides `closes[i]` by the product of the ratios of all events with
    `ex_date > d`.
- **Named conditions (the only ones with an exception type; the grader asserts `ValueError` only for these):**
  - E1 `et_to_utc`: a malformed string; a wall time in the spring gap.
  - E2 `VintageIndex`: an empty `path`.
  - E3 `record`: a `source` not in `SOURCES`; a timestamp not in the `Z` form; `retrieved` earlier than `published`; the same
    `(source, series, obs_date, published)` already stored with a different `value`. An identical re-record is a no-op.
  - E4 `visible` and `visible_series`: a `t` that is not an `Z` instant (naive `t` is one of these).
  - E5 `last_trade_at`: a `t` that is not an `Z` instant.
  - E6 `adjust_closes`: a ratio not greater than zero; `dates` and `closes` of different lengths.
  - Not errors: `visible` returns `None` when no vintage is published at or before `t`, and when the series is unknown;
    `visible_series` returns `{}` in that case; `last_trade_at` returns `None` when no tick is at or before `t`.
- **Constraints.** Python standard library only (`datetime`, `sqlite3`, `bisect`, `heapq`, `fractions`, `math`). No network,
  no DuckDB, no zoneinfo (§11). No mutation of inputs. No print or warning.
- **Grading.** Autograder (`grading: autograder`, `curriculum/04-quant.yaml:592`). The spec's grading entry names the
  autograder. No rubric, no exemplars.
- **Reading list.** `ol.reading-list` cites `croushore2001real` only (registry key; §7.1).
- **The brief's "prove".** The spec says: the no-look-ahead property is tested on every seed; the proof of the property is
  Proposition 2.1 in lesson L02 (B3(b)).

### 5.3 Time budget (`<table id="hours">`, sums to 18 h; one-line rationale per row)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example | 2 | Read and annotate one solved `visible` query |
| Rung 2, completion | 2 | Fill the publication-time filter and run the instant check |
| Timestamps and `et_to_utc`, with the named conditions | 3 | Convert and reject the spring gap; check the autumn overlap |
| `VintageIndex`: record, visible, visible_series | 4 | Persist vintages in SQLite; apply the no-look-ahead rule and the duplicate rule |
| `last_trade_at` and `adjust_closes` | 4 | Sort by `(timestamp, seq)`; apply the split factor with the ex-date boundary |
| Property checks and the local and Pyodide run | 3 | Run the suite locally and in Pyodide; fix the failures the run shows |
| **Total** | **18** | Equals `data-hours-project` on the hub (`18 / 60 = 30 %`) |

### 5.4 Grader design (`grader/`; autograder, per BUILDER_RULES §5.3)

**Files.** `grader/instance.py`, `grader/reference.py` (the full solution of §5.2), `grader/starter.py` (every function raises
`NotImplementedError`; the suite must fail on it), `grader/test_project.py`, `grader/alternatives/alt_1.py` to `alt_5.py`
(§5.4.4), `grader/a2_dataset_reference.py` (the byte-identical copy of CS3's accepted A2 reference, pinned by SHA-256; §0.3 B1).

**5.4.1 Instances.** `make_instance(seed: int) -> dict` is deterministic per seed. It generates: 2 to 4 series across two A2
sources; 4 to 12 observation dates; for each (series, date), 1 to 4 vintages with publication times and retrieval times with
retrieval at or after publication; a revised value at a later publication for about half of the cells; 20 to 120 ticks with
out-of-order arrival and a shared timestamp for some pairs; 10 to 40 closes with 0 to 3 split events (ratio in {2.0, 3.0,
0.5, 4.0}); cut-off times drawn across and at the publication instants. One invalid case per seed, chosen from E1 to E6 only,
returned under the key `invalid`. Every instance is valid except the `invalid` case. The docstring and the page label every
instance **SIMULATED**. Seeds 0 to 49 give materially different answers (BUILDER_RULES §5.3).

**5.4.2 Tests (`grader/test_project.py`; properties and numbers only).** Each test is under 5 s in Pyodide; the suite under 60 s.
- T1 no look-ahead: for each seed and cut-off, `visible` is unchanged after recording every vintage published after the cut-off.
- T2 visible equals a brute-force oracle written in the test from the raw vintage list (publication at most `t`; the greatest
  publication time wins).
- T3 `visible_series` equals the map of `visible` over the observation dates, omitting `None`.
- T4 `et_to_utc` anchors: `2026-01-15 12:00` gives `2026-01-15T17:00:00Z`; `2026-07-01 12:00` gives `2026-07-01T16:00:00Z`;
  `2026-03-08 01:59` gives `2026-03-08T06:59:00Z`; `2026-03-08 03:00` gives `2026-03-08T07:00:00Z`; `2026-11-01 01:30` gives
  `2026-11-01T05:30:00Z` (earlier instant). These dates are the second Sunday of March 2026 (2026-03-08) and the first Sunday of
  November 2026 (2026-11-01), checked by the planner with Python's `date.weekday()`.
- T5 `et_to_utc` gap: `2026-03-08 02:00` and `02:30` raise E1; `01:59` and `03:00` do not.
- T6 `last_trade_at` equals brute force for every cut-off; an out-of-order instance; a shared timestamp resolved by the higher `seq`.
- T7 `adjust_closes`: the split-invariance property (the adjusted return at each pure-split date is zero within 1e-12 relative);
  the ex-date boundary (the close on the ex-date is unadjusted, the close the day before is adjusted); a ratio of 0 and a
  negative ratio each raise E6 (two tests); a length mismatch raises E6.
- T8 `record`: `retrieved == published` is accepted; `retrieved < published` raises E3; an identical re-record is a no-op; a
  different value for the same key raises E3; a source outside `SOURCES` raises E3; a timestamp without `Z` raises E3.
- T9 `visible` and `visible_series` with a naive `t` raise E4; `visible` with no vintage at or before `t` returns `None` and
  not `0` or `""`; `visible` on an unknown series returns `None`.
- T10 `last_trade_at` with a naive `t` raises E5; with no tick at or before `t` returns `None`.
- T11 the `invalid` case of each seed is refused with its named condition's exception.
- T12 `starter.py` fails the suite (all functions raise `NotImplementedError`).

Feedback: a failing test names the property violated and a concept hint (for example, "a value changed after a later
publication: check the publication-time filter in the spec"). It never prints the expected answer. Every test helper that
compares values sets `__tracebackhide__` (fixer-rules line 19).

**5.4.3 Mutants (exactly ten, each a single-change copy of the reference under `ledgers/QR1/mutants/`; the first docstring line
names the student error).** Each must be killed by at least one named test (`tools/mutate_graders.py --unit QR1 --seeds 0-9`).

| ID | Student error (single change to the reference) | Killed by |
|---|---|---|
| M01 | `visible` tests `published < t` (strict), hiding a vintage published exactly at the cut-off | T2 (equality case), T1 |
| M02 | `visible` ignores `published` and returns the latest recorded vintage (look-ahead revision) | T1 |
| M03 | `record` accepts `retrieved < published` silently | T8 |
| M04 | `record` overwrites a duplicate key with the new value silently | T8 |
| M05 | `visible` returns `""` (or `0`) instead of `None` when nothing is visible | T9 |
| M06 | `last_trade_at` takes the last tick in input order instead of the greatest `(timestamp, seq)` | T6 |
| M07 | `adjust_closes` divides the closes on or after the ex-date (off-by-one at the boundary) | T7 (boundary) |
| M08 | `adjust_closes` multiplies pre-event closes by the ratio (direction error) | T7 (split invariance) |
| M09 | `et_to_utc` uses UTC−5 all year (ignores daylight time) | T4 (July anchor) |
| M10 | `et_to_utc` maps a spring-gap wall time to standard time silently | T5 |

A mutant that differs from the reference only where the page states nothing goes to `ledgers/QR1/equivalent/` with a README
proof (ruling 9). A mutant that differs only inside a stated tolerance goes there too (ruling 22, 25). An optional eleventh
mutant (a hard-coded answer for seed 0) is suggested to the verifier and is not required.

**5.4.4 Alternatives (five correct implementations of different styles; each must pass seeds 0 to 49, ruling 10).**
- `alt_1`: SQLite with `ORDER BY published DESC LIMIT 1` and fixed-width UTC text, all four functions in the same file.
- `alt_2`: SQLite with a `ROW_NUMBER()` window per key (requires a SQLite with window functions; checked in the browser).
- `alt_3`: an append-only JSON-lines file with `bisect` over the sorted publication list rebuilt on open.
- `alt_4`: a single JSON file rewritten atomically on each `record`, with a linear scan for `visible`.
- `alt_5`: records as `dataclass(order=True)` objects in a list; `heapq` for ticks; a generator for `visible_series`.
Each alternative implements the full interface. A correct alternative that fails a test is a defect in the test or in the
alternative, and the verifier decides which (ruling 10; a float-based alternative wrong on an exact rule is a mutant).

**5.4.5 Reference.** `grader/reference.py` is the full solution. It must pass T1 to T12 on seeds 0 to 49
(`tools/run_graders.py --unit QR1 --seeds 0-49`). The collect-only count of `test_project.py` is quoted on the project page
(fixer-rules line 19). Excluded from deployment (BLUEPRINT §7).

---

## 6. Real-data policy (B1-data; BLUEPRINT §5.3 and BUILDER_RULES §6.6)

- **Embedded (redistributable, grant quoted):** `fx_daily`, `fx_monthly`, `ust_daily` (`tools/data_sources.yaml:18-116`;
  `course/assets/data/market/MANIFEST.json`). None is needed by QR1. No `data-files` attribute on any QR1 lab.
- **Not embedded, and no grant found:** ALFRED vintages (a primary source with no registry record, N2); FRED third-party
  series (BLUEPRINT §5.3 says FRED carries third-party series under their owners' terms, `BLUEPRINT.md:310-312`); tick data
  (no curriculum source, no registry record); the A2 download step (an honest gap: `atlas/A2.contract.md:8-11`).
- **Every dataset in QR1 is SIMULATED.** Each lab, each figure (none planned) and each project fixture is generated with a seed
  and labelled **SIMULATED** on the page, in the lab docstring, and in `make_instance`'s docstring.
- **Honest-pending note** on the hub and on L02: "The curriculum names ALFRED real-time vintages as a source for this unit.
  No redistributable vintage data is embedded. Every lab and the project's fixtures are generated and labelled SIMULATED."
- **DATA_REQUESTS** (for the architect; the planner does not name a series, licence or URL from memory): a vintage series with
  its issuer URL, the quoted licence sentence and the page that states it, and the transform (BUILDER_RULES §6.6 steps 1 to 5).
  No DATA_REQUEST is required for QR1 to build.
- **Bring-your-own-data** is not required: the project uses fixtures, not a student's file.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

| Key | Record (as read) | Status | Use in QR1 |
|---|---|---|---|
| `croushore2001real` | Croushore & Stark, "A real-time data set for macroeconomists", Journal of Econometrics, volume 105, issue 1, pages 111-130, year 2001, DOI 10.1016/s0304-4076(01)00072-0, Elsevier BV (`references/references.json:6262-6300`); `used_by: ["GM1", "QR1"]` (same block); `status: verified`; no abstract field | verified | L02 at paper level with grade C and the title-level fact only (N4); reading list; the one registry key QR1 cites |

Not cited by QR1: `ALFRED` (not admitted, N2); `codd1970relational` and `raasveldt2019duckdb` (CS3's keys; QR1 has no
claim that needs them, and the lab does not use DuckDB, §0.3 B2).

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- {doi: null, authors: "ALFRED database, Federal Reserve Bank of St. Louis (lead only; the record is not typed)", year: null, title: "ALFRED real-time database (primary)", venue: "the issuer's own page on stlouisfed.org (allow-listed issuer, `references/authorities.yaml:12`, short `frbstl`)", needed_for: "L02 example of a real vintage series, only if a licence is quoted and the series is embedded; otherwise a citation of the source of the SIMULATED concept", confidence: "the source is in the curriculum (`curriculum/04-quant.yaml:584`) and in the review queue (`references/review_queue.json:1325-1328`); no record exists"}
- {doi: null, authors: "US Code / Federal Register (lead only)", year: null, title: "the statute or rule that sets US daylight-saving dates (lead only; not typed)", venue: "uscode.house.gov or ecfr.gov (allow-listed issuers, `references/authorities.yaml:15`, `:18`)", needed_for: "the convention in `et_to_utc` (§5.2). If no source is admitted, the convention is stated as the project's rule and not cited as law", confidence: "need certain; the planner did not read a source and types none"}
- {doi: null, authors: "tick-data and trade-quote literature (lead only; no author typed)", year: null, title: "a textbook or survey on trade and quote data and their timestamps", venue: "not typed", needed_for: "L05 grade-B claims about exchange versus receipt time, if made", confidence: "need certain; no record identified by this planner"}
- {doi: null, authors: "survivorship-bias literature (lead only; no author typed)", year: null, title: "empirical evidence on survivorship bias in stock samples", venue: "not typed", needed_for: "L06 counter-evidence for any graded claim about the size of the effect (BUILDER_RULES §2.5); the SIMULATED lab alone supports only a C-grade statement", confidence: "need certain; no record identified by this planner"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4).
Until resolved, QR1 teaches the models by derivation (Proposition 2.1, Derivation 4.1) and by SIMULATED labs (grade C with the
lab as basis). Each empirical sentence is graded C at most or removed.

---

## 8. Atlas milestone

None for QR1. The curriculum names no Atlas milestone for QR1 (`curriculum/04-quant.yaml:586-592`; `meta.yaml:199-206` lists
A2 for CS3). QR1's brief names the Atlas data layer (`:588-591`). Under B3(a) QR1 consumes A2 read-only through the public
functions `open_store`, `ingest`, `asof`, `verify` in `atlas/A2.contract.md:61-81`, and does not change A2's tables. No
`atlas/QR1.contract.md` is drafted. If the architect makes QR1 a milestone, a contract is needed before the project; that is a
curriculum change (`yaml:586-592`).

---

## 9. Cards builder (Builder F, after A to C)

- `course/modules/QR/QR1/cards.json`, ids `QR1-c001` upward (`check_pages.py` cards check; BUILDER_RULES §7).
- Every lesson L01 to L06 has at least one card. Expected total 30 to 50 cards: one per definition (7), one per misconception
  (at least 3 per lesson), and one per key result and lab result.
- Proposition 2.1 and Derivation 4.1 are grade T with no `cite` and the derivation named in `basis`, for example
  `"basis": "Proposition 2.1 (derivation on the page)"`.
- Lab results are grade C with `basis` naming the lab, for example `"basis": "Lab L02-1 (SIMULATED)"`. A card and its key-results
  row carry the same grade and basis (architect ruling 13).
- `cite` holds `croushore2001real` only where a card states the title-level fact (grade C), and is `[]` for model results.
- Each card tests one fact; each back is checkable against the lesson text; no trivia.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit QR1            # --page L03 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit QR1
.venv/bin/python tools/check_projects.py --unit QR1
.venv/bin/python tools/run_labs.py --unit QR1               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/QR/QR1/L01.html                             # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/QR/QR1/L02.html --refresh lab-QR1-L02-1     # after editing a twin
.venv/bin/python tools/run_graders.py --unit QR1 --seeds 0-49   # project only, after grader/ exists
.venv/bin/ruff check tests/labs/QR1 course/modules/QR/QR1/grader && .venv/bin/ruff format --check tests/labs/QR1
.venv/bin/mypy tests/labs/QR1 course/modules/QR/QR1/grader      # strict, repository configuration
```

Verifier only, on a quiet machine: `.venv/bin/python tools/mutate_graders.py --unit QR1 --seeds 0-9`,
`.venv/bin/python tools/page_smoke.py --unit QR1` (timing-sensitive; not run by builders), and the Pyodide probe for `sqlite3`
(§12 Q6). `tools/verify_refs.py --unit QR1` is the unit ledger's run (VERIFIER §2.1).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`,
`build_site.py --check`, `render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`,
`verify_refs.py --offline`, and the full gate in CLAUDE.md.

Flag checks: `tools/check_pages.py`, `check_dag.py`, `check_projects.py` accept `--unit`; `tools/run_labs.py` accepts `--unit`
and `--page`; `tools/run_graders.py` accepts `--unit` and `--seeds` (`[prior plan]` CS2 §10). The planner did not execute the
builder commands; only the coursekit closure, the concept-owner and built-unit functions, and the DST date arithmetic were run.

---

## 11. Tooling assumptions that do not hold, or are unverified, for QR1

1. **Lab runtime is `python` only.** `tools/run_labs.py:70-71` refuses any other runtime (read). The DuckDB lab cannot run (§0.3 B2).
2. **DuckDB is not pinned or vendored.** `requirements-dev.txt` (read) has no `duckdb`; `tools/vendor_spec.yaml:59` lists
   `numpy`, `scipy`, `pytest` only (read); `course/assets/vendor/LOCK.json` has no DuckDB or sqlite entry (planner grep). The
   grader and labs use the standard library only.
3. **Pyodide `sqlite3` is unverified** (`atlas/A2.contract.md:121-124`). The probe is §12 Q6.
4. **Time zones (`zoneinfo`) are not used** `[planner-derived]`: Pyodide's stdlib is not known to carry a tz database, and
   `tools/vendor_spec.yaml:59` lists no tz package. `et_to_utc` uses integer arithmetic on the dates in §5.2. The builders must
   not import `zoneinfo`; a verifier checks this with a grep.
5. **No Atlas contract for QR1.** `check_projects.py` checks a contract only when the project names an `atlas` key
   `[prior plan]` E5 §11.1 (`check_projects.py:144-146`, not re-read here). QR1 has none.
6. **No debate.** `check_pages.py` requires a debate brief only when the unit has a `debate` key `[prior plan]` E5 §11.2;
   QR1 has none (`curriculum/04-quant.yaml:566-592`).
7. **Autograder only.** No rubric, no exemplars, no question bank (`check_projects.py` `rubric_problems` runs only for `rubric`
   or `both`, `[prior plan]` CS2 §11.4). The spec's grading entry must name "autograder" (`check_projects.py:38`, `[prior plan]`).
8. **check_dag sees linked uses only** `[prior plan]` E5 §11.7. Unlinked uses of D1 to D7 pass the tool; the verifier reads for them.
9. **Rung minimums.** Tier M keeps rungs 1 and 2 minimal (`BUILDER_RULES.md:188`).
10. **Unbuilt prerequisites.** CS1, CS3, CS4, S0 and P0.1 have no built pages. Links go to `concepts.html` anchors only.
11. **Atlas A2 is proposed, not frozen.** The contract header says "architect to confirm" (`atlas/A2.contract.md:4`). Any QR1 test that imports
    the A2 copy depends on the contract being confirmed (§0.3 B1).
12. **Labs in Pyodide.** Each lab under 10 s in Pyodide; each grader test under 5 s in Pyodide and the suite under 60 s
    (`BUILDER_RULES.md` §5.3 item 4).

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **(BLOCKING, B1) Build order and A2.** Confirm `atlas/A2.contract.md` (currently untracked and "proposed"), and confirm that
   CS3 is verified before Builder C starts. **RECOMMENDED:** Builders A and B start now (lessons and labs do not need A2).
   Builder C waits. The grader carries a byte-identical copy of CS3's accepted A2 reference, pinned by SHA-256 in its docstring,
   and `grader/test_project.py` asserts the hash.
2. **(BLOCKING, B2) Lab runtime.** The curriculum lab reads "DuckDB ASOF JOIN point-in-time merge." (`curriculum/04-quant.yaml:585`).
   **RECOMMENDED:** adopt CS3 Q1 option (b), applied to QR1: the lab is `python`; a pure-Python ASOF reference with the A2 tie rule
   (`atlas/A2.contract.md:100-101`); the SQL listing labelled "SQL, not run"; the page says the DuckDB lab is not run. The architect
   accepts the change to the lab wording. Alternative: CS3 Q1 option (a) (a build-tool change; out of QR1's scope).
3. **(BLOCKING, B3a) "Atlas extension".** **RECOMMENDED:** QR1 ships `vintages.py`, a unit-local module that consumes A2
   read-only and adds its own SQLite table in its own file. A2 is unchanged. Not an Atlas milestone. If the architect wants
   A2's tables extended, that is a CONTRACT_CHANGE_REQUEST (`atlas/A2.contract.md:106-117`).
4. **(BLOCKING, B3b) "prove" versus autograder.** **RECOMMENDED:** keep `autograder` (`curriculum/04-quant.yaml:592`). The
   no-look-ahead property is proved in L02 (Proposition 2.1, grade T) and tested on 50 seeds. The brief's "prove" is read as
   "prove on the page and test in the grader". A wording change to the brief is optional.
5. **Publication-time storage.** A2's schema is fixed and keys on retrieval. **RECOMMENDED:** QR1's `VintageIndex(path)` opens
   its own SQLite file and writes its own table (no A2 table is touched). Confirm.
6. **Pyodide `sqlite3` probe.** **RECOMMENDED:** before Builder C's Pyodide run, load `sqlite3` in the vendored Pyodide and run
   one `SELECT 1`. If it fails, the reference switches to JSON-lines persistence (the `alt_3` style) and the tests stay the same.
7. **DST convention source for `et_to_utc`.** **RECOMMENDED:** keep `et_to_utc`, state its rule as the project's convention,
   and request a primary source (§7.2). If no source is admitted before the build, drop `et_to_utc`, tests T4 and T5, and
   mutants M09 and M10; replace M09 with "`visible` accepts a naive `t` as UTC" (killed by T9).
8. **Hours split.** **RECOMMENDED:** 6 lessons × 7 h and an 18 h project (30 %). Alternatives within the rules: 5 × 8 h with a
   20 h project (33 %); 7 × 6 h with an 18 h project (30 %).
9. **Concept placement.** **RECOMMENDED:** keep L03 with no defined concept (the curriculum lab). Alternative: move the lab
   to L02; then L02 defines 2 concepts and carries 2 labs.
10. **Outside concepts (§4).** **RECOMMENDED:** plain prose, no link, for D1 to D7 (`survivorship-bias`, `bid-ask-spread`,
    `limit-order-book`, `macro-data-revision`, the QR2 backtest terms, `llm-lookahead-contamination`, the CRSP and Compustat
    names). No prerequisite change. No DAG_DEFECT.
11. **Croushore content.** The record has no abstract (N4). **RECOMMENDED:** builders state the title-level fact only, at grade C
    with the key. Any broader claim requires the paper to be read; if the architect allows it, the locator is recorded and
    the grade is re-checked.
12. **Grader design.** **RECOMMENDED:** ten mutants M01 to M10 and five alternatives `alt_1` to `alt_5` as §5.4.3 and §5.4.4;
    seeds 0 to 49 for the reference and each alternative (ruling 10). The optional seed-0 hard-coded mutant is not required.
13. **Rungs.** **RECOMMENDED:** rung 1 (one worked example) and rung 2 (one completion lab) at minimum length, with rung 3 the
    graded project and rung 4 optional (BUILDER_RULES §5.1).
14. **Rubric.** **RECOMMENDED:** none. `grading` is `autograder` only (`curriculum/04-quant.yaml:592`). No question bank.
15. **Scope of the first-year grouping** does not apply to QR1. **RECOMMENDED:** no action.

---

## 13. After the builders

1. The orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01 to L02; L03 (the lab and the B2 wording); L04 to L06;
   the project (grader, mutants, alternatives on seeds 0 to 49, the Pyodide run). Failing rows return to the builder that owns
   the file, with only the failing rows.
3. Ledger at `ledgers/QR1.verification.json`; scripts under `ledgers/QR1/scripts/`; the ten mutants under `ledgers/QR1/mutants/`;
   equivalent mutants under `ledgers/QR1/equivalent/` with a README; the five alternatives under `ledgers/QR1/alternatives/`.
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 to B3 must be
   resolved or named as honest gaps first.

Architect decisions: pending (§12). This plan is the planner's proposal. Nothing in §12 is binding until the architect confirms it.

---

## Architect decisions (pending)

Pending. Where the plan states a RECOMMENDED decision for an open question in §12, the architect confirms or replaces it. Until then
the builders may start only the work that §0.3 marks as not blocked (Builders A and B for lessons and labs; Builder F after A to C).
