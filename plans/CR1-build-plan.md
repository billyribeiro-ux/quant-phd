# CR1 Build Plan: Structural & Reduced-Form Credit Models

Unit: **CR1 · Structural & Reduced-Form Credit Models** · tier M · 90 h · prerequisites CF2, SC3 · Atlas milestone A14 (`atlas/A14.contract.md`) · grading `autograder` · output directory `course/modules/CR/CR1/` · lab twins `tests/labs/CR1/` · grader `course/modules/CR/CR1/grader/`.

---

## 0. Curriculum Facts & Requirements

### 0.1 Curriculum Facts (curriculum/curriculum.json)

| Field | Value |
|---|---|
| id | `CR1` |
| title | `Structural & Reduced-Form Credit Models` |
| part | `CR` (`Credit Models`) |
| tier | `M` |
| hours | `90` |
| prereqs | `["CF2", "SC3"]` |
| core | Merton, Black–Cox, Leland, intensity models, distance to default, the credit-spread puzzle. |
| introduces | `merton-structural-model`, `black-cox-model`, `leland-model`, `hazard-rate`, `reduced-form-credit-model`, `distance-to-default`, `credit-spread-puzzle` |
| sources | Merton (1974), Black & Cox (1976), Leland (1994), Jarrow & Turnbull (1995), Duffie & Singleton (1999), Bharath & Shumway (2008), Collin-Dufresne, Goldstein & Martin (2001), Huang & Huang (2012) |
| lab | Merton model on a stylized firm. |
| project | Title: "Atlas A14: credit module"; brief: "Add Merton, Black–Cox and reduced-form pricers, distance to default and spread decomposition to Atlas."; deliverable: "Atlas at milestone A14."; grading: `autograder`; atlas: `A14` |

### 0.2 Hours Breakdown

- Lessons: **6 lessons × 11 h = 66 h** (73.3%)
- Project: **24 h** (26.7%, within the 10–40% curriculum requirement)
- Total: **66 + 24 = 90 h**

### 0.3 Introduced Concepts Mapping

| Concept ID | Name | Assigned Lesson |
|---|---|---|
| `merton-structural-model` | Merton structural credit model | L01 |
| `black-cox-model` | Black–Cox first-passage model | L02 |
| `leland-model` | Leland model of optimal capital structure | L03 |
| `hazard-rate` | Default intensity (hazard rate) | L04 |
| `reduced-form-credit-model` | Reduced-form credit model | L04 |
| `distance-to-default` | Distance to default | L05 |
| `credit-spread-puzzle` | Credit-spread puzzle | L06 |

### 0.4 Verified Registry Keys

| Key | Citation | Role in CR1 |
|---|---|---|
| `merton1974pricing` | Merton (1974), JF 29(2) | L01 foundation; equity as call option, zero-coupon bond pricing |
| `black1976valuing` | Black & Cox (1976), JF 31(2) | L02 first-passage time model, safety covenants |
| `leland1994corporate` | Leland (1994), JF 49(4) | L03 endogenous bankruptcy threshold, corporate taxes, bankruptcy costs |
| `jarrow1995pricing` | Jarrow & Turnbull (1995), JF 50(1) | L04 intensity-based credit risk, foreign currency analogy |
| `duffie1999modeling` | Duffie & Singleton (1999), RFS 12(4) | L04 default-adjusted discount rate, recovery of market value (RMV) |
| `bharath2008forecasting` | Bharath & Shumway (2008), RFS 21(3) | L05 distance to default, iterative vs naive Merton predictors |
| `collindufresne2001determinants` | Collin-Dufresne, Goldstein & Martin (2001), JF 56(6) | L06 determinants of credit spread changes, aggregate systematic factor |
| `huang2012much` | Huang & Huang (2012), RAPS 2(2) | L06 credit spread decomposition, structural calibration, credit spread puzzle |

---

## 1. Lesson Specifications

### Lesson 1: Structural Models: The Merton (1974) Model (11 h)
- **Concept:** `<dfn id="def-merton-structural-model" data-concept="merton-structural-model">Merton structural credit model</dfn>`
- **Focus:** Firm asset dynamics as geometric Brownian motion $dV_t = (r - \delta) V_t dt + \sigma_V V_t dW_t^\mathbb{Q}$; capital structure with equity $E$ and single zero-coupon debt issue maturing at $T$ with face value $D$.
- **Key Results:**
  - Equity is an isomorphic European call option on firm assets: $E = V\Phi(d_1) - De^{-rT}\Phi(d_2)$.
  - Debt value is $B = V - E = De^{-rT}\Phi(d_2) + V(1-\Phi(d_1)) = De^{-rT}[1 - (1/d)\Phi(-d_1) - \Phi(-d_2)]$.
  - Credit spread $s(T) = -\frac{1}{T}\ln(B / (D e^{-rT}))$.
  - Term structure of credit spreads: starts at 0 at $T \to 0$ for solvent firms ($V > D$), hump-shaped for intermediate leverage, downward-sloping for distressed firms.
- **Lab 1 (`lab-CR1-L01-1.py`):** Merton pricing, yield curve and credit spread profiles across maturities $T \in [0.5, 10]$ and leverage ratios $d = D e^{-rT}/V$.

### Lesson 2: First-Passage Time Models: Black–Cox (1976) (11 h)
- **Concept:** `<dfn id="def-black-cox-model" data-concept="black-cox-model">Black–Cox first-passage model</dfn>`
- **Focus:** Failure of Merton model to produce non-zero short-term spreads; safety covenants trigger bankruptcy before maturity whenever $V_t$ drops to an absorbing barrier $C(t) = K e^{-\gamma(T-t)}$.
- **Key Results:**
  - Distribution of first-passage time $\tau = \inf\{t > 0 : V_t \le C(t)\}$.
  - Closed-form survival probability $q(T) = \Prob(\tau > T)$.
  - Zero-coupon bond pricing with recovery payment at default.
  - Short-term credit spreads remain strictly positive as $T \to 0$ if the firm is near the barrier, resolving Merton's zero short-spread puzzle.
- **Lab 1 (`lab-CR1-L02-1.py`):** First-passage density of Brownian motion with drift, survival function, and Black–Cox credit spread term structure vs Merton.

### Lesson 3: Endogenous Default & Capital Structure: Leland (1994) (11 h)
- **Concept:** `<dfn id="def-leland-model" data-concept="leland-model">Leland model of optimal capital structure</dfn>`
- **Focus:** Endogenous bankruptcy threshold chosen rationally by equityholders rather than an exogenous covenant; perpetual debt with coupon $C$; corporate tax shield with tax rate $\tau_c$; bankruptcy costs fraction $\alpha \in [0, 1]$.
- **Key Results:**
  - Value of perpetual tax shield $TB(V) = (\tau_c C / r)(1 - (V/V_B)^{-\beta_1})$.
  - Value of bankruptcy costs $BC(V) = \alpha V_B (V/V_B)^{-\beta_1}$.
  - Smooth-pasting condition $\left.\frac{\partial E}{\partial V}\right|_{V=V_B} = 0$ identifies endogenous default threshold $V_B = \frac{1-\tau_c}{1-\tau_c+\beta_1}\frac{C}{r}$.
  - Optimal coupon $C^*$ and optimal leverage balancing tax benefits against bankruptcy costs.
- **Lab 1 (`lab-CR1-L03-1.py`):** Numerical calculation of endogenous default boundary $V_B$, firm value breakdown, and optimal capital structure.

### Lesson 4: Reduced-Form Credit Models & Intensity Pricing (11 h)
- **Concepts:** `<dfn id="def-hazard-rate" data-concept="hazard-rate">Default intensity (hazard rate)</dfn>`, `<dfn id="def-reduced-form-credit-model" data-concept="reduced-form-credit-model">Reduced-form credit model</dfn>`
- **Focus:** Jarrow & Turnbull (1995) and Duffie & Singleton (1999) intensity framework; default as a jump process with stochastic or deterministic intensity $\lambda_t$; Cox processes.
- **Key Results:**
  - Survival probability $\Prob_t^\mathbb{Q}(\tau > T) = \E_t^\mathbb{Q}[\exp(-\int_t^T \lambda_s ds)]$.
  - Recovery conventions: Recovery of Market Value (RMV), Recovery of Face Value (RFV), Recovery of Treasury (RT).
  - Duffie–Singleton pricing theorem: $P(t, T) = \E_t^\mathbb{Q}[\exp(-\int_t^T (r_s + \lambda_s(1 - R_s))ds)]$.
  - Affine term structure of credit spreads when $(r_t, \lambda_t)$ follow multidimensional CIR or Vasicek diffusions.
- **Lab 1 (`lab-CR1-L04-1.py`):** Duffie–Singleton zero-coupon bond pricing under constant vs CIR stochastic intensity, comparing RMV and RFV recovery.

### Lesson 5: Distance to Default & Empirical Implementation (11 h)
- **Concept:** `<dfn id="def-distance-to-default" data-concept="distance-to-default">Distance to default</dfn>`
- **Focus:** KMV implementation of Merton model; inverting observable equity price $E$ and equity volatility $\sigma_E$ to recover unobservable asset value $V$ and volatility $\sigma_V$; Bharath & Shumway (2008) empirical study.
- **Key Results:**
  - Two-equation simultaneous nonlinear system:
    $E = V \Phi(d_1) - D e^{-rT} \Phi(d_2)$, $\sigma_E = \frac{V \Phi(d_1)}{E} \sigma_V$.
  - Distance to Default: $\text{DD} = \frac{\ln(V/D) + (\mu - 0.5\sigma_V^2)T}{\sigma_V\sqrt{T}}$.
  - The Bharath–Shumway naive approximation ($V_{\text{naive}} = E + D$, $\sigma_{V,\text{naive}} = \frac{E}{E+D}\sigma_E + \frac{D}{E+D}(0.05 + 0.25\sigma_E)$).
  - Empirical finding: Bharath & Shumway (2008) show that naive DD performs as well as or better than computationally intensive iterative KMV DD in out-of-sample default hazard models.
- **Lab 1 (`lab-CR1-L05-1.py`):** Solving the Merton system via 2D root finding, comparing Merton DD with Bharath–Shumway naive DD across leverage regimes.

### Lesson 6: The Credit-Spread Puzzle & Spread Decomposition (11 h)
- **Concept:** `<dfn id="def-credit-spread-puzzle" data-concept="credit-spread-puzzle">Credit-spread puzzle</dfn>`
- **Focus:** Collin-Dufresne, Goldstein & Martin (2001) and Huang & Huang (2012); empirical failure of structural credit models to account for the level and dynamics of investment-grade bond spreads.
- **Key Results:**
  - Credit-spread puzzle: observed corporate spreads exceed expected default losses by an order of magnitude for investment-grade debt.
  - Collin-Dufresne, Goldstein & Martin (2001) findings: monthly credit spread changes are not driven by firm-specific structural variables; residuals have large common systematic factor ($>75\%$ variance explained by first PC).
  - Huang & Huang (2012) calibration: default risk accounts for only $20-30\%$ of 10-year investment-grade spreads (Aaa/Aa/A/Baa), leaving a massive non-credit residual (taxes, illiquidity, microstructure).
  - Multi-component spread decomposition: $s = s_{\text{EL}} + s_{\text{CRP}} + s_{\text{residual}}$.
- **Lab 1 (`lab-CR1-L06-1.py`):** Calibrating spread components, computing expected loss vs credit risk premium, and replicating Huang & Huang rating bucket decomposition.

---

## 2. Atlas A14 Specification & Grader Architecture

### 2.1 Atlas Module: `atlas.credit` (`atlas/credit.py`)

Functions to implement:
1. `merton_price(asset_value: float, debt_face: float, maturity: float, risk_free_rate: float, asset_volatility: float) -> dict[str, float]`
2. `black_cox_price(asset_value: float, debt_face: float, maturity: float, risk_free_rate: float, asset_volatility: float, barrier: float, recovery_rate: float = 0.4) -> dict[str, float]`
3. `reduced_form_price(maturity: float, risk_free_rate: float, hazard_rate: float, recovery_rate: float = 0.4, convention: str = "rmv") -> dict[str, float]`
4. `merton_distance_to_default(equity_value: float, debt_face: float, maturity: float, risk_free_rate: float, equity_volatility: float, expected_return: float | None = None) -> dict[str, float]`
5. `bharath_shumway_naive_dd(equity_value: float, debt_face: float, maturity: float, risk_free_rate: float, equity_volatility: float, expected_return: float | None = None) -> dict[str, float]`
6. `credit_spread_decomposition(market_spread: float, default_prob: float, recovery_rate: float, maturity: float, risk_premium_ratio: float = 0.5) -> dict[str, float]`

### 2.2 Grader Suite (`course/modules/CR/CR1/grader/`)
- `instance.py`: deterministic instance generator `make_instance(seed: int) -> dict` with variation in asset values, debt levels, maturities, volatilities, hazard rates, and market spreads.
- `reference.py`: full, robust implementation of `atlas.credit`.
- `starter.py`: template with raising `NotImplementedError`.
- `test_project.py`: comprehensive pytest suite validating:
  - Merton pricing invariants ($E + B = V$, $s \ge 0$, put-call parity).
  - Black–Cox boundary conditions and first-passage properties.
  - Reduced-form pricing under RMV and RFV, monoticity in $\lambda$ and recovery.
  - Merton distance to default solver precision (reconstructed equity matches input).
  - Bharath–Shumway naive DD formulas and properties.
  - Credit spread decomposition identities ($s_{\text{EL}} + s_{\text{CRP}} + s_{\text{residual}} = s$).
  - Input validation: domain checks, negative maturity/volatility error handling.

### 2.3 Mutants (`ledgers/CR1/mutants/`)
Five plausible flawed student implementations to be killed:
1. `m01_merton_debt_formula_sign_flip.py`: Flips sign in debt formula or uses $V - E$ with wrong put payoff.
2. `m02_black_cox_barrier_discount_error.py`: Ignores exponential discounting on early default recovery payoff.
3. `m03_reduced_form_rfv_formula_error.py`: Omits integration over default times or uses RMV formula when convention is RFV.
4. `m04_merton_dd_drift_sign_error.py`: Uses minus sign for expected drift in distance-to-default formula.
5. `m05_spread_decomp_residual_clamping.py`: Allows negative residual spread or flips expected loss formula.

---

## 3. Verification Plan

1. Verify all HTML pages pass `check_pages.py --unit CR1`.
2. Verify DAG integrity with `check_dag.py --unit CR1`.
3. Verify project specification with `check_projects.py --unit CR1`.
4. Run all lab twins with `run_labs.py --unit CR1`.
5. Run grader across seeds 0–49 with `run_graders.py --unit CR1 --seeds 0-49`.
6. Run mutation testing with `mutate_graders.py --unit CR1 --seeds 0-49`.
7. Type check and lint with `.venv/bin/mypy` and `.venv/bin/ruff`.
8. Verify UI rendering and responsive layout with `page_smoke.py --unit CR1`.
