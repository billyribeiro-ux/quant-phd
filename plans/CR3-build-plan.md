# CR3 Build Plan: Credit Cycles & Macro-Credit

Unit: **CR3 · Credit Cycles & Macro-Credit** · tier M · 50 h · prerequisites CR1, S3 · grading `both` · output directory `course/modules/CR/CR3/` · lab twins `tests/labs/CR3/` · grader `course/modules/CR/CR3/grader/`.

---

## 0. Curriculum Facts & Requirements

### 0.1 Curriculum Facts (`curriculum/curriculum.json`)

| Field | Value |
|---|---|
| id | `CR3` |
| title | `Credit Cycles & Macro-Credit` |
| part | `CR` (`Credit Models`) |
| tier | `M` |
| hours | `50` |
| prereqs | `["CR1", "S3"]` |
| core | The excess bond premium, credit-market sentiment and future growth, the leveraged-loan and private-credit cycle. |
| introduces | `credit-cycle`, `gz-credit-spread`, `excess-bond-premium`, `credit-market-sentiment`, `leveraged-loan-cycle` |
| sources | `gilchrist2012credit`: Gilchrist & Zakrajšek (2012), AER 102(4); `lopezsalido2017credit`: López-Salido, Stein & Zakrajšek (2017), QJE 132(3) |
| lab | EBP as a recession predictor. |
| project | Title: "Credit-cycle indicator"; brief: "Build a credit-conditions indicator from public data, and evaluate its out-of-sample recession-forecasting power against the term spread."; deliverable: "Code plus memo."; grading: `both` |

### 0.2 Hours Breakdown

- Lessons: **5 lessons × 6 h = 30 h** (60.0% of module hours)
- Project: **20 h** (40.0% of module hours, within the 10–40% curriculum requirement)
- Total: **30 + 20 = 50 h**

### 0.3 Introduced Concepts Mapping

| Concept ID | Name | Assigned Lesson |
|---|---|---|
| `credit-cycle` | Credit cycle | L01 |
| `gz-credit-spread` | Gilchrist–Zakrajšek credit spread | L02 |
| `excess-bond-premium` | Excess bond premium | L03 |
| `credit-market-sentiment` | Credit-market sentiment and future growth | L04 |
| `leveraged-loan-cycle` | Leveraged-loan and private-credit cycle | L05 |

### 0.4 Verified Registry Keys

| Key | Citation | Role in CR3 |
|---|---|---|
| `gilchrist2012credit` | Gilchrist & Zakrajšek (2012), AER 102(4) | Core source for L02 (GZ credit spread) and L03 (Excess Bond Premium); forecasting regressions for economic activity |
| `lopezsalido2017credit` | López-Salido, Stein & Zakrajšek (2017), QJE 132(3) | Core source for L04; credit-market sentiment, high-yield issuance share, two-stage predictive spread reversal |
| `estrella1998predicting` | Estrella & Mishkin (1998), REStat 80(1) | Benchmark yield-curve term spread for recession forecasting in L03, L04, and Project |
| `gertler2015monetary` | Gertler & Karadi (2015), AEJ: Macro 7(1) | Monetary policy shocks and credit spreads, transmission through financial intermediaries |
| `huang2012much` | Huang & Huang (2012), RAPS 2(2) | Credit spread decomposition context from CR1 |
| `collindufresne2001determinants` | Collin-Dufresne, Goldstein & Martin (2001), JF 56(6) | Systematic factor in credit spread changes |
| `mian2009consequences` | Mian & Sufi (2009), QJE 124(4) | Household debt expansion, credit cycles, and geographic default evidence |
| `bharath2008forecasting` | Bharath & Shumway (2008), RFS 21(3) | Merton distance-to-default / EDF benchmark used in micro-level spread regressions |

---

## 1. Lesson Specifications

### Lesson 1: The Credit Cycle & Financial Accelerator (6 h)
- **Concept:** `<dfn id="def-credit-cycle" data-concept="credit-cycle">credit-cycle</dfn>`
- **Focus:** Macroeconomic credit fluctuations; the financial accelerator mechanism (Bernanke, Gertler & Gilchrist 1999); endogenous collateral constraints (Kiyotaki & Moore 1997); procyclical leverage and the external finance premium.
- **Key Results:**
  - Definition of credit cycle: recurrent, multi-year co-movement of aggregate credit volume, asset prices, and risk premia relative to long-term fundamentals.
  - The external finance premium equation: $s_t = \mu(Q_t K_t / N_t)$, decreasing in borrower net worth $N_t$ relative to asset value $Q_t K_t$.
  - Balance-sheet feedback loop: adverse shock $\to$ asset price $Q_t \downarrow$ $\to$ net worth $N_t \downarrow$ $\to$ external finance premium $s_t \uparrow$ $\to$ investment $I_t \downarrow$ $\to$ asset demand $Q_t \downarrow$.
  - Procyclical leverage vs countercyclical risk premia.
- **Lab 1 (`lab-CR3-L01-1.py`):** Simulating the financial accelerator: impulse response of output, capital prices, net worth, and credit spreads following a productivity shock under collateral constraints vs frictionless benchmark.

### Lesson 2: The Gilchrist-Zakrajšek Credit Spread (6 h)
- **Concept:** `<dfn id="def-gz-credit-spread" data-concept="gz-credit-spread">gz-credit-spread</dfn>`
- **Focus:** Construction of the micro-level GZ bond spread from secondary market corporate bond prices; eliminating maturity and duration mismatch via synthetic Treasury curve matching (Gürkaynak, Sack & Wright 2007).
- **Key Results:**
  - Micro bond spread $s_{it} = y_{it} - y_{it}^f$, where $y_{it}^f$ is the yield of a synthetic Treasury security with identical coupon dates and principal payment dates.
  - Cross-sectional log-linear bond pricing equation:
    $$\ln s_{ijt} = \beta' x_{ijt} + \gamma \text{EDF}_{it} + \alpha_j + \theta_t + \epsilon_{ijt}$$
  - The aggregate GZ spread: $S_t^{\text{GZ}} = \frac{1}{N_t}\sum_{i=1}^{N_t} s_{it}$.
  - Overcoming the limitations of index-level spreads (Moody's Baa/Aaa, Lehman/Barclays indices) that suffer from maturity drift and rating composition shifts.
- **Lab 1 (`lab-CR3-L02-1.py`):** Synthetic Treasury zero-curve matching for arbitrary fixed-rate corporate coupon bonds, extracting exact micro credit spreads and estimating cross-sectional regression parameters.

### Lesson 3: The Excess Bond Premium (EBP) as an Economic Leading Indicator (6 h)
- **Concept:** `<dfn id="def-excess-bond-premium" data-concept="excess-bond-premium">excess-bond-premium</dfn>`
- **Focus:** Decomposing the GZ credit spread into expected default compensation $\hat{S}_t$ and the residual Excess Bond Premium $\text{EBP}_t$; empirical forecasting of macroeconomic contractions.
- **Key Results:**
  - Decomposition: $S_t^{\text{GZ}} = \hat{S}_t + \text{EBP}_t$.
  - $\hat{S}_t$: component driven by firm-level distance-to-default / EDF and bond indenture characteristics.
  - $\text{EBP}_t$: component reflecting effective risk tolerance, risk aversion, and capital constraints of financial intermediaries.
  - Gilchrist & Zakrajšek (2012) empirical finding: EBP possesses substantial, statistically significant predictive power for economic downturns, investment drops, and unemployment spikes up to 12 months forward, whereas the default-risk component $\hat{S}_t$ shows minimal incremental forecasting power.
- **Lab 1 (`lab-CR3-L03-1.py`):** Bivariate and multivariate forecasting regressions for future GDP growth / industrial production: horse race between EBP, default component $\hat{S}_t$, and the Estrella-Mishkin term spread.

### Lesson 4: Credit Market Sentiment and Predictable Reversals (6 h)
- **Concept:** `<dfn id="def-credit-market-sentiment" data-concept="credit-market-sentiment">credit-market-sentiment</dfn>`
- **Focus:** López-Salido, Stein & Zakrajšek (2017); sentiment dynamics, extrapolative expectations in credit markets, high-yield issuance share, and predictable macroeconomic reversals.
- **Key Results:**
  - Indicators of credit market sentiment: high-yield issuance share $ISS_t$, spread compression, and depressed EBP.
  - Two-stage predictive reversal hypothesis:
    1. Stage 1: Buoyant credit market sentiment at time $t$ predictably forecasts future credit spread widening over horizons $t+2$ to $t+3$:
       $$S_{t+h} - S_t = \alpha + \beta_{\text{rev}} \text{Sentiment}_t + \epsilon_{t+h}, \quad \beta_{\text{rev}} > 0$$
    2. Stage 2: Predictable spread widening drives subsequent contraction in real economic activity:
       $$\Delta^k Y_{t+k} = \theta + \gamma_{\text{sent}} \text{Sentiment}_t + \text{lags} + u_{t+k}, \quad \gamma_{\text{sent}} < 0$$
  - Contrast with rational expectations / efficient market hypothesis: credit spread changes cannot be predicted under rational expectations, whereas sentiment models generate predictable boom-bust dynamics.
- **Lab 1 (`lab-CR3-L04-1.py`):** Two-stage regression of future spread widening on credit market sentiment proxies, and subsequent impulse response on GDP growth.

### Lesson 5: The Leveraged-Loan and Private-Credit Cycle (6 h)
- **Concept:** `<dfn id="def-leveraged-loan-cycle" data-concept="leveraged-loan-cycle">leveraged-loan-cycle</dfn>`
- **Focus:** Structural evolution of corporate credit from public bonds to syndicated leveraged loans and private credit; CLO securitization vehicles; covenant-lite (cov-lite) underwriting; EBITDA adjustments and default recoveries.
- **Key Results:**
  - Leveraged-loan institutional ecosystem: CLOs as dominant buyers ($>60\%$ of syndicated leveraged loans), providing captive, non-mark-to-market funding.
  - Underwriting erosion: proliferation of cov-lite contracts (omitting maintenance covenants like minimum interest coverage, retaining only incurrence covenants) and EBITDA add-backs.
  - Default and recovery implications: cov-lite loans delay default during distress, allowing borrower equity to burn through collateral value; resulting in depressed recovery rates ($40-50\%$ vs historical $70-80\%$).
  - Private credit illiquidity dynamics: synthetic valuations, amend-and-extend practices, and delayed macro transmission.
- **Lab 1 (`lab-CR3-L05-1.py`):** Simulating leveraged loan debt-waterfalls: cash flow coverage, cov-lite vs maintenance covenant breach timing, and loss-given-default across senior secured vs mezzanine tranches.

---

## 2. Project Specification & Grader Architecture

### 2.1 Project Overview: Credit-Cycle Indicator & Recession Forecasting (20 h)
- Ladder:
  - Rung 1 (Worked example): `lab-CR3-project-1.py`
  - Rung 2 (Completion): `lab-CR3-project-2.py`
  - Rung 3 (Independent): `reference.py` tested by `test_project.py` across 50 seeds, plus `memo.md`
  - Rung 4 (Stretch): Machine learning early-warning indicators, mixed-frequency nowcasting.
- Deliverable: Code implementing `credit_cycle.py` functions, and a case memo `memo.md` (600–900 words, 5 sections).
- Grading mode: `both` (autograder and rubric).

### 2.2 Six Core Autograder Functions (`credit_cycle.py`)
1. `decompose_credit_spread(bond_data: dict[str, list[float]]) -> dict[str, Any]`
2. `construct_credit_sentiment_index(hy_issuance_share: list[float], credit_spreads: list[float], ebp: list[float], weights: list[float] | None = None) -> dict[str, Any]`
3. `predict_spread_reversals(sentiment_series: list[float], spread_series: list[float], horizon_steps: int = 4) -> dict[str, Any]`
4. `fit_recession_probit(indicator_series: list[float], term_spread_series: list[float], recession_flags: list[int]) -> dict[str, Any]`
5. `evaluate_recession_forecasts(y_true: list[int], y_prob: list[float], threshold: float = 0.5) -> dict[str, Any]`
6. `simulate_leveraged_loan_waterfall(initial_debt: float, ebitda: float, addback_fraction: float, senior_share: float, cov_lite: bool, distress_factor: float) -> dict[str, Any]`

### 2.3 Mutants (`ledgers/CR3/mutants/`)
Five plausible student errors:
1. `m01_ebp_decomposition_sign_flip.py`: Flips sign when calculating EBP as actual spread minus predicted spread.
2. `m02_sentiment_zscore_omits_standardization.py`: Omits variance normalization when combining sentiment variables into composite index.
3. `m03_spread_reversal_lag_alignment_error.py`: Uses contemporaneous instead of forward lead spread change in reversal regression.
4. `m04_probit_link_logistic_formula_error.py`: Uses inverse logit link without negative sign in denominator or wrong likelihood sign.
5. `m05_covlite_recovery_ignores_equity_burn.py`: Grants full historical recovery rate to cov-lite loans despite absence of maintenance covenant triggers.

---

## 3. Quality & Gate Checklist

- `check_pages.py --unit CR3`: pass all meta tags, headings, ordered sections, formulas, inline labs, problems, quizzes, cards.
- `check_dag.py --unit CR3`: pass 5 introduced concepts, prerequisites [CR1, S3], no forward references.
- `check_projects.py --unit CR3`: pass 4-rung ladder, spec terms, time budget table (20 h), autograder panel, rubric table (5 criteria C1-C5), 2 exemplars, reading list.
- `run_labs.py --unit CR3`: 7 standalone twins pass and byte-match embedded output.
- `run_graders.py --unit CR3 --seeds 0-49`: 50/50 seeds pass, starter fails.
- `mutate_graders.py --unit CR3 --seeds 0-9`: 5/5 mutants killed.
- `ruff` and `mypy --strict`: clean across all files.
- `page_smoke.py --unit CR3`: pass mobile 360px and desktop 1280px without layout overflow or console errors.
