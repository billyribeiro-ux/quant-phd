# AC2 build plan: Haiku builders in parallel (2026-10-27)

Unit: **AC2 · Financial Statement Analysis & Earnings Quality** · tier U · 110 h · prerequisites AC1, S0 · Atlas
milestone **A15** (`atlas/A15.contract.md`, drafted by the architect) · grading `autograder` · output directory
`course/modules/AC/AC2/`. Third Phase-1 pilot (BLUEPRINT §9): the applied-style calibration after S7 (theory) and
AP1 (proof-heavy). Owner: orchestrator (architect). Executors: Claude Haiku builders, then independent Haiku
verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

## Rules for every builder (binding)

- Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `atlas/A15.contract.md`, this file.
  Study S7 (`course/modules/S/S7/`) and AP1 (`course/modules/AP/AP1/`) as the worked examples of the template,
  lab embedding, cards, project ladder and grader layout. Imitate their structure, not their wording.
- Evidence standard: every claim carries a grade and a registry key. The only AC2 keys are `penman2013financial`,
  `sloan1996stock`, `dechow1995detecting`, `piotroski2000value`, `beneish1999detection` (plus keys already used by
  AC1/S0-level material if you can show the key exists in `references/references.json`). A source you want that
  is not in the registry goes into `REFERENCE_REQUESTS`; never type bibliographic data, a table, a page or a
  coefficient from memory. A published number (a coefficient, a threshold, a sample statistic) is quoted only
  with a `data-locator` you have confirmed against the paper or a source that reproduces it; otherwise say in the
  text that it is unconfirmed (grade C at best) or leave it out.
- Concepts are defined once, with `<dfn id="def-<id>" data-concept="<id>">`, in the lesson assigned below, and
  linked elsewhere with `<a class="concept" data-concept="<id>">`. Prerequisite concepts (AC1: double-entry
  bookkeeping, accrual accounting, the three statements, articulation, depreciation, revenue recognition, leases,
  stock-based compensation, deferred taxes; S0: robust statistics, outliers, missing data, stale prices, ...) are
  usable without definition and linked, never re-taught.
- Lab code lives once, in its twin `tests/labs/AC2/<lab-id>.py`; the page carries `@@LAB:`/`@@OUT:` markers and
  `tools/embed_labs.py` fills them. Never type expected output. Labs run in Pyodide (NumPy, SciPy, standard
  library only, under 10 s, seeded, no network) and as the byte-identical twin under CPython.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/assets/data/*.json`,
  `course/index.html`, `course/concepts.html`, `references/*.json`, the market data snapshots, `MANIFEST.json`).
- **Real data.** EDGAR company-facts files are the real source, but embedding them needs the issuer's reuse
  statement quoted in `tools/data_sources.yaml` (BUILDER_RULES §6.6), and the SEC page that carries it has not
  been readable by automated access. Until a human supplies it, **labs and the autograder use generated filers,
  labelled SIMULATED, in the company-facts shape**, and every place the lesson would show a real filer shows an
  explicit honest-pending note naming the missing data request. Never invent figures that look like a real
  company's.
- Do not run `page_smoke.py` (timing-sensitive; verifiers run it on a quiet machine). Targeted checks only:
  `check_pages.py --unit AC2`, `check_dag.py --unit AC2`, `check_projects.py --unit AC2`, `run_labs.py --unit AC2`,
  `run_graders.py --unit AC2`, `ruff`, `mypy`, the unit's own tests. The unit is on branch `claude/ac2-a15`: it is
  incomplete until all four builders finish, so unit-level gates fail until then; check only your files.
- No `git commit`, no push. Report files written, commands run with exact output, and every gap or request
  (`GLOSSARY_REQUESTS`, `DATA_REQUESTS`, `REFERENCE_REQUESTS`, `CONTRACT_CHANGE_REQUESTS`, `DAG_DEFECTS`,
  `KNOWN_LIMITATIONS`) in the BUILDER_RULES output contract.

## Outline and file ownership (the architect's fixed assignment; do not move concepts between lessons)

| Lesson | Title (working) | Concepts it defines | Lab (twin id) | Owner |
|---|---|---|---|---|
| L01 | Filings as data: XBRL facts and standardization | `xbrl-standardization` | `lab-AC2-L01-1`: parse a generated company-facts mapping, apply the annual-observation and as-of rules, standardize to the A15 items | Builder A |
| L02 | Ratio analysis and the DuPont decomposition | `financial-ratio-analysis`, `dupont-decomposition` | `lab-AC2-L02-1`: DuPont decomposition from XBRL data (the curriculum lab) on a generated filer, identity checked | Builder A |
| L03 | Return on invested capital | `return-on-invested-capital` | `lab-AC2-L03-1`: NOPAT, invested capital, ROIC and its sensitivity to the tax-rate convention | Builder A |
| L04 | Earnings and cash-flow quality; operating accruals | `earnings-quality`, `accruals` | `lab-AC2-L04-1`: both accrual measures on a generated panel | Builder B |
| L05 | The accruals anomaly (Sloan 1996) | `accruals-anomaly` | `lab-AC2-L05-1`: a simulated accrual-sorted portfolio study, labelled SIMULATED, with the honest-pending note for real data | Builder B |
| L06 | Earnings management and discretionary accruals | `earnings-management`, `modified-jones-model` | `lab-AC2-L06-1`: the modified Jones regression on a generated cross-section with a planted manipulation | Builder B |
| L07 | The Piotroski F-score | `piotroski-f-score` | `lab-AC2-L07-1`: the nine signals on generated firm-years | Builder C |
| L08 | The Beneish M-score; using the scores together | `beneish-m-score` | `lab-AC2-L08-1`: the eight indices and M on generated firm-years; Beneish constants per the contract's rule | Builder C |
| index | Hub: module map, prerequisites, hours, retrieval-practice entry points | none | none | Builder A |
| project | Atlas A15: fundamentals engine (autograder) | none | `lab-AC2-project-1..3` (rungs 1-3) | Builder D |
| grader | `grader/reference.py` (the A15 reference: `atlas/fundamentals` contract), `starter.py`, `instance.py` (seeded generated filers: valid, answers differ across seeds), `test_project.py` | none | none | Builder D |
| cards | `cards.json`: one card per misconception and key result of L01-L08, with the retrieval-engine fields S7/AP1 use | none | none | Builder E (after A-C) |

Every lesson follows the lesson template (BUILDER_RULES / `course/templates/`): objectives, definitions, results with
proofs or derivations where a result is claimed, worked examples, misconceptions, a lab, a quiz, and the evidence
grades and locators. `tools/check_pages.py` requires 6-12 declared study hours per lesson; the hub declares the split (lessons 76 h,
project 34 h = 110 h) and every page must agree with it. Report the hours you estimate per lesson.

## Project ladder (Builder D), per BLUEPRINT §5 and the AP1 example

Rung 1: a fully solved and annotated `standardize` on a small generated filer. Rung 2: a completion problem
(`dupont`, `roic`, accruals) graded instantly. Rung 3: the independent A15 library to the contract
(`modified_jones`, `piotroski_f_score`, `beneish_m_score`). Rung 4: open-ended stretch (an industry-adjusted
quality screen with a stated hypothesis). Autograder only: `run_graders.py --seeds 0-49`, every instance valid,
instances differing materially; failure messages name the violated property and never leak the answer.
The grader runs identically in the browser (Pyodide) and under pytest.

## After the builders

1. Orchestrator integrates, runs the unit gates once, fixes cross-lesson defects (DAG, links, hours).
2. Independent Haiku verifiers (VERIFIER_RULES; slices L01-L02, L03-L04, L05-L06, L07-L08, project) in fresh
   checkouts; the project verifier writes at least three mutants per round; failures return to a builder with
   only the failing rows. Verification repeats until each slice is all PASS or the remaining rows are named,
   honest gaps. Verifier scripts are archived under `ledgers/AC2/scripts/` (VERIFIER_RULES §3).
3. Branch `claude/ac2-a15` is merged only when the unit ledger is PASS or its gaps are agreed; it is never merged
   incomplete, because an unfinished unit breaks `check_pages --all`.
