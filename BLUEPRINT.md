# Master Blueprint — Doctoral-Track Major in Finance, Economics & Quantitative Markets

**Version:** 2.1 (2026-10-11) · **Chief architect:** Claude · **Owner:** Billy Ribeiro

**Companion files:**

| File | Role |
|---|---|
| [`CURRICULUM.md`](CURRICULUM.md) | The full curriculum: 134 modules, 157 graded projects, and the degree-equivalent credential maps. Generated, never hand-edited |
| [`curriculum/*.yaml`](curriculum/) | Source of truth for the curriculum |
| [`tools/render_curriculum.py`](tools/render_curriculum.py) | Validator and renderer for the curriculum |
| [`BUILDER_RULES.md`](BUILDER_RULES.md) | Binding system prompt for builder agents |
| [`VERIFIER_RULES.md`](VERIFIER_RULES.md) | Binding system prompt for the independent verifier agents |

---

## 1. What this is

This is one continuous program. A student starts with high-school algebra and
finishes holding a defended doctoral thesis. It covers what a top university
spreads across several separate degrees, with no repetition between them:

- **A complete Finance degree.** Corporate finance, valuation, financial
  modeling, working capital and treasury, corporate risk management and
  international finance; financial and managerial accounting and statement
  analysis; investments and equity research; fixed income and derivatives;
  financial markets and institutions; asset management; household finance and
  wealth management; private markets and real estate; financial history, law
  and professional conduct; and a senior capstone. See §1.1.
- **The economics it rests on.** Micro, game theory and information,
  decision theory, macro I and II, monetary, international, and sovereign
  debt and crises.
- **The mathematics, statistics and computing underneath both.** Proof and
  analysis, measure-theoretic probability, optimization and numerical methods;
  inference, econometrics, time series and research integrity; Python, SQL,
  C++, software engineering and HPC.
- **The quantitative and macro specialization.** Stochastic calculus, asset
  pricing theory, empirical asset pricing, portfolio and risk,
  microstructure and execution, quant research engineering, FX and
  commodities, global macro trading, systemic risk.
- **The doctorate.** Qualifying exams, refereeing and replication, the twelve
  great debates of the field, and an original thesis.

**Exit standard.** The graduate can do the following:

1. pass first-year PhD qualifying exams in asset pricing, econometrics and
   macro/monetary
2. derive the canon from first principles
3. replicate published results, and diagnose why replications diverge
4. argue every major open debate from graded evidence
5. ship production research code
6. value a company, structure a deal, and defend a trade in front of a hostile
   investment committee

Undergraduate, master's and PhD courses each teach mostly theory, and each
assumes the student will pick up implementation somewhere else. This program
puts the theory, the replication evidence and the implementation in the same
place.

### 1.1 The degrees inside this program

Three named Finance credentials are built into the curriculum. Each one is an
explicit, machine-checked view over the module graph. The validator proves
three things about each:

- it includes every prerequisite it depends on
- it never reaches above its tier
- every course in its course map is actually inside it

`CURRICULUM.md` carries the full course-by-course map for each.

| Credential | What it covers | Modules | Graded projects | Hours | Credit equivalent | FTE years |
|---|---|---|---|---|---|---|
| **Finance Degree — Bachelor's Level** | Business and quantitative core (calculus, statistics, econometrics, programming, micro, macro, financial and managerial accounting, law and ethics, communication), plus the full finance major (corporate finance I–II, investments, markets and institutions, statement analysis, valuation, financial modeling, short-term finance, fixed income, derivatives, risk management and international finance, asset management, wealth management, financial history), plus a senior capstone | 42 | 47 | 3,881 | ≈86 credits | 1.80 |
| **Master's in Finance / Financial Engineering** | Stochastic calculus, derivatives pricing, computational finance, financial econometrics, asset pricing, portfolio and risk management, plus electives in rates, credit, factors, microstructure, ML, quant research, advanced corporate finance, alternatives, international finance, and volatility | 76 | 84 | 7,546 | ≈168 credits | 3.49 |
| **PhD in Finance** | The first-year sequence (asset pricing theory, empirical asset pricing, continuous-time finance, corporate finance theory, econometrics, micro and macro theory), field courses, qualifying exams, replication, the great debates, and the dissertation | 83 | 87 | 9,171 | ≈204 credits | 4.25 |

Some facts about these numbers:

- Credential hours include every prerequisite the credential pulls in.
- The credentials overlap, so a student who completes the Master's has
  already completed most of the Bachelor's.
- The Bachelor's figure (≈86 credits) is the finance, business-core and
  quantitative content of a 120-credit degree. The remaining credits of a
  conventional degree are general-education requirements, which the program
  deliberately omits.

**External check.** The finance content is also mapped topic by topic to the
CFA Program curriculum topic areas: ethics, quantitative methods, economics,
financial statement analysis, corporate issuers, equity, fixed income,
derivatives, alternatives, and portfolio management and wealth planning. The
validator checks that every mapped module exists. Phase 0 verifies the topic
list against CFA Institute's current outline.

**These are content-equivalent credentials, not degrees.** Only an accredited,
state-authorized institution can award a degree. Market them as "Finance
Degree–equivalent curriculum" or similar. Never market them as a degree.

---

## 2. Where the time is saved (numbers, not slogans)

All figures below are computed by `tools/render_curriculum.py` from the
curriculum sources. They are not estimates typed into this document.

The calibration anchor is the U.S. federal credit-hour definition (34 CFR
600.2). One credit is about 45 hours of student work, so a three-credit course
is about 135 hours and a 120-credit bachelor's degree is about 5,400 hours.
Module hours are sized against the university course content each module
replaces. Every hour figure includes the module's project.

| Milestone | Cumulative hours | Full-time years* |
|---|---|---|
| All F + U tiers (whole major incl. economics & computing) | 4,345 | 2.01 |
| + all M tier (Master's-equivalent breadth) | 11,135 | 5.16 |
| + all D tier, quals (Doctoral Candidate) | 12,495 | 5.78 |
| + thesis (Doctoral) | 13,695 | 6.34 |

\*At 45 hours/week for 48 weeks/year. That is a full-time professional pace,
not a student pace.

Job-ready career tracks are the prerequisite closures of each track's target
modules. They take 1.4–2.4 full-time years. See the table in `CURRICULUM.md`.

The savings come from six mechanisms, and every one of them is designed in:

1. **No general-education or distribution requirements.** Every hour serves
   the exit standard.
2. **No re-teaching across degree levels.** A university teaches CAPM,
   regression and options three times: in the bachelor's, the master's and the
   PhD. Here each concept is defined exactly once in the prerequisite graph and
   then reused. `check_dag.py` enforces this.
3. **Year-round calendar.** Two 15-week semesters give about 30 instructional
   weeks a year. The program runs 48.
4. **Placement test-outs.** Each module opens with a diagnostic. A student who
   scores at the mastery bar on it moves straight to the module project.
5. **Projects that compound.** The program-long Atlas build (§5) means the
   data layer from month 2 runs inside the thesis. Nothing is thrown away.
6. **Research starts early.** Replication, the integrity protocol and
   self-refereeing are graded from the master's tier onward. The thesis grows
   out of work the student already owns.

The hours remain design targets. Phase 1 pilot learners recalibrate them, and
the generated tables update automatically.

---

## 3. The evidence standard (non-negotiable)

Every substantive claim on every page carries an evidence grade and at least
one citation key from the verified reference registry.

| Grade | Meaning | Allowed phrasing |
|---|---|---|
| **T** | Theorem: proved on the page, or with a precisely cited proof | "Theorem.", "It follows that" |
| **A** | Replicated out of sample by independent teams, across periods and/or markets | "The evidence shows" |
| **B** | Published in a top peer-reviewed venue, but not robustly replicated or actively contested | "Published evidence indicates…; contested by…" |
| **C** | Working paper, practitioner research, or single-sample evidence | "One study finds…" |
| **D** | Practitioner lore with no systematic evidence | Only as "It is widely claimed…", always flagged |
| **X** | Refuted, failed replication, or retracted | "Earlier work claimed…; this did not survive…" |

The rules that follow from it:

- **Where numbers can come from.** Every number in prose is either computed
  live on the page from embedded data, quoted from a source with an exact
  locator (table, panel, equation or page), or derived on the page.
- **Contested claims are two-sided.** A claim graded B or C must name its
  published counter-evidence. One-sided treatment is a build failure.
- **Memory is a lead, not a source.** Model recall supplies candidate
  citations and numbers. Every citation enters the registry only through a
  DOI→Crossref lookup. An independent verifier then checks every attribution
  and every quoted number against the source (`VERIFIER_RULES.md`). Errors are
  caught by machinery rather than by trusting any model's confidence. This is
  what lets the program survive hostile review by the people it cites.
- **Freshness.** The knowledge base runs to mid-2026. The verifier checks
  every working paper for a later published version, and every debate for
  2025–2026 contributions.
- **The standard covers how the program teaches, too.** Section 4 is held to
  the same grades.

---

## 4. The learning system, built on learning-science evidence

| Mechanism | Evidence | Grade | How it is built |
|---|---|---|---|
| **Retrieval practice** beats rereading | Roediger & Karpicke (2006), *Psych. Science* 17(3); Dunlosky et al. (2013), *PSPI* 14(1) | A | Every lesson ends in a retrieval quiz. Spaced-retrieval cards are generated from every definition, theorem and key result |
| **Spaced practice** beats massed practice | Cepeda et al. (2006), *Psych. Bulletin* 132(3) | A | An in-browser scheduler (FSRS-family algorithm; Ye, Su & Cao 2022, KDD [V]) resurfaces cards across the whole program, so Part 1 stays alive in Part 20 |
| **Worked examples** before problem solving, for novices | Sweller & Cooper (1985), *Cognition & Instruction* 2(1); Atkinson et al. (2000), *RER* 70(2) | A | Rung 1 of the project ladder (below) |
| **Fading** scaffolds as competence grows | Renkl & Atkinson (2003), *Ed. Psychologist* 38(1) | B | Rung 2: completion problems |
| **Expertise reversal:** scaffolding hurts experts | Kalyuga, Ayres, Chandler & Sweller (2003), *Ed. Psychologist* 38(1) | A | Placement test-outs skip rungs 1–2 for students who already have the skill |
| **Active learning** beats lecture | Freeman et al. (2014), *PNAS* 111(23) | A | Labs run inline in the argument, not at the end; every section has a do-something element |
| **Interleaving** of problem types | Rohrer & Taylor (2007), *Instructional Science* 35 | B | Review sets and quals mix topics, so students must choose the method themselves |
| **Self-explanation** | Chi et al. (1989), *Cognitive Science* 13(2) | B | Proof modules require written step justifications, graded on rubric |
| **Mastery learning** | Kulik, Kulik & Bangert-Drowns (1990), *RER* 60(2) | B | A module unlocks only after its prerequisites' projects pass. The mastery bar is set per module |
| **Rubrics with exemplars** | Jonsson & Svingby (2007), *Educational Research Review* 2(2) [V] | B | Every rubric-graded project ships annotated exemplars at two or more quality levels |

**Projects, maximized, in the right order.** The evidence does not support
throwing novices into open-ended projects. Kirschner, Sweller & Clark (2006,
*Ed. Psychologist* 41(2)) show that minimally guided instruction underperforms
for novices. Hmelo-Silver, Duncan & Chinn (2007, *Ed. Psychologist* 42(2))
reply that well-scaffolded problem-based learning works. Both sides agree on
the synthesis: projects are most effective when scaffolding fades as skill
grows.

So every module runs a four-rung **project ladder**:

1. **Worked example:** a fully solved instance, annotated.
2. **Completion problem:** a partially solved instance that the student
   finishes.
3. **Independent project:** the graded module project, specified in the
   curriculum.
4. **Stretch:** an open-ended extension with no ceiling, which feeds the
   student's portfolio.

Placement results skip rungs 1–2. By the master's tier, rungs 1–2 shrink to
the minimum, because the expertise-reversal evidence says they start to hurt.

Two contested claims are deliberately left out of the design. Bloom's (1984)
"2-sigma" tutoring effect is contested: VanLehn (2011, *Ed. Psychologist*
46(4)) finds a smaller effect. The strong deliberate-practice claim (Ericsson,
Krampe & Tesch-Römer 1993) is contested by Macnamara, Hambrick & Oswald (2014,
*Psych. Science* 25(8)). The program teaches these as graded-B debates rather
than building on them.

---

## 5. The project system

**Scale:** 157 graded projects, made up of 134 module projects and 23 studio
projects. Twenty of the module projects are Atlas milestones. In addition there
are 1–4 inline labs per lesson, and the capstone sequence.

| Layer | Size | Purpose |
|---|---|---|
| **Labs** | Minutes. 1–4 per lesson | Demonstrate one mechanism or numerically check one theorem |
| **Module project** | 10–40% of module hours | Prove mastery of the module, as rung 3 of the ladder |
| **Studio project** | 30–100 h, one per Part | Integrate a whole Part into a realistic professional deliverable: desk, deal, audit, report |
| **Atlas** | 20 milestones across the program | One production-grade research and trading platform, built cumulatively |
| **Capstone** | CAP1–CAP4 | Replication, debates, quals, thesis |

### 5.1 Atlas: the program-long build

Atlas is a single repository the student builds across the whole program. It
grows from a typed skeleton (A1, in CS1) to the following components:

- a point-in-time data layer
- a time-series toolkit, curve engine and pricing library
- a cross-sectional engine and a research-integrity module
- a backtester and execution models
- portfolio construction and a risk engine
- fundamentals and valuation engines
- an ML pipeline
- nowcasting, systemic-risk and macro trade-construction engines

Later milestones import earlier ones, so a weak early milestone costs the
student later. That is intentional: it is how real engineering works. By
graduation, Atlas plus the studio deliverables form a hiring-grade portfolio.

**Where Atlas lives.** Atlas is developed **locally, under git**. Real quant
engineering happens in repositories, not browser sandboxes, and CS4 teaches the
workflow. The course page supplies the spec, the starter code, and a test suite
the student can download. Small and early projects can also run in the
**in-browser workspace**: Pyodide with a virtual filesystem persisted to
IndexedDB, plus one-click zip export and import. Browser storage can be cleared
by the user or the browser, so the page tells students to export their work.

### 5.2 Grading modes

- **Autograder (dual-mode).** The same pytest suite runs in the browser
  (pytest in Pyodide) or locally (`pytest`).
  - Tests are **parameterized per student:** a seed derived from the student's
    workspace ID generates their instance, so answers cannot simply be copied.
  - Every autograder is **mutation-tested** before release. The verifier writes
    at least three plausible wrong solutions, and each one must fail.
  - A static site cannot keep its tests secret, and the program does not
    pretend otherwise. Integrity comes from parameterized instances and from
    the fact that the portfolio itself is the credential.
- **Rubric.** Criteria × four performance levels, with annotated exemplars at
  two or more levels. The student self-assesses, then compares their scoring
  with the exemplar scoring to calibrate.
- **Both.** Code is autograded; the memo or report is rubric-graded.

### 5.3 Data for projects

**Embedded data** comes only from sources that permit redistribution:

- public-domain FRED series
- the Kenneth French Data Library
- Shiller's data
- U.S. Treasury yields
- Federal Reserve datasets
- the Open Source Asset Pricing dataset
- SEC EDGAR / XBRL filings
- FFIEC call reports
- BIS statistics where the terms permit

**Bring-your-own-data mode.** Projects that need prices the program cannot
redistribute accept a student-supplied CSV that never leaves the browser. The
page documents the required schema and validates it.

**Simulated data** is always labelled **SIMULATED** on the figure.

---

## 6. Languages and tooling

| Language | Evidence for its role | Program role | Runs via |
|---|---|---|---|
| **Python 3** | The default research language in buy-side quant research and academic empirical finance. Core libraries are documented in peer-reviewed venues (NumPy: Harris et al. 2020, *Nature*; SciPy: Virtanen et al. 2020, *Nature Methods*; scikit-learn: Pedregosa et al. 2011, *JMLR*) | Primary language for every lab and most projects | Pyodide (in page) and local CPython |
| **C++20** | The language of pricing libraries (QuantLib) and low-latency systems | CS5, CS6, DV4, the CS studio | Emscripten → WASM at build time; native locally |
| **SQL** | Research data access; point-in-time and as-of joins | CS3, QR1, the data layer | DuckDB-WASM in page; DuckDB locally |
| **q / kdb+, R** | Tick-data analytics at banks and HFT firms (q); academic econometrics (R) | Reading literacy | Static, annotated code |
| **Rust, OCaml** | Trading infrastructure; Jane Street documents its OCaml use (Minsky 2011, *ACM Queue*) | Context only | — |

No usage percentages are claimed unless a verified survey is in the registry.

**Front end.** The site is static HTML5 with vanilla ES modules, so there is
no framework churn to maintain. Everything below is vendored, pinned and
SHA-256-locked in `vendor/LOCK.json`, so nothing loads from a CDN at runtime:

- KaTeX for math
- D3 v7 plus hand-authored inline SVG for figures
- Pyodide (with pytest), DuckDB-WASM, and Emscripten output for runnable code
- an FSRS-family scheduler for spaced retrieval
- IndexedDB for progress, cards and the workspace, with JSON and zip export
  and every access wrapped in try/catch

The site works fully offline from `python3 -m http.server`. A local server is
required because WASM runtimes do not load over `file://`. The site can also be
hosted as a static site with no backend.

**Build and verification toolchain:** Python 3.12+, pytest, Playwright with the
pre-installed Chromium, and a Crossref/DOI client.

---

## 7. Repository and site architecture

The repository separates authoring and tooling, at the root, from the deployable
static site in `course/`. ✅ marks what already exists; everything else is built
in the remaining Phase 0 steps.

```
quant-finance/
├── BLUEPRINT.md  BUILDER_RULES.md  VERIFIER_RULES.md       ✅ architecture and agent contracts
├── CURRICULUM.md                                           ✅ generated; never hand-edited
├── curriculum/
│   ├── meta.yaml  NN-*.yaml                                ✅ source of truth: tiers, credentials, tracks, Atlas, modules
│   └── curriculum.json                                     ✅ generated: DAG, topological order, computed stats
├── references/
│   ├── references.json                                     ✅ THE citation registry: Crossref-verified entries only
│   ├── review_queue.json  SEED_REPORT.md                   ✅ everything not yet verifiable, with the reason
│   ├── extra_sources.yaml  doi_hints.yaml                  ✅ blueprint-level citations; DOI hypotheses (still verified)
├── tools/
│   ├── render_curriculum.py                                ✅ validates the DAG, tiers, studios, credentials; renders
│   ├── seed_references.py  verify_refs.py  add_reference.py  refs/   ✅ registry pipeline
│   ├── fetch_data.py                                       # public data → assets/data + MANIFEST (licence, hash)
│   ├── run_labs.py  run_graders.py  mutate_graders.py
│   ├── check_pages.py  check_dag.py  check_projects.py
│   └── page_smoke.py                                       # Playwright: zero console errors, math, labs, graders
├── tests/                                                  ✅ tooling tests (each encodes a real failure mode)
├── notation/{notation,glossary}.json
├── ledgers/<ID>.verification.json                          # verifier output; merge gated on all-PASS
└── course/                                                 # the deployable static site
    ├── index.html                                          # program map: DAG, credentials, tracks, progress, search
    ├── placement/                                          # program-wide and per-module diagnostics
    ├── modules/<PART>/<ID>/{index,L01…Lnn,project}.html + grader/ + cards.json
    ├── studios/<STUDIO-ID>/  atlas/
    └── assets/{css,js,vendor,data,wasm}                    # vendor/ fetched per vendor/LOCK.json (SHA-256), not committed
```

**Design system.**

- Colour tokens on `:root`, with a dark-mode override.
- A serif for prose, a sans-serif for the interface and a monospace for code,
  all vendored.
- 72-character prose measure; theorem/definition/proof callouts; citation
  margin notes with hover popovers.
- A print stylesheet, so every lesson prints as a clean study PDF.
- WCAG 2.2 AA throughout.

**Images.** Every image teaches a mechanism or shows data. No stock photos, no
decoration. SVGs carry `<title>` and `<desc>`. Charts carry their source and
retrieval date.

---

## 8. Module template

Each module consists of a hub page, its lessons, and a project page.

- **Hub.** Lists objectives (4–8 measurable verbs), prerequisites, hours,
  placement test, lesson map and the project ladder.
- **Each lesson** contains, in order:
  1. Why it matters (at most 120 words)
  2. Core content in Definition, Theorem, Proof, Example and Remark blocks,
     every claim graded and cited
  3. Inline labs
  4. Where the canon breaks
  5. Debate brief, where the curriculum tags one
  6. Misconceptions
  7. A tiered problem set (Mechanics / Proof / Empirical / Research), each
     problem with a full worked solution
  8. A key-results table
  9. The retrieval quiz, which also generates spaced-retrieval cards
- **Project page.** Contains ladder rungs 1–4, the full spec, the grader or
  rubric, exemplars, and the reading list.

---

## 9. Build process

| Phase | Output | Gate |
|---|---|---|
| **0 — Foundations** | Design system; templates (hub, lesson, project, studio); all `tools/`; vendored runtimes with lock file; grader harness (Pyodide + local); spaced-retrieval engine; `references.json` seeded from every source in `curriculum/*.yaml` via `seed_references.py` (✅ done: see `references/SEED_REPORT.md`); `notation.json` | `render_curriculum.py` valid; `verify_refs.py` 100% resolved or removed; `page_smoke.py` green on every template |
| **1 — Pilot** | Three modules end to end, chosen to calibrate every style: **S7** (theory + autograder), **AP1** (proof-heavy), **AC2** (applied, rubric + Atlas milestone). Ten pilot learners | Full ledger PASS; hours recalibrated from pilot data; templates and rules revised once |
| **2 — Fan-out** | All remaining modules and studios in topological order (`curriculum.json` → `topological_order`), in batches of up to 8 modules. Each module gets one builder agent and one independent verifier agent | Ledger PASS + `check_dag.py` + `check_projects.py` (incl. mutation tests) + architect review |
| **3 — Integration** | Program map, placement system, Atlas cumulative test suites, capstone, quals bank, thesis rubric | Full-site Playwright run; zero broken links; zero unresolved keys |
| **4 — Freshness** | 2025–2026 literature pass on every debate and working paper | Ledgers re-run on touched modules |

**Agent topology.** A builder (`BUILDER_RULES.md`) writes the module, its
lessons, project and grader. A verifier (`VERIFIER_RULES.md`) is always a
separate agent with a fresh context. It produces the ledger and runs the
mutation tests. The architect reviews and merges. A failure goes back to the
builder with only the failing ledger rows.

---

## 10. Definition of done (whole program)

- [ ] `render_curriculum.py` valid; generated `CURRICULUM.md` committed
- [ ] All 134 module ledgers and 23 studio ledgers PASS, with zero failing or unverifiable rows
- [ ] Every autograder passes its reference solution and fails every mutant (`mutate_graders.py`)
- [ ] Every rubric ships exemplars at two or more levels
- [ ] `verify_refs.py`: 100% resolved; zero orphan or uncited keys
- [ ] `run_labs.py` and `run_graders.py` green both in-browser (Pyodide) and locally
- [ ] Atlas cumulative suites pass from A1 through A20 on the reference implementation
- [ ] `check_dag.py`: zero concepts used before they are introduced; zero concepts defined twice
- [ ] `page_smoke.py`: every page, light and dark mode, zero console errors, all math rendered, works offline
- [ ] Lighthouse accessibility ≥ 95 on every page
- [ ] Every embedded dataset has source, licence, retrieval date, hash and transform in `MANIFEST.json`
- [ ] Pilot-calibrated hours are reflected in the regenerated curriculum
