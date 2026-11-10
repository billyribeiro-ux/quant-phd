# F5 build plan: The Factor Zoo & Replication (planner output, 2026-11-10)

Unit: **F5 · The Factor Zoo & Replication** · tier D · 80 h · prerequisites F2, S5, S7 · no Atlas milestone ·
debate key "Are most published factors false discoveries?" · grading `both` (autograder for adjudication engine, rubric for research note) ·
output directory `course/modules/F/F5/` (part code `F`) · lab twins `tests/labs/F5/` · ledger `ledgers/F5.verification.json`
(fragments `ledgers/F5/F5-a.json`, mutants `ledgers/F5/mutants/`).

---

## 0. Curriculum facts and metadata

| Fact | Locator |
|---|---|
| Part F, code `F`, title "Empirical Asset Pricing & Factors" | `curriculum/curriculum.json` |
| Module ID | `F5` |
| Title | The Factor Zoo & Replication |
| Tier | `D` (Doctoral) |
| Hours | 80 h total: 48 h lessons (6 lessons × 8 h) + 32 h project (40%) |
| Prerequisites | `[F2, S5, S7]` (all verified) |
| Core | Multiple testing in the cross-section, replication studies and their disagreement, factor selection. |
| Concepts introduced (6) | `factor-zoo`, `publication-bias`, `anomaly-replication-rate`, `replication-methodology-choices`, `bayesian-replication-shrinkage`, `double-selection-factor-test` |
| Primary sources | `harvey2015cross`, `hou2018replicating`, `jensen2023there`, `chen2022open`, `feng2020taming` |
| Project title | Replication-Crisis Adjudication Engine |
| Project grading | `both` (autograder and rubric) |
| Debate | "Are most published factors false discoveries?" (placed in L03) |

---

## 1. Lesson Map & Architecture

### L01: The Factor Zoo & Multiple Testing Haircuts (8 h)
- **Concept:** `factor-zoo`
- **Focus:** Historical explosion of empirical anomalies from CAPM (1964) through Cochrane (2011) zoo. The multiple testing problem in cross-sectional asset pricing. Why \(t \ge 1.96\) produces an untenable false discovery rate when 400+ anomalies are searched. Harvey, Liu & Zhu (2016) \(t\)-statistic hurdle raised to \(t > 3.0\) (\(p < 0.0027\)). Multiple-testing adjustment methods: Bonferroni, Holm step-down, Benjamini-Hochberg FDR, and Harvey-Liu-Zhu empirical haircut formulas.
- **Twin Lab:** `tests/labs/F5/lab-F5-L01-1.py` - Multiple testing haircuts on simulated candidate factor cross-sections.

### L02: Publication Bias & Anomaly Alpha Decay (8 h)
- **Concept:** `publication-bias`
- **Focus:** The mechanism of publication bias in financial economics. Journal acceptance filters conditioning on statistical significance (\(t > 2.0\)). Post-publication anomaly decay: McLean & Pontiff (2016) documenting 58% alpha decay, separated into ~26% in-sample statistical bias / p-hacking and ~32% post-publication institutional arbitrage capital inflow. Chen & Zimmermann (2020) publication bias bounds. Funnel plot asymmetry, Egger regression tests, and selection-model truncation corrections.
- **Twin Lab:** `tests/labs/F5/lab-F5-L02-1.py` - Funnel plot asymmetry test and publication bias alpha de-biasing.

### L03: The Anomaly Replication Crisis (8 h)
- **Concept:** `anomaly-replication-rate`
- **Focus:** Defining replication rate across historical anomaly claims. The clash between Hou, Xue & Zhang (2020) [65% of 452 anomalies fail at \(t \ge 1.96\) under value weighting; 85% fail under \(q\)-factor or raised hurdles] and Jensen, Kelly & Pedersen (2023) [80%+ replication rate under global evidence and Bayesian shrinkage].
- **Debate Brief:** "Are most published factors false discoveries?" (Resolution, Strongest case for, Strongest case against, Graded evidence table, State of literature, Settlement criteria).
- **Twin Lab:** `tests/labs/F5/lab-F5-L03-1.py` - Anomaly replication rate auditing across different significance hurdles and weighting schemes.

### L04: Methodological Divergence in Empirical Finance (8 h)
- **Concept:** `replication-methodology-choices`
- **Focus:** Anatomizing the methodological decisions that dictate replication outcomes: (1) equal weighting vs. value weighting; (2) universe filtering (microcap exclusion, NYSE breakpoints vs. all-stock quintiles); (3) rebalancing frequency and timing lags; (4) delisting returns adjustments (Shumway 1997); (5) benchmark control models (CAPM, FF3, FF5, \(q\)-factor). Chen & Zimmermann (2022) Open Source Cross-Sectional Asset Pricing findings.
- **Twin Lab:** `tests/labs/F5/lab-F5-L04-1.py` - Methodological divergence breakdown across portfolio weighting and microcap screens.

### L05: Hierarchical Bayesian Shrinkage of Factor Alphas (8 h)
- **Concept:** `bayesian-replication-shrinkage`
- **Focus:** Jensen, Kelly & Pedersen (2023) Bayesian framework. Modeling latent factor alphas drawn from hierarchical priors. Shrinkage formula \(\hat{\alpha}^{\text{Bayes}}_i = w_i \hat{\alpha}_i + (1 - w_i) \mu_0\), where \(w_i = \frac{\tau^2}{\tau^2 + \sigma_i^2/T}\). Empirical Bayes estimation of prior variance \(\tau^2\) via marginal maximum likelihood. Mitigating the winner's curse in backtested asset pricing.
- **Twin Lab:** `tests/labs/F5/lab-F5-L05-1.py` - Hierarchical empirical Bayes alpha shrinkage and out-of-sample MSE validation.

### L06: Double-Selection Machine Learning Factor Tests (8 h)
- **Concept:** `double-selection-factor-test`
- **Focus:** Testing whether a proposed new factor \(g_t\) provides incremental pricing power over a large library of control factors \(f_t\) (Feng, Giglio & Xiu 2020). The pitfalls of single-selection LASSO. Belloni, Chernozhukov & Hansen (2014) double-selection framework adapted to two-pass cross-sectional factor models. Asymptotic normality of post-double-selection pricing error / risk premium estimators.
- **Twin Lab:** `tests/labs/F5/lab-F5-L06-1.py` - Double-selection factor test on candidate risk factor with 50 high-dimensional controls.

---

## 2. Project Architecture: Replication-Crisis Adjudication Engine (32 h)

- **Mode:** `both` (Autograder + Rubric)
- **Ladder:**
  - Rung 1: Fully worked adjudication example for 10 candidate factors (`lab-F5-project-1.py`).
  - Rung 2: Completion problem with code blanks `___` matching `tests/labs/F5/lab-F5-project-2.py`.
  - Rung 3: Independent project: `course/modules/F/F5/grader/` (`instance.py`, `reference.py`, `starter.py`, `test_project.py`, `integrity.py`).
  - Rung 4: Stretch extensions (global multi-market transferability, transaction cost haircuts, latent IPCA factor adjustment).
- **Grader outputs & functions in reference.py:**
  1. `calculate_multiple_testing_hurdles(t_stats, method)`
  2. `evaluate_replication_matrix(returns_df, method_configs)`
  3. `hierarchical_bayes_shrinkage(alphas, standard_errors)`
  4. `double_selection_factor_test(test_assets, candidate_factor, control_factors)`
  5. `adjudicate_factor_zoo(dataset)`
- **Mutants:** 5 mutants in `ledgers/F5/mutants/` killed by `mutate_graders.py --unit F5 --seeds 0-9`.
- **Seed consistency:** Reference implementation passes 50/50 seeds (`tools/run_graders.py --unit F5 --seeds 0-49`).
