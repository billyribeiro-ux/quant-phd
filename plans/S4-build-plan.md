# S4 build plan: Volatility Econometrics (2026-11-09)

Unit: **S4 · Volatility Econometrics** · tier M · 80 h · prerequisite S3 · Atlas milestone **A4** (time-series toolkit) ·
no debate key · grading `autograder` (no rubric) · output directory `course/modules/S/S4/` (part code `S`) · lab twins
`tests/labs/S4/` · ledgers `ledgers/S4/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits. Executors: Haiku builders, then independent
Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every curriculum statement carries `file:line` read during planning. Anything not in the curriculum is
marked **NOT IN CURRICULUM**. Tool facts were checked by reading the tool source or by running `tools/coursekit.py`
(`prerequisite_closure`, `concept_owner`, `built_units`) through `.venv/bin/python`. Binding rules were read in full:
`BLUEPRINT.md`, `BUILDER_RULES.md`, `VERIFIER_RULES.md`, `references/SEED_REPORT.md`, `/Users/billyribeiro/.fanout/fixer-rules.md`,
`plans/FINAL-ARCHITECT-RULINGS.md`. Structure template: `plans/E5-build-plan.md` (sections 0-13). Nearest built prerequisite
(read): `plans/M3-build-plan.md` (M3 is 3 edges from S4: S4→S3→S2→M3; S2's prerequisites are `[S1, M3]`, see `curriculum/01-foundations.yaml`
S2 block), with `plans/M4-build-plan.md` (4 edges: S4→S3→S2→S1→M4) read for the autograder grader design.

**Status: BLOCKING ISSUES EXIST (§0.3).** The hours are feasible. The Atlas contract `atlas/A4.contract.md` does not exist,
so the project cannot pass `check_projects.py` and cannot be built against a frozen interface. The architect must decide
B1-B3 before Builder E starts. Lessons L01-L06 may start once §1 is confirmed.

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| S4 id, title "Volatility Econometrics", tier `M`, hours `80`, prereqs `[S3]` | `curriculum/01-foundations.yaml:738-742` |
| Core: "ARCH, GARCH, EGARCH, realized volatility, HAR, forecast evaluation (QLIKE, MSE)." | `curriculum/01-foundations.yaml:743` |
| `introduces` has 9 concepts, one entry each (volatility-clustering, arch-model, garch-model, egarch-model, leverage-effect, realized-volatility, har-model, qlike-loss, robust-volatility-loss) | `curriculum/01-foundations.yaml:744-753` |
| Sources: six free-text strings (Engle 1982; Bollerslev 1986; Nelson 1991; Andersen, Bollerslev, Diebold & Labys 2003; Corsi 2009; Patton 2011) | `curriculum/01-foundations.yaml:754-760`; Corsi string at `:759` |
| Lab: "GARCH vs. HAR under QLIKE." | `curriculum/01-foundations.yaml:761` |
| Project "Atlas A4: time-series toolkit"; brief "Add ARMA, GARCH, HAR and Kalman estimators to Atlas, with robust loss-function-based forecast evaluation."; deliverable "Atlas at milestone A4."; grading `autograder`; `atlas: A4` | `curriculum/01-foundations.yaml:762-769` (brief `:764-766`, deliverable `:767`, grading `:768`, atlas `:769`) |
| No `debate:` key on S4 | `curriculum/01-foundations.yaml:738-769` (absent) |
| JSON row for S4 mirrors the YAML (hours 80, prereqs S3, 9 concepts, lab, project atlas A4) | `curriculum/curriculum.json:7040` (`"id": "S4"`), `:7073` (`"atlas": "A4"`) |
| Atlas A4 entry: module S4, title "Time-series toolkit", delivers "ARMA, GARCH, HAR and Kalman estimators with forecast-evaluation tests." | `curriculum/meta.yaml:211-213`; `curriculum/curriculum.json:192` (`"id": "A4"`) |
| Atlas entries A1-A20 form a list; no other entry names S4 | `curriculum/meta.yaml:198` (`atlas:`) through the A20 entry at `:275`; A2 entry at `:203-206` (module CS3) |
| S4 is required by the Master's credential | `curriculum/meta.yaml:98`; course map "Financial Econometrics" [S3, S4, S7] at `curriculum/meta.yaml:105` |
| Concepts whose owner is S4 in `curriculum.json` = the same 9 ids | `tools/coursekit.py` `concept_owner()` (planner run) |
| Prerequisite closure of S4 = {CS1, M1, M2, M3, M4, P0.1, S0, S1, S2, S3} (usable concepts = the closure's `introduces`) | `tools/coursekit.py` `prerequisite_closure("S4")` (planner run) |
| Built units inside that closure: M1, M2, M3, M4. Not built: CS1, P0.1, S0, S1, S2, S3 | `tools/coursekit.py` `built_units()` (planner run); `course/modules/S/` contains only `S7` |
| S3 precedes S4 in the build order (topological index S3 = 39, S4 = 52) | `curriculum/curriculum.json` `topological_order` (planner run) |
| S3 entry (prereq of S4): ARMA (`arma-model`), `kalman-filter`, `stationarity`, `markov-switching-model`, and others | `curriculum/01-foundations.yaml:697-721` |
| Built module S7 depends on S1, S2, S3, which are not built | `curriculum/01-foundations.yaml:831-835` (S7 prereqs); `course/modules/S/S7/` exists |
| PR4 (Risk Measurement) lists S4 as a prerequisite; a dependent, no action for S4 | `curriculum/04-quant.yaml:334` (`prereqs: [PR1, S4]`) |

Hours and tool facts (planner-verified): the hub split must equal the curriculum figure (`tools/check_pages.py:338`); the
project share must lie in 10-40% of module hours (`tools/check_pages.py:340`); a lesson declares 6-12 study hours
(`tools/check_pages.py:228`).

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 80 h (`curriculum/01-foundations.yaml:741`). The tool rules:

- lesson `data-hours` 6-12 (`tools/check_pages.py:228`);
- hub `data-hours-lessons + data-hours-project = 80` (`tools/check_pages.py:338`);
- project share 10-40% of 80, i.e. 8 h to 32 h (`tools/check_pages.py:340`);
- lessons sum to the hub's lessons figure (`tools/check_pages.py` `check_hub`).

Chosen split (recommended, Q5): **6 lessons × 9 h = 54 h; project 26 h (32.5%)**. 54 + 26 = 80. Feasible. No STOP on hours.
Alternative within the rules: 5 × 10 h = 50 h with a 30 h project (37.5%).

### 0.3 Blocking issues (architect decision required before the named part is built)

**B1. The Atlas contract does not exist.** `yaml:769` names `atlas: A4`. `atlas/` holds `A1`, `A2`, `A3`, `A5`, `A8`, `A15`
contracts, and no `A4` (`ls atlas/`). `tools/check_projects.py:144-146` fails the project while
`atlas/A4.contract.md` is missing. BUILDER_RULES §5.5 says the builder implements the contract exactly, so Builder E cannot
start. **Plan's default:** the architect's assistant drafts `atlas/A4.contract.md` in the A3 format (`atlas/A3.contract.md`
precedent: proposed by the assistant, PROPOSED, frozen when the module is released). The surface in §5.2 is the proposal.

**B2. Scope of A4 against S4's own content.** `meta.yaml:212-213` and `yaml:765` both name ARMA and Kalman estimators, which
are S3 content (`yaml:708` `arma-model`; `yaml:720` `kalman-filter`). S3 is a prerequisite (closure), so the estimators may be
used, but S4 teaches neither. **Plan's default:** A4 includes ARMA and Kalman as the curriculum states, graded by the same
suite, with the project's time budget (§5.3) reserving hours for them. The architect may instead narrow the milestone.

**B3. Two Atlas and forecast dependencies lie outside the closure.** (a) The Atlas data layer is A2, built in CS3
(`meta.yaml:203-206`, A2 `module: CS3` at `:204`); CS3 is not in the S4 closure (§0.1). (b) "forecast-evaluation tests" (`meta.yaml:213`)
could mean the Diebold–Mariano test, which is S7 (`diebold-mariano-test`, owner S7, outside the closure).
**Plan's default:** A4 takes in-memory series (the A3 pattern, `atlas/A3.contract.md` lines 6-9), needs no A2 store, and
evaluates forecasts by QLIKE and MSE only (no Diebold–Mariano test). The architect confirms both.

Non-blocking, the architect should see them:

- **B4. No intraday price source.** Realized volatility (`yaml:750`) needs intraday prices. No embedded source provides them
  (`tools/data_sources.yaml:18-116` lists only `fx_daily`, `fx_monthly`, `ust_daily`). **Plan's default:** L04 and the HAR
  lab use SIMULATED intraday paths labelled SIMULATED, with an honest-pending note and a DATA_REQUEST (§6).
- **B5. Corsi year conflict.** The curriculum string says "Corsi (2009), Journal of Financial Econometrics 7(2)"
  (`yaml:759`). The registry record `corsi2008simple` has Crossref year 2008, with `notes.year`
  `{"curriculum": "2009", "crossref": "2008"}` (`references/references.json:6010` block). **Plan's default:** cite the key with no year in the prose
  (the E5 B4 precedent); the architect decides whether to correct `yaml:759` (a curriculum change; builders do not edit `curriculum/*.yaml`).

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

6 lessons × 9 h = 54 h; project 26 h; total 80 h. Concept counts per row sum to 2+1+2+1+1+2 = 9, each concept in exactly one
row (`yaml:745-753`).

| Lesson | Title (working) | Concepts it defines (`yaml:745-753`) | Lab (twin id, `tests/labs/S4/`) | Data | Hours | Owner |
|---|---|---|---|---|---|---|
| L01 | Volatility clustering and the ARCH model | `volatility-clustering`, `arch-model` | `lab-S4-L01-1`: sample autocorrelations of raw and squared daily log returns, lags 1-5 | REAL: `fx_daily.csv`, column EUR | 9 | Builder A |
| L02 | The GARCH(1,1) model and its stationarity | `garch-model` | `lab-S4-L02-1`: variance recursion on a seeded path; unconditional variance against the sample variance of a long path | SIMULATED | 9 | Builder A |
| L03 | Asymmetric volatility: EGARCH and the leverage effect | `egarch-model`, `leverage-effect` | `lab-S4-L03-1`: the EGARCH news-impact curve at stated standardized shocks, exact | none (exact closed form) | 9 | Builder B |
| L04 | Realized volatility and microstructure noise | `realized-volatility` | `lab-S4-L04-1`: realized variance at four sampling steps on a seeded noisy intraday path | SIMULATED (B4) | 9 | Builder B |
| L05 | The HAR model of realized volatility | `har-model` | `lab-S4-L05-1`: exact coefficient recovery on a noiseless HAR path; seeded noisy recovery | SIMULATED | 9 | Builder C |
| L06 | Forecast evaluation: QLIKE and robust losses | `qlike-loss`, `robust-volatility-loss` | `lab-S4-L06-1` (**the curriculum lab**, `yaml:761`): GARCH(1,1) and HAR forecasts against a squared-return proxy, out-of-sample QLIKE and MSE | REAL: `fx_daily.csv`, column EUR; the proxy is stated (Q8) | 9 | Builder C |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 54 / 26 | none | none | none | - | Builder A |
| project | Atlas A4 spec, ladder, grader panel, time budget (`autograder`) | none | `lab-S4-project-1` (rung 1), `lab-S4-project-2` (rung 2, `class="lab completion"`), `lab-S4-project-3` (rung 3 check) | SIMULATED instances only | 26 | Builder E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` | none | none | SIMULATED | - | Builder E |
| alternatives | five correct alternative implementations (§5.5) | none | none | none | - | Builder D (after E's suite is frozen) |
| mutants | ten student-error mutants (§5.6), written under `ledgers/S4/mutants/` | none | none | none | - | the independent project verifier (VERIFIER §2.6), from this list |
| cards | `cards.json` from L01-L06 | none | none | - | - | Builder F (after A-E) |

**Owner note (Q6).** Six lessons cannot give "about three lessons per builder" across Builders A-E while keeping the project at
10-40% of 80 h. The allocation above gives two lessons each to A, B and C. Builder A also owns `index.html`. Builder D has no
lesson files and owns the five alternatives. Builder E (the last builder) owns `project.html`, `grader/` and the three project
labs. Builder F owns the cards.

**Ownership rule.** Each builder writes only its lesson files and twins. Builder A writes the hub after its lessons' titles
are fixed by this plan (titles are fixed in this table). Builder E writes `grader/` before Builder D starts the
alternatives. The verifier writes the mutants.

**Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses, §4).**
- L01 uses S3 `stationarity` and `autocorrelation-function` (`yaml:707`), and M4 `variance` and `correlation`.
- L02 uses L01 (`arch-model`, `volatility-clustering`) and S1 `maximum-likelihood-estimation`.
- L03 uses L02 (`garch-model`) and defines `leverage-effect` (in-module, `yaml:749`).
- L04 uses CS1 `log-return` and M4 `variance`. It defines `realized-volatility`.
- L05 uses L04 (`realized-volatility`) and S2 `ols-estimator` (`curriculum/01-foundations.yaml:671`) and `hac-standard-errors` (`:678`); both are IN the closure.
- L06 uses L02 (`garch-model`), L04 and L05 (the forecasts). It defines `qlike-loss` and `robust-volatility-loss`.

Hours check: 6 × 9 = 54 (hub `data-hours-lessons="54"`); project 26 (hub `data-hours-project="26"`); total 80.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to S4)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `VERIFIER_RULES.md` §2 (what will be checked),
`/Users/billyribeiro/.fanout/fixer-rules.md`, `plans/FINAL-ARCHITECT-RULINGS.md`, `plans/E5-build-plan.md` §2, `plans/M3-build-plan.md`
§5 (grader precedent), this file. Study `course/modules/S/S7/` (built, autograder grader panel and lessons) and
`course/templates/`. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) or from unrounded
   floats, and is rounded only at display, with the rule stated. For S4 this covers every variance, log-likelihood, QLIKE value,
   autocorrelation and coefficient. Precedent: E5 §2.1 item 1; fixer-rules line 6.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only what
   the printed numbers show. Precedent: fixer-rules line 7; M1 LESSON_TEXT_DEFECTS.
3. **Attribute nothing unread.** Only the registry keys in §7.1 may be cited. A key is cited at paper level unless the builder has
   read the abstract. A page, table, equation or coefficient is never typed from memory (fixer-rules line 8).
4. **Scope words need a computation.** "every", "all", "always", "never", "any", "same", "drives", "offsets", "exactly",
   "volatility is persistent", "forecasts are better" are used only where a derivation, a finite check or a printed lab number
   computes the claim (fixer-rules line 14). S4 scope (Q16): univariate return series; Gaussian quasi-likelihood for GARCH;
   no multivariate GARCH, no stochastic volatility, no jump model, no Diebold–Mariano test.
5. **Define before use.** Each of the 9 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned lesson,
   and never before it. Terms outside the 9 (log return as a term already owned by CS1 is linked; "long memory", "unconditional
   variance", "news-impact curve", "proxy", "microstructure noise", "sampling frequency") are defined in prose at first use with a
   plain `<dfn>` and no `data-concept` (`tools/check_dag.py` skips a `<dfn>` without `data-concept`, E5 §2.1 item 5).
6. **Assumptions explicit.** Every Theorem, Proposition and Derivation lists numbered Assumptions (A1, A2, ...) before the
   statement. Required: the unconditional-variance result needs \(\omega > 0\), \(\alpha, \beta \ge 0\) and \(\alpha + \beta < 1\)
   (Assumption A1), and its derivation uses only \(\E[r_t^2] = \E[h_t]\), which follows from A4: \(z_t \iid \Normal(0,1)\) and
   independent of the past. The quasi-likelihood statements need A4 where the model is simulated. The plan's assumption labels are
   A1 (parameter constraints), A2 (positivity of variance and of the realized and forecast values), A3 (zero-mean returns, the QLIKE proxy
   of §6), A4 (Gaussian iid innovations, simulated paths only).
   If a result relies on a fact the page assumes without proof, name it as "Assumption", write "Assuming [condition]" in every statement that
   uses it, keep the grade T only conditional on it, and never state it as proved (fixer-rules line 12).
7. **Grader rule.** Applies in full (autograder project; §5). Every named error condition has its own isolated test, in both
   directions of every inequality (fixer-rules line 19; §5.4).
8. **No money.** S4 has no money output. Volatility is a rate of variance per period; the page states the period and the unit
   (daily squared log returns, or per-day realized variance).
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; `<pre>` scrolls inside its own container; escape
   `$` as `\$` inside math (fixer-rules line 14).
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":`
    guard (`tools/run_labs.py`, E5 §2.1 item 10).
11. **Return and volatility units are basis-explicit.** Every return is a log return or a simple return, stated; every
    variance or volatility is stated per day (or per sampling interval) and in squared units. No annualization is used unless a
    derivation on the page states its factor; a factor of \(\sqrt{252}\) is never assumed.
12. **Scope words need a computation.** Restated for S4: "volatility clusters" is backed by a printed autocorrelation of squared returns
    (L01 lab); "HAR beats GARCH" is not claimed beyond the printed out-of-sample table (L06 lab).
13. **Worked values.** A value the page derives by hand in a numbered Example (with its hypotheses) is graded T with the Example as
    basis. A value that appears only in lab output, or that rests on SIMULATED data the page does not derive, is graded C naming
    the lab. A card and the key-results row it mirrors carry the same grade and basis (architect ruling 13).
14. **Two-sided contested claims.** Every B- or C-graded claim names its published counter-evidence. No counter-evidence is in the
    registry for S4 (§7.2 R4). Until admitted, a B- or C-graded claim about GARCH-versus-HAR or about the forecast-evaluation ranking
    is stated as a result of the printed lab numbers only, or removed.
15. **Process words stay out of learner text** (fixer-rules line 14): no "build", "builder", "verifier", "REQUESTS", "unit report".
    Planning references stay out of code comments.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation.
- Concepts: §1 table; `<dfn>` only for the 9 registered concepts plus plain `<dfn>` for other terms. No `<a class="concept">` for
  any concept outside the prerequisite closure (§4 DAG).
- Prerequisite links: `href="../../../concepts.html#<id>"` for closure concepts (CS1, M1-M4, P0.1, S0-S3); `href="Lnn.html#def-<id>"`
  for earlier S4 lessons. A lesson never links a concept defined in a later lesson. No link to an S-part hub page, because
  `course/modules/S/` holds only S7 and the hubs of S0-S3 are not built.
- Labs: code lives once, in `tests/labs/S4/lab-S4-Lnn-1.py` (and `lab-S4-project-1..3.py`). The page carries `@@LAB:<file>@@` and
  `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-S4-<page>-<n>`.
  Standard library only (`math`, `fractions`, `random.Random(seed)`, `statistics`) except where §6 states a file read.
  Seeded RNG only; no network; under 10 s in Pyodide; no warnings (`-W error`).
- Data labels: REAL (embedded snapshot; the lab lists `data-files`), SIMULATED (generated; the label appears on the lab, the
  figure caption if any, and in the cards' `basis`), or exact (no data; closed form). L02, L04, L05 and the project's instances
  are SIMULATED. L01 and L06 are REAL. L03 is exact.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (§2.1 item 15). Banned strings (`tools/check_pages.py:58-74`): TODO, TBD, lorem, "for
  brevity", "details omitted", "beyond the scope", "left as an exercise", "you can add more", "it is important to note",
  "studies show", "experts agree", "it is well known", "obviously", "clearly", and any ellipsis `...` in visible prose.
- Percent changes and growth rates state the base, the direction and the convention (log or simple; per day).
- A finite enumeration is grade C with its basis named, not grade T (M1 L06 precedent).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration (CF1 KNOWN 3 precedent).
- Problem sets: at least 3 problems in each of Mechanics, Proof, Empirical and Research, each with a full worked solution inside
  `<details class="solution">` (BUILDER_RULES §4.2 item 7). Retrieval quiz: 8-15 items with explanations (§4.2 item 9).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10 output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered macros and symbols that S4 must use only with their registered meaning (`notation/notation.json` `macros` and `symbols`):

| Registered item | Registered meaning (locator) | S4 rule |
|---|---|---|
| `T` | number of return observations (periods) in a sample (`notation.json:112-114`, module S1) | Use `T` only for the number of observations. This is the same meaning, so it is allowed. Do not use bare `T` for a time horizon or a test statistic. |
| `\gamma_3`, `\gamma_4` | skewness, kurtosis (`notation.json:121-130`, module M4) | **Do not** use them for the EGARCH asymmetry coefficient. Use `\vartheta` (Q15). |
| `\emgamma` | Euler–Mascheroni constant (`notation.json:105-108`) | Not used. |
| plain `\gamma` | "stays free for risk aversion" (`notation.json:107`), and E3 uses plain gamma for relative risk aversion (`plans/FINAL-ARCHITECT-RULINGS.md:82-83`) | Not used in S4, to keep one meaning per symbol across the program. |
| `\Phi`, `\Phi^{-1}` | standard normal CDF and its inverse (`notation.json:117-120`) | Not used by S4. |
| `\E` (macro) | expectation operator (`notation.json:5-8`) | Use for \(\E[\,\cdot\,]\). |
| `\Var`, `\Cov`, `\Corr` (macros) | variance, covariance, correlation (`notation.json:13-24`) | Use for variance and correlation statements. |
| `\se` (macro) | standard error (`notation.json:101-104`) | Use for OLS standard errors in L05. |
| `\R`, `\N` (macros) | real numbers, natural numbers (`notation.json:25-32`) | Standard. |
| `\Normal`, `\iid`, `\argmax`, `\argmin` (macros) | normal law, iid, argmax, argmin (`notation.json:37-60`) | Use for the Gaussian innovation law, iid assumptions and the MLE. |
| `\tr`, `\diag` (macros) | matrix trace, diagonal matrix (`notation.json:61-68`) | Use only in the Kalman and HAR matrix forms. |
| `\SR`, `\hSR`, `\PSR`, `\DSR`, `\PBO`, `\FWER`, `\FDR`, `\FDP` | registered macros for the Sharpe-ratio and multiple-testing vocabulary (`notation.json:69-100`) | Not used by S4. |
| `R^\ast`, `R^{e\ast}`, `R_f`, `\mathbb{Q}` (AP1) | `notation.json:132-150` | Not used by S4. |

Local symbols (allowed; `notation.json` `about` says conventionally local letters are defined per lesson): \(\omega\), \(\alpha\),
\(\beta\) for the GARCH constant and coefficients (defined in L02, and not redefined); \(h_t\) for conditional variance; \(r_t\) for
a return; \(\varepsilon_t = \sigma_t z_t\) for an innovation with \(z_t \iid \Normal(0,1)\) (defined in L01); \(\mathrm{RV}_t\) for realized
variance (defined in L04); \(\vartheta\) for the EGARCH asymmetry coefficient (defined in L03); \(\phi\) and \(\theta\) for the ARMA
coefficients (defined in the A4 contract, not in a lesson); \(\sigma_w^2\) and \(\sigma_v^2\) for the Kalman process and measurement
variances (they replace the letters `q` and `r`, which carry other meanings in the program). Each symbol is defined where it first
appears and never redefined.

NOTATION_REQUESTS: none. The plan uses the registered macros above and local symbols only.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2): why it matters (at most 120 words), core content, inline
lab, where the canon breaks, misconceptions (at least 3), problem set, key-results table, retrieval quiz (8-15 items). No lesson
has a debate brief (no `debate` key, §0.1).

- **L01** `volatility-clustering`, `arch-model`: the return process \(r_t = \mu + \varepsilon_t\) with \(\varepsilon_t = \sigma_t z_t\);
  the ARCH(1) variance equation \(\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2\) stated as a model (grade T for the model's
  definition); the stationarity condition for ARCH(1) derived (Assumption A1: \(0 \le \alpha < 1\)). Volatility clustering is the
  descriptive fact of positively autocorrelated squared returns; its evidence is the L01 lab (REAL, grade C naming the lab) and
  `engle1982autoregressive` at paper level (grade B; no locator typed). Where the canon breaks: a constant mean, a conditionally
  Gaussian innovation, and one lag.
- **L02** `garch-model`: GARCH(1,1) \(h_t = \omega + \alpha \varepsilon_{t-1}^2 + \beta h_{t-1}\); the unconditional variance
  \(\omega/(1-\alpha-\beta)\) derived under A1 (grade T); the Gaussian quasi-log-likelihood as the estimation objective (grade T as a
  definition; the claim that it is consistent under non-normal innovations is not made, §7.2 R2). `bollerslev1986generalized` at paper
  level. The L02 lab checks the recursion and the unconditional variance on a SIMULATED path (grade C, lab basis).
- **L03** `egarch-model`, `leverage-effect`: the EGARCH log-variance recursion \(\ln h_t = \omega + \beta \ln h_{t-1} + \alpha
  (|z_{t-1}| - \E|z|) + \vartheta z_{t-1}\) stated as a model; \(\E|z|\) for a standard normal is derived by the lesson (a numerical
  check in the lab, never typed from memory); the leverage effect is defined as the asymmetric response \(\vartheta \neq 0\) of
  \(h_t\) to the sign of \(z_{t-1}\) (the definition is in-module). `nelson1991conditional` at paper level. Where the canon breaks: the
  model's sign convention and one lag.
- **L04** `realized-volatility`: \(\mathrm{RV}_t = \sum_j r_{t,j}^2\) over intraday returns (a finite identity, grade T); the sampling
  frequency trade-off stated; microstructure noise described in plain prose with a plain `<dfn>`, no link (D9). `andersen2003modeling`
  at paper level. The lab (SIMULATED path, §6) prints realized variance at four sampling steps. The claims are about the printed
  numbers only; no convergence theorem is stated (D1).
- **L05** `har-model`: the HAR regression \(\mathrm{RV}_t = \beta_0 + \beta_d \mathrm{RV}_{t-1} + \beta_w \overline{\mathrm{RV}}_{t-1:t-5}
  + \beta_m \overline{\mathrm{RV}}_{t-1:t-22} + u_t\) with daily, weekly (5-day mean) and monthly (22-day mean) components all ending at
  \(t-1\) (no same-day information; the window lengths are stated as conventions). OLS by the normal equations (grade T, derivation).
  `corsi2008simple` at paper level, with no year typed (B5). Where the canon breaks: a linear model of a positive series can be
  negative; the design is not a causal claim.
- **L06** `qlike-loss`, `robust-volatility-loss`: QLIKE \(L(\sigma^2, h) = \sigma^2/h - \ln(\sigma^2/h) - 1\) defined, with its
  positivity and its minimum at \(h = \sigma^2\) derived (grade T, Assumption A2: \(\sigma^2, h > 0\)). The robust-loss property is
  defined in the lesson as: a loss whose ranking of forecasts is unchanged when the proxy is replaced by the true variance plus
  zero-mean noise (the lesson states this as its own definition; it is not attributed). Which losses have the property is graded C
  with the L06 lab as basis, or removed. `patton2011volatility` is cited at paper level only: no statement about its content is made
  until its abstract is read (VERIFIER §2.1). The curriculum lab (`lab-S4-L06-1`, REAL, §6) prints the out-of-sample QLIKE and MSE table
  for the two forecasts.

Lesson-level constraints:
- Each lesson's "Where the canon breaks" names at least one model limit and what changes without it.
- No lesson uses a term from outside the closure as a concept (§4). No lesson uses a term from E6 or E8.
- Every key formula gets a numerical check in a lab, a Fraction-exact check, or a derivation (BUILDER_RULES §3.4).

---

## 4. DAG problems (concepts that natural S4 content would use outside the closure)

Prerequisite closure of S4 (computed): **{CS1, M1, M2, M3, M4, P0.1, S0, S1, S2, S3}**. Owners below are from `curriculum.json`
`concepts` (planner check with `concept_owner()`).

| Ref | Concept | Owner (outside closure) | Where natural S4 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `quadratic-variation` (`concept_owner` = SC1) | SC1 | realized variance as an estimator of integrated variance (L04) | Plain prose; L04 defines \(\mathrm{RV}_t\) as a finite sum and states no convergence result. No link. Architect may add SC1 as a prerequisite (a curriculum change). |
| D2 | `diebold-mariano-test` (S7) | S7 | comparing forecast accuracy (L06, A4 "forecast-evaluation tests") | Not used (B3). The lab compares QLIKE and MSE means, with no test. If wanted, S7 must become a prerequisite of S4 (acyclic, since S7 does not depend on S4), a curriculum change. |
| D3 | `conditional-expectation-l2`, `martingale` (M6) | M6 | the conditional variance given the past; martingale-difference innovations (L01-L02) | The conditional variance is defined by the model equation (\(\sigma_t\) is a function of past returns), not by general conditioning. No link. The M4 `conditional-expectation-elementary` (IN) covers the discrete case only. |
| D4 | `value-at-risk`, `expected-shortfall` (PR4) | PR4 | GARCH-based risk forecasts (not in the curriculum's S4 text) | Not used. |
| D5 | `volatility-targeting`, `volatility-managed-portfolio` (PR2) | PR2 | application of forecasts | Not used. |
| D6 | `implied-volatility` (FC2), `volatility-smile` and `local-volatility` (DV2), `variance-risk-premium` (DV5), `rough-volatility` (DV3) | FC2, DV2, DV5, DV3 | context for the volatility literature | Not used. No claim about them is made. |
| D7 | `brownian-motion` (SC1), `geometric-brownian-motion` (SC2), `continuous-time-martingale` (SC1) | SC1, SC2 | the continuous-time setting of realized variance | Not used. Mention, if at all, in plain prose with no link and no claim. |
| D8 | `high-frequency-trading` (MS2), `lob-dynamics` (MS2), `roll-spread-estimator` (MS1) | MS1, MS2 | the source of microstructure noise (L04) | Plain prose, no link, no claim beyond the lab. |
| D9 | `bias-variance-tradeoff` (QR3) | QR3 | forecast-evaluation discussion (L06) | Plain prose, no link. |
| D10 | "long memory" (no concept in the curriculum) | none | the HAR interpretation (L05) | NOT IN CURRICULUM as a concept. Plain `<dfn>` with no `data-concept`, and no claim beyond the fitted coefficients. |

Each row has a resolution, so no DAG_DEFECT blocks the build. `check_dag.py` checks linked uses only (`tools/check_dag.py` docstring);
an unlinked use of D1-D9 passes the tool, so the verifier reads every lesson for these names (VERIFIER §2.9). **The architect confirms
D1, D2 and D7 (Q14).**

Closure concepts S4 is expected to link (all IN, `concepts.html` anchors): `stationarity`, `autocorrelation-function`, `arma-model`,
`kalman-filter`, `maximum-likelihood-estimation`, `mle-asymptotic-normality`, `ols-estimator`, `hac-standard-errors`,
`log-return`, `variance`, `correlation`, `covariance-matrix`, `estimator`, `heavy-tailed-distribution`, `student-t-distribution`.

---

## 5. Project (`project.html`, Builder E): autograder, Atlas A4, ladder, spec, grader, time budget

### 5.1 Ladder (BLUEPRINT §5.1; `check_projects.py` requires the order)

Tier M: rungs 1-2 are minimal (BUILDER_RULES §5.1).

1. **Rung 1, worked example** (`lab-S4-project-1`, SIMULATED): one annotated computation of the GARCH(1,1) variance path for six
   returns from a seeded instance, with the initial variance convention (§5.3) and each step's "why".
2. **Rung 2, completion** (`lab-S4-project-2`, `class="lab completion"`, SIMULATED): the QLIKE line and the HAR weekly-window line
   are blanked (`___`). Graded instantly. Its twin is the completed solution, and every page line equals the twin's line or contains a
   blank (`tools/run_labs.py` docstring). `check_projects.py` requires a completion lab or a quiz.
3. **Rung 3, independent project** (graded by autograder): the Atlas A4 milestone `atlas.timeseries` (§5.2). `lab-S4-project-3` is the
   rung-3 check: it prints the outputs of the reference on the default instance (seed 0), so a student can compare.
4. **Rung 4, stretch** (optional, not graded): an EGARCH estimator in the same module, or a re-run of the HAR fit on the L06 real
   series with the proxy stated (§6). Feeds the student's portfolio.

### 5.2 Spec (`dl.spec`; `check_projects.py` requires the terms context, inputs, required outputs, constraints, grading)

- **Context.** An Atlas maintainer must add a time-series toolkit to the research repository: ARMA and Kalman estimators, the
  GARCH(1,1) estimator and variance path, the HAR regression, and forecast-evaluation losses. Every estimator is tested on its
  own properties.
- **Inputs.** Python sequences of floats only (no file I/O, no network). Return sequences are log returns (stated in the spec).
  Realized-variance sequences are positive. The grader generates them (SIMULATED instances, §5.3). No Atlas dataset store is read
  (B3).
- **Required outputs.** One module, `atlas/timeseries.py` (proposed path, B1), with the functions in §5.2 frozen by
  `atlas/A4.contract.md` (B1). The spec lists the exact signatures, the return types, and every named `ValueError` condition
  (§5.4). A student file for the suite is the module at that path.
- **Constraints.** Standard library only (`data-packages` empty; Q10). Deterministic. Type hints complete. Every function validates
  its inputs and raises `ValueError` for the named conditions only. Nothing prints or writes files. The suite runs in the browser
  (Pyodide) and locally with `pytest`.
- **Grading.** Autograder: the suite `grader/test_project.py` (the spec's grading entry names "autograder"; `check_projects.py` `GRADING_WORDS`,
  `grading_problems`).
- **Reading list.** `ol.reading-list` cites registry keys only: `engle1982autoregressive`, `bollerslev1986generalized`,
  `nelson1991conditional`, `andersen2003modeling`, `corsi2008simple` (no year typed, B5), `patton2011volatility`, and
  `hamilton1994time` (book level, for ARMA and Kalman). Nothing else.

**Proposed frozen interface (for `atlas/A4.contract.md`; the architect drafts and freezes it, B1).** All functions are pure.

| Function | Signature (proposal) | Named `ValueError` conditions (the only ones a test may assert) |
|---|---|---|
| `garch11_variance` | `(returns: Sequence[float], omega: float, alpha: float, beta: float) -> list[float]`; \(h_0\) = the sample variance of `returns` (divisor n), then \(h_t = \omega + \alpha r_{t-1}^2 + \beta h_{t-1}\); output has length n | n < 2; omega <= 0; alpha < 0; beta < 0 |
| `garch11_loglik` | `(returns, omega, alpha, beta) -> float`; \(-\tfrac12 \sum_t [\ln(2\pi) + \ln h_t + r_t^2/h_t]\) (the constant is included) | the same four as `garch11_variance` |
| `garch11_fit` | `(returns: Sequence[float]) -> dict[str, float]` with keys `omega`, `alpha`, `beta`, `loglik`; maximizes the loglik over omega > 0, alpha >= 0, beta >= 0, alpha + beta < 1 | fewer than 50 returns; any non-finite return |
| `har_design` | `(rv: Sequence[float]) -> tuple[list[list[float]], list[float]]`; row for t (from index 22 on) is [1, RV_{t-1}, mean(RV_{t-5..t-1}), mean(RV_{t-22..t-1})], target RV_t | len(rv) < 23; any rv_t <= 0 |
| `har_fit` | `(rv: Sequence[float]) -> list[float]`: OLS coefficients [b0, bd, bw, bm] by the normal equations | len(rv) < 23; any rv_t <= 0; a singular design (for example a constant series) |
| `har_forecast` | `(rv: Sequence[float], t: int, coefs: Sequence[float]) -> float`: the HAR forecast of \(\mathrm{RV}_t\) from `rv[0..t-1]` only, with `coefs` = [b0, bd, bw, bm]; uses the last one, five and 22 values before t | t < 22; t > len(rv) |
| `qlike` | `(realized: float, forecast: float) -> float`; \(x - \ln x - 1\) with \(x = \text{realized}/\text{forecast}\) | realized <= 0; forecast <= 0 |
| `mse_loss` | `(realized: float, forecast: float) -> float`; \((\text{realized} - \text{forecast})^2\) | none named |
| `kalman_local_level_filter` | `(y: Sequence[float], sigma_w2: float, sigma_v2: float) -> list[float]`: filtered level means for the model \(x_t = x_{t-1} + w_t\), \(y_t = x_t + v_t\), with \(w_t \sim \Normal(0,\sigma_w^2)\), \(v_t \sim \Normal(0,\sigma_v^2)\), initial state diffuse as stated in the contract | empty y; sigma_w2 < 0; sigma_v2 <= 0 |
| `arma11_fit` | `(x: Sequence[float]) -> dict[str, float]` with keys `phi`, `theta`, `sigma2`; conditional-sum-of-squares fit under |phi| < 1 and |theta| < 1 (stated) | len(x) < 30 |

The grader checks the exception type only for the named conditions in the table, each in its own isolated test (§5.4).

### 5.3 Time budget (`<table id="hours">`, sums to 26 h; every row needs a one-line rationale)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One six-return GARCH path, annotated line by line |
| Rung 2, completion problem | 2 | Fill two blanks and run the instant check |
| ARMA(1,1) conditional-sum-of-squares fit and its tests | 3 | Implement `arma11_fit` against the S3 content and the stated constraints |
| Kalman local-level filter and its tests | 3 | Implement the predict and update steps and check the known-answer case |
| GARCH(1,1) variance, log-likelihood and fit, with tests | 6 | The recursion, the constant in the loglik, the constrained maximization and the property tests |
| HAR design, OLS fit, with tests | 4 | The window conventions, the normal equations, the exact-recovery test |
| QLIKE and MSE losses, with tests | 3 | Two loss functions and the named positivity conditions |
| Local suite run, Pyodide check and fixes | 3 | Run `pytest` locally and in the browser; fix property failures |
| **Total** | **26** | Equals `data-hours-project` on the hub |

### 5.4 Grader design (Builder E; `grader/`)

Grading is `autograder` only, so there is no rubric and no exemplar (`yaml:768`; `check_projects.py` requires a rubric only for
`rubric` or `both`). The project page carries `section.grader-panel` with `data-unit="S4" data-grader="grader/"
data-suite="test_project.py" data-support="instance.py" data-solution="atlas/timeseries.py" data-starter="starter.py"
data-packages=""` (`check_projects.py:123-135`; `run_graders.py` reads the panel and copies the solution into the workspace). The
`grader/reference.py` file is the full solution and is excluded from deployment (BLUEPRINT §7 lines 400-401; architect
ruling 4 applies once a deploy step exists).

**Named conditions (ruling 19: test only what the page names; each in its own test, both directions).**
- `garch11_variance` and `garch11_loglik`: n = 1 raises, n = 2 passes; omega = 0 raises, omega = 1e-12 passes; alpha = -1e-12 raises,
  alpha = 0 passes; beta = -1e-12 raises, beta = 0 passes. Nothing else is asserted as an exception: parameters with alpha + beta >= 1 are valid
  inputs to the recursion (the page states this).
- `garch11_fit`: 49 returns raise, 50 pass; a NaN return raises.
- `har_design` and `har_fit`: len 22 raises, len 23 passes; rv = 0 raises, rv = 1e-12 passes; a constant series raises in `har_fit`.
- `har_forecast`: t = 21 raises, t = 22 passes; t = len(rv) + 1 raises, t = len(rv) passes.
- `qlike`: realized = 0 raises, realized = 1e-12 passes; forecast = 0 raises, forecast = 1e-12 passes.
- `kalman_local_level_filter`: empty y raises; sigma_w2 = -1e-12 raises, sigma_w2 = 0 passes; sigma_v2 = 0 raises, sigma_v2 = 1e-12 passes.
- `arma11_fit`: len 29 raises, len 30 passes.

**Instances (`grader/instance.py`).** `make_instance(seed: int) -> dict[str, Any]`, deterministic per seed, valid for the spec:
- `returns`: a SIMULATED GARCH(1,1) path with Gaussian innovations, length n drawn from {500, 600, 700}; parameters drawn from a seeded range
  with alpha in [0.05, 0.15], beta in [0.80, 0.92], alpha + beta < 0.95, omega in [1e-6, 5e-6] (all stated in the docstring); the
  true parameters are returned under `true`.
- `rv`: a positive SIMULATED series of length 400 from a HAR recursion with nonnegative coefficients summing to less than one and a positive
  constant (so the path stays positive by construction); the coefficients under `true_har`.
- `kalman_y` (length 300), `sigma_w2`, `sigma_v2`; `arma_x` (length 400, AR(1)/MA(1) SIMULATED). Each block is labelled SIMULATED in the docstring.
- Seeds 0-49 give materially different answers (the parameters change, not only the labels; BUILDER_RULES §5.3).

**Test suite (`grader/test_project.py`).** Properties and numbers with stated tolerances. No test hard-codes an answer.
- Exact recovery (no randomness): on a noiseless HAR recursion from the instance's `true_har`, `har_fit` returns the coefficients within 1e-9.
- GARCH fit feasibility: `omega > 0`, `alpha >= 0`, `beta >= 0`, `alpha + beta < 1` for the returned fit.
- GARCH fit optimality (property, not a sampling band): `loglik` of the fit is at least `garch11_loglik` at the instance's true parameters minus 1e-4.
- Variance recursion: `garch11_variance` satisfies the recursion to 1e-12 relative at every t, and its first value is the sample variance (divisor n).
- Log-likelihood convention: `garch11_loglik` equals the sum formula computed in the test from `garch11_variance` to 1e-9 (the constant is part of the spec).
- Lookahead: changing `returns[t]` leaves `h_t` unchanged (the variance at t depends only on returns before t).
- QLIKE: `qlike(x, x) == 0`; `qlike(x, f) > 0` for f != x; the minimum over f at f = x (grid of 200 values); value equals the closed form to 1e-12.
- MSE: `mse_loss` equals the closed form to 1e-12; symmetric in its arguments.
- Forecast lookahead: `har_forecast(rv, t, coefs)` does not change when `rv[t]` (or any later value) is perturbed; it equals the
  design-row dot product from `har_design` for the same t (checked on the instance).
- HAR windows: the design row for t uses the means of exactly 5 and 22 lagged values ending at t-1 (checked on a designed series whose
  values identify each lag).
- Kalman: with sigma_v2 small and sigma_w2 = 0, the filtered means equal the observations (known-answer case); the update step is checked
  against the closed form for one step.
- Integer and type checks: outputs are floats (or lists of floats), not ints or strings.
- Runtime: each test under 5 s and the whole suite under 60 s in Pyodide (BUILDER_RULES §5.3 item 4; `run_graders.py` `SUITE_LIMIT_S`).

**Feedback.** Failure messages name the violated property and give a hint at the concept. They never print the expected value
(`__tracebackhide__`, fixer-rules line 19).

**Reference and starter.** `grader/reference.py` is the full solution; it must pass every test for seeds 0-49
(`run_graders.py --unit S4 --seeds 0-49`). `grader/starter.py` raises `NotImplementedError` in every function; the suite must fail on it.

### 5.5 Five alternative correct implementations (Builder D; must pass seeds 0-49)

Each is a different style and passes the same property tests. They live in `ledgers/S4/alternatives/alt_1.py` to `alt_5.py` (Q11) and
are run by the verifier, not by `run_graders.py`.

1. `alt_1`: GARCH fit by a self-written Nelder–Mead on an unconstrained reparameterization (logit and log maps into the feasible set).
2. `alt_2`: GARCH fit by a projected coordinate search that keeps every iterate feasible.
3. `alt_3`: HAR by Cholesky factorization of the normal matrix, with explicit forward and back substitution.
4. `alt_4`: QLIKE and MSE written with `math.log` on the difference of logs, and forecast means through a streaming accumulator class.
5. `alt_5`: Kalman filter in the Joseph-form covariance update, with the same initial state convention as the reference.

A float-based alternative that is wrong on a stated exact rule is a mutant, not an alternative (ruling 10). Each alternative must match the
stated conventions exactly (the variance initialization, the window lengths, the constant in the loglik).

### 5.6 Mutants (the verifier writes them under `ledgers/S4/mutants/`; `tools/mutate_graders.py` requires at least three; each must be killed)

Each mutant is a single-change copy of the reference. The first docstring line names the student error. The planner's list is
the verifier's starting list (VERIFIER §2.6); the verifier may add more.

1. `qlike` with the argument inverted: returns \(h/\sigma^2 - \ln(h/\sigma^2) - 1\). Killed by the QLIKE closed-form and asymmetry tests.
2. `qlike` drops the constant \(-1\). Killed by the closed-form value test (to 1e-12).
3. GARCH variance uses the same-day return: \(h_t\) uses \(r_t\) instead of \(r_{t-1}\). Killed by the lookahead test.
4. GARCH initial variance set to zero instead of the sample variance. Killed by the first-value test.
5. `garch11_loglik` omits the \(\ln(2\pi)\) constant. Killed by the loglik convention test.
6. HAR weekly window uses 7 lags instead of 5. Killed by the designed-series window test.
7. HAR design without the intercept. Killed by the exact-recovery test (the true `b0` is nonzero).
8. HAR regresses \(\sqrt{\mathrm{RV}_t}\) on lags of \(\mathrm{RV}\) (volatility, not variance). Killed by the exact-recovery test.
9. `har_forecast` uses `rv[t]`, the day being forecast, as the daily lag (a same-day lookahead). Killed by the forecast lookahead test.
10. Kalman filter skips the measurement update (filtered mean equals predicted mean). Killed by the known-answer and one-step tests.

Any mutant that differs only inside the stated tolerance of a property is an equivalent, not a survivor, and goes to
`ledgers/S4/equivalent/` with a README proof (rulings 9 and 25).

---

## 6. Real-data policy (BUILDER_RULES §6.6; BLUEPRINT §5.3)

- **Embedded and cleared: `fx_daily`.** `tools/data_sources.yaml:18-51`: daily foreign exchange rates, six currencies, USD per unit of
  foreign currency, Board of Governors of the Federal Reserve System. The licence quote and its page are in the yaml (`:23-26`,
  "Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission"; `licence_url`
  `https://www.federalreserve.gov/disclaimer.htm`). The note (`:28-37`) says these are spot rates; a currency position's return also
  earns an interest differential that the series do not contain. The lab says so.
- **Snapshot facts (MANIFEST, read):** `course/assets/data/market/MANIFEST.json`, entry `fx_daily`: file `fx_daily.csv`, key `date`,
  rows 6706, first 2000-01-03, last 2026-09-30, columns AUD, CAD, CHF, EUR, GBP, JPY, retrieved 2026-10-19. The CSV has 6706 rows and a
  non-missing EUR column (planner read; no holes in EUR).
- **Series used:** the EUR column only (`RXI$US_N.B.EU` in the yaml, not inverted, `:48` and `:51`). Log returns between consecutive
  available rows; the convention is stated on the page. Holidays have no row (the yaml note), so a "day" is a business day with a quote.
- **Lab data files.** `data-files="fx_daily.csv"` on `lab-S4-L01-1` and `lab-S4-L06-1` (`section.lab` with `data-runtime="python"`);
  the lab opens `Path("data") / "fx_daily.csv"`. `check_pages.py` requires the name in MANIFEST and on disk (`check_pages.py:162-184`).
  The citation (the MANIFEST `citation` field) and the retrieval date (2026-10-19) are stated in the hypothesis or interpretation and in
  every figure source line (no figure is planned, Q13).
- **Not embedded, no grant found: intraday prices (B4).** No embedded source gives intraday prices. The planner does not name a source or
  a licence from memory. L04 and the HAR lab use a SIMULATED intraday path, labelled SIMULATED, with an honest-pending note: "The curriculum
  defines realized volatility from intraday returns; no redistributable intraday source is embedded yet. This page uses a simulated path
  labelled SIMULATED (BUILDER_RULES §1.7)."
- **Proxy in the real-data lab (Q8).** `lab-S4-L06-1` uses the squared daily log return as the variance proxy for a day, because no
  realized measure is embedded. The proxy is unbiased for the daily variance only under the model's zero-mean assumption (Assumption A3,
  stated); it is noisier than a realized measure. The page states it, and the lab's interpretation names only the printed QLIKE and MSE
  numbers for that proxy and that sample.
- **DATA_REQUESTS** (§7.2 request D1 below): an intraday price series with a quoted redistribution grant.
- **No MANIFEST entry is added by builders.** No dataset is embedded by this plan.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`; grep-checked)

| Key | Record (as read) | Use in S4 |
|---|---|---|
| `engle1982autoregressive` | Engle, "Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation", Econometrica 50(4), DOI 10.2307/1912773; `used_by: ["S4"]` (`references/references.json:8018`); source string matches `yaml:755` | L01 ARCH (paper level); reading list |
| `bollerslev1986generalized` | Bollerslev, "Generalized autoregressive conditional heteroskedasticity", Journal of Econometrics 31(3), DOI 10.1016/0304-4076(86)90063-1; `used_by: ["S4"]` (`references/references.json:3386`); matches `yaml:756` | L02 GARCH (paper level); reading list |
| `nelson1991conditional` | Nelson, "Conditional Heteroskedasticity in Asset Returns: A New Approach", Econometrica 59(2), DOI 10.2307/2938260; `used_by: ["S4"]` (`references/references.json:17928`); matches `yaml:757` | L03 EGARCH (paper level); reading list |
| `andersen2003modeling` | Andersen, Bollerslev, Diebold & Labys, "Modeling and Forecasting Realized Volatility", Econometrica 71(2), DOI 10.1111/1468-0262.00418; four authors; `used_by: ["S4"]` (`references/references.json:544`); matches `yaml:758` | L04 realized volatility; L05 HAR context (paper level); reading list |
| `corsi2008simple` | Corsi, "A Simple Approximate Long-Memory Model of Realized Volatility", Journal of Financial Econometrics 7(2), DOI 10.1093/jjfinec/nbp001; registry year 2008 (`references/references.json:6010`), `notes.year` flags the curriculum's 2009 (`yaml:759`); `used_by: ["S4"]` | L05 HAR (paper level); reading list. **The year is not typed in prose** (B5). |
| `patton2011volatility` | Patton, "Volatility forecast comparison using imperfect volatility proxies", Journal of Econometrics 160(1), DOI 10.1016/j.jeconom.2010.03.034; `used_by: ["S4"]` (`references/references.json:18734`); matches `yaml:760` | L06 QLIKE and robust losses (paper level); reading list |
| `hamilton1994time` | Hamilton, "Time Series Analysis", DOI 10.1515/9780691218632; `used_by: ["S3"]` (`references/references.json:11346`); matches `yaml:723` | Reading list only, book level, for the ARMA and Kalman estimators of A4 (Q2). Not cited for an S4 result. |

Registry keys that exist but are not used by S4: `diebold1995comparing` (`used_by: ["S7"]`; Diebold–Mariano, not used, B3),
`taylor1993discretion` (E7), `mcneil2000estimation` (PR4). None is cited.

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- R1 {doi: null, authors: "realized-variance measurement literature (lead only; not typed)", year: "not typed", title: "realized variance as a measure of integrated variance (original and later papers)", venue: "not typed", needed_for: "L04 attribution of the realized-variance definition and any claim about its accuracy", confidence: "the need is certain; no record is identified by this planner"}
- R2 {doi: null, authors: "quasi-maximum-likelihood literature for GARCH (lead only; not typed)", year: "not typed", title: "consistency of the Gaussian quasi-likelihood under non-normal innovations", venue: "not typed", needed_for: "L02 statement, if the architect wants to claim it; the page does not claim it now", confidence: "the need is certain only if the claim is made"}
- R3 {doi: null, authors: "microstructure-noise literature (lead only; not typed)", year: "not typed", title: "bias of realized variance from market microstructure noise", venue: "not typed", needed_for: "L04 two-sided treatment of the noise claim (BUILDER_RULES §2.5)", confidence: "the need is certain; no record is identified by this planner"}
- R4 {doi: null, authors: "forecast-comparison literature on GARCH and HAR (lead only; not typed)", year: "not typed", title: "empirical comparisons of GARCH-type and realized-measure volatility forecasts, including results against either", venue: "not typed", needed_for: "L06 and the project's reading list: counter-evidence for any B- or C-graded ranking claim (Q17)", confidence: "the need is certain; no record is identified by this planner"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4). Until
resolved, the lessons teach the models with derivations and printed lab numbers, and every empirical sentence is graded C at most with
its basis named, or is removed.

---

## 8. Atlas milestone A4

- **Milestone.** A4 "Time-series toolkit", delivers "ARMA, GARCH, HAR and Kalman estimators with forecast-evaluation tests"
  (`curriculum/meta.yaml:211-213`; `curriculum/curriculum.json:192`). Module S4 (`meta.yaml:212`).
- **Contract.** `atlas/A4.contract.md` does not exist (B1). The proposal in §5.2 is the content to draft; the architect freezes it. The
  contract states: stdlib only; the in-memory input (no A2 store, B3); the exact signatures, error conditions and tolerances.
- **Cumulative suite.** The A1 through A4 suite must stay green on the reference (BUILDER_RULES §5.5 item 3; BLUEPRINT §10). A1 is the
  repository skeleton (`atlas/A1.contract.md` exists; `meta.yaml:` A1 `module: CS1`). A2 and A3 are reused only if the contract names
  them. The proposal names neither (A3 is the in-memory pattern of `atlas/A3.contract.md`).
- **Frozen earlier APIs.** No earlier milestone API is changed (BUILDER_RULES §5.5 item 2). A breaking change goes to
  `CONTRACT_CHANGE_REQUESTS`.
- **Atlas wording (B2).** ARMA and Kalman are included per the curriculum. If the architect narrows A4, `meta.yaml:212-213` and `yaml:765`
  change (a curriculum change; builders do not edit `curriculum/*.yaml`).

---

## 9. Cards builder (Builder F, after A-E)

- `course/modules/S/S4/cards.json`, ids `S4-c001` upward, `lesson` in L01-L06 (each lesson has at least one card; `check_pages.py`
  `check_cards`). One card per definition, theorem statement, key formula, key empirical result (with its grade) and misconception
  (BUILDER_RULES §7).
- Grade T for every derived result, with `"basis"` naming the derivation or the lab that establishes it, for example
  `"basis": "Lab 2, Derivation 1 (exact)"`.
- A card for a SIMULATED result names the SIMULATED lab in `basis`. A card for a REAL-data result names the lab and the snapshot.
- `cite` lists only §7.1 keys, and only where the lesson cites the source at paper level. A card about a paper-level attribution has
  `"grade": "B"` at most unless the lesson grades it otherwise under §2.1 item 3.
- Cards test one fact each, and each back is checkable against the lesson text. No trivia (BUILDER_RULES §7).

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit S4            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit S4
.venv/bin/python tools/check_projects.py --unit S4         # fails on B1 until atlas/A4.contract.md exists
.venv/bin/python tools/run_labs.py --unit S4               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/S/S4/L01.html             # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/S/S4/L02.html --refresh lab-S4-L02-1
.venv/bin/ruff check tests/labs/S4 && .venv/bin/ruff format --check tests/labs/S4
.venv/bin/mypy tests/labs/S4                               # strict, repository configuration
```

Grader checks (Builder E, after `grader/` exists):

```bash
.venv/bin/python tools/run_graders.py --unit S4 --seeds 0-49   # reference passes 50/50; starter fails; mypy strict clean
.venv/bin/python tools/mutate_graders.py --unit S4 --seeds 0-9 # after ledgers/S4/mutants/ holds the ten mutants (verifier)
```

Not run by builders (verifier only, on a quiet machine): `.venv/bin/python tools/page_smoke.py --unit S4`
(timing-sensitive), `.venv/bin/python tools/verify_refs.py --unit S4` (the unit ledger's run, VERIFIER §2.1).
`tools/fetch_data.py --check` is run only if a dataset is added (none in this plan).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`,
and the full gate in CLAUDE.md.

Flag checks: `check_pages.py`, `check_dag.py`, `check_projects.py` and `run_labs.py` accept `--unit`; `embed_labs.py` accepts pages and
`--refresh [LAB_ID ...]`.

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **Atlas contract missing.** `check_projects.py:144-146` fails on `atlas: A4` with no `atlas/A4.contract.md` (B1).
2. **Grader panel.** `check_projects.py:123-135` requires `section.grader-panel` with `data-unit`, `data-grader`, `data-suite`,
   `data-solution`, `data-starter`, and the files `reference.py` and `instance.py` in the grader directory. `instance.py` must define
   `make_instance(seed: int)` (`check_projects.py` instance check).
3. **Grading words.** The spec's grading entry must name "autograder" (`check_projects.py:38`, `GRADING_WORDS`).
4. **Mutant floor.** `mutate_graders.py` fails with fewer than three files in `ledgers/S4/mutants/`. The plan supplies ten.
5. **Solution path.** `run_graders.py` copies the solution to the panel's `data-solution` path in a workspace. The path `atlas/timeseries.py`
   is a workspace path, not a repository file.
6. **`run_graders.py` imports numpy** (`tools/run_graders.py` top-level import). The repository venv has it. The browser grader is
   stdlib only (Q10), so the panel's `data-packages` is empty and the Pyodide run does not need numpy.
7. **No debate.** S4 has no `debate` key, so no debate brief is required (`check_pages.py:412`). The GARCH-versus-HAR and forecast-ranking
   claims are contested, so the two-sided rule (BUILDER_RULES §2.5) applies anyway (§2.1 item 14).
8. **No rubric.** `grading: autograder` only, so no `table.rubric`, no exemplars and no self-assessment are required
   (`check_projects.py:rubric_problems` runs only for `rubric` or `both`).
9. **Lesson hours.** `check_pages.py:228` requires 6-12 h per lesson; 9 h each satisfies it.
10. **check_dag sees linked uses only.** Unlinked uses of D1-D10 (§4) pass the tool; the verifier reads for them.
11. **Prerequisite units unbuilt.** S0, S1, S2, S3, CS1 and P0.1 are not built (`course/modules/`). S7 is built and depends on S1-S3,
    which are not built. The fan-out order should build S3 before S4 (topological index 39 < 52, §0.1). This is an observation about
    the built set, not a defect in S4.
12. **Rung 2 and the completion lab.** Rung-2 blanks follow the program convention (architect ruling 11): the twin is the completed
    solution and the page shows the same program with `___`.

---

## 12. Open questions for the architect (numbered; each with the RECOMMENDED decision)

1. **B1, the Atlas contract.** Draft and freeze `atlas/A4.contract.md` before Builder E starts. **Recommended:** the architect's assistant
   drafts it from §5.2 in the A3 format (`atlas/A3.contract.md`), marked PROPOSED; the architect freezes it.
2. **B2, ARMA and Kalman in A4.** **Recommended:** keep both, as the curriculum states (`meta.yaml:213`, `yaml:765`). S3 is a prerequisite,
   so they may be used; the suite tests them by property, with the hours in §5.3.
3. **B3, data layer and forecast tests.** **Recommended:** A4 takes in-memory series (no A2 store, no CS3 dependency). Forecast evaluation uses
   QLIKE and MSE only. No Diebold–Mariano test (S7 is outside the closure).
4. **B4, intraday data.** **Recommended:** SIMULATED intraday paths for L04 and the HAR lab, with the honest-pending note (§6) and a
   DATA_REQUEST for a redistributable intraday source. No source is named by the planner.
5. **Lesson count and hours.** **Recommended:** 6 lessons × 9 h and a 26 h project (32.5%). Alternative within the rules: 5 × 10 h and a 30 h
   project (37.5%), which merges L04 into L05 (HAR on realized variance).
6. **Builder allocation.** **Recommended:** A: L01, L02, `index.html`; B: L03, L04; C: L05, L06; D: five alternatives (§5.5); E: project,
   grader and project labs; F: cards. The verifier writes the mutants. (Six lessons cannot give three per builder at 80 h, §1.)
7. **Corsi year (B5).** **Recommended:** cite `corsi2008simple` with no year in the prose; the architect decides whether to correct
   `yaml:759` from 2009 to the record's year after checking the article (a curriculum change).
8. **Proxy in the real-data lab.** **Recommended:** the squared daily log return as the proxy, with Assumption A3 stated and the proxy caveat
   on the page (§6). The lab's interpretation names only the printed numbers.
9. **Estimation time in Pyodide.** **Recommended:** the L06 lab fits GARCH in-lab on a stated in-sample window if the builder's timing run is
   under 10 s; otherwise the fitted parameters are precomputed in the twin at build time and the page says so (BUILDER_RULES §6.1).
10. **Grader dependencies.** **Recommended:** stdlib only (`data-packages=""`). S7 uses `numpy` (`course/modules/S/S7/project.html:188`);
    numpy is not needed for these estimators.
11. **Locations.** **Recommended:** mutants under `ledgers/S4/mutants/` (fixed by `mutate_graders.py`); equivalent mutants under
    `ledgers/S4/equivalent/` with a README proof (rulings 9 and 25); alternatives under `ledgers/S4/alternatives/`.
12. **EGARCH and leverage.** **Recommended:** taught in L03 (`egarch-model` at `curriculum/01-foundations.yaml:748`,
    `leverage-effect` at `:749`), not graded in the project (the project brief names GARCH only, `yaml:765`).
13. **Figures.** **Recommended:** no live figures and no new chart kernel (architect default). Lab output is printed text only.
14. **Concept outside the closure (D1, D2, D7).** **Recommended:** plain prose for each (§4). Confirm no prerequisite change.
15. **Notation.** **Recommended:** EGARCH asymmetry `\vartheta`; Kalman variances `\sigma_w^2`, `\sigma_v^2`; `T` used only for the number of
    observations (§2.3); no NOTATION_REQUESTS.
16. **Scope.** **Recommended:** univariate; Gaussian quasi-likelihood for GARCH; no multivariate GARCH, no stochastic volatility, no jumps, no
    Diebold–Mariano test (§2.1 item 4).
17. **Counter-evidence (R4).** **Recommended:** any B- or C-graded GARCH-versus-HAR or ranking claim stays a printed lab result or is removed
    until R4 is admitted (§2.1 item 14).
18. **Build order.** **Recommended:** build S3 (and its prerequisites S0-S2 where they are not built) before S4, following the topological order
    (`curriculum.json` `topological_order`, S3 = 39, S4 = 52). S4's lessons do not depend on S3's text, only on its concepts.
19. **Adversarial?** **Recommended:** not adversarial; no question bank (`check_projects.py` checks a question bank only when present).
20. **Rung 4 stretch.** **Recommended:** optional and ungraded: an EGARCH estimator, or the HAR fit on the L06 series with the proxy stated.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02 (includes the REAL lab `lab-S4-L01-1`), L03-L04, L05-L06 (includes the
   curriculum lab `lab-S4-L06-1`), project (grader, the five alternatives, the ten mutants, Atlas contract conformance). Failing rows return to
   the owning builder, with only the failing rows.
3. Ledger at `ledgers/S4.verification.json`; scripts under `ledgers/S4/scripts/`; mutants under `ledgers/S4/mutants/` (the ten in §5.6 plus any
   the verifier adds; at least three, `mutate_graders.py`); equivalent mutants under `ledgers/S4/equivalent/` with a README.
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1-B3 must be resolved first.
   B4 and B5 may stand as named honest gaps.

Architect decisions: pending (§12). This plan is the planner's proposal.

**Not established by the planner (stated, not assumed):** the body of `S2` and `S3` lesson text (neither is built; only the curriculum
entries were read); the full text of `references/references.json` (grep-checked for the S4 keys only); the Pyodide timing of any lab or
grader (not run); the content of the cited papers (no locator is typed; only the registry records, read as listed).
