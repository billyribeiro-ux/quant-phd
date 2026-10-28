# FI1 build plan: Bond Math & Curve Construction (planner output, 2026-10-28)

Unit: **FI1 · Bond Math & Curve Construction** · tier U · 90 h · prerequisites M2, CF1 · Atlas milestone **A5** ("Curve
engine") · grading `autograder` · output directory `course/modules/FI/FI1/` (part code `FI`) · lab twins `tests/labs/FI1/`.
Branch `claude/fanout-b3`. Planner: Haiku, plan only. No lesson content, no git operations, no commits, no contract
drafted. Executors: Haiku builders, then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never
writes a ledger.

**Status: two blocking items (§0.1). Lessons L01-L08 can start now. The project cannot pass `check_projects.py` until
`atlas/A5.contract.md` exists, and it does not exist (checked: `atlas/` holds only `A8.contract.md` and `A15.contract.md`).**

Evidence convention: every statement about the curriculum cites `file:line`, read during planning. Anything not in the
curriculum is marked **NOT IN CURRICULUM**. Anything about a source's content that the planner did not read is marked
**UNREAD**.

---

## 0. Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part FI, code `FI`, title "Fixed Income & Rates"; STUDIO-FI requires FI1, FI3 (not a FI1 requirement) | `curriculum/03-markets.yaml:4-8`, `:17` |
| FI1 id, title, tier U, hours 90 | `curriculum/03-markets.yaml:19-22` |
| FI1 prereqs `[M2, CF1]` | `curriculum/03-markets.yaml:23` |
| Core text: pricing, yield conventions, day counts, duration, convexity, DV01, bootstrapping, Nelson–Siegel and Svensson, the GSW curve | `curriculum/03-markets.yaml:24-26` |
| `introduces` has 16 concepts | `curriculum/03-markets.yaml:27-43` |
| Sources (free text, three): Nelson & Siegel (1987) JBus 60(4); Svensson (1994) NBER WP 4871 tagged `[WP]`; Gürkaynak, Sack & Wright (2007) JME 54(8) | `curriculum/03-markets.yaml:44-47` |
| Lab: "Fit Nelson–Siegel to an embedded curve." | `curriculum/03-markets.yaml:48` |
| Project "Atlas A5: curve engine", brief "Add bootstrapping, NS / Svensson fitting and full day-count support to Atlas, tested against published GSW parameters.", deliverable "Atlas at milestone A5.", grading `autograder`, `atlas: A5` | `curriculum/03-markets.yaml:49-56` |
| No `debate` key on FI1 (no debate brief required) | `curriculum/03-markets.yaml:19-56` (absent) |
| Atlas block: `A5`, module FI1, title "Curve engine" | `curriculum/meta.yaml:215-218` |
| JSON row for FI1 mirrors the YAML (hours 90, prereqs M2 CF1, 16 introduces, lab, project, atlas A5) | `curriculum/curriculum.json:8624` (`"id": "FI1"`), atlas block `:8662` |
| Rendered CURRICULUM.md row: "FI1 · Bond Math & Curve Construction · U · 90 h · ← M2, CF1 · ⚑ A5" | `CURRICULUM.md:591` |
| CF1 prerequisites now `[M1, AC1]` (the architect's CF1 decision, applied in the yaml) | `curriculum/02-economics-finance-core.yaml:673` |
| M2 prerequisite `[M1]`; M2 is not built (`course/modules/M/` holds only M1) | `curriculum/01-foundations.yaml:126`; `course/modules` listing |

Registry keys that exist for FI1 (`references/references.json`, all `status: verified`, `used_by: ["FI1"]`):

| Key | Record (as read) | Matches the curriculum string? |
|---|---|---|
| `nelson1987parsimonious` | Nelson & Siegel, "Parsimonious Modeling of Yield Curves", *Journal of Business*, vol 60, issue 4, year 1987, first page 473, doi 10.1086/296409 (`references/references.json:17886`) | Yes (authors, venue, 60(4)). Do not cite a page beyond the record. |
| `gurkaynak2007us` | Gürkaynak, Sack & Wright, "The U.S. Treasury yield curve: 1961 to the present", *Journal of Monetary Economics* 54(8), 2007, doi 10.1016/j.jmoneco.2007.06.029 (`:11264`) | Yes (authors, JME 54(8)). The record title is the paper's, not "GSW curve". |
| `svensson1994estimating` | Svensson, "Estimating and Interpreting Forward Interest Rates: Sweden 1992 - 1994", type `report`, publisher NBER, doi 10.3386/w4871, year 1994 (`:21567`) | Yes, except the title's spacing ("1992 - 1994" in the record, "1992-1994" in the curriculum). A working paper: grade at most C, with the version date (BUILDER_RULES §2.5). |

No registry key exists for: a fixed-income textbook, any day-count convention authority (ISDA or ICMA), the Treasury or
Federal Reserve yield-curve methodology, the GSW published parameter file, or any bond-pricing reference. See §6.

---

## 0.1 Blocking items (for the architect; not resolved by this plan)

**B1. Atlas contract missing.** `atlas/A5.contract.md` does not exist (`ls atlas/`). `check_projects.py` lines 145-146
fail any project whose `atlas` key names a missing contract. BUILDER_RULES §5.5 requires the builder to implement that
contract exactly. This planner does not draft it. Consequence: the project builder (rung 3, grader) is blocked; lessons
L01-L08 are not. Required: the architect drafts `atlas/A5.contract.md` (module path, function signatures, units, money
type, error types), per BLUEPRINT §5.1.

**B2. The curriculum lab names an embedded curve that the registry cannot supply.** The only embedded yield curve is
`ust_daily`, with two columns, `tbill_3m` and `cmt_10y` (`course/assets/data/market/MANIFEST.json:63` and its `columns`
field; `tools/data_sources.yaml:91-110`). Nelson–Siegel has four parameters (λ plus three betas, NOT IN CURRICULUM as a
count; the model's parameter count is a fact the builder must read in `nelson1987parsimonious`, **UNREAD**). Two
maturities cannot fit it. The H.15 release carries more constant-maturity series, but a new snapshot needs (a) the
series identifiers read from the H.15 XML, which the planner did not do and will not type from memory, and (b) a
`tools/data_sources.yaml` entry with the licence quote. Options, in the planner's order:
- (a) DATA_REQUEST for an H.15 constant-maturity snapshot. The Board's licence text is already quoted in
  `tools/data_sources.yaml` for H.15 (`:91-110`), and the architect confirms it covers the new series. Then the lab reads it
  via `data-files`.
- (b) **Fallback that is honest now:** the L06 lab runs on a SIMULATED curve with generating parameters (labelled
  SIMULATED on the page), and the page carries an honest-pending note naming the DATA_REQUEST for the real curve.
Planner recommends (b) immediately and (a) as a follow-up.

**B3. Published GSW parameters.** The project brief requires testing "against published GSW parameters" (`curriculum/03-markets.yaml:52-53`).
The registry holds the GSW paper (`gurkaynak2007us`) but not a parameter file, and the planner has no licence evidence for
any GSW parameter file. Until the architect supplies a DATA_REQUEST with a quoted redistribution statement (BUILDER_RULES
§6.6), the grader's "published parameters" test is an **honest-pending** test: it is written, skipped with a named reason
on the project page, and never fabricated. The autograder's other tests run on SIMULATED instances.

Non-blocking: the Atlas cumulative suite (A1 through A5) cannot be green, because A1-A4 (CS1, CS3, S0, S4) are not built
(`course/modules` holds M, AC, AP, CF, S/S7 only). The FI1 grader runs standalone. Reported as a gap, not a build defect.

---

## 1. Hours (feasible; no STOP condition)

The curriculum figure is 90 h (`curriculum/03-markets.yaml:22`). Tool rules:
- lessons: each `data-hours` 6-12 (`tools/check_pages.py`, `check_lesson`, about line 228);
- hub: `data-hours-lessons + data-hours-project = 90`, project share 10-40 % of 90 (9 to 36 h), and lessons sum to the
  hub's lessons figure (`tools/check_pages.py`, `check_hub`, lines 325-342).

Chosen split: **8 lessons × 9 h = 72 h; project 18 h (20 %)**. Feasible.

Alternative (open question Q4): 7 lessons, 10 h each for six of them and 12 h for one, which merges L06 and L07 (NS and
Svensson). Also feasible; not recommended here, because the NS and Svensson fits are separate labs.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to FI1)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `VERIFIER_RULES.md` §2 (what a verifier will
check), `plans/M1-build-plan.md` and `plans/E1-build-plan.md` (their Architect decisions are binding precedent), this file.
Study `course/modules/M/M1/` (hub, project, grader panel, lab layout), `course/modules/CF/CF1/` (lab twins with `random.Random`
seeding; project ladder) and `course/modules/AC/AC2/` (grader panel with numpy). Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction` where the
   arithmetic is exact, otherwise full-precision float) and rounded only at display. A page that shows a rounded figure
   names the rounding rule. Precedent: E1 §2.1 item 1, AC4 KNOWN LIMITATION 3.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints; the interpretation names only
   what the printed numbers show. The phrase "checked", "verified" or "reproduced" names the lab, line or test that did
   the check. Precedent: M1 LESSON_TEXT_DEFECTS.
3. **Attribute nothing unread.** Cite only the three FI1 keys in §0 and any key the registry gains (§6). A model's formula
   (NS, Svensson, Macaulay duration, the day-count rules) is attributed to its source **only** after the builder has read the
   locator in the paper. Otherwise the formula is a definition written on the page with no citation, or a derivation
   (grade T where it is algebra). No page, table, equation number or coefficient is typed from memory. Precedent: AC2, AC4 §0.
4. **Scope words need a computation.** "every bond", "all conventions", "any curve", "the market", "always", "never",
   "standard" are used only where a proof, a finite check or a lab computes the claim. The core text's "day counts" and
   "the GSW curve" name a scope, so each page states which conventions and which curve it covers. Precedent: E1 §2.1 item 4,
   and E1 Q8 on "market structures".
5. **Define before use.** Each of the 16 concepts is defined once with `<dfn id="def-<id>" data-concept="<id>">` in its
   assigned lesson (§3), never before it. A lesson uses a concept only after the lesson that defines it. Terms outside the
   16 concepts (for example "stub period", "spot curve", "least squares", "root-finding", "par bond", "accrued interest
   convention") are plain prose, or a plain `<dfn>` without `data-concept` (E1 Q10 precedent; `check_dag.py` skips it).
   `check_dag.py` checks linked uses only; the verifier reads every lesson for unlinked use (VERIFIER §2.9).
6. **Proposition hypotheses explicit (T-grade).** Every Theorem or Proposition block lists its assumptions as numbered
   items, named `Assumption 1, 2, ...`, before the statement. Examples the lessons will need: positive cash flows and a
   yield above -1 (L01 price-yield monotonicity); integer coupon periods for the closed-form price (L01, L04); no
   arbitrage between coupon-bearing and zero-coupon bonds of the same maturity (L05 bootstrapping); the nesting condition
   beta-3 = 0 for Svensson-reduces-to-NS (L07). An assumption not used in a proof is removed.
7. **Grader tests demand an exception type only for conditions the page names.** §5.4 lists the named conditions and the
   exception type for each. Any other invalid input may raise any exception or return. **Five alternative correct
   implementations** must pass the suite (§6.6). The verifier writes all five.
8. **Integer cents for money.** Every money output of the engine (dirty price, accrued interest, cash amount on a stated face)
   is an `int` in cents, computed from exact arithmetic where possible and rounded once, half up, by the rule stated on
   the project page. Quoted prices and yields are not money: they are `Fraction` or float with the tolerance stated on the
   page (precedent: E1 Q6; AC4 Q9-Q10). Architect confirms (Q6).
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container, and code blocks scroll inside their own
   container. No element forces the page wider than 360 px. `page_smoke.py` is the verifier's check.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no
    `if __name__ == "__main__":` guard. `run_labs.py` runs each twin as `python -I -W error <twin>` (`tools/run_labs.py`,
    `run_twin`, lines 51-60; `-W error` means a warning fails the lab).
11. **Notation registry is binding** (§5). A registered symbol never takes another meaning, and the FI1 pages do not reuse
    `T` for a maturity.
12. **Ten student-error mutants** for the project (§6.5), in place of the verifier's usual three. Each must be killed.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. `data-cite` only
  for the keys in §0 or §6.
- Prerequisite links: `href="../../../concepts.html#<id>"` for M2, M1, CF1, AC1 and P0.1 concepts (§4); `href="Lnn.html#def-<id>"`
  for earlier FI1 lessons. A lesson never links a concept defined later.
- Labs: code lives once in `tests/labs/FI1/lab-FI1-Lnn-1.py` (and `lab-FI1-project-1..3.py`). The page carries `@@LAB:<file>@@`
  and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-FI1-<page>-<n>`
  (`check_pages.py` line 258). Labs are seeded (`random.Random(seed)`), use the standard library plus NumPy (§5.5 explains
  why NumPy and not SciPy), run under 10 s in Pyodide, make no network request, and emit no warnings (`-W error`).
- Python code on a page must be a lab (`data-run`) or a checked snippet (`data-check="sol-FI1-<page>-<id>"` with a matching
  `<pre class="expected" data-check>`). Any other Python code block fails `check_pages.py` `check_code`
  (`tools/check_pages.py` lines 145-160). Pseudocode is labelled `class="language-pseudocode"`.
- **Banned strings** (`tools/check_pages.py` lines 58-73, matched on visible text, case-insensitive): TODO, TBD, lorem,
  "for brevity", "details omitted", "beyond the scope", "left as an exercise", "you can add more", "it is important to
  note", "studies show", "experts agree", "it is well known", "obviously", "clearly", and the three-dot ellipsis `...`
  anywhere in visible text. Python `...` (the Ellipsis literal) is therefore not used in any visible code block either.
  Use `raise NotImplementedError` in starter stubs.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Never edit `curriculum/*.yaml`. Request changes.
- Learner-visible text has no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning
  references in code comments (precedent: M1 "Convention (project Q5)" defect; AC4 KNOWN 9).
- Percent changes state the base and the direction. Basis points are stated as "1 bp = 0.01 percentage point" once, then used.
- A finite enumeration is grade C with its basis named, not grade T (precedent: M1 L06).
- Day counts and yield conventions are stated explicitly on every page that uses them: the numerator and denominator rule,
  the compounding frequency, and whether the rate is annual or per period. Units on every axis and table column.
- Hub lesson titles match each lesson's `<h1>` at integration (precedent: CF1 KNOWN 3).
- Quiz explanations are read against their lesson (precedent: CF1 KNOWN 6).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10
  output contract.

---

## 3. Outline and file ownership (proposed; the architect confirms)

Lessons: 8 × 9 h = 72 h. Concepts: 16, each in exactly one row. Concept counts per row: 2+3+4+3+1+1+1+1 = 16, matching
`curriculum/03-markets.yaml:28-43`.

| Lesson | Title (working) | Concepts it defines (`introduces`, yaml 28-43) | Lab (twin id, `tests/labs/FI1/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Bond cash flows, the price–yield relation and yield to maturity | `bond-price-yield`, `yield-to-maturity` | `lab-FI1-L01-1`: price of a fixed-coupon bond at a grid of yields; yield to maturity by bisection, residual printed; price falls as yield rises (Assumptions 1-2) | 9 | Builder A |
| L02 | Yield quotation conventions, day counts and clean and dirty price | `yield-conventions`, `day-count-convention`, `clean-and-dirty-price` | `lab-FI1-L02-1`: ACT/360, ACT/365 and the stated 30/360 variant on fixed date pairs; accrued interest and dirty price in integer cents on a stated face | 9 | Builder A |
| L03 | Spot rates, forward rates, the par yield and the term spread | `spot-rate`, `forward-rate`, `par-yield`, `term-spread` | `lab-FI1-L03-1`: spot rates from a SIMULATED par set; forward identity (1+s2)^2 = (1+s1)(1+f) checked exactly with Fraction; term spread printed | 9 | Builder A |
| L04 | Duration, convexity and DV01 | `duration`, `convexity`, `dv01` | `lab-FI1-L04-1`: Macaulay and modified duration, convexity, DV01 against a central finite difference of price; step size stated, error printed | 9 | Builder B |
| L05 | Bootstrapping the zero curve | `curve-bootstrapping` | `lab-FI1-L05-1`: zero rates bootstrapped from SIMULATED par bonds; every input bond repriced to tolerance | 9 | Builder B |
| L06 | The Nelson–Siegel model (**the curriculum lab**) | `nelson-siegel-model` | `lab-FI1-L06-1`: fit Nelson–Siegel to an embedded curve, see §5.2 and B2; parameter recovery on the SIMULATED curve with the generating parameters printed | 9 | Builder C |
| L07 | The Svensson model | `svensson-model` | `lab-FI1-L07-1`: Svensson fit on a SIMULATED two-hump curve; the nested check (second hump off) reproduces the Nelson–Siegel fit | 9 | Builder C |
| L08 | The GSW curve and comparing curve methods | `gsw-curve` | `lab-FI1-L08-1`: bootstrapped versus Nelson–Siegel versus Svensson zero rates on one SIMULATED curve, pricing error per method; published GSW parameters are honest-pending (B3) | 9 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 72 / 18, reading | none | none | - | Builder A |
| project | Atlas A5 curve engine (`autograder`), §6 | none | `lab-FI1-project-1` (rung 1), `lab-FI1-project-2` (rung 2, `class="lab completion"`), `lab-FI1-project-3` (rung 3 check) | 18 | Builder E (after B1 is cleared) |
| grader | `grader/reference.py`, `starter.py`, `instance.py`, `test_project.py` | none | none | - | Builder E |
| cards | `cards.json` from L01-L08 | none | none | - | Builder F (after A-D) |

Ownership rule: a builder writes only its lesson files and twins. Builder A writes the hub after L01-L03 exist, so the lesson
map is right; the hub cross-check runs at integration. Builder E's grader is independent of the lessons, but its files wait for
B1.

Ordering check (no lesson links a later definition):
- L02 uses L01's yield (`yield-to-maturity`) for the dirty price's yield quote.
- L03 uses L01 (yield to maturity, and the M1 `discount-factor`) for spot rates from par bonds; `par-yield` is defined after
  the spot rate it is compared with.
- L04 uses L01 (price-yield) and M2 `derivative` (linked) for the duration definition, and M2 `taylor-theorem` (linked) for
  convexity as the second-order term.
- L05 uses L03 (spot rate, par yield).
- L06 uses L03 (spot rate) and L05 (curve bootstrapping) as the comparison.
- L07 uses L06 (`nelson-siegel-model`), as the extension.
- L08 uses L05, L06 and L07 for the comparison.

Lesson-internal rule: `check_pages.py` `check_lesson` requires each lab to sit before the lesson's `#canon-breaks` section.

---

## 4. Prerequisite closure and the DAG

`coursekit.prerequisite_closure("FI1")` (run by the planner in `.venv`) returns `{M2, CF1, M1, AC1, P0.1}`. Usable without
definition: concepts introduced by M2 (13), M1 (14), CF1 (10), AC1 (12), and P0.1 (11), 60 in total (curriculum.json
`parts` rows; `curriculum/03-markets.yaml:44-47` is the FI1 source list).

Linkable concepts the FI1 pages will use (all in the closure):
- M2: `derivative` (L04), `taylor-theorem` (L04), `limit` (only if L04 names the continuous-time limit; otherwise unused).
- M1: `present-value`, `discount-factor`, `annuity`, `perpetuity` (L01, L03), `exponential-and-logarithm`, `continuous-compounding`,
  `compounding-frequency` (L01, L02, L03), `amortization-schedule` (optional, L01).
- CF1: `internal-rate-of-return` (L01: the yield to maturity is the internal rate of return of the bond's cash flows; a link is
  allowed because CF1 is in the closure), `net-present-value` (L01, L03).
- AC1: `accrual-accounting` (L02, accrued interest as an accrual; optional).
- P0.1: `evidence-grade`, `replication` where a lesson grades an empirical claim.

Concepts outside the closure that the natural content would use. Each is written as plain prose, unlinked, and reported as a
DAG_DEFECT row, or avoided:

| Idea | Owner (curriculum.json `concepts`) | Where it appears | Resolution in this plan |
|---|---|---|---|
| Least squares (NS, Svensson fit) | none; `ols-estimator` is S2 | L06, L07, project | Plain prose "least-squares fit"; no link; DAG_DEFECT (Q6) |
| Root finding (YTM by bisection) | none in `concepts` | L01, project | Plain prose "bisection"; no link (not a concept) |
| Expectations hypothesis | FI3 (`curriculum/03-markets.yaml:97`) | L03 Remark, if mentioned | Mention only in prose as "a later module", no link, no definition |
| Short-rate models (Vasicek, CIR) | FI2 (`short-rate-model`) | out of scope | Not used |
| Interest-rate swap, forward rate agreement | FC2 / none | out of scope | Not used |

No `DAG_DEFECT` blocks the build if the rows above are resolved as stated. The architect confirms (Q6).

---

## 5. Hub, labs and real-data policy

### 5.1 Hub (`index.html`, Builder A)

- `<main data-hours-lessons="72" data-hours-project="18">` (sums to 90; project 20 %).
- 4-8 measurable objectives (verbs: compute, derive, price, convert, fit, compare). Example: "Compute the price of a fixed-coupon bond from its yield on a stated day-count convention."
- Prerequisites: M2, CF1, with concept links to `../../../concepts.html#<id>` for the closure concepts used (§4). Do not link an unbuilt M2 page (M2 is not built).
- Placement: `<section class="quiz" id="placement" data-unit="FI1" data-page="placement" data-mastery="0.8">`, with at least two `data-skill` items on what rungs 1-2 teach (the worked example's price-and-yield computation, and the completion problem's dirty-price step) and the rest testing the closure's prerequisites (M1 present value and annuities; M2 derivatives; CF1 IRR).
- Lesson map linking L01-L08 (`href="L01.html"` ... `L08.html`) and `project.html`.
- Project ladder: `ol.ladder` with four `rung-title` items in order: Worked example, Completion problem, Independent project, Stretch.
- Tier U: rungs 1-2 keep full length. BLUEPRINT §4 reduces them only from tier M upward.

### 5.2 Labs (one per lesson; project labs separately)

- Eight lesson twins plus three project labs (M1 Q2 and E1 precedent). The curriculum names one lab (`curriculum/03-markets.yaml:48`), which is L06's lab (planner's assignment, Q2).
- Each lab states its hypothesis, prints its result, and its interpretation names only what the output shows.
- SIMULATED labelling: every generated curve, par set, price set or grader instance carries **SIMULATED** in the lab's hypothesis and in the project spec. Exact-arithmetic checks (forward identity, day-count fractions, reprice-to-tolerance) are not labelled SIMULATED, because they are computations (E1 §2.2).
- **L06 data (B2):** primary option is a `data-files` snapshot after a DATA_REQUEST; fallback is the SIMULATED curve. The fallback must say, on the page, which real curve is pending and why.

### 5.3 Figures

No figures in this plan (planner recommendation; Q5). A figure would need a kernel in `course/assets/js/stats.js` or a new one, plus a test in `tests/test_figure_kernels.py` before use (BUILDER_RULES §6.4). If the architect approves figures, the L03 spot-and-forward curve and the L06 fitted curve are the candidates.

### 5.4 Data (BUILDER_RULES §6.6; BLUEPRINT §5.3)

- **Embedded now:** `ust_daily` (`course/assets/data/market/ust_daily.csv`; `MANIFEST.json:63`; columns `tbill_3m`, `cmt_10y`; `tools/data_sources.yaml:91`). It is the Board's H.15 release with the licence quoted in `data_sources.yaml`. It has two maturities, so it cannot support a four-parameter NS fit (B2). It is usable for L02's day-count illustration only with the `tbill_3m` discount-basis caveat that the MANIFEST `note` states (read it before use; BUILDER_RULES §6.6).
- **DATA_REQUESTS** (not made by the planner; the architect or a human decides):
  1. H.15 constant-maturity series for NS and Svensson fitting (source URL: the H.15 release zip already in `tools/data_sources.yaml`; series identifiers **to be read from the zip**; licence quote: the Board's disclaimer already quoted; transform: pinned end date, daily).
  2. The published GSW parameter file (B3). The source URL, its own licence statement and the transform are not known to the planner (**UNREAD**).
- **Rejected in advance, not requested:** Kenneth French Data Library and Open Source Asset Pricing (`tools/data_sources.yaml` rejected list). Not needed by FI1.
- **No other dataset.** Real corporate bond prices are not in the registry and no bond-price dataset is requested. Bring-your-own-data mode (BLUEPRINT §5.3) is the project's stretch option if a student wants real prices.

### 5.5 Pyodide packages

Labs and grader may use NumPy, which the repo already runs (`tools/run_graders.py` line 35; `course/modules/AC/AC2/grader/*.py`). SciPy is not planned: the NS and Svensson fits use a grid over the decay parameter(s) plus linear least squares with NumPy (variable projection), and root finding uses bisection written in the lab. The reason is that no `scipy` line is confirmed in the Pyodide package list for this repo (**UNREAD**: `tools/vendor_spec.yaml` not read by the planner for this purpose). The architect confirms (Q7). `data-packages="numpy"` on the grader panel.

---

## 6. Project (`project.html`, Builder E, after B1)

### 6.1 Ladder (BLUEPRINT §5.1; `check_projects.py` line 33 requires the order)

1. **Rung 1, worked example** (`lab-FI1-project-1`): one fully solved and annotated SIMULATED bond: dirty price, yield to maturity, duration and the DV01 line, each step with a "why" note.
2. **Rung 2, completion** (`lab-FI1-project-2`, `class="lab completion"`): the same bond with the accrued-interest line and the DV01 step replaced by `___`. Graded instantly. Its twin is the completed solution; each page line equals the twin's line or contains a blank.
3. **Rung 3, independent project** (graded): the autograded engine `curve_engine.py` (module-local per Q8, or the Atlas module path once B1 is resolved) to the §6.2 interface, plus the `tests/`-run results. `lab-FI1-project-3` is the rung-3 sanity run on the reference instance.
4. **Rung 4, stretch** (optional, not graded): a curve-fitting comparison on the student's own bring-your-own-data CSV (BUILDER_RULES §6.6 BYOD mode; the file never leaves the browser), with a stated hypothesis.

### 6.2 Spec (`dl.spec`; `check_projects.py` lines 34 and 38-49)

Terms: Context (2-4 sentences), Inputs, Required outputs, Constraints, Grading. **Grading entry names both the words "autograder" as the only mode**: the curriculum says `autograder` (`curriculum/03-markets.yaml:55`), so the spec says "Grading: autograder" and does not mention a rubric (no rubric; `check_projects.py` lines 58-73 do not apply).

- **Context.** A desk needs one curve engine that turns par bond quotes into zero rates and fits smooth models. The question: do the fitted curves reprice the input bonds, and how well do the parametric models recover a known curve?
- **Inputs.** SIMULATED instances from `make_instance(seed)` (§6.3). No real data in the autograder (B3 aside).
- **Required outputs** (proposed interface, frozen by the architect before building; Q3):
  - `day_count_fraction(start: date, end: date, convention: str) -> Fraction`. Conventions: `"ACT/360"`, `"ACT/365"`, `"30/360"`. The 30/360 variant is stated in the spec by its rule, not by a source (B1-adjacent: no registry source; REFERENCE_REQUESTS R4). Raises `ValueError` for an unknown convention or `end < start`.
  - `price_from_yield(face_cents: int, coupon_rate: Fraction, periods: int, yield_per_period: Fraction) -> int`. Integer coupon periods; returns the dirty price in cents, rounded once, half up. Raises `ValueError` if `periods < 1` or `yield_per_period <= -1`.
  - `yield_to_maturity(dirty_cents: int, face_cents: int, coupon_rate: Fraction, periods: int) -> Fraction`, to a stated tolerance, by bisection. Raises `ValueError` for a price that no yield above -1 can produce.
  - `bootstrap_zero_rates(par_bonds: list[dict[str, object]]) -> dict[int, Fraction]` (maturity in periods to zero rate).
  - `ns_yield(tau: Fraction, beta0: Fraction, beta1: Fraction, beta2: Fraction, lam: Fraction) -> Fraction` and `svensson_yield(...)` with the extra beta3 and tau2 (exact parameter names frozen with the contract). Raises `ValueError` for `tau <= 0` or `lam <= 0`.
  - `fit_nelson_siegel(maturities: list[Fraction], yields: list[Fraction]) -> dict[str, Fraction]` (NumPy-free output type; the engine may use NumPy internally).
- **Constraints.** Integer cents for every money output, one half-up rounding, stated in the module docstring and on the page. Standard library plus NumPy only (§5.5). No network. The same code runs in Pyodide and under pytest.
- **Grading.** Autograder: `grader/test_project.py`, dual-mode, on seeds 0-49.
- **Reading list** (`ol.reading-list`): `nelson1987parsimonious`, `svensson1994estimating`, `gurkaynak2007us`. Each `data-cite` names only a key in §0.

### 6.3 Grader design (Builder E, after B1)

Files, under `course/modules/FI/FI1/grader/`: `instance.py`, `reference.py` (excluded from deployment, BLUEPRINT §7), `starter.py`, `test_project.py`. The grader panel on `project.html`: `<section class="grader-panel" id="grader" data-unit="FI1" data-grader="grader/" data-suite="test_project.py" data-support="instance.py" data-solution="curve_engine.py" data-starter="starter.py" data-packages="numpy">` (solution path changes to the Atlas path if B1 says so).

- **`instance.py`**: `make_instance(seed: int) -> dict[str, object]`. Deterministic per seed. Generates a SIMULATED par-bond set (coupon, maturity in whole periods, price), a generating Svensson parameter set, and the nominal and convention choices. Labelled SIMULATED in its docstring. Valid by construction: positive maturities, yields above -1, `lam > 0`, `tau2 > 0`. Seeds 0-49 must give materially different curves; the verifier samples 20 seeds.
- **`reference.py`**: the full solution. Passes every test on seeds 0-49 (`run_graders.py --unit FI1 --seeds 0-49`). Uses only Fraction and NumPy.
- **`starter.py`**: `raise NotImplementedError` stubs. The suite must fail on it (`run_graders.py` checks this, line 162-168).
- **`test_project.py`** (properties and numbers, no hard-coded answers; each test recomputes its expected value from the instance's generating parameters by an oracle written separately from `reference.py`):
  - the price from yield matches the closed-form annuity-plus-principal expression to the cent, after the stated rounding;
  - dirty price equals clean price plus accrued interest on each instance, and the accrued interest matches the day count fraction;
  - `day_count_fraction` returns the stated values for each convention on fixed date pairs; `ACT/360` and `ACT/365` differ by the ratio 365/360 for the same actual days;
  - YTM: the price at the solved yield reprices to the input within the stated tolerance, and price is strictly decreasing in yield (Assumption 1);
  - bootstrap: every input par bond reprices to the input within tolerance;
  - Nelson–Siegel and Svensson: parameter recovery on the generating curve within a stated tolerance; the nested check (`beta3 = 0`) reproduces the NS fit;
  - DV01 and duration against the finite difference of price on the instance, to the stated step tolerance;
  - published GSW parameters: **honest-pending** (B3), a test marked skipped with a named reason that the page shows;
  - invalid input raises `ValueError` naming the violated condition for each named case in §6.4; failure messages name the property and hint at the concept. They never print the answer.
- **Dual mode**: the same suite runs in Pyodide and under pytest; each test under 5 s in Pyodide; the suite under 60 s.

### 6.4 Exception table (grader tests demand these, and only these)

| Condition the page names | Exception | Message must name |
|---|---|---|
| unknown day-count convention | `ValueError` | the allowed convention names |
| `end < start` in `day_count_fraction` | `ValueError` | the date order |
| `periods < 1` or `yield_per_period <= -1` in `price_from_yield` | `ValueError` | the violated condition |
| `tau <= 0` or `lam <= 0` in `ns_yield` / `svensson_yield` | `ValueError` | the violated condition |

Any other invalid input may raise any exception or return; the tests do not require a type for it.

### 6.5 Mutants (ten student errors; Builder E writes them, the verifier kills them)

Written by the verifier as complete modules in `ledgers/FI1/mutants/<name>.py`, each docstring's first line naming the error. Planner's list of twelve plausible student errors; items 1-10 are the required ten (Q9), items 11-12 are spares that replace any of 1-10 that the verifier finds equivalent or not killable:

1. Day count ACT/360 used where ACT/365 is specified (the 365/360 error).
2. Accrued interest added to the clean price in the wrong direction (dirty price below clean).
3. Clean price reported as dirty (accrued interest omitted).
4. YTM by bisection that returns the first sign change and ignores the compounding frequency (annual used for semi-annual).
5. Forward rate from simple rather than compound spot rates (the wrong compounding convention).
6. Bootstrapping that discounts each coupon at the par yield, not the zero rate.
7. Nelson–Siegel decay parameter used as `tau` (the scaling error in `lam`).
8. Svensson built without the second hump term (`beta3` dropped).
9. Modified duration without dividing by `1 + y/m`.
10. DV01 with the wrong sign, or reported per 100 of face, not per unit of face.
11. A hard-coded answer for seed 0.
12. Truncation instead of half-up rounding (breaks the cent-exact checks on seeds where the fraction is `.5`).

Ten mutants are the minimum; a mutant that is equivalent on every input must be proven so and dropped, not counted (VERIFIER §2.6).

### 6.6 Five alternative correct implementations (test-only fixtures)

The verifier writes five correct implementations in a scratch checkout and runs the suite on each: (1) closed form, (2) Newton iteration for YTM with bisection as the stop condition, (3) a `Fraction`-throughout version, (4) a float version with the same half-up rounding applied to the exact value, (5) a NumPy linear-solve version for the fit. All five must pass; scripts are archived under `ledgers/FI1/scripts/`.

### 6.7 Time budget (`<table id="hours">`, sums to 18 h)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1 worked example (read and annotate) | 1 | One solved SIMULATED bond, annotated line by line |
| Rung 2 completion problem | 2 | Fill the accrued-interest and DV01 lines, then run the instant check |
| `day_count_fraction`, `price_from_yield`, dirty and clean price | 4 | Exact arithmetic and the cent rounding rule |
| `yield_to_maturity` and `bootstrap_zero_rates` | 3 | Bisection and repricing checks |
| `ns_yield`, `svensson_yield`, `fit_nelson_siegel` | 5 | Grid over the decay parameter and linear least squares |
| Edge cases, invalid-input checks, local pytest runs on your seed | 2 | The §6.4 table |
| Setup, reading the spec, running the starter | 1 | Starter must fail the suite first |
| **Total** | **18** | Equals `data-hours-project` on the hub |

No rubric memo, no exemplars, no self-assessment (grading `autograder` only).

---

## 7. Cards builder (Builder F, after A-E)

- `course/modules/FI/FI1/cards.json`, ids `FI1-c001` upward, `lesson` in L01-L08 (each lesson at least one card).
- One card per definition, key formula, key result and misconception (BUILDER_RULES §7).
- Grade T for every derived formula, with `"basis"` naming the lab or problem that establishes a numerical result, for example `"basis": "Lab 4, Problem 2 (exact)"`.
- Cite a registry key only for an empirical or attributed claim: L06 and L07 may cite `nelson1987parsimonious` and `svensson1994estimating` only for the model's source attribution, with a locator the builder has read; L08 may cite `gurkaynak2007us` for the GSW method. Otherwise `cite` is `[]`.
- Working-paper grading: `svensson1994estimating` is at most grade C with its version date.
- `check_pages.py` checks the unit prefix, the lesson existence, the grades and the registry keys (`check_cards`, lines 366-398).

---

## 8. Registry keys the module may cite

| Key | Status | Use in FI1 |
|---|---|---|
| `nelson1987parsimonious` | verified; matches the curriculum string (§0) | L06 model attribution; reading list |
| `svensson1994estimating` | verified; WP type; title spacing differs from the curriculum string (flag F1) | L07 model attribution; grade C max; version date required |
| `gurkaynak2007us` | verified; matches the curriculum string | L08 GSW curve method; reading list |

Keys not for FI1, though they exist: `vasicek1977equilibrium`, `cox1985theory`, `heath1992bond`, `dai2000specification`, `adrian2013pricing`, `cochrane2005bond`, `bauer2017robust` (all owned by FI2 or FI3 scope; `used_by` names those modules). The registry and `used_by` fields are not changed by this plan.

### 8.1 REFERENCE_REQUESTS (topics only, no bibliographic data from memory)

- R1. A source for the day-count conventions ACT/360, ACT/365 and the 30/360 variant (the authority that defines them; the curriculum names none). Needed for L02 and §6.2. Confidence: the convention exists; the authority's identity is unverified.
- R2. A fixed-income textbook or a Treasury methodology document for bond price, duration and convexity definitions. The curriculum names no textbook for FI1 (`curriculum/03-markets.yaml:44-47`). Needed for L01, L04 definitions if the builder wants an attribution. Otherwise the definitions are derivations (grade T).
- R3. A source for the Treasury or Federal Reserve description of the constant-maturity yield, to say what the H.15 series are (needed for L06 data, B2).
- R4. A source for the 30/360 variant rule as used in the spec (R1 covers it; list it separately only if R1 is not admitted).

The architect resolves these through `tools/add_reference.py` (by DOI, ISBN, or an allow-listed issuer page). The lessons may teach the definitions as derivations with no historical attribution (recommended; Q2).

---

## 9. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

```bash
.venv/bin/python tools/check_pages.py --unit FI1            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit FI1
.venv/bin/python tools/check_projects.py --unit FI1          # fails until atlas/A5.contract.md exists (B1)
.venv/bin/python tools/run_labs.py --unit FI1               # --page L06 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/FI/FI1/L01.html        # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/FI/FI1/L06.html --refresh lab-FI1-L06-1   # after editing a twin
.venv/bin/python tools/run_graders.py --unit FI1 --seeds 0-49               # after B1 and the grader exists
.venv/bin/python tools/mutate_graders.py --unit FI1 --seeds 0-9             # verifier only
.venv/bin/python tools/verify_refs.py --unit FI1                            # verifier only
.venv/bin/ruff check tests/labs/FI1 course/modules/FI/FI1/grader && .venv/bin/ruff format --check tests/labs/FI1
.venv/bin/mypy tests/labs/FI1 course/modules/FI/FI1/grader                 # strict; confirm the configured paths first
.venv/bin/python -m pytest tests/labs/FI1                                   # the twins' own tests, if the builder writes any
```

Notes (flags checked by the planner):
- `check_pages`, `check_dag` and `check_projects` accept `--unit`; `run_labs.py` accepts `--unit`, `--all`, `--page` (`tools/run_labs.py` lines 119-121); `run_graders.py` accepts `--unit` and `--seeds` (lines 129-131); `mutate_graders.py` accepts `--unit` and `--seeds` (lines 30-32); `embed_labs.py` takes pages and `--refresh [LAB_ID ...]`. The planner did not execute these commands against FI1 (FI1 is not built).
- `page_smoke.py` is not run by builders (timing-sensitive; verifiers run it on a quiet machine).
- Repo-wide gates (`check_pages.py --all`, `check_dag.py --all`, `build_site.py --check`, `render_curriculum.py`, `fetch_data.py --check`) are the architect's, once, before merge. Not per builder.
- `fetch_data.py --check` runs only if a DATA_REQUEST is approved and a snapshot is added.

---

## 10. Tooling assumptions that do not hold for FI1 (flagged)

1. **Atlas contract missing (B1).** `check_projects.py` lines 144-146 fail the project. No `atlas/A5.contract.md` exists.
2. **Atlas cumulative suite cannot run (non-blocking).** A1-A4 modules (CS1, CS3, S0, S4) are not built.
3. **M2 is not built.** The hub links M2 concepts through `concepts.html` anchors, not an M2 page. `check_dag.py` checks the curriculum closure, so it does not need M2's page, but the links resolve only once `concepts.html` is generated.
4. **Only one embedded curve, with two maturities (B2).** The lab "Fit Nelson–Siegel to an embedded curve" cannot run on the embedded data as it stands.
5. **No textbook source.** The curriculum names none (`curriculum/03-markets.yaml:44-47`), so bond-math definitions are derivations or unattributed definitions (R2).
6. **Working paper (Svensson).** `[WP]` (`curriculum/03-markets.yaml:46`): grade C at most, with its version date. Freshness check by the verifier (VERIFIER §2.1).
7. **`run_graders.py` imports NumPy at module level** (line 35). NumPy is therefore present in the local gate. Whether Pyodide's package list accepts `numpy` for this grader is **UNREAD** by the planner (`data-packages`). Assumed to work because AC2's grader panel uses it.
8. **`check_pages.py` bans the three-dot ellipsis on all visible text** (line 73). Python `...` in a visible code block fails the check. The starter uses `raise NotImplementedError`.
9. **Python code blocks must be labs or checked snippets** (`check_code`, `check_pages.py` lines 145-160). Unlabelled Python code fails.
10. **Lab count.** The curriculum names one lab (`curriculum/03-markets.yaml:48`); the plan adds one per lesson (M1 Q2 precedent).

---

## 11. Notation (`notation/notation.json`) and foreseen conflicts

Registered symbols and macros that FI1 must not reuse with another meaning:

| Registered | Meaning (registry) | Conflict risk in FI1 | Rule |
|---|---|---|---|
| `T` (`notation/notation.json:112`) | number of observations in a sample (S1) | Maturities are conventionally written `T` | **Use `\tau` for maturity** (the Nelson–Siegel convention). Never write `T` for a maturity or a time. |
| `R_f` (`notation/notation.json:142`) | gross riskless return, reciprocal of a sure payoff's price (AP1) | Gross versus net, and "the risk-free rate" as a spot yield | Do not use `R_f` for a spot or a yield. Use `s(\tau)` for a spot rate and `f` for a forward. |
| `\Phi, \Phi^{-1}` (`:117`) | standard normal CDF and quantile | Not expected in FI1 | Do not use `\Phi` for anything else. |
| `\gamma_3`, `\gamma_4` (registered) | skewness, kurtosis | Not expected in FI1 | Do not use `\gamma` subscripted for any other quantity. |
| `\mathbb{Q}` | risk-neutral measure (AP1) | "Q" used for a quantity in an exchange-style notation | Not used in FI1. Quantities are not named Q. |
| `\E`, `\Prob`, `\Var`, `\Cov`, `\se` (macros) | expectation, probability, variance, covariance, standard error | Fine; the macros are the only notation for these | Use the macros, not `\mathbb{E}` typed directly. |
| `\R`, `\N` (macros) | real and natural numbers | Fine | Use `\R` for the real numbers. |

Local letters (`notation.json` `about`: alpha, beta, gamma, N, S, m, mu, sigma are defined per lesson): `beta_0..beta_3`,
`lambda`, `tau_1, tau_2` (Svensson) are local and must be defined in the lesson where first used. `m` for compounding
frequency is local (`about` lists it as local) and is defined per lesson. `r` is used in M1 for a compounding rate in
`(1 + r/m)^m`. FI1 uses `y` for yield to maturity and `r` only where M1's meaning is carried over, stated on the page. The
planner foresees this conflict and recommends `y` throughout FI1.

Notation requests (NOTATION_REQUESTS, for the builder to report if needed): none foreseen beyond the letters above.

---

## 12. Open questions for the architect (numbered)

1. **B1 (Atlas contract).** Draft `atlas/A5.contract.md`, or accept a module-local `curve_engine.py` with no Atlas link. The second option needs the curriculum's "Atlas A5" wording changed, which the planner does not propose. Blocking for the project only.
2. **B2 (embedded curve for the curriculum lab).** Approve DATA_REQUEST 1 (H.15 constant-maturity snapshot; series identifiers read from the release zip; licence quote confirmed) or accept the SIMULATED fallback for L06 with an honest-pending note. Planner recommends the fallback now and the request in parallel.
3. **Signatures (freeze).** Approve the §6.2 interface and the §6.4 exception table, or name changes, before builders start (E1 Q4, AC4 Q7 precedent).
4. **Hours split.** 8 × 9 h lessons and an 18 h project (Q4 alternative: 7 lessons, merging L06 and L07). Confirm.
5. **Figures.** No figures (recommended), or approve two figures with JS kernels and tests (BUILDER_RULES §6.4).
6. **DAG defects.** Accept the plain-prose resolutions in §4 (least squares, root finding, expectations hypothesis), or add S2 as a prerequisite (a curriculum change; not proposed).
7. **Pyodide packages.** Confirm `numpy` as the only third-party package for FI1 (no SciPy), and confirm the Pyodide runner accepts `data-packages="numpy"`.
8. **Solution file name and path.** Propose `curve_engine.py` (unit-local), or the Atlas path once B1 is resolved.
9. **Mutant count.** Ten mutants (orchestrator request) from the twelve listed in §6.5, or all twelve.
10. **Money.** Integer cents for every amount of money, one half-up rounding, with quoted prices and yields as `Fraction` or float with a stated tolerance (E1 Q6 precedent). Confirm.
11. **Registry gaps.** Approve REFERENCE_REQUESTS R1-R3 as topics for `tools/add_reference.py`, or have the lessons teach conventions and definitions as derivations with no attribution.
12. **GSW parameters (B3).** Supply the DATA_REQUEST with the published-parameter source and its licence quote, or accept the honest-pending test. The planner did not verify any GSW parameter file (**UNREAD**).
13. **Svensson title flag (F1).** Confirm that the registry record's title spacing ("1992 - 1994") is an acceptable match to the curriculum string ("1992-1994"), or correct it through `add_reference.py` (the CF1 Q3 precedent applies: cite only keys whose record matches).

---

## 13. After the builders

1. Orchestrator integrates; runs the §9 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02, L03-L04, L05-L06, L07-L08, project (after B1). The project verifier writes the ten mutants and the five alternative implementations (§6.5, §6.6). Failing rows return to the owning builder, with only the failing rows.
3. Ledger at `ledgers/FI1.verification.json`; per-round mutants under `ledgers/FI1/mutants/`; verifier scripts under `ledgers/FI1/scripts/` (VERIFIER §3).
4. The branch is merged only when the unit ledger is PASS or its remaining gaps are named and agreed. The Atlas-cumulative gap and the honest-pending GSW test are named gaps if they remain.

Architect decisions: pending (§12). This plan is the planner's proposal.
