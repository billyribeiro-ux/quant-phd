# S1 build plan: Statistical Inference (2026-11-09)

Unit: **S1 · Statistical Inference** · tier F · 130 h · prerequisites M4, S0 · no Atlas milestone · no debate key ·
grading `both` (autograder for the power-analysis functions, rubric for the memo) · output directory
`course/modules/S/S1/` (part code `S`) · lab twins `tests/labs/S1/` · grader `course/modules/S/S1/grader/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits, no file edits outside this file.
Executors: Haiku builders, then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a
ledger. Structure copied from `plans/E5-build-plan.md` (sections 0-13); the nearest built prerequisite plan read in full is
`plans/M4-build-plan.md` (M4 is built, `course/modules/M/M4/`).

Evidence convention: every statement about the curriculum, the registry, the notation, the data sources and the tooling
cites `file:line` read during planning. Anything not in those sources is marked **NOT IN CURRICULUM**. Concept owners and
the prerequisite closure were computed with `tools/coursekit.py` (`unit`, `concept_owner`, `prerequisite_closure`) by the
planner through `.venv/bin/python -I`. No paper or book was read; registry facts come from `references/references.json`
records only.

**Status: no blocking issue for hours, data or grading. Four architect decisions (B1-B4, §0.3) are needed before the
builders start, and the decisions in §12 are needed before the grader is frozen.**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| S1 id `S1`, title "Statistical Inference" | `curriculum/01-foundations.yaml:619-620` |
| Tier `F`, hours `130` | `curriculum/01-foundations.yaml:621-622` |
| Prereqs `[M4, S0]` (only) | `curriculum/01-foundations.yaml:623` |
| Core: estimators, bias and variance, MLE and its asymptotics, Fisher information, Cramér–Rao, hypothesis tests, power, confidence intervals, Bayesian inference, the bootstrap | `curriculum/01-foundations.yaml:624-627` |
| `introduces` has 21 concepts (lines 629-649, one per line); mapped to lessons in §1 | `curriculum/01-foundations.yaml:628-649` |
| Sources (free text): "Casella & Berger, Statistical Inference, 2nd ed. (2002)"; "Efron (1979), Annals of Statistics 7(1)" | `curriculum/01-foundations.yaml:650-652` |
| Lab: "Bootstrap vs. asymptotic confidence intervals for a Sharpe ratio." (the curriculum lab) | `curriculum/01-foundations.yaml:653` |
| Project "Power analysis for a strategy"; brief: "Compute how many years of data are needed to detect a given Sharpe ratio at a given power, analytically and by simulation, and reconcile the two."; deliverable "Analysis notebook plus a one-page memo."; grading `both` | `curriculum/01-foundations.yaml:654-660` (brief 656-658, deliverable 659, grading 660) |
| No `atlas:` key on the S1 project; no Atlas entry names S1 (the 20 Atlas modules are CS1, CS3, S0, S4, FI1, DV4, F1, S7, QR2, MS3, PR2, PR4, FI3, CR1, AC2, CF4, QR3, GM1, SR3, GM4) | `curriculum/01-foundations.yaml:654-660` (absent); `curriculum/curriculum.json` `atlas` array |
| No `debate:` key on S1 | `curriculum/01-foundations.yaml:619-660` (absent) |
| JSON row for S1 mirrors the YAML (hours 130, prereqs, 21 introduces, sources, lab, grading both) | `curriculum/curriculum.json:6910` (`"id": "S1"`) |
| All 21 concepts of S1 are owned by S1 in `concepts` (planner check, `concept_owner`) | `curriculum/curriculum.json` `concepts`; planner run of `tools/coursekit.py` |
| S1 is a direct prerequisite of S2 (prereqs `[S1, M3]`, `curriculum/01-foundations.yaml:665`), of S7 (prereqs `[S1, S2, S3]`, `:835`), of the module at `curriculum/03-markets.yaml:227` (prereqs `[M7, S1, E3]`) and of MS1 (`curriculum/04-quant.yaml:434`, prereqs `[E4, S1]`). S7 is built while its prerequisite S1 is not (see §0.3 B2) |
| S1 appears in the `Econometrics I–II` first-year group and in the quantitative-methods topic list | `curriculum/meta.yaml:131`, `:154` |
| Prerequisite closure of S1 (planner run of `prerequisite_closure("S1")`): **{CS1, M1, M2, M4, P0.1, S0}**; usable concepts = 79 (12 + 14 + 13 + 19 + 11 + 10 introduced by those units) | planner run; per-unit `introduces` from `curriculum/curriculum.json` |
| Built status of the closure: M1, M2, M4 built (`course/modules/M/M1`-`M4`); S0, CS1, P0.1 **not built** (`course/modules/S` contains only S7; `course/modules/CS` only CS2; no P directory) | `ls course/modules/*` (planner) and `coursekit.unit(...).built` |
| S1 itself is not built (`course/modules/S/S1` does not exist) | `ls course/modules/S` (planner) |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 130 h (`curriculum/01-foundations.yaml:622`). The tool rules:

- lesson `data-hours` 6-12 (`tools/check_pages.py` `check_lesson`, line 227);
- hub `data-hours-lessons + data-hours-project = 130` (`check_pages.py` `check_hub`, around line 337);
- project share 10-40% of 130, i.e. 13 to 52 h (`check_pages.py` around line 339);
- lessons sum to the hub's lessons figure (`check_pages.py` `check_hub`).

Chosen split: **10 lessons × 10 h = 100 h; project 30 h (23.1%)**. 100 + 30 = 130. Feasible. No STOP condition on hours.

### 0.3 Blocking and decision issues (architect decision before builders start)

**B1. Real data.** No redistributable dataset is needed by the curriculum entry: the lab names no dataset
(`yaml:653`) and the project brief names none (`yaml:656-658`). The only embedded snapshots are `fx_daily`, `fx_monthly`
and `ust_daily` (`tools/data_sources.yaml:19`, `:53`, `:91`). `fx_daily` is a spot-rate series whose note says that its
returns "do not contain" the interest differential (`tools/data_sources.yaml:28-29`), so its returns are not strategy
returns. Coverage claims need a known truth, which only simulation provides.
- **Plan default: SIMULATED throughout** (BUILDER_RULES §1.7; ruling "no real data unless ... otherwise SIMULATED with an
  honest-pending note", E5 architect decisions, 2026-10-28). The page states the generating model on every lab and figure.
  No `data-files` attribute, no MANIFEST entry, no DATA_REQUESTS. Architect may confirm or offer `fx_daily` as an optional
  illustration (§12 Q3).

**B2. Built S7 already links S1 concepts.** The built module S7 links 12 of the 21 S1 concept names through
`concepts.html` anchors, and no built page defines any S1 concept (planner grep over `course/modules/S/S7`, `course/modules/M`,
`course/modules/CS`). Examples: `course/modules/S/S7/index.html:67` (`sharpe-ratio`, `sharpe-ratio-standard-error-iid`,
`hypothesis-test`, `p-value`, `type-i-error`, `statistical-power`, `t-statistic`, `confidence-interval`,
`coverage-probability`, `bootstrap`); `course/modules/S/S7/L03.html:412` (`sharpe-ratio-standard-error-iid`);
`course/modules/S/S7/L05.html:39` (`t-statistic`, `confidence-interval`); `course/modules/S/S7/L02.html:39`
(`hypothesis-test`, `p-value`, `type-i-error`, `statistical-power`). The 9 other S1 concepts are not yet linked by S7.
- **Plan default:** S1 defines the 21 names exactly as `curriculum/01-foundations.yaml:629-649` spells them. The S1 builders
  read the S7 passages above before writing those definitions, so S7's usage is consistent with S1's definition. S7 is not
  edited. The verifier checks each S7 usage against the S1 definition (§13).

**B3. Overlap with S7 on the Sharpe standard error.** S7 owns `nonnormal-sharpe-variance` (`curriculum/curriculum.json`
`concepts`; planner `concept_owner`). S1's `sharpe-ratio-standard-error-iid` (`yaml:649`) is "under iid returns".
The general iid derivation involves skewness and kurtosis, which would duplicate S7's term.
- **Plan default:** S1 derives the iid standard error by the delta method with the general moment formula (grade T, §3 L10),
  writes the normal special case, and never uses the words "nonnormal Sharpe variance". Architect confirms (§12 Q11).

**B4. Edition strings.** The curriculum gives "Casella & Berger, Statistical Inference, 2nd ed. (2002)" (`yaml:651`). The
registry record `casella2002statistical` has year 2002, ISBN 0534243126 and no edition field (`references/references.json`
record `casella2002statistical`, planner read). The registry does not verify "2nd ed.".
- **Plan default:** cite the key only, with no edition and no locator in prose (as M4 Q6). The architect decides whether to
  correct the curriculum string (§12 Q9).

Non-blocking, noted: the Efron record matches its curriculum string (`efron1979bootstrap`: The Annals of Statistics, volume 7,
issue 1, pages 1-26, year 1979, DOI 10.1214/aos/1176344552; `used_by: ["S1"]`).

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

10 lessons × 10 h = 100 h; project 30 h; total 130 h. Concept counts per row sum to 3+2+3+2+3+2+2+1+1+2 = 21, each concept in
exactly one row (`yaml:629-649`).

| Lesson | Title (working) | Concepts it defines (`introduces`, `yaml:629-649`) | Lab (twin id, `tests/labs/S1/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Estimators and their sampling distributions | `estimator`, `estimator-bias-variance`, `consistent-estimator` | `lab-S1-L01-1`: exact bias of the variance estimator with divisor n and n-1 over all samples of size 2 from a three-point law (`Fraction`) | 10 | Builder A |
| L02 | Maximum likelihood and Fisher information | `maximum-likelihood-estimation`, `fisher-information` | `lab-S1-L02-1`: Bernoulli MLE by exact search over a `Fraction` grid; score equation checked; Fisher information exact | 10 | Builder A |
| L03 | MLE asymptotics, the Cramér–Rao bound and the delta method | `mle-asymptotic-normality`, `cramer-rao-bound`, `delta-method` | `lab-S1-L03-1`: Bernoulli sample mean against the bound `p(1-p)/n` in `Fraction`; a delta-method check of a transform by seeded simulation (SIMULATED) | 10 | Builder A |
| L04 | Hypothesis tests and p-values | `hypothesis-test`, `p-value` | `lab-S1-L04-1`: exact binomial test; achieved size at most alpha, computed exactly | 10 | Builder B |
| L05 | Type I and Type II errors, and power | `type-i-error`, `type-ii-error`, `statistical-power` | `lab-S1-L05-1`: exact binomial power curve; Type II error = 1 - power, exact | 10 | Builder B |
| L06 | The t-statistic and the likelihood-ratio test | `t-statistic`, `likelihood-ratio-test` | `lab-S1-L06-1`: t-statistic on a seeded normal sample (SIMULATED); Bernoulli likelihood-ratio statistic exact; its chi-square limit by seeded simulation (SIMULATED) | 10 | Builder B |
| L07 | Confidence intervals and coverage | `confidence-interval`, `coverage-probability` | `lab-S1-L07-1`: exact coverage of the Wald and Wilson intervals for a Bernoulli parameter, n = 20, over a grid of p | 10 | Builder C |
| L08 | The bootstrap | `bootstrap` | `lab-S1-L08-1`: percentile bootstrap interval for a mean on a seeded SIMULATED sample; resample count and seed stated | 10 | Builder C |
| L09 | Bayesian inference | `bayesian-inference` | `lab-S1-L09-1`: posterior on a finite prior grid, exact in `Fraction`; Bayes' rule as the computation | 10 | Builder D |
| L10 | The Sharpe ratio and its standard error (curriculum lab) | `sharpe-ratio`, `sharpe-ratio-standard-error-iid` | `lab-S1-L10-1` (**the curriculum lab**, `yaml:653`): asymptotic and bootstrap 95% intervals for a Sharpe ratio on SIMULATED iid returns; coverage over seeded replications | 10 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 100 / 30 | none | none | - | Builder A |
| project | Power analysis for a strategy (`both`, §5) | none | `lab-S1-project-1` (rung 1), `lab-S1-project-2` (rung 2, `class="lab completion"`), `lab-S1-project-3` (rung 3 check) | 30 | Builder E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py`, `sharpe_power.py` (reference) | none | none | - | Builder E |
| cards | `cards.json` from L01-L10 | none | none | - | Builder F (after A-E) |

Owner rule: each builder writes only its lesson files and twins. Builder A writes the hub after L01-L02 exist. Builder E
writes the project, the grader and its alternatives, and does not depend on the lessons' text beyond the notation of §2.3.

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses only, §4):
- L01 uses only the closure's M4 `random-variable`, `expectation`, `variance`, `independence` (prose or link as §4 allows).
- L02 uses L01 (`estimator`) and M1 `exponential-and-logarithm` (log-likelihood).
- L03 uses L02 (`fisher-information`, `maximum-likelihood-estimation`) and M2 `taylor-theorem` and `derivative`.
- L04 uses L01 (`estimator`) and M4 `normal-distribution` (approximate null distribution).
- L05 uses L04 (`hypothesis-test`, `type-i-error`) and M4 `independence` (iid draws).
- L06 uses L02 (`maximum-likelihood-estimation`) and L04 (`p-value`); the chi-square limit is plain prose (§4 D8).
- L07 uses L04-L05 (`hypothesis-test`, `type-i-error`) and L01 (`estimator`).
- L08 uses L01 (`estimator`), L07 (`confidence-interval`) and M4 `law-of-large-numbers`.
- L09 uses L02 (`maximum-likelihood-estimation`) and M4 `independence`.
- L10 uses L03 (`delta-method`, `mle-asymptotic-normality`), L07 (`confidence-interval`), L08 (`bootstrap`), M4 `covariance-matrix` (prose) and `central-limit-theorem`.

Hours check: 10 × 10 = 100 (hub `data-hours-lessons="100"`); project 30 (hub `data-hours-project="30"`); 130 total.

Builder grouping: A = L01-L03 + index.html (3 lessons, 8 concepts); B = L04-L06 (3 lessons, 7 concepts); C = L07-L08 (2 lessons,
3 concepts); D = L09-L10 (2 lessons, 3 concepts); E = project, grader and project labs; F = cards. Rows per builder follow
the BUILDER_RULES §10 output contract.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to S1)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `plans/E5-build-plan.md` §2 (its carried-over
lessons), `plans/M4-build-plan.md` (the nearest built prerequisite), `plans/FINAL-ARCHITECT-RULINGS.md`, this file, and
`/Users/billyribeiro/.fanout/fixer-rules.md`. Study `course/modules/M/M4/` (the probability module: hub, lesson, project,
grader panel, cards) and `course/modules/S/S7/` (the autograder and rubric reference). Read S7's passages named in §0.3 B2
before writing any S1 definition. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) or from a
   stated float with a stated rounding rule, and rounded only at display. Every printed p-value, power, coverage, years and
   periods states its rounding. Precedent: E5 §2.1(1), AC4 KNOWN LIMITATION 3, CF1 L01 Remark 5.2.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints; the interpretation names only
   what the printed numbers show. A coverage or power claim names the seeded replications or the exact sum that produces it.
   Precedent: M1 LESSON_TEXT_DEFECTS.
3. **Attribute nothing unread.** Only the registry keys in §7.1 may be cited, at book or paper level, with no locator unless the
   builder has opened the source and read the locator (VERIFIER §2.1). No page, table, theorem number, equation, edition or
   year is typed from memory. Where a textbook result is needed, it is a derivation on the page (grade T) with its
   assumptions, or it is left out. Precedent: AC2, AC4, M4 §Evidence.
4. **Scope words need a computation.** "every", "all", "always", "never", "any", "consistent", "unbiased", "optimal",
   "efficient", "exact", "asymptotically", "heavy", "robust" are used only where a derivation, a finite check or a lab computes
   the claim (or the sentence states the assumption that makes it true). E5 §2.1(4) precedent.
5. **Define before use.** Each of the 21 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned
   lesson, and never before it. Other terms (the sample mean, the sample variance, the Wald and Wilson intervals, the
   chi-square distribution, the binomial distribution, the order statistic, the Beta distribution, the pseudo-random number)
   are defined in prose at first use with a plain `<dfn>` and no `data-concept` (`check_dag.py` skips a `<dfn>` without
   `data-concept`) or with no `<dfn>` at all (§4).
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation block lists its numbered Assumptions
   (A1, A2, ...) before the statement. Required: the Cramér–Rao bound needs a regular family (common support, differentiable
   log-density, differentiation under the integral sign, finite Fisher information); the MLE asymptotics needs iid draws, an
   identified parameter, a true parameter in the interior, and the regularity conditions; the delta method needs a
   differentiable transform at the true value and a root-n-consistent, asymptotically normal estimator; the Sharpe standard
   error needs iid returns with finite fourth moments and a non-zero standard deviation.
7. **Grader rule.** Applies to the autograder (§5.3, §5.5-5.6): demand an exception type only for conditions the page names;
   one isolated test per named condition and per direction of every inequality; `__tracebackhide__` in every helper that
   prints a failing value; the failing message names the violated property and never the expected value (fixer-rules item 19).
8. **Money.** S1 has no money output. Probabilities, powers, coverages and years are floats or `Fraction`s rounded only at
   display.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own
   container; nothing forces the page wider than 360 px (`page_smoke.py` is the verifier's check, §13). Quiz options use
   `min-inline-size: 0` on fieldsets; `$` inside math is escaped `\$` (fixer-rules item 14).
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no
    `if __name__ == "__main__":` guard. `run_labs.py` runs each twin as `python -I -W error <twin>` with no network. The M4
    twin `tests/labs/M4/lab-M4-L10-1.py` is the model.
11. **Basis-explicit rates and probabilities.** Every probability, power or coverage is stated with its basis: exact sum,
    closed form, or seeded replications with the replication count and the seed. Annualization follows the registry macro
    convention (§2.3).
12. **Lab runtime and draws.** Under 10 s in Pyodide. Seeded `random.Random(seed)` only. Total random draws in a lab or a
    grader call stay under 4 × 10^5 (§5.4); a longer study is precomputed at build time and the page says so (BUILDER_RULES §6.1).
13. **Ruling 13 grading.** A value the page derives by hand in a numbered Example is graded T with the Example as basis, even when
    a lab prints it too. A value that appears only in lab output is graded C naming the lab (FINAL-ARCHITECT-RULINGS 13).
14. **Ruling 22 tolerance.** Where the page states an accuracy, the tests use it (tolerance versus stated accuracy).

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation or a lab basis. A B- or
  C-graded claim names its published counter-evidence (BUILDER_RULES §2.5). The registry holds no record that this plan has checked
  for a statement of the bootstrap's failure modes or for the iid Sharpe standard error. Those claims are derivations under their
  stated assumptions, or go to `REFERENCE_REQUESTS` (§7.2).
- Concepts: §1 table. `<dfn>` only for the 21 registered concepts, plus plain `<dfn>` (no `data-concept`) for the terms listed
  in 2.1(5) if the builder chooses to define them.
- Prerequisite links: `href="../../../concepts.html#<id>"` for M4, M1, M2, CS1, S0 and P0.1 concepts (the closure, §0.1); no link
  to a prerequisite hub or lesson page, because none of those units is built as an S1 page target (`course/modules/M/M4` exists,
  but S1 links go to `concepts.html` anchors only, as M4 did for M1/M2). `href="Lnn.html#def-<id>"` for earlier S1 lessons.
  A lesson never links a concept defined in a later lesson.
- Labs: code lives once in `tests/labs/S1/lab-S1-Lnn-1.py` (and `lab-S1-project-1..3.py`). The page carries `@@LAB:<file>@@` and
  `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-S1-<page>-<n>`
  (`check_pages.py`, M4 precedent). Standard library only (`fractions`, `math`, `random`, `statistics`, `itertools`); no NumPy
  in labs (M4 precedent: the runner imports NumPy, the labs do not need it). `-W error` clean under `python -I`.
- SIMULATED label: on every lab, figure or grader that uses generated data (L03 part, L06 part, L08, L10, the project's worked
  example and the instance generator). Exact labs (L01, L02, L04, L05, L07, L09) are not labelled SIMULATED but state that they
  are exact.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references in
  code comments (E5 §2.2 precedent).
- Banned strings (`tools/check_pages.py` `BANNED`, lines 58-74): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the
  scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well
  known", "obviously", "clearly", and any ellipsis outside code (write "through", or `\(\dots\)` inside math).
- Percent and annualization: state the base and the direction. Sharpe ratios are per period unless annualization is stated
  (registered macro `\SR`, §2.3). Years and periods are never mixed without the factor `k` (periods per year) on the page.
- A finite enumeration is grade C with its basis named, unless a numbered Example derives it by hand (ruling 13).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration (CF1 KNOWN 3 precedent).
- Quiz explanations are read against their lesson (CF1 KNOWN 6 precedent).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10
  output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols and macros that S1 touches (`notation/notation.json`, `symbols` array lines 110-130, `macros` lines 67-107):

| Registered symbol or macro | Registered meaning (locator) | S1 rule |
|---|---|---|
| `T` | "number of return observations (periods) in a sample", module `S1` (`notation.json:112-114`) | **S1 owns this symbol.** Use `T` only for the number of return observations (periods). Generic i.i.d. sample size in L01-L09 is `n` (not registered). The project's `T` is periods; years are `y = T/k`. |
| `\Phi`, `\Phi^{-1}` | standard normal CDF and its inverse (quantile function), module `M4` (`notation.json:117-119`) | Use `\Phi^{-1}(1-\alpha)` for the one-sided critical point. Do not write `z_\alpha`. |
| `\gamma_3`, `\gamma_4` | skewness and kurtosis of returns, not excess; 3 under normality (`notation.json:122-127`, module `M4`) | Used only in the L10 general iid standard-error derivation (§3, B3). Same meaning throughout. |
| `\SR`, `\hSR` | population and sample Sharpe ratio, "per period unless annualization is stated" (`notation.json` macros lines 69-75) | Use these macros. Annualized values are written `\SR_{\mathrm{ann}}` and `\hSR_{\mathrm{ann}}`, with the factor `\sqrt{k}` stated. |
| `\se` | standard error (macro, `notation.json:101`) | Use it for standard errors. |
| `\PSR`, `\DSR`, `\PBO`, `\FWER`, `\FDR`, `\FDP` | probabilistic and deflated Sharpe ratio, backtest overfitting, FWER, FDR, FDP (`notation.json:77-99`) | **Not used by S1.** These belong to S7's concepts (§4 D4-D5). |
| `\E`, `\Var`, `\Cov`, `\Corr`, `\Normal`, `\iid`, `\dto`, `\pto`, `\R`, `\indic`, `\argmax`, `\argmin`, `\tr`, `\diag` | expectation, variance, covariance, correlation, normal, iid, convergence, indicator, reals, argmax, trace, diagonal (`notation.json` macros) | Use the macros. `\R` is the registered real-numbers macro (FINAL-ARCHITECT-RULINGS 1). |
| `\emgamma` | Euler–Mascheroni constant (subscripted so plain gamma stays free) | Not used. |
| `R^\ast`, `R^{e\ast}`, `R_f`, `\mathbb{Q}` | AP1 meanings (`notation.json` symbols) | Not used. |

Local symbols (allowed; `notation.json` `about`: letters conventionally local are defined per lesson): `n` sample size,
`\mu`, `\sigma`, `\alpha` (Type I error level), `\beta` (Type II error probability), `1-\beta` (power), `\theta` (parameter),
`\ell` (log-likelihood), `I(\theta)` (Fisher information), `k` (periods per year), `y` (years), `B` (bootstrap resamples),
`\hat\theta` (estimator). Each is defined on the lesson where it first appears and never redefined. A registered symbol is never
reused with another meaning (BUILDER_RULES §3.2).

NOTATION_REQUESTS: none. The plan uses only local symbols and registered symbols and macros above.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2). Mandatory content, by lesson:

- **L01** `estimator`, `estimator-bias-variance`, `consistent-estimator`: an estimator as a function of the sample and its
  sampling distribution (defined on a finite population, exact). Bias, variance and mean squared error, with the identity
  MSE = variance + bias squared (T, derived). Consistency in probability via Chebyshev under finite variance (T; hypotheses
  stated). Lab: exact bias of the variance estimator with divisor `n` and `n-1` over all samples of size 2 from a three-point law.
  Misconception: a biased estimator is not inconsistent (the bias vanishes as n grows: the lab shows this only on the grid it
  computes).
- **L02** `maximum-likelihood-estimation`, `fisher-information`: the likelihood and log-likelihood of an iid sample; the MLE as
  the maximizer (T for the Bernoulli and normal-mean examples, derived); the score function and Fisher information
  `I(\theta) = E[(\partial \ell / \partial \theta)^2]` with the regularity assumptions named. The Bernoulli Fisher information
  `1/(p(1-p))` is derived (T). Lab: the Bernoulli MLE by exact search over a `Fraction` grid, score equation checked.
- **L03** `mle-asymptotic-normality`, `cramer-rao-bound`, `delta-method`: the Cramér–Rao lower bound for unbiased estimators
  under the regularity assumptions (T, proof on the page, A1-A4 stated); MLE asymptotic normality
  `\sqrt{n}(\hat\theta - \theta) \dto \Normal(0, I(\theta)^{-1})` (stated as a theorem with assumptions; the proof is a sketch
  labelled as one and names the skipped steps, or it is cited at book level only, grade A/B with no locator, §7.1). The delta
  method for a differentiable transform `g` (T, derived from a first-order Taylor expansion, M2 `taylor-theorem`). Lab: the
  Bernoulli sample mean against `p(1-p)/n` exactly; a delta-method check of `g(\bar X)` by seeded simulation (SIMULATED).
  Forward reference rule: L03 does not link `sharpe-ratio` (L10).
- **L04** `hypothesis-test`, `p-value`: null and alternative, test statistic, critical region, size; the p-value as the smallest
  level at which the null is rejected, computed for an exact discrete test (T for the definition, derived for the binomial
  case). Lab: exact binomial test of `p = 1/2` at n = 20; the achieved size computed exactly and shown to be at most alpha.
- **L05** `type-i-error`, `type-ii-error`, `statistical-power`: size and power; Type II error `\beta(\theta_1)` and power
  `1-\beta(\theta_1)`; the trade-off at fixed n (computed). Lab: exact binomial power curve at n = 20 and alpha at the achieved
  size of L04; Type II = 1 - power, exact.
- **L06** `t-statistic`, `likelihood-ratio-test`: the t-statistic `(\bar X - \mu_0)/(s/\sqrt{n})` and its Student-t null distribution
  under iid normal draws (cite M4 `student-t-distribution`; derivation as a sketch labelled as one, or stated as a fact of M4 with
  its hypothesis). The likelihood-ratio statistic `-2 \log \Lambda` and its chi-square limit (stated with assumptions; the
  chi-square distribution is plain prose, §4 D8). Lab: t-statistic on a seeded normal sample (SIMULATED); the Bernoulli
  likelihood-ratio statistic in exact arithmetic on a grid; a seeded check of the chi-square limit (SIMULATED, replication
  count stated). The page does not claim the t-statistic is exactly Student-t for non-normal data; the registry has
  `gine1997student` only as a non-curriculum record (§7.1, Q7).
- **L07** `confidence-interval`, `coverage-probability`: a confidence interval as a random set with a coverage property;
  coverage `\Prob(\theta \in CI)` and its dependence on the parameter. Lab: exact coverage of the Wald and Wilson intervals for
  a Bernoulli parameter at n = 20 over a grid of p, summed exactly; the two coverages are printed and the page states that
  the Wald coverage varies with p, shown by the printed grid.
- **L08** `bootstrap`: the empirical distribution (S0 `empirical-distribution`, linkable: S0 is a prerequisite, §4 D1), resampling
  with replacement, the percentile interval. The iid bootstrap is justified only under the iid assumption of the sample and
  is stated as an assumption (no citation needed beyond `efron1979bootstrap` at paper level; the claim that the bootstrap is
  consistent for a mean under finite variance is a stated assumption-marked result, graded T conditionally or cited at paper
  level with no locator). Lab: percentile bootstrap interval for a mean, seeded, `B` resamples stated; SIMULATED sample.
  Where the canon breaks: dependent data (block methods are S7/BK5 concepts, §4 D6, plain prose only).
- **L09** `bayesian-inference`: prior, likelihood, posterior, posterior mean and the credible interval as a probability
  statement about the parameter (defined here, plain prose). Conjugate Beta updating uses the Beta distribution, which is not in
  the closure; the lab uses a finite prior grid instead (§4 D9). Lab: posterior on a finite prior grid over `p`, exact in
  `Fraction`, Bayes' rule computed step by step. Where the canon breaks: prior dependence at small n, shown by the lab's two
  priors.
- **L10** `sharpe-ratio`, `sharpe-ratio-standard-error-iid`: the Sharpe ratio per period and annualized (`\SR`, `\SR_{\mathrm{ann}}
  = \sqrt{k}\,\SR`, convention stated). The sample Sharpe ratio `\hSR = \bar r / s` with `s` the sample standard deviation
  (divisor n-1, stated). The asymptotic variance of `\sqrt{n}(\hSR - \SR)` for iid returns with finite fourth moments, by the
  delta method applied to `(\bar r, \overline{r^2})`, equals `1 - \gamma_3 \SR + (\gamma_4 - 1) \SR^2 / 4` (derivation, grade T
  with assumptions A1-A3; the normal special case `1 + \SR^2/2` is written out; the builder re-derives the formula and checks it
  numerically in the lab). Lab (curriculum lab, `yaml:653`): 95% asymptotic and percentile-bootstrap intervals for `\SR` on
  SIMULATED iid normal returns; coverage over seeded replications; replication count and `B` stated; the lab's runtime within the
  limit, else precomputed at build time and stated on the page (§2.1(12)). Where the canon breaks: serial dependence, non-normal
  returns beyond the fourth-moment formula, and estimation risk of the sample Sharpe ratio. Multiple strategies: not in S1 (§4 D5).

Lesson-level constraints:
- Each lesson's "Where the canon breaks" section names at least one model limit and what changes without it.
- No lesson uses a term from S2 or later as a concept (for example `ols-estimator`, `stationarity`, `bonferroni-correction`,
  `probabilistic-sharpe-ratio`, `nonnormal-sharpe-variance`). Those are outside S1 and not in its closure (§4).
- Each lesson has a debate-free structure: S1 has no debate key (`yaml:619-660`), so no debate brief is required. The
  contested-claim rule (BUILDER_RULES §2.5) still applies to any B- or C-graded claim.

---

## 4. DAG problems (concepts that natural S1 content would use outside the closure)

Prerequisite closure of S1 (computed): **{CS1, M1, M2, M4, P0.1, S0}**, 79 usable concepts. Owners below are from
`curriculum/curriculum.json` `concepts` (planner check with `concept_owner`).

| Ref | Concept | Owner (outside closure unless noted) | Where natural S1 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `empirical-distribution`, `qq-plot` (S0, **inside** the closure but S0 is not built) | S0 | L08 bootstrap resamples the empirical distribution; a normal Q-Q check in L06 | Usable and linkable as `concepts.html` anchors (S0 is a prerequisite, §0.1). No S0 page exists, so no hub or page link to S0. |
| D2 | `stationarity`, `autocorrelation-function`, `unit-root` (S3); `autocorrelation-adjusted-sharpe-ratio` (F7) | S3, F7 | serial dependence of returns in L10 (the iid assumption) | Plain prose: "serially dependent returns" with the iid assumption stated; no link, no `<dfn>`. |
| D3 | `ols-estimator`, `hac-standard-errors`, `stambaugh-bias` (S2); `bias-variance-tradeoff` (QR3) | S2, QR3 | regression-based inference; the bias-variance trade-off | Not used. S1's own `estimator-bias-variance` covers the bias and variance of an estimator. |
| D4 | `probabilistic-sharpe-ratio`, `deflated-sharpe-ratio`, `minimum-track-record-length`, `t-stat-hurdle`, `backtest-overfitting` (S7) | S7 | the power question for a strategy, and its reading against selection | Not used as terms and not in notation (`\PSR`, `\DSR`, `\PBO`). The project asks only the power question for one strategy. |
| D5 | `bonferroni-correction`, `holm-stepdown`, `benjamini-hochberg`, `false-discovery-rate`, `false-discovery-exceedance`, `data-snooping-bias` (S7) | S7 | testing many strategies at once | Not used. S1 tests one hypothesis. The page states "one strategy, one test" as its scope. |
| D6 | `stationary-bootstrap` (S7); `moving-block-bootstrap` (BK5) | S7, BK5 | bootstrap of dependent returns (L08, L10) | Not used. L08 says the iid bootstrap is assumed; block methods are named as outside S1 in plain prose only. Architect may confirm (§12 Q4). |
| D7 | `empirical-bayes-shrinkage` (S7); `bayesian-replication-shrinkage` (F5) | S7, F5 | shrinkage of Sharpe estimates (L09, L10) | Not used. The posterior of L09 is for a parameter with a prior, not for a cross-section of strategies. |
| D8 | `chi-square` distribution, `binomial` distribution, `order statistic`, `Beta` distribution (no concept in the curriculum, or `beta` is AP2's CAPM beta) | none (not a concept) or AP2 (`beta`) | L04-L07 (binomial, chi-square limit), L03 (order statistic in prose), L09 (Beta prior) | Plain prose with an inline definition at first use; no `<dfn>`. The Beta prior is replaced by a finite grid (D9). |
| D9 | `pseudo-random-number-generator`, `monte-carlo-integration` (M8) | M8 | all seeded simulations (L03, L06, L08, L10, project) | Plain prose: "a seeded pseudo-random generator (Python's `random.Random`)". No link, no `<dfn>`. |
| D10 | `generalized-method-of-moments`, `efficient-gmm-weighting` (S5); `kkt-conditions`, `lagrange` (M7) | S5, M7 | estimation by moments in L10 (the delta-method route is enough) | Not used. |
| D11 | `implicit-function-theorem`, `taylor-theorem` (M2) | M2 (inside the closure) | the delta method's Taylor step (L03) | Usable: M2 is in the closure. `taylor-theorem` linked as `concepts.html#taylor-theorem`. |
| D12 | `expectation`, `variance`, `covariance-matrix`, `central-limit-theorem`, `law-of-large-numbers` (M4, inside the closure) | M4 | throughout | Usable and linkable (M4 is built). |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Each row needs the architect's confirmation (§12 Q2-Q4).**
`check_dag.py` checks linked uses only (`tools/check_dag.py` docstring); an unlinked use of D2, D4-D7 and D9 passes the tool,
so the verifier reads every lesson for these names (§13).

---

## 5. Project (`project.html`, Builder E): autograder and rubric, ladder, spec, grader, rubric

### 5.1 Ladder (BLUEPRINT §5.1; `check_projects.py` requires the order)

1. **Rung 1, worked example** (`lab-S1-project-1`, SIMULATED): one fully solved, annotated instance. It computes the required
   years in closed form for one Sharpe ratio, alpha and power; then checks the required periods by the power formula; then runs
   a seeded simulation of the test at that T and prints its power. Each step has a "why" annotation. Full length (tier F).
2. **Rung 2, completion** (`lab-S1-project-2`, `class="lab completion"`, SIMULATED): two lines are blanked (`___`): the inflated
   variance term `1 + \SR^2/2` and the ceiling of the required periods. Graded instantly. Its twin is the completed solution;
   every page line equals the twin line or contains a blank (`tools/run_labs.py` docstring; FINAL-ARCHITECT-RULINGS 11).
   `check_projects.py` requires a completion lab or a quiz.
3. **Rung 3, independent project** (graded by autograder and rubric): the module `sharpe_power.py` and the memo. `lab-S1-project-3`
   is the rung-3 check: it prints the four interface results for the default instance from the same closed forms, so a student
   can compare.
4. **Rung 4, stretch** (optional, not graded): the same analysis for a non-normal return law (for example a Student-t sample with
   a stated finite-fourth-moment hypothesis), or a comparison of the closed form with the iid standard error of L10 at a short T.

### 5.2 Spec (`dl.spec`; `check_projects.py` requires the terms context, inputs, required outputs, constraints, grading)

- **Context.** A portfolio manager has a backtest of a strategy and must decide how many years of data would let a test detect a
  stated Sharpe ratio at a stated power. The analysis gives the answer analytically and by simulation, and explains any
  difference.
- **Inputs.** No dataset. The project's inputs are the four parameters of one case: an annualized Sharpe ratio `\SR_{\mathrm{ann}}
  > 0`, periods per year `k` (a positive integer), a one-sided significance level `\alpha \in (0,1)` and a power target
  `1-\beta \in (0,1)`. Returns are iid normal with per-period mean `\SR` and standard deviation 1 in the simulation (SIMULATED).
  The grader's instance generator produces these cases (§5.3); the student's own study uses the same model.
- **Required outputs.** (a) `sharpe_power.py` implementing the four functions of §5.3; (b) an analysis notebook or script that
  computes the analytic and simulated answers for the cases in the memo; (c) `memo.md`, one page, that states the model, the
  closed form, the simulation design, the reconciliation and the limits. The memo states every number with its basis: the
  closed form, or the seed, the replication count and the Monte Carlo standard error.
- **Constraints.**
  - Test: one-sided, level `\alpha`, using `\hSR` with the null standard error `1/\sqrt{T}` (critical value `\Phi^{-1}(1-\alpha)`
    on `\sqrt{T}\,\hSR`). This is the only test the grader accepts.
  - Years are `T/k`; the periods required are the ceiling of the unrounded `T`. Rounding rules are stated on the page.
  - Sample standard deviation uses divisor `T-1`. Returns are per period unless annualization is stated.
  - Standard library only (`data-packages` is empty). No dataset. No series from Atlas (none is named, §8).
  - Every number in the memo is computed from unrounded values, with the rounding rule stated.
- **Grading.** `both`: the spec's grading entry names "autograder" and "rubric" (`tools/check_projects.py` `GRADING_WORDS`,
  `grading_problems`). The autograder covers `sharpe_power.py`; the rubric covers the memo (§5.4).
- **Reading list.** `ol.reading-list` cites `casella2002statistical` and `efron1979bootstrap` (registry keys only, §7.1). Nothing else.

### 5.3 Frozen interface and autograder design (proposal; the architect freezes it, §12 Q5)

`sharpe_power.py` exposes exactly these four functions. Each is documented in `project.html` with units.

1. `sharpe_hat(returns: list[float]) -> float`: the per-period sample Sharpe ratio, mean over the sample standard deviation with
   divisor `n-1`. Raises `ValueError` when fewer than two returns are given or when the sample standard deviation is zero
   (both named on the page).
2. `analytic_years(sr_ann: float, periods_per_year: int, alpha: float, power: float) -> float`: the years of data `y` such that the
   one-sided test in §5.2 has power `power` at the alternative. Closed form:
   `y = (\Phi^{-1}(1-\alpha) + \Phi^{-1}(power) \sqrt{1 + \SR_{\mathrm{ann}}^2/(2k)})^2 / \SR_{\mathrm{ann}}^2`.
   (Derivation on the page: the alternative variance of `\hSR` is `(1 + \SR^2/2)/T` with `\SR = \SR_{\mathrm{ann}}/\sqrt{k}`; the
   algebra is for the builder to show.) Raises `ValueError` when `sr_ann <= 0`, `periods_per_year < 1`, or `alpha` or `power` is not in
   `(0,1)` (each named on the page).
3. `required_periods(sr_ann: float, periods_per_year: int, alpha: float, power: float) -> int`: the smallest integer number of
   periods `T` with the power at least `power`, i.e. `math.ceil(analytic_years(...) * periods_per_year)`, returned as `int`.
   Same `ValueError` conditions as item 2.
4. `simulated_power(periods: int, sr_per_period: float, alpha: float, n_sims: int, seed: int) -> float`: the rejection rate of the
   test in §5.2 over `n_sims` simulated samples of `periods` iid `Normal(sr_per_period, 1)` returns, drawn from
   `random.Random(seed)`. Raises `ValueError` when `periods < 2`, `n_sims < 1`, or `alpha` is not in `(0,1)` (each named on the page).
   The result depends only on the arguments (never on global random state).

Instance generator (`grader/instance.py`, `make_instance(seed: int) -> dict[str, Any]`):
- deterministic per seed; generates only valid instances: `sr_ann` from a fixed grid in `[0.30, 1.50]`, `periods_per_year` in
  `{12, 52, 252}`, `alpha` in `{0.01, 0.05, 0.10}`, `power` in `{0.80, 0.90}`, and a list of 30 returns for `sharpe_hat`,
  generated from `random.Random(seed)`;
- seeds 0-49 give materially different answers (the required periods change, not only the labels; the grader checks 20 seeds,
  `run_graders.py` `check_instances`);
- docstring and page label the instance **SIMULATED** ("generated inputs, not market data").

Reference (`grader/reference.py`) is the full solution as `sharpe_power.py`; `starter.py` raises `NotImplementedError` in every
function and the suite must fail on it (`run_graders.py` `grade`).

### 5.4 Test properties (`grader/test_project.py`; no hard-coded answers; each check uses the instance's own parameters)

Each named condition and each inequality direction has its own isolated test. Failure messages name the property and a concept
hint; they never print an expected value (`__tracebackhide__`; fixer-rules item 19).

1. `sharpe_hat` exact: equals a `Fraction` computation of mean over sample standard deviation (divisor n-1) on the instance's 30
   returns, to 1e-12 relative (ruling 22). Kills the divisor mutant.
2. `sharpe_hat` named errors: fewer than two returns raises `ValueError`; constant returns raise `ValueError`. Two tests.
3. `analytic_years` closed form: the returned `y` solves the power equation: with `T = y·k` the one-sided power
   `1 - \Phi(\,(\Phi^{-1}(1-\alpha) - \sqrt{T}\,\SR)/\sqrt{1+\SR^2/2}\,)` equals `power` to 1e-9 (recomputed in the test with
   `statistics.NormalDist`). Kills the naive variance (no inflation), the two-sided critical value, the swapped levels, the
   missing de-annualization and the periods-for-years mutants, because each changes the solved `y`.
4. `required_periods`: result has type `int` (not `float`); equals `math.ceil(analytic_years(...)*k)`; the power at the result is at
   least `power` (1e-12 tolerance, exact formula); the power at the result minus one is below `power`. Kills the floor mutant and the
   off-by-one mutant. Kills the naive mutant on the power bound.
5. Monotone: `required_periods` at `1.25 * sr_ann` is not larger than at `sr_ann`.
6. `analytic_years` named errors, one test per condition and direction: `sr_ann = 0` and `sr_ann < 0` raise; `sr_ann` just above 0
   does not raise; `periods_per_year = 0` raises and `= 1` does not; `alpha = 0` and `alpha = 1` raise, `alpha = 0.5` does not;
   `power = 0` and `power = 1` raise, `power = 0.5` does not. `required_periods` has the same tests.
7. `simulated_power` null size: at `sr_per_period = 0` the rejection rate is within 4 binomial standard errors of `alpha` (computed
   from `n_sims`). Kills the single-path mutant (every draw identical, rate 0 or 1).
8. `simulated_power` power band: at the instance's required periods the simulated rate is within the band `[power - 4 SE - tol,
   power + 4 SE + tol]`, where `tol` is the finite-T tolerance the builder measures by a sweep over the grid and records in the
   ledger (§12 Q13). Not used to kill the naive mutant (the gap is too small for Monte Carlo noise; test 3 does that).
9. `simulated_power` determinism: the same seed gives the same value; calling it after `random.seed(...)` with another value
   gives the same value (kills the global-random mutant).
10. `simulated_power` named errors: `periods = 1` raises; `n_sims = 0` raises; `alpha` outside `(0,1)` raises. One test each.
11. Hard-coded answers: the answers for seeds 1-49 differ from seed 0's; the function is not a constant table (kills the seed-0
    mutant).
12. Failure messages: a failing test prints the property violated and a concept hint, never the expected number.

Runtime: each test under 5 s in Pyodide; the suite under 60 s. Every call draws at most 4 × 10^5 random numbers in total (for
example `n_sims * periods <= 4e5`), with `n_sims <= 2000` and `periods <= 1000`.

### 5.5 Five alternative correct implementations (must pass seeds 0-49)

The suite must pass five independently written correct implementations, not only `reference.py`. They live under
`tests/graders/S1/alt_1.py` to `alt_5.py` (§12 Q14) and run by a pytest module the verifier adds under `tests/`.

1. Box-Muller normal draws in `simulated_power` (instead of `random.gauss`).
2. Polar (Marsaglia) normal draws in `simulated_power`.
3. `analytic_years` by bisection on the power function (matches the closed form to the test tolerance).
4. `sharpe_hat` by Welford's one-pass update of mean and variance (exact on the test returns to 1e-12).
5. `required_periods` by an integer search started at the closed-form guess (the smallest integer with power at least `power`).

Alternatives 1 and 2 differ from the reference in the random stream; every test that compares simulated values is property-based
(§5.4 items 7-9), so they pass. Each alternative must differ in style, not only in variable names.

### 5.6 Mutants (the verifier writes ten student-error mutants; each must be killed)

Each mutant is a complete single-change copy of `sharpe_power.py` under `ledgers/S1/mutants/`, its first docstring line names the
student error, and `tools/mutate_graders.py --unit S1 --seeds 0-9` must kill each one (`mutate_graders.py` requires at least three).

1. m01 naive variance: ignores the inflation of the alternative variance (uses `(z_{1-\alpha}+z_{1-\beta})^2 / (k \SR^2)`).
2. m02 periods for years: `analytic_years` returns `T` instead of `T/k`.
3. m03 floor: `required_periods` uses `math.floor` instead of `math.ceil`.
4. m04 divisor: `sharpe_hat` divides by `n` instead of `n-1`.
5. m05 two-sided: the critical value is `\Phi^{-1}(1-\alpha/2)`.
6. m06 swapped levels: the critical value uses `\Phi^{-1}(1-\beta)` in place of `\Phi^{-1}(1-\alpha)`.
7. m07 global random: `simulated_power` calls the module-level `random` functions and ignores `seed`.
8. m08 one path: `simulated_power` draws one sample of `periods` returns and reuses it for every simulation.
9. m09 no de-annualization: `analytic_years` uses `sr_ann` where the per-period Sharpe ratio is required.
10. m10 seed-zero answer: `required_periods` returns a constant when `sr_ann` equals the seed-0 instance's value.

Equivalent mutants (none planned): a change that no input can distinguish from the reference goes to `ledgers/S1/equivalent/` with
a README proof (ruling 9). A mutant that differs only inside a stated tolerance goes there too (ruling 22, 25). Threshold mutants
(one refusal above an arbitrary bound) are killed by one accept test at a size beyond any realistic bound (ruling 36): the
accept test uses `periods = 1000` and `n_sims = 1`.

### 5.7 Rubric (memo; the `rubric` half of `both`)

- 5 criteria, four observable levels each (level 4 down to level 1; `table.rubric#rubric`; `check_projects.py` `rubric_problems`
  counts exactly four `td` cells per criterion row):
  1. **Model and assumptions.** Level 4: states iid normal returns, the one-sided test, `k`, and each assumption's role in the
     formula. Level 1: "states some assumptions".
  2. **Analytic derivation.** Level 4: derives the closed form, showing the alternative variance `1 + \SR^2/2` and its effect, and
     checks the power at the required periods. Level 1: "uses the formula".
  3. **Simulation design.** Level 4: states seed, replication count, `T` and the Monte Carlo standard error, and checks the null
     size. Level 1: "runs a simulation".
  4. **Reconciliation.** Level 4: compares analytic and simulated power at the same `T`, names the gap and its cause (variance
     inflation, finite-T normality of `\hSR`, Monte Carlo error) and shows which causes shrink as `T` grows. Level 1: "the two
     agree roughly".
  5. **Units and rounding.** Level 4: keeps years and periods apart with `k`, states the ceiling rule and every rounding rule, and
     computes from unrounded values. Level 1: "rounds the numbers".
- Exemplars at two levels: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, fully written memos on a
  SIMULATED case, each annotated with the descriptors it meets or misses. Self-assessment form (`section.rubric-self`,
  `data-rubric="rubric"`, `data-exemplars="exemplar-a exemplar-b"`, as in M1 and E1; E5 §5 is the template). The page shows where the student's scores
  diverge from the exemplar scores.
- Calibration (ruling 23, FINAL-ARCHITECT-RULINGS 15): a separate scorer agent, which never opens the project page, runs the
  stripping script over the exemplar file and scores the memo prose blind, within one level per criterion.
- No question bank: the memo is not an adversarial defence (§12 Q6).

### 5.8 Time budget (`<table id="hours">`, sums to 30 h; every row needs a one-line rationale)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate one solved case) | 2 | One closed-form case and one seeded simulation, annotated line by line |
| Rung 2, completion problem (fill two blanks, run the instant check) | 2 | Two blanks, graded instantly against the twin |
| Implement `sharpe_power.py` and check it against the autograder | 10 | Four functions, the named errors, and a local suite run to green |
| Simulation study and reconciliation of analytic and simulated power | 8 | Run the test at the memo's cases, measure the gap, and find its cause |
| Memo (one page, every number cited with its basis) | 5 | One page with the model, closed form, simulation design and reconciliation |
| Self-assessment against the exemplars | 3 | Score the memo with the rubric, then compare with exemplar-a and exemplar-b |
| **Total** | **30** | Equals `data-hours-project` on the hub |

---

## 6. Real-data policy (B1 applies)

- **No embedded data is used.** The curriculum names no dataset for S1 (`yaml:653`, `yaml:656-658`). Every lab, figure and grader
  input is generated from formulas and seeds, labelled **SIMULATED** where generated (BUILDER_RULES §1.7).
- **Optional real illustration (architect choice, §12 Q3).** `fx_daily` (`tools/data_sources.yaml:19-52`) carries a quoted licence
  ("Unless otherwise indicated ... public domain", `:23-25`, `licence_url` `:26`). Its series are spot rates, not total returns
  (`:28-29`). If used, it would need `data-files` on the lab, a figure source line with the retrieval date from MANIFEST, and a
  statement that spot returns exclude the interest differential. Default: not used.
- **Honest-pending note.** Not needed under the default, because no real data is claimed. The page says: "All returns in this unit
  are generated from a stated model (SIMULATED). No market data is used."
- **DATA_REQUESTS:** none under the default.
- No `data-files` attribute on any lab. No MANIFEST entry is added by builders.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

| Key | Record (as read) | Status | Use in S1 |
|---|---|---|---|
| `casella2002statistical` | book, "Statistical Inference", year 2002, ISBN 0534243126, no edition field, `used_by: ["S1"]` (`references/references.json`, record read) | verified; curriculum string "2nd ed. (2002)" not verified (B4) | book level only in the lessons' "Sources" line and the reading list; no edition, no locator unless read |
| `efron1979bootstrap` | journal article, "Bootstrap Methods: Another Look at the Jackknife", The Annals of Statistics, volume 7, issue 1, pages 1-26, year 1979, DOI 10.1214/aos/1176344552, `used_by: ["S1"]` (record read) | verified; matches `yaml:652` | L08 bootstrap (paper level, no locator); reading list |

Not curriculum-listed for S1 but registry-verified (default: not cited; architect decision §12 Q6, Q7):
- `lo2002statistics` ("The Statistics of Sharpe Ratios", Financial Analysts Journal, volume 58, issue 4, pages 36-52, year 2002,
  DOI 10.2469/faj.v58.n4.2453; `used_by: ["F7", "S7"]`). A source for `sharpe-ratio-standard-error-iid`. Citing it from S1 needs the
  architect to add S1 to its `used_by`; `tools/add_reference.py` merges `used_by` for an existing key (`add_reference.py:102-110`).
- `gine1997student` ("When is the Student t-statistic asymptotically standard normal?", The Annals of Probability, year 1997,
  DOI 10.1214/aop/1024404523; `used_by: ["S7"]`). Relevant to L06 t-statistic. Same approval path.
- `blitzstein2019introduction` (`used_by: ["M4"]`) and `billingsley2012probability` (`used_by: ["M6"]`): probability texts, not
  curriculum sources for S1. Not cited (M4 Q14 precedent).
- `sharpe1964capital` exists but is the CAPM paper, not the Sharpe-ratio paper; not cited.
- `bailey2012sharpe`, `bailey2014deflated`, `jobson1981performance`, `ledoit2008robust`, `harvey2015backtesting`, `politis1994stationary`,
  `newey1987simple`, `white1980heteroskedastici`, `benjamini1995controlling`, `romano2005stepwise`, `lehmann2005generalizations`: S2, S7
  and F7 records; not S1 content. Not cited.

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- {doi: null, authors: "Sharpe (lead only; no author list typed)", year: "not typed", title: "the original Sharpe-ratio paper (lead only; record not typed)", venue: "not typed", needed_for: "L10 attribution of the Sharpe ratio, if the architect permits an attribution sentence", confidence: "the need is certain; the registry has no record for this paper; no candidate identified by this planner"}
- {doi: null, authors: "Literature on the iid bootstrap under dependence (lead only)", year: "not typed", title: "failure or modification of the iid bootstrap for serially dependent data (lead only; record not typed)", venue: "not typed", needed_for: "L08 counter-evidence for the bootstrap claim, if the claim is graded B or C (BUILDER_RULES §2.5); the default grades it as an assumption-marked result", confidence: "the need is certain only if a graded claim about dependence is made; no record identified"}
- {doi: null, authors: "Literature on estimation error of the sample Sharpe ratio (lead only)", year: "not typed", title: "estimation risk of Sharpe ratios in finite samples (lead only; record not typed)", venue: "not typed", needed_for: "L10 and memo limits, graded B or C with counter-evidence; `lo2002statistics` is the registry candidate (§7.1) and needs approval", confidence: "the need is certain; the planner did not read or name a record"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4).
Until resolved, the lessons teach the models with derivations and assumption-marked statements, and any empirical sentence is
graded C at most with its basis named, or is removed.

---

## 8. Atlas milestone

None. No `atlas:` key on the S1 project (`curriculum/01-foundations.yaml:654-660`), and the Atlas list (E5 §0.1 names the 20 modules)
does not include S1. No `atlas/S1.contract.md` is needed or drafted. The Atlas data layer and programs belong to S0 (A3), CS1, CS3 and
S7 in the curriculum (`curriculum/curriculum.json` `atlas` array). The grader's solution file is unit-local (`sharpe_power.py`),
as in the M4 and S7 patterns.

---

## 9. Cards builder (Builder F, after A-E)

- `course/modules/S/S1/cards.json`, ids `S1-c001` upward, `lesson` in L01-L10, at least one card per lesson (`check_pages.py`
  `check_cards`). One card per definition, theorem statement, key formula, key result and misconception (BUILDER_RULES §7).
- Grade T for each derived result (the Cramér–Rao bound under its assumptions, the MLE variance, the delta-method variance, the
  iid Sharpe standard error, the closed form for `analytic_years`), with `"basis"` naming the derivation or the lab, for example
  `"basis": "Lab L03, Derivation 2 (exact)"`. A card and the key-results row it mirrors carry the same grade and basis
  (FINAL-ARCHITECT-RULINGS 13).
- Cite a registry key (§7.1) only for an empirical or attributed claim. `cite` is `[]` where the card is a model result.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`, with the replication count.
- Each card tests one fact and its back is checkable against the lesson text.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit S1            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit S1
.venv/bin/python tools/check_projects.py --unit S1
.venv/bin/python tools/run_labs.py --unit S1               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/S/S1/L01.html                             # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/S/S1/L02.html --refresh lab-S1-L02-1      # after editing a twin
.venv/bin/python tools/run_graders.py --unit S1 --seeds 0-49                                  # project builder (Builder E)
.venv/bin/python tools/mutate_graders.py --unit S1 --seeds 0-9                                # verifier only
.venv/bin/ruff check tests/labs/S1 course/modules/S/S1/grader && .venv/bin/ruff format --check tests/labs/S1 course/modules/S/S1/grader
.venv/bin/mypy tests/labs/S1 course/modules/S/S1/grader                                       # strict, repository configuration
```

Commands for the five alternatives (Builder E writes the runner; the verifier runs it): `.venv/bin/python -m pytest tests/graders/S1`
(the pytest module that imports each `alt_*.py` and runs the suite on seeds 0-49 with `run_suite` semantics; §5.5, §12 Q14).

Not run for S1 by builders: `tools/page_smoke.py` (verifiers, quiet machine, timing-sensitive). Repo-wide gates (`check_pages.py --all`,
`check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`, `render_curriculum.py` and its diff, `verify_refs.py --offline`)
are the architect's, once, before merge (CLAUDE.md gates).

Flag checks: `check_pages.py`, `check_dag.py` and `check_projects.py` accept `--unit`; `run_labs.py` accepts `--unit` and `--page`;
`run_graders.py` and `mutate_graders.py` accept `--unit` and `--seeds`; `embed_labs.py` accepts pages and `--refresh [LAB_ID ...]`.
The planner did not execute the builder commands; only the coursekit closure, concept-owner, unit and registry functions were run (§0).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** No `atlas:` key on the project and no Atlas entry names S1 (§8). `check_projects.py` skips the contract
   check when no `atlas` key is present (`check_projects.py` `check_unit`).
2. **No debate.** S1 has no `debate:` key (`yaml:619-660`), so `check_pages.py` does not require a debate brief.
3. **Both grading.** `check_projects.py` requires the grader panel and the autograder files for `both`
   (`check_projects.py` `check_unit`, lines 122-137): `section.grader-panel` with `data-unit`, `data-grader`, `data-suite`,
   `data-solution`, `data-starter`, a `data-support` list, and the files `reference.py`, `instance.py`, the suite and the starter must
   exist; `instance.py` must define `make_instance(seed: int)`. The rubric half needs 4-7 criteria with four levels, and exemplars
   (`rubric_problems`).
4. **`run_graders.py` runs only `grader/reference.py`.** `grade()` runs the reference (`tools/run_graders.py` `grade`); the
   alternatives (§5.5) need their own runner (§12 Q14). The builder confirms from `run_graders.workspace` (not read in full by the
   planner) that the solution file is written under the module name the suite imports, before relying on `data-solution`.
5. **`run_graders.py` imports NumPy at top level** (`tools/run_graders.py:35`). The `.venv` has NumPy; the grader and its suite need
   only the standard library (`data-packages` is empty).
6. **`mutate_graders.py` needs at least three mutants** in `ledgers/S1/mutants/` and kills by the first failing test on the seeds
   given (`tools/mutate_graders.py` `mutate`). Equivalent mutants live in `ledgers/S1/equivalent/` (ruling 9), not in `mutants/`.
7. **Rung 2 needs a completion lab or a quiz** (`check_projects.py` `check_unit`). The plan uses `section.lab.completion`.
8. **Lesson hours** 6-12 (`check_pages.py` line 227); the hub's split must sum to 130 (`check_pages.py` `check_hub`).
9. **check_dag sees linked uses only.** Unlinked uses of D2, D4-D7, D9 (§4) pass the tool; the verifier reads for them.
10. **Built units link S1 concepts** (§0.3 B2). `check_dag.py` and `page_smoke.py` do not check that S7's definitions agree with S1's
    text; the verifier does (§13).
11. **Unbuilt prerequisites.** S0, CS1 and P0.1 have no built pages (§0.1). The S1 hub links to `concepts.html` anchors only, as the
    M4 hub did for its unbuilt-prerequisite links (M4 plan, Hub section).

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **Lesson count and hours.** Recommended: 10 lessons × 10 h and a 30 h project (23%). Alternatives within the rules: 9 lessons ×
   11 h and a 31 h project (24%); 10 lessons × 9 h and a 40 h project (31%). Decision: 10 × 10 + 30.
2. **Curriculum lab placement.** `yaml:653` names one lab. Recommended: `lab-S1-L10-1` (L10 defines the Sharpe ratio and its
   standard error, the two things the lab compares). One lab per lesson (M4 Q4 precedent), so 10 lesson twins plus 3 project twins.
3. **Data.** Recommended: SIMULATED throughout (§6). Optional `fx_daily` illustration is not recommended, because spot returns are
   not strategy returns (`tools/data_sources.yaml:28-29`) and the coverage claims need a known truth.
4. **D2, D5, D6 and the other outside concepts (§4).** Recommended: confirm the defaults (plain prose, no link). In particular, no
   block bootstrap, no multiple testing and no S3 stationarity term in S1; the iid assumption is stated and its limits named.
5. **Frozen interface (§5.3).** Recommended: freeze the four functions and the `sharpe_power.py` name as written, with the closed form in
   §5.3 item 2 (AC4 Q7, M4 Q7 precedent).
6. **Adversarial?** Recommended: no. The memo is not an IC defence or a debate; no 15-angle question bank.
7. **`gine1997student` for L06.** Recommended: not cited. L06 states the t-statistic's null distribution as a model assumption
   (iid normal) and names the non-normal case as outside the claim. Architect may approve `used_by` S1 after a read locator.
8. **B3 is kept; `lo2002statistics`.** Recommended: do not cite `lo2002statistics` by default. The iid standard error is a
   derivation (grade T) in L10. The architect may approve adding S1 to its `used_by` (`tools/add_reference.py:102-110`).
9. **B4, Casella edition.** Recommended: cite `casella2002statistical` with no edition or year in prose (M4 Q6 precedent); the
   architect decides whether to correct the curriculum string at `yaml:651` after checking the edition.
10. **Notation.** Recommended: confirm §2.3: `T` is periods only (registered at `notation.json:112-114`); generic sample size is `n`;
    `\Phi^{-1}` is the critical point; `\SR` and `\hSR` are per period unless annualization is stated; S7's `\PSR`, `\DSR`, `\PBO`,
    `\FWER`, `\FDR`, `\FDP` are not used.
11. **Sharpe standard error scope (B3).** Recommended: derive the general iid formula with `\gamma_3`, `\gamma_4` (the registered
    M4 meanings) in L10, state the normal case, and never use S7's term `nonnormal-sharpe-variance`.
12. **Power test convention (§5.2).** Recommended: the one-sided z-type test with the null standard error `1/\sqrt{T}`, critical value
    `\Phi^{-1}(1-\alpha)`. The memo's reconciliation then isolates variance inflation, finite-T normality and Monte Carlo error.
13. **Simulation budget and tolerance (§5.4 items 7-8).** Recommended: `n_sims <= 2000`, `periods <= 1000`, total draws at most
    4 × 10^5 per call; the band in item 8 is `4 SE` plus a finite-T tolerance measured by the builder over the instance grid and
    recorded in `ledgers/S1/scripts/`. If the measured tolerance is larger than one percentage point, the architect decides.
14. **Alternatives and their runner (§5.5).** Recommended: `tests/graders/S1/alt_1.py` to `alt_5.py` and a pytest module
    `tests/graders/S1/test_alternatives.py`, the M4 Q9 pattern. `run_graders.py` is not changed.
15. **Autograder or rubric scope.** Recommended: keep `both` with the autograder covering the four functions and the rubric covering
    the memo (the curriculum says `both`, `yaml:660`).
16. **Hub and prerequisite links.** Recommended: `concepts.html` anchors only for M4, M1, M2, CS1, S0, P0.1 (§11 item 11).
17. **Glossary.** Recommended: no GLOSSARY_REQUESTS. Terms outside the 21 (sample mean, sample variance, Wald and Wilson intervals,
    chi-square distribution, binomial distribution, Beta prior, order statistic) are plain prose or plain `<dfn>` with no `data-concept`.
18. **S7 agreement (B2).** Recommended: S1 defines the 21 names exactly; the builders read the S7 passages in §0.3 B2 first; S7 is not
    edited. The architect confirms that S7's usage is the reference wording where the two differ.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 targeted commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L03 (Builder A), L04-L06 (Builder B), L07-L08 (Builder C), L09-L10
   (Builder D), project and grader (Builder E, including the ten mutants and the five alternatives), cards (Builder F, sampled plus a
   full duplicate scan). Failing rows return to the builder that owns the file, with only the failing rows.
3. A separate scorer agent scores the exemplars blind (§5.7; FINAL-ARCHITECT-RULINGS 23). The verifier does not score them.
4. The verifier checks each S7 usage of an S1 concept (§0.3 B2) against the S1 definition.
5. Ledger at `ledgers/S1.verification.json`; verifier scripts under `ledgers/S1/scripts/`; mutants under `ledgers/S1/mutants/`;
   equivalent mutants under `ledgers/S1/equivalent/` with a README per proof (ruling 9). The closing step is a delta verification
   (FINAL-ARCHITECT-RULINGS 30), with no new mutants written by the closing round (ruling 37).
6. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1-B4 must be resolved first.

Architect decisions: pending (§12). This plan is the planner's proposal.
