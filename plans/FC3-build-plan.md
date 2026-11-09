# FC3 build plan: Market Efficiency: The Evidence Primer (planner output, 2026-11-09)

Unit: **FC3 · Market Efficiency: The Evidence Primer** · tier U · 45 h · prerequisite **AP2** (only; `curriculum/02-economics-finance-core.yaml:436`) · no Atlas milestone · debate key present (`yaml:460`) · grading `both` (autograder for the fund-skill module, rubric for the memo) · output directory `course/modules/FC/FC3/` (part code `FC`) · lab twins `tests/labs/FC3/` · ledger `ledgers/FC3.verification.json`.
Planner: Haiku, plan only. No lesson content, no curriculum edits, no registry edits, no git operations (no commit, no push, no branch change). Executors: Haiku builders, then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every statement about the curriculum cites `file:line` read during planning (JSON locators are `curriculum/curriculum.json` line numbers). Anything not in the curriculum is marked **NOT IN CURRICULUM**. Registry facts cite `references/references.json` line numbers read during planning. Planner-derived statements about tooling cite the tool file and line, or the E5 plan section that read it. Where the planner did not re-read a tool line, the plan says so.

**Status: BLOCKING ISSUES EXIST (§0.3).** The hours are feasible. The direct prerequisite AP2 is not built, and four-lesson structure conflicts with the five-builder split (Q1, Q2). The architect must decide these before the builders start.

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| FC3 id, title "Market Efficiency: The Evidence Primer" | `curriculum/02-economics-finance-core.yaml:432-433`; `curriculum/curriculum.json:7804-7805` |
| Tier `U`, hours `45` | `yaml:434-435`; `curriculum.json:7806-7807` |
| Prereqs `[AP2]` (only) | `yaml:436`; `curriculum.json:7808-7810` |
| Core: "The efficient-markets hypothesis and its forms, the arithmetic of active management, luck vs. skill, the anomalies preview, behavioral explanations." | `yaml:437-439` |
| `introduces` has 7 concepts: `efficient-markets-hypothesis`, `emh-forms`, `joint-hypothesis-problem`, `arithmetic-of-active-management`, `luck-versus-skill`, `anomaly`, `behavioral-explanation` | `yaml:440-447`; `curriculum.json:7812` onward |
| Sources: Fama (1970), JF 25(2); Sharpe (1991), FAJ 47(1); Fama & French (2010), JF 65(5) | `yaml:448-451` |
| Lab: "Sharpe's arithmetic of active management, simulated." | `yaml:452` |
| Project "Fund-skill test"; brief: "Using a simulated fund universe with known skill, show how many funds look skilled by chance, and recover the true skilled set with a bootstrap."; deliverable "Simulation plus memo."; grading `both` | `yaml:453-459` (brief 455-457, deliverable 458, grading 459) |
| Debate: "Are markets efficient? (primer; full debate in AP8 and CAP2)" | `yaml:460`; `curriculum.json:7833` |
| No `atlas:` entry names FC3 (the 20 atlas entries have modules CS1 onward; none is FC3) | `curriculum/curriculum.json` `atlas` array (planner check by script) |
| FC3 is in the Bachelor's credential `requires` and in the Investments course map and the Equity Investments topic | `curriculum/meta.yaml:62-63`, `:78`, `:158` |
| Modules that depend on FC3: BK2 (prereqs `[FC3]`), BK5 (`[FC3, CF1]`), AP8 (`[AP7, FC3]`) | `yaml:1013` and `:1017` (BK2); `yaml:1101` and `:1105` (BK5); `yaml:461` and `:465` (AP8, planner reads `prereqs: [AP7, FC3]` at 03-markets.yaml:465) |
| Topological position: FC3 index 42, AP2 index 34 | `curriculum/curriculum.json:1036` (`topological_order`), entries at 1071 (AP2) and 1079 (FC3) |
| Prerequisite closure of FC3 (computed by the planner by script over `prereqs`): **{AP2, CS1, E1, E3, M1, M2, M3, M4, M7, P0.1, S0, S1}**, 12 modules, all tiers F or U, 162 usable concepts (sum of the closure's `introduces`) | planner computation over `curriculum/curriculum.json` `parts[*].modules[*]` |
| Modules downstream of FC3 (cannot be prerequisites of FC3): AP8, BK2, BK5, CAP0, CAP2 | planner computation (descendant walk over `prereqs`) |
| Data: the curriculum calls the lab and project "simulated"; no real fund-return source is named | `yaml:452`, `yaml:456-457` |

Built status (`course/modules/`): AP2 is **not built** (`course/modules/AP/` holds only `AP1`; no `plans/AP2-build-plan.md`). CS1 is not built (plan exists, `plans/CS1-build-plan.md`). S1 is not built. E1, E3, M1, M2, M7 are built. The FC part holds FC1 and FC2 (built), so FC3 has no directory yet.

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 45 h (`yaml:435`). Tool rules (`tools/check_pages.py`, read by the planner at lines 221-228 and 325-342):

- lesson `data-hours` 6-12 (`check_pages.py:228`);
- hub `data-hours-lessons + data-hours-project = 45` (`check_pages.py:337-338`);
- project share 10-40% of 45, i.e. 4.5 to 18 h (`check_pages.py:339-340`);
- lessons sum to the hub's lessons figure (`check_pages.py:341-342`).

Chosen split: **4 lessons × 8 h = 32 h; project 13 h (28.9%)**. 32 + 13 = 45. Feasible. **No STOP condition on hours.** Alternatives within the rules are in Q1.

### 0.3 Blocking issues (architect decision required before builders start)

**B1. The direct prerequisite AP2 is not built.** FC3's only prerequisite is AP2 (`yaml:436`), and the lessons use CAPM, Jensen's alpha and the one-factor model, all AP2 concepts (`yaml:237`, `:238`, `:241`, `:245`, `:246`). AP2 precedes FC3 in topological order (index 34 vs 42). The bachelor's credential requires both FC3 and AP2 (`meta.yaml:62-63`). Consequence: links to the AP2 concepts go to `concepts.html#<id>` anchors (as E5 did for E1, E5 §0.1 row "E1 is not built"). Whether those anchors exist before AP2 is built is not established by the planner (see Q2).

**B2. The multiple-testing content that the luck-vs-skill lesson needs is in S7, which comes after FC3.** S7 is tier M, hours 100, prereqs `[S1, S2, S3]` (`curriculum/01-foundations.yaml:831-835`), topological index 54 (after FC3 at 42). Adding S7 to FC3's prerequisites would pull S2 and S3 into the closure and reorder the DAG. The default is plain prose with no link (Q3).

**B3. Registry gaps for the natural EMH and mutual-fund content.** Grossman & Stiglitz (1980) is in the review queue with no candidate established identity (`references/review_queue.json:109`; `references/SEED_REPORT.md:31`, "used by E4, AP8"). Malkiel (1995) and Kosowski et al. (2006) have no record in `references/references.json` and no review-queue entry (grep count zero in both files). The registry key `grossman1980takeover` (`references/references.json`, Grossman & Hart 1980, takeover bids) is a different paper and must not be used for the informational-efficiency paradox. These go to `REFERENCE_REQUESTS` (§7.2). They are not blocking if FC3 does not cite them.

**B4. Builder split versus lesson count.** The lesson count (4) cannot give five builders about three lessons each. The default is three builders (A, B, C) and a cards builder F (Q1). This deviates from the task's "A to E" wording and needs architect confirmation.

Non-blocking, the architect should see them:

- **B5. Freshness.** BLUEPRINT §3 requires 2025-2026 contributions in the debate brief (`BLUEPRINT.md:181-183`). The planner identified no 2025-2026 record in the registry for this debate and cannot name one from memory. It is a `REFERENCE_REQUESTS` lead (§7.2), and the verifier must flag it.
- **B6. Sharpe (1991) and Fama (1970) content.** The planner has not read the abstracts of any FC3 source. Every claim that cites them must be checked by the builder against the abstract (BUILDER_RULES §2.6 precedent; VERIFIER §2.1 "Read at least the abstract").

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

4 lessons × 8 h = 32 h; project 13 h; total 45 h. Concept counts per row sum to 2+2+1+2 = 7, each concept in exactly one row (`yaml:440-447`).

| Lesson | Title (working) | Concepts it defines (`introduces`) | Lab (twin id, `tests/labs/FC3/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | The efficient-markets hypothesis and its forms | `efficient-markets-hypothesis`, `emh-forms` | `lab-FC3-L01-1`: a seeded fair-game return series; the conditional mean of next-period return given a past-return rule equals the unconditional mean within a stated Monte Carlo tolerance (SIMULATED) | 8 | Builder A |
| L02 | The joint-hypothesis problem and the arithmetic of active management | `joint-hypothesis-problem`, `arithmetic-of-active-management` | `lab-FC3-L02-1` (**the curriculum lab**, `yaml:452`, SIMULATED): exact `Fraction` arithmetic on a simulated universe; the value-weighted average active return equals the passive return before costs, and falls below it by the cost share after costs | 8 | Builder A |
| L03 | Luck versus skill in fund performance | `luck-versus-skill` | `lab-FC3-L03-1`: N zero-skill funds, the count of one-sided t-statistics above the stated critical value, compared with N times the level, over seeds 0-9 (SIMULATED) | 8 | Builder B |
| L04 | Return anomalies, behavioral explanations and the debate | `anomaly`, `behavioral-explanation` | `lab-FC3-L04-1`: an omitted factor makes a one-factor alpha nonzero exactly; the two-factor alpha is zero (constructed, labelled SIMULATED). **Debate brief** (required, `yaml:460`) lives here | 8 | Builder B |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 32/13 | none | none | - | Builder A (after L01-L02) |
| project | Fund-skill test (`both`, §5) | none | `lab-FC3-project-1` (rung 1), `lab-FC3-project-2` (rung 2, `class="lab completion"`), `lab-FC3-project-3` (rung 3 check) | 13 | Builder C |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` (§5.5) | none | none | (within 13 h) | Builder C |
| cards | `cards.json` from L01-L04 | none | none | - | Builder F (after A-C) |

Builders D and E are not used for FC3 (Q1). The rule that a builder writes only its own files still holds.

Ownership rule: Builder A writes L01, L02 and then the hub (`index.html`). Builder B writes L03 and L04. Builder C writes `project.html`, the grader, the grader panel and the project labs, and does not depend on the lessons' text beyond the concept names.

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses, §4):
- L01 uses only closure concepts (`expectation`, `conditional-expectation-elementary`, `yaml:…` in M4, `curriculum.json` M4 `introduces`) and plain prose for "fair game" and "information set".
- L02 uses L01 (`efficient-markets-hypothesis`, `emh-forms`) and AP2 `capm`, `jensens-alpha`, `linear-factor-model`.
- L03 uses L02 (`arithmetic-of-active-management`, `joint-hypothesis-problem`) and S1 `hypothesis-test`, `p-value`, `t-statistic`, `bootstrap`.
- L04 uses L02 (`joint-hypothesis-problem`) and L03 (`luck-versus-skill`). The words "anomaly" and "behavioral" must not appear as terms in L01-L03 (plain prose before L04 is the same as use before definition).

Hours check: 4 × 8 = 32 (hub `data-hours-lessons="32"`); project 13 (hub `data-hours-project="13"`); 45 total.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to FC3)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, this file, `plans/FC2-build-plan.md` §4-§5 (the built `both` project template in the same part), `plans/E3-build-plan.md` §6 (the built U-tier `both` template in the closure), `plans/E5-build-plan.md` (structure template). Study `course/modules/FC/FC2/` for the layout and the hub and project grammar. `course/templates/` holds the four skeletons (`hub.html`, `lesson.html`, `project.html`, `studio.html`). Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) where the page's claim is exact, and from `float` only where a tolerance is stated. Rounding is stated at display. Precedent: AC4 KNOWN LIMITATION 3, CF1 L01 Remark 5.2, FC2 §5.5.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only what the printed numbers show. Precedent: M1 LESSON_TEXT_DEFECTS. A lab that claims a check must assert it in code; the labs call `main()` at top level and print the values (ruling 18: a lab is a demonstration; no asserts added only to kill mutants).
3. **Attribute nothing unread (fixer rules 8; FINAL ruling 39 for title-only records).** Only the registry keys in §7 may be cited. A key whose abstract the builder has not read is cited at paper level only, with no page, table, equation, coefficient, sample size or date typed from memory. A title-only record is cited for no result (ungraded naming sentence; FINAL ruling 39). Precedent: E3 L07-L08.
4. **Scope words need a computation or a witness.** "every", "all", "always", "never", "any", "only", "same", "drives", "exactly", "markets", "most funds", "most active managers" are used only where a derivation, a finite check or a lab computes the claim, or where the hypothesis states it (fixer rules 9). The FC3 scope statement (Q7): the data are simulated; the market is one factor in the lab and the joint-hypothesis demonstration; costs are the stated cost in the lab only; no real fund data.
5. **Define before use.** Each of the 7 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned lesson and never before it. Terms outside the 7 concepts (fair game, information set, active return, passive return, alpha as a regression intercept, critical value, significance level, bootstrap distribution, cost share) are defined in prose at first use with a plain `<dfn>` and no `data-concept` (`tools/check_dag.py` skips a `<dfn>` without `data-concept`, E5 §2.1 item 5). Terms from §4 that are outside the closure are plain prose or plain `<dfn>` as §4 says.
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation lists its numbered Assumptions (A1, A2, ...) before the statement. Examples the builders must state: the Sharpe arithmetic needs the market portfolio to be the value-weighted average of all managed dollars and a fixed cost schedule; the OLS intercept formula needs T at least 3 and a non-constant factor; the Fama-style bootstrap needs independent residuals across months and the null imposed by construction.
7. **Grader rule (fixer rules 19; FINAL rulings 9, 10, 19, 21, 22, 23, 37).** Applies in full (`both`). See §5.5.
8. **Money.** FC3 has no money output in the grader. Where a cost is shown in a lab, it is a return in decimals (not cents), with its basis stated. If a later edit adds a money output, it is `int` cents (BUILDER_RULES core guardrails).
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own container; no element forces the page wider than 360 px. `page_smoke.py` is the verifier's check. Escape `$` as `\$` inside math (fixer rules 14).
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":` guard (`run_labs.py` runs each twin as `python -I -W error <twin>`, E5 §2.1 item 10; FC2 §5.7).
11. **Return conventions are explicit.** Every return or rate is stated with its unit (monthly decimal or percent per month), its compounding (simple, monthly), and its excess-return basis (over the stated risk-free rate, which the simulated factor is). A value annualized anywhere states the rule.
12. **Process words and planning references never appear in learner text or code comments.** No "build", "builder", "round", "verifier", "REQUESTS", "unit report" (fixer rules 14). A grader docstring names the rule, not the planning ruling.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation or a lab. A B- or C-graded claim names its published counter-evidence (BUILDER_RULES §2.5; ruling 13 for worked values). The debate brief names both sides.
- Concepts: §1 table; `<dfn>` with `data-concept` only for the 7 registered concepts (BUILDER_RULES §4.1). `<a class="concept">` only for closure concepts (§4), with `href="../../../concepts.html#<id>"`, or `href="Lnn.html#def-<id>"` for earlier FC3 lessons. A lesson never links a concept defined in a later lesson.
- Labs: code lives once in `tests/labs/FC3/lab-FC3-Lnn-1.py` (and `lab-FC3-project-1..3.py`). The page carries `@@LAB:<file>@@` and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output (BUILDER_RULES §6.1). Lab ids match `lab-FC3-<page>-<n>`. Standard library only (`fractions`, `math`, `random.Random(seed)`); seeded RNG only; no network; under 10 s in Pyodide; no warnings (`-W error`).
- SIMULATED label: on every lab, figure and project instance that uses generated data (L01, L03, L04's constructed case, L02's universe, the project's worked example and instances). Exact closed-form checks with no generated data are not labelled SIMULATED.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`, `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Banned strings (`tools/check_pages.py` `BANNED`, lines 58-72 as cited in E5 §2.2; re-read by the planner for the first 15 entries): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known", "obviously", "clearly", and any ellipsis `...` outside code.
- Percent and rate statements state the base and the direction (CF1 L07 Misconception 2). The alpha is a monthly decimal; a percent-per-month value is labelled as such.
- A finite enumeration is grade C with its basis named, not grade T (M1 L06).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration (CF1 KNOWN 3).
- Quiz explanations are read against their lesson (CF1 KNOWN 6).
- Debate brief sections are the six of BUILDER_RULES §4.2 item 5: resolution, strongest case for, strongest case against, graded evidence on both sides, state of the literature, what evidence would settle it.
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10 output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols and macros that FC3 must not give a different meaning (`notation/notation.json` `symbols` and `macros`):

| Registered symbol or macro | Registered meaning (locator) | FC3 use and rule |
|---|---|---|
| `T` | number of return observations (periods) in a sample (`notation.json` symbol list, module S1) | **Consistent.** FC3 uses `T` for the number of monthly observations per fund, which is the registered meaning. No other meaning. |
| `\Phi`, `\Phi^{-1}` | standard normal CDF and its inverse (M4) | **Used** for the normal critical value of the one-sided test, written `\Phi^{-1}(1-\eta)` (Q6). Never redefined. |
| `\gamma_3`, `\gamma_4` | skewness and kurtosis (M4) | Not used. |
| `R^\ast`, `R^{e\ast}`, `R_f`, `\mathbb{Q}` | AP1 meanings | Not used (AP1 is outside the closure). |
| `\E` (macro) | expectation operator | Used for expectation of a random quantity. Not used for any other meaning. |
| `\Var`, `\Cov`, `\Corr` (macros) | variance, covariance, correlation | Used with their registered meaning. |
| `\R` (macro) | real numbers | Standard (FINAL ruling 1). `\mathbb{R}` is not written in module pages. |
| `\Prob`, `\N`, `\indic`, `\Normal`, `\iid` (macros) | probability measure, naturals, indicator, normal law, iid | Used only with registered meaning. |

Local symbols (allowed; each defined on the lesson where it first appears and never redefined): `N` number of funds; `i` fund index; `t` month index (lower case, distinct from `T`); `r_{it}` fund excess return; `f_t` factor excess return; `\alpha_i` Jensen's alpha (monthly intercept, AP2 `jensens-alpha`); `\beta_i` factor loading; `\varepsilon_{it}` residual; `\hat\alpha_i`, `\widehat{se}_i` and `\hat t_i` estimates and t-statistic; `\eta` one-sided significance level; `c` a critical value; `B` bootstrap replications; `s` a seed (integer).

NOTATION_REQUESTS: none. The plan uses only local symbols and registered symbols with their registered meaning. Avoid `\beta` for anything other than the loading; avoid `\alpha` for anything other than the intercept (AP2 uses `jensens-alpha` for the same thing, so no second meaning arises).

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2). Mandatory content, by lesson:

- **L01** `efficient-markets-hypothesis`, `emh-forms`: the efficient-markets hypothesis as a statement about what prices reflect (a stated information set), with the fair-game form written as a conditional-expectation condition (`\E[r_{t+1} \mid \mathcal{F}_t] = \E[r_{t+1}]` under the stated expected-return model; assumption A1 names the expected-return model). The three forms (weak, semi-strong, strong) are defined by the information set each one names (grade T as definitions). The paper `fama1970efficient` is cited at paper level for the forms; the builder reads its abstract and grades any empirical sentence C at most unless the abstract supports it. Lab `lab-FC3-L01-1` checks the fair-game property on a seeded series by Monte Carlo (SIMULATED; stated tolerance). Where the canon breaks: the efficiency statement is a joint statement with a return model (point to L02).
- **L02** `joint-hypothesis-problem`, `arithmetic-of-active-management`: the joint-hypothesis problem (a test of efficiency is a test of efficiency together with the expected-return model; the one-factor model is AP2's `capm` and `linear-factor-model`, in closure). The arithmetic of active management (`sharpe1991arithmetic`, FAJ 47(1) 7-9, read at abstract level only): before costs, the market's return equals the asset-weighted average return of the active and passive groups (a derivation, grade T, assumption A2: all managed dollars are in the active or passive group); after costs, the average active return is below the passive return by the cost share (T, derivation). Curriculum lab `lab-FC3-L02-1` is exact `Fraction` arithmetic on a SIMULATED universe. The empirical claim "most active managers underperform" is graded B at most with the counter-evidence named (`fama2010luck`, `barras2010false`, `andrikogiannopoulou2019reassessing`; §7.1).
- **L03** `luck-versus-skill`: the distribution of estimated alphas under zero skill; the one-sided t-test (`hypothesis-test`, `p-value`, `t-statistic` in closure); the expected number of false positives under zero skill is `N \eta` under the normal approximation (grade T given the approximation; Q6). The bootstrap (`bootstrap`, closure S1) as a way to re-draw the null distribution of many t-statistics. The paper `fama2010luck` is cited at paper level for the mutual-fund evidence; `barras2010false` at paper level for the false-discovery approach; both graded B with counter-evidence named. Lab `lab-FC3-L03-1`: N zero-skill funds, count of t above the critical value, compared with `N \eta`; seeds 0-9 printed (SIMULATED). Where the canon breaks: a single-threshold count ignores multiplicity beyond the bootstrap's own threshold; the full multiple-testing treatment is outside FC3 (B2, Q3) and is named in plain prose only.
- **L04** `anomaly`, `behavioral-explanation`: an anomaly is a return pattern that the expected-return model in use does not explain (joint hypothesis from L02). Behavioral versus risk-based explanations are stated as two readings of the same alpha; the risk-based reading is a model claim, the behavioral reading is a claim about mispricing. The lesson cites `jegadeesh1993returns`, `bondt1985stock`, `daniel1998investor`, `barberis1998model` and `shleifer1997limits` at paper level only, graded B at most with counter-evidence; `kahneman1979prospect` is optional at paper level. Lab `lab-FC3-L04-1`: an exact two-factor demonstration (constructed returns with an omitted factor; the one-factor alpha is nonzero, the two-factor alpha is zero; `Fraction`; labelled SIMULATED because the data are constructed). **Debate brief** (`yaml:460`, required by BUILDER_RULES §4.2 item 5): resolution "Are markets efficient?"; strongest case for and against; graded evidence on both sides (`fama2010luck` and `barras2010false` against `andrikogiannopoulou2019reassessing`; `shleifer1997limits` on limits to arbitrage); the state of the literature; what evidence would settle it. Freshness flag B5 applies.

Lesson-level constraints:
- Each lesson's "Where the canon breaks" section names at least one model limit and what changes without it (one factor in L02 and L04; constant expected returns in L01; independent residuals in L03).
- No lesson uses a term from AP8, BK2, BK5, CAP0 or CAP2 (they are downstream, §4). No lesson uses a term from F1-F7, AP6, AP7 as a linked concept (§4).
- No claim about the size of real fund alphas, real anomaly returns, or real persistence numbers appears without a locator the builder has read. The planner has read none of these papers' text; the builder reads each abstract before any sentence cites it.

---

## 4. DAG problems (concepts that natural FC3 content would use outside the closure)

Prerequisite closure of FC3 (computed): **{AP2, CS1, E1, E3, M1, M2, M3, M4, M7, P0.1, S0, S1}**, 162 usable concepts. Closure members relevant to FC3: `capm`, `beta`, `jensens-alpha`, `linear-factor-model` (AP2); `expectation`, `conditional-expectation-elementary` (M4); `hypothesis-test`, `p-value`, `t-statistic`, `bootstrap`, `sharpe-ratio`, `sharpe-ratio-standard-error-iid` (S1); `least-squares-projection` (M3); `expected-utility` (E3). Owners below are from `curriculum/curriculum.json` `concepts` (planner check: owner module of each id). Topological indices are from `curriculum.json:1036`.

| Ref | Concept(s) | Owner (outside closure) and position | Where natural FC3 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `survivorship-bias`, `delisting-bias` | F1 (M, topo 84; `04-quant.yaml:20`) | the fund universe in L03 and the project (funds that closed are missing from a sample) | Plain prose and a limitation sentence in L03 and in the project's "Constraints" (the simulated universe has no delisting). No link, no `dfn` with `data-concept`. |
| D2 | `data-snooping-bias`, `t-stat-hurdle`, `false-discovery-rate`, `expected-maximum-sharpe` | S7 (M, topo 54, prereqs `[S1, S2, S3]`; `01-foundations.yaml:831-835`) | the multiplicity problem in L03 (many funds tested at once) | Plain prose with the phrase "many tests at once"; no link; the bootstrap threshold is the in-closure device. **Missing prerequisite (DAG question Q3).** Adding S7 pulls S2 and S3 into the closure and reorders the DAG. |
| D3 | `bootstrap-skill-test` | AP8 (M, topo 109; downstream of FC3, `yaml:461-465`) | the project's bootstrap | **Forbidden as a link** (AP8 requires FC3, so the link would be circular). The project names the in-closure concept `bootstrap` (S1) only. |
| D4 | `mutual-fund`, `flow-performance-relationship`, `fund-fee-structures`, `berk-green-model`, `active-management-economics`, `efficiently-inefficient-markets`, `indexing-market-effects` | BK2 (U, topo 61; prereqs `[FC3]`, `yaml:1013-1017`), AP8 (downstream) | the fund universe, fees in the arithmetic, the equilibrium reading of active management | **Forbidden as links** (downstream). Plain prose "mutual fund" and "fee" in the lab and project; no `dfn`. |
| D5 | `value-premium`, `size-effect`, `cross-sectional-momentum`, `fama-french-three-factor-model`, `carhart-four-factor-model`, `investment-factor`, `profitability-factor`, `q-factor-model`, `betting-against-beta` | F2 (M, topo 102; `04-quant.yaml:50`) | the "anomalies preview" in L04 | Plain prose that names the anomaly families in one sentence each, with no numbers and no model equations beyond the closure's one-factor model. No link. The families may be cited at paper level by registry key (`fama1993common`, `jegadeesh1993returns`), graded per §7. |
| D6 | `limits-to-arbitrage`, `noise-trader-risk`, `overreaction-underreaction`, `risk-vs-mispricing`, `investor-sentiment-index` | AP6 (D, topo 95; `03-markets.yaml:395`), AP7 (M, topo 96; prereqs `[AP5, E3]`, `03-markets.yaml:427`) | the behavioral-explanation lesson (L04) | Plain prose. The behavioral claims cite paper-level keys (§7.1). The terms are not defined in FC3. |
| D7 | `arbitrage-opportunity`, `cost-of-carry-forward-price` | FC2 (U, topo 30, built; `02-economics-finance-core.yaml:396`; prereqs `[M4, CF1, FC1]`) | "no arbitrage" in the fair-game and limits-to-arbitrage sentences (L01, L04) | **Missing prerequisite (DAG question Q4).** Default: a plain `<dfn>` for "arbitrage" with no `data-concept` (E5 precedent for terms outside the concept list). Adding FC2 pulls CF1 and FC1 into the closure. |
| D8 | `martingale`, `martingale-convergence-theorem`, `stochastic-discount-factor` | M6 (M, topo 20; prereqs `[M4, M5]`, `01-foundations.yaml:262`); AP1 (M) | the martingale form of the fair-game property (L01) | Not used. The fair-game property is stated with conditional expectation (closure, M4), and the word "martingale" is not used. |
| D9 | `look-ahead-bias`, `signal-execution-lag` | QR1 (M, topo 27; prereqs `[CS3, CS4, S0]`, `04-quant.yaml:566`); QR2 | the project's point-in-time check (the factor must not lead the returns) | Plain prose only ("a factor that leads the returns is a look-ahead error"). No link. The grader's mutant m06 (§5.6) is a student error of this kind, named in plain words. |
| D10 | `post-earnings-announcement-drift`, `accruals-anomaly`, `anomaly-net-of-cost`, `anomaly-replication-rate`, `publication-bias`, `factor-zoo`, `post-publication-decay`, `event-study` | AC3 (M, topo 57), AC2 (U, topo 43), MS4 (M), F5 (D, topo 114), F4 (M, topo 122), S6 (M, topo 40) | the anomalies preview and the replication remark in L04 | Not used. If mentioned, plain prose with no number and no claim, and no link. |
| D11 | `expectation` and `conditional-expectation-elementary` | M4 (in closure) | fair-game condition (L01) | Used, linked to `concepts.html#expectation` and `#conditional-expectation-elementary`. Not a DAG issue. |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Q3 and Q4 are the two outside prerequisites the architect may choose to add.** `check_dag.py` checks linked uses only (E5 §4 cites `tools/check_dag.py`); an unlinked use of D1-D10 passes the tool, so the verifier reads every lesson for these names (VERIFIER §2.9).

---

## 5. Project (`project.html`, Builder C): both (autograder and rubric), ladder, spec, interface, grader, rubric

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py` `RUNGS` order, line 33 as cited by FC2 §4.1)

1. **Rung 1, worked example** (`lab-FC3-project-1`, SIMULATED): one fully solved, annotated analysis of a six-fund universe with T = 24 months and one planted skilled fund: the OLS intercept and its t-statistic per fund, the naive count, the expected count `N \eta`, and the bootstrap threshold for one seed. A "why" annotation at every step. Full length (tier U).
2. **Rung 2, completion** (`lab-FC3-project-2`, `class="lab completion"`, SIMULATED): the same analysis with the bootstrap threshold line and the naive-count line replaced by `___`. Graded instantly. The twin is the completed solution; every page line equals the twin line or contains a blank (the completion rule as in FC2 §4.1 and E5 §5.1 item 2).
3. **Rung 3, independent project** (graded, `both`): (a) the autograded module `fund_skill.py` to the §5.3 interface; (b) the memo `memo.md`, rubric-graded (§5.4). `lab-FC3-project-3` is the rung-3 check: it calls the reference `fund_skill` on a fixed SIMULATED instance (seed 0 of the generator) and prints the table the student's memo must reproduce.
4. **Rung 4, stretch** (optional, not graded): the power of the naive count and the bootstrap as the number of planted funds falls from 5 to 1, with the expected detection rule stated as a hypothesis before it is run; or a second generator with a factor that leads the returns, to show how the look-ahead error inflates the count (D9).

### 5.2 Spec (`dl.spec`; `tools/check_projects.py` lines 34-49 as cited by FC2 §4.2; re-read by the planner, the constant `SPEC_TERMS` and `GRADING_WORDS` are at lines 33-38)

Terms present (in this order, with these words): **Context**, **Inputs**, **Required outputs**, **Constraints**, **Grading**. The grading entry must name **both** the autograder and the rubric (`GRADING_WORDS["both"] = ("autograd", "rubric")`, `check_projects.py:38`).

- **Context.** A portfolio committee has 40 funds with five-year monthly records and asks which managers show skill rather than luck. The committee's analyst must count the funds that look skilled by chance, then recover the set that the bootstrap says is skilled, and explain each difference from the planted truth.
- **Inputs.** A SIMULATED universe from `make_instance(seed)` (§5.5). Its keys: `returns` (a list of N lists of T monthly excess returns of each fund, decimal), `factor` (T monthly excess returns of the market factor, decimal), `planted_skill` (sorted list of fund indices with a planted positive alpha), `planted_alpha` (monthly decimal alpha of each fund, zero for non-skilled funds). Labelled **SIMULATED** on the page. Every number on the page is computed from these.
- **Required outputs.** `fund_skill.py` with the four functions in §5.3, and `memo.md` (the memo, §5.4).
- **Constraints.** Standard library only; the same code runs in Pyodide and under local pytest; each function is deterministic given its inputs and, for the bootstrap, its seed. Invalid input raises the exception types in §5.3 only (FINAL ruling 19 and fixer rules 19: the grader demands only the conditions the page names). The memo states the critical-value convention (normal, §Q6) and the seed used.
- **Grading.** Autograder (`grader/test_project.py`, dual mode) and rubric (`memo.md`, §5.4). Both words appear in the spec's grading entry.
- **Reading list.** `ol.reading-list`: `fama2010luck` (mutual-fund luck), `barras2010false` (false discoveries in mutual-fund alphas), `sharpe1991arithmetic` (arithmetic of active management), `jensen1968performance` (fund alpha). Registry status in §7.1. Nothing else.

### 5.3 Interface (planner proposal; the architect freezes it, Q5 and Q6)

- `alpha_and_t(returns: list[float], factor: list[float]) -> tuple[float, float]`: the OLS intercept `a` of `returns` on `factor` with an intercept, and its t-statistic `a / se(a)`, where `s^2 = RSS/(T-2)` and `se(a) = s * sqrt(1/T + mean(f)^2 / S_ff)` with `S_ff = sum (f_t - mean(f))^2`. Units: monthly decimal. Raises `ValueError` under the conditions in the exception table.
- `chance_count(t_stats: list[float], critical: float) -> int`: the number of funds with `t > critical` (strict, one-sided). An empty list gives 0. No exception condition is named (empty input is valid).
- `bootstrap_skilled_set(returns: list[list[float]], factor: list[float], level: float, n_boot: int, seed: int) -> list[int]`: the ascending list of fund indices whose observed t-statistic exceeds the `(1-level)` quantile of the bootstrap distribution of the cross-sectional maximum t-statistic (procedure in §5.5, Q5). Raises `ValueError` under the conditions in the exception table.

### 5.4 Exception table (grader tests demand these types, and only these)

| Condition the page names | Exception | Message must name |
|---|---|---|
| `T < 3`, or `len(returns) != len(factor)` (in `alpha_and_t`) | `ValueError` | "need at least 3 months and equal lengths" |
| `factor` constant, so `S_ff = 0` (in `alpha_and_t`) | `ValueError` | "the factor must vary" |
| residual sum of squares is exactly 0 (t-statistic undefined) (in `alpha_and_t`) | `ValueError` | "residuals are zero; the t-statistic is undefined" |
| `level` not in the open interval (0, 1) (in `bootstrap_skilled_set`) | `ValueError` | "level must lie strictly between 0 and 1" |
| `n_boot < 1` (in `bootstrap_skilled_set`) | `ValueError` | "n_boot must be at least 1" |

Any other invalid input may raise any exception or return. The grader's tests do not require a type for those (FINAL ruling 19; fixer rules 19: a TypeError from a correct implementation must pass unless the page says ValueError). The RSS-zero condition (row 3) is an addition by the planner that the builder must write into the page. Without it, the page states nothing about exact fits.

### 5.5 Grader design (Builder C)

Files: `course/modules/FC/FC3/grader/`: `instance.py`, `reference.py` (the solution; excluded from deployment, BLUEPRINT §7 as cited by FC2 §5.5; the repository has no deploy step yet, FINAL ruling 4), `starter.py` (`NotImplementedError` stubs; the suite must fail on it), `test_project.py`.

- **`instance.py`**: `make_instance(seed: int) -> dict[str, object]`. Deterministic from `random.Random(seed)`. N = 40 funds, T = 60 months (planner suggestion; Q7). Factor and residuals are drawn from normal laws with stated parameters. The generator chooses the planted alpha for each skilled fund as at least 4 times the expected standard error, computed in the generator from its own parameters (the standard-error formula of §5.3 evaluated at the generated factor, with the noise standard deviation as a parameter). Every generated instance is valid (T >= 3, non-constant factor, RSS positive). Seeds 0-49 give materially different planted sets and different flagged sets (FINAL ruling 10 and fixer rules 19: the answers change, not only the labels). Labelled **SIMULATED** in the docstring.
- **Bootstrap procedure (Q5, recommended).** (1) Fit each fund by `alpha_and_t`; keep the fitted slope `b_i` and residuals `e_it`. (2) For replication `k = 1..B`, draw T month indices `tau_1..tau_T` uniformly with replacement from `random.Random(seed)` (one shared draw per replication across all funds, so cross-fund dependence is kept). (3) For each fund, form `r*_it = b_i f_t + e_{i, tau_t}` (the null alpha is zero by construction), compute its t-statistic `t*_{ik}` with `alpha_and_t(r*_i, f)`, and record `M*_k = max_i t*_{ik}`. (4) Threshold `c = ` the ceiling-rank `(1-level)` quantile of `M*_1..M*_B` (sorted index `ceil((1-level) B) - 1`, zero-based). (5) Return the ascending list of `i` with observed `t_i > c`. The page states this procedure exactly, so the grader's oracle and the alternatives agree on the threshold rule. The draw order is stated on the page only if the architect rules that the exact flagged set is pinned (Q5); the recommended default does not pin it (see the tests below).
- **`reference.py`**: the full solution. Passes every test on seeds 0-49 (`run_graders.py --unit FC3 --seeds 0-49`).
- **`test_project.py`** (properties and numbers; no hard-coded answers; each test recomputes its expected value by an oracle written apart from `reference.py`, from explicit sums and from the instance's generating parameters):
  - `alpha_and_t` agrees with the closed-form oracle (explicit sums of §5.3) to relative tolerance 1e-9, on every fund of seeds 0-9;
  - exact-zero intercept: a fund `r = f + noise` with noise orthogonal to `f` and zero mean gives `a = 0` (constructed case, tolerance 1e-12);
  - the t-statistic changes sign with the sign of the intercept (both directions of the inequality, hand-built);
  - `chance_count`: equals the hand count on a hand-built list containing a value exactly equal to the critical value (strict inequality: that value is not counted); monotone non-increasing in `critical`; returns 0 for `[]`;
  - `bootstrap_skilled_set`: the output is a subset of `range(N)`, sorted, with no duplicates; superset chain: for levels 0.01 < 0.05 < 0.20 on the same seed, the outputs are nested in that order (the threshold is non-increasing in `level`);
  - planted recovery: every planted fund with planted t >= 4 (by the generator's own parameters) is in the output, for seeds 0-49, at level 0.05;
  - zero-skill false positives: over seeds 0-49, the share of instances with at least one zero-skill fund flagged is at most 0.20 (a fixed deterministic bound; the verifier checks it is not a knife-edge at the chosen seeds);
  - determinism: two calls with the same inputs and seed return the same list; the test includes one instance whose flagged set changes between two seeds, so an unseeded generator is caught;
  - edge cases: one-fund universe (valid); `n_boot = 1` (valid, returns a list);
  - the exception table §5.4: each named condition raises `ValueError` whose message names the condition; no other exception type is required.
  - Failure messages name the violated property and hint at the concept. They never print the expected value or the planted set (fixer rules 19: `__tracebackhide__` on any check that could print an expected value).
- **Dual mode.** The same suite runs in Pyodide and under pytest; each test under 5 s in Pyodide; the suite under 60 s (BUILDER_RULES §5.3 item 4). The bootstrap tests use `n_boot = 200` (Q8).
- **Five alternative correct implementations** (all must pass seeds 0-49; the verifier writes them as test-only fixtures under `ledgers/FC3/scripts/`). Each is correct under the stated rules; none pins the draw order, so exact-set equality across implementations is not tested, only properties and planted recovery (FINAL rulings 10, 21):
  1. closed-form sums for `alpha_and_t` (`S_ff`, `S_fr` by explicit loops), with floats;
  2. Gauss-Jordan normal equations for a two-column design (intercept and factor);
  3. modified Gram-Schmidt QR for the regression, then the same standard-error formula;
  4. bootstrap draws by `rng.randrange(T)` in a loop (a different draw order from any `choices` call; passes the property tests only);
  5. a class-based design (one `FundRecord` object per fund with methods) with the same function outputs.
- **Mutant set**: §5.6, ten student-error mutants, each a single-change copy of the reference under `ledgers/FC3/mutants/`, first docstring line naming the error. The expected killers are the planner's hypotheses; `mutate_graders.py` decides.

### 5.6 Mutants (ten student errors, each must be killed; VERIFIER §2.6 requires at least three)

1. alpha is the raw mean of the fund's return, not the factor-adjusted intercept (kills on a fund with nonzero factor loading; `alpha_and_t` oracle).
2. standard error uses `s^2 = RSS/T` instead of `RSS/(T-2)` (kills on the closed-form oracle at tolerance 1e-9).
3. the naive count uses `|t| > critical` (two-sided) while the page states one-sided (kills on a hand-built negative-t case).
4. the bootstrap resamples raw returns, not residuals, so the null alpha is not imposed (kills on the zero-skill false-positive bound).
5. the threshold uses the `level` quantile instead of the `(1-level)` quantile (kills on the superset chain test).
6. the factor is shifted one month relative to the returns (look-ahead, D9; kills on the exact constructed-fund intercept test).
7. the naive count counts funds with positive alpha rather than significant t (kills on the zero-skill count and the hand-built `chance_count` case).
8. the bootstrap uses an unseeded generator (kills on the determinism test with the flagged-set-sensitive instance).
9. a hard-coded answer: returns the flagged set of seed 0 for any instance (kills on seeds 1-49).
10. the count and the flagged set use `>=` instead of `>` at the threshold (kills on the boundary case `t == critical`, hand-built).

Not counted among the ten: annualization of alpha, equal-weighting of the naive count, a bootstrap with fewer draws. Any of these may be added by the verifier; a surviving one that violates a stated behaviour is a FAIL (FINAL ruling 9); one that differs only where the page says nothing goes to `ledgers/FC3/equivalent/` with a README proof (FINAL ruling 9, 25).

### 5.7 Rubric (`memo.md`; `both` requires it, `tools/check_projects.py` `rubric_problems` lines 58-73, re-read by the planner, the four-level count and the exemplars rule)

Five criteria, four observable levels each (level 4 down to level 1). Every descriptor names something a grader can see:

1. **Naive count reproduced.** Level 4: reports the count of funds with `t > critical`, the critical value and its convention, the level, and the t-statistic of each flagged fund to two decimals from unrounded values, with the rounding rule. Level 1: "lists some funds".
2. **Chance benchmark.** Level 4: states `N \eta` as the expected count under zero skill, states the normal approximation, and compares it with the count among the zero-skill funds from the instance. Level 1: "many funds look skilled".
3. **Bootstrap procedure.** Level 4: states the null imposed, the number of replications, the seed, the draw rule and the threshold quantile convention, so that a reader can rebuild the threshold. Level 1: "uses a bootstrap".
4. **Recovery accuracy.** Level 4: counts false positives and false negatives against the planted set, separately for the naive count and the bootstrap, and says what each error would cost an allocator. Level 1: "the bootstrap works".
5. **Limits and evidence.** Level 4: names the SIMULATED limits (no costs, no delistings, one factor, normal residuals), and for each claim graded B or C names its counter-evidence from the registry keys (§7.1). Level 1: "notes some caveats".

Exemplars: `data-level="4"` and `data-level="2"`, fully written on a SIMULATED instance (seed published), each annotated with the descriptors it meets or misses. Self-assessment form (`section.rubric-self`, `data-rubric="rubric"`, `data-exemplars="exemplar-a exemplar-b"`, as in E5 §5.4 and FC2 §4.6). The page shows where the student's scores diverge from the exemplars' scores. Calibration: a dedicated blind scorer (FINAL ruling 23) scores both exemplars from a stripped copy, within one level per criterion. No question bank: the memo is not an IC defence or a debate (Q9).

### 5.8 Grader panel (`project.html`)

`<section class="grader-panel" id="grader" data-unit="FC3" data-grader="grader/" data-suite="test_project.py" data-support="instance.py" data-solution="fund_skill.py" data-starter="starter.py" data-packages="">`. Standard library only, so `data-packages` is empty. The grader panel must point at `grader/instance.py` defining `make_instance(seed: int)` (`tools/check_projects.py` lines 122-136 as cited by FC2 §4.7, and `check_projects.py:123-128` re-read by the planner). No Atlas path (no milestone; `check_projects.py` lines 144-146 do not apply; B2 analogue: no Atlas entry names FC3).

### 5.9 Time budget (`<table id="hours">`, rows sum to 13; each row needs a one-line rationale)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 1 | One solved six-fund SIMULATED analysis, annotated line by line |
| Rung 2, completion problem | 1 | Fill the bootstrap threshold line and the naive-count line, then run the instant check |
| Derivations: the OLS intercept and its standard error, the expected count, the bootstrap threshold (proofs in §3 and §5.5) | 2 | Write each formula with its assumptions named |
| `fund_skill.py` (four functions, exception table, edge cases, local pytest runs on the student's seed) | 4 | Implement to §5.3 and §5.4; pass the suite on seeds 0-49 |
| Memo `memo.md` (the five rubric criteria) | 3 | Reproduce the counts, state the bootstrap, compare with the planted set, name the limits |
| Self-assessment against exemplars | 2 | Score the memo, then compare with exemplar level 4 and level 2 |
| **Total** | **13** | Equals `data-hours-project` on the hub |

Planner estimate check (VERIFIER §2.6 requires an independent estimate within 30%): the planner's own rough estimate is 12-14 h. The verifier re-estimates.

---

## 6. Real-data policy

- **Embedded:** none for FC3. The embedded snapshots are `fx_daily`, `fx_monthly` and `ust_daily` (`tools/data_sources.yaml:19`, `:53`, `:91`, as read by the planner; E5 §6 read the same file). None is a fund-return or stock-return series, so FC3 uses no embedded data.
- **Not embedded, no grant found:** mutual-fund returns, fund-level alphas, anomaly return series. No entry exists in `tools/data_sources.yaml` for these. **Not requested.** The curriculum names simulated data for the lab (`yaml:452`) and the project (`yaml:456-457`), so no real-data request is raised.
- **SIMULATED label** on every lab, figure and project instance that uses generated data (BUILDER_RULES §1.7).
- **Honest-pending note** on the project data page and on L03: "The curriculum's fund-skill evidence in this primer is simulated. Published fund-level estimates are cited at paper level and are not reproduced here; no redistributable fund-return source is embedded (BUILDER_RULES §6.6)." This is an explicit honest-pending state (FINAL ruling 14 analogue).
- No `data-files` attribute on any lab (no dataset is read). No MANIFEST entry is added by builders. No `DATA_REQUESTS` entry is raised by this plan.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (keys verified in `references/references.json`; each record's fields were read by the planner from the JSON)

| Key | Record (as read) | `references/references.json` line | Use in FC3 |
|---|---|---|---|
| `fama1970efficient` | Fama, "Efficient Capital Markets: A Review of Theory and Empirical Work", JF 25(2) 383, doi 10.2307/2325486, status verified | 8300 | L01 forms of efficiency (paper level; builder reads abstract); curriculum source `yaml:449` |
| `sharpe1991arithmetic` | Sharpe, "The Arithmetic of Active Management", FAJ 47(1) 7-9, doi 10.2469/faj.v47.n1.7, status verified | 20575 | L02 arithmetic (paper level; builder reads abstract); curriculum source `yaml:450`; reading list |
| `fama2010luck` | Fama & French, "Luck versus Skill in the Cross-Section of Mutual Fund Returns", JF 65(5) 1915-1947, doi 10.1111/j.1540-6261.2010.01598.x, status verified | 8650 | L03 mutual-fund evidence (B at most, counter-evidence named); L04 debate; reading list; curriculum source `yaml:451` |
| `barras2010false` | Barras, Scaillet & Wermers, "False Discoveries in Mutual Fund Performance: Measuring Luck in Estimated Alphas", JF 65(1) 179-216, doi 10.1111/j.1540-6261.2009.01527.x | 1758 | L03 false-discovery approach; L04 debate (for side); reading list |
| `andrikogiannopoulou2019reassessing` | Andrikogiannopoulou & Papakonstantinou, "Reassessing False Discoveries in Mutual Fund Performance: Skill, Luck, or Lack of Power?", JF 74(5) 2667-2688, doi 10.1111/jofi.12784 | 765 | L03 and L04 debate (counter-evidence to the strong-luck reading); B at most |
| `jensen1968performance` | Jensen, "The Performance of Mutual Funds in the Period 1945-1964", JF 23(2) 389-416, doi 10.1111/j.1540-6261.1968.tb00815.x | 13470 | L02 and L03: the alpha concept's origin (paper level); reading list |
| `carhart1997persistence` | Carhart, "On Persistence in Mutual Fund Performance", JF 52(1) 57-82, doi 10.1111/j.1540-6261.1997.tb03808.x | 4695 | L03 and L04 debate (persistence evidence) |
| `jegadeesh1993returns` | Jegadeesh & Titman, "Returns to Buying Winners and Selling Losers", JF 48(1) 65-91, doi 10.1111/j.1540-6261.1993.tb04702.x | 13429 | L04 anomalies preview (paper level) |
| `bondt1985stock` | De Bondt & Thaler, "Does the Stock Market Overreact?", JF 40(3) 793-805, doi 10.1111/j.1540-6261.1985.tb05004.x | 3466 | L04 behavioral explanation (paper level) |
| `daniel1998investor` | Daniel, Hirshleifer & Subrahmanyam, "Investor Psychology and Security Market Under- and Overreactions", JF 53(6) 1839-1885, doi 10.1111/0022-1082.00077 | 6422 | L04 behavioral explanation (paper level) |
| `barberis1998model` | Barberis, Shleifer & Vishny (1998), JFE 49(3) (source-string match; the planner did not print the full record) | 1714 | L04 behavioral explanation (paper level); the builder reads the record before use |
| `shleifer1997limits` | Shleifer & Vishny, "The Limits of Arbitrage", JF 52(1) 35-55, doi 10.1111/j.1540-6261.1997.tb03807.x | 20612 | L04 limits to arbitrage (paper level) |
| `berk2004mutual` | Berk & Green, "Mutual Fund Flows and Performance in Rational Markets", JPE 112(6) 1269-1295, doi 10.1086/424739 | 2381 | Optional, L03 (paper level). Its concepts are downstream (D4), so only the key is cited. |
| `fama1991efficient` | Fama, "Efficient Capital Markets: II", JF 46(5) 1575-1617, doi 10.1111/j.1540-6261.1991.tb04636.x | 8452 | Optional, L01 (the later review, paper level) |
| `fama1993common` | Fama & French, "Common risk factors in the returns on stocks and bonds", JFE 33(1) 3-56, doi 10.1016/0304-405x(93)90023-5 | 8530 | Optional, L04 anomalies preview (paper level; D5) |
| `lo2002statistics` | Lo, "The Statistics of Sharpe Ratios", FAJ 58(4) 36-52, doi 10.2469/faj.v58.n4.2453 | 15834 | Optional, L03 (paper level; used by F7, S7) |

Registry facts the planner established, for the verifier: the three curriculum sources are present with matching journal, volume, issue and year (`fama1970efficient`, `sharpe1991arithmetic`, `fama2010luck`). The registry key `harvey2015cross` carries the source string "Harvey, Liu & Zhu (2016), RFS 29(1)" with the key year 2015; it is not used by FC3, and the verifier must not cite it for FC3 without a check.

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- {doi: null, authors: "Grossman & Stiglitz (lead only)", year: "1980 (lead only)", title: "On the Impossibility of Informationally Efficient Markets", venue: "American Economic Review, volume 70, issue 3 (lead only; record not typed)", needed_for: "L01 informational-efficiency argument (costly information and the paradox). Default: the argument is stated as an ungraded naming sentence, with no key, until admitted.", confidence: "the curriculum string is not in the FC3 sources; the review queue lists this string at `references/review_queue.json:109` (no candidate established identity, used by E4 and AP8 per `references/SEED_REPORT.md:31`). Do not use `grossman1980takeover` (a different paper)."}
- {doi: null, authors: "Malkiel (lead only)", year: "1995 (lead only)", title: "Returns from investing in equity mutual funds (lead only; record not typed)", venue: "not typed", needed_for: "L03 mutual-fund persistence and fee evidence, if the architect permits it", confidence: "no record exists in `references/references.json` and no review-queue entry (grep count zero, planner check). The need is certain only if the architect wants the evidence."}
- {doi: null, authors: "Kosowski et al. (lead only)", year: "2006 (lead only)", title: "mutual fund performance, bootstrap (lead only; record not typed)", venue: "not typed", needed_for: "L03 and L04 counter-evidence on skilled funds, if the architect wants a second bootstrap study", confidence: "no record in the registry or review queue (grep count zero); the planner identifies no record from memory."}
- {doi: null, authors: "2025-2026 literature on mutual-fund skill, false discoveries and anomaly replication (lead only; no author typed)", year: "2025-2026 (lead only)", title: "contributions to the debate brief since 2025 (lead only)", venue: "not typed", needed_for: "L04 debate brief freshness (BLUEPRINT §3; VERIFIER §2.1 Freshness). B5.", confidence: "the need is certain; the planner identifies no record."}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4). Until resolved, the lessons teach the models with derivations and no empirical attribution, and each empirical sentence is graded C at most with its basis named, or is removed.

### 7.3 DATA_REQUESTS

None (§6).

---

## 8. Atlas milestone

None. No Atlas entry in `curriculum/curriculum.json` names FC3 (§0.1). No `atlas/FC3.contract.md` is needed. No contract is drafted here.

---

## 9. Cards builder (Builder F, after A-C)

- `course/modules/FC/FC3/cards.json`, ids `FC3-c001` upward (FINAL ruling 2: gaps and out-of-order ids are not defects), `lesson` in L01-L04, one card per definition, theorem statement, key formula, key result and misconception (BUILDER_RULES §7). `check_pages.py` `check_cards` checks the id prefix, the lesson existence, the grades and the registry keys (E5 §9 cites `check_pages.py` `check_cards`; the planner did not re-read that function).
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example `"basis": "Lab L02-1, derivation of the arithmetic (exact)"`.
- Cite a registry key only for an empirical or attributed claim. `cite` is `[]` where the card is a model result.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`.
- A card and the key-results row it mirrors carry the same grade and basis (FINAL ruling 13).

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit FC3            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit FC3
.venv/bin/python tools/check_projects.py --unit FC3
.venv/bin/python tools/run_labs.py --unit FC3               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/FC/FC3/L01.html                          # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/FC/FC3/L02.html --refresh lab-FC3-L02-1  # after editing a twin
.venv/bin/python tools/run_graders.py --unit FC3 --seeds 0-49        # Builder C, the reference on 50 seeds
.venv/bin/python tools/mutate_graders.py --unit FC3 --seeds 0-9      # Verifier, after the ten mutants exist
.venv/bin/ruff check tests/labs/FC3 course/modules/FC/FC3/grader && .venv/bin/ruff format --check tests/labs/FC3 course/modules/FC/FC3/grader
.venv/bin/mypy tests/labs/FC3 course/modules/FC/FC3/grader   # strict, repository configuration
```

Verifier only, on a quiet machine: `.venv/bin/python tools/page_smoke.py --unit FC3` (not run by builders; timing-sensitive; run alone, FINAL ruling 20 applies to process handling), `.venv/bin/python tools/verify_refs.py --unit FC3` (the unit ledger's run, VERIFIER §2.1).

Not run for FC3: `tools/fetch_data.py --check` (no dataset is added, §6).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`, `render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`, and the full gate in CLAUDE.md.

Flag checks: the flags the E5 plan §10 cites (`--unit`, `--page`, `--refresh`) are unchanged. The planner did not execute the builder commands; no tool was run for FC3 except the closure and concept queries in §0.1 and the reads in §0.

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **Direct prerequisite unbuilt.** AP2 has no directory (`course/modules/AP/` holds AP1 only). Links to AP2 concepts go to `concepts.html` anchors. Whether those anchors are generated for unbuilt modules is not established (Q2).
2. **No Atlas milestone.** No `atlas:` key on the FC3 project and no Atlas entry names FC3 (§0.1). `check_projects.py` skips the contract check (E5 §11 item 1 cites lines 144-146).
3. **Debate present.** FC3 has a `debate:` key (`yaml:460`), so `check_pages.py` requires a debate brief (E5 §11 item 2 cites the check in `check_unit`; the planner did not re-read it). The debate sits in L04.
4. **Both grading.** The autograder must be dual-mode, mutation-tested and have five alternatives (BUILDER_RULES §5.3; FINAL rulings 9, 10, 19). `run_graders.py` and `mutate_graders.py` apply (E5 §11 item 3 says they do not apply to rubric-only units; FC3 is not rubric-only).
5. **Four lessons, three builders.** The five-builder fan-out in the task's wording cannot give about three lessons per builder for four lessons (B4, Q1).
6. **check_dag sees linked uses only.** Unlinked uses of D1-D10 (§4) pass the tool; the verifier reads for them (VERIFIER §2.9).
7. **Lab labels.** Labs use only the standard library; the SIMULATED label is on generated data (§2.2).
8. **Tool locators.** Tool line numbers cited above are from E5 §0.2, E5 §2.2 and FC2 §4-§5, and from the planner's re-reads of `tools/check_projects.py` lines 30-75 and 120-128 and `tools/check_pages.py` lines 58-72, 221-228 and 325-342. Other tool lines are cited as the earlier plans cite them.

---

## 12. Open questions for the architect (numbered; each needs a decision before the builders start)

1. **Lesson count, hours and builder split.** Confirm 4 lessons × 8 h and a 13 h project (28.9%). Alternatives within the rules: 4 × 9 h and a 9 h project (20%); 3 × 11 h and a 12 h project (27%). **Recommended: 4 × 8 h and 13 h**, with builders A (L01, L02, hub), B (L03, L04) and C (project, grader, project labs), plus F for cards. Builders D and E are not used. Blocking for the fan-out only.
2. **B1, the unbuilt direct prerequisite AP2.** Confirm that FC3 is built before AP2, with its AP2 links going to `concepts.html#<id>` as E5 did for E1 (E5 §11 item 6). **Recommended: proceed; the builder checks that the AP2 concept anchors exist in `course/concepts.html` (generated by `build_site.py`) and records the result in the report. If the anchors do not exist, the architect either builds AP2 first or allows the link to be plain prose for AP2 concepts only.** Blocking for `page_smoke` link checks, not for the text.
3. **D2, the multiple-testing concepts in S7.** Confirm that the luck-versus-skill lesson uses plain prose for the multiple-testing ideas and does not add S7 to FC3's prerequisites (S7 is M tier and later, B2). **Recommended: plain prose, no link.** Alternative: a curriculum change moving the multiplicity content to a later module (not a builder decision).
4. **D7, arbitrage (FC2, outside the closure).** Confirm a plain `<dfn>` for "arbitrage" with no `data-concept` (L01), or add FC2 as a prerequisite of FC3 (its prerequisites M4, CF1, FC1 would then join the closure). **Recommended: plain `<dfn>`, no prerequisite change.**
5. **Bootstrap algorithm and draw order.** Confirm the procedure of §5.5 (max-t threshold, residual resampling under the null, one shared draw per replication, ceiling-rank quantile). Confirm that the exact flagged set is **not** pinned across implementations, so that alternative 4 (a different draw order) is valid. **Recommended: as stated.** If the architect pins the draw order instead, the page must state it and alternative 4 is removed (FINAL ruling 21 analogue).
6. **Critical value convention.** `chance_count` takes `critical` as an argument (grader-independent). The page's expected count `N \eta` uses the normal approximation `\Phi^{-1}(1-\eta)`, which is only approximate for T = 60 (the exact law is Student-t with T-2 degrees of freedom). The stdlib has no t quantile. **Recommended: normal approximation, stated as an approximation on the page (memo criterion 2); no t-quantile routine.** The normal quantile is obtained by bisection on `math.erf` in the lab (stdlib), with its tolerance stated.
7. **Scope and simulated parameters.** Confirm the scope in §2.1 item 4 (simulated data only; one factor; costs in the lab only; no delisting; normal residuals) and the instance size N = 40, T = 60. **Recommended: as stated.** The generator sets the planted alpha at 4 times the expected standard error, computed from its own parameters, so planted recovery is guaranteed by construction and not by a typed number.
8. **Runtime of the bootstrap in Pyodide.** `n_boot = 200` in the tests (N = 40, T = 60). Confirm, or allow a smaller N for the tests. **Recommended: `n_boot = 200` in the grader, the default on the page is stated and is 200 as well.** The builder measures the time in Pyodide with `page_smoke`; if a test exceeds 5 s, the architect decides (not a silent change).
9. **Adversarial?** The memo is a rubric-graded memo, not an IC defence or debate. No 15-angle question bank. Confirm. **Recommended: confirm (no question bank).**
10. **Mutants and alternatives count.** Confirm ten student-error mutants and five alternatives, the mutants at `ledgers/FC3/mutants/`, the equivalents at `ledgers/FC3/equivalent/` (FINAL ruling 9). **Recommended: as stated.**
11. **B3, Grossman & Stiglitz and Malkiel.** Confirm that L01 states the informational-efficiency argument as ungraded prose with no citation until the reference is admitted, and that Malkiel is not used. **Recommended: as stated (§7.2).**
12. **B5, freshness.** Confirm that the debate brief's 2025-2026 row is an open gap, named in the report, and that the verifier flags it (BLUEPRINT §3; VERIFIER §2.1). **Recommended: name it as an honest gap; the architect supplies REFERENCE_REQUESTS leads.**
13. **Figures.** No live figures are planned (no chart kernel needed). Confirm, or request one figure with a kernel and test (BUILDER_RULES §6.4). **Recommended: no figures.**
14. **Glossary.** Terms outside the 7 concepts (fair game, information set, active return, passive return, critical value, significance level, cost share, bootstrap distribution) are plain `<dfn>` with no `data-concept` (§2.1 item 5). Confirm that no GLOSSARY_REQUESTS entry is needed. **Recommended: no request.**
15. **RSS-zero exception (§5.4 row 3).** The page needs a named `ValueError` for exact fits, added by the planner. Confirm. **Recommended: confirm.**

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02 (includes the curriculum lab), L03-L04 (includes the debate brief), project (grader, the ten mutants, the five alternatives, the rubric, and blind exemplar scoring by a dedicated scorer, FINAL ruling 23). Failing rows return to the builder that owns the file, with only the failing rows.
3. Ledger at `ledgers/FC3.verification.json`; verifier scripts archived under `ledgers/FC3/scripts/` (VERIFIER §3); the mutants at `ledgers/FC3/mutants/`; the equivalents, if any, at `ledgers/FC3/equivalent/` with a README (FINAL ruling 9).
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1-B4 must be resolved or named as honest gaps first. B5 and the Grossman-Stiglitz and Malkiel requests may stay open as named gaps.

Architect decisions: pending (§12). This plan is the planner's proposal.

---

## Output contract (planner)

- Plan path: `plans/FC3-build-plan.md` (the only file written).
- Lesson count: 4 (L01-L04), 32 h; project 13 h; total 45 h.
- Blocking questions: Q1 (lesson count and builder split), Q2 (AP2 unbuilt; concept anchors).
- Could not establish: (a) the content of the FC3 sources beyond their registry records (no abstract read; the planner read only the JSON records); (b) whether `course/concepts.html` contains anchors for unbuilt AP2 concepts; (c) the `check_pages.py` debate check and the `check_cards` function (cited through E5 §11 and §9, not re-read); (d) any 2025-2026 debate contribution (none identified, B5); (e) the Pyodide run time of the bootstrap (not measured); (f) the registry record of `barberis1998model` (only its source string was matched); (g) whether `coursekit.py` closure output matches the planner's script (the planner computed the closure from `curriculum.json` directly, and the closure has 12 modules and 162 usable concepts; `tools/coursekit.py` was not run).
