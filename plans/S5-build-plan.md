# S5 build plan: GMM & Cross-Sectional Econometrics (planner output, 2026-11-09)

Unit: **S5 · GMM & Cross-Sectional Econometrics** · tier M · 100 h · prerequisites [S2, S3] · no Atlas milestone · no debate key ·
grading `both` (autograder for the Fama–MacBeth / Shanken / GMM module, rubric for the replication note) · output directory
`course/modules/S/S5/` (part code `S`) · lab twins `tests/labs/S5/` · grader folder `course/modules/S/S5/grader/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits. Executors: Haiku builders, then independent
Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Structure template: `plans/E5-build-plan.md` (sections 0-13, copied in order). Nearest built prerequisite: M3 (S2 requires M3,
`curriculum/01-foundations.yaml:665`; S5 reaches M3 in two steps), so `plans/M3-build-plan.md` is read as the precedent for a
`both`-graded tier-F unit with NumPy labs and a grader panel. The closest built analogue is S7 (tier M, 100 h, `both`, the same
70/30 hours split: `course/modules/S/S7/index.html:33`, `data-hours-lessons="70" data-hours-project="30"`).

Evidence convention: every statement about the curriculum cites `file:line` read during planning. Anything not found in the
curriculum or the tools is marked **NOT IN CURRICULUM**. Planner-derived statements about the DAG were computed with
`tools/coursekit.py` (`prerequisite_closure`, `concept_owner`) through the repo venv. The planner does not supply any
econometric formula as a fact: each formula is a derivation the L01-L07 builders write, with its assumptions, or a cited result
graded as the registry allows.

**Status: two BLOCKING issues (§0.3, B1 and B2). Builders may start L01-L05 and L07 at once. L06 (the curriculum lab) and the
project's data section wait for the architect's decision on B1 and B2. The architect's default is in §12, Q1 and Q2.**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| S5 id `S5`, title "GMM & Cross-Sectional Econometrics", tier `M`, hours `100`, prereqs `[S2, S3]` | `curriculum/01-foundations.yaml:770-774` (id 770, title 771, tier 772, hours 773, prereqs 774) |
| Core: "GMM theory and efficient weighting, Fama–MacBeth, Shanken correction, the GRS test, panel fixed effects." | `curriculum/01-foundations.yaml:775-777` |
| `introduces` has 7 concepts: `generalized-method-of-moments`, `efficient-gmm-weighting`, `hansen-j-test`, `fama-macbeth-regression`, `shanken-correction`, `grs-test`, `panel-fixed-effects` | `curriculum/01-foundations.yaml:778-785` |
| Sources: four free-text strings: "Hansen (1982), Econometrica 50(4)"; "Fama & MacBeth (1973), JPE 81(3)"; "Shanken (1992), RFS 5(1)"; "Gibbons, Ross & Shanken (1989), Econometrica 57(5)" | `curriculum/01-foundations.yaml:786-790` |
| Lab: "GRS test on Fama–French portfolios." | `curriculum/01-foundations.yaml:791` |
| Project "Two-pass estimator with errors-in-variables correction"; brief "Implement Fama–MacBeth with Shanken-corrected standard errors and GMM equivalents, and show when the correction changes the conclusion."; deliverable "Tested module plus a replication note."; grading `both` | `curriculum/01-foundations.yaml:792-798` (brief 794-796, deliverable 797, grading 798) |
| No `debate:` key and no `atlas:` key on S5 or its project; no Atlas entry names S5 (the brief names no Atlas milestone) | `curriculum/01-foundations.yaml:770-798` (absent); `curriculum/curriculum.json` `atlas` array |
| JSON row mirrors the YAML | `curriculum/curriculum.json:7078` (`"id": "S5"`) |
| Part S, "Statistics & Econometrics", order 3; S5 sits after S4 and before S6 | `curriculum/01-foundations.yaml` part S block (the block that opens before S0, line 587) and the module order S0-S7 |
| Prerequisite closure of S5 = **{CS1, M1, M2, M3, M4, P0.1, S0, S1, S2, S3}** (10 modules) | `tools/coursekit.py:239` `prerequisite_closure("S5")`, planner run |
| Usable concepts in the closure: 140 (sum of the closure modules' `introduces`) | planner run of `coursekit.curriculum()`; counts per module: CS1 12, M1 14, M2 13, M3 12, M4 19, P0.1 11, S0 10, S1 21, S2 12, S3 16 |
| Hours of the closure modules (excluding S5): 1,226 | planner sum of `hours` for the ten closure modules |
| Built closure modules: M1, M2, M3, M4 (`course/modules/M/`). Unbuilt: CS1, S0, S1, S2, S3 (`course/modules/S/` holds only S7; `course/modules/CS/` holds only CS2) | `ls course/modules/`; §4 link rules |
| Direct S5 prereq S2: prereqs [S1, M3]; S3: prereqs [S2]; S1: prereqs [M4, S0] | `curriculum/01-foundations.yaml:665`, `:701`, `:623` |
| Modules that require S5 (directly): AP3 `[AP1, S5]`; F1 `[S2, AP2, QR1, S5]`; F5 `[F2, S5, S7]`; CAP3 `[AP4, AP6, S5, E7, SC6]`; PHD-FIN requires S5 | `curriculum/03-markets.yaml:305`; `curriculum/04-quant.yaml:24`, `:148`; `curriculum/06-profession-capstone.yaml:265`; `curriculum/meta.yaml:123` |
| F2 requires F1 (so F2 transitively requires S5); F2's closure contains S5 | `curriculum/04-quant.yaml:54` (F2 prereqs [F1]); planner `prerequisite_closure("F2")` includes S5 |
| S5 is in the PhD first-year group "Econometrics I–II" with S1, S2, S3, S6 | `curriculum/meta.yaml:131` (no action planned; §12 Q15) |
| AP2 prereqs [M7, S1, E3]; AP2 is not a descendant of S5 | `curriculum/03-markets.yaml:227`; planner closure of AP2 has no S5 |
| S6 prereqs [S2]; S6 is not a descendant of S5 | `curriculum/01-foundations.yaml:799` (S6 id); planner closure of S6 has no S5 |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 100 h (`curriculum/01-foundations.yaml:773`). The tool rules:

- lesson `data-hours` 6-12 (`tools/check_pages.py:227-228`);
- hub `data-hours-lessons + data-hours-project = 100` (`tools/check_pages.py:337-338`);
- project share 10-40% of 100, i.e. 10 to 40 h (`tools/check_pages.py:339-340`);
- lessons sum to the hub's lessons figure (`tools/check_pages.py:341-342`).

Chosen split: **7 lessons × 10 h = 70 h; project 30 h (30%)**. 70 + 30 = 100. Feasible. The same 70/30 split is used by the built S7
(`course/modules/S/S7/index.html:33`).
**No STOP condition on hours.**

### 0.3 Blocking issues (architect decision required before the named part is built)

**B1. The curriculum lab names Fama–French portfolios, and no redistributable copy of them exists.**
- The lab text (`curriculum/01-foundations.yaml:791`) and the project's autograder need a cross-section of test portfolios.
- The Kenneth R. French Data Library is listed under `rejected:` (`tools/data_sources.yaml:120-131`). Its pages carry a copyright
  line and the page source says "Use in part or whole is illegal except by permission". `tools/data_sources.yaml:127-131` says
  that a lab needing those files "must use bring-your-own-data mode … with the student downloading the file". BLUEPRINT §5.3 lists
  the library as "checked and not cleared" (`BLUEPRINT.md:303-309`).
- No other embedded snapshot holds equity portfolios. The embedded sets are `fx_daily`, `fx_monthly` and `ust_daily`
  (`course/assets/data/market/MANIFEST.json`, datasets array). `fx_daily` is cleared (H.10, public-domain grant quoted at
  `tools/data_sources.yaml:28-52`) but is spot currency data only; its note says a currency position's return "also earns the
  interest differential, which these series do not contain" (`tools/data_sources.yaml`, `fx_daily.note`).
- **Plan's default (architect to confirm):** the L06 lab and the project's autograder use **SIMULATED** test portfolios generated
  from a seed, labelled SIMULATED on the page, with an honest-pending note that the curriculum's Fama–French data are not
  embedded (§6). The project's optional rung-4 stretch may use `fx_daily` (cleared, spot only, 6 currencies, 6,706 rows,
  2000-01-03 to 2026-09-30; `MANIFEST.json` `fx_daily`: `columns`, `rows`, `first`, `last`). No bring-your-own-data mode is
  required for the labs.

**B2. The curriculum lab's portfolios are F-part content, and F-part modules require S5.**
- F1 requires S5 (`curriculum/04-quant.yaml:24`), and F2 requires F1 (`curriculum/04-quant.yaml:54`). So the Fama–French
  factors and the sorted portfolios are built in a module that S5 must not depend on. Using a concept owned by F2 in S5 would create
  a cycle (`coursekit` closure of F2 contains S5).
- **Plan's default:** S5 names the test portfolios as plain prose ("cross-section of test portfolios"); no F-part concept is named
  or linked; the L06 lesson states that the curriculum's Fama–French portfolios are a later module's construction and are not
  built here. The architect may ask for the lab text to be edited (a curriculum change; builders do not edit `curriculum/*.yaml`).

Non-blocking, but the architect should see them (each has a default in §4):

- **B3. Chi-squared and F distributions have no concept.** `chi-squared` and `F` distributions are needed by the J-test (L03) and
  the GRS test (L06). `concept_owner` finds no concept id containing "chi", "f-dist" or "wald" (planner search of
  `curriculum/curriculum.json` `concepts`). Default: plain `<dfn>` with no `data-concept` (§4 D2).
- **B4. Hansen (1982) record trap.** The curriculum string "Hansen (1982), Econometrica 50(4)" matches `hansen1982large`
  (`references/references.json:11425`: Econometrica 50(4), pages 1029; `used_by: ["S5"]`). The key `hansen1982generalized`
  (`references/references.json:11385`) is Hansen & Singleton, Econometrica **50(5)**, `used_by: ["AP3"]`. It must not be cited as
  the S5 source (§7).
- **B5. Verifiers must read abstracts before attributing (VERIFIER_RULES §2.1).** No builder has read the four papers. Every
  attribution is paper-level until the verifier reads an abstract (§7, §12 Q14).

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

7 lessons × 10 h = 70 h; project 30 h; total 100 h. The registered concepts are 7 (`curriculum/01-foundations.yaml:778-785`), one
per lesson: L01 1, L02 1, L03 1, L04 1, L05 1, L06 1, L07 1 = **7**, each concept in exactly one row. Plain terms (§4 D2, D10, D11)
carry no concept id.

| Lesson | Title (working) | Concepts it defines (`introduces`, `yaml:778-785`) | Lab (twin id, `tests/labs/S5/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Moment conditions and the generalized method of moments | `generalized-method-of-moments`; plain `<dfn>`: moment condition, method of moments, instrument, over-identified (more moments than parameters) | `lab-S5-L01-1`: a just-identified IV-type sample moment; the GMM root equals the closed-form ratio; residual printed. SIMULATED | 10 | A |
| L02 | Efficient weighting and the sandwich variance | `efficient-gmm-weighting` | `lab-S5-L02-1`: over-identified GMM with identity weight and with the efficient weight, on a seeded simulated sample; both variances printed against the closed form; Monte Carlo error stated. SIMULATED | 10 | A |
| L03 | Hansen's J-test of overidentifying restrictions | `hansen-j-test`; plain `<dfn>`: chi-squared distribution (B3) | `lab-S5-L03-1`: J-statistic rejection rate at the nominal 5% level over seeded replications, with its Monte Carlo standard error. SIMULATED | 10 | B |
| L04 | The Fama–MacBeth two-pass regression | `fama-macbeth-regression`; plain `<dfn>`: factor loading, cross-sectional regression (not the AP2 CAPM beta) | `lab-S5-L04-1`: the FM premium equals the mean of the monthly slopes exactly; naive FM standard error against the pooled-OLS one. SIMULATED | 10 | B |
| L05 | Shanken's errors-in-variables correction | `shanken-correction` | `lab-S5-L05-1`: naive, Shanken and GMM standard errors on seeded panels; the correction's direction and its size checked against the derived factor. SIMULATED | 10 | C |
| L06 | The GRS test of portfolio efficiency | `grs-test`; plain `<dfn>`: F distribution (B3) | `lab-S5-L06-1` (**the curriculum lab**, `yaml:791`): the GRS F statistic on seeded SIMULATED test portfolios (B1, B2); its null rejection rate against the F critical value. SIMULATED | 10 | C |
| L07 | Panel fixed effects | `panel-fixed-effects` | `lab-S5-L07-1`: the within estimator equals the dummy-variable regression exactly; clustered and naive standard errors compared on a seeded panel. SIMULATED | 10 | D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours 70 + 30 | none | none | - | A |
| project | Two-pass estimator with errors-in-variables correction: `rubric` memo and `autograder` module (§5) | none | `lab-S5-project-1` (rung 1), `lab-S5-project-2` (rung 2, `class="lab completion"`), `lab-S5-project-3` (rung 3 check) | 30 | E |
| grader | `grader/instance.py`, `reference.py`, `test_project.py`, `starter.py`, the unit solution file (§5.2) | none | none | - | E |
| cards | `cards.json` from L01-L07 | none | none | - | F (after A-E) |

Ownership rule: each lesson builder writes only its lesson pages and twins. Builder A writes `index.html` after L01-L02 exist.
Builder E writes `project.html`, `grader/` and the three project labs, and does not depend on the lessons' prose. Builder F writes
`cards.json` only.

Ordering (no lesson links a later definition; `check_dag.py` checks linked uses, §4):
- L01 uses M2 `derivative`, M4 `expectation`, `law-of-large-numbers`, `central-limit-theorem` (`curriculum/01-foundations.yaml:216-217`),
  M4 `covariance-matrix` (`:206`), M3 `positive-semidefinite-matrix` (`:171`) and S1 `delta-method` (`:636`) in prose only.
- L02 uses L01 (`generalized-method-of-moments`, the plain `over-identified` definition) and M3 `positive-semidefinite-matrix`.
- L03 uses L02 (efficient weight, sandwich variance) and S1 `hypothesis-test` (`:637`), `statistical-power` (S1).
- L04 uses L01 (moment conditions, GMM view of FM in §3), S2 `ols-estimator` (`curriculum/01-foundations.yaml:671`),
  S2 `hac-standard-errors` (`:678`) and S3 `stationarity` (`:706`).
- L05 uses L04 (`fama-macbeth-regression`), L02 (sandwich variance), S2 `errors-in-variables` (`:681`), S1 `delta-method`.
- L06 uses S2 `ols-estimator`, S1 `hypothesis-test`, S1 `sharpe-ratio` (`:648`), M4 `multivariate-normal` (`:213`).
- L07 uses S2 `frisch-waugh-lovell-theorem` (`:672`), `clustered-standard-errors` (`:679`), `two-way-clustering` (`:680`).

Hours check: 7 × 10 = 70 (hub `data-hours-lessons="70"`); project 30 (hub `data-hours-project="30"`); 100 total.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to S5)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `plans/E5-build-plan.md` (the template and its
Architect decisions), `plans/M3-build-plan.md` (NumPy and grader precedent), `plans/S7-finish-plan.md` (the built `both`
precedent, if the builder has time), this file, and `plans/FINAL-ARCHITECT-RULINGS.md` (rulings 9, 10, 19, 23, 26, 30). Study
`course/modules/S/S7/` for layout and the grader panel. `course/templates/` holds the four skeletons. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every printed number is computed from unrounded values and rounded only at display. A
   page that shows a rounded figure states its rounding rule (precedent: E5 §2.1 item 1; CF1 L01 Remark 5.2). Monte Carlo rates
   state their replication count and their binomial standard error \(\sqrt{p(1-p)/R}\).
2. **Lab statements match code and output.** The hypothesis states the result the lab prints; the interpretation names only what
   the printed numbers show. A "checked" claim names the lab line or the test that did the check (E5 §2.2).
3. **Attribute nothing unread.** Only the registry keys in §7 may be cited, at paper level unless the verifier has read an
   abstract for the attribution (VERIFIER §2.1). No page, table, equation, coefficient, date or estimate is typed from memory.
4. **Scope words need a computation.** "every", "all", "always", "never", "any", "consistent", "efficient", "valid", "exact", "robust"
   are used only where a derivation, a finite check or a lab computes the claim. S5 scope (§12 Q7): monthly panels;
   linear factor models; constant factor loadings within the estimation window; i.i.d. or stated-dependence residuals; the
   tested sample sizes only.
5. **Define before use.** Each of the 7 registered concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its lesson
   and never earlier. Plain terms (§4) are defined at first use with a plain `<dfn>` and no `data-concept`. The term
   "over-identified" is defined in L01 (plain dfn), so L02 does not use it earlier.
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation block lists numbered Assumptions (A1, A2, ...)
   before the statement. Required hypotheses (the builder states them; the planner does not supply the proofs): GMM consistency and
   asymptotic normality (A1 i.i.d. or stationary ergodic moments with finite second moments; A2 identification, full-rank Jacobian;
   A3 a positive-definite weight matrix); the efficient-weight result (A4 the long-run covariance is positive definite); the J-test
   (A5 the moment conditions hold at the true parameter; the limit is stated as a chi-squared result under A1-A4); the Shanken
   correction (A6 the errors-in-variables model for the loadings, with the stated factor covariance and residual assumptions);
   the GRS exact F distribution (A7 i.i.d. multivariate-normal residuals, fixed factors, N < T − K); the within transformation
   (A8 strict exogeneity of the regressors given the entity effect).
7. **Grader rule.** The autograder rules apply (§5.3, §5.4) and are binding for the grader files (ruling 19): every condition the
   project page names gets its own isolated test, in both directions; a failing check never prints the expected value
   (`__tracebackhide__`).
8. **Money.** S5 has no money output. Estimates are floats with a stated tolerance; the tolerance is printed with each comparison.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their container;
   KaTeX display formulas are wrapped. `page_smoke.py` is the verifier's check.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":`
    guard. `tools/run_labs.py` runs each twin as `python -I -W error <twin>` with a fixed environment (`tools/run_labs.py:49-61`).
    The M1 twin `tests/labs/M1/lab-M1-L04-1.py` is the model.
11. **Estimator basis is explicit.** Every estimated premium, loading, standard error and test statistic states its unit (percent or
    decimal per period, monthly here), the standard-error type (naive, Shanken, GMM sandwich), the degrees of freedom (T − K − 1 or
    T) and the sample it uses.
12. **Forward-premise orderings are checked.** A lesson that uses a term defined later (for example the J-test before L03) is a
    defect, not a style choice. The verifier checks every term in §1's "Ordering" list against the lesson order.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. A B- or C-graded claim
  names its published counter-evidence (BUILDER_RULES §2.5). **The registry holds no GMM-efficiency, J-test size, FM standard-error
  or Shanken-size record that this plan has checked for S5.** Empirical claims of that kind go to `REFERENCE_REQUESTS` (§7.2) and
  are graded C with the basis named, or removed.
- Concepts: §1 table; `<dfn>` only for the 7 registered concepts plus plain `<dfn>` for the terms in §4. No `<a class="concept">` for a
  concept outside the closure {CS1, M1, M2, M3, M4, P0.1, S0, S1, S2, S3} and never a concept owned by a module that requires S5
  (§4 "forbidden").
- Prerequisite links: `href="../../../concepts.html#<id>"` for closure concepts (the anchors exist for S2 and S1 concepts, e.g.
  `errors-in-variables`, `frisch-waugh-lovell-theorem`, `hac-standard-errors`, `sharpe-ratio`; checked: `course/concepts.html`).
  `href="Lnn.html#def-<id>"` for earlier S5 lessons. **No link to the S2, S3, S0, S1 or CS1 hub pages**, because those modules are not
  built (§0.1). A lesson never links a concept defined in a later lesson.
- Labs: code lives once in `tests/labs/S5/lab-S5-Lnn-1.py` (and `lab-S5-project-1..3.py`). The page carries `@@LAB:<file>@@` and
  `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-S5-<page>-<n>`
  (`check_pages.py`). Seeded RNG only (`numpy.random.default_rng(seed)` or `random.Random(seed)`); no network; under 10 s per lab in
  Pyodide. NumPy and SciPy are allowed (Q11) and are declared with `data-packages="numpy scipy"` on the lab section, as AP1 L02
  does (`course/modules/AP/AP1/L02.html:132`). Use SciPy only for distribution quantiles (`scipy.stats.chi2`, `scipy.stats.f`).
- SIMULATED label: on every lab, figure, instance and exemplar that uses generated data. Every lab in S5 is SIMULATED (§6).
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references in
  code comments (precedent: M1 "Convention (project Q5)"; AC4 KNOWN 9).
- Banned strings (`tools/check_pages.py:58-72`, the `BANNED` tuple): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the
  scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well
  known", "obviously", "clearly", and any ellipsis `...` outside code.
- Percent changes state the base and the direction. Growth and rate conventions are stated (log or simple, per month or per year).
- A finite enumeration or a simulation is grade C with its basis named, not grade T (precedent: M1 L06).
- Hub lesson titles match each lesson's `<h1>` at integration (precedent: CF1 KNOWN 3).
- Quiz explanations are read against their lesson (precedent: CF1 KNOWN 6).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10 output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols that S5 must not give a different meaning (`notation/notation.json`, `symbols` and `macros`):

| Registered symbol | Registered meaning (locator) | S5 rule |
|---|---|---|
| `T` | number of return observations (periods) in a sample (`notation/notation.json:112`, module S1) | Allowed **only** with that meaning: the number of monthly periods. The FM first-pass window is written `T_1` (a count of periods, same meaning). Never used for a count of assets, moments, or parameters. |
| `N` | local (not registered) | Number of test portfolios or assets (defined in L04). |
| `\E` (macro, `notation.json:5`) | expectation operator | Used for the expectation of a random quantity, e.g. \(\E[g_t(\theta)]\). |
| `\Var` (macro, `notation/notation.json:13`), `\Cov` (macro, `:17`) | variance, covariance | Used for sample and population moments. |
| `\R` (macro, `:25`) | real numbers | Standard. |
| `\iid` (macro, `:41`) | independently and identically distributed | Used for the GRS and J-test assumptions. |
| `\se` (macro, `:101`) | standard error | Used for every standard error, with a subscript naming its type (`naive`, `Shanken`, `GMM`). |
| `\SR` (macro, `:69`) | population Sharpe ratio of excess returns, per period | Used for the factor Sharpe ratio in L06. |
| `\gamma_3`, `\gamma_4`, `\Phi` (M4) | skewness, kurtosis, standard normal CDF | Not used. No \(\gamma_k\) with an integer subscript (so the FM monthly slopes are \(\hat\lambda_t\), not \(\hat\gamma_t\)). |
| `R^\ast`, `R^{e\ast}`, `R_f`, `\mathbb{Q}` (AP1) | SDF payoff returns, riskless return, risk-neutral measure | Not used. |

Local symbols (allowed; defined on the lesson where they first appear and never redefined):
- moments \(g_t(\theta)\), sample moment \(\bar g_T(\theta)\), weight matrix \(W\), long-run covariance \(S\), the Jacobian \(D\),
  the J-statistic \(J\);
- factor loadings \(\beta_i\) (L04; not the AP2 CAPM beta, not linked), intercepts \(\alpha_i\), factor covariance \(\Sigma_f\),
  premia \(\lambda\) (population), monthly second-pass slopes \(\hat\lambda_t\), the Fama–MacBeth average \(\bar\lambda\);
- the test size is written in words ("the 5% test") and as a quantile \(z_{0.975}\) or \(\chi^2_{q,0.95}\), never as \(\alpha\),
  because \(\alpha\) is the intercept (the L01-L06 rule);
- the GRS factor Sharpe ratio uses \(\SR\) (registered macro); its squared value is written \(\SR^2\), with no new macro.

NOTATION_REQUESTS: none. The plan uses only local symbols and registered macros (§12 Q16).

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2): why it matters (at most 120 words), core content,
inline lab, where the canon breaks, misconceptions (at least 3), the problem set (at least 3 each in Mechanics, Proof, Empirical,
Research, with worked solutions in `<details class="solution">`), key-results table, retrieval quiz (8-15 items). The debate brief
is not required (no `debate:` key, `yaml:770-798`).

- **L01 `generalized-method-of-moments`.** Moment conditions \(\E[g(x_t;\theta_0)]=0\); the sample moment; the GMM criterion
  \(\bar g_T(\theta)^{\top} W \bar g_T(\theta)\); just-identified (\(q=k\)) and over-identified (\(q>k\)) cases defined (plain dfn:
  over-identified). Method of moments as the just-identified case. Consistency and asymptotic normality as Theorems with A1-A3,
  proved in full or as a proof sketch that names the skipped steps (T). The lab checks the just-identified case against the
  closed form. "Where the canon breaks": GMM asymptotics fail under weak identification (named, not proved; S6 concepts are not
  linked, §4 D5).
- **L02 `efficient-gmm-weighting`.** The asymptotic variance \((D^{\top}WD)^{-1}D^{\top}WSWD(D^{\top}WD)^{-1}\) (derived, T); the
  efficient weight \(W=S^{-1}\) and its variance \((D^{\top}S^{-1}D)^{-1}\) (T, with A4); two-step and iterated GMM (procedures stated,
  not claimed optimal in finite samples). The lab compares identity and efficient weights by the printed variances and a stated
  Monte Carlo error. "Where the canon breaks": the estimated \(\hat S\) can be unstable in small samples (stated, lab-checked only
  for the tested sizes).
- **L03 `hansen-j-test`.** The J-statistic \(T\,\bar g_T(\hat\theta)^{\top}\hat S^{-1}\bar g_T(\hat\theta)\) (derived). Under A1-A5 the
  limit is chi-squared with \(q-k\) degrees of freedom (stated as the test's limit with its hypotheses; the proof is a derivation
  from L02 or a precise cite; §7 for the registry). The lab estimates the rejection rate at the nominal 5% level over seeded
  replications and prints it with its standard error. "Where the canon breaks": a rejection can come from misspecification or from
  finite-sample size distortion; the lab shows the rate at the tested sizes only (C).
- **L04 `fama-macbeth-regression`.** Time-series loadings from the first \(T_1\) months (intercept and factor slopes, the
  first pass); monthly cross-sectional regressions of returns on the estimated loadings (the second pass); the Fama–MacBeth premium
  \(\bar\lambda\) as the mean of the \(\hat\lambda_t\); the naive standard error \(\hat\sigma(\hat\lambda_t)/\sqrt{T_2}\), where \(T_2\)
  is the number of second-pass months (derived, T). The GMM view: the two-pass estimator as a just-identified GMM with stacked
  moments (derivation, T, with A1-A3 of L01 and A8). Autocorrelated monthly slopes: the naive standard error is stated under the
  i.i.d. assumption; the HAC alternative is the S2 concept (`hac-standard-errors`), linked. Grade of the claim that the naive standard
  error is too small when loadings are estimated: C at most, with basis the L04 lab, until a counter-reference is admitted (§7).
- **L05 `shanken-correction`.** The errors-in-variables model for the loadings (the S2 concept `errors-in-variables` is linked); the
  second-pass premium's variance including the first-pass estimation error. The **correction factor is derived on the page** under
  A6 (T conditional on A6), in the form the builder derives; the planner does not state its formula. Property stated and tested
  (grader §5.4): the corrected standard error is not smaller than the naive one under A6. Cite `shanken1992estimation` at paper level
  as the source of the result ("the correction is derived here; the paper treats the same problem") after a verifier has read its
  abstract (§7). "Where the canon breaks": the correction assumes the stated residual and factor assumptions; with time-varying
  loadings or non-normal residuals it changes (named; C).
- **L06 `grs-test`.** The GRS test of \(\alpha_i=0\) for all \(i\) given the factors (the curriculum lab, `yaml:791`). The
  exact F statistic under A7 (i.i.d. multivariate-normal residuals, fixed factors, \(N<T-K\)) is derived on the page (T, conditional on
  A7) in terms of the alphas, the residual covariance and the factor Sharpe ratio \(\SR\) (registered macro). The F distribution is
  a plain dfn (B3; no concept link). The lab (SIMULATED, B1 and B2) computes the statistic on seeded test portfolios and prints the
  rejection rate under the null against the F critical value (from `scipy.stats.f`), with its Monte Carlo standard error. "Where the
  canon breaks": the exact F needs normality; with fat-tailed returns the rejection rate changes (named; C, counter-evidence
  requested §7.2). The lesson does not say that the lab's portfolios are the Fama–French ones (B2, honest-pending note).
- **L07 `panel-fixed-effects`.** The within (demeaning) transformation; equivalence to the dummy-variable regression (T, by FWL,
  linking S2 `frisch-waugh-lovell-theorem`); strict exogeneity (A8) and the reason the within estimator removes entity effects;
  clustered and two-way standard errors linked to S2 (`clustered-standard-errors`, `two-way-clustering`). The lab checks the exact
  equality to a tolerance of \(10^{-10}\) and compares naive and clustered standard errors on a seeded panel (SIMULATED). "Where the
  canon breaks": the within estimator is inconsistent with lagged dependent variables (named; the dynamic-panel bias is not derived
  here, and no registry record is cited for it, §7.2).

Lesson-level constraints:
- Each lesson's "Where the canon breaks" section names at least one model limit and what changes without it.
- No lesson uses a term from F, AP3, S6-level IV theory or M7/M8 as a concept (§4 "forbidden" and "plain"). Plain mentions are
  allowed only where §4 says so.
- No lesson claims an empirical size of any premium, loading, or standard error. The only numbers are the lab's printed numbers
  for the stated SIMULATED settings.

---

## 4. DAG problems (concepts that natural S5 content would use outside the closure)

Prerequisite closure of S5 (computed): **{CS1, M1, M2, M3, M4, P0.1, S0, S1, S2, S3}**, with 140 usable concepts (§0.1). Owners below
are from `curriculum/curriculum.json` `concepts` (planner check with `coursekit.concept_owner`). "Forbidden" means the module requires
S5 (directly or through F1), so using its concept would create a cycle (§0.1, the descendant list: AP3, AP4, CAP1-CAP4, DV5, F1-F7,
GM4, GM5, MS4, PM1-PM3, X2-X4).

| Ref | Concept | Owner | Where natural S5 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `fama-french-three-factor-model`, `size-effect`, `value-premium` | F2 (**forbidden**: F2 requires F1, which requires S5, `04-quant.yaml:24`, `:54`) | the factor set and the test portfolios of L04, L06 and the project | Not used. The lab's portfolios are SIMULATED (B1, B2). The FF model is named once in L06's honest-pending note as "a later module's construction", no link, no concept. |
| D2 | `chi-squared` and `F` distributions (no concept) | none in the curriculum (B3) | the J-test's limit (L03) and the GRS F statistic (L06) | Plain `<dfn>` with no `data-concept`, defined in the lesson where first used. Architect may add a concept to M4 (curriculum change; §12 Q4). |
| D3 | `capm`, `beta` (CAPM), `tangency-portfolio`, `jensens-alpha`, `equity-risk-premium`, `linear-factor-model`, `arbitrage-pricing-theory`, `icapm` | AP2 (outside closure; AP2 is not a descendant of S5, so no cycle) | the economic interpretation of loadings, alphas and premia (L04, L06) | Plain prose. Use "factor loading" for \(\beta_i\), "alpha" as "the intercept of the time-series regression", "excess return" as plain prose. No link. No AP2 prerequisite (§12 Q5). |
| D4 | `instrumental-variables`, `weak-instruments` | S6 (outside; S6 entry at `01-foundations.yaml:799`, prereqs [S2] per `coursekit`; not a descendant of S5) | the IV example that makes L01's just-identified case concrete | Plain prose and a plain `<dfn>` for "instrument". No S6 concept, no link. Architect may add S6 (not recommended: S6 is 100 h per `coursekit`, §12 Q6). |
| D5 | `kkt-conditions`, `lagrange-multiplier` | M7 (outside) | none: the GMM and FM estimators are unconstrained | Not used. |
| D6 | `condition-number` | M8 (outside; M8 is not in the closure) | the numerical conditioning of \(\hat S\) (L02, the lab's warning) | Plain prose "the matrix may be nearly singular" with no concept name; the lab reports the smallest eigenvalue (M3 concept, linked). |
| D7 | `stochastic-discount-factor`, `sdf-mean-variance-frontier`, `sdf-existence-uniqueness` | AP1 (outside, not a descendant) | GMM applied to Euler equations (the AP3 use) | Not used in S5. AP3 requires S5 (`03-markets.yaml:305`), so the Euler-equation application is AP3's; S5 does not name it. |
| D8 | `euler-equation-gmm` | AP3 (**forbidden**: AP3 requires S5) | the same application | Not used. |
| D9 | `rational-expectations-equilibrium`, `dynamic-programming` | E4, CS2 (outside) | none | Not used. |
| D10 | `method-of-moments`, `moment-condition`, `orthogonality-condition`, `over-identified`, `instrument` (no concept ids) | none | L01-L02 | Plain `<dfn>`s with no `data-concept`. "over-identified" is defined in L01 before L02 uses it. |
| D11 | `factor-loading`, `cross-sectional-regression`, `risk-premium` (no concept ids) | none | L04-L05 | Plain `<dfn>`s, no `data-concept`. |
| D12 | `expectation`, `covariance-matrix`, `multivariate-normal`, `central-limit-theorem`, `law-of-large-numbers`, `positive-semidefinite-matrix`, `derivative`, `delta-method`, `sharpe-ratio`, `hypothesis-test`, `statistical-power`, `ols-estimator`, `frisch-waugh-lovell-theorem`, `hac-standard-errors`, `clustered-standard-errors`, `two-way-clustering`, `errors-in-variables`, `stationarity` | M4, M3, M2, S1, S2, S3 (**inside** the closure) | throughout | Linked with the `concepts.html` anchors (§2.2). |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Each row needs the architect's confirmation (§12 Q2-Q6).**
`check_dag.py` checks linked uses only; an unlinked use of D1-D11 passes the tool, so the verifier reads every lesson for those names
(VERIFIER §2.9).

---

## 5. Project (`project.html`, Builder E): ladder, spec, hours, rubric and autograder

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py:33` requires the four rungs in order)

S5 is tier M, so **rungs 1 and 2 are kept to the minimum** (BLUEPRINT §4, `BLUEPRINT.md:222-223`; BUILDER_RULES §5.1,
"From tier M upward, rungs 1–2 are kept to the minimum"). The rung-1 and rung-2 pages are short; the placement pass still applies.

1. **Rung 1, worked example** (`lab-S5-project-1`, SIMULATED): one fully solved, annotated run of the FM pipeline on a single
   seeded panel: loadings, monthly slopes, the premium, the naive standard error. Each step carries a "why" note. Minimal length.
2. **Rung 2, completion** (`lab-S5-project-2`, `class="lab completion"`, SIMULATED): the same pipeline with two lines replaced by
   `___` (the monthly-slope average and the standard-error divisor). Graded instantly by the lab's check. The twin is the completed
   solution; every page line equals the twin line or contains a blank (`tools/run_labs.py` docstring). `tools/check_projects.py`
   requires a completion lab or a quiz (its completion test).
3. **Rung 3, independent project** (graded, `both`):
   - **3a, autograded module** `fm_shanken.py` (§5.2-§5.4).
   - **3b, replication note** (rubric, §5.5). `lab-S5-project-3` is the rung-3 check: it runs the rung-1 functions on the public
     demonstration instance and prints the table the note must reproduce. It does not import `grader/reference.py`, because the
     reference is excluded from deployment (BLUEPRINT §7 deploy rule, `BLUEPRINT.md:400-401`; ruling 4 notes there is no deploy step
     yet).
4. **Rung 4, stretch** (optional, not graded): run the same pipeline on the cleared `fx_daily` spot currency returns (6 currencies,
   with the note that interest differentials are absent, `tools/data_sources.yaml`, `fx_daily.note`), with a stated hypothesis about
   whether the correction changes the conclusion. No ceiling.

### 5.2 Spec (`project.html`, `dl.spec`; `tools/check_projects.py:34` `SPEC_TERMS` requires context, inputs, required outputs, constraints, grading)

- **Context.** A researcher replicates a two-pass cross-sectional test of factor premia and must report whether the errors-in-variables
  correction changes the conclusion. The module and the note are graded.
- **Inputs.** Seeded SIMULATED panels from `grader/instance.py` (`make_instance(seed)`): \(T\) monthly excess returns of \(N\) test
  portfolios and \(K\) factor series. Ranges: \(T\in[120,240]\), \(N\in[10,25]\), \(K\in\{1,3\}\) (§5.3). No embedded data, no
  Fama–French data (B1). A student's own CSV, if used, never leaves the browser (BUILDER_RULES §6.6).
- **Required outputs.**
  1. `fm_shanken.py`, a module that exposes the functions of §5.2a with the exact names and types.
  2. `replication_note.md` (the rubric-graded note; length limit RECOMMENDED: 4 pages, a design choice, not a curriculum fact).
- **Constraints.**
  - Every number in the note cites its seed, its sample (T, N, K, train length), its standard-error type and its rounding rule.
  - The note states each claim's grade; each C claim names its basis (the seed and the test).
  - Only the frozen interface is called by the tests; the note's computations use the module's functions.
  - SIMULATED labels on every table.
- **Grading.** `both`: the autograder (`fm_shanken.py` against `grader/test_project.py`) and the rubric (§5.5). The spec names both
  "autograder" and "rubric" (`tools/check_projects.py:38`, `GRADING_WORDS`; `grading_problems`).
- **Reading list.** The four curriculum sources as registry keys: `hansen1982large`, `fama1973risk`, `shanken1992estimation`,
  `gibbons1989test` (§7). Nothing else unless the architect approves (§12 Q12).

#### 5.2a Frozen interface (proposal; the architect freezes it after the L04-L05 derivations)

The student's module `fm_shanken.py` exposes (NumPy arrays; float64; \(T\) rows = months):

- `loadings(excess: NDArray[np.float64], factors: NDArray[np.float64], train: int) -> NDArray[np.float64]`: time-series OLS
  of each of the \(N\) columns on an intercept and the \(K\) factors, over the first `train` rows; returns shape \((N, K+1)\).
- `monthly_slopes(excess_t: NDArray, loadings: NDArray) -> NDArray`: one cross-sectional OLS of a month's \(N\) returns on an
  intercept and the loadings' \(K\) columns; returns shape \((K+1,)\).
- `fama_macbeth(excess, factors, train) -> FMResult`: the second pass over the months after `train`; `FMResult` is a NamedTuple with
  `premia`, `naive_se`, `shanken_se`, `gmm_se`, each of shape \((K+1,)\).
- `shanken_factor(premium_slopes: NDArray, factor_cov: NDArray) -> float`: the derived correction multiplier. Its form is fixed by
  the L05 derivation and stated on the page before the grader is frozen (§12 Q9).
- `conclusion_changes(estimate: float, naive_se: float, shanken_se: float, critical: float) -> bool`: True when the two-sided decision
  \(|\text{estimate}|/\text{se} > \text{critical}\) differs between the naive and the Shanken standard errors. `critical` is
  `statistics.NormalDist().inv_cdf(0.975)` in the page's stated rule (a computed value, not typed).

**Named exceptions (the only ones a test may assert as `ValueError`; ruling 19, M3 §5.2 precedent):**
(i) `excess` and `factors` have different numbers of rows;
(ii) `train < K + 2`, or fewer than 2 months remain after `train`;
(iii) \(N \le K + 1\) (too few assets for the cross-sectional regression);
(iv) any non-finite entry in an input;
(v) `factor_cov` is not positive definite (for `shanken_factor` and `fama_macbeth`).
Every other invalid input is outside the spec: no test asserts an exception type for it. Each named condition has its own test
and a boundary test in each direction (e.g. \(T_2 = 1\) raises, \(T_2 = 2\) does not).

### 5.3 Instances (`grader/instance.py`)

`make_instance(seed: int) -> dict[str, Any]`: deterministic; generates \(T\), \(N\), \(K\) and a planted \(\Sigma_f\) (not identity),
planted loadings, planted premia, residual noise, and the excess returns. Every instance is valid under the spec: \(N>K+1\),
\(\Sigma_f\) positive definite, `train` and the second-pass length satisfy condition (ii). Labelled **SIMULATED** in the docstring and on
the page. Seeds 0-49 give materially different answers (BUILDER_RULES §5.3; the answers change, not only labels). The reference passes
every test on seeds 0-49. The instance dict carries only inputs and the `train` value; the planted truths are used only by property
tests with stated tolerances.

### 5.4 Test suite (`grader/test_project.py`) and implementation neutrality

Each test checks properties and numbers with stated tolerances. Oracles inside the test are independent, direct computations (explicit
loops over months, the normal equations written out), never the reference's code. Each test finishes under 5 s in Pyodide; the suite
under 60 s (BUILDER_RULES §5.3.4). Sizes: \(T\le240\), \(N\le25\), \(K\le3\).

Required tests (minimum set; names are proposals):
- `test_loadings_match_direct_ols` (tolerance 1e-9 against the normal-equation oracle);
- `test_premia_are_mean_of_monthly_slopes` (the premium equals the mean of the oracle's monthly slopes, 1e-10);
- `test_naive_se_formula` (sample standard deviation with \(T_2-1\) divisor, divided by \(\sqrt{T_2}\), 1e-10; both the divisor and the
  \(\sqrt{T_2}\) are checked by the same test);
- `test_second_pass_matches_oracle_with_intercept` (equal to the oracle with the intercept; the oracle without an intercept must differ by
  more than the tolerance on the same instance, so the test cannot pass by accident);
- `test_loadings_ignore_test_months` (perturb returns after `train`; loadings unchanged to 1e-12);
- `test_shanken_not_smaller_than_naive` (property stated on the L05 page under A6; both directions tested: a zero-factor-covariance
  boundary gives equality within 1e-12, a positive one gives strictly larger);
- `test_shanken_factor_matches_derivation` (the factor on a non-identity \(\Sigma_f\) instance against the derived form, 1e-9);
- `test_gmm_efficient_se_closed_form` (the GMM standard error under the efficient weight equals the stacked-moment closed form, relative
  tolerance 1e-8, on an instance where the moments are over-identified);
- `test_decision_uses_corrected_se` (on an instance where `conclusion_changes` is True, a decision made with the naive SE is shown to
  differ; the test checks the function's output, not a fixed boolean);
- `test_matches_oracle_on_seeds_1_to_49` (checks the outputs on seeds 1 to 49, so a seed-0 constant fails);
- the five named `ValueError` tests (each with boundary tests in both directions);
- `test_outputs_finite_and_shapes` (shape \((K+1,)\) and finite values for \(K=1\) and \(K=3\)).

Failure messages name the violated property and give a concept hint; they never print the expected value (ruling 19:
`__tracebackhide__`). The suite is collected once on the reference; the page quotes the collect-only count (ruling 19).

**Five alternative correct implementations (ruling 10; each passes seeds 0-49; each in a different style; the verifier writes them in
`ledgers/S5/alternatives/`):**
1. `numpy.linalg.lstsq` for both passes and the naive standard error.
2. Normal equations solved with `numpy.linalg.solve`, with explicit centring.
3. QR decomposition (`numpy.linalg.qr`) for projection, with the M3 orthogonal-projection view.
4. Pure-Python Gauss-Jordan elimination on lists (no NumPy inside the module), with `tolist()` conversion of the instance.
5. The GMM route for every quantity: stacked moments, a `numpy.linalg.pinv` weight, the sandwich formula for all standard errors.

**Ten student-error mutants (ruling 19; single-change copies of the reference in `ledgers/S5/mutants/`; the first docstring line names
the error; each killed; `tools/mutate_graders.py --unit S5 --seeds 0-9`):**

| # | Mutant file (proposal) | First docstring line (the student error) | Killed by |
|---|---|---|---|
| 1 | `m01_pooled_slopes.py` | Pools all months into one regression instead of averaging the monthly slopes. | `test_premia_are_mean_of_monthly_slopes` |
| 2 | `m02_se_sqrt_n.py` | Divides the standard deviation of the monthly slopes by sqrt(N) instead of sqrt(T2). | `test_naive_se_formula` |
| 3 | `m03_se_ddof0.py` | Uses the population standard deviation (divisor T2) instead of the sample one. | `test_naive_se_formula` (1e-10) |
| 4 | `m04_shanken_sign.py` | Subtracts the errors-in-variables term, so the corrected SE is smaller than the naive one. | `test_shanken_not_smaller_than_naive` |
| 5 | `m05_shanken_no_inverse.py` | Uses the factor covariance where its inverse belongs in the correction. | `test_shanken_factor_matches_derivation` on a non-identity \(\Sigma_f\) |
| 6 | `m06_gmm_identity_weight.py` | Reports the GMM standard error under identity weighting as the efficient one. | `test_gmm_efficient_se_closed_form` |
| 7 | `m07_in_sample_loadings.py` | Estimates the loadings on all months, including the months it then regresses on. | `test_loadings_ignore_test_months` |
| 8 | `m08_no_intercept.py` | Drops the intercept column from the monthly cross-sectional regressions. | `test_second_pass_matches_oracle_with_intercept` |
| 9 | `m09_decision_naive_se.py` | Makes the significance decision with the naive SE even when the corrected SE is reported. | `test_decision_uses_corrected_se` |
| 10 | `m10_seed0_constant.py` | Returns the seed-0 answer for every instance. | `test_matches_oracle_on_seeds_1_to_49` |

A mutant that differs from the reference only where the page states nothing, or only inside a stated tolerance, is moved to
`ledgers/S5/equivalent/` with a README proof (ruling 9, ruling 25), never left in `mutants/`. A threshold family (a mutant that
refuses inputs above an arbitrary size) is killed by one accept test at a size beyond the realistic range (ruling 36 precedent), e.g.
\(N=25\), \(T=240\) accepted.

### 5.5 Replication note (rubric; `section.rubric-self`)

Five criteria, each with four observable levels (`tools/check_projects.py` `rubric_problems`, lines 58-73: each criterion is one table
row with a `th` and exactly four `td` cells for levels 4 down to 1):

1. **Estimates and standard errors.** Level 4: reports the premium of each factor with the naive, Shanken and GMM standard errors,
   names each SE's formula and \(T_2\). Level 1: "reports some standard errors".
2. **Computation and rounding.** Level 4: states the rounding rule and computes every quantity from unrounded values, with the seed,
   T, N, K and `train`. Level 1: "rounds the numbers".
3. **Conclusion.** Level 4: states the decision rule, gives each t-ratio and says whether the decision changes between the naive and the
   Shanken SE, quoting the table row. Level 1: "discusses significance".
4. **Grades and evidence.** Level 4: grades each claim T or C; each C names its basis (the seed and the test, or the lab); each
   attribution uses a registry key from §7 at the level the verifier has read. Level 1: "cites sources loosely".
5. **Limits.** Level 4: names, for each correction, the assumption it needs (A6 for Shanken, A7 for the GRS exact F, A8 for the
   within estimator) and what changes when it fails, and says the results are SIMULATED. Level 1: "notes some caveats".

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, fully written memo prose on a SIMULATED seed,
annotated with the descriptors each passage meets or misses. Self-assessment form (`section.rubric-self`, `data-rubric="rubric"`,
`data-exemplars="exemplar-a exemplar-b"`, as in E5 and M1). The page shows where the student's scores diverge from the exemplar scores.
**Calibration (ruling 23):** a separate scorer agent that never opens the project page scores the exemplars blind, using a stripping
script that drops the annotation elements, the verdict lines and the `data-score(s)` attributes (ruling 15). It must match the
annotations within one level per criterion (VERIFIER §2.6). Adversarial question bank: **not required** (§12 Q8).

### 5.6 Time budget (`<table id="hours">`, sums to 30 h; one rationale per row; `tools/check_projects.py`, the hours check)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One solved SIMULATED run, annotated line by line |
| Rung 2, completion problem | 3 | Fill two lines, then run the instant check |
| Rung 3a, autograded module `fm_shanken.py` | 12 | Five functions, the named exceptions, and a run of the local suite against the reference |
| Rung 3b, replication note | 9 | Tables for three SEs over the seeds, the decision rule, the grades and the limits |
| Self-assessment against exemplars (rung 3c) | 4 | Score the note with the rubric, then compare with exemplar-a and exemplar-b |
| **Total** | **30** | Equals `data-hours-project` on the hub; 30% of 100 |

---

## 6. Real-data policy and honest gaps (B1, B2)

- **Embedded and cleared:** `fx_daily`, `fx_monthly`, `ust_daily` (`course/assets/data/market/MANIFEST.json`; `tools/data_sources.yaml`).
  None is a set of equity test portfolios. `fx_daily` may serve the rung-4 stretch (spot only; §5.1).
- **Not embedded, no grant:** the Fama–French data (`tools/data_sources.yaml:120-131`, `rejected`). No other equity portfolio source
  exists in `data_sources.yaml`. **Not embedded.**
- **Plan's default:** every lab and the autograder are **SIMULATED**. The honest-pending note sits on L06 and on the project's data
  section, verbatim in substance: "The curriculum names Fama–French portfolios for this lab. The French data library states no
  redistribution grant, so the lab uses SIMULATED test portfolios generated from a seed. Fama–French portfolio construction is a later
  module's material and is not built here." It cites `tools/data_sources.yaml` `rejected` and the REFERENCE/DATA request (§7.3).
- **DATA_REQUESTS (for the architect; the planner does not name a source or licence from memory):** an equity test-portfolio dataset
  with a quoted redistribution grant (issuer URL, licence sentence, licence page, transform; BUILDER_RULES §6.6 steps 1-5). Candidate
  classes named in BLUEPRINT §5.3 (FRED series under their owners' terms; Shiller's data) are not checked for this purpose.
- No `data-files` attribute on any S5 lab. No MANIFEST entry is added by builders.
- Every SIMULATED lab prints its seed(s) and states that the numbers describe those seeds only (the scope rule, §2.1 item 4).

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

| Key | Record (as read) | Status | Use in S5 |
|---|---|---|---|
| `hansen1982large` | Hansen, "Large Sample Properties of Generalized Method of Moments Estimators", Econometrica, volume 50, issue 4, pages 1029, year 1982; DOI 10.2307/1912775 (`references/references.json:11425`) | verified; `used_by: ["S5"]`; matches `yaml:786-787` ("Hansen (1982), Econometrica 50(4)") | L01-L03 GMM and J-test, at paper level; reading list |
| `fama1973risk` | Fama & MacBeth, "Risk, Return, and Equilibrium: Empirical Tests", JPE, volume 81, issue 3, pages 607-636, year 1973; DOI 10.1086/260061 (`references/references.json:8336`) | verified; `used_by: ["S5"]`; matches `yaml:788` | L04 Fama–MacBeth, at paper level; reading list |
| `shanken1992estimation` | Shanken, "On the Estimation of Beta-Pricing Models", RFS, volume 5, issue 1, pages 1-33, year 1992; DOI 10.1093/rfs/5.1.1 (`references/references.json:20502`) | verified; `used_by: ["S5"]`; matches `yaml:789` | L05 Shanken correction, at paper level; reading list |
| `gibbons1989test` | Gibbons, Ross & Shanken, "A Test of the Efficiency of a Given Portfolio", Econometrica, volume 57, issue 5, pages 1121, year 1989; DOI 10.2307/1913625 (`references/references.json:10161`) | verified; `used_by: ["S5"]`; matches `yaml:790` | L06 GRS test, at paper level; reading list |
| `newey1987simple` | Newey & West, Econometrica 55(3), 1987 (`references/references.json:18060`); `used_by: ["S2", "S7"]` | verified | optional, L04 (HAC alternative for autocorrelated slopes), paper level; §12 Q12 |
| `petersen2008estimating` | Petersen, RFS 22(1), year 2008, print year 2009 (`references/references.json:19015`); its `source_strings` reads "Petersen (2009), RFS 22(1)" | verified; `used_by: ["S2"]` | optional, L07 (clustered standard errors in panels), paper level; the year field is inconsistent in the record (2008 and 2009), so the lesson cites the key with no year in prose |

**Trap, not to be cited for S5:** `hansen1982generalized` (`references/references.json:11385`; Hansen & Singleton, Econometrica 50(5);
`used_by: ["AP3"]`). It is a different article from the curriculum's "Hansen (1982), Econometrica 50(4)" (B4).

Not used by S5: `hansen1991implications`, `cochrane2005asset` (AP1 content), `fama1993common`, `fama2015five` (F2 content), `white1980heteroskedastici`
(S2; may be cited only in S2's own pages), `taylor1993discretion` (E7).

### 7.2 REFERENCE_REQUESTS (lead only; no bibliographic record typed)

- {doi: null, authors: "Literature on the finite-sample size of Hansen's J-test (lead only)", year: "not typed", title: "simulation
  evidence on overidentification test size", venue: "not typed", needed_for: "L03 counter-evidence to a B- or C-graded claim about the
  J-test's size at the tested sample sizes (BUILDER_RULES §2.5)", confidence: "the need is certain; no record is identified by this planner"}
- {doi: null, authors: "Literature on Fama–MacBeth standard errors under autocorrelated or estimated loadings (lead only)", year: "not
  typed", title: "not typed", venue: "not typed", needed_for: "L04 counter-evidence to the claim that the naive standard error is too
  small", confidence: "the need is certain; no record is identified"}
- {doi: null, authors: "Literature on errors-in-variables in two-pass tests (lead only)", year: "not typed", title: "not typed", venue:
  "not typed", needed_for: "L05 counter-evidence and the size of the correction in practice", confidence: "the need is certain; no record is identified"}
- {doi: null, authors: "Literature on the GRS test under non-normal returns (lead only)", year: "not typed", title: "not typed", venue:
  "not typed", needed_for: "L06 counter-evidence for the exact-F claim under fat tails", confidence: "the need is certain; no record is identified"}
- {doi: null, authors: "Literature on the within estimator with lagged dependent variables (lead only)", year: "not typed", title:
  "not typed", venue: "not typed", needed_for: "L07 'where the canon breaks' (named, not derived)", confidence: "the need is certain; no record is identified"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4). Until
resolved, the lessons teach the models by derivation, cite the four papers at paper level, and every empirical sentence is graded C at
most with its basis named, or removed.

### 7.3 DATA_REQUESTS

- {source_url: null, series_id: null, license: "not established", transform: "equity test portfolios, monthly, with a quoted
  redistribution grant", needed_for: "a real-data version of L06 and the project's rung 4"} (B1; §6)

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for S5 (§0.1: no `atlas:` key, no Atlas entry names S5). No `atlas/S5.contract.md` is
needed, and no B2-style Atlas wording exists for this unit. `tools/check_projects.py` skips the contract check when there is no
`atlas` key (`tools/check_projects.py`, the Atlas branch).

---

## 9. Cards builder (Builder F, after A-E)

- `course/modules/S/S5/cards.json`, ids `S5-c001` upward, `lesson` in L01-L07, one card per definition, theorem statement, key formula,
  key result and misconception (BUILDER_RULES §7). `check_pages.py` checks the id prefix, the lesson existence, the grades and the
  registry keys.
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, e.g.
  `"basis": "L04 derivation 2 (exact)"`.
- A card whose result is a SIMULATED lab output carries grade C and names the lab in `basis`, e.g.
  `"basis": "Lab L06 (SIMULATED, seeds 0-49)"`.
- Cite a registry key only for an empirical or attributed claim (for the four §7.1 keys, at paper level). Most S5 cards have `cite: []`.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit S5            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit S5
.venv/bin/python tools/check_projects.py --unit S5
.venv/bin/python tools/run_labs.py --unit S5               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/S/S5/L01.html                         # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/S/S5/L02.html --refresh lab-S5-L02-1  # after editing a twin
.venv/bin/python tools/run_graders.py --unit S5 --seeds 0-49   # project 3a, after grader/ exists
.venv/bin/ruff check tests/labs/S5 course/modules/S/S5/grader && .venv/bin/ruff format --check tests/labs/S5 course/modules/S/S5/grader
.venv/bin/mypy                                                 # strict, repository configuration (CLAUDE.md gate)
```

Verifier only, on a quiet machine (not run by builders): `.venv/bin/python tools/mutate_graders.py --unit S5 --seeds 0-9`
(`tools/mutate_graders.py:41-43` reads `ledgers/S5/mutants/`, at least three), `.venv/bin/python tools/page_smoke.py --unit S5`
(timing-sensitive), `.venv/bin/python tools/verify_refs.py --unit S5` (the unit ledger's run, VERIFIER §2.1).
`tools/fetch_data.py --check` is not needed unless B1 adds a dataset.

Not run for S5: none (the unit is `both`, so `run_graders.py` and `mutate_graders.py` both apply).

Flag checks: `tools/check_pages.py`, `tools/check_dag.py` and `tools/check_projects.py` accept `--unit`; `tools/run_labs.py` accepts
`--unit` and `--page`; `tools/embed_labs.py` accepts pages and `--refresh [LAB_ID ...]`. The planner did not execute the builder
commands; only the coursekit closure, concept-owner and descendant functions were run (§0.1, §4).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** No `atlas:` key on the S5 project (`curriculum/01-foundations.yaml:792-798`). No `atlas/S5.contract.md` needed (§8).
2. **No debate.** No `debate:` key (`yaml:770-798`); `check_pages.py` does not require a debate brief. The GRS, Shanken and FM claims are
   contested in the two-sided sense of BUILDER_RULES §2.5, so the counter-evidence rule applies anyway.
3. **Grader panel for a `both` unit.** `check_projects.py` requires `section.grader-panel` with `data-unit`, `data-grader`,
   `data-suite`, `data-solution`, `data-starter` (`tools/check_projects.py:122-134`), `grader/instance.py` defining
   `make_instance(seed: int)` (`:136-137`), and the rubric checks (`:138`, `rubric_problems`, lines 58-73). Attribute values follow the
   S7 pattern (`course/modules/S/S7/project.html:188`, `data-packages="numpy"`), with `data-solution` naming the unit-local module.
4. **Rung 2 must be graded instantly.** A completion lab (`class="lab completion"`), as in §5.1.
5. **One curriculum lab, seven required.** The curriculum names one lab (`yaml:791`). BUILDER_RULES §3.4 requires a numerical check per key
   formula; the plan adds one lab per lesson (E5 and M3 precedent).
6. **S2, S3, S0, S1, CS1 are unbuilt.** Links go to `concepts.html` anchors only (§2.2). The hub must not link those modules.
   `check_dag.py` works from the curriculum closure, so the unbuilt modules do not block it.
7. **check_dag sees linked uses only.** Unlinked uses of D1-D11 (§4) pass the tool; the verifier reads for them.
8. **The first-year group.** `curriculum/meta.yaml:131` lists S5 in the "Econometrics I–II" group with S1, S2, S3 and S6. No action planned (§12 Q15).

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **B1, data for the curriculum lab and the autograder.** RECOMMENDED: SIMULATED test portfolios for L06, all other labs and the autograder,
   with the honest-pending note (§6). The optional rung-4 stretch on the cleared `fx_daily` spot data, with the spot-only caveat. No
   Fama–French data embedded. No BYO mode for labs.
2. **B2, the lab's portfolios name later-module content.** RECOMMENDED: S5 names test portfolios as plain prose; L06 states that the
   Fama–French portfolios are a later module's construction and are not built here. The architect may ask for `yaml:791` to be edited
   to "GRS test on simulated test portfolios" (a curriculum change; builders do not edit `curriculum/*.yaml`).
3. **Lesson count and hours.** RECOMMENDED: 7 lessons × 10 h and a 30 h project (30%), one concept per lesson (§1). Alternative within the
   rules: 6 lessons (12, 12, 12, 12, 11, 11 h; L02 carries two concepts, `efficient-gmm-weighting` and `hansen-j-test`) and the same 30 h
   project. Not recommended: 8 lessons (the seventh concept would have no lesson of its own).
4. **Plain distribution terms.** RECOMMENDED: chi-squared and F distributions are plain `<dfn>`s with no `data-concept` (§4 D2). No M4
   change. The architect may add a concept to M4 (a curriculum change).
5. **AP2 concepts (CAPM beta, tangency portfolio, alpha, equity risk premium).** RECOMMENDED: plain prose, "factor loading" for the
   loading, no link, no AP2 prerequisite (§4 D3). AP2 is outside the closure and not a descendant, so the choice is free but
   would extend the closure.
6. **S6 concepts (instruments).** RECOMMENDED: plain prose "instrument" in L01, no S6 prerequisite (§4 D4).
7. **Forbidden descendants.** RECOMMENDED: confirm that no S5 content names or links a concept of F1-F7, AP3, AP4, CAP1-CAP4, DV5, GM4, GM5,
   MS4, PM1-PM3, X2-X4 (the descendant list in §4), and that the scope list in §2.1 item 4 holds.
8. **Project grading and adversarial status.** RECOMMENDED: `both`; ten mutants and five alternatives (§5.4); the replication note is not
   adversarial and has no 15-angle question bank.
9. **Frozen interface and the Shanken factor.** RECOMMENDED: freeze the §5.2a signatures after the L04 and L05 derivations are written and
   checked; the Shanken multiplier's form is taken from the L05 page, not from this plan. The grader is not frozen before that.
10. **Second-pass design.** RECOMMENDED: loadings from the first `train` months and the second pass on the months after them (§5.2a).
    This makes the look-ahead mutant (#7) testable. The alternative (full-sample loadings) cannot be tested for look-ahead and is not recommended.
11. **NumPy and SciPy.** RECOMMENDED: allowed in labs and the project, declared with `data-packages="numpy scipy"` (AP1 L02 precedent);
    SciPy only for distribution quantiles.
12. **Registry keys.** RECOMMENDED: cite exactly the four curriculum sources as `hansen1982large`, `fama1973risk`, `shanken1992estimation`,
    `gibbons1989test` (§7.1). Optional paper-level citations of `newey1987simple` (L04) and `petersen2008estimating` (L07), with no year in
    prose for the latter. No `used_by` edit.
13. **The Hansen trap.** RECOMMENDED: `hansen1982generalized` (Econometrica 50(5), used by AP3) is excluded from S5 (§7.1; B4).
14. **Attributions unread.** RECOMMENDED: every attribution to the four keys is paper-level until a verifier reads an abstract (VERIFIER
    §2.1). The result the lesson attributes is named as "derived here; the paper treats the same problem", never as the paper's number.
15. **The first-year group and the lab's naming.** RECOMMENDED: no action on `meta.yaml:131`; confirm.
16. **Notation.** RECOMMENDED: confirm §2.3: `T` only with the S1 meaning; no \(\gamma_k\) with integer subscripts; test size in words or as a
    quantile, never \(\alpha\); no NOTATION_REQUEST.
17. **Figures.** RECOMMENDED: no live figures and no new JS kernel (the architect's default for every module). Confirm.
18. **Hub links to unbuilt modules.** RECOMMENDED: none; prerequisites by `concepts.html` anchors and the prose (§2.2).
19. **Blind exemplar scoring.** RECOMMENDED: a dedicated scorer agent that never opens the project page (ruling 23), reading only the stripped
    output of ruling 15.
20. **Builder load.** RECOMMENDED: accept the 2-2-2-1 lesson split across builders A-D (§1). Builder D's single lesson (L07) is the lightest load
    and may take the hub's placement quiz items for the closure's skills if the architect wants it balanced.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02, L03-L04, L05-L06 (includes the curriculum lab), L07 and the placement
   quiz, project (the autograder: `run_graders` on seeds 0-49, the five alternatives, the ten mutants; the rubric: a separate blind scorer).
   Failing rows return to the builder that owns the file, with only the failing rows.
3. Ledger at `ledgers/S5.verification.json`; mutants in `ledgers/S5/mutants/` (exactly the killed set), equivalents in
   `ledgers/S5/equivalent/` with a README proof each, alternatives in `ledgers/S5/alternatives/`, verifier scripts under
   `ledgers/S5/scripts/` (VERIFIER §3).
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 and B2 must be resolved or
   named as honest gaps first.

Architect decisions: pending (§12). This plan is the planner's proposal.
