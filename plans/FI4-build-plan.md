# FI4 build plan: Money Markets & Plumbing (2026-11-09)

Unit: **FI4 · Money Markets & Plumbing** · tier U · 60 h · prerequisites FI1, E5 · no debate key · no Atlas milestone ·
grading `both` (autograder for the monitor, rubric for the memo) · output directory `course/modules/FI/FI4/` (part code `FI`) ·
lab twins `tests/labs/FI4/`.

Planner: Haiku, plan only. No lesson content, no git operations, no commits. Executors: Haiku builders A to E (and F for cards),
then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every curriculum fact carries a `file:line` locator read during planning. Facts about the registry carry a
`references.json` key. Anything not in the curriculum or the registry is marked **NOT IN CURRICULUM** or **NOT READ**.
Tool facts were checked by running `tools/coursekit.py` (`prerequisite_closure`, `concept_owner`, `unit`, `built_units`) through
`/Users/billyribeiro/dev/quant-phd/.venv/bin/python` with read-only calls. No file was written except this plan.

**Status: BLOCKING ISSUES EXIST (§0.3). The hours are feasible. No redistributable money-market data source is established, so the
curriculum lab and the project's market inputs run on SIMULATED or bring-your-own-data (BYOD) inputs unless the architect approves
a source (B1). The architect must decide B1 and the DAG questions in §4 before the builders start.**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part FI, code `FI`, title "Fixed Income & Rates", studio STUDIO-FI (requires FI1, FI3) | `curriculum/03-markets.yaml:1-9` |
| FI4 entry begins: id, title "Money Markets & Plumbing" | `curriculum/03-markets.yaml:121-122` |
| Tier `U`, hours `60`, prereqs `[FI1, E5]` | `curriculum/03-markets.yaml:123-125` |
| Core: "Repo, SOFR, reserves and the Fed balance sheet, the Treasury basis trade, dealer balance-sheet constraints, the SLR, the March 2020 dash for cash." | `curriculum/03-markets.yaml:126-128` |
| `introduces` has 10 concepts: repurchase-agreement, repo-haircut, sofr, bank-reserves, central-bank-balance-sheet, treasury-basis-trade, dealer-balance-sheet-constraint, supplementary-leverage-ratio, swap-spread, dash-for-cash | `curriculum/03-markets.yaml:129-139` |
| Sources: "He, Nagel & Song (2022), JFE 143(1)"; "Federal Reserve H.4.1 release (primary)"; "Federal Reserve Bank of New York SOFR methodology (primary)" | `curriculum/03-markets.yaml:140-143` |
| Lab: "Basis-trade P&L with haircut and margin." | `curriculum/03-markets.yaml:144` |
| Project "Plumbing monitor"; brief: "Track reserves, the reverse-repo facility, TGA, repo spreads and swap spreads from public data, and write a mechanism-level explanation of one stress episode."; deliverable "Monitor plus memo."; grading `both` | `curriculum/03-markets.yaml:145-152` (title 146, brief 147-150, deliverable 151, grading 152) |
| No `debate:` key on FI4 (contrast FI3 which has one) | `curriculum/03-markets.yaml:121-152` (absent); FI3 debate at `:120` |
| No `atlas:` key on the FI4 project (contrast FI1 `atlas: A5` at `:56` and FI3 `atlas: A13` at `:119`). The brief does not name Atlas. | `curriculum/03-markets.yaml:145-152` |
| JSON row for FI4 matches the YAML (hours 60, prereqs FI1 and E5, 10 concepts, lab, grading both, part FI) | `coursekit.unit('FI4')` output, read by the planner; `curriculum/curriculum.json` module array (FI4 row) |
| FI4 is referenced by the bachelor's credential requirement list and by a course map | `curriculum/meta.yaml:63` (credential requires list), `:79` (course "Financial Markets & Institutions", modules [FC1, BK1, FI4, BK4]) |
| SR4 requires FI4 (`prereqs: [SR1, FI4, LX2]`) | `curriculum/05-macro-alternatives.yaml:509` |
| Prerequisite closure of FI4 (`coursekit.prerequisite_closure('FI4')`): **{AC1, CF1, E1, E5, FI1, M1, M2, P0.1}** (8 modules). Usable concepts in the closure: 102 (13+13+10+13+12+11+14+16 from the modules' `introduces` lists) | planner run of `tools/coursekit.py` |
| Position of FI4 in the topological order: index 33 (0-based). Positions used in §4: FC1 26, E5 25, FC2 30, BK1 31, BK4 32, LX1 36, E8 41, SR1 49, SR4 73, CR2 99 | `curriculum/curriculum.json` `topological_order`, read through `coursekit.curriculum()` |
| Built status (coursekit `built_units`): E5, FC1, FC2, BK4, LX1, E1, M1 to M7, AC1, CF1, CF8 and others are built. **FI1 is NOT built** (no `course/modules/FI/`), **BK1 and SR1 are NOT built**. | `coursekit.built_units()`; `course/modules/` listing |
| FI4 concepts' owners in the concept map: all 10 are owned by FI4 (no double definition) | `coursekit.concept_owner()` over `curriculum/curriculum.json` `concepts` |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 60 h (`curriculum/03-markets.yaml:124`). Tool rules (as E5, `tools/check_pages.py`): lesson `data-hours` 6 to 12;
hub `data-hours-lessons + data-hours-project = 60`; project share 10 to 40% of 60, i.e. 6 to 24 h; lesson sum equals the hub figure.

Chosen split: **5 lessons × 8 h = 40 h; project 20 h (33.3%)**. 40 + 20 = 60. Feasible. No STOP condition on hours.
Ten concepts over five lessons gives exactly two concepts per lesson (§1), which is the natural grain of the curriculum's `core` list.

### 0.3 Blocking issues (architect decision required before builders start)

**B1. No redistributable money-market data is established. The lab and project data need a decision.**
- The core names repo, SOFR, reserves, Fed balance sheet and swap spreads (`curriculum/03-markets.yaml:126-128`). The project brief
  needs reserves, the reverse-repo facility, TGA, repo spreads and swap spreads "from public data" (`:147-150`). The lab is
  "Basis-trade P&L with haircut and margin" (`:144`), with no data named.
- Embedded snapshots today are `fx_daily`, `fx_monthly` and `ust_daily` only (`tools/data_sources.yaml`, datasets section; `course/assets/data/market/MANIFEST.json`).
  `ust_daily` carries `tbill_3m` and `cmt_10y` (H.15). It has no repo rate, reserves, RRP, TGA, SOFR or swap rate.
- `tools/data_sources.yaml:119` `rejected:` lists only the French library and Open Source Asset Pricing. Nothing else is listed.
- **Federal Reserve H.4.1 (`frbndfederal`, candidate):** the H.4.1 release page (`https://www.federalreserve.gov/releases/h41/`)
  offers an XML zip, `FRB_h41_xml.zip` (planner WebFetch on 2026-11-09; a summary, not a file locator, so the verifier must re-read it).
  The same page states no copying or redistribution terms and links to a "Website Policies" page, which the planner did **not** read.
  The Board's disclaimer (`https://www.federalreserve.gov/disclaimer.htm`, planner WebFetch 2026-11-09) states: "Unless otherwise
  indicated, information on Board's website is in the public domain" and "may be copied and distributed without permission", with
  "Please cite to the Board as the source of the information." The same disclaimer is the grant used for `fx_daily` (`tools/data_sources.yaml`
  `licence_url`). **H.4.1 is therefore a candidate under the Board's site-wide grant, not a cleared source.** It needs the Website Policies
  page read and quoted, a `tools/data_sources.yaml` entry, a MANIFEST snapshot and the architect's approval (BUILDER_RULES §6.6 steps 1-5).
- **NY Fed SOFR (`frbnyndadditional`):** the reference-rate page (`https://www.newyorkfed.org/markets/reference-rates/additional-information-about-reference-rates`,
  planner WebFetch 2026-11-09) has **no** redistribution or licence sentence for SOFR data. It shows only a site-wide "Terms of Use and Privacy
  Statement" link. **Not cleared.** The NY Fed Terms of Use page was not read (NOT READ).
- **Plan's default (for the architect to confirm or replace):** (a) the curriculum lab L05 and the chapter labs run on a generated
  economy of repo, haircut, reserve and swap-rate paths, labelled **SIMULATED** (BUILDER_RULES §1.7), with an honest-pending note that
  the curriculum's "embedded" intent for H.4.1 and SOFR is not met; (b) the project takes reserves, RRP, TGA, repo rates and swap rates in
  **bring-your-own-data** mode (BUILDER_RULES §6.6, last bullet: the page documents the schema and validates a CSV that never leaves the browser);
  (c) `ust_daily` (`cmt_10y`, `tbill_3m`) is used only for the Treasury yield leg of the swap spread, with the basis caveat (§5.2 input 5);
  (d) a DATA_REQUEST is raised for H.4.1 (with the Website Policies quote) and for a SOFR licence (with the NY Fed Terms of Use quote).

**B2. No Atlas issue.** The FI4 brief does not name Atlas (`curriculum/03-markets.yaml:147-150`) and the project has no `atlas:` key
(`:145-152`). No contract is needed. Unlike E5 (B2 there), no curriculum edit is needed. Recorded so the verifier does not expect one.

**B3. Registry records for the three curriculum sources.** The curriculum strings map to registry keys as follows (see §7.1):
- "He, Nagel & Song (2022), JFE 143(1)" → `he2022treasury` (Crossref-verified; authors He, Nagel, Song; JFE 143(1); `used_by` already lists FI4).
- "Federal Reserve H.4.1 release (primary)" → `frbndfederal` (issuer-verified, URL `https://www.federalreserve.gov/releases/h41/`; the record has no year).
- "Federal Reserve Bank of New York SOFR methodology (primary)" → `frbnyndadditional`. **Flag:** the record title is "Additional Information about Reference Rates Administered by the New York Fed", and the registry's own `title_recall` note gives 0.71 against the curriculum string. The planner's WebFetch shows the SOFR calculation is described in a section titled "Calculation Methodology for the TGCR, BGCR, and SOFR" on that same page. Whether the record is the right document must be confirmed by the verifier, who reads the section. The architect decides whether to correct the curriculum string.

**B4. Two-sided treatment without a debate key.** FI4 has no `debate:` key (`curriculum/03-markets.yaml:121-152`), so no debate brief is required
(BUILDER_RULES §4.2 item 5 applies only when the curriculum entry has a debate). The basis trade and the dash for cash are contested in the
literature, so the two-sided rule (BUILDER_RULES §2.5) applies to every B- or C-graded claim anyway. See §12 Q12.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

Five lessons × 8 h = 40 h; project 20 h; total 60 h. Concept counts per row sum to 2+2+2+2+2 = 10, each concept in exactly one row
(`curriculum/03-markets.yaml:129-139`).

| Lesson | Title (working) | Concepts it defines (`introduces`) | Lab (twin id, `tests/labs/FI4/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Repurchase agreements and haircuts | `repurchase-agreement`, `repo-haircut` | `lab-FI4-L01-1`: repo cash due on the day-count basis of FI1 (`day-count-convention`, `curriculum/03-markets.yaml:31`); haircut sizing in integer cents; SIMULATED inputs | 8 | Builder A |
| L02 | SOFR and bank reserves | `sofr`, `bank-reserves` | `lab-FI4-L02-1`: reserves as a balance-sheet line (liability side) on a SIMULATED path; the reserve identity checked exactly | 8 | Builder B |
| L03 | The central-bank balance sheet and dealer constraints | `central-bank-balance-sheet`, `dealer-balance-sheet-constraint` | `lab-FI4-L03-1`: the liability identity (currency + reserves + reverse repo + TGA + other) checked exactly on a SIMULATED table; dealer funding capacity as a ratio of balance-sheet capacity | 8 | Builder B |
| L04 | The supplementary leverage ratio and swap spreads | `supplementary-leverage-ratio`, `swap-spread` | `lab-FI4-L04-1`: the SLR and the swap spread computed in `Fraction`; the sign convention of the spread checked against a worked case | 8 | Builder C |
| L05 | The Treasury basis trade and the dash for cash | `treasury-basis-trade`, `dash-for-cash` | `lab-FI4-L05-1` (**the curriculum lab**, `curriculum/03-markets.yaml:144`, SIMULATED): basis-trade P&L with haircut and margin, integer cents, the margin call from a price move computed exactly | 8 | Builder D |
| index | Hub: objectives, prerequisites (FI1, E5), placement, lesson map, ladder, hours split 40/20 | none | none | - | Builder A |
| project | Plumbing monitor (`both`, §5) | none | `lab-FI4-project-1` (rung 1, SIMULATED), `lab-FI4-project-2` (rung 2, `class="lab completion"`), `lab-FI4-project-3` (rung 3 check) | 20 | Builder E |
| grader | `grader/instance.py`, `reference.py`, `test_project.py`, `starter.py`; `ledgers/FI4/mutants/` (10) and `ledgers/FI4/alternatives/` (5) | none | none | - | Builder E |
| cards | `cards.json` from L01 to L05 | none | none | - | Builder F (after A to E) |

**Assignment deviation (recorded).** The brief asks for "about three lessons per builder". A 60 h unit has five lessons, so five lesson
builders with one lesson each is the closest fit, with Builder A also owning the hub and Builder B taking two lessons (L02, L03) because
they share the reserve identity and the same SIMULATED path generator. Builder E owns project, grader and project labs, as the brief requires.

Ownership rule: each builder writes only its own lesson files and twins. Builder A writes the hub after L01 and L02 exist. Builder E writes the project,
its rubric and exemplars, and the grader. The project does not depend on lesson prose; it depends on the function API in §5.4, which is fixed here.

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses, §7):
- L01 uses only FI1 (`day-count-convention`, `dv01` not needed) and M1 (`present-value`, `discount-factor`) concepts, plus E5 `policy-rate` only in prose.
- L02 uses L01 (`repurchase-agreement`, `repo-haircut`) and FI1 `yield-conventions` in prose.
- L03 uses L02 (`bank-reserves`, `sofr` for the overnight rate in prose).
- L04 uses L03 (`dealer-balance-sheet-constraint`) in prose only, and FI1 `yield-to-maturity`/`term-spread` for the Treasury leg.
- L05 uses L01 (`repo-haircut`), L02 (`bank-reserves`), L04 (`swap-spread`) and FI1 `duration`/`dv01` for the basis-trade risk.

Hours check: 5 × 8 = 40 (hub `data-hours-lessons="40"`); project 20 (hub `data-hours-project="20"`); 60 total.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to FI4)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3 to §8, `plans/E5-build-plan.md` (its architect decisions section is binding precedent),
this file. Study `course/modules/E/E5/` for the hub, lesson and project grammar, and `course/templates/` for the skeletons.
FI1 is NOT built, so `course/modules/FI/FI1/` does not exist. The FI4 hub must not link an FI1 page. Prerequisite links go to `concepts.html` anchors only.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`, integer cents) and rounded only at display.
   Rounding rule stated on the page: money is rounded half-up to whole cents from the exact `Fraction` value (floor of the exact value plus one half;
   see §5.4). Precedent: E5 §2.1 item 1; E3 rulings 27 and 32.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only what the printed numbers show.
3. **Attribute nothing unread.** Only registry keys listed in §7.1 may be cited, and only at paper level unless the builder has read the abstract or the page
   (VERIFIER §2.1). No page, table, equation, coefficient, date or SOFR-methodology detail is typed from memory. Facts about how SOFR, reserves or the SLR are
   computed are derivations on the page or are cited to a read locator. Otherwise they are NOT STATED or removed. Precedent: E5 §2.1 item 3; fixer-rules
   "attribute nothing you have not read".
4. **Scope words need a computation.** "every", "all", "never", "always", "any", "market", "money markets", "dealers", "the Fed" are used only where a
   computation, a finite check or a derivation supports them. Scope of FI4 (confirm, §12 Q7): US dollar money markets in the static one-period setting of each
   computation; repo as a secured one-period loan; SLR as a ratio from the page's formula; the basis trade as a one-period position; the dash for cash as a
   described episode with the lessons' own model limits. No multi-currency content (E8 owns it), no CCP default waterfall (BK4), no formal Basel capital theory (BK1).
5. **Define before use.** Each of the 10 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned lesson, and never before it.
   Terms outside the 10 (the overnight rate, reverse repo, the Treasury general account (TGA), margin, the discount, the day-count basis as a term already in FI1,
   balance-sheet capacity, cash-futures basis, central counterparty, collateral) are defined in prose at first use with a plain `<dfn>` and no `data-concept`
   (`tools/check_dag.py` skips a `<dfn>` without `data-concept`).
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation block lists its numbered Assumptions (A1, A2, ...) before the statement. Examples
   the builders must state: the repo cash-due formula needs a fixed rate, a fixed haircut in [0, 1) and a day count with a stated basis; the SLR needs a
   positive denominator; the swap spread needs both rates on the same maturity and the same compounding convention, stated as an assumption.
7. **Grader rule.** Applies to Builder E only (autograder): every rule of §5.3 and the ruling 19 set (every stated condition isolated and tested in both directions,
   ten student-error mutants, five alternatives, collect-only count on the page).
8. **Money.** Every amount is an integer number of cents in the twins, the grader and the BYOD validator (BUILDER_RULES core guardrails: money = integer, `*_cents`
   value in `int`; no float money). Rates are `Fraction`, shown in percent per year or basis points with the basis stated. Lab output of money is printed in cents.
   Where a money total is shown in dollars, the page states the conversion (1 dollar = 100 cents).
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own container. `page_smoke.py` is the verifier's check.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":` guard.
    `run_labs.py` runs each twin as `python -I -W error <twin>` with no network. The E5 twin `tests/labs/E5/lab-E5-L01-1.py` is the model.
11. **Rate and yield statements are basis-explicit.** Every rate states its unit (percent per year or decimal), compounding and day-count basis, and its source
    (`ust_daily` note for `tbill_3m`, which is a discount-basis series per `tools/data_sources.yaml` `ust_daily.note`).
12. **Haircut and margin conventions are defined on the page, not assumed.** The day-count basis for repo cash due is stated as a **convention of this unit**
    (actual days over a 360-day year, written as the convention, not as a fact about any market), and the twin computes with that convention. No claim
    that a particular market uses it is made unless read (§2.1 item 3).

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. A B- or C-graded claim names its published
  counter-evidence (BUILDER_RULES §2.5). **The registry holds no basis-trade, dash-for-cash or SOFR-computation record that this plan has read.** Those
  claims are derivations (grade T, conditional on the stated model), or are graded C with the basis named, or go to `REFERENCE_REQUESTS` (§7.2).
- Concepts: §1 table; `<dfn>` only for the 10 registered concepts plus plain `<dfn>` for other terms. No `<a class="concept">` for any concept outside
  the prerequisite closure {AC1, CF1, E1, E5, FI1, M1, M2, P0.1} (§4, DAG).
- Prerequisite links: `href="../../../concepts.html#<id>"` for concepts owned by closure modules; `href="Lnn.html#def-<id>"` for earlier FI4 lessons.
  A lesson never links a concept defined in a later lesson.
- Labs: code lives once in `tests/labs/FI4/lab-FI4-Lnn-1.py` (and `lab-FI4-project-1..3.py`). The page carries `@@LAB:<file>@@` and `@@OUT:<file>@@`;
  `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-FI4-<page>-<n>` (`check_pages.py` `check_lesson`). Standard library only
  (`fractions`, `math`, `random.Random(seed)`); seeded RNG only; no network; under 10 s in Pyodide; no warnings (`-W error`).
- SIMULATED label: on every lab, figure or worked example that uses generated data. Exact closed-form checks with no generated data (the cash-due formula,
  the SLR ratio, the identity checks on fixed inputs) are not labelled SIMULATED.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`, `course/assets/data/*`,
  `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references in code comments.
- Banned strings (`tools/check_pages.py` lines 58-72 `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the scope", "left as an exercise",
  "you can add more", "it is important to note", "studies show", "experts agree", "it is well known", "obviously", "clearly", and any ellipsis `...` outside code.
- Percent changes state the base and the direction. Growth and rate statements state the convention.
- A finite enumeration is grade C with its basis named, not grade T (precedent: M1 L06).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration (precedent: CF1 KNOWN 3).
- Quiz explanations are read against their lesson (precedent: CF1 KNOWN 6).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10 output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols that FI4 must not give a different meaning (`notation/notation.json`, `symbols` array; `macros` object):

| Registered symbol | Registered meaning (locator) | FI4 rule |
|---|---|---|
| `T` | number of return observations in a sample (`notation.json`, module S1) | **Do not use bare `T`** for time or for a tax or term. A horizon is written `H`. |
| `R_f` | gross riskless return (AP1) | Not used. |
| `R^\ast`, `R^{e\ast}`, `\mathbb{Q}` | SDF return, excess SDF projection, risk-neutral measure (AP1) | Not used. |
| `\Phi`, `\gamma_3`, `\gamma_4` | normal CDF; skewness; kurtosis (M4) | Not used. |
| `\E` (macro) | expectation operator | Not used in FI4 prose. |
| `\R` (macro) | real numbers | Standard; write `\R`, not `\mathbb{R}` (architect ruling 1). |
| `\SR`, `\PSR`, `\DSR`, `\se`, `\Var`, `\Cov`, `\Corr` (macros) | Sharpe-ratio family, standard error, moments | Not used. |

Suggested local symbols (each defined on the lesson where it first appears and never redefined): principal `P` (in cents, integer), haircut `h`
in [0, 1), day count `d` (days), day-count basis `B` (the convention, 360 in this unit), repo rate `i^{\mathrm{rp}}` (percent per year as a decimal),
reserves `R^{\mathrm{res}}` (not bare `R`), reverse repo `RRP`, TGA `\mathrm{TGA}`, swap spread `s^{\mathrm{sw}}`, SLR `\mathrm{SLR}`.
Each is defined in the lesson where it first appears. A symbol with a registered meaning above is not reused.

NOTATION_REQUESTS: none. The plan uses only local symbols and the registered `\R` macro.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the BUILDER_RULES §4.2 structure. Mandatory content, by lesson:

- **L01 `repurchase-agreement`, `repo-haircut`.** Define a repurchase agreement as a secured one-period loan with a stated collateral, a stated
  rate and a stated repurchase price (derivation: repurchase price = principal + interest on the day-count basis; grade T as a definition with
  the basis stated). Define the haircut as the proportion of collateral value not lent against, and derive the cash lent: `P = (1 - h) V`
  (assumption: collateral value V is known and h in [0, 1)). The lab computes cash due in integer cents with the half-up rule (§5.4).
  No empirical claim about repo rates is made. The lesson's limit: a one-period, one-collateral model with no margin calls (the margin call
  appears in L05).
- **L02 `sofr`, `bank-reserves`.** Define SOFR as the name of a secured overnight rate computed by the NY Fed. **The computation is NOT READ and is NOT
  STATED here.** The lesson describes SOFR only as the overnight secured rate the curriculum names, with no formula, no sample and no volume-weighting
  claim, unless the verifier reads the NY Fed methodology section and quotes its locator (B3). Define bank reserves as the liability of the central bank
  to commercial banks held in their accounts. Derive the reserve identity used in L03. The lab uses SIMULATED reserve paths.
- **L03 `central-bank-balance-sheet`, `dealer-balance-sheet-constraint`.** The liability identity: total liabilities = currency + reserves + reverse
  repo + TGA + other liabilities (T, an accounting identity by definition of the balance-sheet lines; the lab checks it exactly on fixed numbers).
  Define the dealer balance-sheet constraint as a capacity inequality: financed positions ≤ equity-funded capacity under a stated ratio (a
  model, graded T conditional on the stated ratio). The lesson's limit: no dealer price impact and no endogenous reserves.
- **L04 `supplementary-leverage-ratio`, `swap-spread`.** The SLR as a ratio of Tier 1 capital to a total leverage exposure, with the numerator
  and denominator named as definitions taken from the lesson's stated formula (T, with the formula as an assumption). **The regulatory
  definitions and their history are NOT READ.** `bis2014basel` (primary, BIS, 2014) and `frb2020federal` and `frb2025federal` (primary, Board)
  are registry records the builder may cite at record level only after reading the cited page for each locator. Until then they are cited
  for their existence, with no content claim. The swap spread: the difference between a swap rate and a Treasury yield of the same maturity,
  with the sign and basis stated (definition, grade T). `interest-rate-swap` is outside the closure (§4 D1): plain prose.
- **L05 `treasury-basis-trade`, `dash-for-cash`.** Define the cash-futures basis as the difference between the cash Treasury price and the
  implied futures-based price, and show the one-period P&L of a long cash, short futures position with a repo financing leg (T, derivation with
  the stated convention). The curriculum lab (`lab-FI4-L05-1`, `curriculum/03-markets.yaml:144`) computes the P&L with haircut and margin in integer
  cents, SIMULATED. The dash for cash: the lesson describes it as the episode named in the curriculum core, and states what the registry supports.
  `he2022treasury` (JFE 143(1)) is the curriculum's own source: the builder reads its abstract before any claim, and grades each claim by its
  sample and period. Any claim about the size of the basis or the dealer response is graded B or C with the counter-evidence named, or is removed.
  **The claim that repo runs or dealer constraints caused the episode is contested in the literature; the lesson names only the mechanism the
  model derives.**

Lesson-level constraints:
- Each lesson's "Where the canon breaks" section names at least one model limit and what changes without it (for example, no margin calls in L01;
  static dealer capacity in L03; no regulatory dynamics in L04; one-period basis in L05).
- No lesson uses an E8 (open economy, cross-currency basis), SR1 (run on repo), SR4 (SLR policy history), BK1 (Basel capital theory) or LX1 (lender of last resort)
  concept as a defined concept. Those are outside the closure or later in the topological order (§4).

---

## 4. DAG questions (concepts natural FI4 content would use outside the closure)

Prerequisite closure of FI4 (computed): **{AC1, CF1, E1, E5, FI1, M1, M2, P0.1}**. Owners below are from the `concepts` map (`coursekit.concept_owner()`).
"Topo" is the 0-based index in `topological_order`. FI4 is at 33.

| Ref | Concept(s) | Owner, topo index, built status | Where natural FI4 content would use it | Resolution in this plan (recommended) |
|---|---|---|---|---|
| D1 | `interest-rate-swap`, `futures-contract`, `futures-margining`, `forward-contract` | FC2, topo 30, built | swap spread (L04); cash-futures basis and margin (L05) | Plain prose, no link, no `dfn` (architect default). Alternative: add FC2 as a prerequisite (a curriculum change, `curriculum/03-markets.yaml:125`). FC2's closure does not contain FI4 (size 8), so the change is cycle-safe. |
| D2 | `central-counterparty`, `margin-cover`, `ccp-default-waterfall`, `settlement-cycle` | BK4, topo 32, built | central clearing of repo and the margin in L05 | Plain prose. Alternative: add BK4 (its closure of size 5 does not contain FI4). |
| D3 | `basel-iii-capital`, `liquidity-coverage-ratio`, `net-stable-funding-ratio` | BK1, topo 31, **NOT built** (prereqs FC1, FI1, AC1) | the SLR (L04) as a Basel-style leverage ratio | Plain prose only. BK1 is unbuilt, so a link would point at a concept page that is not yet part of the site's built modules. |
| D4 | `run-on-repo`, `liquidity-spiral`, `bank-run` | SR1, topo **49** (later than FI4), **NOT built** (prereqs BK1, E4) | repo runs in the dash for cash (L05) | **Plain prose, no link. Do not add SR1.** A link would be a use before introduction (SR1 is later in the topological order). |
| D5 | `lender-of-last-resort` | LX1, topo **36** (later than FI4), built (prereqs FC1, E5) | Fed backstops in the dash for cash (L05) | Plain prose, no link. |
| D6 | `covered-interest-parity`, `cross-currency-basis` | E8, topo 41 (later) | not used (FX out of scope, §2.1 item 4) | Not used. |
| D7 | `value-at-risk`, `stress-testing` | PR4, topo 86 (later) | haircut sizing could be framed as VaR | Not used. The haircut is defined as a ratio (L01). |
| D8 | `volcker-rule`, `central-clearing-mandate`, `treasury-market-liquidity`, `intermediation-capacity` | SR4, topo 73 (later; SR4 requires FI4) | regulatory history of the SLR and of dealer capacity | Not used. |
| D9 | `cds-bond-basis` | CR2, topo 99 (later) | the basis in the credit market | Not used. |
| D10 | `bid-ask-spread` | FC1, topo 26, built, not in closure | liquidity during the dash for cash (L05) | Plain prose. Alternative: add FC1 (its closure is {P0.1, E1}, cycle-safe). |
| D11 | `limits-to-arbitrage` (and `shleifer1997limits`) | AP6, topo 95 (later) for the concept; the registry key `shleifer1997limits` exists | why a basis can persist (L05) | Plain prose for the phrase; the key may be cited at record level after the builder reads the abstract (§7.1). No concept link. |
| D12 | `expectation` (M4) | M4, not in closure | not needed in FI4 | Not used. |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Each row needs the architect's confirmation (§12 Q3 to Q7).**
`check_dag.py` checks linked uses only (`tools/check_dag.py` docstring). An unlinked use of D1 to D12 passes the tool, so the verifier reads every lesson
for these names (VERIFIER §2.9).

Confirmed by the planner: no FI4 concept is also defined by another module (all 10 owners are FI4). No cycle is created by any alternative in D1, D2 or D10.

---

## 5. Project (`project.html`, Builder E): autograder and rubric (`grading: both`)

### 5.1 Ladder (BLUEPRINT §5.1; `check_projects.py` requires the order)

1. **Rung 1, worked example** (`lab-FI4-project-1`, SIMULATED): one fully solved, annotated computation on a generated five-day plumbing path:
   the cash due on one repo, the haircut-adjusted cash, one swap spread and one reserve-identity check. Each step has a "why" annotation.
   Full length (tier U; BLUEPRINT §4 minimum applies from tier M).
2. **Rung 2, completion** (`lab-FI4-project-2`, `class="lab completion"`, SIMULATED): the reserve-identity line and the swap-spread line are removed (`___`).
   Graded instantly. Its twin is the completed solution; every page line equals the twin line or contains a blank (architect ruling 11).
3. **Rung 3, independent project** (graded by the autograder and the rubric): the monitor and the memo, built from the five input series in §5.2.
   `lab-FI4-project-3` is the rung-3 check: it recomputes the monitor's default state from the same inputs and prints the table the monitor should show.
4. **Rung 4, stretch** (optional, not graded): a second stress episode with the same monitor, or a comparison of two haircut schedules with the
   change in the cash lent stated exactly.

### 5.2 Spec (`dl.spec`; `check_projects.py` requires the terms context, inputs, required outputs, constraints, grading)

- **Context.** A repo desk analyst must monitor the plumbing of the overnight funding market and write a mechanism-level explanation of one stress
  episode. The monitor must show the five input series and the checks that turn them into a status table. The memo must cite the values it uses.
- **Inputs.** Five series, each in BYOD mode unless stated, each with a named source and a stated transform:
  1. reserves held at the central bank (level, USD; BYOD);
  2. the reverse-repo facility balance (level, USD; BYOD);
  3. the Treasury General Account balance (level, USD; BYOD);
  4. repo rates, one overnight secured rate (percent per year; BYOD; the SOFR series is not cleared, B1);
  5. the swap spread, computed from swap rates (BYOD) and the embedded `ust_daily` `cmt_10y` as the Treasury leg, with the basis caveat (`tbill_3m` is on a
     discount basis per `tools/data_sources.yaml` `ust_daily.note`; `cmt_10y` is a constant-maturity yield). The builder states the convention, or the architect
     approves an alternative (§12 Q5).
  The CSV schema for series 1 to 4 (and the swap-rate file for 5) is documented on the project page and validated in the browser; the file never leaves the browser
  (BUILDER_RULES §6.6). Labs and the worked example use generated paths labelled SIMULATED.
  **Schema (recommended).** One file per series. UTF-8 CSV; header `date,value`; `date` ISO 8601 (YYYY-MM-DD); `value` a decimal string with
  at most two decimals for USD amounts (parsed to integer cents, rejected otherwise: `ValueError`) and at most six decimals for rates (parsed to `Fraction`,
  rejected otherwise: `ValueError`); dates strictly increasing; no blank rows. The validator is part of the autograder (§5.4).
- **Required outputs.** `monitor.*` (the student's format: notebook, spreadsheet or static page) showing the five series with units, and a one-page
  memo file `memo.md`. The memo explains one stress episode through the mechanism the lessons derive (haircut, dealer capacity, reserves, SLR) and states
  the monitor's status for the chosen date, with every number cited to its series, date and transform. Every number is recomputed from exact values, with the
  rounding rule stated (§5.4).
- **Constraints.**
  - Every number in the memo cites the series, the date and the transform that produced it.
  - No claim about a series beyond its source's coverage. No claim that a repo rate is SOFR unless the student's file says so.
  - Standard library or any tool the student chooses; the autograder requires the functions in §5.4 with the names and types given.
  - The inputs are the five series above; no series from Atlas is used (B2 does not apply: none is named).
- **Grading.** `both`: autograder (the functions in §5.4, dual-mode) plus rubric (§5.5) for the memo. The spec's grading entry names both.
  Adversarial question bank: not required (§12 Q13).
- **Reading list.** `ol.reading-list` cites `he2022treasury` and `frbndfederal` and `frbnyndadditional` (registry keys; the curriculum sources)
  and, after the builder reads each locator, `bis2014basel`, `frb2020federal` and `frb2025federal`. Nothing else.

### 5.3 Time budget (`<table id="hours">`, sums to 20 h; every row needs a rationale; `check_projects.py` hours check)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 1 | One solved SIMULATED path, annotated line by line |
| Rung 2, completion problem | 2 | Fill the reserve-identity line and the swap-spread line, then run the instant check |
| Data intake: CSV schemas, validation, the swap-spread convention | 4 | Document the schemas, validate a student file, state the basis convention for `tbill_3m` and `cmt_10y` |
| Monitor build: cash-due, haircut, reserve identity, SLR, swap spread | 6 | Five functions of §5.4 plus the status table |
| Memo: one stress episode, mechanism, cited numbers | 5 | One page, every number cited with its date and transform |
| Self-assessment against exemplars | 2 | Score the memo with the rubric, then compare with exemplar-a and exemplar-b |
| **Total** | **20** | Equals `data-hours-project` on the hub |

Builder E checks this table against its own estimate; a total more than 30% away from 20 h fails the verifier (VERIFIER §2.6).

### 5.4 Autograder design (`grader/`; dual-mode; `grading: both`)

Standard library only. Money is `int` cents. Rates are `fractions.Fraction`. Floats are not used anywhere in the reference, the alternatives
or the validator. Instances are SIMULATED and generated per seed; no data file is read by the grader.

**Files.**
- `grader/instance.py`: `make_instance(seed: int) -> dict`. Deterministic; generates a materially different plumbing panel per seed (principal,
  haircut, day count, repo rate, the five series, a swap rate and a Treasury yield). Only valid instances.
- `grader/reference.py`: the full solution. Passes every test for seeds 0 to 49.
- `grader/test_project.py`: pytest suite. Tests check values, invariants and failure behaviour.
- `grader/starter.py`: the stub the student fills in (function signatures with `raise NotImplementedError`).

**Public functions the student implements (names and types fixed on the page).**
1. `repo_cash_due(principal_cents: int, rate: Fraction, days: int, basis: int = 360) -> int`: interest on the convention of L01,
   `interest = principal × rate × days / basis`, rounded half-up to whole cents from the exact value; returns principal plus interest in cents.
   `ValueError` if `principal_cents <= 0`, `days < 0`, `basis <= 0`, or `rate < 0`.
2. `cash_lent(collateral_value_cents: int, haircut: Fraction) -> int`: `floor`-free exact value `collateral × (1 - haircut)` rounded half-up to whole cents.
   `ValueError` if `collateral_value_cents < 0` or `haircut` not in `[0, 1)`.
3. `swap_spread_bp(swap_rate: Fraction, treasury_yield: Fraction) -> Fraction`: `(swap_rate - treasury_yield) × 10000`, in basis points, exact.
   No error case stated; no test demands one.
4. `reserve_identity_gap_cents(total_liabilities_cents: int, currency_cents: int, reserves_cents: int, rrp_cents: int, tga_cents: int, other_cents: int) -> int`:
   `total_liabilities - (currency + reserves + rrp + tga + other)`. Returns 0 on a consistent table. `ValueError` if any input is negative.
5. `slr(tier1_capital_cents: int, total_leverage_exposure_cents: int) -> Fraction`: `tier1 / exposure` exact. `ValueError` if `total_leverage_exposure_cents <= 0`
   or `tier1_capital_cents < 0`.

The page names exactly these conditions for these exception types. Tests demand a `ValueError` only for the named conditions (ruling 19); a
`TypeError` from a correct implementation on a wrong input type must pass.

**Validator (`validate_csv`)** is a public function returning the parsed series or raising `ValueError` on the named rules of §5.2. It is tested
for: a valid file, a header error, an unsorted date, a USD amount with three decimals, a rate with seven decimals, a blank row.

**Test design (`test_project.py`).** Each stated condition, boundary and error type gets its own isolated test, in both directions of every inequality
(for example `haircut = 0` accepted, `haircut = 1` rejected, `haircut = 1/2` accepted; `days = 0` accepted, `days = -1` rejected; `principal = 1` accepted,
`principal = 0` rejected). Values are checked by exact equality on `Fraction` and on `int` cents. The half-up rule has its own tests with exact ties:
a value whose exact fraction is `x.5` cents rounds up, a value at `x.4999…` in exact arithmetic (expressed as a `Fraction` just below `x.5`) rounds down.
Tests must not pass a trivially wrong or hard-coded answer. Failure messages name the violated property and never print the expected value
(`__tracebackhide__`, ruling 19). The suite has a collect-only count quoted on the page. Every test finishes in under 5 s in Pyodide; the whole suite
under 60 s.

**Ten student-error mutants** (single-change copies of the reference, under `ledgers/FI4/mutants/`; first docstring line names the error):
1. `m01_daycount_365`: uses basis 365 as the default in `repo_cash_due`, not the basis the page states.
2. `m02_haircut_inverted`: `cash_lent` returns `collateral / (1 - haircut)`.
3. `m03_end_day_counted`: `days` counted as end minus start plus one in the caller helper.
4. `m04_floor_rounding`: rounds money by floor instead of half-up.
5. `m05_float_money`: computes `cash_lent` and `repo_cash_due` in `float` and rounds with `round()` (wrong on the exact ties in the tests).
6. `m06_swap_spread_sign`: returns `(treasury_yield - swap_rate) × 10000`.
7. `m07_slr_rwa_denominator`: divides by a risk-weighted-assets argument instead of total leverage exposure (the student uses the wrong denominator).
8. `m08_identity_omits_tga`: `reserve_identity_gap_cents` leaves out `tga_cents`.
9. `m09_rate_not_scaled`: uses the rate per year as the per-period rate (no `days/basis` factor).
10. `m10_negative_principal_accepted`: `repo_cash_due` accepts `principal_cents <= 0` without raising.

Each mutant must be killed by at least one test in `test_project.py` on seeds 0 to 9 (`tools/mutate_graders.py --unit FI4 --seeds 0-9`).
A mutant that survives and violates a behaviour stated on the page is killed by a new test (ruling 9). A mutant that differs only where the page states
nothing goes to `ledgers/FI4/equivalent/` with a README proof.

**Five correct alternative implementations** (under `ledgers/FI4/alternatives/`, each of a different style, each passing seeds 0 to 49):
- `alt_1_fraction_direct`: direct `Fraction` arithmetic with a helper `_half_up`.
- `alt_2_basis_points_int`: integer arithmetic on scaled integers (rates in units of 10⁻⁶), no `Fraction` in the core path.
- `alt_3_dataclass_api`: the five functions as methods of small frozen dataclasses that the module-level functions call.
- `alt_4_pure_helpers`: generator-based helpers, one function per formula, no shared state.
- `alt_5_class_monitor`: a `PlumbingMonitor` class that calls the same five functions and caches intermediate results per call.

A float-based alternative that is wrong on a stated exact rule is a mutant, not an alternative (ruling 10).

**Instance check.** The verifier samples 20 seeds: every instance is valid and the answers differ materially (not only the labels).

### 5.5 Rubric (`table.rubric#rubric`; memo, rubric-graded)

Five criteria. Each criterion is one table row: the criterion name in a `th`, and exactly four `td` cells for levels 4 down to 1.
Every level descriptor is observable.

1. **Data and provenance.** Level 4: names each of the five inputs with its source, its date range and its transform, and states which are BYOD and which are
   embedded. Level 1: "uses the data".
2. **Computation.** Level 4: states the rounding rule and computes every money figure from integer cents and every rate from `Fraction`. Level 1: "rounds the numbers".
3. **Mechanism.** Level 4: traces the stress episode through at least two of: the haircut, the dealer balance-sheet constraint, reserves and the reverse-repo
   balance, the SLR, the basis, each with the step that links it to the next. Level 1: "a sensible story".
4. **Evidence and counter-evidence.** Level 4: grades each claim T, A, B or C with its basis, and for every B or C claim names the published counter-evidence
   or states that none was read. Level 1: "cites some sources".
5. **Limits.** Level 4: names the model limit that bears on each conclusion (one period, no margin call, static dealer capacity, coverage of BYOD files) and
   what would change it. Level 1: "notes some caveats".

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, fully written memos on a SIMULATED episode, annotated with the descriptors
each passage meets or misses. Self-assessment form (`section.rubric-self`, `data-rubric="rubric"`, `data-exemplars="exemplar-a exemplar-b"`, as in E5).
The page shows where the student's scores diverge from the exemplar scores.

**Blind scoring (ruling 23).** The exemplars are scored blind by a dedicated scorer agent that never opens `project.html`. It runs a stripping script over the
exemplar files (drops annotation elements, verdict lines and `data-score(s)` attributes) and reads only the script's output (ruling 15). Its scores must match the
official scores within one level on every criterion (VERIFIER §2.6).

---

## 6. Real-data policy (B1 applies)

- **Embedded (redistributable, grant quoted):** `fx_daily`, `fx_monthly`, `ust_daily`. Only `ust_daily` (`cmt_10y`, `tbill_3m`) is relevant, for the Treasury leg of the
  swap spread (§5.2 input 5).
- **Candidate, not cleared:** H.4.1 (`frbndfederal`). The Board's disclaimer grant is recorded (planner WebFetch, 2026-11-09); the H.4.1 page states none
  of its own; the Website Policies page is NOT READ. The architect decides whether to add H.4.1 to `tools/data_sources.yaml` (BUILDER_RULES §6.6). Default: not added.
- **Not cleared:** SOFR (NY Fed reference-rate page has no redistribution sentence; Terms of Use NOT READ). Repo rates: no source identified.
- **Not embedded and not identified:** swap rates, reserves/RRP/TGA time series if H.4.1 is not approved. BYOD (§5.2).
- **Honest-pending note** on L02, L05 and the project's data page: "The curriculum names the Federal Reserve H.4.1 release and the NY Fed SOFR methodology as
  sources for this unit. No redistribution grant for the money-market series has been verified, so the lab uses a generated economy labelled SIMULATED, and the
  project takes these series in bring-your-own-data mode." Cited to the DATA_REQUESTS entries (§7.2).
- **DATA_REQUESTS** (for the architect; the planner does not name a licence from memory): (i) H.4.1 under the Board's website disclaimer, with the Website Policies
  quote and the H.4.1 transform (weekly reserve factors, RRP, TGA); (ii) SOFR and the repo rates under the NY Fed Terms of Use, with the quoted sentence and its page;
  (iii) swap rates for one tenor, with the issuer's terms. Each needs the BUILDER_RULES §6.6 steps 1 to 5.
- No `data-files` attribute on any lab until a dataset is embedded. No MANIFEST entry is added by builders.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (verified in `references/references.json`; grep-checked by key)

| Key | Record (as read) | Status | Use in FI4 |
|---|---|---|---|
| `he2022treasury` | He, Nagel & Song, "Treasury inconvenience yields during the COVID-19 crisis", JFE, volume 143, issue 1, year 2022, DOI 10.1016/j.jfineco.2021.05.044; Crossref-verified; `used_by: ["FI4"]`; source string matches `curriculum/03-markets.yaml:141` | verified | L05 dash for cash and basis (the curriculum's own source); reading list. Claims graded after the abstract is read (§3 L05). |
| `frbndfederal` | Federal Reserve Balance Sheet: H.4.1 release dates page, `https://www.federalreserve.gov/releases/h41/`; issuer-verified; no year; `used_by: ["FI4"]`; `title_recall` 1.00 | verified (issuer) | L02/L03 reserve and RRP data source; project input source. Only the page's existence and its XML download are stated (planner WebFetch); no content claim without the verifier's reading. |
| `frbnyndadditional` | Federal Reserve Bank of New York, "Additional Information about Reference Rates Administered by the New York Fed", `https://www.newyorkfed.org/markets/reference-rates/additional-information-about-reference-rates`; issuer-verified; `used_by: ["FI4"]`; **`title_recall` 0.71 against "SOFR methodology"** (§0.3 B3) | verified (issuer), flagged | L02 SOFR: only the calculation section the verifier reads. Flag for the architect. |
| `gorton2012securitized` | Gorton & Metrick, "Securitized banking and the run on repo", JFE 104(3), 2012 (Crossref); `used_by: ["SR1"]` | verified | L05 repo runs: record-level citation after the builder reads the abstract; not curriculum-listed for FI4 (optional). |
| `brunnermeier2008market` | Brunnermeier & Pedersen, "Market Liquidity and Funding Liquidity", RFS 22(6), 2009 (year field 2008; Crossref); `used_by: ["SR1"]` | verified | L05 funding liquidity: record-level after abstract read (optional). |
| `duffie2011central` | Duffie & Zhu, "Does a Central Clearing Counterparty Reduce Counterparty Risk?", RAPS 1(1), 2011 (Crossref); `used_by: ["BK4"]` | verified | L01 or L05 clearing mention: record-level after abstract read (optional). |
| `bis2014basel` | Basel Committee / BIS, "Basel III leverage ratio framework and disclosure requirements", 2014 (issuer; primary); `used_by: ["SR4"]` | verified (issuer) | L04 SLR definition: cite only after the builder reads the page locator; otherwise existence only. |
| `frb2020federal` | Federal Reserve Board press release on the temporary SLR change, 2020 (issuer; primary); `used_by: ["SR4"]` | verified (issuer) | L04 history of a temporary SLR change: existence only unless read. |
| `frb2025federal` | Federal Reserve Board final rule on the enhanced SLR, 2025 (issuer; primary); `used_by: ["SR4"]` | verified (issuer) | L04 regulatory context: existence only unless read. |
| `shleifer1997limits` | Shleifer & Vishny, "The Limits of Arbitrage", JF 52(1), 1997 (Crossref); `used_by: ["AP1", "AP6"]` | verified | L05 why a basis can persist (D11): record-level after abstract read. |

Keys the module may **not** use: any key with a `used_by` that is an unrelated module and whose claim the plan has not read. The planner read none
of the bodies of the keys above; each claim is graded only after the builder reads the abstract or page.

Not curriculum-listed but registry-verified and not to be used by FI4 without approval: `he2013intermediary` (AP6), `adrian2010liquidity` (SR2), `duffie2010presidential` (AP6).

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- {doi: null, authors: "Basis-trade literature (lead only; no author typed)", year: "not typed", title: "empirical studies of the Treasury cash–futures basis trade", venue: "not typed", needed_for: "L05 two-sided treatment of any claim about the basis's size or persistence (BUILDER_RULES §2.5)", confidence: "the need is certain; no record is identified by this planner"}
- {doi: null, authors: "Dash-for-cash literature beyond He, Nagel & Song (lead only; no author typed)", year: "not typed", title: "studies of Treasury market dislocation and dealer balance sheets in March 2020", venue: "not typed", needed_for: "L05 counter-evidence for the dash-for-cash claim (B4)", confidence: "the need is certain; no record is identified by this planner. Note: the registry holds an unresolved review-queue entry for Duffie (2020) (SR4 use), which must not be admitted by this unit"}
- {doi: null, authors: "SOFR computation (lead only; no author typed)", year: "not typed", title: "NY Fed calculation methodology for the TGCR, BGCR and SOFR", venue: "NY Fed (primary)", needed_for: "L02 statement of how SOFR is computed; if not read, no computation claim", confidence: "the registry record `frbnyndadditional` may or may not be the methodology document (§0.3 B3); the architect confirms the locator"}
- {doi: null, authors: "Repo-market literature (lead only)", year: "not typed", title: "empirical studies of repo rates, haircuts and collateral", venue: "not typed", needed_for: "L01 any empirical haircut or repo-rate claim (none is planned)", confidence: "the need is conditional; the plan makes no empirical haircut claim"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4). Until resolved, the lessons teach the
models with derivations and no empirical attribution, and each empirical sentence is graded C at most with its basis named, or is removed.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for FI4 (`curriculum/03-markets.yaml:145-152`, §0.3 B2). No `atlas/FI4.contract.md` is needed.

---

## 9. Cards builder (Builder F, after A to E)

- `course/modules/FI/FI4/cards.json`, ids `FI4-c001` upward, `lesson` in L01 to L05, one card per definition, theorem statement, key formula, key result
  and misconception (BUILDER_RULES §7). `check_pages.py` `check_cards` checks the id prefix, the lesson existence, the grades and the registry keys.
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example `"basis": "Lab 1, Derivation 2 (exact)"`.
- Cite a registry key only for an empirical or attributed claim. `cite` is `[]` where the card is a model result.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit FI4            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit FI4
.venv/bin/python tools/check_projects.py --unit FI4
.venv/bin/python tools/run_labs.py --unit FI4               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/FI/FI4/L01.html            # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/FI/FI4/L02.html --refresh lab-FI4-L02-1
.venv/bin/ruff check tests/labs/FI4 && .venv/bin/ruff format --check tests/labs/FI4
.venv/bin/mypy tests/labs/FI4                               # strict, repository configuration
```

Builder E (grader), targeted:

```bash
.venv/bin/python tools/run_graders.py --unit FI4 --seeds 0-49
.venv/bin/python tools/mutate_graders.py --unit FI4 --seeds 0-9
```

Verifier only, on a quiet machine: `.venv/bin/python tools/page_smoke.py --unit FI4` (not run by builders; timing-sensitive),
`.venv/bin/python tools/verify_refs.py --unit FI4` (the unit ledger's run, VERIFIER §2.1), and `.venv/bin/python tools/fetch_data.py --check` only if B1
adds a dataset.

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`, and the full gate in CLAUDE.md.

Flag checks: `check_pages.py`, `check_dag.py`, `check_projects.py`, `run_labs.py`, `embed_labs.py` accept `--unit` (or `--page`) as E5 uses them.
The planner did not execute the builder commands; only `coursekit` closure, owner, unit and built-status functions were run (§0.1).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** FI4 has no `atlas:` key and no Atlas entry names FI4 (`curriculum/03-markets.yaml:145-152`). No contract is needed.
2. **No debate.** FI4 has no `debate:` key, so `check_pages.py` does not require a debate brief (B4).
3. **Autograder plus rubric.** Unlike E5 (rubric only), FI4 is `both`. The grader rules of ruling 19 and §5.4 apply in full: ten mutants, five alternatives,
   per-condition isolated tests, collect-only count on the page.
4. **Rung 2 must be graded instantly.** `check_projects.py` accepts a completion lab or a quiz. The plan uses a completion lab.
5. **Lab count.** The curriculum names one lab (`curriculum/03-markets.yaml:144`). BUILDER_RULES §3.4 asks for a numerical check per key formula, so the plan adds one lab per lesson (E5 precedent).
6. **FI1 is not built.** The FI4 hub must not link an FI1 page. Links to FI1 concepts go to `concepts.html` anchors only (as E5 did for E1).
7. **check_dag sees linked uses only.** Unlinked uses of D1 to D12 (§4) pass the tool; the verifier reads for them.
8. **Labs must be exact.** Standard-library `fractions` and integers, `-W error` clean under `python -I`.
9. **The hub's data-hours rules.** Lesson hours 6 to 12 and the hub split (40 + 20 = 60) are satisfied by §1.
10. **Money is in cents.** No float money in any twin or grader (BUILDER_RULES core guardrails; §2.1 item 8).

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **B1, data for the lab and the project.** RECOMMENDED: SIMULATED generated economy for L02, L05 and the project's worked example, with the honest-pending note
   (§6); BYOD for reserves, RRP, TGA, repo rates and swap rates; `ust_daily` for the Treasury leg only. Do not add H.4.1 or SOFR to `tools/data_sources.yaml` until the
   Website Policies page and the NY Fed Terms of Use are read and quoted (DATA_REQUESTS (i) and (ii)).
2. **Lesson count and hours.** RECOMMENDED: 5 lessons × 8 h and a 20 h project (33%). Alternatives within the rules: 4 lessons × 10 h with a 20 h project (two concepts
   per lesson fails for 10 concepts over 4 lessons, so the concept split would need 3+3+2+2); 6 lessons × 6 h with a 24 h project (40% maximum).
3. **D1 FC2 prerequisite.** RECOMMENDED: plain prose for `interest-rate-swap` and `futures-contract`; no prerequisite change. Alternative: add FC2 (cycle-safe, §4 D1).
4. **D2 BK4 prerequisite.** RECOMMENDED: plain prose; no change. Alternative: add BK4.
5. **Term-spread and basis convention for the swap spread (project input 5).** RECOMMENDED: (a) `cmt_10y` minus the swap rate as the Treasury leg, with
   the basis caveat stated and no discount-to-yield conversion claimed (the `tbill_3m` is not used in the swap spread). Alternative: (b) a basis conversion
   written in L04 as a derivation. Do not use (c) dropping the spread: the brief names swap spreads (`curriculum/03-markets.yaml:148-149`).
6. **D3 BK1 and D4 SR1 and D5 LX1.** RECOMMENDED: plain prose for all three; do not add SR1 or BK1 as prerequisites. SR1 is later in the topological order
   (topo 49 against FI4's 33) and BK1 is not built.
7. **Scope (§2.1 item 4).** RECOMMENDED: confirm the scope as written: one-period secured loans, static SLR ratio, one-period basis, dash for cash as a described
   episode. No FX (E8), no CCP waterfall (BK4), no Basel capital theory (BK1).
8. **Curriculum string versus record for the NY Fed source (B3).** RECOMMENDED: keep `frbnyndadditional` as the record; the verifier reads the
   "Calculation Methodology" section and confirms it; the architect then either corrects the curriculum string or accepts the record title. Builders make no SOFR
   computation claim until then.
9. **Registry keys beyond the curriculum's sources.** RECOMMENDED: allow the record-level citations listed in §7.1 (`gorton2012securitized`, `brunnermeier2008market`,
   `duffie2011central`, `bis2014basel`, `frb2020federal`, `frb2025federal`, `shleifer1997limits`) only after the builder reads the abstract or the page for each
   locator; otherwise existence only. Their `used_by` entries are updated by the registry tool at integration, not by builders.
10. **Basis-trade and dash-for-cash literature (REFERENCE_REQUESTS).** RECOMMENDED: file the requests in §7.2. Until admitted, L05 grades every empirical claim C
    with the basis named or removes it. Do not admit the review-queue Duffie (2020) entry from this unit.
11. **Money units.** RECOMMENDED: integer cents in every twin, grader and validator; rates as `Fraction`; the rounding rule half-up from the exact value (§5.4).
    Confirm.
12. **Debate brief.** RECOMMENDED: no debate brief (no `debate:` key, B4); the two-sided rule still applies to B- and C-graded claims in L05.
13. **Adversarial question bank.** RECOMMENDED: none. The project is a monitor and a memo, not an IC defence, debate or referee report.
14. **Notation.** RECOMMENDED: the local symbols in §2.3; no NOTATION_REQUESTS. Confirm that bare `T` is not used for time or tax.
15. **Figures.** RECOMMENDED: no live figures (no chart kernel needed), as E5. Confirm, or request one figure with a kernel and test (BUILDER_RULES §6.4).
16. **Glossary.** RECOMMENDED: terms outside the 10 concepts (overnight rate, reverse repo, TGA, margin, balance-sheet capacity, cash-futures basis, central
    counterparty, collateral) are plain `<dfn>` with no `data-concept`. No GLOSSARY_REQUESTS needed.
17. **FI1 not built.** RECOMMENDED: proceed; FI4 links to FI1 concepts only through `concepts.html` anchors (as E5 did for E1). Confirm the build order is acceptable
    for a prerequisite that is unbuilt, or hold FI4 until FI1 is built for the hub's prerequisite link.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02 (includes the hub's titles), L03-L04, L05 (includes the curriculum lab), the project
   (rubric and exemplar calibration, with the blind scorer of ruling 23), and the grader (ten mutants killed, five alternatives passing seeds 0-49, collect-only count).
   Failing rows return to the builder that owns the file, with only the failing rows.
3. Ledger at `ledgers/FI4.verification.json`; verifier scripts archived under `ledgers/FI4/scripts/` (VERIFIER §3). Mutants under `ledgers/FI4/mutants/`,
   alternatives under `ledgers/FI4/alternatives/`, equivalent mutants under `ledgers/FI4/equivalent/` with a README each (rulings 9 and 24).
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 must be resolved or named as an honest gap first.
   Closing round is a delta verification (ruling 30) once the slice has a full fragment.

Architect decisions: pending (§12). This plan is the planner's proposal. No decision in §12 is treated as made.

## What the planner could not establish

- The content of the He, Nagel & Song (2022) paper, the NY Fed SOFR methodology section, the H.4.1 Website Policies page, the NY Fed Terms of Use page
  and the regulatory texts behind `bis2014basel`, `frb2020federal` and `frb2025federal`. All are NOT READ. Only the WebFetch summaries in §0.3 were seen,
  and those are not file locators.
- Whether the H.4.1 weekly XML contains the reserve, RRP and TGA lines the project needs (not inspected; the zip was not downloaded).
- Any figure, coefficient or market statistic about repo, SOFR, haircuts or the basis. None is typed in this plan.
