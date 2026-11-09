# S6 build plan: Causal Inference & Event Studies (planner output, 2026-11-09)

Unit: **S6 · Causal Inference & Event Studies** · tier M · 100 h · prerequisite S2 · no Atlas milestone · no debate key ·
grading `both` (autograder for the event-study engine, rubric for the research note) · output directory
`course/modules/S/S6/` (part code `S`) · lab twins `tests/labs/S6/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits. Executors: Haiku builders A to E, then
builder F for cards, then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every statement about the curriculum, a tool, a data source or the registry cites `file:line` read
during planning. Anything not found in the sources is marked **NOT IN CURRICULUM** or **NOT IN REGISTRY**. Planner-derived
graph facts were computed by calling `tools/coursekit.py` (`prerequisite_closure`, `concept_owner`, `curriculum`) through
the repository venv, and are marked "computed".

**Status: no hard blocker for the nine lessons or for the grader.** Three items need the architect before the affected
part is written: B1 (announcement dates, blocks the project's real-data path), B2 (asset-price scope) and B3 (MacKinlay
1997 has no record, blocks any citation of it). See §0.3 and §12.

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part S, code `S`, title "Statistics & Econometrics"; the part's modules are S0 to S7 | `curriculum/01-foundations.yaml:570-574` (code at 571); modules listed from 587 |
| S6 id, title "Causal Inference & Event Studies", tier `M`, hours `100` | `curriculum/01-foundations.yaml:799-802` |
| Prerequisites `[S2]` only | `curriculum/01-foundations.yaml:803` |
| Core: "Potential outcomes, IV and weak instruments, difference-in-differences (including staggered adoption), RDD, event studies, synthetic control." | `curriculum/01-foundations.yaml:804-806` |
| `introduces` has 10 concepts: potential-outcomes, instrumental-variables, weak-instruments, difference-in-differences, staggered-adoption-twfe-bias, regression-discontinuity, event-study, abnormal-return, placebo-test, synthetic-control | `curriculum/01-foundations.yaml:807-817` |
| Sources: four strings (Angrist & Pischke 2009; MacKinlay 1997, JEL 35(1); Abadie, Diamond & Hainmueller 2010, JASA 105(490); Goodman-Bacon 2021, J. Econometrics 225(2)) | `curriculum/01-foundations.yaml:818-822` |
| Lab: "Event study with correct abnormal-return variance." It names no dataset. | `curriculum/01-foundations.yaml:823` |
| Project "Policy-shock event study". Brief: "Measure asset-price reactions to a set of scheduled macro announcements using open data, with clustering-robust inference and placebo dates." Deliverable "Code plus a research note." Grading `both` | `curriculum/01-foundations.yaml:824-830` (brief 826-828, deliverable 829, grading 830) |
| No `atlas:` key on the S6 project; no `debate:` key on S6 | `curriculum/01-foundations.yaml:799-830` (absent) |
| JSON row mirrors the YAML (id, hours, prereqs, 10 concepts, four sources, lab, project) | `curriculum/curriculum.json:7112-7146` |
| S2 is the direct prerequisite; its prerequisites are [S1, M3] | `curriculum/01-foundations.yaml:661-665` (prereqs at 665) |
| S1 prerequisites [M4, S0]; S0 prerequisite [CS1] | `curriculum/01-foundations.yaml:619-623` (623); `:587-591` (591) |
| Direct dependents of S6: AC3 (`[AC2, S6]`), CF6 (`[CF3, S6]`), GM3 (`[E7, S6]`) | `curriculum/02-economics-finance-core.yaml:586-590` (AC3), `:831-835` (CF6); `curriculum/05-macro-alternatives.yaml:336-340` (GM3) |
| PhD in Finance credential requires S6; first-year group "Econometrics I–II" lists S1, S2, S3, S5, S6 | `curriculum/meta.yaml:123`, `:131` |
| Prerequisite closure of S6 = {CS1, M1, M2, M3, M4, P0.1, S0, S1, S2}; 124 usable concepts | computed: `prerequisite_closure("S6")`, `concept_owner()` |
| Topological position: S6 is 40; S2 is 28; M3 is 6; M4 is 12 | computed from `curriculum/curriculum.json` `topological_order` |
| Built units inside the closure: M1, M2, M3, M4 (`course/modules/M/`). CS1, S0, S1, S2 are not built. Under `course/modules/S/` only S7 exists | `ls course/modules/M course/modules/S course/modules/CS` |
| **Nearest built prerequisite: M3** (path S6 → S2 → M3, two steps; M4 needs three). Its plan is `plans/M3-build-plan.md`, read in full | this plan; `plans/M3-build-plan.md` |
| Embedded data: fx_daily, fx_monthly and ust_daily only; no calendar, no equity series | `course/assets/data/market/MANIFEST.json` (datasets array: fx_daily at line 5, ust_daily at line 63); `tools/data_sources.yaml:19-116` |
| Registry records for the three curriculum sources that have one: `abadie2010synthetic` (line 7), `angrist2009mostly` (line 853), `goodmanbacon2021difference` (line 10612); each has `used_by: ["S6"]` and status verified | `references/references.json` |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 100 h (`curriculum/01-foundations.yaml:802`). The tool rules:

- lesson `data-hours` 6 to 12 (`tools/check_pages.py:227-228`);
- hub `data-hours-lessons + data-hours-project = 100` (`tools/check_pages.py:337-338`);
- project share 10 to 40% of 100, i.e. 10 to 40 h (`tools/check_pages.py:339-340`);
- lessons sum to the hub's lessons figure (`tools/check_pages.py:341-342`).

Chosen split: **9 lessons totalling 70 h** (7, 9, 8, 8, 8, 8, 8, 7, 7) and **project 30 h (30%)**. 70 + 30 = 100. Feasible.
Precedent: the S7 hub declares `data-hours-lessons="70" data-hours-project="30"` (`course/modules/S/S7/index.html:33`) with
lessons of 7 to 11 h (`data-hours` on `course/modules/S/S7/L01.html`…`L08.html`, line 2 of each). **No STOP condition on hours.**

### 0.3 Blocking issues (architect decision before the named part is written)

**B1. The brief asks for scheduled macro announcements, and no announcement calendar is embedded.**
- The brief says "scheduled macro announcements" (`curriculum/01-foundations.yaml:827-828`). The embedded snapshots are
  `fx_daily`, `fx_monthly` and `ust_daily`, all from Board releases H.10 and H.15 (`tools/data_sources.yaml:19-116`). None
  is a calendar of announcement dates.
- The Board's general public-domain statement is quoted for those releases (`tools/data_sources.yaml:23-26`, `:95-98`). No
  calendar page has been read, quoted or registered, and the planner does not name one from memory (BUILDER_RULES §6.6, steps
  1 and 2).
- **Default (recommended):** the project takes its announcement dates as a student-supplied CSV in bring-your-own-data mode
  (schema on the page; the file never leaves the browser, BUILDER_RULES §6.6). A DATA_REQUEST D1 (§7.3) asks the architect
  to read the Board's own calendar page and quote its licence before any embedding.
- Not blocking: the lessons, the labs and the autograder use SIMULATED data. Blocking: the project's real-data path.

**B2. The brief says "asset-price reactions", and the only cleared asset prices are FX rates and Treasury yields.**
- Cleared and embedded: six daily FX rates in USD per unit of foreign currency (`fx_daily`; `tools/data_sources.yaml:19-51`,
  with CAD, CHF and JPY inverted in the transform at line 51) and the 10-year constant-maturity yield `cmt_10y`, in percent per
  year (`tools/data_sources.yaml:91-116`, note at `:100-103`).
- Not embedded: equity prices and an equity market index. The two equity candidates checked in `tools/data_sources.yaml:118-139`
  grant no redistribution. No equity return series is cleared.
- **Default (recommended):** the project measures reactions in `cmt_10y` yield changes (percentage points) and in FX log
  returns. Equity reactions are a rung-4 stretch in bring-your-own-data mode. The curriculum text is not changed.
  The architect confirms.

**B3. MacKinlay (1997), JEL 35(1), has no registry record, and the review queue holds only wrong candidates.**
- Curriculum string: `curriculum/01-foundations.yaml:820`. Seed report entry: `references/SEED_REPORT.md:30` ("used by S6").
- Review queue: `references/review_queue.json:55-107`. Its three candidates are not the requested article:
  - `10.1016/0304-405x(94)00808-e`: a 1995 Journal of Financial Economics article, "Multifactor models do not explain
    deviations from the CAPM", with the same first author (`review_queue.json:65-76`);
  - `10.1017/s1326011100002799`: a book review in an Australian education journal (`:79-91`);
  - `10.1080/13533319708413690`: an unrelated 1997 article on complex emergencies (`:92-105`).
- **These three must not be admitted.** The architect admits the real article through the manual path of
  `tools/add_reference.py` (publisher's stable URL, BUILDER_RULES §2.4).
- Blocking any citation of MacKinlay. Not blocking the build: builders cite only admitted keys (§7).

**Non-blocking, the architect should see them:**
- **N1.** The registry has records for only three of the four curriculum sources (see §0.1). The canon for IV, weak
  instruments, RDD, staggered-adoption alternatives and event-study power has no record (§7.2). Claims about them are
  derivations, or they are ungraded.
- **N2.** Four closure modules (S0, S1, S2, CS1) are not built. Links go to `../../../concepts.html#<id>` only, as in the E5
  precedent (`plans/E5-build-plan.md` §11 item 6). The hub links no S0 to S2 page.
- **N3.** No Atlas milestone (`curriculum/01-foundations.yaml:824-830`). `atlas/` is not needed.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

9 lessons, total 70 h; project 30 h; total 100 h. Concept counts per row sum to 1+2+1+1+1+1+1+1+1 = 10, each concept in
exactly one row (`curriculum/01-foundations.yaml:807-817`).

| Lesson | Title (working) | Concepts it defines (`<dfn>` with `data-concept`) | Lab twins (`tests/labs/S6/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Potential outcomes and the selection problem | `potential-outcomes` | `lab-S6-L01-1`: a SIMULATED population with a known effect; naive difference against the average effect, in a randomised and an observational sample (seeded) | 7 | Builder A |
| L02 | Instrumental variables and weak instruments | `instrumental-variables`, `weak-instruments` | `lab-S6-L02-1`: the Wald ratio equals the covariance ratio on a seeded sample (identity checked to 1e-12); `lab-S6-L02-2`: two-stage least squares bias against first-stage strength, SIMULATED Monte Carlo | 9 | Builder A |
| L03 | Difference-in-differences | `difference-in-differences` | `lab-S6-L03-1`: a constructed 2 × 2 × 2 panel in `fractions.Fraction`; the difference-in-differences equals the two-way fixed-effects coefficient exactly | 8 | Builder A |
| L04 | Staggered adoption and the two-way fixed-effects bias | `staggered-adoption-twfe-bias` | `lab-S6-L04-1`: a constructed three-cohort panel; the two-way fixed-effects coefficient equals a weighted sum of 2 × 2 comparisons, one weight negative (exact) | 8 | Builder B |
| L05 | Regression discontinuity | `regression-discontinuity` | `lab-S6-L05-1`: a local linear fit on a SIMULATED running variable with a known jump; bandwidth sensitivity table (seeded) | 8 | Builder B |
| L06 | Abnormal returns and their variance | `abnormal-return` | `lab-S6-L06-1`: Monte Carlo check of the abnormal-return variance formula on SIMULATED returns | 8 | Builder C |
| L07 | Event studies | `event-study` | `lab-S6-L07-1` (**the curriculum lab**, `curriculum/01-foundations.yaml:823`): event study with the correct abnormal-return variance against the naive variance, SIMULATED panel, rejection rates under the null | 8 | Builder C |
| L08 | Placebo tests and multiple placebo dates | `placebo-test` | `lab-S6-L08-1`: placebo rejection rate under the null on SIMULATED data against 1 − (1 − α)^m | 7 | Builder D |
| L09 | Synthetic control | `synthetic-control` | `lab-S6-L09-1`: two-donor synthetic control weights by an exact grid over [0, 1]; pre-period fit; constructed or SIMULATED donors | 7 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 70 / 30 | none | none | - | Builder A |
| project | Policy-shock event study (`both`, §5) | none | `lab-S6-project-1` (rung 1), `lab-S6-project-2` (rung 2, `class="lab completion"`), `lab-S6-project-3` (rung-3 check) | 30 | Builder E |
| grader | `grader/instance.py`, `reference.py`, `test_project.py`, `starter.py` | none | none | - | Builder E |
| cards | `cards.json` from L01 to L09 | none | none | - | Builder F (after A to D) |

Ownership rule: each builder writes only its own lesson pages and twins. Builder A writes the hub after L01 to L03 exist.
Builder E writes `project.html`, the grader and the project labs, and does not depend on the lessons' prose; it uses only the
concepts of §1 and the spec of §5.2. Builder counts: A has three lessons, B, C and D have two each (the plan's "about three per
builder"; the M3 precedent is `plans/M3-build-plan.md` §2.2).

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses, §4):
- L01 uses P0.1 `identification` (closure, `curriculum/curriculum.json` concepts) and M4 `expectation`, `independence`, `random-variable`.
- L02 uses L01 `potential-outcomes`; S2 `errors-in-variables`; M3 `least-squares-projection`; S1 `consistent-estimator`.
- L03 uses L01; S1 `hypothesis-test`, `confidence-interval`.
- L04 uses L03 `difference-in-differences`; S2 `frisch-waugh-lovell-theorem`, `clustered-standard-errors`.
- L05 uses L01; M4 `conditional-expectation-elementary`; M2 `limit`.
- L06 uses M4 `variance`, `normal-distribution`; S2 `ols-estimator`; S1 `estimator-bias-variance`.
- L07 uses L06 `abnormal-return`; S1 `t-statistic`; S2 `clustered-standard-errors`.
- L08 uses L07 `event-study` and L01 `potential-outcomes`; S1 `type-i-error`, `statistical-power`.
- L09 uses L01, L08 `placebo-test`; S1 `hypothesis-test`; P0.1 `robustness-check`.
- Note: L08 must not mention placebo tests before L08 (the concept is first introduced there, BUILDER_RULES §1.10).

Hours check: 7 + 9 + 8 + 8 + 8 + 8 + 8 + 7 + 7 = 70 (hub `data-hours-lessons="70"`); project 30 (hub `data-hours-project="30"`); total 100.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to S6)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3 to §8, `VERIFIER_RULES.md` §2, `plans/M3-build-plan.md` (the
nearest built prerequisite's plan), `plans/E5-build-plan.md` (its standing defaults at the end are binding, §12), this file.
Study `course/modules/S/S7/` for layout, the hub and project grammar, and the grader panel (`course/modules/S/S7/project.html:188`).
`course/templates/` holds the four skeletons. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) or from
   unrounded floats, and rounded only at display. A rounded figure states its rounding rule. Precedent: AC4 KNOWN LIMITATION 3
   and CF1 L01 Remark 5.2. For S6 this covers every abnormal return, variance, t-statistic, weight, bias and rejection rate.
   The yield unit conversion is stated: 1 percentage point = 100 basis points (an identity, not an estimate).
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only
   what the printed numbers show. A Monte Carlo rejection rate is quoted with its replication count and seed. Precedent: M1
   LESSON_TEXT_DEFECTS ("checked directly" with no lab behind it).
3. **Attribute nothing unread.** Only the registry keys in §7 may be cited. A paper-level attribution requires the builder to
   have read the abstract (VERIFIER §2.1). A locator (table, theorem, equation, page) requires that the locator was read. No
   page, equation, coefficient, rule of thumb or date is typed from memory. Precedent: AC2 and AC4 ("never type a page or a
   table from memory"). A textbook result is either a derivation on the page (grade T) or cited at book level with no locator.
4. **Scope words need a computation, a witness or an explicit hypothesis** (fixer rules, scope-words bullet): "every", "all", "always",
   "any", "only", "same", "exactly", "robust", "valid", "unbiased", "consistent", "identifies". A lab with 500 seeded replications
   supports the sentence "in the 500 seeded replications of Lab 2" and no broader sentence.
5. **Define before use.** Each of the 10 concepts is defined once with `<dfn id="def-<id>" data-concept="<id>">` in its assigned
   lesson, never before it. Terms outside the 10 (treatment effect, control group, parallel trends, event window, estimation
   window, abnormal-return model, placebo date, bandwidth, first stage, exclusion restriction, cluster) are defined in prose at
   first use with a plain `<dfn>` and no `data-concept` (`tools/check_dag.py:40-47` skips a `<dfn>` without `data-concept`).
   Outside-closure concept names (§4) are never defined here.
6. **Assumptions explicit.** Every Theorem, Proposition and Derivation block lists its numbered Assumptions (A1, A2, …) before the
   statement. Examples the builders must state: the Wald ratio needs an exclusion assumption, a non-zero first-stage covariance
   and independence of the instrument from the potential outcomes; the difference-in-differences needs a parallel-trends
   assumption A-number and no anticipation; the abnormal-return variance needs homoskedastic independent errors independent of the
   market return (the derivation uses only the listed assumptions); the sharp RDD needs continuity of the conditional
   expectation at the cutoff; the placebo false-rejection formula needs independent tests.
7. **Grader rule.** Applies to the autograder (§5.5). A test asserts an exception type only for a condition the spec names
   (fixer rules, PROJECT GRADERS bullet; `plans/M3-build-plan.md` §1.1 item 7). Every named condition has its own isolated test in both directions.
8. **Money.** S6 has no money quantity. Yields are in percent per year; changes in percentage points; reactions in basis points
   for display only.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own box;
   no element forces the page wider than 360 px (fixer rules, no-horizontal-scroll part of the money bullet; `page_smoke.py` is the verifier's check).
10. **Labs call `main()` at top level** and have no `if __name__ == "__main__":` guard. `run_labs.py` runs each twin as
    `python -I -W error <twin>` with no network (`tools/run_labs.py`, lines 51-60, as cited by E5 §2.1). The M1 twin
    `tests/labs/M1/lab-M1-L04-1.py` is the model.
11. **Yield and FX conventions are basis-explicit.** A yield is stated in percent per year, and a yield change in percentage
    points. An FX rate is stated as USD per unit of foreign currency after the transform (`tools/data_sources.yaml:20`, `:51`).
    The builder reads the MANIFEST transform before using a series and does not invert again.
12. **Event time is explicit.** Event day is day 0; the event window is the trading days `[a, b]` with `a ≤ 0 ≤ b`; the estimation
    window is the `L` trading days that end before the event window begins, and the gap is stated.

### 2.2 Standing rules (BUILDER_RULES, unchanged unless stated)

- **Evidence.** Every claim carries a grade (T, A, B, C, D or X; BLUEPRINT §3) and a registry key or a derivation. A grade-B or
  grade-C claim names its published counter-evidence (BUILDER_RULES §2.5). **No registry record for S6 carries a counter-evidence
  claim yet** (§7.2). A claim with no key therefore stays a derivation (T, on the page) or is an ungraded naming sentence.
- **Concepts.** §1 table only, with `<dfn>` for the 10 registered concepts. Links: `href="../../../concepts.html#<id>"` for closure
  concepts (S1, S2, M1 to M4, P0.1, CS1); `href="Lnn.html#def-<id>"` for earlier S6 lessons. A lesson never links a concept
  defined in a later lesson. No link to an S0, S1 or S2 hub page, because those pages are not built (§0.3 N2).
- **Labs.** Code lives once, in `tests/labs/S6/lab-S6-Lnn-k.py` (and `lab-S6-project-1..3.py`). The page carries
  `@@LAB:<file>@@` and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type an expected output. Lab ids match
  `lab-S6-<page>-<n>` (`tools/check_pages.py:258-259`). Labs use the Python standard library only (`fractions`, `math`,
  `random.Random(seed)`); numpy is for the grader's alternatives only (§5.5). Seeded RNG only; no network; under 10 s in Pyodide;
  no warnings (`-W error`).
- **SIMULATED label.** Every lab or figure that uses generated data carries a visible **SIMULATED** label: L02 lab 2, L05, L06,
  L07, L08, L09 when donors are generated, and the project's worked example and grader instances. A hand-written constructed panel
  (L03, L04, L02 lab 1) is labelled "constructed example" and is not called SIMULATED.
- **Never hand-edit generated files** (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- **Learner-visible text:** no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references
  in code comments (E5 §2.2; M1 "Convention (project Q5)").
- **Banned strings** (`tools/check_pages.py:58-72`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the scope", "left
  as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known", "obviously",
  "clearly", and any ellipsis `...` outside code.
- **Percent changes** state the base and the direction (CF1 L07 Misconception 2). Growth or return conventions (simple or log,
  per period or annualised) are stated.
- **A finite enumeration** (for example the placebo dates of one draw) is grade C with its basis named, not grade T (M1 L06).
- **Every "checked" or "verified" claim** names the lab, the line or the test that did the check.
- **Hub lesson titles** match each lesson's `<h1>` at integration (CF1 KNOWN 3).
- **Quiz explanations** are read against their lesson (CF1 KNOWN 6).
- **No `git commit`, no push.** Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10
  output contract.
- **No figures.** No `figures-Lnn.js` or `figures-index.js` (architect standing default, §12 Q14). No new JS kernel.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols and macros that S6 must not give another meaning (`notation/notation.json`, `symbols` and `macros`):

| Registered item | Registered meaning (locator) | S6 rule |
|---|---|---|
| `T` (symbol) | number of return observations in a sample, module S1 (`notation/notation.json:111-115`) | **Never used** for a time horizon, a sample size or an event count. Use `L` (estimation length), `K` (number of events), `N` (number of firms), `G` (number of clusters), `m` (number of placebo dates). |
| `\Phi`, `\Phi^{-1}` (symbol) | standard normal CDF and quantile, module M4 (`:116-120`) | **Not used.** Write the normal distribution as `\Normal(0,1)` and probabilities with `\Prob`. |
| `\gamma_3`, `\gamma_4` (symbols) | skewness and kurtosis, M4 (`:121-130`) | Not used. |
| `R^\ast`, `R^{e\ast}`, `R_f`, `\mathbb{Q}` (symbols) | AP1 items (`:131-150`) | **Not used.** The market return is `R_{m,t}` (subscripted, lowercase `r` for stock returns). The risk-free rate is not used. |
| `\E`, `\Var`, `\Cov`, `\Corr`, `\Prob`, `\indic`, `\se`, `\R`, `\Normal`, `\iid`, `\dto`, `\pto`, `\argmin`, `\argmax` (macros) | registered (`:5-60`, `:101-104`) | Use as registered. `\indic` for indicator functions (for example the treatment indicator). |
| `\FWER`, `\FDR`, `\FDP` (macros) | registered (`:89-100`), owned by S7 concepts | **Not used on S6 pages.** The notation registry allows them, but the concept is outside the closure (§4 D6); write the calculation in plain symbols. Architect may override (§12 Q10). |
| `\SR`, `\hSR`, `\PSR`, `\DSR`, `\PBO`, `\emgamma` (macros) | registered, S1 and S7 items (`:69-108`) | Not used. |

Local symbols (allowed; each defined on the lesson where it first appears and never redefined): `\alpha`, `\beta` (market-model
coefficients), `\sigma^2` (residual variance), `\tau` (event time), `[a, b]` (event window), `L` (estimation length), `K`
(events), `N` (firms), `G` (clusters), `m` (placebo dates), `D_{it}` or `D` (treatment indicator), `Y` (outcome), `Z` (instrument),
`X` (running variable), `c` (RDD cutoff), `h` (bandwidth), `w` (synthetic-control weights), `r_{it}` (stock return), `R_{m,t}`
(market return). `\pi` is avoided for anything other than the number 3.14…

NOTATION_REQUESTS: none. S6 uses registered macros and local symbols only.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2): why it matters (at most 120 words); core content
(Definition, Theorem, Proof, Example, Remark blocks); inline lab; where the canon breaks; misconceptions (at least 3); problem set
(at least 3 each in Mechanics, Proof, Empirical, Research, each with a worked solution in `<details class="solution">`);
key-results table; retrieval quiz (8 to 15 items). The lesson's hours are its design target (§0.2).

- **L01 `potential-outcomes`** (7 h). The potential-outcomes notation `Y_i(1)`, `Y_i(0)` (plain prose definitions); observed
  outcome `Y_i = D_i Y_i(1) + (1 − D_i) Y_i(0)`; the individual effect and the average effect as expectations (`\E`). The
  decomposition of the naive difference in means into the average effect on the treated plus selection bias (T, derivation with
  an explicit identity). Randomisation and the independence assumption; the identification statement from P0.1 (`identification`,
  linked). Grade of any empirical claim: none in this lesson beyond the lab. Registry: `angrist2009mostly` at book level only,
  if at all. Canon breaks: no interference between units (state as assumption A1, not as a fact); a measure that differs
  from the causal quantity. Lab `lab-S6-L01-1`: SIMULATED, seeded; prints naive difference, average effect and bias in both samples.

- **L02 `instrumental-variables`, `weak-instruments`** (9 h). The IV model with an endogenous regressor; the instrument's
  relevance (non-zero covariance with `D`) and exclusion (no direct path to `Y`); the Wald ratio `Cov(Y,Z)/Cov(D,Z)` (T,
  derivation from the model, with assumptions listed). Two-stage least squares as the projection of `D` on `Z` (M3
  `least-squares-projection`, linked; T). Errors-in-variables as a motivating example (S2 `errors-in-variables`, linked; no
  statistic). Weak instruments: small first-stage strength makes the 2SLS distribution far from normal, and 2SLS is biased toward OLS
  (the Monte Carlo shows the pattern; the lesson states no threshold value). A numerical rule of thumb for the first-stage
  F-statistic is not typed (no registry record, §7.2). Canon breaks: exclusion can fail; a weak instrument makes inference
  unreliable. Lab 1 `lab-S6-L02-1`: the Wald ratio equals the covariance ratio on a seeded sample, identity to 1e-12 (constructed
  check, not SIMULATED data beyond the seed). Lab 2 `lab-S6-L02-2`: 2SLS against OLS for three first-stage strengths, SIMULATED,
  fixed replication count and seed, ≤ 10 s in Pyodide.

- **L03 `difference-in-differences`** (8 h). The 2 × 2 design with a treated and a control group, before and after; the
  difference-in-differences estimand as a difference of two differences of expectations (T, derivation). Parallel-trends
  assumption (numbered A-assumption; a statement about counterfactual trends, not a testable claim here); no anticipation.
  The two-way fixed-effects regression with unit and period indicators (OLS, S2 `ols-estimator`, linked) equals the
  difference-in-differences exactly in the 2 × 2 design (T, derivation; S2 `frisch-waugh-lovell-theorem` may be used, linked).
  Clustering at the unit level (S2 `clustered-standard-errors`, linked) as a statement of method. Canon breaks: parallel trends
  can fail; the 2 × 2 case hides timing problems that L04 exposes. Lab `lab-S6-L03-1`: constructed 2 × 2 × 2 panel in
  `fractions.Fraction`; the estimate equals the coefficient exactly. Labelled "constructed example".

- **L04 `staggered-adoption-twfe-bias`** (8 h). Units adopt a treatment at different dates. The two-way fixed-effects coefficient
  is a weighted average of 2 × 2 comparisons. The lesson proves the three-cohort case on the page (T) and shows one weight is
  negative on a constructed panel (lab `lab-S6-L04-1`, exact arithmetic). Attribution of the general decomposition to the
  registered Goodman-Bacon paper (`goodmanbacon2021difference`, paper level): the builder reads the abstract before citing it;
  the general statement is grade C with its basis named until the decomposition's locator is read (VERIFIER §2.1; ruling 13).
  Alternative estimators (Callaway & Sant'Anna; Sun & Abraham; de Chaisemartin & D'Haultfœuille) are **not** in the registry:
  they go to REFERENCE_REQUESTS (§7.2); the lesson may name the problem but not the estimators. Canon breaks: heterogeneous
  effects over time; the negative weights depend on the treatment-timing pattern.

- **L05 `regression-discontinuity`** (8 h). The sharp design: treatment is `\indic\{X \ge c\}`. The estimand is the jump of the
  conditional expectation at the cutoff, a one-sided limit (M2 `limit`, linked; T as a definition of the estimand under the
  continuity assumption, numbered). Local linear estimation within a bandwidth `h` (plain prose; no concept). Lab
  `lab-S6-L05-1`: SIMULATED running variable with a known jump; the local linear estimate against the true jump; a table of
  estimates across bandwidths, with the bandwidth stated in every row. Canon breaks: manipulation of the running variable; the
  estimate depends on `h`. No empirical claim about the validity of RDD designs is made without a registry key (§7.2).

- **L06 `abnormal-return`** (8 h). The market model `r_{i,t} = \alpha_i + \beta_i R_{m,t} + \varepsilon_{i,t}` with OLS on the
  estimation window (`ols-estimator`, linked). The abnormal return `AR_{i,t} = r_{i,t} − (\hat\alpha_i + \hat\beta_i R_{m,t})`. The
  variance of an abnormal return, derived on the page (T, under the listed assumptions):
  `\Var(AR_{i,t}) = \sigma^2 (1 + 1/L + (R_{m,t} − \bar R_m)^2 / \sum_{\tau \in est} (R_{m,\tau} − \bar R_m)^2)`,
  with `\sigma^2` estimated by the residual sum of squares over `L − 2` degrees of freedom. The constant-mean model is the case
  without a market term: `\Var = \sigma^2 (1 + 1/L)` with divisor `L − 1`. The lesson states that the normal-return model is an
  assumption; CAPM is not derived (§4 D3). Lab `lab-S6-L06-1`: Monte Carlo check of the variance formula on SIMULATED returns,
  printed as the ratio of the sample variance of ARs to the formula. Canon breaks: a misspecified normal-return model; the
  estimation error term is ignored by the naive `\sigma^2`.

- **L07 `event-study`** (8 h). The event study as the average or cumulative abnormal return over a window, across firms; the
  cross-sectional t-statistic `\bar{CAR}/(s/\sqrt{K})` with `s` the sample standard deviation (ddof 1); the clustered t-statistic
  when several events share a date (S2 `clustered-standard-errors`, linked). The variance of a CAR as the sum of the daily
  variances, which assumes no cross-day covariance (stated as an assumption). **Curriculum lab** `lab-S6-L07-1`: SIMULATED panel
  of firms with a planted announcement effect; the rejection rate under the null for the correct AR variance and for the naive
  `\sigma^2` variance, with replication count and seed printed. Canon breaks: event-clustering; common shocks; a result is only
  as good as the normal-return model (the lesson cites no literature result; the event-study power claims need REFERENCE_REQUESTS
  §7.2 and are not made).

- **L08 `placebo-test`** (7 h). A placebo test assigns the event to dates where no event occurred and computes the same statistic.
  The rejection rate under the null is the nominal level when the placebo statistics are valid (T, derivation under the stated
  assumptions). With `m` independent tests at level `\alpha`, the probability of at least one false rejection is
  `1 − (1 − \alpha)^m` (T, derivation under independence; the dependent case is not stated). Placebo dates must avoid the event
  window of every true event (the exclusion rule is in the spec, §5.2). Lab `lab-S6-L08-1`: SIMULATED null data; the rejection
  rate across placebo dates against `1 − (1 − \alpha)^m`. Canon breaks: placebo dates that carry other news; dependence across
  dates. Concepts from S7 (multiple-testing family, data snooping) are not named (§4 D6).

- **L09 `synthetic-control`** (7 h). A treated unit is compared with a weighted average of donor units. The weights are
  nonnegative and sum to one (plain prose: the constraint set is the simplex, not a concept), chosen to fit the treated
  unit's pre-period outcomes. The estimand is the post-period gap. Inference by placebo-in-space: apply the same procedure to each
  donor (`placebo-test`, linked, L08). The method is attributed to `abadie2010synthetic` at paper level; the builder reads the
  abstract first. Lab `lab-S6-L09-1`: two-donor case, weights by an exact grid over [0, 1]; the pre-period fit; the post-period gap
  for the chosen weight. Canon breaks: a poor pre-period fit; few donors; the donor pool chosen after seeing outcomes.

---

## 4. DAG problems (concepts that natural S6 content would use outside the closure)

Prerequisite closure of S6 (computed, §0.1): **{CS1, M1, M2, M3, M4, P0.1, S0, S1, S2}**, with 124 usable concepts. Owners below
are from `curriculum/curriculum.json` `concepts` (computed with `concept_owner()`). Names with no registered concept at all are
listed in D12.

| Ref | Concept (owner, outside closure) | Where natural S6 content would use it | Resolution in this plan |
|---|---|---|---|
| D1 | `panel-fixed-effects` (S5) | the two-way fixed-effects estimator (L03, L04, L05 prose) | **Plain prose, no link, no dfn.** The estimator is written as OLS with unit and period indicators (closure: `ols-estimator`, `frisch-waugh-lovell-theorem`). Architect may add S5 as prerequisite (a curriculum change; S5 needs S2 and S3; §12 Q6). |
| D2 | `generalized-method-of-moments`, `efficient-gmm-weighting`, `hansen-j-test` (S5) | IV by GMM and overidentification tests (L02) | **Not used.** IV is the Wald ratio and the projection (closure). |
| D3 | `capm`, `beta`, `jensens-alpha`, `security-market-line`, `equity-risk-premium`, `linear-factor-model` (AP2) | the normal-return model (L06, L07, project) | **Plain prose.** The market model is defined as an OLS regression in L06 (closure). CAPM is named once in L06 as "not derived here" (plain prose, no link). No `jensens-alpha` term. |
| D4 | `fama-french-three-factor-model`, `carhart-four-factor-model`, `fama-french-five-factor-model`, `q-factor-model` (F2) | multi-factor normal returns | **Not used.** |
| D5 | `efficient-markets-hypothesis`, `joint-hypothesis-problem` (FC3) | the interpretation of an abnormal return (L07) | **Plain prose**, no link. The joint-hypothesis point is made in prose ("an abnormal return tests the model and the market jointly") with no concept name. |
| D6 | `bonferroni-correction`, `family-wise-error-rate`, `benjamini-hochberg`, `false-discovery-rate`, `data-snooping-bias`, `p-hacking` (S7) | multiple placebo dates (L08) and the project | **Plain prose and a derivation.** L08 derives `1 − (1 − \alpha)^m` under independence without naming S7 concepts. `\FWER` and `\FDR` macros not used (§2.3). |
| D7 | `stationary-bootstrap` (S7), `moving-block-bootstrap` (BK5) | dependence across days (L07) | **Not used.** The closure's `bootstrap` (S1) is named only if a lab uses it; default: not used. |
| D8 | `monte-carlo-integration`, `pseudo-random-number-generator` (M8) | the Monte Carlo labs (L02 lab 2, L06, L07, L08) | **Plain prose**: "seeded simulation with `random.Random(seed)`". No link. |
| D9 | `convex-set`, `convex-function`, `quadratic-programming`, `mean-variance-optimization` (M7) | the simplex of synthetic-control weights (L09) | **Plain prose.** The constraint is written as explicit inequalities and an equality (nonnegative, sum to one). |
| D10 | `policy-rate` (E5), `fomc-event-study`, `pre-fomc-drift` (GM3), `macro-data-revision` (GM1), `look-ahead-bias` (QR1), `survivorship-bias` (F1) | announcement dates, timing, data hygiene (project and L07) | **Plain prose**, no link. S6 must not define `fomc-event-study`: GM3 requires S6 and owns that concept (`curriculum/05-macro-alternatives.yaml:336-340`). |
| D11 | `local-projections` (E7), `purchasing-power-parity` (X1), `merger-announcement-returns` (CF5) | none planned | **Not used.** |
| D12 | Names with **no registered concept**: market model, parallel trends, average treatment effect, local average treatment effect, exclusion restriction, first stage, permutation test, randomisation inference, event window, estimation window, selection bias, unconfoundedness, bandwidth, donor pool, cumulative abnormal return | used in S6 prose (§3) | **Plain prose with a plain `<dfn>` at first use, no `data-concept`** (BUILDER_RULES §1.10 applies to registered concepts only; `tools/check_dag.py:47` skips unregistered `<dfn>`). No DAG_DEFECT is raised. Architect may register any of them (curriculum change; §12 Q7). |

No DAG_DEFECT blocks the build: every row has a resolution. **Each row needs the architect's confirmation (§12 Q6 to Q10).**
`check_dag.py` checks linked uses only (`tools/check_dag.py` docstring). An unlinked use of D1 to D11 passes the tool, so the
verifier reads every lesson for these names (VERIFIER §2.9).

---

## 5. Project (`project.html`, Builder E): `both` grading, ladder, spec, rubric, autograder

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py:33` requires the rung order)

Tier M: rungs 1 and 2 are kept to the minimum (BLUEPRINT §4, lines 222-223; BUILDER_RULES §5.1, line 188).

1. **Rung 1, worked example** (`lab-S6-project-1`, SIMULATED): one fully solved and annotated run of the reference on one generated
   instance (a seeded panel of five firms, an event window of [-1, 1], a 60-day estimation window). Each step carries a "why"
   note: the estimation window, the market-model fit, the abnormal returns, the variance term, the CAR and the t-statistic.
   Standard library only.
2. **Rung 2, completion** (`section.lab.completion`, `lab-S6-project-2`): the same run with two blanks, `___`, in the variance
   term and in the CAR sum. Graded instantly. The twin is the completed solution; every page line equals the twin's line or
   contains a blank (`tools/run_labs.py` docstring, as in E5 §5.1).
3. **Rung 3, independent project** (graded by autograder and rubric; §5.2 to §5.5). (a) The autograded engine `event_study.py`
   (eight functions, §5.2); (b) the research note `note/research_note.md`, rubric-graded (§5.4). `lab-S6-project-3` is the rung-3
   check: it prints the default instance's output table, which the student's engine must reproduce.
4. **Rung 4, stretch** (optional, not graded): a second event with the constant-mean model on the embedded `cmt_10y` and
   `fx_daily` series, using the student's own dates CSV (B1), or an equity-reaction variant in bring-your-own-data mode (B2).

### 5.2 Spec (`dl.spec`; `tools/check_projects.py:92-100` requires the terms context, inputs, required outputs, constraints, grading)

- **Context.** A macro desk asks whether scheduled macro announcements moved asset prices. The desk accepts a number only with a
  timing rule, a normal-return model, the variance of each reaction and a clustered test. Your engine computes the reactions; your
  note reports them.
- **Inputs.** (1) The autograder instance (SIMULATED), generated by `grader/instance.py` from the workspace seed. (2) Real data
  for the note, optional but scored: the `ust_daily` snapshot (MANIFEST id `ust_daily`, the `cmt_10y` column, percent per year)
  and the `fx_daily` snapshot (MANIFEST id `fx_daily`, USD per unit of foreign currency), both with the Board's public-domain
  licence as quoted in `tools/data_sources.yaml:23-26` and `:95-98`, with download links. (3) Announcement dates as a student-supplied
  CSV, columns `date` (YYYY-MM-DD, a trading day of the series) and `label`, in bring-your-own-data mode; the file never leaves the
  browser (BUILDER_RULES §6.6). Validation of the dates file is done by the student's run script (§12 Q9), not in the page.
  No equity series is embedded (B2).
- **Required outputs.** `event_study.py` implementing exactly the interface in §5.2 below (start from `grader/starter.py`);
  `note/research_note.md` (2 to 4 pages, every number quoted by the run script); `analysis/run_note.py`, which reads the dates CSV and
  the snapshots, calls `event_study.py` and prints every number the note quotes; `note/self_assessment.md`, produced by the form in
  the page after the exemplar scoring is revealed.
- **Frozen interface** (proposal; the architect freezes it, §12 Q19). All functions are pure: they validate inputs, raise
  `ValueError` naming the violated condition, and never print or change their arguments.

```
fit_normal_model(stock: Sequence[float], market: Sequence[float] | None = None) -> tuple[float, float, float]
    # returns (alpha, beta, sigma2). market None: constant-mean model, beta = 0, sigma2 divided by L - 1.
    # market given: market model by OLS, sigma2 divided by L - 2.
abnormal_returns(stock: Sequence[float], market: Sequence[float] | None, alpha: float, beta: float) -> list[float]
abnormal_return_variance(sigma2: float, estimation_market: Sequence[float] | None, event_market: float | None) -> float
    # market model: sigma2 * (1 + 1/L + (event_market - mean)^2 / SS); constant mean: sigma2 * (1 + 1/L).
car(abnormal: Sequence[float]) -> float                     # the sum of the abnormal returns over the window
event_t_statistic(cars: Sequence[float]) -> float           # mean / (s / sqrt(K)), s with ddof 1
clustered_t_statistic(values: Sequence[float], clusters: Sequence[str]) -> float
    # CR1 for an intercept-only model: t = mean / sqrt(V), V = G/(G-1) * sum_g (sum_{i in g} (x_i - mean))^2 / N^2
placebo_dates(calendar_length: int, event_days: Sequence[int], half_window: int, count: int, seed: int) -> list[int]
    # count distinct day indices, none within half_window of any event day; reproducible for a given seed
event_window_car(stock: Sequence[float], market: Sequence[float] | None, event_day: int, est_len: int,
                 window: tuple[int, int]) -> tuple[float, float]
    # (CAR, variance) for one firm: estimation window = est_len days ending before the event window starts;
    # parameters use only the estimation window; CAR is the sum of ARs over the window; variance is the sum of AR variances.
```

- **Named conditions (the only ones a test may assert as `ValueError`).**
  - `fit_normal_model`: unequal lengths of stock and market; fewer than 3 observations in the market model; fewer than 2 in the constant-mean model; a market series with zero sample variance in the market model.
  - `abnormal_returns`: unequal lengths.
  - `abnormal_return_variance`: the estimation market series has zero sample variance when `event_market` is given.
  - `car`: an empty sequence.
  - `event_t_statistic`: fewer than two CARs; zero sample standard deviation.
  - `clustered_t_statistic`: unequal lengths; fewer than two clusters; an empty sequence.
  - `placebo_dates`: `count` greater than the number of eligible days; `half_window` negative.
  - `event_window_car`: `a > b` in the window; the estimation window would start before day 0 of the series.
  Every other invalid input is outside the spec: no test asserts an exception type for it (fixer rules, PROJECT GRADERS bullet).
- **Constraints.** Standard library, or numpy (the alternatives A1 and A2, §5.5 may use it). Every statistic is computed from
  unrounded values; the note states its rounding rule. Yields enter in percentage points; the note converts to basis points for
  display only. Every number in the note cites the series, its date range and its transform. No claim beyond the source's coverage
  (the FX note: spot rates only, no interest differential, `tools/data_sources.yaml:28-30`). The note makes no grade-B or grade-C
  claim without a key from the reading list (§5.4 criterion 5).
- **Grading mode.** Both: autograded by `grader/test_project.py` (the engine) and rubric-graded (the note) against the five criteria of
  §5.4, with the self-assessment form and two annotated exemplars. The grading entry names "autograder" and "rubric" (`tools/check_projects.py:38-50`).
- **Reading list** (`ol.reading-list`, `li data-cite`, registry keys only): `abadie2010synthetic`, `angrist2009mostly`,
  `goodmanbacon2021difference` (§7.1). Nothing else.

### 5.3 Time budget (`<table id="hours">`, sums to 30 h; a rationale on every row; `tools/check_projects.py:107-120`)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate the one run) | 2 | One solved SIMULATED run, annotated line by line |
| Rung 2, completion problem (two blanks, instant check) | 2 | Fill the variance term and the CAR sum, then run the instant check |
| Engine: eight functions and their tests (rung 3a) | 12 | The interface of §5.2, the named conditions, the instant check |
| Data intake: dates CSV schema, FX and yield transforms, the choice of normal model (rung 3b) | 5 | Document the schema, read the MANIFEST transforms, state the model |
| Research note draft and revision (rung 3c) | 6 | Two to four pages, every number quoted by `run_note.py` |
| Self-check against the grader and blind exemplar scoring (rung 3d) | 3 | Run the suite, score the exemplars, compare the scoring |
| **Total** | **30** | Equals `data-hours-project` on the hub |

### 5.4 Rubric (`table.rubric#rubric`; `tools/check_projects.py:58-72`)

Five criteria. Each criterion is one table row: the criterion name in a `th`, and exactly four `td` cells for levels 4 down to 1.
Every descriptor is observable.

1. **Data and timing.** Level 4: names the announcement dates, their source and the timing rule (event day, window, estimation
   window and gap); names each series with its date range and transform (`cmt_10y` in percent per year; FX as USD per unit);
   states whether the run is SIMULATED or real. Level 1: "uses the data".
2. **Normal model and variance.** Level 4: states the model used (market or constant-mean), its estimation length, and the
   variance of each abnormal return with its derivation or citation; reports `\sigma^2` with its divisor. Level 1: "fits a model".
3. **Inference.** Level 4: reports each CAR, its t-statistic and the clustering level, with the convention (CR1, the `G/(G-1)`
   factor) stated; shows the naive and the clustered t-statistics where they differ. Level 1: "reports a t-statistic".
4. **Placebo and multiple dates.** Level 4: states the number of placebo dates, their exclusion rule, and the rejection rate under
   the null with its replication count and seed; uses `1 − (1 − \alpha)^m` only with independence stated. Level 1: "runs a placebo".
5. **Limits and evidence.** Level 4: names each limit used in the reading (the normal-return model, clustering, spot-only FX, yield
   changes in place of returns, SIMULATED versus real data); states the grade and basis of every claim; and makes no grade-B or
   grade-C claim without a reading-list key. Level 1: "notes some caveats".

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, fully written notes on a SIMULATED instance,
annotated with the descriptors each passage meets or misses. Self-assessment form (`section.rubric-self`, `data-rubric="rubric"`,
`data-exemplars="exemplar-a exemplar-b"`, as in M1 and E1). The page shows where the student's scores diverge from the exemplar
scores. Calibration: a separate blind scorer scores both exemplars from a stripped copy of the prose, within one level per
criterion (FINAL-ARCHITECT-RULINGS ruling 15 and ruling 23). Not adversarial: no question bank (§12 Q15).

Known gap at the rubric level: the reading list has no counter-evidence key (§7.2). Criterion 5 therefore cannot require
counter-evidence at level 4 until a key is admitted. The page says so in one sentence.

### 5.5 Autograder design (`grading: both`; BUILDER_RULES §5.3; `tools/check_projects.py:122-137`)

- **Panel.** `section.grader-panel#grader data-unit="S6" data-grader="grader/" data-suite="test_project.py"
  data-support="instance.py" data-solution="event_study.py" data-starter="starter.py" data-packages="numpy"`, the pattern of
  `course/modules/S/S7/project.html:188`. The grader folder holds `instance.py`, `reference.py`, `test_project.py` and
  `starter.py`. `reference.py` is excluded from deployment (BLUEPRINT lines 400-401; FINAL-ARCHITECT-RULINGS ruling 4: no deploy step
  exists yet, so this is recorded, not enforced).
- **Instances (`grader/instance.py`).** `make_instance(seed: int) -> dict`, deterministic, standard library only, labelled
  **SIMULATED** in its docstring. It generates N firms (N in a stated range, for example 20 to 40), a market return series, a
  calendar of trading days, K events (K in a stated range, for example 6 to 12, distinct days), an estimation length L and an event
  window (a, b), cluster labels (announcement months), and planted announcement effects. Every instance is valid under the spec.
  Seeds 0 to 49 give materially different instances: the answers change, not only the labels (BUILDER_RULES §5.3).
- **Reference (`grader/reference.py`).** The full solution of the §5.2 interface. It passes every test on seeds 0 to 49.
- **Tests (`grader/test_project.py`).** Properties and numbers, with stated tolerances (1e-9 for exact formulas; a fixed statistical
  tolerance for planted-effect recovery, expressed as a number of standard errors fixed in the spec). Required tests:
  - each named `ValueError` condition, with an isolated test in both directions;
  - the market-model variance equals the formula at a hand-computed point (exact value), and reduces to the constant-mean form
    when the market term is removed;
  - `fit_normal_model` returns the exact OLS slope on a noise-free fixture, and the divisor `L − 2` on a fixture with known residuals;
  - `abnormal_returns` changes sign with the sign of the planted shock; `car` equals the sum over all entries (no dropped element);
  - `clustered_t_statistic` equals the CR1 value on a two-cluster hand case and differs from the iid value when clusters share shocks;
  - `event_t_statistic` uses the sample standard deviation (ddof 1) on an exact fixture;
  - `placebo_dates` returns distinct days, none within `half_window` of an event day, reproducible for one seed;
  - `event_window_car` is invariant to changes of the stock's returns outside the estimation and event windows, and changes by exactly
    `c × (b − a + 1)` when the event-window returns are shifted by a constant `c` (no look-ahead: the parameters do not move);
  - planted-effect recovery on large-effect instances within the stated tolerance (never a hard-coded value).
  Tests must not pass a trivially wrong or hard-coded answer. A failing check names the violated property and gives a hint at the
  concept; it never prints the expected value (`__tracebackhide__`, fixer rules, PROJECT GRADERS bullet). Each test finishes in under 5 s in
  Pyodide; the suite finishes in under 60 s. The page quotes the collect-only count of the final suite (as S7 quotes 162 checks).
- **Mutants (ten student errors; single-change copies of the reference under `ledgers/S6/mutants/`, first docstring line naming
  the error; the verifier writes them, `tools/mutate_graders.py --unit S6 --seeds 0-9`).**
  1. `m01_var_no_estimation_term`: `abnormal_return_variance` drops the `1/L` term.
  2. `m02_var_no_market_term`: `abnormal_return_variance` drops the `(R_m − mean)^2 / SS` term.
  3. `m03_sigma2_divisor_L`: `fit_normal_model` divides the residual sum of squares by `L` instead of `L − 2`.
  4. `m04_ar_sign_flipped`: `abnormal_returns` returns model minus actual.
  5. `m05_car_drops_last_day`: `car` sums all entries except the last.
  6. `m06_clustered_iid_se`: `clustered_t_statistic` uses the iid standard error.
  7. `m07_no_small_sample_factor`: `clustered_t_statistic` drops the `G/(G−1)` factor.
  8. `m08_placebo_ignores_exclusion`: `placebo_dates` ignores `half_window`.
  9. `m09_population_sd`: `event_t_statistic` divides by `K` (ddof 0) instead of `K − 1`.
  10. `m10_lookahead_fit`: `event_window_car` fits the normal model on the estimation window plus the event window.
  An eleventh probe (a stored answer for the seed-0 instance) is run as an integrity check. It is not one of the ten.
- **Alternatives (five correct implementations of different styles; each passes seeds 0 to 49; ruling 10).**
  - A1: market model by `numpy.linalg.lstsq`.
  - A2: normal equations solved by `numpy.linalg.solve`.
  - A3: pure-Python Gauss–Jordan elimination on floats.
  - A4: the abnormal-return variance through the hat-matrix form `1 + x_0^\top (X^\top X)^{-1} x_0`.
  - A5: CAR and its variance accumulated with `math.fsum`, the t-statistic through `statistics.stdev`.
  A float-based alternative that is wrong on a stated exact rule is a mutant, not an alternative (ruling 10).
- **Equivalence.** A mutant that differs only where the page states nothing goes to `ledgers/S6/equivalent/` with a README proof
  (ruling 9). None is planned.

---

## 6. Real-data policy (B1 and B2 apply)

- **Embedded, redistributable, grant quoted:** `fx_daily` (six currencies, daily, 2000-01-03 to 2026-09-30 per the transform,
  `tools/data_sources.yaml:42-43`), `fx_monthly` (not used by S6), and `ust_daily` (`tbill_3m` and `cmt_10y`, daily, 2000-01-03 to
  2026-09-30, `tools/data_sources.yaml:112-116`). S6 uses `fx_daily` and `cmt_10y` only.
- **Not embedded, and no grant found:** announcement calendars (B1), equity prices and index returns (B2).
  `tools/data_sources.yaml` `rejected:` (`:119-139`) lists the French library and Open Source Asset Pricing; neither grants a licence.
- **Honest-pending note** on the project's data page and on L07: "The brief asks for scheduled macro announcements. No
  redistributable calendar is embedded yet. The worked example and the grader use generated data labelled SIMULATED. The student
  supplies the dates in bring-your-own-data mode." Cited to DATA_REQUEST D1 (§7.3).
- **Labs.** No lab carries a `data-files` attribute (§12 Q17). The embedded snapshots are used only in the project's real-data run.
- **Real-data run.** Document the transform read from MANIFEST for each series (`fx_daily` and `cmt_10y`), and use the constant-mean
  model because no market index is embedded (§12 Q8).

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

| Key | Record (as read) | Status | Use in S6 |
|---|---|---|---|
| `abadie2010synthetic` | Abadie, Diamond & Hainmueller, JASA 105(490), 2010, DOI 10.1198/jasa.2009.ap08746 (`references/references.json:7`) | verified, `used_by: ["S6"]`; source string matches `curriculum/01-foundations.yaml:821` | L09 synthetic control (paper level; abstract read first); reading list |
| `angrist2009mostly` | Angrist & Pischke, *Mostly Harmless Econometrics*, Princeton University Press, 2009, edited-book record (`references/references.json:853`); `years` shows 2009 and 2019 | verified, `used_by: ["S6"]`; source string matches `yaml:819` | L01, L02, L03 book-level conventions; reading list. Cite the key; do not type a page or edition |
| `goodmanbacon2021difference` | Goodman-Bacon, J. Econometrics 225(2), 2021, DOI 10.1016/j.jeconom.2021.03.014 (`references/references.json:10612`) | verified, `used_by: ["S6"]`; source string matches `yaml:822` | L04 decomposition (paper level; abstract read first; general claim grade C until the locator is read); reading list |

Registry-verified keys **not** curriculum-listed for S6 (requires architect approval before use; default: not used):
`ball1968empirical` (`references/references.json:1508`, `used_by: ["AC3"]`; an event-study precedent in accounting) and
`fama1970efficient` (`references/references.json:8300`, `used_by: ["FC3"]`; a market-efficiency review). The rule that a key
must be verified applies; the `used_by` field is not changed (E5 precedent for `taylor1993discretion`: `plans/E5-build-plan.md` §7.1 and §12 Q4).

NOT usable: `andrews2023inference` (`references/references.json`, `used_by: ["S7"]`) is "Inference on Winners", not a
weak-instrument paper; `hansen1982generalized` (`used_by: ["AP3"]`) is Hansen & Singleton, not GMM for S5; `rubin2024type`
(`used_by: ["S7"]`) is a trial-and-error paper.

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- {doi: null, authors: "MacKinlay (lead only; the curriculum string is `curriculum/01-foundations.yaml:820`)", year: "1997 (curriculum string)", title: "Event Studies in Economics and Finance", venue: "Journal of Economic Literature, volume 35, issue 1 (curriculum string; record not typed)", needed_for: "L07 and the project's reading list, if the architect admits it", confidence: "the curriculum string exists; the review queue has no established identity (`references/review_queue.json:55-107`); the three candidates are different articles and must not be admitted (§0.3 B3)"}
- {doi: null, authors: "Rubin (lead only)", year: "not typed", title: "the potential-outcomes framework (originating work; not typed)", venue: "not typed", needed_for: "L01 attribution of the framework (paper level)", confidence: "the need is certain; no record is identified by this planner"}
- {doi: null, authors: "Imbens and Angrist (lead only)", year: "not typed", title: "the local interpretation of the Wald and two-stage estimands (originating work; not typed)", venue: "not typed", needed_for: "L02 two-sided treatment of any local-effect claim", confidence: "the need is certain; no record is identified by this planner"}
- {doi: null, authors: "Staiger and Stock; Stock and Yogo (lead only)", year: "not typed", title: "weak-instrument asymptotics and critical values (originating works; not typed)", venue: "not typed", needed_for: "L02 weak-instrument statement and any threshold (none is typed in S6 until admitted)", confidence: "the need is certain; no record is identified by this planner"}
- {doi: null, authors: "Callaway and Sant'Anna; Sun and Abraham; de Chaisemartin and D'Haultfœuille (lead only)", year: "not typed", title: "alternative estimators for staggered adoption (originating works; not typed)", venue: "not typed", needed_for: "L04 two-sided treatment of the staggered-adoption claim (BUILDER_RULES §2.5)", confidence: "the need is certain; no record is identified by this planner"}
- {doi: null, authors: "Imbens and Lemieux; Lee and Lemieux (lead only)", year: "not typed", title: "regression discontinuity design reviews (not typed)", venue: "not typed", needed_for: "L05 validity claims and bandwidth discussion", confidence: "the need is certain; no record is identified by this planner"}
- {doi: null, authors: "Brown and Warner (lead only); Campbell, Lo and MacKinlay (lead only; book)", year: "not typed", title: "event-study methods and power; the book on financial econometrics (not typed)", venue: "not typed", needed_for: "L07 two-sided treatment of event-study power and the normal-return model (BUILDER_RULES §2.5)", confidence: "the need is certain; no record is identified by this planner"}
- {doi: null, authors: "Literature on placebo tests and dependence across placebo dates (lead only)", year: "not typed", title: "not typed", venue: "not typed", needed_for: "L08 claims about placebo validity under dependence", confidence: "the need is certain; no record is identified by this planner"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4).
Until resolved, the lessons teach the models with derivations and no empirical attribution. Each empirical sentence is grade C at most
with its basis named, or is removed.

### 7.3 DATA_REQUESTS (for the architect; BUILDER_RULES §6.6, steps 1 to 5)

- **D1 (B1).** An announcement calendar. The architect reads the issuer's own calendar page, quotes the sentence that permits
  copying and redistribution with its page, and adds the entry to `tools/data_sources.yaml` before any `fetch_data.py --fetch`.
  The planner does not name the page or the licence from memory. Until then the project uses bring-your-own-data (§0.3 B1).
- **D2 (B2, optional).** A cleared equity return or price series, for an equity-reaction rung-4 variant. None is identified. Until
  one is admitted, equity reactions are bring-your-own-data only.

---

## 8. Atlas milestone

None. The S6 project has no `atlas:` key (`curriculum/01-foundations.yaml:824-830`), and no Atlas entry names S6 (computed:
`curriculum/curriculum.json` `atlas` array). No `atlas/S6.contract.md` is needed, and `check_projects.py` skips the contract check
(`tools/check_projects.py:144-146`). The brief names no Atlas milestone, so B2 of E5 (the brief's Atlas wording) does not arise.

---

## 9. Cards builder (Builder F, after A to D)

- `course/modules/S/S6/cards.json`, ids `S6-c001` upward, `lesson` in L01 to L09, one card per definition, theorem statement,
  key formula, key result and misconception (BUILDER_RULES §7). `tools/check_pages.py` `check_cards` (line 366) checks the id prefix,
  the lesson existence, the grades and the registry keys.
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example
  `"basis": "Lab 3 (exact), Derivation in L03"`.
- Cite a registry key only for an attributed claim. `cite` is `[]` where the card is a model result.
- A card whose result is a lab output carries grade C and `basis` naming the lab, as the card and key-results row must match (ruling 13).
- Cards for SIMULATED results name the SIMULATED lab in `basis`.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit S6            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit S6
.venv/bin/python tools/check_projects.py --unit S6
.venv/bin/python tools/run_labs.py --unit S6               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/S/S6/L01.html                          # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/S/S6/L07.html --refresh lab-S6-L07-1    # after editing a twin
.venv/bin/python tools/run_graders.py --unit S6 --seeds 0-49        # builder E: the reference and the suite
.venv/bin/ruff check tests/labs/S6 course/modules/S/S6/grader && .venv/bin/ruff format --check tests/labs/S6 course/modules/S/S6/grader
.venv/bin/mypy tests/labs/S6 course/modules/S/S6/grader           # strict, repository configuration
```

Verifier only, on a quiet machine: `.venv/bin/python tools/mutate_graders.py --unit S6 --seeds 0-9` (the ten mutants and the
eleventh probe), `.venv/bin/python tools/page_smoke.py --unit S6` (not run by builders; timing-sensitive), and
`.venv/bin/python tools/verify_refs.py --unit S6` (the unit ledger's run, VERIFIER §2.1). `tools/fetch_data.py --check` only if a
dataset is added (B1, B2).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`,
and the full gate in CLAUDE.md.

Flag checks: `tools/check_pages.py` and `tools/check_dag.py` accept `--unit`; `tools/check_projects.py` accepts `--unit`;
`tools/run_labs.py` accepts `--unit` and `--page`; `tools/embed_labs.py` accepts pages and `--refresh [LAB_ID ...]`;
`tools/run_graders.py` accepts `--unit` and `--seeds` (`tools/run_graders.py:126-139`). The planner did not execute any builder command;
it ran only the coursekit closure, concept-owner and topological-order functions (§0.1).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** No `atlas:` key on the S6 project; no Atlas entry names S6 (§8). `check_projects.py` skips the contract
   check (line 144-146).
2. **No debate key.** `check_pages.py` requires a debate brief only when the curriculum tags one (line 412-413). The two-sided rule
   (BUILDER_RULES §2.5) still applies to the staggered-adoption, RDD and event-study claims.
3. **Grading `both`.** A grader is required: the grader panel, the instance generator, the reference, the starter
   (`tools/check_projects.py:122-137`), and the rubric with two exemplars at two levels (`:58-72`). The grading entry names both
   words (`:38-50`). This differs from E5 (rubric only); the E5 mutation exception does not apply.
4. **Rungs 1 and 2 are minimal** (tier M; BLUEPRINT §4, lines 222-223). `check_projects.py` does not check length; the builder keeps
   them short.
5. **Closure contains unbuilt modules** (S0, S1, S2, CS1). Concept links go to `concepts.html` anchors only (§0.3 N2).
6. **`check_dag.py` sees linked uses only** (`tools/check_dag.py` docstring). Unlinked uses of the §4 names pass the tool; the verifier
   reads for them (VERIFIER §2.9).
7. **Labs are standard-library only**; the grader panel declares `data-packages="numpy"` for the numpy alternatives (§5.5).
   `numpy` and `scipy` are vendored packages (`tools/vendor_spec.yaml:59`).
8. **The hub hours rules** (`tools/check_pages.py:227-228`, `:337-342`) are satisfied by §0.2.
9. **The "first-year sequence" grouping** (`curriculum/meta.yaml:131`) lists S6 as "Econometrics I–II", while S6 is tier M.
   This is a grouping observation only; the plan does not act on it (§12 Q20).
10. **The seed-0 integrity probe** is outside the ten mutants (§5.5). It is run by the verifier and recorded separately.

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **Lesson count and hours.** RECOMMENDED: 9 lessons (7, 9, 8, 8, 8, 8, 8, 7, 7 = 70 h) and a 30 h project (§0.2, §1). Alternative
   within the rules: 10 lessons at 7 h each (splits IV from weak instruments). The S7 precedent is 8 lessons at 70 h.
2. **Builder ownership.** RECOMMENDED: A = L01 to L03 and `index.html`; B = L04 and L05; C = L06 and L07; D = L08 and L09; E = project,
   grader and project labs; F = cards after A to D (§1).
3. **B1, announcement dates.** RECOMMENDED: bring-your-own-data CSV for the dates; DATA_REQUEST D1 for the Board's calendar, read and
   quoted by the architect before any embedding. No calendar is embedded until then (§0.3, §7.3).
4. **B2, asset-price scope.** RECOMMENDED: the reactions are measured in `cmt_10y` yield changes (percentage points) and FX log returns;
   equities are bring-your-own-data only (§0.3).
5. **B3, MacKinlay (1997).** RECOMMENDED: the architect admits the real article through the manual path from its publisher's stable URL
   (`tools/add_reference.py`). The three review-queue candidates are rejected. Until admitted, no builder cites it (§0.3, §7.2).
6. **D1 and D2, S5 concepts** (`panel-fixed-effects`, `generalized-method-of-moments`). RECOMMENDED: no prerequisite change;
   two-way fixed effects as OLS with indicators; no GMM (§4). Adding S5 would also add S3 to the closure.
7. **D12, unregistered terms** (market model, parallel trends, event window, first stage, and the rest). RECOMMENDED: plain prose and
   a plain `<dfn>` with no `data-concept` at first use. The architect may register any of them as a curriculum change (§4 D12).
8. **Normal model for the real-data run.** No market index is embedded. RECOMMENDED: the constant-mean model for the note's real run;
   the market model for the SIMULATED autograder instances; both named in §5.2.
9. **Dates-file validation.** RECOMMENDED: the schema is documented on the page and validated by the student's `analysis/run_note.py`.
   No in-browser JS validator is added (architect standing default: no new JS kernels, `plans/E5-build-plan.md` last section).
10. **D6, multiple testing.** RECOMMENDED: L08 derives `1 − (1 − \alpha)^m` under independence and names no S7 concept; the
    `\FWER` and `\FDR` macros are not used (§2.3, §4 D6).
11. **Canon REFERENCE_REQUESTS** (§7.2). RECOMMENDED: admit the leads needed for any two-sided claim the architect wants in the lessons.
    Until then, no grade-B or grade-C claim is made on IV, weak instruments, RDD, staggered-adoption alternatives or event-study power.
12. **Counter-evidence for the rubric** (§5.4 criterion 5). RECOMMENDED: criterion 5 requires a grade and a basis for each claim,
    and a reading-list key for any B or C claim. The note makes no such claim until a key is admitted.
13. **Mutants and alternatives** (§5.5). RECOMMENDED: the ten mutants m01 to m10, the eleventh integrity probe, and the five
    alternatives A1 to A5, as listed.
14. **Figures.** RECOMMENDED: none (architect standing default; `plans/E5-build-plan.md` last section). No `figures-*.js`.
15. **Adversarial.** RECOMMENDED: not adversarial; no question bank (architect standing default).
16. **Rungs 1 and 2 (tier M).** RECOMMENDED: one worked example (one run) and one completion lab with two blanks (§5.1).
17. **Labs and embedded data.** RECOMMENDED: no lab reads an embedded snapshot; the real-data path lives in the project's student run.
18. **Notation.** RECOMMENDED: the local symbols and rules of §2.3; no NOTATION_REQUESTS; `T` never used for a count or a horizon.
19. **Interface freeze.** RECOMMENDED: the architect freezes the eight signatures of §5.2 before Builder E starts; the
    named conditions in §5.2 are then fixed.
20. **First-year grouping** (`curriculum/meta.yaml:131`). RECOMMENDED: no action; confirm.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 builder commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01 to L03 (includes the curriculum-adjacent IV labs), L04 and L05,
   L06 and L07 (includes the curriculum lab), L08 and L09, the project (grader, mutants, alternatives, the rubric and exemplars).
   Failing rows return to the builder that owns the file, with only the failing rows.
3. The exemplars are scored blind by a separate scorer that never opens the project page (FINAL-ARCHITECT-RULINGS ruling 23).
4. Ledger at `ledgers/S6.verification.json`; mutants under `ledgers/S6/mutants/` (ten), the integrity probe under `ledgers/S6/scripts/`,
   the five alternatives under `ledgers/S6/alternatives/`, and any equivalent mutant under `ledgers/S6/equivalent/` with a README proof
   (VERIFIER §3; FINAL-ARCHITECT-RULINGS rulings 9 and 19).
5. The branch merges only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 and B3 are resolved, or named
   as honest gaps, before the project is verified.
6. Open items and DATA_REQUESTs go to `plans/S6-open-items.md`, written by the architect, not by a builder.

Architect decisions: pending (§12). This plan is the planner's proposal. The standing defaults at the end of
`plans/E5-build-plan.md` (concepts outside the closure are plain prose; no real data without a quoted grant, otherwise SIMULATED with
an honest-pending note; no figures; ten mutants and five alternatives; not adversarial) apply to S6 unless the architect overrides them.
