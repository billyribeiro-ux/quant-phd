# AP2 build plan: Mean-Variance, CAPM, ICAPM & APT (planner output, 2026-11-09)

Unit: **AP2 · Mean-Variance, CAPM, ICAPM & APT** · tier U · 90 h · prerequisites M7, S1, E3 · no Atlas milestone ·
no debate key · grading `both` (autograder for the portfolio and CAPM-test engine, rubric for the memo) · output
directory `course/modules/AP/AP2/` (part code `AP`) · lab twins `tests/labs/AP2/` · ledger `ledgers/AP2.verification.json`.

Planner: Haiku, plan only. No lesson text, no curriculum edits, no registry edits, no git operations. The only file
written is this plan. Executors: Haiku builders, then independent Haiku verifiers (VERIFIER_RULES). A builder never
verifies and never writes a ledger. The planner ran read-only checks (`tools/coursekit.py` closure and concept-owner
functions through `.venv/bin/python -I`, and `grep`/`read` on the registry, data sources and tool sources). The planner
ran no build, lab, grader, or check gate.

Evidence convention: every curriculum statement cites `file:line` read during planning. Anything not in the curriculum is
marked **NOT IN CURRICULUM**. Anything computed by a script is marked **(computed)**. Registry facts were read from
`references/references.json` fields; no paper was read, so no paper locator is claimed anywhere in this plan.

**Status: BLOCKING ISSUES EXIST (§0.3, B1-B2). The hours are feasible. The curriculum's data for the lab and the project
(French portfolios, "open data") cannot be embedded: the French library is not cleared. The architect must decide B1-B2
before the builders start. Default for each is stated in §0.3 and §12.**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| AP2 id `AP2`, title "Mean-Variance, CAPM, ICAPM & APT" | `curriculum/03-markets.yaml:223-224`; `curriculum/curriculum.json:8865-8866` |
| Part AP, code `AP`, title "Asset Pricing Theory"; AP2 is the second module listed under it (AP2 first, AP1 second) | `curriculum/03-markets.yaml:206-208`, `:223`, `:264` |
| Tier `U`, hours `90` | `curriculum/03-markets.yaml:225-226` |
| Prereqs `[M7, S1, E3]` (only) | `curriculum/03-markets.yaml:227` |
| Core: "Portfolio choice, two-fund separation, CAPM derivation, the Roll critique, ICAPM, APT, the empirical failure of the CAPM." | `curriculum/03-markets.yaml:228-230` |
| `introduces` has 15 concepts (mapped to lessons in §1) | `curriculum/03-markets.yaml:231-246` |
| Sources: eight free-text strings (Markowitz 1952; Tobin 1958; Sharpe 1964; Lintner 1965; Roll 1977; Merton 1973; Ross 1976; Fama & French 1992) | `curriculum/03-markets.yaml:247-255` |
| Lab: "Security market line on French portfolios." | `curriculum/03-markets.yaml:256` |
| Project "CAPM on trial"; brief: "Test the CAPM with time-series and cross-sectional methods on open data, and write the verdict with the Roll critique addressed."; deliverable "Code plus verdict."; grading `both` | `curriculum/03-markets.yaml:257-263` (title 258, brief 259-261, deliverable 262, grading 263) |
| No `debate:` key, no `atlas:` key on AP2 or its project | `curriculum/03-markets.yaml:223-263` (absent) |
| No Atlas milestone names AP2 (20 entries; their modules are AC2, CF4, CR1, CS1, CS3, DV4, F1, FI1, FI3, GM1, GM4, MS3, PR2, PR4, QR2, QR3, S0, S4, S7, SR3) | `curriculum/curriculum.json` `atlas` array (computed) |
| JSON row for AP2 matches the YAML (hours 90, prereqs M7 S1 E3, 15 concepts, 8 sources, lab, project, grading both) | `curriculum/curriculum.json:8864-8910` (`lab` 8902; `project` 8903-8908; `part` 8909) |
| All 15 concepts map to module AP2 in the `concepts` dict | `curriculum/curriculum.json` `concepts` (computed: 15 owners = AP2) |
| AP2 is listed in the bachelor's credential and in the Investments course group | `curriculum/meta.yaml:63`, `:78` |
| Modules that require AP2 directly (downstream; their concept IDs must not change once AP2 is built): FC3, FC4, CF2, AP1, F1, PR1 | `curriculum/curriculum.json` `prereqs` (computed); AP1 at `curriculum/03-markets.yaml:268` |
| Studio STUDIO-AP requires AP3 and AP4, not AP2 | `curriculum/03-markets.yaml:212` (computed: no studio requires AP2) |
| Prerequisite closure of AP2 (computed with `tools/coursekit.py` `prerequisite_closure("AP2")`, `tools/coursekit.py:239-251`): **{CS1, E1, E3, M1, M2, M3, M4, M7, P0.1, S0, S1}** (11 modules) | run output, planner |
| Built status inside the closure: built E1, E3, M1, M2, M3, M4, M7; **unbuilt** CS1, P0.1, S0, S1 (so links to those go through `concepts.html` anchors only) | `course/modules/` listing and `tools/coursekit.py` `Unit.built` (computed) |
| Nearest built direct prerequisite: **E3** (tier U, built, grading `both`, same mode as AP2; plan `plans/E3-build-plan.md`). M7 is also built and direct; its grader design is read for §5 (`plans/M7-build-plan.md` §7) | `curriculum/02-economics-finance-core.yaml:88-123` (E3); `curriculum/01-foundations.yaml:314-315` (M7 concepts) |
| Concepts of the closure usable without definition (computed: 147 across the 11 modules) include M7 `mean-variance-optimization` (`curriculum/01-foundations.yaml:314`), M7 `quadratic-programming`, `lagrange-multiplier`, `kkt-conditions`; S1 `sharpe-ratio`, `t-statistic`, `estimator`, `hypothesis-test`, `p-value`, `confidence-interval`; M3 `least-squares-projection`, `positive-semidefinite-matrix`; M4 `covariance-matrix`, `correlation`, `variance`, `expectation`; CS1 `simple-return`, `log-return` | `curriculum/curriculum.json` `concepts` (computed owners) |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 90 h (`curriculum/03-markets.yaml:226`). Tool rules:

- lesson `data-hours` 6-12 (`tools/check_pages.py` `check_lesson`, line 227);
- hub `data-hours-lessons + data-hours-project = 90` (`tools/check_pages.py` `check_hub`, lines 325-342);
- project share 10-40% of 90, i.e. 9 to 36 h (`tools/check_pages.py` line 339-340);
- lessons sum to the hub's lessons figure (`tools/check_pages.py` line 341-342);
- objectives 4-8 (`tools/check_pages.py` lines 343-346); the placement diagnostic must carry `data-mastery` (line 351);
- the project ladder needs four rungs (`tools/check_projects.py` line 33; `tools/check_pages.py` line 356).

**Chosen split: 10 lessons × 7 h = 70 h; project 20 h (22%).** 70 + 20 = 90. Feasible. No STOP condition on hours.

### 0.3 Blocking issues (architect decision required before builders start)

**B1. The lab and the project need equity-return data that no embedded source provides.**
- The lab names French portfolios (`curriculum/03-markets.yaml:256`). The project brief names "open data" (`:259-261`).
- The embedded snapshots are `fx_daily`, `fx_monthly` and `ust_daily` only (`course/assets/data/market/MANIFEST.json`, three
  datasets; `tools/data_sources.yaml:19`, `:53`, `:91`). None is an equity return series. `ust_daily` carries `tbill_3m`
  (discount basis) and `cmt_10y` (`tools/data_sources.yaml:101-102`, `:115-116`).
- The Kenneth R. French Data Library is **checked and not cleared**: its pages carry a copyright line, and the HTML
  source reserves use of the images and code (`tools/data_sources.yaml:119-131`). The rejected entry states that a lab
  that needs these files "must use bring-your-own-data mode, with the student downloading the file"
  (`tools/data_sources.yaml:130-131`).
- Open Source Asset Pricing is also not cleared (`tools/data_sources.yaml:132-139`).
- BUILDER_RULES §6.6 bars embedding until the issuer's grant is quoted (`BUILDER_RULES.md` §6.6, "Adding a dataset").
- **Plan default (architect to confirm):** (a) every lab and the graded project run on a generated economy labelled
  **SIMULATED** (BUILDER_RULES §1.7); (b) the curriculum lab's French-portfolio sentence is replaced by a SIMULATED
  cross-section, with an honest-pending note on the lesson and the project page; (c) an optional rung-4 stretch uses
  bring-your-own-data (BYOD): the student downloads the French files from the issuer, the page documents the CSV schema,
  and the Python validator runs in the browser (no file leaves the browser); (d) a DATA_REQUEST is filed for an equity
  return series whose issuer's reuse statement is quoted (§6, DATA_REQUEST bullet). The planner did not read any issuer page and names no
  source or licence from memory.

**B2. The lab sentence and the project brief name data the curriculum cannot supply.**
- `curriculum/03-markets.yaml:256` ("on French portfolios") and `:259-261` ("open data") are the curriculum's words.
  Builders do not edit `curriculum/*.yaml`.
- **Plan default:** keep the lab in L05 (the security market line, §1), run it on SIMULATED data, and say on the page
  that the curriculum named French portfolios and that the library is not cleared (§6). The architect may amend
  `curriculum/03-markets.yaml:256` and `:259-261` to match (a curriculum change, not a builder task).

**B3 (non-blocking, decide with B1). The curriculum's `Roll critique` and `flat security market line` are contested claims.**
Both need counter-evidence named (BUILDER_RULES §2.5). Two registry records that could serve as counter-evidence leads
are present but are used by other units, and their content has not been read by the planner (§7.1).

Non-blocking, for the architect to see:

- **B4. Overlap with M7.** M7 defines `mean-variance-optimization` as a quadratic program (`curriculum/01-foundations.yaml:314`).
  AP2 introduces `efficient-frontier`, `minimum-variance-portfolio` and `tangency-portfolio` (`curriculum/03-markets.yaml:232-234`).
  Different concept IDs, so `check_dag.py` will not flag them. The builder must link M7 for the computation and must not
  restate the quadratic program (§4, DAG Q5).
- **B5. Unbuilt prerequisite pages.** S1, S0, CS1 and P0.1 are in the closure and not built. Links go to `concepts.html` only,
  as in E3 (`plans/E3-build-plan.md` §0.1).

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

10 lessons × 7 h = 70 h; project 20 h; total 90 h. Concept counts per row sum to 2+2+1+2+1+2+1+1+1+2 = **15**, each concept in
exactly one row (`curriculum/03-markets.yaml:231-246`, computed owner check: 15 = AP2).

| Lesson | Title (working) | Concepts it defines (`introduces`, `yaml:232-246`) | Lab twin id (`tests/labs/AP2/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Mean-variance portfolio choice | `efficient-frontier`, `minimum-variance-portfolio` | `lab-AP2-L01-1`: exact GMV weights and frontier points for a hypothetical 3-asset covariance matrix, in `Fraction`; budget and target checked exactly | 7 | Builder A |
| L02 | The tangency portfolio and two-fund separation | `tangency-portfolio`, `two-fund-separation` | `lab-AP2-L02-1`: tangency weights in `Fraction`; proportionality to the excess-return vector checked exactly; separation of a frontier point into two funds checked exactly | 7 | Builder A |
| L03 | The capital market line | `capital-market-line` | `lab-AP2-L03-1`: points on the riskless-plus-tangency mix; slope equals the tangency Sharpe ratio (`\SR`), exact | 7 | Builder A |
| L04 | The CAPM: equilibrium and beta | `capm`, `beta` | `lab-AP2-L04-1`: beta from covariances in `Fraction`; an equilibrium economy built so that the market is the tangency portfolio; the CAPM identity checked exactly | 7 | Builder B |
| L05 | The security market line (curriculum lab) | `security-market-line` | `lab-AP2-L05-1` (**the curriculum lab**, `curriculum/03-markets.yaml:256`, SIMULATED per B1-B2): an exact SML check on the L04 economy; then a seeded 10-asset SIMULATED cross-section and its OLS line, with the mispricing printed | 7 | Builder B |
| L06 | Equity risk premium and Jensen's alpha | `equity-risk-premium`, `jensens-alpha` | `lab-AP2-L06-1`: OLS alpha, beta, residual variance and t-statistic on a seeded SIMULATED excess-return path; closed form checked against the normal-equation solve | 7 | Builder B |
| L07 | The Roll critique | `roll-critique` | `lab-AP2-L07-1`: a finite economy with a riskless asset; a non-tangency proxy breaks the SML exactly while the tangency proxy does not, both checked in `Fraction` | 7 | Builder C |
| L08 | The empirically flat security market line | `flat-security-market-line` | `lab-AP2-L08-1`: seeded SIMULATED cross-sections; the mechanism by which a noisy cross-sectional slope can look flat (the estimate and its t-statistic across seeds); SIMULATED label on the figure-free table | 7 | Builder C |
| L09 | The intertemporal CAPM | `icapm` | `lab-AP2-L09-1`: a two-factor finite-state economy; the CAPM alpha of each asset equals its hedging premium, checked exactly | 7 | Builder D |
| L10 | Linear factor models and arbitrage pricing theory | `linear-factor-model`, `arbitrage-pricing-theory` | `lab-AP2-L10-1`: an exact four-asset, two-factor system; the factor premia solved in `Fraction`; an arbitrage portfolio with zero cost and zero exposure checked to have zero payoff | 7 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 70 / 20 | none | none | – | Builder A |
| project | CAPM on trial (`both`, §5) | none | `lab-AP2-project-1` (rung 1), `lab-AP2-project-2` (rung 2, `class="lab completion"`), `lab-AP2-project-3` (rung 3 check) | 20 | Builder E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py`, and the rubric and exemplars | none | none | – | Builder E |
| cards | `cards.json` from L01-L10 | none | none | – | Builder F (after A-D) |

Builder assignment summary: **A** owns L01-L03 and `index.html` (writes the hub after L01-L02 exist); **B** owns L04-L06;
**C** owns L07-L08; **D** owns L09-L10; **E** owns `project.html`, `grader/`, the three project labs and the exemplars;
**F** owns `cards.json`. Each builder writes only its own lesson files and twins.

Ordering check (no lesson links a later definition; `tools/check_dag.py` checks linked uses only, §4):
- L01 uses M7 `mean-variance-optimization`, `lagrange-multiplier`, `kkt-conditions`; M3 `positive-semidefinite-matrix`;
  M4 `covariance-matrix`, `expectation`, `variance`; M2 `gradient`.
- L02 uses L01 (`efficient-frontier`, `minimum-variance-portfolio`); S1 `sharpe-ratio`; M7 `quadratic-programming`.
- L03 uses L02 (`tangency-portfolio`, `two-fund-separation`) and S1 `sharpe-ratio`.
- L04 uses L02 (`tangency-portfolio`) and L03 (`capital-market-line`); M4 `covariance-matrix`; E1 `competitive-equilibrium`.
- L05 uses L04 (`capm`, `beta`); M3 `least-squares-projection` for the cross-section fit.
- L06 uses L04 (`beta`); M3 `least-squares-projection`; S1 `estimator`, `t-statistic`, `hypothesis-test`, `p-value`.
- L07 uses L02 (`tangency-portfolio`), L05 (`security-market-line`) and L06 (`jensens-alpha`).
- L08 uses L05 (`security-market-line`), L06 (`jensens-alpha`), L07 (`roll-critique`); S1 `confidence-interval`.
- L09 uses L04 (`capm`, `beta`) and L02 (`two-fund-separation`); E3 `expected-utility` in prose for the state variables.
- L10 uses L04 (`beta`), L09 (`icapm`, for the contrast), M3 `least-squares-projection` and M4 `covariance-matrix`.

Hours check: 10 × 7 = 70 (hub `data-hours-lessons="70"`); project 20 (hub `data-hours-project="20"`); total 90.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to AP2)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `VERIFIER_RULES.md` §2, this file,
`plans/E3-build-plan.md` (nearest built prerequisite, its architect decisions section is binding precedent),
`plans/M7-build-plan.md` §7 (autograder design precedent for a portfolio problem), `plans/E5-build-plan.md` (structure
template), and `/Users/billyribeiro/.fanout/fixer-rules.md` (binding defect classes). Study `course/modules/M/M1/` and
`course/modules/AP/AP1/` for layout, the grader panel and the rubric grammar. `course/templates/` holds the four skeletons.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) or from
   floats stated to full precision, rounded only at display. Each page that shows a rounded figure names its rounding rule.
   Precedent: E3 §2.1 item 1; fixer-rules, recompute bullet; E5 §2.1 item 1. For AP2 this covers every weight, beta, alpha, t-statistic and
   Sharpe ratio.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints; the interpretation names only
   what the printed numbers show. Every "checked", "verified" or "shown" claim names the lab, line or test that did it.
   Precedent: M1 LESSON_TEXT_DEFECTS; fixer-rules, lab-statement bullet.
3. **Attribute nothing unread.** Only the registry keys in §7.1 and §7.2 may be cited. Paper-level citation only, unless the
   builder has read the abstract. No page, table, equation number, sample period, coefficient or number is typed from
   memory (fixer-rules, attribute bullet). In particular, the Fama & French (1992) sample period and any estimate from that paper are not
   typed unless read in the abstract the builder cites.
4. **Scope words need a computation.** "every", "all", "never", "always", "any", "same", "only", "market structures",
   "the market", "the CAPM holds", "the data show" are used only where a derivation, a finite check or a lab computes the
   claim, or the scope is stated as a hypothesis (fixer-rules, scope-words bullet). AP2 scope (confirm, §12 Q8): single-period
   mean-variance investors; frictionless market; riskless lending and borrowing at one rate `r_f`; the market portfolio is
   the tangency portfolio in equilibrium; the ICAPM and APT are finite-state or finite-factor models stated with their
   assumptions. No continuous time, no transaction costs, no taxes, no zero-beta CAPM (§12 Q8).
5. **Define before use.** Each of the 15 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned
   lesson and never before it. Terms outside the 15 (market portfolio, riskless asset, excess return, expected return as
   a mean vector, Sharpe ratio as a term, idiosyncratic risk, factor exposure, zero-cost portfolio, mispricing) are defined
   in prose at first use, with a plain `<dfn>` and no `data-concept` (`tools/check_dag.py` line 45-46 skips a `<dfn>` with no
   `data-concept`).
6. **Propositions list their hypotheses.** Every Theorem, Proposition and Derivation block lists numbered Assumptions (A1, A2,
   ...) before the statement, and the proof cites them by number. Unit-wide numbering (A1-A9, used in every lesson and in the grader's
   docstrings): A1 Σ symmetric positive definite; A2 ι and μ not proportional, so the frontier is defined; A3 a riskless asset
   exists; A4 the tangency denominator is non-zero; A5 equilibrium supply sums to the market portfolio; A6 normal errors (time-series
   tests); A7 state-variable pricing (ICAPM); A8 exact factor structure with no idiosyncratic term (APT); A9 the proxy's mean is not
   the riskless rate (Roll). A lesson names only the assumptions it uses.
7. **Grader rule (autograder).** Applies to `grader/` (§5.6). Exception types only for the conditions the page names (§5.6.4);
   every named condition has its own isolated test in both directions (fixer-rules, PROJECT GRADERS bullet).
8. **Money.** AP2 has no money output. All weights, returns, betas and t-statistics are dimensionless. Returns are stated per
   period (monthly or any stated period; one period throughout a lesson).
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own
   container; no element forces the page wider than 360 px. Fraction-valued tables use `table-wrap`. `page_smoke.py` is the
   verifier's check (fixer-rules, money and horizontal-scroll bullet).
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no
    `if __name__ == "__main__":` guard. `run_labs.py` runs each twin as `python -I -W error <twin>`, with no network. Precedent:
    M1 twin `tests/labs/M1/lab-M1-L04-1.py`; E3 §2.1 item 11.
11. **Rates and returns are basis-explicit.** Each return states its period and whether it is a simple or log return
    (CS1 `simple-return`, `log-return`). `r_f` is the net per-period riskless rate, a stated hypothetical constant. The
    per-period convention is stated once on L01 and repeated where a number is quoted.
12. **Mean-variance inputs are exact.** The mean vector, covariance matrix and `r_f` are given as `Fraction` values in every lab
    and in the grader's exact functions. Where a float is used (the regression parts of L06, L08, the project's
    time-series test), the lab or test states the tolerance and the rounding rule.
13. **Notation of the market portfolio and the ones vector.** The vector of ones is written `\iota` (not `\mathbf{1}`, see §2.3).
14. **Learner-visible text.** No process words (build, builder, round, verifier, REQUESTS, unit report) on any page. No
    planning references in code comments (E3 §2.2 precedent). Lab docstrings state units.
15. **Banned strings (`tools/check_pages.py` lines 58-73, `BANNED`):** TODO, TBD, lorem, "for brevity", "details omitted",
    "beyond the scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree",
    "it is well known", "obviously", "clearly", and any ellipsis `...` outside code. Note that `\.\.\.` is the banned pattern,
    so `1...` in prose fails.
16. **Fixer rules apply to the whole unit** (`/Users/billyribeiro/.fanout/fixer-rules.md`): recompute every number from
    unrounded values; every lab statement matches code and printed output; the three rules on assumed facts (named
    Assumption, "Assuming ..." in every result that uses it, T only conditional on it); causal or directional claims are
    checked numerically; ratio bases stated; no grade for a standard nobody read.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- **Evidence.** Every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. A B- or C-graded
  claim names its published counter-evidence (BUILDER_RULES §2.5). A working paper is at most C (BUILDER_RULES §2.5).
- **Concepts.** `<dfn data-concept>` only for the 15 concepts in §1. Concept links: closure concepts use
  `<a class="concept" data-concept="<id>" href="../../../concepts.html#<id>">`. Earlier AP2 lessons use `href="Lnn.html#def-<id>"`.
  A lesson never links a concept defined in a later lesson. There is no link to an E3, M7 or S1 hub page, because only
  `concepts.html` anchors are used for unbuilt modules (B5).
- **Labs.** Code lives once in `tests/labs/AP2/lab-AP2-Lnn-1.py` (and `lab-AP2-project-1..3.py`). The page carries
  `@@LAB:<file>@@` and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output by hand. Lab ids match
  `lab-AP2-<page>-<n>` (`tools/check_pages.py`). Lab code uses the standard library only (`fractions`, `math`, `random`,
  `itertools`), no NumPy, no network, under 10 s in Pyodide, no warnings under `-W error`. A lab that draws random numbers
  seeds `random.Random(seed)`.
- **SIMULATED label.** Required on every lab, figure, table, grader instance and exemplar that uses generated returns,
  generated economies or generated panels. Exact closed-form checks (L01-L05 exact parts, L07, L09, L10) are not labelled
  SIMULATED. Hypothetical parameters in exact labs (for example a 3-asset Σ) are labelled "hypothetical parameters, not data".
- **Never hand-edit generated files**: `CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `notation/notation.json`, `MANIFEST.json`. Request changes in the output contract.
- **Hub lesson titles** match each lesson's `<h1>` at integration (CF1 KNOWN 3 precedent). **Quiz explanations** are read
  against their lesson (CF1 KNOWN 6 precedent). **Percent changes** state the base and the direction (CF1 L07 precedent).
- **A finite enumeration** is grade C with its basis named, not grade T (M1 L06 precedent).
- **Every "checked" or "verified" claim** names the lab, the line or the test that did the check.
- **Known LOW defects** of earlier units are listed in `plans/KNOWN-ISSUES.md`. A LOW wording or presentation defect a fixer defers goes there with its ledger id (ruling 26).
- **No `git commit`, no push.** The builder reports files written, commands run with exact output, and every gap in the
  BUILDER_RULES §10 output contract. Reporting PASS for a check not run is the most serious failure.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols and macros that AP2 must not give a different meaning (`notation/notation.json`):

| Registered symbol or macro | Registered meaning (locator) | AP2 rule |
|---|---|---|
| `T` | number of return observations (periods) in a sample, S1 (`notation/notation.json:111-115`) | **Used with this meaning only**: the time-series regression length. Never a horizon or a tax. |
| `R_f` | gross riskless return, AP1 (`notation/notation.json:141-145`) | **Never written.** AP2 writes the net riskless rate `r_f` (lowercase, not registered), with `r_f` stated as net per period. AP1 comes later; the lowercase symbol avoids a clash. |
| `R^\ast`, `R^{e\ast}` | SDF return and projection of 1, AP1 (`notation/notation.json:131-140`) | Not used. |
| `\mathbb{Q}` | equivalent martingale measure, AP1 (`notation/notation.json:146-150`) | Not used. |
| `\indic` (tex `\mathbf{1}`) | indicator function (`notation/notation.json:33-36`) | **The ones vector is not written `\mathbf{1}`.** Use `\iota`, which is not registered (grep: absent from `notation.json`). |
| `\SR` | population Sharpe ratio of excess returns, per period (`notation/notation.json:69-72`) | Used for the tangency Sharpe ratio and the CML slope. |
| `\hSR` | sample Sharpe ratio (`notation/notation.json:73-76`) | Used only if a sample Sharpe is stated. |
| `\se` | standard error (`notation/notation.json:101-104`) | Used for standard errors of α̂ and β̂. |
| `\E`, `\Var`, `\Cov`, `\Corr`, `\R` | expectation, variance, covariance, correlation, real numbers (`notation/notation.json:5-8`, `:13-28`) | Use the macros, not raw `\mathbb{E}`. |
| `\Normal` | normal distribution (`notation/notation.json:37-40`) | Used for the SIMULATED noise. |

Local symbols (allowed; defined on the lesson where first used, never redefined): μ (mean-return vector), Σ (covariance matrix),
w (weights), `\iota` (ones), `r_f` (net riskless rate), `r_i`, `r_m` (asset and market excess returns, defined as returns in
excess of `r_f` where stated), `α`, `β` (regression intercept and slope, and CAPM beta; `\beta_i` for asset i), `\lambda` (risk
premia in the factor models), `\sigma` (standard deviation), `k` (number of factors), `n` (number of assets).

NOTATION_REQUESTS: none. The plan uses the registered macros above and local letters only. The planner did not register any symbol.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the BUILDER_RULES §4.2 structure. Mandatory content, by lesson. Every result names its
grade and its basis. "Derivation" means a T-graded statement with the steps shown on the page.

- **L01 `efficient-frontier`, `minimum-variance-portfolio`.** Assumptions A1 (Σ symmetric positive definite), A2 (ι and μ not
  proportional, so the frontier is defined for every target above the minimum). The GMV problem, minimise `w'Σw` subject to
  `ι'w = 1`, solved by a Lagrangian (M7 `lagrange-multiplier`, `kkt-conditions`): `w_GMV = Σ^{-1}ι / (ι'Σ^{-1}ι)` (T, derivation).
  The efficient frontier as the set of minimum-variance portfolios for each target mean, written with the scalars
  `A = ι'Σ^{-1}ι`, `B = ι'Σ^{-1}μ`, `C = μ'Σ^{-1}μ`, `D = AC - B^2 > 0` (T; the inequality `D > 0` is derived from A1-A2). Define
  the frontier as the locus, and the M7 `mean-variance-optimization` as the program; the two are linked, not restated (B4).
  Lab: exact GMV and two frontier points in `Fraction`, the variance closed form checked against the direct product.
- **L02 `tangency-portfolio`, `two-fund-separation`.** With the riskless asset (A3), the tangency portfolio maximises the
  Sharpe ratio: `w_T = Σ^{-1}(μ - r_f ι) / (ι'Σ^{-1}(μ - r_f ι))` (T, derivation; the denominator is non-zero under A2 and
  `μ ≠ r_f ι`, stated as an assumption A4). Two-fund separation: every frontier portfolio is a linear combination of `w_GMV` and
  `w_T` (T). Link S1 `sharpe-ratio` for the definition of the ratio, and the registered `\SR` macro for the population value.
  Lab: tangency weights exact; the proportionality `Σw_T ∝ μ - r_f ι` checked exactly; a random frontier point split into
  two funds checked exactly (seeded, `random.Random(seed)`).
- **L03 `capital-market-line`.** Points formed by a riskless asset and the tangency portfolio: `E_p = r_f + σ_p·\SR` for every
  efficient portfolio combined with the riskless asset (T, derivation from L02). The CML slope is the tangency Sharpe ratio.
  Lab: the CML points for a grid of weights, checked exactly on the line; slope equals `\SR` exactly.
- **L04 `capm`, `beta`.** Model assumptions, stated as numbered items: homogeneous beliefs (one μ and Σ for all
  investors), mean-variance preferences, riskless lending and borrowing at `r_f` (A3), and market clearing (A5: aggregate
  holdings sum to the market portfolio). Theorem: in equilibrium the market portfolio is the tangency portfolio (T, from L02
  and A5). CAPM: for every asset `E[r_i] - r_f = \beta_i (E[r_m] - r_f)`, with `\beta_i = \Cov(r_i, r_m)/\Var(r_m)` (T; the proof
  uses the first-order condition `Σw_T ∝ μ - r_f ι` written as `\Cov(r_i, r_m) = c(μ_i - r_f)`). Define `beta` as a
  dimensionless ratio. Cite `sharpe1964capital` and `lintner1965valuation` at paper level for the model; the derivation is
  on the page (T). Where the canon breaks: the one-period, frictionless and homogeneous-beliefs assumptions are named; each
  is a model limit with what changes without it.
- **L05 `security-market-line` (the curriculum lab).** The SML is the CAPM written as a line in `(\beta_i, E[r_i])` space (T,
  rewriting of L04). Mispricing `\alpha_i = E[r_i] - r_f - \beta_i(E[r_m] - r_f)` is defined; under the model it is zero (T).
  Lab: the exact SML check on the L04 economy; then a seeded 10-asset SIMULATED cross-section whose OLS line of mean excess
  return on beta is printed with the mispricing per asset, and the lab states what the printed numbers show (not the
  empirical SML).
- **L06 `equity-risk-premium`, `jensens-alpha`.** The equity risk premium `E[r_m] - r_f` (definition; no number typed). Jensen's
  alpha as the intercept `α` of the time-series regression `r_it - r_ft = α_i + β_i (r_mt - r_ft) + ε_it` (definition). OLS as
  the orthogonal projection (M3 `least-squares-projection`), giving the closed forms for `α̂` and `β̂` (T). The standard error
  of `α̂` from the residual variance with `T - 2` degrees of freedom (T, derivation; `T` is the registered number of return
  observations). The t-statistic `α̂ / \se(α̂)` tests `α = 0` (S1 `hypothesis-test`, `t-statistic`, `p-value`; T conditional on the
  normal-errors assumption A6 and labelled as an assumption). Lab: a seeded SIMULATED excess-return path (T = 120), closed form
  against the normal-equation solve, outputs rounded per the stated rule.
- **L07 `roll-critique`.** Theorem (T, with assumptions A1-A3 from L01-L02, and A9: the proxy portfolio `p` has `E[r_p] ≠ r_f`):
  an exact SML holds for every asset with respect to proxy `p` if and only if `p` is the tangency portfolio. Proof by linear
  algebra on `\Cov(r_i, r_p) = (\Var(r_p)/(E[r_p]-r_f)) (μ_i - r_f)` for all `i` (builder writes both directions). Consequence (the
  Roll critique): because the true market portfolio is not observable, a test of the CAPM with a proxy is a test of the
  proxy's efficiency as well as of the model. The Roll claim is graded B: published work (`roll1977critique`, paper level)
  is contested; the counter-side names the published argument that a broad proxy is close to efficient, as a REFERENCE_REQUEST
  topic (§7.2, R-AP2-3) until admitted. Lab: exact in `Fraction`; a three-asset economy; the tangency proxy and a non-tangency
  proxy; the SML residual is zero for the first and non-zero for the second, printed exactly.
- **L08 `flat-security-market-line`.** Definition: the empirically flat SML (the cross-sectional relation between beta and
  average return is weaker than the CAPM line implies). The claim that the empirical SML is flat is graded B with
  counter-evidence named. Known candidate sources, all in the registry: `fama1992crosssection` (the curriculum source,
  `curriculum/03-markets.yaml:255`); `fama1973risk` (registry `used_by` S5; counter-evidence lead, to be read before any
  attribution). The builder states only what the abstract of each cited paper says (§2.1 item 3). Lab: a seeded SIMULATED
  set of cross-sections; the slope estimate and its t-statistic across seeds; the lab states that a flat-looking estimate is
  possible under noise and does not show the empirical SML is flat.
- **L09 `icapm`.** A two-factor state-variable model in a finite-state economy with stated assumptions: the expected excess
  return satisfies `E[r_i] - r_f = \beta_{i,m}\lambda_m + \beta_{i,h}\lambda_h` (T conditional on the assumed state-variable
  pricing, stated as Assumption A7; the statement is not derived from first principles here). CAPM as the special case with
  no hedging premium (T). Merton (1973) cited at paper level (`merton1973intertemporal`, `curriculum/03-markets.yaml:250-253`
  for the source string). The continuous-time derivation is not on the page; the page says so. Lab: exact in `Fraction`; the
  CAPM alpha of each asset equals its hedging premium.
- **L10 `linear-factor-model`, `arbitrage-pricing-theory`.** Linear factor model `r_i = a_i + b_i'f + e_i` (definition). APT
  in an exact finite economy: Assumption A8 (no idiosyncratic term, `e_i = 0`), the no-arbitrage requirement stated in plain
  words (no zero-cost portfolio with a non-negative payoff and a positive probability of a positive payoff; the wording is
  checked against AP1's material only after AP2 is built, DAG Q2). Theorem (T, finite economy, exact factor structure): under
  no arbitrage there exist factor premia `\lambda` with `E[r_i] - r_f = b_i'\lambda` for every asset `i` (the proof uses a
  linear-algebra separation argument, written in full or stated as a precisely cited result; no authority is typed). The
  approximate APT with diversification limits is not derived here; it is named as a limit (cite `ross1976arbitrage` at
  paper level). Lab: four assets, two factors; the factor premia solved in `Fraction`; an arbitrage portfolio with zero cost
  and zero factor exposure has zero payoff, checked exactly.

Lesson-level constraints (all lessons):
- Each lesson's "Where the canon breaks" section names at least one model limit and what changes without it.
- The 15 concept defining sentences do not claim empirical results. Empirical claims appear only in L06 (SIMULATED, not
  empirical), L07 (B), L08 (B) and in the counter-evidence sentences, and each is graded and cited.
- No lesson uses a term from AP1 (no-arbitrage theory, SDF, law of one price) as a defined concept. The names are used in
  plain words (§4).
- No lesson presents a CAPM number, a risk premium value, or a Sharpe ratio value from memory. Any such value is a computed lab
  output with its SIMULATED label or a hypothetical parameter label.

---

## 4. DAG problems (concepts that natural AP2 content would use outside the closure)

Prerequisite closure of AP2 (computed): **{CS1, E1, E3, M1, M2, M3, M4, M7, P0.1, S0, S1}**, with 147 usable concepts (the
closure's `introduces`, computed by `tools/coursekit.py`). Owners below are from `curriculum/curriculum.json` `concepts`
(computed).

| Ref | Concept | Owner (outside closure) | Where natural AP2 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `stochastic-discount-factor` | AP1 | ICAPM and APT rewritten with a pricing kernel (L09, L10) | Plain prose; not used. The factor-premia form is used instead (no link). |
| D2 | `law-of-one-price`, `fundamental-theorem-of-asset-pricing`, `arbitrage-opportunity` | AP1 (two) and FC2 | the no-arbitrage step of APT (L10) | Plain words: "no zero-cost portfolio with a sure non-negative payoff and a positive chance of a positive payoff". No link. Architect may add FC2 (DAG Q2). |
| D3 | `fama-macbeth-regression` | S5 | the cross-sectional second-pass regression in L05, L08 and the project | Plain prose: "cross-sectional regression of average excess return on beta". No link. Architect may add S5 (DAG Q3; a curriculum change; not proposed). |
| D4 | `heteroskedasticity-robust-standard-errors` | S2 | standard errors for α̂ in L06 if the residuals are not homoskedastic | Not used. The normal-errors assumption A6 is stated; no robust SE is claimed. |
| D5 | `alpha-inference`, `factor-adjusted-alpha` | F7 | the alpha of a factor-model regression in L06, L10 | Not used. L06 names only the CAPM alpha. |
| D6 | `fama-french-three-factor-model`, `carhart-four-factor-model`, `betting-against-beta` | F2 | the empirical factor models after the flat SML (L08 counter-evidence; L10 contrast) | Plain prose, named as later work; no claim about them. |
| D7 | `consumption-capm`, `equity-premium-puzzle` | AP3 | a consumption-based version of the ICAPM hedging premium (L09) | Not used. The state variable is an abstract Assumption A7. |
| D8 | `limits-to-arbitrage`, `factor-zoo`, `anomaly`, `efficient-markets-hypothesis` | AP6, F5, FC3, FC3 | the counter-evidence discussion in L08 and L10 | Not used as terms. The debate is named in plain words where needed, with a registry key and a grade. |
| D9 | `market-completeness` | E4 | the finite-state economy in L09 and L10 | Plain prose ("the state space is finite and the asset set spans or does not span the payoffs"); no link. |
| D10 | `risk-free asset`, `market portfolio`, `excess return`, `factor`, `factor exposure`, `zero-cost portfolio` | none (no concept in `concepts`; computed) | throughout | Plain `<dfn>` with no `data-concept` at first use (§2.1 item 5). |
| D11 | `mean-variance-optimization` (M7, in closure) vs `efficient-frontier`, `tangency-portfolio`, `minimum-variance-portfolio` (AP2) | M7 and AP2 | L01-L02 | Not a DAG error (different IDs). Resolution: AP2 links M7 for the computation and defines the three objects. Architect decision (§12 Q5). |
| D12 | `simple-return`, `log-return` (CS1, in closure, unbuilt) | CS1 | return conventions (§2.1 item 11) | Link via `concepts.html` only. |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Each row needs the architect's confirmation (§12 Q5-Q6).**
`check_dag.py` checks linked uses only (`tools/check_dag.py` docstring, lines 8-10); an unlinked use of D1-D10 passes the tool,
so the verifier reads every lesson and the project for these names (VERIFIER_RULES §2.9).

---

## 5. Project (`project.html`, Builder E): autograder and rubric, ladder, spec, hours, rubric, grader

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py` line 33 requires the order)

1. **Rung 1, worked example** (`lab-AP2-project-1`, SIMULATED): one fully solved, annotated run of the CAPM test on a seeded
   SIMULATED panel of 3 assets and a market series (T = 60): the GMV weights for the three assets, one Jensen regression with
   its alpha, beta and t-statistic, and the SML residual of the one asset. Each step carries a "why" annotation.
2. **Rung 2, completion** (`lab-AP2-project-2`, `class="lab completion"`, SIMULATED): the beta line and the t-statistic line of
   the Jensen regression are replaced by `___` blanks. Graded instantly. Its twin is the completed solution; every page line
   equals the twin line or contains a blank (`tools/run_labs.py` completion rule, lines 77-86).
3. **Rung 3, independent project (graded by autograder and rubric):** (a) the autograded module `capm_tests.py` to the §5.2
   interface, and (b) the memo `report.md`, rubric-graded (§5.5). `lab-AP2-project-3` is the rung-3 check: it prints the
   reference values for the public instance `make_instance(0)` (SIMULATED) to which the student's module must agree.
4. **Rung 4, stretch** (open-ended, not graded): (i) bring-your-own-data: the student downloads a Fama-French style
   portfolio file from its issuer's own site, loads it into the browser, and runs the same suite on the student's own CSV
   (the file never leaves the browser; the program does not embed or redistribute it; §6, BYOD bullet); or (ii) a conditional-beta test
   with the stated conditioning variable as a hypothesis. Both are optional.

### 5.2 Spec (`dl.spec`; `tools/check_projects.py` lines 34-38 require the terms and both grading words)

Terms: Context (2-4 sentences), Inputs, Required outputs, Constraints, Grading (`tools/check_projects.py` `SPEC_TERMS`, line 34).

- **Context.** A portfolio analyst is asked whether the CAPM survives a test on a panel of asset returns. The analyst
  estimates the mean-variance portfolios, runs the time-series and cross-sectional tests, and must say what a failure or a
  success would show, given that the market portfolio is not observed (Roll).
- **Inputs.** (a) A panel generated by `make_instance(seed)` (SIMULATED; §5.6.1): mean returns and a covariance matrix as exact
  `Fraction`s for the mean-variance part; a riskless rate `r_f` as an exact `Fraction`; and T = 60 (or the instance's T)
  periodic simple excess returns for each asset and the market, as floats for the regression part. (b) Optional rung-4 CSV
  (§6, BYOD bullet), with the schema documented on the page and validated by the student's own module.
- **Required outputs.**
  - `capm_tests.py` (student module, name fixed by this plan; §12 Q9) exporting the seven functions of §5.6.2 with the
    signatures given there;
  - `report.md`, a memo of at most two pages with the sections: Data; Mean-variance portfolios; Time-series test; Cross-sectional
    test; Roll critique; Verdict and limits. Every number cites the function that produced it and the rounding rule.
- **Constraints.**
  - Standard library only (`fractions`, `math`, `random`). The same code runs in Pyodide and under local pytest.
  - Exact arithmetic for the mean-variance functions, and for `is_tangency`. Float only where a function's contract says so.
  - Exceptions: `ValueError` only for the named conditions in §5.6.4; any other invalid input may raise any exception or return.
  - The memo's verdict states the test used and the conditioning on which the test is valid (the normal-errors assumption A6
    and the one-period setting), with the claim graded per BLUEPRINT §3.
  - No network. No real data unless the student's own rung-4 file, which never leaves the browser (§6).
- **Grading.** Autograder (dual-mode; `grader/test_project.py`) for `capm_tests.py`; rubric (`rubric-memo`, §5.5) for `report.md`.
  The spec entry names both words: "autograder" and "rubric" (`tools/check_projects.py` `GRADING_WORDS` line 38, `grading_problems`
  lines 41-50).
- **Reading list.** `ol.reading-list` cites the eight curriculum keys (§7.1): `markowitz1952portfolio`, `tobin1958liquidity`,
  `sharpe1964capital`, `lintner1965valuation`, `roll1977critique`, `merton1973intertemporal`, `ross1976arbitrage`,
  `fama1992crosssection`. Nothing else. Counter-evidence keys are cited only after the builder reads their abstracts (§7.1).

### 5.3 Time budget (`<table id="hours">`, sums to 20 h; every row needs a one-line rationale; `tools/check_projects.py` lines 107-120)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One solved SIMULATED panel, annotated line by line |
| Rung 2, completion problem | 2 | Fill the beta line and the t-statistic line, then run the instant check |
| Panel and instrument intake: the instance fields, the rung-4 CSV schema, the validator | 2 | Document the panel fields and units, state the period convention, state the CSV schema |
| `capm_tests.py` implementation and local test runs | 7 | Implement the seven functions in §5.2 and pass the suite on seeds 0-49 locally |
| Memo `report.md` | 4 | Two pages; every number cited with its function and rounding rule |
| Self-assessment against exemplars | 3 | Score the memo with the rubric, then compare with `exemplar-a` and `exemplar-b` |
| **Total** | **20** | Equals `data-hours-project` on the hub |

### 5.4 Pointer

The rubric is §5.5. The ladder and the time budget are checked by `tools/check_projects.py` lines 84-120.

### 5.5 Rubric (`table.rubric#rubric`, `tools/check_projects.py` `rubric_problems`, lines 58-72)

Five criteria. Each criterion is one table row: the criterion name in a `th`, and exactly four `td` cells for levels 4 down to 1
(`tools/check_projects.py` line 65 counts `td` cells). Every level descriptor is observable.

1. **Data and provenance.** Level 4: names the panel source (SIMULATED instance, its seed and its parameters), states the
   period convention and the sample length T, and, if rung 4 was used, names the file's issuer and the rule that it never
   left the browser. Level 1: "uses the data".
2. **Mean-variance and regression computation.** Level 4: states the GMV and tangency formulas used, the rounding rule, and
   which values are exact and which are float with their tolerance. Level 1: "rounds the numbers".
3. **Tests.** Level 4: states the time-series test (α̂, t-statistic, its degrees of freedom and the assumption behind it) and the
   cross-sectional test (slope, intercept, what the estimated line shows), each with its numbers. Level 1: "runs some tests".
4. **Roll critique.** Level 4: states the proxy problem and the exact SML condition from L07, and applies it to the proxy the
   memo uses (says whether that proxy is tangency and how the verdict depends on it). Level 1: "mentions the Roll critique".
5. **Verdict and limits.** Level 4: gives a verdict on the CAPM for the sample, names at least two limits with a direction of
   bias, and states the counter-evidence for each claim graded B or C with its registry key. Level 1: "notes some caveats".

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, excerpts of memos on a SIMULATED instance, each
annotated with the descriptors it meets or misses. Self-assessment form (`section.rubric-self`, `data-rubric="rubric"`,
`data-exemplars="exemplar-a exemplar-b"`, as in M1 and E3). The page shows where the student's scores diverge from the exemplar
scores. **Calibration is done by a dedicated scorer** (ruling 23): an agent that never opens the project page runs a stripping
script (ruling 15) over each exemplar and scores the stripped prose blind by the rubric; scores must match the annotations within
one level per criterion (VERIFIER §2.6).

### 5.6 Grader design (Builder E; autograder for `capm_tests.py`)

#### 5.6.1 Files and instances

`course/modules/AP/AP2/grader/`: `instance.py`, `reference.py` (the full solution; excluded from deployment, BLUEPRINT §7),
`starter.py` (stubs raising `NotImplementedError`), `test_project.py`.

Grader panel on `project.html` (the form of `tools/check_projects.py` lines 122-135; no Atlas path, no `atlas:` key):

```html
<section class="grader-panel" id="grader" data-unit="AP2" data-grader="grader/" data-suite="test_project.py"
         data-support="instance.py" data-solution="capm_tests.py" data-starter="starter.py"></section>
```

`data-packages` is empty (standard library only). This matters: `tools/run_graders.py` imports NumPy at line 35 for its own
runner, but the grader files must not import it (the browser has no NumPy for this unit).

`instance.py`: `make_instance(seed: int) -> dict[str, object]`, deterministic per seed (`random.Random(seed)`), labelled
**SIMULATED** in its docstring. It generates: `n` in {3, 4, 5} assets; an integer matrix `M` with entries in a stated range and
`Σ = M'M + I` (exact, symmetric positive definite, so A1 holds); a mean vector `μ` as exact fractions with `μ` not proportional
to `ι` (A2 guard); a riskless rate `r_f` as an exact fraction below the minimum mean; the tangency denominator non-zero (A4
guard); a condition-number guard (for example the ratio of extreme diagonal entries of `Σ` below a stated bound) so that float
alternatives agree within 1e-9; and a T = 60 panel of simple excess returns for each asset and the market, seeded. Seeds 0-49
must change the answers (which portfolio is tangency, the betas, the alphas), not only the labels (BUILDER_RULES §5.3.1).
Every instance is validated inside the generator; the generator raises on an invalid draw and the test suite never sees one.

`reference.py`: the full solution. It passes every test on seeds 0-49 (`tools/run_graders.py --unit AP2 --seeds 0-49`).
`starter.py`: stubs; the suite must fail on it (`tools/run_graders.py` line 13 and the starter check, lines 162-168).

#### 5.6.2 Student module interface (`capm_tests.py`; frozen by this plan, §12 Q9)

| Function | Contract | Exact or float |
|---|---|---|
| `minimum_variance_weights(cov: list[list[Fraction]]) -> list[Fraction]` | weights summing to 1 minimising `w'Σw` | exact (a float answer within 1e-9 is accepted) |
| `tangency_weights(mu: list[Fraction], cov: list[list[Fraction]], r_f: Fraction) -> list[Fraction]` | weights summing to 1 maximising the Sharpe ratio | exact (float within 1e-9 accepted) |
| `frontier_weights(mu, cov, target: Fraction) -> list[Fraction]` | minimum-variance weights summing to 1 with `μ'w = target` | exact (float within 1e-9 accepted) |
| `is_tangency(mu, cov, r_f, weights) -> bool` | True iff `Σw` is proportional to `μ - r_f ι` with the proportionality constant non-zero, decided in exact arithmetic | **exact, always** |
| `capm_beta(asset: list[Fraction], market: list[Fraction]) -> Fraction` | `Cov(asset, market)/Var(market)` on the same sample (convention cancels) | exact |
| `jensen_regression(asset: list[float], market: list[float]) -> dict[str, float]` | keys `alpha`, `beta`, `se_alpha`, `t_alpha`, `residual_variance`; OLS with `T - 2` degrees of freedom | float, tolerance 1e-9 relative |
| `security_market_line(betas: list[Fraction], mean_excess: list[Fraction]) -> tuple[Fraction, Fraction]` | intercept and slope of the cross-sectional OLS fit (exact normal equations) | exact |

Rounding and presentation rules, stated on the page: exact values are never rounded inside a function; floats are returned at full
precision; the memo rounds at display and states the rule.

#### 5.6.3 Exception table (grader tests demand these, and only these; fixer-rules, PROJECT GRADERS bullet)

| Condition the page names | Exception | Message must name |
|---|---|---|
| `cov` not square, not symmetric, or not positive definite (in the Gauss or Cholesky sense in exact arithmetic) | `ValueError` | "covariance matrix must be square, symmetric and positive definite" |
| `mu` proportional to `ι` (frontier undefined) | `ValueError` | "expected returns must not all be equal" |
| `μ - r_f ι` gives a zero tangency denominator | `ValueError` | "no tangency portfolio: excess returns are not identified" |
| `jensen_regression` or `capm_beta` given fewer than 3 (regression) or 2 (beta) observations, or unequal lengths | `ValueError` | "need matching series of at least three observations" |
| `capm_beta` market variance zero | `ValueError` | "market variance must be positive" |
| `security_market_line` with all betas equal | `ValueError` | "betas must not all be equal" |

Any other invalid input may raise any exception or return. The test suite demands `ValueError` only for the rows above.
Each row has its own isolated test in both directions: the condition raises, and the nearest valid input does not raise
(fixer-rules, PROJECT GRADERS bullet; ruling 9).

#### 5.6.4 Test suite (`test_project.py`)

Properties and numbers. Each test recomputes its expectation with an oracle written separately from `reference.py`
(for example the closed-form `w_GMV`, the direct Sharpe maximisation over a grid for tangency on a 2-asset sub-case, and the
normal-equation solve for OLS). Tests must not pass a hard-coded answer.

- GMV: weights sum to 1 exactly; `Σ w ∝ ι` exactly (stationarity); the variance is no larger than at 200 seeded feasible
  portfolios (sampling check, deterministic).
- Tangency: `is_tangency` is True for the function's output, and False for one coordinate perturbed by 1/1000 (exact);
  Sharpe ratio no smaller than at 200 seeded portfolios; sum to 1.
- Frontier: mean equals the target exactly; the variance equals the closed form `(A·t² - 2B·t + C)/D` at the target `t`
  (oracle); two frontier points combined linearly reproduce a third (two-fund separation, exact or within 1e-9).
- Beta: `capm_beta(asset, c·market) = capm_beta(asset, market)/c` for c > 0 (property; exact); equals the covariance ratio
  written from scratch (oracle).
- Jensen: `alpha`, `beta` equal the normal-equation solve to 1e-9 relative (oracle); `t_alpha = alpha/se_alpha`; `se_alpha` is
  positive and finite; permuting the observations jointly does not change the output; the output for a series built with
  `alpha = 0` by construction is within 4 standard errors (count threshold on seeds 0-49, §12 Q11).
- SML: on a constructed exact linear data set (`mean = a + b·beta`), the function returns `(a, b)` exactly; on random data,
  the intercept and slope satisfy the normal equations exactly.
- `is_tangency`: decides in exact arithmetic (a test where a float decision would fail is supplied by the instance guard).
- Named conditions: §5.6.3, one isolated test each, both directions.
- Output types: exact functions return `Fraction` (or float within tolerance per §5.6.2); `is_tangency` returns `bool`.
- Failure messages name the violated property and hint at the concept ("stationarity fails: check the sign of the multiplier
  term"); they never print the expected value (`__tracebackhide__ = True` in each helper; fixer-rules, PROJECT GRADERS bullet).
- Each test under 5 s in Pyodide and the whole suite under 60 s (`tools/run_graders.py` line 40, `SUITE_LIMIT_S`); the
  collect-only count is quoted on the page and updated when the suite changes (fixer-rules, PROJECT GRADERS bullet).

#### 5.6.5 Student-error mutants (ten, written by the verifier to `ledgers/AP2/mutants/*.py`; each docstring's first line names the error)

Each is a single-change copy of `reference.py`. `tools/mutate_graders.py` reads `ledgers/AP2/mutants/*.py` (line 41) and needs at least
three (line 42-43); this plan requires ten, and the verifier records each mutant's killing test in the ledger.

1. Tangency uses `Σ(μ - r_f ι)` instead of `Σ^{-1}(μ - r_f ι)` (inverse direction forgotten).
2. Tangency uses `μ` instead of `μ - r_f ι` (riskless rate forgotten).
3. Tangency weights are not scaled to sum to 1 (budget ignored).
4. GMV weights are `Σ^{-1}ι` without normalisation (budget constraint violated).
5. `frontier_weights` ignores the target and returns the GMV weights for every target.
6. CML slope computed with `σ_m²` in place of `σ_m` (variance for standard deviation).
7. `capm_beta` inverted: `Var(market)/Cov(asset, market)`.
8. Jensen regression run on raw returns `r_it` instead of excess returns (riskless rate not subtracted).
9. `t_alpha` uses `se_beta` in the denominator (the wrong standard error).
10. `cov` not checked for positive definiteness: a singular matrix is accepted and no `ValueError` is raised (named condition).

Extra, not counted among the ten (the verifier may add it): a hard-coded answer for seed 0. The suite must kill every mutant
on seeds 0-9 (`tools/mutate_graders.py --unit AP2 --seeds 0-9`). A mutant that survives and violates a stated behaviour must
be killed by a new test (ruling 9); a mutant that differs only where the page states nothing is equivalent and goes to
`ledgers/AP2/equivalent/` with a README proof (ruling 9, ruling 25).

#### 5.6.6 Five alternative correct implementations (must all pass seeds 0-49; ruling 10)

Stored by the verifier under `ledgers/AP2/alternatives/alt_1.py` … `alt_5.py` (not in `grader/`; the verifier archives them per
VERIFIER §3). Each implements all seven functions in §5.6.2 and must pass the whole suite on seeds 0-49:

1. Gauss-Jordan elimination in `Fraction`, with the normal-equation solve for OLS.
2. Cholesky factorisation in `Fraction` (positive definiteness is decided by the Cholesky pivots).
3. Adjugate (cofactor) expansion in `Fraction` for `n` ≤ 5.
4. Float Gaussian elimination with partial pivoting for the weights and the regression, returning floats within 1e-9; `is_tangency` and the
   named-condition checks in `Fraction` (the page states that `is_tangency` is exact).
5. Conjugate-gradient iteration in floats to a residual of 1e-12 for the weights and the regression, with exact `is_tangency`.

A float alternative that is wrong on an exact rule is a mutant, not an alternative (ruling 10). The rule that makes alternatives
4 and 5 valid is stated on the page: `is_tangency` decides in exact arithmetic.

#### 5.6.7 Dual mode and tooling facts

- The identical suite runs in Pyodide (pytest in Pyodide) and locally (`pytest`), under `PYTEST_FLAGS` of `tools/run_graders.py`
  (line 39: `-q -p no:cacheprovider --assert=plain -W error`).
- `tools/run_graders.py` checks that the reference, the starter and the instance generator are clean under `mypy --strict`
  (its docstring, line 12): the grader files must be mypy-strict clean.
- `tools/run_graders.py` skips units whose grading is not autograder or both (lines 137-139); AP2 is `both`, so the grader runs.

---

## 6. Real-data policy (B1-B2 apply)

- **Embedded (redistributable, grant quoted):** `fx_daily`, `fx_monthly`, `ust_daily` (`tools/data_sources.yaml:19-116`;
  `course/assets/data/market/MANIFEST.json`, three datasets). None is an equity return series. **AP2 does not use them by
  default.** The riskless rate for every lab and the grader is a stated hypothetical constant (§12 Q4).
- **Not embedded, and not cleared:** the Kenneth R. French Data Library (`tools/data_sources.yaml:119-131`; checked 2026-10-18) and
  Open Source Asset Pricing (`:132-139`; checked 2026-10-17). The lab sentence (`curriculum/03-markets.yaml:256`) and the brief's
  "open data" (`:259-261`) cannot be met with either.
- **Labs and the graded project: SIMULATED.** Every lab (L05, L06, L08 and the project's rung 1-3 labs) and the grader instances
  generate their returns from a seed, and every figure or table of them is labelled SIMULATED on the page.
- **Honest-pending note** on L05, L08 and the project's data section: "The curriculum names French portfolios for this lab, and
  the library's pages reserve use of their data. No equity-return series is embedded. The lab and the graded project use a
  generated economy labelled SIMULATED." Cited to the DATA_REQUEST in §6, DATA_REQUEST bullet.
- **Bring-your-own-data (rung 4 only).** The student downloads a file from the issuer's own site and loads it in the browser. The
  page documents the CSV schema (date, the asset columns, the market column, the riskless column, the period and the return
  convention) and validates it with the student's `capm_tests.py` and a `validate_csv` helper in the same module. The file never
  leaves the browser (BUILDER_RULES §6.6, last bullet). The program does not embed or redistribute the file, and the page says
  so. No `data-files` attribute on any lab (no embedded file is read).
- **No MANIFEST entry, no `data-files`, no fetch.** Builders do not add a MANIFEST entry or run `tools/fetch_data.py`.
- **DATA_REQUEST (for the architect; the planner names no source or licence from memory):** an equity-return series (monthly or
  daily simple returns for a set of assets and a market series) and a riskless series with its basis, each with its issuer URL,
  the quoted licence sentence, the licence page, and the transform (BUILDER_RULES §6.6, steps 1-5). The BLUEPRINT §5.3 candidates
  are the Fama-French and CRSP-type data; each must be checked before use. Not requested as a source name by the planner.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (verified in `references/references.json`; read by planner)

Each key below is `status: verified`, with `used_by: ["AP2"]`, and its container, volume and issue match the curriculum string
(read from the record fields).

| Key | Record (as read: container, volume, issue, pages, year) | Curriculum string (`curriculum/03-markets.yaml`) | Line in registry | Use in AP2 |
|---|---|---|---|---|
| `markowitz1952portfolio` | The Journal of Finance, 7, 1, 77-91, 1952 | Markowitz (1952), JF 7(1) (`:247`) | `references/references.json:16544` | L01 (paper level); reading list |
| `tobin1958liquidity` | The Review of Economic Studies, 25, 2, 65, 1958 | Tobin (1958), REStud 25(2) (`:248`) | `:21810` | L02 two-fund separation (paper level); reading list |
| `sharpe1964capital` | The Journal of Finance, 19, 3, 425-442, 1964 | Sharpe (1964), JF 19(3) (`:249`) | `:20538` | L04 CAPM (paper level); reading list |
| `lintner1965valuation` | The Review of Economics and Statistics, 47, 1, 13, 1965 | Lintner (1965), REStat 47(1) (`:250`) | `:15635` | L04 CAPM (paper level); reading list |
| `roll1977critique` | Journal of Financial Economics, 4, 2, 129-176, 1977 | Roll (1977), JFE 4(2) (`:251`) | `:19955` | L07 (paper level); reading list |
| `merton1973intertemporal` | Econometrica, 41, 5, 867, 1973 | Merton (1973), Econometrica 41(5) (`:252`) | `:17031` | L09 (paper level); reading list |
| `ross1976arbitrage` | Journal of Economic Theory, 13, 3, 341-360, 1976 | Ross (1976), JET 13(3) (`:253`) | `:20279` | L10 (paper level); reading list |
| `fama1992crosssection` | The Journal of Finance, 47, 2, 427-465, 1992; authors FAMA, FRENCH | Fama & French (1992), JF 47(2) (`:254`) | `:8489` | L08 (flat SML; B-claim; only after the abstract is read); reading list |

Registry lines: the `"key"` field line numbers are given above (`grep -n '"key": "<key>"' references/references.json`).

Keys in the registry that are used by other units and are relevant. They may be cited under §2.1 item 3 only after the builder reads
the abstract. Their `used_by` lists do not include AP2; adding AP2 to `used_by` is `add_reference.py`'s job (architect), not a builder's:

- `fama1973risk` (`references/references.json:8336`; Fama & MacBeth 1973, JPE 81(3); `used_by` S5): counter-evidence lead for L08.
- `gibbons1989test` (`:10161`; `used_by` S5): a portfolio-efficiency test; optional for the Roll discussion in L07 (counter-side, read first).
- `jensen1968performance` (`:13470`; JF 23(2); `used_by` F7): optional origin reference for `jensens-alpha` in L06.
- `fama1993common` (`references/references.json`, `used_by` F2): not cited in AP2 (factor model belongs to F2; DAG D6).

Not in the registry (NOT IN CURRICULUM for AP2): a zero-beta CAPM record (no key with that name; grep of `references/references.json`
finds no `black1972*`), and any record for the Gibbons-Ross-Shanken test beyond `gibbons1989test`. These are not cited.

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- R-AP2-1 {doi: null, authors: "lead only: the zero-beta CAPM literature (no author typed)", year: "not typed", title: "zero-beta form of the CAPM, if a zero-beta portfolio is used", venue: "not typed", needed_for: "only if the builder uses a zero-beta form; default: not used (§12 Q8)", confidence: "the need is conditional; no record identified by this planner"}
- R-AP2-2 {doi: null, authors: "lead only: early time-series tests of the CAPM (no author typed)", year: "not typed", title: "time-series tests of the CAPM intercept, counter-evidence to a flat or zero-alpha claim", venue: "not typed", needed_for: "L06 and L08 two-sided treatment of the alpha and flat-SML claims (BUILDER_RULES §2.5)", confidence: "the need is certain; no record identified by this planner"}
- R-AP2-3 {doi: null, authors: "lead only: studies of the sensitivity of CAPM tests to the market proxy (no author typed)", year: "not typed", title: "proxy sensitivity of CAPM tests, the counter-side to the Roll critique", venue: "not typed", needed_for: "L07 counter-evidence for the Roll claim (grade B)", confidence: "the need is certain; no record identified by this planner"}
- R-AP2-4 {doi: null, authors: "lead only: critiques of factor identification in the APT (no author typed)", year: "not typed", title: "identification of the factors in the APT, and the approximate APT", venue: "not typed", needed_for: "L10 counter-evidence and the named limit", confidence: "the need is certain; no record identified by this planner"}
- R-AP2-5 {doi: null, authors: "lead only: the ICAPM state-variable tests (no author typed)", year: "not typed", title: "empirical tests of intertemporal hedging premia", venue: "not typed", needed_for: "L09 two-sided treatment of a grade-B claim about the ICAPM", confidence: "the need is conditional on the L09 claim's grade; no record identified by this planner"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4).
Until resolved, the lessons teach the models with derivations, the empirical claims are grade C at most with the basis named,
or they are removed. The planner recommends that R-AP2-2 and R-AP2-3 be admitted, because L07 and L08 otherwise have no admitted
counter-evidence for their grade-B claims.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for AP2 (`curriculum/curriculum.json` `atlas` array: 20 entries, none with module
AP2; computed). The project has no `atlas:` key (`curriculum/03-markets.yaml:257-263`). `check_projects.py` skips the contract check
when no `atlas` key is present (`tools/check_projects.py` lines 144-146). No `atlas/AP2.contract.md` is needed. The brief's data
wording is B2.

---

## 9. Cards builder (Builder F, after A-D)

- `course/modules/AP/AP2/cards.json`, ids `AP2-c001` upward (gaps and out-of-order ids are not defects: architect ruling 2).
  `lesson` in L01-L10; one card per definition, theorem statement, key formula, key result and misconception (BUILDER_RULES §7).
  `check_pages.py` `check_cards` (lines 366-400) checks the id prefix, the lesson existence, the grades and the registry keys.
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example
  `"basis": "Lab 2, Derivation 2 (exact)"`. Cards for a SIMULATED result name the SIMULATED lab in `basis`.
- Cite a registry key only for an empirical or attributed claim (`cite` is `[]` for a model result). A card for the Roll critique
  cites `roll1977critique` and states the grade-B status with its counter-side key or the REFERENCE_REQUEST topic.
- A card and the key-results row it mirrors carry the same grade and basis (architect ruling 13).

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit AP2            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit AP2
.venv/bin/python tools/check_projects.py --unit AP2
.venv/bin/python tools/run_labs.py --unit AP2               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/AP/AP2/L01.html                          # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/AP/AP2/L02.html --refresh lab-AP2-L02-1  # after editing a twin
.venv/bin/python tools/run_graders.py --unit AP2 --seeds 0-49   # builder E, after reference.py and tests exist
.venv/bin/ruff check tests/labs/AP2 course/modules/AP/AP2/grader && .venv/bin/ruff format --check tests/labs/AP2
.venv/bin/mypy tests/labs/AP2 course/modules/AP/AP2/grader      # strict, repository configuration
```

Verifier only (not run by builders): `.venv/bin/python tools/mutate_graders.py --unit AP2 --seeds 0-9`;
`.venv/bin/python tools/ledger.py --unit AP2 --check` (after fragments exist); `.venv/bin/python tools/page_smoke.py --unit AP2`
(on a quiet machine; timing-sensitive); `.venv/bin/python tools/verify_refs.py --unit AP2` (the unit ledger's run).

Not needed for AP2: `tools/fetch_data.py` (no dataset is added; §6). Repo-wide gates (`check_pages.py --all`, `check_dag.py --all`,
`check_projects.py --all`, `build_site.py --check`, `render_curriculum.py` with `git diff --exit-code`, `verify_refs.py --offline`,
the full CLAUDE.md gate) belong to the architect, once, before any merge.

Flags checked by the planner in the tool sources: `check_pages.py` (`--unit`, `--all`, `--page`), `check_dag.py` (`--unit`, `--all`),
`check_projects.py` (`--unit`, `--all`), `run_labs.py` (`--unit`, `--page`), `run_graders.py` (`--unit`, `--seeds`, default 0-49),
`mutate_graders.py` (`--unit`, `--seeds`). The planner did not execute these builder commands.

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** No `atlas:` key and no Atlas entry names AP2 (`curriculum/03-markets.yaml:257-263`; computed `atlas` array).
   No `atlas/AP2.contract.md` is needed. B2 applies to the brief's wording.
2. **No debate.** AP2 has no `debate:` key (`curriculum/03-markets.yaml:223-263`), so `check_pages.py` does not require a debate
   brief. The CAPM test, the Roll claim and the flat-SML claim are contested anyway: the two-sided rule (BUILDER_RULES §2.5)
   applies.
3. **Grading `both`.** The spec names both words (`tools/check_projects.py` lines 38, 41-50); the grader panel is required
   (lines 122-135); the rubric and two exemplars are required (lines 58-72, 138-139).
4. **Ten lab twins plus three project labs.** The curriculum names one lab (`curriculum/03-markets.yaml:256`). BUILDER_RULES §3.4
   requires a numerical check per key formula; the plan adds one lab per lesson (E3 precedent).
5. **No tool checks the finance formulas.** Nothing in `tools/` checks the GMV, tangency, CML, CAPM, Roll or APT algebra. The labs,
   the grader's oracles and the verifier do (VERIFIER_RULES §2.4-2.5).
6. **`check_dag` sees linked uses only.** Unlinked names of out-of-closure concepts (§4) pass the tool. The verifier reads every
   lesson and the project for them.
7. **Prerequisite pages are not built.** S1, S0, CS1 and P0.1 are unbuilt (computed). Links go to `concepts.html` anchors only.
8. **Mutant and alternative counts are not enforced by a tool beyond three.** `tools/mutate_graders.py` enforces at least three
   (lines 42-43); the ten mutants and the five alternatives are verifier duties recorded in the ledger.
9. **Labs must be exact or stated-precision.** Labs use `Fraction` for the mean-variance parts; the regression part is float and
   states its rounding rule and its tolerance.
10. **The `\indic` macro's tex is `\mathbf{1}`** (`notation/notation.json:33-36`), so the ones vector must be `\iota`. A tool does not
    catch this; the verifier does (VERIFIER §2.4).
11. **The E3 and M7 pages are not the AP2 pages.** The grader panel form, the completion rule and the rubric grammar are copied from
    their structure, not their wording (E5 "imitate structure, not wording").

---

## 12. Open questions for the architect (numbered; each needs a decision before the builders start)

RECOMMENDED decisions are in each item. Where the plan states a recommendation, the builders follow it unless the architect overrides it.

1. **B1, data for the lab and the graded project.** Confirm the default: every lab and the graded project use a generated economy
   labelled SIMULATED; the French library is not embedded (`tools/data_sources.yaml:119-131`); the rung-4 stretch uses BYOD with
   a student download; a DATA_REQUEST is filed (§6, DATA_REQUEST bullet). **RECOMMENDED: confirm.** Alternative: read, quote and add an equity-return
   source to `tools/data_sources.yaml` first (a separate data task).
2. **B2, the curriculum lab sentence.** `curriculum/03-markets.yaml:256` says "Security market line on French portfolios." **RECOMMENDED:**
   keep the lab in L05 on SIMULATED data with an honest-pending note; the architect may amend `:256` to match (a curriculum edit).
3. **B2, the project brief's "open data".** `curriculum/03-markets.yaml:259-261`. **RECOMMENDED:** accept SIMULATED for the graded
   project, with the open-data route as the optional rung-4 stretch; or amend `:259-261` (a curriculum edit).
4. **Riskless rate.** The embedded `ust_daily` `tbill_3m` is on a discount basis (`tools/data_sources.yaml:101-102`). **RECOMMENDED:**
   every lab and the grader use a stated hypothetical constant `r_f` (net, per period); no embedded series is used for AP2. Alternative:
   use `tbill_3m` for `r_f` with a stated basis conversion (a builder would need that conversion checked by the verifier).
5. **D11, overlap with M7.** M7 `mean-variance-optimization` (`curriculum/01-foundations.yaml:314`) is in the closure; AP2 introduces
   `efficient-frontier`, `minimum-variance-portfolio`, `tangency-portfolio` (`curriculum/03-markets.yaml:232-234`). **RECOMMENDED:**
   AP2 defines the three objects and links M7 for the quadratic program; it restates no M7 concept. Confirm, or name a different split.
6. **D1-D10, out-of-closure concepts.** Confirm the defaults in §4: no link, plain prose, no new prerequisite. In particular: `fama-macbeth-regression`
   (S5) and `arbitrage-opportunity` (FC2) are not added as prerequisites. **RECOMMENDED: confirm.** A DAG question for the architect:
   whether AP2 should list S5 (or FC2) as a prerequisite. The planner does not propose it (it would extend the closure and change a
   curriculum prerequisite list).
7. **Lesson count and hours.** **RECOMMENDED: 10 lessons × 7 h = 70 h and a 20 h project (22%)**, with owners A (L01-L03 + index), B (L04-L06),
   C (L07-L08), D (L09-L10), E (project, grader, project labs), F (cards). Alternatives within the rules: 9 × 8 h = 72 h with an 18 h
   project (20%), merging L03 into L02; 9 × 7 h = 63 h with a 27 h project (30%).
8. **Scope.** **RECOMMENDED: confirm** the scope in §2.1 item 4: one period; frictionless; homogeneous beliefs; riskless lending and borrowing
   at one rate; the market portfolio is the tangency portfolio in equilibrium; ICAPM as a two-factor finite-state model under an
   Assumption A7; APT as a finite exact-factor model (A8). No zero-beta CAPM (R-AP2-1 not admitted), no Gibbons-Ross-Shanken test beyond
   the registry record's use, no Newey-West or robust standard errors (S2 not in closure), no continuous time, no transaction costs.
9. **Student module name and interface.** **RECOMMENDED:** `capm_tests.py` with the seven functions and signatures in §5.6.2, frozen before
   building; `is_tangency` exact; floats within 1e-9 accepted for the weights and the regression. Confirm.
10. **Mutant set and alternatives.** **RECOMMENDED: confirm** the ten student-error mutants in §5.6.5 and the five alternatives in §5.6.6.
    The extra seed-0 hard-coded mutant is not counted. Mutants that survive and differ only inside 1e-9 go to `ledgers/AP2/equivalent/`
    with a README (ruling 25).
11. **Count threshold for the alpha test.** The "within 4 standard errors on at least 47 of seeds 0-49" threshold for an `alpha = 0`
    instance (§5.6.4) is a planner proposal, as in E3 §10 Q12. **RECOMMENDED: confirm** or name another threshold.
12. **Hub placement items.** **RECOMMENDED:** `section.quiz#placement` with `data-mastery="0.8"` (the E3 and M1 bar), 13-15 items: two
    `data-skill` items (the GMV computation of the worked example and the beta formula of the completion problem) and at least one item
    for each of the 11 closure modules (CS1, E1, E3, M1, M2, M3, M4, M7, P0.1, S0, S1), as `check_pages.py` requires for the placement
    diagnostic (`tools/check_pages.py` line 351-352; BUILDER_RULES §5.1 "every prerequisite module").
13. **Reference requests.** **RECOMMENDED:** admit R-AP2-2 (time-series counter-evidence) and R-AP2-3 (proxy sensitivity), because L07 and
    L08 have grade-B claims with no admitted counter-side otherwise. Defer R-AP2-1 (zero-beta, not used), R-AP2-4 and R-AP2-5 unless the
    builders need them.
14. **Notation.** **RECOMMENDED: confirm** §2.3: `\iota` for the ones vector (not `\mathbf{1}`, which `\indic` registers); `r_f` for the
    net riskless rate and no `R_f`; `T` only as the sample length; `\SR` for the Sharpe ratio. No NOTATION_REQUESTS.
15. **Figures.** **RECOMMENDED:** no live figures and no new JS kernel (CF1 Q6 and E3 Q5 precedent). Diagrams of the CML and SML are
    inline SVG with `<title>` and `<desc>` if the builder wants them (BUILDER_RULES §6.3); they are not interactive. Confirm.
16. **Adversarial?** **RECOMMENDED: not adversarial** (no question bank; `tools/check_projects.py` requires the bank only when
    `id="question-bank"` is present, line 140-142). The memo is a test report and verdict, not an IC defence or a debate.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 targeted commands once; fixes cross-lesson defects (DAG, links, hours, hub titles, the
   placement item count).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L03 (includes the GMV and tangency labs), L04-L06, L07-L08,
   L09-L10, project (rubric calibration by the dedicated scorer, ruling 23; the ten mutants and the five alternatives; the grader
   suite on seeds 0-49), cards. Failing rows return to the builder that owns the file, with only the failing rows.
3. Ledger at `ledgers/AP2.verification.json`; verifier scripts archived under `ledgers/AP2/scripts/` (VERIFIER §3); mutants under
   `ledgers/AP2/mutants/`; alternatives under `ledgers/AP2/alternatives/`; equivalent mutants with README under `ledgers/AP2/equivalent/`.
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1-B2 must be resolved (or
   named as honest gaps) first.

Architect decisions: pending (§12). This plan is the planner's proposal.

---

## Architect decisions (pending, 2026-11-09). Where the plan states a RECOMMENDED decision for an open question, the builders follow it. Defaults for every module (carried from E5 and E3): concepts outside the prerequisite closure are plain prose with no link and no `<dfn>` `data-concept`; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields or not at all; no real data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every autograder; not adversarial, no question bank. Module specifics for AP2: the lab and project run on SIMULATED data (§6); the riskless rate is a stated constant (§12 Q4); the ones vector is `\iota`; Friedman is not involved; no Atlas.
