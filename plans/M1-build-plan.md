# M1 build plan: Precalculus & Mathematical Reasoning (2026-10-27)

Unit: **M1 · Precalculus & Mathematical Reasoning** · tier F · 100 h · prerequisites P0.1 · no Atlas milestone ·
grading `both` (autograder + rubric) · output directory `course/modules/M/M1/` (part code `M`).
Planner: Haiku, plan only. No lesson content, no git operations. Executors: Haiku builders, then independent Haiku
verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence citations below are `file:line` read during planning. Anything not in the curriculum is marked as such.

## Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part M, code `M`, title "Mathematics"; studio STUDIO-M requires M7, M8 (not M1) | `curriculum/01-foundations.yaml:71`, `:73-76` |
| M1 id, title, tier F, hours 100, prereqs [P0.1] | `curriculum/01-foundations.yaml:87-91` |
| M1 core text (algebra, functions, exp/log, sequences and series, sets, quantifiers, direct proof, contradiction, induction) | `curriculum/01-foundations.yaml:92-95` |
| M1 introduces 14 concepts | `curriculum/01-foundations.yaml:96-110` |
| M1 sources: Velleman, How to Prove It, 3rd ed. (2019) (free text, not a key) | `curriculum/01-foundations.yaml:111-112` |
| M1 lab: "Compounding-frequency convergence to e^{rt}." | `curriculum/01-foundations.yaml:113` |
| M1 project "Annuity and mortgage engine", grading `both`, deliverable "Proofs and a tested Python module" | `curriculum/01-foundations.yaml:114-121` |
| M1 has no `debate` key, so no debate brief is required (`check_pages.py` line 412 keys on `u.entry.get("debate")`) | `curriculum/01-foundations.yaml:87-121` (absent) |
| M1 has no Atlas milestone: the 20 `atlas` entries (A1-A20) name modules CS1, CS3, S0, S4, FI1, DV4, F1, S7, QR2, MS3, PR2, PR4, FI3, CR1, AC2, CF4, QR3, GM1, SR3, GM4; none is M1 | `curriculum/meta.yaml:198` (atlas block), `:200-276` (module lines) |
| The JSON row for M1 mirrors the YAML (id, hours 100, prereqs, 14 introduces, sources, lab, grading both) | `curriculum/curriculum.json` from line 6313 |
| The rendered CURRICULUM.md M1 block agrees | `CURRICULUM.md:214-221` |
| Registry key for Velleman exists: `velleman2019prove`, status verified, Crossref monograph, used_by ["M1"] | `references/references.json:22141` |

Note: the curriculum's `sources` field is free text; the registry key `velleman2019prove` is the only registry entry
whose `used_by` names M1. The builder cites the key, never the free-text string.

## Rules for every builder (binding)

- Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, this file. Study
  `course/modules/S/S7/` and `course/modules/AP/AP1/` for template, ladder and grader layout, and
  `course/modules/AC/AC2/` for the lab-id and hours conventions. Imitate structure, not wording.
  `course/templates/` holds hub.html, lesson.html, project.html, studio.html.
- Evidence standard: every claim carries a grade and a registry key. Theorems and derivations are grade **T** and need
  a complete proof on the page. Derivation steps are shown in full (BUILDER_RULES §3.5). Do not cite a source for a
  result you derive.
- Concepts: each is defined once, with `<dfn id="def-<id>" data-concept="<id>">`, in the lesson assigned below, and
  linked elsewhere with `<a class="concept" data-concept="<id>">`. A lesson never links a concept defined in a later
  lesson (`check_dag.py`). M1's only prerequisite is P0.1, so no concept from M2 or later may be linked or defined
  (see open question Q1 on `limit`).
- Labs: code lives once, in the twin `tests/labs/M1/<lab-id>.py`; the page carries `@@LAB:`/`@@OUT:` markers and
  `tools/embed_labs.py` fills them. Never type expected output. Labs are seeded, use the standard library only
  (`fractions`, `decimal`, `math`, `itertools` are enough; no NumPy is needed), run under 10 s in Pyodide, and need no
  network. Lab ids must match `lab-M1-<page>-<n>` (`check_pages.py` line 258).
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`,
  `course/concepts.html`, `references/*.json`, `course/assets/data/*`).
- No real data is used in this unit (§Real-data policy). Every number is computed, quoted with a locator, or derived.
- Do not run `page_smoke.py`. Targeted checks only (see §Commands).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap or request in the
  BUILDER_RULES §10 output contract.

## Outline and file ownership

Lesson count is derived, not guessed. The hub declares lessons + project = 100 h (`check_pages.py` lines 337-342).
Project = 30 h (30 %, inside the 10-40 % band at `check_pages.py` line 339). Lessons = 70 h. Each lesson is 6-12 h
(`check_pages.py` line 227), so 70 h allows 6 to 11 lessons. Eight lessons are chosen so the 14 concepts group into
coherent units and the proof tools (logic, then induction) come before the formulas that need them.

| Lesson | Title (working) | Concepts it defines | Lab (twin id) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Sets, quantifiers and logical statements | `quantifiers` | `lab-M1-L01-1`: evaluate quantified statements over finite sets by brute force; check negations | 8 | Builder A |
| L02 | Direct proof and proof by contradiction | `direct-proof`, `proof-by-contradiction` | `lab-M1-L02-1`: exhaustive check of a direct-proof claim on a finite range; a contradiction proof checked by a counterexample search that finds none | 9 | Builder A |
| L03 | Exponential and logarithm functions | `exponential-and-logarithm` | `lab-M1-L03-1`: identities \(e^{a}e^{b}=e^{a+b}\) and \(\ln(e^{x})=x\) checked to tolerance | 9 | Builder A |
| L04 | Compounding frequency and continuous compounding | `compounding-frequency`, `continuous-compounding` | `lab-M1-L04-1` (**the curriculum lab**): \((1+r/m)^{m}\) converges to \(e^{r}\) as \(m\) grows, with the error column printed | 9 | Builder B |
| L05 | Present value and the discount factor | `present-value`, `discount-factor` | `lab-M1-L05-1`: discount factors \(1/(1+r)^{t}\) and \(e^{-rt}\) compared across conventions | 8 | Builder B |
| L06 | Geometric series and proof by induction | `mathematical-induction` (defined first, used for the sum), `geometric-series` | `lab-M1-L06-1`: \(\sum_{k=0}^{n-1} q^{k}=(1-q^{n})/(1-q)\) checked for \(n\le 60\) | 9 | Builder C |
| L07 | Annuities, perpetuities and growing perpetuities | `annuity`, `perpetuity`, `growing-perpetuity` | `lab-M1-L07-1`: annuity closed form against direct summation; growing-perpetuity limit case and the \(r > g\) condition | 9 | Builder C |
| L08 | Loan amortization schedules | `amortization-schedule` | `lab-M1-L08-1`: a full amortization table for an illustrative loan; balance reaches zero, and interest + principal = payment | 9 | Builder C |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split | none | none | - | Builder A |
| project | Annuity and mortgage engine (`both`) | none | `lab-M1-project-1..3` (rungs 1-3) | 30 | Builder D |
| grader | `grader/reference.py`, `starter.py`, `instance.py`, `test_project.py` | none | none | - | Builder D |
| cards | `cards.json` from L01-L08 | none | none | - | Builder E (after A-C) |

Totals: lessons 8+9+9+9+8+9+9+9 = 70 h; project 30 h; unit 100 h. Matches the curriculum's 100 h.

Concept coverage check: 1+2+1+2+2+2+3+1 = 14 concepts, each in exactly one row, matching the 14 entries at
`curriculum/01-foundations.yaml:97-107`.

Ordering check: L04 uses L03's exponential; L05 uses L04's compounding; L06 defines induction before the geometric sum
that needs it; L07 uses L05 (present value) and L06 (geometric series); L08 uses L07's annuity. No lesson links a later
definition.

Note on the `core` text: "sets", "functions", "algebra" and "sequences" appear in the curriculum core (`:92-95`) but are
not in `introduces` (`:96-110`). They are taught as prose in L01, L03 and L06 with no `<dfn>` (open question Q3).

## Hub (index.html, Builder A)

- `<main data-hours-lessons="70" data-hours-project="30">` (sums to the curriculum 100).
- 4-8 measurable objectives; prerequisites linked to P0.1 with its concept links.
- Placement diagnostic: `<section class="quiz" id="placement" data-unit="M1" data-page="placement" data-mastery="0.8">`,
  matching the AP1 bar (`course/modules/AP/AP1/index.html:77`). It has at least two `data-skill` items that test
  what rungs 1-2 teach (the worked example's task and the completion problem's missing step), and the rest test P0.1.
- Lesson map linking L01-L08. Project ladder with four rungs (`ol.ladder`, rung titles in order).
- Tier F keeps rungs 1-2 at full length (BLUEPRINT §4: the minimum applies from tier M upward).

## Project ladder (Builder D)

Per BUILDER_RULES §5.1 and the AP1 example (`course/modules/AP/AP1/project.html:43-47`):

1. Rung 1 · Worked example: a fully solved, annotated closed-form computation for a fixed annuity (`lab-M1-project-1`).
2. Rung 2 · Completion problem: the same task with the induction step and the amortization update removed; graded
   instantly (`section.lab.completion`, `lab-M1-project-2`; `check_projects.py` line 90 requires it or a quiz).
3. Rung 3 · Independent project: `annuity_engine.py` (proposed name, Q5) with the closed forms for annuity, perpetuity,
   growing perpetuity, and the amortization schedule, plus the proof write-up. Graded by the autograder and the rubric.
   `lab-M1-project-3` is the rung-3 check.
4. Rung 4 · Stretch: an open-ended extension with no ceiling (for example, a schedule with irregular payments, or a
   proof that the amortization balance is a geometric sequence), suitable for the portfolio.

### Time budget (`<table id="hours">`, declared 30 h, every row needs a one-line rationale)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1 worked example | 2 | Read and annotate one closed-form computation |
| Rung 2 completion | 3 | Fill two induction and recurrence steps, then run the instant check |
| Derivations and proof write-up | 8 | Induction and geometric series for the three closed forms; the written proofs |
| Annuity, perpetuity and growing-perpetuity module with tests | 7 | Implement and check against direct summation |
| Amortization schedule | 6 | Balance recurrence, the final-payment rule, and the sum identities |
| Report and self-assessment | 4 | Half-page rationale; score against the exemplars |
| **Total** | **30** | Equals `data-hours-project` on the hub |

## Grader design (Builder D)

Grading is `both`. `check_projects.py` requires the spec's grading entry to name both "autograder" and "rubric"
(`tools/check_projects.py` lines 41-50). The project page needs a `section.grader-panel` with `data-unit="M1"`,
`data-grader="grader/"`, `data-suite="test_project.py"`, `data-support="instance.py"`,
`data-solution="annuity_engine.py"`, `data-starter="starter.py"` (`check_projects.py` lines 122-135).
No `data-packages` is needed: the grader is standard-library only.

- `grader/instance.py`: `make_instance(seed: int) -> dict`. Deterministic per seed. Generates a valid instance only:
  annual rate \(r > 0\), periods \(n \ge 1\), growth \(g\) with \(g < r\) for the growing-perpetuity cases, and a
  principal. Labelled in the docstring as **generated inputs, not real loan or market data**. Seeds 0-49 give materially
  different answers, not just different labels.
- `grader/reference.py`: the full solution. Must pass every test on seeds 0-49 (`run_graders.py --unit M1 --seeds 0-49`).
- `grader/starter.py`: stubs that raise `NotImplementedError`. The starter must fail the suite (`run_graders.py` checks
  that it does).
- `grader/test_project.py`: pytest suite checking properties and numbers:
  - annuity, perpetuity and growing-perpetuity closed forms against direct summation, to a stated relative tolerance;
  - amortization: the final balance reaches zero to tolerance; per period, payment = interest + principal; total
    principal = the loan;
  - edge cases: \(r = 0\) must be handled explicitly or fail loudly, never divide by zero silently; \(r \le g\) for the
    growing perpetuity raises `ValueError`;
  - invalid input fails loudly with a message naming the condition.
  - Failure messages name the violated property and hint at the concept. They never print the answer.
- Mutants the verifier must write (VERIFIER §2.6; at least three, each must be killed), suggested by the builder but
  written by the verifier:
  1. annuity-due timing used for an ordinary annuity (off-by-one period);
  2. growing-perpetuity with no \(r > g\) guard, returning a negative value;
  3. nominal rate used as the per-period effective rate in the monthly amortization;
  4. last payment not adjusted, leaving a residual balance;
  5. a hard-coded answer for seed 0.

## Cards builder (Builder E, after A-C)

- `course/modules/M/M1/cards.json`, ids `M1-c001` upward, `lesson` in L01-L08, one card per definition, theorem,
  key formula, the worked-example result and each misconception (BUILDER_RULES §7).
- Grade T for every theorem and derived formula, with `"basis"` naming the lab or problem where the lesson itself
  establishes a numerical result (for example `"basis": "Lab 4, Problem E2 (simulation)"`). Cite a registry key only
  for an empirical claim. M1 has no empirical claims, so `cite` is empty on every card.
- `check_pages.py` checks the unit prefix, the lesson existence, the grades and the registry keys.

## Registry keys the module may cite

| Key | Status | Use in M1 |
|---|---|---|
| `velleman2019prove` | verified, Crossref monograph (`references/references.json:22141`) | the curriculum source for proof technique (L01, L02, L06); cite with locators for any statement about proof methods |
| `spivak2008calculus` | verified, Open Library book, used_by ["M2"] | not curriculum-listed for M1; usable only if the architect approves (Q4) |
| `brealey2022principles` | verified, Open Library book, used_by ["CF1","CF8"] | not curriculum-listed for M1; any use needs a confirmed locator (Q4) |

The other keys in the module's lessons (retrieval, scheduling, learning science) belong to P0.1 and P0.2 and are not
needed on M1 pages. The M1 learning-system claims are not made on these pages.

## REFERENCE_REQUESTS

- None required by the curriculum. The curriculum's one named source is registered. The builder must not cite a
  textbook for a formula it derives on the page. If a builder wants a source for a convention (for example day count in
  L05), the request goes here with a DOI or ISBN, and the architect resolves it through `add_reference.py`. Planner did
  not verify any new source, so none is requested.

## Real-data policy

- No real data is needed. M1 is precalculus and proof, and its labs and grader compute from formulas.
- Illustrative loans in L08 and the project are labelled "illustrative input, not data". The grader instances are
  labelled **SIMULATED** in their docstring, with the same wording on the project page (BLUEPRINT §5.3).
- Do not use FRED mortgage rates, Treasury yields or any other public series in M1. Such a series would need a
  redistribution check under BUILDER_RULES §6.6, and the curriculum does not call for one. No DATA_REQUESTS.
- No `data-files` attribute on any lab; no MANIFEST entry.

## Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

```bash
.venv/bin/python tools/check_pages.py --unit M1          # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit M1
.venv/bin/python tools/check_projects.py --unit M1
.venv/bin/python tools/run_labs.py --unit M1             # --page L04 for one lesson
.venv/bin/python tools/run_graders.py --unit M1 --seeds 0-49
.venv/bin/python tools/mutate_graders.py --unit M1 --seeds 0-9   # verifier only
.venv/bin/ruff check tests/labs/M1 course/modules/M/M1 && .venv/bin/ruff format --check tests/labs/M1
.venv/bin/mypy tests/labs/M1 course/modules/M/M1/grader
```

Notes:
- `check_pages`, `check_dag` and `check_projects` already accept `--unit` (`tools/check_pages.py` line 429,
  `tools/check_dag.py` line 89, `tools/check_projects.py` line 159). `run_labs.py` takes `--unit` and `--page`
  (`tools/run_labs.py` lines 119-121). `run_graders.py` takes `--unit` and `--seeds` (`tools/run_graders.py` lines
  129-131). `mutate_graders.py` takes `--unit` and `--seeds` (`tools/mutate_graders.py` lines 30-32).
- `page_smoke.py` is not run by builders. Verifiers run it on a quiet machine.
- `mypy` targets are a suggestion; the project's gate is `.venv/bin/mypy` with its own config (strict). Confirm the
  paths before running.

## Tooling assumptions that do not hold for this module type

1. **No Atlas milestone.** `check_projects.py` only checks `atlas/<id>.contract.md` if the project names one
   (`tools/check_projects.py` lines 145-146). M1 names none, so no contract is needed.
2. **No debate.** The curriculum tags no debate, so `check_pages.py` does not require a debate brief (line 412).
3. **Foundations graded `both`.** This is not a pure autograder unit: the rubric and exemplars are required by
   `check_projects.py` lines 138-139, which applies to any project graded `rubric` or `both`. Two exemplars at two
   levels are needed.
4. **Lessons with one curriculum lab.** The curriculum names one lab (`curriculum/01-foundations.yaml:113`). The
   BUILDER_RULES §3.4 rule ("every key formula gets a numerical check in a lab") requires more. The plan adds one lab
   per lesson (Q2).
5. **Limit-dependent proof.** The convergence of \((1+r/m)^m\) to \(e^r\) is a limit result. The concept `limit` is M2's,
   so the lesson cannot link it (Q1). Without a resolution, this is a DAG_DEFECT.
6. **No data-driven figure.** BUILDER_RULES §6.4-6.6 charts need a source line and retrieval date. M1 figures, if any,
   plot formula output and carry the line "computed from the formula; no data".

## Open questions for the architect

- **Q1 (DAG).** The continuous-compounding lesson (L04) needs \((1+r/m)^m \to e^r\). The concept `limit` belongs to M2
  (`curriculum/01-foundations.yaml:133`). Choose one: (a) L04 states the convergence as a numerical check and treats
  continuous compounding as the defined limit, with no proof of the limit; (b) record a DAG_DEFECT and move the
  limit-based proof to M2; (c) allow a forward reference. The planner recommends (a).
- **Q2 (lab count).** Confirm one lab per lesson (eight twins, plus three project labs), not just the curriculum's
  single compounding lab.
- **Q3 (concepts in core text).** "sets", "functions", "algebra" and "sequences" are in the core text but not in
  `introduces`. Confirm they stay as prose without `<dfn>`, or ask for them to be added to the curriculum. The planner
  cannot change the curriculum.
- **Q4 (sources).** Confirm that `velleman2019prove` is the only source the builders may cite for proof technique.
  Confirm whether `spivak2008calculus` (used_by M2) or `brealey2022principles` (used_by CF1, CF8) may be cited from M1.
- **Q5 (project specification).** Confirm the module name `annuity_engine.py` and the amortization convention: monthly
  compounding of a nominal annual rate, equal payments, and the final-payment rule. The curriculum names the project
  "Annuity and mortgage engine" but does not fix the convention (`curriculum/01-foundations.yaml:114-121`), so the
  grader needs a stated one (BLUEPRINT §5.2 integrity rule applies).
- **Q6 (hours).** The split is 70 h lessons / 30 h project. Confirm, or ask for a different project share within 10-40 %.

## After the builders

1. Orchestrator integrates; runs the targeted commands above once; fixes cross-lesson defects (DAG, links, hours).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L03, L04-L05, L06-L08, project. The project verifier
   writes at least three mutants per round (VERIFIER §2.6). Failing rows return to the builder only.
3. Ledger at `ledgers/M1.verification.json`; verifier scripts archived under `ledgers/M1/scripts/`.
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed.

## Architect decisions (2026-10-27, binding)
Q1: state the limit (1+r/m)^m -> e^r as a numerical observation with the error column; do not prove it and do not use the concept `limit` (M2). Q2: one lab per lesson. Q3: sets, functions, algebra, sequences stay undefined prose. Q4: cite only `velleman2019prove`. Q5: module `annuity_engine.py`; amortization convention is monthly compounding of a nominal rate, final payment adjusted so the balance is exactly zero, money in integer cents. Q6: 70/30 split confirmed.
